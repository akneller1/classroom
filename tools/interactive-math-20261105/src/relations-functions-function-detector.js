/* Each relation gives the y-values it has at a given x (ys), how to draw it, and its domain and range. */
var R = {
  line: { label: 'Line', ys: function (x) { return [0.5 * x + 1]; }, draw: function (g) { g.fn(function (x) { return 0.5 * x + 1; }, { color: 'blue' }); }, fn: true, dom: 'all real numbers', ran: 'all real numbers' },
  parab: { label: 'Parabola', ys: function (x) { return [0.3 * x * x - 4]; }, draw: function (g) { g.fn(function (x) { return 0.3 * x * x - 4; }, { color: 'blue' }); }, fn: true, dom: 'all real numbers', ran: L.V('y') + ' ≥ −4' },
  side: { label: 'Sideways parabola', ys: function (x) { return x < -3 ? [] : x === -3 ? [0] : [Math.sqrt(2 * (x + 3)), -Math.sqrt(2 * (x + 3))]; }, draw: function (g) { g.param(function (t) { return t * t / 2 - 3; }, function (t) { return t; }, -10, 10, { color: 'blue' }); }, fn: false, dom: L.V('x') + ' ≥ −3', ran: 'all real numbers' },
  circle: { label: 'Circle', ys: function (x) { return Math.abs(x) > 5 ? [] : [Math.sqrt(25 - x * x), -Math.sqrt(25 - x * x)]; }, draw: function (g) { g.param(function (t) { return 5 * Math.cos(t); }, function (t) { return 5 * Math.sin(t); }, 0, 2 * Math.PI, { color: 'blue' }); }, fn: false, dom: '−5 ≤ ' + L.V('x') + ' ≤ 5', ran: '−5 ≤ ' + L.V('y') + ' ≤ 5' },
  abs: { label: 'Absolute value', ys: function (x) { return [Math.abs(x - 1) - 3]; }, draw: function (g) { g.fn(function (x) { return Math.abs(x - 1) - 3; }, { color: 'blue' }); }, fn: true, dom: 'all real numbers', ran: L.V('y') + ' ≥ −3' },
  vert: { label: 'Vertical line', ys: function (x) { return Math.abs(x - 3) < 0.26 ? ['all'] : []; }, draw: function (g) { g.line(3, -11, 3, 11, { color: 'blue', width: 4 }); }, fn: false, dom: L.V('x') + ' = 3 only', ran: 'all real numbers' },
  pts: { label: 'My points', fn: null }
};
var st = { rel: 'line', vx: -6, swept: { lo: false, hi: false }, pts: [[-3, 2], [-1, -1], [1, 3], [4, 1]], failed: {}, passed: {}, ptsFunc: false, ptsNot: false };
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -10, ymax: 10, width: 600, height: 600, label: 'Relation and vertical line' });
var tip = L.h('p', { class: 'sub', style: 'margin:8px 6px 0' }, P.stage);
L.chips(P.panel, { label: 'Relation', value: st.rel, options: Object.keys(R).map(function (k) { return { value: k, label: R[k].label }; }), onChange: function (v) { st.rel = v; st.swept = { lo: false, hi: false }; draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var mapBox = L.h('div', null, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Find a relation where the vertical line hits <b>two points at once</b>.', check: function () { return Object.keys(st.failed).length > 0; } },
  { text: 'Sweep the line all the way across a graph that passes the test.', check: function () { return Object.keys(st.passed).length > 0; } },
  { text: 'In <b>My points</b>, plot at least 5 points that make a function.', check: function () { return st.ptsFunc; } },
  { text: 'In <b>My points</b>, change your points so it is <b>not</b> a function. What does the mapping diagram show?', check: function () { return st.ptsNot; } },
  { text: 'Find the domain and range of the circle.', check: function () { return st.circleDR; } }
]);
g.svg.addEventListener('click', function (e) {
  if (st.rel !== 'pts' || e.target.classList.contains('g-handle')) return;
  var pt = g.svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY; var q = pt.matrixTransform(g.svg.getScreenCTM().inverse());
  var x = Math.round(g.ix(q.x)), y = Math.round(g.iy(q.y));
  if (Math.abs(x) > 9 || Math.abs(y) > 9) return;
  var i = st.pts.findIndex(function (p) { return p[0] === x && p[1] === y; });
  if (i >= 0) st.pts.splice(i, 1); else st.pts.push([x, y]);
  draw();
});
function ptsYs(x) { return st.pts.filter(function (p) { return Math.abs(p[0] - x) < 0.26; }).map(function (p) { return p[1]; }); }
function ptsIsFunction() { var seen = {}; return st.pts.every(function (p) { if (seen[p[0]] != null && seen[p[0]] !== p[1]) return false; seen[p[0]] = p[1]; return true; }); }
function mapping() {
  var xs = [], ys = [];
  st.pts.forEach(function (p) { if (xs.indexOf(p[0]) < 0) xs.push(p[0]); if (ys.indexOf(p[1]) < 0) ys.push(p[1]); });
  xs.sort(function (a, b) { return a - b; }); ys.sort(function (a, b) { return a - b; });
  var n = Math.max(xs.length, ys.length, 1), Hh = 40 + n * 34, svg = L.s('svg', { viewBox: '0 0 320 ' + Hh, role: 'img', 'aria-label': 'Mapping diagram', style: 'width:100%;height:auto' }, mapBox);
  [[70, 'Inputs (x)', xs], [250, 'Outputs (y)', ys]].forEach(function (c) {
    L.s('ellipse', { cx: c[0], cy: Hh / 2 + 10, rx: 44, ry: Hh / 2 - 18, fill: 'var(--wash)', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    var t = L.s('text', { x: c[0], y: 16, 'text-anchor': 'middle', class: 'g-label', 'font-size': 13 }, svg); t.textContent = c[1];
  });
  function yAt(i, len) { return 40 + (i + 0.5) * ((Hh - 50) / len); }
  var counts = {}; st.pts.forEach(function (p) { counts[p[0]] = (counts[p[0]] || 0) + 1; });
  st.pts.forEach(function (p) {
    var y1 = yAt(xs.indexOf(p[0]), xs.length), y2 = yAt(ys.indexOf(p[1]), ys.length), bad = counts[p[0]] > 1;
    L.s('line', { x1: 92, y1: y1, x2: 222, y2: y2, stroke: bad ? 'var(--red)' : 'var(--blue)', 'stroke-width': bad ? 3 : 2 }, svg);
    L.s('path', { d: 'M222 ' + y2 + ' l -10 -5 v 10 z', fill: bad ? 'var(--red)' : 'var(--blue)' }, svg);
  });
  xs.forEach(function (v, i) { var t = L.s('text', { x: 70, y: yAt(i, xs.length) + 5, 'text-anchor': 'middle', class: 'g-label', fill: counts[v] > 1 ? 'var(--red)' : null }, svg); t.textContent = L.num(v); });
  ys.forEach(function (v, i) { var t = L.s('text', { x: 250, y: yAt(i, ys.length) + 5, 'text-anchor': 'middle', class: 'g-label' }, svg); t.textContent = L.num(v); });
}
var draw = L.scheduler(function () {
  var r = R[st.rel];
  g.clear(); mapBox.innerHTML = '';
  if (st.rel === 'pts') { st.pts.forEach(function (p) { g.dot(p[0], p[1], { color: 'blue', r: 8 }); }); tip.textContent = 'Click the grid to add a point. Click a point to remove it.'; }
  else { r.draw(g); tip.textContent = 'Drag the orange handle to slide the vertical line across the graph.'; }
  var x = st.vx, ys = st.rel === 'pts' ? ptsYs(x) : r.ys(x);
  var hits = ys.length && ys[0] === 'all' ? Infinity : ys.length, bad = hits > 1;
  g.line(x, -10, x, 10, { color: bad ? 'red' : 'orange', width: 4, dash: '10 6' });
  if (ys[0] === 'all') g.line(x, -10, x, 10, { color: 'red', width: 8, opacity: .5 });
  else ys.forEach(function (y) { g.dot(x, y, { color: bad ? 'red' : 'orange', r: 9 }); });
  g.handle(x, -9, { color: 'orange', snap: st.rel === 'pts' ? 1 : 0.25, label: 'Vertical line', onDrag: function (nx) { st.vx = nx; if (nx <= -8) st.swept.lo = true; if (nx >= 8) st.swept.hi = true; draw(); } });
  if (bad) st.failed[st.rel] = true;
  var sweepDone = st.swept.lo && st.swept.hi;
  if (st.rel === 'circle' && sweepDone) st.circleDR = true;
  var verdict = '';
  if (st.rel === 'pts') {
    var isF = ptsIsFunction();
    if (st.pts.length >= 5 && isF) st.ptsFunc = true;
    if (!isF && st.ptsFunc) st.ptsNot = true;
    verdict = isF ? '<span class="c-green">Function:</span> every input has exactly one output.' : '<span class="c-red">Not a function:</span> an input has more than one output (red in the diagram).';
    mapping();
  } else if (bad) verdict = '<span class="c-red">Not a function.</span> At ' + L.V('x') + ' = ' + L.num(x) + ' the line hits ' + (hits === Infinity ? 'infinitely many' : hits) + ' points.';
  else if (sweepDone) { if (r.fn) { st.passed[st.rel] = true; verdict = '<span class="c-green">Function.</span> The line never hit more than one point.'; } else verdict = '<span class="c-red">Not a function.</span> Somewhere the line hits two points.'; }
  else verdict = 'Keep sweeping: drag the line from the far left to the far right.';
  read.innerHTML = '<div>' + verdict + '</div><div class="sub" style="margin-top:6px">At ' + L.V('x') + ' = ' + L.num(x) + ': ' + (hits === Infinity ? 'every ' + L.V('y') : hits ? ys.map(function (y) { return '(' + L.num(x) + ', ' + L.num(y) + ')'; }).join(', ') : 'no points') + '</div>' +
    (st.rel !== 'pts' && sweepDone ? '<dl class="kv" style="margin-top:8px;text-align:left"><dt>Domain</dt><dd>' + r.dom + '</dd><dt>Range</dt><dd>' + r.ran + '</dd></dl>' : '');
  ch.update();
});
draw();
