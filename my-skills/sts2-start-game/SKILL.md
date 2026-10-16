---
name: sts2-start-game
description: "当本机 STS2 工作需要启动游戏、检查 STS2-Agent 接口，或安全恢复残留会话时使用。启动成功要求同一主机上下文中的 /health、/state、/actions/available 三个 HTTP 端点均可用。"
---

# STS2 启动与 Agent 接口就绪

此技能面向 macOS 本机的 Slay the Spire 2 与游戏内 STS2-Agent。判定目标是可用的 Agent 接口，不是只看进程已启动或诊断命令成功。

## 就绪标准

- STS2-Agent 随游戏加载；它不是应先单独启动的服务。
- 启动成功要求同一主机 shell 对 GET /health、GET /state、GET /actions/available 都成功。
- sts2 ping 仅作诊断，不能单独证明就绪。
- 接口就绪不代表场景就绪。功能或战斗测试还需读取 /state 并确认目标场景；MAIN_MENU 只证明接口可用。

## 执行流程

1. 找到本技能包根目录，也就是包含本 SKILL.md 的目录；将该目录记为 SKILL_DIR。不要从项目当前工作目录推导技能脚本位置。
2. 确认没有另一个自动化驱动正在操作同一游戏。若项目定义了会话互斥机制，按项目约定确认所有权；不确定时先停下，不要并发发送动作。
3. 执行同包脚本：

~~~bash
SKILL_DIR="/已安装技能目录/sts2-start-game"
bash "$SKILL_DIR/scripts/start_sts2.sh" --timeout 180
~~~

当前机器的安装示例目录是 /Users/chris/.agents/skills/sts2-start-game。若技能通过其他位置安装，将 SKILL_DIR 改为该实际目录。仓库根目录的 start_sts2.sh 只是兼容薄包装器，会转调同包 scripts/start_sts2.sh。

4. 脚本先探测三个接口；已有接口可用时复用当前会话。游戏进程仍在加载时，最多等待 --ready-grace 指定的时间。进程存在但接口仍不可用时，脚本会报告状态并退出，不会自动发送信号或重启。
5. 若脚本报告监听端口，lsof 输出只用于找到候选进程。先核对 PID、命令行和可执行文件路径确为 SlayTheSpire2.app，再按项目流程确认没有并行驱动或其他会话使用者；端口归属本身不证明进程身份，也不是可直接传给 kill 的目标。可用以下只读命令核验候选 PID：

~~~bash
PID="<lsof 输出的候选 PID>"
ps -p "$PID" -o pid=,ppid=,comm=,command=
lsof -a -p "$PID" -d txt -Fn
~~~
6. 如任务确需重开游戏，优先在游戏界面正常退出，或在确认目标应用身份和互斥状态后用 macOS 正常退出，再等待进程与监听端口释放。若任务已授权重开当前游戏，这份授权在目标和风险范围未实质变化时覆盖必要的 TERM/KILL 升级，不因信号变化重复询问。只有正常退出已尝试且无效、确切 PID 的命令行与可执行文件身份复核无误、没有其他会话使用者、并确认仍有必要时，才向该 PID 发送 TERM 并进行有界等待；若仍未退出，须再次核实同一 PID 身份、无其他会话和升级必要性，然后才可在原授权范围内向该 PID 发送 KILL。若 PID/对象、授权目的或风险发生实质变化，先确认变化；绝不依据 lsof 的结果直接 kill -9。
7. 需要判断 Steam 启动失败时，可检查：
   - ~/Library/Application Support/Steam/logs/gameprocess_log.txt
   - ~/Library/Application Support/Steam/logs/console_log.txt

## 参数

- --timeout <seconds>：接口总等待预算，默认 180。
- --app-id <id>：Steam app ID，默认 2868840。
- --agent-url <url>：Agent 基地址，默认 http://127.0.0.1:8080。自动启动前需能检查其本机监听端口；非回环地址无法通过本机 lsof 完成安全核验，脚本会失败关闭。
- --ready-grace <seconds>：已有游戏进程处于加载状态时的额外等待时间，默认 30。

## 成功与失败判定

成功必须同时满足 GET /health、GET /state、GET /actions/available。报告时还要区分：

- 接口未就绪：三端点至少一个失败。
- 探测上下文受限：主机 shell 可访问但当前沙箱不可访问；先换到主机上下文，不要据此重启游戏。
- 场景未就绪：接口可用，但 /state 尚未到目标场景。
- 监听身份待核验：lsof 找到本机监听者；脚本不会把该 PID 当成游戏，也不会向它发送信号。
- 环境或游戏启动失败：在接口超时且检查 Steam 日志后再分类。

不把历史实测、游戏进程存在、单一端点成功或 sts2 ping 成功写成当前完整就绪证据。
