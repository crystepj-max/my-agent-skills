#!/usr/bin/env bash
set -euo pipefail

TIMEOUT=180
APP_ID=2868840
AGENT_URL="http://127.0.0.1:8080"
READY_GRACE=30

while [[ $# -gt 0 ]]; do
  case "$1" in
    --timeout)
      TIMEOUT="$2"
      shift 2
      ;;
    --app-id)
      APP_ID="$2"
      shift 2
      ;;
    --agent-url)
      AGENT_URL="$(printf '%s' "$2" | sed 's:/*$::')"
      shift 2
      ;;
    --ready-grace)
      READY_GRACE="$2"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

HEALTH_URL="$AGENT_URL/health"
ACTIONS_URL="$AGENT_URL/actions/available"
STATE_URL="$AGENT_URL/state"

game_process_running() {
  pgrep -f "Slay the Spire 2" >/dev/null 2>&1
}

agent_listener_snapshot() {
  local port output status
  if ! port="$(python3 -c 'from urllib.parse import urlparse; import sys; u=urlparse(sys.argv[1]); h=(u.hostname or "").lower(); p=u.port or {"http":80,"https":443}.get(u.scheme); sys.exit(2) if h not in {"127.0.0.1","localhost","::1"} or p is None else print(p)' "$AGENT_URL")"; then
    echo "Cannot determine a safe local listener port for $AGENT_URL" >&2
    return 2
  fi
  if ! command -v lsof >/dev/null 2>&1; then
    echo "lsof is unavailable; refusing to assume the local port is unused." >&2
    return 2
  fi

  if output="$(lsof -nP -iTCP:"$port" -sTCP:LISTEN 2>&1)"; then
    if [[ -n "$output" ]]; then
      printf '%s\n' "$output" >&2
      return 0
    fi
    return 1
  else
    status=$?
    if [[ "$status" -eq 1 && -z "$output" ]]; then
      return 1
    fi
    echo "Could not verify listener state for TCP/$port." >&2
    if [[ -n "$output" ]]; then
      printf '%s\n' "$output" >&2
    fi
    return 2
  fi
}

wait_for_ready() {
  local deadline="$1"
  while (( SECONDS < deadline )); do
    if is_agent_ready; then
      echo "STS2 ready via STS2-Agent"
      return 0
    fi
    sleep 3
  done
  return 1
}

is_agent_ready() {
  curl -fsS --max-time 5 "$HEALTH_URL" >/dev/null 2>&1 || return 1
  curl -fsS --max-time 5 "$STATE_URL" >/dev/null 2>&1 || return 1
  curl -fsS --max-time 5 "$ACTIONS_URL" >/dev/null 2>&1 || return 1
}

probe_endpoint() {
  local name="$1"
  local url="$2"
  if curl -fsS --max-time 5 "$url" >/dev/null 2>&1; then
    echo "[PASS] $name: $url"
  else
    echo "[FAIL] $name: $url" >&2
  fi
}

diagnose_readiness() {
  echo "STS2-Agent readiness probes:" >&2
  probe_endpoint "health" "$HEALTH_URL" >&2
  probe_endpoint "state" "$STATE_URL" >&2
  probe_endpoint "actions" "$ACTIONS_URL" >&2
  if command -v sts2 >/dev/null 2>&1; then
    if sts2 ping >/dev/null 2>&1; then
      echo "[INFO] sts2 ping succeeded, but it is not used as readiness proof." >&2
    else
      echo "[INFO] sts2 ping failed." >&2
    fi
  fi
}

diagnose_listener() {
  local state
  if agent_listener_snapshot; then
    echo "[INFO] Listener process details are candidates only; no signal was sent." >&2
  else
    state=$?
    if [[ "$state" -eq 1 ]]; then
      echo "[INFO] No local listener was reported for the configured port." >&2
    else
      echo "[INFO] Listener state could not be verified; startup fails closed." >&2
    fi
  fi
}

if is_agent_ready; then
  echo "STS2-Agent already ready"
  exit 0
fi

if game_process_running; then
  echo "STS2 process already running; waiting for readiness before taking any recovery action."
  grace_deadline=$((SECONDS + READY_GRACE))
  if (( grace_deadline > SECONDS + TIMEOUT )); then
    grace_deadline=$((SECONDS + TIMEOUT))
  fi
  if wait_for_ready "$grace_deadline"; then
    exit 0
  fi

  echo "STS2 process remains unready; this script will not signal or restart it." >&2
  diagnose_readiness
  diagnose_listener
  exit 1
fi

if agent_listener_snapshot; then
  echo "A process is already listening on the Agent port; refusing to start another game until its identity and owner are verified." >&2
  exit 1
else
  listener_state=$?
  if [[ "$listener_state" -ne 1 ]]; then
    echo "Listener state is unknown; refusing to launch STS2." >&2
    exit 1
  fi
fi

start_steam_best_effort() {
  if open -a Steam 2>/dev/null; then
    return 0
  fi
  if [[ -d /Applications/Steam.app ]]; then
    open /Applications/Steam.app 2>/dev/null || true
  fi
}

launch_game_best_effort() {
  if open "steam://run/$APP_ID" 2>/dev/null; then
    return 0
  fi
  if open -b com.valvesoftware.steam "steam://run/$APP_ID" 2>/dev/null; then
    return 0
  fi
  return 0
}

start_steam_best_effort
sleep 5
launch_game_best_effort

deadline=$((SECONDS + TIMEOUT))
if wait_for_ready "$deadline"; then
  exit 0
fi

echo "Timed out waiting for STS2 readiness after $TIMEOUT seconds" >&2
diagnose_readiness
diagnose_listener
exit 1
