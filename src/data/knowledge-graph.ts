export type Track = "math" | "prob" | "stat" | "bandit";

export interface GraphNode {
  id: string;
  label: string;
  /** 第二行小字，通常是公式或英文原词 */
  sub?: string;
  track: Track;
  /** 横轴分层：0 数学工具 → 9 渐近最优 */
  stage: number;
  /** 点击跳转的地址；没有则只在图里出现 */
  href?: string;
  /** 一句话说明「为什么需要它」 */
  note: string;
}

export type EdgeKind = "req" | "use" | "contrast" | "template";

export interface GraphEdge {
  from: string;
  to: string;
  kind: EdgeKind;
  label?: string;
}

export const TRACKS: { id: Track; name: string; desc: string }[] = [
  { id: "math", name: "数学工具", desc: "求和、对数、渐近、不等式、KL" },
  { id: "prob", name: "概率论", desc: "公理、条件概率、随机变量、期望、极限定理" },
  { id: "stat", name: "数理统计", desc: "似然、估计、区间、检验、后验" },
  { id: "bandit", name: "序贯决策", desc: "regret、ETC、UCB、Thompson" },
];

export const STAGES: { stage: number; name: string }[] = [
  { stage: 0, name: "数学工具" },
  { stage: 1, name: "概率公理" },
  { stage: 2, name: "随机变量" },
  { stage: 3, name: "期望与条件" },
  { stage: 4, name: "极限定理" },
  { stage: 5, name: "统计推断" },
  { stage: 6, name: "检验与后验" },
  { stage: 7, name: "序列决策" },
  { stage: 8, name: "ETC / UCB" },
  { stage: 9, name: "Thompson / 下界" },
];

