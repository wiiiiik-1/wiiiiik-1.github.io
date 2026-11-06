---
title: "从 ETC 到 UCB：遗憾分析、置信上界与 O(log n)"
description: "接续 Lecture 3b 的 bandit 设定：先把 ETC 的 regret 拆成探索与承诺两段、解出最优 m，再用置信上界把它换成逐臂自适应的 UCB，最后给出 R_n = O(Σ log n / Δ_i) 的定理以及和 ETC 的实测对比。"
date: 2026-11-06
tags: ["多臂老虎机", "UCB", "探索与利用", "Regret", "学习笔记"]
featured: false
lang: "zh-CN"
---

> **材料**：13 页手写讲义，*The Explore-Then-Commit Algorithm 与 The Upper Confidence Bound (UCB)*（ML-DM，October 2026，Lecture 4）。
> **和上一篇的关系**：Lecture 3b 只把 ETC「写出来」，这一讲做三件更硬的事——**给 ETC 算出 regret 界**、**找出它为什么不够好**、**用 UCB 修掉它**。
> **符号沿用手稿**：$\Delta_i=\mu^*-\mu_i$ 是臂 $i$ 的次优间隙，$n$ 是总轮数，$k$ 是臂数，$m$ 是每个臂的探索次数。
>
> **系列位置**：第 3 篇。问题从哪来见 [系列导论](/posts/bandits-series-intro/)；本篇反复用到的 regret 分解公式、次优间隙、$O(\log n)$ 的含义，前置推导都在 [多臂老虎机入门](/posts/multi-armed-bandits-intro/)。

---

## 0. 十三页在做一件事：把「探索预算」从常数改成数据驱动

```text
第 1–2 页   ETC 回顾：两阶段 + 动作序列
   ↓
第 2–5 页   ETC 的 regret 分析：拆两段 → 界（★★）→ 解最优 m → O(log n)
   ↓                        ↑
   │                代价：必须知道 Δ 才能调 m，而且所有臂被均匀地探 m 次
   ↓
第 6–8 页   UCB：乐观面对不确定性，用置信上界当 index，不需要知道 Δ
   ↓
第 9–12 页  为什么有效：置信区间窄于 Δ_i 时该臂就不再被选 → 16 log n / Δ_i²
   ↓
第 12–13 页 UCB 定理 R_n ≤ Σ 16 log n / Δ_i，以及和 ETC 的实测对比
```

| 原页 | 主题 |
|---|---|
| 1 | ETC 伪代码与探索期（$k=5,m=3$） |
| 2 | 承诺期例子；regret 分解公式；探索期 regret |
| 3 | 间隙 $\Delta_i$；承诺期 regret 的分段形式 |
| 4 | 总 regret 式子；概率界 $e^{-m\Delta_i^2/4}$；探索/利用权衡 |
| 5 | 最优 $m=\lceil 4\log n/\Delta^2\rceil$；一般 $k$ 的界 |
| 6 | UCB 的三个改进目标；乐观原理；index 的构成 |
| 7 | 置信界（Hoeffding 型）与 $\delta$ 的取法 |
| 8 | UCB 算法伪代码；$T_i=0$ 时 index 为 $\infty$ |
| 9 | 三臂示例：置信区间与上界 |
| 10 | 为什么有效：$T_i\ge16\log n/\Delta_i^2$ 后不再被选 |
| 11 | index 与置信区间的演化演示 |
| 12 | UCB 的 regret 定理；与 ETC 的结构差异 |
| 13 | $k=2$ 的实测对比图 |

---

## 1. 先把 ETC 摆回来

ETC 的思路和 **A/B testing** 一样，两个阶段：

```text
i  ） Exploration：轮转地把每个臂各拉 m 次（共 mk 轮）
ii ） Commit     ：从 t = mk+1 起，一直拉「探索期经验均值最高」的那个臂
```

$$
A_t=
\begin{cases}
(t \bmod k)+1, & t\le mk\\[4pt]
\arg\max_i \hat\mu_i(mk), & t> mk
\end{cases}
\qquad
\hat\mu_i(t)=\frac{\sum_{s=1}^{t}\mathbf 1[A_s=i]X_s}{T_i(t)}
$$

$k=5,\;m=3$ 时探索期是三个完整轮转：

$$
(2,3,4,5,1,\;2,3,4,5,1,\;2,3,4,5,1)
$$

若 2 号臂在探索期均值最高，之后所有轮都选 2：

$$
(2,3,4,5,1,\;\dots,\;2,\underbrace{2,2,\dots,2}_{t=mk+1\;\to\;n})
$$

> 承诺期一共 $n-mk$ 轮，而且**每轮都是同一个臂**——这一点后面算 regret 时反复用到。

把整条动作序列画出来，两阶段的对比非常直观：

