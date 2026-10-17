---
name: duplicate-cli-unify
description: "当同一个命令行工具（如 Claude Code、Codex 或任何 npm/node 类 CLI）被多个包管理器重复安装时使用——最常见的是 nvm 全局安装与 Homebrew 安装并存，导致版本混乱、残留旧副本、或自动更新静默写入错误路径。提供检测、分析、决策、修复的完整流程，把工具统一到单一安装源。"
---

# Duplicate CLI Unify

## Purpose

Diagnose and resolve duplicate installations of the same CLI tool that originate from two or more package managers on one machine (e.g., an nvm global `npm install -g` alongside a Homebrew cask). The typical symptom is `type -a <tool>` returning more than one path, or the tool reporting an unexpected version because the active PATH selects a different copy than expected.

## When to use

- `type -a <bin>` shows multiple candidates for the same command.
- The executable version does not match the version reported by the package manager or project runtime.
- Two package channels (nvm, Homebrew, npm global, pipx, asdf, apt, etc.) are both present for the same binary.

## Workflow

### 1. Discover without changing the system

Start with the command name, package name if known, the exact shell/session where the wrong version appears, and any PATH or version-manager context in the request. Do not assume multiple paths are redundant: project-pinned runtimes, per-node installs, wrappers, and intentional test versions can all be valid.

Use the read-only commands in [references/detection.md](references/detection.md) to collect:

- every resolved command path in order, plus symlink targets;
- the version reported by each executable, where safe;
- package-manager ownership and package version for each actual package directory;
- the active shell's PATH and any project runtime pin relevant to the command.

Modification time is supporting context, not proof that a package is stale or auto-updated. Do not invoke an updater to test ownership. Redact tokens and any credential-like arguments from command output.

### 2. Explain the observed behavior

Describe which copy the user's current shell will launch and why. Distinguish duplicate files from PATH shadowing, wrappers, package-manager records that do not match disk state, and per-runtime package scopes. Check whether scripts or shell startup files intentionally select the path. If evidence does not establish ownership or usage, keep that copy untouched and mark the uncertainty.

### 3. Choose a target source

Compare the options against the user's actual needs: update behavior, version pinning, project compatibility, node/runtime switching, permissions and maintenance cost. Present a recommended source and the concrete consequences, plus a keep-both option if coexistence is harmless. Do not assume Homebrew, nvm, npm or any other manager is universally preferable.

### 4. Prepare authorized remediation

Before any uninstall, manual file removal, PATH change or runtime pin:

1. list the exact package name, manager, executable path and package directory that would change;
2. verify the package manager owns only that package and does not share the target directory with sibling packages;
3. explain impact and a way to reinstall or restore the configuration;
4. obtain the user's explicit authorization for those exact targets and changes.

Prefer the owning package manager's uninstall command with the intended runtime explicitly selected. If package-manager ownership is ambiguous, do not manually remove files; prepare the issue and ask for the missing ownership decision. Manual removal is a last resort for an exact untracked executable/package path after explicit authorization. Never remove a whole `node_modules`, runtime, Homebrew, nvm, or version-manager directory. Pin a default runtime only if the user selected that behavior and confirmed the exact version.

### 5. Verify the chosen behavior

After authorized changes, inspect the package-manager records and run `type -a <bin>` in the current shell and a new interactive shell. Run the kept executable's `--version` if it is a read-only query. Do not trigger self-updates, change channels, sign into services, or create external side effects merely to validate installation. Report any remaining intentional second copy and its purpose.

## Resources

- `references/detection.md` — portable read-only discovery commands for PATH, symlinks, package managers, versions and runtime pins.

- `references/detection.md` — exact command recipes for detection (paths, versions, mod times, brew tracking check, nvm alias).
