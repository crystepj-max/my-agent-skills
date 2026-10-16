# task +tasklist-members

> **Prerequisite:** If the current context does not already contain the applicable shared rules for this CLI version, use the host-available file-reading method to consult `../../lark-shared/SKILL.md`; reuse a matching version already in context. Any host-available file-reading method is acceptable. Apply the shared rules for authentication, global parameters, and security rules.

Manage tasklist members (editors/owners).

## Recommended Commands

```bash
# Add a member
lark-cli task +tasklist-members --tasklist-id "tl_xxx" --add "ou_aaa"

# Remove a member
lark-cli task +tasklist-members --tasklist-id "tl_xxx" --remove "ou_aaa"

# Replace all members exactly
lark-cli task +tasklist-members --tasklist-id "tl_xxx" --set "ou_aaa,ou_bbb"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--tasklist-id <id>` | Yes | The GUID of the tasklist, or a full AppLink URL. |
| `--add <ids>` | No | Comma-separated list of user `open_id`s to add as members. |
| `--remove <ids>` | No | Comma-separated list of user `open_id`s to remove from members. |
| `--set <ids>` | No | Comma-separated list of user `open_id`s to exactly set as members (replaces all existing). |

## Workflow

1. Confirm the tasklist and members to add/remove/set.
2. Execute the command.
3. Report success.

> [!CAUTION]
> This is a write operation. Execute when the user's request or an earlier approval covers the target, action, fields and impact. Matching authorization remains valid across turns; ask only for a material detail or scope change that is still unresolved. If the CLI returns exit 10 / `confirmation_required`, follow `lark-shared` and preserve the required confirmation flag.
