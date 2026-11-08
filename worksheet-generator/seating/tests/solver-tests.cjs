/* Checks the auto-seat solver and the roster parser.  Run: node seating/tests/solver-tests.cjs [rounds] */
'use strict';
const S = require('../seating-core.js');
const rounds = +(process.argv[2] || 20);
let pass = 0, fail = 0;
function ok(c, msg) { if (c) pass++; else { fail++; console.log('FAIL', msg); } }

function chart(preset, nStudents) {
  const st = {name:'T', roomW:1024, roomH:768, view:'top', items:S.presetItems(preset, {w:1024, h:768}),
    students:[], seats:{}, rules:[], tags:[], history:[]};
  for (let i = 0; i < nStudents; i++) st.students.push({id:'s' + i, name:'First' + i + ' Last' + i, needs:[], tags:[], note:'', pin:false});
  return st;
}
function apply(st, o) { st.seats = S.solve(st, o).seats; return S.check(st); }

// 1. everyone gets a seat, nobody twice, only real seats
for (const p of ['rows', 'pairs', 'group4', 'group6', 'round', 'ushape', 'exam']) {
  const st = chart(p, 24); apply(st, {mode:'all', spread:'any'});
  const keys = new Set(S.seatList(st).map(s => s.key)), vals = Object.values(st.seats);
  ok(vals.length === 24 && new Set(vals).size === 24, p + ' seats everyone once');
  ok(Object.keys(st.seats).every(k => keys.has(k)), p + ' uses real seats');
}
// 2. "any seat" uses back seats too; "front first" uses the front rows only
{
  let backUsed = 0;
  for (let r = 0; r < rounds; r++) {
    const st = chart('rows', 12); apply(st, {mode:'all', spread:'any'});
    const sl = S.seatList(st); if (sl.some(s => st.seats[s.key] && s.y > 500)) backUsed++;
  }
  ok(backUsed > rounds * 0.8, 'random seats reach the back of the room (' + backUsed + '/' + rounds + ')');
  const st = chart('rows', 12); apply(st, {mode:'all', spread:'front'});
  const ys = S.seatList(st).filter(s => st.seats[s.key]).map(s => s.y);
  ok(Math.max(...ys) < 360, 'front first fills the first two rows');
}
// 3. keep apart / work well together / needs / pins
for (let r = 0; r < rounds; r++) {
  const st = chart(r % 2 ? 'group4' : 'pairs', 28);
  st.rules = [{id:'r1', a:'s0', b:'s1', type:'apart'}, {id:'r2', a:'s0', b:'s2', type:'apart'}, {id:'r3', a:'s1', b:'s2', type:'apart'},
              {id:'r4', a:'s3', b:'s4', type:'together'}, {id:'r5', a:'s5', b:'s6', type:'together'}];
  st.students[7].needs = ['front']; st.students[8].needs = ['door']; st.students[9].needs = ['nowindow'];
  st.students[10].needs = ['teacher'];
  const rep = apply(st, {mode:'all', spread:'any', rules:true, needs:true});
  ok(rep.problems.length === 0, 'rules and needs met: ' + rep.problems.map(p => p.text).join(' | '));
  // pin: student 11 stays
  const k = S.seatOf(st, 's11'); st.students[11].pin = true;
  apply(st, {mode:'all', spread:'any'});
  ok(S.seatOf(st, 's11') === k, 'pinned student stays');
}
// 4. fill empty keeps seated students
{
  const st = chart('rows', 10); apply(st, {mode:'all'});
  const before = JSON.stringify(st.seats);
  for (let i = 10; i < 16; i++) st.students.push({id:'s' + i, name:'N' + i, needs:[], tags:[]});
  apply(st, {mode:'empty', spread:'any'});
  const b = JSON.parse(before); ok(Object.keys(b).every(k => st.seats[k] === b[k]), 'fill empty keeps seats');
  ok(Object.keys(st.seats).length === 16, 'fill empty seats the new students');
}
// 5. new neighbors: repeats drop
{
  let rep = 0, tot = 0;
  for (let r = 0; r < rounds; r++) {
    const st = chart('group4', 24); apply(st, {mode:'all'});
    st.history = [{id:'h', date:'x', seats:st.seats, pairs:S.neighborPairs(st)}];
    const old = new Set(st.history[0].pairs.filter(p => p[2] === 2).map(p => [p[0], p[1]].sort().join('|')));
    apply(st, {mode:'all', fresh:true});
    S.neighborPairs(st).filter(p => p[2] === 2).forEach(p => { tot++; if (old.has([p[0], p[1]].sort().join('|'))) rep++; });
  }
  ok(rep / tot < 0.05, 'new neighbors: ' + rep + ' of ' + tot + ' tablemates repeat');
}
// 6. balanced tags and even spread
{
  let worst = 0;
  for (let r = 0; r < rounds; r++) {
    const st = chart('group4', 24); st.tags = [{id:'t1', name:'ELL', color:'#000'}];
    for (let i = 0; i < 8; i++) st.students[i].tags = ['t1'];
    apply(st, {mode:'all', balance:true});
    const per = {}; S.seatList(st).forEach(s => { const sid = st.seats[s.key]; if (sid && +sid.slice(1) < 8) per[s.item.id] = (per[s.item.id] || 0) + 1; });
    worst = Math.max(worst, ...Object.values(per));
  }
  ok(worst <= 1, 'balanced: at most 1 tagged student per group of 4 (worst ' + worst + ')');
  const st = chart('group6', 18); apply(st, {mode:'all', spread:'even'});
  const occ = {}; S.seatList(st).forEach(s => { if (st.seats[s.key]) occ[s.item.id] = (occ[s.item.id] || 0) + 1; });
  ok(Object.values(occ).every(v => v === 3) && Object.keys(occ).length === 6, 'even spread: 3 per group of 6');
}
// 7. more students than seats
{ const st = chart('round', 40); apply(st, {mode:'all'}); ok(Object.keys(st.seats).length === 36, '36 seated, 4 waiting'); }
// 8. roster parsing
const eq = (a, b, m) => ok(JSON.stringify(a) === JSON.stringify(b), m + ' → ' + JSON.stringify(a));
eq(S.parseNames('Smith, Maya\nLeo Chen\n3. Ava Ruiz'), ['Maya Smith', 'Leo Chen', 'Ava Ruiz'], 'textarea lines');
eq(S.parseNames('Maya, Leo, Ava'), ['Maya', 'Leo', 'Ava'], 'one comma line');
eq(S.parseRoster('Last Name,First Name,Email Address\nSmith,Maya,m@x.org\n"O\'Brien",Liam,l@x.org\n'), ['Maya Smith', "Liam O'Brien"], 'Google Classroom export');
eq(S.parseRoster('Student ID,Student Name,Grade\n1001,"Smith, Maya",9\n1002,"Chen, Leo",9'), ['Maya Smith', 'Leo Chen'], 'SIS export');
eq(S.parseRoster('Smith,Maya\nChen,Leo'), ['Maya Smith', 'Leo Chen'], 'headerless last,first');
eq(S.parseRoster('Maya Smith\nLeo Chen\n'), ['Maya Smith', 'Leo Chen'], 'plain list');
eq(S.parseRoster('First\tLast\nMaya\tSmith'), ['Maya Smith'], 'tab separated');
// 9. PDF structure
{ const pdf = S.pdf([{bytes:new Uint8Array([1,2,3]), w:10, h:10}, {bytes:new Uint8Array([4]), w:10, h:20}], S.PAPER.a4);
  const t = Buffer.from(pdf).toString('latin1'); ok(/\/Count 2/.test(t) && /startxref\n\d+\n%%EOF/.test(t), 'two-page pdf'); }

console.log(pass + ' passed, ' + fail + ' failed');
process.exit(fail ? 1 : 0);
