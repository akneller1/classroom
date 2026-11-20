#!/usr/bin/env node
// Whole-site audit (2026-11-20), deploy-time fixes for content that comes from a pinned release.
//
// #9 Grade 5 "Select ALL the problems that are matched with the correct answer" items always had exactly 2 of 4
// correct, so a student could guess the count. The 144 items now alternate between 2 and 3 correct (the bank schema needs at least 2). An option is never
// invented: a correct (or wrong) match is borrowed from another item of the same skill, where the source already
// checked it, and the item's answer list and worked solution are rebuilt from the options.
// Both Grade 5 bank copies get the same items; the step stops if the two copies differ before the change.
//
// Usage: node scripts/apply-site-audit.mjs [_site]
import fs from "node:fs";
import path from "node:path";
import { elementaryPacing } from "./geo-planning.mjs";

const SITE = path.resolve(process.argv[2] || "_site");
const COPIES = [path.join(SITE, "question-banks/grade5"), path.join(SITE, "grade5/math5")].filter((d) => fs.existsSync(d));
if (!COPIES.length) { console.log("Site audit: Grade 5 banks not present, skipped"); process.exit(0); }

const MATCH = /^Select ALL the problems that are matched with the correct answer/;
const hash = (s) => [...s].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);
let changed = 0;
const counts = { 1: 0, 2: 0, 3: 0 };
for (const file of fs.readdirSync(COPIES[0]).filter((f) => f.endsWith(".json"))) {
  const main = JSON.parse(fs.readFileSync(path.join(COPIES[0], file), "utf8"));
  const items = main.questions.filter((q) => q.format === "select-all" && MATCH.test(q.prompt) && q.options.length === 4);
  if (!items.length) continue;
  const bySkill = {};
  for (const q of items) (bySkill[q.skillId] = bySkill[q.skillId] || []).push(q);
  const before = new Map(items.map((q) => [q.id, JSON.stringify(q)]));
  items.sort((a, b) => (a.id < b.id ? -1 : 1)).forEach((q, i) => {
    const target = [2, 3][i % 2], now = q.options.filter((o) => o.correct).length;
    if (now !== 2 || target === 2) { counts[now] = (counts[now] || 0) + 1; return; }
    const want = target === 3, have = new Set(q.options.map((o) => o.text));
    const pool = bySkill[q.skillId].filter((x) => x !== q).flatMap((x) => JSON.parse(before.get(x.id)).options)
      .filter((o) => o.correct === want && !have.has(o.text));
    if (!pool.length) { counts[2]++; return; }
    const slots = q.options.map((o, j) => (o.correct !== want ? j : -1)).filter((j) => j >= 0);
    const h = hash(q.id);
    q.options[slots[h % slots.length]] = { text: pool[h % pool.length].text, correct: want };
    q.answer = q.options.filter((o) => o.correct).map((o) => o.text);
    q.solutionSteps = [q.solutionSteps[0], ...q.options.map((o) => o.text + (o.correct ? ": correct." : ": not correct."))];
    counts[target]++; changed++;
  });
  const byId = new Map(items.map((q) => [q.id, q]));
  fs.writeFileSync(path.join(COPIES[0], file), JSON.stringify(main, null, 2) + "\n");
  for (const dir of COPIES.slice(1)) {
    const f = path.join(dir, file);
    if (!fs.existsSync(f)) continue;
    const other = JSON.parse(fs.readFileSync(f, "utf8"));
    other.questions = other.questions.map((q) => {
      if (!byId.has(q.id)) return q;
      if (JSON.stringify(q) !== before.get(q.id)) throw Error(`Site audit: ${q.id} differs between the Grade 5 bank copies`);
      return byId.get(q.id);
    });
    fs.writeFileSync(f, JSON.stringify(other, null, 2) + "\n");
  }
}
console.log(`Site audit: Grade 5 matched select-all items now have 1 correct: ${counts[1]}, 2: ${counts[2]}, 3: ${counts[3]} (${changed} changed)`);

