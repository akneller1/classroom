/* Least-squares regression with a linked residual plot. ŷ = a + bx with b = r·(s_y/s_x), a = ȳ − b·x̄.
   s = √(Σ residual² / (n − 2)). An optional extra point (orange square) shows outliers, leverage and influence:
   the dashed line is the LSRL without it. Thresholds (stated on screen): outlier |residual| > 2s;
   high leverage |x − x̄| > 2·s_x of the other points; influential when the slope changes by 50% or more. */
var DATA = {
  study: { label: 'Study time and test score', xl: 'study time', yl: 'test score', xu: 'hours', yu: 'points', pts: [[0, 48], [1, 55], [1, 60], [2, 58], [3, 66], [4, 62], [4, 71], [5, 70], [6, 77], [7, 74], [8, 85], [9, 83]], view: [-0.6, 12.6, 0, 112], extra: [6, 30] },
  growth: { label: 'Age and height (one child)', xl: 'age', yl: 'height', xu: 'years', yu: 'inches', pts: [[2, 36], [4, 42], [6, 47], [8, 51], [10, 55], [12, 58], [14, 61], [16, 63], [18, 65]], view: [0, 20.6, 28, 72], extra: [10, 40] }
};
var st = { ds: 'study', pts: null, extra: false, ex: null, mins: false, seen: {} };
function D() { return DATA[st.ds]; }
function k() { return st.ds === 'study' && st.mins ? 60 : 1; }   /* x shown in minutes = hours × 60 */
function fit(P) {
  var n = P.length, mx = 0, my = 0, i; for (i = 0; i < n; i++) { mx += P[i][0]; my += P[i][1]; } mx /= n; my /= n;
  var sxx = 0, syy = 0, sxy = 0; for (i = 0; i < n; i++) { var dx = P[i][0] - mx, dy = P[i][1] - my; sxx += dx * dx; syy += dy * dy; sxy += dx * dy; }
  if (sxx < 1e-12) return null;
  var b = sxy / sxx, a = my - b * mx, r = syy > 1e-12 ? sxy / Math.sqrt(sxx * syy) : NaN, sse = 0;
  for (i = 0; i < n; i++) { var e = P[i][1] - (a + b * P[i][0]); sse += e * e; }
  return { a: a, b: b, r: r, s: n > 2 ? Math.sqrt(sse / (n - 2)) : NaN, mx: mx, sx: Math.sqrt(sxx / (n - 1)) };
}
function shown(p) { return [p[0] * k(), p[1]]; }
function load() { st.pts = D().pts.map(function (p) { return p.slice(); }); st.ex = D().extra.slice(); }
load();
var GO = { xmin: 0, xmax: 1, ymin: 0, ymax: 1, width: 640, height: 400, label: 'Scatterplot with the least-squares line' };
var GR = { xmin: 0, xmax: 1, ymin: -1, ymax: 1, width: 640, height: 210, label: 'Residual plot' };
L.h('p', { class: 'sub', style: 'margin:0 6px 4px;font-weight:700' }, P.stage, 'Scatterplot');
var g = L.graph(P.stage, GO);
L.h('div', { class: 'legend', style: 'margin:6px' }, P.stage, '<span><i style="background:var(--blue)"></i>least-squares line</span><span><i style="background:var(--ghost)"></i>line without the extra point (dashed)</span><span><i style="background:var(--orange)"></i>extra point (square)</span>');
L.h('p', { class: 'sub', style: 'margin:8px 6px 4px;font-weight:700' }, P.stage, 'Residual plot: residual = actual y − predicted ŷ');
var gr = L.graph(P.stage, GR);
L.chips(P.panel, { label: 'Data', value: st.ds, options: Object.keys(DATA).map(function (x) { return { value: x, label: DATA[x].label }; }), onChange: function (v) { st.ds = v; st.mins = false; load(); build(); draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var opt = L.h('div', { class: 'btn-row' }, P.panel);
var bE = L.button(opt, 'Add an extra point', function () { st.extra = !st.extra; draw(); build(); }, true);
var uBox = L.h('div', null, P.panel);
var row = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(row, function () { st.extra = false; st.mins = false; load(); build(); draw(); });
L.h('p', { class: 'sub' }, P.panel, 'Drag any point, or click it and use the arrow keys (steps of 1).');
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Switch to the age and height data. Predict: with r this close to 1, is a line a good model? What does the residual plot show?', check: function () { return st.seen.curve; } },
  { text: 'Add the extra point and place it so it is an <b>outlier</b> (|residual| &gt; 2s) but changes the slope by less than 10%.', check: function () { return st.seen.outlierOnly; } },
  { text: 'Place the extra point so it is <b>influential</b>: it changes the slope by 50% or more. Where did it have to go?', check: function () { return st.seen.influential; } },
  { text: 'Place the extra point far to the right (high leverage) so that it is <b>not</b> influential: the slope changes by less than 5%.', check: function () { return st.seen.leverageOnly; } },
  { text: 'Predict, then test: change study time from hours to minutes. What happens to the slope, to r and to r²?', check: function () { return st.seen.units; } }
]);
L.notice(P.below, '<p><b>Check the residual plot, not just r.</b> A curved pattern in the residuals means a line is the wrong model, even when r is close to 1. A good linear model leaves residuals scattered randomly around 0.</p>' +
  '<p>r² is the fraction of the variation in y that is accounted for by the linear model. s is the typical size of a residual (a typical prediction error), in the units of y.</p>' +
  '<p>An <b>outlier</b> has a large residual. A point with <b>high leverage</b> has an x-value far from the others. A point is <b>influential</b> if removing it changes the line a lot; high-leverage points that don’t follow the pattern are usually the influential ones.</p>' +
  '<p>Changing units rescales the slope (points per hour ÷ 60 = points per minute) but does not change r or r², which have no units.</p>');
function build() {
  bE.textContent = st.extra ? 'Remove the extra point' : 'Add an extra point';
  uBox.innerHTML = '';
  if (st.ds === 'study') L.chips(uBox, { label: 'Units for study time', value: st.mins, options: [{ value: false, label: 'hours' }, { value: true, label: 'minutes' }], onChange: function (v) { st.mins = v; draw(); } });
}
var draw = L.scheduler(function () {
  var d = D(), K = k(), v = d.view;
  var base = st.pts.map(shown), all = st.extra ? base.concat([shown(st.ex)]) : base;
  var F = fit(all), F0 = fit(base);
  L.setNiceView(g, GO, { xmin: v[0] * K, xmax: v[1] * K, ymin: v[2], ymax: v[3] }, 8, 10); g.clear();
  if (F0 && st.extra) g.fullLine(0, F0.a, 1, F0.a + F0.b, { color: 'ghost', width: 3, dash: '8 6' });
  if (F) g.fullLine(0, F.a, 1, F.a + F.b, { color: 'blue', width: 4 });
  st.pts.forEach(function (p, i) {
    g.handle(p[0] * K, p[1], { color: 'blue', r: 8, snap: K, label: 'Data point ' + (i + 1), onDrag: function (x, y) {
      st.pts[i] = [Math.round(Math.max(v[0], Math.min(v[1], x / K))), Math.round(Math.max(v[2], Math.min(v[3], y)))]; draw(); } });
  });
  if (st.extra) {
    var ex = shown(st.ex);
    var hd = g.handle(ex[0], ex[1], { color: 'orange', r: 9, snap: K, label: 'Extra point', onDrag: function (x, y) {
      st.ex = [Math.round(Math.max(v[0], Math.min(v[1], x / K))), Math.round(Math.max(v[2], Math.min(v[3], y)))]; draw(); } });
    /* a square frame marks the extra point by shape as well as color */
    L.s('rect', { x: +hd.getAttribute('cx') - 15, y: +hd.getAttribute('cy') - 15, width: 30, height: 30, fill: 'none', stroke: 'var(--orange)', 'stroke-width': 3, 'pointer-events': 'none' }, hd.parentNode);
  }
  /* residual plot */
  var res = F ? all.map(function (p) { return [p[0], p[1] - (F.a + F.b * p[0])]; }) : [];
  var M = Math.max(2, Math.max.apply(null, res.map(function (q) { return Math.abs(q[1]); }).concat([0])) * 1.25);
  L.setNiceView(gr, GR, { xmin: v[0] * K, xmax: v[1] * K, ymin: -M, ymax: M }, 5, 10); gr.clear();
  gr.line(v[0] * K, 0, v[1] * K, 0, { color: 'ink', width: 2 });
  res.forEach(function (q, i) { var isEx = st.extra && i === res.length - 1;
    gr.line(q[0], 0, q[0], q[1], { color: isEx ? 'orange' : 'blue', width: 1.5, opacity: 0.5 });
    if (isEx) gr.rect(q[0] - 0.18 * K, q[1] - M * 0.05, 0.36 * K, M * 0.1, { fill: 'orange', stroke: 'ink', width: 2 }); else gr.dot(q[0], q[1], { color: 'blue', r: 6 }); });
  if (!F) { read.innerHTML = 'All x-values are equal, so there is no least-squares line.'; info.innerHTML = ''; fb.set('Spread the points out horizontally.', 'warn'); ch.update(); return; }
  var xu = st.ds === 'study' && st.mins ? 'minute' : d.xu.replace(/s$/, ''), yu = d.yu;
  read.innerHTML = 'ŷ = ' + L.num(F.a, 2) + (F.b < 0 ? ' − ' : ' + ') + L.num(Math.abs(F.b), K === 60 ? 4 : 3) + L.V('x') +
    '<div class="sub" style="margin-top:4px">Predicted ' + d.yl + ' changes by ' + L.num(F.b, K === 60 ? 4 : 3) + ' ' + yu + ' for each additional ' + xu + ' of ' + d.xl + '.</div>';
  var rows = '<dt>r</dt><dd>' + L.num(F.r, 4) + '</dd><dt>r²</dt><dd>' + L.num(F.r * F.r, 4) + ' (' + L.num(100 * F.r * F.r, 1) + '% of the variation in ' + d.yl + ')</dd><dt>s</dt><dd>' + L.num(F.s, 3) + ' ' + yu + '</dd>';
  var tags = [];
  if (st.extra) {
    var e = shown(st.ex), re = e[1] - (F.a + F.b * e[0]), dB = F0 ? (F.b - F0.b) / Math.abs(F0.b) : 0, lev = F0 ? Math.abs(e[0] - F0.mx) / F0.sx : 0;
    var isOut = Math.abs(re) > 2 * F.s, isLev = lev > 2, isInf = Math.abs(dB) >= 0.5;
    rows += '<dt>Extra point residual</dt><dd>' + L.num(re, 2) + ' (' + L.num(re / F.s, 2) + 's)</dd><dt>Slope change</dt><dd>' + (dB >= 0 ? '+' : '−') + L.num(Math.abs(100 * dB), 1) + '%</dd><dt>Distance from x̄</dt><dd>' + L.num(lev, 2) + ' SDs of x</dd>';
    if (isOut) tags.push('an <b>outlier</b> (|residual| &gt; 2s)'); if (isLev) tags.push('a <b>high-leverage</b> point (x more than 2 SDs from x̄)'); if (isInf) tags.push('<b>influential</b> (slope changed by 50% or more)');
    if (isOut && Math.abs(dB) < 0.1) st.seen.outlierOnly = true;
    if (isInf) st.seen.influential = true;
    if (st.ex[0] >= (st.ds === 'study' ? 11 : 19) && Math.abs(dB) < 0.05) st.seen.leverageOnly = true;
  }
  info.innerHTML = rows;
  var pattern = st.ds === 'growth' && !st.extra;
  fb.set(st.extra ? 'The extra point is ' + (tags.length ? tags.join(' and ') : 'not an outlier, not high leverage and not influential') + '.' :
    (pattern ? 'r is close to 1, but the residuals curve (negative, then positive, then negative). A line is not the right model for these data.' : 'Residuals look scattered around 0 with no clear pattern: a linear model is reasonable.'), pattern ? 'warn' : '');
  if (st.ds === 'growth') st.seen.curve = true;
  if (st.ds === 'study') { st.seen.r = st.seen.r || {}; st.seen.r[st.mins ? 'min' : 'h'] = true; if (st.seen.r.min && st.seen.r.h) st.seen.units = true; }
  ch.update();
});
build(); draw();
