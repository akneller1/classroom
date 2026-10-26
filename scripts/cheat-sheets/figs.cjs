/* Small SVG figures for cheat sheets: number lines and coordinate planes (curves, points, shaded half-planes).
   Every figure is drawn from numbers, so it always matches the example it illustrates. */
'use strict';
const C = { ink: '#1f2a6b', grid: '#d5dbe8', axis: '#333', a: '#2563eb', b: '#db2777', c: '#16a34a', d: '#ea7a12' };
const fmt = n => (Math.round(n * 100) / 100).toString().replace('-', '−');

/* Number line. segs: [{a, b, ac, bc, color}] where a or b may be null (ray to −∞ / +∞); ac/bc = closed circle.
   points: [{x, closed, color}] single dots. */
function nl(min, max, segs, opts) {
  opts = opts || {};
  const W = opts.w || 300, H = 46, L = 14, R = W - 14, step = opts.step || 1;
  const X = v => L + 8 + (v - min) / (max - min) * (R - L - 16);
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${(W / 96 * (opts.scale || 0.85)).toFixed(2)}in">`;
  s += `<line x1="${L}" y1="20" x2="${R}" y2="20" stroke="${C.axis}" stroke-width="1.5"/><path d="M${L - 2} 20 l7 -4 v8z M${R + 2} 20 l-7 -4 v8z" fill="${C.axis}"/>`;
  for (let v = min; v <= max + 1e-9; v += step) s += `<line x1="${X(v)}" y1="15" x2="${X(v)}" y2="25" stroke="${C.axis}"/><text x="${X(v)}" y="39" font-size="10" text-anchor="middle" font-family="DejaVu Sans,sans-serif">${fmt(v)}</text>`;
  (segs || []).forEach(g => {
    const col = g.color || C.a, x1 = g.a === null || g.a === undefined ? L + 2 : X(g.a), x2 = g.b === null || g.b === undefined ? R - 2 : X(g.b);
    s += `<line x1="${x1}" y1="20" x2="${x2}" y2="20" stroke="${col}" stroke-width="4"/>`;
    if (g.a === null || g.a === undefined) s += `<path d="M${L - 3} 20 l9 -6 v12z" fill="${col}"/>`;
    if (g.b === null || g.b === undefined) s += `<path d="M${R + 3} 20 l-9 -6 v12z" fill="${col}"/>`;
    if (g.a !== null && g.a !== undefined) s += `<circle cx="${X(g.a)}" cy="20" r="5" fill="${g.ac ? col : '#fff'}" stroke="${col}" stroke-width="2"/>`;
    if (g.b !== null && g.b !== undefined) s += `<circle cx="${X(g.b)}" cy="20" r="5" fill="${g.bc ? col : '#fff'}" stroke="${col}" stroke-width="2"/>`;
  });
  (opts.points || []).forEach(p => { s += `<circle cx="${X(p.x)}" cy="20" r="5" fill="${p.closed === false ? '#fff' : (p.color || C.a)}" stroke="${p.color || C.a}" stroke-width="2"/>`; });
  return s + '</svg>';
}

/* Coordinate plane. o: {xmin,xmax,ymin,ymax, size (in), fns:[{f, color, dashed, from, to}], vlines:[{x, color, dashed}],
   shade:[{f, side:'above'|'below', color}], vshade:[{x, side:'left'|'right'}], points:[{x,y,label,color,open}], labels:[{x,y,t}], grid:true, ticks:2} */
