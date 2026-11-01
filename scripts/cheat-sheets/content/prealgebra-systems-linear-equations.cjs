/* Pre-Algebra (8th Grade) Unit 4 cheat sheet. Every worked example is checked by build.cjs; figures are drawn from the same numbers. */
const F = require('../figs.cjs');
const si = F.plane({ id: 's4a', xmin: -3, xmax: 3, ymin: -3, ymax: 4, size: 0.95, fns: [{ f: x => -2 * x / 3 + 2, color: '#2563eb' }], points: [{ x: 0, y: 2, label: '(0, 2)', dx: 5, dy: -4 }, { x: 3, y: 0, label: '', dx: 5 }] });
const sys = F.plane({ id: 's4b', xmin: -1, xmax: 5, ymin: -2, ymax: 6, size: 1.0, fns: [{ f: x => x + 1, color: '#2563eb' }, { f: x => -2 * x + 7, color: '#db2777' }], points: [{ x: 2, y: 3, label: '(2, 3)', dx: 7, dy: 4 }] });
const kinds = F.svg(300, 78,
  [[0, 'one'], [100, 'none'], [200, 'infinitely many']].map(([o, t]) => `<rect x="${o + 6}" y="4" width="88" height="56" fill="#fff" stroke="#d5dbe8"/><text x="${o + 50}" y="74" font-size="10" text-anchor="middle" font-weight="700" fill="#1f2a6b">${t}</text>`).join('') +
  '<line x1="12" y1="54" x2="88" y2="10" stroke="#2563eb" stroke-width="2.2"/><line x1="12" y1="12" x2="88" y2="54" stroke="#db2777" stroke-width="2.2"/>' +
  '<line x1="112" y1="50" x2="188" y2="20" stroke="#2563eb" stroke-width="2.2"/><line x1="112" y1="38" x2="188" y2="8" stroke="#db2777" stroke-width="2.2"/>' +
  '<line x1="212" y1="54" x2="288" y2="10" stroke="#2563eb" stroke-width="4"/><line x1="212" y1="54" x2="288" y2="10" stroke="#db2777" stroke-width="1.6" stroke-dasharray="5 4"/>', 2.9);
