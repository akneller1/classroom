/* Voting, Power & Apportionment Explorer.
   Ranked ballots (k candidates). Plurality: most first-place votes. Borda count: k points for 1st, k − 1 for 2nd, …, 1 for last.
   Plurality with elimination: repeatedly drop the candidate(s) with the fewest first-place votes (if several tie for fewest, all of
   them are dropped together, unless that would drop everyone) until someone has a majority (more than half).
   Pairwise comparisons: 1 point for each head-to-head win, ½ for a tie. Ties for the win are reported, never broken.
   Weighted voting [q: w₁, …, wₙ]: a coalition wins if its weight ≥ q. Critical player: leaving makes a winning coalition lose.
   Banzhaf index = critical count / total critical count. Shapley–Shubik index = pivotal count / n!.
   Apportionment: standard divisor SD = total population / seats; quota = population / divisor. Hamilton: lower quotas, then
   leftover seats by largest fractional part. Jefferson rounds down, Webster rounds to nearest (0.5 rounds up), Adams rounds up,
   each with a modified divisor chosen so the seats add up. */
var css = L.h('style', null, document.head);
css.textContent = '.vt-cols{display:grid;gap:8px;margin:6px 0}.vt-col{display:flex;flex-wrap:wrap;gap:8px;align-items:end;padding:6px 8px;border:2px solid var(--line);border-radius:10px}' +
  '.vt-col label{font-weight:700;display:grid;gap:3px}.vt-col select,.vt-col input{min-height:40px;border:2px solid var(--ink);border-radius:8px;font-weight:700;font-size:1rem;background:var(--card);color:var(--ink)}.vt-col input{width:5em}' +
  '.vt-res{display:grid;gap:6px;margin:6px 0 8px}.vt-res div{padding:6px 10px;border-radius:8px;background:var(--wash)}.vt-res .w{background:var(--green-tint)}.vt-res .x{background:var(--orange-tint)}.vt-big{font-size:1.05rem;margin:2px 0 8px}' +
  '.vt-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:8px}';
var CAND = 'ABCD';
function perms(s) { if (s.length <= 1) return [s]; var out = []; s.split('').forEach(function (c, i) { perms(s.slice(0, i) + s.slice(i + 1)).forEach(function (p) { out.push(c + p); }); }); return out; }
var START = { tab: 'rank', k: 3, cols: [[10, 'ABC'], [6, 'BAC'], [4, 'CAB']], np: 3, q: 4, w: [3, 2, 2, 1, 1], pops: [450, 330, 220, 0, 0], ns: 3, seats: 10, meth: 'ham', div: null };
var st = JSON.parse(JSON.stringify(START)), seen = {};

