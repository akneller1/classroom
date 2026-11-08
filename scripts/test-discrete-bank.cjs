'use strict';
/* Discrete Math bank verification (independent of the Python authoring code).
 * 1. Every bank passes the site's own validator (question-bank-adapter.js) against course-catalog.js skills.
 * 2. Coverage: every catalog skill has >= 30 questions, >= 8 per level; >= 12 error-analysis items per unit (>= 4 per level).
 * 3. Structural checks: MC key = the single correct option; select-all has >= 2 correct and >= 1 wrong; open response >= 4 parts;
 *    images exist; no duplicate prompts; error-analysis items follow the authored format (first step "Mistake:").
 * 4. Independent recomputation of parseable families: truth-table columns, set operations/complements, list counts,
 *    gcd/lcm, Fibonacci terms, dice-sum probabilities, Hamilton apportionment, Banzhaf indices, and LP optima.
 * Usage: node scripts/test-discrete-bank.cjs */
const fs = require('fs'), vm = require('vm'), path = require('path'), assert = require('assert/strict');
const root = path.resolve(__dirname, '..'), g = { window: {} };
for (const p of ['data.js', 'course-catalog.js', 'question-bank-adapter.js']) vm.runInNewContext(fs.readFileSync(path.join(root, p), 'utf8'), g);
const W = g.window, course = W.LIBRARY.courses.find(c => c.id === 'discrete');
assert(course, 'discrete course missing');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'question-banks/manifest.json'), 'utf8'));
let total = 0, recomputed = 0, fails = [];
const fail = (q, msg) => fails.push(q.id + ': ' + msg);
const fam = q => (/family: ([a-z0-9_]+)\)/.exec(q.sourceNotes || '') || [])[1] || '';
const fracStr = (n, d) => { const gg = gcd(Math.abs(n), Math.abs(d)) || 1; n /= gg; d /= gg; if (d < 0) { n = -n; d = -d; } return d === 1 ? String(n) : n + '/' + d; };
function gcd(a, b) { while (b) [a, b] = [b, a % b]; return a; }
const norm = s => String(s).replace(/−/g, '-').replace(/‑/g, '-');

/* ---------- independent propositional evaluator ---------- */
function evalProp(src, env) {
  const t = src.replace(/\s+/g, ''); let i = 0;
  const prec = { '∧': 3, '∨': 2, '⊕': 2, '→': 1, '↔': 0 };
  function prim() {
    const c = t[i];
    if (c === '¬') { i++; return !prim(); }
    if (c === '(') { i++; const v = ex(0); if (t[i] !== ')') throw Error('paren ' + src); i++; return v; }
    if (/[a-z]/.test(c)) { i++; return env[c]; }
    throw Error('token ' + c + ' in ' + src);
  }
  function ex(min) {
    let l = prim();
    while (i < t.length && prec[t[i]] !== undefined && prec[t[i]] >= min) {
      const op = t[i++], r = ex(op === '→' || op === '↔' ? prec[op] : prec[op] + 1);
      l = op === '∧' ? l && r : op === '∨' ? l || r : op === '⊕' ? l !== r : op === '→' ? (!l || r) : l === r;
    }
    return l;
  }
  const v = ex(0); if (i !== t.length) throw Error('trailing in ' + src); return v;
}
function column(f, vars) {
  const out = [];
  for (let m = 0; m < 1 << vars.length; m++) {
    const env = {}; vars.forEach((v, k) => { env[v] = !((m >> (vars.length - 1 - k)) & 1); });
    out.push(evalProp(f, env) ? 'T' : 'F');
  }
  return out.join('');
}

/* ---------- set parsing ---------- */
const parseSet = s => s.trim() === '∅' ? [] : s.replace(/[{}]/g, '').split(',').map(x => x.trim()).filter(Boolean).map(x => /^-?\d+$/.test(norm(x)) ? Number(norm(x)) : x);
const fmtSet = a => { const b = [...new Set(a)].sort((x, y) => typeof x === 'number' && typeof y === 'number' ? x - y : String(x) < String(y) ? -1 : 1); return b.length ? '{' + b.join(', ') + '}' : '∅'; };
function setEval(e, env, U) {
  const t = e.replace(/\s+/g, ''); let i = 0;
  const has = (S, x) => S.some(y => y === x);
  function atom() {
    let v; const c = t[i];
    if (c === '(') { i++; v = ex(); i++; } else if (c === '∅') { i++; v = []; } else { i++; v = c === 'U' ? U : env[c]; }
    while (t[i] === "'") { i++; const w = v; v = U.filter(x => !has(w, x)); }
    return v;
  }
  function ex() {
    let v = atom();
    while (i < t.length && '∪∩−'.includes(t[i])) {
      const op = t[i++], w = atom(), a = v;
      v = op === '∪' ? [...a, ...w.filter(x => !has(a, x))] : op === '∩' ? a.filter(x => has(w, x)) : a.filter(x => !has(w, x));
    }
    return v;
  }
  return ex();
}


