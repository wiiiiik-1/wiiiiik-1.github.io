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


# slug -> (函数, 说明)
FIGURES = {
    "arms": (fig_arms, "臂的奖励分布与次优间隙"),
    "regret-curves": (fig_regret_curves, "贪心 / ETC / UCB1 的累积 regret"),
    "etc-timeline": (fig_etc_timeline, "ETC 的动作序列"),
    "etc-vs-m": (fig_etc_vs_m, "ETC 的界随 m 的 U 形变化"),
    "ucb-intervals": (fig_ucb_intervals, "UCB 的一轮快照"),
    "one-over-t": (fig_one_over_t, "1/t 错误率与对数 regret"),
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
