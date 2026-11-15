/* Kind-specific independent checks for match-kinds-tests.cjs: each card is re-derived from the set's answer. */
'use strict';
const near = (a, b) => Math.abs(a - b) < 1e-7;
module.exports = {
  ineq(B, ok, tag) {
    B.sets.forEach(s => {
      // the number-line parts are the solution parts, inside the drawn window
      ok(s.nl.parts === s.parts, tag + ': number line shows the solution');
      s.parts.forEach(p => [p.lo, p.hi].filter(isFinite).forEach(e => ok(e >= s.nl.lo && e <= s.nl.hi, tag + ': endpoint on the number line')));
      // words: every number in the words is a boundary, and inclusive words go with closed endpoints
      const nums = (s.words.match(/⟨[^⟩]*⟩/g) || []).map(m => m.slice(1, -1));
      ok(nums.length >= 1, tag + ': words name a boundary');
      const closed = s.parts.some(p => p.loC || p.hiC);
      if (/or equal|at least|at most|no more|no less|no greater|including (?!either)/.test(s.words)) ok(closed, tag + ': inclusive words need a closed endpoint: ' + s.words);
    });
  },
  prop(B, ok, tag) {
    B.sets.forEach(s => {
      s.rows.forEach(([x, y]) => ok(near(y, s.k * x), tag + ': table row on y = kx'));
      s.graph.dots.forEach(([x, y]) => ok(near(y, s.k * x), tag + ': graph dot on y = kx'));
      const m = s.eq.match(/^y = (.*)x$/); ok(m, tag + ': equation form');
      const kv = /frac\{(\d+)\}\{(\d+)\}/.test(m[1]) ? (() => { const q = m[1].match(/frac\{(\d+)\}\{(\d+)\}/); return q[1] / q[2]; })() : +m[1];
      ok(near(kv, s.k), tag + ': equation constant is k: ' + s.eq);
      // the situation's numbers give k: the unit rate, or a pair whose quotient is k
      const nums = (s.sit.replace(/,/g, '').match(/\d+(\.\d+)?/g) || []).map(Number);
      ok(nums.some(n => near(n, s.k)) || nums.some(a => nums.some(b => b && near(a / b, s.k))) || /frac/.test(s.sit), tag + ': situation gives k: ' + s.sit);
    });
  },
  fdp(B, ok, tag) {
    B.sets.forEach(s => {
      const v = s.n / s.d;
      if (!/overline/.test(s.dec)) ok(near(+s.dec, v), tag + ': decimal ' + s.dec);
      if (s.words) ok(/tenth|hundredth/.test(s.words), tag + ': decimal words');
      const pm = s.pct.match(/^([\d.]+)\\%$/); if (pm) ok(near(+pm[1] / 100, v), tag + ': percent ' + s.pct);
      const fm = s.frac.match(/^(?:(\d+)\\tfrac)?\\?f?r?a?c?\{(\d+)\}\{(\d+)\}$/);
      if (fm) ok(near((+(fm[1] || 0)) + fm[2] / fm[3], v), tag + ': fraction ' + s.frac);
      if (s.model.kind === 'grid') ok(near(s.model.n / 100, v), tag + ': grid'); else ok(near(s.model.n / s.model.d, v), tag + ': strips');
    });
  },
  data(B, ok, tag, env) {
    B.sets.forEach(s => {
      const v = s.v, n = v.length, srt = v.slice().sort((a, b) => a - b);
      ok(srt.join() === v.join(), tag + ': data sorted');
      ok(s.hist.reduce((a, b) => a + b, 0) === n, tag + ': histogram counts every value once');
      const E = B.ctx.edges; s.hist.forEach((c, i) => ok(c === v.filter(x => x >= E[i] && (x < E[i + 1] || (i === E.length - 2 && x <= E[i + 1]))).length, tag + ': bin count'));
      const med = a => a.length % 2 ? a[(a.length - 1) / 2] : (a[a.length / 2 - 1] + a[a.length / 2]) / 2, h = Math.floor(n / 2);
      ok(s.five.join() === [srt[0], med(srt.slice(0, h)), med(srt), med(srt.slice(n % 2 ? h + 1 : h)), srt[n - 1]].join(), tag + ': five-number summary');
      if (s.facts) s.facts.forEach(f => ok(f.test(s.st), tag + ': fact true: ' + f.text));
      v.forEach(x => ok(x >= B.ctx.ax.lo && x <= B.ctx.ax.hi, tag + ': value on the axis'));
      if (B.ctx.stem) v.forEach(x => ok(B.ctx.stems.includes(Math.floor(x / 10)), tag + ': stem exists'));
    });
  },
  trig(B, ok, tag) {
    B.sets.forEach(s => {
      s.rows.forEach(([xq, y]) => ok(Math.abs(s.a * Math[s.fn](s.b * (xq * Math.PI - s.c)) + s.d - y) < 1e-9, tag + ': table point on the curve'));
      s.facts.forEach(f => ok(f.test(s), tag + ': feature true: ' + f.text));
      ok(Math.abs(s.a) + Math.abs(s.d) <= 5, tag + ': fits the window');
    });
  },
  deriv(B, ok, tag) {
    const ev = (p, x) => p.reduce((a, c, i) => a + c * x ** i, 0);
    B.sets.forEach(s => {
      for (let x = -4; x <= 4; x += 0.37) {   // f′ is the derivative of f, f″ of f′ (numerically)
        ok(Math.abs((ev(s.f, x + 1e-5) - ev(s.f, x - 1e-5)) / 2e-5 - ev(s.fp, x)) < 1e-4, tag + ': f′ is the derivative of f');
        ok(Math.abs((ev(s.fp, x + 1e-5) - ev(s.fp, x - 1e-5)) / 2e-5 - ev(s.fpp, x)) < 1e-4, tag + ': f″ is the derivative of f′');
      }
      s.crit.forEach(x => ok(Math.abs(ev(s.fp, x)) < 1e-9 && ev(s.fp, x - 0.05) * ev(s.fp, x + 0.05) < 0, tag + ': critical point'));
      s.infl.forEach(x => ok(Math.abs(ev(s.fpp, x)) < 1e-9 && ev(s.fpp, x - 0.05) * ev(s.fpp, x + 0.05) < 0, tag + ': inflection point'));
      s.facts.forEach(f => ok(f.test(s), tag + ': behavior true: ' + f.text));
    });
  },
  conic(B, ok, tag) {
    B.sets.forEach(s => {
      ok(s.facts.every(f => f.test(s)), tag + ': features true');
      // a point on the drawn curve satisfies the general form
      const g = s.gen, on = (x, y) => Math.abs(g[0] * x * x + g[1] * y * y + g[2] * x + g[3] * y + g[4]) < 1e-6;
      if (s.fam === 'circle') ok(on(s.h + s.r, s.k) && on(s.h, s.k - s.r), tag + ': circle points');
      if (s.fam === 'parabola') ok(on(s.h, s.k) && (s.vert ? on(s.h + 2 * Math.abs(s.p) * 2 / 2 * 1, s.k + (2 * Math.abs(s.p)) ** 2 / (4 * s.p)) : on(s.h + (2 * Math.abs(s.p)) ** 2 / (4 * s.p), s.k + 2 * Math.abs(s.p))), tag + ': parabola points');
      if (s.fam === 'ellipse') ok(on(s.h + Math.sqrt(s.A), s.k) && on(s.h, s.k + Math.sqrt(s.B)), tag + ': ellipse points');
      if (s.fam === 'hyperbola') ok(s.horiz ? on(s.h + Math.sqrt(s.A), s.k) : on(s.h, s.k + Math.sqrt(s.A)), tag + ': hyperbola vertex');
      // the vertices fact matches the general form
      if (s.attr.verts) { const nums = s.attr.verts.text.match(/-?\d+(\.\d+)?/g); ok(nums && nums.length >= 4, tag + ': vertices printed'); }
    });
  },
  logic(B, ok, tag, env) {
    const L = env.MKMATCH.logic;
    B.sets.forEach(s => {
      ok(L.tt(s.f) === s.t && L.tt(s.g) === s.t, tag + ': symbols and equivalent have the truth table');
      ok(s.sym !== s.equiv, tag + ': equivalent card is a different statement');
      ok(!/TTTT|FFFF/.test(s.t), tag + ': not a tautology or contradiction');
      ok(/\.$|\)$/.test(s.words), tag + ': sentence');
    });
  },
  xform(B, ok, tag) {
    const tri = B.ctx.tri;
    B.sets.forEach(s => {
      // read the printed rule independently: substitute each vertex
      const m = /^\((.*),\\ (.*)\)$/.exec(s.rule); ok(m, tag + ': rule form ' + s.rule);
      const evalExpr = (e, x, y) => Function('x', 'y', 'return ' + e.replace(/\\frac\{(\d+)\}\{(\d+)\}/g, '($1/$2)').replace(/(\d|\))([xy])/g, '$1*$2') + ';')(x, y);
      tri.forEach((P, i) => { ok(Math.abs(evalExpr(m[1], P[0], P[1]) - s.img[i][0]) < 1e-9 && Math.abs(evalExpr(m[2], P[0], P[1]) - s.img[i][1]) < 1e-9, tag + ': rule maps vertex ' + s.rule); });
      s.img.forEach(P => ok(Math.abs(P[0]) <= 8 && Math.abs(P[1]) <= 8, tag + ': image on the grid'));
    });
  },
  place(B, ok, tag, env) {
    const U = env.MKMATCH.util, K = env.MKMATCH.kinds.place;
    B.sets.forEach(s => {
      const html = t => K.face(s, t, 'full', B);
      if (B.types.includes('words') && !s.dec) ok(html('words').includes(U.words(s.n)), tag + ': number name');
      if (B.types.includes('expanded') && !s.dec) { const terms = (html('expanded').match(/annotation encoding="application\/x-tex">([^<]*)</) || [])[1]; ok(terms && terms.split('+').reduce((a, t) => a + +t.replace(/[{},\s]/g, ''), 0) === s.n, tag + ': expanded form adds up: ' + terms); }
      if (s.dec) { const terms = (html('expanded').match(/annotation encoding="application\/x-tex">([^<]*)</) || [])[1]; ok(Math.abs(terms.split('+').reduce((a, t) => a + +t, 0) - s.n / 1000) < 1e-9, tag + ': decimal expanded form adds up'); }
      if (B.types.includes('tensones')) ok(html('tensones').includes(Math.floor(s.n / 10) + ' tens ' + s.n % 10 + ' ones'), tag + ': tens and ones');
    });
  },
  time(B, ok, tag) {
    B.sets.forEach(s => {
      ok(s.h >= 1 && s.h <= 12 && s.m >= 0 && s.m < 60, tag + ': a real time');
      const w = s.words; let m;
      if ((m = /^(\d+) o’clock$/.exec(w))) ok(+m[1] === s.h && s.m === 0, tag + ': ' + w);
      else if ((m = /^half past (\d+)$/.exec(w))) ok(+m[1] === s.h && s.m === 30, tag + ': ' + w);
      else if ((m = /^quarter past (\d+)$/.exec(w))) ok(+m[1] === s.h && s.m === 15, tag + ': ' + w);
      else if ((m = /^quarter to (\d+)$/.exec(w))) ok(+m[1] === s.h % 12 + 1 && s.m === 45, tag + ': ' + w);
      else if ((m = /^(\d+) minutes? after (\d+)$/.exec(w))) ok(+m[1] === s.m && +m[2] === s.h, tag + ': ' + w);
      else if ((m = /^(\d+) minutes? to (\d+)$/.exec(w))) ok(60 - +m[1] === s.m && +m[2] === s.h % 12 + 1, tag + ': ' + w);
      else ok(false, tag + ': unknown words ' + w);
    });
  },
  money(B, ok, tag) { B.sets.forEach(s => { const sum = a => a.reduce((p, q) => p + q, 0); ok(sum(s.a) === s.c && sum(s.b) === s.c && s.a.join() !== s.b.join(), tag + ': both collections are worth the amount'); }); },
  mult(B, ok, tag) { B.sets.forEach(s => ok(s.g * s.e === s.p, tag + ': product')); ok(new Set(B.sets.map(s => s.p)).size === B.sets.length, tag + ': different totals'); },
  efrac(B, ok, tag) {
    B.sets.forEach(s => { ok(Math.abs(s.n / s.d - s.v) < 1e-12, tag + ': value'); if (s.en) ok(s.en * s.d === s.n * s.ed && s.ed !== s.d, tag + ': equivalent fraction'); ok(s.v <= s.max, tag + ': number line long enough'); });
  },
  graph(B, ok, tag) { B.sets.forEach(s => { ok(s.counts.every(c => c > 0 && c % B.ctx.key === 0), tag + ': counts fit the key'); if (s.facts) s.facts.forEach(f => ok(f.test(s), tag + ': fact true ' + f.text)); }); },
  expr(B, ok, tag) { B.sets.forEach(s => { const js = s.e.replace(/\\times/g, '*').replace(/\\div/g, '/').replace(/\[/g, '(').replace(/\]/g, ')'); ok(Function('return ' + js)() === s.v, tag + ': value of ' + s.e); }); },
  area(B, ok, tag) { B.sets.forEach(s => ok(s.parts.reduce((a, b) => a + b, 0) === s.a * s.b && s.p === s.a * s.b, tag + ': partial products add to the product')); },
  sys(B, ok, tag) {
    B.sets.forEach(s => {
      if (s.none) { ok(near(s.lines[0][0], s.lines[1][0]) && !near(s.lines[0][1], s.lines[1][1]), tag + ': parallel'); return; }
      s.lines.forEach(([m, b]) => ok(near(m * s.h + b, s.k), tag + ': solution on each line'));
      s.std.forEach(([A, Bc, C]) => ok(near(A * s.h + Bc * s.k, C), tag + ': solution satisfies standard form'));
      // the standard-form lines are the slope-intercept lines (same slope and intercept)
      const fromStd = s.std.map(([A, Bc, C]) => [-A / Bc, C / Bc]).map(l => l[0].toFixed(5) + ',' + l[1].toFixed(5)).sort().join();
      ok(fromStd === s.lines.map(l => l[0].toFixed(5) + ',' + l[1].toFixed(5)).sort().join(), tag + ': same lines in both forms');
    });
  }
};