/* ---------- quick checks: every one-line template is recomputed from its numbers ---------- */
const comb = (n, r) => { let x = 1; for (let i = 1; i <= r; i++) x = x * (n - r + i) / i; return Math.round(x); };
const isPrime = n => { if (n < 2) return false; for (let d = 2; d * d <= n; d++) if (n % d === 0) return false; return true; };
function quickAnswer(P) {
  let m; const N = s => +s;
  const R = [
    [/^How many subsets does a set with (\d+) elements have\?$/, m => 2 ** N(m[1])],
    [/^How many proper subsets does a set with (\d+) elements have\?$/, m => 2 ** N(m[1]) - 1],
    [/^If \|A\| = (\d+) and \|B\| = (\d+), find \|A × B\|\.$/, m => N(m[1]) * N(m[2])],
    [/^\|A\| = (\d+) and \|B\| = (\d+)\. Find \|A × B\|\.$/, m => N(m[1]) * N(m[2])],
    [/^How many bit strings have length (\d+)\?$/, m => 2 ** N(m[1])],
    [/^How many strings of length 2 use an alphabet of (\d+) letters/, m => N(m[1]) ** 2],
    [/^How many elements are in \{n ∈ ℤ \| (-?\d+) ≤ n ≤ (-?\d+)\}\?$/, m => N(m[2]) - N(m[1]) + 1],
    [/^Find gcd\((\d+), (\d+)\)\.$/, m => gcd(N(m[1]), N(m[2]))],
    [/^Find lcm\((\d+), (\d+)\)\.$/, m => N(m[1]) * N(m[2]) / gcd(N(m[1]), N(m[2]))],
    [/^Find the remainder when (\d+) is divided by (\d+)\.$/, m => N(m[1]) % N(m[2])],
    [/^Find the quotient q when (\d+) = (\d+)·q \+ r/, m => Math.floor(N(m[1]) / N(m[2]))],
    [/^How many positive divisors does (\d+) have\?$/, m => { let c = 0; for (let d = 1; d <= N(m[1]); d++) if (N(m[1]) % d === 0) c++; return c; }],
    [/^What is the smallest prime greater than (\d+)\?$/, m => { let x = N(m[1]) + 1; while (!isPrime(x)) x++; return x; }],
    [/relation a < b on \{1, 2, \.\.\., (\d+)\}\?$/, m => comb(N(m[1]), 2)],
    [/relation a ≤ b on \{1, 2, \.\.\., (\d+)\}\?$/, m => comb(N(m[1]), 2) + N(m[1])],
    [/^How many relations are there on a set with (\d+) elements\?$/, m => 2 ** (N(m[1]) ** 2)],
    [/^How many reflexive relations are there on a set with (\d+) elements\?$/, m => 2 ** (N(m[1]) ** 2 - N(m[1]))],
    [/^How many equivalence classes does congruence mod (\d+) have on ℤ\?$/, m => N(m[1])],
    [/^How many loops does the digraph of "a = b" on \{1, \.\.\., (\d+)\} have\?$/, m => N(m[1])],
    [/^How many elements of \{1, \.\.\., (\d+)\} are in the class \[1\] for congruence mod (\d+)\?$/, m => { let c = 0; for (let x = 1; x <= N(m[1]); x++) if ((x - 1) % N(m[2]) === 0) c++; return c; }],
    [/^How many edges does the complete graph K_(\d+) have\?$/, m => comb(N(m[1]), 2)],
    [/^How many edges does a tree with (\d+) vertices have\?$/, m => N(m[1]) - 1],
    [/^A graph has (\d+) edges\. What is the sum of its degrees\?$/, m => 2 * N(m[1])],
    [/^How many edges does K_(\d+),(\d+) have\?$/, m => N(m[1]) * N(m[2])],
    [/Hamiltonian cycle in a graph with (\d+) vertices use\?$/, m => N(m[1])],
    [/^In K_(\d+), what is the degree of each vertex\?$/, m => N(m[1]) - 1],
    [/^A forest has (\d+) vertices and 3 trees\. How many edges\?$/, m => N(m[1]) - 3],
    [/^How many votes are a majority of (\d+) votes\?$/, m => Math.floor(N(m[1]) / 2) + 1],
    [/^Borda count with (\d+) candidates: how many points does a first-place vote earn\?$/, m => N(m[1])],
    [/^What is the smallest valid quota for weights ([\d, ]+)\?$/, m => Math.floor(m[1].split(',').reduce((a, b) => a + N(b), 0) / 2) + 1],
    [/^Population (\d+), (\d+) seats\. Find the standard divisor\.$/, m => fracStr(N(m[1]), N(m[2]))],
    [/^With (\d+) candidates, how many head-to-head comparisons are there\?$/, m => comb(N(m[1]), 2)],
    [/^How many coalitions \(nonempty\) can (\d+) players form\?$/, m => 2 ** N(m[1]) - 1],
    [/^How many rows does a truth table with (\d+) variables have\?$/, m => 2 ** N(m[1])],
    [/^In a (\d+)-variable truth table, in how many rows is p ∨ q ∨/, m => 2 ** N(m[1]) - 1],
    [/^In a truth table with (\d+) variables, in how many rows is p → q false\?$/, m => 2 ** (N(m[1]) - 2)],
    [/^In a truth table with (\d+) variables, in how many rows is p ↔ q true\?$/, m => 2 ** (N(m[1]) - 1)],
    [/^In a truth table with (\d+) variables, in how many rows is p ∨ q true\?$/, m => 3 * 2 ** (N(m[1]) - 2)],
    [/^In a truth table with (\d+) variables, in how many rows is p ∧ q ∧ r true\?$/, m => 2 ** (N(m[1]) - 3)],
    [/^\|A\| = (\d+), \|B\| = (\d+), \|A ∩ B\| = (\d+)\. Find \|A ∪ B\|\.$/, m => N(m[1]) + N(m[2]) - N(m[3])],
    [/^\|A\| = (\d+), \|B\| = (\d+), \|A ∩ B\| = (\d+)\. Find \|A − B\|\.$/, m => N(m[1]) - N(m[3])],
    [/^\|A\| = (\d+), \|B\| = (\d+), \|A ∩ B\| = (\d+)\. Find \|A ⊕ B\|\.$/, m => N(m[1]) + N(m[2]) - 2 * N(m[3])],
    [/^U has (\d+) elements and \|A\| = (\d+)\. Find \|A′\|\.$/, m => N(m[1]) - N(m[2])],
    [/^Evaluate [PC] = (\d+)x \+ (\d+)y at the corner \((\d+), (\d+)\)\.$/, m => N(m[1]) * N(m[3]) + N(m[2]) * N(m[4])],
    [/^Solve x \+ y = (-?\d+) and x − y = (-?\d+)\./, m => '(' + (N(m[1]) + N(m[2])) / 2 + ', ' + (N(m[1]) - N(m[2])) / 2 + ')'],
    [/^Where does (\d+)x \+ (\d+)y = (\d+) cross the x-axis\? Give x\.$/, m => N(m[3]) / N(m[1])],
    [/^Where does (\d+)x \+ (\d+)y = (\d+) cross the y-axis\? Give y\.$/, m => N(m[3]) / N(m[2])]
  ];
  const t = P.replace(/[‑]/g, '-');
  for (const [re, fn] of R) if ((m = re.exec(t))) return fn(m);
  return null;
}

