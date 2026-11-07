/* Approach x = a from the left and the right. Each case knows its exact one-sided limits; the table values are
   computed from the formula. The value f(a) is set separately, so the limit and the value can be compared. */
var HS = [1, 0.5, 0.1, 0.01, 0.001];
var CASES = {
  hole: { label: 'Hole', a: 1, f: function (x) { return (x * x - 1) / (x - 1); }, tex: L.frac(L.V('x') + '² − 1', L.V('x') + ' − 1'), Lm: 2, Lp: 2, val: null, canSet: true, view: [-2, 4, -1, 5] },
  moved: { label: 'Moved point', a: 2, f: function (x) { return x * x / 2 + 1; }, tex: L.frac(L.V('x') + '²', '2') + ' + 1 for ' + L.V('x') + ' ≠ 2', Lm: 3, Lp: 3, val: 5, canSet: true, view: [-1, 5, -1, 7] },
  jump: { label: 'Jump', a: 1, f: function (x) { return x < 1 ? x + 1 : x - 1; }, tex: L.V('x') + ' + 1 if ' + L.V('x') + ' &lt; 1; ' + L.V('x') + ' − 1 if ' + L.V('x') + ' ≥ 1', Lm: 2, Lp: 0, val: 0, canSet: false, split: true, view: [-2, 4, -2, 4] },
  asym: { label: 'Vertical asymptote', a: 2, f: function (x) { return 1 / ((x - 2) * (x - 2)); }, tex: L.frac('1', '(' + L.V('x') + ' − 2)²'), Lm: Infinity, Lp: Infinity, val: null, canSet: false, view: [-1, 5, -1, 10] },
  osc: { label: 'Oscillation', a: 0, f: function (x) { return Math.sin(1 / x); }, tex: 'sin(' + L.frac('1', L.V('x')) + ')', Lm: NaN, Lp: NaN, val: null, canSet: false, view: [-1, 1, -1.5, 1.5] },
  cont: { label: 'Continuous', a: 2, f: function (x) { return 0.5 * x * x - x + 1; }, tex: L.frac('1', '2') + L.V('x') + '² − ' + L.V('x') + ' + 1', Lm: 1, Lp: 1, val: 1, canSet: false, view: [-1, 5, -1, 5] }
};
var st = { c: 'hole', hi: 0, zoom: 0, reveal: false, defd: false, v: 3, vals: {}, seen: {} };
function C() { return CASES[st.c]; }
function h() { return HS[st.hi]; }
function valueAt() { var c = C(); if (c.canSet) return st.defd ? st.v : null; return c.val; }
var GO = { xmin: -2, xmax: 4, ymin: -1, ymax: 5, width: 600, height: 520, label: 'Graph near x = a' }, g = L.graph(P.stage, GO);
var cap = L.h('p', { class: 'sub', style: 'margin:4px 6px 0' }, P.stage);
L.chips(P.panel, { label: 'Function', value: st.c, options: Object.keys(CASES).map(function (k) { return { value: k, label: CASES[k].label }; }),
  onChange: function (v) { st.c = v; st.zoom = 0; st.reveal = false; st.defd = v === 'moved'; st.v = v === 'moved' ? 5 : 3; sv.set(st.v, true); dc.set(st.defd, true); bR.textContent = 'Reveal the limits'; build(); draw(); } });
