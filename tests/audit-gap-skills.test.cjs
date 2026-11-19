'use strict';
/* The 2026-11-16 coverage-gap skills: each is in the catalog under a stable id, has a full
   published set at every level, carries its standard, and is reachable through the manifest. */
const test = require('node:test');
const assert = require('node:assert');
const fs = require('fs');
const path = require('path');
const root = path.join(__dirname, '..');
require(path.join(root, 'course-catalog.js'));
const catalog = globalThis.MK_COURSE_CATALOG;
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'question-banks/manifest.json'), 'utf8'));
const bank = (c, u) => JSON.parse(fs.readFileSync(path.join(root, 'question-banks', c, u + '.json'), 'utf8')).questions;

const SKILLS = [
  ['prealgebra', 'linear-functional-relationships', 12, 'Proportional relationships, unit rate, and slope', '8.EE.B.5'],
  ['prealgebra7', 'ratios-proportions-percentages', 11, 'Rewriting Expressions in Context', '7.EE.A.2'],
  ['algebra2', 'polynomial-functions', 9, "Binomial Theorem and Pascal's Triangle", 'A-APR.C.5'],
  ['precalculus', 'functions', 18, 'Solving Exponential and Logarithmic Equations', 'F-LE.A.4'],
  ['calculus', 'fundamental-theorem-calculus', 7, 'Integration Using Long Division and Completing the Square', 'AP FUN-6.D'],
  // Statistics audit 2026-11-18: tagged to the AP framework effective fall 2026; goodness of fit and slope tests are Beyond AP.
  ['statistics', 'statistical-inference', 12, 'Beyond AP: Chi-Square Goodness-of-Fit Tests', /^APSTATS\.BEYOND\.GOF$/],
  ['statistics', 'statistical-inference', 13, 'Chi-Square Tests for Homogeneity and Independence', /^APSTATS\.3\.1[45]\.[A-D]$/],
  ['statistics', 'statistical-inference', 14, 'Beyond AP: Significance Tests for the Slope of a Regression Line', /^APSTATS\.BEYOND\.SLOPE$/],
  ['geometry', 'right-triangles-trigonometry', 11, 'Law of Sines and Law of Cosines', 'G-SRT.D.11'],
  ['geometry', 'foundations-geometry', 10, 'Conditional Statements, Converses, and Biconditionals', 'G-CO.C.9']
];

for (const [course, unit, index, name, standard] of SKILLS) {
  test(`${course}/${unit}: "${name}" is published as skill ${index}`, () => {
    const record = catalog.getSkillRecords(course, unit)[index - 1];
    assert.ok(record, 'skill is missing from the catalog');
    assert.strictEqual(record.name, name);
    assert.ok(manifest.banks.some(b => b.courseId === course && b.unitId === unit && (b.approved || b.teacherUse)), 'bank is not published in the manifest');
    const items = bank(course, unit).filter(q => q.skillId === record.id);
    const pairs = course === 'statistics' ? 2 : 0; // Statistics adds one Partner Check pair per level
    if (course === 'statistics') assert.ok(items.length >= 48 + 3 * pairs, 'count'); // later audits add items
    else assert.strictEqual(items.length, 48 + 3 * pairs);
    for (const level of ['cp2', 'cp1', 'honors']) {
      const set = items.filter(q => q.level === level);
      if (course === 'statistics') assert.ok(set.length >= 16 + pairs, level + ' count');
      else assert.strictEqual(set.length, 16 + pairs, level + ' count');
      if (pairs) {
        const pair = set.filter(q => q.partnerRole);
        assert.deepStrictEqual(pair.map(q => q.partnerRole).sort(), ['A', 'B'], level + ' partner pair');
        assert.strictEqual(pair[0].answer, pair[1].answer, level + ' partner answers match');
      }
      assert.ok(set.filter(q => q.format === 'multiple-choice').length >= 6, level + ' multiple choice');
      assert.ok(set.some(q => q.format === 'open-response' && q.parts.length === 4), level + ' open response');
    }
    const single = items.filter(q => q.format !== 'open-response');
    assert.strictEqual(new Set(single.map(q => q.prompt)).size, single.length, 'prompts repeat');
    for (const q of items) {
      assert.ok(standard instanceof RegExp ? q.standards.some(c => standard.test(c)) : q.standards.includes(standard), q.id + ' standard');
      assert.ok(q.answer && q.solutionSteps.length, q.id + ' answer and steps');
      if (q.format === 'multiple-choice') {
        assert.strictEqual(q.options.length, 4, q.id);
        assert.strictEqual(new Set(q.options.map(o => o.text)).size, 4, q.id + ' options repeat');
        assert.deepStrictEqual(q.options.filter(o => o.correct).map(o => o.text), [q.answer], q.id);
      }
    }
  });
}

