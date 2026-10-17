---
name: lark-apps
version: 1.0.0
description: "妙搭（Spark/Miaoda）应用开发与托管。仅在用户明确选择妙搭、当前任务位于一个妙搭应用项目，或任务必须使用妙搭专属资源时触发；涵盖应用开发、应用数据库与文件存储、开放 API Key、访问范围、协作者与角色、线上日志指标、环境变量和应用自动化。普通 HTML、网站、PPT、deck、原型或视觉设计请求不会仅因交付形式触发本技能，也不会因此自动创建妙搭应用。"
metadata:
  requires:
    bins: ["lark-cli"]
  cliHelp: "lark-cli apps --help; lark-cli apps +<cmd> --help"
---

# apps (v1)

妙搭应用属于用户资产。默认用 `--as user`；认证、scope、exit-10、高风险确认、`_notice` 等通用处理遵循 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)：若当前上下文尚未包含适用于本机 CLI 版本的规则，用宿主可用的文件读取方式查看；已有匹配版本可复用，无需特定工具。不要在本 skill 里复制。妙搭应用有两条开发路径：**本地开发**（拉源码本地写）/ **云端会话**（妙搭 AI 生成）。

## 身份与授权

妙搭应用是用户的个人资产，统一 `--as user`（见开头）。已有用户身份可用时直接执行业务命令，**不要为了预防权限问题主动重新登录**，否则可能中断原任务并触发不必要的设备授权。仅当 CLI 明确返回未登录或缺少本域 scope 时，一次性执行：

```bash
lark-cli auth login --domain apps
```

因缺权限失败（`error.subtype == "missing_scope"`）时的通用处理见 [`../lark-shared/SKILL.md`](../lark-shared/SKILL.md)，同样按 `--domain apps` 授权；授权成功后只恢复原业务操作，不扩展任务范围。

## 意图路由

按具体操作查命令（开发路径先用下方「选择开发路径」判定表定好再进来取命令）：

