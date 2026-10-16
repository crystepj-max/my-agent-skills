> **实际启用状态已迁移到 [生命周期清单](skill-lifecycle.md) 与 skill-policy.json。** 本文件保留描述和来源，不作为恢复器的全量安装名单；旧“使用范围”以生命周期清单为准。

# Skill 中文描述与来源档案（含历史公共池表）

> 历史快照生成：2026-08-24 ｜ 原范围：公共池 `~/.agents/skills/`（claude / codex / workbuddy / openclaw / hermes 五端经软链同步中文；kimi / opencode 原生直读公共池）。以下原表、来源与能力描述完整保留，不能作为当前启用/安装状态。

> 说明：本表按旧快照记录当时公共池 `~/.agents/skills/` 中的 skill；53 个 Claude 插件 skill 按当时规则①未改动、仍为英文，不在本表范围；agent 独有（公共池无同名）的 skill 亦不收录。各 skill 的「仓库链接 / 来源」「作者」「仓库简介」三列同源合并。当前状态、范围和维护源以生命周期清单与正式策略为准。

> ⚠️ **排版保护说明**：本表为人工优化版。结构（三块分区、列定义、参考/范围列）请勿手工整体重写；第三方 skill 移入「参考 Skill」板块、第一方「参考的 skill/参考日期」回填，请直接在对应表格行编辑。刷新「最新更新」列请只运行 `scripts/refresh_inventory.py`（该脚本仅更新此列，不改动排版与列结构）。

> 本表保留 Skill 描述、来源与维护责任说明，不设置固定总数；实际启用状态和范围以 [生命周期清单](skill-lifecycle.md) 与 skill-policy.json 为准。各 skill 含「skill 范围」列：用户级 / 项目仓库名 / 宿主限定（仅 codex）。

## 本仓维护的第一方 Skill（原描述表；经软链同步至公共池 `~/.agents/skills/`）

> 本节保留原人工描述表，不是当前所有第一方维护源的完整清单。当前维护来源见文末 99 条映射附表。登记本仓维护源不单独证明历史作者或最初来源；表格「参考的 skill」「参考日期」两列记录当时注明的参考。

| # | Skill 名称 | 中文描述 | 参考的 skill | 参考日期 | skill 范围 | 最新更新 |
|---|---|---|---|---|---|---|
| 1 | `agent-cli-tool-residue-purge` | 当 AI 编程 CLI（Claude Code、Codex、Gemini CLI 等）在某个辅助/代理/包装工具被卸载后开始报错时使用——例如 SessionStart:startup hook error、每次 Bash 调用都 command not found、或 CLI 静默指向已失效的 localhost 端口。提供跨所有配置层（settings 文件、MCP 注册表、hooks、shell rc、launchd、cron）的全面排查与清理流程，确保不留任何陈旧引用。 | — | — | 用户级 | 平台内置 |
| 2 | `agent-skill-bridge` | 管理多个 AI agent 的技能来源与生命周期：第一方源完整执行、第三方原版保留参考、并维护退役与项目范围边界；含只读中文化守护。 | find-skills | 2026-10-05 | 用户级 | 2026-10-15 |
| 3 | `clashx-openai-sse-debug` | 排查 ClashX（ClashX Pro）代理导致 OpenAI 或 API 流式 SSE 连接中断的问题：Codex 桌面端连不上、stream closed before response.completed、SSE 断连、macOS 上 ClashX 规则模式或全局模式下 OpenAI 流式失败。覆盖 ClashX 控制 API、热重载导致 DNS 崩溃的坑、验证 OpenAI 必须走代理、节点选择、SSE 稳定性测试。 | — | — | 用户级 | 平台内置 |
| 4 | `cnb-git` | 封装 CNB 代码平台的 Git 操作；按实际 upstream remote 与服务端分支 fetch/pull，凭据仅发往 CNB URL，保留锁并明确传播 clone/fetch/pull 失败。 | — | — | 用户级 | 2026-10-15 |
| 5 | `cnb-push` | 把本地 Git 仓库推送至 CNB；区分已有仓库更新和首次上传，并说明 --all 与 --set-default 的实际范围。 | — | — | 用户级 | 2026-10-15 |
| 6 | `dsh-source-upgrade` | 按当前 DeepSeek Harness 源码与运行现场升级；将源码升级、单独重启和配置对齐分别处理，并保留真实版本、LLM 与隔离网页验证要求。 | — | — | 用户级 | 2026-10-15 |
| 7 | `dsh-web-access-recovery` | 按当前 DeepSeek Harness 认证、服务与日志证据恢复网页访问；保护 token/cookie，不把旧端口、令牌期限或后台能力当作现行事实。 | — | — | 用户级 | 2026-10-15 |
| 8 | `duplicate-cli-unify` | 当同一个命令行工具（如 Claude Code、Codex 或任何 npm/node 类 CLI）被多个包管理器重复安装时使用——最常见的是 nvm 全局安装与 Homebrew 安装并存，导致版本混乱、残留旧副本、或自动更新静默写入错误路径。提供检测、分析、决策、修复的完整流程，把工具统一到单一安装源。 | — | — | 用户级 | 平台内置 |
| 9 | `workspace-convergence-audit` | 只读审计多 worktree 与独立分支并形成报告；尊重原请求已授权的清理边界，对未知归属和唯一资产保留并报告。 | — | — | 用户级 | 2026-10-15 |

## 其他项目维护的第一方 Skill

> 仅记录其仍可能出现在公共池中的描述。本仓不维护其源代码、不登记或分发；由对应项目直接安装到用户级目录。

| Skill 名称 | 中文描述 | 参考的 skill | 参考日期 | skill 范围 | 维护项目 |
|---|---|---|---|---|---|
| `requirements-analysis` | 需求分析统一入口：把需求来源加工成经人工确认的任务定义，并将正式状态写入 Multica Task；workflow-manager 维护并直接分发，my-agent-skills 不镜像、不登记、不提供用户级入口。 | to-spec、to-tickets | 2026-10-08 | 用户级 | workflow-manager |

> **2026-09-15 退役**：原第 4 项 `dev-workflow-2-0`。其职责已由「AI 任务交付」集合拆分为 M1 `requirements-analysis` / M2 `wf-construction-full-feature` / M3 `execution-plan` 承接，已在 `skill-policy.json` 置为 `retired`，源目录移出发现目录至 `~/.local/share/agent-skills/retired/dev-workflow-2-0`。同批退役的还有 `construction-bootstrap`。

## 历史第三方 Skill 来源与能力说明（旧公共池记录）

> 按原「来源分类 > 字母顺序」表格完整保留，内容反映旧公共池记录；不表示这些条目目前仍是独立执行入口。其当前状态以正式策略 `inventory/skill-policy.json` 和生命周期清单为准。历史上的覆盖关系和来源归属按当时资料展示，不推导为当前可用性或第一方原创声明。
>
> 旧表覆盖关系说明（仅保留历史原意；其中“仍保留为可用入口”不代表当前状态）：当时记录的部分覆盖关系包括 `triage`、`grill-with-docs`、`wayfinder`（对应 `requirements-analysis`）和 `skills-security-check`（对应 `agent-skill-bridge`）；旧表还记载 `tdd` 曾部分依赖已退役的 `dev-workflow-2-0`。这些记录不表示当前仍有相同覆盖或入口。

