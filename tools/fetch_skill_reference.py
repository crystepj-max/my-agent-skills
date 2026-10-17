#!/usr/bin/env python3
"""Save upstream skill snapshots outside every skill discovery/source tree.

This is a reference downloader. It never installs, refreshes, or activates skills.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import shutil
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path, PurePosixPath

REPO = "mattpocock/skills"
SKILLS = {
    "wizard": "skills/engineering/wizard",
    "to-questionnaire": "skills/productivity/to-questionnaire",
    "wait-what": "skills/productivity/wait-what",
}
DEFAULT_OUTPUT_ROOT = Path.home() / ".local/share/agent-skills/upstream-snapshots"


def protected_roots(home: Path | None = None, repo_root: Path | None = None,
                    policy_path: Path | None = None) -> list[Path]:
    home = Path(home or Path.home()).expanduser()
    repo_root = Path(repo_root or Path(__file__).resolve().parents[1]).expanduser()
    fallback = [
        home / ".agents/skills", home / ".codex/skills", home / ".claude/skills",
        home / ".config/claude/skills", home / ".workbuddy/skills",
        home / ".openclaw/skills", home / ".hermes/skills", repo_root / "my-skills",
    ]
    policy_path = Path(policy_path or repo_root / "inventory/skill-policy.json")
    if not policy_path.is_file():
        return fallback
    config = json.loads(policy_path.read_text())
    roots: list[Path] = []

    def expand(value: str) -> Path:
        if value.startswith("~/"):
            return home / value[2:]
        if value.startswith("project:"):
            project, separator, relative = value[8:].partition("/")
            if not separator or not project or not relative:
                raise ValueError(f"无效的项目技能路径：{value}")
            relative_path = PurePosixPath(relative)
            if relative_path.is_absolute() or any(part in {"", ".", ".."} for part in relative_path.parts):
                raise ValueError(f"项目技能路径不能越出登记根目录：{value}")
            return expand(config["projects"][project]) / Path(*relative_path.parts)
        path = Path(value)
        return path if path.is_absolute() else repo_root / path

    roots.append(expand(config["pool"]))
    roots.extend(expand(path) for path in config.get("agent_roots", []))
    roots.extend(expand(path) for path in config.get("discovery_roots", []))
    roots.extend(expand(item["source"]) for item in config.get("skills", []) if item.get("source"))
    for project_root in config.get("projects", {}).values():
        expanded_project = expand(project_root)
        roots.append(expanded_project)
        roots.extend(expanded_project / relative for relative in config.get("project_entry_roots", []))
    roots.append(repo_root / "my-skills")
    return roots or fallback


def resolved(path: Path) -> Path:
    return Path(path).expanduser().resolve(strict=False)


def overlaps(left: Path, right: Path) -> bool:
    """True when either path is the other path or one of its ancestors."""
    return left == right or left in right.parents or right in left.parents


def validate_output_root(output_root: Path, protected: list[Path]) -> Path:
    target = resolved(output_root)
    for root in protected:
        blocked = resolved(root)
        if overlaps(target, blocked):
            raise ValueError(
                f"输出路径与技能发现目录、my-skills 或其祖先/子目录重叠：{target}"
            )
    return target


def safe_relative_path(value: str) -> Path:
    posix = PurePosixPath(value)
    if posix.is_absolute() or not posix.parts or any(part in {"", ".", ".."} for part in posix.parts):
        raise ValueError(f"上游快照包含不安全路径：{value!r}")
    return Path(*posix.parts)


def request_bytes(url: str, opener=urllib.request.urlopen) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "agent-skill-reference-snapshot"})
    response = opener(request, timeout=30)
    try:
        return response.read()
    finally:
        close = getattr(response, "close", None)
        if close:
            close()


def tree_snapshot(branch: str, output_root: Path, opener=urllib.request.urlopen,
                  home: Path | None = None, repo_root: Path | None = None,
                  policy_path: Path | None = None) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9._-]+", branch) or branch in {".", ".."}:
        raise ValueError("branch 只能包含英数、点、下划线和连字符")
    protected = protected_roots(home, repo_root, policy_path)
    safe_root = validate_output_root(output_root, protected)
    safe_root.mkdir(parents=True, exist_ok=True)

    commit_url = f"https://api.github.com/repos/{REPO}/commits/{urllib.parse.quote(branch, safe='')}"
    commit_data = json.loads(request_bytes(commit_url, opener))
    commit_sha = commit_data.get("sha")
    if not isinstance(commit_sha, str) or not re.fullmatch(r"[0-9a-fA-F]{40,64}", commit_sha):
        raise ValueError("GitHub 未返回有效 commit SHA；未写入快照")
    # Pin the tree and every blob to one immutable commit, not the moving branch.
    tree_url = f"https://api.github.com/repos/{REPO}/git/trees/{commit_sha}?recursive=1"
    tree_data = json.loads(request_bytes(tree_url, opener))
    tree_sha = tree_data.get("sha")
    if not isinstance(tree_sha, str) or not re.fullmatch(r"[0-9a-fA-F]{40,64}", tree_sha):
        raise ValueError("GitHub 未返回有效 tree SHA；未写入快照")
    tree_entries = tree_data.get("tree")
    if not isinstance(tree_entries, list):
        raise ValueError("GitHub tree 响应格式错误；未写入快照")
    if tree_data.get("truncated") is True:
        raise ValueError("GitHub 返回截断的 tree；不能保存为完整快照")

    files_by_skill: dict[str, list[dict]] = {}
    for skill, prefix in SKILLS.items():
        files_by_skill[skill] = [
            item for item in tree_entries
            if item.get("type") == "blob" and isinstance(item.get("path"), str)
            and item["path"].startswith(prefix + "/")
        ]
        if not files_by_skill[skill]:
            raise ValueError(f"上游 tree 中没有找到 {skill} 文件；未写入快照")

    snapshot_name = f"{REPO.split('/')[1]}-{branch}-{commit_sha[:12]}"
    final_path = safe_root / snapshot_name
    validate_output_root(final_path, protected)
    if final_path.exists() or final_path.is_symlink():
        raise FileExistsError(f"快照已存在，不覆盖：{final_path}")

    staging = Path(tempfile.mkdtemp(prefix=".skill-reference-", dir=safe_root))
    manifest = {
        "repository": f"https://github.com/{REPO}.git",
        "branch": branch,
        "commit_sha": commit_sha,
        "tree_sha": tree_sha,
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "kind": "reference-only",
        "skills": {},
    }
    try:
        for skill, prefix in SKILLS.items():
            records = []
            skill_root = staging / skill
            for item in files_by_skill[skill]:
                source_path = item["path"]
                relative = safe_relative_path(source_path[len(prefix) + 1:])
                target = skill_root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                data = request_bytes(
                    f"https://raw.githubusercontent.com/{REPO}/{commit_sha}/{urllib.parse.quote(source_path, safe='/')}",
                    opener,
                )
                target.write_bytes(data)
                records.append({
                    "path": relative.as_posix(),
                    "sha256": hashlib.sha256(data).hexdigest(),
                    "size": len(data),
                })
            manifest["skills"][skill] = records
        (staging / "snapshot.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
        final_path.parent.mkdir(parents=True, exist_ok=True)
        os.rename(staging, final_path)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return final_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", default="main", help="上游分支快照；不表示安装或正式版本")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT,
                        help="独立参考快照目录；禁止指向发现目录、my-skills 或其祖先")
    args = parser.parse_args(argv)
    try:
        destination = tree_snapshot(args.branch, args.output_root)
    except Exception as exc:
        parser.error(str(exc))
    print(f"已保存只读参考快照：{destination}")
    print("未修改、安装或激活任何技能。请使用 compare_skill_reference.py 进行只读对照。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
