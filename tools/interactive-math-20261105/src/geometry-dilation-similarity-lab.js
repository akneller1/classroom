var Gm = L.geo;
var st = { A: [1, 1], B: [4, 1], C: [1, 3], O: [-3, -2], k: 1.5, seen: {} };
var g = L.graph(P.stage, { xmin: -10, xmax: 12, ymin: -8, ymax: 12, width: 600, height: 545, label: 'Dilation of triangle ABC' });
var gg = L.geoGraph(g);
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>preimage ABC</span><span><i style="background:var(--orange)"></i>image A′B′C′</span><span><i style="background:var(--purple)"></i>center of dilation O</span>');
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
L.slider(P.panel, { id: 'k', label: 'Scale factor k', min: 0.25, max: 3, step: 0.25, value: st.k, color: 'orange', format: L.nice, onInput: function (v) { st.k = v; draw(); } });
L.h('p', { class: 'sub' }, P.panel, 'Drag A, B, C and the center O.');
var tbl = L.table(P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Make an <b>enlargement</b> that doubles every side. What happens to the area?', check: function () { return st.k === 2; } },
  { text: 'Make a <b>reduction</b>. What kind of number is k?', check: function () { return st.k < 1; } },
  { text: 'Put the center O on vertex A. Which point doesn\'t move?', check: function () { return st.seen.onA; } },
  { text: 'Find the scale factor that makes the image\'s area 9 times the original.', check: function () { return st.k === 3; } },
  { text: 'Set k = 1. What is true about the two triangles?', check: function () { return st.k === 1; } }
]);
function dil(P0) { return [st.O[0] + st.k * (P0[0] - st.O[0]), st.O[1] + st.k * (P0[1] - st.O[1])]; }
var draw = L.scheduler(function () {
  var T = [st.A, st.B, st.C], I = T.map(dil), k = st.k;
  g.clear();
  I.forEach(function (q, i) { var far = Gm.dist(st.O, q) > Gm.dist(st.O, T[i]) ? q : T[i]; g.line(st.O[0], st.O[1], far[0], far[1], { color: 'purple', width: 1.5, dash: '5 5' }); });
  gg.polygon(T, { stroke: 'blue', fill: 'blue', fillOpacity: 0.12 });
  gg.polygon(I, { stroke: 'orange', fill: 'orange', fillOpacity: 0.12 });
  var cen = [(I[0][0] + I[1][0] + I[2][0]) / 3, (I[0][1] + I[1][1] + I[2][1]) / 3];
  ['A′', 'B′', 'C′'].forEach(function (n, i) { gg.vertexLabel(I[i], cen, n, { color: 'orange' }); });
  [['A', 'blue'], ['B', 'blue'], ['C', 'blue']].forEach(function (h) {
    var P0 = st[h[0]]; g.handle(P0[0], P0[1], { color: 'blue', snap: 1, r: 9, label: 'Vertex ' + h[0], onDrag: function (x, y) { st[h[0]] = [x, y]; draw(); } });
    g.text(P0[0], P0[1], h[0], { dx: -12, dy: 20, anchor: 'end', color: 'blue' });
  });
  g.handle(st.O[0], st.O[1], { color: 'purple', snap: 1, label: 'Center O', onDrag: function (x, y) { st.O = [x, y]; draw(); } });
  g.text(st.O[0], st.O[1], 'O', { dx: -14, dy: -10, anchor: 'end', color: 'purple' });
  if (st.O[0] === st.A[0] && st.O[1] === st.A[1]) st.seen.onA = true;
  var names = [['AB', 0, 1], ['BC', 1, 2], ['AC', 0, 2]];
  tbl.set(['Side', 'Original', 'Image', 'Image ÷ original'], names.map(function (n) {
    var o = Gm.dist(T[n[1]], T[n[2]]), im = Gm.dist(I[n[1]], I[n[2]]);
    return [n[0], L.num(o, 2), L.num(im, 2), o ? L.nice(im / o) : '—'];
  }));
  var angs = [Gm.angle(T[1], T[0], T[2]), Gm.angle(T[0], T[1], T[2]), Gm.angle(T[0], T[2], T[1])];
  var per = function (Q) { return Gm.dist(Q[0], Q[1]) + Gm.dist(Q[1], Q[2]) + Gm.dist(Q[0], Q[2]); };
  var a0 = Math.abs(Gm.area(T)), a1 = Math.abs(Gm.area(I));
  read.innerHTML = '(' + L.V('x') + ', ' + L.V('y') + ') → (' + L.nice(k) + L.V('x') + ', ' + L.nice(k) + L.V('y') + ')' + (st.O[0] || st.O[1] ? '<div class="sub">about O(' + st.O[0] + ', ' + st.O[1] + ')</div>' : '') +
    '<div class="sub" style="margin-top:6px">' + (k > 1 ? 'Enlargement' : k < 1 ? 'Reduction' : 'Same size: the image is congruent') + ' · △ABC ~ △A′B′C′</div>';
  info.innerHTML = '<dt>Angles</dt><dd>' + angs.map(function (x) { return L.num(x, 1) + '°'; }).join(', ') + ' in both triangles</dd>' +
    '<dt>Perimeter</dt><dd>' + L.num(per(T), 2) + ' → ' + L.num(per(I), 2) + ' (× ' + L.nice(k) + ')</dd>' +
    '<dt>Area</dt><dd>' + L.num(a0, 2) + ' → ' + L.num(a1, 2) + ' (× ' + L.nice(k * k) + ' = ' + L.nice(k) + '²)</dd>';
  ch.update();
});
draw();
