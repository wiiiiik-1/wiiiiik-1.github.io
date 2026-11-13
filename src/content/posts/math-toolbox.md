---
title: 数学工具箱：写概率推导之前该备好的六件事
description: 求和、对数不等式、渐进记号、五个概率不等式、Stirling 公式与 KL 散度——后面每一篇推导里反复出现的工具，一次备齐。
date: 2026-11-01
tags: ["数学基础", "概率论", "不等式", "KL 散度"]
draft: false
featured: false
lang: zh-CN
---

> **材料来源**：这一章不是某一节课的笔记，而是把前面几篇里「用到了但没解释」的工具集中补齐。求和与阶数来自 [第 3 篇](/posts/from-etc-to-ucb/) 的 ETC 分析，不等式来自第 1 篇的置信区间与第 3 篇的 UCB，KL 来自第 4 篇的下界讨论。
> **和上一篇的关系**：这是整个系列的前置 0，读 bandits 之前看这一篇就够，不需要先读别的。
> **符号约定**：$\log$ 一律指自然对数；$[n]=\{1,\dots,n\}$；$\mathbb{E}$ 与 $\mathrm{Var}$ 写作 $\mathbb{E}[X]$、$\mathrm{Var}(X)$；iid 表示独立同分布。
> **系列位置**：前置 0 · 数学工具。下一篇是 [概率论基础](/posts/probability-foundations/)。

---

## 0. 为什么单独开一章

前面三篇里出现过这样一些句子：

- 「把 $(1-\Delta^2/4)^m$ 换成 $e^{-m\Delta^2/4}$」——这是对数不等式；
- 「所以每个臂最多被拉 $16\log n/\Delta_i^2$ 次」——这是 Hoeffding 加 union bound；
- 「固定 $m$ 的 ETC 是 $O(n^{2/3})$」——这是渐进记号；
- 「下界是 $\log n/\mathrm{KL}$，不是 $\log n/\Delta^2$」——这是 KL 散度。

每一句当时都只用了一行，但那一行背后是一个完整的工具。这一章把这些工具按「什么时候会用到」重新排一遍，**不追求证明的完整，只追求用的时候不心虚**。

如果只想看结论，直接跳到第 8 节的速查表。

## 1. 记号

先把记号钉死，后面不再重复。

| 记号 | 含义 |
|---|---|
| $X, Y$ | 随机变量 |
| $\mathbb{P}(A)$ | 事件 $A$ 的概率 |
| $\mathbb{E}[X]$ | 期望 |
| $\mathrm{Var}(X)$ | 方差，$\mathbb{E}[(X-\mathbb{E}X)^2]$ |
| $X_1,\dots,X_n\overset{\text{iid}}{\sim}P$ | 独立同分布 |
| $\hat\mu_n=\frac1n\sum_t X_t$ | 样本均值（经验均值） |
| $\mathbf{1}\{A\}$ | 指示函数：$A$ 发生为 1，否则为 0 |
| $\sum_{t=1}^n a_t$ | 求和，$t$ 是哑变量 |

有两条约定容易被忽略，但后面一直用：

1. **期望是线性的，方差不是。** $\mathbb{E}[X+Y]=\mathbb{E}X+\mathbb{E}Y$ 永远成立；$\mathrm{Var}(X+Y)=\mathrm{Var}X+\mathrm{Var}Y$ 只在**不相关**时成立。
2. **$O(\cdot)$ 里的常数不告诉你。** 看到 $O(\log n)$ 只能知道「增长得和 $\log n$ 一样快」，不能知道「比 $n$ 小多少」。

## 2. 求和与级数

### 2.1 三个恒等式

$$\sum_{t=1}^{n} c = nc, \qquad \sum_{t=1}^{n} t = \frac{n(n+1)}{2}, \qquad \sum_{t=0}^{n} r^{t}=\frac{1-r^{n+1}}{1-r}\ (r\neq 1).$$

前两个是等差，第三个是等比。等比级数在 $|r|<1$ 时取极限：

$$\sum_{t=0}^{\infty} r^{t}=\frac{1}{1-r}.$$

这三条覆盖了后面 90% 的求和。剩下 10% 是下面这条。

### 2.2 调和数：$\log n$ 到底从哪来

调和数定义为

