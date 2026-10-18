# Skills 总览

> 本文件由 `scripts/build_skills_summary.py` 根据 `inventory/skill-policy.json` 生成，请勿手工编辑。
> 机器操作以 JSON 策略为准；中文描述、来源证据和重要修订分别维护在下列人读子表。

## 查阅入口

| 内容 | 文件 |
|---|---|
| 中文描述 | [skills/descriptions-zh.md](skills/descriptions-zh.md) |
| 作者、来源与上游版本 | [skills/provenance.md](skills/provenance.md) |
| 重要修订记录 | [skills/revision-history.md](skills/revision-history.md) |
| 机器登记与执行策略 | [skill-policy.json](skill-policy.json) |

## 登记概况

共 **143** 项：第一方维护 **128** 项，第三方来源 **15** 项。

| 状态 | 数量 |
|---|---:|
| 启用 | 122 |
| 迁移中 | 1 |
| 仅参考 | 12 |
| 已退役 | 8 |

| 使用范围 | 数量 |
|---|---:|
| `gawain` | 2 |
| `global` | 101 |
| `investments` | 20 |
| `presentations` | 20 |

## Skills 总表

来源列展示当前正式维护/保留路径；它不单独证明最初作者或原创性。来源细节及证据见来源子表。

| Skill | 归属 | 状态 | 范围 | 正式来源/维护源 | 描述 | 来源档案 |
|---|---|---|---|---|---|---|
| `agent-cli-tool-residue-purge` | 第一方维护 | 启用 | `global` | `my-skills/agent-cli-tool-residue-purge` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `agent-skill-bridge` | 第一方维护 | 启用 | `global` | `my-skills/agent-skill-bridge` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `agnes-ai-generation-skill` | 第一方维护 | 已退役 | `global` | `~/.local/share/agent-skills/retired/20261016/agnes-ai-generation-skill` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `ask-matt` | 第一方维护 | 启用 | `global` | `my-skills/ask-matt` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `baoyu-comic` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/baoyu-comic` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `baoyu-image-gen` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/baoyu-image-gen` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `baoyu-infographic` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/baoyu-infographic` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `baoyu-slide-deck` | 第三方来源 | 仅参考 | `presentations` | `project:presentations/.agent-assets/presentations/baoyu-slide-deck` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `beautiful-html-templates` | 第三方来源 | 仅参考 | `presentations` | `project:presentations/.agent-assets/presentations/beautiful-html-templates` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `bottleneck-hunter` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/bottleneck-hunter` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `chatgpt-web-bridge` | 第一方维护 | 启用 | `global` | `my-skills/chatgpt-web-bridge` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `clashx-openai-sse-debug` | 第一方维护 | 启用 | `global` | `my-skills/clashx-openai-sse-debug` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `cnb-git` | 第一方维护 | 启用 | `global` | `my-skills/cnb-git` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `cnb-push` | 第一方维护 | 启用 | `global` | `my-skills/cnb-push` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `code-review` | 第一方维护 | 启用 | `global` | `my-skills/code-review` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `codebase-design` | 第一方维护 | 启用 | `global` | `my-skills/codebase-design` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `codex-bridge-chatgpt` | 第三方来源 | 迁移中 | `global` | `~/.agents/skills/codex-bridge-chatgpt` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `construction-bootstrap` | 第一方维护 | 已退役 | `global` | `~/.local/share/agent-skills/retired/construction-bootstrap` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `cross-domain-borrowing` | 第一方维护 | 启用 | `global` | `my-skills/cross-domain-borrowing` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `deep-company-series` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/deep-company-series` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `dev-workflow-2-0` | 第一方维护 | 已退役 | `global` | `~/.local/share/agent-skills/retired/dev-workflow-2-0` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `diagnosing-bugs` | 第三方来源 | 仅参考 | `global` | `~/.local/share/agent-skills/references/diagnosing-bugs` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `domain-modeling` | 第一方维护 | 启用 | `global` | `my-skills/domain-modeling` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `dsh-source-upgrade` | 第一方维护 | 启用 | `global` | `my-skills/dsh-source-upgrade` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `dsh-web-access-recovery` | 第一方维护 | 启用 | `global` | `my-skills/dsh-web-access-recovery` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `duplicate-cli-unify` | 第一方维护 | 启用 | `global` | `my-skills/duplicate-cli-unify` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `dyp-ask` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/dyp-ask` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `earnings-review` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/earnings-review` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `earnings-team` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/earnings-team` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `edit-article` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/edit-article` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `eli5` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/eli5` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `execution-plan` | 第一方维护 | 已退役 | `global` | `~/.local/share/agent-skills/retired/execution-plan` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `expert-consultation` | 第一方维护 | 启用 | `global` | `my-skills/expert-consultation` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `fact-check` | 第一方维护 | 启用 | `global` | `my-skills/fact-check` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `financial-data` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/financial-data` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `find-skills` | 第三方来源 | 仅参考 | `global` | `~/.local/share/agent-skills/reference/find-skills` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `first-principle` | 第一方维护 | 启用 | `global` | `my-skills/first-principle` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `frontend-design` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/frontend-design` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `frontend-slides` | 第三方来源 | 仅参考 | `presentations` | `project:presentations/.agent-assets/presentations/frontend-slides` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `git-guardrails-claude-code` | 第一方维护 | 已退役 | `global` | `~/.local/share/agent-skills/retired/20261016/git-guardrails-claude-code` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `grill-me` | 第一方维护 | 启用 | `global` | `my-skills/grill-me` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `grill-with-docs` | 第一方维护 | 启用 | `global` | `my-skills/grill-with-docs` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `grilling` | 第一方维护 | 启用 | `global` | `my-skills/grilling` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `guizang-ppt-skill` | 第三方来源 | 仅参考 | `presentations` | `project:presentations/.agent-assets/presentations/guizang-ppt-skill` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `handoff` | 第一方维护 | 启用 | `global` | `my-skills/handoff` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `hatch-pet` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/hatch-pet` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `humanize-ppt` | 第三方来源 | 仅参考 | `presentations` | `project:presentations/.agent-assets/presentations/humanize-ppt` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `implement` | 第三方来源 | 仅参考 | `global` | `~/.local/share/agent-skills/reference/implement` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `implement-spec` | 第一方维护 | 启用 | `global` | `my-skills/implement-spec` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `improve-codebase-architecture` | 第一方维护 | 启用 | `global` | `my-skills/improve-codebase-architecture` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `income-investment` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/income-investment` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `industry-funnel` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/industry-funnel` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `industry-research` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/industry-research` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `investment-checklist` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/investment-checklist` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `investment-memo-craft` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/investment-memo-craft` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `investment-research` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/investment-research` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `investment-team` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/investment-team` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-approval` | 第一方维护 | 启用 | `global` | `my-skills/lark-approval` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-apps` | 第一方维护 | 启用 | `global` | `my-skills/lark-apps` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-attendance` | 第一方维护 | 启用 | `global` | `my-skills/lark-attendance` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-base` | 第一方维护 | 启用 | `global` | `my-skills/lark-base` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-calendar` | 第一方维护 | 启用 | `global` | `my-skills/lark-calendar` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-contact` | 第一方维护 | 启用 | `global` | `my-skills/lark-contact` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-doc` | 第一方维护 | 启用 | `global` | `my-skills/lark-doc` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-drive` | 第一方维护 | 启用 | `global` | `my-skills/lark-drive` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-event` | 第一方维护 | 启用 | `global` | `my-skills/lark-event` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-im` | 第一方维护 | 启用 | `global` | `my-skills/lark-im` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-mail` | 第一方维护 | 启用 | `global` | `my-skills/lark-mail` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-markdown` | 第一方维护 | 启用 | `global` | `my-skills/lark-markdown` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-meeting` | 第一方维护 | 启用 | `global` | `my-skills/lark-meeting` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-minutes` | 第一方维护 | 启用 | `global` | `my-skills/lark-minutes` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-note` | 第一方维护 | 启用 | `global` | `my-skills/lark-note` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-okr` | 第一方维护 | 启用 | `global` | `my-skills/lark-okr` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-openapi-explorer` | 第一方维护 | 启用 | `global` | `my-skills/lark-openapi-explorer` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-shared` | 第一方维护 | 启用 | `global` | `my-skills/lark-shared` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-sheets` | 第一方维护 | 启用 | `global` | `my-skills/lark-sheets` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-skill-maker` | 第一方维护 | 启用 | `global` | `my-skills/lark-skill-maker` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-slides` | 第一方维护 | 启用 | `global` | `my-skills/lark-slides` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-task` | 第一方维护 | 启用 | `global` | `my-skills/lark-task` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-vc` | 第一方维护 | 启用 | `global` | `my-skills/lark-vc` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-vc-agent` | 第一方维护 | 启用 | `global` | `my-skills/lark-vc-agent` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-whiteboard` | 第一方维护 | 启用 | `global` | `my-skills/lark-whiteboard` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-wiki` | 第一方维护 | 启用 | `global` | `my-skills/lark-wiki` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-workflow-meeting-summary` | 第一方维护 | 启用 | `global` | `my-skills/lark-workflow-meeting-summary` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `lark-workflow-standup-report` | 第一方维护 | 启用 | `global` | `my-skills/lark-workflow-standup-report` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `learn_something_new` | 第一方维护 | 启用 | `global` | `my-skills/learn_something_new` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `life-design` | 第一方维护 | 启用 | `global` | `my-skills/life-design` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `llm-wiki-app` | 第一方维护 | 启用 | `global` | `my-skills/llm-wiki-app` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `management-deep-dive` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/management-deep-dive` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `migrate-to-shoehorn` | 第一方维护 | 启用 | `global` | `my-skills/migrate-to-shoehorn` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `minimum-scale-experiment` | 第一方维护 | 启用 | `global` | `my-skills/minimum-scale-experiment` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `neat-freak` | 第一方维护 | 启用 | `global` | `my-skills/neat-freak` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `news-pulse` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/news-pulse` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `obsidian-vault` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/obsidian-vault` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `portfolio-review` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/portfolio-review` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `ppt-master` | 第三方来源 | 仅参考 | `presentations` | `project:presentations/.agent-assets/presentations/ppt-master` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `pr` | 第一方维护 | 启用 | `global` | `my-skills/pr` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `presentation-production` | 第一方维护 | 启用 | `presentations` | `my-skills/presentation-production` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `private-company-research` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/private-company-research` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `prototype` | 第一方维护 | 启用 | `global` | `my-skills/prototype` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `quality-screen` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/quality-screen` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `remotion-best-practices` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/remotion-best-practices` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `remotion-video-production` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/remotion-video-production` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `remotion-video-toolkit` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/remotion-video-toolkit` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `requirements-analysis.bak-20260905-224705` | 第三方来源 | 已退役 | `global` | `~/.local/share/agent-skills/retired/requirements-analysis.bak-20260905-224705` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `research` | 第一方维护 | 启用 | `global` | `my-skills/research` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `research-report-generator` | 第一方维护 | 启用 | `global` | `my-skills/research-report-generator` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `resolving-merge-conflicts` | 第三方来源 | 已退役 | `global` | `~/.local/share/agent-skills/retired/resolving-merge-conflicts` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `retro` | 第一方维护 | 启用 | `global` | `my-skills/retro` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `scaffold-exercises` | 第一方维护 | 启用 | `global` | `my-skills/scaffold-exercises` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `setup-matt-pocock-skills` | 第一方维护 | 启用 | `global` | `my-skills/setup-matt-pocock-skills` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `setup-pre-commit` | 第一方维护 | 启用 | `global` | `my-skills/setup-pre-commit` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `skill-creator` | 第三方来源 | 仅参考 | `global` | `~/.local/share/agent-skills/references/skill-creator` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `skill-workbench` | 第一方维护 | 启用 | `global` | `my-skills/skill-workbench` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `skills-security-check` | 第一方维护 | 启用 | `global` | `my-skills/skills-security-check` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `socratic-clarify` | 第一方维护 | 启用 | `global` | `my-skills/socratic-clarify` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `steelmanning` | 第一方维护 | 启用 | `global` | `my-skills/steelmanning` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `storage-analyzer` | 第一方维护 | 启用 | `global` | `my-skills/storage-analyzer` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `sts2-gawain-regression-recovery` | 第一方维护 | 启用 | `gawain` | `project:gawain/skills/sts2-gawain-regression-recovery` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `sts2-independent-run-regression` | 第一方维护 | 已退役 | `global` | `~/.local/share/agent-skills/retired/20261016/sts2-independent-run-regression` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `sts2-start-game` | 第一方维护 | 启用 | `global` | `my-skills/sts2-start-game` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `tdd` | 第一方维护 | 启用 | `global` | `my-skills/tdd` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `teach` | 第一方维护 | 启用 | `global` | `my-skills/teach` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `test-report-html` | 第一方维护 | 启用 | `gawain` | `project:gawain/.agents/skills/test-report-html` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `thesis-drift` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/thesis-drift` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `thesis-tracker` | 第一方维护 | 启用 | `investments` | `project:investments/codex-skills/thesis-tracker` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `to-questionnaire` | 第一方维护 | 启用 | `global` | `my-skills/to-questionnaire` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `to-spec` | 第三方来源 | 仅参考 | `global` | `~/.local/share/agent-skills/reference/to-spec` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `to-tickets` | 第三方来源 | 仅参考 | `global` | `~/.local/share/agent-skills/reference/to-tickets` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `triage` | 第一方维护 | 启用 | `global` | `my-skills/triage` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `typesafe-ai` | 第一方维护 | 启用 | `global` | `my-skills/typesafe-ai` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `uncover-hidden-talents` | 第一方维护 | 启用 | `global` | `my-skills/uncover-hidden-talents` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `video-production` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/video-production` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `wait-what` | 第一方维护 | 启用 | `global` | `my-skills/wait-what` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `wayfinder` | 第一方维护 | 启用 | `global` | `my-skills/wayfinder` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `wechat-article` | 第一方维护 | 启用 | `presentations` | `project:presentations/.agents/skills/wechat-article` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `wf-construction-full-feature` | 第一方维护 | 启用 | `global` | `~/.agents/skills/wf-construction-full-feature` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `wf-diagnose` | 第一方维护 | 启用 | `global` | `~/.agents/skills/wf-diagnose` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `wf-explore` | 第一方维护 | 启用 | `global` | `~/.agents/skills/wf-explore` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `wf-optimize` | 第一方维护 | 启用 | `global` | `~/.agents/skills/wf-optimize` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `wizard` | 第一方维护 | 启用 | `global` | `my-skills/wizard` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `workspace-convergence-audit` | 第一方维护 | 启用 | `global` | `my-skills/workspace-convergence-audit` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
| `writing-great-skills` | 第一方维护 | 启用 | `global` | `my-skills/writing-great-skills` | [描述](skills/descriptions-zh.md) | [来源](skills/provenance.md) |
