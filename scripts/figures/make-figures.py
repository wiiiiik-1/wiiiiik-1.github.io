#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 bandits 系列笔记里的图解（Ink & Paper 配色，输出 PNG）。

用法（在仓库根目录执行）：

    python scripts/figures/make-figures.py                # 覆盖 public/images/bandit-figures/
    python scripts/figures/make-figures.py --out .figs    # 先写到草稿目录看效果
    python scripts/figures/make-figures.py --only one-over-t
    python scripts/figures/make-figures.py --lang en      # 强制英文标注

依赖：matplotlib + numpy（见同目录 requirements.txt）。
中文标注需要系统里有中文字体（Windows 微软雅黑 / 黑体，macOS 苹方，Linux Noto CJK）；
一个都找不到时自动退回英文标注，图仍然能生成。

所有随机实验都用固定种子，同一台机器、同一套依赖下重跑得到同样的图。
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "public" / "images" / "bandit-figures"

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import FancyArrowPatch  # noqa: E402

# ---------------------------------------------------------------- 配色
PAPER = "#f7f2e8"
INK = "#2b2b2b"
GRID = "#ddd5c6"
VERM = "#b23a2b"
BLUE = "#2f5d8a"
GREEN = "#3f6b52"
PURPLE = "#6b4a7a"
GOLD = "#a8812c"

FONT_CANDIDATES = [
    # Windows
    r"C:/Windows/Fonts/msyh.ttc",
    r"C:/Windows/Fonts/msyhbd.ttc",
    r"C:/Windows/Fonts/simhei.ttf",
    # macOS
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    # Linux（Noto CJK 常见安装位置）
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJKsc-Regular.otf",
]

CN = False  # 是否可用中文标注；main() 里探测


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "axes.edgecolor": "#9a9285",
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": "#5a544a",
            "ytick.color": "#5a544a",
            "axes.grid": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "axes.axisbelow": True,
            "font.size": 10.5,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "legend.frameon": False,
            "savefig.dpi": 200,
        }
    )


def enable_chinese() -> bool:
    """注册一个中文字体；成功返回 True。"""
    for cand in FONT_CANDIDATES:
        if not os.path.exists(cand):
            continue
        try:
            font_manager.fontManager.addfont(cand)
            plt.rcParams["font.family"] = font_manager.FontProperties(fname=cand).get_name()
            return True
        except Exception:  # 字体损坏或不被支持，继续试下一个
            continue
    return False


def t(cn: str, en: str) -> str:
    """有中文字体用中文，否则用英文（避免方框乱码）。"""
    return cn if CN else en


SAVED: list[Path] = []


def save(fig, out_dir: Path, name: str) -> None:
    fig.tight_layout()
    path = out_dir / name
    # 指定 Software 元数据：PNG 里就不写 matplotlib 版本号，重跑更容易得到同样的字节
    fig.savefig(path, bbox_inches="tight", metadata={"Software": "lecturn/make-figures.py"})
    plt.close(fig)
    SAVED.append(path)
    print(f"  {name:<22} {path.stat().st_size / 1024:6.0f} KB")


# ---------------------------------------------------------------- 图 1：臂的分布与间隙
def fig_arms(out_dir: Path) -> None:
    """三个高斯臂的密度曲线 + 最优均值线 + 间隙标注。

    用来说明 Δ_a 到底是什么：两条曲线中心之间的距离。
    """
    x = np.linspace(0, 1.75, 700)
    means = [1.0, 0.70, 0.40]
    sig = 0.20
    colors = [VERM, BLUE, GREEN]
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for i, (m, c) in enumerate(zip(means, colors)):
        y = np.exp(-0.5 * ((x - m) / sig) ** 2) / (sig * math.sqrt(2 * math.pi))
        ax.plot(x, y, color=c, lw=2.0, label=f'{t("臂", "arm")} {i + 1}  ($\\mu$={m:.2f})')
        ax.fill_between(x, y, color=c, alpha=0.10)

    mu_star = max(means)
    ax.axvline(mu_star, color=INK, ls=(0, (4, 3)), lw=1.2)
    ax.annotate(r"$\mu^*$ " + t("（最优均值）", "(best mean)"), xy=(mu_star, 1.72),
                xytext=(mu_star + 0.02, 1.78), fontsize=10.5, color=INK)

    for i, (m, c) in enumerate(zip(means[1:], colors[1:])):
        y0 = 0.10 + 0.13 * i
        ax.add_patch(FancyArrowPatch((m, y0), (mu_star, y0), arrowstyle="<|-|>",
                                     mutation_scale=9, color=c, lw=1.1))
        ax.text((m + mu_star) / 2, y0 + 0.035, rf"$\Delta_{{{i + 2}}}={mu_star - m:.2f}$",
                ha="center", color=c, fontsize=10,
                bbox=dict(boxstyle="round,pad=0.15", fc=PAPER, ec="none", alpha=0.85))

    ax.set_xlabel(t("奖励值 / 平均奖励", "reward / mean reward"))
    ax.set_ylabel(t("概率密度（示意）", "density (schematic)"))
    ax.set_title(t("三个臂的奖励分布、最优均值与次优间隙",
                   "Three arms: reward distributions, best mean and gaps"))
    ax.set_ylim(0, 2.05)
    ax.legend(loc="upper left", fontsize=9.5)
    save(fig, out_dir, "arms-gaps.png")


