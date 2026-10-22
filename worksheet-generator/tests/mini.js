/* Independent math utilities for the test suite.
   Deliberately shares NO code with core/frac.js or core/tex.js: it re-parses the TeX that a student
   would actually see, so a bug in the generators cannot hide itself. */
'use strict';

const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) { [a, b] = [b, a % b]; } return a; };
class Q {
  constructor(n, d = 1) {
    if (!Number.isInteger(n) || !Number.isInteger(d)) throw new Error('non-integer rational ' + n + '/' + d);
    if (d === 0) throw new Error('division by zero');
    if (d < 0) { n = -n; d = -d; }
    const g = gcd(n, d) || 1; this.n = n / g; this.d = d / g;
  }
  add(o) { return new Q(this.n * o.d + o.n * this.d, this.d * o.d); }
  sub(o) { return new Q(this.n * o.d - o.n * this.d, this.d * o.d); }
  mul(o) { return new Q(this.n * o.n, this.d * o.d); }
  div(o) { return new Q(this.n * o.d, this.d * o.n); }
  neg() { return new Q(-this.n, this.d); }
  eq(o) { return this.n === o.n && this.d === o.d; }
  isInt() { return this.d === 1; }
  isZero() { return this.n === 0; }
  val() { return this.n / this.d; }
  toString() { return this.d === 1 ? String(this.n) : this.n + '/' + this.d; }
}
const q = (n, d = 1) => new Q(n, d);
const ZERO = q(0);

/* ---- markup helpers ---- */
const MATH = /⟨([^⟩]*)⟩/g;
const maths = s => [...String(s).matchAll(MATH)].map(m => m[1]);
const stripMath = s => String(s).replace(MATH, ' ').replace(/<[^>]+>/g, ' ');

/* ---- TeX -> linear polynomial {x,y,c} ---- */
function tokenize(s) {
  s = s.replace(/\\,|\\ |\;|\\!|\s+/g, '').replace(/\\cdot/g, '*').replace(/\\dfrac/g, '\\frac');
  const re = /\\frac\{(-?\d+)\}\{(-?\d+)\}|\d+|[A-Za-z]|[+\-*()=]/g, out = []; let m, last = 0;
  while ((m = re.exec(s))) {
    if (m.index !== last) throw new Error('cannot tokenize ' + JSON.stringify(s) + ' at ' + last);
    last = re.lastIndex;
    if (m[1] !== undefined) out.push({ t: 'num', v: q(+m[1], +m[2]) });
    else if (/^\d+$/.test(m[0])) out.push({ t: 'num', v: q(+m[0]) });
    else if (/^[A-Za-z]$/.test(m[0])) out.push({ t: 'var', v: m[0] });
    else out.push({ t: 'op', v: m[0] });
  }
  if (last !== s.length) throw new Error('trailing junk in ' + JSON.stringify(s));
  return out;
}
const P = (x, y, c) => ({ x: x || ZERO, y: y || ZERO, c: c || ZERO });
function pAdd(a, b) { return P(a.x.add(b.x), a.y.add(b.y), a.c.add(b.c)); }
function pNeg(a) { return P(a.x.neg(), a.y.neg(), a.c.neg()); }
function isConst(a) { return a.x.isZero() && a.y.isZero(); }
function pMul(a, b) {
  if (isConst(a)) return P(b.x.mul(a.c), b.y.mul(a.c), b.c.mul(a.c));
  if (isConst(b)) return pMul(b, a);
  throw new Error('nonlinear product');
}
/* varMap lets tests rename context letters (C, d, ...) to y and x. */
function parsePoly(tex, varMap) {
  const toks = tokenize(tex); let i = 0;
  const peek = () => toks[i];
  function primary() {
    const t = toks[i++]; if (!t) throw new Error('unexpected end');
    if (t.t === 'num') return P(null, null, t.v);
    if (t.t === 'var') { const v = (varMap && varMap[t.v]) || t.v; if (v === 'x') return P(q(1)); if (v === 'y') return P(null, q(1)); throw new Error('unknown variable ' + t.v); }
    if (t.t === 'op' && t.v === '(') { const e = expr(); if (!(toks[i] && toks[i].v === ')')) throw new Error('missing )'); i++; return e; }
    throw new Error('bad token ' + JSON.stringify(t));
  }
  function unary() { const t = peek(); if (t && t.t === 'op' && t.v === '-') { i++; return pNeg(unary()); } if (t && t.t === 'op' && t.v === '+') { i++; return unary(); } return primary(); }
  function term() {
    let v = unary();
    for (;;) {
      const t = peek(); if (!t) break;
      if (t.t === 'op' && t.v === '*') { i++; v = pMul(v, unary()); }
      else if (t.t === 'num' || t.t === 'var' || (t.t === 'op' && t.v === '(')) v = pMul(v, primary());
      else break;
    }
    return v;
  }
  function expr() {
    let v = term();
    for (;;) { const t = peek(); if (t && t.t === 'op' && (t.v === '+' || t.v === '-')) { i++; const r = term(); v = pAdd(v, t.v === '+' ? r : pNeg(r)); } else break; }
    return v;
  }
  const r = expr(); if (i !== toks.length) throw new Error('unparsed tokens in ' + tex); return r;
}
/* "lhs = rhs"  ->  {A,B,C} with A x + B y = C */
function parseEq(tex, varMap) {
  tex = tex.replace(/^f\(x\)/, 'y');
  const parts = tex.split('='); if (parts.length !== 2) throw new Error('not an equation: ' + tex);
  const L = parsePoly(parts[0], varMap), R = parsePoly(parts[1], varMap);
  return { A: L.x.sub(R.x), B: L.y.sub(R.y), C: R.c.sub(L.c) };
}
/* Line description: {m,b} or {vert:c} */
function lineOfEq(e) {
  if (!e.B.isZero()) return { m: e.A.neg().div(e.B), b: e.C.div(e.B) };
  if (!e.A.isZero()) return { vert: e.C.div(e.A) };
  throw new Error('degenerate equation');
}
const parseLine = (tex, vm) => lineOfEq(parseEq(tex, vm));
function parseNum(tex) { const p = parsePoly(tex); if (!isConst(p)) throw new Error('not a number: ' + tex); return p.c; }
/* "(a,\,b)" -> ['a','b'] (strings) */
function parsePoint(tex) {
  const t = tex.replace(/\\,/g, '').replace(/\s+/g, '');
  if (t[0] !== '(' || t[t.length - 1] !== ')') throw new Error('not a point: ' + tex);
  const inner = t.slice(1, -1), k = inner.indexOf(',');
  if (k < 0) throw new Error('not a point: ' + tex);
  return [inner.slice(0, k), inner.slice(k + 1)];
}
const pointQ = tex => parsePoint(tex).map(parseNum);
const onLine = (ln, x, y) => ln.vert !== undefined ? x.eq(ln.vert) : y.eq(ln.m.mul(x).add(ln.b));

