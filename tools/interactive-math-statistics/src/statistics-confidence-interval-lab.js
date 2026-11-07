/* Confidence intervals from repeated random samples.
   Proportion: p̂ ± z*·√(p̂(1 − p̂)/n).  Mean: x̄ ± t*·s/√n with df = n − 1 (or, for comparison, z*·s/√n).
   Mean populations: Normal(50, 10) or 40 + Exponential(mean 10), which also has μ = 50 and σ = 10. */
var S = L.stats, R = S.rng(S.seedFromURL());
var st = { mode: 'prop', p: 0.4, pop: 'normal', method: 't', n: 40, level: 95, ints: [], runs: {}, seen: {} };
var MU = 50, SIGMA = 10;
function truth() { return st.mode === 'prop' ? st.p : MU; }
function runKey() { return [st.mode, st.mode === 'prop' ? st.p : st.pop + '/' + st.method, st.n, st.level].join('|'); }
function star() { var a = 1 - (1 - st.level / 100) / 2; return st.mode === 'mean' && st.method === 't' ? S.invT(a, st.n - 1) : S.invNorm(a); }
function one() {
  var est, se, n = st.n, cs = star(), i;
  if (st.mode === 'prop') { var c = 0; for (i = 0; i < n; i++) if (R() < st.p) c++; est = c / n; se = Math.sqrt(est * (1 - est) / n); var it = { est: est, me: cs * se, c: c, se: se }; }
  else { var xs = []; for (i = 0; i < n; i++) xs.push(st.pop === 'normal' ? MU + SIGMA * S.randNormal(R) : 40 - 10 * Math.log(1 - R())); est = S.mean(xs); var s = S.sd(xs); se = s / Math.sqrt(n); it = { est: est, me: cs * se, s: s, se: se }; }
  it.lo = it.est - it.me; it.hi = it.est + it.me; it.hit = it.lo <= truth() && truth() <= it.hi; it.star = cs;
  return it;
}
function make(k) {
  for (var i = 0; i < k; i++) st.ints.push(one());
  var rk = runKey(), hits = st.ints.filter(function (x) { return x.hit; }).length;
  st.runs[rk] = { count: st.ints.length, hits: hits, me: S.mean(st.ints.map(function (x) { return x.me; })) };
  check(); draw();
}
function clearAll() { st.ints = []; draw(); }

var GO = { xmin: 0, xmax: 1, ymin: -2, ymax: 102, width: 640, height: 560, noYAxis: true, yfmt: function () { return ''; }, label: 'Confidence intervals, newest at the top' };
var g = L.graph(P.stage, GO);
L.h('div', { class: 'legend', style: 'margin:6px' }, P.stage, '<span><i style="background:var(--green)"></i>captures the true value (solid)</span><span><i style="background:var(--red)"></i>misses it (dashed, marked ✗)</span><span><i style="background:var(--ink)"></i>true value</span>');
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Each row is one random sample and its interval. Only the newest 100 are drawn; the counts include all of them.');
L.chips(P.panel, { label: 'Parameter', value: st.mode, options: [{ value: 'prop', label: 'Proportion p' }, { value: 'mean', label: 'Mean μ' }], onChange: function (v) { st.mode = v; st.n = v === 'prop' ? 40 : 10; build(); clearAll(); } });
var ctrl = L.h('div', { style: 'display:grid;gap:12px' }, P.panel);
var lv = L.chips(P.panel, { label: 'Confidence level', value: st.level, options: [80, 90, 95, 99].map(function (x) { return { value: x, label: x + '%' }; }), onChange: function (v) { st.level = v; clearAll(); } });
L.h('p', { class: 'lp-mini' }, P.panel, 'Changing a setting clears the intervals, so every count comes from one method.');
var row = L.h('div', { class: 'btn-row' }, P.panel);
L.button(row, 'Make 1 interval', function () { make(1); });
L.button(row, 'Make 20', function () { make(20); }, true);
L.button(row, 'Make 100', function () { make(100); }, true);
var row2 = L.h('div', { class: 'btn-row' }, P.panel);
L.button(row2, 'Clear intervals', clearAll, true);
L.reset(row2, function () { st.mode = 'prop'; st.p = 0.4; st.pop = 'normal'; st.method = 't'; st.n = 40; st.level = 95; lv.set(95, true); P.panel.querySelector('.chips button').click(); clearAll(); });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Make 100 or more 95% intervals. Predict first: about how many will capture the true value?', check: function () { return st.seen.hundred; } },
  { text: 'Keep n the same. Compare the average margin of error at 90% and at 99% (20+ intervals each). Why is there a trade-off?', check: function () { return st.seen.levels; } },
  { text: 'Cut the average margin of error about in half <b>without</b> changing the confidence level. How much did n have to grow?', check: function () { return st.seen.half; } },
  { text: 'Break the Large Counts condition for a proportion (np &lt; 10) and make 200+ 95% intervals. Does the capture rate stay near 95%?', check: function () { return st.seen.broken; } },
  { text: 'For a mean with n = 5, make 200+ 95% intervals using z* with s, then 200+ using t*. Which captures closer to 95%? Why?', check: function () { return st.seen.zt; } }
]);
L.notice(P.below, '<p><b>The confidence level describes the method, not one interval.</b> If we repeat the sampling many times, about 95% of the 95% intervals capture the true parameter. Any one interval either captures it or doesn’t; we can’t tell which.</p>' +
  '<p>Margin of error = critical value × standard error. A higher confidence level needs a larger critical value, so the interval is wider. The standard error shrinks like 1/√n, so to halve the margin of error you need about <b>4 times</b> the sample size.</p>' +
  '<p>The capture rate is only trustworthy when the conditions hold: random sampling, independence, and Large Counts (np̂ ≥ 10 and n(1 − p̂) ≥ 10) or a normal population / large n for means. With s instead of σ, use t* (df = n − 1); z* makes intervals too narrow for small n.</p>' +
  '<p>Simulated capture rates are estimates and vary from run to run.</p>');
