/* Graph Explorer: Euler, Hamilton & Trees. Undirected graphs; loops and parallel edges are allowed (a loop adds 2 to a degree).
   Euler (connected graph): every degree even ⇔ Euler circuit; exactly two odd degrees ⇔ Euler trail between them (route by Hierholzer).
   Hamiltonian cycle: exhaustive search over vertex orders (loops and repeated edges ignored), up to 10 vertices.
   Tree: connected with n − 1 edges. Chromatic number: smallest k with a proper coloring (backtracking); undefined with a loop.
   Kruskal: edges by weight (ties in list order), skipping any edge whose ends are already connected. */
var css = L.h('style', null, document.head);
css.textContent = '.gl-row{display:flex;flex-wrap:wrap;gap:8px;align-items:end;margin:6px 0}.gl-row label{font-weight:700;display:grid;gap:4px}.gl-row select{min-height:44px;min-width:64px;border:2px solid var(--ink);border-radius:8px;font-weight:700;font-size:1rem;background:var(--card);color:var(--ink)}' +
  '.gl-facts{display:grid;gap:6px;margin:6px 0 8px}.gl-facts div{padding:6px 10px;border-radius:8px;background:var(--wash)}.gl-facts .y{background:var(--green-tint)}.gl-facts .n{background:var(--red-tint)}' +
  '.gl-edges input{width:4.2em;min-height:36px;border:2px solid var(--ink);border-radius:6px;font-weight:700}.gl-edges button{min-height:36px}.gl-mode{font-size:.95rem;color:var(--ink-soft);margin:2px 0 6px}';
var LBL = 'ABCDEFGHIJKL', PAL = ['#fca5a5', '#93c5fd', '#86efac', '#fde047', '#f0abfc', '#fdba74'];
function ring(k, cx, cy, r, start) { var out = []; for (var i = 0; i < k; i++) { var t = (start == null ? -Math.PI / 2 : start) + 2 * Math.PI * i / k; out.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return out; }
function mk(pts, edges, w) { return { V: pts.map(function (p) { return { x: Math.round(p[0]), y: Math.round(p[1]) }; }), E: edges.map(function (e, i) { return { u: e[0], v: e[1], w: w ? w[i] : 1 }; }) }; }
var PRE = {
  konig: function () { return mk([[320, 70], [140, 220], [320, 370], [500, 220]], [[0, 1], [0, 1], [1, 2], [1, 2], [0, 3], [1, 3], [2, 3]]); },
  k4: function () { return mk(ring(4, 320, 220, 150, -Math.PI / 4), [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]); },
  k5: function () { var e = []; for (var i = 0; i < 5; i++) for (var j = i + 1; j < 5; j++) e.push([i, j]); return mk(ring(5, 320, 225, 160), e); },
  c5: function () { return mk(ring(5, 320, 225, 160), [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]]); },
  k33: function () { return mk([[170, 90], [320, 90], [470, 90], [170, 350], [320, 350], [470, 350]], [[0, 3], [0, 4], [0, 5], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5]]); },
  pete: function () { var p = ring(5, 320, 225, 180).concat(ring(5, 320, 225, 80)), e = []; for (var i = 0; i < 5; i++) { e.push([i, (i + 1) % 5]); e.push([i, i + 5]); e.push([5 + i, 5 + (i + 2) % 5]); } return mk(p, e); },
  bowtie: function () { return mk([[120, 100], [120, 340], [320, 220], [520, 100], [520, 340]], [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 2]]); },
  house: function () { return mk([[320, 60], [180, 180], [460, 180], [180, 370], [460, 370]], [[0, 1], [0, 2], [1, 2], [1, 3], [2, 4], [3, 4]]); },
  tree: function () { return mk([[320, 60], [180, 170], [460, 170], [100, 300], [260, 300], [460, 300], [460, 410]], [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [5, 6]]); },
  start: function () { return mk([[320, 60], [180, 180], [460, 180], [180, 370], [460, 370], [600, 300]], [[0, 1], [0, 2], [1, 2], [1, 3], [2, 4], [3, 4], [4, 5]]); },
  roads: function () { return mk([[90, 220], [320, 70], [320, 370], [550, 220], [550, 400]], [[0, 1], [0, 2], [1, 2], [1, 3], [2, 3], [2, 4], [3, 4]], [4, 2, 5, 10, 3, 8, 6]); }
};
var st = { V: [], E: [], mode: 'edge', sel: null, weighted: false, hl: 'none', kr: null, fromK: false, focus: null }, seen = {};
function loadPre(k) { var g = PRE[k](); st.V = g.V; st.E = g.E; st.sel = null; st.kr = null; st.fromK = k === 'konig'; st.weighted = k === 'roads'; wC.set(st.weighted ? 'on' : 'off', true); syncForm(); draw(); }