/* ---------- ranked ballots ---------- */
function cands() { return CAND.slice(0, st.k).split(''); }
function firsts(alive) { var t = {}; alive.forEach(function (c) { t[c] = 0; }); st.cols.forEach(function (col) { for (var i = 0; i < col[1].length; i++) if (alive.indexOf(col[1][i]) >= 0) { t[col[1][i]] += col[0]; break; } }); return t; }
function winners(t) { var best = -Infinity, w = []; Object.keys(t).forEach(function (c) { if (t[c] > best + 1e-9) { best = t[c]; w = [c]; } else if (Math.abs(t[c] - best) < 1e-9) w.push(c); }); return w; }
function totalV() { return st.cols.reduce(function (s, c) { return s + c[0]; }, 0); }
function borda() { var t = {}; cands().forEach(function (c) { t[c] = 0; }); st.cols.forEach(function (col) { col[1].split('').forEach(function (c, i) { t[c] += col[0] * (st.k - i); }); }); return t; }
function h2h(x, y) { return st.cols.reduce(function (s, col) { return s + (col[1].indexOf(x) < col[1].indexOf(y) ? col[0] : 0); }, 0); }
function irv() {
  var alive = cands(), rounds = [], N = totalV();
  for (;;) {
    var t = firsts(alive); rounds.push({ alive: alive.slice(), t: t });
    var w = winners(t); if (t[w[0]] * 2 > N) return { win: w, rounds: rounds };
    var low = Math.min.apply(null, alive.map(function (c) { return t[c]; })), out = alive.filter(function (c) { return t[c] === low; });
    if (out.length === alive.length) return { win: alive.slice(), rounds: rounds, tie: true };
    alive = alive.filter(function (c) { return out.indexOf(c) < 0; }); rounds[rounds.length - 1].out = out;
    if (alive.length === 1) { rounds.push({ alive: alive.slice(), t: firsts(alive) }); return { win: alive, rounds: rounds }; }
  }
}
function pairwise() { var C = cands(), pts = {}, cond = null, rows = []; C.forEach(function (c) { pts[c] = 0; });
  for (var i = 0; i < C.length; i++) for (var j = i + 1; j < C.length; j++) { var a = h2h(C[i], C[j]), b = h2h(C[j], C[i]); rows.push([C[i], C[j], a, b]); if (a > b) pts[C[i]]++; else if (b > a) pts[C[j]]++; else { pts[C[i]] += 0.5; pts[C[j]] += 0.5; } }
  C.forEach(function (c) { if (C.every(function (d) { return d === c || h2h(c, d) > h2h(d, c); })) cond = c; });
  return { pts: pts, cond: cond, rows: rows }; }

/* ---------- weighted voting ---------- */
function power() {
  var n = st.np, w = st.w.slice(0, n), q = st.q, crit = w.map(function () { return 0; }), piv = w.map(function () { return 0; }), wins = [];
  for (var m = 1; m < 1 << n; m++) { var s = 0, mem = []; for (var i = 0; i < n; i++) if (m >> i & 1) { s += w[i]; mem.push(i); } if (s >= q) { var cr = mem.filter(function (i) { return s - w[i] < q; }); cr.forEach(function (i) { crit[i]++; }); wins.push({ mem: mem, s: s, cr: cr }); } }
  (function rec(order, used) { if (order.length === n) { var s = 0; for (var k = 0; k < n; k++) { s += w[order[k]]; if (s >= q) { piv[order[k]]++; break; } } return; } for (var i = 0; i < n; i++) if (!used[i]) { used[i] = true; order.push(i); rec(order, used); order.pop(); used[i] = false; } })([], []);
  var tot = w.reduce(function (a, b) { return a + b; }, 0);
  return { w: w, q: q, tot: tot, crit: crit, piv: piv, wins: wins, fact: [1, 1, 2, 6, 24, 120][n] };
}
/* ---------- apportionment ---------- */
function popList() { return st.pops.slice(0, st.ns); }
function ham(pops, seats) { var T = pops.reduce(function (a, b) { return a + b; }, 0), q = pops.map(function (p) { return p * seats / T; }), a = q.map(Math.floor), left = seats - a.reduce(function (x, y) { return x + y; }, 0);
  q.map(function (x, i) { return [x - a[i], i]; }).sort(function (x, y) { return y[0] - x[0] || x[1] - y[1]; }).slice(0, left).forEach(function (z) { a[z[1]]++; }); return a; }
