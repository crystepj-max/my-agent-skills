# 技能生命周期

本表是正式登记 `inventory/skill-policy.json` 的人读状态版本，共 142 条记录。状态和范围决定实际入口；描述与来源历史见 [skill-desc-translation.md](skill-desc-translation.md)。本地 `apply`、`check` 和实际入口路径独立核验最近一轮均通过；29 项 updater 清退已完成，102 条 `reference_copies` 在同一正式 bundle 的两个恢复入口验证中均通过。新会话可见性与业务行为仍须分别验证。

全表当前结构：`first-party` 127 条（active 124、retired 3）；`third-party` 15 条（transition 1、reference 12、retired 2）。范围为 `global` 134、`presentations` 7、`gawain` 1。2026-10-15 新增 first-party active：`chatgpt-web-bridge`（通用 ChatGPT 网页桥接，派生自同表 transition 状态的 `codex-bridge-chatgpt`）。此前一轮的 99 条映射是当时 141 条中的 active first-party 子集（98 个 `global` 用户级源 + 1 个 `gawain` 项目源），不是全仓第一方总量。`reference_copies` 共 102 条：该轮新增 99 条映射，加上原有 `tdd`、`diagnosing-bugs`、`neat-freak` 三份参考。第一方登记源只说明当前维护责任，不代表最初作者或原创来源。

