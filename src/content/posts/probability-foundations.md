---
title: 概率论基础：从公理到中心极限定理
description: 概率空间、条件概率与贝叶斯、随机变量与常见分布、期望与方差、大数定律与中心极限定理——把 bandits 里随手用的每条性质补上出处。
date: 2026-11-02
tags: ["概率论", "数学基础", "贝叶斯"]
draft: false
featured: false
lang: zh-CN
---

> **材料来源**：DeGroot & Schervish, *Probability and Statistics*, 4th ed. 的第 1–6 章（概率、条件概率、随机变量、期望、特殊分布、大样本）。这里只保留后面几篇真正会用到的部分，页码索引在该书目录：概率公理在 Ch.1，条件概率与贝叶斯在 Ch.2，随机变量与分布族在 Ch.3 与 Ch.5，期望与方差在 Ch.4，大数定律与 CLT 在 Ch.6。
> **和上一篇的关系**：数学工具箱给了不等式，这一篇给「不等式作用在什么对象上」。读完这一篇，第 1 篇的四格表和第 4 篇的贝叶斯更新都不会再有符号障碍。
> **符号约定**：与数学工具箱一致；$\mathbb{P}$ 表示概率，$f$ 表示密度，$F$ 表示分布函数，$\Phi$ 表示标准正态分布函数。
> **系列位置**：前置 1 · 概率论。上一篇是 [数学工具箱](/posts/math-toolbox/)，下一篇是 [数理统计基础](/posts/statistics-foundations/)。

---

## 0. 这一章的位置

第 1 篇开头有一张四格表：判对、判错、漏报、误报。它看起来像统计，其实是概率——**把「已知 $\theta$ 时数据的分布」和「看到数据后 $\theta$ 的分布」分开**。这两件事一个是 $P(x\mid\theta)$，一个是 $P(\theta\mid x)$，差别只在一个贝叶斯公式。

第 2 篇到最后都在用期望：$\mathbb{E}[R_n]=\sum_t\Delta_{A_t}$。为什么可以逐项拆？因为期望是线性的，**不需要独立**。

这一章就是把这些「其实一直在用」的东西按顺序铺开。已经熟的可以直接跳到第 7 节的接口表。

## 1. 概率空间

### 1.1 样本空间与事件

一次试验的所有可能结果构成**样本空间** $\Omega$。**事件**是 $\Omega$ 的子集，记作 $A,B,\dots$。

三个基本运算：

- 并 $A\cup B$：至少一个发生；
- 交 $A\cap B$：同时发生；
- 补 $A^{c}$：不发生。

DeMorgan 律把并、交、补串起来：

$$(A\cup B)^{c}=A^{c}\cap B^{c},\qquad (A\cap B)^{c}=A^{c}\cup B^{c}.$$

### 1.2 三条公理

概率是从事件到 $[0,1]$ 的映射，满足

1. **非负性**：$\mathbb{P}(A)\ge 0$；
2. **规范性**：$\mathbb{P}(\Omega)=1$；
3. **可列可加性**：若 $A_1,A_2,\dots$ 两两不相交，则 $\mathbb{P}(\bigcup_i A_i)=\sum_i\mathbb{P}(A_i)$。

三条公理推出来的东西才是平时真正用的：

$$\mathbb{P}(A^{c})=1-\mathbb{P}(A),\qquad \mathbb{P}(\varnothing)=0,$$

$$\mathbb{P}(A\cup B)=\mathbb{P}(A)+\mathbb{P}(B)-\mathbb{P}(A\cap B).$$

最后一条是容斥原理的两事件版。它推广到 $n$ 个事件时是一串加减（DeGroot Ch.1.10），**但实际计算时更常用的是 union bound**——容斥精确但项数爆炸，union bound 松但只有一行。

> **补：为什么「$\mathbb{P}(A)=0$」不等于「$A$ 不可能」**
> 连续分布下 $\mathbb{P}(X=x)=0$ 对每个点都成立，但 $X$ 总要取某个值。这意味着**概率为零与不可能不是一回事**。这条在讨论「p 值恰好等于 0.05」或者「事件恰好在边界」时会咬人。

### 1.3 计数与古典概型

当 $\Omega$ 有限且每个结果等可能时，

$$\mathbb{P}(A)=\frac{|A|}{|\Omega|}.$$

于是概率问题变成计数问题。三个常用的计数结果：

