// Walkthrough steps for the Discrete Math tools: step i must complete "Try this" challenge i (steps run in order on one page).
module.exports = {
  'discrete-truth-table-lab': [
    async (p, H) => { await H.btn(p, 'Converse'); await H.btn(p, 'Contrapositive'); },
    async (p, H) => { await H.type(p, 'tt-s1', 'p v ~p'); },
    async (p, H) => { await H.type(p, 'tt-s1', '~(p ∧ q)'); await H.type(p, 'tt-s2', '~p ∨ ~q'); },
    async (p, H) => { await H.type(p, 'tt-s1', 'p <-> q'); await H.type(p, 'tt-s2', '(p ∧ q) ∨ (~p ∧ ~q)'); },
    async (p, H) => { await H.type(p, 'tt-s1', '~(p -> q)'); await H.type(p, 'tt-s2', 'p & ~q'); },
    async (p, H) => { await H.chip(p, 'Test an argument'); await H.type(p, 'tt-prem', 'p -> q; ~q'); await H.type(p, 'tt-concl', '~p'); await H.type(p, 'tt-prem', 'p -> q; q'); await H.type(p, 'tt-concl', 'p'); }
  ],
  'discrete-euclid-explorer': [
    async (p, H) => { await H.num(p, 'a', 91); await H.num(p, 'b', 120); await H.btn(p, 'Show all steps'); },
    async (p, H) => { await H.num(p, 'a', 89); await H.num(p, 'b', 55); await H.btn(p, 'Next step'); await H.btn(p, 'Show all steps'); },
    async (p, H) => { await H.num(p, 'a', 72); await H.num(p, 'b', 60); await H.btn(p, 'Show all steps'); },
    async (p, H) => { await H.num(p, 'a', 120); await H.num(p, 'b', 40); await H.btn(p, 'Show all steps'); },
    async (p, H) => { await H.tab(p, 'Quotient and remainder'); await H.num(p, 'n', -30); }
  ],
  'discrete-recursion-explorer': [
    async (p, H) => { await H.chip(p, 'Arithmetic'); await H.num(p, 'a1', 5); await H.num(p, 'd', 3); },
    async (p, H) => { await H.chip(p, 'Tower of Hanoi'); await H.type(p, 'rc-guess', '2^n - 1'); },
    async (p, H) => { await H.num(p, 'c', -2); await H.num(p, 'd', 0); await H.num(p, 'a1', 1); },
    async (p, H) => { await H.num(p, 'c', 3); await H.num(p, 'd', -10); await H.num(p, 'a1', 5); },
    async (p, H) => { await H.chip(p, 'Fibonacci'); },
    async (p, H) => { await H.chip(p, 'Geometric'); await H.type(p, 'rc-guess', '3*2^(n-1)'); }
  ],
  'discrete-venn-explorer': [
    async (p, H) => { await H.btn(p, 'in A, not B'); await H.type(p, 'vn-e1', "A ∩ B'"); },
    async (p, H) => { await H.type(p, 'vn-e1', "(A ∪ B)'"); await H.type(p, 'vn-e2', "A' ∩ B'"); },
    async (p, H) => { await H.chip(p, 'A, B and C'); await H.btn(p, 'in A, not B or C'); await H.btn(p, 'in B, not A or C'); await H.btn(p, 'in C, not A or B'); },
    async (p, H) => { await H.type(p, 'vn-e1', '(A ∪ B) − (A ∩ B)'); },
    async (p, H) => { await H.type(p, 'vn-e1', 'A − (B ∪ C)'); await H.type(p, 'vn-e2', '(A − B) ∩ (A − C)'); },
    async (p, H) => { await H.type(p, 'vn-e1', 'A ∩ B'); }
  ],
  'discrete-relation-explorer': [
    async (p, H) => { await H.chip(p, 'a = b'); for (const c of ['1, 2', '2, 1', '2, 3', '3, 2']) await H.click(p, `[aria-label="pair (${c})"]`); },
    async (p, H) => { await H.btn(p, 'Clear'); for (const c of ['1, 1', '1, 2', '2, 1', '2, 2']) await H.click(p, `[aria-label="pair (${c})"]`); },
    async (p, H) => { await H.slider(p, 'size', 5); await H.chip(p, 'same parity'); },
    async (p, H) => { await H.btn(p, 'Clear'); await H.click(p, '[aria-label="pair (1, 1)"]'); },
    async (p, H) => { await H.btn(p, 'Clear'); for (const c of ['1, 2', '2, 3', '3, 4']) await H.click(p, `[aria-label="pair (${c})"]`); await H.btn(p, 'Transitive closure'); },
    async (p, H) => { await H.chip(p, 'a divides b'); }
  ],
  'discrete-counting-explorer': [
    async (p, H) => { await H.slider(p, 'n', 5); await H.slider(p, 'r', 3); },
    async (p, H) => { await H.chip(p, 'No (selections)'); await H.slider(p, 'r', 2); await H.chip(p, 'Group the r! orderings'); },
    async (p, H) => { await H.slider(p, 'r', 3); },
    async (p, H) => { await H.chip(p, 'Yes (arrangements)'); await H.slider(p, 'n', 4); await H.slider(p, 'r', 4); await H.chip(p, 'Starts with A'); },
    async (p, H) => { await H.chip(p, 'No (selections)'); await H.chip(p, 'Yes (with replacement)'); await H.slider(p, 'r', 3); },
    async (p, H) => { await H.chip(p, 'Yes (arrangements)'); await H.slider(p, 'n', 6); await H.slider(p, 'r', 2); await H.chip(p, 'Contains A'); }
  ],
  'discrete-graph-lab': [
    async (p, H) => { await H.chip(p, 'Königsberg'); await H.sel(p, 'gl-from', '0'); await H.sel(p, 'gl-to', '2'); await H.btn(p, 'Add edge'); },
    async (p, H) => { await H.chip(p, 'Bowtie'); },
    async (p, H) => { await H.chip(p, 'K₄'); },
    async (p, H) => { await H.chip(p, 'C₅'); },
    async (p, H) => { await H.chip(p, 'Tree'); await H.btn(p, 'Remove last edge'); await H.sel(p, 'gl-from', '2'); await H.sel(p, 'gl-to', '6'); await H.btn(p, 'Add edge'); },
    async (p, H) => { await H.chip(p, 'Road network (weighted)'); await H.btn(p, 'Kruskal: finish'); }
  ],
  'discrete-voting-explorer': [
    async (p, H) => { await H.btn(p, 'Remove last column'); await H.num2(p, 'vt-n0', 5); await H.sel(p, 'vt-r0', 'ABC'); await H.num2(p, 'vt-n1', 4); await H.sel(p, 'vt-r1', 'BCA'); },
    async (p, H) => { await H.btn(p, 'Add a column'); await H.num2(p, 'vt-n0', 4); await H.num2(p, 'vt-n1', 3); await H.num2(p, 'vt-n2', 2); await H.sel(p, 'vt-r2', 'CBA'); },
    async (p, H) => { await H.num2(p, 'vt-n0', 3); await H.num2(p, 'vt-n2', 3); await H.sel(p, 'vt-r2', 'CAB'); },
    async (p, H) => { await H.btn(p, 'Remove last column'); await H.num2(p, 'vt-n0', 5); await H.num2(p, 'vt-n1', 4); },
    async (p, H) => { await H.tab(p, 'Weighted voting'); await H.num(p, 'w1', 4); await H.num(p, 'w2', 2); await H.num(p, 'w3', 1); await H.slider(p, 'quota', 6); },
    async (p, H) => { await H.slider(p, 'quota', 6); },
    async (p, H) => { await H.tab(p, 'Apportionment'); await H.chip(p, 'Jefferson'); await H.btn(p, 'Find a divisor that works'); },
    async (p, H) => { await H.chip(p, 'Hamilton'); await H.num(p, 'pop1', 130); await H.num(p, 'pop2', 690); await H.num(p, 'pop3', 410); await H.num(p, 'seats', 13); }
  ]
};
