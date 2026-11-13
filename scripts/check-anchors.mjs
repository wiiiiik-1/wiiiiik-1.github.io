#!/usr/bin/env node
// 构建后检查：dist 里所有站内链接（页面与锚点）是否真的可达。
// 用法：node scripts/check-anchors.mjs [distDir]
// 退出码 1 表示有坏链接；CI 在 build 之后跑一次。

import { readdir, readFile } from "node:fs/promises";
import { existsSync } from "node:fs";
import path from "node:path";

const dist = path.resolve(process.argv[2] ?? "dist");

async function walk(dir, out = []) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) await walk(full, out);
    else if (entry.name.endsWith(".html")) out.push(full);
  }
  return out;
}

const files = await walk(dist);
const cache = new Map();
const load = async (file) => {
  if (!cache.has(file)) cache.set(file, await readFile(file, "utf8").catch(() => ""));
  return cache.get(file);
};

const skip = /\.(png|jpg|jpeg|webp|svg|css|js|mjs|xml|txt|pdf|ico)$/i;

function pageFile(target) {
  const clean = target.split("?")[0];
  if (clean.endsWith("/")) return path.join(dist, clean, "index.html");
  if (clean.endsWith(".html")) return path.join(dist, clean);
  return path.join(dist, clean, "index.html");
}

const broken = [];
let pages = 0;
let anchors = 0;

for (const file of files) {
  const html = await load(file);
  for (const match of html.matchAll(/href="(\/[^"#]*)(#[^"]*)?"/g)) {
    const target = decodeURIComponent(match[1]);
    const anchor = match[2] ? decodeURIComponent(match[2].slice(1)) : "";
    if (target.startsWith("/_astro/") || target.startsWith("/images/") || skip.test(target)) continue;
    if (target.startsWith("/posts/") === false && target !== "/" && !target.startsWith("/tags/") &&
        !target.startsWith("/archive") && !target.startsWith("/about") && !target.startsWith("/map")) {
      // 其余路径（如 /rss.xml）按文件存在性检查
    }
    const page = pageFile(target);
    pages++;
    if (!existsSync(page)) {
      broken.push({ from: path.relative(dist, file), to: target + (anchor ? "#" + anchor : ""), why: "page missing" });
      continue;
    }
    if (!anchor) continue;
    anchors++;
    const body = await load(page);
    if (!body.includes(`id="${anchor}"`)) {
      broken.push({ from: path.relative(dist, file), to: target + "#" + anchor, why: "anchor missing" });
    }
  }
}

if (broken.length > 0) {
  console.error(`坏链接 ${broken.length} 个（检查了 ${pages} 个站内链接，其中 ${anchors} 个带锚点）：`);
  for (const item of broken.slice(0, 40)) {
    console.error(`  ${item.from}  ->  ${item.to}   [${item.why}]`);
  }
  if (broken.length > 40) console.error(`  …还有 ${broken.length - 40} 个`);
  process.exit(1);
}

console.log(`站内链接全部可达：${pages} 个链接（${anchors} 个锚点）/ ${files.length} 个页面`);
