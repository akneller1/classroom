/* Menu Assessment Generator — Algebra 1 · Unit 5 Linear Functions and Graphing (roadmap days 57–75).
   Skill groups: SLOPE (slope from points, graphs and tables), FORMS (slope-intercept, point-slope and standard form,
   intercepts), WRITE (writing equations of lines), PARPERP (parallel and perpendicular lines), APPLY (linear models).
   The verifier rebuilds every line from what is printed and compares lines as sets of points, then checks the form. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, M = K.M, num = K.num, lin = K.lin, Fr = K.Fr;
  var need = K.need, nz = K.nz, step = K.step, F = K.F, gcd = K.gcd;
  var skills = [];
  function skill(d) { skills.push(d); return d; }
  function pt(x, y) { return '(' + num(x) + ',\\ ' + num(y) + ')'; }
  function two(a, b) { return pt(a[0], a[1]) + ',\\ ' + pt(b[0], b[1]); }
  function plane(win, extra) { return Object.assign({ kind: 'plane', xmin: win[0], xmax: win[1], ymin: win[2], ymax: win[3], points: [], segs: [], curves: [] }, extra || {}); }
  /* m and b as fractions → "y = mx + b" */
  function si(m, b) { m = Fr.of(m); b = Fr.of(b); return 'y=' + (m.isZero() ? num(b) : lin([[m, 'x'], [b, '']])); }
  function mcoef(m) { m = Fr.of(m); return m.eq(1) ? '' : m.eq(-1) ? '-' : num(m); }
  function ps(m, h, k) { h = Fr.of(h); k = Fr.of(k); return 'y' + (k.isZero() ? '' : (k.sign() < 0 ? '+' : '-') + num(k.abs())) + '=' + mcoef(m) + '(x' + (h.isZero() ? '' : (h.sign() < 0 ? '+' : '-') + num(h.abs())) + ')'; }
  /* standard form Ax + By = C with integers, A ≥ 0, gcd 1, for the line y = mx + b */
  function stdForm(m, b) {
    m = Fr.of(m); b = Fr.of(b); var L = m.d * b.d / gcd(m.d, b.d), A = m.neg().mul(L), B = F(L), Cc = b.mul(L);
    var a = A.n / A.d, bb = B.n / B.d, c = Cc.n / Cc.d, g = gcd(gcd(Math.abs(a), Math.abs(bb)), Math.abs(c)) || 1; a /= g; bb /= g; c /= g;
    if (a < 0 || (a === 0 && bb < 0)) { a = -a; bb = -bb; c = -c; }
    return lin([[a, 'x'], [bb, 'y']]) + '=' + num(c);
  }
  function slopeFrac(r, c) { if (c <= 2) return F(nz(r, -6, 6)); var d = r.pick([2, 3, 4]); var n = nz(r, -7, 7); need(gcd(Math.abs(n), d) === 1); return F(n, d); }

  /* ================= SLOPE ================= */
  skill({
    id: 'slope', best: [0, 1], tag: 'SLOPE', name: 'Find slope',
    blurb: 'Slope from two points, including fraction, zero and undefined slopes (CP2) → slope from a table or a graph (CP1) → a missing coordinate, are three points on one line? (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], A, B, m;
      if (c <= 3) {
        A = [r.int(-8, 6), r.int(-8, 8)];
        if (c === 3 && r.chance(0.5)) { B = r.chance(0.5) ? [A[0], A[1] + nz(r, -9, 9)] : [A[0] + nz(r, -9, 9), A[1]]; }
        else { var dx = r.int(1, 6) * (c === 1 ? 1 : r.sign()); m = c === 1 ? F(r.int(1, 5)) : slopeFrac(r, c === 2 ? 3 : 4); var dy = m.mul(dx); need(dy.isInt()); B = [A[0] + dx, A[1] + dy.n]; }
        var P = two(A, B), vert = A[0] === B[0];
        steps.push(step('Slope = change in y ÷ change in x.', '\\frac{' + num(B[1]) + '-' + (A[1] < 0 ? '(' + A[1] + ')' : A[1]) + '}{' + num(B[0]) + '-' + (A[0] < 0 ? '(' + A[0] + ')' : A[0]) + '}', 2),
          step(vert ? 'The change in x is 0: the slope is undefined (a vertical line).' : 'Simplify.', vert ? '' : 'm=' + num(F(B[1] - A[1], B[0] - A[0])), 2));
        return { variant: 'sl' + c, prompt: 'Find the slope of the line through ' + M(P) + '.', parts: [{ answer: vert ? 'Undefined' : M('m=' + num(F(B[1] - A[1], B[0] - A[0]))), check: { type: 'slope', src: { pairs: P } } }], steps: steps, space: [0.5, 0.7, 0.9] };
      }
      if (c === 5) { m = slopeFrac(r, 4); var x0 = r.int(-6, -1), y0 = r.int(-5, 5), run = m.d * r.int(1, 2) * (Math.abs(m.n) > 3 ? 1 : 2), x1 = x0 + run, y1 = y0 + m.mul(run).n / m.mul(run).d; need(Math.abs(y1) <= 6 && x1 <= 6 && Number.isInteger(y1));
        var fig = plane([-7, 7, -7, 7], { segs: [{ a: [x0, y0], b: [x1, y1], aEnd: 'arrow', bEnd: 'arrow' }], points: [{ x: x0, y: y0 }, { x: x1, y: y1 }] });
        steps.push(step('Count rise and run between the marked points.', 'm=\\frac{' + (y1 - y0) + '}{' + (x1 - x0) + '}=' + num(m), 3));
        return { variant: 'sl5', prompt: 'Find the slope of the line.', fig: fig, parts: [{ answer: M('m=' + num(m)), check: { type: 'slope', src: { fig: true } } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 4) { m = slopeFrac(r, 5); var xs = [r.int(-6, 0)]; for (var i = 0; i < 3; i++) xs.push(xs[i] + m.d * r.int(1, 2)); var b0 = r.int(-9, 9), rows = xs.map(function (x) { return [x, m.mul(x).add(b0)]; }); need(rows.every(function (rw) { return rw[1].isInt(); }));
        var tfig = { kind: 'table', head: ['x', 'y'], rows: rows.map(function (rw) { return [rw[0], rw[1].n]; }) };
        steps.push(step('Pick two rows: change in y ÷ change in x.', 'm=' + num(m), 3));
        return { variant: 'sl4', prompt: 'The table shows points on a line. Find its slope.', fig: tfig, parts: [{ answer: M('m=' + num(m)), check: { type: 'slope', src: { fig: true } } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 6) { m = slopeFrac(r, 5); var x1b = r.int(-5, 5), x2b = x1b + m.d * nz(r, -3, 3), y2b = r.int(-9, 9), k = Fr.of(y2b).sub(m.mul(x2b - x1b)); need(k.isInt());
        var mT = num(m), pB = pt(x2b, y2b);
        steps.push(step('Use the slope formula with the unknown y-value k.', '\\frac{' + y2b + '-k}{' + x2b + '-' + (x1b < 0 ? '(' + x1b + ')' : x1b) + '}=' + mT, 2), step('Solve for k.', 'k=' + num(k), 2));
        return { variant: 'sl6', prompt: 'The line through ' + M('(' + x1b + ',\\ k)') + ' and ' + M(pB) + ' has slope ' + M(mT) + '. Find ' + M('k') + '.', parts: [{ answer: M('k=' + num(k)), check: { type: 'slope', want: 'missing', m: mT, x1: String(x1b), x2: String(x2b), y2: String(y2b) } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      m = slopeFrac(r, 5); var a0 = [r.int(-6, 0), r.int(-6, 6)], d1 = m.d * r.int(1, 2), d2 = m.d * r.int(1, 3), on = r.chance(0.5);
      var p1 = [a0[0] + d1, m.mul(d1).add(a0[1])], p2 = [a0[0] + d1 + d2, m.mul(d1 + d2).add(a0[1]).add(on ? 0 : r.pick([-1, 1, 2]))]; need(p1[1].isInt() && p2[1].isInt());
      var pts3 = pt(a0[0], a0[1]) + ',\\ ' + pt(p1[0], p1[1]) + ',\\ ' + pt(p2[0], p2[1]);
      steps.push(step('Find the slope between the first two points and between the last two.', '', 2), step(on ? 'The slopes are equal, so the points are on one line.' : 'The slopes are different, so the points are not on one line.', '', 2));
      return { variant: 'sl7', prompt: 'Do the points ' + M(pts3) + ' lie on one line? Explain using slopes.', parts: [{ answer: on ? 'Yes: the slope between each pair of points is ' + M(num(m)) + '.' : 'No: the slopes between the pairs of points are different.', check: { type: 'slope', want: 'collinear', pts: pts3 } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= FORMS ================= */
  skill({
    id: 'forms', best: [0, 1, 2], tag: 'FORMS', name: 'Slope-intercept, point-slope and standard form',
    blurb: 'Slope and y-intercept of y = mx + b (CP2) → from point-slope form, standard form to slope-intercept (CP1) → slope-intercept to standard form, x- and y-intercepts, fractions (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], m = slopeFrac(r, c <= 3 ? 1 : c), b = c <= 3 ? nz(r, -9, 9) : F(nz(r, -9, 9), c >= 7 ? r.pick([1, 2, 3]) : 1);
      var eqSI = si(m, b);
      if (c <= 2) { var eq1 = c === 1 ? eqSI : 'y=' + num(b) + (m.sign() < 0 ? '-' : '+') + (m.abs().eq(1) ? '' : num(m.abs())) + 'x';
        steps.push(step('In ' + M('y=mx+b') + ', m is the slope and b is the y-intercept.', '', 2));
        return { variant: 'fm' + c, prompt: 'For ' + M(eq1) + ':', parts: [{ label: 'a', prompt: 'What is the slope?', answer: M('m=' + num(m)), check: { type: 'slope', src: { eq: eq1 } } },
          { label: 'b', prompt: 'What is the y-intercept?', answer: M(pt(0, b)), check: { type: 'intercepts', want: 'y', src: { eq: eq1 } } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 3) { var h = nz(r, -6, 6), k = nz(r, -6, 6), eq3 = ps(m, h, k);
        steps.push(step('In ' + M('y-y_1=m(x-x_1)') + ', m is the slope and ' + M('(x_1,\\ y_1)') + ' is a point.', '', 2));
        return { variant: 'fm3', prompt: 'For ' + M(eq3) + ':', parts: [{ label: 'a', prompt: 'What is the slope?', answer: M('m=' + num(m)), check: { type: 'slope', src: { eq: eq3 } } },
          { label: 'b', prompt: 'Write the equation in slope-intercept form.', answer: M(si(m, F(k).sub(m.mul(h)))), check: { type: 'line-eq', form: 'slope-intercept', src: { eq: eq3 } } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      var std = stdForm(m, b);
      if (c === 4) { steps.push(step('Solve the equation for y.', eqSI, 3));
        return { variant: 'fm4', prompt: 'For ' + M(std) + ':', parts: [{ label: 'a', prompt: 'Write it in slope-intercept form.', answer: M(eqSI), check: { type: 'line-eq', form: 'slope-intercept', src: { eq: std } } },
          { label: 'b', prompt: 'What is the y-intercept?', answer: M(pt(0, b)), check: { type: 'intercepts', want: 'y', src: { eq: std } } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      if (c === 5) { steps.push(step('Move the x-term to the left side.', '', 1), step('Clear fractions and make the x-coefficient positive.', std, 2));
        return { variant: 'fm5', prompt: 'Write ' + M(eqSI) + ' in standard form ' + M('Ax+By=C') + ' (integers, ' + M('A\\ge 0') + ').', parts: [{ answer: M(std), check: { type: 'line-eq', form: 'standard', src: { eq: eqSI } } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 6) { var Ai = r.int(1, 9), Bi = nz(r, -9, 9), xi = nz(r, -6, 6), Ci = Ai * xi; need(Ci % Bi === 0 && gcd(gcd(Ai, Math.abs(Bi)), Math.abs(Ci)) === 1); var eq6 = lin([[Ai, 'x'], [Bi, 'y']]) + '=' + num(Ci);
        steps.push(step('x-intercept: set y = 0 and solve.', pt(xi, 0), 2), step('y-intercept: set x = 0 and solve.', pt(0, Ci / Bi), 2));
        return { variant: 'fm6', prompt: 'Find the intercepts of ' + M(eq6) + '.', parts: [{ label: 'a', prompt: 'x-intercept', answer: M(pt(xi, 0)), check: { type: 'intercepts', want: 'x', src: { eq: eq6 } } },
          { label: 'b', prompt: 'y-intercept', answer: M(pt(0, Ci / Bi)), check: { type: 'intercepts', want: 'y', src: { eq: eq6 } } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      var h7 = nz(r, -6, 6), k7 = nz(r, -6, 6), eq7 = ps(m, h7, k7), b7 = F(k7).sub(m.mul(h7));
      steps.push(step('Distribute and solve for y.', si(m, b7), 2), step('Rewrite with integer coefficients.', stdForm(m, b7), 2));
      return { variant: 'fm7', prompt: 'For ' + M(eq7) + ':', parts: [{ label: 'a', prompt: 'Write it in slope-intercept form.', answer: M(si(m, b7)), check: { type: 'line-eq', form: 'slope-intercept', src: { eq: eq7 } } },
        { label: 'b', prompt: 'Write it in standard form ' + M('Ax+By=C') + ' (integers, ' + M('A\\ge 0') + ').', answer: M(stdForm(m, b7)), check: { type: 'line-eq', form: 'standard', src: { eq: eq7 } } }], steps: steps, space: [0.8, 1.0, 1.2] };
    }
  });

  /* ================= WRITE ================= */
  skill({
    id: 'write-line', best: [0, 1, 2], tag: 'WRITE', name: 'Write the equation of a line',
    blurb: 'Given slope and y-intercept, horizontal and vertical lines, slope and a point (CP2) → two points, a graph (CP1) → point-slope form, fraction slopes in standard form (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], m = slopeFrac(r, c <= 4 ? 2 : c), b = nz(r, -9, 9), x1 = nz(r, -6, 6), y1 = m.mul(x1).add(b);
      if (c === 1) { var mT = num(m); steps.push(step('Substitute m and b into ' + M('y=mx+b') + '.', si(m, b), 2));
        return { variant: 'wl1', prompt: 'Write the equation of the line with slope ' + M(mT) + ' and y-intercept ' + M(num(b)) + '.', parts: [{ answer: M(si(m, b)), check: { type: 'line-eq', form: 'slope-intercept', src: { m: mT, yint: num(b) } } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 2) { var hx = nz(r, -7, 7), hy = nz(r, -7, 7), P6 = pt(hx, hy), vert = r.chance(0.5);
        steps.push(step(vert ? 'A vertical line has the same x-value at every point.' : 'A horizontal line has the same y-value at every point.', vert ? 'x=' + hx : 'y=' + hy, 3));
        return { variant: 'wl2', prompt: 'Write the equation of the ' + (vert ? 'vertical' : 'horizontal') + ' line through ' + M(P6) + '.', parts: [{ answer: M(vert ? 'x=' + num(hx) : 'y=' + num(hy)), check: { type: 'line-eq', form: 'slope-intercept', src: { slope: vert ? 'undefined' : '0', point: P6 } } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 3) { need(y1.isInt() && Math.abs(y1.n) <= 20); var P = pt(x1, y1.n);
        steps.push(step('Substitute the point into ' + M('y=mx+b') + ' to find b.', num(y1) + '=' + num(m) + '(' + num(x1) + ')+b', 2), step('Write the equation.', si(m, b), 2));
        return { variant: 'wl3', prompt: 'Write the equation of the line with slope ' + M(num(m)) + ' through ' + M(P) + ', in slope-intercept form.', parts: [{ answer: M(si(m, b)), check: { type: 'line-eq', form: 'slope-intercept', src: { slope: num(m), point: P } } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 4 || c === 7) { var x2 = x1 + m.d * nz(r, -3, 3), y2 = m.mul(x2).add(b); need(y1.isInt() && y2.isInt() && (c === 7 || Math.max(Math.abs(y1.n), Math.abs(y2.n)) <= 24)); var PP = two([x1, y1.n], [x2, y2.n]);
        steps.push(step('Slope from the two points.', 'm=' + num(m), 2), step('Find b using one point.', 'b=' + num(b), 1), step(c === 7 ? 'Rewrite in standard form with integers.' : 'Write the equation.', c === 7 ? stdForm(m, b) : si(m, b), 1));
        if (c === 4) return { variant: 'wl4', prompt: 'Write the equation of the line through ' + M(PP) + ' in slope-intercept form.', parts: [{ answer: M(si(m, b)), check: { type: 'line-eq', form: 'slope-intercept', src: { pairs: PP } } }], steps: steps, space: [0.7, 0.9, 1.1] };
        need(!m.isInt());
        return { variant: 'wl7', prompt: 'Write the equation of the line through ' + M(PP) + ' in standard form ' + M('Ax+By=C') + ' (integers, ' + M('A\\ge 0') + ').', parts: [{ answer: M(stdForm(m, b)), check: { type: 'line-eq', form: 'standard', src: { pairs: PP } } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      if (c === 5) { var mm = slopeFrac(r, 4), x0 = r.int(-6, -1), y0 = r.int(-5, 5), run = mm.d * (Math.abs(mm.n) > 3 ? 1 : 2), xe = x0 + run, ye = y0 + mm.mul(run).n / mm.mul(run).d; need(xe <= 6 && Math.abs(ye) <= 6 && Number.isInteger(ye));
        var bb = Fr.of(y0).sub(mm.mul(x0)); need(bb.isInt() && Math.abs(bb.n) <= 7);
        var fig = plane([-7, 7, -7, 7], { segs: [{ a: [x0, y0], b: [xe, ye], aEnd: 'arrow', bEnd: 'arrow' }], points: [{ x: x0, y: y0 }, { x: xe, y: ye }] });
        steps.push(step('Read the slope (rise over run) and the y-intercept from the graph.', 'm=' + num(mm) + ',\\ b=' + num(bb), 2), step('Write the equation.', si(mm, bb), 2));
        return { variant: 'wl5', prompt: 'Write the equation of the line in slope-intercept form.', fig: fig, parts: [{ answer: M(si(mm, bb)), check: { type: 'line-eq', form: 'slope-intercept', src: { fig: true } } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      need(y1.isInt()); var P5 = pt(x1, y1.n);
      steps.push(step('Substitute the slope and the point into ' + M('y-y_1=m(x-x_1)') + '.', ps(m, x1, y1), 3));
      return { variant: 'wl6', prompt: 'Write the equation of the line with slope ' + M(num(m)) + ' through ' + M(P5) + ' in point-slope form.', parts: [{ answer: M(ps(m, x1, y1)), check: { type: 'line-eq', form: 'point-slope', point: P5, src: { slope: num(m), point: P5 } } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= PARPERP ================= */
  skill({
    id: 'parperp', best: [1, 2], tag: 'PARPERP', name: 'Parallel and perpendicular lines',
    blurb: 'Slopes of parallel and perpendicular lines (CP2) → parallel, perpendicular or neither, a parallel line through a point (CP1) → a perpendicular line through a point, lines in standard form (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], m = slopeFrac(r, c <= 2 ? 1 : 5), b = nz(r, -9, 9), eq = si(m, b);
      var perpM = Fr.of(-1).div(m);
      if (c <= 2) { var perp = c === 2;
        steps.push(step(perp ? 'Perpendicular slopes are opposite reciprocals.' : 'Parallel lines have equal slopes.', 'm=' + num(perp ? perpM : m), 3));
        return fixPt(r, eq, perp, m, perpM, steps); }
      if (c === 3) { var kind = r.pick(['parallel', 'perpendicular', 'neither']), m2 = kind === 'parallel' ? m : kind === 'perpendicular' ? perpM : m.add(r.pick([1, -1, 2])), b2 = nz(r, -9, 9); need(b2 !== b && !(kind !== 'perpendicular' && m2.eq(m) && b2 === b));
        need(kind !== 'neither' || (!m2.eq(m) && !m2.mul(m).eq(-1)));
        var eq2 = r.chance(0.5) ? si(m2, b2) : stdForm(m2, b2);
        steps.push(step('Find both slopes: ' + M(num(m)) + ' and ' + M(num(m2)) + '.', '', 2), step('Equal: parallel. Product −1: perpendicular. Otherwise: neither.', '', 2));
        return { variant: 'pp3', prompt: 'Are the lines ' + M(eq) + ' and ' + M(eq2) + ' parallel, perpendicular, or neither?', parts: [{ answer: kind.charAt(0).toUpperCase() + kind.slice(1), check: { type: 'slope', want: 'relation', eqs: [eq, eq2] } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      var x1 = nz(r, -6, 6), perp4 = c >= 5, mN = perp4 ? perpM : m, y1 = nz(r, -8, 8), bN = Fr.of(y1).sub(mN.mul(x1)), P = pt(x1, y1), given = c >= 6 ? stdForm(m, b) : eq;
      if (ctx.intOnly) need(bN.isInt()); need(perp4 || !bN.eq(b));
      var std = c === 7;
      steps.push(step((perp4 ? 'Perpendicular' : 'Parallel') + ' slope: ' + M(num(mN)) + '.', '', 2), step('Use the point to find b.', 'b=' + num(bN), 1), step('Write the equation.', std ? stdForm(mN, bN) : si(mN, bN), 1));
      return { variant: 'pp' + c, prompt: 'Write the equation of the line through ' + M(P) + ' that is ' + (perp4 ? 'perpendicular' : 'parallel') + ' to ' + M(given) + (std ? ', in standard form ' + M('Ax+By=C') + ' (integers, ' + M('A\\ge 0') + ').' : ', in slope-intercept form.'),
        parts: [{ answer: M(std ? stdForm(mN, bN) : si(mN, bN)), check: { type: 'line-eq', form: std ? 'standard' : 'slope-intercept', src: { [perp4 ? 'perp' : 'parallel']: given, point: P } } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });
  /* slope of a parallel/perpendicular line: the verifier needs a printed point, so ask through a point and report the slope */
  function fixPt(r, eq, perp, m, perpM, steps) {
    var x = nz(r, -5, 5), y = nz(r, -5, 5), P = pt(x, y), key = perp ? 'perp' : 'parallel', src = { point: P }; src[key] = eq;
    return { variant: 'pp' + (perp ? 2 : 1), prompt: 'A line passes through ' + M(P) + ' and is ' + (perp ? 'perpendicular' : 'parallel') + ' to ' + M(eq) + '. What is its slope?', parts: [{ answer: M('m=' + num(perp ? perpM : m)), check: { type: 'slope', src: src } }], steps: steps, space: [0.5, 0.7, 0.9] };
  }

  /* ================= APPLY · linear models ================= */
  var JOBS = [['A plumber charges a {b} dollar visit fee plus {m} dollars per hour.', 'hours', 'the cost in dollars', 'x', 'y', 'up'], ['A gym charges a {b} dollar sign-up fee plus {m} dollars per month.', 'months', 'the total cost in dollars', 'x', 'y', 'up'],
    ['A pool holds {b} gallons of water and drains {m} gallons per minute.', 'minutes', 'the gallons left', 'x', 'y', 'down', 'are'], ['A candle is {b} cm tall and burns {m} cm per hour.', 'hours', 'the height in cm', 'x', 'y', 'down'],
    ['Maya has {b} dollars saved and adds {m} dollars each week.', 'weeks', 'her savings in dollars', 'x', 'y', 'up', 'are']];
  skill({
    id: 'line-model', best: [0, 1, 2], tag: 'APPLY', name: 'Linear models and rate of change',
    blurb: 'Find a value from words, write the model, when does it reach a value (CP2) → interpret slope and intercept (CP1) → models from two data points, predictions, multi-part (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], j = r.pick(JOBS), down = j[5] === 'down', mv = down ? r.int(2, 9) : r.int(5, 40), bv = down ? r.int(4, 12) * 10 * (j[0].indexOf('gallons') >= 0 ? 10 : 1) : r.int(2, 12) * 5;
      var text = j[0].replace('{b}', bv).replace('{m}', mv), slope = down ? -mv : mv, rule = 'y=' + lin([[slope, 'x'], [bv, '']]), vars = ' Let ' + M('x') + ' be the number of ' + j[1] + ' and ' + M('y') + ' be ' + j[2] + '.';
      if (c === 1) { var x1 = r.int(2, 9), v1 = slope * x1 + bv; need(v1 >= 0);
        steps.push(step('Start with ' + bv + ' and ' + (down ? 'subtract ' : 'add ') + mv + ' for each of the ' + x1 + ' ' + j[1] + '.', bv + (down ? '-' : '+') + mv + '\\cdot ' + x1 + '=' + v1, 3));
        return { variant: 'lm1', prompt: text + ' Find ' + j[2].replace(/^her /, 'her ') + ' after ' + x1 + ' ' + j[1] + '.', parts: [{ answer: M(String(v1)), check: { type: 'line-apply', want: 'value', start: 0, rate: 1, at: 2 } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 2) { steps.push(step('The starting amount is b; the rate per ' + j[1].slice(0, -1) + ' is m' + (down ? ' (negative, because it goes down)' : '') + '.', rule, 3));
        return { variant: 'lm2', prompt: text + vars + ' Write an equation for ' + M('y') + '.', parts: [{ answer: M(rule), check: { type: 'line-apply', want: 'equation', start: 0, rate: 1 } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 3) { var xt = r.int(2, 10), target = slope * xt + bv; need(target > 0);
        steps.push(step('Write the model.', rule, 1), step('Set y = ' + target + ' and solve for x.', 'x=' + xt, 3));
        return { variant: 'lm3', prompt: text + ' After how many ' + j[1] + ' will ' + j[2].replace(/^(the|her) /, 'the ') + ' be ' + target + '?', parts: [{ answer: M('x=' + xt) + ' ' + j[1], check: { type: 'line-apply', want: 'when', start: 0, rate: 1, target: 2 } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      if (c === 4) { steps.push(step('The slope is the rate of change; the y-intercept is the starting value.', '', 3));
        return { variant: 'lm4', prompt: 'The equation ' + M(rule) + ' models ' + j[2] + ' after ' + M('x') + ' ' + j[1] + '.', parts: [{ label: 'a', prompt: 'What does the slope mean?', answer: 'The amount ' + (down ? 'decreases' : 'increases') + ' by ' + M(String(mv)) + ' each ' + j[1].slice(0, -1) + '.', check: { type: 'stat-line', rule: rule, want: 'slope' } },
          { label: 'b', prompt: 'What does the y-intercept mean?', answer: 'The starting amount (when ' + M('x=0') + ') is ' + M(String(bv)) + '.', check: { type: 'stat-line', rule: rule, want: 'intercept' } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      // c5–c7: a model from two data points
      var xa = r.int(1, 4), xb = xa + r.int(2, 6), ya = slope * xa + bv, yb = slope * xb + bv; need(ya > 0 && yb > 0);
      var words = 'After ' + xa + ' ' + j[1] + ', ' + j[2] + ' ' + (j[6] || 'is') + ' ' + ya + '. After ' + xb + ' ' + j[1] + ', ' + (j[6] ? 'they are ' : 'it is ') + yb + '. The relationship is linear.';
      steps.push(step('Rate = change in y ÷ change in x.', 'm=\\frac{' + yb + '-' + ya + '}{' + xb + '-' + xa + '}=' + slope, 2), step('Work back to x = 0 for the starting value, then write the model.', rule, 2));
      if (c === 5) return { variant: 'lm5', prompt: words + vars + ' Write an equation for ' + M('y') + '.', parts: [{ answer: M(rule), check: { type: 'line-apply', want: 'equation', pts: [[0, 1], [2, 3]] } }], steps: steps, space: [0.8, 1.0, 1.2] };
      var xq = xb + r.int(1, 5), yq = slope * xq + bv; need(yq >= 0);
      if (c === 6) { steps.push(step('Substitute x = ' + xq + '.', 'y=' + yq, 1));
        return { variant: 'lm6', prompt: words + ' What will ' + (j[6] ? 'they' : 'it') + ' be after ' + xq + ' ' + j[1] + '?', parts: [{ answer: M(String(yq)), check: { type: 'line-apply', want: 'value', pts: [[0, 1], [2, 3]], at: 4 } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      return { variant: 'lm7', prompt: words + vars,
        parts: [{ label: 'a', prompt: 'Find the rate of change.', answer: M(String(slope)) + ' per ' + j[1].slice(0, -1), check: { type: 'line-apply', want: 'rate', pts: [[0, 1], [2, 3]] } },
          { label: 'b', prompt: 'Find the starting value.', answer: M(String(bv)), check: { type: 'line-apply', want: 'start', pts: [[0, 1], [2, 3]] } },
          { label: 'c', prompt: 'Write an equation for ' + M('y') + '.', answer: M(rule), check: { type: 'line-apply', want: 'equation', pts: [[0, 1], [2, 3]] } }], steps: steps, space: [1.0, 1.3, 1.6] };
    }
  });

  /* ================= TRANSFORM · transformations of linear functions ================= */
  function fx(name, m, b) { return name + '(x)=' + (Fr.of(m).isZero() ? num(b) : lin([[m, 'x'], [b, '']])); }
  function shiftWords(d) { return 'shifted ' + Math.abs(d) + ' unit' + (Math.abs(d) === 1 ? '' : 's') + (d > 0 ? ' up' : ' down'); }
  skill({
    id: 'lin-transform', best: [0, 1, 2], tag: 'TRANSFORM', name: 'Transformations of linear functions',
    blurb: 'Shifts up and down (CP2) → steeper, less steep, reflections, a shift and a slope change together (CP1) → write g from a description or from g(x) = f(x − h) (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], m1 = nz(r, -4, 4), b1 = r.int(-6, 6), m2 = m1, b2 = b1;
      if (c === 1) b2 = b1 + r.int(1, 8); if (c === 2) b2 = b1 - r.int(1, 8);
      if (c === 3) { m2 = r.pick([m1 * r.int(2, 3), F(m1, r.int(2, 4))]); need(!Fr.of(m2).eq(m1)); }
      if (c === 4) m2 = -m1;
      if (c === 5) { m2 = m1 * r.int(2, 3) * r.pick([1, -1]); b2 = b1 + nz(r, -6, 6); }
      if (c <= 5) {
        var f = fx('f', m1, b1), g = fx('g', m2, b2), w = [], M1 = Fr.of(m1), M2 = Fr.of(m2);
        if (M1.sign() !== M2.sign()) w.push('reflected across the y-axis');
        if (!M1.abs().eq(M2.abs())) w.push(M2.abs().gt(M1.abs()) ? 'steeper' : 'less steep');
        if (b2 !== b1) w.push(shiftWords(b2 - b1));
        var ansW = w.join(', and '); ansW = ansW.charAt(0).toUpperCase() + ansW.slice(1) + '.';
        steps.push(step('Compare the slopes ⟨' + num(m1) + '⟩ and ⟨' + num(m2) + '⟩ and the y-intercepts ⟨' + b1 + '⟩ and ⟨' + b2 + '⟩.', '', 2));
        steps.push(step('A bigger |slope| is steeper; the opposite slope reflects the line; a new y-intercept shifts it up or down.', '', 2));
        return { variant: 'lt' + c, prompt: 'Describe how the graph of ' + M(g) + ' compares with the graph of ' + M(f) + '.', parts: [{ answer: ansW, check: { type: 'lin-transform', want: 'describe', f: f, g: g } }], steps: steps, space: [0.4, 0.5, 0.6] };
      }
      var f6 = fx('f', m1, b1);
      if (c === 6) { var d6 = nz(r, -9, 9);
        steps.push(step('A shift up or down adds to the whole function: ⟨g(x)=f(x)' + (d6 > 0 ? '+' : '-') + Math.abs(d6) + '⟩.', fx('g', m1, b1 + d6), 3));
        return { variant: 'lt6', prompt: 'The graph of ' + M(f6) + ' is ' + shiftWords(d6) + ' to make the graph of ⟨g⟩. Write ⟨g(x)⟩ in slope-intercept form.', parts: [{ answer: M(fx('g', m1, b1 + d6)), check: { type: 'lin-transform', want: 'shift-eq', f: f6 } }], steps: steps, space: [0.5, 0.6, 0.7] }; }
      var h = nz(r, -6, 6), rel = 'g(x)=f(x' + (h > 0 ? '-' + h : '+' + (-h)) + ')';
      steps.push(step('Replace ⟨x⟩ with ⟨x' + (h > 0 ? '-' + h : '+' + (-h)) + '⟩ in the rule for ⟨f⟩.', 'g(x)=' + mcoef(m1) + '(x' + (h > 0 ? '-' + h : '+' + (-h)) + ')' + (b1 ? (b1 > 0 ? '+' : '-') + Math.abs(b1) : ''), 2), step('Distribute and combine.', fx('g', m1, b1 - m1 * h), 2));
      return { variant: 'lt7', prompt: 'Let ' + M(f6) + ' and ' + M(rel) + '. Write ⟨g(x)⟩ in slope-intercept form. How is the graph moved?', parts: [{ label: 'a', answer: M(fx('g', m1, b1 - m1 * h)), check: { type: 'lin-transform', want: 'h-eq', f: f6, rel: rel } },
        { label: 'b', answer: 'Shifted ' + Math.abs(h) + ' unit' + (Math.abs(h) === 1 ? '' : 's') + (h > 0 ? ' right.' : ' left.'), check: { type: 'lin-transform', want: 'h-words', f: f6, rel: rel } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* Explicit graphical response skills for the online Assessment Readiness Check. */
  skill({
    id: 'graph-slope-intercept', difficultyProfile:'focused',best: [0, 1, 2], tag: 'GRAPHLINE', name: 'Graph lines in slope-intercept form',
    blurb: 'Plot the y-intercept and use rise/run (CP2) → negative and fractional slopes (CP1) → horizontal and steep lines (Honors).',
    generate: function (ctx) {
      var r=ctx.rng,c=ctx.c,steps=[],m,b;
      if(c<=2)m=F(r.pick([-2,-1,1,2]));
      else if(c<=5){var den=r.pick([1,2,3]),n=r.pick([-3,-2,-1,1,2,3]);m=F(n,den);}
      else m=F(r.pick([-4,-3,-2,0,2,3,4]),r.pick([1,2]));
      b=F(r.int(-5,5));var eq=si(m,b);
      var run=m.d,dy=m.n;
      need(Math.abs(dy)<=7&&Math.abs(b.n+dy)<=8&&run<=4);
      var p0=[0,b.n],p1=[run,b.n+dy],fig=plane([-10,10,-10,10],{segs:[{a:p0,b:p1,aEnd:'arrow',bEnd:'arrow'}],points:[{x:p0[0],y:p0[1]},{x:p1[0],y:p1[1]}]});
      steps.push(step('Start at the y-intercept.',pt(0,b.n),1),step('Use slope as rise over run to find a second point.',pt(p1[0],p1[1]),2),step('Draw one straight line through both points.',eq,1));
      return {variant:'gsi'+c,prompt:'Graph '+M(eq)+' on the coordinate plane. Plot two points and draw the line.',
        fig:plane([-10,10,-10,10]),parts:[{answer:M(eq),check:{type:'line-eq',form:'slope-intercept',src:{eq:eq}},answerFig:fig}],steps:steps,space:[1,1.2,1.5]};
    }
  });

  skill({
    id: 'graph-from-points',difficultyProfile:'focused',best:[0,1],tag:'GRAPHLINE',name:'Graph a line through two points',
    blurb:'Plot two points, then draw their line; includes positive, negative and zero slope.',
    generate:function(ctx){
      var r=ctx.rng,c=ctx.c,x=r.int(-5,3),y=r.int(-5,5),dx=r.pick([2,3,4]),dy=r.pick([-3,-2,0,2,3]),xx=x+dx,yy=y+dy;
      need(Math.abs(xx)<=8&&Math.abs(yy)<=8);
      var a=[x,y],b=[xx,yy],eq=si(F(dy,dx),F(y).sub(F(dy,dx).mul(x)));
      return {variant:'gpts'+c,prompt:'Graph the line through '+M(pt(x,y))+' and '+M(pt(xx,yy))+'. Plot both points and draw the line.',
        fig:plane([-10,10,-10,10]),parts:[{answer:M(eq),check:{type:'line-eq',form:'any',src:{pairs:two(a,b)}},
          answerFig:plane([-10,10,-10,10],{segs:[{a:a,b:b,aEnd:'arrow',bEnd:'arrow'}]})}],
        steps:[step('Plot the two given points.',M(two(a,b)),1),step('Connect with a straight line.',eq,1)],space:[1,1.2,1.5]};
    }
  });
  skill({
    id:'graph-special-lines',difficultyProfile:'focused',best:[0,1],tag:'GRAPHLINE',name:'Graph horizontal and vertical lines',
    blurb:'Draw x = a and y = b, including negative intercepts.',
    generate:function(ctx){
      var r=ctx.rng,k=nz(r,-7,7),vertical=r.chance(.5),eq=(vertical?'x=':'y=')+k;
      var a=vertical?[k,-5]:[-5,k],b=vertical?[k,5]:[5,k];
      return {variant:'gspecial'+(vertical?'v':'h'),prompt:'Graph '+M(eq)+' on the coordinate plane. Plot two points.',
        fig:plane([-10,10,-10,10]),parts:[{answer:M(eq),check:{type:'line-eq',form:'any',src:{eq:eq}},
          answerFig:plane([-10,10,-10,10],{segs:[{a:a,b:b,aEnd:'arrow',bEnd:'arrow'}]})}],
        steps:[step(vertical?'Every point has the same x-coordinate.':'Every point has the same y-coordinate.',eq,1),
        step('Plot two points and connect.',M(two(a,b)),1)],space:[1,1.2,1.5]};
    }
  });
  skill({
    id:'graph-standard-form',difficultyProfile:'focused',best:[1,2],tag:'GRAPHLINE',name:'Graph linear equations in standard form',
    blurb:'Rearrange Ax + By = C to slope-intercept form and graph using two points.',
    generate:function(ctx){
      var r=ctx.rng,m=F(r.pick([-3,-2,-1,1,2,3])),b=F(r.int(-5,5)),eq=stdForm(m,b);
      var p0=[0,b.n],p1=[1,b.n+m.n];need(Math.abs(p1[1])<=9);
      return {variant:'gstd',prompt:'Graph '+M(eq)+' using two points. Draw the complete line.',
        fig:plane([-10,10,-10,10]),parts:[{answer:M(si(m,b)),check:{type:'line-eq',form:'any',src:{eq:eq}},
          answerFig:plane([-10,10,-10,10],{segs:[{a:p0,b:p1,aEnd:'arrow',bEnd:'arrow'}]})}],
        steps:[step('Rewrite in slope-intercept form.',si(m,b),2),
        step('Plot the intercept and use slope for a second point.',M(two(p0,p1)),1)],space:[1,1.2,1.5]};
    }
  });

  NS.registerSkillSet({
    id: 'algebra1-linear-equations-slope', course: 'algebra1', courseName: 'Algebra 1', unit: 'linear-equations-slope', unitName: 'Linear Functions and Graphing',
    title: 'The Slope Shack',
    tags: { SLOPE: 'Slope', FORMS: 'Forms of linear equations', WRITE: 'Writing equations of lines', PARPERP: 'Parallel and perpendicular lines', APPLY: 'Linear models', TRANSFORM: 'Transformations', GRAPHLINE: 'Graphing linear functions' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Slope</h4><p>⟨m=\\frac{y_2-y_1}{x_2-x_1}⟩ (rise over run). Horizontal: ⟨m=0⟩. Vertical: undefined.</p></section>' +
      '<section><h4>Forms</h4><p>Slope-intercept: ⟨y=mx+b⟩. Point-slope: ⟨y-y_1=m(x-x_1)⟩. Standard: ⟨Ax+By=C⟩ with integers and ⟨A\\ge 0⟩.</p></section>' +
      '<section><h4>Intercepts</h4><p>x-intercept: set ⟨y=0⟩. y-intercept: set ⟨x=0⟩.</p></section>' +
      '<section><h4>Parallel and perpendicular</h4><p>Parallel: equal slopes. Perpendicular: slopes multiply to ⟨-1⟩ (opposite reciprocals).</p></section>' +
      '<section><h4>Special lines</h4><p>Horizontal: ⟨y=k⟩. Vertical: ⟨x=h⟩.</p></section>' +
      '<section><h4>Models</h4><p>⟨y=mx+b⟩: m is the rate of change, b is the starting value.</p></section></div>',
    gaps: ['Direct variation and absolute-value graphs are not generated.'],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
