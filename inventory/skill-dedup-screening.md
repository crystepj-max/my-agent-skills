# 开发工作流 Skill 去重筛选表

> ⚠️ **架构更正（2026-09-15）**：本表撰写于 09-09 重构之前。该重构引入了 `inventory/skill-policy.json` 作为**技能范围的唯一登记表**（`skill-lifecycle.md` 与 `skill-desc-translation.md` 均由其派生），并把 `tools/install_all_skills.sh` 降级为兼容 shim（真实实现迁到 `scripts/restore.sh` → `manage-skills.py`）。因此：
> - **§7 的排除清单机制已作废** —— 新架构下 `skill-policy.json` 本身就是安装范围与排除机制，`skill-exclusions.txt` 不再需要，本 PR 也未包含它。
> - 退役的正确做法见 `my-skills/agent-skill-bridge/SKILL.md` 的「语义重复：不同名同物」一节：先确认承接方已登记 → 旧版置 `retired` → 目录移出发现目录 → 同步派生文档。
> - D-1 已按新架构执行完毕（见下方执行记录）；D-2/D-3/D-4 的筛选结论仍待你填写。

> 生成：2026-09-14 ｜ 范围：用户级 skill 及其真实来源
> 扫描方式：**全程只读** —— 目录列举 + frontmatter 描述导出 + SKILL.md 内容指纹比对 + 全仓引用 grep。未修改/删除任何 skill 文件。
> 用法：在「你的决定」列直接填写（如 `删` / `留` / `待议`）。未填一律视为「不动」。填完交回，我按表执行（执行前会先生成整目录备份并列出全部受影响路径）。

---

## 0. 池子结构与落点

> ⚠️ **扫描范围 = Windows 机器**（`D:\workspace\my-agent-skills` + `C:\Users\22487\...`）。本表所有计数与池内判断均来自该机器。
> 仓库内两份历史文档是 **Mac 快照**，不可与本表计数直接比较：`docs/diagnostic-deepseek-harness-skill-discovery.md` 明写「dsh 现运行于本机 Mac mini」（2026-08-25）；`inventory/skill-desc-translation.md`（2026-08-24）的第一方板块含 `clashx-openai-sse-debug` 等 macOS 专有项，同为 Mac 侧认知。
> **跨机器后果**：仓库经 GitHub 同步后，Mac 侧的 `my-skills/construction-bootstrap` 会随之消失，其 4 处软链将变成悬空软链，需在 Mac 上单独清理（见 §8）。