# ---------------------------------------------------------------- 图 2：三种策略的累积 regret
def _simulate_curves(mu, n: int, trials: int, etc_m: int, seed: int) -> dict[str, np.ndarray]:
    """把 trials 条轨迹并排推进，返回三种策略各自的平均累积 regret 曲线。

    为什么用 numpy 并排跑而不是逐条跑 Python 循环：ETC 曲线的高度取决于
    「有没有押错臂」这种稀有事件（一次押错就多亏 (n−mk)·Δ），200 次平均的方差大到
    能让 ETC 看起来和贪心一样差。并排推进快两个数量级，才敢把 trials 提到 2000。
    """
    mu = np.asarray(mu, dtype=float)
    k, best = len(mu), float(mu.max())
    rows = np.arange(trials)
    curves: dict[str, np.ndarray] = {}

    for policy in ("greedy", "etc", "ucb"):
        rng = np.random.default_rng(seed)  # 每条策略用独立的随机流
        counts = np.zeros((trials, k), dtype=np.int64)
        sums = np.zeros((trials, k))
        acc = np.zeros(trials)
        curve = np.empty(n)
        committed = np.full(trials, -1)
        for step in range(1, n + 1):
            mean_hat = sums / np.maximum(counts, 1)  # 用上一轮为止的样本
            if policy == "etc":
                if step <= etc_m * k:  # 探索期：轮转，不看奖励
                    a = np.full(trials, (step - 1) % k)
                else:  # 承诺期：第一次到这里时按经验均值定死
                    todo = committed < 0
                    if todo.any():
                        committed[todo] = np.argmax(mean_hat[todo], axis=1)
                    a = committed
            else:
                if policy == "greedy":
                    idx = np.argmax(mean_hat, axis=1)
                else:  # UCB1
                    idx = np.argmax(mean_hat + np.sqrt(2.0 * np.log(step) / np.maximum(counts, 1)), axis=1)
                a = np.where(step <= k, step - 1, idx)  # 前 k 轮每臂先试一次
            reward = (rng.random(trials) < mu[a]).astype(float)
            counts[rows, a] += 1
            sums[rows, a] += reward
            acc += best - mu[a]
            curve[step - 1] = acc.mean()
        curves[policy] = curve
    return curves


def fig_regret_curves(out_dir: Path, trials: int = 2000, seed: int = 11) -> None:
    """贪心 / ETC / UCB1 的累积 regret 曲线。

    μ 取 (0.60, 0.45, 0.25)：三个臂差别足够大，才能在 8000 轮里看出
    「直线 vs 弯线」。(0.50, 0.45, 0.35) 这种接近的取值会让三条线几乎重合。
    """
    mu = [0.60, 0.45, 0.25]
    k, n, etc_m = len(mu), 8000, 20
    curves = _simulate_curves(mu, n, trials, etc_m, seed)

    specs = [
        ("greedy", PURPLE, t("贪心（先各试一次）", "greedy")),
        ("etc", BLUE, f"ETC ($m$={etc_m})"),
        ("ucb", VERM, "UCB1"),
    ]

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    xs = np.arange(1, n + 1)
    for name, color, label in specs:
        ax.plot(xs, curves[name], color=color, lw=2.2 if name == "ucb" else 1.8, label=label)
    ax.set_xlabel(t("轮数 t", "round t"))
    ax.set_ylabel(t("累积 regret $R_t$", "cumulative regret $R_t$"))
    ax.set_title(t(rf"三种策略的累积 regret（$k={k}$, $\mu=(0.60,0.45,0.25)$，{trials} 次平均）",
                   f"Cumulative regret, k={k}, mu=(0.6,0.45,0.25), {trials} runs"))
    ax.legend(loc="upper left")
    save(fig, out_dir, "regret-curves.png")


# ---------------------------------------------------------------- 图 3：ETC 的动作序列
def fig_etc_timeline(out_dir: Path) -> None:
    """每一轮选了哪条臂：探索期锯齿（轮转）+ 承诺期水平线。"""
    k, m, n = 5, 10, 90
    seq = [(i % k) + 1 for i in range(m * k)] + [2] * (n - m * k)
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    ax.axvspan(0.5, m * k + 0.5, color=GOLD, alpha=0.14, lw=0)
    ax.step(range(1, n + 1), seq, where="mid", color=INK, lw=1.4)
    ax.scatter(range(1, m * k + 1), seq[: m * k], s=10, color=BLUE, zorder=3)
    ax.scatter(range(m * k + 1, n + 1), seq[m * k:], s=10, color=VERM, zorder=3)
    ax.axvline(m * k + 0.5, color=VERM, ls=(0, (4, 3)), lw=1.2)
    ax.text(m * k * 0.5, 5.32, t("探索 Exploration（轮转，每臂 m 次）",
                                 "exploration (round-robin, m each)"),
            ha="center", fontsize=10, color="#7a5a1c")
    ax.text(m * k + (n - m * k) * 0.5, 5.32, t("承诺 Commit", "commit"),
            ha="center", fontsize=10, color=VERM)
    ax.set_ylim(0.4, 5.8)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_xlabel(t("轮数 t", "round t"))
    ax.set_ylabel(t("被选中的臂", "arm chosen"))
    ax.set_title(t(r"ETC 的动作序列（$k=5$, $m=10$）", "ETC action sequence (k=5, m=10)"))
    save(fig, out_dir, "etc-timeline.png")


