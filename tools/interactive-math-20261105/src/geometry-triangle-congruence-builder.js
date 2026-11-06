/* Vertex A at the origin, side AB along the x-axis. Angles in degrees. Sides: a = BC, b = AC, c = AB. */
var Gm = L.geo, R = Math.PI / 180;
var MODES = {
  SSS: { parts: [['a', 'side BC', 'side', 6], ['b', 'side AC', 'side', 5], ['c', 'side AB', 'side', 7]] },
  SAS: { parts: [['b', 'side AC', 'side', 5], ['A', 'included angle A', 'angle', 50], ['c', 'side AB', 'side', 7]] },
  ASA: { parts: [['A', 'angle A', 'angle', 50], ['c', 'included side AB', 'side', 7], ['B', 'angle B', 'angle', 60]] },
  AAS: { parts: [['A', 'angle A', 'angle', 50], ['B', 'angle B', 'angle', 60], ['a', 'side BC (not between them)', 'side', 6]] },
  SSA: { parts: [['b', 'side AC', 'side', 7], ['a', 'side BC (opposite A)', 'side', 5], ['A', 'angle A (not between the sides)', 'angle', 40]] },
  AAA: { parts: [['A', 'angle A', 'angle', 50], ['B', 'angle B', 'angle', 60]] }
};
var st = { mode: 'SSS', v: {}, seen: {} };
Object.keys(MODES).forEach(function (k) { MODES[k].parts.forEach(function (p) { st.v[k + p[0]] = p[3]; }); });
var g = L.graph(P.stage, { xmin: -3, xmax: 15, ymin: -2.5, ymax: 12, width: 620, height: 500, noGrid: true, label: 'Triangles that match the given parts' });
var gg = L.geoGraph(g);
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
L.chips(P.panel, { label: 'What you are given', value: st.mode, options: Object.keys(MODES).map(function (k) { return { value: k, label: k }; }), onChange: function (v) { st.mode = v; build(); draw(); } });
var ctrl = L.h('div', { style: 'display:grid;gap:12px' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'With SSS, choose three lengths that <b>can\'t</b> make a triangle.', check: function () { return st.seen.sssNone; } },
  { text: 'With SSA, make <b>two different</b> triangles from the same three parts.', check: function () { return st.seen.ssa2; } },
  { text: 'With SSA, make exactly one triangle. What did you change?', check: function () { return st.seen.ssa1; } },
  { text: 'With AAA, see why matching angles don\'t prove congruence.', check: function () { return st.mode === 'AAA'; } },
  { text: 'Try SAS, ASA and AAS. Does each give exactly one triangle?', check: function () { return st.seen.SAS && st.seen.ASA && st.seen.AAS; } }
]);
function build() {
  ctrl.innerHTML = '';
  MODES[st.mode].parts.forEach(function (p) {
    var key = st.mode + p[0];
    L.slider(ctrl, { id: key, label: p[1], min: p[2] === 'side' ? 2 : 15, max: p[2] === 'side' ? 11 : 140, step: p[2] === 'side' ? 0.5 : 5, value: st.v[key], color: p[2] === 'side' ? 'blue' : 'orange', format: p[2] === 'side' ? L.nice : L.deg, onInput: function (x) { st.v[key] = x; draw(); } });
  });
}
function tri(A, c, Cpt) { return [[0, 0], [c, 0], Cpt]; }
/* Returns a list of triangles [[A,B,C], ...] (or 'many' for AAA). */
function solve() {
  var v = function (k) { return st.v[st.mode + k]; }, out = [];
  if (st.mode === 'SSS') {
    var a = v('a'), b = v('b'), c = v('c');
    if (a + b <= c || a + c <= b || b + c <= a) return [];
    var x = (b * b + c * c - a * a) / (2 * c); out.push(tri(0, c, [x, Math.sqrt(Math.max(0, b * b - x * x))]));
  } else if (st.mode === 'SAS') { var b2 = v('b'), A = v('A'), c2 = v('c'); out.push(tri(0, c2, [b2 * Math.cos(A * R), b2 * Math.sin(A * R)])); }
  else if (st.mode === 'ASA' || st.mode === 'AAS') {
    var A1 = v('A'), B1 = v('B'); if (A1 + B1 >= 180) return [];
    var C1 = 180 - A1 - B1, cc = st.mode === 'ASA' ? v('c') : v('a') * Math.sin(C1 * R) / Math.sin(A1 * R);
    var bb = cc * Math.sin(B1 * R) / Math.sin(C1 * R); out.push(tri(0, cc, [bb * Math.cos(A1 * R), bb * Math.sin(A1 * R)]));
  } else if (st.mode === 'SSA') {
    // C is at distance b along angle A from the origin; B on the x-axis with |BC| = a
    var b3 = v('b'), a3 = v('a'), A3 = v('A'), C = [b3 * Math.cos(A3 * R), b3 * Math.sin(A3 * R)], h = C[1];
    if (a3 < h - 1e-9) return [];
    var dx = Math.sqrt(Math.max(0, a3 * a3 - h * h));
    [C[0] - dx, C[0] + dx].forEach(function (bx) { if (bx > 1e-9 && !out.some(function (t) { return Math.abs(t[1][0] - bx) < 1e-6; })) out.push([[0, 0], [bx, 0], C]); });
  } else {
    var A4 = v('A'), B4 = v('B'); if (A4 + B4 >= 180) return [];
    var C4 = 180 - A4 - B4;
    [4, 7, 10].forEach(function (cc) { var bb = cc * Math.sin(B4 * R) / Math.sin(C4 * R); out.push(tri(0, cc, [bb * Math.cos(A4 * R), bb * Math.sin(A4 * R)])); });
  }
  return out;
}
var COLORS = ['blue', 'purple', 'green'];
var draw = L.scheduler(function () {
  var T = solve();
  g.clear();
  // fit the view to the triangles
  var xs = [0, 8], ys = [0, 6]; T.forEach(function (t) { t.forEach(function (p) { xs.push(p[0]); ys.push(p[1]); }); });
  var x0 = Math.min.apply(null, xs) - 1.5, x1 = Math.max.apply(null, xs) + 1.5, y0 = Math.min.apply(null, ys) - 1.5, y1 = Math.max.apply(null, ys) + 1.5;
  var w = Math.max(x1 - x0, (y1 - y0) * 620 / 500), hgt = w * 500 / 620;
  g.setView({ xmin: x0, xmax: x0 + w, ymin: y0, ymax: y0 + hgt });
  T.forEach(function (t, i) {
    var col = COLORS[i % 3], cen = [(t[0][0] + t[1][0] + t[2][0]) / 3, (t[0][1] + t[1][1] + t[2][1]) / 3];
    gg.polygon(t, { stroke: col, fill: col, fillOpacity: 0.08, width: 4, dash: i ? '10 6' : null });
    gg.vertexLabel(t[2], cen, T.length > 1 && st.mode !== 'AAA' ? 'C' : 'C', { color: col });
    if (i === 0 || st.mode === 'SSA') gg.vertexLabel(t[1], cen, T.length > 1 && st.mode === 'SSA' ? 'B' + (i + 1) : 'B', { color: col });
  });
  if (T.length) {
    var t0 = T[0], cen0 = [(t0[0][0] + t0[1][0] + t0[2][0]) / 3, (t0[0][1] + t0[1][1] + t0[2][1]) / 3];
    gg.vertexLabel(t0[0], cen0, 'A');
    MODES[st.mode].parts.forEach(function (p) {
      if (p[2] === 'angle') { var V = p[0] === 'A' ? t0[0] : t0[1], O1 = p[0] === 'A' ? t0[1] : t0[0]; gg.angle(O1, V, t0[2], { r: 1, color: 'orange', fill: true, label: L.num(st.v[st.mode + p[0]]) + '°', labelColor: 'orange' }); }
    });
  }
  var n = T.length, verdict;
  if (!n) verdict = '<span class="c-red"><b>No triangle</b> fits these parts.</span>' + (st.mode === 'SSS' ? ' Two sides must add to more than the third.' : st.mode === 'SSA' ? ' Side BC is too short to reach line AB.' : ' The two angles already add to 180° or more.');
  else if (st.mode === 'AAA') verdict = '<span class="c-red"><b>Infinitely many triangles</b>, all the same shape but different sizes.</span> AAA proves similarity, not congruence.';
  else if (n === 2) verdict = '<span class="c-red"><b>Two different triangles</b> fit the same parts</span> (blue and dashed purple). SSA is not a congruence shortcut.';
  else verdict = '<span class="c-green"><b>Exactly one triangle</b> fits.</span> ' + (st.mode === 'SSA' ? 'This time SSA worked, but it doesn\'t always.' : st.mode + ' proves two triangles congruent.');
  read.innerHTML = st.mode + '<div class="sub" style="margin-top:6px">' + verdict + '</div>';
  if (st.mode === 'SSS' && !n) st.seen.sssNone = true;
  if (st.mode === 'SSA' && n === 2) st.seen.ssa2 = true;
  if (st.mode === 'SSA' && n === 1) st.seen.ssa1 = true;
  if (n === 1 && ['SAS', 'ASA', 'AAS'].indexOf(st.mode) >= 0) st.seen[st.mode] = true;
  ch.update();
});
build(); draw();
