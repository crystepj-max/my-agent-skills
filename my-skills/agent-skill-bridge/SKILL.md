---
name: agent-skill-bridge
description: 统一管理多个 AI agent（claude / codex / workbuddy 等）的第三方 skill 安装流程——安全审计 + 安装到公共池 ~/.agents/skills/ + 中文化（把英文/空 description 译为中文，提升 "/" 命令可读性）+ 软链桥接到各 agent 默认目录 + 校验每个 agent 对同一 skill 只保留 1 份（去重）。当用户的意图涉及——安装新的第三方 skill、统一 skill 入口、让多个 agent 共享/复用 skill、把某 agent 的 skill 同步到其他 agent、避免各 agent skill 重复维护、清理同名 skill 冲突、对每个 agent 做 skill 去重、把 skill 描述中文化/翻译成中文、或提到 ~/.agents/skills 这个公共池——务必使用本 skill；即使对方只说"让 codex 也能用 claude 的 skill"、"统一一下各 agent 的技能"、"装个新 skill 给其他 agent 也能用"、"去重一下各 agent 的 skill" 或 "把 skill 描述翻译成中文" 也应触发。
agent_created: true
---

# 多 Agent 第三方 Skill 统一安装流水线

把第三方 skill 安全地接入多 agent 环境。每个新 skill 都必须走完下面六步，缺一不可：

**安全审计 → 安装到公共池 → 中文化 → 软链桥接 → 校验 agent 去重 → 同步回 GitHub**

## 核心概念

- **公共池（真源）**：`~/.agents/skills/<skill>/`，每个 skill 一个目录带 `SKILL.md`。所有 agent 共享同一份。
- **桥接目标**：各 agent 默认的 user-level skill 目录，例如 `~/.claude/skills/`、`~/.codex/skills/`、`~/.workbuddy/skills/`。
- **机制**：agent 各自只扫描自己硬编码的目录，不会原生发现 `~/.agents/skills/`。唯一通用办法是在各自目录里放**指向真源的软链接**（Claude/Codex/WorkBuddy 均 follow 自己目录内的软链）。
- **去重原则**：每个 agent 对同一 skill 名字只应保留 1 份——即 `~/.agent/skills/<name>` 里那条指向公共池的软链。其它发现路径（命令 .md、插件副本）若同名即视为重复。

## 四条规则（用户确认版，必须严格遵守）

1. **插件型 skill 不碰**：不碰 `installed_plugins.json`、`config.toml [plugins.*]`、marketplaces 缓存。脚本只扫 agent 主 skill 目录与 commands，天然不碰插件体系（插件内重复靠卸载插件解决，见第 4 步）。
2. **agent 默认路径 / 独有 skill 不碰**：不挪目录、不动 agent 独有（公共池无同名）的 skill。容器不动，只替换与公共池重名的"内容"。
3. **公共池靠软链桥接**：公共池有的、agent 目录没有的 → 建软链。
4. **同名冲突 → 删 agent 副本、改用公共池**：agent 目录已有同名（无论实体还是别处软链）→ 先备份再删除，改指公共池。

> 规则 2 与规则 4 在"同名"上冲突：**规则 4 优先级更高**——名字撞到公共池的，就地替换成软链。

> **例外：同名不同物 → 改名并存（第三条路）**。规则 4 的前提是"同名即同一个 skill 的不同副本"。若比对后确认两者**功能不同、都有价值**（如 `llm-wiki`：Hermes 自带的是"手搓互链知识库"方法论，新装的是某桌面应用的 API 契约文档），机械替换会造成有效资产丢失。此时应给用户选项，推荐**新装的那份改名进池**（目录名 + frontmatter `name` 同步改，如 `llm-wiki-app`），旧的保留原名。判定手法：`cmp` 逐文件比对 + 读两边 frontmatter 的 `description`/`author`/`version`，**不要只看目录名就判定为副本**。

---

## 第 0 步：安全审计（装任何第三方 skill 之前必做）

