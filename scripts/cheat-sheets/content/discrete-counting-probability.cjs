/* Discrete Math Unit 7 cheat sheet (Counting and Probability). Every count is checked by build.cjs. */
const D = require('../dmfigs.cjs');
const C = (n, r) => { let x = 1; for (let i = 1; i <= r; i++) x = x * (n - r + i) / i; return Math.round(x); };
const P = (n, r) => { let x = 1; for (let i = 0; i < r; i++) x *= n - i; return x; };
module.exports = {
  name: 'discrete-counting-probability', course: 'Discrete Math', unitNo: 7, unitName: 'Counting and Probability',
  focus: 'sample spaces, events, lists and arrays, possibility trees, addition and multiplication rules',
  morefocus: 'permutations and combinations, equally likely probability and counting with probability',
  front: [
    { title: 'Sample Spaces and Events', color: 'purple', kind: 'vocab', rows: [
      ['sample space S', 'all outcomes', 'two coins: HH, HT, TH, TT'],
      ['event E', 'a subset of ⟨S⟩', '“at least one H”: 3 outcomes'],
      ['equally likely', 'every outcome has the same chance', 'a fair die'],
      ['mutually exclusive', 'events with no common outcome', 'roll 1 / roll 6']] },
    { title: 'Possibility Trees', color: 'blue', kind: 'html', figFirst: true,
      fig: D.tree({ levels: [['H', 'T'], ['H', 'T'], ['H', 'T']], inches: 2.1, gap: 13 }),
      html: 'Three coin tosses give ⟨2 \\cdot 2 \\cdot 2 = 8⟩ leaves. Trees also handle processes that stop early, such as a best-of-three match (6 outcomes: AA, ABA, ABB, BAA, BAB, BB).',
      check: [{ num: '2**3', is: 8 }, { num: '["AA","ABA","ABB","BAA","BAB","BB"].length', is: 6 }] },
    { title: 'Lists: the Fencepost Rule', color: 'green', kind: 'example', text: 'The list ⟨m, m + 1, \\dots, n⟩ has ⟨n - m + 1⟩ integers.',
      example: 'How many multiples of 7 are between 100 and 500?', steps: [['Multiples:', '⟨7 \\cdot 15 = 105⟩ to ⟨7 \\cdot 71 = 497⟩'], ['Count:', '⟨71 - 15 + 1⟩']], answer: '57',
      check: { num: '[...Array(401).keys()].map(i => i + 100).filter(n => n % 7 === 0).length', is: 57 } },
    { title: 'Addition and Multiplication', color: 'orange', kind: 'table', plain: true, head: ['Rule', 'Use when', 'Example'], rows: [
      ['multiplication', 'a sequence of steps (“and”)', '3 shirts and 4 pants: 12 outfits'],
      ['addition', 'disjoint cases (“or”)', '7 mysteries or 5 biographies: 12'],
      ['inclusion-exclusion', 'overlapping cases', '⟨|A \\cup B| = |A| + |B| - |A \\cap B|⟩'],
      ['complement', '“at least one”', '⟨2^8 - 1 = 255⟩ bit strings with a 1']],
      check: [{ num: '3*4', is: 12 }, { num: '2**8-1', is: 255 }] },
    { title: 'State the Assumptions', color: 'pink', kind: 'table', head: ['Order?', 'Repetition?', 'Count', 'Example (n = 10, r = 3)'], rows: [
      ['yes', 'yes', '⟨n^r⟩', 'lock codes: 1000'], ['yes', 'no', '⟨P(n, r) = \\tfrac{n!}{(n - r)!}⟩', 'gold, silver, bronze: 720'], ['no', 'no', '⟨C(n, r) = \\tfrac{n!}{r!\\,(n - r)!}⟩', 'committees: 120'],
      ['no', 'yes', '⟨C(n + r - 1, r)⟩', '3 scoops of 10 flavors: 220']],
      check: [{ num: '10**3', is: 1000 }, { num: P(10, 3), is: 720 }, { num: C(10, 3), is: 120 }, { num: C(12, 3), is: 220 }] },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Decide order, repetition and replacement first.', 'Handle restricted positions first (no leading 0).', 'Use the complement for “at least one”.'],
      bad: [['Adding for “and”', 'multiply'], ['⟨40 - 15⟩ integers in 15…40', '⟨40 - 15 + 1 = 26⟩'], ['Counting a team as ordered', 'divide by ⟨r!⟩']] }
  ],
  back: [
    { title: 'Permutations and Combinations', color: 'purple', kind: 'example', text: 'Repeated identical objects: divide by the factorial of each repeat count.',
      example: 'Arrangements of MISSISSIPPI', steps: [['Letters:', '11 total; I 4, S 4, P 2'], ['Count:', '⟨\\tfrac{11!}{4!\\,4!\\,2!}⟩']], answer: '34650',
      check: { num: '39916800/(24*24*2)', is: 34650 } },
    { title: 'Equally Likely Probability', color: 'blue', kind: 'example', text: '⟨P(E) = \\tfrac{|E|}{|S|}⟩ when outcomes are equally likely; ⟨0 \\le P(E) \\le 1⟩ and ⟨P(E\') = 1 - P(E)⟩.',
      example: 'Two fair dice: ⟨P(\\text{sum} = 8)⟩', steps: [['Outcomes:', '(2,6), (3,5), (4,4), (5,3), (6,2)'], ['Divide:', '⟨\\tfrac{5}{36}⟩']], answer: '⟨\\tfrac{5}{36}⟩',
      check: { num: '[1,2,3,4,5,6].flatMap(a => [1,2,3,4,5,6].map(b => a + b)).filter(s => s === 8).length', is: 5 } },
    { title: 'Two Dice Sums', color: 'green', kind: 'table', head: ['sum', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'], rows: [['ways', ...[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map(s => String(6 - Math.abs(7 - s)))]],
      after: 'The 11 sums are <b>not</b> equally likely; the 36 ordered pairs are. ⟨P(7) = \\tfrac{6}{36} = \\tfrac{1}{6}⟩.',
      check: { num: '[2,3,4,5,6,7,8,9,10,11,12].map(s => 6 - Math.abs(7 - s)).reduce((a, b) => a + b)', is: 36 } },
    { title: 'With vs Without Replacement', color: 'orange', kind: 'example', text: 'Use the same counting model for favorable and total outcomes.',
      example: 'Bag: 3 red, 2 blue. Draw 2. P(both red)?', steps: [['With replacement:', '⟨\\tfrac{3}{5} \\cdot \\tfrac{3}{5} = \\tfrac{9}{25}⟩'], ['Without:', '⟨\\tfrac{C(3,2)}{C(5,2)} = \\tfrac{3}{10}⟩']], answer: '⟨\\tfrac{9}{25}⟩ vs ⟨\\tfrac{3}{10}⟩',
      check: [{ num: '9/25', is: 0.36 }, { num: C(3, 2) / C(5, 2), is: 0.3 }] },
    { title: 'Counting + Probability', color: 'pink', kind: 'table', plain: true, head: ['Question', 'Answer'], rows: [
      ['5 coin tosses: P(exactly 3 heads)', '⟨\\tfrac{C(5, 3)}{2^5} = \\tfrac{10}{32} = \\tfrac{5}{16}⟩'],
      ['Committee of 4 from 6 boys, 4 girls: P(2 girls)', '⟨\\tfrac{C(4,2)C(6,2)}{C(10,4)} = \\tfrac{90}{210} = \\tfrac{3}{7}⟩'],
      ['Seat 4 people at random: P(Ann next to Bo)', '⟨\\tfrac{2 \\cdot 3!}{4!} = \\tfrac{1}{2}⟩']],
      check: [{ num: C(5, 3) / 32, is: 5 / 16 }, { num: C(4, 2) * C(6, 2) / C(10, 4), is: 3 / 7 }, { num: '2*6/24', is: 0.5 }] },
    { title: 'Challenge: Birthdays', color: 'teal', kind: 'html',
      html: 'Assume 365 equally likely birthdays, independent, no leap day. For ⟨n⟩ people, ⟨P(\\text{all different}) = \\tfrac{365 \\cdot 364 \\cdots (366 - n)}{365^n}⟩. With 23 people, ⟨P(\\text{some match}) \\approx 0.507⟩ — more than half!',
      check: { num: 'Math.round((1 - [...Array(23).keys()].reduce((p, i) => p * (365 - i) / 365, 1)) * 1000) / 1000', is: 0.507 } }
  ]
};
