'use strict';
/* Discrete Math audit (2026-11-18): regression checks for the fixes, plus independent recomputation of the
 * election, weighted-voting, apportionment, linear-programming and relation families (audit #20).
 * Usage: node scripts/test-discrete-audit.cjs */
const fs = require('fs'), path = require('path'), assert = require('assert/strict');
const ROOT = path.resolve(__dirname, '..'), DIR = path.join(ROOT, 'question-banks/discrete');
const banks = fs.readdirSync(DIR).filter(f => f.endsWith('.json')).map(f => JSON.parse(fs.readFileSync(path.join(DIR, f), 'utf8')));
const Q = banks.flatMap(b => b.questions);
const fam = q => (/family: ([a-z0-9_-]+)\)/.exec(q.sourceNotes || '') || [])[1] || '';
const allText = q => [q.prompt, JSON.stringify(q.answer), ...(q.solutionSteps || []), ...(q.options || []).map(o => o.text), ...(q.parts || []).flatMap(p => [p.prompt, p.answer])].join('\n');
const gcd = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
const frac = (n, d) => { const g = gcd(n, d) || 1; n /= g; d /= g; if (d < 0) { n = -n; d = -d; } return d === 1 ? String(n) : n + '/' + d; };
let checked = 0;
const fails = [];
const check = (q, ok, msg) => { checked++; if (!ok) fails.push(q.id + ': ' + msg); };

/* #10 multiple-choice keys are spread over the positions. */
const mc = Q.filter(q => q.format === 'multiple-choice' && q.options.length === 4), pos = [0, 0, 0, 0];
for (const q of mc) pos[q.options.findIndex(o => o.correct)]++;
for (const n of pos) assert(n / mc.length >= 0.2 && n / mc.length <= 0.3, 'MC key positions ' + pos.join('/'));