![ETC 的动作序列：前 mk 轮按 2,3,4,5,1 轮转，之后固定选 2 号臂](/images/bandit-figures/etc-timeline.png)

*看图要点*：

- 左边浅黄区是**探索期**（$t\le mk=50$）：蓝色点画出一条整齐的锯齿——它在做**轮转**，每个臂各被拉 $m=10$ 次，与奖励无关。**这一步不"学习"，只是按部就班采样**；
- 右边是**承诺期**：红色点是一条水平线，锁定 2 号臂，直到 $t=n$；
- 分界处那条竖虚线就是 $t=mk$ 的**突变**——决策规则在这一刻彻底换了，而且之后再也不会回去看数据。这正是第 6 页「三个改进目标」里第三条要修的东西。

再补一句量级：探索期只占 $mk$ 轮，如果 $m$ 取得很小，图上左边那段会很窄——但承诺期一旦押错，整条水平线就钉在了错误的臂上。

---

## 2. ETC 的 regret 分析

### 2.1 从分解公式出发

上一篇已经推过（讲义第 2 页又写了一遍）：

$$
R_n=\sum_{a\in\mathcal A}\Delta_a\,\mathbb E[T_a(n)],
\qquad
\boxed{\Delta_i=\mu^*-\mu_i}
$$

其中 $\mu^*$ 是**最优臂**的平均奖励，$k$ 是臂数，$n$ 是总轮数。注意一个平凡但关键的事实：

> $\Delta_i$ 里**恰好有一个是 0**，就是 $i=a^*$（最优臂本身）。

所以后面所有求和都可以从 $i=2$ 开始（讲义把最优臂重新编号成 1 号；一般写法是只对 $\Delta_i>0$ 的臂求和）。

### 2.2 探索期：每个臂都被拉了 $m$ 次

探索期里每个臂**固定**被选 $m$ 次，所以

$$
\text{Regret during exploration}
=\sum_{i=1}^{k}m\cdot\Delta_i
=m\sum_{i=1}^{k}\Delta_i .
$$

这一步是 ETC 最「浪费」的地方：**不管这个臂有多差，都要花 $m$ 次机会去了解它**。

### 2.3 承诺期：一个分段函数

承诺期一共 $n-mk$ 轮，全部押在同一个臂上。写成条件形式：

$$
\text{Regret in commit phase}=
\begin{cases}
(n-mk)\Delta_1, & \text{若 } \hat\mu_1(mk)\ge\max_{i\ne1}\hat\mu_i(mk)\\
(n-mk)\Delta_2, & \text{若 } \hat\mu_2(mk)\ge\max_{i\ne2}\hat\mu_i(mk)\\
\quad\vdots & \quad\vdots\\
(n-mk)\Delta_k, & \text{若 } \hat\mu_k(mk)\ge\max_{i\ne k}\hat\mu_i(mk)
\end{cases}
$$

取期望，就得到「以概率加权」的形式。

### 2.4 合起来，并给概率一个上界

$$
\boxed{
R_n
=\underbrace{m\sum_{i=1}^{k}\Delta_i}_{\text{探索期}}
+\underbrace{(n-mk)\sum_{i=1}^{k}\Delta_i\,
P\!\left(\hat\mu_i(mk)\ge\max_{j\ne i}\hat\mu_j(mk)\right)}_{\text{承诺期}}
}
$$

把「承诺到次优臂」的概率用指数界压下去，就得到讲义第 4 页那个框：

$$
\boxed{
R_n\le m\sum_{i=2}^{k}\Delta_i
+(n-mk)\sum_{i=2}^{k}\Delta_i\,e^{-\frac{m\Delta_i^2}{4}}
}\qquad(\star\star)
$$

**为什么是指数界（补充推导，讲义只给了结果）**：设 $i$ 是次优臂、$i^*$ 是最优臂。二者经验均值之差

$$
\hat\mu_i-\hat\mu_{i^*}
$$

的均值为 $-\Delta_i$；每个均值只用了 $m$ 个 1-sub-Gaussian 样本，所以这个差的次高斯参数是 $\sqrt{2/m}$。于是

$$
P(\hat\mu_i\ge\hat\mu_{i^*})
=P\!\left(\hat\mu_i-\hat\mu_{i^*}\ge 0\right)
\le\exp\!\left(-\frac{\Delta_i^2}{2\cdot(2/m)}\right)
=e^{-\frac{m\Delta_i^2}{4}} .
$$

（「承诺到次优臂」的概率不会超过「它压过最优臂」的概率，所以用它当上界。）

### 2.5 最优的 $m$：两害相权

$(\star\star)$ 里两项的方向正好相反，讲义把这个权衡讲得很清楚：

