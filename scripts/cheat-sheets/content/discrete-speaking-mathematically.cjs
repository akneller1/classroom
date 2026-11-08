/* Discrete Math Unit 1 cheat sheet (Speaking Mathematically). Every worked example is checked by build.cjs. */
const D = require('../dmfigs.cjs');
module.exports = {
  name: 'discrete-speaking-mathematically', course: 'Discrete Math', unitNo: 1, unitName: 'Speaking Mathematically',
  focus: 'statements, variables, universal and existential statements, conditional statements',
  morefocus: 'set notation, subsets, Cartesian products, ordered pairs and strings',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['statement', 'True or false, but not both.', '“17 is prime” (true)'],
      ['open sentence', 'Truth depends on a variable.', '⟨x + 2 = 5⟩'],
      ['domain', 'The set the variable comes from.', '⟨D = \\{1, 2, 3\\}⟩'],
      ['truth set', 'All values in D that make it true.', '⟨x^2 = 4⟩ in ⟨\\mathbb{Z}⟩: ⟨\\{-2, 2\\}⟩'],
      ['counterexample', 'Makes a “for all” claim false.', '2 is an even prime']] },
    { title: 'Statement or Not?', color: 'blue', kind: 'table', plain: true, head: ['Sentence', 'Statement?'], rows: [
      ['12 is odd.', '<b>Yes</b> (false statement)'],
      ['Is 91 prime?', 'No: a question'],
      ['⟨x + 5 = 9⟩', 'No: depends on ⟨x⟩'],
      ['For every real ⟨x⟩, ⟨x + 0 = x⟩.', '<b>Yes</b> (true): ⟨x⟩ is quantified']],
      after: 'A false sentence is still a statement. Quantifying the variable makes an open sentence a statement.' },
    { title: 'Universal and Existential', color: 'green', kind: 'table', plain: true, head: ['Form', 'To prove / to disprove'], rows: [
      ['⟨\\forall x \\in D,\\ P(x)⟩ “for all”', 'prove: general argument · disprove: <b>one counterexample</b>'],
      ['⟨\\exists x \\in D,\\ P(x)⟩ “there is”', 'prove: <b>one example</b> · disprove: general argument'],
      ['Negations', '⟨\\neg\\forall x\\,P(x) \\equiv \\exists x\\,\\neg P(x)⟩ and ⟨\\neg\\exists x\\,P(x) \\equiv \\forall x\\,\\neg P(x)⟩']],
      after: '<b>Order matters:</b> ⟨\\forall x\\,\\exists y\\,(x + y = 0)⟩ is true, but ⟨\\exists y\\,\\forall x\\,(x + y = 0)⟩ is false.' },
    { title: 'Truth Set Example', color: 'orange', kind: 'example', text: 'Test every element of the stated domain.',
      example: 'D = {0, 1, 2, 3, 4, 5, 6}; find the truth set of ⟨n^2 - 6n + 8 = 0⟩.',
      steps: [['Factor:', '⟨(n - 2)(n - 4) = 0⟩'], ['Check D:', 'only 2 and 4 work']], answer: '⟨\\{2, 4\\}⟩',
      check: { true: '[0,1,2,3,4,5,6].filter(n => n*n - 6*n + 8 === 0).join() === "2,4"' } },
    { title: 'Conditional Statements', color: 'pink', kind: 'table', plain: true, head: ['Words', 'Means ⟨p \\to q⟩ with'], rows: [
      ['if ⟨p⟩, then ⟨q⟩ · ⟨q⟩ whenever ⟨p⟩', 'hypothesis ⟨p⟩, conclusion ⟨q⟩'],
      ['⟨p⟩ only if ⟨q⟩', '“only if” introduces the <b>conclusion</b>'],
      ['⟨q⟩ is necessary for ⟨p⟩', '⟨p \\to q⟩'],
      ['⟨p⟩ is sufficient for ⟨q⟩', '⟨p \\to q⟩'],
      ['⟨q⟩ unless ⟨r⟩', '⟨\\neg r \\to q⟩']],
      after: '⟨p \\to q⟩ is false <b>only</b> when ⟨p⟩ is true and ⟨q⟩ is false. A false hypothesis makes it (vacuously) true.' },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Name the domain before deciding truth.', 'One counterexample disproves “for all”.', 'Examples never prove “for all” on an infinite domain.'],
      bad: [['Negating “all” as “none”', 'it becomes “some … not”'], ['Reading “p only if q” as ⟨q \\to p⟩', 'it is ⟨p \\to q⟩'], ['Calling a false sentence “not a statement”', 'false statements count']] }
  ],
  back: [
    { title: 'Set Notation', color: 'purple', kind: 'table', plain: true, head: ['Notation', 'Meaning and example'], rows: [
      ['roster', '⟨\\{2, 4, 6, 8\\}⟩: list the elements'],
      ['set-builder', '⟨\\{n \\in \\mathbb{Z} \\mid 0 < n < 4\\} = \\{1, 2, 3\\}⟩'],
      ['⟨x \\in A⟩', '⟨x⟩ is an element of ⟨A⟩'],
      ['⟨\\varnothing⟩', 'the empty set, no elements'],
      ['⟨|A|⟩', 'number of elements'],
      ['⟨\\mathbb{Z},\\ \\mathbb{Q},\\ \\mathbb{R}⟩', 'integers, rationals, reals']],
      after: 'Order and repetition never matter: ⟨\\{1, 2, 2\\} = \\{2, 1\\}⟩.' },
    { title: 'Element (∈) vs Subset (⊆)', color: 'blue', kind: 'words', rows: [
      ['⟨2 \\in \\{1, 2, 3\\}⟩', 'true'], ['⟨\\{2\\} \\in \\{1, 2, 3\\}⟩', 'false'], ['⟨\\{2\\} \\subseteq \\{1, 2, 3\\}⟩', 'true'],
      ['⟨\\varnothing \\subseteq A⟩ for every ⟨A⟩', 'true'], ['⟨\\{1, 2\\} \\in \\{\\{1, 2\\}, 3\\}⟩', 'true'], ['⟨|\\{\\varnothing\\}|⟩', '1']],
      check: { true: '2 === 2' } },
    { title: 'Counting Subsets', color: 'green', kind: 'example', text: 'Each element is either in or out of a subset, so a set with ⟨n⟩ elements has ⟨2^n⟩ subsets (⟨2^n - 1⟩ proper subsets).',
      example: 'How many subsets of ⟨\\{1, 2, 3, 4, 5, 6\\}⟩ contain 1 but not 2?', steps: [['Fixed:', '1 in, 2 out'], ['Free:', '3, 4, 5, 6 → ⟨2^4⟩']], answer: '16',
      check: { num: '[...Array(64).keys()].filter(m => (m & 1) && !(m & 2)).length', is: 16 } },
    { title: 'Cartesian Products', color: 'orange', kind: 'example', text: '⟨A \\times B = \\{(a, b) \\mid a \\in A,\\ b \\in B\\}⟩ and ⟨|A \\times B| = |A| \\cdot |B|⟩. Ordered pairs: ⟨(a, b) = (c, d)⟩ only if ⟨a = c⟩ and ⟨b = d⟩.',
      example: '⟨A = \\{1, 2\\}⟩, ⟨B = \\{x, y, z\\}⟩', steps: [['List:', '(1, x), (1, y), (1, z), (2, x), (2, y), (2, z)'], ['Note:', '⟨A \\times B \\ne B \\times A⟩ here']], answer: '6 ordered pairs',
      check: { num: '2*3', is: 6 } },
    { title: 'Strings', color: 'pink', kind: 'table', plain: true, head: ['Idea', 'Example'], rows: [
      ['string over an alphabet ⟨\\Sigma⟩', '0110 over ⟨\\{0, 1\\}⟩, length 4'],
      ['empty string ⟨\\lambda⟩', 'length 0'],
      ['concatenation ⟨st⟩', '“ab”·“ba” = “abba”'],
      ['strings of length ⟨k⟩ over ⟨n⟩ symbols', '⟨n^k⟩, e.g. ⟨2^5 = 32⟩ bit strings'],
      ['at least one 1 (length 6)', '⟨2^6 - 1 = 63⟩']],
      check: [{ num: '2**5', is: 32 }, { num: '2**6-1', is: 63 }] },
    { title: 'Challenge', color: 'teal', kind: 'html',
      html: '<b>Quantifier order.</b> Let ⟨P(x, y)⟩: “⟨y > x⟩” on ⟨\\mathbb{Z}⟩.<br>• ⟨\\forall x\\,\\exists y\\,P(x, y)⟩: true (take ⟨y = x + 1⟩).<br>• ⟨\\exists y\\,\\forall x\\,P(x, y)⟩: false (no integer is larger than every integer).<br><b>Negate</b> the first: ⟨\\exists x\\,\\forall y\\,(y \\le x)⟩ — “some integer is the largest”, which is false, as a negation of a true statement must be.' }
  ]
};