var read = L.h('div', { class: 'readout small', 'aria-live': 'polite' }, P.panel);
var sh = L.slider(P.panel, { id: 'distance-h', label: 'How close: distance h from a', min: 0, max: 4, value: st.hi, color: 'orange', format: function (i) { return 'h = ' + HS[i]; }, onInput: function (i) { st.hi = i; draw(); } });
var setBox = L.h('div', { style: 'display:grid;gap:8px' }, P.panel);
var dc = L.chips(setBox, { label: 'The value f(a)', value: st.defd, options: [{ value: false, label: 'undefined' }, { value: true, label: 'defined as' }], onChange: function (v) { st.defd = v; draw(); } });
var sv = L.slider(setBox, { id: 'value-at-a', label: 'f(a) =', min: -1, max: 7, step: 0.5, value: st.v, color: 'green', format: L.nice, onInput: function (v) { st.v = v; st.defd = true; dc.set(true, true); draw(); } });
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.button(btns, '🔍 Zoom in', function () { if (st.zoom < 4) st.zoom++; draw(); }, true);
L.button(btns, 'Zoom out', function () { if (st.zoom > 0) st.zoom--; draw(); }, true);
var bR = L.button(btns, 'Reveal the limits', function () { st.reveal = !st.reveal; bR.textContent = st.reveal ? 'Hide the limits' : 'Reveal the limits'; draw(); });
L.reset(btns, function () { st.hi = 0; st.zoom = 0; st.reveal = false; bR.textContent = 'Reveal the limits'; sh.set(0, true); st.defd = st.c === 'moved'; st.v = st.c === 'moved' ? 5 : 3; sv.set(st.v, true); dc.set(st.defd, true); draw(); });
var tbl = L.table(P.panel);
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'In <b>Hole</b>, get within h = 0.01 of x = 1 on both sides. What number are both sides approaching? Is f(1) that number?', check: function () { return st.c === 'hole' && h() <= 0.01; } },
  { text: 'In <b>Moved point</b>, set f(2) to three different values. Predict first: does the limit change?', check: function () { return Object.keys(st.vals).length >= 3; } },
  { text: 'In <b>Moved point</b>, choose f(2) so the function is continuous at x = 2.', check: function () { return st.c === 'moved' && st.defd && st.v === 3; } },
  { text: 'In <b>Jump</b>, approach from both sides, then reveal the limits. Why doesn’t the two-sided limit exist?', check: function () { return st.c === 'jump' && st.reveal && h() <= 0.01; } },
  { text: 'In <b>Oscillation</b>, zoom in 4 times. Does the graph settle on one height? What does that say about zooming as evidence?', check: function () { return st.c === 'osc' && st.zoom >= 4; } },
  { text: 'In <b>Vertical asymptote</b>, get to h = 0.001. Is there a number that f(x) approaches?', check: function () { return st.c === 'asym' && h() <= 0.001; } }
]);
L.notice(P.below, '<p><b>The limit is about the values near a, not the value at a.</b> lim f(x) as x → a is the number f(x) gets close to as x gets close to a from both sides; f(a) itself can be different, or undefined, without changing the limit.</p>' +
  '<p>The two-sided limit exists only when the left-hand and right-hand limits are the same number. A function is <b>continuous</b> at a when f(a) is defined and equals the limit.</p>' +
  '<p>Tables and zooming are <b>evidence, not proof</b>: they only check some x-values. sin(1/x) keeps oscillating no matter how far you zoom, and a function can look settled in a table and still misbehave between the rows.</p>');
