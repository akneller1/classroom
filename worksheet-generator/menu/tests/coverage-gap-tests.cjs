/* Skills added to close earlier coverage gaps (Algebra 1 and Geometry): registration, class → unit browsing,
   topic search, verified variety at every difficulty, wrong answers rejected, the response formats each skill
   supports (and only those), regeneration that keeps skill, difficulty and format, and the property classifier. */
'use strict';
const assert = require('node:assert/strict'), fs = require('fs'), vm = require('vm'), path = require('path');
const env = require('./load.cjs')(['games/bank.js', 'menu/render.js']), NS = env.MKMENU, GB = env.MKGAMES;
const app = fs.readFileSync(path.join(__dirname, '../app.js'), 'utf8');
vm.runInContext(app.slice(app.indexOf('  // Topic worksheets'), app.indexOf('  /* ---------------- start ---------------- */')) + '\nregisterTopicSets();',
  Object.assign(env, { NS, doc: {}, S: null, draft: null, ui: {}, snapshot() {}, render() {}, autosave() {}, classGroup() {}, console }));
let checks = 0; const ok = (c, m) => { checks++; assert.ok(c, m); };

// [unit, skill, search words, formats expected to work at (c) → true/false]
const NEW = [
  ['algebra1-foundations', 'properties', 'properties', { mc: [1, 4, 7], multi: [2, 5], mcas: [4, 6] }],
  ['algebra1-foundations', 'real-number-operations', 'integers fractions', { mc: [2, 4, 6] }],
  ['algebra1-foundations', 'interpret-expression', 'interpret expression', { mc: [2, 4] }],
  ['algebra1-linear-equations-slope', 'direct-variation', 'direct variation', { mc: [2, 5], mcas: [5] }],
  ['algebra1-quadratics', 'table-model-type', 'quadratic exponential', { mc: [2, 5] }],
  ['geometry-angles-parallel-lines', 'angle-pairs-figure', 'angle pairs', { mc: [2, 4], multi: [2] }],
  ['geometry-angles-parallel-lines', 'parallel-lines-converse', 'converse', {}],
  ['geometry-triangles-congruence', 'congruence-rigid-motions', 'rigid motions', {}],
  ['geometry-triangle-relationships', 'triangle-concurrency-name', 'concurrency', { mc: [2, 5] }],
  ['geometry-triangle-relationships', 'triangle-circumcenter-incenter', 'circumcenter', { mc: [2, 5] }],
  ['geometry-similarity', 'similarity-area-volume-ratio', 'similar figures', { mc: [2, 5] }],
  ['geometry-similarity', 'similarity-area-investigation', 'similar figures', { mcas: [5, 7] }],
  ['geometry-right-triangles-trigonometry', 'law-of-sines', 'law of sines', { mc: [5, 7] }],
  ['geometry-right-triangles-trigonometry', 'law-of-cosines', 'law of cosines', { mc: [5, 7] }],
  ['geometry-quadrilaterals-polygons', 'kite-isosceles-trapezoid', 'kite', { mc: [2, 5] }],
  ['geometry-transformations', 'transformation-sequence-congruence', 'glide', {}],
  ['geometry-area-surface-area-volume', 'measure-pyramid-surface', 'pyramid surface', { mc: [2, 5] }],
  ['geometry-area-surface-area-volume', 'measure-cone-surface', 'cone surface', { mc: [2, 6] }],
  ['geometry-area-surface-area-volume', 'measure-composite-round', 'composite', { mc: [3, 6] }],
  ['geometry-area-surface-area-volume', 'measure-unit-conversion', 'conversion', { mc: [2, 5] }],
  ['geometry-area-surface-area-volume', 'measure-similar-solids', 'similar solids', { mc: [2, 6] }]
];

