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

## 推送范围与授权

- 默认只推当前分支；显式分支参数只推所列分支，`--tags` 只推标签。
- `--all` 会把**本地全部分支和全部标签**推到目标 CNB 仓库，可能包含本次任务无关分支。要求用户明确授权这一完整范围；已有授权仅在目标仓库和分支/标签范围完全一致时复用，不重复询问。
- `--set-default` 会写入仓库本地的 `remote.pushDefault=cnb`，影响之后未显式指定远端的 `git push`。把这项持久配置变更单独纳入授权；只有既有授权也明确覆盖它时才可复用。
- 用户要求推送当前改动到 CNB，不自动等于授权推送全部分支或修改默认推送目标。对未覆盖的范围只确认缺失的授权，不重复已明确授权的部分。

## 首次上传与已有仓库更新

- **首次上传**：远端为空最容易直接推送，但不是脚本的硬性前置条件。若网页建仓时已初始化 README 等内容，先比较远端与本地历史并决定如何衔接；不得用 force 覆盖远端内容。
- **更新已有仓库**：照常非强制推送已提交内容。若远端拒绝非快进更新，停止并报告；只有在授权范围内明确安排后，才另行取回并整合远端提交。
- 两种情况都不自动提交、stash、改写 origin 或强推；未提交改动保留在本地。

## 硬规则（不可违反）

1. **绝不 force push** — 脚本不接受也不传递 `--force` / `-f`。
2. **绝不自动 commit / stash** — 工作区未提交改动原样保留；推送只传已提交内容。
3. **绝不改动 origin** — GitHub 地址是灾备，必须保留。只新增 `cnb` remote。
4. **遵守本节的目标和范围授权** — 不能把推送当前分支扩大成全部分支/标签，也不能未经授权修改仓库默认推送目标。
5. **token 不外泄** — 通过 `http.extraHeader` 传递，不写入 `.git/config`，日志自动脱敏为 `***TOKEN***`。

## 前置条件

- CNB 仓库已存在且当前凭据有写入权限；首次上传时远端为空最简单，但已有初始化内容须先核对并决定如何衔接
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
| `Repository Not Found` | CNB 仓库未建、名字不对或 token 无权访问 | 核对目标 URL、仓库与权限；首次上传的远端如已有 README 等内容，先比较历史，不要强推覆盖 |
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
