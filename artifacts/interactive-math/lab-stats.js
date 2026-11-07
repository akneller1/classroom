/* Mr. K's Classroom: statistics helpers for the Interactive Math tools (loaded after lab.js and lab-plus.js
   by the Statistics tools only). Lab.stats: seeded random numbers, normal and t distributions (CDF and quantiles),
   summary statistics, and a histogram helper for Lab.graph. Checked against published table values by
   tools/interactive-math-statistics/tests/stats-core.cjs. */
(function (G) {
'use strict';
var L = G.Lab;
if (!L) return;
/* Seeded generator (mulberry32) so a class can share the same random draws with ?seed=. */
function rng(seed) {
  var a = (seed >>> 0) || 1;
  return function () { a = (a + 0x6D2B79F5) >>> 0; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}
function seedFromURL() { var m = /[?&]seed=(\d+)/.exec(G.location.search); return m ? +m[1] : Math.floor(Math.random() * 4294967296); }
function randNormal(r) { var u = 0, v = 0; while (u === 0) u = r(); v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }
/* erfc with fractional error below 1.2e-7 everywhere (Numerical Recipes, Chebyshev fit). */
function erfc(x) {
  var z = Math.abs(x), t = 1 / (1 + 0.5 * z);
  var r = t * Math.exp(-z * z - 1.26551223 + t * (1.00002368 + t * (0.37409196 + t * (0.09678418 + t * (-0.18628806 + t * (0.27886807 + t * (-1.13520398 + t * (1.48851587 + t * (-0.82215223 + t * 0.17087277)))))))));
  return x >= 0 ? r : 2 - r;
}
function normCdf(z) { return 0.5 * erfc(-z / Math.SQRT2); }
function normPdf(z) { return Math.exp(-0.5 * z * z) / Math.sqrt(2 * Math.PI); }
/* Inverse normal: Acklam's rational approximation, then one Halley refinement step. */
function invNorm(p) {
  if (p <= 0) return -Infinity; if (p >= 1) return Infinity;
  var a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02, 1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00],
      b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02, 6.680131188771972e+01, -1.328068155288572e+01],
      c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00, -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00],
      d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00], q, r, x;
  if (p < 0.02425) { q = Math.sqrt(-2 * Math.log(p)); x = (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
  else if (p > 1 - 0.02425) { q = Math.sqrt(-2 * Math.log(1 - p)); x = -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1); }
  else { q = p - 0.5; r = q * q; x = (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1); }
  var e = normCdf(x) - p, u = e * Math.sqrt(2 * Math.PI) * Math.exp(x * x / 2);
  return x - u / (1 + x * u / 2);
}
/* Regularized incomplete beta I_x(a, b) (continued fraction, Numerical Recipes). */
function lgamma(x) { var c = [76.18009172947146, -86.50532032941677, 24.01409824083091, -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5], y = x, t = x + 5.5, s = 1.000000000190015; t -= (x + 0.5) * Math.log(t); for (var j = 0; j < 6; j++) s += c[j] / ++y; return -t + Math.log(2.5066282746310005 * s / x); }
function betacf(a, b, x) {
  var qab = a + b, qap = a + 1, qam = a - 1, c = 1, d = 1 - qab * x / qap, m, m2, aa, del, h;
  if (Math.abs(d) < 1e-300) d = 1e-300; d = 1 / d; h = d;
  for (m = 1; m <= 300; m++) {
    m2 = 2 * m; aa = m * (b - m) * x / ((qam + m2) * (a + m2));
    d = 1 + aa * d; if (Math.abs(d) < 1e-300) d = 1e-300; c = 1 + aa / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; h *= d * c;
    aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2));
    d = 1 + aa * d; if (Math.abs(d) < 1e-300) d = 1e-300; c = 1 + aa / c; if (Math.abs(c) < 1e-300) c = 1e-300; d = 1 / d; del = d * c; h *= del;
    if (Math.abs(del - 1) < 3e-14) break;
  }
  return h;
}
function ibeta(x, a, b) {
  if (x <= 0) return 0; if (x >= 1) return 1;
  var bt = Math.exp(lgamma(a + b) - lgamma(a) - lgamma(b) + a * Math.log(x) + b * Math.log(1 - x));
  return x < (a + 1) / (a + b + 2) ? bt * betacf(a, b, x) / a : 1 - bt * betacf(b, a, 1 - x) / b;
}
function tCdf(t, df) { var x = df / (df + t * t), tail = 0.5 * ibeta(x, df / 2, 0.5); return t >= 0 ? 1 - tail : tail; }
function invT(p, df) { var lo = -1e6, hi = 1e6; for (var i = 0; i < 200; i++) { var mid = (lo + hi) / 2; if (tCdf(mid, df) < p) lo = mid; else hi = mid; } return (lo + hi) / 2; }
function mean(a) { var s = 0; for (var i = 0; i < a.length; i++) s += a[i]; return s / a.length; }
function sd(a, pop) { var m = mean(a), s = 0; for (var i = 0; i < a.length; i++) s += (a[i] - m) * (a[i] - m); return Math.sqrt(s / (a.length - (pop ? 0 : 1))); }
/* Draw a histogram of values on a Lab.graph: bins of width w starting at x0. Returns the counts. */
function histogram(g, values, x0, w, nb, o) {
  o = o || {}; var counts = []; for (var i = 0; i < nb; i++) counts.push(0);
  values.forEach(function (v) { var k = Math.floor((v - x0) / w + 1e-9); if (k >= 0 && k < nb) counts[k]++; else if (k === nb && Math.abs(v - (x0 + nb * w)) < 1e-9) counts[nb - 1]++; });
  var scale = o.density ? 1 / (values.length * w) : 1;
  counts.forEach(function (c, i) { if (c) g.rect(x0 + i * w, 0, w, c * scale, { fill: o.fill || 'blue', opacity: o.opacity == null ? 0.55 : o.opacity, stroke: o.stroke || 'ink', width: o.width || 1 }); });
  return counts;
}
L.stats = { rng: rng, seedFromURL: seedFromURL, randNormal: randNormal, normCdf: normCdf, normPdf: normPdf, invNorm: invNorm, tCdf: tCdf, invT: invT, ibeta: ibeta, mean: mean, sd: sd, histogram: histogram };
})(window);
