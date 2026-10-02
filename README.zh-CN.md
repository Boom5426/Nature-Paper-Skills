<div align="center">

# 🧬 Nature-Paper-Skills

**把科研初稿改成论证清楚、证据扎实的期刊论文。**

面向 Codex 和 Claude Code：结构修订、文字修改、图表、引用、投稿检查与审稿回复。
聚焦 Nature 系列生命科学、计算生物学与方法学稿件。

[![Skills](https://img.shields.io/badge/skills-27-8a63d2)](docs/skill-map.md)
[![CI](https://github.com/Boom5426/Nature-Paper-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/Boom5426/Nature-Paper-Skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT%20%2B%20Apache--2.0-green)](#许可)
[![Stars](https://img.shields.io/github/stars/Boom5426/Nature-Paper-Skills?style=social)](https://github.com/Boom5426/Nature-Paper-Skills/stargazers)

[English](README.md) · **简体中文** · [快速开始](#快速开始) · [按任务选择](#按任务选择) · [完整技能目录](docs/skill-map.md)

</div>

## 修改效果示例

写作层会去掉项目日志式表达和防御性解释，同时保留理解结果所需的事实。

| 修改前 | 修改后 | 保留什么 |
|---|---|---|
| “We carefully verified that survival changed by 1 percentage point (95% CI −3 to 5), which should not be overinterpreted.” | “Survival changed by 1 percentage point (95% CI −3 to 5), with no clear evidence of improvement.” | 效应值、置信区间及不确定性 |
| “These orderings should not be read as a universal ranking across all settings.” | “These orderings hold for the tested settings.” | 比较的适用范围 |
| “The analysis reads the final output from `results/final_scores.csv`.” | “The analysis uses the measured response scores.” | 科学对象；文件获取细节放在需要它的方法或数据说明中 |

这些是示意改写，不代表真实研究结果。影响科学解释或复现的条件必须保留。更多内容见[修改前后案例](skills/core/anti-defensive-writing/references/worked-examples.md)和[完整入门示例](examples/first-run/README.md)。

## 快速开始

**需要准备：** Codex 或 Claude Code、Bash、Python 3.9+（仅使用标准库，无需额外 pip 包）。远程安装还需要 `curl` 和 `tar`。Windows 请在运行 agent 的 WSL 或 Git Bash 环境中执行；下面不是 PowerShell 命令。已验证范围见[环境与文件格式](docs/compatibility.md)。

一条命令安装推荐的 19 个 skill，包含审稿回复所需技能：

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash
```

要明确指定 agent，在 `bash` 后追加 `-s -- --agent codex` 或 `-s -- --agent claude`。
也可以先读 [install.sh](install.sh)，或[克隆后安装](docs/installation-codex.md)。更新前会备份已有技能，详见[更新与恢复](docs/installation-management.md)。

**第一次实际使用：** 将当前稿件和相关结果放进 agent 的工作目录，然后说：

```text
用 paper-workflow。依据 evidence.md 中的证据修改 draft.md 的 Results 段落。
保留测量值和图号，保存修订副本，并简要说明关键改动。
```

没有现成材料时，直接用[第一次完成修订](examples/first-run/README.md)，里面有输入、提示词和参考输出。Codex CLI/IDE 可用 `$paper-workflow` 明确调用；Claude Code 可用 `/paper-workflow`。如果找不到技能，刷新技能列表或重新打开会话，再看[排错说明](docs/installation-management.md#troubleshooting)。

之后可以直接说“优化这篇论文”，也可以点名某个技能。工作流会先判断问题和范围，再执行需要的步骤，无需记住全部技能名。

## 按任务选择

| 想完成什么 | 提供什么 | 得到什么 | 入口 |
|---|---|---|---|
| 优化整篇论文 | 当前稿件、相关结果/图表、已确定的期刊 | 修订稿、关键修改、待补证据 | `paper-workflow` |
| 修改一个段落 | 原文、上下文、修改范围 | 修改后的段落和必要说明 | `write-scientific-manuscript` |
| 去掉审计式／防御式表达 | 正文、SI、图注或数据声明 | 更直接的科学表达，保留数字与必要条件 | `anti-defensive-writing` |
| 规划或制作图表 | 科学问题、结果表或现有图 | 面板方案；有数据和工具时输出图文件 | `figure-planner`；出图另加 `--figure` |
| 投稿前检查 | 最终稿、SI、参考文献和目标期刊 | 有定位、按重要性排序的问题；注明未检查项 | `submission-audit` |
| 回复审稿意见 | 原始意见、稿件、已完成的新证据 | 保留编号的回复草稿及对应稿件修改 | `paper-workflow` |

要求“检查／给建议”时先交付诊断；要求“修改”时在授权范围内改稿。缺失的证据会指出，不会补写成已完成的实验。

## 核心特点

- **先论证，再润色。** 先检查科学问题、贡献和证据链；已稳定的文字无需反复改写。
- **图表服务于结论。** 明确每个面板的作用，保持图注与 Results 一致。可选图形技能提供字号、碰撞、对齐与源数据检查脚本。
- **面向论文读者。** 去掉正文中的审计式、防御式、自我批评式、评论式、开发者式和未来承诺式语言，保留阴性结果、必要报告与复现事实。
- **区分引用检查。** 参考文献格式、文献是否真实存在、文献是否支持当前论断是三件事。本地扫描通过不代表另外两项已验证。
- **按任务控制工作量。** 先检查相关层次，只修改有问题的部分，再复查受影响的关系。研究论文和综述分别路由，长稿不自动当作综述。

[工作流](docs/workflow-map.md) · [写作原则](docs/design-principles.md) · [图形流程与退出码](docs/figure-workflow.md) · [常用任务示例](docs/task-recipes.md)

## 安装选项

```bash
# 克隆后使用本地文件；只有指定 --ref 才重新下载
git clone https://github.com/Boom5426/Nature-Paper-Skills.git
cd Nature-Paper-Skills
bash install.sh --agent codex --local     # 当前项目 .agents/skills
bash install.sh --agent claude --local    # 当前项目 .claude/skills
bash install.sh --agent both             # 两个 agent 的用户级位置
bash install.sh --agent codex --figure   # 加装图形制作与检查
bash install.sh --agent codex --set all  # 全部 27 个 skill
bash install.sh --agent codex --dry-run  # 预览
bash install.sh --agent codex --doctor   # 检查文件、版本与依赖
```

**默认：** 19 个写作、评审与期刊技能。**图形扩展：** `nature-figure`、`figure-style`，需要 Python 绘图包或 R 绘图环境。**完整集：** 全部 27 个技能，包含文献研究、结果分析及可选的会议、演示、在线文献核验流程。核心写作和数据绘图不需要 OpenRouter 密钥；只有可选 AI 示意草图路线需要。图像使用须符合目标期刊要求。

分 agent 安装说明：[Codex](docs/installation-codex.md) · [Claude Code](docs/installation-claude.md)。版本变化见 [CHANGELOG](CHANGELOG.md)。通过 `--ref <完整提交SHA>` 固定版本；安装器会记录来源和文件哈希。

## 适用范围与边界

面向生命科学、计算生物学、方法、基准和资源类期刊论文。用户明确的期刊要求及项目决定优先于默认 Nature 风格。本项目独立于 Nature Portfolio，不预测录用结果。

技能提供操作规则与部分辅助脚本，不自带 Word 编辑器、PDF 渲染器、LaTeX 环境、联网访问权限或实验数据。[兼容说明](docs/compatibility.md)分别列出可读取、可编辑与可导出的范围。

仓库测试覆盖脚本、安装与文件一致性。[行为案例](evals/README.md)用于检查修改范围、证据保留及缺少能力时的诚实报告；实际运行记录与适用边界单独列出。

## 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。影响用户行为的修改应附任务案例或示例，中英文首页同步维护。组件来源见 [ATTRIBUTION.md](ATTRIBUTION.md)。

## 致谢

部分内容受到 [OpenLAIR/dr-claw](https://github.com/OpenLAIR/dr-claw)、[Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) 和 Claude Science skill pack 的启发。

图形层还参考了 [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) 的设计经验。本仓库不分发该项目的代码或文字；详见 [THIRD_PARTY_NOTICES](skills/figure/nature-figure/THIRD_PARTY_NOTICES.md)。

## 许可

原创内容使用 [MIT](LICENSE)。含 Apache-2.0 材料的组件保留 [LICENSE-APACHE](LICENSE-APACHE) 与 [NOTICE](NOTICE)，安装器分发时也会携带。覆盖范围见 [ATTRIBUTION](ATTRIBUTION.md)。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Boom5426/Nature-Paper-Skills&type=Date)](https://star-history.com/#Boom5426/Nature-Paper-Skills&Date)
