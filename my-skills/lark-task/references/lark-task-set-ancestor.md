# task +set-ancestor

> **Prerequisite:** If the current context does not already contain the applicable shared rules for this CLI version, use the host-available file-reading method to consult `../../lark-shared/SKILL.md`; reuse a matching version already in context. Any host-available file-reading method is acceptable. Apply the shared rules for authentication, global parameters, and security rules.

Set a parent task for a task, or clear the parent to make it independent.

## Recommended Commands

```bash
# Set a parent task
lark-cli task +set-ancestor --task-id "guid_1" --ancestor-id "guid_2"

# Clear the parent task
lark-cli task +set-ancestor --task-id "guid_1"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid>` | Yes | The task GUID to update. |
| `--ancestor-id <guid>` | No | The parent task GUID. Omit it to clear the ancestor. |

## Workflow

1. Confirm the child task and, if applicable, the ancestor task.
2. Execute `lark-cli task +set-ancestor ...`
3. Report the updated task GUID and whether the ancestor was set or cleared.

> [!CAUTION]
> This is a write operation. Execute when the user's request or an earlier approval covers the target, action, fields and impact. Matching authorization remains valid across turns; ask only for a material detail or scope change that is still unresolved. If the CLI returns exit 10 / `confirmation_required`, follow `lark-shared` and preserve the required confirmation flag.

