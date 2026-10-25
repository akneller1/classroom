/* Unit 7 · Exponents and Scientific Notation: unit pack content (see build.cjs).
   (The data.js unit id is exponents-exponential-functions; its skills are exponent rules and scientific notation.) */
'use strict';
module.exports = {
  unit: 'exponents-exponential-functions', prefix: 'exponents-scientific-notation', unitNo: 7, unitName: 'Exponents and Scientific Notation', course: 'Algebra 1',

  mystery: {
    skills: 'exponent rules, zero and negative exponents, evaluating powers, and scientific notation.',
    slug: 'planetarium-power-outage', title: 'The Planetarium Power Outage', eyebrow: 'Case file No. 7',
    tagline: 'The Star Map vanished from the Cosmos Planetarium during a blackout. Solve each problem to earn a clue.',
    palette: { navy: '#141b3d', accent: '#ffcf5a' },
    labels: { p: 'The Suspects', l: 'The Places', m: 'The Methods' },
    placeholder: 'Your answer', inputHint: 'Type a number like -4, or an expression like 3x^5 (use ^ for exponents).', symbols: ['^'],
    intro: [
      'It was the grand opening of the <b>Cosmos Planetarium</b>. In the middle of the star show the power went out, and when the lights came back, the <b>Star Map</b>, a 400-year-old chart of the night sky, was gone from its frame!',
      'Six people were in the building, each seen in a different spot, and there are six ways the map could have been sneaked out. You are the lead detective. Find out <b>who</b> took it, <b>where</b> they were, and <b>how</b> they did it.'
    ],
    suspects: [
      { name: 'Dr. Vega', role: 'Head Astronomer', skin: '#c68a5b', hair: 'bun', hairColor: '#1d1d1d', color: '#2b3a8c', bg: '#dbe2fb', acc: 'glasses' },
      { name: 'Orion Blake', role: 'Show Narrator', skin: '#f4d3b5', hair: 'short', hairColor: '#b5651d', color: '#7a3fb0', bg: '#e8d9f5', acc: 'bowtie' },
      { name: 'Luna Reyes', role: 'Telescope Tech', skin: '#8d5a3b', hair: 'long', hairColor: '#15151a', color: '#c0392b', bg: '#fbdada', acc: 'none' },
      { name: 'Mr. Halley', role: 'Gift Shop Manager', skin: '#e0ac7e', hair: 'bald', hairColor: '#1d1d1d', color: '#1f7a4d', bg: '#d3f1ea', acc: 'none' },
      { name: 'Stella Park', role: 'Student Volunteer', skin: '#f1c9a5', hair: 'long', hairColor: '#2a1a12', color: '#e4752a', bg: '#ffe3c9', acc: 'none' },
      { name: 'Captain Nash', role: 'Security Chief', skin: '#c68a5b', hair: 'short', hairColor: '#1d1d1d', color: '#24406e', bg: '#d6e2f7', acc: 'cap' }
    ],
    places: ['Star Theater', 'Telescope Deck', 'Gift Shop', 'Meteorite Hall', 'Control Booth', 'Rooftop Garden'],
    methods: ['Rolled up in a poster tube', 'Hidden in a telescope case', 'Slipped under a seat cushion', 'Packed in a moon-rock box', 'Tucked inside a rocket model', 'Lowered off the roof on a rope'],
    culprit: { p: 1, l: 4, m: 4 },
    ending: 'When the lights went out, <b>Orion Blake</b> left the microphone running a recording, slipped into the <b>Control Booth</b>, rolled up the Star Map and hid it <b>inside a rocket model</b> headed for the gift shop. Every alibi and every cleared method pointed straight at him. Case closed, Orion!',
    questions: [
      { instr: 'Simplify:', tex: 'x^3 \\cdot x^4', answer: { t: 'expr', v: 'x^7', simplified: true }, check: { expr: 'x**3*x**4', is: 'x**7' },
        steps: ['Same base: add the exponents.', '⟨x^{3+4} = x^7⟩'], clue: { p: 0, l: 1, text: 'Dr. Vega was on the Telescope Deck the whole show. Three visitors were looking through her telescope.' } },
      { instr: 'Simplify:', tex: '(x^2)^5', answer: { t: 'expr', v: 'x^10', simplified: true }, check: { expr: '(x**2)**5', is: 'x**10' },
        steps: ['Power of a power: multiply the exponents.', '⟨x^{2 \\cdot 5} = x^{10}⟩'], clue: { m: 0, text: 'The only poster tube in the building held a poster of Saturn. Nothing else.' } },
      { instr: 'Simplify:', tex: '(2x^3)^2', answer: { t: 'expr', v: '4x^6', simplified: true }, check: { expr: '(2*x**3)**2', is: '4*x**6' },
        steps: ['Square each factor: ⟨2^2 \\cdot (x^3)^2⟩', '⟨= 4x^6⟩'], clue: { p: 2, l: 0, text: 'Luna Reyes was fixing the star projector in the Star Theater. The audience watched her the whole time.' } },
      { instr: 'Evaluate:', tex: '5^0 + 2^{-3} \\cdot 8', answer: { t: 'num', v: '2' }, check: { num: '5**0+2**-3*8', is: 2 },
        steps: ['⟨5^0 = 1⟩ and ⟨2^{-3} = \\tfrac{1}{8}⟩', '⟨1 + \\tfrac{1}{8} \\cdot 8 = 1 + 1 = 2⟩'], clue: { m: 1, text: 'Every telescope case was locked, and Captain Nash has the only key. All empty.' } },
      { instr: 'Simplify. Use a positive exponent.', tex: '\\dfrac{x^9}{x^4}', answer: { t: 'expr', v: 'x^5', simplified: true, posExp: true }, check: { expr: 'x**9/x**4', is: 'x**5' },
        steps: ['Same base: subtract the exponents.', '⟨x^{9-4} = x^5⟩'], clue: { p: 3, l: 2, text: 'Mr. Halley was selling glow-in-the-dark stars in the Gift Shop. The register printed a receipt every few minutes.' } },
      { instr: 'Write 0.00042 in scientific notation as ⟨4.2 \\times 10^{n}⟩. What is ⟨n⟩?', text: '0.00042 = 4.2 × 10ⁿ', answer: { t: 'num', v: '-4' }, check: { num: 'Math.round(Math.log10(0.00042/4.2))', is: -4 },
        steps: ['Move the decimal 4 places right to get 4.2.', 'A small number has a negative exponent: ⟨n = -4⟩'], clue: { m: 2, text: 'The seat cushions are sewn shut. A thick paper map would have made a lump everyone could see.' } },
      { instr: 'Simplify:', tex: '\\dfrac{6x^5}{2x^2}', answer: { t: 'expr', v: '3x^3', simplified: true, posExp: true }, check: { expr: '6*x**5/(2*x**2)', is: '3*x**3' },
        steps: ['Divide the numbers: ⟨6 \\div 2 = 3⟩', 'Subtract the exponents: ⟨x^{5-2} = x^3⟩', '⟨3x^3⟩'], clue: { p: 4, l: 3, text: 'Stella Park was guiding a school group through Meteorite Hall. Twenty kids were with her.' } },
      { instr: 'Evaluate:', tex: '(-2)^4 - 2^4', answer: { t: 'num', v: '0' }, check: { num: '(-2)**4-2**4', is: 0 },
        steps: ['⟨(-2)^4 = 16⟩ (the negative is inside the parentheses)', '⟨2^4 = 16⟩, so ⟨16 - 16 = 0⟩'], clue: { m: 3, text: 'The moon-rock boxes are glass. You can see straight through them.' } },
      { instr: 'Multiply. Give the answer as a number in standard form.', tex: '(3 \\times 10^4)(2 \\times 10^2)', answer: { t: 'num', v: '6000000' }, check: { num: '3e4*2e2', is: 6000000 },
        steps: ['Multiply the numbers: ⟨3 \\cdot 2 = 6⟩', 'Add the exponents: ⟨10^{4+2} = 10^6⟩', '⟨6 \\times 10^6 = 6{,}000{,}000⟩'], clue: { p: 5, l: 5, text: 'Captain Nash was checking the fire exits in the Rooftop Garden. The door camera recorded him.' } },
      { instr: 'How many times larger is ⟨8 \\times 10^6⟩ than ⟨2 \\times 10^2⟩?', text: 'Divide: ⟨\\dfrac{8 \\times 10^6}{2 \\times 10^2}⟩', answer: { t: 'num', v: '40000' }, check: { num: '8e6/2e2', is: 40000 },
        steps: ['⟨8 \\div 2 = 4⟩ and ⟨10^{6-2} = 10^4⟩', '⟨4 \\times 10^4 = 40{,}000⟩ times larger'], clue: { m: 5, text: 'The roof hatch was bolted for the storm. No rope could have gone over the edge.' } }
    ]
  },

  escape: {
    title: 'Escape the Rocket Lab', emoji: '🚀', endEmoji: '🚀🌕',
    intro: 'Your class is touring the Rocket Lab when the launch computer locks every door for countdown! The only way out is to solve the lab’s power puzzles, unlock five rooms, and reach the exit in <b>30 minutes</b>, before liftoff.',
    finalStory: 'The exit hatch has a five-letter keypad. A note on the wall says: “Line up your key cards from the smallest stamp to the largest. The letters spell the password.”',
    finalAsk: 'Password?', word: 'ORBIT',
    outro: 'ORBIT! The hatch hisses open. Behind you the countdown stops, and the flight director gives you a salute: “Mission accomplished, crew.”',
    stages: [
      { name: 'The Fuel Panel', type: 'fields', stamp: 45, letter: 'B',
        story: 'The fuel gauges are labeled with powers. Enter two readings to start the pumps.',
        scene: { kind: 'svg', viewBox: '0 0 400 300', svg: '<rect x="90" y="60" width="220" height="150" rx="14" fill="#1b2150" stroke="#ffc857" stroke-width="3"/><text x="200" y="100" text-anchor="middle" fill="#fff" font-size="18">FUEL PANEL</text><text x="150" y="160" text-anchor="middle" fill="#ffc857" font-size="30" font-weight="700">2⁵</text><text x="250" y="160" text-anchor="middle" fill="#ffc857" font-size="30" font-weight="700">(−3)²</text><text x="200" y="260" text-anchor="middle" font-size="48">⛽</text>' },
        title: 'Fuel Readings', prompt: '<p>Evaluate each power.</p>', fields: [{ label: '2⁵ =', answer: 32 }, { label: '(−3)² =', answer: 9 }], button: 'Start the pumps',
        hints: ['2⁵ means 2 · 2 · 2 · 2 · 2.', 'A negative number squared is positive.', '2⁵ = 32 and (−3)² = 9.'], key: '2⁵ = 32, (−3)² = 9.', check: [['2**5', 32], ['(-3)**2', 9]] },
      { name: 'Mission Control', type: 'cipher', stamp: 12, letter: 'O',
        story: 'A coded message scrolls across the main screen. The shift is written somewhere in this room. Click things to search.',
        scene: { kind: 'emoji', bg: '#0f1830', floor: '#1f2b45', items: [{ e: '🖥️', x: 90, y: 150, s: 60, msg: 'The countdown clock: T-minus 29 minutes.' }, { e: '📓', x: 300, y: 200, s: 50, clue: 'Flight log:<br>Shift = 5⁰ + 2²', msg: 'A flight log with a note in it!' }, { e: '🎧', x: 200, y: 215, s: 42, msg: 'Headsets. Someone left in a hurry.' }, { e: '🛰️', x: 220, y: 105, s: 46, msg: 'A model satellite. Not a clue.' }] },
        plain: 'THE NEXT KEY IS IN THE AIRLOCK', shift: 5, answer: 'AIRLOCK', askLabel: 'Where is the next key?',
        hints: ['Click the flight log.', 'Any number (except 0) to the zero power is 1.', '1 + 4 = 5. Set the shift to 5.'], key: 'Shift = 5⁰ + 2² = 1 + 4 = 5. The message says THE NEXT KEY IS IN THE AIRLOCK.', checkNum: ['5**0+2**2', 5] },
      { name: 'The Airlock', type: 'classify', stamp: 91, letter: 'T',
        story: 'The airlock checks four exponent rules before it opens. Mark each one true or false.',
        scene: { kind: 'emoji', bg: '#172033', floor: '#2d3a52', items: [{ e: '🚪', x: 200, y: 175, s: 110, msg: 'The inner airlock door.' }, { e: '🧑‍🚀', x: 320, y: 185, s: 60, msg: 'A space suit hanging on a hook.' }], caption: 'true or false?' },
        title: 'True or false?', prompt: '<p style="color:var(--dim)">Check each statement with the exponent rules.</p>',
        items: ['2³ · 2⁴ = 2⁷', '(x²)³ = x⁵', 'x⁰ = 1 (when x ≠ 0)', '3⁻² = −9'], options: ['True', 'False'], answer: [0, 1, 0, 1],
        hints: ['Multiply same bases: add exponents. Power of a power: multiply exponents.', '(x²)³ = x⁶, not x⁵.', '3⁻² = 1/9, not −9.'], key: 'True, false (x⁶), true, false (1/9).' },
      { name: 'The Engine Room', type: 'order', stamp: 27, letter: 'R',
        story: 'The engine computer multiplies (4 × 10³)(6 × 10⁵). Put its steps in order to restart the engines.',
        scene: { kind: 'emoji', bg: '#26160f', floor: '#4a2c1c', items: [{ e: '⚙️', x: 120, y: 170, s: 70, msg: 'Gears turning slowly.' }, { e: '🔥', x: 290, y: 175, s: 56, msg: 'The engine glow.' }], caption: 'put the steps in order' },
        title: 'Multiply in scientific notation', prompt: '<div class="eq">(4 × 10³)(6 × 10⁵)</div><p>Place the steps from first to last.</p>',
        steps: ['Multiply the numbers: 4 × 6 = 24', 'Add the exponents: 10³ · 10⁵ = 10⁸', 'Write the product: 24 × 10⁸', 'Make the first number between 1 and 10: 2.4 × 10⁹'],
        hints: ['Group the numbers and the powers of 10.', 'Same base 10: add the exponents.', '24 is too big for scientific notation, so finish by adjusting it.'], key: '4 × 6 = 24; 10³ · 10⁵ = 10⁸; 24 × 10⁸ = 2.4 × 10⁹.', checkExpr: ['4e3*6e5', '2.4e9'] },
      { name: 'The Launch Hatch', type: 'fields', stamp: 68, letter: 'I', ui: 'dial',
        story: 'Two dials control the hatch. Dial A is the exponent n in 37,000 = 3.7 × 10ⁿ. Dial B is the exponent k in x⁹ ÷ x³ = xᵏ.',
        scene: { kind: 'emoji', bg: '#20160e', floor: '#3a2a1a', items: [{ e: '🛞', x: 200, y: 180, s: 110, msg: 'A heavy hatch with two dials.' }], caption: 'dial A, then dial B' },
        title: 'The Hatch Dials', prompt: '<div class="eq">37,000 = 3.7 × 10ⁿ &nbsp; &nbsp; x⁹ ÷ x³ = xᵏ</div><p>A = n, B = k.</p>', fields: [{ label: 'A', answer: 4 }, { label: 'B', answer: 6 }], button: 'Open the hatch',
        hints: ['Count how many places the decimal moves to get from 37,000 to 3.7.', 'It moves 4 places, so n = 4.', 'Dividing same bases: subtract the exponents, 9 − 3.'], key: 'A = 4 (37,000 = 3.7 × 10⁴), B = 6 (x⁹ ÷ x³ = x⁶).', check: [['Math.round(Math.log10(37000/3.7))', 4], ['9-3', 6]] }
    ]
  },

  cheat: {
    focus: 'exponent rules, zero and negative exponents, and evaluating powers',
    morefocus: 'scientific notation and operations with it',
    front: [
      { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
        ['base', 'The number being multiplied.', '⟨5⟩ in ⟨5^3⟩'], ['exponent', 'How many times the base is a factor.', '⟨3⟩ in ⟨5^3⟩'],
        ['power', 'A base with an exponent.', '⟨5^3 = 125⟩'], ['coefficient', 'The number in front of a variable.', '⟨4⟩ in ⟨4x^2⟩'],
        ['monomial', 'A number, variable, or product of them.', '⟨-3x^2y⟩']] },
      { title: 'The Exponent Rules', color: 'blue', kind: 'table', head: ['Rule', 'In symbols', 'Example'], rows: [
        ['Product', '⟨x^a \\cdot x^b = x^{a+b}⟩', '⟨x^3 \\cdot x^4 = x^7⟩'], ['Quotient', '⟨\\dfrac{x^a}{x^b} = x^{a-b}⟩', '⟨\\dfrac{x^9}{x^4} = x^5⟩'], ['Power', '⟨(x^a)^b = x^{ab}⟩', '⟨(x^2)^5 = x^{10}⟩'],
        ['Product to a power', '⟨(xy)^a = x^a y^a⟩', '⟨(2x)^3 = 8x^3⟩'], ['Zero', '⟨x^0 = 1⟩', '⟨7^0 = 1⟩'], ['Negative', '⟨x^{-a} = \\dfrac{1}{x^a}⟩', '⟨2^{-3} = \\tfrac{1}{8}⟩']] },
      { title: 'Power of a Product', color: 'green', kind: 'example', text: 'Raise EVERY factor inside the parentheses to the power, including the number.',
        example: 'Simplify ⟨(3x^4)^2⟩.', steps: [['Each factor:', '⟨3^2 \\cdot (x^4)^2⟩'], ['Simplify:', '⟨9x^8⟩']], answer: '⟨9x^8⟩' },
      { title: 'Negative Exponents', color: 'orange', kind: 'example', text: 'A negative exponent means “one over.” Move the factor across the fraction bar and make the exponent positive.',
        example: 'Simplify ⟨\\dfrac{4x^{-2}}{x^3}⟩.', steps: [['Move ⟨x^{-2}⟩ to the bottom:', '⟨\\dfrac{4}{x^2 \\cdot x^3}⟩'], ['Add exponents:', '⟨\\dfrac{4}{x^5}⟩']], answer: '⟨\\dfrac{4}{x^5}⟩' },
      { title: 'Evaluating Powers', color: 'pink', kind: 'example', text: 'Watch the parentheses: the exponent applies only to what it touches.',
        example: 'Compare ⟨(-3)^2⟩ and ⟨-3^2⟩.', steps: [['⟨(-3)^2⟩:', '⟨(-3)(-3) = 9⟩'], ['⟨-3^2⟩:', '⟨-(3 \\cdot 3) = -9⟩']], answer: '⟨9⟩ and ⟨-9⟩' },
      { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
        good: ['Multiply same bases: ADD exponents.', 'Power of a power: MULTIPLY exponents.', 'Any nonzero number to the zero power is 1.'],
        bad: [['⟨x^3 \\cdot x^4 \\ne x^{12}⟩', 'add, do not multiply'], ['⟨2^{-3} \\ne -8⟩', 'it is ⟨\\tfrac{1}{8}⟩'], ['⟨(2x)^3 \\ne 2x^3⟩', 'cube the 2 too: ⟨8x^3⟩']] }
    ],
    back: [
      { title: 'Scientific Notation', color: 'green', kind: 'example', text: 'A number between 1 and 10, times a power of 10: ⟨a \\times 10^n⟩ with ⟨1 \\le a < 10⟩.',
        example: 'Write ⟨0.00056⟩ in scientific notation.', steps: [['Move the decimal:', '4 places right gives ⟨5.6⟩'], ['Small number:', 'negative exponent']], answer: '⟨5.6 \\times 10^{-4}⟩' },
      { title: 'Big or Small?', color: 'purple', kind: 'table', head: ['Standard form', 'Scientific notation'], rows: [
        ['⟨4{,}500{,}000⟩', '⟨4.5 \\times 10^6⟩'], ['⟨72{,}000⟩', '⟨7.2 \\times 10^4⟩'], ['⟨0.03⟩', '⟨3 \\times 10^{-2}⟩'], ['⟨0.000801⟩', '⟨8.01 \\times 10^{-4}⟩']],
        after: 'Big numbers (10 or more) have positive exponents; numbers less than 1 have negative exponents.' },
      { title: 'Multiplying', color: 'blue', kind: 'example', text: 'Multiply the numbers, add the exponents, then adjust so the number is between 1 and 10.',
        example: '⟨(4 \\times 10^3)(6 \\times 10^5)⟩', steps: [['Numbers:', '⟨4 \\cdot 6 = 24⟩'], ['Powers:', '⟨10^{3+5} = 10^8⟩'], ['Adjust:', '⟨24 \\times 10^8 = 2.4 \\times 10^9⟩']], answer: '⟨2.4 \\times 10^9⟩' },
      { title: 'Dividing', color: 'orange', kind: 'example', text: 'Divide the numbers, subtract the exponents, then adjust.',
        example: '⟨\\dfrac{3 \\times 10^2}{6 \\times 10^7}⟩', steps: [['Numbers:', '⟨3 \\div 6 = 0.5⟩'], ['Powers:', '⟨10^{2-7} = 10^{-5}⟩'], ['Adjust:', '⟨0.5 \\times 10^{-5} = 5 \\times 10^{-6}⟩']], answer: '⟨5 \\times 10^{-6}⟩' },
      { title: 'Powers of 10', color: 'pink', kind: 'table', head: ['Power', 'Value'], rows: [
        ['⟨10^3⟩', '⟨1{,}000⟩'], ['⟨10^1⟩', '⟨10⟩'], ['⟨10^0⟩', '⟨1⟩'], ['⟨10^{-1}⟩', '⟨0.1⟩'], ['⟨10^{-3}⟩', '⟨0.001⟩']] },
      { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
        'Did I add exponents when multiplying and subtract when dividing?', 'Is my coefficient between 1 and 10?', 'Did I raise the number in front to the power too?', 'Are all my exponents positive in the final answer?'] }
    ]
  }
};