| $m$ 的取法 | 第一项（探索期） | 第二项（承诺期） |
|---|---|---|
| $m$ **很大** | 变大（线性） | $e^{-m\Delta^2/4}\to 0$，几乎不犯错了 |
| $m$ **很小** | 变小 | 变大，常常押错臂，之后一路亏 |

把 $(\star\star)$ 的右端直接画出来，就是一个**先降后升的 U 形**：

![ETC 的 regret 上界随 m 变化的 U 形曲线，标出数值最小点与讲义公式给出的 m*](/images/bandit-figures/etc-regret-vs-m.png)

*看图要点*：

- 左端陡降：$m$ 太小，指数项 $e^{-m\Delta^2/4}$ 几乎等于 1，等于没学到东西就直接承诺；
- 右端缓升：$m$ 大到一定程度后指数项已接近 0，再增加 $m$ 只会线性地多付探索费；
- 谷底才是「两害相权」的解。图中两条竖线给出两个参考：绿色是**把 $(\star\star)$ 直接数值最小化**得到的 $m\approx453$，红色是**讲义公式** $\lceil4\log n/\Delta^2\rceil\approx921$。两者不重合是正常的——公式是渐近的、常数没优化，它对的是**增长阶**，不是有限 $n$ 下的最优点。

先看最简单的 $k=2$（只有一个间隙 $\Delta$）。取

$$
\boxed{m=\left\lceil\frac{4\log n}{\Delta^2}\right\rceil}
$$

（$\lceil x\rceil$ 是向上取整，即满足 $x\le\lceil x\rceil<x+1$ 的最小整数。）代回 $(\star\star)$：

$$
\boxed{R_n\le\frac{4\log n}{\Delta}+2\Delta}
\qquad\xrightarrow{\;n\to\infty\;}\qquad
R_n\approx\frac{4\log n}{\Delta},
$$

也就是说

$$
\boxed{R_n=O(\log n)}
$$

**这句话的物理含义**：要把两个均值相差 $\Delta$ 的臂区分开，需要各取约

$$
\frac{4\log n}{\Delta^2}
$$

个样本。间隙越小，需要的样本越多——这是平方反比关系，后面 UCB 的 $1/\Delta_i^2$ 也是同一个来源。

### 2.6 一般的 $k$：被「最小间隙」拖累

多个臂时，最优探索次数是

$$
\boxed{
m=\left\lceil\frac{4\log n}{\min_{j\ne1}\Delta_j^2}\right\rceil
}
$$

> 讲义在这里特别标注了一句：**决定最优 $m$ 的是「最优臂与第二好臂之间的间隙」**。

代入后

$$
R_n\ \lesssim\
\left\lceil\frac{4\log n}{\min_{j\ne1}\Delta_j^2}\right\rceil
\cdot\sum_{i=2}^{k}\Delta_i
\;+\;(\text{与 } n \text{ 无关的小项}) .
$$

**这就是 ETC 的病根**：$\min_j\Delta_j^2$ 是「最难分辨的那一对」的间隙。只要有一个臂和最优臂几乎一样好（$\min\Delta_j\to0$），$m$ 就会爆炸——**所有 $k$ 个臂都得陪着它一起被探 $m$ 次**，包括那些一眼就能看出很差的臂。

### 2.7 于是有了三个要修的点

讲义第 6 页把它们列成一张清单，这也正是 UCB 的设计目标：

1. **不需要知道 $\Delta$。** ETC 的最优 $m$ 里含 $\Delta$，可 $\Delta$ 正是我们想知道的——这是循环依赖。
2. **不同臂应该有不同探索次数**，按 $\Delta_i$ 分配，而不是一律 $m$ 次。
3. **避免探索/利用的突变切换**。ETC 在 $t=mk$ 那一轮从「轮转」直接跳到「永远同一个臂」，前面探到的信息在切换后就再也不更新了。

---

## 3. UCB：用「置信上界」替掉「已知的 $\Delta$」

### 3.1 核心原则：乐观面对不确定性

UCB 的出发点是 **optimism in the face of uncertainty**（面对不确定性时保持乐观）。

> 每一轮，给每个臂算一个分数 **UCB index**，它在我们已观测的数据下、以高概率**不低于**该臂的真实均值；然后选分数最高的那个臂。

一个「被高估但还没试够」的臂，分数自然高；一旦把它试够了，置信区间收窄，分数落回真值附近，它就不再被选。**探索量因此自动由数据决定，不需要事先算 $m$。**

index 的结构非常直白：

$$
\text{UCB 指数}
=\underbrace{\hat\mu_i(t)}_{\text{平均奖励}}
+\underbrace{\text{exploration bonus}}_{\text{探索奖励，随 }T_i\text{ 递减}}
$$

