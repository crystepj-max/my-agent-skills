---
name: setup-matt-pocock-skills
description: "为当前仓库配置 issue 跟踪方式、分诊角色映射与领域文档约定。仅在用户要求设置或调整这类项目配置时使用。"
disable-model-invocation: true
---

# Setup Matt Pocock's Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker**: where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels**: the strings used for the five canonical triage roles
- **Domain docs**: where `GLOSSARY.md` and ADRs live, and the consumer rules for reading them

Inspect the repository before changing it. Use current files and clear defaults to complete a requested setup; ask only when a missing choice would change how work is tracked or documented. Preserve existing configuration and local edits.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config`: is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root: does either exist? Is there already an `## Agent skills` section in either?
- `GLOSSARY.md` and `GLOSSARY-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/`: does this skill's prior output already exist?
- `.scratch/`: a sign that a local-markdown issue tracker convention is already in use
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals: a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. These are present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Resolve only meaningful choices

Summarise the current state and the defaults you will use. Do not turn every section into a required interview.

Lead with a recommendation when a choice remains. Skip choices already settled by repository configuration or the user's request.

**Section A: Issue tracker.**

> Explainer: The issue tracker is where this repository tracks incoming work. `triage` and `wayfinder` can use this configuration when present; other skills can also finish without an issue tracker.

Infer the default from the current repository. Use GitHub when the remote points to GitHub, GitLab when it points to GitLab, and local Markdown when there is no supported remote. Ask only if multiple remotes or existing configuration leave the intended tracker unclear. Supported choices are:

- **GitHub**: issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab**: issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown**: issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.): ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off**. Leave it off and don't raise it: a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B: Triage label vocabulary.** Skip this section if `triage` is not installed or the repository does not use it.

If it is installed, read the existing label configuration. Keep it if it maps the canonical roles. If none exists, use the canonical defaults unless the tracker or repository already uses different labels; ask only if that choice remains unclear.

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. If the existing tracker already uses labels with the same meaning (for example, `bug:triage` for `needs-triage`), record that mapping rather than creating duplicate labels.

**Section C: Domain docs.** Default to **single-context** (one `GLOSSARY.md` + `docs/adr/` at the repo root) unless repository structure already shows several distinct domains.

Use **multi-context** (a root `GLOSSARY-MAP.md` pointing to per-context `GLOSSARY.md` files) only when exploration found multiple domains with different terms. Ask only if the existing structure does not reveal how they should be grouped.

### 3. Prepare the requested configuration

Prepare only the files needed for the requested setup:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)

If a material choice remains unresolved, show that exact draft and ask about that choice before writing. Otherwise proceed and report the files changed.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, follow the repository's documented agent-instruction convention. If none exists, use `AGENTS.md` as the general-purpose default and add only the small references needed for this configuration.

Do not create a competing instruction file when the repository already has an authoritative one. Keep existing instructions and edit only the `## Agent skills` block if one exists.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout: "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md): GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md): GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md): local-markdown issue tracker
- [triage-labels.md](./triage-labels.md): label mapping (only if `triage` is installed)
- [domain.md](./domain.md): domain doc consumer rules + layout

For another issue tracker, use its existing connector and repository documentation when available; ask for the missing workflow details only when they cannot be inferred safely.

### 5. Verify and hand off

Check that every referenced file exists, links resolve, and the repository instruction file points to the actual configuration. Tell the user what is now configured and which active skills read it. They can edit `docs/agents/*.md` directly later; re-run this skill only when they want to switch or revise a choice.
