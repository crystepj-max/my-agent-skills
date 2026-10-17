# lark-apps 本地开发

适用：用户明确选择妙搭应用，并要把应用源码（full_stack、frontend 或 html）拉到本地，用本地 code agent/IDE 开发。其中调试数据库仅 full_stack 适用（frontend / html 无数据库）。本地实现、提交/推送和发布是不同动作；仅在用户明确要求相应动作或既有授权覆盖其范围时分别执行。

## 新建 vs 已有应用

新建还是修改已有，由上方入口（SKILL.md「选择开发路径」）判定；仅在当前请求覆盖妙搭应用和相应创建/初始化动作时进入本地流程。提交、推送和发布授权分开核对，用户只要求实现时保留本地交付并停止。

- **新建**：从 `+create` 开始走下面的端到端流程。
- **已有应用**（本地还没有源码）：跳过 `+create`，先按下方「存量应用入口」拿 `app_id`，再 `+init`（或 `+git-credential-init` + `git clone`）把它拉到本地，然后照常开发。

## 本地开发与可选发布流程（新建应用）

下列示例展示本地开发和平台部署的完整技术链。用户只要求创建、初始化和实现时，执行已授权的创建/初始化与实现部分；默认在本地保存、检查并交付。示例中的 commit、push、release 仅在用户明确要求相应动作或既有授权覆盖相同项目、内容版本和目标环境后执行。若 +init 的实际计划包含超出初始化授权的外部提交/推送影响，先使用已支持的本地准备路径，或只请求该新增影响的授权。

### full_stack

`+create(full_stack)`（仅创建授权覆盖新建应用时）-> `+init`（仅初始化授权覆盖准备本地仓库时；或手动 `+git-credential-init` + `git clone`）-> 读仓库 Skill -> `npm install && npm run dev` -> 按需 `+db-*` 调库。commit、push、release 需分别受当前请求/既有授权覆盖；用户只要求实现时，保存并检查本地实现后交付，不自动提交、推送或发布。包含自动化 handler 时，若用户明确授权发布，再转到 [automation SOP](lark-apps-automation.md)，由它接管状态门禁和发布流程。

```bash
# 新建 full_stack 应用
lark-cli apps +create --as user --name "审批系统" --app-type full_stack \
  --description "支持登录、提交申请、多级审批、状态查询"

# 初始化本地仓库（--dir 取值见下方「领域规则」，勿照抄此处示例值）
lark-cli apps +init --as user --app-id app_xxx --dir ./approval-app

# 进入仓库后按项目脚手架启动
cd ./approval-app
npm install
npm run dev

# 本地开发完成默认保存并检查；仅在用户明确授权 commit、push 和 release 后，才运行下方可选部署命令。
# +release-create 部署的是远端 sprint/default 上已 push 的代码，不是本地工作区——没 commit + push 的改动不会进入发布。
  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
git add <本次开发的文件>          # 提交粒度见下方「改完代码后部署上线」
git commit -m "feat: ..."
  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
git push origin sprint/default
  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
lark-cli apps +release-create --as user --app-id app_xxx --branch sprint/default --apply-reason "发布审批系统功能更新"
```

### frontend

纯前端应用（vite-react，无数据库）。本地流程包含 `+init`、`npm run dev`；commit/push/release 仅在用户明确授权这些动作时执行，差别是无 `+db-*` 调库步骤。后续需要数据库/后端能力时不在本地升级，按 SKILL.md「类型升级」引导到云端会话。

