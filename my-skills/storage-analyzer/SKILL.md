---
name: storage-analyzer
description: "macOS / Windows 存储分析：只读扫描磁盘占用，分级解释大目录并生成报告。报告默认不启用删除；只有用户明确授权具体路径与动作时，才启用对应操作。"
---

# Storage Analyzer

对 macOS 或 Windows 做只读存储分析，产出可交互或静态 HTML 报告。扫描只读；写入扫描 JSON 和报告文件属于本地交付。任何文件清理都需要用户已明确授权具体路径和动作。默认报告不提供一键删除。流程：扫描 → 分析分级 → 生成报告 → 说明估算和限制。

## 铁律

- **扫描全程只读。** 允许在用户交付目录写入 JSON 和 HTML 报告。扫描不得改动被扫描内容。
- **不自动清理。** 用户要求分析不等于授权删除。只有当现有授权尚未覆盖准确绝对路径和动作时，才先列出路径、动作（移入废纸篓或直接删除）及影响并请求授权；已有授权适用于同一对象、动作和影响时继续使用，不因重新启动或整理报告而重复询问。授权范围不外推。
- **估算标注清楚。** 涉及"可释放空间"一律说明是估算值。
- **路径、命令保留原文不翻译。**
- **使用当前用户权限扫描，不调用 `sudo`。** 权限不足的目录记录到 `denied` 并在报告中说明；继续扫描其余目录，不把未读取部分说成完整覆盖。

## 扫描性能注意（macOS）

不同 macOS / BSD / GNU 环境的 `du` 参数能力和目录遍历开销可能不同。不要仅凭系统名称推断某个参数是否可用；先查看当前 `du --help` / `du -h`（按本机支持的帮助参数）或对非敏感的临时目录做小探针。扫描耗时受文件数量、磁盘状态、权限与系统版本影响，不能按磁盘容量给固定时长承诺。

`scan.py` 逐个对子目录运行 `du -sk`；`scripts/scan_batch.py` 每批把最多 20 个子目录交给一次 `du -sk`。目录很多或逐项模式明显过慢时，可尝试批处理模式；实际提升取决于当前主机和目录，不预设倍数。若扫描超时，先检查可用的 `du` 参数和批处理输出，再选择仍只读的执行方式。权限拒绝的目录应保留在 `denied` 字段并在报告中说明覆盖限制。

## 执行流程

### Step 1 扫描（只读）

**默认用 `scan.py`**（逐个 `du -sk`，先确认当前系统的 `du` 支持这些参数）：

```bash
python3 scripts/scan.py > /tmp/storage_scan.json
```

**如果 Container 子目录很多或逐项扫描过慢，可改用 `scan_batch.py`**（批量 `du -sk`，每批最多 20 个；先用小范围探针确认本机行为，再决定是否用于完整只读扫描）：

```bash
python3 scripts/scan_batch.py > /tmp/storage_scan.json
```

两者输出相同格式的 JSON。`scan.py` 自动识别系统（`sys.platform`）：
- **macOS**：扫 home、library、caches、containers、group_containers、app_support、applications、downloads、dev_caches，用 `du` 算大小。
- **Windows**：扫 user_profile、appdata_local、appdata_roaming、temp、downloads、program_files(_x86)、dev_caches，用 `os.scandir` 算大小；`system.disks` 含所有盘符。

输出 JSON：`system`（系统/磁盘信息，含 `disk_name` 主盘名 + `disks` 全部盘）+ `groups`（各组子目录大小，已降序、过滤 50MB 以下）。扫描较慢，耐心等。读不到的目录标 `denied`，需在报告里列出并提示遗漏体量。

### Step 2 分析与分级

先看 `system.os` 判断系统，读对应的数据布局参考：macOS 读 [references/macos.md](references/macos.md)，Windows 读 [references/windows.md](references/windows.md)（讲该系统东西存哪、怎么辨认、归哪一级）。然后读 `/tmp/storage_scan.json` 做这几件事：

