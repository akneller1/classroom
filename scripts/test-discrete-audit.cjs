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

/* #1 solutions show the work: at least 2 steps everywhere, an option-by-option line on every select-all, and short
   solutions (under 60 characters) are rare. */
{
  let short = 0;
  for (const q of Q.filter(q => q.format !== 'open-response')) {
    check(q, q.solutionSteps.length >= 2, 'fewer than 2 solution steps');
    if (q.solutionSteps.join(' ').length < 60) short++;
    if (q.format === 'select-all') check(q, q.solutionSteps.some(x => /^Option by option: /.test(x) && q.options.every(o => x.includes(o.text))), 'select-all without a line per option');
  }
  assert(short / Q.length <= 0.05, 'short solutions: ' + short);
}
/* #2 at most 4 one-line quick checks per skill and level. */
{
  const n = {};
  for (const q of Q.filter(q => fam(q) === 'quick_check')) { const k = q.skillId + '/' + q.level; n[k] = (n[k] || 0) + 1; }
  for (const [k, v] of Object.entries(n)) assert(v <= 4, 'quick checks in ' + k + ': ' + v);
}
/* #4 no Advanced item is a Support template with new numbers. */
{
  const tmpl = s => s.replace(/\{[^}]*\}/g, '{S}').replace(/\[[^\]]*\]/g, '[W]').replace(/\b(Kim|Lee|Ann|Ben|Ana|Bo|Cy|Sam|Jordan|Riley|Casey|Avery|Morgan|Taylor|Jamie|Quinn|Alex)\b/g, 'Nm').replace(/[A-Z](?: > [A-Z])+/g, 'R').replace(/\d+(\.\d+)?/g, '#');
  const cp2 = new Set(Q.filter(q => q.level === 'cp2').map(q => q.skillId + '|' + tmpl(q.prompt)));
  // An Advanced clone may stay only when it is pinned (release fixture, partner-check target) or when its skill is at the floor
  // the Advanced game decks and Tarsia puzzles need (5 multiple-choice and 4 short-answer Advanced items).
  const fixed = new Set(require('../tests/fixtures/content-20261115.json').filter(e => e.course === 'discrete').map(e => e.id));
  for (const q of Q) { const m = /^Partner-check companion to (\S+) /.exec(q.sourceNotes || ''); if (m) fixed.add(m[1]); }
  const KEEP = { 'multiple-choice': 5, 'short-answer': 4 }, n = {};
  for (const q of Q.filter(q => q.level === 'honors')) n[q.skillId + q.format] = (n[q.skillId + q.format] || 0) + 1;
  const clones = Q.filter(q => q.level === 'honors' && cp2.has(q.skillId + '|' + tmpl(q.prompt)));
  for (const q of clones) check(q, fixed.has(q.id) || n[q.skillId + q.format] <= (KEEP[q.format] || 0), 'Advanced item reuses a Support template');
  assert(clones.length <= 120, 'Advanced clones of Support templates: ' + clones.length);
}
/* #3 the practice test grades sets, truth columns, lists, statement forms and one-word answers. */
{
  const vm = require('vm'), c = {}; c.window = c; vm.createContext(c);
  for (const f of ['worksheet-generator/menu/mathcheck.js', 'worksheet-generator/practice/radical-grading.js', 'worksheet-generator/practice/exact-grading.js', 'worksheet-generator/practice/discrete-grading.js', 'worksheet-generator/practice/grading.js'])
    vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), c, { filename: f });
  const P = c.MKPRACTICE, sa = Q.filter(q => q.format === 'short-answer'), auto = sa.filter(q => P.bankAnswer(String(q.answer)) !== null);
  assert(auto.length / sa.length >= 0.8, 'auto-graded short answers ' + auto.length + '/' + sa.length);
  for (const q of auto) check(q, P.gradeBank(String(q.answer), String(q.answer)).status === 'correct', 'key does not grade itself correct');
  for (const [k, t, want] of [['{2, 4, 6}', '{6,4,2}', 'correct'], ['{2, 4, 6}', '{2, 4}', 'incorrect'], ['∅', '{}', 'correct'], ['{(1, 2), (2, 3)}', '{(2,3),(1,2)}', 'correct'],
    ['TFTT', 't f t t', 'correct'], ['TFTT', 'TFTF', 'incorrect'], ['(F, T)', 'F,T', 'correct'], ['13, 11, 6', '13,11,6', 'correct'], ['13, 11, 6', '6, 11, 13', 'incorrect'],
    ['P1, P2', 'P2, P1', 'correct'], ['p ∧ ¬q', '~q ^ p', 'correct'], ['p ∧ ¬q', 'p ∨ q', 'incorrect'], ['p ∧ ¬q', '¬(¬p ∨ q)', 'self'], ['Yes', 'yes', 'correct'], ['Yes', 'no', 'incorrect'],
    ['q = 3, r = 2', 'r=2, q=3', 'correct'], ['A', 'a', 'correct'], ['27.50', '27.5', 'correct']])
    assert.equal(P.gradeBank(k, t).status, want, k + ' ← ' + t);
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

