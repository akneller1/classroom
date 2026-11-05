var SYM = { eq: '=', lt: '<', le: '≤', gt: '>', ge: '≥' };
var st = { m1: 1, b1: 1, m2: -0.5, b2: 5, s1: 'eq', s2: 'eq', ineq: false, test: [0, 0], seen: {} };
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -10, ymax: 10, width: 600, height: 600, label: 'Two lines and their intersection' });
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>Line 1</span><span><i style="background:var(--orange)"></i>Line 2</span><span><i style="background:var(--green)"></i>solution</span>');
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
function fmtm(v) { return L.nice(v, 4); }
L.h('h2', { class: 'c-blue' }, P.panel, 'Line 1');
L.slider(P.panel, { id: 'm1', label: 'slope', min: -4, max: 4, step: 0.25, value: st.m1, color: 'blue', format: fmtm, onInput: function (v) { st.m1 = v; draw(); } });
L.slider(P.panel, { id: 'b1', label: 'y-intercept', min: -8, max: 8, value: st.b1, color: 'blue', format: L.num, onInput: function (v) { st.b1 = v; draw(); } });
L.h('h2', { class: 'c-orange' }, P.panel, 'Line 2');
L.slider(P.panel, { id: 'm2', label: 'slope', min: -4, max: 4, step: 0.25, value: st.m2, color: 'orange', format: fmtm, onInput: function (v) { st.m2 = v; draw(); } });
L.slider(P.panel, { id: 'b2', label: 'y-intercept', min: -8, max: 8, value: st.b2, color: 'orange', format: L.num, onInput: function (v) { st.b2 = v; draw(); } });
L.chips(P.panel, { label: 'Mode', value: false, options: [{ value: false, label: 'Equations' }, { value: true, label: 'Inequalities' }], onChange: function (v) { st.ineq = v; if (v && st.s1 === 'eq') { st.s1 = 'ge'; st.s2 = 'le'; c1.set('ge', true); c2.set('le', true); } build(); draw(); } });
var ineqBox = L.h('div', { style: 'display:grid;gap:10px' }, P.panel);
var c1 = L.chips(ineqBox, { label: 'Line 1: ' + L.V('y'), value: st.s1, options: ['lt', 'le', 'gt', 'ge'].map(function (k) { return { value: k, label: SYM[k] }; }), onChange: function (v) { st.s1 = v; draw(); } });
var c2 = L.chips(ineqBox, { label: 'Line 2: ' + L.V('y'), value: st.s2, options: ['lt', 'le', 'gt', 'ge'].map(function (k) { return { value: k, label: SYM[k] }; }), onChange: function (v) { st.s2 = v; draw(); } });
L.h('p', { class: 'sub' }, ineqBox, 'Drag the purple test point to check whether it solves both inequalities.');
function build() { ineqBox.hidden = !st.ineq; }
var ch = L.challenges(P.panel, [
  { text: 'Make a system whose solution is (2, 3).', check: function () { return st.seen.p23; } },
  { text: 'Make a system with <b>no solution</b>.', check: function () { return st.seen.none; } },
  { text: 'Make a system with <b>infinitely many</b> solutions.', check: function () { return st.seen.inf; } },
  { text: 'Make the solution land in Quadrant II.', check: function () { return st.seen.q2; } },
  { text: 'In Inequalities mode, find a test point that solves <b>both</b> inequalities.', check: function () { return st.seen.both; } }
]);
function sat(s, y, f) { return s === 'lt' ? y < f : s === 'le' ? y <= f + 1e-9 : s === 'gt' ? y > f : y >= f - 1e-9; }
function eqn(m, b, s) { return L.V('y') + ' ' + SYM[s] + ' ' + L.terms([[m, 'x'], [b, '']]); }
var draw = L.scheduler(function () {
  var m1 = st.m1, b1 = st.b1, m2 = st.m2, b2 = st.b2, s1 = st.ineq ? st.s1 : 'eq', s2 = st.ineq ? st.s2 : 'eq';
  g.clear();
  if (st.ineq) {
    [[m1, b1, s1, 'blue'], [m2, b2, s2, 'orange']].forEach(function (L1) {
      var up = L1[2] === 'gt' || L1[2] === 'ge', e = up ? 11 : -11;
      g.poly([[-11, L1[1] - 11 * L1[0]], [11, L1[1] + 11 * L1[0]], [11, up ? 60 : -60], [-11, up ? 60 : -60]], { fill: L1[3], opacity: 0.16 });
    });
  }
  g.fullLine(0, b1, 1, b1 + m1, { color: 'blue', width: 4, dash: st.ineq && (s1 === 'lt' || s1 === 'gt') ? '12 8' : null });
  g.fullLine(0, b2, 1, b2 + m2, { color: 'orange', width: 4, dash: st.ineq && (s2 === 'lt' || s2 === 'gt') ? '12 8' : (m1 === m2 && b1 === b2 ? '14 10' : null) });
  var status, sol = '';
  if (m1 === m2) {
    if (b1 === b2) { status = '<span class="c-green"><b>Infinitely many solutions.</b></span> The lines are the same line, so every point on it works.'; st.seen.inf = true; }
    else { status = '<span class="c-red"><b>No solution.</b></span> Same slope, different y-intercepts: the lines are parallel and never meet.'; st.seen.none = true; }
  } else {
    var x = (b2 - b1) / (m1 - m2), y = m1 * x + b1;
    sol = '(' + L.nice(x, 12) + ', ' + L.nice(y, 12) + ')';
    if (Math.abs(x) <= 10 && Math.abs(y) <= 10) { g.dot(x, y, { color: 'green', r: 10, stroke: 'ink', strokeWidth: 3 }); g.text(x, y, '(' + L.num(x) + ', ' + L.num(y) + ')', { dx: 14, dy: -12, color: 'green' }); }
    status = '<span class="c-green"><b>One solution:</b></span> ' + sol + (Math.abs(x) > 10 || Math.abs(y) > 10 ? ' (off the screen)' : '');
    if (Math.abs(x - 2) < 1e-9 && Math.abs(y - 3) < 1e-9) st.seen.p23 = true;
    if (x < 0 && y > 0) st.seen.q2 = true;
  }
  var tline = '';
  if (st.ineq) {
    var tx = st.test[0], ty = st.test[0] * 0 + st.test[1];
    var ok1 = sat(s1, ty, m1 * tx + b1), ok2 = sat(s2, ty, m2 * tx + b2);
    g.handle(tx, ty, { color: 'purple', snap: 1, label: 'Test point', onDrag: function (a, b) { st.test = [a, b]; draw(); } });
    if (ok1 && ok2) st.seen.both = true;
    tline = '<div class="sub" style="margin-top:6px">Test (' + L.num(tx) + ', ' + L.num(ty) + '): Line 1 ' + (ok1 ? '<b class="c-green">✓</b>' : '<b class="c-red">✗</b>') + ' · Line 2 ' + (ok2 ? '<b class="c-green">✓</b>' : '<b class="c-red">✗</b>') + (ok1 && ok2 ? ' · in the overlap, so it solves the system' : '') + '</div>';
    status = 'The solutions are the points where the two shadings <b>overlap</b>.';
  }
  read.innerHTML = '<div class="c-blue">' + eqn(m1, b1, s1) + '</div><div class="c-orange">' + eqn(m2, b2, s2) + '</div><div class="sub" style="margin-top:6px">' + status + '</div>' + tline;
  ch.update();
});
build(); draw();
