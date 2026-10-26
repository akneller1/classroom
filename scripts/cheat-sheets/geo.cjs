/* Geometry diagrams for cheat sheets (SVG strings). Every number on a diagram comes from the arguments. */
'use strict';
const { svg } = require('./figs.cjs');
const INK = '#1f2a6b', A = '#2563eb', B = '#db2777', G = '#16a34a', O = '#ea7a12';
const rad = d => d * Math.PI / 180;
const t = (x, y, s, o) => `<text x="${x}" y="${y}" font-size="${(o && o.fs) || 11}" fill="${(o && o.c) || INK}" font-weight="${(o && o.w) || 700}" text-anchor="${(o && o.a) || 'middle'}">${s}</text>`;
const dot = (x, y, c) => `<circle cx="${x}" cy="${y}" r="3" fill="${c || INK}"/>`;
const line = (x1, y1, x2, y2, c, w, dash) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${c || INK}" stroke-width="${w || 2}"${dash ? ' stroke-dasharray="5 4"' : ''}/>`;
const arrowHead = (x, y, ang, c) => { const a = rad(ang), l = 8; return `<path d="M${x} ${y} L${x - l * Math.cos(a - 0.4)} ${y - l * Math.sin(a - 0.4)} L${x - l * Math.cos(a + 0.4)} ${y - l * Math.sin(a + 0.4)}Z" fill="${c || INK}"/>`; };
const arc = (cx, cy, r, a1, a2, c, fill) => { const x1 = cx + r * Math.cos(rad(a1)), y1 = cy - r * Math.sin(rad(a1)), x2 = cx + r * Math.cos(rad(a2)), y2 = cy - r * Math.sin(rad(a2)); const large = Math.abs(a2 - a1) > 180 ? 1 : 0; return `<path d="${fill ? `M${cx} ${cy} L` : 'M'}${x1} ${y1} A${r} ${r} 0 ${large} 0 ${x2} ${y2}${fill ? 'Z' : ''}" fill="${fill ? (c || A) : 'none'}" fill-opacity="${fill ? .25 : 1}" stroke="${c || A}" stroke-width="1.6"/>`; };
const tick = (x1, y1, x2, y2, n) => { const mx = (x1 + x2) / 2, my = (y1 + y2) / 2, ang = Math.atan2(y2 - y1, x2 - x1), px = -Math.sin(ang), py = Math.cos(ang), dx = Math.cos(ang), dy = Math.sin(ang); let s = ''; for (let i = 0; i < (n || 1); i++) { const o = (i - ((n || 1) - 1) / 2) * 4; s += line(mx + dx * o - px * 5, my + dy * o - py * 5, mx + dx * o + px * 5, my + dy * o + py * 5, B, 1.6); } return s; };

