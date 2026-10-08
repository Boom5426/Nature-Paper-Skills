<div align="center">

# 🧬 Nature-Paper-Skills

**从科研初稿到投稿与返修，把研究成果写成论证清楚、证据扎实的期刊论文。**

27 个 skill，将结构修订、科学写作、论文图表、引用核验与审稿回复串成一套工作流。
面向 Codex 和 Claude Code，聚焦 Nature 系列生命科学、计算生物学与方法学稿件。

🧠 **论文结构** · 📊 **科研图表** · ✍️ **科学写作** · 📚 **引用核验** · 📨 **审稿回复**

[![Skills](https://img.shields.io/badge/skills-27-8a63d2)](docs/skill-map.md)
[![CI](https://github.com/Boom5426/Nature-Paper-Skills/actions/workflows/ci.yml/badge.svg)](https://github.com/Boom5426/Nature-Paper-Skills/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT%20%2B%20Apache--2.0-green)](#许可)
[![Stars](https://img.shields.io/github/stars/Boom5426/Nature-Paper-Skills?style=social)](https://github.com/Boom5426/Nature-Paper-Skills/stargazers)

🌐 [English](README.md) · **简体中文**

[🗺️ 工作流总览](#工作流总览) · [🚀 快速开始](#快速开始) · [🧩 按任务选择](#按任务选择) · [📚 完整技能目录](docs/skill-map.md)

</div>

---

<a name="核心特点"></a>

## ✨ 核心特点

- 🎯 **先稳住论证，再打磨句子。** 把科学问题、贡献和证据链接起来，再处理段落与语言。
- 📊 **让每张图都有明确任务。** 一图一主张，组织面板，保持图注与 Results 一致；可选图形技能提供字号、碰撞、对齐与源数据检查。
- ✍️ **写给论文读者看。** 把项目日志式表达和防御性解释改成直接的科学叙述，保留测量值、必要条件与阴性结果。
- 📚 **核查引用到底支持什么。** 分别检查参考文献格式、文献是否存在，以及原文是否支持当前论断。
- 📨 **让审稿回复与改稿对应。** 保留审稿人的编号，逐条回应，把回复落到已完成的证据和稿件修改上。
- 🧩 **整篇、章节、段落都能进入。** 工作流按任务选择相关层次，处理有问题的部分，保留已经稳定的内容。

<a name="工作流总览"></a>

## 🗺️ 工作流总览

**从科学问题到审稿回复，把论文各层接成一套工作流。**

```mermaid
flowchart LR
    A("🎯 立稿与定位<br/>问题 · 期刊")
    B("🧠 结构与证据<br/>主张 · 证据")
    C("📊 图表与结果<br/>面板 · 图注")
    D("✍️ 表达与语言<br/>逻辑 · 风格")
    E("📨 投稿与返修<br/>预检 · 回复")
    I(["🔎 贯穿全程的核查<br/>统计 · 引用 · 数据"])
    A --> B --> C --> D --> E
    I -.-> B
    I -.-> C
    I -.-> E
    classDef frame fill:#eef2ff,stroke:#818cf8,color:#312e81;
    classDef argument fill:#f5f0ff,stroke:#a78bfa,color:#4c1d95;
    classDef figures fill:#ecfdf5,stroke:#34d399,color:#064e3b;
    classDef prose fill:#fff7ed,stroke:#fb923c,color:#7c2d12;
    classDef response fill:#eff6ff,stroke:#60a5fa,color:#1e3a8a;
    classDef integrity fill:#f8fafc,stroke:#94a3b8,color:#334155,stroke-dasharray:4 3;
    class A frame;
    class B argument;
    class C figures;
    class D prose;
    class E response;
    class I integrity;
```

结构与证据先于句子润色，统计、引用与论断、数据可用性核查贯穿相关阶段。按任务从需要的位置进入；修改一个段落时，只处理相关层次。综述、survey 和 Perspective 有独立的架构路径。

图中的图形制作需加装 `--figure`；默认安装已包含图形规划、稿件修订与审稿回复。

[🗺️ 完整工作流](docs/workflow-map.md) · [📚 全部技能](docs/skill-map.md) · [✍️ 写作原则](docs/design-principles.md) · [📊 图形流程](docs/figure-workflow.md)

<a name="修改效果示例"></a>

## 🪄 修改效果示例

工作流同时处理稿件修订、图表与审稿回复。下面聚焦写作层：去掉项目日志式表达和防御性解释，同时保留理解结果所需的事实。

| 📝 修改前 | ✨ 修改后 | 🔒 保留什么 |
|---|---|---|
| “We carefully verified that survival changed by 1 percentage point (95% CI −3 to 5), which should not be overinterpreted.” | “Survival changed by 1 percentage point (95% CI −3 to 5), with no clear evidence of improvement.” | 效应值、置信区间及不确定性 |
| “These orderings should not be read as a universal ranking across all settings.” | “These orderings hold for the tested settings.” | 比较的适用范围 |
| “The analysis reads the final output from `results/final_scores.csv`.” | “The analysis uses the measured response scores.” | 科学对象；文件获取细节放在需要它的方法或数据说明中 |

这些是示意改写，不代表真实研究结果。影响科学解释或复现的条件必须保留。更多内容见[修改前后案例](skills/core/anti-defensive-writing/references/worked-examples.md)和[完整入门示例](examples/first-run/README.md)。

<a name="快速开始"></a>

## 🚀 快速开始

<a name="1-安装"></a>

### 📥 1. 安装

完整科研流程选择 27 个技能；只做论文写作和审稿，可选 19 个。完整集增加实际绘图、文献研究、结果分析、参考文献核验、会议论文与学术演示。本地安装需要 Bash 和 Python 3.9+；远程安装还需要 curl 和 tar。

**让代理自动安装：** 点击下方代码块右上角的复制按钮，再粘贴到代理对话中：

**完整科研流程：全部 27 个 skill**

```text
读取并执行 https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md，为当前环境安装 Nature Paper Skills 全部 27 个技能（all 完整集），并验证结果。
若页面读取失败，请使用可用的 GitHub 工具或 git clone 获取 main 分支源码，再读取根目录 INSTALL.md；不要用搜索摘要代替原文。
```

**论文写作与审稿：推荐的 19 个 skill**

```text
读取并执行 https://github.com/Boom5426/Nature-Paper-Skills/blob/main/INSTALL.md，为当前环境安装 Nature Paper Skills 推荐的 19 个技能，并验证结果。
若页面读取失败，请使用可用的 GitHub 工具或 git clone 获取 main 分支源码，再读取根目录 INSTALL.md；不要用搜索摘要代替原文。
```

无需指定 creator。[INSTALL.md](INSTALL.md) 让代理选择受支持的路径，自行取得资源并验证。网页版持久安装尚未验证，代理须确认账号注册能力后才能报告成功。

| 你使用的应用 | 从这里开始 |
|---|---|
| Codex：App、CLI 或 IDE | [Codex 安装](#install-codex-bash)；Windows 操作放在详细指南中 |
| Claude Code | [Claude Code 安装](#install-claude-code) |
| 网页版 ChatGPT Work | [网页版安装与可用性](#install-chatgpt-work-web)；自动安装尚未验证 |

<a name="install-codex-bash"></a>

<details>
<summary><b>Codex</b></summary>

Linux/macOS 运行：

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent codex --set all
```

此命令安装全部 27 个；需要 19 个写作与审稿技能时，将 `--set all` 换成 `--set recommended`。

Windows 请按 [Windows 安装说明](docs/installation-codex.md#windows-desktop-app)，选择 App 实际使用的原生 agent 或 WSL2 路径。

默认安装到 `~/.agents/skills`。刷新技能列表或新建会话，再选择 `paper-workflow`；CLI/IDE 可显式调用 `$paper-workflow`。环境要求和验证范围见 [Codex 安装指南](docs/installation-codex.md)。

如果使用内置 `skill-installer`，请指定包含 `SKILL.md` 的目录，例如 [`skills/core/paper-workflow`](https://github.com/Boom5426/Nature-Paper-Skills/tree/main/skills/core/paper-workflow)。仓库根目录是技能集合，不能作为单个 skill 安装；完整工作流需要哪些目录，见[技能地图](docs/skill-map.md)。

</details>

<a name="install-claude-code"></a>

<details>
<summary><b>Claude Code</b></summary>

在 Claude Code 所用的机器和用户环境中运行：

```bash
curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent claude --set all
```

此命令安装全部 27 个；需要 19 个写作与审稿技能时，将 `--set all` 换成 `--set recommended`。

默认安装到 `~/.claude/skills`。刷新或重新打开 Claude Code，再调用 `/paper-workflow`。环境要求和验证范围见 [Claude Code 安装指南](docs/installation-claude.md)。

</details>

<a name="install-chatgpt-work-web"></a>

<details>
<summary><b>网页版 ChatGPT Work</b></summary>

使用上方**任一条复制指令**，让代理自行取得资源并执行当前环境支持的安装流程；无需你点选 `@skill-creator`、运行 Python 或上传 ZIP。

**网页版自动安装尚未验证。** 当前账号须提供受支持的保存／注册流程；网页任务中下载了文件或生成了技能目录，不能证明新会话可调用。如果缺少注册能力，代理应直接说明原因。

可靠分发需由维护者发布插件，或由工作区管理员导入 GitHub marketplace。见[网页版分发与验证](docs/installation-chatgpt-work.md)；打包命令属于维护者操作。

</details>

仓库安装器会备份已有副本。添加 `--figure` 安装绘图技能，或用 `--set all` 安装全部 27 个 skill；安装范围、预览、更新和恢复命令见[安装选项](#安装选项)。

<a name="2-完成第一次修订"></a>

### ✍️ 2. 完成第一次修订

在本地 agent 中确认技能可见后，将当前稿件和相关结果放进工作目录，然后说：

```text
用 paper-workflow。依据 evidence.md 中的证据修改 draft.md 的 Results 段落。
保留测量值和图号，保存修订副本，并简要说明关键改动。
```

没有现成材料时，直接用[第一次完成修订](examples/first-run/README.md)，里面有输入、提示词和参考输出。Codex CLI/IDE 可用 `$paper-workflow` 明确调用；Claude Code 可用 `/paper-workflow`。

之后可以直接说“优化这篇论文”，也可以点名某个技能。工作流会先判断问题和范围，再执行需要的步骤，无需记住全部技能名。

<a name="按任务选择"></a>

## 🧩 按任务选择

| 想完成什么 | 提供什么 | 得到什么 | 入口 |
|---|---|---|---|
| 🧬 优化整篇论文 | 当前稿件、相关结果/图表、已确定的期刊 | 修订稿、关键修改、待补证据 | `paper-workflow` |
| ✍️ 修改一个段落 | 原文、上下文、修改范围 | 修改后的段落和必要说明 | `write-scientific-manuscript` |
| 🪄 去掉审计式／防御式表达 | 正文、SI、图注或数据声明 | 更直接的科学表达，保留数字与必要条件 | `anti-defensive-writing` |
| 📊 规划或制作图表 | 科学问题、结果表或现有图 | 面板方案；有数据和工具时输出图文件 | `figure-planner`；出图另加 `--figure` |
| 🔎 投稿前检查 | 最终稿、SI、参考文献和目标期刊 | 有定位、按重要性排序的问题；注明未检查项 | `submission-audit` |
| 📨 回复审稿意见 | 原始意见、稿件、已完成的新证据 | 保留编号的回复草稿及对应稿件修改 | `paper-workflow` |

要求“检查／给建议”时先交付诊断；要求“修改”时在授权范围内改稿。缺失的证据会指出，不会补写成已完成的实验。

完整提示词与任务准备方式见[常用任务示例](docs/task-recipes.md)。选择 `--set all` 还包含[可复算的统计示例](skills/research/results-analysis/USAGE.md)，其示例 helper 需要 SciPy。

<a name="安装选项"></a>

## 📦 安装选项

<details>
<summary><b>⚙️ 选择 agent、安装范围与技能组合</b></summary>

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

</details>

<details>
<summary><b>🛠️ 环境要求与技能加载排错</b></summary>

**本地安装器需要：** Codex 或 Claude Code、Bash、Python 3.9+（安装只用标准库，无需额外 pip 包）。远程安装还需要 `curl` 和 `tar`。Windows 操作见 [Codex Windows 安装说明](docs/installation-codex.md#windows-desktop-app)。[网页版 ChatGPT Work](#install-chatgpt-work-web)采用独立分发流程。已验证范围见[环境与文件格式](docs/compatibility.md)。

如果找不到技能，刷新技能列表或重新打开会话，再看[排错说明](docs/installation-management.md#troubleshooting)。分 agent 安装说明：[Codex](docs/installation-codex.md) · [Claude Code](docs/installation-claude.md)。

</details>

<details>
<summary><b>🔄 查看安装器、更新、恢复与固定版本</b></summary>

可以先读 [install.sh](install.sh)，或按上方命令克隆后安装。更新前会备份已有技能，详见[更新与恢复](docs/installation-management.md)。

多个 agent 共用一份安装副本时，可采用[手动软链接布局](docs/installation-management.md#manual-layout-one-canonical-copy-linked-into-the-agent-directory)。更新、检查与恢复都针对中央安装目录执行；已有 agent 条目会保留。

通过 `--ref <完整提交SHA>` 固定版本；安装器会记录来源和文件哈希。版本变化见 [CHANGELOG](CHANGELOG.md)。

</details>

<a name="适用范围与边界"></a>

## 🧭 适用范围与边界

面向生命科学、计算生物学、方法、基准和资源类期刊论文。用户明确的期刊要求及项目决定优先于默认 Nature 风格。本项目独立于 Nature Portfolio，不预测录用结果。

技能提供操作规则与部分辅助脚本，不自带 Word 编辑器、PDF 渲染器、LaTeX 环境、联网访问权限或实验数据。[兼容说明](docs/compatibility.md)分别列出可读取、可编辑与可导出的范围。

仓库测试覆盖脚本、安装与文件一致性。[行为案例](evals/README.md)用于检查修改范围、证据保留及缺少能力时的诚实报告；实际运行记录与适用边界单独列出。

<a name="参与贡献"></a>

## 🤝 参与贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。影响用户行为的修改应附任务案例或示例，中英文首页同步维护。组件来源见 [ATTRIBUTION.md](ATTRIBUTION.md)。

<a name="致谢"></a>

## 💙 致谢

部分内容受到 [OpenLAIR/dr-claw](https://github.com/OpenLAIR/dr-claw)、[Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) 和 Claude Science skill pack 的启发。

图形层还参考了 [ChenLiu-1996/figures4papers](https://github.com/ChenLiu-1996/figures4papers) 的设计经验。本仓库不分发该项目的代码或文字；详见 [THIRD_PARTY_NOTICES](skills/figure/nature-figure/THIRD_PARTY_NOTICES.md)。

<a name="许可"></a>

## ⚖️ 许可

原创内容使用 [MIT](LICENSE)。含 Apache-2.0 材料的组件保留 [LICENSE-APACHE](LICENSE-APACHE) 与 [NOTICE](NOTICE)，安装器分发时也会携带。覆盖范围见 [ATTRIBUTION](ATTRIBUTION.md)。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Boom5426/Nature-Paper-Skills&type=Date)](https://star-history.com/#Boom5426/Nature-Paper-Skills&Date)
