# 更新与 `_notice`

lark-cli 命令执行后，如果检测到新版本，JSON 输出中会包含 `_notice.update` 字段（含 `message`、`command` 等）。

除非用户正在询问更新、版本或 notice，否则不要把 `_notice` 原样复制为当前任务的主要答案，也不要为了 notice 中断当前任务去反复查 help。

需要稳定 JSON 给脚本或机器读取时，可以在命令前设置：

```bash
LARKSUITE_CLI_NO_UPDATE_NOTIFIER=1 LARKSUITE_CLI_NO_SKILLS_NOTIFIER=1 <lark-cli command>
```

当你在输出中看到 `_notice.update` 时，先完成用户当前请求；如仍相关，先用本机 `lark-cli update --help` 核对 CLI 自身更新命令及其副作用。当前本机帮助说明 `lark-cli update` 更新 CLI 包，并提供只检查版本的 `--check`；它没有说明会更新 skill 内容。不要把旧文档里关于“一次更新 CLI 和 AI Skills”的说法当作当前行为。

用户询问 CLI 版本时，可以先运行帮助明确标注的只读检查；只有用户要求更新且本机帮助确认更新范围后，才执行 CLI 更新。若更新命令会安装、刷新或覆盖 skills，停止该组合步骤，不要让本次 CLI 更新重新安装已迁出的 Lark skills。

若 `_notice.skills` 提示本地 skills 与 CLI 不同步，不要运行 `npx skills update`、`npx skills add`、`lark-cli` 的 skill 安装/同步命令，也不要让第三方 updater 覆盖活跃目录。用户要求核对上游版本时，只把官方 tar 包取到 `~/.agents/skills` 之外的独立 reference 目录；保存来源 URL、取得日期、原始压缩包及校验值，解包时保留许可证与署名，逐文件比较现有 first-party，并输出差异供人工治理。该流程只生成来源参考和差异，不安装、不登记、不覆盖 first-party。

另外一类 notice：
- `_notice.deprecated_command`：本次使用了兼容保留的旧命令；后续调用改用 `replacement`。若同时提供 `action: "lark-cli update"`，按上面的 CLI 更新规则处理，不触发 skill 更新。