// #15 Grade 5 web pacing page, like Grades 1-4 and 6-8 (Grade 5 had only a PDF). The skill standards come from the bank:
// each skill is tagged with the standards its questions practice.
const g5 = path.join(SITE, "question-banks/grade5");
if (fs.existsSync(path.join(SITE, "grade5/grade5-main-catalog.js")) && fs.existsSync(g5) && fs.existsSync(path.join(SITE, "grade-6-pacing/index.html"))) {
  const map = {};
  for (const file of fs.readdirSync(g5).filter((f) => f.endsWith(".json"))) {
    const unit = "grade5-" + file.replace(/\.json$/, ""), bySkill = {};
    for (const q of JSON.parse(fs.readFileSync(path.join(g5, file), "utf8")).questions)
      for (const s of q.standards || []) { const m = (bySkill[q.skillId] = bySkill[q.skillId] || {}); m[s] = (m[s] || 0) + 1; }
    map[unit] = Object.fromEntries(Object.entries(bySkill).map(([k, m]) => [k, Object.keys(m).sort((a, b) => m[b] - m[a]).slice(0, 3)]));
  }
  fs.writeFileSync(path.join(SITE, "grade5/grade5-standards-map.js"), "/* Site audit 2026-11-20: Grade 5 skill standards, from the bank's question tags. */\n(function(G){var M=" + JSON.stringify(map) +
    ";G.MKSTD_SKILLS=G.MKSTD_SKILLS||{};Object.keys(M).forEach(function(k){G.MKSTD_SKILLS[k]=M[k];});})(typeof window!==\"undefined\"?window:globalThis);\n");
  const pacing = elementaryPacing(5, SITE);
  if (!pacing) throw Error("Site audit: Grade 5 pacing could not be built");
  const desc = "A 180-day 5th Grade Math pacing guide with Grade 5 MCAS review, a one-semester block plan, and Common Core Grade 5 standards coverage for every question-bank skill.";
  const page = fs.readFileSync(path.join(SITE, "grade-6-pacing/index.html"), "utf8").replace(/<main>[\s\S]*<\/main>/, "<main>\n" + pacing + "\n</main>")
    .replace(/6th Grade Math Pacing Guide and Standards Coverage/g, "5th Grade Math Pacing Guide and Standards Coverage").replace(/grade-6-pacing\//g, "grade-5-pacing/")
    .replace(/<meta name="description" content="[^"]*"/, `<meta name="description" content="${desc}"`).replace(/<meta property="og:description" content="[^"]*"/, `<meta property="og:description" content="${desc}"`)
    .replace(/<a href="\.\.\/u\/math6\/">[^<]*<\/a>/, '<a href="../u/grade5/">5th Grade Math</a>');
  fs.mkdirSync(path.join(SITE, "grade-5-pacing"), { recursive: true });
  fs.writeFileSync(path.join(SITE, "grade-5-pacing/index.html"), page);
  const covered = /(\d+) of (\d+) standards have question-bank practice/.exec(page);
  console.log(`Site audit: Grade 5 pacing page written (${covered ? covered[0] : "coverage not found"})`);
}

// #12 Grades 6 and 7: "Select ALL problems that are matched with the correct answer" items always had 3 of 6 correct
// (182 items). They now cycle through 3, 2 and 4 correct. To add a correct match, one is borrowed from another item of
// the same skill; to remove one, a correct match's final number goes up by 1, which makes it wrong. These banks are
// regenerated by the authoring tools, so the change is made here at deploy and the source banks stay as generated.
for (const course of ["math6", "prealgebra7"]) {
  const dir = path.join(SITE, "question-banks", course);
  if (!fs.existsSync(dir)) continue;
  const n = { 2: 0, 3: 0, 4: 0 };
  for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json")).sort()) {
    const d = JSON.parse(fs.readFileSync(path.join(dir, file), "utf8"));
    const items = d.questions.filter((q) => q.format === "select-all" && /matched with the correct answer/.test(q.prompt) && q.options.length === 6 && q.options.filter((o) => o.correct).length === 3)
      .sort((a, b) => (a.id < b.id ? -1 : 1));
    if (!items.length || d.questions.some((q) => q.format === "select-all" && /matched with the correct answer/.test(q.prompt) && q.options.length === 6 && q.options.filter((o) => o.correct).length !== 3)) continue;   // already done
    const orig = new Map(items.map((q) => [q.id, JSON.parse(JSON.stringify(q))]));
    items.forEach((q, i) => {
      const k = [3, 2, 4][i % 3], h = hash(q.id);
      if (k === 3) { n[3]++; return; }
      const have = new Set(q.options.map((o) => o.text)), want = k === 4;
      const slots = q.options.map((o, j) => (o.correct !== want ? j : -1)).filter((j) => j >= 0), j = slots[h % slots.length];
      if (want) {
        const pool = items.filter((x) => x !== q && x.skillId === q.skillId).flatMap((x) => orig.get(x.id).options).filter((o) => o.correct && !have.has(o.text));
        if (!pool.length) { n[3]++; return; }
        q.options[j] = { text: pool[h % pool.length].text, correct: true };
      } else {
        const t = q.options[j].text, cut = t.lastIndexOf(" → ");
        const ans = cut < 0 ? "" : t.slice(cut + 3), m = [...ans.matchAll(/\d+/g)].pop();
        if (!m) { n[3]++; return; }
        const next = t.slice(0, cut + 3) + ans.slice(0, m.index) + (Number(m[0]) + 1) + ans.slice(m.index + m[0].length);
        if (have.has(next)) { n[3]++; return; }
        q.options[j] = { text: next, correct: false };
      }
      q.answer = q.options.filter((o) => o.correct).map((o) => o.text);
      q.solutionSteps = [q.solutionSteps[0], ...q.options.filter((o) => o.correct).map((o) => o.text + ": correct."), ...q.options.filter((o) => !o.correct).map((o) => o.text + ": incorrect.")];
      n[k]++;
    });
    fs.writeFileSync(path.join(dir, file), JSON.stringify(d, null, 1) + "\n");
  }
  console.log(`Site audit: ${course} matched select-all items with 2, 3, 4 correct: ${n[2]}, ${n[3]}, ${n[4]}`);
}