/* ---------- other engines ---------- */
const fib = n => { let a = 1, b = 1; for (let k = 2; k < n; k++) [a, b] = [b, a + b]; return n <= 2 ? 1 : b; };
function hamilton(pops, seats) {
  const T = pops.reduce((a, b) => a + b, 0), q = pops.map(p => p * seats / T), a = q.map(Math.floor);
  const order = q.map((x, i) => [x - a[i], i]).sort((x, y) => y[0] - x[0]);
  const left = seats - a.reduce((x, y) => x + y, 0);
  for (let k = 0; k < left; k++) a[order[k][1]]++;
  return a;
}
function banzhaf(q, w) {
  const n = w.length, c = Array(n).fill(0);
  for (let m = 1; m < 1 << n; m++) {
    const s = w.reduce((t, x, i) => t + ((m >> i) & 1 ? x : 0), 0);
    if (s < q) continue;
    for (let i = 0; i < n; i++) if ((m >> i) & 1 && s - w[i] < q) c[i]++;
  }
  return c;
}
function lpBest(cons, obj, sense) { // cons: [a,b,c] for a x + b y <= c ; brute-force vertices
  const all = cons.concat([[-1, 0, 0], [0, -1, 0]]), pts = [];
  for (let i = 0; i < all.length; i++) for (let j = i + 1; j < all.length; j++) {
    const [a1, b1, c1] = all[i], [a2, b2, c2] = all[j], det = a1 * b2 - a2 * b1;
    if (!det) continue;
    const x = (c1 * b2 - c2 * b1) / det, y = (a1 * c2 - a2 * c1) / det;
    if (x >= -1e-9 && y >= -1e-9 && cons.every(([a, b, c]) => a * x + b * y <= c + 1e-9)) pts.push([x, y]);
  }
  const vals = pts.map(([x, y]) => obj[0] * x + obj[1] * y);
  return sense === 'max' ? Math.max(...vals) : Math.min(...vals);
}
const parseIneq = s => { // "2x + 3y ≤ 12" or "x ≥ 0"
  const m = /^(.*?)\s*(≤|≥)\s*(-?[\d/]+)$/.exec(s.trim()); if (!m) return null;
  let a = 0, b = 0; const lhs = m[1].replace(/\s+/g, '').replace(/−/g, '-');
  for (const term of lhs.match(/[+-]?[^+-]+/g)) { const mm = /^([+-]?)(\d*(?:\/\d+)?)([xy])$/.exec(term); if (!mm) return null; const k = (mm[1] === '-' ? -1 : 1) * (mm[2] ? eval(mm[2]) : 1); if (mm[3] === 'x') a += k; else b += k; }
  const c = eval(m[3]); return m[2] === '≤' ? [a, b, c] : [-a, -b, -c];
};

