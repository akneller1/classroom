#!/usr/bin/env node
// Whole-site audit #19 (2026-11-20): worked solutions for the pinned Financial Algebra banks.
//
// The repo's own Financial Algebra export is rebuilt from financial/content with fuller steps. The deploy also
// publishes a pinned upstream copy (financial/banks, financial-algebra/...), whose concept and claim items still
// have one step. This step adds the same steps there, matched by prompt text, and never changes anything else.
//   concept: [setup step, the item's own step, check step]   (financial/content/concept-steps.mjs and
//            tools/site-audit-20261120/fa-extra-concept-steps.json for concepts that exist only upstream)
//   claim:   [the item's own model answer, the worked example, "Verdict: ..."]
// Usage: node scripts/apply-fa-steps.mjs [_site]
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SITE = path.resolve(process.argv[2] || "_site");
const DIRS = ["financial/banks", "financial-algebra/financial/banks", "financial-algebra/question-banks/financial-algebra", "question-banks/financial-algebra"]
  .map((d) => path.join(SITE, d)).filter((d) => fs.existsSync(d));
if (!DIRS.length) { console.log("FA steps: no Financial Algebra banks, skipped"); process.exit(0); }

const key = (s) => String(s).replace(/\$(\d[\d,]*)\.00\b/g, "$$$1").replace(/\s+/g, " ").trim();
const cents = (s) => s.replace(/\$(\d{1,3}(?:,\d{3})+|\d+)(?![\d,]*\.\d|,\d|\d)/g, "$$$1.00");
const STEPS = (await import(pathToFileURL(path.join(ROOT, "financial/content/concept-steps.mjs")).href)).default;
const EXTRA = JSON.parse(fs.readFileSync(path.join(ROOT, "tools/site-audit-20261120/fa-extra-concept-steps.json"), "utf8"));
const CONCEPT = new Map(Object.entries(EXTRA).map(([q, s]) => [key(q), s]));
const CLAIM = new Map();
for (const f of fs.readdirSync(path.join(ROOT, "financial/content")).filter((f) => /^[a-z]+\.mjs$/.test(f) && f !== "kit.mjs" && f !== "cheat-sheets.mjs")) {
  const unit = f.replace(".mjs", "");
  const c = (await import(pathToFileURL(path.join(ROOT, "financial/content", f)).href)).default;
  (c.concepts || []).forEach((x, i) => { if (STEPS[unit + "#" + i]) CONCEPT.set(key(x.q), STEPS[unit + "#" + i]); });
  (c.claims || []).forEach((x) => CLAIM.set(key(x.claim), x));
}

let added = 0, files = 0;
const left = [];
for (const dir of DIRS) for (const f of fs.readdirSync(dir).filter((f) => f.endsWith(".json") && f !== "index.json")) {
  const file = path.join(dir, f);
  const d = JSON.parse(fs.readFileSync(file, "utf8"));
  if (!Array.isArray(d.questions)) continue;
  let n = 0;
  for (const q of d.questions) {
    const s = q.solutionSteps || [];
    if (s.length > 1) continue;
    const money = /\$\d[\d,]*\.\d\d/.test(q.prompt) ? cents : (t) => t;
    const claim = (q.prompt.match(/^(?:Evaluate the claim|A friend says): “([^”]+)”/) || [])[1];
    let next = null;
    if (claim) {
      const c = CLAIM.get(key(claim));
      const ex = c?.example || (q.parts || [])[1]?.answer;
      const verdict = typeof q.answer === "string" ? q.answer : null;
      next = [...s, ...(ex && !/^Answers vary/.test(ex) ? ["Example: " + money(ex)] : []), ...(verdict ? ["Verdict: " + verdict + "."] : [])];
    } else if (CONCEPT.has(key(q.prompt))) {
      const [a, b] = CONCEPT.get(key(q.prompt));
      next = [a, ...s, b].filter(Boolean).map(money);
    }
    if (next && next.length > 1) { q.solutionSteps = next; n++; } else left.push(path.relative(SITE, file) + ": " + q.id);
  }
  if (n) { fs.writeFileSync(file, JSON.stringify(d, null, 1)); added += n; files++; }
}
console.log(`FA steps: fuller worked steps on ${added} items in ${files} files` + (left.length ? `; still one step: ${left.length}` : ""));
if (left.length) { console.log(left.slice(0, 20).join("\n")); process.exit(1); }
