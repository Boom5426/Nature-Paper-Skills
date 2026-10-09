帮我把这篇研究论文的摘要改好，目标期刊是 Nature Methods。只改摘要，其他部分不动。只在回复中给成品，不创建文件。

当前摘要：

> Single-cell technologies have transformed biology and generated unprecedented amounts of data. Predicting how cells respond to genetic perturbations is an important problem, and many methods have been proposed, but they all have limitations. Here we propose CellShift, a novel deep learning framework that leverages optimal transport and attention. CellShift achieves a Pearson delta of 0.61, 0.58 and 0.66, an MSE of 0.012, 0.015 and 0.010, and a direction accuracy of 0.78, 0.74 and 0.81 on screens S1, S2 and S3, significantly outperforming all existing methods (P < 0.001). CellShift will be a powerful tool for virtual cell modeling.

Results 的当前结论（合成示例数据，数字已核定）：

- 三个扰动筛选数据集 S1、S2、S3，按扰动划分，测试集中的扰动在训练中从未出现。对照方法为均值偏移基线、线性模型和两个已发表的深度模型 M1、M2，每个方法 5 个随机种子。
- S1 和 S2 上，CellShift 的 Pearson delta 最高：S1 为 0.61，次优 M1 为 0.55；S2 为 0.58，次优线性模型为 0.54。
- S1 的未见组合扰动上，CellShift 的方向准确率为 0.78，次优 M2 为 0.69。
- MSE 没有一致的最优方法；S2 上线性模型的 MSE 最低。
- S3 正在因预处理修正而重跑，现有 S3 数字可能改变，Results 中 S3 小节尚未定稿。
- 稿件中没有报告 P 值。
