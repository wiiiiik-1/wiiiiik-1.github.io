#!/usr/bin/env node
// 把 archify 生成的独立 HTML 拆成一个可内联的自包含 SVG。
//
// 用法（在仓库根目录）：
//   node scripts/map/extract-diagram.mjs <archify.html> src/assets/posts-map.svg
//
// 做四件事：
//   1. 抽出 <svg>；
//   2. 把 archify 页面里给 SVG 用的 40 条 CSS 规则搬进 SVG 的 <style>，选择器统一加
//      `svg#posts-map` 作用域前缀，避免污染站点其它样式；
//   3. 补上 9 个 CSS 变量（浅色 / [data-theme="dark"] 深色两套，取值沿用 archify 的 palette）；
//   4. 用 knowledge-graph.ts 的 CHAPTERS 把每个节点组包成 <a href="/posts/<slug>/">，
//      并把里面的交互属性（role=button / tabindex）去掉，避免嵌套可交互元素。

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const [, , inHtml, outSvg] = process.argv;
if (!inHtml || !outSvg) {
  console.error("usage: node scripts/map/extract-diagram.mjs <archify.html> <out.svg>");
  process.exit(2);
}

const graph = await import(new URL("../../src/data/knowledge-graph.ts", import.meta.url).href);
const { CHAPTERS } = graph;
const slugById = new Map(CHAPTERS.map((c) => [c.id, c.slug]));

const html = readFileSync(inHtml, "utf8");
const svgMatch = html.match(/<svg[\s\S]*?<\/svg>/);
if (!svgMatch) throw new Error("no <svg> found in input");
let svg = svgMatch[0];
const rest = html.replace(svg, "");

/* ---------------- 1. 变量 ---------------- */
const LIGHT = {
  "--mask": "#ffffff",
  "--grid": "#e9edf2",
  "--text": "#111827",
  "--text-muted": "#5b6474",
  "--cloud-fill": "rgba(251, 191, 36, 0.18)",
  "--cloud-stroke": "#d97706",
  "--database-fill": "rgba(167, 139, 250, 0.2)",
  "--database-stroke": "#7c3aed",
  "--backend-fill": "rgba(52, 211, 153, 0.18)",
  "--backend-stroke": "#059669",
  "--security-fill": "rgba(251, 113, 133, 0.15)",
  "--security-stroke": "#e11d48",
  "--messagebus-fill": "rgba(251, 146, 60, 0.15)",
  "--messagebus-stroke": "#ea580c",
  "--arrow": "#64748b",
  "--arrow-emphasis": "#059669",
  "--lane-stroke": "#cbd5e1",
};
const DARK = {
  "--mask": "#07101e",
  "--grid": "#15233a",
  "--text": "#f5fbff",
  "--text-muted": "#9eb0c7",
  "--cloud-fill": "rgba(251, 191, 36, 0.16)",
  "--cloud-stroke": "#fbbf24",
  "--database-fill": "rgba(167, 139, 250, 0.16)",
  "--database-stroke": "#a78bfa",
  "--backend-fill": "rgba(52, 211, 153, 0.16)",
  "--backend-stroke": "#34d399",
  "--security-fill": "rgba(251, 113, 133, 0.14)",
  "--security-stroke": "#fb7185",
  "--messagebus-fill": "rgba(251, 146, 60, 0.14)",
  "--messagebus-stroke": "#fb923c",
  "--arrow": "#94a3b8",
  "--arrow-emphasis": "#34d399",
  "--lane-stroke": "#334155",
};
const vars = (scope, table) =>
  `${scope} {\n${Object.entries(table)
    .map(([k, v]) => `  ${k}: ${v};`)
    .join("\n")}\n}`;

/* ---------------- 2. 规则 ---------------- */
const tokens = new Set();
for (const m of svg.matchAll(/class="([^"]+)"/g)) {
  for (const token of m[1].split(/\s+/)) tokens.add(token);
}

