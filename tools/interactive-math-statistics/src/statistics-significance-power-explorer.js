/* One-proportion z test, H0: p = p0, using the normal approximation (stated on screen).
   p-value tab: z = (p̂ − p0)/SE0 with SE0 = √(p0(1 − p0)/n); the p-value is the shaded tail area under the null model.
   Errors & power tab: rejection region from α; Type I = α (area under the null model in the region);
   Type II = β (area under the true-p model outside the region); power = 1 − β. */
var S = L.stats;
var st = { tab: 'p', p0: 0.5, alt: 'gt', n: 100, x: 56, alpha: 0.05, pa: 0.6, runs: {}, pv: {}, seen: {} };
function se0() { return Math.sqrt(st.p0 * (1 - st.p0) / st.n); }
function sea() { return Math.sqrt(st.pa * (1 - st.pa) / st.n); }
function phat() { return st.x / st.n; }
function zstat() { return (phat() - st.p0) / se0(); }
function pval() { var z = zstat(); return st.alt === 'gt' ? 1 - S.normCdf(z) : st.alt === 'lt' ? S.normCdf(z) : 2 * Math.min(S.normCdf(z), 1 - S.normCdf(z)); }
function crit() { /* rejection region in p̂ units */
  var s = se0();
  if (st.alt === 'gt') return { hi: st.p0 + S.invNorm(1 - st.alpha) * s };
  if (st.alt === 'lt') return { lo: st.p0 - S.invNorm(1 - st.alpha) * s };
  var z = S.invNorm(1 - st.alpha / 2); return { lo: st.p0 - z * s, hi: st.p0 + z * s };
}
function power() { var c = crit(), s = sea(), pw = 0; if (c.hi != null) pw += 1 - S.normCdf((c.hi - st.pa) / s); if (c.lo != null) pw += S.normCdf((c.lo - st.pa) / s); return pw; }
var ALT = { gt: 'p &gt; ', lt: 'p &lt; ', ne: 'p ≠ ' };

var tabs = L.tabs(P.stage, [{ id: 'p', label: 'p-value' }, { id: 'power', label: 'Errors & power' }], function (id) { st.tab = id; build(); draw(); });
var GO = { xmin: 0, xmax: 1, ymin: 0, ymax: 1, width: 640, height: 400, noYAxis: true, yfmt: function () { return ''; }, label: 'Sampling distribution of p̂' };
var g = L.graph(P.stage, GO);
var legend = L.h('div', { class: 'legend', style: 'margin:6px' }, P.stage);
L.h('p', { class: 'sub', style: 'margin:0 6px' }, P.stage, 'Horizontal axis: sample proportion p̂. Curves are normal approximations (Large Counts must hold). Areas are probabilities.');
var hyp = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var ctrl = L.h('div', { style: 'display:grid;gap:12px' }, P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var fb = L.feedback(P.panel);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st.p0 = 0.5; st.alt = 'gt'; st.n = 100; st.x = 56; st.alpha = 0.05; st.pa = 0.6; build(); draw(); });
var ch = L.challenges(P.panel, [
  { text: 'For H<sub>0</sub>: p = 0.5 vs. H<sub>a</sub>: p &gt; 0.5 with n = 100, find a number of successes whose p-value is between 0.01 and 0.05.', check: function () { return st.seen.between; } },
  { text: 'Keep the same data and switch from a one-sided to a two-sided alternative. Predict, then check: what happens to the p-value?', check: function () { return st.seen.twoSided; } },
  { text: 'Keep p̂ = 0.55 (H<sub>0</sub>: p = 0.5, H<sub>a</sub>: p &gt; 0.5, α = 0.05). Increase n until a result that was <b>not</b> significant becomes significant.', check: function () { return st.seen.bigN; } },
  { text: 'In Errors & power, with p<sub>0</sub> = 0.5, H<sub>a</sub>: p &gt; 0.5, α = 0.05 and true p = 0.6, find the smallest n (on the slider) with power of at least 0.80.', check: function () { return st.seen.power80; } },
  { text: 'Change only α from 0.05 to 0.01. What happens to the probability of a Type II error?', check: function () { return st.seen.alphaBeta; } },
  { text: 'Set the true p equal to p<sub>0</sub>. What does “power” equal now? Explain why.', check: function () { return st.seen.nullTrue; } }
]);
L.notice(P.below, '<p><b>A p-value is the probability, assuming H<sub>0</sub> is true, of getting a sample result at least as extreme as the one observed</b> (in the direction of H<sub>a</sub>). It is <b>not</b> the probability that H<sub>0</sub> is true. A two-sided p-value counts both tails.</p>' +
  '<p>Small p-values are convincing evidence against H<sub>0</sub>. If the p-value is not small, we <b>fail to reject</b> H<sub>0</sub>; that is not evidence that H<sub>0</sub> is true. The same p̂ is more convincing with a larger n, because the null distribution is narrower.</p>' +
  '<p>Type I error: rejecting a true H<sub>0</sub> (probability α). Type II error: failing to reject a false H<sub>0</sub> (probability β). Power = 1 − β grows with n, with α and with the distance between the true p and p<sub>0</sub>. Lowering α makes Type II errors more likely.</p>');