/* 1. registration, class → unit browsing and topic search */
for (const [unit, skill, words] of NEW) {
  const set = NS.skillSets[unit]; ok(set && set.byId[skill], unit + ': ' + skill + ' registered');
  ok(set.tags[set.byId[skill].tag], skill + ': its tag is listed, so the skill is shown in step 4');
  const group = NS.CATALOG.find(g => g.units.some(u => u[0] === unit)); ok(group, unit + ' is in the class catalog');
  const topic = NS.skillSets[env.topicId ? env.topicId(group) : 'topic-' + group.course.toLowerCase().replace(/[^a-z0-9]+/g, '-')];
  ok(topic && topic.byId[unit + ':' + skill], skill + ' is searchable in the ' + group.course + ' topic set');
  const sugg = env.topicSuggestionsFor(group, words); ok(sugg.length > 0, 'topic suggestions for "' + words + '"');
  ok(NS.skillSets['topic-all'].byId[unit + ':' + skill], skill + ' is in the all-classes topic set');
}
ok(!NS.skillSets['algebra1-foundations'].gaps.length, 'Unit 1 has no remaining gap warning');

/* 2. verified, distinct questions at every difficulty; difficulty changes the problems; wrong answers rejected */
for (const [unit, skill] of NEW) for (let c = 1; c <= 7; c++) for (const intOnly of [true, false]) {
  const used = { keys: new Set(), sigs: new Set() }, variants = new Set();
  for (let i = 0; i < 12; i++) {
    const p = NS.generateProblem(unit, skill, c, { intOnly, level: 'x' }, 'gap|' + c + '|' + i + intOnly, used);
    ok(!p.failed, skill + ' c' + c + ' #' + i + ': ' + p.reason);
    ok(p.verify.status === 'verified' && NS.verifyProblem(p, { intOnly }).ok, skill + ' c' + c + ': verified');
    ok(Array.isArray(p.steps) && p.steps.length >= 1, skill + ': worked steps');
    variants.add(p.variant);
    p.parts.forEach((pt, k) => (pt.check.alts || []).forEach(a => { ok(!GB.answerOk(p, k, a).ok, skill + ' c' + c + ': distractor ' + a + ' must be rejected'); }));
    const wrong = JSON.parse(JSON.stringify(p)); wrong.parts[0].answer = wrong.parts[0].answer.replace(/(\d+)(?!.*\d)/, d => String(+d + 7)).replace(/^(Yes|No)\b/, w => w === 'Yes' ? 'No' : 'Yes');
    if (wrong.parts[0].answer !== p.parts[0].answer && !/Property|angles|pair|center|cent(er|roid)|inside|outside|Congruent|Similar|Linear|Quadratic|Exponential|fee|cost/.test(p.parts[0].answer)) ok(!NS.verifyProblem(wrong, { intOnly: false }).ok, skill + ' c' + c + ': a changed answer is rejected (' + wrong.parts[0].answer + ')');
  }
}
{ // difficulty changes the mathematics: CP2 warm-ups name a property of whole numbers; Honors adds variables, negatives, reciprocals and four-step justifications
  const lo = [], hi = new Set();
  for (let i = 0; i < 20; i++) { lo.push(NS.generateProblem('algebra1-foundations', 'properties', 1, { intOnly: true, level: 'x' }, 'lo' + i, null)); hi.add(NS.generateProblem('algebra1-foundations', 'properties', 7, { intOnly: false, level: 'x' }, 'hi' + i, null).variant.split('-')[1]); }
  ok(lo.every(p => !/[a-z]/.test(p.parts[0].check.eq.replace(/\\[a-z]+/g, ''))), 'CP2 warm-up properties use whole numbers only');
  ok(hi.size >= 4, 'Honors properties mix several question types (' + [...hi] + ')');
}

