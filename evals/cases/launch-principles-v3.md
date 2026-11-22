# 论文审查与修改：发布会原则 V3

严格按照**发布会原则**审查和修改论文：**论文是发布会，不是工作汇报。科学真实性是底线，最强贡献是叙事中心，读者理解是最终检验。**

## 一、核心原则

1. **聚焦最强贡献**：围绕最重要的科学问题、最有价值的发现和最有力的证据组织全文。明确论文最希望读者记住什么，其他内容为此服务。

2. **不写工作流水账**：不按研究过程、尝试顺序或实验清单展开。按照科学论证的需要选择内容、安排顺序，而不是复述做过的工作。

3. **不主动削弱贡献**：避免不必要的自我否定、弱化措辞和防御性解释。不突出缺乏优势的比较，但必须如实呈现影响核心结论的负面证据与适用边界。

4. **让优势成为结论**：不要只堆砌数字或期待读者自行发现贡献。每项关键结果都应明确回答：发现了什么、证明了什么、为什么重要。比较指标必须服务于科学问题。

5. **实验服务于科学主张**：每个关键实验都应有明确的论证职责。区分实验证据、合理推断和未经验证的主张。删除重复、无关或不能增强论证的内容。

6. **建立清晰的叙事主线**：摘要和引言遵循“重要问题 → 关键缺口 → 核心思路 → 最强证据”。结果部分围绕关键发现展开，讨论解释其科学意义，结论强化最重要的记忆点。

7. **面向大同行，简洁准确**：默认读者具备相关基础，但不了解本文具体问题。优先使用常见、直接、准确的学术表达，减少术语堆砌、冗余修饰和不必要的技术细节，同时保持科学严谨性。

8. **首次阅读测试（最重要的检查之一）**：完全站在第一次接触论文的大同行视角，不预设作者意图，独立判断：
   - 读完标题、摘要和引言，读者认为这篇论文究竟想解决什么问题？为什么值得关注？
   - 读者认为最重要的新贡献是什么？能否理解它与已有工作的本质区别？
   - 读完主要图表和结果，读者最终会记住什么科学发现？这些证据是否真正支撑核心主张？
   - 哪些地方会让读者困惑、误解、失去兴趣，或需要自行推断作者没有说清楚的结论？

   **重点检查“作者想传达的贡献”与“读者实际接收到的信息”是否一致。** 如果最强贡献没有成为读者最自然的理解，应优先调整叙事重点、信息层级和论证顺序，而不是只做语言润色。

## 二、执行要求

**先从整体审视论文，再逐处修改文字。**

**第一步：整体诊断**

以首次阅读者的视角，简要回答：这篇论文实际上在讲什么？最强贡献是什么？读者最可能记住什么？目前叙事最影响说服力的地方在哪里？

重点判断科学贡献是否突出、论证是否成立、信息主次是否合理，以及是否存在需要调整的章节或段落结构。

**第二步：逐处审查**

检查全文所有文字，包括标题、摘要、引言、方法、结果、讨论、结论、图表标题及图注。

按照论文出现顺序，针对每个有实质优化价值的位置给出：

- **原文**：准确引用需要修改的文字，并标明位置。
- **问题**：指出具体的叙事、逻辑、证据或表达问题，以及它对读者理解的影响。
- **建议改法**：给出可以直接替换的完整文字；如果主要问题是结构或顺序，则明确提出调整方案。

**第三步：优先级判断**

区分影响核心贡献和科学论证的问题，与一般语言优化。优先解决前者，不陷入细枝末节。

## 三、修改边界

- **不为了修改而修改**：没有实质问题的内容保持不变。
- **不编造、不夸大、不掩盖**：任何修改都必须忠于已有数据和证据。
- **不把审查变成弱点清单**：重点是让真实贡献得到最清楚、最有力的表达，而非替审稿人寻找无关紧要的批评。
- **优先提升论文，而非句子**：当问题源于叙事定位、证据组织或信息层级时，应从结构上解决，不做表面润色。

**最终目标：让第一次阅读论文的大同行，能够轻松理解其重要性，准确识别其独特贡献，并被最有力的证据说服。**

严格按照这个来审查下面的文字。目标期刊 Nature Methods。数字都已核定，不要改数字。只在回复中给出，不创建文件。

Introduction 最后一段（供参考，不用改）：

> Most compounds that a screen would profile next share no scaffold with any compound already measured. Here we present ScaffoldResponse, which predicts the transcriptional response to a compound from its chemical structure and is designed to transfer to scaffolds absent from training.

摘要：

> Predicting transcriptional responses to small molecules is an important problem in drug discovery. We developed ScaffoldResponse, a graph neural network, after first trying a transformer encoder that did not improve over a multilayer perceptron. Unfortunately, on the standard random split ScaffoldResponse only reaches a Pearson r of 0.62, still clearly behind scGPT-ft (0.66). On held-out scaffolds it reaches 0.48 against 0.31 for scGPT-ft, and on dose extrapolation it matches the best baseline. These results suggest that ScaffoldResponse may be useful, although its gains on random splits are limited.

Results 中的一段：

> We first trained a transformer encoder on the same features, which did not improve over the MLP baseline (r = 0.58 against 0.59), and then tried adding pathway priors, which helped only marginally. The final model therefore uses a graph encoder. On the random split, ScaffoldResponse reached r = 0.62 (95% CI 0.60 to 0.64), slightly lower than scGPT-ft (0.66, 0.64 to 0.68). On held-out scaffolds it reached 0.48 (0.45 to 0.51) against 0.31 (0.28 to 0.34) for scGPT-ft and 0.27 (0.24 to 0.30) for the MLP. On dose extrapolation it matches the best baseline (difference +0.01, 95% CI -0.08 to +0.10). Differences among the four baselines on this split ranged from 0.02 to 0.05. This gap on the random split is likely the price of not using target annotations. Adding target annotations raised random-split r from 0.62 to 0.65 and lowered held-out-scaffold r from 0.48 to 0.41 (Supplementary Table 4). With shuffled compound labels, held-out-scaffold r fell to 0.02, so the gain does not come from compound-independent structure in the responses.

Discussion 最后一段：

> ScaffoldResponse predicts responses to new scaffolds better than existing models. However, we must acknowledge that the model was evaluated in only three cancer cell lines, and its performance in primary cells remains unknown, which limits its use. Moreover, it still lags behind scGPT-ft on random splits.