对要安装的第三方 skill（其 `SKILL.md` 及 `scripts/`、`references/`、`assets/` 所有文件）跑安全审计：

- 调用 **`skills-security-check`** skill 加载审计流程，按它的清单逐项检查（外部请求、危险命令、凭证读取、隐式执行等）。
- 判定风险等级：
  - **P0**：强烈警告，要求用户显式确认才装。
  - **P1**：警告并要求确认。
  - **P2**：安全，正常安装。
- 审计结论先报给用户，再进入第 1 步。

## 第 1 步：安装到指定文件夹（公共池）

把审计通过的 skill 安装到公共池真源目录：

```sh
# 示例：从 git 仓库安装 mattpocock/skills 里的某个 skill
git clone --depth 1 <repo-url> /tmp/_skill_src
# 把其中的 <skill>/ 目录（含 SKILL.md）整体放入公共池
cp -R /tmp/_skill_src/<skill> ~/.agents/skills/<skill>
```

- 目标目录必须是 `~/.agents/skills/<skill>/`，且含 `SKILL.md`。
- 记得 `rm -rf <目标>/.git`，别把仓库元数据带进池。
- 安装后**立刻跑第 2、3、4、5 步**；不要只装不桥接。

**装前两项前置核验（省得装完发现是摆设）：**

1. **依赖的本机应用/服务是否真的存在且在跑**。很多 skill 是某个本地服务的接口说明书，服务没装等于白装。核验手法：`pgrep -fl -i <关键词>`、`lsof -nP -iTCP:<端口> -sTCP:LISTEN`、`ls -d /Applications/*<关键词>*`。若服务有免鉴权健康检查接口，直接探一次拿到**鉴权状态与版本号**——能提前发现「token 未配置，所有接口 401」这类装完即不可用的情况，以及「skill 文档标注适配 v0.4，本机已是 v0.6」的接口漂移风险。
2. **跨全部 agent 做重名碰撞检查**（含 hermes 递归子目录、openclaw 各 workspace）：
   ```sh
   for d in ~/.claude/skills ~/.codex/skills ~/.workbuddy/skills ~/.openclaw/skills ~/.hermes/skills; do
     find "$d" -maxdepth 2 -iname "*<关键词>*"
   done
   ```
   有碰撞先按上面「同名不同物」判定，再决定替换还是改名。

### 第 1b 步：把已锁在单个 agent 里的通用 skill 提升进池（promote）

场景：某个通用 skill 当初只装在 `~/.codex/skills/` 或 `~/.workbuddy/skills/` 下，其它 agent 用不到。用 `promote` 把它**移动**进公共池，原位置自动换成软链——一次操作，全 agent 共享。

```sh
# 只读规划：检查哪些可提升、有无与池同名冲突
python3 <skill>/scripts/bridge.py --mode promote \
  --agents codex,workbuddy --names skillA,skillB

# 实际执行（自动备份到 ~/.agents/skill-bridge-backups/promote/<日期>/）
python3 <skill>/scripts/bridge.py --mode promote --fix \
  --agents codex,workbuddy --names skillA,skillB
```

**提升前必做重名碰撞检查**：把「提升后池名单」与所有待桥接 agent（尤其 hermes 递归子目录、openclaw 各 workspace）的现有 skill 名求交集，交集非空就先跟用户确认取舍，别直接覆盖。

> 提升进池后**必须重跑第 2 步中文化**——被提升的 skill 可能是英文描述，进池即被全 agent 看见。

## 第 2 步：中文化（把英文 / 空 description 译为中文）

第三方 skill 的 `description` 多为英文，导致在 agent 里打 `/` + skill 命令时看不懂它是干啥的。统一在装完池后做中文化，让三个 agent 经软链同步看到中文。

```sh
# 只读报告：列出所有自有 skill 中仍为英文主导 / 空的 description，并标注可自动归一化的中英夹杂项
python3 <skill>/scripts/bridge.py --mode cn

# 实际修复：自动归一化中英夹杂项（如剥 'AI Berkshire skill:' 前缀、'Source:'→'来源：'）并写入；
#          列出仍需 LLM 翻译的纯英文项
python3 <skill>/scripts/bridge.py --mode cn --fix
```