- 排列：$n!$；
- 从 $n$ 个里选 $k$ 个：$\binom{n}{k}=\frac{n!}{k!(n-k)!}$；
- 多项系数：$\frac{n!}{n_1!\cdots n_k!}$。

计数题的难点从来不是公式，而是**「样本空间到底等不等可能」**。把两个球当成可区分还是不可区分，会直接改变答案。

## 2. 条件概率

### 2.1 定义与乘法公式

当 $\mathbb{P}(B)>0$ 时，

$$\mathbb{P}(A\mid B)=\frac{\mathbb{P}(A\cap B)}{\mathbb{P}(B)}.$$

移项就是乘法公式：

$$\mathbb{P}(A\cap B)=\mathbb{P}(A\mid B)\,\mathbb{P}(B)=\mathbb{P}(B\mid A)\,\mathbb{P}(A).$$

**条件概率是一次「换样本空间」**：把 $\Omega$ 缩到 $B$ 上，再重新归一化。后面第 4 篇的贝叶斯更新，本质就是连续地做这件事。

### 2.2 全概率公式

若 $B_1,\dots,B_k$ 是 $\Omega$ 的一个划分（互不相交、并起来是全集），则

$$\mathbb{P}(A)=\sum_{i=1}^{k}\mathbb{P}(A\mid B_i)\,\mathbb{P}(B_i).$$

**直觉**：把「$A$ 发生」按「是哪种情形下发生的」拆成若干块，每块用乘法公式，再全部加起来。这是贝叶斯公式的分母。

### 2.3 贝叶斯定理

把乘法公式的两种写法相等，就得到

$$\mathbb{P}(B_i\mid A)=\frac{\mathbb{P}(A\mid B_i)\,\mathbb{P}(B_i)}{\sum_j \mathbb{P}(A\mid B_j)\,\mathbb{P}(B_j)}.$$

分子是「这一种情形下看到 $A$ 的联合概率」，分母是「看到 $A$ 的总概率」。

**经典陷阱：基础率**。设某病患病率 $0.1\%$，检测灵敏度 $99\%$、特异度 $99\%$。阳性时真患病的概率是

$$\mathbb{P}(\text{病}\mid+)=\frac{0.99\times 0.001}{0.99\times0.001+0.01\times0.999}\approx 9\%.$$

大多数人的直觉是「99%」，差了一个数量级。**错在把 $\mathbb{P}(+\mid\text{病})$ 当成了 $\mathbb{P}(\text{病}\mid+)$**。这两个数之间隔着基础率和检测的错误率。

> **补：这条式子在第 1 篇里长什么样**
> 第 1 篇的 MAP 规则写的是「后验最大」，把后验展开就是上面这条式子：先验 $\mathbb{P}(\theta)$ 乘似然 $\mathbb{P}(x\mid\theta)$，分母与 $\theta$ 无关所以可以不写。所谓 MAP 与 ML 的差别，就是**要不要乘那个先验**。

### 2.4 独立性

两个事件独立，当且仅当

$$\mathbb{P}(A\cap B)=\mathbb{P}(A)\,\mathbb{P}(B).$$

等价地（当 $\mathbb{P}(B)>0$）：$\mathbb{P}(A\mid B)=\mathbb{P}(A)$——**知道 $B$ 发生，对 $A$ 的判断没有改变**。

$n$ 个事件**相互独立**要求任意子集的交都等于概率的乘积；**两两独立**只要求任意两个。两者不等价：

> **反例**：掷两次硬币，$A=\{$第一次正面$\}$，$B=\{$第二次正面$\}$，$C=\{$两次相同$\}$。两两独立，但 $\mathbb{P}(A\cap B\cap C)=0\neq\frac18$。

**条件独立**是另一回事：给定 $C$ 后 $A$ 与 $B$ 独立，写作 $A\perp B\mid C$。第 1 篇的朴素贝叶斯、第 4 篇的共轭更新，都默认了某种条件独立。**条件独立既不等价于独立，也不能由独立推出**。

## 3. 随机变量

### 3.1 离散与连续

**随机变量**是从 $\Omega$ 到 $\mathbb{R}$ 的可测函数。它把「事件」翻译成「数」，之后才能谈期望、方差、极限。

- **离散型**：取值至多可列，用概率质量函数 $p(x)=\mathbb{P}(X=x)$ 描述，$\sum_x p(x)=1$；
- **连续型**：存在密度 $f\ge 0$，使 $\mathbb{P}(X\in B)=\int_B f(x)\,\mathrm{d}x$，$\int f=1$。

