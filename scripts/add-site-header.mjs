// Adds the shared Mr. K's Classroom header (assets/site-header.js) to activity pages in the built site.
// Run by .github/workflows/deploy-site.yml after every course has been assembled into _site.
// Local preview: node scripts/build-site.mjs && node scripts/add-site-header.mjs
//
// Pages covered: everything under artifacts/, financial/ and grade1-5/, and the standalone players in
// worksheet-generator/ (games, flashcards, practice). The header script itself skips pages that already show
// the Mr. K's Classroom name at the top, pages shown inside the activity viewer, printing and full screen.
// When a page belongs to exactly one unit in the catalog, its course and unit are written onto the script tag
// so the Back link returns to that unit.
import fs from "node:fs";
import path from "node:path";
import { loadSiteCatalog, sitePath } from "./load-site-catalog.mjs";

const OUT = path.resolve(process.env.SITE_DIR || "_site");
const VERSION = "site-header-20261113";
const SKIP_PLAYERS = new Set([ // core tools that already have the full site header
  "worksheet.html", "printables.html", "lesson-planner.html", "menu-assessment.html", "seating-chart.html",
]);
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out); else if (/\.html?$/i.test(e.name)) out.push(p);
  }
  return out;
}

// Page -> the one unit it belongs to (pages used by several units get no unit).
const owner = new Map();
try {
  const { library } = loadSiteCatalog(OUT, { quiet: true });
  for (const c of library.courses) for (const u of c.units || []) for (const a of u.artifacts || []) {
    if (!a || !a.path || /^(https?:)?\/\//.test(a.path)) continue;
    const key = sitePath(a.path);
    const entry = { course: c.id, courseName: c.name || c.title || "", unit: u.id, unitName: u.name || u.title || "" };
    if (!owner.has(key)) owner.set(key, entry);
    else if (owner.get(key) && (owner.get(key).course !== entry.course || owner.get(key).unit !== entry.unit)) owner.set(key, null);
  }
} catch (e) {
  console.warn("Catalog not read; headers are added without unit links (" + e.message + ")");
}

const files = [
  ...walk(path.join(OUT, "artifacts")),
  ...walk(path.join(OUT, "financial")),
  ...["grade1", "grade2", "grade3", "grade4", "grade5"].flatMap((g) => walk(path.join(OUT, g))),
  ...fs.readdirSync(path.join(OUT, "worksheet-generator")).filter((n) => /\.html$/.test(n) && !SKIP_PLAYERS.has(n))
    .map((n) => path.join(OUT, "worksheet-generator", n)),
];
let added = 0, withUnit = 0;
for (const file of files) {
  let html = fs.readFileSync(file, "utf8");
  if (html.includes("site-header.js") || !/<\/body>/i.test(html)) continue;
  if (/<meta[^>]+http-equiv=["']refresh/i.test(html)) continue; // redirect stubs
  const rel = path.relative(OUT, file).split(path.sep).join("/");
  const o = owner.get(rel);
  const attrs = o ? ` data-course="${esc(o.course)}" data-unit="${esc(o.unit)}" data-course-name="${esc(o.courseName)}" data-unit-name="${esc(o.unitName)}"` : "";
  const tag = `<script src="/assets/site-header.js?v=${VERSION}" defer${attrs}></script>`;
  const at = html.search(/<\/body>(?![\s\S]*<\/body>)/i);
  html = html.slice(0, at) + tag + "\n" + html.slice(at);
  fs.writeFileSync(file, html);
  added++; if (o) withUnit++;
}
console.log(`Shared header added to ${added} pages (${withUnit} with a Back-to-unit link).`);
