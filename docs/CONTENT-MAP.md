# 博客内容地图（给后续会话）

> **用途**：让新的会话不必先读完 5 篇、约 10 万字符，就能知道这里**有什么、怎么写的、还能补什么**。
> **最后更新**：2026-11-13（前置三章 + 知识拓扑页 `/map/` + 每篇正文的局部子图；CI 改用 `npm ci`）
> **状态**：本地 = 远端 = 已部署，CI 全绿。

---

## 0. 一句话现状

一个 Ink & Paper 风格的数学笔记站。主体是**一个四篇的 bandits 系列**（假设检验 → 多臂老虎机 → ETC/UCB → Thompson Sampling）+ 一篇导论，前面再补**三篇前置章节**（数学工具箱 → 概率论基础 → 数理统计基础），外加一个把八篇拆成 45 个知识点、75 条依赖边的**知识拓扑页 `/map/`**。示意图由脚本生成、可复现；每篇末尾附手写讲义原页扫描。

---

## 1. 站点与仓库

| 项 | 值 |
|---|---|
| 线上地址 | <https://wiiiiik-1.github.io/> |
| 仓库 | `wiiiiik-1/wiiiiik-1.github.io`，分支 `main` |
| 技术栈 | Astro 5.18.2 + Markdown + `remark-math` / `rehype-katex`（构建时渲染公式）；依赖用 lockfile 锁定，CI 跑 `npm ci` |
| 部署 | push 到 `main` → `.github/workflows/deploy.yml` → GitHub Pages，约 2 分钟 |
| 本地命令 | `npm install` / `npm run dev` / `npm run build` / `npm run new -- "标题" slug "标签"` |
| 页面 | `/` 首页、`/posts/`、`/posts/<slug>/`、`/map/`（知识拓扑）、`/tags/`、`/archive/`、`/about/`、`/rss.xml` |

内容集合的 schema 在 `src/content.config.ts`：`title, description, date, updated?, tags[], draft, featured, pdf?, lang`。

---

## 2. 内容资产盘点

| 文件 | 标题 | 日期 | 行数 | 字符 | 首页大卡 | 手稿页 | 图解 |
|---|---|---|---|---|---|---|---|
| `math-toolbox.md` | 数学工具箱：写概率推导之前该备好的六件事 | 2026-11-01 | 340 | 9.0k | – | – | 1（复用） |
| `probability-foundations.md` | 概率论基础：从公理到中心极限定理 | 2026-11-02 | 330 | 10.4k | – | – | 0 |
| `statistics-foundations.md` | 数理统计基础：估计、区间与检验 | 2026-11-03 | 400 | 10.3k | – | – | 0 |
| `bandits-series-intro.md` | 系列导论：从一道暴雨预警，到假设检验与多臂老虎机 | 2026-11-06 | 384 | 9.4k | ✅ | – | 1 |
| `hypothesis-testing-and-estimation.md` | 假设检验与参数估计：两份讲义的中英对照精读笔记 | 2026-10-23 | 1597 | 36.7k | ✅ | 3 图 | 0 |
| `multi-armed-bandits-intro.md` | 多臂老虎机入门：从 Regret 到 Explore-Then-Commit | 2026-10-30 | 610 | 16.8k | – | 10 页 | 2 |
| `from-etc-to-ucb.md` | 从 ETC 到 UCB：遗憾分析、置信上界与 O(log n) | 2026-11-06 | 699 | 17.9k | – | 13 页 | 4 |
| `thompson-sampling.md` | 从 UCB 到 Thompson Sampling：贝叶斯学习、随机化与渐进最优 | 2026-11-13 | 656 | 21.0k | – | 14 页 | 7 |

图片资产：`public/images/` 下共 **5 个目录、约 10.4 MB**
（`bandit-figures` 1.3 MB / 13 张 + `.keep`，`hypothesis-testing-and-estimation` 1.0 MB / 3 张，`multi-armed-bandits-intro` 2.2 MB / 11 张，`from-etc-to-ucb` 3.0 MB / 14 张，`thompson-sampling` 2.9 MB / 14 张）。

---

