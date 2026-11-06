var Gm = L.geo;
var REFL = { x: { label: 'x-axis', f: function (p) { return [p[0], -p[1]]; }, rule: '(x, −y)' }, y: { label: 'y-axis', f: function (p) { return [-p[0], p[1]]; }, rule: '(−x, y)' },
  yx: { label: 'y = x', f: function (p) { return [p[1], p[0]]; }, rule: '(y, x)' }, ynx: { label: 'y = −x', f: function (p) { return [-p[1], -p[0]]; }, rule: '(−y, −x)' } };
var ROT = { 90: { f: function (p) { return [-p[1], p[0]]; }, rule: '(−y, x)' }, 180: { f: function (p) { return [-p[0], -p[1]]; }, rule: '(−x, −y)' }, 270: { f: function (p) { return [p[1], -p[0]]; }, rule: '(y, −x)' } };
var st = { kind: 'translate', T: [[1, 1], [5, 2], [2, 5]], a: 2, b: 1, refl: 'y', rot: 90, k: 2, seen: {} };
var g = L.graph(P.stage, { xmin: -10, xmax: 10, ymin: -10, ymax: 10, width: 600, height: 600, label: 'Preimage and image' });
var gg = L.geoGraph(g);
L.h('div', { class: 'legend' }, P.stage, '<span><i style="background:var(--blue)"></i>preimage ABC (drag the corners)</span><span><i style="background:var(--orange)"></i>image A′B′C′</span>');
L.chips(P.panel, { label: 'Transformation', value: st.kind, options: [{ value: 'translate', label: 'Translate' }, { value: 'reflect', label: 'Reflect' }, { value: 'rotate', label: 'Rotate' }, { value: 'dilate', label: 'Dilate' }], onChange: function (v) { st.kind = v; build(); draw(); } });
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var ctrl = L.h('div', { style: 'display:grid;gap:12px' }, P.panel);
var tbl = L.table(P.panel);
var info = L.h('dl', { class: 'kv' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Apply the translation (' + L.V('x') + ', ' + L.V('y') + ') → (' + L.V('x') + ' + 3, ' + L.V('y') + ' − 2).', check: function () { return st.seen.tr; } },
  { text: 'Reflect over the line ' + L.V('y') + ' = ' + L.V('x') + '. What happens to each coordinate pair?', check: function () { return st.kind === 'reflect' && st.refl === 'yx'; } },
  { text: 'Rotate 180° about the origin.', check: function () { return st.kind === 'rotate' && st.rot === 180; } },
  { text: 'Find a transformation that reverses the order A → B → C (orientation).', check: function () { return st.seen.flip; } },
  { text: 'Find a transformation that is <b>not</b> a rigid motion.', check: function () { return st.seen.notRigid; } }
]);
function build() {
  ctrl.innerHTML = '';
  if (st.kind === 'translate') {
    L.slider(ctrl, { id: 'a', label: 'Horizontal shift a', min: -8, max: 8, value: st.a, color: 'orange', format: L.num, onInput: function (v) { st.a = v; draw(); } });
    L.slider(ctrl, { id: 'b', label: 'Vertical shift b', min: -8, max: 8, value: st.b, color: 'orange', format: L.num, onInput: function (v) { st.b = v; draw(); } });
  } else if (st.kind === 'reflect') L.chips(ctrl, { label: 'Line of reflection', value: st.refl, options: Object.keys(REFL).map(function (k) { return { value: k, label: REFL[k].label }; }), onChange: function (v) { st.refl = v; draw(); } });
  else if (st.kind === 'rotate') L.chips(ctrl, { label: 'Counterclockwise about the origin', value: st.rot, options: [90, 180, 270].map(function (d) { return { value: d, label: d + '°' }; }), onChange: function (v) { st.rot = v; draw(); } });
  else L.slider(ctrl, { id: 'k', label: 'Scale factor k (center at the origin)', min: 0.5, max: 3, step: 0.5, value: st.k, color: 'orange', format: L.nice, onInput: function (v) { st.k = v; draw(); } });
}
function sgnTerm(v, n) { return n ? (n > 0 ? ' + ' : ' − ') + Math.abs(n) : ''; }
var draw = L.scheduler(function () {
  var T = st.T, f, rule, rigid = true;
  if (st.kind === 'translate') { f = function (p) { return [p[0] + st.a, p[1] + st.b]; }; rule = '(' + L.V('x') + sgnTerm('x', st.a) + ', ' + L.V('y') + sgnTerm('y', st.b) + ')'; }
  else if (st.kind === 'reflect') { f = REFL[st.refl].f; rule = REFL[st.refl].rule.replace(/x/g, L.V('x')).replace(/y/g, L.V('y')); }
  else if (st.kind === 'rotate') { f = ROT[st.rot].f; rule = ROT[st.rot].rule.replace(/x/g, L.V('x')).replace(/y/g, L.V('y')); }
  else { f = function (p) { return [st.k * p[0], st.k * p[1]]; }; rule = '(' + L.nice(st.k) + L.V('x') + ', ' + L.nice(st.k) + L.V('y') + ')'; rigid = st.k === 1; }
  var I = T.map(f);
  g.clear();
  if (st.kind === 'reflect') { var lines = { x: [[-11, 0], [11, 0]], y: [[0, -11], [0, 11]], yx: [[-11, -11], [11, 11]], ynx: [[-11, 11], [11, -11]] }[st.refl]; g.line(lines[0][0], lines[0][1], lines[1][0], lines[1][1], { color: 'red', width: 3, dash: '10 6' }); T.forEach(function (p, i) { g.line(p[0], p[1], I[i][0], I[i][1], { color: 'ink-soft', width: 1.5, dash: '4 4' }); }); }
  if (st.kind === 'translate') T.forEach(function (p, i) { g.line(p[0], p[1], I[i][0], I[i][1], { color: 'ink-soft', width: 1.5, dash: '4 4' }); });
  if (st.kind === 'rotate') T.forEach(function (p, i) { g.line(0, 0, p[0], p[1], { color: 'ink-soft', width: 1.2, dash: '3 4' }); g.line(0, 0, I[i][0], I[i][1], { color: 'orange', width: 1.2, dash: '3 4' }); });
  if (st.kind === 'rotate' || st.kind === 'dilate') g.dot(0, 0, { color: 'red', r: 6 });
  gg.polygon(T, { stroke: 'blue', fill: 'blue', fillOpacity: 0.12 });
  gg.polygon(I, { stroke: 'orange', fill: 'orange', fillOpacity: 0.15 });
  var ci = [(I[0][0] + I[1][0] + I[2][0]) / 3, (I[0][1] + I[1][1] + I[2][1]) / 3];
  ['A′', 'B′', 'C′'].forEach(function (n, i) { gg.vertexLabel(I[i], ci, n, { color: 'orange' }); });
  ['A', 'B', 'C'].forEach(function (n, i) {
    g.handle(T[i][0], T[i][1], { color: 'blue', snap: 1, r: 9, label: 'Vertex ' + n, onDrag: function (x, y) { st.T[i] = [x, y]; draw(); } });
    g.text(T[i][0], T[i][1], n, { dx: 12, dy: -10, color: 'blue' });
  });
  var o1 = Math.sign(Gm.area(T)), o2 = Math.sign(Gm.area(I)), flipped = o1 !== o2;
  read.innerHTML = '(' + L.V('x') + ', ' + L.V('y') + ') → ' + rule;
  tbl.set(['Point', 'Preimage', 'Image'], T.map(function (p, i) { return ['ABC'.charAt(i), '(' + L.num(p[0]) + ', ' + L.num(p[1]) + ')', '(' + L.num(I[i][0]) + ', ' + L.num(I[i][1]) + ')']; }));
  info.innerHTML = '<dt>Rigid motion?</dt><dd>' + (rigid ? 'yes: lengths and angles are kept, so the image is congruent' : 'no: lengths change, so the image is similar, not congruent') + '</dd><dt>Orientation</dt><dd>' + (flipped ? '<span class="c-red">reversed</span> (A → B → C goes the other way around)' : 'kept') + '</dd>';
  if (st.kind === 'translate' && st.a === 3 && st.b === -2) st.seen.tr = true;
  if (flipped) st.seen.flip = true; if (!rigid) st.seen.notRigid = true;
  ch.update();
});
build(); draw();