function slider(id, label, min, max, step, val, color, fmt, on) { return L.slider(ctrl, { id: id, label: label, min: min, max: max, step: step, value: val, color: color, format: fmt, onInput: on }); }
function build() {
  ctrl.innerHTML = '';
  slider('null-p0', 'Null value p₀', 0.1, 0.9, 0.05, st.p0, 'ink', function (v) { return L.num(v, 2); }, function (v) { st.p0 = v; draw(); });
  L.chips(ctrl, { label: 'Alternative hypothesis', value: st.alt, options: [{ value: 'gt', label: 'p > p₀' }, { value: 'lt', label: 'p < p₀' }, { value: 'ne', label: 'p ≠ p₀' }], onChange: function (v) { st.alt = v; draw(); } });
  L.chips(ctrl, { label: 'Significance level α', value: st.alpha, options: [0.01, 0.05, 0.1].map(function (a) { return { value: a, label: 'α = ' + a }; }), onChange: function (v) { st.alpha = v; draw(); } });
  var sx;
  slider('sample-size', 'Sample size n', 10, 1000, 10, st.n, 'purple', L.num, function (v) { var ph = phat(); st.n = v; st.x = Math.round(ph * v); if (sx) { sx.el.querySelector('input').max = v; sx.set(st.x, true); } draw(); });
  if (st.tab === 'p') sx = slider('successes', 'Successes in the sample', 0, st.n, 1, st.x, 'orange', L.num, function (v) { st.x = Math.min(v, st.n); draw(); });
  else slider('true-p', 'True proportion p (for power)', 0.05, 0.95, 0.01, st.pa, 'red', function (v) { return L.num(v, 2); }, function (v) { st.pa = v; draw(); });
}
function curve(mu, sd, color, dash) { g.fn(function (x) { return S.normPdf((x - mu) / sd) / sd; }, { color: color, width: 3, dash: dash || null, samples: 600 }); }
function shade(mu, sd, a, b, color, op) {
  var v = g.view; a = Math.max(a, v.xmin); b = Math.min(b, v.xmax); if (b <= a) return;
  var pts = [[a, 0]]; for (var i = 0; i <= 120; i++) { var x = a + (b - a) * i / 120; pts.push([x, S.normPdf((x - mu) / sd) / sd]); } pts.push([b, 0]);
  g.poly(pts, { fill: color, opacity: op || 0.45, stroke: 'none', width: 0 });
}
function f(x, d) { return x < 0.0001 && x > 0 ? '&lt; 0.0001' : L.num(x, d || 4); }
var draw = L.scheduler(function () {
  var s0 = se0(), c = crit(), z = zstat(), pv = pval(), lc = st.n * st.p0 >= 10 && st.n * (1 - st.p0) >= 10;
  var spread = Math.max(4.5 * s0, st.tab === 'power' ? Math.abs(st.pa - st.p0) + 4.5 * sea() : Math.abs(phat() - st.p0) + 2 * s0);
  var lo = Math.max(-0.02, st.p0 - spread), hi = Math.min(1.02, st.p0 + spread), top = S.normPdf(0) / Math.min(s0, st.tab === 'power' ? sea() : s0);
  L.setNiceView(g, GO, { xmin: lo, xmax: hi, ymin: -top * 0.06, ymax: top * 1.18 }, 0, 9); g.clear();
  hyp.innerHTML = 'H<sub>0</sub>: p = ' + L.num(st.p0, 2) + ' &nbsp; H<sub>a</sub>: ' + ALT[st.alt] + L.num(st.p0, 2) + '<div class="sub" style="margin-top:4px">α = ' + st.alpha + ', n = ' + st.n + '</div>';
  if (st.tab === 'p') {
    var ph = phat();
    if (st.alt === 'gt') shade(st.p0, s0, ph, 2, 'orange');
    else if (st.alt === 'lt') shade(st.p0, s0, -1, ph, 'orange');
    else { var d = Math.abs(ph - st.p0); shade(st.p0, s0, st.p0 + d, 2, 'orange'); shade(st.p0, s0, -1, st.p0 - d, 'orange'); }
    curve(st.p0, s0, 'blue');
    if (c.hi != null) g.line(c.hi, 0, c.hi, top * 1.05, { color: 'red', width: 2, dash: '4 5' });
    if (c.lo != null) g.line(c.lo, 0, c.lo, top * 1.05, { color: 'red', width: 2, dash: '4 5' });
    g.line(ph, 0, ph, top * 0.95, { color: 'purple', width: 4 }); g.text(ph, top * 0.97, 'p̂ = ' + L.num(ph, 3), { anchor: 'middle', dy: -4, color: 'purple', size: 13 });
    g.text(st.p0, top * 1.1, 'null model, centered at p₀', { anchor: 'middle', color: 'blue', size: 13 });
    legend.innerHTML = '<span><i style="background:var(--blue)"></i>null model (if H₀ is true)</span><span><i style="background:var(--orange)"></i>p-value area</span><span><i style="background:var(--red)"></i>cutoff(s) for α</span>';
    info.innerHTML = '<dt>p̂</dt><dd>' + L.frac(String(st.x), String(st.n)) + ' = ' + L.num(ph, 4) + '</dd><dt>SE (using p₀)</dt><dd>' + L.num(s0, 4) + '</dd><dt>z</dt><dd>' + L.frac('p̂ − p₀', 'SE') + ' = ' + L.num(z, 3) + '</dd><dt>p-value</dt><dd><b>' + f(pv) + '</b></dd>';
    var rej = pv <= st.alpha;
    fb.set((lc ? '' : '<b>Large Counts fails</b> (np₀ or n(1 − p₀) &lt; 10): this normal approximation is not reliable. ') +
      (rej ? 'p-value ' + f(pv) + ' ≤ α = ' + st.alpha + ': <b>reject H<sub>0</sub></b>. There is convincing evidence that ' + ALT[st.alt] + L.num(st.p0, 2) + '.'
           : 'p-value ' + f(pv) + ' &gt; α = ' + st.alpha + ': <b>fail to reject H<sub>0</sub></b>. There is not convincing evidence that ' + ALT[st.alt] + L.num(st.p0, 2) + ' (this does not show that H<sub>0</sub> is true).'), lc ? (rej ? 'good' : '') : 'warn');
    var dk = st.n + '/' + st.x + '/' + st.p0; st.pv[dk] = st.pv[dk] || {}; st.pv[dk][st.alt] = pv;
    if (st.pv[dk].ne != null && (st.pv[dk].gt != null || st.pv[dk].lt != null)) st.seen.twoSided = true;
    if (st.p0 === 0.5 && st.alt === 'gt' && st.n === 100 && pv > 0.01 && pv < 0.05) st.seen.between = true;
    if (st.p0 === 0.5 && st.alt === 'gt' && st.alpha === 0.05 && Math.abs(ph - 0.55) < 1e-9) { st.seen['p55' + (rej ? 'sig' : 'non')] = st.n; if (st.seen.p55sig && st.seen.p55non) st.seen.bigN = true; }
  } else {
    var sa = sea(), pw = power(), beta = 1 - pw;
    var L0 = c.lo != null ? c.lo : -1, H0 = c.hi != null ? c.hi : 2;
    if (Math.abs(st.pa - st.p0) > 1e-9) shade(st.pa, sa, L0, H0, 'orange', 0.35);
    if (c.hi != null) shade(st.pa, sa, c.hi, 2, 'green', 0.3);
    if (c.lo != null) shade(st.pa, sa, -1, c.lo, 'green', 0.3);
    if (c.hi != null) shade(st.p0, s0, c.hi, 2, 'red', 0.75);   // α drawn last so it stays visible on top of power
    if (c.lo != null) shade(st.p0, s0, -1, c.lo, 'red', 0.75);
    curve(st.p0, s0, 'blue'); curve(st.pa, sa, 'ink', '8 6');
    if (c.hi != null) g.line(c.hi, 0, c.hi, top * 1.05, { color: 'red', width: 2.5 });
    if (c.lo != null) g.line(c.lo, 0, c.lo, top * 1.05, { color: 'red', width: 2.5 });
    g.text(st.p0, S.normPdf(0) / s0, 'null p₀', { anchor: 'middle', dy: -8, color: 'blue', size: 13 }); g.text(st.pa, S.normPdf(0) / sa, 'true p', { anchor: 'middle', dy: -8, size: 13 });
    legend.innerHTML = '<span><i style="background:var(--red)"></i>α: Type I error (reject a true H₀)</span><span><i style="background:var(--orange)"></i>β: Type II error</span><span><i style="background:var(--green)"></i>power</span>';
    info.innerHTML = '<dt>Reject H₀ when p̂ is</dt><dd>' + (c.lo != null ? '≤ ' + L.num(c.lo, 4) : '') + (c.lo != null && c.hi != null ? ' or ' : '') + (c.hi != null ? '≥ ' + L.num(c.hi, 4) : '') + '</dd>' +
      '<dt>P(Type I error)</dt><dd>α = ' + st.alpha + '</dd><dt>P(Type II error)</dt><dd>β = ' + L.num(beta, 4) + '</dd><dt>Power</dt><dd><b>' + L.num(pw, 4) + '</b></dd>';
    fb.set(Math.abs(st.pa - st.p0) < 1e-9 ? 'The true p equals p₀, so H₀ is true: there is no Type II error to make, and “rejecting” happens with probability α = ' + st.alpha + '.' :
      'If the true p is ' + L.num(st.pa, 2) + ', this test rejects H₀ with probability ' + L.num(pw, 3) + (pw >= 0.8 ? ' (power ≥ 0.80).' : '. Increase n, increase α, or test a true p farther from p₀ to raise power.'), pw >= 0.8 && Math.abs(st.pa - st.p0) > 1e-9 ? 'good' : '');
    var key = [st.p0, st.alt, st.pa, st.n].join('/'); st.runs[key] = st.runs[key] || {}; st.runs[key][st.alpha] = beta;
    if (st.runs[key][0.05] != null && st.runs[key][0.01] != null) st.seen.alphaBeta = true;
    if (Math.abs(st.pa - st.p0) < 1e-9) st.seen.nullTrue = true;
    if (st.p0 === 0.5 && st.alt === 'gt' && st.alpha === 0.05 && Math.abs(st.pa - 0.6) < 1e-9 && pw >= 0.8) { var n0 = st.n; st.n = n0 - 10; var prev = n0 > 10 ? power() : 0; st.n = n0; if (prev < 0.8) st.seen.power80 = true; }
  }
  ch.update();
});
build(); draw();