### 3.2 分布函数与密度

**分布函数**定义为

$$F(x)=\mathbb{P}(X\le x).$$

它有三个性质：单调不减、右连续、$\lim_{x\to-\infty}F=0$、$\lim_{x\to+\infty}F=1$。

连续型时 $F(x)=\int_{-\infty}^{x}f(t)\,\mathrm{d}t$，且 $f=F'$（在连续点）。

两条容易记错的：

- $f(x)$ 可以大于 1（区间很窄时），**只有积分才必须是 1**；
- $\mathbb{P}(a<X\le b)=F(b)-F(a)$，端点不影响连续型的概率。

### 3.3 常见分布

| 分布 | 参数 | 概率/密度 | 均值 | 方差 | 在后文出现的地方 |
|---|---|---|---|---|---|
| Bernoulli | $p$ | $p^{x}(1-p)^{1-x}$ | $p$ | $p(1-p)$ | 广告点击、单臂奖励 |
| Binomial | $n,p$ | $\binom{n}{x}p^{x}(1-p)^{n-x}$ | $np$ | $np(1-p)$ | 累计点击数 |
| Poisson | $\lambda$ | $e^{-\lambda}\lambda^{x}/x!$ | $\lambda$ | $\lambda$ | 稀有事件计数 |
| Geometric | $p$ | $(1-p)^{x-1}p$ | $1/p$ | $(1-p)/p^{2}$ | 首次成功 |
| Uniform | $a,b$ | $1/(b-a)$ | $(a+b)/2$ | $(b-a)^{2}/12$ | 先验、随机化 |
| Normal | $\mu,\sigma^{2}$ | $\frac{1}{\sqrt{2\pi}\sigma}e^{-(x-\mu)^{2}/2\sigma^{2}}$ | $\mu$ | $\sigma^{2}$ | CLT、Gaussian 后验 |
| Exponential | $\lambda$ | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^{2}$ | 等待时间 |
| Gamma | $\alpha,\beta$ | $\frac{\beta^{\alpha}}{\Gamma(\alpha)}x^{\alpha-1}e^{-\beta x}$ | $\alpha/\beta$ | $\alpha/\beta^{2}$ | 精度参数的先验 |
| Beta | $a,b$ | $\frac{x^{a-1}(1-x)^{b-1}}{B(a,b)}$ | $\frac{a}{a+b}$ | $\frac{ab}{(a+b)^{2}(a+b+1)}$ | TS 的伯努利后验 |

第 4 篇里用的两个更新，就是这张表的直接应用：伯努利 + Beta 先验 → Beta 后验；正态 + 正态先验 → 正态后验。

### 3.4 随机变量的函数

已知 $X$ 的分布，求 $Y=g(X)$ 的分布，有两种办法。

**离散**：$\mathbb{P}(Y=y)=\sum_{x:g(x)=y}\mathbb{P}(X=x)$。

**连续、$g$ 单调可导**：用变换公式

$$f_Y(y)=f_X\big(g^{-1}(y)\big)\left|\frac{\mathrm{d}}{\mathrm{d}y}g^{-1}(y)\right|.$$

**不单调**时要把每一支加起来。

很多情况下根本不需要密度，只需要期望——这时用 **LOTUS**（无意识统计学家法则）：

$$\mathbb{E}[g(X)]=\sum_x g(x)p(x)\quad\text{或}\quad\int g(x)f(x)\,\mathrm{d}x.$$

**注意**：$\mathbb{E}[g(X)]=g(\mathbb{E}X)$ 一般不成立（那是 Jensen 取等号的情形，只有 $g$ 线性时才对）。

## 4. 期望

### 4.1 定义

$$\mathbb{E}[X]=\sum_x x\,p(x)\quad\text{或}\quad\int x\,f(x)\,\mathrm{d}x.$$

它要求绝对可积（$\mathbb{E}|X|<\infty$），否则期望不存在——柯西分布是标准反例。

### 4.2 线性性

对任意常数 $a,b$ 和任意随机变量（**不需要独立**）：

$$\mathbb{E}[aX+bY]=a\,\mathbb{E}[X]+b\,\mathbb{E}[Y].$$

这是全站用得最多的一条。第 2 篇把 $R_n=\sum_t\Delta_{A_t}$ 拆成逐轮之和、第 3 篇把「每个臂的拉动次数」求和、第 4 篇把 regret 按臂分解，全靠它。