/* ------------------------------------------------------------------
   节点：45 个知识点
   stage 只表示「大致在哪一列」，不表示强制的先后
------------------------------------------------------------------ */
export const NODES: GraphNode[] = [
  // ---------- stage 0：数学工具 ----------
  { id: "sum", label: "求和与级数", sub: "Hₙ ≈ ln n", track: "math", stage: 0,
    href: "/posts/math-toolbox/#2-求和与级数", note: "ETC 的界里每一步都在换求和；H_n 长什么样决定了 log 从哪来。" },
  { id: "logineq", label: "对数不等式", sub: "1 − x ≤ e⁻ˣ", track: "math", stage: 0,
    href: "/posts/math-toolbox/#3-对数与指数三个反复用的不等式", note: "把 (1−Δ²/4)^m 换成 e^{−mΔ²/4}，ETC 的指数衰减全靠它。" },
  { id: "bigo", label: "渐进记号", sub: "O / o / Θ", track: "math", stage: 0,
    href: "/posts/math-toolbox/#4-渐进记号", note: "「O(log n) 已经不能再好」这句话，离开 O 就没法说清楚。" },
  { id: "tail", label: "尾界不等式", sub: "Hoeffding / Chernoff", track: "math", stage: 0,
    href: "/posts/math-toolbox/#5-五个概率不等式", note: "置信区间、UCB 的 bonus、TS 的后验收缩，都从这里出发。" },
  { id: "jensen", label: "凸性与 Jensen", sub: "E[φ(X)] ≥ φ(E X)", track: "math", stage: 0,
    href: "/posts/math-toolbox/#5-五个概率不等式", note: "KL ≥ 0、Cramér–Rao 的证明骨架，都只是这一行。" },
  { id: "stirling", label: "Stirling 公式", sub: "n! ≈ √(2πn)·(n/e)ⁿ", track: "math", stage: 0,
    href: "/posts/math-toolbox/#6-stirling-公式与阶乘", note: "二项系数与二项尾界的数量级，不查这条算不出来。" },

  // ---------- stage 1：概率公理 ----------
  { id: "axiom", label: "概率公理", sub: "P(Ω)=1", track: "prob", stage: 1,
    href: "/posts/probability-foundations/#1-概率空间", note: "后面所有「可以加、不能减」的操作，合法性都来自这三条。" },
  { id: "cnt", label: "计数与古典概型", track: "prob", stage: 1,
    href: "/posts/probability-foundations/#13-计数与古典概型", note: "等可能样本空间里算概率，本质是数数。" },
  { id: "indep", label: "独立性", sub: "P(AB)=P(A)P(B)", track: "prob", stage: 1,
    href: "/posts/probability-foundations/#24-独立性", note: "union bound 之所以能乘，t 检验之所以能合并方差，都靠它。" },
  { id: "kl", label: "KL 散度", sub: "KL(P‖Q) ≥ 0", track: "math", stage: 1,
    href: "/posts/math-toolbox/#7-kl-散度", note: "bandit 下界的「距离」是 KL，不是欧氏距离。" },

  // ---------- stage 2：随机变量 ----------
  { id: "rv", label: "随机变量", track: "prob", stage: 2,
    href: "/posts/probability-foundations/#3-随机变量", note: "把「事件」换成「数」，才能谈期望、方差、极限。" },
  { id: "cdf", label: "分布函数与密度", sub: "F, f", track: "prob", stage: 2,
    href: "/posts/probability-foundations/#32-分布函数与密度", note: "连续分布下 P(X=x)=0，很多直觉错误都出在这里。" },
  { id: "cond", label: "条件概率", sub: "P(A|B)", track: "prob", stage: 2,
    href: "/posts/probability-foundations/#2-条件概率", note: "「已经看到黑球」之后的世界，是另一个概率空间。" },
  { id: "total", label: "全概率公式", track: "prob", stage: 2,
    href: "/posts/probability-foundations/#22-全概率公式", note: "把复杂事件按「哪个袋子」拆开，是贝叶斯的前半段。" },

  // ---------- stage 3：期望与条件 ----------
  { id: "expect", label: "期望与线性性", sub: "E[ΣXᵢ] = ΣE[Xᵢ]", track: "prob", stage: 3,
    href: "/posts/bandits-series-intro/#71-期望与全期望", note: "regret 的期望可以逐项拆开，靠的是线性性，不是独立性。" },
  { id: "var", label: "方差与协方差", track: "prob", stage: 3,
    href: "/posts/probability-foundations/#5-方差与协方差", note: "「估计准不准」的第一个量化指标；t 统计量的分母。" },
  { id: "condx", label: "条件期望", sub: "E[X|Y]", track: "prob", stage: 3,
    href: "/posts/probability-foundations/#43-条件期望", note: "全期望公式是「拆层」的标准动作。" },
  { id: "ind", label: "指示函数", sub: "1{A}", track: "prob", stage: 3,
    href: "/posts/bandits-series-intro/#72-指示函数", note: "把「第 t 轮选错了吗」变成一个 0/1 变量，regret 才写得出。" },
  { id: "bayes", label: "贝叶斯定理", sub: "P(θ|x) ∝ P(x|θ)P(θ)", track: "prob", stage: 3,
    href: "/posts/thompson-sampling/#34-一般形式", note: "第 4 篇整篇的地基；也是第 1 篇 MAP 规则的同一条式子。" },

  // ---------- stage 4：极限定理 ----------
  { id: "lln", label: "大数定律", sub: "μ̂ → μ", track: "prob", stage: 4,
    href: "/posts/probability-foundations/#6-极限定理", note: "「样本多了，经验均值会靠近真值」——ETC 与 UCB 的共同前提。" },
  { id: "clt", label: "中心极限定理", track: "prob", stage: 4,
    href: "/posts/probability-foundations/#63-中心极限定理", note: "置信区间的 ±1.96σ/√n 与 t 分布的形状，都来自它。" },
  { id: "model", label: "统计模型与似然", sub: "p(x;θ)", track: "stat", stage: 4,
    href: "/posts/statistics-foundations/#1-统计模型", note: "先假定数据从哪个分布里来，才谈得上估计。" },

  // ---------- stage 5：统计推断 ----------
  { id: "est", label: "估计量、偏差与方差", sub: "MSE = b² + v", track: "stat", stage: 5,
    href: "/posts/hypothesis-testing-and-estimation/#33-估计量的评价performance-metrics偏差标准误一致性", note: "「准」与「稳」是两件事，MSE 把它们加在一起。" },
  { id: "mle", label: "极大似然估计", track: "stat", stage: 5,
    href: "/posts/hypothesis-testing-and-estimation/#34-最大似然估计maximum-likelihood-estimation-mle", note: "贝叶斯之前最常用的点估计；也是似然比检验的原料。" },
  { id: "suff", label: "充分统计量", sub: "Fisher 信息", track: "stat", stage: 5,
    href: "/posts/statistics-foundations/#4-充分统计量与信息", note: "「数据里对 θ 有信息的就那么多」——Cramér–Rao 下界的来源。" },
  { id: "samp", label: "抽样分布", sub: "t / χ² / F", track: "stat", stage: 5,
    href: "/posts/statistics-foundations/#2-抽样分布", note: "t 检验的临界值为什么不是正态分位数，答案在这三个分布。" },
  { id: "decision", label: "贝叶斯决策与风险", sub: "后验风险", track: "stat", stage: 5,
    href: "/posts/hypothesis-testing-and-estimation/#24-从错误概率到贝叶斯风险", note: "把「判错要付多少」写进目标函数，MAP 规则就从这里掉出来。" },

  // ---------- stage 6：检验与后验 ----------
  { id: "ci", label: "置信区间", sub: "1−α 覆盖率", track: "stat", stage: 6,
    href: "/posts/statistics-foundations/#5-置信区间", note: "UCB 的「区间」是它的小表弟：宽度换成 1/√T。" },
  { id: "test", label: "假设检验与两类错误", track: "stat", stage: 6,
    href: "/posts/hypothesis-testing-and-estimation/#22-四格表两类错误", note: "第 1 篇的四格表；把「信错/不信错」分成两个代价。" },
  { id: "pval", label: "p 值", track: "stat", stage: 6,
    href: "/posts/statistics-foundations/#64-p-值", note: "最常见的误读：它不是一个「假设为真的概率」。" },
  { id: "np", label: "Neyman–Pearson / 似然比", track: "stat", stage: 6,
    href: "/posts/statistics-foundations/#65-neymanpearson-引理", note: "「给定错误率下最强的检验」长什么样，以及为什么是似然比。" },
  { id: "post", label: "后验与共轭先验", sub: "Beta–Bernoulli", track: "stat", stage: 6,
    href: "/posts/thompson-sampling/#22-贝叶斯的答案给环境一个先验然后最小化期望损失", note: "TS 每一步抽的就是它；共轭让它能一行更新。" },

  // ---------- stage 7：序列决策 ----------
  { id: "seq", label: "序列决策模型", track: "bandit", stage: 7,
    href: "/posts/multi-armed-bandits-intro/#1-问题设定一场-learner-与-environment-的序列博弈", note: "一步决策变成 n 步，目标就从「这一次对」变成「总共亏多少」。" },
  { id: "regret", label: "Regret 定义", sub: "Rₙ = ΣΔ", track: "bandit", stage: 7,
    href: "/posts/multi-armed-bandits-intro/#4-regret把亏了多少写成公式", note: "把「亏」变成一个可比较、可求界的数。" },
  { id: "gap", label: "次优间隙 Δ", sub: "Δᵢ = μ* − μᵢ", track: "bandit", stage: 7,
    href: "/posts/multi-armed-bandits-intro/#34-次优间隙", note: "bandit 里所有常数都带 Δ；Δ 越小，问题越难。" },
  { id: "ee", label: "探索–利用两难", track: "bandit", stage: 7,
    href: "/posts/multi-armed-bandits-intro/#13-explorationexploitation-dilemma探索与利用的两难", note: "多试一次可能选对，也可能白亏一次——所有算法都在权衡这个。" },

  // ---------- stage 8：ETC / UCB ----------
  { id: "etc", label: "ETC 算法", sub: "先试 m 次，再锁定", track: "bandit", stage: 8,
    href: "/posts/multi-armed-bandits-intro/#5-explore-then-commitetc", note: "最朴素的「定额探索」，也是理解后面所有算法的对照组。" },
  { id: "etcb", label: "ETC 的界", sub: "m* = 4ln n / Δ²", track: "bandit", stage: 8,
    href: "/posts/from-etc-to-ucb/#25-最优的-m两害相权", note: "界里出现 m 与 e^{−mΔ²/4} 的拉锯，最优 m 从这里解出来。" },
  { id: "ucb", label: "UCB 与乐观原理", track: "bandit", stage: 8,
    href: "/posts/from-etc-to-ucb/#31-核心原则乐观面对不确定性", note: "面对不确定性时，先假设它站在你这边。" },
  { id: "ucbx", label: "Index 与置信区间", sub: "μ̂ + √(2ln(1/δ)/T)", track: "bandit", stage: 8,
    href: "/posts/from-etc-to-ucb/#41-直觉置信区间会窄下去", note: "UCB 的 bonus 与置信区间的半宽，是同一个量。" },
  { id: "ucbT", label: "16 log n / Δ²", sub: "Tᵢ 的上界", track: "bandit", stage: 8,
    href: "/posts/from-etc-to-ucb/#43-定量tiδi216logn", note: "「每个次优臂最多被拉这么多次」，regret 的界由它直接求和得到。" },

  // ---------- stage 9：Thompson / 下界 ----------
  { id: "ts", label: "Thompson 抽样", track: "bandit", stage: 9,
    href: "/posts/thompson-sampling/#41-主循环", note: "从后验里抽一个参数，按它行动——随机化本身就是探索。" },
  { id: "rand", label: "随机化即探索", track: "bandit", stage: 9,
    href: "/posts/thompson-sampling/#42-随机化带来探索", note: "后验宽的时候偶尔会抽到高值，这个「偶尔」就是探索预算。" },
  { id: "tsb", label: "2 log n / Δ", sub: "Rₙ 的上界", track: "bandit", stage: 9,
    href: "/posts/thompson-sampling/#51-定理", note: "常数从 16 压到 2，正好贴住下界。" },
  { id: "lai", label: "Lai–Robbins 下界", sub: "log n / KL", track: "bandit", stage: 9,
    href: "/posts/thompson-sampling/#55-定理的边界为什么要先各试一次", note: "没有任何算法能比它更快；TS 的上界与它同阶。" },
];