```bash
# 新建 frontend 应用
lark-cli apps +create --as user --name "JSON 格式化工具" --app-type frontend \
  --description "纯前端交互工具，无需数据库"

# 初始化本地仓库（--dir 取值见下方「领域规则」，勿照抄此处示例值）
lark-cli apps +init --as user --app-id app_xxx --dir ./json-tool

# 进入仓库后按项目脚手架启动（vite-react）
cd ./json-tool
npm install
npm run dev

# 默认只完成本地实现；仅在用户明确授权 commit、push 和 release 后，才运行下方可选部署命令。
  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
git add <本次开发的文件>
git commit -m "feat: ..."
  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
git push origin sprint/default
  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
lark-cli apps +release-create --as user --app-id app_xxx --branch sprint/default --apply-reason "发布 JSON 格式化功能更新"
# 发布是异步的：用 +release-get 轮询到 status=finished 才算部署完成、拿到 online_url
lark-cli apps +release-get --as user --app-id app_xxx --release-id <上一步返回的 release_id>
```

### html

#### 首次开发（无 app，无代码）

`+create(html)`（仅创建授权覆盖时）→ `+init` 或等价本地准备路径（授权覆盖初始化及其实际影响时）→ 加载 [creative-design](../creative-design/creative-design.md) skill 在 repo 根目录产出文件。本地实现完成后默认停止并交付；只有用户明确授权发布时，再单独运行 git commit、git push、`+release-create` 和 `+release-get`。

```bash
lark-cli apps +create --name "活动页" --app-type html --as user

lark-cli apps +init --app-id app_xxx --dir ./my-page

cd ./my-page
# html 类型无需 npm install，+init 已跳过依赖安装
# 加载 creative-design skill，在 repo 根目录产出 HTML 及关联文件（JSX 组件、starter components 等）

  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
git add .
git commit -m "feat: ..."
  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
git push origin sprint/default
# 创意模式 html 不需要发布理由
  # 仅在用户明确要求且授权覆盖该提交/推送/发布动作、目标和内容版本时执行；实现本身不授权此步骤。
lark-cli apps +release-create --app-id app_xxx
```

#### 已有 app，二次开发/迭代

`+init`（拉取远程代码；核对其实际计划包含的同步、commit/push、环境变量影响）或等价本地准备路径 → 加载 creative-design skill 在 repo 根目录迭代。用户只要求实现时，本地保存、检查并交付；commit/push/release 只有在用户明确授权该动作及项目/版本/环境范围后才执行。

#### creative-design 已提前生成文件，需要 init 后迁入

`+create(html)`（仅创建授权覆盖时）→ `+init` 或等价本地准备路径 → 先 `ls` 查看 repo 根目录模板结构（创意模式模板无 `src/` 目录，文件直接放根目录）→ 将已生成的产出文件（HTML、JSX 组件、starter components 等）拷贝到 repo 根目录。默认只交付本地实现；只有授权覆盖同一应用、选定内容版本和目标环境时，才继续执行 git commit、git push、`+release-create` 与 `+release-get`。

`+init` 是推荐便捷入口；想逐步手动控制时，先 `+git-credential-init` 拿 `repository_url`，再用原生 `git clone` / `git checkout sprint/default`。

**`+init` 完成后必须执行**：`cat <project-path>/.agents/skills/plugin-guide/SKILL.md`，读取仓库插件指引。该文件包含插件目录、实例配置规则和调用代码生成方式——不读就无法正确集成插件能力。文件不存在则跳过。

## Trigger guide 的项目边界

涉及自动化业务代码时，先查看工作区 `.agents/skills/`，读取与自动化任务匹配的 `trigger-guide`。它定义业务 handler 的实现与接入约束；Apps 触发器配置细节见 [automation SOP](lark-apps-automation.md)。

文件缺失或不能覆盖当前任务时，报告项目缺少可用的领域 guide；不要在本 lark-cli reference 中猜测安装命令、版本或包内目录。由项目维护方通过其受支持的初始化或同步流程补齐后，再继续代码闭环；`+init` 只负责准备本地项目，不能替代领域 guide。

## 改完代码后部署上线

用户明确要求推送时才执行推送；只有另行明确要求部署/上线/发布时才执行 release。先分别核对每个动作对应的授权对象、目标、版本和影响，再执行覆盖范围内的步骤；不得由“推上去”推导出发布。

