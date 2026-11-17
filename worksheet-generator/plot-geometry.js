/* Geometry plotting practice for plot-practice.html (2026-11-17, audit #17).
   Generated items for the Geometry units: plot a midpoint or a partition point, the image of a triangle under a
   transformation, the fourth vertex of a quadrilateral, and the center and four points of a circle. Each item uses the
   'points' tool of core/plot.js, so the check is exact; the answer key is drawn as an SVG grid from the same points. */
(function (G) {
  'use strict';
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[R(0, a.length - 1)]; }
  var GRID = { xmin: -10, xmax: 10, ymin: -10, ymax: 10, step: 1, snap: 1 };
  var FB = { position: 'Not quite. Check each point: move across first (x), then up or down (y).', 'swapped-coordinates': 'One point is at (y, x). The first coordinate is x.', count: 'Check how many points you need to place.' };
  var pt = function (p) { return '(' + p[0] + ', ' + p[1] + ')'; };
  var inGrid = function (ps) { return ps.every(function (p) { return Math.abs(p[0]) <= 10 && Math.abs(p[1]) <= 10; }); };
  function keySvg(points, labels, extra) {
    var s = 14, w = 21 * s, o = 10 * s, X = function (x) { return o + x * s + 10; }, Y = function (y) { return o - y * s + 10; }, h = '';
    for (var i = -10; i <= 10; i++) h += '<line x1="' + X(i) + '" y1="' + Y(-10) + '" x2="' + X(i) + '" y2="' + Y(10) + '" stroke="' + (i ? '#ddd' : '#333') + '"/><line x1="' + X(-10) + '" y1="' + Y(i) + '" x2="' + X(10) + '" y2="' + Y(i) + '" stroke="' + (i ? '#ddd' : '#333') + '"/>';
    if (extra && extra.circle) h += '<circle cx="' + X(extra.circle.c[0]) + '" cy="' + Y(extra.circle.c[1]) + '" r="' + extra.circle.r * s + '" fill="none" stroke="#2467a5" stroke-width="2"/>';
    if (extra && extra.poly) h += '<polygon points="' + extra.poly.map(function (p) { return X(p[0]) + ',' + Y(p[1]); }).join(' ') + '" fill="none" stroke="#888" stroke-dasharray="5 4" stroke-width="1.5"/>';
    points.forEach(function (p, k) { h += '<circle cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="4" fill="#c0392b"/><text x="' + (X(p[0]) + 6) + '" y="' + (Y(p[1]) - 6) + '" font-family="Arial" font-size="12">' + (labels[k] || '') + pt(p) + '</text>'; });
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="' + (w + 20) + '" height="' + (w + 20) + '" viewBox="0 0 ' + (w + 20) + ' ' + (w + 20) + '"><rect width="100%" height="100%" fill="#fff"/>' + h + '</svg>');
  }
  function item(id, skillId, prompt, points, labels, steps, extra) {
    return { id: id, skillId: skillId, prompt: prompt, solutionSteps: steps, plot: { tool: 'points', grid: GRID, labels: labels, target: { points: points }, feedback: FB,
      answerKey: { svg: keySvg(points, labels, extra), alt: 'Coordinate grid with ' + labels.map(function (l, k) { return l + pt(points[k]); }).join(', ') + '.' }, check: { type: 'exact-after-snap' } } };
  }
  var big = function (lv) { return lv === 'cp2' ? 6 : lv === 'cp1' ? 8 : 9; };
  var MAKERS = {
    'foundations-geometry': {
      midpoint: ['Midpoint of a segment', function (lv) {
        var A = [R(-big(lv), big(lv)), R(-big(lv), big(lv))], d = [2 * R(-4, 4), 2 * R(-4, 4)]; if (!d[0] && !d[1]) return null; var B = [A[0] + d[0], A[1] + d[1]], M = [A[0] + d[0] / 2, A[1] + d[1] / 2];
        if (!inGrid([B])) return null;
        return ['Segment AB has endpoints A' + pt(A) + ' and B' + pt(B) + '. Plot its midpoint M.', [M], ['M'], ['M = ((x₁ + x₂)/2, (y₁ + y₂)/2) = ((' + A[0] + ' + ' + B[0] + ')/2, (' + A[1] + ' + ' + B[1] + ')/2) = ' + pt(M) + '.']];
      }],
      endpoint: ['Missing endpoint from a midpoint', function (lv) {
        var A = [R(-6, 6), R(-6, 6)], M = [A[0] + R(-3, 3), A[1] + R(-3, 3)], B = [2 * M[0] - A[0], 2 * M[1] - A[1]];
        if ((M[0] === A[0] && M[1] === A[1]) || !inGrid([B, M])) return null;
        return ['M' + pt(M) + ' is the midpoint of segment AB, and A is at ' + pt(A) + '. Plot endpoint B.', [B], ['B'], ['Go from A to M: ' + (M[0] - A[0]) + ' in x and ' + (M[1] - A[1]) + ' in y.', 'Repeat the same move from M to reach B = ' + pt(B) + '.']];
      }],
      partition: ['Partition a directed segment', function (lv) {
        var m = R(1, lv === 'cp2' ? 2 : 4), n = R(1, lv === 'cp2' ? 3 : 4); if (m === n) return null; var t = m + n, A = [R(-8, 6), R(-8, 6)], k = [R(-2, 2), R(-2, 2)]; if (!k[0] && !k[1]) return null;
        var B = [A[0] + k[0] * t, A[1] + k[1] * t], P = [A[0] + k[0] * m, A[1] + k[1] * m]; if (!inGrid([B])) return null;
        return ['Directed segment AB goes from A' + pt(A) + ' to B' + pt(B) + '. Plot point P on AB with AP : PB = ' + m + ' : ' + n + '.', [P], ['P'], ['P is ' + m + '/' + t + ' of the way from A to B.', 'Change from A to B: ' + (B[0] - A[0]) + ' in x, ' + (B[1] - A[1]) + ' in y. Take ' + m + '/' + t + ' of each and add to A: P = ' + pt(P) + '.']];
      }]
    },
    transformations: {
      translate: ['Translate a triangle', function (lv) { return tri(lv, 'translate'); }],
      reflect: ['Reflect a triangle', function (lv) { return tri(lv, 'reflect'); }],
      rotate: ['Rotate a triangle about the origin', function (lv) { return tri(lv, 'rotate'); }],
      dilate: ['Dilate a triangle about the origin', function (lv) { return tri(lv, 'dilate'); }]
    },
    'quadrilaterals-polygons': {
      fourth: ['Fourth vertex of a quadrilateral', function (lv) {
        var kind = pick(lv === 'cp2' ? ['rectangle', 'parallelogram'] : ['rectangle', 'parallelogram', 'square']), A = [R(-7, 2), R(-7, 2)], u = [R(2, 6), R(-2, 3)], v;
        if (kind === 'rectangle') { u = [R(2, 7), 0]; v = [0, R(2, 6)]; if (lv !== 'cp2' && Math.random() < 0.5) { var a = R(1, 3), b = R(1, 3); u = [2 * a, a]; v = [-b, 2 * b]; } }
        else if (kind === 'square') { var p = R(1, 4), q = R(1, 3); u = [p, q]; v = [-q, p]; }
        else v = [R(-2, 3), R(2, 5)];
        var B = [A[0] + u[0], A[1] + u[1]], D = [A[0] + v[0], A[1] + v[1]], C = [B[0] + v[0], B[1] + v[1]]; if (!inGrid([B, C, D])) return null;
        return ['ABCD is a ' + kind + ' with A' + pt(A) + ', B' + pt(B) + ' and D' + pt(D) + '. Plot vertex C.', [C], ['C'], ['In a ' + kind + ', AB and DC are parallel and equal: C = D + (B − A).', 'B − A = ' + pt(u) + ', so C = ' + pt(D) + ' + ' + pt(u) + ' = ' + pt(C) + '.'], { poly: [A, B, C, D] }];
      }]
    },
    circles: {
      circle: ['Graph a circle from its equation', function (lv) {
        var h = R(-4, 4), k = R(-4, 4), r = R(2, lv === 'cp2' ? 4 : 6); if (Math.abs(h) + r > 10 || Math.abs(k) + r > 10) return null;
        var sq = function (v, s) { return s === 0 ? v + '²' : '(' + v + (s > 0 ? ' − ' + s : ' + ' + (-s)) + ')²'; }, eq = sq('x', h) + ' + ' + sq('y', k) + ' = ' + r * r;
        var P = [[h, k], [h + r, k], [h - r, k], [h, k + r], [h, k - r]];
        return ['Graph the circle ' + eq + '. Plot its center C and the four points of the circle directly right of, left of, above and below the center.', P, ['C', 'R', 'L', 'U', 'D'], ['Standard form (x − h)² + (y − k)² = r² gives center (' + h + ', ' + k + ') and r = √' + r * r + ' = ' + r + '.', 'Move ' + r + ' units right, left, up and down from the center.'], { circle: { c: [h, k], r: r } }];
      }]
    }
  };
  function tri(lv, how) {
    var A = [R(1, 5), R(1, 5)], B = [A[0] + R(1, 4), A[1] + R(-2, 2)], C = [A[0] + R(-1, 2), A[1] + R(2, 4)], s = Math.random() < 0.5 ? -1 : 1;
    var P = [A, B, C].map(function (p) { return [s * p[0], p[1]]; }), f, desc, steps;
    if (how === 'translate') { var dx = R(-6, 6), dy = R(-6, 6); if (!dx && !dy) return null; f = function (p) { return [p[0] + dx, p[1] + dy]; }; var mv = function (d, neg, pos) { return Math.abs(d) + ' unit' + (Math.abs(d) === 1 ? '' : 's') + (d < 0 ? neg : pos); }; desc = 'translated ' + [dx ? mv(dx, ' left', ' right') : '', dy ? mv(dy, ' down', ' up') : ''].filter(Boolean).join(' and '); steps = 'Add ' + dx + ' to each x and ' + dy + ' to each y: (x, y) → (x ' + (dx < 0 ? '− ' + -dx : '+ ' + dx) + ', y ' + (dy < 0 ? '− ' + -dy : '+ ' + dy) + ').'; }
    else if (how === 'reflect') { var ax = pick(lv === 'cp2' ? ['x', 'y'] : ['x', 'y', 'y=x']); f = ax === 'x' ? function (p) { return [p[0], -p[1]]; } : ax === 'y' ? function (p) { return [-p[0], p[1]]; } : function (p) { return [p[1], p[0]]; }; desc = 'reflected across ' + (ax === 'y=x' ? 'the line y = x' : 'the ' + ax + '-axis'); steps = ax === 'x' ? '(x, y) → (x, −y).' : ax === 'y' ? '(x, y) → (−x, y).' : '(x, y) → (y, x).'; }
    else if (how === 'rotate') { var a = pick(lv === 'cp2' ? ['180'] : ['90cw', '90ccw', '180']); f = a === '180' ? function (p) { return [-p[0], -p[1]]; } : a === '90cw' ? function (p) { return [p[1], -p[0]]; } : function (p) { return [-p[1], p[0]]; }; desc = 'rotated ' + (a === '180' ? '180°' : '90° ' + (a === '90cw' ? 'clockwise' : 'counterclockwise')) + ' about the origin'; steps = a === '180' ? '(x, y) → (−x, −y).' : a === '90cw' ? '(x, y) → (y, −x).' : '(x, y) → (−y, x).'; }
    else { var k = lv === 'cp2' ? 2 : pick([2, 0.5]); P = P.map(function (p) { return k === 0.5 ? [p[0] * 2 > 8 ? p[0] : p[0] * 2, p[1] * 2 > 8 ? p[1] : p[1] * 2] : p; }); if (k === 0.5 && P.some(function (p) { return p[0] % 2 || p[1] % 2; })) return null; f = function (p) { return [p[0] * k, p[1] * k]; }; desc = 'dilated about the origin by a scale factor of ' + (k === 0.5 ? '1/2' : k); steps = 'Multiply both coordinates by ' + (k === 0.5 ? '1/2' : k) + '.'; }
    var I = P.map(f); if (!inGrid(P.concat(I))) return null;
    return ['Triangle ABC has vertices A' + pt(P[0]) + ', B' + pt(P[1]) + ' and C' + pt(P[2]) + '. It is ' + desc + '. Plot the image A′B′C′.', I, ['A′', 'B′', 'C′'], [steps, 'A′' + pt(I[0]) + ', B′' + pt(I[1]) + ', C′' + pt(I[2]) + '.'], { poly: P }];
  }
  var API = G.MK_GEO_PLOT = {
    units: Object.keys(MAKERS),
    skills: function (unitId) { var m = MAKERS[unitId] || {}; return Object.keys(m).map(function (k) { return { id: k, name: m[k][0] }; }); },
    pool: function (unitId, level, skillId, n) {
      var m = MAKERS[unitId] || {}, ids = skillId ? [skillId] : Object.keys(m), out = [], seen = {}, tries = 0;
      while (out.length < (n || 12) && tries++ < 600) {
        var id = ids[out.length % ids.length], r = m[id] && m[id][1](level || 'cp1'); if (!r) continue;
        var key = r[0]; if (seen[key]) continue; seen[key] = 1;
        out.push(item('geo-plot-' + unitId + '-' + id + '-' + out.length, id, r[0], r[1], r[2], r[3], r[4]));
      }
      return out;
    }
  };
  void API;
})(typeof window !== 'undefined' ? window : globalThis);
