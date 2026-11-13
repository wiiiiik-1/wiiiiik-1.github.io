---
title: 数理统计基础：估计、区间与检验
description: 统计模型与抽样分布、偏差与 MSE、MLE 与充分统计量、置信区间的正确读法、Neyman–Pearson 与 p 值、贝叶斯后验——第 1 篇与第 4 篇之间缺的那块地板。
date: 2026-11-03
tags: ["数理统计", "参数估计", "假设检验", "贝叶斯"]
draft: false
featured: false
lang: zh-CN
---

> **材料来源**：DeGroot & Schervish, *Probability and Statistics*, 4th ed. 的第 7–9 章（估计、估计量的抽样分布、假设检验），以及第 11 章里回归部分的记号。MLE 与充分统计量在该书 Ch.7，t 与 F 分布在 Ch.8，Neyman–Pearson 与似然比检验在 Ch.9。
> **和上一篇的关系**：概率论告诉你怎么从参数算数据，这一篇反过来：**拿着数据说参数**。第 1 篇的 MLE、置信区间、p 值都在这一篇里有完整出处。
> **符号约定**：$\theta$ 是参数，$\hat\theta$ 是估计量，$x_{1:n}=(x_1,\dots,x_n)$ 是样本，$L(\theta)=p(x_{1:n};\theta)$ 是似然，$\ell=\log L$。
> **系列位置**：前置 2 · 数理统计。上一篇是 [概率论基础](/posts/probability-foundations/)，下一篇是 [第 1 篇 · 假设检验与估计](/posts/hypothesis-testing-and-estimation/)。

---

## 0. 这一章补的是哪块地板

第 1 篇直接从「四格表」开始，第 4 篇直接用「后验」更新。中间那些东西——样本方差为什么除以 $n-1$、$t$ 分布为什么比正态胖、p 值到底在说什么——都被略过了。

这一篇按「一个统计问题从提出到回答」的顺序补：

$$\text{模型}\ \to\ \text{估计}\ \to\ \text{区间}\ \to\ \text{检验}\ \to\ \text{贝叶斯}.$$

## 1. 统计模型

### 1.1 参数模型与似然

统计推断的起点是一句假设：**数据来自某个带参数的分布族**，

$$x_1,\dots,x_n\overset{\text{iid}}{\sim}p(x;\theta),\qquad \theta\in\Theta.$$

$\theta$ 是未知的、固定的（频率派）或者随机的（贝叶斯派）。两种世界观在后面会分叉，但**似然函数是共用的**：

$$L(\theta)=p(x_{1:n};\theta)=\prod_{i=1}^{n}p(x_i;\theta).$$

> **补：似然不是概率**
> $L(\theta)$ 作为 $\theta$ 的函数，**对 $\theta$ 不归一化**：$\int L(\theta)\,\mathrm{d}\theta$ 一般不等于 1。它只是「在参数取 $\theta$ 时，看到这组数据的相对可能性」。把似然当概率去积分，是初学阶段最常见的错误。

### 1.2 统计量

**统计量**是样本的函数，且不含未知参数。例如 $\bar X$、$S^{2}$、$\max X_i$。

统计量自己也是随机变量——换一组样本就变一次。它的分布叫**抽样分布**，这是第 2 节的主题。

## 2. 抽样分布

### 2.1 样本均值与样本方差

$$\bar X=\frac1n\sum_{i=1}^{n}X_i,\qquad S^{2}=\frac{1}{n-1}\sum_{i=1}^{n}(X_i-\bar X)^{2}.$$

$\bar X$ 的无偏性是显然的（期望线性）。$S^{2}$ 除以 $n-1$ 而不是 $n$，是因为

$$\mathbb{E}\!\left[\sum_{i=1}^{n}(X_i-\bar X)^{2}\right]=(n-1)\sigma^{2}.$$

**减掉 $\bar X$ 用掉了一个自由度**。用 $n$ 除会系统性低估方差——这就是 $n-1$ 的全部原因，不是什么「修正系数」。

### 2.2 $\chi^{2}$、$t$、$F$

设 $X_i\overset{\text{iid}}{\sim}\mathcal{N}(\mu,\sigma^{2})$。

**卡方**：$\sum_{i=1}^{n}Z_i^{2}\sim\chi^{2}_n$（$Z_i$ 独立标准正态）。样本方差的分布是

