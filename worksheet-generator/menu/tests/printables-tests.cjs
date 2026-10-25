/* Printable Generators (printables.html): every unit × printable × level, checked independently of the builders.
   Run: node worksheet-generator/menu/tests/printables-tests.cjs   (SEEDS=n for more builds) */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(['games/bank.js', 'menu/printables.js']), M = env.MKMENU, PR = M.printables, GB = env.MKGAMES;
const SEEDS = +(process.env.SEEDS || 2);
let checks = 0, builds = 0; const ok = (c, m) => { checks++; assert.ok(c, m); };
const accepts = (p, a) => GB.answerOk(p, 0, a).ok;
/* Printables a unit cannot make (too few short problems): listed here so a new gap fails the test. */
const UNSUPPORTED = { 'algebra1-statistics-data-modeling': ['tarsia'] };

function verified(it, tag) {
  ok(it.p.verify && it.p.verify.status === 'verified', tag + ': problem verified');
  ok(accepts(it.p, it.key), tag + ': the key is accepted');
}
const CHECK = {
  maze(B, tag) {
    const at = (r, c) => B.rooms.find(x => x.r === r && x.c === c);
    ok(B.path.length >= 10 && B.path.length <= 13, tag + ': path of 10–13 rooms');
    ok(B.path[0].join() === '0,0' && B.path[B.path.length - 1].join() === '3,3', tag + ': START to FINISH');
    B.rooms.forEach(rm => {
      if (rm.finish) return;
      verified(rm.item, tag);
      const mine = B.doors.filter(d => (d.a[0] === rm.r && d.a[1] === rm.c) || (d.b[0] === rm.r && d.b[1] === rm.c));
      const acc = mine.filter(d => accepts(rm.item.p, d.label));
      if (rm.step === null) ok(acc.length === 0, tag + ': a dead end has no door with its answer');
      else {
        ok(acc.length === 1, tag + ': exactly one door accepts the answer of path room ' + rm.step);
        const nxt = B.path[rm.step + 1], d = acc[0], other = d.a[0] === rm.r && d.a[1] === rm.c ? d.b : d.a;
        ok(other.join() === nxt.join(), tag + ': that door leads to the next room on the path');
      }
    });
    const keys = B.rooms.filter(r => !r.finish).map(r => r.item);
    keys.forEach((a, i) => keys.forEach((b, j) => { if (i < j) ok(!accepts(a.p, b.key) && !accepts(b.p, a.key), tag + ': rooms have different answers'); }));
    void at;
  },
  color(B, tag) {
    const N = B.items.length;
    B.items.forEach(it => verified(it, tag));
    for (let n = 1; n <= N; n++) ok(B.cells.some(row => row.includes(n)), tag + ': problem ' + n + ' is in the picture');
    B.cells.forEach((row, r) => row.forEach((n, c) => ok(B.colorOf[n - 1] === B.grid[r][c], tag + ': square color matches its problem')));
    B.code.forEach(k => k.answers.forEach(a => { const i = B.items.findIndex(it => it.key === a); ok(i >= 0 && B.colorOf[i] === k.ch, tag + ': color code lists the right answers'); }));
    B.items.forEach((a, i) => B.items.forEach((b, j) => { if (i < j) ok(!accepts(a.p, b.key) && !accepts(b.p, a.key), tag + ': answers are all different'); }));
  },
  partner(B, tag) {
    ok(B.rows.length >= 4, tag + ': at least four rows');
    B.rows.forEach(r => {
      verified(r.A, tag); verified(r.B, tag);
      ok(r.A.p.prompt !== r.B.p.prompt, tag + ': different problems');
      ok(accepts(r.A.p, r.B.key) && accepts(r.B.p, r.A.key), tag + ': partners have the same answer');
    });
  },
  error(B, tag) {
    ok(B.cases.length >= 4, tag + ': at least four cases');
    B.cases.forEach(cs => {
      verified(cs.item, tag);
      ok(!accepts(cs.item.p, cs.wrong), tag + ': the student’s answer is wrong (' + cs.wrong + ')');
      const shown = cs.work.filter(l => l.bad);
      ok(shown.length <= 1, tag + ': at most one changed line');
    });
  },
  tarsia(B, tag) {
    const inner = B.items.length;
    ok(inner === (B.shape === 'hexagon' ? 30 : 18), tag + ': every inner edge is a match');
    B.items.forEach(it => verified(it, tag));
    B.items.forEach((a, i) => B.items.forEach((b, j) => { if (i < j) ok(!accepts(a.p, b.key) && !accepts(b.p, a.key), tag + ': answers are all different'); }));
    let q = 0, a = 0, d = 0;
    B.pieces.forEach(pc => pc.kind.forEach((k, e) => { if (k === 'q') q++; if (k === 'a') a++; if (k === 'd') { d++; ok(!B.items.some(it => accepts(it.p, pc.text[e])), tag + ': a border decoy matches no problem'); } }));
    ok(q === inner && a === inner, tag + ': one problem edge and one answer edge per match');
    ok(new Set(B.scrambled.map(s => s.piece)).size === B.pieces.length, tag + ': the student copy has every piece once');
  }
};

for (const unit of Object.keys(M.skillSets)) for (const kind of PR.KINDS.map(k => k.id)) for (const level of ['cp2', 'cp1', 'honors']) for (let s = 0; s < SEEDS; s++) {
  const cfg = PR.defaultConfig(unit, kind); cfg.level = level; cfg.seed = 500 + s;
  const B = PR.build(cfg, s % 2), tag = unit + ' ' + kind + ' ' + level;
  if ((UNSUPPORTED[unit] || []).includes(kind)) { ok(!!B.error, tag + ': listed as unsupported (remove it from UNSUPPORTED if it works now)'); continue; }
  ok(!B.error, tag + ': built (' + (B.error || '') + ')');
  CHECK[kind](B, tag); builds++;
}
// versions differ
{ const cfg = PR.defaultConfig('algebra1-quadratics', 'maze'); cfg.seed = 9; const A = PR.build(cfg, 0), B = PR.build(cfg, 1);
  ok(A.rooms[0].item.p.prompt !== B.rooms[0].item.p.prompt, 'Version B has different problems'); }
console.log('PASS: ' + builds + ' printables built, ' + checks + ' checks');
