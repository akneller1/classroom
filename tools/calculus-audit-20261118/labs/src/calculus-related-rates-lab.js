/* Sliding ladder: x² + y² = L², the bottom moves away from the wall at dx/dt.
   Exact rates: dy/dt = −x·(dx/dt)/y, dθ/dt = −(dx/dt)/y (θ = angle with the ground), dA/dt = (dx/dt/2)(y − x²/y). */
var st = { L: 13, r: 2, x: 5, play: false, seen: {}, rates: {} };
function Y(x) { return Math.sqrt(Math.max(0, st.L * st.L - x * x)); }
function rates(x) { var y = Y(x), r = st.r; return { y: y, dy: -x * r / y, dth: -r / y, dA: r / 2 * (y - x * x / y) }; }
var GO = { xmin: -1.5, xmax: 14.5, ymin: -1.5, ymax: 14.5, width: 520, height: 520, label: 'Ladder against a wall' }, g = L.graph(P.stage, GO);
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Drag the orange foot of the ladder, or press Play to slide it out at the chosen rate.');
var GR = { xmin: 0, xmax: 13, ymin: -8, ymax: 1, width: 520, height: 260, label: 'Rate the top moves, dy/dt, against x' }, gr = L.graph(P.stage, GR);
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Bottom: dy/dt for every position of the foot, with the current moment marked. The rate is not constant even though dx/dt is.');
L.chips(P.panel, { label: 'Ladder length L (ft)', value: st.L, options: [10, 13, 25].map(function (v) { return { value: v, label: v + ' ft' }; }), onChange: function (v) { st.L = v; st.x = Math.min(st.x, v - 0.5); sx.set(st.x, true); draw(); } });
var sr = L.slider(P.panel, { id: 'rate', label: 'dx/dt, speed of the foot (ft/s)', min: 0.5, max: 4, step: 0.5, value: st.r, color: 'blue', format: L.nice, onInput: function (v) { st.r = v; draw(); } });
var sx = L.slider(P.panel, { id: 'foot-x', label: 'x, distance from the wall (ft)', min: 0.5, max: 24.9, step: 0.1, value: st.x, color: 'orange', format: function (v) { return L.num(v, 1); }, onInput: function (v) { st.x = Math.min(v, st.L - 0.1); if (v > st.L - 0.1) sx.set(st.x, true); draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var btns = L.h('div', { class: 'btn-row' }, P.panel), timer = null;
var bP = L.button(btns, '▶ Play', function () {
  st.play = !st.play; bP.textContent = st.play ? '❚❚ Pause' : '▶ Play';
  if (st.play) { var last = performance.now(); (function step(now) { if (!st.play) return; var dt = Math.min(0.05, (now - last) / 1000); last = now; st.x = Math.min(st.L - 0.1, st.x + st.r * dt); sx.set(st.x, true); draw(); if (st.x >= st.L - 0.1) { st.play = false; bP.textContent = '▶ Play'; return; } timer = requestAnimationFrame(step); })(last); }
});
L.reset(btns, function () { st.play = false; bP.textContent = '▶ Play'; st.L = 13; st.r = 2; st.x = 5; sr.set(2, true); sx.set(5, true); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Use L = 13 ft and d' + L.V('x') + '/d' + L.V('t') + ' = 2 ft/s. Move the foot to ' + L.V('x') + ' = 5 ft. How fast is the top sliding down?', check: function () { return st.seen.classic; } },
  { text: 'Find where the top slides down <b>twice</b> as fast as the foot slides out.', check: function () { return st.seen.twice; } },
  { text: 'Find where the area of the triangle stops growing and starts shrinking.', check: function () { return st.seen.areaTurn; } },
  { text: 'Make the top fall faster than 10 ft/s. Where is the foot?', check: function () { return st.seen.fast; } },
  { text: 'Keep ' + L.V('x') + ' the same and change d' + L.V('x') + '/d' + L.V('t') + '. What happens to d' + L.V('y') + '/d' + L.V('t') + '?', check: function () { return st.seen.linear; } }
]);
L.notice(P.below, '<p><b>Related rates:</b> differentiate the equation that links the quantities, x² + y² = L², with respect to time: 2x·dx/dt + 2y·dy/dt = 0, so dy/dt = −(x/y)·dx/dt.</p>' +
  '<p>The foot moves at a constant rate, but the top does not: when the foot is near the wall the top barely moves, and as the top nears the ground (y → 0) its speed grows without bound.</p>' +
  '<p>Substitute the numbers <b>after</b> differentiating. At x = y the two ends move equally fast, and that is also where the area x·y/2 is largest (dA/dt = 0).</p>');
var draw = L.scheduler(function () {
  var Lm = st.L, x = st.x, R = rates(x), y = R.y;
  L.setNiceView(g, GO, { xmin: -0.12 * Lm, xmax: 1.12 * Lm, ymin: -0.12 * Lm, ymax: 1.12 * Lm }, 6, 6); g.clear();
  L.setNiceView(gr, GR, { xmin: -0.06 * Lm, xmax: Lm, ymin: -4 * st.r, ymax: st.r * 0.5 }, 5, 6); gr.clear();
  g.poly([[0, 0], [x, 0], [0, y]], { fill: 'green', opacity: 0.18 });
  g.line(0, 0, 0, 1.08 * Lm, { color: 'ink', width: 6 });
  g.line(-0.1 * Lm, 0, 1.1 * Lm, 0, { color: 'ink', width: 6 });
  g.line(x, 0, 0, y, { color: 'purple', width: 7 });
  g.text(x / 2, 0, 'x = ' + L.num(x, 2), { dy: 22, anchor: 'middle', color: 'orange', size: 15 });
  g.text(0, y / 2, 'y = ' + L.num(y, 2), { dx: 10, color: 'blue', size: 15 });
  g.text(x * 0.78, 0, 'θ', { dy: -8, color: 'purple', size: 15 });
  g.line(x, 0, x + 0.12 * Lm * Math.sign(st.r), 0, { color: 'orange', width: 4 });
  g.text(x + 0.13 * Lm, 0, '→ ' + L.nice(st.r) + ' ft/s', { dy: -10, color: 'orange', size: 13 });
  g.line(0, y, 0, y + Math.max(-0.3 * Lm, Math.min(-0.02 * Lm, R.dy * 0.12 * Lm / st.r)), { color: 'blue', width: 4 });
  g.dot(0, y, { color: 'blue', r: 8 });
  g.handle(x, 0, { color: 'orange', snap: 0.1, label: 'Foot of the ladder', onDrag: function (nx) { st.x = Math.max(0.5, Math.min(Lm - 0.1, L.round(nx, 1))); sx.set(st.x, true); draw(); } });
  gr.fn(function (s) { return s < Lm - 1e-6 ? -s * st.r / Y(s) : NaN; }, { color: 'blue', width: 3, from: 0, to: Lm - 0.01 });
  gr.line(0, -st.r, Lm, -st.r, { color: 'ghost', width: 2, dash: '6 6' });
  gr.text(0.55 * Lm, -st.r, 'y-rate equal to −dx/dt', { dy: 16, color: 'ghost', size: 12 });
  gr.dot(x, Math.max(-4 * st.r, R.dy), { color: 'orange', r: 7, stroke: 'ink', strokeWidth: 2 });
  read.innerHTML = 'x² + y² = ' + Lm + '²: y = ' + L.num(y, 3) + ' ft' +
    '<div style="margin-top:6px">d' + L.V('y') + '/d' + L.V('t') + ' = −(' + L.num(x, 2) + ' / ' + L.num(y, 2) + ')(' + L.nice(st.r) + ') = <b>' + L.num(R.dy, 3) + ' ft/s</b></div>' +
    '<div class="sub" style="margin-top:4px">dθ/d' + L.V('t') + ' = ' + L.num(R.dth, 3) + ' rad/s · area rate dA/d' + L.V('t') + ' = ' + L.num(R.dA, 3) + ' ft²/s</div>';
  fb.set(Math.abs(R.dA) < 0.02 * st.r * Lm ? 'dA/dt ≈ 0: the triangle is as large as it gets (x = y).' : R.dA > 0 ? 'dA/dt > 0: the triangle is still growing.' : 'dA/dt < 0: the triangle is shrinking even though x is growing.', Math.abs(R.dy) > 10 ? 'warn' : '');
  if (Lm === 13 && st.r === 2 && Math.abs(x - 5) < 0.051) st.seen.classic = true;
  if (Math.abs(R.dy + 2 * st.r) < 0.06 * st.r) st.seen.twice = true;
  if (Math.abs(x - y) < 0.12) st.seen.areaTurn = true;
  if (R.dy < -10) st.seen.fast = true;
  var k = Lm + ':' + L.num(x, 1); st.rates[k] = st.rates[k] || {}; st.rates[k][st.r] = true; if (Object.keys(st.rates[k]).length >= 2) st.seen.linear = true;
  ch.update();
});
draw();