/* ---------- analysis ---------- */
function degs() { var d = st.V.map(function () { return 0; }); st.E.forEach(function (e) { d[e.u]++; d[e.v]++; }); return d; }
function comps() { var p = st.V.map(function (_, i) { return i; }); function f(x) { while (p[x] !== x) x = p[x] = p[p[x]]; return x; } st.E.forEach(function (e) { p[f(e.u)] = f(e.v); }); var s = {}; st.V.forEach(function (_, i) { s[f(i)] = 1; }); return Object.keys(s).length; }
function adj() { var n = st.V.length, A = []; for (var i = 0; i < n; i++) { A.push([]); for (var j = 0; j < n; j++) A[i].push(false); } st.E.forEach(function (e) { if (e.u !== e.v) { A[e.u][e.v] = A[e.v][e.u] = true; } }); return A; }
function euler() {
  var n = st.V.length, d = degs(), odd = [];
  d.forEach(function (x, i) { if (x % 2) odd.push(i); });
  if (!st.E.length) return { kind: 'none', odd: odd, why: 'there are no edges' };
  if (comps() > 1) return { kind: 'none', odd: odd, why: 'the graph is not connected' };
  if (odd.length !== 0 && odd.length !== 2) return { kind: 'none', odd: odd, why: odd.length + ' vertices have odd degree' };
  /* Hierholzer */
  var used = st.E.map(function () { return false; }), inc = st.V.map(function () { return []; });
  st.E.forEach(function (e, i) { inc[e.u].push(i); if (e.v !== e.u) inc[e.v].push(i); });
  var stack = [[odd.length ? odd[0] : st.E[0].u, -1]], route = [];
  while (stack.length) {
    var top = stack[stack.length - 1], v = top[0], next = -1;
    for (var k = 0; k < inc[v].length; k++) if (!used[inc[v][k]]) { next = inc[v][k]; break; }
    if (next < 0) { route.push(stack.pop()); continue; }
    used[next] = true; var e = st.E[next]; stack.push([e.u === v ? e.v : e.u, next]);
  }
  route.reverse();
  return { kind: odd.length ? 'trail' : 'circuit', odd: odd, verts: route.map(function (r) { return r[0]; }), edges: route.slice(1).map(function (r) { return r[1]; }) };
}
function hamilton() {
  var n = st.V.length; if (n < 3) return { ok: false, why: 'a Hamiltonian cycle needs at least 3 vertices' };
  if (n > 10) return { ok: null };
  var A = adj(), path = [0], usedV = [true], found = null;
  (function rec() {
    if (found) return;
    if (path.length === n) { if (A[path[n - 1]][0]) found = path.concat([0]); return; }
    for (var v = 1; v < n; v++) if (!usedV[v] && A[path[path.length - 1]][v]) { usedV[v] = true; path.push(v); rec(); path.pop(); usedV[v] = false; if (found) return; }
  })();
  return found ? { ok: true, cyc: found } : { ok: false, why: 'every possible order of the vertices was checked' };
}
function coloring() {
  var n = st.V.length; if (st.E.some(function (e) { return e.u === e.v; })) return null;
  if (!n) return { k: 0, c: [] };
  var A = adj(), order = st.V.map(function (_, i) { return i; }).sort(function (a, b) { return A[b].filter(Boolean).length - A[a].filter(Boolean).length; });
  for (var k = 1; k <= n; k++) {
    var c = st.V.map(function () { return -1; });
    var ok = (function rec(t) { if (t === n) return true; var v = order[t]; for (var col = 0; col < k; col++) { var fine = true; for (var u = 0; u < n; u++) if (A[v][u] && c[u] === col) { fine = false; break; } if (fine) { c[v] = col; if (rec(t + 1)) return true; c[v] = -1; } } return false; })(0);
    if (ok) return { k: k, c: c };
  }
}
function hasTriangle() { var A = adj(), n = st.V.length; for (var a = 0; a < n; a++) for (var b = a + 1; b < n; b++) if (A[a][b]) for (var c = b + 1; c < n; c++) if (A[a][c] && A[b][c]) return true; return false; }
function krStart() { var order = st.E.map(function (_, i) { return i; }).sort(function (a, b) { return st.E[a].w - st.E[b].w || a - b; }); st.kr = { order: order, i: 0, acc: [], skip: [], log: [] }; }
function krStep() {
  var K = st.kr; if (!K) { krStart(); K = st.kr; }
  if (K.i >= K.order.length) return;
  var p = st.V.map(function (_, i) { return i; }); function f(x) { while (p[x] !== x) x = p[x]; return x; }
  K.acc.forEach(function (j) { p[f(st.E[j].u)] = f(st.E[j].v); });
  var j = K.order[K.i++], e = st.E[j];
  if (f(e.u) === f(e.v)) { K.skip.push(j); K.log.push('skip ' + LBL[e.u] + LBL[e.v] + ' (' + e.w + '): ' + (e.u === e.v ? 'a loop' : 'it would make a cycle')); }
  else { K.acc.push(j); K.log.push('take ' + LBL[e.u] + LBL[e.v] + ' (' + e.w + ')'); }
  if (K.acc.length === st.V.length - comps()) K.i = K.order.length;
}

