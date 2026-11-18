/* Exact comparison of constant answers for authored-bank short answers (Precalculus audit #2, 2026-11-18).
   Values are exact sums of rational · √r · πᵏ · iᵐ terms (r square-free, BigInt rationals; no floating point).
   Supported answers: exact numbers such as (√3)/2, -(2√3)/3, 7π/2, 3 - 4i; tuples and vectors (√2, -4√2), ⟨1, -10⟩;
   matrices [6, 5; 1, 1]; interval unions (-∞, -4) ∪ (-4, ∞); and solution lists x = π/6 or x = 7π/6.
   A typed answer must also be in simplest form, so a student cannot pass by retyping the question: radicands
   square-free, like terms combined, no product of sums, and no decimals where the key is exact.
   MKEXACT.supports(key) → kind or null; MKEXACT.grade(key, typed) → {status, message?}. */
(function (G) {
'use strict';
var API = G.MKEXACT = {};

// ---------- rationals
function rat(n, d) { n = BigInt(n); d = BigInt(d === undefined ? 1 : d); if (!d) throw Error('division by zero'); if (d < 0n) { n = -n; d = -d; } var a = n < 0n ? -n : n, b = d; while (b) { var t = a % b; a = b; b = t; } var g = a || 1n; return [n / g, d / g]; }
function radd(a, b) { return rat(a[0] * b[1] + b[0] * a[1], a[1] * b[1]); }
function rmul(a, b) { return rat(a[0] * b[0], a[1] * b[1]); }
function rinv(a) { if (!a[0]) throw Error('division by zero'); return rat(a[1], a[0]); }
function decimal(s) { var p = s.split('.'), f = p[1] || ''; return rat(BigInt(p[0] + f), 10n ** BigInt(f.length)); }

// ---------- values: { key: [n, d] }, key = rad|pi|i
function key(rad, pi, im) { return rad + '|' + pi + '|' + im; }
function unpack(k) { var p = k.split('|'); return { rad: BigInt(p[0]), pi: +p[1], im: +p[2] }; }
function clean(v) { var o = {}; for (var k in v) if (v[k][0] !== 0n) o[k] = v[k]; return o; }
function constant(r) { var o = {}; o[key(1n, 0, 0)] = r; return clean(o); }
function add(a, b) { var o = {}, k; for (k in a) o[k] = a[k]; for (k in b) o[k] = o[k] ? radd(o[k], b[k]) : b[k]; return clean(o); }
function neg(a) { var o = {}; for (var k in a) o[k] = rmul(a[k], [-1n, 1n]); return o; }
function squareFree(n) { // n ≥ 1 → [outside, inside]
  if (n > 10n ** 12n) throw Error('radicand too large');
  var out = 1n, inside = n;
  for (var f = 2n; f * f <= inside; f++) while (inside % (f * f) === 0n) { inside /= f * f; out *= f; }
  return [out, inside];
}
function mulTerm(ka, ca, kb, cb) {
  var a = unpack(ka), b = unpack(kb), sf = squareFree(a.rad * b.rad), c = rmul(rmul(ca, cb), [sf[0], 1n]), im = a.im + b.im;
  if (im >= 2) { im -= 2; c = rmul(c, [-1n, 1n]); }
  var o = {}; o[key(sf[1], a.pi + b.pi, im)] = c; return o;
}
function mul(a, b) { var o = {}; for (var ka in a) for (var kb in b) o = add(o, mulTerm(ka, a[ka], kb, b[kb])); return o; }
function inv(a) { // only monomials can be divisors
  var ks = Object.keys(a); if (ks.length !== 1) throw Error('divide only by a single term');
  var t = unpack(ks[0]), c = a[ks[0]], o = {};
  // 1/(c·√r·πᵏ·iᵐ) = √r/(c·r) · π⁻ᵏ · (iᵐ → 1/i = -i)
  var coef = rinv(rmul(c, [t.rad, 1n]));
  if (t.im) coef = rmul(coef, [-1n, 1n]);
  o[key(t.rad, -t.pi, t.im)] = coef; return o;
}
function sqrtOf(a) {
  var ks = Object.keys(a);
  if (!ks.length) return {};
  if (ks.length !== 1 || ks[0] !== key(1n, 0, 0)) throw Error('unsupported radicand');
  var r = a[ks[0]]; if (r[0] < 0n) throw Error('negative radicand');
  // √(n/d) = √(n·d)/d
  var sf = squareFree(r[0] * r[1]), o = {};
  o[key(sf[1], 0, 0)] = rat(sf[0], r[1]); return o;
}
function equal(a, b) { a = clean(a); b = clean(b); var ka = Object.keys(a).sort(), kb = Object.keys(b).sort(); if (ka.join() !== kb.join()) return false; return ka.every(function (k) { return a[k][0] === b[k][0] && a[k][1] === b[k][1]; }); }
function isRational(a) { var ks = Object.keys(clean(a)); return !ks.length || (ks.length === 1 && ks[0] === key(1n, 0, 0)); }

// ---------- parser (records simplest-form problems in `flags`)
function normalize(s) {
  return String(s == null ? '' : s).replace(/[−–]/g, '-').replace(/[·×*]/g, '*').replace(/\\pi/g, 'π').replace(/\s+/g, '').replace(/pi/gi, 'π').replace(/sqrt/gi, '√');
}
function parseValue(src, flags) {
  var s = normalize(src), i = 0;
  if (!s || s.length > 120 || /[^0-9./()+\-*√πi^]/.test(s)) throw Error('unsupported');
  var radicals = 0;
  function peek() { return s[i]; }
  function expr(top) {
    var terms = [], v = {}, first = true;
    while (true) {
      var sign = 1;
      if (peek() === '+' || peek() === '-') { sign = peek() === '-' ? -1 : 1; i++; }
      else if (!first) break;
      var t = term();
      terms.push(t);
      v = add(v, sign < 0 ? neg(t) : t);
      first = false;
      if (peek() !== '+' && peek() !== '-') break;
    }
    if (top) { // like terms must be combined: no two top-level terms with the same √/π/i part
      var seen = {};
      terms.forEach(function (t) { var ks = Object.keys(t); if (ks.length === 1) { if (seen[ks[0]]) flags.combine = true; seen[ks[0]] = 1; } });
    }
    v.__n = terms.length;
    return v;
  }
  function term() {
    var v = factor(), sumFactor = !!v.__sum, radFactors = radMono(v) ? 1 : 0;
    while (i < s.length && peek() !== '+' && peek() !== '-' && peek() !== ')') {
      if (peek() === '/') { i++; var before = radicals; var d = factor(); if (radicals > before || (d.__sum && /√/.test(s))) flags.denominator = true; if (d.__sum && Object.keys(clean(strip(d))).length > 1) throw Error('divide only by a single term'); v = mul(strip(v), inv(strip(d))); continue; }
      if (peek() === '*') i++;
      var f = factor();
      if (sumFactor || f.__sum) flags.product = true;   // e.g. (2 + i)(4 - 6i) or 2(3 + √2)
      if (radMono(f)) radFactors++;
      v = mul(strip(v), strip(f));
    }
    if (radFactors > 1) flags.product = true;   // e.g. 2√3·√3: multiply the radicals
    return strip(v);
  }
  function radMono(v) { var ks = Object.keys(strip(v)); return ks.length === 1 && unpack(ks[0]).rad !== 1n; }
  function strip(v) { var o = {}; for (var k in v) if (k.indexOf('__') !== 0) o[k] = v[k]; return o; }
  function factor() {
    var v = atom();
    if (peek() === '^') { i++; var m = /^\d/.exec(s.slice(i)); if (!m) throw Error('bad power'); i++; var n = +m[0], r = constant([1n, 1n]); for (var k = 0; k < n; k++) r = mul(r, strip(v)); v = r; }
    return v;
  }
  function atom() {
    var c = peek();
    if (c === '(') {
      i++; var v = expr(false); if (peek() !== ')') throw Error('missing )'); i++;
      var out = strip(v); if (v.__n > 1) out.__sum = true; return out;
    }
    if (c === '√') {
      i++; radicals++; var arg;
      if (peek() === '(') { i++; arg = strip(expr(false)); if (peek() !== ')') throw Error('missing )'); i++; }
      else { var m = /^\d+(?:\.\d+)?/.exec(s.slice(i)); if (!m) throw Error('bad radical'); i += m[0].length; if (m[0].indexOf('.') >= 0) flags.decimal = true; arg = constant(decimal(m[0])); }
      if (!isRational(arg)) throw Error('nested radical');
      var r = (clean(arg)[key(1n, 0, 0)] || [0n, 1n]);
      if (r[1] === 1n) { var sf = squareFree(r[0] < 0n ? -r[0] : r[0]); if (sf[0] !== 1n) flags.radical = true; }
      else flags.radical = true;
      return sqrtOf(arg);
    }
    if (c === 'π') { i++; var o = {}; o[key(1n, 1, 0)] = [1n, 1n]; return o; }
    if (c === 'i') { i++; var o2 = {}; o2[key(1n, 0, 1)] = [1n, 1n]; return o2; }
    var n = /^\d+(?:\.\d+)?/.exec(s.slice(i));
    if (!n) throw Error('unexpected ' + c);
    i += n[0].length; if (n[0].indexOf('.') >= 0) flags.decimal = true;
    return constant(decimal(n[0]));
  }
  var v = expr(true);
  if (i !== s.length) throw Error('unexpected ' + s[i]);
  return strip(v);
}

// ---------- structured answers
function splitTop(s, sep) { var out = [], depth = 0, cur = ''; for (var k = 0; k < s.length; k++) { var ch = s[k]; if ('([⟨'.indexOf(ch) >= 0) depth++; if (')]⟩'.indexOf(ch) >= 0) depth--; if (ch === sep && depth === 0) { out.push(cur); cur = ''; } else cur += ch; } out.push(cur); return out; }
function shape(raw) {
  var s = String(raw == null ? '' : raw).replace(/[−–]/g, '-').trim().replace(/\.$/, '');
  var m;
  if (/∪|∞/.test(s) || /^[[(][^,]+,[^,]+[\])](\s*∪\s*[[(][^,]+,[^,]+[\])])*$/.test(s) && /\[|\]/.test(s)) return { kind: 'interval', s: s };
  if ((m = /^⟨(.*)⟩$/.exec(s))) return { kind: 'vector', parts: splitTop(m[1], ',') };
  if ((m = /^\[(.*)\]$/.exec(s))) return { kind: 'matrix', rows: m[1].split(';').map(function (r) { return splitTop(r, ','); }) };
  if ((m = /^\((.*)\)$/.exec(s)) && splitTop(m[1], ',').length >= 2) return { kind: 'tuple', parts: splitTop(m[1], ',') };
  if (/^[a-zθ]\s*=/.test(s) && /\bor\b|,/.test(s)) {
    var list = s.replace(/^[a-zθ]\s*=\s*/, '').split(/\s*,\s*|\s+or\s+/).map(function (p) { return p.replace(/^[a-zθ]\s*=\s*/, ''); });
    return { kind: 'list', parts: list };
  }
  if ((m = /^[a-zθ]\s*=\s*(.+)$/.exec(s)) && !/[a-zθ]/.test(m[1].replace(/π|i|sqrt/g, ''))) return { kind: 'value', s: m[1] };
  return { kind: 'value', s: s };
}
function intervals(s) {
  return s.split('∪').map(function (p) {
    p = p.trim(); var m = /^([[(])\s*(.+?)\s*,\s*(.+?)\s*([\])])$/.exec(p);
    if (!m) throw Error('not an interval');
    var lo = /^-∞$/.test(m[2]) ? 'neg' : m[2], hi = /^\+?∞$/.test(m[3]) ? 'pos' : m[3];
    if ((lo === 'neg' && m[1] === '[') || (hi === 'pos' && m[4] === ']')) throw Error('bracket on infinity');
    return { lo: lo, hi: hi, lc: m[1] === '[', hc: m[4] === ']' };
  });
}
function exactOf(text, flags) { return parseValue(text, flags); }

// Rounded keys such as "x ≈ 4.489", "≈ 12.2 km/h", "B ≈ 47.2°" or "≈ $8,430": the typed number must round to the key at the key's precision.
// Money signs and thousands separators are ignored on both sides.
function plainNum(s) { return String(s == null ? '' : s).replace(/[−–]/g, '-').replace(/(≈\s*-?|^\s*-?)\$/, '$1').replace(/^(\s*-?)\$/, '$1').replace(/(\d),(?=\d{3}(?!\d))/g, '$1'); }
var APPROX = /^(?:[a-zA-Zθ]\w*\s*)?≈\s*(-?\d+(?:\.(\d+))?)\s*(°|%|[a-zA-Z][a-zA-Z\/²³ ]{0,12})?$/;
function approxGrade(answer, typed) {
  var m = APPROX.exec(plainNum(answer).trim().replace(/\.$/, '')), dp = m[2] ? m[2].length : 0;
  var t = plainNum(typed).replace(/^[a-zA-Zθ]\w*\s*[=≈]\s*/, '').replace(/^≈\s*/, '').trim().replace(/\s*(°|%|[a-zA-Z][a-zA-Z\/²³ ]{0,12})\.?$/, '');
  if (!/^-?\d+(?:\.\d+)?$/.test(t)) return { status: 'invalid', message: 'Enter a number rounded as the question asks.' };
  var tdp = (t.split('.')[1] || '').length;
  var k = decimal(m[1].replace('-', '')), v = decimal(t.replace('-', ''));
  if (m[1][0] === '-') k = rmul(k, [-1n, 1n]); if (t[0] === '-') v = rmul(v, [-1n, 1n]);
  if (tdp < dp) return { status: 'incorrect' };
  var diff = radd(v, rmul(k, [-1n, 1n])), half = rat(5n, 10n ** BigInt(dp + 1));
  var absd = diff[0] < 0n ? [-diff[0], diff[1]] : diff;
  return { status: absd[0] * half[1] <= half[0] * absd[1] ? 'correct' : 'incorrect' };
}

API.supports = function (answer) {
  if (APPROX.test(plainNum(answer).trim().replace(/\.$/, ''))) return 'approx';
  try {
    var sh = shape(answer), f = {};
    if (sh.kind === 'interval') { intervals(sh.s).forEach(function (iv) { if (iv.lo !== 'neg') exactOf(iv.lo, f); if (iv.hi !== 'pos') exactOf(iv.hi, f); }); return 'interval'; }
    if (sh.kind === 'vector' || sh.kind === 'tuple' || sh.kind === 'list') { sh.parts.forEach(function (p) { exactOf(p.trim(), f); }); return sh.kind; }
    if (sh.kind === 'matrix') { sh.rows.forEach(function (r) { r.forEach(function (p) { exactOf(p.trim(), f); }); }); return 'matrix'; }
    exactOf(sh.s.trim(), f); return 'value';
  } catch (e) { return null; }
};

API.grade = function (answer, typed) {
  var kind = API.supports(answer);
  if (!kind) return { status: 'self' };
  var t = String(typed == null ? '' : typed).trim();
  if (!t) return { status: 'empty' };
  if (kind === 'approx') return approxGrade(answer, t);
  if (t.length > 180) return { status: 'invalid', message: 'Enter only your final answer (180 characters maximum).' };
  if (kind === 'vector') t = t.replace(/^</, '⟨').replace(/>$/, '⟩');
  var a = shape(answer), b = shape(t), f = {}, keyIrrational = false, typedRational = true;
  if (kind === 'list' && b.kind !== 'list') b = { kind: 'list', parts: t.replace(/^[a-zθ]\s*=\s*/, '').split(/\s*,\s*|\s+or\s+/).map(function (p) { return p.replace(/^[a-zθ]\s*=\s*/, ''); }) };
  function val(text, isKey) { var flags = isKey ? {} : f, v = exactOf(text.trim(), flags); if (isKey && !isRational(v)) keyIrrational = true; if (!isKey && !isRational(v)) typedRational = false; return v; }
  var ok;
  try {
    if (kind === 'interval') {
      if (b.kind !== 'interval') return { status: 'invalid', message: 'Use interval notation, such as (-∞, 3] or (-2, 5).' };
      var A = intervals(a.s), B = intervals(b.s);
      ok = A.length === B.length && A.every(function (x) {
        return B.some(function (y) {
          return x.lc === y.lc && x.hc === y.hc && (x.lo === 'neg' ? y.lo === 'neg' : y.lo !== 'neg' && equal(val(x.lo, true), val(y.lo))) &&
            (x.hi === 'pos' ? y.hi === 'pos' : y.hi !== 'pos' && equal(val(x.hi, true), val(y.hi)));
        });
      });
    } else if (kind === 'matrix') {
      if (b.kind !== 'matrix') return { status: 'invalid', message: 'Enter a matrix with rows separated by semicolons, such as [1, 2; 3, 4].' };
      ok = a.rows.length === b.rows.length && a.rows.every(function (r, i) { return r.length === b.rows[i].length && r.every(function (x, j) { return equal(val(x, true), val(b.rows[i][j])); }); });
    } else if (kind === 'vector' || kind === 'tuple') {
      var parts = b.kind === 'vector' || b.kind === 'tuple' ? b.parts : null;
      if (!parts) return { status: 'invalid', message: kind === 'vector' ? 'Enter the vector in component form, such as ⟨3, -4⟩.' : 'Enter the coordinates, such as (2, -3).' };
      ok = a.parts.length === parts.length && a.parts.every(function (x, i) { return equal(val(x, true), val(parts[i])); });
    } else if (kind === 'list') {
      var got = b.kind === 'list' ? b.parts : [b.kind === 'value' ? b.s : t];
      var want = a.parts.map(function (x) { return val(x, true); }), have = got.map(function (x) { return val(x); });
      ok = want.length === have.length && want.every(function (w) { return have.some(function (h) { return equal(w, h); }); }) && have.every(function (h) { return want.some(function (w) { return equal(w, h); }); });
    } else {
      if (b.kind !== 'value') return { status: 'incorrect' };
      ok = equal(val(a.s, true), val(b.s));
    }
  } catch (e) {
    return { status: 'invalid', message: 'Answer format could not be read. Use exact values such as (√3)/2, 7π/6 or 3 - 4i.' };
  }
  if (!ok && f.decimal && keyIrrational && typedRational) return { status: 'invalid', message: 'Give an exact answer (use √ and π), not a decimal.' };
  if (ok && f.denominator) return { status: 'invalid', message: 'Rationalize the denominator, as in 1/√2 = (√2)/2.' };
  if (ok && f.radical) return { status: 'invalid', message: 'Simplify the radical: take out square factors, as in √12 = 2√3.' };
  if (ok && (f.product || f.combine)) return { status: 'invalid', message: 'Simplify completely: multiply out and combine like terms.' };
  return { status: ok ? 'correct' : 'incorrect' };
};
})(typeof window !== 'undefined' ? window : globalThis);
