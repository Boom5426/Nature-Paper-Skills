给下列正文和 SI 的定义公式加序号，保留现有的编号规则、标签和引用。参数取值集合和中间推导不要编号。公式内容、标点和段落意思不改；只回复修订后的 LaTeX，不创建文件。环境不能编译或渲染，不能声称已经完成 PDF 检查。

正文片段：

```latex
\usepackage{amsmath}
\begin{document}
The baseline in equation~\eqref{eq:baseline} uses
\begin{equation}\label{eq:baseline}
S(q,d)=\cos(\bar q,\bar d).
\end{equation}
The magnitude-aware score is
\[
M(q,d)=-\|\bar q-\bar d\|_2,
\]
where the two means use matched controls.

The thresholds were varied over
\[
\{0.10,\;0.25,\;0.40,\;0.50\}.
\]
For the following intermediate derivation,
\begin{align*}
r_0 &= \delta,\\
r_1 &= \delta.
\end{align*}
\end{document}
```

SI 是独立编译的文档，现有片段：

```latex
\usepackage{amsmath}
\renewcommand{\theequation}{S\arabic{equation}}
\begin{document}
The existing score is
\begin{equation}\label{eq:si:score}
S(q,d)=-D(q,d).
\end{equation}
The utility contrast is
\[
A=u(d_M,0)-u(d_C,0).
\]
\end{document}
```
