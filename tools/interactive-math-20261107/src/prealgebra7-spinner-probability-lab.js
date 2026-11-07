/* A spinner with up to four colors. Each color gets a number of equal parts, so P(color) = parts / total parts.
   Spins are random; the running share of red is graphed against the number of spins. */
var COLS = [{ id: 'red', name: 'Red', c: 'red', l: 'R' }, { id: 'blue', name: 'Blue', c: 'blue', l: 'B' }, { id: 'green', name: 'Green', c: 'green', l: 'G' }, { id: 'yellow', name: 'Yellow', c: 'sun', l: 'Y' }];
var st = { parts: [3, 2, 1, 0], counts: [0, 0, 0, 0], n: 0, hist: [], last: null, recent: [], seen: {} };
function total() { return st.parts.reduce(function (a, b) { return a + b; }, 0); }
function prob(i) { return st.parts[i] / total(); }
function spin(k) {
  var T = total();
  for (var j = 0; j < k; j++) {
    var r = Math.random() * T, i = 0, acc = st.parts[0];
    while (r >= acc && i < 3) { i++; acc += st.parts[i]; }
    st.counts[i]++; st.n++; st.last = i; st.recent.push(i); if (st.recent.length > 20) st.recent.shift();
    st.hist.push(st.counts[0] / st.n);
    checkRun();
  }
  draw();
}
function checkRun() {
  var n = st.n;
  if (n === 10 || n === 20) for (var i = 0; i < 4; i++) if (st.parts[i] && Math.abs(st.counts[i] / n - prob(i)) >= 0.2 - 1e-9) st.seen.miss = true;
  if (n >= 1000 && COLS.every(function (c, i) { return Math.abs(st.counts[i] / n - prob(i)) <= 0.03; })) st.seen.lln = true;
}
function clearRuns() { st.counts = [0, 0, 0, 0]; st.n = 0; st.hist = []; st.last = null; st.recent = []; }

var W = 640, H = 300;
var svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Spinner and results' }, P.stage);
var g = L.graph(P.stage, { xmin: 0, xmax: 100, ymin: -0.04, ymax: 1, width: 640, height: 260, ystep: 0.1, ylabelStep: 0.2, label: 'Share of red so far' });
L.h('div', { class: 'legend', style: 'margin:6px' }, P.stage, '<span><i style="background:var(--red)"></i>share of spins that were red so far</span><span><i style="background:var(--ink)"></i>theoretical P(red)</span>');
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
L.h('h2', null, P.panel, 'Build the spinner');
var sliders = COLS.map(function (c, i) {
  return L.slider(P.panel, { id: c.id + '-parts', label: c.name + ' parts', min: 0, max: 8, value: st.parts[i], color: c.c === 'sun' ? 'orange' : c.c, format: L.num,
    onInput: function (v) { if (total() - st.parts[i] + v === 0) { sliders[i].set(st.parts[i], true); fb.set('A spinner needs at least one part.', 'warn'); return; } st.parts[i] = v; clearRuns(); draw(); } });
});
L.h('p', { class: 'lp-mini' }, P.panel, 'Changing the spinner clears the results, because old spins came from a different spinner.');
L.h('h2', null, P.panel, 'Spin');
var row = L.h('div', { class: 'btn-row' }, P.panel);
[1, 10, 100, 1000].forEach(function (k) { L.button(row, 'Spin ' + k.toLocaleString(), function () { spin(k); }, k !== 10); });
var row2 = L.h('div', { class: 'btn-row' }, P.panel);
L.button(row2, 'Clear results', function () { clearRuns(); draw(); }, true);
L.reset(row2, function () { st.parts = [3, 2, 1, 0]; sliders.forEach(function (s, i) { s.set(st.parts[i], true); }); clearRuns(); draw(); });
var tbl = L.table(P.panel);
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Build a spinner with at least 3 colors where P(red) = ' + L.frac(1, 4) + '.', check: function () { return st.seen.quarter; } },
  { text: 'Clear the results and spin 10 times. Find a run where some color’s share misses its theoretical probability by 0.2 or more.', check: function () { return st.seen.miss; } },
  { text: 'Predict how many reds you expect in 200 spins. Clear, spin exactly 200 times, and compare.', check: function () { return st.n === 200; } },
  { text: 'Spin until every color is within 0.03 of its theoretical probability (1,000 spins or more).', check: function () { return st.seen.lln; } },
  { text: 'Red came up several times in a row. Is blue now “due”? Make a spinner where the answer is easy to see: make blue <b>impossible</b>, then <b>certain</b>.', check: function () { return st.seen.imp && st.seen.cert; } }
]);
L.notice(P.below, '<p><b>Theoretical probability</b> comes from the spinner: P(color) = ' + L.frac('parts for that color', 'total parts') + '. <b>Experimental probability</b> comes from spinning: ' + L.frac('times it happened', 'total spins') + '.</p>' +
  '<p>With a few spins the two can be far apart. With many spins the experimental share settles close to the theoretical probability (but almost never exactly on it).</p>' +
  '<p>The spinner has no memory: every spin has the same probabilities, no matter what came before. The expected number of results is P × number of spins.</p>');

