你在协助我写论文，全程遵守【发布会原则】：论文是发布会，不是工作汇报。1.只围绕最强优势组织叙事；2.不按"做了什么、试过什么、哪些失败了"的过程写；3.禁止自我削弱表达("遗憾的是""仅""仍明显落后""效果有限")，不替审稿人总结弱点；4.打不赢的指标不设为比赛，换评价维度或比较口径；5.不占优的结果不说输，从目标差异或合理权衡解释；6.优势必须主动说清楚，别指望审稿人自己从表格里发现；7.每个实验必须有论证职责，没有就删；8.摘要引言像发布会开场：问题→缺口→思路→最硬的结果；9.结论只强化记忆点，不突然自我否定。现在检查我发你的文字里所有的防御性写作，逐处指出并给出改法。

目标期刊 Nature Methods。数字都已核定，不要改数字。最后给出摘要、Results 段落和 Discussion 末段改好的全文。只在回复中给出，不创建文件。

Introduction 最后一段（供参考，不用改）：

> Most compounds that a screen would profile next share no scaffold with any compound already measured. Here we present ScaffoldResponse, which predicts the transcriptional response to a compound from its chemical structure and is designed to transfer to scaffolds absent from training.

摘要：

> Predicting transcriptional responses to small molecules is an important problem in drug discovery. We developed ScaffoldResponse, a graph neural network, after first trying a transformer encoder that did not improve over a multilayer perceptron. Unfortunately, on the standard random split ScaffoldResponse only reaches a Pearson r of 0.62, still clearly behind scGPT-ft (0.66). On held-out scaffolds it reaches 0.48 against 0.31 for scGPT-ft, and on dose extrapolation it matches the best baseline. These results suggest that ScaffoldResponse may be useful, although its gains on random splits are limited.

Results 中的一段：

> We first trained a transformer encoder on the same features, which did not improve over the MLP baseline (r = 0.58 against 0.59), and then tried adding pathway priors, which helped only marginally. The final model therefore uses a graph encoder. On the random split, ScaffoldResponse reached r = 0.62 (95% CI 0.60 to 0.64), slightly lower than scGPT-ft (0.66, 0.64 to 0.68). On held-out scaffolds it reached 0.48 (0.45 to 0.51) against 0.31 (0.28 to 0.34) for scGPT-ft and 0.27 (0.24 to 0.30) for the MLP. On dose extrapolation it matches the best baseline (difference +0.01, 95% CI -0.08 to +0.10). Differences among the four baselines on this split ranged from 0.02 to 0.05. This gap on the random split is likely the price of not using target annotations. Adding target annotations raised random-split r from 0.62 to 0.65 and lowered held-out-scaffold r from 0.48 to 0.41 (Supplementary Table 4). With shuffled compound labels, held-out-scaffold r fell to 0.02, so the gain does not come from compound-independent structure in the responses.

Discussion 最后一段：

> ScaffoldResponse predicts responses to new scaffolds better than existing models. However, we must acknowledge that the model was evaluated in only three cancer cell lines, and its performance in primary cells remains unknown, which limits its use. Moreover, it still lags behind scGPT-ft on random splits.