/* #5 the lesson planner has teaching notes for every Discrete Math skill. */
{
  const vm = require('vm'), w = { console, Math, Date, JSON }; w.window = w; w.globalThis = w; vm.createContext(w);
  for (const rel of ['data.js', 'course-catalog.js', 'worksheet-generator/menu/standards.js', 'worksheet-generator/menu/standards-map.js',
    'worksheet-generator/planner/notes-teach-discrete.js', 'worksheet-generator/planner/scope-algebra2.js'])
    vm.runInContext(fs.readFileSync(path.join(ROOT, rel), 'utf8'), w, { filename: rel });
  const N = w.MKPLAN_TEACH.discrete, course = w.LIBRARY.courses.find(c => c.id === 'discrete');
  let skills = 0;
  for (const u of course.units) for (const s of w.MK_COURSE_CATALOG.getSkillRecords('discrete', u.id)) {
    skills++;
    const r = N[s.id];
    assert(r && r.obj && !/^work with /.test(r.obj) && r.idea.length > 20 && r.watch, 'teaching notes for ' + s.id);
    assert(Array.isArray(r.voc) && r.voc.length >= 2 && r.voc.every(v => v[0] && v[1]), s.id + ' vocabulary');
    assert(r.cards.length >= 1 && r.cards.every(c => c.h && c.big && c.steps.length >= 2 && c.steps.some(x => /\{\{/.test(x))), s.id + ' card with blanks');
  }
  assert.equal(Object.keys(N).length, skills, 'no notes outside the catalog');
  const lessons = w.MKPLAN_SCOPE_DISCRETE.days.filter(d => d.day_type === 'Lesson');
  assert.equal(lessons.length, skills);
  for (const d of lessons) assert(!/able to work with /.test(d.content_objective) && d.key_vocabulary && d.common_misconception, d.lesson_id + ' planner fields');
  const html = fs.readFileSync(path.join(ROOT, 'worksheet-generator/lesson-planner.html'), 'utf8');
  assert(html.indexOf('planner/notes-teach-discrete.js') > 0 && html.indexOf('planner/notes-teach-discrete.js') < html.indexOf('planner/scope-algebra2.js'), 'planner page loads the Discrete notes first');
  console.log('PASS Discrete Math teaching notes for ' + skills + ' skills');
}

/* #7 skill-level standards; #8 drawn graphs; #11 proof writing; #18 LP Graphing Practice; #19 Speaking Mathematically lab. */
{
  const STD = require(path.join(ROOT, 'worksheet-generator/menu/standards.js'));
  const STRAND = { 'speaking-mathematically': 'LANG', 'compound-statements-logic': 'LOGIC', 'number-theory-proof': 'PROOF', 'sequences-induction-recursion': 'INDUCTION', 'set-theory': 'SETS', 'properties-relations': 'RELATIONS', 'counting-probability': 'COUNTING', 'graphs-trees': 'GRAPHS', 'election-theory': 'ELECTIONS', 'linear-programming': 'LP' };
  for (const q of Q) {
    const [unit, n] = q.skillId.split('-skill-'), code = 'DM.' + STRAND[unit] + '.' + Number(n);
    check(q, q.standards[0] === code && STD.describe(code), 'skill-level strand ' + code);
    check(q, !(q.standards.includes('MP.4') && /^graphs-trees-skill-0[1235]/.test(q.skillId)), 'modeling tag on a graph-structure skill');
    check(q, !q.standards.includes('G-CO.A.5'), 'transformation standard on a pattern item');
    if (/^graphs-trees/.test(q.skillId) && /vertices [A-Z](?:, [A-Z])+ and edges [A-Z]{2}/.test(q.prompt))
      check(q, q.diagram && fs.existsSync(path.join(ROOT, q.diagram.spec.src)), 'graph given as an edge list has no drawing');
  }
  for (const sk of ['number-theory-proof-skill-02', 'number-theory-proof-skill-06', 'number-theory-proof-skill-07', 'set-theory-skill-06', 'set-theory-skill-07', 'sequences-induction-recursion-skill-08']) {
    const s = Q.filter(q => q.skillId === sk);
    assert(s.filter(q => q.format === 'open-response').length >= 9 && s.filter(q => fam(q) === 'proof_order').length >= 6, sk + ' proof writing');
  }
  const plots = Q.filter(q => q.format === 'plot' && /^linear-programming/.test(q.skillId));
  assert(plots.length >= 24 && ['cp2', 'cp1', 'honors'].every(l => plots.filter(q => q.level === l).length >= 8), 'LP Graphing Practice items');
  const vm = require('vm'), dctx = { window: {} }; vm.runInNewContext(fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8'), dctx);
  assert(/"discrete":\["linear-programming"\]/.test(fs.readFileSync(path.join(ROOT, 'data.js'), 'utf8')), 'Graphing Practice enabled for Linear Programming');
  const sm = dctx.window.LIBRARY.courses.find(c => c.id === 'discrete').units.find(u => u.id === 'speaking-mathematically');
  assert(sm.artifacts.some(a => a.path === 'artifacts/discrete-quantifier-explorer/index.html' && fs.existsSync(path.join(ROOT, a.worksheet)) && fs.existsSync(path.join(ROOT, a.thumb))), 'Quantifier & Set-Notation Explorer card');
  console.log('PASS Discrete Math standards, drawings, proofs, graphing practice and lab');
}
if (fails.length) { console.error(fails.slice(0, 40).join('\n')); console.error(fails.length + ' problems'); process.exit(1); }
console.log('PASS Discrete Math audit fixes; MC key positions ' + pos.join('/') + '; ' + checked + ' checks');
