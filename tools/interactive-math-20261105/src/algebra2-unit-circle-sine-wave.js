var R3 = '√3', R2 = '√2';
function fr(n, d) { return L.frac(n, d); }
var EXACT = { 0: ['1', '0'], 30: [fr(R3, 2), fr(1, 2)], 45: [fr(R2, 2), fr(R2, 2)], 60: [fr(1, 2), fr(R3, 2)], 90: ['0', '1'] };
function exact(deg) { // exact [cos, sin] for multiples of 30° and 45°
  deg = ((deg % 360) + 360) % 360;
  var ref = deg <= 90 ? deg : deg <= 180 ? 180 - deg : deg <= 270 ? deg - 180 : 360 - deg;
  if (!EXACT[ref]) return null;
  var c = EXACT[ref][0], s = EXACT[ref][1];
  var cs = deg > 90 && deg < 270 ? -1 : 1, ss = deg > 180 && deg < 360 ? -1 : 1;
  function sign(v, sg) { return v === '0' ? '0' : (sg < 0 ? '−' : '') + v; }
  return [sign(c, cs), sign(s, ss)];
}
function rad(deg) { // degrees as a multiple of π, stacked fraction
  if (deg === 0) return '0';
  var g = L.gcd(deg, 180), n = deg / g, d = 180 / g, top = (n === 1 ? '' : n) + 'π';
  return d === 1 ? top : L.frac(top, d);
}
var PI_TICKS = [];
[-4, -3, -2, -1, 1, 2, 3, 4].forEach(function (k) { var sg = k < 0 ? '−' : '', a = Math.abs(k); PI_TICKS.push(a % 2 ? { x: k * Math.PI / 2, num: sg + (a === 1 ? '' : a) + 'π', den: '2' } : { x: k * Math.PI / 2, num: sg + (a === 2 ? '' : a / 2) + 'π' }); });
var st = { mode: 'circle', deg: 30, snap: true, A: 1, B: 1, C: 0, D: 0, seen: {} };
L.tabs(P.stage, [{ id: 'circle', label: 'Unit circle to wave' }, { id: 'wave', label: 'Transform the wave' }], function (id) { st.mode = id; build(); draw(); });
var row = L.h('div', { style: 'display:grid;grid-template-columns:minmax(0,0.8fr) minmax(0,1.2fr);gap:8px;align-items:center;margin-top:8px' }, P.stage);
var cBox = L.h('div', null, row), wBox = L.h('div', null, row);
var gc = L.graph(cBox, { xmin: -1.35, xmax: 1.35, ymin: -1.35, ymax: 1.35, width: 360, height: 360, xstep: 0.5, ystep: 0.5, noLabels: true, label: 'Unit circle' });
var gw = L.graph(wBox, { xmin: -0.3, xmax: 2 * Math.PI + 0.3, ymin: -1.4, ymax: 1.4, width: 520, height: 300, xstep: Math.PI / 6, ystep: 0.5, xticks: PI_TICKS, label: 'Sine and cosine graphs' });
var legend = L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--orange)"></i>sine = height (' + L.V('y') + ')</span><span><i style="background:var(--blue)"></i>cosine = horizontal position (' + L.V('x') + ')</span>');
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var ctrl = L.h('div', { style: 'display:grid;gap:12px' }, P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Find the angle where sine is at its <b>maximum</b>.', check: function () { return st.seen.max; } },
  { text: 'Find an angle where sine is negative but cosine is positive.', check: function () { return st.seen.q4; } },
  { text: 'Find an angle where sine and cosine are equal.', check: function () { return st.seen.eq; } },
  { text: 'In Transform the wave, make the amplitude 3.', check: function () { return Math.abs(st.A) === 3; } },
  { text: 'Make the period π. What value of ' + L.V('B') + ' does that take?', check: function () { return st.B === 2; } }
]);
function build() {
  ctrl.innerHTML = '';
  if (st.mode === 'circle') {
    cBox.hidden = false; row.style.gridTemplateColumns = 'minmax(0,0.8fr) minmax(0,1.2fr)';
    gw.setView({ xmin: -0.3, xmax: 2 * Math.PI + 0.3, ymin: -1.4, ymax: 1.4 });
    st.sDeg = L.slider(ctrl, { id: 'deg', label: 'Angle θ (or drag the point)', min: 0, max: 360, step: 15, value: st.deg, color: 'purple', format: function (v) { return v + '°'; }, onInput: function (v) { st.deg = v; draw(); } });
    L.chips(ctrl, { label: 'Dragging', value: true, options: [{ value: true, label: 'snap to 15°' }, { value: false, label: 'free' }], onChange: function (v) { st.snap = v; } });
    legend.hidden = false;
  } else {
    cBox.hidden = true; row.style.gridTemplateColumns = '1fr';
    gw.setView({ xmin: -2 * Math.PI - 0.3, xmax: 2 * Math.PI + 0.3, ymin: -4.5, ymax: 4.5 });
    L.slider(ctrl, { id: 'A', label: 'A: amplitude (and reflection)', min: -3, max: 3, step: 0.5, value: st.A, color: 'orange', format: L.nice, onInput: function (v) { st.A = v; draw(); } });
    L.slider(ctrl, { id: 'B', label: 'B: changes the period', min: 0.5, max: 4, step: 0.5, value: st.B, color: 'purple', format: L.nice, onInput: function (v) { st.B = v; draw(); } });
    L.slider(ctrl, { id: 'C', label: 'C: phase shift', min: -12, max: 12, value: st.C * 12 / Math.PI, color: 'blue', format: function (v) { return v === 0 ? '0' : (v < 0 ? '−' : '') + rad(Math.abs(v) * 15); }, onInput: function (v) { st.C = v * Math.PI / 12; st.Cn = v; draw(); } });
    L.slider(ctrl, { id: 'D', label: 'D: midline (up or down)', min: -3, max: 3, step: 0.5, value: st.D, color: 'green', format: L.nice, onInput: function (v) { st.D = v; draw(); } });
    legend.hidden = true;
  }
}
var draw = L.scheduler(function () {
  gw.clear();
  if (st.mode === 'circle') {
    var t = st.deg * Math.PI / 180, c = Math.cos(t), s = Math.sin(t);
    gc.clear();
    gc.param(Math.cos, Math.sin, 0, 2 * Math.PI, { color: 'ink', width: 3 });
    gc.param(function (u) { return 0.25 * Math.cos(u); }, function (u) { return 0.25 * Math.sin(u); }, 0, t, { color: 'purple', width: 3 });
    gc.line(0, 0, c, s, { color: 'purple', width: 3 });
    gc.line(0, 0, c, 0, { color: 'blue', width: 6 });
    gc.line(c, 0, c, s, { color: 'orange', width: 6 });
    gc.handle(c, s, { color: 'purple', label: 'Point on the unit circle', onDrag: function (x, y) {
      var d = Math.atan2(y, x) * 180 / Math.PI; if (d < 0) d += 360;
      d = st.snap ? Math.round(d / 15) * 15 : Math.round(d); if (d === 360 && st.deg < 180) d = 0;
      st.deg = d; st.sDeg.set(d, true); st.sDeg.el.querySelector('output').textContent = d + '°'; draw(); } });
    gw.fn(Math.sin, { color: 'orange', width: 2, dash: '6 6', opacity: 0.5 });
    gw.fn(Math.cos, { color: 'blue', width: 2, dash: '6 6', opacity: 0.5 });
    gw.fn(Math.sin, { color: 'orange', width: 4, from: 0, to: t });
    gw.fn(Math.cos, { color: 'blue', width: 4, from: 0, to: t });
    gw.line(t, 0, t, s, { color: 'orange', width: 3 });
    gw.dot(t, s, { color: 'orange', r: 7 }); gw.dot(t, c, { color: 'blue', r: 7 });
    var ex = st.deg % 15 === 0 ? exact(st.deg) : null;
    read.innerHTML = 'θ = ' + st.deg + '° = ' + rad(st.deg) + ' radians';
    info.innerHTML = '<dt>Point</dt><dd>(cos θ, sin θ) = (' + L.num(c, 3) + ', ' + L.num(s, 3) + ')</dd>' +
      '<dt class="c-blue">cos θ</dt><dd>' + (ex ? ex[0] + ' ≈ ' : '') + L.num(c, 3) + '</dd><dt class="c-orange">sin θ</dt><dd>' + (ex ? ex[1] + ' ≈ ' : '') + L.num(s, 3) + '</dd>' +
      '<dt>Quadrant</dt><dd>' + (st.deg % 90 === 0 ? 'on an axis' : ['I', 'II', 'III', 'IV'][Math.floor(st.deg / 90) % 4]) + '</dd>';
    if (st.deg === 90) st.seen.max = true; if (s < -1e-9 && c > 1e-9) st.seen.q4 = true; if (Math.abs(s - c) < 1e-9) st.seen.eq = true;
  } else {
    var A = st.A, B = st.B, C = st.C, D = st.D;
    gw.fn(Math.sin, { color: 'ghost', width: 3, dash: '8 6' });
    gw.line(-7, D, 7, D, { color: 'green', width: 2, dash: '5 5' });
    gw.fn(function (x) { return A * Math.sin(B * (x - C)) + D; }, { color: 'orange', width: 4, samples: 1200 });
    var per = 2 / B, pf = L.toFrac(per, 16), perTxt = !pf ? L.num(per, 3) + 'π' : pf[1] === 1 ? (pf[0] === 1 ? '' : pf[0]) + 'π' : L.frac((pf[0] === 1 ? '' : pf[0]) + 'π', pf[1]);
    var cn = st.Cn || 0, cTxt = cn === 0 ? '' : (cn > 0 ? ' − ' : ' + ') + rad(Math.abs(cn) * 15);
    read.innerHTML = L.V('y') + ' = ' + (A === 1 ? '' : A === -1 ? '−' : L.nice(A)) + 'sin(' + (B === 1 ? '' : L.nice(B)) + (cn ? '(' + L.V('x') + cTxt + ')' : L.V('x')) + ')' + (D ? (D > 0 ? ' + ' : ' − ') + L.nice(Math.abs(D)) : '');
    info.innerHTML = '<dt>Amplitude |A|</dt><dd>' + L.nice(Math.abs(A)) + (A < 0 ? ' (reflected)' : '') + '</dd><dt>Period ' + L.frac('2π', L.V('B')) + '</dt><dd>' + perTxt + '</dd>' +
      '<dt>Phase shift</dt><dd>' + (cn === 0 ? 'none' : rad(Math.abs(cn) * 15) + ' ' + (cn > 0 ? 'right' : 'left')) + '</dd><dt>Midline</dt><dd>' + L.V('y') + ' = ' + L.nice(D) + '</dd>';
  }
  ch.update();
});
build(); draw();
