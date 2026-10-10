这是我们 ICLR 投稿附录里的一小节（LaTeX 源码，合成示例，数字已核定）。帮我改得更像 ICLR 论文：去掉审计味和防御腔，但 ICLR 审稿人需要的信息要保留。只在回复中给改后的 LaTeX 和简短说明，不创建文件。

```latex
\subsection{Evaluation protocol}
% numbers copied from /home/lab/vcell/ledger.md entry L-17; do not edit by hand
Splits were assigned deterministically by SHA-256 hashing of gene symbols. The hash function and
salt were locked at commit 4f2a9c1 before any scoring, so the assignment cannot have been tuned.
All hyperparameters of the scorer were selected on the development split. To be clear, the
held-context evaluation pool was never used to choose hyperparameters, so no leakage is possible.

The routing analysis was preregistered and frozen before evaluation. Routing is supported if the
lower bound of the 95\% bootstrap confidence interval of the gain over the base scorer exceeds 0.
We used the unit-target variant, which was prespecified. On the held-context pool its gain was
$+0.0492$ (95\% CI $[0.0121, 0.0868]$), so the criterion was met.
% unit-target chosen after comparing both variants on the held-context pool
% raw-target variant on the same pool: +0.0454 (95% CI [0.0087, 0.0819]); not reported

Nothing is trained in the routing step and no weight is fitted. The base scorer was trained once
(seed 3407). Confidence intervals use 10{,}000 bootstrap resamples over contexts (seed 7). As a
sanity check, all values above were verified against the artifacts in
\texttt{results/manifest.sha256}. Again, nothing is trained in the routing step.
```
