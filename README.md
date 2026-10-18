# my-agent-skills

维护个性化第一方技能、第三方参考与过渡能力，以及多助手实际入口。

## 唯一登记与职责

- `inventory/skill-policy.json`：正式状态、范围、维护来源、已审阅版本和专业工作空间位置。
- `inventory/skills-summary.md`：面向人的全局总表，由 `python3 scripts/build_skills_summary.py` 从机器登记生成。
- `inventory/skills/descriptions-zh.md`、`provenance.md`、`revision-history.md`：分别维护中文描述、来源/上游版本、重要修订；日期或来源无证据时明确标为未记录/未确证。
- `my-skills/`：本仓承担维护的第一方执行来源之一；登记表也指向其他项目维护源及专业工作空间。登记维护责任不证明最初作者或原创来源。历史 `requirements-analysis` 副本留在 `inventory/history/`，不再登记或分发；唯一维护源和用户级安装入口在 workflow-manager。M1 需求分析由 workflow-manager 维护并直接分发，M3 执行计划只在 dev-flow 项目内维护；本仓不登记、不镜像、不分发 M1/M3。M2 单任务交付继续由 workflow-manager 蓝图生成。
- `my-plugins/leader/`：个人插件的可维护来源；正式策略保留 leader 的 3 条已审阅定点修正（SKILL.md、anatomy.md、style.md）。`overrides/baoyu-image-gen.json`、`baoyu-infographic.json`、`grilling.json`、`investment-team.json` 是保留的旧修正文件，不在当前正式覆盖策略中，不应自动应用。定点修正不自动适配未知上游版本。
- 全局任务分类、批准与完成规则由 agent-policy 维护，此仓不复制一套。

既有迁移范围包括：3 项技能退役并保留完整备份；13 项创作技能迁至 Chris-Vault 的 `presentations` 项目；20 项金融技能迁至 `ai-valueinvest` 的 `investments` 项目；`test-report-html` 以一个登记名同时映射到 Gawain 与 AUTOTEST。2026-10-17 候选在此基础上纳入此前暂缓的 `improve-codebase-architecture`、`prototype`、`pr`、`retro`、`setup-pre-commit` 五项第一方维护源，并为各自原安装快照保留只读 reference。

## 原件、上游对照与参考边界

候选的远端基线 `origin/main`（`9a5c930`）有 137 项登记：`first-party` 122 项（active 116、retired 6），`third-party` 15 项（transition 1、reference 12、retired 2）；范围为 `global` 95、`presentations` 20、`investments` 20、`gawain` 2，`reference_copies` 为 100 条。候选新增 5 项 `first-party/global/active`，并为五份原安装快照各新增一条 reference，合计 142 项、127 项第一方维护（active 121、retired 6）、15 项第三方来源，以及 105 条 reference；原有 137 项和 100 条 reference 保持不变。`test-report-html` 仍只计一个技能名，同时覆盖 Gawain 与 AUTOTEST。2026-10-18 追加 1 项第一方维护源 `research-report-generator` 后为 143 项、128 项第一方维护（active 122、retired 6）、15 项第三方来源，`reference_copies` 仍为 105 条。完整映射见 [Skills 总览](inventory/skills-summary.md) 与 [来源档案](inventory/skills/provenance.md)。

此前对 137 项/100 条的正式 `apply`、`check` 和独立入口核验属于上一轮基线，不能代替本候选的应用结果。本候选的 64 项管理测试在隔离 worktree 中通过；两个恢复入口在全新临时 HOME 中各自恢复 105/105 条参考并匹配完整指纹，重复恢复保留了刻意修改；临时 HOME 的 `Manager.apply` 建立 35 个入口，重复检查为 35 个 `OK`、5 个 `SOURCE`，无 `CHANGE`、`CONFLICT` 或 `MISSING`。未对真实 HOME 执行本候选的策略 `apply`。这些结果不证明新会话可见性、真实业务行为、Windows 恢复或用户验收。

已被第一方入口承接的旧完整安装包只作为参考资料，保存在策略登记的独立 reference 目录；不得因解包或恢复而把被替代的原第三方入口重新放回技能发现目录。历史原件与当前第一方维护源分别记录，不把“当前由本仓/项目维护”解释成“最初由其原创”。

