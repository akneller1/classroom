/* Menu Assessment Generator — Algebra 1 · Unit 6 Systems of Equations and Inequalities (roadmap days 76–90).
   Skill groups: GRAPH (solutions and graphs), SUBST (substitution), ELIM (elimination), APPLY (word problems),
   INEQ (linear inequalities in two variables and their systems).
   The verifier solves every system again from the printed equations, the drawn lines or the numbers in the story,
   and reads boundary lines and shading back from the drawn graph. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, M = K.M, num = K.num, lin = K.lin, Fr = K.Fr;
  var need = K.need, nz = K.nz, step = K.step, F = K.F;
  var skills = [];
  function skill(d) { skills.push(d); return d; }
  function pt(x, y) { return '(' + num(x) + ',\\ ' + num(y) + ')'; }
  function si(m, b) { m = Fr.of(m); b = Fr.of(b); return 'y=' + (m.isZero() ? num(b) : lin([[m, 'x'], [b, '']])); }
  function std(a, b, c, vx, vy) { return lin([[a, vx || 'x'], [b, vy || 'y']]) + '=' + num(c); }
  function sysTeX(e1, e2) { return M(e1) + ' and ' + M(e2); }
  function pairAns(x, y) { return M(pt(x, y)); }
  function win() { return { kind: 'plane', xmin: -6, xmax: 6, ymin: -6, ymax: 6, points: [], segs: [], curves: [] }; }
  /* the longest lattice segment of y = m(x − x0) + y0 inside the window */
  function lineSeg(m, x0, y0) {
    m = Fr.of(m); var dx = m.d, dy = m.n, lo = 0, hi = 0, inW = function (t) { var x = x0 + t * dx, y = y0 + t * dy; return x >= -6 && x <= 6 && y >= -6 && y <= 6; };
    need(inW(0)); while (inW(lo - 1)) lo--; while (inW(hi + 1)) hi++; need(lo < 0 && hi > 0 && hi - lo >= 3);
    return { a: [x0 + lo * dx, y0 + lo * dy], b: [x0 + hi * dx, y0 + hi * dy], aEnd: 'arrow', bEnd: 'arrow' };
  }
  function slopePick(r, frac) { if (!frac) return F(nz(r, -3, 3)); var d = r.pick([2, 3]), n = nz(r, -3, 3); need(n % d !== 0); return F(n, d); }
  /* a·x + b·y = c with the solution (x0, y0) */
  function eqThrough(a, b, x0, y0) { return std(a, b, a * x0 + b * y0); }
  function det(a1, b1, a2, b2) { return a1 * b2 - a2 * b1; }

  /* ================= GRAPH ================= */
  skill({
    id: 'sys-graph', best: [0, 1, 2], tag: 'GRAPH', name: 'Solutions of systems and graphs',
    blurb: 'Read the solution from a graph, is a point a solution? (CP2) → how many solutions a graph shows, standard form (CP1) → how many solutions from the equations, a value of k for no solution or infinitely many (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], x0 = r.int(-4, 4), y0 = r.int(-4, 4);
      if (c === 2 || c === 5) {
        var e1, e2;
        if (c === 2) { var m1 = nz(r, -4, 4), m2 = nz(r, -4, 4); need(m1 !== m2); e1 = si(m1, y0 - m1 * x0); e2 = si(m2, y0 - m2 * x0); }
        else { var a1 = nz(r, -5, 5), b1 = nz(r, -5, 5), a2 = nz(r, -5, 5), b2 = nz(r, -5, 5); need(det(a1, b1, a2, b2) !== 0); e1 = eqThrough(a1, b1, x0, y0); e2 = eqThrough(a2, b2, x0, y0); }
        var yes = r.chance(0.5), px = x0, py = yes ? y0 : y0 + r.pick([-1, 1, 2]);
        steps.push(step('Substitute ' + M('x=' + px) + ' and ' + M('y=' + py) + ' into each equation.', '', 2), step(yes ? 'Both equations are true.' : 'At least one equation is false.', '', 2));
        return { variant: 'gr' + c, prompt: 'Is ' + M(pt(px, py)) + ' a solution of the system ' + sysTeX(e1, e2) + '? Explain.', parts: [{ answer: yes ? 'Yes: it makes both equations true.' : 'No: it does not make both equations true.', check: { type: 'system', want: 'is-solution', eqs: [e1, e2], point: pt(px, py) } }], steps: steps, space: [0.6, 0.8, 1.0] };
      }
      if (c === 1 || c === 3 || c === 4) {
        var mA = slopePick(r, c === 3), mB = slopePick(r, false), parallel = c === 4 && r.chance(0.4);
        if (parallel) mB = mA; need(!mA.eq(mB) || parallel);
        var sA = lineSeg(mA, x0, y0), sB = parallel ? lineSeg(mB, x0, y0 + r.pick([-3, -2, 2, 3])) : lineSeg(mB, x0, y0), fig = win(); fig.segs = [sA, sB];
        if (c === 4) { steps.push(step(parallel ? 'The lines have the same slope and never meet.' : 'The lines cross at one point.', '', 2), step(parallel ? 'No point is on both lines.' : 'That point is the only solution.', parallel ? '' : pt(x0, y0), 2));
          return { variant: 'gr4', prompt: 'The graph shows a system of two linear equations. How many solutions does it have? If there is one, give it.', fig: fig, parts: [{ answer: parallel ? 'No solution: the lines are parallel.' : 'One solution: ' + pairAns(x0, y0), check: { type: 'system', want: 'count', src: { fig: true } } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
        steps.push(step('Find the point where the two lines cross.', pt(x0, y0), 3), step('Check: the point is on both lines.', '', 1));
        return { variant: 'gr' + c, prompt: 'Use the graph to solve the system.', fig: fig, parts: [{ answer: pairAns(x0, y0), check: { type: 'system', src: { fig: true } } }], steps: steps, space: [0.5, 0.7, 0.9] };
      }
      if (c === 6) {
        var kind = r.pick(['one', 'none', 'infinite']), A = nz(r, 1, 5), B = nz(r, -5, 5), C = r.int(-9, 9), k = r.pick([2, 3, -2]), eA = std(A, B, C), eB;
        if (kind === 'one') { var A2 = nz(r, -5, 5), B2 = nz(r, -5, 5); need(det(A, B, A2, B2) !== 0); eB = std(A2, B2, r.int(-9, 9)); }
        else if (kind === 'none') { var C2 = k * C + r.pick([-3, -1, 1, 2]); eB = std(k * A, k * B, C2); }
        else eB = std(k * A, k * B, k * C);
        need(B !== 0); var msA = F(-A, B);
        if (r.chance(0.5)) { eA = si(msA, F(C, B)); }
        steps.push(step('Write both equations in slope-intercept form (or compare coefficients).', '', 2), step(kind === 'one' ? 'Different slopes: the lines cross once.' : kind === 'none' ? 'Same slope, different y-intercepts: parallel lines.' : 'Same slope and same y-intercept: the same line.', '', 2));
        return { variant: 'gr6', prompt: 'Without solving, how many solutions does the system ' + sysTeX(eA, eB) + ' have? Explain.', parts: [{ answer: kind === 'one' ? 'One solution: the slopes are different.' : kind === 'none' ? 'No solution: same slope, different y-intercepts.' : 'Infinitely many solutions: the equations describe the same line.', check: { type: 'system', want: 'count', eqs: [eA, eB] } }], steps: steps, space: [0.7, 0.9, 1.1] };
      }
      // c7: a value of k
      var target = r.pick(['none', 'infinite']), a = nz(r, 1, 4), b = nz(r, -5, 5), cc = nz(r, -9, 9), mlt = r.pick([2, 3, -2]), kk = mlt * b;
      var e1k = std(a, b, cc), e2k = lin([[mlt * a, 'x']]) + (kk ? '+ky' : '') + '=' + num(target === 'infinite' ? mlt * cc : mlt * cc + r.pick([-2, 1, 3]));
      need(kk !== 0);
      steps.push(step('For ' + (target === 'none' ? 'no solution the lines must be parallel' : 'infinitely many solutions the lines must be the same') + ': the coefficients must be proportional.', '', 2), step('The x-coefficients have ratio ' + M(String(mlt)) + ', so ' + M('k=' + mlt + '\\cdot' + (b < 0 ? '(' + b + ')' : b)) + '.', 'k=' + kk, 2));
      return { variant: 'gr7', prompt: 'For what value of ' + M('k') + ' does the system ' + sysTeX(e1k, e2k) + ' have ' + (target === 'none' ? 'no solution' : 'infinitely many solutions') + '?', parts: [{ answer: M('k=' + kk), check: { type: 'system', want: 'param', eqs: [e1k, e2k], target: target } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= SUBST ================= */
  skill({
    id: 'sys-subst', best: [0, 1, 2], tag: 'SUBST', name: 'Solve by substitution',
    blurb: 'One variable already isolated (CP2) → isolate a variable first, negative solutions (CP1) → fraction coefficients, fraction solutions (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], x0 = c <= 2 ? r.int(1, 8) : nz(r, -8, 8), y0 = c <= 2 ? r.int(1, 9) : nz(r, -9, 9), e1, e2, iso;
      if (c === 1) { var m = r.int(2, 5); y0 = m * x0; e1 = 'y=' + m + 'x'; var a = r.int(1, 4), b = r.pick([1, 2, 3]); e2 = std(a, b, a * x0 + b * y0); iso = 'y'; }
      else if (c === 2) { var m2 = nz(r, -4, 4), b0 = y0 - m2 * x0; e1 = si(m2, b0); var a2 = r.int(1, 5), b2 = r.pick([1, 2, 3, -1, -2]); need(a2 + b2 * m2 !== 0); e2 = std(a2, b2, a2 * x0 + b2 * y0); iso = 'y'; }
      else if (c === 3) { var p = nz(r, -4, 4), q = x0 - p * y0; e1 = 'x=' + lin([[p, 'y'], [q, '']]); var a3 = r.pick([1, 2, 3, -2]), b3 = nz(r, -4, 4); need(a3 * p + b3 !== 0); e2 = std(a3, b3, a3 * x0 + b3 * y0); iso = 'x'; }
      else if (c === 4 || c === 5) { var b4 = nz(r, -5, 5), a5 = nz(r, -5, 5), b5 = nz(r, -5, 5); need(det(1, b4, a5, b5) !== 0 && Math.abs(a5) !== 1);
        e1 = c === 4 ? std(1, b4, x0 + b4 * y0) : std(a5, 1, a5 * x0 + y0); e2 = c === 4 ? std(a5, b5, a5 * x0 + b5 * y0) : std(b4, b5, b4 * x0 + b5 * y0); need(det(c === 4 ? 1 : a5, c === 4 ? b4 : 1, c === 4 ? a5 : b4, b5) !== 0);
        if (c === 5) need(Math.abs(b4) !== 1); iso = c === 4 ? 'x' : 'y'; }
      else if (c === 6) { var mf = slopePick(r, true); x0 = mf.d * r.int(-3, 3); var bf = F(y0).sub(mf.mul(x0)); need(bf.isInt()); e1 = si(mf, bf); var a6 = nz(r, -4, 4), b6 = nz(r, -4, 4); need(!F(a6).add(mf.mul(b6)).isZero()); e2 = std(a6, b6, a6 * x0 + b6 * y0); iso = 'y'; }
      else { var a7 = nz(r, -5, 5), b7 = nz(r, -5, 5), h7 = F(1, 2), d7 = F(b7).sub(h7.mul(a7)); need(!d7.isZero()); var c1 = r.int(-9, 9), c2 = r.int(-9, 9);
        var X = F(c1 * b7 - a7 * c2).div(d7), Y = F(c2).sub(h7.mul(c1)).div(d7); need(ctx.intOnly ? X.isInt() && Y.isInt() : !(X.isInt() && Y.isInt()));
        e1 = std(1, a7, c1); e2 = std(h7, b7, c2); iso = 'x';
        steps.push(step('Solve the first equation for x.', 'x=' + lin([[-a7, 'y'], [c1, '']]), 1), step('Substitute into the second equation and solve for y.', 'y=' + num(Y), 2), step('Substitute back to find x.', 'x=' + num(X), 1));
        return { variant: 'su7', prompt: 'Solve the system by substitution: ' + sysTeX(e1, e2) + '.', parts: [{ answer: pairAns(X, Y), check: { type: 'system', eqs: [e1, e2] } }], steps: steps, space: [0.9, 1.1, 1.3] }; }
      steps.push(step(iso === 'y' ? 'Use (or make) an equation with y by itself and substitute it into the other equation.' : 'Use (or make) an equation with x by itself and substitute it into the other equation.', '', 1),
        step('Solve the one-variable equation.', (iso === 'y' ? 'x=' + num(x0) : 'y=' + num(y0)), 2), step('Substitute back to find the other variable.', iso === 'y' ? 'y=' + num(y0) : 'x=' + num(x0), 1));
      return { variant: 'su' + c, prompt: 'Solve the system by substitution: ' + sysTeX(e1, e2) + '.', parts: [{ answer: pairAns(x0, y0), check: { type: 'system', eqs: [e1, e2] } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= ELIM ================= */
  skill({
    id: 'sys-elim', best: [0, 1, 2], tag: 'ELIM', name: 'Solve by elimination',
    blurb: 'Opposite coefficients, then equal coefficients (CP2) → multiply one or both equations, rearrange first (CP1) → no solution or infinitely many, decimal coefficients (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], x0 = c <= 2 ? r.int(-3, 8) : nz(r, -8, 8), y0 = c <= 2 ? r.int(-3, 8) : nz(r, -8, 8), a1, b1, a2, b2, e1, e2, hint;
      if (c === 1) { a1 = nz(r, -5, 5); b1 = r.int(1, 6) * r.sign(); a2 = nz(r, -5, 5); b2 = -b1; hint = 'Add the equations: the y-terms cancel.'; }
      else if (c === 2) { a1 = r.int(1, 6); b1 = nz(r, -5, 5); a2 = a1; b2 = nz(r, -5, 5); hint = 'Subtract the equations: the x-terms cancel.'; }
      else if (c === 3) { a1 = nz(r, -4, 4); b1 = nz(r, -3, 3); var kk = r.pick([2, 3, -2, -3]); a2 = nz(r, -6, 6); b2 = kk * b1; need(Math.abs(b2) > 1 && Math.abs(b1) !== Math.abs(b2)); hint = 'Multiply the first equation by ' + num(-kk) + ' so the y-terms cancel.'; }
      else if (c === 4 || c === 5) { a1 = r.pick([2, 3, 4, 5]) * r.sign(); a2 = r.pick([2, 3, 4, 5, 6]) * r.sign(); b1 = r.pick([2, 3, 5, 7]) * r.sign(); b2 = r.pick([2, 3, 4, 5]) * r.sign(); need(K.gcd(Math.abs(a1), Math.abs(a2)) < Math.min(Math.abs(a1), Math.abs(a2)) && K.gcd(Math.abs(b1), Math.abs(b2)) < Math.min(Math.abs(b1), Math.abs(b2))); hint = 'Multiply both equations so one variable has opposite coefficients.'; }
      else if (c === 6) {
        var kind = r.pick(['none', 'infinite', 'one']), A = nz(r, 1, 6), B = nz(r, -6, 6), C = r.int(-9, 9), m = r.pick([2, 3, -2]);
        e1 = std(A, B, C); e2 = kind === 'infinite' ? std(m * A, m * B, m * C) : kind === 'none' ? std(m * A, m * B, m * C + r.pick([-4, -1, 2, 5])) : null;
        if (kind === 'one') { a2 = nz(r, -6, 6); b2 = nz(r, -6, 6); need(det(A, B, a2, b2) !== 0); var X6 = nz(r, -6, 6), Y6 = F(C - A * X6, B); need(Y6.isInt()); e2 = std(a2, b2, a2 * X6 + b2 * Y6.n);
          steps.push(step('Eliminate one variable and solve.', '', 2), step('Substitute back.', pt(X6, Y6), 2));
          return { variant: 'el6', prompt: 'Solve the system by elimination: ' + sysTeX(e1, e2) + '. If there is no solution or there are infinitely many, say so.', parts: [{ answer: pairAns(X6, Y6), check: { type: 'system', eqs: [e1, e2] } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
        steps.push(step('Multiply the first equation by ' + m + ' and subtract.', kind === 'none' ? '0=' + num((function () { var R = /=(.*)$/.exec(e2)[1]; return Number(R) - m * C; })()) : '0=0', 2), step(kind === 'none' ? 'A false statement: the lines are parallel, so there is no solution.' : 'A true statement: the equations describe the same line.', '', 2));
        return { variant: 'el6', prompt: 'Solve the system by elimination: ' + sysTeX(e1, e2) + '. If there is no solution or there are infinitely many, say so.', parts: [{ answer: kind === 'none' ? 'No solution: eliminating gives a false statement.' : 'Infinitely many solutions: eliminating leaves a true statement.', check: { type: 'system', eqs: [e1, e2] } }], steps: steps, space: [0.8, 1.0, 1.2] };
      }
      else {   // c7: decimal coefficients
        var p1 = r.pick([2, 4, 5, 15, 25]), q1 = r.pick([1, 3, 5, 2]), p2 = r.pick([1, 3, 5, 12]), q2 = r.pick([2, 4, 6, 15]); need(det(p1, q1, p2, q2) !== 0);
        var d10 = function (n) { return K.dec(n); };
        e1 = d10(p1) + 'x' + (q1 < 0 ? '-' : '+') + d10(Math.abs(q1)) + 'y=' + d10(p1 * x0 + q1 * y0); e2 = d10(p2) + 'x' + (q2 < 0 ? '-' : '+') + d10(Math.abs(q2)) + 'y=' + d10(p2 * x0 + q2 * y0);
        e1 = e1.replace(/^1x/, 'x').replace(/([+-])1y/, '$1y'); e2 = e2.replace(/^1x/, 'x').replace(/([+-])1y/, '$1y');
        need(!/^0x|[+-]0y/.test(e1 + e2));
        steps.push(step('Multiply both equations by 10 to clear the decimals.', std(p1, q1, p1 * x0 + q1 * y0), 1), step('Eliminate a variable and solve.', 'x=' + x0 + ',\\ y=' + y0, 2), step('Check in an original equation.', '', 1));
        return { variant: 'el7', prompt: 'Solve the system: ' + sysTeX(e1, e2) + '.', parts: [{ answer: pairAns(x0, y0), check: { type: 'system', eqs: [e1, e2] } }], steps: steps, space: [0.9, 1.1, 1.3] };
      }
      need(det(a1, b1, a2, b2) !== 0);
      e1 = eqThrough(a1, b1, x0, y0); e2 = eqThrough(a2, b2, x0, y0);
      if (c === 5) { var rhs = a1 * x0 + b1 * y0; e1 = lin([[a1, 'x']]) + '=' + lin([[-b1, 'y'], [rhs, '']]); e2 = lin([[b2, 'y']]) + '=' + lin([[-a2, 'x'], [a2 * x0 + b2 * y0, '']]); hint = 'Rewrite both equations as Ax + By = C, then ' + hint.charAt(0).toLowerCase() + hint.slice(1); }
      steps.push(step(hint, '', 2), step('Solve for the remaining variable, then substitute back.', 'x=' + num(x0) + ',\\ y=' + num(y0), 2));
      return { variant: 'el' + c, prompt: 'Solve the system by elimination: ' + sysTeX(e1, e2) + '.', parts: [{ answer: pairAns(x0, y0), check: { type: 'system', eqs: [e1, e2] } }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= APPLY ================= */
  var TICKETS = [['Adult tickets cost', 'student tickets cost', 'tickets', 'adult tickets', 'student tickets', 'a', 's'], ['Large pizzas cost', 'small pizzas cost', 'pizzas', 'large pizzas', 'small pizzas', 'L', 'S'],
    ['Hardcover books cost', 'paperback books cost', 'books', 'hardcovers', 'paperbacks', 'h', 'p']];
  skill({
    id: 'sys-apply', best: [0, 1, 2], tag: 'APPLY', name: 'Systems in context',
    blurb: 'Sum and difference, ticket sales, write the system (CP2) → when two plans cost the same, prices with cents (CP1) → mixtures, boats in a current (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [];
      if (c === 1) { var big = r.int(12, 40), small = r.int(2, big - 2), S = big + small, D = big - small;
        steps.push(step('Let x be the larger number and y the smaller.', 'x+y=' + S + ',\\ x-y=' + D, 2), step('Add the equations.', '2x=' + (2 * big), 1), step('Solve.', 'x=' + big + ',\\ y=' + small, 1));
        return { variant: 'ap1', prompt: 'The sum of two numbers is ' + S + ' and their difference is ' + D + '. Find the larger number and the smaller number.', parts: [{ answer: M(String(big)) + ' and ' + M(String(small)), check: { type: 'sys-apply', rows: [[1, 1, { n: 0 }], [1, -1, { n: 1 }]], int: true } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 2 || c === 3 || c === 5) { var T = r.pick(TICKETS), cents = c === 5, pa = cents ? r.int(30, 90) * 25 : r.int(6, 15), pb = cents ? r.int(8, pa / 25 - 4) * 25 : r.int(2, pa - 2), na = r.int(5, 30), nb = r.int(5, 30), N = na + nb, tot = pa * na + pb * nb;
        var money = function (v) { return cents ? (v / 100).toFixed(2) : String(v); };
        var story = T[0] + ' $' + money(pa) + ' and ' + T[1] + ' $' + money(pb) + '. A club sold ' + N + ' ' + T[2] + ' for a total of $' + money(tot) + '.';
        var rows = [[1, 1, { n: 2 }], [{ n: 0 }, { n: 1 }, { n: 3 }]];
        if (c === 3) { var vA = T[5], vB = T[6];
          steps.push(step('One equation counts the ' + T[2] + '.', vA + '+' + vB + '=' + N, 2), step('One equation adds up the money.', lin([[pa, vA], [pb, vB]]) + '=' + tot, 2));
          return { variant: 'ap3', prompt: story + ' Let ' + M(vA) + ' be the number of ' + T[3] + ' and ' + M(vB) + ' the number of ' + T[4] + '. Write a system of equations for this situation.', parts: [{ answer: M(vA + '+' + vB + '=' + N) + ' and ' + M(lin([[pa, vA], [pb, vB]]) + '=' + tot), check: { type: 'sys-apply', want: 'model', vx: vA, vy: vB, rows: rows, int: true, pos: true } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
        steps.push(step('Count equation and money equation.', 'x+y=' + N + ',\\ ' + lin([[F(pa, cents ? 100 : 1), 'x'], [F(pb, cents ? 100 : 1), 'y']]) + '=' + num(F(tot, cents ? 100 : 1)), 2), step('Solve the system (substitution or elimination).', 'x=' + na + ',\\ y=' + nb, 2));
        return { variant: 'ap' + c, prompt: story + ' How many ' + T[3] + ' and how many ' + T[4] + ' were sold?', parts: [{ answer: M(String(na)) + ' ' + T[3] + ' and ' + M(String(nb)) + ' ' + T[4], check: { type: 'sys-apply', rows: rows, int: true, pos: true } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      if (c === 4) { var r1 = r.int(2, 9) * 5, r2 = r1 + r.int(1, 4) * 5, xm = r.int(2, 12), f2 = r.int(1, 6) * 10, f1 = f2 + (r2 - r1) * xm, cost = f1 + r1 * xm; need(f1 <= 400);
        steps.push(step('Write a cost equation for each plan.', 'y=' + r1 + 'x+' + f1 + ',\\ y=' + r2 + 'x+' + f2, 2), step('Set the costs equal and solve.', 'x=' + xm, 2), step('Find the cost.', 'y=' + cost, 1));
        return { variant: 'ap4', prompt: 'Gym A charges a $' + f1 + ' joining fee plus $' + r1 + ' per month. Gym B charges a $' + f2 + ' joining fee plus $' + r2 + ' per month. After how many months do the two gyms cost the same, and what is that total cost?', parts: [{ answer: M(String(xm)) + ' months, ' + M(String(cost)) + ' dollars', check: { type: 'sys-apply', rows: [[{ n: 1, s: -1 }, 1, { n: 0 }], [{ n: 3, s: -1 }, 1, { n: 2 }]], int: true, pos: true } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      if (c === 6) { var pL = r.pick([10, 20, 25, 30]), pH = r.pick([40, 50, 60, 70]), tot2 = r.pick([10, 20, 30, 40, 50]), xa = r.int(1, tot2 - 1), pT = (pL * xa + pH * (tot2 - xa)) / tot2; need(Number.isInteger(pT) && pT !== pL && pT !== pH);
        steps.push(step('Liters: x + y = ' + tot2 + '. Amount of pure chemical: ' + pL + '% of x plus ' + pH + '% of y.', 'x+y=' + tot2 + ',\\ ' + (pL / 100) + 'x+' + (pH / 100) + 'y=' + (pT * tot2 / 100), 2), step('Solve.', 'x=' + xa + ',\\ y=' + (tot2 - xa), 2));
        return { variant: 'ap6', prompt: 'A chemist mixes a ' + pL + '% acid solution with a ' + pH + '% acid solution to make ' + tot2 + ' liters of a ' + pT + '% acid solution. How many liters of the ' + pL + '% solution and how many liters of the ' + pH + '% solution are used?', parts: [{ answer: pL + '% solution: ' + M(String(xa)) + ' liters; ' + pH + '% solution: ' + M(String(tot2 - xa)) + ' liters', check: { type: 'sys-apply', rows: [[1, 1, { n: 2 }], [{ n: 0 }, { n: 1 }, { n: 3, mul: 2 }]], int: true, pos: true } }], steps: steps, space: [0.9, 1.1, 1.3] }; }
      var b = r.int(8, 25), cur = r.int(1, b - 3), t1 = r.int(2, 5), t2 = r.int(2, 6), d1 = (b + cur) * t1, d2 = (b - cur) * t2;
      steps.push(step('Downstream the speeds add; upstream they subtract. Distance = rate × time.', t1 + '(b+c)=' + d1 + ',\\ ' + t2 + '(b-c)=' + d2, 2), step('Divide each equation by its time and solve.', 'b=' + b + ',\\ c=' + cur, 2));
      return { variant: 'ap7', prompt: 'A boat travels ' + d1 + ' km downstream in ' + t1 + ' hours. The return trip of ' + d2 + ' km upstream takes ' + t2 + ' hours. Find the speed of the boat in still water and the speed of the current (km per hour).', parts: [{ answer: 'Boat ' + M(String(b)) + ' km/h, current ' + M(String(cur)) + ' km/h', check: { type: 'sys-apply', rows: [[{ n: 1 }, { n: 1 }, { n: 0 }], [{ n: 3 }, { n: 3, s: -1 }, { n: 2 }]], int: true, pos: true } }], steps: steps, space: [0.9, 1.1, 1.3] };
    }
  });

  /* ================= INEQ ================= */
  var RELTEX = { '>': '>', '<': '<', ge: '\\ge ', le: '\\le ' };
  function hpSpec(r, frac) {
    var m = slopePick(r, frac), b = r.int(-3, 3), up = r.chance(0.5), strict = r.chance(0.5), rel = up ? (strict ? '>' : 'ge') : (strict ? '<' : 'le');
    return { m: m, b: b, rel: rel, tex: 'y' + RELTEX[rel] + (si(m, b).slice(2)), fig: { a: [0, b], b: [m.d, b + m.n], dashed: strict, side: [0, b + (up ? 3 : -3)] } };
  }
  function inside(h, x, y) { var v = F(y).sub(h.m.mul(x).add(h.b)); return h.rel === '>' ? v.sign() > 0 : h.rel === 'ge' ? v.sign() >= 0 : h.rel === '<' ? v.sign() < 0 : v.sign() <= 0; }
  var JOBS = [['A theater sells adult tickets for $', ' and student tickets for $', '. It can sell at most ', ' tickets and needs at least $', ' in sales.', 'adult tickets', 'student tickets'],
    ['A bakery sells cakes for $', ' and pies for $', '. It can bake at most ', ' items a day and wants at least $', ' in sales.', 'cakes', 'pies']];
  skill({
    id: 'sys-ineq', best: [0, 1, 2], tag: 'INEQ', name: 'Linear inequalities and systems of inequalities',
    blurb: 'Is a point a solution of an inequality? Write the inequality for a graph, name a point in the solution of a system (CP2) → is a point a solution of a system, write a system from its graph (CP1) → fraction slopes, write a system of inequalities from a situation (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [];
      if (c === 1 || c === 4) {
        var h1 = hpSpec(r, false), h2 = hpSpec(r, false), px = r.int(-4, 4), py = r.int(-5, 5), list = c === 1 ? [h1] : [h1, h2];
        need(c === 1 || !h1.m.eq(h2.m)); var yes = list.every(function (h) { return inside(h, px, py); });
        need(c === 1 || yes || r.chance(0.6));
        steps.push(step('Substitute ' + M('x=' + px) + ' and ' + M('y=' + py) + ' into ' + (c === 1 ? 'the inequality' : 'each inequality') + '.', '', 2), step(yes ? 'Every inequality is true.' : 'A statement is false.', '', 2));
        return { variant: 'iq' + c, prompt: 'Is ' + M(pt(px, py)) + ' a solution of ' + (c === 1 ? M(h1.tex) : 'the system ' + sysTeX(h1.tex, h2.tex)) + '? Explain.', parts: [{ answer: yes ? 'Yes: it makes ' + (c === 1 ? 'the inequality' : 'both inequalities') + ' true.' : 'No: it does not make ' + (c === 1 ? 'the inequality' : 'both inequalities') + ' true.', check: { type: 'ineq2', want: 'is-solution', ineqs: list.map(function (h) { return h.tex; }), point: pt(px, py) } }], steps: steps, space: [0.6, 0.8, 1.0] };
      }
      if (c === 2) { var h = hpSpec(r, false), fig = win(); fig.halfplanes = [h.fig];
        steps.push(step('Boundary line: read the slope and the y-intercept.', si(h.m, h.b), 2), step((h.fig.dashed ? 'Dashed line: < or >.' : 'Solid line: ≤ or ≥.') + ' Shading ' + (/>|ge/.test(h.rel) ? 'above: y is greater.' : 'below: y is less.'), h.tex, 2));
        return { variant: 'iq' + c, prompt: 'Write the inequality shown by the graph.', fig: fig, parts: [{ answer: M(h.tex), check: { type: 'ineq2', want: 'inequality' } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 3 || c === 5 || c === 6) { var A = hpSpec(r, c === 6), B = hpSpec(r, false), f2 = win(); need(!A.m.eq(B.m)); f2.halfplanes = [A.fig, B.fig];
        if (c === 3) { var cands = []; for (var x = -5; x <= 5; x++) for (var y = -5; y <= 5; y++) if (inside(A, x, y) && inside(B, x, y) && !F(y).eq(A.m.mul(x).add(A.b)) && !F(y).eq(B.m.mul(x).add(B.b))) cands.push([x, y]);
          need(cands.length >= 6); var P = r.pick(cands);
          steps.push(step('The solution is where the two shadings overlap.', '', 2), step('Pick a point inside the overlap (not on a dashed line) and check it in both inequalities.', pt(P[0], P[1]), 2));
          return { variant: 'iq3', prompt: 'The graph shows a system of linear inequalities. Name one point that is a solution of the system.', fig: f2, parts: [{ answer: M(pt(P[0], P[1])) + ' (any point in the overlap)', check: { type: 'ineq2', want: 'point-in' } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
        steps.push(step('Write each boundary line, then decide solid or dashed and the shaded side.', '', 2), step('The system:', A.tex + ',\\ ' + B.tex, 2));
        return { variant: 'iq' + c, prompt: 'Write the system of inequalities shown by the graph.', fig: f2, parts: [{ answer: M(A.tex) + ' and ' + M(B.tex), check: { type: 'ineq2', want: 'inequality' } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      // c7: a system of inequalities from a situation, and a check
      var J = r.pick(JOBS), pa = r.int(6, 15), pb = r.int(3, pa - 1), N = r.int(4, 12) * 10, T = r.int(Math.ceil(pb * N / 10) + 1, Math.floor(pa * N / 10) - 1) * 10, ta = r.int(5, N - 5), tb = r.int(5, N - ta);
      need(T > pb * N && T < pa * N);
      var story = J[0] + pa + J[1] + pb + J[2] + N + J[3] + T + J[4], ok = ta + tb <= N && pa * ta + pb * tb >= T;
      var hr = [[1, 1, { n: 2 }, 'le'], [{ n: 0 }, { n: 1 }, { n: 3 }, 'ge']];
      steps.push(step('Count: at most ' + N + '.', 'x+y\\le ' + N, 1), step('Money: at least ' + T + '.', lin([[pa, 'x'], [pb, 'y']]) + '\\ge ' + T, 2), step('Substitute the point into both inequalities.', '', 1));
      return { variant: 'iq7', prompt: story + ' Let ' + M('x') + ' be the number of ' + J[5] + ' and ' + M('y') + ' the number of ' + J[6] + '.',
        parts: [{ label: 'a', prompt: 'Write a system of inequalities for the situation.', answer: M('x+y\\le ' + N) + ' and ' + M(lin([[pa, 'x'], [pb, 'y']]) + '\\ge ' + T), check: { type: 'ineq2', want: 'inequality', hrows: hr } },
          { label: 'b', prompt: 'Can they sell ' + ta + ' ' + J[5] + ' and ' + tb + ' ' + J[6] + ', the point ' + M(pt(ta, tb)) + '? Explain.', answer: ok ? 'Yes: it satisfies both inequalities.' : 'No: it does not satisfy both inequalities.', check: { type: 'ineq2', want: 'is-solution', hrows: hr, point: pt(ta, tb) } }], steps: steps, space: [1.0, 1.2, 1.4] };
    }
  });

  /* ================= GRAPH BY HAND (the key shows the finished graph; the verifier reads it back) ================= */
  skill({
    id: 'graph-hand', best: [0, 1, 2], tag: 'INEQ', name: 'Graph systems and inequalities by hand',
    blurb: 'Graph one inequality: solid or dashed, which side to shade (CP2) → graph a system of equations and read the solution (CP1) → graph and shade a system of inequalities, fraction slopes, standard form first (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], blank = win(), key = win();
      if (c <= 2) {
        var h = hpSpec(r, false);
        if (c === 1) need(h.rel === 'ge' || h.rel === 'le'); else need(h.rel === '>' || h.rel === '<');
        key.halfplanes = [h.fig];
        steps.push(step('Graph the boundary line ' + M(si(h.m, h.b)) + ': start at ' + M(pt(0, h.b)) + ', then use the slope.', '', 2));
        steps.push(step((h.fig.dashed ? 'Use a dashed line (< or >).' : 'Use a solid line (≤ or ≥).') + ' Shade ' + (/>|ge/.test(h.rel) ? 'above' : 'below') + ' the line.', '', 2));
        return { variant: 'gh' + c, prompt: 'Graph ' + M(h.tex) + ' on the grid.', fig: blank,
          parts: [{ answer: 'Boundary ' + M(si(h.m, h.b)) + ' (' + (h.fig.dashed ? 'dashed' : 'solid') + '), shaded ' + (/>|ge/.test(h.rel) ? 'above' : 'below') + '.', answerFig: key, check: { type: 'graph-key', ineqs: [h.tex] } }], steps: steps, space: [0.5, 0.6, 0.7] };
      }
      if (c <= 4) {
        var x0 = r.int(-4, 4), y0 = r.int(-4, 4), m1 = slopePick(r, false), m2 = slopePick(r, c === 4); need(!m1.eq(m2));
        var e1 = si(m1, F(y0).sub(m1.mul(x0))), e2 = si(m2, F(y0).sub(m2.mul(x0)));
        key.segs = [lineSeg(m1, x0, y0), lineSeg(m2, x0, y0)]; key.points = [{ x: x0, y: y0 }];
        steps.push(step('Graph each line from its y-intercept and slope.', '', 2), step('The lines cross at the solution.', pt(x0, y0), 2));
        return { variant: 'gh' + c, prompt: 'Solve the system by graphing: ' + sysTeX(e1, e2) + '.', fig: blank,
          parts: [{ answer: 'Solution: ' + M(pt(x0, y0)), answerFig: key, check: { type: 'graph-key', eqs: [e1, e2] } }], steps: steps, space: [0.5, 0.6, 0.7] };
      }
      var A = hpSpec(r, c >= 6), B = hpSpec(r, false); need(!A.m.eq(B.m));
      var texA = A.tex;
      if (c === 7) {   // the first inequality in standard form: −m·x + y (rel) b, cleared of fractions
        var d = A.m.d, n = A.m.n; texA = lin([[-n, 'x'], [d, 'y']]) + RELTEX[A.rel] + num(A.b * d);
        steps.push(step('Solve the first inequality for ' + M('y') + '.', A.tex, 2));
      }
      key.halfplanes = [A.fig, B.fig];
      steps.push(step('Graph each boundary line; dashed for < or >, solid for ≤ or ≥.', '', 2), step('Shade each side; the solution is where the shadings overlap.', '', 2));
      return { variant: 'gh' + c, prompt: 'Graph the system of inequalities and shade the solution: ' + sysTeX(texA, B.tex) + '.', fig: blank,
        parts: [{ answer: 'Boundaries ' + M(si(A.m, A.b)) + ' (' + (A.fig.dashed ? 'dashed' : 'solid') + ', shade ' + (/>|ge/.test(A.rel) ? 'above' : 'below') + ') and ' + M(si(B.m, B.b)) + ' (' + (B.fig.dashed ? 'dashed' : 'solid') + ', shade ' + (/>|ge/.test(B.rel) ? 'above' : 'below') + '); the solution is the overlap.',
          answerFig: key, check: { type: 'graph-key', ineqs: [texA, B.tex] } }], steps: steps, space: [0.5, 0.6, 0.7] };
    }
  });


  // Lesson-specific aliases of independently verified generators; these remain selectable skills.
  (function(){var base=skills.find(function(s){return s.id==="graph-hand";});if(!base)return;
    skill({id:"graph-coordinate-inequality",best:base.best,tag:base.tag,name:"Graph a linear inequality in two variables",blurb:"Plot the boundary line and choose the correct shaded half-plane.",
      difficultyProfile:'focused',fixedDifficulty:1,generate:function(ctx){return base.generate(Object.assign({},ctx,{c:1}));}});
  })();
  (function(){var base=skills.find(function(s){return s.id==="graph-hand";});if(!base)return;
    skill({id:"graph-dashed-inequality",best:base.best,tag:base.tag,name:"Graph strict linear inequalities in two variables",blurb:"Use a dashed line and shade the correct half-plane.",
      difficultyProfile:'focused',fixedDifficulty:2,generate:function(ctx){return base.generate(Object.assign({},ctx,{c:2}));}});
  })();
  (function(){var base=skills.find(function(x){return x.id==='graph-hand';});if(base)skill({id:'graph-two-lines',best:[0,1],tag:'GRAPH',name:'Solve systems by graphing two lines',blurb:'Plot two points for each line and identify the intersection.',difficultyProfile:'focused',fixedDifficulty:3,generate:function(ctx){return base.generate(Object.assign({},ctx,{c:3}));}});})();
  NS.registerSkillSet({
    id: 'algebra1-systems-of-equations', course: 'algebra1', courseName: 'Algebra 1', unit: 'systems-of-equations', unitName: 'Systems of Equations and Inequalities',
    title: 'The Intersection Inn',
    tags: { GRAPH: 'Solutions and graphs', SUBST: 'Substitution', ELIM: 'Elimination', APPLY: 'Systems in context', INEQ: 'Inequalities in two variables' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Solutions</h4><p>A solution makes <b>every</b> equation true: the point where the lines cross.</p></section>' +
      '<section><h4>How many?</h4><p>Different slopes: one. Same slope, different intercept: none. Same line: infinitely many.</p></section>' +
      '<section><h4>Substitution</h4><p>Isolate a variable, substitute it into the other equation, solve, substitute back.</p></section>' +
      '<section><h4>Elimination</h4><p>Multiply so one variable has opposite coefficients, add, solve, substitute back.</p></section>' +
      '<section><h4>Inequalities</h4><p>⟨<⟩, ⟨>⟩: dashed line. ⟨\\le⟩, ⟨\\ge⟩: solid line. ⟨y>⟩: shade above.</p></section>' +
      '</div>',
    gaps: ['Three-variable systems and nonlinear systems are not generated. Graphs drawn by students are checked against the key graph by the teacher.'],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