$$H_n=\sum_{t=1}^{n}\frac{1}{t}=\ln n+\gamma+O\!\left(\frac1n\right),\qquad \gamma\approx 0.5772\ (\text{Euler–Mascheroni}).$$

这个式子是本系列里 $\log n$ 的唯一来源。推导只用「面积夹逼」：函数 $1/x$ 递减，所以

$$\int_{1}^{n+1}\frac{\mathrm{d}x}{x}\ \le\ \sum_{t=1}^{n}\frac{1}{t}\ \le\ 1+\int_{1}^{n}\frac{\mathrm{d}x}{x}.$$

左边是 $\ln(n+1)$，右边是 $1+\ln n$，两边只差一个常数——所以 $H_n=\ln n+O(1)$。

![把 1/t 和曲线下面积放在一起：红区面积是 ln n，蓝区是常数](/images/bandit-figures/one-over-t.png)

*看图要点*：红线下方的面积就是 $\sum 1/t$ 的连续版本，等于 $\ln n$；蓝区是「每轮错误率恒为常数」时的累计，是线性的。**两个面积一对比，就知道为什么 ETC 只能拿线性、而 $1/t$ 的错误率能拿 $\log n$。**

### 2.3 为什么 bandit 里到处都是 $\log n$

因为「第 $t$ 轮还犯错的概率」一旦是 $1/t$ 这种量级，累计错误次数就是

$$\sum_{t=1}^{n}\mathbb{P}(\text{第 }t\text{ 轮选错})\approx \sum_{t=1}^{n}\frac{1}{t}=H_n\approx\ln n.$$

**累计的阶由单轮速率决定**：$1/t$ 给出 $\ln n$，$1/\sqrt t$ 给出 $2\sqrt n$，常数给出 $n$。这也是为什么第 2 篇 4.4 节要专门问一句「$1/t$ 是哪来的」。

### 2.4 交换求和顺序

后面推 regret 界时要按臂重排：

$$\sum_{t=1}^{n}\sum_{i=1}^{k} a_{t,i}=\sum_{i=1}^{k}\sum_{t=1}^{n} a_{t,i}.$$

只要 $a_{t,i}\ge 0$（或者有限项），交换就是合法的。**regret 的每一项都是非负的**，所以这一步在 bandit 的证明里从来不需要额外条件。

## 3. 对数与指数：三个反复用的不等式

### 3.1 $\log(1+x)\le x$

对所有 $x>-1$ 成立。证明：令 $f(x)=x-\log(1+x)$，则 $f(0)=0$，$f'(x)=\frac{x}{1+x}$，在 $x>0$ 时为正、$x<0$ 时为负，所以 $0$ 是最小值。

这一条是所有「连乘变指数」的源头。

### 3.2 $1-x\le e^{-x}$

把 3.1 里的 $x$ 换成 $-u$（$u<1$）就得到 $\log(1-u)\le -u$，两边取指数：

$$1-u\ \le\ e^{-u}.$$

### 3.3 连乘变指数（第 3 篇最常用的一次）

把 $u=\Delta^2/4$ 代入 3.2：

$$1-\frac{\Delta^2}{4}\le e^{-\Delta^2/4}\quad\Longrightarrow\quad\left(1-\frac{\Delta^2}{4}\right)^{m}\le e^{-m\Delta^2/4}.$$

这就是 ETC 的界里那个指数项的来源。换成 $u=\Delta^2/2$ 就得到 UCB 与 TS 里更常见的 $e^{-m\Delta^2/2}$。

### 3.4 $(1-1/n)^n\le e^{-1}$

3.3 取 $u=1/n$。左边收敛到 $1/e\approx 0.3679$，永远从下方逼近。这个式子解释了「为什么 $\delta=1/n^2$ 里的指数正好是 2」——见第 3 篇 3.3 节。

### 3.5 尺度的感觉

$\ln n$ 增长得慢到违反直觉：

| $n$ | $10^3$ | $10^6$ | $10^{9}$ | $10^{12}$ | $10^{18}$ |
|---|---|---|---|---|---|
| $\ln n$ | 6.9 | 13.8 | 20.7 | 27.6 | 41.4 |