function plane(o) {
  const xmin = o.xmin, xmax = o.xmax, ymin = o.ymin, ymax = o.ymax, P = 14;
  const u = 200 / Math.max(xmax - xmin, ymax - ymin), W = (xmax - xmin) * u + 2 * P, H = (ymax - ymin) * u + 2 * P;
  const X = x => P + (x - xmin) * u, Y = y => P + (ymax - y) * u;
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W.toFixed(1)} ${H.toFixed(1)}" width="${(o.size || 1.5).toFixed(2)}in" font-family="DejaVu Sans,sans-serif">`;
  s += `<defs><clipPath id="c${o.id || 0}"><rect x="${X(xmin)}" y="${Y(ymax)}" width="${(xmax - xmin) * u}" height="${(ymax - ymin) * u}"/></clipPath></defs><rect x="0" y="0" width="${W}" height="${H}" fill="#fff"/>`;
  if (o.grid !== false) for (let x = Math.ceil(xmin); x <= xmax; x++) s += `<line x1="${X(x)}" y1="${Y(ymin)}" x2="${X(x)}" y2="${Y(ymax)}" stroke="${C.grid}" stroke-width=".7"/>`;
  if (o.grid !== false) for (let y = Math.ceil(ymin); y <= ymax; y++) s += `<line x1="${X(xmin)}" y1="${Y(y)}" x2="${X(xmax)}" y2="${Y(y)}" stroke="${C.grid}" stroke-width=".7"/>`;
  const g = [];
  (o.shade || []).forEach(sh => {
    const pts = []; for (let i = 0; i <= 80; i++) { const x = xmin + (xmax - xmin) * i / 80; pts.push([X(x), Y(sh.f(x))]); }
    const edge = sh.side === 'above' ? Y(ymax + 50) : Y(ymin - 50);
    g.push(`<path d="M${pts.map(p => p.join(' ')).join(' L')} L${X(xmax)} ${edge} L${X(xmin)} ${edge}Z" fill="${sh.color || C.a}" fill-opacity=".16"/>`);
  });
  (o.vshade || []).forEach(sh => g.push(`<rect x="${sh.side === 'left' ? X(xmin) : X(sh.x)}" y="${Y(ymax)}" width="${sh.side === 'left' ? X(sh.x) - X(xmin) : X(xmax) - X(sh.x)}" height="${(ymax - ymin) * u}" fill="${sh.color || C.a}" fill-opacity=".16"/>`));
  s += `<g clip-path="url(#c${o.id || 0})">${g.join('')}</g>`;
  if (ymin <= 0 && ymax >= 0) s += `<line x1="${X(xmin)}" y1="${Y(0)}" x2="${X(xmax)}" y2="${Y(0)}" stroke="${C.axis}" stroke-width="1.3"/>`;
  if (xmin <= 0 && xmax >= 0) s += `<line x1="${X(0)}" y1="${Y(ymin)}" x2="${X(0)}" y2="${Y(ymax)}" stroke="${C.axis}" stroke-width="1.3"/>`;
  const t = o.ticks || 0;
  if (t) {
    for (let x = Math.ceil(xmin / t) * t; x <= xmax; x += t) if (x !== 0) s += `<text x="${X(x)}" y="${Y(0) + 11}" font-size="9" text-anchor="middle">${fmt(x)}</text>`;
    for (let y = Math.ceil(ymin / t) * t; y <= ymax; y += t) if (y !== 0) s += `<text x="${X(0) - 4}" y="${Y(y) + 3}" font-size="9" text-anchor="end">${fmt(y)}</text>`;
  }
  const c = [];
  (o.fns || []).forEach(fn => {
    const a = fn.from !== undefined ? fn.from : xmin, b = fn.to !== undefined ? fn.to : xmax, pts = [];
    for (let i = 0; i <= 160; i++) { const x = a + (b - a) * i / 160, y = fn.f(x); if (isFinite(y) && y > ymin - 20 && y < ymax + 20) pts.push(X(x).toFixed(1) + ' ' + Y(y).toFixed(1)); }
    c.push(`<path d="M${pts.join(' L')}" fill="none" stroke="${fn.color || C.a}" stroke-width="2.2"${fn.dashed ? ' stroke-dasharray="6 4"' : ''}/>`);
  });
  (o.vlines || []).forEach(v => c.push(`<line x1="${X(v.x)}" y1="${Y(ymin)}" x2="${X(v.x)}" y2="${Y(ymax)}" stroke="${v.color || C.b}" stroke-width="1.8"${v.dashed !== false ? ' stroke-dasharray="5 4"' : ''}/>`));
  (o.segments || []).forEach(v => c.push(`<line x1="${X(v.x1)}" y1="${Y(v.y1)}" x2="${X(v.x2)}" y2="${Y(v.y2)}" stroke="${v.color || C.ink}" stroke-width="${v.w || 2}"${v.dashed ? ' stroke-dasharray="5 4"' : ''}/>`));
  (o.polys || []).forEach(v => c.push(`<polygon points="${v.pts.map(p => X(p[0]) + ',' + Y(p[1])).join(' ')}" fill="${v.fill || 'none'}" fill-opacity="${v.opacity || .2}" stroke="${v.color || C.a}" stroke-width="2"${v.dashed ? ' stroke-dasharray="5 4"' : ''}/>`));
  s += `<g clip-path="url(#c${o.id || 0})">${c.join('')}</g>`;
  (o.points || []).forEach(p => {
    s += `<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="3.6" fill="${p.open ? '#fff' : (p.color || C.ink)}" stroke="${p.color || C.ink}" stroke-width="1.6"/>`;
    if (p.label) s += `<text x="${X(p.x) + (p.dx || 5)}" y="${Y(p.y) + (p.dy || -5)}" font-size="${p.fs || 10}" fill="${p.color || C.ink}" font-weight="700"${p.anchor ? ' text-anchor="' + p.anchor + '"' : ''}>${p.label}</text>`;
  });
  (o.labels || []).forEach(l => { s += `<text x="${X(l.x)}" y="${Y(l.y)}" font-size="${l.fs || 10}" fill="${l.color || C.ink}" font-weight="${l.bold === false ? 400 : 700}" text-anchor="${l.anchor || 'middle'}">${l.t}</text>`; });
  return s + '</svg>';
}
/* A free SVG (geometry diagrams): body is SVG markup in a w × h viewBox. */
function svg(w, h, body, inches) { return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${(inches || w / 96).toFixed(2)}in" font-family="DejaVu Sans,sans-serif" font-size="11">${body}</svg>`; }
module.exports = { nl, plane, svg, C };
