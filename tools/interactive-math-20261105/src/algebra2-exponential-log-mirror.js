var NS = [1, 2, 4, 12, 52, 365, 8760, 525600];
var st = { mode: 'mirror', b: 2, t: 1, n: 1, seen: {} };
L.tabs(P.stage, [{ id: 'mirror', label: 'Exponential & log mirror' }, { id: 'e', label: 'Finding e' }], function (id) { st.mode = id; build(); draw(); });
var g = L.graph(P.stage, { xmin: -6, xmax: 8, ymin: -6, ymax: 8, width: 600, height: 600, xstep: 1, ystep: 1, label: 'Exponential function and its inverse' });
var legend = L.h('div', { class: 'legend' }, P.stage);
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var ctrl = L.h('div', { style: 'display:grid;gap:12px' }, P.panel);
var tbl = L.table(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Use the matching points to show that log<sub>2</sub> 8 = 3.', check: function () { return st.b === 2 && st.t === 3; } },
  { text: 'Make a base between 0 and 1. What happens to both graphs?', check: function () { return st.b < 1; } },
  { text: 'Find a base where the two graphs just touch the line ' + L.V('y') + ' = ' + L.V('x') + '.', check: function () { return st.b >= 1.4 && st.b <= 1.5; } },
  { text: 'In Finding e, compound every <b>day</b>. How close to ' + L.V('e') + ' are you?', check: function () { return st.n >= 365; } },
  { text: 'Find ' + L.V('e') + ' correct to 4 decimal places.', check: function () { return st.n >= 525600; } }
]);
function build() {
  ctrl.innerHTML = '';
  if (st.mode === 'mirror') {
    L.slider(ctrl, { id: 'base', label: 'Base b', min: 0.2, max: 4, step: 0.05, value: st.b, color: 'blue', format: function (v) { return L.num(v); }, onInput: function (v) { st.b = v; draw(); } });
    L.slider(ctrl, { id: 't', label: 'Input for the exponential', min: -3, max: 4, step: 0.5, value: st.t, color: 'orange', format: L.nice, onInput: function (v) { st.t = v; draw(); } });
    legend.innerHTML = '<span><i style="background:var(--blue)"></i>' + L.V('y') + ' = ' + L.V('b') + '<sup>' + L.V('x') + '</sup></span><span><i style="background:var(--purple)"></i>' + L.V('y') + ' = log<sub>' + L.V('b') + '</sub> ' + L.V('x') + '</span><span><i style="background:var(--ghost)"></i>' + L.V('y') + ' = ' + L.V('x') + ' (the mirror)</span>';
  } else {
    L.chips(ctrl, { label: 'Compound how often? ($1 at 100% interest for 1 year)', value: st.n, options: NS.map(function (n) { return { value: n, label: { 1: 'yearly', 2: 'twice', 4: 'quarterly', 12: 'monthly', 52: 'weekly', 365: 'daily', 8760: 'hourly', 525600: 'every minute' }[n] }; }), onChange: function (v) { st.n = v; draw(); } });
    legend.innerHTML = '<span><i style="background:var(--orange)"></i>value after 1 year</span><span><i style="background:var(--red)"></i>' + L.V('e') + ' ≈ 2.71828</span>';
  }
}
var draw = L.scheduler(function () {
  g.clear();
  if (st.mode === 'mirror') {
    g.setView({ xmin: -6, xmax: 8, ymin: -6, ymax: 8 });
    var b = st.b;
    if (Math.abs(b - 1) < 1e-9) { read.innerHTML = '<span class="c-red">Base 1 doesn\'t work: 1<sup>' + L.V('x') + '</sup> is always 1, so it has no inverse function.</span>'; tbl.set([], []); ch.update(); return; }
    g.fn(function (x) { return x; }, { color: 'ghost', width: 2, dash: '8 6' });
    g.fn(function (x) { return Math.pow(b, x); }, { color: 'blue' });
    g.fn(function (x) { return x > 0 ? Math.log(x) / Math.log(b) : NaN; }, { color: 'purple', samples: 1200 });
    var y = Math.pow(b, st.t);
    if (y <= 8) {
      g.line(st.t, y, y, st.t, { color: 'orange', width: 2, dash: '5 5' });
      g.dot(st.t, y, { color: 'blue', r: 8, stroke: 'ink', strokeWidth: 2 }); g.dot(y, st.t, { color: 'purple', r: 8, stroke: 'ink', strokeWidth: 2 });
      g.text(st.t, y, '(' + L.num(st.t) + ', ' + L.num(y) + ')', { dx: -12, dy: -12, anchor: 'end', color: 'blue' });
      g.text(y, st.t, '(' + L.num(y) + ', ' + L.num(st.t) + ')', { dx: 12, dy: 18, color: 'purple' });
    }
    read.innerHTML = L.num(b) + '<sup>' + L.num(st.t) + '</sup> = ' + L.num(y, 3) + ' &nbsp;⟷&nbsp; log<sub>' + L.num(b) + '</sub> ' + L.num(y, 3) + ' = ' + L.num(st.t) +
      '<div class="sub" style="margin-top:6px">The inputs and outputs swap, so the graphs are reflections across ' + L.V('y') + ' = ' + L.V('x') + '.</div>';
    var rows = [-2, -1, 0, 1, 2, 3].map(function (x) { var v = Math.pow(b, x); return [L.num(x), L.num(v, 3), L.num(v, 3), L.num(x)]; });
    tbl.set([L.V('x'), L.V('b') + '<sup>' + L.V('x') + '</sup>', L.V('x'), 'log<sub>' + L.V('b') + '</sub> ' + L.V('x')], rows);
  } else {
    g.setView({ xmin: -0.5, xmax: 8.5, ymin: 1.8, ymax: 2.85 });
    g.line(-1, Math.E, 9, Math.E, { color: 'red', width: 2, dash: '8 6' });
    var pts = NS.map(function (n, i) { return [i, Math.pow(1 + 1 / n, n)]; });
    pts.forEach(function (p, i) { if (NS[i] <= st.n) { g.rect(p[0] - 0.3, 1.8, 0.6, p[1] - 1.8, { fill: 'orange', opacity: NS[i] === st.n ? 1 : 0.45, stroke: 'ink' }); g.text(p[0], p[1], L.num(p[1], 4), { anchor: 'middle', dy: -8, size: 12 }); } });
    var n = st.n, v = Math.pow(1 + 1 / n, n);
    read.innerHTML = '(1 + ' + L.frac(1, L.num(n)) + ')<sup>' + L.num(n) + '</sup> = ' + L.num(v, 6) + '<div class="sub" style="margin-top:6px">' + L.V('e') + ' = 2.718282… &nbsp; difference: ' + L.num(Math.E - v, 6) + '</div>';
    tbl.set(['times per year', 'value of $1'], NS.filter(function (m) { return m <= n; }).map(function (m) { return [m.toLocaleString(), '$' + L.num(Math.pow(1 + 1 / m, m), 6)]; }));
  }
  ch.update();
});
build(); draw();