$n$ 涨六个数量级，$\ln n$ 只翻一倍。第 4 篇 5.4 节算过这笔账：想让 $R_n/\ln n$ 从 13.5 爬到 27，需要 $n\sim10^{28}$。**「$\log n$ 的界很好」是渐进意义上的好，不是「$n=10^5$ 时已经很接近」的好。**

## 4. 渐进记号

### 4.1 四个记号

| 记号 | 含义 | 一句话 |
|---|---|---|
| $f=O(g)$ | 存在常数 $C$，使 $f\le Cg$（$n$ 足够大） | 增长不快于 $g$ |
| $f=\Omega(g)$ | 存在常数 $c>0$，使 $f\ge cg$ | 增长不慢于 $g$ |
| $f=\Theta(g)$ | 同时是 $O$ 与 $\Omega$ | 与 $g$ 同阶 |
| $f=o(g)$ | $f/g\to 0$ | 比 $g$ 低一阶 |

还有 $\tilde O(g)$：忽略 $\log$ 因子的 $O(g)$。说「UCB 的 regret 是 $\tilde O(\sqrt{n})$」时，意思是「$\sqrt{n}$ 乘上若干 $\log$ 的幂」。

### 4.2 三条使用规则

1. **常数被吃掉**：$16\log n$ 与 $2\log n$ 都是 $\Theta(\log n)$。所以第 4 篇里那个「16 压到 2」的改进，**在 $O$ 记号下看不出来**，它是常数的改进。
2. **$O$ 只对足够大的 $n$ 成立**：有限 $n$ 上什么都可能发生，第 3 篇第 6 节的实测就是例子（前 1000 轮 UCB 反而更亏）。
3. **等式方向是单向的**：写 $f=O(g)$ 是约定俗成的滥用，不能反推 $O(g)=f$，也不能对 $O$ 做减法。

### 4.3 三个常用的展开

$$H_n=\ln n+O(1),$$

$$\ln(n!)=n\ln n-n+O(\log n),$$

$$\binom{n}{k}\le\left(\frac{en}{k}\right)^{k}.$$

最后一条来自 Stirling（第 6 节），在数二项分布的尾部概率时反复用到。

## 5. 五个概率不等式

这一节是全章的骨干。每条按「条件 → 形式 → 什么时候用」写。

### 5.1 Markov 不等式

**条件**：$X\ge 0$。**形式**：

$$\mathbb{P}(X\ge a)\le\frac{\mathbb{E}[X]}{a}.$$

**用法**：只知道一阶矩时唯一能说的话。它是下面两条的老祖宗。

### 5.2 Chebyshev 不等式

**条件**：$\mathrm{Var}(X)<\infty$。对 $a>0$，

$$\mathbb{P}(|X-\mathbb{E}X|\ge a)\le\frac{\mathrm{Var}(X)}{a^{2}}.$$

**怎么来的**：把 Markov 用在 $(X-\mu)^2$ 上。**用法**：证明弱大数定律（见概率论基础第 6 节），以及「样本均值偏离 $\epsilon$ 的概率是 $O(1/(n\epsilon^2))$」。

注意它给出的衰减是 $1/n$，比 Hoeffding 的 $e^{-n}$ 差得多——但 Chebyshev 只要求二阶矩存在。

### 5.3 Hoeffding / Chernoff

**条件**：$X_1,\dots,X_n$ 独立，$X_i\in[a_i,b_i]$。令 $\bar X=\frac1n\sum X_i$、$\mu=\mathbb{E}\bar X$，则对任意 $\epsilon>0$，

$$\mathbb{P}(|\bar X-\mu|\ge\epsilon)\le 2\exp\!\left(-\frac{2n\epsilon^{2}}{(b-a)^{2}}\right).$$

伯努利情形（$X_i\in\{0,1\}$，$b-a=1$）最常用：

$$\mathbb{P}(|\hat\mu_n-\mu|\ge\epsilon)\le 2e^{-2n\epsilon^{2}}.$$

**用法**：UCB 的 bonus $\sqrt{2\log(1/\delta)/T}$、第 1 篇 3.6 节的置信区间、TS 的后验收缩，全是它的变形。变形方法是把右边设成 $\delta$ 再解出 $\epsilon$：

$$\epsilon=\sqrt{\frac{\log(2/\delta)}{2n}}.$$

#### 5.3.1 补：Hoeffding 的四步

