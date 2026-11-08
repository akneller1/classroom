// Correctness checks for the Discrete Math tools: drives each page with known inputs and compares what it displays with
// values computed independently here (or taken from the cheat sheets and question bank). Also checks phone-width layout
// (no sideways scrolling), that every control has an accessible name, and keyboard use of draggable/selectable SVG items.
// Usage (repository root): node tools/interactive-math-discrete/tests/correctness.cjs
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../../..');
const T = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' };
const serve = () => new Promise(r => { const s = http.createServer((q, res) => { const u = decodeURIComponent(q.url.split('?')[0]); fs.readFile(path.join(ROOT, u), (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { 'Content-Type': T[path.extname(u)] || 'application/octet-stream' }); res.end(d); }); }); s.listen(0, () => r(s)); });
let pass = 0, fail = 0;
const ok = (c, msg) => { if (c) pass++; else { fail++; console.log('FAIL', msg); } };
const gcd = (a, b) => b ? gcd(b, a % b) : a;
const C = (n, r) => { let x = 1; for (let i = 1; i <= r; i++) x = x * (n - r + i) / i; return Math.round(x); };
const Pn = (n, r) => { let x = 1; for (let i = 0; i < r; i++) x *= n - i; return x; };
(async () => {
  const srv = await serve(), port = srv.address().port, b = await chromium.launch();
  const open = async (slug, w = 1280) => { const p = await b.newPage({ viewport: { width: w, height: 900 } }); p.errs = []; p.on('pageerror', e => p.errs.push(e.message)); await p.goto(`http://localhost:${port}/artifacts/${slug}/index.html`); await p.waitForTimeout(150); return p; };
  const set = (p, id, v, ev = 'input') => p.evaluate(([id, v, ev]) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event(ev)); if (ev === 'input') e.dispatchEvent(new Event('change')); }, [id, v, ev]).then(() => p.waitForTimeout(40));
  const click = (p, t, sel = 'button') => p.evaluate(([t, sel]) => { const all = [...document.querySelectorAll(sel)].filter(b => b.offsetParent !== null); const x = all.find(b => b.textContent.trim() === t) || all.find(b => b.textContent.trim().startsWith(t)); if (!x) throw new Error('no ' + t); x.click(); }, [t, sel]).then(() => p.waitForTimeout(40));
  const text = (p, sel) => p.evaluate(s => [...document.querySelectorAll(s)].map(e => e.textContent).join(' | '), sel);

  /* truth tables */
  let p = await open('discrete-truth-table-lab');
  const eqCases = [['p -> q', '~p v q', true], ['p -> q', 'q -> p', false], ['~(p & q)', '~p | ~q', true], ['p -> (q -> r)', '(p & q) -> r', true], ['(p -> q) -> r', 'p -> (q -> r)', false], ['p xor q', '(p v q) & ~(p & q)', true], ['p <-> q', '(p -> q) & (q -> p)', true]];
  for (const [a, c, e] of eqCases) { await set(p, 'tt-s1', a); await set(p, 'tt-s2', c); const f = await text(p, '.lp-feedback'); ok(f.includes(e ? 'Equivalent' : 'Not equivalent'), `truth table ${a} vs ${c}`); }
  await set(p, 'tt-s1', 'p -> q -> r'); await set(p, 'tt-s2', ''); const rows = await p.evaluate(() => document.querySelectorAll('.tt tbody tr').length); ok(rows === 8, 'three variables give 8 rows');
  await set(p, 'tt-s1', 'p & ~p'); ok((await text(p, '.tt-sum')).includes('contradiction'), 'contradiction detected');
  await click(p, 'Test an argument', 'button.chip');
  for (const [pr, co, v] of [['p -> q; p', 'q', true], ['p -> q; ~p', '~q', false], ['p v q; ~p', 'q', true], ['p -> q; q -> r', 'p -> r', true], ['p; ~p', 'q', true]]) { await set(p, 'tt-prem', pr); await set(p, 'tt-concl', co); const f = await text(p, '.lp-feedback'); ok(f.includes(v ? 'Valid' : 'Invalid'), `argument ${pr} ∴ ${co}`); }
  await set(p, 'tt-prem', 'p ->'); ok((await text(p, '#tt-prem-err')).length > 0, 'parse error is reported');
  ok(!p.errs.length, 'truth table: no page errors ' + p.errs); await p.close();

  /* Euclid */
  p = await open('discrete-euclid-explorer');
  for (const [a, c] of [[252, 198], [89, 55], [1, 999], [600, 600], [17, 391], [462, 987]]) {
    await set(p, 'ni-a', a, 'change'); await set(p, 'ni-b', c, 'change'); await click(p, 'Show all steps');
    const t = await text(p, '.eu-big'), g = gcd(a, c); ok(t.includes(`gcd(${a}, ${c}) = ${g}`) && t.includes(`lcm(${a}, ${c}) = ${a * c / g}`), `gcd/lcm ${a}, ${c}: ${t}`);
    const lc = (await text(p, '.eu-fac')).match(/Linear combination: (\d+) = \(?(−?\d+)\)? · (\d+) \+ \(?(−?\d+)\)? · (\d+)/);
    ok(lc && +lc[1] === g && (+lc[2].replace('−', '-')) * a + (+lc[4].replace('−', '-')) * c === g, `Bezout ${a}, ${c}`);
  }
  await click(p, 'Quotient and remainder', 'button.tab');
  for (const [n, d] of [[-23, 7], [23, 7], [-14, 7], [0, 5], [-1, 20]]) { await set(p, 'ni-n', n, 'change'); await set(p, 'sl-d', d); const t = await text(p, '.eu-big'), r = ((n % d) + d) % d; ok(t.includes('+ ' + r + ' ') && t.includes('0 ≤ ' + r), `remainder ${n} mod ${d}: ${t}`); }
  ok(!p.errs.length, 'euclid: no page errors'); await p.close();

  /* recursion */
  p = await open('discrete-recursion-explorer');
  await click(p, 'Fibonacci', 'button.chip');
  let cells = await p.evaluate(() => [...document.querySelectorAll('.stage tbody tr')].map(r => [...r.children].map(c => c.textContent)));
  ok(cells[11][1] === '144' && cells[9][2] === '143', 'Fibonacci a12 = 144, S10 = 143');
  await click(p, 'Tower of Hanoi', 'button.chip'); await set(p, 'rc-guess', '2^n-1');
  ok((await text(p, '.lp-feedback')).includes('matches all 15'), 'Hanoi closed form matches');
  await set(p, 'rc-guess', '2^n'); ok((await text(p, '.lp-feedback')).includes('first disagrees at n = 1'), 'wrong guess caught at n = 1');
  await set(p, 'rc-guess', '(n+1)(n+2)/2-1'); ok((await text(p, '.lp-feedback')).includes('disagrees'), 'implicit multiplication parses');
  await set(p, 'ni-c', 0.5, 'change'); await set(p, 'ni-d', 3, 'change'); await set(p, 'ni-a1', 2, 'change'); await click(p, 'Show a closed form');
  ok((await text(p, '.rc-rule')).includes('fixed point L = d/(1 − c) = 6'), 'fixed point 3/(1 − 0.5) = 6');
  ok(!p.errs.length, 'recursion: no page errors'); await p.close();

  /* Venn */
  p = await open('discrete-venn-explorer');
  const U = [...Array(20)].map((_, i) => i + 1), A = U.filter(x => x % 2 === 0), B = U.filter(x => x % 3 === 0), Cp = [2, 3, 5, 7, 11, 13, 17, 19];
  const has = (S, x) => S.includes(x), ros = S => S.length ? '{' + S.join(', ') + '}' : '∅';
  await click(p, 'A, B and C', 'button.chip');
  const vcases = [["(A ∪ B)'", U.filter(x => !has(A, x) && !has(B, x))], ['A ∩ B ∩ C', []], ['A − (B ∪ C)', A.filter(x => !has(B, x) && !has(Cp, x))], ["C ⊕ A", U.filter(x => has(A, x) !== has(Cp, x))], ["(A ∩ C)′ ∩ B", B.filter(x => !(has(A, x) && has(Cp, x)))], ['A ∪ B ∩ C', U.filter(x => has(A, x) || (has(B, x) && has(Cp, x)))], ["U − C'", Cp]];
  for (const [e, S] of vcases) { await set(p, 'vn-e1', e); const t = await text(p, '.vn-res'); ok(t.includes('Expression 1 = ' + ros(S) + ' '), `Venn ${e}: ${t.split('Expression 2')[0]}`); }
  ok(!p.errs.length, 'venn: no page errors'); await p.close();

  /* relations */
  p = await open('discrete-relation-explorer');
  const props = async () => (await text(p, '.rl-props div'));
  await set(p, 'sl-size', 5); await click(p, 'a divides b', 'button.chip'); let pr = await props();
  ok(/Reflexive: yes/.test(pr) && /Symmetric: no/.test(pr) && /Antisymmetric: yes/.test(pr) && /Transitive: yes/.test(pr), 'divides is a partial order: ' + pr);
  await click(p, 'a ≡ b (mod 3)', 'button.chip'); ok((await text(p, '.lp-feedback')).includes('[1] = {1, 4}, [2] = {2, 5}, [3] = {3}'), 'mod 3 classes on {1..5}');
  await click(p, 'a < b', 'button.chip'); pr = await props(); ok(/Reflexive: no/.test(pr) && /Transitive: yes/.test(pr) && /Antisymmetric: yes/.test(pr), '< is irreflexive-type, transitive');
  await click(p, 'Clear'); for (const c of ['1, 2', '2, 1']) { await p.evaluate(c => document.querySelector(`[aria-label="pair (${c})"]`).click(), c); await p.waitForTimeout(40); } pr = await props(); ok(/Transitive: no, \(1, 2\) and \(2, 1\) ∈ R but \(1, 1\) ∉ R/.test(pr), 'symmetric pair without loops is not transitive: ' + pr);
  await p.focus('[aria-label^="vertex 3"]'); await p.keyboard.press('Enter'); await p.waitForTimeout(60); await p.focus('[aria-label^="vertex 3"]'); await p.keyboard.press('Enter'); await p.waitForTimeout(60);
  ok((await text(p, '.rl-set')).includes('(3, 3)'), 'keyboard: Enter twice on a vertex adds a loop');
  ok(!p.errs.length, 'relation: no page errors'); await p.close();

  /* counting */
  p = await open('discrete-counting-explorer');
  for (const [ord, rep, f] of [['Yes (arrangements)', 'Yes (with replacement)', (n, r) => n ** r], ['Yes (arrangements)', 'No', Pn], ['No (selections)', 'No', C], ['No (selections)', 'Yes (with replacement)', (n, r) => C(n + r - 1, r)]]) {
    await click(p, ord, 'button.chip'); await click(p, rep, 'button.chip');
    for (const [n, r] of [[4, 2], [5, 3], [7, 4], [3, 3]]) { await set(p, 'sl-n', n); await set(p, 'sl-r', r); const t = await text(p, '.ct-big'), want = f(n, r); const listed = await p.evaluate(() => document.querySelectorAll('.ct-list > span, .ct-list > .grp').length);
      ok(t.replace(/,/g, '').endsWith('= ' + want), `${ord}/${rep} n=${n} r=${r}: ${t}`); ok(listed === Math.min(want, 600), `listed outcomes ${listed} vs ${want}`); }
  }
  await click(p, 'Yes (arrangements)', 'button.chip'); await set(p, 'sl-n', 6); await set(p, 'sl-r', 2); await click(p, 'Contains A', 'button.chip');
  ok((await text(p, '.lp-feedback')).includes('11/36'), 'P(at least one A) = 11/36');
  await click(p, 'No (selections)', 'button.chip'); ok((await text(p, '.lp-feedback')).includes('not equally likely') && (await text(p, '.lp-feedback')).includes('11/36'), 'multiset warning gives the ordered probability 11/36');
  ok(!p.errs.length, 'counting: no page errors'); await p.close();

  /* graphs */
  p = await open('discrete-graph-lab');
  const facts = async () => text(p, '.gl-facts div');
  await click(p, 'Königsberg', 'button.chip'); ok((await facts()).includes('No Euler trail or circuit: 4 vertices have odd degree'), 'Königsberg has no Euler trail');
  ok((await text(p, '.gl-mode')).includes('A 3, B 5, C 3, D 3. Sum = 14 = 2 × 7'), 'Königsberg degrees');
  await click(p, 'Petersen', 'button.chip'); let fx = await facts(); ok(fx.includes('No Hamiltonian cycle') && fx.includes('χ = 3'), 'Petersen: no Hamiltonian cycle, χ = 3');
  await click(p, 'K₃,₃', 'button.chip'); fx = await facts(); ok(fx.includes('χ = 2 (bipartite)') && fx.includes('Hamiltonian cycle:'), 'K3,3 bipartite and Hamiltonian');
  await click(p, 'K₅', 'button.chip'); fx = await facts(); ok(fx.includes('Euler circuit') && fx.includes('χ = 5'), 'K5 Euler circuit, χ = 5');
  await click(p, 'Bowtie', 'button.chip'); const route = (await facts()).match(/Route: ([A-L–]+)/)[1].split('–');
  ok(route.length === 7 && route[0] === route[6], 'bowtie Euler circuit uses all 6 edges and closes');
  await click(p, 'Road network (weighted)', 'button.chip'); await click(p, 'Kruskal: finish'); const kf = await text(p, '.lp-feedback');
  ok(kf.includes('total weight 15') && kf.includes('skip BC (5)'), 'Kruskal on the cheat-sheet network: weight 15, skip BC: ' + kf);
  await click(p, 'Move a vertex', 'button.chip'); const before = await p.evaluate(() => document.querySelector('[data-v="0"] circle').getAttribute('cx'));
  await p.focus('[data-v="0"]'); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(60);
  const after = await p.evaluate(() => document.querySelector('[data-v="0"] circle').getAttribute('cx')); ok(+after === +before + 10, 'keyboard arrow moves a vertex');
  ok(!p.errs.length, 'graph: no page errors'); await p.close();

  /* voting */
  p = await open('discrete-voting-explorer');
  await click(p, 'Add a column');
  const sched = [[14, 'ABC'], [10, 'CBA'], [8, 'BCA'], [3, 'CAB']];
  for (let i = 0; i < 4; i++) { await set(p, 'vt-n' + i, sched[i][0], 'change'); await set(p, 'vt-r' + i, sched[i][1], 'change'); }
  const vr = await text(p, '.vt-res div');
  ok(/Plurality: A 14, B 8, C 13 → A/.test(vr) && /Borda .*A 66, B 75, C 69 → B/.test(vr) && /→ C/.test(vr.split('elimination')[1]) && /Pairwise comparisons: A 0, B 2, C 1 points → B/.test(vr), 'cheat-sheet schedule winners: ' + vr);
  await click(p, 'Weighted voting', 'button.tab'); await set(p, 'ni-w1', 4, 'change'); await set(p, 'ni-w2', 3, 'change'); await set(p, 'ni-w3', 2, 'change'); await set(p, 'sl-quota', 6);
  const wt = await p.evaluate(() => [...document.querySelectorAll('.stage tbody tr')].map(r => [...r.children].map(c => c.textContent)));
  ok(wt.map(r => r[2]).join() === '3,1,1' && wt[0][6] === 'veto power' && wt[0][5].startsWith('2/3'), 'Banzhaf [6: 4, 3, 2] = 3, 1, 1; P1 veto; Shapley–Shubik P1 = 2/3');
  await click(p, 'Apportionment', 'button.tab');
  const app = async () => p.evaluate(() => [...document.querySelectorAll('.stage tbody tr')].map(r => r.children[5].textContent));
  ok((await app()).slice(0, 3).join() === '5,3,2', 'Hamilton 450, 330, 220 → 5, 3, 2');
  await click(p, '4', 'button.chip'); await set(p, 'ni-pop1', 5100, 'change'); await set(p, 'ni-pop2', 1600, 'change'); await set(p, 'ni-pop3', 1500, 'change'); await set(p, 'ni-pop4', 1200, 'change'); await set(p, 'ni-seats', 20, 'change');
  await click(p, 'Jefferson', 'button.chip'); await click(p, 'Find a divisor that works');
  let ja = await app(); ok(ja.slice(0, 4).join() === '12,3,3,2' && ja[4] === '20' && (await text(p, '.lp-feedback')).includes('violates the quota rule'), 'Jefferson quota violation example: ' + ja);
  await click(p, 'Webster', 'button.chip'); await click(p, 'Find a divisor that works'); ja = await app(); ok(ja[4] === '20', 'Webster divisor found: ' + ja);
  await click(p, 'Adams', 'button.chip'); await click(p, 'Find a divisor that works'); ja = await app(); ok(ja[4] === '20', 'Adams divisor found: ' + ja);
  ok(!p.errs.length, 'voting: no page errors'); await p.close();

  /* phone width, names */
  for (const slug of require('../manifest.json').tools.map(t => t.slug)) {
    p = await open(slug, 390);
    const r = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, unnamed: [...document.querySelectorAll('button, input, select, [tabindex]')].filter(e => { const n = e.getAttribute('aria-label') || e.textContent.trim() || (e.id && document.querySelector(`label[for="${e.id}"]`)) || e.closest('label'); return !n; }).map(e => e.outerHTML.slice(0, 80)) }));
    ok(r.sw <= 392, `${slug}: no sideways scroll at 390px (scrollWidth ${r.sw})`);
    ok(!r.unnamed.length, `${slug}: every control has a name ${r.unnamed.join(' ')}`);
    await p.close();
  }
  await b.close(); srv.close();
  console.log(`${pass} checks passed, ${fail} failed`); process.exit(fail ? 1 : 0);
})();
