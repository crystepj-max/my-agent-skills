# Automatic Doctor

打开 ChatGPT 之前先运行本地安装体检：

```bash
node scripts/doctor.mjs --json
```

仅在返回 `READY` 时继续。Node.js 18 或更新版本不可用时报告 `MISSING_RUNTIME`；必需文件缺失或 SKILL.md 名称不符时，报告 `INVALID_INSTALLATION` 并附失败的检查项 ID。

打开或宣称 ChatGPT 之前，再检查版本化自动化决定：

```bash
node scripts/automation-consent.mjs status --json
```

可能的状态：

- `NEEDS_AUTOMATION_CONSENT`：不存在当前决定、决定文件无效，或披露版本已变化。
- `AUTOMATION_DISABLED`：用户已拒绝或撤回自动浏览器交接。
- `READY`：当前披露已被明确接受。

状态为 `NEEDS_AUTOMATION_CONSENT` 时，原样展示以下披露，不得软化：

> 非官方实验性浏览器自动化将使用你已登录的会话，经由本宿主的浏览器控制能力向 chatgpt.com 提交内容并取回结果。这携带非零账号与合规风险，可能触发安全防护、临时限制或账号处置。本项目无法保证账号安全、政策合规或永久的配额隔离，也不以绕过限制为目的。仅在你理解并接受上述风险时启用。

询问是否启用全自动浏览器交接。肯定答复必须明确且出现在当前对话中；沉默、调用本 Skill 或无关回复都不构成同意。此后才运行：

```bash
node scripts/automation-consent.mjs enable --acknowledge-risk I_ACCEPT_EXPERIMENTAL_BROWSER_AUTOMATION_RISK_V1 --json
```

用户拒绝时运行 `node scripts/automation-consent.mjs disable --json`。状态为 `AUTOMATION_DISABLED` 时，不得打开、宣称、检查或控制 ChatGPT。

同意就绪后，每次交接都要按 [transport.md](transport.md) 做易变的浏览器预检：

1. 按 `codex-in-app-browser` → `user-chrome` → `host-browser-use` 的优先级探测通道，锁定唯一通道。
2. 在所选通道打开 `https://chatgpt.com/`，保持页面可见。
3. 检查可见账号 UI。未登录则报告 `NEEDS_CHATGPT_LOGIN`，请用户接管页面，保留原任务待续。
4. 在可见 UI 核对用户指定的模型。不可用则报告 `NEEDS_MODEL_SELECTION`；不得静默代换其他模型。
5. 站点或浏览器访问被宿主权限拦截时，报告 `NEEDS_SITE_PERMISSION`，按宿主的权限流程处理。
6. 认证与模型检查均可见满足后才返回 `READY`。

人工登录是接管步骤，不是自动化步骤。永不调用 ChatGPT 私密端点，永不检查 cookie、local storage、session storage、隐藏鉴权头、浏览器配置文件、密码、验证码或凭据文件。