function build() { setBox.hidden = !C().canSet; }
function fmt(y) { if (!isFinite(y)) return 'undefined'; return Math.abs(y) >= 1e5 ? y.toExponential(2).replace('e+', ' × 10^') : L.num(y, 6); }
function limTxt(Lv) { return Lv === Infinity ? '∞ (grows without bound; no real limit)' : isNaN(Lv) ? 'does not exist' : L.nice(Lv); }
var draw = L.scheduler(function () {
  var c = C(), a = c.a, hv = h(), z = Math.pow(2, st.zoom);
  var Lc = isFinite(c.Lm) && c.Lm === c.Lp ? c.Lm : (isFinite(c.Lm) ? (c.Lm + c.Lp) / 2 : (c.view[2] + c.view[3]) / 2);
  var w = (c.view[1] - c.view[0]) / z, hh = (c.view[3] - c.view[2]) / z, cx = st.zoom ? a : (c.view[0] + c.view[1]) / 2, cy = st.zoom ? (st.c === 'asym' ? hh / 2 : Lc) : (c.view[2] + c.view[3]) / 2;
  L.setNiceView(g, GO, { xmin: cx - w / 2, xmax: cx + w / 2, ymin: cy - hh / 2, ymax: cy + hh / 2 }, 8, 8); g.clear();
  var opt = { color: 'blue', samples: st.c === 'osc' ? 4000 : 800 };
  if (c.split) { g.fn(c.f, Object.assign({}, opt, { to: a - 1e-9 })); g.fn(c.f, Object.assign({}, opt, { from: a })); }
  else g.fn(function (x) { return Math.abs(x - a) < 1e-12 ? NaN : c.f(x); }, opt);
  g.line(a, -1e3, a, 1e3, { color: 'ghost', width: 1.5, dash: '4 6' });
  /* open circles where the graph has no point */
  if (isFinite(c.Lm)) g.dot(a, c.Lm, { open: true, color: 'blue', r: 7 });
  if (isFinite(c.Lp) && c.Lp !== c.Lm) g.dot(a, c.Lp, { open: true, color: 'blue', r: 7 });
  var fv = valueAt();
  if (fv !== null) g.dot(a, fv, { color: 'green', r: 8, stroke: 'ink', strokeWidth: 2 });
  /* tracers */
  [[-1, 'orange'], [1, 'purple']].forEach(function (s) { var x = a + s[0] * hv, y = c.f(x); if (!isFinite(y)) return;
    g.line(x, Math.min(0, y), x, Math.max(0, y), { color: s[1], width: 2, dash: '3 5', opacity: 0.7 });
    g.dot(x, y, { color: s[1], r: 7, stroke: 'ink', strokeWidth: 2 }); });
  cap.innerHTML = 'f(' + L.V('x') + ') = ' + c.tex + ' near ' + L.V('x') + ' = ' + a + '. Orange: ' + L.V('x') + ' = a − h. Purple: ' + L.V('x') + ' = a + h.' + (st.zoom ? ' Zoom ×' + z + ': zooming is evidence, not proof.' : '');
  /* table */
  var rows = HS.slice(0, st.hi + 1).map(function (hh2) { return [L.num(a - hh2, 4), fmt(c.f(a - hh2)), L.num(a + hh2, 4), fmt(c.f(a + hh2))]; });
  tbl.set([L.V('x') + ' (left)', 'f(' + L.V('x') + ')', L.V('x') + ' (right)', 'f(' + L.V('x') + ')'], rows);
  /* readout */
  var two = isFinite(c.Lm) && c.Lm === c.Lp ? L.nice(c.Lm) : c.Lm === Infinity && c.Lp === Infinity ? '∞ (no real limit)' : 'does not exist';
  var lim = function (side) { return 'lim<sub>' + L.V('x') + '→' + a + (side || '') + '</sub> f(' + L.V('x') + ')'; };
  read.innerHTML = st.reveal ?
    '<dl class="kv" style="text-align:left"><dt>' + lim('⁻') + '</dt><dd>' + limTxt(c.Lm) + '</dd><dt>' + lim('⁺') + '</dt><dd>' + limTxt(c.Lp) + '</dd><dt>' + lim() + '</dt><dd>' + two + '</dd><dt>f(' + a + ')</dt><dd>' + (fv === null ? 'undefined' : L.nice(fv)) + '</dd></dl>' :
    'Approach ' + L.V('x') + ' = ' + a + ' from both sides. What do the table values approach? <div class="sub" style="margin-top:4px">f(' + a + ') = ' + (fv === null ? 'undefined' : L.nice(fv)) + '</div>';
  var cont = fv !== null && isFinite(c.Lm) && c.Lm === c.Lp && Math.abs(fv - c.Lm) < 1e-12;
  fb.set(st.reveal ? (cont ? '<b class="c-green">Continuous at ' + a + ':</b> f(' + a + ') is defined and equals the limit.' :
    '<b class="c-red">Not continuous at ' + a + ':</b> ' + (fv === null ? 'f(' + a + ') is undefined' : c.Lm !== c.Lp || !isFinite(c.Lm) ? 'the two-sided limit does not exist' : 'f(' + a + ') = ' + L.nice(fv) + ' but the limit is ' + L.nice(c.Lm)) + '.') :
    'The table only shows some x-values near ' + a + '. Use it to make a conjecture, then reveal.', st.reveal ? (cont ? 'good' : 'warn') : '');
  if (st.c === 'moved' && st.defd) st.vals[st.v] = true;
  ch.update();
});
build(); draw();