# ---------------------------------------------------------------- 图 4：ETC 的界随 m 变化
def fig_etc_vs_m(out_dir: Path) -> None:
    """界 (★★) 对 m 是 U 形：m 太小押错、m 太大白亏。

    同时标出数值最小点与讲义闭式解 4ln n/Δ²，并说明两者为何不重合。
    """
    n, delta = 10000, 0.2
    ms = np.arange(1, 2400)
    bound = ms * delta + (n - 2 * ms) * delta * np.exp(-ms * delta ** 2 / 4)
    bound = np.maximum(bound, 0)
    m_star = 4 * math.log(n) / delta ** 2
    m_num = int(ms[int(np.argmin(bound))])
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    ax.plot(ms, bound, color=BLUE, lw=2.0, label=t(r"界 $(\star\star)$ 的右端", "the bound"))
    ax.axvline(m_star, color=VERM, ls=(0, (4, 3)), lw=1.2,
               label=t(r"讲义公式 $4\ln n/\Delta^2$", "closed form"))
    ax.axvline(m_num, color=GREEN, ls=(0, (2, 3)), lw=1.4,
               label=t(f"数值最小点 $m\\approx{m_num}$", f"numeric min m={m_num}"))
    ax.set_xlabel(t("每个臂的探索次数 m", "exploration budget m"))
    ax.set_ylabel(t(r"regret 上界 $(\star\star)$", "regret bound"))
    ax.set_title(t(r"ETC 的界随 m 的变化（$k=2$, $\Delta=0.2$, $n=10^4$）",
                   "ETC bound vs m (k=2, delta=0.2, n=1e4)"))
    ax.legend(loc="upper right")
    save(fig, out_dir, "etc-regret-vs-m.png")


# ---------------------------------------------------------------- 图 5：UCB 的置信区间
def fig_ucb_intervals(out_dir: Path) -> None:
    """一轮快照：经验均值、置信区间（宽度 ∝ 1/√T）、UCB index、真实均值。"""
    arms = [
        ("arm 1", 0.60, 0.585, 400),
        ("arm 2", 0.55, 0.610, 150),
        ("arm 3", 0.40, 0.405, 40),
    ]
    ln_t = math.log(200)
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    xs = np.arange(len(arms))
    for i, (_name, mu, mu_hat, T) in enumerate(arms):
        half = math.sqrt(2 * ln_t / T)
        ax.plot([i, i], [mu_hat - half, mu_hat + half], color=BLUE, lw=6, alpha=0.30,
                solid_capstyle="butt")
        ax.scatter([i], [mu_hat], color=INK, s=34, zorder=4)
        ax.scatter([i], [mu_hat + half], marker="v", color=VERM, s=46, zorder=5)
        ax.plot([i - 0.30, i + 0.30], [mu, mu], color=GREEN, ls=(0, (3, 2)), lw=1.3)
        ax.text(i, 0.085, f"$T_i$={T}", fontsize=9, color="#5a544a", ha="center")
    ax.set_xticks(xs)
    ax.set_xticklabels([a[0] for a in arms])
    ax.set_ylabel(t("奖励均值", "mean reward"))
    ax.set_title(t("UCB 的一轮快照：均值、置信区间与上界（示意）",
                   "One round of UCB: means, intervals, upper bounds (schematic)"))
    handles = [
        Line2D([], [], color=INK, marker="o", ls="none", markersize=6,
               label=t(r"经验均值 $\hat\mu_i$", "empirical mean")),
        Line2D([], [], color=BLUE, lw=6, alpha=0.30, label=t("置信区间", "confidence interval")),
        Line2D([], [], color=VERM, marker="v", ls="none", markersize=7,
               label=t("UCB index（区间上端）", "UCB index")),
        Line2D([], [], color=GREEN, ls=(0, (3, 2)), lw=1.3,
               label=t("真实均值（算法看不到）", "true mean (hidden)")),
    ]
    ax.legend(handles=handles, loc="upper left", fontsize=9)
    ax.set_xlim(-0.55, 2.55)
    ax.set_ylim(0.05, 1.02)
    save(fig, out_dir, "ucb-intervals.png")