| 用户意图 | 先用 | 按需读取 |
|---|---|---|
| 创建**新**应用资产、拿 app_id | `+create` | [`lark-apps-create.md`](references/lark-apps-create.md) |
| 找已有 app_id、按名字过滤应用 | `+list --keyword <name>` | [`lark-apps-list.md`](references/lark-apps-list.md) |
| 查单个应用详情（类型、名称、发布状态等） | `+get --app-id <app_id>` | [`lark-apps-get.md`](references/lark-apps-get.md) |
| 改应用名或描述 | `+update` | [`lark-apps-update.md`](references/lark-apps-update.md) |
| 用户已选择妙搭的 HTML 应用 / 创意模式 — 在指定妙搭应用中制作 HTML 页面、deck、mockup、原型或视觉材料 | 加载 [`creative-design/creative-design.md`](creative-design/creative-design.md)（开发步骤与可选发布流程） | [`creative-design/creative-design.md`](creative-design/creative-design.md) |
| 旧版存量 HTML 应用（无 Git 管理）继续上传已有静态产物 | `+html-publish`（仅兼容旧链路；新建 html / 创意模式 / creative-design 产物不得使用） | [`lark-apps-html-publish.md`](references/lark-apps-html-publish.md) |
| 开发已有应用 / 初始化本地仓库（开发方式已定为本地后；先解析 app_id，勿 `+create` 新建） | `+init`（或手动 `+git-credential-init` + 原生 git）。**执行前必读** [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md)，含端到端流程和领域规则 | [`lark-apps-init.md`](references/lark-apps-init.md), [`lark-apps-git-credential.md`](references/lark-apps-git-credential.md) |
| 只要一份源码快照、不做本地开发；或要取**别人分享给你的**应用源码（你对其仓库无权限） | `+export`（下载 zip；不配 git 凭证、不建工作区）。要继续开发用 `+init` 而非本命令 | [`lark-apps-export.md`](references/lark-apps-export.md) |
| 本地开发时 `.env.local` 损坏/丢失，重新拉取启动期环境变量 | `+env-pull` | [`lark-apps-env-pull.md`](references/lark-apps-env-pull.md) |
| 管理应用环境变量（查看/设置/删除） | `+env-list`, `+env-set`, `+env-delete` | [`lark-apps-env.md`](references/lark-apps-env.md) |
| 查线上日志、Trace、请求数、错误率、延迟、CPU、memory、PV/UV/访问量 | `+log-list`, `+log-get`, `+trace-list`, `+trace-get`, `+metric-list`, `+analytics-list` | [`lark-apps-observability.md`](references/lark-apps-observability.md) |
| 看表 / 看结构 / 初始化多环境 / 导入导出数据 / 变更追溯 / 行级审计 / dev→online 发布 / 时间点恢复 / 查 DB 用量 | `+db-table-list`、`+db-table-get`、`+db-env-create`、`+db-data-export`/`+db-data-import`、`+db-changelog-list`、`+db-audit-status`/`+db-audit-enable`/`+db-audit-disable`/`+db-audit-list`、`+db-env-diff`/`+db-env-migrate`、`+db-recovery-diff`/`+db-recovery-apply`、`+db-quota-get` | [`lark-apps-db.md`](references/lark-apps-db.md) |
| 逐条执行 SQL（SELECT / DML / DDL）；建表 / 改表 / 写 SQL 的平台规范 | `+db-execute` | [`lark-apps-db-execute.md`](references/lark-apps-db-execute.md)（含「平台 SQL 规范」：审计列 / RLS / `user_profile` / 禁用 SQL / PG 陷阱） |
| 管理应用文件存储：上传/下载本地文件、列出/查看/删除已存文件、生成临时分享链接、查存储用量 | `+file-upload`/`+file-download`/`+file-list`/`+file-get`/`+file-sign`/`+file-delete`/`+file-quota-get` | [`lark-apps-file.md`](references/lark-apps-file.md) |
| 调试应用运行时缓存：查看/删除单个业务 key、清空指定环境缓存 | `+cache-get`/`+cache-delete`/`+cache-clear` | [`lark-apps-cache.md`](references/lark-apps-cache.md) |
| **部署/上线应用**（"部署""上线""推上去并部署""发布到云端"）；查发布状态/历史 | 本地开发链路先按 [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md) 确认本次改动已 git commit + git push，再用 `+release-create` / `+release-get`；查历史用 `+release-list` | [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md), [`lark-apps-release-create.md`](references/lark-apps-release-create.md), [`lark-apps-release-get.md`](references/lark-apps-release-get.md), [`lark-apps-release-list.md`](references/lark-apps-release-list.md) |
| 设置或查看运行时可见范围 | `+access-scope-set`, `+access-scope-get` | 对应 access-scope reference |
| 管理应用协作者（列出/添加/改权限/移除）或协作权限设置 | `+member-list`, `+member-add`, `+member-update`, `+member-remove`, `+member-settings-get`, `+member-settings-set` | 本文「应用协作者与协作权限设置」 |
| 创意模式（html）应用的评论相关操作 | 创意模式应用评论走 lark-drive 文档评论体系，读取 [`../lark-drive/SKILL.md`](../lark-drive/SKILL.md) 了解评论能力 | [`../lark-drive/SKILL.md`](../lark-drive/SKILL.md) |
| 管理 `app_...` 应用内角色、角色成员，或查询用户匹配角色 | `+role-list/get/create/update/delete`, `+role-member-list/add/remove`, `+role-match-list` | [`lark-apps-role.md`](references/lark-apps-role.md) |
| 云端 Agent 生成/迭代应用（开发方式已定为云端后） | `+session-create` -> `+chat` -> `+session-get` | [`lark-apps-cloud-dev.md`](references/lark-apps-cloud-dev.md) |
| 管理妙搭应用开放 API Key（创建/查看/启停/重置/删除凭证；密钥仅 create/reset 一次性返回） | `+openapi-key-list/get/create/update/enable/disable/delete/reset` | [`lark-apps-openapi-key.md`](references/lark-apps-openapi-key.md) |
| 管理妙搭应用自动化触发器（定时/记录变更/Webhook/飞书审批四类触发器的查询/创建/更新/启停；Webhook URL·Token 一次性回显、不落盘） | `+automation-list/get/create/update/enable/disable` | [`lark-apps-automation.md`](references/lark-apps-automation.md) |
| 查看某次会话某一轮（turn）的回复消息（含仍在生成中的本轮）/ 导出上一轮模型回复（"这一轮回复了什么""上一轮的回复""导出某轮消息"） | 先 `+session-get`（取 `latest_turn.turn_id`）-> `+session-messages-list --turn-id <id>`（仅 user 身份；分页用 `--page-token`） | [`lark-apps-session-messages-list.md`](references/lark-apps-session-messages-list.md) |
| 外部能力(AI模型能力和飞书平台能力)集成/插件/Plugin/Capability | `+plugin-install`, `+plugin-list`, `+plugin-uninstall` | [`lark-apps-plugin-install.md`](references/lark-apps-plugin-install.md), [`lark-apps-plugin-uninstall.md`](references/lark-apps-plugin-uninstall.md), [`lark-apps-plugin-list.md`](references/lark-apps-plugin-list.md) |
| 把一批 ID 在妙搭 user_id ↔ 飞书 open_id / union_id / 飞书 user_id 之间互转（例如拿到 open_id 但下游要 user_id） | `+user-id-convert --convert-type <方向> --ids <id1,id2,...>` | [`lark-apps-user-id-convert.md`](references/lark-apps-user-id-convert.md) |