处理逻辑（`--mode cn`）：
- **自动归一化（确定性，可 `--fix` 写入）**：中英夹杂但中文为主的描述，剥掉英文前缀（如 `AI Berkshire skill:`）并把 `Source: skills/...` 改为 `。来源：skills/...`，归一化为纯中文。
- **需 LLM 翻译（脚本不自动写）**：纯英文主导或空的 `description`。`--fix` 只**报告**这些项（含路径），由 agent 用 **Edit** 工具逐条写入中文翻译。
- 写入前自动备份到 `~/.agents/skill-bridge-backups/cn/<日期>/`。
- 范围：**公共池全集 + WorkBuddy 原生（非软链）skill**。**53 个 Claude 插件 skill 受规则 1 约束不在范围内**（插件更新会覆盖，需另处理）。

闭环操作：先跑 `--mode cn --fix`（自动归一化 + 列出纯英文项）→ 用 Edit 把列出的纯英文项译为中文 → 重跑 `--mode cn` 直到「需 LLM 翻译」计数归零。

**日常守护脚本 `cn_guard.sh`**（A 方案落地）：把上面的闭环封装成「更新/重装 skill 后的强制收尾」一键命令。从上游重新 clone/pull 覆盖了公共池后，跑 `bash scripts/cn_guard.sh` 即可自动归一化并校验「需 LLM 翻译」计数是否归零，未归零会列出待翻译清单。任何重拉/重装动作后必跑。

## 第 3 步：软链桥接（dry → apply → verify）

### 3a. dry-run 只读规划（永远先跑，不改动任何东西）

```sh
python3 <skill>/scripts/bridge.py --mode dry
```

输出给每个 agent 列出 `[ADD 软链]` / `[REPLACE 删副本]` / `[已正确,跳过]`，最后用"规则2 校验"列出各 agent 将保持不动的独有 skill。**把这份映射念给用户确认**，尤其关注 REPLACE 项。

### 3b. apply 执行（仅在用户确认后）

```sh
python3 <skill>/scripts/bridge.py --mode apply
```

- 冲突副本先自动备份到 `~/.agents/skill-bridge-backups/<agent>/<name>/`，再删除并建链。已备份的不重复备份。
- 幂等：已正确链接的跳过。执行完自动跑 verify。

> 安全门控：唯一"删除"操作都是先备份后删，可回滚。若用户要求硬删不留备份，需显式确认。

### 3c. verify 校验

```sh
python3 <skill>/scripts/bridge.py --mode verify
```

确认每个 agent 对公共池 **0 缺失、0 断链**。

## 第 4 步：校验 agent 去重（dedup）

确保**每个 agent 对同一 skill 名字只保留 1 份**（指向公共池的软链）。

```sh
# 只读报告：列出每个 agent 的发现路径里同名 skill 的重复项
python3 <skill>/scripts/bridge.py --mode dedup

# 实际修复：移除可安全删除的重复项（命令 .md / 非池软链），先备份
python3 <skill>/scripts/bridge.py --mode dedup --fix
```

去重扫描覆盖一个 agent 的全部 skill 发现路径：

- `~/.agent/skills/`（含软链）—— 真源软链在此。
- `~/.claude/commands/*.md`（仅 claude；命令与 skill 同命名空间，同名即重复）。
- `~/.claude/plugins/**/SKILL.md`（仅 claude；插件体系）。

判定逻辑：

- 某 skill 名字如果有**指向公共池的真源软链**：其余同名条目（命令 `.md`、 skills 目录内未指向池的软链/目录）会被 `--fix` 自动移除（先备份）。**插件副本只报告、不自动删**（避免破坏插件体系）。
- 某 skill 名字如果**没有公共池真源**（纯插件内部重复 / agent 独有）：只报告、不自动删。插件内部重复 → 提示用户卸载对应插件；agent 独有 skill → 按规则 2 保留。

