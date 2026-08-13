# 公共池 Skill 中文描述总表（共 73 个）

> 生成：2026-08-02 ｜ 范围：公共池 `~/.agents/skills/`（codex / claude / workbuddy 三端经软链同步中文）

> 说明：53 个 Claude 插件 skill 按规则①未改动，仍为英文。

> **新增「仓库链接 / 来源」列（2026-08-04）**：用于在另一台电脑原样安装。来源分四类：
> 1. **大型集合仓库（整仓克隆后取对应 skill 目录）**：
>    - `mattpocock/skills` → 25 个（ask-matt、code-review、codebase-design、diagnosing-bugs、domain-modeling、grill-me、grilling、handoff、implement、improve-codebase-architecture、prototype、resolving-merge-conflicts、teach、to-spec、to-tickets、triage、tdd、wayfinder、writing-great-skills、grill-with-docs、research、setup-matt-pocock-skills、wizard、to-questionnaire、wait-what）
>    - `JimLiu/baoyu-skills` → 4 个（baoyu-comic、baoyu-image-gen、baoyu-infographic、baoyu-slide-deck）
>    - `xbtlin/ai-berkshire` → 21 个（bottleneck-hunter、deep-company-series、dyp-ask、earnings-review、earnings-team、financial-data、income-investment、industry-funnel、industry-research、investment-checklist、investment-memo-craft、investment-research、investment-team、management-deep-dive、portfolio-review、private-company-research、quality-screen、thesis-drift、thesis-tracker、wechat-article、news-pulse）
> 2. **独立仓库（直接克隆对应仓库）**：agnes-ai-generation-skill、beautiful-html-templates、frontend-slides、guizang-ppt-skill、humanize-ppt、llm-wiki、remotion-video-toolkit、ppt-master（共 8 个）
> 3. **WorkBuddy 内置 / 应用市场（无独立公开仓库）**：edit-article、find-skills、frontend-design、git-guardrails-claude-code、hatch-pet、migrate-to-shoehorn、neat-freak、obsidian-vault、remotion-best-practices、remotion-video-production、scaffold-exercises、setup-pre-commit、skill-creator、storage-analyzer、video-production（共 15 个）→ 用下方「一键原样脚本」安装
>
> **两种安装方式**
> - **仓库链接安装**：从上游重新拉取，干净但版本可能略新于本机。
> - **一键原样安装（推荐，字节级一致，含本机中文化与私有改动）**：`bash install_all_skills.sh` —— 自动解包到 `~/.agents/skills/` 并桥接到 `~/.workbuddy/skills` 等目录。脚本已打包 **65 个轻量 skill**；**5 个含大体积本地资源的 skill**（ppt-master / humanize-ppt / beautiful-html-templates / baoyu-slide-deck / guizang-ppt-skill，标注「体积大」）未打包，请用其仓库链接安装。


|---|---|---|---|

|---|---|---|---|---|


> **新增「最新更新」列（2026-08-11）**：通过各仓库 `pushed_at` 自动获取，按来源分类展示。无公开仓库的 WorkBuddy 内置/市场 skill 标记为「平台内置」。
|---|---|---|---|---|


> **「最新更新」列**：通过各仓库 `pushed_at` 自动获取，按来源分类展示。无公开仓库的 WorkBuddy 内置/市场 skill 标记为「平台内置」。可运行 `scripts/refresh_inventory.py` 刷新。
|---|---|---|---|---|


> **「最新更新」列**：通过各仓库 `pushed_at` 自动获取，按来源分类展示。无公开仓库的 WorkBuddy 内置/市场 skill 标记为「平台内置」。可运行 `scripts/refresh_inventory.py` 刷新。
|---|---|---|---|---|


> **「最新更新」列**：通过各仓库 `pushed_at` 自动获取，按来源分类展示。无公开仓库的 WorkBuddy 内置/市场 skill 标记为「平台内置」。可运行 `scripts/refresh_inventory.py` 刷新。
|---|---|---|---|---|


