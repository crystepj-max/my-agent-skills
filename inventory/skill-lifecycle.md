# 技能生命周期

本表是本轮正式策略 `inventory/skill-policy.json` 的人读状态版本。状态和范围决定登记入口；描述与来源历史见 [skill-desc-translation.md](skill-desc-translation.md)。本轮正式 `apply`、`check` 与重复检查通过；独立入口核验确认 37 项全局入口已退出、35 个项目技能实例就位、5 项 hold 的本机源和别名保持，64 项管理测试通过。100 条参考副本已通过两个恢复入口分别核验，均为 100/100 完整指纹匹配（离线包 SHA-256：`410ebcee70e2cbe53007f4af7c756dfb5d008225681535b90a964bdeb76b94de`）；新会话可见性、创作/投研/游戏业务行为、Windows 恢复与用户验收仍未验证。

登记共 137 条：`first-party` 122 条（active 116、retired 6）；`third-party` 15 条（transition 1、reference 12、retired 2）。范围为 `global` 95、`presentations` 20、`investments` 20、`gawain` 2。`test-report-html` 通过一条 `project_sources` 同时映射 Gawain 与 AUTOTEST，按一个登记名计数。登记 `reference_copies` 共 100 条：保留 142 行基线中其他来源与原件记录，排除 5 项本机待讨论项，并纳入 main 中新增且已核指纹的 3 项 DSH/workspace 原件参考。本机待讨论且不进入本次分发策略、参考副本或离线包的技能仅记名称：`improve-codebase-architecture`、`prototype`、`pr`、`retro`、`setup-pre-commit`。

