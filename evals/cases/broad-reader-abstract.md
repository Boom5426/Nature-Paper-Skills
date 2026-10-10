帮我改一下这篇研究论文的摘要，目标期刊 Nature Methods。只改摘要，其他部分不动。只在回复中给成品，不创建文件。

当前摘要：

> Single-cell RNA sequencing combined with multiplexed chemical screening enables high-throughput profiling of drug responses. However, existing deep generative models fail to generalize to unseen drug combinations. Here we propose DoseFormer, a conditional variational autoencoder with a cross-attention drug encoder and a dose-aware latent arithmetic module. On screen A and two in-house combinatorial screens, DoseFormer improves the R² of the top-50 differentially expressed genes and reduces the energy distance relative to two published generative models. Ablations confirm the contribution of each module. DoseFormer provides a scalable framework for in silico drug screening.

Introduction 第一段（已定稿）：

> Combination therapies are central to cancer treatment, but the number of possible drug pairs grows quadratically with the number of drugs, so most pairs are never tested. Whether a pair acts additively or produces effects beyond the sum of its single-drug effects cannot currently be predicted from single-drug measurements in individual cells.

Results 的当前结论（合成示例数据，数字已核定）：

- 公开筛选 A 只含单药处理；自建筛选 B 和 C 含药物组合。测试集是训练中从未一起出现过的药物组合，其中每种药物单独出现过。对照为两个已发表的生成模型 G1、G2，每个方法 5 个随机种子。
- 在未见过的组合上，DoseFormer 对 50 个变化最大的基因的表达变化预测 R² 为：B 上 0.71（次优 G2 为 0.63），C 上 0.66（次优 G2 为 0.60）。
- 预测细胞分布与实测分布的能量距离：B 上比 G2 低 18%；C 上与 G2 的差异在种子间波动范围内。
- 筛选 B 的 40 个未见组合中，DoseFormer 正确判断了 31 个组合的效应是否偏离单药效应之和（即协同或拮抗），G2 为 22 个。
- 去掉剂量模块后，B 上的 R² 下降 0.04。
- 稿件中没有报告 P 值。