// #15 Text: "1 feet", "1 inches", "1 units" and "the the" in every bank (not after an operator such as "+ 1 meters",
// where the unit belongs to the whole expression). Done at deploy because several banks are generated.
const SING = { apples: "apple", marbles: "marble", students: "student", dollars: "dollar", cents: "cent", hours: "hour", minutes: "minute", days: "day", cookies: "cookie",
  books: "book", pencils: "pencil", inches: "inch", feet: "foot", meters: "meter", units: "unit", cars: "car", points: "point", years: "year", miles: "mile", pounds: "pound", cups: "cup" };
const ONE = new RegExp("(?<![\\d.,/\\-−+=×] )(?<![\\d.,/\\-−])\\b1 (" + Object.keys(SING).join("|") + ")\\b", "g");
let fixedText = 0;
const fixText = (x) => {
  if (typeof x === "string") { const y = x.replace(ONE, (m, w) => "1 " + SING[w]).replace(/\bthe the\b/g, "the"); if (y !== x) fixedText++; return y; }
  if (Array.isArray(x)) return x.map(fixText);
  if (x && typeof x === "object") { const o = {}; for (const k of Object.keys(x)) o[k] = k === "id" || k === "skillId" ? x[k] : fixText(x[k]); return o; }
  return x;
};
// Grades 1-4 are left to their own audit overlays, whose deploy checks recompute every key.
const bankDirs = [...fs.readdirSync(path.join(SITE, "question-banks")).filter((c) => !/^grade[1-4]$/.test(c)).map((c) => path.join(SITE, "question-banks", c)),
  path.join(SITE, "grade5/math5")].filter((d) => fs.existsSync(d) && fs.statSync(d).isDirectory());
for (const dir of bankDirs) for (const file of fs.readdirSync(dir).filter((f) => f.endsWith(".json"))) {
  const f = path.join(dir, file), raw = fs.readFileSync(f, "utf8");
  if (!ONE.test(raw) && !/\bthe the\b/.test(raw)) continue;
  ONE.lastIndex = 0;
  const before = fixedText, d = fixText(JSON.parse(raw));
  if (fixedText > before) fs.writeFileSync(f, JSON.stringify(d, null, 1) + "\n");
}
console.log(`Site audit: ${fixedText} text glitches fixed ("1 feet", "the the")`);

// Interactive math audit (2026-11-20): the Make a Ten motion diagram on the Grades 1-3 unit pages that teach regrouping.
// The elementary catalogs come from a pinned release, so the card is added to the built catalog here.
const TEN = { 1: ["tens-ones", "add-subtract-100"], 2: ["add-subtract-100", "add-subtract-1000"], 3: ["addition-subtraction-1000"] };
for (const [grade, units] of Object.entries(TEN)) {
  const f = path.join(SITE, `grade${grade}-main-catalog.js`);
  if (!fs.existsSync(f) || !fs.existsSync(path.join(SITE, "artifacts/motion-make-a-ten/index.html"))) continue;
  let src = fs.readFileSync(f, "utf8");
  const m = src.match(/var course=(\{.*?\}),skills=/s);
  if (!m) throw Error(`Site audit: grade${grade} catalog has an unexpected shape`);
  const course = JSON.parse(m[1]);
  let added = 0;
  for (const u of course.units.filter((x) => units.includes(x.id))) {
    if (u.artifacts.some((a) => /motion-make-a-ten/.test(a.path))) continue;
    u.artifacts.push({ level: ["Support", "Standard", "Advanced"], title: "Make a Ten: Regrouping with Base-Ten Blocks",
      path: "artifacts/motion-make-a-ten/index.html", type: "Interactive", bankFormat: "interactive-math",
      thumb: "thumbs/motion-make-a-ten.jpg", worksheet: "artifacts/motion-make-a-ten/worksheet.pdf", answerKey: "artifacts/motion-make-a-ten/teacher-key.pdf",
      description: "Watch base-ten blocks move: ten ones join to make a ten when you add, and a ten opens into ten ones when you subtract. A place-value chart follows each step." });
    added++;
  }
  src = src.replace(m[1], () => JSON.stringify(course));
  fs.writeFileSync(f, src);
  console.log(`Site audit: Make a Ten added to ${added} Grade ${grade} units`);
}
