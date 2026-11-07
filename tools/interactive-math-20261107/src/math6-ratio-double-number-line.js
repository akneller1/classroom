/* Double number line: top amount a, bottom amount b. A marker at multiplier k shows (k·a, k·b).
   The same pairs appear in the ratio table and as points on a line through the origin. */
var CTX = {
  juice: { top: 'cups of concentrate', bot: 'cups of water', one: 'cup of concentrate', a: 3, b: 5 },
  trip: { top: 'hours', bot: 'miles', one: 'hour', a: 2, b: 7 },
  shop: { top: 'pounds of apples', bot: 'dollars', one: 'pound of apples', a: 4, b: 6 }
};
var KMAX = 6;
var st = { ctx: 'juice', a: 3, b: 5, k: 1, test: null, seen: {} };
function q() { return CTX[st.ctx]; }
function step() { return 1 / (st.a * st.b); }
function snapK(k) { var s = step(); return L.round(Math.max(0, Math.min(KMAX, Math.round(k / s) * s)), 9); }
/* Exact fraction text for n/d (stacked), mixed with whole numbers. */
function fr(n, d) { var g = L.gcd(n, d); n /= g; d /= g; return d === 1 ? L.num(n) : L.frac(n, d); }
function kParts() { var s = st.a * st.b, n = Math.round(st.k * s); return [n, s]; }   // k = n / s exactly
function topTxt() { var p = kParts(); return fr(p[0] * st.a, p[1]); }
function botTxt() { var p = kParts(); return fr(p[0] * st.b, p[1]); }
function topVal() { return st.k * st.a; }
function botVal() { return st.k * st.b; }

L.chips(P.panel, { label: 'Situation', value: st.ctx, options: [{ value: 'juice', label: 'Juice recipe' }, { value: 'trip', label: 'Road trip' }, { value: 'shop', label: 'Buying apples' }],
  onChange: function (v) { st.ctx = v; st.a = CTX[v].a; st.b = CTX[v].b; sA.set(st.a, true); sB.set(st.b, true); st.k = 1; st.test = null; tA.set(''); tB.set(''); draw(); } });
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var sA = L.slider(P.panel, { id: 'top-amount', label: 'Top amount in the ratio', min: 1, max: 9, value: st.a, color: 'blue', format: L.num, onInput: function (v) { st.a = v; st.k = snapK(st.k); draw(); } });
var sB = L.slider(P.panel, { id: 'bottom-amount', label: 'Bottom amount in the ratio', min: 1, max: 9, value: st.b, color: 'orange', format: L.num, onInput: function (v) { st.b = v; st.k = snapK(st.k); draw(); } });
L.h('p', { class: 'sub' }, P.panel, 'Drag the purple marker along the double number line (or focus it and use the arrow keys; Shift + arrow jumps to the next whole copy of the ratio).');
var tbl = L.table(P.panel);

/* Test any pair */
L.h('h2', null, P.panel, 'Test a pair');
var testRow = L.h('div', { class: 'lp-row' }, P.panel);
var tA = L.numInput(testRow, { id: 'test-top', label: 'Top', min: 0, max: 200, step: 'any', value: '', onChange: function () { readTest(); } });
var tB = L.numInput(testRow, { id: 'test-bottom', label: 'Bottom', min: 0, max: 200, step: 'any', value: '', onChange: function () { readTest(); } });
var fb = L.feedback(P.panel);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st.a = CTX[st.ctx].a; st.b = CTX[st.ctx].b; sA.set(st.a, true); sB.set(st.b, true); st.k = 1; st.test = null; tA.set(''); tB.set(''); draw(); });
function readTest() { var x = tA.get(), y = tB.get(); st.test = x == null || y == null ? null : [x, y]; draw(); }