- 平均奖励：到目前为止这个臂看起来有多好；
- 探索奖励：**采样越少，奖励越大**（a decreasing function of $T_i$）。

两项一加，就同时编码了「现在选它好不好」和「还没试够，值不值得再试」。

### 3.2 置信界从哪来

讲义给的是标准的次高斯/Hoeffding 型单边界。设 $X_1,\dots,X_n$ 独立、1-sub-Gaussian、均值 $\mu$，$\hat\mu=\frac1n\sum X_t$，则对任意 $\delta\in(0,1)$：

$$
\boxed{
P\!\left(\hat\mu+\sqrt{\frac{2\log(1/\delta)}{n}}\;>\;\mu\right)\ \ge\ 1-\delta
}
$$

三项的含义：$\hat\mu$ 是 $n$ 个样本的经验平均；根号那一项是为了**高估**真值而加的余量；右边是「该臂真实均值低于这个上界」的概率至少 $1-\delta$。

#### 补：这个式子是怎么来的

（讲义直接给了结论，这里补三行推导——只需要上一篇 §5.1 那条次高斯尾界。）

1-sub-Gaussian 的样本均值满足单边 Hoeffding 不等式：

$$
P\left(\hat\mu-\mu\ \ge\ t\right)\ \le\ e^{-\frac{nt^2}{2}} .
$$

我们希望右边等于 $\delta$，反解出 $t$：

$$
e^{-\frac{nt^2}{2}}=\delta
\iff
\frac{nt^2}{2}=\log\frac1\delta
\iff
t=\sqrt{\frac{2\log(1/\delta)}{n}} .
$$

于是「$\hat\mu$ 加上 $t$ 之后仍低于 $\mu$」的概率最多 $\delta$，等价地：

$$
P\left(\hat\mu+\sqrt{\frac{2\log(1/\delta)}{n}}>\mu\right)\ge 1-\delta .
$$

**三个值得注意的点**：

- $t$ 里 $n$ 在分母上——**样本越多，余量越小**，这正是「置信区间随采样收缩」的代数体现；
- $\log(1/\delta)$ 出现在分子：要求更高的把握（更小的 $\delta$），余量按 $\sqrt{\log(1/\delta)}$ 增长，**不是**按 $1/\delta$ 增长——对数惩罚很便宜；
- 反过来看，固定余量 $t$ 时需要的样本数是 $n\approx 2\log(1/\delta)/t^2$，**与 $t^2$ 成反比**。这就是后面 $16\log n/\Delta_i^2$ 的雏形。

于是臂 $i$ 被选过 $T_i$ 次时，取

$$
\boxed{
\mathrm{UCB}_i=\hat\mu_i+\sqrt{\frac{2\log(1/\delta)}{T_i}}
}
$$

这个 index 就有至少 $1-\delta$ 的概率是真实均值的上界。

### 3.3 为什么取 $\delta=\dfrac{1}{n^2}$

单轮保证不够——我们要的是**所有臂、所有轮次**都成立。讲义的处理是取一个足够小的 $\delta$：

$$
\delta=\frac{1}{n^2}
\quad\Longrightarrow\quad
\sqrt{\frac{2\log(1/\delta)}{T_i}}
=\sqrt{\frac{4\log n}{T_i}}
$$

$$
\boxed{
\mathrm{UCB}_i(t-1)=\hat\mu_i(t-1)+\sqrt{\frac{2\log(1/\delta)}{T_i(t-1)}}
\ \approx\ \hat\mu_i(t-1)+\sqrt{\frac{4\log n}{T_i(t-1)}}
}
$$

#### 补：为什么要 $1/n^2$——并集界

（讲义只说「small enough」，这里把它补成可算的。）

每个臂、每一轮都有一次「index 没盖住真值」的坏事件。要保证**一次都不出错**，需要对所有坏事件取并集：

$$
P\left(\bigcup_{t=1}^{n}\bigcup_{i=1}^{k}E_{t,i}\right)
\ \le\ \sum_{t=1}^{n}\sum_{i=1}^{k}P(E_{t,i})
\ \le\ nk\,\delta .
$$

（第一个不等号就是**并集界 / union bound**：多个事件至少发生一个的概率，不超过各自概率之和。）

代入 $\delta=1/n^2$：

$$
nk\cdot\frac{1}{n^2}=\frac{k}{n}.
$$

也就是说：**以至少 $1-k/n$ 的概率，所有臂在所有轮次的 index 都是真值的上界**。$k$ 是常数，于是 $k/n\to0$——总失败概率随 $n$ 收敛到 0。

几个细节：

