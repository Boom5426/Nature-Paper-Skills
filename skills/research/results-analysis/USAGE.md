# Results Analysis 使用指南

直接调用 `results-analysis` skill 分析数据。它属于研究扩展，安装时选择
`--set all`（从仓库根目录运行 `bash install.sh --set all`）。

## 快速开始

在 Codex CLI/IDE 中明确调用 `$results-analysis`，在 Claude Code 中调用
`/results-analysis`，并说明数据路径、实验单位和输出路径。例如：

```text
Use results-analysis. Compare the models in experiments/results.csv.
Report mean, sample SD, n, and the planned comparisons. Preserve all runs,
seed labels and metrics. Save the report to analysis-report-v2.md and the
Results draft to results-draft-v2.md; do not overwrite existing files.
```

按需要说明任务是完整分析、模型对比、消融分析或可视化。Agent 使用数据加载、
统计验证、可视化和写作流程；检验方法由独立/配对设计、分析单位和推断目标决定。

## 可复算的三模型示例

本页是**合成教学示例**，不代表真实模型实验。完整的 15 条运行记录见
[usage-runs.csv](examples/usage-runs.csv)：三个模型各 5 次运行，保留种子标识
42、123、456、789、1024。每行包含 model、seed、accuracy、f1_score 和
training_time；准确率/F1 的单位为百分比，训练时间为小时。

数据由各指标的既有均值和 SD 按
`mean + SD × [-2, -1, 0, 1, 2] / sqrt(2.5)` 构造并重排，保存到小数点后六位。
种子是示例中的运行标识，没有执行模型训练或随机采样。本次用完整合成输入替换了
原先与输出 SD 不一致的 CSV 片段，保留原报告中的均值和 SD。

从仓库根目录复算：

```bash
python3 skills/research/results-analysis/scripts/example_statistics.py --example usage
```

helper 需要 SciPy（`python3 -m pip install scipy`），只向标准输出打印 JSON。
它从 CSV 的未舍入数值计算样本 SD（ddof=1）、t、双侧 P 和 pooled Cohen's d，
并给出三项比较的 Bonferroni 校正 P。公式与
[SciPy 的汇总统计 t 检验定义](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind_from_stats.html)
一致。

教学设计预设每个模型有 5 次独立运行、近似正态误差和相等总体方差，
采用等方差双侧双样本 t 检验。相同 seed 标签不用于模型间配对；真实实验中若
运行按共同数据划分或实验单位匹配，应按实际设计分析。小样本的正态性或方差检验
`p > 0.05` 不能证明假设成立，本例不虚构这些预检验结果。

### analysis-report.md

```markdown
# 合成实验结果分析报告

## 描述性统计

数值为 5 次运行的均值 ± 样本 SD：
- Baseline LSTM: 86.2% ± 0.21%
- BERT-base: 91.3% ± 0.18%
- Our Method: 93.5% ± 0.23%

## 预先指定的三项准确率比较

| 对比 | t-statistic | 未校正 p-value | Cohen's d | Bonferroni p-value |
|------|-------------|----------------|-----------|--------------------|
| Our Method vs Baseline LSTM | t(8) = 52.41 | p = 1.95e-11 | d = 33.15 | p = 5.84e-11 |
| Our Method vs BERT-base | t(8) = 16.84 | p = 1.56e-7 | d = 10.65 | p = 4.69e-7 |
| BERT-base vs Baseline LSTM | t(8) = 41.23 | p = 1.32e-10 | d = 26.08 | p = 3.96e-10 |

等方差双侧双样本 t 检验，每组 n = 5，df = 8。检验族包含上表三项比较，
家族 α = 0.05，未校正 P 的判定阈值为 α' = 0.05/3 ≈ 0.0167。
三项比较均通过 Bonferroni 校正。检验使用未舍入的 CSV 数值。
```

这些很大的 d 来自示例中很小的运行间 SD；效应量的实际意义还需要结合任务和设计判断。

### results-draft.md