var ch = L.challenges(P.panel, [
  { text: 'Find the <b>unit rate</b>: move the marker so the top line reads exactly 1. What does the bottom line say?', check: function () { return st.seen.unitTop; } },
  { text: 'Now find the other unit rate: how much of the <b>top</b> amount goes with exactly 1 of the bottom amount?', check: function () { return st.seen.unitBot; } },
  { text: 'Test a pair that is equivalent to the ratio and has both numbers greater than 20. Predict it before you type it.', check: function () { return st.seen.big; } },
  { text: 'A classmate says “add the same number to both parts and the ratio stays the same.” Test a pair made that way. What happens?', check: function () { return st.seen.additive; } },
  { text: 'Change the ratio so the juice is <b>stronger</b> than 3 : 5 (more concentrate for each cup of water). Which column of the table proves it?', check: function () { return st.ctx === 'juice' && st.a / st.b > 0.6 + 1e-9; } }
]);
L.notice(P.below, '<p><b>Equivalent ratios come from multiplying (or dividing) both amounts by the same number.</b> On the double number line, every tick on the top line lines up with a tick on the bottom line, so the two amounts always grow by the same factor.</p>' +
  '<p>The <b>unit rate</b> is the amount that goes with exactly 1. It is the same in every row of the table: bottom ÷ top never changes for equivalent ratios.</p>' +
  '<p>Adding the same number to both parts does <b>not</b> keep the ratio: 3 : 5 and 5 : 7 are different mixtures. On the graph, equivalent pairs sit on one straight line through (0, 0); other pairs fall off it.</p>');

var W = 640, H = 320, X0 = 40, X1 = 600, YT = 80, YB = 240;
var svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Double number line' }, P.stage);
var GO = { xmin: -1, xmax: 30, ymin: -1, ymax: 30, width: 640, height: 330, label: 'Graph of equivalent pairs' }, g = L.graph(P.stage, GO);
L.h('p', { class: 'sub', style: 'margin:4px 6px 0' }, P.stage, 'Graph: each equivalent pair (top, bottom) is a point. Your test pair is the square.');
var keeper = L.focusKeeper(svg);
function XK(k) { return X0 + k / KMAX * (X1 - X0); }
function txt(x, y, s, o) { o = o || {}; var t = L.s('text', { x: x, y: y, 'text-anchor': o.anchor || 'middle', class: o.cls || 'g-label', 'font-size': o.size || 15, fill: o.color || null }, svg); t.innerHTML = s; return t; }

