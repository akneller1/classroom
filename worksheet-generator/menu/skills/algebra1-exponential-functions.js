/* Menu Assessment Generator — Algebra 1 · Unit 8 Exponential Functions (roadmap days 104–115).
   Skill groups: EVAL (evaluate exponential functions), GROWTH (growth/decay, initial value, factor,
   rate, key features of the graph), MODEL (linear vs. exponential, writing y = a·b^x), SOLVE (equations
   with a common base), SEQUENCE (geometric sequences), APPLY (growth and decay in context).
   Every answer is re-derived by menu/verify.js from what students see. */
(function (G) {
  'use strict';
  var NS = G.MKMENU, K = NS.kit, Fr = K.Fr, M = K.M, num = K.num, lin = K.lin;
  var need = K.need, F = K.F, nz = K.nz, step = K.step;
  var skills = [];
  function skill(d) { skills.push(d); return d; }
  function plane(win, extra) { return Object.assign({ kind: 'plane', xmin: win[0], xmax: win[1], ymin: win[2], ymax: win[3], points: [], segs: [], curves: [] }, extra || {}); }

  /* bases: {f: Fr value, tex: how it is printed inside the rule, int: whole-number base} */
  function B(n, d) { var f = F(n, d === undefined ? 1 : d); return { f: f, int: f.isInt(), tex: f.isInt() ? String(f.n) : '\\left(\\frac{' + f.n + '}{' + f.d + '}\\right)' }; }
  function Bdec(s) { var parts = s.split('.'), den = Math.pow(10, (parts[1] || '').length); return { f: F(Math.round(parseFloat(s) * den), den), int: false, dec: true, tex: '(' + s + ')' }; }
  function fpow(f, n) { var r = F(1); for (var i = 0; i < Math.abs(n); i++) r = r.mul(f); return n < 0 ? F(1).div(r) : r; }
  /* "a·b^{x}" written the way a textbook does */
  function expTeX(a, b, v, h, k) {
    a = Fr.of(a); var co = a.eq(1) ? '' : a.eq(-1) ? '-' : num(a) + (b.int ? '\\cdot ' : '');
    var ex = h ? lin([[1, v], [-h, '']]) : v;
    var s = co + b.tex + '^{' + ex + '}';
    return k ? K.addConst(s, k) : s;
  }
  function val(a, b, x, h, k) { return Fr.of(a).mul(fpow(b.f, x - (h || 0))).add(k || 0); }
  function decStr(f) { var x = f.n / f.d; return String(Math.round(x * 1e6) / 1e6); }
  function pct(b) { var r = b.f.sub(1).mul(100); return Math.abs(r.n / r.d); }

  /* ================= EVAL · evaluate exponential functions ================= */
  skill({
    id: 'exp-eval', best: [0, 1], tag: 'EVAL', name: 'Evaluate exponential functions',
    blurb: 'f(3) for f(x) = 3·2ˣ (CP2) → x = 0 and negative inputs, fraction bases (CP1) → shifts, decimal bases, combining values (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, a, b, x, h = 0, k = 0, rule, call, v, steps = [];
      if (c <= 2) { b = B(r.int(2, c === 1 ? 4 : 5)); a = r.int(1, 9); x = c === 1 ? r.int(1, 3) : r.int(0, 4); need(Math.pow(b.f.n, x) * a <= 2000); }
      else if (c === 3) { b = B(r.int(2, 5)); x = -r.int(1, b.f.n === 2 ? 3 : 2); a = r.int(1, 6) * Math.pow(b.f.n, -x); need(a <= 400); }
      else if (c === 4) { b = B(1, r.int(2, 3)); x = r.int(-2, 3); a = r.int(1, 3) * Math.pow(b.f.d, Math.max(0, x)); }
      else if (c === 5) { b = B(r.int(2, 3)); h = r.int(1, 3) * r.sign(); k = nz(r, -9, 9); a = r.int(1, 4); x = h + r.int(-1, 3); need(x - h >= 0 || a % Math.pow(b.f.n, h - x) === 0); }
      else if (c === 6) { b = r.pick([Bdec('1.5'), Bdec('0.5'), Bdec('2.5'), Bdec('0.2')]); x = r.int(1, 3); a = r.pick([40, 80, 100, 200, 400, 1000]); }
      if (c <= 6) {
        rule = 'f(x)=' + expTeX(a, b, 'x', h, k); call = 'f(' + num(x) + ')'; v = val(a, b, x, h, k);
        need(ctx.c <= 5 || ctx.intOnly ? v.isInt() : true); need(Math.abs(v.n) < 100000);
        var aT = Fr.of(a).eq(1) ? '' : num(a) + (b.int ? '\\cdot ' : ''), exT = h ? (x < 0 ? '(' + num(x) + ')' : num(x)) + (h > 0 ? '-' + h : '+' + (-h)) : (x < 0 ? '(' + num(x) + ')' : num(x));
        steps.push(step('Replace x with ' + M(num(x)) + '.', K.addConst(aT + b.tex + '^{' + exT + '}', k), 1));
        if (x - h < 0) steps.push(step('A negative exponent means a reciprocal: ' + M(num(b.f) + '^{' + (x - h) + '}=\\frac{1}{' + num(fpow(b.f, h - x)) + '}') + '.', '', 1));
        steps.push(step('Evaluate the power first, then multiply' + (k ? ' and add.' : '.'), call + '=' + num(v), 2));
        var vTeX = b.dec && !v.isInt() ? decStr(v) : num(v);
        return { variant: 'ee' + c, prompt: 'For ' + M(rule) + ', find ' + M(call) + '.', parts: [{ answer: M(call + '=' + vTeX), check: { type: 'func-eval', rule: rule, expr: call } }], steps: steps, space: [0.6, 0.8, 1.0] };
      }
      // c7: combine two functions
      var bb = B(r.int(2, 3)), aa = r.int(1, 4), g = 'g(x)=' + K.axb(r.int(2, 6) * r.sign(), nz(r, -9, 9)), f = 'f(x)=' + expTeX(aa, bb, 'x');
      var u = r.int(2, 4), w = r.int(-2, 2), expr = 'f(' + u + ')-g(' + num(w) + ')';
      var gf = /g\(x\)=(.*)/.exec(g)[1], gm = NS.check.evalNode(NS.check.parseExpr(gf), { x: new NS.check.Q(w) }), gv = F(Number(gm.n), Number(gm.d));
      var res = val(aa, bb, u).sub(gv);
      steps.push(step('Evaluate each function: ' + M('f(' + u + ')=' + num(val(aa, bb, u))) + ' and ' + M('g(' + num(w) + ')=' + num(gv)) + '.', '', 2), step('Subtract.', num(res), 2));
      return { variant: 'ee7', prompt: 'For ' + M(f) + ' and ' + M(g) + ', find ' + M(expr) + '.', parts: [{ answer: M(expr + '=' + num(res)), check: { type: 'func-combo', rules: [f, g], expr: expr } }], steps: steps, space: [0.8, 1.0, 1.2] };
    }
  });

  /* ================= GROWTH · growth or decay, initial value, factor, rate ================= */
  skill({
    id: 'exp-identify', best: [0, 1], tag: 'GROWTH', name: 'Identify growth or decay, initial value and rate',
    blurb: 'y = 5·2ˣ: growth or decay, initial value (CP2) → decay factors, percent rates from 1.05 and 0.85 (CP1) → rates in context, fraction bases above 1 (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, a = r.pick([2, 3, 4, 5, 6, 8, 10, 12, 20, 25, 50, 100, 250, 500]), b, v = 'x', fn = 'y', steps = [], parts = [], prompt;
      if (c === 1) b = B(r.int(2, 5));
      else if (c === 2) b = r.chance(0.5) ? B(1, r.int(2, 4)) : B(r.int(2, 6));
      else if (c === 3) b = Bdec('1.0' + r.int(2, 9));
      else if (c === 4) b = Bdec(r.pick(['0.9', '0.85', '0.8', '0.75', '0.95', '0.7']));
      else if (c === 5) b = Bdec(r.pick(['1.12', '1.15', '1.2', '1.25', '0.88', '0.92', '0.6']));
      else if (c === 6) b = r.pick([B(3, 2), B(5, 4), B(3, 4), B(4, 5), B(5, 2)]);
      else b = Bdec(r.pick(['1.035', '1.045', '0.965', '0.975', '1.125', '0.875']));
      if (c >= 5) { var ctxs = b.f.gt(1) ? [['P', 't', 'the population of a town', 'years'], ['A', 't', 'the amount in a savings account, in dollars,', 'years'], ['N', 't', 'the number of fish in a lake', 'months']] : [['V', 't', 'the value of a car, in dollars,', 'years'], ['N', 't', 'the number of fish in a lake', 'months'], ['P', 't', 'the population of a town', 'years']]; var cx = r.pick(ctxs); fn = cx[0]; v = cx[1]; a = r.pick([800, 1200, 2500, 4000, 15000, 30000]);
        prompt = 'The function ' + M(fn + '(' + v + ')=' + expTeX(a, b, v)) + ' models ' + cx[2] + ' after ' + M(v) + ' ' + cx[3] + '.'; }
      var rule = (c >= 5 ? fn + '(' + v + ')' : 'y') + '=' + expTeX(a, b, v), growth = b.f.gt(1), kind = growth ? 'growth' : 'decay';
      if (!prompt) prompt = 'For ' + M(rule) + ':';
      var why = ', because the base ' + M(b.dec ? b.tex.slice(1, -1) : num(b.f)) + (growth ? ' is greater than one.' : ' is between zero and one.');
      parts.push({ label: 'a', prompt: 'Is this exponential growth or decay?', answer: (growth ? 'Growth' : 'Decay') + why, check: { type: 'exp-identify', rule: rule, v: v, want: 'kind' } });
      parts.push({ label: 'b', prompt: 'What is the initial value?', answer: 'Initial value: ' + M(num(a)), check: { type: 'exp-identify', rule: rule, v: v, want: 'initial' } });
      if (c === 2 || c >= 6) parts.push({ label: 'c', prompt: 'What is the ' + kind + ' factor?', answer: kind.charAt(0).toUpperCase() + kind.slice(1) + ' factor: ' + M(b.dec ? decStr(b.f) : num(b.f)), check: { type: 'exp-identify', rule: rule, v: v, want: 'factor' } });
      if (c >= 3) parts.push({ label: String.fromCharCode(97 + parts.length), prompt: 'What is the percent rate of ' + (c >= 5 ? 'change? Say whether it is growth or decay.' : kind + '?'), answer: pct(b) + '% ' + kind + (c >= 5 ? ' per ' + (fn === 'N' ? 'month' : 'year') : ''), check: { type: 'exp-identify', rule: rule, v: v, want: 'rate' } });
      var v2 = F(a).mul(fpow(b.f, 2)); if (c === 7 && (!ctx.intOnly || v2.isInt())) { parts.push({ label: 'e', prompt: 'Find ' + M(fn + '(2)') + '.', answer: M(fn + '(2)=' + decStr(v2)), check: { type: 'func-eval', rule: rule, expr: fn + '(2)' } }); }
      steps.push(step('Compare with ' + M('y=a\\cdot b^{x}') + ': ' + M('a=' + num(a)) + ' and ' + M('b=' + (b.dec ? b.tex.slice(1, -1) : num(b.f))) + '.', '', 1),
        step('b > 1 means growth; 0 < b < 1 means decay. The initial value is a (the value at ' + M(v + '=0') + ').', '', 2));
      if (c >= 3) steps.push(step('Rate: ' + (growth ? M('b=1+r') : M('b=1-r')) + ', so ' + M('r=' + decStr(growth ? b.f.sub(1) : F(1).sub(b.f))) + ' = ' + pct(b) + '%.', '', 2));
      return { variant: 'ei' + c, prompt: prompt, parts: parts, steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= GROWTH · key features of the graph ================= */
  function curve(a, b, k, win) {
    var pts = [];
    for (var x = win[0]; x <= win[1] + 1e-9; x += 0.25) { var y = (a * Math.pow(b.f.n / b.f.d, x)) + k; if (y > win[3] + 0.5 || y < win[2] - 0.5) { if (pts.length) break; continue; } pts.push([Math.round(x * 1000) / 1000, Math.round(y * 1000) / 1000]); }
    return pts;
  }
  skill({
    id: 'exp-graph', best: [0, 1, 2], tag: 'GROWTH', name: 'Key features of exponential graphs',
    blurb: 'y-intercept, asymptote, increasing or decreasing from a graph and its rule (CP2) → domain and range, vertical shifts (CP1) → reflections, all features at once (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, b = r.chance(c <= 2 ? 0.6 : 0.5) ? B(r.int(2, 4)) : B(1, r.int(2, 4)), a = r.int(1, 5), k = 0, parts = [], steps = [];
      if (c >= 4) k = nz(r, -4, 4);
      if (c >= 6) a = -a;
      var rule = 'f(x)=' + expTeX(a, b, 'x', 0, k), win = [-5, 5, -8, 8], fig = null;
      { var pts = curve(a, b, k, win); need(pts.length > 6); fig = plane(win, { curves: [pts], points: [{ x: 0, y: a + k }] }); }
      var y0 = a + k, wantList = c === 1 ? ['intercept', 'behavior'] : c === 2 ? ['intercept', 'asymptote', 'behavior'] : c === 3 ? ['domain', 'range', 'behavior'] : c === 4 ? ['intercept', 'asymptote', 'range'] : c === 5 ? ['asymptote', 'range', 'behavior'] : c === 6 ? ['intercept', 'range', 'behavior'] : ['intercept', 'asymptote', 'domain', 'range', 'behavior'];
      var growth = b.f.gt(1), inc = (a > 0) === growth;
      var Q = { intercept: ['What is the y-intercept?', M('(0,\\ ' + num(y0) + ')')], asymptote: ['What is the equation of the horizontal asymptote?', M('y=' + num(k))], domain: ['What is the domain?', 'All real numbers'],
        range: ['What is the range?', M('y' + (a > 0 ? '>' : '<') + num(k))], behavior: ['Is the function increasing or decreasing?', inc ? 'Increasing' : 'Decreasing'] };
      wantList.forEach(function (w, i) { parts.push({ label: 'abcde'[i], prompt: Q[w][0], answer: Q[w][1], check: { type: 'exp-features', rule: rule, v: 'x', want: w } }); });
      steps.push(step('y-intercept: substitute x = 0, so ' + M('f(0)=' + num(a) + K.addConst('', k) + '=' + num(y0)) + '.', '', 1),
        step('The graph levels off toward ' + M('y=' + num(k)) + ' (the added constant), which is never reached.', '', 1),
        step('Range: ' + (a > 0 ? 'above' : 'below') + ' the asymptote. Domain: all real numbers.', '', 1),
        step((growth ? 'Base > 1' : 'Base between 0 and 1') + (a < 0 ? ', flipped by the negative a' : '') + ': the graph is ' + (inc ? 'increasing.' : 'decreasing.'), '', 1));
      return { variant: 'eg' + c, prompt: (fig ? 'The graph shows ' : 'Consider ') + M(rule) + (fig ? '.' : '.'), fig: fig, parts: parts, steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= MODEL · linear, exponential, or neither ================= */
  skill({
    id: 'lin-vs-exp', best: [0, 1], tag: 'MODEL', name: 'Linear, exponential, or neither?',
    blurb: 'Common difference or common ratio in a table (CP2) → decreasing tables and decay (CP1) → x-steps of 2, fraction ratios, “neither” (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, step0 = c >= 6 ? 2 : 1, x0 = c >= 4 ? r.int(-1, 2) : 0, xs = [0, 1, 2, 3, 4].slice(0, c >= 3 ? 5 : 4).map(function (i) { return x0 + i * step0; });
      var kind = r.pick(c >= 5 ? ['linear', 'exponential', 'neither'] : ['linear', 'exponential']), ys, extra, steps = [];
      if (kind === 'linear') { var m = c <= 2 ? r.int(2, 9) : nz(r, -9, 9), b0 = r.int(-10, 20); ys = xs.map(function (x, i) { return F(b0 + m * i * step0); }); extra = 'Linear: the y-values change by ' + M(num(ys[1].sub(ys[0]))) + ' each time.'; }
      else if (kind === 'exponential') { var bs = c <= 2 ? B(r.int(2, 4)) : c <= 4 ? B(1, r.int(2, 3)) : r.pick([B(3), B(1, 2), B(3, 2), B(2, 3)]); var a0 = r.int(1, 5) * Math.pow(bs.f.d, xs.length); if (c <= 2 && r.chance(0.5)) bs = B(r.int(2, 3));
        ys = xs.map(function (x, i) { return F(a0).mul(fpow(bs.f, i)); }); extra = 'Exponential: each y-value is ' + M(num(ys[1].div(ys[0]))) + ' times the one before.'; }
      else { var p2 = r.int(1, 3), q2 = r.int(-5, 5); ys = xs.map(function (x) { return F(p2 * x * x + q2); }); need(ys.every(function (y) { return !y.isZero(); })); extra = 'Neither: the y-values do not change by a constant difference or a constant factor.'; }
      ys.forEach(function (y) { need(y.isInt() && Math.abs(y.n) < 2000); });
      var fig = { kind: 'table', head: ['x', 'y'], rows: xs.map(function (x, i) { return [x, ys[i].n]; }) };
      steps.push(step('Subtract consecutive y-values: are the differences equal?', '', 1), step('Divide consecutive y-values: are the ratios equal?', '', 1), step('Equal differences: linear. Equal ratios: exponential. Neither: neither.', '', 2));
      return { variant: 'lve-' + kind, prompt: 'Is the relationship in the table linear, exponential, or neither? Explain.', fig: fig, parts: [{ answer: extra, check: { type: 'exp-model' } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= MODEL · write y = a·bˣ ================= */
  skill({
    id: 'exp-write', best: [0, 1, 2], tag: 'MODEL', name: 'Write an exponential function',
    blurb: 'From a table that starts at x = 0 (CP2) → decay tables, tables that start at x = 1 (CP1) → two points or a graph, fraction factors (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, b, a, steps = [], fig = null, pairs = null, prompt;
      b = c === 7 ? r.pick([B(1, 2), B(3, 2), B(1, 3), B(2, 3), B(4, 3)]) : c <= 3 ? B(r.int(2, 5)) : c === 4 ? r.pick([B(1, 2), B(1, 3), B(1, 4), B(1, 5), B(2, 3), B(3, 4)]) : c === 5 ? r.pick([B(1, 2), B(1, 3), B(2, 3), B(3, 4), B(3, 2)]) : c <= 5 ? r.pick([B(2), B(3), B(1, 2), B(4)]) : r.pick([B(2), B(3), B(1, 2), B(3, 2), B(1, 3)]);
      var maxX = c <= 2 ? 3 : c === 3 ? 4 : c === 4 ? 3 : c === 5 ? 5 : 6;
      a = r.int(1, 9) * Math.pow(b.f.d, maxX);
      need(a <= (c === 5 ? 2500 : 800));
      var rule = 'y=' + expTeX(a, b, 'x'), parts;
      if (c <= 5) {
        var xs = c === 3 ? [1, 2, 3, 4] : c === 5 ? [2, 3, 4, 5] : [0, 1, 2, 3];
        fig = { kind: 'table', head: ['x', 'y'], rows: xs.map(function (x) { var y = val(a, b, x); need(y.isInt() && y.n <= 5000); return [x, y.n]; }) };
        prompt = 'Write an exponential function ' + M('y=a\\cdot b^{x}') + ' for the table.';
        steps.push(step('Divide consecutive y-values to find the factor.', 'b=' + num(b.f), 2), step(c === 3 || c === 5 ? 'Work back to x = 0: divide by b once for each step back.' : 'The y-value at x = 0 is a.', 'a=' + num(a), 1), step('Write the function.', rule, 1));
        parts = [{ answer: M(rule), check: { type: 'exp-rule', v: 'x' } }];
      } else {
        var x1 = r.int(0, 2), gap = c === 7 ? 3 : 2, x2 = x1 + gap, y1 = val(a, b, x1), y2 = val(a, b, x2), xp = x2 + r.int(1, 2), yp = val(a, b, xp);
        need(y1.isInt() && y2.isInt() && y1.n <= 2000 && y2.n <= 2000 && y1.n > 0 && y2.n > 0 && (yp.isInt() || !ctx.intOnly));
        pairs = '(' + x1 + ',\\ ' + y1.n + '),\\ (' + x2 + ',\\ ' + y2.n + ')';
        prompt = 'An exponential function ' + M('y=a\\cdot b^{x}') + ' passes through ' + M(pairs) + '.';
        steps.push(step('Divide the y-values: ' + M('b^{' + gap + '}=\\frac{' + y2.n + '}{' + y1.n + '}=' + num(y2.div(y1))) + ', so ' + M('b=' + num(b.f)) + '.', '', 2), step('Use one point to find a: ' + M(y1.n + '=a\\cdot ' + num(b.f) + '^{' + x1 + '}') + '.', 'a=' + num(a), 1), step('Write the function.', rule, 1), step('(b) Substitute x = ' + xp + '.', 'y=' + num(yp), 1));
        parts = [{ label: 'a', prompt: 'Write the function.', answer: M(rule), check: { type: 'exp-rule', pairs: pairs, v: 'x' } },
                 { label: 'b', prompt: 'Use it to find ' + M('y') + ' when ' + M('x=' + xp) + '.', answer: M('y=' + num(yp)), check: { type: 'exp-rule', pairs: pairs, v: 'x', predict: String(xp) } }];
      }
      return { variant: 'ew' + c, prompt: prompt, fig: fig, parts: parts, steps: steps, space: [0.7, 0.9, 1.1] };
    }
  });

  /* ================= SOLVE · exponential equations with a common base ================= */
  skill({
    id: 'exp-solve', best: [0, 1, 2], tag: 'SOLVE', name: 'Solve exponential equations (common base)',
    blurb: '2ˣ = 32 (CP2) → 3·2ˣ = 48, 3ˣ⁻¹ = 27, same base on both sides (CP1) → rewrite with a common base, fraction answers (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], eq, x, base = r.pick([2, 3, 5]), lhs, rhs;
      function pw(bs, e) { return bs + '^{' + e + '}'; }
      if (c === 1) { base = r.pick([2, 3, 4, 5, 6, 7, 10]); x = r.int(2, { 2: 9, 3: 6, 4: 5, 5: 4, 6: 3, 7: 3, 10: 5 }[base]); eq = pw(base, 'x') + '=' + Math.pow(base, x); steps.push(step('Write ' + Math.pow(base, x) + ' as a power of ' + base + '.', pw(base, 'x') + '=' + pw(base, x), 2)); }
      else if (c === 2) { x = r.int(1, 4); var co = r.int(2, 5); eq = co + '\\cdot ' + pw(base, 'x') + '=' + co * Math.pow(base, x); need(co * Math.pow(base, x) < 2000); steps.push(step('Divide both sides by ' + co + '.', pw(base, 'x') + '=' + Math.pow(base, x), 1), step('Write both sides with the same base.', pw(base, 'x') + '=' + pw(base, x), 1)); }
      else if (c === 3) { var hh = nz(r, -3, 3), e = r.int(1, base === 2 ? 6 : 4); x = e - hh; eq = pw(base, lin([[1, 'x'], [hh, '']])) + '=' + Math.pow(base, e); steps.push(step('Write the right side as a power of ' + base + '.', pw(base, lin([[1, 'x'], [hh, '']])) + '=' + pw(base, e), 1), step('Set the exponents equal.', lin([[1, 'x'], [hh, '']]) + '=' + e, 1)); }
      else if (c === 4) { var m1 = r.int(2, 4), m2 = 1; x = r.int(1, 5); var h2 = (m1 - m2) * x; eq = pw(base, m1 + 'x') + '=' + pw(base, lin([[1, 'x'], [h2, '']])); steps.push(step('The bases are equal, so the exponents are equal.', m1 + 'x=' + lin([[1, 'x'], [h2, '']]), 2)); }
      else if (c === 5) { var pr = r.pick([[4, 2, 2], [9, 3, 2], [8, 2, 3], [25, 5, 2], [27, 3, 3]]); x = r.int(1, 4) * r.sign(); var hh5 = (pr[2] - 1) * x; need(hh5 !== 0);
        eq = pw(pr[0], 'x') + '=' + pw(pr[1], lin([[1, 'x'], [hh5, '']])); steps.push(step('Rewrite ' + pr[0] + ' as ' + M(pr[1] + '^{' + pr[2] + '}') + '.', pw(pr[1], pr[2] + 'x') + '=' + pw(pr[1], lin([[1, 'x'], [hh5, '']])), 2), step('Set the exponents equal and solve.', '', 1)); }
      else if (c === 6) { if (ctx.intOnly || r.chance(0.5)) { var bs6 = r.pick([2, 3, 4, 5]), e6 = r.int(1, bs6 === 2 ? 5 : 3), h6 = nz(r, -3, 3); x = -e6 - h6; eq = '\\left(\\frac{1}{' + bs6 + '}\\right)^{' + (h6 ? lin([[1, 'x'], [h6, '']]) : 'x') + '}=' + Math.pow(bs6, e6); steps.push(step('Write ' + M('\\frac{1}{' + bs6 + '}') + ' as ' + M(bs6 + '^{-1}') + ' and ' + Math.pow(bs6, e6) + ' as ' + M(bs6 + '^{' + e6 + '}') + '.', bs6 + '^{' + (h6 ? '-(' + lin([[1, 'x'], [h6, '']]) + ')' : '-x') + '}=' + bs6 + '^{' + e6 + '}', 2)); }
        else { var pr6 = r.pick([[4, 8, 2, 2, 3], [9, 27, 3, 2, 3], [25, 125, 5, 2, 3], [8, 4, 2, 3, 2], [27, 9, 3, 3, 2], [8, 16, 2, 3, 4], [16, 8, 2, 4, 3], [4, 32, 2, 2, 5], [9, 243, 3, 2, 5], [8, 32, 2, 3, 5], [27, 81, 3, 3, 4], [32, 8, 2, 5, 3]]); var h6b = nz(r, -2, 2); x = F(pr6[4], pr6[3]).sub(h6b); var ex6 = lin([[1, 'x'], [h6b, '']]); eq = pw(pr6[0], ex6) + '=' + pr6[1]; steps.push(step('Write both sides as powers of ' + pr6[2] + '.', pw(pr6[2], pr6[3] + '(' + ex6 + ')') + '=' + pw(pr6[2], pr6[4]), 2), step('Set the exponents equal: ' + M(pr6[3] + '(' + ex6 + ')=' + pr6[4]) + '.', '', 1)); } }
      else { var pr7 = r.pick([[8, 4, 2, 3, 2], [4, 8, 2, 2, 3], [9, 27, 3, 2, 3], [27, 9, 3, 3, 2]]), p1 = nz(r, -3, 3), p2 = nz(r, -3, 3);
        // pr7[0]^{x+p1} = pr7[1]^{x+p2}  →  e0(x+p1) = e1(x+p2)
        var e0 = pr7[3], e1 = pr7[4]; need(e0 !== e1); x = F(e1 * p2 - e0 * p1, e0 - e1);
        eq = pw(pr7[0], lin([[1, 'x'], [p1, '']])) + '=' + pw(pr7[1], lin([[1, 'x'], [p2, '']]));
        steps.push(step('Write both bases as powers of ' + pr7[2] + '.', pw(pr7[2], e0 + '(' + lin([[1, 'x'], [p1, '']]) + ')') + '=' + pw(pr7[2], e1 + '(' + lin([[1, 'x'], [p2, '']]) + ')'), 2), step('Set the exponents equal, distribute and solve.', '', 1)); }
      x = Fr.of(x); if (ctx.intOnly) need(x.isInt());
      steps.push(step('Solve.', 'x=' + num(x), 1));
      return { variant: 'es' + c, prompt: 'Solve ' + M(eq) + '.', parts: [{ answer: M('x=' + num(x)), check: { type: 'exp-solve', eq: eq, v: 'x' } }], steps: steps, space: [0.6, 0.8, 1.0] };
    }
  });

  /* ================= SEQUENCE · geometric sequences ================= */
  skill({
    id: 'geo-seq', best: [0, 1, 2], tag: 'SEQUENCE', name: 'Geometric sequences',
    blurb: 'Next terms (CP2) → negative and fraction ratios, the nth term, an explicit formula (CP1) → which term is k, formulas from two terms, recursive and explicit (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, rt = c <= 1 ? F(r.int(2, 5)) : c === 2 ? r.pick([F(-2), F(1, 2), F(-3), F(3), F(1, 3), F(4)]) : c <= 5 ? r.pick([F(2), F(3), F(-2), F(4), F(-3), F(5)]) : r.pick([F(2), F(3), F(-2), F(1, 2), F(-3)]);
      var a1 = F(r.int(1, 9) * (rt.d === 1 ? 1 : Math.pow(rt.d, 6))), term = function (n) { return a1.mul(fpow(rt, n - 1)); };
      need(Math.abs(a1.n) <= 800);
      var terms = [1, 2, 3, 4].map(term), tt = terms.map(num).join(',\\ ') + ',\\ \\dots', steps = [];
      var formula = 'a_n=' + (a1.eq(1) ? '' : num(a1) + '\\cdot ') + (rt.isInt() && rt.n > 0 ? String(rt.n) : '\\left(' + num(rt) + '\\right)') + '^{n-1}';
      steps.push(step('Common ratio: divide a term by the one before it.', 'r=' + num(rt), 1));
      if (c <= 2) { steps.push(step('Multiply by r to get each next term.', num(term(5)) + ',\\ ' + num(term(6)), 2));
        return { variant: 'gs-next', prompt: 'Find the next two terms of the geometric sequence ' + M(tt) + '.', parts: [{ answer: M(num(term(5)) + ',\\ ' + num(term(6))), check: { type: 'sequence', terms: tt, want: 'next' } }], steps: steps, space: [0.5, 0.7, 0.9] }; }
      if (c === 3) { var n3 = r.int(6, 8); need(Math.abs(term(n3).n) < 100000); steps.push(step('Use ' + M('a_n=a_1\\cdot r^{n-1}') + '.', 'a_{' + n3 + '}=' + num(a1) + '\\cdot ' + (rt.n < 0 ? '(' + num(rt) + ')' : num(rt)) + '^{' + (n3 - 1) + '}=' + num(term(n3)), 3));
        return { variant: 'gs-nth', prompt: 'Find the ' + n3 + 'th term of the geometric sequence ' + M(tt) + '.', parts: [{ answer: M('a_{' + n3 + '}=' + num(term(n3))), check: { type: 'sequence', terms: tt, want: 'nth', n: n3 } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 4) { steps.push(step('Substitute ' + M('a_1') + ' and r into ' + M('a_n=a_1\\cdot r^{n-1}') + '.', formula, 3));
        return { variant: 'gs-formula', prompt: 'Write an explicit formula for the geometric sequence ' + M(tt) + '.', parts: [{ answer: M(formula), check: { type: 'sequence', terms: tt, want: 'formula' } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 5) { var nk = r.int(6, 9), vk = term(nk); need(Math.abs(vk.n) < 100000); steps.push(step('Keep multiplying by r (or solve ' + M(num(a1) + '\\cdot ' + (rt.isInt() && rt.n > 0 ? num(rt) : '\\left(' + num(rt) + '\\right)') + '^{n-1}=' + num(vk)) + ').', 'n=' + nk, 3));
        return { variant: 'gs-which', prompt: 'Which term of the geometric sequence ' + M(tt) + ' is ' + M(num(vk)) + '?', parts: [{ answer: 'Term ' + M('n=' + nk), check: { type: 'sequence', terms: tt, want: 'which', value: num(vk).replace(/\\frac\{(\d+)\}\{(\d+)\}/, '$1/$2') } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 6) { var i1 = r.int(1, 3), i2 = i1 + r.pick([1, 3]), g1 = 'a_{' + i1 + '}=' + num(term(i1)), g2 = 'a_{' + i2 + '}=' + num(term(i2)); need(term(i1).isInt() && term(i2).isInt() && Math.abs(term(i2).n) < 5000);
        steps.push(step('Divide: ' + M('r^{' + (i2 - i1) + '}=\\frac{' + num(term(i2)) + '}{' + num(term(i1)) + '}') + ', so ' + M('r=' + num(rt)) + '.', '', 2), step('Work back to ' + M('a_1') + ' and write the formula.', formula, 2));
        return { variant: 'gs-two', prompt: 'A geometric sequence has ' + M(g1) + ' and ' + M(g2) + '. Write an explicit formula.', parts: [{ answer: M(formula), check: { type: 'sequence', given: [{ tex: g1, n: i1, val: String(term(i1).n) }, { tex: g2, n: i2, val: String(term(i2).n) }], want: 'formula' } }], steps: steps, space: [0.7, 0.9, 1.1] }; }
      var isT = r.chance(0.5), nk7 = r.int(6, 9), test = isT ? term(nk7) : term(nk7).add(rt.isInt() ? 1 : 0); need(isT || rt.isInt()); need(test.isInt() && Math.abs(test.n) < 100000);
      var recursive = 'a_1=' + num(a1) + ',\\ a_n=' + num(rt) + 'a_{n-1}';
      steps.push(step('(a) Start value and “multiply by r”.', recursive, 2), step('(b) Explicit formula.', formula, 2), step('(c) Keep multiplying by r and compare with ' + num(test) + '.', '', 2));
      return { variant: 'gs-full', prompt: 'For the geometric sequence ' + M(tt),
        parts: [{ label: 'a', prompt: 'Write a recursive formula.', answer: M(recursive), check: { type: 'sequence', terms: tt, want: 'recursive' } },
                { label: 'b', prompt: 'Write an explicit formula.', answer: M(formula), check: { type: 'sequence', terms: tt, want: 'formula' } },
                { label: 'c', prompt: 'Is ' + M(num(test)) + ' a term of the sequence? Explain.', answer: isT ? 'Yes: it is term ' + M('n=' + nk7) + '.' : 'No: it is skipped between two terms of the sequence.', check: { type: 'sequence', terms: tt, want: 'which', value: String(test.n), yesno: true } }],
        steps: steps, space: [1.1, 1.4, 1.7] };
    }
  });

  /* ================= APPLY · growth and decay in context ================= */
  var THINGS = [['bacteria', 'A colony starts with {a} bacteria and doubles every {p}.', 'How many bacteria are there after {t}?', 'doubles'],
    ['followers', 'A new video channel has {a} followers, and the number triples every {p}.', 'How many followers will it have after {t}?', 'triples'],
    ['medicine', 'A patient takes {a} mg of a medicine. The amount in the body halves every {p}.', 'How many milligrams are left after {t}?', 'halves']];
  function per(n, unit) { return n === 1 ? unit : n + ' ' + unit + 's'; }
  skill({
    id: 'exp-apply', best: [0, 1, 2], tag: 'APPLY', name: 'Exponential growth and decay in context',
    blurb: 'Doubling and halving (CP2) → write P(t) = a(1 ± r)ᵗ, interest and depreciation (CP1) → rounding, doubling periods, when a value passes a target (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, steps = [], prompt, parts;
      if (c <= 2 || c === 6) {
        var th = c === 1 ? THINGS[0] : c === 2 ? r.pick([THINGS[1], THINGS[2]]) : r.pick(THINGS), f = th[3] === 'doubles' ? 2 : th[3] === 'triples' ? 3 : 0.5;
        var unit = r.pick(['hour', 'day', 'week']), pN = c === 6 ? r.int(2, 4) : 1, n = r.int(2, f === 3 ? 4 : 5), t = n * pN, a = f === 0.5 ? r.int(1, 9) * Math.pow(2, n) * 5 : r.pick([5, 10, 20, 25, 40, 50, 100]);
        var v = a * Math.pow(f, n); need(Number.isInteger(v) && v < 1e6);
        var fTeX = f === 0.5 ? '\\left(\\frac{1}{2}\\right)' : String(f), what = th[0] === 'medicine' ? 'mg' : th[0];
        steps.push(step('Number of ' + (f === 0.5 ? 'halvings' : f === 2 ? 'doublings' : 'triplings') + ': ' + (pN > 1 ? t + ' ÷ ' + pN + ' = ' : '') + n + '.', '', 1), step('Multiply the start by ' + (f === 0.5 ? M('\\frac{1}{2}') : f) + ' that many times.', a + '\\cdot ' + fTeX + '^{' + n + '}=' + v, 3));
        if (c <= 2) {
          prompt = th[1].replace('{a}', a).replace('{p}', unit) + ' ' + th[2].replace('{t}', per(t, unit));
          return { variant: 'ea' + c, prompt: prompt, parts: [{ answer: M(String(v)) + ' ' + what, check: { type: 'exp-apply', want: 'value', start: 0, time: 1 } }], steps: steps, space: [0.6, 0.8, 1.0] };
        }
        var rule6 = 'y=' + a + (f === 0.5 ? '' : '\\cdot ') + fTeX + '^{\\frac{t}{' + pN + '}}';
        steps.unshift(step('(a) The quantity is multiplied by ' + (f === 0.5 ? M('\\frac{1}{2}') : f) + ' once every ' + pN + ' ' + unit + 's, so the exponent is ' + M('\\frac{t}{' + pN + '}') + '.', rule6, 2));
        return { variant: 'ea6', prompt: th[1].replace('{a}', a).replace('{p}', per(pN, unit)),
          parts: [{ label: 'a', prompt: 'Write a function ' + M('y') + ' for the amount after ' + M('t') + ' ' + unit + 's.', answer: M(rule6), check: { type: 'exp-apply', want: 'rule', start: 0, every: 1, v: 't' } },
                  { label: 'b', prompt: th[2].replace('{t}', per(t, unit)), answer: M(String(v)) + ' ' + what, check: { type: 'exp-apply', want: 'value', start: 0, every: 1, time: 2 } }],
          steps: steps, space: [0.9, 1.1, 1.3] };
      }
      var up = r.chance(0.5), rate = r.pick(up ? [2, 3, 4, 5, 6, 8, 10] : [5, 10, 15, 20, 25]);
      var cx = up ? r.pick([['A town has a population of {a}. The population grows {r}% per year.', 'P', 'the population', [1200, 2000, 5000, 8000, 10000]], ['Maya deposits ${a} in an account that earns {r}% interest each year.', 'A', 'the amount in the account', [500, 1000, 2000, 4000]]])
        : r.pick([['A car is bought for ${a}. Its value decreases {r}% each year.', 'V', 'the value of the car', [10000, 20000, 25000, 30000]], ['A lake has {a} fish. The number of fish declines {r}% per year.', 'N', 'the number of fish', [800, 1000, 2000, 5000]]]);
      var a0 = r.pick(cx[3]), factor = up ? 1 + rate / 100 : 1 - rate / 100, fStr = String(Math.round(factor * 1000) / 1000), base = Bdec(fStr), intro = cx[0].replace('{a}', a0.toLocaleString('en-US')).replace('{r}', rate);
      var rule = cx[1] + '(t)=' + a0 + base.tex + '^{t}', ruleStep = step('Initial value ' + M('a=' + a0) + '; factor ' + M('b=1' + (up ? '+' : '-') + decStr(F(rate, 100)) + '=' + fStr) + '.', rule, 2);
      var writePart = { label: 'a', prompt: 'Write a function for ' + cx[2] + ' after ' + M('t') + ' years.', answer: M(rule), check: { type: 'exp-apply', want: 'rule', start: 0, pct: 1, v: 't' } };
      var t4 = r.int(2, c === 3 ? 3 : 5), exact = F(a0).mul(fpow(base.f, t4));
      if (c === 3) { need(exact.isInt() || exact.mul(100).isInt());
        steps.push(step('Each year multiply by ' + M(fStr) + '.', rule, 1), step('Substitute t = ' + t4 + '.', cx[1] + '(' + t4 + ')=' + a0 + base.tex + '^{' + t4 + '}=' + decStr(exact), 3));
        return { variant: 'ea3', prompt: intro + ' Find ' + cx[2] + ' after ' + t4 + ' years.', parts: [{ answer: M(decStr(exact)), check: { type: 'exp-apply', want: 'value', start: 0, pct: 1, time: 2 } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 4) { steps.push(ruleStep);
        return { variant: 'ea4', prompt: intro + ' Write a function for ' + cx[2] + ' after ' + M('t') + ' years.', parts: [{ answer: M(rule), check: { type: 'exp-apply', want: 'rule', start: 0, pct: 1, v: 't' } }], steps: steps, space: [0.6, 0.8, 1.0] }; }
      if (c === 5) { var money = /\$/.test(intro), rounded = Math.round(exact.n / exact.d * (money ? 100 : 1)) / (money ? 100 : 1);
        steps.push(ruleStep, step('(b) Substitute t = ' + t4 + ' and round.', cx[1] + '(' + t4 + ')\\approx ' + (money ? rounded.toFixed(2) : rounded), 2));
        return { variant: 'ea5', prompt: intro, parts: [writePart, { label: 'b', prompt: 'Find ' + cx[2] + ' after ' + t4 + ' years. Round to the nearest ' + (money ? 'cent' : 'whole number') + '.', answer: M(money ? rounded.toFixed(2) : String(rounded)), check: { type: 'exp-apply', want: 'value', start: 0, pct: 1, time: 2, round: money ? 2 : 0 } }], steps: steps, space: [0.9, 1.1, 1.3] }; }
      // c7: write the function, then find when it first passes a target
      var target = up ? Math.round(a0 * r.pick([1.3, 1.5, 1.8, 2])) : Math.round(a0 * r.pick([0.5, 0.6, 0.7])), when = null, vv = F(a0);
      for (var y = 0; y <= 60; y++) { if (up ? vv.n / vv.d > target : vv.n / vv.d < target) { when = y; break; } vv = vv.mul(base.f); }
      need(when !== null && when >= 2 && when <= 12 && Math.abs(F(a0).mul(fpow(base.f, when)).sub(target).n) > 0);
      steps.push(step('(a) ' + M('a=' + a0) + ' and ' + M('b=' + fStr) + '.', rule, 2), step('(b) Make a table of values year by year (or use a graph) until the value is ' + (up ? 'more' : 'less') + ' than ' + target.toLocaleString('en-US') + '.', 't=' + when, 2));
      return { variant: 'ea7', prompt: intro,
        parts: [writePart,
                { label: 'b', prompt: 'After how many whole years will ' + cx[2] + ' first be ' + (up ? 'more' : 'less') + ' than ' + target.toLocaleString('en-US') + '?', answer: 'After ' + M(String(when)) + ' years', check: { type: 'exp-apply', want: 'when', start: 0, pct: 1, threshold: 2 } }],
        steps: steps, space: [1.0, 1.3, 1.6] };
    }
  });

  /* ================= APPLY · compound interest and continuous growth ================= */
  var PER = { annually: 1, semiannually: 2, quarterly: 4, monthly: 12, daily: 365 };
  var SAVERS = ['Maya', 'Jordan', 'Luis', 'Priya', 'Sam', 'Avery', 'Noah', 'Zoe', 'Elena', 'Marcus'];
  function dollars(x) { var cents = Math.round(x * 100), d = Math.floor(cents / 100), c2 = cents % 100; return '$' + String(d).replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (c2 ? '.' + (c2 < 10 ? '0' : '') + c2 : '.00'); }
  function whole(x) { return '$' + String(x).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function grow(P, rate, how, t) { return how === 'continuously' ? P * Math.exp(rate / 100 * t) : P * Math.pow(1 + rate / 100 / PER[how], PER[how] * t); }
  function safeCents(x) { var f = x * 100 - Math.floor(x * 100); return Math.abs(f - 0.5) > 1e-4; }
  skill({
    id: 'compound', best: [1, 2], tag: 'APPLY', name: 'Compound interest and continuous growth',
    blurb: 'Interest compounded once a year (CP2) → several times a year, interest earned (CP1) → compounded continuously, comparing two accounts (Honors).',
    generate: function (ctx) {
      var r = ctx.rng, c = ctx.c, who = r.pick(SAVERS), P = r.int(c <= 2 ? 5 : 10, c <= 2 ? 40 : 100) * 100, rate = c <= 2 ? r.int(2, 8) : r.pick([2, 2.5, 3, 3.5, 4, 4.5, 5, 6, 7]), steps = [];
      var t = c === 1 ? r.int(2, 3) : c === 2 ? r.int(4, 10) : r.int(3, 20);
      var how = c <= 2 ? 'annually' : c === 3 ? r.pick(['semiannually', 'quarterly']) : c === 4 ? r.pick(['monthly', 'quarterly']) : c === 5 ? 'continuously' : r.pick(['monthly', 'daily', 'continuously']);
      var formula = how === 'continuously' ? 'A=Pe^{rt}' : how === 'annually' ? 'A=P(1+r)^{t}' : 'A=P\\left(1+\\frac{r}{n}\\right)^{nt}';
      if (c === 7) {
        var r1 = r.pick([3, 3.5, 4, 4.5, 5]), r2 = r1 + r.pick([-0.25, -0.1, 0.1, 0.25]), h1 = r.pick(['quarterly', 'monthly', 'annually']), h2 = 'continuously';
        var A1 = grow(P, r1, h1, t), A2 = grow(P, r2, h2, t); need(safeCents(A1) && safeCents(A2));
        var c1 = Math.round(A1 * 100), c2 = Math.round(A2 * 100); need(c1 !== c2);
        var win = c1 > c2 ? 'A' : 'B', diff = Math.abs(c1 - c2) / 100;
        steps.push(step('Account A: ⟨A=P\\left(1+\\frac{r}{n}\\right)^{nt}⟩ with ⟨r=' + r1 / 100 + '⟩, ⟨n=' + PER[h1] + '⟩.', '', 1), step('Account A balance: ' + dollars(A1) + '.', '', 2));
        steps.push(step('Account B: ⟨A=Pe^{rt}⟩ with ⟨r=' + r2 / 100 + '⟩.', '', 1), step('Account B balance: ' + dollars(A2) + '.', '', 2), step('Account ' + win + ' has ' + dollars(diff) + ' more.', '', 1));
        return { variant: 'cmp-' + h1, prompt: 'Account A pays ' + r1 + '% interest compounded ' + h1 + '. Account B pays ' + r2 + '% interest compounded ' + h2 + '. ' + who + ' deposits ' + whole(P) + ' in one of them for ' + t + ' years. Which account gives more money, and how much more? Round each balance to the nearest cent.',
          parts: [{ answer: 'Account ' + win + ', by ' + dollars(diff), check: { type: 'compound', want: 'compare' } }], steps: steps, space: [1.3, 1.6, 1.9] };
      }
      var A = grow(P, rate, how, t), want = (c === 4 || c === 6) && r.chance(0.5) ? 'interest' : 'balance', val = want === 'interest' ? A - P : A;
      need(safeCents(A));
      var nTxt = how === 'continuously' ? '' : how === 'annually' ? '' : ', ⟨n=' + PER[how] + '⟩';
      steps.push(step('Use ⟨' + formula + '⟩ with ⟨P=' + P + '⟩, ⟨r=' + rate / 100 + '⟩' + nTxt + ', ⟨t=' + t + '⟩.', '', 2));
      steps.push(step('Balance: ' + dollars(A) + '.', '', 2));
      if (want === 'interest') steps.push(step('Interest earned = balance − deposit = ' + dollars(A) + ' − ' + whole(P) + '.', '', 1));
      return { variant: 'ci-' + how + '-' + want,
        prompt: who + ' deposits ' + whole(P) + ' in an account that pays ' + rate + '% interest compounded ' + how + '. ' + (want === 'interest' ? 'How much interest does the account earn in ' + t + ' years?' : 'How much is in the account after ' + t + ' years?') + ' Round to the nearest cent.',
        parts: [{ answer: dollars(Math.round(A * 100) / 100 - (want === 'interest' ? P : 0)), check: { type: 'compound', want: want } }], steps: steps, space: [0.9, 1.1, 1.3] };
      void val;
    }
  });


  // Lesson-specific aliases of independently verified generators; these remain selectable skills.
  (function(){var base=skills.find(function(s){return s.id==="exp-graph";});if(!base)return;
    skill({id:"exponential-graph-features",best:base.best,tag:base.tag,name:"Read exponential graph features",blurb:"Determine domain, range and growth/decay from exponential graphs.",
      difficultyProfile:'focused',fixedDifficulty:3,generate:function(ctx){return base.generate(Object.assign({},ctx,{c:3}));}});
  })();
  /* Student-ready exponential graphing with three integer-coordinate anchor points. */
  skill({
    id:'exp-graph-hand',difficultyProfile:'focused',best:[0,1],tag:'GROWTH',name:'Graph an exponential function by plotting points',
    blurb:'Plot points for x = −1, 0 and 1, then see the growth/decay curve.',
    generate:function(ctx){
      var r=ctx.rng,n=r.int(1,4),d=r.int(1,4),a=r.int(1,8),k=r.int(-6,5);
      need(n!==d && a*d%n===0 && a*n%d===0);
      var base=d===1?String(n):'\\left(\\frac{'+n+'}{'+d+'}\\right)';
      var suffix=k===0?'':(k>0?'+'+k:String(k));
      var eq='y='+a+'\\cdot '+base+'^{x}'+suffix;
      var values=[a*d/n+k,a+k,a*n/d+k];
      need(values.every(function(v){return Number.isInteger(v)&&Math.abs(v)<=9;}));
      var pts=[];
      for(var x=-4;x<=4;x+=0.125){var y=a*Math.pow(n/d,x)+k;if(y>=-10&&y<=10)pts.push([x,y]);}
      need(pts.length>=5);
      var key=plane([-10,10,-10,10],{curves:[pts],points:[{x:-1,y:values[0]},{x:0,y:values[1]},{x:1,y:values[2]}]});
      var steps=[step('Evaluate the function at x = −1, 0, and 1.', '',2),
        step('Plot the three points and draw a smooth growth or decay curve.', '',2)];
      return {variant:'explot'+a+'-'+n+'-'+d+'-'+k,prompt:'Graph '+M(eq)+'. Plot points for '+M('x=-1')+', '+M('x=0')+', and '+M('x=1')+'.',
        fig:plane([-10,10,-10,10]),parts:[{answer:M(String(a+k)),answerFig:key,check:{type:'exp-graph-points',a:a,n:n,d:d,k:k,eq:eq}}],
        steps:steps,space:[0.8,1,1.2]};

    }
  });

  NS.registerSkillSet({
    id: 'algebra1-exponential-functions', course: 'algebra1', courseName: 'Algebra 1', unit: 'exponential-functions', unitName: 'Exponential Functions',
    title: 'The Exponential Eatery',
    tags: { EVAL: 'Evaluating exponential functions', GROWTH: 'Growth, decay and graphs', MODEL: 'Linear vs. exponential; writing rules', SOLVE: 'Exponential equations', SEQUENCE: 'Geometric sequences', APPLY: 'Growth and decay in context' },
    reference:
      '<div class="mm-refgrid">' +
      '<section><h4>Exponential functions</h4><p>⟨y=a\\cdot b^{x}⟩: ⟨a⟩ is the initial value (the y-intercept), ⟨b⟩ is the factor.</p><p>⟨b>1⟩: growth. ⟨0<b<1⟩: decay.</p></section>' +
      '<section><h4>Percent rates</h4><p>Growth: ⟨b=1+r⟩. Decay: ⟨b=1-r⟩.</p><p>5% growth: ⟨b=1.05⟩. 20% decay: ⟨b=0.8⟩.</p></section>' +
      '<section><h4>Exponent rules</h4><p>⟨b^{0}=1⟩, ⟨b^{-n}=\\frac{1}{b^{n}}⟩</p><p>If ⟨b^{m}=b^{n}⟩, then ⟨m=n⟩.</p></section>' +
      '<section><h4>Graphs</h4><p>⟨y=a\\cdot b^{x}+k⟩ has the horizontal asymptote ⟨y=k⟩.</p><p>Domain: all real numbers. Range: above (or below) the asymptote.</p></section>' +
      '<section><h4>Linear or exponential?</h4><p>Equal differences: linear. Equal ratios: exponential.</p></section>' +
      '<section><h4>Geometric sequences</h4><p>Explicit: ⟨a_n=a_1\\cdot r^{n-1}⟩. Recursive: ⟨a_n=r\\cdot a_{n-1}⟩.</p></section></div>',
    gaps: [],
    skills: skills
  });
})(typeof window !== 'undefined' ? window : globalThis);