| 池 | 路径 | 性质 | git 可回滚 |
|---|---|---|---|
| 公共池 | `C:\Users\22487\.agents\skills\` | 第三方 skill 真实目录 + 第一方 skill 的软链 | 否 |
| WorkBuddy 池 | `C:\Users\22487\.workbuddy\skills\` | 几乎全为软链；唯一真实目录是 `workbuddy-bash-toolchain-fix` | 否 |
| 第一方真源 | `D:\workspace\my-agent-skills\my-skills\` | 16 个目录，git 管理 | 是 |
| 生成物来源 | workflow-manager 蓝图 `templates/*.json` | `wf-*` 由生成器编译，skill 内声明「生成物不可手改，改蓝图重生成」 | 否（在另一仓） |

关键含义：**第一方 skill 的删除可用 git 回滚；第三方与 `wf-*` 的删除不可回滚**，只能靠重装或从上游重取。

---

## 1. 核心交付链明细（7 个）

| # | Skill | 环节 | 形态 | 落点 | 引用/依赖 | 建议 | 你的决定 |
|---|---|---|---|---|---|---|---|
| 1 | `requirements-analysis` | M1 需求定义 | 第一方 | `my-skills/` | `ai-task-skill-set/README.md`、`public-task-contract.md:198` 称其为「唯一入口」；被 D-5 中的 triage/wayfinder 部分重叠 | 留 | |
| 2 | `construction-bootstrap` | M2 建设·完整功能开发 | 第一方 **shim** | ~~`my-skills/`~~ | `ai-task-skill-set/README.md:8`；自身 `SKILL.md:22`、`shim-map.md:15,20` | **已删除（D-1，2026-09-14）** | 删 |
| 3 | `execution-plan` | M3 批量调度 | 第一方 | `my-skills/` | 依赖 workflow-manager 的 `scripts/ai-task-execution-plan.mjs` | 留 | |
| 4 | `wf-construction-full-feature` | 完整功能开发 | 生成物 | 公共池真实目录 | 依赖 `wf_run` 工具 / workflowEngine；含 `roles/`+`script.mjs`+`meta.json` | 留（D-1 保留方） | |
| 5 | `wf-diagnose` | 诊断·缺陷修复 | 生成物 | 公共池真实目录 | 同上 | 留（D-3 保留方） | |
| 6 | `wf-explore` | 探索·多视角 | 生成物 | 公共池真实目录 | 同上 | 留（D-4 保留方） | |
| 7 | `wf-optimize` | 优化·快速迭代 | 生成物 | 公共池真实目录 | 同上；**无重复对象** | 留 | |

---

## 2. 第三方工程辅助明细（23 个）

「触发面」列：`模型+斜杠` = 模型可自动触发；`仅斜杠` = SKILL.md 标了 `disable-model-invocation: true`。

| # | Skill | 环节 | 触发面 | 重叠/被覆盖对象 | 建议 | 你的决定 |
|---|---|---|---|---|---|---|
| 1 | `to-spec` | 定义 | 仅斜杠 | 被 `requirements-analysis` 覆盖（inventory 原文） | 候选 ① | |
| 2 | `to-tickets` | 定义 | 仅斜杠 | 同上 | 候选 ① | |
| 3 | `triage` | 分诊 | 仅斜杠 | inventory 标「被 requirements-analysis 部分覆盖」，但实为 issue 状态机分诊，面不同 | 留 | |
| 4 | `wayfinder` | 规划 | 仅斜杠 | 跨会话决策地图，与单次定义不同 | 留 | |
| 5 | `research` | 调研 | 模型+斜杠 | 无 | 留 | |
| 6 | `implement` | 开发 | 仅斜杠 | inventory 列为「参考 Skill」；原覆盖依据 `dev-workflow-2-0` 已不存在；与 `wf-construction-full-feature` 的 dev 角色重叠 | 候选 ① | |
| 7 | `prototype` | 开发 | 模型+斜杠 | 无 | 留 | |
| 8 | `tdd` | 开发 | 模型+斜杠 | inventory 标「被 dev-workflow-2-0 部分覆盖」，但该 skill 不存在 → **覆盖依据失效** | 留（待重估） | |
| 9 | `codebase-design` | 开发 | 模型+斜杠 | 无 | 留 | |
| 10 | `domain-modeling` | 开发 | 模型+斜杠 | 无 | 留 | |
| 11 | `code-review` | 审查 | 模型+斜杠 | 无（`wf-*` 的 review 角色是引擎内证明者，非同一入口） | 留 | |
| 12 | `improve-codebase-architecture` | 审查 | 仅斜杠 | 无 | 留 | |
| 13 | `diagnosing-bugs` | 诊断 | 模型+斜杠 | **D-3**：与 `wf-diagnose` 重叠 | **已退役为参考类（2026-09-15）** | 退役 |
| 14 | `grilling` | 打磨 | 模型+斜杠 | **D-2** 保留方 | 留 | |
| 15 | `grill-me` | 打磨 | 仅斜杠 | **D-2**：与 `grilling` 零增量 | **保留（2026-09-15）** | 留 |
| 16 | `grill-with-docs` | 打磨 | 仅斜杠 | **D-2**：`grilling` + 产出 ADR/术语表 | **保留（2026-09-15）** | 留 |
| 17 | `handoff` | 交接 | 仅斜杠 | 无 | 留 | |
| 18 | `resolving-merge-conflicts` | 收尾 | 模型+斜杠 | 无 | 留 | |
| 19 | `setup-pre-commit` | 收尾 | 模型+斜杠 | 无 | 留 | |
| 20 | `neat-freak` | 收尾 | 模型+斜杠 | 无 | 留 | |
| 21 | `migrate-to-shoehorn` | 收尾 | 模型+斜杠 | 技术栈专用（TS 测试断言迁移），可能与本机栈无关 | 待议 | |
| 22 | `scaffold-exercises` | 收尾 | 模型+斜杠 | 教学场景专用，可能与本机栈无关 | 待议 | |
| 23 | `git-guardrails-claude-code` | 护栏 | 模型+斜杠 | 偏 Claude Code hooks 专用 | 待议 | |

候选 ① = 第 4 节「参考 Skill」4 个（inventory 原文已标注「可被第一方覆盖、不再单独使用」）。

**边界外（skill 工具链，不计入开发工作流，供参考）**：`skill-creator`、`writing-great-skills`、`agent-skill-bridge`、`ask-matt`、`setup-matt-pocock-skills`、`find-skills`。
其中 `find-skills` 是**最安全的候选**：WorkBuddy 另有平台内置副本（`plugins/cache/codebuddy-plugins-official/find-skills`），删公共池那份不丢能力。

---

## 3. 重复组明细（4 组）

### D-1 建设工作流 —— 最高置信

| 项 | 内容 |
|---|---|
| 成员 | `construction-bootstrap`（第一方 shim，git 管理）⟷ `wf-construction-full-feature`（生成物，公共池真实目录） |
| 证据 1 | 阶段链完全一致：实施前检查 → 开发 → 收敛审查 → 测试 → UAT → 收口 |
| 证据 2 | `construction-bootstrap/shim-map.md` 退役纪律第 2 条**自声明**：「最终形态：本 skill 成为 #82「建设」正式 Built-in 的运行包装，**不留 construction-bootstrap 与正式建设两份可见业务模板**（#105 Formal Convergence）」 |
| 证据 3 | `wf-construction-full-feature` 即该正式 Built-in：蓝图 `templates/wf-construction-full-feature.json`，走 `wf_run` / `templateId`，6 节点 22 边，带看板续跑、完成类型、fanout/agent 上限、Decision Package |
| 证据 4 | `ai-task-skill-set/README.md:8` 仍写 M2 = `construction-bootstrap` → 文档已过期 |
| 增量差异 | `construction-bootstrap` 独有：DSH 会话内 controller 驱动 + `cwf-*.mjs` 六脚本（preflight / run-init / record / checkpoint / validate / evidence-verify）+ 七类 JSON 记录落盘 + worktree/branch 纪律 |
| 删除影响面 | 5 处引用需同步改：`ai-task-skill-set/README.md:8`、`shim-map.md:15,20`、自身 `SKILL.md:22`、`docs/diagnostic-deepseek-harness-skill-discovery.md` 的技能计数 |
| 回滚成本 | 低 —— 第一方 git 管理，`git revert` 可完全恢复 |
| **前置验证（未做）** | `wf_run` 通道可用性未实测。若 `workflowEngine` 不可用，`wf-construction-full-feature` 会退化为内置 `workflow` 工具单段运行、不可从看板续跑。**不建议在验证前删除** |
| 建议 | 先验证 `wf_run`，通过后删 `construction-bootstrap`，同步更新 README M2 行 | 
| 你的决定 | **已删除（2026-09-14）** —— 松哥裁定 `wf-construction-full-feature` 为更新版本，直接退役 shim；未等 `wf_run` 实测（该验证缺口已如实记录于归档 README） |

### D-2 追问式打磨三胞胎 —— 高置信

| 项 | 内容 |
|---|---|
| 成员 | `grilling`（模型可触发）⟷ `grill-me`（`allow_implicit_invocation: false`）⟷ `grill-with-docs`（同 false） |
| 证据 | 三者 `SKILL.md` **均只有 frontmatter、无正文**；`agents/openai.yaml` 的 `display_name` 分别为 Grilling / Grill Me / 同族 |
| 增量差异 | `grilling` = 通用入口；`grill-me` = **零增量**（同一场访谈）；`grill-with-docs` = 有增量（产出 ADR + 术语表） |
| 删除影响面 | 需四处同时生效：`~/.agents/skills`、`~/.workbuddy/skills`、`~/.claude/skills`、`~/.codex/skills`（桥接由脚本统一处理）；斜杠命令 `/grill-me` 消失 |
| 回滚成本 | 中 —— 公共池非 git 管理，需删排除清单行后重装，或从上游仓库重取 |
| 建议 | 删 `grill-me`（零增量），保留 `grilling` + `grill-with-docs` |
| 你的决定 | **保留全部三个（2026-09-15）** —— 三者的触发面不同（`grilling` 模型可触发，另两个 `disable-model-invocation` 仅斜杠），`/grill-me` 与 `/grill-with-docs` 是独立入口，不做合并。本组结案，不动任何文件 |

### D-3 缺陷诊断 —— 中置信

| 项 | 内容 |
|---|---|
| 成员 | `wf-diagnose`（生成物）⟷ `diagnosing-bugs`（第三方 + 第一方改写版） |
| 证据 | 都是 bug 诊断 → 修复闭环 |
| 增量差异 | `wf-diagnose`：5 节点 18 边、返工额度记账、需 workflowEngine。`diagnosing-bugs`：轻量诊断循环，任意会话可用、无编排无记录 |
| 删除影响面 | 删 `diagnosing-bugs` 后，非运行时的临时排查无轻量专用入口，须起 `wf-diagnose` |
| 建议 | 保留双方（调用面不同）。确实要收敛则删 `diagnosing-bugs` |
| 你的决定 | **保留 `wf-diagnose`，`diagnosing-bugs` 退役为参考类第三方（2026-09-15，已执行）** —— 见 §8 执行记录 |

### D-4 多视角 —— 中置信【已补充详细信息，待你定】

| 项 | 内容 |
|---|---|
| 成员 | `wf-explore`（生成物）⟷ `expert-consultation`（第一方，git 管理） |
| 证据 | 都是「挑互补视角 → 独立研究 → 交叉质疑 → 汇总共识/分歧」 |
| 建议 | 见下方详细对比后判断 |
| 你的决定 | **待定** |

#### D-4a `expert-consultation` 来源

| 项 | 事实 |
|---|---|
| 性质 | **纯第一方自研**，非改编自任何第三方 |
| 引入 | 单次提交 `f87433a`，2026-09-01 15:21，"feat: 新增 expert-consultation 多视角专家会诊 skill (完整数据)" |
| 改动面 | 仅新增 1 个文件，118 行；**无** `source-manifest.json`、无 `upstream` 字段、无 `reference_copies` 条目 |
| 资产 | 无脚本、无 `assets/`、无 `roles/`、无 `evals/` |
| 登记 | `skill-policy.json`：`active` / `global` / `origin: first-party` / 2 个 `accepted_fingerprints`（值相同） |
| **文档缺口** | **未出现在 `skill-desc-translation.md` 任何一张表**（第一方/第三方/参考表均无），该表漏收了它 |
| 与第三方关系 | 无参考来源声明，判定为方法自拟 |

#### D-4b `expert-consultation` 作用

面向**「难决的问题」**，把单一视角的路径依赖拆开，收敛到一份决策建议。

流程四步：

1. **信息核查**——核对「问题 / 已知事实 / 目标 / 现实约束」四项；缺关键项时**只问一个问题**，不列清单。
2. **选 3 个互补视角并说明必要性**——硬性规则明确禁止「3 个相似身份」（如三个前端工程师），必须从不同维度切分（价值机会 / 风险约束 / 落地可行 / 用户受影响 / 长期系统）。
3. **每视角独立答 4 问**——①重定义问题 ②最推荐路径 ③其他视角易忽略的风险 ④什么新证据会推翻自己。强调认知隔离，不提前剧透他人结论。
4. **三方互相质疑**——共同认可的事实 / 真正的分歧 / **分歧背后的不同假设**（作者认为多数「分歧」实为假设不同）。
5. **主持人综合收口（五段）**——推荐方案 / 适用条件 / 最大风险 / 退出条件（止损线）/ 第一步行动。

硬性护栏：先不开药（流程走完前不给结论）；不模仿、不编造真实人物，视角是「专业透镜」而非具名个人。

#### D-4c 与 `wf-explore` 的逐维对比

| 维度 | `expert-consultation` | `wf-explore` |
|---|---|---|
| 收敛目标 | **决策**（要不要做、怎么做） | **研究结论**（问题到底是怎么回事） |
| 视角数量 | 固定 3 个 | 3–5 个，由统筹节点决定 |
| 产出物 | 决策建议五段（含退出条件、第一步行动） | 证据地图 + 共识/分歧 + 完成类型 |
| 终止条件 | 走完四步即结束 | `PASS` / `NEEDS_RESEARCH` / `INSUFFICIENT`，可自动补研 ≤2 轮 |
| 运行载体 | 单会话内完成，**零外部依赖** | 4 节点 / 10 边，**需 `wf_run` 或 workflowEngine** |
| 记录留痕 | 无落盘要求 | Logical Run / 分段 / 完成类型 / 可续跑 |
| 视角身份 | 抽象专业透镜（明令禁止套用真人） | 专家 Agent，接收任务书 |
| 体量 | 118 行单文件 | 6 文件（SKILL + meta + script + 4 roles，共约 480 行） |
| 上游 | 松哥自研，无上游 | workflow-manager 蓝图编译生成物 |

**结论**：重叠是真实存在的（都做「互补视角 + 独立作答 + 交叉质疑」），但**收敛目标不同**——一个收敛到决策，一个收敛到研究结论；且 `wf-explore` 硬依赖引擎，`expert-consultation` 零依赖，因此后者天然是「引擎不可用时」的轻量替代路径。

**三个可选处置**（未选定，等你定）：

| 选项 | 动作 | 代价 |
|---|---|---|
| A 保留双方 | 不动，各自按触发词分流 | 触发词有重叠（"从多个角度看""帮我分析一下"），可能都触发 |
| B 降级为轻量替代 | 保留但改 `description`，明确「仅当 wf-explore 引擎不可用时使用」 | 需改 SKILL.md 触发条件；功能仍在 |
| C 退役 | 与 D-1/D-3 同法，`skill-policy.json` 置 `retired` + 目录移出发现目录 | 失去零依赖路径；且它是自研资产，无第三方可回退 |

---

## 4. 存量记录的复核（inventory 已标注，但现状已变）

`inventory/skill-desc-translation.md` 原文标注了 5 处「被部分覆盖」，逐条复核：

| 原文标注 | 现状复核 | 结论 |
|---|---|---|
| `tdd` 被 `dev-workflow-2-0` 部分覆盖 | `dev-workflow-2-0` 在本仓 git 历史中 **0 个提交**，仅存在于 inventory 文本中；实际已被 M1/M2/M3 取代 | **覆盖依据失效** → `tdd` 需重新评估。**已于 2026-09-14 处置**：松哥确认该 skill 过期，已从 inventory 移出（第一方 6→5、合计 81→80），并同步删除第三方前言中的该条覆盖声明 |
| `triage` 被 `requirements-analysis` 部分覆盖 | `requirements-analysis` 自称「唯一定义入口」，但 `triage` 做 issue 状态机分诊，职责不同 | 保留 |
| `grill-with-docs` 被 `requirements-analysis` 部分覆盖 | 见 D-2 | 并入 D-2 |
| `wayfinder` 被 `requirements-analysis` 部分覆盖 | `wayfinder` 做跨会话决策地图，与单次定义不同 | 保留 |
| `skills-security-check` 被 `agent-skill-bridge` 部分覆盖 | `agent-skill-bridge` 内置审计步骤，但 `skills-security-check` 可对任意 skill 独立审计 | 保留 |

**「参考 Skill」板块 4 个**（inventory 原文定义：功能可被第一方覆盖、不再单独使用）：

| Skill | 复核 | 建议 |
|---|---|---|
| `implement` | 原覆盖依据 `dev-workflow-2-0` 已不存在；但与 `wf-construction-full-feature` 的 dev 角色重叠 | 候选 |
| `to-spec` | 若 `requirements-analysis` 已含规格产出，可删 | 候选 |
| `to-tickets` | 同上 | 候选 |
| `find-skills` | **WorkBuddy 另有平台内置副本**，删公共池那份不丢能力 | 候选（最低风险，建议优先） |

---

## 5. 清单本身的问题（不涉及删除，但影响筛选依据）

1. **`inventory` 第一方板块在本仓无法对账（部分已处置）**：原写「第一方 6 个」，其中 `dev-workflow-2-0` **已于 2026-09-14 确认过期并移出**（职责由 M1 `requirements-analysis` / M2 `wf-construction-full-feature` / M3 `execution-plan` 承接，第一方 6→5、合计 81→80）。余下 3 个（`agent-cli-tool-residue-purge`、`clashx-openai-sse-debug`、`duplicate-cli-unify`）在本仓 git 历史中 **0 个提交**——均系 macOS 专有能力（launchd / Homebrew / ClashX），可能属 Mac 侧本地未入库，Windows 侧无法判定，**本次未动**。同时该板块漏记 12 个存在于本仓真源目录的 skill：`execution-plan`、`cross-domain-borrowing`、`expert-consultation`、`fact-check`、`first-principle`、`learn_something_new`、`life-design`、`minimum-scale-experiment`、`socratic-clarify`、`steelmanning`、`uncover-hidden-talents`、`skills-security-check`（真源现有 14 个含 SKILL.md 的目录，`construction-bootstrap` 删除后由 15 降为 14；inventory 只覆盖到其中 2 个）。
2. **`wf-*` 四个生成物未入表**。
3. **`my-skills/skills-security-check`** 是第三方内容放在第一方真源目录（inventory 列为第三方 #71）。
4. **`ai-task-skill-set/README.md` 的 M2 行过期**（仍指向 `construction-bootstrap`）—— **已修正（2026-09-14），M2 现指向 `wf-construction-full-feature`，并补入「收敛记录」小节**。
5. **计数不可直接对账**：inventory 写「共 81 个」（Mac 快照，2026-08-24），Windows 池实测 92 个含 SKILL.md 的目录。两者机器与时间点均不同，差额不能全部归因于失真。

---

## 6. 风险与前置验证项

1. **`tools/install_all_skills.sh` 会把删掉的第三方 skill 装回来** —— 已在 §7 处理；但注意排除清单**只管「不装」，不管「删除」**。
2. **`wf_run` 通道未实测** —— D-1 删除的前置条件。
3. **第三方与 `wf-*` 删除不可 git 回滚** —— 只有第一方在 git 里。
4. **`install_all_skills.sh` 不覆盖 5 个大体积 skill**（`ppt-master` / `humanize-ppt` / `beautiful-html-templates` / `baoyu-slide-deck` / `guizang-ppt-skill`），它们由仓库链接单独安装，与本次去重无关。
5. **文档计数不要从 Windows 侧改**：`docs/diagnostic-deepseek-harness-skill-discovery.md` 是 Mac 快照（自述「本机 Mac mini」），其 85/86 对应 Mac 池，与 Windows 池无对应关系；`inventory/skill-desc-translation.md` 同属 Mac 快照。**本次不改这两份文件**，避免用 A 机器的数据改写 B 机器的记录。
6. **跨机器连带影响**：仓库经 GitHub 同步后，Mac 侧 `my-skills/construction-bootstrap` 会消失，Mac 的 4 处软链将悬空，需在 Mac 上单独清理。

---

## 7. 排除清单机制（已实施）

| 项 | 内容 |
|---|---|
| 新增文件 | `tools/skill-exclusions.txt` —— 一行一个 skill 目录名，`#` 开头为注释，空行忽略 |
| 脚本改动 | `tools/install_all_skills.sh`：解包后按清单跳过安装；桥接阶段同样跳过，并清理已存在的桥接软链 |
| 语义 | **只做「不安装 / 不桥接」，不等于「删除」**。已存在的目录不会被脚本删除 |
| 验证 | `bash -n` 语法通过；匹配逻辑单测通过（空清单不误命中、前后空白与 CRLF 容错、精确匹配不误伤） |
| 当前状态 | 清单为空（待本表筛选结果填入）—— 注：`construction-bootstrap` 属第一方（不在本脚本内嵌 tarball 中，已解码核验 0 匹配），因此无需加入排除清单 |

---

## 8. 执行记录

### 2026-09-14｜D-1 已执行

**决定**：删除 `construction-bootstrap`，保留 `wf-construction-full-feature`（后者为前者的更新版本）。

| 项 | 内容 |
|---|---|
| 备份 | `.workbuddy/backup/2026-09-14-construction-bootstrap/`（含 `SKILL.md` / `runbook.md` / `shim-map.md` + 归档说明 README），逐文件 md5 校验一致 |
| 已删除路径 | ① `D:\workspace\my-agent-skills\my-skills\construction-bootstrap\`（真源，git 管理）<br>② `C:\Users\22487\.agents\skills\construction-bootstrap`（软链）<br>③ `C:\Users\22487\.workbuddy\skills\construction-bootstrap`（软链）<br>④ `C:\Users\22487\.claude\skills\construction-bootstrap`（软链）<br>⑤ `C:\Users\22487\.codex\skills\construction-bootstrap`（软链） |
| 核验 | 5 处路径全部清除；4 个 skill 池悬空软链扫描结果为空；`wf-construction-full-feature` 在 4 个池中均完好 |
| 引用同步 | `ai-task-skill-set/README.md` M2 行已改指 `wf-construction-full-feature`，并新增「收敛记录」小节承接 `shim-map.md` 的退役纪律记录（原文随目录归档） |
| 未提交 | 改动**未 commit**（按约定不自行提交），待你确认后用 `scripts/sync.sh` 推送 |
| **跨机器待办** | 仓库同步到 Mac 后，需在 Mac 上清理 4 处悬空软链：`~/.agents/skills/construction-bootstrap`、`~/.workbuddy/skills/construction-bootstrap`、`~/.claude/skills/construction-bootstrap`、`~/.codex/skills/construction-bootstrap` |
| **遗留验证缺口** | `wf_run` 通道仍未实测。若 `workflowEngine` 不可用，`wf-construction-full-feature` 会退化为内置 `workflow` 工具单段运行、不可从看板续跑 |

> 说明：D-1 当日在**过期基线**（`8617e8c`）上执行；09-15 发现 CNB 基线 `b6933e4` 已把 `my-skills/construction-bootstrap` 扩到 23 文件，遂在新基线上重做，并在同一 PR 内登记 4 个 `wf-*`。以 §2026-09-15 记录为准。

### 2026-09-15｜D-3 已执行 + `wf-*` 登记

**决定**：登记 4 个 `wf-*`；`construction-bootstrap` 与 `dev-workflow-2-0` 置 `retired`；`diagnosing-bugs` 退役为参考类第三方，诊断职责由 `wf-diagnose` 承接。

| 项 | 内容 |
|---|---|
| 基线 | CNB `b6933e4`（本地原基线 `8617e8c` 落后 2 提交，已快进对齐） |
| 登记 4 个 `wf-*` | `wf-construction-full-feature` / `wf-diagnose` / `wf-explore` / `wf-optimize`，`active` + `global`，`upstream` 指向 workflow-manager 蓝图，指纹由 `manage-skills.fingerprint()` 生成 |
| 退役 2 个 | `construction-bootstrap`（23 文件，active）、`dev-workflow-2-0`（9 文件，transition）→ `retired`，目录移至 `~/.local/share/agent-skills/retired/<name>` |
| D-3 处置 | `diagnosing-bugs`：`active`/`first-party`/`my-skills/diagnosing-bugs` → `reference`/`third-party`/`~/.local/share/agent-skills/references/diagnosing-bugs`，加 `migrate: true`；第一方改写版（1 文件）归档至 `retired/diagnosing-bugs-first-party/`；`my-skills/diagnosing-bugs/` 已 `git rm` |
| 参考副本落盘 | 执行 `reference_copies` 声明的迁移：`~/.agents/skills/diagnosing-bugs` → `~/.local/share/agent-skills/references/diagnosing-bugs`（3 文件）；清理 `.workbuddy` / `.claude` / `.codex` 三处桥接软链，无悬空 |
| 派生文档 | `skill-lifecycle.md` 按登记表重建（D-1 部分 6 行 + D-3 部分 1 行）；`skill-desc-translation.md` 中 `diagnosing-bugs` 由第三方表移入「参考 Skill」板块（第三方 71→70、参考 4→5，总数不变） |
| 验证 | `plan`：UNMANAGED 6→2（余 `llm-wiki`、`windows-ai-coding-env-setup`）、MISSING 17→16（`references/diagnosing-bugs` 由缺失转为就位）、OK 224→228、SOURCE 75→79 |
| **已知偏差** | `plan` 对 `references/diagnosing-bugs` 报 `CONFLICT 参考资料与保留版本不同，未覆盖` —— 因参考副本由手工落盘而非 `apply` 生成。该行为**不覆盖任何内容、无数据损失**；在本机执行一次 `manage-skills.py apply` 即可对齐 |
| 产物 | commit `010c0d4` + 本批 D-3 改动，已推送 CNB 分支 `chore-skill-dedup-20260915`，PR #2 |

---

## 待办

- [x] D-1 执行（2026-09-14，后于 09-15 在新基线上重做）
- [x] D-2 结论：保留全部三个
- [x] D-3 执行（2026-09-15）
- [ ] **D-4 待你选**：A 保留双方 / B 降级为轻量替代 / C 退役（见 D-4 详细对比）
- [ ] 实测 `wf_run` 通道（D-1 遗留验证缺口）
- [ ] 在 Mac 上清理 `construction-bootstrap` 4 处悬空软链，并在本机跑一次 `manage-skills.py apply` 对齐 `references/diagnosing-bugs` 的 CONFLICT
- [ ] 修正 `skill-desc-translation.md` 漏收 `expert-consultation` 的缺口（D-4a 发现）
- [ ] 择机在**各自机器上**修正两份 Mac 快照文档（`docs/diagnostic-deepseek-harness-skill-discovery.md` 技能计数）—— 不在 Windows 侧代改
