/* 8th Grade Math short-answer grading (8th Grade Math audit #4 and #20, 2026-11-19).
   Bank keys the rational and exact graders leave to self-review:
   - one-word classifications from a closed list (rational / irrational, linear / nonlinear, similar / congruent,
     increasing / decreasing / constant, positive / negative / no association, one / no / infinitely many solutions …)
   - "8 and 9" (consecutive whole numbers a root lies between): "8, 9", "8 & 9", "between 8 and 9"
   - a number with a unit phrase ("6 units", "49 miles per hour", "36π cubic inches"): the number or π value is graded
   - scientific notation ("2.3 × 10⁶"): the value must match and the answer must be in scientific notation
   - equations of lines ("y = 2x - 5", "C = 14g + 24"): any equivalent form solved for the same variable, without parentheses
   - expanded expressions ("6x + 18"): an equivalent expanded expression (no parentheses, no more terms than the key)
   - equations that model a situation ("33 + 20c = 133"): the same equation with its sides or terms rearranged
   - "slope -1, y-intercept 5" and "from x = 1 to x = 6"
   - "Which is greater" answers: the chosen number as written
   Typed answers may use ±, e-notation (7.1e-3), x for ×, ^ for powers and sqrt( ) for √.
   Only on 8th Grade Math practice tests (practice.js sets MK_PRACTICE_COURSE); anything else stays with the other graders. */
