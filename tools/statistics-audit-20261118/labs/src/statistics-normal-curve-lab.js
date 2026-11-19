/* Normal Curve lab: X ~ N(μ, σ). Shade X < a, X > a, a < X < b or the two tails, read z-scores and the area two ways
   (exact and Table A with z rounded to two decimals), or run the inverse: give an area and find the cutoff.
   Φ uses the Abramowitz–Stegun 7.1.26 erf approximation (error < 1.5e-7); the inverse uses bisection on Φ. */
var st = { mu: 100, sd: 15, za: 1, zb: 2, mode: 'left', p: 0.9, seen: {} };
function phi(z) { var t = 1 / (1 + 0.3275911 * Math.abs(z) / Math.SQRT2), y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-z * z / 2); return z >= 0 ? (1 + y) / 2 : (1 - y) / 2; }
function invPhi(p) { var lo = -8, hi = 8; for (var i = 0; i < 80; i++) { var m = (lo + hi) / 2; if (phi(m) < p) lo = m; else hi = m; } return (lo + hi) / 2; }
function tab(z) { return Math.round(phi(Math.round(z * 100) / 100) * 1e4) / 1e4; }
function dens(x) { var z = (x - st.mu) / st.sd; return Math.exp(-z * z / 2) / (st.sd * Math.sqrt(2 * Math.PI)); }
var GO = { xmin: 40, xmax: 160, ymin: -0.004, ymax: 0.03, width: 640, height: 360, label: 'Normal curve with the shaded area', noYAxis: true, yfmt: function () { return ''; } }, g = L.graph(P.stage, GO);
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Drag the orange (and purple) cutoff, or use the sliders. The shaded area is the probability.');
var GZ = { xmin: -4, xmax: 4, ymin: -0.06, ymax: 0.45, width: 640, height: 220, label: 'Standard Normal curve with the same area', noYAxis: true, yfmt: function () { return ''; } }, gz = L.graph(P.stage, GZ);
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Bottom: the same area on the z scale. Standardizing changes the numbers on the axis, not the area.');
L.chips(P.panel, { label: 'Model', value: '100,15', options: [{ value: '100,15', label: 'IQ N(100, 15)' }, { value: '64,2.5', label: 'Heights N(64, 2.5)' }, { value: '500,100', label: 'Scores N(500, 100)' }, { value: '0,1', label: 'Z N(0, 1)' }],
  onChange: function (v) { var m = v.split(',').map(Number); st.mu = m[0]; st.sd = m[1]; sa.set(st.za, true); sb.set(st.zb, true); draw(); } });
L.chips(P.panel, { label: 'Shade', value: st.mode, options: [{ value: 'left', label: 'X < a' }, { value: 'right', label: 'X > a' }, { value: 'between', label: 'a < X < b' }, { value: 'tails', label: 'Both tails' }, { value: 'inverse', label: 'Find a from an area' }],
  onChange: function (v) { st.mode = v; if (v === 'tails' && st.za > 0) { st.za = -st.za; sa.set(st.za, true); } draw(); } });
function xfmt(z) { return L.num(st.mu + z * st.sd, 2) + ' (z = ' + L.num(z, 2) + ')'; }
var sa = L.slider(P.panel, { id: 'cut-a', label: 'a, cutoff', min: -3.5, max: 3.5, step: 0.01, value: st.za, color: 'orange', format: xfmt, onInput: function (v) { st.za = v; draw(); } });
var sb = L.slider(P.panel, { id: 'cut-b', label: 'b, second cutoff (a < X < b)', min: -3.5, max: 3.5, step: 0.01, value: st.zb, color: 'purple', format: xfmt, onInput: function (v) { st.zb = v; draw(); } });
var sp = L.slider(P.panel, { id: 'area', label: 'Area to the left of a (inverse mode)', min: 0.01, max: 0.99, step: 0.01, value: st.p, color: 'green', format: function (v) { return L.num(v, 2); }, onInput: function (v) { st.p = v; draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st.mu = 100; st.sd = 15; st.za = 1; st.zb = 2; st.mode = 'left'; st.p = 0.9; sa.set(1, true); sb.set(2, true); sp.set(0.9, true); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'IQ scores are N(100, 15). Shade the proportion of people with IQ above 130. About what percent is it?', check: function () { return st.seen.iq130; } },
  { text: 'Check the empirical rule: shade the area within one standard deviation of the mean.', check: function () { return st.seen.rule68; } },
  { text: 'Find the 90th percentile of heights N(64, 2.5) with the inverse mode.', check: function () { return st.seen.p90; } },
  { text: 'Shade both tails beyond z = ±1.96. What total area do you get?', check: function () { return st.seen.tails95; } },
  { text: 'Put a one standard deviation above the mean (X < a), then switch to another model. Does the area change?', check: function () { return st.seen.sameZ; } }
]);
L.notice(P.below, '<p><b>Standardize:</b> z = (x − μ)/σ tells how many standard deviations x is from the mean. Every Normal curve has the same area beyond the same z.</p>' +
  '<p><b>Table A</b> gives the area to the <b>left</b> of z, with z rounded to two decimal places. For a right tail use 1 − (table value); for an interval, subtract two table values.</p>' +
  '<p><b>Inverse:</b> to find a percentile, look up the area inside Table A to get z, then x = μ + zσ.</p>');