## 高频路径

- **Base 到应用数据库同步**：用户说“Base 同步到数据库 / 整库同步 / 多张表同步 / 批量任务重新启用 / operation-not-allowed”时，先读 [`lark-apps-db.md`](references/lark-apps-db.md) 的 Base 数据同步段落，再查 app_id 或处理授权。先形成计划再动手：`+db-sync-create` 一次只处理一张 Base 表，整库/多表必须拆成多份单表配置和多次 preview/create；batch/import 任务是一次性任务，不能重新 enable，遇 operation-not-allowed 先解释生命周期边界，再用 `+db-sync-get` 查状态/结果，持续同步要新建 streaming 任务。
- **性能/监控/观测指标**：用户问“接口请求量、错误量、错误率、接口慢、延迟、CPU、内存、最近一小时/七天趋势”时，不要去当前工作区搜索监控文件，也不要询问“监控数据在哪”。先按「app_id 获取」解析应用：`lark-cli apps +list --keyword "<应用名>" --as user`；拿到 `app_id` 后读 [`lark-apps-observability.md`](references/lark-apps-observability.md)，用 `+metric-list`。
- **请求量 + 错误量 + 延迟**：请求量/错误量用 `lark-cli apps +metric-list --app-id <app_id> --metric requests --since <range> --as user`（不传 `--series` 会同时返回 total/error）；延迟用 `--metric latency`（不传 `--series` 会返回 p50/p99）。如果用户给了具体接口，再加 `--api <path-or-name>`；不要臆造 group-by 参数。
- **PV/UV/访问量/活跃用户**：先解析 `app_id`，再用 `+analytics-list`，不要误用 `+metric-list`。
- **设置环境变量**：如果用户只给应用名，仍先 `+list --keyword` 解析 app_id；设置 online 环境先核对当前请求/既有授权是否覆盖同一 app、环境、key、value/配置版本和影响。匹配时按 lark-shared 的 CLI hint 带 `--yes`，不因换轮、技能或认证重试重复询问；只对授权缺口请求补充授权。回复和日志摘要里只提 key / env / app，不回显真实 value；需要传复杂值时优先用 `@file` 或 stdin。
- **删除环境变量**：`+env-delete` 是破坏性操作。执行前核对用户授权是否覆盖该 app/env/key 及删除后果；已有匹配授权持续有效，不因认证重试或换轮失效。对象或影响不在授权范围内时，先展示并请求补充授权，再加 `--yes`。

