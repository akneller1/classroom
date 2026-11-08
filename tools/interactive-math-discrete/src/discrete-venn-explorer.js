/* Venn Diagram & Membership Table Explorer. Universe U = {1, 2, …, 20}; A = even numbers, B = multiples of 3, C = primes.
   Complements are taken relative to U. Operations: X′ (complement), ∩, ∪, − (difference), ⊕ (symmetric difference).
   Precedence: complement first, then ∩, then ∪, − and ⊕ from left to right (use parentheses to be clear).
   Each expression is computed as the set of Venn regions it contains (2ⁿ regions for n sets) and as a set of elements. */
var css = L.h('style', null, document.head);
css.textContent = '.vn-in{width:100%;min-height:44px;border:2px solid var(--ink);border-radius:8px;padding:6px 10px;font-size:1.15rem;font-weight:700;background:var(--card);color:var(--ink)}' +
  '.vn-lab{font-weight:700;display:block;margin:6px 0 4px}.vn-err{color:var(--red);font-weight:700;min-height:1.2em;font-size:.95rem}' +
  '.vn-keys,.vn-regs{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0}.vn-keys button{min-width:44px;min-height:44px;font-size:1.15rem}.vn-regs button{min-height:40px;font-size:.9rem}' +
  '.vn-regs button[aria-pressed="true"]{background:var(--purple);color:#fff;border-color:var(--purple)}.vn-res{font-size:1.02rem;line-height:1.6;margin:4px 0 8px}.vn-res b{font-family:var(--display)}' +
  '.vn-tbl td.y{color:var(--green);font-weight:700}.vn-tbl tr.diff td{background:var(--orange-tint)}';
var U = []; for (var i = 1; i <= 20; i++) U.push(i);
var DEF = { A: function (x) { return x % 2 === 0; }, B: function (x) { return x % 3 === 0; }, C: function (x) { return [2, 3, 5, 7, 11, 13, 17, 19].indexOf(x) >= 0; } };
var GEO = { 2: { A: [235, 210, 135], B: [405, 210, 135] }, 3: { A: [255, 170, 120], B: [385, 170, 120], C: [320, 280, 120] } };
var START = { k: 2, e1: "(A ∪ B)′", e2: "A′ ∪ B′", view: 'e1', mine: 0 };
var st = Object.assign({}, START), seen = {};
function names() { return st.k === 2 ? ['A', 'B'] : ['A', 'B', 'C']; }
function nreg() { return 1 << st.k; }
function inSet(r, S) { var idx = names().indexOf(S); return !!((r >> (st.k - 1 - idx)) & 1); }
function maskOf(S) { var m = 0; for (var r = 0; r < nreg(); r++) if (inSet(r, S)) m |= 1 << r; return m; }
function full() { return (1 << nreg()) - 1; }
function regionOf(x) { var r = 0; names().forEach(function (S) { r = r * 2 + (DEF[S](x) ? 1 : 0); }); return r; }
function regName(r) { var ins = names().filter(function (S) { return inSet(r, S); }), outs = names().filter(function (S) { return !inSet(r, S); });
  return ins.length === 0 ? 'outside ' + (st.k === 2 ? 'A and B' : 'all three') : ins.length === st.k ? 'in ' + ins.join(' and ') : 'in ' + ins.join(' and ') + ', not ' + outs.join(' or '); }