/* ---- table parsing (HTML produced by NS.table) ---- */
function parseTable(html) {
  const rows = {};
  [...html.matchAll(/<tr><th>⟨(\w)⟩<\/th>(.*?)<\/tr>/g)].forEach(m => {
    rows[m[1]] = [...m[2].matchAll(/<td( class="blank")?>(?:⟨([^⟩]*)⟩|&nbsp;)<\/td>/g)].map(c => c[1] ? null : parseNum(c[2]));
  });
  return rows;
}

/* ---- SVG reading (independent geometry) ---- */
function readSvg(svg) {
  const at = n => +(svg.match(new RegExp(' data-' + n + '="(-?[\\d.]+)"'))[1]);
  const g = { xmin: at('xmin'), xmax: at('xmax'), ymin: at('ymin'), ymax: at('ymax'), cell: at('cell'), padl: at('padl'), padt: at('padt') };
  const toX = px => g.xmin + (px - g.padl) / g.cell, toY = py => g.ymax - (py - g.padt) / g.cell;
  const lines = [...svg.matchAll(/<path class="gline" d="M([-\d.]+) ([-\d.]+) L([-\d.]+) ([-\d.]+)"/g)].map(m => ({
    a: [toX(+m[1]), toY(+m[2])], b: [toX(+m[3]), toY(+m[4])]
  }));
  const points = [...svg.matchAll(/<circle class="gpt" cx="([-\d.]+)" cy="([-\d.]+)"/g)].map(m => [toX(+m[1]), toY(+m[2])]);
  const labels = [...svg.matchAll(/<text[^>]*>(\([^<]*\))<\/text>/g)].map(m => m[1]);
  return { g, lines, points, labels };
}
/* Turn a drawn segment into an exact line {m,b} / {vert}, within drawing tolerance. */
function segLine(seg) {
  const [x1, y1] = seg.a, [x2, y2] = seg.b;
  if (Math.abs(x2 - x1) < 0.03) return { vert: Math.round(x1 * 1000) / 1000 };
  const m = (y2 - y1) / (x2 - x1), b = y1 - m * x1;
  return { mf: m, bf: b };
}
const near = (a, b, tol = 0.03) => Math.abs(a - b) <= tol;
/* does a drawn segment lie on the exact line ln (Q-based)?  also returns true slope for reading. */
function segmentMatches(seg, ln) {
  const pts = [seg.a, seg.b];
  if (ln.vert !== undefined) return pts.every(p => near(p[0], ln.vert.val()));
  return pts.every(p => near(p[1], ln.m.val() * p[0] + ln.b.val()));
}
/* Round a drawn slope to the nearest rational with denominator <= 12 (best fit, not first fit). */
function ratFromFloat(v, maxDen = 12) {
  let best = null;
  for (let d = 1; d <= maxDen; d++) {
    const n = Math.round(v * d), err = Math.abs(n / d - v);
    if (!best || err < best.err - 1e-12) best = { n, d, err };
  }
  if (best.err > 0.004) throw new Error('cannot rationalize ' + v);
  return q(best.n, best.d);
}

module.exports = { Q, q, ZERO, gcd, maths, stripMath, MATH, parsePoly, parseEq, lineOfEq, parseLine, parseNum, parsePoint, pointQ, onLine, parseTable, readSvg, segLine, near, segmentMatches, ratFromFloat, tokenize };
