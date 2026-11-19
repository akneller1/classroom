/* Circles lab: circumference and area. Circumference: roll the circle along a line; the distance it covers in one turn is
   C = πd, a little more than 3 diameters. Area: cut the circle into n equal sectors and rearrange them, alternating
   up and down, into a shape that approaches a parallelogram with base πr (half the circumference) and height r, so A = πr². */
var st = { r: 3, mode: 'circ', t: 0.35, n: 8, seen: {}, C: {}, A: {} };
var G = { xmin: 0, xmax: 1, ymin: 0, ymax: 1, width: 660, height: 300, label: 'Circle model', noGrid: true, noLabels: true }, g = L.graph(P.stage, G);
var cap = L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, '');
L.chips(P.panel, { label: 'Model', value: st.mode, options: [{ value: 'circ', label: 'Circumference: roll it out' }, { value: 'area', label: 'Area: cut and rearrange' }], onChange: function (v) { st.mode = v; draw(); } });
var fr = function (v) { return L.num(v, 1); };
var sr = L.slider(P.panel, { id: 'r', label: 'Radius r', min: 1, max: 10, step: 0.5, value: st.r, color: 'blue', format: fr, onInput: function (v) { st.r = v; draw(); } });
var sw = L.slider(P.panel, { id: 'roll', label: 'Roll the circle (part of one turn)', min: 0, max: 1, step: 0.05, value: st.t, color: 'orange', format: function (v) { return Math.round(v * 100) + '%'; }, onInput: function (v) { st.t = v; draw(); } });
L.chips(P.panel, { label: 'Number of sectors (area model)', value: String(st.n), options: [4, 8, 16, 32].map(function (k) { return { value: String(k), label: String(k) }; }), onChange: function (v) { st.n = +v; draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st.r = 3; st.t = 0.35; st.n = 8; sr.set(3, true); sw.set(0.35, true); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Roll a circle with radius 3 all the way out (100%). About how many diameters long is the circumference?', check: function () { return st.seen.unroll; } },
  { text: 'Find the circumference for r = 2 and for r = 4. What happens to C when the radius doubles?', check: function () { return st.C[2] && st.C[4]; } },
  { text: 'Find the area for r = 2 and for r = 4. What happens to A when the radius doubles?', check: function () { return st.A[2] && st.A[4]; } },
  { text: 'Cut the circle into 32 sectors. What shape do the rearranged pieces look like? What are its base and height?', check: function () { return st.seen.n32; } },
  { text: 'Find the radius whose circumference is about 31.4 units. What is its area?', check: function () { return st.seen.c314; } }
]);
L.notice(P.below, '<p><b>Circumference:</b> every circle’s circumference is π times its diameter, C = πd = 2πr. π ≈ 3.14, a little more than 3.</p>' +
  '<p><b>Area:</b> the rearranged sectors make a near-parallelogram with base half the circumference (πr) and height r, so A = πr · r = πr².</p>' +
  '<p>Doubling the radius doubles the circumference but multiplies the area by 4.</p>');
var n2 = function (v) { return L.num(v, 2); };
function arcPts(cx, cy, r, a0, a1, k) { var p = []; for (var i = 0; i <= k; i++) { var a = a0 + (a1 - a0) * i / k; p.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); } return p; }
var draw = L.scheduler(function () {
  var r = st.r, C = 2 * Math.PI * r, A = Math.PI * r * r;
  g.clear();
  if (st.mode === 'circ') {
    var th = 2 * Math.PI * st.t, cx = th * r, xs = -1.2 * r, xe = C + 1.25 * r, span = xe - xs, ys = -0.75 * r;
    g.setView({ xmin: xs, xmax: xe, ymin: ys, ymax: ys + span * 300 / 660 });
    g.line(xs, 0, xe, 0, { color: 'ink-soft', width: 2 });
    g.param(function (a) { return cx + r * Math.cos(a); }, function (a) { return r + r * Math.sin(a); }, 0, 2 * Math.PI, { color: 'ink-soft', width: 1.5, dash: '5 6' });
    if (th < 2 * Math.PI - 1e-9) g.param(function (a) { return cx + r * Math.cos(a); }, function (a) { return r + r * Math.sin(a); }, -Math.PI / 2, 1.5 * Math.PI - th, { color: 'orange', width: 6 });
    if (th > 0) g.line(0, 0, cx, 0, { color: 'orange', width: 6 });
    g.line(cx - r, r, cx + r, r, { color: 'blue', width: 3 }); g.dot(cx, r, { color: 'ink', r: 4 });
    g.text(cx, r, 'd = ' + n2(2 * r), { dy: -8, anchor: 'middle', color: 'blue', size: 13 });
    var mk = 1.5 * Math.PI - th; g.dot(cx + r * Math.cos(mk), r + r * Math.sin(mk), { color: 'red', r: 6 }); g.dot(0, 0, { color: 'red', r: 5 });
    var yb = -0.38 * r;
    for (var k = 0; k <= 3; k++) { g.line(2 * r * k, yb - 0.08 * r, 2 * r * k, yb + 0.08 * r, { color: 'blue', width: 2 }); if (k) g.text(2 * r * k, yb, k + 'd', { dy: 20, anchor: 'middle', color: 'blue', size: 12 }); }
    g.line(0, yb, 6 * r, yb, { color: 'blue', width: 2 }); g.line(6 * r, yb, C, yb, { color: 'purple', width: 4 });
    g.line(C, yb - 0.12 * r, C, yb + 0.12 * r, { color: 'purple', width: 3 }); g.text(C, yb, 'C', { dy: -10, anchor: 'middle', color: 'purple', size: 13, weight: 700 });
    cap.textContent = 'The red dot started at 0. The orange part of the circle is laid flat as it rolls; one full turn covers the circumference, about 3.14 diameters.';
    if (st.t >= 1 && r === 3) st.seen.unroll = true;
    st.C[r] = true;
  } else {
    var nn = st.n, w = 2 * Math.PI / nn, b = 2 * r * Math.sin(w / 2), c = Math.cos(w / 2), sx = -0.2 * r, ex = 7.3 * r;
    g.setView({ xmin: sx, xmax: ex, ymin: -0.55 * r, ymax: -0.55 * r + (ex - sx) * 300 / 660 });
    var ox = 1.35 * r, oy = 1.1 * r, kk = Math.max(4, Math.round(48 / nn));
    for (var i = 0; i < nn; i++) {
      var top = i < nn / 2;
      g.poly([[ox, oy]].concat(arcPts(ox, oy, r, i * w, (i + 1) * w, kk)), { fill: top ? 'blue' : 'orange', opacity: 0.35, stroke: 'ink', width: 1.2 });
    }
    g.line(ox, oy, ox - r, oy, { color: 'green', width: 3 }); g.text(ox - r, oy, 'r = ' + fr(r), { dx: -6, dy: 5, anchor: 'end', color: 'green', size: 13, weight: 700 });
    // rearranged: blue sectors with the arc on top (apex at the bottom), orange with the arc at the bottom (apex at the top)
    var x0 = 2.7 * r + b / 2, y0 = 0.15 * r;
    for (var j = 0; j < nn / 2; j++) {
      var dx = x0 + j * b;
      g.poly([[dx - b / 2, y0 + r]].concat(arcPts(dx - b / 2, y0 + r, r, -Math.PI / 2 - w / 2, -Math.PI / 2 + w / 2, kk)), { fill: 'orange', opacity: 0.35, stroke: 'ink', width: 1.2 });
      g.poly([[dx, y0 + r * (1 - c)]].concat(arcPts(dx, y0 + r * (1 - c), r, Math.PI / 2 - w / 2, Math.PI / 2 + w / 2, kk)), { fill: 'blue', opacity: 0.35, stroke: 'ink', width: 1.2 });
    }
    var xl = x0 - b, xr = x0 - b / 2 + (nn / 2) * b, yt = y0 + r;
    g.line(xl + b / 2, y0 - 0.12 * r, xr, y0 - 0.12 * r, { color: 'purple', width: 3 });
    g.text((xl + b / 2 + xr) / 2, y0 - 0.12 * r, 'base ≈ πr = ' + n2(Math.PI * r), { dy: 18, anchor: 'middle', color: 'purple', size: 13 });
    g.line(xr + 0.12 * r, y0, xr + 0.12 * r, yt, { color: 'green', width: 3 });
    g.text(xr + 0.12 * r, (y0 + yt) / 2, 'height ≈ r', { dx: 6, anchor: 'start', color: 'green', size: 13 });
    cap.textContent = 'Left: the circle cut into ' + nn + ' equal sectors. Right: the same sectors, half pointing up and half pointing down. More sectors make the shape closer to a parallelogram.';
    if (nn === 32) st.seen.n32 = true;
    st.A[r] = true;
  }
  if (Math.abs(C - 31.4) < 0.1) st.seen.c314 = true;
  read.innerHTML = 'r = ' + fr(r) + ', d = ' + fr(2 * r) +
    '<div style="margin-top:6px">C = πd = ' + fr(2 * r) + 'π ≈ <b>' + n2(C) + '</b> &nbsp;(with 3.14: ' + n2(3.14 * 2 * r) + ')</div>' +
    '<div>A = πr² = ' + L.num(r * r, 2) + 'π ≈ <b>' + n2(A) + '</b> &nbsp;(with 3.14: ' + n2(3.14 * r * r) + ')</div>' +
    '<div style="margin-top:6px">C ÷ d = ' + n2(C / (2 * r)) + ' for every circle</div>';
  fb.set(st.mode === 'circ' && st.t >= 1 ? 'One full turn: the circle covered C ≈ ' + n2(C) + ', which is π ≈ 3.14 diameters.' : '', '');
  ch.update();
});
draw();
