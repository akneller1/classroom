/* Region between top f and bottom g on [a, b] (their intersections). Area: n rectangles of height f − g at midpoints.
   Volume about the x-axis: n washers π(f² − g²)Δx. Exact values are given for comparison. */
var PAIRS = {
  p1: { f: function (x) { return x; }, g: function (x) { return x * x; }, ft: 'y = x', gt: 'y = x²', a: 0, b: 1, area: 1 / 6, areaT: '1/6', vol: 2 * Math.PI / 15, volT: '2π/15', view: [-0.2, 1.4, -0.2, 1.3] },
  p2: { f: function (x) { return 2 * x; }, g: function (x) { return x * x; }, ft: 'y = 2x', gt: 'y = x²', a: 0, b: 2, area: 4 / 3, areaT: '4/3', vol: 64 * Math.PI / 15, volT: '64π/15', view: [-0.3, 2.6, -0.4, 4.6] },
  p3: { f: function (x) { return Math.sqrt(x); }, g: function (x) { return x / 2; }, ft: 'y = √x', gt: 'y = x/2', a: 0, b: 4, area: 4 / 3, areaT: '4/3', vol: 8 * Math.PI / 3, volT: '8π/3', view: [-0.4, 4.8, -0.4, 2.6] },
  p4: { f: function (x) { return 4 - x * x; }, g: function () { return 0; }, ft: 'y = 4 − x²', gt: 'y = 0', a: -2, b: 2, area: 32 / 3, areaT: '32/3', vol: 512 * Math.PI / 15, volT: '512π/15', view: [-2.6, 2.6, -0.6, 4.8] }
};
var st = { pair: 'p1', n: 4, mode: 'area', seen: {} };
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
L.chips(P.panel, { label: 'Region', value: st.pair, options: [{ value: 'p1', label: 'x and x²' }, { value: 'p2', label: '2x and x²' }, { value: 'p3', label: '√x and x/2' }, { value: 'p4', label: '4 − x² and 0' }], onChange: function (v) { st.pair = v; draw(); } });
L.tabs(P.panel, [{ id: 'area', label: 'Area: rectangles' }, { id: 'vol', label: 'Volume: washers' }], function (id) { st.mode = id; draw(); });
var sn = L.slider(P.panel, { id: 'slices-n', label: 'Number of slices n', min: 1, max: 60, step: 1, value: st.n, color: 'orange', format: function (v) { return L.num(v); }, onInput: function (v) { st.n = v; draw(); } });
var tbl = L.table(P.panel);
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'For x and x², use enough rectangles that the sum is within 0.001 of the exact area.', check: function () { return st.seen.close1; } },
  { text: 'Find the intersections of 2x and x². Which curve is on top between them?', check: function () { return st.seen.p2; } },
  { text: 'Switch to washers. With n = 1, what are the outer and inner radii?', check: function () { return st.seen.w1; } },
  { text: 'For √x and x/2, compare π · (area)² with the true volume. Are they equal?', check: function () { return st.seen.p3vol; } },
  { text: 'For 4 − x² and 0, the washers have no hole. What are they called, and what is the volume?', check: function () { return st.seen.p4vol; } }
]);
L.notice(P.below, '<p>Each thin rectangle has height <b>top − bottom</b>, so the area is ∫ from a to b of (f(x) − g(x)) dx, where a and b are where the curves meet.</p>' +
  '<p>Rotating the region about the x-axis makes washers with outer radius f(x) and inner radius g(x). Each washer has volume π(f² − g²)Δx, so V = π∫ (f² − g²) dx. This is <b>not</b> π∫(f − g)² dx and not π times the area squared.</p>');
var gopts = { width: 640, height: 440, label: 'Region between two curves with slices' };
var gr = L.graph(P.stage, gopts);
var draw = L.scheduler(function () {
  var p = PAIRS[st.pair], n = st.n, dx = (p.b - p.a) / n, sumA = 0, sumV = 0, w = p.view;
  if (st.mode === 'vol') L.setNiceView(gr, gopts, { xmin: w[0], xmax: w[1], ymin: -w[3], ymax: w[3] }, 8, 8); else L.setNiceView(gr, gopts, { xmin: w[0], xmax: w[1], ymin: w[2], ymax: w[3] }, 8, 8);
  gr.clear();
  for (var i = 0; i < n; i++) {
    var xm = p.a + (i + 0.5) * dx, top = p.f(xm), bot = p.g(xm);
    sumA += (top - bot) * dx; sumV += Math.PI * (top * top - bot * bot) * dx;
    if (st.mode === 'area') gr.rect(p.a + i * dx, bot, dx, top - bot, { fill: 'orange', opacity: 0.35, stroke: 'orange', width: 1 });
    else { gr.rect(p.a + i * dx, bot, dx, top - bot, { fill: 'orange', opacity: 0.35, stroke: 'orange', width: 1 }); gr.rect(p.a + i * dx, -top, dx, top - bot, { fill: 'orange', opacity: 0.35, stroke: 'orange', width: 1 }); }
  }
  gr.fn(p.f, { color: 'blue' }); gr.fn(p.g, { color: 'purple' });
  if (st.mode === 'vol') { gr.fn(function (x) { return -p.f(x); }, { color: 'blue', dash: '6 6', width: 2 }); gr.fn(function (x) { return -p.g(x); }, { color: 'purple', dash: '6 6', width: 2 }); }
  gr.dot(p.a, p.f(p.a), { color: 'ink' }); gr.dot(p.b, p.f(p.b), { color: 'ink' });
  gr.text(p.b, p.f(p.b), p.ft, { dx: 8, dy: -8, color: 'blue' });
  gr.text(p.a + 0.6 * (p.b - p.a), p.g(p.a + 0.6 * (p.b - p.a)), p.gt, { dy: 22, color: 'purple' });
  var exact = st.mode === 'area' ? p.area : p.vol, sum = st.mode === 'area' ? sumA : sumV;
  read.innerHTML = (st.mode === 'area' ? 'Area ≈ ' : 'Volume ≈ ') + L.num(sum, 5) + '<div class="sub">exact: ' + (st.mode === 'area' ? p.areaT : p.volT + ' ≈ ' + L.num(p.vol, 5)) + ' · error = ' + L.num(Math.abs(sum - exact), 5) + ' · curves meet at x = ' + L.num(p.a) + ' and x = ' + L.num(p.b) + '</div>';
  var x0 = p.a + dx / 2;
  tbl.set(['First slice at x', 'Top (outer radius)', 'Bottom (inner radius)', st.mode === 'area' ? 'Height' : 'Washer area'],
    [[L.num(x0, 4), L.num(p.f(x0), 4), L.num(p.g(x0), 4), st.mode === 'area' ? L.num(p.f(x0) - p.g(x0), 4) : 'π(' + L.num(p.f(x0), 3) + '² − ' + L.num(p.g(x0), 3) + '²)']]);
  fb.set(st.mode === 'area' ? 'Each rectangle: (top − bottom) × Δx, with Δx = ' + L.num(dx, 4) + '.' : 'Each washer: π(outer² − inner²) × Δx. The dashed curves are the mirror image of the region after rotating it.', '');
  if (st.pair === 'p1' && st.mode === 'area' && Math.abs(sumA - p.area) < 0.001) st.seen.close1 = true;
  if (st.pair === 'p2') st.seen.p2 = true;
  if (st.mode === 'vol' && n === 1) st.seen.w1 = true;
  if (st.pair === 'p3' && st.mode === 'vol') st.seen.p3vol = true;
  if (st.pair === 'p4' && st.mode === 'vol') st.seen.p4vol = true;
  ch.update();
});
draw();
