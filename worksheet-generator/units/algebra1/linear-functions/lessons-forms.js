/* Category D — Forms of Linear Equations (sub-lessons 14-18). */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr, F = NS.frac.F, T = NS.tex, gen = NS.gen, LF = NS.lf;
  var M = T.M, num = T.num, numP = T.numP, pt = T.pt, lin = T.lin;
  var U = LF.UNIT;

  function fracIntercept(ctx) {                    // a non-integer intercept like 1/2 or -3/4
    var d = ctx.rng.pick([2, 3, 4]), n;
    do { n = ctx.rng.int(-7, 7); } while (n === 0 || n % d === 0);
    return F(n, d);
  }

  /* 14 --------------------------------------------------------------- */
  var FORMS = {
    basic: ['plain', 'plain', 'noB', 'unit'],
    standard: ['plain', 'unit', 'noB', 'commuted', 'fn'],
    honors: ['plain', 'fn', 'commuted', 'unit', 'horizontal', 'noB']
  };
  NS.registerLesson({
    id: 'lf-identify-slope-intercept', unit: U, category: 'forms', num: 14,
    title: 'Identify slope and y-intercept from slope-intercept form',
    instruction: 'State the slope and the y-intercept of each line.',
    layout: 'half', space: [0.2, 0.3, 0.7],
    generate: function (ctx) {
      var rng = ctx.rng, forms = FORMS[ctx.difficulty], form = forms[(ctx.slot + ctx.stable) % forms.length];
      var m = form === 'unit' ? F(rng.sign()) : form === 'horizontal' ? F(0) : gen.slope(ctx);
      var b = form === 'noB' ? 0 : (ctx.allowFracIntercept && rng.chance(0.35)) ? fracIntercept(ctx) : gen.intercept(ctx, { allowZero: false });
      var eq;
      if (form === 'commuted') eq = 'y=' + lin([[b, ''], [m, 'x']]);
      else if (form === 'fn') eq = 'f(x)=' + lin([[m, 'x'], [b, '']]);
      else eq = T.eqSI(m, b);
      gen.need(form !== 'commuted' || !Fr.of(b).isZero());
      var bf = Fr.of(b);
      var steps = [];
      if (form === 'commuted') steps.push('Rewrite in the order ' + M('y=mx+b') + ': ' + M(T.eqSI(m, b)));
      if (form === 'horizontal') steps.push(M(eq) + ' has no ' + M('x') + '-term, so ' + M('m=0') + ' and ' + M('b=' + num(b)) + '.');
      else if (form === 'noB') steps.push('There is no constant term, so ' + M('b=0') + '. The coefficient of ' + M('x') + ' is the slope.');
      else steps.push('Compare with ' + M('y=mx+b') + ': ' + M('m') + ' is the coefficient of ' + M('x') + ' and ' + M('b') + ' is the constant.');
      return {
        prompt: M(eq) + '<div class="blanks">Slope: <span class="ln"></span> &nbsp; y-intercept: <span class="ln"></span></div>',
        keyPrompt: M(eq),
        answer: 'Slope ' + M('m=' + num(m)) + '; y-intercept ' + M('b=' + num(b)) + ' (the point ' + M(pt(0, b)) + ')',
        steps: steps, key: 's14|' + eq, equiv: form + '|' + m
      };
    }
  });

  /* 15 --------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-std-to-slope-intercept', unit: U, category: 'forms', num: 15,
    title: 'Convert standard form to slope-intercept form',
    instruction: 'Rewrite each equation in slope-intercept form, y = mx + b.',
    layout: 'half', space: [0.9, 1.6, 2.2],
    generate: function (ctx) {
      var rng = ctx.rng, A, B, C, m, b;
      if (ctx.numberMode === 'integers') {
        var Bmax = ctx.difficulty === 'basic' ? 3 : ctx.difficulty === 'standard' ? 5 : 6;
        var Bs = Math.abs(rng.chance(0.3) ? 1 : rng.int(1, Bmax));
        m = gen.slope(ctx, { int: true }); b = gen.intercept(ctx, { allowZero: true, max: Math.min(ctx.D.maxB, 9) });
        B = (m.n > 0 ? -1 : 1) * Bs;                  // keep A > 0 (standard form convention)
        A = -m.n * B; C = b * B;
      } else {
        m = gen.slope(ctx);
        b = (ctx.allowFracIntercept && rng.chance(0.4)) ? fracIntercept(ctx) : gen.intercept(ctx, { allowZero: true, max: Math.min(ctx.D.maxB, 9) });
        var st = T.toStandard(m, b); A = st.A; B = st.B; C = st.C;
      }
      gen.need(A > 0 && B !== 0 && Math.abs(A) <= 30 && Math.abs(C) <= 60 && Math.abs(B) <= 12);
      // verify: B*y = -A*x + C  <=>  y = (-A/B) x + C/B
      gen.need(F(-A, B).eq(m) && F(C, B).eq(b));
      var eq = T.eqStd(A, B, C), mT = num(m), steps = [];
      steps.push('Get the ' + M('y') + '-term alone by subtracting ' + M(lin([[A, 'x']])) + ' from both sides: ' + M(lin([[B, 'y']]) + '=' + lin([[-A, 'x'], [C, '']])));
      if (B === -1) steps.push('Multiply both sides by ' + M('-1') + ': ' + M(T.eqSI(m, b)));
      else if (B !== 1) {
        steps.push('Divide every term by ' + M(num(B)) + ': ' + M('y=\\frac{' + lin([[-A, 'x'], [C, '']]) + '}{' + num(B) + '}'));
        steps.push('Simplify: ' + M(T.eqSI(m, b)));
      }
      return { prompt: M(eq), answer: M(T.eqSI(m, b)), steps: steps, key: 's15|' + eq, equiv: m + '|' + b };
    }
  });

  /* 16 --------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-slope-intercept-to-std', unit: U, category: 'forms', num: 16,
    title: 'Convert slope-intercept form to standard form',
    instruction: 'Rewrite each equation in standard form, Ax + By = C, with integer coefficients and A > 0.',
    layout: 'half', space: [0.9, 1.6, 2.2],
    generate: function (ctx) {
      var rng = ctx.rng;
      var m = gen.slope(ctx);
      var b = (ctx.allowFracIntercept && rng.chance(0.45)) ? fracIntercept(ctx) : gen.intercept(ctx, { allowZero: false, max: Math.min(ctx.D.maxB, 9) });
      b = Fr.of(b);
      var L = NS.frac.lcm(m.d, b.d), st = T.toStandard(m, b);
      gen.need(st.A > 0 && Math.abs(st.A) <= 30 && Math.abs(st.B) <= 20 && Math.abs(st.C) <= 80);
      // verify by plugging lattice-free check: A m' ... A*x + B*y = C must hold for y = m x + b at x = 0 and x = 1
      gen.need(F(st.C).eq(F(st.B).mul(b)) && F(st.A).add(F(st.B).mul(m)).eq(0));
      var eq = T.eqSI(m, b), steps = [], Lm = m.mul(L), Lb = b.mul(L);
      var cur = eq;
      if (L > 1) steps.push('Multiply every term by ' + M(String(L)) + ' to clear the fractions: ' + M(lin([[L, 'y']]) + '=' + lin([[Lm, 'x'], [Lb, '']])));
      steps.push('Move the ' + M('x') + '-term to the left side: ' + M(lin([[Lm.neg(), 'x'], [L, 'y']]) + '=' + num(Lb)));
      if (Lm.neg().sign() < 0) steps.push('Multiply both sides by ' + M('-1') + ' so that ' + M('A') + ' is positive: ' + M(T.eqStd(st.A, st.B, st.C)));
      return { prompt: M(eq), answer: M(T.eqStd(st.A, st.B, st.C)), steps: steps, key: 's16|' + eq, equiv: m + '|' + b };
    }
  });

  /* 17 --------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-write-point-slope', unit: U, category: 'forms', num: 17,
    title: 'Write equations in point-slope form',
    instruction: 'Write the equation of each line in point-slope form, y − y₁ = m(x − x₁).',
    layout: 'half', space: [0.7, 1.2, 1.8],
    generate: function (ctx) {
      var rng = ctx.rng, lim = Math.min(ctx.D.lim, 9);
      var type = ['sp', 'tp', 'sp'][(ctx.slot + ctx.stable) % 3];
      function nz() { return rng.nonzero(-lim, lim); }
      if (type === 'sp') {
        var m = gen.slope(ctx), x1 = nz(), y1 = nz();
        return {
          prompt: 'Slope ' + M('m=' + num(m)) + ', point ' + M(pt(x1, y1)),
          answer: M(T.eqPS(m, x1, y1)),
          steps: ['Use ' + M('y-y_1=m(x-x_1)') + ' with ' + M('m=' + num(m)) + ' and ' + M('(x_1,\\,y_1)=' + pt(x1, y1)) + '.',
            'Substitute: ' + M(T.eqPS(m, x1, y1))],
          key: 's17|' + m + '|' + x1 + ',' + y1, equiv: 'sp|' + m
        };
      }
      var mm = gen.slope(ctx), d = mm.d, k = rng.pick([1, 2, 3]) * rng.sign();
      var xa = nz(), ya = nz(), xb = xa + d * k, yb = ya + mm.n * k;
      gen.need(Math.abs(xb) <= lim && Math.abs(yb) <= lim && xb !== 0 && yb !== 0);
      var A = [xa, ya], B = [xb, yb], P = rng.chance(0.5) ? A : B, Q = P === A ? B : A;
      gen.need(Fr.of(Q[1] - P[1]).div(Q[0] - P[0]).eq(mm));
      return {
        prompt: 'Line through ' + M(pt(P[0], P[1])) + ' and ' + M(pt(Q[0], Q[1])),
        answer: M(T.eqPS(mm, P[0], P[1])) + '<br><span class="note">Using the other point is also correct: </span>' + M(T.eqPS(mm, Q[0], Q[1])),
        steps: LF.slopeSteps(P, Q).concat(['Use the point ' + M(pt(P[0], P[1])) + ' in ' + M('y-y_1=m(x-x_1)') + ': ' + M(T.eqPS(mm, P[0], P[1]))]),
        key: 's17t|' + LF.pairKey([A, B]), equiv: 'tp|' + mm
      };
    }
  });

  /* 18 --------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-point-slope-to-slope-intercept', unit: U, category: 'forms', num: 18,
    title: 'Convert point-slope form to slope-intercept form',
    instruction: 'Rewrite each equation in slope-intercept form, y = mx + b.',
    layout: 'half', space: [0.8, 1.4, 2.0],
    generate: function (ctx) {
      var rng = ctx.rng, lim = Math.min(ctx.D.lim, 9);
      var m = gen.slope(ctx), d = m.d;
      var x1 = ctx.allowFracIntercept ? rng.nonzero(-lim, lim) : d * rng.nonzero(-Math.floor(lim / d), Math.floor(lim / d));
      var y1 = rng.nonzero(-lim, lim);
      gen.need(x1 !== 0);
      var b = Fr.of(y1).sub(m.mul(x1));
      gen.need(Math.abs(b.val()) <= 25 && b.d <= 6 && (ctx.allowFracIntercept || b.isInt()));
      gen.need(m.mul(x1).add(b).eq(y1));                                       // the given point lies on the answer
      var eq = T.eqPS(m, x1, y1);
      var distributed = lin([[1, 'y'], [-y1, '']]) + '=' + lin([[m, 'x'], [m.mul(x1).neg(), '']]);
      var addY = 'y=' + lin([[m, 'x'], [m.mul(x1).neg(), '']]) + (y1 > 0 ? '+' : '-') + Math.abs(y1);
      var steps = ['Distribute ' + (m.eq(1) ? '' : M(num(m)) + ' ') + 'across the parentheses: ' + M(distributed),
        (y1 > 0 ? 'Add ' : 'Subtract ') + M(String(Math.abs(y1))) + ' ' + (y1 > 0 ? 'to' : 'from') + ' both sides: ' + M(addY),
        'Combine the constants: ' + M(T.eqSI(m, b))];
      return { prompt: M(eq), answer: M(T.eqSI(m, b)), steps: steps, key: 's18|' + eq, equiv: m + '|' + b };
    }
  });
})(typeof window !== 'undefined' ? window : globalThis);
