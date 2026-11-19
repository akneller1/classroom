/* Statistics audit #7 (2026-11-18): grading for Statistics keys made of labelled numbers and number lists, such as
   "Min = 15, Q1 = 25, Median = 35, Q3 = 50, Max = 90", "μ = 1.80, σ ≈ 1.208", "Fences 8 and 20; outlier: 30",
   "z ≈ 2.40, p-value ≈ 0.0082; reject H₀" or "Yes; upper fence = 34.50", which the other graders leave to self-check.
   The student types the numbers in the same order; labels are optional. A number the prompt already gives (such as the
   99 in "99% CI") may be left out. A key value with d decimal places accepts the same value or any more precise value
   that rounds to it (so 0.16667 or 1/6 matches 0.1667, but 1.21 does not match 1.208). Where the key has "a ≈ b", either
   form is accepted. A key that also says yes/no or reject/fail to reject H₀ needs the same decision. Equations, steps and
   sentences are not graded here. */
(function (G) {
  'use strict';
  var LABELS = /^(?:min|max|median|q|q1|q3|treatments?|students|differences|iqr|mean|means?|sd|se|df|z|t|r|r²|s|sₓ|x|y|w|p|n|range|fences?|outliers?|outlier\(s\)|estimate|exact|residuals?|predicted|difference|variance|var|me|and|to|with|without|at|upper|lower|fence|yes|no|reject|fail|h₀|hₐ|p-value|pvalue|values?|is|of|overall|mild|severe|a|b|c|min\.?|minutes|hours|seconds|cm|in|lb|kg|g|ms|mph|points|ci|μ|σ|x̄|p̂|ŷ|μ_x̄|σ_x̄|μ_p̂|σ_p̂|p̂₁|p̂₂|p̂_c|d̄|s_d|t\*|z\*|χ²|p\(x\)|p\(w\)|μ_d)$/i;
  var NUM = /(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+\/\d+|\d*\.\d+|\d+)/g;
  function norm(s) { return String(s == null ? '' : s).replace(/[−–]/g, '-').replace(/ /g, ' ').trim(); }
  function stripLabelDigits(s) { return s.replace(/\b[Qq]([13])\b/g, 'Q').replace(/\bH[₀ₐ0a]\b/g, 'H').replace(/\bP\((?:[A-Za-z|∣ ]+)\)/g, 'P'); }
  /* Read numbers in order. A minus sign counts only when attached to the number and preceded by a start, space, "(", ",",
     ";", ":", "=" or "≈". "a ≈ b" becomes one slot with two accepted forms. */
  function numbers(s) {
    var t = stripLabelDigits(norm(s)), out = [], m;
    NUM.lastIndex = 0;
    while ((m = NUM.exec(t))) {
      var txt = m[1], i = m.index, neg = false;
      if (i > 0 && t[i - 1] === '-' && (i === 1 || /[\s(,;:=≈]/.test(t[i - 2]))) neg = true;
      var after = t.slice(NUM.lastIndex);
      var slot = { forms: [mk(txt, neg)], end: NUM.lastIndex };
      var prev = out[out.length - 1];
      if (prev && prev.approxNext) { prev.forms.push(slot.forms[0]); prev.approxNext = false; continue; }
      slot.approxNext = /^\s*%?\s*≈/.test(after);
      out.push(slot);
    }
    return out;
  }
  function mk(txt, neg) {
    var clean = txt.replace(/,/g, ''), v, d = 0, frac = /\//.test(clean);
    if (frac) { var p = clean.split('/'); v = +p[0] / +p[1]; d = -1; }
    else { v = +clean; d = (clean.split('.')[1] || '').length; }
    return { v: neg ? -v : v, d: d, text: (neg ? '-' : '') + clean };
  }
  function roundHalfUp(v, d) { var f = Math.pow(10, d); return Math.round((Math.abs(v) * f) + 1e-9) / f * (v < 0 ? -1 : 1); }
  function matches(form, x) {
    if (form.d === -1 || x.d === -1) return Math.abs(form.v - x.v) < 1e-9 || (x.d === -1 && form.d > 0 && Math.abs(roundHalfUp(x.v, form.d) - form.v) < 1e-9);
    if (Math.abs(form.v - x.v) < 1e-9) return true;
    return form.d >= 1 && x.d > form.d && Math.abs(roundHalfUp(x.v, form.d) - form.v) < 1e-9;
  }
  function decision(s) {
    var t = norm(s).toLowerCase();
    if (/fail(?:s|ed)? to reject/.test(t)) return 'fail';
    if (/\breject/.test(t)) return 'reject';
    if (/^\s*yes\b/.test(t)) return 'yes';
    if (/^\s*no\b/.test(t)) return 'no';
    return null;
  }
  function supports(answer) {
    var a = norm(answer);
    if (!a || a.length > 160 || /^step\b/i.test(a) || /[+×÷√]|ŷ\s*=|\bx\s*$/.test(a) || /\d\s*[a-z]\b(?!\))/i.test(a.replace(/\d+(?:\.\d+)?\s*(?:min|hours|seconds|cm|in|lb|kg|g|ms|mph|points)\b/gi, ''))) return false;
    var ns = numbers(a);
    if (ns.length < 1) return false;
    var rest = stripLabelDigits(a).replace(NUM, ' ').replace(/[=≈:;,()%$.<>≤≥|∣]/g, ' ').replace(/[-]/g, ' ').trim();
    var words = rest.split(/\s+/).filter(Boolean);
    if (!words.every(function (w) { return LABELS.test(w); })) return false;
    /* a bare number is the rational grader's job; one labelled number ("sₓ ≈ 2.74") or "a ≈ b" is read here */
    return ns.length >= 2 || !!decision(a) || words.length > 0 || ns[0].forms.length > 1;
  }
  function grade(answer, typed, prompt) {
    if (!supports(answer)) return { status: 'self' };
    var input = norm(typed);
    if (!input) return { status: 'empty' };
    if (input.length > 200) return { status: 'invalid', message: 'Enter only your final answer (200 characters maximum).' };
    var key = numbers(answer), got = numbers(input), p = norm(prompt);
    var dk = decision(answer);
    if (dk && decision(input) !== dk) return { status: decision(input) ? 'incorrect' : 'invalid', message: 'Include your decision (' + (dk === 'yes' || dk === 'no' ? 'yes or no' : 'reject or fail to reject H₀') + ') with the numbers.' };
    if (!got.length) return { status: 'invalid', message: 'Enter the numbers in the same order as the question asks, for example Q1 = 25, Q3 = 50.' };
    var j = 0;
    for (var i = 0; i < key.length; i++) {
      var k = key[i], x = got[j];
      if (x && k.forms.some(function (f) { return matches(f, x.forms[0]); })) { j++; continue; }
      var given = k.forms.some(function (f) { return new RegExp('(^|[^\\d.])' + f.text.replace(/^-/, '[-−]?').replace(/\./g, '\\.') + '(?![\\d])').test(p); });
      if (given) continue;
      return { status: 'incorrect' };
    }
    return { status: j === got.length ? 'correct' : 'incorrect' };
  }
  G.MKSTAT = { supports: supports, grade: grade, numbers: numbers };
})(typeof window !== 'undefined' ? window : globalThis);