$$\frac{(n-1)S^{2}}{\sigma^{2}}\sim\chi^{2}_{n-1}.$$

**t**：若 $Z\sim\mathcal{N}(0,1)$、$V\sim\chi^{2}_{\nu}$ 且独立，则

$$T=\frac{Z}{\sqrt{V/\nu}}\sim t_{\nu}.$$

把 $Z=\sqrt{n}(\bar X-\mu)/\sigma$ 与 $V=(n-1)S^{2}/\sigma^{2}$ 代进去，$\sigma$ 被约掉：

$$\frac{\bar X-\mu}{S/\sqrt n}\sim t_{n-1}.$$

**这就是「$\sigma$ 未知时用 $t$ 而不是 $z$」的来历**：你不知道 $\sigma$，只好用 $S$ 代替，代价是分布变胖。

**F**：两个独立卡方各自除以自由度再相除。用于比较两个方差，也是 ANOVA 的检验统计量。

### 2.3 为什么 $t$ 比正态胖

$t$ 的密度是

$$f(t)=\frac{\Gamma\!\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi}\,\Gamma\!\left(\frac{\nu}{2}\right)}\left(1+\frac{t^{2}}{\nu}\right)^{-(\nu+1)/2}.$$

尾部按 $|t|^{-(\nu+1)}$ 衰减，比正态的 $e^{-t^{2}/2}$ 慢得多。$\nu\to\infty$ 时收敛到正态。

**直观解释**：分母 $S$ 本身是随机的，偶尔偏小，于是整个比值被放大。$n$ 小的时候这种「偶尔」很常见，所以尾巴厚。$n=30$ 以上时 $t_{29}$ 与正态的分位数差别已经在 2% 以内，但 $n=5$ 时差别很大（$t_{4}$ 的 97.5% 分位数是 2.776，正态是 1.96）。

## 3. 估计量

### 3.1 偏差、方差、MSE

$$\text{Bias}(\hat\theta)=\mathbb{E}[\hat\theta]-\theta,\qquad \mathrm{MSE}(\hat\theta)=\mathbb{E}[(\hat\theta-\theta)^{2}].$$

三者之间有一条必须记住的分解：

$$\mathrm{MSE}=\text{Bias}^{2}+\mathrm{Var}.$$

**「准」与「稳」是两件事**，MSE 把它们合成一个数。有偏估计可能比无偏估计更好——只要方差降得够多。教科书例子：正态均值用 $c\bar X$ 估计，$c=\frac{n}{n+1}$ 时 MSE 更小（收缩估计的雏形）。

### 3.2 一致性

$\hat\theta_n$ 依概率收敛到 $\theta$ 时称一致。充分条件：$\text{Bias}\to0$ 且 $\mathrm{Var}\to0$，由 Chebyshev 立得。

**无偏不一定一致**（比如用第一个样本估计均值），**一致也不一定无偏**（$\frac{n}{n+1}\bar X$）。

### 3.3 有效性

无偏估计里方差最小的叫**有效**（UMVUE，一致最小方差无偏估计）。Rao–Blackwell 与 Lehmann–Scheffé 给出构造方法，核心工具是第 4 节的充分统计量。

## 4. 充分统计量与信息

### 4.1 因子分解定理

$T(X_{1:n})$ 是 $\theta$ 的充分统计量，当且仅当似然能写成

$$L(\theta)=g\big(T(x_{1:n}),\theta\big)\,h(x_{1:n}).$$

**含义**：给定 $T$ 之后，原始数据不再含有关于 $\theta$ 的额外信息。$n$ 个伯努利样本的充分统计量是 $\sum X_i$（总和），不是顺序。

### 4.2 Fisher 信息

$$\mathcal{I}(\theta)=\mathbb{E}\!\left[\left(\frac{\partial}{\partial\theta}\log p(X;\theta)\right)^{2}\right]=-\mathbb{E}\!\left[\frac{\partial^{2}}{\partial\theta^{2}}\log p(X;\theta)\right].$$

它是「数据里关于 $\theta$ 的信息量」，量纲是 $1/\theta^{2}$。$n$ 个独立样本的信息是 $n\mathcal{I}(\theta)$。

### 4.3 Cramér–Rao 下界

对任何无偏估计量，

