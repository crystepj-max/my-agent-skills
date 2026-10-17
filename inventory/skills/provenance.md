# Skill 来源与版本档案

本档案按正式策略登记的 `first-party` 技能逐项列示。`first-party` 表示当前由本人/本项目维护，不自动等同于“从零原创”。来源结论以证据为准；“未确证”表示目前没有可靠出处，不据名称或相似度推断。

## 日期口径

- **创建/首次入档日期**：本表只把可核对的本仓 Git 最早提交日期作为“首次入档”；它不证明原始创作日期。当前 Git 历史没有记录时写“未记录”，不把迁入本仓日期当作创作日期。
- **最近修订日期**：优先记录当前维护源中可核对的最近一次 Git 提交日期；未提交或没有相关历史时写“未记录”。它不代表该技能从未更新。
- **外部参考版本/日期**：必须记录仓库、技能路径、固定 commit、上游提交日期及本地获取日期。只有分支名或网页当前内容不足以锁定参考版本。无外部来源的第一方技能记“无已确认外部参考”。
- **修订历史**：Git 可用时按技能路径查看提交历史；后续重要的非 Git 来源变更也应在本档案记录日期与说明。

更新上游时，将快照保存在技能发现目录之外，以 commit 固定版本；再用 `tools/compare_skill_reference.py` 输出只读差异。比较报告须保留快照路径、上游 commit、日期和报告日期。此流程只用于检查，不自动把上游内容覆盖到维护源。

## 技能来源与日期登记
> 本节保留原 122 项第一方技能的来源/日期档案；当前 127 个维护源及新增 5 项的来源映射见后文。按字母分组，来源结论与维护路径、日期记录分开查阅。`first-party` 表示当前维护责任，不等于原创声明；“未记录”表示现有材料无法证明日期。

### 来源与维护路径

以下“参考版本”保留原登记的来源线索；如尚无固定 commit 和获取日期，会明确标出，不能据此判断上游是否已有更新。

#### A–F｜来源与维护路径