(function (G) {
  'use strict';
  var API = G.MKGRADE8 = {};
  var SUP = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-' };
  function C() { return G.MKMENU && G.MKMENU.check; }
  function clean(s) { return String(s == null ? '' : s).replace(/[−–‑]/g, '-').replace(/\s+/g, ' ').trim().replace(/\.$/, ''); }
  function low(s) { return clean(s).toLowerCase(); }
  function supToCaret(s) { return s.replace(/[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+/g, function (m) { return '^' + m.split('').map(function (c) { return SUP[c]; }).join(''); }); }
  /* typed-answer normalisation shared by every kind */
  function typedNorm(s) {
    s = clean(s).replace(/sqrt\s*\(([^()]*)\)/gi, '√($1)').replace(/(?<![a-z])pi(?![a-z])/gi, 'π');
    var pm = /^x\s*=\s*±\s*(.+)$/i.exec(s) || /^±\s*(.+)$/.exec(s);
    if (pm) s = 'x = ' + pm[1] + ' or x = -' + pm[1];
    return s;
  }

  /* ---------- closed word list ---------- */
  var WORDS = [
    [/^rational(?: number)?$/, 'rational'], [/^irrational(?: number)?$/, 'irrational'],
    [/^linear(?: function)?$/, 'linear'], [/^(?:non-?linear|not linear)(?: function)?$/, 'nonlinear'],
    [/^similar$/, 'similar'], [/^congruent$/, 'congruent'],
    [/^increasing$/, 'increasing'], [/^decreasing$/, 'decreasing'], [/^constant$/, 'constant'],
    [/^increases?$/, 'increase'], [/^decreases?$/, 'decrease'],
    [/^positive(?: association)?$/, 'positive'], [/^negative(?: association)?$/, 'negative'],
    [/^(?:no association|none|no correlation|no relationship)$/, 'no association'],
    [/^positive linear(?: association)?$/, 'positive linear'], [/^negative linear(?: association)?$/, 'negative linear'],
    [/^(?:positive )?nonlinear(?: association)?$/, 'nonlinear association'],
    [/^(?:one|exactly one|1) solution$/, 'one solution'], [/^(?:no solutions?|none|0 solutions)$/, 'no solution'],
    [/^(?:infinitely many(?: solutions)?|infinite(?:ly many)?(?: solutions)?|all real numbers)$/, 'infinitely many solutions'],
    [/^(?:yes|y)$/, 'yes'], [/^(?:no|n)$/, 'no'],
    [/^enlargement$/, 'enlargement'], [/^reduction$/, 'reduction'],
    [/^(?:a )?translation$/, 'translation'], [/^(?:a )?reflection$/, 'reflection'], [/^(?:a )?rotation$/, 'rotation'], [/^(?:a )?dilation$/, 'dilation'],
    [/^(?:a )?function$/, 'function'], [/^not a function$/, 'not a function']
  ];
  function word(s) { s = low(s).replace(/[.!]$/, ''); for (var i = 0; i < WORDS.length; i++) if (WORDS[i][0].test(s)) return WORDS[i][1]; return null; }
  // a key word that is also a synonym of another (e.g. "nonlinear" key vs "nonlinear association") compares by family
  function wordFamily(w) { return { 'nonlinear association': 'nonlinear' }[w] || w; }

  /* ---------- numbers with units ---------- */
  var DIRECTION = /\b(?:above|below|left|right|up|down|before|after|from|to|of|than|more|less|north|south|east|west)\b/i;
  function numberUnit(s) {
    var m = /^(\$?)\s*(-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:\/\d+)?|\(-?\d+\/\d+\)π|-?\d*(?:\.\d+)?π(?:\/\d+)?|-?\d+\/\d+π)\s*([a-zA-Z°%][a-zA-Z .\/²³°-]{0,40})?$/.exec(clean(s));
    if (!m || DIRECTION.test(m[3] || '')) return null;
    return { value: m[2].replace(/,/g, ''), unit: (m[3] || '').trim() };
  }
  function sameValue(a, b) {
    if (/π/.test(a) || /π/.test(b)) { if (!G.MKEXACT) return null; var r = G.MKEXACT.grade(a, b); return r.status === 'correct' ? true : r.status === 'incorrect' ? false : null; }
    try { return C().readNumber(a).eq(C().readNumber(b)); } catch (e) { return null; }
  }

  /* ---------- scientific notation ---------- */
  function sci(s) {
    s = clean(s).replace(/\s+/g, '');
    s = supToCaret(s).replace(/[x×*·]/gi, '×');
    var m = /^(-?\d+(?:\.\d+)?)×10\^\(?(-?\d+)\)?$/.exec(s) || /^(-?\d+(?:\.\d+)?)e(-?\d+)$/i.exec(s);
    if (!m) return null;
    return { a: m[1], n: +m[2] };
  }
  function sciEq(k, t) {
    var a = Number(k.a) * Math.pow(10, k.n), b = Number(t.a) * Math.pow(10, t.n);
    // compare mantissa digits exactly: shift both to the same exponent with strings
    var norm = function (p) { var m = p.a.replace('-', ''), neg = p.a[0] === '-', i = m.indexOf('.'); var digits = m.replace('.', ''), e = p.n + (i < 0 ? m.length : i); digits = digits.replace(/^0+/, ''); var lead = m.replace('.', '').length - m.replace('.', '').replace(/^0+/, '').length; e -= lead; digits = digits.replace(/0+$/, ''); return (neg ? '-' : '') + digits + 'e' + e; };
    return norm(k) === norm(t) || (a === 0 && b === 0);
  }

  /* ---------- equations and expressions ---------- */
  function stripFracParens(s) { return s.replace(/\((-?\d+\/\d+)\)/g, '$1'); }
  function linearEq(s) { var m = /^\s*([a-zA-Z])\s*=\s*(.+)$/.exec(clean(s)); return m ? { v: m[1], rhs: m[2] } : null; }
  function exprOK(s) { try { C().parseExpr(supToCaret(s)); return true; } catch (e) { return false; } }
  function equiv(a, b) { try { return !!C().equivalent(supToCaret(a), supToCaret(b)); } catch (e) { return null; } }
  function terms(s) { return stripFracParens(clean(s)).replace(/^-/, '').split(/\s*[+-]\s*/).filter(Boolean).length; }
  function nums(s) { return (clean(s).match(/\d+(?:\.\d+)?/g) || []).map(Number).sort(function (a, b) { return a - b; }).join(','); }
  function modelEq(s) { var p = clean(s).split('='); if (p.length !== 2 || !/[a-z]/i.test(s)) return null; if (!exprOK(p[0]) || !exprOK(p[1])) return null; return p; }

  /* ---------- kinds ---------- */
  function kind(answer, prompt) {
    var a = clean(answer);
    if (/^which is greater/i.test(prompt || '')) return 'pick';
    if (/^order from (?:least to greatest|greatest to least)/i.test(prompt || '') && /,/.test(a)) return 'order';
    if (word(a)) return 'word';
    if (/^-?\d+ and -?\d+$/.test(a)) return 'between';
    if (/^slope -?\d+(?:\/\d+)?, y-intercept -?\d+(?:\/\d+)?$/i.test(a)) return 'slopeint';
    if (/^from x = -?\d+ to x = -?\d+$/i.test(a)) return 'interval';
    if (sci(a)) return 'sci';
    var le = linearEq(a);
    if (le && exprOK(le.rhs) && !/[()]/.test(stripFracParens(le.rhs))) return 'line';
    var me = modelEq(a);
    if (me && !le) return 'model';
    var nu = numberUnit(a);
    if (nu && nu.unit) return 'unit';
    if (!/[=<>\s]/.test(a) && /[a-z]/i.test(a) && exprOK(a)) return 'form';
    if (!/[=<>]/.test(a) && /[a-z]/i.test(a) && /\d/.test(a) && exprOK(a) && !/[()]/.test(stripFracParens(a)) && a.split(' ').length > 1) return 'expanded';
    return null;
  }
  API.supports = function (answer, prompt) { return typeof answer === 'string' ? kind(answer, prompt) : null; };
  /* preferred(): keys the other graders would mis-grade, which this grader must take first */
  API.preferred = function (answer, prompt) { var k = API.supports(answer, prompt); return k === 'pick' || k === 'order' || k === 'word' || k === 'sci' || k === 'unit' || k === 'between'; };

  API.grade = function (answer, typed, prompt) {
    var k = kind(answer, prompt), t = typedNorm(typed), a = clean(answer);
    if (!t) return { status: 'empty' };
    if (t.length > 180) return { status: 'invalid', message: 'Enter only your final answer (180 characters maximum).' };
    try {
      if (k === 'pick') {
        var sq = function (s) { return clean(s).replace(/\s+/g, '').replace(/√\((\d+)\)/g, '√$1').toLowerCase(); };
        return { status: sq(a) === sq(t) ? 'correct' : 'incorrect' };
      }
      if (k === 'order') {
        var it = function (s) { return clean(s).split(/\s*[,;]\s*/).map(function (x) { return x.replace(/\s+/g, '').replace(/√\((\d+)\)/g, '√$1').replace(/…|\.\.\./g, '').toLowerCase(); }); };
        var ka2 = it(a), ta2 = it(t);
        if (ta2.length !== ka2.length) return { status: 'invalid', message: 'List all ' + ka2.length + ' numbers, separated by commas.' };
        return { status: ka2.every(function (x, i) { return x === ta2[i]; }) ? 'correct' : 'incorrect' };
      }
      if (k === 'word') {
        var w = word(t);
        if (!w) return { status: 'invalid', message: 'Answer with the word or phrase the question asks for.' };
        return { status: wordFamily(w) === wordFamily(word(a)) ? 'correct' : 'incorrect' };
      }
      if (k === 'between') {
        var am = a.match(/-?\d+/g), tm = low(t).replace(/^between\s+/, '').match(/^(-?\d+)\s*(?:and|,|&|-|to)\s*(-?\d+)$/);
        if (!tm) return { status: 'invalid', message: 'Enter the two whole numbers, such as 8 and 9.' };
        var x = [+tm[1], +tm[2]].sort(function (p, q) { return p - q; });
        return { status: x[0] === +am[0] && x[1] === +am[1] ? 'correct' : 'incorrect' };
      }
      if (k === 'slopeint') {
        var an = a.match(/-?\d+(?:\/\d+)?/g), tn = t.match(/-?\d+(?:\.\d+)?(?:\/\d+)?/g);
        if (!tn || tn.length !== 2) return { status: 'invalid', message: 'Enter the slope and the y-intercept, such as slope -1, y-intercept 5.' };
        return { status: sameValue(an[0], tn[0]) && sameValue(an[1], tn[1]) ? 'correct' : 'incorrect' };
      }
      if (k === 'interval') {
        var ai = a.match(/-?\d+/g), ti = t.match(/-?\d+(?:\.\d+)?/g);
        if (!ti || ti.length !== 2) return { status: 'invalid', message: 'Enter the interval, such as from x = 1 to x = 6.' };
        return { status: +ti[0] === +ai[0] && +ti[1] === +ai[1] ? 'correct' : 'incorrect' };
      }
      if (k === 'sci') {
        var ka = sci(a), ta = sci(t);
        if (!ta) return { status: 'invalid', message: 'Write your answer in scientific notation, such as 2.3 × 10^6.' };
        var mant = Math.abs(Number(ta.a));
        if (!(mant >= 1 && mant < 10)) return { status: 'incorrect', message: 'The first factor must be at least 1 and less than 10.' };
        return { status: sciEq(ka, ta) ? 'correct' : 'incorrect' };
      }
      if (k === 'unit') {
        var kn = numberUnit(a), tn2 = numberUnit(t.replace(/^\$\s*/, '$'));
        if (!tn2) { var bare = clean(t); if (sameValue(kn.value, bare) !== null) tn2 = { value: bare }; }
        if (!tn2) return { status: 'invalid', message: 'Enter a number (the unit is optional).' };
        var same = sameValue(kn.value, tn2.value);
        return same === null ? { status: 'invalid', message: 'Answer format could not be read.' } : { status: same ? 'correct' : 'incorrect' };
      }
      if (k === 'line') {
        var kl = linearEq(a), tl = linearEq(t);
        if (!tl) return { status: 'invalid', message: 'Enter an equation solved for ' + kl.v + ', such as ' + kl.v + ' = 2x + 3.' };
        if (tl.v.toLowerCase() !== kl.v.toLowerCase()) return { status: 'incorrect' };
        if (/[()]/.test(stripFracParens(tl.rhs))) return { status: 'invalid', message: 'Simplify the right side (no parentheses).' };
        var e1 = equiv(kl.rhs, tl.rhs);
        return e1 === null ? { status: 'invalid', message: 'Answer format could not be read.' } : { status: e1 ? 'correct' : 'incorrect' };
      }
      if (k === 'expanded') {
        if (/=/.test(t)) return { status: 'invalid', message: 'Enter an expression without an equals sign.' };
        if (/[()]/.test(stripFracParens(t))) return { status: 'incorrect', message: 'Write the expression without parentheses.' };
        var e2 = equiv(a, t);
        if (e2 === null) return { status: 'invalid', message: 'Answer format could not be read.' };
        return { status: e2 && terms(t) <= terms(a) ? 'correct' : 'incorrect' };
      }
      if (k === 'form') {
        var cf = function (x) { return supToCaret(clean(x)).replace(/[\s*·]/g, '').replace(/\^\((-?\d+)\)/g, '^$1'); };
        if (cf(a) === cf(t)) return { status: 'correct' };
        var e3 = equiv(a, t);
        return e3 ? { status: 'self' } : e3 === null ? { status: 'invalid', message: 'Answer format could not be read.' } : { status: 'incorrect' };
      }
      if (k === 'model') {
        var kp = modelEq(a), tp = modelEq(t);
        if (!tp) return { status: 'invalid', message: 'Enter an equation, such as 20c + 33 = 133.' };
        var d1 = '(' + kp[0] + ')-(' + kp[1] + ')', d2 = '(' + tp[0] + ')-(' + tp[1] + ')';
        var ok = equiv(d1, d2) || equiv(d1, '-(' + d2 + ')');
        return { status: ok && nums(a) === nums(t) ? 'correct' : 'incorrect' };
      }
    } catch (e) { return { status: 'invalid', message: 'Answer format could not be read.' }; }
    return { status: 'self' };
  };
  API.normalizeTyped = typedNorm;
})(typeof window !== 'undefined' ? window : globalThis);
