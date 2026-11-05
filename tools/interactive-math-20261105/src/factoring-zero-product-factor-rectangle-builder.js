var TARGETS = [[5, 6], [7, 12], [-1, -6], [-8, 15], [2, -8], [6, 9], [0, -9], [1, 1]];
var st = { t: 0, p: 1, q: 1, solved: {}, prime: false };
var W = 600, H = 440, XL = 120, U = 22;
var svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Factor rectangle' }, P.stage);
var msg = L.h('p', { class: 'readout small', 'aria-live': 'polite', style: 'margin:8px 0 0' }, P.stage);
L.chips(P.panel, { label: 'Trinomial to factor', value: 0, options: TARGETS.map(function (t, i) { return { value: i, label: String(i + 1) }; }), onChange: function (v) { st.t = v; st.prime = false; draw(); } });
var read = L.h('div', { class: 'readout' }, P.panel);
var sp = L.slider(P.panel, { id: 'p', label: 'First factor: (x + ?)', min: -9, max: 9, value: st.p, color: 'blue', format: L.num, onInput: function (v) { st.p = v; st.prime = false; draw(); } });
var sq = L.slider(P.panel, { id: 'q', label: 'Second factor: (x + ?)', min: -9, max: 9, value: st.q, color: 'orange', format: L.num, onInput: function (v) { st.q = v; st.prime = false; draw(); } });
var row = L.h('div', { class: 'btn-row' }, P.panel);
L.button(row, 'No rectangle works', function () { st.prime = true; draw(); }, true);
L.h('h2', null, P.panel, 'Graph of the trinomial');
var g = L.graph(P.panel, { xmin: -10, xmax: 10, ymin: -20, ymax: 20, width: 400, height: 300, ystep: 5, ylabelStep: 10, xlabelStep: 2, label: 'Graph of the trinomial' });
var ch = L.challenges(P.panel, [
  { text: 'Factor trinomial 1.', check: function () { return st.solved[0]; } },
  { text: 'Factor a trinomial with a <b>negative</b> constant (3 or 5).', check: function () { return st.solved[2] || st.solved[4]; } },
  { text: 'Factor trinomial 6. What is special about its rectangle?', check: function () { return st.solved[5]; } },
  { text: 'Factor trinomial 7, which has no ' + L.V('x') + '-term.', check: function () { return st.solved[6]; } },
  { text: 'Decide whether trinomial 8 can be factored.', check: function () { return st.solved[7]; } }
]);
function tri(b, c) { return L.terms([[1, 'x²'], [b, 'x'], [c, '']]); }
function bin(p) { return '(' + L.terms([[1, 'x'], [p, '']]) + ')'; }
function factorable(b, c) { var disc = b * b - 4 * c; if (disc < 0) return false; var r = Math.round(Math.sqrt(disc)); return r * r === disc; }
var draw = L.scheduler(function () {
  var T = TARGETS[st.t], b = T[0], c = T[1], p = st.p, q = st.q;
  var pb = p + q, pc = p * q, ok = pb === b && pc === c;
  if (ok) st.solved[st.t] = true;
  if (st.prime && !factorable(b, c)) st.solved[st.t] = true;
  svg.innerHTML = '';
  var ox = 70, oy = 50, w = XL + Math.abs(p) * U, h = XL + Math.abs(q) * U, s = Math.min(1.5, (W - ox - 20) / w, (H - oy - 20) / h);
  var gg = L.s('g', { transform: 'translate(' + ox + ' ' + oy + ') scale(' + s + ')' }, svg);
  function cell(x, y, cw, chh, kind, neg) { L.s('rect', { x: x + 1, y: y + 1, width: cw - 2, height: chh - 2, rx: 3, fill: neg ? 'var(--red-tint)' : kind === 'x2' ? 'var(--blue-tint)' : kind === 'x' ? 'var(--green-tint)' : 'var(--orange-tint)', stroke: neg ? 'var(--red)' : 'var(--ink)', 'stroke-width': 1.5 }, gg); }
  var cols = [['x', XL, false]], rows = [['x', XL, false]], i;
  for (i = 0; i < Math.abs(p); i++) cols.push(['1', U, p < 0]);
  for (i = 0; i < Math.abs(q); i++) rows.push(['1', U, q < 0]);
  var yy = 0; rows.forEach(function (r) { var xx = 0; cols.forEach(function (k) { cell(xx, yy, k[1], r[1], r[0] === 'x' && k[0] === 'x' ? 'x2' : r[0] === '1' && k[0] === '1' ? 'one' : 'x', r[2] !== k[2]); xx += k[1]; }); yy += r[1]; });
  L.s('rect', { x: 0, y: 0, width: w, height: h, fill: 'none', stroke: ok ? 'var(--green)' : 'var(--ink)', 'stroke-width': (ok ? 7 : 4) / s }, gg);
  var t1 = L.s('text', { x: ox + w * s / 2, y: 32, 'text-anchor': 'middle', class: 'g-label', 'font-size': 20, fill: 'var(--blue)' }, svg); t1.textContent = bin(p).replace(/<[^>]+>/g, '');
  var t2 = L.s('text', { x: ox - 12, y: oy + h * s / 2, 'text-anchor': 'end', class: 'g-label', 'font-size': 20, fill: 'var(--orange)' }, svg); t2.textContent = bin(q).replace(/<[^>]+>/g, '');
  function mark(good) { return good ? ' <b class="c-green">✓</b>' : ' <b class="c-red">✗</b>'; }
  read.innerHTML = '<div class="sub">Factor</div>' + tri(b, c) + '<div class="sub" style="margin-top:8px">Your rectangle</div>' + bin(p) + bin(q) + ' = ' + tri(pb, pc) +
    '<div class="sub" style="margin-top:6px">middle term: ' + L.num(pb) + mark(pb === b) + ' (add) &nbsp; constant: ' + L.num(pc) + mark(pc === c) + ' (multiply)</div>';
  if (ok) msg.innerHTML = '<span class="c-green"><b>Factored!</b> ' + tri(b, c) + ' = ' + bin(p) + bin(q) + '. Set each factor to 0: ' + L.V('x') + ' = ' + L.num(-p) + ' or ' + L.V('x') + ' = ' + L.num(-q) + '. Those are the ' + L.V('x') + '-intercepts.</span>';
  else if (st.prime) msg.innerHTML = factorable(b, c) ? '<span class="c-red">This one does factor. Find two numbers that multiply to ' + L.num(c) + ' and add to ' + L.num(b) + '.</span>' : '<span class="c-green"><b>Right:</b> no two integers multiply to ' + L.num(c) + ' and add to ' + L.num(b) + '. The graph never crosses the ' + L.V('x') + '-axis.</span>';
  else msg.innerHTML = 'Find two numbers that <b>multiply</b> to ' + L.num(c) + ' and <b>add</b> to ' + L.num(b) + '.';
  g.clear();
  g.fn(function (x) { return x * x + b * x + c; }, { color: 'purple' });
  if (ok) [-p, -q].forEach(function (z) { g.dot(z, 0, { color: 'green', r: 8 }); g.text(z, 0, L.num(z), { dx: 6, dy: -12, color: 'green' }); });
  ch.update();
});
draw();
