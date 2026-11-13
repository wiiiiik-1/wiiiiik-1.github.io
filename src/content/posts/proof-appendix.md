---
title: 附录：公式与证明索引
description: 站内所有关键公式的推导集中在这里——从调和数的面积夹逼到 UCB 的 16log n/Δ²，每条给出条件、结论、证明与出处。
date: 2026-11-04
tags: ["附录", "证明", "数学基础", "数理统计"]
draft: false
featured: false
lang: zh-CN
---

> **这是什么**：一个「活」的证明附录。正文里出现过的公式，只要推导超过三行，就收在这里，正文只留结论。
> **体例**：每条固定四段——**条件 / 结论 / 证明 / 用在哪**。不写「显然」「易证」，除非真的两行能完。
> **怎么用**：读到正文某个式子卡住时，按编号跳过来；反过来，每条都给了它在哪一节被用到。
> **不在这里证明的**：见 F 节，附不证明的理由。
> **系列位置**：附录，不参与主线顺序；它是 [数学工具箱](/posts/math-toolbox/) 与后面各篇的技术底座。

---

## A 分析工具

### A1 调和数的面积夹逼

**结论**：$H_n=\sum_{t=1}^n\frac1t=\ln n+\gamma+O(1/n)$，其中 $\gamma\approx0.5772$。

**证明**。因为 $1/x$ 在 $[1,\infty)$ 上递减，矩形面积被曲线夹住：

$$\int_1^{n+1}\frac{\mathrm{d}x}{x}\ \le\ \sum_{t=1}^{n}\frac1t\ \le\ 1+\int_1^{n}\frac{\mathrm{d}x}{x},$$

即 $\ln(n+1)\le H_n\le 1+\ln n$，所以 $H_n=\ln n+O(1)$。

常数 $\gamma$ 的存在性：令 $a_n=H_n-\ln n$。由 $\log(1+x)\ge \frac{x}{1+x}$（对 $x>0$）得

$$a_{n+1}-a_n=\frac{1}{n+1}-\ln\!\Big(1+\frac1{n+1}\Big)\le0,$$

且 $a_n\ge \ln(n+1)-\ln n\ge0$，单调有下界，故收敛，极限记为 $\gamma$。$O(1/n)$ 来自 $a_n-\gamma=\int_n^{\infty}\frac{\{x\}}{x^{2}}\,\mathrm{d}x$ 的估值。

