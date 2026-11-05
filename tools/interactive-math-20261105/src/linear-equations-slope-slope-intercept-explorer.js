var st = { rise: 2, run: 3, b: 1, compare: 'none' };
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -10, ymax: 10, width: 600, height: 600, label: 'Graph of the line y = mx + b' });
var leg = L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>your line</span><span><i style="background:var(--orange)"></i>slope triangle (rise and run)</span><span><i style="background:var(--purple)"></i>comparison line</span>');

var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var srise = L.slider(P.panel, { id: 'rise', label: 'Rise (up or down)', min: -8, max: 8, value: st.rise, color: 'orange', format: L.num, onInput: function (v) { st.rise = v; draw(); } });
var srun = L.slider(P.panel, { id: 'run', label: 'Run (to the right)', min: 1, max: 8, value: st.run, color: 'orange', format: L.num, onInput: function (v) { st.run = v; draw(); } });
var sb = L.slider(P.panel, { id: 'b', label: 'b, the y-intercept', min: -8, max: 8, value: st.b, color: 'green', format: L.num, onInput: function (v) { st.b = v; draw(); } });
L.chips(P.panel, { label: 'Compare with', value: 'none', options: [{ value: 'none', label: 'Nothing' }, { value: 'parallel', label: 'Parallel line' }, { value: 'perp', label: 'Perpendicular line' }], onChange: function (v) { st.compare = v; draw(); } });
L.h('p', { class: 'sub' }, P.panel, 'Tip: drag the green point to change b, or the orange point to change the slope.');
var tbl = L.table(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Make a line that goes <b>downhill</b> from left to right.', check: function () { return m() < 0; } },
  { text: 'Make a <b>horizontal</b> line.', check: function () { return st.rise === 0; } },
  { text: 'Build ' + L.V('y') + ' = 2' + L.V('x') + ' − 3.', check: function () { return m() === 2 && st.b === -3; } },
  { text: 'Build ' + L.V('y') + ' = −' + L.frac(1, 2) + L.V('x') + ' + 4.', check: function () { return Math.abs(m() + 0.5) < 1e-9 && st.b === 4; } },
  { text: 'Make a line steeper than ' + L.V('y') + ' = 3' + L.V('x') + '.', check: function () { return Math.abs(m()) > 3; } },
  { text: 'Show a perpendicular line, and make your slope ' + L.frac(2, 3) + '. What is the other line\'s slope?', check: function () { return st.compare === 'perp' && Math.abs(m() - 2 / 3) < 1e-9; } }
]);

function m() { return st.rise / st.run; }
function slopeHTML(x) { var f = L.toFrac(x, 64); return f ? L.frac(f[0], f[1]) : L.num(x); }
function eq(mm, bb) { var f = L.toFrac(mm, 64), mpart;
  if (mm === 0) return L.V('y') + ' = ' + L.num(bb);
  mpart = (mm < 0 ? '−' : '') + (Math.abs(mm) === 1 ? '' : (f ? L.frac(Math.abs(f[0]), f[1]) : L.num(Math.abs(mm)))) + L.V('x');
  return L.V('y') + ' = ' + mpart + (bb ? (bb > 0 ? ' + ' : ' − ') + L.num(Math.abs(bb)) : ''); }

var draw = L.scheduler(function () {
  var mm = m(), b = st.b;
  g.clear();
  if (st.compare !== 'none') {
    var cm = st.compare === 'parallel' ? mm : (mm === 0 ? Infinity : -1 / mm), cb = b - 4;
    if (cm === Infinity) g.line(0, -11, 0, 11, { color: 'purple', width: 3, dash: '10 8' });
    else g.fullLine(0, cb, 1, cb + cm, { color: 'purple', width: 3, dash: '10 8' });
  }
  g.fullLine(0, b, 1, b + mm, { color: 'blue', width: 5 });
  // slope triangle from the y-intercept
  g.line(0, b, st.run, b, { color: 'orange', width: 4 });
  g.line(st.run, b, st.run, b + st.rise, { color: 'orange', width: 4 });
  if (st.run) g.text(st.run / 2, b, 'run ' + st.run, { anchor: 'middle', dy: st.rise >= 0 ? 22 : -10, color: 'orange' });
  if (st.rise) g.text(st.run, b + st.rise / 2, 'rise ' + L.num(st.rise), { dx: 10, color: 'orange' });
  g.handle(0, b, { color: 'green', snap: 1, label: 'y-intercept point', onDrag: function (x, y) { st.b = Math.max(-8, Math.min(8, y)); sb.set(st.b, true); draw(); } });
  g.handle(st.run, b + st.rise, { color: 'orange', snap: 1, label: 'slope point', onDrag: function (x, y) {
    st.run = Math.max(1, Math.min(8, x)); st.rise = Math.max(-8, Math.min(8, y - st.b)); srun.set(st.run, true); srise.set(st.rise, true); draw(); } });
  read.innerHTML = eq(mm, b) + '<div class="sub" style="margin-top:6px">slope ' + L.V('m') + ' = ' + (st.run === 1 ? L.num(st.rise) : L.frac(L.num(st.rise), st.run) + (L.gcd(st.rise, st.run) > 1 ? ' = ' + slopeHTML(mm) : '')) + ' &nbsp;·&nbsp; y-intercept (0, ' + L.num(b) + ')' +
    (st.compare !== 'none' ? ' &nbsp;·&nbsp; <span class="c-purple">' + (st.compare === 'parallel' ? 'parallel slope ' + slopeHTML(mm) : (mm === 0 ? 'perpendicular line is vertical' : 'perpendicular slope ' + slopeHTML(-1 / mm))) + '</span>' : '') + '</div>';
  var rows = [], ch1 = (mm >= 0 ? '+' : '') + slopeHTML(mm);
  for (var x = -2; x <= 2; x++) rows.push([L.num(x), slopeHTML(mm * x + b), x === -2 ? '—' : ch1]);
  tbl.set([L.V('x'), L.V('y'), 'change in ' + L.V('y')], rows);
  ch.update();
});
draw();
