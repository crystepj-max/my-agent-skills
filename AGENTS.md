# 技能治理项目约定

全局协作规则见 `~/.config/agent-policy/AGENTS.md`；本文件只补充本项目约定。

- 目标：第一方入口负责完整执行，第三方逐步转为参考，专业能力进入项目工作空间；恢复后不倒退。
- 正式登记为 `inventory/skill-policy.json`，人读状态表为 `inventory/skill-lifecycle.md`。说明清单保留来源资料，不能代替实际启用状态。
- 允许围绕当前请求修改 my-skills、my-plugins、overrides、inventory、scripts、tools 和相应说明；不改无关业务代码、凭据、其他助手独有配置。
- 需求、建设、批量调度在 workflow-manager 的 dsh/skills 和对应 scripts/docs 维护，通过其 sync-ai-task-skill-set.mjs 连同资产及校验清单分发；不在这里独立演变这三项产品流程。
- 第一方入口连接维护源；未审阅的本机差异须保留。参考、退役和备份放在发现目录外。定点第三方修正仅适配登记的原版本，遇到上游变化先报告。
- 规则文字或安装行为调整属于编程治理工作：明确范围→内部验证→呈交验收。用户对两轮审阅调整的现有授权是本次范围基线，不逐文件重复确认。
- 验证：`python3 -m unittest discover -s tests`；`python3 scripts/manage-skills.py plan`；应用后 `python3 scripts/manage-skills.py check`；核对新会话可见目录与未验证限制。管理检查不是每个创作工具的业务验收。
- 不自动提交、推送或发布；明确授权后只处理已审阅的指定文件。备份与生成检查报告不进入版本库。
