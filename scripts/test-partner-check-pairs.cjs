#!/usr/bin/env node
/* Partner Check sheets: every row is two different problems with the same verified answer, rows never share
   an answer, problems stay at the selected level, and a sheet with fewer than 8 rows explains why.
   The audit's short selections must now reach 8 rows for every seed. Also checks the companion questions
   (tools/partner-check-companions-20261107) and the two Statistics Honors formats.
   Usage: node scripts/test-partner-check-pairs.cjs [seeds per selection, default 3] */
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const root = path.resolve(__dirname, '..'), SEEDS = +process.argv[2] || 3;
const context = { console, URLSearchParams, setTimeout, clearTimeout }; context.window = context; context.globalThis = context;
context.fetch = async url => ({ ok: true, json: async () => JSON.parse(fs.readFileSync(path.resolve(root, 'worksheet-generator', url), 'utf8')) });
vm.createContext(context);
const html = fs.readFileSync(path.join(root, 'worksheet-generator/worksheet.html'), 'utf8');
for (const m of html.matchAll(/<script[^>]*src="([^"?]+)[^"]*"[^>]*><\/script>/g)) {
  const src = m[1]; if (/vendor|math-display|menu\/app|approved-resource-preview/.test(src)) continue;
  vm.runInContext(fs.readFileSync(path.resolve(root, 'worksheet-generator', src), 'utf8'), context, { filename: src });
}
// Selections the activity audit reported with 1–3 pairs (whole unit, all skills): they must now give 8 rows.
const PRIORITY = [
  ['algebra2-functions-transformations', 'honors'], ['algebra2-quadratic-functions-complex-numbers', 'cp1'], ['algebra2-quadratic-functions-complex-numbers', 'honors'],
  ['algebra2-polynomial-functions', 'cp1'], ['algebra2-exponential-logarithmic-functions', 'cp1'], ['algebra2-rational-functions', 'cp1'], ['algebra2-rational-functions', 'honors'],
  ['algebra2-sequences-series', 'cp1'], ['algebra2-sequences-series', 'honors'], ['algebra2-conic-sections', 'honors'],
  ['calculus-precalculus-review', 'cp2'], ['calculus-precalculus-review', 'honors'], ['math6-inequalities', 'cp2'], ['math6-inequalities', 'cp1'],
  ['prealgebra7-decimals-equations', 'cp1']];

