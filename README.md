# my-agent-skills

集中管理与跨设备同步我的 agent skill。

## 这个仓库存什么

本仓库刻意**只存两类内容**，不囤第三方 skill 的完整数据：

1. **我自己原创的 skill（完整数据）** —— `my-skills/`
   - 目前：`agent-skill-bridge`（统一管理多 agent 第三方 skill 安装的安全审计 + 公共池 + 中文化 + 桥接 + 去重流水线）
   - 后续你自建/深度改造的 skill，都放这里，带完整文件。
2. **公共 skill 清单（仅元数据，不存数据）** —— `inventory/skill-desc-translation.md`
   - 我当前维护的全部 skill（含第三方）的名称、中文描述、仓库链接/来源、最新更新时间。
   - 按来源分类：大型集合仓库 / 独立仓库 / WorkBuddy 内置·市场。
   - 第三方 skill 只记录信息，**不克隆、不存储其数据**；恢复时按链接从上游拉取。

此外 `tools/` 放我自用的安装/打包脚本（如 `install_all_skills.sh` 一键原样安装 65 个轻量第三方 skill），直接服务跨设备恢复。

## 目录结构

```
my-agent-skills/
├── my-skills/                    # 我自己原创的 skill，完整数据（git 跟踪）
│   └── agent-skill-bridge/
├── inventory/
│   └── skill-desc-translation.md # 公共清单（来源分类 + 最新更新）
├── tools/                        # 自用管理/安装脚本（跨设备恢复用）
│   ├── install_all_skills.sh     # 一键原样安装 65 个轻量第三方 skill（自解压）
│   ├── build_install_all.py
│   ├── add_repo_column.py
│   └── fetch_new_skills.py
├── scripts/
│   ├── sync.sh                   # 自动：提交并推送变更到 main
│   └── restore.sh                # 新电脑：恢复我的常用 skill
├── .gitignore
└── README.md
```

## 日常：更新后自动同步到 GitHub

当你改了 `my-skills/` 下的自有 skill，或更新了清单 `inventory/`，运行：

```bash
bash scripts/sync.sh
```

它会 `git add -A && commit && push` 到 `main`（仅在确有变更时提交）。

> 想更“自动”：可把 `sync.sh` 接进 `agent-skill-bridge` 流水线的最后一步，让每次装/更新 skill 后顺手提交推送。

## 换电脑：快速恢复

在全新或存量电脑上：

```bash
git clone https://github.com/crystepj-max/my-agent-skills.git
cd my-agent-skills
bash scripts/restore.sh
```

`restore.sh` 会：
1. 把 `my-skills/*` 软链进 `~/.agents/skills/`（自有 skill 直接生效，且改完跑 `sync.sh` 即回传）；
2. 运行 `tools/install_all_skills.sh`，字节级一致地恢复 **65 个轻量第三方 skill** 并桥接 WorkBuddy；
3. 运行 `agent-skill-bridge` 把全部 skill 桥接到 claude / codex / workbuddy；
4. 打印 **5 个大体积 skill** 与 **15 个 WorkBuddy 内置/市场 skill** 的手动安装步骤（前者走仓库链接，后者走技能市场）。

> ⚠️ 各 agent 在会话启动时缓存 skill 列表，恢复后请**重启对应 agent 会话**，`/` 才会刷新。

## 新增「我自己原创的 skill」

把完整 skill 目录丢进 `my-skills/`，然后 `bash scripts/sync.sh`。
