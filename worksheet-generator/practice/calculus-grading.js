/* Calculus audit #2 (2026-11-18): grade typed answers whose keys are expressions, equations or constants with e, ln,
   trig and √, which the rational and exact graders leave self-checked.

   MKCALC.supports(key) → a kind or null; MKCALC.grade(key, typed) → {status: 'correct'|'incorrect'|'invalid'|'empty'|'self', message?}.
   Kinds:
   - expression  "12x³ - 1", "f′(x) = x⁴(-x + 5)e^(-x)", "y = 7x + 1", "dy/dx = -(2x + y)/(x + 2y)": equal at sample points.
   - antiderivative  "x⁴ - 5x + C": the typed answer must differ from the key by a constant and include + C.
   - family  "y = Ce^(5x)", "y = -1/(11x + C)": every member of the key's family is a member of the typed family and back.
   - implicit  "2y² - x² = C": the typed left side is a nonzero multiple of the key's plus a constant.
   - constant  "-1 + e⁴", "ln(4)", "(9√3)/π", "128π cm³/s", "-∞": the same number (units may be left off; exact keys need exact typing).
   - compound  "-79 at x = -3", "x = 10 in; V = 16000 in³": each part graded as above.
   Numbers are compared in floating point with a relative tolerance of 1e-7, so an equivalent form in any arrangement is
   accepted; a decimal approximation of an exact key is not. No eval. */
