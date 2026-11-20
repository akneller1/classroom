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
