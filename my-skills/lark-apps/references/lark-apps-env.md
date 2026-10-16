# apps env

> **前置条件：** 先阅读 [`../../lark-shared/SKILL.md`](../../lark-shared/SKILL.md)（认证 / 全局参数 / 安全）。

管理妙搭应用环境变量。查看用 `+env-list`，设置用 `+env-set`，删除用 `+env-delete`。没有单变量 get 命令；要确认某个 key 是否存在，使用 list 后用 `--jq` 过滤。

环境 flag 使用 `--environment`；不要使用旧的 `--env`，也不要使用短选项。

## 查看

`+env-list` 默认查 dev，且默认不返回 value。只有显式传 `--include-values` 后，响应中才可能出现变量值；不要在公开日志里展示带值输出。

接口契约：list 使用 `POST env_vars`，body 固定包含 `env` 和 CLI 场景 `scene=2`；set 使用 `POST create_or_update_env_var`；delete 使用 `POST delete_env_vars`。`--include-values` 只控制 CLI 输出是否展示 value，不作为服务端查询参数发送。

```bash
lark-cli apps +env-list --app-id <app_id>
lark-cli apps +env-list --app-id <app_id> --environment online
lark-cli apps +env-list --app-id <app_id> --include-values --jq '.data.items[] | select(.key == "FOO")'
```

## 设置

dev 环境设置不需要 `--yes`。设置 online 环境是高风险写入：先核对当前请求/既有授权是否覆盖同一 app、online 环境、key、value/配置版本和影响；匹配时按 `lark-shared` 返回的 `hint` 带 `--yes` 执行，不按轮次失效或重复询问。若环境、key、值或影响有未覆盖部分，只请求该差异的授权。保留服务端门禁，不静默加 flag。`--dry-run` 可用于预览请求且不需要 `--yes`。变量值支持直接传 `<value>`，也支持 `@file` 或 stdin 输入。

回复中只说明 app/env/key 和执行结果；不要回显真实 value。需要举例时使用 `<value>`、`@file` 或 stdin。

```bash
lark-cli apps +env-set --app-id <app_id> --key FOO --value <value>
lark-cli apps +env-set --app-id <app_id> --key FOO --value @./secret.txt
lark-cli apps +env-set --app-id <app_id> --environment online --key FOO --value <value> --dry-run
lark-cli apps +env-set --app-id <app_id> --environment online --key FOO --value <value> --yes
```

## 删除

`+env-delete` 是 high-risk-write。先核对用户当前请求/既有授权是否覆盖同一 app、env、具体 key 和删除后果；匹配时遵循 exit 10 的 `hint` 使用 `--yes`，不因认证重试或轮次变化重复询问。若目标或后果超出授权，只请求该缺口；重新登录不扩展原授权范围。不得静默添加或绕过 `--yes`。

```bash
lark-cli apps +env-delete --app-id <app_id> --key FOO --dry-run
lark-cli apps +env-delete --app-id <app_id> --key FOO --yes
lark-cli apps +env-delete --app-id <app_id> --environment online --key FOO --yes
```

## 反模式

- 不要把 `+env-pull` 当成环境变量管理命令；它只是刷新本地 `.env.local` 的兜底工具。
- 不要为了看一个变量臆造名为 env-get 的 apps shortcut；用 `+env-list --include-values` 加 `--jq`。
- 不要把真实 secret 写进示例或对话输出；需要示例时使用 `<value>`、`@file` 或 stdin。
