#!/usr/bin/env node
/* Precalculus audit #1 (2026-11-18): every Precalculus skill has teaching notes, so the planner's lessons have a real
   objective, key idea, vocabulary with meanings, a common mistake and at least one explanation card with worked steps. */
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const ROOT = path.join(__dirname, '..');

const w = { console, Math, Date, JSON }; w.window = w; w.globalThis = w; vm.createContext(w);
for (const rel of ['data.js', 'course-catalog.js', 'worksheet-generator/menu/standards.js', 'worksheet-generator/menu/standards-map.js',
  'worksheet-generator/planner/notes-teach-precalculus.js', 'worksheet-generator/planner/scope-algebra2.js'])
  vm.runInContext(fs.readFileSync(path.join(ROOT, rel), 'utf8'), w, { filename: rel });

const N = w.MKPLAN_TEACH.precalculus;
const units = Object.keys(w.MK_COURSE_CATALOG.skills.precalculus);
assert.equal(units.length, 9, 'nine Precalculus units');

/* Same rule as closeBlank in planner/notes-diagrams.js. */
function closeBlank(s, i) {
  let depth = 0;
  for (let k = i; k < s.length; k++) {
    const ch = s.charAt(k);
    if (ch === '\\') { k++; continue; }
    if (ch === '{') depth++;
    else if (ch === '}') { if (depth > 0) depth--; else if (s.charAt(k + 1) === '}') return k; }
  }
  return -1;
}
function textOk(s) {
  if ((s.match(/⟨/g) || []).length !== (s.match(/⟩/g) || []).length) return false;
  for (let k = 0; k < s.length; k++) if (s.startsWith('{{', k)) { const e = closeBlank(s, k + 2); if (e < 0) return false; k = e + 1; }
  return true;
}

let skills = 0, blanks = 0;
for (const u of units) for (const s of w.MK_COURSE_CATALOG.getSkillRecords('precalculus', u)) {
  skills++;
  const r = N[s.id];
  assert(r, 'teaching notes for ' + s.id);
  assert(r.obj && !/^work with /.test(r.obj) && r.obj === r.obj.trim(), s.id + ' objective');
  assert(r.idea && r.idea.length > 20, s.id + ' key idea');
  assert(Array.isArray(r.voc) && r.voc.length >= 2 && r.voc.every((v) => v[0] && v[1]), s.id + ' vocabulary with meanings');
  assert(r.watch, s.id + ' common mistake');
  assert(Array.isArray(r.cards) && r.cards.length >= 1, s.id + ' cards');
  for (const c of r.cards) {
    assert(c.h && c.big && Array.isArray(c.steps) && c.steps.length >= 2, s.id + ' card has a heading, explanation and steps');
    for (const t of [c.big].concat(c.steps)) { assert(textOk(t), s.id + ' markup: ' + t); blanks += (t.match(/\{\{/g) || []).length; }
  }
}
assert.equal(skills, 93, '93 Precalculus skills');
assert.equal(Object.keys(N).length, skills, 'no notes for skills outside the catalog');
assert(blanks >= 200, 'guided notes have blanks (' + blanks + ')');

/* The planner sequence uses the notes: no lesson objective falls back to "work with …". */
const scope = w.MKPLAN_SCOPE_PRECALCULUS;
const lessons = scope.days.filter((d) => d.day_type === 'Lesson');
assert.equal(lessons.length, 93, 'one planner lesson per skill');
for (const d of lessons) {
  assert(!/able to work with /.test(d.content_objective), d.lesson_id + ' objective: ' + d.content_objective);
  assert(d.key_vocabulary && d.common_misconception, d.lesson_id + ' vocabulary and misconception');
}

/* The page loads the notes before the planner scope, and notes-teach.js uses their key ideas and meanings. */
const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/lesson-planner.html'), 'utf8');
const iNotes = html.indexOf('planner/notes-teach-precalculus.js'), iScope = html.indexOf('planner/scope-algebra2.js');
assert(iNotes > 0 && iNotes < iScope, 'lesson-planner.html loads notes-teach-precalculus.js before scope-algebra2.js');
assert(/course\(\) === 'precalculus'/.test(fs.readFileSync(path.join(ROOT, 'worksheet-generator/planner/notes-teach.js'), 'utf8')),
  'notes-teach.js reads Precalculus key ideas and vocabulary meanings');

console.log('Precalculus teaching notes: ' + skills + ' skills, ' + blanks + ' blanks');