**乘法就不是这样了**：$\mathbb{E}[XY]=\mathbb{E}X\,\mathbb{E}Y$ 需要独立（或至少不相关），不能随口用。

### 4.3 条件期望

给定 $Y$ 时 $X$ 的条件期望记作 $\mathbb{E}[X\mid Y]$，它是一个**关于 $Y$ 的函数**（随机变量），不是常数。

两个性质：

$$\mathbb{E}\big[\mathbb{E}[X\mid Y]\big]=\mathbb{E}[X]\qquad\text{（全期望公式）},$$

$$\mathbb{E}[X\mid Y]=\mathbb{E}[X]\quad\text{若 }X\perp Y.$$

全期望公式的意思是「先按 $Y$ 分层算，再对层做加权平均」。第 3 篇里的「按轮次分层」、TS 里的「按后验分层」都是这个动作。

### 4.4 指示函数

$$\mathbf{1}\{A\}=\begin{cases}1,& A\text{ 发生},\\ 0,& \text{否则}.\end{cases}$$

它的期望就是概率：

$$\mathbb{E}[\mathbf{1}\{A\}]=\mathbb{P}(A).$$

**这是把「计数」变成「求和」的桥**：事件发生的次数 $N=\sum_{i}\mathbf{1}\{A_i\}$，于是

$$\mathbb{E}[N]=\sum_i\mathbb{P}(A_i).$$

第 2 篇的 4.4 节之所以能把「错误次数」写成 $\sum_t\mathbf{1}\{A_t\neq A^{*}\}$，就是因为这一条。

## 5. 方差与协方差

### 5.1 定义

$$\mathrm{Var}(X)=\mathbb{E}\big[(X-\mathbb{E}X)^{2}\big]=\mathbb{E}[X^{2}]-(\mathbb{E}X)^{2}.$$

第二个等号是计算时真正用的那个。性质：

$$\mathrm{Var}(aX+b)=a^{2}\,\mathrm{Var}(X),\qquad \mathrm{Var}(X)\ge 0.$$

标准差 $\sigma_X=\sqrt{\mathrm{Var}(X)}$ 与 $X$ 同量纲。

### 5.2 和的方差

$$\mathrm{Var}\!\left(\sum_{i=1}^{n}X_i\right)=\sum_{i=1}^{n}\mathrm{Var}(X_i)+2\sum_{i<j}\mathrm{Cov}(X_i,X_j).$$

**独立时协方差项全为零**，方差可加。这就是为什么第 1 篇里 $n$ 个样本的均值方差是 $\sigma^{2}/n$：

$$\mathrm{Var}(\bar X)=\frac{\sigma^{2}}{n}.$$

### 5.3 协方差与相关系数

$$\mathrm{Cov}(X,Y)=\mathbb{E}[(X-\mathbb{E}X)(Y-\mathbb{E}Y)]=\mathbb{E}[XY]-\mathbb{E}X\,\mathbb{E}Y,$$

$$\rho=\frac{\mathrm{Cov}(X,Y)}{\sigma_X\sigma_Y}\in[-1,1].$$

**独立 $\Rightarrow$ 不相关，反之不成立**。反例：$X\sim U(-1,1)$，$Y=X^{2}$，$\mathrm{Cov}(X,Y)=0$ 但两者明显依赖。相关系数只捕捉线性关系。

## 6. 极限定理

### 6.1 大数定律

设 $X_1,\dots,X_n$ iid 且 $\mathbb{E}|X_1|<\infty$，则

$$\bar X_n=\frac1n\sum_{i=1}^{n}X_i\ \xrightarrow{\ \mathbb{P}\ }\ \mu=\mathbb{E}[X_1].$$

这是**弱**大数定律（依概率收敛）。强版本给出几乎必然收敛，条件相同或更松。

证明弱版本只需要 Chebyshev：

$$\mathbb{P}(|\bar X_n-\mu|\ge\epsilon)\le\frac{\mathrm{Var}(\bar X_n)}{\epsilon^{2}}=\frac{\sigma^{2}}{n\epsilon^{2}}\to 0.$$

**但 Chebyshev 只给出 $1/n$ 的速率，而且要求方差有限。** 想要指数速率就得换 Hoeffding（数学工具箱 5.3）。

这就是为什么 UCB 里的界要写 $\exp(-2T\Delta^{2})$ 而不是 $1/T$——**指数衰减让 union bound 之后仍然收敛**。

