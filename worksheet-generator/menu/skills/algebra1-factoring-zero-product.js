/* Menu Assessment Generator — Algebra 1 · Unit 10 Factoring and the Zero Product Property (roadmap days 130–145).
   Skill groups: GCF (greatest common factor and grouping), TRI (trinomials), SPECIAL (difference of squares,
   perfect squares), SOLVE (zero product property, solving by factoring), APPLY (area, integers, falling objects).
   The verifier multiplies every factorization back out, checks every factor is primitive and irreducible over the
   integers, and finds the rational roots of every equation itself. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, M = K.M, num = K.num, lin = K.lin;
  var need = K.need, nz = K.nz, step = K.step, gcd = K.gcd;
  var skills = [], CUR = 'x';   // the variable letter of the current problem
  function letter(r) { CUR = r.pick(['x', 'x', 'x', 'y', 'a', 'm', 't', 'n']); return CUR; }
  function skill(d) { skills.push(d); return d; }
  function g3(a, b, c) { return gcd(gcd(Math.abs(a), Math.abs(b)), Math.abs(c || 0)); }
  /* (p·x + q) as TeX; a single x stays bare */
  function f1(p, q, v) { return '(' + lin([[p, v || CUR], [q, '']]) + ')'; }
  function poly(cs, v) { v = v || CUR; var t = []; for (var k = cs.length - 1; k >= 0; k--) if (cs[k]) t.push([cs[k], k === 0 ? '' : k === 1 ? v : v + '^' + k]); return lin(t); }
  /* multiply coefficient lists (low → high) */
  function mul(a, b) { var out = []; for (var i = 0; i < a.length + b.length - 1; i++) out.push(0); a.forEach(function (x, i) { b.forEach(function (y, j) { out[i + j] += x * y; }); }); return out; }
  function mono(g, k, v) { v = v || CUR; return (g === 1 ? '' : g === -1 ? '-' : num(g)) + (k ? v + (k > 1 ? '^' + k : '') : (Math.abs(g) === 1 ? '1' : '')); }
  function isSq(n) { return n >= 0 && Math.round(Math.sqrt(n)) * Math.round(Math.sqrt(n)) === n; }
  function irr2(a, b, c) { return !isSq(b * b - 4 * a * c); }
  function ord(r, x, y) { return r.chance(0.5) ? [x, y] : [y, x]; }
  var FACTOR = 'Factor completely: ';

  /* ================= GCF · greatest common factor and grouping ================= */
  skill({
    id: 'gcf', best: [0, 1, 2], tag: 'GCF', name: 'Factor out the GCF; factor by grouping',
    blurb: '6x + 9 (CP2) → 4x² + 10x, three terms, a common binomial factor (CP1) → grouping four terms, GCF then grouping, grouping that factors again (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], cs, ans; letter(r);
      if (c === 1) { var g = r.int(2, 9), a = r.int(1, 7), b = r.int(1, 9); need(gcd(a, b) === 1); cs = [g * b, g * a]; ans = num(g) + f1(a, b);
        steps.push(step('The GCF of the coefficients is ' + g + '.', '', 1), step('Divide each term by the GCF.', ans, 2)); }
      else if (c === 2) { var g2 = r.int(2, 6), a2 = r.int(1, 5), b2 = nz(r, -9, 9); need(gcd(a2, Math.abs(b2)) === 1); cs = [0, g2 * b2, g2 * a2]; ans = mono(g2, 1) + f1(a2, b2);
        steps.push(step('The GCF is ' + M(mono(g2, 1)) + ' (the number and the variable).', '', 1), step('Divide each term by the GCF.', ans, 2)); }
      else if (c === 4) { var g3v = r.int(2, 5) * r.sign(), k3 = 1, a3 = 1, b3 = nz(r, -7, 7), c3 = nz(r, -9, 9); need(g3(a3, b3, c3) === 1 && irr2(a3, b3, c3));
        var inner = poly([c3, b3, a3]); cs = mul(k3 === 1 ? [0, g3v] : [0, 0, g3v], [c3, b3, a3]); ans = mono(g3v, k3) + '(' + inner + ')';
        steps.push(step('GCF: ' + M(mono(g3v, k3)) + (g3v < 0 ? ' (take out the negative so the first term inside is positive)' : '') + '.', '', 1), step('Divide every term by the GCF; the trinomial left does not factor.', ans, 2)); }
      else if (c === 3) { var h4 = nz(r, -7, 7), a4 = r.int(1, 5), b4 = nz(r, -9, 9); need(gcd(a4, Math.abs(b4)) === 1);
        var expr4 = mono(a4, 1) + f1(1, h4) + (b4 < 0 ? '-' : '+') + (Math.abs(b4) === 1 ? '' : Math.abs(b4)) + f1(1, h4); ans = f1(1, h4) + f1(a4, b4);
        steps.push(step('Both terms share the binomial ' + M(f1(1, h4)) + '.', '', 2), step('Factor it out.', ans, 2));
        return { variant: 'gcf3', prompt: FACTOR + M(expr4) + '.', parts: [{ answer: M(ans), check: { type: 'factor', expr: expr4, v: CUR } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      else {
        // grouping: (x + h)(a·x² + d), possibly with a GCF in front (c6) or a quadratic that factors again (c7)
        var h = nz(r, -6, 6), a5 = r.int(1, 3), d, gg = c === 6 ? r.int(2, 4) : 1, quad;
        if (c === 7) { var n7 = r.int(1, 5); a5 = 1; d = -n7 * n7; quad = f1(1, -n7) + f1(1, n7); need(n7 !== Math.abs(h)); gg = 0; }
        else { d = nz(r, -9, 9); need(gcd(a5, Math.abs(d)) === 1 && (d > 0 || !isSq(-d * a5) || a5 > 1) && irr2(a5, 0, d)); quad = '(' + poly([d, 0, a5]) + ')'; }
        cs = gg === 0 ? mul([0, 1], mul([h, 1], [d, 0, a5])) : mul([gg], mul([h, 1], [d, 0, a5])); ans = (gg === 0 ? CUR : gg > 1 ? num(gg) : '') + f1(1, h) + quad;
        steps.push(step((gg !== 1 ? 'Take out the GCF ' + M(gg === 0 ? CUR : String(gg)) + ' first. Then group' : 'Group') + ' the first two terms and the last two terms.', '', 1),
          step('Factor each group: ' + M(mono(a5, 2) + f1(1, h) + (d < 0 ? '-' : '+') + Math.abs(d) + f1(1, h)) + '.', '', 2),
          step(c === 7 ? 'Factor out ' + M(f1(1, h)) + ', then factor the difference of squares.' : 'Factor out the common binomial.', ans, 2));
      }
      var expr = poly(cs);
      return { variant: 'gcf' + c, prompt: FACTOR + M(expr) + '.', parts: [{ answer: M(ans), check: { type: 'factor', expr: expr, v: CUR } }], steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= TRI · x² + bx + c ================= */
  skill({
    id: 'tri-a1', best: [0, 1], tag: 'TRI', name: 'Factor x² + bx + c',
    blurb: 'x² + 7x + 12 (CP2) → negative b and c, a GCF first, a negative leading term, prime trinomials (CP1) → x³ trinomials, x⁴ − 13x² + 36 (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], m, n, cs, ans, expr; letter(r);
      if (c <= 3) { m = c === 1 ? r.int(1, 9) : c === 2 ? -r.int(1, 9) : r.int(1, 12); n = c === 1 ? r.int(1, 9) : c === 2 ? -r.int(1, 9) : -r.int(1, 12); need(m !== -n && m !== n && Math.abs(m * n) <= 72); }
      else if (c <= 6) { m = nz(r, -9, 9); n = nz(r, -9, 9); need(m !== -n); }
      if (c <= 3) { cs = mul([m, 1], [n, 1]); var p2 = ord(r, m, n); ans = f1(1, p2[0]) + f1(1, p2[1]);
        steps.push(step('Find two numbers that multiply to ' + num(m * n) + ' and add to ' + num(m + n) + '.', num(m) + ',\\ ' + num(n), 2), step('Write the factors.', ans, 2)); }
      else if (c === 5) { var g = r.int(2, 5); cs = mul([g], mul([m, 1], [n, 1])); ans = num(g) + f1(1, m) + f1(1, n);
        steps.push(step('Take out the GCF ' + g + '.', num(g) + '(' + poly(mul([m, 1], [n, 1])) + ')', 1), step('Two numbers with product ' + num(m * n) + ' and sum ' + num(m + n) + ': ' + num(m) + ' and ' + num(n) + '.', ans, 3)); }
      else if (c === 4) {
        if (r.chance(0.3)) { var b5 = nz(r, -12, 12), c5 = nz(r, -30, 30); need(irr2(1, b5, c5)); expr = poly([c5, b5, 1]);
          steps.push(step('List the factor pairs of ' + num(c5) + '; none adds to ' + num(b5) + '.', '', 3), step('The trinomial is prime.', '', 1));
          return { variant: 'tri4p', prompt: FACTOR + M(expr) + '. If it cannot be factored, write “prime.”', parts: [{ answer: 'Prime', check: { type: 'factor', expr: expr, v: CUR } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
        cs = mul([-1], mul([m, 1], [n, 1])); ans = '-' + f1(1, m) + f1(1, n);
        steps.push(step('Take out −1 so the leading coefficient is positive.', '-(' + poly(mul([m, 1], [n, 1])) + ')', 1), step('Two numbers with product ' + num(m * n) + ' and sum ' + num(m + n) + '.', ans, 3));
        expr = poly(cs);
        return { variant: 'tri4', prompt: FACTOR + M(expr) + '. If it cannot be factored, write “prime.”', parts: [{ answer: M(ans), check: { type: 'factor', expr: expr, v: CUR } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      else if (c === 6) { var g6 = r.int(1, 3) * r.sign(); cs = mul([0, g6], mul([m, 1], [n, 1])); ans = mono(g6, 1) + f1(1, m) + f1(1, n);
        steps.push(step('Take out the GCF ' + M(mono(g6, 1)) + '.', mono(g6, 1) + '(' + poly(mul([m, 1], [n, 1])) + ')', 1), step('Factor the trinomial.', ans, 3)); }
      else { var p = r.int(1, 4), q = r.int(1, 5); need(p !== q); cs = mul(mul([-p * p, 0, 1], [-q * q, 0, 1]), [1]); var lo = Math.min(p, q), hi = Math.max(p, q);
        ans = f1(1, -lo) + f1(1, lo) + f1(1, -hi) + f1(1, hi);
        steps.push(step('Treat it like a trinomial in ' + M(CUR + '^2') + ': two numbers with product ' + p * p * q * q + ' and sum ' + num(-(p * p + q * q)) + '.', '(' + CUR + '^2-' + p * p + ')(' + CUR + '^2-' + q * q + ')', 2), step('Each factor is a difference of squares.', ans, 2)); }
      expr = poly(cs);
      return { variant: 'tri' + c, prompt: FACTOR + M(expr) + '.', parts: [{ answer: M(ans), check: { type: 'factor', expr: expr, v: CUR } }], steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= TRI · ax² + bx + c ================= */
  skill({
    id: 'tri-a', best: [1, 2], tag: 'TRI', name: 'Factor ax² + bx + c',
    blurb: '2x² + 7x + 3 (CP2) → mixed signs, a = 4 or 6 (CP1) → a GCF first, larger coefficients, prime trinomials (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], p, q, m, n, g = 1; letter(r);
      if (c <= 3) { p = r.pick([2, 3, 5]); q = 1; m = c <= 2 ? r.int(1, 7) : nz(r, -7, 7); n = c <= 2 ? r.int(1, 7) : nz(r, -7, 7); }
      else if (c === 4) { p = r.pick([2, 3, 5, 7]); q = 1; m = nz(r, -9, 9); n = nz(r, -9, 9); }
      else { p = r.int(2, c === 7 ? 6 : 4); q = r.int(2, c === 7 ? 5 : 3); m = nz(r, -9, 9); n = nz(r, -9, 9); if (c === 6) g = r.int(2, 4) * (r.chance(0.3) ? -1 : 1); }
      need(gcd(p, Math.abs(m)) === 1 && gcd(q, Math.abs(n)) === 1);
      if (c === 7) { var sq = r.pick([2, 3]), k7 = r.int(1, 5); need(k7 !== 1 || sq !== 1); var csq = mul([-1, 0, sq * sq], [-k7 * k7, 0, 1]), e7 = poly(csq);
        var a7 = f1(sq, -1) + f1(sq, 1) + f1(1, -k7) + f1(1, k7);
        steps.push(step('Treat it as a trinomial in ' + M(CUR + '^2') + ' and use the ac method.', '(' + poly([-1, 0, sq * sq]) + ')(' + poly([-k7 * k7, 0, 1]) + ')', 2), step('Both factors are differences of squares.', a7, 2));
        return { variant: 'tria7', prompt: FACTOR + M(e7) + '.', parts: [{ answer: M(a7), check: { type: 'factor', expr: e7, v: CUR } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      if (false) { var A = r.int(2, 9), B = nz(r, -15, 15), Cc = nz(r, -20, 20); need(g3(A, B, Cc) === 1 && irr2(A, B, Cc)); var exprP = poly([Cc, B, A]);
        steps.push(step('ac = ' + A * Cc + ': no factor pair adds to ' + B + '.', '', 3), step('The trinomial is prime.', '', 1));
        return { variant: 'tria7p', prompt: FACTOR + M(exprP) + '. If it cannot be factored, write “prime.”', parts: [{ answer: 'Prime', check: { type: 'factor', expr: exprP, v: CUR } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      var tri = mul([m, p], [n, q]), cs = mul([g], tri), expr = poly(cs);
      var ans = (g !== 1 ? num(g) : '') + (r.chance(0.5) ? f1(p, m) + f1(q, n) : f1(q, n) + f1(p, m));
      var ac = tri[2] * tri[0];
      if (g !== 1) steps.push(step('Take out the GCF ' + g + '.', num(g) + '(' + poly(tri) + ')', 1));
      steps.push(step('ac method: ' + M('ac=' + num(ac)) + '. Find two numbers with product ' + num(ac) + ' and sum ' + num(tri[1]) + ': ' + num(p * n) + ' and ' + num(q * m) + '.', '', 2),
        step('Split the middle term and factor by grouping.', ans, 2));
      return { variant: 'tria' + c, prompt: FACTOR + M(expr) + (c === 7 ? '. If it cannot be factored, write “prime.”' : '.'), parts: [{ answer: M(ans), check: { type: 'factor', expr: expr, v: CUR } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= SPECIAL · difference of squares, perfect squares ================= */
  skill({
    id: 'special', best: [0, 1, 2], tag: 'SPECIAL', name: 'Special products: a² − b² and perfect squares',
    blurb: 'x² − 49 (CP2) → 4x² − 25, perfect square trinomials (CP1) → a GCF first, x⁴ − 81, sums of squares are prime (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], cs, ans, prime = false; letter(r);
      var a = c === 1 || c === 2 ? 1 : r.int(2, 5), n = r.int(1, 12); need(gcd(a, n) === 1);
      if (c === 1 || c === 3) { cs = [-n * n, 0, a * a]; ans = f1(a, -n) + f1(a, n); steps.push(step('This is a difference of squares: ' + M('(' + mono(a, 1) + ')^2-' + n + '^2') + '.', '', 2), step('Use ' + M('a^2-b^2=(a-b)(a+b)') + '.', ans, 2)); }
      else if (c === 2 || c === 4) { var s = r.sign(); cs = mul([s * n, a], [s * n, a]); ans = '(' + lin([[a, CUR], [s * n, '']]) + ')^2';
        steps.push(step('First and last terms are squares, and the middle term is ' + M('2\\cdot ' + mono(a, 1) + '\\cdot ' + n) + ' (sign ' + (s > 0 ? '+' : '−') + ').', '', 2), step('Use ' + M('a^2\\pm 2ab+b^2=(a\\pm b)^2') + '.', ans, 2)); }
      else if (c === 5) { var g = r.int(2, 5), k = r.int(0, 1); cs = mul(k ? [0, g] : [g], [-n * n, 0, a * a]); ans = mono(g, k) + f1(a, -n) + f1(a, n); need(g !== a);
        steps.push(step('Take out the GCF ' + M(mono(g, k)) + '.', mono(g, k) + '(' + poly([-n * n, 0, a * a]) + ')', 1), step('Factor the difference of squares.', ans, 2)); }
      else if (c === 6) { var n6 = r.int(1, 3), a6 = r.int(1, 2), g6 = r.pick([1, 1, 2, 3]); need(gcd(a6, n6) === 1); cs = mul([g6], [-Math.pow(n6, 4), 0, 0, 0, Math.pow(a6, 4)]);
        ans = (g6 > 1 ? num(g6) : '') + '(' + poly([n6 * n6, 0, a6 * a6]) + ')' + f1(a6, -n6) + f1(a6, n6);
        steps.push(step('Difference of squares: ' + M('(' + mono(a6 * a6, 2) + ')^2-(' + n6 * n6 + ')^2') + '.', '(' + poly([n6 * n6, 0, a6 * a6]) + ')(' + poly([-n6 * n6, 0, a6 * a6]) + ')', 2), step('The second factor is a difference of squares again; the sum of squares is prime.', ans, 2)); }
      else { if (r.chance(0.4)) { prime = true; cs = [n * n, 0, a * a]; steps.push(step('A sum of squares has no real factors.', '', 2), step('It is prime.', '', 1)); }
        else { var g7 = r.int(2, 4); cs = mul([0, 0, g7], [-n * n, 0, a * a]); ans = mono(g7, 2) + f1(a, -n) + f1(a, n); steps.push(step('Take out ' + M(mono(g7, 2)) + '.', '', 1), step('Factor the difference of squares.', ans, 2)); } }
      var expr = poly(cs);
      return { variant: 'sp' + c + (prime ? 'p' : ''), prompt: FACTOR + M(expr) + (c >= 6 ? '. If it cannot be factored, write “prime.”' : '.'), parts: [{ answer: prime ? 'Prime' : M(ans), check: { type: 'factor', expr: expr, v: CUR } }], steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= SOLVE · zero product property ================= */
  function rootsTeX(rs, v) { return rs.map(function (x) { return M((v || 'x') + '=' + num(x)); }).join(' or '); }
  skill({
    id: 'zero-product', best: [0, 1, 2], tag: 'SOLVE', name: 'Zero product property; solve by factoring',
    blurb: '(x − 3)(x + 5) = 0 (CP2) → x² + bx + c = 0, move every term to one side (CP1) → ax² + bx + c = 0, cubics such as x³ − 9x = 0 (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], eq, roots, K2 = K.Fr; CUR = 'x';
      var m = nz(r, -9, 9), n = nz(r, -9, 9);
      if (c === 1) { need(m !== n); eq = f1(1, -m) + f1(1, -n) + '=0'; roots = [m, n]; steps.push(step('Zero product property: set each factor equal to 0.', 'x' + (m < 0 ? '+' : '-') + Math.abs(m) + '=0\\text{ or }x' + (n < 0 ? '+' : '-') + Math.abs(n) + '=0', 2)); }
      else if (c === 2) { if (r.chance(0.5)) { eq = 'x' + f1(1, -n) + '=0'; roots = [0, n]; } else { var p2 = r.int(2, 4); eq = f1(p2, -p2 * m) + f1(1, -n) + '=0'; roots = [m, n]; need(m !== n); }
        steps.push(step('Set each factor equal to 0 and solve each equation.', '', 3)); }
      else if (c === 3) { need(m !== n); eq = poly(mul([-m, 1], [-n, 1])) + '=0'; roots = [m, n]; steps.push(step('Factor.', f1(1, -m) + f1(1, -n) + '=0', 2), step('Set each factor equal to 0.', '', 1)); }
      else if (c === 4) { need(m !== n); var cs4 = mul([-m, 1], [-n, 1]), kk = r.int(1, 9) * r.sign();
        if (r.chance(0.5)) { eq = poly([0, cs4[1], 1]) + '=' + num(-cs4[0]); } else { eq = poly([cs4[0] + kk, cs4[1], 1]) + '=' + num(kk); }
        roots = [m, n]; steps.push(step('Move every term to one side so the other side is 0.', poly(cs4) + '=0', 1), step('Factor and use the zero product property.', f1(1, -m) + f1(1, -n) + '=0', 2)); }
      else if (c === 5) { need(m !== n); var r1 = m, r2 = n;
        if (r.chance(0.5)) { var mm = nz(r, -6, 6), nn = -(r1 + r2) - mm, kk5 = mm * nn - r1 * r2; need(kk5 !== 0 && nn !== 0); eq = f1(1, mm) + f1(1, nn) + '=' + num(kk5);
          steps.push(step('The right side is not 0, so the zero product property does not apply yet. Multiply out and subtract ' + num(kk5) + '.', poly(mul([-r1, 1], [-r2, 1])) + '=0', 2)); }
        else { var cs5 = mul([-r1, 1], [-r2, 1]), d5 = nz(r, -5, 5), e5 = nz(r, -9, 9); eq = poly([cs5[0] + e5, cs5[1] + d5, 1]) + '=' + poly([e5, d5]);
          steps.push(step('Collect every term on the left side.', poly(cs5) + '=0', 2)); }
        roots = [r1, r2]; steps.push(step('Factor and set each factor equal to 0.', f1(1, -r1) + f1(1, -r2) + '=0', 1)); }
      else if (c === 6) { var p6 = r.pick([2, 3, 5]), q6 = ctx.intOnly ? p6 * nz(r, -4, 4) : nz(r, -9, 9), n6 = nz(r, -9, 9); need(ctx.intOnly || gcd(p6, Math.abs(q6)) === 1); need(-q6 / p6 !== n6); var cs6 = mul([q6, p6], [-n6, 1]); eq = poly(cs6) + '=0';
        roots = [new K2(-q6, p6), n6];
        steps.push(step('Factor with the ac method.', f1(p6, q6) + f1(1, -n6) + '=0', 2), step('Set each factor equal to 0.', '', 1)); }
      else { var a7 = r.int(1, 3) * r.sign(); need(m !== n && m !== 0 && n !== 0); var cs7 = mul([0, a7], mul([-m, 1], [-n, 1])); eq = poly(cs7) + '=0'; roots = [0, m, n];
        steps.push(step('Take out the GCF ' + M(mono(a7, 1)) + '.', mono(a7, 1) + '(' + poly(mul([-m, 1], [-n, 1])) + ')=0', 2), step('Factor the trinomial and set each factor equal to 0.', '', 2)); }
      roots = roots.map(function (x) { return K.Fr.of(x); }).sort(function (x, y) { return x.cmp(y); }).filter(function (x, i, arr) { return i === 0 || !arr[i - 1].eq(x); });
      steps.push(step('Solutions.', roots.map(function (x) { return 'x=' + num(x); }).join(',\\ '), 1));
      return { variant: 'zp' + c, prompt: 'Solve ' + M(eq) + '.', parts: [{ answer: rootsTeX(roots), check: { type: 'quad-roots', eq: eq, v: 'x' } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= APPLY · problems solved by factoring ================= */
  skill({
    id: 'factor-apply', best: [1, 2], tag: 'APPLY', name: 'Solve problems by factoring',
    blurb: 'Consecutive integers (CP2) → rectangle areas, a dropped object (CP1) → length = 2w ± k, a thrown object, a uniform border (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = []; CUR = 'x';
      if (c <= 2) { var stp = c === 1 ? 1 : 2, kind = c === 1 ? '' : r.pick(['even ', 'odd ']), n = c === 1 ? r.int(3, 30) : (kind === 'even ' ? 2 * r.int(2, 15) : 2 * r.int(2, 15) + 1), P = n * (n + stp);
        steps.push(step('Let the integers be ' + M('n') + ' and ' + M('n+' + stp) + '.', 'n(n+' + stp + ')=' + P, 1), step('Rewrite and factor.', '(n-' + n + ')(n+' + (n + stp) + ')=0', 2), step('Use the positive solution.', 'n=' + n, 1));
        return { variant: 'fa' + c, prompt: 'The product of two consecutive positive ' + kind + 'integers is ' + P + '. Find the integers.', parts: [{ answer: 'The integers are ' + M(String(n)) + ' and ' + M(String(n + stp)) + '.', check: { type: 'quad-apply', form: 'consec', p: 0 } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      if (c === 3 || c === 4) { var w = r.int(2, 12), unit = r.pick(['feet', 'meters', 'inches']), u1 = unit === 'feet' ? 'foot' : unit.slice(0, -1);
        var twice = c === 4, more = !twice || r.chance(0.5), k = r.int(1, 9), L = (twice ? 2 * w : w) + (more ? k : -k); need(L > w);
        var phrase = k + ' ' + (k === 1 ? u1 : unit) + ' ' + (more ? 'more' : 'less') + ' than ' + (twice ? 'twice ' : '') + 'its width', A = w * L;
        steps.push(step('Let the width be ' + M('w') + '; the length is ' + M(twice ? '2w' + (more ? '+' : '-') + k : 'w+' + k) + '.', 'w(' + (twice ? '2w' : 'w') + (more ? '+' : '-') + k + ')=' + A, 1), step('Write in standard form and factor.', '', 2), step('Width must be positive.', 'w=' + w, 1));
        return { variant: 'fa' + c, prompt: 'The length of a rectangle is ' + phrase + '. The area is ' + A + ' square ' + unit + '. Find the width and the length.', parts: [{ answer: 'Width ' + M(String(w)) + ' ' + unit + ', length ' + M(String(L)) + ' ' + unit + '.', check: { type: 'quad-apply', form: 'rect', k: 0, A: 1 } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      if (c === 6 || c === 7) { var a = r.int(1, c === 6 ? 8 : 7), b = c === 6 ? a : r.int(1, 4), up = c === 7; need(!up || a > b);
        var v = up ? 16 * (a - b) : 0, h0 = 16 * a * b, rule = 'h=' + poly([h0, v, -16], 't');
        steps.push(step('The object hits the ground when ' + M('h=0') + '.', poly([h0, v, -16], 't') + '=0', 1), step('Take out −16 and factor.', '-16' + f1(1, -a, 't') + f1(1, b, 't') + '=0', 2), step('Time must be positive.', 't=' + a, 1));
        var thing = r.pick(up ? [['A ball is thrown upward from a platform', 'it'], ['A rocket is launched upward from a tower', 'it'], ['A water balloon is tossed upward from a balcony', 'it']] : [['A stone is dropped from a cliff', 'it'], ['A phone falls from a bridge', 'it'], ['A wrench is dropped from a crane', 'it'], ['An apple falls from a tall tree branch', 'it']]);
        var intro = thing[0] + ' ' + h0 + ' feet high. Its height after ' + M('t') + ' seconds is ' + M(rule) + '.';
        return { variant: 'fa' + c, prompt: intro + ' After how many seconds does it hit the ground?', parts: [{ answer: M('t=' + a) + ' seconds', check: { type: 'quad-apply', form: 'rule', rule: rule, v: 't' } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      // c7: a uniform border
      var W = r.int(4, 12), Ln = W + r.int(1, 6), x = r.int(1, 4), Ab = (W + 2 * x) * (Ln + 2 * x);
      steps.push(step('With a border of width ' + M('x') + ' on every side, the outer dimensions are ' + M('(' + W + '+2x)') + ' by ' + M('(' + Ln + '+2x)') + '.', '(' + W + '+2x)(' + Ln + '+2x)=' + Ab, 2), step('Expand, move ' + Ab + ' to the left, and factor.', '', 2), step('A width must be positive.', 'x=' + x, 1));
      return { variant: 'fa5', prompt: 'A photo is ' + W + ' inches by ' + Ln + ' inches. A frame of uniform width ' + M('x') + ' inches goes around it. The photo and frame together cover ' + Ab + ' square inches. Find ' + M('x') + '.', parts: [{ answer: M('x=' + x) + ' inches', check: { type: 'quad-apply', form: 'border', W: 0, L: 1, A: 2 } }], steps: steps, space: [0.9, 1.1, 1.3] };
    }
  });

  /* ================= SPECIAL · sums and differences of cubes ================= */
  function cubeFactors(a, b, sgn, v) {   // a³x³ ± b³ = (ax ± b)(a²x² ∓ abx + b²)
    return f1(a, sgn * b, v) + '(' + poly([b * b, -sgn * a * b, a * a], v) + ')';
  }
  skill({
    id: 'cubes', print: ['maze', 'color', 'tarsia', 'error', 'who', 'stations'], best: [1, 2], tag: 'SPECIAL', name: 'Sums and differences of cubes',
    blurb: 'x³ − 8 and x³ + 27 (CP2) → 8x³ − 27, a common factor first (CP1) → a GCF with x, x⁶ − 64 (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, v = letter(r), sgn = r.sign(), steps = [], a = 1, b, g = 1, gx = 0, expr, ans;
      if (c === 7 && r.chance(0.5)) {   // x⁶ − b⁶: difference of squares first, then a sum and a difference of cubes
        b = r.int(1, 2); var b3 = b * b * b;
        expr = poly([-b3 * b3, 0, 0, 0, 0, 0, 1], v);
        ans = f1(1, -b, v) + '(' + poly([b * b, b, 1], v) + ')' + f1(1, b, v) + '(' + poly([b * b, -b, 1], v) + ')';
        steps.push(step('Difference of squares first.', '(' + poly([-b3, 0, 0, 1], v) + ')(' + poly([b3, 0, 0, 1], v) + ')', 2), step('Factor each cube.', ans, 3));
        return { variant: 'cube6', prompt: FACTOR + M(expr), parts: [{ answer: M(ans), check: { type: 'factor', expr: expr, v: v } }], steps: steps, space: [1.1, 1.3, 1.5] };
      }
      b = c <= 2 ? r.int(1, c === 1 ? 4 : 6) : r.int(1, 5);
      if (c >= 3) { a = r.int(2, c === 3 ? 3 : 4); need(gcd(a, b) === 1); }
      if (c >= 4) g = r.int(2, 5) * (c === 7 && r.chance(0.3) ? -1 : 1);
      if (c === 6 || c === 7) gx = 1;
      var cs = [sgn * b * b * b * g, 0, 0, a * a * a * g]; if (gx) cs.unshift(0);
      expr = poly(cs, v);
      var gcfTex = g === 1 && !gx ? '' : mono(g, gx, v);
      ans = gcfTex + cubeFactors(a, b, sgn, v);
      if (gcfTex) steps.push(step('Factor out the GCF ' + M(gcfTex) + '.', gcfTex + '(' + poly(gx ? [sgn * b * b * b, 0, 0, a * a * a] : [sgn * b * b * b, 0, 0, a * a * a], v) + ')', 2));
      steps.push(step('Write each term as a cube: ' + M('(' + (a === 1 ? v : a + v) + ')^3') + ' and ' + M(b + '^3') + '.', '', 1));
      steps.push(step(sgn < 0 ? 'Difference of cubes: ⟨a^3-b^3=(a-b)(a^2+ab+b^2)⟩.' : 'Sum of cubes: ⟨a^3+b^3=(a+b)(a^2-ab+b^2)⟩.', ans, 3));
      return { variant: 'cube' + c + (sgn < 0 ? 'd' : 's'), prompt: FACTOR + M(expr), parts: [{ answer: M(ans), check: { type: 'factor', expr: expr, v: v } }], steps: steps, space: [0.9, 1.1, 1.3] };
    }
  });

  /* ================= TRI · two variables ================= */
  function t2(a, b, c) { return lin([[a, 'x^2'], [b, 'xy'], [c, 'y^2']]); }
  function f2(p, q) { return '(' + lin([[p, 'x'], [q, 'y']]) + ')'; }
  skill({
    id: 'two-var', print: ['maze', 'color', 'tarsia', 'error', 'who', 'stations'], best: [1, 2], tag: 'TRI', name: 'Factor with two variables',
    blurb: 'x² − 9y² and x² + 5xy + 6y² (CP2) → negative middle terms, a common factor such as 3xy (CP1) → leading coefficients other than 1, a GCF and a trinomial, x⁴ − 16y⁴ (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], expr, ans, g = 1;
      if (c === 1 || (c === 7 && r.chance(0.35))) {
        var b = r.int(2, c === 7 ? 3 : 15);
        if (c === 7) { expr = lin([[1, 'x^4'], [-b * b * b * b, 'y^4']]); ans = '(' + lin([[1, 'x^2'], [b * b, 'y^2']]) + ')' + f2(1, b) + f2(1, -b);
          steps.push(step('Difference of squares.', '(' + lin([[1, 'x^2'], [b * b, 'y^2']]) + ')(' + lin([[1, 'x^2'], [-b * b, 'y^2']]) + ')', 2), step('The second factor is a difference of squares again.', ans, 2)); }
        else { var sw = r.chance(0.5), U = sw ? 'y' : 'x', V = sw ? 'x' : 'y'; expr = lin([[1, U + '^2'], [-b * b, V + '^2']]); ans = '(' + lin([[1, U], [b, V]]) + ')(' + lin([[1, U], [-b, V]]) + ')'; steps.push(step('Difference of squares: ⟨a^2-b^2=(a+b)(a-b)⟩.', ans, 3)); }
      } else if (c === 4) {   // a monomial GCF such as 3xy
        var k = r.int(2, 6), p4 = nz(r, -7, 7), q4 = nz(r, -7, 7), ex = r.pick([[1, 0], [0, 1], [1, 1]]); need(gcd(Math.abs(p4), Math.abs(q4)) === 1);
        var gm = (k === 1 ? '' : k) + (ex[0] ? 'x' : '') + (ex[1] ? 'y' : '');
        expr = lin([[k * p4, 'x^' + (1 + ex[0]) + (ex[1] ? 'y' : '')], [k * q4, (ex[0] ? 'x' : '') + 'y^' + (1 + ex[1])]]).replace(/\^1(?!\d)/g, '');
        ans = gm + f2(p4, q4); steps.push(step('Factor out the GCF ' + M(gm) + '.', ans, 3));
        return { variant: 'gcf2', prompt: FACTOR + M(expr), parts: [{ answer: M(ans), check: { type: 'factor', expr: expr, v: 'x', v2: 'y' } }], steps: steps, space: [0.8, 1.0, 1.2] };
      } else {
        var p = nz(r, c <= 2 ? 1 : -9, 9), q = nz(r, c <= 2 ? 1 : -9, 9), A = c >= 5 ? r.int(2, 4) : 1, B = 1;
        if (c >= 5) need(gcd(A, Math.abs(q)) === 1);
        if (c === 6 || c === 7) g = r.int(2, 5);
        if (c === 3) need(p < 0 || q < 0);
        // (A·x + p·y)(B·x + q·y) = AB x² + (Aq + Bp) xy + pq y²
        var a = A * B, bb = A * q + B * p, cc = p * q; need(bb !== 0);
        expr = t2(g * a, g * bb, g * cc);
        ans = (g === 1 ? '' : String(g)) + f2(A, p) + f2(B, q);
        if (g !== 1) steps.push(step('Factor out the GCF ' + g + '.', g + '(' + t2(a, bb, cc) + ')', 2));
        steps.push(step(a === 1 ? 'Find two numbers that multiply to ' + cc + ' and add to ' + bb + '; use ' + M('y') + ' with each.' : 'Use the ac method with ⟨ac=' + a * cc + '⟩.', ans, 3));
      }
      return { variant: 'two' + c, prompt: FACTOR + M(expr), parts: [{ answer: M(ans), check: { type: 'factor', expr: expr, v: 'x', v2: 'y' } }], steps: steps, space: [0.9, 1.1, 1.3] };
    }
  });


  // Lesson-specific aliases of independently verified generators; these remain selectable skills.
  (function(){var base=skills.find(function(s){return s.id==="gcf";});if(!base)return;
    skill({id:"factor-by-grouping",best:base.best,tag:base.tag,name:"Factor polynomials by grouping",blurb:"Group four terms and factor a common binomial.",
      difficultyProfile:'focused',fixedDifficulty:5,generate:function(ctx){return base.generate(Object.assign({},ctx,{c:5}));}});
  })();
  NS.registerSkillSet({
    id: 'algebra1-factoring-zero-product', course: 'algebra1', courseName: 'Algebra 1', unit: 'factoring-zero-product', unitName: 'Factoring and Zero Product Property',
    title: 'The Factor Factory Café',
    tags: { GCF: 'GCF and grouping', TRI: 'Factoring trinomials', SPECIAL: 'Special products', SOLVE: 'Zero product property', APPLY: 'Problems solved by factoring' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Always first</h4><p>Take out the greatest common factor (GCF), including a negative if the leading term is negative.</p><p>Check by multiplying the factors back out.</p></section>' +
      '<section><h4>Trinomials</h4><p>⟨x^2+bx+c⟩: two numbers with product ⟨c⟩ and sum ⟨b⟩.</p><p>⟨ax^2+bx+c⟩: two numbers with product ⟨ac⟩ and sum ⟨b⟩; split the middle term and group.</p></section>' +
      '<section><h4>Special products</h4><p>⟨a^2-b^2=(a-b)(a+b)⟩</p><p>⟨a^2+2ab+b^2=(a+b)^2⟩, ⟨a^2-2ab+b^2=(a-b)^2⟩</p><p>⟨a^2+b^2⟩ is prime.</p></section>' +
      '<section><h4>Grouping</h4><p>Group two terms at a time, factor each group, then factor out the common binomial.</p></section>' +
      '<section><h4>Zero product property</h4><p>If ⟨ab=0⟩, then ⟨a=0⟩ or ⟨b=0⟩. Get 0 on one side first; never divide by the variable.</p></section>' +
      '<section><h4>Word problems</h4><p>Falling objects: ⟨h=-16t^2+vt+h_0⟩ (feet). Keep only answers that make sense (positive lengths and times).</p></section></div>',
    gaps: [],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
