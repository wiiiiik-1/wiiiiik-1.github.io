#!/usr/bin/env node
// 从 src/data/knowledge-graph.ts 生成 Archify 的 architecture candidate.json。
//
// 用法（在仓库根目录）：
//   node scripts/map/export-archify.mjs <outDir> --mode graph    # 54 个知识点 · 89 条边
//   node scripts/map/export-archify.mjs <outDir> --mode posts    # 8 篇笔记 · 7 条边
//
// 两种模式：
//   graph  13 个 stage 各占一列，每个 stage 是一个 region boundary；
//          密度高，archify 的构图校验会报大量 edge-through-node，只适合当实验。
//   posts  三行：前置三章 / 主线四篇 / 第 5 篇；边只有章节级依赖，能通过 showcase 校验。
//
// 上色借 componentType（只有 7 种），再用 meta.legend 改名字。

import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const dir = args.find((a) => !a.startsWith("--"));
const mode = args.includes("--mode") ? args[args.indexOf("--mode") + 1] : "posts";
if (!dir) {
  console.error("usage: node scripts/map/export-archify.mjs <outDir> [--mode graph|posts]");
  process.exit(2);
}

const graph = await import(new URL("../../src/data/knowledge-graph.ts", import.meta.url).href);
const { NODES, EDGES, STAGES, TRACKS, CHAPTERS, CHAPTER_EDGES } = graph;

const TRACK_ORDER = { math: 0, prob: 1, stat: 2, bandit: 3, rl: 4 };
const TRACK_TYPE = {
  math: "database",
  prob: "cloud",
  stat: "security",
  bandit: "backend",
  rl: "messagebus",
};
const TRACK_LABEL = Object.fromEntries(TRACKS.map((t) => [t.id, t.name]));
const legend = {
  entries: {
    database: { label: TRACK_LABEL.math },
    cloud: { label: TRACK_LABEL.prob },
    security: { label: TRACK_LABEL.stat },
    backend: { label: TRACK_LABEL.bandit },
    messagebus: { label: TRACK_LABEL.rl },
  },
};

const output = `${path.basename(dir)}/knowledge-topology-${mode}.html`;

function buildGraph() {
  const COL_X = (stage) => 70 + stage * 232;
  const ROW_Y = (i) => 150 + i * 64;
  const byStage = new Map();
  for (const node of NODES) {
    const list = byStage.get(node.stage) ?? [];
    list.push(node);
    byStage.set(node.stage, list);
  }
  for (const list of byStage.values()) {
    list.sort((a, b) => TRACK_ORDER[a.track] - TRACK_ORDER[b.track] || a.id.localeCompare(b.id));
  }

  const components = [];
  for (const [stage, list] of [...byStage.entries()].sort((a, b) => a[0] - b[0])) {
    list.forEach((node, i) => {
      const item = {
        id: node.id,
        type: TRACK_TYPE[node.track],
        label: node.label,
        pos: [COL_X(stage), ROW_Y(i)],
        size: [196, 52],
      };
      if (node.sub && node.sub.length <= 16) item.sublabel = node.sub;
      components.push(item);
    });
  }

  const boundaries = [...byStage.entries()]
    .sort((a, b) => a[0] - b[0])
    .map(([stage, list]) => ({
      kind: "region",
      label: `${String(stage).padStart(2, "0")} ${STAGES.find((s) => s.stage === stage)?.name ?? ""}`.trim(),
      wraps: list.map((n) => n.id),
      pad: 18,
    }));

  const variantOf = (kind) =>
    kind === "contrast" ? "emphasis" : kind === "use" ? "dashed" : "default";

  const connections = EDGES.map((edge, i) => {
    const item = { id: `e${i}`, from: edge.from, to: edge.to, variant: variantOf(edge.kind) };
    if (edge.label && (edge.kind === "contrast" || edge.kind === "template")) item.label = edge.label;
    return item;
  });

  return {
    schema_version: 1,
    diagram_type: "architecture",
    meta: {
      title: "九篇笔记的知识拓扑 · 全图",
      subtitle: `${NODES.length} 个知识点 · ${EDGES.length} 条依赖边 · ${byStage.size} 个阶段；箭头从左指向右，表示「读右边之前先有左边」`,
      locale: "zh-CN",
      output,
      visual_preset: "editorial",
      quality_profile: "standard",
      legend,
    },
    components,
    boundaries,
    connections,
    cards: [
      {
        dot: "slate",
        title: "怎么读",
        items: [
          "每一列是一个阶段，按依赖顺序从左到右，不是阅读顺序",
          "实线是「必须先有」，虚线是「用到」，加粗是「对照」",
        ],
      },
      {
        dot: "cyan",
        title: "这一版没有的东西",
        items: ["不能点进小节：architecture 类型不带超链接", "没有轨道筛选与悬停高亮"],
      },
    ],
  };
}

