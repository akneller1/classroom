/* Unit 4 · Relations and Functions: unit pack content (see build.cjs). */
'use strict';
const T = (rows) => '<table>' + rows.map((r, i) => '<tr>' + r.map(c => (i ? '<td>' : '<th>') + c + (i ? '</td>' : '</th>')).join('') + '</tr>').join('') + '</table>';
module.exports = {
  unit: 'relations-functions', unitNo: 4, unitName: 'Relations and Functions', course: 'Algebra 1',

  mystery: {
    skills: 'evaluating functions, solving f(x) = k, domain and range, rate of change, and arithmetic sequences.',
    slug: 'arcade-token-heist', title: 'The Arcade Token Heist', eyebrow: 'Case file No. 4',
    tagline: 'The Grand Champion Joystick vanished from Pixel Palace Arcade. Solve each problem to earn a clue.',
    palette: { navy: '#2b1846', accent: '#3ee0c5' },
    labels: { p: 'The Suspects', l: 'The Places', m: 'The Methods' },
    placeholder: 'Your answer', inputHint: 'Type a number like -4. For a set, list the numbers with commas, like -1, 0, 2.', symbols: [],
    intro: [
      'It was tournament night at <b>Pixel Palace Arcade</b>. Just before the awards, the crowd gasped: the <b>Grand Champion Joystick</b>, a golden trophy worth a fortune in tokens, was gone from its glowing case!',
      'Six people were in the arcade, each seen in a different spot, and there are six sneaky ways to sneak out a trophy. You are the lead detective. Find out <b>who</b> took it, <b>where</b> they were, and <b>how</b> they got it away.'
    ],
    suspects: [
      { name: 'Max Rivera', role: 'Arcade Manager', skin: '#c68a5b', hair: 'short', hairColor: '#1d1d1d', color: '#24406e', bg: '#d6e2f7', acc: 'none' },
      { name: 'Lena Cho', role: 'Prize Counter Clerk', skin: '#f4d3b5', hair: 'long', hairColor: '#15151a', color: '#c0392b', bg: '#fbdada', acc: 'glasses' },
      { name: 'Coach Banks', role: 'Team Coach', skin: '#8d5a3b', hair: 'bald', hairColor: '#1d1d1d', color: '#1f7a4d', bg: '#d3f1ea', acc: 'cap' },
      { name: 'Priya Shah', role: 'Champion Gamer', skin: '#c68a5b', hair: 'bun', hairColor: '#2a1a12', color: '#7a3fb0', bg: '#e8d9f5', acc: 'none' },
      { name: 'Mr. Ortega', role: 'Maintenance Tech', skin: '#e0ac7e', hair: 'short', hairColor: '#5a3a22', color: '#8a5a2b', bg: '#f1e4c9', acc: 'cap' },
      { name: 'Zoe King', role: 'Birthday Guest', skin: '#f1c9a5', hair: 'long', hairColor: '#b5651d', color: '#e4752a', bg: '#ffe3c9', acc: 'bowtie' }
    ],
    places: ['Prize Counter', 'Pinball Alley', 'Racing Zone', 'Snack Bar', 'Back Office', 'Party Room'],
    methods: ['Hidden in a claw machine', 'Stuffed in a prize bag', 'Carried in a pizza box', 'Rolled out in a trash bin', 'Taped under a pinball table', 'Slipped down a skee-ball lane'],
    culprit: { p: 4, l: 4, m: 3 },
    ending: 'While everyone watched the final race, <b>Mr. Ortega</b> slipped into the <b>Back Office</b>, dropped the joystick into a <b>trash bin</b>, and rolled it out the back door with the evening garbage. Every alibi and every method you cleared pointed straight at him. Game over, Mr. Ortega!',
    questions: [
      { instr: 'If f(x) = 3x − 5, find:', tex: 'f(4)', answer: { t: 'num', v: '7' }, check: { num: '3*4-5', is: 7 },
        steps: ['⟨f(4) = 3(4) - 5⟩', '⟨= 7⟩'], clue: { p: 0, l: 0, text: 'Max Rivera was handing out prizes at the Prize Counter the whole night. The security camera shows him there.' },
        wrong: [['⟨29⟩', 'read 3x as 34'], ['⟨17⟩', 'added 5 instead of subtracting'], ['⟨-7⟩', 'sign error']] },
      { instr: 'If f(x) = x² + 2x, find:', tex: 'f(-3)', answer: { t: 'num', v: '3' }, check: { num: '(-3)**2+2*(-3)', is: 3 },
        steps: ['⟨(-3)^2 + 2(-3)⟩', '⟨9 - 6 = 3⟩'], clue: { m: 0, text: 'The claw machine was emptied for repairs this morning. Nothing inside but a lost sock.' },
        wrong: [['⟨-15⟩', 'used (−3)² = −9'], ['⟨15⟩', 'added 9 and 6'], ['⟨-3⟩', 'used (−3)² = −9 and +6']] },
      { instr: 'If g(x) = 2x + 1, find x when:', tex: 'g(x) = 15', answer: { t: 'num', v: '7' }, check: { num: '(15-1)/2', is: 7 },
        steps: ['⟨2x + 1 = 15⟩', '⟨2x = 14,\\ x = 7⟩'], clue: { p: 1, l: 1, text: 'Lena Cho was fixing a jammed machine in Pinball Alley. Three players waited for her.' },
        wrong: [['⟨31⟩', 'found g(15) instead'], ['⟨8⟩', 'added 1 before dividing'], ['⟨6⟩', 'subtracted 3']] },
      { instr: 'State the domain of the relation:', tex: '\\{(2, 5),\\ (-1, 3),\\ (4, 5),\\ (0, -2)\\}', answer: { t: 'nums', v: ['-1', '0', '2', '4'] }, check: { list: ['-1', '0', '2', '4'], is: [-1, 0, 2, 4] }, show: '⟨\\{-1, 0, 2, 4\\}⟩',
        steps: ['The domain is the set of inputs (x-values).', '⟨\\{-1, 0, 2, 4\\}⟩'], clue: { m: 1, text: 'Every prize bag was searched at the exit. Only stuffed animals and candy.' },
        wrong: [['⟨\\{-2, 3, 5\\}⟩', 'gave the range'], ['⟨\\{2, 5\\}⟩', 'used only the first pair'], ['⟨\\{-2, -1, 0, 2, 3, 4, 5\\}⟩', 'listed every number']] },
      { instr: 'Find the range of y = x² for the domain:', tex: '\\{-2,\\ -1,\\ 0,\\ 1,\\ 2\\}', answer: { t: 'nums', v: ['0', '1', '4'] }, check: { list: ['0', '1', '4'], is: [0, 1, 4] }, show: '⟨\\{0, 1, 4\\}⟩',
        steps: ['Square each input: ⟨4, 1, 0, 1, 4⟩', 'List each output once: ⟨\\{0, 1, 4\\}⟩'], clue: { p: 2, l: 2, text: 'Coach Banks was cheering his team in the Racing Zone. His voice is on every race video.' },
        wrong: [['⟨\\{-4, -1, 0, 1, 4\\}⟩', 'kept the negative signs'], ['⟨\\{0, 2, 4\\}⟩', 'doubled instead of squaring'], ['⟨\\{-2, -1, 0, 1, 2\\}⟩', 'gave the domain']] },
      { instr: 'Find the rate of change of the table:', text: 'x: 1, 3, 5, 7 and y: 4, 10, 16, 22', html: T([['x', '1', '3', '5', '7'], ['y', '4', '10', '16', '22']]), answer: { t: 'num', v: '3' }, check: { num: '(10-4)/(3-1)', is: 3 },
        steps: ['⟨\\dfrac{\\Delta y}{\\Delta x} = \\dfrac{10 - 4}{3 - 1}⟩', '⟨= 3⟩'], clue: { m: 2, text: 'The pizza boxes were all from tonight’s party. Every one held only crusts.' },
        wrong: [['⟨6⟩', 'used only the change in y'], ['⟨\\tfrac{1}{3}⟩', 'divided change in x by change in y'], ['⟨4⟩', 'used the first y-value']] },
      { instr: 'Find the 10th term of the sequence:', tex: '7,\\ 11,\\ 15,\\ 19,\\ \\dots', answer: { t: 'num', v: '43' }, check: { num: '7+9*4', is: 43 },
        steps: ['⟨a_n = 7 + (n - 1)(4)⟩', '⟨a_{10} = 7 + 9(4) = 43⟩'], clue: { p: 3, l: 3, text: 'Priya Shah was signing autographs at the Snack Bar. Fans lined up the whole time.' },
        wrong: [['⟨47⟩', 'used 10 × 4 + 7'], ['⟨40⟩', 'used 10 × 4'], ['⟨39⟩', 'used 9 × 4 + 3']] },
      { instr: 'If f(x) = 4x − 1, which input gives an output of 27?', text: 'Find x so that f(x) = 27.', answer: { t: 'num', v: '7' }, check: { num: '(27+1)/4', is: 7 },
        steps: ['⟨4x - 1 = 27⟩', '⟨4x = 28,\\ x = 7⟩'], clue: { m: 4, text: 'Every pinball table was flipped for cleaning. Nothing was taped underneath.' },
        wrong: [['⟨107⟩', 'found f(27) instead'], ['⟨6.5⟩', 'subtracted 1 instead of adding'], ['⟨28⟩', 'forgot to divide by 4']] },
      { instr: 'Find the average rate of change of f(x) = x² from x = 1 to x = 3.', text: '⟨\\dfrac{f(3) - f(1)}{3 - 1}⟩', answer: { t: 'num', v: '4' }, check: { num: '(9-1)/(3-1)', is: 4 },
        steps: ['⟨f(3) = 9,\\ f(1) = 1⟩', '⟨\\dfrac{9 - 1}{3 - 1} = 4⟩'], clue: { p: 5, l: 5, text: 'Zoe King was opening presents in the Party Room. Her whole family took photos.' },
        wrong: [['⟨8⟩', 'did not divide by the change in x'], ['⟨\\tfrac{1}{4}⟩', 'divided upside down'], ['⟨2⟩', 'used only the change in x']] },
      { instr: 'If f(x) = −2x + 6 and g(x) = x², find:', tex: 'f(2) + g(-2)', answer: { t: 'num', v: '6' }, check: { num: '(-2*2+6)+(-2)**2', is: 6 },
        steps: ['⟨f(2) = -4 + 6 = 2⟩', '⟨g(-2) = 4⟩', '⟨2 + 4 = 6⟩'], clue: { m: 5, text: 'The skee-ball lanes were closed for waxing. Nothing rolled down them tonight.' },
        wrong: [['⟨-2⟩', 'used g(−2) = −4'], ['⟨-6⟩', 'used f(2) = −10'], ['⟨10⟩', 'used f(2) = 6']] }
    ],
    falseClues: [
      'Mr. Ortega was showing kids how to play pinball all night.', 'A tech checked every trash bin. All empty.', 'Max Rivera was seen walking out of the Back Office.',
      'Mr. Ortega was refilling napkins at the Snack Bar.', 'Lena Cho had a heavy trash bin by the back door.', 'Coach Banks stepped into the Back Office for twenty minutes.',
      'Mr. Ortega never went near the Back Office.', 'The trash bins were emptied an hour before the theft.', 'Priya Shah was spotted near the Back Office door.',
      'The trophy fit perfectly in a prize bag.', 'Mr. Ortega was racing in the Racing Zone with the team.', 'Zoe King carried a big pizza box to her car.',
      'Coach Banks wheeled a trash bin out back.', 'Mr. Ortega was taking photos in the Party Room.', 'A claw machine was rattling strangely.',
      'Lena Cho was alone in the Back Office.', 'Mr. Ortega was fixing the prize counter all night.', 'Someone taped something under a pinball table.',
      'Max Rivera rolled a trash bin outside.', 'Mr. Ortega was eating pizza with the birthday party.', 'The skee-ball lane had a gold scratch.',
      'Priya Shah left the Snack Bar for half an hour.', 'The trash bin was locked in a closet all night.', 'Mr. Ortega was in Pinball Alley with Lena.',
      'Zoe King wandered into the Back Office.', 'A pizza box felt much too heavy.', 'Mr. Ortega was cheering in the Racing Zone.',
      'Coach Banks carried a claw-machine prize bag.', 'The Back Office was locked all night.', 'Mr. Ortega was handing out tickets at the Prize Counter.'
    ]
  },

  escape: {
    title: 'Escape the Function Factory', emoji: '🏭', endEmoji: '⚙️🏆',
    intro: 'Your class tour of the Function Factory went wrong: the doors locked and the machines are running wild! Every machine follows a rule. Figure out the rules, unlock five rooms, and reach the exit in <b>30 minutes</b>, before the night shift starts.',
    finalStory: 'The exit door has a five-letter keypad. A sign reads: “Line up your key cards from the smallest stamp to the largest. The letters spell the password.”',
    finalAsk: 'Password?', word: 'GEARS',
    outro: 'GEARS! The exit rolls open and the machines power down. The factory manager laughs: “You figured out every rule. Want a job?”',
    stages: [
      { name: 'The Input-Output Machine', type: 'fields', stamp: 46, letter: 'A',
        story: 'The first machine is labeled f(x) = 2x + 3. It will only open when you tell it two of its outputs.',
        scene: { kind: 'svg', viewBox: '0 0 400 300', svg: '<rect x="110" y="70" width="180" height="120" rx="14" fill="#1b2150" stroke="#ffc857" stroke-width="3"/><text x="200" y="115" text-anchor="middle" fill="#fff" font-size="18">FUNCTION MACHINE</text><text x="200" y="160" text-anchor="middle" fill="#ffc857" font-size="26" font-weight="700">f(x) = 2x + 3</text><text x="55" y="135" text-anchor="middle" fill="#fff" font-size="26">→</text><text x="345" y="135" text-anchor="middle" fill="#fff" font-size="26">→</text><text x="200" y="250" text-anchor="middle" font-size="50">⚙️</text>' },
        title: 'Machine Panel', prompt: '<p>Find each output.</p>', fields: [{ label: 'f(5) =', answer: 13 }, { label: 'f(−4) =', answer: -5 }], button: 'Start the machine',
        hints: ['Replace x with the input.', 'f(5) = 2(5) + 3.', 'f(−4) = 2(−4) + 3 = −8 + 3.'], key: 'f(5) = 13, f(−4) = −5.', check: [['2*5+3', 13], ['2*(-4)+3', -5]] },
      { name: 'The Control Room', type: 'cipher', stamp: 14, letter: 'G',
        story: 'A coded message blinks on the control panel. The shift is written somewhere in this room. Click things to search.',
        scene: { kind: 'emoji', bg: '#101a2e', floor: '#1f2b45', items: [{ e: '🖥️', x: 90, y: 150, s: 60, msg: 'A screen full of blinking lights.' }, { e: '📋', x: 300, y: 200, s: 50, clue: 'Clipboard note:<br>f(x) = x² − 2<br>Shift = f(3)', msg: 'A clipboard with a rule on it!' }, { e: '☕', x: 200, y: 215, s: 40, msg: 'Cold coffee. Someone left in a hurry.' }, { e: '🔧', x: 210, y: 110, s: 44, msg: 'A wrench. Not a clue, just a wrench.' }] },
        plain: 'THE NEXT KEY IS HIDDEN IN THE BOILER', shift: 7, answer: 'BOILER', askLabel: 'Where is the next key?',
        hints: ['Click the clipboard.', 'f(3) = 3² − 2.', '9 − 2 = 7. Set the shift to 7.'], key: 'f(3) = 9 − 2 = 7. The message says THE NEXT KEY IS HIDDEN IN THE BOILER.', checkNum: ['3**2-2', 7] },
      { name: 'The Sorting Belt', type: 'classify', stamp: 88, letter: 'S',
        story: 'Four crates roll down the belt. Only functions can go to the next room. Sort each crate.',
        scene: { kind: 'emoji', bg: '#1d1530', floor: '#3a2b4a', items: [{ e: '📦', x: 70, y: 170, s: 54 }, { e: '📦', x: 160, y: 170, s: 54 }, { e: '📦', x: 250, y: 170, s: 54 }, { e: '📦', x: 340, y: 170, s: 54 }], caption: 'is each crate a function?' },
        title: 'Function or not?', prompt: '<p style="color:var(--dim)">Each input may have only ONE output.</p>',
        items: ['{(1, 2), (2, 3), (3, 4)}', '{(1, 2), (1, 5), (2, 3)}', 'y = x²', 'x = y² (a sideways parabola)'], options: ['Function', 'Not a function'], answer: [0, 1, 0, 1],
        hints: ['Look for an input that appears twice with different outputs.', 'Crate 2: the input 1 goes to 2 AND to 5.', 'A sideways parabola fails the vertical line test.'], key: 'Function, not a function, function, not a function.' },
      { name: 'The Assembly Line', type: 'order', stamp: 29, letter: 'E',
        story: 'Robots on the line add the same number each step: 3, 7, 11, 15, … To unlock the line, put the steps for finding the 20th term in order.',
        scene: { kind: 'emoji', bg: '#13261c', floor: '#2c4a2c', items: [{ e: '🤖', x: 120, y: 170, s: 70, msg: 'Beep. Boop. Arithmetic.' }, { e: '🔩', x: 290, y: 175, s: 50, msg: 'A bolt.' }], caption: 'put the steps in order' },
        title: 'Find the 20th term', prompt: '<div class="eq">3, 7, 11, 15, …</div><p>Place the steps from first to last.</p>',
        steps: ['Find the common difference: d = 4', 'Write the rule: aₙ = 3 + (n − 1)(4)', 'Simplify: aₙ = 4n − 1', 'Substitute n = 20: a₂₀ = 4(20) − 1 = 79'],
        hints: ['First figure out what is added each time.', 'Then write the explicit rule using the first term.', 'Simplify before you plug in 20.'], key: 'd = 4; aₙ = 3 + 4(n − 1) = 4n − 1; a₂₀ = 79.', checkExpr: ['3+(x-1)*4', '4*x-1'] },
      { name: 'The Exit Gate', type: 'fields', stamp: 63, letter: 'R', ui: 'dial',
        story: 'The gate shows a table from a linear machine. Dial A is its rate of change. Dial B is its starting value (the output when x = 0).',
        scene: { kind: 'emoji', bg: '#20160e', floor: '#3a2a1a', items: [{ e: '🚪', x: 200, y: 180, s: 120, msg: 'A steel gate with two dials.' }], caption: 'dial A, then dial B' },
        title: 'The Gate Table', prompt: '<table style="margin:auto;border-collapse:collapse"><tr><th style="border:1px solid #888;padding:4px 10px">x</th><td style="border:1px solid #888;padding:4px 10px">0</td><td style="border:1px solid #888;padding:4px 10px">1</td><td style="border:1px solid #888;padding:4px 10px">2</td><td style="border:1px solid #888;padding:4px 10px">3</td></tr><tr><th style="border:1px solid #888;padding:4px 10px">y</th><td style="border:1px solid #888;padding:4px 10px">2</td><td style="border:1px solid #888;padding:4px 10px">5</td><td style="border:1px solid #888;padding:4px 10px">8</td><td style="border:1px solid #888;padding:4px 10px">11</td></tr></table><p>A = rate of change, B = starting value.</p>', fields: [{ label: 'A', answer: 3 }, { label: 'B', answer: 2 }], button: 'Open the gate',
        hints: ['Rate of change = change in y ÷ change in x.', 'y goes up 3 each time x goes up 1.', 'The starting value is y when x = 0.'], key: 'A = 3 (y rises 3 per 1), B = 2.', check: [['(5-2)/(1-0)', 3], ['2', 2]] }
    ]
  },

  stations: [
    { title: 'Relations, Domain and Range', note: 'Show your work. Use set notation for domain and range.',
      items: [
        ['State the domain: ⟨\\{(1,4),\\ (2,6),\\ (3,8),\\ (4,10)\\}⟩', '⟨\\{1, 2, 3, 4\\}⟩'],
        ['State the range: ⟨\\{(1,4),\\ (2,6),\\ (3,8),\\ (4,10)\\}⟩', '⟨\\{4, 6, 8, 10\\}⟩'],
        ['Is ⟨\\{(1,4),\\ (2,6),\\ (1,8)\\}⟩ a function? Explain.', 'No: the input 1 has two outputs.'],
        ['Is ⟨\\{(-2,3),\\ (0,3),\\ (2,3)\\}⟩ a function? Explain.', 'Yes: each input has one output (outputs may repeat).'],
        ['Find the range of ⟨y = x + 2⟩ for the domain ⟨\\{-1, 0, 1\\}⟩.', '⟨\\{1, 2, 3\\}⟩', { list: ['-1+2', '0+2', '1+2'], is: [1, 2, 3] }],
        ['A mapping sends 1 → a, 2 → a and 3 → b. Is it a function?', 'Yes: each input has exactly one output.'],
        ['A graph passes through ⟨(2, 1)⟩ and ⟨(2, -3)⟩. Can it be a function?', 'No: it fails the vertical line test at ⟨x = 2⟩.'],
        ['A taxi ride can be 0 to 20 miles. State a reasonable domain for the miles ⟨m⟩.', '⟨0 \\le m \\le 20⟩'],
        ['State the range: ⟨\\{(-3, 9),\\ (-1, 1),\\ (0, 0),\\ (1, 1),\\ (3, 9)\\}⟩', '⟨\\{0, 1, 9\\}⟩'],
        ['Is ⟨y = |x|⟩ a function? Explain.', 'Yes: every x has exactly one absolute value.']] },
    { title: 'Function Notation', note: 'Evaluate or solve. Show the substitution.',
      items: [
        ['⟨f(x) = 5x - 2⟩. Find ⟨f(3)⟩.', '⟨13⟩', { num: '5*3-2', is: 13 }],
        ['⟨f(x) = 5x - 2⟩. Find ⟨f(-1)⟩.', '⟨-7⟩', { num: '5*(-1)-2', is: -7 }],
        ['⟨g(x) = x^2 - 4⟩. Find ⟨g(-3)⟩.', '⟨5⟩', { num: '(-3)**2-4', is: 5 }],
        ['⟨h(x) = -2x + 7⟩. Find ⟨h(0)⟩.', '⟨7⟩', { num: '7', is: 7 }],
        ['⟨f(x) = 3x + 1⟩. Find ⟨x⟩ when ⟨f(x) = 19⟩.', '⟨x = 6⟩', { num: '(19-1)/3', is: 6 }],
        ['⟨g(x) = \\tfrac{x}{2} + 4⟩. Find ⟨g(10)⟩.', '⟨9⟩', { num: '10/2+4', is: 9 }],
        ['⟨f(x) = x^2 + x⟩. Find ⟨f(2) + f(-2)⟩.', '⟨6 + 2 = 8⟩', { num: '(4+2)+(4-2)', is: 8 }],
        ['⟨p(t) = 50 + 12t⟩ is the money saved after ⟨t⟩ weeks. Find ⟨p(5)⟩.', '$110', { num: '50+12*5', is: 110 }],
        ['⟨f(x) = 4x - 3⟩. Find ⟨f(a + 1)⟩.', '⟨4a + 1⟩', { expr: '4*(x+1)-3', is: '4*x+1' }],
        ['⟨f(x) = -x^2 + 10⟩. Find ⟨f(4)⟩.', '⟨-6⟩', { num: '-(4**2)+10', is: -6 }]] },
    { title: 'Rate of Change', note: 'Find each rate of change. Include units when there are units.',
      items: [
        ['Find the rate of change from ⟨(1, 3)⟩ to ⟨(4, 12)⟩.', '⟨3⟩', { num: '(12-3)/(4-1)', is: 3 }],
        ['Find the rate of change of the table.<br>' + T([['x', '0', '2', '4', '6'], ['y', '5', '9', '13', '17']]), '⟨2⟩', { num: '(9-5)/2', is: 2 }],
        ['Find the average rate of change of ⟨f(x) = x^2⟩ from ⟨x = 0⟩ to ⟨x = 4⟩.', '⟨4⟩', { num: '(16-0)/4', is: 4 }],
        ['A car travels 180 miles in 3 hours. What is its rate?', '60 miles per hour', { num: '180/3', is: 60 }],
        ['Is the table linear? Explain.<br>' + T([['x', '1', '2', '3', '4'], ['y', '2', '4', '8', '16']]), 'No: the y-values do not change by the same amount.'],
        ['Is the table linear? Explain.<br>' + T([['x', '0', '1', '2', '3'], ['y', '7', '4', '1', '−2']]), 'Yes: y changes by −3 each time.'],
        ['Find the rate of change from ⟨(-2, 5)⟩ to ⟨(3, -5)⟩.', '⟨-2⟩', { num: '(-5-5)/(3-(-2))', is: -2 }],
        ['A plant is 4 cm tall at week 0 and 22 cm tall at week 6. Find its average growth rate.', '3 cm per week', { num: '(22-4)/6', is: 3 }],
        ['Find the average rate of change of ⟨f(x) = x^2 - 2x⟩ from ⟨x = 1⟩ to ⟨x = 3⟩.', '⟨2⟩', { num: '((9-6)-(1-2))/(3-1)', is: 2 }],
        ['What is the rate of change of ⟨y = -4x + 1⟩?', '⟨-4⟩']] },
    { title: 'Arithmetic Sequences', note: 'Use ⟨a_n = a_1 + (n - 1)d⟩.',
      items: [
        ['Write the next three terms: ⟨5, 9, 13, \\dots⟩', '⟨17, 21, 25⟩', { list: ['13+4', '13+8', '13+12'], is: [17, 21, 25] }],
        ['Find the common difference: ⟨20, 14, 8, \\dots⟩', '⟨-6⟩', { num: '14-20', is: -6 }],
        ['Find the 12th term: ⟨3, 7, 11, \\dots⟩', '⟨47⟩', { num: '3+11*4', is: 47 }],
        ['Write a rule for ⟨6, 11, 16, \\dots⟩', '⟨a_n = 5n + 1⟩', { expr: '6+(x-1)*5', is: '5*x+1' }],
        ['Write a rule for ⟨10, 7, 4, \\dots⟩', '⟨a_n = -3n + 13⟩', { expr: '10+(x-1)*(-3)', is: '-3*x+13' }],
        ['Find the 25th term: ⟨2, 5, 8, \\dots⟩', '⟨74⟩', { num: '2+24*3', is: 74 }],
        ['Which term of ⟨4, 9, 14, \\dots⟩ is 99?', 'the 20th term', { num: '(99-4)/5+1', is: 20 }],
        ['⟨a_1 = 8⟩ and ⟨d = -2⟩. Find ⟨a_{10}⟩.', '⟨-10⟩', { num: '8+9*(-2)', is: -10 }],
        ['Row 1 of a theater has 12 seats, and each row has 3 more than the row before. How many seats are in row 15?', '54 seats', { num: '12+14*3', is: 54 }],
        ['Is ⟨2, 4, 8, 16, \\dots⟩ arithmetic? Explain.', 'No: there is no common difference (it doubles).']] }
  ],

  cheat: {
    focus: 'relations, functions, domain and range, and function notation',
    morefocus: 'rate of change, linear vs. nonlinear, sequences and reading graphs',
    front: [
      { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
        ['relation', 'Any set of ordered pairs (inputs and outputs).', '⟨\\{(1,3),(2,5)\\}⟩'], ['function', 'Each input has exactly ONE output.', '⟨y = 2x + 1⟩'],
        ['domain', 'All the inputs (x-values).', '⟨\\{1, 2\\}⟩'], ['range', 'All the outputs (y-values).', '⟨\\{3, 5\\}⟩'],
        ['independent', 'The input variable ⟨x⟩.', 'hours worked'], ['dependent', 'The output variable ⟨y⟩.', 'money earned']] },
      { title: 'Is It a Function?', color: 'blue', kind: 'table', head: ['Form', 'Function when…'], rows: [
        ['ordered pairs', 'no x-value repeats with a different y'], ['mapping diagram', 'each input has only one arrow'], ['table', 'no input is listed with two outputs'], ['graph', 'it passes the <b>vertical line test</b>'], ['equation', 'each x gives one y (⟨x = y^2⟩ is not)']],
        after: '✔ Outputs may repeat: ⟨\\{(1,5),(2,5)\\}⟩ is a function.' },
      { title: 'Domain & Range', color: 'green', kind: 'example', text: 'Domain = inputs (x). Range = outputs (y). List each value once, in order.',
        example: '⟨\\{(-2, 4), (0, 1), (3, 4), (5, -1)\\}⟩', steps: [['Domain:', '⟨\\{-2, 0, 3, 5\\}⟩'], ['Range:', '⟨\\{-1, 1, 4\\}⟩']], answer: 'D ⟨\\{-2,0,3,5\\}⟩, R ⟨\\{-1,1,4\\}⟩' },
      { title: 'Function Notation', color: 'orange', kind: 'example', text: '⟨f(x)⟩ is read “f of x” and means the output when the input is ⟨x⟩. It does NOT mean f times x.',
        example: '⟨f(x) = 3x^2 - 1⟩. Find ⟨f(-2)⟩.', steps: [['Substitute:', '⟨3(-2)^2 - 1⟩'], ['Simplify:', '⟨3(4) - 1 = 11⟩']], answer: '⟨f(-2) = 11⟩' },
      { title: 'Solving f(x) = k', color: 'pink', kind: 'example', text: 'When the OUTPUT is given, set the rule equal to it and solve for ⟨x⟩.',
        example: '⟨g(x) = 2x - 5⟩. When is ⟨g(x) = 9⟩?', steps: [['Set equal:', '⟨2x - 5 = 9⟩'], ['Solve:', '⟨2x = 14,\\ x = 7⟩']], answer: '⟨x = 7⟩' },
      { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
        good: ['Domain → x, Range → y.', 'Use parentheses when you substitute a negative.', 'A vertical line hitting a graph twice means NOT a function.'],
        bad: [['⟨f(3)⟩ is not ⟨f \\cdot 3⟩', 'it means “put 3 in for x”'], ['repeated outputs', 'are fine; repeated INPUTS with different outputs are not'], ['⟨f(x) = 9⟩', 'is solving, not evaluating']] }
    ],
    back: [
      { title: 'Rate of Change', color: 'green', kind: 'example', text: 'Rate of change = how much ⟨y⟩ changes for each 1 unit change in ⟨x⟩.',
        example: 'From ⟨(2, 7)⟩ to ⟨(6, 19)⟩:', steps: [['Formula:', '⟨\\dfrac{y_2 - y_1}{x_2 - x_1}⟩'], ['Substitute:', '⟨\\dfrac{19 - 7}{6 - 2} = \\dfrac{12}{4}⟩']], answer: '⟨3⟩ per unit' },
      { title: 'Linear or Nonlinear?', color: 'purple', kind: 'table', head: ['Linear', 'Nonlinear'], rows: [
        ['constant rate of change', 'rate of change varies'], ['graph is a straight line', 'graph curves'], ['⟨y = mx + b⟩', '⟨y = x^2,\\ y = 2^x⟩'], ['x: 0, 1, 2 → y: 1, 4, 7 (+3)', 'x: 0, 1, 2 → y: 1, 2, 4 (×2)']] },
      { title: 'Arithmetic Sequences', color: 'blue', kind: 'example', text: 'Add the same number ⟨d⟩ (common difference) each time. ⟨a_n = a_1 + (n - 1)d⟩',
        example: '⟨4, 10, 16, 22, \\dots⟩: find ⟨a_{30}⟩.', steps: [['d:', '⟨10 - 4 = 6⟩'], ['Rule:', '⟨a_n = 4 + (n - 1)6 = 6n - 2⟩'], ['n = 30:', '⟨6(30) - 2 = 178⟩']], answer: '⟨178⟩' },
      { title: 'Reading Graphs', color: 'orange', kind: 'list', items: [
        '<b>Increasing</b>: the graph rises from left to right. <b>Decreasing</b>: it falls.', '<b>Constant</b>: a flat (horizontal) piece.', '<b>x-intercept</b>: where the graph crosses the x-axis (y = 0).',
        '<b>y-intercept</b>: where it crosses the y-axis (x = 0): the starting value.', '<b>Maximum / minimum</b>: the highest / lowest point.'] },
      { title: 'Four Ways to Show a Function', color: 'pink', kind: 'table', head: ['Words', 'Equation', 'Table'], rows: [
        ['Earn $8 per hour plus a $5 bonus.', '⟨y = 8x + 5⟩', 'x: 0, 1, 2<br>y: 5, 13, 21']], after: 'Graph: a line starting at ⟨(0, 5)⟩ that rises 8 for every 1 to the right.' },
      { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
        'Did I use x for the domain and y for the range?', 'Did I substitute with parentheses?', 'Is the rate of change constant (linear) or not?', 'Does my sequence rule give the first term when ⟨n = 1⟩?'] }
    ]
  }
};
