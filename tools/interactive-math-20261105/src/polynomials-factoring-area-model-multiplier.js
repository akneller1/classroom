var st = { a: 1, b: 1, c: 1, d: 4, seen: {} };
var W = 640, H = 560, XL = 104, U = 21;
var svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Area model rectangle' }, P.stage);
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>' + L.V('x') + '² pieces</span><span><i style="background:var(--green)"></i>' + L.V('x') + ' pieces</span><span><i style="background:var(--orange)"></i>number pieces</span><span><i style="background:var(--red)"></i>negative pieces</span>');
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
L.h('h2', null, P.panel, 'First factor (across the top)');
var sa = L.slider(P.panel, { id: 'a', label: 'x-coefficient', min: 1, max: 3, value: st.a, color: 'blue', format: L.num, onInput: function (v) { st.a = v; draw(); } });
var sb = L.slider(P.panel, { id: 'b', label: 'constant', min: -6, max: 6, value: st.b, color: 'orange', format: L.num, onInput: function (v) { st.b = v; draw(); } });
L.h('h2', null, P.panel, 'Second factor (down the side)');
var sc = L.slider(P.panel, { id: 'c', label: 'x-coefficient', min: 1, max: 3, value: st.c, color: 'blue', format: L.num, onInput: function (v) { st.c = v; draw(); } });
var sd = L.slider(P.panel, { id: 'd', label: 'constant', min: -6, max: 6, value: st.d, color: 'orange', format: L.num, onInput: function (v) { st.d = v; draw(); } });
var row = L.h('div', { class: 'btn-row' }, P.panel);
L.button(row, 'Square the first factor', function () { sc.set(st.a, true); sd.set(st.b, true); st.c = st.a; st.d = st.b; draw(); }, true);
var ch = L.challenges(P.panel, [
  { text: 'Build (' + L.V('x') + ' + 2)(' + L.V('x') + ' + 3).', check: function () { return st.seen.b23; } },
  { text: 'Build (' + L.V('x') + ' + 3)². Is it ' + L.V('x') + '² + 9?', check: function () { return st.a === 1 && st.c === 1 && st.b === 3 && st.d === 3; } },
  { text: 'Make the middle term disappear. What do the factors have in common?', check: function () { return st.seen.mid0; } },
  { text: 'Make a product whose constant term is negative.', check: function () { return st.b * st.d < 0; } },
  { text: 'Make a product that starts with 6' + L.V('x') + '².', check: function () { return st.a * st.c === 6; } }
]);
function bin(a, b) { return '(' + L.terms([[a, 'x'], [b, '']]) + ')'; }
function txt(x, y, s, o) { o = o || {}; var t = L.s('text', { x: x, y: y, 'text-anchor': o.anchor || 'middle', class: 'g-label', 'font-size': o.size || 16, fill: o.color || null }, svg); t.textContent = s; return t; }
function cell(x, y, w, h, kind, neg) {
  var fill = neg ? 'var(--red-tint)' : kind === 'x2' ? 'var(--blue-tint)' : kind === 'x' ? 'var(--green-tint)' : 'var(--orange-tint)';
  L.s('rect', { x: x + 1, y: y + 1, width: w - 2, height: h - 2, rx: 3, fill: fill, stroke: neg ? 'var(--red)' : 'var(--ink)', 'stroke-width': 1.5 }, svg);
}
var draw = L.scheduler(function () {
  var a = st.a, b = st.b, c = st.c, d = st.d;
  svg.innerHTML = '';
  var ox = 90, oy = 70, wTop = a * XL + Math.abs(b) * U, hSide = c * XL + Math.abs(d) * U;
  var sc2 = Math.min(1.6, (W - ox - 30) / wTop, (H - oy - 30) / hSide);
  var g = L.s('g', { transform: 'translate(' + ox + ' ' + oy + ') scale(' + sc2 + ')' }, svg);
  var save = svg; svg = g;
  var i, j;
  // column pieces across the top: a x-lengths then |b| units; row pieces down: c x-lengths then |d| units
  var cols = [], rows = [];
  for (i = 0; i < a; i++) cols.push(['x', XL, false]); for (i = 0; i < Math.abs(b); i++) cols.push(['1', U, b < 0]);
  for (i = 0; i < c; i++) rows.push(['x', XL, false]); for (i = 0; i < Math.abs(d); i++) rows.push(['1', U, d < 0]);
  var yy = 0;
  rows.forEach(function (r) {
    var xx = 0;
    cols.forEach(function (k) {
      var kind = r[0] === 'x' && k[0] === 'x' ? 'x2' : r[0] === '1' && k[0] === '1' ? 'one' : 'x';
      cell(xx, yy, k[1], r[1], kind, r[2] !== k[2]);
      xx += k[1];
    });
    yy += r[1];
  });
  L.s('rect', { x: 0, y: 0, width: wTop, height: hSide, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 4 / sc2 }, g);
  svg = save;
  // edge labels
  var xx2 = ox;
  cols.forEach(function (k) { txt(xx2 + k[1] * sc2 / 2, oy - 14, k[0] === 'x' ? 'x' : (k[2] ? '−1' : '1'), { size: k[0] === 'x' ? 18 : 12, color: k[2] ? 'var(--red)' : null }); xx2 += k[1] * sc2; });
  var yy2 = oy;
  rows.forEach(function (r) { txt(ox - 16, yy2 + r[1] * sc2 / 2 + 5, r[0] === 'x' ? 'x' : (r[2] ? '−1' : '1'), { size: r[0] === 'x' ? 18 : 12, color: r[2] ? 'var(--red)' : null, anchor: 'end' }); yy2 += r[1] * sc2; });
  txt(ox + wTop * sc2 / 2, 26, bin(a, b).replace(/<[^>]+>/g, ''), { size: 20, color: 'var(--blue)' });
  var A2 = a * c, Bx = a * d + b * c, C0 = b * d;
  if (st.a === 1 && st.b === 2 && st.c === 1 && st.d === 3 || st.a === 1 && st.b === 3 && st.c === 1 && st.d === 2) st.seen.b23 = true;
  if (Bx === 0) st.seen.mid0 = true;
  read.innerHTML = bin(a, b) + bin(c, d) + '<div class="sub" style="margin:8px 0 4px">Pieces: <span class="c-blue">' + L.terms([[A2, 'x²']]) + '</span> &nbsp; <span class="c-green">' + L.terms([[a * d, 'x']]) + ' and ' + L.terms([[b * c, 'x']]) + '</span> &nbsp; <span class="c-orange">' + L.num(C0) + '</span></div>' +
    '= ' + L.terms([[A2, 'x²'], [a * d, 'x'], [b * c, 'x'], [C0, '']]).replace(/(\+|−) 0<span class="v">x<\/span>/, '') + '<br>= <b>' + L.terms([[A2, 'x²'], [Bx, 'x'], [C0, '']]) + '</b>';
  ch.update();
});
draw();