上面的式子看起来像天上掉下来的。其实它只有四步，而且每一步都很朴素。

**第一步：把「和」指数化。** 对任意 $t>0$，

$$\mathbb{P}(\bar X-\mu\ge\epsilon)=\mathbb{P}\big(e^{t(\bar X-\mu)}\ge e^{t\epsilon}\big)\le e^{-t\epsilon}\,\mathbb{E}\big[e^{t(\bar X-\mu)}\big].$$

这里只用 Markov（$e^{t(\bar X-\mu)}$ 非负）。**指数化不是为了精确，而是为了把「加法」变成「乘法」**，让下一步的独立性有地方用。

**第二步：独立性拆开。**

$$\mathbb{E}\big[e^{t(\bar X-\mu)}\big]=\prod_{i=1}^{n}\mathbb{E}\big[e^{t(X_i-\mu_i)/n}\big].$$

**第三步：Hoeffding 引理。** 若 $X\in[a,b]$、$\mathbb{E}X=\mu$，则

$$\mathbb{E}\big[e^{t(X-\mu)}\big]\le\exp\!\Big(\frac{t^{2}(b-a)^{2}}{8}\Big).$$

证明只用一个事实：$e^{tx}$ 是凸函数，所以它在 $[a,b]$ 上**低于端点连线**：

$$e^{tx}\le\frac{b-x}{b-a}e^{ta}+\frac{x-a}{b-a}e^{tb}.$$

取期望。记 $p=\dfrac{\mu-a}{b-a}$、$w=t(b-a)$，则

$$\mathbb{E}e^{tX}\le(1-p)e^{ta}+p\,e^{tb}=e^{t\mu}\Big[(1-p)e^{-pw}+p\,e^{(1-p)w}\Big].$$

括号取对数，记 $\psi(w)=\log\big((1-p)e^{-pw}+p e^{(1-p)w}\big)$。直接求导：

$$\psi(0)=0,\qquad \psi'(0)=-p+\frac{p\,e^{w}}{1-p+p\,e^{w}}\Big|_{w=0}=-p+p=0,$$

$$\psi''(w)=\frac{p(1-p)e^{w}}{(1-p+p\,e^{w})^{2}}=z(1-z),\qquad z=\frac{p\,e^{w}}{1-p+p\,e^{w}}\in(0,1).$$

$z(1-z)$ 的最大值是 $\dfrac14$，于是由带余项的 Taylor 展开

$$\psi(w)=\psi(0)+\psi'(0)w+\int_0^{w}(w-s)\,\psi''(s)\,\mathrm{d}s\le\frac14\cdot\frac{w^{2}}{2}=\frac{w^{2}}{8}.$$

**那个 $1/4$ 就是这么来的**——不是凑的，是 $z(1-z)$ 的峰。合起来就是引理。

**第四步：代回并优化 $t$。**

$$\mathbb{P}(\bar X-\mu\ge\epsilon)\le\exp\!\Big(-t\epsilon+\frac{t^{2}(b-a)^{2}}{8n}\Big).$$

右边对 $t$ 是二次函数，最小值在 $t^{*}=\dfrac{4n\epsilon}{(b-a)^{2}}$，代回去：

$$\exp\!\Big(-\frac{2n\epsilon^{2}}{(b-a)^{2}}\Big).$$

双边再补一次 $-X$ 的版本（同一个 $[a,b]$、同样的推导），加 union bound 得 $2$ 倍。**公式里没有一个数字是假设的**：$2$ 来自双边，$(b-a)^{2}$ 来自引理，$n$ 来自独立性。

![同一个 ε 下：Chebyshev 按 ε⁻² 掉，Hoeffding 按 e⁻²ⁿᵋ² 掉，真实尾概率夹在中间](/images/bandit-figures/tail-bounds.png)

*看图要点*：三条线都是「偏离 ε 超过这么多的概率」的上界（虚线是真实值）。$n=100$、伯努利 $\tfrac12$ 时，$\epsilon=0.2$ 处 Chebyshev 给 $6\times10^{-2}$、Hoeffding 给 $7\times10^{-4}$，真实值 $2\times10^{-4}$——**差的两个数量级全部来自「ε 在指数上」而不是「ε 在分母上」**。左上角灰带是「界比 1 还大」的无意义区，也是所有尾界都要面对的尴尬。