/* ------------------------------------------------------------------
   边：req 前置 / use 使用 / contrast 对照 / template 同一模板
------------------------------------------------------------------ */
export const EDGES: GraphEdge[] = [
  // 数学工具内部
  { from: "sum", to: "logineq", kind: "use" },
  { from: "jensen", to: "kl", kind: "use", label: "KL ≥ 0" },
  { from: "stirling", to: "tail", kind: "use" },
  { from: "sum", to: "tail", kind: "use" },

  // 概率公理
  { from: "axiom", to: "cnt", kind: "use" },
  { from: "axiom", to: "cond", kind: "req" },
  { from: "cond", to: "total", kind: "req" },
  { from: "total", to: "bayes", kind: "req" },
  { from: "cond", to: "indep", kind: "use" },
  { from: "indep", to: "bayes", kind: "use" },
  { from: "axiom", to: "rv", kind: "req" },
  { from: "rv", to: "cdf", kind: "req" },
  { from: "cdf", to: "expect", kind: "req" },
  { from: "rv", to: "var", kind: "req" },
  { from: "expect", to: "var", kind: "req" },
  { from: "expect", to: "condx", kind: "req" },
  { from: "cond", to: "condx", kind: "use" },
  { from: "expect", to: "ind", kind: "use" },
  { from: "var", to: "lln", kind: "req", label: "Chebyshev" },
  { from: "indep", to: "lln", kind: "req" },
  { from: "lln", to: "clt", kind: "use" },
  { from: "cdf", to: "clt", kind: "use" },
  { from: "stirling", to: "clt", kind: "use" },
  { from: "tail", to: "clt", kind: "contrast", label: "非渐近 vs 渐近" },

  // 统计
  { from: "rv", to: "model", kind: "req" },
  { from: "model", to: "est", kind: "req" },
  { from: "expect", to: "est", kind: "req" },
  { from: "var", to: "est", kind: "req" },
  { from: "model", to: "mle", kind: "req" },
  { from: "model", to: "suff", kind: "req" },
  { from: "cdf", to: "samp", kind: "req" },
  { from: "clt", to: "samp", kind: "req" },
  { from: "samp", to: "ci", kind: "req" },
  { from: "est", to: "ci", kind: "req" },
  { from: "tail", to: "ci", kind: "use", label: "Hoeffding 区间" },
  { from: "est", to: "test", kind: "req" },
  { from: "samp", to: "test", kind: "req" },
  { from: "test", to: "pval", kind: "use" },
  { from: "test", to: "np", kind: "use" },
  { from: "mle", to: "np", kind: "req", label: "似然比" },
  { from: "decision", to: "bayes", kind: "template" },
  { from: "bayes", to: "post", kind: "req" },
  { from: "post", to: "decision", kind: "use" },
  { from: "suff", to: "est", kind: "use", label: "Cramér–Rao" },
  { from: "decision", to: "test", kind: "template", label: "同一张四格表" },

  // 决策链
  { from: "seq", to: "regret", kind: "req" },
  { from: "expect", to: "regret", kind: "req" },
  { from: "ind", to: "regret", kind: "use" },
  { from: "seq", to: "gap", kind: "req" },
  { from: "seq", to: "ee", kind: "req" },
  { from: "lln", to: "ee", kind: "use" },
  { from: "regret", to: "etc", kind: "req" },
  { from: "gap", to: "etcb", kind: "req" },
  { from: "etc", to: "etcb", kind: "req" },
  { from: "tail", to: "etcb", kind: "use", label: "Hoeffding" },
  { from: "logineq", to: "etcb", kind: "use" },
  { from: "sum", to: "etcb", kind: "use" },
  { from: "etcb", to: "ucb", kind: "req", label: "换成自适应" },
  { from: "etcb", to: "ucbT", kind: "use" },
  { from: "ucb", to: "ucbx", kind: "req" },
  { from: "tail", to: "ucbx", kind: "use", label: "√(2ln(1/δ)/T)" },
  { from: "bigo", to: "ucbx", kind: "use", label: "δ = 1/n²" },
  { from: "ucbx", to: "ucbT", kind: "req" },
  { from: "ucbx", to: "ci", kind: "contrast", label: "同一区间，两种用法" },
  { from: "ucbT", to: "ucb", kind: "use", label: "回到 regret 界" },
  { from: "ucb", to: "ts", kind: "contrast", label: "乐观 vs 相信" },
  { from: "post", to: "ts", kind: "req" },
  { from: "bayes", to: "ts", kind: "req" },
  { from: "ts", to: "rand", kind: "req" },
  { from: "clt", to: "ts", kind: "use", label: "Gaussian 更新" },
  { from: "ts", to: "tsb", kind: "use" },
  { from: "kl", to: "tsb", kind: "use", label: "常数 2" },
  { from: "tsb", to: "lai", kind: "contrast", label: "上界贴住下界" },
  { from: "ucbT", to: "lai", kind: "contrast" },
  { from: "bigo", to: "lai", kind: "use", label: "同阶" },
];