| # | Skill 名称 | 中文描述 | 仓库链接 / 来源 | 作者 | 仓库简介 | skill 范围 | 最新更新 |
|---|---|---|---|---|---|---|---|
| 1 | `agnes-ai-generation-skill` | 调用 Agnes AI / Sapiens AI 的生成接口，支持文本、图像、视频。当用户要使用 Agnes 模型、Agnes 图像/视频、Agnes 2.0 Flash、apihub.agnes-ai.com，或要生成文本、图像、编辑图像、创作视频、让图像动起来、生成关键帧视频，或测试 Agnes API 时。 | [github.com/Yacey/agnes-ai-generation-skill](https://github.com/Yacey/agnes-ai-generation-skill) | Yacey | Agnes AI 文/图/视频生成 API 的 Agent Skill | 用户级 | 2026-06-21 |
| 2 | `ask-matt` | 询问哪个 skill 或流程适合当前情况。相当于本仓库 skills 的路由器。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock | 面向真实工程师的 Skills 合集，源自作者 .agents 目录 | 用户级 | 2026-10-05 |
| 3 | `baoyu-comic` | 基于多种艺术风格与基调的知识漫画创作工具，可生成原创教育漫画，含分镜排版与连贯的图像生成。当用户要创作『知识漫画』『教育漫画』『传记漫画』『教程漫画』或 Logicomix 风格的漫画时使用。 | [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) | Jim Liu | 宝哥（baoyu）系列 AI 创作工具合集 | 用户级 | 2026-09-10 |
| 4 | `baoyu-image-gen` | 基于 OpenAI、Google、DashScope 接口的 AI 图像生成。支持文生图、参考图、多种宽高比。默认串行生成，可按需并行。当用户要生成、创作或绘制图像时使用。 |  |  |  | 用户级 | 平台内置 |
| 5 | `baoyu-infographic` | 专业信息图生成工具，提供 20 种版式与 17 种视觉风格。会分析内容、推荐『版式×风格』组合并生成可直接发布的成品信息图。当用户要制作信息图、数据可视化海报或一页式图解时使用。 |  |  |  | 用户级 | 平台内置 |
| 6 | `baoyu-slide-deck` | 根据内容生成专业的幻灯片图像。先生成带风格说明的大纲，再逐页生成幻灯片图。当用户说『做幻灯片』『做演示』『生成 deck』『slide deck』或『PPT』时使用。 |  |  |  | crystepj-max/Chris-Vault/ | 平台内置 |
| 7 | `beautiful-html-templates` | 英文 HTML 演讲稿渲染与模板选择。用于在 humanize-ppt 已完成大纲和逐页意图后，从上游模板库选择并渲染英文演示文稿。使用前阅读本目录的 AGENTS.md 与 index.json；不负责大纲、观众状态或演讲体检。 | [github.com/zarazhangrui/beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates) | zarazhangrui | HTML 幻灯片模板库，供编码 agent 自动生成精美演示 | crystepj-max/Chris-Vault/ | 2026-06-09 |
| 8 | `bottleneck-hunter` | 供应链瓶颈猎手：AI驱动的全球产业链瓶颈套利。来源：skills/bottleneck-hunter.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | xbtlin | AI 时代伯克希尔：基于 Claude Code/Codex 的价值投资研究框架 | 用户级 | 2026-09-27 |
| 9 | `code-review` | 针对某个基准点(提交/分支/标签/merge-base)之后的改动做审查，分两个维度——规范(代码是否遵循本仓库编码规范?)与需求(代码是否匹配原始 issue/PRD 的要求?)。两个维度并行由子 agent 审查并并排汇报。当用户要审查分支、PR、进行中的改动，或说『review since X』时使用。 |  |  |  | 用户级 | 平台内置 |
| 10 | `codebase-design` | 设计深层模块时的共享词汇表。当用户要设计或改进某模块的接口、寻找深化机会、决定接缝位置、让代码更易测试或更利于 AI 导航，或别的 skill 需要深层模块词汇时使用。 |  |  |  | 用户级 | 平台内置 |
| 11 | `deep-company-series` | 深度公司系列：8 篇长文拆一家公司。来源：skills/deep-company-series.md. |  |  |  | 用户级 | 平台内置 |
| 12 | `domain-modeling` | 构建并打磨项目的领域模型。当用户要敲定领域术语或通用语言、记录架构决策，或别的 skill 需要维护领域模型时使用。 |  |  |  | 用户级 | 平台内置 |
| 13 | `dyp-ask` | 段永平问答：以他的方式思考。来源：skills/dyp-ask.md. |  |  |  | 用户级 | 平台内置 |
| 14 | `earnings-review` | 财报精读：一手资料深度解读。来源：skills/earnings-review.md. |  |  |  | 用户级 | 平台内置 |
| 15 | `earnings-team` | 财报精读团队：四大师并行解读 + 公众号发布。来源：skills/earnings-team.md. |  |  |  | 用户级 | 平台内置 |
| 16 | `edit-article` | 通过重组章节、提升清晰度、收紧文风来编辑润色文章。当用户要编辑、修订或改进文章草稿时使用。 | WorkBuddy 内置 / 应用市场 | WorkBuddy 平台（检索未定位独立上游仓库） | WorkBuddy 平台内置 skill | 用户级 | 平台内置 |
| 17 | `eli5` | 当用户键入 /eli5 或想要图文并茂的讲解时使用。用大图、少文字的 HTML 图卡，把任意主题讲得像给 5 岁小孩解释那样通俗易懂。 | [github.com/companion-inc/feynman](https://github.com/companion-inc/feynman) | Companion Inc | 用通俗方式讲解概念的 skill（费曼学习法） | 用户级 | 2026-10-05 |
| 18 | `financial-data` | 财务数据获取与交叉验证规范。来源：skills/financial-data.md. |  |  |  | 用户级 | 平台内置 |
| 19 | `frontend-design` | 构建新界面或重塑旧界面时，提供独特、有意图的视觉设计指引。帮助确定美学方向、排版，以及做出不像模板默认值的取舍。 | [github.com/anthropics/skills](https://github.com/anthropics/skills) | Anthropic（官方） | Anthropic 官方 Agent Skills 公共仓库 | 用户级 | 2026-10-05 |
| 20 | `frontend-slides` | 从零创建动画丰富的 HTML 演示，或将 PowerPoint 文件转换而来。当用户要制作演示、把 PPT/PPTX 转成网页、或为演讲/路演做幻灯片时使用。通过可视化探索(而非抽象选项)帮助非设计者找到自己的美学。 | [github.com/zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) | zarazhangrui | 用编码 agent 的前端能力在 Web 上创建精美幻灯片 | crystepj-max/Chris-Vault/ | 2026-06-23 |
| 21 | `git-guardrails-claude-code` | 在危险 git 命令(push、reset --hard、clean、branch -D 等)执行前，用 Claude Code hooks 拦截。当用户想防止破坏性 git 操作、添加 git 安全钩子，或在 Claude Code 中阻止 git push/reset 时使用。 |  |  |  | 用户级 | 平台内置 |
| 22 | `grill-me` | 一场毫不留情的追问式访谈，用来打磨计划或设计。 |  |  |  | 用户级 | 平台内置 |
| 23 | `grill-with-docs` | 一场毫不留情的追问式访谈，用来打磨计划或设计，同时边聊边产出文档(ADR 与术语表)。 |  |  |  | 用户级 | 平台内置 |
| 24 | `grilling` | 就某个计划、决策或想法对用户穷追不舍地追问。当用户想压力测试自己的思路，或使用了任何『grill』触发词时使用。 |  |  |  | 用户级 | 平台内置 |
| 25 | `guizang-ppt-skill` | 生成横向翻页网页 PPT（单 HTML 文件），含 WebGL 背景、章节幕封、数据大字报、图片网格等模板。提供两种风格：① "电子杂志 × 电子墨水"（衬线 + 流体背景 + 暖色） ② "瑞士国际主义"（无衬线 + 网格点阵 + IKB/柠檬黄/柠檬绿/安全橙高亮）。当用户需要制作分享 / 演讲 / 发布会风格的网页 PPT，或提到"杂志风 PPT"、"瑞士风 PPT"、"Swiss Style"、"horizontal swipe deck"时使用。 | [github.com/op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) | op7418 | 生成精美 HTML 幻灯片的 AI-agent skill（杂志风/瑞士风） | crystepj-max/Chris-Vault/ | 2026-08-07 |
| 26 | `handoff` | 把当前对话压缩成一份交接文档，供另一个 agent 接手。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | Matt Pocock | 面向真实工程师的 Skills 合集，源自作者 .agents 目录 | 用户级 | 2026-10-05 |
| 27 | `hatch-pet` | 从角色原画、生成图、公司/客户品牌线索或视觉参考中，创建、修复、校验、可视化 QA，并打包兼容 Codex 的 v2 动画宠物。适用于任何新的 Codex 宠物、自定义吉祥物、非像素风宠物、品牌灵感宠物、已有宠物修复，或需要 9 行标准动画、16 个朝向、确定性装配、QA 产物与 spriteVersionNumber 2 打包的 8x11 雪碧图流程。 | [github.com/openai/skills](https://github.com/openai/skills) | OpenAI（官方） | OpenAI 官方 Skills 目录（面向 Codex） | 用户级 | 2026-09-08 |
| 28 | `humanize-ppt` | 为 Agent 生成的 PPT 做『人性化』润色——把原始素材转成以听众心智转化为目标的结构化演讲，而非模板堆砌。当用户要制作演讲/PPT/幻灯片，或希望内容有叙事与节奏时使用。 | [github.com/LearnPrompt/humanize-ppt](https://github.com/LearnPrompt/humanize-ppt) | LearnPrompt | 基于 AST 的大纲导演，打造以人为中心的 AI 演示工作流 | crystepj-max/Chris-Vault/ | 2026-07-31 |
| 29 | `implement-spec` | 在代码中实现 to-spec / to-tickets 的产出时使用。把工单读成**任务图**，在就绪的 frontier 上并行启动实现子 agent（各自独立 worktree），全部汇入同一条集成分支，最后以 code-review 收口。**目标是集成分支本身而不是 PR**；每个实现者用 tdd 构建工单、并把集成分支尖端合入自己分支后再报完成，使每次合并都是快进。用户手动调用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/implement-spec) | Matt Pocock | 面向真实工程师的 Skills 合集，源自作者 .agents 目录 | 用户级 | 2026-10-05 |
| 30 | `improve-codebase-architecture` | 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，再就你选定的那一项展开追问式打磨。 |  |  |  | 用户级 | 平台内置 |
| 31 | `income-investment` | 收益投资——稳健与机会主义的分配分析。来源：skills/income-investment.md。 |  |  |  | 用户级 | 平台内置 |
| 32 | `industry-funnel` | 行业漏斗筛选：从全市场到 3 家的价值投资精选流程。来源：skills/industry-funnel.md. |  |  |  | 用户级 | 平台内置 |
| 33 | `industry-research` | 行业投资研究：产业链全景扫描 + 四大师个股分析框架。来源：skills/industry-research.md. |  |  |  | 用户级 | 平台内置 |
| 34 | `investment-checklist` | 巴菲特价值投资买入前 Checklist。来源：skills/investment-checklist.md. |  |  |  | 用户级 | 平台内置 |
| 35 | `investment-memo-craft` | 仅 Codex 使用的写作与排版层，用于 AI Berkshire 投资研究报告的撰写。每当 Codex 创建、重写、修订或批评公司/行业/基金研究报告，尤其是需要财务严谨、可读的商业机理、逆向分析、估值到行动的指引、针对投资人的建议、克制的排版与清晰的买入/持有/卖出信号的长文 Markdown 报告时使用。不要用它修改 Claude Code 斜杠命令源。 |  |  |  | 用户级 | 平台内置 |
| 36 | `investment-research` | 投资研究：巴菲特-芒格-段永平-李录 四大师综合分析框架。来源：skills/investment-research.md. |  |  |  | 用户级 | 平台内置 |
| 37 | `investment-team` | 投研团队：四角色并行分析框架。来源：skills/investment-team.md. |  |  |  | 用户级 | 平台内置 |
| 38 | `llm-wiki-app` | 查询用户的 LLM Wiki 知识库（运行在 127.0.0.1:19828 的 LLM Wiki 桌面应用，并非 Obsidian、Notion、Apple Notes、Logseq 或其他 PKM 工具）。仅当用户明确提到 LLM Wiki 时使用。 | [github.com/nashsu/llm_wiki_skill](https://github.com/nashsu/llm_wiki_skill) | nashsu | 查询本地 LLM Wiki 知识库的 skill | 用户级 | 2026-05-19 |
| 39 | `management-deep-dive` | 管理层纵深研究：买股票就是买人。来源：skills/management-deep-dive.md. |  |  |  | 用户级 | 平台内置 |
| 40 | `migrate-to-shoehorn` | 把测试文件从 `as` 类型断言迁移到 @total-typescript/shoehorn。当用户提到 shoehorn、想替换测试中的 `as`，或需要部分测试数据时使用。 |  |  |  | 用户级 | 平台内置 |
| 41 | `neat-freak` | 会话结束时以极致严谨做知识清理：将项目文档(CLAUDE.md、README、docs)与 agent 记忆、代码库对账，消除不一致，保持仓库整洁。 | [github.com/KKKKhazix/khazix-skills](https://github.com/KKKKhazix/khazix-skills) | 数字生命卡兹克 (KKKKhazix) | 数字生命卡兹克开源的 AI Skills 合集 | 用户级 | 2026-10-01 |
| 42 | `news-pulse` | 公司新闻脉搏：股价异动时快速归因。用 4 个并行 Agent 侦察公司事件/监管政策/行业对手/市场情绪，产出"事件时间线 + 异动主因判断 + 是否触发论文重审"。 |  |  |  | 用户级 | 平台内置 |
| 43 | `obsidian-vault` | 在 Obsidian 仓库中搜索、创建与管理笔记，支持双链与索引笔记。当用户想在 Obsidian 中查找、创建或整理笔记时使用。 |  |  |  | 用户级 | 平台内置 |
| 44 | `portfolio-review` | 组合管理：从\"研究公司\"到\"管理组合\"。来源：skills/portfolio-review.md. |  |  |  | 用户级 | 平台内置 |
| 45 | `ppt-master` | AI 驱动的演示文稿工作流：生成可编辑的 PPTX 文件，创建可复用的品牌/版式/成套工作区，填充原生 PPTX 模板。 | [github.com/hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) | Hugo He | AI 将文档/主题转为原生 PowerPoint 演示文稿 | crystepj-max/Chris-Vault/ | 2026-10-05 |
| 46 | `pr` | 写 Pull Request 描述时使用。PR 正文应是「改动前后对照」而非「改动清单」——用最小可视化（伪代码、调用树、文件树、Mermaid、diff）说清改了什么、给出改前改后的证据、并明确判断这是单向门还是双向门（可逆 / 难回退）及影响半径。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr) | Matt Pocock | 面向真实工程师的 Skills 合集，源自作者 .agents 目录 | 用户级 | 2026-10-05 |
| 47 | `private-company-research` | 未上市公司研究：多Agent并行深度研究框架。来源：skills/private-company-research.md. |  |  |  | 用户级 | 平台内置 |
| 48 | `prototype` | 构建一个一次性的原型来验证某个设计问题。当用户想快速验证状态模型或逻辑是否成立，或探索某个 UI 应该长什么样时使用。 |  |  |  | 用户级 | 平台内置 |
| 49 | `quality-screen` | 去劣筛选：7条指标快速排除非一流公司。来源：skills/quality-screen.md. |  |  |  | 用户级 | 平台内置 |
| 50 | `remotion-best-practices` | Remotion 最佳实践。 |  |  |  | 用户级 | 平台内置 |
| 51 | `remotion-video-production` | Remotion 视频生产：当提示或既有流程显式要求 Remotion 视频生产时使用（代码优先的视频生成方案）。 | [github.com/akillness/jeo-skills](https://github.com/akillness/jeo-skills) | akillness | 面向 codex/code/antigravity 的 skills 合集 | 用户级 | 2026-10-03 |
| 52 | `remotion-video-toolkit` | 用 Remotion + React 做程序化视频创作的完整工具箱。涵盖动画、时序、渲染(CLI/Node.js/Lambda/Cloud Run)、字幕、3D、图表、文字特效、转场与媒体处理。在编写 Remotion 代码、搭建视频生成管线，或创建数据驱动视频模板时使用。 | [github.com/shreefentsar/remotion-video-toolkit](https://github.com/shreefentsar/remotion-video-toolkit) | shreefentsar | Remotion 程序化视频创作工具箱（React） | 用户级 | 2026-01-29 |
| 53 | `research` | 针对高可信一手来源调研某个问题，并把结论以 Markdown 文件存入仓库。当用户想调研某个主题、收集文档或 API 事实，或把繁琐的资料查阅交给后台 agent 时使用。 |  |  |  | 用户级 | 平台内置 |
| 54 | `resolving-merge-conflicts` | ~~已退役（2026-10-06）~~ 当你需要解决进行中的 git merge/rebase 冲突时使用。上游 v1.3.0 已移除、无替代，源目录移至 `~/.local/share/agent-skills/retired/`。 |  |  |  | 用户级 | 平台内置 |
| 55 | `retro` | 对一次编码会话做复盘时使用。**复盘的对象是 agent 的工作环境，不是代码本身**——导航指引、自动化检查、编码规范、steering 文件、工具经济性、信息可达性。机械性违规配确定性检查（lint 规则 / pre-commit 钩子 / CI 任务），需判断的记入 CODING_STANDARDS.md；仓库完全没有护栏本身就是一条发现。用户手动调用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro) | Matt Pocock | 面向真实工程师的 Skills 合集，源自作者 .agents 目录 | 用户级 | 2026-10-05 |
| 56 | `scaffold-exercises` | 创建含章节、题目、解答与讲解的练习目录结构，且能通过 lint。当用户想搭建练习、创建练习桩，或新建一门课程章节时使用。 |  |  |  | 用户级 | 平台内置 |
| 57 | `setup-matt-pocock-skills` | 为本仓库配置工程类 skills——设置 issue 跟踪器、分诊标签词表与领域文档布局。在首次使用其他工程类 skill 前运行一次。 |  |  |  | 用户级 | 平台内置 |
| 58 | `setup-pre-commit` | 在当前仓库用 Husky pre-commit 钩子配合 lint-staged(Prettier)、类型检查与测试。当用户想添加 pre-commit 钩子、配置 Husky、设置 lint-staged，或添加提交时格式化/类型检查/测试时使用。 |  |  |  | 用户级 | 平台内置 |
| 59 | `skill-creator` | 创建新 skill、修改并改进已有 skill，并衡量 skill 表现。当用户想从零创建 skill、编辑或优化已有 skill、运行评测测试 skill、用方差分析基准测试 skill 表现，或为更好的触发准确率优化 skill 的描述时使用。 |  |  |  | 用户级 | 平台内置 |
| 60 | `skills-security-check` | 腾讯云鼎实验室出品，Skill 安全审查工具。对用户指定的 skill.md 文件及其配套的文档、程序、脚本等进行全面安全审计，确保引用安全。 | WorkBuddy 内置 / 应用市场（腾讯云鼎实验室） | 腾讯云鼎实验室 | Skill 安全审查工具（腾讯云鼎实验室出品，WorkBuddy 平台内置） | 用户级 | 平台内置 |
| 61 | `storage-analyzer` | macOS / Windows 只读存储分析：扫描整机磁盘占用，定位占用大户，分级给出可自动清理/需人工判断/谨慎清理方案，并生成可一键删除的交互式 HTML 报告。 |  |  |  | 用户级 | 平台内置 |
| 62 | `tdd` | 测试驱动开发。当用户想以测试先行的方式构建功能或修复 bug、提到『red-green-refactor』，或想要集成测试时使用。 |  |  |  | 用户级 | 平台内置 |
| 63 | `teach` | 在当前工作区内，教用户一项新技能或概念。 |  |  |  | 用户级 | 平台内置 |
| 64 | `thesis-drift` | 投资论文漂移检测：分清事实变化与措辞变化。来源：skills/thesis-drift.md. |  |  |  | 用户级 | 平台内置 |
| 65 | `thesis-tracker` | 投资论文追踪：买入后的纪律系统。来源：skills/thesis-tracker.md. |  |  |  | 用户级 | 平台内置 |
| 66 | `to-questionnaire` | 把你自己无法完全回答的一个决策，转化成一份由他人填写的问卷。 |  |  |  | 用户级 | 平台内置 |
| 67 | `triage` | 通过分诊角色的状态机推进 issue 与外部 PR——分类、核验、必要时追问，并写出可供 agent 使用的简报。 |  |  |  | 用户级 | 平台内置 |
| 68 | `typesafe-ai` | 用 TypeSafe 把 AI 智能做成可组合的编程原语：System One 模型（含旗舰模型 Jev）读自然语言与应用状态，输出带类型与概率的判断而非生成文本。适用于路由、排序、抽取、校验、重排及交互式体验。规则、计算与执行仍留在代码里；实时文档与 cookbook 是准绳。 | [github.com/typesafe-ai/skills](https://github.com/typesafe-ai/skills) | typesafe-ai | TypeSafe System One / Jev 结构化判断原语 | 用户级 | 2026-09-12 |
| 69 | `video-production` | 规划并调度「代码优先 / 模板优先 / 混合」的内容视频生产管线。当用户需要可程序化或自动化的视频生产时使用。 | [github.com/jmagly/aiwg](https://github.com/jmagly/aiwg) | jmagly | 面向 AI 辅助软件开发的认知架构：专用 agent、结构化工作流、多平台部署 | 用户级 | 2026-10-05 |
| 70 | `wait-what` | 停。上一条消息没说明白：重新表述一遍。 |  |  |  | 用户级 | 平台内置 |
| 71 | `wayfinder` | 规划一块庞大的工作(超过一个 agent 会话所能承载)，在 issue 跟踪器上以共享的决策工单地图呈现，并逐一解决，直到通往目标的路径清晰。 |  |  |  | 用户级 | 平台内置 |
| 72 | `wechat-article` | 微信公众号文章：作者-编辑-读者三Agent协作。来源：skills/wechat-article.md. |  |  |  | 用户级 | 平台内置 |
| 73 | `wizard` | 生成一个交互式 bash 向导，带着用户走完只有他们才能执行的步骤。适用于配置基础设施、设置凭据或 CI 密钥、引导陌生的第三方控制台，或执行一次性迁移/切换。不要用于 agent 能自行完成的步骤。 |  |  |  | 用户级 | 平台内置 |
| 74 | `writing-great-skills` | 写好、改好 skill 的参考书——让 skill 可预期所需的词汇与原则。 | [github.com/sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | sickn33 | 本地 agent-first 控制面，包含 2000+ agentic skills 编目 | 用户级 | 2026-10-06 |
| 76 | `codex-bridge-chatgpt` | 当复杂仓库任务需要 ChatGPT 网页推理、而 Codex仍负责本地证据、编辑与测试时使用。⚠️ Codex 专属技能，仅桥接 `~/.codex/skills`；启用前需先取得浏览器自动化授权。2026-10-14 曾短暂退役（判定无实用价值），当日按用户要求装回并恢复治理。来源不可考。 | 来源不可考（无 git / README / 作者声明） | 未知 | 人工粘贴式 ChatGPT 推理桥接 | 用户级（仅 codex） | 2026-09-05 |
| 77 | `codex-with-chatgpt` | 让 ChatGPT 网页版充当 Codex 编码会话的规划与评审大脑，执行权完全留给 Codex；靠 MCP 只读连接器让 ChatGPT 自主读仓库，无需人工粘贴上下文包。❌ 已于 2026-10-14 卸载：本地来源目录与上游 checkout（`/Users/chris/plugins/codex-with-chatgpt`）均已删除，用户判定用不了、不再恢复，登记表条目已移除（内容不存在故无法走 retired 保留流程）。如需再用需重新 clone 上游仓库。 | [github.com/XiaoDuoYa/codex-with-chatgpt](https://github.com/XiaoDuoYa/codex-with-chatgpt) | XiaoDuoYa | C2C 桥接：ChatGPT 只读接入工作区，Codex 保留全部执行权 | 已卸载 | 2026-10-14 |

## 历史参考 Skill 记录（曾被第一方参考或可替代的第三方）

> 本板块收录「第一方 skill 打造时参考的第三方 skill」以及「功能可被第一方 skill 覆盖、不再单独使用的第三方 skill」。表格字段与第三方 skill 表一致（含 skill 范围列）。

| # | Skill 名称 | 中文描述 | 仓库链接 / 来源 | 作者 | 仓库简介 | skill 范围 | 最新更新 |
|---|---|---|---|---|---|---|---|
| 4 | `implement` | 根据规格说明或一组工单来实现某项工作。 |  |  |  | 用户级 | 平台内置 |
| 5 | `to-spec` | 把当前对话转成规格说明并发布到项目 issue 跟踪器——无需访谈，只是把你已讨论内容的综合。 |  |  |  | 用户级 | 平台内置 |
| 6 | `to-tickets` | 把计划、规格或当前对话拆解成一组『追踪子弹』工单，每张标注其阻塞边界，发布到已配置的跟踪器——本地以每工单一个文件、边界以文本呈现，或在真实跟踪器上以原生阻塞链接呈现。 |  |  |  | 用户级 | 平台内置 |
| 7 | `find-skills` | 当用户问『怎么实现 X』『有没有做 X 的 skill』『有没有能…的 skill』，或表达想扩展能力时，帮助发现并安装 agent skill。应在用户寻找可能以可安装 skill 形式存在的功能时使用。 |  |  |  | 用户级 | 平台内置 |
| 8 | `diagnosing-bugs` | 针对难缠 bug 与性能回退的诊断循环。当用户说『diagnose』『debug this』，或报告某东西报错/失败/变慢时使用。已于 2026-09-15 退役为参考：诊断职责由 `wf-diagnose` 承接。 |  |  |  | 用户级 | 平台内置 |

**历史快照合计**：共 **84** 个 skill —— 第一方 **5** + 第三方 **74** + 参考 Skill **5**。该数字仅对应旧表快照，不是当前 141 条策略记录的统计。

> 2026-10-04：新增第三方 `typesafe-ai`（typesafe-ai/skills，TypeSafe System One / Jev 结构化判断原语）。合计 80 → 81，第三方 70 → 71。同时按表格实际行数校正前言计数（原写 6/71/4，实为 5/70/5）。安装前已过安全审计（纯文档、无脚本、无网络执行，P2）。

> 2026-09-15：`diagnosing-bugs` 由第三方表移入参考 Skill 板块（退役为参考，诊断职责由 `wf-diagnose` 承接）。总数不变，第三方 71 → 70、参考 4 → 5。

> 2026-09-15 减 1：第一方 `dev-workflow-2-0` 退役（81 → 80）。技能范围的权威登记表是 `inventory/skill-policy.json`，本表与 `skill-lifecycle.md` 均由其派生。

## 版本更新记录

> **「最新更新」列说明**：
> - 有公开仓库的 skill：取对应仓库 `pushed_at`（上游最后推送日期），同仓库多 skill 共享该日期。
> - WorkBuddy 内置 / 应用市场 skill：无公开仓库，标记为「平台内置」。
> - 自研（本仓库 / 用户自建）skill：无上游仓库，标记为本地 `SKILL.md` 最后修改日期。
> - 可运行 `scripts/refresh_inventory.py` 刷新「最新更新」列。

> **近期更新（2026-10 月）**：
> - 10-06：合计 81 → 84，第三方 71 → 74（新增 `pr` / `retro` / `implement-spec`；`resolving-merge-conflicts` 保留在表内但标注退役，未减数）。第三方表序号已按 skill 名重排。
> - 10-05：**`agent-skill-bridge` 中文化守护修复** —— `cn_guard.sh` 此前调用的 `bridge.py --mode cn` 在 b6933e4 重构中已被删除，脚本成为孤儿；且它用 `grep` 匹配输出判断成败，工具报错时 grep 无匹配 → **误判「守护通过」并 exit 0（假绿灯，会骗过 CI）**。现把 `cn` 能力作为 `manage-skills.py` 的一个模式恢复（只读校验，不自动改写），`bridge.py` 与 `cn_guard.sh` 均转交该模式并直接透传退出码。回归见 `tests/test_cn_guard.py`（11 例）。
> - 10-04：新增第三方 `typesafe-ai`（来源 [github.com/typesafe-ai/skills](https://github.com/typesafe-ai/skills)）。经安全审计为 P2：仅 SKILL.md + LICENSE 纯文档，无脚本、无远程执行、无凭据读取；description 已中文化。

> **近期更新（2026-10 月）**：
> - 10-06：mattpocock/skills v1.3.0 新增 3 个 skill 入池——`implement-spec`（整份规格一次性实现，任务图 + 并行子 agent + 集成分支）、`retro`（编码会话复盘，改进 agent 环境）、`pr`（写 PR 描述，模型自动调用）。三者均由 in-progress 提升为正式 engineering 桶。
> - 10-06：`resolving-merge-conflicts` **退役** —— 上游 v1.3.0 明确移除且无替代（合并/rebase 冲突由 agent 自行处理），源目录移至 `~/.local/share/agent-skills/retired/resolving-merge-conflicts`。
> - 10-06：`ppt-master` v4.5.0 → **v6.6.0**（跨 2 个大版本）。旧 CLI（`template_fill_pptx` / `native_enhance_pptx` / `native_narration_pptx`）及 45 张旧图表 SVG 由上游 `7f000fb8` 主动废弃，本次一并清理；新入口为 `workflows/edit-native-pptx.md` + `scripts/authoring_roundtrip.py`（未改动页面可字节级还原）。

> **近期更新**：
> - 10-10：`requirements-analysis` 改由 workflow-manager 统一维护并直接分发；本仓退役其登记并把完整历史副本移至 `inventory/history/requirements-analysis/`。
> - 10-08：`execution-plan` 改为 dev-flow 项目级技能，旧用户级副本退出公共入口并保留到 `~/.local/share/agent-skills/retired/execution-plan`。
> - 09-15：**`dev-workflow-2-0` 退役** —— 职责已由 M1 `requirements-analysis` / M2 `wf-construction-full-feature` / M3 `execution-plan` 拆分承接。合计 81 → 80，第一方 6 → 5。
> - 09-15：同步移除第三方前言中的「`tdd` 被 `dev-workflow-2-0` 部分覆盖」——覆盖来源消失，`tdd` 视为无覆盖。
> - 09-14：`construction-bootstrap` 退役（见 `skill-policy.json`）。

> **近期更新（2026-08 月）**：
> - 08-24：新增 `eli5`、`video-production`、`remotion-video-production`、`to-questionnaire`、`wait-what`、`wizard`（均为第三方，经 GitHub 核实来源）；移除 4 个 STS2 项目级 skill。
> - 08-24：来源大规模校正——`git-guardrails-claude-code` 等 4 个改归 mattpocock/skills；`skill-creator`/`frontend-design` 归 anthropics/skills；`neat-freak`/`storage-analyzer` 归数字生命卡兹克；`hatch-pet` 归 openai/skills；`skills-security-check` 归腾讯云鼎实验室（WorkBuddy 内置）。
> - 08-22：`agent-skill-bridge` 更新。
> - 08-20：`dev-workflow-2-0` 更新。
> - 08-18：`requirements-analysis` 更新。
> - 08-07：`mattpocock/skills` 上游推送。
> - 08-23：`xbtlin/ai-berkshire` 上游推送。

## 分类说明

> **来源分六类**（对应上表「仓库链接 / 来源」列）：
> 1. **大型集合 / 官方仓库**（整仓克隆后取对应 skill 目录）：
>    - `mattpocock/skills` → 28 个
>    - `JimLiu/baoyu-skills` → 4 个
>    - `xbtlin/ai-berkshire` → 21 个
>    - `anthropics/skills`（Anthropic 官方）→ 2 个
>    - `KKKKhazix/khazix-skills`（数字生命卡兹克）→ 2 个
>    - `openai/skills`（OpenAI 官方）→ 1 个
> 2. **独立仓库（直接克隆对应仓库）**：12 个（agnes-ai-generation-skill、beautiful-html-templates、companion-inc/feynman、frontend-slides、guizang-ppt-skill、humanize-ppt、jmagly/aiwg、akillness/jeo-skills、llm-wiki-app、ppt-master、remotion-video-toolkit、sickn33/agentic-awesome-skills）
> 3. **WorkBuddy 内置 / 应用市场（GitHub 检索未定位独立上游仓库）**：4 个（edit-article、find-skills、obsidian-vault、remotion-best-practices）
> 4. **WorkBuddy 内置（腾讯云鼎实验室出品）**：1 个（skills-security-check）
> 5. **自研（本仓库 / 用户自建）**：本仓 4 个，详见上方「第一方 Skill」板块；`requirements-analysis` 由 workflow-manager 维护，见「其他项目维护的第一方 Skill」

> **体积提示**：以下 5 个 skill 含大体积本地资源，未打包进一键安装脚本，请用其仓库链接单独安装——`ppt-master`、`humanize-ppt`、`beautiful-html-templates`、`baoyu-slide-deck`、`guizang-ppt-skill`。

## 旧安装方式说明（历史记录，不作为当前恢复指令）

> **以下只记录旧安装方式**：旧全量包及旧安装器仅供追溯历史，不得用于重新启用已被第一方替代的 99 份原第三方入口。当前恢复按策略登记的范围执行；本轮原件归档为 reference，恢复也只补回参考位置。
>
> **旧记录中的两种安装方式**
> - **仓库链接安装**：从上游重新拉取，干净但版本可能略新于本机。
> - **一键原样安装（推荐，字节级一致，含本机中文化与私有改动）**：`bash install_all_skills.sh` —— 自动解包到 `~/.agents/skills/` 并桥接到 `~/.workbuddy/skills/` 等目录。脚本已打包 **65 个轻量 skill**；**5 个含大体积本地资源的 skill**（见上「体积提示」）未打包，请用其仓库链接安装。


## 本轮 99 条第一方正式维护源与原件参考映射

本表按 2026-10-15 经审阅的 `formal-policy-preview.json` 生成，列出本轮新增的 99 条 active first-party 映射（98 个 `global` 用户级源 + 1 个 Gawain 项目源）。它是全仓 141 条策略记录的一个子集，不代表全仓第一方总数；正式全量状态请看 [生命周期清单](skill-lifecycle.md)。

「正式维护源」和「原件参考」是不同路径：维护源由正式登记表确定，不等同于原作者/原创声明；原安装快照仅用于历史保留和只读比较，不作为现行入口。上游列只呈现可追溯的来源线索；有来源冲突或未确认时按说明保留，不补造作者和仓库。本轮 99 条映射包含 98 个用户级 `global` 源与 1 个 Gawain 项目源；原有三份未挂接到本轮映射的参考（`tdd`、`diagnosing-bugs`、`neat-freak`）仍单独保留，因此全表 `reference_copies` 为 99 + 3 = 102。正式维护源已本地应用，`apply`、`check` 与实际入口路径独立核验通过；29 项 updater 清退已完成，102 条参考副本在同一正式 bundle 的两个恢复入口验证中均通过。新会话可见性和业务行为仍分别验证。

| Skill | 正式维护源 | 范围 | 原安装快照（来源 → 参考保存位置） | 登记上游/来源线索 |
|---|---|---|---|---|
| `agent-cli-tool-residue-purge` | `my-skills/agent-cli-tool-residue-purge` | 用户级（global） | local-installed-snapshot: `~/.agents/skills/agent-cli-tool-residue-purge` → `~/.local/share/agent-skills/references/agent-cli-tool-residue-purge` | 原始上游未确证；不推断作者或仓库 |
| `agnes-ai-generation-skill` | `my-skills/agnes-ai-generation-skill` | 用户级（global） | installed-snapshot: `~/.agents/skills/agnes-ai-generation-skill` → `~/.local/share/agent-skills/references/agnes-ai-generation-skill` | 历史来源清单：[github.com/Yacey/agnes-ai-generation-skill](https://github.com/Yacey/agnes-ai-generation-skill)；inventory/skill-desc-translation.md 记录 GitHub Yacey/agnes-ai-generation-skill。 |
| `ask-matt` | `my-skills/ask-matt` | 用户级（global） | installed-snapshot: `~/.agents/skills/ask-matt` → `~/.local/share/agent-skills/references/ask-matt` | 旧来源表线索：[仓库/来源](https://github.com/mattpocock/skills)（历史归属，非作者结论） |
| `baoyu-comic` | `my-skills/baoyu-comic` | 用户级（global） | installed-snapshot: `~/.agents/skills/baoyu-comic` → `~/.local/share/agent-skills/references/baoyu-comic` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-comic) |
| `baoyu-image-gen` | `my-skills/baoyu-image-gen` | 用户级（global） | installed-snapshot: `~/.agents/skills/baoyu-image-gen` → `~/.local/share/agent-skills/references/baoyu-image-gen` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-image-gen)；来源说明：原 SKILL.md 的 homepage 指向 JimLiu/baoyu-skills；inventory/skill-desc-translation.md 将来源列为平台内置。并存记录，不推断安装来源。 |
| `baoyu-infographic` | `my-skills/baoyu-infographic` | 用户级（global） | installed-snapshot: `~/.agents/skills/baoyu-infographic` → `~/.local/share/agent-skills/references/baoyu-infographic` | [登记来源链接](https://github.com/JimLiu/baoyu-skills#baoyu-infographic)；来源说明：原 SKILL.md 的 homepage 指向 JimLiu/baoyu-skills；inventory/skill-desc-translation.md 将来源列为平台内置。并存记录，不推断安装来源。 |
| `bottleneck-hunter` | `my-skills/bottleneck-hunter` | 用户级（global） | installed-snapshot: `~/.agents/skills/bottleneck-hunter` → `~/.local/share/agent-skills/references/bottleneck-hunter` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `clashx-openai-sse-debug` | `my-skills/clashx-openai-sse-debug` | 用户级（global） | local-installed-snapshot: `~/.agents/skills/clashx-openai-sse-debug` → `~/.local/share/agent-skills/references/clashx-openai-sse-debug` | 原始上游未确证；不推断作者或仓库 |
| `code-review` | `my-skills/code-review` | 用户级（global） | installed-snapshot: `~/.agents/skills/code-review` → `~/.local/share/agent-skills/references/code-review` | 原始上游未确证；不推断作者或仓库 |
| `codebase-design` | `my-skills/codebase-design` | 用户级（global） | installed-snapshot: `~/.agents/skills/codebase-design` → `~/.local/share/agent-skills/references/codebase-design` | 原始上游未确证；不推断作者或仓库 |
| `deep-company-series` | `my-skills/deep-company-series` | 用户级（global） | installed-snapshot: `~/.agents/skills/deep-company-series` → `~/.local/share/agent-skills/references/deep-company-series` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `domain-modeling` | `my-skills/domain-modeling` | 用户级（global） | installed-snapshot: `~/.agents/skills/domain-modeling` → `~/.local/share/agent-skills/references/domain-modeling` | 原始上游未确证；不推断作者或仓库 |
| `duplicate-cli-unify` | `my-skills/duplicate-cli-unify` | 用户级（global） | local-installed-snapshot: `~/.agents/skills/duplicate-cli-unify` → `~/.local/share/agent-skills/references/duplicate-cli-unify` | 原始上游未确证；不推断作者或仓库 |
| `dyp-ask` | `my-skills/dyp-ask` | 用户级（global） | installed-snapshot: `~/.agents/skills/dyp-ask` → `~/.local/share/agent-skills/references/dyp-ask` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `earnings-review` | `my-skills/earnings-review` | 用户级（global） | installed-snapshot: `~/.agents/skills/earnings-review` → `~/.local/share/agent-skills/references/earnings-review` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `earnings-team` | `my-skills/earnings-team` | 用户级（global） | installed-snapshot: `~/.agents/skills/earnings-team` → `~/.local/share/agent-skills/references/earnings-team` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `edit-article` | `my-skills/edit-article` | 用户级（global） | installed-snapshot: `~/.agents/skills/edit-article` → `~/.local/share/agent-skills/references/edit-article` | 历史来源清单：WorkBuddy 内置 / 应用市场；inventory/skill-desc-translation.md 将其列为 WorkBuddy/平台内置；未将其改称独立 GitHub 上游。 |
| `eli5` | `my-skills/eli5` | 用户级（global） | installed-snapshot: `~/.agents/skills/eli5` → `~/.local/share/agent-skills/references/eli5` | 历史来源清单：[github.com/companion-inc/feynman](https://github.com/companion-inc/feynman)；inventory/skill-desc-translation.md 记录 GitHub companion-inc/feynman。 |
| `financial-data` | `my-skills/financial-data` | 用户级（global） | installed-snapshot: `~/.agents/skills/financial-data` → `~/.local/share/agent-skills/references/financial-data` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `frontend-design` | `my-skills/frontend-design` | 用户级（global） | installed-snapshot: `~/.agents/skills/frontend-design` → `~/.local/share/agent-skills/references/frontend-design` | 历史来源清单：[github.com/anthropics/skills](https://github.com/anthropics/skills)；inventory/skill-desc-translation.md 记录 Anthropic 官方 skills 仓库。 |
| `git-guardrails-claude-code` | `my-skills/git-guardrails-claude-code` | 用户级（global） | installed-snapshot: `~/.agents/skills/git-guardrails-claude-code` → `~/.local/share/agent-skills/references/git-guardrails-claude-code` | 原始上游未确证；不推断作者或仓库 |
| `grill-me` | `my-skills/grill-me` | 用户级（global） | installed-snapshot: `~/.agents/skills/grill-me` → `~/.local/share/agent-skills/references/grill-me` | 原始上游未确证；不推断作者或仓库 |
| `grill-with-docs` | `my-skills/grill-with-docs` | 用户级（global） | installed-snapshot: `~/.agents/skills/grill-with-docs` → `~/.local/share/agent-skills/references/grill-with-docs` | 原始上游未确证；不推断作者或仓库 |
| `grilling` | `my-skills/grilling` | 用户级（global） | installed-snapshot: `~/.agents/skills/grilling` → `~/.local/share/agent-skills/references/grilling` | 原始上游未确证；不推断作者或仓库 |
| `handoff` | `my-skills/handoff` | 用户级（global） | installed-snapshot: `~/.agents/skills/handoff` → `~/.local/share/agent-skills/references/handoff` | 旧来源表线索：[仓库/来源](https://github.com/mattpocock/skills)（历史归属，非作者结论） |
| `hatch-pet` | `my-skills/hatch-pet` | 用户级（global） | installed-snapshot: `~/.agents/skills/hatch-pet` → `~/.local/share/agent-skills/references/hatch-pet` | 历史来源清单：[github.com/openai/skills](https://github.com/openai/skills)；inventory/skill-desc-translation.md 记录 OpenAI 官方 skills 仓库。 |
| `implement-spec` | `my-skills/implement-spec` | 用户级（global） | installed-snapshot: `~/.agents/skills/implement-spec` → `~/.local/share/agent-skills/references/implement-spec` | [登记来源链接](https://github.com/mattpocock/skills/tree/main/skills/engineering/implement-spec) |
| `improve-codebase-architecture` | `my-skills/improve-codebase-architecture` | 用户级（global） | installed-snapshot: `~/.agents/skills/improve-codebase-architecture` → `~/.local/share/agent-skills/references/improve-codebase-architecture` | 原始上游未确证；不推断作者或仓库 |
| `income-investment` | `my-skills/income-investment` | 用户级（global） | installed-snapshot: `~/.agents/skills/income-investment` → `~/.local/share/agent-skills/references/income-investment` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `industry-funnel` | `my-skills/industry-funnel` | 用户级（global） | installed-snapshot: `~/.agents/skills/industry-funnel` → `~/.local/share/agent-skills/references/industry-funnel` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `industry-research` | `my-skills/industry-research` | 用户级（global） | installed-snapshot: `~/.agents/skills/industry-research` → `~/.local/share/agent-skills/references/industry-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `investment-checklist` | `my-skills/investment-checklist` | 用户级（global） | installed-snapshot: `~/.agents/skills/investment-checklist` → `~/.local/share/agent-skills/references/investment-checklist` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `investment-memo-craft` | `my-skills/investment-memo-craft` | 用户级（global） | installed-snapshot: `~/.agents/skills/investment-memo-craft` → `~/.local/share/agent-skills/references/investment-memo-craft` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `investment-research` | `my-skills/investment-research` | 用户级（global） | installed-snapshot: `~/.agents/skills/investment-research` → `~/.local/share/agent-skills/references/investment-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `investment-team` | `my-skills/investment-team` | 用户级（global） | installed-snapshot: `~/.agents/skills/investment-team` → `~/.local/share/agent-skills/references/investment-team` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `lark-approval` | `my-skills/lark-approval` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-approval` → `~/.local/share/agent-skills/references/lark-approval` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-approval.tar.gz) |
| `lark-apps` | `my-skills/lark-apps` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-apps` → `~/.local/share/agent-skills/references/lark-apps` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-apps.tar.gz) |
| `lark-attendance` | `my-skills/lark-attendance` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-attendance` → `~/.local/share/agent-skills/references/lark-attendance` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-attendance.tar.gz) |
| `lark-base` | `my-skills/lark-base` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-base` → `~/.local/share/agent-skills/references/lark-base` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-base.tar.gz) |
| `lark-calendar` | `my-skills/lark-calendar` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-calendar` → `~/.local/share/agent-skills/references/lark-calendar` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-calendar.tar.gz) |
| `lark-contact` | `my-skills/lark-contact` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-contact` → `~/.local/share/agent-skills/references/lark-contact` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-contact.tar.gz) |
| `lark-doc` | `my-skills/lark-doc` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-doc` → `~/.local/share/agent-skills/references/lark-doc` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-doc.tar.gz) |
| `lark-drive` | `my-skills/lark-drive` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-drive` → `~/.local/share/agent-skills/references/lark-drive` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-drive.tar.gz) |
| `lark-event` | `my-skills/lark-event` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-event` → `~/.local/share/agent-skills/references/lark-event` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-event.tar.gz) |
| `lark-im` | `my-skills/lark-im` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-im` → `~/.local/share/agent-skills/references/lark-im` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-im.tar.gz) |
| `lark-mail` | `my-skills/lark-mail` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-mail` → `~/.local/share/agent-skills/references/lark-mail` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-mail.tar.gz) |
| `lark-markdown` | `my-skills/lark-markdown` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-markdown` → `~/.local/share/agent-skills/references/lark-markdown` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-markdown.tar.gz) |
| `lark-meeting` | `my-skills/lark-meeting` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-meeting` → `~/.local/share/agent-skills/references/lark-meeting` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-meeting.tar.gz) |
| `lark-minutes` | `my-skills/lark-minutes` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-minutes` → `~/.local/share/agent-skills/references/lark-minutes` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-minutes.tar.gz) |
| `lark-note` | `my-skills/lark-note` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-note` → `~/.local/share/agent-skills/references/lark-note` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-note.tar.gz) |
| `lark-okr` | `my-skills/lark-okr` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-okr` → `~/.local/share/agent-skills/references/lark-okr` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-okr.tar.gz) |
| `lark-openapi-explorer` | `my-skills/lark-openapi-explorer` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-openapi-explorer` → `~/.local/share/agent-skills/references/lark-openapi-explorer` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-openapi-explorer.tar.gz) |
| `lark-shared` | `my-skills/lark-shared` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-shared` → `~/.local/share/agent-skills/references/lark-shared` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-shared.tar.gz) |
| `lark-sheets` | `my-skills/lark-sheets` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-sheets` → `~/.local/share/agent-skills/references/lark-sheets` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-sheets.tar.gz) |
| `lark-skill-maker` | `my-skills/lark-skill-maker` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-skill-maker` → `~/.local/share/agent-skills/references/lark-skill-maker` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-skill-maker.tar.gz) |
| `lark-slides` | `my-skills/lark-slides` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-slides` → `~/.local/share/agent-skills/references/lark-slides` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-slides.tar.gz) |
| `lark-task` | `my-skills/lark-task` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-task` → `~/.local/share/agent-skills/references/lark-task` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-task.tar.gz) |
| `lark-vc` | `my-skills/lark-vc` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-vc` → `~/.local/share/agent-skills/references/lark-vc` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-vc.tar.gz) |
| `lark-vc-agent` | `my-skills/lark-vc-agent` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-vc-agent` → `~/.local/share/agent-skills/references/lark-vc-agent` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-vc-agent.tar.gz) |
| `lark-whiteboard` | `my-skills/lark-whiteboard` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-whiteboard` → `~/.local/share/agent-skills/references/lark-whiteboard` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-whiteboard.tar.gz) |
| `lark-wiki` | `my-skills/lark-wiki` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-wiki` → `~/.local/share/agent-skills/references/lark-wiki` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-wiki.tar.gz) |
| `lark-workflow-meeting-summary` | `my-skills/lark-workflow-meeting-summary` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-workflow-meeting-summary` → `~/.local/share/agent-skills/references/lark-workflow-meeting-summary` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-workflow-meeting-summary.tar.gz) |
| `lark-workflow-standup-report` | `my-skills/lark-workflow-standup-report` | 用户级（global） | installed-snapshot: `~/.agents/skills/lark-workflow-standup-report` → `~/.local/share/agent-skills/references/lark-workflow-standup-report` | [登记来源链接](https://open.feishu.cn/lark-cli/skills/regular/.well-known/agent-skills/lark-workflow-standup-report.tar.gz) |
| `llm-wiki-app` | `my-skills/llm-wiki-app` | 用户级（global） | installed-snapshot: `~/.agents/skills/llm-wiki-app` → `~/.local/share/agent-skills/references/llm-wiki-app` | 未确证独立上游；仓库登记与包内来源一致。 |
| `management-deep-dive` | `my-skills/management-deep-dive` | 用户级（global） | installed-snapshot: `~/.agents/skills/management-deep-dive` → `~/.local/share/agent-skills/references/management-deep-dive` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `migrate-to-shoehorn` | `my-skills/migrate-to-shoehorn` | 用户级（global） | installed-snapshot: `~/.agents/skills/migrate-to-shoehorn` → `~/.local/share/agent-skills/references/migrate-to-shoehorn` | 未确证独立上游；不据此推断独立作者或 Git 仓库。 |
| `news-pulse` | `my-skills/news-pulse` | 用户级（global） | installed-snapshot: `~/.agents/skills/news-pulse` → `~/.local/share/agent-skills/references/news-pulse` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `obsidian-vault` | `my-skills/obsidian-vault` | 用户级（global） | installed-snapshot: `~/.agents/skills/obsidian-vault` → `~/.local/share/agent-skills/references/obsidian-vault` | 未确证独立上游；inventory/skill-desc-translation.md 将其列为 WorkBuddy/平台内置；未将其改称独立 GitHub 上游。 |
| `portfolio-review` | `my-skills/portfolio-review` | 用户级（global） | installed-snapshot: `~/.agents/skills/portfolio-review` → `~/.local/share/agent-skills/references/portfolio-review` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `pr` | `my-skills/pr` | 用户级（global） | installed-snapshot: `~/.agents/skills/pr` → `~/.local/share/agent-skills/references/pr` | [登记来源链接](https://github.com/mattpocock/skills/tree/main/skills/engineering/pr) |
| `private-company-research` | `my-skills/private-company-research` | 用户级（global） | installed-snapshot: `~/.agents/skills/private-company-research` → `~/.local/share/agent-skills/references/private-company-research` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `prototype` | `my-skills/prototype` | 用户级（global） | installed-snapshot: `~/.agents/skills/prototype` → `~/.local/share/agent-skills/references/prototype` | 原始上游未确证；不推断作者或仓库 |
| `quality-screen` | `my-skills/quality-screen` | 用户级（global） | installed-snapshot: `~/.agents/skills/quality-screen` → `~/.local/share/agent-skills/references/quality-screen` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `remotion-best-practices` | `my-skills/remotion-best-practices` | 用户级（global） | installed-snapshot: `~/.agents/skills/remotion-best-practices` → `~/.local/share/agent-skills/references/remotion-best-practices` | 未确证独立上游；inventory/skill-desc-translation.md 将其列为 WorkBuddy/平台内置；未将其改称独立 GitHub 上游。 |
| `remotion-video-production` | `my-skills/remotion-video-production` | 用户级（global） | installed-snapshot: `~/.agents/skills/remotion-video-production` → `~/.local/share/agent-skills/references/remotion-video-production` | 历史来源清单：[github.com/akillness/jeo-skills](https://github.com/akillness/jeo-skills)；inventory/skill-desc-translation.md 记录 akillness/jeo-skills；当前包作为兼容别名。 |
| `remotion-video-toolkit` | `my-skills/remotion-video-toolkit` | 用户级（global） | installed-snapshot: `~/.agents/skills/remotion-video-toolkit` → `~/.local/share/agent-skills/references/remotion-video-toolkit` | 历史来源清单：[github.com/shreefentsar/remotion-video-toolkit](https://github.com/shreefentsar/remotion-video-toolkit)；inventory/skill-desc-translation.md 记录 shreefentsar/remotion-video-toolkit。 |
| `research` | `my-skills/research` | 用户级（global） | installed-snapshot: `~/.agents/skills/research` → `~/.local/share/agent-skills/references/research` | 原始上游未确证；不推断作者或仓库 |
| `retro` | `my-skills/retro` | 用户级（global） | installed-snapshot: `~/.agents/skills/retro` → `~/.local/share/agent-skills/references/retro` | [登记来源链接](https://github.com/mattpocock/skills/tree/main/skills/engineering/retro) |
| `scaffold-exercises` | `my-skills/scaffold-exercises` | 用户级（global） | installed-snapshot: `~/.agents/skills/scaffold-exercises` → `~/.local/share/agent-skills/references/scaffold-exercises` | 未确证独立上游；不补造独立 GitHub 来源。 |
| `setup-matt-pocock-skills` | `my-skills/setup-matt-pocock-skills` | 用户级（global） | installed-snapshot: `~/.agents/skills/setup-matt-pocock-skills` → `~/.local/share/agent-skills/references/setup-matt-pocock-skills` | 原始上游未确证；不推断作者或仓库 |
| `setup-pre-commit` | `my-skills/setup-pre-commit` | 用户级（global） | installed-snapshot: `~/.agents/skills/setup-pre-commit` → `~/.local/share/agent-skills/references/setup-pre-commit` | 未确证独立上游；不推断独立作者或仓库来源。 |
| `skill-workbench` | `my-skills/skill-workbench` | 用户级（global） | installed-snapshot: `~/.agents/skills/skill-creator` → `~/.local/share/agent-skills/references/skill-creator` | 原始上游未确证；不推断作者或仓库 |
| `storage-analyzer` | `my-skills/storage-analyzer` | 用户级（global） | installed-snapshot: `~/.agents/skills/storage-analyzer` → `~/.local/share/agent-skills/references/storage-analyzer` | 原始上游未确证；不推断作者或仓库 |
| `sts2-gawain-regression-recovery` | `project:gawain/skills/sts2-gawain-regression-recovery` | Gawain 项目（gawain） | installed-snapshot: `~/.agents/skills/sts2-gawain-regression-recovery` → `~/.local/share/agent-skills/references/sts2-gawain-regression-recovery` | 当前 Gawain 项目维护源已知；原作者与最初上游未确证 |
| `sts2-independent-run-regression` | `my-skills/sts2-independent-run-regression` | 用户级（global） | installed-snapshot: `~/.agents/skills/sts2-independent-run-regression` → `~/.local/share/agent-skills/references/sts2-independent-run-regression` | 由本仓接管维护；原作者与最初上游未确证，不推断作者或仓库 |
| `sts2-start-game` | `my-skills/sts2-start-game` | 用户级（global） | installed-snapshot: `~/.agents/skills/sts2-start-game` → `~/.local/share/agent-skills/references/sts2-start-game` | 已知 Git 来源：`crystepj-max/STS2-AUTOTEST`；技能路径提交 `860ed5048ee4f4101046c213728bfdb618b4478d`，审计 HEAD `41f89387fa31d8208b277054828b6de00efe6eaf`。当前维护源从安装快照接管并保留其改进；该提交不代表安装版哈希或原创作者确证。 |
| `teach` | `my-skills/teach` | 用户级（global） | installed-snapshot: `~/.agents/skills/teach` → `~/.local/share/agent-skills/references/teach` | 未确证独立上游；来源为历史平台记录；没有独立上游仓库可确认。 |
| `test-report-html` | `my-skills/test-report-html` | 用户级（global） | installed-snapshot: `~/.agents/skills/test-report-html` → `~/.local/share/agent-skills/references/test-report-html` | 未确证独立上游；维护 inventory 与当前 skill-lock 均未找到该项；未发现可证实来源，不虚构仓库。 |
| `thesis-drift` | `my-skills/thesis-drift` | 用户级（global） | installed-snapshot: `~/.agents/skills/thesis-drift` → `~/.local/share/agent-skills/references/thesis-drift` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `thesis-tracker` | `my-skills/thesis-tracker` | 用户级（global） | installed-snapshot: `~/.agents/skills/thesis-tracker` → `~/.local/share/agent-skills/references/thesis-tracker` | [登记来源链接](https://github.com/xbtlin/ai-berkshire) |
| `to-questionnaire` | `my-skills/to-questionnaire` | 用户级（global） | installed-snapshot: `~/.agents/skills/to-questionnaire` → `~/.local/share/agent-skills/references/to-questionnaire` | 原始上游未确证；不推断作者或仓库 |
| `triage` | `my-skills/triage` | 用户级（global） | installed-snapshot: `~/.agents/skills/triage` → `~/.local/share/agent-skills/references/triage` | 原始上游未确证；不推断作者或仓库 |
| `typesafe-ai` | `my-skills/typesafe-ai` | 用户级（global） | installed-snapshot: `~/.agents/skills/typesafe-ai` → `~/.local/share/agent-skills/references/typesafe-ai` | [登记来源链接](https://github.com/typesafe-ai/skills.git) |
| `video-production` | `my-skills/video-production` | 用户级（global） | installed-snapshot: `~/.agents/skills/video-production` → `~/.local/share/agent-skills/references/video-production` | 历史来源清单：[github.com/jmagly/aiwg](https://github.com/jmagly/aiwg)；inventory/skill-desc-translation.md 记录 jmagly/aiwg。 |
| `wait-what` | `my-skills/wait-what` | 用户级（global） | installed-snapshot: `~/.agents/skills/wait-what` → `~/.local/share/agent-skills/references/wait-what` | 原始上游未确证；不推断作者或仓库 |
| `wayfinder` | `my-skills/wayfinder` | 用户级（global） | installed-snapshot: `~/.agents/skills/wayfinder` → `~/.local/share/agent-skills/references/wayfinder` | 原始上游未确证；不推断作者或仓库 |
| `wechat-article` | `my-skills/wechat-article` | 用户级（global） | installed-snapshot: `~/.agents/skills/wechat-article` → `~/.local/share/agent-skills/references/wechat-article` | 未确证独立上游；tools/add_repo_column.py 将其映射到 ai-berkshire 且该仓存在同名 canonical/generated 文件；inventory 行记“平台内置”。正文匹配度只作定位，报告保留该冲突。 |
| `wizard` | `my-skills/wizard` | 用户级（global） | installed-snapshot: `~/.agents/skills/wizard` → `~/.local/share/agent-skills/references/wizard` | 原始上游未确证；不推断作者或仓库 |
| `writing-great-skills` | `my-skills/writing-great-skills` | 用户级（global） | installed-snapshot: `~/.agents/skills/writing-great-skills` → `~/.local/share/agent-skills/references/writing-great-skills` | 未确证独立上游；证据支持“Matt Pocock/mattpocock/skills 为上游作者及技能来源，sickn33/agentic-awesome-skills 为目录/分发记录”并存。检查 ~/.agents/.skill-lock.json 未发现此技能的 lock 项，因此精确安装来源和安装 commit 未确证。 |
