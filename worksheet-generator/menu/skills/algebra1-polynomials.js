/* Menu Assessment Generator — Algebra 1 · Unit 9 Polynomials (roadmap days 116–129).
   Skill groups: CLASSIFY (degree, terms, standard form), ADDSUB (adding and subtracting), MULT (multiplying),
   SPECIAL (special products), APPLY (dividing by a monomial, area, perimeter and volume expressions).
   The verifier checks every answer for equivalence with the printed expression (or the expression built from the
   printed side lengths) and for standard form: like terms combined, degrees from highest to lowest. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, M = K.M, num = K.num;
  var need = K.need, nz = K.nz, step = K.step;
  var skills = [];
  function skill(d) { skills.push(d); return d; }
  function vp(v, e) { return e === 0 ? '' : e === 1 ? v : v + '^{' + e + '}'; }
  /* polynomial = list of [coef, ex, ey]; printed in the given order (or standard order) with signs */
  function key(t) { return t[1] + ',' + (t[2] || 0); }
  function combine(ts) { var m = {}, order = []; ts.forEach(function (t) { var k = key(t); if (!(k in m)) { m[k] = 0; order.push(t); } m[k] += t[0]; }); return order.map(function (t) { return [m[key(t)], t[1], t[2] || 0]; }).filter(function (t) { return t[0] !== 0; }); }
  function stdSort(ts) { return ts.slice().sort(function (a, b) { return (b[1] + b[2]) - (a[1] + a[2]) || b[1] - a[1]; }); }
  function tex(ts, x, y) {
    x = x || 'x'; y = y || 'y'; if (!ts.length) return '0';
    return ts.map(function (t, i) {
      var c = t[0], body = vp(x, t[1]) + vp(y, t[2] || 0), a = Math.abs(c), s = (a === 1 && body ? '' : String(a)) + body;
      return i === 0 ? (c < 0 ? '-' : '') + s : (c < 0 ? '-' : '+') + s;
    }).join('');
  }
  function mul(A, B) { var out = []; A.forEach(function (a) { B.forEach(function (b) { out.push([a[0] * b[0], a[1] + b[1], (a[2] || 0) + (b[2] || 0)]); }); }); return stdSort(combine(out)); }
  function add(A, B, k) { return stdSort(combine(A.concat(B.map(function (b) { return [b[0] * (k === undefined ? 1 : k), b[1], b[2] || 0]; })))); }
  function P(t) { return '\\left(' + t + '\\right)'; }
  function lin(a, b, x) { return [[a, 1, 0], [b, 0, 0]].filter(function (t) { return t[0] !== 0; }); }
  function lin2(a, b) { return [[a, 1, 0], [b, 0, 1]]; }
  function randPoly(r, deg, n, lo, hi) {   // n distinct degrees ≤ deg including deg itself
    var ds = [deg], pool = []; for (var d = deg - 1; d >= 0; d--) pool.push(d); r.shuffle(pool).slice(0, n - 1).forEach(function (d) { ds.push(d); });
    return stdSort(ds.map(function (d) { return [nz(r, lo || -9, hi || 9), d, 0]; }));
  }
  var LET = ['x', 'a', 'm', 'n', 't', 'p', 'k', 'c'];
  var DEG = ['constant', 'linear', 'quadratic', 'cubic', 'quartic', 'quintic'], TERMS = [null, 'monomial', 'binomial', 'trinomial'];

  /* ================= CLASSIFY ================= */
  skill({
    id: 'poly-classify', best: [0, 1, 2], tag: 'CLASSIFY', name: 'Classify polynomials',
    blurb: 'Degree and number of terms (CP2) → names such as “cubic trinomial”, standard form and leading coefficient (CP1) → degree with two variables, the degree of a product, simplify then classify (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 2, 3, 4, 5, 7, 6][ctx.c], steps = [], x = r.pick(LET);
      if (c === 1 || c === 2 || c === 3) {
        var deg = r.int(c === 1 ? 2 : 1, c === 3 ? 5 : 4), n = r.int(1, Math.min(3, deg + 1)); if (c === 3 && r.chance(0.2)) n = 4; n = Math.min(n, deg + 1);
        var poly = randPoly(r, deg, n), shown = r.chance(c === 1 ? 0 : 0.5) ? r.shuffle(poly) : poly, e = tex(shown, x);
        if (c === 1) { steps.push(step('The degree is the largest exponent.', String(deg), 3));
          return { variant: 'cl1', prompt: 'What is the degree of ' + M(e) + '?', parts: [{ answer: M(String(deg)), check: { type: 'poly-classify', want: 'degree', expr: e } }], steps: steps, space: [0.4, 0.6, 0.8] }; }
        var tn = TERMS[n] || 'polynomial', dn = DEG[deg], name = (c === 3 ? dn + ' ' : '') + tn;
        steps.push(step('Count the terms: ' + n + '.', '', 2), step(c === 3 ? 'Highest exponent ' + deg + ': ' + dn + '.' : 'Name by number of terms.', '', 2));
        return { variant: 'cl' + c, prompt: (c === 2 ? 'Name ' + M(e) + ' by its number of terms (monomial, binomial, trinomial or polynomial).' : 'Name ' + M(e) + ' by its degree and its number of terms.'), parts: [{ answer: name.charAt(0).toUpperCase() + name.slice(1), check: c === 2 ? { type: 'poly-classify', want: 'name', expr: e, only: 'terms' } : { type: 'poly-classify', want: 'name', expr: e } }], steps: steps, space: [0.4, 0.6, 0.8] };
      }
      if (c === 4) { var p4 = randPoly(r, r.int(2, 5), r.int(3, 4)), sh = r.shuffle(p4); need(tex(sh, x) !== tex(p4, x)); var e4 = tex(sh, x);
        steps.push(step('Write the terms from the highest exponent to the lowest.', tex(p4, x), 2), step('The leading coefficient is the coefficient of the first term.', String(p4[0][0]), 2));
        return { variant: 'cl4', prompt: 'For ' + M(e4) + ':', parts: [{ label: 'a', prompt: 'Write it in standard form.', answer: M(tex(p4, x)), check: { type: 'poly-classify', want: 'standard', expr: e4 } },
          { label: 'b', prompt: 'What is the leading coefficient?', answer: M(String(p4[0][0])), check: { type: 'poly-classify', want: 'leading', expr: e4, v: x } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 5) { var ts = [], used = {}; for (var i = 0; i < r.int(2, 4); i++) { var a = r.int(0, 4), b = r.int(0, 4); if (used[a + ',' + b] || (a + b === 0 && i === 0)) continue; used[a + ',' + b] = 1; ts.push([nz(r, -9, 9), a, b]); }
        need(ts.length >= 2); var e5 = tex(ts, 'x', 'y'), deg5 = Math.max.apply(null, ts.map(function (t) { return t[1] + t[2]; })); need(deg5 >= 2);
        steps.push(step('The degree of a term is the sum of its exponents.', '', 2), step('The degree of the polynomial is the largest term degree.', String(deg5), 2));
        return { variant: 'cl5', prompt: 'What is the degree of ' + M(e5) + '?', parts: [{ answer: M(String(deg5)), check: { type: 'poly-classify', want: 'degree', expr: e5 } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 6) { var A = randPoly(r, r.int(2, 4), r.int(2, 3)), B = randPoly(r, A[0][1], r.int(2, 3)); if (r.chance(0.6)) B[0] = [A[0][0], A[0][1], 0];
        var sum = add(A, B, -1); need(sum.length >= 1); var e6 = P(tex(A, x)) + '-' + P(tex(B, x)), d6 = sum.length ? Math.max.apply(null, sum.map(function (t) { return t[1]; })) : 0;
        steps.push(step('Subtract: change the signs of the second polynomial and combine like terms.', tex(sum, x), 2), step('Find the degree of the result.', String(d6), 2));
        return { variant: 'cl6', prompt: 'Simplify ' + M(e6) + ', then give the degree of the result.', parts: [{ label: 'a', prompt: 'Simplify.', answer: M(tex(sum, x)), check: { type: 'poly-simplify', expr: e6 } }, { label: 'b', prompt: 'Degree of the result?', answer: M(String(d6)), check: { type: 'poly-classify', want: 'degree', expr: e6 } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      var F1 = randPoly(r, r.int(2, 4), 2, -6, 6), F2 = randPoly(r, r.int(1, 3), 2, -6, 6), e7 = P(tex(F1, x)) + P(tex(F2, x)), d7 = F1[0][1] + F2[0][1];
      steps.push(step('The leading terms multiply to give the highest power.', vp(x, F1[0][1]) + '\\cdot ' + vp(x, F2[0][1]) + '=' + vp(x, d7), 3));
      return { variant: 'cl7', prompt: 'Without multiplying it out, what is the degree of ' + M(e7) + '?', parts: [{ answer: M(String(d7)), check: { type: 'poly-classify', want: 'degree', expr: e7 } }], steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= ADDSUB ================= */
  skill({
    id: 'poly-addsub', best: [0, 1, 2], tag: 'ADDSUB', name: 'Add and subtract polynomials',
    blurb: 'Add, subtract (CP2) → missing terms, terms out of order, three polynomials (CP1) → two variables, multiples of polynomials (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], x = r.pick(LET), A, B, Cc, e, res;
      if (c <= 4) { var d = c <= 2 ? 2 : r.int(3, 4); A = randPoly(r, d, c <= 2 ? 3 : r.int(3, 4), c === 1 ? 1 : -9, 9); B = randPoly(r, c <= 2 ? 2 : r.int(2, d), 3, c === 1 ? -5 : -9, c === 1 ? 5 : 9); var sub = c === 2 || c === 4 || (c === 3 && r.chance(0.5));
        res = add(A, B, sub ? -1 : 1); need(res.length >= 2);
        var sA = c === 4 ? r.shuffle(A) : A, sB = c === 4 ? r.shuffle(B) : B; e = P(tex(sA, x)) + (sub ? '-' : '+') + P(tex(sB, x));
        steps.push(step(sub ? 'Distribute the minus sign to every term of the second polynomial.' : 'Remove the parentheses.', '', sub ? 2 : 1), step('Combine like terms and write in standard form.', tex(res, x), 2)); }
      else if (c === 5) { A = randPoly(r, 2, 3); B = randPoly(r, 2, r.int(2, 3)); Cc = randPoly(r, r.int(1, 2), 2); var s1 = r.chance(0.5);
        res = add(add(A, B, s1 ? -1 : 1), Cc, 1); need(res.length >= 2); e = P(tex(A, x)) + (s1 ? '-' : '+') + P(tex(B, x)) + '+' + P(tex(Cc, x));
        steps.push(step('Work left to right; distribute the minus sign.', '', 2), step('Combine like terms.', tex(res, x), 2)); }
      else if (c === 6) { var mk = function () { return stdSort(combine([[nz(r, -9, 9), 2, 0], [nz(r, -9, 9), 1, 1], [nz(r, -9, 9), 0, 2], [r.chance(0.5) ? nz(r, -9, 9) : 0, 1, 0]].filter(function (t) { return t[0]; }))); };
        A = mk(); B = mk(); res = add(A, B, -1); need(res.length >= 2); e = P(tex(A, 'x', 'y')) + '-' + P(tex(B, 'x', 'y')); x = 'x';
        steps.push(step('Distribute the minus sign.', '', 2), step('Combine like terms (same variables with the same exponents).', tex(res, 'x', 'y'), 2));
        return { variant: 'as6', prompt: 'Simplify ' + M(e) + '.', parts: [{ answer: M(tex(res, 'x', 'y')), check: { type: 'poly-simplify', expr: e } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      else if (r.chance(0.5)) { var q1 = r.int(2, 4), q2 = r.int(2, 4), mk2 = function () { return stdSort(combine([[nz(r, -6, 6), 2, 0], [nz(r, -6, 6), 1, 1], [nz(r, -6, 6), 0, 2]])); }; A = mk2(); B = mk2();
        res = add(A.map(function (t) { return [t[0] * q1, t[1], t[2]]; }), B.map(function (t) { return [t[0] * q2, t[1], t[2]]; }), -1); need(res.length >= 2); e = q1 + P(tex(A, 'x', 'y')) + '-' + q2 + P(tex(B, 'x', 'y'));
        steps.push(step('Distribute ' + q1 + ' and ' + M('-' + q2) + '.', '', 2), step('Combine like terms.', tex(res, 'x', 'y'), 2));
        return { variant: 'as7b', prompt: 'Simplify ' + M(e) + '.', parts: [{ answer: M(tex(res, 'x', 'y')), check: { type: 'poly-simplify', expr: e } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      else { var k1 = r.int(2, 4), k2 = r.int(2, 4); A = randPoly(r, 3, 4, -6, 6); B = randPoly(r, 3, r.int(3, 4), -6, 6);
        res = add(A.map(function (t) { return [t[0] * k1, t[1], 0]; }), B.map(function (t) { return [t[0] * k2, t[1], 0]; }), -1); need(res.length >= 2); e = k1 + P(tex(A, x)) + '-' + k2 + P(tex(B, x));
        steps.push(step('Distribute ' + k1 + ' and ' + M('-' + k2) + '.', tex(A.map(function (t) { return [t[0] * k1, t[1], 0]; }), x) + tex(B.map(function (t) { return [-t[0] * k2, t[1], 0]; }), x).replace(/^(?!-)/, '+'), 2), step('Combine like terms.', tex(res, x), 2)); }
      return { variant: 'as' + c, prompt: 'Simplify ' + M(e) + '. Write the answer in standard form.', parts: [{ answer: M(tex(res, x)), check: { type: 'poly-simplify', expr: e } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= MULT ================= */
  skill({
    id: 'poly-mult', best: [0, 1, 2], tag: 'MULT', name: 'Multiply polynomials',
    blurb: 'A monomial times a binomial, two binomials, a monomial times a trinomial (CP2) → leading coefficients other than 1, a binomial times a trinomial (CP1) → two variables, three binomials (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 3, 2, 4, 5, 6, 7][ctx.c], steps = [], x = r.pick(LET), y = 'y', A, B, res, e, two = false;
      if (c === 1 || c === 2) { var m = [[nz(r, c === 1 ? 2 : -6, 6), r.int(1, 3), 0]]; need(Math.abs(m[0][0]) > 1 || m[0][1] > 1); B = randPoly(r, r.int(1, 3), c === 1 ? 2 : 3, -8, 8); res = mul(m, B); e = tex(m, x) + P(tex(B, x));
        steps.push(step('Multiply the monomial by every term: multiply coefficients, add exponents.', tex(res, x), 3)); }
      else if (c === 3 || c === 4) { A = lin(c === 3 ? 1 : nz(r, -5, 5), nz(r, -9, 9)); B = lin(c === 3 ? 1 : nz(r, -5, 5), nz(r, -9, 9)); if (c === 4) need(Math.abs(A[0][0]) > 1 || Math.abs(B[0][0]) > 1); res = mul(A, B); need(res.length === 3); e = P(tex(A, x)) + P(tex(B, x));
        steps.push(step('Multiply each term of the first binomial by each term of the second (FOIL or a box).', '', 2), step('Combine the middle terms.', tex(res, x), 2)); }
      else if (c === 5) { A = lin(r.chance(0.5) ? 1 : nz(r, -4, 4), nz(r, -7, 7)); B = randPoly(r, 2, 3, -6, 6); res = mul(A, B); need(res.length >= 3); e = P(tex(A, x)) + P(tex(B, x));
        steps.push(step('Multiply each term of the binomial by every term of the trinomial (6 products).', '', 2), step('Combine like terms.', tex(res, x), 2)); }
      else if (c === 6) { two = true; A = lin2(nz(r, -5, 5), nz(r, -6, 6)); B = lin2(nz(r, -5, 5), nz(r, -6, 6)); res = mul(A, B); need(res.length === 3); e = P(tex(A, 'x', y)) + P(tex(B, 'x', y));
        steps.push(step('Multiply each term by each term.', '', 2), step('Combine the ' + M('xy') + '-terms.', tex(res, 'x', y), 2)); }
      else { A = lin(1, nz(r, -5, 5)); B = lin(1, nz(r, -5, 5)); var C3 = lin(r.chance(0.5) ? 1 : 2, nz(r, -5, 5)), AB = mul(A, B); res = mul(AB, C3); need(res.length >= 3); e = P(tex(A, x)) + P(tex(B, x)) + P(tex(C3, x));
        steps.push(step('Multiply the first two binomials.', tex(AB, x), 2), step('Multiply that trinomial by the third binomial and combine like terms.', tex(res, x), 2)); }
      var ans = two ? tex(res, 'x', y) : tex(res, x);
      return { variant: 'mu' + c, prompt: 'Multiply. Write the answer in standard form: ' + M(e) + '.', parts: [{ answer: M(ans), check: { type: 'poly-simplify', expr: e } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= SPECIAL ================= */
  skill({
    id: 'poly-special', best: [0, 1, 2], tag: 'SPECIAL', name: 'Special products',
    blurb: 'Square of a sum, square of a difference, sum times difference (CP2) → leading coefficients other than 1, squares with two variables (CP1) → sum times difference with two variables, differences of squares of binomials, a cube (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 3, 2, 4, 6, 5, 7][ctx.c], steps = [], x = r.pick(LET), a = r.int(1, 12), k = r.int(2, 7), e, res, rule;
      if (c === 1) { e = P(tex(lin(1, a), x)) + '^{2}'; res = mul(lin(1, a), lin(1, a)); rule = '(a+b)^{2}=a^{2}+2ab+b^{2}'; }
      else if (c === 2) { e = P(tex(lin(1, -a), x)) + P(tex(lin(1, a), x)); res = mul(lin(1, -a), lin(1, a)); rule = '(a-b)(a+b)=a^{2}-b^{2}'; }
      else if (c === 3) { e = P(tex(lin(1, -a), x)) + '^{2}'; res = mul(lin(1, -a), lin(1, -a)); rule = '(a-b)^{2}=a^{2}-2ab+b^{2}'; }
      else if (c === 4) { var s4 = r.pick([1, -1]); e = P(tex(lin(k, s4 * a), x)) + '^{2}'; res = mul(lin(k, s4 * a), lin(k, s4 * a)); rule = '(a\\pm b)^{2}=a^{2}\\pm 2ab+b^{2}'; }
      else if (c === 5) { var b5 = r.int(1, 7); e = P(tex(lin2(k, -b5), 'x', 'y')) + P(tex(lin2(k, b5), 'x', 'y')); res = mul(lin2(k, -b5), lin2(k, b5)); rule = '(a-b)(a+b)=a^{2}-b^{2}';
        steps.push(step('Use ' + M(rule) + '.', '', 1), step('Square each term.', tex(res, 'x', 'y'), 3));
        return { variant: 'sp5', prompt: 'Multiply: ' + M(e) + '.', parts: [{ answer: M(tex(res, 'x', 'y')), check: { type: 'poly-simplify', expr: e } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      else if (c === 6) { var b6 = nz(r, -7, 7); e = P(tex(lin2(k, b6), 'x', 'y')) + '^{2}'; res = mul(lin2(k, b6), lin2(k, b6)); rule = '(a+b)^{2}=a^{2}+2ab+b^{2}';
        steps.push(step('Use ' + M(rule) + ' with ' + M('a=' + k + 'x') + '.', '', 1), step('Square, double the product, square.', tex(res, 'x', 'y'), 3));
        return { variant: 'sp6', prompt: 'Multiply: ' + M(e) + '.', parts: [{ answer: M(tex(res, 'x', 'y')), check: { type: 'poly-simplify', expr: e } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      else if (r.chance(0.6)) { var b7 = r.int(1, 6), A7 = lin(r.int(2, 3), a), B7 = lin(1, -b7); e = P(tex(A7, x)) + '^{2}-' + P(tex(B7, x)) + '^{2}'; res = add(mul(A7, A7), mul(B7, B7), -1); need(res.length >= 1); rule = '(a+b)^{2}=a^{2}+2ab+b^{2}'; }
      else { var b8 = nz(r, -4, 4), L = lin(1, b8); e = P(tex(L, x)) + '^{3}'; res = mul(mul(L, L), L); rule = '(a+b)^{3}=(a+b)^{2}(a+b)'; }
      steps.push(step('Use the pattern ' + M(rule) + '.', '', 1), step('Expand and combine like terms.', tex(res, x), 3));
      return { variant: 'sp' + c, prompt: 'Multiply' + (c === 7 ? ' and simplify' : '') + ': ' + M(e) + '.', parts: [{ answer: M(tex(res, x)), check: { type: 'poly-simplify', expr: e } }], steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= APPLY ================= */
  skill({
    id: 'poly-apply', best: [0, 1, 2], tag: 'APPLY', name: 'Divide by a monomial; area and perimeter',
    blurb: 'Perimeter and area of a rectangle, divide a polynomial by a monomial (CP2) → shaded regions (CP1) → volume of a box, dividing with two variables (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 2, 3, 1, 5, 7, 6, 4][ctx.c], steps = [], x = r.pick(['x', 'x', 'n', 'w']);
      if (c === 1 || c === 4) {
        var m = c === 1 ? [[r.int(2, 6), r.int(1, 2), 0]] : [[nz(r, -6, 6), r.int(1, 2), r.int(0, 2)]], Q = c === 1 ? randPoly(r, r.int(1, 3), r.int(2, 3), -6, 6) : stdSort(combine([[nz(r, -6, 6), 2, 1], [nz(r, -6, 6), 1, 2], [nz(r, -6, 6), 1, 0]]));
        need(Math.abs(m[0][0]) > 1 || m[0][1] > 0); var Pn = mul(m, Q), e = '\\frac{' + (c === 1 ? tex(Pn, x) : tex(Pn, 'x', 'y')) + '}{' + (c === 1 ? tex(m, x) : tex(m, 'x', 'y')) + '}', ans = c === 1 ? tex(Q, x) : tex(Q, 'x', 'y');
        steps.push(step('Divide every term of the numerator by the monomial: divide coefficients, subtract exponents.', ans, 3));
        return { variant: 'ap' + c, prompt: 'Divide: ' + M(e) + '.', parts: [{ answer: M(ans), check: { type: 'poly-simplify', expr: e } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      var side = function () { return tex(lin(r.int(1, 4), nz(r, -6, 9)), x); };
      if (c === 2 || c === 3) { var L = side(), W = side(); need(L !== W);
        var res = c === 2 ? 'perimeter' : 'area', a2 = c === 2 ? add(add(lin(0, 0), parse(L)).map(dbl), parse(W).map(dbl), 1) : mul(parse(L), parse(W));
        steps.push(step(c === 2 ? 'Perimeter = 2(length) + 2(width).' : 'Area = length × width.', '', 1), step(c === 2 ? 'Combine like terms.' : 'Multiply the binomials and combine like terms.', tex(a2, x), 3));
        return { variant: 'ap' + c, prompt: 'A rectangle has length ' + M(L) + ' and width ' + M(W) + '. Write a polynomial in standard form for its ' + res + '.', parts: [{ answer: M(tex(a2, x)), check: { type: 'poly-apply', want: res, sides: [L, W] } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 5 || c === 7) { var ob1 = r.int(3, 9), ob2 = r.int(3, 9), oa = c === 7 ? r.pick([1, 2]) : 1, oL = tex(lin(oa, ob1), x), oW = c === 7 ? oL : tex(lin(1, ob2), x), ib1 = r.int(-2, Math.min(ob1, ob2) - 2), ib2 = nz(r, -2, Math.min(ob1, ob2) - 2), iL = tex(lin(1, ib1), x), iW = tex(lin(1, ib2), x); need((iL !== iW || c === 7) && (c === 7 || ob1 !== ob2));
        var outA = mul(parse(oL), parse(oW)), inA = mul(parse(iL), parse(iW)), sh = add(outA, inA, -1); need(sh.length >= 1);
        steps.push(step('Shaded area = outer area − inner area.', '', 1), step('Outer: ' + M(tex(outA, x)) + '. Inner: ' + M(tex(inA, x)) + '.', '', 2), step('Subtract and combine like terms.', tex(sh, x), 2));
        return { variant: 'ap' + c, prompt: (c === 7 ? 'A square with side ' + M(oL) : 'A rectangle with length ' + M(oL) + ' and width ' + M(oW)) + ' has a rectangular hole with length ' + M(iL) + ' and width ' + M(iW) + ' cut out of it. Write a polynomial in standard form for the area that is left.', parts: [{ answer: M(tex(sh, x)), check: c === 7 ? { type: 'poly-apply', want: 'shaded', square: true, sides: [oL, oL, iL, iW] } : { type: 'poly-apply', want: 'shaded', sides: [oL, oW, iL, iW] } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      var s1 = x, s2 = tex(lin(1, r.int(1, 5)), x), s3 = tex(lin(r.pick([1, 2]), nz(r, -4, 6)), x), vol = mul(mul(parse(s1), parse(s2)), parse(s3));
      steps.push(step('Volume = length × width × height.', '', 1), step('Multiply two factors, then the third; combine like terms.', tex(vol, x), 3));
      return { variant: 'ap6', prompt: 'A box has length ' + M(s1) + ', width ' + M(s2) + ' and height ' + M(s3) + '. Write a polynomial in standard form for its volume.', parts: [{ answer: M(tex(vol, x)), check: { type: 'poly-apply', want: 'volume', sides: [s1, s2, s3] } }], steps: steps, space: [0.7, 0.9, 1.1] };
      function dbl(t) { return [t[0] * 2, t[1], t[2]]; }
      function parse(s) {   // back from a printed binomial "ax+b" (generator side only)
        var m2 = /^(-?\d*)([a-z])([+-]\d+)?$/.exec(s); if (!m2) throw new Error('side ' + s);
        var co = m2[1] === '' ? 1 : m2[1] === '-' ? -1 : +m2[1]; return [[co, 1, 0]].concat(m2[3] ? [[+m2[3], 0, 0]] : []);
      }
    }
  });

  /* ================= DIVIDE · by a binomial ================= */
  function remTerm(rm, D) { return rm === 0 ? '' : (rm < 0 ? '-' : '+') + '\\frac{' + Math.abs(rm) + '}{' + tex(D) + '}'; }
  skill({
    id: 'poly-divide', print: ['maze', 'color', 'tarsia', 'error', 'who', 'stations'], best: [1, 2], tag: 'DIVIDE', name: 'Divide by a binomial',
    blurb: 'A quadratic divided by x + a with no remainder (CP2) → remainders, cubics, missing terms (CP1) → leading coefficients other than 1, divisors such as 2x − 1 (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [];
      var k = c === 7 ? r.int(2, 3) : 1, a = nz(r, c <= 1 ? 1 : -9, 9), D = [[k, 1, 0], [a, 0, 0]];
      var Q = c <= 3 ? [[c === 3 ? r.int(1, 3) : 1, 1, 0], [nz(r, -9, 9), 0, 0]] : [[c >= 6 ? r.int(2, 4) : 1, 2, 0], [r.int(-9, 9), 1, 0], [nz(r, -9, 9), 0, 0]];
      Q = Q.filter(function (t) { return t[0] !== 0; });
      var rem = c === 3 || c >= 6 ? nz(r, -12, 12) : 0;
      var Dv = add(mul(Q, D), rem ? [[rem, 0, 0]] : []);
      if (c === 5) need(Dv.length < 4);          // a missing term: the student must write a 0 placeholder
      if (c <= 2) need(Dv.length === 3);
      var expr = '\\frac{' + tex(Dv) + '}{' + tex(D) + '}', ans = tex(Q) + remTerm(rem, D);
      steps.push(step('Divide the leading terms to get the first term of the quotient' + (c === 5 ? ' (write ⟨0⟩ for the missing term).' : '.'), '', 1));
      steps.push(step('Multiply, subtract, bring down; repeat.', '', 2));
      steps.push(step(rem ? 'The remainder is ' + rem + '; write it over the divisor.' : 'The remainder is 0.', ans, 2));
      return { variant: 'pdiv' + c, prompt: 'Divide ' + M(expr) + '.' + (rem ? ' Write any remainder as a fraction.' : ''),
        parts: [{ answer: M(ans), check: { type: 'poly-divide', expr: expr } }], steps: steps, space: [1.3, 1.6, 1.9] };
    }
  });

  NS.registerSkillSet({
    id: 'algebra1-polynomials', course: 'algebra1', courseName: 'Algebra 1', unit: 'polynomials-factoring', unitName: 'Polynomials',
    title: 'The Polynomial Pizzeria',
    tags: { CLASSIFY: 'Classify polynomials', ADDSUB: 'Add and subtract', MULT: 'Multiply', SPECIAL: 'Special products', APPLY: 'Divide by a monomial; geometry', DIVIDE: 'Divide by a binomial' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Names</h4><p>Terms: monomial (1), binomial (2), trinomial (3). Degree: linear (1), quadratic (2), cubic (3), quartic (4), quintic (5).</p></section>' +
      '<section><h4>Standard form</h4><p>Combine like terms; write the terms from the highest degree to the lowest.</p></section>' +
      '<section><h4>Special products</h4><p>⟨(a+b)^{2}=a^{2}+2ab+b^{2}⟩, ⟨(a-b)^{2}=a^{2}-2ab+b^{2}⟩, ⟨(a+b)(a-b)=a^{2}-b^{2}⟩.</p></section>' +
      '<section><h4>Geometry</h4><p>Rectangle: ⟨P=2l+2w⟩, ⟨A=lw⟩. Box: ⟨V=lwh⟩.</p></section>' +
      '</div>',
    gaps: ['Factoring is in Unit 10.'],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
