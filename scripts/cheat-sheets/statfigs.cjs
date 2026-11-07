/* Statistics figures for cheat sheets: box plots, scatterplots (with a line), residual plots and normal curves
   with shaded regions. Every figure is drawn from numbers, so it always matches the example it illustrates. */
'use strict';
const { svg } = require('./figs.cjs');
const INK = '#1f2a6b', BLUE = '#2563eb', PINK = '#db2777', GREEN = '#16a34a', GRID = '#d5dbe8';
const fmt = n => (Math.round(n * 100) / 100).toString().replace('-', '−');

/* Horizontal box plot on a number line. s = {min, q1, med, q3, max, outliers:[...], lo, hi, step, w, inches} */
function boxplot(s) {
  const W = s.w || 300, H = 62, L = 14, R = W - 14, X = v => L + (v - s.lo) / (s.hi - s.lo) * (R - L);
  let b = `<line x1="${L}" y1="44" x2="${R}" y2="44" stroke="#333" stroke-width="1.2"/>`;
  for (let v = s.lo; v <= s.hi + 1e-9; v += s.step) b += `<line x1="${X(v)}" y1="41" x2="${X(v)}" y2="47" stroke="#333"/><text x="${X(v)}" y="58" font-size="9" text-anchor="middle">${fmt(v)}</text>`;
  b += `<line x1="${X(s.min)}" y1="20" x2="${X(s.q1)}" y2="20" stroke="${INK}" stroke-width="1.6"/><line x1="${X(s.q3)}" y1="20" x2="${X(s.max)}" y2="20" stroke="${INK}" stroke-width="1.6"/>`;
  b += `<line x1="${X(s.min)}" y1="14" x2="${X(s.min)}" y2="26" stroke="${INK}" stroke-width="1.6"/><line x1="${X(s.max)}" y1="14" x2="${X(s.max)}" y2="26" stroke="${INK}" stroke-width="1.6"/>`;
  b += `<rect x="${X(s.q1)}" y="8" width="${X(s.q3) - X(s.q1)}" height="24" fill="#e6efff" stroke="${BLUE}" stroke-width="1.8"/><line x1="${X(s.med)}" y1="8" x2="${X(s.med)}" y2="32" stroke="${BLUE}" stroke-width="2.4"/>`;
  (s.outliers || []).forEach(o => { b += `<circle cx="${X(o)}" cy="20" r="3.6" fill="#fff" stroke="${PINK}" stroke-width="1.8"/><text x="${X(o)}" y="6" font-size="8.5" fill="${PINK}" text-anchor="middle" font-weight="700">outlier</text>`; });
  return svg(W, H, b, s.inches || 2.9);
}

/* Scatterplot. o = {pts:[[x,y]], xlo,xhi,ylo,yhi, xstep, ystep, line:[a,b] (y = a + bx), xlab, ylab, w, h, inches, resid:true (zero line)} */
function scatter(o) {
  const W = o.w || 240, H = o.h || 150, L = 30, R = W - 8, T = 8, B = H - 26;
  const X = x => L + (x - o.xlo) / (o.xhi - o.xlo) * (R - L), Y = y => B - (y - o.ylo) / (o.yhi - o.ylo) * (B - T);
  let b = `<rect x="${L}" y="${T}" width="${R - L}" height="${B - T}" fill="#fff" stroke="#999"/>`;
  for (let v = o.xlo; v <= o.xhi + 1e-9; v += o.xstep) b += `<line x1="${X(v)}" y1="${T}" x2="${X(v)}" y2="${B}" stroke="${GRID}" stroke-width=".7"/><text x="${X(v)}" y="${B + 11}" font-size="9" text-anchor="middle">${fmt(v)}</text>`;
  for (let v = o.ylo; v <= o.yhi + 1e-9; v += o.ystep) b += `<line x1="${L}" y1="${Y(v)}" x2="${R}" y2="${Y(v)}" stroke="${GRID}" stroke-width=".7"/><text x="${L - 4}" y="${Y(v) + 3}" font-size="9" text-anchor="end">${fmt(v)}</text>`;
  if (o.resid) b += `<line x1="${L}" y1="${Y(0)}" x2="${R}" y2="${Y(0)}" stroke="${PINK}" stroke-width="1.6" stroke-dasharray="5 4"/>`;
  if (o.line) b += `<line x1="${X(o.xlo)}" y1="${Y(o.line[0] + o.line[1] * o.xlo)}" x2="${X(o.xhi)}" y2="${Y(o.line[0] + o.line[1] * o.xhi)}" stroke="${PINK}" stroke-width="2"/>`;
  o.pts.forEach(p => { b += `<circle cx="${X(p[0])}" cy="${Y(p[1])}" r="3.3" fill="${BLUE}"/>`; });
  if (o.xlab) b += `<text x="${(L + R) / 2}" y="${H - 2}" font-size="9" text-anchor="middle" fill="${INK}" font-weight="700">${o.xlab}</text>`;
  if (o.ylab) b += `<text x="8" y="${(T + B) / 2}" font-size="9" text-anchor="middle" fill="${INK}" font-weight="700" transform="rotate(-90 8 ${(T + B) / 2})">${o.ylab}</text>`;
  return svg(W, H, b, o.inches || 2.3);
}

/* Standard normal curve from z = −3.5 to 3.5 with shaded regions. o = {shade:[[a,b,color]], marks:[{z, t}], labels:[{z, y (0–1 of peak), t, color}], w, inches} */
function normal(o) {
  const W = o.w || 280, H = 92, L = 10, R = W - 10, B = 70, T = 8, f = z => Math.exp(-z * z / 2);
  const X = z => L + (z + 3.5) / 7 * (R - L), Y = v => B - v * (B - T);
  const path = (a, c) => { const p = []; for (let i = 0; i <= 120; i++) { const z = a + (c - a) * i / 120; p.push(X(z).toFixed(1) + ' ' + Y(f(z)).toFixed(1)); } return p; };
  let b = '';
  (o.shade || []).forEach(s => { const a = Math.max(-3.5, s[0]), c = Math.min(3.5, s[1]); b += `<path d="M${X(a)} ${B} L${path(a, c).join(' L')} L${X(c)} ${B}Z" fill="${s[2] || BLUE}" fill-opacity=".28"/>`; });
  b += `<path d="M${path(-3.5, 3.5).join(' L')}" fill="none" stroke="${INK}" stroke-width="2"/><line x1="${L}" y1="${B}" x2="${R}" y2="${B}" stroke="#333" stroke-width="1.2"/>`;
  (o.marks || []).forEach(m => { b += `<line x1="${X(m.z)}" y1="${B - 3}" x2="${X(m.z)}" y2="${B + 3}" stroke="#333"/><text x="${X(m.z)}" y="${B + 14}" font-size="${m.fs || 8.5}" text-anchor="middle">${m.t}</text>`; });
  (o.labels || []).forEach(l => { b += `<text x="${X(l.z)}" y="${Y(l.y)}" font-size="${l.fs || 9.5}" text-anchor="middle" font-weight="700" fill="${l.color || INK}">${l.t}</text>`; });
  return svg(W, H, b, o.inches || 2.7);
}

/* Standard normal tail area P(Z > z) by numerical integration (used by the checks). */
function upper(z) { let s = 0; const h = 0.0005; for (let x = z; x < 9; x += h) { const m = x + h / 2; s += Math.exp(-m * m / 2) * h; } return s / Math.sqrt(2 * Math.PI); }

module.exports = { boxplot, scatter, normal, upper };