# ---------------------------------------------------------------- 图 6：1/t 与常数
def fig_one_over_t(out_dir: Path) -> None:
    """「曲线下的面积」：1/t 的积分是 ln n，常数错误率的积分是线性。

    0.128 来自 scripts/sim/etc-worked-example.py 的 20 万次模拟
    （2 臂、μ=(0.6,0.4)、ETC m=10、n=100 时押错臂的频率）。
    """
    n = 400
    ts = np.arange(1, n + 1)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.plot(ts, 1.0 / ts, color=VERM, lw=2.0,
            label=t(r"按 $1/t$ 衰减（log 级 regret 需要）", r"decays as $1/t$"))
    ax.plot(ts, np.full_like(ts, 0.13, dtype=float), color=BLUE, lw=2.0,
            label=t("ETC 的常数错误率（示意 0.128）", "ETC: constant error rate"))
    ax.fill_between(ts, 1.0 / ts, color=VERM, alpha=0.10)
    ax.set_xlabel(t("轮数 t", "round t"))
    ax.set_ylabel(t("选到次优臂的概率", "P(suboptimal at round t)"))
    ax.set_title(t(r"为什么 $\log n$ 级 regret 要求概率按 $1/t$ 衰减",
                   r"Why $\log n$ regret needs a $1/t$ error rate"))
    ax.set_ylim(0, 0.34)
    ax.legend(loc="upper right")
    ax.annotate(t(r"面积 $\approx\sum_t 1/t\approx\ln n$", r"area = $\sum_t 1/t \approx \ln n$"),
                xy=(120, 1 / 120), xytext=(150, 0.075), fontsize=9.5, color=VERM,
                arrowprops=dict(arrowstyle="->", color=VERM, lw=1))
    save(fig, out_dir, "one-over-t.png")


# ---------------------------------------------------------------- 图 7–10：Lecture 5（贝叶斯 / Thompson Sampling）
def _run_bandit(mu, n, trials, policy, rng, etc_m=0, gaussian=True, ucb_c=4.0, checkpoints=None):
    r"""并排跑 trials 条轨迹，返回累积 regret。

    policy: "ucb" | "etc" | "ts"。奖励默认 N(mu, 1)；gaussian=False 时用伯努利。
    ucb_c 是 bonus 里 log 的系数：sqrt(c*log t/T)，c=4 是讲义里 δ=1/n² 的版本。
    checkpoints 给定时只在这些轮次记录，返回 (trials, len(checkpoints)) 的矩阵——
    跑 n=1e6 那样长的轨迹时，全量记录会占几个 GB。
    """
    mu = np.asarray(mu, dtype=float)
    k, best = len(mu), float(mu.max())
    rows = np.arange(trials)
    counts = np.zeros((trials, k), dtype=np.int64)
    sums = np.zeros((trials, k))
    acc = np.zeros(trials)
    cum = np.empty((trials, n))
    committed = np.full(trials, -1)
    cp_set = set(int(c) for c in checkpoints) if checkpoints is not None else None
    snapshots = []

    for t in range(1, n + 1):
        mean_hat = sums / np.maximum(counts, 1)
        if policy == "ucb":
            bonus = np.sqrt(ucb_c * np.log(max(t, 2)) / np.maximum(counts, 1))
            idx = np.argmax(mean_hat + bonus, axis=1)
            a = np.where(t <= k, t - 1, idx)
        elif policy == "etc":
            if t <= etc_m * k:
                a = np.full(trials, (t - 1) % k)
            else:
                todo = committed < 0
                if todo.any():
                    committed[todo] = np.argmax(mean_hat[todo], axis=1)
                a = committed
        else:  # ts：从后验 N(mean_hat, 1/T) 里抽一个 theta
            sd = 1.0 / np.sqrt(np.maximum(counts, 1))
            theta = rng.normal(loc=mean_hat, scale=sd, size=(trials, k))
            a = np.where(t <= k, t - 1, np.argmax(theta, axis=1))

        if gaussian:
            reward = mu[a] + rng.normal(size=trials)
        else:
            reward = (rng.random(trials) < mu[a]).astype(float)
        counts[rows, a] += 1
        sums[rows, a] += reward
        acc += best - mu[a]
        if cp_set is not None:
            if t in cp_set:
                snapshots.append(acc.copy())
        else:
            cum[:, t - 1] = acc
    if cp_set is not None:
        return np.column_stack(snapshots)
    return cum