> **「最新更新」列**：通过各仓库 `pushed_at` 自动获取，按来源分类展示。无公开仓库的 WorkBuddy 内置/市场 skill 标记为「平台内置」。可运行 `scripts/refresh_inventory.py` 刷新。
| # | Skill 名称 | 中文描述 | 仓库链接 / 来源 | 最新更新 |
|---|---|---|---|---|
| 1 | `agnes-ai-generation-skill` | 调用 Agnes AI / Sapiens AI 的生成接口，支持文本、图像、视频。当用户要使用 Agnes 模型、Agnes 图像/视频、Agnes 2.0 Flash、apihub.agnes-ai.com，或要生成文本、图像、编辑图像、创作视频、让图像动起来、生成关键帧视频，或测试 Agnes API 时。 | [github.com/Yacey/agnes-ai-generation-skill](https://github.com/Yacey/agnes-ai-generation-skill) | N/A |
| 2 | `ask-matt` | 询问哪个 skill 或流程适合当前情况。相当于本仓库 skills 的路由器。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 3 | `baoyu-comic` | 基于多种艺术风格与基调的知识漫画创作工具，可生成原创教育漫画，含分镜排版与连贯的图像生成。当用户要创作『知识漫画』『教育漫画』『传记漫画』『教程漫画』或 Logicomix 风格的漫画时使用。 | [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) | N/A |
| 4 | `baoyu-image-gen` | 基于 OpenAI、Google、DashScope 接口的 AI 图像生成。支持文生图、参考图、多种宽高比。默认串行生成，可按需并行。当用户要生成、创作或绘制图像时使用。 | [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) | N/A |
| 5 | `baoyu-infographic` | 专业信息图生成工具，提供 20 种版式与 17 种视觉风格。会分析内容、推荐『版式×风格』组合并生成可直接发布的成品信息图。当用户要制作信息图、数据可视化海报或一页式图解时使用。 | [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) | N/A |
| 6 | `baoyu-slide-deck` | 根据内容生成专业的幻灯片图像。先生成带风格说明的大纲，再逐页生成幻灯片图。当用户说『做幻灯片』『做演示』『生成 deck』『slide deck』或『PPT』时使用。 | [github.com/JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills)（体积大，建议用仓库链接安装，未打包进脚本） | N/A |
| 7 | `beautiful-html-templates` | 英文 HTML 演讲稿渲染与模板选择。用于在 humanize-ppt 已完成大纲和逐页意图后，从上游模板库选择并渲染英文演示文稿。使用前阅读本目录的 AGENTS.md 与 index.json；不负责大纲、观众状态或演讲体检。 | [github.com/zarazhangrui/beautiful-html-templates](https://github.com/zarazhangrui/beautiful-html-templates)（体积大，建议用仓库链接安装，未打包进脚本） | 2026-06-09 |
| 8 | `bottleneck-hunter` | 供应链瓶颈猎手：AI驱动的全球产业链瓶颈套利。来源：skills/bottleneck-hunter.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 9 | `code-review` | 针对某个基准点(提交/分支/标签/merge-base)之后的改动做审查，分两个维度——规范(代码是否遵循本仓库编码规范?)与需求(代码是否匹配原始 issue/PRD 的要求?)。两个维度并行由子 agent 审查并并排汇报。当用户要审查分支、PR、进行中的改动，或说『review since X』时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 10 | `codebase-design` | 设计深层模块时的共享词汇表。当用户要设计或改进某模块的接口、寻找深化机会、决定接缝位置、让代码更易测试或更利于 AI 导航，或别的 skill 需要深层模块词汇时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 11 | `deep-company-series` | 深度公司系列：8 篇长文拆一家公司。来源：skills/deep-company-series.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 12 | `diagnosing-bugs` | 针对难缠 bug 与性能回退的诊断循环。当用户说『diagnose』『debug this』，或报告某东西报错/失败/变慢时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 13 | `domain-modeling` | 构建并打磨项目的领域模型。当用户要敲定领域术语或通用语言、记录架构决策，或别的 skill 需要维护领域模型时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 14 | `dyp-ask` | 段永平问答：以他的方式思考。来源：skills/dyp-ask.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 15 | `earnings-review` | 财报精读：一手资料深度解读。来源：skills/earnings-review.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 16 | `earnings-team` | 财报精读团队：四大师并行解读 + 公众号发布。来源：skills/earnings-team.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 17 | `edit-article` | 通过重组章节、提升清晰度、收紧文风来编辑润色文章。当用户要编辑、修订或改进文章草稿时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 18 | `financial-data` | 财务数据获取与交叉验证规范。来源：skills/financial-data.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 19 | `find-skills` | 当用户问『怎么实现 X』『有没有做 X 的 skill』『有没有能…的 skill』，或表达想扩展能力时，帮助发现并安装 agent skill。应在用户寻找可能以可安装 skill 形式存在的功能时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 20 | `frontend-design` | 构建新界面或重塑旧界面时，提供独特、有意图的视觉设计指引。帮助确定美学方向、排版，以及做出不像模板默认值的取舍。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 21 | `frontend-slides` | 从零创建动画丰富的 HTML 演示，或将 PowerPoint 文件转换而来。当用户要制作演示、把 PPT/PPTX 转成网页、或为演讲/路演做幻灯片时使用。通过可视化探索(而非抽象选项)帮助非设计者找到自己的美学。 | [github.com/zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) | 2026-06-23 |
| 22 | `git-guardrails-claude-code` | 在危险 git 命令(push、reset --hard、clean、branch -D 等)执行前，用 Claude Code hooks 拦截。当用户想防止破坏性 git 操作、添加 git 安全钩子，或在 Claude Code 中阻止 git push/reset 时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 23 | `grill-me` | 一场毫不留情的追问式访谈，用来打磨计划或设计。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 24 | `grill-with-docs` | 一场毫不留情的追问式访谈，用来打磨计划或设计，同时边聊边产出文档(ADR 与术语表)。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 25 | `grilling` | 就某个计划、决策或想法对用户穷追不舍地追问。当用户想压力测试自己的思路，或使用了任何『grill』触发词时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 26 | `guizang-ppt-skill` | 生成横向翻页网页 PPT（单 HTML 文件），含 WebGL 背景、章节幕封、数据大字报、图片网格等模板。提供两种风格：① "电子杂志 × 电子墨水"（衬线 + 流体背景 + 暖色） ② "瑞士国际主义"（无衬线 + 网格点阵 + IKB/柠檬黄/柠檬绿/安全橙高亮）。当用户需要制作分享 / 演讲 / 发布会风格的网页 PPT，或提到"杂志风 PPT"、"瑞士风 PPT"、"Swiss Style"、"horizontal swipe deck"时使用。 | [github.com/op7418/guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)（体积大，建议用仓库链接安装，未打包进脚本） | N/A |
| 27 | `handoff` | 把当前对话压缩成一份交接文档，供另一个 agent 接手。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 28 | `hatch-pet` | 从角色原画、生成图、公司/客户品牌线索或视觉参考中，创建、修复、校验、可视化 QA，并打包兼容 Codex 的 v2 动画宠物。适用于任何新的 Codex 宠物、自定义吉祥物、非像素风宠物、品牌灵感宠物、已有宠物修复，或需要 9 行标准动画、16 个朝向、确定性装配、QA 产物与 spriteVersionNumber 2 打包的 8x11 雪碧图流程。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 29 | `humanize-ppt` | 为 Agent 生成的 PPT 做『人性化』润色——把原始素材转成以听众心智转化为目标的结构化演讲，而非模板堆砌。当用户要制作演讲/PPT/幻灯片，或希望内容有叙事与节奏时使用。 | [github.com/LearnPrompt/humanize-ppt](https://github.com/LearnPrompt/humanize-ppt)（体积大，建议用仓库链接安装，未打包进脚本） | 2026-07-31 |
| 30 | `implement` | 根据规格说明或一组工单来实现某项工作。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 31 | `improve-codebase-architecture` | 扫描代码库寻找深化机会，以可视化 HTML 报告呈现，再就你选定的那一项展开追问式打磨。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 32 | `income-investment` | 收益投资——稳健与机会主义的分配分析。来源：skills/income-investment.md。 | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 33 | `industry-funnel` | 行业漏斗筛选：从全市场到 3 家的价值投资精选流程。来源：skills/industry-funnel.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 34 | `industry-research` | 行业投资研究：产业链全景扫描 + 四大师个股分析框架。来源：skills/industry-research.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 35 | `investment-checklist` | 巴菲特价值投资买入前 Checklist。来源：skills/investment-checklist.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 36 | `investment-memo-craft` | 仅 Codex 使用的写作与排版层，用于 AI Berkshire 投资研究报告的撰写。每当 Codex 创建、重写、修订或批评公司/行业/基金研究报告，尤其是需要财务严谨、可读的商业机理、逆向分析、估值到行动的指引、针对投资人的建议、克制的排版与清晰的买入/持有/卖出信号的长文 Markdown 报告时使用。不要用它修改 Claude Code 斜杠命令源。 | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 37 | `investment-research` | 投资研究：巴菲特-芒格-段永平-李录 四大师综合分析框架。来源：skills/investment-research.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 38 | `investment-team` | 投研团队：四角色并行分析框架。来源：skills/investment-team.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 39 | `llm-wiki` | 查询用户的 LLM Wiki 知识库（运行在 127.0.0.1:19828 的 LLM Wiki 桌面应用，并非 Obsidian、Notion、Apple Notes、Logseq 或其他 PKM 工具）。仅当用户明确提到 LLM Wiki 时使用。 | [github.com/nashsu/llm_wiki_skill](https://github.com/nashsu/llm_wiki_skill) | 2026-05-19 |
| 40 | `management-deep-dive` | 管理层纵深研究：买股票就是买人。来源：skills/management-deep-dive.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 41 | `migrate-to-shoehorn` | 把测试文件从 `as` 类型断言迁移到 @total-typescript/shoehorn。当用户提到 shoehorn、想替换测试中的 `as`，或需要部分测试数据时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 42 | `neat-freak` | 会话结束时以极致严谨做知识清理：将项目文档(CLAUDE.md、README、docs)与 agent 记忆、代码库对账，消除不一致，保持仓库整洁。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 43 | `news-pulse` | 公司新闻脉搏：股价异动时快速归因。用 4 个并行 Agent 侦察公司事件/监管政策/行业对手/市场情绪，产出"事件时间线 + 异动主因判断 + 是否触发论文重审"。 | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 44 | `obsidian-vault` | 在 Obsidian 仓库中搜索、创建与管理笔记，支持双链与索引笔记。当用户想在 Obsidian 中查找、创建或整理笔记时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 45 | `portfolio-review` | 组合管理：从\\"研究公司\\"到\\"管理组合\\"。来源：skills/portfolio-review.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 46 | `ppt-master` | AI 驱动的演示文稿工作流：生成可编辑的 PPTX 文件，创建可复用的品牌/版式/成套工作区，填充原生 PPTX 模板。 | [github.com/hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)（体积大，建议用仓库链接安装，未打包进脚本） | 2026-08-13 |
| 47 | `private-company-research` | 未上市公司研究：多Agent并行深度研究框架。来源：skills/private-company-research.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 48 | `prototype` | 构建一个一次性的原型来验证某个设计问题。当用户想快速验证状态模型或逻辑是否成立，或探索某个 UI 应该长什么样时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 49 | `quality-screen` | 去劣筛选：7条指标快速排除非一流公司。来源：skills/quality-screen.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 50 | `remotion-best-practices` | Remotion 最佳实践。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 51 | `remotion-video-production` | Remotion 视频生产：当提示或既有流程显式要求 Remotion 视频生产时使用（代码优先的视频生成方案）。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 52 | `remotion-video-toolkit` | 用 Remotion + React 做程序化视频创作的完整工具箱。涵盖动画、时序、渲染(CLI/Node.js/Lambda/Cloud Run)、字幕、3D、图表、文字特效、转场与媒体处理。在编写 Remotion 代码、搭建视频生成管线，或创建数据驱动视频模板时使用。 | [github.com/shreefentsar/remotion-video-toolkit](https://github.com/shreefentsar/remotion-video-toolkit) | N/A |
| 53 | `research` | 针对高可信一手来源调研某个问题，并把结论以 Markdown 文件存入仓库。当用户想调研某个主题、收集文档或 API 事实，或把繁琐的资料查阅交给后台 agent 时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 54 | `resolving-merge-conflicts` | 当你需要解决进行中的 git merge/rebase 冲突时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 55 | `scaffold-exercises` | 创建含章节、题目、解答与讲解的练习目录结构，且能通过 lint。当用户想搭建练习、创建练习桩，或新建一门课程章节时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 56 | `setup-matt-pocock-skills` | 为本仓库配置工程类 skills——设置 issue 跟踪器、分诊标签词表与领域文档布局。在首次使用其他工程类 skill 前运行一次。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 57 | `setup-pre-commit` | 在当前仓库用 Husky pre-commit 钩子配合 lint-staged(Prettier)、类型检查与测试。当用户想添加 pre-commit 钩子、配置 Husky、设置 lint-staged，或添加提交时格式化/类型检查/测试时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 58 | `skill-creator` | 创建新 skill、修改并改进已有 skill，并衡量 skill 表现。当用户想从零创建 skill、编辑或优化已有 skill、运行评测测试 skill、用方差分析基准测试 skill 表现，或为更好的触发准确率优化 skill 的描述时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 59 | `storage-analyzer` | macOS / Windows 只读存储分析：扫描整机磁盘占用，定位占用大户，分级给出可自动清理/需人工判断/谨慎清理方案，并生成可一键删除的交互式 HTML 报告。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 60 | `tdd` | 测试驱动开发。当用户想以测试先行的方式构建功能或修复 bug、提到『red-green-refactor』，或想要集成测试时使用。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 61 | `teach` | 在当前工作区内，教用户一项新技能或概念。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 62 | `thesis-drift` | 投资论文漂移检测：分清事实变化与措辞变化。来源：skills/thesis-drift.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 63 | `thesis-tracker` | 投资论文追踪：买入后的纪律系统。来源：skills/thesis-tracker.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 64 | `to-spec` | 把当前对话转成规格说明并发布到项目 issue 跟踪器——无需访谈，只是把你已讨论内容的综合。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 65 | `to-tickets` | 把计划、规格或当前对话拆解成一组『追踪子弹』工单，每张标注其阻塞边界，发布到已配置的跟踪器——本地以每工单一个文件、边界以文本呈现，或在真实跟踪器上以原生阻塞链接呈现。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 66 | `triage` | 通过分诊角色的状态机推进 issue 与外部 PR——分类、核验、必要时追问，并写出可供 agent 使用的简报。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 67 | `video-production` | 规划并调度代码优先 / 模板优先 / 混合的内容视频生产管线。当用户需要可程序化或自动化的视频生产时使用。 | WorkBuddy 内置/应用市场（见 install_all_skills.sh 原样打包） | 平台内置 |
| 68 | `wayfinder` | 规划一块庞大的工作(超过一个 agent 会话所能承载)，在 issue 跟踪器上以共享的决策工单地图呈现，并逐一解决，直到通往目标的路径清晰。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 69 | `wechat-article` | 微信公众号文章：作者-编辑-读者三Agent协作。来源：skills/wechat-article.md. | [github.com/xbtlin/ai-berkshire](https://github.com/xbtlin/ai-berkshire) | 2026-08-12 |
| 70 | `writing-great-skills` | 写好、改好 skill 的参考书——让 skill 可预期所需的词汇与原则。 | [github.com/mattpocock/skills](https://github.com/mattpocock/skills) | 2026-08-07 |
| 71 | `wizard` | 生成一个交互式 bash 向导(TUI)，一步步带人完成只有人能手动完成的操作——配置基础设施、设置凭证或 CI 密钥、走陌生的第三方后台、执行一次性迁移或切换。agent 自己能做的步骤不要用它。 | [github.com/mattpocock/skills/tree/main/skills/engineering/wizard](https://github.com/mattpocock/skills/tree/main/skills/engineering/wizard) | 2026-08-07 |
| 72 | `to-questionnaire` | 把你自己答不上来的决策，变成一份交给别人填写的问卷文档。 | [github.com/mattpocock/skills/tree/main/skills/productivity/to-questionnaire](https://github.com/mattpocock/skills/tree/main/skills/productivity/to-questionnaire) | 2026-08-07 |
| 73 | `wait-what` | 没看懂模型上一句在说什么？让它重述：补上你缺失的上下文，用更简单的语言讲清楚。 | [github.com/mattpocock/skills/tree/main/skills/productivity/wait-what](https://github.com/mattpocock/skills/tree/main/skills/productivity/wait-what) | 2026-08-07 |

**合计：73 个 skill 描述已全部中文化，并标注最新更新。**

> **「最新更新」列**：通过各仓库 `pushed_at` 自动获取，按来源分类展示。无公开仓库的 WorkBuddy 内置/市场 skill 标记为「平台内置」。可运行 `scripts/refresh_inventory.py` 刷新。
