# my-agent-skills

维护个性化第一方技能、第三方参考与过渡能力，以及多助手实际入口。

## 唯一登记与职责

- `inventory/skill-policy.json`：正式状态、范围、维护来源、已审阅版本和专业工作空间位置。
- `inventory/skill-lifecycle.md`：登记表的人读版本；`skill-desc-translation.md` 保留上游来源与描述。
- `my-skills/`：第一方执行入口。需求、建设、批量调度三项从 workflow-manager 同步，带完整 assets 和 source-manifest，不能仅同步 SKILL.md。
- `my-plugins/leader/`：个人插件的可维护来源；`overrides/` 保存已审阅第三方条款与个人插件的定点修正，不自动适配未知上游版本。
- 全局任务分类、批准与完成规则由 agent-policy 维护，此仓不复制一套。

## 使用与恢复

```bash
python3 scripts/manage-skills.py plan --report /tmp/skill-plan.json
python3 scripts/manage-skills.py apply --report /tmp/skill-apply.json
python3 scripts/manage-skills.py check
python3 -m unittest discover -s tests
```

应用前核对范围；任务已有授权时不重复批准。不同本机内容保留为 CONFLICT；MISSING 不当作成功。备份留在 `~/.local/share/agent-skills/backups/`，退出执行的资料留在登记的 reference/retired 或专业工作空间。

换设备：先 clone 本仓，按实际位置修改登记表的 projects，再运行 `bash scripts/restore.sh`。恢复器只提取清单需要且缺失的离线资料，随后按范围建立入口；已存在内容不会被旧全量包覆盖。

`tools/skills-bundle.tar.gz` 是轻量过渡/参考资料的离线恢复包，延续原有打包能力但不包含第一方副本、退役备份和大型 PPT 资产。用 `python3 tools/build_install_all.py` 从已核对来源重建。原 `tools/install_all_skills.sh` 只转交新恢复器。

大型演示资料留在 Chris-Vault 的 `.agent-assets/presentations/`，不收入技能仓库。更换设备需同步该专业空间的资产；缺失时报告 MISSING，不把旧能力重新装回全局。第一方 `presentation-production` 安装在该空间的 `.agents/skills/` 和 `.claude/skills/`，可使用宿主已有制作能力。其他插件内置演示能力仍属宿主管理，不自动卸载或改写。

新会话才可能载入更新后的技能目录；当前会话中已展开的旧指令不会因改文件自动消失。检查磁盘入口、宿主实际目录与任务行为是三个不同层次。

## 维护与发布

第一方源改动经校验后直接经入口引用；三项开发流程先在 workflow-manager 修改，然后运行 `node scripts/sync-ai-task-skill-set.mjs <本仓路径>`。完整同步会保留原目录备份。

本地应用、恢复或检查不自动提交。用户明确要求发布后，先审阅并只暂存本次文件，再运行 `bash scripts/sync.sh --publish-staged "提交说明"`；只推送当前分支，不强制推到 main。
