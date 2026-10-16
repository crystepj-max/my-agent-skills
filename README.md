# my-agent-skills

维护个性化第一方技能、第三方参考与过渡能力，以及多助手实际入口。

## 唯一登记与职责

- `inventory/skill-policy.json`：正式状态、范围、维护来源、已审阅版本和专业工作空间位置。
- `inventory/skill-lifecycle.md`：登记表的人读版本；`skill-desc-translation.md` 保留上游来源与描述。
- `my-skills/`：本仓承担维护的第一方执行来源之一；登记表也指向其他项目维护源及专业工作空间。登记维护责任不证明最初作者或原创来源。历史 `requirements-analysis` 副本留在 `inventory/history/`，不再登记或分发；唯一维护源和用户级安装入口在 workflow-manager。M1 需求分析由 workflow-manager 维护并直接分发，M3 执行计划只在 dev-flow 项目内维护；本仓不登记、不镜像、不分发 M1/M3。M2 单任务交付继续由 workflow-manager 蓝图生成。
- `my-plugins/leader/`：个人插件的可维护来源；正式策略保留 leader 的 3 条已审阅定点修正（SKILL.md、anatomy.md、style.md）。`overrides/baoyu-image-gen.json`、`baoyu-infographic.json`、`grilling.json`、`investment-team.json` 是保留的旧修正文件，不在当前正式覆盖策略中，不应自动应用。定点修正不自动适配未知上游版本。
- 全局任务分类、批准与完成规则由 agent-policy 维护，此仓不复制一套。

本轮登记范围：3 项技能退役并保留完整备份；13 项创作技能迁至 Chris-Vault 的 `presentations` 项目；20 项金融技能迁至 `ai-valueinvest` 的 `investments` 项目；`test-report-html` 以一个登记名同时映射到 Gawain 与 AUTOTEST。`improve-codebase-architecture`、`prototype`、`pr`、`retro`、`setup-pre-commit` 只列名称为本机待讨论项，不进入本次发布策略、参考副本或离线包；本机源与别名留存。

## 原件、上游对照与参考边界

本轮正式登记以 142 条已接受登记为基线，排除 5 项本机待讨论技能后为 137 条：`first-party` 122 条（active 116、retired 6），`third-party` 15 条（transition 1、reference 12、retired 2）。范围为 `global` 95、`presentations` 20、`investments` 20、`gawain` 2。项目源映射中 `test-report-html` 仍只计一个技能名，同时覆盖 Gawain 与 AUTOTEST。本轮登记 `reference_copies` 为 100 条（旧 102 条减 5 项 hold，再纳入 main 中新增的 3 份 DSH/workspace 原件参考）。完整映射见 [生命周期清单](inventory/skill-lifecycle.md) 与 [来源说明表](inventory/skill-desc-translation.md)。本轮正式 `apply`、`check` 与重复检查均已通过；独立本机入口核验确认 37 项全局入口已退出、35 个项目技能实例就位，5 项 hold 的本机源与别名保持；64 项管理测试通过。本轮 100 条参考副本已通过两个恢复入口分别核验，均为 100/100 完整指纹匹配；重复恢复保留 fixture 中已有改动。当前离线包 SHA-256 为 `410ebcee70e2cbe53007f4af7c756dfb5d008225681535b90a964bdeb76b94de`。旧 102 条恢复证据不能替代本轮结果。新会话可见性、创作/投研/游戏业务行为、Windows 恢复与用户验收仍未验证。

已被第一方入口承接的旧完整安装包只作为参考资料，保存在策略登记的独立 reference 目录；不得因解包或恢复而把被替代的原第三方入口重新放回技能发现目录。历史原件与当前第一方维护源分别记录，不把“当前由本仓/项目维护”解释成“最初由其原创”。