- 若想更干净，取 $\delta=\dfrac{1}{kn^2}$，总量就是 $1/n$；再取 $\dfrac{1}{2kn^2}$ 还能把 $\log(1/\delta)$ 写成 $\log n+\log(2k)$。这些常数差别不影响阶，讲义只用「small enough」带过。
- 并集界的代价是**保守**：它假设所有坏事件互斥，实际往往重叠，所以真实失败概率比上界小得多。这也是 UCB 常数偏大的一个来源。
- $\delta$ 越小 → 余量越大 → 探索越多。所以「取小 $\delta$」不是免费的，它换来的是**保证**，付出的是常数。

### 3.4 算法

```text
1: Input k（臂数）和 δ（如 δ = 1/n²）
2: for t = 1, …, n
3:     A_t = argmax_i UCB_i(t-1, δ)
4:     观测 X_t，更新 UCB 指数
         （只需更新「刚被选中的那个臂」的指数）
5: end for
```

```text
其中  UCB_i(t-1, δ) = μ̂_i(t-1) + sqrt( 2·log(1/δ) / T_i(t-1) )
```

**边界条款**：若 $T_i(t-1)=0$（这个臂还一次都没被选过），则 $\mathrm{UCB}_i=\infty$。

> 这条让**每个臂至少在开头被选一次**。实现时通常要显式写出来：前 $k$ 轮每个臂各选一次，从 $t=k+1$ 起才真正按 index 选。

---

## 4. UCB 为什么有效

### 4.1 直觉：置信区间会窄下去

第 9 页的图（三臂）把三样东西画在一起：

- 每个臂的**经验均值** $\hat\mu_i$；
- 它上面的**置信区间**（误差棒），宽度随样本数增加而变窄；
- 最高那根棒的顶端就是 **UCB index**。

选臂 = 选「棒子顶端最高」的臂。一个臂的样本越多，棒子越短；短到一定程度，它就不再被选中。

![三个臂的经验均值、置信区间与 UCB 上界的一端快照](/images/bandit-figures/ucb-intervals.png)

*看图要点*（一张图把 UCB 的机制全画完了）：

1. **黑点是经验均值** $\hat\mu_i$——算法目前对每个臂的估计；
2. **浅蓝竖条是置信区间**：宽度 $\propto 1/\sqrt{T_i}$，样本越多越窄。三个臂的 $T_i=400/150/40$，宽度差别一眼可见；
3. **红色倒三角是 UCB index**，即区间**上端**。选臂只看这个三角的高低，不看黑点；
4. 于是 `arm 3` 虽然黑点最低（0.405），但样本只有 40 个、区间很宽，**上端反而最高**——它会被再试一次。这就是「乐观」的全部内容；
5. **绿色虚线是真实均值**，算法看不到。注意 `arm 2` 的经验均值 $(0.61)$ 恰好高估了真实值 $(0.55)$，而它的区间仍然盖住了真值——这正是置信区间的意义：**估计可以错，但区间大概率不会漏**。

随着轮次推进，`arm 3` 的区间窄下去、倒三角落到可能均值以下，它就不再被选；`arm 1` 与 `arm 2` 会继续交替，直到 $\Delta_2=0.05$ 也被区分开。

### 4.2 次优臂什么时候停止被选

设 $i$ 是次优臂，$\mu_{i^*}=\mu_i+\Delta_i$。它被选的条件是

$$
\mathrm{UCB}_i\ \ge\ \mathrm{UCB}_{i^*}\ \approx\ \mu_{i^*} .
$$

所以只要

$$
\boxed{\mathrm{UCB}_i-\mu_i<\Delta_i}
$$

也就是**臂 $i$ 的置信区间半宽小于 $\Delta_i$** 时，它就不可能再被选中了。

### 4.3 定量：$T_i\ge\dfrac{16\log n}{\Delta_i^2}$

用 $\delta=1/n^2$ 的 index，置信区间的**全宽**是

$$
\mathrm{UCB}_i-\mathrm{LCB}_i=2\sqrt{\frac{4\log n}{T_i}} .
$$

要求它不超过 $\Delta_i$：

$$
2\sqrt{\frac{4\log n}{T_i}}\le\Delta_i
\iff
\sqrt{\frac{4\log n}{T_i}}\le\frac{\Delta_i}{2}
\iff
\frac{4\log n}{T_i}\le\frac{\Delta_i^2}{4}
$$

$$
\boxed{
T_i\ \ge\ \frac{16\log n}{\Delta_i^2}
}
$$

于是得到一个非常干脆的结论：

> **UCB 算法选中次优臂 $i$ 的次数不超过 $\dfrac{16\log n}{\Delta_i^2}$。**

对比一下 ETC：它需要

$$
\frac{4\log n}{\min_{j\ne1}\Delta_j^2}
$$

个样本——**取决于最小间隙**，而且每个臂都一样多。

$$
\text{ETC}: \frac{1}{\min_j\Delta_j^2}
\qquad\text{vs.}\qquad
\text{UCB}: \frac{1}{\Delta_i^2}\ \text{（逐臂）}
$$

