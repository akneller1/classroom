/* Menu Assessment Generator — Algebra 1 · Expressions & Equations skill library.

   Every skill is answer-first: it chooses the solution, then builds the problem backward,
   so the numbers are always "nice" for the requested level. Difficulty is ONE number per
   problem, c = 1 … 7, and it changes the mathematics (structure, number size, signs,
   fractions, number of steps), not just a label:

        CP2 (foundational)  Appetizer 1 · Entrée 2 · Chef's Special 3
        CP1 (standard)      Appetizer 3 · Entrée 4 · Chef's Special 5
        Honors (advanced)   Appetizer 5 · Entrée 6 · Chef's Special 7

   A teacher can nudge any single problem up or down (c ± 1).

   Each generated problem carries `check` specs that name the exact student-facing math
   (the TeX shown inside ⟨…⟩). menu/verify.js re-reads that math with the independent
   checker in menu/mathcheck.js and recomputes every answer. If a generator here were
   wrong, the problem would be rejected, not printed.

   Reused from the worksheet generator: core/rng.js (seeded randomness), core/frac.js
   (exact fractions) and core/tex.js (lin/num TeX builders). */
(function (G) {
  'use strict';
  var WS = G.MKWS, NS = (G.MKMENU = G.MKMENU || {});
  var T = WS.tex, Fr = WS.frac.Fr, M = T.M, num = T.num, lin = T.lin, gcd = WS.frac.gcd;

  /* ---------- small helpers ---------- */
  function need(c, why) { if (!c) throw new WS.gen.Reject(why || 'constraint'); }
  function F(n, d) { return new Fr(n, d === undefined ? 1 : d); }
  function nz(r, lo, hi) { return r.nonzero(lo, hi); }
  function cp(a) { a = Fr.of(a); return a.eq(1) ? '' : a.eq(-1) ? '-' : num(a); }            // coefficient before (…)
  function grp(a, inner) { return cp(a) + '(' + inner + ')'; }
  function signed(first, a, body) {                                                          // "+ 3(…)" / "- 3(…)"
    a = Fr.of(a);
    if (first) return grp(a, body);
    return (a.sign() < 0 ? '-' : '+') + grp(a.abs(), body);
  }
  function addConst(s, k) { k = Fr.of(k); return k.isZero() ? s : s + (k.sign() < 0 ? '-' : '+') + num(k.abs()); }
  function addX(s, k, v) { k = Fr.of(k); if (k.isZero()) return s; return s + (k.sign() < 0 ? '-' : '+') + (k.abs().eq(1) ? '' : num(k.abs())) + (v || 'x'); }
  function xb(b, v) { return lin([[1, v || 'x'], [b, '']]); }                                // "x + b"
  function ax_b(a, b, v) { return lin([[a, v || 'x'], [b, '']]); }
  function eq(l, r) { return l + '=' + r; }
  function dec(n10) { var s = (Math.abs(n10) / 10).toFixed(1); return (n10 < 0 ? '-' : '') + s.replace(/\.0$/, ''); } // tenths -> "1.2"
  function step(t, m, w) { return { t: t || '', m: m || '', w: w === undefined ? 1 : w }; }
  function answerX(v, x) { return v + '=' + num(x); }
  function pickAnswer(ctx, lo, hi, allowZero) {
    var x = ctx.rng.int(lo, hi);
    if (!allowZero && x === 0) x = ctx.rng.chance(0.5) ? hi : lo;
    return x;
  }
  /* A non-integer answer, only when the teacher allows fractions (Honors default). */
  function fracAnswer(ctx) {
    var d = ctx.rng.int(2, 5), n = nz(ctx.rng, -14, 14);
    need(gcd(n, d) === 1 && Math.abs(n) > 1);
    return F(n, d);
  }
  function solveSpec(eqTeX, v) { return { type: 'solve', eq: eqTeX, v: v || 'x' }; }
  function wantsFraction(ctx) { return !ctx.intOnly && ctx.c >= 6 && ctx.rng.chance(0.5); }

  /* Work an equation a·x + b = c·x + d (already simplified) to the answer. */
  function finishLinear(steps, A, B, C, D, v) {
    v = v || 'x';
    A = Fr.of(A); B = Fr.of(B); C = Fr.of(C); D = Fr.of(D);
    if (!C.isZero()) {
      steps.push(step('Collect the ' + v + '-terms on one side.', eq(ax_b(A.sub(C), B, v), num(D)), 1));
      A = A.sub(C); C = F(0);
    }
    if (!B.isZero()) { steps.push(step('Undo the constant.', eq(lin([[A, v]]), num(D.sub(B))), 1)); D = D.sub(B); }
    var x = D.div(A);
    if (!A.eq(1)) steps.push(step(A.isInt() ? 'Divide both sides by ' + num(A) + '.' : 'Multiply both sides by the reciprocal.', answerX(v, x), 1));
    return x;
  }

  var skills = [];
  function skill(def) { skills.push(def); return def; }

  /* ============================================================
     SIMPLIFY · Combine like terms
     ============================================================ */
  skill({
    id: 'like-terms', best: [0, 1], tag: 'SIMPLIFY', name: 'Combine like terms',
    blurb: 'One variable (CP2) → two variables with negatives (CP1) → fractions and squared terms (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, kinds, maxK = c <= 2 ? 9 : 12;
      if (c <= 2) kinds = ['x', ''];
      else if (c <= 4) kinds = ['x', 'y', ''];
      else kinds = ctx.intOnly || c === 5 ? ['x^2', 'x', ''] : ['x^2', 'x', 'y', ''];
      var useFrac = !ctx.intOnly && c >= 5 && r.chance(0.6);
      var terms = [], result = [];
      kinds.forEach(function (k, i) {
        var total, a, b;
        if (useFrac && k === 'x') {
          var d1 = r.pick([2, 3, 4]), d2 = r.pick([2, 3, 4, 6]);
          a = F(nz(r, -5, 5), d1); b = F(nz(r, -5, 5), d2); total = a.add(b);
          need(!total.isZero() && !a.isInt() && !b.isInt());
        } else {
          total = c === 1 ? r.int(2, maxK + 3) : nz(r, -maxK, maxK);
          a = c === 1 ? r.int(1, total - 1) : nz(r, -maxK, maxK);
          b = Fr.of(total).sub(a);
          if (c === 1) need(Fr.of(b).sign() > 0 && !(Fr.of(a).eq(1) && Fr.of(b).eq(1)));
          need(!Fr.of(b).isZero());
          total = Fr.of(total);
        }
        terms.push([a, k]); terms.push([b, k]); result.push([total, k]);
      });
      if (c >= 4) { // a third term for one kind
        var pick = r.int(0, kinds.length - 1), extra = nz(r, -6, 6);
        terms.push([F(extra), kinds[pick]]); result[pick][0] = Fr.of(result[pick][0]).add(extra);
        need(!result[pick][0].isZero());
      }
      var order = c <= 1 ? terms : r.shuffle(terms);
      if (c === 1) order = [terms[0], terms[1], terms[2], terms[3]];
      need(Fr.of(order[0][0]).sign() > 0 || c >= 3);
      var expr = lin(order), ans = lin(result);
      need(expr.indexOf('+-') < 0);
      var grouped = kinds.map(function (k) {
        return '(' + lin(order.filter(function (t) { return t[1] === k; })) + ')';
      }).join('+');
      return {
        variant: 'k' + kinds.length + (useFrac ? 'f' : ''),
        prompt: 'Simplify ' + M(expr) + '.',
        parts: [{ answer: M(ans), check: { type: 'simplify', expr: expr, answer: ans } }],
        steps: [step('Group like terms.', grouped, 2), step('Add the coefficients of each kind of term.', ans, 2)],
        space: [0.9, 1.1, 1.3]
      };
    }
  });

  /* ============================================================
     DISTRIB · Distribute and simplify
     ============================================================ */
  skill({
    id: 'distribute', best: [0, 1], tag: 'DISTRIB', name: 'Distribute and simplify',
    blurb: 'One positive factor (CP2) → negative factors and two groups (CP1) → fraction factors and nested groups (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, expr, groups = [], extraX = 0, extraC = 0, steps = [], variant;
      function g(a, b, k) { groups.push({ a: Fr.of(a), b: Fr.of(b), k: Fr.of(k) }); }
      if (c === 1) { g(r.int(2, 6), r.int(1, 5), r.int(1, 9)); variant = 'one'; }
      else if (c === 2) { g(r.int(2, 6), r.int(1, 5), nz(r, -9, 9)); if (r.chance(0.5)) extraX = nz(r, -6, 6); else extraC = nz(r, -9, 9); variant = 'one+'; }
      else if (c === 3) { g(-r.int(2, 6), r.int(1, 5), nz(r, -9, 9)); extraX = nz(r, -7, 7); variant = 'neg'; }
      else if (c === 4) { g(r.int(2, 6), nz(r, -5, 5), nz(r, -9, 9)); g(nz(r, -6, 6), nz(r, -5, 5), nz(r, -9, 9)); variant = 'two'; }
      else if (c === 5) { g(r.int(2, 7), nz(r, -6, 6), nz(r, -9, 9)); g(-r.int(2, 7), nz(r, -6, 6), nz(r, -9, 9)); extraC = nz(r, -9, 9); variant = 'two-sub'; }
      else if (c === 6) {
        var d1 = r.pick([2, 3, 4]), d2 = r.pick([2, 3, 5]);
        if (ctx.intOnly) { g(F(1, d1), d1 * nz(r, -4, 4), d1 * nz(r, -4, 4)); g(F(-r.int(1, 2), d2), d2 * nz(r, -3, 3), d2 * nz(r, -3, 3)); }
        else { g(F(r.int(1, 3), d1), nz(r, -6, 6), nz(r, -8, 8)); g(F(-r.int(1, 3), d2), nz(r, -6, 6), nz(r, -8, 8)); }
        need(!groups[0].a.isInt() && !groups[1].a.isInt());
        variant = 'frac';
      } else {
        // nested: a[ b(x + p) - q ] - e(gx - f) + h
        var a = r.int(2, 4), b = r.int(2, 5), p = nz(r, -6, 6), q = r.int(1, 9), e = r.int(2, 6), gg = r.int(2, 5), f = nz(r, -8, 8), hh = nz(r, -9, 9);
        expr = a + '[' + grp(b, xb(p)) + '-' + q + ']' + '-' + grp(e, ax_b(gg, -f)) + addConst('', hh);
        var X = a * b - e * gg, C = a * (b * p - q) + e * f + hh;
        need(X !== 0);
        var ans7 = ax_b(X, C);
        steps.push(step('Distribute inside the brackets first.', a + '[' + ax_b(b, b * p - q) + ']' + '-' + grp(e, ax_b(gg, -f)) + addConst('', hh), 1));
        steps.push(step('Distribute the outside factors (the subtraction changes both signs).', lin([[a * b, 'x'], [a * (b * p - q), ''], [-e * gg, 'x'], [e * f, ''], [hh, '']]), 2));
        steps.push(step('Combine like terms.', ans7, 1));
        return { variant: 'nested', prompt: 'Simplify ' + M(expr) + '.', parts: [{ answer: M(ans7), check: { type: 'simplify', expr: expr, answer: ans7 } }], steps: steps, space: [1.2, 1.5, 1.8] };
      }
      if (groups[0].b.sign() < 0) { groups[0] = { a: groups[0].a.neg(), b: groups[0].b.neg(), k: groups[0].k.neg() }; }
      expr = groups.map(function (gr, i) { return signed(i === 0, gr.a, ax_b(gr.b, gr.k)); }).join('');
      expr = addConst(addX(expr, extraX), extraC);
      var X = Fr.of(extraX), C = Fr.of(extraC), expanded = [];
      groups.forEach(function (gr) { expanded.push([gr.a.mul(gr.b), 'x'], [gr.a.mul(gr.k), '']); X = X.add(gr.a.mul(gr.b)); C = C.add(gr.a.mul(gr.k)); });
      if (extraX) expanded.push([extraX, 'x']); if (extraC) expanded.push([extraC, '']);
      need(!X.isZero());
      if (c >= 6 && ctx.intOnly) need(X.isInt() && C.isInt());
      var ans = ax_b(X, C);
      if (groups.length === 1 && !extraX && !extraC) steps.push(step('Multiply ' + M(num(groups[0].a)) + ' by each term inside.', ans, 3));
      else { steps.push(step('Distribute.', lin(expanded), 2)); steps.push(step('Combine like terms.', ans, 2)); }
      return { variant: variant, prompt: 'Simplify ' + M(expr) + '.', parts: [{ answer: M(ans), check: { type: 'simplify', expr: expr, answer: ans } }], steps: steps, space: [0.9, 1.2, 1.5] };
    }
  });

  /* ============================================================
     SIMPLIFY · Evaluate expressions
     ============================================================ */
  skill({
    id: 'evaluate', best: [0, 1], tag: 'SIMPLIFY', name: 'Evaluate expressions',
    blurb: 'Positive inputs (CP2) → negatives, squares and two variables (CP1) → fraction bars and fraction inputs (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, expr, vals = {}, variant, a = r.int(2, 9), b = r.int(1, 12);
      if (c === 1) { vals.x = r.int(1, 9); expr = ax_b(a, b); variant = 'lin+'; }
      else if (c === 2) { vals.x = -r.int(1, 8); expr = r.chance(0.5) ? ax_b(a, -b) : lin([[b, ''], [-a, 'x']]); variant = 'lin-'; }
      else if (c === 3) {
        if (r.chance(0.5)) { vals.x = nz(r, -5, 5); expr = lin([[nz(r, -4, 4), 'x^2'], [nz(r, -6, 6), 'x'], [nz(r, -9, 9), '']]); variant = 'quad'; }
        else { vals.x = nz(r, -6, 6); vals.y = nz(r, -6, 6); expr = lin([[a, 'x'], [-r.int(2, 6), 'y'], [nz(r, -9, 9), '']]); variant = 'xy'; }
      } else if (c === 4) { vals.x = nz(r, -5, 5); vals.y = nz(r, -6, 6); expr = lin([[nz(r, -3, 3), 'x^2'], [nz(r, -5, 5), 'xy'], [nz(r, -6, 6), 'y']]); variant = 'x2y'; }
      else if (c === 5) {
        var dd = r.int(2, 5); vals.x = nz(r, -7, 7); vals.y = nz(r, -5, 5);
        expr = '\\frac{' + ax_b(a, nz(r, -9, 9)) + '}{' + dd + '}' + addX('', nz(r, -4, 4), 'y'); variant = 'fracbar';
      } else if (c === 6) {
        if (!ctx.intOnly && r.chance(0.5)) { vals.x = F(nz(r, -3, 3), r.pick([2, 3])); need(!vals.x.isInt()); expr = lin([[r.pick([4, 6, 12]), 'x^2'], [nz(r, -6, 6), 'x'], [nz(r, -5, 5), '']]); variant = 'fracin'; }
        else { vals.x = nz(r, -5, 5); vals.y = nz(r, -5, 5); expr = addConst('(' + lin([[1, 'x'], [-1, 'y']]) + ')^2' + addX('', nz(r, -4, 4), 'xy'), nz(r, -9, 9)); variant = 'sq'; }
      } else {
        vals.x = nz(r, -6, 6); vals.y = nz(r, -6, 6);
        expr = '\\frac{' + lin([[1, 'x^2'], [nz(r, -4, 4), 'y']]) + '}{' + lin([[1, 'x'], [1, 'y']]) + '}' + addX('', nz(r, -4, 4), 'x');
        variant = 'ratio';
      }
      // value with this package's own fractions (the checker recomputes independently)
      var env = vals, value = evalLocal(expr, env);
      need(value !== null);
      if (ctx.intOnly || c <= 5) need(value.isInt());
      need(Math.abs(value.val()) <= 400);
      var names = Object.keys(vals);
      var sub = expr;
      names.forEach(function (v) { sub = sub.replace(new RegExp(v, 'g'), '(' + num(vals[v]) + ')'); });
      var prompt = 'Evaluate ' + M(expr) + ' when ' + names.map(function (v) { return M(v + '=' + num(vals[v])); }).join(' and ') + '.';
      var valTeX = {}; names.forEach(function (v) { valTeX[v] = num(vals[v]); });
      return {
        variant: variant, prompt: prompt,
        parts: [{ answer: M(num(value)), check: { type: 'evaluate', expr: expr, values: valTeX } }],
        steps: [step('Substitute, using parentheses.', sub, 2), step('Follow the order of operations.', num(value), 3)],
        space: [0.9, 1.1, 1.3]
      };
    }
  });
  /* Tiny evaluator for the expression shapes built above (generator side only). */
  function evalLocal(expr, env) {
    try {
      var js = expr.replace(/\s+/g, '').replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, '(($1)/($2))')
        .replace(/\^(\d)/g, '^$1').replace(/(\d)([xy(])/g, '$1*$2').replace(/([xy)])([xy(])/g, '$1*$2').replace(/([xy)])([xy(])/g, '$1*$2');
      // exact evaluation by expanding with Fr
      return frEval(js, env);
    } catch (e) { return null; }
  }
  function frEval(s, env) {
    var i = 0;
    function peek() { return s[i]; }
    function expr() { var v = term(); while (peek() === '+' || peek() === '-') { var o = s[i++]; var w = term(); v = o === '+' ? v.add(w) : v.sub(w); } return v; }
    function term() { var v = unary(); while (peek() === '*' || peek() === '/') { var o = s[i++]; var w = unary(); v = o === '*' ? v.mul(w) : v.div(w); } return v; }
    function unary() { if (peek() === '-') { i++; return unary().neg(); } return pow(); }
    function pow() { var v = atom(); if (peek() === '^') { i++; var k = +s[i++]; var r = F(1); for (var j = 0; j < k; j++) r = r.mul(v); v = r; } return v; }
    function atom() {
      var ch = peek();
      if (ch === '(') { i++; var v = expr(); i++; return v; }
      if (/\d/.test(ch)) { var j = i; while (/\d/.test(s[j])) j++; var n = +s.slice(i, j); i = j; return F(n); }
      if (/[xy]/.test(ch)) { i++; return Fr.of(env[ch]); }
      throw new Error('bad ' + ch);
    }
    var v = expr(); if (i !== s.length) throw new Error('trailing'); return v;
  }

  /* ============================================================
     SOLVE · One- and two-step equations
     ============================================================ */
  skill({
    id: 'two-step', best: [0, 1], tag: 'SOLVE', name: 'Solve one- and two-step equations',
    blurb: 'One step with positives (CP2) → negatives and x/a (CP1) → fraction or decimal coefficients (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, x, e, steps = [], variant, a, b, k;
      if (c === 1) {
        x = r.int(1, 12); variant = r.pick(['add', 'sub', 'mul']);
        if (variant === 'add') { b = r.int(1, 15); e = eq(xb(b), String(x + b)); steps.push(step('Subtract ' + b + ' from both sides.', answerX('x', x), 2)); }
        else if (variant === 'sub') { b = r.int(1, 15); e = eq(xb(-b), String(x - b)); steps.push(step('Add ' + b + ' to both sides.', answerX('x', x), 2)); }
        else { a = r.int(2, 9); e = eq(a + 'x', String(a * x)); steps.push(step('Divide both sides by ' + a + '.', answerX('x', x), 2)); }
      } else if (c === 2) {
        x = r.int(1, 10); a = r.int(2, 9); b = nz(r, -15, 15); e = eq(ax_b(a, b), String(a * x + b)); variant = 'axb';
        finishLinear(steps, a, b, 0, a * x + b);
      } else if (c === 3) {
        x = nz(r, -10, 10);
        if (r.chance(0.5)) { a = nz(r, -9, 9); need(Math.abs(a) > 1); b = nz(r, -15, 15); e = eq(ax_b(a, b), String(a * x + b)); variant = 'neg'; finishLinear(steps, a, b, 0, a * x + b); }
        else { a = r.int(2, 6); k = nz(r, -8, 8); x = a * k; b = nz(r, -12, 12); e = eq('\\frac{x}{' + a + '}' + addConst('', b), String(k + b)); variant = 'xdiv';
          steps.push(step('Undo the constant.', eq('\\frac{x}{' + a + '}', String(k)), 1)); steps.push(step('Multiply both sides by ' + a + '.', answerX('x', x), 1)); }
      } else if (c === 4) {
        x = nz(r, -12, 12); a = r.int(2, 9); b = nz(r, -20, 20); variant = 'b-ax';
        e = eq(lin([[b, ''], [-a, 'x']]), String(b - a * x));
        steps.push(step('Subtract ' + num(b) + ' from both sides.', eq(lin([[-a, 'x']]), String(-a * x)), 1));
        steps.push(step('Divide both sides by ' + num(-a) + '.', answerX('x', x), 1));
      } else if (c === 5) {
        var d = r.int(2, 5), n = nz(r, -4, 4); need(gcd(Math.abs(n), d) === 1 && Math.abs(n) !== d);
        k = nz(r, -6, 6); x = d * k; b = nz(r, -12, 12); a = F(n, d); variant = 'fraccoef';
        e = eq(ax_b(a, b), num(a.mul(x).add(b)));
        steps.push(step('Undo the constant.', eq(lin([[a, 'x']]), num(a.mul(x))), 1));
        steps.push(step('Multiply both sides by ' + M(num(a.inv())) + '.', answerX('x', x), 2));
      } else {
        if (r.chance(0.5)) { // decimals: 0.4x - 1.2 = 3.6 (answer integer unless fractions allowed)
          var A10 = nz(r, -9, 9), B10 = nz(r, -40, 40); need(Math.abs(A10) > 1);
          x = wantsFraction(ctx) ? F(nz(r, -9, 9), 2) : F(nz(r, -12, 12));
          var R10 = Fr.of(A10).mul(x).add(B10); need(R10.isInt());
          e = eq(dec(A10) + 'x' + (B10 < 0 ? '-' : '+') + dec(Math.abs(B10)), dec(R10.n)); variant = 'decimal';
          steps.push(step('Multiply every term by 10.', eq(ax_b(A10, B10), num(R10)), 1));
          finishLinear(steps, A10, B10, 0, R10);
        } else {
          var dd = r.int(2, 6), nn = nz(r, -7, 7); need(gcd(Math.abs(nn), dd) === 1 && Math.abs(nn) > 1);
          a = F(nn, dd); x = wantsFraction(ctx) ? fracAnswer(ctx) : F(dd * nz(r, -5, 5)); b = nz(r, -15, 15);
          var rhs = a.mul(x).add(b); need(rhs.isInt());
          e = eq(ax_b(a, b), num(rhs)); variant = 'fraccoef2';
          steps.push(step('Undo the constant.', eq(lin([[a, 'x']]), num(rhs.sub(b))), 1));
          steps.push(step('Multiply both sides by ' + M(num(a.inv())) + '.', answerX('x', x), 2));
        }
      }
      return finishSolve(e, x, steps, variant, c);
    }
  });
  function finishSolve(e, x, steps, variant, c, v) {
    v = v || 'x';
    steps.unshift(step('', e, 0));
    steps.push(step('Check: substitute ' + M(answerX(v, x)) + ' into the original equation.', '', 1));
    return {
      variant: variant, prompt: 'Solve ' + M(e) + '.',
      parts: [{ answer: M(answerX(v, x)), check: solveSpec(e, v) }],
      steps: steps, space: [0.9 + 0.12 * c, 1.1 + 0.15 * c, 1.3 + 0.18 * c]
    };
  }

  /* ============================================================
     SOLVE · Multi-step equations (distribute and combine)
     ============================================================ */
  skill({
    id: 'multi-step', best: [1, 2], tag: 'SOLVE', name: 'Solve multi-step equations',
    blurb: 'a(x + b) = c (CP2) → distribute then combine like terms (CP1) → two groups, fraction factors, nested brackets (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], e, x = nz(r, -10, 10), variant, A, B, D;
      if (c <= 2) x = r.int(1, 10);
      if (c === 1) {
        var a = r.int(2, 8), b = nz(r, -9, 9); D = a * (x + b); e = eq(grp(a, xb(b)), String(D)); variant = 'a(x+b)';
        steps.push(step('Distribute.', eq(ax_b(a, a * b), String(D)), 1)); finishLinear(steps, a, a * b, 0, D);
      } else if (c === 2) {
        var a2 = r.int(2, 7), b2 = nz(r, -9, 9), k2 = nz(r, -12, 12); D = a2 * (x + b2) + k2;
        e = eq(addConst(grp(a2, xb(b2)), k2), String(D)); variant = 'a(x+b)+k';
        steps.push(step('Distribute.', eq(lin([[a2, 'x'], [a2 * b2, ''], [k2, '']]), String(D)), 1));
        steps.push(step('Combine like terms.', eq(ax_b(a2, a2 * b2 + k2), String(D)), 1)); finishLinear(steps, a2, a2 * b2 + k2, 0, D);
      } else if (c === 3 || c === 4) {
        var a3 = c === 3 ? r.int(2, 7) : -r.int(2, 7), b3 = nz(r, -9, 9), cx = nz(r, -8, 8); A = a3 + cx; need(A !== 0 && cx !== 0);
        D = a3 * (x + b3) + cx * x; e = eq(addX(grp(a3, xb(b3)), cx), String(D)); variant = c === 3 ? 'a(x+b)+cx' : '-a(x+b)+cx';
        steps.push(step('Distribute.', eq(lin([[a3, 'x'], [a3 * b3, ''], [cx, 'x']]), String(D)), 1));
        steps.push(step('Combine like terms.', eq(ax_b(A, a3 * b3), String(D)), 1)); finishLinear(steps, A, a3 * b3, 0, D);
      } else if (c === 5) {
        var p = r.int(2, 6), q = nz(r, -4, 4), s = nz(r, -9, 9), t = r.int(2, 6), u = nz(r, -4, 4), w = nz(r, -9, 9);
        A = p * q - t * u; need(A !== 0); B = p * s - t * w; D = A * x + B; need(Math.abs(D) <= 150);
        e = eq(grp(p, ax_b(q, s)) + '-' + grp(t, ax_b(u, w)), String(D)); variant = 'two-groups';
        steps.push(step('Distribute (the subtraction changes both signs in the second group).', eq(lin([[p * q, 'x'], [p * s, ''], [-t * u, 'x'], [-t * w, '']]), String(D)), 2));
        steps.push(step('Combine like terms.', eq(ax_b(A, B), String(D)), 1)); finishLinear(steps, A, B, 0, D);
      } else if (c === 6) {
        var d = r.pick([2, 3, 4]), mm = r.int(1, 3); need(gcd(mm, d) === 1);
        var fa = F(mm, d), ib = d * nz(r, -3, 3), ic = d * nz(r, -4, 4), kk = r.int(2, 5), jj = nz(r, -6, 6);
        A = fa.mul(ib).sub(kk); need(!A.isZero());
        var X = wantsFraction(ctx) ? fracAnswer(ctx) : F(x);
        B = fa.mul(ic).add(kk * jj); var R = A.mul(X).add(B); need(R.isInt() && Math.abs(R.val()) <= 120);
        e = eq(grp(fa, ax_b(ib, ic)) + '-' + grp(kk, xb(-jj)), num(R)); variant = 'frac-factor';
        steps.push(step('Distribute the fraction and the ' + kk + ' (the subtraction changes both signs).', eq(lin([[fa.mul(ib), 'x'], [fa.mul(ic), ''], [-kk, 'x'], [kk * jj, '']]), num(R)), 2));
        steps.push(step('Combine like terms.', eq(ax_b(A, B), num(R)), 1));
        finishLinear(steps, A, B, 0, R); x = X;
      } else {
        var o = r.int(2, 4), i1 = r.int(2, 4), p1 = nz(r, -6, 6), q1 = r.int(1, 9), k7 = r.int(2, 5), j7 = nz(r, -6, 6);
        A = o * i1 - k7; need(A !== 0); B = o * (i1 * p1 - q1) + k7 * j7;
        var X7 = wantsFraction(ctx) ? fracAnswer(ctx) : F(x); var R7 = Fr.of(A).mul(X7).add(B); need(R7.isInt() && Math.abs(R7.val()) <= 150);
        e = eq(o + '[' + grp(i1, xb(p1)) + '-' + q1 + ']-' + grp(k7, xb(-j7)), num(R7)); variant = 'nested';
        steps.push(step('Distribute inside the brackets.', eq(o + '[' + ax_b(i1, i1 * p1 - q1) + ']-' + grp(k7, xb(-j7)), num(R7)), 1));
        steps.push(step('Distribute the ' + o + ' and the ' + k7 + '.', eq(lin([[o * i1, 'x'], [o * (i1 * p1 - q1), ''], [-k7, 'x'], [k7 * j7, '']]), num(R7)), 2));
        steps.push(step('Combine like terms.', eq(ax_b(A, B), num(R7)), 1));
        finishLinear(steps, A, B, 0, R7); x = X7;
      }
      return finishSolve(e, x, steps, variant, c);
    }
  });

  /* ============================================================
     SOLVE · Variables on both sides
     ============================================================ */
  skill({
    id: 'both-sides', best: [1, 2], tag: 'SOLVE', name: 'Solve equations with variables on both sides',
    blurb: 'Positive coefficients (CP2) → distribution on one or both sides (CP1) → extra terms, fraction factors, fraction answers (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], e, variant, x = c <= 1 ? r.int(1, 10) : nz(r, -10, 10);
      var X = (c >= 7 && wantsFraction(ctx)) ? fracAnswer(ctx) : F(x);
      var L, Rr; // [coefX, const] after simplifying each side
      if (c === 1) {
        var a = r.int(3, 9), cc = r.int(1, a - 1), b = r.int(1, 12), d = b + (a - cc) * x;
        e = eq(ax_b(a, b), ax_b(cc, d)); variant = 'pos'; L = [a, b]; Rr = [cc, d];
      } else if (c === 2) {
        var a2 = nz(r, -9, 9), c2 = nz(r, -9, 9); need(a2 !== c2);
        var b2 = nz(r, -15, 15), d2 = b2 + (a2 - c2) * x; need(d2 !== 0);
        e = eq(ax_b(a2, b2), ax_b(c2, d2)); variant = 'neg'; L = [a2, b2]; Rr = [c2, d2];
      } else if (c === 3) {
        var a3 = nz(r, -6, 6), b3 = nz(r, -8, 8), c3 = nz(r, -9, 9); need(a3 !== c3 && Math.abs(a3) > 1);
        var d3 = a3 * (x + b3) - c3 * x; need(d3 !== 0);
        e = eq(grp(a3, xb(b3)), ax_b(c3, d3)); variant = 'dist-one';
        steps.push(step('Distribute.', eq(ax_b(a3, a3 * b3), ax_b(c3, d3)), 1)); L = [a3, a3 * b3]; Rr = [c3, d3];
      } else if (c === 4 || c === 5) {
        var a4 = nz(r, -7, 7), b4 = nz(r, -8, 8), c4 = nz(r, -7, 7), ex = c === 5 ? nz(r, -5, 5) : 0, fx = c === 5 ? nz(r, -9, 9) : 0;
        need(Math.abs(a4) > 1 && Math.abs(c4) > 1 && a4 + ex !== c4);
        // a(x+b) + ex = c(x+d) + f  -> choose d so that x is the solution
        var lhs = a4 * (x + b4) + ex * x, rest = lhs - c4 * x - fx; need(rest % c4 === 0);
        var d4 = rest / c4; need(d4 !== 0);
        e = eq(addX(grp(a4, xb(b4)), ex), addConst(grp(c4, xb(d4)), fx)); variant = c === 4 ? 'dist-both' : 'dist-both+';
        steps.push(step('Distribute on both sides.', eq(lin([[a4, 'x'], [a4 * b4, ''], [ex, 'x']]), lin([[c4, 'x'], [c4 * d4, ''], [fx, '']])), 2));
        if (ex || fx) steps.push(step('Combine like terms on each side.', eq(ax_b(a4 + ex, a4 * b4), ax_b(c4, c4 * d4 + fx)), 1));
        L = [a4 + ex, a4 * b4]; Rr = [c4, c4 * d4 + fx];
      } else if (c === 6) {
        var p = r.pick([2, 3]), q = r.pick([2, 3, 4]); need(p !== q);
        var u = nz(r, -3, 3) * p, w = nz(r, -4, 4) * p, s = nz(r, -3, 3) * q;
        var A6 = F(u, p), B6 = F(w, p), C6 = F(s, q); need(!A6.sub(C6).isZero());
        var t6 = A6.mul(x).add(B6).sub(C6.mul(x)).mul(q); need(t6.isInt() && !t6.isZero());
        e = eq(grp(F(1, p), ax_b(u, w)), grp(F(1, q), ax_b(s, t6))); variant = 'frac-both';
        steps.push(step('Distribute the fractions.', eq(ax_b(A6, B6), ax_b(C6, t6.div(q))), 2));
        L = [A6, B6]; Rr = [C6, t6.div(q)];
      } else {
        // a(x + b) - k = c(dx + e) + fx    (distribution on both sides and an extra x-term)
        var a7 = r.int(2, 6), b7 = nz(r, -6, 6), k7 = r.int(1, 9), c7 = nz(r, -5, 5), dx = r.int(2, 4), f7 = nz(r, -5, 5);
        need(Math.abs(c7) > 1);
        var Lx = a7, Lc = a7 * b7 - k7, Rx = c7 * dx + f7; need(Lx !== Rx);
        var e7 = Fr.of(Lx).mul(X).add(Lc).sub(Fr.of(Rx).mul(X)).div(c7); need(e7.isInt() && !e7.isZero());
        e = eq(addConst(grp(a7, xb(b7)), -k7), addX(grp(c7, ax_b(dx, e7)), f7)); variant = 'dist-both-extra';
        steps.push(step('Distribute on both sides.', eq(lin([[a7, 'x'], [a7 * b7, ''], [-k7, '']]), lin([[c7 * dx, 'x'], [e7.mul(c7), ''], [f7, 'x']])), 2));
        steps.push(step('Combine like terms on each side.', eq(ax_b(Lx, Lc), ax_b(Rx, e7.mul(c7))), 1));
        L = [Lx, Lc]; Rr = [Rx, e7.mul(c7)];
      }
      var sol = finishLinear(steps, L[0], L[1], Rr[0], Rr[1]);
      need(sol.eq(c >= 7 ? X : F(x)), 'solution mismatch');
      return finishSolve(e, sol, steps, variant, c);
    }
  });

  /* ============================================================
     SOLVE · Equations with fractions and decimals
     ============================================================ */
  skill({
    id: 'fraction-eq', best: [1, 2], tag: 'SOLVE', name: 'Solve equations with fractions or decimals',
    blurb: 'x/a = b (CP2) → (x + b)/a = c and decimals (CP1) → clearing an LCD, fractions on both sides (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], e, variant, x, a, b, k;
      if (c === 1) { a = r.int(2, 9); k = r.int(1, 10); x = a * k; e = eq('\\frac{x}{' + a + '}', String(k)); variant = 'x/a';
        steps.push(step('Multiply both sides by ' + a + '.', answerX('x', x), 2)); }
      else if (c === 2) { a = r.int(2, 8); k = nz(r, -9, 9); x = a * k; b = nz(r, -12, 12); e = eq('\\frac{x}{' + a + '}' + addConst('', b), String(k + b)); variant = 'x/a+b';
        steps.push(step('Undo the constant.', eq('\\frac{x}{' + a + '}', String(k)), 1)); steps.push(step('Multiply both sides by ' + a + '.', answerX('x', x), 1)); }
      else if (c === 3) { a = r.int(2, 8); k = nz(r, -9, 9); b = nz(r, -12, 12); x = a * k - b; e = eq('\\frac{' + xb(b) + '}{' + a + '}', String(k)); variant = '(x+b)/a';
        steps.push(step('Multiply both sides by ' + a + '.', eq(xb(b), String(a * k)), 1)); steps.push(step('Undo the constant.', answerX('x', x), 1)); }
      else if (c === 4) {
        var A10 = r.int(2, 9), B10 = nz(r, -50, 50); x = nz(r, -12, 12); var R10 = A10 * x + B10;
        e = eq(dec(A10) + 'x' + (B10 < 0 ? '-' : '+') + dec(Math.abs(B10)), dec(R10)); variant = 'decimal';
        steps.push(step('Multiply every term by 10.', eq(ax_b(A10, B10), String(R10)), 1)); finishLinear(steps, A10, B10, 0, R10);
      } else if (c === 5) {
        var p = r.pick([2, 3, 4, 5, 6]), q = r.pick([2, 3, 4, 5, 6]); need(p < q);
        var L = p * q / gcd(p, q); k = nz(r, -4, 4); x = L * k; var S = F(x, p).add(F(x, q)); need(S.isInt());
        e = eq('\\frac{x}{' + p + '}+\\frac{x}{' + q + '}', num(S)); variant = 'lcd';
        steps.push(step('Multiply every term by the LCD, ' + L + '.', eq(ax_b(L / p + L / q, 0), num(S.mul(L))), 2));
        finishLinear(steps, L / p + L / q, 0, 0, S.mul(L));
      } else if (c === 6) {
        // (x + a)/b = (x - c)/d   built from x and k = (x+a)/b
        var bb = r.int(2, 6), dd = r.int(2, 6); need(bb !== dd);
        x = nz(r, -12, 12); k = nz(r, -6, 6); var aa = k * bb - x, cc = x - dd * k; need(aa !== 0 && cc !== 0);
        e = eq('\\frac{' + xb(aa) + '}{' + bb + '}', '\\frac{' + xb(-cc) + '}{' + dd + '}'); variant = 'frac-both';
        steps.push(step('Cross-multiply.', eq(grp(dd, xb(aa)), grp(bb, xb(-cc))), 2));
        steps.push(step('Distribute.', eq(ax_b(dd, dd * aa), ax_b(bb, -bb * cc)), 1));
        finishLinear(steps, dd, dd * aa, bb, -bb * cc);
      } else {
        var c1 = r.pick([2, 3, 4]), f1 = r.pick([3, 4, 5, 6]); need(c1 !== f1);
        var a1 = r.int(1, 4), b1 = nz(r, -6, 6), d1 = r.int(1, 4), e1 = nz(r, -6, 6);
        var Lc = c1 * f1 / gcd(c1, f1), X = wantsFraction(ctx) ? fracAnswer(ctx) : F(nz(r, -10, 10));
        var val = Fr.of(a1).mul(X).add(b1).div(c1).sub(Fr.of(d1).mul(X).sub(e1).div(f1)); need(val.isInt());
        var A = F(a1 * Lc / c1 - d1 * Lc / f1); need(!A.isZero());
        e = eq('\\frac{' + ax_b(a1, b1) + '}{' + c1 + '}-\\frac{' + ax_b(d1, -e1) + '}{' + f1 + '}', num(val)); variant = 'lcd-groups';
        steps.push(step('Multiply every term by the LCD, ' + Lc + '.', eq(grp(Lc / c1, ax_b(a1, b1)) + '-' + grp(Lc / f1, ax_b(d1, -e1)), num(val.mul(Lc))), 2));
        var B = F(b1 * Lc / c1 + e1 * Lc / f1);
        steps.push(step('Distribute and combine like terms.', eq(ax_b(A, B), num(val.mul(Lc))), 1));
        x = finishLinear(steps, A, B, 0, val.mul(Lc)); need(x.eq(X));
      }
      return finishSolve(e, x, steps, variant, c);
    }
  });

  /* ============================================================
     SOLVE · One, none, or infinitely many solutions
     ============================================================ */
  skill({
    id: 'special-solutions', best: [1, 2], tag: 'SOLVE', name: 'One solution, no solution, or infinitely many',
    blurb: 'Already-simplified sides (CP2) → distribution on one side (CP1) → distribution and extra terms on both sides (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, outcome = r.pick(['none', 'none', 'all', 'all', 'one']);
      var P = nz(r, -7, 7), Q = nz(r, -12, 12), P2 = P, Q2 = Q, x = nz(r, -8, 8);
      if (outcome === 'none') { Q2 = Q + nz(r, -9, 9); }
      if (outcome === 'one') { P2 = nz(r, -7, 7); need(P2 !== P); Q2 = Q + (P - P2) * x; }
      var formL = Math.min(3, Math.max(0, c - 2 + r.int(0, 1))), formR = c <= 2 ? 0 : c <= 4 ? r.int(0, 1) : Math.min(3, c - 3);
      if (c <= 2) formL = r.int(0, 1) ? 0 : 0;
      var Lt = rep(r, P, Q, formL), Rt = rep(r, P2, Q2, formR);
      need(Lt.tex !== Rt.tex);
      var e = eq(Lt.tex, Rt.tex), steps = [step('', e, 0)];
      if (formL || formR) steps.push(step('Simplify each side.', eq(ax_b(P, Q), ax_b(P2, Q2)), 2));
      var ans, chk = { type: 'classify', eq: e, v: 'x' };
      if (outcome === 'none') { steps.push(step('Subtract ' + M(lin([[P, 'x']])) + ' from both sides.', eq(String(Q), String(Q2)), 1)); steps.push(step('That is false, so no value of x works.', '', 1)); ans = 'No solution'; }
      else if (outcome === 'all') { steps.push(step('Both sides are the same expression.', eq(String(Q), String(Q)), 1)); steps.push(step('That is always true, so every value of x works.', '', 1)); ans = 'Infinitely many solutions'; }
      else { var s = finishLinear(steps, P, Q, P2, Q2); need(s.eq(x)); ans = 'One solution: ' + M(answerX('x', x)); }
      return {
        variant: outcome + formL + formR,
        prompt: 'Does ' + M(e) + ' have one solution, no solution, or infinitely many solutions? If it has one solution, find it.',
        parts: [{ answer: ans, check: chk }], steps: steps, space: [1.0, 1.3, 1.6]
      };
    }
  });
  /* write P·x + Q in a given form: 0 plain · 1 k(x+m)+r · 2 k(x+m)+jx+r · 3 two groups */
  function rep(r, P, Q, form) {
    if (form === 0) return { tex: r.chance(0.5) || P < 0 ? ax_b(P, Q) : lin([[Q, ''], [P, 'x']]) };
    if (form === 1) { need(Math.abs(P) > 1); var m = nz(r, -6, 6), rr = Q - P * m; return { tex: addConst(grp(P, xb(m)), rr) }; }
    if (form === 2) { var k = nz(r, -6, 6), j = P - k; need(j !== 0 && Math.abs(k) > 1); var m2 = nz(r, -6, 6), r2 = Q - k * m2; return { tex: addConst(addX(grp(k, xb(m2)), j), r2) }; }
    for (var tries = 0; tries < 40; tries++) {
      var k2 = r.pick([-4, -3, -2, 2, 3, 4]), u = nz(r, -3, 3), k1 = P - k2 * u;
      if (Math.abs(k1) < 2) continue;
      var m1 = nz(r, -6, 6), rest = Q - k1 * m1;
      if (rest === 0 || rest % k2 !== 0) continue;
      var m3 = rest / k2; if (u < 0) { k2 = -k2; u = -u; m3 = -m3; }
      return { tex: grp(k1, xb(m1)) + signed(false, k2, ax_b(u, m3)) };
    }
    need(false, 'two-group form');
  }

  /* ============================================================
     SOLVE · Proportions
     ============================================================ */
  skill({
    id: 'proportion', best: [0, 1, 2], tag: 'SOLVE', name: 'Solve proportions',
    blurb: 'x/a = b/c (CP2) → variable in a denominator or a binomial (CP1) → binomials on both sides (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], e, variant, x, a, b, cc, d;
      function ratio() { var p, q; do { p = r.int(1, 9); q = r.int(2, 9); } while (p === q || p % q === 0); return [p, q]; }
      var pq = ratio(); b = pq[0]; cc = pq[1];
      if (c === 1) { var mult = r.int(1, 5); a = cc * mult; x = b * mult; e = eq('\\frac{x}{' + a + '}', '\\frac{' + b + '}{' + cc + '}'); variant = 'x/a';
        steps.push(step('Cross-multiply.', eq(cc + 'x', String(a * b)), 1)); steps.push(step('Divide both sides by ' + cc + '.', answerX('x', x), 1)); }
      else if (c === 2) { var m2 = r.int(1, 6); x = cc * m2; a = b * m2; e = eq('\\frac{' + a + '}{x}', '\\frac{' + b + '}{' + cc + '}'); variant = 'a/x';
        steps.push(step('Cross-multiply.', eq(b + 'x', String(a * cc)), 1)); steps.push(step('Divide both sides by ' + b + '.', answerX('x', x), 1)); }
      else if (c === 3) { var m3 = nz(r, -5, 5); d = cc * Math.abs(m3); var top = b * Math.abs(m3); a = nz(r, -9, 9); x = top - a; e = eq('\\frac{' + xb(a) + '}{' + d + '}', '\\frac{' + b + '}{' + cc + '}'); variant = '(x+a)/d';
        steps.push(step('Cross-multiply.', eq(grp(cc, xb(a)), String(d * b)), 1)); steps.push(step('Distribute.', eq(ax_b(cc, cc * a), String(d * b)), 1)); finishLinear(steps, cc, cc * a, 0, d * b); }
      else if (c === 4) { var m4 = r.int(1, 4); var den = cc * m4; a = b * m4; var off = nz(r, -9, 9); x = den - off; need(x !== -off);
        e = eq('\\frac{' + a + '}{' + xb(off) + '}', '\\frac{' + b + '}{' + cc + '}'); variant = 'a/(x+b)';
        steps.push(step('Cross-multiply.', eq(grp(b, xb(off)), String(a * cc)), 1)); steps.push(step('Distribute.', eq(ax_b(b, b * off), String(a * cc)), 1)); finishLinear(steps, b, b * off, 0, a * cc); }
      else {
        var lead = c === 5 ? 1 : r.int(2, 3), X = c === 7 && wantsFraction(ctx) ? fracAnswer(ctx) : F(nz(r, -12, 12));
        var bb = r.int(2, 7), dd = r.int(2, 7); need(bb !== dd);
        var k = nz(r, -6, 6), aa = Fr.of(k * bb).sub(X.mul(lead)); need(aa.isInt() && !aa.isZero());
        var ccc = X.sub(k * dd); need(ccc.isInt() && !ccc.isZero());
        if (c === 7) { // general: (lead x + aa)/bb = (x - ccc)/dd with the leading coefficient on the right too
          var lr = r.int(2, 3); ccc = X.mul(lr).sub(k * dd); need(ccc.isInt() && !ccc.isZero() && dd * lead !== bb * lr);
          e = eq('\\frac{' + ax_b(lead, aa) + '}{' + bb + '}', '\\frac{' + ax_b(lr, ccc.neg()) + '}{' + dd + '}');
          steps.push(step('Cross-multiply.', eq(grp(dd, ax_b(lead, aa)), grp(bb, ax_b(lr, ccc.neg()))), 2));
          steps.push(step('Distribute.', eq(ax_b(dd * lead, aa.mul(dd)), ax_b(bb * lr, ccc.neg().mul(bb))), 1));
          x = finishLinear(steps, dd * lead, aa.mul(dd), bb * lr, ccc.neg().mul(bb)); variant = 'general';
        } else {
          need(dd * lead !== bb);
          e = eq('\\frac{' + ax_b(lead, aa) + '}{' + bb + '}', '\\frac{' + xb(ccc.neg()) + '}{' + dd + '}');
          steps.push(step('Cross-multiply.', eq(grp(dd, ax_b(lead, aa)), grp(bb, xb(ccc.neg()))), 2));
          steps.push(step('Distribute.', eq(ax_b(dd * lead, aa.mul(dd)), ax_b(bb, ccc.neg().mul(bb))), 1));
          x = finishLinear(steps, dd * lead, aa.mul(dd), bb, ccc.neg().mul(bb)); variant = 'binomials' + lead;
        }
        need(Fr.of(x).eq(X));
      }
      return finishSolve(e, x, steps, variant, c);
    }
  });

  /* ============================================================
     LITERAL · Literal equations and formulas
     ============================================================ */
  var FORMULAS = [
    // [min c, formula TeX, solve-for, answer TeX, step text, numeric pick(rng) -> {values, target}]
    { c: 3, f: 'P=2l+2w', v: 'w', a: 'w=\\frac{P-2l}{2}', t: 'Subtract 2l, then divide by 2.', pick: function (r) { var l = r.int(4, 20), w = r.int(2, l); return { vals: { P: 2 * l + 2 * w, l: l }, ans: w }; } },
    { c: 3, f: 'd=rt', v: 't', a: 't=\\frac{d}{r}', t: 'Divide both sides by r.', pick: function (r) { var rr = r.pick([30, 40, 45, 50, 55, 60, 65]), t = r.int(2, 8); return { vals: { d: rr * t, r: rr }, ans: t }; } },
    { c: 3, f: 'V=lwh', v: 'h', a: 'h=\\frac{V}{lw}', t: 'Divide both sides by lw.', pick: function (r) { var l = r.int(2, 12), w = r.int(2, 10), h = r.int(2, 9); return { vals: { V: l * w * h, l: l, w: w }, ans: h }; } },
    { c: 3, f: 'y=mx+b', v: 'b', a: 'b=y-mx', t: 'Subtract mx from both sides.', pick: function (r) { var m = r.nonzero(-6, 6), x = r.nonzero(-6, 6), b = r.nonzero(-12, 12); return { vals: { y: m * x + b, m: m, x: x }, ans: b }; } },
    { c: 5, f: 'y=mx+b', v: 'x', a: 'x=\\frac{y-b}{m}', t: 'Subtract b, then divide by m.', pick: function (r) { var m = r.nonzero(-6, 6), x = r.nonzero(-8, 8), b = r.nonzero(-12, 12); if (Math.abs(m) === 1) m = 2; return { vals: { y: m * x + b, m: m, b: b }, ans: x }; } },
    { c: 5, f: 'A=\\frac{1}{2}bh', v: 'h', a: 'h=\\frac{2A}{b}', t: 'Multiply both sides by 2, then divide by b.', pick: function (r) { var b = r.int(3, 16), h = r.int(2, 14); if ((b * h) % 2) h++; return { vals: { A: b * h / 2, b: b }, ans: h }; } },
    { c: 5, f: 'P=2(l+w)', v: 'l', a: 'l=\\frac{P}{2}-w', t: 'Divide both sides by 2, then subtract w.', pick: function (r) { var l = r.int(5, 25), w = r.int(2, l); return { vals: { P: 2 * (l + w), w: w }, ans: l }; } },
    { c: 5, f: 'F=\\frac{9}{5}C+32', v: 'C', a: 'C=\\frac{5}{9}(F-32)', t: 'Subtract 32, then multiply by the reciprocal of 9/5.', pick: function (r) { var C = 5 * r.int(-4, 20); return { vals: { F: 9 * C / 5 + 32 }, ans: C }; } },
    { c: 6, f: 'A=\\frac{h(b+c)}{2}', v: 'b', a: 'b=\\frac{2A}{h}-c', t: 'Multiply by 2, divide by h, then subtract c.', pick: function (r) { var h = r.int(2, 10), b = r.int(2, 15), c = r.int(2, 15); if ((h * (b + c)) % 2) b++; return { vals: { A: h * (b + c) / 2, h: h, c: c }, ans: b }; } },
    { c: 6, f: 'I=Prt', v: 'r', a: 'r=\\frac{I}{Pt}', t: 'Divide both sides by Pt.', pick: function (r) { var P = 100 * r.int(2, 20), t = r.int(2, 6), rr = F(r.int(1, 9), 100); return { vals: { I: rr.mul(P * t).n, P: P, t: t }, ans: rr }; } },
    { c: 6, f: 'S=\\frac{n(a+L)}{2}', v: 'L', a: 'L=\\frac{2S}{n}-a', t: 'Multiply by 2, divide by n, then subtract a.', pick: function (r) { var n = r.int(4, 12), a = r.int(1, 9), L = a + r.int(5, 40); if ((n * (a + L)) % 2) L++; return { vals: { S: n * (a + L) / 2, n: n, a: a }, ans: L }; } }
  ];
  skill({
    id: 'literal', best: [0, 1, 2], tag: 'LITERAL', name: 'Solve literal equations and formulas',
    blurb: 'Solve for y with one move (CP2) → simple formulas, then dividing every term (CP1) → multi-step formulas, then using them (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], e, v, ans, variant, prompt;
      if (c <= 2) {
        var a = c === 1 ? r.int(2, 9) : nz(r, -9, 9), k = c === 1 ? r.int(2, 15) : nz(r, -15, 15), form = r.int(0, 2);
        v = 'y';
        if (form === 0) { e = eq(lin([[a, 'x'], [1, 'y']]), String(k)); ans = 'y=' + lin([[k, ''], [-a, 'x']]); steps.push(step('Subtract ' + M(lin([[a, 'x']])) + ' from both sides.', ans, 3)); }
        else if (form === 1) { e = eq(lin([[1, 'y'], [-a, 'x']]), String(k)); ans = 'y=' + lin([[a, 'x'], [k, '']]); steps.push(step('Add ' + M(lin([[a, 'x']])) + ' to both sides.', ans, 3)); }
        else { e = eq(lin([[a, 'x'], [-1, 'y']]), String(k)); ans = 'y=' + lin([[a, 'x'], [-k, '']]); steps.push(step('Subtract ' + M(lin([[a, 'x']])) + ', then multiply both sides by −1.', ans, 3)); need(c === 2); }
        variant = 'y' + form;
      } else if (c === 4) {
        var bq = r.int(2, 6) * r.sign(), aq = bq * nz(r, -4, 4), kq = bq * nz(r, -6, 6); v = 'y';
        if (!ctx.intOnly && r.chance(0.4)) { aq = nz(r, -9, 9); kq = nz(r, -12, 12); need(aq % bq !== 0); }
        e = eq(lin([[aq, 'x'], [bq, 'y']]), String(kq)); ans = 'y=' + lin([[F(-aq, bq), 'x'], [F(kq, bq), '']]);
        steps.push(step('Subtract ' + M(lin([[aq, 'x']])) + ' from both sides.', eq(lin([[bq, 'y']]), lin([[-aq, 'x'], [kq, '']])), 1));
        steps.push(step('Divide every term by ' + num(bq) + '.', ans, 2)); variant = 'ax+by';
      } else if ((c === 3 || c === 5 || c === 6) && r.chance(c === 3 ? 0.5 : 0.4)) {
        var pool = FORMULAS.filter(function (f) { return f.c <= c && f.c >= c - 1; }), fm = r.pick(pool);
        e = fm.f; v = fm.v; ans = fm.a; steps.push(step(fm.t, ans, 3)); variant = 'formula:' + fm.f;
      } else if (c === 3) {
        // k·a + m·b = c  for b   (three letters, numeric coefficients)
        var L4 = r.pick([['a', 'b', 'c'], ['p', 'q', 'r'], ['m', 'n', 'k'], ['x', 'y', 'z']]), k4 = nz(r, -9, 9), m4 = r.int(2, 9) * r.sign();
        e = eq(lin([[k4, L4[0]], [m4, L4[1]]]), L4[2]); v = L4[1];
        ans = m4 > 0 ? v + '=\\frac{' + lin([[1, L4[2]], [-k4, L4[0]]]) + '}{' + m4 + '}' : v + '=\\frac{' + lin([[k4, L4[0]], [-1, L4[2]]]) + '}{' + (-m4) + '}';
        steps.push(step('Subtract ' + M(lin([[k4, L4[0]]])) + ' from both sides.', eq(lin([[m4, v]]), lin([[1, L4[2]], [-k4, L4[0]]])), 1));
        steps.push(step('Divide both sides by ' + m4 + '.', ans, 2)); variant = 'letters4';
      } else if (c === 5) {
        // (x + a)/k = y  for x      or   k(m + n) = q  for m
        var k5 = r.int(2, 6), j5 = r.pick([1, 2, 3, -1, -2]), k1 = r.int(2, 5), L5 = r.pick([['x', 'a', 'y'], ['p', 'q', 'r'], ['m', 'n', 'k'], ['t', 's', 'd']]);
        if (r.chance(0.5)) {
          // (k1·x + j·a)/k = y  ->  x = (k·y − j·a)/k1
          var top = lin([[k1, L5[0]], [j5, L5[1]]]);
          e = eq('\\frac{' + top + '}{' + k5 + '}', L5[2]); v = L5[0];
          ans = v + '=\\frac{' + lin([[k5, L5[2]], [-j5, L5[1]]]) + '}{' + k1 + '}';
          steps.push(step('Multiply both sides by ' + k5 + '.', eq(top, k5 + L5[2]), 1));
          steps.push(step('Move ' + M(lin([[j5, L5[1]]])) + ' to the other side.', eq(lin([[k1, L5[0]]]), lin([[k5, L5[2]], [-j5, L5[1]]])), 1));
          steps.push(step('Divide by ' + k1 + '.', ans, 1)); variant = 'fracletter';
        } else {
          // k(x + j·a) + b = y  ->  x = (y − b)/k − j·a
          var inner = lin([[1, L5[0]], [j5, L5[1]]]), extra = r.pick(['b', 'c', 'h']);
          e = eq(grp(k5, inner) + '+' + extra, L5[2]); v = L5[0];
          ans = v + '=\\frac{' + lin([[1, L5[2]], [-1, extra]]) + '}{' + k5 + '}' + (j5 > 0 ? '-' : '+') + (Math.abs(j5) === 1 ? '' : Math.abs(j5)) + L5[1];
          steps.push(step('Subtract ' + M(extra) + ' from both sides.', eq(grp(k5, inner), lin([[1, L5[2]], [-1, extra]])), 1));
          steps.push(step('Divide both sides by ' + k5 + '.', eq(inner, '\\frac{' + lin([[1, L5[2]], [-1, extra]]) + '}{' + k5 + '}'), 1));
          steps.push(step('Move ' + M(lin([[j5, L5[1]]])) + ' to the other side.', ans, 1)); variant = 'groupletter';
        }
      } else if (c === 6) {
        if (r.chance(0.5)) {
          // Solve for x: p(x - a) = q(x + b)
          var p6 = r.int(2, 7), q6 = r.int(1, 7); need(p6 !== q6);
          e = eq(grp(p6, 'x-a'), grp(q6, 'x+b')); v = 'x';
          var co = p6 - q6, top6 = lin([[p6, 'a'], [q6, 'b']]);
          ans = co === 1 ? 'x=' + top6 : 'x=\\frac{' + top6 + '}{' + co + '}';
          steps.push(step('Distribute both sides.', eq(lin([[p6, 'x'], [-p6, 'a']]), lin([[q6, 'x'], [q6, 'b']])), 1));
          steps.push(step('Collect the x-terms on the left and the other terms on the right.', eq(lin([[co, 'x']]), top6), 1));
          if (co !== 1) steps.push(step('Divide by ' + co + '.', ans, 1));
          return { variant: 'letters6b', prompt: 'Solve ' + M(e) + ' for ' + M(v) + '.', parts: [{ answer: M(ans), check: { type: 'literal', eq: e, v: v } }], steps: steps, space: [1.1, 1.4, 1.7] };
        }
        // Solve for x: p(x - a) = q x + b   (letters a, b)
        var p = r.int(2, 9), q = r.int(1, 8); need(p !== q);
        e = eq(grp(p, 'x-a'), lin([[q, 'x'], [1, 'b']])); v = 'x';
        var coef = p - q; ans = coef === 1 ? 'x=' + lin([[p, 'a'], [1, 'b']]) : 'x=\\frac{' + lin([[p, 'a'], [1, 'b']]) + '}{' + coef + '}';
        steps.push(step('Distribute.', eq(lin([[p, 'x'], [-p, 'a']]), lin([[q, 'x'], [1, 'b']])), 1));
        steps.push(step('Collect the x-terms; move ' + M(lin([[-p, 'a']])) + ' to the other side.', eq(lin([[coef, 'x']]), lin([[p, 'a'], [1, 'b']])), 1));
        if (coef !== 1) steps.push(step('Divide by ' + coef + '.', ans, 1)); variant = 'letters';
      } else {
        // Chef's special: (a) rearrange a formula, (b) use it
        var fm7 = r.pick(FORMULAS.filter(function (f) { return f.c >= 5; })), pk = fm7.pick(r);
        need(!ctx.intOnly || Fr.of(pk.ans).isInt());
        var given = Object.keys(pk.vals).map(function (k2) { return k2 + '=' + num(pk.vals[k2]); }).join(',\\ ');
        var bAns = fm7.v + '=' + num(pk.ans);
        prompt = 'Use the formula ' + M(fm7.f) + '.';
        return {
          variant: 'formula2:' + fm7.f,
          prompt: prompt,
          parts: [
            { label: 'a', prompt: 'Solve the formula for ' + M(fm7.v) + '.', answer: M(fm7.a), check: { type: 'literal', eq: fm7.f, v: fm7.v } },
            { label: 'b', prompt: 'Find ' + M(fm7.v) + ' when ' + M(given) + '.', answer: M(bAns), check: { type: 'literal-eval', eq: fm7.f, v: fm7.v, given: given } }
          ],
          steps: [step('(a) ' + fm7.t, fm7.a, 4), step('(b) Substitute the given values into your formula.', bAns, 3), step('Check by substituting into the original formula.', '', 1)],
          space: [1.5, 1.9, 2.3]
        };
      }
      return {
        variant: variant, prompt: 'Solve ' + M(e) + ' for ' + M(v) + '.',
        parts: [{ answer: M(ans), check: { type: 'literal', eq: e, v: v } }], steps: steps, space: [0.9, 1.2, 1.5]
      };
    }
  });

  /* ============================================================
     MODEL · Write and solve equations from words
     ============================================================ */
  var PEOPLE = ['Maya', 'Jordan', 'Luis', 'Priya', 'Sam', 'Avery', 'Noah', 'Zoe', 'Elena', 'Marcus'];
  var JOBS = [['A plumber', 'visit fee', 'hour', 'hours', 'h'], ['A dog walker', 'sign-up fee', 'walk', 'walks', 'w'], ['A bike shop', 'rental fee', 'hour', 'hours', 'h'],
    ['A tutor', 'booking fee', 'session', 'sessions', 's'], ['A moving company', 'truck fee', 'hour', 'hours', 'h'], ['A photographer', 'setup fee', 'hour', 'hours', 'h']];
  var PLANS = [['Gym A', 'Gym B', 'joining fee', 'month', 'months', 'm'], ['Phone plan A', 'Phone plan B', 'activation fee', 'month', 'months', 'm'],
    ['Streaming service A', 'Streaming service B', 'sign-up fee', 'month', 'months', 'm'], ['Car-share A', 'Car-share B', 'membership fee', 'trip', 'trips', 't']];
  function money(n) { return '$' + n; }
  skill({
    id: 'model', best: [0, 1, 2], tag: 'MODEL', name: 'Write and solve equations from word problems',
    blurb: 'Fee + rate (CP2) → consecutive integers and perimeter (CP1) → comparing plans, multi-part comparisons (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [];
      if (c === 1 || (c === 2 && r.chance(0.5))) {
        var job = r.pick(JOBS), fee = 5 * r.int(2, 12), rate = c === 1 ? 5 * r.int(2, 10) : r.int(12, 48), n = r.int(2, 9), total = fee + rate * n, v = job[4];
        var eqn = eq(lin([[fee, ''], [rate, v]]), String(total));
        steps.push(step('Let ' + M(v) + ' = number of ' + job[3] + '. Write the equation.', eqn, 2));
        steps.push(step('Subtract ' + fee + ' from both sides.', eq(rate + v, String(total - fee)), 1));
        steps.push(step('Divide by ' + rate + '.', v + '=' + n, 1));
        return {
          variant: 'fee-rate:' + job[0],
          prompt: job[0] + ' charges a ' + money(fee) + ' ' + job[1] + ' plus ' + money(rate) + ' per ' + job[2] + '. A bill is ' + money(total) + '. Write an equation and solve it to find the number of ' + job[3] + ', ' + M(v) + '.',
          parts: [{ answer: M(eqn), check: { type: 'model-eq', scenario: 'fee-rate', v: v } },
                  { answer: M(v + '=' + n) + ' ' + job[3], check: { type: 'scenario', scenario: 'fee-rate', want: 'n' } }],
          steps: steps, space: [1.1, 1.4, 1.7]
        };
      }
      if (c === 2) {
        var who = r.pick(PEOPLE), start = 10 * r.int(15, 40), sp = 5 * r.int(2, 9), wk = r.int(3, 12), left = start - sp * wk;
        need(left > 0);
        var eq2 = eq(lin([[start, ''], [-sp, 'w']]), String(left));
        steps.push(step('Let ' + M('w') + ' = number of weeks. Write the equation.', eq2, 2));
        steps.push(step('Subtract ' + start + ' from both sides.', eq(lin([[-sp, 'w']]), String(left - start)), 1));
        steps.push(step('Divide by ' + (-sp) + '.', 'w=' + wk, 1));
        return {
          variant: 'spend',
          prompt: who + ' has ' + money(start) + ' saved and spends ' + money(sp) + ' each week. After how many weeks will ' + who + ' have ' + money(left) + ' left? Write and solve an equation.',
          parts: [{ answer: M(eq2), check: { type: 'model-eq', scenario: 'spend', v: 'w' } },
                  { answer: M('w=' + wk) + ' weeks', check: { type: 'scenario', scenario: 'spend', want: 'n' } }],
          steps: steps, space: [1.1, 1.4, 1.7]
        };
      }
      if (c === 5 || c === 7) {
        var pl = r.pick(PLANS), m = r.int(3, 12), r1 = r.int(8, 30), r2 = r1 - r.int(2, 9), f1 = 5 * r.int(1, 8);
        var f2 = f1 + (r1 - r2) * m; need(r2 > 1);
        var cost = f1 + r1 * m, vv = pl[5], eq3 = eq(lin([[f1, ''], [r1, vv]]), lin([[f2, ''], [r2, vv]]));
        steps.push(step('Let ' + M(vv) + ' = number of ' + pl[4] + '. Set the costs equal.', eq3, 2));
        steps.push(step('Subtract ' + M(r2 + vv) + ' and ' + f1 + ' from both sides.', eq((r1 - r2) + vv, String(f2 - f1)), 1));
        steps.push(step('Divide.', vv + '=' + m, 1));
        steps.push(step('Find the cost: ' + M(f1 + '+' + r1 + '(' + m + ')') + '.', '\\$' + cost, 1));
        var parts = [{ label: 'a', prompt: 'After how many ' + pl[4] + ' do the two plans cost the same?', answer: M(vv + '=' + m) + ' ' + pl[4], check: { type: 'scenario', scenario: 'two-plans', want: 'n' } },
                     { label: 'b', prompt: 'What is that cost?', answer: '$' + cost, check: { type: 'scenario', scenario: 'two-plans', want: 'cost' } }];
        var variant = 'two-plans';
        if (c === 7) {
          var N = m + r.int(2, 6), A = f1 + r1 * N, B = f2 + r2 * N; need(A !== B);
          parts.push({ label: 'c', prompt: 'For ' + N + ' ' + pl[4] + ', which plan costs less, and by how much?', answer: (A < B ? pl[0] : pl[1]) + ', by $' + Math.abs(A - B), check: { type: 'scenario', scenario: 'two-plans', want: 'compare', n: N } });
          steps.push(step('(c) Compare: ' + M(f1 + '+' + r1 + '(' + N + ')=' + A) + ' and ' + M(f2 + '+' + r2 + '(' + N + ')=' + B) + '.', '', 2)); variant = 'two-plans+';
        }
        return {
          variant: variant + ':' + pl[0],
          prompt: pl[0] + ' charges a ' + money(f1) + ' ' + pl[2] + ' plus ' + money(r1) + ' per ' + pl[3] + '. ' + pl[1] + ' charges a ' + money(f2) + ' ' + pl[2] + ' plus ' + money(r2) + ' per ' + pl[3] + '.',
          parts: parts, steps: steps, space: [1.6, 2.0, 2.4]
        };
      }
      if (c === 4 || c === 6) {
        var mult = r.int(2, 4), more = nz(r, -6, 9), w = r.int(3, 15), L = mult * w + more; need(L > w && L > 0);
        var P = 2 * L + 2 * w, unit = r.pick(['cm', 'in.', 'ft', 'm']);
        var rel = more > 0 ? Math.abs(more) + ' ' + unit + ' more than ' + mult + ' times its width' : Math.abs(more) + ' ' + unit + ' less than ' + mult + ' times its width';
        var eq4 = eq('2(' + lin([[mult, 'w'], [more, '']]) + ')+2w', String(P));
        steps.push(step('Let ' + M('w') + ' = width, so length = ' + M(lin([[mult, 'w'], [more, '']])) + '.', eq4, 2));
        steps.push(step('Distribute and combine.', eq(lin([[2 * mult + 2, 'w'], [2 * more, '']]), String(P)), 1));
        steps.push(step('Solve.', 'w=' + w, 1));
        steps.push(step('Length: ' + M(mult + '(' + w + ')' + (more < 0 ? '-' : '+') + Math.abs(more) + '=' + L) + '.', '', 1));
        var parts4 = [{ label: c === 6 ? 'a' : '', prompt: c === 6 ? 'Find the width and the length.' : '', answer: 'width ' + w + ' ' + unit + ', length ' + L + ' ' + unit, check: { type: 'scenario', scenario: 'perimeter', want: 'wl' } }];
        if (c === 6) {
          need(P % 4 === 0); var side = P / 4, sqA = side * side, recA = L * w; need(sqA !== recA);
          parts4.push({ label: 'b', prompt: 'A square has the same perimeter. Which shape has the greater area, and by how much?', answer: 'The square, by ' + (sqA - recA) + ' ' + unit + '²', check: { type: 'scenario', scenario: 'perimeter', want: 'square' } });
          steps.push(step('(b) Square side ' + M(P + '\\div 4=' + side) + '; areas ' + M(side + '^2=' + sqA) + ' and ' + M(L + '\\cdot' + w + '=' + recA) + '.', '', 3));
        }
        return {
          variant: 'perimeter' + c,
          prompt: 'The length of a rectangle is ' + rel + '. The perimeter is ' + P + ' ' + unit + '.' + (c === 6 ? '' : ' Write and solve an equation to find the width and the length.'),
          parts: parts4, steps: steps, space: [1.5, 1.9, 2.3]
        };
      }
      // c = 3: consecutive integers
      var count = r.pick([3, 3, 4]), kind = r.pick(['', 'even ', 'odd ']), gap = kind ? 2 : 1;
      var first = r.int(-20, 40); if (kind === 'even ') first = 2 * Math.round(first / 2); if (kind === 'odd ') first = 2 * Math.round(first / 2) + 1;
      var list = []; for (var i = 0; i < count; i++) list.push(first + gap * i);
      var S = list.reduce(function (s, t) { return s + t; }, 0), word = { 3: 'three', 4: 'four' }[count];
      var terms = []; for (var j = 0; j < count; j++) terms.push(j === 0 ? 'n' : '(n+' + gap * j + ')');
      var eq5 = eq(terms.join('+'), String(S)), off = gap * count * (count - 1) / 2;
      steps.push(step('Let ' + M('n') + ' be the smallest integer.', eq5, 2));
      steps.push(step('Combine like terms.', eq(lin([[count, 'n'], [off, '']]), String(S)), 1));
      steps.push(step('Solve.', 'n=' + first, 1));
      return {
        variant: 'consecutive' + count + kind,
        prompt: 'The sum of ' + word + ' consecutive ' + kind + 'integers is ' + S + '. Write and solve an equation to find the integers.',
        parts: [{ answer: list.join(', '), check: { type: 'scenario', scenario: 'consecutive', want: 'list' } }],
        steps: steps, space: [1.2, 1.5, 1.8]
      };
    }
  });

  var K = NS.kit;
  /* ============================================================
     SOLVE · Absolute value equations   (checked as solution sets by the inequality checker)
     ============================================================ */
  skill(NS.absEqSkill('SOLVE'));

  /* ============================================================
     SOLVE · Find and fix the mistake (equations)
     ============================================================ */
  /* plain text for the mistake explanation (the line number is what is checked) */
  function P(t) { return String(t).replace(/\\frac\{([^{}]*)\}\{([^{}]*)\}/g, '$1/$2').replace(/\s+/g, ' ').replace(/-/g, '−'); }
  var WHO = ['Alex', 'Jordan', 'Sam', 'Taylor', 'Riley', 'Casey', 'Morgan', 'Jamie', 'Avery', 'Quinn'];
  skill({
    id: 'eq-error', best: [1, 2], tag: 'SOLVE', name: 'Find and fix the mistake',
    blurb: 'A sign slip in a one- or two-step equation (CP2) → distributing to only one term, moving a term without changing its sign (CP1) → a negative times a group, clearing fractions, mistakes deep in longer work (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, who = r.pick(WHO), x = pickAnswer(ctx, -9, 9), orig, lines = [], why;
      if (c === 1) {
        var b = r.int(2, 15), R = x + b; need(R !== 0);
        orig = eq(xb(b), num(R)); lines.push(answerX('x', R + b)); why = 'added ' + b + ' to both sides instead of subtracting it';
      } else if (c === 2) {
        var a2 = r.int(2, 7) * r.sign(), b2 = nz(r, -15, 15), R2 = a2 * x + b2;
        orig = eq(ax_b(a2, b2), num(R2)); lines.push(eq(lin([[a2, 'x']]), num(R2 + b2))); lines.push(answerX('x', F(R2 + b2, a2)));
        why = (b2 > 0 ? 'added ' + b2 : 'subtracted ' + (-b2)) + ' on the right side instead of undoing it';
      } else if (c === 3) {
        var a3 = r.int(2, 6), b3 = nz(r, -9, 9), R3 = a3 * (x + b3); need(R3 !== 0);
        orig = eq(grp(a3, xb(b3)), num(R3)); lines.push(eq(ax_b(a3, b3), num(R3))); lines.push(eq(lin([[a3, 'x']]), num(R3 - b3))); lines.push(answerX('x', F(R3 - b3, a3)));
        why = 'multiplied only the ' + P('x') + ' by ' + a3 + ' when distributing (the ' + num(b3) + ' must be multiplied too)';
      } else if (c === 4) {
        var a4 = r.int(2, 9) * r.sign(), d4 = r.int(1, 7) * r.sign(), b4 = nz(r, -12, 12); need(a4 !== d4 && a4 + d4 !== 0);
        var e4 = (a4 - d4) * x + b4; need(e4 !== 0);
        orig = eq(ax_b(a4, b4), ax_b(d4, e4)); lines.push(eq(ax_b(a4 + d4, b4), num(e4))); lines.push(eq(lin([[a4 + d4, 'x']]), num(e4 - b4))); lines.push(answerX('x', F(e4 - b4, a4 + d4)));
        why = 'moved ' + P(lin([[d4, 'x']])) + ' to the left side without changing its sign';
      } else if (c === 5) {
        var p5 = r.int(2, 20), q5 = r.int(2, 6), d5 = nz(r, -8, 8), R5 = p5 - q5 * (x + d5);
        orig = eq(p5 + '-' + grp(q5, xb(d5)), num(R5));
        var wrongB = p5 + q5 * d5;   // wrote −q(x + d) as −qx + qd
        lines.push(eq(lin([[p5, ''], [-q5, 'x'], [q5 * d5, '']]), num(R5))); lines.push(eq(ax_b(-q5, wrongB), num(R5)));
        lines.push(eq(lin([[-q5, 'x']]), num(R5 - wrongB))); lines.push(answerX('x', F(R5 - wrongB, -q5)));
        why = 'distributed ' + P('-' + q5) + ' but did not change the sign of ' + P(num(d5)) + ' (it should be ' + P(num(-q5 * d5)) + ')';
      } else if (c === 6) {   // x on both sides; the negative group distributed with the wrong sign
        var p6 = r.int(2, 20), q6 = r.int(2, 6), d6 = nz(r, -8, 8), e6 = nz(r, -5, 5); need(-q6 - e6 !== 0);
        var R6 = p6 - q6 * (x + d6) - e6 * x, W6 = p6 + q6 * d6;
        orig = eq(p6 + '-' + grp(q6, xb(d6)), ax_b(e6, R6));
        lines.push(eq(lin([[p6, ''], [-q6, 'x'], [q6 * d6, '']]), ax_b(e6, R6))); lines.push(eq(ax_b(-q6, W6), ax_b(e6, R6)));
        lines.push(eq(lin([[-q6 - e6, 'x']]), num(R6 - W6))); lines.push(answerX('x', F(R6 - W6, -q6 - e6)));
        why = 'distributed ' + P('-' + q6) + ' but did not change the sign of ' + P(num(d6)) + ' (it should be ' + P(num(-q6 * d6)) + ')';
      } else {
        var a7 = r.int(2, 6), b7 = nz(r, -6, 6), c7 = r.int(2, 5), d7 = r.int(1, 7), e7 = nz(r, -4, 4);
        var A1 = a7 - c7, B1 = a7 * b7 + c7 * d7; need(A1 !== e7);
        var f7 = (A1 - e7) * x + B1; need(f7 !== 0);
        orig = eq(grp(a7, xb(b7)) + '-' + grp(c7, xb(-d7)), ax_b(e7, f7));
        var Bw7 = a7 * b7 - c7 * d7;
        lines.push(eq(lin([[a7, 'x'], [a7 * b7, ''], [-c7, 'x'], [-c7 * d7, '']]), ax_b(e7, f7)));
        lines.push(eq(ax_b(A1, Bw7), ax_b(e7, f7))); lines.push(eq(lin([[A1 - e7, 'x']]), num(f7 - Bw7))); lines.push(answerX('x', F(f7 - Bw7, A1 - e7)));
        why = 'distributed ' + P('-' + c7) + ' and wrote ' + P(num(-c7 * d7)) + ' instead of ' + P('+' + c7 * d7) + ' (a negative times a negative is positive)';
      }
      var C = NS.check, base = C.solutionSet(orig, 'x'), first = 0;
      need(base.length === 1);
      lines.forEach(function (ln, i) { if (!first && !C.setEqual(C.solutionSet(ln, 'x'), base)) first = i + 1; });
      need(first > 0);
      var X = base[0].lo; need(ctx.intOnly ? X.n % X.d === 0n : true);
      var xs = F(Number(X.n), Number(X.d)), st = [step('Line ' + first + ': ' + who + ' ' + why + '.', '', 3)];
      st.push(step('Correct solution:', answerX('x', xs), 3));
      return {
        variant: 'eq-error' + c, prompt: who + ' solved ' + M(orig) + ' like this:', work: lines,
        parts: [{ label: 'a', prompt: 'Which line has the first mistake? Explain what went wrong.', answer: 'Line ' + first + ': ' + who + ' ' + why + '.', check: { type: 'error-line', ineq: orig, lines: lines, v: 'x' } },
                { label: 'b', prompt: 'Solve the equation correctly.', answer: M(answerX('x', xs)), check: solveSpec(orig, 'x') }],
        steps: st, space: [1.3, 1.6, 1.9]
      };
    }
  });

  /* ============================================================
     MODEL · Percent problems (re-solved from the words and numbers printed)
     ============================================================ */
  var ITEMS_PCT = [['jacket', 'jackets'], ['video game', 'games'], ['pair of shoes', 'shoes'], ['bike', 'bikes'], ['backpack', 'backpacks'], ['headphones', 'headphones']];
  function cents(x) { var v = Math.round(x * 100); return '$' + (v % 100 === 0 ? String(v / 100) : (v / 100).toFixed(2)); }
  skill({
    id: 'percent', best: [0, 1, 2], tag: 'MODEL', name: 'Percent problems',
    blurb: 'A percent of a number, what percent, the whole (CP2) → percent change, discounts, simple interest (CP1) → discount then tax, finding the original price, two changes in a row (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], item = r.pick(ITEMS_PCT)[0], prompt, ans, sc;
      if (c === 1) {
        var p1 = r.pick([10, 20, 25, 50, 5, 30, 40, 75]), n1 = r.int(2, 30) * (100 / gcd(p1, 100)); need(n1 <= 400);
        var v1 = p1 * n1 / 100; prompt = 'What is ' + p1 + '% of ' + n1 + '?'; ans = M(String(v1)); sc = 'of';
        steps.push(step('Write the percent as a decimal and multiply.', (p1 / 100) + '\\times ' + n1 + '=' + v1, 3));
      } else if (c === 2) {
        var p2 = r.pick([5, 10, 15, 20, 25, 30, 40, 60, 75, 80]), w2 = r.int(2, 20) * (100 / gcd(p2, 100)); need(w2 <= 400);
        var part2 = p2 * w2 / 100; prompt = part2 + ' is what percent of ' + w2 + '?'; ans = p2 + '%'; sc = 'what-pct';
        steps.push(step('Divide the part by the whole.', '\\frac{' + part2 + '}{' + w2 + '}=' + (p2 / 100), 2), step('Write the decimal as a percent.', p2 + '\\%', 1));
      } else if (c === 3) {
        var p3 = r.pick([5, 10, 20, 25, 40, 60, 75, 15, 35]), w3 = r.int(2, 20) * (100 / gcd(p3, 100)); need(w3 <= 500);
        var part3 = p3 * w3 / 100; prompt = part3 + ' is ' + p3 + '% of what number?'; ans = M(String(w3)); sc = 'whole';
        steps.push(step('Write an equation.', part3 + '=' + (p3 / 100) + 'n', 2), step('Divide.', 'n=' + w3, 1));
      } else if (c === 4) {
        var o4 = r.int(2, 30) * r.pick([4, 5, 10, 20]), p4 = r.pick([10, 20, 25, 50, 5, 15, 40, 75]), up = r.chance(0.5);
        need(o4 * p4 % 100 === 0); var n4 = up ? o4 + o4 * p4 / 100 : o4 - o4 * p4 / 100;
        prompt = 'A club had ' + o4 + ' members last year and has ' + n4 + ' members this year. Find the percent change and say whether it is an increase or a decrease.';
        ans = p4 + '% ' + (up ? 'increase' : 'decrease'); sc = 'change';
        steps.push(step('Change = new − old.', String(n4 - o4), 1), step('Divide by the original amount.', '\\frac{' + Math.abs(n4 - o4) + '}{' + o4 + '}=' + (p4 / 100), 2), step('As a percent: ' + p4 + '% ' + (up ? 'increase' : 'decrease') + '.', '', 1));
      } else if (c === 5) {
        if (r.chance(0.5)) {
          var pr5 = r.int(4, 40) * 5, d5 = r.pick([10, 20, 25, 15, 30, 40]); need(pr5 * d5 % 100 === 0 || ctx.intOnly === false);
          var sale = pr5 * (100 - d5) / 100; prompt = 'A ' + item + ' costs ' + cents(pr5) + '. It is on sale for ' + d5 + '% off. What is the sale price?'; ans = cents(sale); sc = 'discount';
          steps.push(step('Discount = ' + d5 + '% of ' + cents(pr5) + '.', (d5 / 100) + '\\times ' + pr5 + '=' + (pr5 * d5 / 100), 2), step('Subtract from the price.', pr5 + '-' + (pr5 * d5 / 100) + '=' + sale, 1));
        } else {
          var P5 = r.int(2, 30) * 100, rr = r.pick([2, 3, 4, 5, 6]), t5 = r.int(2, 6), I5 = P5 * rr * t5 / 100;
          prompt = 'Maya puts ' + cents(P5) + ' in an account that earns ' + rr + '% simple interest per year. How much interest does she earn in ' + t5 + ' years?';
          ans = cents(I5); sc = 'interest'; steps.push(step('Use ⟨I=Prt⟩.', 'I=' + P5 + '(' + (rr / 100) + ')(' + t5 + ')=' + I5, 3));
        }
      } else if (c === 6) {
        if (r.chance(0.5)) {
          var pr6 = r.int(4, 30) * 10, d6 = r.pick([10, 20, 25, 30]), tx = r.pick([5, 6, 8, 10]); var s6 = pr6 * (100 - d6) / 100, tot = s6 * (100 + tx) / 100;
          need(Math.abs(tot * 100 - Math.round(tot * 100)) < 1e-9);
          prompt = 'A ' + item + ' costs ' + cents(pr6) + '. It is ' + d6 + '% off, and then ' + tx + '% sales tax is added to the sale price. What is the total cost?'; ans = cents(tot); sc = 'disc-tax';
          steps.push(step('Sale price: ' + cents(pr6) + ' × ' + ((100 - d6) / 100) + '.', String(s6), 2), step('Add the tax: × ' + ((100 + tx) / 100) + '.', String(tot), 2));
        } else {
          var o6 = r.int(4, 40) * 5, d66 = r.pick([10, 20, 25, 40, 50, 30]), s66 = o6 * (100 - d66) / 100; need(Math.abs(s66 - Math.round(s66 * 100) / 100) < 1e-9);
          prompt = 'After a ' + d66 + '% discount, a ' + item + ' costs ' + cents(s66) + '. What was the original price?'; ans = cents(o6); sc = 'original';
          steps.push(step('The sale price is ' + (100 - d66) + '% of the original.', s66 + '=' + ((100 - d66) / 100) + 'p', 2), step('Divide.', 'p=' + o6, 2));
        }
      } else {
        var o7 = r.int(2, 20) * 50, u7 = r.pick([10, 20, 25, 50]), d7 = r.pick([10, 20, 25, 40]); var m7 = o7 * (100 + u7) / 100, f7 = m7 * (100 - d7) / 100;
        need(Math.abs(f7 * 100 - Math.round(f7 * 100)) < 1e-9);
        prompt = 'A store raises the price of a ' + item + ' that cost ' + cents(o7) + ' by ' + u7 + '%. Later it lowers the new price by ' + d7 + '%. What is the final price, and is it more or less than the original?';
        ans = cents(f7) + ', ' + (f7 > o7 ? 'more' : f7 < o7 ? 'less' : 'the same as') + (f7 === o7 ? ' the original' : ' than the original'); sc = 'two-changes'; need(f7 !== o7);
        steps.push(step('Increase: ' + cents(o7) + ' × ' + ((100 + u7) / 100) + '.', String(m7), 2), step('Decrease: × ' + ((100 - d7) / 100) + '.', String(f7), 2), step('Compare with ' + cents(o7) + '.', '', 1));
      }
      return { variant: 'pct-' + sc, prompt: prompt, parts: [{ answer: ans, check: { type: 'percent', scenario: sc } }], steps: steps, space: [0.8, 1.0, 1.2] };
    }
  });

  /* ============================================================
     SIMPLIFY · Find and fix the mistake (expressions, for Unit 1)
     ============================================================ */
  skill({
    id: 'expr-error', best: [1, 2], tag: 'SIMPLIFY', name: 'Find and fix the mistake (expressions)',
    blurb: 'Combining unlike terms (CP2) → distributing to only one term, subtracting a group (CP1) → two groups, two variables, fractions (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, who = r.pick(WHO), orig, lines = [], why, fix;
      if (c === 1) {
        var a = r.int(2, 9), b = r.int(2, 12), d = r.int(2, 9);
        orig = a + 'x+' + b + '+' + d + 'x'; lines.push(lin([[a + d + b, 'x']]));
        why = 'added the constant ' + b + ' to the ' + P('x') + '-terms (only like terms combine)'; fix = ax_b(a + d, b);
      } else if (c === 2) {
        var a2 = r.int(2, 9), b2 = r.int(2, 9), e2 = r.int(2, 12);
        orig = grp(a2, xb(b2)) + '+' + e2; lines.push(lin([[a2, 'x'], [b2, ''], [e2, '']])); lines.push(ax_b(a2, b2 + e2));
        why = 'multiplied only the ' + P('x') + ' by ' + a2 + ' (the ' + b2 + ' must be multiplied too)'; fix = ax_b(a2, a2 * b2 + e2);
      } else if (c === 3 || c === 4) {
        var a3 = r.int(3, 9), q3 = r.int(2, 6), d3 = r.int(1, 9) * r.sign();
        orig = a3 + 'x-' + grp(q3, xb(d3)); lines.push(lin([[a3, 'x'], [-q3, 'x'], [q3 * d3, '']])); lines.push(ax_b(a3 - q3, q3 * d3));
        why = 'did not change the sign of ' + P(num(d3)) + ' when distributing ' + P('-' + q3) + ' (it should be ' + P(num(-q3 * d3)) + ')'; fix = ax_b(a3 - q3, -q3 * d3); need(a3 !== q3);
        if (c === 4) {
          var y1 = r.int(2, 8), y2 = r.int(2, 8), x1 = r.int(2, 9), x2 = r.int(1, 8); need(x1 !== x2);
          orig = lin([[x1, 'x'], [y1, 'y'], [-x2, 'x'], [y2, 'y']]); lines = [lin([[x1, 'x'], [-x2, 'x'], [y1, 'y'], [y2, 'y']]), lin([[x1 + x2, 'x'], [y1 + y2, 'y']])];
          why = 'added ' + P(lin([[x2, 'x']])) + ' instead of subtracting it'; fix = lin([[x1 - x2, 'x'], [y1 + y2, 'y']]);
        }
      } else if (c === 5 || c === 6) {
        var a5 = r.int(2, 5), b5 = nz(r, -7, 7), q5 = r.int(2, 5), d5 = nz(r, -7, 7);
        orig = grp(a5, xb(b5)) + '-' + grp(q5, xb(d5));
        lines.push(lin([[a5, 'x'], [a5 * b5, ''], [-q5, 'x'], [-q5 * d5, '']])); lines.push(ax_b(a5 - q5, a5 * b5 - q5 * d5));
        var wrongIdx = c === 5 ? 1 : 0; need(a5 !== q5); fix = ax_b(a5 - q5, a5 * b5 - q5 * d5);
        if (wrongIdx === 1) { lines[1] = ax_b(a5 + q5, a5 * b5 - q5 * d5); why = 'combined ' + P(a5 + 'x') + ' and ' + P('-' + q5 + 'x') + ' as ' + P((a5 + q5) + 'x') + ' (it should be ' + P(num(a5 - q5) + 'x') + ')'; need(a5 - q5 !== 0); }
        else { lines[0] = lin([[a5, 'x'], [a5 * b5, ''], [-q5, 'x'], [q5 * d5, '']]); lines[1] = ax_b(a5 - q5, a5 * b5 + q5 * d5); why = 'did not change the sign of ' + P(num(d5)) + ' when distributing ' + P('-' + q5); need(a5 - q5 !== 0); }
      } else {
        var h = r.pick([2, 3, 4]), u = r.int(1, 5) * h, w = nz(r, -4, 4) * h, k7 = r.int(1, 9);
        var g7 = r.int(2, 9);
        orig = '\\frac{1}{' + h + '}(' + ax_b(u, w) + ')-(x-' + k7 + ')+' + g7 + 'x';
        lines.push(lin([[u / h, 'x'], [w / h, ''], [-1, 'x'], [-k7, ''], [g7, 'x']])); lines.push(lin([[u / h - 1 + g7, 'x'], [w / h, ''], [-k7, '']])); lines.push(ax_b(u / h - 1 + g7, w / h - k7));
        why = 'subtracted the group but wrote ' + P('-' + k7) + ' instead of ' + P('+' + k7) + ' (subtracting a group changes every sign)'; need(u / h - 1 + g7 !== 0); fix = ax_b(u / h - 1 + g7, w / h + k7);
      }
      var C = NS.check, first = 0;
      lines.forEach(function (ln, i) { if (!first && !C.equivalent(orig, ln)) first = i + 1; });
      need(first > 0);
      need(C.equivalent(orig, fix));
      return {
        variant: 'expr-error' + c, prompt: who + ' simplified ' + M(orig) + ' like this:', work: lines,
        parts: [{ label: 'a', prompt: 'Which line has the first mistake? Explain what went wrong.', answer: 'Line ' + first + ': ' + who + ' ' + why + '.', check: { type: 'expr-error-line', expr: orig, lines: lines } },
                { label: 'b', prompt: 'Simplify the expression correctly.', answer: M(fix), check: { type: 'simplify', expr: orig } }],
        steps: [step('Line ' + first + ': ' + who + ' ' + why + '.', '', 3), step('Correct simplified form:', fix, 3)], space: [1.2, 1.5, 1.8]
      };
    }
  });

  /* ============================================================
     NUMBER · Classify real numbers   (the verifier classifies each printed number itself)
     ============================================================ */
  var SETNAMES = ['natural', 'whole', 'integer', 'rational', 'irrational', 'real'];
  /* a printed number and the sets it belongs to: {tex, sets:[…]} */
  function numObj(kind, r) {
    var t, s;
    if (kind === 'nat') { t = String(r.int(1, 40)); s = ['natural', 'whole', 'integer', 'rational', 'real']; }
    else if (kind === 'zero') { t = '0'; s = ['whole', 'integer', 'rational', 'real']; }
    else if (kind === 'negint') { t = String(-r.int(1, 30)); s = ['integer', 'rational', 'real']; }
    else if (kind === 'frac') { var d = r.int(2, 9), n = r.int(1, 20) * r.sign(); need(gcd(Math.abs(n), d) === 1); t = (n < 0 ? '-' : '') + '\\frac{' + Math.abs(n) + '}{' + d + '}'; s = ['rational', 'real']; }
    else if (kind === 'fracint') { var d2 = r.int(2, 6), q = r.int(2, 8) * r.sign(); t = (q < 0 ? '-' : '') + '\\frac{' + Math.abs(q * d2) + '}{' + d2 + '}'; s = q > 0 ? ['natural', 'whole', 'integer', 'rational', 'real'] : ['integer', 'rational', 'real']; }
    else if (kind === 'dec') { t = (r.chance(0.3) ? '-' : '') + r.int(0, 9) + '.' + r.pick(['25', '5', '75', '125', '4', '05', '36']); s = ['rational', 'real']; }
    else if (kind === 'rep') { t = (r.chance(0.3) ? '-' : '') + r.int(0, 9) + '.\\overline{' + r.pick(['3', '6', '1', '27', '45', '142857']) + '}'; s = ['rational', 'real']; }
    else if (kind === 'sqsq') { var k = r.int(2, 12); t = (r.chance(0.3) ? '-' : '') + '\\sqrt{' + k * k + '}'; s = t[0] === '-' ? ['integer', 'rational', 'real'] : ['natural', 'whole', 'integer', 'rational', 'real']; }
    else if (kind === 'sqrt') { var m = r.pick([2, 3, 5, 6, 7, 8, 10, 11, 12, 15, 20]); t = (r.chance(0.3) ? '-' : '') + '\\sqrt{' + m + '}'; s = ['irrational', 'real']; }
    else if (kind === 'pi') { t = r.pick(['\\pi', '2\\pi', '-\\pi', '\\frac{\\pi}{2}']); s = ['irrational', 'real']; }
    else { var a = r.int(1, 7), b = r.int(2, 9); need(gcd(a, b) === 1); t = '\\sqrt{\\frac{' + a * a + '}{' + b * b + '}}'; s = ['rational', 'real']; }
    return { tex: t, sets: s };
  }
  function setWords(s) { return s.map(function (w) { return w === 'integer' ? 'integer' : w; }).join(', '); }
  skill({
    id: 'real-numbers', best: [0, 1], tag: 'NUMBER', name: 'Classify real numbers',
    blurb: 'Natural, whole and integers (CP2) → fractions, decimals, repeating decimals and square roots (CP1) → numbers in disguise such as −12/4 and √(4/9), choosing the irrational numbers from a list (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [];
      var KINDS = [null, ['nat', 'zero', 'negint'], ['negint', 'frac'], ['dec', 'rep', 'frac'], ['sqsq', 'sqrt', 'rep'], ['fracint', 'sqfrac', 'pi', 'sqsq']];
      if (c <= 5) {
        var o = numObj(r.pick(KINDS[c]), r), ans = o.sets.map(function (w) { return w.charAt(0).toUpperCase() + w.slice(1); });
        steps.push(step(o.sets.indexOf('irrational') >= 0 ? 'It cannot be written as a fraction of integers (its decimal never ends or repeats): irrational.' : 'It can be written as a fraction of integers: rational.', '', 2));
        steps.push(step('Check each smaller set: natural (1, 2, 3, …), whole (0, 1, 2, …), integers (…, −1, 0, 1, …). Every number here is real.', '', 2));
        return { variant: 'rn' + c, prompt: 'Name every set the number ' + M(o.tex) + ' belongs to: natural, whole, integer, rational, irrational, real.', parts: [{ answer: ans.join(', '), check: { type: 'num-class', num: o.tex } }], steps: steps, space: [0.5, 0.6, 0.7] };
      }
      var want = c === 6 ? 'irrational' : r.pick(['integer', 'rational']), list = [], kinds = ['nat', 'negint', 'frac', 'fracint', 'dec', 'rep', 'sqsq', 'sqrt', 'pi', 'sqfrac'];
      r.shuffle(kinds).slice(0, 6).forEach(function (k) { list.push(numObj(k, r)); });
      var texs = list.map(function (o) { return o.tex; }); need(new Set(texs).size === 6);
      var yes = list.filter(function (o) { return o.sets.indexOf(want) >= 0 && (want !== 'rational' || o.sets.indexOf('integer') < 0); }); need(yes.length >= 1 && yes.length <= 4);
      var qw = want === 'rational' ? 'rational but NOT integers' : want === 'integer' ? 'integers' : 'irrational';
      steps.push(step('Rewrite each number in its simplest form first (for example ⟨\\sqrt{25}=5⟩, ⟨-\\frac{12}{4}=-3⟩).', '', 2), step('Then test each one.', '', 2));
      return { variant: 'rn-list-' + want, prompt: 'Which of these numbers are ' + qw + '? ' + texs.map(M).join(', '), parts: [{ answer: yes.map(function (o) { return M(o.tex); }).join(', '), check: { type: 'num-class', list: texs, want: want === 'rational' ? 'rational-not-integer' : want } }], steps: steps, space: [0.5, 0.6, 0.7] };
    }
  });

  /* ============================================================
     WORDS · Verbal phrases → expressions   (the verifier reads the English itself)
     ============================================================ */
  var NWORD = { 2: 'twice', 3: 'three times', 4: 'four times', 5: 'five times', 6: 'six times' };
  function vphrase(r, c, v) {   // returns [english, tex]
    var a = r.int(2, 12), b = r.int(2, 9), k = r.int(2, 6), V = 'a number ' + v;
    var simple = [['the sum of ' + V + ' and ' + a, v + '+' + a], [V + ' increased by ' + a, v + '+' + a], ['the product of ' + k + ' and ' + V, k + v],
      [a + ' more than ' + V, v + '+' + a]];
    var two = [[a + ' less than ' + V, v + '-' + a], ['the difference of ' + V + ' and ' + a, v + '-' + a], ['the quotient of ' + V + ' and ' + k, '\\frac{' + v + '}{' + k + '}'], [V + ' decreased by ' + a, v + '-' + a]];
    var ops = [[a + ' less than ' + NWORD[k] + ' ' + V, k + v + '-' + a], [a + ' more than ' + NWORD[k] + ' ' + V, k + v + '+' + a], [NWORD[k] + ' ' + V + ' decreased by ' + a, k + v + '-' + a], ['the quotient of ' + V + ' and ' + k + ', increased by ' + a, '\\frac{' + v + '}{' + k + '}+' + a]];
    var grp = [['the product of ' + k + ' and the sum of ' + V + ' and ' + a, k + '(' + v + '+' + a + ')'], [NWORD[k] + ' the difference of ' + V + ' and ' + a, k + '(' + v + '-' + a + ')'], ['the product of ' + k + ' and the difference of ' + V + ' and ' + a, k + '(' + v + '-' + a + ')']];
    var sq = [[a + ' less than the square of ' + V, v + '^2-' + a], ['the square of the sum of ' + V + ' and ' + b, '(' + v + '+' + b + ')^2'], ['the sum of the square of ' + V + ' and ' + a, v + '^2+' + a]];
    var twov = [['the sum of ' + NWORD[k] + ' x and ' + NWORD[b > 6 ? 3 : b] + ' y', k + 'x+' + (b > 6 ? 3 : b) + 'y'], ['the product of x and y, decreased by ' + a, 'xy-' + a], ['the quotient of x and the sum of y and ' + a, '\\frac{x}{y+' + a + '}']];
    var pool = c === 1 ? simple : c === 2 ? two : c === 3 ? ops : c === 4 ? grp : c === 5 ? sq : twov;
    return r.pick(pool);
  }
  skill({
    id: 'verbal', best: [0, 1], tag: 'WORDS', name: 'Write expressions from words',
    blurb: 'Sum, difference, product, quotient (CP2) → “less than”, two operations (CP1) → grouping, squares, two variables, and writing the words for an expression (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, v = r.pick(['n', 'x', 'm', 't']), steps = [];
      if (c === 6) v = 'n';
      var ph = vphrase(r, Math.min(c, 6), c >= 6 ? 'x' : v), eng = ph[0], tex = ph[1];
      if (c === 7) {   // write the words for an expression; the verifier reads the student's words
        var p7 = vphrase(r, r.int(3, 4), 'n');
        steps.push(step('Read the expression from the outside in: the last operation names the phrase.', '', 2), step('One correct phrase:', '', 2));
        return { variant: 'vb7', prompt: 'Write a verbal phrase for the expression ' + M(p7[1]) + '. Use “a number n” for the variable.', parts: [{ answer: p7[0].charAt(0).toUpperCase() + p7[0].slice(1) + '.', check: { type: 'verbal-words', expr: p7[1] } }], steps: steps, space: [0.5, 0.6, 0.7] };
      }
      steps.push(step('“' + (/less than/.test(eng) ? 'Less than' : /more than/.test(eng) ? 'More than' : 'The phrase') + '” tells you the order: write each part, then the operation.', tex, 3));
      return { variant: 'vb' + c, prompt: 'Write an algebraic expression for “' + eng + '”.', parts: [{ answer: M(tex), check: { type: 'verbal-expr' } }], steps: steps, space: [0.4, 0.5, 0.6] };
    }
  });

  /* ============================================================
     MODEL · Units and dimensional analysis
     ============================================================ */
  var CONV = [['feet', 'inches', 12], ['yards', 'feet', 3], ['miles', 'feet', 5280], ['meters', 'centimeters', 100], ['kilometers', 'meters', 1000], ['hours', 'minutes', 60], ['minutes', 'seconds', 60],
    ['gallons', 'quarts', 4], ['quarts', 'pints', 2], ['pints', 'cups', 2], ['pounds', 'ounces', 16], ['kilograms', 'grams', 1000]];
  var TWO = [['yards', 'inches'], ['gallons', 'cups'], ['hours', 'seconds'], ['miles', 'inches'], ['gallons', 'pints'], ['kilometers', 'centimeters']];
  function factor(from, to) {   // to-units per from-unit, by following the table
    var f = {}; CONV.forEach(function (c) { f[c[0] + '>' + c[1]] = c[2]; f[c[1] + '>' + c[0]] = 1 / c[2]; });
    if (f[from + '>' + to]) return f[from + '>' + to];
    var mids = Object.keys(f).filter(function (k) { return k.indexOf(from + '>') === 0; });
    for (var i = 0; i < mids.length; i++) { var mid = mids[i].split('>')[1]; if (f[mid + '>' + to]) return f[mids[i]] * f[mid + '>' + to];
      var m2 = Object.keys(f).filter(function (k) { return k.indexOf(mid + '>') === 0; }); for (var j = 0; j < m2.length; j++) { var mm = m2[j].split('>')[1]; if (mm !== from && f[mm + '>' + to]) return f[mids[i]] * f[m2[j]] * f[mm + '>' + to]; } }
    throw new WS.gen.Reject('no path');
  }
  function r1(x) { return Math.round(x * 10) / 10; }
  skill({
    id: 'units', best: [0, 1, 2], tag: 'MODEL', name: 'Units and dimensional analysis',
    blurb: 'One conversion factor (CP2) → two factors, rates such as miles per hour (CP1) → converting both units of a rate, square units (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], q, from, to, val, ans, prompt;
      if (c <= 2) { var cv = r.pick(CONV); from = c === 1 ? cv[0] : cv[1]; to = c === 1 ? cv[1] : cv[0]; q = c === 1 ? r.int(2, 15) : cv[2] * r.int(2, 12); val = q * factor(from, to);
        prompt = 'Convert ' + q + ' ' + from + ' to ' + to + '.'; ans = String(val) + ' ' + to;
        steps.push(step('Multiply by a conversion factor that cancels ' + from + '.', q + '\\cdot\\frac{' + (c === 1 ? cv[2] + '\\text{ ' + to + '}' : '1\\text{ ' + to + '}') + '}{' + (c === 1 ? '1\\text{ ' + from + '}' : cv[2] + '\\text{ ' + from + '}') + '}=' + val, 3)); }
      else if (c === 3) { var tw = r.pick(TWO); from = tw[0]; to = tw[1]; q = r.int(2, 9); val = q * factor(from, to); need(val <= 2000000);
        prompt = 'Convert ' + q + ' ' + from + ' to ' + to + '.'; ans = String(val) + ' ' + to; steps.push(step('Chain two conversion factors so the units cancel.', '', 2), step('Result: ' + val + ' ' + to + '.', '', 2)); }
      else if (c === 4) { var rate = r.int(2, 12) * 60, unit = r.pick(['miles', 'gallons', 'pages', 'meters']); val = rate / 60;
        prompt = 'A machine works at ' + rate + ' ' + unit + ' per hour. Convert this rate to ' + unit + ' per minute.'; ans = val + ' ' + unit + ' per minute';
        steps.push(step('Divide by 60 because 1 hour = 60 minutes.', '\\frac{' + rate + '}{60}=' + val, 3)); }
      else if (c === 5 || c === 6) { var mph = c === 5 ? r.int(10, 75) : r.int(20, 120), km = c === 6; val = km ? mph * 1000 / 3600 : mph * 5280 / 3600; need(Math.abs(val * 10 - Math.floor(val * 10) - 0.5) > 1e-6);
        prompt = 'Convert ' + mph + (km ? ' kilometers per hour to meters per second' : ' miles per hour to feet per second') + '. Round to the nearest tenth.'; ans = r1(val) + (km ? ' meters per second' : ' feet per second');
        steps.push(step('Change the distance unit (×' + (km ? 1000 : 5280) + ') and the time unit (÷3600).', mph + '\\cdot\\frac{' + (km ? 1000 : 5280) + '}{3600}\\approx ' + r1(val), 3)); }
      else { var sq = r.pick([['square feet', 'square inches', 144], ['square yards', 'square feet', 9], ['square meters', 'square centimeters', 10000]]); q = r.int(2, 30); val = q * sq[2];
        prompt = 'Convert ' + q + ' ' + sq[0] + ' to ' + sq[1] + '.'; ans = val + ' ' + sq[1];
        steps.push(step('A square unit converts by the factor twice (the factor squared): ' + Math.sqrt(sq[2]) + '² = ' + sq[2] + '.', q + '\\cdot ' + sq[2] + '=' + val, 3)); }
      return { variant: 'un' + c, prompt: prompt, parts: [{ answer: ans, check: { type: 'units' } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });


  // Lesson-specific aliases of independently verified generators; these remain selectable skills.
  (function(){var base=skills.find(function(s){return s.id==="both-sides";});if(!base)return;
    skill({id:"solve-equations-variables-both-sides",best:base.best,tag:base.tag,name:"Equations with variables on both sides",blurb:"Solve multi-step equations with variable terms on both sides.",
      difficultyProfile:'focused',fixedDifficulty:2,generate:function(ctx){return base.generate(Object.assign({},ctx,{c:2}));}});
  })();
  NS.registerSkillSet({
    id: 'algebra1-expressions-equations', course: 'algebra1', courseName: 'Algebra 1', unit: 'expressions-equations', unitName: 'Solving Linear Equations',
    title: 'The Equation Bistro',
    tags: { SIMPLIFY: 'Simplify & evaluate', DISTRIB: 'Distribute', SOLVE: 'Solve equations', LITERAL: 'Literal equations', MODEL: 'Model with equations', NUMBER: 'Real numbers', WORDS: 'Expressions from words' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Properties</h4><p>Distributive: ⟨a(b+c)=ab+ac⟩</p><p>Combine like terms: ⟨3x+5x=8x⟩, but ⟨3x+5y⟩ stays as it is.</p><p>Subtracting a group changes every sign: ⟨-(x-4)=-x+4⟩</p></section>' +
      '<section><h4>Solving an equation</h4><ol><li>Distribute and clear fractions (multiply by the LCD).</li><li>Combine like terms on each side.</li><li>Collect the variable on one side.</li><li>Undo addition/subtraction, then multiplication/division.</li><li>Check by substituting.</li></ol></section>' +
      '<section><h4>Special cases</h4><p>⟨5=7⟩ (false) → no solution.</p><p>⟨5=5⟩ (always true) → infinitely many solutions.</p></section>' +
      '<section><h4>Proportions</h4><p>If ⟨\\frac{a}{b}=\\frac{c}{d}⟩, then ⟨ad=bc⟩.</p></section>' +
      '<section><h4>Formulas</h4><p>Perimeter of a rectangle ⟨P=2l+2w⟩ · Area ⟨A=lw⟩</p><p>Triangle ⟨A=\\frac{1}{2}bh⟩ · Trapezoid ⟨A=\\frac{h(b+c)}{2}⟩</p><p>Distance ⟨d=rt⟩ · Simple interest ⟨I=Prt⟩</p><p>Temperature ⟨F=\\frac{9}{5}C+32⟩</p></section>' +
      '<section><h4>Words to equations</h4><p>“3 more than twice ⟨w⟩” → ⟨2w+3⟩</p><p>Consecutive integers: ⟨n,\\ n+1,\\ n+2⟩; consecutive even or odd: ⟨n,\\ n+2,\\ n+4⟩</p><p>Fee + rate: ⟨\\text{total}=\\text{fee}+\\text{rate}\\cdot n⟩</p></section></div>',
    gaps: [],
    skills: skills
  });

  /* Unit 1 · Foundations of Algebra: the simplify, distribute and evaluate skills on their own
     (the same generators and checks; Unit 2 keeps them for review). */
  NS.registerSkillSet({
    id: 'algebra1-foundations', course: 'algebra1', courseName: 'Algebra 1', unit: 'foundations-algebra', unitName: 'Foundations of Algebra',
    title: 'The Expression Café',
    tags: { SIMPLIFY: 'Simplify & evaluate', DISTRIB: 'Distribute', MODEL: 'Percent', NUMBER: 'Real numbers', WORDS: 'Expressions from words' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Order of operations</h4><p>Grouping symbols → exponents → multiply and divide (left to right) → add and subtract (left to right).</p></section>' +
      '<section><h4>Properties</h4><p>Distributive: ⟨a(b+c)=ab+ac⟩</p><p>Combine like terms: ⟨3x+5x=8x⟩, but ⟨3x+5y⟩ stays as it is.</p><p>Subtracting a group changes every sign: ⟨-(x-4)=-x+4⟩</p></section>' +
      '<section><h4>Evaluating</h4><p>Replace each variable with its value in parentheses: if ⟨x=-3⟩, then ⟨x^2=(-3)^2=9⟩.</p></section></div>',
    gaps: [
      'Naming properties (commutative, associative, identity) is not generated yet. Use Add → Write your own problem.'
    ],
    skills: skills.filter(function (s) { return ['like-terms', 'distribute', 'evaluate', 'expr-error', 'percent', 'real-numbers', 'verbal'].indexOf(s.id) >= 0; })
  });
})(typeof window !== 'undefined' ? window : globalThis);
