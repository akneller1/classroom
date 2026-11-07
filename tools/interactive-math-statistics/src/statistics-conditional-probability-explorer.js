/* Screening tests. prevalence = P(C), sensitivity = P(+ | C), specificity = P(− | not C).
   P(C | +) = P(C)·sens / [P(C)·sens + P(not C)·(1 − spec)] (Bayes). Counts are expected counts out of 100,000, rounded to whole people;
   probabilities use the exact rates. */
var PREV = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 30, 50];
var CTX = { med: { cond: 'has the condition', no: 'does not have it', pos: 'tests positive', neg: 'tests negative', C: 'condition', short: 'C' },
            spam: { cond: 'is spam', no: 'is not spam', pos: 'is flagged', neg: 'is not flagged', C: 'spam', short: 'spam' } };
var st = { ctx: 'med', pi: 6, sens: 90, spec: 90, seen: {} };
function q() { var p = PREV[st.pi] / 100, se = st.sens / 100, sp = st.spec / 100;
  var tp = p * se, fn = p * (1 - se), fp = (1 - p) * (1 - sp), tn = (1 - p) * sp, pos = tp + fp, neg = fn + tn;
  return { p: p, se: se, sp: sp, tp: tp, fn: fn, fp: fp, tn: tn, pos: pos, neg: neg, ppv: pos ? tp / pos : NaN, npv: neg ? tn / neg : NaN, cneg: neg ? fn / neg : NaN }; }
function c(x) { return Math.round(x * 100000).toLocaleString(); }
function pct(x) { return isNaN(x) ? 'undefined' : L.num(100 * x, x < 0.001 ? 3 : 1) + '%'; }
L.chips(P.panel, { label: 'Situation', value: st.ctx, options: [{ value: 'med', label: 'Medical screening' }, { value: 'spam', label: 'Spam filter' }], onChange: function (v) { st.ctx = v; draw(); } });
var read = L.h('div', { class: 'readout', 'aria-live': 'polite' }, P.panel);
var sP = L.slider(P.panel, { id: 'prevalence', label: 'Prevalence: P(condition)', min: 0, max: PREV.length - 1, value: st.pi, color: 'purple', format: function (i) { return PREV[i] + '%'; }, onInput: function (i) { st.pi = i; draw(); } });
var sS = L.slider(P.panel, { id: 'sensitivity', label: 'Sensitivity: P(positive | condition)', min: 50, max: 100, step: 0.5, value: st.sens, color: 'green', format: function (v) { return v + '%'; }, onInput: function (v) { st.sens = v; draw(); } });
var sQ = L.slider(P.panel, { id: 'specificity', label: 'Specificity: P(negative | no condition)', min: 50, max: 100, step: 0.5, value: st.spec, color: 'blue', format: function (v) { return v + '%'; }, onInput: function (v) { st.spec = v; draw(); } });
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st.pi = 6; st.sens = 90; st.spec = 90; sP.set(6, true); sS.set(90, true); sQ.set(90, true); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Predict first: a test is 99% sensitive and 99% specific, and 1% of people have the condition. If you test positive, what is the chance you have it? Then set it up and check.', check: function () { return st.seen.classic; } },
  { text: 'Keep the 99%/99% test. Change only the prevalence until a positive result means at least a 90% chance of the condition.', check: function () { return st.seen.prev90; } },
  { text: 'Find settings where P(positive | condition) is at least 95% but P(condition | positive) is below 20%.', check: function () { return st.seen.swap; } },
  { text: 'With prevalence 5%, improve the 99%/99% test until P(condition | positive) is at least 90%. Which slider mattered, sensitivity or specificity? Why?', check: function () { return st.seen.which; } },
  { text: 'Make the test useless: testing positive is equally likely with or without the condition. What does that say about independence?', check: function () { return st.seen.indep; } }
]);
L.notice(P.below, '<p><b>P(condition | positive) is not P(positive | condition).</b> The first divides by everyone who tests positive; the second divides by everyone who has the condition. Swapping them is the most common conditional-probability mistake.</p>' +
  '<p>When a condition is rare, almost everyone is in the “no condition” branch, so even a small false-positive rate produces more false positives than true positives. That is why P(condition | positive) depends so much on the <b>prevalence</b> (the base rate) and on specificity.</p>' +
  '<p>Events A and B are <b>independent</b> when P(A | B) = P(A | not B) = P(A). A test whose positive rate is the same with or without the condition tells you nothing.</p><p>Counts are expected counts out of 100,000 people, rounded to whole people.</p>');

