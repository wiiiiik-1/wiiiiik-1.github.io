# 图解生成

系列笔记里的示意图和模拟曲线都用 `make-figures.py` 画，配色跟站点一致（米白纸底、墨色、朱砂 `#b23a2b`）。图是**生成的**，不是从讲义里裁的，所以改参数、改配色都能重跑。

## 跑起来

```bash
python -m pip install -r scripts/figures/requirements.txt
python scripts/figures/make-figures.py
```

输出写到 `public/images/bandit-figures/`，也就是文章里 `/images/bandit-figures/xxx.png` 引用的位置。

常用参数：

```bash
python scripts/figures/make-figures.py --out .figs       # 先写草稿目录，比对满意再覆盖
python scripts/figures/make-figures.py --only one-over-t # 只重画一张
python scripts/figures/make-figures.py --lang en         # 强制英文标注
python scripts/figures/make-figures.py --trials 5000     # 曲线更平滑（也就几秒）
```

| 参数 | 说明 |
|---|---|
| `--out` | 输出目录，默认 `public/images/bandit-figures` |
| `--only` | 只画指定图，可重复；取值见下表 slug |
| `--lang` | `auto`（默认）/ `zh` / `en` |
| `--trials` | 蒙特卡洛次数，默认 2000 |
| `--seed` | 随机种子，默认 11 |

中文标注需要系统里有中文字体：Windows 用微软雅黑或黑体，macOS 用苹方，Linux 装 Noto CJK。一个都没有时脚本自动退回英文标注（图照样能出，只是标签变英文），不会画成方框。

## 十二张图分别在哪、想说明什么

| slug | 文件 | 用在 | 想说明的一件事 |
|---|---|---|---|
| `arms` | `arms-gaps.png` | 导论 §3、3b §3.4 | 间隙 $\Delta_a$ 就是两条密度曲线中心之间的距离；重叠越多越难分辨 |
| `one-over-t` | `one-over-t.png` | 3b §4.4 | 曲线下面积：$\sum 1/t\approx\ln n$，常数错误率的面积是线性 |
| `etc-timeline` | `etc-timeline.png` | 4b §1 | 探索期锯齿（与奖励无关）+ 承诺期水平线，中间是 $t=mk$ 的硬切换 |
| `etc-vs-m` | `etc-regret-vs-m.png` | 4b §2.5 | 界对 $m$ 是 U 形；数值最小点与闭式解 $4\ln n/\Delta^2$ 不重合 |
| `ucb-intervals` | `ucb-intervals.png` | 4b §4.1 | 经验均值、置信区间、index、真值四层关系；样本少的臂 index 被抬高 |
| `regret-curves` | `regret-curves.png` | 4b §6 | 贪心/ETC 近似直线，UCB 弯下去（前 1000 轮 UCB 并不占优） |
| `etc-vs-gap` | `etc-ucb-vs-gap.png` | 5 §1.5 | 固定 $m$ 的 ETC 只在某段 $\Delta$ 上好；把 UCB 的常数从 4 换成 2，曲线整体掉下来 |
| `policy-loss` | `policy-loss.png` | 5 §2.1 | 「被支配」= 处处更高；可容许 = 各有一段最好 |
| `bayes-bag` | `bayes-bag.png` | 5 §3.1 | 黑球一步排除、白球只把 1/2 推到 2/3 |
| `ts-sampling` | `ts-sampling.png` | 5 §4.2 | 后验均值低的臂也能赢下一次抽样——探索来自随机化 |
| `posterior-shrink` | `posterior-shrink.png` | 5 §4.4 | 后验方差 $\propto1/T$，越采越窄 |
| `ts-vs-ucb` | `ts-vs-ucb.png` | 5 §5.3 | TS 全程低于 UCB1，但 10–90 分位很宽（方差大） |

（3b = `multi-armed-bandits-intro`，4b = `from-etc-to-ucb`，5 = `thompson-sampling`。）

## 关于「可复现」

- 所有随机实验都有固定种子，同一台机器、同一套依赖下重跑，得到**逐像素相同**的图；
- PNG 的 `Software` 元数据写死成 `lecturn/make-figures.py`，不写 matplotlib 版本号，所以重跑连字节都一样；
- 换 matplotlib 版本后像素可能有细微差别（字体度量、抗锯齿策略会变），这属于正常，正文结论不受影响。

### 为什么 `regret-curves` 用 2000 次蒙特卡洛

其它五张图都是解析或示意，只有这张要跑模拟。**ETC 的曲线高度由「有没有押错臂」这种稀有事件决定**——一次押错就多亏 $(n-mk)\Delta$，约 1190。200 次平均时，多押错一两次就能让 ETC 的位置差一倍（同一份代码换个种子，8000 轮处可能是 150，也可能是 350），看起来甚至和贪心一样差。

所以这张图改成 numpy 并排推进 2000 条轨迹（8 秒左右跑完），并排推进比逐条跑 Python 循环快两个数量级。三个种子下 8000 轮处的终值：

```text
seed=11   greedy=412.3   etc=174.0   ucb=107.2
seed=12   greedy=453.7   etc=167.8   ucb=107.7
seed=13   greedy=447.2   etc=178.9   ucb=107.5
```

同一张图现在只需要一次渲染：跑 `--trials 200` 会明显更抖，那是采样噪声，不是策略差异。

## 没采用的图

还写过一张「regret 上界随间隙 $\Delta$ 变化」的 log-log 图，但讲义第 13 页已经用一张图讲完了同一件事，放进来只是重复，就删掉了。需要时可以从 git 历史里找回（提交 `08844ee` 之前）。