/* ------------------------------------------------------------------
   篇章级：哪一篇是另一篇的前置
------------------------------------------------------------------ */
export interface Chapter {
  id: string;
  label: string;
  slug: string;
  eyebrow: string;
  note: string;
  tone: "math" | "prob" | "stat" | "bandit";
}

export const CHAPTERS: Chapter[] = [
  { id: "math", label: "数学工具箱", slug: "math-toolbox", eyebrow: "前置 0", tone: "math",
    note: "求和、对数、渐进记号、五个不等式、KL" },
  { id: "prob", label: "概率论基础", slug: "probability-foundations", eyebrow: "前置 1", tone: "prob",
    note: "公理 → 条件概率 → 随机变量 → 期望 → 极限定理" },
  { id: "stat", label: "数理统计基础", slug: "statistics-foundations", eyebrow: "前置 2", tone: "stat",
    note: "似然 → 估计 → 区间 → 检验 → 后验" },
  { id: "hyp", label: "第 1 篇 · 假设检验与估计", slug: "hypothesis-testing-and-estimation", eyebrow: "第 1 篇", tone: "stat",
    note: "两份讲义：四格表、p 值、MLE、置信区间" },
  { id: "mab", label: "第 2 篇 · 多臂老虎机", slug: "multi-armed-bandits-intro", eyebrow: "第 2 篇", tone: "bandit",
    note: "regret 的定义与 ETC 的 $O(n^{2/3})$" },
  { id: "ucb", label: "第 3 篇 · ETC → UCB", slug: "from-etc-to-ucb", eyebrow: "第 3 篇", tone: "bandit",
    note: "$16\log n/\Delta^2$ 与乐观原理" },
  { id: "ts", label: "第 4 篇 · Thompson", slug: "thompson-sampling", eyebrow: "第 4 篇", tone: "bandit",
    note: "贝叶斯后验、随机化探索、$2\log n/\Delta$" },
];

