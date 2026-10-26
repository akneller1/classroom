const F = require('../figs.cjs');
const g = (id, f, side, dashed, extra) => F.plane(Object.assign({ id, xmin: -4, xmax: 4, ymin: -4, ymax: 4, size: 1.05, fns: [{ f, dashed }], shade: [{ f, side }] }, extra || {}));
module.exports = {
  name: 'graphing-inequalities', course: 'Algebra 1', unitNo: 6, unitName: 'Graphing Linear Inequalities',
  focus: 'graphing linear inequalities in two variables',
  morefocus: 'systems of inequalities and feasible regions',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['boundary line', 'The line from replacing the symbol with =.', '⟨y = 2x - 1⟩'], ['half-plane', 'The region on one side of the boundary.', 'shaded side'],
      ['test point', 'A point not on the line used to pick the side.', '⟨(0, 0)⟩'], ['solution region', 'All points ⟨(x, y)⟩ that make it true.', 'the shading']] },
    { title: 'Solid or Dashed?', color: 'blue', kind: 'table', head: ['Symbol', 'Boundary', 'Points on the line'], rows: [
      ['⟨<⟩ or ⟨>⟩', '<b>dashed</b>', 'not solutions'], ['⟨\\le⟩ or ⟨\\ge⟩', '<b>solid</b>', 'solutions']],
      after: 'In ⟨y = mx + b⟩ form: ⟨y >⟩ or ⟨y \\ge⟩ shades <b>above</b>; ⟨y <⟩ or ⟨y \\le⟩ shades <b>below</b>.' },
    { title: 'Graph a Linear Inequality', color: 'green', kind: 'example', text: '1. Write in ⟨y = mx + b⟩ form. 2. Draw the boundary (solid or dashed). 3. Test a point. 4. Shade.',
      example: '⟨y < 2x + 3⟩', steps: [['Boundary:', 'dashed ⟨y = 2x + 3⟩'], ['Test ⟨(0, 0)⟩:', '⟨0 < 3⟩ true'], ['Shade:', 'the side with ⟨(0, 0)⟩ (below)']], answer: 'dashed line, shade below',
      fig: g('gl', x => 2 * x + 3, 'below', true), check: { true: '0 < 2*0+3' } },
    { title: 'Rewrite First', color: 'orange', kind: 'example', text: 'Solve for ⟨y⟩. Flip the sign if you divide by a negative.',
      example: '⟨3x - y \\ge 6⟩', steps: [['Subtract ⟨3x⟩:', '⟨-y \\ge -3x + 6⟩'], ['Divide by ⟨-1⟩, flip:', '⟨y \\le 3x - 6⟩']], answer: 'solid line, shade below', check: { true: '3*0-(-7) >= 6 && -7 <= 3*0-6' } },
    { title: 'Using a Test Point', color: 'pink', kind: 'words', rows: [
      ['⟨y > 2x - 1⟩ with ⟨(0, 0)⟩: ⟨0 > -1⟩', 'true: shade its side'], ['⟨3x - y \\ge 6⟩ with ⟨(0, 0)⟩: ⟨0 \\ge 6⟩', 'false: shade the other side'], ['If the line passes through ⟨(0, 0)⟩', 'test ⟨(1, 0)⟩ instead']],
      check: { true: '0 > 2*0-1 && !(0 >= 6)' } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Dashed for ⟨<, >⟩; solid for ⟨\\le, \\ge⟩.', 'Use a test point to choose the side.', 'Check one point from the shading in the inequality.'],
      bad: [['Solid line for ⟨<⟩', 'use dashed'], ['Forgetting to flip', 'when dividing by a negative'], ['Testing a point on the line', 'pick one off the line']] }
  ],
  back: [
    { title: 'Write an Inequality from a Graph', color: 'purple', kind: 'example', text: 'Find the boundary line, then read solid/dashed and the shading.',
      example: 'Dashed line through ⟨(0, -1)⟩ with slope 1, shaded above.', steps: [['Boundary:', '⟨y = x - 1⟩'], ['Dashed, above:', '⟨>⟩']], answer: '⟨y > x - 1⟩',
      fig: g('wi', x => x - 1, 'above', true) },
    { title: 'Systems of Inequalities', color: 'blue', kind: 'example', text: 'Graph each inequality. The solution is where the shadings <b>overlap</b>.',
      example: '⟨y \\ge x - 1⟩ and ⟨y < -x + 2⟩', steps: [['Line 1:', 'solid, shade above'], ['Line 2:', 'dashed, shade below']], answer: 'the overlap (left wedge)',
      fig: F.plane({ id: 'ss', xmin: -4, xmax: 4, ymin: -4, ymax: 4, size: 1.1, fns: [{ f: x => x - 1 }, { f: x => -x + 2, color: '#db2777', dashed: true }], shade: [{ f: x => x - 1, side: 'above' }, { f: x => -x + 2, side: 'below', color: '#db2777' }] }) },
    { title: 'Is a Point a Solution?', color: 'green', kind: 'words', rows: [
      ['⟨(0, 0)⟩ in ⟨y \\ge x - 1⟩: ⟨0 \\ge -1⟩ ✔ and ⟨y < -x + 2⟩: ⟨0 < 2⟩ ✔', 'yes'], ['⟨(3, 0)⟩: ⟨0 \\ge 2⟩ ✘', 'no'], ['A point on a dashed line', 'not a solution']],
      check: { true: '0 >= -1 && 0 < 2 && !(0 >= 3-1)' } },
    { title: 'Feasible Region', color: 'orange', kind: 'example', text: 'The region that meets every constraint (often ⟨x \\ge 0,\\ y \\ge 0⟩ in context).',
      example: '⟨x \\ge 0⟩, ⟨y \\ge 0⟩, ⟨x + y \\le 4⟩', steps: [['Corners:', '⟨(0, 0),\\ (4, 0),\\ (0, 4)⟩']], answer: 'the shaded triangle',
      fig: F.plane({ id: 'fr', xmin: -1, xmax: 5, ymin: -1, ymax: 5, size: 1.0, polys: [{ pts: [[0, 0], [4, 0], [0, 4]], fill: '#ea7a12', color: '#ea7a12' }] }) },
    { title: 'In Context', color: 'pink', kind: 'example', text: 'Define variables, write a constraint, then keep points that make sense (whole numbers, not negative).',
      example: 'Pens cost $2, notebooks $5; spend at most $30.', steps: [['Constraint:', '⟨2p + 5n \\le 30⟩'], ['Try ⟨(5, 4)⟩:', '⟨10 + 20 = 30 \\le 30⟩ ✔']], answer: '5 pens and 4 notebooks works', check: { true: '2*5+5*4 <= 30' } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I solve for ⟨y⟩ (and flip if I divided by a negative)?', 'Is each boundary solid or dashed correctly?', 'Did a test point decide the shading?', 'For a system, is my answer the overlap, not everything shaded?'] }
  ]
};