/* #13 #15 #16 text: no authoring notes, Python output, template grammar slips or references to other items. */
for (const q of Q) {
  const t = allText(q);
  check(q, !/other choices are near misses/.test(t), 'authoring note in solution');
  check(q, !/\{'[^']+': /.test(t), 'Python dict in solution');
  check(q, !/\b1 hours\b|with 1 elements|1 of the options appear\b|(?<![\d.,/\w])1[xy]\b|\{1, 2, \.\.\., [1-3]\}/.test(t), 'template grammar');
  check(q, !/^(Same |Using the same|The same )/.test(q.prompt), 'depends on another item');
}
/* #14 money is in dollars and cents. */
for (const q of Q.filter(q => fam(q) === 'sealed_bids')) check(q, !/^-?\d+\/\d+$/.test(String(q.answer)) && !/fraction a\/b/.test(q.prompt), 'money as a fraction');
/* #17 the binding-constraint item asks what its key answers. */
{ const q = Q.find(q => q.id === 'dm-lp-s07-cp1-005'); assert(/which statements are true/.test(q.prompt) && q.answer.includes('x + y ≤ 30 is binding (it uses 30 of 30)')); }
/* #9 Relations on Finite and Infinite Sets is about infinite sets. */
{
  const s4 = Q.filter(q => q.skillId === 'properties-relations-skill-04');
  const inf = s4.filter(q => /ℤ|ℝ|ℕ|ℚ|infinite|integers|real/.test(q.prompt));
  assert(inf.length / s4.length >= 0.9, 'infinite-set items in skill 4: ' + inf.length + '/' + s4.length);
}
/* #20 every item has a family tag. */
for (const q of Q) check(q, !!fam(q), 'no family tag');
/* #12 no preference schedule or weighted system repeats within the computed election families. */
{
  const seen = new Map();
  for (const q of Q.filter(q => ['method_winner', 'condorcet_check', 'first_place', 'head_to_head', 'borda_points'].includes(fam(q)) && q.format !== 'open-response')) {
    const k = (q.prompt.match(/\d+ voters: [A-Z](?: > [A-Z])+/g) || []).join('|');
    if (k) { check(q, !seen.has(k), 'schedule repeats ' + seen.get(k)); seen.set(k, q.id); }
  }
}

/* ---------- independent recomputation ---------- */
const sched = P => [...P.matchAll(/(\d+) voters: ([A-Z](?: > [A-Z])+)/g)].map(m => [+m[1], m[2].split(' > ')]);
const h2h = (R, a, b) => R.reduce((s, [n, r]) => s + (r.indexOf(a) < r.indexOf(b) ? n : 0), 0);
const tallyTop = c => { const m = Math.max(...Object.values(c)), w = Object.keys(c).filter(k => c[k] === m); return w.length === 1 ? w[0] : null; };
const first = R => { const c = {}; for (const x of R[0][1]) c[x] = 0; for (const [n, r] of R) c[r[0]] += n; return c; };
const borda = R => { const c = {}; for (const x of R[0][1]) c[x] = 0; for (const [n, r] of R) r.forEach((x, i) => { c[x] += n * (r.length - i); }); return c; };
const pairwise = R => { const C = [...R[0][1]].sort(), c = {}; C.forEach(x => c[x] = 0); for (let i = 0; i < C.length; i++) for (let j = i + 1; j < C.length; j++) { const x = h2h(R, C[i], C[j]), y = h2h(R, C[j], C[i]); if (x > y) c[C[i]] += 2; else if (y > x) c[C[j]] += 2; else { c[C[i]]++; c[C[j]]++; } } return c; };
const irv = R => { let C = [...R[0][1]]; const tot = R.reduce((s, [n]) => s + n, 0); for (;;) { const c = {}; C.forEach(x => c[x] = 0); for (const [n, r] of R) c[r.find(x => C.includes(x))] += n; for (const x of C) if (2 * c[x] > tot) return x; const lo = Math.min(...Object.values(c)), out = C.filter(x => c[x] === lo); if (out.length > 1) return null; C = C.filter(x => !out.includes(x)); } };
const condorcet = R => R[0][1].find(a => R[0][1].every(b => b === a || h2h(R, a, b) > h2h(R, b, a))) || null;
const coalitions = (q, w) => { const out = []; for (let m = 1; m < 1 << w.length; m++) { const S = w.map((_, i) => i).filter(i => (m >> i) & 1); if (S.reduce((s, i) => s + w[i], 0) >= q) out.push(S); } return out; };
const banzhaf = (q, w) => { const c = w.map(() => 0); for (const S of coalitions(q, w)) { const s = S.reduce((t, i) => t + w[i], 0); for (const i of S) if (s - w[i] < q) c[i]++; } return c; };
const perms = a => a.length <= 1 ? [a] : a.flatMap((x, i) => perms([...a.slice(0, i), ...a.slice(i + 1)]).map(p => [x, ...p]));
const shapley = (q, w) => { const c = w.map(() => 0); for (const p of perms(w.map((_, i) => i))) { let s = 0; for (const i of p) { s += w[i]; if (s >= q) { c[i]++; break; } } } return c; };
const quotaSys = P => { const m = /\[(\d+): ([\d, ]+)\]/.exec(P); return m ? [+m[1], m[2].split(',').map(Number)] : null; };
for (const q of Q) {
  const f = fam(q), P = q.prompt.replace(/[‑]/g, '-'), A = String(q.answer);
  if (q.format === 'open-response') continue;
  const R = sched(P);
  if (f === 'method_winner' && R.length) {
    const w = /plurality with elimination|instant runoff/.test(P) ? irv(R) : /Borda/.test(P) ? tallyTop(borda(R)) : /pairwise/.test(P) ? tallyTop(pairwise(R)) : /plurality/.test(P) ? tallyTop(first(R)) : undefined;
    if (w !== undefined) check(q, A === (w || 'There is a tie'), 'winner ' + w);
  }
  if (f === 'condorcet_check' && R.length && q.format === 'multiple-choice') { const c = condorcet(R); check(q, A === (c ? 'Yes, ' + c : 'No Condorcet winner'), 'Condorcet ' + c); }
  if (f === 'first_place' && R.length) check(q, A === String(first(R)[/does ([A-Z]) receive/.exec(P)[1]]), 'first-place count');
  if (f === 'head_to_head' && R.length) { const [, a, b] = /prefer ([A-Z]) to ([A-Z])/.exec(P); check(q, A === String(h2h(R, a, b)), 'head-to-head'); }
  if (f === 'borda_points' && R.length) check(q, A === String(borda(R)[/Find ([A-Z])'s total/.exec(P)[1]]), 'Borda points');
  const W = quotaSys(P);
  if (W && !/_error$/.test(f)) {
    const [qq, w] = W;
    if (f === 'count_winning') check(q, A === String(coalitions(qq, w).length), 'winning coalitions');
    if (f === 'veto') check(q, A === (w.map((x, i) => w.reduce((s, y) => s + y, 0) - x < qq ? 'P' + (i + 1) : null).filter(Boolean).join(', ') || 'none'), 'veto players');
    if (f === 'banzhaf' && /index of P1/.test(P)) { const c = banzhaf(qq, w); check(q, A === frac(c[0], c.reduce((s, x) => s + x, 0)), 'Banzhaf'); }
    if (f === 'shapley') { const c = shapley(qq, w); check(q, A === frac(c[0], c.reduce((s, x) => s + x, 0)), 'Shapley–Shubik'); }
  }
  if (f === 'standard_divisor') { const pops = [...P.split('seats')[0].matchAll(/[A-Za-z]+ (\d+)/g)].map(m => +m[1]), S = +/(\d+) seats/.exec(P)[1]; check(q, A === frac(pops.reduce((s, x) => s + x, 0), S), 'standard divisor'); }
  if (f === 'divisor_method') {
    const pops = [...P.split('seats')[0].matchAll(/[A-Za-z]+ (\d+)/g)].map(m => +m[1]), S = +/(\d+) seats/.exec(P)[1];
    const mode = /Jefferson/.test(P) ? 'down' : /Adams/.test(P) ? 'up' : 'near', a = pops.map(() => mode === 'up' ? 1 : 0);
    const pri = i => mode === 'down' ? pops[i] / (a[i] + 1) : mode === 'up' ? pops[i] / a[i] : pops[i] / (a[i] + 0.5);
    while (a.reduce((s, x) => s + x, 0) < S) { let b = 0; for (let i = 1; i < a.length; i++) if (pri(i) > pri(b)) b = i; a[b]++; }
    check(q, A === a.join(', '), mode + ' apportionment');
  }
  if (f === 'test_point') {
    const [x, y] = /\((-?\d+), (-?\d+)\)/.exec(P).slice(1).map(Number);
    const ok = /system (.*?)\?$/.exec(P)[1].split('; ').every(c => { const m = /^(.*?) (≤|≥) (-?\d+)$/.exec(c.trim()); const v = Function('x', 'y', 'return ' + m[1].replace(/(\d)([xy])/g, '$1*$2'))(x, y); return m[2] === '≤' ? v <= +m[3] : v >= +m[3]; });
    check(q, A === (ok ? 'Yes' : 'No'), 'test point');
  }
  if (f === 'check_property') {
    const dom = /A = \{([^}]*)\}/.exec(P)[1].split(',').map(Number), rs = /R = (∅|\{.*?\})\. Is/.exec(P)[1];
    const R2 = rs === '∅' ? [] : [...rs.matchAll(/\((\d+), (\d+)\)/g)].map(m => [+m[1], +m[2]]), has = (a, b) => R2.some(([x, y]) => x === a && y === b);
    const prop = /Is R (\w+)\?/.exec(P)[1];
    const v = { reflexive: dom.every(a => has(a, a)), symmetric: R2.every(([a, b]) => has(b, a)), transitive: R2.every(([a, b]) => R2.every(([c, d]) => b !== c || has(a, d))) }[prop];
    check(q, A === (v ? 'Yes' : 'No'), prop);
  }
}
if (fails.length) { console.error(fails.slice(0, 40).join('\n')); console.error(fails.length + ' problems'); process.exit(1); }
console.log('PASS Discrete Math audit fixes; MC key positions ' + pos.join('/') + '; ' + checked + ' checks');
