/* Category A — Slope (sub-lessons 1-5). */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr, F = NS.frac.F, T = NS.tex, gen = NS.gen, LF = NS.lf;
  var M = T.M, num = T.num, numP = T.numP, pt = T.pt, lin = T.lin;
  var U = LF.UNIT;

  /* 1 ---------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-slope-two-points', unit: U, category: 'slope', num: 1,
    title: 'Find slope from two points',
    instruction: 'Find the slope of the line that passes through each pair of points.',
    layout: 'half', space: [0.45, 0.95, 1.7],
    generate: function (ctx) {
      var rng = ctx.rng, lim = ctx.D.lim;
      var m = gen.slope(ctx);
      var k = rng.pick([1, 1, 2, 3]) * rng.sign();
      var dx = m.d * k, dy = m.n * k;
      var x1 = rng.int(-lim, lim), y1 = rng.int(-lim, lim), x2 = x1 + dx, y2 = y1 + dy;
      gen.need(Math.abs(x2) <= lim && Math.abs(y2) <= lim && Math.abs(dx) <= lim);
      var A = [x1, y1], B = [x2, y2];
      var P = rng.chance(0.5) ? A : B, Q = P === A ? B : A;
      gen.need(Fr.of(Q[1] - P[1]).div(Q[0] - P[0]).eq(m));          // verify
      return {
        prompt: 'Find the slope of the line through ' + M(pt(P[0], P[1])) + ' and ' + M(pt(Q[0], Q[1])) + '.',
        answer: M('m=' + num(m)),
        steps: LF.slopeSteps(P, Q),
        key: 's1|' + LF.pairKey([A, B]), equiv: 'm=' + m
      };
    }
  });

  /* 2 ---------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-slope-graph', unit: U, category: 'slope', num: 2,
    title: 'Find slope from a graph',
    instruction: 'Find the slope of each line. Two points on each line are marked.',
    layout: 'half', figWidth: 2.25, space: [0.2, 0.35, 0.8],
    generate: function (ctx) {
      var rng = ctx.rng, W = LF.W8, lim = 7;
      var m = gen.slope(ctx);
      var k = rng.pick([1, 2, 3]) * rng.sign();
      var dx = m.d * k, dy = m.n * k;
      gen.need(Math.max(Math.abs(dx), Math.abs(dy)) >= 3 && Math.max(Math.abs(dx), Math.abs(dy)) <= 10);
      var x1 = rng.int(-lim, lim), y1 = rng.int(-lim, lim), x2 = x1 + dx, y2 = y1 + dy;
      gen.need(Math.abs(x2) <= lim && Math.abs(y2) <= lim);
      var b = Fr.of(y1).sub(m.mul(x1));
      gen.need(Math.abs(b.val()) <= 40);
      var spec = LF.spec(W, [LF.line(m, b)], [{ x: x1, y: y1 }, { x: x2, y: y2 }]);
      var P = [x1, y1], Q = [x2, y2];
      return {
        prompt: 'Find the slope of the line shown.',
        fig: spec, figWhere: 'below',
        answer: M('m=' + num(m)),
        steps: ['Read two points on the line: ' + M(pt(x1, y1)) + ' and ' + M(pt(x2, y2)) + '.']
          .concat(['Count rise and run: ' + M('\\text{rise}=' + num(dy) + ',\\ \\text{run}=' + num(dx))])
          .concat(['Slope ' + M('m=\\frac{\\text{rise}}{\\text{run}}=' + T.litFrac(num(dy), num(dx)) + (T.litFrac(num(dy), num(dx)) !== num(m) ? '=' + num(m) : ''))]),
        key: 's2|' + LF.pairKey([P, Q]), equiv: 'm=' + m
      };
    }
  });

  /* 3 ---------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-slope-table', unit: U, category: 'slope', num: 3,
    title: 'Find slope from a table',
    instruction: 'Each table shows a linear function. Find the slope (rate of change).',
    layout: 'half', space: [0.2, 0.45, 1.0],
    generate: function (ctx) {
      var rng = ctx.rng, diff = ctx.difficulty;
      var m = gen.slope(ctx), d = m.d;
      var mult = diff === 'basic' ? rng.pick([1, 1, 2]) : diff === 'standard' ? rng.pick([1, 2, 2, 3]) : rng.pick([1, 2, 3, 4, 5]);
      var ncols = diff === 'honors' ? 5 : 4, xs = [];
      if (diff === 'honors' && rng.chance(0.5)) {              // unevenly spaced inputs
        var x = d * rng.int(-3, 0); xs.push(x);
        for (var i = 1; i < ncols; i++) { x += d * rng.pick([1, 2, 3]); xs.push(x); }
        var gaps = new Set(xs.slice(1).map(function (v, i2) { return v - xs[i2]; }));
        gen.need(gaps.size > 1);
      } else {
        var x0 = d * rng.int(-3, 1);
        for (var j = 0; j < ncols; j++) xs.push(x0 + j * d * mult);
      }
      var b = gen.intercept(ctx, { max: Math.min(ctx.D.maxB, 9), allowZero: true });
      var ys = xs.map(function (xx) { return m.mul(xx).add(b); });
      gen.need(ys.every(function (y) { return y.isInt() && Math.abs(y.n) <= 40; }));
      gen.need(xs.every(function (v) { return Math.abs(v) <= 24; }));
      // verify the table really is linear with slope m
      for (var t = 1; t < xs.length; t++) gen.need(ys[t].sub(ys[t - 1]).div(xs[t] - xs[t - 1]).eq(m));
      var html = NS.table([{ label: 'x', cells: xs }, { label: 'y', cells: ys }]);
      return {
        prompt: '<div class="tbl">' + html + '</div>',
        answer: M('m=' + num(m)),
        steps: ['Use any two points from the table, such as ' + M(pt(xs[0], ys[0])) + ' and ' + M(pt(xs[1], ys[1])) + '.']
          .concat(LF.slopeSteps([xs[0], ys[0].n], [xs[1], ys[1].n])),
        key: 's3|' + xs.join(',') + '|' + ys.map(String).join(','), equiv: 'm=' + m + '|' + (xs[1] - xs[0])
      };
    }
  });

  /* 4 ---------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-slope-missing-coordinate', unit: U, category: 'slope', num: 4,
    title: 'Find a missing coordinate given the slope',
    instruction: 'Find the missing coordinate so that the line through the two points has the given slope.',
    layout: 'half', space: [0.7, 1.35, 2.0],
    generate: function (ctx) {
      var rng = ctx.rng, lim = ctx.D.lim;
      var m = gen.slope(ctx);
      var unknown = rng.chance(0.5) ? 'x' : 'y';
      var k = rng.int(1, 3) * rng.sign();
      var dx = m.d * k, dy = m.n * k;
      var x1 = rng.int(-lim, lim), y1 = rng.int(-lim, lim), x2 = x1 + dx, y2 = y1 + dy;
      gen.need(Math.abs(x2) <= lim && Math.abs(y2) <= lim && Math.abs(dx) <= lim);
      var known = LF.ptVar(x1, y1);
      var other = unknown === 'x' ? LF.ptVar('x', y2) : LF.ptVar(x2, 'y');
      var first = rng.chance(0.5) ? known : other, second = first === known ? other : known;
      var ans = unknown === 'x' ? x2 : y2;
      // independent verification: plug the answer back in
      gen.need(Fr.of(y2 - y1).div(x2 - x1).eq(m));
      var steps = ['Let ' + M('(x_1,\\,y_1)=' + known) + ' be the known point and use ' + M('m=\\frac{y_2-y_1}{x_2-x_1}') + '.'];
      if (unknown === 'x') {
        var den = lin([[1, 'x'], [-x1, '']]);
        steps.push('Substitute: ' + M(num(m) + '=\\frac{' + num(y2) + '-' + numP(y1) + '}{x-' + numP(x1) + '}'));
        steps.push('Simplify: ' + M(num(m) + '=\\frac{' + num(dy) + '}{' + den + '}'));
        steps.push('Cross-multiply: ' + M(LF.coefTimes(m.n, den) + '=' + num(m.d * dy)));
        steps.push('Solve: ' + M(den + '=' + num(dx)) + ', so ' + M('x=' + num(x2)));
      } else {
        var num1 = lin([[1, 'y'], [-y1, '']]);
        steps.push('Substitute: ' + M(num(m) + '=\\frac{y-' + numP(y1) + '}{' + num(x2) + '-' + numP(x1) + '}'));
        steps.push('Simplify: ' + M(num(m) + '=\\frac{' + num1 + '}{' + num(dx) + '}'));
        steps.push('Multiply both sides by ' + M(num(dx)) + ': ' + M(num1 + '=' + num(m.mul(dx))));
        steps.push('Solve: ' + M('y=' + num(y2)));
      }
      return {
        prompt: 'The line through ' + M(first) + ' and ' + M(second) + ' has slope ' + M(num(m)) + '. Find ' + M(unknown) + '.',
        answer: M(unknown + '=' + num(ans)),
        steps: steps,
        key: 's4|' + unknown + '|' + x1 + ',' + y1 + '|' + m, equiv: unknown + '|' + m
      };
    }
  });

  /* 5 ---------------------------------------------------------------- */
  var CLASSES = ['positive', 'negative', 'zero', 'undefined'];
  NS.registerLesson({
    id: 'lf-slope-classify', unit: U, category: 'slope', num: 5,
    title: 'Identify positive, negative, zero, and undefined slopes',
    instruction: 'Is the slope of each line positive, negative, zero, or undefined?',
    layout: 'half', figWidth: 1.85, space: [0.25, 0.4, 0.8],
    generate: function (ctx) {
      var rng = ctx.rng, lim = Math.min(ctx.D.lim, 8);
      var cls = CLASSES[(ctx.slot + ctx.stable) % 4];
      var reps = cls === 'zero' || cls === 'undefined' ? ['points', 'eq', 'graph'] : ['points', 'eq', 'graph', 'std'];
      if (ctx.difficulty === 'basic') reps = reps.filter(function (r) { return r !== 'std'; });
      var rep = rng.pick(reps);
      var prompt, fig = null, mval = null, steps = [], keyTxt;
      var x1 = rng.int(-lim, lim), y1 = rng.int(-lim, lim), x2, y2, A, B;

      function pickPoints() {
        if (cls === 'zero') { y2 = y1; do { x2 = rng.int(-lim, lim); } while (x2 === x1); }
        else if (cls === 'undefined') { x2 = x1; do { y2 = rng.int(-lim, lim); } while (y2 === y1); }
        else {
          var m = gen.slope(ctx, { sign: cls === 'positive' ? 1 : -1 });
          var kk = rng.int(1, 3) * rng.sign(); x2 = x1 + m.d * kk; y2 = y1 + m.n * kk;
          gen.need(Math.abs(x2) <= lim && Math.abs(y2) <= lim);
        }
        A = [x1, y1]; B = [x2, y2];
      }
      if (rep === 'points') {
        pickPoints();
        prompt = 'The line through ' + M(pt(x1, y1)) + ' and ' + M(pt(x2, y2));
        if (cls === 'undefined') steps = ['The ' + M('x') + '-coordinates are equal, so the line is vertical and the run is 0.', M('m=\\frac{' + num(y2 - y1) + '}{0}') + ' is undefined.'];
        else steps = LF.slopeSteps(A, B);
        mval = cls === 'undefined' ? null : Fr.of(y2 - y1).div(x2 - x1);
      } else if (rep === 'graph') {
        pickPoints();
        var mm = cls === 'undefined' ? null : Fr.of(y2 - y1).div(x2 - x1);
        var line = cls === 'undefined' ? LF.vline(x1) : LF.line(mm, Fr.of(y1).sub(mm.mul(x1)));
        fig = LF.spec(LF.W8, [line], [{ x: x1, y: y1 }, { x: x2, y: y2 }]);
        prompt = 'The line shown'; mval = mm;
        steps = cls === 'undefined' ? ['The line is vertical, so its slope is undefined.'] : cls === 'zero' ? ['The line is horizontal, so its slope is 0.'] :
          ['The line ' + (cls === 'positive' ? 'rises' : 'falls') + ' from left to right, so the slope is ' + cls + '.'].concat(LF.slopeSteps(A, B));
      } else if (rep === 'eq') {
        if (cls === 'undefined') { var c = rng.nonzero(-9, 9); prompt = M('x=' + c); steps = ['A vertical line ' + M('x=' + c) + ' has an undefined slope.']; }
        else if (cls === 'zero') { var c2 = rng.int(-9, 9); prompt = M('y=' + c2); steps = ['A horizontal line ' + M('y=' + c2) + ' has slope 0.']; mval = F(0); }
        else {
          var mq = gen.slope(ctx, { sign: cls === 'positive' ? 1 : -1 }), bq = gen.intercept(ctx, { allowZero: true });
          prompt = M(T.eqSI(mq, bq)); mval = mq;
          steps = ['In ' + M('y=mx+b') + ' form the slope is the coefficient of ' + M('x') + ': ' + M('m=' + num(mq)) + '.'];
        }
      } else {                                                      // std: Ax + By = C
        var mq2 = gen.slope(ctx, { sign: cls === 'positive' ? 1 : -1, int: true });
        var b2 = rng.int(-6, 6), st = T.toStandard(mq2, b2);
        prompt = M(T.eqStd(st.A, st.B, st.C)); mval = mq2;
        var left = lin([[-st.A, 'x'], [st.C, '']]);
        steps = ['Solve for ' + M('y') + ': ' + M(lin([[st.B, 'y']]) + '=' + left), 'Divide by ' + M(num(st.B)) + ': ' + M(T.eqSI(mq2, F(st.C, st.B))),
          'The slope is ' + M('m=' + num(mq2)) + '.'];
      }
      var word = cls === 'undefined' ? 'undefined' : cls;
      var ans = cls === 'undefined' ? 'Undefined' : cls === 'zero' ? 'Zero ' + M('(m=0)') : cls.charAt(0).toUpperCase() + cls.slice(1) + (mval ? ' ' + M('(m=' + num(mval) + ')') : '');
      // verify classification of the final slope value
      if (cls === 'positive') gen.need(mval && mval.sign() > 0);
      if (cls === 'negative') gen.need(mval && mval.sign() < 0);
      if (cls === 'zero') gen.need(mval && mval.isZero());
      if (cls === 'undefined') gen.need(mval === null);
      return {
        prompt: prompt, fig: fig, figWhere: 'below',
        answer: ans, steps: steps,
        key: 's5|' + rep + '|' + cls + '|' + prompt + '|' + JSON.stringify(fig && fig.points), equiv: cls + '|' + rep
      };
    }
  });
})(typeof window !== 'undefined' ? window : globalThis);
