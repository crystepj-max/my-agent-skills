# CLI duplicate detection recipes

These commands are for read-only discovery. Replace placeholders with the exact executable or package name. Use them only for package managers present on the machine. Do not print environment variables, credentials, or command arguments that contain secrets.

## List commands in PATH order

```bash
type -a <bin>
command -v <bin>
```

The first resolved path is normally selected by the current shell, but aliases, shell functions, wrappers, project runtime managers, and cached command hashes can affect resolution. If needed, inspect the active shell's hash table without changing it.

## Inspect candidate paths and symlinks

```bash
ls -la -- <candidate-path>
realpath <candidate-path>
```

Use the platform's equivalent when `realpath` is unavailable. Do not assume a prefix such as `/opt/homebrew` or `~/.nvm`; discover the actual path from the command and package manager.

## Check package-manager ownership

Use the manager's read-only list/info command for the identified package, such as `brew list --versions <formula>`, `brew info <formula>`, `npm ls -g --depth=0`, `pipx list`, or the equivalent for the installed tool. A `Not installed` receipt does not prove files are orphaned; check whether another manager owns that same location before acting.

For Node packages, inspect the exact runtime's `npm root -g`, then the package's `package.json` version. Runtime-specific global packages can coexist under different Node installations. A recent modification time alone does not prove which copy is current.

## Inspect runtime selection

For nvm, `nvm current`, `nvm ls`, and `nvm alias default` show the active/default runtime. Do not change the default alias as part of discovery. Check project version files (such as `.nvmrc`, `.node-version`, `mise.toml`, or the project package manager file) before treating a globally installed copy as the desired one.

## Check references to a candidate path

Search only likely launch/config files with a literal path search and list the matching file names first. Inspect minimal relevant values with secrets redacted. Exclude credentials, `.env`, keychain, browser data, caches, backups and historical logs.

## Removal boundary

Use the manager that owns the exact package when the user has explicitly authorized the uninstall. If a manual removal is unavoidable, state the single exact executable/package path and preserve sibling packages; never remove an entire runtime or shared package directory. This document contains no fixed user-specific paths.