> **补：为什么值得费这么大劲**
> Chebyshev 只要求二阶矩，代价是 $1/\epsilon^{2}$；Hoeffding 要求有界与独立，换来 $e^{-n\epsilon^{2}}$。**指数衰减是 union bound 之后仍然收敛的前提**——第 3 篇要把 $nk$ 个坏事件一起控制住，多项式衰减根本压不住。

### 5.4 Union bound（并集界）

**条件**：无。**形式**：

$$\mathbb{P}\!\left(\bigcup_{i}A_i\right)\le\sum_{i}\mathbb{P}(A_i).$$

**用法**：同时控制很多个坏事件。第 3 篇里对 $n$ 轮、$k$ 个臂一起做 union bound，得到 $nk\delta$；取 $\delta=1/n^{2}$ 就把它压成 $k/n$。**注意它完全不计重复计数**，所以 union bound 永远偏保守。

### 5.5 Jensen 不等式

**条件**：$\varphi$ 凸，$X$ 与 $\varphi(X)$ 可积。**形式**：

$$\varphi(\mathbb{E}[X])\le\mathbb{E}[\varphi(X)].$$

**用法**：KL 非负性（第 7 节）、Cramér–Rao 下界、以及「$\log$ 是凹的所以 $\mathbb{E}\log X\le\log\mathbb{E}X$」这类判断。

> **补：为什么说「KL 不是距离」**
> KL 满足非负性，但不满足对称性与三角不等式：$\mathrm{KL}(P\|Q)\neq\mathrm{KL}(Q\|P)$。bandit 下界里出现的是**有方向的那一个**，方向由「真实分布在前」决定。把它当欧氏距离去理解，会在第 4 篇 5.5 节卡住。

### 5.6 次高斯：从有界到方差

**定义**：若存在 $\sigma>0$，使对一切 $t\in\mathbb{R}$ 都有

$$\mathbb{E}\big[e^{t(X-\mu)}\big]\le e^{\sigma^{2}t^{2}/2},$$

则称 $X$ 是 **$\sigma$-次高斯**的（$\mu=\mathbb{E}X$）。

这个定义看起来很奇怪——为什么要管矩母函数长什么样？因为它只做一件事：**让 Chernoff 那一步能走通**。把 5.3 的第 1、4 步重做一遍（这次不拆 $n$ 个样本，只对单个 $X$）：

$$\mathbb{P}(X-\mu\ge\epsilon)\le e^{-t\epsilon}\,\mathbb{E}e^{t(X-\mu)}\le \exp\!\Big(-t\epsilon+\frac{\sigma^{2}t^{2}}{2}\Big),$$

对 $t$ 取最优 $t^{*}=\epsilon/\sigma^{2}$：

$$\mathbb{P}(X-\mu\ge\epsilon)\le e^{-\epsilon^{2}/(2\sigma^{2})}.$$

双边就是

$$\boxed{\ \mathbb{P}(|X-\mu|\ge\epsilon)\le 2e^{-\epsilon^{2}/(2\sigma^{2})}\ }$$

**于是「次高斯」= 「尾部按 $e^{-\epsilon^{2}}$ 掉」**，$\sigma$ 就是那个尺度的名字。

#### 5.6.1 三个来源

**一、有界 $\Rightarrow$ 次高斯。** 由 5.3 的引理，$X\in[a,b]$ 时 $\mathbb{E}e^{t(X-\mu)}\le e^{t^{2}(b-a)^{2}/8}$，与 $e^{\sigma^{2}t^{2}/2}$ 对齐得

$$\sigma=\frac{b-a}{2}.$$

**注意 $\sigma$ 不是标准差**：$\mathrm{Bern}(p)$ 的 $\sigma=1/2$，而它的标准差 $\sqrt{p(1-p)}\le 1/2$。次高斯的 $\sigma$ 是「最坏情况下的尺度」，通常比真实标准差大。

**二、正态 $\Rightarrow$ 次高斯**，且 $\sigma^{2}$ 恰好等于方差（把正态的矩母函数直接代入即可）。

**三、独立的次高斯相加**仍是次高斯的，$\sigma^{2}$ 相加：

