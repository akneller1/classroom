// Adds the calm theme for tool pages (assets/calm-tools.css) to generator, planner, practice,
// game and viewer pages in the built site, including the Grade 1-5 and Financial Algebra copies
// assembled from the FinancialAlgebra repository. Hand-built activities are left as they are.
// Run by add-site-header.mjs (so the Deploy site workflow runs it after every course is assembled).
// Local preview: node scripts/build-site.mjs && node scripts/add-calm-theme.mjs
import fs from "node:fs";
import path from "node:path";

const OUT = path.resolve(process.env.SITE_DIR || "_site");
const VERSION = "calm-tools-20261118";
// A page gets the theme when it loads one of the shared tool stylesheets below.
const TOOL_CSS = /<link\b[^>]*href=["'](?:[^"']*\/)?(?:core\/app|classroom-base|menu\/menu|planner\/planner|practice\/practice|seating\/seating|games\/games|activity|lib\/fa|course-site|elementary\/el|elementary\/el-tools|g5|g5-tools)\.css[^"']*["'][^>]*>/i;
const TAG = `<link rel="stylesheet" href="/assets/calm-tools.css?v=${VERSION}">`;

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === "node_modules" || e.name.startsWith(".")) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out); else if (/\.html?$/i.test(e.name)) out.push(p);
  }
  return out;
}

export function addCalmTheme(out = OUT) {
  if (!fs.existsSync(path.join(out, "assets", "calm-tools.css"))) throw new Error("assets/calm-tools.css missing from the built site");
  let added = 0;
  for (const file of walk(out)) {
    if (path.relative(out, file) === "index.html") continue; // the home page has calm.css
    let html = fs.readFileSync(file, "utf8");
    if (html.includes("calm-tools.css") || !TOOL_CSS.test(html) || !/<\/head>/i.test(html)) continue;
    // After the page's own stylesheets, so the calm rules win.
    html = html.replace(/<\/head>/i, `${TAG}\n</head>`);
    fs.writeFileSync(file, html);
    added++;
  }
  return added;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  console.log(`Calm tool theme added to ${addCalmTheme()} pages.`);
}