function rnd(x) { return st.meth === 'jef' ? Math.floor(x + 1e-12) : st.meth === 'ada' ? Math.ceil(x - 1e-12) : Math.floor(x + 0.5 + 1e-12); }
function divApp(pops, d) { return pops.map(function (p) { return rnd(p / d); }); }
function findDiv(pops, seats) {
  var cands2 = [];
  pops.forEach(function (p) { for (var k = 1; k <= seats + 1; k++) { var c = st.meth === 'jef' ? p / k : st.meth === 'web' ? p / (k - 0.5) : (k > 1 ? p / (k - 1) : null); if (c) cands2.push(c); } });
  cands2.sort(function (a, b) { return a - b; }); cands2 = cands2.filter(function (c, i) { return i === 0 || c - cands2[i - 1] > 1e-9; });
  var sum = function (d) { return divApp(pops, d).reduce(function (a, b) { return a + b; }, 0); };
  var pts = [cands2[0] / 2].concat(cands2.map(function (c, i) { return i + 1 < cands2.length ? [c, cands2[i + 1]] : [c, c * 1.5]; }));
  for (var i = 1; i < pts.length; i++) { var lo = pts[i][0], hi = pts[i][1], mid = (lo + hi) / 2; if (sum(mid) === seats) { for (var dp = 0; dp <= 4; dp++) { var f = Math.pow(10, dp), x = Math.ceil(lo * f + 1e-9) / f; if (x < hi - 1e-9 && x > lo + 1e-9 && sum(x) === seats) return x; } return Math.round(mid * 1e4) / 1e4; } }
  return null;
}

