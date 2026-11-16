'use strict';
// Re-audit fixes, 16 Nov 2026: page copy, course-scoped bank loading, tool/activity metadata,
// Financial Algebra vocabulary and duplicate questions across levels.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.join(__dirname, '..');

test('unit and course pages: public level names, short titles, whole descriptions', async () => {
  const c = await import(path.join(root, 'scripts/page-copy.mjs'));
  assert.equal(c.levelText('Pick skills and CP2, CP1 or Honors difficulty'), 'Pick skills and Support, Standard or Advanced difficulty');
  assert.equal(c.levelText('Supports CP2, CP1 and Honors.'), 'Supports Support, Standard and Advanced.');
  assert.equal(c.levelText('CP2/CP1/Honors'), 'Support/Standard/Advanced');
  assert.deepEqual(c.levelList(['CP2', 'CP1', 'Honors']), ['Support', 'Standard', 'Advanced']);
  for (const [course, unit] of [['Algebra 1', 'Quadratic Functions and Equations'], ['Statistics', 'Anticipating Patterns: Probability and Simulation'], ['Calculus', 'Limits']]) {
    assert.ok(c.unitPageTitle(course, unit).length <= 65, unit);
    const d = c.unitDescription(course, unit, [{ type: 'Game', title: 'Showdown' }, { type: 'Study Guide', title: 'Flashcards' }]);
    assert.ok(d.length <= 155 && !/…$/.test(d), d);
  }
  const groups = c.groupItems([{ type: 'Game' }, { type: 'Generator' }, { type: 'Printable' }, { type: 'Mystery' }]).map((g) => g[0]);
  assert.deepEqual(groups, ['Plan, practice and assess', 'Classroom games', 'Printable activities', 'More resources']);
  const body = c.unitBody({ courseTitle: 'Algebra 1', unitTitle: 'Quadratics', skills: ['Vertex form'], items: [{ type: 'Game', title: 'Showdown', path: 'x.html', level: ['CP2', 'CP1', 'Honors'] }], depth: 3, href: (p) => p });
  assert.match(body, /<h2>Skills in Quadratics<\/h2>/);
  assert.match(body, /\(Game, Support \/ Standard \/ Advanced\)/);
});

test('generator pages load only the course they open on', () => {
  const ctx = { console, URLSearchParams, location: { search: '', hash: '#unit=algebra1-quadratics', pathname: '/worksheet-generator/worksheet.html' } };
  ctx.window = ctx; ctx.globalThis = ctx; ctx.MK_QUESTION_BANKS = { available: () => false };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(root, 'question-bank-loader.js'), 'utf8'), ctx);
  const L = ctx.MK_BANK_LOADER;
  assert.deepEqual([...L.pageCourses()], ['algebra']);
  const cases = [
    [{ hash: '#unit=prealgebra7-ratios-proportions-percentages' }, 'prealgebra7'],
    [{ hash: '#unit=prealgebra-linear-functional-relationships' }, 'prealgebra'],
    [{ hash: '#unit=geometry-basics-reasoning&kind=maze' }, 'geometry'],
    [{ hash: '#course=algebra1&day=3' }, 'algebra'],
    [{ search: '?course=statistics&unit=statistical-inference&game=showdown' }, 'statistics'],
    [{ search: '?unit=conic-sections&game=showdown', pathname: '/worksheet-generator/algebra2-game.html' }, 'algebra2'],
    [{ hash: '#unit=grade3-multiplication-meaning' }, 'grade3']
  ];
  for (const [loc, want] of cases) {
    const got = L.pageCourses(Object.assign({ search: '', hash: '', pathname: '/x.html' }, loc));
    assert.deepEqual(got && [...got], [want], JSON.stringify(loc));
  }
  assert.equal(L.pageCourses({ search: '', hash: '', pathname: '/worksheet-generator/worksheet.html' }), null);
  for (const page of ['worksheet.html', 'menu-assessment.html', 'printables.html', 'lesson-planner.html'])
    assert.match(fs.readFileSync(path.join(root, 'worksheet-generator', page), 'utf8'), /MK_BANK_FALLBACK_COURSES=\['algebra'\]/, page);
  assert.match(fs.readFileSync(path.join(root, 'worksheet-generator/algebra2-bank-native.js'), 'utf8'), /NS\.ensureUnitBanks=/);
  assert.match(fs.readFileSync(path.join(root, 'worksheet-generator/menu/app.js'), 'utf8'), /NS\.ensureUnitBanks\(id\)/);
});

test('tool and activity pages get a description, canonical and one H1', async () => {
  const tool = await import(path.join(root, 'scripts/tool-page-meta.mjs'));
  const html = '<!doctype html><html><head><title>Classroom Activities · Mr. K\'s Classroom</title></head><body><div id="app"></div></body></html>';
  const out = tool.applyToolMeta(html, 'worksheet-generator/course-game.html');
  assert.match(out, /<html lang="en"/);
  assert.match(out, /<meta charset="utf-8">/);
  assert.match(out, /<link rel="canonical" href="https:\/\/mrksclassroom\.com\/worksheet-generator\/course-game\.html">/);
  assert.match(out, /name="description" content="Classroom review games for any unit/);
  assert.equal((out.match(/<h1/g) || []).length, 1);
  const act = await import(path.join(root, 'scripts/activity-page-meta.mjs'));
  assert.equal(act.pageTitle('A1 Line Labeler', { title: 'Line Labeler' }, 'Algebra 1'), "Line Labeler · Algebra 1 | Mr. K's Classroom");
  assert.equal(act.addStaticH1('<body><h1>Hi</h1></body>', 'X'), '<body><h1>Hi</h1></body>');
});

test('Financial Algebra vocabulary covers every unit', () => {
  const ctx = {}; ctx.window = ctx; vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(root, 'worksheet-generator/vocabulary-data-financial.js'), 'utf8'), ctx);
  const units = ['income', 'budgeting', 'banking', 'credit', 'borrowing', 'investing', 'housing', 'insurance', 'college', 'retirement'];
  for (const u of units) {
    const terms = (ctx.MKVOCAB_BANKS['financial-algebra-' + u] || '').split(';');
    assert.ok(terms.length >= 8 && terms.length <= 12, u);
    terms.forEach((t) => assert.ok(t.split('|').length >= 3, t));
  }
  assert.match(fs.readFileSync(path.join(root, 'worksheet-generator/vocabulary.html'), 'utf8'), /vocabulary-data-financial\.js/);
});

test('no question repeats word for word at two levels', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'question-banks/manifest.json'), 'utf8'));
  const dups = [];
  for (const b of manifest.banks) {
    const seen = new Map();
    for (const q of JSON.parse(fs.readFileSync(path.join(root, b.path), 'utf8')).questions) {
      const key = JSON.stringify([q.skillId, q.prompt, q.answer, q.diagram || null, q.plot || null, (q.options || []).map((o) => o.text).sort(), q.parts || null]);
      const levels = seen.get(key) || new Set(); levels.add(q.level); seen.set(key, levels);
    }
    for (const [key, levels] of seen) if (levels.size > 1) dups.push(b.path + ' ' + JSON.parse(key)[1]);
  }
  assert.deepEqual(dups, []);
});