1. **挑 Top 5** 占用大户，判定类型（系统资产/应用本体/应用数据/应用缓存/开发缓存/用户文件/媒体内容/下载内容/虚拟机镜像/回收站/其他）。
2. **识别"神秘大目录"**：UUID 命名的 Container、不明的隐藏目录，要追查它属于哪个 App、装的是什么（例如某 97GB 的 UUID Container 实为 Bilibili 离线视频缓存）。必要时 `ls`/`du` 深入一层看清楚，但仍只读。
3. **三级分类 = 清理决策清单，不是全盘点。** 只把"存在'要不要动它'这个决策"的项放进三灯；日常在用的正常应用、操作系统本身、海量零碎小文件没有清理决策，不进三灯，它们落在磁盘条的蓝色"系统及其他"里。判定标准：
   - 🟢 **可再生候选**：纯缓存、临时文件、安装包残留、明确可再生且不影响功能、不丢用户数据（pip/uv/npm/Xcode DerivedData 等开发缓存、浏览器缓存）。标签表示内容风险较低，不代表已授权执行清理。
   - 🟡 **需人工判断**：含用户数据或有判断成本（离线视频、文档、项目代码 node_modules、聊天记录、设计稿）。给内容画像、可行处置路径和风险提示。服务模式提供非破坏性文件管理器定位；只有对应路径和移入废纸篓操作已获明确授权、且使用 `--enable-actions` 时，才显示可逆移动按钮。没有明确路径时不给 `trash_paths`。红灯只提供正规卸载说明与非破坏性定位。`open_note` 可解释应用内部目录为何不适合手动挑选。口吻保持中性、像产品说明。
   - 🔴 **谨慎清理（有决策但不建议手删）**：你可能想动、但建议别手删的具体项——重复安装的应用、想卸载的大应用、运行中应用的核心数据等。给"为什么不建议手删" + `indirect_release` 写**具体卸载步骤**（自带卸载器 / 启动台长按 / 右键移废纸篓 / AppCleaner 清残留 / App Store 可重装等，要可照做不是空话）。应用项给 `app_paths`（真实 `.app` 绝对路径数组）→ 网页出现「在文件管理器打开（去卸载）」按钮，定位到 App 让用户自己正规卸载。**红灯不给删除/卸载按钮**（应用在系统目录、可能要管理员密码、可能有自带卸载器和残留，后台代删不稳妥）。**纯系统文件、APFS 快照不要单独列红卡**（没有清理决策），归蓝色即可；系统层面的释放技巧（重启释 swap、Time Machine 快照策略、可清除空间自动回收）写进 `summary.long_term` 长期建议。

每个 🟢 候选项要给：预估释放空间、清理前需关闭的进程，以及安全处理说明。未获得精确授权时，不提供可直接执行的删除命令或网页删除按钮；可以给应用内清理路径。若用户已授权指定缓存路径，可只对这些授权路径准备命令/允许列表，并优先可逆移入废纸篓。

**大小字段写干净**：`size` / `size_estimate` 用"约 14 GB""合计约 8.6 GB"即可——"约"已表示估算，不要再加"（估算）"，重复且不专业（模板也会自动去掉这种冗余括号）。可再生属性已由分级标题和按钮说明覆盖，别塞进大小字段。

### Step 3 生成交互报告

把分析结果写成 analysis JSON（schema 见 `scripts/build_report.py` 顶部注释）。

仅在用户**明确授权具体路径和操作**后，才在 JSON 的 `trash_paths` 中放入本次获准路径。其他候选项不进入操作白名单。

默认启动交互式报告，但保持只读：
```bash
python3 scripts/server.py /tmp/storage_analysis.json   # 默认只读；Ctrl+C 停
```
此模式只开放非破坏性的文件管理器定位功能；不会显示移入废纸篓或直接删除按钮。服务器绑定 127.0.0.1，并校验随机 token、Host、realpath、三套路径白名单以及 `$HOME`/`/Applications` 边界。

若已有明确的路径+动作授权，可重新启动并只把获准路径写入 `trash_paths`，然后传 `--enable-actions` 启用可逆移入废纸篓。不可逆删除需要对准确路径和直接删除操作的明确授权，并额外传 `--enable-hard-delete`；不要把清空整个绿灯列表当默认动作。页面确认框是额外检查，不替代用户授权。