var draw = L.scheduler(function () {
  keeper.save();
  svg.innerHTML = '';
  var a = st.a, b = st.b, c = q();
  /* lines */
  [[YT, 'blue', c.top], [YB, 'orange', c.bot]].forEach(function (r) {
    L.s('line', { x1: X0 - 10, x2: X1 + 18, y1: r[0], y2: r[0], stroke: 'var(--' + r[1] + ')', 'stroke-width': 4 }, svg);
    L.s('path', { d: 'M' + (X1 + 26) + ' ' + r[0] + ' l -12 -7 v 14 z', fill: 'var(--' + r[1] + ')' }, svg);
    txt(X0 - 10, r[0] === YT ? r[0] - 34 : r[0] + 44, r[2], { anchor: 'start', size: 14, color: 'var(--' + r[1] + ')' });
  });
  for (var k = 0; k <= KMAX; k++) {
    L.s('line', { x1: XK(k), x2: XK(k), y1: YT - 9, y2: YT + 9, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    L.s('line', { x1: XK(k), x2: XK(k), y1: YB - 9, y2: YB + 9, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    txt(XK(k), YT - 14, L.num(k * a), { size: 15 });
    txt(XK(k), YB + 26, L.num(k * b), { size: 15 });
  }
  /* marker */
  var xm = XK(st.k);
  L.s('line', { x1: xm, x2: xm, y1: YT - 2, y2: YB + 2, stroke: 'var(--purple)', 'stroke-width': 3, 'stroke-dasharray': '7 5' }, svg);
  L.s('circle', { cx: xm, cy: YT, r: 7, fill: 'var(--purple)' }, svg);
  L.s('circle', { cx: xm, cy: YB, r: 7, fill: 'var(--purple)' }, svg);
  var hnd = L.s('rect', { x: xm - 15, y: (YT + YB) / 2 - 18, width: 30, height: 36, rx: 8, fill: 'var(--purple)', stroke: 'var(--ink)', 'stroke-width': 3 }, svg);
  L.drag(hnd, { svg: svg, label: 'Marker on the double number line', valueText: 'top ' + L.num(topVal(), 3) + ', bottom ' + L.num(botVal(), 3),
    onMove: function (x) { st.k = snapK((x - X0) / (X1 - X0) * KMAX); draw(); },
    onKey: function (dx, dy, big) { var d = dx || dy; if (!d) return; st.k = big ? (d > 0 ? Math.floor(st.k + 1e-9) + 1 : Math.ceil(st.k - 1e-9) - 1) : st.k + d * step(); st.k = snapK(Math.max(0, Math.min(KMAX, st.k))); draw(); } });
  /* value labels beside the marker */
  var right = xm < W - 150, lx = right ? xm + 14 : xm - 134;
  [[YT + 10, topTxt()], [YB - 50, botTxt()]].forEach(function (r) {
    var fo = L.s('foreignObject', { x: lx, y: r[0], width: 120, height: 40 }, svg);
    fo.innerHTML = '<div xmlns="http://www.w3.org/1999/xhtml" style="display:flex;height:100%;align-items:center;justify-content:' + (right ? 'flex-start' : 'flex-end') + ';font-weight:800;color:var(--purple);font-size:19px;line-height:1.05">' + r[1] + '</div>';
  });
  keeper.restore();

  /* readout */
  var p = kParts();
  read.innerHTML = a + ' : ' + b + ' = ' + topTxt() + ' : ' + botTxt() +
    '<div class="sub" style="margin-top:6px">both amounts × ' + fr(p[0], p[1]) + '</div><div class="sub">unit rate: ' + fr(b, a) + ' ' + c.bot + ' per ' + c.one + '</div>';
  /* table */
  var rows = [];
  for (k = 1; k <= 5; k++) rows.push([L.num(k * a), L.num(k * b), fr(b, a)]);
  tbl.set([c.top, c.bot, c.bot + ' per ' + c.one], rows);

  /* graph */
  var M = Math.max(6 * a, 6 * b, st.test ? Math.max(st.test[0], st.test[1]) : 0) * 1.08 + 1;
  L.setNiceView(g, GO, { xmin: -M / 30, xmax: M, ymin: -M / 30, ymax: M }, 8, 10); g.clear();
  g.line(0, 0, M, M * b / a, { color: 'ghost', width: 2, dash: '6 6' });
  for (k = 1; k <= KMAX; k++) g.dot(k * a, k * b, { color: 'blue', r: 6 });
  g.dot(topVal(), botVal(), { color: 'purple', r: 9, stroke: 'ink', strokeWidth: 2 });
  g.text(M * 0.02, M * 0.95, 'bottom', { size: 13, color: 'ink-soft' });
  g.text(M * 0.98, M * 0.03, 'top', { size: 13, color: 'ink-soft', anchor: 'end' });

  /* test pair */
  var t = st.test;
  if (!t) fb.set('Type a top and a bottom number to test whether they make an equivalent ratio.');
  else {
    var eqv = t[0] > 0 && t[1] > 0 && Math.abs(t[0] * b - t[1] * a) < 1e-9 * Math.max(1, t[0] * b);
    var sq = 12;
    L.s('rect', { x: g.X(t[0]) - sq / 2, y: g.Y(t[1]) - sq / 2, width: sq, height: sq, fill: eqv ? 'var(--green)' : 'var(--red)', stroke: 'var(--ink)', 'stroke-width': 2 }, g.top);
    if (t[0] === 0 && t[1] === 0) fb.set('0 : 0 has no amounts to compare. Try other numbers.', 'warn');
    else if (eqv) {
      fb.set('<b class="c-green">Equivalent.</b> ' + L.num(t[0]) + ' : ' + L.num(t[1]) + ' is ' + a + ' : ' + b + ' with both amounts multiplied by ' + L.nice(t[0] / a, 12, 3) + '. Its point is on the line.', 'good');
      if (t[0] > 20 && t[1] > 20) st.seen.big = true;
    } else {
      var fa = t[0] / a, fbv = t[1] / b;
      fb.set('<b class="c-red">Not equivalent.</b> To get ' + L.num(t[0]) + ' you multiply the top by ' + L.nice(fa, 12, 3) + ', but to get ' + L.num(t[1]) + ' you multiply the bottom by ' + L.nice(fbv, 12, 3) + '. Its point is off the line.', 'bad');
      var dA = t[0] - a, dB = t[1] - b;
      if (a !== b && Math.abs(dA - dB) < 1e-9 && Math.abs(dA) > 1e-9) st.seen.additive = true;
    }
  }
  if (Math.abs(topVal() - 1) < 1e-9) st.seen.unitTop = true;
  if (Math.abs(botVal() - 1) < 1e-9 && a !== b) st.seen.unitBot = true;
  ch.update();
});
draw();