$$\mathrm{Var}(\hat\theta)\ \ge\ \frac{1}{n\mathcal{I}(\theta)}.$$

**它解释了为什么「更准」有物理上限**：想再准，只能增加样本或改进模型，不能靠更聪明的算法。

MLE 在正则条件下渐近达到这个下界：

$$\sqrt{n}(\hat\theta_{\text{MLE}}-\theta)\ \xrightarrow{\ d\ }\ \mathcal{N}\!\left(0,\ \mathcal{I}(\theta)^{-1}\right).$$

**这句话是后面所有「$\hat\mu\pm z\sigma/\sqrt n$」的理论根据。**

## 5. 置信区间

### 5.1 枢轴量法

找一个**分布不依赖 $\theta$** 的量 $Q(X_{1:n},\theta)$（枢轴量），再解不等式

$$\mathbb{P}(q_{1}\le Q\le q_{2})=1-\alpha\ \Longrightarrow\ \theta\in[\hat\theta_L,\hat\theta_U].$$

**关键在「分布不依赖 $\theta$」**：只有这样才能把 $Q$ 的分位数当常数用。

### 5.2 正态均值

$\sigma$ 已知：

$$\bar X\pm z_{1-\alpha/2}\frac{\sigma}{\sqrt n}.$$

$\sigma$ 未知：

$$\bar X\pm t_{n-1,1-\alpha/2}\frac{S}{\sqrt n}.$$

### 5.3 比例的区间：Wald 的失败

$\hat p$ 的 Wald 区间是

$$\hat p\pm z_{1-\alpha/2}\sqrt{\frac{\hat p(1-\hat p)}{n}}.$$

**它在 $\hat p=0$ 或 $1$ 时宽度为零**，显然荒谬。$n=20$、观察到 0 次成功时，Wald 给出 $[0,0]$，而真实覆盖率远低于名义值。

Wilson 区间（score interval）修掉了这个问题：

$$\frac{\hat p+\frac{z^{2}}{2n}\pm z\sqrt{\frac{\hat p(1-\hat p)}{n}+\frac{z^{2}}{4n^{2}}}}{1+\frac{z^{2}}{n}}.$$

$\hat p=0$ 时它给出一个非退化的上界。**经验法则：$n\hat p<10$ 时别用 Wald。**

### 5.4 Hoeffding 区间

第 1 篇 3.6 节用的就是这个。由 Hoeffding 不等式反解：

$$\mathbb{P}\left(|\hat\mu_n-\mu|\ge\sqrt{\frac{\log(2/\delta)}{2n}}\right)\le\delta.$$

所以 $1-\delta$ 的区间是

$$\hat\mu_n\pm\sqrt{\frac{\log(2/\delta)}{2n}}.$$

**它不要求正态、不要求方差已知**，只要求有界与独立——代价是比 $z\sigma/\sqrt n$ 宽（通常宽 20%–40%）。

### 5.5 覆盖率怎么读

「95% 置信区间」的正确含义：**如果重复抽样无数次，95% 的区间会盖住真值**。它**不是**「$\theta$ 落在这个区间里的概率是 95%」——在频率派框架下 $\theta$ 是固定的，没有概率可言。

这个区别在贝叶斯那里才被消掉：可信区间（credible interval）说的确实是「后验概率 95%」。两者在 $n$ 大时数值接近，小样本时可能完全不同。

> **补：为什么这个区别不是咬文嚼字**
> 一个具体的 95% 区间 $[3.1,4.2]$，要么盖住真值要么没有，没有「95% 的概率」。置信区间的 95% 是**程序**的性质，不是**这一次结果**的性质。第 1 篇里那句「用 Hoeffding 做区间估计」之所以要写清楚「对每次抽样的覆盖」，原因就在这里。

## 6. 假设检验

### 6.1 原假设、拒绝域与功效

要检验 $H_0:\theta\in\Theta_0$ 对 $H_1:\theta\in\Theta_1$。检验就是一个拒绝域 $R$：$x\in R$ 时拒绝 $H_0$。

**功效函数**：

$$\pi(\theta)=\mathbb{P}_\theta(X\in R).$$

它给出「参数为 $\theta$ 时拒绝 $H_0$ 的概率」。在 $\Theta_0$ 上希望它小（少误报），在 $\Theta_1$ 上希望它大（少漏报）。

