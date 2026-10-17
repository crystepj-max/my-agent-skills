# task +complete

> **Prerequisite:** If the current context does not already contain the applicable shared rules for this CLI version, use the host-available file-reading method to consult `../../lark-shared/SKILL.md`; reuse a matching version already in context. Any host-available file-reading method is acceptable. Apply the shared rules for authentication, global parameters, and security rules.

Mark a task as completed.

## Recommended Commands

```bash
# Complete a task
lark-cli task +complete --task-id "<task_guid>"

# A task applink is accepted directly; the CLI extracts its guid query value
lark-cli task +complete --task-id "https://applink.larksuite.com/client/todo/task?guid=<task_guid>"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid-or-applink>` | Yes | Task OpenAPI GUID or a task applink containing `guid=`. Display task IDs such as `t104121` / `suite_entity_num` are rejected. |

## Workflow

1. Confirm the task to complete.
2. Execute the command.
3. Read `data.status`, `data.completed_at`, and `data.already_completed` from the result. `already_completed: true` means the shortcut observed an already-completed task and skipped the PATCH.
4. Do not routinely call `task tasks get` when the result already reports `status: done` and a non-zero `completed_at`. Query details only if confirmation fields are absent or the user explicitly asks for a full verification.

> [!CAUTION]
> This is a write operation. Execute when the user's request or an earlier approval covers the target, action, fields and impact. Matching authorization remains valid across turns; ask only for a material detail or scope change that is still unresolved. If the CLI returns exit 10 / `confirmation_required`, follow `lark-shared` and preserve the required confirmation flag.