/* Angle with vertex label and measure: deg in (0, 180]. */
function angle(deg, labels, o) {
  o = o || {}; const cx = 30, cy = 70, L = 90, x2 = cx + L * Math.cos(rad(deg)), y2 = cy - L * Math.sin(rad(deg));
  return svg(150, 90, line(cx, cy, cx + L, cy) + line(cx, cy, x2, y2) + (deg === 90 ? `<rect x="${cx}" y="${cy - 12}" width="12" height="12" fill="none" stroke="${B}" stroke-width="1.6"/>` : arc(cx, cy, 20, 0, deg, B, true)) +
    dot(cx, cy) + dot(cx + L, cy) + dot(x2, y2) + t(cx - 6, cy + 14, labels[1]) + t(cx + L + 8, cy + 4, labels[2]) + t(x2 + 6, y2 - 3, labels[0]) + (o.m ? t(cx + 38 * Math.cos(rad(deg / 2)), cy - 38 * Math.sin(rad(deg / 2)) + 4, o.m, { c: B }) : ''), o.in || 1.6);
}
/* Segment with points and optional lengths: pts [[label, x]], lens [[from, to, text]] (x in 0..1). */
function segment(pts, lens, o) {
  o = o || {}; const X = v => 15 + v * 200;
  let s = line(X(0), 30, X(1), 30);
  (lens || []).forEach(l => { s += t((X(l[0]) + X(l[1])) / 2, l[3] ? 52 : 20, l[2], { c: l[3] || A }); });
  (o.ticks || []).forEach(k => { s += tick(X(k[0]), 30, X(k[1]), 30, k[2]); });
  pts.forEach(p => { s += dot(X(p[1]), 30, p[2]) + t(X(p[1]), 47, p[0]); });
  return svg(230, 58, s, o.in || 2.5);
}
/* Two lines crossing: vertical angles and linear pairs. */
function crossing(a, o) {
  o = o || {}; const cx = 80, cy = 45, L = 70;
  const d1 = [Math.cos(rad(a)), -Math.sin(rad(a))];
  return svg(160, 90, line(cx - L, cy, cx + L, cy) + line(cx - L * d1[0], cy - L * d1[1], cx + L * d1[0], cy + L * d1[1]) + arc(cx, cy, 16, 0, a, B, true) + arc(cx, cy, 16, 180, 180 + a, B, true) + arc(cx, cy, 22, a, 180, G) +
    t(cx + 30, cy - 8, o.l1 || '1', { c: B }) + t(cx - 30, cy + 16, o.l3 || '3', { c: B }) + t(cx - 4, cy - 26, o.l2 || '2', { c: G }), o.in || 1.7);
}
/* Parallel lines cut by a transversal, angles numbered 1–8. */
function parallels(o) {
  o = o || {}; const y1 = 25, y2 = 75;
  const tx = y => 70 + (y - 50) * -0.7;
  let b = line(10, y1, 210, y1) + line(10, y2, 210, y2) + line(tx(0), 0, tx(100), 100, A) + arrowHead(206, y1, 0) + arrowHead(206, y2, 0);
  [[y1, 0], [y2, 4]].forEach(([y, k]) => { const x = tx(y); [[x + 14, y - 5, 1], [x - 14, y - 5, 2], [x - 14, y + 14, 3], [x + 14, y + 14, 4]].forEach(p => { b += t(p[0], p[1], p[2] + k, { fs: 10, c: B }); }); });
  return svg(220, 100, b, o.in || 2.3);
}
/* Triangle from three points with labels, optional side texts and tick marks. */
function triangle(P, labels, o) {
  o = o || {}; let s = `<polygon points="${P.map(p => p.join(',')).join(' ')}" fill="${o.fill || '#e6efff'}" stroke="${INK}" stroke-width="2"/>`;
  (o.ticks || []).forEach(k => { s += tick(P[k[0]][0], P[k[0]][1], P[k[1]][0], P[k[1]][1], k[2]); });
  (o.sides || []).forEach(k => { const m = [(P[k[0]][0] + P[k[1]][0]) / 2, (P[k[0]][1] + P[k[1]][1]) / 2]; s += t(m[0] + (k[3] || 0), m[1] + (k[4] || 0), k[2], { c: A }); });
  (o.angles || []).forEach(k => { s += t(P[k[0]][0] + k[2], P[k[0]][1] + k[3], k[1], { c: B, fs: 10 }); });
  if (o.right !== undefined) { const p = P[o.right]; s += `<rect x="${p[0] + (o.rdx || 0)}" y="${p[1] + (o.rdy || -12)}" width="12" height="12" fill="none" stroke="${B}" stroke-width="1.5"/>`; }
  labels.forEach((l, i) => { if (l) s += t(P[i][0] + (o.lo ? o.lo[i][0] : 0), P[i][1] + (o.lo ? o.lo[i][1] : 0), l); });
  return svg(o.w || 200, o.h || 120, s, o.in || 1.9);
}
module.exports = { angle, segment, crossing, parallels, triangle, line, t, dot, arc, tick, svg, INK, A, B, G, O, rad };
