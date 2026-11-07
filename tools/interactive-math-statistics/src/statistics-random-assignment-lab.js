/* Experiment: does a study app raise quiz scores? 20 volunteers with fixed GPAs (the lurking variable).
   Each run: quiz score = 50 + 10·GPA + random noise (SD 3) + δ if the student used the app.
   Assignment: random (10 of 20), randomized pairs (sort by GPA, flip a coin within each pair), or let students choose
   (higher-GPA students are more likely to pick the app: weights e^{3(GPA − 3)}).
   Randomization test: keep one experiment's scores, reshuffle the group labels many times (as if the app did nothing),
   and find the share of shuffles with a difference at least as large as the observed one (one-sided: the app helps). */
var S = L.stats, R = S.rng(S.seedFromURL());
var GPA = [2.06, 2.12, 2.07, 2.32, 2.5, 2.55, 2.63, 2.8, 2.9, 3.05, 3.14, 3.07, 3.25, 3.25, 3.59, 3.47, 3.64, 3.85, 3.78, 4.0];
var NAMES = ['Ava', 'Ben', 'Cy', 'Dee', 'Eli', 'Fay', 'Gus', 'Hal', 'Ivy', 'Jo', 'Kai', 'Lu', 'Max', 'Nia', 'Oz', 'Pia', 'Quin', 'Rae', 'Sol', 'Tess'];
var METHODS = { random: 'Random assignment', pairs: 'Randomized pairs (matched on GPA)', choose: 'Students choose' };
var st = { tab: 'assign', m: 'random', d: 0, last: null, diffs: [], runs: {}, exp: null, nulls: [], seen: {} };
function assign(method) {
  var m = method || st.m, T = []; for (var i = 0; i < 20; i++) T.push(false);
  if (m === 'random') { var idx = []; for (i = 0; i < 20; i++) idx.push(i); for (i = 0; i < 10; i++) { var j = i + Math.floor(R() * (20 - i)); var t = idx[i]; idx[i] = idx[j]; idx[j] = t; T[idx[i]] = true; } }
  else if (m === 'pairs') { var ord = GPA.map(function (g, k) { return k; }).sort(function (a, b) { return GPA[a] - GPA[b] || a - b; }); for (i = 0; i < 10; i++) T[ord[2 * i + (R() < 0.5 ? 0 : 1)]] = true; }
  else { var left = GPA.map(function (g, k) { return k; }); for (var c = 0; c < 10; c++) { var w = left.map(function (k) { return Math.exp(3 * (GPA[k] - 3)); }), tot = w.reduce(function (a, b) { return a + b; }, 0), r = R() * tot, p = 0; while (r >= w[p] && p < w.length - 1) { r -= w[p]; p++; } T[left[p]] = true; left.splice(p, 1); } }
  return T;
}
function outcomes(T) { return GPA.map(function (g, i) { return Math.round((50 + 10 * g + 3 * S.randNormal(R) + (T[i] ? st.d : 0)) * 10) / 10; }); }
function diff(y, T) { var a = 0, b = 0; for (var i = 0; i < 20; i++) if (T[i]) a += y[i]; else b += y[i]; return a / 10 - b / 10; }
function gdiff(T) { return diff(GPA, T); }
function runAssign(k) {
  for (var t = 0; t < k; t++) { var T = assign(), y = outcomes(T); st.last = { T: T, y: y, d: diff(y, T), g: gdiff(T) }; st.diffs.push(st.last.d);
    if (st.m === 'random' && k === 1 && st.last.g >= 0.3 - 1e-9) st.seen.unbalanced = true; }
  var key = st.m + '|' + st.d; st.runs[key] = { m: st.m, d: st.d, count: st.diffs.length, center: S.mean(st.diffs), sd: st.diffs.length > 1 ? S.sd(st.diffs) : 0 };
  draw();
}
function newExperiment() { var T = assign('random'); var y = outcomes(T); st.exp = { T: T, y: y, d: diff(y, T), delta: st.d }; st.nulls = []; draw(); }
function shuffle(k) {
  if (!st.exp) newExperiment();
  var y = st.exp.y;
  for (var t = 0; t < k; t++) { var idx = []; for (var i = 0; i < 20; i++) idx.push(i); var T = []; for (i = 0; i < 20; i++) T.push(false);
    for (i = 0; i < 10; i++) { var j = i + Math.floor(R() * (20 - i)); var s = idx[i]; idx[i] = idx[j]; idx[j] = s; T[idx[i]] = true; } st.nulls.push(diff(y, T)); }
  draw();
}
function pval() { if (!st.nulls.length) return null; var c = 0; st.nulls.forEach(function (x) { if (x >= st.exp.d - 1e-9) c++; }); return c / st.nulls.length; }

