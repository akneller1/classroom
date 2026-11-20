#!/usr/bin/env node
// Whole-site audit 2 (2026-11-20), deploy-time fixes for content that comes from pinned releases.
//  #5  A question bank never holds the same question twice. Two Grades 2 and 4 items became copies of a neighbour after
//      earlier wording overlays; the later copy is rewritten (levels keep their size). Any other repeat stops the build.
//  #11 The legacy Financial Algebra mirror's pacing page linked every unit one folder too high (../../u/ from
//      /financial-algebra/financial/pacing/); its links now reach /u/financial-algebra/<unit>/.
// Usage: node scripts/apply-site-audit2.mjs [_site]
import fs from "node:fs";
import path from "node:path";

const SITE = path.resolve(process.argv[2] || "_site");
const key = (q) => JSON.stringify([String(q.prompt).trim(), q.answer, q.diagram || null, (q.options || []).map((o) => o.text).sort(), q.level, q.parts || null, q.plot || null]);

const REWRITE = {
  'm4-ga-s04-cp2-020': { prompt: 'A quadrilateral has 2 pairs of parallel sides, 4 right angles, and sides that are not all the same length. What is the most specific name for it?',
    answer: 'rectangle', options: ['rectangle', 'square', 'rhombus', 'parallelogram'],
    solutionSteps: ['2 pairs of parallel sides and 4 right angles make it a rectangle.', 'Its sides are not all the same length, so it is not a square. The most specific name is rectangle.'] },
  'm2-sh-s04-cp2-023': { prompt: 'A rectangle has 4 rows of 2 same‑size squares. How many squares in all?', answer: '8', options: ['6', '8', '10', '12'],
    solutionSteps: ['Add 2 once for each row.', '2 + 2 + 2 + 2 = 8.'] },
};
let rewritten = 0, files = 0;
const left = [];
const dirs = ["question-banks/grade1", "question-banks/grade2", "question-banks/grade3", "question-banks/grade4", "question-banks/grade5",
  "grade5/math5", ...[1, 2, 3, 4, 5].map((g) => `grade${g}/question-banks/math${g}`)].map((d) => path.join(SITE, d)).filter((d) => fs.existsSync(d));
for (const dir of dirs) for (const f of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
  const file = path.join(dir, f);
  const d = JSON.parse(fs.readFileSync(file, "utf8"));
  if (!Array.isArray(d.questions)) continue;
  const seen = new Set(); let n = 0;
  for (const q of d.questions) {
    if (seen.has(key(q)) && REWRITE[q.id]) {
      const r = REWRITE[q.id];
      Object.assign(q, { prompt: r.prompt, answer: r.answer, solutionSteps: r.solutionSteps, options: r.options.map((t) => ({ text: t, correct: t === r.answer })) });
      q.sourceNotes = String(q.sourceNotes || '') + ' Rewritten 2026-11-20 (whole-site audit 2 #5): an earlier overlay had made it a copy of a neighbouring item.';
      n++;
    }
    if (seen.has(key(q))) left.push(path.relative(SITE, file) + ': ' + q.id);
    seen.add(key(q));
  }
  if (n) { fs.writeFileSync(file, JSON.stringify(d)); rewritten += n; files++; }
}
console.log(`Site audit 2: ${rewritten} repeated questions rewritten in ${files} elementary bank files`);
if (left.length) { console.error('Repeated questions left:\n' + left.join('\n')); process.exit(1); }

const pacing = path.join(SITE, "financial-algebra/financial/pacing/index.html");
if (fs.existsSync(pacing)) {
  const html = fs.readFileSync(pacing, "utf8"), fixed = html.replace(/href="\.\.\/\.\.\/u\/financial-algebra\//g, 'href="/u/financial-algebra/');
  if (fixed !== html) { fs.writeFileSync(pacing, fixed); console.log("Site audit 2: legacy Financial Algebra pacing links fixed"); }
}

// #8 Financial Algebra games always said "Standard" in the page header, even when a teacher's link asked for Support or
// Advanced (the games already use the level in ?level=). The header now names the level being played.
for (const rel of ["financial/games/index.html", "financial-algebra/financial/games/index.html"]) {
  const f = path.join(SITE, rel);
  if (!fs.existsSync(f)) continue;
  const html = fs.readFileSync(f, "utf8");
  const from = "<small>Standard · Fictional classroom scenarios</small>";
  if (!html.includes(from)) continue;
  const to = '<small id="faLevelNote">Standard · Fictional classroom scenarios</small><script>(function(){var n={cp2:"Support",cp1:"Standard",honors:"Advanced",support:"Support",standard:"Standard",advanced:"Advanced"}[new URLSearchParams(location.search).get("level")||""];if(n)document.getElementById("faLevelNote").textContent=n+" · Fictional classroom scenarios";})();</script>';
  fs.writeFileSync(f, html.replace(from, to));
  console.log("Site audit 2: Financial Algebra games header names the level (" + rel + ")");
}
