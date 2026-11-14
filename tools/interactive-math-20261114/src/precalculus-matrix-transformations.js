/* [a b; c d] acting on the unit square and a letter F. Columns = images of (1, 0) and (0, 1); det = signed area factor. */
var st = { a: 1, b: 0, c: 0, d: 1, seen: {} };
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var sl = {};
[['a', 'a (top left)', 'orange'], ['b', 'b (top right)', 'purple'], ['c', 'c (bottom left)', 'orange'], ['d', 'd (bottom right)', 'purple']].forEach(function (k) {
  sl[k[0]] = L.slider(P.panel, { id: 'entry-' + k[0], label: k[1], min: -3, max: 3, step: 0.5, value: st[k[0]], color: k[2], format: function (v) { return L.num(v); }, onInput: function (v) { st[k[0]] = v; draw(); } });
});
var pre = L.h('div', { class: 'btn-row' }, P.panel);
function setM(a, b, c, d) { st.a = a; st.b = b; st.c = c; st.d = d; ['a', 'b', 'c', 'd'].forEach(function (k) { sl[k].set(st[k], true); }); draw(); }
L.button(pre, 'Identity', function () { setM(1, 0, 0, 1); }, true);
L.button(pre, 'Rotate 90°', function () { setM(0, -1, 1, 0); }, true);
L.button(pre, 'Reflect in x-axis', function () { setM(1, 0, 0, -1); }, true);
L.button(pre, 'Dilate × 2', function () { setM(2, 0, 0, 2); }, true);
L.button(pre, 'Shear', function () { setM(1, 1, 0, 1); }, true);
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Without the presets, build a matrix that rotates the F 180°.', check: function () { return st.seen.rot180; } },
  { text: 'Make the square into a shape with area 6.', check: function () { return st.seen.area6; } },
  { text: 'Flip the F (mirror image) without changing its area.', check: function () { return st.seen.flip1; } },
  { text: 'Squash the whole plane onto a line. What is the determinant?', check: function () { return st.seen.det0; } },
  { text: 'Change the shape of the square but keep its area 1 (not a rotation or reflection).', check: function () { return st.seen.shearKeep; } }
]);
L.notice(P.below, '<p><b>The columns tell you everything:</b> the first column (a, c) is where (1, 0) goes and the second column (b, d) is where (0, 1) goes. Every other point follows: (x, y) → (ax + by, cx + dy).</p>' +
  '<p>The <b>determinant</b> ad − bc is the factor that multiplies every area. If it is negative, the shape is flipped (the F reads backward). If it is 0, the plane collapses onto a line or a point.</p>');
var gr = L.graph(P.stage, { xmin: -8, xmax: 8, ymin: -8, ymax: 8, width: 560, height: 560, xstep: 1, ystep: 1, xlabelStep: 2, ylabelStep: 2, label: 'Unit square and the letter F before and after the matrix' });
var F = [[0, 0], [0.4, 0], [0.4, 1.2], [1.2, 1.2], [1.2, 1.6], [0.4, 1.6], [0.4, 2.2], [1.6, 2.2], [1.6, 2.6], [0, 2.6]];
function T(p) { return [st.a * p[0] + st.b * p[1], st.c * p[0] + st.d * p[1]]; }
var draw = L.scheduler(function () {
  var det = st.a * st.d - st.b * st.c;
  gr.clear();
  gr.poly([[0, 0], [1, 0], [1, 1], [0, 1]], { fill: 'ink', opacity: 0.08, stroke: 'ink', width: 1 });
  gr.poly(F.map(function (p) { return [p[0] + 1.3, p[1] + 1.3]; }), { fill: 'ink', opacity: 0.08, stroke: 'ink', width: 1 });
  gr.poly([[0, 0], [1, 0], [1, 1], [0, 1]].map(T), { fill: 'blue', opacity: 0.3, stroke: 'blue', width: 3 });
  gr.poly(F.map(function (p) { return T([p[0] + 1.3, p[1] + 1.3]); }), { fill: det < 0 ? 'red' : 'green', opacity: 0.35, stroke: det < 0 ? 'red' : 'green', width: 3 });
  gr.line(0, 0, st.a, st.c, { color: 'orange', width: 5 }); gr.line(0, 0, st.b, st.d, { color: 'purple', width: 5 });
  gr.dot(st.a, st.c, { color: 'orange' }); gr.dot(st.b, st.d, { color: 'purple' });
  gr.text(st.a, st.c, '(' + L.num(st.a) + ', ' + L.num(st.c) + ')', { dx: 8, dy: 18, color: 'orange' });
  gr.text(st.b, st.d, '(' + L.num(st.b) + ', ' + L.num(st.d) + ')', { dx: 8, dy: -8, color: 'purple' });
  read.innerHTML = '[ ' + L.num(st.a) + '  ' + L.num(st.b) + ' ; ' + L.num(st.c) + '  ' + L.num(st.d) + ' ]' +
    '<div class="sub">det = (' + L.num(st.a) + ')(' + L.num(st.d) + ') − (' + L.num(st.b) + ')(' + L.num(st.c) + ') = ' + L.num(det) + ' · area of the image of the unit square = ' + L.num(Math.abs(det)) + '</div>';
  fb.set(det === 0 ? 'Determinant 0: every point lands on one line (or the origin). The transformation cannot be undone.' : det < 0 ? 'Negative determinant: the F is flipped (orientation reversed).' : 'Area is multiplied by ' + L.num(det) + '.', det === 0 ? 'warn' : '');
  if (st.a === -1 && st.b === 0 && st.c === 0 && st.d === -1) st.seen.rot180 = true;
  if (Math.abs(det) === 6) st.seen.area6 = true;
  if (det === -1) st.seen.flip1 = true;
  if (det === 0) st.seen.det0 = true;
  var orth = Math.abs(st.a * st.b + st.c * st.d) < 1e-9 && Math.abs(st.a * st.a + st.c * st.c - 1) < 1e-9 && Math.abs(st.b * st.b + st.d * st.d - 1) < 1e-9;
  if (det === 1 && !orth) st.seen.shearKeep = true;
  ch.update();
});
setM(1, 0, 0, 1);
