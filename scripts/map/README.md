# 示意图（archify）

`九篇怎么走` 那张图不是手写的 SVG，是用 [archify](https://github.com/tt-a1i/archify) 生成后抽出来的。
产物只有一个文件：`src/assets/posts-map.svg`（约 27 KB），由 `<PostsMap />` 直接内联，
导论正文与 `/map/` 的「篇与篇之间」共用它。

## 两步流水线

```bash
# 1) 从 knowledge-graph.ts 导出 archify 的 candidate.json，并用 archify 校验/出 HTML
node scripts/map/export-archify.mjs .archify/posts-map --mode posts
node <archify>/bin/archify.mjs finalize architecture \
     .archify/posts-map/candidate.json .archify/posts-map/posts-map.html --quality showcase

# 2) 把 HTML 拆成自包含 SVG：搬 34 条样式、补浅/深两套配色变量、给节点包 <a>
node scripts/map/extract-diagram.mjs .archify/posts-map/posts-map.html src/assets/posts-map.svg
```

`<archify>` 是本机安装位置，例如
`C:\Users\<user>\.dsh\profiles\desktop\node_modules\@tt-a1i\archify-dsh\skills\archify`。
`finalize` 会跑真实浏览器的构图检查（`browser-check`），在沙箱里会 `spawn EPERM`，需要放开进程限制。

## 为什么 extraction 要自己写

archify 交付的是一个独立 HTML（含查看器、约 830 KB）。站点要的是**能内联、跟随站点明暗主题、
节点可点**的图，所以 `extract-diagram.mjs` 做了四件事：

1. 只取 `<svg>`（22 KB）；
2. 把页面里给 SVG 用的 CSS 规则搬进 SVG 自己的 `<style>`，选择器统一加 `svg#posts-map` 前缀，
   避免 `.c-database`、`.t-primary` 这类通用类名污染站点样式；
3. 补上 9 个 CSS 变量：浅色一套、`[data-theme="dark"]` 一套（站点把主题写在 `<html>` 上，
   所以内联后深色模式自动跟随）；
4. 用 `CHAPTERS` 把每个 `<g id="node-…">` 包成 `<a href="/posts/<slug>/">`，
   并去掉原来的 `role="button"` / `tabindex`，避免嵌套可交互元素。

## 为什么全图不走这条路

`--mode graph`（54 个知识点 / 89 条边 / 13 列）也能导出 candidate，但 archify 的构图校验会报
**162 条**问题——93 条连线穿过无关节点、37 条贴着边界框走、24 条短于 24px。降到 `standard`
档也一样，因为这是密度问题，不是画质档问题。所以 54 节点那张仍然是站点自己的 SVG
（`src/components/KnowledgeMap.astro`），只有「篇与篇之间」这一层交给 archify。

要按轨道拆成 5 张小图是可行的后续方向，`export-archify.mjs` 目前只支持 `posts` / `graph` 两种模式。

## 改篇目之后

`CHAPTERS` 一变（新增或重排），上面两步都要重跑，否则图上少一篇或顺序不对。
`posts` 模式的坐标是手写的三行布局：前置三章一行、主线四篇一行、第 5 篇单独一行；
新增第 6 篇时改 `buildPosts()` 里的 `pre` / `main` 两个数组和 `posOf()`。
