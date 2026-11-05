var PARENTS = {
  abs: { label: '|x|', f: function (x) { return Math.abs(x); }, name: function (u) { return '|' + u + '|'; }, key: [0, 0], keyName: 'vertex' },
  sq: { label: 'x²', f: function (x) { return x * x; }, name: function (u) { return '(' + u + ')²'; }, key: [0, 0], keyName: 'vertex' },
  sqrt: { label: '√x', f: function (x) { return x < 0 ? NaN : Math.sqrt(x); }, name: function (u) { return '√(' + u + ')'; }, key: [0, 0], keyName: 'starting point' },
  cube: { label: 'x³', f: function (x) { return x * x * x; }, name: function (u) { return '(' + u + ')³'; }, key: [0, 0], keyName: 'center point' },
  recip: { label: '1/x', f: function (x) { return Math.abs(x) < 1e-9 ? NaN : 1 / x; }, name: function (u) { return L.frac('1', u); }, key: [1, 1], keyName: 'point (1, 1)' },
  exp: { label: '2ˣ', f: function (x) { return Math.pow(2, x); }, name: function (u) { return '2<sup>' + u + '</sup>'; }, key: [0, 1], keyName: 'point (0, 1)' }
};
var st = { p: 'sq', a: 1, b: 1, h: 0, k: 0, seen: {} };
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -10, ymax: 10, width: 600, height: 600, label: 'Parent function and its transformation' });
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--ghost)"></i>parent function</span><span><i style="background:var(--blue)"></i>transformed function</span><span><i style="background:var(--orange)"></i>key point</span>');
L.chips(P.panel, { label: 'Parent function', value: st.p, options: Object.keys(PARENTS).map(function (k) { return { value: k, label: k === 'recip' ? L.frac(1, L.V('x')) : PARENTS[k].label.replace('x', L.V('x')) }; }), onChange: function (v) { st.p = v; draw(); } });
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
function f4(v) { return L.nice(v, 4); }
L.slider(P.panel, { id: 'a', label: 'a: vertical stretch / reflect over x-axis', min: -3, max: 3, step: 0.5, value: st.a, color: 'purple', format: f4, onInput: function (v) { st.a = v; draw(); } });
L.slider(P.panel, { id: 'b', label: 'b: horizontal stretch / reflect over y-axis', min: -3, max: 3, step: 0.5, value: st.b, color: 'blue', format: f4, onInput: function (v) { st.b = v; draw(); } });
L.slider(P.panel, { id: 'h', label: 'h: shift left or right', min: -8, max: 8, value: st.h, color: 'orange', format: L.num, onInput: function (v) { st.h = v; draw(); } });
L.slider(P.panel, { id: 'k', label: 'k: shift up or down', min: -8, max: 8, value: st.k, color: 'green', format: L.num, onInput: function (v) { st.k = v; draw(); } });
var desc = L.h('ul', { class: 'sub', style: 'margin:0;padding-left:20px' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Reflect any parent function over the <b>x-axis</b>.', check: function () { return st.seen.rx; } },
  { text: 'Reflect √' + L.V('x') + ' over the <b>y-axis</b>.', check: function () { return st.seen.ry; } },
  { text: 'Move √' + L.V('x') + ' so it starts at (−3, 2).', check: function () { return st.p === 'sqrt' && st.h === -3 && st.k === 2 && st.a > 0 && st.b > 0; } },
  { text: 'Move the asymptotes of ' + L.frac(1, L.V('x')) + ' to ' + L.V('x') + ' = 2 and ' + L.V('y') + ' = −1.', check: function () { return st.p === 'recip' && st.h === 2 && st.k === -1; } },
  { text: 'Use ' + L.V('a') + ' = −1 and ' + L.V('b') + ' = −1 on ' + L.V('x') + '³. Why does the graph look unchanged?', check: function () { return st.p === 'cube' && st.a === -1 && st.b === -1; } }
]);
function inner() {
  var b = st.b, h = st.h, x = L.V('x');
  var base = h ? '(' + x + (h > 0 ? ' − ' : ' + ') + Math.abs(h) + ')' : x;
  if (b === 1) return h ? base.slice(1, -1) : x;
  return (b === -1 ? '−' : f4(b)) + base;
}
var draw = L.scheduler(function () {
  var P0 = PARENTS[st.p], a = st.a, b = st.b, h = st.h, k = st.k;
  g.clear();
  g.fn(P0.f, { color: 'ghost', width: 3, dash: '8 6' });
  if (b === 0) { read.innerHTML = '<span class="c-red">' + L.V('b') + ' can\'t be 0: every input would become 0.</span>'; ch.update(); return; }
  var F = function (x) { return a * P0.f(b * (x - h)) + k; };
  if (st.p === 'recip') { g.line(h, -11, h, 11, { color: 'red', width: 2, dash: '6 6' }); g.line(-11, k, 11, k, { color: 'red', width: 2, dash: '6 6' }); }
  if (st.p === 'exp') g.line(-11, k, 11, k, { color: 'red', width: 2, dash: '6 6' });
  g.fn(F, { color: 'blue', samples: 900 });
  var kx = P0.key[0] / b + h, ky = a * P0.key[1] + k;
  g.dot(P0.key[0], P0.key[1], { color: 'ghost', r: 6 });
  if (Math.abs(kx) <= 10 && Math.abs(ky) <= 10) { g.dot(kx, ky, { color: 'orange', r: 8, stroke: 'ink', strokeWidth: 2 }); g.text(kx, ky, '(' + L.num(kx) + ', ' + L.num(ky) + ')', { dx: 12, dy: -10, color: 'orange' }); }
  var u = inner(), body = P0.name(u);
  read.innerHTML = L.V('f') + '(' + L.V('x') + ') = ' + (a === 1 ? '' : a === -1 ? '−' : f4(a)) + body + (k ? (k > 0 ? ' + ' : ' − ') + Math.abs(k) : '');
  var items = [];
  if (a < 0) items.push('reflected over the x-axis');
  if (Math.abs(a) > 1) items.push('stretched vertically by ' + L.num(Math.abs(a)));
  if (Math.abs(a) < 1) items.push('compressed vertically by ' + f4(Math.abs(a)));
  if (b < 0) items.push('reflected over the y-axis');
  if (Math.abs(b) > 1) items.push('compressed horizontally by a factor of ' + L.frac(1, L.num(Math.abs(b))));
  if (Math.abs(b) < 1) items.push('stretched horizontally by a factor of ' + f4(1 / Math.abs(b)));
  if (h) items.push('shifted ' + Math.abs(h) + ' ' + (h > 0 ? 'right' : 'left'));
  if (k) items.push('shifted ' + Math.abs(k) + ' ' + (k > 0 ? 'up' : 'down'));
  desc.innerHTML = (items.length ? items : ['no change: this is the parent function']).map(function (t) { return '<li>' + t + '</li>'; }).join('') + '<li>' + P0.keyName + ' (' + P0.key.join(', ') + ') moves to (' + L.nice(kx) + ', ' + L.nice(ky) + ')</li>';
  if (a < 0) st.seen.rx = true; if (st.p === 'sqrt' && b < 0) st.seen.ry = true;
  ch.update();
});
draw();