| Skill | 当前维护源 | 出处/作者结论 | 外部参考版本/日期 |
|---|---|---|---|
| `agent-cli-tool-residue-purge` | `my-skills/agent-cli-tool-residue-purge` | 按确认结果：无可靠第三方参考源，作为第一方维护 | 无已确认外部参考 |
| `agent-skill-bridge` | `my-skills/agent-skill-bridge` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `agnes-ai-generation-skill` | `~/.local/share/agent-skills/retired/20261016/agnes-ai-generation-skill` | 历史来源清单：[github.com/Yacey/agnes-ai-generation-skill](https://github.com/Yacey/agnes-ai-generation-skill)；inventory/skills/descriptions-zh.md 记录 GitHub Yacey/agnes-ai-generation-skill。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `ask-matt` | `my-skills/ask-matt` | 旧来源表线索：[仓库/来源](https://github.com/mattpocock/skills)（历史归属，非作者结论） | 见出处/作者线索；固定版本与获取日期未登记 |
| `baoyu-comic` | `project:presentations/.agents/skills/baoyu-comic` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-comic) | 见出处/作者线索；固定版本与获取日期未登记 |
| `baoyu-image-gen` | `project:presentations/.agents/skills/baoyu-image-gen` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-image-gen)；来源说明：原 SKILL.md 的 homepage 指向 JimLiu/baoyu-skills；inventory/skills/descriptions-zh.md 将来源列为平台内置。并存记录，不推断安装来源。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `baoyu-infographic` | `project:presentations/.agents/skills/baoyu-infographic` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-infographic)；来源说明：原 SKILL.md 的 homepage 指向 JimLiu/baoyu-skills；inventory/skills/descriptions-zh.md 将来源列为平台内置。并存记录，不推断安装来源。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `bottleneck-hunter` | `project:investments/codex-skills/bottleneck-hunter` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `chatgpt-web-bridge` | `my-skills/chatgpt-web-bridge` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `clashx-openai-sse-debug` | `my-skills/clashx-openai-sse-debug` | 按确认结果：无可靠第三方参考源，作为第一方维护 | 无已确认外部参考 |
| `cnb-git` | `my-skills/cnb-git` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `cnb-push` | `my-skills/cnb-push` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `code-review` | `my-skills/code-review` | 已确认：mattpocock/skills · skills/engineering/code-review | 固定 commit、上游提交日期及本地获取日期未登记 |
| `codebase-design` | `my-skills/codebase-design` | 已确认：mattpocock/skills · skills/engineering/codebase-design | 固定 commit、上游提交日期及本地获取日期未登记 |
| `construction-bootstrap` | `~/.local/share/agent-skills/retired/construction-bootstrap` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `cross-domain-borrowing` | `my-skills/cross-domain-borrowing` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `deep-company-series` | `project:investments/codex-skills/deep-company-series` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `dev-workflow-2-0` | `~/.local/share/agent-skills/retired/dev-workflow-2-0` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `domain-modeling` | `my-skills/domain-modeling` | 已确认：mattpocock/skills · skills/engineering/domain-modeling | 固定 commit、上游提交日期及本地获取日期未登记 |
| `dsh-source-upgrade` | `my-skills/dsh-source-upgrade` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `dsh-web-access-recovery` | `my-skills/dsh-web-access-recovery` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `duplicate-cli-unify` | `my-skills/duplicate-cli-unify` | 按确认结果：无可靠第三方参考源，作为第一方维护 | 无已确认外部参考 |
| `dyp-ask` | `project:investments/codex-skills/dyp-ask` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `earnings-review` | `project:investments/codex-skills/earnings-review` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `earnings-team` | `project:investments/codex-skills/earnings-team` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `edit-article` | `project:presentations/.agents/skills/edit-article` | 历史来源清单：WorkBuddy 内置 / 应用市场；inventory/skills/descriptions-zh.md 将其列为 WorkBuddy/平台内置；未将其改称独立 GitHub 上游。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `eli5` | `project:presentations/.agents/skills/eli5` | 历史来源清单：[github.com/companion-inc/feynman](https://github.com/companion-inc/feynman)；inventory/skills/descriptions-zh.md 记录 GitHub companion-inc/feynman。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `execution-plan` | `~/.local/share/agent-skills/retired/execution-plan` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `expert-consultation` | `my-skills/expert-consultation` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `fact-check` | `my-skills/fact-check` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `financial-data` | `project:investments/codex-skills/financial-data` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `first-principle` | `my-skills/first-principle` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `frontend-design` | `project:presentations/.agents/skills/frontend-design` | 历史来源清单：[github.com/anthropics/skills](https://github.com/anthropics/skills)；inventory/skills/descriptions-zh.md 记录 Anthropic 官方 skills 仓库。 | 见出处/作者线索；固定版本与获取日期未登记 |

#### G–L｜来源与维护路径

| Skill | 当前维护源 | 出处/作者结论 | 外部参考版本/日期 |
|---|---|---|---|
| `git-guardrails-claude-code` | `~/.local/share/agent-skills/retired/20261016/git-guardrails-claude-code` | 已确认：mattpocock/skills · skills/misc/git-guardrails-claude-code | 固定 commit、上游提交日期及本地获取日期未登记 |
| `grill-me` | `my-skills/grill-me` | 已确认：mattpocock/skills · skills/productivity/grill-me | 固定 commit、上游提交日期及本地获取日期未登记 |
| `grill-with-docs` | `my-skills/grill-with-docs` | 已确认：mattpocock/skills · skills/engineering/grill-with-docs | 固定 commit、上游提交日期及本地获取日期未登记 |
| `grilling` | `my-skills/grilling` | 已确认：mattpocock/skills · skills/productivity/grilling | 固定 commit、上游提交日期及本地获取日期未登记 |
| `handoff` | `my-skills/handoff` | 旧来源表线索：[仓库/来源](https://github.com/mattpocock/skills)（历史归属，非作者结论） | 见出处/作者线索；固定版本与获取日期未登记 |
| `hatch-pet` | `project:presentations/.agents/skills/hatch-pet` | 历史来源清单：[github.com/openai/skills](https://github.com/openai/skills)；inventory/skills/descriptions-zh.md 记录 OpenAI 官方 skills 仓库。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `implement-spec` | `my-skills/implement-spec` | [登记来源链接](https://github.com/mattpocock/skills/tree/main/skills/engineering/implement-spec) | 见出处/作者线索；固定版本与获取日期未登记 |
| `income-investment` | `project:investments/codex-skills/income-investment` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `industry-funnel` | `project:investments/codex-skills/industry-funnel` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `industry-research` | `project:investments/codex-skills/industry-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `investment-checklist` | `project:investments/codex-skills/investment-checklist` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `investment-memo-craft` | `project:investments/codex-skills/investment-memo-craft` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `investment-research` | `project:investments/codex-skills/investment-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `investment-team` | `project:investments/codex-skills/investment-team` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-approval` | `my-skills/lark-approval` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-approval.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-apps` | `my-skills/lark-apps` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-apps.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-attendance` | `my-skills/lark-attendance` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-attendance.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-base` | `my-skills/lark-base` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-base.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-calendar` | `my-skills/lark-calendar` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-calendar.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-contact` | `my-skills/lark-contact` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-contact.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-doc` | `my-skills/lark-doc` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-doc.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-drive` | `my-skills/lark-drive` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-drive.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-event` | `my-skills/lark-event` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-event.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-im` | `my-skills/lark-im` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-im.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-mail` | `my-skills/lark-mail` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-mail.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-markdown` | `my-skills/lark-markdown` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-markdown.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-meeting` | `my-skills/lark-meeting` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-meeting.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-minutes` | `my-skills/lark-minutes` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-minutes.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-note` | `my-skills/lark-note` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-note.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-okr` | `my-skills/lark-okr` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-okr.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-openapi-explorer` | `my-skills/lark-openapi-explorer` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-openapi-explorer.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-shared` | `my-skills/lark-shared` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-shared.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-sheets` | `my-skills/lark-sheets` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-sheets.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-skill-maker` | `my-skills/lark-skill-maker` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-skill-maker.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-slides` | `my-skills/lark-slides` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-slides.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-task` | `my-skills/lark-task` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-task.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-vc` | `my-skills/lark-vc` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-vc.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-vc-agent` | `my-skills/lark-vc-agent` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-vc-agent.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-whiteboard` | `my-skills/lark-whiteboard` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-whiteboard.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-wiki` | `my-skills/lark-wiki` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-wiki.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-workflow-meeting-summary` | `my-skills/lark-workflow-meeting-summary` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-workflow-meeting-summary.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `lark-workflow-standup-report` | `my-skills/lark-workflow-standup-report` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-workflow-standup-report.tar.gz) | 见出处/作者线索；固定版本与获取日期未登记 |
| `learn_something_new` | `my-skills/learn_something_new` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `life-design` | `my-skills/life-design` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `llm-wiki-app` | `my-skills/llm-wiki-app` | 未确证独立上游；仓库登记与包内来源一致。 | 见出处/作者线索；固定版本与获取日期未登记 |

#### M–R｜来源与维护路径

| Skill | 当前维护源 | 出处/作者结论 | 外部参考版本/日期 |
|---|---|---|---|
| `management-deep-dive` | `project:investments/codex-skills/management-deep-dive` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `migrate-to-shoehorn` | `my-skills/migrate-to-shoehorn` | 已确认：mattpocock/skills · skills/misc/migrate-to-shoehorn | 固定 commit、上游提交日期及本地获取日期未登记 |
| `minimum-scale-experiment` | `my-skills/minimum-scale-experiment` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `neat-freak` | `my-skills/neat-freak` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `news-pulse` | `project:investments/codex-skills/news-pulse` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `obsidian-vault` | `project:presentations/.agents/skills/obsidian-vault` | 按确认结果：无可靠第三方参考源，作为第一方维护 | 无已确认外部参考 |
| `portfolio-review` | `project:investments/codex-skills/portfolio-review` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `presentation-production` | `my-skills/presentation-production` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `private-company-research` | `project:investments/codex-skills/private-company-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `quality-screen` | `project:investments/codex-skills/quality-screen` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `remotion-best-practices` | `project:presentations/.agents/skills/remotion-best-practices` | 未确证独立上游；inventory/skills/descriptions-zh.md 将其列为 WorkBuddy/平台内置；未将其改称独立 GitHub 上游。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `remotion-video-production` | `project:presentations/.agents/skills/remotion-video-production` | 历史来源清单：[github.com/akillness/jeo-skills](https://github.com/akillness/jeo-skills)；inventory/skills/descriptions-zh.md 记录 akillness/jeo-skills；当前包作为兼容别名。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `remotion-video-toolkit` | `project:presentations/.agents/skills/remotion-video-toolkit` | 历史来源清单：[github.com/shreefentsar/remotion-video-toolkit](https://github.com/shreefentsar/remotion-video-toolkit)；inventory/skills/descriptions-zh.md 记录 shreefentsar/remotion-video-toolkit。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `research` | `my-skills/research` | 已确认：mattpocock/skills · skills/engineering/research | 固定 commit、上游提交日期及本地获取日期未登记 |

#### S–Z｜来源与维护路径

| Skill | 当前维护源 | 出处/作者结论 | 外部参考版本/日期 |
|---|---|---|---|
| `scaffold-exercises` | `my-skills/scaffold-exercises` | 已确认：mattpocock/skills · skills/misc/scaffold-exercises | 固定 commit、上游提交日期及本地获取日期未登记 |
| `setup-matt-pocock-skills` | `my-skills/setup-matt-pocock-skills` | 已确认：mattpocock/skills · skills/engineering/setup-matt-pocock-skills | 固定 commit、上游提交日期及本地获取日期未登记 |
| `skill-workbench` | `my-skills/skill-workbench` | 原始上游未确证；不推断作者或仓库 | 见出处/作者线索；固定版本与获取日期未登记 |
| `skills-security-check` | `my-skills/skills-security-check` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `socratic-clarify` | `my-skills/socratic-clarify` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `steelmanning` | `my-skills/steelmanning` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `storage-analyzer` | `my-skills/storage-analyzer` | 原始上游未确证；不推断作者或仓库 | 见出处/作者线索；固定版本与获取日期未登记 |
| `sts2-gawain-regression-recovery` | `project:gawain/skills/sts2-gawain-regression-recovery` | 当前 Gawain 项目维护源已知；原作者与最初上游未确证 | 见出处/作者线索；固定版本与获取日期未登记 |
| `sts2-independent-run-regression` | `~/.local/share/agent-skills/retired/20261016/sts2-independent-run-regression` | 由本仓接管维护；原作者与最初上游未确证，不推断作者或仓库 | 见出处/作者线索；固定版本与获取日期未登记 |
| `sts2-start-game` | `my-skills/sts2-start-game` | 已知 Git 来源：`crystepj-max/STS2-AUTOTEST`；技能路径提交 `860ed5048ee4f4101046c213728bfdb618b4478d`，审计 HEAD `41f89387fa31d8208b277054828b6de00efe6eaf`。当前维护源从安装快照接管并保留其改进；该提交不代表安装版哈希或原创作者确证。 | 未确证外部参考版本 |
| `tdd` | `my-skills/tdd` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `teach` | `my-skills/teach` | 已确认：mattpocock/skills · skills/productivity/teach | 固定 commit、上游提交日期及本地获取日期未登记 |
| `test-report-html` | `project:gawain/.agents/skills/test-report-html` | 按确认结果：无可靠第三方参考源，作为第一方维护 | 无已确认外部参考 |
| `thesis-drift` | `project:investments/codex-skills/thesis-drift` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `thesis-tracker` | `project:investments/codex-skills/thesis-tracker` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) | 见出处/作者线索；固定版本与获取日期未登记 |
| `to-questionnaire` | `my-skills/to-questionnaire` | 已确认：mattpocock/skills · skills/productivity/to-questionnaire | 固定 commit、上游提交日期及本地获取日期未登记 |
| `triage` | `my-skills/triage` | 已确认：mattpocock/skills · skills/engineering/triage | 固定 commit、上游提交日期及本地获取日期未登记 |
| `typesafe-ai` | `my-skills/typesafe-ai` | [登记来源链接](https://github.com/typesafe-ai/skills.git) | 见出处/作者线索；固定版本与获取日期未登记 |
| `uncover-hidden-talents` | `my-skills/uncover-hidden-talents` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `video-production` | `project:presentations/.agents/skills/video-production` | 历史来源清单：[github.com/jmagly/aiwg](https://github.com/jmagly/aiwg)；inventory/skills/descriptions-zh.md 记录 jmagly/aiwg。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `wait-what` | `my-skills/wait-what` | 已确认：mattpocock/skills · skills/productivity/wait-what | 固定 commit、上游提交日期及本地获取日期未登记 |
| `wayfinder` | `my-skills/wayfinder` | 已确认：mattpocock/skills · skills/engineering/wayfinder | 固定 commit、上游提交日期及本地获取日期未登记 |
| `wechat-article` | `project:presentations/.agents/skills/wechat-article` | 未确证独立上游；tools/add_repo_column.py 将其映射到 ai-berkshire 且该仓存在同名 canonical/generated 文件；inventory 行记“平台内置”。正文匹配度只作定位，报告保留该冲突。 | 见出处/作者线索；固定版本与获取日期未登记 |
| `wf-construction-full-feature` | `~/.agents/skills/wf-construction-full-feature` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `wf-diagnose` | `~/.agents/skills/wf-diagnose` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `wf-explore` | `~/.agents/skills/wf-explore` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `wf-optimize` | `~/.agents/skills/wf-optimize` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `wizard` | `my-skills/wizard` | 已确认：mattpocock/skills · skills/engineering/wizard | 固定 commit、上游提交日期及本地获取日期未登记 |
| `workspace-convergence-audit` | `my-skills/workspace-convergence-audit` | 来源尚未确证；登记维护源不构成原创声明 | 未确证外部参考版本 |
| `writing-great-skills` | `my-skills/writing-great-skills` | 未确证独立上游；证据支持“Matt Pocock/mattpocock/skills 为上游作者及技能来源，sickn33/agentic-awesome-skills 为目录/分发记录”并存。检查 ~/.agents/.skill-lock.json 未发现此技能的 lock 项，因此精确安装来源和安装 commit 未确证。 | 见出处/作者线索；固定版本与获取日期未登记 |

### 创建与修订日期

日期取自可核对的本仓 Git 历史：首次入档日期不是原始创作日期；最近修订日期仅覆盖可查到的提交。没有记录时不以文件时间戳或迁移日期代替。

#### A–F｜日期

| Skill | 首次入档 | 最近可核对修订 |
|---|---|---|
| `agent-cli-tool-residue-purge` | 未记录 | 未记录 |
| `agent-skill-bridge` | 2026-08-12 | 2026-10-10 |
| `agnes-ai-generation-skill` | 未记录 | 未记录 |
| `ask-matt` | 未记录 | 未记录 |
| `baoyu-comic` | 未记录 | 未记录 |
| `baoyu-image-gen` | 未记录 | 未记录 |
| `baoyu-infographic` | 未记录 | 未记录 |
| `bottleneck-hunter` | 未记录 | 未记录 |
| `chatgpt-web-bridge` | 未记录 | 未记录 |
| `clashx-openai-sse-debug` | 未记录 | 未记录 |
| `cnb-git` | 2026-09-16 | 2026-09-16 |
| `cnb-push` | 2026-09-16 | 2026-09-16 |
| `code-review` | 未记录 | 未记录 |
| `codebase-design` | 未记录 | 未记录 |
| `construction-bootstrap` | 未记录 | 未记录 |
| `cross-domain-borrowing` | 2026-09-02 | 2026-09-02 |
| `deep-company-series` | 未记录 | 未记录 |
| `dev-workflow-2-0` | 未记录 | 未记录 |
| `domain-modeling` | 未记录 | 未记录 |
| `dsh-source-upgrade` | 未记录 | 未记录 |
| `dsh-web-access-recovery` | 未记录 | 未记录 |
| `duplicate-cli-unify` | 未记录 | 未记录 |
| `dyp-ask` | 未记录 | 未记录 |
| `earnings-review` | 未记录 | 未记录 |
| `earnings-team` | 未记录 | 未记录 |
| `edit-article` | 未记录 | 未记录 |
| `eli5` | 未记录 | 未记录 |
| `execution-plan` | 未记录 | 未记录 |
| `expert-consultation` | 2026-09-01 | 2026-09-01 |
| `fact-check` | 2026-09-01 | 2026-09-01 |
| `financial-data` | 未记录 | 未记录 |
| `first-principle` | 2026-08-25 | 2026-08-25 |
| `frontend-design` | 未记录 | 未记录 |

#### G–L｜日期

| Skill | 首次入档 | 最近可核对修订 |
|---|---|---|
| `git-guardrails-claude-code` | 未记录 | 未记录 |
| `grill-me` | 未记录 | 未记录 |
| `grill-with-docs` | 未记录 | 未记录 |
| `grilling` | 未记录 | 未记录 |
| `handoff` | 未记录 | 未记录 |
| `hatch-pet` | 未记录 | 未记录 |
| `implement-spec` | 未记录 | 未记录 |
| `income-investment` | 未记录 | 未记录 |
| `industry-funnel` | 未记录 | 未记录 |
| `industry-research` | 未记录 | 未记录 |
| `investment-checklist` | 未记录 | 未记录 |
| `investment-memo-craft` | 未记录 | 未记录 |
| `investment-research` | 未记录 | 未记录 |
| `investment-team` | 未记录 | 未记录 |
| `lark-approval` | 未记录 | 未记录 |
| `lark-apps` | 未记录 | 未记录 |
| `lark-attendance` | 未记录 | 未记录 |
| `lark-base` | 未记录 | 未记录 |
| `lark-calendar` | 未记录 | 未记录 |
| `lark-contact` | 未记录 | 未记录 |
| `lark-doc` | 未记录 | 未记录 |
| `lark-drive` | 未记录 | 未记录 |
| `lark-event` | 未记录 | 未记录 |
| `lark-im` | 未记录 | 未记录 |
| `lark-mail` | 未记录 | 未记录 |
| `lark-markdown` | 未记录 | 未记录 |
| `lark-meeting` | 未记录 | 未记录 |
| `lark-minutes` | 未记录 | 未记录 |
| `lark-note` | 未记录 | 未记录 |
| `lark-okr` | 未记录 | 未记录 |
| `lark-openapi-explorer` | 未记录 | 未记录 |
| `lark-shared` | 未记录 | 未记录 |
| `lark-sheets` | 未记录 | 未记录 |
| `lark-skill-maker` | 未记录 | 未记录 |
| `lark-slides` | 未记录 | 未记录 |
| `lark-task` | 未记录 | 未记录 |
| `lark-vc` | 未记录 | 未记录 |
| `lark-vc-agent` | 未记录 | 未记录 |
| `lark-whiteboard` | 未记录 | 未记录 |
| `lark-wiki` | 未记录 | 未记录 |
| `lark-workflow-meeting-summary` | 未记录 | 未记录 |
| `lark-workflow-standup-report` | 未记录 | 未记录 |
| `learn_something_new` | 2026-08-25 | 2026-08-25 |
| `life-design` | 2026-09-04 | 2026-09-04 |
| `llm-wiki-app` | 未记录 | 未记录 |

#### M–R｜日期

| Skill | 首次入档 | 最近可核对修订 |
|---|---|---|
| `management-deep-dive` | 未记录 | 未记录 |
| `migrate-to-shoehorn` | 未记录 | 未记录 |
| `minimum-scale-experiment` | 2026-09-04 | 2026-09-04 |
| `neat-freak` | 2026-09-09 | 2026-10-05 |
| `news-pulse` | 未记录 | 未记录 |
| `obsidian-vault` | 未记录 | 未记录 |
| `portfolio-review` | 未记录 | 未记录 |
| `presentation-production` | 2026-09-09 | 2026-09-09 |
| `private-company-research` | 未记录 | 未记录 |
| `quality-screen` | 未记录 | 未记录 |
| `remotion-best-practices` | 未记录 | 未记录 |
| `remotion-video-production` | 未记录 | 未记录 |
| `remotion-video-toolkit` | 未记录 | 未记录 |
| `research` | 未记录 | 未记录 |

#### S–Z｜日期

| Skill | 首次入档 | 最近可核对修订 |
|---|---|---|
| `scaffold-exercises` | 未记录 | 未记录 |
| `setup-matt-pocock-skills` | 未记录 | 未记录 |
| `skill-workbench` | 未记录 | 未记录 |
| `skills-security-check` | 2026-08-12 | 2026-08-12 |
| `socratic-clarify` | 2026-08-25 | 2026-09-09 |
| `steelmanning` | 2026-09-04 | 2026-09-04 |
| `storage-analyzer` | 未记录 | 未记录 |
| `sts2-gawain-regression-recovery` | 未记录 | 未记录 |
| `sts2-independent-run-regression` | 未记录 | 未记录 |
| `sts2-start-game` | 未记录 | 未记录 |
| `tdd` | 2026-09-09 | 2026-09-09 |
| `teach` | 未记录 | 未记录 |
| `test-report-html` | 未记录 | 未记录 |
| `thesis-drift` | 未记录 | 未记录 |
| `thesis-tracker` | 未记录 | 未记录 |
| `to-questionnaire` | 未记录 | 未记录 |
| `triage` | 未记录 | 未记录 |
| `typesafe-ai` | 未记录 | 未记录 |
| `uncover-hidden-talents` | 2026-09-01 | 2026-09-01 |
| `video-production` | 未记录 | 未记录 |
| `wait-what` | 未记录 | 未记录 |
| `wayfinder` | 未记录 | 未记录 |
| `wechat-article` | 未记录 | 未记录 |
| `wf-construction-full-feature` | 未记录 | 未记录 |
| `wf-diagnose` | 未记录 | 未记录 |
| `wf-explore` | 未记录 | 未记录 |
| `wf-optimize` | 未记录 | 未记录 |
| `wizard` | 未记录 | 未记录 |
| `workspace-convergence-audit` | 未记录 | 未记录 |
| `writing-great-skills` | 未记录 | 未记录 |

## 来源待核实的候选

以下结论保留待核实状态，不作为已确认上游：`llm-wiki-app`（候选 `nashsu/llm_wiki_skill`）、`storage-analyzer`（候选 `KKKKhazix/khazix-skills`）、`remotion-best-practices`（候选 Remotion 官方仓库）、`wechat-article`（候选 `xbtlin/ai-berkshire`）。精确参考路径、相似度依据与冲突记录见 [来源说明表](descriptions-zh.md)。未经确认前，不写入已确认上游字段。

`writing-great-skills` 记录上游技能来源 `mattpocock/skills`，分发记录 `sickn33/agentic-awesome-skills`；两者角色不同，不能混写为一个来源。另 5 项无可靠第三方出处的技能按无已确认外部参考的第一方技能管理。两项 STS2 技能按已确认结果作为第一方处理。

## 当前第一方维护源与原件参考映射

本表保留已登记维护来源、范围与原件参考线索；当前状态以正式策略和 [Skills 总览](../skills-summary.md) 为准。历史来源/能力表反映当时公共池记录，不作为现行分发状态。此前暂缓的 5 项现已作为第一方维护源登记；各自旧安装快照另存为只读 reference，不作为执行入口。

「正式维护源」和「原件参考」是不同路径：维护源由正式登记表确定，不等同于原作者/原创声明；原安装快照仅用于历史保留和只读比较，不作为现行入口。上游列只呈现可追溯的来源线索；有来源冲突或未确认时按说明保留，不补造作者和仓库。远端 `main` 的基线为 137 项策略与 100 条 reference；本候选新增 5 项 `first-party/global/active` 登记及 5 条原版 reference，合计 142 项与 105 条，原 137 条登记和 100 条 reference 均保留。候选恢复与入口验证只在隔离临时 HOME 中进行；没有对真实 HOME 执行 `apply`。新会话可见性、真实业务行为、Windows 恢复与用户验收仍未验证。

| Skill | 正式维护源 | 范围 | 原安装快照（来源 → 参考保存位置） | 登记上游/来源线索 |
|---|---|---|---|---|
| `agent-cli-tool-residue-purge` | `my-skills/agent-cli-tool-residue-purge` | 用户级（global） | local-installed-snapshot: `~/.agents/skills/agent-cli-tool-residue-purge` → `~/.local/share/agent-skills/references/agent-cli-tool-residue-purge` | 原始上游未确证；不推断作者或仓库 |
| `agnes-ai-generation-skill` | `~/.local/share/agent-skills/retired/20261016/agnes-ai-generation-skill` | 已退役；完整备份移至 retired/20261016 | installed-snapshot: `~/.agents/skills/agnes-ai-generation-skill` → `~/.local/share/agent-skills/references/agnes-ai-generation-skill` | 历史来源清单：[github.com/Yacey/agnes-ai-generation-skill](https://github.com/Yacey/agnes-ai-generation-skill)；inventory/skills/descriptions-zh.md 记录 GitHub Yacey/agnes-ai-generation-skill。 |
| `ask-matt` | `my-skills/ask-matt` | 用户级（global） | installed-snapshot: `~/.agents/skills/ask-matt` → `~/.local/share/agent-skills/references/ask-matt` | 旧来源表线索：[仓库/来源](https://github.com/mattpocock/skills)（历史归属，非作者结论） |
| `baoyu-comic` | `project:presentations/.agents/skills/baoyu-comic` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/baoyu-comic` → `~/.local/share/agent-skills/references/baoyu-comic` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-comic) |
| `baoyu-image-gen` | `project:presentations/.agents/skills/baoyu-image-gen` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/baoyu-image-gen` → `~/.local/share/agent-skills/references/baoyu-image-gen` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-image-gen)；来源说明：原 SKILL.md 的 homepage 指向 JimLiu/baoyu-skills；inventory/skills/descriptions-zh.md 将来源列为平台内置。并存记录，不推断安装来源。 |
| `baoyu-infographic` | `project:presentations/.agents/skills/baoyu-infographic` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/baoyu-infographic` → `~/.local/share/agent-skills/references/baoyu-infographic` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-infographic)；来源说明：原 SKILL.md 的 homepage 指向 JimLiu/baoyu-skills；inventory/skills/descriptions-zh.md 将来源列为平台内置。并存记录，不推断安装来源。 |
| `bottleneck-hunter` | `project:investments/codex-skills/bottleneck-hunter` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/bottleneck-hunter` → `~/.local/share/agent-skills/references/bottleneck-hunter` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `clashx-openai-sse-debug` | `my-skills/clashx-openai-sse-debug` | 用户级（global） | local-installed-snapshot: `~/.agents/skills/clashx-openai-sse-debug` → `~/.local/share/agent-skills/references/clashx-openai-sse-debug` | 原始上游未确证；不推断作者或仓库 |
| `code-review` | `my-skills/code-review` | 用户级（global） | installed-snapshot: `~/.agents/skills/code-review` → `~/.local/share/agent-skills/references/code-review` | 原始上游未确证；不推断作者或仓库 |
| `codebase-design` | `my-skills/codebase-design` | 用户级（global） | installed-snapshot: `~/.agents/skills/codebase-design` → `~/.local/share/agent-skills/references/codebase-design` | 原始上游未确证；不推断作者或仓库 |
| `deep-company-series` | `project:investments/codex-skills/deep-company-series` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/deep-company-series` → `~/.local/share/agent-skills/references/deep-company-series` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `domain-modeling` | `my-skills/domain-modeling` | 用户级（global） | installed-snapshot: `~/.agents/skills/domain-modeling` → `~/.local/share/agent-skills/references/domain-modeling` | 原始上游未确证；不推断作者或仓库 |
| `duplicate-cli-unify` | `my-skills/duplicate-cli-unify` | 用户级（global） | local-installed-snapshot: `~/.agents/skills/duplicate-cli-unify` → `~/.local/share/agent-skills/references/duplicate-cli-unify` | 原始上游未确证；不推断作者或仓库 |
| `dyp-ask` | `project:investments/codex-skills/dyp-ask` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/dyp-ask` → `~/.local/share/agent-skills/references/dyp-ask` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `earnings-review` | `project:investments/codex-skills/earnings-review` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/earnings-review` → `~/.local/share/agent-skills/references/earnings-review` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `earnings-team` | `project:investments/codex-skills/earnings-team` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/earnings-team` → `~/.local/share/agent-skills/references/earnings-team` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `edit-article` | `project:presentations/.agents/skills/edit-article` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/edit-article` → `~/.local/share/agent-skills/references/edit-article` | 历史来源清单：WorkBuddy 内置 / 应用市场；inventory/skills/descriptions-zh.md 将其列为 WorkBuddy/平台内置；未将其改称独立 GitHub 上游。 |
| `eli5` | `project:presentations/.agents/skills/eli5` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/eli5` → `~/.local/share/agent-skills/references/eli5` | 历史来源清单：[github.com/companion-inc/feynman](https://github.com/companion-inc/feynman)；inventory/skills/descriptions-zh.md 记录 GitHub companion-inc/feynman。 |
| `financial-data` | `project:investments/codex-skills/financial-data` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/financial-data` → `~/.local/share/agent-skills/references/financial-data` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `frontend-design` | `project:presentations/.agents/skills/frontend-design` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/frontend-design` → `~/.local/share/agent-skills/references/frontend-design` | 历史来源清单：[github.com/anthropics/skills](https://github.com/anthropics/skills)；inventory/skills/descriptions-zh.md 记录 Anthropic 官方 skills 仓库。 |
| `git-guardrails-claude-code` | `~/.local/share/agent-skills/retired/20261016/git-guardrails-claude-code` | 已退役；完整备份移至 retired/20261016 | installed-snapshot: `~/.agents/skills/git-guardrails-claude-code` → `~/.local/share/agent-skills/references/git-guardrails-claude-code` | 原始上游未确证；不推断作者或仓库 |
| `grill-me` | `my-skills/grill-me` | 用户级（global） | installed-snapshot: `~/.agents/skills/grill-me` → `~/.local/share/agent-skills/references/grill-me` | 原始上游未确证；不推断作者或仓库 |
| `grill-with-docs` | `my-skills/grill-with-docs` | 用户级（global） | installed-snapshot: `~/.agents/skills/grill-with-docs` → `~/.local/share/agent-skills/references/grill-with-docs` | 原始上游未确证；不推断作者或仓库 |
| `grilling` | `my-skills/grilling` | 用户级（global） | installed-snapshot: `~/.agents/skills/grilling` → `~/.local/share/agent-skills/references/grilling` | 原始上游未确证；不推断作者或仓库 |
| `handoff` | `my-skills/handoff` | 用户级（global） | installed-snapshot: `~/.agents/skills/handoff` → `~/.local/share/agent-skills/references/handoff` | 旧来源表线索：[仓库/来源](https://github.com/mattpocock/skills)（历史归属，非作者结论） |
| `hatch-pet` | `project:presentations/.agents/skills/hatch-pet` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/hatch-pet` → `~/.local/share/agent-skills/references/hatch-pet` | 历史来源清单：[github.com/openai/skills](https://github.com/openai/skills)；inventory/skills/descriptions-zh.md 记录 OpenAI 官方 skills 仓库。 |
| `implement-spec` | `my-skills/implement-spec` | 用户级（global） | installed-snapshot: `~/.agents/skills/implement-spec` → `~/.local/share/agent-skills/references/implement-spec` | [登记来源链接](https://github.com/mattpocock/skills/tree/main/skills/engineering/implement-spec) |
| `improve-codebase-architecture` | `my-skills/improve-codebase-architecture` | 用户级（global） | installed-snapshot: `~/.agents/skills/improve-codebase-architecture` → `~/.local/share/agent-skills/references/improve-codebase-architecture` | 旧登记为第三方；具体上游未确证，不据此推断作者或原创来源。 |
| `income-investment` | `project:investments/codex-skills/income-investment` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/income-investment` → `~/.local/share/agent-skills/references/income-investment` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `industry-funnel` | `project:investments/codex-skills/industry-funnel` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/industry-funnel` → `~/.local/share/agent-skills/references/industry-funnel` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `industry-research` | `project:investments/codex-skills/industry-research` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/industry-research` → `~/.local/share/agent-skills/references/industry-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `investment-checklist` | `project:investments/codex-skills/investment-checklist` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/investment-checklist` → `~/.local/share/agent-skills/references/investment-checklist` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `investment-memo-craft` | `project:investments/codex-skills/investment-memo-craft` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/investment-memo-craft` → `~/.local/share/agent-skills/references/investment-memo-craft` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `investment-research` | `project:investments/codex-skills/investment-research` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/investment-research` → `~/.local/share/agent-skills/references/investment-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `investment-team` | `project:investments/codex-skills/investment-team` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/investment-team` → `~/.local/share/agent-skills/references/investment-team` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `lark-approval` | `my-skills/lark-approval` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-approval` → `~/.local/share/agent-skills/references/lark-approval` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-approval.tar.gz) |
| `lark-apps` | `my-skills/lark-apps` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-apps` → `~/.local/share/agent-skills/references/lark-apps` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-apps.tar.gz) |
| `lark-attendance` | `my-skills/lark-attendance` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-attendance` → `~/.local/share/agent-skills/references/lark-attendance` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-attendance.tar.gz) |
| `lark-base` | `my-skills/lark-base` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-base` → `~/.local/share/agent-skills/references/lark-base` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-base.tar.gz) |
| `lark-calendar` | `my-skills/lark-calendar` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-calendar` → `~/.local/share/agent-skills/references/lark-calendar` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-calendar.tar.gz) |
| `lark-contact` | `my-skills/lark-contact` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-contact` → `~/.local/share/agent-skills/references/lark-contact` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-contact.tar.gz) |
| `lark-doc` | `my-skills/lark-doc` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-doc` → `~/.local/share/agent-skills/references/lark-doc` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-doc.tar.gz) |
| `lark-drive` | `my-skills/lark-drive` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-drive` → `~/.local/share/agent-skills/references/lark-drive` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-drive.tar.gz) |
| `lark-event` | `my-skills/lark-event` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-event` → `~/.local/share/agent-skills/references/lark-event` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-event.tar.gz) |
| `lark-im` | `my-skills/lark-im` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-im` → `~/.local/share/agent-skills/references/lark-im` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-im.tar.gz) |
| `lark-mail` | `my-skills/lark-mail` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-mail` → `~/.local/share/agent-skills/references/lark-mail` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-mail.tar.gz) |
| `lark-markdown` | `my-skills/lark-markdown` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-markdown` → `~/.local/share/agent-skills/references/lark-markdown` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-markdown.tar.gz) |
| `lark-meeting` | `my-skills/lark-meeting` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-meeting` → `~/.local/share/agent-skills/references/lark-meeting` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-meeting.tar.gz) |
| `lark-minutes` | `my-skills/lark-minutes` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-minutes` → `~/.local/share/agent-skills/references/lark-minutes` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-minutes.tar.gz) |
| `lark-note` | `my-skills/lark-note` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-note` → `~/.local/share/agent-skills/references/lark-note` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-note.tar.gz) |
| `lark-okr` | `my-skills/lark-okr` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-okr` → `~/.local/share/agent-skills/references/lark-okr` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-okr.tar.gz) |
| `lark-openapi-explorer` | `my-skills/lark-openapi-explorer` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-openapi-explorer` → `~/.local/share/agent-skills/references/lark-openapi-explorer` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-openapi-explorer.tar.gz) |
| `lark-shared` | `my-skills/lark-shared` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-shared` → `~/.local/share/agent-skills/references/lark-shared` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-shared.tar.gz) |
| `lark-sheets` | `my-skills/lark-sheets` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-sheets` → `~/.local/share/agent-skills/references/lark-sheets` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-sheets.tar.gz) |
| `lark-skill-maker` | `my-skills/lark-skill-maker` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-skill-maker` → `~/.local/share/agent-skills/references/lark-skill-maker` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-skill-maker.tar.gz) |
| `lark-slides` | `my-skills/lark-slides` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-slides` → `~/.local/share/agent-skills/references/lark-slides` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-slides.tar.gz) |
| `lark-task` | `my-skills/lark-task` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-task` → `~/.local/share/agent-skills/references/lark-task` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-task.tar.gz) |
| `lark-vc` | `my-skills/lark-vc` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-vc` → `~/.local/share/agent-skills/references/lark-vc` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-vc.tar.gz) |
| `lark-vc-agent` | `my-skills/lark-vc-agent` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-vc-agent` → `~/.local/share/agent-skills/references/lark-vc-agent` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-vc-agent.tar.gz) |
| `lark-whiteboard` | `my-skills/lark-whiteboard` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-whiteboard` → `~/.local/share/agent-skills/references/lark-whiteboard` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-whiteboard.tar.gz) |
| `lark-wiki` | `my-skills/lark-wiki` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-wiki` → `~/.local/share/agent-skills/references/lark-wiki` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-wiki.tar.gz) |
| `lark-workflow-meeting-summary` | `my-skills/lark-workflow-meeting-summary` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-workflow-meeting-summary` → `~/.local/share/agent-skills/references/lark-workflow-meeting-summary` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-workflow-meeting-summary.tar.gz) |
| `lark-workflow-standup-report` | `my-skills/lark-workflow-standup-report` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-workflow-standup-report` → `~/.local/share/agent-skills/references/lark-workflow-standup-report` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-workflow-standup-report.tar.gz) |
| `llm-wiki-app` | `my-skills/llm-wiki-app` | 用户级（global） | installed-snapshot: `~/.agents/skills/llm-wiki-app` → `~/.local/share/agent-skills/references/llm-wiki-app` | 未确证独立上游；仓库登记与包内来源一致。 |
| `management-deep-dive` | `project:investments/codex-skills/management-deep-dive` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/management-deep-dive` → `~/.local/share/agent-skills/references/management-deep-dive` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `migrate-to-shoehorn` | `my-skills/migrate-to-shoehorn` | 用户级（global） | installed-snapshot: `~/.agents/skills/migrate-to-shoehorn` → `~/.local/share/agent-skills/references/migrate-to-shoehorn` | 未确证独立上游；不据此推断独立作者或 Git 仓库。 |
| `news-pulse` | `project:investments/codex-skills/news-pulse` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/news-pulse` → `~/.local/share/agent-skills/references/news-pulse` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `obsidian-vault` | `project:presentations/.agents/skills/obsidian-vault` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/obsidian-vault` → `~/.local/share/agent-skills/references/obsidian-vault` | 未确证独立上游；inventory/skills/descriptions-zh.md 将其列为 WorkBuddy/平台内置；未将其改称独立 GitHub 上游。 |
| `portfolio-review` | `project:investments/codex-skills/portfolio-review` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/portfolio-review` → `~/.local/share/agent-skills/references/portfolio-review` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `pr` | `my-skills/pr` | 用户级（global） | installed-snapshot: `~/.agents/skills/pr` → `~/.local/share/agent-skills/references/pr` | 历史上游线索：[mattpocock/skills · engineering/pr](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr)；可视化内容另注明 Dex Horthy / Humanlayer `show-me`，见 `my-skills/pr/CREDITS.md`。 |
| `private-company-research` | `project:investments/codex-skills/private-company-research` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/private-company-research` → `~/.local/share/agent-skills/references/private-company-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `prototype` | `my-skills/prototype` | 用户级（global） | installed-snapshot: `~/.agents/skills/prototype` → `~/.local/share/agent-skills/references/prototype` | 旧登记为第三方，但未找到可确认的上游或作者；第一方维护不等同于原创声明。 |
| `quality-screen` | `project:investments/codex-skills/quality-screen` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/quality-screen` → `~/.local/share/agent-skills/references/quality-screen` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `remotion-best-practices` | `project:presentations/.agents/skills/remotion-best-practices` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/remotion-best-practices` → `~/.local/share/agent-skills/references/remotion-best-practices` | 未确证独立上游；inventory/skills/descriptions-zh.md 将其列为 WorkBuddy/平台内置；未将其改称独立 GitHub 上游。 |
| `remotion-video-production` | `project:presentations/.agents/skills/remotion-video-production` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/remotion-video-production` → `~/.local/share/agent-skills/references/remotion-video-production` | 历史来源清单：[github.com/akillness/jeo-skills](https://github.com/akillness/jeo-skills)；inventory/skills/descriptions-zh.md 记录 akillness/jeo-skills；当前包作为兼容别名。 |
| `remotion-video-toolkit` | `project:presentations/.agents/skills/remotion-video-toolkit` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/remotion-video-toolkit` → `~/.local/share/agent-skills/references/remotion-video-toolkit` | 历史来源清单：[github.com/shreefentsar/remotion-video-toolkit](https://github.com/shreefentsar/remotion-video-toolkit)；inventory/skills/descriptions-zh.md 记录 shreefentsar/remotion-video-toolkit。 |
| `research` | `my-skills/research` | 用户级（global） | installed-snapshot: `~/.agents/skills/research` → `~/.local/share/agent-skills/references/research` | 原始上游未确证；不推断作者或仓库 |
| `retro` | `my-skills/retro` | 用户级（global） | installed-snapshot: `~/.agents/skills/retro` → `~/.local/share/agent-skills/references/retro` | 历史上游线索：[mattpocock/skills · engineering/retro](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro)；固定 commit 与获取日期未登记。 |
| `scaffold-exercises` | `my-skills/scaffold-exercises` | 用户级（global） | installed-snapshot: `~/.agents/skills/scaffold-exercises` → `~/.local/share/agent-skills/references/scaffold-exercises` | 未确证独立上游；不补造独立 GitHub 来源。 |
| `setup-matt-pocock-skills` | `my-skills/setup-matt-pocock-skills` | 用户级（global） | installed-snapshot: `~/.agents/skills/setup-matt-pocock-skills` → `~/.local/share/agent-skills/references/setup-matt-pocock-skills` | 原始上游未确证；不推断作者或仓库 |
| `setup-pre-commit` | `my-skills/setup-pre-commit` | 用户级（global） | installed-snapshot: `~/.agents/skills/setup-pre-commit` → `~/.local/share/agent-skills/references/setup-pre-commit` | 旧登记为第三方，但未找到可确认的上游或作者；不据此推断原创来源。 |
| `skill-workbench` | `my-skills/skill-workbench` | 用户级（global） | installed-snapshot: `~/.agents/skills/skill-creator` → `~/.local/share/agent-skills/references/skill-creator` | 原始上游未确证；不推断作者或仓库 |
| `storage-analyzer` | `my-skills/storage-analyzer` | 用户级（global） | installed-snapshot: `~/.agents/skills/storage-analyzer` → `~/.local/share/agent-skills/references/storage-analyzer` | 原始上游未确证；不推断作者或仓库 |
| `sts2-gawain-regression-recovery` | `project:gawain/skills/sts2-gawain-regression-recovery` | Gawain 项目（gawain） | installed-snapshot: `~/.agents/skills/sts2-gawain-regression-recovery` → `~/.local/share/agent-skills/references/sts2-gawain-regression-recovery` | 当前 Gawain 项目维护源已知；原作者与最初上游未确证 |
| `sts2-independent-run-regression` | `~/.local/share/agent-skills/retired/20261016/sts2-independent-run-regression` | 已退役；完整备份移至 retired/20261016 | installed-snapshot: `~/.agents/skills/sts2-independent-run-regression` → `~/.local/share/agent-skills/references/sts2-independent-run-regression` | 由本仓接管维护；原作者与最初上游未确证，不推断作者或仓库 |
| `sts2-start-game` | `my-skills/sts2-start-game` | 用户级（global） | installed-snapshot: `~/.agents/skills/sts2-start-game` → `~/.local/share/agent-skills/references/sts2-start-game` | 已知 Git 来源：`crystepj-max/STS2-AUTOTEST`；技能路径提交 `860ed5048ee4f4101046c213728bfdb618b4478d`，审计 HEAD `41f89387fa31d8208b277054828b6de00efe6eaf`。当前维护源从安装快照接管并保留其改进；该提交不代表安装版哈希或原创作者确证。 |
| `teach` | `my-skills/teach` | 用户级（global） | installed-snapshot: `~/.agents/skills/teach` → `~/.local/share/agent-skills/references/teach` | 未确证独立上游；来源为历史平台记录；没有独立上游仓库可确认。 |
| `test-report-html` | `多项目来源：project:gawain/.agents/skills/test-report-html；project:autotest/.agents/skills/test-report-html` | Gawain + AUTOTEST（gawain + autotest；一个登记名） | installed-snapshot: `~/.agents/skills/test-report-html` → `~/.local/share/agent-skills/references/test-report-html` | 未确证独立上游；维护 inventory 与当前 skill-lock 均未找到该项；未发现可证实来源，不虚构仓库。 |
| `thesis-drift` | `project:investments/codex-skills/thesis-drift` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/thesis-drift` → `~/.local/share/agent-skills/references/thesis-drift` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `thesis-tracker` | `project:investments/codex-skills/thesis-tracker` | ai-valueinvest 项目（investments） | installed-snapshot: `~/.agents/skills/thesis-tracker` → `~/.local/share/agent-skills/references/thesis-tracker` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `to-questionnaire` | `my-skills/to-questionnaire` | 用户级（global） | installed-snapshot: `~/.agents/skills/to-questionnaire` → `~/.local/share/agent-skills/references/to-questionnaire` | 原始上游未确证；不推断作者或仓库 |
| `triage` | `my-skills/triage` | 用户级（global） | installed-snapshot: `~/.agents/skills/triage` → `~/.local/share/agent-skills/references/triage` | 原始上游未确证；不推断作者或仓库 |
| `typesafe-ai` | `my-skills/typesafe-ai` | 用户级（global） | installed-snapshot: `~/.agents/skills/typesafe-ai` → `~/.local/share/agent-skills/references/typesafe-ai` | [登记来源链接](https://github.com/typesafe-ai/skills.git) |
| `video-production` | `project:presentations/.agents/skills/video-production` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/video-production` → `~/.local/share/agent-skills/references/video-production` | 历史来源清单：[github.com/jmagly/aiwg](https://github.com/jmagly/aiwg)；inventory/skills/descriptions-zh.md 记录 jmagly/aiwg。 |
| `wait-what` | `my-skills/wait-what` | 用户级（global） | installed-snapshot: `~/.agents/skills/wait-what` → `~/.local/share/agent-skills/references/wait-what` | 原始上游未确证；不推断作者或仓库 |
| `wayfinder` | `my-skills/wayfinder` | 用户级（global） | installed-snapshot: `~/.agents/skills/wayfinder` → `~/.local/share/agent-skills/references/wayfinder` | 原始上游未确证；不推断作者或仓库 |
| `wechat-article` | `project:presentations/.agents/skills/wechat-article` | Chris-Vault 项目（presentations） | installed-snapshot: `~/.agents/skills/wechat-article` → `~/.local/share/agent-skills/references/wechat-article` | 未确证独立上游；tools/add_repo_column.py 将其映射到 ai-berkshire 且该仓存在同名 canonical/generated 文件；inventory 行记“平台内置”。正文匹配度只作定位，报告保留该冲突。 |
| `wizard` | `my-skills/wizard` | 用户级（global） | installed-snapshot: `~/.agents/skills/wizard` → `~/.local/share/agent-skills/references/wizard` | 原始上游未确证；不推断作者或仓库 |
| `writing-great-skills` | `my-skills/writing-great-skills` | 用户级（global） | installed-snapshot: `~/.agents/skills/writing-great-skills` → `~/.local/share/agent-skills/references/writing-great-skills` | 未确证独立上游；证据支持“Matt Pocock/mattpocock/skills 为上游作者及技能来源，sickn33/agentic-awesome-skills 为目录/分发记录”并存。检查 ~/.agents/.skill-lock.json 未发现此技能的 lock 项，因此精确安装来源和安装 commit 未确证。 |