## 3. 逐篇摘要

### 3.0 前置三章（2026-11 新增）

**定位**：bandits 系列的地板。三篇按依赖顺序排：数学工具 → 概率论 → 数理统计。它们不是某节课的笔记，而是把前面几篇「用到了但没解释」的东西集中补齐，材料参照 DeGroot & Schervish 4th ed.（Ch.1–6 概率、Ch.7–9 统计）。

- `math-toolbox`：记号、求和与 $H_n$、三个对数不等式、$O/o/\Theta$、五个概率不等式（Markov / Chebyshev / Hoeffding / union bound / Jensen）、Stirling、KL 散度、速查表、六个坑。
- `probability-foundations`：概率公理与容斥、条件概率与贝叶斯（含基础率陷阱）、独立性（两两≠相互）、随机变量与 8 个常见分布表、期望/条件期望/指示函数、方差与协方差、LLN 与 CLT、与后文的接口表。
- `statistics-foundations`：参数模型与似然、抽样分布（$\chi^2/t/F$ 与 $n-1$ 的来历）、偏差与 MSE 分解、Fisher 信息与 Cramér–Rao、置信区间（正态 / Wilson / Hoeffding / 覆盖率读法）、检验与 Neyman–Pearson / p 值、Beta–Bernoulli 与 Normal–Normal 共轭、与 bandits 的接口表。

三篇之间用「上一篇 / 下一篇」硬链接串起来，结尾都指向下一章；导论 §6 的篇目表已同步为八篇。

### 3.1 导论 `bandits-series-intro`（系列 hub）

**定位**：用一个「三条暴雨预警只能信一条、且天天重来」的场景，把四篇笔记串成一条线。所有跨篇链接都从这里出发，**改系列结构时第一个要动的是这篇**。

**骨架**：`1 一个具体的早晨` → `2 第一层：这一次该不该信（假设检验）` → `3 第二层：长期该信谁（bandit/regret）` → `4 第三层：探索预算给多少（ETC→UCB）` → `5 手算一次：亏到底亏多少` → `6 四篇笔记的地图` → `7 前置知识的最小集合`（期望/指示函数/O 记号/次高斯/两个尾界）→ `8 怎么读这个系列`

**关键数字**：第 5 节那个算例——2 臂、μ=(0.6,0.4)、ETC m=10、n=100，20 万次模拟得「押错 12.8%、平均 regret 4.05」。由 `scripts/sim/etc-worked-example.py` 复现。

**图**：`bandit-figures/arms-gaps.png`（臂的密度与间隙）。

---

### 3.2 第 1 篇 `hypothesis-testing-and-estimation`

**定位**：系列的地基，也是最长的一篇。把**两份讲义**（假设检验/分类、参数估计）对照着读，最后统一到同一个贝叶斯模板。

**骨架**：`0 先给结论` → `1 统一符号表` → `2 材料一：假设检验与分类`（约 730 行，含四格表、两类错误、似然比、Bayes 阈值、p 值）→ `3 材料二：参数估计`（约 400 行，含 MLE、MAP、置信区间）→ `4 两份讲义的联系：同一个贝叶斯模板` → `5 公式速查表` → `6 自测题（附答案要点）` → `7 一页纸记忆版` → `8 English Summary` → `附录：页码索引`

**特点**：唯一带「自测题」和「English Summary」的篇；公式也最多（行内约 484 处、块级 100 处，全站之最；第 4 篇是 299 + 17）。

**图**：`hypothesis-testing-and-estimation/doc1_p14_bayes_rule.png`、`doc1_p15_summary.png`、`doc1_p16_proof.png`（讲义截图，不是生成的）。

---

### 3.3 第 2 篇 `multi-armed-bandits-intro`

**定位**：把「反复决策 + 答案未知」形式化，定义 regret，并给出第一个算法 ETC。

**骨架**：`0 一条线看懂这十页` → `1 问题设定（learner vs environment）` → `2 目标函数：为什么落在期望上` → `3 均值、最优臂、次优间隙` → `4 Regret：把「亏了多少」写成公式`（含 4.3 的 log n 下界、4.4 的 $1/t$ 概率含义、4.5 分解公式）→ `5 ETC`（含 5.4 的 $O(n^{2/3})$ 讨论）→ `6 公式速查` → `7 术语` → `8 五个坑` → `9 一页纸记忆版` → `10 手稿原页`

