/* Matching kinds for number sense and algebra (grades 6–8, Algebra 1, Precalculus):
     ineq  Inequalities: inequality ↔ number line ↔ words (↔ interval notation in Precalculus)
     prop  Proportional relationships: situation ↔ equation y = kx ↔ table ↔ graph
     fdp   Fractions, decimals and percents: fraction ↔ decimal ↔ percent ↔ model (hundred grid or fraction strip)
     sys   Systems of linear equations: graph ↔ slope-intercept form ↔ standard form ↔ solution
   Every set is generated from its answer (the solution set, the constant of proportionality, the value, the
   solution point) and every printed card is checked against that answer by evaluating what it shows.
   Needs: menu/match-kinds.js. */
(function (G) {
  'use strict';
  var MK = G.MKMATCH, U = MK.util, SV = MK.svg;
  var tx = U.tex, k = U.k, kd = U.kd, esc = U.esc;
  function signed(v, first) { var a = Math.abs(v), s = U.tex(a); return first ? (v < 0 ? '-' : '') + s : (v < 0 ? ' - ' : ' + ') + s; }
  /* a·x + b as TeX (a may be a fraction) */
  function lin(a, b, v) {
    v = v || 'x'; var out = '';
    if (!U.near(a, 0)) { var aa = Math.abs(a); out = (a < 0 ? '-' : '') + (U.near(aa, 1) ? '' : U.tex(aa)) + v; }
    if (!U.near(b, 0) || !out) out += out ? signed(b) : U.tex(b);
    return out;
  }

  /* ======================= INEQUALITIES ======================= */
  var OPS = { lt: '<', gt: '>', le: '\\le', ge: '\\ge' }, FLIP = { lt: 'gt', gt: 'lt', le: 'ge', ge: 'le' };
  function test(op, l, r) { return op === 'lt' ? l < r - 1e-9 : op === 'gt' ? l > r + 1e-9 : op === 'le' ? l <= r + 1e-9 : l >= r - 1e-9; }
  function inSet(parts, x) { return parts.some(function (p) { return (x > p.lo || (p.loC && U.near(x, p.lo))) && (x < p.hi || (p.hiC && U.near(x, p.hi))); }); }
  function solKey(parts) { return parts.map(function (p) { return (p.loC ? '[' : '(') + p.lo + ',' + p.hi + (p.hiC ? ']' : ')'); }).join('u'); }
  function ray(op, b) { return op === 'lt' ? { lo: -Infinity, hi: b, hiC: false } : op === 'le' ? { lo: -Infinity, hi: b, hiC: true } : op === 'gt' ? { lo: b, loC: false, hi: Infinity } : { lo: b, loC: true, hi: Infinity }; }
  function intervalTex(parts) {
    return parts.map(function (p) { return (isFinite(p.lo) ? (p.loC ? '[' : '(') + U.tex(p.lo) : '(-\\infty') + ',\\ ' + (isFinite(p.hi) ? U.tex(p.hi) + (p.hiC ? ']' : ')') : '\\infty)'); }).join(' \\cup ');
  }
  var W = {
    gt: [['greater than'], ['greater than', 'more than']], ge: [['greater than or equal to'], ['greater than or equal to', 'at least', 'no less than']],
    lt: [['less than'], ['less than']], le: [['less than or equal to'], ['less than or equal to', 'at most', 'no more than', 'no greater than']]
  };
  function wordFor(op, b, rng, L) { var list = W[op][L === 'cp2' ? 0 : 1]; return rng.pick(list) + ' ' + U.m(U.tex(b)); }
  function wordsOf(parts, rng, L) {
    if (parts.length === 2) return 'All numbers ' + wordFor(parts[0].hiC ? 'le' : 'lt', parts[0].hi, rng, L) + ' or ' + wordFor(parts[1].loC ? 'ge' : 'gt', parts[1].lo, rng, L);
    var p = parts[0];
    if (!isFinite(p.lo)) return 'All numbers ' + wordFor(p.hiC ? 'le' : 'lt', p.hi, rng, L);
    if (!isFinite(p.hi)) return 'All numbers ' + wordFor(p.loC ? 'ge' : 'gt', p.lo, rng, L);
    if (rng.next() < 0.5) return 'All numbers ' + wordFor(p.loC ? 'ge' : 'gt', p.lo, rng, L) + ' and ' + wordFor(p.hiC ? 'le' : 'lt', p.hi, rng, L);
    var inc = p.loC && p.hiC ? ', including both' : p.loC ? ', including ' + U.m(U.tex(p.lo)) + ' but not ' + U.m(U.tex(p.hi)) : p.hiC ? ', including ' + U.m(U.tex(p.hi)) + ' but not ' + U.m(U.tex(p.lo)) : ', not including either one';
    return 'All numbers between ' + U.m(U.tex(p.lo)) + ' and ' + U.m(U.tex(p.hi)) + inc;
  }
  /* each family returns { tex, f(x) → is x a solution of the printed inequality, parts } */
  var IFAM = {
    simple: function (rng, L, b) {
      var op = rng.pick(['lt', 'gt', 'le', 'ge']);
      if (L === 'honors' && rng.next() < 0.4) return { tex: U.tex(b) + ' ' + OPS[FLIP[op]] + ' x', f: function (x) { return test(FLIP[op], b, x); }, parts: [ray(op, b)] };
      return { tex: 'x ' + OPS[op] + ' ' + U.tex(b), f: function (x) { return test(op, x, b); }, parts: [ray(op, b)] };
    },
    one: function (rng, L, b) {
      var op = rng.pick(['lt', 'gt', 'le', 'ge']), kind = U.wpick(rng, L === 'cp2' ? { add: 3, sub: 2, mul: 1 } : { add: 2, sub: 2, mul: 3, div: 2 });
      var neg = L === 'honors' && rng.next() < 0.6;
      if (kind === 'add' || kind === 'sub') { var a = rng.int(1, 9) * (kind === 'sub' ? -1 : 1), c = b + a; return { tex: lin(1, a) + ' ' + OPS[op] + ' ' + U.tex(c), f: function (x) { return test(op, x + a, c); }, parts: [ray(op, b)] }; }
      if (kind === 'mul') { var m = rng.int(2, 6) * (neg ? -1 : 1), op2 = m < 0 ? FLIP[op] : op, rhs = m * b; return { tex: lin(m, 0) + ' ' + OPS[op2] + ' ' + U.tex(rhs), f: function (x) { return test(op2, m * x, rhs); }, parts: [ray(op, b)] }; }
      var d = rng.int(2, 5) * (neg ? -1 : 1); if (!U.isInt(b / d)) return null;
      var op3 = d < 0 ? FLIP[op] : op, q = b / d;
      return { tex: '\\frac{x}{' + d + '} ' + OPS[op3] + ' ' + U.tex(q), f: function (x) { return test(op3, x / d, q); }, parts: [ray(op, b)] };
    },
    two: function (rng, L, b) {
      var op = rng.pick(['lt', 'gt', 'le', 'ge']), m = rng.int(2, 5) * (L !== 'cp2' && rng.next() < 0.5 ? -1 : 1), c = rng.int(-9, 9) || 4;
      var op2 = m < 0 ? FLIP[op] : op, rhs = m * b + c;
      if (L === 'honors' && rng.next() < 0.35) return { tex: U.tex(rhs) + ' ' + OPS[FLIP[op2]] + ' ' + lin(m, c), f: function (x) { return test(FLIP[op2], rhs, m * x + c); }, parts: [ray(op, b)] };
      if (rng.next() < 0.3) return { tex: U.tex(c) + (m < 0 ? ' - ' : ' + ') + (Math.abs(m) === 1 ? '' : Math.abs(m)) + 'x ' + OPS[op2] + ' ' + U.tex(rhs), f: function (x) { return test(op2, c + m * x, rhs); }, parts: [ray(op, b)] };
      return { tex: lin(m, c) + ' ' + OPS[op2] + ' ' + U.tex(rhs), f: function (x) { return test(op2, m * x + c, rhs); }, parts: [ray(op, b)] };
    },
    multi: function (rng, L, b) {
      var op = rng.pick(['lt', 'gt', 'le', 'ge']);
      if (rng.next() < 0.4) {   // a(x + p) op rhs
        var a = rng.int(2, 4) * (L === 'honors' && rng.next() < 0.5 ? -1 : 1), p = rng.int(-6, 6) || 2, op2 = a < 0 ? FLIP[op] : op, rhs = a * (b + p);
        return { tex: U.tex(a) + '(' + lin(1, p) + ') ' + OPS[op2] + ' ' + U.tex(rhs), f: function (x) { return test(op2, a * (x + p), rhs); }, parts: [ray(op, b)] };
      }
      var a1 = rng.int(-5, 6), a2 = rng.int(-5, 6); if (a1 === a2 || !a1) return null;
      var c1 = rng.int(-9, 9), c2 = (a1 - a2) * b + c1, op3 = a1 - a2 < 0 ? FLIP[op] : op;
      if (Math.abs(c2) > 30) return null;
      return { tex: lin(a1, c1) + ' ' + OPS[op3] + ' ' + lin(a2, c2), f: function (x) { return test(op3, a1 * x + c1, a2 * x + c2); }, parts: [ray(op, b)] };
    },
    compound: function (rng, L, b) {
      if (rng.next() < 0.55) {   // lo < mx + c ≤ hi
        var w = rng.int(2, 6), lo = b, hi = b + w, loC = rng.next() < 0.5, hiC = rng.next() < 0.5, m = L === 'cp2' ? 1 : rng.pick([1, 2, 3]), c = rng.int(-6, 6);
        var Lt = m * lo + c, Ht = m * hi + c, o1 = loC ? 'le' : 'lt', o2 = hiC ? 'le' : 'lt';
        return { tex: U.tex(Lt) + ' ' + OPS[o1] + ' ' + lin(m, c) + ' ' + OPS[o2] + ' ' + U.tex(Ht), f: function (x) { return test(o1, Lt, m * x + c) && test(o2, m * x + c, Ht); }, parts: [{ lo: lo, loC: loC, hi: hi, hiC: hiC }] };
      }
      var w2 = rng.int(2, 6), A = b, B = b + w2, aC = rng.next() < 0.5, bC = rng.next() < 0.5, p1 = rng.int(-5, 5), p2 = rng.int(-5, 5);
      var oa = aC ? 'le' : 'lt', ob = bC ? 'ge' : 'gt';
      return { tex: lin(1, p1) + ' ' + OPS[oa] + ' ' + U.tex(A + p1) + '\\ \\text{ or }\\ ' + lin(1, p2) + ' ' + OPS[ob] + ' ' + U.tex(B + p2), f: function (x) { return test(oa, x + p1, A + p1) || test(ob, x + p2, B + p2); }, parts: [{ lo: -Infinity, hi: A, hiC: aC }, { lo: B, loC: bC, hi: Infinity }] };
    },
    abs: function (rng, L, b) {
      var h = b, r = rng.int(1, 5), inside = rng.next() < 0.5, strict = rng.next() < 0.5, m = L === 'honors' && rng.next() < 0.4 ? rng.pick([2, 3]) : 1;
      var c = -m * h, rhs = m * r, op = inside ? (strict ? 'lt' : 'le') : (strict ? 'gt' : 'ge'), lo = h - r, hi = h + r;   // |mx − mh| op mr ⇔ |x − h| op r
      var parts = inside ? [{ lo: lo, loC: !strict, hi: hi, hiC: !strict }] : [{ lo: -Infinity, hi: lo, hiC: !strict }, { lo: hi, loC: !strict, hi: Infinity }];
      return { tex: '\\left|' + lin(m, c) + '\\right| ' + OPS[op] + ' ' + U.tex(rhs), f: function (x) { return test(op, Math.abs(m * x + c), rhs); }, parts: parts };
    }
  };
  MK.register({
    id: 'ineq', name: 'Inequality Matching Game', short: 'Inequalities', noun: 'inequality', anchor: 'ineq',
    anchorText: 'Start with each inequality already in its set', anchorHint: 'Recommended: students solve each inequality, then find its graph and description.',
    blurb: 'Match each <b>inequality</b> to the <b>number line</b> that shows its solutions and the <b>words</b> that describe them. Look-alike sets share a boundary point but differ in direction or in whether the endpoint is included.',
    tip: 'Solve the inequality first. Then look at the boundary number, whether it is included (closed dot, ≤ or ≥) or not (open dot, < or >), and which direction the solutions go.',
    fams: { simple: 'Already solved (x > 3)', one: 'One-step', two: 'Two-step', multi: 'Multi-step and variables on both sides', compound: 'Compound (and / or)', abs: 'Absolute value' }, famLabel: 'Inequality types',
    types: [{ id: 'ineq', L: 'I', name: 'Inequality', plural: 'Inequalities' }, { id: 'line', L: 'N', name: 'Number line', plural: 'Number lines' }, { id: 'words', L: 'W', name: 'Words', plural: 'Words' }, { id: 'interval', L: 'S', name: 'Interval notation', plural: 'Interval notation' }],
    units: {
      'math6-inequalities': { fams: ['simple', 'one'], def: ['simple', 'one'], types: ['ineq', 'line', 'words'] },
      'prealgebra7-one-step-equations-inequalities': { fams: ['simple', 'one'], def: ['one'], types: ['ineq', 'line', 'words'] },
      'prealgebra7-solving-equations-inequalities': { fams: ['one', 'two', 'multi'], def: ['two', 'multi'], types: ['ineq', 'line', 'words'] },
      'algebra1-inequalities': { fams: ['one', 'two', 'multi', 'compound', 'abs'], def: ['two', 'multi', 'compound'], types: ['ineq', 'line', 'words'] },
      'precalculus-equations-inequalities': { fams: ['two', 'multi', 'compound', 'abs'], def: ['compound', 'abs'] }
    },
    gen: function (rng, L, cfg, Un, sets) {
      var fam = rng.pick(cfg.fams), b;
      var twin = sets.length && rng.next() < (L === 'cp2' ? 0.25 : 0.45) ? rng.pick(sets) : null;   // look-alike: same boundary
      b = twin ? twin.b : rng.int(-7, 7);
      if (L === 'honors' && fam !== 'abs' && fam !== 'compound' && rng.next() < 0.15 && /precalculus|algebra1/.test(cfg.unit)) b += 0.5;
      var r = IFAM[fam](rng, L, b); if (!r) return null;
      // independent check: the printed inequality's solutions are exactly the solution set
      var pts = []; r.parts.forEach(function (p) { [p.lo, p.hi].forEach(function (e) { if (isFinite(e)) pts.push(e - 0.5, e - 0.01, e, e + 0.01, e + 0.5); }); });
      for (var x = -20; x <= 20; x += 0.25) pts.push(x);
      if (!pts.every(function (x0) { return r.f(x0) === inSet(r.parts, x0); })) return null;
      var ends = []; r.parts.forEach(function (p) { if (isFinite(p.lo)) ends.push(p.lo); if (isFinite(p.hi)) ends.push(p.hi); });
      var mn = Math.min.apply(null, ends), mx = Math.max.apply(null, ends);
      if (mx - mn > 10) return null;
      var half = ends.some(function (e) { return !U.isInt(e); });
      var lo = Math.floor((mn + mx) / 2) - 6, nl = { lo: lo, hi: lo + 12, step: half ? 0.5 : 1, labelEvery: half ? 2 : 1, parts: r.parts };
      return { fam: fam, b: b, tex: r.tex, parts: r.parts, key: solKey(r.parts), nl: nl, words: wordsOf(r.parts, rng, L), interval: intervalTex(r.parts) };
    },
    key: function (t, s) { return s.key; },
    face: function (s, t, mode) {
      if (t === 'ineq') return U.bigTex(s.tex);
      if (t === 'line') return '<div class="mk-wide">' + SV.numberLine(s.nl) + '</div>';
      if (t === 'words') return '<div class="mk-txt">' + U.mt(s.words) + '</div>';
      return U.bigTex(s.interval);
    },
    summary: function (s) { return k(s.tex); },
    noGrid: true, wide: ['line'], printCols: { line: 2, words: 3 }, printRows: { line: 6 }
  });

  /* ======================= PROPORTIONAL RELATIONSHIPS ======================= */
  var CTX = [   // r: the rates that make sense in each situation
    { id: 'apples', r: [0.25, 6], x: 'pounds of apples', y: 'cost in dollars', money: true, unit: function (kk) { return 'Apples cost ' + money(kk) + ' per pound.'; }, pair: function (q, p) { return q + ' pounds of apples cost ' + money(p) + '.'; } },
    { id: 'bike', r: [5, 16], x: 'hours', y: 'miles', unit: function (kk) { return 'A cyclist rides at ' + num(kk) + ' miles per hour.'; }, pair: function (q, p) { return 'A cyclist rides ' + num(p) + ' miles in ' + q + ' hours.'; } },
    { id: 'printer', r: [1, 12], x: 'minutes', y: 'pages', unit: function (kk) { return 'A printer prints ' + num(kk) + ' pages per minute.'; }, pair: function (q, p) { return 'A printer prints ' + num(p) + ' pages in ' + q + ' minutes.'; } },
    { id: 'job', r: [7, 16], x: 'hours worked', y: 'dollars earned', money: true, unit: function (kk) { return 'Maya earns ' + money(kk) + ' per hour.'; }, pair: function (q, p) { return 'Maya earns ' + money(p) + ' for ' + q + ' hours of work.'; } },
    { id: 'hose', r: [1, 12], x: 'minutes', y: 'gallons', unit: function (kk) { return 'A hose fills a pool at ' + num(kk) + ' gallons per minute.'; }, pair: function (q, p) { return 'A hose puts ' + num(p) + ' gallons into a pool in ' + q + ' minutes.'; } },
    { id: 'recipe', r: [0.25, 4], x: 'cups of flour', y: 'cups of sugar', unit: function (kk) { return 'A recipe uses ' + num(kk) + ' cups of sugar for every cup of flour.'; }, pair: function (q, p) { return 'A recipe uses ' + num(p) + ' cups of sugar for every ' + q + ' cups of flour.'; } },
    { id: 'plant', r: [0.25, 5], x: 'weeks', y: 'centimeters of growth', unit: function (kk) { return 'A plant grows ' + num(kk) + ' centimeters each week.'; }, pair: function (q, p) { return 'A plant grows ' + num(p) + ' centimeters in ' + q + ' weeks.'; } },
    { id: 'walk', r: [0.1, 1.5], x: 'minutes', y: 'laps around the track', unit: function (kk) { return 'Jon walks ' + num(kk) + (kk === 1 ? ' lap' : kk < 1 ? ' of a lap' : ' laps') + ' each minute.'; }, pair: function (q, p) { return 'Jon walks ' + num(p) + ' laps in ' + q + ' minutes.'; } },
    { id: 'tickets', r: [4, 15], x: 'tickets', y: 'cost in dollars', money: true, unit: function (kk) { return 'Movie tickets cost ' + money(kk) + ' each.'; }, pair: function (q, p) { return q + ' movie tickets cost ' + money(p) + '.'; } },
    { id: 'snack', r: [0.5, 3], x: 'bags of trail mix', y: 'cups of peanuts', unit: function (kk) { return 'Each bag of trail mix has ' + num(kk) + ' cups of peanuts.'; }, pair: function (q, p) { return q + ' bags of trail mix have ' + num(p) + ' cups of peanuts.'; } },
    { id: 'fuel', r: [2, 12], x: 'liters of gas', y: 'kilometers driven', unit: function (kk) { return 'A scooter goes ' + num(kk) + ' kilometers on each liter of gas.'; }, pair: function (q, p) { return 'A scooter goes ' + num(p) + ' kilometers on ' + q + ' liters of gas.'; } }
  ];
  function money(v) { return '$' + (U.isInt(v) ? String(Math.round(v)) : v.toFixed(2)); }
  function num(v) { return U.isInt(v) ? String(Math.round(v)) : U.isInt(v * 100) ? String(U.round(v, 2)) : U.m(U.tex(v)); }
  var KPOOL = {
    cp2: [2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    cp1: [1.5, 2.5, 0.5, 3.5, 1.25, 0.75, 2, 3, 4, 6, 4.5, 0.25],
    honors: [2 / 3, 3 / 4, 4 / 3, 3 / 2, 5 / 2, 2 / 5, 5 / 4, 1 / 3, 3 / 5, 7 / 2, 5 / 3, 0.4, 1.2]
  };
  MK.register({
    id: 'prop', name: 'Proportional Relationship Matching', short: 'Proportional Relationships', noun: 'proportional relationship', anchor: 'sit',
    anchorText: 'Start with each situation already in its set', anchorHint: 'Recommended: students find the unit rate in each situation, then the matching equation, table and graph.',
    blurb: 'Match each <b>situation</b> to its <b>equation</b> (y = kx), <b>table</b> and <b>graph</b>. Find the constant of proportionality (the unit rate) in every representation. Watch for look-alikes that flip the rate (3/4 and 4/3).',
    tip: 'Find the unit rate: how much y for 1 x. In a table it is y ÷ x; on a graph it is the y-value at x = 1; in the equation y = kx it is k.',
    types: [{ id: 'sit', L: 'S', name: 'Situation', plural: 'Situations' }, { id: 'eq', L: 'E', name: 'Equation', plural: 'Equations' }, { id: 'table', L: 'T', name: 'Table', plural: 'Tables' }, { id: 'graph', L: 'G', name: 'Graph', plural: 'Graphs' }],
    units: { 'math6-ratios-rates-percent-proportions': {}, 'prealgebra7-ratios-proportions-percentages': {} },
    context: function (rng) { return { ctx: rng.shuffle(CTX.slice()) }; },
    gen: function (rng, L, cfg, Un, sets) {
      var pool = L === 'honors' ? KPOOL.honors.concat([2, 3, 1.5]) : KPOOL[L], kk;
      var twin = sets.length && L !== 'cp2' && rng.next() < 0.4 ? rng.pick(sets) : null;
      kk = twin && !U.near(1 / twin.k, twin.k) ? 1 / twin.k : rng.pick(pool);
      if (L === 'cp2' && !U.isInt(kk)) return null;
      var q = U.toQ(kk, 12); if (!q || q.d > 6 || q.n > 12 * q.d) return null;
      var C = cfg.ctx.ctx.filter(function (c0) { return kk >= c0.r[0] && kk <= c0.r[1] && !sets.some(function (o) { return o.ctx === c0.id; }); })[0];
      if (!C) return null;
      if (C.money && U.toQ(kk * 100, 1) === null) return null;
      // table: four x-values that give whole (or money) y-values
      var base = q.d, xs = rng.pick([[1, 2, 3, 4], [1, 2, 4, 5], [2, 3, 5, 6], [1, 3, 5, 8]]).map(function (i) { return i * base; });
      var rows = xs.map(function (x) { return [x, kk * x]; });
      if (rows.some(function (r) { return !U.isInt(r[1]) && !(C.money && U.isInt(r[1] * 100)); })) return null;
      // situation: the unit rate itself, or a pair to divide (not at cp2)
      var pairQ = (L === 'cp2' ? 1 : rng.pick([2, 3, 4, 5, 6])) * base; if (pairQ === 1 && !U.isInt(kk)) pairQ = base;
      var pairP = kk * pairQ, unitForm = L === 'cp2' ? rng.next() < 0.6 : rng.next() < 0.25;
      if (!U.isInt(pairP) && !(C.money && U.isInt(pairP * 100))) return null;
      if (!unitForm && pairQ === 1) unitForm = true;
      if (unitForm && !C.money && !U.isInt(kk) && L === 'cp2') return null;
      var sit = (unitForm ? C.unit(kk) : C.pair(pairQ, pairP)) + ' Let ' + U.m('x') + ' be the ' + C.x + ' and ' + U.m('y') + ' the ' + C.y + '.';
      // graph window: first quadrant, about ten squares each way
      var xmax = Math.max(10, base * 5), xstep = xmax > 12 ? Math.ceil(xmax / 10) : 1; xmax = xstep * 10;
      var ymaxRaw = kk * xmax, ystep = [1, 2, 5, 10, 20, 25, 50].filter(function (s0) { return ymaxRaw / s0 <= 12; })[0] || 100, ymax = ystep * Math.max(6, Math.min(12, Math.ceil(ymaxRaw / ystep)));
      var dots = []; for (var x = xstep; x <= xmax; x += xstep) { var y = kk * x; if (y <= ymax && U.isInt(y / ystep * 2) && U.isInt(y)) dots.push([x, y]); }
      if (dots.length < 2) return null;
      var eq = 'y = ' + (U.isInt(kk) ? String(kk) : (!U.isInt(kk * 100) || (L === 'honors' && rng.next() < 0.6)) ? U.tex(kk) : String(U.round(kk, 2))) + 'x';
      return { k: kk, sit: sit, eq: eq, rows: rows, graph: { xmin: 0, xmax: xmax, ymin: 0, ymax: ymax, xstep: xstep, ystep: ystep, ylabEvery: ymax / ystep > 8 ? 2 : 1, xlabEvery: 2, dots: dots.slice(0, 3) }, ctx: C.id };
    },
    key: function (t, s) { return t === 'sit' ? 'k' + s.k.toFixed(6) + '|' + s.ctx : 'k' + s.k.toFixed(6); },
    fits: function (t, a, b) { return U.near(a.k, b.k); },
    face: function (s, t, mode) {
      if (t === 'sit') return '<div class="mk-txt left">' + U.mt(s.sit) + '</div>';
      if (t === 'eq') return U.bigTex(s.eq, true);
      if (t === 'table') return '<table class="mk-tt"><tr><th>' + k('x') + '</th><th>' + k('y') + '</th></tr>' + s.rows.map(function (r) { return '<tr><td>' + k(U.tex(r[0])) + '</td><td>' + k(U.isInt(r[1]) ? String(r[1]) : r[1].toFixed(2)) + '</td></tr>'; }).join('') + '</table>';
      var g = s.graph, items = [{ kind: 'curve', pts: [[0, 0], [Math.min(g.xmax, g.ymax / s.k), Math.min(g.ymax, s.k * g.xmax)]] }].concat(g.dots.map(function (d) { return { kind: 'dot', x: d[0], y: d[1] }; }));
      return SV.plane({ xmin: 0, xmax: g.xmax, ymin: 0, ymax: g.ymax, xstep: g.xstep, ystep: g.ystep, xlabEvery: g.xlabEvery, ylabEvery: g.ylabEvery, items: items.concat([{ kind: 'dot', x: 0, y: 0, r: 3.4 }]) }, { big: mode === 'big' });
    },
    summary: function (s) { return k(s.eq); }
  });

  /* ======================= FRACTIONS, DECIMALS, PERCENTS ======================= */
  var VPOOL = {
    cp2: [[1, 2], [1, 4], [3, 4], [1, 5], [2, 5], [3, 5], [4, 5], [1, 10], [3, 10], [7, 10], [9, 10], [37, 100], [3, 20], [1, 20], [6, 25]],
    cp1: [[1, 8], [3, 8], [5, 4], [3, 2], [7, 20], [9, 25], [3, 100], [1, 25], [17, 20], [11, 50], [6, 5], [2, 5], [3, 4], [7, 10], [1, 20]],
    honors: [[1, 3], [2, 3], [1, 6], [5, 6], [5, 8], [7, 8], [1, 200], [9, 4], [7, 40], [4, 3], [1, 9], [3, 400], [11, 8], [5, 3]]
  };
  function decTex(n, d) {   // exact decimal, or repeating with an overline
    var ip = Math.floor(n / d), r = n % d, digits = '', seen = {}, i = 0;
    while (r && seen[r] === undefined && i < 12) { seen[r] = i++; r *= 10; digits += Math.floor(r / d); r %= d; }
    if (!r) return ip + (digits ? '.' + digits : '');
    var st = seen[r]; return ip + '.' + digits.slice(0, st) + '\\overline{' + digits.slice(st) + '}';
  }
  function pctTex(n, d, L) {
    var p = n * 100 / d;
    if (U.isInt(p)) return Math.round(p) + '\\%';
    if (U.isInt(p * 1000)) return String(U.round(p, 3)) + '\\%';
    var g = U.gcd(n * 100, d), pn = n * 100 / g, pd = d / g, w = Math.floor(pn / pd);
    return (w ? w : '') + '\\tfrac{' + (pn % pd) + '}{' + pd + '}\\%';
  }
  /* Grade 4: tenths and hundredths, written with a denominator of 10 or 100 as in the course */
  function tenthsSet(rng, L, sets) {
    var hund = L === 'cp2' ? rng.next() < 0.4 : rng.next() < 0.7, whole = L === 'honors' && rng.next() < 0.4 ? 1 : 0, part = hund ? rng.int(1, 99) : rng.int(1, 9);
    var twin = sets.length && rng.next() < 0.4 ? rng.pick(sets) : null;
    if (twin) { if (twin.d === 10) { hund = true; part = twin.p; } else if (twin.p % 10 && twin.p < 10) { hund = false; part = twin.p; } else if (twin.p > 9 && twin.p % 10) { hund = true; part = (twin.p % 10) * 10 + Math.floor(twin.p / 10); } }   // 0.4 and 0.04; 0.37 and 0.73
    if (hund && part % 10 === 0) return null;
    var d = hund ? 100 : 10, n = whole * d + part, v = n / d;
    var ord = d === 10 ? ['tenth', 'tenths'] : ['hundredth', 'hundredths'], words = (whole ? 'one and ' : '') + U.words(part) + ' ' + ord[part === 1 ? 0 : 1];
    return { n: n, d: d, p: part, v: v, frac: whole && L === 'honors' ? '1\\tfrac{' + part + '}{' + d + '}' : '\\frac{' + n + '}{' + d + '}', dec: v.toFixed(d === 10 ? 1 : 2), pct: '', words: words, model: { kind: 'grid', n: Math.round(v * 100) } };
  }
  MK.register({
    id: 'fdp', name: 'Fraction, Decimal and Percent Matching', short: 'Fractions, Decimals & Percents', noun: 'number', anchor: 'frac',
    anchorText: 'Start with each fraction already in its set', anchorHint: 'Turn this off for a harder sort that can start from any card.',
    blurb: 'Match each <b>fraction</b> to the same amount as a <b>decimal</b>, a <b>percent</b> and a <b>model</b> (a hundred grid or a fraction strip). Look-alikes such as 40% and 4% (0.4 and 0.04) sit side by side.',
    tip: 'Change everything to hundredths: a percent is "per hundred", and a hundred grid shows hundredths. For a strip, count the shaded parts out of the parts in one whole.',
    types: [{ id: 'frac', L: 'F', name: 'Fraction', plural: 'Fractions' }, { id: 'dec', L: 'D', name: 'Decimal', plural: 'Decimals' }, { id: 'pct', L: 'P', name: 'Percent', plural: 'Percents' }, { id: 'model', L: 'M', name: 'Model', plural: 'Models' }, { id: 'words', L: 'W', name: 'Words', plural: 'Words' }],
    units: { 'math6-ratios-rates-percent-proportions': { types: ['frac', 'dec', 'pct', 'model'] }, 'prealgebra7-ratios-proportions-percentages': { types: ['frac', 'dec', 'pct', 'model'] },
      'grade4-fraction-operations-decimals': { types: ['frac', 'dec', 'model', 'words'], tenths: true, name: 'Fraction Operations and Decimals', short: 'Tenths and Hundredths', noun: 'decimal' } },
    gen: function (rng, L, cfg, Un, sets) {
      if (Un.tenths) return tenthsSet(rng, L, sets);
      var pool = L === 'cp2' ? VPOOL.cp2 : L === 'cp1' ? VPOOL.cp1.concat(VPOOL.cp2) : VPOOL.honors.concat(VPOOL.cp1), nd;
      var twin = sets.length && rng.next() < 0.35 ? rng.pick(sets) : null;
      if (twin) { var t2 = rng.pick([[twin.n, twin.d * 10], [twin.n * 10, twin.d]]); var g0 = U.gcd(t2[0], t2[1]); nd = [t2[0] / g0, t2[1] / g0]; if (nd[0] / nd[1] > 2.5 || nd[0] / nd[1] < 0.005 || nd[1] > 400) return null; }
      else nd = rng.pick(pool);
      var n = nd[0], d = nd[1], v = n / d, h = v * 100;
      if (U.isInt(h) && h <= 200 && h >= 1) var model = { kind: 'grid', n: Math.round(h) };
      else if (d <= 12) model = { kind: 'bars', n: n, d: d };
      else return null;
      if (model.kind === 'grid' && d <= 10 && rng.next() < 0.35) model = { kind: 'bars', n: n, d: d };   // strips for some tenths and fifths too
      var shown = [n, d];   // an equivalent fraction that is not simplified, sometimes
      if (L !== 'cp2' && d <= 10 && rng.next() < 0.35) { var m = rng.pick([2, 3, 4]); shown = [n * m, d * m]; }
      var mixed = L !== 'cp2' && shown[0] > shown[1] && rng.next() < 0.6;
      var frac = mixed ? Math.floor(shown[0] / shown[1]) + '\\tfrac{' + (shown[0] % shown[1]) + '}{' + shown[1] + '}' : '\\frac{' + shown[0] + '}{' + shown[1] + '}';
      if (mixed && shown[0] % shown[1] === 0) frac = String(shown[0] / shown[1]);
      return { n: n, d: d, v: v, frac: frac, dec: decTex(n, d), pct: pctTex(n, d, L), model: model };
    },
    key: function (t, s) { return String(s.v); },
    face: function (s, t, mode) {
      if (t === 'frac') return U.bigTex(s.frac, true);
      if (t === 'dec') return U.bigTex(s.dec);
      if (t === 'pct') return U.bigTex(s.pct);
      if (t === 'words') return '<div class="mk-txt">' + s.words + '</div>';
      return '<div class="mk-wide">' + (s.model.kind === 'grid' ? SV.hundredGrids(s.model.n) : SV.bars(s.model.n, s.model.d)) + '</div>';
    },
    summary: function (s) { return k(s.frac) + ' = ' + k(s.dec) + (s.pct ? ' = ' + k(s.pct) : ''); },
    noGrid: true, wide: ['model'], printCols: { model: 2 }, printRows: { model: 4 }
  });

  /* ======================= SYSTEMS OF LINEAR EQUATIONS ======================= */
  function stdForm(m, b) {   // y = mx + b  →  Ax + By = C with integers, A > 0 (or B > 0 when A = 0), gcd 1
    var q = U.toQ(m, 12), qb = U.toQ(b, 12), L2 = q.d * qb.d / U.gcd(q.d, qb.d);
    var A = -m * L2, B = L2, C = b * L2; A = Math.round(A); C = Math.round(C);
    var g = U.gcd(U.gcd(A, B), C); A /= g; B /= g; C /= g;
    if (A < 0 || (A === 0 && B < 0)) { A = -A; B = -B; C = -C; }
    return [A, B, C];
  }
  function stdTex(f) { var A = f[0], B = f[1], C = f[2], s = ''; if (A) s = (A === 1 ? '' : A === -1 ? '-' : A) + 'x'; if (B) s += (s ? (B < 0 ? ' - ' : ' + ') : (B < 0 ? '-' : '')) + (Math.abs(B) === 1 ? '' : Math.abs(B)) + 'y'; return s + ' = ' + C; }
  var MPOOL = { cp2: [1, 2, 3, -1, -2, -3], cp1: [1, 2, 3, -1, -2, -3, 1 / 2, -1 / 2, 4, -4], honors: [1, 2, 3, -1, -2, -3, 1 / 2, -1 / 2, 2 / 3, -2 / 3, 3 / 2, -3 / 2, 1 / 3, -1 / 3] };
  MK.register({
    id: 'sys', name: 'Systems of Equations Matching', short: 'Systems of Equations', noun: 'system', anchor: 'si',
    anchorText: 'Start with each system in slope-intercept form already in its set', anchorHint: 'Recommended: students graph or solve each system, then find its other cards.',
    blurb: 'Match each <b>system in slope-intercept form</b> to its <b>graph</b>, the same system in <b>standard form</b>, and its <b>solution</b>. Look-alike sets share one line, and one set may have no solution.',
    tip: 'The solution is the point where the two lines cross: check it in both equations. To compare forms, rewrite Ax + By = C as y = mx + b.',
    types: [{ id: 'si', L: 'Y', name: 'Slope-intercept form', plural: 'Slope-intercept' }, { id: 'graph', L: 'G', name: 'Graph', plural: 'Graphs' }, { id: 'std', L: 'S', name: 'Standard form', plural: 'Standard form' }, { id: 'sol', L: 'X', name: 'Solution', plural: 'Solutions' }],
    units: { 'algebra1-systems-of-equations': {}, 'prealgebra-systems-linear-equations': {} },
    gen: function (rng, L, cfg, Un, sets) {
      var pool = MPOOL[L], m1 = rng.pick(pool), m2 = rng.pick(pool), h = rng.int(-4, 4), kk = rng.int(-4, 4), none = false;
      if (L !== 'cp2' && !sets.some(function (s) { return s.none; }) && rng.next() < 0.15) none = true;
      var twin = sets.length && rng.next() < 0.4 ? rng.pick(sets.filter(function (s) { return !s.none; })) : null;
      var l1, l2;
      if (none) { var mm = rng.pick(pool), b1 = rng.int(-5, 5), b2 = rng.int(-5, 5); if (b1 === b2) return null; l1 = [mm, b1]; l2 = [mm, b2]; }
      else {
        if (U.near(m1, m2)) return null;
        if (twin) { l1 = twin.lines[rng.int(0, 1)]; var hh = rng.int(-5, 5); if (!U.isInt(l1[0] * hh)) return null; h = hh; kk = l1[0] * h + l1[1]; if (U.near(m2, l1[0])) return null; }
        else l1 = [m1, kk - m1 * h];
        l2 = [m2, kk - m2 * h];
        if (!U.isInt(l1[1]) || !U.isInt(l2[1]) || !U.isInt(kk) || Math.abs(kk) > 5 || Math.abs(h) > 5) return null;
      }
      if ([l1, l2].some(function (l) { return Math.abs(l[1]) > 7; })) return null;
      if (rng.next() < 0.5) { var t0 = l1; l1 = l2; l2 = t0; }
      var lines = [l1, l2], std = lines.map(function (l) { return stdForm(l[0], l[1]); });
      if (L !== 'cp2' && rng.next() < 0.3) { var sc = rng.pick([2, -1, 3]); std[1] = std[1].map(function (c) { return c * sc; }); }
      if (rng.next() < 0.5) std = [std[1], std[0]];
      // independent check: the solution satisfies both printed standard-form equations; parallel lines never meet
      if (!none && !std.every(function (f) { return U.near(f[0] * h + f[1] * kk, f[2]); })) return null;
      if (none && !U.near(std[0][0] * std[1][1] - std[0][1] * std[1][0], 0)) return null;
      return { lines: lines, std: std, none: none, h: h, k: kk, sol: none ? 'none' : h + ',' + kk };
    },
    key: function (t, s) { var ls = s.lines.map(function (l) { return l[0].toFixed(4) + ':' + l[1]; }).sort().join('|'); return t === 'sol' ? s.sol : ls; },
    face: function (s, t, mode) {
      if (t === 'si') return U.bigTex('\\begin{cases} y = ' + lin(s.lines[0][0], s.lines[0][1]) + ' \\\\ y = ' + lin(s.lines[1][0], s.lines[1][1]) + '\\end{cases}', true);
      if (t === 'std') return U.bigTex('\\begin{cases} ' + stdTex(s.std[0]) + ' \\\\ ' + stdTex(s.std[1]) + '\\end{cases}', true);
      if (t === 'sol') return '<div class="mk-txt mk-big">' + (s.none ? 'No solution' : k('(' + s.h + ',\\ ' + s.k + ')')) + '</div>';
      var w = { xmin: -7, xmax: 7, ymin: -7, ymax: 7 };
      return SV.plane({ xmin: -7, xmax: 7, ymin: -7, ymax: 7, xstep: 1, ystep: 1, items: s.lines.map(function (l, i) { return { kind: 'curve', pieces: SV.sample(function (x) { return l[0] * x + l[1]; }, w, { n: 60 }), color: i ? SV.colors.orange : SV.colors.blue }; }) }, { big: mode === 'big' });
    },
    summary: function (s) { return s.none ? 'No solution' : k('(' + s.h + ',\\ ' + s.k + ')'); }
  });
})(typeof window !== 'undefined' ? window : globalThis);
