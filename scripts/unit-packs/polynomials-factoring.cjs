/* Unit 9 · Polynomials: unit pack content (see build.cjs).
   (The data.js unit id is polynomials-factoring; its skills are classifying, adding, subtracting, multiplying and dividing polynomials.) */
'use strict';
module.exports = {
  unit: 'polynomials-factoring', prefix: 'polynomials', unitNo: 9, unitName: 'Polynomials', course: 'Algebra 1',

  mystery: {
    skills: 'classifying, adding, subtracting, multiplying and dividing polynomials, and special products.',
    slug: 'toy-factory-takedown', title: 'The Toy Factory Takedown', eyebrow: 'Case file No. 9',
    tagline: 'The prototype robot vanished from Tinker Toy Works the night before the big reveal. Solve each problem to earn a clue.',
    palette: { navy: '#1d2b2a', accent: '#ff8a3d' },
    labels: { p: 'The Suspects', l: 'The Places', m: 'The Methods' },
    placeholder: 'Your answer', inputHint: 'Type a number, or a polynomial in standard form like 3x^2 - 4x + 5 (use ^ for exponents).', symbols: ['^'],
    intro: [
      'Tomorrow was the big reveal at <b>Tinker Toy Works</b>: “Gizmo,” a robot that can build its own blocks. But when the night shift clocked in, the <b>Gizmo prototype</b> was gone from the design lab!',
      'Six people were in the factory, each seen in a different spot, and there are six ways the robot could have been sneaked out. You are the lead detective. Find out <b>who</b> took it, <b>where</b> they were, and <b>how</b> they did it.'
    ],
    suspects: [
      { name: 'Ms. Pratt', role: 'Head Designer', skin: '#f4d3b5', hair: 'bun', hairColor: '#5a3a22', color: '#7a3fb0', bg: '#e8d9f5', acc: 'glasses' },
      { name: 'Gus Moreno', role: 'Assembly Lead', skin: '#c68a5b', hair: 'short', hairColor: '#1d1d1d', color: '#24406e', bg: '#d6e2f7', acc: 'cap' },
      { name: 'Dot Ellis', role: 'Paint Artist', skin: '#8d5a3b', hair: 'long', hairColor: '#15151a', color: '#c0392b', bg: '#fbdada', acc: 'none' },
      { name: 'Mr. Krane', role: 'Rival Toymaker', skin: '#e0ac7e', hair: 'bald', hairColor: '#1d1d1d', color: '#1f7a4d', bg: '#d3f1ea', acc: 'bowtie' },
      { name: 'Penny Lu', role: 'Quality Tester', skin: '#f1c9a5', hair: 'long', hairColor: '#2a1a12', color: '#e4752a', bg: '#ffe3c9', acc: 'none' },
      { name: 'Hank Ford', role: 'Night Watchman', skin: '#c68a5b', hair: 'short', hairColor: '#7a7a7a', color: '#8a5a2b', bg: '#f1e4c9', acc: 'cap' }
    ],
    places: ['Design Lab', 'Paint Shop', 'Assembly Line', 'Shipping Dock', 'Break Room', 'Testing Room'],
    methods: ['Packed in a teddy-bear box', 'Hidden in a paint barrel', 'Driven out in a toy truck', 'Mailed in a shipping crate', 'Stuffed in a laundry cart', 'Walked out by remote control'],
    culprit: { p: 3, l: 0, m: 2 },
    ending: '<b>Mr. Krane</b>, the rival toymaker, had sneaked in with a tour group. He hid in the <b>Design Lab</b>, set Gizmo in the back of a giant <b>toy truck</b> and drove it out the loading door. Every alibi and every cleared method pointed straight at him. Game over, Mr. Krane!',
    questions: [
      { instr: 'Add. Write the answer in standard form.', tex: '(3x^2 + 2x - 5) + (x^2 - 4x + 7)', answer: { t: 'expr', v: '4x^2 - 2x + 2', maxParens: 0 }, check: { expr: '(3*x**2+2*x-5)+(x**2-4*x+7)', is: '4*x**2-2*x+2' },
        steps: ['Combine like terms: ⟨3x^2 + x^2 = 4x^2⟩, ⟨2x - 4x = -2x⟩, ⟨-5 + 7 = 2⟩', '⟨4x^2 - 2x + 2⟩'], clue: { p: 0, l: 5, text: 'Ms. Pratt was in the Testing Room all night, timing how fast the robot dogs could fetch. The test videos show her.' } },
      { instr: 'Subtract. Write the answer in standard form.', tex: '(5x^2 - 3x + 1) - (2x^2 + x - 4)', answer: { t: 'expr', v: '3x^2 - 4x + 5', maxParens: 0 }, check: { expr: '(5*x**2-3*x+1)-(2*x**2+x-4)', is: '3*x**2-4*x+5' },
        steps: ['Change every sign in the second polynomial: ⟨5x^2 - 3x + 1 - 2x^2 - x + 4⟩', '⟨3x^2 - 4x + 5⟩'], clue: { m: 0, text: 'The teddy-bear boxes were sealed with tape that has not been cut.' } },
      { instr: 'What is the degree of this polynomial?', tex: '4x^3 - 7x^5 + 2', answer: { t: 'num', v: '5' }, check: { num: '5', is: 5 },
        steps: ['The degree is the largest exponent.', '⟨-7x^5⟩ has exponent 5, so the degree is ⟨5⟩'], clue: { p: 1, l: 2, text: 'Gus Moreno was fixing a stuck conveyor belt on the Assembly Line. His whole crew was with him.' } },
      { instr: 'Multiply:', tex: '3x(2x - 5)', answer: { t: 'expr', v: '6x^2 - 15x', maxParens: 0 }, check: { expr: '3*x*(2*x-5)', is: '6*x**2-15*x' },
        steps: ['Distribute ⟨3x⟩ to each term.', '⟨3x \\cdot 2x - 3x \\cdot 5 = 6x^2 - 15x⟩'], clue: { m: 1, text: 'The paint barrels are full to the brim. A robot would have made them overflow.' } },
      { instr: 'Multiply:', tex: '(x + 4)(x - 3)', answer: { t: 'expr', v: 'x^2 + x - 12', maxParens: 0 }, check: { expr: '(x+4)*(x-3)', is: 'x**2+x-12' },
        steps: ['FOIL: ⟨x^2 - 3x + 4x - 12⟩', '⟨x^2 + x - 12⟩'], clue: { p: 2, l: 1, text: 'Dot Ellis was painting 200 toy rockets in the Paint Shop. The paint fumes alarm logged her the whole time.' } },
      { instr: 'Multiply:', tex: '(x - 5)^2', answer: { t: 'expr', v: 'x^2 - 10x + 25', maxParens: 0 }, check: { expr: '(x-5)**2', is: 'x**2-10*x+25' },
        steps: ['⟨(a - b)^2 = a^2 - 2ab + b^2⟩', '⟨x^2 - 10x + 25⟩'], clue: { m: 3, text: 'The shipping crates were all weighed. Not one was heavy enough to hold a robot.' } },
      { instr: 'Multiply:', tex: '(2x + 3)(2x - 3)', answer: { t: 'expr', v: '4x^2 - 9', maxParens: 0 }, check: { expr: '(2*x+3)*(2*x-3)', is: '4*x**2-9' },
        steps: ['Difference of squares: ⟨(a + b)(a - b) = a^2 - b^2⟩', '⟨(2x)^2 - 3^2 = 4x^2 - 9⟩'], clue: { p: 4, l: 3, text: 'Penny Lu was loading trucks at the Shipping Dock. The truck drivers waited with her.' } },
      { instr: 'Divide:', tex: '\\dfrac{12x^3 - 8x^2}{4x}', answer: { t: 'expr', v: '3x^2 - 2x', maxParens: 0 }, check: { expr: '(12*x**3-8*x**2)/(4*x)', is: '3*x**2-2*x' },
        steps: ['Divide each term by ⟨4x⟩.', '⟨\\dfrac{12x^3}{4x} - \\dfrac{8x^2}{4x} = 3x^2 - 2x⟩'], clue: { m: 4, text: 'The laundry carts are tiny. They only hold aprons.' } },
      { instr: 'What is the leading coefficient of this polynomial?', tex: '6 - 2x + 9x^3', answer: { t: 'num', v: '9' }, check: { num: '9', is: 9 },
        steps: ['Write it in standard form: ⟨9x^3 - 2x + 6⟩', 'The leading coefficient is ⟨9⟩'], clue: { p: 5, l: 4, text: 'Hank Ford was in the Break Room watching the security monitors. The monitor log shows him there.' } },
      { instr: 'A rectangle is 2x + 1 long and x + 3 wide. Write its area as a polynomial.', text: 'Area = ⟨(2x + 1)(x + 3)⟩', answer: { t: 'expr', v: '2x^2 + 7x + 3', maxParens: 0 }, check: { expr: '(2*x+1)*(x+3)', is: '2*x**2+7*x+3' },
        steps: ['⟨(2x + 1)(x + 3) = 2x^2 + 6x + x + 3⟩', '⟨2x^2 + 7x + 3⟩'], clue: { m: 5, text: 'The robot’s remote was locked in the safe. Without it, Gizmo cannot walk anywhere.' } }
    ]
  },

  escape: {
    title: 'Escape the Toy Workshop', emoji: '🧸', endEmoji: '🧸🎁',
    intro: 'You are helping at the Toy Workshop when the elves’ security system locks every door! Each lock runs on a polynomial. Solve them, unlock five rooms, and get out in <b>30 minutes</b>, before the toys go out for delivery.',
    finalStory: 'The front door has a five-letter keypad. A gift tag says: “Line up your key cards from the smallest stamp to the largest. The letters spell the password.”',
    finalAsk: 'Password?', word: 'BLOCK',
    outro: 'BLOCK! The door swings open and a toy train toots. The head toymaker grins: “You put the pieces together. Come back any time.”',
    stages: [
      { name: 'The Block Machine', type: 'fields', stamp: 71, letter: 'C',
        story: 'The block machine needs two numbers. Evaluate each polynomial when x = 2.',
        scene: { kind: 'svg', viewBox: '0 0 400 300', svg: '<rect x="90" y="60" width="220" height="150" rx="14" fill="#1b2150" stroke="#ff8a3d" stroke-width="3"/><text x="200" y="100" text-anchor="middle" fill="#fff" font-size="18">BLOCK MACHINE</text><text x="200" y="150" text-anchor="middle" fill="#ff8a3d" font-size="26" font-weight="700">x = 2</text><text x="200" y="260" text-anchor="middle" font-size="48">🧱</text>' },
        title: 'Machine Settings', prompt: '<p>Evaluate when x = 2.</p>', fields: [{ label: 'x² + 3x =', answer: 10 }, { label: '2x³ − 1 =', answer: 15 }], button: 'Start the machine',
        hints: ['Replace every x with 2.', '2² + 3(2) = 4 + 6.', '2(2³) − 1 = 2(8) − 1.'], key: 'x² + 3x = 10, 2x³ − 1 = 15.', check: [['2**2+3*2', 10], ['2*2**3-1', 15]] },
      { name: 'The Paint Room', type: 'cipher', stamp: 14, letter: 'B',
        story: 'A coded message is painted on the wall. The shift is written somewhere in this room. Click things to search.',
        scene: { kind: 'emoji', bg: '#2a1530', floor: '#43264a', items: [{ e: '🎨', x: 90, y: 150, s: 60, msg: 'A palette of wet paint.' }, { e: '📋', x: 300, y: 200, s: 50, clue: 'Work order:<br>Shift = the degree of 3x⁴ − x + 8, plus its number of terms', msg: 'A work order with a rule on it!' }, { e: '🖌️', x: 200, y: 215, s: 42, msg: 'Brushes soaking in water.' }, { e: '🪀', x: 220, y: 105, s: 44, msg: 'A yo-yo. Just a yo-yo.' }] },
        plain: 'THE NEXT KEY IS INSIDE THE DRUM', shift: 7, answer: 'DRUM', askLabel: 'Where is the next key?',
        hints: ['Click the work order.', 'The degree is the biggest exponent. Count the terms too.', 'Degree 4 plus 3 terms = 7. Set the shift to 7.'], key: 'Degree 4 + 3 terms = 7. The message says THE NEXT KEY IS INSIDE THE DRUM.', checkNum: ['4+3', 7] },
      { name: 'The Sorting Bins', type: 'classify', stamp: 90, letter: 'K',
        story: 'Four toys have polynomial tags. Put each one in the right bin.',
        scene: { kind: 'emoji', bg: '#13261c', floor: '#2c4a2c', items: [{ e: '🪁', x: 70, y: 170, s: 54 }, { e: '🚂', x: 160, y: 170, s: 54 }, { e: '🪆', x: 250, y: 170, s: 54 }, { e: '🎲', x: 340, y: 170, s: 54 }], caption: 'how many terms?' },
        title: 'Monomial, binomial or trinomial?', prompt: '<p style="color:var(--dim)">Count the terms after combining like terms.</p>',
        items: ['7x³', 'x² − 9', '2x² + 5x − 3', '−4'], options: ['Monomial', 'Binomial', 'Trinomial'], answer: [0, 1, 2, 0],
        hints: ['A monomial has 1 term, a binomial 2, a trinomial 3.', 'A number by itself is a monomial.', 'x² − 9 has two terms.'], key: 'Monomial, binomial, trinomial, monomial.' },
      { name: 'The Gift-Wrap Station', type: 'order', stamp: 33, letter: 'L',
        story: 'The wrapping robot multiplies (x + 3)(x + 5). Put its steps in order.',
        scene: { kind: 'emoji', bg: '#26160f', floor: '#4a2c1c', items: [{ e: '🤖', x: 120, y: 170, s: 70, msg: 'Wrap. Tape. Bow.' }, { e: '🎁', x: 290, y: 175, s: 56, msg: 'A perfectly wrapped present.' }], caption: 'put the steps in order' },
        title: 'Multiply two binomials', prompt: '<div class="eq">(x + 3)(x + 5)</div><p>Place the steps from first to last.</p>',
        steps: ['Multiply the first terms: x · x = x²', 'Multiply the outer and inner terms: 5x and 3x', 'Multiply the last terms: 3 · 5 = 15', 'Combine like terms: x² + 8x + 15'],
        hints: ['Use FOIL: First, Outer, Inner, Last.', 'Combining like terms always comes at the end.', 'x², then 5x + 3x, then 15.'], key: 'x²; 5x and 3x; 15; x² + 8x + 15.', checkExpr: ['(x+3)*(x+5)', 'x**2+8*x+15'] },
      { name: 'The Loading Door', type: 'fields', stamp: 52, letter: 'O', ui: 'dial',
        story: 'The door shows (x + 3)² = x² + Ax + B. Set dial A and dial B.',
        scene: { kind: 'emoji', bg: '#20160e', floor: '#3a2a1a', items: [{ e: '🚪', x: 200, y: 180, s: 120, msg: 'A rolling door with two dials.' }], caption: 'dial A, then dial B' },
        title: 'Square the binomial', prompt: '<div class="eq">(x + 3)² = x² + Ax + B</div><p>Set A and B.</p>', fields: [{ label: 'A', answer: 6 }, { label: 'B', answer: 9 }], button: 'Open the door',
        hints: ['(x + 3)² means (x + 3)(x + 3).', 'The middle term is 2 · x · 3.', 'x² + 6x + 9.'], key: 'A = 6, B = 9: (x + 3)² = x² + 6x + 9.', check: [['2*3', 6], ['3**2', 9]] }
    ]
  },

  cheat: {
    focus: 'vocabulary, classifying, adding and subtracting polynomials',
    morefocus: 'multiplying, special products and dividing by a monomial',
    front: [
      { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
        ['term', 'Numbers and variables joined by multiplication.', '⟨5x^2⟩'], ['like terms', 'Same variables with the same exponents.', '⟨3x^2,\\ -x^2⟩'],
        ['degree', 'The largest exponent of the polynomial.', '⟨x^3 + x⟩: 3'], ['leading coefficient', 'The number in front of the highest-degree term.', '⟨-4x^3 + 1⟩: −4'],
        ['standard form', 'Terms written from highest to lowest degree.', '⟨2x^2 - x + 7⟩']] },
      { title: 'Name It', color: 'blue', kind: 'table', head: ['Polynomial', 'Degree', 'Terms', 'Name'], rows: [
        ['⟨-6⟩', '0', '1', 'constant monomial'], ['⟨4x - 1⟩', '1', '2', 'linear binomial'], ['⟨x^2 + 3x - 2⟩', '2', '3', 'quadratic trinomial'], ['⟨5x^3⟩', '3', '1', 'cubic monomial']] },
      { title: 'Adding', color: 'green', kind: 'example', text: 'Remove the parentheses and combine like terms.',
        example: '⟨(2x^2 + 5x - 1) + (x^2 - 3x + 4)⟩', steps: [['Group:', '⟨(2x^2 + x^2) + (5x - 3x) + (-1 + 4)⟩'], ['Combine:', '⟨3x^2 + 2x + 3⟩']], answer: '⟨3x^2 + 2x + 3⟩' },
      { title: 'Subtracting', color: 'orange', kind: 'example', text: 'Change EVERY sign in the second polynomial, then add.',
        example: '⟨(4x^2 - x + 6) - (x^2 + 2x - 3)⟩', steps: [['Change signs:', '⟨4x^2 - x + 6 - x^2 - 2x + 3⟩'], ['Combine:', '⟨3x^2 - 3x + 9⟩']], answer: '⟨3x^2 - 3x + 9⟩' },
      { title: 'Standard Form', color: 'pink', kind: 'example', text: 'Write the terms from the highest exponent to the lowest. The first term tells you the degree and leading coefficient.',
        example: 'Write ⟨7 - 2x^3 + 5x⟩ in standard form.', steps: [['Order:', '⟨-2x^3 + 5x + 7⟩'], ['Read it:', 'degree 3, leading coefficient −2']], answer: '⟨-2x^3 + 5x + 7⟩' },
      { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
        good: ['Only like terms combine: same variable AND same exponent.', 'When adding, exponents stay the same.', 'Subtracting: change every sign in the second polynomial.'],
        bad: [['⟨x^2 + x^2 \\ne x^4⟩', 'it is ⟨2x^2⟩'], ['⟨-(x^2 - 3)⟩', 'is ⟨-x^2 + 3⟩, not ⟨-x^2 - 3⟩'], ['⟨3x + 2x^2⟩', 'cannot be combined']] }
    ],
    back: [
      { title: 'Distributing a Monomial', color: 'green', kind: 'example', text: 'Multiply the monomial by EVERY term. Multiply the numbers and add the exponents.',
        example: '⟨2x(3x^2 - 4x + 1)⟩', steps: [['Each term:', '⟨2x \\cdot 3x^2 - 2x \\cdot 4x + 2x \\cdot 1⟩'], ['Simplify:', '⟨6x^3 - 8x^2 + 2x⟩']], answer: '⟨6x^3 - 8x^2 + 2x⟩' },
      { title: 'FOIL Two Binomials', color: 'blue', kind: 'example', text: 'First, Outer, Inner, Last, then combine like terms.',
        example: '⟨(x + 4)(2x - 3)⟩', steps: [['F, O, I, L:', '⟨2x^2 - 3x + 8x - 12⟩'], ['Combine:', '⟨2x^2 + 5x - 12⟩']], answer: '⟨2x^2 + 5x - 12⟩' },
      { title: 'Special Products', color: 'purple', kind: 'table', head: ['Name', 'Pattern', 'Example'], rows: [
        ['Square of a sum', '⟨(a + b)^2 = a^2 + 2ab + b^2⟩', '⟨(x + 3)^2 = x^2 + 6x + 9⟩'], ['Square of a difference', '⟨(a - b)^2 = a^2 - 2ab + b^2⟩', '⟨(x - 5)^2 = x^2 - 10x + 25⟩'], ['Sum times difference', '⟨(a + b)(a - b) = a^2 - b^2⟩', '⟨(2x + 3)(2x - 3) = 4x^2 - 9⟩']],
        after: '⚠ ⟨(x + 3)^2⟩ is NOT ⟨x^2 + 9⟩: do not forget the middle term.' },
      { title: 'Dividing by a Monomial', color: 'orange', kind: 'example', text: 'Divide EVERY term by the monomial. Divide the numbers and subtract the exponents.',
        example: '⟨\\dfrac{15x^4 - 10x^2}{5x^2}⟩', steps: [['Each term:', '⟨\\dfrac{15x^4}{5x^2} - \\dfrac{10x^2}{5x^2}⟩'], ['Simplify:', '⟨3x^2 - 2⟩']], answer: '⟨3x^2 - 2⟩' },
      { title: 'Area and Perimeter', color: 'pink', kind: 'example', text: 'Area multiplies the sides; perimeter adds all four sides.',
        example: 'A rectangle is ⟨x + 5⟩ by ⟨x + 2⟩.', steps: [['Area:', '⟨(x + 5)(x + 2) = x^2 + 7x + 10⟩'], ['Perimeter:', '⟨2(x + 5) + 2(x + 2) = 4x + 14⟩']], answer: 'A ⟨= x^2 + 7x + 10⟩, P ⟨= 4x + 14⟩' },
      { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
        'Did I combine ONLY like terms?', 'Did I change every sign when subtracting?', 'Did I multiply every term by every term?', 'Is my answer in standard form?', 'Quick check: plug in ⟨x = 1⟩ on both sides.'] }
    ]
  }
};
