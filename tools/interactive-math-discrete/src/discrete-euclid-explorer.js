/* Euclidean Algorithm Explorer. For positive integers a ≥ b: a = bq + r with 0 ≤ r < b, and gcd(a, b) = gcd(b, r).
   The a × b rectangle is cut into the largest squares that fit; each row of equal squares is one division step,
   and the last square size is gcd(a, b). Extended algorithm: rᵢ = sᵢa + tᵢb, carried down the table.
   Quotient-remainder theorem: for any integer n and d > 0 there are unique q, r with n = dq + r and 0 ≤ r < d (q = ⌊n/d⌋). */
var css = L.h('style', null, document.head);
css.textContent = '.eu-big{font-size:1.15rem;margin:4px 0 8px}.eu-eq{font-family:var(--body);font-size:1.05rem;line-height:1.7}.eu-eq b{color:var(--purple)}' +
  '.eu-fac span{display:inline-block;margin:2px 4px 2px 0;padding:2px 8px;border-radius:999px;background:var(--wash);font-weight:700}.eu-fac span.common{background:var(--green-tint);outline:2px solid var(--green)}';
var COLORS = ['purple', 'blue', 'green', 'orange', 'red'];
var START = { tab: 'gcd', a: 252, b: 198, k: 99, n: 23, d: 7 };
var st = Object.assign({}, START), seen = {};
function euclid(a, b) { var rows = []; while (b > 0) { var q = Math.floor(a / b), r = a - b * q; rows.push({ a: a, b: b, q: q, r: r }); a = b; b = r; } return { rows: rows, g: a }; }
function ext(a, b) { /* table method: r, q, s, t */
  var T = [{ r: a, q: null, s: 1, t: 0 }, { r: b, q: null, s: 0, t: 1 }];
  while (T[T.length - 1].r > 0) { var p = T[T.length - 2], c = T[T.length - 1], q = Math.floor(p.r / c.r); c.q = q; T.push({ r: p.r - q * c.r, q: null, s: p.s - q * c.s, t: p.t - q * c.t }); }
  return T;
}
function factor(n) { var f = {}, p = 2; while (n > 1 && p * p <= n) { while (n % p === 0) { f[p] = (f[p] || 0) + 1; n /= p; } p++; } if (n > 1) f[n] = (f[n] || 0) + 1; return f; }
function isPrime(n) { if (n < 2) return false; for (var i = 2; i * i <= n; i++) if (n % i === 0) return false; return true; }
function fstr(f) { var k = Object.keys(f).map(Number).sort(function (x, y) { return x - y; }); return k.length ? k.map(function (p) { return p + (f[p] > 1 ? '<sup>' + f[p] + '</sup>' : ''); }).join(' · ') : '1'; }
function sgn(x) { return x < 0 ? '(−' + (-x) + ')' : String(x); }

