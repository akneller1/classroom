/* Matching kinds beyond functions (menu/match-kinds*.js): every unit × level × set count × seed builds,
   every card fits only its own set (checked again here from what each card shows), and every face renders
   without NaN/undefined. Kind-specific checks re-derive each card from the set's answer.
   Run: node worksheet-generator/menu/tests/match-kinds-tests.cjs   (SEEDS=n for more builds, KIND=id for one kind) */
'use strict';
const assert = require('node:assert/strict');
const fs = require('fs'), path = require('path'), vm = require('vm');
const WG = path.resolve(__dirname, '..', '..');
const env = { console, Math, Date, JSON, Set, Map }; env.window = env; env.globalThis = env; vm.createContext(env);
for (const f of ['vendor/katex/katex.min.js', 'core/rng.js', 'menu/match-kinds.js', 'menu/match-kinds-number.js', 'menu/match-kinds-data.js', 'menu/match-kinds-advanced.js', 'menu/match-kinds-discrete.js', 'menu/match-kinds-elementary.js'])
  vm.runInContext(fs.readFileSync(path.join(WG, f), 'utf8'), env, { filename: f });
const MK = env.MKMATCH, SEEDS = +(process.env.SEEDS || 5);
let checks = 0, builds = 0; const ok = (c, m) => { checks++; assert.ok(c, m); };
const extra = require('./match-kinds-checks.cjs');
for (const id of Object.keys(MK.kinds)) {
  if (process.env.KIND && process.env.KIND !== id) continue;
  const K = MK.kinds[id];
  for (const unit of Object.keys(K.units)) {
    const Un = K.units[unit], famSets = Un.fams ? [Un.def].concat(Un.fams.length > 1 ? [Un.fams] : []).concat(Un.fams.map(f => [f])) : [[]];
    for (const fams of famSets) for (const level of ['cp2', 'cp1', 'honors']) for (const sets of (Un.setOptions || [4, 6, 8])) for (let s = 0; s < SEEDS; s++) {
      const cfg = { unit, level, sets, seed: 7000 + s * 104729 + sets * 31, fams };
      const tag = `${id} ${unit} ${fams.join('+')} ${level} ${sets} sets seed ${cfg.seed}`;
      const B = MK.build(id, cfg, s % 3); builds++;
      if (B.error && fams.length === 1 && (K.optionalFamFail || []).includes(fams[0])) continue;   // a single narrow type may not have enough sets
      ok(!B.error, tag + ': ' + B.error);
      ok(B.sets.length === sets, tag + ': number of sets');
      // ids: every type numbered 1..N once
      B.types.forEach(t => ok(B.ids[t].slice().sort((a, b) => a - b).join() === Array.from({ length: sets }, (_, i) => i + 1).join(), tag + ': ids ' + t));
      // every card against every other set
      for (let a = 0; a < sets; a++) for (let b = 0; b < sets; b++) if (a !== b) B.types.forEach(t => {
        if (K.fits) ok(!K.fits(t, B.sets[a], B.sets[b]), `${tag}: ${t} card of set ${a} also fits set ${b}`);
        else ok(K.key(t, B.sets[a]) !== K.key(t, B.sets[b]), `${tag}: ${t} cards of sets ${a} and ${b} show the same thing`);
      });
      // faces
      B.sets.forEach(st => B.types.forEach(t => ['full', 'mini', 'big'].forEach(mode => { const h = K.face(st, t, mode, B); ok(typeof h === 'string' && h.length > 10 && !/NaN|undefined|Infinity|\[object/.test(h), `${tag}: face ${t} ${mode}: ${String(h).slice(0, 200)}`); if (/katex-error/.test(h)) ok(false, `${tag}: KaTeX error in ${t}: ${h.match(/title="([^"]*)"/)?.[1]}`); })));
      if (extra[id]) extra[id](B, ok, tag, env);
      if (fams.length && Un.fams) B.sets.forEach(st => st.fam && ok(fams.includes(st.fam), tag + ': only chosen types'));
    }
  }
}
console.log('match kinds: ' + builds + ' builds, ' + checks + ' checks passed');