/* ---------- controls ---------- */
var preC = L.chips(P.panel, { label: 'Start from', value: null, options: [{ value: 'konig', label: 'Königsberg' }, { value: 'k4', label: 'K₄' }, { value: 'k5', label: 'K₅' }, { value: 'c5', label: 'C₅' }, { value: 'k33', label: 'K₃,₃' }, { value: 'pete', label: 'Petersen' }, { value: 'bowtie', label: 'Bowtie' }, { value: 'house', label: 'House' }, { value: 'tree', label: 'Tree' }, { value: 'roads', label: 'Road network (weighted)' }],
  onChange: function (v) { loadPre(v); } });
var modeC = L.chips(P.panel, { label: 'Clicking on the graph will…', value: st.mode, options: [{ value: 'vertex', label: 'Add a vertex' }, { value: 'edge', label: 'Add an edge' }, { value: 'move', label: 'Move a vertex' }, { value: 'delete', label: 'Delete' }], onChange: function (v) { st.mode = v; st.sel = null; draw(); } });
var modeHelp = L.h('div', { class: 'gl-mode', 'aria-live': 'polite' }, P.panel);
var form = L.h('div', { class: 'gl-row' }, P.panel);
function sel(label, id) { var l = L.h('label', null, form, label); return L.h('select', { id: id }, l); }
var fromS = sel('From', 'gl-from'), toS = sel('To', 'gl-to');
var wIn = L.numInput(form, { id: 'weight', label: 'Weight', min: 0, max: 999, step: 1, value: 1 });
L.button(form, 'Add edge', function () { addEdge(+fromS.value, +toS.value); });
var form2 = L.h('div', { class: 'btn-row' }, P.panel);
L.button(form2, 'Add vertex', function () { addVertex(null, null); }, true);
L.button(form2, 'Remove last edge', function () { if (st.E.length) { st.E.pop(); changed(); } }, true);
L.button(form2, 'Clear graph', function () { st.V = []; st.E = []; st.fromK = false; changed(); }, true);
var wC = L.chips(P.panel, { label: 'Edge weights', value: 'off', options: [{ value: 'off', label: 'Off' }, { value: 'on', label: 'On' }], onChange: function (v) { st.weighted = v === 'on'; st.kr = null; draw(); } });
var hlC = L.chips(P.panel, { label: 'Highlight', value: st.hl, options: [{ value: 'none', label: 'Nothing' }, { value: 'euler', label: 'Euler route' }, { value: 'ham', label: 'Hamiltonian cycle' }, { value: 'color', label: 'Coloring' }, { value: 'mst', label: 'Kruskal (MST)' }], onChange: function (v) { st.hl = v; if (v === 'mst' && !st.kr) krStart(); draw(); } });
var krRow = L.h('div', { class: 'btn-row' }, P.panel);
L.button(krRow, 'Kruskal: next edge', function () { if (!st.weighted) { wC.set('on'); } st.hl = 'mst'; hlC.set('mst', true); krStep(); draw(); });
L.button(krRow, 'Kruskal: finish', function () { if (!st.weighted) { wC.set('on'); } st.hl = 'mst'; hlC.set('mst', true); if (!st.kr) krStart(); while (st.kr.i < st.kr.order.length) krStep(); draw(); }, true);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st.mode = 'edge'; modeC.set('edge', true); st.hl = 'none'; hlC.set('none', true); preC.set(null, true); loadPre('start'); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Load Königsberg (4 land masses, 7 bridges). Add <b>one</b> bridge so that an Euler trail exists. Where must it go?', check: function () { return seen.konig; } },
  { text: 'Build a connected graph with at least 5 vertices that has an <b>Euler circuit</b> but <b>no Hamiltonian cycle</b>.', check: function () { return seen.eNotH; } },
  { text: 'Build a graph that has a <b>Hamiltonian cycle</b> but <b>no Euler circuit</b>.', check: function () { return seen.hNotE; } },
  { text: 'Build a graph with <b>no triangle</b> that still needs <b>3 colors</b>.', check: function () { return seen.col3; } },
  { text: 'Build a <b>tree</b> with 7 vertices and exactly <b>4 leaves</b>. How many edges does it have?', check: function () { return seen.tree; } },
  { text: 'Load the weighted road network and run Kruskal to the end. Which edges were skipped, and what is the total weight?', check: function () { return seen.mst; } }
]);
L.notice(P.below, '<p><b>Degrees.</b> Each edge adds 2 to the degree sum (a loop adds 2 to one vertex), so Σ deg = 2|E| and the number of odd-degree vertices is even.</p>' +
  '<p><b>Euler vs Hamilton.</b> An Euler circuit uses every <i>edge</i> exactly once; a connected graph has one exactly when every degree is even (exactly two odd vertices give an Euler trail from one to the other). A Hamiltonian cycle visits every <i>vertex</i> once; there is no simple test, so the tool searches every order (fine for small graphs, hopeless for large ones).</p>' +
  '<p><b>Walk, trail, path, circuit, cycle.</b> A trail repeats no edge; a path repeats no vertex; a circuit is a closed trail; a cycle is a circuit that repeats no vertex except the start.</p>' +
  '<p><b>Trees.</b> A connected graph with n vertices is a tree exactly when it has n − 1 edges; then every edge is a bridge. <b>Kruskal</b> picks the lightest remaining edge that does not close a cycle; it ends with n − 1 edges of minimum total weight.</p>' +
  '<p><b>Coloring.</b> χ(G) is the fewest colors with no edge joining two same-colored vertices. A triangle forces 3 colors, but so does any odd cycle.</p>');

