/* A particle on a line with velocity v(t) and starting position x(0) = x0. Position, displacement and total distance
   are exact: x(t) = x0 + V(t) − V(0) with an antiderivative V, and total distance adds |V| between the zeros of v. */
var PI = Math.PI;
var FN = {
  quad: { label: 't² − 5t + 4', v: function (t) { return t * t - 5 * t + 4; }, a: function (t) { return 2 * t - 5; }, V: function (t) { return t * t * t / 3 - 5 * t * t / 2 + 4 * t; }, zeros: [1, 4], vr: [-3, 10] },
  lin: { label: '4 − 2t', v: function (t) { return 4 - 2 * t; }, a: function () { return -2; }, V: function (t) { return 4 * t - t * t; }, zeros: [2], vr: [-9, 5] },
  wave: { label: '3 sin(πt/3)', v: function (t) { return 3 * Math.sin(PI * t / 3); }, a: function (t) { return PI * Math.cos(PI * t / 3); }, V: function (t) { return -9 / PI * Math.cos(PI * t / 3); }, zeros: [3], vr: [-3.5, 3.5] }
};
var st = { fn: 'quad', x0: 0, t: 0.5, play: false, seen: {}, x0s: {} };
function F() { return FN[st.fn]; }
function pos(t) { return st.x0 + F().V(t) - F().V(0); }
function dist(t) { var f = F(), cuts = [0].concat(f.zeros.filter(function (z) { return z < t; })).concat([t]), s = 0; for (var i = 0; i < cuts.length - 1; i++) s += Math.abs(f.V(cuts[i + 1]) - f.V(cuts[i])); return s; }
var GN = { xmin: -12, xmax: 12, ymin: -1, ymax: 1.6, width: 640, height: 130, noGrid: true, noYAxis: true, xstep: 1, xlabelStep: 2, label: 'Particle on the number line' }, gn = L.graph(P.stage, GN);
var GX = { xmin: -0.45, xmax: 6.1, ymin: -6, ymax: 10, width: 640, height: 250, xstep: 0.5, xlabelStep: 1, label: 'Position x(t)' }, gx = L.graph(P.stage, GX);
var GV = { xmin: -0.45, xmax: 6.1, ymin: -3, ymax: 10, width: 640, height: 250, xstep: 0.5, xlabelStep: 1, label: 'Velocity v(t) with the area from 0 to t shaded' }, gv = L.graph(P.stage, GV);
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Top: where the particle is, with its path so far. Middle: position against time. Bottom: velocity; blue area adds to the position, red area subtracts.');
L.chips(P.panel, { label: 'Velocity v(t) (m/s)', value: st.fn, options: Object.keys(FN).map(function (k) { return { value: k, label: FN[k].label }; }), onChange: function (v) { st.fn = v; draw(); } });
var st0 = L.slider(P.panel, { id: 'start-x0', label: 'x(0), starting position (m)', min: -5, max: 5, step: 1, value: st.x0, color: 'green', format: L.nice, onInput: function (v) { st.x0 = v; draw(); } });
var stt = L.slider(P.panel, { id: 'time-t', label: 't, time (s)', min: 0, max: 6, step: 0.05, value: st.t, color: 'purple', format: function (v) { return L.num(v, 2); }, onInput: function (v) { st.t = v; draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
var bP = L.button(btns, '▶ Play', function () {
  st.play = !st.play; bP.textContent = st.play ? '❚❚ Pause' : '▶ Play';
  if (st.t >= 6) st.t = 0;
  if (st.play) { var last = performance.now(); (function step(now) { if (!st.play) return; st.t = Math.min(6, st.t + Math.min(0.05, (now - last) / 1000) * 0.8); last = now; stt.set(st.t, true); draw(); if (st.t >= 6) { st.play = false; bP.textContent = '▶ Play'; return; } requestAnimationFrame(step); })(last); }
});
L.reset(btns, function () { st.play = false; bP.textContent = '▶ Play'; st.x0 = 0; st.t = 0.5; st0.set(0, true); stt.set(0.5, true); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Find a time when the particle changes direction. What is ' + L.V('v') + ' there, and what happens to its sign?', check: function () { return st.seen.turn; } },
  { text: 'Find a time when the particle is <b>speeding up</b> while moving <b>left</b>.', check: function () { return st.seen.upLeft; } },
  { text: 'Find a time ' + L.V('t') + ' &gt; 0 when the displacement is 0 but the total distance is not.', check: function () { return st.seen.back; } },
  { text: 'For ' + L.V('t') + '² − 5' + L.V('t') + ' + 4, record the displacement and the total distance at ' + L.V('t') + ' = 6. Why are they different?', check: function () { return st.seen.end; } },
  { text: 'Keep the same velocity and time, and change ' + L.V('x') + '(0). Which numbers change, and which stay the same?', check: function () { return st.seen.x0; } }
]);
L.notice(P.below, '<p><b>Position = starting position + net change:</b> x(t) = x(0) + ∫<sub>0</sub><sup>t</sup> v(u) du. The displacement is the signed area under v; the <b>total distance</b> is the area under |v|, so area below the axis counts as positive distance.</p>' +
  '<p>The particle changes direction where v changes sign, not just where v = 0. It speeds up when v and a = v′ have the <b>same sign</b> and slows down when their signs differ, whichever way it is moving.</p>' +
  '<p>Changing x(0) slides the position graph up or down; velocity, acceleration, displacement and distance do not change.</p>');
var draw = L.scheduler(function () {
  var f = F(), t = st.t, x = pos(t), v = f.v(t), a = f.a(t), d = pos(t) - st.x0, D = dist(t);
  var lo = Infinity, hi = -Infinity; for (var s = 0; s <= 6.0001; s += 0.05) { var p = pos(s); lo = Math.min(lo, p); hi = Math.max(hi, p); }
  L.setNiceView(gx, GX, { ymin: Math.floor(lo - 1), ymax: Math.ceil(hi + 1) }, 6); gx.clear();
  L.setNiceView(gv, GV, { ymin: f.vr[0], ymax: f.vr[1] }, 6); gv.clear();
  gn.setView({ xmin: Math.min(-6, Math.floor(lo - 1)), xmax: Math.max(6, Math.ceil(hi + 1)) }); gn.clear();
  /* number line with ticks, the path so far drawn as a zig-zag in time (higher = later) */
  for (var k = Math.ceil(gn.view.xmin); k <= gn.view.xmax; k++) { gn.line(k, -0.12, k, 0.12, { color: 'ink', width: 2 }); if (k % 2 === 0) gn.text(k, 0, String(k).replace('-', '−'), { dy: 26, anchor: 'middle', size: 12 }); }
  gn.line(gn.view.xmin, 0, gn.view.xmax, 0, { color: 'ink', width: 2 });
  if (t > 0) gn.param(function (s) { return pos(s); }, function (s) { return 0.25 + 1.2 * s / 6; }, 0, t, { color: 'ghost', width: 3 });
  gn.dot(st.x0, 0, { color: 'green', r: 6 });
  gn.dot(x, 0, { color: 'purple', r: 10, stroke: 'ink', strokeWidth: 2 });
  if (Math.abs(v) > 0.02) gn.line(x, 0.55, x + Math.sign(v) * Math.min(3, 0.6 + Math.abs(v) / 3), 0.55, { color: v > 0 ? 'blue' : 'red', width: 5 });
  gx.fn(pos, { color: 'ghost', width: 2, dash: '6 6', from: 0, to: 6 });
  gx.fn(pos, { color: 'purple', width: 4, from: 0, to: t });
  gx.dot(t, x, { color: 'purple', r: 7, stroke: 'ink', strokeWidth: 2 });
  var N = Math.max(2, Math.round(t * 60));
  for (var i = 0; i < N; i++) { var t0 = t * i / N, t1 = t * (i + 1) / N, y0 = f.v(t0), y1 = f.v(t1); gv.poly([[t0, 0], [t0, y0], [t1, y1], [t1, 0]], { fill: y0 + y1 >= 0 ? 'blue' : 'red', opacity: 0.3 }); }
  gv.fn(f.v, { color: 'ink', width: 3, from: 0, to: 6 });
  gv.line(t, 0, t, v, { color: 'purple', width: 3 });
  gv.handle(t, 0, { color: 'purple', snap: 0.05, label: 'Time t', onDrag: function (nt) { st.t = Math.max(0, Math.min(6, L.round(nt, 2))); stt.set(st.t, true); draw(); } });
  var moving = Math.abs(v) < 0.02 ? 'at rest for an instant' : v > 0 ? 'moving right' : 'moving left';
  var speed = Math.abs(v) < 0.02 || Math.abs(a) < 0.02 ? '' : (v * a > 0 ? ', speeding up' : ', slowing down');
  read.innerHTML = 'x(' + L.num(t, 2) + ') = ' + L.num(x, 3) + ' m · v = ' + L.num(v, 3) + ' m/s · a = ' + L.num(a, 3) + ' m/s²' +
    '<div style="margin-top:6px"><b>' + moving + speed + '</b></div>' +
    '<div class="sub" style="margin-top:4px">displacement ∫<sub>0</sub><sup>t</sup> v = ' + L.num(d, 3) + ' m · total distance ∫<sub>0</sub><sup>t</sup> |v| = ' + L.num(D, 3) + ' m</div>';
  fb.set(Math.abs(d) < 0.05 && D > 0.5 ? 'Back where it started: displacement 0, but it has traveled ' + L.num(D, 2) + ' m.' : D - Math.abs(d) > 0.01 ? 'Distance &gt; |displacement| because the particle has turned around.' : 'No turn yet, so distance = |displacement|.', '');
  if (f.zeros.some(function (z) { return Math.abs(t - z) < 0.051; })) st.seen.turn = true;
  if (v < -0.05 && a < -0.05) st.seen.upLeft = true;
  if (t > 0.3 && Math.abs(d) < 0.06 && D > 0.5) st.seen.back = true;
  if (st.fn === 'quad' && t > 5.97) st.seen.end = true;
  var key = st.fn + ':' + L.num(t, 2); st.x0s[key] = st.x0s[key] || {}; st.x0s[key][st.x0] = true; if (Object.keys(st.x0s[key]).length >= 2) st.seen.x0 = true;
  ch.update();
});
draw();
