---
name: agent-cli-tool-residue-purge
description: "当 AI 编程 CLI（Claude Code、Codex、Gemini CLI 等）在某个辅助/代理/包装工具被卸载后开始报错时使用——例如 SessionStart:startup hook error、每次 Bash 调用都 command not found、或 CLI 静默指向已失效的 localhost 端口。提供跨所有配置层（settings 文件、MCP 注册表、hooks、shell rc、launchd、cron）的全面排查与清理流程，确保不留任何陈旧引用。关键词：headroom、hook error、卸载残留、proxy 残留、ANTHROPIC_BASE_URL、OPENAI_BASE_URL、mcpServers。"
---

# AI CLI 工具残留清理

## 用途

某个辅助工具（本地代理 / hook 注入器 / MCP 服务 / token 优化器）被删除后，AI CLI 仍反复报错。
典型症状：

- `SessionStart:startup hook error` → `<path>: No such file or directory`
- 每次 Bash 调用打一行 `command not found` warning
- CLI 完全连不上模型（被指向一个已经没有监听的 localhost 端口）
- MCP server 启动失败

根因：这类工具可能写入多个宿主的多层配置，卸载脚本可能只清一部分。先证明目标工具与残留的关联，分清用户配置与工具自身数据；不扫描凭据、密钥库或不相关文件。

## 核心原则（按顺序，别跳）

### 1. 先找部署清单；默认只读调查 🔴 最重要

这类工具通常在自己的数据目录里留有部署记录，直接列出所有被它改过的宿主：

```bash
# 常见位置
cat ~/.<tool>/deploy/*/manifest.json
cat ~/.<tool>/*install*.json
ls ~/.<tool>/
```

重点看 `targets` / `tool_envs` / `mutations` / `artifacts` 字段。

**经验**：部署清单可能列出多个宿主。清理前先保存清单副本并按清单逐项核实，避免删除目录后失去追踪线索。

**注意**：清单可能"言过其实" —— 声明要改的地方不一定真落地（实测 codex 的
`config.toml` 就没被注入）。清单用来**确定搜索范围**，实际是否存在必须逐个核实。

### 2. 配置分层，只看主配置会漏项

**Claude Code 三层**：

| 文件 | 内容 | 优先级 |
|---|---|---|
| `~/.claude/settings.json` | 主配置：env / hooks / permissions | 低 |
| `~/.claude/settings.local.json` | 本地覆盖，**同名字段压过主配置** | **高** |
| `~/.claude.json` | `mcpServers` 注册表（不在 .claude/ 目录里） | — |

**Codex**：先依据本机当前安装版本的官方文档与实际配置发现位置；不要把历史配置路径当成固定契约。只读检查 `~/.codex/config.toml` 等与本次残留直接相关的配置。

### 3. env 污染比 hook 报错危险得多 🟡

hook 报错是"非阻塞 warning"，吵但不致命。
真正致命的是 `settings.local.json` 里的：

```json
"env": { "ANTHROPIC_BASE_URL": "http://127.0.0.1:8787" }
```

代理程序已删 → 端口无监听 → 而 local 层优先级最高 → **CLI 彻底连不上模型**。
排查时务必 `lsof -i :<port>` 确认端口死活。

对应 codex 侧是 `OPENAI_BASE_URL`。

### 4. 连带失效的依赖要一并处理

被删工具常通过 PATH 注入方式提供其他二进制。工具没了，PATH 也没了，
依赖这些二进制的**其他 hook 会跟着失效**（如依赖 `rtk` 的 `rtk-rewrite.sh`）。

`command -v <dep>` 与部署清单交叉核对后，说明缺失依赖会影响哪些 hook。不要为了恢复一个功能而移动二进制或改写 hook；先给出方案，按用户授权的范围逐项处理。

## 执行流程

### 阶段一：确定范围并只读扫描

先从故障信息、被卸载工具的名称和部署清单选出可能受影响的宿主。只查这些宿主的运行入口；不扫描 `.env`、keychain、登录状态、浏览器资料或其他凭据目录。检索时按字面匹配，并且只列出命中文件路径，不把整行配置或命令参数输出到对话。

```bash
TARGET_TOOL="headroom"  # 按本轮目标替换
for f in ~/.zshrc ~/.bashrc ~/.bash_profile ~/.profile ~/.zprofile ~/.zshenv; do
  [ -f "$f" ] && rg -l -F -- "$TARGET_TOOL" "$f" 2>/dev/null
done

# 仅在部署清单或错误信息指向 launchd / cron 时检查
rg -l -F -- "$TARGET_TOOL" "$HOME/Library/LaunchAgents" /Library/LaunchAgents /Library/LaunchDaemons 2>/dev/null

# 仅列出相关配置文件，不输出可能包含 secret 的整行
rg -l -F -- "$TARGET_TOOL" ~/.claude/settings.json ~/.claude/settings.local.json \
  ~/.claude.json ~/.codex/config.toml 2>/dev/null

command -v -- "$TARGET_TOOL"
ls -ld -- "$HOME/.$TARGET_TOOL" "$HOME/.config/$TARGET_TOOL" 2>/dev/null
```

