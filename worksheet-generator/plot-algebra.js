/* Algebra 1 Statistics plotting practice for plot-practice.html (2026-11-17, Algebra 1 audit #7).
   Generated items for the Statistics and Data Modeling unit: make a scatter plot from a table, draw a line of fit
   through two given data points, plot a predicted point, make a box plot and make a histogram. Each item uses a
   tool of core/plot.js ('points', 'line', 'box-plot', 'histogram'), so the check is exact; the answer key is an SVG
   drawn from the same numbers. Contexts use realistic ranges (audit #2). */
(function (G) {
  'use strict';
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[R(0, a.length - 1)]; }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = R(0, i), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  var GRID = { xmin: 0, xmax: 12, ymin: 0, ymax: 12, step: 1, snap: 1 };
  var pt = function (p) { return '(' + p[0] + ', ' + p[1] + ')'; };
  var fmt = function (v) { return String(Math.round(v * 100) / 100); };
  var svgUrl = function (w, h, body) { return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '"><rect width="100%" height="100%" fill="#fff"/>' + body + '</svg>'); };
  function gridKey(points, line, xl, yl) {
    var s = 24, o = 30, X = function (x) { return o + x * s; }, Y = function (y) { return o + (12 - y) * s; }, h = '';
    for (var i = 0; i <= 12; i++) h += '<line x1="' + X(i) + '" y1="' + Y(0) + '" x2="' + X(i) + '" y2="' + Y(12) + '" stroke="' + (i ? '#ddd' : '#333') + '"/><line x1="' + X(0) + '" y1="' + Y(i) + '" x2="' + X(12) + '" y2="' + Y(i) + '" stroke="' + (i ? '#ddd' : '#333') + '"/>' + (i % 2 === 0 ? '<text x="' + X(i) + '" y="' + (Y(0) + 14) + '" font-size="10" text-anchor="middle" font-family="Arial">' + i + '</text><text x="' + (X(0) - 6) + '" y="' + (Y(i) + 4) + '" font-size="10" text-anchor="end" font-family="Arial">' + i + '</text>' : '');
    if (line) { var x0 = 0, x1 = 12, y0 = line.m * x0 + line.b, y1 = line.m * x1 + line.b; h += '<line x1="' + X(x0) + '" y1="' + Y(y0) + '" x2="' + X(x1) + '" y2="' + Y(y1) + '" stroke="#2467a5" stroke-width="2"/>'; }
    points.forEach(function (p) { h += '<circle cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="4" fill="#c0392b"/>'; });
    h += '<text x="' + X(6) + '" y="' + (Y(0) + 28) + '" font-size="12" text-anchor="middle" font-family="Arial">' + xl + '</text><text x="12" y="' + Y(6) + '" font-size="12" font-family="Arial" transform="rotate(-90 12 ' + Y(6) + ')" text-anchor="middle">' + yl + '</text>';
    return svgUrl(12 * s + 2 * o, 12 * s + 2 * o + 10, h);
  }
  function boxKey(t, axis) {
    var X = function (v) { return 30 + (v - axis.min) / (axis.max - axis.min) * 480; }, h = '<line x1="30" y1="120" x2="510" y2="120" stroke="#333"/>';
    for (var v = axis.min; v <= axis.max; v += axis.labelEvery) h += '<line x1="' + X(v) + '" y1="116" x2="' + X(v) + '" y2="124" stroke="#333"/><text x="' + X(v) + '" y="140" font-size="11" text-anchor="middle" font-family="Arial">' + v + '</text>';
    h += '<line x1="' + X(t.min) + '" y1="70" x2="' + X(t.q1) + '" y2="70" stroke="#2467a5" stroke-width="2"/><line x1="' + X(t.q3) + '" y1="70" x2="' + X(t.max) + '" y2="70" stroke="#2467a5" stroke-width="2"/>';
    h += '<rect x="' + X(t.q1) + '" y="45" width="' + (X(t.q3) - X(t.q1)) + '" height="50" fill="#e8f0fb" stroke="#2467a5" stroke-width="2"/><line x1="' + X(t.median) + '" y1="45" x2="' + X(t.median) + '" y2="95" stroke="#2467a5" stroke-width="3"/>';
    [t.min, t.max].forEach(function (v) { h += '<line x1="' + X(v) + '" y1="58" x2="' + X(v) + '" y2="82" stroke="#2467a5" stroke-width="2"/>'; });
    h += '<text x="270" y="25" font-size="12" text-anchor="middle" font-family="Arial">min ' + t.min + ', Q1 ' + t.q1 + ', median ' + t.median + ', Q3 ' + t.q3 + ', max ' + t.max + '</text>';
    return svgUrl(540, 155, h);
  }
  function histKey(counts, bins, ymax, label) {
    var bw = 480 / bins.count, Y = function (c) { return 230 - c / ymax * 200; }, h = '<line x1="40" y1="230" x2="520" y2="230" stroke="#333"/><line x1="40" y1="30" x2="40" y2="230" stroke="#333"/>';
    for (var c = 0; c <= ymax; c++) h += '<text x="34" y="' + (Y(c) + 4) + '" font-size="10" text-anchor="end" font-family="Arial">' + c + '</text>';
    counts.forEach(function (n, i) { h += '<rect x="' + (40 + i * bw) + '" y="' + Y(n) + '" width="' + bw + '" height="' + (230 - Y(n)) + '" fill="#e8f0fb" stroke="#2467a5"/>'; });
    for (var i = 0; i <= bins.count; i++) h += '<text x="' + (40 + i * bw) + '" y="246" font-size="10" text-anchor="middle" font-family="Arial">' + (bins.start + i * bins.width) + '</text>';
    h += '<text x="280" y="264" font-size="12" text-anchor="middle" font-family="Arial">' + label + '</text>';
    return svgUrl(540, 272, h);
  }
  /* five-number summary, exclusive method (the same as core/plot.js): halves leave out the median when n is odd */
  function med(a) { var n = a.length, m = Math.floor(n / 2); return n % 2 ? a[m] : (a[m - 1] + a[m]) / 2; }
  function five(data) { var a = data.slice().sort(function (x, y) { return x - y; }), n = a.length, h = Math.floor(n / 2); return { min: a[0], q1: med(a.slice(0, h)), median: med(a), q3: med(a.slice(n % 2 ? h + 1 : h)), max: a[n - 1], sorted: a }; }
  var PAIRS = [['Hours of practice', 'Free throws made (out of 12)', 1], ['Hours studied', 'Quiz score (out of 12)', 1], ['Days absent', 'Quiz score (out of 12)', -1], ['Age of a car (years)', 'Value (thousands of dollars)', -1], ['Workers on a job', 'Days to finish the job', -1], ['Weeks of training', 'Push-ups in a row (tens)', 1]];
  var LISTS = [['Test scores', 'points', 50, 100], ['Minutes spent on homework', 'minutes', 10, 90], ['Points scored by a basketball player', 'points', 0, 40], ['Daily high temperatures', '°F', 40, 95], ['Pages read in a week', 'pages', 20, 220]];
  var FB_PTS = { position: 'Not quite. Check each point: go across to the x-value first, then up to the y-value.', 'swapped-coordinates': 'One point is at (y, x). The first number in each pair is x.', count: 'Plot one point for each row of the table.' };
  var FB_LINE = { 'same-point': 'Place two different points.', intercept: 'Your slope is right. Check where the line crosses the y-axis.', 'slope-sign': 'Your line slants the wrong way.', 'slope-reciprocal': 'You used run over rise. Slope is rise over run.', slope: 'Your line must pass through both given data points.' };
  var FB_BOX = { median: 'Check the median: order the data and find the middle value (or the mean of the two middle values).', 'mean-not-median': 'You used the mean. A box plot shows the median.', 'quartile-method': 'For Q1 and Q3, take the median of each half without the overall median when n is odd.', quartile: 'Check Q1 and Q3: they are the medians of the lower and upper halves of the ordered data.', outlier: 'There are no outliers to plot here.', whisker: 'The whiskers go to the smallest and largest values.' };
  var FB_HIST = { count: 'Every bar needs a height on the scale.', boundary: 'A value on a boundary goes in the bar that starts there. Each bar includes its left edge but not its right edge.', total: 'Your bars add up to the wrong total.', position: 'Not quite. Count how many values fall in each interval.' };
  function trendPoints(lv, dir) {
    var n = lv === 'cp2' ? 5 : lv === 'cp1' ? 6 : 8, m = dir * (R(4, 9) / 10), b = dir > 0 ? R(1, 4) : R(8, 11), xs = shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]).slice(0, n).sort(function (x, y) { return x - y; });
    var P = xs.map(function (x) { return [x, Math.max(0, Math.min(12, Math.round(m * x + b + R(-1, 1))))]; });
    return P;
  }
  var MAKERS = {
    scatter: ['Make a scatter plot from a table', function (lv) {
      var c = pick(PAIRS), P = trendPoints(lv, c[2]), keys = {}; if (P.some(function (p) { var k = p.join(); if (keys[k]) return true; keys[k] = 1; return false; })) return null;
      return { prompt: 'The table shows ' + c[0].toLowerCase() + ' (x) and ' + c[1].toLowerCase() + ' (y): ' + P.map(pt).join(', ') + '. Make a scatter plot of the data.', tool: 'points', target: { points: P }, feedback: FB_PTS,
        key: gridKey(P, null, c[0], c[1]), alt: 'Scatter plot with points ' + P.map(pt).join(', ') + '.', steps: ['Each ordered pair (x, y) is one point: go across to x, then up to y.', 'The points ' + (c[2] > 0 ? 'rise' : 'fall') + ' from left to right, so the association is ' + (c[2] > 0 ? 'positive' : 'negative') + '.'] };
    }],
    'line-of-fit': ['Draw a line of fit through two data points', function (lv) {
      var c = pick(PAIRS), P = trendPoints(lv === 'cp2' ? 'cp1' : lv, c[2]), A = P[0], B = P[P.length - 1]; if (A[0] === B[0] || A[1] === B[1]) return null;
      var m = (B[1] - A[1]) / (B[0] - A[0]), b = A[1] - m * A[0];
      var mFr = (function () { var n = B[1] - A[1], d = B[0] - A[0], g = function (x, y) { return y ? g(y, x % y) : Math.abs(x); }, k = g(n, d); n /= k; d /= k; if (d < 0) { n = -n; d = -d; } return d === 1 ? String(n) : n + '/' + d; })();
      var bFr = (function () { var n = A[1] * (B[0] - A[0]) - (B[1] - A[1]) * A[0], d = B[0] - A[0], g = function (x, y) { return y ? g(y, x % y) : Math.abs(x); }, k = g(n, d) || 1; n /= k; d /= k; if (d < 0) { n = -n; d = -d; } return d === 1 ? String(n) : n + '/' + d; })();
      return { prompt: 'Data on ' + c[0].toLowerCase() + ' (x) and ' + c[1].toLowerCase() + ' (y): ' + P.map(pt).join(', ') + '. Draw a line of fit through the first and last data points, ' + pt(A) + ' and ' + pt(B) + '.', tool: 'line', target: { m: mFr, b: bFr }, feedback: FB_LINE,
        key: gridKey(P, { m: m, b: b }, c[0], c[1]), alt: 'Scatter plot with a line of fit through ' + pt(A) + ' and ' + pt(B) + '.', steps: ['Slope: (' + B[1] + ' − ' + A[1] + ') ÷ (' + B[0] + ' − ' + A[0] + ') = ' + fmt(m) + '.', 'Plot both points and draw the line through them: y = ' + fmt(m) + 'x + ' + fmt(b) + ' (rounded).'] };
    }],
    predict: ['Plot a predicted value from a line of fit', function (lv) {
      var c = pick(PAIRS), mm = c[2] * pick(lv === 'cp2' ? [1, 2] : [0.5, 1, 1.5, 2]), b = c[2] > 0 ? R(0, 3) : R(9, 12), x = R(1, 11), y = mm * x + b;
      if (y < 0 || y > 12 || y !== Math.round(y)) return null;
      return { prompt: 'A line of fit for ' + c[1].toLowerCase() + ' (y) against ' + c[0].toLowerCase() + ' (x) is y = ' + mm + 'x ' + (b >= 0 ? '+ ' + b : '− ' + -b) + '. Plot the predicted point for x = ' + x + '.', tool: 'points', target: { points: [[x, y]] }, feedback: FB_PTS,
        key: gridKey([[x, y]], { m: mm, b: b }, c[0], c[1]), alt: 'The predicted point ' + pt([x, y]) + ' on the line of fit.', steps: ['Substitute x = ' + x + ': y = ' + mm + '(' + x + ') + ' + b + ' = ' + y + '.', 'Plot ' + pt([x, y]) + '.'] };
    }],
    'box-plot': ['Make a box plot from a data set', function (lv) {
      var L = pick(LISTS), n = lv === 'cp2' ? 7 : lv === 'cp1' ? R(8, 11) : R(10, 13), d = []; for (var i = 0; i < n; i++) d.push(R(L[2], L[3]));
      var t = five(d), span = L[3] - L[2], le = span > 100 ? 20 : span > 50 ? 10 : 5, axis = { min: Math.floor(L[2] / le) * le, max: Math.ceil(L[3] / le) * le, step: 1, labelEvery: le, snap: 0.5, label: L[1] };
      return { prompt: L[0] + ' (' + L[1] + '): ' + d.join(', ') + '. Make a box plot.', tool: 'box-plot', target: { data: d }, extra: { axis: axis, outlierRule: false, title: L[0], source: { type: 'list', values: t.sorted } }, feedback: FB_BOX,
        key: boxKey(t, axis), alt: 'Box plot: minimum ' + t.min + ', Q1 ' + t.q1 + ', median ' + t.median + ', Q3 ' + t.q3 + ', maximum ' + t.max + '.',
        steps: ['Order the ' + n + ' values: ' + t.sorted.join(', ') + '.', 'Median: ' + t.median + '. Q1 (median of the lower half): ' + t.q1 + '. Q3 (median of the upper half): ' + t.q3 + '.', 'Whiskers go to the minimum ' + t.min + ' and maximum ' + t.max + '.'] };
    }],
    histogram: ['Make a histogram from a data set', function (lv) {
      var L = pick(LISTS), n = lv === 'cp2' ? 12 : lv === 'cp1' ? 16 : 20, w = (L[3] - L[2]) > 100 ? 40 : (L[3] - L[2]) > 50 ? 10 : 10, start = Math.floor(L[2] / w) * w, count = Math.ceil((L[3] - start + 1) / w), d = [];
      for (var i = 0; i < n; i++) d.push(R(L[2], L[3]));
      var counts = Array(count).fill(0); d.forEach(function (v) { counts[Math.floor((v - start) / w)]++; }); var ymax = Math.max(6, Math.max.apply(null, counts) + 1);
      return { prompt: L[0] + ' (' + L[1] + '): ' + d.join(', ') + '. Make a histogram with bins of width ' + w + ' starting at ' + start + '. Each bin includes its left edge but not its right edge.', tool: 'histogram', target: { data: d },
        extra: { title: L[0], bins: { start: start, width: w, count: count, closed: 'left' }, valueAxis: { label: 'Frequency', min: 0, max: ymax, step: 1, snap: 1 }, categoryLabel: L[1], source: { type: 'list', values: d } }, feedback: FB_HIST,
        key: histKey(counts, { start: start, count: count, width: w }, ymax, L[1]), alt: 'Histogram with counts ' + counts.join(', ') + '.',
        steps: ['Bins: ' + counts.map(function (c, i) { return (start + i * w) + ' to under ' + (start + (i + 1) * w); }).join('; ') + '.', 'Counts: ' + counts.join(', ') + '. Check: they add to ' + n + '.'] };
    }]
  };
  function item(id, skillId, r) {
    var plot = Object.assign({ tool: r.tool, target: r.target, feedback: r.feedback, answerKey: { svg: r.key, alt: r.alt }, check: { type: r.tool === 'histogram' ? 'exact' : 'exact-after-snap' } }, r.tool === 'points' || r.tool === 'line' ? { grid: GRID, labels: r.tool === 'points' ? r.target.points.map(function () { return ''; }) : undefined } : {}, r.extra || {});
    return { id: id, skillId: skillId, prompt: r.prompt, solutionSteps: r.steps, plot: plot };
  }
  G.MK_A1_PLOT = {
    units: ['statistics-data-modeling'],
    skills: function () { return Object.keys(MAKERS).map(function (k) { return { id: k, name: MAKERS[k][0] }; }); },
    pool: function (unitId, level, skillId, n) {
      if (this.units.indexOf(unitId) < 0) return [];
      var ids = skillId ? [skillId] : Object.keys(MAKERS), out = [], seen = {}, tries = 0;
      while (out.length < (n || 12) && tries++ < 600) {
        var id = ids[out.length % ids.length], r = MAKERS[id] && MAKERS[id][1](level || 'cp1'); if (!r || seen[r.prompt]) continue; seen[r.prompt] = 1;
        out.push(item('a1-plot-' + id + '-' + out.length, id, r));
      }
      return out;
    }
  };
})(typeof window !== 'undefined' ? window : globalThis);