var W = 640, H = 420, svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Tree diagram and positive-test bar' }, P.stage);
var tbl = L.table(P.stage);
function t(x, y, s, o) { o = o || {}; var e = L.s('text', { x: x, y: y, 'text-anchor': o.anchor || 'middle', class: 'g-label', 'font-size': o.size || 13, fill: o.color || null }, svg); e.textContent = s; return e; }
function branch(x1, y1, x2, y2, label) {   /* line plus a label offset to the outside of the branch */
  L.s('line', { x1: x1, y1: y1, x2: x2, y2: y2, stroke: 'var(--ink-soft)', 'stroke-width': 2 }, svg);
  var mx = (x1 + x2) / 2, my = (y1 + y2) / 2, len = Math.hypot(x2 - x1, y2 - y1), nx = -(y2 - y1) / len, ny = (x2 - x1) / len;
  if (ny > 0) { nx = -nx; ny = -ny; }   /* normal pointing up */
  var up = y2 <= y1, k = up ? 13 : -15;
  t(mx + nx * k, my + ny * k + 4, label, { size: 12.5, color: 'var(--ink-soft)' });
}
function box(x, y, w, h, color, lines) { L.s('rect', { x: x, y: y, width: w, height: h, rx: 8, fill: 'var(--' + color + '-tint)', stroke: 'var(--' + color + ')', 'stroke-width': 2 }, svg); lines.forEach(function (s, i) { t(x + w / 2, y + 17 + i * 16, s, { size: 12.5 }); }); }
var draw = L.scheduler(function () {
  var r = q(), C = CTX[st.ctx];
  svg.innerHTML = '';
  /* tree */
  t(70, 22, '100,000', { size: 14 }); t(70, 38, st.ctx === 'med' ? 'people' : 'emails', { size: 12, color: 'var(--ink-soft)' });
  var B = [[200, 70, 'purple', C.cond, r.p, r.p], [200, 210, 'ink', C.no, 1 - r.p, 1 - r.p]];
  var leaves = [[420, 20, 'green', 'true positive: ' + C.pos, r.se, r.tp], [420, 100, 'orange', 'false negative: ' + C.neg, 1 - r.se, r.fn], [420, 170, 'red', 'false positive: ' + C.pos, 1 - r.sp, r.fp], [420, 250, 'blue', 'true negative: ' + C.neg, r.sp, r.tn]];
  B.forEach(function (b, i) {
    branch(110, 30, b[0], b[1] + 20, pct(b[4]));
    box(b[0], b[1], 170, 40, b[2] === 'ink' ? 'blue' : 'purple', [b[3], c(b[5])]);
    [leaves[2 * i], leaves[2 * i + 1]].forEach(function (l) {
      branch(b[0] + 170, b[1] + 20, l[0], l[1] + 20, pct(l[4]));
      box(l[0], l[1], 210, 40, l[2], [l[3], c(l[5])]);
    });
  });
  /* who tests positive */
  var y0 = 330, X0 = 20, X1 = 620, wTP = r.pos ? (X1 - X0) * r.tp / r.pos : 0;
  t(X0, y0 - 10, 'Everyone who ' + C.pos + ': ' + c(r.pos), { anchor: 'start', size: 14 });
  if (r.pos) {
    if (wTP > 0) L.s('rect', { x: X0, y: y0, width: wTP, height: 40, fill: 'var(--green)', opacity: 0.8 }, svg);
    L.s('rect', { x: X0 + wTP, y: y0, width: X1 - X0 - wTP, height: 40, fill: 'var(--red)', opacity: 0.55 }, svg);
    for (var k = X0 + wTP + 6; k < X1; k += 10) L.s('line', { x1: k, y1: y0, x2: k - 6, y2: y0 + 40, stroke: '#fff', 'stroke-width': 1.2, opacity: 0.6 }, svg);
    L.s('rect', { x: X0, y: y0, width: X1 - X0, height: 40, fill: 'none', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    t(X0, y0 + 62, 'true positives ' + c(r.tp) + ' (solid green)', { anchor: 'start', color: 'var(--green)' });
    t(X1, y0 + 62, 'false positives ' + c(r.fp) + ' (striped red)', { anchor: 'end', color: 'var(--red)' });
  } else t(W / 2, y0 + 25, 'No one tests positive.', { color: 'var(--ink-soft)' });
  tbl.set(['', C.pos.replace('tests ', '').replace('is ', ''), C.neg.replace('tests ', '').replace('is ', ''), 'Total'], [
    [C.C === 'spam' ? 'Spam' : 'Condition', c(r.tp), c(r.fn), c(r.p)], [C.C === 'spam' ? 'Not spam' : 'No condition', c(r.fp), c(r.tn), c(1 - r.p)], ['Total', c(r.pos), c(r.neg), '100,000']]);
  read.innerHTML = 'P(' + C.short + ' | +) = ' + L.frac(c(r.tp), c(r.tp) + ' + ' + c(r.fp)) + ' = <b>' + pct(r.ppv) + '</b>' +
    '<div class="sub" style="margin-top:6px">compare P(+ | ' + C.short + ') = ' + pct(r.se) + ' · P(' + C.short + ' | −) = ' + pct(r.cneg) + '</div>';
  var dep = Math.abs(r.se - (1 - r.sp)) < 1e-12;
  fb.set(dep ? 'P(+ | ' + C.short + ') = P(+ | not ' + C.short + ') = ' + pct(r.se) + ': the result is <b>independent</b> of the condition, so the test tells you nothing. P(' + C.short + ' | +) equals the prevalence.' :
    'Of everyone who ' + C.pos + ', ' + pct(r.ppv) + ' really ' + C.cond.replace('has', 'have').replace('is', 'are') + ' and ' + pct(1 - r.ppv) + ' are false positives.', dep ? 'warn' : r.ppv >= 0.9 ? 'good' : '');
  var prev = PREV[st.pi];
  if (prev === 1 && st.sens === 99 && st.spec === 99) st.seen.classic = true;
  if (st.sens === 99 && st.spec === 99 && r.ppv >= 0.9) st.seen.prev90 = true;
  if (r.se >= 0.95 && r.ppv < 0.2) st.seen.swap = true;
  if (prev === 5 && r.ppv >= 0.9) st.seen.which = true;
  if (dep) st.seen.indep = true;
  ch.update();
});
draw();