/* ---------- main ---------- */
const cells = {};
for (const unit of course.units) {
  const entry = manifest.banks.find(b => b.courseId === 'discrete' && b.unitId === unit.id);
  assert(entry, 'manifest entry missing for ' + unit.id);
  assert(entry.approved === true && entry.teacherUse === true, 'manifest flags for ' + unit.id);
  const bank = JSON.parse(fs.readFileSync(path.join(root, entry.path), 'utf8'));
  const v = W.MK_QUESTION_BANKS.validate(bank); assert(v.ok, unit.id + ': ' + v.errors.join('; '));
  const skills = W.MK_COURSE_CATALOG.getSkillRecords('discrete', unit.id), prompts = new Set();
  const errLv = { cp2: 0, cp1: 0, honors: 0 };
  for (const q of bank.questions) {
    total++;
    const k = q.skillId + '/' + q.level; cells[k] = (cells[k] || 0) + 1;
    const sig = q.prompt + '|' + JSON.stringify(q.diagram || null) + '|' + q.format;
    if (prompts.has(sig)) fail(q, 'duplicate prompt'); prompts.add(sig);
    if (q.format === 'multiple-choice') {
      const c = q.options.filter(o => o.correct); if (c.length !== 1 || c[0].text !== String(q.answer)) fail(q, 'MC key mismatch');
      if (new Set(q.options.map(o => o.text)).size !== q.options.length) fail(q, 'duplicate options');
      if (q.options.length < 4) fail(q, 'fewer than 4 options');
    }
    if (q.format === 'select-all') {
      const c = q.options.filter(o => o.correct).map(o => o.text);
      if (c.length < 2 || c.length === q.options.length || JSON.stringify([...c].sort()) !== JSON.stringify([...q.answer].sort())) fail(q, 'select-all structure');
    }
    if (q.format === 'open-response' && (q.parts || []).length < 4) fail(q, 'open response parts');
    if (q.diagram && q.diagram.type === 'image' && !fs.existsSync(path.join(root, q.diagram.spec.src))) fail(q, 'missing image');
    if (/_error$/.test(fam(q))) { errLv[q.level]++; if (!/^Mistake: /.test(q.solutionSteps[0]) || !/'s work:/.test(q.prompt)) fail(q, 'error-analysis format'); }
    /* ---- independent recomputation ---- */
    try {
      const f = fam(q), P = q.prompt;
      if (['tt_column', 'cond_column'].includes(f) && q.format !== 'open-response') {
        const m = /(?:column (?:for|of) |truth column of )(.+?) (?:as a string|in the standard)/.exec(P) || /Complete the truth table for (.+?)\. Give/.exec(P);
        if (m) { const form = m[1], vars = /\(p, q, r\)/.test(P) ? ['p', 'q', 'r'] : ['p', 'q']; assert.equal(column(form, vars), String(q.answer)); recomputed++; }
      }
      if (['set_op', 'complement_op'].includes(f)) {
        const env = {}; for (const [, n, s] of P.matchAll(/([ABC]) = (\{[^}]*\}|∅)/g)) env[n] = parseSet(s);
        const Um = /Universe U = (\{[^}]*\})/.exec(P), U = Um ? parseSet(Um[1]) : [...new Set([].concat(...Object.values(env)))];
        const e = (/Find (.+?)(?: \(the complement| \(complements|\. Write|\.$)/.exec(P) || [])[1];
        if (e) { assert.equal(fmtSet(setEval(e, env, U)), norm(q.answer).replace(/-/g, '-')); recomputed++; }
      }
      if (f === 'list_count') { const m = /list (-?\d+), -?\d+, \.\.\., (-?\d+)/.exec(P) || /list (\d+), \d+, \d+, \.\.\., (\d+)/.exec(P); if (m) { assert.equal(Number(q.answer), Number(m[2]) - Number(m[1]) + 1); recomputed++; } }
      if (f === 'gcd') { const m = /gcd\((\d+), (\d+)\)/.exec(P); assert.equal(Number(q.answer), gcd(+m[1], +m[2])); recomputed++; }
      if (f === 'lcm') { const m = /lcm\((\d+), (\d+)\)/.exec(P); assert.equal(Number(q.answer), +m[1] * +m[2] / gcd(+m[1], +m[2])); recomputed++; }
      if (f === 'fib_term') { const m = /F_(\d+)/.exec(P.split('find').pop()) || /F_(\d+)\?/.exec(P); assert.equal(Number(q.answer), fib(+m[1])); recomputed++; }
      if (f === 'equally_likely' && /Two fair dice are rolled\. Find P\(sum = (\d+)\)/.test(P)) {
        const s = +/sum = (\d+)/.exec(P)[1]; let n = 0; for (let a = 1; a <= 6; a++) for (let b = 1; b <= 6; b++) if (a + b === s) n++;
        assert.equal(String(q.answer), fracStr(n, 36)); recomputed++;
      }
      if (f === 'hamilton') {
        const pops = [...P.split('seats')[0].matchAll(/[A-Za-z]+ (\d+)/g)].map(m => +m[1]), seats = +/; (\d+) seats/.exec(P)[1];
        assert.equal(String(q.answer), hamilton(pops, seats).join(', ')); recomputed++;
      }
      if (f === 'banzhaf' && q.format !== 'open-response') {
        const m = /\[(\d+): ([\d, ]+)\]/.exec(P), w = m[2].split(',').map(Number), c = banzhaf(+m[1], w), T = c.reduce((a, b) => a + b, 0);
        assert.equal(String(q.answer), fracStr(c[0], T)); recomputed++;
      }
      if (f === 'optimize' && /subject to/.test(P)) {
        const sense = /^Maximize/.test(P) ? 'max' : 'min', om = /P = (\d*)x \+ (\d*)y/.exec(P), obj = [om[1] ? +om[1] : 1, om[2] ? +om[2] : 1];
        const cons = P.split('subject to ')[1].replace(/\..*$/s, '').split('; ').map(parseIneq).filter(c => c && !(c[2] === 0 && (c[0] === -1 && c[1] === 0 || c[0] === 0 && c[1] === -1)));
        const best = lpBest(cons, obj, sense), ans = /P = (-?[\d/]+)\s*$/.exec(String(q.answer)) || [null, String(q.answer)];
        assert(Math.abs(eval(ans[1]) - best) < 1e-9, 'LP ' + best + ' vs ' + q.answer); recomputed++;
      }
      if (f === 'quick_check') { const v = quickAnswer(P); if (v !== null) { assert.equal(String(q.answer), String(v), P); recomputed++; } else fail(q, 'quick check not recomputed: ' + P); }
    } catch (e) { fail(q, 'recompute: ' + e.message.slice(0, 160)); }
  }
  for (const s of skills) {
    const n = ['cp2', 'cp1', 'honors'].map(l => cells[s.id + '/' + l] || 0);
    if (n.reduce((a, b) => a + b, 0) < 30 || Math.min(...n) < 8) fails.push('thin skill ' + s.id + ' ' + n);
  }
  if (Object.values(errLv).some(n => n < 4) || Object.values(errLv).reduce((a, b) => a + b, 0) < 12) fails.push('error analysis coverage ' + unit.id);
}
if (fails.length) { console.error(fails.slice(0, 60).join('\n')); console.error(fails.length + ' problems'); process.exit(1); }
console.log('PASS ' + total + ' Discrete Math questions in 10 banks; every skill >= 30 (>= 8 per level); error analysis >= 12 per unit; ' + recomputed + ' answers independently recomputed');