只读静态报告可用：
```bash
python3 scripts/build_report.py /tmp/storage_analysis.json ~/Desktop/storage-report.html && open ~/Desktop/storage-report.html
```

**默认没有删除按钮是预期行为。** 只有授权的精确路径、`trash_paths` 和对应的 `--enable-actions` 同时存在时，才会显示移入废纸篓操作；直接删除还需要 `--enable-hard-delete`。

报告阅读流：磁盘总览（容量、进度条、容量 pills、系统信息）→ 占用排行 Top5 → 执行建议 → 🟢🟡🔴 三类可折叠卡片（分析和安全处理说明；只有已授权命令才提供复制）→ 长期优化建议。即"现状 → 诊断 → 处方 → 操作 → 预防"。

注意 `summary.overview` 要写成一句话洞察（直接说最大占用是什么、能释放多少），不要重复总/已用/可用数字——那些已在卡片大数字里显示。overview 渲染在"执行建议"小节开头作引子（普通文字），紧接着是 `summary.priority` 优先级清单。

磁盘进度条把"已用"拆成分段：绿(可自动清)+橙(需手动)+红(已识别的不建议动项)+蓝(系统及其他，自动取 已用−绿−橙−红 的余量)，余下为可用(灰底)。`summary.tier_stats` 的 green / yellow / red 三个值都要以可解析的 GB 数字开头（如 "约 27.8 GB"），脚本从中取数算分段；蓝色段和"系统及其他"pill 由模板自动算余量。

pills 只渲染解析出的纯数字（如"约 5.5 GB"），不显示数据里的附注，所以 tier_stats 三个值写干净的数字即可，别加"仅已识别项/系统未计"这类道歉式说明——系统文件本来就归在蓝色段，红色只放你能量化的 🔴 项（重复应用、可卸载大应用等），量不准的系统文件/快照自然落到蓝色。

### Step 4 对话里给摘要

报告生成后，在对话里用一段话给结论先行的摘要：总可释放估算、最该先清的 2-3 项、风险最高的一项。细节让用户看网页。

## 依赖与运行前提

- 全部脚本使用 **Python 3 标准库**，没有第三方 Python 依赖。先按当前主机检查可用解释器（例如 `python3 --version`、`python --version` 或 `py -3 --version`），再用实际存在的命令运行；不要假设系统预装 Python，也不要自动安装依赖。
- macOS 扫描路径会调用 `du`、`sw_vers` 和 `diskutil`；运行前用 `command -v` 检查脚本所需命令。可先对非敏感临时目录做小范围 `du -sk` 探针。缺少命令或参数不受支持时，说明具体缺项并停止受影响的扫描，不声称得到完整结果。
- Windows 扫描使用 Python 的 `os.scandir`；以现场存在的 `python` 或 `py -3` 为准。只有用户已授权具体路径、并显式启用可逆废纸篓动作时，macOS/Windows 才需要相应宿主动作接口（macOS 为 `osascript`）。默认只读报告不依赖这些动作接口。
- 本 skill 是 **agent 驱动**：扫描出数据后由当前 agent 做分级分析，不是双击即用的独立 App。

## 平台状态

- **macOS**：原始上游文档记载过扫描、报告和删除流程的实机测试；该记录不代表本轮测试。本轮只做了静态审阅/隔离 mock 验证（若对应验证已运行则在交付中注明）。
- **Windows**：代码包含 `scan.py` 的 `scan_windows` 和 `server.py` 的 `_trash_windows` (`SHFileOperationW`)，原包声明未在真实 Windows 实测。真实系统清理仍需用户自行验收；多盘符主盘分段条与其他盘列表尚需对应环境验证。

## 长期优化建议素材（写进报告 summary.long_term）

- 定期清理：`brew cleanup`、Xcode DerivedData、浏览器缓存
- 可视化工具：DaisyDisk、GrandPerspective、OmniDiskSweeper
- 大文件归档到外置盘 / iCloud / NAS；macOS「系统设置 > 通用 > 储存空间」的优化选项