> codex / workbuddy 当前无 commands / plugins 重复风险，只扫各自 skills 目录；如发现同名软链冲突也会被 `--fix` 修复。

---

## 第 5 步：同步回 GitHub（自动回传）

让「本地改动」与集中管理仓库保持一致（公开仓库 `crystepj-max/my-agent-skills`），支撑跨设备快速恢复。仓库同时存**自有 skill 完整数据**（仅 `my-skills/`，第三方只存元数据清单，不囤数据）。

触发方式：

- **自动**：`apply` / `cn --fix` / `dedup --fix` 成功后自动执行（除非传 `--no-sync`）。
- **手动**：`python3 <skill>/scripts/bridge.py --mode sync`

`run_sync()` 依次做三件事：

1. 复制自有 skill `agent-skill-bridge` 当前真源 → 仓库 `my-skills/agent-skill-bridge/`（自动排除 `__pycache__` 等）。
2. 运行 `scripts/refresh_inventory.py` 刷新 `inventory/skill-desc-translation.md` 的「最新更新」列（按各仓库 `pushed_at`）。
3. 运行 `scripts/sync.sh` 提交并推送 `main`（`sync.sh` 仅在确有变更时提交，无变更自动跳过）。

> 仓库位置优先取活跃工作区 `~/workspace/my-agent-skills`（日常开发提交都在这里），不存在时才退回 `~/my-agent-skills`。若两者都不是 git 仓库，自动跳过同步、不影响本地。

---

## 工作流串起来（安装一个新第三方 skill 的标准动作）

```
1. skills-security-check 审计目标 skill            # 第 0 步
2. cp -R <skill> ~/.agents/skills/<skill>          # 第 1 步：安装到公共池
2b. bridge.py --mode promote --fix --agents .. --names ..   # 第 1b 步（可选）：提升 agent 专属 skill 进池
3. bridge.py --mode cn --fix  -> 对列出的纯英文项用 Edit 译中文 -> 重跑直到归零   # 第 2 步：中文化
3b. bash scripts/cn_guard.sh   # 日后任何『重拉/重装 skill』后的强制收尾（A 方案：更新-翻译一条龙守护）
4. bridge.py --mode dry      -> 用户确认           # 第 3a 步
5. bridge.py --mode apply     (含自动 verify + 自动同步回 GitHub)   # 第 3b/c 步：桥接
6. bridge.py --mode dedup --fix                     # 第 4 步：去重（--fix 也会自动同步；--no-sync 可关闭回传）
```

**全量梳理场景**（用户说"梳理本机所有 agent 的 skill"）额外前置：先只读盘点全机 skill 容器（`find ~ -name SKILL.md`，排除 node_modules / Library / plugins），按 agent 归类统计「实体 vs 软链」，用 realpath 做异源重复分析，**把方案选项摆给用户确认收拢范围后再动手**。

## 扩展

- **加 agent**：编辑脚本里 `DEFAULT_AGENTS`，加一行 `"<name>": os.path.expanduser("~/.<agent>/skills")`，再用 `--agents <name>` 调用。未知 agent 名会被跳过并提示。
- **项目级池**：约定 `<project>/.agents/skills/`。当前脚本聚焦用户级；项目级做法是堆一版指向项目池的软链（同样走 dry→apply→verify→dedup），按需扩展。

### 本机 agent 加载约定实测表（2026-08-03 核验）