| 技能 | 状态 | 范围 | 正式来源 |
|---|---|---|---|
| agent-cli-tool-residue-purge | active | global | `my-skills/agent-cli-tool-residue-purge` |
| agent-skill-bridge | active | global | `my-skills/agent-skill-bridge` |
| agnes-ai-generation-skill | retired | global | `~/.local/share/agent-skills/retired/20261016/agnes-ai-generation-skill` |
| ask-matt | active | global | `my-skills/ask-matt` |
| baoyu-comic | active | presentations | `project:presentations/.agents/skills/baoyu-comic` |
| baoyu-image-gen | active | presentations | `project:presentations/.agents/skills/baoyu-image-gen` |
| baoyu-infographic | active | presentations | `project:presentations/.agents/skills/baoyu-infographic` |
| baoyu-slide-deck | reference | presentations | `project:presentations/.agent-assets/presentations/baoyu-slide-deck` |
| beautiful-html-templates | reference | presentations | `project:presentations/.agent-assets/presentations/beautiful-html-templates` |
| bottleneck-hunter | active | investments | `project:investments/codex-skills/bottleneck-hunter` |
| chatgpt-web-bridge | active | global | `my-skills/chatgpt-web-bridge`（说明：通用 ChatGPT 网页桥接；通道优先级 codex-in-app-browser → user-chrome（用户已登录 Chrome 会话）→ host-browser-use；reasoning 与 image 两类任务合同；启用前需通过 automation-consent 同意门；自动传输属非官方实验特性，有账号风险，禁止无头/反检测执行。） |
| clashx-openai-sse-debug | active | global | `my-skills/clashx-openai-sse-debug` |
| cnb-git | active | global | `my-skills/cnb-git`（说明：按实际 upstream remote 与服务端分支执行 fetch/pull；凭据仅注入 CNB URL；不自动删 Git lock，clone/fetch/pull 错误明确失败。） |
| cnb-push | active | global | `my-skills/cnb-push`（说明：CNB 推送封装；区分现有仓更新与首次上传，--all/--set-default 按其实际影响范围授权并复用既有授权。） |
| code-review | active | global | `my-skills/code-review` |
| codebase-design | active | global | `my-skills/codebase-design` |
| codex-bridge-chatgpt | transition | global | `~/.agents/skills/codex-bridge-chatgpt`（说明：2026-10-14 曾在 16:55 退役（判定无实用价值），当日 22:21 用户要求装回并恢复治理。来源不可考：无 git / README / LICENSE，全文无 URL 或作者声明，安装时间戳同为一秒。启用需先取得浏览器自动化授权（automation-consent状态为 missing_state，未授权时不会操作 ChatGPT）。功能与 codex-with-chatgpt 重叠：旧的靠人工粘贴 1–3K 上下文包，新靠 MCP 只读连接器。；宿主限制：Codex 专属：依赖 Codex 内置浏览器能力（browser:control-in-app-browser）与 ChatGPT 桌面应用，其他宿主无对应能力，桥接即为坏副本） |
| construction-bootstrap | retired | global | `~/.local/share/agent-skills/retired/construction-bootstrap` |
| cross-domain-borrowing | active | global | `my-skills/cross-domain-borrowing` |
| deep-company-series | active | investments | `project:investments/codex-skills/deep-company-series` |
| dev-workflow-2-0 | retired | global | `~/.local/share/agent-skills/retired/dev-workflow-2-0`（调用范围：explicit-legacy-only） |
| diagnosing-bugs | reference | global | `~/.local/share/agent-skills/references/diagnosing-bugs` |
| domain-modeling | active | global | `my-skills/domain-modeling` |
| dsh-source-upgrade | active | global | `my-skills/dsh-source-upgrade`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/dsh-source-upgrade） |
| dsh-web-access-recovery | active | global | `my-skills/dsh-web-access-recovery`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/dsh-web-access-recovery） |
| duplicate-cli-unify | active | global | `my-skills/duplicate-cli-unify` |
| dyp-ask | active | investments | `project:investments/codex-skills/dyp-ask` |
| earnings-review | active | investments | `project:investments/codex-skills/earnings-review` |
| earnings-team | active | investments | `project:investments/codex-skills/earnings-team` |
| edit-article | active | presentations | `project:presentations/.agents/skills/edit-article` |
| eli5 | active | presentations | `project:presentations/.agents/skills/eli5` |
| execution-plan | retired | global | `~/.local/share/agent-skills/retired/execution-plan`（历史副本保留；正式入口为 dev-flow 项目级技能） |
| expert-consultation | active | global | `my-skills/expert-consultation` |
| fact-check | active | global | `my-skills/fact-check` |
| financial-data | active | investments | `project:investments/codex-skills/financial-data` |
| find-skills | reference | global | `~/.local/share/agent-skills/reference/find-skills` |
| first-principle | active | global | `my-skills/first-principle` |
| frontend-design | active | presentations | `project:presentations/.agents/skills/frontend-design` |
| frontend-slides | reference | presentations | `project:presentations/.agent-assets/presentations/frontend-slides` |
| git-guardrails-claude-code | retired | global | `~/.local/share/agent-skills/retired/20261016/git-guardrails-claude-code` |
| grill-me | active | global | `my-skills/grill-me` |
| grill-with-docs | active | global | `my-skills/grill-with-docs` |
| grilling | active | global | `my-skills/grilling` |
| guizang-ppt-skill | reference | presentations | `project:presentations/.agent-assets/presentations/guizang-ppt-skill` |
| handoff | active | global | `my-skills/handoff` |
| hatch-pet | active | presentations | `project:presentations/.agents/skills/hatch-pet` |
| humanize-ppt | reference | presentations | `project:presentations/.agent-assets/presentations/humanize-ppt` |
| implement | reference | global | `~/.local/share/agent-skills/reference/implement` |
| implement-spec | active | global | `my-skills/implement-spec` |
| income-investment | active | investments | `project:investments/codex-skills/income-investment` |
| industry-funnel | active | investments | `project:investments/codex-skills/industry-funnel` |
| industry-research | active | investments | `project:investments/codex-skills/industry-research` |
| investment-checklist | active | investments | `project:investments/codex-skills/investment-checklist` |
| investment-memo-craft | active | investments | `project:investments/codex-skills/investment-memo-craft` |
| investment-research | active | investments | `project:investments/codex-skills/investment-research` |
| investment-team | active | investments | `project:investments/codex-skills/investment-team` |
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
| management-deep-dive | active | investments | `project:investments/codex-skills/management-deep-dive` |
| migrate-to-shoehorn | active | global | `my-skills/migrate-to-shoehorn` |
| minimum-scale-experiment | active | global | `my-skills/minimum-scale-experiment` |
| neat-freak | active | global | `my-skills/neat-freak` |
| news-pulse | active | investments | `project:investments/codex-skills/news-pulse` |
| obsidian-vault | active | presentations | `project:presentations/.agents/skills/obsidian-vault` |
| portfolio-review | active | investments | `project:investments/codex-skills/portfolio-review` |
| ppt-master | reference | presentations | `project:presentations/.agent-assets/presentations/ppt-master` |
| presentation-production | active | presentations | `my-skills/presentation-production` |
| private-company-research | active | investments | `project:investments/codex-skills/private-company-research` |
| quality-screen | active | investments | `project:investments/codex-skills/quality-screen` |
| remotion-best-practices | active | presentations | `project:presentations/.agents/skills/remotion-best-practices` |
| remotion-video-production | active | presentations | `project:presentations/.agents/skills/remotion-video-production` |
| remotion-video-toolkit | active | presentations | `project:presentations/.agents/skills/remotion-video-toolkit` |
| requirements-analysis.bak-20260905-224705 | retired | global | `~/.local/share/agent-skills/retired/requirements-analysis.bak-20260905-224705` |
| research | active | global | `my-skills/research`（宿主限制：Hermes 的 research 是包含多个内置技能的分类目录，不可替换为公共技能） |
| resolving-merge-conflicts | retired | global | `~/.local/share/agent-skills/retired/resolving-merge-conflicts`（退役日期：2026-10-06；退役原因：上游 mattpocock/skills v1.3.0 已移除该 skill（无替代，agent 自行处理合并/rebase 冲突）） |
| scaffold-exercises | active | global | `my-skills/scaffold-exercises` |
| setup-matt-pocock-skills | active | global | `my-skills/setup-matt-pocock-skills` |
| skill-creator | reference | global | `~/.local/share/agent-skills/references/skill-creator`（替代：skill-workbench） |
| skill-workbench | active | global | `my-skills/skill-workbench` |
| skills-security-check | active | global | `my-skills/skills-security-check` |
| socratic-clarify | active | global | `my-skills/socratic-clarify` |
| steelmanning | active | global | `my-skills/steelmanning` |
| storage-analyzer | active | global | `my-skills/storage-analyzer` |
| sts2-gawain-regression-recovery | active | gawain | `project:gawain/skills/sts2-gawain-regression-recovery` |
| sts2-independent-run-regression | retired | global | `~/.local/share/agent-skills/retired/20261016/sts2-independent-run-regression` |
| sts2-start-game | active | global | `my-skills/sts2-start-game` |
| tdd | active | global | `my-skills/tdd` |
| teach | active | global | `my-skills/teach` |
| test-report-html | active | gawain | gawain: `project:gawain/.agents/skills/test-report-html`；autotest: `project:autotest/.agents/skills/test-report-html` |
| thesis-drift | active | investments | `project:investments/codex-skills/thesis-drift` |
| thesis-tracker | active | investments | `project:investments/codex-skills/thesis-tracker` |
| to-questionnaire | active | global | `my-skills/to-questionnaire` |
| to-spec | reference | global | `~/.local/share/agent-skills/reference/to-spec` |
| to-tickets | reference | global | `~/.local/share/agent-skills/reference/to-tickets` |
| triage | active | global | `my-skills/triage` |
| typesafe-ai | active | global | `my-skills/typesafe-ai` |
| uncover-hidden-talents | active | global | `my-skills/uncover-hidden-talents` |
| video-production | active | presentations | `project:presentations/.agents/skills/video-production` |
| wait-what | active | global | `my-skills/wait-what` |
| wayfinder | active | global | `my-skills/wayfinder` |
| wechat-article | active | presentations | `project:presentations/.agents/skills/wechat-article` |
| wf-construction-full-feature | active | global | `~/.agents/skills/wf-construction-full-feature` |
| wf-diagnose | active | global | `~/.agents/skills/wf-diagnose` |
| wf-explore | active | global | `~/.agents/skills/wf-explore` |
| wf-optimize | active | global | `~/.agents/skills/wf-optimize` |
| wizard | active | global | `my-skills/wizard` |
| workspace-convergence-audit | active | global | `my-skills/workspace-convergence-audit`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/workspace-convergence-audit） |
| writing-great-skills | active | global | `my-skills/writing-great-skills` |
