# mail +send

> **前置条件：** 先阅读 [`../../lark-shared/SKILL.md`](../../lark-shared/SKILL.md) 了解认证、全局参数和安全规则。

发送新邮件，支持：
- 纯文本或 HTML 正文
- 抄送/密送
- 本地文件附件（`--attach`）
- 内嵌图片（`--inline`，CID 可用随机字符串）

本 skill 对应 shortcut：`lark-cli mail +send`。

## CRITICAL — 发送工作流（必须遵循）

**CRITICAL — 编辑邮件内容前，确保当前上下文已包含 [lark-mail-html.md](lark-mail-html.md) 的完整书写规范；若没有，使用宿主可用的文件读取方式完整查看当前版本。上下文已有匹配版本可复用，无需特定工具。**

此命令默认**只保存草稿**，不会发送邮件。需要发送时，有两种合规方式：

**方式 A** — 用户只要求起草、或正文/收件人等关键细节尚未确定时，先创建草稿供审阅：
```bash
lark-cli mail +send --to '<收件人>' --subject '<主题>' --body '<正文>'
```
→ 返回 `draft_id`

向用户展示邮件摘要（收件人、主题、正文预览）；如果用户想先看效果，可引导其去飞书邮件里打开该草稿查看详情。

用户明确授权发送该收件人集合与正文版本后，发送该草稿。若用户此前的请求或批准已覆盖同一收件人、发件身份、主题、正文、附件和发送时间，沿用该授权，不重复询问：
```bash
lark-cli mail user_mailbox.drafts send --params '{"user_mailbox_id":"me","draft_id":"<Step 1 返回的 draft_id>"}'
```

**方式 B** — 用户明确要求发送，且现有授权覆盖收件人、发件身份、主题、正文、附件和发送时间时，可直接使用 `--confirm-send`。CLI exit 10 后先按 `lark-shared-high-risk-approval.md` 核对同一授权，再按 `hint` 重试：
```bash
lark-cli mail +send --to '<收件人>' --subject '<主题>' --body '<正文>' --confirm-send
```

没有覆盖该次发送的用户授权时，不得发送。对象、正文版本或影响发生变化时，展示差异并只请求对变化部分授权。

## 命令

