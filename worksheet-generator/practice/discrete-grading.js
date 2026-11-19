/* Discrete Math short-answer grading (Discrete Math audit #3, 2026-11-18).
   Bank keys the rational and exact graders cannot read:
   - sets such as {2, 4, 6}, {(1, 2), (2, 3)}, {{1, 3}, {2}} or ∅: order, spacing and repeats do not matter; {} = ∅
   - truth columns (TFTT) and truth-value rows such as (F, T)
   - lists: ordered (13, 11, 6 · 2, 5, 8, 11 · HH, HT, TH, TT) or, for players P1, P2, …, in any order;
     "q = 3, r = 2" style answers by name
   - statement forms in p, q, r, s: the same form up to the order of ∧ / ∨ / ↔ operands is correct; a form with a different
     truth column is incorrect; an equivalent form written differently is left to the teacher, because a question may ask for
     a particular rewriting (simplified, without →, …)
   - step orders such as BDAC (proof steps), in any spacing or punctuation
   - one-word answers: Yes / No, True / False, T / F, none, a single candidate letter.
   Anything else stays self-checked. */
(function (G) {
  'use strict';
  var MINUS = /[−–‑]/g;
  function clean(s) { return String(s == null ? '' : s).replace(MINUS, '-').replace(/\s+/g, ' ').trim().replace(/\.$/, ''); }

  /* ---------- sets ---------- */
  function splitTop(s) {
    var out = [], depth = 0, cur = '';
    for (var i = 0; i < s.length; i++) {
      var c = s[i];
      if (c === '{' || c === '(') depth++;
      if (c === '}' || c === ')') depth--;
      if (depth < 0) throw Error('brackets');
      if (c === ',' && depth === 0) { out.push(cur); cur = ''; } else cur += c;
    }
    if (depth !== 0) throw Error('brackets');
    out.push(cur);
    return out.map(function (x) { return x.trim(); });
  }
  function atom(x) {
    if (/^-?\d+(?:\.\d+)?$/.test(x)) return String(Number(x));
    if (/^-?\d+\/\d+$/.test(x)) return x;
    if (/^[A-Za-z][A-Za-z0-9]*$/.test(x)) return x;
    throw Error('element');
  }
  function canon(x) {
    x = x.trim();
    if (x === '∅' || x === '{}' || x === '{ }') return '{}';
    if (/^\{.*\}$/.test(x)) {
      var inner = x.slice(1, -1).trim();
      if (!inner) return '{}';
      var els = splitTop(inner).map(canon), uniq = [];
      els.forEach(function (e) { if (uniq.indexOf(e) < 0) uniq.push(e); });
      return '{' + uniq.sort().join(',') + '}';
    }
    if (/^\(.*\)$/.test(x)) return '(' + splitTop(x.slice(1, -1)).map(canon).join(',') + ')';
    return atom(x);
  }
  function isSetKey(k) { return /^\{.*\}$/.test(k) || k === '∅'; }

  /* ---------- statement forms ---------- */
  var FORM = /^[pqrs¬∧∨→↔⊕() ]+$/;
  function normForm(s) {
    return clean(s).replace(/<->|<=>|\biff\b/gi, '↔').replace(/->|=>/g, '→').replace(/\bnot\b|~|!/gi, '¬')
      .replace(/\band\b|\^|&+/gi, '∧').replace(/\bor\b|\|+/gi, '∨').replace(/\bxor\b/gi, '⊕')
      .replace(/\s+/g, '');
  }
  function parse(src) {
    var t = src, i = 0, prec = { '∧': 3, '∨': 2, '⊕': 2, '→': 1, '↔': 0 };
    function prim() {
      var c = t[i];
      if (c === '¬') { i++; return { op: '¬', a: prim() }; }
      if (c === '(') { i++; var v = ex(0); if (t[i] !== ')') throw Error('paren'); i++; return v; }
      if (/[pqrs]/.test(c)) { i++; return { v: c }; }
      throw Error('token');
    }
    function ex(min) {
      var l = prim();
      while (i < t.length && prec[t[i]] !== undefined && prec[t[i]] >= min) {
        var op = t[i++], r = ex(op === '→' || op === '↔' ? prec[op] : prec[op] + 1);
        l = { op: op, a: l, b: r };
      }
      return l;
    }
    var v = ex(0);
    if (i !== t.length) throw Error('trailing');
    return v;
  }
  function evalForm(n, env) {
    if (n.v) return env[n.v];
    if (n.op === '¬') return !evalForm(n.a, env);
    var a = evalForm(n.a, env), b = evalForm(n.b, env);
    return n.op === '∧' ? a && b : n.op === '∨' ? a || b : n.op === '⊕' ? a !== b : n.op === '→' ? (!a || b) : a === b;
  }
  function vars(n, out) { out = out || {}; if (n.v) out[n.v] = 1; if (n.a) vars(n.a, out); if (n.b) vars(n.b, out); return out; }
  function shape(n) {   // canonical string up to the order of commutative operands (flattening ∧ / ∨ chains)
    if (n.v) return n.v;
    if (n.op === '¬') return '¬' + shape(n.a);
    if (n.op === '∧' || n.op === '∨') {
      var parts = [];
      (function flat(m) { if (m.op === n.op) { flat(m.a); flat(m.b); } else parts.push(shape(m)); })(n);
      return '(' + parts.sort().join(n.op) + ')';
    }
    var a = shape(n.a), b = shape(n.b);
    if (n.op === '↔' || n.op === '⊕') { var s = [a, b].sort(); a = s[0]; b = s[1]; }
    return '(' + a + n.op + b + ')';
  }
  function column(n, vs) {
    var out = '';
    for (var m = 0; m < 1 << vs.length; m++) {
      var env = {};
      vs.forEach(function (v, k) { env[v] = !((m >> (vs.length - 1 - k)) & 1); });
      out += evalForm(n, env) ? 'T' : 'F';
    }
    return out;
  }
  function isFormKey(k) { return FORM.test(k) && /[pqrs]/.test(k) && /[¬∧∨→↔⊕]/.test(k); }

  /* ---------- lists ---------- */
  var TOKEN = /^(?:-?\d+(?:\.\d+)?|-?\d+\/\d+|P\d+|[A-Z]{1,4}|[TF]|[a-z]{3,10})$/;
  function listOf(k) {
    if (/^P\d+$/.test(k)) return [k];
    if (!/,/.test(k) || /[{}]/.test(k) || /^\(.*\)$/.test(k)) return null;
    var parts = k.split(/\s*,\s*/);
    if (parts.length < 2 || !parts.every(function (x) { return TOKEN.test(x); })) return null;
    return parts;
  }
  function namedOf(k) {   // q = 3, r = 2
    var parts = k.split(/\s*,\s*/), out = {};
    if (parts.length < 2) return null;
    for (var i = 0; i < parts.length; i++) {
      var m = /^([a-z])\s*=\s*(-?\d+(?:\/\d+)?)$/.exec(parts[i]);
      if (!m) return null;
      out[m[1]] = m[2];
    }
    return out;
  }
  function tupleTF(k) { var m = /^\(\s*([TF](?:\s*,\s*[TF])+)\s*\)$/.exec(k); return m ? m[1].replace(/\s+/g, '') : null; }

  var WORDS = /^(?:yes|no|true|false|none|t|f)$/i;
  function kind(k) {
    k = clean(k);
    if (isSetKey(k)) { try { canon(k); return 'set'; } catch (e) { return null; } }
    if (/^[TF]{2,}$/.test(k)) return 'column';
    if (tupleTF(k)) return 'tuple';
    if (namedOf(k)) return 'named';
    if (listOf(k)) return 'list';
    if (isFormKey(k)) { try { parse(normForm(k)); return 'form'; } catch (e) { return null; } }
    if (/^[A-H]{3,8}$/.test(k) && new Set(k).size === k.length) return 'order';
    if (WORDS.test(k)) return 'word';
    if (/^[A-E]$/.test(k)) return 'letter';
    if (/^P\d+$/.test(k)) return 'list';
    if (/^[pqrs]$/.test(k)) return 'form';
    return null;
  }
  function supports(answer) { return typeof answer === 'string' && kind(answer) !== null; }

  function grade(answer, typed) {
    var k = clean(answer), t = clean(typed), kd = kind(k);
    if (!t) return { status: 'invalid', message: 'Enter an answer.' };
    try {
      if (kd === 'set') {
        if (!/^\{.*\}$|^∅$/.test(t)) return { status: 'invalid', message: 'Write a set in braces, such as {1, 2, 3}, or ∅ for the empty set.' };
        return { status: canon(k) === canon(t) ? 'correct' : 'incorrect' };
      }
      if (kd === 'column') {
        var col = t.toUpperCase().replace(/[\s,]/g, '');
        if (!/^[TF]+$/.test(col)) return { status: 'invalid', message: 'Write the column as T and F letters, such as TFTT.' };
        return { status: col === k ? 'correct' : 'incorrect' };
      }
      if (kd === 'tuple') {
        var tt = tupleTF(t.toUpperCase()) || (/^[TF](?:\s*,?\s*[TF])+$/.test(t.toUpperCase()) ? t.toUpperCase().replace(/[\s,]/g, '').split('').join(',') : null);
        if (!tt) return { status: 'invalid', message: 'Write the row like (T, F).' };
        return { status: tt === tupleTF(k) ? 'correct' : 'incorrect' };
      }
      if (kd === 'named') {
        var a = namedOf(k), b = namedOf(t.replace(/\s*;\s*/g, ', '));
        if (!b) return { status: 'invalid', message: 'Write the answer like ' + k + '.' };
        var ks = Object.keys(a);
        return { status: ks.length === Object.keys(b).length && ks.every(function (x) { return b[x] !== undefined && Number(eval0(b[x])) === Number(eval0(a[x])); }) ? 'correct' : 'incorrect' };
      }
      if (kd === 'list') {
        var A = listOf(k), T = t.replace(/\s+and\s+/gi, ', ').split(/\s*,\s*|\s+/).filter(Boolean);
        var num = function (x) { return /^-?\d+(?:\.\d+)?$|^-?\d+\/\d+$/.test(x) ? String(eval0(x)) : x.toUpperCase(); };
        A = A.map(num); T = T.map(num);
        if (A.every(function (x) { return /^P\d+$/.test(x); })) { A = A.slice().sort(); T = T.slice().sort(); }
        return { status: A.length === T.length && A.every(function (x, i) { return x === T[i]; }) ? 'correct' : 'incorrect' };
      }
      if (kd === 'form') {
        var kn = parse(normForm(k)), tn;
        try { tn = parse(normForm(t)); } catch (e) { return { status: 'invalid', message: 'Use p, q, r with ¬ (not), ∧ (and), ∨ (or), → and ↔.' }; }
        if (shape(kn) === shape(tn)) return { status: 'correct' };
        var vs = Object.keys(Object.assign(vars(kn), vars(tn))).sort();
        return column(kn, vs) === column(tn, vs) ? { status: 'self' } : { status: 'incorrect' };
      }
      if (kd === 'order') {
        var o = t.toUpperCase().replace(/[^A-H]/g, '');
        if (o.length !== k.length) return { status: 'invalid', message: 'Answer with the ' + k.length + ' letters in order, like ' + 'ABCDEFGH'.slice(0, k.length) + '.' };
        return { status: o === k ? 'correct' : 'incorrect' };
      }
      if (kd === 'word') {
        var w = function (x) { x = x.toLowerCase(); return x === 't' ? 'true' : x === 'f' ? 'false' : x; };
        return { status: w(t) === w(k) ? 'correct' : WORDS.test(t) ? 'incorrect' : 'invalid' };
      }
      if (kd === 'letter') return /^[A-Za-z]$/.test(t) ? { status: t.toUpperCase() === k ? 'correct' : 'incorrect' } : { status: 'invalid', message: 'Answer with the letter.' };
    } catch (e) { return { status: 'invalid', message: 'The answer could not be read.' }; }
    return { status: 'self' };
  }
  function eval0(x) { var m = /^(-?\d+)\/(\d+)$/.exec(x); return m ? Number(m[1]) / Number(m[2]) : Number(x); }

  G.MKDISCRETE = { supports: supports, grade: grade, kind: kind };
})(typeof window !== 'undefined' ? window : globalThis);
