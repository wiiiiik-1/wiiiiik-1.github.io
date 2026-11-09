#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复算导论里那个 ETC 手算例子（2 臂、伯努利、m=10、n=100、Δ=0.2）。

默认参数大致输出：

    平均 regret      4.0x
    押错臂的比例      0.128
    探索期理论亏      2.00    = m·Δ
    押错时的额外亏    16.00   = (n−2m)·Δ
    按频率推算        4.05    = 2.0 + 0.128×16

导论正文里的「2.0 + 0.128×16 ≈ 4.05」就是最后一行：探索期固定亏 2.0，
承诺期以 12.8% 的概率押错，押错后每轮亏 Δ、共 (n−2m)·Δ=16。

用法：
    python scripts/sim/etc-worked-example.py
    python scripts/sim/etc-worked-example.py --trials 500000 --m 20
    python scripts/sim/etc-worked-example.py --mu 0.7,0.5,0.3
"""

from __future__ import annotations

import argparse
import random
import statistics


def run_etc(rng: random.Random, mu: list[float], n: int, m: int) -> tuple[float, int | None]:
    """跑一次 ETC，返回 (累积 regret, 最终押中的臂)。"""
    k = len(mu)
    top = max(mu)
    counts, sums = [0] * k, [0.0] * k
    regret, commit = 0.0, None
    for t in range(1, n + 1):
        if t <= m * k:  # 探索：轮转，与观测无关
            a = (t - 1) % k
        elif commit is None:  # 承诺：按经验均值一次性定死
            commit = max(range(k), key=lambda i: sums[i] / counts[i])
            a = commit
        else:
            a = commit
        counts[a] += 1
        sums[a] += 1.0 if rng.random() < mu[a] else 0.0
        regret += top - mu[a]
    return regret, commit


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="ETC 手算例子的数值核对")
    ap.add_argument("--mu", default="0.6,0.4", help="各臂真实均值，逗号分隔")
    ap.add_argument("--n", type=int, default=100, help="总轮数")
    ap.add_argument("--m", type=int, default=10, help="每臂探索次数")
    ap.add_argument("--trials", type=int, default=200_000, help="模拟次数")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args(argv)

    mu = [float(x) for x in args.mu.split(",")]
    k, top = len(mu), max(mu)
    rng = random.Random(args.seed)

    vals, wrong = [], 0
    for _ in range(args.trials):
        reg, commit = run_etc(rng, mu, args.n, args.m)
        vals.append(reg)
        if commit is None or mu[commit] < top:
            wrong += 1

    p_wrong = wrong / args.trials
    explored = min(args.m * k, args.n)
    print(f"ETC  m={args.m}  n={args.n}  mu={mu}  trials={args.trials}")
    print(f"  平均 regret     {statistics.mean(vals):.2f}")
    print(f"  中位数          {statistics.median(vals):.2f}")
    print(f"  P90             {sorted(vals)[int(len(vals) * 0.9)]:.2f}")
    print(f"  押错臂的比例     {p_wrong:.3f}")

    if k == 2:
        gap = top - min(mu)
        explore = args.m * gap
        extra = (args.n - explored) * gap
        print(f"  探索期理论亏     {explore:.2f}   (= m·Δ)")
        print(f"  押错时的额外亏   {extra:.2f}   (= (n-mk)·Δ)")
        print(f"  按频率推算       {explore + p_wrong * extra:.2f}   (= m·Δ + p·(n-mk)·Δ)")
    else:
        print("  （k>2 时不再拆「探索期 / 承诺期」两项，直接看上面的平均值）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
