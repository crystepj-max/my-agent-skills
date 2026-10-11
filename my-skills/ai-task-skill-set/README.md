# AI 任务工作流入口索引

本文件只记录技能归属，不负责安装、同步或分发。

| 能力 | 唯一维护源 | 使用位置 | 用途 |
|---|---|---|---|
| Requirements Analysis | `workflow-manager/dsh/skills/requirements-analysis` | 用户级技能目录；使用 workflow-manager 的安装脚本 | 分析需求、确认基线并将正式定义写入 Multica Task |
| 单任务交付 | workflow-manager 内置 Workflow | DSH 工作流 | 按已确认的任务定义施工 |
| Execution Plan | `dev-flow/.agents/skills/execution-plan` | dev-flow 项目级技能目录 | 读取 Multica Task 状态并生成开发计划 |

`my-agent-skills` 不镜像、不登记、不分发 `requirements-analysis` 或 `execution-plan`。历史副本保留在 `inventory/history/requirements-analysis/content/`；不得把它作为当前来源。
