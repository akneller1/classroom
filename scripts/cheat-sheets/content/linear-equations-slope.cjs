const F = require('../figs.cjs');
const types = '<div style="display:flex;gap:4px;justify-content:space-around;font-size:7.5pt;text-align:center">' + [
  ['positive', x => 1.5 * x, '#db2777'], ['negative', x => -1.5 * x, '#2563eb'], ['zero', () => 1, '#16a34a']].map((t, i) => '<div>' + F.plane({ id: 'lt' + i, xmin: -3, xmax: 3, ymin: -3, ymax: 3, size: 0.62, fns: [{ f: t[1], color: t[2] }] }) + '<br>' + t[0] + '</div>').join('') +
  '<div>' + F.plane({ id: 'lt3', xmin: -3, xmax: 3, ymin: -3, ymax: 3, size: 0.62, vlines: [{ x: 1, color: '#7b4fd0', dashed: false }] }) + '<br>undefined</div></div>';
module.exports = {
  name: 'linear-equations-slope', course: 'Algebra 1', unitNo: 5, unitName: 'Linear Functions and Graphing',
  focus: 'slope, rate of change, slope-intercept form and graphing lines',
  morefocus: 'writing equations of lines, intercepts, parallel and perpendicular lines',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['slope', 'Steepness: vertical change ÷ horizontal change.', '⟨m = 2⟩'], ['rate of change', 'Change in ⟨y⟩ for each 1 unit change in ⟨x⟩.', '$3 per hour'],
      ['x-intercept', 'Where the line crosses the x-axis (⟨y = 0⟩).', '⟨(4, 0)⟩'], ['y-intercept', 'Where the line crosses the y-axis (⟨x = 0⟩).', '⟨(0, -3)⟩'],
      ['linear', 'Constant rate of change; graph is a line.', '⟨y = 2x - 5⟩']] },
    { title: 'Slope from Two Points', color: 'blue', kind: 'example', text: '⟨m = \\dfrac{\\text{rise}}{\\text{run}} = \\dfrac{y_2 - y_1}{x_2 - x_1}⟩. Keep the points in the same order.',
      example: 'Slope through ⟨(-2, 3)⟩ and ⟨(4, -1)⟩.', steps: [['Substitute:', '⟨m = \\dfrac{-1 - 3}{4 - (-2)} = \\dfrac{-4}{6}⟩']], answer: '⟨m = -\\dfrac{2}{3}⟩', check: { num: '(-1-3)/(4-(-2))', is: -2 / 3 } },
    { title: 'Types of Slope', color: 'green', kind: 'html', html: 'Rises left to right: <b>positive</b>. Falls: <b>negative</b>. Horizontal: <b>zero</b> (⟨y = b⟩). Vertical: <b>undefined</b> (⟨x = a⟩).', fig: types },
    { title: 'Slope-Intercept Form', color: 'orange', kind: 'example', text: '⟨y = mx + b⟩: ⟨m⟩ is the slope, ⟨b⟩ is the y-intercept ⟨(0, b)⟩.',
      example: 'Graph ⟨y = 2x - 1⟩.', steps: [['Plot:', 'the y-intercept ⟨(0, -1)⟩'], ['Slope 2:', 'up 2, right 1 to ⟨(1, 1)⟩']], answer: 'draw the line',
      fig: F.plane({ id: 'si', xmin: -3, xmax: 3, ymin: -3, ymax: 3, size: 1.05, fns: [{ f: x => 2 * x - 1, color: '#ea7a12' }], points: [{ x: 0, y: -1, label: '(0,−1)', dx: 4, dy: 10 }, { x: 1, y: 1, label: '(1,1)' }] }), check: { num: '2*1-1', is: 1 } },
    { title: 'Slope from a Table', color: 'pink', kind: 'table', head: ['⟨x⟩', '0', '1', '2', '3'], rows: [['⟨y⟩', '1', '4', '7', '10']],
      after: '⟨y⟩ goes up 3 each time ⟨x⟩ goes up 1, so ⟨m = 3⟩ and ⟨b = 1⟩: ⟨y = 3x + 1⟩.', check: { list: ['3*0+1', '3*1+1', '3*2+1', '3*3+1'], is: [1, 4, 7, 10] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Slope = rise over run = change in ⟨y⟩ over change in ⟨x⟩.', 'The y-intercept is ⟨(0, b)⟩.', 'Check by plotting points or using a table.'],
      bad: [['⟨\\tfrac{y_2 - y_1}{x_1 - x_2}⟩', 'mixed order: keep both differences the same way'], ['run over rise', 'it is rise over run'], ['b is the x-intercept', 'b is the y-intercept']] }
  ],
  back: [
    { title: 'Forms of a Line', color: 'purple', kind: 'table', head: ['Form', 'Equation', 'Use it when…'], rows: [
      ['Slope-intercept', '⟨y = mx + b⟩', 'you know ⟨m⟩ and ⟨b⟩'], ['Point-slope', '⟨y - y_1 = m(x - x_1)⟩', 'you know ⟨m⟩ and a point'], ['Standard', '⟨Ax + By = C⟩', 'finding intercepts']],
      after: 'Standard form: integers, ⟨A \\ge 0⟩. ⟨y = 2x - 4 \\to 2x - y = 4⟩.' },
    { title: 'Slope and a Point', color: 'blue', kind: 'example', text: 'Use point-slope form, then simplify.',
      example: 'Slope 3 through ⟨(2, -1)⟩.', steps: [['Point-slope:', '⟨y + 1 = 3(x - 2)⟩'], ['Simplify:', '⟨y = 3x - 7⟩']], answer: '⟨y = 3x - 7⟩', check: { num: '3*2-7', is: -1 } },
    { title: 'Two Points', color: 'green', kind: 'example', text: 'Find the slope first, then use one point.',
      example: 'Through ⟨(1, 2)⟩ and ⟨(4, -1)⟩.', steps: [['Slope:', '⟨m = \\dfrac{-1 - 2}{4 - 1} = -1⟩'], ['Point ⟨(1, 2)⟩:', '⟨y - 2 = -1(x - 1)⟩']], answer: '⟨y = -x + 3⟩', check: { list: ['-1+3', '-4+3'], is: [2, -1] } },
    { title: 'Finding Intercepts', color: 'orange', kind: 'example', text: 'x-intercept: set ⟨y = 0⟩. y-intercept: set ⟨x = 0⟩.',
      example: '⟨2x - 3y = 12⟩', steps: [['⟨y = 0⟩:', '⟨2x = 12,\\ x = 6⟩'], ['⟨x = 0⟩:', '⟨-3y = 12,\\ y = -4⟩']], answer: '⟨(6, 0)⟩ and ⟨(0, -4)⟩', check: { list: ['2*6-3*0', '2*0-3*(-4)'], is: [12, 12] } },
    { title: 'Parallel & Perpendicular', color: 'pink', kind: 'table', head: ['Lines', 'Slopes', 'Example (m = 4)'], rows: [
      ['parallel', 'equal: ⟨m_1 = m_2⟩', '⟨4⟩'], ['perpendicular', 'opposite reciprocals: ⟨m_1 \\cdot m_2 = -1⟩', '⟨-\\tfrac{1}{4}⟩']],
      after: 'Parallel lines never meet; perpendicular lines meet at a right angle.', check: { num: '4*(-1/4)', is: -1 } },
    { title: 'Slope & Intercept in Context', color: 'teal', kind: 'example', text: 'Slope = rate (with units); y-intercept = starting value.',
      example: 'A bike rental costs $5 plus $3 per hour.', steps: [['Model:', '⟨y = 3x + 5⟩'], ['Slope 3:', '$3 more for each hour'], ['Intercept 5:', 'the $5 fee when ⟨x = 0⟩']], answer: '⟨y = 3x + 5⟩' }
  ]
};