test('new skills do not disturb existing skill ids', () => {
  assert.strictEqual(catalog.getSkillRecords('statistics', 'statistical-inference')[10].name, 'Beyond AP: Confidence Intervals for a Regression Slope');
  assert.strictEqual(catalog.getSkillRecords('geometry', 'foundations-geometry')[8].name, 'Compass-and-Straightedge Constructions');
  assert.strictEqual(catalog.getSkillRecords('geometry', 'right-triangles-trigonometry')[9].name, 'Right-Triangle Word Problems');
});

test('existing items that already teach a standard are tagged with it', () => {
  const tagged = (c, u, code) => bank(c, u).filter(q => q.standards.includes(code)).length;
  assert.ok(tagged('math6', 'expressions-equations', '6.EE.B.6') >= 30);
  assert.ok(tagged('math6', 'data-displays', '6.SP.A.3') >= 20);
  assert.ok(tagged('prealgebra7', 'operations-fractions', '7.NS.A.3') >= 60);
});

test('no Algebra 2 prompt refers to a graph that is not attached', () => {
  const dir = path.join(root, 'question-banks/algebra2');
  for (const file of fs.readdirSync(dir).filter(f => f.endsWith('.json'))) {
    for (const q of JSON.parse(fs.readFileSync(path.join(dir, file), 'utf8')).questions) {
      if (/^Use the graph\b|graph (shown|below|above)/.test(q.prompt)) assert.ok(q.diagram || q.plot || q.image, q.id + ' mentions a graph but has none');
    }
  }
});

test('the worksheet generator serves every new skill at every level', async () => {
  const vm = require('node:vm');
  const ctx = { console, URLSearchParams, setTimeout, clearTimeout };
  ctx.window = ctx; ctx.globalThis = ctx;
  ctx.fetch = async url => ({ ok: true, json: async () => JSON.parse(fs.readFileSync(path.resolve(root, 'worksheet-generator', url))) });
  vm.createContext(ctx);
  for (const m of fs.readFileSync(path.join(root, 'worksheet-generator/worksheet.html'), 'utf8').matchAll(/<script[^>]*src="([^"?]+)[^"]*"[^>]*><\/script>/g)) {
    if (/vendor|math-display|menu\/app|approved-resource-preview/.test(m[1])) continue;
    vm.runInContext(fs.readFileSync(path.resolve(root, 'worksheet-generator', m[1]), 'utf8'), ctx, { filename: m[1] });
  }
  await ctx.MK_COURSE_BANKS_READY;
  const N = ctx.MKMENU;
  const setId = (course, unit) => course === 'geometry' && unit === 'foundations-geometry' ? 'geometry-basics-reasoning' : course + '-' + unit;
  for (const [course, unit, index] of SKILLS) {
    const id = setId(course, unit), skill = unit + '-skill-' + String(index).padStart(2, '0');
    assert.ok(N.skillSets[id] && N.skillSets[id].byId[skill], id + ' does not list ' + skill);
    for (const level of ['cp2', 'cp1', 'honors']) {
      for (const format of ['short-answer', 'multiple-choice']) {
        const used = { keys: new Set(), sigs: new Set() }, seen = new Set();
        for (let i = 0; i < 5; i++) {
          const p = N.generateProblem(id, skill, 4, { level, authoredFormats: [format], adjacentLevels: false }, 'gap-' + level + format + i, used);
          assert.ok(!p.failed, `${skill} ${level} ${format} draw ${i} failed`);
          assert.strictEqual(p.source, 'authored-bank');
          assert.ok(p.prompt && p.parts && p.parts.length && p.parts.every(part => part.answer), skill + ' prompt and answer');
          if (format === 'multiple-choice') assert.ok(!N.makeChoices(p).fail, skill + ' choices');
          seen.add(p.prompt);
        }
        assert.strictEqual(seen.size, 5, `${skill} ${level} ${format} repeated a question`);
      }
    }
  }
});
