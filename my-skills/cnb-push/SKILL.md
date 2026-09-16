---
name: cnb-push
description: 把本地 git 仓库推送到 CNB（cnb.cool）代码平台。当用户要求推送/同步/上传代码到 CNB、把 GitHub 仓库迁移到 CNB、或需要把本机未推送的提交备份到 CNB 时使用。脚本已内置代理绕过、HTTP/1.1 降级、大包缓冲和自动重试，调用者无需记忆任何 git 参数。
agent_created: true
---

# cnb-push — 推送到 CNB（cnb.cool）

> **需要 pull / clone / 建分支 / 建 PR / 合并 PR 等推送以外的操作？用 `cnb-git`。**
> 本 skill 只管推送，是 `cnb-git` 的精简版（`cnb-git.sh push` 会委托本脚本）。

## 何时使用

- 用户要求「推到 CNB」「同步到 CNB」「备份到 CNB」
- 需要抢救只存在于本机的提交（GitHub 账号暂停等场景）
- 迁移仓库到 CNB

**不要用于**：推送到 GitHub / Gitee 等其他平台（本 skill 专用于 CNB）。

## 快速开始

```bash
# 推当前分支
bash ~/.agents/skills/cnb-push/scripts/cnb-push.sh

# 推全部分支 + 标签（迁移场景用这个）
bash ~/.agents/skills/cnb-push/scripts/cnb-push.sh --all

# 指定仓库
bash ~/.agents/skills/cnb-push/scripts/cnb-push.sh /path/to/repo --all

# 先空跑看计划（推荐）
bash ~/.agents/skills/cnb-push/scripts/cnb-push.sh --dry --all

# 顺带把 CNB 设为默认推送目标
bash ~/.agents/skills/cnb-push/scripts/cnb-push.sh --set-default --all
```

参数：`--all`（全部分支+标签）| `--tags`（仅标签）| `--dry` | `--direct`（强制直连）| `--org <组织>` | `--set-default`

## 硬规则（不可违反）

1. **绝不 force push** — 脚本不接受也不传递 `--force` / `-f`。
2. **绝不自动 commit / stash** — 工作区未提交改动原样保留；推送只传已提交内容。
3. **绝不改动 origin** — GitHub 地址是灾备，必须保留。只新增 `cnb` remote。
4. **需用户授权** — 用户没有明确要求推送时，不得主动推送。
5. **token 不外泄** — 通过 `http.extraHeader` 传递，不写入 `.git/config`，日志自动脱敏为 `***TOKEN***`。

## 前置条件

- CNB 仓库**已建好且为空**（在网页端建，勿勾选初始化 README，否则首次推送会冲突）
- 凭据存在 `~/.cnb/token`（cnb CLI 授权后自动生成）
- 若仓库名 ≠ 目录名（如 `STS2-ART-FACTORY` → `game-art-factory`），先在仓库内执行：
  ```bash
  git remote add cnb https://cnb.cool/<组织>/<仓库名>.git
  ```

## 为什么必须用这个脚本

直接 `git push` 会踩三个坑（2026-09-09 实测）：

| 坑 | 现象 | 脚本内置修正 |
|---|---|---|
| **DNS 被 fake-ip 劫持** | iKuuuVPN 的 TUN 把 `cnb.cool` 解析成 `198.18.x`，直连被限速到 **14 KiB/s**（256M 仓库要 2.6 小时） | 自动检测代理端口，走 SOCKS5 让代理端解析真实 DNS → **131 MiB/s** |
| **大 pack 走 HTTP/2 必失败** | `curl 16 Error in the HTTP2 framing layer` | 强制 `http.version=HTTP/1.1` |
| **postBuffer 太小** | 大仓库推送中断 | `http.postBuffer=524288000`（500M）+ `pack.compression=1` |

脚本还会检测 `nslookup cnb.cool` 是否返回 `198.18.*`，命中时明确提示原因。

## 故障表

| 报错 | 原因 | 处理 |
|---|---|---|
| `Repository Not Found` | CNB 仓库未建，或名字不对 | 网页端建空仓；核对仓库名与目录名是否一致 |
| `LibreSSL SSL_read: bad record mac` | 代理 TLS 偶发抖动 | 脚本已内置 3 次重试；仍失败可加 `--direct` 试直连 |
| `HTTP2 framing layer` | 大 pack 走 HTTP/2 | 脚本已强制 HTTP/1.1，无需处理 |
| `token 为空 / 解析失败` | 凭据过期 | 重新授权 cnb CLI，或到 CNB 网页端建 PAT |
| 推送成功但极慢 | 走了被劫持的直连 | 确认 ClashX 在 7890 端口监听；脚本会自动选 SOCKS5 |
| `空 push --tags` 报 SSL 错 | 仓库标签数为 0 时的协议边缘故障 | 脚本自动跳过（无标签则跳过） |

## 推送后验证

```bash
git -c "http.extraHeader=Authorization: Bearer $(python3 -c "import json;print(json.load(open('$HOME/.cnb/token'))['access_token'])")" \
    -c http.proxy=socks5://127.0.0.1:7890 \
    ls-remote --heads https://cnb.cool/<组织>/<仓库>.git
```

比对本地 `git branch -v` 的 sha 是否与远端一致。

## 环境备注

- 默认组织：`chris.ai`（CNB 建仓只认组织，个人命名空间不是有效 slug）
- 本机代理：ClashX `127.0.0.1:7890`
- 已迁移仓库（2026-09-09）：my-agent-skills、workflow-manager、ai-invest、STS2-AUTOTEST、STS2-GAWAIN、sts2-dev-infra
