/* Menu Assessment Generator — Algebra 1 · Inequalities skill library.
   Skill groups follow the static "Inequalities Bistro": SOLVE, COMPOUND, REASON, APPLY.
   Answer-first, difficulty c = 1…7 (see the Expressions & Equations file for the level map).
   Every answer and every number line is re-checked by menu/verify.js, which solves the printed
   inequality with its own critical-point method and reads the drawn number line back from the SVG. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, Fr = K.Fr, M = K.M, num = K.num, lin = K.lin;
  var need = K.need, F = K.F, nz = K.nz, step = K.step, grp = K.grp, xb = K.xb, axb = K.axb, rel = K.rel, gcd = K.gcd;

  function pickOp(r) { return r.pick(K.OPS); }
  function fracBound(ctx) { var d = ctx.rng.int(2, 5), n = nz(ctx.rng, -14, 14); need(gcd(Math.abs(n), d) === 1 && Math.abs(n) > 1); return F(n, d); }
  function wantsFraction(ctx) { return !ctx.intOnly && ctx.c >= 6 && ctx.rng.chance(0.45); }
  function setPieces(op, k) { return K.rayPieces(op, k); }
  /* Standard "solve and graph" problem from a printed inequality and its worked solution. */
  function solved(ctx, e, res, steps, variant, extra) {
    var win = K.window(ctx.rng, [res.k], true), v = 'x';
    steps.unshift(step('', e, 0));
    steps.push(step('Graph: ' + (res.op.length > 1 ? 'closed' : 'open') + ' circle at ' + M(num(res.k)) + ', shade ' + (res.op[0] === '<' ? 'left' : 'right') + '.', '', 1));
    return Object.assign({
      variant: variant, prompt: 'Solve ' + M(e) + ' and graph the solution.', fig: K.line(win),
      parts: [{ answer: M(K.ans(v, res.op, res.k)), check: { type: 'ineq', ineq: e, v: v }, answerFig: K.line(win, setPieces(res.op, res.k)) }],
      steps: steps, space: [0.9 + 0.1 * ctx.c, 1.1 + 0.13 * ctx.c, 1.35 + 0.15 * ctx.c]
    }, extra || {});
  }
  function partial(st) { st.partial = true; return st; }   // shows one piece of a compound answer
  var skills = [];
  function skill(d) { skills.push(d); return d; }

  /* ================= SOLVE · one- and two-step ================= */
  skill({
    id: 'ineq-solve', best: [0, 1], tag: 'SOLVE', name: 'Solve one- and two-step inequalities',
    blurb: 'One step with positives (CP2) → negative coefficients that reverse the sign (CP1) → fraction and decimal coefficients (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, op = pickOp(r), steps = [], e, res, a, b, k = c <= 2 ? r.int(-6, 10) : nz(r, -12, 12), variant;
      if (c === 1) {
        variant = r.pick(['add', 'sub', 'mul']);
        if (variant === 'add') { b = r.int(1, 15); e = rel(xb(b), op, String(k + b)); res = K.solveIneq(steps, 1, b, 0, k + b, op); }
        else if (variant === 'sub') { b = r.int(1, 15); e = rel(xb(-b), op, String(k - b)); res = K.solveIneq(steps, 1, -b, 0, k - b, op); }
        else { a = r.int(2, 9); e = rel(a + 'x', op, String(a * k)); res = K.solveIneq(steps, a, 0, 0, a * k, op); }
      } else if (c === 2) {
        a = r.int(2, 9); b = nz(r, -15, 15); e = rel(axb(a, b), op, String(a * k + b)); variant = 'axb'; res = K.solveIneq(steps, a, b, 0, a * k + b, op);
      } else if (c === 3) {
        if (r.chance(0.5)) { a = -r.int(2, 9); b = nz(r, -15, 15); e = rel(axb(a, b), op, String(a * k + b)); variant = 'neg'; res = K.solveIneq(steps, a, b, 0, a * k + b, op); }
        else { a = r.int(2, 6); var m = nz(r, -6, 6); k = a * m; b = nz(r, -12, 12); e = rel('\\frac{x}{' + a + '}' + K.addConst('', b), op, String(m + b)); variant = 'xdiv';
          steps.push(step('Undo the constant.', rel('\\frac{x}{' + a + '}', op, String(m)), 1)); steps.push(step('Multiply both sides by ' + a + '.', K.ans('x', op, k), 1)); res = { op: op, k: F(k) }; }
      } else if (c === 4) {
        if (r.chance(0.5)) { a = r.int(2, 9); b = nz(r, -20, 20); e = rel(lin([[b, ''], [-a, 'x']]), op, String(b - a * k)); variant = 'b-ax'; res = K.solveIneq(steps, -a, b, 0, b - a * k, op); }
        else { a = r.int(2, 6); var m4 = nz(r, -6, 6); k = -a * m4; e = rel('\\frac{x}{' + (-a) + '}', op, String(m4)); variant = 'x/-a';
          res = { op: K.flip(op), k: F(k) }; steps.push(step('Multiply both sides by ' + M(String(-a)) + ' and reverse the inequality sign.', K.ans('x', res.op, k), 2)); }
      } else if (c === 5) {
        var q = r.int(2, 5), p = nz(r, -4, 4); need(gcd(Math.abs(p), q) === 1 && Math.abs(p) !== q);
        a = F(p, q); k = q * nz(r, -6, 6); b = nz(r, -12, 12); var R = a.mul(k).add(b); need(R.isInt());
        e = rel(axb(a, b), op, num(R)); variant = 'fraccoef'; res = K.solveIneq(steps, a, b, 0, R, op);
      } else {
        if (r.chance(0.5)) {
          var A10 = nz(r, -9, 9), B10 = nz(r, -40, 40); need(Math.abs(A10) > 1);
          var X = wantsFraction(ctx) ? F(nz(r, -9, 9), 2) : F(nz(r, -12, 12)), R10 = Fr.of(A10).mul(X).add(B10); need(R10.isInt());
          e = rel(K.dec(A10) + 'x' + (B10 < 0 ? '-' : '+') + K.dec(Math.abs(B10)), op, K.dec(R10.n)); variant = 'decimal';
          steps.push(step('Multiply every term by 10.', rel(axb(A10, B10), op, num(R10)), 1)); res = K.solveIneq(steps, A10, B10, 0, R10, op);
        } else {
          var dd = r.int(2, 6), nn = nz(r, -7, 7); need(gcd(Math.abs(nn), dd) === 1 && Math.abs(nn) > 1);
          a = F(nn, dd); var Xf = wantsFraction(ctx) ? fracBound(ctx) : F(dd * nz(r, -4, 4)); b = nz(r, -15, 15);
          var Rf = a.mul(Xf).add(b); need(Rf.isInt()); e = rel(axb(a, b), op, num(Rf)); variant = 'fraccoef2'; res = K.solveIneq(steps, a, b, 0, Rf, op);
        }
      }
      return solved(ctx, e, res, steps, variant);
    }
  });

  /* ================= SOLVE · multi-step ================= */
  skill({
    id: 'ineq-multi', best: [1, 2], tag: 'SOLVE', name: 'Solve multi-step inequalities',
    blurb: 'a(x + b) < c (CP2) → variables on both sides, negative coefficients (CP1) → fraction bars, LCDs, several groups (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, op = pickOp(r), steps = [], e, res, k = nz(r, -10, 10), variant, A, B, C2, D;
      if (c === 1) { var a = r.int(2, 8), b = nz(r, -9, 9); D = a * (k + b); e = rel(grp(a, xb(b)), op, String(D)); variant = 'a(x+b)';
        steps.push(step('Distribute.', rel(axb(a, a * b), op, String(D)), 1)); res = K.solveIneq(steps, a, a * b, 0, D, op); }
      else if (c === 2) { var a2 = r.int(2, 7), b2 = nz(r, -9, 9), cx = nz(r, -6, 6); A = a2 + cx; need(A !== 0);
        D = a2 * (k + b2) + cx * k; e = rel(K.addX(grp(a2, xb(b2)), cx), op, String(D)); variant = 'combine';
        steps.push(step('Distribute.', rel(lin([[a2, 'x'], [a2 * b2, ''], [cx, 'x']]), op, String(D)), 1));
        steps.push(step('Combine like terms.', rel(axb(A, a2 * b2), op, String(D)), 1)); res = K.solveIneq(steps, A, a2 * b2, 0, D, op); }
      else if (c === 3) { var a3 = r.int(2, 7), b3 = nz(r, -9, 9); D = -a3 * (k - b3); e = rel(grp(-a3, xb(-b3)), op, String(D)); variant = '-a(x-b)';
        steps.push(step('Distribute.', rel(axb(-a3, a3 * b3), op, String(D)), 1)); res = K.solveIneq(steps, -a3, a3 * b3, 0, D, op); }
      else if (c === 4 && r.chance(0.5)) {
        // (x − a)/(−b) op m
        var b6 = r.int(2, 6), m6 = nz(r, -6, 6), a6 = nz(r, -9, 9); k = a6 - b6 * m6;
        e = rel('\\frac{' + xb(-a6) + '}{' + (-b6) + '}', op, String(m6)); variant = 'fracbar-neg';
        var op1 = K.flip(op); steps.push(step('Multiply both sides by ' + M(String(-b6)) + ' and reverse the sign.', rel(xb(-a6), op1, String(-b6 * m6)), 2));
        steps.push(step('Undo the constant.', K.ans('x', op1, k), 1)); res = { op: op1, k: F(k) };
      }
      else if (c === 4) { var a4 = nz(r, -6, 6), m4 = nz(r, -6, 6), c4 = nz(r, -9, 9); need(Math.abs(a4) > 1 && a4 !== c4); var d4 = a4 * (k + m4) - c4 * k; need(d4 !== 0);
        e = rel(grp(a4, xb(m4)), op, axb(c4, d4)); variant = 'both-dist';
        steps.push(step('Distribute.', rel(axb(a4, a4 * m4), op, axb(c4, d4)), 1)); res = K.solveIneq(steps, a4, a4 * m4, c4, d4, op); }
      else if (c === 5) {
        // d − e(x + f) op g·x + h
        var d5 = r.int(2, 12), e5 = r.int(2, 5), f5 = nz(r, -6, 6), g5 = nz(r, -5, 5); need(-e5 !== g5);
        A = -e5; B = d5 - e5 * f5; C2 = g5; var h5 = (A - C2) * k + B; need(h5 !== 0);
        e = rel(d5 + '-' + grp(e5, xb(f5)), op, axb(g5, h5)); variant = 'd-e(x+f)';
        steps.push(step('Distribute (the subtraction changes both signs).', rel(lin([[d5, ''], [-e5, 'x'], [-e5 * f5, '']]), op, axb(g5, h5)), 2));
        steps.push(step('Combine like terms.', rel(axb(A, B), op, axb(g5, h5)), 1)); res = K.solveIneq(steps, A, B, C2, h5, op);
      } else if (c === 6) {
        {
          // (ax + b)/p op (cx + d)/q
          var p6 = r.pick([2, 3, 4]), q6 = r.pick([3, 4, 5, 6]); need(p6 !== q6);
          var L = p6 * q6 / gcd(p6, q6), a7 = nz(r, -5, 5), c7 = nz(r, -5, 5), X6 = wantsFraction(ctx) ? fracBound(ctx) : F(k);
          A = F(a7 * L / p6); C2 = F(c7 * L / q6); need(!A.eq(C2));
          var b7 = nz(r, -9, 9); var lhs = Fr.of(a7).mul(X6).add(b7).div(p6); // choose d so that X6 is the boundary
          var d7 = lhs.mul(q6).sub(Fr.of(c7).mul(X6)); need(d7.isInt() && !d7.isZero());
          e = rel('\\frac{' + axb(a7, b7) + '}{' + p6 + '}', op, '\\frac{' + axb(c7, d7) + '}{' + q6 + '}'); variant = 'lcd';
          steps.push(step('Multiply both sides by the LCD, ' + L + ' (positive, so the sign stays).', rel(grp(L / p6, axb(a7, b7)), op, grp(L / q6, axb(c7, d7))), 2));
          steps.push(step('Distribute.', rel(axb(A, b7 * L / p6), op, axb(C2, d7.mul(L / q6))), 1));
          res = K.solveIneq(steps, A, b7 * L / p6, C2, d7.mul(L / q6), op); need(res.k.eq(X6));
        }
      } else {
        // a(bx − c) − d(x + e) op f(x − g) + h
        var a8 = r.int(2, 4), b8 = r.int(1, 3), c8 = nz(r, -6, 6), d8 = r.int(2, 5), e8 = nz(r, -6, 6), f8 = nz(r, -4, 4);
        A = a8 * b8 - d8; B = -a8 * c8 - d8 * e8; C2 = f8; need(A !== C2);
        var X8 = wantsFraction(ctx) ? fracBound(ctx) : F(k), g8 = nz(r, -6, 6);
        var h8 = Fr.of(A).mul(X8).add(B).sub(Fr.of(f8).mul(X8.sub(g8))); need(h8.isInt());
        e = rel(grp(a8, axb(b8, -c8)) + '-' + grp(d8, xb(e8)), op, K.addConst(grp(f8, xb(-g8)), h8)); variant = 'groups';
        steps.push(step('Distribute on both sides.', rel(lin([[a8 * b8, 'x'], [-a8 * c8, ''], [-d8, 'x'], [-d8 * e8, '']]), op, lin([[f8, 'x'], [-f8 * g8, ''], [h8, '']])), 2));
        steps.push(step('Combine like terms on each side.', rel(axb(A, B), op, axb(f8, h8.sub(f8 * g8))), 1));
        res = K.solveIneq(steps, A, B, f8, h8.sub(f8 * g8), op); need(res.k.eq(X8));
      }
      return solved(ctx, e, res, steps, variant);
    }
  });

  /* ================= SOLVE · all real numbers / no solution ================= */
  skill({
    id: 'ineq-special', best: [1, 2], tag: 'SOLVE', name: 'All real numbers or no solution?',
    blurb: 'Same x-terms on both sides (CP2) → after distributing (CP1) → after distributing and combining on both sides (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, op = pickOp(r), P = nz(r, -6, 6), Q = nz(r, -12, 12), Q2 = Q + nz(r, -9, 9), P2 = P;
      var one = r.chance(0.2); if (one) { P2 = nz(r, -6, 6); need(P2 !== P); var kOne = nz(r, -8, 8); Q2 = Q + (P - P2) * kOne; }
      function form(PP, QQ, lvl) {
        if (lvl <= 0) return axb(PP, QQ);
        if (lvl === 1) { need(Math.abs(PP) > 1); var m = nz(r, -6, 6); return K.addConst(grp(PP, xb(m)), QQ - PP * m); }
        if (lvl === 2) { var kk = nz(r, -5, 5), j = PP - kk; need(j !== 0 && Math.abs(kk) > 1); var m2 = nz(r, -5, 5); return K.addConst(K.addX(grp(kk, xb(m2)), j), QQ - kk * m2); }
        var k1 = r.int(2, 5), k2 = -r.int(2, 4), u = PP - k1 - k2; var m3 = nz(r, -5, 5), m4 = nz(r, -5, 5), rr = QQ - k1 * m3 - k2 * m4;
        return K.addConst(K.addX(grp(k1, xb(m3)) + '-' + grp(-k2, xb(m4)), u), rr);
      }
      var lv = c <= 2 ? 0 : c <= 4 ? 1 : c <= 6 ? 2 : 3;
      var e = rel(form(P, Q, lv), op, form(P2, Q2, c <= 3 ? 0 : lv - 1)), steps = [step('', e, 0)];
      if (lv) steps.push(step('Simplify each side.', rel(axb(P, Q), op, axb(P2, Q2)), 1));
      var ans, res;
      if (!one) {
        steps.push(step('Subtract ' + M(lin([[P, 'x']])) + ' from both sides.', rel(String(Q), op, String(Q2)), 2));
        var holds = op === '<' ? Q < Q2 : op === '>' ? Q > Q2 : op === '<=' ? Q <= Q2 : Q >= Q2;
        steps.push(step(holds ? 'That is always true, so every number works.' : 'That is never true, so no number works.', '', 1));
        ans = holds ? 'All real numbers' : 'No solution';
      } else { res = K.solveIneq(steps, P, Q, P2, Q2, op); ans = M(K.ans('x', res.op, res.k)); need(res.k.isInt() || !ctx.intOnly); }
      return {
        variant: (one ? 'one' : 'special') + lv, prompt: 'Solve ' + M(e) + '. If every number is a solution, or no number is, say so.',
        parts: [{ answer: ans, check: { type: 'ineq', ineq: e, v: 'x', allowSpecial: true } }], steps: steps, space: [1.0, 1.25, 1.5]
      };
    }
  });

  /* ================= COMPOUND · and ================= */
  function interval(k1, c1, k2, c2) { return num(k1) + (c1 ? '\\le ' : '<') + 'x' + (c2 ? '\\le ' : '<') + num(k2); }
  skill({
    id: 'compound-and', best: [0, 1, 2], tag: 'COMPOUND', name: 'Solve and graph compound “and” inequalities',
    blurb: 'a < x + b ≤ c (CP2) → a negative coefficient or two separate inequalities (CP1) → fraction middles (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, k1 = nz(r, -8, 6), k2 = k1 + r.int(2, 9), lowC = r.chance(0.5), upC = r.chance(0.5), steps = [], e, variant;
      var K1 = F(k1), K2 = F(k2);
      if (c === 7 && wantsFraction(ctx)) { K1 = fracBound(ctx); K2 = K1.add(r.int(2, 7)); }
      var o1 = lowC ? '<=' : '<', o2 = upC ? '<=' : '<';
      if (c <= 3 || c === 5 || c === 6 || c === 7) {
        var b = c === 1 ? 1 : c === 2 ? r.int(2, 5) : c === 3 ? -r.int(2, 5) : c === 5 ? r.int(2, 4) : -r.int(2, 4), cc = nz(r, -9, 9), den = c >= 5 ? r.int(2, 4) : 1;
        if (c === 7) { b = r.chance(0.4) ? r.int(2, 5) : -r.int(2, 5); den = r.int(2, 3); }
        var mid = function (X) { return Fr.of(b).mul(X).add(cc).div(den); };
        var lo, hi, opA, opB;
        if (b > 0) { lo = mid(K1); hi = mid(K2); opA = o1; opB = o2; } else { lo = mid(K2); hi = mid(K1); opA = o2; opB = o1; }
        need(lo.isInt() && hi.isInt());
        var midTeX = den === 1 ? axb(b, cc) : '\\frac{' + axb(b, cc) + '}{' + den + '}';
        e = num(lo) + K.opTeX(opA) + midTeX + K.opTeX(opB) + num(hi); variant = 'chain' + (b > 0 ? '+' : '-') + den;
        steps.push(step('', e, 0));
        if (den !== 1) steps.push(step('Multiply all three parts by ' + den + '.', num(lo.mul(den)) + K.opTeX(opA) + axb(b, cc) + K.opTeX(opB) + num(hi.mul(den)), 1));
        steps.push(step('Undo the constant in all three parts.', num(lo.mul(den).sub(cc)) + K.opTeX(opA) + lin([[b, 'x']]) + K.opTeX(opB) + num(hi.mul(den).sub(cc)), 1));
        if (b !== 1) steps.push(step('Divide all three parts by ' + M(String(b)) + (b < 0 ? ' and reverse both signs.' : '.'), interval(K1, lowC, K2, upC), b < 0 ? 2 : 1));
      } else {
        // c = 4: two separate inequalities joined by "and"
        var a1 = r.int(2, 5), b1 = nz(r, -9, 9), a2 = -r.int(2, 5), b2 = nz(r, -9, 9);
        var left = rel(axb(a1, b1), o1 === '<' ? '>' : '>=', String(a1 * k1 + b1));   // x > k1  (or ≥)
        var right = rel(axb(a2, b2), o2 === '<' ? '>' : '>=', String(a2 * k2 + b2));  // flips to x < k2 (or ≤)
        e = left + '\\text{ and }' + right; variant = 'separate';
        steps.push(step('', e, 0));
        steps.push(partial(step('Solve the first inequality.', K.ans('x', o1 === '<' ? '>' : '>=', k1), 1)));
        steps.push(partial(step('Solve the second (dividing by a negative reverses the sign).', K.ans('x', o2, k2), 2)));
        steps.push(step('“And” means both are true.', interval(K1, lowC, K2, upC), 1));
      }
      var win = K.window(r, [K1, K2], true);
      steps.push(step('Graph: ' + (lowC ? 'closed' : 'open') + ' circle at ' + M(num(K1)) + ', ' + (upC ? 'closed' : 'open') + ' circle at ' + M(num(K2)) + ', shade between.', '', 1));
      return {
        variant: variant, prompt: 'Solve ' + M(e) + ' and graph the solution.', fig: K.line(win),
        parts: [{ answer: M(interval(K1, lowC, K2, upC)), check: { type: 'ineq', ineq: e, v: 'x' }, answerFig: K.line(win, [{ lo: K.toPair(K1), loC: lowC, hi: K.toPair(K2), hiC: upC }]) }],
        steps: steps, space: [1.0 + 0.1 * c, 1.2 + 0.12 * c, 1.45 + 0.14 * c]
      };
    }
  });

  /* ================= COMPOUND · or ================= */
  skill({
    id: 'compound-or', best: [1, 2], tag: 'COMPOUND', name: 'Solve and graph compound “or” inequalities',
    blurb: 'x + a < b or x − c > d (CP2) → coefficients, one negative (CP1) → fractions and overlapping rays (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, k1 = nz(r, -9, 4), k2 = k1 + r.int(2, 9), lc = r.chance(0.5), rc = r.chance(0.5), steps = [];
      var overlap = c >= 6 && r.chance(0.25);
      if (overlap) { var t = k1; k1 = k2; k2 = t; }                     // x < big or x > small  -> every number
      var oL = lc ? '<=' : '<', oR = rc ? '>=' : '>';
      function piece(k, op, lvl) {
        if (lvl === 0) { var b = nz(r, -9, 9); return { tex: rel(xb(b), op, String(k + b)), how: 'Undo the constant.' }; }
        if (lvl >= 4) { var qd = r.int(2, 4), pn = nz(r, -3, 3); need(gcd(Math.abs(pn), qd) === 1); var fa = F(pn, qd), bb = nz(r, -9, 9); need(k % qd === 0);
          return { tex: rel(axb(fa, bb), pn < 0 ? K.flip(op) : op, num(fa.mul(k).add(bb))), how: 'Undo the constant, then multiply by ' + M(num(fa.inv())) + (pn < 0 ? ' and reverse the sign.' : '.') }; }
        var a = r.int(2, 6) * (lvl >= 2 && r.chance(0.5) ? -1 : 1), b2 = nz(r, -12, 12);
        if (lvl >= 3 && r.chance(0.5)) { var m = nz(r, -5, 5), kk = a * m; return { tex: rel('\\frac{x}{' + a + '}' + K.addConst('', b2), a < 0 ? K.flip(op) : op, String(m + b2)), how: 'Undo the constant, then multiply by ' + M(String(a)) + (a < 0 ? ' and reverse the sign.' : '.'), k: kk }; }
        return { tex: rel(axb(a, b2), a < 0 ? K.flip(op) : op, String(a * k + b2)), how: 'Undo the constant, then divide by ' + M(String(a)) + (a < 0 ? ' and reverse the sign.' : '.') };
      }
      var lvl = c <= 2 ? 0 : c <= 3 ? 1 : c <= 5 ? 2 : c === 6 ? 3 : 4;
      var P1 = piece(k1, oL, lvl); if (P1.k !== undefined) k1 = P1.k;
      var P2 = piece(k2, oR, lvl); if (P2.k !== undefined) k2 = P2.k;
      if (!overlap) need(k1 < k2); else need(k1 > k2);
      var e = P1.tex + '\\text{ or }' + P2.tex, ans, fig, win = K.window(r, [k1, k2], true);
      steps.push(step('', e, 0)); steps.push(partial(step('First: ' + P1.how, K.ans('x', oL, k1), 1))); steps.push(partial(step('Second: ' + P2.how, K.ans('x', oR, k2), 1)));
      if (overlap) {
        ans = 'All real numbers'; steps.push(step('The two rays overlap and cover the whole line, so every number works.', '', 2));
        fig = K.line(win, [{ lo: null, loC: false, hi: null, hiC: false }]);
      } else {
        ans = M(K.ans('x', oL, k1)) + ' or ' + M(K.ans('x', oR, k2)); steps.push(step('“Or” keeps both rays.', '', 1));
        fig = K.line(win, [{ lo: null, loC: false, hi: [k1, 1], hiC: lc }, { lo: [k2, 1], loC: rc, hi: null, hiC: false }]);
      }
      return {
        variant: 'or' + lvl + (overlap ? 'all' : ''), prompt: 'Solve ' + M(e) + ' and graph the solution.', fig: K.line(win),
        parts: [{ answer: ans, check: { type: 'ineq', ineq: e, v: 'x', allowSpecial: overlap }, answerFig: fig }], steps: steps, space: [1.1 + 0.1 * c, 1.35 + 0.12 * c, 1.6 + 0.14 * c]
      };
    }
  });

  /* ================= COMPOUND · absolute value ================= */
  skill({
    id: 'abs-ineq', best: [1, 2], tag: 'COMPOUND', name: 'Solve absolute value inequalities',
    blurb: '|x| < a (CP2) → |x − h| and |ax + b| (CP1) → isolating the absolute value first, special cases (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, op = pickOp(r), rad = r.int(1, 8), m = c <= 2 ? 0 : nz(r, -6, 6), steps = [], e, inner, a = 1, k = 1, s = 0;
      var special = c === 7 && r.chance(0.35);
      if (c >= 5) a = r.int(2, 4);
      if (c >= 6) { k = r.int(2, 4); s = nz(r, -9, 9); }
      inner = a === 1 ? xb(-m) : axb(a, -a * m);
      var rhs = a * rad;
      if (special) {
        var neg = -r.int(1, 6);
        e = rel(K.addConst(K.cp(k) + '|' + inner + '|', s), op, String(k * neg + s));
        steps.push(step('', e, 0));
        if (k !== 1 || s) steps.push(step('Isolate the absolute value.', rel('|' + inner + '|', op, String(neg)), 1));
        var all = op[0] === '>';
        steps.push(step('An absolute value is never negative, so it is ' + (all ? 'always greater than' : 'never less than') + ' ' + M(String(neg)) + '.', '', 2));
        var win0 = K.window(r, [m], true);
        return { variant: 'abs-special', prompt: 'Solve ' + M(e) + '. If every number is a solution, or no number is, say so.', fig: K.line(win0),
          parts: [{ answer: all ? 'All real numbers' : 'No solution', check: { type: 'ineq', ineq: e, v: 'x', allowSpecial: true }, answerFig: all ? K.line(win0, [{ lo: null, loC: false, hi: null, hiC: false }]) : null }],
          steps: steps, space: [1.2, 1.5, 1.8] };
      }
      e = rel(K.addConst(K.cp(k) + '|' + inner + '|', s), op, String(k * rhs + s));
      steps.push(step('', e, 0));
      if (k !== 1 || s) steps.push(step('Isolate the absolute value.', rel('|' + inner + '|', op, String(rhs)), 1));
      var lo = F(m - rad), hi = F(m + rad), closed = op.length > 1, ans, fig;
      var win = K.window(r, [lo, hi], true);
      if (op[0] === '<') {
        steps.push(step('“Less than” means between: write a compound inequality.', String(-rhs) + K.opTeX(op) + inner + K.opTeX(op) + rhs, 2));
        if (a !== 1 || m) steps.push(step('Solve all three parts.', interval(lo, closed, hi, closed), 1));
        ans = M(interval(lo, closed, hi, closed)); fig = K.line(win, [{ lo: K.toPair(lo), loC: closed, hi: K.toPair(hi), hiC: closed }]);
      } else {
        steps.push(step('“Greater than” means outside: write two inequalities joined by “or”.', rel(inner, K.flip(op), String(-rhs)) + '\\text{ or }' + rel(inner, op, String(rhs)), 2));
        steps.push(step('Solve each one.', '', 1));
        ans = M(K.ans('x', closed ? '<=' : '<', lo)) + ' or ' + M(K.ans('x', closed ? '>=' : '>', hi));
        fig = K.line(win, [{ lo: null, loC: false, hi: K.toPair(lo), hiC: closed }, { lo: K.toPair(hi), loC: closed, hi: null, hiC: false }]);
      }
      steps.push(step('Graph the solution.', '', 1));
      return { variant: 'abs' + (a > 1 ? 'a' : '') + (k > 1 ? 'k' : '') + (op[0] === '<' ? 'and' : 'or'), prompt: 'Solve ' + M(e) + ' and graph the solution.', fig: K.line(win),
        parts: [{ answer: ans, check: { type: 'ineq', ineq: e, v: 'x' }, answerFig: fig }], steps: steps, space: [1.1 + 0.1 * c, 1.35 + 0.12 * c, 1.6 + 0.14 * c] };
    }
  });

  /* ================= REASON · graphs ================= */
  skill({
    id: 'graph-read', best: [0, 1], tag: 'REASON', name: 'Graph inequalities and read graphs',
    blurb: 'Graph or read a ray (CP2) → read and draw intervals (CP1) → “or” graphs and absolute value inequalities for a graph (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, k1 = nz(r, -7, 5), k2 = k1 + 2 * r.int(1, 4), cl1 = r.chance(0.5), cl2 = r.chance(0.5), op = pickOp(r);
      var win = K.window(r, [k1, k2], true), pieces, ansTeX, mode = c === 1 ? 'draw-ray' : c === 2 ? 'read-ray' : c === 3 ? 'read-and' : c === 4 ? 'read-or' : c === 5 ? 'draw-or' : c === 6 ? 'abs-and' : 'abs-or';
      var steps = [];
      if (mode === 'draw-ray' || mode === 'draw-or') {
        var e = mode === 'draw-ray' ? K.ans('x', op, k1) : K.ans('x', cl1 ? '<=' : '<', k1) + '\\text{ or }' + K.ans('x', cl2 ? '>=' : '>', k2);
        pieces = mode === 'draw-ray' ? K.rayPieces(op, k1) : [{ lo: null, loC: false, hi: [k1, 1], hiC: cl1 }, { lo: [k2, 1], loC: cl2, hi: null, hiC: false }];
        steps.push(step(mode === 'draw-ray' ? (op.length > 1 ? 'Closed' : 'Open') + ' circle at ' + M(String(k1)) + ' (' + (op.length > 1 ? 'included' : 'not included') + '), shade ' + (op[0] === '<' ? 'left.' : 'right.') : 'Circles at ' + M(String(k1)) + ' and ' + M(String(k2)) + ' (filled when included), shade between.', '', 3));
        return { variant: mode, prompt: 'Graph ' + M(e) + ' on the number line.', fig: K.line(win),
          parts: [{ answer: M(e), check: { type: 'ineq', ineq: e, v: 'x' }, answerFig: K.line(win, pieces) }], steps: steps, space: [0.3, 0.4, 0.5] };
      }
      var form = null, twoForms = mode.indexOf('abs') === 0;
      if (mode === 'read-ray') { pieces = K.rayPieces(op, k1); ansTeX = M(K.ans('x', op, k1)); }
      else if (mode === 'read-and') { pieces = [{ lo: [k1, 1], loC: cl1, hi: [k2, 1], hiC: cl2 }]; ansTeX = M(interval(F(k1), cl1, F(k2), cl2)); }
      else if (mode === 'read-or') { pieces = [{ lo: null, loC: false, hi: [k1, 1], hiC: cl1 }, { lo: [k2, 1], loC: cl2, hi: null, hiC: false }]; ansTeX = M(K.ans('x', cl1 ? '<=' : '<', k1)) + ' or ' + M(K.ans('x', cl2 ? '>=' : '>', k2)); }
      else {
        var mid = (k1 + k2) / 2, rad = (k2 - k1) / 2, inner = xb(-mid);
        form = 'abs';
        if (mode === 'abs-and') { pieces = [{ lo: [k1, 1], loC: cl1, hi: [k2, 1], hiC: cl1 }]; ansTeX = M('|' + inner + '|' + (cl1 ? '\\le ' : '<') + rad); }
        else { pieces = [{ lo: null, loC: false, hi: [k1, 1], hiC: cl1 }, { lo: [k2, 1], loC: cl1, hi: null, hiC: false }]; ansTeX = M('|' + inner + '|' + (cl1 ? '\\ge ' : '>') + rad); }
        steps.push(step('The center is ' + M(String(mid)) + ' (halfway between ' + M(String(k1)) + ' and ' + M(String(k2)) + '); the distance to each end is ' + M(String(rad)) + '.', '', 2));
      }
      steps.push(step('Filled circles mean “or equal to”; the shading shows the direction.', '', 2));
      if (twoForms) {
        var plain = mode === 'abs-and' ? M(interval(F(k1), cl1, F(k2), cl1)) : M(K.ans('x', cl1 ? '<=' : '<', k1)) + ' or ' + M(K.ans('x', cl1 ? '>=' : '>', k2));
        return { variant: mode, prompt: 'The graph shows the solutions of an inequality.', fig: K.line(win, pieces),
          parts: [{ label: 'a', prompt: 'Write the inequality without absolute value.', answer: plain, check: { type: 'read-graph', v: 'x' } },
                  { label: 'b', prompt: 'Write it as an absolute value inequality.', answer: ansTeX, check: { type: 'read-graph', v: 'x', form: 'abs' } }],
          steps: steps, space: [0.8, 1.0, 1.25] };
      }
      return { variant: mode, prompt: 'Write an inequality for the solutions shown on the graph.',
        fig: K.line(win, pieces), parts: [{ answer: ansTeX, check: { type: 'read-graph', v: 'x', form: form } }], steps: steps, space: [0.45, 0.6, 0.8] };
    }
  });

  /* ================= REASON · test values ================= */
  skill({
    id: 'check-values', best: [0, 1], tag: 'REASON', name: 'Decide which values are solutions',
    blurb: 'Simple inequalities (CP2) → two-step with negatives (CP1) → compound and absolute value (Honors). Boundary values test open vs. closed.',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, op = pickOp(r), k = nz(r, -6, 6), e, cond;
      if (c <= 2) { var b = nz(r, -9, 9); e = rel(xb(b), op, String(k + b)); }
      else if (c <= 4) { var a = nz(r, -6, 6); need(Math.abs(a) > 1); var b2 = nz(r, -9, 9); e = rel(axb(a, b2), op, String(a * k + b2)); }
      else if (c <= 5) { var k2 = k + r.int(2, 6); e = interval(F(k), r.chance(0.5), F(k2), r.chance(0.5)); var b3 = nz(r, -6, 6); e = e.replace('x', xb(b3)); e = e.replace(/^(-?\d+)/, function (d) { return String(+d + b3); }).replace(/(-?\d+)$/, function (d) { return String(+d + b3); }); }
      else if (c === 6) { var rad = r.int(1, 5), aa = r.int(2, 3); e = rel('|' + axb(aa, -aa * k) + '|', op, String(aa * rad)); }
      else { var rad7 = r.int(1, 4), kq = r.int(2, 3), sq = nz(r, -8, 8); e = rel(K.addConst(kq + '|' + xb(-k) + '|', sq), op, String(kq * rad7 + sq)); }
      var pool = []; for (var t = k - 6; t <= k + 6; t++) pool.push(t);
      var vals = r.shuffle(pool).slice(0, c <= 2 ? 4 : c <= 5 ? 5 : 6);
      if (vals.indexOf(k) < 0) vals[0] = k;                                  // always test the boundary
      vals.sort(function (p, q) { return p - q; });
      var yes = vals.filter(function (v) { return evalCond(e, v); });
      need(yes.length >= 1 && yes.length < vals.length);
      var list = vals.map(function (v) { return M(String(v)); }).join(', ');
      return {
        variant: 'values' + (c <= 2 ? 1 : c <= 4 ? 2 : c <= 5 ? 3 : 4),
        prompt: 'Which of the numbers ' + list + ' are solutions of ' + M(e) + '? Show how you checked each one.',
        parts: [{ answer: yes.map(function (v) { return M(String(v)); }).join(', '), check: { type: 'ineq-members', ineq: e, v: 'x', values: vals.map(String) } }],
        steps: [step('Substitute each number and decide whether the statement is true.', '', 3), step('Solutions: ' + yes.join(', ') + '.', '', 2)],
        space: [0.9, 1.15, 1.4]
      };
    }
  });
  /* generator-side evaluation for the shapes above (the verifier recomputes independently) */
  function evalCond(e, v) {
    var parts = e.replace(/\\le /g, '≤').replace(/\\ge /g, '≥').split(/(<|>|≤|≥)/);
    function val(s) { var t = s.replace(/\|([^|]*)\|/g, 'Math.abs($1)').replace(/(\d)Math/g, '$1*Math').replace(/(\d)x/g, '$1*x').replace(/x/g, '(' + v + ')').replace(/(\d)\(/g, '$1*(').replace(/\)\(/g, ')*('); return Function('return ' + t)(); }
    var ok = true;
    for (var i = 1; i < parts.length; i += 2) {
      var A = val(parts[i - 1]), B = val(parts[i + 1]), o = parts[i];
      ok = ok && (o === '<' ? A < B : o === '>' ? A > B : o === '≤' ? A <= B : A >= B);
    }
    return ok;
  }

  /* ================= REASON · find the mistake ================= */
  var STUDENTS = ['Ravi', 'Maya', 'Jordan', 'Priya', 'Luis', 'Zoe', 'Sam', 'Elena'];
  skill({
    id: 'error-analysis', best: [1, 2], tag: 'REASON', name: 'Find and fix the mistake',
    blurb: 'Forgot to reverse the sign (CP2) → distributing or moving terms incorrectly (CP1) → errors inside longer solutions (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, who = r.pick(STUDENTS), op = pickOp(r), k = nz(r, -9, 9), lines = [], kind, orig;
      // correct state A·x + B (op) C·x + D, written line by line; one line is altered and the rest follow from it
      if (c <= 2) {
        var a = -r.int(2, 6), b = nz(r, -9, 9), R = a * k + b; orig = rel(axb(a, b), op, String(R)); kind = 'noflip';
        lines.push(rel(lin([[a, 'x']]), op, String(R - b)));
        lines.push(K.ans('x', op, F(R - b, a)));                        // did not reverse the sign
      } else if (c <= 4) {
        var p6 = r.pick([2, 3, 4]), a6 = nz(r, -5, 5), b6 = nz(r, -9, 9), c6 = nz(r, -4, 4);
        need(Math.abs(a6) > 1 && a6 !== c6 * p6);
        var X = F(k), d6 = Fr.of(a6).mul(X).add(b6).div(p6).sub(Fr.of(c6).mul(X)); need(d6.isInt());
        orig = rel('\\frac{' + axb(a6, b6) + '}{' + p6 + '}', op, axb(c6, d6));
        kind = r.pick(['lcd', 'noflip']);
        if (kind === 'lcd') {   // multiplied only the left side by the denominator
          lines.push(rel(axb(a6, b6), op, axb(c6, d6)));
          var A6 = a6 - c6; need(A6 !== 0);
          lines.push(rel(lin([[A6, 'x']]), op, num(d6.sub(b6))));
          lines.push(K.ans('x', A6 < 0 ? K.flip(op) : op, d6.sub(b6).div(A6)));
        } else {
          var A7 = a6 - p6 * c6; need(A7 < 0);
          lines.push(rel(axb(a6, b6), op, axb(p6 * c6, d6.mul(p6))));
          lines.push(rel(lin([[A7, 'x']]), op, num(d6.mul(p6).sub(b6))));
          lines.push(K.ans('x', op, d6.mul(p6).sub(b6).div(A7)));        // forgot to reverse
        }
      } else if (c === 7) {
        // a(x + b) − c(x − d) op e·x + f, with the second group distributed with the wrong sign
        var a7 = r.int(2, 6), b7 = nz(r, -6, 6), c7 = r.int(2, 5), d7 = r.int(1, 7), e7 = nz(r, -4, 4);
        var A1 = a7 - c7, B1 = a7 * b7 + c7 * d7; need(A1 !== e7);
        var f7 = (A1 - e7) * k + B1; need(f7 !== 0);
        orig = rel(grp(a7, xb(b7)) + '-' + grp(c7, xb(-d7)), op, axb(e7, f7)); kind = 'sign2';
        var Bw7 = a7 * b7 - c7 * d7;                                       // wrote −c(x − d) as −cx − cd
        lines.push(rel(lin([[a7, 'x'], [a7 * b7, ''], [-c7, 'x'], [-c7 * d7, '']]), op, axb(e7, f7)));
        lines.push(rel(axb(A1, Bw7), op, axb(e7, f7)));
        lines.push(rel(lin([[A1 - e7, 'x']]), op, String(f7 - Bw7)));
        lines.push(K.ans('x', A1 - e7 < 0 ? K.flip(op) : op, F(f7 - Bw7, A1 - e7)));
      } else {
        var e5 = r.int(2, 5), f5 = nz(r, -6, 6), d5 = r.int(2, 12), g5 = r.int(1, 4) * r.sign(), A = -e5, B = d5 - e5 * f5, h5 = (A - g5) * k + B;
        need(A !== g5 && h5 !== 0);
        orig = rel(d5 + '-' + grp(e5, xb(f5)), op, axb(g5, h5));
        kind = r.pick(['distribute', 'sign']);
        if (kind === 'distribute') {
          var Bw = d5 - f5; need(Bw !== B);                               // multiplied only the x
          lines.push(rel(lin([[d5, ''], [-e5, 'x'], [-f5, '']]), op, axb(g5, h5)));
          lines.push(rel(axb(A, Bw), op, axb(g5, h5)));
          lines.push(rel(lin([[A - g5, 'x']]), op, String(h5 - Bw)));
          var kw = F(h5 - Bw, A - g5); lines.push(K.ans('x', A - g5 < 0 ? K.flip(op) : op, kw));
        } else {
          lines.push(rel(lin([[d5, ''], [-e5, 'x'], [-e5 * f5, '']]), op, axb(g5, h5)));
          lines.push(rel(axb(A, B), op, axb(g5, h5)));
          var wrongA = A + g5; need(wrongA !== 0 && wrongA !== A - g5);    // added g·x instead of subtracting
          lines.push(rel(lin([[wrongA, 'x']]), op, String(h5 - B)));
          lines.push(K.ans('x', wrongA < 0 ? K.flip(op) : op, F(h5 - B, wrongA)));
        }
      }
      var why = { noflip: 'divided by a negative number but did not reverse the inequality sign', distribute: 'did not multiply every term inside the parentheses', sign: 'moved the x-term to the other side without changing its sign', lcd: 'multiplied only one side by the denominator', sign2: '' }[kind];
      if (kind === 'sign2') why = 'distributed −' + c7 + ' but wrote −' + c7 * d7 + ' instead of +' + c7 * d7 + ' (a negative times a negative is positive)';
      var steps = [], res;
      // correct solution, worked from the original
      var correct = NS.check.solutionSet(orig.replace(/\\le /g, '\\le ').replace(/\\ge /g, '\\ge '), 'x');
      var ansText = NS.check.setText(correct, 'x');
      need(correct.length === 1 && (!correct[0].lo !== !correct[0].hi));
      var ks = correct[0].lo || correct[0].hi; need(ks.isInt() || !ctx.intOnly);
      var firstWrong = 0;
      lines.forEach(function (ln, i) { if (!firstWrong && !NS.check.setEqual(NS.check.solutionSet(ln, 'x'), correct)) firstWrong = i + 1; });
      need(firstWrong > 0);
      steps.push(step('Line ' + firstWrong + ': ' + who + ' ' + why + '.', '', 3));
      steps.push(step('Correct solution:', ansText, 3));
      return {
        variant: 'error-' + kind, prompt: who + ' solved ' + M(orig) + ' like this:', work: lines,
        parts: [{ label: 'a', prompt: 'Which line has the first mistake? Explain what went wrong.', answer: 'Line ' + firstWrong + ': ' + who + ' ' + why + '.', check: { type: 'error-line', ineq: orig, lines: lines, v: 'x' } },
                { label: 'b', prompt: 'Solve the inequality correctly.', answer: M(ansText), check: { type: 'ineq', ineq: orig, v: 'x' } }],
        steps: steps, space: [1.3, 1.6, 1.9]
      };
    }
  });

  /* ================= APPLY · word problems ================= */
  var ITEMS = [['Movie tickets', 'ticket', 'tickets', 't'], ['Notebooks', 'notebook', 'notebooks', 'n'], ['Songs', 'song', 'songs', 's'], ['Bus passes', 'pass', 'passes', 'p']];
  var NAMES = ['Sam', 'Maya', 'Jordan', 'Ana', 'Luis', 'Kai', 'Nora', 'Theo'];
  skill({
    id: 'apply', best: [0, 1, 2], tag: 'APPLY', name: 'Write and solve inequalities from word problems',
    blurb: 'Buying with a budget (CP2) → fees, saving goals, comparing plans (CP1) → compound budgets and averages with interpretation (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, who = r.pick(NAMES), mode = c <= 1 ? 'buy-max' : c === 2 ? 'fee-max' : c === 3 ? 'save-min' : c === 4 ? 'plans' : c === 5 ? (r.chance(0.5) ? 'range' : 'average') : c === 6 ? 'average' : 'range3';
      var parts, prompt, steps = [], v;
      if (mode === 'buy-max') {
        var it = r.pick(ITEMS), price = r.int(3, 15), budget = price * r.int(3, 9) + r.int(1, price - 1); v = it[3];
        var best = Math.floor(budget / price);
        prompt = it[0] + ' cost $' + price + ' each. ' + who + ' has $' + budget + '. Write an inequality for the number of ' + it[2] + ', ' + M(v) + ', that ' + who + ' can buy. Solve it and explain what your answer means.';
        parts = [{ label: 'a', prompt: '', answer: M(price + v + '\\le ' + budget), check: { type: 'model-ineq', scenario: 'buy-max', v: v } },
                 { label: 'b', prompt: '', answer: M(v + '\\le ' + num(F(budget, price))) + ', so ' + who + ' can buy at most ' + best + ' ' + it[2] + '.', check: { type: 'iscenario', scenario: 'buy-max', v: v, want: 'best' } }];
        steps.push(step('Cost of ' + M(v) + ' ' + it[2] + ' is at most the money available.', price + v + '\\le ' + budget, 2), step('Divide by ' + price + '.', v + '\\le ' + num(F(budget, price)), 1), step('Only whole ' + it[2] + ' can be bought, so the most is ' + best + '.', '', 2));
      } else if (mode === 'fee-max') {
        var fee = 5 * r.int(2, 10), rate = r.int(6, 25), n = r.int(4, 14), cap = fee + rate * n + r.int(0, rate - 1); v = 'm';
        prompt = 'A gym charges a $' + fee + ' joining fee plus $' + rate + ' per month. ' + who + ' can spend at most $' + cap + '. Write and solve an inequality for the number of months, ' + M(v) + ', and state the answer in words.';
        parts = [{ label: 'a', prompt: '', answer: M(fee + '+' + rate + 'm\\le ' + cap), check: { type: 'model-ineq', scenario: 'fee-max', v: v } },
                 { label: 'b', prompt: '', answer: M('m\\le ' + num(F(cap - fee, rate))) + ', so ' + who + ' can belong for at most ' + n + ' months.', check: { type: 'iscenario', scenario: 'fee-max', v: v, want: 'best' } }];
        steps.push(step('Fee plus monthly cost is at most the budget.', fee + '+' + rate + 'm\\le ' + cap, 2), step('Subtract ' + fee + ', then divide by ' + rate + '.', 'm\\le ' + num(F(cap - fee, rate)), 2), step('Whole months only: at most ' + n + '.', '', 1));
      } else if (mode === 'save-min') {
        var start = 5 * r.int(2, 12), save = r.int(8, 25), goal = start + save * r.int(4, 14) - r.int(0, save - 1); v = 'w';
        var wmin = Math.ceil((goal - start) / save); need(goal > start);
        prompt = who + ' has $' + start + ' and saves $' + save + ' each week. Write and solve an inequality to find how many weeks, ' + M(v) + ', it will take to have at least $' + goal + '.';
        parts = [{ label: 'a', prompt: '', answer: M(start + '+' + save + 'w\\ge ' + goal), check: { type: 'model-ineq', scenario: 'save-min', v: v } },
                 { label: 'b', prompt: '', answer: M('w\\ge ' + num(F(goal - start, save))) + ', so it takes at least ' + wmin + ' weeks.', check: { type: 'iscenario', scenario: 'save-min', v: v, want: 'best' } }];
        steps.push(step('Savings must be at least the goal.', start + '+' + save + 'w\\ge ' + goal, 2), step('Subtract ' + start + ', then divide by ' + save + '.', 'w\\ge ' + num(F(goal - start, save)), 2), step('Whole weeks: at least ' + wmin + '.', '', 1));
      } else if (mode === 'plans') {
        var f1 = 5 * r.int(2, 8), r1 = r.int(7, 15), r2 = r1 - r.int(2, 5), kk = r.int(5, 14), f2 = f1 + (r1 - r2) * kk + (r.chance(0.5) ? 0 : r.int(1, r1 - r2 - 1 || 1)); v = 'n';
        need(r2 > 1 && f2 > f1);
        var kq = F(f2 - f1, r1 - r2), most = kq.isInt() ? kq.n - 1 : Math.floor(kq.n / kq.d);
        prompt = 'Studio A charges a $' + f1 + ' sign-up fee plus $' + r1 + ' per class. Studio B charges a $' + f2 + ' sign-up fee plus $' + r2 + ' per class. For how many classes, ' + M(v) + ', is Studio A cheaper? Write and solve an inequality.';
        parts = [{ label: 'a', prompt: '', answer: M(f1 + '+' + r1 + 'n<' + f2 + '+' + r2 + 'n'), check: { type: 'model-ineq', scenario: 'plans', v: v } },
                 { label: 'b', prompt: '', answer: M('n<' + num(kq)) + ', so Studio A is cheaper for at most ' + most + ' classes.', check: { type: 'iscenario', scenario: 'plans', v: v, want: 'best' } }];
        steps.push(step('Studio A’s cost is less than Studio B’s.', f1 + '+' + r1 + 'n<' + f2 + '+' + r2 + 'n', 2), step('Collect terms.', (r1 - r2) + 'n<' + (f2 - f1), 1), step('Divide by ' + (r1 - r2) + '.', 'n<' + num(kq), 1), step('Whole classes: up to ' + most + '.', '', 1));
      } else if (mode === 'range' || mode === 'range3') {
        var base = r.int(2, 6), per = r.int(2, 5), lo = r.int(2, 6), hi = lo + r.int(3, 9);
        var L$ = base + per * lo + (mode === 'range3' ? r.int(1, per - 1) : 0), H$ = base + per * hi + (mode === 'range3' ? r.int(1, per - 1) : 0); v = 'm';
        var loQ = F(L$ - base, per), hiQ = F(H$ - base, per);
        prompt = 'A taxi charges $' + base + ' plus $' + per + ' per mile. ' + who + ' wants to spend at least $' + L$ + ' and at most $' + H$ + '. Write and solve a compound inequality for the number of miles, ' + M(v) + '.';
        parts = [{ label: 'a', prompt: '', answer: M(L$ + '\\le ' + base + '+' + per + 'm\\le ' + H$), check: { type: 'model-ineq', scenario: 'range', v: v } },
                 { label: 'b', prompt: '', answer: M(num(loQ) + '\\le m\\le ' + num(hiQ)), check: { type: 'iscenario', scenario: 'range', v: v, want: 'set' } }];
        if (mode === 'range3') {
          var a3 = Math.ceil(loQ.n / loQ.d), b3 = Math.floor(hiQ.n / hiQ.d);
          prompt += ' Then list the whole numbers of miles that work.';
          parts.push({ label: 'c', prompt: '', answer: 'From ' + a3 + ' to ' + b3 + ' miles', check: { type: 'iscenario', scenario: 'range', v: v, want: 'range' } });
        }
        steps.push(step('The cost is between the two amounts.', L$ + '\\le ' + base + '+' + per + 'm\\le ' + H$, 2), step('Subtract ' + base + ' from all three parts, then divide by ' + per + '.', num(loQ) + '\\le m\\le ' + num(hiQ), 2));
      } else {
        var count = r.pick([3, 4]), target = r.pick([75, 80, 85, 88, 90]), scores = [];
        for (var i = 0; i < count; i++) scores.push(r.int(target - 12, Math.min(100, target + 8)));
        var sum = scores.reduce(function (s, x) { return s + x; }, 0), needQ = F(target * (count + 1) - sum);
        need(needQ.n > 0 && needQ.n <= 100);
        v = 's';
        prompt = who + ' scored ' + scores.slice(0, -1).join(', ') + ' and ' + scores[scores.length - 1] + ' on the first tests. What score, ' + M(v) + ', on the next test gives an average of at least ' + target + '? Write and solve an inequality.';
        // (the verifier reads the scores and the target from these words)
        parts = [{ label: 'a', prompt: '', answer: M('\\frac{' + sum + '+s}{' + (count + 1) + '}\\ge ' + target), check: { type: 'model-ineq', scenario: 'average', v: v } },
                 { label: 'b', prompt: '', answer: M('s\\ge ' + needQ.n) + ', so ' + who + ' needs at least ' + needQ.n + '.', check: { type: 'iscenario', scenario: 'average', v: v, want: 'best' } }];
        steps.push(step('The average of all ' + (count + 1) + ' scores is at least ' + target + '.', '\\frac{' + sum + '+s}{' + (count + 1) + '}\\ge ' + target, 2), step('Multiply by ' + (count + 1) + ', then subtract ' + sum + '.', 's\\ge ' + needQ.n, 2));
      }
      parts.forEach(function (pt) { pt.label = ''; });
      return { variant: mode, prompt: prompt, parts: parts, steps: steps, space: [1.3, 1.6, 2.0] };
    }
  });

  /* absolute value EQUATIONS: the shared generator from the Expressions & Equations file */
  skill(NS.absEqSkill('COMPOUND'));

  NS.registerSkillSet({
    id: 'algebra1-inequalities', course: 'algebra1', courseName: 'Algebra 1', unit: 'inequalities', unitName: 'Linear Inequalities',
    title: 'The Inequalities Bistro',
    tags: { SOLVE: 'Solve inequalities', COMPOUND: 'Compound and absolute value', REASON: 'Graphs, checking and error analysis', APPLY: 'Word problems' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Symbols</h4><p>⟨<⟩ less than · ⟨>⟩ greater than</p><p>⟨\\le⟩ at most · ⟨\\ge⟩ at least</p><p>Open circle: not included. Closed circle: included.</p></section>' +
      '<section><h4>The one rule that changes</h4><p>Multiplying or dividing both sides by a <b>negative</b> number reverses the sign: ⟨-2x<6⟩ → ⟨x>-3⟩.</p></section>' +
      '<section><h4>Compound inequalities</h4><p>“And”: both are true; the graph is the overlap, for example ⟨-1<x\\le 4⟩.</p><p>“Or”: either is true; the graph keeps both pieces.</p></section>' +
      '<section><h4>Absolute value</h4><p>⟨|x-h|<r⟩ → ⟨h-r<x<h+r⟩ (between)</p><p>⟨|x-h|>r⟩ → ⟨x<h-r⟩ or ⟨x>h+r⟩ (outside)</p><p>Isolate the absolute value first.</p></section>' +
      '<section><h4>Words</h4><p>at most, no more than → ⟨\\le⟩</p><p>at least, no less than → ⟨\\ge⟩</p><p>more than → ⟨>⟩ · less than, fewer than → ⟨<⟩</p></section>' +
      '<section><h4>Check</h4><p>Test a number from your shaded region in the original inequality.</p></section></div>',
    gaps: ['Inequalities in two variables are in Unit 6 (systems of inequalities).'],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
