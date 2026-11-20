#!/usr/bin/env node
// Whole-site audit 2 #3 (2026-11-20), Grade 5 part: Standard items that reused a Support template are rewritten with an
// added step. Grade 5 comes from a pinned release, so the rewrites live in content-updates/2026-11-20/grade5-levels.json
// (made by the audit tools, every key recomputed by their verify.py) and are applied here to every published copy of the
// Grade 5 banks. Each item must still have the prompt and answer the rewrite was made from; otherwise the build stops.
// Runs after apply-site-audit2.mjs. Usage: node scripts/apply-grade5-levels.mjs [_site]
import fs from "node:fs";
import path from "node:path";

const SITE = path.resolve(process.argv[2] || "_site");
const { items } = JSON.parse(fs.readFileSync(path.resolve("content-updates/2026-11-20/grade5-levels.json"), "utf8"));
const dirs = ["question-banks/grade5", "grade5/math5", "grade5/question-banks/math5"].map((d) => path.join(SITE, d)).filter((d) => fs.existsSync(d));
let changed = 0, files = 0;
const problems = [], seen = new Set();
for (const dir of dirs) for (const f of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
  const file = path.join(dir, f);
  const raw = fs.readFileSync(file, "utf8");
  const d = JSON.parse(raw);
  if (!Array.isArray(d.questions)) continue;
  let n = 0;
  for (const q of d.questions) {
    const e = items[q.id];
    if (!e) continue;
    seen.add(q.id);
    if (q.prompt === e.to.prompt) continue;   // already applied
    if (q.prompt !== e.from.prompt || JSON.stringify(q.answer) !== JSON.stringify(e.from.answer)) { problems.push(path.relative(SITE, file) + ": " + q.id + " changed upstream"); continue; }
    Object.assign(q, e.to);
    delete q.hint;
    if (!e.to.options) delete q.options;
    n++;
  }
  if (n) { fs.writeFileSync(file, raw.trimStart().startsWith("{\n") ? JSON.stringify(d, null, 1) + "\n" : JSON.stringify(d)); changed += n; files++; }
}
const missing = Object.keys(items).filter((id) => !seen.has(id));
if (missing.length) problems.push(missing.length + " rewritten items are not in the Grade 5 banks: " + missing.slice(0, 5).join(", "));
console.log(`Grade 5 levels: ${changed} item copies rewritten in ${files} files (${Object.keys(items).length} Standard items)`);
if (problems.length) { console.error(problems.join("\n")); process.exit(1); }
