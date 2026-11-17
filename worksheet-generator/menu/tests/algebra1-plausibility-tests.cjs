/* Algebra 1 plausibility guards (2026-11-17, audit #2): numbers in a named context must be possible in real life. */
'use strict';
const assert = require('node:assert/strict');
const M = require('./load.cjs')().MKMENU;
const RANGES = [[/quiz scores \(out of 20 points\)/, 0, 20], [/quiz scores \(out of 30 points\)/, 0, 30], [/test scores/, 40, 100], [/minutes spent on homework/, 5, 90],
  [/points scored by a basketball player/, 0, 40], [/hours of sleep/, 5, 11], [/books read this year/, 0, 60], [/text messages sent/, 0, 120], [/daily high temperatures/, 20, 100],
  [/pages read in a week/, 0, 300], [/goals scored in each soccer game/, 0, 8], [/ages of people at a family party/, 1, 90]];
let checked = 0;
for (const skill of ['center', 'stdev', 'statistics-mean', 'statistics-median', 'statistics-mode']) for (const lv of ['cp2', 'cp1', 'honors']) for (const c of M.LEVELS[lv].tiers) for (let n = 0; n < 25; n++) {
  const p = M.generateProblem('algebra1-statistics-data-modeling', skill, c, { intOnly: lv !== 'honors', level: lv }, 'plaus:' + skill + lv + c + n, { keys: new Set(), sigs: new Set() });
  assert.ok(!p.failed, p.reason);
  const text = p.prompt.replace(/\\ /g, ' ');
  const vals = p.fig && p.fig.kind === 'dotplot' ? Object.keys(p.fig.counts).map(Number) : ((/⟨([-0-9.,\\ ]+)⟩/.exec(text) || [])[1] || '').split(',').map(Number).filter(Number.isFinite);
  for (const [re, lo, hi] of RANGES) if (re.test(text) || (p.fig && re.test(p.fig.label || ''))) { assert.ok(vals.every(v => v >= lo && v <= hi), 'Impossible values for ' + re + ': ' + vals + ' in ' + text); checked++; }
}
for (const lv of ['cp2', 'cp1', 'honors']) for (const c of M.LEVELS[lv].tiers) for (const s of Object.values(M.skillSets).filter(s => /^algebra1-/.test(s.id))) for (let n = 0; n < 6; n++) {
  const p = M.generateProblem(s.id, 'mcas-context', c, { intOnly: lv !== 'honors', level: lv }, 'plaus-ctx:' + s.id + lv + c + n, { keys: new Set(), sigs: new Set() });
  assert.ok(!p.failed, p.reason);
  const a = p.parts.map(x => x.answer); assert.equal(new Set(a).size, a.length, 'Four-part problem repeats an answer: ' + a + ' in ' + p.prompt);
  assert.ok(!/ squared|times ten to the power/.test(p.prompt + p.parts.map(x => x.prompt).join(' ')), 'Math written in words: ' + p.prompt);
  const sci = /⟨(\d+(?:\.\d+)?)\\times 10\^\{\d+\}⟩/.exec(p.prompt); if (sci) assert.ok(+sci[1] >= 1 && +sci[1] < 10, 'Not scientific notation: ' + p.prompt);
  checked++;
}
console.log('Algebra 1 plausibility: ' + checked + ' checks passed.');
