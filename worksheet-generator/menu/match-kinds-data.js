/* Matching kind "data": one data set shown four ways.
     6th Grade, Algebra 1:   dot plot ↔ histogram ↔ box plot ↔ summary statistics
     Pre-Algebra, Statistics: stem-and-leaf plot ↔ histogram ↔ box plot ↔ summary statistics
   All displays in one activity share one number line, so cards can be compared side by side. Quartiles use the
   median of each half (the median itself is left out when the count is odd), as in the courses' lessons.
   Every display is computed from the data; the builder rejects a set whose histogram, box plot or summary would
   also fit another set, so each card fits exactly one data set.
   Needs: menu/match-kinds.js. */
(function (G) {
  'use strict';
  var MK = G.MKMATCH, U = MK.util, SV = MK.svg, k = U.k;
  function stats(v) {
    var s = v.slice().sort(function (a, b) { return a - b; }), n = s.length, half = Math.floor(n / 2);
    var lower = s.slice(0, half), upper = s.slice(n % 2 ? half + 1 : half);
    var mean = s.reduce(function (a, b) { return a + b; }, 0) / n;
    var cnt = {}; s.forEach(function (x) { cnt[x] = (cnt[x] || 0) + 1; });
    var top = Math.max.apply(null, Object.keys(cnt).map(function (x) { return cnt[x]; })), modes = Object.keys(cnt).filter(function (x) { return cnt[x] === top; }).map(Number);
    var q1 = U.median(lower), q3 = U.median(upper), iqr = q3 - q1;
    var mad = s.reduce(function (a, x) { return a + Math.abs(x - mean); }, 0) / n;
    var sd = Math.sqrt(s.reduce(function (a, x) { return a + (x - mean) * (x - mean); }, 0) / (n - 1));
    var out = s.filter(function (x) { return x < q1 - 1.5 * iqr || x > q3 + 1.5 * iqr; });
    return { s: s, n: n, min: s[0], max: s[n - 1], med: U.median(s), q1: q1, q3: q3, iqr: iqr, range: s[n - 1] - s[0], mean: mean, mode: top > 1 && modes.length === 1 ? modes[0] : null, mad: mad, sd: sd, outliers: out };
  }
  MK.dataStats = stats;
  function n1(v) { return U.isInt(v) ? String(Math.round(v)) : String(U.round(v, 2)); }
  /* summary facts: each is a sentence and a test on any data set */
  var FACTS = {
    med: { lv: 0, make: function (t) { return { text: 'The median is ' + U.m(n1(t.med)) + '.', test: function (u) { return U.near(u.med, t.med); } }; } },
    range: { lv: 0, make: function (t) { return { text: 'The range is ' + U.m(n1(t.range)) + '.', test: function (u) { return U.near(u.range, t.range); } }; } },
    mode: { lv: 0, make: function (t) { return t.mode === null ? null : { text: 'The mode is ' + U.m(n1(t.mode)) + '.', test: function (u) { return u.mode !== null && U.near(u.mode, t.mode); } }; } },
    min: { lv: 0, make: function (t) { return { text: 'The least value is ' + U.m(n1(t.min)) + '.', test: function (u) { return U.near(u.min, t.min); } }; } },
    max: { lv: 0, make: function (t) { return { text: 'The greatest value is ' + U.m(n1(t.max)) + '.', test: function (u) { return U.near(u.max, t.max); } }; } },
    n: { lv: 0, make: function (t) { return { text: 'There are ' + U.m(t.n) + ' data values.', test: function (u) { return u.n === t.n; } }; } },
    mean: { lv: 1, make: function (t) { return !U.isInt(t.mean * 10) ? null : { text: 'The mean is ' + U.m(n1(t.mean)) + '.', test: function (u) { return U.near(u.mean, t.mean); } }; } },
    iqr: { lv: 1, make: function (t) { return { text: 'The interquartile range is ' + U.m(n1(t.iqr)) + '.', test: function (u) { return U.near(u.iqr, t.iqr); } }; } },
    q: { lv: 1, make: function (t) { return { text: 'The first quartile is ' + U.m(n1(t.q1)) + ' and the third quartile is ' + U.m(n1(t.q3)) + '.', test: function (u) { return U.near(u.q1, t.q1) && U.near(u.q3, t.q3); } }; } },
    mad: { lv: 2, only: /math6/, make: function (t) { return !U.isInt(t.mad * 10) ? null : { text: 'The mean absolute deviation is ' + U.m(n1(t.mad)) + '.', test: function (u) { return U.near(u.mad, t.mad); } }; } },
    sd: { lv: 2, only: /statistics|algebra1/, make: function (t) { var r = U.round(t.sd, 1); return { text: 'The standard deviation is about ' + U.m(r.toFixed(1)) + '.', test: function (u) { return U.near(U.round(u.sd, 1), r); } }; } },
    out: { lv: 2, only: /statistics|algebra1/, make: function (t) { var o = t.outliers; return { text: o.length ? 'It has ' + (o.length === 1 ? 'one outlier, ' + U.m(n1(o[0])) : 'outliers at ' + o.map(function (x) { return U.m(n1(x)); }).join(' and ')) + ' (1.5 × IQR rule).' : 'It has no outliers (1.5 × IQR rule).', test: function (u) { return u.outliers.join() === o.join(); } }; } }
  };
  function chooseFacts(set, sets, rng, L, unit) {
    var lv = L === 'cp2' ? 0 : L === 'cp1' ? 1 : 2, t = set.st;
    var avail = Object.keys(FACTS).filter(function (id) { var F = FACTS[id]; return F.lv <= lv && (!F.only || F.only.test(unit)); });
    var made = {}; avail.forEach(function (id) { var f = FACTS[id].make(t); if (f && f.test(t)) made[id] = f; });
    var ids = Object.keys(made), pref = ids.filter(function (id) { return FACTS[id].lv === lv; });
    for (var tries = 0; tries < 80; tries++) {
      var size = rng.pick([2, 2, 3]), pick = rng.shuffle(pref.length ? [rng.pick(pref)] : []).concat(rng.shuffle(ids)).filter(function (x, i, a) { return a.indexOf(x) === i; }).slice(0, size);
      if (pick.length < 2) continue;
      if (pick.indexOf('min') >= 0 && pick.indexOf('max') >= 0 && pick.indexOf('range') >= 0) continue;
      var fs = pick.map(function (id) { return made[id]; });
      if (sets.every(function (o) { return o === set || !fs.every(function (f) { return f.test(o.st); }); })) return fs;
    }
    return null;
  }
  function histOf(v, edges) { return edges.slice(0, -1).map(function (e, i) { var last = i === edges.length - 2; return v.filter(function (x) { return x >= e && (x < edges[i + 1] || (last && x <= edges[i + 1])); }).length; }); }
  function stemLeaf(s, stems) {
    return stems.map(function (st) { return [st, s.filter(function (x) { return Math.floor(x / 10) === st; }).map(function (x) { return x % 10; })]; });
  }
  MK.register({
    id: 'data', name: 'Data Display Matching', short: 'Data Displays', noun: 'data set', anchor: 'dot',
    anchorText: 'Start with each data set already in its set', anchorHint: 'Recommended: the dot plot (or stem-and-leaf plot) shows every value; students find the displays and summary that match it.',
    blurb: 'Match each data set’s <b>dot plot</b> (or stem-and-leaf plot) to its <b>histogram</b>, <b>box plot</b> and <b>summary statistics</b>. All displays share one scale. Look-alike data sets share a median, a range or a shape, so students must compute to be sure.',
    tip: 'From the full data, find the five-number summary (least value, first quartile, median, third quartile, greatest value) for the box plot, and count how many values fall in each interval for the histogram.',
    types: [{ id: 'dot', L: 'P', name: 'Dot plot', plural: 'Dot plots' }, { id: 'stem', L: 'L', name: 'Stem-and-leaf plot', plural: 'Stem-and-leaf' }, { id: 'hist', L: 'H', name: 'Histogram', plural: 'Histograms' }, { id: 'box', L: 'B', name: 'Box plot', plural: 'Box plots' }, { id: 'stats', L: 'S', name: 'Summary', plural: 'Summaries' }],
    units: {
      'math6-data-displays': { types: ['dot', 'hist', 'box', 'stats'] },
      'algebra1-statistics-data-modeling': { types: ['dot', 'hist', 'box', 'stats'] },
      'prealgebra7-data-analysis-probability': { types: ['stem', 'hist', 'box', 'stats'], anchor: 'stem' },
      'statistics-exploring-data': { types: ['stem', 'hist', 'box', 'stats'], anchor: 'stem' }
    },
    maxSets: 8, setOptions: [4, 6, 8], genTypes: ['dot', 'hist', 'box'],
    context: function (rng, L, cfg) {
      var stem = cfg.types.indexOf('stem') >= 0;
      if (stem) { var lo = rng.pick([10, 20, 30]), w = rng.pick([5, 10]); return { stem: true, ax: { lo: lo, hi: lo + 40, step: 1, labelEvery: 5 }, edges: [0, 1, 2, 3, 4, 5, 6, 7, 8].filter(function (i) { return i * w <= 40; }).map(function (i) { return lo + i * w; }), stems: [0, 1, 2, 3].map(function (i) { return lo / 10 + i; }) }; }
      var span = L === 'cp2' ? 12 : 20, lo2 = rng.pick([0, 0, 10, 20]), bw = span === 12 ? rng.pick([2, 3]) : rng.pick([2, 4, 5]);
      return { stem: false, ax: { lo: lo2, hi: lo2 + span, step: 1, labelEvery: span > 12 ? 2 : 1 }, edges: Array.from({ length: span / bw + 1 }, function (_, i) { return lo2 + i * bw; }) };
    },
    gen: function (rng, L, cfg, Un, sets) {
      var C = cfg.ctx, ax = C.ax, span = ax.hi - ax.lo, n = L === 'cp2' ? rng.int(9, 12) : L === 'cp1' ? rng.int(12, 16) : rng.int(15, 20);
      if (C.stem) n = L === 'cp2' ? rng.int(10, 13) : rng.int(13, 19);
      var shape = rng.pick(['mound', 'right', 'left', 'flat', 'two', 'outlier']), c = ax.lo + span * (0.3 + 0.4 * rng.next()), sp = span * (0.12 + 0.12 * rng.next()), v = [];
      for (var i = 0; i < n; i++) {
        var u = rng.next(), x;
        if (shape === 'mound') x = c + (rng.next() + rng.next() + rng.next() - 1.5) * sp * 1.6;
        else if (shape === 'right') x = ax.lo + span * 0.15 + u * u * span * 0.75;
        else if (shape === 'left') x = ax.hi - span * 0.15 - u * u * span * 0.75;
        else if (shape === 'flat') x = c - sp * 1.5 + u * sp * 3;
        else if (shape === 'two') x = (rng.next() < 0.5 ? ax.lo + span * 0.28 : ax.lo + span * 0.72) + (rng.next() - 0.5) * sp;
        else x = i === 0 ? (rng.next() < 0.5 ? ax.lo + 1 : ax.hi - 1) : c + (rng.next() + rng.next() - 1) * sp;
        v.push(Math.max(ax.lo + 1, Math.min(ax.hi - 1, Math.round(x))));
      }
      var st = stats(v);
      if (st.range < 4 || st.iqr <= 0) return null;
      var hist = histOf(st.s, C.edges);
      if (hist.filter(Boolean).length < 2) return null;
      return { v: st.s, st: st, hist: hist, five: [st.min, st.q1, st.med, st.q3, st.max], shape: shape };
    },
    finish: function (sets, rng, L, cfg) {
      var ymax = Math.max.apply(null, sets.map(function (s) { return Math.max.apply(null, s.hist); }));
      for (var i = 0; i < sets.length; i++) { sets[i].ymax = ymax; if (cfg.types.indexOf('stats') >= 0) { sets[i].facts = chooseFacts(sets[i], sets, rng, L, cfg.unit); if (!sets[i].facts) return false; } }
      return true;
    },
    fits: function (t, a, b) {
      if (t === 'dot' || t === 'stem') return a.v.join() === b.v.join();
      if (t === 'hist') return a.hist.join() === b.hist.join();
      if (t === 'box') return a.five.join() === b.five.join();
      if (t === 'stats') return !!a.facts && a.facts.every(function (f) { return f.test(b.st); });
      return false;
    },
    face: function (s, t, mode, B) {
      var C = B.ctx;
      if (t === 'dot') return SV.dotPlot(s.v, C.ax);
      if (t === 'hist') return SV.histogram(C.edges, s.hist, C.ax, s.ymax);
      if (t === 'box') return SV.boxPlot(s.five, C.ax);
      if (t === 'stem') return '<table class="mk-tt mk-stem"><tr><th>Stem</th><th>Leaf</th></tr>' + stemLeaf(s.v, C.stems).map(function (r) { return '<tr><td>' + r[0] + '</td><td class="lf">' + (r[1].join(' ') || '&nbsp;') + '</td></tr>'; }).join('') + '</table><div class="mk-key">Key: ' + C.stems[1] + ' | 4 means ' + (C.stems[1] * 10 + 4) + '</div>';
      return '<div class="mk-txt left">' + s.facts.map(function (f) { return '<p>' + U.mt(f.text) + '</p>'; }).join('') + '</div>';
    },
    summary: function (s) { return k('\\text{median } ' + n1(s.st.med) + ',\\ \\text{IQR } ' + n1(s.st.iqr)); },
    noGrid: true, wide: ['dot', 'hist', 'box'], printCols: { dot: 2, hist: 2, box: 2, stats: 3, stem: 3 }, printRows: { dot: 4, hist: 4, box: 5 }
  });
})(typeof window !== 'undefined' ? window : globalThis);