const SKIP = /(html\[|data-share-route|@)/;
const scopeSelector = (sel) => {
  const parts = sel.split(",").map((s) => s.trim()).filter(Boolean);
  return parts
    .map((s) => {
      if (s.startsWith("svg#posts-map")) return s;
      if (s.startsWith("svg")) return s.replace(/^svg/, "svg#posts-map");
      return `svg#posts-map ${s}`;
    })
    .join(",\n");
};

const rules = [];
// 先去注释：archify 的 CSS 里注释夹在选择器和块之间，不去掉会拼出非法选择器
const cssText = rest.replace(/\/\*[\s\S]*?\*\//g, "");
for (const m of cssText.matchAll(/([^{}]+)\{([^{}]*)\}/g)) {
  const sel = m[1].trim();
  const body = m[2].trim();
  if (!sel || SKIP.test(sel)) continue;
  const hit = [...tokens].some((token) => sel.includes(`.${token}`));
  if (!hit) continue;
  if (/\{\s*$/.test(sel)) continue;
  rules.push(`${scopeSelector(sel)} { ${body} }`);
}

/* ---------------- 3. 节点包链接 ---------------- */
const groupRange = (id) => {
  const open = svg.indexOf(`<g id="node-${id}"`);
  if (open < 0) return null;
  let depth = 0;
  for (const m of svg.slice(open).matchAll(/<g\b|<\/g>/g)) {
    if (m[0] === "</g>") depth -= 1;
    else depth += 1;
    if (depth === 0) {
      const end = open + m.index + m[0].length;
      return [open, end];
    }
  }
  return null;
};

let linked = 0;
for (const [id, slug] of slugById) {
  const range = groupRange(id);
  if (!range) continue;
  const [start, end] = range;
  let group = svg.slice(start, end);
  group = group
    .replace(/\s+tabindex="[^"]*"/, "")
    .replace(/\s+role="button"/, "")
    .replace(/\s+aria-pressed="[^"]*"/, "");
  const wrapped = `<a href="/posts/${slug}/" class="pm-link" aria-label="读 ${id}">${group}</a>`;
  svg = svg.slice(0, start) + wrapped + svg.slice(end);
  linked += 1;
}

/* ---------------- 4. 组装 style ---------------- */
const styleBlock = `<style>
svg#posts-map { max-width: 100%; height: auto; display: block; }
${vars("svg#posts-map", LIGHT)}
[data-theme="dark"] ${vars("svg#posts-map", DARK).replace(/ \{$/, " {")}
${rules.join("\n")}
svg#posts-map .pm-link { cursor: pointer; }
svg#posts-map .pm-link:hover [data-node-id] > rect:not(.c-mask),
svg#posts-map .pm-link:focus-visible [data-node-id] > rect:not(.c-mask) { stroke-width: 2.6; }
svg#posts-map [data-node-id] > rect:not(.c-mask) { filter: drop-shadow(0 1px 1px rgba(17, 24, 39, 0.05)) drop-shadow(0 5px 10px rgba(17, 24, 39, 0.05)); }
[data-theme="dark"] svg#posts-map [data-node-id] > rect:not(.c-mask) { filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.35)); }
</style>`;

// 放进 <title> 之后，避免和已有的 <style> 抢顺序
if (svg.includes("</style>")) {
  // archify 自带一段深色覆盖规则，保留它，把新样式插在 </defs> 之后
}
const defsEnd = svg.indexOf("</defs>");
if (defsEnd < 0) throw new Error("no </defs>");
const insertAt = defsEnd + "</defs>".length;
svg = svg.slice(0, insertAt) + "\n" + styleBlock + svg.slice(insertAt);

// 根节点加 id，供作用域选择器使用
svg = svg.replace("<svg ", '<svg id="posts-map" ');

mkdirSync(path.dirname(outSvg), { recursive: true });
writeFileSync(outSvg, `${svg}\n`, "utf8");
console.log(`wrote ${outSvg}  ${(svg.length / 1024).toFixed(1)} KB  rules=${rules.length}  linked=${linked}`);