/* parser */
function parse(src) {
  var s = src.replace(/\s+/g, '').replace(/union/gi, '∪').replace(/intersect(ion)?/gi, '∩').replace(/xor|Δ/gi, '⊕').replace(/[|+u]/g, '∪').replace(/[&*^n]/g, '∩')
    .replace(/[\\−–-]/g, '−').replace(/['’ᶜ]/g, '′').replace(/Ø|∅|\{\}/g, '∅'), i = 0;
  if (!s) throw new Error('Type an expression.');
  function atom() {
    var c = s[i];
    if (c === '(') { i++; var e = low(); if (s[i] !== ')') throw new Error('Missing “)”.'); i++; return post(e); }
    if (c === 'U') { i++; return post(full()); }
    if (c === '∅') { i++; return post(0); }
    if (c === 'A' || c === 'B' || c === 'C') { if (names().indexOf(c) < 0) throw new Error('There is no set C in the two-set diagram.'); i++; return post(maskOf(c)); }
    throw new Error(c ? '“' + c + '” is not allowed here.' : 'The expression ends too early.');
  }
  function post(m) { while (s[i] === '′') { i++; m = full() & ~m; } return m; }
  function mid() { var l = atom(); while (s[i] === '∩') { i++; l = l & atom(); } return l; }
  function low() { var l = mid(); while (s[i] === '∪' || s[i] === '−' || s[i] === '⊕') { var o = s[i++], r = mid(); l = o === '∪' ? l | r : o === '−' ? l & ~r : l ^ r; } return l; }
  var m = low(); if (i < s.length) throw new Error(s[i] === ')' ? 'There is an extra “)”.' : 'Two sets need an operation between them.');
  return m & full();
}
function elems(m) { return U.filter(function (x) { return (m >> regionOf(x)) & 1; }); }
function roster(m) { var e = elems(m); return e.length ? '{' + e.join(', ') + '}' : '∅'; }

var kC = L.chips(P.panel, { label: 'Sets', value: 2, options: [{ value: 2, label: 'A and B' }, { value: 3, label: 'A, B and C' }], onChange: function (v) { st.k = v; st.mine = 0; build(); read(); draw(); } });
var last = null;
function field(id, label, val) {
  L.h('label', { class: 'vn-lab', for: id }, P.panel, label);
  var inp = L.h('input', { id: id, class: 'vn-in', type: 'text', value: val, autocomplete: 'off', spellcheck: 'false', 'aria-describedby': id + '-err' }, P.panel);
  var err = L.h('div', { id: id + '-err', class: 'vn-err', 'aria-live': 'polite' }, P.panel);
  inp.addEventListener('focus', function () { last = inp; });
  inp.addEventListener('input', function () { read(); draw(); });
  return { inp: inp, err: err };
}
var F1 = field('vn-e1', 'Expression 1', st.e1), F2 = field('vn-e2', 'Expression 2 (optional, to compare)', st.e2);
var keys = L.h('div', { class: 'vn-keys', role: 'group', 'aria-label': 'Insert a symbol' }, P.panel);
[['A', 'A'], ['B', 'B'], ['C', 'C'], ['U', 'universe U'], ['∪', 'union'], ['∩', 'intersection'], ['−', 'minus'], ['⊕', 'symmetric difference'], ['′', 'complement'], ['(', 'left parenthesis'], [')', 'right parenthesis'], ['∅', 'empty set']].forEach(function (k) {
  var b = L.h('button', { class: 'btn ghost', type: 'button', 'aria-label': 'Insert ' + k[1] }, keys, k[0]);
  b.addEventListener('mousedown', function (e) { e.preventDefault(); });
  b.addEventListener('click', function () { var f = last || F1.inp, a = f.selectionStart == null ? f.value.length : f.selectionStart, z = f.selectionEnd == null ? a : f.selectionEnd, t = '∪∩−⊕'.indexOf(k[0]) >= 0 ? ' ' + k[0] + ' ' : k[0]; f.value = f.value.slice(0, a) + t + f.value.slice(z); f.focus(); f.selectionStart = f.selectionEnd = a + t.length; read(); draw(); });
});
var viewC = L.chips(P.panel, { label: 'Shade on the diagram', value: st.view, options: [{ value: 'e1', label: 'Expression 1' }, { value: 'e2', label: 'Expression 2' }, { value: 'mine', label: 'My shading' }], onChange: function (v) { st.view = v; draw(); } });
L.h('span', { style: 'font-weight:700;display:block;margin-top:6px' }, P.panel, 'My shading: click a region on the diagram or press a button');
var regBox = L.h('div', { class: 'vn-regs', role: 'group', 'aria-label': 'Regions for my shading' }, P.panel), regBtns = [];
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.button(btns, 'Clear my shading', function () { st.mine = 0; draw(); }, true);
L.reset(btns, function () { st = Object.assign({}, START); F1.inp.value = st.e1; F2.inp.value = st.e2; kC.set(2, true); viewC.set('e1', true); build(); read(); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Shade A ∩ B′ yourself (click regions or use the buttons), then type it as Expression 1 to check your shading.', check: function () { return seen.shade; } },
  { text: 'De Morgan: make Expression 1 = (A ∪ B)′ and find an Expression 2 with ∩ and no ∪ that is equal to it.', check: function () { return seen.dm; } },
  { text: 'With three sets, shade the elements that are in <b>exactly one</b> of A, B and C. Which numbers are they?', check: function () { return seen.one; } },
  { text: 'Write the symmetric difference A ⊕ B (in A or B but not both) without using ⊕.', check: function () { return seen.sym; } },
  { text: 'With three sets, use the membership table to show A − (B ∪ C) = (A − B) ∩ (A − C).', check: function () { return seen.diff; } },
  { text: 'Type an expression whose elements are exactly {6, 12, 18}.', check: function () { return seen.six; } }
]);
L.notice(P.below, '<p><b>Universe.</b> U = {1, 2, …, 20}, A = even numbers, B = multiples of 3, C = primes. The complement X′ means everything in U that is not in X, so it depends on U.</p>' +
  '<p><b>Membership table.</b> Each row is one region of the diagram (a choice of in/out for each set). Two expressions name the same set exactly when their columns agree in every row. This is the set version of a truth table: ∪ ↔ or, ∩ ↔ and, ′ ↔ not.</p>' +
  '<p><b>Disproving an identity.</b> One region where the columns differ is enough; listing an element in that region gives a concrete counterexample. An identity that fails on this U could still hold “by accident” for particular sets, which is why the region test (all 2ⁿ rows) is the general check.</p>' +
  '<p>Typing tips: ’ or ′ for complement, u or + or | for ∪, n or & for ∩, - for −. Use parentheses: A − B ∪ C is read as (A − B) ∪ C.</p>');

var res = L.h('div', { class: 'vn-res', 'aria-live': 'polite' }, P.stage);
var W = 640, H = 420, svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Venn diagram' }, P.stage);
var tw = L.h('div', { class: 'vn-tbl' }, P.stage), tbl = L.table(tw);
var E1, E2;
function build() {
  regBox.innerHTML = ''; regBtns = [];
  for (var r = nreg() - 1; r >= 0; r--) (function (r) {
    var b = L.h('button', { class: 'btn ghost', type: 'button', 'aria-pressed': 'false' }, regBox, L.esc(regName(r)));
    b.addEventListener('click', function () { st.mine ^= 1 << r; st.view = 'mine'; viewC.set('mine', true); draw(); });
    regBtns[r] = b;
  })(r);
  F2.inp.placeholder = st.k === 3 ? 'for example (A − B) ∩ (A − C)' : 'for example A′ ∩ B′';
}
function read() {
  [[F1, 'e1'], [F2, 'e2']].forEach(function (z) {
    var v = z[0].inp.value.trim(); st[z[1]] = z[0].inp.value;
    if (!v) { z[0].err.textContent = ''; z[0].inp.removeAttribute('aria-invalid'); if (z[1] === 'e1') E1 = undefined; else E2 = null; return; }
    try { var m = parse(v); z[0].err.textContent = ''; z[0].inp.removeAttribute('aria-invalid'); if (z[1] === 'e1') E1 = m; else E2 = m; }
    catch (e) { z[0].err.textContent = e.message; z[0].inp.setAttribute('aria-invalid', 'true'); if (z[1] === 'e1') E1 = undefined; else E2 = undefined; }
  });
}
function inCircle(x, y, c) { return (x - c[0]) * (x - c[0]) + (y - c[1]) * (y - c[1]) <= c[2] * c[2]; }
function pointRegion(x, y) { var G = GEO[st.k], r = 0; names().forEach(function (S) { r = r * 2 + (inCircle(x, y, G[S]) ? 1 : 0); }); return r; }
svg.addEventListener('click', function (ev) { var q = L.svgPoint(svg, ev); if (q.x < 20 || q.x > W - 20 || q.y < 20 || q.y > H - 20) return; st.mine ^= 1 << pointRegion(q.x, q.y); st.view = 'mine'; viewC.set('mine', true); draw(); });
function places() { /* spread each region's elements over sample points inside it, away from the circle edges */
  var G = GEO[st.k], pts = {}, out = {};
  for (var y = 40; y < H - 30; y += 21) for (var x = 40; x < W - 30; x += 25) {
    var ok = names().every(function (S) { var c = G[S], d = Math.hypot(x - c[0], y - c[1]); return Math.abs(d - c[2]) > 13; });
    if (!ok) continue; var r = pointRegion(x, y); (pts[r] = pts[r] || []).push([x, y]);
  }
  for (var r = 0; r < nreg(); r++) {
    var es = U.filter(function (v) { return regionOf(v) === r; }), P0 = pts[r] || [];
    if (!es.length || !P0.length) continue;
    var cx = P0.reduce(function (s, p) { return s + p[0]; }, 0) / P0.length, cy = P0.reduce(function (s, p) { return s + p[1]; }, 0) / P0.length;
    if (r === 0) { cx = 70; cy = H / 2; }
    P0.sort(function (p, q) { return Math.hypot(p[0] - cx, p[1] - cy) - Math.hypot(q[0] - cx, q[1] - cy); });
    es.forEach(function (v, k) { out[v] = P0[Math.min(k, P0.length - 1)]; });
  }
  return out;
}
var draw = L.scheduler(function () {
  svg.innerHTML = '';
  var G = GEO[st.k], N = names(), defs = L.s('defs', null, svg);
  N.forEach(function (S) {
    var cp = L.s('clipPath', { id: 'vc' + S }, defs); L.s('circle', { cx: G[S][0], cy: G[S][1], r: G[S][2] }, cp);
    var mk = L.s('mask', { id: 'vm' + S }, defs); L.s('rect', { x: 0, y: 0, width: W, height: H, fill: '#fff' }, mk); L.s('circle', { cx: G[S][0], cy: G[S][1], r: G[S][2], fill: '#000' }, mk);
  });
  L.s('rect', { x: 20, y: 20, width: W - 40, height: H - 40, rx: 10, fill: 'var(--card)', stroke: 'var(--ink)', 'stroke-width': 2.5 }, svg);
  var m = st.view === 'e1' ? E1 : st.view === 'e2' ? E2 : st.mine, color = { e1: 'blue', e2: 'orange', mine: 'purple' }[st.view];
  if (m != null) for (var r = 0; r < nreg(); r++) if ((m >> r) & 1) {
    var g = svg;
    N.forEach(function (S) { g = L.s('g', inSet(r, S) ? { 'clip-path': 'url(#vc' + S + ')' } : { mask: 'url(#vm' + S + ')' }, g); });
    L.s('rect', { x: 20, y: 20, width: W - 40, height: H - 40, rx: 10, fill: 'var(--' + color + ')', 'fill-opacity': 0.42 }, g);
  }
  N.forEach(function (S) { var c = G[S]; L.s('circle', { cx: c[0], cy: c[1], r: c[2], fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2.5 }, svg); });
  var lab = { 2: { A: [130, 70], B: [510, 70] }, 3: { A: [140, 60], B: [500, 60], C: [470, 395] } }[st.k];
  N.forEach(function (S) { var t = L.s('text', { x: lab[S][0], y: lab[S][1], class: 'g-label', 'font-size': 22, 'font-weight': 800, 'text-anchor': 'middle' }, svg); t.textContent = S; });
  var tu = L.s('text', { x: 36, y: 44, class: 'g-label', 'font-size': 18, 'font-weight': 800 }, svg); tu.textContent = 'U';
  var pl = places();
  U.forEach(function (v) { var p = pl[v]; if (!p) return; var t = L.s('text', { x: p[0], y: p[1] + 5, class: 'g-label', 'font-size': 15, 'text-anchor': 'middle', 'font-weight': 700 }, svg); t.textContent = v; });
  svg.setAttribute('aria-label', 'Venn diagram of ' + N.join(', ') + ' in U = {1, …, 20}; shaded: ' + (m == null ? 'nothing' : roster(m)));
  regBtns.forEach(function (b, r) { if (b) b.setAttribute('aria-pressed', String(!!((st.mine >> r) & 1))); });
  /* results */
  var lines = [];
  if (E1 != null) lines.push('<b>Expression 1</b> = ' + roster(E1) + ' &nbsp; n = ' + elems(E1).length);
  if (E2 != null) lines.push('<b>Expression 2</b> = ' + roster(E2) + ' &nbsp; n = ' + elems(E2).length);
  lines.push('<b>My shading</b> = ' + roster(st.mine));
  res.innerHTML = lines.join('<br>');
  var rows = [], diff = [];
  for (var rr = nreg() - 1; rr >= 0; rr--) {
    var y = function (b) { return b == null ? '' : (b ? '<span class="y">∈</span>' : '∉'); };
    var a1 = E1 == null ? null : (E1 >> rr) & 1, a2 = E2 == null ? null : (E2 >> rr) & 1, mm = (st.mine >> rr) & 1;
    rows.push(N.map(function (S) { return inSet(rr, S) ? '∈' : '∉'; }).concat([y(a1), y(a2), y(mm), elems(1 << rr).join(', ') || '—']));
    diff.push(a1 != null && a2 != null && a1 !== a2);
  }
  tbl.set(N.concat(['Expr 1', 'Expr 2', 'Mine', 'elements']), rows);
  tw.querySelectorAll('tbody tr').forEach(function (tr, k) { tr.className = diff[k] ? 'diff' : ''; });
  if (E1 != null && E2 != null) {
    var eq = E1 === E2, rb = -1; for (var q = nreg() - 1; q >= 0; q--) if (((E1 ^ E2) >> q) & 1) { rb = q; break; }
    var ex = rb >= 0 ? elems(1 << rb) : [];
    fb.set(eq ? '<b>Equal sets:</b> the two expressions contain exactly the same regions, so they are equal for <i>any</i> sets A, B' + (st.k === 3 ? ', C' : '') + ', not just these.' :
      '<b>Not equal.</b> They differ in the region “' + regName(rb) + '”' + (ex.length ? ' (for example the element ' + ex[0] + ')' : ' (no element of this U lies there, but other sets could put one there)') + '.', eq ? 'good' : 'warn');
  } else if (E1 != null) fb.set(st.mine === E1 ? 'Your shading matches Expression 1.' : 'Shade regions to match Expression 1, or add Expression 2 to compare.', st.mine === E1 && st.mine ? 'good' : '');
  else fb.set('Fix Expression 1 to see it shaded.', 'warn');
  /* challenges */
  var nc = function (t) { return t.replace(/\s/g, ''); };
  var t1 = nc(st.e1), t2 = nc(st.e2);
  if (E1 != null && st.mine === E1 && E1 === (maskOf('A') & ~maskOf('B'))) seen.shade = true;
  var dmT = full() & ~(maskOf('A') | maskOf('B'));
  if (E1 === dmT && E2 === dmT && ((/∩|&|n/.test(t2) && !/∪|\||\+|u/.test(t2)) || (/∩|&|n/.test(t1) && !/∪|\||\+|u/.test(t1)))) seen.dm = true;
  if (st.k === 3) { var one = 0; for (var z = 0; z < 8; z++) if ([1, 2, 4].indexOf(z) >= 0) one |= 1 << z; if (st.mine === one) seen.one = true; }
  var sy = maskOf('A') ^ maskOf('B');
  if ((E1 === sy && !/⊕|Δ|xor/i.test(t1)) || (E2 === sy && !/⊕|Δ|xor/i.test(t2))) seen.sym = true;
  if (st.k === 3) { var dT = maskOf('A') & ~(maskOf('B') | maskOf('C')); if (E1 === dT && E2 === dT && /[−\-\\]/.test(t1) && /[−\-\\]/.test(t2) && t1 !== t2) seen.diff = true; }
  [E1, E2].forEach(function (E) { if (E != null && roster(E) === '{6, 12, 18}') seen.six = true; });
  ch.update();
});
build(); read(); draw();
