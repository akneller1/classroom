var Gm = L.geo;
var st = { mode: 'tri', A: [-5, -3], B: [5, -3], C: [1, 5], center: 'none', ext: false, s1: 3, s2: 4, s3: 6, seen: {} };
L.tabs(P.stage, [{ id: 'tri', label: 'Angles, sides & centers' }, { id: 'ineq', label: 'Can it be a triangle?' }], function (id) { st.mode = id; build(); draw(); });
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -8, ymax: 10, width: 600, height: 540, label: 'Triangle ABC' });
var gg = L.geoGraph(g);
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var ctrl = L.h('div', { style: 'display:grid;gap:12px' }, P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Make an <b>obtuse</b> triangle. Does the angle sum change?', check: function () { return st.seen.obtuse; } },
  { text: 'Make a <b>right</b> triangle (snap a vertex so one angle is 90°).', check: function () { return st.seen.right; } },
  { text: 'Show the circumcenter and move it <b>outside</b> the triangle.', check: function () { return st.seen.ccOut; } },
  { text: 'Show the exterior angle at C and compare it with ∠A + ∠B.', check: function () { return st.seen.ext; } },
  { text: 'In "Can it be a triangle?", find three lengths that do <b>not</b> make a triangle.', check: function () { return st.seen.noTri; } }
]);
function build() {
  ctrl.innerHTML = '';
  if (st.mode === 'tri') {
    L.chips(ctrl, { label: 'Show a triangle center', value: st.center, options: [{ value: 'none', label: 'none' }, { value: 'centroid', label: 'centroid' }, { value: 'circum', label: 'circumcenter' }, { value: 'in', label: 'incenter' }, { value: 'ortho', label: 'orthocenter' }], onChange: function (v) { st.center = v; draw(); } });
    L.chips(ctrl, { label: 'Exterior angle at C', value: st.ext, options: [{ value: true, label: 'show' }, { value: false, label: 'hide' }], onChange: function (v) { st.ext = v; draw(); } });
  } else {
    [['s1', 'Side 1', 'blue'], ['s2', 'Side 2', 'green'], ['s3', 'Side 3', 'purple']].forEach(function (p) {
      L.slider(ctrl, { id: p[0], label: p[1], min: 1, max: 12, step: 0.5, value: st[p[0]], color: p[2], format: L.nice, onInput: function (v) { st[p[0]] = v; draw(); } });
    });
  }
}
function centers(A, B, C) {
  var a = Gm.dist(B, C), b = Gm.dist(A, C), c = Gm.dist(A, B), s = a + b + c;
  var D = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]));
  var sq = function (P) { return P[0] * P[0] + P[1] * P[1]; };
  var cc = [(sq(A) * (B[1] - C[1]) + sq(B) * (C[1] - A[1]) + sq(C) * (A[1] - B[1])) / D, (sq(A) * (C[0] - B[0]) + sq(B) * (A[0] - C[0]) + sq(C) * (B[0] - A[0])) / D];
  var gc = [(A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3];
  return { centroid: gc, circum: cc, R: Gm.dist(cc, A), in: [(a * A[0] + b * B[0] + c * C[0]) / s, (a * A[1] + b * B[1] + c * C[1]) / s], r: Math.abs(Gm.area([A, B, C])) * 2 / s,
    ortho: [A[0] + B[0] + C[0] - 2 * cc[0], A[1] + B[1] + C[1] - 2 * cc[1]] };
}
function inside(P, T) { var s1 = Gm.area([T[0], T[1], P]), s2 = Gm.area([T[1], T[2], P]), s3 = Gm.area([T[2], T[0], P]); return (s1 >= 0 && s2 >= 0 && s3 >= 0) || (s1 <= 0 && s2 <= 0 && s3 <= 0); }
var draw = L.scheduler(function () {
  g.clear();
  if (st.mode === 'ineq') {
    g.setView({ xmin: -1, xmax: 13, ymin: -2, ymax: 10.6 });
    var a = st.s1, b = st.s2, c = st.s3, sides = [a, b, c].sort(function (x, y) { return x - y; }), ok = sides[0] + sides[1] > sides[2];
    var A = [0, 0], B = [c, 0];
    if (ok) {
      var x = (b * b + c * c - a * a) / (2 * c), C = [x, Math.sqrt(Math.max(0, b * b - x * x))];
      if (b * b - x * x < 0) ok = false; else {
        gg.polygon([A, B, C], { stroke: 'ink', fill: 'green', fillOpacity: 0.12, width: 2 });
        g.line(A[0], A[1], B[0], B[1], { color: 'purple', width: 6 }); g.line(A[0], A[1], C[0], C[1], { color: 'green', width: 6 }); g.line(B[0], B[1], C[0], C[1], { color: 'blue', width: 6 });
      }
    }
    if (!ok) {
      g.line(0, 0, c, 0, { color: 'purple', width: 6 });
      var tip1 = Math.min(b, 12), tip2 = Math.max(c - a, -1);
      g.line(0, 0.4, b, 0.4, { color: 'green', width: 6 }); g.line(c, 0.8, c - a, 0.8, { color: 'blue', width: 6 });
      g.text(c / 2, 0, 'The other two sides can\'t reach each other', { anchor: 'middle', dy: 34, color: 'red' });
      st.seen.noTri = true;
    }
    read.innerHTML = (ok ? '<span class="c-green">These lengths make a triangle.</span>' : '<span class="c-red">No triangle.</span>') +
      '<div class="sub" style="margin-top:6px">Two shortest: ' + L.nice(sides[0]) + ' + ' + L.nice(sides[1]) + ' = ' + L.nice(sides[0] + sides[1]) + (ok ? ' &gt; ' : ' ≤ ') + L.nice(sides[2]) + ' (longest)</div>';
    info.innerHTML = '<dt>Rule</dt><dd>The sum of any two sides must be greater than the third side.</dd><dt>Third side range</dt><dd>' + L.nice(Math.abs(a - b)) + ' &lt; side 3 &lt; ' + L.nice(a + b) + ' (for sides 1 and 2)</dd>';
  } else {
    g.setView({ xmin: -10, xmax: 10, ymin: -8, ymax: 10 });
    var Ap = st.A, Bp = st.B, Cp = st.C, T = [Ap, Bp, Cp], cen = [(Ap[0] + Bp[0] + Cp[0]) / 3, (Ap[1] + Bp[1] + Cp[1]) / 3];
    var area = Math.abs(Gm.area(T));
    gg.polygon(T, { stroke: 'blue', fill: 'blue', fillOpacity: 0.08 });
    if (area < 1e-9) { read.innerHTML = '<span class="c-red">The three points are on one line, so there is no triangle.</span>'; info.innerHTML = ''; handles(); ch.update(); return; }
    var angA = Gm.angle(Bp, Ap, Cp), angB = Gm.angle(Ap, Bp, Cp), angC = Gm.angle(Ap, Cp, Bp);
    var a2 = Gm.dist(Bp, Cp), b2 = Gm.dist(Ap, Cp), c2 = Gm.dist(Ap, Bp);
    gg.angle(Bp, Ap, Cp, { r: 1, color: 'orange', fill: true, label: L.num(angA, 0) + '°' });
    gg.angle(Ap, Bp, Cp, { r: 1, color: 'green', fill: true, label: L.num(angB, 0) + '°' });
    gg.angle(Ap, Cp, Bp, { r: 1, color: 'purple', fill: true, label: L.num(angC, 0) + '°' });
    if (st.ext) {
      var E = Gm.polar(Cp, 4, Gm.dir(Bp, Cp));
      g.line(Cp[0], Cp[1], E[0], E[1], { color: 'ink', width: 3, dash: '8 6' });
      gg.angle(Ap, Cp, E, { r: 1.4, color: 'red', width: 3, label: L.num(180 - angC, 0) + '°', labelColor: 'red' });
      st.seen.ext = true;
    }
    gg.sideLabel(Bp, Cp, cen, 'a = ' + L.num(a2, 1)); gg.sideLabel(Ap, Cp, cen, 'b = ' + L.num(b2, 1)); gg.sideLabel(Ap, Bp, cen, 'c = ' + L.num(c2, 1));
    var C0 = centers(Ap, Bp, Cp), pt = null, name = '';
    if (st.center === 'centroid') { [[Ap, Bp, Cp], [Bp, Ap, Cp], [Cp, Ap, Bp]].forEach(function (q) { var Mq = Gm.mid(q[1], q[2]); g.line(q[0][0], q[0][1], Mq[0], Mq[1], { color: 'green', width: 2 }); }); pt = C0.centroid; name = 'Centroid: where the medians meet'; }
    if (st.center === 'circum') { gg.circle(C0.circum, C0.R, { stroke: 'purple', width: 2, dash: '6 5' }); [[Ap, Bp], [Bp, Cp], [Cp, Ap]].forEach(function (q) { var Mq = Gm.mid(q[0], q[1]); g.line(Mq[0], Mq[1], C0.circum[0], C0.circum[1], { color: 'purple', width: 2 }); }); pt = C0.circum; name = 'Circumcenter: where the perpendicular bisectors meet'; if (!inside(pt, T)) st.seen.ccOut = true; }
    if (st.center === 'in') { gg.circle(C0.in, C0.r, { stroke: 'orange', width: 2, dash: '6 5' }); T.forEach(function (q) { g.line(q[0], q[1], C0.in[0], C0.in[1], { color: 'orange', width: 2 }); }); pt = C0.in; name = 'Incenter: where the angle bisectors meet'; }
    if (st.center === 'ortho') { [[Ap, Bp, Cp], [Bp, Ap, Cp], [Cp, Ap, Bp]].forEach(function (q) { var F = Gm.foot(q[0], q[1], q[2]); g.line(q[0][0], q[0][1], F[0], F[1], { color: 'red', width: 2 }); g.line(F[0], F[1], C0.ortho[0], C0.ortho[1], { color: 'red', width: 1.5, dash: '4 4' }); }); pt = C0.ortho; name = 'Orthocenter: where the altitudes meet'; }
    if (pt && Math.abs(pt[0]) < 12 && Math.abs(pt[1]) < 12) g.dot(pt[0], pt[1], { color: 'ink', r: 7 });
    var maxA = Math.max(angA, angB, angC), kind = Math.abs(maxA - 90) < 0.05 ? 'right' : maxA > 90 ? 'obtuse' : 'acute';
    if (kind === 'obtuse') st.seen.obtuse = true; if (kind === 'right') st.seen.right = true;
    var sideOrder = [['a', a2, 'A'], ['b', b2, 'B'], ['c', c2, 'C']].sort(function (x, y) { return y[1] - x[1]; });
    read.innerHTML = '∠A + ∠B + ∠C = ' + L.num(angA, 1) + '° + ' + L.num(angB, 1) + '° + ' + L.num(angC, 1) + '° = <b>' + L.num(angA + angB + angC, 0) + '°</b>' +
      (st.ext ? '<div class="sub" style="margin-top:6px"><span class="c-red">Exterior angle at C</span> = ' + L.num(180 - angC, 1) + '° = ∠A + ∠B</div>' : '');
    info.innerHTML = '<dt>Type</dt><dd>' + kind + '</dd><dt>Longest side</dt><dd>' + sideOrder[0][0] + ', across from the largest angle, ∠' + sideOrder[0][2] + '</dd><dt>Shortest side</dt><dd>' + sideOrder[2][0] + ', across from the smallest angle, ∠' + sideOrder[2][2] + '</dd>' + (name ? '<dt>Center</dt><dd>' + name + (pt ? ' (' + (inside(pt, T) ? 'inside' : 'outside') + ' the triangle)' : '') + '</dd>' : '');
    handles();
  }
  ch.update();
});
function handles() {
  [['A', 'orange'], ['B', 'green'], ['C', 'purple']].forEach(function (h) {
    var P0 = st[h[0]]; g.handle(P0[0], P0[1], { color: h[1], snap: 1, label: 'Vertex ' + h[0], onDrag: function (x, y) { st[h[0]] = [x, y]; draw(); } });
    g.text(P0[0], P0[1], h[0], { dx: 14, dy: -12, size: 17 });
  });
}
build(); draw();