var tabs = L.tabs(P.stage, [{ id: 'assign', label: 'Assign the treatment' }, { id: 'test', label: 'Randomization test' }], function (id) { st.tab = id; build(); draw(); });
var W = 640, svg = L.s('svg', { viewBox: '0 0 640 170', role: 'img', 'aria-label': 'The 20 volunteers and their groups' }, P.stage);
var cap = L.h('p', { class: 'sub', style: 'margin:8px 6px 0;font-weight:700' }, P.stage, '');
var GO = { xmin: -15, xmax: 20, ymin: 0, ymax: 1, width: 640, height: 260, noYAxis: true, yfmt: function () { return ''; }, xstep: 1, xlabelStep: 5, label: 'Distribution of differences in mean score' };
var g = L.graph(P.stage, GO);
L.h('div', { class: 'legend', style: 'margin:6px' }, P.stage, '<span>■ orange square = uses the app (treatment)</span><span>● blue circle = no app (control)</span><span>darker = higher GPA</span>');
var ctrl = L.h('div', { style: 'display:grid;gap:12px' }, P.panel);
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var tbl = L.table(P.panel);
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Set the true effect to 0 and let students choose (200+ repetitions). Does the app <b>look</b> effective? What explains it?', check: function () { return st.seen.fake; } },
  { text: 'Now use random assignment with a true effect of 0 (200+ repetitions). Where are the differences centered?', check: function () { return st.seen.fair; } },
  { text: 'One random assignment can still be lopsided. Assign once at a time until the app group’s mean GPA is at least 0.3 higher.', check: function () { return st.seen.unbalanced; } },
  { text: 'At the same true effect, compare random assignment with randomized pairs (200+ each). Which estimates vary less? Why?', check: function () { return st.seen.pairs; } },
  { text: 'Randomization test with a true effect of 0: run one experiment and 1,000+ re-randomizations. Predict first: is the p-value small?', check: function () { return st.seen.null; } },
  { text: 'Find a true effect for which one experiment gives a p-value below 0.05 (1,000+ re-randomizations). Does every experiment at that effect?', check: function () { return st.seen.sig; } }
]);
L.notice(P.below, '<p><b>Random assignment balances lurking variables on average.</b> When students choose, the stronger students pick the app, so the groups differ before the experiment starts. The difference in scores mixes the app’s effect with GPA: the variables are <b>confounded</b>, and the app can look effective even when it does nothing.</p>' +
  '<p>Any single random assignment can still be unbalanced by chance; that chance variation is exactly what inference measures. Pairing similar students and randomizing within pairs (a matched-pairs design, a kind of blocking) removes much of that variation, so the estimates vary less.</p>' +
  '<p>A <b>randomization test</b> asks: if the app did nothing, how often would shuffling the labels give a difference at least this large? That share is the p-value. A small p-value is convincing evidence of an effect; with a true effect of 0, small p-values happen only about 5% of the time.</p>');
