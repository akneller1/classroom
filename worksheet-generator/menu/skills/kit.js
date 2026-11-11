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
  /* Try a generator again (same rng stream) when one of its constraints rejects; for pages that call generate() directly. */
  K.retry = function (f) { for (var i = 0; ; i++) { try { return f(); } catch (e) { if (!e || !e.isReject || i >= 200) throw e; } } };
  K.step = function (t, m, w) { return { t: t || '', m: m || '', w: w === undefined ? 1 : w }; };


  /* Geometry Units 3 and 8: congruent or similar after a described sequence of transformations, and glide reflections
     of a point. Checked by the verifier's "sequence" and "glide" readers, which re-read the printed sentence. */
  K.rigidSequence = function (ctx) {
    var r = ctx.rng, c = ctx.c, step = K.step, M = K.M;
    var rigid = [function () { return 'translated ' + r.int(2, 9) + ' units ' + r.pick(['left', 'right', 'up', 'down']); }, function () { return 'reflected across the ' + r.pick(['x-axis', 'y-axis', 'line y = x']); },
      function () { return 'rotated ' + r.pick([90, 180, 270]) + '° ' + r.pick(['clockwise', 'counterclockwise']) + ' about the origin'; }];
    if (c >= 5 && r.chance(0.3)) {   // glide reflection of a point
      var x = K.nz(r, -9, 9), y = K.nz(r, -9, 9), d = r.int(2, 8), ax = r.pick(['x', 'y']), dir = ax === 'x' ? r.pick(['right', 'left']) : r.pick(['up', 'down']);
      var X = x + (dir === 'right' ? d : dir === 'left' ? -d : 0), Y = y + (dir === 'up' ? d : dir === 'down' ? -d : 0); if (ax === 'x') Y = -Y; else X = -X;
      return { variant: 'geo-glide-' + ax + '-' + c, prompt: 'The point (' + x + ', ' + y + ') is translated ' + d + ' units ' + dir + ' and then reflected across the ' + ax + '-axis. Because the translation is parallel to the mirror line, this is a glide reflection. What are the coordinates of the image?',
        parts: [{ answer: '(' + X + ', ' + Y + ')', check: { type: 'derive', kind: 'glide', alts: ['(' + (ax === 'x' ? X : -X) + ', ' + (ax === 'x' ? -Y : Y) + ')', '(' + (ax === 'x' ? x : -x) + ', ' + (ax === 'x' ? -y : y) + ')', '(' + Y + ', ' + X + ')', '(' + (-X) + ', ' + (-Y) + ')'].filter(function (a, i, arr) { return a !== '(' + X + ', ' + Y + ')' && arr.indexOf(a) === i; }) } }],
        steps: [step('Translate first: (' + x + ', ' + y + ') → (' + (x + (dir === 'right' ? d : dir === 'left' ? -d : 0)) + ', ' + (y + (dir === 'up' ? d : dir === 'down' ? -d : 0)) + ').', ''), step('Then reflect across the ' + ax + '-axis (' + (ax === 'x' ? 'change the sign of y' : 'change the sign of x') + '): (' + X + ', ' + Y + ').', '')], space: [0.8, 1.0, 1.2] };
    }
    var n = c <= 2 ? r.int(1, 2) : r.int(2, 3), parts = [], scale = 1, dil = c <= 1 ? r.chance(0.5) : r.chance(0.6), dWords = null;
    for (var i = 0; i < n; i++) parts.push(r.pick(rigid)());
    if (dil) {
      if (c >= 6 && r.chance(0.35)) { var k = r.pick([2, 3]); parts.splice(r.int(0, parts.length), 0, 'dilated by a scale factor of ' + k + ' centered at the origin'); parts.push('dilated by a scale factor of ' + (k === 2 ? 'one-half' : 'one-third') + ' centered at the origin'); scale = 1; dWords = 'The two dilations undo each other (' + k + ' × 1/' + k + ' = 1).'; }
      else if (c >= 5 && r.chance(0.5)) { var w = r.pick(['one-half', 'one-third']); scale = w === 'one-half' ? 0.5 : 1 / 3; parts.splice(r.int(0, parts.length), 0, 'dilated by a scale factor of ' + w + ' centered at the origin'); }
      else { var k2 = r.int(2, 4); scale = k2; parts.splice(r.int(0, parts.length), 0, 'dilated by a scale factor of ' + k2 + ' centered at the origin'); }
    }
    var seq = parts.join(', then '), cong = Math.abs(scale - 1) < 1e-9, askLen = c >= 3 && r.chance(0.4);
    var why = cong ? (dWords || 'Translations, reflections and rotations are rigid motions: they keep every length and angle.') : 'A dilation with scale factor ' + (scale === 0.5 ? '½' : scale < 0.5 ? '⅓' : scale) + ' changes the lengths but keeps the angles, so the figures are similar.';
    if (askLen) {
      var L0 = scale === 0.5 ? 2 * r.int(2, 9) : scale < 0.5 ? 3 * r.int(2, 6) : r.int(3, 12), L1 = Math.round(L0 * scale * 1000) / 1000;
      return { variant: 'geo-sequence-len-' + c, prompt: 'Figure P is ' + seq + '. The result is figure Q. A side of figure P is ' + L0 + ' units long. How long is the matching side of figure Q?',
        parts: [{ answer: M(String(L1)) + ' units', check: { type: 'derive', kind: 'sequence', alts: [String(L0 === L1 ? L0 * 2 : L0), String(L0 + 2), String(L1 * 2 === L0 ? L0 * 4 : L1 * 2)].filter(function (z) { return +z !== L1; }) } }],
        steps: [step(why, ''), step('Matching side: ' + L0 + ' × ' + (cong ? 1 : scale === 0.5 ? '½' : scale < 0.5 ? '⅓' : scale) + ' = ' + L1 + ' units.', '')], space: [0.9, 1.1, 1.3] };
    }
    return { variant: 'geo-sequence-class-' + (cong ? 'c' : 's') + '-' + c, prompt: 'Figure P is ' + seq + '. The result is figure Q. Is figure Q congruent to figure P, similar but not congruent, or neither?',
      parts: [{ answer: cong ? 'Congruent' : 'Similar but not congruent', check: { type: 'derive', kind: 'sequence' } }], steps: [step(why, ''), step('Answer: ' + (cong ? 'congruent' : 'similar but not congruent') + '.', '')], space: [0.7, 0.8, 0.9] };
  };

  /* absolute value equations: shared by Units 2 and 3 (checked as solution sets by the inequality checker) */
  function ansX(v, x) { return v + '=' + K.num(x); }
  function orList(v, xs) { return xs.map(function (x) { return K.M(ansX(v, x)); }).join(' or '); }
  K.absEqSkill = NS.absEqSkill = function (tag) {
    return {
      id: 'abs-eq', best: [1, 2], tag: tag, name: 'Solve absolute value equations',
      blurb: '|x| = a and |x + b| = a (CP2) → |ax + b| = c, isolating the absolute value first (CP1) → no-solution and one-solution cases, fractions, two absolute values (Honors).',
      generate: function (ctx) {
        var r = ctx.rng, c = ctx.c, steps = [], e, inner, k = 1, s = 0, sols, a = 1, b = 0, R;
        var frac = !ctx.intOnly && c >= 6 && r.chance(0.5);
        if (c === 7 && r.chance(0.4)) {     // |ax + b| = |cx + d|: two cases
          var x1 = r.int(-9, 9), x2 = r.int(-9, 9); K.need(x1 !== x2);
          var a1 = r.int(1, 4), c1 = r.int(1, 4); K.need(a1 !== c1);
          // a1·x + b1 = c1·x + d1 at x1 and a1·x + b1 = −(c1·x + d1) at x2
          // b1 − d1 = (c1 − a1)·x1 and b1 + d1 = −(a1 + c1)·x2
          var S1 = (c1 - a1) * x1, S2 = -(a1 + c1) * x2; K.need((S1 + S2) % 2 === 0);
          var b1 = (S1 + S2) / 2, d1 = (S2 - S1) / 2; K.need(b1 !== 0 && d1 !== 0);
          var L = K.axb(a1, b1), Rr = K.axb(c1, d1);
          e = '|' + L + '|=|' + Rr + '|';
          steps.push(K.step('Two absolute values are equal when the insides are equal or opposite.', L + '=' + Rr + '\\text{ or }' + L + '=-(' + Rr + ')', 2));
          steps.push(K.step('Solve each equation.', '', 1));
          sols = [Math.min(x1, x2), Math.max(x1, x2)];
          return { variant: 'abs-two', prompt: 'Solve ' + K.M(e) + '.', parts: [{ answer: orList('x', sols), check: { type: 'ineq', ineq: e, v: 'x', allowSpecial: true } }],
            steps: steps.concat([K.step('Solutions:', 'x=' + sols[0] + '\\text{ or }x=' + sols[1], 1)]), space: [1.3, 1.6, 1.9] };
        }
        if (c === 1) { R = r.int(2, 40); inner = 'x'; }
        else if (c === 2) { b = K.nz(r, -9, 9); R = r.int(2, 12); inner = K.xb(b); }
        else { a = r.int(2, 5) * (c >= 6 && r.chance(0.3) ? -1 : 1); b = K.nz(r, -12, 12); R = r.int(1, 12) * Math.abs(a); inner = K.axb(a, b); }
        if (c >= 4) { k = r.int(2, 5) * (c === 7 && r.chance(0.4) ? -1 : 1); s = K.nz(r, -15, 15); }
        if (frac) { R = r.int(1, 15); K.need((R - b) % a !== 0 || (-R - b) % a !== 0); }
        var special = c >= 5 && r.chance(0.3) ? r.pick(['none', 'one']) : null;
        if (special === 'none') R = -r.int(1, 8);
        if (special === 'one') R = 0;
        var lhs = k === 1 ? '|' + inner + '|' : K.cp(k) + '|' + inner + '|';
        e = K.addConst(lhs, s) + '=' + K.num(k * R + s);
        if (k !== 1 || s) steps.push(K.step('Isolate the absolute value.', '|' + inner + '|=' + K.num(R), 2));
        if (R < 0) {
          steps.push(K.step('An absolute value is never negative, so there is no solution.', '', 2));
          return { variant: 'abs-none', prompt: 'Solve ' + K.M(e) + '. If there is no solution, say so.', parts: [{ answer: 'No solution', check: { type: 'ineq', ineq: e, v: 'x', allowSpecial: true } }], steps: steps, space: [0.9, 1.1, 1.3] };
        }
        if (R === 0) {
          var z = K.F(-b, a); K.need(z.isInt() || (!ctx.intOnly && c >= 6));
          steps.push(K.step('Only 0 has absolute value 0, so the inside must be 0.', inner + '=0', 2));
          steps.push(K.step('Solve.', ansX('x', z), 1));
          return { variant: 'abs-one', prompt: 'Solve ' + K.M(e) + '.', parts: [{ answer: K.M(ansX('x', z)), check: { type: 'ineq', ineq: e, v: 'x', allowSpecial: true } }], steps: steps, space: [0.9, 1.1, 1.3] };
        }
        var p1 = K.F(R - b, a), p2 = K.F(-R - b, a);
        if (!frac) K.need(p1.isInt() && p2.isInt());
        steps.push(K.step('The inside is ' + K.M(K.num(R)) + ' or ' + K.M(K.num(-R)) + '.', inner + '=' + K.num(R) + '\\text{ or }' + inner + '=' + K.num(-R), 2));
        var lo = p1.sub(p2).sign() < 0 ? p1 : p2, hi = lo === p1 ? p2 : p1;
        if (a !== 1 || b) steps.push(K.step('Solve each equation.', ansX('x', lo) + '\\text{ or }' + ansX('x', hi), 1));
        return { variant: 'abs' + (a !== 1 ? 'a' : '') + (k !== 1 ? 'k' : '') + c, prompt: 'Solve ' + K.M(e) + (c >= 5 ? '. If there is no solution, say so.' : '.'),
          parts: [{ answer: orList('x', [lo, hi]), check: { type: 'ineq', ineq: e, v: 'x', allowSpecial: true } }], steps: steps, space: [0.9 + 0.08 * c, 1.1 + 0.1 * c, 1.3 + 0.12 * c] };
      }
    };
  };

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
