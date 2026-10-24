/* Mr. K's Classroom — Menu Assessment Generator: independent math checker.

   This file deliberately shares NO code with the problem generators (it does not use
   core/frac.js, core/tex.js or any skill file). It reads the math exactly as a student
   sees it (the TeX inside ⟨…⟩, or plain calculator syntax a teacher types), parses it
   with its own parser, and works with its own exact arithmetic (BigInt rationals and
   multivariate polynomials / rational functions). It is used for:
     • automated tests over large batches of generated problems,
     • re-checking every generated problem in the browser before it is shown,
     • checking teacher-edited problems (never trusting the old generated answer).
*/
(function (G) {
  'use strict';
  var NS = (G.MKMENU = G.MKMENU || {});

  /* ---------------- exact rationals (BigInt) ---------------- */
  function bgcd(a, b) { if (a < 0n) a = -a; if (b < 0n) b = -b; while (b) { var t = a % b; a = b; b = t; } return a; }
  function Q(n, d) {
    n = BigInt(n); d = d === undefined ? 1n : BigInt(d);
    if (d === 0n) throw new CheckError('division by zero');
    if (d < 0n) { n = -n; d = -d; }
    var g = bgcd(n, d); if (g > 1n) { n /= g; d /= g; }
    if (n === 0n) d = 1n;
    this.n = n; this.d = d;
  }
  Q.ZERO = new Q(0); Q.ONE = new Q(1);
  Q.prototype.add = function (o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); };
  Q.prototype.sub = function (o) { return new Q(this.n * o.d - o.n * this.d, this.d * o.d); };
  Q.prototype.mul = function (o) { return new Q(this.n * o.n, this.d * o.d); };
  Q.prototype.div = function (o) { if (o.n === 0n) throw new CheckError('division by zero'); return new Q(this.n * o.d, this.d * o.n); };
  Q.prototype.neg = function () { return new Q(-this.n, this.d); };
  Q.prototype.isZero = function () { return this.n === 0n; };
  Q.prototype.isInt = function () { return this.d === 1n; };
  Q.prototype.eq = function (o) { return this.n === o.n && this.d === o.d; };
  Q.prototype.toString = function () { return this.d === 1n ? String(this.n) : this.n + '/' + this.d; };
  Q.prototype.pow = function (k) {
    if (k < 0) return Q.ONE.div(this.pow(-k));
    var r = Q.ONE; for (var i = 0; i < k; i++) r = r.mul(this); return r;
  };
  Q.parseDecimal = function (s) {
    var m = /^(\d*)(?:\.(\d+))?$/.exec(s); if (!m) throw new CheckError('bad number ' + s);
    var ip = m[1] || '0', fp = m[2] || '';
    return new Q(BigInt(ip + fp), 10n ** BigInt(fp.length));
  };

  function CheckError(msg) { this.message = msg; this.name = 'CheckError'; }
  CheckError.prototype = Object.create(Error.prototype);

  /* ---------------- tokenizer ---------------- */
  // Accepts the TeX subset the generators print and plain syntax teachers type:
  //   3(x-4)+2 = 5x/2,  \frac{x+1}{3},  \dfrac, \left( \right), \cdot, \times, ^, x^{2}, −, ·
  function tokenize(src) {
    var s = String(src)
      .replace(/[⟨⟩$]/g, ' ')
      .replace(/\\left|\\right|\\displaystyle/g, '')
      .replace(/\\dfrac|\\tfrac/g, '\\frac')
      .replace(/\\[,;:! ]|~/g, ' ')
      .replace(/[−–]/g, '-').replace(/[·×]|\\cdot|\\times/g, '*').replace(/÷|\\div/g, '/')
      .replace(/\\le(q)?\b|≤/g, '≤').replace(/\\ge(q)?\b|≥/g, '≥')
      .replace(/\\pi\b|π/g, 'π');
    var out = [], i = 0;
    while (i < s.length) {
      var c = s[i];
      if (/\s/.test(c)) { i++; continue; }
      if (/[0-9.]/.test(c)) {
        var j = i; while (j < s.length && /[0-9.]/.test(s[j])) j++;
        var txt = s.slice(i, j); if ((txt.match(/\./g) || []).length > 1) throw new CheckError('bad number ' + txt);
        out.push({ t: 'num', v: Q.parseDecimal(txt) }); i = j; continue;
      }
      if (c === '\\') {
        var m = /^\\([a-zA-Z]+)/.exec(s.slice(i));
        if (!m) throw new CheckError('unknown symbol ' + s.slice(i, i + 3));
        if (m[1] === 'frac') { out.push({ t: 'frac' }); i += m[0].length; continue; }
        if (m[1] === 'text' || m[1] === 'mathrm') throw new CheckError('text inside math');
        throw new CheckError('unsupported command \\' + m[1]);
      }
      if (/[a-zA-Zπ]/.test(c)) { out.push({ t: 'var', v: c }); i++; continue; }
      if ('+-*/^(){}[]=<>≤≥'.indexOf(c) >= 0) {
        if (c === '[') c = '('; if (c === ']') c = ')';
        out.push({ t: c }); i++; continue;
      }
      if (c === '_') throw new CheckError('subscripts are not supported');
      throw new CheckError('unexpected character ' + c);
    }
    return out;
  }

  /* ---------------- parser -> AST ---------------- */
  // AST: {k:'num',v:Q} {k:'var',v:'x'} {k:'add',a,b} {k:'sub',a,b} {k:'mul',a,b} {k:'div',a,b} {k:'neg',a} {k:'pow',a,e:int}
  //      {k:'grp',a}  (a parenthesised group — kept so form checks can see parentheses)
  function Parser(tokens) { this.t = tokens; this.i = 0; }
  Parser.prototype.peek = function () { return this.t[this.i]; };
  Parser.prototype.take = function (type) {
    var tk = this.t[this.i];
    if (!tk || (type && tk.t !== type)) throw new CheckError('expected ' + type + (tk ? ' but found ' + tk.t : ' at end'));
    this.i++; return tk;
  };
  Parser.prototype.expr = function () {
    var a = this.term();
    for (;;) {
      var tk = this.peek();
      if (tk && (tk.t === '+' || tk.t === '-')) { this.i++; var b = this.term(); a = { k: tk.t === '+' ? 'add' : 'sub', a: a, b: b }; }
      else return a;
    }
  };
  Parser.prototype.startsAtom = function (tk) { return tk && (tk.t === 'num' || tk.t === 'var' || tk.t === '(' || tk.t === 'frac' || tk.t === '{'); };
  Parser.prototype.term = function () {
    var a = this.unary();
    for (;;) {
      var tk = this.peek();
      if (tk && (tk.t === '*' || tk.t === '/')) { this.i++; var b = this.unary(); a = { k: tk.t === '*' ? 'mul' : 'div', a: a, b: b }; }
      else if (this.startsAtom(tk)) {
        if (tk.t === 'num' && endsWithNumber(a)) throw new CheckError('two numbers written next to each other');
        var c = this.power(); a = { k: 'mul', a: a, b: c, implicit: true };
      }
      else return a;
    }
  };
  function endsWithNumber(node) { while (node.k === 'mul') node = node.b; return node.k === 'num' || node.k === 'pow'; }
  Parser.prototype.unary = function () {
    var tk = this.peek();
    if (tk && tk.t === '-') { this.i++; return { k: 'neg', a: this.unary() }; }
    if (tk && tk.t === '+') { this.i++; return this.unary(); }
    return this.power();
  };
  Parser.prototype.power = function () {
    var a = this.atom();
    var tk = this.peek();
    if (tk && tk.t === '^') {
      this.i++;
      var e = this.peek(), neg = false, val;
      if (e && e.t === '{') { this.i++; if (this.peek() && this.peek().t === '-') { neg = true; this.i++; } val = this.take('num').v; this.take('}'); }
      else { if (e && e.t === '-') { neg = true; this.i++; } val = this.take('num').v; }
      if (!val.isInt() || val.n > 12n) throw new CheckError('unsupported exponent');
      a = { k: 'pow', a: a, e: Number(val.n) * (neg ? -1 : 1) };
    }
    return a;
  };
  Parser.prototype.atom = function () {
    var tk = this.take();
    if (tk.t === 'num') return { k: 'num', v: tk.v };
    if (tk.t === 'var') return { k: 'var', v: tk.v };
    if (tk.t === '(') { var a = this.expr(); this.take(')'); return { k: 'grp', a: a }; }
    if (tk.t === '{') { var b = this.expr(); this.take('}'); return b; }
    if (tk.t === 'frac') {
      this.take('{'); var n = this.expr(); this.take('}');
      this.take('{'); var d = this.expr(); this.take('}');
      return { k: 'div', a: n, b: d, frac: true };
    }
    throw new CheckError('unexpected ' + tk.t);
  };

  function parseExpr(src) {
    var toks = tokenize(src); if (!toks.length) throw new CheckError('empty expression');
    var p = new Parser(toks), a = p.expr();
    if (p.i !== toks.length) throw new CheckError('could not read "' + src + '"');
    return a;
  }
  /* "lhs = rhs" (or an inequality) -> {lhs, rhs, rel} */
  function parseRelation(src) {
    var toks = tokenize(src), idx = -1, rel = null;
    toks.forEach(function (tk, i) { if ('=<>≤≥'.indexOf(tk.t) >= 0) { if (idx >= 0) throw new CheckError('more than one = or inequality sign'); idx = i; rel = tk.t; } });
    if (idx < 0) throw new CheckError('no = sign');
    var L = new Parser(toks.slice(0, idx)), R = new Parser(toks.slice(idx + 1));
    var lhs = L.expr(), rhs = R.expr();
    if (L.i !== idx || R.i !== toks.length - idx - 1) throw new CheckError('could not read "' + src + '"');
    return { lhs: lhs, rhs: rhs, rel: rel };
  }

  /* ---------------- polynomials & rational functions ---------------- */
  // Poly: Map from monomial key ("x^2*y^1", "" for constant) to Q.
  function monoKey(m) { return Object.keys(m).sort().filter(function (v) { return m[v]; }).map(function (v) { return v + '^' + m[v]; }).join('*'); }
  function monoOf(key) { var m = {}; if (key) key.split('*').forEach(function (p) { var s = p.split('^'); m[s[0]] = +s[1]; }); return m; }
  function P(map) { this.m = map || new Map(); }
  P.const = function (q) { var p = new P(); if (!q.isZero()) p.m.set('', q); return p; };
  P.variable = function (v) { var p = new P(); p.m.set(v + '^1', Q.ONE); return p; };
  P.prototype.add = function (o) {
    var r = new Map(this.m);
    o.m.forEach(function (q, k) { var s = (r.get(k) || Q.ZERO).add(q); if (s.isZero()) r.delete(k); else r.set(k, s); });
    return new P(r);
  };
  P.prototype.neg = function () { var r = new Map(); this.m.forEach(function (q, k) { r.set(k, q.neg()); }); return new P(r); };
  P.prototype.sub = function (o) { return this.add(o.neg()); };
  P.prototype.mul = function (o) {
    var r = new P();
    this.m.forEach(function (q1, k1) {
      o.m.forEach(function (q2, k2) {
        var a = monoOf(k1), b = monoOf(k2);
        Object.keys(b).forEach(function (v) { a[v] = (a[v] || 0) + b[v]; });
        var t = new P(); t.m.set(monoKey(a), q1.mul(q2)); r = r.add(t);
      });
    });
    return r;
  };
  P.prototype.isZero = function () { return this.m.size === 0; };
  P.prototype.isConst = function () { return this.m.size === 0 || (this.m.size === 1 && this.m.has('')); };
  P.prototype.constVal = function () { return this.m.get('') || Q.ZERO; };
  P.prototype.vars = function () { var s = {}; this.m.forEach(function (q, k) { Object.keys(monoOf(k)).forEach(function (v) { s[v] = 1; }); }); return Object.keys(s).sort(); };
  P.prototype.degreeIn = function (v) { var d = 0; this.m.forEach(function (q, k) { d = Math.max(d, monoOf(k)[v] || 0); }); return d; };
  /* coefficient (as a polynomial in the other variables) of v^k */
  P.prototype.coeffOf = function (v, k) {
    var r = new P();
    this.m.forEach(function (q, key) { var m = monoOf(key); if ((m[v] || 0) === k) { delete m[v]; var t = new P(); t.m.set(monoKey(m), q); r = r.add(t); } });
    return r;
  };
  P.prototype.evalAt = function (env) {
    var tot = Q.ZERO;
    this.m.forEach(function (q, key) {
      var m = monoOf(key), t = q;
      Object.keys(m).forEach(function (v) { if (!env[v]) throw new CheckError('no value for ' + v); t = t.mul(env[v].pow(m[v])); });
      tot = tot.add(t);
    });
    return tot;
  };
  P.prototype.toString = function () { var a = []; this.m.forEach(function (q, k) { a.push(q + (k ? '·' + k : '')); }); return a.sort().join(' + ') || '0'; };

  // Rational function n/d (d never the zero polynomial).
  function RF(n, d) { this.n = n; this.d = d || P.const(Q.ONE); }
  RF.prototype.add = function (o) { return new RF(this.n.mul(o.d).add(o.n.mul(this.d)), this.d.mul(o.d)); };
  RF.prototype.sub = function (o) { return new RF(this.n.mul(o.d).sub(o.n.mul(this.d)), this.d.mul(o.d)); };
  RF.prototype.mul = function (o) { return new RF(this.n.mul(o.n), this.d.mul(o.d)); };
  RF.prototype.div = function (o) { if (o.n.isZero()) throw new CheckError('division by zero'); return new RF(this.n.mul(o.d), this.d.mul(o.n)); };
  RF.prototype.isPoly = function () { return this.d.isConst(); };
  RF.prototype.asPoly = function () { var c = this.d.constVal(); return this.n.mul(P.const(Q.ONE.div(c))); };

  function toRF(node) {
    switch (node.k) {
      case 'num': return new RF(P.const(node.v));
      case 'var': return new RF(P.variable(node.v));
      case 'grp': return toRF(node.a);
      case 'neg': var a = toRF(node.a); return new RF(a.n.neg(), a.d);
      case 'add': return toRF(node.a).add(toRF(node.b));
      case 'sub': return toRF(node.a).sub(toRF(node.b));
      case 'mul': return toRF(node.a).mul(toRF(node.b));
      case 'div': return toRF(node.a).div(toRF(node.b));
      case 'pow':
        var base = toRF(node.a), r = new RF(P.const(Q.ONE));
        for (var i = 0; i < Math.abs(node.e); i++) r = r.mul(base);
        return node.e < 0 ? new RF(P.const(Q.ONE)).div(r) : r;
    }
    throw new CheckError('bad node ' + node.k);
  }
  function evalNode(node, env) {
    switch (node.k) {
      case 'num': return node.v;
      case 'var': if (!env[node.v]) throw new CheckError('no value for ' + node.v); return env[node.v];
      case 'grp': return evalNode(node.a, env);
      case 'neg': return evalNode(node.a, env).neg();
      case 'add': return evalNode(node.a, env).add(evalNode(node.b, env));
      case 'sub': return evalNode(node.a, env).sub(evalNode(node.b, env));
      case 'mul': return evalNode(node.a, env).mul(evalNode(node.b, env));
      case 'div': return evalNode(node.a, env).div(evalNode(node.b, env));
      case 'pow': return evalNode(node.a, env).pow(node.e);
    }
    throw new CheckError('bad node');
  }
  function varsOf(node, acc) {
    acc = acc || {};
    if (node.k === 'var') acc[node.v] = 1;
    ['a', 'b'].forEach(function (s) { if (node[s]) varsOf(node[s], acc); });
    return acc;
  }
  function substitute(node, v, repl) {
    if (node.k === 'var') return node.v === v ? { k: 'grp', a: repl } : node;
    var c = Object.assign({}, node);
    if (c.a) c.a = substitute(c.a, v, repl);
    if (c.b) c.b = substitute(c.b, v, repl);
    return c;
  }

  /* ---------------- answers ---------------- */
  // Reads a displayed answer: "x=4", "x = -\frac{3}{2}", "4", "No solution", "Infinitely many solutions",
  // "One solution: x=3", "h=4 hours", "$9" ...
  function readNumber(src) {
    var s = String(src).replace(/[⟨⟩$]/g, ' ').replace(/,(?=\d{3}\b)/g, '').trim();
    var r = parseExpr(s), rf = toRF(r);
    if (!rf.isPoly() || !rf.asPoly().isConst()) throw new CheckError('not a number: ' + src);
    return rf.asPoly().constVal();
  }
  function classifyText(txt) {
    var t = String(txt).toLowerCase();
    if (/no solution/.test(t)) return 'none';
    if (/infinite|all real|every real|identity/.test(t)) return 'all';
    return null;
  }

  /* ---------------- core checks ---------------- */
  // Solve a relation that is linear in v after clearing denominators.
  // Returns {kind:'one', value:Q} | {kind:'none'} | {kind:'all'}; throws if not linear in v.
  function solveLinear(eqSrc, v) {
    var rel = typeof eqSrc === 'string' ? parseRelation(eqSrc) : eqSrc;
    if (rel.rel !== '=') throw new CheckError('not an equation');
    var vars = Object.keys(Object.assign(varsOf(rel.lhs), varsOf(rel.rhs)));
    vars.forEach(function (w) { if (w !== v) throw new CheckError('unexpected variable ' + w); });
    var f = toRF(rel.lhs).sub(toRF(rel.rhs));
    var num = f.n, den = f.d;
    var deg = num.degreeIn(v);
    if (deg > 1) throw new CheckError('equation is not linear in ' + v);
    var a = num.coeffOf(v, 1).constVal(), b = num.coeffOf(v, 0).constVal();
    var res;
    if (a.isZero()) res = b.isZero() ? { kind: 'all' } : { kind: 'none' };
    else res = { kind: 'one', value: b.neg().div(a) };
    // values that make a denominator zero are excluded
    if (res.kind === 'one') {
      var env = {}; env[v] = res.value;
      if (den.evalAt(env).isZero()) res = { kind: 'none', excluded: res.value };
    } else if (res.kind === 'all' && !den.isConst()) res.restricted = true;
    return res;
  }

  function equivalent(srcA, srcB) {
    var a = typeof srcA === 'string' ? parseExpr(srcA) : srcA, b = typeof srcB === 'string' ? parseExpr(srcB) : srcB;
    var d = toRF(a).sub(toRF(b));
    return d.n.isZero();
  }

  /* Is an expression written in simplest form? (sum of distinct like-terms, no parentheses,
     no 1/0 coefficients, constants combined, fractions only as numeric coefficients). */
  function simplifiedForm(src) {
    var node = typeof src === 'string' ? parseExpr(src) : src;
    var terms = [], problems = [];
    (function flatten(n, sign) {
      if (n.k === 'add') { flatten(n.a, sign); flatten(n.b, sign); }
      else if (n.k === 'sub') { flatten(n.a, sign); flatten(n.b, -sign); }
      else terms.push(n);
    })(node, 1);
    var seen = {};
    terms.forEach(function (t, i) {
      if (i > 0 && t.k === 'neg') problems.push('double sign');
      var core = t.k === 'neg' ? t.a : t;
      var info = monomialShape(core);
      if (!info) { problems.push('term is not a single monomial'); return; }
      if (info.coef && info.coef.isZero()) problems.push('zero term');
      if (info.coef && info.coef.eq(Q.ONE) && info.key !== '' && info.explicitOne) problems.push('coefficient 1 written');
      if (seen[info.key]) problems.push('like terms not combined'); seen[info.key] = 1;
    });
    return { ok: problems.length === 0, problems: problems };
  }
  // number? * vars^k ...  or  \frac{num}{num} * vars  or  vars/num
  function monomialShape(n) {
    var factors = [];
    (function f(x) { if (x.k === 'mul') { f(x.a); f(x.b); } else if (x.k === 'neg' && factors.length === 0) f(x.a); else factors.push(x); })(n);
    var coef = null, explicitOne = false, mono = {};
    for (var i = 0; i < factors.length; i++) {
      var x = factors[i];
      if (x.k === 'num') { if (coef) return null; coef = x.v; explicitOne = x.v.eq(Q.ONE); }
      else if (x.k === 'div' && x.a.k === 'num' && x.b.k === 'num') { if (coef) return null; coef = x.a.v.div(x.b.v); }
      else if (x.k === 'div' && x.b.k === 'num' && varsOnly(x.a)) { if (coef) return null; coef = Q.ONE.div(x.b.v); addVars(x.a, mono); }
      else if (x.k === 'var') mono[x.v] = (mono[x.v] || 0) + 1;
      else if (x.k === 'pow' && x.a.k === 'var' && x.e > 0) mono[x.a.v] = (mono[x.a.v] || 0) + x.e;
      else return null;
    }
    return { coef: coef, key: monoKey(mono), explicitOne: explicitOne };
  }
  function varsOnly(n) { return n.k === 'var' || (n.k === 'mul' && varsOnly(n.a) && varsOnly(n.b)) || (n.k === 'pow' && n.a.k === 'var'); }
  function addVars(n, mono) { if (n.k === 'var') mono[n.v] = (mono[n.v] || 0) + 1; else if (n.k === 'pow') mono[n.a.v] = (mono[n.a.v] || 0) + n.e; else { addVars(n.a, mono); addVars(n.b, mono); } }

  /* Literal equation: does "v = expr" make the original equation an identity? */
  function checkLiteral(eqSrc, v, answerSrc) {
    var rel = parseRelation(eqSrc), ans = parseRelation(answerSrc);
    var lhsIsV = ans.lhs.k === 'var' && ans.lhs.v === v, rhsIsV = ans.rhs.k === 'var' && ans.rhs.v === v;
    if (!lhsIsV && !rhsIsV) return { ok: false, reason: 'answer must start with ' + v + ' =' };
    var expr = lhsIsV ? ans.rhs : ans.lhs;
    if (varsOf(expr)[v]) return { ok: false, reason: v + ' still appears on the other side' };
    var L = substitute(rel.lhs, v, expr), R = substitute(rel.rhs, v, expr);
    var d = toRF(L).sub(toRF(R));
    if (!d.n.isZero()) return { ok: false, reason: 'substituting the answer does not satisfy the formula' };
    return { ok: true };
  }

  /* Plain-text math (what a teacher types) -> TeX for display. */
  function toTeX(src, opts) {
    var rel = null, s = String(src);
    try { rel = parseRelation(s); } catch (e) { rel = null; }
    if (rel) return texNode(rel.lhs) + ({ '=': '=', '<': '<', '>': '>', '≤': '\\le ', '≥': '\\ge ' })[rel.rel] + texNode(rel.rhs);
    return texNode(parseExpr(s));
  }
  function texNode(n, parentPrec) {
    var prec = { add: 1, sub: 1, neg: 2, mul: 3, div: 3, pow: 4, num: 5, var: 5, grp: 5 }[n.k];
    var out;
    switch (n.k) {
      case 'num': out = n.v.isInt() ? String(n.v.n) : '\\frac{' + String(n.v.n < 0n ? -n.v.n : n.v.n) + '}{' + n.v.d + '}'; if (n.v.n < 0n && !n.v.isInt()) out = '-' + out; break;
      case 'var': out = n.v === 'π' ? '\\pi ' : n.v; break;
      case 'grp': out = '(' + texNode(n.a, 0) + ')'; break;
      case 'neg': out = '-' + texNode(n.a, 2); break;
      case 'add': out = texNode(n.a, 1) + '+' + texNode(n.b, 1); break;
      case 'sub': out = texNode(n.a, 1) + '-' + texNode(n.b, 2); break;
      case 'mul':
        var A = texNode(n.a, 3), B = texNode(n.b, 3);
        out = n.implicit || /^[a-zπ(\\]/i.test(B) && !/^\\frac/.test(B) ? A + B : A + '\\cdot ' + B; break;
      case 'div': out = '\\frac{' + texNode(n.a, 0) + '}{' + texNode(n.b, 0) + '}'; break;
      case 'pow': out = texNode(n.a, 4) + '^{' + n.e + '}'; break;
    }
    return parentPrec !== undefined && prec < parentPrec && n.k !== 'grp' ? '(' + out + ')' : out;
  }

  /* math snippets displayed in a prompt */
  function snippets(markup) { var r = [], re = /⟨([^⟩]*)⟩/g, m; while ((m = re.exec(markup))) r.push(m[1]); return r; }
  function plainText(markup) { return String(markup).replace(/⟨[^⟩]*⟩/g, ' ').replace(/<[^>]+>/g, ' '); }
  /* numbers written in the words of a prompt, in order (e.g. "$40 plus $25 per hour") */
  function numbersInText(markup) {
    return (plainText(markup).replace(/,(?=\d{3}\b)/g, '').match(/-?\d+(?:\.\d+)?/g) || []).map(function (t) {
      var neg = t[0] === '-'; var q = Q.parseDecimal(neg ? t.slice(1) : t); return neg ? q.neg() : q;
    });
  }

  NS.check = {
    Q: Q, CheckError: CheckError, tokenize: tokenize, parseExpr: parseExpr, parseRelation: parseRelation,
    toRF: toRF, evalNode: evalNode, varsOf: varsOf, solveLinear: solveLinear, equivalent: equivalent,
    simplifiedForm: simplifiedForm, checkLiteral: checkLiteral, readNumber: readNumber, classifyText: classifyText,
    toTeX: toTeX, snippets: snippets, plainText: plainText, numbersInText: numbersInText, monoKey: monoKey
  };
})(typeof window !== 'undefined' ? window : globalThis);