| Agent | skill 加载目录 | 是否需桥接 |
|---|---|---|
| **kimi**（kimi-code） | 二进制内 `USER_GENERIC_DIRS = [".agents/skills"]` | ❌ **原生直读公共池，零操作** |
| **opencode** | 官方文档明写 `~/.agents/skills/<name>/SKILL.md` 自动加载 | ❌ **原生直读公共池，零操作** |
| claude | `~/.claude/skills` | ✅ 已桥接 |
| codex | `~/.codex/skills`（`.system/` 为官方内置，升级会重建，**不碰**） | ✅ 已桥接 |
| workbuddy | `~/.workbuddy/skills` | ✅ 已桥接 |
| openclaw | 源码 `join(agentDir,"skills")` → `~/.openclaw/skills`；另有 workspace 级隔离池（`~/.openclaw/<workspace>/skills`，**不动**） | ✅ 已桥接 |
| hermes | `~/hermes-agent/tools/skills_hub.py` 里 `SKILLS_DIR = ~/.hermes/skills`；原生是**分类子目录**结构（aihot/buffett/... 36 类、约 130 个），池软链平铺在顶层与之共存 | ✅ 已桥接 |

> 判定手法：二进制用 `strings -a <bin> | grep -i skill` 找路径常量；源码型 agent 直接 grep `SKILLS_DIR` / `join(...,"skills")`。**不要凭空建目录**，先确认加载约定。

## 已知坑（务必提醒用户）

1. **插件型 skill 覆盖不到**：插件是另一套发现机制，软链桥接管不了，得分别在各自体系里 enable；插件内同名重复要靠卸载插件解决（本 skill 的 dedup 只报告，不自动删插件副本）。
2. **同名/异源 skill**：同名但内容不同的（如某 agent 自带一份 baoyu-image-gen），按规则 4 备份后改用公共池副本；务必让用户知道他丢的是哪份、备份在哪。
3. **运行时是否 follow 软链需分别验证**：文件系统层软链正确 ≠ agent 运行时真的加载。Claude 已实测可加载；Codex/WorkBuddy 建议各跑一次 skill 列表确认，若哪个不跟软链，需单独处理。
4. **name 冲突定位**：用 realpath 比对，不要靠目录名（会有同名不同源的软链），否则会误判。
5. **cc-switch 聚合视图会"虚高"**：cc-switch 同时扫描公共池 + 各 agent 软链，同一个 skill 会被计成多份（池 1 + 每个 agent 软链 1）。这是聚合视图的显示特性，不是真有 N 份文件；真源只有公共池那 1 份。
6. **SKILL.md 可能带非 UTF-8 字节，会让 cn 模式报「解析错误」**：实测 `dataclaw/SKILL.md` 混入 Big5 残留 `\xa1\xaa`(应为 `—`, 17 处) 与 `\xa1\xfa`(应为 `→`, 5 处)，Python 以 utf-8 打开直接抛 `UnicodeDecodeError`。处理套路：以 **bytes 方式**读入 → 逐字节定位非 UTF-8 序列并打印上下文 → `s.decode('big5')` 反推原字符 → `raw.replace()` 修复 → 再 `decode('utf-8')` 校验 → 然后才做描述替换。**别用文本模式硬读，也别 `errors='ignore'`（会静默丢字符）。**
7. **英文判定会误伤技术名词密集的中文描述**：`has_english_sentence` 原按「≥4 个连续英文单词」判定，`clashx-openai-sse-debug` 这类中文描述里塞满 `ClashX Pro / OpenAI SSE / TUN` 的会被误判为英文。现已改为**先算 CJK 占比，中文占主导则直接判定为已中文**。若再遇假阳性，优先改判定逻辑，不要去改描述迁就脚本。
8. **中文化/改描述后需重启 agent 会话才生效**：agent 在会话启动时把 skill 列表读进内存缓存，改完磁盘描述后，**当前会话不会自动刷新**。Claude Code / WorkBuddy / Codex 都需新开（或重启）会话，打 `/` 才会显示更新后的中文描述。验证可直接读磁盘文件确认已改，不依赖会话内显示。

## 回滚

- 撤某 agent 桥接：删对应软链即可（`rm ~/.codex/skills/lark-approval` 等）。
- 还原被 replace 的 agent 副本：从 `~/.agents/skill-bridge-backups/<agent>/<name>` 复制回去。
- 还原被 dedup 删掉的命令 .md：从 `~/.agents/skill-bridge-backups/dedup-commands/<agent>/<name>.md` 复制回去。
