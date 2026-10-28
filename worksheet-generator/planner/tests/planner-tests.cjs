/* Daily Lesson Planner tests (Node).
   • every lesson in the scope & sequence is in the skill map; every mapped skill exists and makes a verified problem
     at every difficulty in its range, for every class level
   • every day × level × seed builds: every problem verified (or flagged, which counts as a failure here),
     no repeated problem on one day, sections match the day type
   SEEDS=n (default 2). */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const load = require('../../menu/tests/load.cjs');
const env = load();
env.location = { hash: process.env.COURSE === 'geometry' ? '#course=geometry' : '' };   // COURSE=geometry tests the Geometry scope and skill map
['planner/scope-algebra1.js', 'planner/lesson-skills.js', 'planner/scope-geometry.js', 'planner/lesson-skills-geometry.js', 'planner/course.js', 'planner/planner.js'].forEach(f =>
  vm.runInContext(fs.readFileSync(path.join(__dirname, '..', '..', f), 'utf8'), env, { filename: f }));
const M = env.MKMENU, P = env.MKPLAN, SC = env.MKPLAN_SCOPE, MAP = env.MKPLAN_SKILLS;
let checks = 0, fails = [];
function ok(c, msg) { checks++; if (!c) fails.push(msg); }

// 1. map ↔ scope
const lessonIds = SC.days.filter(d => d.day_type === 'Lesson').map(d => d.lesson_id);
lessonIds.forEach(id => ok(MAP.lessons[id], 'lesson ' + id + ' missing from lesson-skills.js'));
Object.keys(MAP.lessons).forEach(id => ok(id === 'LAUNCH-2' || lessonIds.includes(id), 'skill map lists unknown lesson ' + id));
SC.days.forEach(d => ['do_now_source_ids', 'spiral_review_ids', 'lessons_covered'].forEach(k => (d[k] || []).forEach(id => ok(id === 'LAUNCH-2' || lessonIds.includes(id), 'day ' + d.day + ' ' + k + ' references unknown ' + id))));
// 2. every mapped skill × c × level
Object.keys(MAP.lessons).forEach(id => {
  const m = MAP.lessons[id];
  ok(['full', 'partial', 'none'].includes(m.cover), id + ': bad cover');
  ok(m.cover === 'full' || m.note, id + ': partial/none needs a note');
  ok(m.skills.length > 0, id + ': no skills');
  m.skills.forEach(s => {
    const set = M.skillSets[MAP.SETS[s[0]]];
    ok(set && set.byId[s[1]], id + ': unknown skill ' + s[0] + '/' + s[1]); if (!set || !set.byId[s[1]]) return;
    for (let c = s[2] || 1; c <= (s[3] || 7); c++) ['cp2', 'cp1', 'honors'].forEach(lv => {
      const pol = { intOnly: M.LEVELS[lv].intOnly, level: lv };
      const p = M.generateProblem(set.id, s[1], c, pol, 'map|' + id + '|' + c);
      ok(!p.failed, id + ' ' + s[1] + ' c' + c + ' ' + lv + ': ' + p.reason);
    });
  });
});
// 3. every day
const SEEDS = +(process.env.SEEDS || 2), t0 = Date.now(), counts = {};
let problems = 0;
SC.days.forEach(d => ['cp2', 'cp1', 'honors'].forEach(lv => { for (let s = 0; s < SEEDS; s++) {
  const plan = P.buildDay(d.day, { level: lv, seed: 'T' + s });
  const all = P.allItems(plan), keys = new Set();
  problems += all.length;
  all.forEach(p => {
    ok(!p.failed, 'day ' + d.day + ' ' + lv + ' seed ' + s + ': no verified problem for ' + (p.lesson + ' ' + p.skill) + ' (' + p.reason + ')');
    if (p.failed) return;
    ok(p.verify && p.verify.status === 'verified', 'day ' + d.day + ': unverified ' + p.skill);
    const r = M.verifyProblem(p, { intOnly: M.LEVELS[lv].intOnly, level: lv });   // re-check independently
    ok(r.ok, 'day ' + d.day + ': re-verify failed ' + p.skill + ' ' + (r.issues || []).join('; '));
    ok(!keys.has(p.key), 'day ' + d.day + ' ' + lv + ': repeated problem ' + p.key); keys.add(p.key);
    ok(p.entry.cmin <= p.c && p.c <= p.entry.cmax, 'day ' + d.day + ': c ' + p.c + ' outside ' + p.entry.cmin + '–' + p.entry.cmax);
  });
  const ids = plan.sections.map(x => x.id).join(',');
  const want = { Lesson: 'donow,notes,examples,practice,exit', Practice: 'donow,notes,practice,exit', Quiz: 'donow,practice,exit', Review: 'donow,notes,practice,exit', Assessment: 'donow,practice,exit', Flex: 'donow,notes,practice,exit', Diagnostic: 'practice,exit', 'Exam Review': 'donow,notes,practice,exit', Exam: 'practice', Project: 'donow,notes,practice,exit', Launch: 'donow,notes,practice,exit' }[d.day_type];
  ok(ids === want, 'day ' + d.day + ' (' + d.day_type + ') sections ' + ids);
  const nProb = { Lesson: 1, Practice: 1, Quiz: 1, Review: 1, Assessment: 1, Flex: 1, Diagnostic: 1, 'Exam Review': 1, Exam: 1 }[d.day_type];
  if (nProb) ok(all.length > 0, 'day ' + d.day + ' has no problems');
  if (d.day_type === 'Lesson') { const dn = plan.sections[0].groups[0].items.length; ok(dn === 4, 'day ' + d.day + ' Do Now has ' + dn); }
  counts[d.day_type] = (counts[d.day_type] || 0) + 1;
} }));
const sec = ((Date.now() - t0) / 1000).toFixed(1);
fails.slice(0, 40).forEach(f => console.log('FAIL', f));
console.log('planner: ' + checks + ' checks, ' + problems + ' problems on ' + SC.days.length + ' days × 3 levels × ' + SEEDS + ' seeds (' + sec + 's), ' + fails.length + ' failures');
process.exit(fails.length ? 1 : 0);