def fig_etc_ucb_vs_gap(out_dir: Path, trials: int = 250, seed: int = 5) -> None:
    """k=2、间隙 Δ 变化时，ETC（几个固定 m + 每个 Δ 最好 m）与 UCB 的期望 regret。

    对应讲义第 3 页：固定 m 的 ETC 只在自己那段 Δ 上接近最优，而 UCB 整段都不差；
    「每个 Δ 都取最好的 m」是上帝视角，真实算法拿不到——因为它需要知道 Δ。
    """
    n = 1000
    deltas = np.linspace(0.05, 0.95, 19)
    m_grid = [10, 25, 40, 50, 75, 100, 150, 200, 320, 500]
    show = [25, 50, 75, 100]
    ucb_v, ucb2_v, oracle_v = [], [], []
    grid_v = {m: [] for m in m_grid}

    for d in deltas:
        mu = [0.5 + d / 2, 0.5 - d / 2]  # 两臂关于 0.5 对称，间隙恰为 d
        ucb_v.append(_run_bandit(mu, n, trials, "ucb", np.random.default_rng(seed), gaussian=False).mean(0)[-1])
        ucb2_v.append(_run_bandit(mu, n, trials, "ucb", np.random.default_rng(seed),
                                  gaussian=False, ucb_c=2.0).mean(0)[-1])
        for m in m_grid:
            grid_v[m].append(_run_bandit(mu, n, trials, "etc", np.random.default_rng(seed),
                                         etc_m=m, gaussian=False).mean(0)[-1])
        oracle_v.append(min(grid_v[m][-1] for m in m_grid))

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    shades = ["#b9cfe1", "#93b2cc", "#6c93b4", "#43749a"]
    for m, c in zip(show, shades):
        ax.plot(deltas, grid_v[m], color=c, lw=1.4, label=f"ETC ($m$={m})")
    ax.plot(deltas, oracle_v, color=GOLD, lw=2.2, label=t("ETC（每个 Δ 取最好的 m）", "ETC (best m per gap)"))
    ax.plot(deltas, ucb_v, color=INK, lw=2.2, label=t(r"UCB1：$\sqrt{4\log t/T_i}$", r"UCB1: $\sqrt{4\log t/T_i}$"))
    ax.plot(deltas, ucb2_v, color=INK, lw=1.6, ls=(0, (4, 2)),
            label=t(r"UCB1：$\sqrt{2\log t/T_i}$", r"UCB1: $\sqrt{2\log t/T_i}$"))
    ax.set_xlabel(t(r"间隙 $\Delta$", r"gap $\Delta$"))
    ax.set_ylabel(t("期望 regret", "expected regret"))
    ax.set_title(t(r"$k=2$：期望 regret 随间隙的变化（$n=1000$）",
                   r"Expected regret vs gap ($k=2$, $n=1000$)"))
    ax.legend(loc="upper right", fontsize=8.5)
    ax.set_ylim(0, 60)
    save(fig, out_dir, "etc-ucb-vs-gap.png")


def fig_bayes_bag(out_dir: Path) -> None:
    """两球袋子的先验与两个后验：黑球一步排除，白球只把信念推到 2/3。"""
    panels = [
        (t("先验", "prior"), ["1/2", "1/2"], [0.5, 0.5], "#9a9285"),
        (t("观测：白球", "observe: white"), ["2/3", "1/3"], [2 / 3, 1 / 3], BLUE),
        (t("观测：黑球", "observe: black"), ["0", "1"], [0.0, 1.0], VERM),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.0), sharey=True)
    labels = ["$P(\\mathrm{WW})$", "$P(\\mathrm{WB})$"]
    for ax, (title, texts, vals, color) in zip(axes, panels):
        bars = ax.bar(labels, vals, color=[color, color], alpha=0.75, width=0.55)
        for bar, v, s in zip(bars, vals, texts):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 0.03, s,
                    ha="center", fontsize=11, color=INK)
        ax.set_title(title, fontsize=11)
        ax.set_ylim(0, 1.15)
        ax.grid(axis="x", visible=False)
    axes[0].set_ylabel(t("概率", "probability"))
    fig.suptitle(t("一个装了「两白」或「一白一黑」的袋子：先验 → 后验",
                   "A bag with WW or WB: prior -> posterior"), fontsize=11.5, y=1.02)
    save(fig, out_dir, "bayes-bag.png")


