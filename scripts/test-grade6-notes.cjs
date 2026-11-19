#!/usr/bin/env node
/* Grade 6 audit #12 and #19 (2026-11-19): every 6th Grade Math skill has teaching notes, so the planner's lessons have a
   real objective, key idea, vocabulary with meanings, a common mistake, a talk frame and an explanation card with worked
   steps and guided-notes blanks; skills that mostly practice Grade 7 standards are titled "(extension)". */
'use strict';
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const ROOT = path.join(__dirname, '..');

const w = { console, Math, Date, JSON }; w.window = w; w.globalThis = w; vm.createContext(w);
for (const rel of ['data.js', 'course-catalog.js', 'worksheet-generator/menu/standards.js', 'worksheet-generator/menu/standards-map.js',
  'worksheet-generator/planner/notes-teach-math6.js', 'worksheet-generator/planner/scope-algebra2.js'])
  vm.runInContext(fs.readFileSync(path.join(ROOT, rel), 'utf8'), w, { filename: rel });

const N = w.MKPLAN_TEACH.math6;
const units = Object.keys(w.MK_COURSE_CATALOG.skills.math6);
assert.equal(units.length, 7, 'seven Grade 6 units');

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
for (const u of units) for (const s of w.MK_COURSE_CATALOG.getSkillRecords('math6', u)) {
  skills++;
  const r = N[s.id];
  assert(r, 'teaching notes for ' + s.id);
  assert(r.obj && !/^work with /.test(r.obj) && r.obj === r.obj.trim(), s.id + ' objective');
  assert(r.idea && r.idea.length > 20, s.id + ' key idea');
  assert(Array.isArray(r.voc) && r.voc.length >= 2 && r.voc.every((v) => v[0] && v[1]), s.id + ' vocabulary with meanings');
  assert(r.watch, s.id + ' common mistake');
  assert(r.frame && r.frame.includes('___'), s.id + ' talk frame');
  assert(Array.isArray(r.cards) && r.cards.length >= 1, s.id + ' cards');
  for (const c of r.cards) {
    assert(c.h && c.big && Array.isArray(c.steps) && c.steps.length >= 2, s.id + ' card has a heading, explanation and steps');
    for (const t of [c.big].concat(c.steps)) { assert(textOk(t), s.id + ' markup: ' + t); blanks += (t.match(/\{\{/g) || []).length; }
    assert(/\{\{/.test([c.big].concat(c.steps).join(' ')), s.id + ' card has a guided-notes blank');
  }
}
assert.equal(skills, 53, '53 Grade 6 skills');
assert.equal(Object.keys(N).length, skills, 'no notes for skills outside the catalog');
assert(blanks >= 106, 'guided notes have blanks (' + blanks + ')');

/* The planner sequence uses the notes: no lesson objective falls back to "work with …". */
const scope = w.MKPLAN_SCOPE_MATH6;
const lessons = scope.days.filter((d) => d.day_type === 'Lesson');
assert.equal(lessons.length, 53, 'one planner lesson per skill');
for (const d of lessons) {
  assert(!/able to work with /.test(d.content_objective), d.lesson_id + ' objective: ' + d.content_objective);
  assert(d.key_vocabulary && d.common_misconception, d.lesson_id + ' vocabulary and misconception');
  assert(!/^To .*I first ___ and then ___\.$/.test(d.sentence_frame), d.lesson_id + ' uses its own talk frame');
}
const ext = lessons.filter((d) => / \(extension\)$/.test(d.title));
assert.equal(ext.length, Object.values(N).filter((r) => r.ext).length, 'every extension skill is titled (extension)');
assert.deepEqual(ext.map((d) => d.title).sort(), ['Comparing Data Displays (extension)', 'Solving One-Variable Inequalities (extension)'], 'extension skills');
for (const d of ext) assert(/Extension: most items here also practice a Grade 7 standard/.test(d.content_objective), d.lesson_id + ' extension note');
assert(!lessons.some((d) => / \(review\)$/.test(d.title)), 'no Grade 6 skill is review');

/* The page loads the notes before the planner scope, and notes-teach.js uses their key ideas and meanings. */
const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/lesson-planner.html'), 'utf8');
const iNotes = html.indexOf('planner/notes-teach-math6.js'), iScope = html.indexOf('planner/scope-algebra2.js');
assert(iNotes > 0 && iNotes < iScope, 'lesson-planner.html loads notes-teach-math6.js before scope-algebra2.js');
assert(/course\(\) === 'math6'/.test(fs.readFileSync(path.join(ROOT, 'worksheet-generator/planner/notes-teach.js'), 'utf8')),
  'notes-teach.js reads Grade 6 key ideas and vocabulary meanings');

console.log('PASS Grade 6 teaching notes: ' + skills + ' skills, ' + blanks + ' blanks, ' + ext.length + ' extension skills');