## 应用协作者与协作权限设置

这组命令管理妙搭应用的开发协作者和协作策略，不等同于 `+access-scope-*` 的运行时访问范围，也不等同于 `+role-*` 的应用内业务角色。所有命令使用 `app_...` 应用 ID 和 `--as user`。不要读取或判断 `app_type` 来预判支持范围，直接调用对应的协作者命令。

- `+member-list`、`+member-settings-get` 是只读命令，需要 `spark:app:read`。
- `+member-add`、`+member-update`、`+member-remove`、`+member-settings-set` 是高风险写命令，需要 `spark:app:write`。先用 `--dry-run` 核对目标、URL 和请求体；dry-run 不需要 `--yes`。现有授权覆盖具体应用、成员/设置及影响时，按服务端要求加 `--yes`；授权不匹配时先展示差异并请求补充授权。批量移除成员仍需授权覆盖实际成员集合和后果，不能从泛化的“直接做”推导出 `--yes`。
- 添加、更新、移除成员时必须显式提供匹配的外部 ID 类型，禁止传内部数字 ID、猜测类型或做隐式转换：用户 `--member-type openid --member-id ou_...`；群组 `--member-type openchat --member-id oc_...`；部门 `--member-type opendepartmentid --member-id od-...`。
- `+member-list --member-type` 的筛选枚举是响应对象类型 `user` / `department` / `chat`，与写命令的 ID 类型枚举不同。可再用 `--role view|edit|full_access` 筛选。
- `+member-list` 一次返回应用的全部直接协作者，不提供分页参数；可用 `--member-type` 和 `--role` 缩小结果范围。
- 成员响应不包含应用详情。需要名称、类型或发布状态时单独调用 `+get --app-id <app_id>`，不要期待成员分页重复返回 `app`。
- 收到 subtype `feature_not_available`（OpenAPI code `3340005`；直连服务可能为 `40005`）时，立即停止 CLI 自动化，不切换 `app_type`，也不尝试用 access scope、应用角色或其它成员命令绕过。向用户说明该应用暂不支持通过 lark-cli 设置协作者，并引导其在妙搭后台的权限设置中操作。
- `external_invite` 只在 `+member-settings-get` 的响应中读取，不能独立设置；它会跟随 `external_access`。CLI 不注册 `--external-invite`，需要改变外部协作能力时只设置 `--external-access`。
- `copy_download_by` 也只在 `+member-settings-get` 的响应中读取。CCM 当前明确不支持为妙搭对象写入复制、打印和下载权限，因此 CLI 不注册 `--copy-download-by`。保留读取结果，不要尝试写入，也不要改用其它权限字段模拟。

```bash
# 读取协作者和当前协作策略
lark-cli apps +member-list --app-id <app_id> --as user
lark-cli apps +member-settings-get --app-id <app_id> --as user

# 写操作先预览精确的 typed-ID 字段；授权覆盖该动作后才把 --dry-run 换成 --yes
lark-cli apps +member-add --app-id <app_id> --member-type openid --member-id ou_xxx --perm view --dry-run --as user
lark-cli apps +member-update --app-id <app_id> --member-type openchat --member-id oc_xxx --perm edit --dry-run --as user
lark-cli apps +member-remove --app-id <app_id> --member-type opendepartmentid --member-id od-xxx --dry-run --as user
lark-cli apps +member-settings-set --app-id <app_id> --external-access disabled --comment-by viewer --dry-run --as user
```

## 选择开发路径（进意图路由前先判这步）

