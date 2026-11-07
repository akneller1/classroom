/* Dot plot of whole-number data from 0 to 20. Each dot can be dragged (or moved with the arrow keys).
   The mean is drawn as the balance point under the line; the median as a dashed line. */
var START = [5, 6, 6, 7, 8, 8, 9, 10, 13];
var st = { d: START.slice(), dist: false, seen: {} };
function sorted() { return st.d.slice().sort(function (a, b) { return a - b; }); }
function median(a) { var n = a.length, m = Math.floor(n / 2); return n % 2 ? a[m] : (a[m - 1] + a[m]) / 2; }
function stats() {
  var a = sorted(), n = a.length, sum = a.reduce(function (s, x) { return s + x; }, 0), mean = sum / n;
  var half = Math.floor(n / 2), lo = a.slice(0, half), hi = a.slice(n % 2 ? half + 1 : half);
  var dev = a.reduce(function (s, x) { return s + Math.abs(x - mean); }, 0);
  var left = a.reduce(function (s, x) { return s + (x < mean ? mean - x : 0); }, 0);
  return { n: n, sum: sum, mean: mean, med: median(a), q1: median(lo), q3: median(hi), range: a[n - 1] - a[0], mad: dev / n, left: left };
}
function meanTxt(S) { var f = L.toFrac(S.mean, S.n); return f && f[1] !== 1 ? L.frac(S.sum, S.n) + ' ≈ ' + L.num(S.mean, 2) : L.num(S.mean, 2); }
function madTxt(S) { var tot = S.mad * S.n; return Math.abs(S.mad - Math.round(S.mad)) < 1e-9 ? L.num(S.mad) : '≈ ' + L.num(S.mad, 2); }

var W = 640, H = 300, X0 = 30, X1 = 610, YA = 220, R = 11, GAP = 23;
function X(v) { return X0 + v / 20 * (X1 - X0); }
var svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Dot plot' }, P.stage);
var keeper = L.focusKeeper(svg);
L.h('div', { class: 'legend', style: 'margin:6px' }, P.stage, '<span><i style="background:var(--purple)"></i>mean (balance point ▲)</span><span><i style="background:var(--green)"></i>median (middle value)</span><span><i style="background:var(--orange)"></i>distance from the mean</span>');
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var row = L.h('div', { class: 'btn-row' }, P.panel);
L.button(row, '+ Add a value', function () { if (st.d.length < 20) { st.d.push(10); draw(); } }, true);
L.button(row, '− Remove a value', function () { if (st.d.length > 3) { st.d.pop(); draw(); } }, true);
var bDist = L.button(row, 'Show distances from the mean', function () { st.dist = !st.dist; bDist.textContent = st.dist ? 'Hide distances' : 'Show distances from the mean'; draw(); }, true);
L.reset(row, function () { st.d = START.slice(); draw(); });
L.h('p', { class: 'sub' }, P.panel, 'Drag a dot left or right, or click it and use the arrow keys. New values start at 10.');
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Predict, then test: drag one value far to the right to make an outlier. Which moves more, the mean or the median?', check: function () { return st.seen.outlier; } },
  { text: 'Make the mean exactly 10 without any value at 10.', check: function () { return st.seen.mean10; } },
  { text: 'Show the distances from the mean and make the <b>left</b> total at least 15. What is the right total?', check: function () { return st.seen.left15; } },
  { text: 'Make the spread bigger: get the MAD above 4 while the mean stays exactly 8.', check: function () { return st.seen.mad4; } },
  { text: 'Make the median 12 while the mean is less than 10. What does the dot plot look like?', check: function () { return st.seen.skew; } }
]);
L.notice(P.below, '<p><b>The mean is the balance point.</b> The total distance of the values below the mean always equals the total distance of the values above it, so the dot plot would balance on the ▲.</p>' +
  '<p><b>The median is the middle value</b> when the data are in order. It only cares about order, so moving one value far away changes the mean a lot but the median little or not at all.</p>' +
  '<p>The range, interquartile range (IQR) and mean absolute deviation (MAD) measure <b>spread</b>. MAD is the average distance from the mean. Data can have the same mean but very different spreads.</p>');

