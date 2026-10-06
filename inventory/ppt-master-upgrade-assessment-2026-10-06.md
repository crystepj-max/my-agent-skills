# ppt-master 升级评估报告（v4.5.0 → v6.6.0）

> 评估时间：2026-10-06
> 评估方式：上游 v1.3.1 tag 浅克隆 + git 历史追溯 + 本地全量 mtime 扫描（只读，未改动任何文件）
> 结论：**本地无自定义内容，51 个"独有文件"是上游淘汰的旧版残留，可安全整体升级**

## 一、事实链

| 维度 | 数据 |
|---|---|
| 本地版本 | **v4.5.0**（`SKILL.md` metadata.version） |
| 上游版本 | **v6.6.0**（skill 自身版本；仓库 tag 为 v1.3.1） |
| 本地文件总数 | 12232 |
| 上游文件总数 | 13016 |
| 内容不同 | 639 个文件 |
| 上游新增 | 490 个文件 |
| 本地独有 | 51 个文件 |
| 本地文件 mtime 范围 | 2026-08-13 ～ 2026-08-16（**集中在安装日，无近期生成文件**） |

## 二、关键判定：51 个本地独有文件不是定制，是旧版残留

松哥提出「是否只是 PPT 制作过程中的缓存或临时文件」——**假设被证据否证**：

### 证据 1：时间戳排除缓存/临时文件
本地 12232 个文件 mtime 全部落在 2026-08-13～08-16（安装日）。缓存与临时文件会在每次制作 PPT 时持续产生**新时间戳文件**，此处不存在任何近期文件。

### 证据 2：上游主动废弃记录（git 历史实证）
本地独有的 5 个 Python 脚本 + 2 个工作流文档，在上游对应提交：

```
7f000fb8  2026-08-27  feat(roundtrip): round-trip authoring tools and
                      retirement of legacy fill/enhance CLIs
```

提交标题直白写明「**retirement of legacy fill/enhance CLIs**」（旧填充/增强命令行的退役）。受影响文件：
- `scripts/native_enhance_pptx.py`
- `scripts/native_enhance_pptx_core.py`
- `scripts/native_narration_pptx.py`
- `scripts/template_fill_pptx.py` + `scripts/template_fill_pptx/`
- `workflows/native-enhance-pptx.md`
- `workflows/template-fill-pptx.md`

### 证据 3：45 张图表 SVG 属旧版图表集
本地 `templates/charts/` 下 45 个 SVG（timeline.svg、kpi_cards.svg、pyramid_chart.svg 等）+ CHART_STYLE_GUIDE.md，上游当前该目录已换为新图表集（area_chart.svg、bar_of_pie_chart.svg、box_plot_chart.svg 等）。属旧版模板残留，非本机生成。

## 三、风险评估

| 风险 | 等级 | 说明 |
|---|---|---|
| 丢失自定义内容 | 🟢 无 | 已用 git 历史 + mtime 双重验证无本机改动痕迹 |
| 覆盖不可逆 | 🟡 中 | 全量替换 12232 个文件，需先完整备份 |
| 上游 v6.6.0 自身稳定性 | 🟡 中 | 跨 2 个大版本（v4.5 → v6.6），上游自身标注为 v1.3.1 首个正式 tag，CHANGELOG 需确认是否有破坏性变更 |
| 影响现有 PPT 工作流 | 🟡 待查 | 松哥 24 页微众红蓝主题 PPT 依赖 `template_fill_pptx` / `native_enhance_pptx`——**这两个脚本上游已废弃**，升级后原工作流入口可能改变，需确认替代路径 |

## 四、旧入口 → 新入口映射（已查明）

上游以「round-trip authoring」体系取代废弃的两个 CLI，**能力等价且更强**（原版只能改，改动后重新导出；新版未改动的页面可字节级还原）：

| 旧入口（v4.5.0，本地） | 新入口（v6.6.0，上游） | 变化 |
|---|---|---|
| `scripts/template_fill_pptx.py`<br>`workflows/template-fill-pptx.md` | `workflows/edit-native-pptx.md`<br>（`pptx_to_svg.py --roundtrip` 导入 → 改 → `svg_to_pptx.py --roundtrip` 导出） | 从"填充"变为"往返编辑"：未动页面字节级还原，不破坏原 PPT 设计 |
| `scripts/native_enhance_pptx.py`<br>`scripts/native_enhance_pptx_core.py` | `scripts/authoring_roundtrip.py`<br>（被 `svg_to_pptx.py --roundtrip` 内部调用） | 从独立 CLI 变为底层模块；对外入口是 `edit-native-pptx` 工作流 |
| `scripts/native_narration_pptx.py` | `workflows/edit-native-pptx.md` 的 notes/narration/motion 叠加层 | 旁列为叠加层，不重写可见内容 |
| `templates/charts/` 45 张旧版 SVG | 上游新图表集（area_chart / bar_of_pie / box_plot 等） | 旧图表集整体废弃 |
| `templates/charts/CHART_STYLE_GUIDE.md` | 上游 `scripts/chart_recall.py` + 新图表自带样式 | 由静态指南改为可调用召回 |

**结论：能力无缺口**。松哥现有 24 页微众红蓝主题 PPT 工作流依赖的"模板填充 + 原生增强"，在新版由 `edit-native-pptx` 路由完整承接，且新增"未改页面字节级还原"能力（对品牌模板是净收益）。

⚠️ 唯一需注意：调用入口名变了（`template_fill_pptx.py` → `edit-native-pptx.md` 工作流）。若有固化脚本调用旧入口，需同步改调用路径。

## 五、推荐执行顺序（待松哥确认后执行）

1. 完整备份本地 ppt-master（12232 文件）到 `/tmp/ppt-master-backup-4.5.0/`
2. 出具旧入口 → 新入口映射表，确认工作流连续性
3. rsync 覆盖升级到 v6.6.0
4. 跑 cn_guard.sh 确认 description 仍为中文
5. 验证 24 页 PPT 工作流可正常执行

## 六、当前状态

- 本次评估**全程只读**，未改动 ppt-master 任何文件
- 未创建第二份副本，未在库目录执行删除
- 等待松哥决策：直接升级（先备份） / 只清残留 / 先看差异报告
