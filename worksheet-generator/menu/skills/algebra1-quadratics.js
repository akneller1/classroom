/* Menu Assessment Generator — Algebra 1 · Unit 11 Quadratic Functions and Equations (roadmap days 146–162).
   Skill groups: GRAPH (features of parabolas), ROOTS (square roots and factoring), FORMULA (discriminant and the
   quadratic formula), COMPLETE (completing the square and vertex form), APPLY (projectile models).
   The verifier reads every parabola back from the printed equation or the drawn curve, solves exactly (simplest radical
   form is required for exact answers) and rounds only when the problem asks for it. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, M = K.M, num = K.num, lin = K.lin, Fr = K.Fr;
  var need = K.need, nz = K.nz, step = K.step, F = K.F, gcd = K.gcd;
  var skills = [];
  function skill(d) { skills.push(d); return d; }
  function pt(x, y) { return '(' + num(x) + ',\\ ' + num(y) + ')'; }
  function quad(a, b, c, v) { v = v || 'x'; return lin([[a, v + '^{2}'], [b, v], [c, '']]); }
  function vform(a, h, k, v) { v = v || 'x'; a = Fr.of(a); var co = a.eq(1) ? '' : a.eq(-1) ? '-' : num(a); var inner = h === 0 ? v : v + (h > 0 ? '-' + h : '+' + (-h));
    return 'y=' + co + (h === 0 ? v + '^{2}' : '(' + inner + ')^{2}') + (k === 0 ? '' : (k > 0 ? '+' : '-') + Math.abs(k)); }
  function parab(a, h, k) {
    var pts = []; for (var x = h - 5; x <= h + 5; x += 0.5) { var y = Fr.of(a).val() * (x - h) * (x - h) + k; if (Math.abs(x) <= 7 && Math.abs(y) <= 7) pts.push([x, y]); }
    need(pts.length >= 7); return { kind: 'plane', xmin: -7, xmax: 7, ymin: -7, ymax: 7, points: [], segs: [], curves: [pts] };
  }
  /* exact roots of ax² + bx + c (integers): a list of TeX values in simplest form, or [] when there are none */
  function sqfree(n) { var m = 1, r = n; for (var k = 2; k * k <= r; k++) while (r % (k * k) === 0) { r /= k * k; m *= k; } return [m, r]; }
  function exact(a, b, c) {
    var D = b * b - 4 * a * c; if (D < 0) return { D: D, list: [] };
    var s0 = Math.round(Math.sqrt(D));
    if (s0 * s0 === D) { var r1 = F(-b - s0, 2 * a), r2 = F(-b + s0, 2 * a), L = [r1, r2].sort(function (p, q) { return p.cmp(q); }); if (L[0].eq(L[1])) L = [L[0]]; return { D: D, rational: true, list: L.map(num), vals: L }; }
    var mr = sqfree(D), m = mr[0], r = mr[1], g = gcd(gcd(Math.abs(b), m), Math.abs(2 * a)), p = -b / g, q = m / g, s = 2 * a / g; if (s < 0) { p = -p; s = -s; }
    var rad = (q === 1 ? '' : q) + '\\sqrt{' + r + '}', top = (p === 0 ? '' : p) + '\\pm ' + rad;
    return { D: D, rational: false, pm: s === 1 ? top : '\\frac{' + top + '}{' + s + '}', approx: [(-b - Math.sqrt(D)) / (2 * a), (-b + Math.sqrt(D)) / (2 * a)].sort(function (x, y) { return x - y; }) };
  }
  function solAns(ex, v) { v = v || 'x'; if (!ex.list && !ex.pm) return 'No real solutions'; if (ex.pm) return M(v + '=' + ex.pm); return ex.list.map(function (t) { return M(v + '=' + t); }).join(' and '); }
  function rnd(x, d) { var s = Math.pow(10, d); return Math.round(x * s + 1e-9) / s; }

  /* ================= GRAPH ================= */
  skill({
    id: 'q-features', best: [0, 1, 2], tag: 'GRAPH', name: 'Features of parabolas',
    blurb: 'Vertex and zeros from a graph, the vertex of y = ax² + bx + c (CP2) → axis of symmetry and maximum or minimum from a graph, the equation of a graphed parabola (CP1) → maximum or minimum and range, axis, vertex and y-intercept from the equation (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 3, 4, 2, 7, 6, 5][ctx.c], steps = [];
      if (c <= 3) { var a = c === 3 ? r.pick([1, -1]) : r.pick([1, -1, 2, -2, F(1, 2), F(-1, 2)]), h = r.int(-4, 4), k = c === 3 ? (Fr.of(a).sign() > 0 ? -r.int(1, 4) : r.int(1, 4)) : r.int(-5, 5);
        if (c === 3) { var root = Math.sqrt(-k / Fr.of(a).val()); need(Number.isInteger(root) && root > 0); }
        var fig = parab(a, h, k), up = Fr.of(a).sign() > 0;
        if (c === 1) { steps.push(step('The vertex is the turning point of the parabola.', pt(h, k), 3));
          return { variant: 'fe1', prompt: 'What is the vertex of the parabola?', fig: fig, parts: [{ answer: M(pt(h, k)), check: { type: 'quad-feature', want: 'vertex' } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
        if (c === 2) { steps.push(step('The axis of symmetry is the vertical line through the vertex.', 'x=' + h, 2), step('The parabola opens ' + (up ? 'up, so the vertex is a minimum.' : 'down, so the vertex is a maximum.'), String(k), 2));
          return { variant: 'fe2', prompt: 'Use the graph of the parabola.', fig: fig, parts: [{ label: 'a', prompt: 'What is the axis of symmetry?', answer: M('x=' + h), check: { type: 'quad-feature', want: 'axis' } }, { label: 'b', prompt: 'Is the vertex a maximum or a minimum? What is that value?', answer: (up ? 'Minimum' : 'Maximum') + ' value ' + M(String(k)), check: { type: 'quad-feature', want: 'maxmin' } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
        steps.push(step('The zeros are where the parabola crosses the x-axis.', 'x=' + (h - root) + ',\\ x=' + (h + root), 3));
        return { variant: 'fe3', prompt: 'What are the zeros of the function graphed?', fig: fig, parts: [{ answer: M('x=' + (h - root)) + ' and ' + M('x=' + (h + root)), check: { type: 'quad-feature', want: 'zeros' } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 7) { var a7 = r.pick([1, -1, 2, -2, F(1, 2), F(-1, 2)]), h7 = r.int(-3, 3), k7 = r.int(-4, 4); need(h7 !== 0); var f7 = parab(a7, h7, k7);
        steps.push(step('Read the vertex from the graph.', pt(h7, k7), 1), step('Use another point on the curve to find a.', 'a=' + num(a7), 2), step('Write the equation in vertex form.', vform(a7, h7, k7), 1));
        return { variant: 'fe7', prompt: 'Write the equation of the parabola in vertex form.', fig: f7, parts: [{ answer: M(vform(a7, h7, k7)), check: { type: 'quad-vertex-eq', form: 'vertex' } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      var A = nz(r, -3, 3), H = r.int(-5, 5), Kk = r.int(-9, 9), B = -2 * A * H, C0 = A * H * H + Kk, eq = 'y=' + quad(A, B, C0); need(B !== 0);
      if (c === 4) { steps.push(step('The x-coordinate of the vertex is ' + M('-\\frac{b}{2a}') + '.', 'x=' + H, 2), step('Substitute to find y.', 'y=' + Kk, 2));
        return { variant: 'fe4', prompt: 'Find the vertex of ' + M(eq) + '.', parts: [{ answer: M(pt(H, Kk)), check: { type: 'quad-feature', want: 'vertex', eq: eq, fn: true } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 5) { steps.push(step(M('x=-\\frac{b}{2a}') + ' gives the axis of symmetry.', 'x=' + H, 2), step('Substitute for the vertex; set x = 0 for the y-intercept.', pt(H, Kk) + ',\\ ' + pt(0, C0), 2));
        return { variant: 'fe5', prompt: 'For ' + M(eq) + ':', parts: [{ label: 'a', prompt: 'Axis of symmetry?', answer: M('x=' + H), check: { type: 'quad-feature', want: 'axis', eq: eq, fn: true } },
          { label: 'b', prompt: 'Vertex?', answer: M(pt(H, Kk)), check: { type: 'quad-feature', want: 'vertex', eq: eq, fn: true } }, { label: 'c', prompt: 'y-intercept?', answer: M(pt(0, C0)), check: { type: 'quad-feature', want: 'yint', eq: eq, fn: true } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      var mx = A < 0;
      steps.push(step('a is ' + (mx ? 'negative: the parabola opens down and has a maximum.' : 'positive: the parabola opens up and has a minimum.'), '', 1), step('The vertex gives the value.', String(Kk), 2), step('The range is every y-value ' + (mx ? 'at or below' : 'at or above') + ' it.', 'y' + (mx ? '\\le ' : '\\ge ') + Kk, 2));
      return { variant: 'fe6', prompt: 'For ' + M(eq) + ':', parts: [{ label: 'a', prompt: 'Does it have a maximum or a minimum value? What is it?', answer: (mx ? 'Maximum' : 'Minimum') + ' value ' + M(String(Kk)), check: { type: 'quad-feature', want: 'maxmin', eq: eq, fn: true } },
        { label: 'b', prompt: 'What is the range?', answer: M('y' + (mx ? '\\le ' : '\\ge ') + Kk), check: { type: 'quad-feature', want: 'range', eq: eq, fn: true } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= ROOTS ================= */
  skill({
    id: 'q-roots', best: [0, 1, 2], tag: 'ROOTS', name: 'Solve by square roots and factoring',
    blurb: 'x² = k, (x − h)² = k, x² = k in simplest radical form (CP2) → ax² + c = d, factoring x² + bx + c (CP1) → (x − h)² = k with radicals, factoring ax² + bx + c (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 4, 5, 2, 3, 6, 7][ctx.c], steps = [], v = r.pick(['x', 'x', 'n', 't']), eq, ex, rad = false;
      if (c === 1) { var s1 = r.int(2, 12); eq = v + '^{2}=' + s1 * s1; ex = exact(1, 0, -s1 * s1); steps.push(step('Take the square root of both sides; remember ±.', v + '=\\pm' + s1, 3)); }
      else if (c === 2) { var a2 = r.int(2, 5), s2 = r.int(1, 8), c2 = nz(r, -20, 20); eq = a2 + v + '^{2}' + (c2 < 0 ? '-' : '+') + Math.abs(c2) + '=' + (a2 * s2 * s2 + c2); ex = exact(a2, 0, -a2 * s2 * s2);
        steps.push(step('Isolate ' + M(v + '^{2}') + '.', v + '^{2}=' + s2 * s2, 2), step('Take square roots (±).', v + '=\\pm' + s2, 2)); }
      else if (c === 3) { var p = nz(r, -9, 9), q = nz(r, -9, 9); need(p !== -q); eq = quad(1, -(p + q), p * q, v) + '=0'; ex = exact(1, -(p + q), p * q);
        steps.push(step('Factor.', '(' + lin([[1, v], [-p, '']]) + ')(' + lin([[1, v], [-q, '']]) + ')=0', 2), step('Set each factor equal to 0.', v + '=' + p + ',\\ ' + v + '=' + q, 2)); }
      else if (c === 4 || c === 6) { var h = nz(r, -8, 8), k4 = c === 4 ? r.pick([1, 4, 9, 16, 25, 36]) : r.pick([2, 3, 5, 6, 7, 8, 12, 18, 20, 27, 28, 45, 50]); rad = c === 6;
        eq = '(' + lin([[1, v], [-h, '']]) + ')^{2}=' + k4; ex = exact(1, -2 * h, h * h - k4);
        steps.push(step('Take square roots of both sides (±).', lin([[1, v], [-h, '']]) + '=\\pm\\sqrt{' + k4 + '}', 2), step('Add ' + h + ' to both sides' + (rad ? ' and simplify the radical.' : '.'), ex.pm ? v + '=' + ex.pm : ex.list.map(function (t) { return v + '=' + t; }).join(',\\ '), 2)); }
      else if (c === 5) { var k5 = r.pick([8, 12, 18, 20, 24, 27, 28, 32, 45, 48, 50, 72, 75, 98]); rad = true; var a5 = r.pick([1, 1, 2, 3]); eq = (a5 === 1 ? '' : a5) + v + '^{2}=' + a5 * k5; ex = exact(1, 0, -k5);
        steps.push(step('Isolate ' + M(v + '^{2}') + ' and take square roots (±).', v + '=\\pm\\sqrt{' + k5 + '}', 2), step('Simplify the radical.', v + '=' + ex.pm, 2)); }
      else { var A = r.int(2, 6), P = nz(r, -7, 7), Q = nz(r, -7, 7); need(gcd(A, Math.abs(P)) === 1); eq = quad(A, -(P + A * Q), P * Q, v) + '=0'; ex = exact(A, -(P + A * Q), P * Q); need(ex.rational && ex.list.length === 2);
        steps.push(step('Factor (ac method).', '(' + lin([[A, v], [-P, '']]) + ')(' + lin([[1, v], [-Q, '']]) + ')=0', 2), step('Set each factor equal to 0.', ex.list.map(function (t) { return v + '=' + t; }).join(',\\ '), 2)); }
      return { variant: 'ro' + c, prompt: 'Solve ' + M(eq) + '.' + (rad ? ' Write exact answers in simplest radical form.' : ''), parts: [{ answer: solAns(ex, v), check: { type: 'quad-solve', eq: eq, v: v, radical: rad || undefined, exact: c === 7 || undefined } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= FORMULA ================= */
  skill({
    id: 'q-formula', best: [0, 1, 2], tag: 'FORMULA', name: 'Discriminant and the quadratic formula',
    blurb: 'The discriminant and the number of real solutions, the formula with whole-number answers (CP2) → rounded answers, exact answers (CP1) → exact answers with a ≠ 1, rewriting in standard form first (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], a = c <= 4 ? r.pick([1, 1, 2, 3, -1]) : r.int(2, 5) * r.sign(), b = nz(r, -9, 9), cc = nz(r, -9, 9), eq = quad(a, b, cc) + '=0', ex = exact(a, b, cc), D = ex.D;
      if (c === 1 || c === 2) {
        if (c === 1) { steps.push(step('Discriminant ' + M('b^{2}-4ac') + '.', '(' + b + ')^{2}-4(' + a + ')(' + cc + ')=' + D, 3));
          return { variant: 'fo1', prompt: 'Find the discriminant of ' + M(eq) + '.', parts: [{ answer: M(String(D)), check: { type: 'quad-disc', want: 'value', eq: eq } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
        var kind = D > 0 ? 'Two' : D === 0 ? 'One' : 'No'; if (r.chance(0.25)) { var s0 = r.int(1, 6) * r.sign(); b = 2 * s0; a = 1; cc = s0 * s0; eq = quad(1, b, cc) + '=0'; D = 0; kind = 'One'; }
        steps.push(step('Find the discriminant.', String(D), 2), step('Positive: two real solutions; zero: one; negative: none.', '', 2));
        return { variant: 'fo2', prompt: 'How many real solutions does ' + M(eq) + ' have? Use the discriminant.', parts: [{ answer: kind + ' real solution' + (kind === 'One' ? '' : 's') + ' (the discriminant is ' + M(String(D)) + ').', check: { type: 'quad-disc', want: 'count', eq: eq } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 3) { var p = nz(r, -8, 8), q = nz(r, -8, 8), aa = r.pick([1, 1, 2]); need(p !== q); a = aa; b = -aa * (p + q); cc = aa * p * q; eq = quad(a, b, cc) + '=0'; ex = exact(a, b, cc); }
      else if (c === 7) { var lhsA = r.int(2, 5), rb = nz(r, -9, 9), rc = nz(r, -9, 9); a = lhsA; b = -rb; cc = -rc; ex = exact(a, b, cc); need(!ex.rational && ex.D > 0); eq = lhsA + 'x^{2}=' + lin([[rb, 'x'], [rc, '']]); }
      need(ex.D > 0 && (c === 3 ? ex.rational : !ex.rational));
      var fx = 'x=\\frac{' + (-b) + '\\pm\\sqrt{' + ex.D + '}}{' + 2 * a + '}';
      steps.push(step(c === 7 ? 'Rewrite in standard form ' + M('ax^{2}+bx+c=0') + '.' : 'Identify a, b and c.', c === 7 ? quad(a, b, cc) + '=0' : 'a=' + a + ',\\ b=' + b + ',\\ c=' + cc, 1),
        step('Substitute into the quadratic formula.', fx, 2), step(c === 4 ? 'Use a calculator and round to the nearest tenth.' : 'Simplify.', c === 4 ? 'x\\approx ' + ex.approx.map(function (z) { return rnd(z, 1); }).join(',\\ ') : (ex.pm ? 'x=' + ex.pm : ex.list.map(function (t) { return 'x=' + t; }).join(',\\ ')), 2));
      if (c === 4) { var rr = ex.approx.map(function (z) { return rnd(z, 1); }); need(rr[0] !== rr[1]);
        return { variant: 'fo4', prompt: 'Solve ' + M(eq) + ' with the quadratic formula. Round to the nearest tenth.', parts: [{ answer: rr.map(function (z) { return M('x\\approx ' + z); }).join(' and '), check: { type: 'quad-solve', eq: eq, round: 1 } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      return { variant: 'fo' + c, prompt: 'Solve ' + M(eq) + ' with the quadratic formula.' + (c === 3 ? '' : ' Write exact answers in simplest radical form.'), parts: [{ answer: solAns(ex), check: { type: 'quad-solve', eq: eq, radical: c === 3 ? undefined : true } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= COMPLETE ================= */
  skill({
    id: 'q-complete', best: [0, 1, 2], tag: 'COMPLETE', name: 'Completing the square and vertex form',
    blurb: 'The number that completes the square, solving by completing the square (CP2) → radical answers, odd b (CP1) → a ≠ 1 equations, vertex form (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = [0, 1, 3, 4, 6, 7, 2, 5][ctx.c], steps = [], hb = nz(r, -9, 9), b = 2 * hb;
      if (c === 1) { var v1 = r.pick(['x', 'n', 'm', 't']), e1 = quad(1, b, 0, v1); steps.push(step('Take half of b and square it.', '\\left(\\frac{' + b + '}{2}\\right)^{2}=' + hb * hb, 3));
        return { variant: 'cs1', prompt: 'What number must be added to ' + M(e1) + ' to make a perfect-square trinomial?', parts: [{ answer: M(String(hb * hb)), check: { type: 'quad-ctsq', expr: e1, v: v1 } }], steps: steps, space: [0.4, 0.6, 0.8] }; }
      if (c === 2 || c === 5) { var a = c === 2 ? 1 : r.pick([2, 3, -1, -2]), k = r.int(-9, 9), h = -hb, eq = 'y=' + quad(a, -2 * a * h, a * h * h + k);
        steps.push(step(c === 2 ? 'Complete the square: add and subtract ' + hb * hb + '.' : 'Factor ' + a + ' out of the x-terms, then complete the square inside.', '', 2), step('Write in vertex form.', vform(a, h, k), 2));
        return { variant: 'cs' + c, prompt: 'Write ' + M(eq) + ' in vertex form ' + M('y=a(x-h)^{2}+k') + '.', parts: [{ answer: M(vform(a, h, k)), check: { type: 'quad-vertex-eq', form: 'vertex', eq: eq, fn: true } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      var A = 1, B = b, Cc, ex;
      if (c === 3) { var t = r.int(1, 8); Cc = hb * hb - t * t; }
      else if (c === 4) { var kk = r.pick([2, 3, 5, 6, 7, 8, 10, 11, 12, 13]); Cc = hb * hb - kk; }
      else if (c === 6) { B = nz(r, -4, 4) * 2 + 1; Cc = nz(r, -9, 9); }
      else { A = r.pick([2, 3]); B = A * nz(r, -4, 4) * 2; Cc = nz(r, -9, 9); }
      ex = exact(A, B, Cc); need(ex.D > 0 && (c === 3 ? ex.rational : !ex.rational)); var eq2 = quad(A, B, Cc) + '=0';
      steps.push(step(A === 1 ? 'Move the constant to the other side.' : 'Divide by ' + A + ' and move the constant.', '', 1), step('Add ' + M('\\left(\\frac{b}{2}\\right)^{2}') + ' to both sides and factor the perfect square.', '', 2), step('Take square roots (±) and solve.', ex.pm ? 'x=' + ex.pm : ex.list.map(function (z) { return 'x=' + z; }).join(',\\ '), 2));
      return { variant: 'cs' + c, prompt: 'Solve ' + M(eq2) + ' by completing the square.' + (ex.rational ? '' : ' Write exact answers in simplest radical form.'), parts: [{ answer: solAns(ex), check: { type: 'quad-solve', eq: eq2, radical: ex.rational ? undefined : true } }], steps: steps, space: [0.8, 1.0, 1.2] };
    }
  });

  /* ================= APPLY ================= */
  skill({
    id: 'q-apply', best: [0, 1, 2], tag: 'APPLY', name: 'Projectile models',
    blurb: 'Height at a time, time of the maximum height (CP2) → maximum height, when it lands (rounded) (CP1) → metric models, multi-part questions (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], metric = c === 6, g = metric ? F(-49, 10) : F(-16), tm = r.int(1, 4) * (metric ? 1 : 1), v0 = metric ? 9.8 * tm : 32 * tm, h0 = r.int(0, 12) * (metric ? 1 : 5);
      var vF = metric ? F(98 * tm, 10) : F(32 * tm), eq = 'h(t)=' + (metric ? '-4.9t^{2}+' + num(vF).replace(/\\frac\{(\d+)\}\{5\}/, function (w, n) { return String(+n / 5); }) + 't' : '-16t^{2}+' + 32 * tm + 't') + (h0 ? '+' + h0 : ''), unit = metric ? 'meters' : 'feet';
      if (metric) eq = 'h(t)=-4.9t^{2}+' + (Math.round(v0 * 10) / 10) + 't' + (h0 ? '+' + h0 : '');
      var hmax = g.mul(tm * tm).add(vF.mul(tm)).add(h0), story = 'A ball is thrown upward. Its height in ' + unit + ' after ' + M('t') + ' seconds is ' + M(eq) + '.', chk = { eq: eq, fn: true, v: 't' };
      var A = Fr.of(g).val(), disc = v0 * v0 - 4 * A * h0, land = (-v0 - Math.sqrt(disc)) / (2 * A);
      function ds(q) { return String(Math.round(Fr.of(q).val() * 1000) / 1000); }
      function part(label, prompt, want, answer, extra) { return { label: label, prompt: prompt, answer: answer, check: Object.assign({ type: 'quad-proj', want: want }, chk, extra || {}) }; }
      if (c === 1) { var t1 = r.int(1, 2 * tm), h1 = g.mul(t1 * t1).add(vF.mul(t1)).add(h0); need(h1.sign() > 0);
        steps.push(step('Substitute ' + M('t=' + t1) + '.', 'h(' + t1 + ')=' + ds(h1), 3));
        return { variant: 'qa1', prompt: story + ' What is its height after ' + t1 + ' second' + (t1 === 1 ? '' : 's') + '?', parts: [part('', '', 'at', M(ds(h1)) + ' ' + unit, { at: t1 })], steps: steps, space: [0.5, 0.7, 0.9] }; }
      var tStep = step('The maximum is at the vertex: ' + M('t=-\\frac{b}{2a}') + '.', 't=' + tm, 2), hStep = step('Substitute that time.', 'h(' + tm + ')=' + ds(hmax), 2), lStep = step('Set h(t) = 0 and use the quadratic formula; keep the positive time.', 't\\approx ' + rnd(land, 2), 2);
      if (c === 2) { steps.push(tStep); return { variant: 'qa2', prompt: story + ' After how many seconds does it reach its maximum height?', parts: [part('', '', 'tmax', M(String(tm)) + (tm === 1 ? ' second' : ' seconds'))], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 3) { steps.push(tStep, hStep); return { variant: 'qa3', prompt: story + ' What is its maximum height?', parts: [part('', '', 'max', M(ds(hmax)) + ' ' + unit)], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 4) { need(h0 > 0); steps.push(lStep); return { variant: 'qa4', prompt: story + ' When does it hit the ground? Round to the nearest hundredth of a second.', parts: [part('', '', 'ground', M(String(rnd(land, 2))) + ' seconds', { round: 2 })], steps: steps, space: [0.7, 0.9, 1.1] }; }
      if (c === 5 || c === 6) { steps.push(tStep, hStep);
        return { variant: 'qa' + c, prompt: story, parts: [part('a', 'When does it reach its maximum height?', 'tmax', M(String(tm)) + (tm === 1 ? ' second' : ' seconds')), part('b', 'What is the maximum height?', 'max', M(ds(hmax)) + ' ' + unit)], steps: steps, space: [0.8, 1.0, 1.2] }; }
      need(h0 > 0 && tm > 1); var t7 = r.int(1, tm - 1); var h7 = g.mul(t7 * t7).add(vF.mul(t7)).add(h0); steps.push(step('Substitute ' + M('t=' + t7) + '.', ds(h7), 1), tStep, hStep, lStep);
      return { variant: 'qa7', prompt: story, parts: [part('a', 'What is its height after ' + t7 + ' second' + (t7 === 1 ? '' : 's') + '?', 'at', M(ds(h7)) + ' ' + unit, { at: t7 }), part('b', 'What is the maximum height?', 'max', M(ds(hmax)) + ' ' + unit), part('c', 'When does it hit the ground? Round to the nearest hundredth.', 'ground', M(String(rnd(land, 2))) + ' seconds', { round: 2 })], steps: steps, space: [1.0, 1.2, 1.4] };
    }
  });

  /* ================= GRAPH · by hand (the key shows the parabola; the verifier reads it back) ================= */
  function blank7() { return { kind: 'plane', xmin: -7, xmax: 7, ymin: -7, ymax: 7, points: [], segs: [], curves: [] }; }
  function sform(a, b, c) { return 'y=' + quad(a, b, c); }
  skill({
    id: 'q-graph', best: [0, 1, 2], tag: 'GRAPH', name: 'Graph a parabola by hand',
    blurb: 'Vertex form with a = 1 (CP2) → opening down, a = 2 or ½, standard form (CP1) → standard form with a ≠ 1, finding the vertex first (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], h = r.int(-3, 3), k = r.int(-4, 4), a = 1;
      if (c === 1) { h = r.int(-6, 6); k = r.int(-7, 4); var pick1 = r.int(0, 2); if (pick1 === 0) h = 0; else if (pick1 === 1) k = 0; else { h = nz(r, -2, 2); k = nz(r, -2, 2); } }
      if (c === 2) need(h !== 0 && k !== 0);
      if (c === 3 || c === 6) a = -1;
      if (c === 4) a = r.pick([2, -2, F(1, 2), F(-1, 2)]);
      if (c === 7) a = r.pick([2, -2]);
      a = Fr.of(a); need(!(h === 0 && k === 0));
      var eq, b = a.mul(-2 * h), cc = a.mul(h * h).add(k);
      if (c >= 5) { need(b.isInt() && cc.isInt()); eq = sform(a, b, cc); steps.push(step('Find the vertex: ⟨x=-\\frac{b}{2a}=' + h + '⟩, then ⟨y=' + k + '⟩.', '', 2)); }
      else eq = vform(a, h, k);
      var y1 = a.add(k), key = parab(a, h, k); key.points = [{ x: h, y: k }];
      need(Math.abs(y1.val()) <= 7);
      steps.push(step('Plot the vertex ' + M(pt(h, k)) + ' and draw the axis of symmetry ' + M('x=' + h) + '.', '', 2));
      steps.push(step('One step left or right of the vertex, ⟨y⟩ changes by ⟨a=' + num(a) + '⟩: plot ' + M(pt(h - 1, y1)) + ' and ' + M(pt(h + 1, y1)) + ', then more points, and draw a smooth curve.', '', 2));
      return { variant: 'qg' + c, prompt: 'Graph ' + M(eq) + '. Label the vertex.', fig: blank7(),
        parts: [{ answer: 'Vertex ' + M(pt(h, k)) + ', axis of symmetry ' + M('x=' + h) + '; it passes through ' + M(pt(h - 1, y1)) + ' and ' + M(pt(h + 1, y1)) + '.', answerFig: key, check: { type: 'quad-graph', eq: eq, fn: true } }], steps: steps, space: [0.5, 0.6, 0.7] };
    }
  });

  /* ================= TRANSFORM · transformations of y = x² in words ================= */
  function moves(a, h, k) {
    var w = [], A = Fr.of(a), aa = A.abs();
    if (A.sign() < 0) w.push('reflected across the x-axis');
    if (!aa.eq(1)) w.push((aa.gt(1) ? 'vertically stretched by a factor of ' : 'vertically compressed by a factor of ') + (aa.isInt() ? String(aa.n) : aa.n + '/' + aa.d));
    var sh = [];
    if (h) sh.push(Math.abs(h) + ' unit' + (Math.abs(h) === 1 ? '' : 's') + (h > 0 ? ' right' : ' left'));
    if (k) sh.push(Math.abs(k) + ' unit' + (Math.abs(k) === 1 ? '' : 's') + (k > 0 ? ' up' : ' down'));
    if (sh.length) w.push('shifted ' + sh.join(' and '));
    return w;
  }
  function joinW(w) { return w.length === 1 ? w[0] : w.slice(0, -1).join(', ') + ' and ' + w[w.length - 1]; }
  skill({
    id: 'q-transform', best: [0, 1, 2], tag: 'TRANSFORM', name: 'Transformations of y = x²',
    blurb: 'Shifts up, down, left and right (CP2) → both shifts, reflections, stretches and compressions (CP1) → write the equation from a description (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], h = nz(r, -6, 6), k = nz(r, -8, 8), a = F(1);
      if (c === 1) { h = 0; k = nz(r, -15, 15); } if (c === 2) { k = 0; h = nz(r, -14, 14); }
      if (c === 4 || c === 6) a = F(-1);
      if (c === 5 || c === 7) a = F(r.pick([2, 3, 4, -2, -3])); if (c === 5 && r.chance(0.4)) a = F(r.pick([1, -1]), r.pick([2, 3, 4]));
      var eq = vform(a, h, k), w = moves(a, h, k);
      if (c <= 5) {
        steps.push(step('Compare with ⟨y=a(x-h)^2+k⟩: ⟨a=' + num(a) + '⟩, ⟨h=' + h + '⟩, ⟨k=' + k + '⟩.', '', 2));
        steps.push(step('⟨h⟩ moves the graph right (positive) or left (negative); ⟨k⟩ moves it up or down' + (a.eq(1) ? '.' : '; ⟨a⟩ reflects and stretches it.'), '', 2));
        var ansW = joinW(w); ansW = ansW.charAt(0).toUpperCase() + ansW.slice(1) + '.';
        return { variant: 'qt' + c, prompt: 'Describe how the graph of ' + M(eq) + ' is related to the graph of ' + M('y=x^{2}') + '.', parts: [{ answer: ansW, check: { type: 'quad-transform', eq: eq, want: 'describe' } }], steps: steps, space: [0.4, 0.5, 0.6] };
      }
      steps.push(step('A shift right ⟨h⟩ gives ⟨(x-h)⟩; a shift up ⟨k⟩ adds ⟨k⟩; a reflection makes ⟨a⟩ negative.', '', 2), step('The equation:', eq, 2));
      return { variant: 'qt' + c, prompt: 'The graph of ' + M('y=x^{2}') + ' is ' + joinW(w) + '. Write the equation of the new graph in vertex form.', parts: [{ answer: M(eq), check: { type: 'quad-transform', want: 'equation' } }], steps: steps, space: [0.5, 0.6, 0.7] };
    }
  });

  /* ================= MODEL · fitting a quadratic to data ================= */
  var QCTX = [['Time (s)', 'Height (ft)'], ['Price ($)', 'Profit ($)'], ['Speed (mph)', 'Fuel use'], ['Day', 'Visitors']];
  function rH(x) { return Math.round(x * 100 + (x < 0 ? -1e-9 : 1e-9)) / 100; }
  function fmtC(v) { var x = rH(v); return (x < 0 ? '-' : '') + String(Math.abs(x)); }
  function quadReg(pts) {   // least squares: solve the 3×3 normal equations
    var S = [0, 0, 0, 0, 0], T = [0, 0, 0]; pts.forEach(function (p) { var x = p[0], y = p[1], xp = 1; for (var i = 0; i < 5; i++) { S[i] += xp; if (i < 3) T[i] += xp * y; xp *= x; } });
    var A = [[S[4], S[3], S[2], T[2]], [S[3], S[2], S[1], T[1]], [S[2], S[1], S[0], T[0]]];
    for (var i = 0; i < 3; i++) { var piv = i; for (var j = i + 1; j < 3; j++) if (Math.abs(A[j][i]) > Math.abs(A[piv][i])) piv = j; var tmp = A[i]; A[i] = A[piv]; A[piv] = tmp;
      for (var j2 = 0; j2 < 3; j2++) if (j2 !== i) { var f = A[j2][i] / A[i][i]; for (var k = i; k < 4; k++) A[j2][k] -= f * A[i][k]; } }
    return [A[0][3] / A[0][0], A[1][3] / A[1][1], A[2][3] / A[2][2]];
  }
  function safeH(x) { var f = x * 100 - Math.floor(x * 100); return Math.abs(f - 0.5) > 1e-6; }
  skill({
    id: 'q-fit', best: [1, 2], tag: 'MODEL', name: 'Quadratic models and regression',
    blurb: 'The quadratic through three points that include the y-intercept (CP2) → three points anywhere (CP1) → quadratic regression with a calculator, and predictions from it (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], cx = r.pick(QCTX), pts = [], fig;
      if (c <= 3) {
        var a = nz(r, -4, 4), b = c === 1 ? 0 : r.int(-6, 6), cc = r.int(-9, 9), xsP = c <= 2 ? [-1, 0, 1] : r.shuffle([-3, -2, -1, 1, 2, 3]).slice(0, 2).concat([0]);
        if (c === 3) xsP = [r.int(-3, -1), r.int(1, 2), r.int(3, 4)];
        xsP.sort(function (p, q) { return p - q; }); xsP.forEach(function (x) { pts.push([x, a * x * x + b * x + cc]); });
        fig = { kind: 'table', vertical: true, head: ['x', 'y'], rows: pts };
        steps.push(step('Substitute each point into ⟨y=ax^2+bx+c⟩ to get three equations.', '', 2), step('Solve the system for ⟨a⟩, ⟨b⟩ and ⟨c⟩.', sform(a, b, cc), 3));
        return { variant: 'qf' + c, prompt: 'Find the equation ' + M('y=ax^{2}+bx+c') + ' of the parabola through the points in the table.', fig: fig,
          parts: [{ answer: M(sform(a, b, cc)), check: { type: 'quad-fit', want: 'exact' } }], steps: steps, space: [1.2, 1.5, 1.8] };
      }
      var A0 = -r.pick([0.5, 1, 1.5, 2, 2.5, 3]), x0 = r.int(3, 6), y0 = r.int(20, 60), n = r.int(6, 8);
      for (var i = 0; i < n; i++) { var x = i + 1, y = A0 * (x - x0) * (x - x0) + y0 + r.int(-2, 2); pts.push([x, y]); }
      var co = quadReg(pts); need(co.every(safeH) && Math.abs(co[0]) > 0.05);
      fig = { kind: 'table', vertical: true, head: cx, rows: pts };
      var cf = function (v, first) { var x = rH(v), ab = Math.abs(x), body = ab === 1 ? '' : String(ab); return (first ? (x < 0 ? '-' : '') : (x < 0 ? '-' : '+')) + body; };
      need(rH(co[1]) !== 0 && rH(co[2]) !== 0);
      var ln = 'y=' + cf(co[0], true) + 'x^{2}' + cf(co[1]) + 'x' + (rH(co[2]) < 0 ? '-' : '+') + Math.abs(rH(co[2]));
      steps.push(step('Enter the data in two lists and run quadratic regression (QuadReg).', '', 2), step('Round each coefficient to the nearest hundredth.', ln, 3));
      var parts = [{ label: c >= 6 ? 'a' : '', answer: M(ln), check: { type: 'quad-fit', want: 'reg' } }];
      if (c >= 6) { var xp = n + (c === 7 ? 2 : 1), yp = rH(co[0]) * xp * xp + rH(co[1]) * xp + rH(co[2]), yr = Math.round(yp * 10) / 10; need(Math.abs(yp * 10 - Math.floor(yp * 10) - 0.5) > 1e-6);
        parts.push({ label: 'b', answer: 'y ≈ ' + M(String(yr)), check: { type: 'quad-fit', want: 'predict', at: 'x=' + xp } });
        steps.push(step('Substitute ⟨x=' + xp + '⟩ into the rounded model.', 'y\\approx ' + yr, 2)); }
      if (!parts[0].label) delete parts[0].label;
      return { variant: 'qf' + c, prompt: 'Use quadratic regression on a calculator to find a model ' + M('y=ax^{2}+bx+c') + ' for the data. Round each coefficient to the nearest hundredth.' + (c >= 6 ? ' Then use your rounded model to predict ⟨y⟩ when ' + M('x=' + (n + (c === 7 ? 2 : 1))) + ', to the nearest tenth.' : ''), fig: fig, parts: parts, steps: steps, space: [1.0, 1.3, 1.6] };
    }
  });


  // Lesson-specific aliases of independently verified generators; these remain selectable skills.
  (function(){var base=skills.find(function(s){return s.id==="q-graph";});if(!base)return;
    skill({id:"quadratic-graphing",best:base.best,tag:base.tag,name:"Plot a quadratic from its equation",blurb:"Graph a quadratic with its vertex and symmetric points.",
      difficultyProfile:'focused',fixedDifficulty:3,generate:function(ctx){return base.generate(Object.assign({},ctx,{c:3}));}});
  })();
  (function(){var parent=skills.find(function(s){return s.id==="q-roots";});if(parent)skill({id:"quadratic-solve-factoring",best:parent.best,tag:parent.tag,name:"Solve quadratics by factoring",blurb:"Factor a quadratic equation and use the zero product property.",difficultyProfile:'focused',fixedDifficulty:5,generate:function(ctx){return parent.generate(Object.assign({},ctx,{c:5}));}});})();
  NS.registerSkillSet({
    id: 'algebra1-quadratics', course: 'algebra1', courseName: 'Algebra 1', unit: 'quadratics', unitName: 'Quadratic Functions and Equations',
    title: 'The Parabola Bakery',
    tags: { GRAPH: 'Features of parabolas', ROOTS: 'Square roots and factoring', FORMULA: 'Quadratic formula', COMPLETE: 'Completing the square', APPLY: 'Projectile models', TRANSFORM: 'Transformations', MODEL: 'Quadratic models' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Vertex</h4><p>⟨y=ax^{2}+bx+c⟩: axis ⟨x=-\\frac{b}{2a}⟩. Vertex form ⟨y=a(x-h)^{2}+k⟩ has vertex ⟨(h,\\ k)⟩.</p></section>' +
      '<section><h4>Quadratic formula</h4><p>⟨x=\\frac{-b\\pm\\sqrt{b^{2}-4ac}}{2a}⟩. Discriminant ⟨b^{2}-4ac⟩: positive two, zero one, negative none.</p></section>' +
      '<section><h4>Completing the square</h4><p>Add ⟨\\left(\\frac{b}{2}\\right)^{2}⟩ to ⟨x^{2}+bx⟩.</p></section>' +
      '<section><h4>Projectiles</h4><p>⟨h(t)=-16t^{2}+v_{0}t+h_{0}⟩ (feet) or ⟨-4.9t^{2}+v_{0}t+h_{0}⟩ (meters).</p></section>' +
      '</div>',
    gaps: ['A parabola drawn by a student is checked against the key graph by the teacher.'],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