仅当用户明确选择妙搭、当前正在妙搭项目中，或任务必须使用妙搭资源时才进入本技能。新建妙搭应用前须确认当前请求覆盖妙搭平台及新应用创建；修改已有应用时先按「app_id 获取」指认目标，不擅自 `+create`。已有平台选择、应用项目和开发方式继续有效，不因换轮或加载技能而重问。仅当某个未定选项会实质改变目标、交付或风险，且无法从上下文和项目状态推断时，才询问该选项。

**app_type 三类边界**（先判"要不要把数据存到服务端"，再判"纯展示还是有交互"）：

| 信号 | 判定 |
|---|---|
| 含数据库 / 后端持久化：登录 / 增删改查 / 报名·投票·站会存记录 / 多人协作 / 泛称"系统·工具"且明确要存数据 | `app_type=full_stack` |
| 用户已选择妙搭且目标为纯静态展示（无 JS 交互）：PPT/deck / demo / 落地页 / 海报 / UI mockup / 线框图 / 静态仪表盘 / 视觉探索 | `app_type=html`，加载 [`creative-design/creative-design.md`](creative-design/creative-design.md)（实现步骤与需单独授权的发布流程） |
| 有 JS 交互但无数据库（给人"用"的前端应用）：可交互原型 / SPA / 表单校验 / 动态计算 / 调用外部 API / 泛称"工具·系统"但未明确要存数据 | `app_type=frontend`（**默认倾向**：用户未明确提出数据库需求时默认引导 frontend，不默认 full_stack） |
| 类型模糊（尤其"要不要存数据"不清） | 先检查现有需求、代码和项目资源；只有存储方式会实质改变方案且无法推断时，才询问这一点，其余采用合理默认并说明 |
| 用户要自己写 / 本地 IDE·code agent / 拉源码到本地 / 交研发 | 本地开发，读 [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md) |
| 让妙搭 AI 云端生成 / 对话式 / 自己不碰代码 | 云端会话，读 [`lark-apps-cloud-dev.md`](references/lark-apps-cloud-dev.md) |
| 未表达"谁来写"偏好 | 先看当前应用、仓库与已选平台；沿用已有开发路径。只有本地与云端选择会显著改变结果且无法从上下文推断时，才问一次 |
| 修改已有 + 当前目录是 `.spark/meta.json` 项目 | 直接沿用本地路径，不重复询问平台或开发方式 |
| 修改已有 + 用户已选择云端 | 沿用云端会话；已有选择在认证重试和技能切换后仍有效 |
| 修改已有 + 没有项目或开发方式线索 | 使用适合当前项目的合理默认；只有会实质影响交付时才提问 |

**类型升级**：`frontend` 应用后续需要数据库/后端能力时，本地 CLI 不提供类型升级；引导用户到云端会话（打开 `https://miaoda.feishu.cn/app/{app_id}`），用自然语言描述后端需求（如"给这个应用加登录和数据存储"）即可触发升级，无需特殊指令。

## 发布态护栏