| 技能 | 状态 | 范围 | 正式来源 |
|---|---|---|---|
| agent-cli-tool-residue-purge | active | global | `my-skills/agent-cli-tool-residue-purge` |
| agent-skill-bridge | active | global | `my-skills/agent-skill-bridge` |
| agnes-ai-generation-skill | active | global | `my-skills/agnes-ai-generation-skill` |
| ask-matt | active | global | `my-skills/ask-matt` |
| baoyu-comic | active | global | `my-skills/baoyu-comic` |
| baoyu-image-gen | active | global | `my-skills/baoyu-image-gen` |
| baoyu-infographic | active | global | `my-skills/baoyu-infographic` |
| baoyu-slide-deck | reference | presentations | `project:presentations/.agent-assets/presentations/baoyu-slide-deck` |
| beautiful-html-templates | reference | presentations | `project:presentations/.agent-assets/presentations/beautiful-html-templates` |
| bottleneck-hunter | active | global | `my-skills/bottleneck-hunter` |
| chatgpt-web-bridge | active | global | `my-skills/chatgpt-web-bridge`（说明：通用 ChatGPT 网页桥接；通道优先级 codex-in-app-browser → user-chrome（用户已登录 Chrome 会话）→ host-browser-use；reasoning 与 image 两类任务合同；启用前需通过 automation-consent 同意门；自动传输属非官方实验特性，有账号风险，禁止无头/反检测执行。） |
| clashx-openai-sse-debug | active | global | `my-skills/clashx-openai-sse-debug` |
| cnb-git | active | global | `my-skills/cnb-git`（说明：按实际 upstream remote 与服务端分支执行 fetch/pull；凭据仅注入 CNB URL；不自动删 Git lock，clone/fetch/pull 错误明确失败。） |
| cnb-push | active | global | `my-skills/cnb-push`（说明：CNB 推送封装；区分现有仓更新与首次上传，--all/--set-default 按其实际影响范围授权并复用既有授权。） |
| code-review | active | global | `my-skills/code-review` |
| codebase-design | active | global | `my-skills/codebase-design` |
| codex-bridge-chatgpt | transition | global | `~/.agents/skills/codex-bridge-chatgpt`（说明：2026-10-14 曾在 16:55 退役（判定无实用价值），当日 22:21 用户要求装回并恢复治理。来源不可考：无 git / README / LICENSE，全文无 URL 或作者声明，安装时间戳同为一秒。启用需先取得浏览器自动化授权（automation-consent状态为 missing_state，未授权时不会操作 ChatGPT）。功能与 codex-with-chatgpt 重叠：旧的靠人工粘贴 1–3K 上下文包，新靠 MCP 只读连接器。；宿主限制：Codex 专属：依赖 Codex 内置浏览器能力（browser:control-in-app-browser）与 ChatGPT 桌面应用，其他宿主无对应能力，桥接即为坏副本） |
| construction-bootstrap | retired | global | `~/.local/share/agent-skills/retired/construction-bootstrap` |
| cross-domain-borrowing | active | global | `my-skills/cross-domain-borrowing` |
| deep-company-series | active | global | `my-skills/deep-company-series` |
| dev-workflow-2-0 | retired | global | `~/.local/share/agent-skills/retired/dev-workflow-2-0`（调用范围：explicit-legacy-only） |
| diagnosing-bugs | reference | global | `~/.local/share/agent-skills/references/diagnosing-bugs` |
| domain-modeling | active | global | `my-skills/domain-modeling` |
| dsh-source-upgrade | active | global | `my-skills/dsh-source-upgrade`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/dsh-source-upgrade） |
| dsh-web-access-recovery | active | global | `my-skills/dsh-web-access-recovery`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/dsh-web-access-recovery） |
| duplicate-cli-unify | active | global | `my-skills/duplicate-cli-unify` |
| dyp-ask | active | global | `my-skills/dyp-ask` |
| earnings-review | active | global | `my-skills/earnings-review` |
| earnings-team | active | global | `my-skills/earnings-team` |
| edit-article | active | global | `my-skills/edit-article` |
| eli5 | active | global | `my-skills/eli5` |
| execution-plan | retired | global | `~/.local/share/agent-skills/retired/execution-plan`（历史副本保留；正式入口为 dev-flow 项目级技能） |
| expert-consultation | active | global | `my-skills/expert-consultation` |
| fact-check | active | global | `my-skills/fact-check` |
| financial-data | active | global | `my-skills/financial-data` |
| find-skills | reference | global | `~/.local/share/agent-skills/reference/find-skills` |
| first-principle | active | global | `my-skills/first-principle` |
| frontend-design | active | global | `my-skills/frontend-design` |
| frontend-slides | reference | presentations | `project:presentations/.agent-assets/presentations/frontend-slides` |
| git-guardrails-claude-code | active | global | `my-skills/git-guardrails-claude-code` |
| grill-me | active | global | `my-skills/grill-me` |
| grill-with-docs | active | global | `my-skills/grill-with-docs` |
| grilling | active | global | `my-skills/grilling` |
| guizang-ppt-skill | reference | presentations | `project:presentations/.agent-assets/presentations/guizang-ppt-skill` |
| handoff | active | global | `my-skills/handoff` |
| hatch-pet | active | global | `my-skills/hatch-pet` |
| humanize-ppt | reference | presentations | `project:presentations/.agent-assets/presentations/humanize-ppt` |
| implement | reference | global | `~/.local/share/agent-skills/reference/implement` |
| implement-spec | active | global | `my-skills/implement-spec` |
| improve-codebase-architecture | active | global | `my-skills/improve-codebase-architecture` |
| income-investment | active | global | `my-skills/income-investment` |
| industry-funnel | active | global | `my-skills/industry-funnel` |
| industry-research | active | global | `my-skills/industry-research` |
| investment-checklist | active | global | `my-skills/investment-checklist` |
| investment-memo-craft | active | global | `my-skills/investment-memo-craft` |
| investment-research | active | global | `my-skills/investment-research` |
| investment-team | active | global | `my-skills/investment-team` |
| lark-approval | active | global | `my-skills/lark-approval` |
| lark-apps | active | global | `my-skills/lark-apps` |
| lark-attendance | active | global | `my-skills/lark-attendance` |
| lark-base | active | global | `my-skills/lark-base` |
| lark-calendar | active | global | `my-skills/lark-calendar` |
| lark-contact | active | global | `my-skills/lark-contact` |
| lark-doc | active | global | `my-skills/lark-doc` |
| lark-drive | active | global | `my-skills/lark-drive` |
| lark-event | active | global | `my-skills/lark-event` |
| lark-im | active | global | `my-skills/lark-im` |
| lark-mail | active | global | `my-skills/lark-mail` |
| lark-markdown | active | global | `my-skills/lark-markdown` |
| lark-meeting | active | global | `my-skills/lark-meeting` |
| lark-minutes | active | global | `my-skills/lark-minutes` |
| lark-note | active | global | `my-skills/lark-note` |
| lark-okr | active | global | `my-skills/lark-okr` |
| lark-openapi-explorer | active | global | `my-skills/lark-openapi-explorer` |
| lark-shared | active | global | `my-skills/lark-shared` |
| lark-sheets | active | global | `my-skills/lark-sheets` |
| lark-skill-maker | active | global | `my-skills/lark-skill-maker` |
| lark-slides | active | global | `my-skills/lark-slides` |
| lark-task | active | global | `my-skills/lark-task` |
| lark-vc | active | global | `my-skills/lark-vc` |
| lark-vc-agent | active | global | `my-skills/lark-vc-agent` |
| lark-whiteboard | active | global | `my-skills/lark-whiteboard` |
| lark-wiki | active | global | `my-skills/lark-wiki` |
| lark-workflow-meeting-summary | active | global | `my-skills/lark-workflow-meeting-summary` |
| lark-workflow-standup-report | active | global | `my-skills/lark-workflow-standup-report` |
| learn_something_new | active | global | `my-skills/learn_something_new` |
| life-design | active | global | `my-skills/life-design` |
| llm-wiki-app | active | global | `my-skills/llm-wiki-app` |
| management-deep-dive | active | global | `my-skills/management-deep-dive` |
| migrate-to-shoehorn | active | global | `my-skills/migrate-to-shoehorn` |
| minimum-scale-experiment | active | global | `my-skills/minimum-scale-experiment` |
| neat-freak | active | global | `my-skills/neat-freak` |
| news-pulse | active | global | `my-skills/news-pulse` |
| obsidian-vault | active | global | `my-skills/obsidian-vault` |
| portfolio-review | active | global | `my-skills/portfolio-review` |
| ppt-master | reference | presentations | `project:presentations/.agent-assets/presentations/ppt-master` |
| pr | active | global | `my-skills/pr` |
| presentation-production | active | presentations | `my-skills/presentation-production` |
| private-company-research | active | global | `my-skills/private-company-research` |
| prototype | active | global | `my-skills/prototype` |
| quality-screen | active | global | `my-skills/quality-screen` |
| remotion-best-practices | active | global | `my-skills/remotion-best-practices` |
| remotion-video-production | active | global | `my-skills/remotion-video-production` |
| remotion-video-toolkit | active | global | `my-skills/remotion-video-toolkit` |
| requirements-analysis.bak-20260905-224705 | retired | global | `~/.local/share/agent-skills/retired/requirements-analysis.bak-20260905-224705` |
| research | active | global | `my-skills/research`（宿主限制：Hermes 的 research 是包含多个内置技能的分类目录，不可替换为公共技能） |
| resolving-merge-conflicts | retired | global | `~/.local/share/agent-skills/retired/resolving-merge-conflicts`（退役日期：2026-10-06；退役原因：上游 mattpocock/skills v1.3.0 已移除该 skill（无替代，agent 自行处理合并/rebase 冲突）） |
| retro | active | global | `my-skills/retro` |
| scaffold-exercises | active | global | `my-skills/scaffold-exercises` |
| setup-matt-pocock-skills | active | global | `my-skills/setup-matt-pocock-skills` |
| setup-pre-commit | active | global | `my-skills/setup-pre-commit` |
| skill-creator | reference | global | `~/.local/share/agent-skills/references/skill-creator`（替代：skill-workbench） |
| skill-workbench | active | global | `my-skills/skill-workbench` |
| skills-security-check | active | global | `my-skills/skills-security-check` |
| socratic-clarify | active | global | `my-skills/socratic-clarify` |
| steelmanning | active | global | `my-skills/steelmanning` |
| storage-analyzer | active | global | `my-skills/storage-analyzer` |
| sts2-gawain-regression-recovery | active | gawain | `project:gawain/skills/sts2-gawain-regression-recovery` |
| sts2-independent-run-regression | active | global | `my-skills/sts2-independent-run-regression` |
| sts2-start-game | active | global | `my-skills/sts2-start-game` |
| tdd | active | global | `my-skills/tdd` |
| teach | active | global | `my-skills/teach` |
| test-report-html | active | global | `my-skills/test-report-html` |
| thesis-drift | active | global | `my-skills/thesis-drift` |
| thesis-tracker | active | global | `my-skills/thesis-tracker` |
| to-questionnaire | active | global | `my-skills/to-questionnaire` |
| to-spec | reference | global | `~/.local/share/agent-skills/reference/to-spec` |
| to-tickets | reference | global | `~/.local/share/agent-skills/reference/to-tickets` |
| triage | active | global | `my-skills/triage` |
| typesafe-ai | active | global | `my-skills/typesafe-ai` |
| uncover-hidden-talents | active | global | `my-skills/uncover-hidden-talents` |
| video-production | active | global | `my-skills/video-production` |
| wait-what | active | global | `my-skills/wait-what` |
| wayfinder | active | global | `my-skills/wayfinder` |
| wechat-article | active | global | `my-skills/wechat-article` |
| wf-construction-full-feature | active | global | `~/.agents/skills/wf-construction-full-feature` |
| wf-diagnose | active | global | `~/.agents/skills/wf-diagnose` |
| wf-explore | active | global | `~/.agents/skills/wf-explore` |
| wf-optimize | active | global | `~/.agents/skills/wf-optimize` |
| wizard | active | global | `my-skills/wizard` |
| workspace-convergence-audit | active | global | `my-skills/workspace-convergence-audit`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/workspace-convergence-audit） |
| writing-great-skills | active | global | `my-skills/writing-great-skills` |

## 宿主限定说明

以下技能虽为 global 范围，但已在登记表用 `excluded_agent_roots` 限定只桥接指定宿主，勿手工补链到其他端。

| 技能 | 仅桥接 | 排除原因 |
|---|---|---|
| codex-bridge-chatgpt | `~/.codex/skills` | Codex 专属：依赖 Codex 内置浏览器能力（`browser:control-in-app-browser`）与 ChatGPT 桌面应用，其他宿主无对应能力 |
| research | 排除 `~/.hermes/skills` | Hermes 的 research 是包含多个内置技能的分类目录，不可替换为公共技能 |
