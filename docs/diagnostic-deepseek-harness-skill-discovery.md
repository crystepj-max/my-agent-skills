# dsh（DeepSeek Harness）技能加载机制 — 确认报告（终版）

> 📌 **计数更新（2026-08-25）**：本文原写就于 2026-08-16，彼时公共池含 78 个技能。截至本次更新，dsh 实际识别的技能数（含说明文件的一级技能目录）已刷新为 **85** 个，公共池一级条目共 **86** 个（其中 1 个为不含说明文件的目录，dsh 不识别）。自 8/16 以来新增/变动的技能：`dev-workflow-2-0`、`eli5`、`grill-with-docs`、`remotion-video-production`、`to-questionnaire`、`to-tickets`、`triage`、`video-production`、`wait-what`、`wayfinder`、`wizard`（共 11 项）。正文计数已同步刷新，机制结论不变。

> 背景：用户观察到 dsh「新建的 requirements-analysis 被识别、其余技能未识别」。
> 经排查 + 用户确认运行环境后，结论已收敛为「机制确认」而非「故障定位」——
> dsh 现运行于本机 Mac mini、已正常识别全部技能。本报告只回答核心问题：
> **dsh 到底用什么方式读取并加载 skill？**

## 一、直接结论

🔴 **dsh 是「直接扫描根目录 + 就地读 SKILL.md」，不依赖软链接、也不复制技能到自己目录。**

具体地说：dsh 把 `~/.agents/skills`（你的公共池、单一真源）当作默认扫描根之一，
遍历其中的每个条目、就地读取其 `SKILL.md` 并解析 frontmatter。它既不是通过
「软链接桥接」加载（那是 Claude/Codex/WorkBuddy 那套 agent 目录的用法），也不是
「拷贝式」加载。

## 二、三个子问题的逐一回答

### Q1：是读取 `~/.agents/skills` 吗？
✅ **是，且是直接读取。**
代码铁证 `dsh-skill-filesystem/lib/index.js:177-180`：
```js
roots.push({
  path: join(this.agentsHome, "skills"),   // = ~/.agents/skills
  source: "user-agents",                   // 来源标记
  rank: USER_AGENTS_RANK
});
```
`agentsHome` 默认 = `~/.agents`（`index.js:78`，除非被 `DSH_AGENTS_HOME` 或配置覆盖）。
`includeDefaultRoots` 默认 `true`（`index.js:33/76`），故该根始终被扫描。

### Q2：是采用软链接方式吗？
🔶 **否，dsh 自身不强依赖软链；但它「会跟随软链接」。**
- dsh **不要求**技能是软链，也不会把技能软链到自己目录。
- 但其扫描器 `nodeEntryKind()` 对条目先用 `lstat` 再 `stat`（穿透软链），
  所以**若扫描根里某个技能本身是软链指向真实目录，它照样被识别**——
  这是健壮性设计，不是加载必需环节。
- 你的公共池 `~/.agents/skills` 里 86 个一级条目（其中 85 个为含说明文件的真实技能目录），软链无关紧要。

> 对照实验（临时 agentsHome，未触碰真实 `~/.agents/skills`）：
> 同时放入「真实目录技能」与「指向它的软链技能」，dsh 均识别（source 均为 `user-agents`）。
> 证明：DSH 跟随软链，但不依赖软链。

### Q3：还有其他加载方式吗？
dsh 的扫描根不止 `~/.agents/skills`，完整清单（`index.js:150-188`）：

| 来源标记 | 扫描根 | 本机状态 |
|---|---|---|
| `project-dsh` | `<cwd 推导的项目根>/.dsh/skills` | 按会话 cwd，本次为空 |
| `project-agents` | `<项目根>/.agents/skills` | 按会话 cwd，本次为空 |
| `custom` | `customSkillDirs`（agent 预设附加） | 默认仅框架自带 2 个 cordis 技能 |
| `user-dsh` | `~/.dsh/skills` | **本机不存在，为空** |
| **`user-agents`** | **`~/.agents/skills`** | **本次 85 个技能全部来自此根** |
| `bundled` | 框架内置技能目录（`DSH_BUNDLED_SKILL_DIR`） | 框架自带，非用户技能 |

## 三、实测验证（决定性）

用真实 `dsh-skill-filesystem` 包在进程内执行发现逻辑（`agentsHome=/Users/chris/.agents`，
`cwd=/Users/chris/workspace/my-agent-skills`）：

```
发现候选总数: 85
按来源根(source)分组:
  [user-agents] 85 个        <-- 全部来自 ~/.agents/skills

代表性路径:
  user-agents  agent-cli-tool-residue-purge  <- /Users/chris/.agents/skills/agent-cli-tool-residue-purge
  user-agents  agent-skill-bridge            <- /Users/chris/.agents/skills/agent-skill-bridge

requirements-analysis -> source=user-agents, dir=/Users/chris/.agents/skills/requirements-analysis
code-review           -> source=user-agents, dir=/Users/chris/.agents/skills/code-review
tdd                   -> source=user-agents, dir=/Users/chris/.agents/skills/tdd
```

**结论：requirements-analysis 与其余 85 个老技能，全部从同一个根 `~/.agents/skills` 被读出来，
路径一致、机制一致。没有任何「区别对待」。**

## 四、对你的 agent-skill-bridge 架构的含义（好消息）

你的「单一真源 = `~/.agents/skills`（公共池）」设计，**与 dsh 天然兼容**：
- dsh 直接读公共池，无需为 dsh 单独桥接（不像 Claude/Codex 需要软链到 `~/.claude/skills` 等）。
- 你在公共池新增/修改任一技能，dsh 下次扫描即生效（受文件监听 `watchManager` 自动刷新）。
- 唯一要注意：dsh 不扫 `~/.workbuddy/skills` 这类「agent 专属软链目录」，
  所以给 dsh 配技能**只动公共池**即可，不要指望软链桥接生效。

## 五、是否需要进一步操作

- ✅ 无需修复：发现机制本就正常，dsh 现正常识别全部 85 个技能。
- 若未来想把「项目级私有技能」暴露给 dsh：在项目根建 `.agents/skills/` 或 `.dsh/skills/`
  放入技能即可（按会话 cwd 自动被 `project-agents`/`project-dsh` 根扫描）。
- 若担心默认根被覆盖：检查 `DSH_AGENTS_HOME` 环境变量与 `~/.dsh/settings.yaml`
  是否设了 `agentsHome`/`customSkillDirs`（当前均默认，无覆盖）。