var tabs = L.tabs(P.panel, [{ id: 'gcd', label: 'GCD and the algorithm' }, { id: 'div', label: 'Quotient and remainder' }], function (id) { st.tab = id; show(); draw(); });
var gBox = L.h('div', null, P.panel), dBox = L.h('div', null, P.panel);
var nA = L.numInput(gBox, { id: 'a', label: 'a (1 to 999)', min: 1, max: 999, step: 1, value: st.a, onChange: function (v) { st.a = Math.round(v); nA.set(st.a); st.k = 0; draw(); } });
var nB = L.numInput(gBox, { id: 'b', label: 'b (1 to 999)', min: 1, max: 999, step: 1, value: st.b, onChange: function (v) { st.b = Math.round(v); nB.set(st.b); st.k = 0; draw(); } });
var stepRow = L.h('div', { class: 'btn-row' }, gBox);
L.button(stepRow, 'Next step', function () { st.k++; draw(); });
L.button(stepRow, 'Show all steps', function () { st.k = 99; draw(); }, true);
L.button(stepRow, 'Swap a and b', function () { var t = st.a; st.a = st.b; st.b = t; nA.set(st.a); nB.set(st.b); st.k = 0; draw(); }, true);
var nN = L.numInput(dBox, { id: 'n', label: 'n (any integer from −200 to 200)', min: -200, max: 200, step: 1, value: st.n, onChange: function (v) { st.n = Math.round(v); nN.set(st.n); draw(); } });
var sD = L.slider(dBox, { id: 'd', label: 'Divisor d', min: 1, max: 20, value: st.d, color: 'blue', onInput: function (v) { st.d = v; draw(); } });
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { st = Object.assign({}, START); nA.set(st.a); nB.set(st.b); nN.set(st.n); sD.set(st.d, true); tabs.set('gcd'); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Find two <b>composite</b> numbers between 50 and 200 that are <b>relatively prime</b> (their GCD is 1).', check: function () { return seen.coprime; } },
  { text: 'Find a pair that needs at least <b>6 division steps</b>. What kind of numbers make the algorithm slow?', check: function () { return seen.slow; } },
  { text: 'Find a and b with gcd(a, b) = 12 and lcm(a, b) = 360.', check: function () { return seen.gl; } },
  { text: 'Find a pair where the algorithm stops after <b>one</b> step with b < a. What is true about b?', check: function () { return seen.one; } },
  { text: 'On the Quotient and remainder tab, divide a <b>negative</b> number by 7. Check that the remainder is still between 0 and 6.', check: function () { return seen.neg; } }
]);
L.notice(P.below, '<p><b>Why it works.</b> If d divides a and b, it divides r = a − bq; if d divides b and r, it divides a = bq + r. So a, b and b, r have exactly the same common divisors, and gcd(a, b) = gcd(b, r). The remainders shrink, so the process stops; the last nonzero remainder is the GCD.</p>' +
  '<p><b>In the picture</b>, each row of squares of the same size is one step: q squares of side b fit along a, leaving an r × b strip. The final squares have side gcd(a, b), and they tile everything.</p>' +
  '<p><b>Linear combination (Bézout).</b> Running the steps backward (or carrying s and t down the table) writes gcd(a, b) = sa + tb. Also gcd(a, b) · lcm(a, b) = ab, and in prime factorizations the GCD takes the smaller exponents while the LCM takes the larger.</p>' +
  '<p><b>Negative numbers.</b> The quotient-remainder theorem needs 0 ≤ r < d, so −23 = 7(−4) + 5, not 7(−3) − 2. Then n mod d = r and n div d = q = ⌊n/d⌋.</p>');

var big = L.h('div', { class: 'eu-big', 'aria-live': 'polite' }, P.stage);
var W = 640, H = 400, svg = L.s('svg', { viewBox: '0 0 ' + W + ' ' + H, role: 'img', 'aria-label': 'Rectangle cut into squares' }, P.stage);
var eqs = L.h('div', { class: 'eu-eq' }, P.stage), tbl = L.table(P.stage), fac = L.h('div', { class: 'eu-fac' }, P.stage);
function show() { gBox.style.display = st.tab === 'gcd' ? '' : 'none'; dBox.style.display = st.tab === 'div' ? '' : 'none'; }
function txt(x, y, s, o) { o = o || {}; var e = L.s('text', { x: x, y: y, 'text-anchor': o.anchor || 'middle', class: 'g-label', 'font-size': o.size || 14, fill: o.color || null, 'font-weight': o.weight || null }, svg); e.textContent = s; return e; }

