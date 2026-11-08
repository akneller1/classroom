/* Discrete Math Unit 5 cheat sheet (Set Theory). Set results are recomputed by the checks. */
const D = require('../dmfigs.cjs');
const S = a => '[' + [...new Set(a)].sort((x, y) => x - y).join(',') + ']';
const U = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], A = [1, 2, 3, 4, 5, 6], B = [4, 5, 6, 7, 8];
module.exports = {
  name: 'discrete-set-theory', course: 'Discrete Math', unitNo: 5, unitName: 'Set Theory',
  focus: 'set equality, the empty set, union, intersection, difference, complements and Venn diagrams',
  morefocus: 'power sets, element-argument proofs, set identities and disproving set statements',
  front: [
    { title: 'Operations', color: 'purple', kind: 'table', head: ['Name', 'Notation', 'Elements'], rows: [
      ['union', '⟨A \\cup B⟩', 'in ⟨A⟩ or ⟨B⟩ (or both)'], ['intersection', '⟨A \\cap B⟩', 'in both'], ['difference', '⟨A - B⟩', 'in ⟨A⟩, not in ⟨B⟩'],
      ['complement', '⟨A^{c}⟩ or ⟨A\'⟩', 'in the universe ⟨U⟩, not in ⟨A⟩'], ['disjoint', '⟨A \\cap B = \\varnothing⟩', 'no common elements']],
      after: 'Always state the universe before taking a complement: in ⟨U = \\mathbb{Z}⟩ the complement of the evens is the odds.' },
    { title: 'Worked Example', color: 'blue', kind: 'example', text: '⟨U = \\{1, \\dots, 10\\}⟩, ⟨A = \\{1, \\dots, 6\\}⟩, ⟨B = \\{4, \\dots, 8\\}⟩.',
      example: 'Find each set.', steps: [['⟨A \\cap B⟩:', '⟨\\{4, 5, 6\\}⟩'], ['⟨A - B⟩:', '⟨\\{1, 2, 3\\}⟩'], ['⟨(A \\cup B)\'⟩:', '⟨\\{9, 10\\}⟩']], answer: '⟨A\' \\cap B\' = \\{9, 10\\}⟩ too',
      check: [{ true: `"${S(A.filter(x => B.includes(x)))}" === "[4,5,6]"` }, { true: `"${S(A.filter(x => !B.includes(x)))}" === "[1,2,3]"` }, { true: `"${S(U.filter(x => !A.includes(x) && !B.includes(x)))}" === "[9,10]"` }] },
    { title: 'Venn Diagram Regions', color: 'green', kind: 'html', figFirst: true,
      fig: D.venn({ id: 'v1', sets: ['A', 'B'], labels: { A: '1, 2, 3', AB: '4, 5, 6', B: '7, 8', '': '9, 10' }, inches: 2.2 }),
      html: 'The diagram shows the example: each element goes in exactly one region. ⟨|A \\cup B| = |A| + |B| - |A \\cap B| = 6 + 5 - 3 = 8⟩.',
      check: { num: '6+5-3', is: 8 } },
    { title: 'Shading Practice', color: 'orange', kind: 'html',
      html: '<div style="display:flex;justify-content:space-around;text-align:center;font-size:8.5pt"><div>' + D.venn({ id: 'v2', sets: ['A', 'B'], shade: ['A'], inches: 1.05 }) + '<br>⟨A - B⟩</div><div>' +
        D.venn({ id: 'v3', sets: ['A', 'B'], shade: ['A', 'B'], inches: 1.05 }) + '<br>⟨A \\oplus B⟩</div><div>' + D.venn({ id: 'v4', sets: ['A', 'B'], shade: [''], inches: 1.05 }) + '<br>⟨(A \\cup B)\'⟩</div></div>' +
        '<div style="margin-top:3px">Three sets: ⟨A \\cap (B \\cup C)⟩ shades the regions of ⟨A⟩ that also lie in ⟨B⟩ or ⟨C⟩.</div>' },
    { title: 'Inclusion-Exclusion', color: 'pink', kind: 'example', text: '⟨|A \\cup B \\cup C| = |A| + |B| + |C| - |A \\cap B| - |A \\cap C| - |B \\cap C| + |A \\cap B \\cap C|⟩',
      example: 'How many integers from 1 to 100 are divisible by 3 or 5?', steps: [['Count:', '⟨33 + 20 - 6⟩'], ['Overlap:', 'multiples of 15: 6']], answer: '47',
      check: { num: '[...Array(100).keys()].map(i=>i+1).filter(n => n%3===0 || n%5===0).length', is: 47 } },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['List each element once.', 'A − B only contains elements of A.', 'Endpoints matter for intervals: ⟨[1, 4] - (2, 6) = [1, 2]⟩.'],
      bad: [['⟨(A \\cap B)\' = A\' \\cap B\'⟩', 'it is ⟨A\' \\cup B\'⟩'], ['Complement with no universe', 'state ⟨U⟩'], ['Counting the overlap twice', 'subtract ⟨|A \\cap B|⟩']] }
  ],
  back: [
    { title: 'Power Sets', color: 'purple', kind: 'example', text: '⟨\\mathcal{P}(A)⟩ is the set of all subsets of ⟨A⟩; ⟨|\\mathcal{P}(A)| = 2^{|A|}⟩.',
      example: '⟨\\mathcal{P}(\\{a, b\\})⟩', steps: [['Subsets:', '⟨\\varnothing, \\{a\\}, \\{b\\}, \\{a, b\\}⟩'], ['Note:', '⟨\\{a\\} \\in \\mathcal{P}(A)⟩ but ⟨a \\notin \\mathcal{P}(A)⟩']], answer: '4 elements',
      check: { num: '2**2', is: 4 } },
    { title: 'Proving a Subset', color: 'blue', kind: 'example', text: 'To show ⟨X \\subseteq Y⟩: let ⟨x \\in X⟩ be arbitrary and show ⟨x \\in Y⟩.',
      example: 'Prove ⟨A - B \\subseteq A \\cap B\'⟩.', steps: [['Let:', '⟨x \\in A - B⟩'], ['Then:', '⟨x \\in A⟩ and ⟨x \\notin B⟩'], ['So:', '⟨x \\in A⟩ and ⟨x \\in B\'⟩']], answer: '⟨x \\in A \\cap B\'⟩' },
    { title: 'Set Identities', color: 'green', kind: 'table', plain: true, head: ['Law', 'Identity'], rows: [
      ['commutative', '⟨A \\cup B = B \\cup A⟩'], ['distributive', '⟨A \\cap (B \\cup C) = (A \\cap B) \\cup (A \\cap C)⟩'], ['De Morgan', '⟨(A \\cup B)\' = A\' \\cap B\'⟩'],
      ['absorption', '⟨A \\cup (A \\cap B) = A⟩'], ['complement', '⟨A \\cup A\' = U,\\ A \\cap A\' = \\varnothing⟩'], ['set difference', '⟨A - B = A \\cap B\'⟩']],
      after: 'Prove an identity by showing both inclusions (⊆ and ⊇) or by a chain of laws.' },
    { title: 'Proving Set Equality', color: 'orange', kind: 'example', text: 'Chain of laws, naming each one.',
      example: 'Show ⟨A - (A - B) = A \\cap B⟩.', steps: [['Difference law:', '⟨A \\cap (A \\cap B\')\'⟩'], ['De Morgan:', '⟨A \\cap (A\' \\cup B)⟩'], ['Distribute:', '⟨(A \\cap A\') \\cup (A \\cap B) = \\varnothing \\cup (A \\cap B)⟩']], answer: '⟨A \\cap B⟩',
      check: { true: '(() => { const U=[0,1,2,3], A=[1,3], B=[2,3]; const d=(X,Y)=>X.filter(x=>!Y.includes(x)); return JSON.stringify(d(A,d(A,B))) === JSON.stringify(A.filter(x=>B.includes(x))); })()' } },
    { title: 'Disproving with a Counterexample', color: 'pink', kind: 'table', plain: true, head: ['False claim', 'Counterexample'], rows: [
      ['⟨A - B = B - A⟩', '⟨A = \\{1\\},\\ B = \\varnothing⟩'], ['⟨A \\cup B = A⟩', '⟨A = \\varnothing,\\ B = \\{1\\}⟩'], ['⟨(A \\cup B) - B = A⟩', '⟨A = B = \\{1\\}⟩'],
      ['⟨\\mathcal{P}(A \\cup B) = \\mathcal{P}(A) \\cup \\mathcal{P}(B)⟩', '⟨A = \\{1\\},\\ B = \\{2\\}⟩: ⟨\\{1, 2\\}⟩ is missing']],
      after: 'An example where the claim works proves nothing; you need specific sets where it <b>fails</b>.' },
    { title: 'Challenge', color: 'teal', kind: 'html',
      html: 'True or false for all sets: (1) ⟨A \\subseteq B \\Rightarrow \\mathcal{P}(A) \\subseteq \\mathcal{P}(B)⟩ <b>true</b>: if ⟨X \\subseteq A⟩ then ⟨X \\subseteq B⟩. (2) ⟨\\mathcal{P}(A - B) = \\mathcal{P}(A) - \\mathcal{P}(B)⟩ <b>false for every A, B</b>: ⟨\\varnothing⟩ is on the left but never on the right. (3) How many subsets of ⟨\\{1, \\dots, 7\\}⟩ have no two consecutive numbers? ⟨F_9 = 34⟩.',
      check: { num: '[...Array(128).keys()].filter(m => (m & (m >> 1)) === 0).length', is: 34 } }
  ]
};