var draw = L.scheduler(function () {
  var mu = st.mu, sd = st.sd, lo = mu - 4 * sd, hi = mu + 4 * sd, top = dens(mu);
  if (st.mode === 'inverse') st.za = invPhi(st.p);
  if (st.mode === 'between' && st.zb <= st.za) { st.zb = Math.min(3.5, st.za + 1); sb.set(st.zb, true); }
  if (st.mode === 'tails') { st.za = -Math.abs(st.za) || -1; st.zb = -st.za; }
  st.a = mu + st.za * sd; st.b = mu + st.zb * sd;
  L.setNiceView(g, GO, { xmin: lo, xmax: hi, ymin: -0.14 * top, ymax: 1.12 * top }, 8, 4); g.clear(); gz.clear();
  var za = st.za, zb = st.zb, segs = [], area, tarea;
  if (st.mode === 'left' || st.mode === 'inverse') { segs = [[lo, st.a]]; area = phi(za); tarea = tab(za); }
  else if (st.mode === 'right') { segs = [[st.a, hi]]; area = 1 - phi(za); tarea = 1 - tab(za); }
  else if (st.mode === 'between') { segs = [[st.a, st.b]]; area = phi(zb) - phi(za); tarea = tab(zb) - tab(za); }
  else { segs = [[lo, st.a], [st.b, hi]]; area = phi(za) + 1 - phi(zb); tarea = tab(za) + 1 - tab(zb); }
  segs.forEach(function (sg) {
    var a = Math.max(lo, sg[0]), b = Math.min(hi, sg[1]); if (b <= a) return;
    var pts = [[a, 0]], pz = [[(a - mu) / sd, 0]];
    for (var i = 0; i <= 120; i++) { var x = a + (b - a) * i / 120; pts.push([x, dens(x)]); pz.push([(x - mu) / sd, dens(x) * sd]); }
    pts.push([b, 0]); pz.push([(b - mu) / sd, 0]);
    g.poly(pts, { fill: 'blue', opacity: 0.35 }); gz.poly(pz, { fill: 'green', opacity: 0.35 });
  });
  g.fn(dens, { color: 'blue', width: 3 }); gz.fn(function (z) { return Math.exp(-z * z / 2) / Math.sqrt(2 * Math.PI); }, { color: 'green', width: 3 });
  [-3, -2, -1, 1, 2, 3].forEach(function (k) { g.line(mu + k * sd, 0, mu + k * sd, dens(mu + k * sd), { color: 'ghost', width: 1.5, dash: '4 5' }); });
  g.text(mu, 0, 'μ', { dy: -6, anchor: 'middle', color: 'ink', size: 14 });
  g.handle(st.a, 0, { color: 'orange', snap: sd / 100, label: 'Cutoff a', onDrag: function (nx) { if (st.mode === 'inverse') return; st.za = Math.max(-3.5, Math.min(3.5, L.round((nx - mu) / sd, 2))); sa.set(st.za, true); draw(); } });
  if (st.mode === 'between') g.handle(st.b, 0, { color: 'purple', snap: sd / 100, label: 'Cutoff b', onDrag: function (nx) { st.zb = Math.max(st.za + 0.01, Math.min(3.5, L.round((nx - mu) / sd, 2))); sb.set(st.zb, true); draw(); } });
  if (st.mode === 'tails') g.dot(st.b, 0, { color: 'purple', r: 7 });
  gz.line(za, -0.02, za, 0.42, { color: 'orange', width: 2, dash: '5 4' });
  if (st.mode === 'between' || st.mode === 'tails') gz.line(zb, -0.02, zb, 0.42, { color: 'purple', width: 2, dash: '5 4' });
  var zs = 'z<sub>a</sub> = (' + L.num(st.a, 2) + ' − ' + L.nice(mu) + ')/' + L.nice(sd) + ' = <b>' + L.num(za, 2) + '</b>' + (st.mode === 'between' || st.mode === 'tails' ? ' · z<sub>b</sub> = <b>' + L.num(zb, 2) + '</b>' : '');
  read.innerHTML = 'X ~ N(' + L.nice(mu) + ', ' + L.nice(sd) + ')<div style="margin-top:6px">' + zs + '</div>' +
    '<div style="margin-top:6px">Shaded area = <b>' + L.num(area, 4) + '</b> <span class="sub">(Table A with z to two decimals: ' + L.num(tarea, 4) + ')</span></div>' +
    (st.mode === 'inverse' ? '<div style="margin-top:4px">Area ' + L.num(st.p, 2) + ' to the left: z = ' + L.num(za, 3) + ', so a = ' + L.nice(mu) + ' + (' + L.num(za, 3) + ')(' + L.nice(sd) + ') = <b>' + L.num(st.a, 2) + '</b></div>' : '');
  fb.set(area < 0.05 ? 'Less than 5% of the distribution is shaded: an unusual region.' : Math.abs(area - 0.6827) < 0.003 ? 'About 68%: the area within one standard deviation of the mean.' : '', area < 0.05 ? 'warn' : '');
  if (mu === 100 && sd === 15 && st.mode === 'right' && Math.abs(za - 2) < 0.001) st.seen.iq130 = true;
  if (st.mode === 'between' && Math.abs(za + 1) < 0.01 && Math.abs(zb - 1) < 0.01) st.seen.rule68 = true;
  if (st.mode === 'inverse' && mu === 64 && sd === 2.5 && Math.abs(st.p - 0.9) < 0.001) st.seen.p90 = true;
  if (st.mode === 'tails' && Math.abs(za + 1.96) < 0.001) st.seen.tails95 = true;
  if (Math.abs(za - 1) < 0.001 && st.mode === 'left') { st.seen.sdz = st.seen.sdz || {}; st.seen.sdz[mu + ',' + sd] = true; if (Object.keys(st.seen.sdz).length >= 2) st.seen.sameZ = true; }
  ch.update();
});
draw();