### 6.2 两类错误

| | $H_0$ 真 | $H_0$ 假 |
|---|---|---|
| 拒绝 $H_0$ | 第一类错误（$\alpha$） | 正确（功效 $1-\beta$） |
| 不拒绝 | 正确 | 第二类错误（$\beta$） |

**两者不能同时变小**：固定 $n$ 时压低 $\alpha$ 必然抬高 $\beta$。唯一的出路是增加样本量——这就是「功效分析」要算的东西。

### 6.3 检验的构造：从似然比出发

绝大多数检验都可以写成似然比的形式：

$$\Lambda(x)=\frac{\sup_{\theta\in\Theta_0}L(\theta)}{\sup_{\theta\in\Theta}L(\theta)}\in[0,1].$$

$\Lambda$ 小就拒绝 $H_0$。$t$ 检验、$F$ 检验、卡方拟合优度检验都是它的特例（经过单调变换）。

### 6.4 p 值

$$p\text{-value}=\mathbb{P}_{H_0}(\text{统计量比观测值更极端}).$$

**正确读法**：假设 $H_0$ 为真，重复实验时看到「至少这么极端」的结果的概率。

**错误读法**（三种最常见）：

1. 「$p=0.03$ 表示 $H_0$ 为真的概率是 3%」——错，p 值是 $P(\text{数据}\mid H_0)$，不是 $P(H_0\mid\text{数据})$；
2. 「$p>0.05$ 就证明 $H_0$ 成立」——错，只能说没有足够证据拒绝；
3. 「$p$ 越小效应越大」——错，$p$ 同时依赖效应与样本量，$n$ 很大时微小效应也能得到极小的 $p$。

第 1 篇 3.1 节用「证据强度」这个说法，就是为了避免第一种误读。

### 6.5 Neyman–Pearson 引理

**简单假设** $H_0:\theta=\theta_0$ 对 $H_1:\theta=\theta_1$ 时，水平 $\alpha$ 下功效最大的检验由似然比给出：

$$\Lambda(x)=\frac{L(\theta_1)}{L(\theta_0)}\ \gtrless\ k,\qquad \mathbb{P}_{\theta_0}(\Lambda>k)=\alpha.$$

**它只处理简单对简单**，但把「最强检验长什么样」这个问题彻底回答了：一定是似然比。复合假设要靠 Karlin–Rubin（单调似然比）推广。

**与贝叶斯的关系**：如果给两个假设各一个先验，后验比就是

$$\frac{\mathbb{P}(H_1\mid x)}{\mathbb{P}(H_0\mid x)}=\frac{\pi_1}{\pi_0}\cdot\frac{L(\theta_1)}{L(\theta_0)},$$

所以贝叶斯检验也是「似然比对一个阈值」，只不过阈值由先验与代价决定。**第 1 篇说的「同一个贝叶斯模板」，指的就是这件事。**

### 6.6 两个最常用的检验

**单样本 $t$ 检验**（$\sigma$ 未知，检验均值）：

$$t=\frac{\bar X-\mu_0}{S/\sqrt n}\ \sim\ t_{n-1}\ \text{在 }H_0\text{ 下}.$$

**卡方拟合优度**：观察频数 $O_i$ 与期望频数 $E_i$，

$$\sum_{i=1}^{k}\frac{(O_i-E_i)^{2}}{E_i}\ \sim\ \chi^{2}_{k-1-m},$$

$m$ 是估计掉的参数个数。第 1 篇里的「分类」问题如果有多类，用的就是它。

## 7. 贝叶斯推断

### 7.1 先验、后验、共轭

$$p(\theta\mid x_{1:n})\ \propto\ p(x_{1:n}\mid\theta)\,p(\theta).$$

如果后验与先验同族，称**共轭**。共轭不是数学上的必然，只是为了能写出闭式解。

### 7.2 两个必须会的共轭

**Beta–Bernoulli**：$X_i\sim\mathrm{Bern}(p)$，先验 $p\sim\mathrm{Beta}(a,b)$，则

$$p\mid x_{1:n}\sim\mathrm{Beta}\!\left(a+\sum x_i,\ b+n-\sum x_i\right).$$

后验均值是

$$\hat p_{\text{Bayes}}=\frac{a+\sum x_i}{a+b+n},$$

