/* Quantifier & Set-Notation Explorer (Discrete Math audit #19, 2026-11-18).
   Choose a domain D and an open sentence P(x). Every element of D is shown true or false, the truth set is written in
   roster and set-builder notation, and the tool decides ∀x ∈ D, P(x) (with a counterexample when it fails) and
   ∃x ∈ D, P(x) (with a witness when it holds). The negation view shows ¬∀x P(x) ≡ ∃x ¬P(x) and ¬∃x P(x) ≡ ∀x ¬P(x). */
var css = L.h('style', null, document.head);
css.textContent = '.qx-res{font-size:1.05rem;line-height:1.65;margin:4px 0 8px}.qx-res b{font-family:var(--display)}.qx-big{font-size:1.15rem;font-weight:800}' +
  '.qx-t{color:var(--green);font-weight:800}.qx-f{color:var(--red);font-weight:800}';
var DOMAINS = {
  z5: { label: '{−5, …, 5}', name: '{−5, −4, …, 5}', els: [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5] },
  n12: { label: '{1, …, 12}', name: '{1, 2, …, 12}', els: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] },
  pr: { label: 'Primes < 30', name: '{2, 3, 5, 7, 11, 13, 17, 19, 23, 29}', els: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] }
};
function isPrime(n) { if (n < 2) return false; for (var d = 2; d * d <= n; d++) if (n % d === 0) return false; return true; }
var PREDS = {
  sq: { label: 'x² > x', f: function (x) { return x * x > x; } },
  even: { label: 'x is even', f: function (x) { return x % 2 === 0; } },
  four: { label: 'x² = 4', f: function (x) { return x * x === 4; } },
  lin: { label: '2x + 1 > 0', f: function (x) { return 2 * x + 1 > 0; } },
  odd: { label: 'x is odd', f: function (x) { return Math.abs(x % 2) === 1; } },
  prime: { label: 'x is prime', f: isPrime },
  big: { label: 'x² ≥ 30', f: function (x) { return x * x >= 30; } },
  nn: { label: 'x² ≥ 0', f: function (x) { return x * x >= 0; } }
};
var START = { d: 'z5', p: 'sq', view: 'stmt' };
var st = Object.assign({}, START), seen = {}, touched = false, allSeen = {};
function fmt(x) { return String(x).replace('-', '−'); }
function roster(xs) { return xs.length ? '{' + xs.map(fmt).join(', ') + '}' : '∅'; }
function truthSet() { var P = PREDS[st.p].f; return DOMAINS[st.d].els.filter(P); }
function falseSet() { var P = PREDS[st.p].f; return DOMAINS[st.d].els.filter(function (x) { return !P(x); }); }

var dC = L.chips(P.panel, { label: 'Domain D', value: st.d, options: Object.keys(DOMAINS).map(function (k) { return { value: k, label: DOMAINS[k].label }; }), onChange: function (v) { st.d = v; touched = true; draw(); } });
var pC = L.chips(P.panel, { label: 'Open sentence P(x)', value: st.p, options: Object.keys(PREDS).map(function (k) { return { value: k, label: PREDS[k].label }; }), onChange: function (v) { st.p = v; touched = true; draw(); } });
var vC = L.chips(P.panel, { label: 'Show', value: st.view, options: [{ value: 'stmt', label: 'The statements' }, { value: 'neg', label: 'Their negations' }], onChange: function (v) { st.view = v; touched = true; draw(); } });
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st = Object.assign({}, START); dC.set(st.d, true); pC.set(st.p, true); vC.set(st.view, true); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Choose a domain and an open sentence that make <b>∀x ∈ D, P(x)</b> true.', check: function () { return seen.all; } },
  { text: 'Make <b>∃x ∈ D, P(x)</b> true while <b>∀x ∈ D, P(x)</b> is false. What does the counterexample show?', check: function () { return seen.some; } },
  { text: 'Make the truth set empty. What is the truth value of ∃x ∈ D, P(x) then?', check: function () { return seen.none; } },
  { text: 'Keep one open sentence and change only the domain so that the truth of ∀x ∈ D, P(x) changes.', check: function () { return seen.domain; } },
  { text: 'Show the negations for a statement ∀x ∈ D, P(x) that is false, and check that ∃x ∈ D, ¬P(x) is true.', check: function () { return seen.neg; } }
]);
L.notice(P.below, '<p><b>Truth set.</b> The truth set of P(x) in D is {x ∈ D | P(x)}: set-builder notation names it by the property, roster notation lists its elements.</p>' +
  '<p><b>Quantifiers.</b> ∀x ∈ D, P(x) is true when the truth set is all of D; one counterexample makes it false. ∃x ∈ D, P(x) is true when the truth set is not empty; one witness makes it true.</p>' +
  '<p><b>Negations.</b> ¬(∀x ∈ D, P(x)) ≡ ∃x ∈ D, ¬P(x) and ¬(∃x ∈ D, P(x)) ≡ ∀x ∈ D, ¬P(x): negating swaps the quantifier and negates the sentence.</p>');