function buildPosts() {
  const W = 240;
  const H = 86;
  const pre = ["math", "prob", "stat"];
  const main = ["hyp", "mab", "ucb", "ts"];

  // 主线卡间距 350：240 宽 + 110 空档，正好放得下「同一个贝叶斯模板」这块标签（渲染器要 ≥103px）
  const posOf = (id) => {
    const i = pre.indexOf(id);
    if (i >= 0) return [90 + i * 290, 110];
    const j = main.indexOf(id);
    if (j >= 0) return [90 + j * 350, 380];
    return [90 + 3 * 350, 650];
  };

  const order = ["math", "prob", "stat", "hyp", "mab", "ucb", "ts", "rl"];
  const components = order.map((id) => {
    const chapter = CHAPTERS.find((c) => c.id === id);
    if (!chapter) throw new Error(`chapter ${id} not found`);
    const [x, y] = posOf(id);
    return {
      id,
      type: TRACK_TYPE[chapter.tone],
      label: chapter.label,
      sublabel: chapter.eyebrow,
      pos: [x, y],
      size: [W, H],
    };
  });

  const connections = CHAPTER_EDGES.map((edge, i) => {
    const item = { id: `c${i}`, from: edge.from, to: edge.to };
    if (edge.label) item.label = edge.label;
    // 前置线末端 → 主线起点是一条「回车线」：从 stat 底部下来、横穿到 hyp 顶部再落下。
    // 不写 via 的话自动路由会绕到 hyp 的右侧、箭头朝左，看起来像第 2 篇 → 第 1 篇。
    if (edge.from === "stat" && edge.to === "hyp") {
      const [sx] = posOf("stat");
      const [hx] = posOf("hyp");
      item.fromSide = "bottom";
      item.toSide = "top";
      item.via = [[sx + W / 2, 300], [hx + W / 2, 300]];
      // 标签钉在横穿那一段（segment 1）上；自动放置会把它甩到两篇之间
      item.labelSegment = 1;
      item.labelDy = -12;
    }
    if (edge.from === "hyp" && edge.to === "mab") {
      // 两篇相邻，直接一条横线；不钉死的话路由器会绕到卡片下方
      item.fromSide = "right";
      item.toSide = "left";
      item.route = "straight";
    }
    return item;
  });

  return {
    schema_version: 1,
    diagram_type: "architecture",
    meta: {
      title: "九篇笔记怎么走",
      subtitle: "上面是前置三章，中间是主线四篇，下面是加回状态的第 5 篇；箭头上的字是连接的理由",
      locale: "zh-CN",
      output,
      visual_preset: "editorial",
      quality_profile: "showcase",
      legend,
    },
    components,
    boundaries: [
      { kind: "region", label: "前置章节 · 只补够用的部分", wraps: ["math", "prob", "stat"], pad: 26 },
      { kind: "region", label: "主线 · 四篇其实是一个问题", wraps: ["hyp", "mab", "ucb", "ts"], pad: 26 },
    ],
    connections,
    cards: [
      {
        dot: "slate",
        title: "怎么读",
        items: [
          "前置线只在需要时补：求和与不等式 → 概率公理 → 估计与检验",
          "主线按顺序读，第 1 篇的四格表是把「检验」接到「决策」的地方",
        ],
      },
      {
        dot: "amber",
        title: "三条路线",
        items: [
          "最短：只要看得懂 bandits —— 跳过第 1 篇的检验细节",
          "补齐：从零到第 4 篇 —— 推荐路线",
          "倒读：先看结论，遇到不认识的符号再往回跳",
        ],
      },
      {
        dot: "cyan",
        title: "这一版没有的东西",
        items: ["不能点进小节：architecture 类型不带超链接", "站内 /map/ 仍是可点的 SVG 版本"],
      },
    ],
  };
}

const candidate = mode === "graph" ? buildGraph() : buildPosts();
mkdirSync(dir, { recursive: true });
const file = path.join(dir, "candidate.json");
writeFileSync(file, `${JSON.stringify(candidate, null, 2)}\n`, "utf8");
console.log(
  `wrote ${file}  mode=${mode}  ${candidate.components.length} components, ${candidate.connections.length} connections`,
);