- **发布授权**：只有用户明确要求发布、部署、上线或生成线上分享链接，或已有明确授权的范围覆盖这次发布，才进入发布链路。用户说"直接做"、"做好"或只要求实现时，只授权完成实现，不自动 commit、push 或发布。发布授权持续覆盖同一应用、内容版本和目标环境；内容、应用或环境变化时只核对变化部分。
- `+release-create` 的发布理由按应用类型处理：创意模式 `html` 不需要发布理由，命令不得传 `--apply-reason`；`frontend` / `full_stack` 先加载 [`lark-apps-release-create.md`](references/lark-apps-release-create.md)，生成理由并确认它仍落在用户的发布授权范围内；理由或影响超出已授权范围时，只请求新增授权。
- `+release-get` 尚未返回 `finished` / `failed`，且返回 `current_node_info.current_status=PENDING` 时（顶层可能是 `publishing` 或 `pending`）立即加载 [`lark-apps-release-get.md`](references/lark-apps-release-get.md)，停止轮询并告知当前用户正在等待审批负责人处理；不得假定当前用户或 `submitted_by` 是审批人。终态优先于可能残留的 PENDING 节点。
- `+release-create` 或 `+release-get` 仅当服务端错误明确说明客户端版本过旧或要求升级时，才建议执行 `lark-cli update` 后重试原命令（查询仍使用同一个 `release_id`）。不要硬编码或猜测最低版本，不要用 `--help` 做能力预检；`X-Cli-Version` 由 CLI 请求统一携带且不是认证信息，本工作流不增加 CLI 版本门禁。
- 完成 ≠ 发布：云端会话完成 / `+list is_published=true` 都不代表最新内容已部署。
- 开发态链接 `https://miaoda.feishu.cn/app/{app_id}`（full_stack / frontend 应用）：进应用编辑/开发态、管理与继续开发应用的入口，也是 frontend 升级为 full_stack 的入口（云端会话）。创意模式（html）应用开发态和发布态是同一个链接，无需额外提供开发态链接。
- 发布态链接来源：`+release-get` 轮询 `finished` 给 `online_url` / `failed` 给 `error_logs`（html / frontend / full_stack 统一走 `+release-get`）。
- html 应用的主链路是创意模式开发方式：按 [`lark-apps-local-dev.md`](references/lark-apps-local-dev.md) 在用户已选择的妙搭应用内初始化仓库并产出 HTML 及关联文件。提交、推送和发布是可选的独立动作；只有用户明确要求或既有授权覆盖相同应用、内容版本和环境时才执行。任何已授权的 git 操作（clone / pull / push）报错时，先执行 `lark-cli apps +git-credential-init --app-id <app_id> --as user` 刷新本地 Git 凭证，再重试原 git 命令。
- 创意模式（html）应用的链接格式为 `https://{租户域名}/page/{meta_token}`，**开发态和发布态是同一个链接**（区别于 full_stack 应用两者分开）。此链接形似飞书文档链接。`+get --app-id <meta_token>` 可获取应用信息（含 `app_id`），`+get --app-id <app_id>` 可获取 `meta_token`。看到 `/page/xxx` 链接时，它是妙搭创意模式应用，不要当成飞书文档跳过。

## 平台资源与应用源码边界

- `apps` 命令的 `--path`、`--file`、`--output` 等路径参数只接受当前工作目录（cwd）下的相对路径，传绝对路径会报错。如果目标文件不在 cwd 下，先 `cd` 到目标目录再执行命令。
- 图片、字体、音视频等资源型文件属于平台资源，不应提交到 git 仓库、引用本地路径或以 base64 内联到源码中。先通过 `lark-cli apps +file-upload --app-id <app_id> --file <local_path>` 上传到应用文件存储，拿到返回的远端 URL 后在代码中引用。上传返回的链接按 app 隔离，不同应用必须各自重新上传，不能跨应用复用同一链接。详情读 [`lark-apps-file.md`](references/lark-apps-file.md)。
- `apps +role-*` 只管理平台角色资源；修改已初始化应用的源码（包括当前目录已经是应用项目）时，先查看工作区 `.agents/skills/`，完整读取与任务匹配的领域 skill，再按其路由读取所需 reference。角色鉴权或运行态角色管理读应用内 `authz-guide`，不能用本 skill 的平台命令参考推断运行时合同。
- `lark-cli` 只用于开发过程中的平台资源核验或变更。应用运行时代码必须使用工程内领域 skill 规定的 SDK，禁止通过 `exec` 或子进程调用 `lark-cli`。
- 平台回读出的当前资源 ID、名称和成员只用于事实核验，不自动构成业务策略；除非需求或应用内领域 skill 明确定义，禁止把当前样本硬编码成 allowlist、denylist、只读集合或权限规则。
- 实现领域 SDK 时，以实际包导出的类型和应用内领域 reference 记录的入参、响应路径为准；禁止修改 ambient `.d.ts`、补造宽松类型或强制断言，让猜测的 SDK 结构仅在本地"编译通过"。
- typecheck/build 成功不等于合同正确。交付前逐项核对每个 SDK 调用的入参、响应取值路径和策略分支；涉及更新、删除等不同动作时，分别验证各自动作所需的完整状态，不能复用更弱的前置判断。
- 源码任务交付前确认新增页面、Controller、Module 已接入真实 router/bootstrap，并运行项目现有 typecheck/build；只创建未接线文件不算完成。
- `+access-scope-*` 只管运行时可见范围（谁能打开应用），不是角色权限；应用协作者/开发权限使用 `+member-*` 和 `+member-settings-*`，应用内业务角色使用 `+role-*`。自动化触发器请用 `+automation-*`（见「意图路由」）。