context.MK_COURSE_BANKS_READY.then(() => {
  for (const name of ['printables', 'printables-scenes', 'printables-cases', 'printables-match'])
    vm.runInContext(fs.readFileSync(path.join(root, 'worksheet-generator/menu/' + name + '.js'), 'utf8'), context);
  const N = context.MKMENU, PR = N.printables, GB = context.MKGAMES, QB = context.MK_QUESTION_BANKS;
  const nrm = s => String(s).replace(/\s+|⟨|⟩|\\,|\\left|\\right/g, '').toLowerCase();
  // authored source questions by id (level and key come from the bank file, not from the generator)
  const source = new Map();
  for (const c of context.LIBRARY.courses) for (const u of c.units)
    if (QB.available(c.id, u.id)) for (const q of QB.select({ courseId: c.id, unitId: u.id })) source.set(q.id, q);
  const verifyOne = (it, level, where) => {
    if (it.p.source === 'authored-bank') {
      const q = source.get(it.p.sourceId); assert(q, where + ': unknown source ' + it.p.sourceId);
      assert.equal(q.level, level, where + ': ' + q.id + ' is a ' + q.level + ' question on a ' + level + ' sheet');
      assert.equal(String(it.key), String(Array.isArray(q.answer) ? q.answer.join('; ') : q.answer), where + ': key differs from the bank answer');
    } else {
      assert.equal(it.p.verify && it.p.verify.status, 'verified', where + ': unverified problem');
      assert(GB.answerOk(it.p, 0, it.key).ok, where + ': verifier rejects its own key');
    }
  };
  let sheets = 0, rows = 0, short = [], priorityRuns = 0;
  for (const g of N.CATALOG) for (const u of g.units) {
    const id = u[0], set = N.skillSets[id]; if (!set) continue;
    if (!set.skills.some(s => PR.capable(id, s.id, 'partner'))) continue;
    for (const level of ['cp2', 'cp1', 'honors']) {
      const prio = PRIORITY.some(p => p[0] === id && p[1] === level), seeds = prio ? Math.max(SEEDS, 5) : SEEDS;
      for (let sd = 1; sd <= seeds; sd++) {
        const cfg = PR.defaultConfig(id, 'partner'); cfg.level = level; cfg.seed = 'pair-' + sd;
        const B = PR.build(cfg, 0), where = id + '/' + level + '/seed ' + sd;
        if (B.error) { short.push(where + ': ' + B.error); continue; }
        sheets++;
        assert(!B.levelNote || !/uses Standard|from the .* bank/i.test(B.levelNote), where + ': partner check substituted another level');
        B.rows.forEach((r, i) => {
          rows++;
          assert.notEqual(nrm(r.A.p.prompt), nrm(r.B.p.prompt), where + ' row ' + (i + 1) + ': the same problem twice');
          if (r.A.p.source === 'authored-bank') assert.notEqual(r.A.p.sourceId, r.B.p.sourceId, where + ': one question used twice');
          verifyOne(r.A, level, where + ' row ' + (i + 1) + 'A'); verifyOne(r.B, level, where + ' row ' + (i + 1) + 'B');
          const same = r.A.p.source === 'authored-bank' && r.B.p.source === 'authored-bank'
            ? PR.partnerAnswerKey(r.A.key) === PR.partnerAnswerKey(r.B.key)
            : GB.answerOk(r.A.p, 0, r.B.key).ok && GB.answerOk(r.B.p, 0, r.A.key).ok;
          assert(same, where + ' row ' + (i + 1) + ': partners do not share an answer (' + r.A.key + ' / ' + r.B.key + ')');
          B.rows.slice(i + 1).forEach((o, j) => {
            const clash = PR.partnerAnswerKey(r.A.key) === PR.partnerAnswerKey(o.A.key) || PR.clash(r.A, o.A);
            assert(!clash, where + ': rows ' + (i + 1) + ' and ' + (i + j + 2) + ' share an answer (' + r.A.key + ')');
          });
        });
        if (B.rows.length < 8) { assert(B.levelNote && /partner pairs/.test(B.levelNote), where + ': short sheet without an explanation'); short.push(where + ': ' + B.rows.length + ' rows'); }
        if (prio) { priorityRuns++; assert.equal(B.rows.length, 8, where + ': audit selection still short (' + B.rows.length + ')'); }
      }
    }
  }
  // Companion questions: same answer string as the partner named in sourceNotes, at the same level, different prompt.
  let companions = 0;
  for (const q of source.values()) {
    const m = /^Partner-check companion to (\S+) /.exec(q.sourceNotes || ''); if (!m) continue;
    const p = source.get(m[1]); assert(p, q.id + ': partner ' + m[1] + ' missing');
    assert.equal(q.answer, p.answer, q.id + ': answer differs from partner'); assert.equal(q.level, p.level, q.id + ': level differs from partner');
    assert.notEqual(nrm(q.prompt), nrm(p.prompt), q.id + ': repeats its partner'); companions++;
  }
  // Statistics Honors: Exploring Data whodunnit and Sampling and Experimentation maze build from Honors questions only.
  for (const [unit, kind] of [['statistics-exploring-data', 'who'], ['statistics-sampling-experimentation', 'maze']]) for (let sd = 1; sd <= 5; sd++) {
    const cfg = PR.defaultConfig(unit, kind); cfg.level = 'honors'; cfg.seed = 'stat-h-' + sd;
    const B = PR.build(cfg, 0), where = unit + '/' + kind + '/seed ' + sd;
    assert(!B.error, where + ': ' + B.error); assert(!B.levelNote, where + ': ' + B.levelNote);
    const items = kind === 'who' ? B.cards.map(c => c.item || c.it || c) : B.items;
    assert(items.length >= (kind === 'who' ? 10 : 8), where + ': only ' + items.length + ' problems');
    for (const it of B.items || items) { const q = source.get(it.p.sourceId); assert(q && q.level === 'honors', where + ': non-Honors question ' + (q && q.id)); }
  }
  console.log('PASS ' + sheets + ' partner sheets (' + rows + ' rows, both problems checked, answers unique per sheet); ' + priorityRuns +
    ' audit-selection runs at 8 rows; ' + companions + ' companion questions; Statistics Honors whodunnit and maze use Honors questions only. ' +
    'Short sheets with an explanation: ' + short.length);
  if (process.env.VERBOSE) short.forEach(s => console.log('  ' + s));
}).catch(e => { console.error(e); process.exitCode = 1; });
