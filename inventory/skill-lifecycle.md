# 技能生命周期

本表由 skill-policy.json 生成；状态与范围决定实际入口，第三方来源说明另见 skill-desc-translation.md。

| 技能 | 状态 | 范围 | 正式来源 |
|---|---|---|---|
| agent-cli-tool-residue-purge | transition | global | `~/.agents/skills/agent-cli-tool-residue-purge` |
| agent-skill-bridge | active | global | `my-skills/agent-skill-bridge` |
| agnes-ai-generation-skill | transition | global | `~/.agents/skills/agnes-ai-generation-skill` |
| ask-matt | transition | global | `~/.agents/skills/ask-matt` |
| baoyu-comic | transition | global | `~/.agents/skills/baoyu-comic` |
| baoyu-image-gen | transition | global | `~/.agents/skills/baoyu-image-gen` |
| baoyu-infographic | transition | global | `~/.agents/skills/baoyu-infographic` |
| baoyu-slide-deck | reference | presentations | `project:presentations/.agent-assets/presentations/baoyu-slide-deck` |
| beautiful-html-templates | reference | presentations | `project:presentations/.agent-assets/presentations/beautiful-html-templates` |
| bottleneck-hunter | transition | global | `~/.agents/skills/bottleneck-hunter` |
| clashx-openai-sse-debug | transition | global | `~/.agents/skills/clashx-openai-sse-debug` |
| cnb-git | active | global | `my-skills/cnb-git`（说明：按实际 upstream remote 与服务端分支执行 fetch/pull；凭据仅注入 CNB URL；不自动删 Git lock，clone/fetch/pull 错误明确失败。） |
| cnb-push | active | global | `my-skills/cnb-push`（说明：CNB 推送封装；区分现有仓更新与首次上传，--all/--set-default 按其实际影响范围授权并复用既有授权。） |
| code-review | transition | global | `~/.agents/skills/code-review` |
| codebase-design | transition | global | `~/.agents/skills/codebase-design` |
| construction-bootstrap | retired | global | `~/.local/share/agent-skills/retired/construction-bootstrap` |
| cross-domain-borrowing | active | global | `my-skills/cross-domain-borrowing` |
| deep-company-series | transition | global | `~/.agents/skills/deep-company-series` |
| dev-workflow-2-0 | retired | global | `~/.local/share/agent-skills/retired/dev-workflow-2-0` |
| diagnosing-bugs | reference | global | `~/.local/share/agent-skills/references/diagnosing-bugs` |
| domain-modeling | transition | global | `~/.agents/skills/domain-modeling` |
| dsh-source-upgrade | active | global | `my-skills/dsh-source-upgrade`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/dsh-source-upgrade） |
| dsh-web-access-recovery | active | global | `my-skills/dsh-web-access-recovery`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/dsh-web-access-recovery） |
| duplicate-cli-unify | transition | global | `~/.agents/skills/duplicate-cli-unify` |
| dyp-ask | transition | global | `~/.agents/skills/dyp-ask` |
| earnings-review | transition | global | `~/.agents/skills/earnings-review` |
| earnings-team | transition | global | `~/.agents/skills/earnings-team` |
| edit-article | transition | global | `~/.agents/skills/edit-article` |
| eli5 | transition | global | `~/.agents/skills/eli5` |
| execution-plan | retired | global | `~/.local/share/agent-skills/retired/execution-plan`（历史副本保留；正式入口为 dev-flow 项目级技能） |
| expert-consultation | active | global | `my-skills/expert-consultation` |
| fact-check | active | global | `my-skills/fact-check` |
| financial-data | transition | global | `~/.agents/skills/financial-data` |
| find-skills | reference | global | `~/.local/share/agent-skills/reference/find-skills` |
| first-principle | active | global | `my-skills/first-principle` |
| frontend-design | transition | global | `~/.agents/skills/frontend-design` |
| frontend-slides | reference | presentations | `project:presentations/.agent-assets/presentations/frontend-slides` |
| git-guardrails-claude-code | transition | global | `~/.agents/skills/git-guardrails-claude-code` |
| grill-me | transition | global | `~/.agents/skills/grill-me` |
| grill-with-docs | transition | global | `~/.agents/skills/grill-with-docs` |
| grilling | transition | global | `~/.agents/skills/grilling` |
| guizang-ppt-skill | reference | presentations | `project:presentations/.agent-assets/presentations/guizang-ppt-skill` |
| handoff | active | global | `~/.agents/skills/handoff` |
| hatch-pet | transition | global | `~/.agents/skills/hatch-pet` |
| humanize-ppt | reference | presentations | `project:presentations/.agent-assets/presentations/humanize-ppt` |
| implement | reference | global | `~/.local/share/agent-skills/reference/implement` |
| improve-codebase-architecture | transition | global | `~/.agents/skills/improve-codebase-architecture` |
| income-investment | transition | global | `~/.agents/skills/income-investment` |
| industry-funnel | transition | global | `~/.agents/skills/industry-funnel` |
| industry-research | transition | global | `~/.agents/skills/industry-research` |
| investment-checklist | transition | global | `~/.agents/skills/investment-checklist` |
| investment-memo-craft | transition | global | `~/.agents/skills/investment-memo-craft` |
| investment-research | transition | global | `~/.agents/skills/investment-research` |
| investment-team | transition | global | `~/.agents/skills/investment-team` |
| learn_something_new | active | global | `my-skills/learn_something_new` |
| life-design | active | global | `my-skills/life-design` |
| llm-wiki-app | transition | global | `~/.agents/skills/llm-wiki-app` |
| management-deep-dive | transition | global | `~/.agents/skills/management-deep-dive` |
| migrate-to-shoehorn | transition | global | `~/.agents/skills/migrate-to-shoehorn` |
| minimum-scale-experiment | active | global | `my-skills/minimum-scale-experiment` |
| neat-freak | active | global | `my-skills/neat-freak` |
| news-pulse | transition | global | `~/.agents/skills/news-pulse` |
| obsidian-vault | transition | global | `~/.agents/skills/obsidian-vault` |
| portfolio-review | transition | global | `~/.agents/skills/portfolio-review` |
| ppt-master | reference | presentations | `project:presentations/.agent-assets/presentations/ppt-master` |
| presentation-production | active | presentations | `my-skills/presentation-production` |
| private-company-research | transition | global | `~/.agents/skills/private-company-research` |
| prototype | transition | global | `~/.agents/skills/prototype` |
| quality-screen | transition | global | `~/.agents/skills/quality-screen` |
| remotion-best-practices | transition | global | `~/.agents/skills/remotion-best-practices` |
| remotion-video-production | transition | global | `~/.agents/skills/remotion-video-production` |
| remotion-video-toolkit | transition | global | `~/.agents/skills/remotion-video-toolkit` |
| requirements-analysis.bak-20260905-224705 | retired | global | `~/.local/share/agent-skills/retired/requirements-analysis.bak-20260905-224705` |
| research | transition | global | `~/.agents/skills/research` |
| resolving-merge-conflicts | transition | global | `~/.agents/skills/resolving-merge-conflicts` |
| scaffold-exercises | transition | global | `~/.agents/skills/scaffold-exercises` |
| setup-matt-pocock-skills | transition | global | `~/.agents/skills/setup-matt-pocock-skills` |
| setup-pre-commit | transition | global | `~/.agents/skills/setup-pre-commit` |
| skill-creator | transition | global | `~/.agents/skills/skill-creator` |
| skills-security-check | active | global | `my-skills/skills-security-check` |
| socratic-clarify | active | global | `my-skills/socratic-clarify` |
| steelmanning | active | global | `my-skills/steelmanning` |
| storage-analyzer | transition | global | `~/.agents/skills/storage-analyzer` |
| sts2-gawain-regression-recovery | transition | global | `~/.agents/skills/sts2-gawain-regression-recovery` |
| sts2-independent-run-regression | transition | global | `~/.agents/skills/sts2-independent-run-regression` |
| sts2-start-game | transition | global | `~/.agents/skills/sts2-start-game` |
| tdd | active | global | `my-skills/tdd` |
| teach | transition | global | `~/.agents/skills/teach` |
| test-report-html | transition | global | `~/.agents/skills/test-report-html` |
| thesis-drift | transition | global | `~/.agents/skills/thesis-drift` |
| thesis-tracker | transition | global | `~/.agents/skills/thesis-tracker` |
| to-questionnaire | transition | global | `~/.agents/skills/to-questionnaire` |
| to-spec | reference | global | `~/.local/share/agent-skills/reference/to-spec` |
| to-tickets | reference | global | `~/.local/share/agent-skills/reference/to-tickets` |
| triage | transition | global | `~/.agents/skills/triage` |
| typesafe-ai | transition | global | `~/.agents/skills/typesafe-ai` |
| uncover-hidden-talents | active | global | `my-skills/uncover-hidden-talents` |
| video-production | transition | global | `~/.agents/skills/video-production` |
| wait-what | transition | global | `~/.agents/skills/wait-what` |
| wayfinder | transition | global | `~/.agents/skills/wayfinder` |
| wechat-article | transition | global | `~/.agents/skills/wechat-article` |
| wf-construction-full-feature | active | global | `~/.agents/skills/wf-construction-full-feature` |
| wf-diagnose | active | global | `~/.agents/skills/wf-diagnose` |
| wf-explore | active | global | `~/.agents/skills/wf-explore` |
| wf-optimize | active | global | `~/.agents/skills/wf-optimize` |
| wizard | transition | global | `~/.agents/skills/wizard` |
| workspace-convergence-audit | active | global | `my-skills/workspace-convergence-audit`（说明：本仓按用户决定承担当前维护；原作者与最初来源未证实，完整原件保存在 /Users/chris/Documents/Codex/2026-10-13/user-skills-instruction-review/optimization-handoff/first-party-backup/workspace-convergence-audit） |
| writing-great-skills | transition | global | `~/.agents/skills/writing-great-skills` |
