# Skills 重要修订记录

本表汇总有证据可查的项目结构调整和主要 Skill 更新，按日期倒序排列，最新记录在最上方。它是里程碑摘要，不替代各维护源的完整 Git 历史；每条尽量附上提交号或当时的登记记录。

| 日期 | 项目结构与治理 | Skill 修订/迁移 | 依据/证据 |
|---|---|---|---|
| 2026-10-18 | 新增 1 项 `first-party/global/active` 登记；策略合计 143 项、第一方维护 128 项，`reference_copies` 仍为 105 条，人读总表按脚本重新生成。 | 入池 `research-report-generator`：按五条铁律输出 8 章节用户调研报告并套用内置 HTML 模板；纯 prompt 与模板资产，无脚本、网络与凭据依赖。 | `a0f9721`（CNB 合并请求 #3）；本地按仓库算法复核指纹 `51275c7e…` 与目录内容一致。 |
| 2026-10-17 | 将此前暂缓的 5 项登记为 `first-party/global/active`，并为每项保留一份带指纹的原版只读 reference；维护源与旧参考分开恢复。 | 修订并纳入 `improve-codebase-architecture`、`prototype`、`pr`、`retro`、`setup-pre-commit` 五个完整包；架构审阅默认给出有证据的设计建议，仅按明确实施请求进入实现。 | 五项维护源、原版 SHA-256 与本轮策略/来源记录；四项已审阅提交 `af24122`、`4acfdfa`、`02ef22c`、`651f9ac`。 |
| 2026-10-17 | 人读目录重整：总表改名为 `skills-summary.md`；中文描述、来源档案、重要修订拆到 `inventory/skills/`，总表从机器 JSON 生成。 | 来源登记版式优化，并补录此前可查的结构与 Skill 更新里程碑。 | 本轮目录与文档修订 |
| 2026-10-16 | 扩大项目级维护范围，登记演示、金融、Gawain/AUTOTEST 来源并保留原件参考；3 项退役、5 项本机待讨论技能留在发布范围之外。 | 内化及调整多项第一方 Skill；新增 `chatgpt-web-bridge`；13 项演示技能与 20 项金融技能迁入各自项目范围，`test-report-html` 同时映射到 Gawain 与 AUTOTEST。 | `0719846`、`498e011`、`5d1df54` |
| 2026-10-15 | 细化第一方 Skill 治理规则和定点修正。 | 修订 `agent-skill-bridge`、`leader` 及多项第一方 Skills；新增 DSH 升级/访问恢复和工作区收敛能力。 | `4dd008c`、`dd01b57` |
| 2026-10-10 | 明确跨项目工作流的维护职责。 | `requirements-analysis` 改由 workflow-manager 维护并直接分发；本仓保留历史副本，不再作为其维护源。 | `a37d22a` |
| 2026-10-08 | 将项目技能与全局技能分开管理。 | `execution-plan` 改为 dev-flow 项目级技能，旧用户级副本退出公共入口并保留。 | `inventory/skills/descriptions-zh.md` 历史更新记录 |
| 2026-10-06 | 继续登记上游新增与退役状态。 | 引入 `implement-spec`、`retro`、`pr`；退役上游已移除的 `resolving-merge-conflicts`；`ppt-master` 从 v4.5.0 升至 v6.6.0。 | `f3a3f85`；旧版本更新记录 |
| 2026-10-05 | 修复技能中文守护与管理命令的错误判定。 | 9 项 Matt Pocock 技能和 `neat-freak` 对齐上游；`agent-skill-bridge` 的中文守护从误报通过改为校验退出码。 | `0f85a8b`、`6eb259d` |
| 2026-10-04 | 修复 Windows 目录联接入口检查。 | 新增第三方 `typesafe-ai`，经安全审计后纳入。 | `7543393`；旧版本更新记录 |
| 2026-09-21 | 清单继续记录上游对齐与来源变化。 | 对齐第三方上游、恢复中文描述，并移除 `claude-handoff`。 | `4ff1ac7` |
| 2026-09-16 | 继续按项目责任维护技能。 | 新增 `cnb-git`、`cnb-push`，并迭代 `execution-plan`、`requirements-analysis`。 | `3037869` |
| 2026-09-14–15 | 按生命周期和责任拆分项目/用户级技能；登记 `wf-*` 生成技能。 | 退役 `construction-bootstrap`、`dev-workflow-2-0`；将 `diagnosing-bugs` 调整为参考项，由 `wf-diagnose` 承接诊断职责。 | `010c0d4`、`2299c96`；旧版本更新记录 |
| 2026-09-09 | 建立声明式 `skill-policy.json`、管理脚本和人读生命周期表，作为技能入口管理基础。 | 同批补齐 5 个第一方 Skill，并调整 `agent-skill-bridge` 的管理职责。 | `b6933e4` |
| 2026-09-06 | 人工清单拆成第一方、第三方、参考三块，并增加范围列和 PPT 项目级标记；加固刷新脚本以保护排版。 | 分类与范围信息开始在表格中显式呈现。 | `6e3f5ad`、`b2bed7a` |
| 2026-09-05 | 尚未引入统一机器策略。 | `requirements-analysis` 调整为产出“已定义”任务的需求定义 Skill。 | `52e63c5` |
| 2026-09-04 | 同步自有 Skill 与清单。 | 多项自有 Skill 内容更新。 | `29cc3e9` |
| 2026-08-25 | 重新梳理第三方 Skill 清单。 | 更新自有 Skill，并核对第三方技能及来源。 | `88f8b9f` |
| 2026-08-24 | 补充并核对第三方来源记录。 | 新增 `eli5`、`video-production`、`remotion-video-production`、`to-questionnaire`、`wait-what`、`wizard`；校正多项来源归属，并移除 4 项 STS2 项目技能记录。 | `53e77a7`；当期中文描述表更新记录 |
| 2026-08-18–22 | 继续按技能职责调整维护内容。 | 更新 `requirements-analysis`、`dev-workflow-2-0` 和 `agent-skill-bridge`。 | [中文描述表历史更新记录](descriptions-zh.md) |
| 2026-08-15 | 清单继续以同步快照维护。 | 更新自有 Skill 与清单。 | `655a038` |
| 2026-08-13 | 延续集中清单与技能同步，形成多次分批修订。 | 更新当时的自有 Skill 与公共池内容。 | `a8192d8`、`8d19794`、`6923bdf`、`bc5cac9`、`9b1943e` |
| 2026-08-12 | 建立集中管理自有 Skills 与公共 Skills 清单。 | 开始集中维护自有 Skill 和共享技能来源/更新时间信息。 | `a00458c` |

## 记录约定

- 记录来源确认/更正、参考版本更新、生命周期或维护源变更，以及明显改变使用流程的修订。
- 按项目级重要里程碑记录，不要求把每次小改动都复制到本表；完整细节以对应技能维护仓库的 Git 历史为准。
- “创建日期”与“首次纳入当前仓库”分开记录；Git 首次提交只证明入档时间。
- 未有证据的日期标为“未记录”，不根据文件时间戳或推测补齐。
- 子表链接指向相应技能目录或提交；未完成的核实注明状态和缺少的证据。
