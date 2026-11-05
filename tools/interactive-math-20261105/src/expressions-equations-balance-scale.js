/* Each side is px + q. The hidden solution x* decides how the scale tips. */
var PRESETS = [
  { name: 'A', L: [2, 3], R: [0, 11] },
  { name: 'B', L: [3, -5], R: [0, 10] },
  { name: 'C', L: [5, 2], R: [2, 14] },
  { name: 'D', L: [6, -4], R: [2, 8] },
  { name: 'E', L: [2, 10], R: [2, 10] },
  { name: 'F', L: [3, 4], R: [3, -2] }
];
var st = { preset: 0, L: null, R: null, op: 'sub', amt: 3, kind: 'num', side: 'both', hist: [], tilted: false, solved: {}, identity: false, noSol: false };
function load(i) { st.preset = i; var p = PRESETS[i]; st.L = p.L.slice(); st.R = p.R.slice(); st.hist = []; st.steps = []; st.orig = { L: p.L.slice(), R: p.R.slice() }; draw(); }
function xstar() { var a = st.orig.L[0] - st.orig.R[0], b = st.orig.R[1] - st.orig.L[1]; return Math.abs(a) < 1e-12 ? 0 : b / a; }
function val(side, x) { return side[0] * x + side[1]; }
function ex(side) { return L.terms([[side[0], 'x'], [side[1], '']]); }

var W = 640, H = 420;
var svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Balance scale' }, P.stage);
var msg = L.h('p', { class: 'readout small', 'aria-live': 'polite', style: 'margin:8px 0 0' }, P.stage);
L.chips(P.panel, { label: 'Equation', value: 0, options: PRESETS.map(function (p, i) { return { value: i, label: p.name }; }), onChange: load });
var read = L.h('div', { class: 'readout' }, P.panel);
L.chips(P.panel, { label: 'Operation', value: st.op, options: [{ value: 'add', label: 'Add' }, { value: 'sub', label: 'Subtract' }, { value: 'mul', label: 'Multiply' }, { value: 'div', label: 'Divide' }], onChange: function (v) { st.op = v; } });
var kindChips = L.chips(P.panel, { label: 'What to use', value: st.kind, options: [{ value: 'num', label: 'a number' }, { value: 'x', label: 'x-terms' }], onChange: function (v) { st.kind = v; } });
L.slider(P.panel, { id: 'amount', label: 'Amount', min: 1, max: 12, value: st.amt, color: 'blue', format: L.num, onInput: function (v) { st.amt = v; } });
L.chips(P.panel, { label: 'Apply to', value: st.side, options: [{ value: 'both', label: 'Both sides' }, { value: 'L', label: 'Left only' }, { value: 'R', label: 'Right only' }], onChange: function (v) { st.side = v; } });
var row = L.h('div', { class: 'btn-row' }, P.panel);
L.button(row, 'Apply', apply);
L.button(row, 'Undo', function () { var h = st.hist.pop(); if (h) { st.L = h.L; st.R = h.R; st.steps.pop(); } draw(); }, true);
L.button(row, 'Start over', function () { load(st.preset); }, true);
var log = L.h('ol', { class: 'sub', style: 'margin:0;padding-left:20px;display:grid;gap:2px' }, P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Do an operation to <b>only one side</b>. What happens to the scale?', check: function () { return st.tilted; } },
  { text: 'Solve equation A: get ' + L.V('x') + ' alone on one side.', check: function () { return st.solved[0]; } },
  { text: 'Solve equation C, which has ' + L.V('x') + ' on both sides.', check: function () { return st.solved[2]; } },
  { text: 'In equation E, get rid of the ' + L.V('x') + '-terms. What is left, and is it true?', check: function () { return st.identity; } },
  { text: 'In equation F, get rid of the ' + L.V('x') + '-terms. What is left, and is it true?', check: function () { return st.noSol; } }
]);

