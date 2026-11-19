/* Grade 7 graphing practice for plot-practice.html (2026-11-19, Grade 7 audit #14).
   Generated items for four Grade 7 (Pre-Algebra) units that had no graphing practice: plot points in all four quadrants
   and find a missing rectangle corner; solve a one-step inequality and graph it; graph a proportional relationship
   y = kx; and plot the image of a triangle under a translation or a rotation about the origin. Items use the 'points',
   'line' and 'number-line-inequality' tools of core/plot.js, so the check is exact; every target is on the snap grid,
   and the answer key is an SVG drawn from the same numbers. */
(function (G) {
  'use strict';
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[R(0, a.length - 1)]; }
  var M = function (v) { return String(v).replace('-', '−'); };
  var pt = function (p) { return '(' + M(p[0]) + ', ' + M(p[1]) + ')'; };
  var GRID = { xmin: -10, xmax: 10, ymin: -10, ymax: 10, step: 1, snap: 1 };
  var QGRID = { xmin: 0, xmax: 12, ymin: 0, ymax: 12, step: 1, snap: 1 };
  var FB_PTS = { position: 'Not quite. Check each point: move across first (x), then up or down (y).', 'swapped-coordinates': 'One point is at (y, x). The first coordinate is x.', count: 'Check how many points you need to place.' };
  var FB_LINE = { 'same-point': 'Place two different points.', intercept: 'A proportional relationship passes through the origin (0, 0).', 'slope-sign': 'Your line slants the wrong way.',
    'slope-reciprocal': 'You used x over y. The constant of proportionality is y ÷ x.', slope: 'Check the unit rate: when x = 1, y = k.' };
  var FB_INEQ = { boundary: 'Check the boundary: solve the inequality first.', direction: 'Check the direction: "greater than" shades right, "less than" shades left.', 'closed-open': 'Use a closed dot for ≤ or ≥ and an open dot for < or >.' };
  var svg = function (w, h, body) { return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '"><rect width="100%" height="100%" fill="#fff"/>' + body + '</svg>'); };
  function gridKey(g, points, labels, opts) {
    opts = opts || {};
    var s = g.xmin < 0 ? 14 : 24, W = (g.xmax - g.xmin) * s + 90, H = (g.ymax - g.ymin) * s + 40, X = function (x) { return 20 + (x - g.xmin) * s; }, Y = function (y) { return 20 + (g.ymax - y) * s; }, h = '';
    for (var i = g.xmin; i <= g.xmax; i++) h += '<line x1="' + X(i) + '" y1="' + Y(g.ymin) + '" x2="' + X(i) + '" y2="' + Y(g.ymax) + '" stroke="' + (i ? '#ddd' : '#333') + '"/>';
    for (var j = g.ymin; j <= g.ymax; j++) h += '<line x1="' + X(g.xmin) + '" y1="' + Y(j) + '" x2="' + X(g.xmax) + '" y2="' + Y(j) + '" stroke="' + (j ? '#ddd' : '#333') + '"/>';
    if (opts.poly) h += '<polygon points="' + opts.poly.map(function (p) { return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '" fill="none" stroke="#888" stroke-dasharray="5 4" stroke-width="1.5"/>';
    if (opts.image) h += '<polygon points="' + opts.image.map(function (p) { return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '" fill="#4f81bd" fill-opacity="0.18" stroke="#c0392b" stroke-width="2"/>';
    if (opts.k !== undefined) { var x2 = Math.min(g.xmax, g.ymax / opts.k); h += '<line x1="' + X(0) + '" y1="' + Y(0) + '" x2="' + X(x2) + '" y2="' + Y(opts.k * x2) + '" stroke="#2467a5" stroke-width="2.5"/>'; }
    points.forEach(function (p, k) { h += '<circle cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="4.5" fill="#c0392b"/><text x="' + (X(p[0]) + 6) + '" y="' + (Y(p[1]) - 6) + '" font-family="Arial" font-size="12">' + (labels[k] || '') + pt(p) + '</text>'; });
    return svg(W, H, h);
  }
  function lineKey(lo, hi, b, closed, dir) {
    var W = 560, H = 90, L = 30, Rr = 530, y0 = 45, X = function (v) { return L + (v - lo) / (hi - lo) * (Rr - L); }, h = '<line x1="' + L + '" y1="' + y0 + '" x2="' + Rr + '" y2="' + y0 + '" stroke="#333" stroke-width="1.5"/>';
    for (var t = lo; t <= hi; t++) h += '<line x1="' + X(t) + '" y1="' + (y0 - 5) + '" x2="' + X(t) + '" y2="' + (y0 + 5) + '" stroke="#333"/><text x="' + X(t) + '" y="' + (y0 + 20) + '" font-size="11" text-anchor="middle" font-family="Arial">' + M(t) + '</text>';
    h += '<path d="M' + X(b) + ' ' + y0 + ' H' + X(dir === 'right' ? hi : lo) + '" stroke="#1f5fa8" stroke-width="6"/>';
    h += '<circle cx="' + X(b) + '" cy="' + y0 + '" r="7" fill="' + (closed ? '#1f5fa8' : '#fff') + '" stroke="#1f5fa8" stroke-width="3"/>';
    return svg(W, H, h);
  }
  var inG = function (ps) { return ps.every(function (p) { return Math.abs(p[0]) <= 10 && Math.abs(p[1]) <= 10; }); };
  var NAMES = ['Maya', 'Leo', 'Priya', 'Diego', 'Ana', 'Owen', 'Nia', 'Raj'];
  var MAKERS = {
    'algebraic-expressions-integers': {
      'plot-points': ['Plot points in all four quadrants', function (lv) {
        var n = lv === 'cp2' ? 2 : 3, ps = [], labels = ['A', 'B', 'C'].slice(0, n), used = {};
        while (ps.length < n) { var p = [R(-8, 8), R(-8, 8)]; if (!p[0] || !p[1] || used[p]) continue; if (ps.some(function (q) { return (q[0] > 0) === (p[0] > 0) && (q[1] > 0) === (p[1] > 0); })) continue; used[p] = 1; ps.push(p); }
        if (lv === 'honors') {
          var a = ps[0], desc = [Math.abs(a[0]) + ' units ' + (a[0] < 0 ? 'left of' : 'right of') + ' the y-axis and ' + Math.abs(a[1]) + ' units ' + (a[1] < 0 ? 'below' : 'above') + ' the x-axis'];
          var b = [-ps[0][0], ps[0][1]], c = [ps[0][0], -ps[0][1]];
          return { prompt: 'Point A is ' + desc[0] + '. Point B is A reflected across the y-axis, and point C is A reflected across the x-axis. Plot A, B and C.', tool: 'points', grid: GRID, labels: ['A', 'B', 'C'],
            target: { points: [a, b, c] }, feedback: FB_PTS, key: gridKey(GRID, [a, b, c], ['A', 'B', 'C']), alt: 'Coordinate grid with A' + pt(a) + ', B' + pt(b) + ' and C' + pt(c) + '.',
            steps: ['A = ' + pt(a) + ': left/right gives x, below/above gives y.', 'Reflecting across the y-axis changes the sign of x: B = ' + pt(b) + '.', 'Reflecting across the x-axis changes the sign of y: C = ' + pt(c) + '.'] };
        }
        var named = ps.map(function (p, k) { return labels[k] + pt(p); });
        return { prompt: 'Plot ' + named.slice(0, -1).join(', ') + ' and ' + named[named.length - 1] + '.', tool: 'points', grid: GRID, labels: labels, target: { points: ps }, feedback: FB_PTS,
          key: gridKey(GRID, ps, labels), alt: 'Coordinate grid with ' + ps.map(function (p, k) { return labels[k] + pt(p); }).join(', ') + '.',
          steps: ['Start at the origin. Move across first: right for positive x, left for negative x.', 'Then move up for positive y or down for negative y.'].concat(ps.map(function (p, k) { return labels[k] + pt(p) + ' is in Quadrant ' + (p[0] > 0 ? (p[1] > 0 ? 'I' : 'IV') : (p[1] > 0 ? 'II' : 'III')) + '.'; })) };
      }],
      'fourth-corner': ['Find the fourth corner of a rectangle', function (lv) {
        var x1 = R(-8, 2), y1 = R(-8, 2), w = R(lv === 'cp2' ? 3 : 4, 8), h = R(3, 7);
        var A = [x1, y1], B = [x1 + w, y1], C = [x1 + w, y1 + h], D = [x1, y1 + h];
        if (!inG([A, B, C, D])) return null;
        var extra = lv === 'honors' ? ' Then find the rectangle\'s area.' : '';
        return { prompt: 'Three corners of rectangle ABCD are A' + pt(A) + ', B' + pt(B) + ' and C' + pt(C) + '. Plot the fourth corner, D.' + extra, tool: 'points', grid: GRID, labels: ['D'], target: { points: [D] }, feedback: FB_PTS,
          key: gridKey(GRID, [A, B, C, D], ['A', 'B', 'C', 'D'], { poly: [A, B, C, D] }), alt: 'Rectangle ABCD with D at ' + pt(D) + '.',
          steps: ['AB is horizontal and BC is vertical, so D is straight above A and straight left of C.', 'D has the x-coordinate of A and the y-coordinate of C: D = ' + pt(D) + '.'].concat(lv === 'honors' ? ['Width = ' + w + ', height = ' + h + ', area = ' + w * h + ' square units.'] : []) };
      }]
    },
    'one-step-equations-inequalities': {
      'solve-graph': ['Solve a one-step inequality and graph it', function (lv) {
        var v = pick(['x', 'n', 'm', 'k']), sol = R(-6, 6), op, a, rel = pick(['<', '>', '≤', '≥']), shown = rel, prompt, steps;
        var flip = { '<': '>', '>': '<', '≤': '≥', '≥': '≤' };
        if (lv === 'cp2') { a = R(2, 9) * pick([1, -1]); prompt = v + (a > 0 ? ' + ' + a : ' − ' + (-a)) + ' ' + rel + ' ' + M(sol + a); steps = [(a > 0 ? 'Subtract ' + a : 'Add ' + (-a)) + ' on both sides: ' + v + ' ' + rel + ' ' + M(sol) + '.']; }
        else if (lv === 'cp1') { a = pick([2, 3, 4, 5]); prompt = a + v + ' ' + rel + ' ' + M(a * sol); steps = ['Divide both sides by ' + a + ' (positive, so the sign stays): ' + v + ' ' + rel + ' ' + M(sol) + '.']; }
        else { a = -pick([2, 3, 4, 5]); prompt = '−' + (-a) + v + ' ' + rel + ' ' + M(a * sol); shown = flip[rel]; steps = ['Divide both sides by ' + M(a) + '. Dividing by a negative number reverses the inequality sign.', v + ' ' + shown + ' ' + M(sol) + '.']; }
        var closed = shown === '≤' || shown === '≥', dir = shown === '>' || shown === '≥' ? 'right' : 'left';
        steps.push((closed ? 'Closed' : 'Open') + ' dot at ' + M(sol) + ' (' + (closed ? 'the boundary is included' : 'the boundary is not included') + '), shading to the ' + dir + '.');
        return { prompt: 'Solve ' + prompt + '. Then graph the solution on the number line.', tool: 'number-line-inequality', line: { min: -10, max: 10, tick: 1, labelEvery: 1, labelFormat: 'decimal', snap: 1 },
          target: { boundary: sol, closed: closed, direction: dir }, feedback: FB_INEQ, key: lineKey(-10, 10, sol, closed, dir), alt: 'Number line with a ' + (closed ? 'closed' : 'open') + ' dot at ' + M(sol) + ' and shading to the ' + dir + '.', steps: steps };
      }]
    },
    'ratios-proportions-percentages': {
      'graph-proportional': ['Graph a proportional relationship', function (lv) {
        var ctx = pick([['hours', 'miles'], ['pounds', 'dollars'], ['minutes', 'pages'], ['tickets', 'dollars'], ['days', 'inches']]), k, prompt, steps;
        if (lv === 'cp2') { k = R(2, 4); prompt = 'Each ' + ctx[0].replace(/s$/, '') + ' gives ' + k + ' ' + ctx[1] + '. Graph y = ' + k + 'x, where x is ' + ctx[0] + ' and y is ' + ctx[1] + '.'; }
        else if (lv === 'cp1') { var xs = [2, 4, 6].map(function (x) { return x; }); k = pick([0.5, 1.5, 2, 3]); prompt = 'The table shows a proportional relationship: x (' + ctx[0] + '): ' + xs.join(', ') + '; y (' + ctx[1] + '): ' + xs.map(function (x) { return M(x * k); }).join(', ') + '. Graph the relationship.'; }
        else { var x0 = pick([4, 6, 8]); k = pick([0.5, 1.5, 0.75, 1.25]); if ((x0 * k) % 1) return null; prompt = pick(NAMES) + ' records that ' + x0 + ' ' + ctx[0] + ' correspond to ' + M(x0 * k) + ' ' + ctx[1] + ', and the relationship is proportional. Graph it, then find the constant of proportionality.'; }
        var kFr = k === 0.5 ? '1/2' : k === 1.5 ? '3/2' : k === 0.75 ? '3/4' : k === 1.25 ? '5/4' : String(k);
        steps = ['A proportional relationship is a line through the origin, y = kx.', 'k = y ÷ x = ' + kFr + ', so the line passes through (0, 0) and ' + (k % 1 ? pt([4, 4 * k]) : pt([1, k])) + '.', 'Draw the line through those two points.'];
        return { prompt: prompt, tool: 'line', grid: QGRID, target: { m: kFr, b: '0' }, feedback: FB_LINE, key: gridKey(QGRID, [[0, 0], k % 1 ? [4, 4 * k] : [1, k]], ['', ''], { k: k }),
          alt: 'Line y = ' + kFr + 'x through the origin on a first-quadrant grid.', steps: steps };
      }]
    },
    'spatial-thinking': {
      'translate': ['Translate a triangle', function (lv) {
        var A = [R(-6, 2), R(-6, 2)], B = [A[0] + R(2, 4), A[1]], C = [A[0] + R(0, 3), A[1] + R(2, 4)], dx = R(-5, 5) || 3, dy = R(-5, 5) || -2;
        var img = [A, B, C].map(function (p) { return [p[0] + dx, p[1] + dy]; });
        if (!inG(img)) return null;
        var rule = lv === 'cp2' ? (Math.abs(dx) + ' units ' + (dx > 0 ? 'right' : 'left') + ' and ' + Math.abs(dy) + ' units ' + (dy > 0 ? 'up' : 'down')) : '(x, y) → (x ' + (dx < 0 ? '− ' + (-dx) : '+ ' + dx) + ', y ' + (dy < 0 ? '− ' + (-dy) : '+ ' + dy) + ')';
        return { prompt: 'Triangle ABC has A' + pt(A) + ', B' + pt(B) + ' and C' + pt(C) + '. Plot A′, B′ and C′, its image under the translation ' + rule + '.', tool: 'points', grid: GRID, labels: ['A′', 'B′', 'C′'], target: { points: img }, feedback: FB_PTS,
          key: gridKey(GRID, img, ['A′', 'B′', 'C′'], { poly: [A, B, C], image: img }), alt: 'Triangle ABC and its image A′' + pt(img[0]) + ', B′' + pt(img[1]) + ', C′' + pt(img[2]) + '.',
          steps: ['Add ' + M(dx) + ' to each x-coordinate and ' + M(dy) + ' to each y-coordinate.'].concat(img.map(function (p, k) { return ['A', 'B', 'C'][k] + '′ = ' + pt(p) + '.'; })) };
      }],
      'rotate': ['Rotate a triangle about the origin', function (lv) {
        var ang = lv === 'cp2' ? 180 : pick([90, 180, 270]), A = [R(1, 6), R(1, 6)], B = [A[0] + R(1, 3), A[1] - R(0, 2)], C = [A[0], A[1] + R(1, 3)];
        var rot = function (p) { return ang === 90 ? [-p[1], p[0]] : ang === 180 ? [-p[0], -p[1]] : [p[1], -p[0]]; }, img = [A, B, C].map(rot);
        if (!inG([A, B, C].concat(img))) return null;
        var rule = ang === 90 ? '(x, y) → (−y, x)' : ang === 180 ? '(x, y) → (−x, −y)' : '(x, y) → (y, −x)';
        return { prompt: 'Triangle ABC has A' + pt(A) + ', B' + pt(B) + ' and C' + pt(C) + '. Rotate it ' + ang + '° counterclockwise about the origin and plot A′, B′ and C′.', tool: 'points', grid: GRID, labels: ['A′', 'B′', 'C′'], target: { points: img }, feedback: FB_PTS,
          key: gridKey(GRID, img, ['A′', 'B′', 'C′'], { poly: [A, B, C], image: img }), alt: 'Triangle ABC and its image after a ' + ang + '° rotation: A′' + pt(img[0]) + ', B′' + pt(img[1]) + ', C′' + pt(img[2]) + '.',
          steps: ['A ' + ang + '° counterclockwise rotation about the origin uses the rule ' + rule + '.'].concat(img.map(function (p, k) { return ['A', 'B', 'C'][k] + '′ = ' + pt(p) + '.'; })) };
      }]
    }
  };
  function item(id, skillId, r) {
    var plot = { tool: r.tool, target: r.target, feedback: r.feedback, answerKey: { svg: r.key, alt: r.alt }, check: { type: 'exact-after-snap' } };
    if (r.grid) plot.grid = r.grid;
    if (r.labels) plot.labels = r.labels;
    if (r.line) plot.numberLine = r.line;
    return { id: id, skillId: skillId, prompt: r.prompt, solutionSteps: r.steps, plot: plot };
  }
  G.MK_G7_PLOT = {
    units: Object.keys(MAKERS),
    makers: MAKERS,
    skills: function (unitId) { var m = MAKERS[unitId] || {}; return Object.keys(m).map(function (k) { return { id: k, name: m[k][0] }; }); },
    pool: function (unitId, level, skillId, n) {
      var m = MAKERS[unitId]; if (!m) return [];
      var ids = skillId ? [skillId] : Object.keys(m), out = [], seen = {}, tries = 0;
      while (out.length < (n || 12) && tries++ < 3000) {
        var id = ids[out.length % ids.length], r = m[id] && m[id][1](level || 'cp1'); if (!r || seen[r.prompt]) continue; seen[r.prompt] = 1;
        out.push(item('g7-plot-' + id + '-' + out.length, id, r));
      }
      return out;
    }
  };
})(typeof window !== 'undefined' ? window : globalThis);
