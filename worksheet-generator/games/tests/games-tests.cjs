/* Game bank tests: every multiple-choice key verifies, every distractor is rejected by the verifier,
   and every typeable key, written the way a student would type it, is accepted. */
'use strict';
const path = require('path');
const load = require(path.join(__dirname, '..', '..', 'menu', 'tests', 'load.cjs'));
const env = load(['games/bank.js']);
const M = env.MKMENU, GB = env.MKGAMES;
const N = +(process.env.N || 6), UNIT = process.env.UNIT;
let checks = 0; const fails = [];
function ok(c, m) { checks++; if (!c) fails.push(m); }
const stats = {};
for (const setId of Object.keys(M.skillSets).filter(id => !UNIT || id === UNIT)) {
  for (const sk of M.skillSets[setId].skills) for (let c = 1; c <= 7; c++) for (let i = 0; i < N; i++) {
    const items = GB.makeItems(setId, sk.id, c, { intOnly: c <= 5, level: 'test' }, 'gt|' + i, null);
    const st = stats[setId + '/' + sk.id] = stats[setId + '/' + sk.id] || { items: 0, typed: 0, opts: 0, noMC: 0 };
    if (!items.length) st.noMC++;
    items.forEach(it => {
      st.items++; st.opts += it.options.length; if (it.typed) st.typed++;
      const tag = sk.id + ' c' + c + ' #' + i + ' (' + (it.p.parts[it.k].label || '') + ') :: ' + it.p.prompt.slice(0, 90);
      ok(it.options.filter(o => o.ok).length === 1, tag + ': exactly one correct option');
      it.options.forEach(o => { const r = GB.answerOk(it.p, it.k, o.a); ok(r.ok === o.ok, tag + ': option ' + o.a + (o.ok ? ' should verify' : ' should be rejected')); });
      ok(new Set(it.options.map(o => o.a.replace(/\s/g, ''))).size === it.options.length, tag + ': duplicate options');
      ok(it.options.length >= 2, tag + ': fewer than 2 options');
      if (it.typed) {
        const typed = /^\s*prime/i.test(it.p.parts[it.k].answer) ? 'prime' : it.typed === 'percent' ? it.p.parts[it.k].answer.trim() : GB.typedForm(it.p.parts[it.k]);
        const r = GB.checkTyped(it, typed); ok(r.ok, tag + ': typed key "' + typed + '" (' + it.typed + ') rejected as ' + r.markup);
        it.options.filter(o => !o.ok).slice(0, 1).forEach(o => { const w = it.typed === 'percent' ? o.a.trim() : GB.typedForm({ answer: o.a }); if (w) { const r2 = GB.checkTyped(it, w); ok(!r2.ok, tag + ': typed wrong answer "' + w + '" accepted'); } });
        ok(!GB.checkTyped(it, '').ok, tag + ': empty answer accepted');
        // other ways students type the same answer
        const alts = [];
        if (it.typed === 'solve') alts.push(typed.replace(/^[a-z]\s*=\s*/, ''));
        if (it.typed === 'set') alts.push(typed.replace(/[{}]/g, ''));
        if (it.typed === 'list') alts.push(typed.replace(/,/g, ' and '));
        if (/rule|formula|expr|literal/.test(it.typed)) alts.push(typed.replace(/\s+/g, ''));
        alts.forEach(a => { const r3 = GB.checkTyped(it, a); ok(r3.ok, tag + ': typed form "' + a + '" rejected as ' + r3.markup); });
      }
    });
  }
}
Object.entries(stats).forEach(([k, s]) => console.log('  ' + k.padEnd(52) + ' items ' + String(s.items).padStart(4) + '  typed ' + String(s.typed).padStart(4) + '  avg options ' + (s.opts / Math.max(1, s.items)).toFixed(2) + (s.noMC ? '  no-MC problems ' + s.noMC : '')));
if (fails.length) { console.log('FAIL: ' + fails.length + ' of ' + checks); [...new Set(fails)].slice(0, 40).forEach(f => console.log('  - ' + f)); process.exit(1); }
console.log('PASS: ' + checks + ' game-bank checks');