var info = L.h('div', { class: 'gl-mode', 'aria-live': 'polite', style: 'font-size:1.02rem;color:var(--ink)' }, P.stage);
var W = 640, H = 440, svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Graph' }, P.stage);
var facts = L.h('div', { class: 'gl-facts', 'aria-live': 'polite' }, P.stage);
var ew = L.h('div', { class: 'gl-edges' }, P.stage), etbl = L.table(ew);
ew.addEventListener('click', function (e) { var b = e.target.closest('[data-del]'); if (b) { st.E.splice(+b.getAttribute('data-del'), 1); changed(); } });
ew.addEventListener('change', function (e) { var t = e.target; if (t.hasAttribute('data-w')) { var v = Math.max(0, Math.round(+t.value || 0)); st.E[+t.getAttribute('data-w')].w = v; st.kr = null; draw(); } });

function syncForm() {
  var opts = st.V.map(function (_, i) { return '<option value="' + i + '">' + LBL[i] + '</option>'; }).join('');
  var a = fromS.value, b = toS.value; fromS.innerHTML = opts; toS.innerHTML = opts;
  if (a !== '' && +a < st.V.length) fromS.value = a; if (b !== '' && +b < st.V.length) toS.value = b; else if (st.V.length > 1) toS.value = '1';
}
function changed() { st.kr = null; st.sel = null; syncForm(); draw(); }
function addVertex(x, y) {
  if (st.V.length >= 12) { fb.set('This tool allows at most 12 vertices.', 'warn'); return; }
  if (x == null) { var spots = ring(12, 320, 220, 175); for (var k = 0; k < 12; k++) { var s = spots[k]; if (st.V.every(function (v) { return Math.hypot(v.x - s[0], v.y - s[1]) > 50; })) { x = s[0]; y = s[1]; break; } } if (x == null) { x = 320; y = 220; } }
  st.V.push({ x: Math.round(x), y: Math.round(y) }); changed();
}
function addEdge(u, v) { if (!(u >= 0 && v >= 0 && u < st.V.length && v < st.V.length)) { fb.set('Add at least one vertex first.', 'warn'); return; } st.E.push({ u: u, v: v, w: Math.max(0, Math.round(wIn.get() || 1)) }); changed(); }
function vClick(i) {
  if (st.mode === 'edge') { if (st.sel == null) { st.sel = i; draw(); } else { var a = st.sel; st.sel = null; addEdge(a, i); } }
  else if (st.mode === 'delete') { st.E = st.E.filter(function (e) { return e.u !== i && e.v !== i; }).map(function (e) { return { u: e.u - (e.u > i), v: e.v - (e.v > i), w: e.w }; }); st.V.splice(i, 1); changed(); }
}
svg.addEventListener('click', function (ev) { if (st.mode !== 'vertex' || ev.target.closest('.gl-v')) return; var q = L.svgPoint(svg, ev); addVertex(Math.max(30, Math.min(W - 30, q.x)), Math.max(30, Math.min(H - 30, q.y))); });

