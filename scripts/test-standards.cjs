#!/usr/bin/env node
/* Standards on teacher copies: the skill map is current, every mapped code has a summary,
   codes normalize consistently, and the summary/chip HTML is well formed.
   Run: node scripts/test-standards.cjs */
'use strict';
const path = require('path'), { execFileSync } = require('child_process');
const ROOT = path.resolve(__dirname, '..');
let fails = 0;
function ok(c, msg) { if (!c) { fails++; console.error('FAIL ' + msg); } }

execFileSync(process.execPath, [path.join(ROOT, 'scripts/build_standards_map.cjs'), '--check'], { stdio: 'inherit' });
const STD = require(path.join(ROOT, 'worksheet-generator/menu/standards.js'));
require(path.join(ROOT, 'worksheet-generator/menu/standards-map.js'));
const M = globalThis.MKSTD_SKILLS;

[['A.SSE.A.1a', 'A-SSE.A.1a'], ['HSA-REI.B.4b', 'A-REI.B.4b'], ['7.NS.A.2.D', '7.NS.A.2d'], ['N.RN.B.3', 'N-RN.B.3'], ['G-CO', 'G-CO'],
 ['AP FUN-5.A', 'AP FUN-5.A'], ['APSTATS.I.B.3', 'APSTATS.I.B.3'], ['SMP 1–8', 'SMP 1–8'], ['8.EE.A.1', '8.EE.A.1']]
  .forEach(([a, b]) => ok(STD.norm(a) === b, 'norm ' + a + ' → ' + STD.norm(a) + ' (want ' + b + ')'));

let n = 0;
Object.keys(M).forEach(set => Object.keys(M[set]).forEach(skill => {
  const list = M[set][skill]; n++;
  ok(Array.isArray(list) && list.length, set + ':' + skill + ' has no standards');
  list.forEach(c => { ok(STD.describe(c), set + ':' + skill + ' ' + c + ' has no summary'); ok(STD.norm(c) === c, c + ' is not normalized'); });
}));
ok(n > 700, 'only ' + n + ' skills mapped');
['algebra1-foundations', 'algebra1-quadratics', 'geometry-triangles-congruence', 'algebra2-conic-sections', 'math6-geometry']
  .forEach(set => ok(M[set] && Object.keys(M[set]).length, set + ' missing'));

/* A bank question's own content tags win; practice-only tags fall back to the skill. */
ok(STD.forProblem({ skill: 'q-roots', standards: ['F-IF.C.8a', 'MP.1'] }, 'algebra1-quadratics').join() === 'F-IF.C.8a', 'own tags');
ok(STD.forProblem({ skill: 'q-roots' }, 'algebra1-quadratics').join() === M['algebra1-quadratics']['q-roots'].join(), 'skill tags');
ok(STD.forProblem({ skill: 'x', failed: true }, 'algebra1-quadratics').length === 0, 'failed problem');

const html = STD.summaryHtml([{ label: '1', codes: ['A-REI.B.4b'] }, { label: '2', codes: ['A-REI.B.4b', 'F-IF.C.7a'] }, { label: '3', codes: ['A-REI.B.4b'] }]);
ok(/Common Core standards addressed/.test(html) && /1–3/.test(html) && /F-IF\.C\.7a/.test(html), 'summary html');
ok(STD.summaryHtml([]) === '', 'empty summary');
ok(/AP Statistics/.test(STD.summaryHtml([{ codes: ['APSTATS.I.B.3'] }])), 'AP title');
ok(/mk-std-chip/.test(STD.chipsHtml(['A-APR.A.1'])) && STD.chipsHtml([]) === '', 'chips');
ok(/<li><b>A-SSE\.A\.1<\/b> — /.test(STD.listHtml('A.SSE.A.1, SMP 1–8')), 'planner list');

/* Exercise real worksheet/test/menu standards tables with the existing generator engines. */
const env = require(path.join(ROOT, 'worksheet-generator/menu/tests/load.cjs'))(['menu/standards.js', 'menu/standards-map.js', 'menu/render.js']);
let generatedKeys = 0;
for (const set of ['algebra1-quadratics', 'geometry-triangles-congruence'])
  for (const mode of ['worksheet', 'test', 'menu'])
    for (const level of ['cp2', 'cp1', 'honors']) {
      const cfg = env.MKMENU.defaultConfig(set, mode);
      cfg.level = level; cfg.versions = 1; cfg.seed = 'standards-verification';
      const state = env.MKMENU.newAssessment(cfg);
      const block = env.MKMENU.standardsBlock(state, 0);
      ok(block && /Common Core standards addressed/.test(block.html), set + '/' + mode + '/' + level + ' teacher standards table');
      generatedKeys++;
    }
console.log('Teacher standards tables: ' + generatedKeys + ' worksheet/test/menu configurations checked');

console.log(fails ? fails + ' standards checks failed' : 'standards: ' + n + ' skills mapped, all checks passed');
process.exit(fails ? 1 : 0);
