正文图尽量放页顶，整图和图注尽量同页；SI 长表调整得更易读。只在回复里给最小 LaTeX 修改建议。图文件、图注文字、表格数据和分析都已批准，此轮不得更改。当前环境不能编译、渲染或读取图文件，不创建文件。

使用普通 article 类，已有 graphicx、float、caption、longtable 和 pdflscape。版心高度 650 pt。正文图按当前宽度显示时高 360 pt，图注约 140 pt。目前的图：

```latex
\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{approved_main.pdf}
\caption{Approved caption retained verbatim.}
\label{fig:approved}
\end{figure}
```

SI 表是一张连续的 80 行患者表，不能按独立实验拆分。当前字号 10 pt；12 列在纵向版心中挤得难读。SI 允许横向页面。表采用 longtable，已有重复列标题，所有行、单位和说明都必须保留。正文其他小节不需要另起页，也没有请求重绘图。
