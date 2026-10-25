/* Unit 1 · Foundations of Algebra: content for the unit pack (mystery online + printable, escape room, stations,
   cheat sheet). Build: node scripts/unit-packs/build.cjs foundations-algebra
   Math in ⟨…⟩ is TeX. `check` entries are verified by the builder (numbers by evaluation, expressions by
   comparing values at several points), so a typo in an answer stops the build. */
'use strict';
module.exports = {
  unit: 'foundations-algebra', unitNo: 1, unitName: 'Foundations of Algebra', course: 'Algebra 1',
  short: 'Foundations of Algebra',

  /* ======================= MYSTERY (online + printable) ======================= */
  mystery: {
    skills: 'order of operations, evaluating expressions, combining like terms, the distributive property, and writing expressions from words.',
    slug: 'midnight-library-mystery', title: 'The Midnight Library Mystery', eyebrow: 'Case file No. 1',
    tagline: 'A priceless atlas vanished during Family Game Night. Solve each problem to earn a clue.',
    palette: { navy: '#1f2a4d', accent: '#f2c14e' },
    labels: { p: 'The Suspects', l: 'The Places', m: 'The Methods' },
    intro: [
      'It was Family Game Night at the Westbrook Public Library when the lights flickered. When they came back on, the glass case in the lobby was empty: <b>The Map of Everything</b>, a 200-year-old atlas, was gone!',
      'Six people were in the building, each seen in a different room, and there are six sneaky ways to smuggle out a giant book. You are the lead detective. Find out <b>who</b> took it, <b>where</b> they were, and <b>how</b> they got it away.'
    ],
    suspects: [
      { name: 'Mr. Patel', role: 'Head Librarian', skin: '#c68a5b', hair: 'short', hairColor: '#1d1d1d', color: '#24406e', bg: '#d6e2f7', acc: 'glasses' },
      { name: 'Ms. Greene', role: 'Book Club Leader', skin: '#f4d3b5', hair: 'long', hairColor: '#7a4a21', color: '#2a7f6f', bg: '#d3f1ea', acc: 'none' },
      { name: 'Officer Ruiz', role: 'Night Guard', skin: '#e0ac7e', hair: 'short', hairColor: '#2a1a12', color: '#1f2a4d', bg: '#dfe3ee', acc: 'cap' },
      { name: 'Jada Brooks', role: 'Teen Volunteer', skin: '#8d5a3b', hair: 'bun', hairColor: '#15151a', color: '#7a3fb0', bg: '#e8d9f5', acc: 'none' },
      { name: 'Professor Hale', role: 'Visiting Author', skin: '#f1c9a5', hair: 'bald', hairColor: '#d9d9df', color: '#8a5a2b', bg: '#f1e4c9', acc: 'bowtie' },
      { name: 'Mr. Fox', role: 'Game Night Host', skin: '#d9a074', hair: 'short', hairColor: '#b5651d', color: '#c0392b', bg: '#fbdada', acc: 'none' }
    ],
    places: ['Front Desk', 'Reading Room', 'Rare Books Vault', 'Children’s Corner', 'Map Room', 'Computer Lab'],
    methods: ['Hidden in a book cart', 'Tucked in a backpack', 'Slipped into a board-game box', 'Rolled up in a poster tube', 'Swapped with a fake cover', 'Lowered out a window in a basket'],
    culprit: { p: 4, l: 4, m: 3 },
    ending: 'When the lights flickered, <b>Professor Hale</b> slipped into the <b>Map Room</b>, rolled the atlas into a <b>poster tube</b> labeled “Book Tour Posters,” and strolled toward the exit. Every alibi and every method you cleared pointed straight at him. Brilliant detective work!',
    /* clue: what the CORRECT answer reveals. Suspect clues also clear the place they were seen. */
    questions: [
      { instr: 'Evaluate:', tex: '18 - 2(3 + 4)', answer: { t: 'num', v: '4' }, check: { num: '18-2*(3+4)', is: 4 },
        steps: ['⟨2(7) = 14⟩', '⟨18 - 14 = 4⟩'], clue: { p: 0, l: 0, text: 'Mr. Patel was checking out books at the Front Desk the whole time. Twelve families saw him there.' },
        wrong: [['⟨112⟩', 'subtracted before multiplying'], ['⟨16⟩', 'multiplied only the 3 by 2'], ['⟨23⟩', 'ignored the multiplication']] },
      { instr: 'Evaluate:', tex: '3^2 + 4 \\cdot 5 - 6', answer: { t: 'num', v: '23' }, check: { num: '3**2+4*5-6', is: 23 },
        steps: ['⟨9 + 20 - 6⟩', '⟨= 23⟩'], clue: { m: 0, text: 'The book cart was searched at the door. It held only picture books.' },
        wrong: [['⟨20⟩', 'used 3² = 6'], ['⟨59⟩', 'worked left to right, adding before multiplying'], ['⟨5⟩', 'subtracted 5 − 6 first']] },
      { instr: 'Evaluate when x = 5:', tex: '4x - 7', answer: { t: 'num', v: '13' }, check: { num: '4*5-7', is: 13 },
        steps: ['⟨4(5) - 7⟩', '⟨20 - 7 = 13⟩'], clue: { p: 1, l: 1, text: 'Ms. Greene was leading a book club in the Reading Room. Her group never let her leave.' },
        wrong: [['⟨38⟩', 'read 4x as 45'], ['⟨-8⟩', 'subtracted before multiplying'], ['⟨27⟩', 'added 7 instead of subtracting']] },
      { instr: 'Evaluate when a = −3 and b = 4:', tex: 'a^2 - 2b', answer: { t: 'num', v: '1' }, check: { num: '(-3)**2-2*4', is: 1 },
        steps: ['⟨(-3)^2 - 2(4)⟩', '⟨9 - 8 = 1⟩'], clue: { m: 1, text: 'Every backpack was checked at the exit. No atlas would even fit.' },
        wrong: [['⟨-17⟩', 'used −3² = −9'], ['⟨-14⟩', 'used a² = 2a'], ['⟨17⟩', 'added instead of subtracting']] },
      { instr: 'Simplify:', tex: '5x + 3 - 2x + 8', answer: { t: 'expr', v: '3x+11', maxParens: 0 }, check: { expr: '5*x+3-2*x+8', is: '3*x+11' },
        steps: ['⟨(5x - 2x) + (3 + 8)⟩', '⟨3x + 11⟩'], clue: { p: 2, l: 2, text: 'Officer Ruiz was locked inside the Rare Books Vault doing inventory. The vault log shows the door never opened.' },
        wrong: [['⟨14x⟩', 'combined unlike terms'], ['⟨7x + 11⟩', 'added 2x instead of subtracting'], ['⟨3x + 5⟩', 'subtracted the 8']] },
      { instr: 'Simplify:', tex: '4(2x - 3)', answer: { t: 'expr', v: '8x-12', maxParens: 0 }, check: { expr: '4*(2*x-3)', is: '8*x-12' },
        steps: ['⟨4(2x) - 4(3)⟩', '⟨8x - 12⟩'], clue: { m: 2, text: 'The board-game boxes were all opened for Game Night. Nothing but game pieces inside.' },
        wrong: [['⟨8x - 3⟩', 'distributed to the first term only'], ['⟨6x - 7⟩', 'added 4 instead of multiplying'], ['⟨8x + 12⟩', 'sign error']] },
      { instr: 'Simplify:', tex: '3(x + 4) - 5x', answer: { t: 'expr', v: '-2x+12', maxParens: 0 }, check: { expr: '3*(x+4)-5*x', is: '-2*x+12' },
        steps: ['⟨3x + 12 - 5x⟩', '⟨-2x + 12⟩'], clue: { p: 3, l: 3, text: 'Jada Brooks was reading to toddlers in the Children’s Corner. A dozen parents took videos.' },
        wrong: [['⟨8x + 12⟩', 'added 3x and 5x'], ['⟨-2x + 4⟩', 'did not multiply the 4 by 3'], ['⟨2x + 12⟩', 'sign error']] },
      { instr: 'Write an expression:', text: '5 less than 3 times a number x', answer: { t: 'expr', v: '3x-5' }, check: { expr: '3*x-5', is: '3*x-5' },
        steps: ['3 times a number: ⟨3x⟩', '5 less than that: ⟨3x - 5⟩'], clue: { m: 4, text: 'The fake cover in the case is a decoy the library always uses. The real atlas was never swapped.' },
        wrong: [['⟨5 - 3x⟩', 'subtracted in the wrong order'], ['⟨3(x - 5)⟩', 'took 5 from x first'], ['⟨5x - 3⟩', 'switched the numbers']] },
      { instr: 'Evaluate:', tex: '|-8| + (-3)(4)', answer: { t: 'num', v: '-4' }, check: { num: 'Math.abs(-8)+(-3)*4', is: -4 },
        steps: ['⟨8 + (-12)⟩', '⟨= -4⟩'], clue: { p: 5, l: 5, text: 'Mr. Fox was running a trivia contest from the Computer Lab. The livestream never shows him leaving.' },
        wrong: [['⟨-20⟩', 'used |−8| = −8'], ['⟨20⟩', 'used (−3)(4) = 12'], ['⟨9⟩', 'added instead of multiplying']] },
      { instr: 'Simplify:', tex: '-2(3x - 5) + 7x', answer: { t: 'expr', v: 'x+10', maxParens: 0 }, check: { expr: '-2*(3*x-5)+7*x', is: 'x+10' },
        steps: ['⟨-6x + 10 + 7x⟩', '⟨x + 10⟩'], clue: { m: 5, text: 'All the windows are painted shut for the winter. Nothing went out in a basket.' },
        wrong: [['⟨x - 10⟩', 'sign error: −2 × −5 = +10'], ['⟨13x + 10⟩', 'sign error on 6x'], ['⟨x + 5⟩', 'did not multiply the 5 by −2']] }
    ],
    /* false clues for wrong choices (each clears something it should not) */
    falseClues: [
      'Professor Hale was signing books at the Front Desk the whole time.', 'The poster tubes were checked. Only posters inside.', 'Mr. Patel took a long break in the Map Room.',
      'Professor Hale never left the Reading Room.', 'Jada Brooks was seen hurrying out of the Map Room.', 'Officer Ruiz was patrolling the Computer Lab.',
      'A guard checked every poster tube at the door.', 'Ms. Greene was alone in the Map Room for ten minutes.', 'The Map Room was locked all evening.',
      'Mr. Fox carried a large backpack out to his car.', 'Professor Hale spent the night in the Children’s Corner.', 'Someone saw a book cart rolling toward the loading dock.',
      'Officer Ruiz left the vault to check the Map Room.', 'Professor Hale was in the Rare Books Vault with the guard.', 'The window basket was found sitting on the lawn.',
      'Jada Brooks had a poster tube under her arm.', 'Professor Hale was helping in the Computer Lab.', 'A board-game box felt much too heavy.',
      'Mr. Patel walked out with a very large backpack.', 'Professor Hale was reading in the Children’s Corner.', 'The fake cover had been swapped with the real one.',
      'Mr. Fox was spotted near the Map Room door.', 'Ms. Greene asked to borrow a poster tube.', 'Professor Hale never touched a poster tube.',
      'Officer Ruiz left the vault for an hour.', 'The poster tube was empty when security looked.', 'Jada Brooks left the Children’s Corner early.',
      'A basket was lowered from the Reading Room window.', 'Professor Hale was at the Front Desk with Mr. Patel.', 'Mr. Fox left the livestream for twenty minutes.'
    ]
  },

  /* ======================= ESCAPE ROOM ======================= */
  escape: {
    title: 'Night at the Number Museum', emoji: '🏛️', endEmoji: '☄️🏆',
    intro: 'You stayed too late on the field trip, and now the Number Museum is locked for the night! The night guard left a note: every gallery door opens with a math code. Crack all five galleries and reach the exit in <b>30 minutes</b>, before the alarms reset.',
    finalStory: 'The exit door has a five-letter keypad. A brass plate says: “Lay your key cards from the smallest stamp to the largest. The letters spell the password.”',
    finalAsk: 'Password?', word: 'COMET',
    outro: 'The keypad glows green: COMET! The exit slides open just as the alarms reset. The night guard waves from the lobby: “Not bad, mathematicians. See you on the next field trip.”',
    stages: [
      { name: 'The Order-of-Operations Gallery', type: 'fields', stamp: 41, letter: 'M',
        story: 'Two statues guard the first door. Each holds a sign with an expression. The door code is the value of each sign.',
        scene: { kind: 'svg', viewBox: '0 0 400 300', svg: '<rect x="30" y="60" width="150" height="110" rx="12" fill="#1b2150" stroke="#ffc857" stroke-width="3"/><text x="105" y="95" text-anchor="middle" fill="#fff" font-size="16">Sign A</text><text x="105" y="140" text-anchor="middle" fill="#ffc857" font-size="24" font-weight="700">6 + 4 · 3 − 2</text><rect x="220" y="60" width="150" height="110" rx="12" fill="#1b2150" stroke="#ffc857" stroke-width="3"/><text x="295" y="95" text-anchor="middle" fill="#fff" font-size="16">Sign B</text><text x="295" y="140" text-anchor="middle" fill="#ffc857" font-size="22" font-weight="700">(6 + 4) · 3 − 2</text><text x="200" y="240" text-anchor="middle" font-size="60">🗿</text>' },
        title: 'Statue Signs', prompt: '<p>Evaluate each sign. Remember the order of operations.</p>', fields: [{ label: 'Sign A =', answer: 16 }, { label: 'Sign B =', answer: 28 }], button: 'Open the door',
        hints: ['Multiply before you add or subtract (unless parentheses say otherwise).', 'Sign A: 4 · 3 = 12 first, then 6 + 12 − 2.', 'Sign B: do the parentheses first: 10 · 3 − 2.'],
        key: 'A: 6 + 12 − 2 = 16. B: 10 · 3 − 2 = 28.', check: [['6+4*3-2', 16], ['(6+4)*3-2', 28]] },
      { name: 'The Planet Hall', type: 'cipher', stamp: 12, letter: 'C',
        story: 'A scrambled message is painted on the ceiling. The shift is hidden somewhere in this hall. Click things to search.',
        scene: { kind: 'emoji', bg: '#0b0e2a', floor: '#1b1f3f', items: [{ e: '🪐', x: 90, y: 120, s: 64, msg: 'Saturn. Its rings are made of tiny hints.' }, { e: '🔭', x: 320, y: 205, s: 54, clue: 'Scratched on the telescope:<br>Shift = 5 + 2² − 2', msg: 'There is writing on the telescope!' }, { e: '☄️', x: 230, y: 90, s: 46, msg: 'A comet model. Very shiny.' }, { e: '🌍', x: 150, y: 210, s: 52, msg: 'Earth. You live here.' }] },
        plain: 'THE NEXT KEY IS BEHIND THE PLANETS', shift: 7, answer: 'PLANETS', askLabel: 'Where is the next key?',
        hints: ['Click the telescope.', 'Exponents before addition and subtraction: 2² = 4.', '5 + 4 − 2 = 7. Set the shift to 7.'],
        key: '5 + 4 − 2 = 7. Shift 7 decodes “THE NEXT KEY IS BEHIND THE PLANETS.” Answer: PLANETS.', checkNum: ['5+2**2-2', 7] },
      { name: 'The Hall of Properties', type: 'classify', stamp: 87, letter: 'T',
        story: 'Four plaques describe famous number rules, but the labels fell off. Put each plaque back under the right property.',
        scene: { kind: 'emoji', bg: '#1d1530', floor: '#3a2b4a', items: [{ e: '🏺', x: 80, y: 170, s: 60 }, { e: '🖼️', x: 170, y: 150, s: 56 }, { e: '📜', x: 250, y: 160, s: 50 }, { e: '🗝️', x: 330, y: 170, s: 50 }], caption: 'four plaques, four properties' },
        title: 'Which property?', prompt: '<p style="color:var(--dim)">Choose the property each plaque shows.</p>',
        items: ['3 + 8 = 8 + 3', '(2 · 5) · 4 = 2 · (5 · 4)', '6(x + 2) = 6x + 12', 'x + 0 = x'], options: ['Commutative', 'Associative', 'Distributive', 'Identity'], answer: [0, 1, 2, 3],
        hints: ['Commutative = the ORDER changes. Associative = the GROUPING changes.', 'Distributive: a number multiplies each term inside parentheses.', 'Adding 0 leaves a number the same: that is the identity property.'],
        key: 'Commutative, Associative, Distributive, Identity.' },
      { name: 'The Sculpture Garden', type: 'order', stamp: 23, letter: 'O',
        story: 'A sculpture opens only when the steps to simplify 4(x + 3) − 2(x − 1) are shown in the right order. The guard scrambled them!',
        scene: { kind: 'emoji', bg: '#13261c', floor: '#2c4a2c', items: [{ e: '🗿', x: 120, y: 170, s: 80, msg: 'The sculpture stares at you.' }, { e: '🌳', x: 290, y: 170, s: 70, msg: 'A tree. Not a math tree.' }], caption: 'put the steps in order' },
        title: 'Simplify in Order', prompt: '<div class="eq">4(x + 3) − 2(x − 1)</div><p>Place the steps from first to last.</p>',
        steps: ['Distribute: 4x + 12 − 2x + 2', 'Group like terms: (4x − 2x) + (12 + 2)', 'Combine like terms: 2x + 14', 'Check with x = 1: 4(4) − 2(0) = 16 and 2(1) + 14 = 16'],
        hints: ['Clear the parentheses first.', 'Watch the sign: −2 times −1 is +2.', 'After grouping, combine. Checking goes last.'],
        key: 'Distribute (4x + 12 − 2x + 2), group, combine (2x + 14), check.', checkExpr: ['4*(x+3)-2*(x-1)', '2*x+14'] },
      { name: 'The Exit Vault', type: 'fields', stamp: 55, letter: 'E', ui: 'dial',
        story: 'The last vault has two dials. A plate says: “Use x = 2 and y = 3.”',
        scene: { kind: 'emoji', bg: '#20160e', floor: '#3a2a1a', items: [{ e: '🚪', x: 200, y: 180, s: 120, msg: 'A heavy vault door with two dials.' }], caption: 'dial A, then dial B' },
        title: 'The Brass Plate', prompt: '<div class="eq">A = x² + y</div><br><div class="eq">B = 2y − x</div><p>Use x = 2 and y = 3. Each dial is a single digit.</p>', fields: [{ label: 'A', answer: 7 }, { label: 'B', answer: 4 }], button: 'Turn the handle',
        hints: ['Replace x with 2 and y with 3 in each expression.', 'A = 2² + 3.', 'B = 2(3) − 2.'],
        key: 'A = 4 + 3 = 7. B = 6 − 2 = 4.', check: [['2**2+3', 7], ['2*3-2', 4]] }
    ]
  },

  /* ======================= STATIONS ======================= */
  stations: [
    { title: 'Order of Operations and Evaluating Expressions', note: 'Show your work. Simplify completely.',
      items: [
        ['Evaluate: ⟨12 - 3 \\cdot 2 + 5⟩', '⟨11⟩', { num: '12-3*2+5', is: 11 }],
        ['Evaluate: ⟨(8 + 4) \\div 3 \\cdot 2⟩', '⟨8⟩', { num: '(8+4)/3*2', is: 8 }],
        ['Evaluate: ⟨5 + 2^3 - 4⟩', '⟨9⟩', { num: '5+2**3-4', is: 9 }],
        ['Evaluate: ⟨36 \\div (2 + 4) - 1⟩', '⟨5⟩', { num: '36/(2+4)-1', is: 5 }],
        ['Evaluate: ⟨2[10 - (3 + 4)]⟩', '⟨6⟩', { num: '2*(10-(3+4))', is: 6 }],
        ['Evaluate: ⟨\\dfrac{15 - 3^2}{2 \\cdot 3}⟩', '⟨1⟩', { num: '(15-3**2)/(2*3)', is: 1 }],
        ['Evaluate ⟨3x + 4⟩ for ⟨x = -2⟩.', '⟨-2⟩', { num: '3*(-2)+4', is: -2 }],
        ['Evaluate ⟨x^2 - 5x⟩ for ⟨x = 3⟩.', '⟨-6⟩', { num: '3**2-5*3', is: -6 }],
        ['Evaluate ⟨\\dfrac{a + b}{2}⟩ for ⟨a = 7⟩ and ⟨b = -1⟩.', '⟨3⟩', { num: '(7+(-1))/2', is: 3 }],
        ['Evaluate ⟨2m^2 - n⟩ for ⟨m = -3⟩ and ⟨n = 5⟩.', '⟨13⟩', { num: '2*(-3)**2-5', is: 13 }]] },
    { title: 'Real Numbers and Properties', note: 'List every set each number belongs to: natural, whole, integer, rational, irrational. Then name each property.',
      items: [
        ['Classify ⟨-6⟩.', 'integer, rational'],
        ['Classify ⟨0⟩.', 'whole, integer, rational'],
        ['Classify ⟨\\sqrt{49}⟩.', 'natural, whole, integer, rational (it equals 7)'],
        ['Classify ⟨\\tfrac{2}{3}⟩.', 'rational'],
        ['Classify ⟨\\sqrt{10}⟩.', 'irrational'],
        ['Classify ⟨-0.25⟩.', 'rational'],
        ['Name the property: ⟨7 + 9 = 9 + 7⟩', 'commutative property of addition'],
        ['Name the property: ⟨(3 \\cdot 4) \\cdot 5 = 3 \\cdot (4 \\cdot 5)⟩', 'associative property of multiplication'],
        ['Name the property: ⟨8 + 0 = 8⟩', 'identity property of addition'],
        ['Name the property: ⟨5(x - 2) = 5x - 10⟩', 'distributive property']] },
    { title: 'Combining Like Terms and the Distributive Property', note: 'Simplify each expression.',
      items: [
        ['⟨7x + 3x⟩', '⟨10x⟩', { expr: '7*x+3*x', is: '10*x' }],
        ['⟨4a - 9 + 2a + 5⟩', '⟨6a - 4⟩', { expr: '4*x-9+2*x+5', is: '6*x-4' }],
        ['⟨3y^2 + 2y - y^2 + 6y⟩', '⟨2y^2 + 8y⟩', { expr: '3*x**2+2*x-x**2+6*x', is: '2*x**2+8*x' }],
        ['⟨5(x + 6)⟩', '⟨5x + 30⟩', { expr: '5*(x+6)', is: '5*x+30' }],
        ['⟨-3(2n - 4)⟩', '⟨-6n + 12⟩', { expr: '-3*(2*x-4)', is: '-6*x+12' }],
        ['⟨2(3x + 1) + 4x⟩', '⟨10x + 2⟩', { expr: '2*(3*x+1)+4*x', is: '10*x+2' }],
        ['⟨6 - (x + 4)⟩', '⟨-x + 2⟩', { expr: '6-(x+4)', is: '-x+2' }],
        ['⟨4(2a - 1) - 3(a + 5)⟩', '⟨5a - 19⟩', { expr: '4*(2*x-1)-3*(x+5)', is: '5*x-19' }],
        ['⟨\\tfrac{1}{2}(8x - 6) + 3⟩', '⟨4x⟩', { expr: '(8*x-6)/2+3', is: '4*x' }],
        ['⟨3(2x - y) - 2(x + 4y)⟩', '⟨4x - 11y⟩', { expr: '3*(2*x-y)-2*(x+4*y)', is: '4*x-11*y' }]] },
    { title: 'Words to Expressions and Applications', note: 'Write an expression. When a value is given, evaluate.',
      items: [
        ['The sum of a number ⟨n⟩ and 9', '⟨n + 9⟩'],
        ['7 less than a number ⟨x⟩', '⟨x - 7⟩'],
        ['The product of 6 and a number ⟨y⟩', '⟨6y⟩'],
        ['Twice a number ⟨x⟩, decreased by 5', '⟨2x - 5⟩'],
        ['The quotient of a number ⟨m⟩ and 4, increased by 1', '⟨\\tfrac{m}{4} + 1⟩'],
        ['Three times the sum of a number ⟨x⟩ and 2', '⟨3(x + 2)⟩'],
        ['A movie ticket costs $12 and popcorn costs $5. Write an expression for the cost of ⟨t⟩ tickets and one popcorn.', '⟨12t + 5⟩'],
        ['Use your expression from #7 to find the cost of 4 tickets and one popcorn.', '$53', { num: '12*4+5', is: 53 }],
        ['A rectangle is ⟨x + 3⟩ long and 4 wide. Write and simplify an expression for its perimeter.', '⟨2(x + 3) + 2(4) = 2x + 14⟩', { expr: '2*(x+3)+2*4', is: '2*x+14' }],
        ['A phone plan costs $20 plus $0.10 per text. Write an expression for ⟨t⟩ texts, then find the cost of 150 texts.', '⟨20 + 0.10t⟩; $35', { num: '20+0.10*150', is: 35 }]] }
  ],

  /* ======================= CHEAT SHEET ======================= */
  cheat: {
    focus: 'variables, order of operations, real numbers, properties and simplifying',
    morefocus: 'like terms, the distributive property, words to algebra and integers',
    front: [
      { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
        ['variable', 'A letter that stands for a number.', '⟨x,\\ y,\\ n⟩'], ['expression', 'Numbers, variables and operations (no equal sign).', '⟨3x - 5⟩'],
        ['term', 'A part of an expression separated by + or −.', 'In ⟨4x + 7 - 2y⟩: ⟨4x,\\ 7,\\ -2y⟩'], ['coefficient', 'The number multiplying a variable.', 'In ⟨5x⟩, it is 5.'],
        ['constant', 'A term with no variable.', '⟨7,\\ -3,\\ 12⟩'], ['like terms', 'Same variables raised to the same powers.', '⟨3x⟩ and ⟨-5x⟩']] },
      { title: 'Order of Operations (PEMDAS)', color: 'blue', kind: 'pemdas',
        example: '⟨3 + 4(2^2 - 5)⟩', steps: [['Parentheses (exponent inside):', '⟨2^2 - 5 = 4 - 5 = -1⟩'], ['Multiply:', '⟨4(-1) = -4⟩'], ['Add:', '⟨3 + (-4) = -1⟩']], answer: '⟨-1⟩' },
      { title: 'Evaluating Expressions', color: 'green', kind: 'example', text: 'Substitute the value for the variable (use parentheses!), then follow PEMDAS.',
        example: 'Evaluate ⟨x^2 - 3x⟩ when ⟨x = -2⟩.', steps: [['Substitute:', '⟨(-2)^2 - 3(-2)⟩'], ['Simplify:', '⟨4 + 6⟩']], answer: '⟨10⟩' },
      { title: 'The Real Numbers', color: 'orange', kind: 'sets' },
      { title: 'Properties', color: 'pink', kind: 'props', rows: [
        ['Commutative', 'order changes', '⟨a + b = b + a⟩', '⟨ab = ba⟩'], ['Associative', 'grouping changes', '⟨(a + b) + c = a + (b + c)⟩', '⟨(ab)c = a(bc)⟩'],
        ['Identity', 'nothing changes', '⟨a + 0 = a⟩', '⟨a \\cdot 1 = a⟩'], ['Inverse', 'back to 0 or 1', '⟨a + (-a) = 0⟩', '⟨a \\cdot \\tfrac{1}{a} = 1⟩'],
        ['Distributive', 'multiply every term', '⟨a(b + c) = ab + ac⟩', '']] },
      { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
        good: ['Do parentheses and exponents first.', 'Multiply/divide left to right, then add/subtract left to right.', 'Put substituted negatives in parentheses.', 'Combine only like terms.'],
        bad: [['⟨-3^2⟩ is not ⟨9⟩', '⟨-3^2 = -9⟩, but ⟨(-3)^2 = 9⟩'], ['⟨3x + 2x \\ne 5x^2⟩', 'it is ⟨5x⟩'], ['⟨4(x + 2) \\ne 4x + 2⟩', 'it is ⟨4x + 8⟩']] }
    ],
    back: [
      { title: 'Combining Like Terms', color: 'green', kind: 'example', text: 'Add or subtract the coefficients of like terms. Keep the variable part the same.',
        example: 'Simplify ⟨6x + 4 - 2x + 9⟩.', steps: [['Group:', '⟨(6x - 2x) + (4 + 9)⟩'], ['Combine:', '⟨4x + 13⟩']], answer: '⟨4x + 13⟩' },
      { title: 'Distributive Property', color: 'purple', kind: 'example', text: 'Multiply the number outside by EVERY term inside the parentheses.',
        example: 'Simplify ⟨-3(2x - 5) + x⟩.', steps: [['Distribute:', '⟨-6x + 15 + x⟩'], ['Combine:', '⟨-5x + 15⟩']], answer: '⟨-5x + 15⟩' },
      { title: 'Words to Algebra', color: 'blue', kind: 'words', rows: [
        ['sum, plus, more than, increased by', '⟨+⟩'], ['difference, minus, less than, decreased by', '⟨-⟩'], ['product, times, twice, of', '⟨\\times⟩'], ['quotient, divided by, per', '⟨\\div⟩'],
        ['5 less than ⟨x⟩', '⟨x - 5⟩'], ['twice a number, plus 3', '⟨2n + 3⟩'], ['the sum of ⟨x⟩ and 4, times 3', '⟨3(x + 4)⟩']] },
      { title: 'Integers & Absolute Value', color: 'orange', kind: 'list', items: [
        'Same signs: add and keep the sign. ⟨-4 + (-6) = -10⟩', 'Different signs: subtract and keep the sign of the larger. ⟨-9 + 4 = -5⟩', 'Subtracting = adding the opposite. ⟨3 - (-5) = 3 + 5 = 8⟩',
        'Multiply/divide: same signs ⟨\\to⟩ positive, different signs ⟨\\to⟩ negative.', 'Absolute value is distance from 0: ⟨|-7| = 7⟩, ⟨|7| = 7⟩'] },
      { title: 'Putting It Together', color: 'pink', kind: 'example', text: 'Simplify, then evaluate.',
        example: 'Simplify ⟨2(x + 3) - 4x⟩, then evaluate for ⟨x = 5⟩.', steps: [['Distribute:', '⟨2x + 6 - 4x⟩'], ['Combine:', '⟨-2x + 6⟩'], ['Evaluate:', '⟨-2(5) + 6 = -4⟩']], answer: '⟨-4⟩' },
      { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
        'Did you distribute to every term?', 'Did you keep the sign in front of each term?', 'Are there any like terms left to combine?', 'Substitute a number into both forms: equal expressions give the same value.'] }
    ]
  }
};
