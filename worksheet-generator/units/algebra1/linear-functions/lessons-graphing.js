/* Category B — Graphing Linear Equations (sub-lessons 6-9). */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr, F = NS.frac.F, T = NS.tex, gen = NS.gen, LF = NS.lf;
  var M = T.M, num = T.num, numP = T.numP, pt = T.pt, lin = T.lin;
  var U = LF.UNIT;
  var NO_GRID_SPACE = [1.9, 2.6, 3.3];

  function blankFig(ctx) { return ctx.grids ? LF.spec(LF.W10) : null; }
  function noGridNote(ctx) { return ctx.grids ? '' : ' <span class="note">(Use graph paper.)</span>'; }

  /* Lattice points of y = mx+b inside the window, chosen to show the rise/run pattern. */
  function plotPoints(m, b, w) {
    m = Fr.of(m); var pts = [], d = m.d, n = m.n;
    function inside(x, y) { return Math.abs(x) <= w && Math.abs(y.val()) <= w; }
    var cand = [0, d, -d, 2 * d, -2 * d, 3 * d, -3 * d];
    cand.forEach(function (x) {
      var y = m.mul(x).add(b);
      if (y.isInt() && inside(x, y) && pts.length < 3) pts.push({ x: x, y: y.n, label: true });
    });
    return pts;
  }

  /* 6 ---------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-graph-slope-intercept', unit: U, category: 'graphing', num: 6,
    title: 'Graph equations in slope-intercept form',
    instruction: 'Graph each equation. Plot the y-intercept first, then use the slope to find more points.',
    layout: 'row', figWidth: 2.75, space: [0.0, 0.15, 0.5],
    generate: function (ctx) {
      var m = gen.slope(ctx), b = gen.intercept(ctx, { max: 8, allowZero: true });
      gen.need(gen.latticeCount(m, b, 10) >= 3);
      var pts = plotPoints(m, b, 10);
      gen.need(pts.length >= 3 && pts.some(function (p) { return p.x === 0; }));
      // verify every plotted point satisfies the equation
      pts.forEach(function (p) { gen.need(m.mul(p.x).add(b).eq(p.y)); });
      var up = m.n > 0 ? 'up ' + m.n : 'down ' + Math.abs(m.n);
      return {
        prompt: 'Graph ' + M(T.eqSI(m, b)) + '.' + noGridNote(ctx),
        fig: blankFig(ctx), figWhere: ctx.grids ? 'right' : 'none', space: ctx.grids ? null : NO_GRID_SPACE,
        answerFig: LF.spec(LF.W10, [LF.line(m, b)], pts),
        answer: 'The line with slope ' + M(num(m)) + ' and y-intercept ' + M(pt(0, b)),
        steps: [
          'Identify the slope and y-intercept: ' + M('m=' + num(m) + ',\\ \\ b=' + num(b)),
          'Plot the y-intercept ' + M(pt(0, b)) + '.',
          'Use the slope ' + M(num(m)) + ' (rise over run): from ' + M(pt(0, b)) + ' go ' + (m.n > 0 ? 'up ' : 'down ') + Math.abs(m.n) + ' and right ' + m.d + ' to plot ' + M(pt(m.d, Fr.of(b).add(m.n))) + '.',
          'Draw a straight line through the points and extend it with arrows.'
        ],
        key: 's6|' + m + '|' + b, equiv: String(m)
      };
    }
  });

  /* 7 ---------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-graph-table', unit: U, category: 'graphing', num: 7,
    title: 'Graph equations by creating a table',
    instruction: 'Complete the table of values for each equation, then graph the line.',
    layout: 'row', figWidth: 2.75, space: [0.0, 0.15, 0.5],
    generate: function (ctx) {
      var rng = ctx.rng;
      var m = gen.slope(ctx), d = m.d, b = gen.intercept(ctx, { max: 7, allowZero: true });
      var xs = [-2, -1, 0, 1, 2].map(function (k) { return k * d; });
      var ys = xs.map(function (x) { return m.mul(x).add(b); });
      gen.need(ys.every(function (y) { return y.isInt() && Math.abs(y.n) <= 10; }));
      gen.need(xs.every(function (x) { return Math.abs(x) <= 10; }));
      var useStd = ctx.difficulty === 'honors' && rng.chance(0.45);
      var eq, st = T.toStandard(m, b);
      if (useStd) {
        gen.need(st.B !== 0 && Math.abs(st.A) <= 12 && Math.abs(st.C) <= 60);
        // independent check: every table row satisfies Ax + By = C
        xs.forEach(function (x, i) { gen.need(st.A * x + st.B * ys[i].n === st.C); });
        eq = T.eqStd(st.A, st.B, st.C);
      } else eq = T.eqSI(m, b);
      var blankTbl = NS.table([{ label: 'x', cells: xs }, { label: 'y', cells: ys, blank: true }]);
      var fullTbl = NS.table([{ label: 'x', cells: xs }, { label: 'y', cells: ys, blank: true }], true);
      var pts = xs.map(function (x, i) { return { x: x, y: ys[i].n }; });
      function subst(x, y) {                       // one substitution, written out
        if (useStd) {
          var left = (st.A === 1 ? numP(x) : num(st.A) + '(' + num(x) + ')') + (st.B > 0 ? '+' : '') + lin([[st.B, 'y']]);
          return left + '=' + num(st.C) + '\\ \\Rightarrow\\ ' + lin([[st.B, 'y']]) + '=' + num(st.C - st.A * Fr.of(x).val()) + '\\ \\Rightarrow\\ y=' + num(y);
        }
        var prod = m.eq(1) ? num(x) : m.eq(-1) ? '-' + numP(x) : num(m) + '(' + num(x) + ')';
        var bt = b === 0 ? '' : (b > 0 ? '+' : '-') + Math.abs(b);
        return 'y=' + prod + bt + '=' + num(y);
      }
      var head = 'Complete the table for ' + M(eq) + '. Then graph the line.' + noGridNote(ctx);
      return {
        prompt: head + '<div class="tbl">' + blankTbl + '</div>',
        keyPrompt: head + '<div class="tbl">' + fullTbl + '</div>',
        fig: blankFig(ctx), figWhere: ctx.grids ? 'right' : 'none', space: ctx.grids ? null : NO_GRID_SPACE,
        answerFig: LF.spec(LF.W10, [LF.line(m, b)], pts),
        answer: 'Table values ' + M('y=' + ys.map(function (y) { return num(y); }).join(',\\ ')) + ' and the line through them',
        steps: ['Substitute each ' + M('x') + '-value into ' + M(eq) + (useStd ? ' and solve for ' + M('y') : '') + '.']
          .concat(xs.slice(0, 2).map(function (x, i) { return 'When ' + M('x=' + num(x)) + ': ' + M(subst(x, ys[i])); }))
          .concat(['Plot the points ' + M(pts.map(function (p) { return pt(p.x, p.y); }).join(',\\ ')) + ' and draw the line.']),
        key: 's7|' + eq + '|' + xs.join(','), equiv: String(m) + '|' + b
      };
    }
  });

  /* 8 ---------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-graph-intercepts', unit: U, category: 'graphing', num: 8,
    title: 'Graph equations using x- and y-intercepts',
    instruction: 'Find the x- and y-intercepts of each equation, then graph the line.',
    layout: 'row', figWidth: 2.75, space: [0.0, 0.15, 0.5],
    generate: function (ctx) {
      var rng = ctx.rng, R = ctx.difficulty === 'basic' ? 6 : ctx.difficulty === 'standard' ? 8 : 10;
      var capC = ctx.difficulty === 'basic' ? 24 : ctx.difficulty === 'standard' ? 48 : 90;
      var a = rng.nonzero(-R, R), b = rng.nonzero(-R, R);
      var st = T.toStandard(F(-b, a), b);
      gen.need(st.A !== 0 && st.B !== 0 && st.C !== 0);
      gen.need(F(st.C, st.A).eq(a) && F(st.C, st.B).eq(b));          // verify intercepts
      gen.need(Math.abs(st.C) <= capC && Math.abs(st.A) <= 14 && Math.abs(st.B) <= 14);
      var eq = T.eqStd(st.A, st.B, st.C);
      var pts = [{ x: a, y: 0, label: true }, { x: 0, y: b, label: true }];
      var blanks = '<div class="blanks">' + M('x\\text{-intercept: }') + ' (<span class="ln"></span>, 0)<br>' + M('y\\text{-intercept: }') + ' (0, <span class="ln"></span>)</div>';
      return {
        prompt: 'Graph ' + M(eq) + ' using its intercepts.' + noGridNote(ctx) + blanks,
        keyPrompt: 'Graph ' + M(eq) + ' using its intercepts.',
        fig: blankFig(ctx), figWhere: ctx.grids ? 'right' : 'none', space: ctx.grids ? null : NO_GRID_SPACE,
        answerFig: LF.spec(LF.W10, [LF.line(F(-b, a), b)], pts),
        answer: M('x\\text{-intercept: }' + pt(a, 0)) + ' &nbsp; ' + M('y\\text{-intercept: }' + pt(0, b)),
        steps: [
          'To find the x-intercept, let ' + M('y=0') + ': ' + M(lin([[st.A, 'x']]) + '=' + num(st.C)) + ', so ' + M('x=' + num(a)) + '. The point is ' + M(pt(a, 0)) + '.',
          'To find the y-intercept, let ' + M('x=0') + ': ' + M(lin([[st.B, 'y']]) + '=' + num(st.C)) + ', so ' + M('y=' + num(b)) + '. The point is ' + M(pt(0, b)) + '.',
          'Plot both intercepts and draw the line through them.'
        ],
        key: 's8|' + eq, equiv: a + '|' + b
      };
    }
  });

  /* 9 ---------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-graph-horizontal-vertical', unit: U, category: 'graphing', num: 9,
    title: 'Graph horizontal and vertical lines',
    instruction: 'Graph each line. Then answer the question.',
    layout: 'half', figWidth: 2.3, space: [0.2, 0.3, 0.7],
    generate: function (ctx) {
      var rng = ctx.rng, W = LF.W8;
      var types = ctx.difficulty === 'basic' ? ['h', 'v'] : ['h', 'v', 'both'];
      var t = types[(ctx.slot + ctx.stable) % types.length];
      var fig = ctx.grids ? LF.spec(W) : null, note = noGridNote(ctx);
      var c = rng.nonzero(-7, 7), prompt, ans, steps, answerFig, key;
      if (t === 'h') {
        prompt = 'Graph ' + M('y=' + c) + '.' + note + '<div class="blanks">Slope: <span class="ln"></span></div>';
        ans = 'Slope ' + M('=0') + ' (horizontal line through ' + M(pt(0, c)) + ')';
        steps = ['Every point has ' + M('y=' + c) + ', so the line is horizontal through ' + M(pt(0, c)) + '.', 'A horizontal line has slope 0.'];
        answerFig = LF.spec(W, [LF.line(0, c)], [{ x: 0, y: c, label: true }]); key = 'h' + c;
      } else if (t === 'v') {
        prompt = 'Graph ' + M('x=' + c) + '.' + note + '<div class="blanks">Slope: <span class="ln"></span></div>';
        ans = 'Slope is undefined (vertical line through ' + M(pt(c, 0)) + ')';
        steps = ['Every point has ' + M('x=' + c) + ', so the line is vertical through ' + M(pt(c, 0)) + '.', 'A vertical line has an undefined slope.'];
        answerFig = LF.spec(W, [LF.vline(c)], [{ x: c, y: 0, label: true }]); key = 'v' + c;
      } else {
        var h, k; do { h = rng.nonzero(-7, 7); k = rng.nonzero(-7, 7); } while (h === k);
        prompt = 'Graph ' + M('x=' + h) + ' and ' + M('y=' + k) + ' on the same grid.' + note + '<div class="blanks">They intersect at (<span class="ln"></span>, <span class="ln"></span>).</div>';
        ans = 'They intersect at ' + M(pt(h, k));
        steps = [M('x=' + h) + ' is a vertical line and ' + M('y=' + k) + ' is a horizontal line.', 'They cross where ' + M('x=' + h) + ' and ' + M('y=' + k) + ': ' + M(pt(h, k)) + '.'];
        answerFig = LF.spec(W, [LF.vline(h), LF.line(0, k)], [{ x: h, y: k, label: true }]); key = 'b' + h + ',' + k;
      }
      return {
        prompt: prompt, keyPrompt: prompt.replace(/<div class="blanks">.*<\/div>/, ''),
        fig: fig, figWhere: ctx.grids ? 'below' : 'none', space: ctx.grids ? null : [1.4, 1.9, 2.4],
        answerFig: answerFig, answer: ans, steps: steps, key: 's9|' + t + '|' + key, equiv: t + '|' + key
      };
    }
  });
})(typeof window !== 'undefined' ? window : globalThis);
