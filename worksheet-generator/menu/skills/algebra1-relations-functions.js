/* Menu Assessment Generator — Algebra 1 · Unit 4 Relations and Functions (roadmap days 41–56).
   Skill groups: RELATIONS (domain, range, is it a function), NOTATION (function notation, reading
   values from tables and graphs), REPRESENT (tables ↔ rules), RATE (rate of change, interpreting
   graphs), SEQUENCE (arithmetic sequences as functions).
   Figures (coordinate graphs, tables, mapping diagrams) are data specs drawn by menu/figures.js; the
   verifier reads the drawn SVG/HTML back, so every answer is checked against what students see. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, Fr = K.Fr, M = K.M, num = K.num, lin = K.lin;
  var need = K.need, F = K.F, nz = K.nz, step = K.step, axb = K.axb, gcd = K.gcd;
  var skills = [];
  function skill(d) { skills.push(d); return d; }
  function t(v) { return v < 0 ? '−' + Math.abs(v) : String(v); }          // plain-text number
  function setTeX(vals) { return '\\{' + vals.map(function (v) { return num(v); }).join(',\\ ') + '\\}'; }
  function uniqSorted(a) { return a.slice().sort(function (p, q) { return p - q; }).filter(function (v, i, arr) { return i === 0 || arr[i - 1] !== v; }); }
  function pairsTeX(pairs) { return pairs.map(function (p) { return '(' + num(p[0]) + ',\\ ' + num(p[1]) + ')'; }).join(',\\ '); }
  function distinctXs(r, n, lo, hi) { var xs = []; while (xs.length < n) { var x = r.int(lo, hi); if (xs.indexOf(x) < 0) xs.push(x); } return xs; }
  function plane(win, extra) { return Object.assign({ kind: 'plane', xmin: win[0], xmax: win[1], ymin: win[2], ymax: win[3], points: [], segs: [], curves: [] }, extra || {}); }
  function rangeWord(axis) { return axis === 'x' ? 'Domain' : 'Range'; }
  function ineqTeX(v, lo, loIn, hi, hiIn) {
    if (lo === null) return v + (hiIn ? '\\le ' : '<') + num(hi);
    if (hi === null) return v + (loIn ? '\\ge ' : '>') + num(lo);
    return num(lo) + (loIn ? '\\le ' : '<') + v + (hiIn ? '\\le ' : '<') + num(hi);
  }

  /* ================= RELATIONS · domain and range ================= */
  skill({
    id: 'domain-range', best: [0, 1, 2], tag: 'RELATIONS', name: 'Find the domain and range',
    blurb: 'Ordered pairs and tables (CP2) → mapping diagrams and plotted points (CP1) → graphs with closed/open endpoints and arrows (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, prompt, fig = null, pairsChk = null, steps = [], parts;
      if (c <= 4) {
        var n = r.int(4, 6), xs = distinctXs(r, n, c === 1 ? 0 : -6, 9), ys = xs.map(function () { return c === 1 ? r.int(0, 9) : r.int(-8, 9); });
        if (r.chance(0.6)) ys[r.int(1, n - 1)] = ys[0];                                     // a repeated output
        var pairs = xs.map(function (x, i) { return [x, ys[i]]; });
        if (c >= 3) { var jx = r.int(0, n - 1), oy = ys[jx] + r.pick([-4, -3, 3, 4]); need(Math.abs(oy) <= 9); pairs.push([xs[jx], oy]); ys = ys.concat([oy]); }   // one input used twice: list it once
        if (c === 1) { pairsChk = pairsTeX(pairs); prompt = 'Find the domain and range of the relation ' + M(pairsChk) + '.'; }
        else if (c === 2) { fig = { kind: 'table', vertical: true, head: ['x', 'y'], rows: pairs }; prompt = 'Find the domain and range of the relation in the table.'; }
        else if (c === 3) {
          var L = uniqSorted(xs), R = uniqSorted(ys);
          fig = { kind: 'mapping', left: L, right: R, arrows: pairs.map(function (p) { return [L.indexOf(p[0]), R.indexOf(p[1])]; }) };
          prompt = 'Find the domain and range of the relation shown in the mapping diagram.';
        } else { fig = plane([-7, 7, -7, 7], { points: pairs.map(function (p) { return { x: p[0], y: Math.max(-7, Math.min(7, p[1])) }; }) }); pairs = fig.points.map(function (p) { return [p.x, p.y]; }); prompt = 'Find the domain and range of the relation graphed below.'; }
        var D = uniqSorted(pairs.map(function (p) { return p[0]; })), Rg = uniqSorted(pairs.map(function (p) { return p[1]; }));
        steps.push(step('Domain: list each x-value once.', setTeX(D), 2), step('Range: list each y-value once (repeats count once).', setTeX(Rg), 2));
        parts = [{ answer: 'Domain: ' + M(setTeX(D)), check: { type: 'domain-range', want: 'domain', pairs: pairsChk } },
                 { answer: 'Range: ' + M(setTeX(Rg)), check: { type: 'domain-range', want: 'range', pairs: pairsChk } }];
        return { variant: 'dr-' + c, prompt: prompt, fig: fig, parts: parts, steps: steps, space: [0.6, 0.8, 1.0] };
      }
      // graphs: a segment (c5), a segment or ray with an open end (c6), two connected pieces (c7)
      var win = [-7, 7, -7, 7], segs = [];
      var ax = r.int(-6, -1), bx = r.int(1, 6), ay = r.int(-6, 6), by = r.int(-6, 6); need(ay !== by);
      if (c === 5) segs.push({ a: [ax, ay], b: [bx, by], aEnd: 'closed', bEnd: 'closed' });
      else if (c === 6) { var ends = r.pick([['closed', 'open'], ['open', 'closed'], ['closed', 'arrow'], ['arrow', 'closed'], ['open', 'arrow']]); segs.push({ a: [ax, ay], b: [bx, by], aEnd: ends[0], bEnd: ends[1] }); }
      else { var mx = r.int(ax + 1, bx - 1), my = r.int(-6, 6); need(my !== ay && my !== by && (my - ay) * (by - my) < 0); segs.push({ a: [ax, ay], b: [mx, my], aEnd: r.pick(['closed', 'open']), bEnd: 'none' }, { a: [mx, my], b: [bx, by], aEnd: 'none', bEnd: r.pick(['closed', 'open', 'arrow']) }); }
      fig = plane(win, { segs: segs });
      // answers from the generator's own geometry (the verifier re-reads the picture)
      function span(k) {
        var lo = null, hi = null, loIn = false, hiIn = false, loInf = false, hiInf = false;
        segs.forEach(function (sg) {
          [['a', sg.a, sg.aEnd, sg.b], ['b', sg.b, sg.bEnd, sg.a]].forEach(function (e) {
            var v = e[1][k], inc = e[2] !== 'open', inf = e[2] === 'arrow';
            if (inf) { if (e[1][k] < e[3][k]) loInf = true; else if (e[1][k] > e[3][k]) hiInf = true; return; }
            if (lo === null || v < lo || (v === lo && inc)) { if (lo === null || v < lo) { lo = v; loIn = inc; } else loIn = loIn || inc; }
            if (hi === null || v > hi || (v === hi && inc)) { if (hi === null || v > hi) { hi = v; hiIn = inc; } else hiIn = hiIn || inc; }
          });
        });
        return ineqTeX(k ? 'y' : 'x', loInf ? null : lo, loIn, hiInf ? null : hi, hiIn);
      }
      var dTeX = span(0), rTeX = span(1);
      steps.push(step('Domain: read the x-values from the leftmost to the rightmost point (open circle: not included; arrow: keeps going).', dTeX, 2),
                 step('Range: read the y-values from the lowest to the highest point.', rTeX, 2));
      return { variant: 'dr-graph' + c, prompt: 'Write the domain and range of the graphed relation as inequalities.', fig: fig,
        parts: [{ answer: 'Domain: ' + M(dTeX), check: { type: 'domain-range', want: 'domain' } }, { answer: 'Range: ' + M(rTeX), check: { type: 'domain-range', want: 'range' } }],
        steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= RELATIONS · is it a function? ================= */
  skill({
    id: 'is-function', best: [0, 1], tag: 'RELATIONS', name: 'Decide whether a relation is a function',
    blurb: 'Ordered pairs and tables (CP2) → mapping diagrams and graphs, the vertical line test (CP1) → curves and equations such as x = y² (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, isF = r.chance(0.5), fig = null, chk = { type: 'is-function' }, prompt, why;
      if (c <= 4) {
        var n = r.int(4, 5) + (c === 3 ? 1 : 0), xs = distinctXs(r, n, -6, 9), ys = xs.map(function () { return r.int(-8, 9); }), pairs = xs.map(function (x, i) { return [x, ys[i]]; });
        if (!isF) { var j = r.int(0, n - 1); var other = ys[j] + r.pick([-3, -2, 2, 3, 5]); pairs.splice(r.int(0, n), 0, [xs[j], other]); why = M('x=' + num(xs[j])) + ' is paired with both ' + M(num(ys[j])) + ' and ' + M(num(other)) + '.'; }
        else why = 'every x-value appears with exactly one y-value.';
        if (c === 1) { chk.pairs = pairsTeX(pairs); prompt = 'Is the relation ' + M(chk.pairs) + ' a function? Explain.'; }
        else if (c === 2) { fig = { kind: 'table', vertical: true, head: ['x', 'y'], rows: pairs }; prompt = 'Does the table represent a function? Explain.'; }
        else if (c === 3) { var L = uniqSorted(pairs.map(function (p) { return p[0]; })), R = uniqSorted(pairs.map(function (p) { return p[1]; })); fig = { kind: 'mapping', left: L, right: R, arrows: pairs.map(function (p) { return [L.indexOf(p[0]), R.indexOf(p[1])]; }) }; prompt = 'Is the relation in the mapping diagram a function? Explain.'; }
        else { fig = plane([-7, 7, -7, 7], { points: pairs.map(function (p) { return { x: p[0] > 7 ? 7 : p[0], y: Math.max(-7, Math.min(7, p[1])) }; }) }); prompt = 'Is the graphed relation a function? Use the vertical line test.';
          var seen = {}; isF = true; fig.points.forEach(function (p) { if (seen[p.x] !== undefined && seen[p.x] !== p.y) isF = false; seen[p.x] = p.y; });
          why = isF ? 'no vertical line passes through two points.' : 'a vertical line passes through two of the points.'; }
      } else if (c <= 6) {
        var shape = c === 6 ? 'split' : r.pick(isF ? ['parab', 'abs', 'line', 'v'] : ['sideparab', 'circle', 'vertical', 'sidev']);
        var pl = plane([-6, 6, -6, 6]), h = r.int(-2, 2), k = r.int(-2, 2);
        if (shape === 'split') { var k2 = k + r.pick([-3, -2, 2, 3]); pl.segs.push({ a: [-6, k + r.int(-2, 2)], b: [h, k], aEnd: 'arrow', bEnd: 'closed' }, { a: [h, k2], b: [6, k2 + r.int(-3, 3)], aEnd: isF ? 'open' : 'closed', bEnd: 'arrow' }); }
        if (shape === 'line') pl.segs.push({ a: [-5, k - 2], b: [5, k + 2], aEnd: 'arrow', bEnd: 'arrow' });
        if (shape === 'v') pl.segs.push({ a: [h - 4, k + 4], b: [h, k], aEnd: 'arrow', bEnd: 'none' }, { a: [h, k], b: [h + 4, k + 4], aEnd: 'none', bEnd: 'arrow' });
        if (shape === 'vertical') pl.segs.push({ a: [h, -5], b: [h, 5], aEnd: 'arrow', bEnd: 'arrow' });
        if (shape === 'sidev') pl.segs.push({ a: [h + 4, k + 4], b: [h, k], aEnd: 'arrow', bEnd: 'none' }, { a: [h, k], b: [h + 4, k - 4], aEnd: 'none', bEnd: 'arrow' });
        if (shape === 'parab') pl.curves.push([-2, -1, 0, 1, 2].map(function (u) { return [h + u, k - 2 + u * u]; }));
        if (shape === 'abs') pl.curves.push([[h - 3, k + 1], [h, k - 2], [h + 3, k + 1]]);
        if (shape === 'sideparab') pl.curves.push([-2, -1, 0, 1, 2].map(function (u) { return [h - 2 + u * u, k + u]; }));
        if (shape === 'circle') pl.curves.push([[h + 3, k], [h + 2, k + 2], [h, k + 3], [h - 2, k + 2], [h - 3, k], [h - 2, k - 2], [h, k - 3], [h + 2, k - 2], [h + 3, k]]);
        fig = pl; prompt = 'Use the vertical line test: is the graphed relation a function? Explain.';
        why = isF ? 'every vertical line crosses the graph at most once.' : 'some vertical line crosses the graph more than once.';
        if (shape === 'split') why = isF ? 'at ' + M('x=' + num(h)) + ' the open circle is not on the graph, so each x has one y.' : 'at ' + M('x=' + num(h)) + ' both closed dots are on the graph, so that x has two y-values.';
      } else {
        var a = r.int(1, 4), b = nz(r, -6, 6), form = r.pick(isF ? ['y=x^2', 'y=|x|', 'y=lin'] : ['x=y^2', 'x+y^2', 'x=|y|']);
        var eqn = { 'y=x^2': 'y=' + lin([[a, 'x^2'], [b, '']]), 'y=|x|': 'y=' + (a === 1 ? '' : a) + '|x|' + K.addConst('', b), 'y=lin': lin([[a, 'x'], [1, 'y']]) + '=' + b,
          'x=y^2': 'x=' + lin([[a, 'y^2'], [b, '']]), 'x+y^2': lin([[1, 'x'], [1, 'y^2']]) + '=' + Math.abs(b) * 3, 'x=|y|': 'x=' + (a === 1 ? '' : a) + '|y|' + K.addConst('', b) }[form];
        chk.equation = eqn; prompt = 'Is ' + M('y') + ' a function of ' + M('x') + ' for ' + M(eqn) + '? Explain.';
        why = isF ? 'each x-value gives exactly one y-value.' : 'some x-values give two y-values (a positive and a negative y).';
      }
      if (fig) need(!(fig.kind === 'plane' && !fig.points.length && !fig.segs.length && !fig.curves.length));
      return { variant: 'isf-' + c + (isF ? 'y' : 'n'), prompt: prompt, fig: fig,
        parts: [{ answer: (isF ? 'Yes, ' : 'No, ') + why, check: chk }],
        steps: [step(isF ? 'Each input has exactly one output.' : 'Find an input with two different outputs.', '', 2), step('Conclusion: ' + (isF ? 'it is a function.' : 'it is not a function.'), '', 2)], space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= NOTATION · evaluate and solve with function notation ================= */
  skill({
    id: 'func-eval', best: [0, 1], tag: 'NOTATION', name: 'Use function notation',
    blurb: 'Evaluate f(4) for a linear rule (CP2) → negative inputs, quadratics, solve f(x) = k (CP1) → combine two functions, f(a + 2) (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, a = r.int(2, 6), b = nz(r, -9, 9), rule, steps = [], chk, ans, prompt, x;
      if (c <= 2) { rule = 'f(x)=' + axb(c === 1 ? a : -a, b); x = c === 1 ? r.int(1, 8) : -r.int(1, 7); var call = 'f(' + num(x) + ')', val = (c === 1 ? a : -a) * x + b;
        prompt = 'For ' + M(rule) + ', find ' + M(call) + '.'; chk = { type: 'func-eval', rule: rule, expr: call }; ans = M(call + '=' + val);
        steps.push(step('Replace x with ' + M(num(x)) + '.', (c === 1 ? a : -a) + '(' + num(x) + ')' + K.addConst('', b), 2), step('Simplify.', String(val), 2)); }
      else if (c === 3) { var p = nz(r, -5, 5), q = nz(r, -9, 9); rule = 'f(x)=' + lin([[1, 'x^2'], [p, 'x'], [q, '']]); x = nz(r, -4, 4); var call3 = 'f(' + num(x) + ')', v3 = x * x + p * x + q;
        prompt = 'For ' + M(rule) + ', find ' + M(call3) + '.'; chk = { type: 'func-eval', rule: rule, expr: call3 }; ans = M(call3 + '=' + v3);
        steps.push(step('Substitute with parentheses.', '(' + num(x) + ')^2' + K.addX('', p, '(' + num(x) + ')').replace('x', '') + K.addConst('', q), 2), step('Simplify.', String(v3), 2)); }
      else if (c === 4) { var m4 = r.int(2, 7) * r.sign(); x = nz(r, -9, 9); var k4 = m4 * x + b; rule = 'f(x)=' + axb(m4, b);
        prompt = 'For ' + M(rule) + ', find ' + M('x') + ' so that ' + M('f(x)=' + k4) + '.'; chk = { type: 'func-solve', rule: rule, value: String(k4), v: 'x' }; ans = M('x=' + x);
        steps.push(step('Set the rule equal to ' + k4 + '.', axb(m4, b) + '=' + k4, 2), step('Solve.', 'x=' + x, 2)); }
      else if (c === 6) { var g = 'g(x)=' + lin([[1, 'x^2'], [nz(r, -4, 4), '']]); rule = 'f(x)=' + axb(a, b); var u = nz(r, -4, 4), w = nz(r, -3, 3), co = r.int(2, 3);
        var expr = co + 'f(' + num(u) + ')-g(' + num(w) + ')';
        var vf = a * u + b, vg = w * w + Number((g.split('x^2')[1] || '0').replace(/\s/g, '') || 0), v5 = co * vf - vg;
        prompt = 'For ' + M(rule) + ' and ' + M(g) + ', find ' + M(expr) + '.'; chk = { type: 'func-combo', rules: [rule, g], expr: expr }; ans = M(String(v5));
        steps.push(step('Find each value: ' + M('f(' + num(u) + ')=' + vf) + ', ' + M('g(' + num(w) + ')=' + vg) + '.', '', 2), step('Combine.', co + '(' + num(vf) + ')-(' + num(vg) + ')=' + v5, 2)); }
      else if (c === 5) { var p6 = nz(r, -3, 3), q6 = nz(r, -6, 6), lead = r.int(2, 3) * r.sign(); rule = 'f(x)=' + lin([[lead, 'x^2'], [p6, 'x'], [q6, '']]); x = nz(r, -3, 3); var call6 = 'f(' + num(x) + ')', v6 = lead * x * x + p6 * x + q6;
        prompt = 'For ' + M(rule) + ', find ' + M(call6) + '.'; chk = { type: 'func-eval', rule: rule, expr: call6 }; ans = M(call6 + '=' + v6);
        steps.push(step('Substitute; square first, then multiply.', '', 2), step('Simplify.', String(v6), 2)); }
      else { var m7 = nz(r, -5, 5), b7 = nz(r, -9, 9), k7 = r.int(2, 4) * r.sign(), h7 = nz(r, -5, 5); rule = 'f(x)=' + axb(m7, b7); var inner7 = lin([[k7, 'a'], [h7, '']]), call7 = 'f(' + inner7 + ')';
        var res7 = lin([[m7 * k7, 'a'], [m7 * h7 + b7, '']]), xs7 = nz(r, -9, 9), val7 = m7 * xs7 + b7;
        prompt = 'For ' + M(rule) + ':';
        var parts7 = [{ label: 'a', prompt: 'Find and simplify ' + M(call7) + '.', answer: M(call7 + '=' + res7), check: { type: 'func-eval', rule: rule, expr: call7, symbolic: true } },
                      { label: 'b', prompt: 'Find ' + M('x') + ' so that ' + M('f(x)=' + val7) + '.', answer: M('x=' + xs7), check: { type: 'func-solve', rule: rule, value: String(val7), v: 'x' } }];
        steps.push(step('(a) Replace x with ' + M('(' + inner7 + ')') + ', then distribute and combine.', num(m7) + '(' + inner7 + ')' + K.addConst('', b7) + '=' + res7, 2), step('(b) Set the rule equal to ' + val7 + ' and solve.', 'x=' + xs7, 2));
        return { variant: 'fe7', prompt: prompt, parts: parts7, steps: steps, space: [0.9, 1.1, 1.3] }; }
      return { variant: 'fe' + c, prompt: prompt, parts: [{ answer: ans, check: chk }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= NOTATION · read values from tables and graphs ================= */
  skill({
    id: 'read-func', best: [0, 1], tag: 'NOTATION', name: 'Read function values from tables and graphs',
    blurb: 'Find f(a) in a table (CP2) → read a graph, find x when f(x) = k (CP1) → piecewise graphs with two solutions (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, fig, parts, steps = [];
      if (c <= 2) {
        var xs = c === 1 ? [0, 1, 2, 3, 4] : distinctXs(r, 5, -4, 6).sort(function (p, q) { return p - q; }), ys = xs.map(function () { return r.int(-9, 12); });
        fig = { kind: 'table', head: ['x', 'f(x)'], rows: xs.map(function (x, i) { return [x, ys[i]]; }) };
        var i0 = r.int(0, 4), kIdx = r.int(0, 4); need(ys.filter(function (y) { return y === ys[kIdx]; }).length === 1 && kIdx !== i0);
        parts = [{ label: 'a', prompt: 'Find ' + M('f(' + num(xs[i0]) + ')') + '.', answer: M('f(' + num(xs[i0]) + ')=' + ys[i0]), check: { type: 'read-fig', want: 'value', at: String(xs[i0]) } },
                 { label: 'b', prompt: 'Find ' + M('x') + ' when ' + M('f(x)=' + ys[kIdx]) + '.', answer: M('x=' + xs[kIdx]), check: { type: 'read-fig', want: 'inputs', k: String(ys[kIdx]) } }];
        steps.push(step('(a) Find the column with x = ' + t(xs[i0]) + ' and read f(x).', '', 2), step('(b) Find ' + t(ys[kIdx]) + ' in the f(x) row and read x.', '', 2));
        return { variant: 'rt' + c, prompt: 'Use the table.', fig: fig, parts: parts, steps: steps, space: [0.5, 0.7, 0.9] };
      }
      // a connected piecewise-linear graph through integer vertices
      var win = [-7, 7, -7, 7], verts, nPieces = c <= 4 ? 1 : c === 5 ? 2 : 3;
      var slopes = c === 3 ? [1, 2, -1, -2] : c === 4 ? [0.5, -0.5, 1, -1, 2, -2] : [1, 2, -1, -2, 0.5, -0.5];
      verts = [[r.int(-6, -3), r.int(-5, 5)]];
      for (var pc = 0; pc < nPieces; pc++) {
        var last = verts[verts.length - 1], sl = r.pick(slopes);
        if (nPieces > 1 && pc === 0) sl = -Math.abs(sl); if (nPieces > 1 && pc === nPieces - 1) sl = Math.abs(sl); if (nPieces === 3 && pc === 1) sl = r.pick([0, sl > 0 ? sl : -sl]);
        var runs = (Math.abs(sl) === 0.5 ? [2, 4, 6] : nPieces === 1 ? [4, 5, 6, 7, 8, 9] : [2, 3, 4]).filter(function (rn) { return last[0] + rn <= 6 && Math.abs(last[1] + sl * rn) <= 6 && Number.isInteger(sl * rn); });
        need(runs.length > 0); var run = r.pick(runs);
        verts.push([last[0] + run, last[1] + sl * run]);
      }
      need(verts.every(function (v) { return Number.isInteger(v[1]) && Math.abs(v[1]) <= 6; }) && verts[verts.length - 1][0] <= 6);
      var segs = []; for (var vi = 0; vi + 1 < verts.length; vi++) segs.push({ a: verts[vi], b: verts[vi + 1], aEnd: vi === 0 ? 'closed' : 'none', bEnd: vi + 2 === verts.length ? 'closed' : 'none' });
      fig = plane(win, { segs: segs });
      function yAt(x) { var out = []; segs.forEach(function (sg) { if (x >= sg.a[0] && x <= sg.b[0]) out.push(sg.a[1] + (sg.b[1] - sg.a[1]) * (x - sg.a[0]) / (sg.b[0] - sg.a[0])); }); return out.filter(function (v, i, arr) { return arr.indexOf(v) === i; }); }
      function solveK(k) { var out = [], flat = false; segs.forEach(function (sg) { if (sg.b[1] === sg.a[1]) { if (sg.a[1] === k) flat = true; return; } var tt = (k - sg.a[1]) / (sg.b[1] - sg.a[1]); if (tt >= 0 && tt <= 1) out.push(sg.a[0] + tt * (sg.b[0] - sg.a[0])); }); return flat ? null : out.filter(function (v, i, arr) { return arr.indexOf(v) === i; }).sort(function (p, q) { return p - q; }); }
      var intXs = []; for (var xx = verts[0][0]; xx <= verts[verts.length - 1][0]; xx++) if (Number.isInteger(yAt(xx)[0])) intXs.push(xx);
      var xa = r.pick(intXs.filter(function (x) { return !verts.some(function (v) { return v[0] === x; }) || c >= 4; })), ya = yAt(xa);
      var wantN = c <= 4 ? 1 : 2, kCands = intXs.map(function (x) { return yAt(x)[0]; }).filter(function (k, i, arr) { var sl2 = solveK(k); return arr.indexOf(k) === i && sl2 && sl2.length === wantN && sl2.every(Number.isInteger) && k !== ya[0]; });
      need(kCands.length > 0); var kx = r.pick(kCands), sol = solveK(kx);
      parts = [{ label: 'a', prompt: 'Find ' + M('f(' + num(xa) + ')') + '.', answer: M('f(' + num(xa) + ')=' + num(ya[0])), check: { type: 'read-fig', want: 'value', at: String(xa) } },
               { label: 'b', prompt: (c >= 5 ? 'Find every ' : 'Find the ') + M('x') + ' with ' + M('f(x)=' + kx) + '.', answer: sol.map(function (v) { return M('x=' + v); }).join(' and '), check: { type: 'read-fig', want: 'inputs', k: String(kx) } }];
      steps.push(step('(a) Go to x = ' + t(xa) + ', up or down to the graph, and read y.', '', 2), step('(b) Draw the horizontal line y = ' + t(kx) + ' and read the x-value of every crossing.', '', 2));
      if (c === 7) { var yb = ya[0], yb2 = yAt(yb); need(yb2.length === 1 && Number.isInteger(yb2[0]) && yb !== xa);
        parts.push({ label: 'c', prompt: 'Find ' + M('f(f(' + num(xa) + '))') + '.', answer: M('f(f(' + num(xa) + '))=f(' + num(yb) + ')=' + num(yb2[0])), check: { type: 'read-fig', want: 'value', at: String(yb), inner: String(xa) } });
        steps.push(step('(c) Use the answer to (a) as the new input.', '', 2)); }
      return { variant: 'rg' + nPieces + (c === 7 ? 'c' : ''), prompt: 'The graph shows ' + M('y=f(x)') + '.', fig: fig, parts: parts, steps: steps, space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= REPRESENT · write a rule from a table or graph ================= */
  skill({
    id: 'linear-rule', best: [0, 1, 2], tag: 'REPRESENT', name: 'Write a rule from a table or graph',
    blurb: 'x = 0, 1, 2, 3 with a positive rate (CP2) → negative rates, tables that skip values (CP1) → fraction rates, graphs, “is it linear?” (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, m = c <= 1 ? r.int(2, 6) : nz(r, -6, 6), b = nz(r, -9, 9), fig, xs, steps = [];
      var notLinear = c === 3 && r.chance(0.2);
      if (c <= 2) xs = [0, 1, 2, 3, 4];
      else if (c === 3) { var s0 = r.int(1, 3); xs = [s0, s0 + 1, s0 + 2, s0 + 3]; }
      else if (c === 5) { var st5 = r.shuffle([1, 2, 3, 1, 2]), x5 = -r.int(4, 6); xs = [x5]; st5.slice(0, 4).forEach(function (d5) { xs.push(xs[xs.length - 1] + d5); }); need(xs.indexOf(0) < 0); }
      else if (c === 6 || c === 7) { var dd = r.int(2, 3); m = F(nz(r, -4, 4), dd); need(!m.isInt()); xs = c === 6 ? [dd, 2 * dd, 3 * dd, 4 * dd] : [-3 * dd, -2 * dd, dd, 2 * dd, 4 * dd]; }
      if (c === 4) {
        var half = r.chance(0.7), x0 = r.int(-5, -1), m6 = half ? F(r.pick([-3, -1, 1, 3]), 2) : F(nz(r, -3, 3)), y0 = r.int(-5, 5), x1 = x0 + (half ? 2 * r.int(1, 3) : r.int(2, 5)), y1 = m6.mul(x1 - x0).add(y0); need(y1.isInt() && Math.abs(y1.n) <= 6 && x1 <= 6); y1 = Number(y1.n);
        fig = plane([-7, 7, -7, 7], { segs: [{ a: [x0, y0], b: [x1, y1], aEnd: 'arrow', bEnd: 'arrow' }], points: [{ x: x0, y: y0 }, { x: x1, y: y1 }] });
        var b6 = F(y0).sub(m6.mul(x0)); var rule6 = 'y=' + axb(m6, b6);
        steps.push(step('Slope from the two marked points: rise over run.', 'm=' + num(m6), 2), step('Find b from a point, then write the rule.', rule6, 2));
        return { variant: 'lr-graph', prompt: 'Write an equation for the line through the two marked points.', fig: fig, parts: [{ answer: M(rule6), check: { type: 'linear-rule' } }], steps: steps, space: [0.6, 0.8, 1.0] };
      }
      var rows = xs.map(function (x) { return [x, Fr.of(m).mul(x).add(b)]; });
      if (notLinear) { rows = xs.map(function (x, i) { return [x, F(b + i * i)]; }); }
      rows.forEach(function (rw) { need(rw[1].isInt()); });
      fig = { kind: 'table', head: ['x', 'y'], rows: rows.map(function (rw) { return [rw[0], rw[1].n]; }) };
      var rule = 'y=' + axb(m, b);
      if (notLinear) { steps.push(step('Check the change in y for equal changes in x.', '', 2), step('The changes are not equal, so the table is not linear.', '', 2));
        return { variant: 'lr-notlinear', prompt: 'Is the relationship in the table linear? If it is, write its rule in the form ' + M('y=mx+b') + '.', fig: fig, parts: [{ answer: 'Not linear: as ' + M('x') + ' goes up by ' + (xs[1] - xs[0]) + ' each time, ' + M('y') + ' changes by ' + M(rows.slice(1).map(function (rw, i) { return num(rw[1].sub(rows[i][1])); }).join(',\\ ')) + ', not a constant amount.', check: { type: 'linear-rule' } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      steps.push(step('Rate of change: change in y divided by change in x.', 'm=' + num(m), 2), step('Find the y-value when x = 0 (work back if needed).', 'b=' + num(b), 1), step('Write the rule.', rule, 1));
      if (c === 7) { var X7 = 6 * dd, Y7 = Fr.of(m).mul(X7).add(b); need(Y7.isInt());
        steps.push(step('(b) Substitute x = ' + X7 + ' into the rule.', 'y=' + num(Y7), 2));
        return { variant: 'lr7', prompt: 'The table shows a linear relationship.', fig: fig,
          parts: [{ label: 'a', prompt: 'Write its rule in the form ' + M('y=mx+b') + '.', answer: M(rule), check: { type: 'linear-rule' } },
                  { label: 'b', prompt: 'Predict ' + M('y') + ' when ' + M('x=' + X7) + '.', answer: M('y=' + num(Y7)), check: { type: 'linear-rule', predict: String(X7) } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      return { variant: 'lr' + c, prompt: c === 3 ? 'Is the relationship in the table linear? If it is, write its rule in the form ' + M('y=mx+b') + '.' : 'Write a rule for the table in the form ' + M('y=mx+b') + '.', fig: fig,
        parts: [{ answer: M(rule), check: { type: 'linear-rule' } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= REPRESENT · complete a table from a rule ================= */
  skill({
    id: 'table-fill', best: [0, 1], tag: 'REPRESENT', name: 'Complete a table from a rule',
    blurb: 'Outputs for y = 2x + 1 (CP2) → negative inputs and quadratics (CP1) → missing inputs that must be solved, fraction rules (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, a = c <= 2 ? r.int(2, 5) : nz(r, -5, 5), b = nz(r, -8, 8), rule, f, xs = c <= 2 ? [0, 1, 2, 3, 4] : distinctXs(r, 5, -4, 5).sort(function (p, q) { return p - q; });
      if (c === 4 || c === 5) { var p = nz(r, -3, 3); rule = 'y=' + lin([[1, 'x^2'], [p, 'x'], [b, '']]); f = function (x) { return F(x * x + p * x + b); }; }
      else if (c === 7) { var dd = r.int(2, 3); var fa = F(nz(r, -4, 4), dd); need(!fa.isInt()); rule = 'y=' + axb(fa, b); xs = [-2 * dd, -dd, 0, dd, 2 * dd]; f = function (x) { return fa.mul(x).add(b); }; }
      else { rule = 'y=' + axb(a, b); f = function (x) { return F(a * x + b); }; }
      var rows = xs.map(function (x) { return [x, f(x).n]; }), ans = [];
      var hide = r.shuffle([0, 1, 2, 3, 4]).slice(0, 3).sort();
      var missIn = c >= 6 && !/x\^2/.test(rule) ? hide[0] : -1, missIn2 = c >= 6 ? hide[1] : -1;
      var shown = rows.map(function (rw, i) { if (i === missIn || i === missIn2) return ['?', rw[1]]; if (hide.indexOf(i) >= 0) return [rw[0], '?']; return rw; });
      shown.forEach(function (rw, i) { if (rw[1] === '?') ans.push(rows[i][1]); else if (rw[0] === '?') ans.push(rows[i][0]); });
      return { variant: 'tf' + c, prompt: 'Complete the table for ' + M(rule) + '. List the missing values from left to right.',
        fig: { kind: 'table', head: ['x', 'y'], rows: shown },
        parts: [{ answer: ans.map(function (v) { return M(num(v)); }).join(', '), check: { type: 'table-fill', rule: rule, v: 'x' } }],
        steps: [step('Substitute each x into the rule' + (missIn >= 0 || missIn2 >= 0 ? '; for a missing x, set the rule equal to y and solve.' : '.'), '', 3), step('Missing values: ' + ans.map(t).join(', '), '', 1)], space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= RATE · rate of change ================= */
  var CONTEXTS = [['temperature', '°F', 'hour', 'hours', 'At {x1} hours after noon the temperature was {y1} °F. At {x2} hours after noon it was {y2} °F.'],
    ['water in a tank', 'gallons', 'minute', 'minutes', 'After {x1} minutes a tank held {y1} gallons. After {x2} minutes it held {y2} gallons.'],
    ['savings', 'dollars', 'week', 'weeks', 'After {x1} weeks Jordan had saved {y1} dollars. After {x2} weeks Jordan had {y2} dollars.'],
    ['height of a plant', 'cm', 'day', 'days', 'On day {x1} a plant was {y1} cm tall. On day {x2} it was {y2} cm tall.']];
  skill({
    id: 'rate-of-change', best: [0, 1, 2], tag: 'RATE', name: 'Find and interpret rate of change',
    blurb: 'Between two points (CP2) → from tables, graphs and words with units (CP1) → average rate of change of nonlinear functions, comparing intervals (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], prompt, fig = null, chk, ans, rate;
      if (c === 1 || c === 2) { var x1 = r.int(-6, 3), dx = r.int(1, 5), m = c === 1 ? r.int(1, 5) : nz(r, -6, 6), y1 = r.int(-8, 8), x2 = x1 + dx, y2 = y1 + m * dx;
        var pts = '(' + num(x1) + ',\\ ' + num(y1) + '),\\ (' + num(x2) + ',\\ ' + num(y2) + ')'; fig = null;
        prompt = 'Find the rate of change between the points ' + M(pts) + '.'; chk = { type: 'rate', pairs: pts }; rate = F(m);
        steps.push(step('Change in y over change in x.', '\\frac{' + num(y2) + '-' + (y1 < 0 ? '(' + y1 + ')' : y1) + '}{' + num(x2) + '-' + (x1 < 0 ? '(' + x1 + ')' : x1) + '}=' + m, 3)); }
      else if (c === 3) { var m3 = nz(r, -6, 6), b3 = nz(r, -9, 9), xs = [0, 2, 4, 6]; fig = { kind: 'table', head: ['x', 'y'], rows: xs.map(function (x) { return [x, m3 * x + b3]; }) };
        prompt = 'The table shows a linear function. Find its rate of change.'; chk = { type: 'rate', constant: true }; rate = F(m3);
        steps.push(step('Use any two rows: change in y over change in x.', 'm=' + m3, 3)); }
      else if (c === 4) { var cx = r.pick(CONTEXTS), a1 = r.int(1, 4), a2 = a1 + r.int(2, 6), sgn = r.sign(), mm = r.int(2, 9) * sgn, v1 = r.int(20, 80), v2 = v1 + mm * (a2 - a1); need(v2 > 0);
        prompt = cx[4].replace('{x1}', a1).replace('{y1}', v1).replace('{x2}', a2).replace('{y2}', v2) + ' Find the average rate of change and explain what it means.';
        chk = { type: 'rate', words: [0, 1, 2, 3] }; rate = F(mm);
        steps.push(step('Rate = change in ' + cx[1] + ' ÷ change in ' + cx[3] + '.', '\\frac{' + v2 + '-' + v1 + '}{' + a2 + '-' + a1 + '}=' + mm, 3), step('Interpret with units.', '', 1));
        ans = M(String(mm)) + ' ' + cx[1] + ' per ' + cx[2] + ': the ' + cx[0] + (mm > 0 ? ' increased' : ' decreased') + ' by ' + Math.abs(mm) + ' ' + cx[1] + ' each ' + cx[2] + ' on average.'; }
      else if (c === 5 || c === 7) { var p = nz(r, -4, 4), q = nz(r, -6, 6), xs5 = [-2, -1, 0, 1, 2, 3, 4]; fig = { kind: 'table', head: ['x', 'f(x)'], rows: xs5.map(function (x) { return [x, x * x + p * x + q]; }) };
        var A = r.int(-2, 1), B = A + r.int(2, 3); rate = F((B * B + p * B) - (A * A + p * A), B - A);
        if (c === 7) { var A2 = r.int(-2, 1), B2 = A2 + r.int(1, 3); need(B2 <= 4 && (A2 !== A || B2 !== B)); var rate2 = F((B2 * B2 + p * B2) - (A2 * A2 + p * A2), B2 - A2); need(!rate2.eq(rate));
          var bigger = rate.gt(rate2) ? 'first' : 'second';
          prompt = 'Using the table, which interval has the greater average rate of change: ' + M(num(A) + '\\le x\\le ' + num(B)) + ' (first) or ' + M(num(A2) + '\\le x\\le ' + num(B2)) + ' (second)?';
          chk = { type: 'rate', intervals: [[num(A), num(B)], [num(A2), num(B2)]] };
          steps.push(step('First interval: ' + M('\\frac{f(' + num(B) + ')-f(' + num(A) + ')}{' + num(B) + '-' + num(A) + '}=' + num(rate)) + '.', '', 2), step('Second interval: ' + M(num(rate2)) + '.', '', 2), step('Compare.', '', 1));
          ans = 'The ' + bigger + ' interval (' + M(num(rate)) + ' vs. ' + M(num(rate2)) + ').';
          return { variant: 'roc-compare', prompt: prompt, fig: fig, parts: [{ answer: ans, check: chk }], steps: steps, space: [0.9, 1.1, 1.3] }; }
        prompt = 'Find the average rate of change of ' + M('f') + ' from ' + M('x=' + num(A)) + ' to ' + M('x=' + num(B)) + '.'; chk = { type: 'rate', from: String(A), to: String(B) };
        steps.push(step('Average rate of change = (f(b) − f(a)) ÷ (b − a).', '\\frac{f(' + num(B) + ')-f(' + num(A) + ')}{' + num(B) + '-' + num(A) + '}=' + num(rate), 3)); }
      else { var p6 = nz(r, -4, 4), q6 = nz(r, -6, 6), rule = 'f(x)=' + lin([[1, 'x^2'], [p6, 'x'], [q6, '']]), A6 = r.int(-3, 2), B6 = A6 + r.int(2, 4);
        rate = F((B6 * B6 + p6 * B6) - (A6 * A6 + p6 * A6), B6 - A6);
        prompt = 'Find the average rate of change of ' + M(rule) + ' on the interval ' + M(num(A6) + '\\le x\\le ' + num(B6)) + '.'; chk = { type: 'rate', rule: rule, from: String(A6), to: String(B6), v: 'x' };
        steps.push(step('Evaluate the function at both ends.', 'f(' + num(A6) + ')=' + (A6 * A6 + p6 * A6 + q6) + ',\\ f(' + num(B6) + ')=' + (B6 * B6 + p6 * B6 + q6), 2), step('Divide the change in f by the change in x.', num(rate), 2)); }
      if (!ans) ans = M(num(rate));
      return { variant: 'roc' + c, prompt: prompt, fig: fig, parts: [{ answer: ans, check: chk }], steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= RATE · interpret graphs ================= */
  var STORIES = [['Distance from home (miles)', 'Time (hours)', 'Maya’s distance from home'], ['Water in a tank (gallons)', 'Time (minutes)', 'the water in a tank'], ['Height (m)', 'Time (seconds)', 'a drone’s height']];
  skill({
    id: 'graph-behavior', best: [1, 2], tag: 'RATE', name: 'Interpret increasing, decreasing and constant intervals',
    blurb: 'Where is the graph increasing? (CP2) → increasing, decreasing and constant intervals (CP1) → four or five pieces, a story (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, nseg = c <= 1 ? 2 : c <= 4 ? 3 : c <= 6 ? 4 : 5, x = 0, y = r.int(1, 4), segs = [], kinds = [];
      var pool = r.shuffle(['up', 'down', 'flat', 'up', 'down'].concat(nseg > 4 ? [r.pick(['up', 'down', 'flat'])] : []));
      for (var i = 0; i < nseg; i++) {
        var len = r.int(1, 3), kind = pool[i] || r.pick(['up', 'down', 'flat']), dy = kind === 'flat' ? 0 : (kind === 'up' ? 1 : -1) * r.int(1, 3) * (len > 1 ? r.int(1, 2) : 1);
        var ny = y + dy; need(ny >= 0 && ny <= 9 && (i === 0 || kind !== kinds[i - 1]));
        segs.push({ a: [x, y], b: [x + len, ny], aEnd: i === 0 ? 'closed' : 'none', bEnd: i === nseg - 1 ? 'closed' : 'none' }); kinds.push(kind); x += len; y = ny;
      }
      need(x <= 10 && (c > 2 || kinds.indexOf('up') >= 0) && (c !== 2 || kinds.indexOf('down') >= 0));
      var fig = { kind: 'plane', xmin: 0, xmax: Math.max(8, x + 1), ymin: 0, ymax: 10, points: [], segs: segs, curves: [] };
      function intervals(k) { return segs.filter(function (s, i) { return kinds[i] === k; }).map(function (s) { return M(s.a[0] + '<x<' + s.b[0]); }); }
      var wants = c <= 1 ? ['increasing'] : c === 2 ? ['increasing', 'decreasing'] : ['increasing', 'decreasing', 'constant'];
      var parts = wants.map(function (w, i) {
        var list = intervals({ increasing: 'up', decreasing: 'down', constant: 'flat' }[w]);
        return { label: wants.length > 1 ? 'abc'[i] : '', prompt: wants.length > 1 ? 'Where is the function ' + w + '?' : '', answer: list.length ? list.join(' and ') : 'Never', check: { type: 'graph-behavior', want: w } };
      });
      var story = c >= 5 ? r.pick(STORIES) : null;
      return { variant: 'gb' + nseg, prompt: (story ? 'The graph shows ' + story[2] + ' over time (x is time). ' : '') + (wants.length > 1 ? 'Use the graph. Give intervals of x.' : 'Over which interval(s) of x is the function increasing?'), fig: fig,
        parts: parts, steps: [step('Read the graph from left to right: going up means increasing, going down decreasing, level constant.', '', 3), step('Give each interval by its x-values (endpoints not included).', '', 1)], space: [0.5, 0.7, 0.9] };
    }
  });

  /* ================= SEQUENCE · arithmetic sequences as functions ================= */
  skill({
    id: 'sequence', best: [0, 1, 2], tag: 'SEQUENCE', name: 'Arithmetic sequences as functions',
    blurb: 'Next terms (CP2) → the 10th term, an explicit formula (CP1) → formulas from two terms, which term equals k (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, a1 = r.int(-10, 15), d = c <= 1 ? r.int(2, 9) : nz(r, -8, 9), terms = [a1, a1 + d, a1 + 2 * d, a1 + 3 * d];
      var tt = terms.map(num).join(',\\ ') + ',\\ \\dots', term = function (n) { return a1 + (n - 1) * d; }, parts, steps = [];
      var formula = 'a_n=' + lin([[d, 'n'], [a1 - d, '']]);
      if (c <= 2) { parts = [{ answer: M(num(term(5)) + ',\\ ' + num(term(6))), check: { type: 'sequence', terms: tt, want: 'next' } }];
        steps.push(step('Common difference: subtract consecutive terms.', 'd=' + d, 2), step('Add d twice.', num(term(5)) + ',\\ ' + num(term(6)), 2));
        return { variant: 'seq-next', prompt: 'Find the next two terms of ' + M(tt) + '.', parts: parts, steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 3) { var n3 = r.int(8, 15); steps.push(step('Common difference.', 'd=' + d, 1), step('Use ' + M('a_n=a_1+(n-1)d') + '.', 'a_{' + n3 + '}=' + num(a1) + '+(' + (n3 - 1) + ')(' + num(d) + ')=' + term(n3), 3));
        return { variant: 'seq-nth', prompt: 'Find the ' + n3 + 'th term of ' + M(tt) + '.', parts: [{ answer: M('a_{' + n3 + '}=' + term(n3)), check: { type: 'sequence', terms: tt, want: 'nth', n: n3 } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      if (c === 4) { steps.push(step('Common difference and first term.', 'd=' + d + ',\\ a_1=' + num(a1), 1), step('Substitute into ' + M('a_n=a_1+(n-1)d') + ' and simplify.', formula, 3));
        return { variant: 'seq-formula', prompt: 'Write an explicit formula for ' + M(tt) + '.', parts: [{ answer: M(formula), check: { type: 'sequence', terms: tt, want: 'formula' } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      if (c === 6) { var i1 = r.int(2, 4), i2 = i1 + r.int(3, 6), g1 = 'a_{' + i1 + '}=' + term(i1), g2 = 'a_{' + i2 + '}=' + term(i2);
        steps.push(step('d = change in value ÷ change in position.', 'd=\\frac{' + term(i2) + '-' + (term(i1) < 0 ? '(' + term(i1) + ')' : term(i1)) + '}{' + i2 + '-' + i1 + '}=' + d, 2), step('Work back to the first term, then write the formula.', formula, 2));
        return { variant: 'seq-two', prompt: 'An arithmetic sequence has ' + M(g1) + ' and ' + M(g2) + '. Write an explicit formula.', parts: [{ answer: M(formula), check: { type: 'sequence', given: [{ tex: g1, n: i1, val: String(term(i1)) }, { tex: g2, n: i2, val: String(term(i2)) }], want: 'formula' } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      var nK = r.int(12, 40), val = term(nK);
      if (c === 5) { steps.push(step('Write the formula and set it equal to ' + val + '.', lin([[d, 'n'], [a1 - d, '']]) + '=' + val, 2), step('Solve for n.', 'n=' + nK, 2));
        return { variant: 'seq-which', prompt: 'Which term of ' + M(tt) + ' is ' + M(num(val)) + '?', parts: [{ answer: 'Term ' + M('n=' + nK), check: { type: 'sequence', terms: tt, want: 'which', value: String(val) } }], steps: steps, space: [0.8, 1.0, 1.2] }; }
      var isT = r.chance(0.5), test = isT ? val : val + (Math.abs(d) > 1 ? r.pick([1, -1]) : 0); need(isT || Math.abs(d) > 1);
      var recursive = 'a_1=' + num(a1) + ',\\ a_n=a_{n-1}' + K.addConst('', d);
      parts = [{ label: 'a', prompt: 'Write a recursive formula.', answer: M(recursive), check: null },
               { label: 'b', prompt: 'Write an explicit formula.', answer: M(formula), check: { type: 'sequence', terms: tt, want: 'formula' } },
               { label: 'c', prompt: 'Is ' + M(num(test)) + ' a term of the sequence? Explain.', answer: isT ? 'Yes: it is term ' + M('n=' + nK) + '.' : 'No: solving gives a value of n that is not a whole number.', check: { type: 'sequence', terms: tt, want: 'which', value: String(test), yesno: true } }];
      parts[0].check = { type: 'sequence', terms: tt, want: 'recursive' };
      steps.push(step('(a) Start value and the common difference.', recursive, 2), step('(b) Explicit formula.', formula, 2), step('(c) Set the formula equal to ' + test + ' and solve for n.', '', 2));
      return { variant: 'seq-full', prompt: 'For the arithmetic sequence ' + M(tt), parts: parts, steps: steps, space: [1.2, 1.5, 1.8] };
    }
  });

  /* ================= RATE · describe a curved graph ================= */
  function pt(x, y) { return '(' + num(x) + ',\ ' + num(y) + ')'; }
  function curvePts(f, x1, x2) { var pts = []; for (var x = x1; x <= x2 + 1e-9; x += 0.5) pts.push([x, f(x)]); return pts; }
  skill({
    id: 'curve-behavior', best: [1, 2], tag: 'RATE', name: 'Describe a curved graph',
    blurb: 'Where a parabola rises or falls (CP2) → its maximum or minimum, both intervals (CP1) → a curve with two turning points: every interval, the relative maximum and minimum (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], f, turns, x1, x2;
      if (c <= 4) {
        var h = r.int(-2, 2), k = r.int(-3, 4), a = r.pick([1, -1, 0.5, -0.5]); f = function (x) { return a * (x - h) * (x - h) + k; };
        x1 = h - r.int(2, 3); x2 = h + r.int(2, 3); turns = [[h, k, a < 0 ? 'max' : 'min']];
      } else {
        var m = 1, k3 = r.int(-2, 2), a3 = r.pick([1, -1]), s = r.int(-1, 1); f = function (x) { return a3 * ((x - s) * (x - s) * (x - s) - 3 * (x - s)) + k3; };
        x1 = s - 2; x2 = s + 2; turns = [[s - 1, f(s - 1), a3 > 0 ? 'max' : 'min'], [s + 1, f(s + 1), a3 > 0 ? 'min' : 'max']]; void m;
      }
      var pts = curvePts(f, x1, x2); need(pts.every(function (q) { return Math.abs(q[1]) <= 7 && Math.abs(q[0]) <= 7; }));
      var ys = pts.map(function (q) { return q[1]; }), fig = { kind: 'plane', xmin: Math.min(-1, x1 - 1), xmax: Math.max(1, x2 + 1), ymin: Math.min(-1, Math.floor(Math.min.apply(null, ys)) - 1), ymax: Math.max(1, Math.ceil(Math.max.apply(null, ys)) + 1), points: [{ x: x1, y: f(x1) }, { x: x2, y: f(x2) }], segs: [], curves: [pts] };
      // monotone pieces between the ends and the turning points
      var cuts = [x1].concat(turns.map(function (t) { return t[0]; })).concat([x2]), pieces = [];
      for (var i = 0; i + 1 < cuts.length; i++) pieces.push({ lo: cuts[i], hi: cuts[i + 1], up: f(cuts[i + 1]) > f(cuts[i]) });
      var iv = function (up) { var L = pieces.filter(function (pc) { return pc.up === up; }).map(function (pc) { return M(num(F(pc.lo * 2, 2)) + '<x<' + num(F(pc.hi * 2, 2))); }); return L.length ? L.join(' and ') : 'Never'; };
      var ext = function (t) { return (turns.length > 1 ? 'Relative ' : '') + (t[2] === 'max' ? (turns.length > 1 ? 'maximum' : 'Maximum') : (turns.length > 1 ? 'minimum' : 'Minimum')) + ' value ' + M('y=' + num(F(t[1] * 4, 4))) + ' at ' + M('x=' + t[0]); };
      var parts = [], wants = c === 1 ? ['increasing'] : c === 2 ? ['decreasing'] : c === 3 ? ['extreme'] : c === 4 ? ['increasing', 'decreasing'] : c === 5 ? ['increasing', 'decreasing'] : ['increasing', 'decreasing', 'extreme'];
      wants.forEach(function (w, j) {
        var lab = wants.length > 1 ? 'abc'[j] : '';
        if (w === 'extreme') parts.push({ label: lab, prompt: wants.length > 1 ? (turns.length > 1 ? 'Give the relative maximum and minimum values and where they occur.' : 'Give the maximum or minimum value and where it occurs.') : '', answer: turns.map(ext).join('; '), check: { type: 'curve-behavior', want: 'extreme' } });
        else parts.push({ label: lab, prompt: wants.length > 1 ? 'Where is the function ' + w + '?' : '', answer: iv(w === 'increasing'), check: { type: 'curve-behavior', want: w } });
      });
      steps.push(step('Read the graph from left to right: it rises where it is increasing and falls where it is decreasing.', '', 2));
      steps.push(step('The turning point' + (turns.length > 1 ? 's are' : ' is') + ' at ' + turns.map(function (t) { return M(pt(t[0], F(t[1] * 4, 4))); }).join(' and ') + '.', '', 2));
      var q0 = wants.length > 1 ? 'Use the graph of the function on ' + M(x1 + '\\le x\\le ' + x2) + '.' : wants[0] === 'extreme' ? 'Use the graph of the function on ' + M(x1 + '\\le x\\le ' + x2) + '. Give its maximum or minimum value and where it occurs.' : 'Use the graph of the function on ' + M(x1 + '\\le x\\le ' + x2) + '. Where is the function ' + wants[0] + '?';
      return { variant: 'cb' + c, prompt: q0, fig: fig, parts: parts, steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });


  // Lesson-specific aliases of independently verified generators; these remain selectable skills.
  (function(){var base=skills.find(function(s){return s.id==="sequence";});if(!base)return;
    skill({id:"arithmetic-explicit",best:base.best,tag:base.tag,name:"Write an explicit arithmetic sequence formula",blurb:"Use the first term and common difference to write a_n.",
      difficultyProfile:'focused',fixedDifficulty:4,generate:function(ctx){return base.generate(Object.assign({},ctx,{c:4}));}});
  })();
  (function(){var parent=skills.find(function(s){return s.id==="sequence";});if(parent)skill({id:"arithmetic-nth",best:parent.best,tag:parent.tag,name:"Find a specified arithmetic sequence term",blurb:"Use the common difference to calculate the nth term.",difficultyProfile:'focused',fixedDifficulty:3,generate:function(ctx){return parent.generate(Object.assign({},ctx,{c:3}));}});})();
  /* A discrete/continuous lesson-specific bank with verifiable numeric choice answers. */
  skill({
    id:'discrete-continuous',difficultyProfile:'focused',best:[0,1],tag:'RELATIONS',name:'Discrete versus continuous functions',
    blurb:'Choose whether the input can take every value in an interval or only separate whole-number values.',
    generate:function(ctx){
      var cases=[
        ['A student buys individual notebooks. The input is the number of notebooks purchased.',1],
        ['The height of a plant is measured over elapsed time. The input is elapsed time in hours.',2],
        ['Tickets sold for a school game are counted. The input is the number of tickets.',1],
        ['Water flows into a tank. The input is the number of minutes elapsed.',2],
        ['A classroom counts the number of students present. The input is the number of students.',1],
        ['A cyclist travels along a trail. The input is the distance ridden in miles.',2],
        ['A store charges per individual bag of apples. The input is the number of bags.',1],
        ['A bathtub drains steadily. The input is the volume of water remaining in gallons.',2]
      ];
      var item=ctx.rng.pick(cases),answer=item[1];
      return {variant:'dc'+answer,prompt:item[0]+' Is this input discrete or continuous? Enter 1 for discrete or 2 for continuous.',
        parts:[{answer:String(answer),check:{type:'discrete-continuous',scenario:item[0]}}],
        steps:[step(answer===1?'Individual objects are counted in whole numbers.':'A measured quantity can vary through values between whole numbers.',String(answer),1)],
        space:[0.5,0.7,0.9]};
    }
  });

  NS.registerSkillSet({
    id: 'algebra1-relations-functions', course: 'algebra1', courseName: 'Algebra 1', unit: 'relations-functions', unitName: 'Relations and Functions',
    title: 'The Function Diner',
    tags: { RELATIONS: 'Relations, domain and range', NOTATION: 'Function notation', REPRESENT: 'Tables, rules and graphs', RATE: 'Rate of change and graphs', SEQUENCE: 'Sequences as functions' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Relations and functions</h4><p>A relation pairs inputs (x) with outputs (y).</p><p>A <b>function</b> gives each input exactly one output.</p><p>Vertical line test: if a vertical line hits a graph twice, it is not a function.</p></section>' +
      '<section><h4>Domain and range</h4><p>Domain: all x-values (inputs). Range: all y-values (outputs).</p><p>Points/tables: list values in braces, e.g. ⟨\\{-2,\\ 0,\\ 3\\}⟩.</p><p>Graphs: use inequalities, e.g. ⟨-3\\le x<4⟩. Open circle: not included. Arrow: continues forever.</p></section>' +
      '<section><h4>Function notation</h4><p>⟨f(3)⟩ means “the output when ⟨x=3⟩”. Substitute with parentheses.</p><p>⟨f(x)=7⟩ means “find the input that gives 7”: solve.</p></section>' +
      '<section><h4>Rate of change</h4><p>⟨\\text{rate}=\\frac{\\text{change in }y}{\\text{change in }x}=\\frac{y_2-y_1}{x_2-x_1}⟩</p><p>Average rate of change on ⟨a\\le x\\le b⟩: ⟨\\frac{f(b)-f(a)}{b-a}⟩</p></section>' +
      '<section><h4>Arithmetic sequences</h4><p>Common difference ⟨d⟩. Explicit: ⟨a_n=a_1+(n-1)d⟩</p><p>Recursive: ⟨a_n=a_{n-1}+d⟩ with ⟨a_1⟩ given.</p></section>' +
      '<section><h4>Reading graphs</h4><p>Left to right: up = increasing, down = decreasing, level = constant.</p></section></div>',
    gaps: [],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