function build() {
  ctrl.innerHTML = '';
  L.slider(ctrl, { id: 'true-effect', label: 'True effect of the app δ (points)', min: 0, max: 12, step: 2, value: st.d, color: 'orange', format: function (v) { return '+' + v; }, onInput: function (v) { st.d = v; st.diffs = []; st.last = null; st.exp = null; st.nulls = []; draw(); } });
  if (st.tab === 'assign') {
    L.chips(ctrl, { label: 'How are students put in groups?', value: st.m, options: Object.keys(METHODS).map(function (k) { return { value: k, label: METHODS[k] }; }), onChange: function (v) { st.m = v; st.diffs = []; st.last = null; draw(); } });
    var row = L.h('div', { class: 'btn-row' }, ctrl);
    L.button(row, 'Assign once', function () { runAssign(1); }); L.button(row, 'Repeat 100 times', function () { runAssign(100); }, true);
    var row2 = L.h('div', { class: 'btn-row' }, ctrl); L.button(row2, 'Clear', function () { st.diffs = []; st.last = null; draw(); }, true);
    L.reset(row2, function () { st.d = 0; st.m = 'random'; st.diffs = []; st.last = null; st.runs = {}; build(); draw(); });
  } else {
    var r1 = L.h('div', { class: 'btn-row' }, ctrl);
    L.button(r1, 'Run a new experiment', newExperiment); L.button(r1, 'Re-randomize 1,000 times', function () { shuffle(1000); }, true);
    var r2 = L.h('div', { class: 'btn-row' }, ctrl); L.reset(r2, function () { st.d = 0; st.exp = null; st.nulls = []; build(); draw(); });
    L.h('p', { class: 'lp-mini' }, ctrl, 'The experiment uses random assignment. Re-randomizing keeps each student’s score and only shuffles the group labels.');
  }
}
function people(T, y) {
  svg.innerHTML = '';
  for (var i = 0; i < 20; i++) {
    var col = i % 10, row = Math.floor(i / 10), cx = 36 + col * 63, cy = 42 + row * 78, shade = 0.25 + 0.75 * (GPA[i] - 2) / 2, tr = T && T[i];
    var fillc = T ? (tr ? 'var(--orange)' : 'var(--blue)') : 'var(--ghost)';
    if (tr) L.s('rect', { x: cx - 15, y: cy - 15, width: 30, height: 30, rx: 3, fill: fillc, 'fill-opacity': shade, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    else L.s('circle', { cx: cx, cy: cy, r: 16, fill: fillc, 'fill-opacity': shade, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    var t1 = L.s('text', { x: cx, y: cy + 30, 'text-anchor': 'middle', class: 'g-tick', 'font-size': 12 }, svg); t1.textContent = NAMES[i] + ' ' + GPA[i].toFixed(2);
    if (y) { var t2 = L.s('text', { x: cx, y: cy + 4, 'text-anchor': 'middle', 'font-size': 12, 'font-weight': 800, fill: '#ffffff', stroke: '#14173a', 'stroke-width': 3, 'paint-order': 'stroke', 'font-family': 'var(--display)' }, svg); t2.textContent = Math.round(y[i]); }
  }
}
function hist(vals, color, mark, tail) {
  var lo = -15, hi = 20, bw = 0.5, cnt = {}, top = 1;
  vals.forEach(function (v) { var k = Math.floor(v / bw); cnt[k] = (cnt[k] || 0) + 1; top = Math.max(top, cnt[k]); });
  g.setView({ xmin: lo, xmax: hi, ymin: -top * 0.08, ymax: top * 1.2 }); g.clear();
  Object.keys(cnt).forEach(function (k) { var x = k * bw, isTail = tail != null && x + bw / 2 >= tail; g.rect(x, 0, bw, cnt[k], { fill: isTail ? 'red' : color, opacity: isTail ? 0.75 : 0.5, stroke: 'ink', width: 0.6 }); });
  g.line(0, 0, 0, top * 1.15, { color: 'ink', width: 1.5, dash: '3 4' });
  if (mark != null) { g.line(mark, 0, mark, top * 1.15, { color: 'purple', width: 3 }); g.text(mark, top * 1.1, 'observed ' + (mark >= 0 ? '+' : '−') + L.num(Math.abs(mark), 2), { dx: 6, color: 'purple', size: 13 }); }
  return top;
}
var draw = L.scheduler(function () {
  if (st.tab === 'assign') {
    people(st.last ? st.last.T : null, st.last ? st.last.y : null);
    cap.textContent = 'Difference in mean score (app − no app) from every assignment so far';
    var top = hist(st.diffs, 'orange', null, null);
    if (st.diffs.length) { g.line(st.d, 0, st.d, top * 1.15, { color: 'green', width: 3 }); g.text(st.d, top * 1.1, 'true effect +' + st.d, { dx: 6, color: 'green', size: 13 }); }
    read.innerHTML = st.last ? 'Latest: app − no app = <b>' + (st.last.d >= 0 ? '+' : '−') + L.num(Math.abs(st.last.d), 2) + '</b> points<div class="sub" style="margin-top:4px">mean GPA, app − no app: ' + (st.last.g >= 0 ? '+' : '−') + L.num(Math.abs(st.last.g), 2) + '</div>' : METHODS[st.m] + ' · true effect +' + st.d;
    var rows = Object.keys(st.runs).map(function (k) { var x = st.runs[k]; return [METHODS[x.m].split(' (')[0], '+' + x.d, x.count, (x.center >= 0 ? '+' : '−') + L.num(Math.abs(x.center), 2), x.count > 1 ? L.num(x.sd, 2) : '—']; });
    tbl.set(['Assignment', 'True effect', 'Runs', 'Center of differences', 'SD'], rows.length ? rows : [['—', '', '', '', '']]);
    var cur = st.runs[st.m + '|' + st.d];
    fb.set(!cur || cur.count < 100 ? 'Repeat 100+ times to see where this method’s differences center and how much they vary.' :
      Math.abs(cur.center - st.d) > 1.5 ? 'The differences center at ' + L.num(cur.center, 1) + ', not at the true effect +' + st.d + ': GPA is <b>confounded</b> with using the app.' :
      'The differences center near the true effect +' + st.d + ' (unbiased). SD = ' + L.num(cur.sd, 2) + ' points.', !cur || cur.count < 100 ? '' : Math.abs(cur.center - st.d) > 1.5 ? 'bad' : 'good');
    var ok = function (m, d) { var x = st.runs[m + '|' + d]; return x && x.count >= 200; };
    if (ok('choose', 0)) st.seen.fake = true;
    if (ok('random', 0)) st.seen.fair = true;
    if (ok('random', st.d) && ok('pairs', st.d)) st.seen.pairs = true;
  } else {
    var e = st.exp; people(e ? e.T : null, e ? e.y : null);
    cap.textContent = 'Differences from re-randomizing the labels (as if the app did nothing)';
    hist(st.nulls, 'blue', e ? e.d : null, e && st.nulls.length ? e.d : null);
    var p = pval();
    read.innerHTML = e ? 'Observed difference (app − no app): <b>' + (e.d >= 0 ? '+' : '−') + L.num(Math.abs(e.d), 2) + '</b><div class="sub" style="margin-top:4px">' + (p == null ? 'Re-randomize to build the null distribution.' : st.nulls.length.toLocaleString() + ' shuffles: ' + Math.round(p * st.nulls.length) + ' at least as large → p-value ≈ ' + L.num(p, 3)) + '</div>' : 'Run an experiment first.';
    tbl.set(['', 'Value'], [['H₀', 'the app has no effect (δ = 0)'], ['Hₐ', 'the app raises scores (δ > 0)'], ['True effect used to simulate', '+' + st.d + ' (unknown in real life)']]);
    fb.set(p == null ? 'The p-value is the share of shuffled differences at least as large as the observed one.' : p < 0.05 ? 'p-value ≈ ' + L.num(p, 3) + ' &lt; 0.05: a difference this large rarely happens by chance alone. Convincing evidence that the app raises scores.' : 'p-value ≈ ' + L.num(p, 3) + ': a difference this large happens often by chance alone. Not convincing evidence of an effect (that does not prove there is none).', p == null ? '' : p < 0.05 ? 'good' : '');
    if (e && st.nulls.length >= 1000 && e.delta === 0) st.seen.null = true;
    if (e && st.nulls.length >= 1000 && p < 0.05) st.seen.sig = true;
  }
  ch.update();
});
build(); draw();