/* ---------- controls ---------- */
var tabs = L.tabs(P.panel, [{ id: 'rank', label: 'Ranked ballots' }, { id: 'wt', label: 'Weighted voting' }, { id: 'app', label: 'Apportionment' }], function (id) { st.tab = id; show(); draw(); });
var bR = L.h('div', null, P.panel), bW = L.h('div', null, P.panel), bA = L.h('div', null, P.panel);
var kC = L.chips(bR, { label: 'Candidates', value: st.k, options: [{ value: 3, label: 'A, B, C' }, { value: 4, label: 'A, B, C, D' }], onChange: function (v) { st.k = v; st.cols.forEach(function (c) { c[1] = v === 4 ? (c[1].length === 3 ? c[1] + 'D' : c[1]) : c[1].replace('D', ''); }); buildCols(); draw(); } });
L.h('span', { style: 'font-weight:700' }, bR, 'Preference schedule: each column is a group of identical ballots');
var colBox = L.h('div', { class: 'vt-cols' }, bR);
var cRow = L.h('div', { class: 'btn-row' }, bR);
L.button(cRow, 'Add a column', function () { if (st.cols.length < 6) { st.cols.push([1, cands().join('')]); buildCols(); draw(); } }, true);
L.button(cRow, 'Remove last column', function () { if (st.cols.length > 1) { st.cols.pop(); buildCols(); draw(); } }, true);
function buildCols() {
  colBox.innerHTML = '';
  st.cols.forEach(function (col, i) {
    var row = L.h('div', { class: 'vt-col' }, colBox);
    var l1 = L.h('label', null, row, 'Column ' + (i + 1) + ': voters'), inp = L.h('input', { type: 'number', min: 0, max: 999, step: 1, value: col[0], id: 'vt-n' + i }, l1);
    inp.addEventListener('change', function () { col[0] = Math.max(0, Math.min(999, Math.round(+inp.value || 0))); inp.value = col[0]; draw(); });
    var l2 = L.h('label', null, row, 'Ranking (1st to last)'), s = L.h('select', { id: 'vt-r' + i }, l2);
    s.innerHTML = perms(cands().join('')).map(function (p) { return '<option value="' + p + '">' + p.split('').join(' > ') + '</option>'; }).join('');
    s.value = col[1]; s.addEventListener('change', function () { col[1] = s.value; draw(); });
  });
}
var npC = L.chips(bW, { label: 'Players', value: st.np, options: [{ value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }], onChange: function (v) { st.np = v; wGrid(); draw(); } });
var wBox = L.h('div', { class: 'vt-grid' }, bW), wIns = [];
function wGrid() { wBox.innerHTML = ''; wIns = []; for (var i = 0; i < st.np; i++) (function (i) { wIns.push(L.numInput(wBox, { id: 'w' + (i + 1), label: 'P' + (i + 1) + ' weight', min: 0, max: 99, step: 1, value: st.w[i], onChange: function (v) { st.w[i] = Math.round(v); draw(); } })); })(i); }
var qS = L.slider(bW, { id: 'quota', label: 'Quota q', min: 1, max: 60, value: st.q, color: 'purple', onInput: function (v) { st.q = v; draw(); } });
var nsC = L.chips(bA, { label: 'States', value: st.ns, options: [{ value: 3, label: '3' }, { value: 4, label: '4' }, { value: 5, label: '5' }], onChange: function (v) { st.ns = v; for (var i = 0; i < v; i++) if (!st.pops[i]) st.pops[i] = 100; pGrid(); st.div = null; draw(); } });
var pBox = L.h('div', { class: 'vt-grid' }, bA), pIns = [];
function pGrid() { pBox.innerHTML = ''; pIns = []; for (var i = 0; i < st.ns; i++) (function (i) { pIns.push(L.numInput(pBox, { id: 'pop' + (i + 1), label: 'State ' + (i + 1) + ' population', min: 1, max: 999999, step: 1, value: st.pops[i], onChange: function (v) { st.pops[i] = Math.round(v); st.div = null; draw(); } })); })(i); }
var seatIn = L.numInput(bA, { id: 'seats', label: 'Seats', min: 1, max: 99, step: 1, value: st.seats, onChange: function (v) { st.seats = Math.round(v); st.div = null; draw(); } });
var mC = L.chips(bA, { label: 'Method', value: st.meth, options: [{ value: 'ham', label: 'Hamilton' }, { value: 'jef', label: 'Jefferson' }, { value: 'web', label: 'Webster' }, { value: 'ada', label: 'Adams' }], onChange: function (v) { st.meth = v; draw(); } });
var divBox = L.h('div', null, bA);
var divIn = L.numInput(divBox, { id: 'divisor', label: 'Modified divisor', min: 0.01, max: 999999, step: 'any', value: 100, onChange: function (v) { st.div = v; draw(); } });
var dRow = L.h('div', { class: 'btn-row' }, divBox);
L.button(dRow, 'Use the standard divisor', function () { st.div = null; draw(); }, true);
L.button(dRow, 'Find a divisor that works', function () { var d = findDiv(popList(), st.seats); if (d) { st.div = d; draw(); } else fb.set('No single divisor gives exactly ' + st.seats + ' seats here (a tie in the quotients).', 'warn'); }, true);
var btns = L.h('div', { class: 'btn-row' }, P.panel);
L.reset(btns, function () { var t = st.tab; st = JSON.parse(JSON.stringify(START)); st.tab = t; kC.set(3, true); npC.set(3, true); nsC.set(3, true); mC.set('ham', true); qS.set(st.q, true); seatIn.set(st.seats); buildCols(); wGrid(); pGrid(); draw(); });
var fb = L.feedback(P.panel);
var ch = L.challenges(P.panel, [
  { text: 'Ranked ballots: change the schedule so that <b>plurality and Borda</b> pick different winners.', check: function () { return seen.pb; } },
  { text: 'Make a schedule with a <b>Condorcet winner</b> who does <b>not</b> win the plurality vote.', check: function () { return seen.cnp; } },
  { text: 'Make a schedule with <b>no Condorcet winner</b> (a voting cycle: A beats B, B beats C, C beats A).', check: function () { return seen.cyc; } },
  { text: 'Make a schedule where some candidate has a <b>majority</b> of first-place votes but the <b>Borda</b> count chooses someone else.', check: function () { return seen.maj; } },
  { text: 'Weighted voting: set up a valid system with a <b>dummy</b> (a player who is never critical) who has positive weight.', check: function () { return seen.dummy; } },
  { text: 'Find a valid system where some player has <b>veto power</b> but is <b>not a dictator</b>.', check: function () { return seen.veto; } },
  { text: 'Apportionment: use <b>Jefferson</b> with a modified divisor so the seats add up exactly.', check: function () { return seen.jef; } },
  { text: 'Find the <b>Alabama paradox</b>: with Hamilton, adding one seat makes some state lose a seat. (Hint: try populations 130, 690, 410 with 13 seats.)', check: function () { return seen.ala; } }
]);
L.notice(P.below, '<p><b>Name the method and the tie rule.</b> The four methods use the same ballots but answer different questions, so they can choose four different winners. Majority means <i>more than half</i>; a plurality can be less than half.</p>' +
  '<p><b>Fairness criteria.</b> Majority: a candidate with a majority of first places should win (Borda can fail). Condorcet: a candidate who beats every other head-to-head should win (plurality, Borda and elimination can fail). Arrow’s theorem: with three or more candidates, no ranked method satisfies every fairness condition.</p>' +
  '<p><b>Weighted voting.</b> A valid quota is more than half the total weight and at most the total. A dictator’s weight alone meets the quota; a player has veto power when everyone else together falls short; a dummy is never critical. Power is not proportional to weight: count critical appearances (Banzhaf) or pivotal positions (Shapley–Shubik).</p>' +
  '<p><b>Apportionment.</b> Hamilton always gives each state its lower or upper quota (the quota rule) but can show the Alabama, population and new-states paradoxes. Divisor methods (Jefferson, Webster, Adams) avoid those paradoxes but can violate the quota rule.</p>');

