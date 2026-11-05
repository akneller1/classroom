var st = { a: 2, b: 1.5, m: 3, c: 2, seen: {} };
var g = L.graph(P.stage, { xmin: -1, xmax: 10, ymin: -5, ymax: 60, width: 640, height: 520, label: 'Linear and exponential functions', xstep: 1, ystep: 5, ylabelStep: 10 });
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>linear: adds the same amount</span><span><i style="background:var(--orange)"></i>exponential: multiplies by the same amount</span>');
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
L.h('h2', { class: 'c-orange' }, P.panel, 'Exponential ' + L.V('y') + ' = ' + L.V('a') + ' · ' + L.V('b') + '<sup>' + L.V('x') + '</sup>');
L.slider(P.panel, { id: 'a', label: 'a, starting value', min: 1, max: 10, value: st.a, color: 'orange', format: L.num, onInput: function (v) { st.a = v; draw(); } });
L.slider(P.panel, { id: 'b', label: 'b, growth factor', min: 0.25, max: 3, step: 0.05, value: st.b, color: 'orange', format: function (v) { return L.num(v); }, onInput: function (v) { st.b = v; draw(); } });
L.h('h2', { class: 'c-blue' }, P.panel, 'Linear ' + L.V('y') + ' = ' + L.V('mx') + ' + ' + L.V('c'));
L.slider(P.panel, { id: 'm', label: 'm, amount added each step', min: -5, max: 10, value: st.m, color: 'blue', format: L.num, onInput: function (v) { st.m = v; draw(); } });
L.slider(P.panel, { id: 'c', label: 'c, starting value', min: 0, max: 20, value: st.c, color: 'blue', format: L.num, onInput: function (v) { st.c = v; draw(); } });
var tbl = L.table(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Make the exponential function <b>decay</b>.', check: function () { return st.b < 1; } },
  { text: 'Make it decay by <b>half</b> each step.', check: function () { return Math.abs(st.b - 0.5) < 1e-9; } },
  { text: 'Set ' + L.V('b') + ' = 1. What happens, and why?', check: function () { return Math.abs(st.b - 1) < 1e-9; } },
  { text: 'Make the linear function start ahead, then have the exponential pass it before ' + L.V('x') + ' = 8.', check: function () { return st.seen.pass; } },
  { text: 'Make 25% growth: the exponential grows by 25% each step.', check: function () { return Math.abs(st.b - 1.25) < 1e-9; } }
]);
var draw = L.scheduler(function () {
  var a = st.a, b = st.b, m = st.m, c = st.c;
  var top = 10; for (var x = 0; x <= 10; x++) top = Math.max(top, Math.min(400, a * Math.pow(b, x)), m * x + c);
  var ymax = top <= 60 ? 60 : top <= 120 ? 120 : top <= 250 ? 250 : 400;
  g.setView({ ymin: -ymax / 12, ymax: ymax }); g.clear();
  g.fn(function (x) { return m * x + c; }, { color: 'blue', from: 0 });
  g.fn(function (x) { return a * Math.pow(b, x); }, { color: 'orange', from: 0 });
  for (x = 0; x <= 10; x++) { g.dot(x, m * x + c, { color: 'blue', r: 5 }); var ey = a * Math.pow(b, x); if (ey <= ymax) g.dot(x, ey, { color: 'orange', r: 5 }); }
  if (b < 1) g.line(0, 0, 10, 0, { color: 'red', width: 3, dash: '8 6' });
  var rows = [];
  for (x = 0; x <= 6; x++) {
    var ly = m * x + c, ex = a * Math.pow(b, x);
    rows.push([x, L.num(ly), x ? (m >= 0 ? '+' : '') + L.num(m) : '—', L.num(ex, 2), x ? '×' + L.num(b) : '—']);
  }
  tbl.set([L.V('x'), 'linear', 'change', 'exponential', 'change'], rows);
  var lead = c > a, pass = false; for (x = 1; x <= 8; x++) if (lead && a * Math.pow(b, x) > m * x + c) pass = true;
  if (pass) st.seen.pass = true;
  var pct = Math.round((b - 1) * 100);
  read.innerHTML = '<span class="c-orange">' + L.V('y') + ' = ' + L.num(a) + ' · ' + L.num(b) + '<sup>' + L.V('x') + '</sup></span><br><span class="c-blue">' + L.V('y') + ' = ' + L.terms([[m, 'x'], [c, '']], { frac: false }) + '</span>' +
    '<div class="sub" style="margin-top:6px">' + (b > 1 ? 'Growth: ' + pct + '% more each step' : b < 1 ? 'Decay: ' + (-pct) + '% less each step. The graph gets closer to ' + L.V('y') + ' = 0 but never reaches it.' : 'b = 1: multiplying by 1 changes nothing, so the graph is flat.') + '</div>';
  ch.update();
});
draw();
