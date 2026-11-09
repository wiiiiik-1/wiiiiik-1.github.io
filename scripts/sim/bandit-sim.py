#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""数值实验：贪心 / ETC / UCB1 在三个场景下的 regret（正文没有直接引用，用来观察边界）。

三个场景是故意选的，重点不是「哪个算法最好」，而是「log regret 是阶的比较，
常数和场景会让小规模上的胜负翻过来」：

    A. 间隙 0.05 + 短视界（n=1000）      ETC 探索成本低，平均约 24，领先；
                                          UCB 还在爬坡，约 38。
    B. 间隙 0.2/0.35 + 长视界（n=10000）  m=50 调得合适时 ETC 约 50，仍压过 UCB1 约 103
                                          —— UCB 的 16ln n/Δ 常数并不小。
    C. 20 个臂、18 个只有 0.10（n=20000）  均匀探索开始变贵：m 从 20 加到 100，
                                          ETC 的平均 regret 从约 460 翻到约 910。

所以「ETC 只能拿线性 regret」讲的是**阶**；在有限 n 上，一个调好 m 的 ETC
完全可能赢过 UCB，正文里也提到了这一点。数字来自固定种子的一次运行，
场景 C 由稀有事件主导，换种子会有较大波动。

用法：
    python scripts/sim/bandit-sim.py                 # 三个场景全跑
    python scripts/sim/bandit-sim.py --scenario A
    python scripts/sim/bandit-sim.py --trials 200
"""

from __future__ import annotations

import argparse
import math
import random
import statistics


def make_greedy(k: int):
    def pick(t: int, counts, sums):
        if 0 in counts:  # 每个臂先试一次，否则永远不碰没试过的臂
            return counts.index(0)
        return max(range(k), key=lambda i: sums[i] / counts[i])

    return pick


def make_etc(k: int, m: int):
    state: dict = {}

    def pick(t: int, counts, sums):
        if t <= m * k:
            return (t - 1) % k
        if "commit" not in state:
            state["commit"] = max(range(k), key=lambda i: sums[i] / counts[i])
        return state["commit"]

    return pick


def make_ucb1(k: int):
    def pick(t: int, counts, sums):
        if 0 in counts:
            return counts.index(0)
        return max(range(k), key=lambda i: sums[i] / counts[i] + math.sqrt(2.0 * math.log(t) / counts[i]))

    return pick


def simulate(mu: list[float], n: int, factory, rng: random.Random) -> float:
    """跑一条策略，返回 n 轮累积 regret。"""
    k, top = len(mu), max(mu)
    counts, sums, regret = [0] * k, [0.0] * k, 0.0
    pick = factory(k)
    for t in range(1, n + 1):
        a = pick(t, counts, sums)
        counts[a] += 1
        sums[a] += 1.0 if rng.random() < mu[a] else 0.0
        regret += top - mu[a]
    return regret


def scenario(title: str, mu: list[float], n: int, etc_ms: list[int], trials: int, seed: int) -> None:
    gaps = sorted({round(max(mu) - m, 4) for m in mu if m < max(mu)})
    print(f"\n=== {title} ===")
    print(f"k={len(mu)}  n={n}  trials={trials}  gaps: {gaps[:3]}{' ...' if len(gaps) > 3 else ''}")
    print(f"{'strategy':<16}{'mean':>10}{'median':>10}{'P90':>10}")

    rng = random.Random(seed)
    runs = [("greedy", make_greedy)]
    runs += [(f"ETC m={m}", (lambda mm: (lambda k: make_etc(k, mm)))(m)) for m in etc_ms]
    runs.append(("UCB1", make_ucb1))

    for name, factory in runs:
        vals = sorted(simulate(mu, n, factory, rng) for _ in range(trials))
        print(f"{name:<16}{statistics.mean(vals):>10.1f}{vals[len(vals) // 2]:>10.1f}"
              f"{vals[int(len(vals) * 0.9)]:>10.1f}")


SCENARIOS = {
    "A": ("A. 难分辨的一对 (0.50 / 0.45 / 0.35)，n=1000", [0.50, 0.45, 0.35], 1000, [50], 1200),
    "B": ("B. 差距明显 (0.50 / 0.30 / 0.15)，n=10000", [0.50, 0.30, 0.15], 10000, [50], 1200),
    "C": ("C. 20 个臂，只有两个值得试，n=20000", [0.50, 0.45] + [0.10] * 18, 20000, [20, 100], 400),
}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="贪心 / ETC / UCB1 的 regret 对比")
    ap.add_argument("--scenario", choices=sorted(SCENARIOS), action="append",
                    help="只跑指定场景，可重复；默认全跑")
    ap.add_argument("--trials", type=int, default=None, help="覆盖每个场景的模拟次数")
    ap.add_argument("--seed", type=int, default=20261106)
    args = ap.parse_args(argv)

    print("固定种子 %d；同一台机器重跑结果一致。" % args.seed)
    for key in args.scenario or sorted(SCENARIOS):
        title, mu, n, etc_ms, trials = SCENARIOS[key]
        scenario(title, mu, n, etc_ms, args.trials or trials, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
