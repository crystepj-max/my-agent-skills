---
name: scaffold-exercises
description: "按当前项目约定创建课程练习目录、题目、解答与讲解，并运行项目实际提供的检查。当用户想搭建练习或课程章节时使用。"
---

# Scaffold Exercises

Create the requested exercise structure inside the user's named project and follow its existing conventions. Validate with the project's actual lint command when one exists. Do not stage or commit changes.

## Directory naming

- **Sections**: `XX-section-name/` inside `exercises/` (e.g., `01-retrieval-skill-building`)
- **Exercises**: `XX.YY-exercise-name/` inside a section (e.g., `01.03-retrieval-with-bm25`)
- Section number = `XX`, exercise number = `XX.YY`
- Names are dash-case (lowercase, hyphens)

## Exercise variants

Each exercise needs at least one of these subfolders:

- `problem/` - student workspace with TODOs
- `solution/` - reference implementation
- `explainer/` - conceptual material, no TODOs

When stubbing, default to `explainer/` unless the plan specifies otherwise.

## Required files

Each subfolder (`problem/`, `solution/`, `explainer/`) needs a `readme.md` that:

- Is **not empty** (must have real content, even a single title line works)
- Has no broken links

When stubbing, create a minimal readme with a title and a description:

```md
# Exercise Title

Description here
```

If the subfolder has code, it also needs a `main.ts` (>1 line). But for stubs, a readme-only exercise is fine.

## Workflow

1. Resolve the output root from the user's request or the open project. Inspect the current tree, package scripts, course conventions, and working-tree state before writing. Reuse any names, section numbers, exercise count, and variant types the user already supplied. Ask only when a missing detail would change the requested learning outcome or structure.
2. Preserve existing exercises. Add only the requested sections and variants; do not renumber unrelated material. Use the project's naming convention if it differs from the defaults below.
3. Create the minimum complete content for each requested variant. A stub is appropriate only when the user asked for scaffolding; otherwise write the actual learning prompt or explanation from the provided plan. Check relative links after creating files.
4. Find the real validation path from package scripts, project docs, Makefile, or available local CLI help. Run the narrow exercise lint if present. The original command pnpm ai-hero-cli internal lint belongs to the AI Hero project and is not a universal dependency. Do not install a missing CLI or package just to make this skill's historical command available.
5. If no exercise-specific linter exists, perform available structural and link checks and clearly report that the project has no runnable exercise lint. Do not call an absent lint a failure or a pass.
6. Review the final diff and confirm all requested paths and variants exist. Leave changes unstaged and uncommitted.

## Lint rules summary

The list below describes the original AI Hero linter, not a repository-wide contract. Confirm the current project's actual linter and documentation before applying it. If that CLI is not present, use these checks only as a useful content checklist and report that the original lint command was unavailable.

- Exercise folders follow the project's expected shape.
- At least one requested variant exists.
- The primary variant has a non-empty readme.md.
- Relative links resolve.
- No placeholder files or commands forbidden by the project's linter are introduced.
- A code-bearing variant has the entry file required by the project; a readme-only stub is acceptable only when scaffolding was requested.

## Moving/renaming exercises

When the user requests renumbering or moving exercises, update only the named paths and references. A normal filesystem rename leaves changes unstaged; Git can detect renames from file content when reviewing. Use git mv only when the user or repository workflow explicitly requires staging the rename, since git mv updates the index.

## Example: stubbing from a plan

Given a plan like:

```
Section 05: Memory Skill Building
- 05.01 Introduction to Memory
- 05.02 Short-term Memory (explainer + problem + solution)
- 05.03 Long-term Memory
```

Create:

```bash
mkdir -p exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer
mkdir -p exercises/05-memory-skill-building/05.02-short-term-memory/{explainer,problem,solution}
mkdir -p exercises/05-memory-skill-building/05.03-long-term-memory/explainer
```

Then create readme stubs:

```
exercises/05-memory-skill-building/05.01-introduction-to-memory/explainer/readme.md -> "# Introduction to Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/explainer/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/problem/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.02-short-term-memory/solution/readme.md -> "# Short-term Memory"
exercises/05-memory-skill-building/05.03-long-term-memory/explainer/readme.md -> "# Long-term Memory"
```
