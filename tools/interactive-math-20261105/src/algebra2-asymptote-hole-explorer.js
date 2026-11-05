/* f(x) = k · (x − n1)(x − n2) / ((x − d1)(x − d2)); each factor can be switched off. */
var st = { k: 1, n: [[true, -2], [false, 3]], d: [[true, 2], [false, -4]], seen: {} };
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -10, ymax: 10, width: 600, height: 600, label: 'Rational function' });
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>graph</span><span><i style="background:var(--red)"></i>asymptotes</span><span><i style="background:var(--green)"></i>' + L.V('x') + '-intercepts</span><span>○ hole</span>');
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
function factorControls(list, title, color) {
  L.h('h2', null, P.panel, title);
  list.forEach(function (f, i) {
    var box = L.h('div', { style: 'display:grid;grid-template-columns:auto 1fr;gap:10px;align-items:end' }, P.panel);
    var c = L.chips(box, { value: f[0], options: [{ value: true, label: 'on' }, { value: false, label: 'off' }], onChange: function (v) { f[0] = v; draw(); } });
    L.slider(box, { id: title.charAt(0) + i, label: 'factor (' + L.V('x') + ' − ?)', min: -6, max: 6, value: f[1], color: color, format: L.num, onInput: function (v) { f[1] = v; draw(); } });
  });
}
factorControls(st.n, 'Numerator factors', 'blue');
factorControls(st.d, 'Denominator factors', 'orange');
L.slider(P.panel, { id: 'k', label: 'Constant multiplier k', min: -4, max: 4, step: 0.5, value: st.k, color: 'purple', format: L.nice, onInput: function (v) { st.k = v; draw(); } });
var info = L.h('dl', { class: 'kv' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Make a <b>hole</b> at ' + L.V('x') + ' = 2.', check: function () { return st.seen.hole2; } },
  { text: 'Make <b>two</b> vertical asymptotes.', check: function () { return st.seen.va2; } },
  { text: 'Make the horizontal asymptote ' + L.V('y') + ' = 0.', check: function () { return st.seen.ha0; } },
  { text: 'Make the horizontal asymptote ' + L.V('y') + ' = 3.', check: function () { return st.seen.ha3; } },
  { text: 'Make a graph with <b>no</b> horizontal asymptote.', check: function () { return st.seen.noha; } }
]);
function fac(r) { return r === 0 ? L.V('x') : '(' + L.V('x') + (r > 0 ? ' − ' : ' + ') + Math.abs(r) + ')'; }
var draw = L.scheduler(function () {
  var N = st.n.filter(function (f) { return f[0]; }).map(function (f) { return f[1]; });
  var D = st.d.filter(function (f) { return f[0]; }).map(function (f) { return f[1]; });
  var k = st.k;
  // cancel common factors
  var n2 = N.slice(), d2 = [], holes = [];
  D.forEach(function (r) { var i = n2.indexOf(r); if (i >= 0) { n2.splice(i, 1); holes.push(r); } else d2.push(r); });
  var f = function (x) { var y = k; N.forEach(function (r) { y *= x - r; }); D.forEach(function (r) { y /= x - r; }); return y; };
  var fs = function (x) { var y = k; n2.forEach(function (r) { y *= x - r; }); d2.forEach(function (r) { y /= x - r; }); return y; };
  g.clear();
  if (k === 0) { read.innerHTML = '<span class="c-red">With ' + L.V('k') + ' = 0 the function is just 0.</span>'; info.innerHTML = ''; ch.update(); return; }
  var vas = d2.filter(function (r, i) { return d2.indexOf(r) === i; });
  vas.forEach(function (r) { g.line(r, -11, r, 11, { color: 'red', width: 2, dash: '8 6' }); });
  var dn = N.length, dd = D.length, ha = null;
  if (dn < dd) ha = 0; else if (dn === dd) ha = k;
  if (ha !== null) g.line(-11, ha, 11, ha, { color: 'red', width: 2, dash: '8 6' });
  g.fn(function (x) { return d2.some(function (r) { return Math.abs(x - r) < 1e-9; }) ? NaN : fs(x); }, { color: 'blue', samples: 1600 });
  holes.forEach(function (r) { var y = fs(r); if (isFinite(y) && Math.abs(y) <= 10) g.dot(r, y, { open: true, color: 'blue', r: 7 }); });
  var zeros = n2.filter(function (r, i) { return n2.indexOf(r) === i && d2.indexOf(r) < 0; });
  zeros.forEach(function (r) { g.dot(r, 0, { color: 'green', r: 7 }); });
  var top = N.length ? N.map(fac).join('') : '1', bot = D.length ? D.map(fac).join('') : '';
  read.innerHTML = L.V('f') + '(' + L.V('x') + ') = ' + (k === 1 ? '' : k === -1 ? '−' : L.nice(k)) + (bot ? L.frac(top, bot) : top);
  if (holes.indexOf(2) >= 0) st.seen.hole2 = true; if (vas.length >= 2) st.seen.va2 = true; if (ha === 0) st.seen.ha0 = true; if (ha === 3) st.seen.ha3 = true; if (ha === null) st.seen.noha = true;
  info.innerHTML = '<dt>Holes</dt><dd>' + (holes.length ? holes.map(function (r) { return '(' + r + ', ' + L.nice(fs(r)) + ') — the factor ' + fac(r) + ' cancels'; }).join('<br>') : 'none') + '</dd>' +
    '<dt>Vertical asymptotes</dt><dd>' + (vas.length ? vas.map(function (r) { return L.V('x') + ' = ' + r; }).join(', ') : 'none') + '</dd>' +
    '<dt>Horizontal asymptote</dt><dd>' + (ha === null ? 'none (top degree ' + dn + ' &gt; bottom degree ' + dd + ')' : L.V('y') + ' = ' + L.nice(ha) + ' (top degree ' + dn + (dn < dd ? ' &lt; ' : ' = ') + 'bottom degree ' + dd + ')') + '</dd>' +
    '<dt>' + L.V('x') + '-intercepts</dt><dd>' + (zeros.length ? zeros.map(function (r) { return '(' + r + ', 0)'; }).join(', ') : 'none') + '</dd>';
  ch.update();
});
draw();