### 4.4 一句话记住这套机制

> **每一次「错误」都在让它下次更不可能发生。**
>
> 选了次优臂 $\to$ 它的样本多了 $\to$ 它的置信区间窄了 $\to$ 它再压过最优臂的机会小了。
>
> 而 ETC 的探索期是一次性投入、承诺期永不更新——它没有这个自我纠正的回路。

顺着这条线，还能得到讲义强调的那个比例关系：

> 间隙 $\Delta_i$ 越大，被选次数越少，且**与 $1/\Delta_i^2$ 成比例**。

---

## 5. UCB 的 regret 定理

$$
\boxed{
\text{Theorem（}\delta=\tfrac{1}{n^2}\text{）}:\quad
R_n\ \le\ \sum_{i:\,\Delta_i>0}\frac{16\log n}{\Delta_i}
\ =\ O(\log n)
}
$$

推导只有一步：把 §4.3 的「选中次数 $\le 16\log n/\Delta_i^2$」代回 regret 分解公式，每次被选付 $\Delta_i$：

$$
R_n=\sum_i \Delta_i\,\mathbb E[T_i(n)]
\ \le\ \sum_{i:\Delta_i>0}\Delta_i\cdot\frac{16\log n}{\Delta_i^2}
=\sum_{i:\Delta_i>0}\frac{16\log n}{\Delta_i}.
$$

### 和 ETC 的结构差异（这才是重点）

| | ETC（最优 $m$） | UCB |
|---|---|---|
| regret | $O\!\left(\frac{\log n}{\Delta_{\min}}\cdot k\right)$ 量级 | $O\!\left(\sum_i \frac{\log n}{\Delta_i}\right)$ |
| 次优臂被选次数 | $\approx \frac{4\log n}{\Delta_{\min}^2}$（**所有臂一律**） | $\le \frac{16\log n}{\Delta_i^2}$（**逐臂**） |
| 要不要知道 $\Delta$ | **要**（否则 $m$ 没法调） | 不要 |
| 探索/利用切换 | 突变，切换后不再更新 | 每轮都在更新，平滑过渡 |
| 常数 | — | 16；换更紧的 index 可降到 **2** |

> **常数从 16 降到 2**：讲义只说「by using a different and tighter UCB index」。常见做法是更紧的经验 Bernstein 型 bonus，或者把 $\log(1/\delta)$ 里的并集界算得更精细（补充，非讲义内容）。

---

## 6. 实测对比（$k=2$）

先看一个 $k=3$ 的对照实验（我自己跑的，不是讲义内容），三种策略用同样的预算：

![贪心、ETC 与 UCB1 的累积 regret 曲线：两条直线 vs 一条弯曲线](/images/bandit-figures/regret-curves.png)

*看图要点*（$\mu=(0.60,0.45,0.25)$，$n=8000$，200 次平均）：

- **贪心**（紫）和 **ETC**（蓝）都是**近似直线**。原因不同：贪心一旦被早期运气骗住就再也不回头；ETC 则是承诺之后就停止学习——押错就一直错。两者的斜率都近似「错误率 × 间隙」，这正是 §4.4 里「常数错误率 → 线性 regret」的图形版本；
- **UCB1**（红）是**一条弯下去的曲线**：前 1000 轮它也要交学费（三条线挤在一起），之后探索量随 $\hat\mu_i$ 的收敛自动减少，斜率持续变缓。这就是 $\log$ 级 regret 的样子——**不是不涨，是越涨越慢**；
- 注意 ETC 在 $t<1000$ 时**比 UCB 低**：它只花 60 轮就完成了探索。这说明「log 级」是渐近性质，短视界内固定预算的探索反而更划算——和第 13 页那条「最优调参的 ETC 有时小幅赢过 UCB」的结论一致。

下面是讲义原图（$k=2$，横轴是间隙 $\Delta$ 而不是轮数）：

第 13 页给了 $k=2$、次优臂间隙为 $\Delta$ 时，**期望 regret 随 $\Delta$ 的变化**：

- 曲线：ETC 取 $m=25,50,75,100$ 四条，加上 **ETC (optimal m)** 和 **UCB**；
- 横轴 $\Delta$，纵轴 expected regret。

读图要点：

1. **ETC 的每条曲线都有一个「先升后降」的鼓包**。原因在图上那行注记：
   $$
   \text{Regret}\le\min\left\{n\cdot\Delta,\ \frac{4\log n}{\Delta}\right\}
   $$
   $\Delta$ 很小时，$4\log n/\Delta$ 主导（分辨不出，只能一直错）；$\Delta$ 大时，$n\Delta$ 主导但……其实这时探索反而更划算。中间那段（$\Delta$ 中等）是 ETC 最难受的区域。
