/* Menu Assessment Generator — Algebra 1 · Unit 7 Exponents and Scientific Notation (roadmap days 91–103).
   Skill groups: PRODUCT (product and power rules), QUOTIENT (quotient rule, zero and negative exponents),
   EVAL (numerical powers, negative and rational exponents), SCI (scientific notation), SCIOPS (operations and contexts).
   The verifier checks that a simplified answer is equivalent to the printed expression and really simplified
   (positive exponents, each variable once, reduced numbers), and recomputes every scientific-notation value exactly. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, M = K.M, num = K.num, Fr = K.Fr;
  var need = K.need, nz = K.nz, step = K.step, F = K.F, gcd = K.gcd;
  var skills = [];
  function skill(d) { skills.push(d); return d; }
  var LETTERS = [['x', 'y'], ['a', 'b'], ['m', 'n'], ['p', 'q']];
  function letters(r) { return r.pick(LETTERS); }
  function vpow(v, e) { return e === 1 ? v : v + '^{' + e + '}'; }
  /* a monomial as printed in a problem: coefficient and variables with any exponents (shown as written) */
  function mono(c, vs) {
    var s = vs.filter(function (ve) { return ve[1] !== null; }).map(function (ve) { return vpow(ve[0], ve[1]); }).join('');
    if (!s) return num(c);
    return (c === 1 ? '' : c === -1 ? '-' : num(c)) + s;
  }
  /* the simplified answer for coefficient c (Fr) and net exponents {v: e} */
  function simp(c, ex, order) {
    c = Fr.of(c); var top = [], bot = [];
    order.forEach(function (v) { var e = ex[v] || 0; if (e > 0) top.push(vpow(v, e)); else if (e < 0) bot.push(vpow(v, -e)); });
    var n = Math.abs(c.n), d = c.d, sg = c.n < 0 ? '-' : '';
    if (!bot.length && d === 1) return sg + (n === 1 && top.length ? '' : String(n)) + top.join('');
    return sg + '\\frac{' + (n === 1 && top.length ? '' : String(n)) + top.join('') + '}{' + (d === 1 ? '' : String(d)) + bot.join('') + '}';
  }
  function paren(s) { return '\\left(' + s + '\\right)'; }

  /* ================= PRODUCT ================= */
  skill({
    id: 'pow-product', best: [0, 1, 2], tag: 'PRODUCT', name: 'Product and power rules',
    blurb: 'Multiply powers, a power of a power, coefficients (CP2) → a power of a product, products of monomials in two variables (CP1) → combined power and product rules, negative coefficients (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], L = letters(r), x = L[0], y = L[1], expr, cf, ex = {};
      if (c === 1) { var a = r.int(2, 9), b = r.int(2, 9); expr = vpow(x, a) + '\\cdot ' + vpow(x, b); cf = 1; ex[x] = a + b; steps.push(step('Same base: add the exponents.', vpow(x, a + b), 3)); }
      else if (c === 2) { var a2 = r.int(2, 6), b2 = r.int(2, 5); expr = paren(vpow(x, a2)) + '^{' + b2 + '}'; cf = 1; ex[x] = a2 * b2; steps.push(step('Power of a power: multiply the exponents.', vpow(x, a2 * b2), 3)); }
      else if (c === 3) { var c1 = r.int(2, 9) * (r.chance(0.3) ? -1 : 1), c2 = r.int(2, 9), a3 = r.int(1, 7), b3 = r.int(2, 7);
        expr = paren(mono(c1, [[x, a3]])) + paren(mono(c2, [[x, b3]])); cf = c1 * c2; ex[x] = a3 + b3;
        steps.push(step('Multiply the coefficients.', num(cf), 1), step('Add the exponents of ' + x + '.', simp(cf, ex, [x]), 2)); }
      else if (c === 4) { var k = r.int(2, 5) * (r.chance(0.3) ? -1 : 1), a4 = r.int(1, 5), b4 = r.int(1, 4), n = r.pick([2, 3]); need(Math.abs(Math.pow(k, n)) <= 125);
        expr = paren(mono(k, [[x, a4], [y, b4]])) + '^{' + n + '}'; cf = Math.pow(k, n); ex[x] = a4 * n; ex[y] = b4 * n;
        steps.push(step('Raise every factor to the power ' + n + '.', '', 1), step('Coefficient ' + num(k) + '^' + n + ' = ' + cf + '; multiply each exponent by ' + n + '.', simp(cf, ex, [x, y]), 2)); }
      else if (c === 5) { var p1 = nz(r, -6, 6), p2 = nz(r, -6, 6), e1 = r.int(1, 5), e2 = r.int(1, 4), e3 = r.int(1, 5), e4 = r.int(1, 4); need(Math.abs(p1) > 1 && Math.abs(p2) > 1);
        expr = paren(mono(p1, [[x, e1], [y, e2]])) + paren(mono(p2, [[x, e3], [y, e4]])); cf = p1 * p2; ex[x] = e1 + e3; ex[y] = e2 + e4;
        steps.push(step('Multiply the coefficients.', num(cf), 1), step('Add exponents with the same base.', simp(cf, ex, [x, y]), 2)); }
      else { var q1 = r.int(2, 4) * (c === 7 && r.chance(0.5) ? -1 : 1), m1 = r.int(1, 4), n1 = c === 7 ? 3 : r.pick([2, 3]), q2 = r.int(2, 5), m2 = r.int(1, 3), w2 = r.int(1, 3), n2 = 2, wy = c === 7 ? r.int(1, 3) : null;
        need(Math.abs(Math.pow(q1, n1) * Math.pow(q2, n2)) <= 2000);
        expr = paren(mono(q1, [[x, m1], [y, wy]])) + '^{' + n1 + '}' + paren(mono(q2, [[x, m2], [y, w2]])) + '^{' + n2 + '}';
        cf = Math.pow(q1, n1) * Math.pow(q2, n2); ex[x] = m1 * n1 + m2 * n2; ex[y] = (wy || 0) * n1 + w2 * n2;
        steps.push(step('Apply each power first.', mono(Math.pow(q1, n1), [[x, m1 * n1], [y, wy ? wy * n1 : null]]) + '\\cdot ' + mono(Math.pow(q2, n2), [[x, m2 * n2], [y, w2 * n2]]), 2), step('Multiply: coefficients, then add exponents.', simp(cf, ex, [x, y]), 2)); }
      return { variant: 'pp' + c, prompt: 'Simplify ' + M(expr) + '.', parts: [{ answer: M(simp(cf, ex, [x, y])), check: { type: 'pow-simplify', expr: expr } }], steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= QUOTIENT ================= */
  skill({
    id: 'pow-quotient', best: [0, 1, 2], tag: 'QUOTIENT', name: 'Quotient rule, zero and negative exponents',
    blurb: 'Divide powers, with coefficients (CP2) → zero and negative exponents, quotients that leave a fraction, two variables (CP1) → products with negative exponents, a negative power of a monomial (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], L = letters(r), x = L[0], y = L[1], expr, cf, ex = {};
      if (c === 1) { var b = r.int(2, 6), a = b + r.int(1, 7); expr = '\\frac{' + vpow(x, a) + '}{' + vpow(x, b) + '}'; cf = F(1); ex[x] = a - b; steps.push(step('Same base: subtract the exponents.', vpow(x, a - b), 3)); }
      else if (c === 2) { var d2 = r.int(2, 6), k2 = r.int(2, 8), b2 = r.int(1, 5), a2 = b2 + r.int(1, 6); expr = '\\frac{' + mono(d2 * k2, [[x, a2]]) + '}{' + mono(d2, [[x, b2]]) + '}'; cf = F(k2); ex[x] = a2 - b2;
        steps.push(step('Divide the coefficients and subtract the exponents.', simp(cf, ex, [x]), 3)); }
      else if (c === 3) { var k3 = r.pick([1, 2, 3, 5, 7]) * (r.chance(0.2) ? -1 : 1), a3 = r.int(2, 6), b3 = r.int(2, 5), zero = r.chance(0.5);
        expr = mono(k3, [[x, -a3], [y, zero ? 0 : b3]]); cf = F(k3); ex[x] = -a3; ex[y] = zero ? 0 : b3; need(k3 !== 1 || !zero);
        steps.push(step('A negative exponent moves the factor to the denominator' + (zero ? '; anything (nonzero) to the 0 power is 1.' : '.'), simp(cf, ex, [x, y]), 3)); }
      else if (c === 4) { var p = r.int(2, 9), q = r.int(2, 9); need(gcd(p, q) > 1 && p % q !== 0 && q % p !== 0); var a4 = r.int(1, 4), b4 = a4 + r.int(1, 5);
        expr = '\\frac{' + mono(p, [[x, a4]]) + '}{' + mono(q, [[x, b4]]) + '}'; cf = F(p, q); ex[x] = a4 - b4;
        steps.push(step('Reduce the coefficients.', num(cf), 1), step('Subtract exponents; a negative result goes to the denominator.', simp(cf, ex, [x]), 2)); }
      else if (c === 5) { var p5 = r.int(2, 12) * (r.chance(0.3) ? -1 : 1), q5 = r.int(2, 9), e = [r.int(1, 6), r.int(1, 6), r.int(1, 6), r.int(1, 6)]; need(e[0] !== e[2] && e[1] !== e[3] && (e[0] - e[2]) * (e[1] - e[3]) < 0);
        expr = '\\frac{' + mono(p5, [[x, e[0]], [y, e[1]]]) + '}{' + mono(q5, [[x, e[2]], [y, e[3]]]) + '}'; cf = F(p5, q5); ex[x] = e[0] - e[2]; ex[y] = e[1] - e[3];
        steps.push(step('Reduce the coefficients.', num(cf), 1), step('Subtract exponents for each variable; write negative ones in the denominator.', simp(cf, ex, [x, y]), 2)); }
      else if (c === 6) { var s1 = nz(r, -6, 6), s2 = r.int(2, 6), f = [r.int(-6, 6), r.int(-5, 5), r.int(-6, 6), r.int(-5, 5)]; need(f.every(function (z) { return z !== 0 && z !== 1; }) && f[0] + f[2] !== 0 && f[1] + f[3] !== 0 && (f[0] < 0 || f[2] < 0) && (f[1] < 0 || f[3] < 0) && (f[0] + f[2] < 0 || f[1] + f[3] < 0) && Math.abs(s1) > 1);
        expr = paren(mono(s1, [[x, f[0]], [y, f[1]]])) + paren(mono(s2, [[x, f[2]], [y, f[3]]])); cf = F(s1 * s2); ex[x] = f[0] + f[2]; ex[y] = f[1] + f[3];
        steps.push(step('Multiply the coefficients and add the exponents (negative exponents too).', mono(s1 * s2, [[x, ex[x]], [y, ex[y]]]), 2), step('Write with positive exponents.', simp(cf, ex, [x, y]), 2)); }
      else { var k7 = r.pick([2, 3, 4, 5]), a7 = r.int(-4, 4), b7 = r.int(-4, 4), n7 = r.pick([2, 3]); need(a7 !== 0 && b7 !== 0 && a7 !== 1 && b7 !== 1 && (a7 < 0 || b7 < 0) && Math.pow(k7, n7) <= 125);
        expr = paren(mono(k7, [[x, a7], [y, b7]])) + '^{-' + n7 + '}'; cf = F(1, Math.pow(k7, n7)); ex[x] = -a7 * n7; ex[y] = -b7 * n7;
        steps.push(step('Multiply every exponent by ' + M('-' + n7) + '.', mono(k7, [[x, null]]) + '^{-' + n7 + '}' + vpow(x, -a7 * n7) + vpow(y, -b7 * n7), 2), step('Write with positive exponents: ' + M(k7 + '^{-' + n7 + '}=\\frac{1}{' + Math.pow(k7, n7) + '}') + '.', simp(cf, ex, [x, y]), 2)); }
      return { variant: 'pq' + c, prompt: 'Simplify ' + M(expr) + '. Write the answer with positive exponents only.', parts: [{ answer: M(simp(cf, ex, [x, y])), check: { type: 'pow-simplify', expr: expr } }], steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= EVAL ================= */
  skill({
    id: 'pow-eval', best: [0, 1, 2], tag: 'EVAL', name: 'Evaluate powers',
    blurb: 'Products of powers, zero exponents, quotients and negative exponents (CP2) → negative exponents, negative bases, sums (CP1) → fraction bases, rational exponents (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], expr, val;
      if (c === 1) { var b = r.pick([2, 3, 5, 10]), m = r.int(2, 6), n = r.int(1, 3); need(Math.pow(b, m - n) <= 1000 && m > n);
        { var u = r.int(1, 3); need(Math.pow(b, m + u - n) <= 1000); expr = b + '^{' + (m - n) + '}\\cdot ' + b + '^{' + u + '}'; val = F(Math.pow(b, m - n + u)); steps.push(step('Add the exponents.', b + '^{' + (m - n + u) + '}', 2), step('Evaluate.', String(val.n), 2)); } }
      else if (c === 2) { var b2 = r.int(2, 12), k = r.int(2, 9); expr = k + '\\cdot ' + b2 + '^{0}'; val = F(k); if (r.chance(0.5)) { var b3 = r.pick([2, 3, 4, 5, 10]); expr = b3 + '^{-1}\\cdot ' + b3 + '^{2}'; val = F(b3); }
        steps.push(step('Use the rules: ' + M('a^{0}=1') + ', and add exponents with the same base.', String(val.n), 3)); }
      else if (c === 3 || c === 4) { var b4 = r.pick([2, 3, 4, 5, 10]) * (c === 4 && r.chance(0.5) ? -1 : 1), e4 = r.int(1, 3); need(Math.pow(Math.abs(b4), e4) <= 125);
        var bt = b4 < 0 ? '(' + b4 + ')' : String(b4); val = F(1, Math.pow(Math.abs(b4), e4)); if (b4 < 0 && e4 % 2) val = val.mul(-1);
        if (c === 3 && r.chance(0.5)) { var m3 = r.int(1, 4); expr = '\\frac{' + bt + '^{' + m3 + '}}{' + bt + '^{' + (m3 + e4) + '}}'; steps.push(step('Subtract the exponents.', bt + '^{-' + e4 + '}', 2), step('Write as a fraction.', num(val), 2)); }
        else if (c === 3 && r.chance(0.5)) { expr = '\\frac{1}{' + bt + '^{-' + e4 + '}}'; val = val.inv(); steps.push(step('A negative exponent in the denominator moves up.', bt + '^{' + e4 + '}', 2), step('Evaluate.', num(val), 2)); }
        else if (c === 4) { var add = r.int(1, 3); expr = bt + '^{-' + e4 + '}+' + add + '^{0}'; val = val.add(1); steps.push(step(M(bt + '^{-' + e4 + '}=\\frac{1}{' + bt + '^{' + e4 + '}}') + ' and ' + M(add + '^{0}=1') + '.', '', 2), step('Add.', num(val), 2)); }
        else { expr = bt + '^{-' + e4 + '}'; steps.push(step('Write as one over the positive power.', '\\frac{1}{' + bt + '^{' + e4 + '}}', 2), step('Evaluate.', num(val), 2)); } }
      else if (c === 5) { var pn = r.int(1, 5), pd = r.int(2, 5); need(gcd(pn, pd) === 1); var e5 = r.pick([1, 2, 3]); need(Math.pow(pd, e5) <= 125);
        expr = '\\left(\\frac{' + pn + '}{' + pd + '}\\right)^{-' + e5 + '}'; val = F(Math.pow(pd, e5), Math.pow(pn, e5));
        steps.push(step('A negative exponent flips the fraction.', '\\left(\\frac{' + pd + '}{' + pn + '}\\right)^{' + e5 + '}', 2), step('Evaluate.', num(val), 2)); }
      else { var root = r.pick([2, 3, 4]), base = r.pick(root === 2 ? [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] : root === 3 ? [2, 3, 4, 5] : [2, 3]), pw = c === 6 ? r.pick([1, 1, -1]) : r.pick([2, 3, 4, 5, -2, -3, -4]), rad = Math.pow(base, root); need(K.gcd(Math.abs(pw), root) === 1 && Math.pow(base, Math.abs(pw)) <= 243);
        
        expr = rad + '^{' + (pw < 0 ? '-' : '') + '\\frac{' + Math.abs(pw) + '}{' + root + '}}'; val = F(Math.pow(base, Math.abs(pw))); if (pw < 0) val = val.inv();
        steps.push(step('The denominator ' + root + ' means the ' + (root === 2 ? 'square' : root === 3 ? 'cube' : 'fourth') + ' root.', '\\sqrt' + (root === 2 ? '' : '[' + root + ']') + '{' + rad + '}=' + base, 2), step(Math.abs(pw) === 1 && pw > 0 ? 'That is the value.' : 'Then apply the numerator' + (pw < 0 ? ' and the negative sign (reciprocal).' : '.'), num(val), 2)); }
      return { variant: 'pe' + c, prompt: 'Evaluate ' + M(expr) + '. Write the answer as a whole number or a fraction.', parts: [{ answer: M(num(val)), check: { type: 'pow-eval', expr: expr } }], steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ---------- scientific notation helpers ---------- */
  /* exact decimal text for the integer m times 10^p */
  function dec(m, p) {
    var neg = m < 0, s = String(Math.abs(m));
    if (p >= 0) s = s + new Array(p + 1).join('0');
    else { var k = -p; while (s.length <= k) s = '0' + s; s = s.slice(0, s.length - k) + '.' + s.slice(s.length - k); s = s.replace(/0+$/, '').replace(/\.$/, ''); }
    return (neg ? '-' : '') + s;
  }
  /* a mantissa with 1–3 significant digits: {m: integer digits, d: decimals} with 1 ≤ m/10^d < 10 */
  function mant(r, sig) { var d = sig - 1, m = r.int(Math.pow(10, d), Math.pow(10, d + 1) - 1); if (d > 0 && m % 10 === 0) m += 1; return { m: m, d: d }; }
  function sci(mt, e) { return dec(mt.m, -mt.d) + '\\times10^{' + e + '}'; }
  function norm(m, d, e) { while (Math.abs(m) >= Math.pow(10, d + 1)) { if (m % 10 === 0) m /= 10; else d++; e++; } while (Math.abs(m) < Math.pow(10, d)) { if (d > 0) d--; else m *= 10; e--; } while (d > 0 && m % 10 === 0) { m /= 10; d--; } return { m: m, d: d, e: e }; }
  function sciN(n) { return dec(n.m, -n.d) + '\\times10^{' + n.e + '}'; }

  /* ================= SCI ================= */
  skill({
    id: 'sci-convert', best: [0, 1, 2], tag: 'SCI', name: 'Scientific notation',
    blurb: 'Large and small numbers to scientific notation and back (CP2) → negative exponents, fixing numbers that are not in scientific notation (CP1) → comparing numbers in scientific notation (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [];
      if (c === 1 || c === 3) { var mt = mant(r, c === 1 ? 2 : 3), e = c === 1 ? r.int(4, 7) : -r.int(3, 8), std = dec(mt.m, e - mt.d);
        steps.push(step('Move the decimal point so one nonzero digit is in front of it.', dec(mt.m, -mt.d), 2), step('Count the places moved: ' + (e > 0 ? 'a large number gets a positive exponent.' : 'a small number gets a negative exponent.'), sci(mt, e), 2));
        return { variant: 'sc' + c, prompt: 'Write ' + M(std) + ' in scientific notation.', parts: [{ answer: M(sci(mt, e)), check: { type: 'sci', want: 'to-sci', expr: std } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 2 || c === 4) { var mt2 = mant(r, r.pick([2, 3])), e2 = c === 2 ? r.int(3, 8) : -r.int(2, 6), s2 = sci(mt2, e2);
        steps.push(step('The exponent ' + e2 + ' moves the decimal point ' + Math.abs(e2) + ' places to the ' + (e2 > 0 ? 'right.' : 'left.'), dec(mt2.m, e2 - mt2.d), 3));
        return { variant: 'sc' + c, prompt: 'Write ' + M(s2) + ' in standard form.', parts: [{ answer: M(dec(mt2.m, e2 - mt2.d)), check: { type: 'sci', want: 'to-std', expr: s2 } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 7) { var es = r.shuffle([r.int(-6, 9), r.int(-6, 9), r.int(-6, 9)]), ms = [mant(r, 2), mant(r, 2), mant(r, 2)]; need(es[0] !== es[1] || ms[0].m !== ms[1].m); need(new Set(es).size >= 2);
        var terms = ms.map(function (m0, i) { return sci(m0, es[i]); }), vals = ms.map(function (m0, i) { return m0.m / Math.pow(10, m0.d) * Math.pow(10, es[i]); }), bi = vals.indexOf(Math.max.apply(null, vals));
        need(vals.filter(function (v) { return v === vals[bi]; }).length === 1);
        steps.push(step('Compare the exponents first; the larger exponent is the larger number.', '', 2), step('If the exponents are equal, compare the first factors.', terms[bi], 2));
        return { variant: 'sc7', prompt: 'Which number is the largest: ' + M(terms[0]) + ', ' + M(terms[1]) + ' or ' + M(terms[2]) + '?', parts: [{ answer: M(terms[bi]), check: { type: 'sci', want: 'compare', terms: terms } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      // c5, c6: a number written with the wrong first factor
      var big = c === 5 ? r.int(11, 999) : r.int(1, 9), dd = c === 5 ? r.int(0, 1) : r.int(1, 3), ee = r.int(-8, 9), shown = dec(big, -dd) + '\\times10^{' + ee + '}';
      if (c === 6) shown = dec(big, -dd - 1) + '\\times10^{' + ee + '}';
      need(!/^0?\.?0*$/.test(shown) && big % 10 !== 0);
      var nn = norm(big, c === 6 ? dd + 1 : dd, ee); need(sciN(nn) !== shown);
      steps.push(step('Rewrite the first factor so it is between 1 and 10.', '', 2), step('Moving the decimal point ' + (c === 5 ? 'left adds to' : 'right subtracts from') + ' the exponent.', sciN(nn), 2));
      return { variant: 'sc' + c, prompt: 'The number ' + M(shown) + ' is not in scientific notation. Rewrite it in scientific notation.', parts: [{ answer: M(sciN(nn)), check: { type: 'sci', want: 'op', expr: shown } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= SCIOPS ================= */
  var RATIOS = [['A large city has a population of ', ' people. A small town has ', ' people. How many times larger is the city’s population than the town’s?'],
    ['The Sun is about ', ' meters from Earth. The Moon is about ', ' meters from Earth. How many times farther away is the Sun?'],
    ['A hard drive holds ', ' bytes. A photo uses ', ' bytes. How many photos fit on the drive?']];
  skill({
    id: 'sci-ops', best: [0, 1, 2], tag: 'SCIOPS', name: 'Operations in scientific notation',
    blurb: 'Multiply and divide (CP2) → results that need rewriting, negative exponents, adding and subtracting (CP1) → “how many times” contexts and rounded answers (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], a = mant(r, c <= 2 ? 1 : 2), b = mant(r, c <= 2 ? 1 : 2), ea = r.int(c <= 2 ? 2 : -6, 9), eb = r.int(c <= 2 ? 2 : -6, 9);
      if (c === 1 || c === 3) { var prod = norm(a.m * b.m, a.d + b.d, ea + eb); need(a.m > 1 && b.m > 1 && prod.e !== 0); if (c === 1) need(a.m * b.m < 10); else need(a.m * b.m >= Math.pow(10, a.d + b.d + 1) || (ea < 0 || eb < 0));
        var ex = '\\left(' + sci(a, ea) + '\\right)\\left(' + sci(b, eb) + '\\right)';
        steps.push(step('Multiply the first factors and add the exponents.', dec(a.m * b.m, -(a.d + b.d)) + '\\times10^{' + (ea + eb) + '}', 2), step(c === 1 ? 'The first factor is already between 1 and 10.' : 'Rewrite so the first factor is between 1 and 10.', sciN(prod), 2));
        return { variant: 'so' + c, prompt: 'Multiply. Write the answer in scientific notation: ' + M(ex) + '.', parts: [{ answer: M(sciN(prod)), check: { type: 'sci', want: 'op', expr: ex } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 2 || c === 4) { var q = mant(r, c === 2 ? 1 : 2), eq = r.int(c === 2 ? 1 : -5, 7), top = norm(q.m * b.m, q.d + b.d, eq + eb), quo = norm(q.m, q.d, eq);
        if (c === 2) need(q.m * b.m < Math.pow(10, q.d + b.d + 1) && eq + eb > 0); else need(q.m * b.m >= Math.pow(10, q.d + b.d + 1) || eq < 0 || eb < 0);
        need(q.m > 1 && b.m > 1 && top.e !== 0 && eb !== 0 && quo.e !== 0); var ex2 = '\\frac{' + sciN(top) + '}{' + sci(b, eb) + '}';
        steps.push(step('Divide the first factors and subtract the exponents.', '', 2), step('Write the result in scientific notation.', sciN(quo), 2));
        return { variant: 'so' + c, prompt: 'Divide. Write the answer in scientific notation: ' + M(ex2) + '.', parts: [{ answer: M(sciN(quo)), check: { type: 'sci', want: 'op', expr: ex2 } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 5) { var e5 = r.int(3, 9), d5 = r.pick([1, 2]), a5 = mant(r, 2), b5 = mant(r, 2), sub = r.chance(0.4);
        var A = a5.m * Math.pow(10, d5), B = b5.m;   // same scale: A·10^(e5−1−d5…) — align: second number has exponent e5 − d5
        var ex5 = sci(a5, e5) + (sub ? '-' : '+') + sci(b5, e5 - d5); var tot = sub ? A - B : A + B; need(tot > 0);
        var res = norm(tot, a5.d + d5, e5);
        steps.push(step('Rewrite so both have the same power of 10.', dec(b5.m, -(b5.d + d5)) + '\\times10^{' + e5 + '}', 2), step((sub ? 'Subtract' : 'Add') + ' the first factors, then write in scientific notation.', sciN(res), 2));
        return { variant: 'so5', prompt: (sub ? 'Subtract' : 'Add') + '. Write the answer in scientific notation: ' + M(ex5) + '.', parts: [{ answer: M(sciN(res)), check: { type: 'sci', want: 'op', expr: ex5 } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      var R = r.pick(RATIOS), small = mant(r, c === 6 ? 1 : 2), es = r.int(2, 6), k6 = c === 6 ? r.pick([2, 3, 4, 5, 6]) : null;
      if (c === 6) { var shift = r.int(2, 5), bigM = norm(small.m * k6, small.d, es + shift), t1 = sciN(bigM), t2 = sci(small, es), rr = norm(k6, 0, shift);
        steps.push(step('Divide the larger number by the smaller one.', '\\frac{' + t1 + '}{' + t2 + '}', 2), step('Divide the first factors and subtract the exponents.', sciN(rr), 2));
        return { variant: 'so6', prompt: R[0] + M(t1) + R[1] + M(t2) + R[2] + ' Write the answer in scientific notation.', parts: [{ answer: M(sciN(rr)), check: { type: 'sci', want: 'ratio', terms: [t1, t2], op: 'div' } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      var big7 = mant(r, 3), eb7 = es + r.int(2, 6), u1 = sci(big7, eb7), u2 = sci(small, es), qv7 = (big7.m / Math.pow(10, big7.d)) / (small.m / Math.pow(10, small.d)) * Math.pow(10, eb7 - es);
      var ex7 = Math.floor(Math.log10(qv7) + 1e-12), man7 = Math.round(qv7 / Math.pow(10, ex7) * 10 + 1e-9) / 10; if (man7 >= 10) { man7 = man7 / 10; ex7++; }
      need(Math.abs(qv7 / Math.pow(10, ex7) * 10 - Math.round(qv7 / Math.pow(10, ex7) * 10)) > 0.02 && Math.abs(Math.abs(qv7 / Math.pow(10, ex7) * 10 - Math.floor(qv7 / Math.pow(10, ex7) * 10)) - 0.5) > 0.02);
      steps.push(step('Divide the larger number by the smaller one.', '\\frac{' + u1 + '}{' + u2 + '}', 2), step('Divide the first factors, subtract the exponents, round to one decimal place.', man7 + '\\times10^{' + ex7 + '}', 2));
      return { variant: 'so7', prompt: R[0] + M(u1) + R[1] + M(u2) + R[2] + ' Write the answer in scientific notation, rounding the first factor to one decimal place.', parts: [{ answer: M(String(man7).replace(/^(\d)$/, '$1.0') + '\\times10^{' + ex7 + '}'), check: { type: 'sci', want: 'ratio', terms: [u1, u2], op: 'div', round: 1 } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  NS.registerSkillSet({
    id: 'algebra1-exponents-scientific-notation', course: 'algebra1', courseName: 'Algebra 1', unit: 'exponents-exponential-functions', unitName: 'Exponents and Scientific Notation',
    title: 'The Power Pantry',
    tags: { PRODUCT: 'Product and power rules', QUOTIENT: 'Quotient, zero and negative exponents', EVAL: 'Evaluate powers', SCI: 'Scientific notation', SCIOPS: 'Operations in scientific notation' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Product and power</h4><p>⟨a^{m}\\cdot a^{n}=a^{m+n}⟩, ⟨(a^{m})^{n}=a^{mn}⟩, ⟨(ab)^{n}=a^{n}b^{n}⟩.</p></section>' +
      '<section><h4>Quotient</h4><p>⟨\\frac{a^{m}}{a^{n}}=a^{m-n}⟩, ⟨a^{0}=1⟩, ⟨a^{-n}=\\frac{1}{a^{n}}⟩.</p></section>' +
      '<section><h4>Rational exponents</h4><p>⟨a^{\\frac{1}{n}}=\\sqrt[n]{a}⟩, ⟨a^{\\frac{m}{n}}=(\\sqrt[n]{a})^{m}⟩.</p></section>' +
      '<section><h4>Scientific notation</h4><p>⟨a\\times10^{n}⟩ with ⟨1\\le a<10⟩. Large numbers: ⟨n>0⟩; small numbers: ⟨n<0⟩.</p></section>' +
      '</div>',
    gaps: ['Simplifying radicals (such as ⟨\\sqrt{72}⟩) and variables with rational exponents are not generated.'],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