var draw = L.scheduler(function () {
  var S = stats();
  keeper.save(); svg.innerHTML = '';
  /* axis */
  L.s('line', { x1: X0 - 8, x2: X1 + 8, y1: YA, y2: YA, stroke: 'var(--ink)', 'stroke-width': 3 }, svg);
  for (var v = 0; v <= 20; v++) {
    L.s('line', { x1: X(v), x2: X(v), y1: YA - 6, y2: YA + 6, stroke: 'var(--ink)', 'stroke-width': v % 5 ? 1.5 : 2.5 }, svg);
    var t = L.s('text', { x: X(v), y: YA + 24, 'text-anchor': 'middle', class: 'g-tick', 'font-size': 13 }, svg); t.textContent = v;
  }
  /* stacked positions */
  var count = {}, pos = st.d.map(function (val) { count[val] = (count[val] || 0) + 1; return count[val] - 1; });
  var tall = Math.max.apply(null, Object.keys(count).map(function (k) { return count[k]; }));
  GAP = Math.min(23, (YA - R - 40) / Math.max(1, tall - 1)); var rr = Math.min(R, GAP / 2 + 1);
  /* distances from mean */
  if (st.dist) st.d.forEach(function (val, i) {
    var y = YA - R - 4 - pos[i] * GAP;
    if (Math.abs(val - S.mean) > 1e-9) L.s('line', { x1: X(val), x2: X(S.mean), y1: y, y2: y, stroke: 'var(--orange)', 'stroke-width': 4, opacity: 0.8 }, svg);
  });
  /* median */
  L.s('line', { x1: X(S.med), x2: X(S.med), y1: 24, y2: YA, stroke: 'var(--green)', 'stroke-width': 3, 'stroke-dasharray': '8 6' }, svg);
  var mt = L.s('text', { x: X(S.med), y: 18, 'text-anchor': 'middle', class: 'g-label', fill: 'var(--green)', 'font-size': 14 }, svg); mt.textContent = 'median ' + L.num(S.med, 2);
  /* dots */
  st.d.forEach(function (val, i) {
    var cy = YA - R - 4 - pos[i] * GAP;
    var c = L.s('circle', { cx: X(val), cy: cy, r: rr, fill: 'var(--blue)', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    L.drag(c, { svg: svg, label: 'Data value ' + (i + 1), valueText: String(val),
      onMove: function (x) { st.d[i] = Math.max(0, Math.min(20, Math.round((x - X0) / (X1 - X0) * 20))); draw(); },
      onKey: function (dx) { if (!dx) return; st.d[i] = Math.max(0, Math.min(20, st.d[i] + dx)); draw(); } });
  });
  /* fulcrum */
  var fx = X(S.mean);
  L.s('path', { d: 'M' + fx + ' ' + (YA + 2) + ' l -14 26 h 28 z', fill: 'var(--purple)', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
  var ft = L.s('text', { x: fx, y: YA + 46, 'text-anchor': 'middle', class: 'g-label', fill: 'var(--purple)', 'font-size': 14 }, svg); ft.textContent = 'mean ' + L.num(S.mean, 2);
  keeper.restore();

  read.innerHTML = '<span class="c-purple">mean = ' + L.frac('sum', 'count') + ' = ' + L.frac(String(S.sum), String(S.n)) + (S.sum % S.n ? ' ≈ ' + L.num(S.mean, 2) : ' = ' + L.num(S.mean)) + '</span>' +
    '<div style="margin-top:4px" class="c-green">median = ' + L.num(S.med, 2) + '</div>';
  info.innerHTML = '<dt>Number of values</dt><dd>' + S.n + '</dd><dt>Range</dt><dd>' + S.range + '</dd>' +
    '<dt>Q1, Q3</dt><dd>' + L.num(S.q1, 2) + ', ' + L.num(S.q3, 2) + '</dd><dt>IQR</dt><dd>' + L.num(S.q3 - S.q1, 2) + '</dd>' +
    '<dt>MAD</dt><dd>' + madTxt(S) + '</dd>' +
    (st.dist ? '<dt class="c-orange">Left of mean</dt><dd>' + L.num(S.left, 2) + '</dd><dt class="c-orange">Right of mean</dt><dd>' + L.num(S.left, 2) + '</dd>' : '');
  var gap = Math.abs(S.mean - S.med);
  fb.set(gap < 0.05 ? 'The mean and median are (almost) the same: the data are balanced around the middle.' :
    'The mean is ' + (S.mean > S.med ? 'above' : 'below') + ' the median by ' + L.num(gap, 2) + '. Values far out on the ' + (S.mean > S.med ? 'right' : 'left') + ' pull the mean toward them.', '');

  var a = sorted();
  if (a[a.length - 1] - a[a.length - 2] >= 5 && S.mean - S.med >= 0.5) st.seen.outlier = true;
  if (Math.abs(S.mean - 10) < 1e-9 && st.d.indexOf(10) < 0) st.seen.mean10 = true;
  if (st.dist && S.left >= 15 - 1e-9) st.seen.left15 = true;
  if (S.mad > 4 && Math.abs(S.mean - 8) < 1e-9) st.seen.mad4 = true;
  if (Math.abs(S.med - 12) < 1e-9 && S.mean < 10) st.seen.skew = true;
  ch.update();
});
draw();