2. **$m$ 取大了/取小了都会有一条曲线长期吃亏**，只有 optimal $m$ 那条贴着下包络——而 optimal $m$ **需要知道 $\Delta$**（图注：Requires knowledge of $\Delta$）。
3. **UCB 不需要 $\Delta$**，却在整段 $\Delta$ 上都贴着下包络走。

讲义的结论（第 13 页）说得很克制：

- 如果按每个 $\Delta$ 单独把 $m$ 调到最优，**ETC 能小幅赢过 UCB**；
- 但这只在 $k=2$ 时成立；
- **$k$ 一般、且 $\min_j\Delta_j$ 很小时，即使 $m$ 调到最优，ETC 也会输给 UCB**（因为 ETC 的探索量被最小间隙绑死）；
- 存在 UCB 的变体，**连最优调参的 ETC 都能赢**。

---

## 7. 公式速查

| 名称 | 公式 |
|---|---|
| 次优间隙 | $\Delta_i=\mu^*-\mu_i$，$\Delta_{a^*}=0$ |
| ETC 的总 regret | $R_n=m\sum_i\Delta_i+(n-mk)\sum_i\Delta_iP(\text{承诺到 }i)$ |
| ETC 的界 $(\star\star)$ | $R_n\le m\sum_{i\ge2}\Delta_i+(n-mk)\sum_{i\ge2}\Delta_i e^{-m\Delta_i^2/4}$ |
| 单臂概率界 | $P(\hat\mu_i\ge\max_{j\ne i}\hat\mu_j)\le e^{-m\Delta_i^2/4}$ |
| 最优 $m$（$k=2$） | $\lceil 4\log n/\Delta^2\rceil$ |
| 最优 $m$（一般 $k$） | $\lceil 4\log n/\min_{j\ne1}\Delta_j^2\rceil$ |
| ETC 的 regret | $R_n\le 4\log n/\Delta+2\Delta=O(\log n)$ |
| 置信界 | $P\!\left(\hat\mu+\sqrt{\tfrac{2\log(1/\delta)}{n}}>\mu\right)\ge1-\delta$ |
| UCB index | $\hat\mu_i+\sqrt{\tfrac{2\log(1/\delta)}{T_i}}$，取 $\delta=1/n^2$ 得 $\sqrt{\tfrac{4\log n}{T_i}}$ |
| 边界 | $T_i=0\Rightarrow \mathrm{UCB}_i=\infty$ |
| 停止判据 | $\mathrm{UCB}_i-\mu_i<\Delta_i$ |
| 选中次数界 | $T_i\ge 16\log n/\Delta_i^2$ |
| UCB 的 regret | $R_n\le\sum_{i:\Delta_i>0}\frac{16\log n}{\Delta_i}=O(\log n)$ |

---

## 8. 术语对照

| English | 中文 | 备注 |
|---|---|---|
| exploration / exploitation | 探索 / 利用 | |
| commit phase | 承诺阶段 | ETC 的第二段 |
| sub-optimality gap | 次优间隙 | $\Delta_i$ |
| regret | 遗憾 | 相对事后最优固定臂 |
| regret decomposition | 遗憾分解 | 按臂求和 |
| upper confidence bound (UCB) | 置信上界 | 本讲主角 |
| confidence interval | 置信区间 | 宽度 $\propto 1/\sqrt{T_i}$ |
| exploration bonus | 探索奖励 | index 的第二项 |
| optimism in the face of uncertainty | 面对不确定性保持乐观 | UCB 的核心原则 |
| index | 指数 / 打分 | 每轮给每个臂算的分 |
| tune | 调参 | 如调 $m$ |
| horizon | 时间跨度 | $n$ |
| union bound | 并集界 | 让 $\delta$ 对所有臂/轮次同时成立 |
| sub-Gaussian | 次高斯 | 置信界的前提 |

---

## 9. 六个容易踩的坑

1. **$(\star\star)$ 的求和从 $i=2$ 开始**，是因为讲义把最优臂编成了 1 号；写成 $\sum_{i:\Delta_i>0}$ 才不会漏或多。
2. **$m$ 是「每个臂」的次数，不是总探索轮数**；总探索轮数是 $mk$。
3. **承诺期的 regret 是 $(n-mk)\Delta_i$，不是 $n\Delta_i$**——探索期已经单独算过了，别重复计。
4. **UCB 的 bonus 用的是 $T_i$（这个臂被选过几次），不是 $t$**。用 $t$ 就成了对所有臂加同一个常数，探索性会消失（严格说仍会探索，但不再「少的更该试」）。
5. **$T_i=0$ 必须处理成 $\infty$**，否则分子分母都为零或 bonus 无定义；实现上就是「前 $k$ 轮各选一次」。
6. **$16\log n/\Delta_i^2$ 是「次数」，不是 regret**；乘上 $\Delta_i$ 才变成 regret，所以最终界里是 $1/\Delta_i$ 而不是 $1/\Delta_i^2$。