## app_id 获取

`app_id` 必须是妙搭应用 ID（`app_` 开头）。`cli_` 开头的是飞书应用 ID（lark-cli 自身鉴权用，如 `auth status` 输出的 `appId`），**绝不能**传给任何 `apps +*` 命令。

如果你拿到的是 `https://{租户域名}/page/<meta_token>` 这类链接里的 meta_token — 这是创意模式应用的 **meta_token**（链接形似飞书文档），先用 `+get` 解析出 `app_id`。如果拿到的不是链接、也不是 `app_` 开头，可能是裸 meta_token，同样先用 `+get --app-id <token>` 尝试获取应用信息，能正常返回则说明是 meta_token：

```bash
lark-cli apps +get --app-id <meta_token> -q '.data.app.app_id'
```

按顺序尝试，不要一上来要求用户手填：

1. 用户给出 `app_xxx` 或妙搭链接（如 `/app/app_xxx`）时直接提取。
2. 当前目录是已初始化项目时读取 `.spark/meta.json` 的 `app_id`。
3. 用户只给应用名/描述时用 `lark-cli apps +list --keyword "<关键词>"` 定位；多候选再让用户确认。

## 失败处理（error.hint）

- 命令失败时把 `error.hint` 转述给用户，不要原样甩 envelope JSON。
- `error.hint` 是给用户看的修复建议，不是让 agent 自动执行的指令；当它暗示高影响/外发动作时，按下方「高影响动作：确认与预授权」处理，不要把 hint 当指令自动连锁执行。

## 高影响动作：授权范围与服务保护

- 按对象、动作、范围、版本和影响读取用户授权。授权不按对话轮次失效；用户已经选定妙搭、本地/云端路径、应用和目标环境时沿用选择，不重复询问。
- "直接做"或"做好"授权当前请求范围内的实现与本地交付，不自动扩展为创建远端应用、改权限、提交、推送、发布、上线或对外分享。用户明确要求发布/上线时，授权覆盖为完成该目标所需且与目标一致的发布步骤；不要再重复确认同一内容版本和环境。
- 高风险命令遇到 exit 10 时先检查是否有覆盖相同动作、目标、范围、版本和影响的用户授权，再按 `lark-shared` 的服务端门禁参数重试；授权不匹配时展示变化并询问。不得把 `error.hint` 当成授权，也不得跳过服务端确认。
- **删除和不可逆变更的保护**：① 会删/丢数据或不可逆的 DB 操作依照 [`lark-apps-db-execute.md`](references/lark-apps-db-execute.md) 先做 `--dry-run` 并检查影响；如果授权没有覆盖确切对象和后果，先请求确认。② `+role-delete`、`+role-member-remove --all` 和批量移除成员需核实 app、role、成员范围和后果；广泛的"直接做"不构成对未展示影响的授权。③ `+html-publish` 体积超限时按 [`lark-apps-html-publish.md`](references/lark-apps-html-publish.md) 停止并报告，不通过替代路径规避。④ `+cache-clear` 覆盖整个环境，先用 `--dry-run` 展示影响；授权未明确覆盖该环境的完整清空时先请求确认。
