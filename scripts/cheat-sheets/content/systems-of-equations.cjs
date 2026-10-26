const F = require('../figs.cjs');
const kinds = '<div style="display:flex;gap:4px;justify-content:space-around;font-size:7.5pt;text-align:center">' + [
  ['one solution', [x => x + 1, x => -x + 3]], ['no solution', [x => x + 1, x => x - 1.5]], ['infinitely many', [x => 0.5 * x, x => 0.5 * x]]].map((t, i) =>
  '<div>' + F.plane({ id: 'sk' + i, xmin: -3, xmax: 3, ymin: -3, ymax: 3, size: 0.72, fns: [{ f: t[1][0], color: '#2563eb' }, { f: t[1][1], color: '#db2777', dashed: i === 2 }] }) + '<br>' + t[0] + '</div>').join('') + '</div>';
module.exports = {
  name: 'systems-of-equations', course: 'Algebra 1', unitNo: 6, unitName: 'Systems of Equations',
  focus: 'solving systems by graphing, substitution and elimination',
  morefocus: 'special systems, choosing a method and word problems',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['system', 'Two or more equations with the same variables.', '⟨y = 2x + 1,\\ y = -x + 4⟩'], ['solution', 'An ordered pair that makes every equation true.', '⟨(1, 3)⟩'],
      ['intersection', 'Where the graphs cross; the solution.', '⟨(1, 3)⟩'], ['substitution', 'Replace a variable with an equal expression.', '⟨y = 3x + 1⟩'], ['elimination', 'Add or subtract equations to cancel a variable.', '⟨+2y⟩ and ⟨-2y⟩']] },
    { title: 'Solving by Graphing', color: 'blue', kind: 'example', text: 'Graph both lines. The point where they cross is the solution.',
      example: '⟨y = 2x - 1⟩ and ⟨y = -x + 5⟩', steps: [['Intersection:', '⟨(2, 3)⟩']], answer: '⟨(2, 3)⟩', check: { list: ['2*2-1', '-2+5'], is: [3, 3] },
      fig: F.plane({ id: 'sg', xmin: -1, xmax: 5, ymin: -2, ymax: 5, size: 1.15, fns: [{ f: x => 2 * x - 1 }, { f: x => -x + 5, color: '#db2777' }], points: [{ x: 2, y: 3, label: '(2, 3)' }] }) },
    { title: 'Solving by Substitution', color: 'green', kind: 'example', text: 'Solve one equation for a variable, substitute into the other, solve, then substitute back.',
      example: '⟨y = 3x + 1⟩ and ⟨2x + y = 11⟩', steps: [['Substitute:', '⟨2x + (3x + 1) = 11⟩'], ['Solve:', '⟨5x = 10,\\ x = 2⟩'], ['Back:', '⟨y = 3(2) + 1 = 7⟩']], answer: '⟨(2, 7)⟩', check: { list: ['3*2+1', '2*2+7'], is: [7, 11] } },
    { title: 'Solving by Elimination', color: 'orange', kind: 'example', text: 'Line up the variables; add the equations so one variable cancels.',
      example: '⟨3x + 2y = 14⟩ and ⟨5x - 2y = 2⟩', steps: [['Add:', '⟨8x = 16,\\ x = 2⟩'], ['Substitute:', '⟨3(2) + 2y = 14,\\ y = 4⟩']], answer: '⟨(2, 4)⟩', check: { list: ['3*2+2*4', '5*2-2*4'], is: [14, 2] } },
    { title: 'Types of Solutions', color: 'pink', kind: 'html', html: '<b>One</b>: the lines cross. <b>None</b>: parallel lines (same slope, different intercept). <b>Infinitely many</b>: the same line.', fig: kinds },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['A solution must make <b>both</b> equations true.', 'Write the answer as an ordered pair ⟨(x, y)⟩.', 'Check in both original equations.'],
      bad: [['Stopping after finding ⟨x⟩', 'find ⟨y⟩ too'], ['Forgetting to multiply every term', 'when making opposite coefficients'], ['⟨0 = 5⟩ means “0”', 'it means no solution']] }
  ],
  back: [
    { title: 'Elimination: Multiply First', color: 'purple', kind: 'example', text: 'Multiply one or both equations so a variable has opposite coefficients.',
      example: '⟨2x + 3y = 8⟩ and ⟨x - y = -1⟩', steps: [['× 3 (2nd):', '⟨3x - 3y = -3⟩'], ['Add:', '⟨5x = 5,\\ x = 1⟩'], ['Back:', '⟨1 - y = -1,\\ y = 2⟩']], answer: '⟨(1, 2)⟩', check: { list: ['2*1+3*2', '1-2'], is: [8, -1] } },
    { title: 'Special Systems', color: 'blue', kind: 'words', rows: [
      ['⟨y = 2x + 3⟩, ⟨y = 2x - 1⟩: same slope, different intercepts', 'no solution'], ['⟨y = 3x - 4⟩, ⟨2y = 6x - 8⟩: the same line', 'infinitely many'], ['Solving gives ⟨0 = 4⟩ (false)', 'no solution'], ['Solving gives ⟨0 = 0⟩ (true)', 'infinitely many']] },
    { title: 'Choosing a Method', color: 'green', kind: 'words', rows: [
      ['a variable is already alone: ⟨y = 4x - 2⟩', 'substitution'], ['coefficients match or are opposites: ⟨3y⟩, ⟨-3y⟩', 'elimination'], ['you need a picture or an estimate', 'graphing']] },
    { title: 'Word Problems', color: 'orange', kind: 'example', text: 'Define two variables, write one equation for each fact, solve, answer in words.',
      example: '5 adult and 3 student tickets cost $43. Adult tickets cost $3 more.', steps: [['Equations:', '⟨5a + 3s = 43,\\ a = s + 3⟩'], ['Substitute:', '⟨5(s + 3) + 3s = 43,\\ s = 3.5⟩'], ['Adult:', '⟨a = 6.5⟩']], answer: 'student $3.50, adult $6.50', check: { list: ['5*6.5+3*3.5', '6.5-3.5'], is: [43, 3] } },
    { title: 'Checking a Solution', color: 'pink', kind: 'words', rows: [
      ['Is ⟨(2, -1)⟩ a solution of ⟨3x + y = 5⟩? ⟨3(2) + (-1) = 5⟩', '<span class="ok">✔</span>'], ['…and of ⟨x - 2y = 4⟩? ⟨2 - 2(-1) = 4⟩', '<span class="ok">✔</span>'], ['Both are true, so ⟨(2, -1)⟩ solves the system.', 'solution']],
      check: { list: ['3*2+(-1)', '2-2*(-1)'], is: [5, 4] } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I line up ⟨x⟩, ⟨y⟩ and the constants before eliminating?', 'Did I multiply <b>every</b> term of the equation?', 'Did I substitute back to find the other variable?', 'Does my ordered pair work in both equations?'] }
  ]
};