var draw = L.scheduler(function () {
  svg.innerHTML = '';
  if (st.tab === 'gcd') {
    var a = st.a, b = st.b, E = euclid(Math.max(a, b), Math.min(a, b)), rows = E.rows, g = E.g, lcm = a / g * b, k = Math.min(st.k, rows.length);
    svg.setAttribute('aria-label', 'A ' + Math.max(a, b) + ' by ' + Math.min(a, b) + ' rectangle cut into squares; the smallest squares have side ' + g);
    big.innerHTML = 'gcd(' + a + ', ' + b + ') = <b>' + (k >= rows.length ? g : '?') + '</b>' + (k >= rows.length ? ' &nbsp; lcm(' + a + ', ' + b + ') = <b>' + lcm + '</b>' : ' &nbsp; <span style="color:var(--ink-soft)">(step ' + k + ' of ' + rows.length + ')</span>');
    /* tiling: long side horizontal */
    var A = Math.max(a, b), B = Math.min(a, b), sc = Math.min((W - 20) / A, (H - 20) / B), ox = (W - A * sc) / 2, oy = (H - B * sc) / 2;
    L.s('rect', { x: ox, y: oy, width: A * sc, height: B * sc, fill: 'var(--card)', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    var x = 0, y = 0, w = A, h = B;
    for (var i = 0; i < k; i++) {
      var r = rows[i], col = 'var(--' + COLORS[i % COLORS.length] + ')';
      for (var j = 0; j < r.q; j++) {
        var side = r.b, sx, sy;
        if (w >= h) { sx = x + j * side; sy = y; } else { sx = x; sy = y + j * side; }
        L.s('rect', { x: ox + sx * sc, y: oy + sy * sc, width: side * sc, height: side * sc, fill: col, 'fill-opacity': 0.28, stroke: col, 'stroke-width': side * sc > 6 ? 2 : 0.6 }, svg);
      }
      if (side * sc > 34 && r.q <= 12) txt(ox + (w >= h ? x + side / 2 : x + side / 2) * sc, oy + (w >= h ? y + side / 2 : y + side / 2) * sc + 5, String(side), { size: Math.min(18, side * sc / 3) });
      if (w >= h) { x += r.q * r.b; w = r.r; } else { y += r.q * r.b; h = r.r; }
    }
    eqs.innerHTML = rows.slice(0, k).map(function (r, i) { return '<div>Step ' + (i + 1) + ': ' + r.a + ' = ' + r.b + ' · ' + r.q + ' + <b>' + r.r + '</b> &nbsp;<span style="color:var(--ink-soft)">so gcd(' + r.a + ', ' + r.b + ') = gcd(' + r.b + ', ' + r.r + ')</span></div>'; }).join('') +
      (k >= rows.length ? '<div>The last nonzero remainder is <b>' + g + '</b>.</div>' : '');
    if (k >= rows.length) {
      var T = ext(a, b), last = T[T.length - 2];
      tbl.set(['r', 'q', 's', 't', 'check: s·' + a + ' + t·' + b], T.map(function (row) { return [row.r === g && row === last ? '<b>' + row.r + '</b>' : row.r, row.q == null ? '' : row.q, row.s, row.t, row.s * a + row.t * b]; }));
      var fa = factor(a), fbb = factor(b);
      fac.innerHTML = '<div style="margin-top:8px"><b>Linear combination:</b> ' + g + ' = ' + sgn(last.s) + ' · ' + a + ' + ' + sgn(last.t) + ' · ' + b + '</div>' +
        '<div style="margin-top:6px"><b>Prime factorizations</b> (shared primes outlined):</div>' +
        [[a, fa, fbb], [b, fbb, fa]].map(function (z) { return '<div>' + z[0] + ' = ' + Object.keys(z[1]).map(Number).sort(function (p, q) { return p - q; }).map(function (p) { return '<span class="' + (z[2][p] ? 'common' : '') + '">' + p + (z[1][p] > 1 ? '<sup>' + z[1][p] + '</sup>' : '') + '</span>'; }).join('') + (z[0] === 1 ? '1 (no prime factors)' : '') + '</div>'; }).join('') +
        '<div>gcd uses the smaller exponents: ' + fstr(factor(g)) + ' = ' + g + '; lcm uses the larger: ' + fstr(factor(lcm)) + ' = ' + lcm + '. Check: ' + g + ' · ' + lcm + ' = ' + (g * lcm) + ' = ' + a + ' · ' + b + '.</div>';
      fb.set(g === 1 ? a + ' and ' + b + ' are <b>relatively prime</b>: their only common positive divisor is 1.' : 'Every common divisor of ' + a + ' and ' + b + ' divides ' + g + '.', g === 1 ? 'good' : '');
      if (g === 1 && a >= 50 && a <= 200 && b >= 50 && b <= 200 && !isPrime(a) && !isPrime(b) && a !== b) seen.coprime = true;
      if (rows.length >= 6) seen.slow = true;
      if (g === 12 && lcm === 360) seen.gl = true;
      if (rows.length === 1 && a !== b) seen.one = true;
    } else { tbl.set([], []); fac.innerHTML = ''; fb.set('Press <b>Next step</b> to make the next cut, or <b>Show all steps</b>.', ''); }
  } else {
    var n = st.n, d = st.d, q = Math.floor(n / d), r = n - d * q;
    big.innerHTML = n + ' = ' + d + ' · (' + (q < 0 ? '−' + (-q) : q) + ') + <b>' + r + '</b> &nbsp; with 0 ≤ ' + r + ' < ' + d;
    var lo = Math.min(0, d * q) - d, hi = Math.max(0, n) + d, X = function (v) { return 30 + (v - lo) / (hi - lo) * (W - 60); }, y0 = 200;
    svg.setAttribute('aria-label', 'Number line with multiples of ' + d + ' and the point ' + n);
    L.s('line', { x1: 20, y1: y0, x2: W - 20, y2: y0, stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    for (var m = Math.ceil(lo / d); m * d <= hi; m++) {
      var xv = X(m * d), on = m === q;
      L.s('line', { x1: xv, y1: y0 - (on ? 18 : 10), x2: xv, y2: y0 + (on ? 18 : 10), stroke: on ? 'var(--blue)' : 'var(--ink-soft)', 'stroke-width': on ? 4 : 2 }, svg);
      if ((hi - lo) / d < 26 || on || m === 0) txt(xv, y0 + 36, String(m * d).replace('-', '−'), { size: 12, color: on ? 'var(--blue)' : null });
    }
    if (q !== 0 || n !== 0) txt(X(0), y0 + 54, '0', { size: 12, color: 'var(--ink-soft)' });
    L.s('circle', { cx: X(n), cy: y0, r: 8, fill: 'var(--purple)', stroke: 'var(--ink)', 'stroke-width': 2 }, svg);
    txt(X(n), y0 - 28, 'n = ' + String(n).replace('-', '−'), { color: 'var(--purple)', weight: 700 });
    if (r > 0) { L.s('path', { d: 'M' + X(d * q) + ' ' + (y0 - 60) + ' H' + X(n), stroke: 'var(--green)', 'stroke-width': 4, 'marker-end': '' }, svg); txt((X(d * q) + X(n)) / 2, y0 - 68, 'r = ' + r, { color: 'var(--green)', weight: 700 }); }
    txt(X(d * q), y0 - 88, 'd · q = ' + String(d * q).replace('-', '−'), { color: 'var(--blue)' });
    eqs.innerHTML = '<div>q = ⌊' + String(n).replace('-', '−') + ' / ' + d + '⌋ = ' + String(q).replace('-', '−') + ' &nbsp; so &nbsp; ' + String(n).replace('-', '−') + ' div ' + d + ' = ' + String(q).replace('-', '−') + ' and ' + String(n).replace('-', '−') + ' mod ' + d + ' = <b>' + r + '</b></div>' +
      '<div style="color:var(--ink-soft)">The remainder is the distance from the largest multiple of ' + d + ' that is ≤ n up to n.</div>';
    tbl.set(['n', 'n mod ' + d], [n - 2, n - 1, n, n + 1, n + 2].map(function (v) { return [String(v).replace('-', '−'), ((v % d) + d) % d]; }));
    fac.innerHTML = '';
    fb.set(n < 0 ? 'For negative n, the quotient rounds <b>down</b> (toward −∞), so the remainder stays nonnegative.' : 'Try a negative n: the remainder must still satisfy 0 ≤ r < d.', n < 0 ? 'good' : '');
    if (n < 0 && d === 7) seen.neg = true;
  }
  ch.update();
});
show(); draw();
