// Final sitemap pass, run after every course and page is assembled:
//  1. adds the indexable activity pages (games, labs, flashcards…) that the /u/ unit pages link to, and
//  2. gives each URL a lastmod from the git history of the files behind it (its question bank and activity
//     folders for unit pages, the page file itself for standalone pages). URLs whose sources are not in this
//     repository (the separately assembled grade courses) get no lastmod rather than a made-up one.
// Needs full git history in CI (actions/checkout with fetch-depth: 0); with a shallow clone the dates are
// only as good as the history available.
// Run by .github/workflows/deploy-site.yml after tool-page-meta.mjs. Local: node scripts/finalize-sitemap.mjs
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";

const ROOT = process.cwd();
const OUT = path.resolve(process.env.SITE_DIR || "_site");
const SITE_URL = (process.env.SITE_URL || "https://mrksclassroom.com/").replace(/\/?$/, "/");
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// file -> newest commit date (YYYY-MM-DD)
const fileDate = new Map();
try {
  const log = execFileSync("git", ["log", "--format=__%cI", "--name-only", "--no-renames"], { cwd: ROOT, maxBuffer: 1 << 30 }).toString();
  let date = "";
  for (const line of log.split("\n")) {
    if (line.startsWith("__")) date = line.slice(2, 12);
    else if (line && !fileDate.has(line)) fileDate.set(line, date);
  }
} catch { console.warn("finalize-sitemap: no git history; lastmod left out."); }
const newest = (dates) => dates.filter(Boolean).sort().pop() || "";
const dirMax = new Map();
for (const [f, d] of fileDate) { const k = f.split("/").slice(0, 2).join("/"); if (d > (dirMax.get(k) || "")) dirMax.set(k, d); }
const dirDate = (dir) => dirMax.get(dir.replace(/\/$/, "")) || "";

const sitemapFile = path.join(OUT, "sitemap.xml");
const xml = fs.readFileSync(sitemapFile, "utf8");
const urls = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1].replace(/&amp;/g, "&"));
const seen = new Set(urls);

const rel = (u) => u.slice(SITE_URL.length);
const read = (r) => { const f = path.join(OUT, r.endsWith("/") || !r ? r + "index.html" : r); return fs.existsSync(f) ? fs.readFileSync(f, "utf8") : ""; };
const linkedArtifacts = (html, base) => [...html.matchAll(/href="([^"#?]+)/g)].map((m) => {
  try { return new URL(m[1], SITE_URL + base).href.slice(SITE_URL.length); } catch { return ""; }
}).filter((r) => /^artifacts\/[^/]+\//.test(r));

// 1. Activity pages linked from unit pages: self-canonical, indexable HTML pages only.
const activities = new Set();
for (const u of urls.filter((u) => /\/u\/[^/]+\/[^/]+\/$/.test(u))) {
  for (const r of linkedArtifacts(read(rel(u)), rel(u))) {
    if (!/\.html?$/.test(r)) continue;
    const html = read(r);
    if (!html || /name=["']robots["'][^>]*noindex/i.test(html)) continue;
    const can = (html.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)["']/i) || [])[1];
    if (can !== SITE_URL + r) continue;
    activities.add(SITE_URL + r);
  }
}
for (const a of activities) if (!seen.has(a)) { urls.push(a); seen.add(a); }
// Financial Algebra planning pages (2026-11-17): the pacing guide and standards map, and the Spreadsheet Labs.
for (const r of ["financial/pacing/", "financial/spreadsheet-labs/"]) if (read(r) && !seen.has(SITE_URL + r)) { urls.push(SITE_URL + r); seen.add(SITE_URL + r); }

// 2. lastmod per URL.
function lastmod(u) {
  const r = rel(u);
  if (!r) return newest(["index.html", "app.js", "data.js"].map((f) => fileDate.get(f)));
  let m = r.match(/^u\/([^/]+)\/([^/]+)\/$/);
  if (m) return newest([fileDate.get(`question-banks/${m[1]}/${m[2]}.json`), ...linkedArtifacts(read(r), r).map((a) => dirDate(a.split("/").slice(0, 2).join("/")))]);
  m = r.match(/^u\/([^/]+)\/$/);
  if (m) return newest(urls.filter((x) => rel(x).startsWith(r) && rel(x) !== r).map(lastmod));
  if (/^artifacts\/[^/]+\//.test(r)) return dirDate(r.split("/").slice(0, 2).join("/"));
  return fileDate.get(r.endsWith("/") ? r + "index.html" : r) || "";
}
const memo = new Map();
const entries = urls.map((u) => { if (!memo.has(u)) memo.set(u, lastmod(u)); const d = memo.get(u); return `  <url><loc>${esc(u)}</loc>${d ? `<lastmod>${d}</lastmod>` : ""}</url>`; });
fs.writeFileSync(sitemapFile, `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries.join("\n")}\n</urlset>\n`);
const dated = [...memo.values()].filter(Boolean);
console.log(`Sitemap: ${urls.length} URLs (${activities.size} activity pages), ${dated.length} with lastmod across ${new Set(dated).size} distinct dates.`);
