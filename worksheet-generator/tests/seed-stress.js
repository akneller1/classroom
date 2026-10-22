/* Reliability stress: random seeds + random settings must never throw "could not generate". */
'use strict';
const NS = require('./load.js');
const ids = Object.keys(NS.registry.lessons);
const R = Math.random; let built = 0, probs = 0, maxAttempts = 0; const errors = {};
const N = +process.env.N || 3000;
for (let i = 0; i < N; i++) {
  const lessons = {}; ids.forEach(id => { if (R() < 0.5) lessons[id] = 1 + Math.floor(R() * 10); });
  if (!Object.keys(lessons).length) lessons[ids[0]] = 8;
  const s = Object.assign(NS.defaultSettings(), { lessons, seed: Math.floor(R() * 4e9), versions: 1 + Math.floor(R() * 3),
    difficulty: ['basic', 'standard', 'honors'][Math.floor(R() * 3)], numberMode: ['integers', 'preferred', 'fractions'][Math.floor(R() * 3)], grids: R() < 0.7 });
  try {
    const ws = NS.buildWorksheet(s, 'algebra1-linear-functions'); built++;
    ws.versions.forEach(v => v.sections.forEach(sec => sec.problems.forEach(p => { probs++; if (p.attempts > maxAttempts) maxAttempts = p.attempts; })));
  } catch (e) { const k = String(e.message).slice(0, 120); errors[k] = (errors[k] || 0) + 1; errors.__last = JSON.stringify(s).slice(0, 400); }
}
console.log(`${built}/${N} worksheets built, ${probs} problems, max attempts for one problem: ${maxAttempts}`);
if (Object.keys(errors).length) { console.log('ERRORS', errors); process.exit(1); } else console.log('NO GENERATION FAILURES');
