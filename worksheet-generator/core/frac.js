/* Exact rational arithmetic. All slopes, intercepts and answers are Fr objects, so there is
   never any floating-point rounding in the math itself. */
(function (G) {
  'use strict';
  var NS = (G.MKWS = G.MKWS || {});

  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function lcm(a, b) { return a === 0 || b === 0 ? 0 : Math.abs(a * b) / gcd(a, b); }

  function Fr(n, d) {
    if (d === undefined) d = 1;
    if (!Number.isInteger(n) || !Number.isInteger(d)) throw new Error('Fr needs integers: ' + n + '/' + d);
    if (d === 0) throw new Error('Fr: zero denominator');
    if (d < 0) { n = -n; d = -d; }
    var g = gcd(n, d) || 1;
    this.n = n / g; this.d = d / g;
  }
  Fr.of = function (x) { return x instanceof Fr ? x : new Fr(x, 1); };
  var P = Fr.prototype;
  P.add = function (o) { o = Fr.of(o); return new Fr(this.n * o.d + o.n * this.d, this.d * o.d); };
  P.sub = function (o) { o = Fr.of(o); return new Fr(this.n * o.d - o.n * this.d, this.d * o.d); };
  P.mul = function (o) { o = Fr.of(o); return new Fr(this.n * o.n, this.d * o.d); };
  P.div = function (o) { o = Fr.of(o); if (o.n === 0) throw new Error('Fr: divide by zero'); return new Fr(this.n * o.d, this.d * o.n); };
  P.neg = function () { return new Fr(-this.n, this.d); };
  P.abs = function () { return new Fr(Math.abs(this.n), this.d); };
  P.inv = function () { return new Fr(this.d, this.n); };
  P.eq = function (o) { o = Fr.of(o); return this.n === o.n && this.d === o.d; };
  P.cmp = function (o) { o = Fr.of(o); return this.n * o.d - o.n * this.d; };
  P.lt = function (o) { return this.cmp(o) < 0; };
  P.gt = function (o) { return this.cmp(o) > 0; };
  P.isInt = function () { return this.d === 1; };
  P.isZero = function () { return this.n === 0; };
  P.sign = function () { return this.n > 0 ? 1 : this.n < 0 ? -1 : 0; };
  P.val = function () { return this.n / this.d; };
  P.toString = function () { return this.d === 1 ? String(this.n) : this.n + '/' + this.d; };

  NS.frac = {
    Fr: Fr, gcd: gcd, lcm: lcm,
    F: function (n, d) { return new Fr(n, d === undefined ? 1 : d); },
    of: Fr.of
  };
})(typeof window !== 'undefined' ? window : globalThis);
