# Nature-Paper-Skills

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Nature-first](https://img.shields.io/badge/focus-Nature%20series-1f6feb)](docs/venue-routing.md)
[![Workflow](https://img.shields.io/badge/workflow-claim--driven-blue)](docs/workflow-map.md)
[![Codex](https://img.shields.io/badge/agent-Codex-0a7ea4)](docs/installation-codex.md)
[![Claude Code](https://img.shields.io/badge/agent-Claude%20Code-cc785c)](docs/installation-claude.md)
[![Contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/Boom5426/nature-paper-skills?style=social)](https://github.com/Boom5426/nature-paper-skills/stargazers)

简体中文 | [English](README.en.md)

这是一个面向 `Nature` 系列期刊稿件的 agent skill 仓库，重点覆盖从初稿搭建、结构修订、图文对齐、引用核验、投稿前预检到返修回复的完整链路。

本仓库是强约束的，不是“通用论文写作技巧集合”。默认立场是 journal-first、claim-driven、证据边界优先。

## 快速开始

最快的上手方式不是先通读所有 skill，而是先把推荐安装集装好，然后直接让 agent 帮你路由下一步。

### 第 1 步：克隆仓库

```bash
git clone https://github.com/Boom5426/nature-paper-skills.git
cd nature-paper-skills
```

### 第 2 步：选一种安装方式

#### 方式 A：直接让 Codex 安装

把下面这句话直接发给 Codex：

```text
把当前仓库里的推荐 skills 安装到 ~/.codex/skills/：paper-workflow、paper-bootstrap、nature-portfolio-playbook、scientific-writing、manuscript-optimizer、results-section-revision、figure-planner、citation-verifier、submission-audit、rebuttal-response。复制整个 skill 目录，不要只复制 SKILL.md。安装完成后，列出已安装目录，并用 paper-workflow 帮我判断当前稿件下一步该用哪个 skill。
```

#### 方式 B：直接让 Claude Code 安装

把下面这句话直接发给 Claude Code：

```text
把当前仓库里的推荐 skills 安装到 ~/.claude/skills/：paper-workflow、paper-bootstrap、nature-portfolio-playbook、scientific-writing、manuscript-optimizer、results-section-revision、figure-planner、citation-verifier、submission-audit、rebuttal-response。复制整个 skill 目录，不要只复制 SKILL.md。安装完成后，列出已安装目录，并用 paper-workflow 帮我判断当前稿件下一步该用哪个 skill。
```

#### 方式 C：手动安装

如果你更想自己动手，先克隆仓库，然后复制完整 skill 目录。

Codex:

```bash
mkdir -p ~/.codex/skills
cp -R \
  skills/core/paper-workflow \
  skills/core/paper-bootstrap \
  skills/core/scientific-writing \
  skills/core/manuscript-optimizer \
  skills/core/results-section-revision \
  skills/core/figure-planner \
  skills/core/citation-verifier \
  skills/core/submission-audit \
  skills/core/rebuttal-response \
  skills/venue/nature-portfolio-playbook \
  ~/.codex/skills/
```

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -R \
  skills/core/paper-workflow \
  skills/core/paper-bootstrap \
  skills/core/scientific-writing \
  skills/core/manuscript-optimizer \
  skills/core/results-section-revision \
  skills/core/figure-planner \
  skills/core/citation-verifier \
  skills/core/submission-audit \
  skills/core/rebuttal-response \
  skills/venue/nature-portfolio-playbook \
  ~/.claude/skills/
```

### 安装后第一句话

装完以后，最短路径通常是直接说：

```text
用 paper-workflow 帮我判断这篇稿子下一步该用哪个 skill。
```

更详细的安装说明见 [docs/installation-codex.md](docs/installation-codex.md) 和 [docs/installation-claude.md](docs/installation-claude.md)。

## 默认工作流

```text
paper-bootstrap
  -> nature-portfolio-playbook
  -> scientific-writing / manuscript-optimizer
  -> figure-planner
  -> results-section-revision
  -> citation-verifier
  -> submission-audit
  -> rebuttal-response
```

默认假设：
- 以期刊稿为主，不以会议稿为主
- 未明确 venue 时按 `Nature` 系列期刊导向处理
- 先修结构与证据链，再做语句级润色

## 仓库里有什么

### 核心技能
- `paper-workflow`: 选择正确 skill 并按正确顺序推进
- `paper-bootstrap`: 初始化论文项目、source of truth 和状态文件
- `scientific-writing`: 章节撰写与重写
- `manuscript-optimizer`: 结构与证据链修复
- `results-section-revision`: Results 小节级叙述结构修复
- `figure-planner`: 一图一主张、panel 角色、legend 同步
- `citation-verifier`: 引用与 BibTeX 卫生检查
- `submission-audit`: 投稿前/返修前总预检
- `rebuttal-response`: 审稿意见回复与改稿联动

### 期刊定位技能
- `nature-portfolio-playbook`: 做 `Nature` 系列期刊范围内的定位判断，并执行投稿前预检

### 研究与审稿技能
- `paper-analyzer`
- `academic-researcher`
- `results-analysis`
- `paper-reviewer`

### 可选技能
- `reference-audit-guide`
- `conference-paper-writing`
- `academic-presentations`

## 仓库结构

```text
nature-paper-skills/
├── .github/
├── docs/
├── examples/
├── skills/
│   ├── core/
│   ├── venue/
│   ├── research/
│   ├── review/
│   └── optional/
├── .gitignore
├── ATTRIBUTION.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── README.en.md
└── README.zh.md
```

脚本随 skill 目录分发，保证 skill 可独立复制和复用。

## 设计原则

- claim-driven，而不是 panel-driven
- 一张主图尽量只承载一个主结论
- 图注是结果叙述的第二层，不是只解释坐标轴
- 主文只保留支撑本段 claim 的关键数字
- 对已有章节重写前，先做 reverse outline
- 不允许前半部分（Abstract/Introduction）比下游证据更强
- venue 与 article type 要前置决策，不要末期再救火

详见：
- [workflow-map.md](docs/workflow-map.md)
- [skill-map.md](docs/skill-map.md)
- [venue-routing.md](docs/venue-routing.md)
- [design-principles.md](docs/design-principles.md)

## 仓库元信息

GitHub 仓库 description、topics 和 About 面板文案统一放在 [.github/repo-metadata.md](.github/repo-metadata.md)。

## 适用范围

适用于：
- `Nature` 系列生命科学/计算生物/方法学论文
- methods / frameworks / benchmarks / resources / translational 分析类工作
- 写作、修稿、投稿前预检与返修回复

不追求：
- 覆盖所有期刊写作风格
- 会议模板大全
- 全量研究平台编排
- 替代官方 author guidelines

## 贡献

贡献规范、命名约定和 PR 预期见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 归因

来源归因见 [ATTRIBUTION.md](ATTRIBUTION.md)。

## 致谢

本仓库部分代码和灵感来源于 [OpenLAIR/dr-claw](https://github.com/OpenLAIR/dr-claw) and [罗小罗团队Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)，感谢所有为本项目贡献代码、文档和测试的开发者社区成员。

