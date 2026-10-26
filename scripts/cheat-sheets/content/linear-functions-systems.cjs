const F = require('../figs.cjs');
module.exports = {
  name: 'linear-functions-systems', course: 'Algebra 2', unitNo: 2, unitName: 'Linear Functions & Systems',
  focus: 'slope, forms of a line, parallel and perpendicular lines, and linear models',
  morefocus: 'inequalities, systems, linear programming and three variables',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['slope', 'Rise over run: ⟨\\tfrac{y_2 - y_1}{x_2 - x_1}⟩.', '⟨m = -2⟩'], ['y-intercept', 'Value when ⟨x = 0⟩ (the start).', '⟨(0, b)⟩'],
      ['residual', 'Actual − predicted ⟨y⟩.', '⟨-1.57⟩'], ['correlation r', 'Strength of a linear fit, ⟨-1 \\le r \\le 1⟩.', '⟨r \\approx 0.99⟩'], ['feasible region', 'Points meeting every constraint.', 'shaded overlap']] },
    { title: 'Slope & Rate of Change', color: 'blue', kind: 'example', text: 'Subtract in the same order on top and bottom. In context, slope has units (change in ⟨y⟩ per unit of ⟨x⟩).',
      example: 'Slope through ⟨(-2, 5)⟩ and ⟨(4, -7)⟩.', steps: [['Formula:', '⟨\\dfrac{-7 - 5}{4 - (-2)} = \\dfrac{-12}{6}⟩']], answer: '⟨m = -2⟩', check: { num: '(-7-5)/(4+2)', is: -2 } },
    { title: 'Three Forms of a Line', color: 'green', kind: 'table', head: ['Form', 'Equation', 'Best for'], rows: [
      ['Slope-intercept', '⟨y = mx + b⟩', 'graphing, models'], ['Point-slope', '⟨y - y_1 = m(x - x_1)⟩', 'a point and a slope'], ['Standard', '⟨Ax + By = C⟩', 'intercepts; slope ⟨-\\tfrac{A}{B}⟩']],
      after: 'Through ⟨(-2, 5)⟩, ⟨m = -2⟩: ⟨y - 5 = -2(x + 2)⟩ → ⟨y = -2x + 1⟩ → ⟨2x + y = 1⟩.', check: { list: ['-2*(-2)+1', '2*4+(-7)'], is: [5, 1] } },
    { title: 'Parallel & Perpendicular', color: 'orange', kind: 'example', text: 'Parallel: ⟨m_1 = m_2⟩. Perpendicular: flip and change the sign, ⟨m_1 m_2 = -1⟩.',
      example: 'Lines through ⟨(6, 1)⟩ related to ⟨y = \\tfrac{2}{3}x - 1⟩.', steps: [['Parallel:', '⟨y = \\tfrac{2}{3}x - 3⟩'], ['Perpendicular:', '⟨y = -\\tfrac{3}{2}x + 10⟩']], answer: 'both pass through ⟨(6, 1)⟩', check: { list: ['2/3*6-3', '-3/2*6+10'], is: [1, 1] } },
    { title: 'Linear Models & Best Fit', color: 'pink', kind: 'example', text: 'Use technology for the regression line; interpret slope and intercept with units. Interpolating is safer than extrapolating.',
      example: 'Weekly miles: ⟨y = 2.429x + 9.286⟩, ⟨r \\approx 0.986⟩', steps: [['Slope:', 'about 2.4 more miles each week'], ['Residual week 3 (15 mi):', '⟨15 - 16.57 = -1.57⟩']], answer: 'strong positive fit', check: { num: 'Math.round((15-(2.429*3+9.286))*100)/100', is: -1.57 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Change in ⟨y⟩ goes on top.', 'In point-slope, ⟨x - (-2)⟩ becomes ⟨x + 2⟩.', 'Give units when you interpret slope and intercept.'],
      bad: [['Run over rise', 'it is rise over run'], ['Perpendicular: flip only', 'flip and change the sign'], ['Trusting extrapolation', 'far outside the data is unreliable']] }
  ],
  back: [
    { title: 'Linear Inequalities', color: 'purple', kind: 'example', text: 'Solve for ⟨y⟩ (flip if you divide by a negative). Dashed for ⟨<, >⟩, solid for ⟨\\le, \\ge⟩; test a point.',
      example: 'Graph ⟨3x - 2y > 6⟩.', steps: [['Solve:', '⟨y < \\tfrac{3}{2}x - 3⟩'], ['Dashed,', 'shade below']], answer: '⟨(0, 0)⟩ is not a solution',
      fig: F.plane({ id: 'li', xmin: -2, xmax: 5, ymin: -5, ymax: 3, size: 1.0, fns: [{ f: x => 1.5 * x - 3, dashed: true }], shade: [{ f: x => 1.5 * x - 3, side: 'below' }] }), check: { true: '!(0 > 6) && 3*2-2*(-5) > 6' } },
    { title: 'Systems: How Many Solutions?', color: 'blue', kind: 'words', rows: [
      ['Lines cross; algebra gives ⟨x = 2,\\ y = 3⟩', 'one'], ['Parallel lines; algebra gives ⟨0 = 4⟩', 'none (inconsistent)'], ['Same line; algebra gives ⟨0 = 0⟩', 'infinitely many (dependent)'],
      ['⟨3x + 2y = 12⟩, ⟨5x - 2y = 4⟩: add → ⟨8x = 16⟩', '⟨(2, 3)⟩']], check: { list: ['3*2+2*3', '5*2-2*3'], is: [12, 4] } },
    { title: 'Systems in Context', color: 'green', kind: 'example', text: 'Set the two costs equal to find where they match; compare on each side.',
      example: 'Bike A: ⟨C = 15 + 3h⟩. Bike B: ⟨C = 5 + 5h⟩.', steps: [['Equal:', '⟨15 + 3h = 5 + 5h,\\ h = 5⟩'], ['Cost:', '⟨C = 30⟩']], answer: '(5 h, $30); under 5 h B is cheaper', check: { list: ['15+3*5', '5+5*5'], is: [30, 30] } },
    { title: 'Systems of Inequalities', color: 'orange', kind: 'example', text: 'Graph each boundary, keep the overlap. Vertices: intersect pairs of boundaries, then check all constraints.',
      example: '⟨x + y \\le 8⟩, ⟨2x + y \\le 10⟩, ⟨x, y \\ge 0⟩', steps: [['Vertices:', '⟨(0,0),\\ (5,0),\\ (2,6),\\ (0,8)⟩']], answer: 'the shaded quadrilateral',
      fig: F.plane({ id: 'lp', xmin: -1, xmax: 9, ymin: -1, ymax: 9, size: 0.95, polys: [{ pts: [[0, 0], [5, 0], [2, 6], [0, 8]], fill: '#ea7a12', color: '#ea7a12' }], points: [{ x: 2, y: 6, label: '(2,6)' }] }), check: { list: ['2+6', '2*2+6'], is: [8, 10] } },
    { title: 'Linear Programming', color: 'pink', kind: 'table', head: ['Vertex', '⟨(0,0)⟩', '⟨(5,0)⟩', '⟨(2,6)⟩', '⟨(0,8)⟩'], rows: [['⟨P = 30x + 20y⟩', '0', '150', '<b>180</b>', '160']],
      after: 'Test every vertex: the maximum is ⟨P = 180⟩ at ⟨(2, 6)⟩. A minimum works the same way.', check: { list: ['30*5', '30*2+20*6', '20*8'], is: [150, 180, 160] } },
    { title: 'Three Variables', color: 'teal', kind: 'example', text: 'Eliminate the same variable twice, solve the 2-variable system, back-substitute, check.',
      example: '⟨x + y + z = 6⟩, ⟨2x - y + z = 3⟩, ⟨x + 2y - z = 2⟩', steps: [['(1)+(3), (1)−(2):', '⟨2x + 3y = 8⟩, ⟨-x + 2y = 3⟩'], ['Solve:', '⟨x = 1,\\ y = 2⟩, then ⟨z = 3⟩']], answer: '⟨(1, 2, 3)⟩', check: { list: ['1+2+3', '2-2+3', '1+4-3'], is: [6, 3, 2] } }
  ]
};