var big = L.h('div', { class: 'vt-big', 'aria-live': 'polite' }, P.stage);
var res = L.h('div', { class: 'vt-res', 'aria-live': 'polite' }, P.stage);
var tw = L.h('div', null, P.stage), tbl = L.table(tw), tw2 = L.h('div', null, P.stage), tbl2 = L.table(tw2);
function show() { bR.style.display = st.tab === 'rank' ? '' : 'none'; bW.style.display = st.tab === 'wt' ? '' : 'none'; bA.style.display = st.tab === 'app' ? '' : 'none'; }
function wlist(w) { return w.length === 1 ? '<b>' + w[0] + '</b>' : '<b>tie: ' + w.join(', ') + '</b> (this tool does not break ties)'; }
function nf(x) { return (Math.round(x * 1000) / 1000).toString(); }
function frac2(a, b) { if (!b) return '—'; var g = (function gc(x, y) { return y ? gc(y, x % y) : x; })(a, b); return (a / g) + '/' + (b / g); }

var draw = L.scheduler(function () {
  var C = cands();
  if (st.tab === 'rank') {
    var N = totalV(), pl = firsts(C), wP = winners(pl), bo = borda(), wB = winners(bo), ir = irv(), pw = pairwise(), wPW = winners(pw.pts);
    var majC = C.filter(function (c) { return pl[c] * 2 > N; })[0] || null;
    big.innerHTML = N + ' voters; a majority is more than ' + nf(N / 2) + ', so at least ' + (Math.floor(N / 2) + 1) + ' votes.' + (majC ? ' <b>' + majC + '</b> has a majority of first-place votes.' : ' No candidate has a majority of first places.');
    var R = [];
    R.push(['Plurality: ' + C.map(function (c) { return c + ' ' + pl[c]; }).join(', ') + ' → ' + wlist(wP), 1]);
    R.push(['Borda (' + st.k + ' points for 1st … 1 for last): ' + C.map(function (c) { return c + ' ' + bo[c]; }).join(', ') + ' → ' + wlist(wB), 1]);
    R.push(['Plurality with elimination: ' + ir.rounds.map(function (r, i) { return 'round ' + (i + 1) + ' (' + r.alive.map(function (c) { return c + ' ' + r.t[c]; }).join(', ') + ')' + (r.out ? ', drop ' + r.out.join(' and ') : ''); }).join('; ') + ' → ' + wlist(ir.win), 1]);
    R.push(['Pairwise comparisons: ' + C.map(function (c) { return c + ' ' + pw.pts[c]; }).join(', ') + ' points → ' + wlist(wPW), 1]);
    res.innerHTML = R.map(function (r) { return '<div>' + r[0] + '</div>'; }).join('');
    tbl.set(['Head-to-head', 'Votes', 'Winner'], pw.rows.map(function (r) { return [r[0] + ' vs ' + r[1], r[2] + '–' + r[3], r[2] > r[3] ? r[0] : r[3] > r[2] ? r[1] : 'tie']; }));
    tbl2.set(['Voters'].concat(st.cols.map(function (c) { return String(c[0]); })), C.map(function (_, i) { return [['1st', '2nd', '3rd', '4th'][i]].concat(st.cols.map(function (c) { return c[1][i]; })); }));
    var msgs = [];
    if (pw.cond) msgs.push('<b>' + pw.cond + '</b> is the Condorcet winner (beats everyone head-to-head).'); else msgs.push('There is <b>no Condorcet winner</b>.');
    var one = function (w) { return w.length === 1 ? w[0] : null; };
    [['Plurality', wP], ['Borda', wB], ['Elimination', ir.win], ['Pairwise', wPW]].forEach(function (m) {
      if (majC && one(m[1]) !== majC) msgs.push(m[0] + ' violates the <b>majority criterion</b> here.');
      else if (pw.cond && one(m[1]) !== pw.cond) msgs.push(m[0] + ' violates the <b>Condorcet criterion</b> here.');
    });
    fb.set(msgs.join(' '), msgs.length > 1 ? 'warn' : 'good');
    if (one(wP) && one(wB) && one(wP) !== one(wB)) seen.pb = true;
    if (pw.cond && wP.indexOf(pw.cond) < 0) seen.cnp = true;
    if (!pw.cond && N > 0 && pw.rows.every(function (r) { return r[2] !== r[3]; })) seen.cyc = true;
    if (majC && one(wB) !== majC) seen.maj = true;
  } else if (st.tab === 'wt') {
    var p = power(), valid = p.q > p.tot / 2 && p.q <= p.tot;
    qS.input.max = Math.max(1, p.tot); if (st.q > p.tot && p.tot > 0) { st.q = p.tot; qS.set(p.tot, true); p = power(); valid = p.q > p.tot / 2 && p.q <= p.tot; }
    big.innerHTML = '[' + p.q + ': ' + p.w.join(', ') + '] &nbsp; total weight ' + p.tot + '. ' + (valid ? 'Valid quota (more than ' + nf(p.tot / 2) + ', at most ' + p.tot + ').' : '<b>Not a valid quota</b>: it must be more than half the total (' + nf(p.tot / 2) + ') and at most ' + p.tot + '.');
    var tc = p.crit.reduce(function (a, b) { return a + b; }, 0), roles = p.w.map(function (w, i) { var others = p.tot - w, r = []; if (w >= p.q) r.push('dictator'); else if (others < p.q) r.push('veto power'); if (p.crit[i] === 0) r.push('dummy'); return r.join(', ') || '—'; });
    tbl.set(['Player', 'Weight', 'Times critical', 'Banzhaf index', 'Times pivotal', 'Shapley–Shubik index', 'Role'], p.w.map(function (w, i) { return ['P' + (i + 1), w, p.crit[i], tc ? frac2(p.crit[i], tc) + ' ≈ ' + nf(p.crit[i] / tc) : '—', p.piv[i], frac2(p.piv[i], p.fact) + ' ≈ ' + nf(p.piv[i] / p.fact), roles[i]]; }));
    res.innerHTML = '<div><b>' + p.wins.length + ' winning coalition' + (p.wins.length === 1 ? '' : 's') + '</b> (critical players in bold): ' + (p.wins.length ? p.wins.map(function (c) { return '{' + c.mem.map(function (i) { return c.cr.indexOf(i) >= 0 ? '<b>P' + (i + 1) + '</b>' : 'P' + (i + 1); }).join(', ') + '} ' + c.s; }).join(' &nbsp; ') : 'none') + '</div>';
    tbl2.set([], []);
    var wv = p.w.slice().sort(function (a, b) { return b - a; });
    fb.set(valid ? 'Banzhaf counts: ' + p.crit.join(', ') + ' (total ' + tc + '). Compare the indices with the weights: power is not proportional to weight.' : 'With this quota, two opposing coalitions could both win (or nobody can win). Fix the quota first.', valid ? '' : 'warn');
    if (valid && p.w.some(function (w, i) { return w > 0 && p.crit[i] === 0; })) seen.dummy = true;
    if (valid && p.w.some(function (w) { return w < p.q && p.tot - w < p.q; })) seen.veto = true;
  } else {
    var pops = popList(), T = pops.reduce(function (a, b) { return a + b; }, 0), SD = T / st.seats, isDiv = st.meth !== 'ham', d = isDiv ? (st.div || SD) : SD;
    divBox.style.display = isDiv ? '' : 'none'; if (isDiv) divIn.set(Math.round(d * 10000) / 10000);
    var a = isDiv ? divApp(pops, d) : ham(pops, st.seats), sum = a.reduce(function (x, y) { return x + y; }, 0);
    big.innerHTML = 'Total population ' + T.toLocaleString() + ', ' + st.seats + ' seats: standard divisor SD = ' + nf(SD) + (isDiv ? '; divisor used d = ' + nf(d) : '') + '.';
    var name = { ham: 'Hamilton', jef: 'Jefferson (round down)', web: 'Webster (round to nearest)', ada: 'Adams (round up)' }[st.meth];
    tbl.set(['State', 'Population', 'Standard quota', 'Lower / upper', isDiv ? 'Modified quota' : 'Fractional part', name + ' seats', 'Quota rule'], pops.map(function (pp, i) {
      var q = pp / SD, lo = Math.floor(q + 1e-12), up = Math.ceil(q - 1e-12), okQ = a[i] === lo || a[i] === up;
      return ['State ' + (i + 1), pp.toLocaleString(), nf(q), lo + ' / ' + up, isDiv ? nf(pp / d) : nf(q - lo), '<b>' + a[i] + '</b>', okQ ? 'satisfied' : '<b>violated</b>'];
    }).concat([['Total', T.toLocaleString(), nf(st.seats), '', '', '<b>' + sum + '</b>', '']]));
    var h1 = ham(pops, st.seats), h2 = ham(pops, st.seats + 1), lose = h1.map(function (x, i) { return h2[i] < x ? i : -1; }).filter(function (i) { return i >= 0; });
    res.innerHTML = '<div class="' + (lose.length ? 'x' : '') + '">Alabama paradox check (Hamilton, ' + st.seats + ' → ' + (st.seats + 1) + ' seats): ' + h1.join(', ') + ' → ' + h2.join(', ') + '. ' + (lose.length ? '<b>State ' + lose.map(function (i) { return i + 1; }).join(' and ') + ' loses a seat even though the house grew.</b>' : 'No state loses a seat.') + '</div>';
    tbl2.set([], []);
    var viol = pops.some(function (pp, i) { var q = pp / SD; return a[i] !== Math.floor(q + 1e-12) && a[i] !== Math.ceil(q - 1e-12); });
    fb.set(isDiv && sum !== st.seats ? 'The rounded quotas add to ' + sum + ', not ' + st.seats + '. ' + (sum > st.seats ? 'Make the divisor larger.' : 'Make the divisor smaller.') + ' (Or press “Find a divisor that works”.)' :
      'The seats add up to ' + st.seats + '.' + (viol ? ' This apportionment <b>violates the quota rule</b>.' : ''), isDiv && sum !== st.seats ? 'warn' : viol ? 'warn' : 'good');
    if (st.meth === 'jef' && sum === st.seats && Math.abs(d - SD) > 1e-9) seen.jef = true;
    if (lose.length) seen.ala = true;
  }
  ch.update();
});
buildCols(); wGrid(); pGrid(); show(); draw();