(function (G) {
  'use strict';
  var API = (G.MKCALC = G.MKCALC || {});
  var SUP = { '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9', '⁻': '-' };
  var FUN = { sin: Math.sin, cos: Math.cos, tan: Math.tan, sec: function (v) { return 1 / Math.cos(v); }, csc: function (v) { return 1 / Math.sin(v); }, cot: function (v) { return 1 / Math.tan(v); },
    ln: Math.log, log: Math.log10, sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, arcsin: Math.asin, arccos: Math.acos, arctan: Math.atan, asin: Math.asin, acos: Math.acos, atan: Math.atan };
  var UNIT = /(?:°F|\s+(?:°F per hour|°F|ft\/s²|ft\/s|m\/s²|m\/s|cm³\/s|cm²\/s|in³\/s|ft³\/min|L\/min|liters per minute|gallons per minute|dollars per item|ft²|m²|cm²|in²|ft³|m³|cm³|in³|ft|m|cm|in|km|L|liters|gallons|thousand gallons|inches|hours|minutes|seconds|people|bacteria|cars|dollars|square units|units²|units)\.?)$/;

  function clean(s) {
    return String(s == null ? '' : s).replace(/[−–]/g, '-').replace(/[·×]/g, '*').replace(/÷/g, '/').replace(/π/g, 'pi').replace(/ˣ/g, '^x').replace(/∞/g, 'inf')
      .replace(/′/g, "'").replace(/\s+/g, ' ').trim().replace(/\.$/, '');
  }

  /* ---------- tokenizer and parser ---------- */
  function tokens(src) {
    var s = src, out = [], i = 0, m;
    while (i < s.length) {
      var ch = s[i];
      if (ch === ' ') { i++; continue; }
      if ((m = /^\d+(?:\.\d+)?|^\.\d+/.exec(s.slice(i)))) { out.push({ t: 'num', v: parseFloat(m[0]), raw: m[0] }); i += m[0].length; continue; }
      if (SUP[ch]) { var j = i, e = ''; while (j < s.length && SUP[s[j]]) e += SUP[s[j++]]; out.push({ t: 'sup', v: e }); i = j; continue; }
      if (ch === '√') { out.push({ t: 'fn', v: 'sqrt' }); i++; continue; }
      if ((m = /^(arcsin|arccos|arctan|sin|cos|tan|sec|csc|cot|ln|log|sqrt|exp|abs)/.exec(s.slice(i)))) {
        var name = m[0]; i += name.length;
        if (s.slice(i, i + 2) === '⁻¹') { name = { sin: 'asin', cos: 'acos', tan: 'atan' }[name] || name; i += 2; }
        out.push({ t: 'fn', v: name }); continue;
      }
      if ((m = /^(pi|inf)/.exec(s.slice(i)))) { out.push({ t: 'id', v: m[0] }); i += m[0].length; continue; }
      if (/[a-zA-Z]/.test(ch)) { out.push({ t: 'id', v: ch }); i++; continue; }
      if ('+-*/^()|'.indexOf(ch) >= 0) { out.push({ t: ch }); i++; continue; }
      throw Error('unexpected ' + ch);
    }
    return out;
  }
  // AST nodes: ['n', v] ['v', name] ['+', a, b] ['-', a, b] ['*', a, b] ['/', a, b] ['^', a, b] ['neg', a] ['f', name, a]
  function parse(src) {
    var tk = tokens(src), i = 0;
    function peek() { return tk[i]; }
    function eat(t) { if (!tk[i] || tk[i].t !== t) throw Error('expected ' + t); return tk[i++]; }
    function startsAtom(x) { return x && (x.t === 'num' || x.t === 'id' || x.t === 'fn' || x.t === '(' || x.t === '|'); }
    function expr() {
      var a = term();
      while (peek() && (peek().t === '+' || peek().t === '-')) { var op = tk[i++].t; a = [op, a, term()]; }
      return a;
    }
    function term() {
      var a = unary();
      for (;;) {
        var p = peek();
        if (p && (p.t === '*' || p.t === '/')) { i++; a = [p.t, a, unary()]; }
        else if (startsAtom(p) && !(p.t === '|' && absDepth > 0)) a = ['*', a, power()];
        else return a;
      }
    }
    function unary() { if (peek() && peek().t === '-') { i++; return ['neg', unary()]; } if (peek() && peek().t === '+') { i++; return unary(); } return power(); }
    function power() {
      var a = atom();
      for (;;) {
        var p = peek();
        if (p && p.t === 'sup') { i++; a = ['^', a, ['n', parseFloat(p.v)]]; }
        else if (p && p.t === '^') { i++; a = ['^', a, unary()]; }
        else return a;
      }
    }
    var absDepth = 0;
    function atom() {
      var p = tk[i++];
      if (!p) throw Error('unexpected end');
      if (p.t === 'num') return ['n', p.v];
      if (p.t === 'id') return p.v === 'pi' ? ['n', Math.PI] : p.v === 'inf' ? ['n', Infinity] : p.v === 'e' ? ['n', Math.E] : ['v', p.v];
      if (p.t === '(') { var a = expr(); eat(')'); return a; }
      if (p.t === '|') { absDepth++; var b = expr(); absDepth--; eat('|'); return ['f', 'abs', b]; }
      if (p.t === 'fn') {
        var pw = null;
        if (peek() && peek().t === 'sup') pw = parseFloat(tk[i++].v);   // sin²(x)
        var arg = p.v === 'sqrt' ? power() : (peek() && peek().t === '(' ? (i++, (function () { var v = expr(); eat(')'); return v; })()) : power());
        var f = ['f', p.v, arg];
        return pw === null ? f : ['^', f, ['n', pw]];
      }
      throw Error('unexpected token');
    }
    var tree = expr();
    if (i !== tk.length) throw Error('trailing input');
    return tree;
  }
  function vars(n, acc) { acc = acc || {}; if (n[0] === 'v') acc[n[1]] = 1; for (var k = 1; k < n.length; k++) if (Array.isArray(n[k])) vars(n[k], acc); return acc; }
  function ev(n, env) {
    switch (n[0]) {
      case 'n': return n[1];
      case 'v': if (!(n[1] in env)) throw Error('unknown variable ' + n[1]); return env[n[1]];
      case '+': return ev(n[1], env) + ev(n[2], env);
      case '-': return ev(n[1], env) - ev(n[2], env);
      case '*': return ev(n[1], env) * ev(n[2], env);
      case '/': return ev(n[1], env) / ev(n[2], env);
      case '^': return Math.pow(ev(n[1], env), ev(n[2], env));
      case 'neg': return -ev(n[1], env);
      case 'f': return FUN[n[1]](ev(n[2], env));
    }
    throw Error('bad node');
  }
  function close(a, b, tol) { if (!isFinite(a) || !isFinite(b)) return a === b; return Math.abs(a - b) <= (tol || 1e-11) * Math.max(1, Math.abs(a), Math.abs(b)); }

  /* ---------- sample points ---------- */
  var XS = [0.37, 0.71, 1.13, 1.62, 2.29, 2.83, 3.41, 0.043, 0.112, -0.071, -0.53, 4.37, 6.21, 7.93, 9.48, 12.7, -2.3], YS = [1.31, 0.83, 1.97, 2.44, 0.59, 1.73, 2.91, 1.12, 0.67, 2.21, 1.49, 3.17, 0.92, 1.58, 2.67, 0.71, 1.86];
  function samples(names) {
    var out = [];
    for (var k = 0; k < XS.length; k++) { var e = {}; names.forEach(function (nm, j) { e[nm] = j === 0 ? XS[k] : YS[(k + j * 3) % YS.length]; }); out.push(e); }
    return out;
  }

  /* ---------- answer shapes ---------- */
  var LHS = /^(?:[a-zA-Z](?:'{1,3}|″|‴)?\(x\)|y|dy\/dx|g'\(x\)|h'\(x\)|f'\(x\)|F\(x\)|f\(x\)|y'|c|x|k|t)\s*=\s*/;
  function unitTail(s) {   // "20/(49pi) ft/min": a constant followed by a unit not in the list
    var m = /^(.*?\S)\s+([a-zA-Z°][a-zA-Z°\/²³ ]*)$/.exec(s);
    if (!m) return null;
    try { if (Object.keys(vars(parse(stripLabel(m[1])))).length) return null; } catch (e) { return null; }
    return { index: m[1].length, 0: s.slice(m[1].length) };
  }
  function stripLabel(s) { return s.replace(LHS, ''); }
  function hasC(s) { return /(^|[^a-zA-Z])C([^a-zA-Z]|$)/.test(s); }

  function classify(key) {
    var s = clean(key);
    if (!s) return null;
    if (/^(does not exist|dne)$/i.test(s)) return { kind: 'word', s: 'dne' };
    if (/^(yes|no)$/i.test(s)) return { kind: 'yesno', s: s.toLowerCase() };
    if (/^-?inf$/.test(s)) return { kind: 'constant', s: s, inf: true };
    if (/ at x = /.test(s)) { var p = s.split(' at x = '); var a = classify(p[0]), b = classify(p[1]); return a && b && a.kind === 'constant' && b.kind === 'constant' ? { kind: 'compound', sep: ' at x = ', parts: [a, b] } : null; }
    if (/;/.test(s) && !/[a-z]{4,}/.test(s.replace(/\b(sin|cos|tan|sqrt)\b/g, ''))) {
      var ps = s.split(/\s*;\s*/).map(function (x) { return classify(x.replace(/^[A-Za-z]\s*=\s*/, '')); });
      return ps.every(function (x) { return x && x.kind === 'constant'; }) ? { kind: 'compound', sep: ';', parts: ps } : null;
    }
    var unit = UNIT.exec(s) || unitTail(s), body = unit ? s.slice(0, unit.index) : s;
    if (/[a-zA-Z]{3,}/.test(body.replace(/(arcsin|arccos|arctan|sin|cos|tan|sec|csc|cot|ln|log|sqrt|exp|abs|pi|inf)/g, ''))) return null;   // words
    if (/[<>≤≥∪]|\[|^\(.*,.*\)$/.test(body)) return null;                                      // intervals, points: other graders
    var eq = body.split('=');
    try {
      if (eq.length === 2 && !LHS.test(body)) {                                                  // implicit F(x, y) = C
        if (clean(eq[1]) !== 'C') return null;
        var L = parse(eq[0]), vv = vars(L);
        if (!vv.x || !vv.y) return null;
        return { kind: 'implicit', tree: L };
      }
      if (eq.length > 2) return null;
      var expr = stripLabel(body), tree = parse(expr), v = vars(tree);
      var names = Object.keys(v).filter(function (n) { return n !== 'C'; });
      if (names.some(function (n) { return ['x', 'y', 't', 'h'].indexOf(n) < 0; })) return null;
      if (v.C) return /\+ ?C$/.test(expr) && !/C[^\s]/.test(expr.replace(/\+ ?C$/, '')) && !hasC(expr.replace(/\+ ?C$/, '')) ? { kind: 'antiderivative', tree: tree, names: names } : { kind: 'family', tree: tree, names: names };
      if (!names.length) return { kind: 'constant', tree: tree, unit: unit ? String(unit[0]).trim() : '', exact: !/\d\.\d/.test(expr) };
      return { kind: 'expression', tree: tree, names: names };
    } catch (e) { return null; }
  }
  API.supports = function (key) { var c = classify(key); return c ? c.kind : null; };

  /* ---------- comparisons ---------- */
  function compareExpr(a, b, names) {
    var used = 0;
    for (var s of samples(names.length ? names : ['x'])) {
      var x, y;
      try { x = ev(a, s); y = ev(b, s); } catch (e) { return false; }
      if (!isFinite(x) && !isFinite(y)) continue;
      if (!isFinite(x) || !isFinite(y) || isNaN(x) || isNaN(y)) { if (isNaN(x) && isNaN(y)) continue; return false; }
      if (!close(x, y)) return false;
      used++;
    }
    return used >= 3;
  }
  function differByConstant(a, b, names) {
    var d = null, used = 0;
    for (var s of samples(names.length ? names : ['x'])) {
      s.C = 0;
      var x, y; try { x = ev(a, s); y = ev(b, s); } catch (e) { return false; }
      if (!isFinite(x) || !isFinite(y)) continue;
      if (d === null) d = x - y; else if (!close(x - y, d)) return false;
      used++;
    }
    return used >= 3;
  }
  function affine(a, b, names) {   // b = p·a + q with p ≠ 0, on sample (x, y) points
    var pts = [];
    for (var s of samples(names)) { try { var u = ev(a, s), w = ev(b, s); if (isFinite(u) && isFinite(w)) pts.push([u, w]); } catch (e) { return false; } }
    if (pts.length < 4) return false;
    var i0 = 0, i1 = pts.findIndex(function (p) { return Math.abs(p[0] - pts[0][0]) > 1e-6; });
    if (i1 < 0) return false;
    var p = (pts[i1][1] - pts[i0][1]) / (pts[i1][0] - pts[i0][0]), q = pts[i0][1] - p * pts[i0][0];
    if (Math.abs(p) < 1e-9) return false;
    return pts.every(function (pt) { return close(pt[1], p * pt[0] + q); });
  }
  function solveC(tree, names, s, target) {   // every C (found by secant from several starts or by a scan) with tree(s, C) = target
    var roots = [];
    function F(c) { try { return ev(tree, Object.assign({}, s, { C: c })) - target; } catch (e) { return NaN; } }
    function add(c) { if (c !== null && isFinite(c) && Math.abs(F(c)) < 1e-7 * Math.max(1, Math.abs(target)) && !roots.some(function (r) { return Math.abs(r - c) < 1e-6; })) roots.push(c); }
    [-7.3, -2.1, -0.4, 0.6, 1.9, 4.7, 13.1].forEach(function (st) {
      var c0 = st, c1 = st + 0.37, f0 = F(c0), f1 = F(c1);
      for (var k = 0; k < 60 && isFinite(f1) && isFinite(f0) && f1 !== f0; k++) {
        var c2 = c1 - f1 * (c1 - c0) / (f1 - f0);
        if (!isFinite(c2)) break;
        c0 = c1; f0 = f1; c1 = c2; f1 = F(c1);
        if (Math.abs(f1) < 1e-12 * Math.max(1, Math.abs(target))) break;
      }
      add(c1);
    });
    var prev = -25, fp = F(prev);
    for (var c = -25 + 0.013; c <= 25; c += 0.013) {
      var fc = F(c);
      if (isFinite(fp) && isFinite(fc) && fp * fc <= 0) {
        var lo = prev, hi = c, flo = fp;
        for (var it = 0; it < 80; it++) { var mid = (lo + hi) / 2, fm = F(mid); if (flo * fm <= 0) hi = mid; else { lo = mid; flo = fm; } }
        add((lo + hi) / 2);
      }
      prev = c; fp = fc;
    }
    return roots;
  }
  function sameFamily(a, b, names) {   // every member of a's family is in b's, for two values of C
    var pts = samples(names.length ? names : ['x']);
    for (var c of [1.7, -0.6]) {
      var first = Object.assign({}, pts[1], { C: c }), target;
      try { target = ev(a, first); } catch (e) { return false; }
      if (!isFinite(target)) return false;
      var cands = solveC(b, names, pts[1], target);
      var ok = cands.some(function (cb) {
        for (var s of pts) {
          var u, w; try { u = ev(a, Object.assign({}, s, { C: c })); w = ev(b, Object.assign({}, s, { C: cb })); } catch (e) { return false; }
          if (isFinite(u) || isFinite(w)) if (!close(u, w, 1e-7)) return false;
        }
        return true;
      });
      if (!ok) return false;
    }
    return true;
  }

  function label(s) { var m = LHS.exec(clean(s)); return m ? m[0].replace(/\s*=\s*$/, '').replace(/\s+/g, '') : ''; }
  function gradeOne(k, typed) {
    var t = clean(typed);
    if (k.label && label(t) && label(t) !== k.label && !(/^[a-zA-Z]'?\(x\)$/.test(k.label) && /^[a-zA-Z]'?\(x\)$/.test(label(t)) && k.label.slice(1) === label(t).slice(1))) return { status: 'incorrect' };
    if (!t) return { status: 'empty' };
    if (t.length > 180) return { status: 'invalid', message: 'Enter only your final answer (180 characters maximum).' };
    try {
      if (k.kind === 'yesno') return { status: /^(yes|no)\b/i.test(t) ? (t.toLowerCase().slice(0, k.s.length) === k.s ? 'correct' : 'incorrect') : 'invalid', message: /^(yes|no)\b/i.test(t) ? undefined : 'Answer yes or no.' };
      if (k.kind === 'word') return { status: /^(does not exist|dne)$/i.test(t) ? 'correct' : 'incorrect' };
      if (k.kind === 'implicit') {
        var eq = t.split('=');
        if (eq.length !== 2) return { status: 'invalid', message: 'Enter an equation such as 2y² − x² = C.' };
        var L = parse(eq[0]), R = parse(eq[1]), tree = ['-', L, R];
        if (!vars(tree).C) return { status: 'invalid', message: 'Include the constant C.' };
        // put C alone: typed must be (expression in x, y) = C, or C on either side
        var lv = vars(L), rv = vars(R);
        var side = rv.C && !lv.C ? L : lv.C && !rv.C ? R : null;
        if (!side) return { status: 'self' };
        return { status: affine(k.tree, side, ['x', 'y']) ? 'correct' : 'incorrect' };
      }
      if (k.kind === 'constant') {
        var u = UNIT.exec(t) || unitTail(t), body = stripLabel(u ? t.slice(0, u.index) : t);
        if (k.inf) return { status: body.replace(/^\+/, '') === k.s ? 'correct' : (/^-?inf/.test(body) ? 'incorrect' : 'invalid') };
        var tv = parse(body);
        if (Object.keys(vars(tv)).length) return { status: 'invalid', message: 'Enter a number.' };
        if (u && k.unit && u[0].trim().replace(/\.$/, '') !== k.unit.replace(/\.$/, '')) return { status: 'incorrect', message: 'Check the units.' };
        if (k.exact && /\d\.\d/.test(body)) { var kv = ev(k.tree, {}); if (!Number.isInteger(kv)) return { status: 'invalid', message: 'Give an exact answer (no decimals).' }; }
        return { status: close(ev(k.tree, {}), ev(tv, {})) ? 'correct' : 'incorrect' };
      }
      var tb = stripLabel(t);
      if (/=/.test(tb)) return { status: 'invalid', message: 'Enter only the expression (you may start with y = ).' };
      var tt = parse(tb), tv2 = vars(tt);
      var extra = Object.keys(tv2).filter(function (n) { return n !== 'C' && k.names.indexOf(n) < 0 && !(k.names.length === 0); });
      if (extra.length) return { status: 'incorrect' };
      if (k.kind === 'expression') return { status: compareExpr(k.tree, tt, k.names) ? 'correct' : 'incorrect' };
      if (k.kind === 'antiderivative') {
        var ok = differByConstant(k.tree, tt, k.names);
        if (!tv2.C) return ok ? { status: 'incorrect', message: 'Include the constant of integration, + C.' } : { status: 'incorrect' };
        return { status: ok ? 'correct' : 'incorrect' };
      }
      if (k.kind === 'family') {
        if (!tv2.C) return { status: 'incorrect', message: 'A general solution includes the constant C.' };
        return { status: sameFamily(k.tree, tt, k.names) && sameFamily(tt, k.tree, k.names) ? 'correct' : 'incorrect' };
      }
    } catch (e) {
      return { status: 'invalid', message: 'Check the expression: use ^ or superscripts for powers, and parentheses for function inputs.' };
    }
    return { status: 'self' };
  }

  function isProduct(n) { while (n[0] === 'neg') n = n[1]; return n[0] === '*' || n[0] === '^' || n[0] === 'v' || n[0] === 'n'; }
  function hasFn(n) { if (n[0] === 'f') return true; if (n[0] === 'n' && n[1] === Math.E) return true; for (var k = 1; k < n.length; k++) if (Array.isArray(n[k]) && hasFn(n[k])) return true; return false; }
  /* Keys this grader handles even when the rational grader can read them: expressions, antiderivatives, families and
     implicit equations (the rational grader misreads superscripts such as x² in typed answers). */
  API.preferred = function (key) {
    var k = classify(key);
    if (!k || ['expression', 'antiderivative', 'family', 'implicit'].indexOf(k.kind) < 0) return false;
    return true;   // every expression key: sampling handles superscripts, functions and several variables
  };
  API.grade = function (key, typed, prompt) {
    var k = classify(key);
    if (!k) return { status: 'self' };
    k.label = label(key);
    // A question that asks for a particular form (vertex form, scientific notation, factor out the GCF, ...) is only
    // graded here when the typed text matches the key exactly; "Factor completely" is checked for a product below.
    var ask = String(prompt || '');
    if (/\b(vertex form|intercept form|factored form|standard form|expanded form|scientific notation|simplest form|GCF|greatest common factor|factor out)\b/i.test(ask) && !/Factor completely/i.test(ask)) {
      var norm = function (x) { return clean(x).replace(/\s+/g, ''); };
      return norm(typed) === norm(key) ? { status: 'correct' } : { status: 'self' };
    }
    if (prompt && /^Factor completely/i.test(String(prompt).split('\n').filter(function (l) { return /Factor completely/i.test(l); })[0] || '') && k.kind === 'expression') {
      var r0 = gradeOne(k, typed);
      if (r0.status === 'correct') { try { if (!isProduct(parse(stripLabel(clean(typed))))) return { status: 'incorrect', message: 'Write the answer in factored form.' }; } catch (e) { /* graded above */ } }
      return r0;
    }
    if (k.kind === 'compound') {
      var t = clean(typed);
      if (!t) return { status: 'empty' };
      var parts = k.sep === ' at x = ' ? t.split(/\s+at\s+(?:x\s*=\s*)?/) : t.split(/\s*[;,]\s*/).map(function (x) { return x.replace(/^[A-Za-z]\s*=\s*/, ''); });
      if (parts.length !== k.parts.length) return { status: 'invalid', message: k.sep === ' at x = ' ? 'Enter the value and where it occurs, such as 28 at x = 2.' : 'Enter each part, separated by a semicolon.' };
      var rs = parts.map(function (p, i) { return gradeOne(k.parts[i], p); });
      if (rs.some(function (r) { return r.status === 'invalid'; })) return rs.find(function (r) { return r.status === 'invalid'; });
      return { status: rs.every(function (r) { return r.status === 'correct'; }) ? 'correct' : 'incorrect' };
    }
    return gradeOne(k, typed);
  };
  API.parse = parse;   // for tests
})(typeof window !== 'undefined' ? window : globalThis);
