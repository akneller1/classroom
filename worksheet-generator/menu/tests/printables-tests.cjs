/* Printable Generators (printables.html): every unit × printable × level, checked independently of the builders.
   Run: node worksheet-generator/menu/tests/printables-tests.cjs   (SEEDS=n for more builds) */
'use strict';
const assert = require('node:assert/strict');
const load = require('./load.cjs');
const env = load(['games/bank.js', 'menu/printables.js', 'menu/printables-scenes.js', 'menu/printables-cases.js']), M = env.MKMENU, PR = M.printables, GB = env.MKGAMES;
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
    ok(B.path.length >= 10 && B.path.length <= 12, tag + ': path of 10–12 rooms');
    for (let i = 1; i < B.path.length; i++) ok(Math.max(Math.abs(B.path[i][0] - B.path[i - 1][0]), Math.abs(B.path[i][1] - B.path[i - 1][1])) === 1, tag + ': each step goes to a neighboring room');
    const blocks = {}; B.doors.filter(d => d.kind === 'd' || d.kind === 'a').forEach(d => { const k = Math.min(d.a[0], d.b[0]) + ',' + Math.min(d.a[1], d.b[1]); ok(!blocks[k], tag + ': one diagonal door per corner'); blocks[k] = 1; });
    B.doors.forEach(d => ok(PR.natural(d.label), tag + ': door labels look like real answers (' + d.label + ')'));
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
    const sc = PR.SCENES[B.scene], N = B.items.length;
    ok(N === sc.groups.length, tag + ': one problem per color');
    B.items.forEach(it => verified(it, tag));
    ok(new Set(B.groupNum).size === N && B.groupNum.every(n => n >= 1 && n <= N), tag + ': every problem colors exactly one group');
    B.code.forEach(k => { const i = k.num - 1; ok(B.items[i].key === k.answer && B.colorOf[i] === k.color, tag + ': color code lists the right answer for each color'); });
    ok(new Set(B.code.map(k => k.color)).size === N, tag + ': ten different colors');
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
  who(B, tag) {
    const S = B.S, C = B.culprit;
    ok(B.cards.length === 10, tag + ': ten clue cards');
    const sus = new Set(), pl = new Set(), me = new Set(), truthT = new Set(), falseT = new Set();
    B.cards.forEach((c, i) => {
      verified(c.item, tag);
      ok(c.opts.length === 4 && c.opts.filter(o => o.ok).length === 1 && c.opts[c.pos].ok, tag + ': four choices, one correct');
      ok(new Set(c.opts.map(o => String(o.a).replace(/\s+/g, ''))).size === 4, tag + ': four different choices');
      c.opts.forEach(o => { if (!o.ok) ok(!accepts(c.item.p, o.a), tag + ': wrong choice is wrong (' + o.a + ')'); });
      const t = c.truth; truthT.add(t.text);
      if (t.p !== undefined) { sus.add(t.p); pl.add(t.l); ok(t.text.startsWith(S.suspects[t.p].n + ' was ') && t.text.includes(S.places[t.l].n), tag + ': alibi names its suspect and place'); }
      else { me.add(t.m); ok(S.methods[t.m].clear.includes(t.text), tag + ': method clue is that method’s'); }
      c.opts.forEach(o => { if (o.ok) return;
        ok(!falseT.has(o.clue), tag + ': no false clue printed twice'); falseT.add(o.clue);
        const cn = S.suspects[C.p].n, cl = S.places[C.l].n, cm = S.methods[C.m].clear;
        if (o.clears === 'p') ok(o.clue.startsWith(cn + ' was '), tag + ': false alibi clears the culprit');
        else if (o.clears === 'l') ok(o.clue.includes(' ' + cl + ' the whole time'), tag + ': false clue clears the crime scene');
        else if (o.clears === 'm') ok(cm.includes(o.clue), tag + ': false clue clears the real method');
        else ok(o.clears === 'x' && !o.clue.includes(cn) && !o.clue.includes(' ' + cl + ' the whole time') && !cm.includes(o.clue), tag + ': noise clue clears only innocent things');
      });
    });
    ok(sus.size === 5 && !sus.has(C.p) && pl.size === 5 && !pl.has(C.l) && me.size === 5 && !me.has(C.m), tag + ': true clues leave exactly the culprit, the place and the method');
    falseT.forEach(t => ok(!truthT.has(t), tag + ': a false clue is never a true clue'));
  },
  stations(B, tag, cfg) {
    const all = PR.skillsFor(cfg), seen = [];
    ok(B.stations.length === Math.min(cfg.stations, all.length) || (B.levelNote && B.stations.length < cfg.stations), tag + ': the chosen number of stations (or fewer, with a note)');
    B.stations.forEach(st => {
      ok(st.items.length >= 4 && st.items.length <= cfg.perStation, tag + ': 4 to ' + cfg.perStation + ' problems');
      st.items.forEach(it => { verified(it, tag); ok(st.skills.includes(it.skill), tag + ': problem from this station’s skills'); });
      st.items.forEach((a, i) => st.items.forEach((b, j) => { if (i < j) ok(a.p.prompt !== b.p.prompt, tag + ': different problems'); }));
      seen.push(...st.skills);
    });
    ok(seen.length === all.length && new Set(seen).size === all.length, tag + ': every chosen skill is in exactly one station');
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

for (const unit of Object.keys(M.skillSets)) for (const kind of PR.KINDS.map(k => k.id).filter(k => k !== 'vocabulary' && k !== 'match')) for (const level of ['cp2', 'cp1', 'honors']) for (let s = 0; s < SEEDS; s++) {
  const cfg = PR.defaultConfig(unit, kind); cfg.level = level; cfg.seed = 500 + s;
  const B = PR.build(cfg, s % 2), tag = unit + ' ' + kind + ' ' + level;
  if ((UNSUPPORTED[unit] || []).includes(kind)) { ok(!!B.error, tag + ': listed as unsupported (remove it from UNSUPPORTED if it works now)'); continue; }
  ok(!B.error, tag + ': built (' + (B.error || '') + ')');
  CHECK[kind](B, tag, cfg); builds++;
}
// versions differ
{ const cfg = PR.defaultConfig('algebra1-quadratics', 'maze'); cfg.seed = 9; const A = PR.build(cfg, 0), B = PR.build(cfg, 1);
  ok(A.rooms[0].item.p.prompt !== B.rooms[0].item.p.prompt, 'Version B has different problems'); }
console.log('PASS: ' + builds + ' printables built, ' + checks + ' checks');
