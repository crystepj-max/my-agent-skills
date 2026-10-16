#!/usr/bin/env python3
"""Batch scanner — runs du -sk on multiple children at once.

Use when the original scan.py (which does one `du -sk` per child) is too slow.
Passing up to 20 child paths per call reduces process launches, but the actual
runtime depends on the host, filesystem, permissions, and directory contents.

Still strictly read-only. Outputs the same JSON schema as scan.py.
"""
import json, os, re, shutil, subprocess, sys, time

HOME = os.path.expanduser("~")

def human(kb):
    n = float(kb) * 1024
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit not in ("B", "KB") else f"{int(n)} {unit}"
        n /= 1024

def run(cmd, timeout=180):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout).stdout
    except Exception:
        return ""

def du_batch(children, timeout=120):
    """Run du -sk on a batch of up to 20 paths at once."""
    results = []
    cmd = ["du", "-sk"] + children
    out = run(cmd, timeout=timeout)
    for line in out.strip().split("\n"):
        m = re.match(r'^\s*(\d+)\s+(.+)$', line)
        if not m:
            continue
        kb = int(m.group(1))
        child_path = m.group(2).strip()
        name = os.path.basename(child_path)
        results.append({"name": name, "path": child_path, "size_kb": kb, "size_h": human(kb)})
    return results

def du_children_batched(path, min_kb=51200, limit=40, batch_size=20):
    """List children, then du -sk in batches."""
    if not os.path.isdir(path):
        return []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return [{"name": "(permission denied)", "path": path, "size_kb": 0, "size_h": "?", "denied": True}]
    children = [os.path.join(path, n) for n in entries
                if n not in (".", "..") and not os.path.islink(os.path.join(path, n))]
    if not children:
        return []
    results = []
    for i in range(0, len(children), batch_size):
        batch = children[i:i+batch_size]
        results.extend(du_batch(batch))
    results = [r for r in results if r["size_kb"] >= min_kb]
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results[:limit]

def du_children(path, min_kb=51200, limit=40):
    """Original one-by-one du -sk (slow but reliable for small dirs)."""
    if not os.path.isdir(path):
        return []
    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return [{"name": "(permission denied)", "path": path, "size_kb": 0, "size_h": "?", "denied": True}]
    results = []
    for name in entries:
        if name in (".", ".."):
            continue
        child = os.path.join(path, name)
        if os.path.islink(child):
            continue
        out = run(["du", "-sk", child], timeout=120)
        m = re.match(r"\s*(\d+)", out)
        if not m:
            continue
        kb = int(m.group(1))
        if kb < min_kb:
            continue
        results.append({"name": name, "path": child, "size_kb": kb, "size_h": human(kb)})
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results[:limit]

def system_info():
    info = {}
    info["os"] = "macOS " + run(["sw_vers", "-productVersion"]).strip()
    info["build"] = run(["sw_vers", "-buildVersion"]).strip()
    arch = run(["uname", "-m"]).strip()
    brand = run(["sysctl", "-n", "machdep.cpu.brand_string"]).strip()
    info["arch"] = f"Apple Silicon (arm64){' / ' + brand if brand else ''}" if arch == "arm64" else f"{arch}{' / ' + brand if brand else ''}"
    info["user"] = os.environ.get("USER", "")
    info["home"] = HOME
    try:
        t, u, f = shutil.disk_usage("/")
        info["disk_total"], info["disk_used"], info["disk_free"] = human(t // 1024), human(u // 1024), human(f // 1024)
    except:
        info["disk_total"] = info["disk_used"] = info["disk_free"] = "?"
    dinfo = run(["diskutil", "info", "/"])
    fs = re.search(r"File System Personality:\s*(.+)", dinfo)
    info["filesystem"] = fs.group(1).strip() if fs else "APFS"
    pm = re.search(r"Purgeable Space:\s*([\d.,]+ \w+)", dinfo)
    info["purgeable"] = pm.group(1).strip() if pm else ""
    info["disk_name"] = "Macintosh HD"
    info["disks"] = [{"name": "Macintosh HD", "total": info["disk_total"], "used": info["disk_used"], "free": info["disk_free"]}]
    return info

def dev_caches():
    paths = [
        "~/Library/Caches/pip", "~/Library/Caches/uv", "~/.cache", "~/.cargo",
        "~/.npm", "~/.pnpm-store", "~/.gradle", "~/.m2",
        "~/Library/Developer/Xcode/DerivedData", "~/Library/Developer/CoreSimulator",
        "~/Library/Developer/Xcode/iOS DeviceSupport", "~/Library/pnpm",
        "~/go/pkg", "~/.docker",
    ]
    results = []
    for p in paths:
        path = os.path.expanduser(p)
        if not os.path.isdir(path):
            continue
        out = run(["du", "-sk", path], timeout=180)
        m = re.match(r'\s*(\d+)', out)
        if not m:
            continue
        kb = int(m.group(1))
        if kb < 51200:
            continue
        results.append({"name": os.path.basename(path.rstrip("/")) or path,
                        "path": path, "size_kb": kb, "size_h": human(kb)})
    results.sort(key=lambda r: r["size_kb"], reverse=True)
    return results

def main():
    started = time.time()
    system = system_info()
    groups = {}

    # Home: use one-by-one (few children, each large)
    print("Scanning home...", file=sys.stderr)
    groups["home"] = du_children(HOME, min_kb=102400)

    # Library, Caches, App Support, Downloads: few children, one-by-one OK
    lib = os.path.join(HOME, "Library")
    print("Scanning Library...", file=sys.stderr)
    groups["library"] = du_children(lib)

    print("Scanning Caches...", file=sys.stderr)
    groups["caches"] = du_children(os.path.join(lib, "Caches"))

    print("Scanning App Support...", file=sys.stderr)
    groups["app_support"] = du_children(os.path.join(lib, "Application Support"))

    print("Scanning Downloads...", file=sys.stderr)
    groups["downloads"] = du_children(os.path.join(HOME, "Downloads"))

    # Containers: can have 600+ children — use batched mode
    print("Scanning Containers (batched, 20 per du call)...", file=sys.stderr)
    groups["containers"] = du_children_batched(os.path.join(lib, "Containers"))

    # Group Containers
    print("Scanning Group Containers...", file=sys.stderr)
    groups["group_containers"] = du_children(os.path.join(lib, "Group Containers"))

    # Applications
    print("Scanning Applications...", file=sys.stderr)
    groups["applications"] = du_children("/Applications", min_kb=102400)

    # Dev caches
    print("Scanning dev_caches...", file=sys.stderr)
    groups["dev_caches"] = dev_caches()

    data = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "system": system,
        "groups": groups,
        "scan_seconds": round(time.time() - started, 1),
    }
    print(json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