可以读成「把先验当成 $a$ 次成功、$b$ 次失败掺进去」。$a=b=1$ 时是先验均匀的 Laplace 平滑。

**Normal–Normal**：$X_i\sim\mathcal{N}(\mu,\sigma^{2})$（$\sigma^{2}$ 已知），先验 $\mu\sim\mathcal{N}(\mu_0,\tau^{2})$，则

$$\mu\mid x_{1:n}\sim\mathcal{N}\!\left(\frac{\frac{\mu_0}{\tau^{2}}+\frac{n\bar x}{\sigma^{2}}}{\frac{1}{\tau^{2}}+\frac{n}{\sigma^{2}}},\ \left(\frac{1}{\tau^{2}}+\frac{n}{\sigma^{2}}\right)^{-1}\right).$$

后验均值是「先验均值与样本均值按精度加权平均」，后验方差是「两个精度相加的倒数」。

**第 4 篇 TS 的 Gaussian 更新就是这个式子**，只不过把 $\tau^{2}$ 换成「当前的后验方差」、把 $n\bar x/\sigma^{2}$ 换成「已观测的充分统计量」。

### 7.3 可信区间与置信区间

**可信区间**：$[a,b]$ 使 $\mathbb{P}(\theta\in[a,b]\mid x)=1-\alpha$。说的确实是「$\theta$ 在区间里的后验概率」。

**置信区间**：$[A(X),B(X)]$ 使 $\mathbb{P}(\theta\in[A,B])=1-\alpha$（对重复抽样）。说的是一组区间的覆盖率。

$n$ 大时两者数值通常接近（Bernstein–von Mises），小样本或强先验时可能差别很大。

## 8. 与 bandits 的接口

| 统计概念 | 在 bandits 里的对应物 |
|---|---|
| 参数模型 | 每个臂的奖励分布 $P_i$ |
| 置信区间 | UCB 的 $\hat\mu_i\pm\sqrt{2\log(1/\delta)/T_i}$ |
| 后验 | TS 每一步抽的那个分布 |
| 共轭更新 | Beta–Bernoulli、Normal–Normal |
| 估计量方差 | bonus 的宽度 $\propto 1/\sqrt{T}$ |
| 覆盖率的权衡 | 探索与利用的两难 |

**一句话**：UCB 是「用置信上界做决策」的频率派算法，TS 是「用后验抽样做决策」的贝叶斯派算法。**两者共用同一套估计量理论，区别只在用什么代替「不确定」**。

## 9. 速查

| 主题 | 公式 |
|---|---|
| MSE 分解 | $\mathbb{E}[(\hat\theta-\theta)^{2}]=\text{Bias}^{2}+\mathrm{Var}$ |
| 样本方差 | $S^{2}=\frac{1}{n-1}\sum(X_i-\bar X)^{2}$ |
| t 统计量 | $\frac{\bar X-\mu}{S/\sqrt n}\sim t_{n-1}$ |
| Cramér–Rao | $\mathrm{Var}(\hat\theta)\ge 1/(n\mathcal{I}(\theta))$ |
| Wald 区间 | $\hat p\pm z\sqrt{\hat p(1-\hat p)/n}$ |
| Hoeffding 区间 | $\hat\mu\pm\sqrt{\log(2/\delta)/(2n)}$ |
| Neyman–Pearson | 似然比 $>k$ |
| Beta 后验 | $\mathrm{Beta}(a+\sum x_i,\,b+n-\sum x_i)$ |
| 后验均值 | 先验均值与样本均值按精度加权 |

## 10. 六个容易错的地方

1. **把 $n-1$ 说成「修正系数」**：它是自由度，来源是减去 $\bar X$。
2. **把似然当概率积分**：$L(\theta)$ 对 $\theta$ 不归一化。
3. **$\sigma$ 未知还用 $z$**：$n$ 小的时候置信区间会偏窄，第一类错误率被抬高。
4. **$\hat p$ 接近 0 或 1 时用 Wald**：覆盖率会崩，换 Wilson。
5. **把 p 值当「$H_0$ 为真的概率」**：方向反了，见 6.4。
6. **把置信区间说成「参数有 95% 概率在里面」**：那是可信区间的说法。

---

**下一篇**：[第 1 篇 · 假设检验与参数估计](/posts/hypothesis-testing-and-estimation/) —— 两份讲义，中英对照。
