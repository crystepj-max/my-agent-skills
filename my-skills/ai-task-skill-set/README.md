# AI 任务交付 Skill 集合（从 workflow-manager 同步）

本目录说明 + 下列三个 skill 构成通用集合；到点开跑（M4）不另建 Skill，见 `execution-plan` 内说明。

| 代号 | Skill 目录 | 作用 |
|---|---|---|
| M1 | `requirements-analysis` | 谈到「已定义」 |
| M2 | `wf-construction-full-feature` | 启动「完整功能开发」单任务交付（由 workflow-manager 蓝图 `templates/wf-construction-full-feature.json` 编译生成，非本仓副本） |
| M3 | `execution-plan` | 批量调度；定时 = 到点再调本入口 |
| M4 | （无独立 Skill） | 到点启动脚本在 workflow-manager：`scripts/ai-task-scheduled-trigger.mjs` |

同步命令（在 workflow-manager）：

```bash
node scripts/sync-ai-task-skill-set.mjs
```

**不要**在此仓单独改出第二套流程规则；以 workflow-manager 工程真源为准后再同步。

## 收敛记录

| 日期 | 事项 | 说明 |
|---|---|---|
| 2026-09-15 | `construction-bootstrap` 退役 | 该 skill 是「建设」正式 Built-in 的 Bootstrap shim（23 个文件，含 assets/ 与 cwf-*.mjs）。已由 M2 正式生成物 `wf-construction-full-feature` 承接，两者阶段链一致。在 `skill-policy.json` 置为 `retired`，目录移出发现目录至 `~/.local/share/agent-skills/retired/construction-bootstrap`。 |
| 2026-09-15 | `dev-workflow-2-0` 退役 | 原「开发工作流 2.0」整体入口，职责已拆分为 M1 `requirements-analysis` / M2 `wf-construction-full-feature` / M3 `execution-plan`。在 `skill-policy.json` 由 `transition` 置为 `retired`，目录移至 `~/.local/share/agent-skills/retired/dev-workflow-2-0`。 |
| 2026-09-15 | 4 个 `wf-*` 登记入表 | `wf-construction-full-feature` / `wf-diagnose` / `wf-explore` / `wf-optimize` 此前在 `manage-skills.py plan` 中属 UNMANAGED（未登记）。现已登记为 `active` + `global`，`upstream` 指向 workflow-manager 蓝图。 |