若本次改动包含自动化 handler，在执行本节通用 commit/push/release 序列前就转到 [automation SOP](lark-apps-automation.md) 的匹配路径，由该 SOP 负责完整的状态门禁、commit/push、release 和可选 enable/test；不要先按本节发布再补 trigger 状态检查。下列通用序列只用于不含自动化 handler 的改动。

> `+release-create` 部署的是远端 `sprint/default` 上**已 push** 的代码，不是你本地工作区——未 commit / 未 push 的改动不会进入这次发布。所以发布前务必先把本次改动提交并推送。

1. 仅在提交动作已获授权后，`git status` 查看本次改动；`git add <本次相关文件>` 暂存并提交。只提交本次任务相关的改动。
2. 仅在推送动作已获授权后，`git push origin sprint/default` 把工作分支推到云端（遇非 fast-forward：先 `git pull --rebase origin sprint/default` 解决冲突再推，绝不 force-push；遇 Git 认证失败 / 401 / 403 / credential helper 缺失 / token 过期：先执行 `lark-cli apps +git-credential-init --app-id <app_id> --as user` 刷新本地 Git 凭证，再重试原 git 命令；刷新凭证也失败时，停止并向用户报告错误，不要换路）。
3. 仅在发布授权覆盖同一应用、内容版本和目标环境时，按应用类型发起部署并记下返回的 `release_id`：创意模式 `html` 执行 `lark-cli apps +release-create --as user --app-id <app_id> --branch sprint/default`，不传发布理由；`frontend` / `full_stack` 先读取 [`lark-apps-release-create.md`](lark-apps-release-create.md)，根据已授权的发布范围生成理由；仅当理由或影响超出该范围时，才请求补充授权，然后执行 `lark-cli apps +release-create --as user --app-id <app_id> --branch sprint/default --apply-reason "发布本轮已提交并推送的功能更新"`。示例文本须替换为刚确认的实际理由且保持逐字相同。
4. `lark-cli apps +release-get --as user --app-id <app_id> --release-id <release_id>` 先按顶层 status 识别终态：`finished` / `failed` 优先于可能残留的 PENDING 节点。尚未进入终态且 `current_node_info.current_status=PENDING` 时（顶层可能是 `publishing` 或 `pending`）立即停止本轮轮询，保留同一个 `release_id`，并按 [`lark-apps-release-get.md`](lark-apps-release-get.md) 告知当前用户正在等待审批负责人处理；不得假定当前用户或 `submitted_by` 是审批人。当前用户明确确认审批负责人已处理后继续查询该 ID。在此之前不得自动审批或写回发布节点，也不得新建另一轮 release。非 PENDING 的 `publishing` 时每 20 秒继续轮询，整体最多约 5 分钟；超时仍未完成时停止本轮轮询、报告 `release_id` 和当前 status。`status=pending` 但没有明确 PENDING 节点时停止自动轮询并原样报告，不要补出审批人、审批链接或新建 release。`finished` 成功时，若返回 `online_url`，可直接使用；未返回时不要编造链接。`pending` 响应里即使提前出现 `online_url` 也不能视为本轮部署完成。交付线上访问链接给他人前，注意 `online_url` 默认仅创建者可见，需先告知当前仅本人可见、按需用 `+access-scope-set` 放开可见范围。无需再调 `+list`；`failed` 时若返回非空 `error_logs`，据此给出失败原因；否则只报告 `release_id` 和当前 status，不要编造原因。其他未知 status 立即停止自动轮询并原样报告，不要自行判定结果或创建新 release（`+list` 仅作独立查询入口）。

