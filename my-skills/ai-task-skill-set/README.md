# AI 任务交付 Skill 集合（从 workflow-manager 同步）

本目录说明 + 下列三个 skill 构成通用集合：

| 代号 | Skill 目录 | 作用 |
|---|---|---|
| M1 | `requirements-analysis` | 谈到「已定义」 |
| M2 | `construction-bootstrap` | 启动「完整功能开发」单任务交付（蓝图真源在 workflow-manager） |
| M3 | `execution-plan` | 批量调度 |

同步命令（在 workflow-manager）：

```bash
node scripts/sync-ai-task-skill-set.mjs
```

**不要**在此仓单独改出第二套流程规则；以 workflow-manager 工程真源为准后再同步。
