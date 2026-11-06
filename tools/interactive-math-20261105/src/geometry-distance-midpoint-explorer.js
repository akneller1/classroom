var Gm = L.geo;
var st = { mode: 'dist', A: [-4, -2], B: [4, 4], t: 0.3, seen: {} };
L.tabs(P.stage, [{ id: 'dist', label: 'Distance & midpoint' }, { id: 'seg', label: 'Segment addition' }], function (id) { st.mode = id; draw(); });
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -10, ymax: 10, width: 600, height: 600, label: 'Segment AB on the coordinate plane' });
var gg = L.geoGraph(g);
L.h('p', { class: 'sub', style: 'margin:4px 6px 0' }, P.stage, 'Drag A and B (orange). In Segment addition, drag C (purple) along the segment.');
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Make a segment of length exactly 5 that is <b>not</b> horizontal or vertical.', check: function () { return st.seen.d5; } },
  { text: 'Move the points so the midpoint is the origin.', check: function () { return st.seen.m0; } },
  { text: 'Make a horizontal segment of length 6. How do you find its length without the formula?', check: function () { return st.seen.h6; } },
  { text: 'Make a segment whose length is √50 = 5√2.', check: function () { return st.seen.d50; } },
  { text: 'In Segment addition, put C at the midpoint so AC = CB.', check: function () { return st.seen.cmid; } }
]);
function pt(p) { return '(' + L.num(p[0]) + ', ' + L.num(p[1]) + ')'; }
var draw = L.scheduler(function () {
  var A = st.A, B = st.B, dx = B[0] - A[0], dy = B[1] - A[1], d2 = dx * dx + dy * dy, d = Math.sqrt(d2), M = Gm.mid(A, B);
  g.clear();
  if (st.mode === 'dist') {
    var Cn = [B[0], A[1]];
    if (dx && dy) { g.line(A[0], A[1], Cn[0], Cn[1], { color: 'green', width: 3, dash: '8 6' }); g.line(Cn[0], Cn[1], B[0], B[1], { color: 'purple', width: 3, dash: '8 6' }); gg.angle(A, Cn, B, { r: 0.6, color: 'ink', width: 2 }); }
    g.line(A[0], A[1], B[0], B[1], { color: 'blue', width: 5 });
    if (dx) g.text((A[0] + B[0]) / 2, A[1], '|Δx| = ' + Math.abs(dx), { anchor: 'middle', dy: dy > 0 ? 22 : -12, color: 'green' });
    if (dy) g.text(B[0], (A[1] + B[1]) / 2, '|Δy| = ' + Math.abs(dy), { dx: dx > 0 ? 10 : -10, anchor: dx > 0 ? 'start' : 'end', color: 'purple' });
    g.dot(M[0], M[1], { color: 'red', r: 8 }); g.text(M[0], M[1], 'M ' + pt(M), { dx: -12, dy: -12, anchor: 'end', color: 'red' });
    var rad = Gm.radical(d2), root = Math.round(d), dTxt;
    if (root * root === d2) dTxt = ' = ' + root;
    else dTxt = (rad.charAt(0) !== '√' ? ' = ' + rad : '') + ' ≈ ' + L.num(d, 2);
    read.innerHTML = 'AB = √(' + Math.abs(dx) + '² + ' + Math.abs(dy) + '²) = √' + d2 + dTxt;
    info.innerHTML = '<dt>A</dt><dd>' + pt(A) + '</dd><dt>B</dt><dd>' + pt(B) + '</dd><dt>Midpoint M</dt><dd>(' + L.frac(L.num(A[0]) + ' + ' + (B[0] < 0 ? '(' + L.num(B[0]) + ')' : L.num(B[0])), 2) + ', ' + L.frac(L.num(A[1]) + ' + ' + (B[1] < 0 ? '(' + L.num(B[1]) + ')' : L.num(B[1])), 2) + ') = ' + '(' + L.nice(M[0]) + ', ' + L.nice(M[1]) + ')</dd>';
    if (Math.abs(d - 5) < 1e-9 && dx && dy) st.seen.d5 = true;
    if (M[0] === 0 && M[1] === 0 && d > 0) st.seen.m0 = true;
    if (dy === 0 && Math.abs(dx) === 6) st.seen.h6 = true;
    if (d2 === 50) st.seen.d50 = true;
  } else {
    var C = Gm.lerp(A, B, st.t), ac = Gm.dist(A, C), cb = Gm.dist(C, B);
    g.line(A[0], A[1], C[0], C[1], { color: 'green', width: 6 }); g.line(C[0], C[1], B[0], B[1], { color: 'purple', width: 6 });
    g.handle(C[0], C[1], { color: 'purple', label: 'Point C', onDrag: function (x, y) {
      var dd = d2 || 1, t = ((x - A[0]) * dx + (y - A[1]) * dy) / dd; t = Math.max(0, Math.min(1, Math.round(t * 20) / 20)); st.t = t; draw(); } });
    g.text(C[0], C[1], 'C', { dx: 12, dy: -12, color: 'purple' });
    read.innerHTML = '<span class="c-green">AC</span> + <span class="c-purple">CB</span> = AB<div style="margin-top:4px">' + L.num(ac, 2) + ' + ' + L.num(cb, 2) + ' = ' + L.num(d, 2) + '</div>';
    info.innerHTML = '<dt>C is</dt><dd>' + L.nice(st.t, 20) + ' of the way from A to B</dd><dt>C</dt><dd>(' + L.num(C[0], 2) + ', ' + L.num(C[1], 2) + ')</dd>';
    if (Math.abs(st.t - 0.5) < 1e-9) st.seen.cmid = true;
  }
  g.handle(A[0], A[1], { color: 'orange', snap: 1, label: 'Point A', onDrag: function (x, y) { st.A = [x, y]; draw(); } });
  g.handle(B[0], B[1], { color: 'orange', snap: 1, label: 'Point B', onDrag: function (x, y) { st.B = [x, y]; draw(); } });
  g.text(A[0], A[1], 'A', { dx: -14, dy: 20, anchor: 'end' }); g.text(B[0], B[1], 'B', { dx: 14, dy: -12 });
  ch.update();
});
draw();