/* 3. response formats: each skill works in the formats it supports; unsupported combinations are reported, never substituted */
for (const [unit, skill, , fm] of NEW) {
  for (const f of ['mc', 'multi', 'mcas']) for (const c of (fm[f] || [])) ok(NS.skillFormatOk(unit, skill, f, c), skill + ' supports ' + f + ' at c' + c);
  if (!fm.multi) ok(!NS.skillFormatOk(unit, skill, 'multi', 4), skill + ': choose-all is reported as unsupported');
}
ok(!NS.skillFormatOk('algebra1-foundations', 'properties', 'mcas', 2), 'properties: no four-part question at CP2 difficulty is reported, not substituted');
{ // a four-part section keeps the requested skill from its minimum difficulty up
  const c = NS.defaultConfig('algebra1-foundations', 'worksheet'); c.level = 'honors'; c.versions = 1; c.coverage.on = false; c.skills = { properties: true };
  c.sections = [{ id: NS.uid('s'), name: 'OR', note: '', points: 1, offered: 3, required: 3, tier: 'ramp', adjust: 0, skills: ['properties'], qformat: 'mcas' }];
  const st = NS.newAssessment(c); st.versions[0].sections[0].items.forEach(it => { ok(it.skill === 'properties' && !it.mcasFail && it.parts.length >= 4, 'Open Response keeps the properties skill'); });
}
// multiple choice: four options, exactly the key accepted
for (const [unit, skill, , fm] of NEW) for (const c of (fm.mc || [])) {
  let made = 0;
  for (let i = 0; i < 6 && made < 2; i++) { const p = NS.generateProblem(unit, skill, c, { intOnly: c <= 5, level: 'x' }, 'mc' + i, null); const m = NS.makeChoices(p); if (m.fail) continue; made++;
    const q = m.derived || p; ok(m.opts.length === 4 && new Set(m.opts).size === 4, skill + ': four different choices');
    m.opts.forEach((o, k) => ok(GB.answerOk(q, 0, o).ok === (k === m.key), skill + ': only the key is accepted (' + o + ')')); }
  ok(made > 0, skill + ' c' + c + ': makes multiple-choice questions');
}
// choose-all: properties and angle pairs build checked option sets
for (const [unit, skill, c] of [['algebra1-foundations', 'properties', 3], ['geometry-angles-parallel-lines', 'angle-pairs-figure', 2]]) {
  let made = 0;
  for (let i = 0; i < 10; i++) { const p = NS.generateProblem(unit, skill, c, { intOnly: true, level: 'x' }, 'ms' + i, null), m = NS.makeMultiSelect(p); if (m.fail) continue; made++;
    ok(m.opts.length === 5 && m.keys.length >= 2 && m.keys.length <= 3, skill + ': five options, two or three correct');
    ok(m.derived && NS.verifyProblem(m.derived, { intOnly: false }).ok, skill + ': the choose-all question verifies');
    const flipped = JSON.parse(JSON.stringify(m.derived)); flipped.parts[0].answer = m.opts.filter((o, k) => !m.keys.includes(k)).join('; ');
    ok(!NS.verifyProblem(flipped, { intOnly: false }).ok, skill + ': selecting the wrong options is rejected'); }
  ok(made >= 3, skill + ': choose-all questions are made');
}