上游版本对照应在技能发现目录之外，以固定 commit 单独下载到独立快照目录，再运行只读 diff；不直接覆盖维护源或现行入口。当前 `tools/fetch_skill_reference.py` 只预置 Matt Pocock 仓库的 `wizard`、`to-questionnaire`、`wait-what` 三项，不会自动获取本轮迁至项目空间的 34 个技能名。其余已登记上游按各自来源信息单独获取参考；来源未确认的项目保持未确认，不补造作者或仓库。`tools/compare_skill_reference.py` 只报告差异，不安装、不更新入口。恢复已保存的旧原件只补回策略指定的 reference 位置，不重启或重建被替代的原入口。

`tools/skills-bundle.tar.gz` 是本地生成的过渡/参考恢复资料，不是技能状态名单，也不纳入 Git：`.gitignore` 忽略所有 `*.tar.gz`。当前候选包由 `python3 tools/build_install_all.py` 本地生成，包含 105 条登记 reference；第一方维护源由仓库策略连接到源目录，不放进归档。候选包指纹为 `019e7ad62d87fa3b5bd7152184b8e81e97c5e79a852d1a3002a0e4a712023d52`，此文件需在保存原参考资料的机器上单独保留。单纯 clone 不会下载该归档；若需从离线资料恢复，须另行提供归档，或在原参考目录仍可用时先重新构建。两个恢复入口均已在临时 HOME 中各自恢复 105/105 条 reference，且均位于技能发现目录之外。

## 使用与恢复

```bash
python3 scripts/manage-skills.py plan --report /tmp/skill-plan.json
python3 scripts/manage-skills.py apply --report /tmp/skill-apply.json
python3 scripts/manage-skills.py check
python3 scripts/build_skills_summary.py
python3 -m unittest discover -s tests
```

应用前核对范围；任务已有授权时不重复批准。不同本机内容保留为 CONFLICT；MISSING 不当作成功。备份留在 `~/.local/share/agent-skills/backups/`，退出执行的资料留在登记的 reference/retired 或专业工作空间。

换设备：先 clone 本仓，按实际位置修改登记表的 projects，再准备本地参考归档后运行 `bash scripts/restore.sh`。恢复器只提取登记范围需要且缺失的离线资料，随后按范围建立入口；已存在内容不会被旧全量包覆盖。reference 只恢复到登记的发现目录之外，不会启用被替代的旧入口。单纯 clone 不包含被 `.gitignore` 忽略的本地 `tools/skills-bundle.tar.gz`。

`tools/skills-bundle.tar.gz` 是按登记范围生成的轻量过渡/参考离线资料包，不包含第一方维护源、退役备份和大型 PPT 资产。候选本地归档包含 105 条 reference，SHA-256 为 `019e7ad62d87fa3b5bd7152184b8e81e97c5e79a852d1a3002a0e4a712023d52`；归档本身不在 Git 中，必须单独保存。第一方维护源由仓库中的策略建立入口。原 `tools/install_all_skills.sh` 只转交恢复器；它不是旧全量安装行为的授权入口。

大型演示资料留在 Chris-Vault 的 `.agent-assets/presentations/`，不收入技能仓库。更换设备需同步该专业空间的资产；缺失时报告 MISSING，不把旧能力重新装回全局。第一方 `presentation-production` 安装在该空间的 `.agents/skills/` 和 `.claude/skills/`，可使用宿主已有制作能力。其他插件内置演示能力仍属宿主管理，不自动卸载或改写。

新会话才可能载入更新后的技能目录；当前会话中已展开的旧指令不会因改文件自动消失。检查磁盘入口、宿主实际目录与任务行为是三个不同层次。

## 维护与发布

`requirements-analysis` 的维护和用户级分发由 workflow-manager 完成；本仓不提供同步命令。执行计划只在 dev-flow 项目目录中使用，不经本仓同步。

本地应用、恢复或检查不自动提交。用户明确要求发布后，先审阅并只暂存本次文件，再运行 `bash scripts/sync.sh --publish-staged "提交说明"`；只推送当前分支，不强制推到 main。