**用在哪**：[数学工具箱 §2.2](/posts/math-toolbox/#2-求和与级数)、[第 2 篇 §4.4](/posts/multi-armed-bandits-intro/#44-对数-regret-的概率含义)。

### A2 两个对数不等式

**结论**：对 $x>-1$ 有 $\log(1+x)\le x$；对 $u<1$ 有 $1-u\le e^{-u}$。

**证明**。令 $f(x)=x-\log(1+x)$，则 $f(0)=0$，$f'(x)=\frac{x}{1+x}$ 在 $x>0$ 时为正、$x<0$ 时为负，故 $0$ 是全局最小值。取 $x=-u$ 得 $\log(1-u)\le -u$，两边取指数即第二式。

**用在哪**：[数学工具箱 §3](/posts/math-toolbox/#3-对数与指数三个反复用的不等式)、ETC 的指数项。

### A3 二项系数的上界

**结论**：$\binom{n}{k}\le\left(\dfrac{en}{k}\right)^{k}$。

**证明**。$\binom{n}{k}=\dfrac{n(n-1)\cdots(n-k+1)}{k!}\le\dfrac{n^{k}}{k!}$，而由 Stirling 的下界 $k!\ge (k/e)^{k}$，于是 $\binom{n}{k}\le n^{k}\left(\dfrac{e}{k}\right)^{k}=\left(\dfrac{en}{k}\right)^{k}$。

**用在哪**：二项尾界的量级估计；[数学工具箱 §4.3](/posts/math-toolbox/#4-渐进记号)。

### A4 等比级数与一次矩

**结论**：$|r|<1$ 时 $\sum_{t\ge0}r^{t}=\dfrac{1}{1-r}$，$\sum_{t\ge1}t\,r^{t}=\dfrac{r}{(1-r)^{2}}$。

**证明**。第一式是等比求和取极限。对第一式关于 $r$ 求导：$\sum_{t\ge1}t\,r^{t-1}=\dfrac{1}{(1-r)^{2}}$，两边乘 $r$ 得第二式。求导在 $|r|<1$ 内一致收敛，可以逐项求。

**用在哪**：ETC 的界里对 $m$ 求和、TS 的几何型估计。

## B 概率不等式

### B1 Markov 不等式

**条件**：$X\ge0$，$\mathbb{E}X<\infty$。**结论**：$\mathbb{P}(X\ge a)\le\dfrac{\mathbb{E}X}{a}$。

**证明**。$\mathbb{E}X\ge\mathbb{E}[X\mathbf{1}\{X\ge a\}]\ge a\,\mathbb{P}(X\ge a)$，两边除以 $a$。

**用在哪**：B2、B4、B5 的起点。

### B2 Chebyshev 不等式

**条件**：$\mathrm{Var}(X)<\infty$。**结论**：$\mathbb{P}(|X-\mu|\ge a)\le\dfrac{\mathrm{Var}(X)}{a^{2}}$。

**证明**。对非负随机变量 $(X-\mu)^{2}$ 用 Markov，取阈值 $a^{2}$。

**用在哪**：[概率论基础 §6.1](/posts/probability-foundations/#6-极限定理)、弱大数定律（C4）。

### B3 Hoeffding 引理

**条件**：$X\in[a,b]$，$\mathbb{E}X=\mu$。**结论**：对一切 $t$，$\mathbb{E}e^{t(X-\mu)}\le e^{t^{2}(b-a)^{2}/8}$。

**证明**。$e^{tx}$ 凸，故在 $[a,b]$ 上低于端点连线：

$$e^{tx}\le\frac{b-x}{b-a}e^{ta}+\frac{x-a}{b-a}e^{tb}.$$

取期望，记 $p=\frac{\mu-a}{b-a}$、$w=t(b-a)$：

$$\mathbb{E}e^{tX}\le e^{t\mu}\big[(1-p)e^{-pw}+p\,e^{(1-p)w}\big].$$

令 $\psi(w)=\log((1-p)e^{-pw}+pe^{(1-p)w})$。直接求导得 $\psi(0)=\psi'(0)=0$，且

$$\psi''(w)=\frac{p(1-p)e^{w}}{(1-p+pe^{w})^{2}}=z(1-z)\le\frac14,\qquad z=\frac{pe^{w}}{1-p+pe^{w}}\in(0,1).$$

于是 $\psi(w)=\int_0^{w}(w-s)\psi''(s)\,\mathrm{d}s\le\frac{w^{2}}{8}$，即得。

**用在哪**：[数学工具箱 §5.3.1](/posts/math-toolbox/#531-补hoeffding-的四步)、B4、B6。

### B4 Hoeffding 定理

**条件**：$X_1,\dots,X_n$ 独立，$X_i\in[a_i,b_i]$，$\mu_i=\mathbb{E}X_i$。**结论**：

$$\mathbb{P}(|\bar X-\mu|\ge\epsilon)\le2\exp\!\Big(-\frac{2n^{2}\epsilon^{2}}{\sum_i(b_i-a_i)^{2}}\Big).$$

等长区间时化为 $2e^{-2n\epsilon^{2}/(b-a)^{2}}$。

**证明**。对 $t>0$，由 Markov：

$$\mathbb{P}(\bar X-\mu\ge\epsilon)\le e^{-t\epsilon}\prod_i\mathbb{E}e^{t(X_i-\mu_i)/n}\le\exp\!\Big(-t\epsilon+\frac{t^{2}}{8n^{2}}\sum_i(b_i-a_i)^{2}\Big),$$

第二式由 B3 与独立性。对 $t$ 求最小：$t^{*}=\dfrac{4n^{2}\epsilon}{\sum_i(b_i-a_i)^{2}}$，代回得单边 $\exp\!\big(-\frac{2n^{2}\epsilon^{2}}{\sum_i(b_i-a_i)^{2}}\big)$。对 $-X$ 重复一次，union bound 得 $2$ 倍。

**用在哪**：置信区间、[第 3 篇 §3.2](/posts/from-etc-to-ucb/#32-置信界从哪来)、[第 1 篇 §3.6](/posts/hypothesis-testing-and-estimation/#36-置信区间confidence-interval用-hoeffding-不等式做区间估计)。

### B5 次高斯推出尾界

**条件**：$\mathbb{E}e^{t(X-\mu)}\le e^{\sigma^{2}t^{2}/2}$ 对一切 $t$ 成立。**结论**：$\mathbb{P}(|X-\mu|\ge\epsilon)\le 2e^{-\epsilon^{2}/(2\sigma^{2})}$。

**证明**。同 B4：$\mathbb{P}(X-\mu\ge\epsilon)\le\exp(-t\epsilon+\sigma^{2}t^{2}/2)$，取 $t=\epsilon/\sigma^{2}$ 得 $e^{-\epsilon^{2}/(2\sigma^{2})}$；另一侧同理。

**用在哪**：[数学工具箱 §5.6](/posts/math-toolbox/#56-次高斯从有界到方差)。

### B6 有界推出次高斯

**结论**：$X\in[a,b]\Rightarrow X$ 是 $\sigma=\frac{b-a}{2}$-次高斯。

**证明**。B3 给出 $\mathbb{E}e^{t(X-\mu)}\le e^{t^{2}(b-a)^{2}/8}$，与定义 $e^{\sigma^{2}t^{2}/2}$ 对齐：$\frac{(b-a)^{2}}{8}=\frac{\sigma^{2}}{2}\Rightarrow\sigma=\frac{b-a}{2}$。

**用在哪**：$\mathrm{Bern}(p)$ 的 $\sigma=\frac12$；UCB 的 bonus。

### B7 union bound

**结论**：$\mathbb{P}\big(\bigcup_i A_i\big)\le\sum_i\mathbb{P}(A_i)$。

**证明**。对 $n=2$：$\mathbb{P}(A\cup B)=\mathbb{P}(A)+\mathbb{P}(B)-\mathbb{P}(A\cap B)\le\mathbb{P}(A)+\mathbb{P}(B)$。对 $n$ 用归纳。不需要独立性。

**用在哪**：[第 3 篇 §3.3](/posts/from-etc-to-ucb/#33-为什么取-delta-dfrac1n2)、B4 的双边化。

### B8 Jensen 不等式

**条件**：$\varphi$ 凸，$\mathbb{E}|X|<\infty$，$\mathbb{E}|\varphi(X)|<\infty$。**结论**：$\varphi(\mathbb{E}X)\le\mathbb{E}\varphi(X)$。

**证明**。凸函数在任意点 $x_0$ 有支撑线：存在 $m$ 使 $\varphi(x)\ge\varphi(x_0)+m(x-x_0)$。取 $x_0=\mathbb{E}X$，把 $x=X$ 代入后两边取期望，右端第二项期望为零，得证。

**用在哪**：B9、Cramér–Rao（D4）。

### B9 KL 散度非负

**结论**：$\mathrm{KL}(P\|Q)=\sum_xP(x)\log\frac{P(x)}{Q(x)}\ge0$。

**证明**。由 B8（$\log$ 凹）：

$$-\mathrm{KL}(P\|Q)=\sum_xP(x)\log\frac{Q(x)}{P(x)}\le\log\sum_xP(x)\frac{Q(x)}{P(x)}=\log1=0.$$

**用在哪**：[第 4 篇 §5.5](/posts/thompson-sampling/#55-定理的边界为什么要先各试一次)。

### B10 伯努利 KL 的二次近似

**结论**：$d(p,q)=\mathrm{KL}(\mathrm{Bern}(p)\|\mathrm{Bern}(q))$ 在 $p\to q$ 时满足

$$d(p,q)=\frac{(p-q)^{2}}{2q(1-q)}+O((p-q)^{3}).$$

**证明**。$d(p,q)=p\log\frac pq+(1-p)\log\frac{1-p}{1-q}$，且 $d(q,q)=0$、$\partial_p d(q,q)=0$，

$$\partial_p^{2}d(p,q)=\frac1p+\frac1{1-p}\Big|_{p=q}=\frac{1}{q(1-q)}.$$

由 Taylor 展开得二阶项 $\frac{(p-q)^{2}}{2q(1-q)}$。

**用在哪**：[第 4 篇 §5.5](/posts/thompson-sampling/#55-定理的边界为什么要先各试一次)（常数 $2$ 的来源）。
## C 期望与方差

### C1 全期望公式

**结论**：$\mathbb{E}[X]=\mathbb{E}\big[\mathbb{E}[X\mid Y]\big]$。

**证明**（离散情形）。$\mathbb{E}[X\mid Y=y]=\sum_x x\,\mathbb{P}(X=x\mid Y=y)$，于是

$$\sum_y\mathbb{E}[X\mid Y=y]\,\mathbb{P}(Y=y)=\sum_y\sum_x x\,\frac{\mathbb{P}(X=x,Y=y)}{\mathbb{P}(Y=y)}\mathbb{P}(Y=y)=\sum_x x\,\mathbb{P}(X=x)=\mathbb{E}X.$$

**用在哪**：[导论 §7.1](/posts/bandits-series-intro/#71-期望与全期望)、[概率论基础 §4.3](/posts/probability-foundations/#43-条件期望)。

### C2 和的方差

**结论**：$\mathrm{Var}\!\big(\sum_iX_i\big)=\sum_i\mathrm{Var}(X_i)+2\sum_{i<j}\mathrm{Cov}(X_i,X_j)$。

**证明**。记 $\tilde X_i=X_i-\mathbb{E}X_i$，则 $\mathrm{Var}(\sum X_i)=\mathbb{E}\big[(\sum\tilde X_i)^{2}\big]=\sum_i\mathbb{E}\tilde X_i^{2}+2\sum_{i<j}\mathbb{E}[\tilde X_i\tilde X_j]$，逐项识别即可。独立时协方差为零，故可加。

**用在哪**：[概率论基础 §5.2](/posts/probability-foundations/#52-和的方差)、$\mathrm{Var}(\bar X)=\sigma^{2}/n$。

### C3 指示函数的期望

**结论**：$\mathbb{E}\mathbf{1}\{A\}=\mathbb{P}(A)$。

**证明**。$\mathbf{1}\{A\}$ 只取 $0,1$，故 $\mathbb{E}\mathbf{1}\{A\}=1\cdot\mathbb{P}(A)+0\cdot\mathbb{P}(A^{c})$。

**用在哪**：regret 的按臂重排（E1）。

### C4 弱大数定律（Chebyshev 版）

**条件**：$X_i$ iid，$\mathbb{E}X_i=\mu$，$\mathrm{Var}(X_i)=\sigma^{2}<\infty$。**结论**：$\bar X_n\xrightarrow{\ \mathbb{P}\ }\mu$。

**证明**。由 C2 与独立性，$\mathrm{Var}(\bar X_n)=\sigma^{2}/n$。对任意 $\epsilon>0$，用 B2：

$$\mathbb{P}(|\bar X_n-\mu|\ge\epsilon)\le\frac{\sigma^{2}}{n\epsilon^{2}}\to0.$$

**用在哪**：[概率论基础 §6.1](/posts/probability-foundations/#6-极限定理)。

## D 数理统计

### D1 样本方差的无偏性

**结论**：$\mathbb{E}[S^{2}]=\sigma^{2}$，其中 $S^{2}=\frac{1}{n-1}\sum(X_i-\bar X)^{2}$。

**证明**。恒等式 $\sum(X_i-\bar X)^{2}=\sum(X_i-\mu)^{2}-n(\bar X-\mu)^{2}$。取期望：第一项 $n\sigma^{2}$，第二项 $n\cdot\frac{\sigma^{2}}{n}=\sigma^{2}$，相减得 $(n-1)\sigma^{2}$，再除 $n-1$。

**用在哪**：[数理统计基础 §2.1](/posts/statistics-foundations/#2-抽样分布)。

### D2 MSE 分解

**结论**：$\mathbb{E}[(\hat\theta-\theta)^{2}]=\mathrm{Var}(\hat\theta)+\big(\mathbb{E}\hat\theta-\theta\big)^{2}$。

**证明**。令 $b=\mathbb{E}\hat\theta-\theta$、$\tilde\theta=\hat\theta-\mathbb{E}\hat\theta$，则 $\hat\theta-\theta=\tilde\theta+b$，展开平方，交叉项期望为零。

**用在哪**：[数理统计基础 §3.1](/posts/statistics-foundations/#3-估计量)。

### D3 t 统计量服从 t 分布

**条件**：$X_i$ iid $\mathcal{N}(\mu,\sigma^{2})$。**结论**：$\dfrac{\bar X-\mu}{S/\sqrt n}\sim t_{n-1}$。

**证明**。由 Fisher 引理，$Z=\frac{\sqrt n(\bar X-\mu)}{\sigma}\sim\mathcal{N}(0,1)$、$V=\frac{(n-1)S^{2}}{\sigma^{2}}\sim\chi^{2}_{n-1}$，且两者独立。于是

$$T=\frac{Z}{\sqrt{V/(n-1)}}=\frac{\bar X-\mu}{S/\sqrt n}.$$

设 $Z\sim\mathcal N(0,1)$ 与 $V\sim\chi^{2}_{\nu}$ 独立。作代换 $z=t\sqrt{v/\nu}$，联合密度对 $v$ 积分：

$$f_T(t)=\frac{\Gamma\!\big(\frac{\nu+1}{2}\big)}{\sqrt{\nu\pi}\,\Gamma\!\big(\frac{\nu}{2}\big)}\Big(1+\frac{t^{2}}{\nu}\Big)^{-(\nu+1)/2},$$

中间只剩一个 Gamma 积分 $\int_0^{\infty}v^{\frac{\nu+1}{2}-1}e^{-v(1+t^{2}/\nu)/2}\,\mathrm dv$。$\nu\to\infty$ 时收敛到标准正态。

**用在哪**：[数理统计基础 §2.2](/posts/statistics-foundations/#22-chi2tf)。

### D4 Cramér–Rao 下界

**条件**：正则族，$\hat\theta$ 无偏。**结论**：$\mathrm{Var}(\hat\theta)\ge\dfrac{1}{n\mathcal I(\theta)}$。

**证明**。记得分函数 $S=\partial_\theta\log L(\theta)$，则 $\mathbb{E}S=0$、$\mathrm{Var}(S)=n\mathcal I(\theta)$，且由 $\mathbb{E}\hat\theta=\theta$ 对 $\theta$ 求导得 $\mathrm{Cov}(\hat\theta,S)=1$。由 Cauchy–Schwarz：

$$1=\mathrm{Cov}^{2}(\hat\theta,S)\le\mathrm{Var}(\hat\theta)\,\mathrm{Var}(S).$$

**用在哪**：[数理统计基础 §4.3](/posts/statistics-foundations/#43-cramer-rao-下界)。

### D5 Beta–Bernoulli 共轭

**结论**：$X_i\sim\mathrm{Bern}(p)$、先验 $p\sim\mathrm{Beta}(a,b)$，则后验为 $\mathrm{Beta}\big(a+\sum x_i,\ b+n-\sum x_i\big)$。

**证明**。后验 $\propto p^{\sum x_i}(1-p)^{n-\sum x_i}\cdot p^{a-1}(1-p)^{b-1}=p^{a+\sum x_i-1}(1-p)^{b+n-\sum x_i-1}$，正是 Beta 核。

**用在哪**：[数理统计基础 §7.2](/posts/statistics-foundations/#72-两个必须会的共轭)、Thompson Sampling。

### D6 Normal–Normal 后验

**结论**：$X_i\sim\mathcal N(\mu,\sigma^{2})$（$\sigma^{2}$ 已知）、先验 $\mu\sim\mathcal N(\mu_0,\tau^{2})$，则后验为

$$\mathcal N\!\left(\frac{\mu_0/\tau^{2}+n\bar x/\sigma^{2}}{1/\tau^{2}+n/\sigma^{2}},\ \Big(\frac{1}{\tau^{2}}+\frac{n}{\sigma^{2}}\Big)^{-1}\right).$$

**证明**。后验的对数是 $\mu$ 的二次式：

$$-\frac{(\mu-\mu_0)^{2}}{2\tau^{2}}-\frac{\sum(x_i-\mu)^{2}}{2\sigma^{2}}=-\frac{\mu^{2}}{2}\Big(\frac{1}{\tau^{2}}+\frac{n}{\sigma^{2}}\Big)+\mu\Big(\frac{\mu_0}{\tau^{2}}+\frac{n\bar x}{\sigma^{2}}\Big)+\text{常数},$$

配方即得后验均值与方差。

**用在哪**：[数理统计基础 §7.2](/posts/statistics-foundations/#72-两个必须会的共轭)、TS 的 Gaussian 更新。

### D7 Neyman–Pearson 引理

**条件**：简单对简单，$H_0:f_0$ 对 $H_1:f_1$。**结论**：拒绝域 $\{f_1>k f_0\}$（边界随机化）在水平 $\alpha$ 下功效最大。

**证明**。设 $\varphi^{*}$ 为上述检验，$\varphi$ 为任一水平 $\le\alpha$ 的检验。则

$$\mathbb{E}_1[\varphi]-\mathbb{E}_1[\varphi^{*}]=\int(\varphi-\varphi^{*})(f_1-kf_0)\,\mathrm dx+k\int(\varphi-\varphi^{*})f_0\,\mathrm dx.$$

第二项 $\le k(\alpha-\alpha)=0$。第一项中，$f_1>kf_0$ 时 $\varphi^{*}=1\ge\varphi$，$f_1<kf_0$ 时 $\varphi^{*}=0\le\varphi$，两种情形的被积函数都 $\le0$。故差值 $\le0$。

**用在哪**：[数理统计基础 §6.5](/posts/statistics-foundations/#65-neymanpearson-引理)。

### D8 Wald 区间在边界处退化

**结论**：$\hat p=0$ 时 Wald 区间为 $\{0\}$，对任何 $p>0$ 覆盖率都是 $0$。

**证明**。区间半宽 $z\sqrt{\hat p(1-\hat p)/n}=0$，故区间退化为 $[0,0]$。而 $\mathbb{P}(p\in[0,0])=0$。

**用在哪**：[数理统计基础 §5.3](/posts/statistics-foundations/#53-比例的区间wald-的失败)。

## E 序贯决策

### E1 regret 等于「间隙 × 拉动次数」

**结论**：$R_n=\sum_{t=1}^{n}\Delta_{A_t}=\sum_{i}\Delta_i\,T_i(n)$。

**证明**。用指示函数重排（C3）：

$$\sum_t\Delta_{A_t}=\sum_t\sum_i\Delta_i\mathbf 1\{A_t=i\}=\sum_i\Delta_i\sum_t\mathbf 1\{A_t=i\}=\sum_i\Delta_iT_i(n).$$

**用在哪**：[第 2 篇 §4.1](/posts/multi-armed-bandits-intro/#4-regret把亏了多少写成公式)。

### E2 ETC 的 regret 界

**条件**：$k$ 臂，每臂探索 $m$ 次后锁定。**结论**：

$$R_n\le m\sum_i\Delta_i+(n-mk)\sum_i\Delta_i\,e^{-m\Delta_i^{2}/2}.$$

**证明**。探索期贡献 $m\sum\Delta_i$。承诺期若锁定到次优臂 $i$，说明 $\hat\mu_i\ge\hat\mu_*$；这要求 $\hat\mu_i\ge\mu_i+\Delta_i/2$ 或 $\hat\mu_*\le\mu_*-\Delta_i/2$ 至少一个发生，各自由 Hoeffding（$[0,1]$，$m$ 个样本）给出 $\le e^{-m\Delta_i^{2}/2}$。

> **补：为什么讲义的常数是 4 而不是 2**
> 第 3 篇写的是 $e^{-m\Delta_i^{2}/4}$。差别来自对「两个样本均值之差」用哪一种尾界：直接对差用 Hoeffding 会多出一个因子 $2$ 在指数上。两种写法给出同一个 $m^{*}=\Theta(\log n/\Delta^{2})$，常数不同但阶相同。

**用在哪**：[第 3 篇 §2](/posts/from-etc-to-ucb/#2-etc-的-regret-分析)。

### E3 ETC 的最优探索量

**结论**：单间隙情形下 $m^{*}\approx\dfrac{2}{\Delta^{2}}\ln\dfrac{n\Delta^{2}}{2}$，即 $\Theta(\log n/\Delta^{2})$。

**证明**。把 E2 的界看成 $m$ 的函数 $g(m)=m\Delta+n\Delta e^{-m\Delta^{2}/2}$，令

$$g'(m)=\Delta-n\Delta\frac{\Delta^{2}}{2}e^{-m\Delta^{2}/2}=0\ \Longrightarrow\ e^{-m\Delta^{2}/2}=\frac{2}{n\Delta^{2}},$$

解出 $m^{*}$。$g''>0$，故是最小值。

**用在哪**：[第 3 篇 §2.5](/posts/from-etc-to-ucb/#25-最优的-m两害相权)。

### E4 UCB 的停止判据

**条件**：奖励在 $[0,1]$，$\delta=1/n^{2}$，bonus $c_i(t)=\sqrt{2\log(1/\delta)/T_i(t)}$。**结论**：以高概率 $T_i(n)\le\dfrac{16\log n}{\Delta_i^{2}}+2$。

**证明**。定义好事件 $E=\{\forall i,t:|\hat\mu_i(t)-\mu_i|\le c_i(t)\}$。由 Hoeffding 与 union bound，$\mathbb{P}(E^{c})\le2nk\delta=2k/n$。

在 $E$ 上，若第 $t$ 轮选了次优臂 $i$，则

$$\hat\mu_i+c_i\ge\hat\mu_*+c_*\ge\mu_*,$$

而 $\hat\mu_i\le\mu_i+c_i$，故 $\mu_i+2c_i\ge\mu_*$，即 $\Delta_i\le2c_i$。两边平方并解出 $T_i$：

$$T_i\le\frac{8\log(1/\delta)}{\Delta_i^{2}}=\frac{16\log n}{\Delta_i^{2}}.$$

**用在哪**：[第 3 篇 §4.3](/posts/from-etc-to-ucb/#43-定量tiδi216logn)。

### E5 UCB 的 regret 界

**结论**：$R_n\le16\log n\sum_{i:\Delta_i>0}\dfrac{1}{\Delta_i}+O(1)$。

**证明**。由 E1 与 E4：

$$R_n=\sum_i\Delta_iT_i(n)\le\sum_i\Delta_i\cdot\frac{16\log n}{\Delta_i^{2}}=16\log n\sum_i\frac{1}{\Delta_i}.$$

（$T_i\le n$ 给了 $O(1)$ 的截断项。）

**用在哪**：[第 3 篇 §5](/posts/from-etc-to-ucb/#5-ucb-的-regret-定理)。

### E6 Thompson Sampling 的界（只陈述）

**结论**：对伯努利或高斯奖励，$\mathbb{E}[R_n]\le\sum_i\dfrac{2\log n}{\Delta_i}+O(1)$，与 Lai–Robbins 下界同阶。

**为什么不在这里证**：完整证明需要「变化测度 + 后验集中」两套工具（对每个次优臂构造一个与真实分布 KL 距离有限的替代分布，再用后验以指数速度集中到真实参数的结论）。第 4 篇 §5.5 用 KL 解释了常数 $2$ 的来历，但没有展开这两步。

**用在哪**：[第 4 篇 §5.1](/posts/thompson-sampling/#51-定理)。

## F 没有在这里证明的

| 结论 | 为什么跳过 |
|---|---|
| 中心极限定理 | 需要特征函数与 Lévy 连续性定理；证明长度超出附录一节的篇幅 |
| Berry–Esseen 定理 | 需要更细的展开与 $\mathbb{E}\lvert X\rvert^{3}$ 条件 |
| Neyman–Pearson 的复合假设推广（Karlin–Rubin） | 需要单调似然比族的构造 |
| Lai–Robbins 下界 | 需要变化测度（change of measure）与大偏差原理 |
| Azuma / 鞅版 Hoeffding | 需要鞅差序列与停时 |
| 回归与 GLM 的渐近正态 | 需要矩阵值版本的 CLT 与更重的正则条件 |

**这些跳过的结论在正文里都只作为「事实」使用**，不参与任何一步推导；用到时会在那一节标注「引用，不证」。

---

## 怎么给这个附录补一条

1. 正文里先写结论与「用在哪」，把证明留空并链接到这里；
2. 这里按 A–E 的字母段加一条，编号顺延；
3. 四段齐全：条件 / 结论 / 证明 / 用在哪——**缺一段就不要收进来**；
4. 如果证明里用到了别的结论，写编号（比如「由 B3」「由 C2」），让依赖链可查；
5. 加完检查：这条编号有没有被别的条目引用、链接的锚点是否还活着。