$$\mathbb{E}e^{t\sum(X_i-\mu_i)}=\prod\mathbb{E}e^{t(X_i-\mu_i)}\le\exp\!\Big(\frac{t^{2}}{2}\sum\sigma_i^{2}\Big).$$

所以 $\bar X=\frac1n\sum X_i$ 是 $\frac{\bar\sigma}{\sqrt n}$-次高斯的，其中 $\bar\sigma^{2}=\frac1{n^{2}}\sum\sigma_i^{2}$。**这正是「样本越多，区间越窄」的全部内容**：宽度 $\propto 1/\sqrt T$。

#### 5.6.2 它与 Hoeffding 的关系

把 $\sigma=(b-a)/2$ 代进上面的框：

$$2e^{-\epsilon^{2}/(2\sigma^{2})}=2e^{-2\epsilon^{2}/(b-a)^{2}},$$

这正是 5.3 的 Hoeffding。**所以 Hoeffding 不是另一个不等式，它就是「有界分布是次高斯的」这句话的展开。**

| 说法 | 形式 | 用在哪 |
|---|---|---|
| 次高斯（定义） | $\mathbb{E}e^{t(X-\mu)}\le e^{\sigma^{2}t^{2}/2}$ | 一切「指数化 + Markov」的起点 |
| 次高斯（尾界） | $\mathbb{P}(\lvert X-\mu\rvert\ge\epsilon)\le 2e^{-\epsilon^{2}/(2\sigma^{2})}$ | 置信区间、UCB 的 bonus |
| 有界 ⇒ 次高斯 | $\sigma=(b-a)/2$ | 伯努利、$[0,1]$ 奖励 |
| Hoeffding | $2e^{-2n\epsilon^{2}/(b-a)^{2}}$ | 把 $n$ 个样本一起算 |

第 3 篇的 UCB 用的是 $\sigma=1/2$（奖励在 $[0,1]$），于是

$$\mathrm{UCB}_i=\hat\mu_i+\sqrt{\frac{2\log(1/\delta)}{T_i}}.$$

这个 bonus 就是「宽度为 $\sqrt{2\log(1/\delta)/T_i}$ 的置信区间」的上端——5.3 和 5.6 到这里合流了。

#### 5.6.3 四个会误用它的地方

1. **「有界」不是必需的，但「尾部足够瘦」是。** 柯西分布、$\alpha<2$ 的帕累托都不次高斯，它们的样本均值根本不稳定。
2. **次高斯的 $\sigma$ 不是标准差。** 用真实标准差代进去会得到一个「看着更紧但不对」的界。
3. **依赖数据的 $t$ 要小心。** UCB 里 $T_i(t)$ 是随机的，联合界必须一次性对所有 $(i,t)$ 成立，不能每步单独用。
4. **有界但相关的样本不能直接乘。** 第 2 步用的是独立性；换成鞅或混合条件，要改用 Azuma / Bernstein 型结论。

---

## 6. Stirling 公式与阶乘

$$n!=\sqrt{2\pi n}\,\left(\frac{n}{e}\right)^{n}\left(1+O\!\left(\frac1n\right)\right).$$

取对数：

$$\ln(n!)=n\ln n-n+\frac12\ln(2\pi n)+O\!\left(\frac1n\right).$$

**什么时候用**：算 $\binom{n}{k}=\frac{n!}{k!(n-k)!}$ 的数量级（组合数、二项分布尾界、生日问题）；以及「$\ln(n!)$ 的主项是 $n\ln n$」这类判断。

一个直接推论是 4.3 节的二项系数上界。另一个是：**大数定律里 $\binom{n}{k}$ 不会爆炸**——它的对数增长是 $O(n)$，而不是 $O(n\log n)$。

## 7. KL 散度

### 7.1 定义

对两个离散分布 $P,Q$（$P\ll Q$），

$$\mathrm{KL}(P\|Q)=\sum_{x}P(x)\log\frac{P(x)}{Q(x)}.$$

连续情形把求和换成积分。约定 $0\log 0=0$。

### 7.2 非负性

由 Jensen（$\log$ 凹）：

$$-\mathrm{KL}(P\|Q)=\sum_x P(x)\log\frac{Q(x)}{P(x)}\le\log\sum_x P(x)\frac{Q(x)}{P(x)}=\log 1=0.$$

