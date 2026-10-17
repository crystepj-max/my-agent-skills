# task +reminder

> **Prerequisite:** If the current context does not already contain the applicable shared rules for this CLI version, use the host-available file-reading method to consult `../../lark-shared/SKILL.md`; reuse a matching version already in context. Any host-available file-reading method is acceptable. Apply the shared rules for authentication, global parameters, and security rules.
> **Priority:** For creating or modifying task reminder times, prioritize using this `+reminder` shortcut over other task update methods. It provides a more reliable and direct way to manage reminders.

Manage task reminders. Set new reminders or remove existing ones. Note that setting a task reminder requires a due date.

## Recommended Commands

```bash
# Set a reminder (e.g., 30 minutes before due)
lark-cli task +reminder --task-id "<task_guid>" --set "30"

# Set a reminder (e.g., 1 hour before due)
lark-cli task +reminder --task-id "<task_guid>" --set "1h"

# Remove all reminders
lark-cli task +reminder --task-id "<task_guid>" --remove "true"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid>` | Yes | The task GUID to modify. For Feishu task applinks, use the `guid` query parameter, not the `suite_entity_num` / display task ID like `t104121`. |
| `--set <val>` | No | Relative fire minutes before the due time. Supports numbers (e.g., `30`) or units (e.g., `15m`, `1h`, `1d`). |
| `--remove <bool>` | No | If set to `true`, removes all existing reminders from the task. |

## Workflow

1. Confirm the task and reminder action.
2. Execute the command.
3. Report success.

> [!CAUTION]
> This is a write operation. Execute when the user's request or an earlier approval covers the target, action, fields and impact. Matching authorization remains valid across turns; ask only for a material detail or scope change that is still unresolved. If the CLI returns exit 10 / `confirmation_required`, follow `lark-shared` and preserve the required confirmation flag.