function apply() {
  var k = st.amt, before = { L: st.L.slice(), R: st.R.slice() };
  if ((st.op === 'mul' || st.op === 'div') && st.kind === 'x') { msg.textContent = 'Multiply or divide by a number, not by x.'; return; }
  function f(side) {
    if (st.op === 'add') return st.kind === 'x' ? [side[0] + k, side[1]] : [side[0], side[1] + k];
    if (st.op === 'sub') return st.kind === 'x' ? [side[0] - k, side[1]] : [side[0], side[1] - k];
    if (st.op === 'mul') return [side[0] * k, side[1] * k];
    return [side[0] / k, side[1] / k];
  }
  if (st.side !== 'R') st.L = f(st.L);
  if (st.side !== 'L') st.R = f(st.R);
  st.hist.push(before);
  var word = { add: 'Add', sub: 'Subtract', mul: 'Multiply by', div: 'Divide by' }[st.op];
  var what = st.kind === 'x' ? (k === 1 ? '' : k) + 'x' : String(k);
  st.steps.push(word + ' ' + what + ' ' + (st.side === 'both' ? 'on both sides' : st.side === 'L' ? 'on the left only' : 'on the right only'));
  draw();
}
var draw = L.scheduler(function () {
  var x = xstar(), diff = val(st.L, x) - val(st.R, x);
  var noSolution = Math.abs(st.orig.L[0] - st.orig.R[0]) < 1e-12 && Math.abs(st.orig.L[1] - st.orig.R[1]) > 1e-12;
  var tilt = noSolution ? 0 : Math.max(-14, Math.min(14, diff * 2));
  if (!noSolution && Math.abs(diff) > 1e-9) st.tilted = true;
  svg.innerHTML = '';
  var cx = W / 2, cy = 150, arm = 195;
  L.s('path', { d: 'M ' + (cx - 70) + ' ' + (H - 20) + ' L ' + (cx + 70) + ' ' + (H - 20) + ' L ' + cx + ' ' + cy + ' Z', fill: 'var(--wash)', stroke: 'var(--ink)', 'stroke-width': 3, 'stroke-linejoin': 'round' }, svg);
  var gBeam = L.s('g', { transform: 'rotate(' + (-tilt) + ' ' + cx + ' ' + cy + ')', style: 'transition:transform .5s ease' }, svg);
  L.s('rect', { x: cx - arm - 10, y: cy - 7, width: 2 * arm + 20, height: 14, rx: 7, fill: 'var(--ink)' }, gBeam);
  L.s('circle', { cx: cx, cy: cy, r: 10, fill: 'var(--sun)', stroke: 'var(--ink)', 'stroke-width': 3 }, svg);
  [[-1, st.L], [1, st.R]].forEach(function (pr) {
    var px = cx + pr[0] * arm, py = cy + pr[0] * Math.sin(-tilt * Math.PI / 180) * arm;
    L.s('line', { x1: px, y1: py, x2: px - 82, y2: py + 90, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    L.s('line', { x1: px, y1: py, x2: px + 82, y2: py + 90, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    L.s('path', { d: 'M ' + (px - 104) + ' ' + (py + 90) + ' h 208 a 104 26 0 0 1 -208 0 z', fill: pr[0] < 0 ? 'var(--blue-tint)' : 'var(--orange-tint)', stroke: 'var(--ink)', 'stroke-width': 3 }, svg);
    var fo = L.s('foreignObject', { x: px - 104, y: py + 22, width: 208, height: 64 }, svg);
    var d = document.createElement('div'); d.style.cssText = 'height:100%;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700;color:var(--ink);text-align:center';
    d.innerHTML = ex(pr[1]); fo.appendChild(d);
  });
  read.innerHTML = ex(st.L) + ' = ' + ex(st.R);
  log.innerHTML = st.steps.length ? '' : '<li style="list-style:none;margin-left:-20px">Your steps will be listed here.</li>';
  st.steps.forEach(function (t) { L.h('li', null, log, t); });
  var noX = Math.abs(st.L[0]) < 1e-12 && Math.abs(st.R[0]) < 1e-12;
  var solvedL = Math.abs(st.L[0] - 1) < 1e-12 && Math.abs(st.L[1]) < 1e-12 && Math.abs(st.R[0]) < 1e-12;
  var solvedR = Math.abs(st.R[0] - 1) < 1e-12 && Math.abs(st.R[1]) < 1e-12 && Math.abs(st.L[0]) < 1e-12;
  if (noSolution) {
    msg.innerHTML = noX ? '<span class="c-red">' + ex(st.L) + ' = ' + ex(st.R) + ' is never true. This equation has <b>no solution</b>: no value of ' + L.V('x') + ' balances the scale.</span>' : 'No value of ' + L.V('x') + ' can balance this scale. Try to find out why.';
    if (noX) st.noSol = true;
  } else if (Math.abs(diff) > 1e-9) {
    msg.innerHTML = '<span class="c-red">The scale tipped. The two sides are no longer equal, so this is not the same equation any more.</span>';
  } else if (noX && Math.abs(st.orig.L[0] - st.orig.R[0]) < 1e-12) {
    msg.innerHTML = '<span class="c-green">' + ex(st.L) + ' = ' + ex(st.R) + ' is always true. <b>Every</b> value of ' + L.V('x') + ' works: infinitely many solutions.</span>'; st.identity = true;
  } else if (solvedL || solvedR) {
    var sol = solvedL ? st.R[1] : st.L[1];
    msg.innerHTML = '<span class="c-green"><b>Solved:</b> ' + L.V('x') + ' = ' + L.nice(sol) + '. Check it: put ' + L.nice(sol) + ' into the original equation.</span>';
    st.solved[st.preset] = true;
  } else msg.textContent = 'Balanced. Keep going until x is alone on one side.';
  ch.update();
});
load(0);