```markdown
## Results

### Performance Comparison

Our method achieved 93.5% ± 0.23% accuracy, compared with 86.2% ± 0.21%
for Baseline LSTM and 91.3% ± 0.18% for BERT-base.

**Table 1**: Synthetic model performance. Values are mean ± sample SD across
five runs per model; accuracy and F1 are percentages, and training time is hours.

| Model | Accuracy (%) | F1 Score (%) | Training Time (h) |
|-------|--------------|--------------|-------------------|
| Baseline LSTM | 86.2 ± 0.21 | 85.8 ± 0.19 | 2.5 ± 0.08 |
| BERT-base | 91.3 ± 0.18 | 90.7 ± 0.16 | 8.5 ± 0.12 |
| **Our Method** | **93.5 ± 0.23** | **92.8 ± 0.21** | **5.2 ± 0.10** |

Using five independent runs per model (n = 5 per group), our method exceeded
Baseline LSTM by 7.3 percentage points (equal-variance two-sided two-sample
t-test, t(8) = 52.41, P = 1.95e-11, Cohen's d = 33.15) and BERT-base by
2.2 percentage points (t(8) = 16.84, P = 1.56e-07, Cohen's d = 10.65).
Both differences remained significant after Bonferroni correction over the
three predefined pairwise comparisons (family α = 0.05).
```

### visualization-specs.md

```markdown
# 可视化规格

## Figure 1: 性能对比
- X 轴：模型名称
- Y 轴：准确率（%）
- 展示所有运行的点，并明确标注均值和样本 SD
- 输出：PDF 和 PNG
- 配色：Okabe-Ito；标签和字体按最终展示尺寸检查

Caption: "Synthetic model performance across five runs per model.
Error bars show sample SD. Accuracy differences against both baselines
remain significant after Bonferroni correction over three predefined comparisons."
```

## 四数据集示例

[分析报告](examples/example-analysis-report.md)和
[Results 草稿](examples/example-results-section.md)使用另一组较大 SD 的合成数据：
[benchmark-runs.csv](examples/benchmark-runs.csv)。两组示例均保留各自既有的均值和 SD，
不共用 t、d 或 P。构造方法与上文相同。benchmark 四列分别采用基准秩序列
`[0,1,2,3,4]`、`[0,2,1,4,3]`、`[1,0,2,4,3]`、`[0,1,3,2,4]`
索引标准化的 `[-2,-1,0,1,2]`；三个模型再按
`[0,1,2,3,4]`、`[2,0,4,1,3]`、`[3,1,4,0,2]` 重排完整运行。
这些构造用于复算演示，不是从真实观测反推或估计跨数据集协方差。

benchmark CSV 每行是一个模型运行，含四个数据集的准确率。先在同一行内取四个
数据集的均值，再对每个模型的 5 个运行均值计算 SD 和模型间检验。这样保留了
运行内的跨数据集协方差；各数据集 SD 的算术平均不能替代平均准确率的 SD。

```bash
python3 skills/research/results-analysis/scripts/example_statistics.py --example benchmark
```

## 其他任务

### 消融分析

```text
Use results-analysis. Analyze experiments/ablation/.
Report each component's accuracy change in percentage points and its uncertainty.
Preserve the full-model reference and save a new report to ablation-report-v2.md.
```

例如，93.5% 降到 90.8% 是下降 2.7 个百分点；相对下降百分比需要另行计算。

### 可视化

```text
Use results-analysis. Make visualization specifications from experiments/results.csv.
Specify the observations, units and error bars. Save to visualization-specs-v2.md.
```

### 数据或设计不完整

缺少运行记录、样本量、配对关系或独立单位时，明确哪些统计量不能复算。
只有汇总数据时，不报告需要原始观测的 Shapiro-Wilk 或 Levene 结果。
重复次数由所需精度、变异性和功效确定；5 次运行本身不保证结论可靠。
检验选择基于设计、目标和诊断，不因一个正态性检验 P 值自动切换方法。

## 方法与检查

- [统计方法](references/statistical-methods.md)：设计、检验、效应量和校正。
- [结果写作](references/results-writing-guide.md)：报告模板和数值含义。
- [常见问题](references/common-pitfalls.md)：SD/SE、统计推断和重复设计。
- 每个数值都应能回到原始记录或明确的汇总输入。
- 表格、正文、图注使用同一分析单位、同一比较和同一校正范围。
- 由未舍入数值计算，最后只对报告值舍入；缺失的方差或协方差不凭空补齐。