上游版本对照应在技能发现目录之外，以固定 commit 单独下载到独立快照目录，再运行只读 diff；不直接覆盖维护源或现行入口。当前 `tools/fetch_skill_reference.py` 只预置 Matt Pocock 仓库的 `wizard`、`to-questionnaire`、`wait-what` 三项，不会自动获取本轮迁至项目空间的 34 个技能名。其余已登记上游按各自来源信息单独获取参考；来源未确认的项目保持未确认，不补造作者或仓库。`tools/compare_skill_reference.py` 只报告差异，不安装、不更新入口。恢复已保存的旧原件只补回策略指定的 reference 位置，不重启或重建被替代的原入口。

`tools/skills-bundle.tar.gz` 是按登记范围构建的过渡/参考离线资料，不是技能状态名单。本轮正式策略登记 100 条 `reference_copies`；旧包和既往 102 条参考副本的恢复验证只对应先前登记快照，不能作为新 100 条清单的验证证据。本轮离线包已按正式登记重建，并通过两个恢复入口的 100/100 完整指纹核验（SHA-256：`410ebcee70e2cbe53007f4af7c756dfb5d008225681535b90a964bdeb76b94de`）；第一方维护源、退役备份及大型演示资产不由旧全量安装包替代。

本轮正式 `inventory/skill-policy.json` 已应用；`apply`、`check` 与重复检查通过，独立本机入口核验及 64 项管理测试也已通过。100 条 `reference_copies` 已通过两个恢复入口分别核验，均为 100/100 完整指纹匹配；离线包 SHA-256 为 `410ebcee70e2cbe53007f4af7c756dfb5d008225681535b90a964bdeb76b94de`。先前针对 102 条的结果只是旧策略快照证据。新会话可见性、创作/投研/游戏业务行为、Windows 恢复与用户验收仍未验证。

## 使用与恢复

```bash
python3 scripts/manage-skills.py plan --report /tmp/skill-plan.json
python3 scripts/manage-skills.py apply --report /tmp/skill-apply.json
python3 scripts/manage-skills.py check
python3 -m unittest discover -s tests
```

应用前核对范围；任务已有授权时不重复批准。不同本机内容保留为 CONFLICT；MISSING 不当作成功。备份留在 `~/.local/share/agent-skills/backups/`，退出执行的资料留在登记的 reference/retired 或专业工作空间。

换设备：先 clone 本仓，按实际位置修改登记表的 projects，再运行 `bash scripts/restore.sh`。恢复器只提取登记范围需要且缺失的离线资料，随后按范围建立入口；已存在内容不会被旧全量包覆盖。恢复完整旧安装包时只补回登记的 reference 位置，不会启用已退役的原入口，也不会把本机待讨论技能重新分发。

`tools/skills-bundle.tar.gz` 是按登记范围生成的轻量过渡/参考离线资料包，不包含第一方维护源、退役备份和大型 PPT 资产。本轮正式登记后已重建并复核离线包（SHA-256：`410ebcee70e2cbe53007f4af7c756dfb5d008225681535b90a964bdeb76b94de`），两个恢复入口各自恢复 100/100 条参考副本且完整指纹匹配。原 `tools/install_all_skills.sh` 只转交恢复器；它不是旧全量安装行为的授权入口。

大型演示资料留在 Chris-Vault 的 `.agent-assets/presentations/`，不收入技能仓库。更换设备需同步该专业空间的资产；缺失时报告 MISSING，不把旧能力重新装回全局。第一方 `presentation-production` 安装在该空间的 `.agents/skills/` 和 `.claude/skills/`，可使用宿主已有制作能力。其他插件内置演示能力仍属宿主管理，不自动卸载或改写。

新会话才可能载入更新后的技能目录；当前会话中已展开的旧指令不会因改文件自动消失。检查磁盘入口、宿主实际目录与任务行为是三个不同层次。

## 维护与发布

`requirements-analysis` 的维护和用户级分发由 workflow-manager 完成；本仓不提供同步命令。执行计划只在 dev-flow 项目目录中使用，不经本仓同步。

本地应用、恢复或检查不自动提交。用户明确要求发布后，先审阅并只暂存本次文件，再运行 `bash scripts/sync.sh --publish-staged "提交说明"`；只推送当前分支，不强制推到 main。
