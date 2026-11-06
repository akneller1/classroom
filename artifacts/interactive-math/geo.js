/* Mr. K's Classroom: geometry helpers for the Interactive Math tools (loaded after lab.js).
   Lab.geo: point math. Lab.geoGraph(g): angle arcs, tick marks and labels on a Lab.graph with equal x and y scales. */
(function (G) {
'use strict';
var L = G.Lab;
var D = Math.PI / 180;
var geo = {
  dist: function (A, B) { return Math.hypot(B[0] - A[0], B[1] - A[1]); },
  mid: function (A, B) { return [(A[0] + B[0]) / 2, (A[1] + B[1]) / 2]; },
  dir: function (A, B) { return Math.atan2(B[1] - A[1], B[0] - A[0]) / D; },           // degrees
  angle: function (A, V, B) {                                                          // angle AVB in degrees, 0–180
    var a = Math.atan2(A[1] - V[1], A[0] - V[0]), b = Math.atan2(B[1] - V[1], B[0] - V[0]);
    var d = Math.abs(a - b) / D; return d > 180 ? 360 - d : d;
  },
  polar: function (C, r, deg) { return [C[0] + r * Math.cos(deg * D), C[1] + r * Math.sin(deg * D)]; },
  lerp: function (A, B, t) { return [A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t]; },
  area: function (P) { var s = 0; for (var i = 0; i < P.length; i++) { var a = P[i], b = P[(i + 1) % P.length]; s += a[0] * b[1] - b[0] * a[1]; } return s / 2; },
  /* Intersection of lines P1P2 and P3P4 (null if parallel). */
  meet: function (P1, P2, P3, P4) {
    var d = (P1[0] - P2[0]) * (P3[1] - P4[1]) - (P1[1] - P2[1]) * (P3[0] - P4[0]);
    if (Math.abs(d) < 1e-12) return null;
    var a = P1[0] * P2[1] - P1[1] * P2[0], b = P3[0] * P4[1] - P3[1] * P4[0];
    return [(a * (P3[0] - P4[0]) - (P1[0] - P2[0]) * b) / d, (a * (P3[1] - P4[1]) - (P1[1] - P2[1]) * b) / d];
  },
  /* Foot of the perpendicular from P to line AB. */
  foot: function (P, A, B) { var dx = B[0] - A[0], dy = B[1] - A[1], t = ((P[0] - A[0]) * dx + (P[1] - A[1]) * dy) / (dx * dx + dy * dy); return [A[0] + t * dx, A[1] + t * dy]; },
  /* √n in simplest radical form, as text: 3√2, 5, √7. */
  radical: function (n) {
    n = Math.round(n); if (n < 0) return null;
    var out = 1, inside = n;
    for (var f = 2; f * f <= inside; f++) while (inside % (f * f) === 0) { inside /= f * f; out *= f; }
    return inside === 1 ? String(out) : (out === 1 ? '' : out) + '√' + inside;
  }
};
function col(c) { return c && c.indexOf('#') !== 0 && c.indexOf('var(') !== 0 && c !== 'none' ? 'var(--' + c + ')' : c; }
function geoGraph(g) {
  return {
    /* Arc for angle A-V-B (the smaller angle), radius r in data units, with an optional label. Right angles get a square. */
    angle: function (A, V, B, p) {
      p = p || {};
      var r = p.r || 0.9, a = geo.dir(V, A), b = geo.dir(V, B), m = geo.angle(A, V, B);
      var start = a, sweep = ((b - a) % 360 + 360) % 360; if (sweep > 180) { start = b; sweep = 360 - sweep; }
      var c = col(p.color || 'orange');
      if (!p.noSquare && Math.abs(m - 90) < 0.5) {
        var s = r * 0.7, u = geo.polar([0, 0], s, start), w = geo.polar([0, 0], s, start + 90);
        var pts = [[V[0] + u[0], V[1] + u[1]], [V[0] + u[0] + w[0], V[1] + u[1] + w[1]], [V[0] + w[0], V[1] + w[1]]];
        L.s('path', { d: 'M' + pts.map(function (q) { return g.X(q[0]).toFixed(1) + ' ' + g.Y(q[1]).toFixed(1); }).join(' L'), fill: 'none', stroke: c, 'stroke-width': p.width || 3 }, g.layer);
      } else {
        var P0 = geo.polar(V, r, start), P1 = geo.polar(V, r, start + sweep), R = Math.abs(g.X(r) - g.X(0));
        var d = 'M' + g.X(P0[0]).toFixed(1) + ' ' + g.Y(P0[1]).toFixed(1) + ' A ' + R.toFixed(1) + ' ' + R.toFixed(1) + ' 0 0 0 ' + g.X(P1[0]).toFixed(1) + ' ' + g.Y(P1[1]).toFixed(1);
        if (p.fill) L.s('path', { d: d + ' L ' + g.X(V[0]).toFixed(1) + ' ' + g.Y(V[1]).toFixed(1) + ' Z', fill: c, 'fill-opacity': p.fillOpacity || 0.25, stroke: 'none' }, g.layer);
        L.s('path', { d: d, fill: 'none', stroke: c, 'stroke-width': p.width || 3 }, g.layer);
      }
      if (p.label != null) { var Lp = geo.polar(V, r + (p.labelGap || 0.55), start + sweep / 2); g.text(Lp[0], Lp[1], p.label, { anchor: 'middle', dy: 5, color: p.labelColor || p.color || 'ink', size: p.size || 15 }); }
      return m;
    },
    /* n tick marks across segment AB (to show congruent sides). */
    ticks: function (A, B, n, p) {
      p = p || {}; var M = geo.mid(A, B), d = geo.dir(A, B), len = p.len || 0.28, gap = p.gap || 0.18;
      for (var i = 0; i < n; i++) {
        var off = (i - (n - 1) / 2) * gap, C = geo.polar(M, off, d), P1 = geo.polar(C, len, d + 90), P2 = geo.polar(C, len, d - 90);
        g.line(P1[0], P1[1], P2[0], P2[1], { color: p.color || 'ink', width: 2.5 });
      }
    },
    /* Label next to a vertex, pushed away from the polygon's center. */
    vertexLabel: function (P, center, text, p) {
      p = p || {}; var d = geo.dir(center, P), Q = geo.polar(P, p.gap || 0.7, d);
      g.text(Q[0], Q[1], text, { anchor: 'middle', dy: 6, color: p.color || 'ink', size: p.size || 17 });
    },
    /* Segment label at the midpoint, offset outward. */
    sideLabel: function (A, B, center, text, p) {
      p = p || {}; var M = geo.mid(A, B), d = geo.dir(A, B), n1 = geo.polar(M, 1, d + 90), n2 = geo.polar(M, 1, d - 90);
      var out = geo.dist(n1, center) > geo.dist(n2, center) ? d + 90 : d - 90, Q = geo.polar(M, p.gap || 0.6, out);
      g.text(Q[0], Q[1], text, { anchor: 'middle', dy: 5, color: p.color || 'ink', size: p.size || 14 });
    },
    polygon: function (P, p) {
      p = p || {};
      return L.s('polygon', { points: P.map(function (q) { return g.X(q[0]).toFixed(1) + ',' + g.Y(q[1]).toFixed(1); }).join(' '), fill: p.fill ? col(p.fill) : 'none', 'fill-opacity': p.fillOpacity == null ? 0.15 : p.fillOpacity,
        stroke: col(p.stroke || 'blue'), 'stroke-width': p.width || 4, 'stroke-linejoin': 'round', 'stroke-dasharray': p.dash || null }, p.layer || g.layer);
    },
    circle: function (C, r, p) {
      p = p || {}; var R = Math.abs(g.X(r) - g.X(0));
      return L.s('circle', { cx: g.X(C[0]), cy: g.Y(C[1]), r: R, fill: p.fill ? col(p.fill) : 'none', 'fill-opacity': p.fillOpacity == null ? 0.12 : p.fillOpacity, stroke: col(p.stroke || 'ink'), 'stroke-width': p.width || 3, 'stroke-dasharray': p.dash || null }, p.layer || g.layer);
    }
  };
}
L.geo = geo; L.geoGraph = geoGraph;
L.deg = function (x, dp) { return L.num(x, dp == null ? 1 : dp) + '°'; };
})(window);
