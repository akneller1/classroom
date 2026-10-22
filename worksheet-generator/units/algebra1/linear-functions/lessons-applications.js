/* Category E — Applications (sub-lessons 19-21).
   All word-problem numbers are whole numbers so that every answer is exact and realistic. */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr, F = NS.frac.F, T = NS.tex, gen = NS.gen, LF = NS.lf;
  var M = T.M, num = T.num, numP = T.numP, pt = T.pt, lin = T.lin;
  var U = LF.UNIT;
  function $(n) { return '$' + n; }

  /* Context library.  dir: 'inc' (y = mx + b, b > 0) or 'dec' (y = -mx + b).
     ranges: m = rate (positive size), b = starting amount (multiples of `step`), x = input values. */
  var CONTEXTS = [
    { id: 'taxi', dir: 'inc', ys: 'C', xs: 'd', m: [2, 6], b: [3, 12, 1], x: [3, 15],
      yPhrase: 'the total cost, in dollars, of a taxi ride', xPhrase: 'the number of miles driven',
      scen: function (m, b) { return 'A taxi company charges a flat fee of ' + $(b) + ' plus ' + $(m) + ' for each mile driven.'; },
      at: function (x, y) { return 'A ' + x + '-mile ride costs ' + $(y) + '.'; },
      slopeMean: function (m) { return 'The cost increases by ' + $(m) + ' for each additional mile (the cost per mile).'; },
      interceptMean: function (b) { return 'The flat fee is ' + $(b) + ': the cost of a ride of 0 miles.'; },
      evalQ: function (x) { return 'How much does a ' + x + '-mile ride cost?'; }, evalA: function (y) { return $(y); },
      solveQ: function (y) { return 'A ride costs ' + $(y) + '. How many miles was the ride?'; }, solveA: function (x) { return x + ' miles'; } },
    { id: 'gym', dir: 'inc', ys: 'C', xs: 'n', m: [15, 45, 5], b: [20, 100, 5], x: [2, 12],
      yPhrase: 'the total cost, in dollars, of a gym membership', xPhrase: 'the number of months',
      scen: function (m, b) { return 'A gym charges a one-time sign-up fee of ' + $(b) + ' plus ' + $(m) + ' per month.'; },
      at: function (x, y) { return 'After ' + x + ' months, the total cost is ' + $(y) + '.'; },
      slopeMean: function (m) { return 'The total cost increases by ' + $(m) + ' each month (the monthly fee).'; },
      interceptMean: function (b) { return 'The sign-up fee is ' + $(b) + ': the cost at 0 months.'; },
      evalQ: function (x) { return 'What is the total cost after ' + x + ' months?'; }, evalA: function (y) { return $(y); },
      solveQ: function (y) { return 'The total cost is ' + $(y) + '. For how many months has the person belonged?'; }, solveA: function (x) { return x + ' months'; } },
    { id: 'savings', dir: 'inc', ys: 'S', xs: 'w', m: [5, 25, 5], b: [20, 150, 10], x: [2, 14],
      yPhrase: 'the amount of money saved, in dollars', xPhrase: 'the number of weeks',
      scen: function (m, b) { return 'Jordan has ' + $(b) + ' saved and adds ' + $(m) + ' each week.'; },
      at: function (x, y) { return 'After ' + x + ' weeks, Jordan has saved ' + $(y) + '.'; },
      slopeMean: function (m) { return 'Jordan’s savings grow by ' + $(m) + ' each week.'; },
      interceptMean: function (b) { return 'Jordan starts with ' + $(b) + ': the amount saved at week 0.'; },
      evalQ: function (x) { return 'How much will Jordan have after ' + x + ' weeks?'; }, evalA: function (y) { return $(y); },
      solveQ: function (y) { return 'After how many weeks will Jordan have ' + $(y) + '?'; }, solveA: function (x) { return x + ' weeks'; } },
    { id: 'handyman', dir: 'inc', ys: 'C', xs: 'h', m: [20, 60, 5], b: [25, 80, 5], x: [2, 10],
      yPhrase: 'the total charge, in dollars, for a repair visit', xPhrase: 'the number of hours worked',
      scen: function (m, b) { return 'A repair technician charges ' + $(b) + ' to come to the house plus ' + $(m) + ' for each hour of work.'; },
      at: function (x, y) { return 'A ' + x + '-hour job costs ' + $(y) + '.'; },
      slopeMean: function (m) { return 'The charge increases by ' + $(m) + ' for each hour of work (the hourly rate).'; },
      interceptMean: function (b) { return 'The charge for coming to the house is ' + $(b) + ': the cost for 0 hours of work.'; },
      evalQ: function (x) { return 'How much does a ' + x + '-hour job cost?'; }, evalA: function (y) { return $(y); },
      solveQ: function (y) { return 'A job costs ' + $(y) + '. How many hours did it take?'; }, solveA: function (x) { return x + ' hours'; } },
    { id: 'plant', dir: 'inc', ys: 'H', xs: 'w', m: [2, 6], b: [5, 20, 1], x: [2, 10],
      yPhrase: 'the height, in centimeters, of a plant', xPhrase: 'the number of weeks since it was measured',
      scen: function (m, b) { return 'A plant is ' + b + ' centimeters tall and grows ' + m + ' centimeters each week.'; },
      at: function (x, y) { return 'After ' + x + ' weeks, the plant is ' + y + ' centimeters tall.'; },
      slopeMean: function (m) { return 'The plant grows ' + m + ' centimeters each week.'; },
      interceptMean: function (b) { return 'The plant is ' + b + ' centimeters tall at the start (week 0).'; },
      evalQ: function (x) { return 'How tall is the plant after ' + x + ' weeks?'; }, evalA: function (y) { return y + ' cm'; },
      solveQ: function (y) { return 'After how many weeks will the plant be ' + y + ' centimeters tall?'; }, solveA: function (x) { return x + ' weeks'; } },
    { id: 'pool', dir: 'inc', ys: 'V', xs: 't', m: [10, 40, 5], b: [50, 300, 10], x: [3, 12],
      yPhrase: 'the amount of water, in gallons, in a pool', xPhrase: 'the number of minutes since the hose was turned on',
      scen: function (m, b) { return 'A pool holds ' + b + ' gallons of water. A hose adds ' + m + ' gallons each minute.'; },
      at: function (x, y) { return 'After ' + x + ' minutes, the pool holds ' + y + ' gallons.'; },
      slopeMean: function (m) { return 'The amount of water increases by ' + m + ' gallons each minute.'; },
      interceptMean: function (b) { return 'The pool holds ' + b + ' gallons when the hose is first turned on (0 minutes).'; },
      evalQ: function (x) { return 'How much water is in the pool after ' + x + ' minutes?'; }, evalA: function (y) { return y + ' gallons'; },
      solveQ: function (y) { return 'After how many minutes will the pool hold ' + y + ' gallons?'; }, solveA: function (x) { return x + ' minutes'; } },
    { id: 'candle', dir: 'dec', ys: 'H', xs: 't', m: [1, 3], b: [12, 30, 2], x: [2, 8],
      yPhrase: 'the height, in centimeters, of a candle', xPhrase: 'the number of hours it has burned',
      scen: function (m, b) { return 'A new candle is ' + b + ' centimeters tall. It burns down ' + m + ' centimeter' + (m === 1 ? '' : 's') + ' each hour.'; },
      at: function (x, y) { return 'After ' + x + ' hours, the candle is ' + y + ' centimeters tall.'; },
      slopeMean: function (m) { return 'The candle gets ' + m + ' centimeter' + (m === 1 ? '' : 's') + ' shorter each hour. The slope is negative because the height decreases.'; },
      interceptMean: function (b) { return 'The candle is ' + b + ' centimeters tall before it is lit (0 hours).'; },
      evalQ: function (x) { return 'How tall is the candle after ' + x + ' hours?'; }, evalA: function (y) { return y + ' cm'; },
      solveQ: function (y) { return 'After how many hours is the candle ' + y + ' centimeters tall?'; }, solveA: function (x) { return x + ' hours'; } },
    { id: 'tank', dir: 'dec', ys: 'W', xs: 't', m: [4, 12], b: [60, 200, 10], x: [2, 10],
      yPhrase: 'the amount of water, in gallons, left in a tank', xPhrase: 'the number of minutes since draining began',
      scen: function (m, b) { return 'A tank holds ' + b + ' gallons of water. It is drained at a rate of ' + m + ' gallons per minute.'; },
      at: function (x, y) { return 'After ' + x + ' minutes, ' + y + ' gallons are left.'; },
      slopeMean: function (m) { return 'The amount of water decreases by ' + m + ' gallons each minute. The slope is negative because the amount is decreasing.'; },
      interceptMean: function (b) { return 'The tank holds ' + b + ' gallons when draining starts (0 minutes).'; },
      evalQ: function (x) { return 'How much water is left after ' + x + ' minutes?'; }, evalA: function (y) { return y + ' gallons'; },
      solveQ: function (y) { return 'After how many minutes will ' + y + ' gallons be left?'; }, solveA: function (x) { return x + ' minutes'; } },
    { id: 'battery', dir: 'dec', ys: 'P', xs: 'h', m: [4, 12], b: [100, 100, 1], x: [2, 8],
      yPhrase: 'the battery charge, in percent, of a tablet', xPhrase: 'the number of hours it has been in use',
      scen: function (m, b) { return 'A tablet starts at ' + b + '% battery. The battery drops ' + m + ' percentage points each hour of use.'; },
      at: function (x, y) { return 'After ' + x + ' hours of use, the battery is at ' + y + '%.'; },
      slopeMean: function (m) { return 'The battery charge drops ' + m + ' percentage points each hour. The slope is negative because the charge decreases.'; },
      interceptMean: function (b) { return 'The battery starts at ' + b + '% (0 hours of use).'; },
      evalQ: function (x) { return 'What is the battery charge after ' + x + ' hours of use?'; }, evalA: function (y) { return y + '%'; },
      solveQ: function (y) { return 'After how many hours of use is the battery at ' + y + '%?'; }, solveA: function (x) { return x + ' hours'; } }
  ];

  /* Draw a believable (m, b, xs) for a context at the chosen difficulty. */
  function drawContext(ctx, c) {
    var rng = ctx.rng, diff = ctx.difficulty;
    function r(rg) {
      var lo = rg[0], hi = rg[1], st = rg[2] || 1;
      if (diff === 'basic' && hi > lo) hi = Math.min(hi, lo + Math.max(st, Math.floor((hi - lo) / 2 / st) * st));   // basic: lower half of the range
      var steps = Math.floor((hi - lo) / st);
      return lo + st * rng.int(0, steps);
    }
    var m = r(c.m), b = r(c.b);
    var xHi = diff === 'basic' ? Math.min(c.x[1], c.x[0] + Math.ceil((c.x[1] - c.x[0]) / 2)) : c.x[1];   // basic: smaller inputs
    var x1 = rng.int(c.x[0], xHi);
    return { m: m, b: b, slope: c.dir === 'dec' ? -m : m, x1: x1, xHi: xHi };
  }
  function eqText(c, slope, b) { return c.ys + '=' + lin([[slope, c.xs], [b, '']]); }
  function pickCtx(ctx, dirWanted) {
    var list = CONTEXTS.filter(function (c) { return !dirWanted || c.dir === dirWanted; });
    var i = (ctx.slot + ctx.stable + ctx.rng.int(0, 1000)) % list.length;
    return list[ctx.rng.int(0, list.length - 1)];
  }

  /* 19 --------------------------------------------------------------- */
  NS.registerLesson({
    id: 'lf-interpret-slope-intercept', unit: U, category: 'applications', num: 19,
    title: 'Interpret slope and intercepts in context',
    instruction: 'Each equation models a real situation. Identify the slope and y-intercept and explain what each means in context.',
    layout: 'full', space: [0.55, 0.9, 1.4],
    generate: function (ctx) {
      var rng = ctx.rng;
      var dirWanted = (ctx.slot + ctx.stable) % 3 === 2 ? 'dec' : null;      // about a third decreasing
      var c = pickCtx(ctx, dirWanted), v = drawContext(ctx, c);
      var eq = eqText(c, v.slope, v.b);
      gen.need(Fr.of(v.slope).mul(0).add(v.b).eq(v.b));                       // y-intercept really is b
      gen.need(ctx.difficulty !== 'basic' || v.b <= 150);
      var q = 'The equation ' + M(eq) + ' gives ' + c.yPhrase + ', where ' + M(c.xs) + ' is ' + c.xPhrase + '.' +
        '<div class="parts"><div><b>(a)</b> What is the slope? What does it mean in this situation?</div>' +
        '<div><b>(b)</b> What is the y-intercept? What does it mean in this situation?</div></div>';
      return {
        prompt: q,
        answer: '<b>(a)</b> ' + M('m=' + num(v.slope)) + '. ' + c.slopeMean(v.m) + '<br><b>(b)</b> ' + M('b=' + num(v.b)) + '. ' + c.interceptMean(v.b),
        steps: ['The equation is in the form ' + M('y=mx+b') + ', so ' + M('m=' + num(v.slope)) + ' and ' + M('b=' + num(v.b)) + '.',
          'The slope is the rate of change: how much ' + M(c.ys) + ' changes for each 1 unit increase in ' + M(c.xs) + '.',
          'The y-intercept is the value of ' + M(c.ys) + ' when ' + M(c.xs + '=0') + ': the starting amount.'],
        key: 's19|' + c.id + '|' + v.m + '|' + v.b, equiv: c.id
      };
    }
  });

  /* 20 --------------------------------------------------------------- */
  var WP_TYPES = ['forward', 'twopoints', 'forward', 'twopoints'];
  NS.registerLesson({
    id: 'lf-word-problems', unit: U, category: 'applications', num: 20,
    title: 'Solve linear word problems',
    instruction: 'Read each situation. Write a linear equation and use it to answer the questions. Show your work.',
    layout: 'full', space: [0.9, 1.4, 2.0],
    generate: function (ctx) {
      var rng = ctx.rng, diff = ctx.difficulty, type = WP_TYPES[(ctx.slot + ctx.stable) % WP_TYPES.length];
      var dirWanted = (ctx.slot + ctx.stable) % 3 === 1 ? 'dec' : null;
      var c = pickCtx(ctx, dirWanted), v = drawContext(ctx, c), s = v.slope, b = v.b;
      var eq = eqText(c, s, b), steps, answer, q;
      function yAt(x) { return s * x + b; }
      // choose x values so that every y is a positive whole number
      var xmax = c.dir === 'dec' ? Math.floor((b - 1) / v.m) : v.xHi;
      var xlo = c.x[0], xtop = Math.min(xmax, v.xHi);
      gen.need(xtop >= xlo + 2);
      var xA = rng.int(xlo, xtop), xB;
      do { xB = rng.int(xlo, xtop); } while (xB === xA);
      var cap = diff === 'basic' ? 150 : 100000;                          // keep Basic numbers friendly
      if (type === 'forward') {
        var yB = yAt(xB);
        gen.need(yB > 0 && yAt(xA) > 0 && yB <= cap && yAt(xA) <= cap);
        q = c.scen(v.m, b) + '<div class="parts"><div><b>(a)</b> Write an equation for ' + M(c.ys) + ' in terms of ' + M(c.xs) + ', where ' + M(c.xs) + ' is ' + c.xPhrase + '.</div>' +
          '<div><b>(b)</b> ' + c.evalQ(xA) + '</div><div><b>(c)</b> ' + c.solveQ(yB) + '</div></div>';
        answer = '<b>(a)</b> ' + M(eq) + '<br><b>(b)</b> ' + c.evalA(yAt(xA)) + '<br><b>(c)</b> ' + c.solveA(xB);
        steps = ['Starting amount ' + M('b=' + num(b)) + ' and rate of change ' + M('m=' + num(s)) + ' give ' + M(eq) + '.',
          'Substitute ' + M(c.xs + '=' + xA) + ': ' + M(c.ys + '=' + num(s) + '(' + xA + ')' + (b >= 0 ? '+' : '-') + Math.abs(b) + '=' + yAt(xA)) + '.',
          'Set ' + M(c.ys + '=' + yB) + ': ' + M(yB + '=' + lin([[s, c.xs], [b, '']])) + '.',
          'Subtract ' + M(String(b)) + ': ' + M(num(yB - b) + '=' + num(s) + c.xs) + '. Divide by ' + M(num(s)) + ': ' + M(c.xs + '=' + xB) + '.'];
        // independent verification
        gen.need(yAt(xB) === yB && s * xB + b === yB);
      } else {
        var x1 = Math.min(xA, xB), x2 = Math.max(xA, xB), y1 = yAt(x1), y2 = yAt(x2);
        var x3 = x2 + rng.int(1, diff === 'basic' ? 2 : 4);
        if (c.dir === 'dec') gen.need(yAt(x3) > 0 && y1 > 0 && y2 > 0); else gen.need(y1 > 0 && y2 > 0);
        gen.need(Math.max(y1, y2, yAt(x3)) <= cap);
        gen.need((y2 - y1) / (x2 - x1) === s && Number.isInteger(s));
        q = c.at(x1, y1) + ' ' + c.at(x2, y2) + ' Assume the relationship is linear, with ' + M(c.xs) + ' = ' + c.xPhrase + '.' +
          '<div class="parts"><div><b>(a)</b> Find the rate of change (slope).</div><div><b>(b)</b> Write an equation for ' + M(c.ys) + ' in terms of ' + M(c.xs) + '.</div>' +
          '<div><b>(c)</b> Use your equation to find ' + M(c.ys) + ' when ' + M(c.xs + '=' + x3) + '.</div></div>';
        answer = '<b>(a)</b> ' + M('m=' + num(s)) + '<br><b>(b)</b> ' + M(eq) + '<br><b>(c)</b> ' + M(c.ys + '=' + yAt(x3));
        steps = LF.slopeSteps([x1, y1], [x2, y2]).concat(LF.findBSteps(F(s), x1, y1).steps)
          .concat(['Substitute ' + M(c.xs + '=' + x3) + ': ' + M(c.ys + '=' + num(s) + '(' + x3 + ')' + (b >= 0 ? '+' : '-') + Math.abs(b) + '=' + yAt(x3))]);
      }
      return { prompt: q, answer: answer, steps: steps, key: 's20|' + type + '|' + c.id + '|' + v.m + '|' + b + '|' + xA + '|' + xB, equiv: type + '|' + c.id };
    }
  });

  /* 21 --------------------------------------------------------------- */
  var KINDS = [['eq', 'table'], ['graph', 'eq'], ['table', 'graph'], ['eq', 'graph'], ['table', 'eq'], ['graph', 'table']];
  NS.registerLesson({
    id: 'lf-compare-functions', unit: U, category: 'applications', num: 21,
    title: 'Compare linear functions (equations, graphs, tables)',
    instruction: 'Two linear functions are shown in different forms. Compare them.',
    layout: 'full', figWidth: 2.2, space: [0.3, 0.6, 1.0],
    generate: function (ctx) {
      var rng = ctx.rng, diff = ctx.difficulty;
      var kinds = KINDS[(ctx.slot + ctx.stable) % KINDS.length];
      var L = [0, 1].map(function () {
        var m = gen.slope(ctx), b = gen.intercept(ctx, { max: 6, allowZero: false });
        return { m: m, b: b };
      });
      gen.need(!L[0].m.eq(L[1].m) && L[0].b !== L[1].b);
      var figs = [], names = ['A', 'B'];
      var needFig = function (k) { return k === 'graph'; };
      function rep(i) {
        var l = L[i], kind = kinds[i], d = l.m.d;
        if (kind === 'eq') return { html: M('y=' + lin([[l.m, 'x'], [l.b, '']]).replace(/^$/, '0')), data: null };
        if (kind === 'table') {
          var base = diff === 'honors' && rng.chance(0.6) ? 1 : 0;           // honors tables may skip x = 0
          var xs = [0, 1, 2, 3].map(function (k) { return (k + base) * d * (rng.chance(0) ? 1 : 1); });
          var ys = xs.map(function (x) { return l.m.mul(x).add(l.b); });
          gen.need(ys.every(function (y) { return y.isInt() && Math.abs(y.n) <= 40; }));
          return { html: '<div class="tbl">' + NS.table([{ label: 'x', cells: xs }, { label: 'y', cells: ys }]) + '</div>', xs: xs, ys: ys };
        }
        var k = rng.pick([1, 2, 3]) * (l.m.n > 0 ? 1 : 1), x2 = d * k, y2 = Fr.of(l.b).add(l.m.n * k);
        if (Math.abs(x2) > 7 || Math.abs(y2.n) > 7) { x2 = -d * k; y2 = Fr.of(l.b).sub(l.m.n * k); }
        gen.need(Math.abs(x2) <= 7 && Math.abs(y2.n) <= 7 && gen.latticeCount(l.m, l.b, 8) >= 2);
        gen.need(Math.abs(l.b) <= 7);
        figs.push(LF.spec(LF.W8, [LF.line(l.m, l.b)], [{ x: 0, y: l.b }, { x: x2, y: y2.n }]));
        return { html: '[[fig:' + (figs.length - 1) + ']]', graph: true };
      }
      var R = [rep(0), rep(1)];
      var panels = '<div class="panels">' + R.map(function (r, i) { return '<div class="panel"><div class="ph">Function ' + names[i] + '</div>' + r.html + '</div>'; }).join('') + '</div>';
      var parts = '<div class="parts"><div><b>(a)</b> Which function has the greater slope? Slope of A: <span class="ln"></span> &nbsp; Slope of B: <span class="ln"></span></div>' +
        '<div><b>(b)</b> Which function has the greater y-intercept? y-int of A: <span class="ln"></span> &nbsp; y-int of B: <span class="ln"></span></div>';
      var x0 = null;
      if (diff === 'honors') {
        do { x0 = rng.int(2, 6); } while (L[0].m.mul(x0).add(L[0].b).eq(L[1].m.mul(x0).add(L[1].b)));
        parts += '<div><b>(c)</b> Which function has the greater value when ' + M('x=' + x0) + '?</div>';
      }
      parts += '</div>';
      var gm = L[0].m.gt(L[1].m) ? 'A' : 'B', gb = L[0].b > L[1].b ? 'A' : 'B';
      var ans = '<b>(a)</b> Function ' + gm + ' (' + M('m_A=' + num(L[0].m) + ',\\ m_B=' + num(L[1].m)) + ')<br><b>(b)</b> Function ' + gb + ' (' + M('b_A=' + num(L[0].b) + ',\\ b_B=' + num(L[1].b)) + ')';
      var steps = ['Function A: ' + M('m=' + num(L[0].m) + ',\\ b=' + num(L[0].b)) + '. Function B: ' + M('m=' + num(L[1].m) + ',\\ b=' + num(L[1].b)) + '.'];
      kinds.forEach(function (k, i) {
        if (k === 'table') steps.push('Function ' + names[i] + ' (table): the slope is the change in ' + M('y') + ' divided by the change in ' + M('x') + ' between two columns; the y-intercept is the value at ' + M('x=0') + (R[i].xs && R[i].xs[0] !== 0 ? ' (found by continuing the pattern backward)' : '') + '.');
        if (k === 'graph') steps.push('Function ' + names[i] + ' (graph): read the y-intercept where the line crosses the y-axis and use rise over run for the slope.');
      });
      if (x0 !== null) {
        var vA = L[0].m.mul(x0).add(L[0].b), vB = L[1].m.mul(x0).add(L[1].b);
        gen.need(!vA.eq(vB));
        ans += '<br><b>(c)</b> Function ' + (vA.gt(vB) ? 'A' : 'B') + ' (' + M('y_A=' + num(vA) + ',\\ y_B=' + num(vB)) + ')';
        steps.push('At ' + M('x=' + x0) + ': ' + M('y_A=' + num(vA)) + ' and ' + M('y_B=' + num(vB)) + '.');
      }
      return {
        prompt: panels + parts, figs: figs, answer: ans, steps: steps,
        key: 's21|' + kinds.join('') + '|' + L.map(function (l) { return l.m + ',' + l.b; }).join('|'), equiv: kinds.join('') + '|' + gm + gb
      };
    }
  });
})(typeof window !== 'undefined' ? window : globalThis);
