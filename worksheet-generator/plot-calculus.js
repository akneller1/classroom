/* Calculus graphing practice for plot-practice.html (2026-11-18, Calculus audit #15).
   Generated items for five Calculus units: graph a tangent line, plot values of f′, plot relative extrema and points
   of inflection, plot an accumulation function or an antiderivative through a given point, plot a particular solution
   of a differential equation and plot a particle's position from its velocity. Each item uses the 'line' or 'points'
   tool of core/plot.js, so the check is exact; every answer is an integer point on the grid, computed from the same
   polynomial the prompt shows, and the answer key is an SVG of the curve with the answer drawn on it. */
(function (G) {
  'use strict';
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function pick(a) { return a[R(0, a.length - 1)]; }
  var LO = -8, HI = 8, GRID = { xmin: LO, xmax: HI, ymin: LO, ymax: HI, step: 1, snap: 1 };
  var M = function (v) { return String(v).replace('-', '−'); };
  var pt = function (p) { return '(' + M(p[0]) + ', ' + M(p[1]) + ')'; };
  var inGrid = function (v) { return Number.isInteger(v) && v >= LO && v <= HI; };
  /* polynomial helpers: c[k] is the coefficient of x^k */
  function ev(c, x) { return c.reduce(function (s, a, k) { return s + a * Math.pow(x, k); }, 0); }
  function der(c) { return c.slice(1).map(function (a, k) { return a * (k + 1); }); }
  var SUP = ['', '', '²', '³', '⁴'];
  function poly(c, v) {
    v = v || 'x'; var s = '';
    for (var k = c.length - 1; k >= 0; k--) {
      var a = c[k]; if (!a) continue;
      var mag = Math.abs(a), term = k === 0 ? String(mag) : (mag === 1 ? '' : String(mag)) + v + SUP[k];
      s += s ? (a < 0 ? ' − ' : ' + ') + term : (a < 0 ? '−' : '') + term;
    }
    return s || '0';
  }
  var svgUrl = function (w, h, body) { return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h + '"><rect width="100%" height="100%" fill="#fff"/>' + body + '</svg>'); };
  /* answer key: grid from −8 to 8, the curve (if any), the line (if any) and the answer points */
  function key(curve, line, points, xl, yl) {
    var s = 20, o = 24, X = function (x) { return o + (x - LO) * s; }, Y = function (y) { return o + (HI - y) * s; }, h = '';
    for (var i = LO; i <= HI; i++) {
      h += '<line x1="' + X(i) + '" y1="' + Y(LO) + '" x2="' + X(i) + '" y2="' + Y(HI) + '" stroke="' + (i ? '#e3e3e3' : '#333') + '"/><line x1="' + X(LO) + '" y1="' + Y(i) + '" x2="' + X(HI) + '" y2="' + Y(i) + '" stroke="' + (i ? '#e3e3e3' : '#333') + '"/>';
      if (i % 2 === 0 && i) h += '<text x="' + X(i) + '" y="' + (Y(0) + 13) + '" font-size="9" text-anchor="middle" font-family="Arial">' + M(i) + '</text><text x="' + (X(0) - 4) + '" y="' + (Y(i) + 3) + '" font-size="9" text-anchor="end" font-family="Arial">' + M(i) + '</text>';
    }
    if (curve) {
      var d = '', pen = false;
      for (var x = curve.from; x <= curve.to + 1e-9; x += 0.05) {
        var y = curve.f(x); if (y < LO - 0.5 || y > HI + 0.5) { pen = false; continue; }
        d += (pen ? ' L' : ' M') + X(x).toFixed(1) + ' ' + Y(y).toFixed(1); pen = true;
      }
      h += '<path d="' + d + '" fill="none" stroke="#2467a5" stroke-width="2"/>';
    }
    if (line) {
      var xa = line.m ? Math.max(LO, Math.min((HI - line.b) / line.m, (LO - line.b) / line.m)) : LO, xb = line.m ? Math.min(HI, Math.max((HI - line.b) / line.m, (LO - line.b) / line.m)) : HI;
      h += '<line x1="' + X(xa) + '" y1="' + Y(line.m * xa + line.b) + '" x2="' + X(xb) + '" y2="' + Y(line.m * xb + line.b) + '" stroke="#c0392b" stroke-width="2"/>';
    }
    (points || []).forEach(function (p) { h += '<circle cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="4.5" fill="#c0392b"/>'; });
    h += '<text x="' + (X(HI) - 2) + '" y="' + (Y(0) - 5) + '" font-size="11" text-anchor="end" font-family="Arial">' + xl + '</text><text x="' + (X(0) + 5) + '" y="' + (Y(HI) + 10) + '" font-size="11" font-family="Arial">' + yl + '</text>';
    return svgUrl(16 * s + 2 * o, 16 * s + 2 * o, h);
  }
  var FB_PTS = { position: 'Not quite. Compute each y-value, then go across to x and up or down to y.', 'swapped-coordinates': 'One point is at (y, x). The first number in each pair is x.', count: 'Plot one point for each x-value asked for.' };
  var FB_LINE = { 'same-point': 'Place two different points.', intercept: 'Your slope is right. Check the point of tangency: the line must pass through (a, f(a)).', 'slope-sign': 'Your line slants the wrong way. Check the sign of f′(a).', 'slope-reciprocal': 'You used run over rise. The slope is f′(a), rise over run.', slope: 'The slope of the tangent line is f′(a). Find f′(x), then substitute x = a.' };
  function xs(lo, hi) { var a = []; for (var x = lo; x <= hi; x++) a.push(x); return a; }
  function cubicish(lv) {
    /* polynomials whose derivatives stay small: c[k] coefficients */
    if (lv === 'cp2') return pick([[R(-3, 3), R(-3, 3), 1], [R(-3, 3), R(-3, 3), -1], [R(-2, 2), R(-2, 2), 1]]);
    if (lv === 'cp1') return pick([[R(-3, 3), R(-3, 3), pick([1, -1])], [R(-2, 2), pick([-3, -1, 1, 3]), 0, 1], [R(-2, 2), R(-2, 2), pick([2, -2])]]);
    return pick([[R(-2, 2), pick([-3, -2, 2, 3]), 0, pick([1, -1])], [R(-2, 2), R(-3, 3), pick([-1, 1]), 1], [R(-2, 2), 0, pick([-2, 2]), 0, 1]]);
  }
  var MAKERS = {
    derivatives: {
      tangent: ['Graph a tangent line', function (lv) {
        var c = cubicish(lv), a = pick(lv === 'cp2' ? [-1, 0, 1, 2] : [-2, -1, 1, 2]), m = ev(der(c), a), fa = ev(c, a), b = fa - m * a;
        if (!inGrid(fa) || !inGrid(b) || !inGrid(m + b) || Math.abs(m) > 6) return null;
        var f = poly(c);
        return { prompt: 'Graph the line tangent to f(x) = ' + f + ' at x = ' + M(a) + '. Drag two points on the line.', tool: 'line', target: { m: String(m), b: String(b) }, feedback: FB_LINE,
          key: key({ f: function (x) { return ev(c, x); }, from: LO, to: HI }, { m: m, b: b }, [[a, fa]], 'x', 'y'), alt: 'The curve y = ' + f + ' with its tangent line y = ' + poly([b, m]) + ' touching it at ' + pt([a, fa]) + '.',
          steps: ['Point of tangency: f(' + M(a) + ') = ' + M(fa) + ', so the line passes through ' + pt([a, fa]) + '.', 'Slope: f′(x) = ' + poly(der(c)) + ', so f′(' + M(a) + ') = ' + M(m) + '.', 'Tangent line: y = ' + poly([b, m]) + '. Plot ' + pt([a, fa]) + ' and ' + pt([a + 1, fa + m]) + '.'] };
      }],
      'derivative-values': ['Plot values of the derivative', function (lv) {
        var c = cubicish(lv), d = der(c), X = lv === 'cp1' ? xs(-2, 2) : [-1, 0, 1], P = X.map(function (x) { return [x, ev(d, x)]; });
        if (!P.every(function (p) { return inGrid(p[1]); })) return null;
        return { prompt: 'f(x) = ' + poly(c) + '. Plot the points (x, f′(x)) for x = ' + X.map(M).join(', ') + '.', tool: 'points', target: { points: P }, feedback: FB_PTS,
          key: key({ f: function (x) { return ev(d, x); }, from: LO, to: HI }, null, P, 'x', 'y = f′(x)'), alt: 'Graph of f′(x) = ' + poly(d) + ' with the points ' + P.map(pt).join(', ') + '.',
          steps: ['Differentiate term by term: f′(x) = ' + poly(d) + '.', 'Evaluate: ' + P.map(function (p) { return 'f′(' + M(p[0]) + ') = ' + M(p[1]); }).join('; ') + '.', 'Plot each pair (x, f′(x)). The points lie on the graph of f′, not f.'] };
      }]
    },
    'applications-derivatives': {
      extrema: ['Plot relative extrema', function (lv) {
        var k = R(-3, 3), forms = [
          [[k, -3, 0, 1], [-1, 1]], [[k, 3, 0, -1], [-1, 1]], [[k, 0, -3, 1], [0, 2]], [[k, 0, 3, 1], [-2, 0]], [[k, 0, -2, 0, 1], [-1, 0, 1]], [[k, 0, 2, 0, -1], [-1, 0, 1]]];
        var F = lv === 'cp2' ? pick(forms.slice(0, 4)) : pick(forms), c = F[0], cs = F[1], d2 = der(der(c)), P = cs.map(function (x) { return [x, ev(c, x)]; });
        if (!P.every(function (p) { return inGrid(p[1]); })) return null;
        var kinds = cs.map(function (x) { return ev(d2, x) > 0 ? 'relative minimum' : 'relative maximum'; });
        return { prompt: 'f(x) = ' + poly(c) + '. Plot each relative extremum of f as a point (x, f(x)).', tool: 'points', target: { points: P }, feedback: FB_PTS,
          key: key({ f: function (x) { return ev(c, x); }, from: LO, to: HI }, null, P, 'x', 'y'), alt: 'Graph of y = ' + poly(c) + ' with its relative extrema ' + P.map(pt).join(', ') + ' marked.',
          steps: ['f′(x) = ' + poly(der(c)) + ' = 0 at x = ' + cs.map(M).join(', ') + '.', 'f″(x) = ' + poly(d2) + ': ' + cs.map(function (x, i) { return 'f″(' + M(x) + ') = ' + M(ev(d2, x)) + ', a ' + kinds[i]; }).join('; ') + '.', 'Plot ' + P.map(pt).join(', ') + '.'] };
      }],
      inflection: ['Plot points of inflection', function (lv) {
        var h = R(-2, 2), k = R(-3, 3), c, P, steps;
        if (lv === 'honors' && Math.random() < 0.5) {
          c = [R(-1, 3), 0, -6, 0, 1]; P = [[-1, ev(c, -1)], [1, ev(c, 1)]];
          steps = ['f″(x) = ' + poly(der(der(c))) + ' = 12(x² − 1) = 0 at x = −1 and x = 1.', 'f″ changes sign at both (positive, negative, positive), so both are points of inflection.', 'Plot ' + P.map(pt).join(' and ') + '.'];
        } else {
          /* f(x) = (x − h)³ + s(x − h) + k expanded: the inflection point is (h, k) */
          var s = pick(lv === 'cp2' ? [0, -3, 3] : [-3, -1, 1, 3]);
          c = [-h * h * h - s * h + k, 3 * h * h + s, -3 * h, 1]; P = [[h, k]];
          steps = ['f″(x) = ' + poly(der(der(c))) + ' = 0 at x = ' + M(h) + '.', 'f″ changes from negative to positive at x = ' + M(h) + ', so it is a point of inflection.', 'f(' + M(h) + ') = ' + M(k) + ': plot ' + pt([h, k]) + '.'];
        }
        if (!P.every(function (p) { return inGrid(p[1]); })) return null;
        return { prompt: 'f(x) = ' + poly(c) + '. Plot every point of inflection of the graph of f.', tool: 'points', target: { points: P }, feedback: FB_PTS,
          key: key({ f: function (x) { return ev(c, x); }, from: LO, to: HI }, null, P, 'x', 'y'), alt: 'Graph of y = ' + poly(c) + ' with its point(s) of inflection ' + P.map(pt).join(', ') + ' marked.', steps: steps };
      }]
    },
    'fundamental-theorem-calculus': {
      accumulation: ['Plot an accumulation function', function (lv) {
        var m = pick([2, -2]) * (lv === 'cp2' ? 1 : pick([1, 1, 2])), b = R(-4, 4), X = lv === 'cp2' ? [0, 1, 2, 3] : [-1, 0, 1, 2, 3], P = X.map(function (x) { return [x, m * x * x / 2 + b * x]; });
        if (!P.every(function (p) { return inGrid(p[1]); })) return null;
        var f = poly([b, m], 't');
        return { prompt: 'Let g(x) = ∫ from 0 to x (' + f + ') dt. Plot the points (x, g(x)) for x = ' + X.map(M).join(', ') + '.', tool: 'points', target: { points: P }, feedback: FB_PTS,
          key: key({ f: function (x) { return m * x * x / 2 + b * x; }, from: LO, to: HI }, null, P, 'x', 'y = g(x)'), alt: 'Graph of g(x) = ' + poly([0, b, m / 2]) + ' with the points ' + P.map(pt).join(', ') + '.',
          steps: ['Antiderivative: g(x) = [' + poly([0, b, m / 2], 't') + '] from 0 to x = ' + poly([0, b, m / 2]) + '.', 'g(0) = 0 because the interval has no width' + (X[0] < 0 ? '; for x = −1 the integral runs backward, so g(−1) = −∫ from −1 to 0' : '') + '.', 'Values: ' + P.map(function (p) { return 'g(' + M(p[0]) + ') = ' + M(p[1]); }).join('; ') + '.'] };
      }],
      antiderivative: ['Plot the antiderivative through a given point', function (lv) {
        var a = pick(lv === 'cp2' ? [0] : [0, 1]), c2 = pick([1, -1]) * (lv === 'honors' ? pick([1, 3]) : 1), fpr = lv === 'honors' ? [R(-2, 2), 0, c2] : [R(-3, 3), 2 * pick([1, -1])], F0 = R(-3, 3);
        var F = [0].concat(fpr.map(function (v, k) { return v / (k + 1); })), C = F0 - ev(F, a); F[0] = C;
        var X = xs(-2, 2), P = X.map(function (x) { return [x, ev(F, x)]; });
        if (!P.every(function (p) { return inGrid(p[1]); }) || !F.every(Number.isInteger)) return null;
        return { prompt: 'F′(x) = ' + poly(fpr) + ' and F(' + M(a) + ') = ' + M(F0) + '. Plot F(x) for x = −2, −1, 0, 1, 2.', tool: 'points', target: { points: P }, feedback: FB_PTS,
          key: key({ f: function (x) { return ev(F, x); }, from: LO, to: HI }, null, P, 'x', 'y = F(x)'), alt: 'Graph of F(x) = ' + poly(F) + ' with the points ' + P.map(pt).join(', ') + '.',
          steps: ['Antidifferentiate term by term: F(x) = ' + poly([0].concat(F.slice(1))) + ' + C.', 'F(' + M(a) + ') = ' + M(F0) + ' gives C = ' + M(C) + ', so F(x) = ' + poly(F) + '.', 'Values: ' + P.map(function (p) { return 'F(' + M(p[0]) + ') = ' + M(p[1]); }).join('; ') + '.'] };
      }]
    },
    'applications-integrals': {
      position: ['Plot position from velocity', function (lv) {
        var a = pick(lv === 'cp2' ? [2, -2] : [2, -2, 4]), b = R(-4, 4), x0 = R(-3, 3), T = xs(0, lv === 'cp2' ? 3 : 4), P = T.map(function (t) { return [t, x0 + b * t + a * t * t / 2]; });
        if (!P.every(function (p) { return inGrid(p[1]); })) return null;
        var s = [x0, b, a / 2];
        return { prompt: 'A particle moves along a line with velocity v(t) = ' + poly([b, a], 't') + ' and position x(0) = ' + M(x0) + '. Plot its position (t, x(t)) for t = ' + T.join(', ') + '.', tool: 'points', target: { points: P }, feedback: FB_PTS,
          key: key({ f: function (t) { return ev(s, t); }, from: 0, to: HI }, null, P, 't', 'x(t)'), alt: 'Graph of the position x(t) = ' + poly(s, 't') + ' with the points ' + P.map(pt).join(', ') + '.',
          steps: ['Position = starting position + net change: x(t) = ' + M(x0) + ' + ∫ from 0 to t (' + poly([b, a], 'u') + ') du = ' + poly(s, 't') + '.', 'Values: ' + P.map(function (p) { return 'x(' + p[0] + ') = ' + M(p[1]); }).join('; ') + '.', 'The particle turns around where v(t) = 0' + (b * a < 0 && -b / a > 0 ? ', at t = ' + M(-b / a) : '') + '.'] };
      }]
    },
    'differential-equations': {
      'particular-solution': ['Plot a particular solution', function (lv) {
        var a = lv === 'cp2' ? 2 : pick([2, -2]), b = lv === 'cp2' ? R(-2, 2) : R(-3, 3), x0 = lv === 'honors' ? pick([1, -1]) : 0, y0 = R(-3, 3);
        var Fp = [0, b, a / 2], C = y0 - ev(Fp, x0), F = [C, b, a / 2], X = xs(-2, 2), P = X.map(function (x) { return [x, ev(F, x)]; });
        if (!P.every(function (p) { return inGrid(p[1]); })) return null;
        return { prompt: 'y = f(x) is the solution of dy/dx = ' + poly([b, a]) + ' with f(' + M(x0) + ') = ' + M(y0) + '. Plot f(x) for x = −2, −1, 0, 1, 2.', tool: 'points', target: { points: P }, feedback: FB_PTS,
          key: key({ f: function (x) { return ev(F, x); }, from: LO, to: HI }, null, P, 'x', 'y'), alt: 'Graph of the particular solution y = ' + poly(F) + ' with the points ' + P.map(pt).join(', ') + '.',
          steps: ['Integrate both sides: y = ' + poly([0, b, a / 2]) + ' + C.', 'f(' + M(x0) + ') = ' + M(y0) + ' gives C = ' + M(C) + ', so y = ' + poly(F) + '.', 'Values: ' + P.map(function (p) { return 'f(' + M(p[0]) + ') = ' + M(p[1]); }).join('; ') + '.'] };
      }]
    }
  };
  function item(id, skillId, r) {
    var plot = { tool: r.tool, target: r.target, feedback: r.feedback, answerKey: { svg: r.key, alt: r.alt }, check: { type: 'exact-after-snap' }, grid: GRID };
    if (r.tool === 'points') plot.labels = r.target.points.map(function () { return ''; });
    return { id: id, skillId: skillId, prompt: r.prompt, solutionSteps: r.steps, plot: plot };
  }
  G.MK_CAL_PLOT = {
    units: Object.keys(MAKERS),
    makers: MAKERS,
    skills: function (unitId) { var m = MAKERS[unitId] || {}; return Object.keys(m).map(function (k) { return { id: k, name: m[k][0] }; }); },
    pool: function (unitId, level, skillId, n) {
      var m = MAKERS[unitId]; if (!m) return [];
      var ids = skillId ? [skillId] : Object.keys(m), out = [], seen = {}, tries = 0;
      while (out.length < (n || 12) && tries++ < 2000) {
        var id = ids[out.length % ids.length], r = m[id] && m[id][1](level || 'cp1'); if (!r || seen[r.prompt]) continue; seen[r.prompt] = 1;
        out.push(item('cal-plot-' + id + '-' + out.length, id, r));
      }
      return out;
    }
  };
})(typeof window !== 'undefined' ? window : globalThis);
