/* SVG figures for the Discrete Math cheat sheets: Venn diagrams (with shaded regions), graphs and digraphs (loops and
   parallel edges allowed), possibility trees and small truth tables. Every figure is drawn from data, so it matches its example. */
'use strict';
const INK = '#1f2a6b', SH = '#93c5fd';
const svgOpen = (w, h, inches) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${inches.toFixed(2)}in" font-family="DejaVu Sans,sans-serif">`;

/* Venn diagram. sets: 2 or 3 labels; shade: list of region keys ('A', 'AB', 'ABC', '' = outside, ...); labels: {key: text} */
function venn(o) {
  const n = o.sets.length, W = 220, H = n === 2 ? 130 : 170, r = n === 2 ? 46 : 44;
  const C = n === 2 ? [[84, 66], [136, 66]] : [[88, 66], [132, 66], [110, 104]];
  const id = o.id || 'v';
  let s = svgOpen(W, H, o.inches || 1.6);
  s += `<defs>${C.map((c, i) => `<clipPath id="${id}c${i}"><circle cx="${c[0]}" cy="${c[1]}" r="${r}"/></clipPath>`).join('')}` +
    `${C.map((c, i) => `<mask id="${id}m${i}"><rect width="${W}" height="${H}" fill="#fff"/><circle cx="${c[0]}" cy="${c[1]}" r="${r}" fill="#000"/></mask>`).join('')}</defs>`;
  s += `<rect x="4" y="4" width="${W - 8}" height="${H - 8}" fill="#fff" stroke="${INK}" stroke-width="1.6"/>`;
  (o.shade || []).forEach(key => {
    // build nested groups: inside sets in key (clip), outside sets not in key (mask)
    let inner = `<rect width="${W}" height="${H}" fill="${SH}"/>`;
    o.sets.forEach((L, i) => { inner = key.includes(L) ? `<g clip-path="url(#${id}c${i})">${inner}</g>` : `<g mask="url(#${id}m${i})">${inner}</g>`; });
    s += `<g>${inner}</g>`;
  });
  s += `<rect x="4" y="4" width="${W - 8}" height="${H - 8}" fill="none" stroke="${INK}" stroke-width="1.6"/>`;
  C.forEach(c => { s += `<circle cx="${c[0]}" cy="${c[1]}" r="${r}" fill="none" stroke="${INK}" stroke-width="1.6"/>`; });
  const lab = n === 2 ? [[40, 26], [180, 26]] : [[38, 24], [182, 24], [110, 164]];
  o.sets.forEach((L, i) => { s += `<text x="${lab[i][0]}" y="${lab[i][1]}" font-size="14" font-weight="700" fill="${INK}" text-anchor="middle">${L}</text>`; });
  s += `<text x="14" y="${H - 12}" font-size="11" font-style="italic" fill="${INK}">${o.universe || 'U'}</text>`;
  const pos = n === 2 ? { AB: [110, 70], A: [66, 70], B: [154, 70], '': [196, H - 12] } :
    { ABC: [110, 80], AB: [110, 50], AC: [86, 92], BC: [134, 92], A: [70, 56], B: [150, 56], C: [110, 128], '': [198, H - 12] };
  Object.entries(o.labels || {}).forEach(([k, t]) => { const p = pos[k]; s += `<text x="${p[0]}" y="${p[1]}" font-size="10.5" text-anchor="middle" fill="#111">${t}</text>`; });
  return s + '</svg>';
}

/* Graph. v: {name: [x, y]} in a 0..100 box; e: [[a, b], ...] (repeat a pair for parallel edges; [a, a] = loop);
   directed: arrows; hl: list of edge indexes drawn bold; w: optional edge labels */
function graph(o) {
  const W = o.w || 160, H = o.h || 120, P = 14, sx = (W - 2 * P) / 100, sy = (H - 2 * P) / 100;
  const X = p => [P + p[0] * sx, P + p[1] * sy];
  let s = svgOpen(W, H, o.inches || 1.4) + `<defs><marker id="${o.id || 'g'}ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="${INK}"/></marker></defs>`;
  const seen = {};
  o.e.forEach((ed, i) => {
    const [a, b] = ed, pa = X(o.v[a]), pb = X(o.v[b]), bold = (o.hl || []).includes(i), col = bold ? '#db2777' : INK, sw = bold ? 3 : 1.6;
    if (a === b) {
      s += `<circle cx="${pa[0]}" cy="${pa[1] - 13}" r="8" fill="none" stroke="${col}" stroke-width="${sw}"/>`;
      return;
    }
    const key = [a, b].sort().join('|'), k = seen[key] = (seen[key] || 0) + 1;
    const dx = pb[0] - pa[0], dy = pb[1] - pa[1], L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L, r = 9;
    const s1 = [pa[0] + ux * r, pa[1] + uy * r], s2 = [pb[0] - ux * (r + (o.directed ? 1 : 0)), pb[1] - uy * (r + (o.directed ? 1 : 0))];
    const bend = k === 1 ? (o.directed && o.e.some(f => f[0] === b && f[1] === a) ? 10 : 0) : (k % 2 ? 1 : -1) * 12 * Math.ceil((k - 1) / 2 + .5);
    const mx = (s1[0] + s2[0]) / 2 - uy * bend, my = (s1[1] + s2[1]) / 2 + ux * bend;
    s += `<path d="M${s1[0].toFixed(1)} ${s1[1].toFixed(1)} Q${mx.toFixed(1)} ${my.toFixed(1)} ${s2[0].toFixed(1)} ${s2[1].toFixed(1)}" fill="none" stroke="${col}" stroke-width="${sw}"${o.directed ? ` marker-end="url(#${o.id || 'g'}ar)"` : ''}/>`;
    if (o.wt) s += `<text x="${mx - uy * 6}" y="${my + ux * 6 + 3}" font-size="9.5" text-anchor="middle" fill="#7c2d12" font-weight="700">${o.wt[i]}</text>`;
  });
  Object.entries(o.v).forEach(([nm, p]) => { const q = X(p); s += `<circle cx="${q[0]}" cy="${q[1]}" r="9" fill="${(o.color || {})[nm] || '#fff'}" stroke="${INK}" stroke-width="1.5"/><text x="${q[0]}" y="${q[1] + 3.5}" font-size="10" font-weight="700" text-anchor="middle" fill="${INK}">${nm}</text>`; });
  return s + '</svg>';
}

/* Possibility tree: levels = [['H','T'], ['H','T'], ...] */
function tree(o) {
  const lv = o.levels, leaves = lv.reduce((a, l) => a * l.length, 1), W = 40 + 60 * lv.length, H = Math.max(60, leaves * (o.gap || 13) + 10);
  let s = svgOpen(W, H, o.inches || 1.5);
  function draw(x, y0, y1, d) {
    const y = (y0 + y1) / 2;
    if (d === lv.length) return;
    lv[d].forEach((lab, i) => {
      const a = y0 + (y1 - y0) * i / lv[d].length, b = y0 + (y1 - y0) * (i + 1) / lv[d].length, ny = (a + b) / 2;
      s += `<line x1="${x}" y1="${y}" x2="${x + 44}" y2="${ny}" stroke="${INK}" stroke-width="1.2"/><text x="${x + 47}" y="${ny + 3.5}" font-size="10" fill="#111">${lab}</text>`;
      draw(x + 60, a, b, d + 1);
    });
  }
  draw(8, 4, H - 4, 0);
  return s + `<circle cx="8" cy="${H / 2}" r="3" fill="${INK}"/></svg>`;
}

module.exports = { venn, graph, tree };