function wedge(cx, cy, r, a0, a1) { var x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0), x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1); return 'M' + cx + ' ' + cy + ' L' + x0 + ' ' + y0 + ' A' + r + ' ' + r + ' 0 ' + (a1 - a0 > Math.PI ? 1 : 0) + ' 1 ' + x1 + ' ' + y1 + ' Z'; }
var draw = L.scheduler(function () {
  var T = total(), cx = 150, cy = 150, r = 120;
  svg.innerHTML = '';
  var a = -Math.PI / 2, mids = [];
  COLS.forEach(function (c, i) {
    if (!st.parts[i]) { mids.push(null); return; }
    var da = st.parts[i] / T * 2 * Math.PI;
    if (st.parts[i] === T) L.s('circle', { cx: cx, cy: cy, r: r, fill: 'var(--' + c.c + ')', stroke: 'var(--ink)', 'stroke-width': 3 }, svg);
    else L.s('path', { d: wedge(cx, cy, r, a, a + da), fill: 'var(--' + c.c + ')', stroke: 'var(--ink)', 'stroke-width': 3, 'stroke-linejoin': 'round' }, svg);
    for (var k = 1; k < st.parts[i]; k++) { var ak = a + k * 2 * Math.PI / T; L.s('line', { x1: cx, y1: cy, x2: cx + r * Math.cos(ak), y2: cy + r * Math.sin(ak), stroke: 'var(--ink)', 'stroke-width': 1, opacity: 0.5 }, svg); }
    var am = a + da / 2; mids.push(am);
    var tl = L.s('text', { x: cx + r * 0.62 * Math.cos(am), y: cy + r * 0.62 * Math.sin(am) + 6, 'text-anchor': 'middle', 'font-size': 20, 'font-weight': 800, fill: '#ffffff', stroke: '#14173a', 'stroke-width': 4, 'paint-order': 'stroke', 'font-family': 'var(--display)' }, svg); tl.textContent = c.l;
    a += da;
  });
  if (st.last !== null && mids[st.last] !== null) {
    var am2 = mids[st.last];
    L.s('line', { x1: cx, y1: cy, x2: cx + (r - 18) * Math.cos(am2), y2: cy + (r - 18) * Math.sin(am2), stroke: 'var(--ink)', 'stroke-width': 6, 'stroke-linecap': 'round' }, svg);
  }
  L.s('circle', { cx: cx, cy: cy, r: 10, fill: 'var(--card)', stroke: 'var(--ink)', 'stroke-width': 3 }, svg);
  /* bar chart: theoretical outline vs experimental fill */
  var bx = 320, bw = 60, by = 250, bh = 200;
  L.s('line', { x1: bx - 10, x2: W - 10, y1: by, y2: by, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
  [0, 0.5, 1].forEach(function (v) { var ty = L.s('text', { x: bx - 14, y: by - v * bh + 4, 'text-anchor': 'end', class: 'g-tick' }, svg); ty.textContent = v; L.s('line', { x1: bx - 10, x2: W - 10, y1: by - v * bh, y2: by - v * bh, stroke: 'var(--grid)' }, svg); });
  COLS.forEach(function (c, i) {
    var x = bx + i * (bw + 16), th = prob(i), ex = st.n ? st.counts[i] / st.n : 0;
    if (st.n) L.s('rect', { x: x, y: by - ex * bh, width: bw, height: ex * bh, fill: 'var(--' + c.c + ')', opacity: 0.85 }, svg);
    L.s('rect', { x: x, y: by - th * bh, width: bw, height: th * bh, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2.5, 'stroke-dasharray': '6 4' }, svg);
    var tt = L.s('text', { x: x + bw / 2, y: by + 20, 'text-anchor': 'middle', class: 'g-label', 'font-size': 14 }, svg); tt.textContent = c.name;
  });
  var cap = L.s('text', { x: bx - 10, y: 30, class: 'g-tick', 'font-size': 13 }, svg); cap.textContent = 'dashed = theoretical · filled = experimental';
  /* running share of red */
  var n = Math.max(20, st.n);
  g.setView({ xmin: -n * 0.05, xmax: n, ymin: -0.04, ymax: 1 }); g.clear();
  g.line(0, prob(0), n, prob(0), { color: 'ink', width: 2, dash: '8 6' });
  if (st.hist.length > 1) {
    var stp = Math.max(1, Math.floor(st.hist.length / 600)), d = '';
    for (var j = 0; j < st.hist.length; j += stp) d += (d ? 'L' : 'M') + g.X(j + 1).toFixed(1) + ' ' + g.Y(st.hist[j]).toFixed(1);
    d += 'L' + g.X(st.hist.length).toFixed(1) + ' ' + g.Y(st.hist[st.hist.length - 1]).toFixed(1);
    L.s('path', { d: d, fill: 'none', stroke: 'var(--red)', 'stroke-width': 3 }, g.layer);
  }
  /* table + readout */
  tbl.set(['Color', 'Theoretical', 'Count', 'Experimental', 'Expected count'], COLS.map(function (c, i) {
    return [c.name, st.parts[i] ? L.frac(st.parts[i], T) + ' ≈ ' + L.num(prob(i), 3) : '0', st.counts[i], st.n ? L.num(st.counts[i] / st.n, 3) : '—', L.num(prob(i) * st.n, 1)];
  }));
  read.innerHTML = st.n ? st.n.toLocaleString() + ' spins · last: <b>' + COLS[st.last].name + '</b><div class="sub" style="margin-top:4px">last spins: ' + st.recent.map(function (i) { return COLS[i].l; }).join(' ') + '</div>' : 'P(red) = ' + (st.parts[0] ? L.frac(st.parts[0], T) : '0') + '. Spin to collect results.';
  if (!st.n) fb.set('Theoretical probabilities come from the spinner. Spin to compare.', '');
  else { var worst = 0; COLS.forEach(function (c, i) { worst = Math.max(worst, Math.abs(st.counts[i] / st.n - prob(i))); }); fb.set('Largest gap between experimental and theoretical: ' + L.num(worst, 3) + (st.n < 50 ? '. With so few spins, big gaps are normal.' : st.n >= 1000 ? '. Many spins: the shares settle near the theoretical values.' : '.'), worst <= 0.03 && st.n >= 500 ? 'good' : ''); }
  if (st.parts[0] * 4 === T && st.parts.filter(function (p) { return p > 0; }).length >= 3) st.seen.quarter = true;
  if (st.parts[1] === 0) st.seen.imp = true;
  if (st.parts[1] > 0 && st.parts[1] === T) st.seen.cert = true;
  ch.update();
});
draw();
