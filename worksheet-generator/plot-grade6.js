/* Grade 6 graphing practice for plot-practice.html (2026-11-19, Grade 6 audit #11).
   Generated items for three Grade 6 units that had no graphing practice: plot the pairs of a ratio table and graph the
   unit-rate line (Ratios, Rates, Percent); plot the (x, y) pairs of an equation with a dependent and an independent
   variable and graph the line (Expressions and Equations); and draw polygons on the coordinate plane from side lengths
   (Geometry). Items use the 'points' and 'line' tools of core/plot.js, so the check is exact; every target is on the snap
   grid, and the answer key is an SVG drawn from the same numbers. */
(function (G) {
  'use strict';
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[R(0, a.length - 1)]; }
  var M = function (v) { return String(v).replace('-', '−'); };
  var pt = function (p) { return '(' + M(p[0]) + ', ' + M(p[1]) + ')'; };
  var GRID = { xmin: -10, xmax: 10, ymin: -10, ymax: 10, step: 1, snap: 1 };
  var QGRID = { xmin: 0, xmax: 12, ymin: 0, ymax: 12, step: 1, snap: 1 };
  var Q20 = { xmin: 0, xmax: 10, ymin: 0, ymax: 20, step: 1, snap: 1 };
  var FB_PTS = { position: 'Not quite. Check each point: move across first (x), then up (y).', 'swapped-coordinates': 'One point is at (y, x). The first number is x.', count: 'Check how many points you need to place.' };
  var FB_LINE = { 'same-point': 'Place two different points.', intercept: 'Check where the line crosses the y-axis: what is y when x = 0?', 'slope-sign': 'Your line slants the wrong way.',
    'slope-reciprocal': 'You used x over y. Find how much y grows when x grows by 1.', slope: 'Check the rate: when x grows by 1, how much does y grow?' };
  var svg = function (w, h, body) { return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '"><rect width="100%" height="100%" fill="#fff"/>' + body + '</svg>'); };
  function gridKey(g, points, labels, opts) {
    opts = opts || {};
    var s = g.xmin < 0 ? 14 : (g.ymax > 12 ? 16 : 24), W = (g.xmax - g.xmin) * s + 90, H = (g.ymax - g.ymin) * s + 40, X = function (x) { return 20 + (x - g.xmin) * s; }, Y = function (y) { return 20 + (g.ymax - y) * s; }, h = '';
    for (var i = g.xmin; i <= g.xmax; i++) h += '<line x1="' + X(i) + '" y1="' + Y(g.ymin) + '" x2="' + X(i) + '" y2="' + Y(g.ymax) + '" stroke="' + (i ? '#ddd' : '#333') + '"/>';
    for (var j = g.ymin; j <= g.ymax; j++) h += '<line x1="' + X(g.xmin) + '" y1="' + Y(j) + '" x2="' + X(g.xmax) + '" y2="' + Y(j) + '" stroke="' + (j ? '#ddd' : '#333') + '"/>';
    if (opts.poly) h += '<polygon points="' + opts.poly.map(function (p) { return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '" fill="#4f81bd" fill-opacity="0.15" stroke="#2467a5" stroke-width="2"/>';
    if (opts.line) { var m = opts.line[0], b = opts.line[1], x2 = Math.min(g.xmax, (g.ymax - b) / m); h += '<line x1="' + X(0) + '" y1="' + Y(b) + '" x2="' + X(x2) + '" y2="' + Y(b + m * x2) + '" stroke="#2467a5" stroke-width="2.5"/>'; }
    points.forEach(function (p, k) { h += '<circle cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="5" fill="#c0392b"/>' + (labels[k] ? '<text x="' + (X(p[0]) + 7) + '" y="' + (Y(p[1]) - 7) + '" font-size="13" font-family="Arial" font-weight="bold">' + labels[k] + '</text>' : ''); });
    return svg(W, H, h);
  }
  var frac = function (n, d) { var a = Math.abs(n), b = d; while (b) { var t = a % b; a = b; b = t; } return d / a === 1 ? String(n / a) : (n / a) + '/' + (d / a); };
  var CTX = [['cups of flour', 'cups of milk'], ['minutes', 'laps'], ['tickets', 'dollars'], ['packs', 'pencils'], ['hours', 'miles'], ['batches', 'eggs']];
  var MAKERS = {
    'ratios-rates-percent-proportions': {
      'ratio-table': ['Plot the pairs in a ratio table', function (lv) {
        var c = pick(CTX), a = lv === 'cp2' ? 1 : R(2, 3), b = lv === 'cp2' ? R(2, 3) : R(1, 4);
        if (a === b) return null;
        var n = lv === 'cp2' ? 3 : 4, xs = [], ys = [];
        for (var k = 1; k <= n; k++) { xs.push(a * k); ys.push(b * k); }
        if (xs[n - 1] > 12 || ys[n - 1] > 12) return null;
        var ps = xs.map(function (x, k) { return [x, ys[k]]; }), shown = ps, prompt;
        if (lv === 'honors') { shown = ps.slice(0, 2); prompt = 'The ratio of ' + c[0] + ' to ' + c[1] + ' is ' + a + ' to ' + b + '. Complete a ratio table with ' + n + ' equivalent ratios, starting with ' + a + ' to ' + b + ', and plot every pair (' + c[0] + ', ' + c[1] + ').'; }
        else prompt = 'The ratio table shows ' + c[0] + ' (x): ' + xs.join(', ') + ' and ' + c[1] + ' (y): ' + ys.join(', ') + '. Plot each pair (x, y).';
        return { prompt: prompt, tool: 'points', grid: QGRID, labels: ps.map(function () { return ''; }), target: { points: ps }, feedback: FB_PTS,
          key: gridKey(QGRID, ps, ps.map(function () { return ''; }), { line: [b / a, 0] }), alt: 'First-quadrant grid with the points ' + ps.map(pt).join(', ') + ' on a line through the origin.',
          steps: ['Each pair is (' + c[0] + ', ' + c[1] + ').'].concat(lv === 'honors' ? ['Multiply both numbers of ' + a + ' : ' + b + ' by 1, 2, 3 and 4.'] : []).concat(['Points: ' + ps.map(pt).join(', ') + '.', 'The points line up with the origin because every pair has the same ratio.']) };
      }],
      'unit-rate-line': ['Graph a unit rate', function (lv) {
        var c = pick(CTX), k, prompt;
        if (lv === 'cp2') { k = R(2, 5); prompt = 'Each of the ' + c[0] + ' goes with ' + k + ' ' + c[1] + '. Graph y = ' + k + 'x, where x is ' + c[0] + ' and y is ' + c[1] + '.'; }
        else if (lv === 'cp1') { var x0 = R(2, 4); k = R(2, 4); prompt = x0 + ' ' + c[0] + ' go with ' + x0 * k + ' ' + c[1] + '. Find the unit rate and graph the relationship, with x = ' + c[0] + ' and y = ' + c[1] + '.'; }
        else { k = pick([0.5, 1.5, 2.5]); var x1 = 4; prompt = x1 + ' ' + c[0] + ' go with ' + x1 * k + ' ' + c[1] + '. Graph the relationship, with x = ' + c[0] + ' and y = ' + c[1] + '. The unit rate is not a whole number.'; }
        var kF = k % 1 ? frac(k * 2, 2) : String(k), p2 = k % 1 ? [2, 2 * k] : [1, k];
        return { prompt: prompt, tool: 'line', grid: QGRID, target: { m: kF, b: '0' }, feedback: FB_LINE, key: gridKey(QGRID, [[0, 0], p2], ['', ''], { line: [k, 0] }),
          alt: 'Line y = ' + kF + 'x through the origin on a first-quadrant grid.',
          steps: ['The unit rate is ' + kF + ' ' + c[1] + ' for each one of the ' + c[0] + ', so y = ' + kF + 'x.', 'The line passes through (0, 0) and ' + pt(p2) + '.', 'Draw the line through those two points.'] };
      }]
    },
    'expressions-equations': {
      'table-points': ['Plot pairs from an equation', function (lv) {
        var m = R(1, lv === 'cp2' ? 3 : 4), b = lv === 'cp2' ? 0 : R(1, 5), xs = lv === 'honors' ? [0, 1, 2, 3, 4] : [0, 1, 2, 3], v = pick([['n', 'c'], ['h', 'p'], ['t', 'd'], ['x', 'y']]);
        var ps = xs.map(function (x) { return [x, m * x + b]; });
        if (ps[ps.length - 1][1] > 20) return null;
        var eq = v[1] + ' = ' + (m === 1 ? '' : m) + v[0] + (b ? ' + ' + b : '');
        return { prompt: 'The equation ' + eq + ' gives the dependent variable ' + v[1] + ' for the independent variable ' + v[0] + '. Plot the pairs (' + v[0] + ', ' + v[1] + ') for ' + v[0] + ' = ' + xs.join(', ') + '.', tool: 'points', grid: Q20,
          labels: ps.map(function () { return ''; }), target: { points: ps }, feedback: FB_PTS, key: gridKey(Q20, ps, ps.map(function () { return ''; }), { line: [m, b] }),
          alt: 'Grid with the points ' + ps.map(pt).join(', ') + '.', steps: ['Substitute each value of ' + v[0] + ' into ' + eq + '.'].concat(ps.map(function (p) { return v[0] + ' = ' + p[0] + ': ' + v[1] + ' = ' + (m === 1 ? '' : m + ' × ') + p[0] + (b ? ' + ' + b : '') + ' = ' + p[1] + '.'; })) };
      }],
      'graph-equation': ['Graph an equation in two variables', function (lv) {
        var m = R(1, 3), b = lv === 'cp2' ? 0 : R(2, 6), c = pick([['weeks', 'dollars saved'], ['hours', 'dollars earned'], ['minutes', 'cm of water'], ['days', 'pages read']]), prompt, x2 = R(2, 4);
        if (lv === 'honors') { prompt = 'Let x be the number of ' + c[0] + ' and y the ' + c[1] + '. y starts at ' + b + ' when x = 0 and is ' + (b + m * x2) + ' when x = ' + x2 + ', growing by the same amount for each 1 added to x. Graph the relationship.'; }
        else prompt = 'Graph y = ' + (m === 1 ? '' : m) + 'x' + (b ? ' + ' + b : '') + ', where x is ' + c[0] + ' and y is ' + c[1] + '.';
        return { prompt: prompt, tool: 'line', grid: Q20, target: { m: String(m), b: String(b) }, feedback: FB_LINE, key: gridKey(Q20, [[0, b], [1, b + m]], ['', ''], { line: [m, b] }),
          alt: 'Line y = ' + m + 'x + ' + b + ' starting at (0, ' + b + ').',
          steps: (lv === 'honors' ? ['It grows by (' + (b + m * x2) + ' − ' + b + ') ÷ ' + x2 + ' = ' + m + ' for each one of the ' + c[0] + ', so y = ' + m + 'x + ' + b + '.'] : []).concat(['When x = 0, y = ' + b + ': the point (0, ' + b + ').', 'When x = 1, y = ' + (b + m) + ': the point (1, ' + (b + m) + ').', 'Draw the line through those points.']) };
      }]
    },
    'geometry': {
      'draw-rectangle': ['Draw a rectangle from its side lengths', function (lv) {
        var A = [R(-8, 2), R(-8, 2)], w = R(3, 8), h = R(2, 7);
        if (w === h) return null;
        var B = [A[0] + w, A[1]], C = [A[0] + w, A[1] + h], D = [A[0], A[1] + h];
        if ([B, C, D].some(function (p) { return Math.abs(p[0]) > 10 || Math.abs(p[1]) > 10; })) return null;
        var ask = lv === 'honors' ? ' Its area is ' + w * h + ' square units and side PQ is ' + w + ' units long.' : ' Side PQ is ' + w + ' units long and side QR is ' + h + ' units long.';
        return { prompt: 'Rectangle PQRS has P at ' + pt(A) + '. Q is to the right of P and R is above Q.' + ask + ' Plot Q, R and S (one dot on each corner, in any order).', tool: 'points', grid: GRID, labels: ['Q', 'R', 'S'], target: { points: [B, C, D] }, feedback: FB_PTS,
          key: gridKey(GRID, [A, B, C, D], ['P', 'Q', 'R', 'S'], { poly: [A, B, C, D] }), alt: 'Rectangle PQRS with P' + pt(A) + ', Q' + pt(B) + ', R' + pt(C) + ', S' + pt(D) + '.',
          steps: (lv === 'honors' ? ['QR = area ÷ PQ = ' + w * h + ' ÷ ' + w + ' = ' + h + ' units.'] : []).concat(['Q is ' + w + ' units right of P: Q = ' + pt(B) + '.', 'R is ' + h + ' units above Q: R = ' + pt(C) + '.', 'S is above P and level with R: S = ' + pt(D) + '.']) };
      }],
      'reflect-vertex': ['Complete a polygon by reflecting', function (lv) {
        var a = [R(1, 7), R(1, 7)], axis = lv === 'cp2' ? 'y' : pick(['x', 'y']);
        var B = axis === 'y' ? [-a[0], a[1]] : [a[0], -a[1]];
        var C = lv === 'honors' ? [-a[0], -a[1]] : null;
        var tgt = C ? [B, C, [a[0], -a[1]].toString() === B.toString() ? [-a[0], a[1]] : [a[0], -a[1]]] : [B];
        var labels = C ? ['Q', 'R', 'S'] : ['Q'];
        var prompt = C ? 'Point P is at ' + pt(a) + '. Q is P reflected across the ' + axis + '-axis, R is P reflected across both axes, and S completes rectangle PQRS. Plot Q, R and S (one dot on each, in any order), then find the perimeter.'
          : 'Point P is at ' + pt(a) + '. Plot Q, the reflection of P across the ' + axis + '-axis, and find the distance PQ.';
        var dist = axis === 'y' ? 2 * a[0] : 2 * a[1];
        return { prompt: prompt, tool: 'points', grid: GRID, labels: labels, target: { points: tgt }, feedback: FB_PTS,
          key: gridKey(GRID, [a].concat(tgt), ['P'].concat(labels), C ? { poly: [a, tgt[0], tgt[1], tgt[2]] } : {}), alt: 'Point P' + pt(a) + ' and ' + tgt.map(function (p, k) { return labels[k] + pt(p); }).join(', ') + '.',
          steps: ['Reflecting across the ' + axis + '-axis changes the sign of ' + (axis === 'y' ? 'x' : 'y') + ': Q = ' + pt(B) + '.', 'PQ = ' + (axis === 'y' ? '|' + a[0] + '| + |' + M(-a[0]) + '|' : '|' + a[1] + '| + |' + M(-a[1]) + '|') + ' = ' + dist + ' units.']
            .concat(C ? ['R = ' + pt(tgt[1]) + ' and S = ' + pt(tgt[2]) + '.', 'Perimeter = 2(' + 2 * a[0] + ' + ' + 2 * a[1] + ') = ' + 2 * (2 * a[0] + 2 * a[1]) + ' units.'] : []) };
      }]
    }
  };
  function item(id, skillId, r) {
    var plot = { tool: r.tool, target: r.target, feedback: r.feedback, answerKey: { svg: r.key, alt: r.alt }, check: { type: 'exact-after-snap' } };
    if (r.grid) plot.grid = r.grid;
    if (r.labels) plot.labels = r.labels;
    return { id: id, skillId: skillId, prompt: r.prompt, solutionSteps: r.steps, plot: plot };
  }
  G.MK_G6_PLOT = {
    units: Object.keys(MAKERS),
    makers: MAKERS,
    skills: function (unitId) { var m = MAKERS[unitId] || {}; return Object.keys(m).map(function (k) { return { id: k, name: m[k][0] }; }); },
    pool: function (unitId, level, skillId, n) {
      var m = MAKERS[unitId]; if (!m) return [];
      var ids = skillId ? [skillId] : Object.keys(m), out = [], seen = {}, tries = 0;
      while (out.length < (n || 12) && tries++ < 3000) {
        var id = ids[out.length % ids.length], r = m[id] && m[id][1](level || 'cp1'); if (!r || seen[r.prompt]) continue; seen[r.prompt] = 1;
        out.push(item('g6-plot-' + id + '-' + out.length, id, r));
      }
      return out;
    }
  };
})(typeof window !== 'undefined' ? window : globalThis);