/* 4. several distinct questions of one skill, and regeneration that keeps skill, difficulty and format */
for (const [unit, skill, fmt, level] of [['algebra1-foundations', 'properties', 'mc', 'cp1'], ['geometry-right-triangles-trigonometry', 'law-of-sines', 'open', 'honors'], ['algebra1-foundations', 'properties', 'multi', 'cp2']]) {
  const c = NS.defaultConfig(unit, 'worksheet'); c.level = level; c.versions = 1; c.coverage.on = false; c.skills = {}; c.skills[skill] = true;
  c.sections = [{ id: NS.uid('s'), name: 'P', note: '', points: 1, offered: 6, required: 6, tier: 'ramp', adjust: 0, skills: [skill], qformat: fmt }];
  const st = NS.newAssessment(c), items = st.versions[0].sections[0].items;
  ok(new Set(items.map(i => i.key + JSON.stringify((i.multi || i.mc || {}).opts || null))).size === items.length, skill + ' ' + fmt + ': distinct questions');
  items.forEach(it => ok(it.skill === skill && !it.failed && (fmt !== 'mc' || it.mc) && (fmt !== 'multi' || it.multi), skill + ' ' + fmt + ': requested skill and format'));
  const before = items[2], r = NS.regenerate(st, 0, before.uid), after = st.versions[0].sections[0].items[2];
  ok(after && !after.failed && after.skill === skill && after.c === before.c && after.key !== before.key && (fmt !== 'mc' || after.mc) && (fmt !== 'multi' || after.multi), skill + ' ' + fmt + ': regenerate keeps skill, difficulty and format'); void r;
  // the student copy prints no answers, the key prints them
  const student = NS.studentText(after);
  ok(!/Answer:/.test(student), skill + ': no answer text in the student prompt');
}
{ // topic search: several distinct previews of a new skill, same skill and format
  const group = NS.CATALOG.find(g => g.course === 'Geometry'), sk = NS.skillSets['topic-all'].byId['geometry-quadrilaterals-polygons:kite-isosceles-trapezoid'];
  const c = NS.defaultConfig('geometry-quadrilaterals-polygons', 'worksheet'); c.level = 'cp1'; c.coverage.on = false; c.skills = { 'kite-isosceles-trapezoid': true };
  c.sections = [{ id: NS.uid('s'), name: sk.name, note: '', points: 1, offered: 1, required: 1, tier: 1, adjust: 0, skills: ['kite-isosceles-trapezoid'], qformat: 'mc' }];
  const st = NS.newAssessment(c); env.gapItem = { p: st.versions[0].sections[0].items[0], section: c.sections[0], skill: sk.id, tag: sk.tag, format: 'mc', unit: 'geometry-quadrilaterals-polygons', level: 'cp1' };
  vm.runInContext('var gapBatch=topicQuestionBatch(gapItem,4,[]);', env);
  ok(env.gapBatch.length === 4 && new Set(env.gapBatch.map(env.topicQuestionKey)).size === 4, 'topic search: four distinct kite/trapezoid previews');
  env.gapBatch.forEach(x => ok(x.p.skill === 'kite-isosceles-trapezoid' && x.p.mc, 'topic search: same skill, multiple choice kept')); void group;
}

/* 5. the property classifier: exactly one property, or the question is rejected */
const P = NS.propertyCheck, E = {
  '8+15=15+8': 'comm-add', 'x\\cdot 7=7x': 'comm-mul', '(3+8)+12=3+(8+12)': 'assoc-add', '3(4x)=(3\\cdot 4)x': 'assoc-mul', '27+0=27': 'id-add', '7y\\cdot 1=7y': 'id-mul',
  '-3x+3x=0': 'inv-add', '\\frac{2}{5}\\cdot\\frac{5}{2}=1': 'inv-mul', '0\\cdot 41=0': 'zero', '-2(x-5)=-2x+10': 'dist', '4(x+5)=4(5+x)': 'comm-add', '(x+6)+2=2+(x+6)': 'comm-add', '6x+18=6(x+3)': 'dist' };
for (const [eq, want] of Object.entries(E)) ok(P.of(eq) === want, 'classifier: ' + eq + ' → ' + want + ' (got ' + P.of(eq) + ')');
ok(P.of('(2+3)+4=2+(4+3)') === null, 'two properties at once (regroup and reorder) is rejected');
ok(P.of('2+3=5') === null && P.of('3(x+4)=3x+4') === null && P.of('x+x=x+x') === null && P.of('1\\cdot(4x-3)=4x-3') === null, 'not a property / false / trivial equations are rejected');
ok(P.code('Additive identity') === 'id-add' && P.code('Zero Product Property') === null && P.code('associative') === null, 'names: ambiguous or wrong names are not read as a property');

console.log('Coverage-gap tests passed: ' + NEW.length + ' skills, ' + checks + ' checks (registration, browsing, search, variety, wrong answers, formats, regeneration, classifier).');