export const CHAPTER_EDGES: { from: string; to: string; label?: string }[] = [
  { from: "math", to: "prob" },
  { from: "prob", to: "stat" },
  { from: "stat", to: "hyp" },
  { from: "hyp", to: "mab", label: "同一个贝叶斯模板" },
  { from: "mab", to: "ucb" },
  { from: "ucb", to: "ts" },
];
/* ------------------------------------------------------------------
   子图：某一篇正文自己的节点 + 它们的全部前置
------------------------------------------------------------------ */
export function postSlugOf(node: GraphNode): string | null {
  const match = node.href?.match(/^\/posts\/([^/#]+)/);
  return match ? match[1] : null;
}

export interface SubGraph {
  nodes: GraphNode[];
  edges: GraphEdge[];
  /** 本篇自己讲的节点；其余是前置 */
  own: Set<string>;
}

const parentsOf = (() => {
  const map = new Map<string, string[]>();
  for (const edge of EDGES) {
    const list = map.get(edge.to) ?? [];
    list.push(edge.from);
    map.set(edge.to, list);
  }
  return map;
})();

export function subgraphFor(slug: string, depth = 2): SubGraph {
  const own = new Set(
    NODES.filter((node) => postSlugOf(node) === slug).map((node) => node.id),
  );
  if (own.size === 0) return { nodes: [], edges: [], own };

  const keep = new Set(own);
  let frontier = [...own];
  for (let level = 0; level < depth; level++) {
    const next: string[] = [];
    for (const current of frontier) {
      for (const parent of parentsOf.get(current) ?? []) {
        if (!keep.has(parent)) {
          keep.add(parent);
          next.push(parent);
        }
      }
    }
    frontier = next;
  }

  return {
    nodes: NODES.filter((node) => keep.has(node.id)),
    edges: EDGES.filter((edge) => keep.has(edge.from) && keep.has(edge.to)),
    own,
  };
}

export function postsWithNodes(): string[] {
  const set = new Set<string>();
  for (const node of NODES) {
    const slug = postSlugOf(node);
    if (slug) set.add(slug);
  }
  return [...set];
}
