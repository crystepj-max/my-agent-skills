# task +tasklist-create

> **Prerequisite:** If the current context does not already contain the applicable shared rules for this CLI version, use the host-available file-reading method to consult `../../lark-shared/SKILL.md`; reuse a matching version already in context. Any host-available file-reading method is acceptable. Apply the shared rules for authentication, global parameters, and security rules.

Create a new tasklist, and optionally batch create tasks within it.

## Recommended Commands

```bash
# Create an empty tasklist
lark-cli task +tasklist-create --name "Q1 Goals"

# Create a tasklist and add members
lark-cli task +tasklist-create --name "Project A" --member "ou_xxx,ou_yyy"

# Create a tasklist and batch create tasks within it
lark-cli task +tasklist-create --name "Launch Checklist" --data '[{"summary": "Code Review", "assignee": "ou_aaa"}, {"summary": "Deploy", "assignee": "ou_bbb"}]'
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--name <text>` | Yes | The name of the tasklist. |
| `--member <ids>` | No | Comma-separated list of user `open_id`s to add as editors. |
| `--data <json>` | No | JSON array of task definitions to create and add to the tasklist automatically. |

## Workflow

1. Confirm the tasklist name, members, and tasks (if any).
2. Execute the command `lark-cli task +tasklist-create ...`.
3. Report success, including the new tasklist ID and the result of the batch task creation.

> [!CAUTION]
> This is a write operation. Execute when the user's request or an earlier approval covers the target, action, fields and impact. Matching authorization remains valid across turns; ask only for a material detail or scope change that is still unresolved. If the CLI returns exit 10 / `confirmation_required`, follow `lark-shared` and preserve the required confirmation flag.