```bash
# 保存为草稿（默认行为，不发送）— HTML 格式推荐
lark-cli mail +send --to 'alice@example.com' --subject '周报' \
  --body '<p>本周进展：</p><ul><li>完成 A 模块</li><li>修复 3 个 bug</li></ul>'

# 保存为草稿并抄送
lark-cli mail +send --to 'alice@example.com' --cc 'bob@example.com' --subject '状态更新' --body '<b>已完成</b>'

# 发送（仅在用户请求/批准覆盖本邮件时使用；重复确认无需按轮次重新获取）
lark-cli mail +send --to 'alice@example.com' --subject '周报' \
  --body '<p>本周进展如下...</p>' --confirm-send

# 保存带附件的草稿
lark-cli mail +send --to 'alice@example.com' --subject '请查收' --body '<p>见附件</p>' --attach './report.pdf' --attach './logs.zip'

# 保存带内嵌图片的草稿（推荐：直接用相对路径，自动解析）
lark-cli mail +send --to 'alice@example.com' --subject '预览图' --body '<img src="./logo.png" />'

# 纯文本邮件（仅在内容极简时使用）
lark-cli mail +send --to 'alice@example.com' --subject '确认' --body '收到，谢谢'

# Dry Run（仅打印请求，不执行）
lark-cli mail +send --to 'alice@example.com' --subject '测试' --body '<p>test</p>' --dry-run
```

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--to '<email>'` | 是 | 收件人邮箱。多个收件人请重复传 `--to`，每次只放一个地址，参数值用单引号包住 |
| `--subject <text>` | 是 | 邮件主题 |
| `--body <text>` | 二选一 | 邮件正文。推荐使用 HTML 获得富文本排版；也支持纯文本（自动检测）。使用 `--plain-text` 可强制纯文本模式。支持 `<img src="./local.png" />` 相对路径自动解析为内嵌图片（仅支持相对路径，不支持绝对路径）。与 `--body-file` 互斥 |
| `--body-file <path>` | 二选一 | 从文件读取邮件正文 HTML（相对路径，仅限 cwd 子树）。与 `--body` 互斥。文件大小上限 32 MB |
| `--from <email>` | 否 | 发件人邮箱地址（EML From 头）。使用别名（send_as）发信时，设为别名地址并配合 `--mailbox` 指定所属邮箱。默认读取邮箱主地址 |
| `--mailbox <email>` | 否 | 邮箱地址，指定草稿所属的邮箱（默认回退到 `--from`，再回退到 `me`）。当发件人（`--from`）与邮箱不同时使用。可通过 `accessible_mailboxes` 查询可用邮箱 |
| `--cc '<email>'` | 否 | 抄送邮箱。多个抄送请重复传 `--cc`，每次只放一个地址，参数值用单引号包住 |
| `--bcc '<email>'` | 否 | 密送邮箱。多个密送请重复传 `--bcc`，每次只放一个地址，参数值用单引号包住 |
| `--plain-text` | 否 | 强制纯文本模式，忽略 HTML 自动检测。不可与 `--inline` 同时使用。纯文本模式下也会自动追加纯文本签名（HTML 签名经 `PlainTextFromHTML` 转换，内联图片丢弃） |
| `--attach '<path>'` | 否 | 附件文件路径。多个附件请重复传 `--attach`，每次只放一个相对路径，参数值用单引号包住；按传入顺序追加。当附件导致 EML 总大小超过 25 MB 时，超出部分自动上传为超大附件（HTML 邮件插入下载卡片，纯文本邮件追加下载链接），单个文件上限 3 GB |
| `--inline '<json>'` | 否 | 高级用法：手动指定内嵌图片 CID 映射。多个 inline 图片请重复传 `--inline`，每次只放一个 JSON object，并用单引号包住：`'{"cid":"mycid","file_path":"./logo.png"}'`。`file_path` 必须是相对路径；CID 应唯一，例如随机十六进制字符串；在 body 中用 `<img src="cid:mycid">` 引用。推荐直接在 `--body` 中使用 `<img src="./path" />`（自动解析）。不可与 `--plain-text` 同时使用 |
| `--signature-id <id>` | 否 | 签名 ID。附加邮箱签名到正文末尾。运行 `mail +signature` 查看可用签名。与 `--no-signature` 互斥 |
| `--no-signature` | 否 | 跳过默认签名自动追加。与 `--signature-id` 互斥，同时使用时返回参数校验错误（退出码 2） |
| `--priority <level>` | 否 | 邮件优先级：`high`、`normal`、`low`。省略或 `normal` 时不设置优先级 |
| `--event-summary <text>` | 否 | 日程标题。设置此参数即在邮件中嵌入日程邀请（text/calendar）。需同时设置 `--event-start` 和 `--event-end` |
| `--event-start <time>` | 条件必填 | 日程开始时间（ISO 8601，如 `2026-04-20T14:00+08:00`） |
| `--event-end <time>` | 条件必填 | 日程结束时间（ISO 8601） |
| `--event-location <text>` | 否 | 日程地点 |
| `--confirm-send` | 否 | 直接发送（默认只保存草稿）。仅在用户授权覆盖收件人、发件身份、内容版本、附件和时间后使用 |
| `--send-time <timestamp>` | 否 | 定时发送时间，Unix 时间戳（秒）。需至少为当前时间 + 5 分钟。配合 `--confirm-send` 使用可定时发送邮件 |
| `--request-receipt` | 否 | 请求已读回执（RFC 3798 Message Disposition Notification）。在出站 EML 里写 `Disposition-Notification-To: <sender>` 头。收件人的邮件客户端**可能**弹出提示询问是否回执、可能自动发送、也可能忽略——送达不保证 |
| `--dry-run` | 否 | 仅打印请求，不执行 |

### 日程邀请约束

使用 `--event-*` 时需满足以下条件：

- `--event-summary`、`--event-start`、`--event-end` 必须同时出现或同时不出现
- 与 `--send-time` 互斥，不可同时使用（日程邀请必须立即发送，否则收件人可能在日程开始后才收到）
- 不可与 `--bcc` 同时使用：日程参会人（ATTENDEE）仅来自 To 和 Cc，Bcc 收件人不在参会人列表中、无法 RSVP，且该组合将导致邮件发送失败。需要邀请某人参加日程请用 `--to` 或 `--cc`；如只想告知而不邀请，请单独发一封无日程的邮件

## 返回值

**草稿模式（默认）：**

```json
{
  "ok": true,
  "data": {
    "draft_id": "草稿ID",
    "tip": "draft saved. To send: lark-cli mail user_mailbox.drafts send --params '{...}'"
  }
}
```

草稿模式下，只要结果不是直接发信而是产出了草稿，就应给用户展示草稿打开链接。当前应以 `create` / `edit` / `send` 链路返回的链接信息为准，不要把 `user_mailbox.drafts get` 当作拿草稿打开链接的来源。如果返回中带有 `reference`，应把链接与 `draft_id` 一并返回；当前没有链接时，静默处理，不要伪造链接。

**发送模式（`--confirm-send`）：**

```json
{
  "ok": true,
  "data": {
    "message_id": "邮件ID",
    "thread_id": "会话ID"
  }
}
```

可选字段：

- `automation_send_disable_reason`：发送被邮箱自动化设置拦截时返回的原因
- `automation_send_disable_reference`：发送被拦截时的草稿打开链接
- `recall_available` / `recall_tip`：发送成功后若返回可撤回提示，按需参考 [lark-mail-recall](lark-mail-recall.md)

字段语义：

- 若返回中包含 `automation_send_disable_reason` / `automation_send_disable_reference`，说明邮件未真正发出，而是被邮箱设置拦截。此时应直接向用户展示原因和草稿打开链接，不要继续假设已经发送成功
- 若返回中包含 `recall_available: true`，说明该邮件支持撤回；仅当用户明确要求撤回时，读取 [lark-mail-recall](lark-mail-recall.md) 并执行撤回流程

## 典型场景

### 场景 1：用户说"帮我写一封邮件给 Alice"（只创建草稿）
```bash
lark-cli mail +send --to 'alice@example.com' --subject '周报' --body '<p>本周进展如下...</p>'
```
→ 返回草稿结果时，如输出中带有草稿打开链接，则一起展示给用户；如果当前输出没有链接，则静默处理。如果用户想先看效果，可去飞书邮件 UI 中打开草稿查看详情。

### 场景 2：用户说“发邮件给 Alice 说收到了”（需要发送）

用户已明确要求发送，且收件人解析唯一、正文和发件身份无歧义时，直接使用发送模式；不再先创建草稿后重复询问。用户只要求起草，或正文含未授权承诺/敏感信息、收件人仍有多个候选时，才先建草稿并询问具体缺口。

```bash
# 先确认 Alice 唯一解析到此地址；发送范围由用户直接请求覆盖
lark-cli mail +send --to 'alice@example.com' --subject '收到' --body '<p>已收到，谢谢！</p>' --confirm-send
```

### 场景 3：用户说“下午 3 点给 Alice 发一封周报”（定时发送）

若 Alice 已唯一解析，用户给出邮件内容与发送时间，且时区/时间含义明确，直接按授权定时发送。只在收件人、正文或时间存在实质歧义时才先建草稿并询问该缺口。

```bash
# 直接请求的定时范围已明确；时间戳使用用户时区换算后的 unix timestamp
lark-cli mail +send --to 'alice@example.com' --subject '周报' --body '<p>本周进展如下...</p>' --send-time <unix_timestamp> --confirm-send
```

### 场景 4：用户说"等等，先不发那封邮件了"（取消定时发送）
```bash
# 取消定时发送（取消后邮件变回草稿）
lark-cli mail user_mailbox.drafts cancel_scheduled_send --params '{"user_mailbox_id":"me","draft_id":"<draft_id>"}'
```
→ 取消成功后邮件恢复为草稿状态，用户可重新编辑或在之后重新发送。

## 发送后跟进

邮件发送后，分两种情况处理：

- 若返回中有 `automation_send_disable_reason` / `automation_send_disable_reference`：说明发送被邮箱设置拦截，应直接告诉用户原因并提供草稿打开链接，**不要**调用 `send_status`

### 立即发送（无 `--send-time`）

若返回非空 `message_id`，调用：

```bash
lark-cli mail user_mailbox.messages send_status --params '{"user_mailbox_id":"me","message_id":"<发送返回的 message_id>"}'
```

状态码：1=正在投递, 2=投递失败重试, 3=退信, 4=投递成功, 5=待审批, 6=审批拒绝。向用户简要报告各收件人投递结果，异常状态需重点提示。

### 定时发送（指定了 `--send-time`）

定时发送不会立即产生 `message_id`，因此 `send_status` 在定时发送成功后会返回"待发送"状态，**不建议在定时发送后立即查询**。可在预定发送时间后再查询投递状态。

如需取消定时发送，可在预定时间前调用取消接口：

```bash
lark-cli mail user_mailbox.drafts cancel_scheduled_send --params '{"user_mailbox_id":"me","draft_id":"<draft_id>"}'
```

**取消后邮件会变回草稿**，可继续编辑或在之后重新发送。

## 实现说明

- 使用 EML 构建器生成完整 MIME 邮件并 base64url 编码后发送。
- `--attach` 作为普通附件添加。多个附件请重复传 `--attach`，每次只放一个相对路径。
- `--inline` 手动指定 inline 图片时，多个图片请重复传 `--inline`，每次只放一个 JSON object。每项需提供 `cid`（唯一标识符，可用随机十六进制字符串）和 `file_path`（相对路径），作为 inline part 嵌入邮件。
- **超大附件**：当附件导致 EML 总大小（headers + body + inline images + attachments，base64 编码后）超过 25 MB 时，超出的文件自动通过 `medias/upload_*` API 上传到云端。HTML 邮件插入与飞书客户端一致的下载卡片；纯文本邮件追加包含文件名、大小和下载链接的文本块。单个文件上限 3 GB，总附件数量上限 250 个。

## 相关命令

- `lark-cli mail +reply` — 回复邮件
- `lark-cli mail +reply-all` — 回复全部
- `lark-cli mail +forward` — 转发邮件
- `lark-cli mail user_mailbox.messages list` — 列出邮件