var res = L.h('div', { class: 'qx-res', 'aria-live': 'polite' }, P.stage);
var W = 640, H = 170, svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Elements of the domain' }, P.stage);
var draw = L.scheduler(function () {
  var D = DOMAINS[st.d], pr = PREDS[st.p], T = truthSet(), Fs = falseSet(), all = Fs.length === 0, some = T.length > 0;
  svg.innerHTML = '';
  var n = D.els.length, gap = (W - 60) / Math.max(n - 1, 1);
  D.els.forEach(function (x, i) {
    var cx = 30 + i * gap, yes = pr.f(x);
    L.s('circle', { cx: cx, cy: 70, r: 22, fill: yes ? 'var(--green)' : 'var(--card)', 'fill-opacity': yes ? 0.85 : 1, stroke: 'var(--ink)', 'stroke-width': 2.5 }, svg);
    var t = L.s('text', { x: cx, y: 76, 'text-anchor': 'middle', class: 'g-label', 'font-size': 17, 'font-weight': 800 }, svg); t.textContent = fmt(x);
    var u = L.s('text', { x: cx, y: 120, 'text-anchor': 'middle', class: 'g-label', 'font-size': 14, 'font-weight': 700 }, svg); u.textContent = yes ? 'T' : 'F';
  });
  var cap = L.s('text', { x: 30, y: 158, class: 'g-label', 'font-size': 14 }, svg); cap.textContent = 'Filled circles: P(x) is true.';
  svg.setAttribute('aria-label', 'Domain ' + D.name + '; P(x): ' + pr.label + '; true for ' + roster(T));
  var lines = ['<b>D</b> = ' + D.name + ' &nbsp; <b>P(x)</b>: ' + pr.label,
    '<b>Truth set</b> {x ∈ D | ' + pr.label + '} = ' + roster(T)];
  var tv = function (b) { return b ? '<span class="qx-t">true</span>' : '<span class="qx-f">false</span>'; };
  if (st.view === 'stmt') {
    lines.push('<span class="qx-big">∀x ∈ D, ' + pr.label + '</span> is ' + tv(all) + (all ? ' — every element is in the truth set.' : ' — counterexample: x = ' + fmt(Fs[0]) + '.'));
    lines.push('<span class="qx-big">∃x ∈ D, ' + pr.label + '</span> is ' + tv(some) + (some ? ' — witness: x = ' + fmt(T[0]) + '.' : ' — the truth set is empty.'));
  } else {
    lines.push('<span class="qx-big">¬(∀x ∈ D, ' + pr.label + ') ≡ ∃x ∈ D, ¬(' + pr.label + ')</span> is ' + tv(!all) + (!all ? ' — witness: x = ' + fmt(Fs[0]) + '.' : ' — no element makes P(x) false.'));
    lines.push('<span class="qx-big">¬(∃x ∈ D, ' + pr.label + ') ≡ ∀x ∈ D, ¬(' + pr.label + ')</span> is ' + tv(!some) + (some ? ' — counterexample: x = ' + fmt(T[0]) + '.' : ' — no element makes P(x) true.'));
  }
  res.innerHTML = lines.join('<br>');
  fb.set(all ? 'Every element of D is in the truth set, so the universal statement is true.' : some ? 'Some elements work and some do not: ∃ is true, ∀ is false.' : 'No element works: the truth set is ∅, so even ∃ is false.', all ? 'good' : '');
  if (touched) {
    if (all) seen.all = true;
    if (some && !all) seen.some = true;
    if (!some) seen.none = true;
    var k = st.p; allSeen[k] = allSeen[k] || {}; allSeen[k][String(all)] = true;
    if (allSeen[k]['true'] && allSeen[k]['false']) seen.domain = true;
    if (st.view === 'neg' && !all) seen.neg = true;
  }
  ch.update();
});
draw();
