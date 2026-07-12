# `nature-figure` 技能

`nature-figure` 用于生成可投稿级科研图，面向 Nature 级期刊和高影响力学术场景，同时支持 Python 与 R 两条绘图路径。若用户明确需要 AI 生成论文示意图、机制图或 graphical abstract，也支持通过 OpenRouter Images API 调用 `openai/gpt-image-2` 生成概念示意图草稿。

该技能从“图件契约”开始，而不是直接套模板。开始绘图前，必须明确核心结论、证据层级、图件原型、后端选择、期刊与导出约束、统计说明和 source-data 可追溯性。第一次使用绘图路径时，用户选择 Python 或 R 后会写入默认偏好；后续默认沿用该后端，除非用户明确切换。只有在科学逻辑明确后，才使用绘图模板。

Python 路径主要使用 `matplotlib`、`seaborn`、`subplot_mosaic` 和 `statsmodels`，适合精细低层布局控制。R 路径使用 `ggplot2`、`patchwork`、`ComplexHeatmap`、`ggrepel`、`svglite`、`cairo_pdf` 和 `ragg`。如果使用私有模板集合，不得在面向用户的输出中暴露私有路径、文件名或来源信息。

该技能参考了 [figures4papers](https://github.com/ChenLiu-1996/figures4papers) 中来自 *Nature Machine Intelligence* 和顶级机器学习/生物信息学论文的生产脚本。原始 demo 脚本和预览图未随本精简仓库分发，可在上游查看：[nature-skills/skills/nature-figure/assets](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-figure/assets)。

---

## OpenRouter AI 示意图生成

当用户明确要求“用 OpenRouter / GPT Image 2 生成论文示意图、机制示意图、graphical abstract”时，走独立 AI-schematic route，不需要先询问 Python 或 R。

```bash
export OPENROUTER_API_KEY="sk-or-..."
python scripts/generate_openrouter_schematic.py \
  --title "Paper title" \
  --abstract-file abstract.txt \
  --panel-map "left: problem; center: proposed mechanism; right: validated outcome" \
  --outdir outputs/schematic \
  --basename graphical_abstract
```

这个功能生成的是概念视觉草稿，不应作为定量数据面板。正式投稿前，建议检查科学元素是否被幻觉扩写，并把关键文字、箭头和标注重画成可编辑矢量对象。

---

## 示例图库

下面列出的是按本技能规则生成的模拟数据 mockup：优先导出可编辑 SVG、使用克制的语义配色、小写 panel label，并采用非对称多面板信息结构。预览 PNG 未随本精简仓库分发，可在[上游图库](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-figure/assets)查看。

| 图件 | 展示能力 |
|--------|-----------------------------|
| 材料设计与物理验证 | 机制示意主导的复合图、SEM-like 图像面板、流变、释放动力学、滞留图、相关性与终点定量 |
| 空间滞留与摄取 | 深色显微图版、通道行、局部放大、深度剖面、摄取直方图、3D 穿透热图和图像衍生相关性 |
| 体内疗效与耐受性 | 实验时间线、肿瘤纵向曲线、个体生长轨迹、waterfall response、forest plot、组织学、免疫组成和毒性面板 |
| 单细胞系统图 | UMAP-style embedding、组成、marker heatmap、pseudotime、volcano plot、enrichment、ligand-receptor bubble matrix 和空间邻域关系 |
| 扰动验证 | 机制扰动时间线、复发终点、polar summary、剂量反应、synergy matrix、生物分布、细胞因子、flow-like scatter 和安全评分 |

**图库文件策略**：真实用户应从源数据和脚本重新生成可编辑输出，而不是复用预览。上游只保留轻量 PNG 预览，且不提交大型生成 SVG/PDF。

---

## 图表类型图谱

下面的图谱按 chart family 分类。每个条目在上游对应一张紧凑的 4 x 4 小面板 atlas，用来展示可组合进 Nature 风格结果图的视觉语法范围。预览 PNG 未随本精简仓库分发，可在[上游 chart atlas](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-figure/assets)查看。

| 类型 | 常见用途 |
|------|------------|
| 柱状图 | 组间比较、有符号差值、组内分组设计、堆叠组成 |
| 折线与纵向趋势 | 时间过程、不确定性带、干预标记、个体轨迹 |
| 热图 | Z-score 矩阵、连续丰度图、带注释表格、聚类块 |
| 散点与气泡图 | 相关性、簇、volcano-style 检验、象限总结、第三变量编码 |
| 雷达与极坐标图 | 多轴 benchmarking、圆形摘要、polar histogram、方向密度 |
| 分布图 | 直方图、小提琴图、箱线图、ridgeline 和样本级分布 |
| Forest 与区间图 | 效应量、置信区间、点范围、配对斜率比较 |
| 面积与堆叠趋势 | 填充轨迹、份额堆叠、累计曲线、stream-like 构图 |
| 图像板 | 显微通道、叠加图、裁剪、比例尺和暗色面板 |
| 网络与矩阵图 | 气泡矩阵、邻接图、node-link 图和二分互作面板 |

---

## 文件结构

该技能采用 router/static-dynamic 结构：短 `SKILL.md` 路由配合 `manifest.yaml`，加载常驻 core、用户选择的后端片段，以及按需 references。

```text
nature-figure/
├── SKILL.md                     # 短路由：后端 gate，加载 fragments
├── manifest.yaml                # always_load core + backend axis + 按需 references
├── README.md                    # 本文件
├── scripts/
│   ├── generate_openrouter_schematic.py
│   └── nature_figure_backend.py
├── static/
│   ├── core/                    # 始终加载
│   │   ├── contract.md          # 图件契约、后端 gate、互斥规则、运行时缺失处理
│   │   └── stance.md            # 配色策略、默认立场、隐私、何时加载
│   └── fragments/
│       └── backend/             # 在 Python-or-R gate 解决后加载
│           ├── python.md        # Python-only 规则与 matplotlib quick-start
│           └── r.md             # R-only 规则与 ggplot2 quick-start
# 注意：demo assets（gallery/、chart-atlas/、figures4papers/）未随本精简仓库分发，
# 见上游 https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-figure/assets
└── references/                  # 按需打开
    ├── figure-contract.md       # 核心结论、证据层级、panel map
    ├── backend-selection.md     # Python vs R 选择规则
    ├── r-workflow.md            # R scaffold、patchwork、ComplexHeatmap、导出
    ├── r-template-index.md      # 本地 R template atlas
    ├── qa-contract.md           # 投稿/返修 QA 清单
    ├── api.md                   # PALETTE 常量、helper 函数签名
    ├── design-theory.md         # 字体、色彩理论、布局、导出策略
    ├── common-patterns.md       # 可复用代码模式
    ├── openrouter-image-generation.md
    ├── tutorials.md             # 端到端教程
    ├── chart-types.md           # radar、3D sphere、scatter、fill_between、log-scale
    └── demos.md                 # figures4papers demo map 与路由指南
```

---

## 后端与图件契约规则

绘图任务优先使用用户已经指定的后端；如果没有指定，则读取 `scripts/nature_figure_backend.py` 保存的默认偏好。第一次使用且尚未保存偏好时，再询问用户选择 **Python 或 R**，并把答案保存为后续默认后端。如果用户需要推荐，参考 `references/backend-selection.md`。

后端一旦选定，绘图、预览、导出和视觉 QA 都必须只使用该后端。如果所选运行时或包缺失，应停止并报告 blocker；不要用另一种语言临时替代。该规则双向适用：不能用 Python 替代 R，也不能用 R 替代 Python。

绘图前必须写明或推断核心结论、图件原型、panel map、证据层级、目标输出、统计/source-data 需求和导出包。图件首先服务科学逻辑，美观和模板匹配是次级目标。

面向用户的输出不得暴露私有本地路径、私有文件名、内部参考文档、模板编号或私有材料来源，除非用户明确要求审计轨迹。

---

## Python 强制规则

### 1. 三个必需 rcParams：保留 SVG 可编辑文本

```python
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
```

`svg.fonttype = 'none'` 可以避免 matplotlib 默认把每个字形转为 bezier 曲线。这样导出的 SVG 中，文字仍是 `<text>` 节点，可选择、可搜索，也方便在 Illustrator 或 Inkscape 中重新对齐。

字体栈中包含 `Arial`、`DejaVu Sans` 和 `Liberation Sans`：`Arial` 是 macOS/Windows 常见字体，`DejaVu Sans` 随 matplotlib 提供，`Liberation Sans` 在 RHEL/Ubuntu 上与 Arial 度量兼容。这个级联能提高跨平台字距一致性。

### 2. 主输出格式是 SVG

```python
fig.savefig('figure.svg', bbox_inches='tight')           # 主输出：可编辑文本
fig.savefig('figure.png', dpi=300, bbox_inches='tight')  # 可选栅格预览
```

当图要进入论文或需要后期文字微调的 slide deck 时，不要只导出 PNG。

### 3. 始终关闭 figure

```python
plt.close(fig)
```

---

## 快速模板

```python
import matplotlib
matplotlib.use('Agg')                    # headless / server rendering
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# 必需设置
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'

# 基础样式
plt.rcParams.update({
    'font.size': 12,
    'axes.spines.right': False,
    'axes.spines.top': False,
    'axes.linewidth': 2.0,
    'legend.frameon': False,
    'xtick.major.width': 1.5,
    'ytick.major.width': 1.5,
})

# 图件
fig, ax = plt.subplots(figsize=(8, 5))
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)

# ... 在这里写绘图代码 ...

fig.tight_layout(pad=2)
fig.savefig('output.svg', bbox_inches='tight')
fig.savefig('output.png', dpi=300, bbox_inches='tight')
plt.close(fig)
```

---

## 配色方案

```python
PALETTE = {
    # 主方法 / 核心系列
    'blue_main':      '#0F4D92',
    'blue_secondary': '#3775BA',

    # 正向 / 提升色阶
    'green_1': '#DDF3DE',
    'green_2': '#AADCA9',
    'green_3': '#8BCF8B',

    # 基线 / 对照
    'red_1':      '#F6CFCB',
    'red_2':      '#E9A6A1',
    'red_strong': '#B64342',

    # 中性辅助
    'neutral_light': '#CFCECE',
    'neutral_mid':   '#767676',
    'neutral_dark':  '#4D4D4D',
    'neutral_black': '#272727',

    # 强调色，谨慎使用
    'gold':    '#FFD700',
    'teal':    '#42949E',
    'violet':  '#9A4D8E',
    'magenta': '#EA84DD',
}
```

语义映射约定：`blue_main` 表示本文方法或核心系列，`green_3` 表示正向变体，`red_strong` 表示基线，`neutral_light` 表示参考或背景。所有 panel 中必须保持一致。

推荐在近期 Nature Machine Intelligence 风格的密集多面板图中使用统一低饱和配色：一个 coherent baseline family 加一个 coherent hero family，绿色/红色只用于差值标记或真正有方向性的语义。

```python
PALETTE_NMI_PASTEL = {
    # 基线 / 对照家族
    'baseline_dark': '#484878',
    'baseline_mid':  '#7884B4',
    'baseline_soft': '#B4C0E4',

    # 本文方法家族
    'ours_tiny':  '#E4E4F0',
    'ours_base':  '#E4CCD8',
    'ours_large': '#F0C0CC',

    # 概览 / 概念面板背景块
    'bg_lilac': '#E0E0F0',
    'bg_aqua':  '#E0F0F0',
    'bg_peach': '#F0E0D0',

    # 中性辅助
    'neutral_light': '#D8D8D8',
    'neutral_mid':   '#A8A8A8',
    'neutral_dark':  '#606060',

    # 仅用于方向性标注
    'delta_up':   '#2E9E44',
    'delta_down': '#E53935',
}

DEFAULT_COLORS_NMI_PASTEL = [
    PALETTE_NMI_PASTEL['baseline_dark'],
    PALETTE_NMI_PASTEL['baseline_mid'],
    PALETTE_NMI_PASTEL['baseline_soft'],
    PALETTE_NMI_PASTEL['ours_tiny'],
    PALETTE_NMI_PASTEL['ours_base'],
    PALETTE_NMI_PASTEL['ours_large'],
]
```

适用场景：

- 比较 `Tiny / Base / Large` 等相关模型家族。
- 构建 1 页 result atlas，需要多个 panel 视觉统一。
- 追求低饱和编辑风格，而不是最大化类别区分。

实践规则：同一方法家族在所有 panel 中保持同一 hue family。不要因为某个 panel 需要对比，就把 panel `a` 中的蓝灰模型在 panel `d` 里改成绿色。

---

## 支持的图表类型

| 图表 | 文件 | 关键模式 |
|-------|------|-------------|
| 分组柱状图 | `tutorials.md` | `ax.bar()` 配合 `x + offset`，最后一个 panel 只放 legend |
| 堆叠柱状图 | `common-patterns.md` | 遍历 `col_order`，累计 `bottom` |
| 横向 ablation bar | `tutorials.md` | `ax.barh()`，用 alpha-gradient 编码完整性 |
| 趋势 / 折线 | `tutorials.md` + `api.md` | `make_trend()`，用 `fill_between` 表示不确定性 |
| 连续热图 | `api.md` | `make_heatmap()`、`YlOrRd`、按亮度决定 cell annotation 颜色 |
| 发散 / z-score 热图 | `design-theory.md §11` | `RdBu_r`，`vmin=-2.5, vmax=2.5` |
| 气泡散点图 | `design-theory.md §11` | x/y 表示两个维度，`s=` 表示第三变量 |
| 雷达 / 极坐标图 | `chart-types.md` | `projection='polar'`，自定义 spokes，逐轴归一化 |
| 3D sphere / illustration | `chart-types.md` | 用 numpy 网格 ray-cast 实现 Lambertian shading |
| Fill-between / 堆叠面积 | `chart-types.md` | 使用 hatch 保证灰度打印安全 |
| Log-scale bar | `chart-types.md` | `set_yscale('log')`，顶部留出标注空间 |
| 多面板 GridSpec | `chart-types.md` | `GridSpec(rows, cols)`，用 `gs[0, :]` 做全宽 panel |

---

## 多面板信息结构

多面板图中的每个 panel 都必须回答一个**唯一**科学问题。遮住任意一个 panel 后，其他 panel 不应能完全替代它。

### 推荐的三层递进复杂度

| 层级 | 问题 | 编码方式 |
|-------|----------|----------|
| Overview | “整体格局是什么？” | 堆叠柱、组成图 |
| Deviation | “每组的独特性是什么？” | Z-score 热图、发散色图 |
| Relationship | “变量之间如何共变？” | 气泡散点、相关性图 |

### 常见冗余陷阱

| 陷阱 | 示例 | 修正 |
|------|---------|-----|
| 绝对值 + 绝对值 | 堆叠柱百分比 + 同一百分比热图 | 把热图换成 z-score deviation |
| 父集的子集 | tumor-only ranked bar 只是堆叠柱的一列 | 换成 tumor % vs immune % 散点 |
| 两个排序 | 两个相关指标的 ranked bar | 将其中一个换成气泡散点 |
| 图形不同但数据相同 | 饼图 + 堆叠柱 | 合并或换成关系图 |

### Z-score deviation 热图

```python
z = (heat - heat.mean(axis=0)) / heat.std(axis=0)
im = ax.imshow(z.values, cmap='RdBu_r', aspect='auto', vmin=-2.5, vmax=2.5)
cbar.set_label('Z-score vs pan-cohort mean')
```

`RdBu_r` 中红色表示高于平均富集，蓝色表示低于平均。它与 panel a 中展示的绝对百分比形成正交信息。

### 带象限标签的气泡散点

```python
ax.scatter(x, y, s=size_var * scale, c=colors, edgecolors='white', linewidth=0.8, alpha=0.9)
ax.axvline(np.median(x), lw=1.2, ls='--', color='#767676', alpha=0.6)
ax.axhline(np.median(y), lw=1.2, ls='--', color='#767676', alpha=0.6)
```

象限标签放在角落，使用小号灰色斜体文字，例如 `fontsize=7.5, color='#888888', style='italic'`。

---

## 布局规则

### Figure 尺寸

| 类型 | `figsize` |
|------|-----------|
| 多指标柱状图（3-4 个指标 + legend panel） | `(28-45, 6-12)` |
| 大型多面板图（3 panels，2-row GridSpec） | `(22, 17)` |
| 紧凑单柱状图 | `(9-16, 5-8)` |
| 趋势 / 折线多面板 | `(14, 4)` 或 `(9, 8)` |
| 单热图 | `(8-20, 5-9)` |
| 雷达极坐标 | `(12, 10)` |

规则：比较型柱状面板的宽度通常约为高度的 3-4 倍。

### Panel labels

```python
ax.text(-0.05, 1.06, 'a', transform=ax.transAxes,
        fontsize=22, fontweight='bold', va='top', ha='right')
```

每个 subplot 左上角使用小写粗体 `a`、`b`、`c`，通过 `transAxes` 放置。

### Legend

- 多轴图件中，legend 应有独立 axis，例如 `ax.set_axis_off()`。
- 始终使用 `frameon=False`。
- 如果 legend 较大，放在 panel 下方：`bbox_to_anchor=(0.5, -0.24), loc='upper center'`。

---

## 字号层级

| 场景 | `font.size` |
|---------|-------------|
| 基础紧凑子图 | 12-16 |
| 大型柱状 panel（figsize > 28 in） | 24 |
| 大 panel 坐标轴标题 | 32-54，可逐标签覆盖 |
| 柱内 / cell 内注释 | 6.5-12 |
| Panel letter label | 20-22 |
| Legend | 8-14 |

---

## 坐标轴与边框规则

```python
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['legend.frameon'] = False

ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
```

默认不使用 gridline。用稀疏 `set_yticks` 引导阅读。Y 轴范围要贴近数据，不要在所有值都落在 `80-95` 时使用 `0-100`。

---

## Cell / bar 内文字对比度

```python
def luminance_text_color(hex_color):
    c = hex_color.lstrip('#')
    r, g, b = int(c[0:2],16)/255, int(c[2:4],16)/255, int(c[4:6],16)/255
    return 'white' if 0.299*r + 0.587*g + 0.114*b < 0.5 else '#333333'
```

---

## 复现检查清单

- [ ] 核心结论和 panel map 在美化前已经明确。
- [ ] 后端已明确为 Python 或 R。
- [ ] **前 3 个设置**包含 `font.family`、`font.sans-serif` 三字体栈、`svg.fonttype = 'none'`。
- [ ] 主输出为 **SVG**，并使用 `bbox_inches='tight'`。
- [ ] 右侧和顶部 spines 关闭，`legend.frameon = False`。
- [ ] 字号符合最终用途：密集期刊图通常 5-7 pt，只有 slide-sized panel 才使用更大字号。
- [ ] 颜色来自同一个 coherent palette system：语义 `PALETTE` 或统一 `PALETTE_NMI_PASTEL`。
- [ ] 相关模型大小或变体共享同一 hue family，不给同胞系列分配不相关的高饱和颜色。
- [ ] 绿色 / 红色只用于提升、下降、阈值或真正有方向性的语义。
- [ ] Y 轴范围贴近数据范围。
- [ ] 多面板图中每个 panel 回答**不同**问题，已通过反冗余检查。
- [ ] Panel labels 使用粗体小写 `a`、`b`、`c`，字号适合最终输出。
- [ ] 面向手稿时，已记录统计、`n`、source data 和图像完整性说明。
- [ ] 保存前调用 `tight_layout(pad=2)`。
- [ ] 保存后调用 `plt.close(fig)`。
