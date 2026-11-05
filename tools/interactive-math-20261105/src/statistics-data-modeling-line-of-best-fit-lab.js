var BASE = [[1, 52], [2, 58], [2, 63], [3, 61], [4, 70], [5, 68], [5, 76], [6, 78], [7, 80], [8, 88]];
var st = { pts: BASE.map(function (p) { return p.slice(); }), l1: [1, 50], l2: [8, 70], showFit: false, showRes: false, seen: {}, outlier: false };
var g = L.graph(P.stage, { xmin: -0.8, xmax: 10, ymin: 30, ymax: 100, width: 620, height: 520, xstep: 1, ystep: 5, ylabelStep: 10, label: 'Scatter plot of hours studied and test score', noYAxis: false });
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>data (drag the points)</span><span><i style="background:var(--orange)"></i>your line (drag its ends)</span><span><i style="background:var(--green)"></i>line of best fit</span>');
L.h('p', { class: 'sub', style: 'margin:4px 6px 0' }, P.stage, 'Hours studied (x) and test score (y) for 10 students.');
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var row = L.h('div', { class: 'btn-row' }, P.panel);
var bFit = L.button(row, 'Show line of best fit', function () { st.showFit = !st.showFit; bFit.textContent = st.showFit ? 'Hide line of best fit' : 'Show line of best fit'; draw(); });
var bRes = L.button(row, 'Show residuals', function () { st.showRes = !st.showRes; bRes.textContent = st.showRes ? 'Hide residuals' : 'Show residuals'; draw(); }, true);
var row2 = L.h('div', { class: 'btn-row' }, P.panel);
L.button(row2, 'Add an outlier', function () { if (!st.outlier) { st.pts.push([8, 40]); st.outlier = true; } draw(); }, true);
L.button(row2, 'Reset data', function () { st.pts = BASE.map(function (p) { return p.slice(); }); st.outlier = false; draw(); }, true);
var info = L.h('dl', { class: 'kv' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Drag your line until its total squared error is within 10% of the best line\'s.', check: function () { return st.seen.close; } },
  { text: 'Drag data points until ' + L.V('r') + ' is greater than 0.97.', check: function () { return st.seen.r97; } },
  { text: 'Add the outlier. What happens to ' + L.V('r') + ' and to the best-fit line?', check: function () { return st.outlier && st.showFit; } },
  { text: 'Drag the points so the correlation is <b>negative</b>.', check: function () { return st.seen.neg; } },
  { text: 'Make ' + L.V('r') + ' close to 0 (between −0.2 and 0.2).', check: function () { return st.seen.zero; } }
]);
function stats(pts) {
  var n = pts.length, mx = 0, my = 0; pts.forEach(function (p) { mx += p[0]; my += p[1]; }); mx /= n; my /= n;
  var sxx = 0, syy = 0, sxy = 0; pts.forEach(function (p) { sxx += (p[0] - mx) * (p[0] - mx); syy += (p[1] - my) * (p[1] - my); sxy += (p[0] - mx) * (p[1] - my); });
  var m = sxx ? sxy / sxx : 0, b = my - m * mx, r = sxx && syy ? sxy / Math.sqrt(sxx * syy) : 0;
  return { m: m, b: b, r: r };
}
function sse(pts, m, b) { var s = 0; pts.forEach(function (p) { var e = p[1] - (m * p[0] + b); s += e * e; }); return s; }
var draw = L.scheduler(function () {
  var S = stats(st.pts);
  var um = (st.l2[1] - st.l1[1]) / ((st.l2[0] - st.l1[0]) || 1e-9), ub = st.l1[1] - um * st.l1[0];
  g.clear();
  if (st.showRes) st.pts.forEach(function (p) { g.line(p[0], p[1], p[0], um * p[0] + ub, { color: 'red', width: 2, dash: '4 4' }); });
  if (st.showFit) g.fullLine(0, S.b, 1, S.b + S.m, { color: 'green', width: 4 });
  g.fullLine(st.l1[0], st.l1[1], st.l2[0], st.l2[1], { color: 'orange', width: 4 });
  st.pts.forEach(function (p, i) {
    g.handle(p[0], p[1], { color: 'blue', r: 8, snap: 0.5, label: 'Data point ' + (i + 1), onDrag: function (x, y) { st.pts[i] = [x, y]; draw(); } });
  });
  g.handle(st.l1[0], st.l1[1], { color: 'orange', snap: 0.5, label: 'Your line, left end', onDrag: function (x, y) { st.l1 = [x, y]; draw(); } });
  g.handle(st.l2[0], st.l2[1], { color: 'orange', snap: 0.5, label: 'Your line, right end', onDrag: function (x, y) { st.l2 = [x, y]; draw(); } });
  var yours = sse(st.pts, um, ub), best = sse(st.pts, S.m, S.b);
  if (yours <= best * 1.1 + 1e-9) st.seen.close = true;
  if (S.r > 0.97) st.seen.r97 = true; if (S.r < 0) st.seen.neg = true; if (Math.abs(S.r) < 0.2) st.seen.zero = true;
  read.innerHTML = '<span class="c-orange">Your line: ' + L.V('y') + ' = ' + L.terms([[L.round(um, 2), 'x'], [L.round(ub, 1), '']], { frac: false }) + '</span>' +
    (st.showFit ? '<br><span class="c-green">Best fit: ' + L.V('y') + ' = ' + L.terms([[L.round(S.m, 2), 'x'], [L.round(S.b, 1), '']], { frac: false }) + '</span>' : '');
  var strength = Math.abs(S.r) > 0.8 ? 'strong' : Math.abs(S.r) > 0.5 ? 'moderate' : Math.abs(S.r) > 0.2 ? 'weak' : 'no clear';
  info.innerHTML = '<dt>Correlation ' + L.V('r') + '</dt><dd>' + L.num(S.r, 3) + ' (' + strength + (Math.abs(S.r) > 0.2 ? (S.r > 0 ? ' positive' : ' negative') : '') + ')</dd>' +
    '<dt>Your squared error</dt><dd>' + L.num(yours, 0) + '</dd>' + (st.showFit ? '<dt>Best squared error</dt><dd>' + L.num(best, 0) + '</dd>' : '');
  ch.update();
});
draw();