用户只要求启用已有 trigger 时，转到 [automation SOP 的「仅启用已有 disabled trigger」路径](lark-apps-automation.md#仅启用已有-disabled-trigger)；不得因 enable 反向修改 handler、commit/push 或 release。

## 领域规则

- 代码读写走原生 `git`；CLI 负责凭证、初始化、发布和数据库调试。不存在 `apps +pull` / `apps +push` / `apps code +read` 这类代码读写 shortcut，不要臆造。
- 工作环境没有 `git` 时，先引导安装 Git（macOS 可用 `xcode-select --install` 或 `brew install git`；Linux 按发行版包管理器安装），安装后重试原 `+init` / git 命令；不要因此改走其他发布链路。
- `+init` 会编排 `+git-credential-init`、`git clone`、切到 `sprint/default`、运行脚手架；输出可含 `committed` / `pushed`。执行前先看当前 `lark-cli apps +init --help` 和 dry-run 计划，明确核对这些效果。用户的 +init 授权覆盖命令公开的初始化副作用；若其实际外部提交/推送超出用户请求范围，就用 `+git-credential-init` + 原生 git clone 等价准备方式，或只请求该缺口授权。后续 `+release-create` 仍是独立发布动作，不能由 +init 授权推导。
- `+init --dir` 选目录：用户已预授权或表达"不要询问"（见 SKILL.md「预授权判定」）→ 按应用名派生 `./<app-name>` 直接传 `--dir`、不停问；否则先问用户用哪个目录再传。目标已存在/非空时回问换目录。
- `sprint/default` 是工作分支；`main` 是发布态快照，由 `+release-create` 成功后服务端 fast-forward 推进；服务端护栏禁直推 `main`、拒 force-push、要求 `sprint/default` fast-forward。
- 已拉到本地后，pull/push/diff/log 都用原生 git；云端 `sprint/default` 比本地新时，先 `git pull --rebase origin sprint/default`，解决冲突后再 push 和 publish。
- `git clone` / `git pull` / `git push` 如果报认证失败、401/403、credential helper 缺失或 token 过期，优先重新执行 `lark-cli apps +git-credential-init --app-id <app_id> --as user` 更新本地 Git 凭证，然后重试原 git 命令；刷新凭证也失败时，停止并向用户报告错误，不要换路；不要手动复制 token、不要把 token 拼进 remote URL。
- 环境变量由脚手架在本地启动时处理；需要手动刷新时用 `+env-pull`。
- 资源型文件（图片、字体、音视频等）不要直接引用本地路径，也不要提交到 git 仓库或以 base64 内联到代码中。先通过 `lark-cli apps +file-upload --app-id <app_id> --file <local_path>` 上传到应用文件存储，拿到返回的远端 URL 后在代码中引用该 URL。详情读 [`lark-apps-file.md`](lark-apps-file.md)。上传返回的链接按 app 隔离，不同应用必须各自重新上传，不能跨应用复用同一链接。
- DB 调试用 `+db-table-list` / `+db-table-get` / `+db-execute`；不要裸连数据库或自行拼连接串。
- DB 分 `dev` / `online`；使用 `--environment dev|online`，不要使用旧的 `--env`。只有确认应用已开启多环境时才引导 `--environment dev`；单环境应用省略 `--environment`（服务端选 online）或显式传 `--environment online`。在 dev 写入不能证明线上 handler 已验证。dev 的库结构变更要上线时，仍按应用发布链路走 `+release-create`，不要另造“数据库发布”步骤。
- 存量单库应用需要 dev/online 多环境时，用 `+db-env-create --environment dev`。这是不可逆 high-risk 操作。
- 只从 `+list` 看到 `is_published=true`，不能证明本地刚推送的代码已经部署；必须有本轮 `+release-get finished`。

## 存量应用入口

已有项目目录先读 `.spark/meta.json` 取 `app_id`；没有本地项目但知道应用名时用：

```bash
lark-cli apps +list --keyword "应用名"
```

拿到 `app_id` 后再 `+init` 或 `+git-credential-init`。

## 何时不用

- 用户明确要云端妙搭 Agent 生成/迭代，而不是本地写代码：读 [`lark-apps-cloud-dev.md`](lark-apps-cloud-dev.md)。
