/* Shared building blocks for menu skill files (TeX builders, steps, number-line specs).
   Generator-side only: nothing here is used by the verifier. */
(function (G) {
  'use strict';
  var WS = G.MKWS, NS = (G.MKMENU = G.MKMENU || {});
  var T = WS.tex, Fr = WS.frac.Fr, num = T.num, lin = T.lin;
  var K = NS.kit = {};
  K.M = T.M; K.num = num; K.lin = lin; K.Fr = Fr; K.gcd = WS.frac.gcd;
  K.need = function (c, why) { if (!c) throw new WS.gen.Reject(why || 'constraint'); };
  K.F = function (n, d) { return new Fr(n, d === undefined ? 1 : d); };
  K.nz = function (r, lo, hi) { return r.nonzero(lo, hi); };
  K.cp = function (a) { a = Fr.of(a); return a.eq(1) ? '' : a.eq(-1) ? '-' : num(a); };
  K.grp = function (a, inner) { return K.cp(a) + '(' + inner + ')'; };
  K.signed = function (first, a, body) { a = Fr.of(a); return first ? K.grp(a, body) : (a.sign() < 0 ? '-' : '+') + K.grp(a.abs(), body); };
  K.addConst = function (s, k) { k = Fr.of(k); return k.isZero() ? s : s + (k.sign() < 0 ? '-' : '+') + num(k.abs()); };
  K.addX = function (s, k, v) { k = Fr.of(k); if (k.isZero()) return s; return s + (k.sign() < 0 ? '-' : '+') + (k.abs().eq(1) ? '' : num(k.abs())) + (v || 'x'); };
  K.xb = function (b, v) { return lin([[1, v || 'x'], [b, '']]); };
  K.axb = function (a, b, v) { return lin([[a, v || 'x'], [b, '']]); };
  K.dec = function (n10) { var s = (Math.abs(n10) / 10).toFixed(1); return (n10 < 0 ? '-' : '') + s.replace(/\.0$/, ''); };
  K.step = function (t, m, w) { return { t: t || '', m: m || '', w: w === undefined ? 1 : w }; };

  /* ---------- inequalities ---------- */
  var TEX = { '<': '<', '>': '>', '<=': '\\le ', '>=': '\\ge ' };
  K.OPS = ['<', '>', '<=', '>='];
  K.opTeX = function (op) { return TEX[op]; };
  K.flip = function (op) { return { '<': '>', '>': '<', '<=': '>=', '>=': '<=' }[op]; };
  K.rel = function (l, op, r) { return l + TEX[op] + r; };
  K.ans = function (v, op, k) { return v + TEX[op] + num(k); };
  /* Solve A·x + B (op) C·x + D, writing the steps. Returns {op, k}. */
  K.solveIneq = function (steps, A, B, C, D, op, v) {
    v = v || 'x'; A = Fr.of(A); B = Fr.of(B); C = Fr.of(C); D = Fr.of(D);
    if (!C.isZero()) { A = A.sub(C); steps.push(K.step('Collect the ' + v + '-terms on one side.', K.rel(K.axb(A, B, v), op, num(D)), 1)); }
    if (!B.isZero()) { D = D.sub(B); steps.push(K.step('Undo the constant on both sides.', K.rel(lin([[A, v]]), op, num(D)), 1)); }
    K.need(!A.isZero());
    var k = D.div(A), out = op;
    if (A.sign() < 0) { out = K.flip(op); steps.push(K.step('Divide both sides by ' + T.M(num(A)) + ' and reverse the inequality sign.', K.ans(v, out, k), 2)); }
    else if (!A.eq(1)) steps.push(K.step(A.isInt() ? 'Divide both sides by ' + num(A) + '.' : 'Multiply both sides by ' + T.M(num(A.inv())) + '.', K.ans(v, out, k), 1));
    return { op: out, k: k };
  };
  K.toPair = function (q) { if (q === null) return null; q = Fr.of(q); return [q.n, q.d]; };
  /* Number-line pieces for a ray "v op k". */
  K.rayPieces = function (op, k) {
    var p = K.toPair(k);
    if (op === '<' || op === '<=') return [{ lo: null, loC: false, hi: p, hiC: op === '<=' }];
    return [{ lo: p, loC: op === '>=', hi: null, hiC: false }];
  };
  K.window = function (r, ends, jitter) {
    var vs = ends.map(function (q) { q = Fr.of(q); return q.n / q.d; });
    var lo = Math.floor(Math.min.apply(null, vs)) - (jitter ? r.int(2, 5) : 3), hi = Math.ceil(Math.max.apply(null, vs)) + (jitter ? r.int(2, 5) : 3);
    while (hi - lo < 10) { if (r.chance(0.5)) lo--; else hi++; }
    if (hi - lo > 20) { if (lo % 2) lo--; if (hi % 2) hi++; }
    return { min: lo, max: hi };
  };
  K.line = function (win, pieces) { return { kind: 'numberline', min: win.min, max: win.max, pieces: pieces || [] }; };
})(typeof window !== 'undefined' ? window : globalThis);
