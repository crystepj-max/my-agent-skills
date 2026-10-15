# 证据层级与发布终态

## 风险决定证据深度

| 结论 | 最低证据 |
|---|---|
| “文档链接有效” | 项目自己的 doc-link/index check 或逐链接存在性 |
| “规则已同源” | realpath/readlink/import + 平台实际加载顺序 |
| “代码实现是 X” | 当前目标分支代码、schema、配置与相关测试 |
| “PR 已完成” | PR state=merged + merge commit；不能推导已部署 |
| “已部署” | deploy marker/release 指向目标 commit + 服务 active |
| “用户已看到新版本” | canonical 用户 URL/API 的真实响应，必要时同时比 origin/cache |
| “可安全清场” | 对象、版本、保留用途与唯一内容已核验；发布现场另需适用的 merged / production / knowledge receipt 证据 |
| “已获准清场” | 有效授权覆盖同一对象、范围、版本和影响；现场明确约定的汇报后人工关口另行满足 |
| “整个项目干净” | 项目内所有适用事实面 verified；warning、pending 和 out-of-scope 单列 |

代码直觉、旧 memory、commit message 和 cache-buster URL 都只能当线索，不能单独证明生产终态。

## 真相矩阵

对每个发现至少记录：

```text
topic: <事实主题>
authority: <当前权威来源>
code: verified-current | stale | n/a
runtime: verified-current | stale | unverified | n/a
docs: verified-current | stale | changed
rules: verified-current | stale | changed | n/a
memory: verified-current | stale | generated-read-only | changed | n/a
action: <做了什么或为什么没做>
verification: <命令、页面或门禁>
```

用户不需要看到完整矩阵，但最终摘要必须保留未闭合状态。

## 发布状态机

```text
implemented
  -> locally verified
  -> pushed / PR opened
  -> CI + required backtest/visual review passed
  -> merged
  -> deployed
  -> live verified
  -> knowledge closed + receipt recorded
  -> cleanup candidates and effective authorization verified
  -> any explicitly required human gate satisfied
  -> workspace cleaned
  -> post-cleanup audit passed
  -> cleanup result appended
```

跳过的状态必须有项目规则允许的原因。失败停在哪一格，就按那一格汇报，不能用“基本完成”覆盖。

## 缓存和多表面产品

当用户可见内容经过 CDN、边缘缓存、搜索索引、异步 worker 或多客户端时，至少识别：

- origin 是否为新内容；
- canonical URL 是否仍为旧缓存；
- API/页面/通知/RSS 是否共享同一数据出口；
- deploy marker 是否在所有异步进程真正切换之后才写；
- cache-buster 是否只是诊断，而非真实用户验收。

只验证其中一个表面时，在结论里明确限制范围。

## 清场前 gate

按对象风险执行适用步骤，不把发布门禁套到本轮可再生临时文件：

1. 对历史分支、worktree、库和产物，核验唯一内容、集成状态与恢复路径；发布收尾另核验部署及知识凭证。
2. 列出具体候选及内容版本，对照有效授权。
3. 同一对象、范围、版本和影响已获批准时继续；范围变化、唯一资产未核清或缺少约定的人工关口时，只暂停相关对象，先呈交清单再请求决定。
4. 清理已授权且安全的对象，保留交付物、验证证据和所需恢复备份。
5. 复查工作区并汇报实际结果。

笼统的“收尾并清理”不足以授权删除未知历史资产；具体清单的有效预授权也不会因经过一次汇报或技能切换而失效。目录名、分支年龄和会话关闭都不能单独证明可删除。

## 验证失败时

- 同一失败第二次出现，停止盲重试，重新检查假设、环境和命令名。
- 门禁要求机器可读 metadata 时，补正确留痕并触发新事件；不要用人工确认绕过可修复的格式问题。
- 失败发生在生产写入前，明确说“尚未影响生产”；发生在切流后，先确认当前 active release 和回滚边界。
- 任何未验证项保持 `pending`，不要为了摘要好看把它降格成 warning。
