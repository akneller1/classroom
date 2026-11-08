/* Discrete Math Unit 10 cheat sheet (Linear Programming). Corners and optimal values are recomputed by the checks. */
const F = require('../figs.cjs');
const val = (p, q, pts) => pts.map(([x, y]) => p * x + q * y);
module.exports = {
  name: 'discrete-linear-programming', course: 'Discrete Math', unitNo: 10, unitName: 'Linear Programming',
  focus: 'writing constraints, graphing systems of inequalities, feasible regions and objective functions',
  morefocus: 'corner points, maximizing and minimizing, special cases and interpreting solutions',
  front: [
    { title: 'Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['decision variables', 'the amounts you choose', 'x tables, y chairs'],
      ['constraint', 'an inequality limiting the variables', '⟨2x + y \\le 40⟩'],
      ['feasible region', 'points meeting every constraint', 'the shaded polygon'],
      ['objective function', 'the quantity to maximize or minimize', '⟨P = 30x + 50y⟩'],
      ['corner point', 'where boundary lines meet', '⟨(4, 2)⟩']] },
    { title: 'Writing Constraints', color: 'blue', kind: 'table', plain: true, head: ['Words', 'Inequality'], rows: [
      ['at most 60 items', '⟨x + y \\le 60⟩'], ['sales of at least $400 at $8 and $5', '⟨8x + 5y \\ge 400⟩'], ['chairs at least 4 times tables', '⟨y \\ge 4x⟩'],
      ['at most 30% deluxe (x) of all items', '⟨x \\le 0.3(x + y)⟩'], ['cannot make negative amounts', '⟨x \\ge 0,\\ y \\ge 0⟩']],
      after: 'Check a ratio with numbers: 2 tables need at least 8 chairs, so ⟨y \\ge 4x⟩, not ⟨x \\ge 4y⟩.' },
    { title: 'Graphing a System', color: 'green', kind: 'html', figFirst: true,
      fig: F.plane({ id: 'lp1', xmin: 0, xmax: 6, ymin: 0, ymax: 6, size: 1.45, ticks: 1, shade: [], polys: [{ pts: [[0, 0], [5, 0], [4, 2], [0, 4]], fill: '#2563eb', opacity: .2 }], fns: [{ f: x => 10 - 2 * x, from: 2, to: 5 }, { f: x => (8 - x) / 2 }], points: [{ x: 0, y: 0 }, { x: 5, y: 0, label: '(5,0)', dy: -5, dx: -14 }, { x: 4, y: 2, label: '(4,2)' }, { x: 0, y: 4, label: '(0,4)', dx: 4 }] }),
      html: '⟨2x + y \\le 10⟩, ⟨x + 2y \\le 8⟩, ⟨x, y \\ge 0⟩. Solid lines for ⟨\\le, \\ge⟩; dashed for ⟨<, >⟩. Test ⟨(0, 0)⟩ to choose the side.',
      check: [{ true: '2*4+2 === 10 && 4+2*2 === 8' }, { true: '[[0,0],[5,0],[4,2],[0,4]].every(([x,y]) => 2*x+y <= 10 && x+2*y <= 8)' }] },
    { title: 'Corner-Point Method', color: 'orange', kind: 'example', text: 'If a linear objective has an optimum on the region, it occurs at a corner point.',
      example: 'Maximize ⟨P = 3x + 4y⟩ on the region shown.', steps: [['Corners:', '(0, 0), (5, 0), (4, 2), (0, 4)'], ['Values:', '0, 15, 20, 16']], answer: 'max ⟨P = 20⟩ at (4, 2)',
      check: { true: '"' + val(3, 4, [[0, 0], [5, 0], [4, 2], [0, 4]]).join() + '" === "0,15,20,16"' } },
    { title: 'Finding a Corner', color: 'pink', kind: 'example', text: 'Solve the two boundary equations together.',
      example: '⟨2x + y = 10⟩ and ⟨x + 2y = 8⟩', steps: [['Eliminate:', '⟨4x + 2y = 20⟩ minus ⟨x + 2y = 8⟩'], ['So:', '⟨3x = 12⟩, ⟨x = 4⟩, ⟨y = 2⟩']], answer: '(4, 2)',
      check: { true: '2*4+2 === 10 && 4+2*2 === 8' } },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Evaluate the objective at every corner.', 'Check that every candidate corner is feasible.', 'Use profit = price − cost per unit.'],
      bad: [['“At most” as ⟨\\ge⟩', 'use ⟨\\le⟩'], ['Picking the corner with the biggest coordinates', 'compare objective values'], ['Testing only one constraint', 'a solution meets all of them']] }
  ],
  back: [
    { title: 'Minimizing on an Unbounded Region', color: 'purple', kind: 'html', figFirst: true,
      fig: F.plane({ id: 'lp2', xmin: 0, xmax: 9, ymin: 0, ymax: 7, size: 1.5, ticks: 2, polys: [{ pts: [[0, 6], [4, 2], [8, 0], [9, 0], [9, 7], [0, 7]], fill: '#16a34a', opacity: .18, color: 'none' }], fns: [{ f: x => 6 - x, to: 4 }, { f: x => (8 - x) / 2, from: 4 }], points: [{ x: 0, y: 6, label: '(0,6)', dx: 4 }, { x: 4, y: 2, label: '(4,2)' }, { x: 8, y: 0, label: '(8,0)', dx: -14 }] }),
      html: 'Minimize ⟨C = 2x + 3y⟩ with ⟨x + y \\ge 6⟩, ⟨x + 2y \\ge 8⟩: C = 18, 14, 16, so <b>min 14 at (4, 2)</b>. There is <b>no maximum</b>: the region is unbounded.',
      check: { true: '"' + val(2, 3, [[0, 6], [4, 2], [8, 0]]).join() + '" === "18,14,16"' } },
    { title: 'Special Cases', color: 'blue', kind: 'table', plain: true, head: ['Case', 'Sign', 'Example'], rows: [
      ['unique optimum', 'one corner is best', 'max ⟨3x + 4y⟩ above'], ['multiple optima', 'two adjacent corners tie: the whole edge is optimal', 'max ⟨x + 2y⟩ on ⟨x + 2y \\le 12,\\ 3x + 2y \\le 18⟩: (0, 6) and (3, 4.5) both give 12'],
      ['unbounded', 'region extends in a direction that improves the objective', 'max ⟨x + y⟩ with ⟨x + y \\ge 4⟩'], ['infeasible', 'no point meets every constraint', '⟨x + y \\le 3⟩ and ⟨x + y \\ge 5⟩']],
      check: { true: '0 + 2*6 === 12 && 3 + 2*4.5 === 12 && 3*3 + 2*4.5 === 18' } },
    { title: 'A Complete Problem', color: 'green', kind: 'example', text: 'Chairs (x): 2 h cutting, 1 h finishing, $30 profit. Tables (y): 1 h cutting, 3 h finishing, $50 profit. 40 h cutting, 45 h finishing.',
      example: 'Maximize ⟨P = 30x + 50y⟩ s.t. ⟨2x + y \\le 40⟩, ⟨x + 3y \\le 45⟩', steps: [['Corners:', '(0, 0), (20, 0), (15, 10), (0, 15)'], ['Values:', '0, 600, 950, 750']], answer: '15 chairs and 10 tables: $950',
      check: [{ true: '2*15+10 === 40 && 15+3*10 === 45' }, { true: '"' + val(30, 50, [[0, 0], [20, 0], [15, 10], [0, 15]]).join() + '" === "0,600,950,750"' }] },
    { title: 'Interpreting the Solution', color: 'orange', kind: 'table', plain: true, head: ['Idea', 'Meaning'], rows: [
      ['optimal point', 'how much of each item to make'], ['optimal value', 'the best profit or cost, with units'],
      ['binding constraint', 'used exactly at the optimum (both constraints above)'], ['slack', 'unused amount: at (20, 0), finishing uses 20 of 45 h: slack 25'],
      ['whole numbers', 'if the optimum is fractional, check nearby feasible integer points']],
      check: { num: '45-20', is: 25 } },
    { title: 'Level Lines', color: 'pink', kind: 'html',
      html: 'Set ⟨P = k⟩: ⟨3x + 4y = k⟩ is a line with slope ⟨-\\tfrac34⟩. Increasing ⟨k⟩ slides it away from the origin. The last corner it touches is the maximum. If the level lines are parallel to an edge, every point on that edge is optimal.' },
    { title: 'Challenge', color: 'teal', kind: 'html',
      html: 'For ⟨P = ax + y⟩ ⟨(a > 0)⟩ on the triangle with corners ⟨(0, 0), (4, 0), (0, 6)⟩: values ⟨0, 4a, 6⟩. The maximum is at ⟨(4, 0)⟩ when ⟨a > \\tfrac32⟩, at ⟨(0, 6)⟩ when ⟨a < \\tfrac32⟩, and along the whole edge when ⟨a = \\tfrac32⟩.',
      check: { num: '4*1.5', is: 6 } }
  ]
};