### 6.2 两种收敛的差别

| 收敛方式 | 记号 | 含义 |
|---|---|---|
| 依概率 | $X_n\xrightarrow{\mathbb{P}}X$ | 对任意 $\epsilon$，$\mathbb{P}(|X_n-X|>\epsilon)\to0$ |
| 几乎必然 | $X_n\xrightarrow{\text{a.s.}}X$ | $\mathbb{P}(\lim_n X_n=X)=1$ |

几乎必然更强。两者都不保证 $\mathbb{E}[X_n]\to\mathbb{E}[X]$（需要一致可积性）。

### 6.3 中心极限定理

设 $X_i$ iid，$\mathbb{E}X_i=\mu$，$\mathrm{Var}(X_i)=\sigma^{2}\in(0,\infty)$，则

$$\frac{\sqrt{n}(\bar X_n-\mu)}{\sigma}\ \xrightarrow{\ d\ }\ \mathcal{N}(0,1).$$

等价地，$\bar X_n$ **近似**服从 $\mathcal{N}(\mu,\sigma^{2}/n)$。

**CLT 与 LLN 的分工**：LLN 说「$\bar X_n$ 会靠近 $\mu$」，CLT 说「靠近的方式是抖动的，抖动幅度是 $\sigma/\sqrt n$，形状是正态」。置信区间的宽度来自后者。

### 6.4 用 CLT 做近似

$$\mathbb{P}\!\left(\bar X_n\in\left[\mu-z_{1-\alpha/2}\frac{\sigma}{\sqrt n},\ \mu+z_{1-\alpha/2}\frac{\sigma}{\sqrt n}\right]\right)\approx 1-\alpha,$$

其中 $z_{0.975}\approx1.96$。这正是第 1 篇里那些「$\pm1.96\sigma/\sqrt n$」的来源。

三个使用条件：

1. **独立**（或弱相关）；
2. **方差有限**；
3. $n$ 足够大——但「多大算够」取决于分布的偏度。严重偏态时要 $n$ 上千甚至上万，Berry–Esseen 定理给出的是 $O(1/\sqrt n)$ 的误差界。

> **补：CLT 不告诉你尾有多厚**
> CLT 是中心附近的结果。$n=30$ 时中间已经很像正态，但尾部可能还差很远。这也是为什么「用正态近似算极端分位数」经常出错——第 1 篇里用 Hoeffding 做区间，就是不想依赖渐近。

## 7. 与后文的接口

| 这一章的概念 | 出现在哪 | 用来干什么 |
|---|---|---|
| 条件概率、贝叶斯 | 第 1 篇 §2、第 4 篇 §3 | 从 $P(x\mid\theta)$ 得到 $P(\theta\mid x)$ |
| 独立性 | 第 3 篇 §3.2、第 1 篇 §3.6 | 让 union bound 与合并方差成立 |
| 期望线性性 | 第 2 篇 §4、第 3 篇 §5 | 把 regret 拆成逐轮之和 |
| 指示函数 | 第 2 篇 §4.4 | 把「错误次数」写成随机变量之和 |
| 方差 | 第 1 篇 §3.6、第 3 篇 §4 | 置信区间的宽度 |
| 大数定律 | 第 2 篇 §5.1 | 「样本多了经验均值会准」的前提 |
| 中心极限定理 | 第 1 篇 §3.6、第 4 篇 §4.4 | $\pm1.96\sigma/\sqrt n$、Gaussian 更新 |
| Beta / 正态分布 | 第 4 篇 §4.4 | 共轭更新的具体形式 |

## 8. 六个容易错的地方

1. **把 $\mathbb{P}(A\mid B)$ 与 $\mathbb{P}(B\mid A)$ 混用**：这是医学检测、p 值、贝叶斯更新里最常见的错误。
2. **以为独立就是「没有关系」**：独立是概率意义，不是因果意义；不相关也不等于独立。
3. **以为 $f(x)$ 是概率**：连续分布里 $f(x)$ 可以大于 1，只有积分有意义。
4. **把 $\mathbb{E}[g(X)]$ 写成 $g(\mathbb{E}X)$**：除线性以外都不成立。
5. **把 CLT 用在极端尾部**：中心极限说的是中心，不是尾部。
6. **忽略方差是否有限**：柯西分布没有期望，LLN 与 CLT 都失效。

---

**下一篇**：[数理统计基础](/posts/statistics-foundations/) —— 把「分布」变成「从数据推断参数」。
