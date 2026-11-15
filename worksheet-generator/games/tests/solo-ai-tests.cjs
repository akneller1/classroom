/* Checks the solo-mode computer opponent (games/solo-ai.js) without a browser.
   1. Every move is legal, and with no slips the computer takes a win and blocks a threat.
   2. Simulated games against a "student" who answers 70% of problems correctly and plays sensibly:
      the computer must be beatable on every level, and each level must be harder than the one before.
   Run: node worksheet-generator/games/tests/solo-ai-tests.cjs */
'use strict';
const assert = require('assert');
const path = require('path');
require(path.join(__dirname, '..', 'solo-ai.js'));
const A = globalThis.MKSOLOAI;
let passed = 0;
function ok(m) { passed++; console.log('  ✓ ' + m); }

/* ---- 1. legality and basic sense (with slips switched off) ---- */
A._setRandom(() => 0.999);   // chance(p) is false for every p < 0.999: no random moves, no missed wins or blocks
assert.strictEqual(A.ticTacToeMove(['R', 'R', null, 'L', 'L', null, null, null, null], 'R', 'L', 'easy'), 2, 'takes a win');
assert.strictEqual(A.ticTacToeMove(['L', 'L', null, null, 'R', null, null, null, null], 'R', 'L', 'easy'), 2, 'blocks');
assert.strictEqual(A.ticTacToeMove(['L', 'R', 'L', 'R', 'L', 'R', 'R', 'L', null], 'R', 'L', 'hard'), 8, 'last open square');
const empty = () => Array.from({ length: 6 }, () => Array(7).fill(null));
let g = empty(); g[5][0] = g[5][1] = g[5][2] = 'R'; g[4][0] = g[4][1] = 'L';
assert.strictEqual(A.connectFourMove(g, 'R', 'L', 'easy'), 3, 'connect four: takes a win');
g = empty(); g[5][1] = g[5][2] = g[5][3] = 'L'; g[4][2] = 'R';
assert.ok([0, 4].includes(A.connectFourMove(g, 'R', 'L', 'easy')), 'connect four: blocks an open three');
g = empty(); for (let c = 0; c < 6; c++) for (let r = 0; r < 6; r++) g[r][c] = (r + Math.floor(c / 2)) % 2 ? 0 : 1;
assert.strictEqual(A.connectFourMove(g, 1, 0, 'hard'), 6, 'connect four: numeric team ids (0 and 1) and the only open column');
ok('legal moves; takes wins and blocks when it does not slip; works with team ids 0/1 as well as L/R');

A._setRandom(Math.random);
for (let k = 0; k < 300; k++) {
  const level = ['easy', 'medium', 'hard'][k % 3];
  const b = Array(9).fill(null).map(() => (Math.random() < 0.3 ? (Math.random() < 0.5 ? 'L' : 'R') : null));
  if (b.every(Boolean)) continue;
  const m = A.ticTacToeMove(b, 'R', 'L', level); assert.ok(m >= 0 && m < 9 && !b[m], 'tic-tac-toe move is an open square');
  const c = empty(); for (let col = 0; col < 7; col++) { const h = Math.floor(Math.random() * 7); for (let i = 0; i < h && i < 6; i++) c[5 - i][col] = Math.random() < 0.5 ? 'L' : 'R'; }
  if (c[0].every(Boolean)) continue;
  const col = A.connectFourMove(c, 'R', 'L', level); assert.ok(col >= 0 && col < 7 && !c[0][col], 'connect four move is an open column');
}
ok('300 random positions per game: the computer always picks an open square or column');

/* ---- 2. simulated games ---- */
const r = Math.random, ACC = 0.7, SEES = 0.8;
function tttStudent(b) {
  const f = [...Array(9).keys()].filter(i => !b[i]);
  for (const m of ['L', 'R']) for (const i of f) { const c = b.slice(); c[i] = m; if (A.ticTacToeWinner(c) === m && r() < SEES) return i; }
  if (!b[4] && r() < 0.6) return 4;
  return f[Math.floor(r() * f.length)];
}
function drop(g, c, p) { for (let i = 5; i >= 0; i--) if (!g[i][c]) { g[i][c] = p; return; } }
function c4Student(g) {
  const v = [0, 1, 2, 3, 4, 5, 6].filter(c => !g[0][c]);
  for (const p of ['L', 'R']) for (const c of v) { const k = g.map(x => x.slice()); drop(k, c, p); if (A.connectFourWins(k, p) && r() < SEES) return c; }
  const safe = v.filter(c => { const k = g.map(x => x.slice()); drop(k, c, 'L'); return !v.some(c2 => { const k2 = k.map(x => x.slice()); if (k2[0][c2]) return false; drop(k2, c2, 'R'); return A.connectFourWins(k2, 'R'); }) || r() > SEES; });
  const pool = safe.length ? safe : v; pool.sort((a, b) => Math.abs(a - 3) - Math.abs(b - 3) + (r() - 0.5) * 4); return pool[0];
}
function rate(game, level, n) {
  let won = 0;
  for (let i = 0; i < n; i++) {
    let t = i % 2 ? 'R' : 'L', turns = 0;
    if (game === 'ttt') {
      const b = Array(9).fill(null);
      for (;;) {
        const w = A.ticTacToeWinner(b); if (w) { if (w === 'L') won++; break; }
        if (b.every(Boolean) || turns > 80) break;
        if (t === 'L') { const s = tttStudent(b); if (r() < ACC) b[s] = 'L'; } else { const s = A.ticTacToeMove(b, 'R', 'L', level); if (A.answers(level)) b[s] = 'R'; }
        t = t === 'L' ? 'R' : 'L'; turns++;
      }
    } else {
      const g = empty();
      for (;;) {
        if (A.connectFourWins(g, 'L')) { won++; break; }
        if (A.connectFourWins(g, 'R') || g[0].every(Boolean) || turns > 250) break;
        if (t === 'L') { const c = c4Student(g); if (r() < ACC) drop(g, c, 'L'); } else { const c = A.connectFourMove(g, 'R', 'L', level); if (A.answers(level)) drop(g, c, 'R'); }
        t = t === 'L' ? 'R' : 'L'; turns++;
      }
    }
  }
  return won / n;
}
for (const game of ['ttt', 'c4']) {
  const n = game === 'ttt' ? 600 : 300;
  const w = { easy: rate(game, 'easy', n), medium: rate(game, 'medium', n), hard: rate(game, 'hard', n) };
  const name = game === 'ttt' ? 'tic-tac-toe' : 'connect four';
  assert.ok(w.hard >= 0.08, name + ': hard is still beatable (' + w.hard + ')');
  assert.ok(w.easy >= 0.45, name + ': easy is usually beatable (' + w.easy + ')');
  assert.ok(w.easy > w.medium && w.medium > w.hard, name + ': each level is harder than the last ' + JSON.stringify(w));
  assert.ok(w.medium >= 0.25 && w.medium <= 0.65, name + ': medium is a fair fight (' + w.medium + ')');
  ok(name + ' student win rates (70% accuracy): easy ' + Math.round(w.easy * 100) + '%, medium ' + Math.round(w.medium * 100) + '%, hard ' + Math.round(w.hard * 100) + '%');
}
console.log(passed + ' solo AI checks passed');
