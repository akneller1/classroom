/* Discrete Math Unit 6 cheat sheet (Properties of Relations). Properties are recomputed by the checks. */
const D = require('../dmfigs.cjs');
const R = [[1, 1], [2, 2], [3, 3], [1, 2], [2, 1]];
const has = (S, a, b) => S.some(p => p[0] === a && p[1] === b);
const refl = (S, A) => A.every(a => has(S, a, a)), sym = S => S.every(p => has(S, p[1], p[0])), trans = S => S.every(p => S.every(q => p[1] !== q[0] || has(S, p[0], q[1])));
module.exports = {
  name: 'discrete-properties-relations', course: 'Discrete Math', unitNo: 6, unitName: 'Properties of Relations',
  focus: 'relations and inverses, directed graphs, reflexive, symmetric and transitive properties',
  morefocus: 'relations on infinite sets, partitions, equivalence relations and equivalence classes',
  front: [
    { title: 'Relation Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['relation on A', 'a subset of ⟨A \\times A⟩', '⟨\\{(1, 2), (2, 3)\\}⟩'],
      ['a R b', '⟨(a, b) \\in R⟩', '⟨2 < 5⟩'],
      ['inverse R⁻¹', 'reverse every pair', '“taller than” → “shorter than”'],
      ['digraph', 'arrow ⟨a \\to b⟩ for ⟨(a, b)⟩, loop for ⟨(a, a)⟩', 'see the next panel']] },
    { title: 'Directed Graph of R', color: 'blue', kind: 'html',
      fig: D.graph({ id: 'r1', v: { 1: [10, 20], 2: [90, 20], 3: [50, 85] }, e: [[1, 1], [2, 2], [3, 3], [1, 2], [2, 1]], directed: true, inches: 1.9, h: 120 }),
      figFirst: true, html: '⟨A = \\{1, 2, 3\\}⟩, ⟨R = \\{(1,1), (2,2), (3,3), (1,2), (2,1)\\}⟩. Loops at every vertex: reflexive. Every arrow has a return arrow: symmetric. Every two-step path has a shortcut: transitive.',
      check: [{ true: refl(R, [1, 2, 3]) + ' && ' + sym(R) + ' && ' + trans(R) }] },
    { title: 'The Three Properties', color: 'green', kind: 'table', plain: true, head: ['Property', 'Definition (on set A)', 'Digraph test'], rows: [
      ['reflexive', '⟨(a, a) \\in R⟩ for every ⟨a \\in A⟩', 'loop at every vertex'],
      ['symmetric', '⟨(a, b) \\in R \\Rightarrow (b, a) \\in R⟩', 'arrows come in pairs'],
      ['transitive', '⟨(a, b), (b, c) \\in R \\Rightarrow (a, c) \\in R⟩', 'every 2-step path has a shortcut']],
      after: 'To <b>disprove</b> a property, give one failing pair (or pair of pairs).' },
    { title: 'Checking an Example', color: 'orange', kind: 'example', text: '⟨A = \\{1, 2, 3\\}⟩, ⟨R = \\{(1, 1), (2, 2), (1, 2), (2, 3)\\}⟩.',
      example: 'Which properties fail?', steps: [['Reflexive:', 'no, ⟨(3, 3) \\notin R⟩'], ['Symmetric:', 'no, ⟨(1, 2)⟩ but not ⟨(2, 1)⟩'], ['Transitive:', 'no, ⟨(1, 2), (2, 3)⟩ but not ⟨(1, 3)⟩']], answer: 'none of the three hold',
      check: { true: '!' + refl([[1, 1], [2, 2], [1, 2], [2, 3]], [1, 2, 3]) + ' && !' + sym([[1, 1], [2, 2], [1, 2], [2, 3]]) + ' && !' + trans([[1, 1], [2, 2], [1, 2], [2, 3]]) } },
    { title: 'Familiar Relations', color: 'pink', kind: 'table', head: ['Relation', 'Refl.', 'Sym.', 'Trans.'], rows: [
      ['⟨=⟩ on ⟨\\mathbb{R}⟩', '✔', '✔', '✔'], ['⟨<⟩ on ⟨\\mathbb{R}⟩', '✘', '✘', '✔'], ['⟨\\le⟩ on ⟨\\mathbb{R}⟩', '✔', '✘', '✔'], ['⟨\\ne⟩ on ⟨\\mathbb{Z}⟩', '✘', '✔', '✘'],
      ['⟨a \\mid b⟩ on ⟨\\mathbb{Z}^{+}⟩', '✔', '✘', '✔'], ['⟨|x - y| < 1⟩ on ⟨\\mathbb{R}⟩', '✔', '✔', '✘']],
      after: '⟨|x - y| < 1⟩ fails transitivity: ⟨0, 0.6, 1.2⟩.', check: { true: 'Math.abs(0-0.6)<1 && Math.abs(0.6-1.2)<1 && !(Math.abs(0-1.2)<1)' } },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Reflexive needs a loop at <b>every</b> element.', 'Check every chain for transitivity, including ones that return to the start.', 'The empty relation is symmetric and transitive (vacuously).'],
      bad: [['⟨R^{-1}⟩ = negate the numbers', 'reverse each pair'], ['One working example proves a property', 'you need every case'], ['Symmetric + transitive ⟹ reflexive', 'false if some element is related to nothing']] }
  ],
  back: [
    { title: 'Counting Relations', color: 'purple', kind: 'table', plain: true, head: ['On a set with ⟨n⟩ elements', 'Number'], rows: [
      ['all relations', '⟨2^{n^2}⟩ (⟨n = 3⟩: 512)'], ['reflexive', '⟨2^{n^2 - n}⟩ (64)'], ['symmetric', '⟨2^{n(n+1)/2}⟩ (64)'], ['reflexive and symmetric', '⟨2^{n(n-1)/2}⟩ (8)']],
      check: [{ num: '2**9', is: 512 }, { num: '2**6', is: 64 }, { num: '2**(3*4/2)', is: 64 }, { num: '2**3', is: 8 }] },
    { title: 'Partitions', color: 'blue', kind: 'example', text: 'A partition of ⟨A⟩ is a set of <b>nonempty</b>, <b>disjoint</b> blocks whose union is ⟨A⟩. Its induced relation: ⟨x\\,R\\,y⟩ when ⟨x, y⟩ are in the same block.',
      example: 'Partition ⟨\\{\\{1, 2, 3\\}, \\{4, 5\\}\\}⟩ of ⟨\\{1, \\dots, 5\\}⟩', steps: [['Pairs:', 'a block of size ⟨k⟩ gives ⟨k^2⟩ pairs'], ['Count:', '⟨3^2 + 2^2⟩']], answer: '13 ordered pairs',
      check: { num: '3*3+2*2', is: 13 } },
    { title: 'Equivalence Relations', color: 'green', kind: 'html',
      html: 'An <b>equivalence relation</b> is reflexive, symmetric and transitive. Examples: “same birthday”, congruence ⟨a \\equiv b \\pmod n⟩ (⟨n \\mid a - b⟩), ⟨x^2 = y^2⟩. Not: “⟨\\le⟩” (not symmetric), “friend of” (not transitive).<br><b>Theorem:</b> equivalence relations and partitions correspond one-to-one: the classes form a partition.' },
    { title: 'Equivalence Classes', color: 'orange', kind: 'example', text: '⟨[a] = \\{x \\mid a\\,R\\,x\\}⟩. Any two classes are equal or disjoint.',
      example: 'Congruence mod 4 on ⟨\\{0, 1, \\dots, 9\\}⟩', steps: [['⟨[0]⟩:', '⟨\\{0, 4, 8\\}⟩'], ['⟨[1] = [5]⟩:', '⟨\\{1, 5, 9\\}⟩'], ['Others:', '⟨\\{2, 6\\}⟩, ⟨\\{3, 7\\}⟩']], answer: '4 distinct classes',
      fig: D.graph({ id: 'eq', v: { 0: [0, 10], 4: [26, 10], 8: [13, 85], 2: [45, 10], 6: [45, 85], 3: [62, 10], 7: [62, 85], 1: [80, 10], 5: [100, 47], 9: [80, 85] }, e: [[0, 4], [4, 8], [8, 0], [2, 6], [3, 7], [1, 5], [5, 9], [9, 1]], inches: 2.3, w: 220, h: 90 }),
      check: { num: 'new Set([...Array(10).keys()].map(x => x % 4)).size', is: 4 } },
    { title: 'Proving an Equivalence Relation', color: 'pink', kind: 'list', items: [
      '<b>Relation:</b> ⟨m\\,R\\,n \\iff 3 \\mid (m - n)⟩ on ⟨\\mathbb{Z}⟩.',
      '<b>Reflexive:</b> ⟨m - m = 0 = 3 \\cdot 0⟩.',
      '<b>Symmetric:</b> ⟨m - n = 3k \\Rightarrow n - m = 3(-k)⟩.',
      '<b>Transitive:</b> ⟨m - n = 3k⟩, ⟨n - p = 3j⟩ ⟹ ⟨m - p = 3(k + j)⟩.',
      '<b>Classes:</b> ⟨[0], [1], [2]⟩ (remainders mod 3).'] },
    { title: 'Challenge', color: 'teal', kind: 'html',
      html: 'How many equivalence relations are there on ⟨\\{1, 2, 3, 4\\}⟩? Count partitions: one block (1), two blocks (7), three blocks (6), four blocks (1): <b>15</b> (the Bell number ⟨B_4⟩).<br>On ⟨\\mathbb{Z} \\times (\\mathbb{Z} - \\{0\\})⟩, ⟨(a, b)\\,R\\,(c, d) \\iff ad = bc⟩ is an equivalence relation whose classes are the rational numbers.',
      check: { num: '1+7+6+1', is: 15 } }
  ]
};
