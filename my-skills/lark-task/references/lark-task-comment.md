# task +comment

> **Prerequisite:** If the current context does not already contain the applicable shared rules for this CLI version, use the host-available file-reading method to consult `../../lark-shared/SKILL.md`; reuse a matching version already in context. Any host-available file-reading method is acceptable. Apply the shared rules for authentication, global parameters, and security rules.

Add a comment to an existing task.

## Recommended Commands

```bash
# Add a comment
lark-cli task +comment --task-id "<task_guid>" --content "Looks good!"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--task-id <guid>` | Yes | The task GUID to comment on. For Feishu task applinks, use the `guid` query parameter, not the `suite_entity_num` / display task ID like `t104121`. |
| `--content <text>` | Yes | The text content of the comment. |

## Workflow

1. Confirm the task and comment content.
2. Execute `lark-cli task +comment --task-id "..." --content "..."`
3. Report success and comment ID.

> [!CAUTION]
> This is a write operation. Execute when the user's request or an earlier approval covers the target, action, fields and impact. Matching authorization remains valid across turns; ask only for a material detail or scope change that is still unresolved. If the CLI returns exit 10 / `confirmation_required`, follow `lark-shared` and preserve the required confirmation flag.
