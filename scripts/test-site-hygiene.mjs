// Final check of the assembled public site, run by deploy-site.yml just before publishing.
// Fails the deploy (nothing is published; the live site stays as it was) when:
//  1. a card in the catalog points at a page, file or thumbnail that is not in the site;
//  2. a published page or script links to an akneller1.github.io address (every page should stay on mrksclassroom.com);
//  3. a published page shows a literal "\n" between tags (an escaped newline that leaked into the HTML).
// Local run: node scripts/test-site-hygiene.mjs   (after the build and integration steps)
import fs from "node:fs";
import path from "node:path";
import { loadSiteCatalog, sitePath } from "./load-site-catalog.mjs";

const OUT = path.resolve(process.env.SITE_DIR || "_site");
const problems = [];
const LIMIT = Number(process.env.MAX_PROBLEMS) || 200;
const add = (kind, msg) => problems.push(`[${kind}] ${msg}`);

// 1. Catalog paths and thumbnails
const { library, problems: loadProblems } = loadSiteCatalog(OUT, { quiet: true });
for (const p of loadProblems) add("catalog", "catalog script could not be loaded: " + p);
let cards = 0;
for (const c of library.courses) for (const u of c.units || []) for (const a of u.artifacts || []) {
  if (!a) continue;
  cards++;
  for (const key of ["path", "thumb"]) {
    const value = a[key];
    if (!value || /^(https?:)?\/\//.test(value) || /^mailto:/.test(value)) continue;
    const file = path.join(OUT, sitePath(value));
    if (!fs.existsSync(file)) add("missing", `${c.id} / ${u.id} / "${a.title}": ${key} ${value}`);
  }
}

// 2 and 3. Off-site links and leaked "\n"
function walk(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out); else if (/\.(html?|js|mjs|css)$/i.test(e.name)) out.push(p);
  }
  return out;
}
const OFFSITE = /https?:\/\/akneller1\.github\.io\b[^"'\s)<]*/gi; // your own old addresses (third-party docs links are fine)
for (const file of walk(OUT)) {
  const rel = path.relative(OUT, file).split(path.sep).join("/");
  const text = fs.readFileSync(file, "utf8");
  for (const m of text.matchAll(OFFSITE)) add("off-site", `${rel} links to ${m[0].slice(0, 120)}`);
  if (/\.html?$/i.test(rel)) {
    const leak = text.match(/>\\n\s*</);
    if (leak) add("stray-text", `${rel} shows a literal \\n: …${text.slice(Math.max(0, leak.index - 60), leak.index + 6).replace(/\s+/g, " ")}…`);
  }
}

if (problems.length) {
  console.error(`Site check found ${problems.length} problem(s):\n  ` + problems.slice(0, LIMIT).join("\n  "));
  if (problems.length > LIMIT) console.error(`  …and ${problems.length - LIMIT} more`);
  console.error("\nNothing was published. Fix the items above (or ask for help) and push again.");
  process.exit(1);
}
console.log(`PASS site check: ${cards} catalog cards, files and thumbnails present; no off-site links; no stray \\n.`);
