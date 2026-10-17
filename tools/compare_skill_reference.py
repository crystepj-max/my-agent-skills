#!/usr/bin/env python3
"""Read-only comparison of an independent upstream snapshot and its mapping."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any


def digest_tree(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in sorted(root.rglob("*")):
        relative = item.relative_to(root).as_posix()
        if item.is_symlink():
            value = ("link:" + os.readlink(item)).encode()
        elif item.is_file():
            value = item.read_bytes()
        else:
            continue
        result[relative] = hashlib.sha256(value).hexdigest()
    return result


def manager_fingerprint(root: Path) -> str:
    """Match scripts/manage-skills.py fingerprint() for the preserved copy.

    相对路径统一用 POSIX 形式参与哈希。str(Path) 会带上平台分隔符
    （Windows `agents\\openai.yaml`、macOS `agents/openai.yaml`），
    同一份内容在两个平台会得到不同指纹，导致比对工具误报漂移。
    """
    digest = hashlib.sha256()
    ignored = {".git", "__pycache__", ".DS_Store", "node_modules", ".venv"}
    entries: list[tuple[str, bytes]] = []
    for item in root.rglob("*"):
        relative = item.relative_to(root)
        if any(part in ignored for part in relative.parts):
            continue
        if item.is_symlink():
            value = ("link:" + os.readlink(item)).encode()
        elif item.is_file():
            value = item.read_bytes()
        else:
            continue
        entries.append(("/".join(relative.parts), value))
    for key, value in sorted(entries):
        digest.update(key.encode() + b"\0" + value + b"\0")
    return digest.hexdigest()


def expand(path: str, repo_root: Path, home: Path,
           projects: dict[str, str] | None = None) -> Path:
    if path.startswith("~/"):
        return home / path[2:]
    if path.startswith("project:"):
        project_key, separator, relative = path[8:].partition("/")
        if not separator or not project_key or not relative:
            raise ValueError(f"無效的项目路径：{path}")
        relative_path = PurePosixPath(relative)
        if relative_path.is_absolute() or any(part in {"", ".", ".."} for part in relative_path.parts):
            raise ValueError(f"项目路径不能越出登记根目录：{path}")
        project_root = (projects or {}).get(project_key)
        if not project_root:
            raise ValueError(f"登记中没有项目路径：{project_key}")
        return expand(project_root, repo_root, home, projects) / relative
    candidate = Path(path)
    return candidate if candidate.is_absolute() else repo_root / candidate


def compare(policy_path: Path, skill_name: str, new_snapshot: Path,
            repo_root: Path, home: Path | None = None) -> dict[str, Any]:
    home = Path(home or Path.home()).resolve()
    repo_root = Path(repo_root).resolve()
    config = json.loads(policy_path.read_text())
    skill = next((item for item in config.get("skills", []) if item.get("name") == skill_name), None)
    reference = next((item for item in config.get("reference_copies", [])
                      if item.get("name") == skill_name or item.get("maps_to") == skill_name), None)
    if not skill or not reference:
        raise ValueError(f"登记中没有 {skill_name} 的第一方来源与原版参考映射")

    projects = config.get("projects", {})
    old_root = expand(reference["destination"], repo_root, home, projects).resolve()
    first_party_root = expand(skill["source"], repo_root, home, projects).resolve()
    new_root = Path(new_snapshot).expanduser().resolve(strict=True)
    protected = []
    for value in [config.get("pool"), *config.get("agent_roots", []),
                  *(item.get("source") for item in config.get("skills", []) if item.get("source"))]:
        if value:
            protected.append(expand(value, repo_root, home, projects))
    for project_root in projects.values():
        expanded_project = expand(project_root, repo_root, home, projects)
        protected.append(expanded_project)
        for relative in config.get("project_entry_roots", []):
            protected.append(expanded_project / relative)
    protected.append(repo_root / "my-skills")
    for root in protected:
        root = root.resolve(strict=False)
        if new_root == root or new_root in root.parents or root in new_root.parents:
            raise ValueError("新快照必须独立于发现目录、my-skills 及其祖先")
    if not old_root.is_dir() or not first_party_root.is_dir() or not new_root.is_dir():
        raise ValueError("原版参考、第一方来源和新快照都必须是已存在目录")

    recorded = reference.get("fingerprint")
    if recorded and manager_fingerprint(old_root) != recorded:
        raise ValueError("登记的原版参考指纹与现场不符；先调查漂移，不继续对照")

    old_files, new_files = digest_tree(old_root), digest_tree(new_root)
    old_set, new_set = set(old_files), set(new_files)
    return {
        "skill": skill_name,
        "upstream": skill.get("upstream") or reference.get("upstream"),
        "first_party_source": str(first_party_root),
        "preserved_reference": str(old_root),
        "new_reference_snapshot": str(new_root),
        "changes": {
            "added": sorted(new_set - old_set),
            "removed": sorted(old_set - new_set),
            "changed": sorted(path for path in old_set & new_set if old_files[path] != new_files[path]),
            "unchanged": sorted(path for path in old_set & new_set if old_files[path] == new_files[path]),
        },
        "action": "review only; no copy, install, restore, registry edit, or activation",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=Path(__file__).resolve().parents[1] / "inventory/skill-policy.json")
    parser.add_argument("--name", required=True, help="登记中的 skill 名称")
    parser.add_argument("--new-snapshot", required=True, type=Path, help="独立快照内该技能的目录")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    try:
        report = compare(args.policy, args.name, args.new_snapshot, args.repo_root)
    except Exception as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