module.exports = {
  name: 'prealgebra-systems-linear-equations', course: 'Pre-Algebra (8th Grade)', unitNo: 4, unitName: 'Systems of Linear Equations',
  focus: 'slope-intercept form and solving systems by graphing',
  morefocus: 'substitution, elimination, inspection and word problems',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['system', 'Two or more equations with the same variables.', 'two lines'],
      ['solution', 'An ordered pair that makes every equation true.', '⟨(2, 3)⟩'],
      ['slope-intercept', '⟨y = mx + b⟩: slope ⟨m⟩, ⟨y⟩-intercept ⟨b⟩.', '⟨y = 4x - 3⟩'],
      ['parallel', 'Same slope, different intercepts; never meet.', '⟨y = 2x⟩ and ⟨y = 2x + 5⟩']] },
    { title: 'Slope-Intercept Graphs', color: 'blue', kind: 'example', text: 'Plot the ⟨y⟩-intercept ⟨b⟩, then use the slope (rise over run) to find more points.',
      example: 'Graph ⟨2x + 3y = 6⟩.', steps: [['Solve for ⟨y⟩:', '⟨3y = -2x + 6⟩, ⟨y = -\\tfrac{2}{3}x + 2⟩'], ['Plot:', 'start at ⟨(0, 2)⟩, down 2, right 3']], answer: 'line through ⟨(0, 2)⟩ and ⟨(3, 0)⟩', fig: si,
      check: [{ num: '2*0+3*2', is: 6 }, { num: '2*3+3*0', is: 6 }] },
    { title: 'Solving by Graphing', color: 'green', kind: 'example', text: 'Graph both lines. The point where they cross is the solution. Check it in both equations.',
      example: '⟨y = x + 1⟩ and ⟨y = -2x + 7⟩', steps: [['Crossing:', '⟨(2, 3)⟩'], ['Check:', '⟨3 = 2 + 1⟩ ✓ and ⟨3 = -4 + 7⟩ ✓']], answer: '⟨(2, 3)⟩', fig: sys,
      check: [{ num: '2+1', is: 3 }, { num: '-2*2+7', is: 3 }] },
    { title: 'How Many Solutions?', color: 'orange', kind: 'html', html: '<b>One</b>: different slopes (lines cross). <b>None</b>: same slope, different ⟨b⟩ (parallel). <b>Infinitely many</b>: same slope and same ⟨b⟩ (the same line).', fig: kinds },
    { title: 'Solving by Inspection', color: 'pink', kind: 'table', plain: true, head: ['System', 'Look at…', 'Solutions'], rows: [
      ['⟨y = 3x + 1⟩, ⟨y = 3x - 4⟩', 'same slope, different ⟨b⟩', 'none'], ['⟨x + y = 5⟩, ⟨2x + 2y = 10⟩', 'second = first × 2', 'infinitely many'], ['⟨y = 2x⟩, ⟨y = -x + 6⟩', 'different slopes', 'one']],
      check: { expr: '2*(x+y)', is: '2*x+2*y' } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Write the solution as an ordered pair ⟨(x, y)⟩.', 'Check the pair in <b>both</b> equations.', 'Line up ⟨x⟩, ⟨y⟩ and numbers before eliminating.'],
      bad: [['Solving for ⟨x⟩ only', 'find ⟨y⟩ too'], ['Subtracting only part of an equation', 'subtract every term'], ['"⟨0 = 0⟩ means no solution"', 'it means infinitely many']] }
  ],
  back: [
    { title: 'Substitution', color: 'purple', kind: 'example', text: 'Use when one equation is already solved for a variable. Replace that variable in the other equation.',
      example: '⟨y = 2x - 1⟩ and ⟨3x + y = 14⟩', steps: [['Substitute:', '⟨3x + (2x - 1) = 14⟩'], ['Solve:', '⟨5x = 15,\\ x = 3⟩'], ['Back-substitute:', '⟨y = 2(3) - 1 = 5⟩']], answer: '⟨(3, 5)⟩',
      check: [{ num: '2*3-1', is: 5 }, { num: '3*3+5', is: 14 }] },
    { title: 'Elimination', color: 'blue', kind: 'example', text: 'Add or subtract the equations so one variable cancels. Multiply an equation first if needed.',
      example: '⟨2x + 3y = 12⟩ and ⟨4x - 3y = 6⟩', steps: [['Add:', '⟨6x = 18,\\ x = 3⟩'], ['Substitute:', '⟨2(3) + 3y = 12,\\ y = 2⟩']], answer: '⟨(3, 2)⟩',
      check: [{ num: '2*3+3*2', is: 12 }, { num: '4*3-3*2', is: 6 }] },
    { title: 'Multiply, Then Eliminate', color: 'green', kind: 'example', text: 'Make the coefficients of one variable opposites.',
      example: '⟨x + 2y = 7⟩ and ⟨3x - y = 7⟩', steps: [['Multiply 2nd by 2:', '⟨6x - 2y = 14⟩'], ['Add:', '⟨7x = 21,\\ x = 3⟩, then ⟨y = 2⟩']], answer: '⟨(3, 2)⟩',
      check: [{ num: '3+2*2', is: 7 }, { num: '3*3-2', is: 7 }] },
    { title: 'Which Method?', color: 'orange', kind: 'table', plain: true, head: ['If you see…', 'Use'], rows: [
      ['a variable already alone (⟨y = …⟩)', 'substitution'], ['opposite coefficients (⟨3y⟩ and ⟨-3y⟩)', 'elimination (add)'], ['same slopes / multiples', 'inspection'], ['a picture or a quick estimate', 'graphing']] },
    { title: 'Word Problems', color: 'pink', kind: 'example', text: 'Define two variables, write two equations, solve, then answer in words.',
      example: 'Tickets: adults $8, students $5. 20 tickets cost $121. How many of each?', steps: [['Equations:', '⟨a + s = 20⟩, ⟨8a + 5s = 121⟩'], ['Substitute ⟨s = 20 - a⟩:', '⟨3a + 100 = 121,\\ a = 7⟩']], answer: '7 adult and 13 student tickets',
      check: [{ num: '7+13', is: 20 }, { num: '8*7+5*13', is: 121 }] },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Does my ordered pair make <b>both</b> equations true?', 'Did I find both ⟨x⟩ and ⟨y⟩?', 'If the variables vanished, did I decide none (false) or infinitely many (true)?', 'Does my word-problem answer make sense (whole tickets, positive amounts)?'] }
  ]
};