只在进程本身与报错相关时核对进程名。对于命中文件，只读检查最小相关键名、hook 名称、MCP server 名称和路径；任何 `env`、token、secret、password、key、授权头或 URL 查询参数的值都不要读取、复制或回显。

### 阶段二：核对安装清单和实际生效位置

查找工具自己的 `manifest.json`、安装记录和 uninstall 文档，先确认文件存在。只读取 `targets`、`mutations`、`artifacts` 等必要字段；忽略并遮盖认证、环境变量和凭据字段。清单描述只是线索，逐一核实它列出的目标当前是否存在、是否生效。

Claude Code 的主设置、本地覆盖、用户 MCP 注册表可能分别保存配置；确认当前版本实际读取哪些文件。Codex 与其他 CLI 的配置位置按本机当前版本文档和实际路径核对，不假设历史路径仍是契约。若 CLI 的 URL 指向 localhost，优先确认监听端口是否存在，只检查地址/端口，不输出 URL 中的凭据。

### 阶段三：准备可恢复快照

只备份本次确需修改且存在的配置文件和工具清单。将副本放在发现目录与 Git 仓库之外，保留相对路径、权限和符号链接，并生成逐文件 SHA-256 清单。敏感文件快照不得被打印或纳入报告。先呈现备份范围和预计变更路径。

### 阶段四：准备并审阅最小差异

逐条列出候选残留、证据、受影响 host、预期行为和恢复方法。默认生成修改草案，不写配置。用户明确授权具体配置路径和清理内容后，才按授权范围修改：

- 只移除已确认属于目标工具的 hook 或 MCP 条目，保留同一数组/对象里的其他工具；
- 空 hook 事件块可一并移除，避免留下无效空配置；
- 对 JSON/TOML 使用结构化解析器，保留未知键和格式；不要做全局文本替换；
- 修复 `ANTHROPIC_BASE_URL`、`OPENAI_BASE_URL` 等路由时只改对应键；不显示完整 URL 中可能包含的敏感参数；
- 若依赖二进制实际缺失，给出恢复或摘除 hook 的选项，不擅自安装、移动其他工具或改写非目标配置。

写入后展示仅含非敏感字段的精确 diff，重新解析文件并确认未授权字段没有变化。

### 阶段五：归档工具数据

工具自己的数据目录可能包含用户状态或恢复所需信息。删除/移动前核对准确路径、内容类型、大小和备份 hash，说明影响并等到用户明确授权该目录及归档方式。优先放入用户指定的仓外参考归档；如果选择废纸篓，使用当前系统支持的回收方式，检查目标路径不会覆盖已有内容。不要用删除命令或脚本绕过用户授权，也不要把特定机器遇到的沙箱错误当作普遍规则。

### 阶段六：验证并交付

对本轮修改过的配置重新解析，再用阶段一的**目标限定范围**复查。残留如果是注释、历史记录、备份或无关单词，应说明并保留，不以“零命中”为目标。列出修改和归档路径、每项恢复方法、验证命令与仍需用户在日常环境确认的 CLI。静态检查不能代替真实启动验证。

## 误报识别

宽泛搜索会产生无关匹配。先按字面目标定位，再逐条核实命中是否是当前运行入口：

| 误报模式 | 说明 |
|---|---|
| 英文单词本身 | `headroom` = 余量，常见于代码注释 `~25% headroom` |
| 端口号撞车 | `8787` 是 **Cloudflare wrangler 默认端口**，会在 skills / 文档目录大量命中 |
| 备份与历史 | `backups/`、`*.bak`、历史日志、sessions 里的引用通常不是运行入口，先核实用途再保留 |
| 二进制文件 | `Binary file ... matches`（如 sqlite-wal）忽略 |

## 检查清单

- [ ] 已把本次目标限定为有故障/部署证据的 host 和入口
- [ ] 未扫描凭据、keychain、`.env`、浏览器资料或认证目录
- [ ] 按部署清单核实目标路径；敏感值已遮盖
- [ ] 区分当前运行配置与注释、历史、备份和示例
- [ ] 已列出每个候选改动和准确恢复路径
- [ ] 只修改用户明确授权的配置路径与内容
- [ ] 保留同一设置内无关 hook/MCP 及其他 agent 的配置
- [ ] 工具数据目录只在精确授权后归档并记录 hash
- [ ] 解析实际修改过的配置格式
- [ ] 用户最终启动受影响 CLI 验证模型连接和 hooks