---

## 10. 一页纸记忆版

```text
ETC：探索 mk 轮（每臂 m 次）→ 锁定经验均值最高的臂
      Rn ≤ m·ΣΔi + (n−mk)·ΣΔi·e^{−mΔi²/4}
      最优 m = ⌈4 log n / Δ²⌉  ⇒  Rn ≤ 4 log n/Δ + 2Δ = O(log n)
      病根：① m 依赖未知的 Δ   ② 每臂都探 m 次   ③ 切换后不再更新

UCB：每轮选 argmax[ μ̂i + sqrt(2 log(1/δ)/Ti) ]，δ = 1/n² ⇒ bonus = sqrt(4 log n/Ti)
      Ti = 0 → index = ∞（先各试一次）
      次优臂在 Ti ≥ 16 log n / Δi² 后不再被选
      ⇒ Rn ≤ Σ_{Δi>0} 16 log n / Δi = O(log n)，且逐臂自适应

一句话：ETC 的探索是「预算」，UCB 的探索是「好奇心」——试得越少越想知道。
```

> 这一讲真正完成的动作，是把「探索/利用」从一个**需要人为设定的参数 $m$**，变成**由数据自动决定的量**。代价是多了一个 $\log$ 项和一套置信界；收益是**不再需要知道 $\Delta$**——而在真实问题里，$\Delta$ 恰恰是我们最不知道的东西。

---

## 11. 手稿原页

十三页手写讲义的完整扫描，按原顺序排列。正文提到「原页 $N$」时，指的就是这一节的第 $N$ 张。

**原页 1 · ETC 伪代码与探索期**

![Lecture 4 第 1 页：Explore-Then-Commit 算法与 k=5、m=3 的轮转](/images/from-etc-to-ucb/p01.jpg)

**原页 2 · 承诺期例子与 regret 分解**

![Lecture 4 第 2 页：commit 阶段的动作序列、regret 分解公式与探索期 regret](/images/from-etc-to-ucb/p02.jpg)

**原页 3 · 间隙 $\Delta_i$ 与承诺期的分段 regret**

![Lecture 4 第 3 页：Δi 的定义与承诺期 regret 的分段写法](/images/from-etc-to-ucb/p03.jpg)

**原页 4 · 总 regret 与概率界**

![Lecture 4 第 4 页：Rn 的两项分解、e 的负 mΔ²/4 次方上界与探索-利用权衡](/images/from-etc-to-ucb/p04.jpg)

**原页 5 · 最优 $m$ 与一般 $k$ 的界**

![Lecture 4 第 5 页：m=⌈4log n/Δ²⌉、Rn≤4log n/Δ+2Δ，以及任意 k 的版本](/images/from-etc-to-ucb/p05.jpg)

**原页 6 · UCB 的三个改进目标与 index 结构**

![Lecture 4 第 6 页：不需要知道 Δ、按臂分配探索、避免突变；乐观原理与 index 的两项](/images/from-etc-to-ucb/p06.jpg)

**原页 7 · 置信界与 $\delta$ 的取法**

![Lecture 4 第 7 页：Hoeffding 型单边界、置信区间图与 δ=1/n² 的选择](/images/from-etc-to-ucb/p07.jpg)

**原页 8 · UCB 算法伪代码**

![Lecture 4 第 8 页：UCB 算法与 Ti=0 时 index 取 ∞ 的处理](/images/from-etc-to-ucb/p08.jpg)

**原页 9 · 三臂示例：置信区间与上界**

![Lecture 4 第 9 页：三臂的经验均值、置信区间与 UCB 上界](/images/from-etc-to-ucb/p09.jpg)

**原页 10 · 为什么有效**

![Lecture 4 第 10 页：UCB_i−μ_i<Δ_i 的停止判据与 Ti≥16log n/Δi² 的结论](/images/from-etc-to-ucb/p10.jpg)

**原页 11 · index 与置信区间的演化**

![Lecture 4 第 11 页：三个臂的置信区间随采样收缩的演示](/images/from-etc-to-ucb/p11.jpg)

**原页 12 · UCB 的 regret 定理**

![Lecture 4 第 12 页：Rn≤Σ16log n/Δi 以及与 ETC 的结构对比](/images/from-etc-to-ucb/p12.jpg)

**原页 13 · 与 ETC 的性能对比**

![Lecture 4 第 13 页：k=2 时期望 regret 随间隙 Δ 变化的对比曲线](/images/from-etc-to-ucb/p13.jpg)