function build() {
  ctrl.innerHTML = '';
  if (st.mode === 'prop') {
    L.slider(ctrl, { id: 'true-p', label: 'True proportion p (unknown in real life)', min: 0.05, max: 0.95, step: 0.05, value: st.p, color: 'red', format: function (v) { return L.num(v, 2); }, onInput: function (v) { st.p = v; clearAll(); } });
    L.slider(ctrl, { id: 'sample-size', label: 'Sample size n', min: 10, max: 400, step: 5, value: st.n, color: 'purple', format: L.num, onInput: function (v) { st.n = v; clearAll(); } });
  } else {
    L.chips(ctrl, { label: 'Population (μ = 50, σ = 10)', value: st.pop, options: [{ value: 'normal', label: 'Normal' }, { value: 'skew', label: 'Right-skewed' }], onChange: function (v) { st.pop = v; clearAll(); } });
    L.chips(ctrl, { label: 'Critical value', value: st.method, options: [{ value: 't', label: 't* (df = n − 1)' }, { value: 'z', label: 'z* with s' }], onChange: function (v) { st.method = v; clearAll(); } });
    L.slider(ctrl, { id: 'sample-size', label: 'Sample size n', min: 2, max: 100, value: st.n, color: 'purple', format: L.num, onInput: function (v) { st.n = v; clearAll(); } });
  }
}
function check() {
  var r = st.runs, k = runKey().split('|');
  if (st.level === 95 && st.ints.length >= 100) st.seen.hundred = true;
  Object.keys(r).forEach(function (o) {
    var a = o.split('|');
    if (a[0] !== k[0] || a[1] !== k[1] || r[o].count < 20 || st.ints.length < 20) return;
    if (a[2] === k[2] && ((a[3] === '90' && k[3] === '99') || (a[3] === '99' && k[3] === '90'))) st.seen.levels = true;
    if (a[3] === k[3] && (+k[2] === 4 * +a[2] || +a[2] === 4 * +k[2])) st.seen.half = true;
  });
  if (st.mode === 'prop' && st.level === 95 && (st.n * st.p < 10 || st.n * (1 - st.p) < 10) && st.ints.length >= 200) st.seen.broken = true;
  var zr = r['mean|' + st.pop + '/z|5|95'], tr = r['mean|' + st.pop + '/t|5|95'];
  if (zr && tr && zr.count >= 200 && tr.count >= 200) st.seen.zt = true;
}
var draw = L.scheduler(function () {
  var T = truth(), prop = st.mode === 'prop';
  L.setNiceView(g, GO, prop ? { xmin: -0.02, xmax: 1.02 } : { xmin: 20, xmax: 80 }, 0, 10); g.clear();
  g.line(T, -2, T, 102, { color: 'ink', width: 3 });
  g.text(T, 101, (prop ? 'p = ' : 'μ = ') + L.num(T, 2), { dx: 6, dy: 4, size: 13 });
  var show = st.ints.slice(-100), v = g.view;
  show.forEach(function (it, i) {
    var y = 100 - (show.length - 1 - i) - 0.5, lo = Math.max(v.xmin, it.lo), hi = Math.min(v.xmax, it.hi);
    g.line(lo, y, hi, y, { color: it.hit ? 'green' : 'red', width: it.hit ? 2.5 : 2.5, dash: it.hit ? null : '5 3' });
    g.dot(it.est, y, { color: it.hit ? 'green' : 'red', r: 2.6 });
    if (!it.hit) g.text(Math.min(hi, v.xmax), y, '✗', { dx: 4, dy: 4, size: 11, color: 'red' });
  });
  if (!show.length) g.text((v.xmin + v.xmax) / 2, 50, 'Make some intervals', { anchor: 'middle', size: 15, color: 'ink-soft' });
  var last = st.ints[st.ints.length - 1], n = st.n, a = 1 - (1 - st.level / 100) / 2;
  var critName = prop || st.method === 'z' ? 'z*' : 't*';
  if (last) read.innerHTML = (prop ? 'p̂ = ' + L.frac(String(last.c), String(n)) + ' = ' + L.num(last.est, 3) : 'x̄ = ' + L.num(last.est, 2) + ', s = ' + L.num(last.s, 2)) +
    '<div class="sub" style="margin-top:4px">' + critName + ' = ' + L.num(last.star, 3) + (critName === 't*' ? ' (df = ' + (n - 1) + ')' : '') + ' · SE = ' + L.num(last.se, 4) + ' · ME = ' + L.num(last.me, 4) + '</div>' +
    '<div class="sub">interval: (' + L.num(last.lo, prop ? 3 : 2) + ', ' + L.num(last.hi, prop ? 3 : 2) + ') ' + (last.hit ? '<b class="c-green">captures</b>' : '<b class="c-red">misses</b>') + ' the true value</div>';
  else read.innerHTML = st.level + '% intervals: estimate ± ' + critName + ' × SE<div class="sub" style="margin-top:4px">' + critName + ' = ' + L.num(star(), 3) + (critName === 't*' ? ' with df = ' + (n - 1) : '') + '</div>';
  var hits = st.ints.filter(function (x) { return x.hit; }).length;
  info.innerHTML = '<dt>Intervals made</dt><dd>' + st.ints.length.toLocaleString() + '</dd><dt>Captured</dt><dd>' + hits.toLocaleString() + (st.ints.length ? ' (' + L.num(100 * hits / st.ints.length, 1) + '%)' : '') + '</dd>' +
    '<dt>Average margin of error</dt><dd>' + (st.ints.length ? L.num(S.mean(st.ints.map(function (x) { return x.me; })), prop ? 4 : 3) : '—') + '</dd>';
  if (prop) { var ok = n * st.p >= 10 && n * (1 - st.p) >= 10; fb.set('Large Counts for this p and n: np = ' + L.num(n * st.p, 1) + ', n(1 − p) = ' + L.num(n * (1 - st.p), 1) + (ok ? '. Both ≥ 10.' : '. Not met: the capture rate may fall short of ' + st.level + '%.') + (last && (last.c < 10 || n - last.c < 10) ? ' (Latest sample: np̂ or n(1 − p̂) is below 10.)' : ''), ok ? 'good' : 'warn'); }
  else fb.set(st.method === 'z' ? 'Using z* with s ignores the extra uncertainty from estimating σ. Compare the capture rate with t*.' : (st.pop === 'skew' && n < 30 ? 'Skewed population with n &lt; 30: the t procedure’s capture rate may be off.' : 't* uses df = n − 1 and is wider than z* for small n.'), st.method === 'z' || (st.pop === 'skew' && n < 30) ? 'warn' : '');
  ch.update();
});
build(); draw();