所以 $\mathrm{KL}(P\|Q)\ge 0$，等号当且仅当 $P=Q$。

### 7.3 两个伯努利的 KL

$P=\mathrm{Bern}(p)$、$Q=\mathrm{Bern}(q)$ 时

$$d(p,q)=p\log\frac{p}{q}+(1-p)\log\frac{1-p}{1-q}.$$

当 $p\approx q$ 时，二阶展开给出

$$d(p,q)\approx\frac{(p-q)^{2}}{2q(1-q)},$$

分母 $2q(1-q)$ 就是「$2\log n/\Delta$ 里的 2」的来源（第 4 篇 5.5 节有完整推导）。**KL 在局部是二次的，所以它和 $\Delta^2$ 只差一个曲率因子。**

### 7.4 在 bandit 里扮演什么角色

Lai–Robbins 下界写的是

$$R_n\ \ge\ (1-o(1))\ln n\sum_{i}\frac{\Delta_i}{\mathrm{KL}(P_i\|P^{*})}.$$

它回答的是「最好的算法能做到多快」：**决定难度的不是间隙 $\Delta$ 本身，而是「把 $P_i$ 和 $P^*$ 区分开需要多少信息」**。两个分布均值差同样的量，方差大的那个更难分辨。

## 8. 速查表

| 工具 | 形式 | 用在哪 |
|---|---|---|
| 调和数 | $H_n=\ln n+O(1)$ | $1/t$ 错误率 → $\log n$ |
| 对数不等式 | $\log(1+x)\le x$ | 连乘转指数 |
| 指数不等式 | $1-x\le e^{-x}$ | ETC 界的指数项 |
| Markov | $\mathbb{P}(X\ge a)\le\mathbb{E}X/a$ | 一切尾界的老祖宗 |
| Chebyshev | $\mathbb{P}(\lvert X-\mu\rvert\ge a)\le\sigma^2/a^2$ | 弱大数定律 |
| Hoeffding 引理 | $\mathbb{E}e^{t(X-\mu)}\le e^{t^2(b-a)^2/8}$ | 四步推导的核心，$1/4$ 的出处 |
| Hoeffding | $\mathbb{P}(\lvert\bar X-\mu\rvert\ge\epsilon)\le 2e^{-2n\epsilon^2}$ | 置信区间、UCB bonus |
| 次高斯 | $\mathbb{E}e^{t(X-\mu)}\le e^{\sigma^2t^2/2}$，$\sigma=(b-a)/2$ | 一切「指数化 + Markov」的起点 |
| Union bound | $\mathbb{P}(\cup A_i)\le\sum\mathbb{P}(A_i)$ | $\delta=1/n^2$ |
| Jensen | $\varphi(\mathbb{E}X)\le\mathbb{E}\varphi(X)$ | KL ≥ 0、Cramér–Rao |
| Stirling | $n!\approx\sqrt{2\pi n}(n/e)^n$ | 组合数、二项尾界 |
| KL | $\sum P\log(P/Q)\ge 0$ | 下界的「距离」 |

> **证明去哪了**：5.3.1 的四步是完整证明。其余式子的推导（Markov、Chebyshev、union bound、Jensen、KL 非负、Stirling 推论、以及后面统计与 bandits 的每一条界）都收在 [附录：公式与证明索引](/posts/proof-appendix/)。

## 9. 六个容易踩的坑

1. **把 $O(1)$ 当成「很小」**。$O(1)$ 只表示不随 $n$ 增长，可以是 $10^{6}$。
2. **给 Markov 用了负值**。Markov 要求 $X\ge 0$，$|X-\mu|$ 要用 Chebyshev。
3. **以为 union bound 需要独立**。它不需要，代价是可能非常松。
4. **把 $\mathbb{E}[XY]=\mathbb{E}X\,\mathbb{E}Y$ 当成恒等式**。它只在独立（或至少不相关）时成立。
5. **忘了 Hoeffding 要有界**。无界分布（比如正态）要走次高斯版本，不能直接套 $[a,b]$。
6. **把 KL 当距离用**。它不对称，也不满足三角不等式。

---

**下一篇**：[概率论基础](/posts/probability-foundations/) —— 把这套工具装进概率空间里。