**核心结论**：$R_n=\sum_{t}\Delta_{A_t}$；ETC 的探索是「定额预算」，因而被 $\min_j\Delta_j$ 绑死，最好的量级是 $O(n^{2/3})$，够不到 $\log n$。

**图**：`arms-gaps.png`（§3.4）、`one-over-t.png`（§4.4，曲线下面积 = $\ln n$）。

---

### 3.4 第 3 篇 `from-etc-to-ucb`

**定位**：给 ETC 算出 regret 界、指出它为什么不够好、用 UCB 修掉。

**骨架**：`0 十三页在做什么` → `1 先把 ETC 摆回来` → `2 ETC 的 regret 分析`（分解 → $(\star\star)$ 界 → 最优 $m$）→ `3 UCB：用置信上界替掉已知的 Δ`（乐观原理、index、$\delta=1/n^2$）→ `4 UCB 为什么有效`（$\mathrm{UCB}_i-\mu_i<\Delta_i$ 的停止判据）→ `5 UCB 的 regret 定理` → `6 实测对比` → `7 公式速查` → `8 术语` → `9 六个坑` → `10 一页纸记忆版` → `11 手稿原页`

**关键公式**：ETC 的 $R_n\le m\sum\Delta_i+(n-mk)\sum\Delta_ie^{-m\Delta_i^2/4}$，最优 $m=\lceil4\ln n/\Delta^2\rceil$；UCB1 的 $T_i\le16\log n/\Delta_i^2$，$R_n\le\sum16\log n/\Delta_i$。

**图**：`etc-timeline.png`（§1）、`etc-regret-vs-m.png`（§2.5，界的 U 形）、`ucb-intervals.png`（§4.1）、`regret-curves.png`（§6，贪心/ETC/UCB）。

---

### 3.5 第 4 篇 `thompson-sampling`

**定位**：前半给第 3 篇收尾（16 的来源、与 ETC 的胜负、常数 16→2），后半换贝叶斯世界观，落到 TS 与 $2\log n/\Delta_i$ 定理。

**骨架**：`0 十四页在做什么` → `1 先把上一篇收尾`（1.1 index 与宽度、1.2 定理、1.3 逐臂自适应 vs min gap、1.4 常数 16→2、1.5 实测对比）→ `2 换世界观`（被支配/可容许、先验 + 期望损失、序贯更新）→ `3 贝叶斯定理最小复习`（袋子例子、手算、一般形式）→ `4 TS`（主循环、随机化即探索、算法 1、Gaussian/Beta 更新）→ `5 凭什么好`（定理、与 UCB 对照、实测、收敛速度、边界、KL 视角）→ `6 三种算法对照` → `7 公式速查` → `8 术语` → `9 六个坑` → `10 一页纸记忆版` → `11 手稿原页`

