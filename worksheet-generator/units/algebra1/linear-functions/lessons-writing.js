/* Category C — Writing Linear Equations (sub-lessons 10-13). */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr, F = NS.frac.F, T = NS.tex, gen = NS.gen, LF = NS.lf;
  var M = T.M, num = T.num, numP = T.numP, pt = T.pt, lin = T.lin;
  var U = LF.UNIT;

  /* 10 --------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-write-from-graph', unit: U, category: 'writing', num: 10,
    title: 'Write an equation from a graph',
    instruction: 'Write the equation of each line shown. Use slope-intercept form, ' + '(a vertical line is written as x = c).',
    layout: 'half', figWidth: 2.25, space: [0.25, 0.45, 0.9],
    generate: function (ctx) {
      var rng = ctx.rng, W = LF.W8, lim = 7;
      var special = null;
      if (ctx.difficulty === 'basic') special = rng.chance(0.08) ? 'h' : null;
      else { var r = rng.next(); special = r < 0.1 ? 'h' : r < 0.18 ? 'v' : null; }
      var spec, eq, steps, ans, key;
      if (special === 'h') {
        var c = gen.intercept(ctx, { max: 7, allowZero: true });
        var xa = rng.int(-6, -1), xb = rng.int(1, 6);
        spec = LF.spec(W, [LF.line(0, c)], [{ x: xa, y: c }, { x: xb, y: c }]);
        ans = M('y=' + c); key = 'h' + c;
        steps = ['The line is horizontal and passes through ' + M(pt(xa, c)) + ' and ' + M(pt(xb, c)) + '.', 'Every point has ' + M('y=' + c) + ', so the equation is ' + M('y=' + c) + '.'];
      } else if (special === 'v') {
        var cv = rng.nonzero(-7, 7);
        var ya = rng.int(-6, -1), yb = rng.int(1, 6);
        spec = LF.spec(W, [LF.vline(cv)], [{ x: cv, y: ya }, { x: cv, y: yb }]);
        ans = M('x=' + cv); key = 'v' + cv;
        steps = ['The line is vertical and passes through ' + M(pt(cv, ya)) + ' and ' + M(pt(cv, yb)) + '.', 'Every point has ' + M('x=' + cv) + ', so the equation is ' + M('x=' + cv) + '.'];
      } else {
        var m = gen.slope(ctx), b = gen.intercept(ctx, { max: 6, allowZero: true });
        var k = rng.pick([1, 2, 3]) * rng.sign();
        var x2 = m.d * k, y2 = Fr.of(b).add(m.n * k);
        gen.need(Math.abs(x2) <= lim && Math.abs(y2.n) <= lim && Math.max(Math.abs(x2), Math.abs(m.n * k)) >= 2);
        gen.need(gen.latticeCount(m, b, 8) >= 3);
        gen.need(Fr.of(y2).sub(b).div(x2).eq(m));                      // verify marked points give slope m
        spec = LF.spec(W, [LF.line(m, b)], [{ x: 0, y: b }, { x: x2, y: y2.n }]);
        eq = T.eqSI(m, b); ans = M(eq); key = m + '|' + b;
        steps = ['The line crosses the y-axis at ' + M(pt(0, b)) + ', so ' + M('b=' + num(b)) + '.',
          'From ' + M(pt(0, b)) + ' to ' + M(pt(x2, y2)) + ': ' + M('\\text{rise}=' + num(m.n * k) + ',\\ \\text{run}=' + num(x2)) + ', so ' + M('m=' + T.litFrac(num(m.n * k), num(x2)) + (T.litFrac(num(m.n * k), num(x2)) !== num(m) ? '=' + num(m) : '')) + '.',
          'Substitute into ' + M('y=mx+b') + ': ' + M(eq)];
      }
      return {
        prompt: 'Write the equation of the line.', fig: spec, figWhere: 'below',
        answer: ans, steps: steps, key: 's10|' + key, equiv: special ? special : String(key.split('|')[0])
      };
    }
  });

  /* 11 --------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-write-two-points', unit: U, category: 'writing', num: 11,
    title: 'Write an equation from two points',
    instruction: 'Write the equation of the line through each pair of points in slope-intercept form. (A vertical line is written as x = c.)',
    layout: 'half', space: [1.0, 1.9, 2.6],
    generate: function (ctx) {
      var rng = ctx.rng, lim = ctx.D.lim;
      var special = null;
      if (ctx.difficulty !== 'basic') { var r = rng.next(); special = r < 0.08 ? 'h' : r < 0.15 ? 'v' : null; }
      var P, Q, ans, steps, key, eqText;
      if (special === 'h') {
        var c = rng.int(-lim, lim), xa = rng.int(-lim, lim), xb; do { xb = rng.int(-lim, lim); } while (xb === xa);
        P = [xa, c]; Q = [xb, c]; eqText = 'y=' + c; key = 'h' + c + '|' + xa + ',' + xb;
        steps = ['Both points have the same ' + M('y') + '-value, so the line is horizontal.', 'The equation is ' + M('y=' + c) + '.'];
      } else if (special === 'v') {
        var cv = rng.int(-lim, lim), ya = rng.int(-lim, lim), yb; do { yb = rng.int(-lim, lim); } while (yb === ya);
        P = [cv, ya]; Q = [cv, yb]; eqText = 'x=' + cv; key = 'v' + cv + '|' + ya + ',' + yb;
        steps = ['Both points have the same ' + M('x') + '-value, so the line is vertical.', 'The equation is ' + M('x=' + cv) + '.'];
      } else {
        var m = gen.slope(ctx), d = m.d, k = rng.pick([1, 1, 2, 3]) * rng.sign();
        var x1 = ctx.allowFracIntercept ? rng.int(-lim, lim) : d * rng.int(-Math.floor(lim / d), Math.floor(lim / d));
        var y1 = rng.int(-lim, lim), x2 = x1 + d * k, y2 = y1 + m.n * k;
        gen.need(Math.abs(x2) <= lim && Math.abs(y2) <= lim);
        var b = Fr.of(y1).sub(m.mul(x1));
        gen.need(Math.abs(b.val()) <= 20 && (ctx.allowFracIntercept || b.isInt()));
        gen.need(b.d <= 6);
        var A = [x1, y1], B = [x2, y2]; P = rng.chance(0.5) ? A : B; Q = P === A ? B : A;
        gen.need(Fr.of(Q[1] - P[1]).div(Q[0] - P[0]).eq(m));
        gen.need(Fr.of(P[1]).eq(m.mul(P[0]).add(b)) && Fr.of(Q[1]).eq(m.mul(Q[0]).add(b)));   // both points satisfy the answer
        var fb = LF.findBSteps(m, P[0], P[1]);
        steps = LF.slopeSteps(P, Q).concat(fb.steps);
        eqText = T.eqSI(m, b); key = LF.pairKey([A, B]);
      }
      return {
        prompt: 'Write the equation of the line through ' + M(pt(P[0], P[1])) + ' and ' + M(pt(Q[0], Q[1])) + '.',
        answer: M(eqText), steps: steps, key: 's11|' + key, equiv: eqText
      };
    }
  });

  /* 12 --------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-write-slope-point', unit: U, category: 'writing', num: 12,
    title: 'Write an equation given a slope and a point',
    instruction: 'Write the equation of the line with the given slope that passes through the given point. Use slope-intercept form.',
    layout: 'half', space: [0.9, 1.6, 2.3],
    generate: function (ctx) {
      var rng = ctx.rng, lim = ctx.D.lim;
      var zero = ctx.difficulty !== 'basic' && rng.chance(0.1);
      var m = zero ? F(0) : gen.slope(ctx), d = m.d;
      var x1 = ctx.allowFracIntercept ? rng.int(-lim, lim) : d * rng.int(-Math.floor(lim / d), Math.floor(lim / d));
      var y1 = rng.int(-lim, lim);
      var b = Fr.of(y1).sub(m.mul(x1));
      gen.need(Math.abs(b.val()) <= 20 && b.d <= 6 && (ctx.allowFracIntercept || b.isInt()));
      gen.need(m.mul(x1).add(b).eq(y1));                                   // verify the point is on the line
      var steps;
      if (zero) steps = ['A slope of 0 means the line is horizontal.', 'Every point has the same ' + M('y') + '-value as ' + M(pt(x1, y1)) + ', so ' + M('y=' + y1) + '.'];
      else steps = LF.findBSteps(m, x1, y1).steps;
      return {
        prompt: 'Slope ' + M('m=' + num(m)) + ', point ' + M(pt(x1, y1)),
        answer: M(T.eqSI(m, b)), steps: steps, key: 's12|' + m + '|' + x1 + ',' + y1, equiv: 'm' + m
      };
    }
  });

  /* 13 --------------------------------------------------------------- */
  var TYPES = {
    basic: ['parallel', 'perpendicular', 'classify'],
    standard: ['parallel', 'perpendicular', 'classify', 'perpendicular'],
    honors: ['parallel-std', 'perpendicular-std', 'classify', 'perpendicular', 'parallel']
  };
  NS.registerLesson({
    id: 'lf-write-parallel-perpendicular', unit: U, category: 'writing', num: 13,
    title: 'Write equations of parallel and perpendicular lines',
    instruction: 'Follow each direction. Write equations in slope-intercept form.',
    layout: 'half', space: [1.1, 1.9, 2.6],
    generate: function (ctx) {
      var rng = ctx.rng, lim = Math.min(ctx.D.lim, 9);
      var types = TYPES[ctx.difficulty], type = types[(ctx.slot + ctx.stable) % types.length];
      var perpMode = type.indexOf('perpendicular') === 0;
      var useStd = /-std$/.test(type);

      /* the given line: slope g, intercept c.  For perpendicular problems in integers-only mode the
         given slope is +-1/k so that the perpendicular slope is a whole number. */
      function givenSlope(forPerp) {
        if (forPerp && ctx.numberMode === 'integers') return rng.chance(0.12) ? F(rng.sign()) : gen.slope(ctx, { unit: true });
        return gen.slope(ctx);
      }

      if (type === 'classify') {
        var want = ['parallel', 'perpendicular', 'neither'][(ctx.slot + ctx.stable) % 3];
        var m1 = givenSlope(want === 'perpendicular'), b1 = gen.intercept(ctx, { max: 8, allowZero: true });
        var m2, b2 = gen.intercept(ctx, { max: 8, allowZero: true });
        if (want === 'parallel') { m2 = m1; gen.need(b2 !== b1); }
        else if (want === 'perpendicular') m2 = m1.inv().neg();
        else {
          var opts = [m1.neg(), m1.inv(), m1.add(rng.pick([1, 2, -1, -2])), gen.slope(ctx)];
          m2 = rng.pick(opts);
          gen.need(!m2.isZero() && !m2.eq(m1) && !m2.mul(m1).eq(-1));
        }
        gen.need(m2.d <= 8 && Math.abs(m2.n) <= 12);
        // verify the intended relationship from the numbers themselves
        var rel = m1.eq(m2) ? 'parallel' : m1.mul(m2).eq(-1) ? 'perpendicular' : 'neither';
        gen.need(rel === want && !(rel === 'parallel' && b1 === b2));
        var std2 = ctx.difficulty === 'honors' && rng.chance(0.5);
        var e1 = T.eqSI(m1, b1), e2;
        var st2 = T.toStandard(m2, b2);
        if (std2) { gen.need(Math.abs(st2.A) <= 14 && Math.abs(st2.B) <= 14 && Math.abs(st2.C) <= 80); e2 = T.eqStd(st2.A, st2.B, st2.C); } else e2 = T.eqSI(m2, b2);
        var st = [];
        st.push('Line 1 has slope ' + M('m_1=' + num(m1)) + '.');
        st.push('Line 2' + (std2 ? ' (solve for ' + M('y') + ' to find the slope)' : '') + ' has slope ' + M('m_2=' + num(m2)) + '.');
        if (rel === 'parallel') st.push('The slopes are equal and the lines are different, so the lines are parallel.');
        else if (rel === 'perpendicular') st.push('The product of the slopes is ' + M(num(m1) + '\\cdot' + numP(m2) + '=-1') + ', so the lines are perpendicular.');
        else st.push('The slopes are not equal and their product is ' + M(num(m1.mul(m2))) + ', not ' + M('-1') + ', so the lines are neither parallel nor perpendicular.');
        return {
          prompt: 'Line 1: ' + M(e1) + '<br>Line 2: ' + M(e2) + '<br>Are the lines parallel, perpendicular, or neither?',
          answer: rel.charAt(0).toUpperCase() + rel.slice(1), steps: st,
          key: 's13c|' + e1 + '|' + e2, equiv: 'c|' + rel + '|' + m1
        };
      }

      var g = givenSlope(perpMode), c = gen.intercept(ctx, { max: 8, allowZero: true });
      var m = perpMode ? g.inv().neg() : g;
      // the point must give an integer intercept for the new line
      var step = m.d, x1 = step * rng.int(-Math.floor(lim / step), Math.floor(lim / step));
      var y1 = rng.int(-lim, lim);
      var b = Fr.of(y1).sub(m.mul(x1));
      gen.need(b.isInt() && Math.abs(b.n) <= 25);
      gen.need(!(m.eq(g) && b.eq(c)));                                     // not the same line
      gen.need(perpMode ? m.mul(g).eq(-1) : m.eq(g));                      // verify the relationship
      gen.need(m.d <= 9 && Math.abs(m.n) <= 12);
      var stG = T.toStandard(g, c), given;
      if (useStd) { gen.need(Math.abs(stG.A) <= 14 && Math.abs(stG.B) <= 14 && Math.abs(stG.C) <= 80); given = T.eqStd(stG.A, stG.B, stG.C); }
      else given = T.eqSI(g, c);
      var steps = [];
      if (useStd) steps.push('Solve for ' + M('y') + ' to find the slope of the given line: ' + M(T.eqSI(g, c)) + ', so its slope is ' + M(num(g)) + '.');
      else steps.push('The given line has slope ' + M(num(g)) + '.');
      if (perpMode) steps.push('A perpendicular line has the negative reciprocal slope (flip the fraction and change the sign): ' + M(num(g) + '\\ \\to\\ ' + num(m)) + '.');
      else steps.push('A parallel line has the same slope: ' + M('m=' + num(m)) + '.');
      steps = steps.concat(LF.findBSteps(m, x1, y1).steps);
      return {
        prompt: 'Write the equation of the line that is ' + (perpMode ? 'perpendicular' : 'parallel') + ' to ' + M(given) + ' and passes through ' + M(pt(x1, y1)) + '.',
        answer: M(T.eqSI(m, b)), steps: steps, key: 's13|' + type + '|' + given + '|' + x1 + ',' + y1, equiv: type + '|' + g
      };
    }
  });
})(typeof window !== 'undefined' ? window : globalThis);
