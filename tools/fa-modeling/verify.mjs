#!/usr/bin/env node
/* Recomputes the key of every computed question in the Quantitative Modeling units from its printed prompt.
 * Each family in tools/fa-modeling/content/<unit>.mjs carries verify(prompt), which reads the numbers in the question
 * text and works the answer again without the generator's variables. A family with verify() must check at least one
 * question, and every one must agree (numbers within a cent, or the exact answer text). Multiple-choice keys must
 * also be the one option marked correct. Usage: node tools/fa-modeling/verify.mjs <extended FA dir> <unit ...> */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
const [dir, ...ids] = process.argv.slice(2);
let checked = 0, bad = [], families = 0;
for (const id of ids) {
  const content = (await import(pathToFileURL(path.join(dir, 'financial/content', id + '.mjs')).href)).default;
  const bank = JSON.parse(fs.readFileSync(path.join(dir, 'financial/banks', id + '.json'), 'utf8'));
  for (const fam of content.families.filter((f) => f.verify)) {
    families++;
    const qs = bank.questions.filter((q) => q.family === fam.id);
    if (!qs.length) { bad.push(`${id}/${fam.id}: no questions`); continue; }
    for (const q of qs) {
      checked++;
      const text = String(q.prompt).replace(/\*\*/g, '');
      let want;
      try { want = fam.verify(text, q); } catch (e) { bad.push(`${q.id}: verify threw ${e.message}`); continue; }
      const ok = typeof want === 'number'
        ? q.numeric && Math.abs(q.numeric.value - want) <= Math.max(q.numeric.tolerance || 0, 0.011)
        : String(want).replace(/\.00\b/g, '') === String(q.answer).replace(/\.00\b/g, '');
      if (!ok) bad.push(`${q.id}: key ${JSON.stringify(q.numeric ? q.numeric.value : q.answer)}, recomputed ${JSON.stringify(want)} :: ${text.slice(0, 110)}`);
      if (q.format === 'multiple-choice') {
        const right = q.options.filter((o) => o.correct).map((o) => o.text);
        if (right.length !== 1 || right[0] !== q.answer || new Set(q.options.map((o) => o.text)).size !== q.options.length) bad.push(`${q.id}: options`);
      }
    }
  }
}
for (const b of bad.slice(0, 40)) console.error(b);
console.log(`FA extension keys: ${checked} questions in ${families} families recomputed from their prompts, ${bad.length} problems.`);
process.exit(bad.length ? 1 : 0);