def fig_ts_sampling(out_dir: Path) -> None:
    """TS 的一次抽样：后验均值高的臂也可能输掉，这就是随机化带来的探索。"""
    xs = np.linspace(0.15, 1.05, 600)
    specs = [
        ("arm 1", 0.62, 0.10, BLUE, 0.55),
        ("arm 2", 0.55, 0.18, VERM, 0.70),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for name, mu, sd, color, draw in specs:
        y = np.exp(-0.5 * ((xs - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
        ax.plot(xs, y, color=color, lw=2.0, label=f"{name}: $\\mathcal{{N}}$({mu}, {sd}$^2$)")
        ax.fill_between(xs, y, color=color, alpha=0.10)
        peak = np.exp(-0.5 * ((draw - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
        ax.plot([draw, draw], [0, peak], color=color, ls=(0, (2, 2)), lw=1.2)
        ax.scatter([draw], [0], marker="^", s=60, color=color, zorder=5)
        ax.text(draw, 0.16, rf"$\theta$={draw}", ha="center", fontsize=9.5, color=color,
                bbox=dict(boxstyle="round,pad=0.15", fc=PAPER, ec="none", alpha=0.9))
    ax.annotate(t(r"抽到 $\theta_2>\theta_1$，于是选 arm 2" + "\n"
                  + r"尽管它的后验均值更低 —— 这就是探索",
                  "theta_2 > theta_1: pick arm 2"),
                xy=(0.70, 1.30), xytext=(0.80, 3.35), fontsize=9.5, color=VERM, ha="center",
                arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))
    ax.set_ylim(-0.05, 4.55)
    ax.set_xlabel(t("奖励均值 $\\mu$", "mean reward $\\mu$"))
    ax.set_ylabel(t("后验密度", "posterior density"))
    ax.set_title(t("Thompson Sampling 决策前的一次抽样（示意）",
                   "One draw per arm before the decision"))
    ax.legend(loc="upper left", fontsize=9)
    save(fig, out_dir, "ts-sampling.png")


def fig_ts_vs_ucb(out_dir: Path, trials: int = 300, seed: int = 7) -> None:
    """Gaussian bandits 上 TS 与 UCB1 的累积 regret。

    讲义第 14 页的定理是 Gaussian 版：R_n ≤ Σ 2log n/Δ_i。
    注意这里的曲线**不画** 2log n/Δ 那条渐近线：它的常数项是 O(1)，
    在 n=1e4 时还在曲线上面，硬画出来会像是 TS 违反了下界。
    """
    mu = [0.60, 0.50, 0.40]
    n = 10000
    ts = _run_bandit(mu, n, trials, "ts", np.random.default_rng(seed))
    ucb = _run_bandit(mu, n, trials, "ucb", np.random.default_rng(seed + 1), gaussian=True)

    ts_mean, ucb_mean = ts.mean(0), ucb.mean(0)
    lo, hi = np.percentile(ts, 10, axis=0), np.percentile(ts, 90, axis=0)
    slope = sum(2.0 / (max(mu) - m) for m in mu if m < max(mu))  # Σ 2/Δ_i

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    xs = np.arange(1, n + 1)
    ax.fill_between(xs, lo, hi, color=VERM, alpha=0.14, lw=0, label=t("TS 的 10–90 分位", "TS 10-90%"))
    ax.plot(xs, ts_mean, color=VERM, lw=2.2, label="Thompson Sampling")
    ax.plot(xs, ucb_mean, color=BLUE, lw=2.0, label="UCB1")
    ax.text(0.40, 0.80,
            t(f"渐近极限：$R_n/\\ln n\\to\\sum 2/\\Delta_i={slope:.0f}$\n"
              "常数项是 $O(1)$，$n=10^4$ 还没逼近，所以不画成曲线",
              f"asymptote: $R_n/\\ln n\\to{slope:.0f}$"),
            transform=ax.transAxes, fontsize=9, color="#5a544a")
    ax.set_xlabel(t("轮数 t", "round t"))
    ax.set_ylabel(t("累积 regret $R_t$", "cumulative regret $R_t$"))
    ax.set_title(t(r"Gaussian bandits 上 TS 与 UCB1（$\mu=(0.6,0.5,0.4)$, 300 次平均）",
                   "TS vs UCB1 on Gaussian bandits (300 runs)"))
    ax.legend(loc="upper left", fontsize=9.5)
    save(fig, out_dir, "ts-vs-ucb.png")


def fig_policy_loss(out_dir: Path) -> None:
    """四条策略在各环境下的损失：2 被 3 处处支配，1/3/4 各有一段最佳区间。"""
    x = np.linspace(0, 1, 400)
    curves = [
        ("policy 1", 0.05 + 0.85 * x, GREEN),
        ("policy 2", 0.75 - 0.18 * x + 0.015 * np.sin(3 * x), "#c2185b"),
        ("policy 3", 0.62 - 0.16 * x, BLUE),
        ("policy 4", 0.15 + 0.55 * np.exp(-((x - 0.5) / 0.07) ** 2), VERM),
    ]
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    for name, y, c in curves:
        ax.plot(x, y, color=c, lw=2.0, label=name)
    p2 = 0.75 - 0.18 * x + 0.015 * np.sin(3 * x)
    p3 = 0.62 - 0.16 * x
    ax.fill_between(x, p3, p2, color="#c2185b", alpha=0.10, lw=0)
    ax.text(0.06, 0.93, t("阴影：policy 2 处处高于 policy 3\n→ 被支配，可以删掉",
                          "shaded: policy 2 above policy 3 -> dominated"),
            fontsize=9, color="#c2185b", va="top")
    for xx, txt, c in ((0.02, t("1 最佳", "1 best"), GREEN), (0.50, t("4 最佳", "4 best"), VERM),
                       (0.98, t("4 最佳", "4 best"), VERM)):
        ax.text(xx, 0.02, txt, fontsize=8.5, color=c, ha="left" if xx < 0.5 else "right")
    ax.set_xlabel(t("环境 υ", r"environment $\upsilon$"))
    ax.set_ylabel(t("损失（越小越好）", "loss (lower is better)"))
    ax.set_title(t("策略在各环境下的损失：可容许 vs 被支配",
                   "Loss of four policies: admissible vs dominated"))
    ax.set_ylim(0, 1.12)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.0), fontsize=9, ncol=2)
    save(fig, out_dir, "policy-loss.png")


def fig_posterior_shrink(out_dir: Path) -> None:
    """同一条臂，样本越多后验越窄；窄到一定程度就不会再被抽中。"""
    xs = np.linspace(-0.4, 1.6, 700)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for T, alpha, color in ((4, 0.16, "#9a9285"), (16, 0.22, BLUE), (64, 0.30, VERM)):
        sd = 1.0 / math.sqrt(T)
        y = np.exp(-0.5 * ((xs - 0.6) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
        ax.plot(xs, y, color=color, lw=2.0, label=t(rf"$T_i$={T}，$\sigma$={sd:.2f}", rf"$T_i$={T}"))
        ax.fill_between(xs, y, color=color, alpha=alpha)
    ax.axvline(0.6, color=INK, ls=(0, (3, 3)), lw=1.0)
    ax.annotate(t("样本越多，后验越窄\n→ 抽到偏高值的概率越小",
                  "more samples -> narrower posterior"),
                xy=(0.80, 0.62), xytext=(1.00, 1.45), fontsize=9.5, color=VERM,
                arrowprops=dict(arrowstyle="->", color=VERM, lw=1.1))
    ax.set_xlabel(t(r"$\mu_i$", r"$\mu_i$"))
    ax.set_ylabel(t("后验密度", "posterior density"))
    ax.set_title(t(r"后验随采样次数收缩：$\mathcal{N}(\hat\mu_i,\ 1/T_i)$",
                   r"Posterior shrinks: $\mathcal{N}(\hat\mu_i, 1/T_i)$"))
    ax.set_ylim(0, 3.45)
    ax.legend(loc="upper left", fontsize=8.5)
    save(fig, out_dir, "posterior-shrink.png")


def fig_regret_over_logn(out_dir: Path, trials: int = 150, seed: int = 9) -> None:
    r"""把 regret 除以 $\ln n$：看它到底怎么逼近常数 $\sum 2/\Delta_i=30$。

    这张图存在的理由：$2\log n/\Delta$ 经常被当成「n 轮就错这么多次」，
    但它的常数项是 $O(1)$，而 $\ln n$ 增长得太慢，冲淡这点偏移需要极大的 n。
    """
    mu = [0.60, 0.50, 0.40]
    n_max = 200_000
    cps = np.unique(np.round(np.logspace(2, math.log10(n_max), 70)).astype(int))
    ln = np.log(cps)
    slope = sum(2.0 / (max(mu) - m) for m in mu if m < max(mu))

    ts = _run_bandit(mu, n_max, trials, "ts", np.random.default_rng(seed), checkpoints=cps) / ln
    ucb = _run_bandit(mu, n_max, trials, "ucb", np.random.default_rng(seed + 1), checkpoints=cps) / ln

    ts_m, ucb_m = ts.mean(0), ucb.mean(0)
    lo, hi = np.percentile(ts, 10, axis=0), np.percentile(ts, 90, axis=0)

    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    ax.fill_between(cps, lo, hi, color=VERM, alpha=0.14, lw=0, label=t("TS 的 10–90 分位", "TS 10-90%"))
    ax.plot(cps, ts_m, color=VERM, lw=2.2, label="Thompson Sampling")
    ax.plot(cps, ucb_m, color=BLUE, lw=2.0, label="UCB1")
    ax.axhline(slope, color="#9a9285", ls=(0, (4, 3)), lw=1.3,
               label=t(rf"$\sum 2/\Delta_i={slope:.0f}$（渐进下界，也是 TS 的极限）",
                       rf"$\sum 2/\Delta_i={slope:.0f}$"))
    ax.set_xscale("log")
    ax.set_xlabel(t("轮数 n（对数轴）", "rounds n (log scale)"))
    ax.set_ylabel(t(r"$R_n/\ln n$", r"$R_n/\ln n$"))
    ax.set_title(t(r"把 regret 除以 $\ln n$：收敛有多慢", r"$R_n/\ln n$: how slow the convergence is"))
    ax.text(0.42, 0.88,
            t("下界只在 $n\\to\\infty$ 成立：$\\ln n$ 增长太慢，\n$O(1)$ 的偏移要极大的 $n$ 才被冲淡",
              "the bound is asymptotic only"),
            transform=ax.transAxes, fontsize=9, color="#5a544a")
    ax.set_ylim(0, 62)
    ax.legend(loc="upper left", fontsize=8.5)
    save(fig, out_dir, "regret-over-logn.png")



# ---------------------------------------------------------------- 图 14：尾界对比
def fig_tail_bounds(out_dir: Path) -> None:
    """Chebyshev、Hoeffding 与真实尾概率（n=100，Bernoulli(1/2)）的对数坐标对比。

    想说明两件事：
      1. 同样只用「有界 + 独立」，Hoeffding 比 Chebyshev 快了一个数量级以上；
      2. 快的原因是 ε 在指数上（e^{-nε²}）而不是在分母上（1/(nε²)）。
    真实尾概率用二项分布精确计算，作为「界离真值多远」的参照。
    """
    n = 100
    eps = np.linspace(0.04, 0.50, 260)
    cheb = np.minimum(10.0, 1.0 / (4 * n * eps ** 2))
    hoef = np.minimum(10.0, 2 * np.exp(-2 * n * eps ** 2))

    pmf = np.array([math.comb(n, k) / 2 ** n for k in range(n + 1)])
    ks = np.arange(n + 1) / n
    exact = np.array([pmf[np.abs(ks - 0.5) >= e].sum() for e in eps])

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.axhspan(1.0, 10.0, color=GRID, alpha=0.55, lw=0)
    ax.axhline(1.0, color="#9a9285", lw=1.0, ls=(0, (4, 3)))
    ax.text(0.285, 1.30, t("y > 1：界比 1 还大，等于什么都没说", "bound above 1: vacuous"),
            fontsize=9, color="#6f675c")

    ax.plot(eps, cheb, color=BLUE, lw=2.0,
            label=t(r"Chebyshev  $1/(4n\epsilon^2)$", r"Chebyshev  $1/(4n\epsilon^2)$"))
    ax.plot(eps, hoef, color=VERM, lw=2.0,
            label=t(r"Hoeffding  $2e^{-2n\epsilon^2}$", r"Hoeffding  $2e^{-2n\epsilon^2}$"))
    ax.plot(eps, exact, color=GREEN, lw=1.6, ls=(0, (4, 3)),
            label=t("真实尾概率（二项分布）", "exact tail (binomial)"))

    ax.set_yscale("log")
    ax.set_ylim(1e-10, 10)
    ax.set_xlim(0.04, 0.50)
    ax.set_xlabel(t(r"偏差 $\epsilon$", r"deviation $\epsilon$"))
    ax.set_ylabel(t("概率上界（对数轴）", "bound (log scale)"))
    ax.set_title(t(r"同一个 $\epsilon$：Chebyshev 是 $\epsilon^{-2}$，Hoeffding 是 $e^{-n\epsilon^2}$（$n=100$）",
                   r"Chebyshev $\epsilon^{-2}$ vs Hoeffding $e^{-n\epsilon^2}$ ($n=100$)"))

    i30 = int(np.argmin(np.abs(eps - 0.31)))
    ax.annotate(t("\u03b5 在指数上：每加 0.05，Hoeffding 掉几个数量级",
                  "exponential in \u03b5"),
                xy=(eps[i30], hoef[i30]), xytext=(0.325, 8e-6),
                fontsize=9, color=VERM, ha="left",
                arrowprops=dict(arrowstyle="->", color=VERM, lw=1.0,
                                connectionstyle="arc3,rad=0.18"))
    ax.legend(loc="lower left", fontsize=9)
    save(fig, out_dir, "tail-bounds.png")


# slug -> (函数, 说明)
FIGURES = {
    "arms": (fig_arms, "臂的奖励分布与次优间隙"),
    "regret-curves": (fig_regret_curves, "贪心 / ETC / UCB1 的累积 regret"),
    "etc-timeline": (fig_etc_timeline, "ETC 的动作序列"),
    "etc-vs-m": (fig_etc_vs_m, "ETC 的界随 m 的 U 形变化"),
    "ucb-intervals": (fig_ucb_intervals, "UCB 的一轮快照"),
    "one-over-t": (fig_one_over_t, "1/t 错误率与对数 regret"),
    "etc-vs-gap": (fig_etc_ucb_vs_gap, "ETC / UCB 的期望 regret 随间隙变化"),
    "bayes-bag": (fig_bayes_bag, "先验与后验：两球袋子的贝叶斯更新"),
    "ts-sampling": (fig_ts_sampling, "Thompson Sampling 的一次抽样决策"),
    "ts-vs-ucb": (fig_ts_vs_ucb, "TS 与 UCB1 的累积 regret（含渐进下界）"),
    "policy-loss": (fig_policy_loss, "策略损失曲线：可容许与被支配"),
    "posterior-shrink": (fig_posterior_shrink, "后验随采样次数收缩"),
    "regret-over-logn": (fig_regret_over_logn, "R_n/ln n 的收敛速度"),
    "tail-bounds": (fig_tail_bounds, "Chebyshev / Hoeffding / 真实尾概率的对数对比"),
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="生成 bandits 系列的图解 PNG")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="输出目录（默认 public/images/bandit-figures）")
    ap.add_argument("--only", action="append", choices=sorted(FIGURES), help="只画指定的图，可重复")
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto",
                    help="标注语言；auto 表示有中文字体就用中文")
    ap.add_argument("--trials", type=int, default=2000, help="regret 曲线的蒙特卡洛次数")
    ap.add_argument("--seed", type=int, default=11, help="随机种子")
    args = ap.parse_args(argv)

    global CN
    setup_style()
    CN = enable_chinese() if args.lang != "en" else False
    if args.lang == "zh" and not CN:
        print("找不到中文字体，无法用 --lang zh 标注；请安装字体或改用 --lang en", file=sys.stderr)
        return 2
    print(f"中文标注: {'是' if CN else '否'}   输出: {Path(args.out).resolve()}")

    out_dir = Path(args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    names = args.only or list(FIGURES)
    for slug in names:
        func, desc = FIGURES[slug]
        print(f"[{slug}] {desc}")
        if slug == "regret-curves":
            func(out_dir, trials=args.trials, seed=args.seed)
        else:
            func(out_dir)

    total = sum(p.stat().st_size for p in SAVED if p.exists())
    print(f"共 {len(SAVED)} 张，{total / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())