**关键公式**：$A_t=\arg\max_i\theta_i(t),\ \theta_i\sim F_i(t)$；Gaussian 更新 $\mathcal N(\hat\mu_i,1/T_i)$（次高斯版 $\sigma^2/T_i$）；Beta 更新 $\mathrm{Beta}(1+\#1,1+\#0)$；定理 $R_n\le\sum2\log n/\Delta_i$，等于下界 $\log n/\mathrm{KL}$。

**图**：`etc-ucb-vs-gap.png`（§1.5）、`policy-loss.png`（§2.1）、`bayes-bag.png`（§3.1）、`ts-sampling.png`（§4.2）、`posterior-shrink.png`（§4.4）、`ts-vs-ucb.png`（§5.3）、`regret-over-logn.png`（§5.4）。

---

## 4. 写作约定（改文前必读）

1. **公式只用 `$...$` 与 `$$...$$`**。`\(...\)` / `\[...\]` 会原样漏成纯文本（2026-10-24 踩过一次，全文 384 处）。
2. **表格单元格里的公式也用 `$...$`**，公式内的竖线写 `\mid`，不要写裸 `|`（会切断表格）。
3. **每张图下面配一段 `*看图要点*`**，用斜体，逐条说明「看见什么 → 说明什么」。这是全站统一的做法，别只丢图。
4. **每篇开头有引用块**：材料来源、和上一篇的关系、符号约定、`**系列位置**：第 N 篇` + 前后篇链接。新增篇目时，**旧篇的这条也要一起改**。
5. **正文里的「补：…」引用块**用来放延伸解释（为什么常数是 4、为什么是 KL、为什么下界不能画成曲线）。这类块是本站的主要解释手段。
6. **每篇结尾五件套**：公式速查 / 术语对照 / 容易踩的坑 / 一页纸记忆版 / 手稿原页。
7. 中文用「」，不用英文直引号；数字与英文两侧留空格；`$O(\log n)$` 这类行内公式前后不加空格以外的标点。

---

## 5. 图解系统

- 生成脚本：`scripts/figures/make-figures.py`（13 张，Ink & Paper 配色，固定随机种子）
- 逐图说明：`scripts/figures/README.md`（slug → 文件 → 用在哪一节 → 想说明什么）
- 输出：`public/images/bandit-figures/`
- 参数：`--only <slug>`、`--out <dir>`、`--lang en`、`--trials`、`--seed`
- 依赖：`scripts/figures/requirements.txt`（matplotlib + numpy）；中文标注缺字体时自动退回英文
- **改图流程**：`--out .figs` 先出草稿 → 用 `read_image` 目视核对 → 确认后复制进 `public/images/bandit-figures/`（这一步需要 `danger-full-access`，沙箱默认禁止写 `public/`）→ 重跑一次做逐像素比对
- 数值实验脚本：`scripts/sim/etc-worked-example.py`（12.8% / 4.05）、`scripts/sim/bandit-sim.py`（三场景）

> 注意：图里的结论都经过实测核对，**不要凭印象改注释里的数字**。第 4 篇有两次是「先写结论、再跑仿真，结果仿真不同意」——最后改的是文字，不是数据。

---

## 6. 验证与发布

| 目的 | 做法 |
|---|---|
| 看构建是否成功 | `node work/wait-run.mjs <sha>` 或 `node work/poll-run.mjs`（GitHub API） |
| 检查线上图是否 200 | `node work/check-ts.mjs`（还顺带查 KaTeX 数量、残留定界符、互链、首页收录） |
| 本地无法用 `web_fetch` | 本站域名解析到 198.18.x（TUN 假 IP），一律用 `node` 的 `fetch` 走 `work/*.mjs` |
| 本地构建 | `node node_modules/astro/astro.js build`（没有 `.bin`，要走这个入口）。沙箱下会 `spawn EPERM`（Vite 的 realpath 优化），需要一次 `danger-full-access`；同理 `npm install` 也要提权 |
| 锚点校验 | build 后逐条比对 `src/data/knowledge-graph.ts` 里的 `href` 与 `dist` 里的 `id` |

---

## 7. 已知缺口 / 可补充的方向

**内容**
1. **Lecture 6 及以后**尚未出现，系列可继续往后接（TS 之后通常是 Lai–Robbins 下界的完整证明、UCB-V / KL-UCB、非平稳 bandit）。
2. **下界只有一句话**：第 4 篇 §5.5 用 KL 视角解释了常数 2，但**没有证明** Lai–Robbins。若要补，最自然的位置是第 4 篇 §5 末尾加一节，或单独成第 5 篇。
3. **第 1 篇（假设检验）与 bandits 的连接偏薄**：只在导论第 2 节和该篇第 4 节各提了一次「同一条贝叶斯模板」。可以把导论里那个「四格表 → regret」的桥写实一点。
4. **没有「系列页」**：目前靠导论当 hub。若篇目继续增加，值得加一个 `/series/` 页面或在 `/posts/` 顶部分组。
5. **站内没有搜索**；标签页是自动生成的，但标签体系没有统一（`多臂老虎机` 出现在 4 篇，`Regret` 出现在 3 篇）。

**工程**
6. **手稿页体积偏大**：每篇 2–3 MB 的 JPEG。若要优化，可换 WebP（视觉无损，约省 40%）或加 `loading="lazy"`。
7. **`work/` 是 scratch（已 gitignore）**：里面的 `check-*.mjs`、`pdf-render.py` 等没入库。若想让别人复现「PDF → 笔记」的流程，可挑几个整理进 `scripts/`。
8. **`refs/` 是本地参考资料（已 gitignore）**：目前有一本 DeGroot《Probability and Statistics》（911 页，含文本层）。前置三章已按它 Ch.1–9 的框架组织；后续若写贝叶斯或回归，可以直接从 Ch.7–9、Ch.11 取材料。
9. **拓扑页的节点数是手写的**：导论 §6 里写死「45 个知识点」，改 `src/data/knowledge-graph.ts` 的 `NODES` 后要同步这一句（`/map/` 页本身用的是 `NODES.length`，不会错）。
10. **每篇开头没有「本节的拓扑位置」小图**：目前只有导论、以及五篇系列正文顶部的一行「在拓扑中的位置」。若想每篇都有一张局部子图，可以在 `knowledge-graph.ts` 里给节点加 `post` 字段再按篇滤一遍。

---

## 8. 常见改动的操作清单

**加一篇新笔记**
1. `src/content/posts/<slug>.md`，frontmatter 至少 `title/description/date/tags`；
2. 图片放 `public/images/<slug>/`；
3. 开头写「材料 / 和上一篇的关系 / 符号 / 系列位置」四行引用块；
4. 结尾补五件套；
5. **回来改导论**：描述、入口段、第 6 节的地图与篇目表、第 8 节的阅读路线；
6. 若在系列中间插入，改前后两篇的「系列位置」。

**加一张图解**
1. 在 `scripts/figures/make-figures.py` 加函数 → 注册进 `FIGURES`；
2. `python scripts/figures/make-figures.py --out .figs --only <slug>` 出草稿并目视核对；
3. 复制进 `public/images/bandit-figures/`（需提权）；
4. 文章里 `![alt](/images/bandit-figures/x.png)` + `*看图要点*`；
5. 更新 `scripts/figures/README.md` 的表与张数。

**加 / 改一个拓扑节点**
1. `src/data/knowledge-graph.ts`：往 `NODES` 加一项（`id/label/track/stage/href/note`），往 `EDGES` 加依赖边（`req` 前置 / `use` 使用 / `contrast` 对照 / `template` 同模板）；
2. **边的两端 stage 必须左小右大**，否则线会往回画；
3. `href` 指向某一节的锚点，锚点由标题自动生成，**标题里有公式时别手写锚点**：KaTeX 会改写标题文本，实际 id 往往变成 `73-o-与渐近记号`、`43-定量tiδi216logn` 这种。正确做法是先 build，再在 `dist/posts/<slug>/index.html` 里搜 `<h2 id=`，抄真实 id；
4. 改完 build 一次，跑一遍「锚点全量校验」（读 `dist` 里的 html，逐个 `href` 查 `id="…"` 是否存在）。
5. **节点的「归属篇目」由 `href` 决定**：`postSlugOf()` 从 `href` 里取 `/posts/<slug>/`，`subgraphFor()` 再把该篇节点与 1–2 级前置一起取出。所以把某个节点的 `href` 从一个章节挪到另一个章节，会同时改变它出现在哪一篇的子图里（`bigo`、`tail`、`kl` 就是这样从导论/第 4 篇挪到数学工具箱的）。
6. **每篇正文的子图是自动的**：`PostLayout` 末尾渲染 `<KnowledgeMap post={post.id} compact />`，先取 2 级前置，节点超过 18 个就退回 1 级。朱砂色填充的是「本篇直接讲」的节点。**新增一篇带节点的文章不需要改 PostLayout**，往 `NODES` 加节点即可。

**改公式/文字**
- 只动 `.md`，push 即可；CI 会自动重建。
- 改完建议跑一次 `node work/check-ts.mjs` 确认没有残留定界符、图片没丢。
