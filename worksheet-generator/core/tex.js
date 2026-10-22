/* Math-to-TeX formatting. Student-facing math is written as TeX between the marker
   characters U+27E8 and U+27E9 (use M(...)); render.js turns those into KaTeX.
   Division is always a stacked fraction, never a slash. */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});
  var Fr = NS.frac.Fr;

  var OPEN = '⟨', CLOSE = '⟩';
  function M(tex) { return OPEN + tex + CLOSE; }

  function num(x) {                       // integer or fraction -> TeX
    x = Fr.of(x);
    if (x.d === 1) return String(x.n);
    return (x.n < 0 ? '-' : '') + '\\frac{' + Math.abs(x.n) + '}{' + x.d + '}';
  }
  function numP(x) { x = Fr.of(x); return x.n < 0 ? '(' + num(x) + ')' : num(x); }   // parenthesize negatives

  function pt(x, y) { return '(' + num(x) + ',\\,' + num(y) + ')'; }

  function term(absCoef, v) {             // |coef| with its variable, coefficient 1 omitted
    if (v === '') return num(absCoef);
    if (absCoef.eq(1)) return v;
    return num(absCoef) + v;
  }
  /* lin([[coef,'x'],[coef,'y'],[const,'']]) -> "3x - 2y + 5" */
  function lin(list) {
    var out = '', first = true;
    list.forEach(function (t) {
      var c = Fr.of(t[0]);
      if (c.isZero()) return;
      var s = c.sign() < 0 ? '-' : '+';
      var body = term(c.abs(), t[1]);
      if (first) { out += (s === '-' ? '-' : '') + body; first = false; }
      else out += ' ' + s + ' ' + body;
    });
    return first ? '0' : out;
  }

  function eqSI(m, b) { return 'y=' + lin([[m, 'x'], [b, '']]); }
  function eqStd(A, B, C) { return lin([[A, 'x'], [B, 'y']]) + '=' + num(C); }
  function eqPS(m, x1, y1) {              // y - y1 = m(x - x1)
    m = Fr.of(m);
    var left = lin([[1, 'y'], [Fr.of(y1).neg(), '']]);
    var inner = lin([[1, 'x'], [Fr.of(x1).neg(), '']]);
    var right;
    if (m.eq(1)) right = inner;
    else if (m.eq(-1)) right = '-(' + inner + ')';
    else right = num(m) + '(' + inner + ')';
    return left + '=' + right;
  }
  function litFrac(n, d) {                // unsimplified fraction, exactly as given
    return '\\frac{' + n + '}{' + d + '}';
  }
  function eqVert(c) { return 'x=' + num(c); }
  function eqHoriz(c) { return 'y=' + num(c); }

  /* Standard form with integer coefficients, A > 0 (or A = 0 and B > 0), gcd(A,B,C) = 1,
     for the line y = m x + b.  Returns {A,B,C}. */
  function toStandard(m, b) {
    m = Fr.of(m); b = Fr.of(b);
    var L = NS.frac.lcm(m.d, b.d);
    // multiply y = m x + b by L:  L y = (L m) x + L b   ->  -(L m) x + L y = L b
    var A = -(m.n * (L / m.d)), B = L, C = b.n * (L / b.d);
    var g = NS.frac.gcd(NS.frac.gcd(A, B), C) || 1;
    A /= g; B /= g; C /= g;
    if (A < 0 || (A === 0 && B < 0)) { A = -A; B = -B; C = -C; }
    return { A: A, B: B, C: C };
  }

  var MINUS = '−';
  function plain(n) {                     // plain-text number (SVG labels, prose) with a real minus sign
    n = Fr.of(n);
    return (n.n < 0 ? MINUS : '') + Math.abs(n.n) + (n.d === 1 ? '' : '/' + n.d);
  }

  NS.tex = {
    OPEN: OPEN, CLOSE: CLOSE, M: M, num: num, numP: numP, pt: pt, lin: lin,
    eqSI: eqSI, eqStd: eqStd, eqPS: eqPS, eqVert: eqVert, eqHoriz: eqHoriz,
    litFrac: litFrac, toStandard: toStandard, plain: plain, MINUS: MINUS
  };
})(typeof window !== 'undefined' ? window : globalThis);