var draw = L.scheduler(function () {
  var n = st.V.length, m = st.E.length, d = degs(), cc = n ? comps() : 0, eu = euler(), hm = hamilton(), co = coloring();
  var active = document.activeElement, fIdx = active && active.getAttribute && active.getAttribute('data-v');
  modeHelp.textContent = { vertex: 'Click an empty spot to add a vertex.', edge: st.sel == null ? 'Click a vertex, then another (or the same one for a loop). Or use the form below.' : 'Now click the second vertex for the edge from ' + LBL[st.sel] + '.', move: 'Drag a vertex, or focus it with Tab and use the arrow keys.', delete: 'Click a vertex or an edge to delete it.' }[st.mode];
  svg.innerHTML = '';
  var hlE = {}, hlV = {}, label = {};
  if (st.hl === 'euler' && eu.edges) eu.edges.forEach(function (j, k) { hlE[j] = 'var(--green)'; label[j] = String(k + 1); });
  if (st.hl === 'ham' && hm.ok) { for (var k = 0; k < hm.cyc.length - 1; k++) { var a = hm.cyc[k], b = hm.cyc[k + 1]; for (var j = 0; j < m; j++) { var e = st.E[j]; if (!hlE[j] && ((e.u === a && e.v === b) || (e.u === b && e.v === a))) { hlE[j] = 'var(--orange)'; break; } } } }
  if (st.hl === 'mst' && st.kr) { st.kr.acc.forEach(function (j) { hlE[j] = 'var(--blue)'; }); st.kr.skip.forEach(function (j) { hlE[j] = 'skip'; }); }
  /* edges, with parallel edges bent apart */
  var groups = {};
  st.E.forEach(function (e, j) { var key = Math.min(e.u, e.v) + '-' + Math.max(e.u, e.v); (groups[key] = groups[key] || []).push(j); });
  Object.keys(groups).forEach(function (key) {
    var js = groups[key], c = js.length;
    js.forEach(function (j, k) {
      var e = st.E[j], p = st.V[e.u], q = st.V[e.v], path, mx, my, col = hlE[j] && hlE[j] !== 'skip' ? hlE[j] : 'var(--ink)';
      if (e.u === e.v) { var rr = 18 + 9 * k; path = 'M' + p.x + ' ' + (p.y - 16) + ' a' + rr + ' ' + rr + ' 0 1 1 0.1 0'; mx = p.x; my = p.y - 16 - 2 * rr; path = 'M' + (p.x - 8) + ' ' + (p.y - 14) + ' C' + (p.x - 8 - rr) + ' ' + (p.y - 30 - 2 * rr) + ' ' + (p.x + 8 + rr) + ' ' + (p.y - 30 - 2 * rr) + ' ' + (p.x + 8) + ' ' + (p.y - 14); my = p.y - 22 - 1.5 * rr; }
      else { var off = (k - (c - 1) / 2) * 34, dx = q.x - p.x, dy = q.y - p.y, len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len, cx = (p.x + q.x) / 2 + nx * off * 2, cy = (p.y + q.y) / 2 + ny * off * 2; path = 'M' + p.x + ' ' + p.y + ' Q' + cx + ' ' + cy + ' ' + q.x + ' ' + q.y; mx = (p.x + q.x) / 2 + nx * off; my = (p.y + q.y) / 2 + ny * off; }
      L.s('path', { d: path, fill: 'none', stroke: col, 'stroke-width': hlE[j] && hlE[j] !== 'skip' ? 6 : 3, 'stroke-dasharray': hlE[j] === 'skip' ? '8 7' : null, opacity: hlE[j] === 'skip' ? 0.5 : 1, 'stroke-linecap': 'round' }, svg);
      var hit = L.s('path', { d: path, fill: 'none', stroke: 'transparent', 'stroke-width': 18, style: st.mode === 'delete' ? 'cursor:pointer' : null }, svg);
      hit.addEventListener('click', function (ev) { if (st.mode === 'delete') { ev.stopPropagation(); st.E.splice(j, 1); changed(); } });
      var tag = [st.weighted ? String(e.w) : '', label[j] ? '#' + label[j] : ''].filter(Boolean).join(' ');
      if (tag) { var t = L.s('text', { x: mx, y: my + 5, 'text-anchor': 'middle', class: 'g-label', 'font-size': 14, 'font-weight': 800, 'paint-order': 'stroke', stroke: 'var(--card)', 'stroke-width': 5 }, svg); t.textContent = tag; }
    });
  });
  st.V.forEach(function (v, i) {
    var fill = st.hl === 'color' && co ? PAL[co.c[i] % PAL.length] : st.sel === i ? 'var(--orange)' : 'var(--purple-tint)';
    var g = L.s('g', { class: 'gl-v', 'data-v': i, style: 'cursor:pointer' }, svg);
    L.s('circle', { cx: v.x, cy: v.y, r: 20, fill: fill, stroke: 'var(--ink)', 'stroke-width': 3 }, g);
    var t = L.s('text', { x: v.x, y: v.y + 6, 'text-anchor': 'middle', class: 'g-label', 'font-size': 17, 'font-weight': 800 }, g); t.textContent = LBL[i];
    var dt = L.s('text', { x: v.x > W - 90 ? v.x - 24 : v.x + 24, y: v.y - 18, 'text-anchor': v.x > W - 90 ? 'end' : 'start', class: 'g-label', 'font-size': 12, fill: 'var(--ink-soft)' }, g); dt.textContent = 'deg ' + d[i];
    L.drag(g, { svg: svg, label: 'vertex ' + LBL[i] + ', degree ' + d[i] + (st.sel === i ? ', selected' : ''),
      onMove: function (x, y) { if (st.mode !== 'move') return; v.x = Math.round(Math.max(24, Math.min(W - 24, x))); v.y = Math.round(Math.max(24, Math.min(H - 24, y))); draw(); },
      onKey: function (dx, dy, big) { if (st.mode !== 'move') { st.mode = 'move'; modeC.set('move', true); } var s = big ? 40 : 10; v.x = Math.max(24, Math.min(W - 24, v.x + dx * s)); v.y = Math.max(24, Math.min(H - 24, v.y - dy * s)); draw(); } });
    g.setAttribute('data-v', i);
    g.addEventListener('click', function (ev) { ev.stopPropagation(); vClick(i); });
    g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); vClick(i); } });
  });
  if (fIdx != null) { var el = svg.querySelector('[data-v="' + fIdx + '"]'); if (el) el.focus({ preventScroll: true }); }
  svg.setAttribute('aria-label', 'Graph with ' + n + ' vertices and ' + m + ' edges: ' + st.E.map(function (e) { return LBL[e.u] + LBL[e.v]; }).join(', '));
  info.innerHTML = '<b>' + n + '</b> vertices, <b>' + m + '</b> edges. Degrees: ' + (n ? st.V.map(function (_, i) { return LBL[i] + ' ' + d[i]; }).join(', ') : '—') + '. Sum = ' + d.reduce(function (s, x) { return s + x; }, 0) + ' = 2 × ' + m + '.';
  var isTree = n > 0 && cc === 1 && m === n - 1, leaves = d.filter(function (x) { return x === 1; }).length;
  var F = [];
  F.push([cc === 1, cc === 1 ? 'Connected.' : n ? 'Not connected: ' + cc + ' components.' : 'No vertices yet.']);
  F.push([eu.kind !== 'none', eu.kind === 'circuit' ? 'Euler circuit: every degree is even. Route: ' + eu.verts.map(function (v) { return LBL[v]; }).join('–') : eu.kind === 'trail' ? 'Euler trail (no circuit): exactly two odd vertices, ' + LBL[eu.odd[0]] + ' and ' + LBL[eu.odd[1]] + '. Route: ' + eu.verts.map(function (v) { return LBL[v]; }).join('–') : 'No Euler trail or circuit: ' + eu.why + '.']);
  F.push([hm.ok, hm.ok === null ? 'Hamiltonian cycle: too many vertices to search here (limit 10).' : hm.ok ? 'Hamiltonian cycle: ' + hm.cyc.map(function (v) { return LBL[v]; }).join('–') : 'No Hamiltonian cycle: ' + hm.why + '.']);
  F.push([isTree, isTree ? 'Tree: connected with ' + n + ' − 1 = ' + m + ' edges; ' + leaves + ' leaves.' : 'Not a tree' + (n ? (cc > 1 ? ' (not connected).' : m >= n ? ' (it has a cycle: ' + m + ' edges ≥ n = ' + n + ').' : '.') : '.')]);
  F.push([!!co, co ? 'Chromatic number χ = ' + co.k + (co.k === 2 ? ' (bipartite).' : '.') + (st.hl === 'color' ? ' Colors shown.' : ' Choose Highlight → Coloring to see one.') : 'No proper coloring: a loop joins a vertex to itself.']);
  facts.innerHTML = F.map(function (f) { return '<div class="' + (f[0] ? 'y' : 'n') + '">' + f[1] + '</div>'; }).join('');
  etbl.set(['Edge', st.weighted ? 'Weight' : 'Type', ''], st.E.map(function (e, j) { return [LBL[e.u] + '–' + LBL[e.v], st.weighted ? '<input type="number" min="0" max="999" step="1" value="' + e.w + '" data-w="' + j + '" aria-label="weight of edge ' + LBL[e.u] + LBL[e.v] + '">' : e.u === e.v ? 'loop' : groups[Math.min(e.u, e.v) + '-' + Math.max(e.u, e.v)].length > 1 ? 'parallel' : '', '<button class="btn ghost" type="button" data-del="' + j + '" aria-label="delete edge ' + LBL[e.u] + LBL[e.v] + '">Delete</button>']; }));
  if (st.hl === 'mst') {
    var K = st.kr, tw = K ? K.acc.reduce(function (s, j) { return s + st.E[j].w; }, 0) : 0, done = K && K.i >= K.order.length;
    fb.set(!st.weighted ? 'Turn edge weights on for Kruskal.' : !K || !K.log.length ? 'Press <b>Kruskal: next edge</b>. Edges are tried from lightest to heaviest.' :
      K.log.join('; ') + '. ' + (done ? '<b>Done</b>: ' + K.acc.length + ' edges, total weight <b>' + tw + '</b>' + (cc > 1 ? ' (a spanning forest: the graph is not connected).' : '.') : 'Total so far ' + tw + '.'), done ? 'good' : '');
    if (done && cc === 1 && n >= 5 && st.weighted && K.skip.length) seen.mst = true;
  } else if (st.hl === 'ham' && hm.ok === false) fb.set('No Hamiltonian cycle to highlight.', 'warn');
  else if (st.hl === 'euler' && eu.kind === 'none') fb.set('No Euler route to highlight.', 'warn');
  else fb.set(st.hl === 'euler' ? 'Green numbers give the order of the edges in the Euler route.' : 'Build or load a graph and watch the facts update.', '');
  /* challenges */
  var odd = d.filter(function (x) { return x % 2; }).length;
  if (st.fromK && n === 4 && m === 8 && cc === 1 && odd === 2) seen.konig = true;
  if (cc === 1 && n >= 5 && eu.kind === 'circuit' && hm.ok === false) seen.eNotH = true;
  if (hm.ok && eu.kind !== 'circuit') seen.hNotE = true;
  if (co && co.k === 3 && !hasTriangle()) seen.col3 = true;
  if (isTree && n === 7 && leaves === 4) seen.tree = true;
  ch.update();
});
loadPre('start');
