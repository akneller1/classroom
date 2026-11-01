/* Pre-Algebra (8th Grade) Unit 3 cheat sheet. Every worked example is checked by build.cjs; figures are drawn from the same numbers. */
const F = require('../figs.cjs');
const lin = F.plane({ id: 'l3a', xmin: -1, xmax: 4, ymin: -1, ymax: 7, size: 1.15, fns: [{ f: x => 2 * x - 1, color: '#ea7a12' }], points: [{ x: 0, y: -1, label: '(0, −1)', dx: 6, dy: 4 }, { x: 2, y: 3, label: '(2, 3)', dx: 6, dy: 4 }] });
const pw = F.plane({ id: 'l3b', xmin: 0, xmax: 6, ymin: 0, ymax: 6, size: 1.35, ticks: 2,
  segments: [{ x1: 0, y1: 0, x2: 2, y2: 4, color: '#2563eb', w: 2.6 }, { x1: 2, y1: 4, x2: 4, y2: 4, color: '#2563eb', w: 2.6 }, { x1: 4, y1: 4, x2: 6, y2: 1, color: '#2563eb', w: 2.6 }],
  labels: [{ x: 0.8, y: 3.4, t: 'up', fs: 9 }, { x: 3, y: 4.5, t: 'flat', fs: 9 }, { x: 5.4, y: 3.3, t: 'down', fs: 9 }] });
module.exports = {
  name: 'prealgebra-linear-functional-relationships', course: 'Pre-Algebra (8th Grade)', unitNo: 3, unitName: 'Linear and Functional Relationships',
  focus: 'functions, function rules, tables and graphs',
  morefocus: 'linear vs. nonlinear, rate of change, intervals and graphs in context',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['function', 'Each input has exactly one output.', '⟨y = 3x + 1⟩'],
      ['input / output', '⟨x⟩ goes in, ⟨y⟩ comes out.', '⟨x = 2 \\to y = 7⟩'],
      ['rate of change', 'Change in ⟨y⟩ ÷ change in ⟨x⟩ (the slope).', '$12 per hour'],
      ['initial value', 'The output when ⟨x = 0⟩ (the ⟨y⟩-intercept).', '⟨b⟩ in ⟨y = mx + b⟩'],
      ['linear', 'Constant rate of change; graph is a line.', '⟨y = -2x + 5⟩']] },
    { title: 'Is It a Function?', color: 'blue', kind: 'list', items: [
      'Table or ordered pairs: no input ⟨x⟩ repeats with a different output.', '⟨\\{(1, 4), (2, 5), (1, 6)\\}⟩ is <b>not</b> a function: ⟨x = 1⟩ has two outputs.',
      'Graph: <b>vertical line test</b>. A vertical line may cross the graph at most once.', 'Outputs may repeat: ⟨\\{(1, 3), (2, 3)\\}⟩ is a function.'] },
    { title: 'Writing a Function Rule', color: 'green', kind: 'example', text: 'Find the rate of change from a table, then the starting value.',
      example: '⟨x⟩: 0, 1, 2, 3 &nbsp; ⟨y⟩: 5, 8, 11, 14', steps: [['Rate:', 'each step adds 3, so ⟨m = 3⟩'], ['Start:', 'at ⟨x = 0⟩, ⟨y = 5⟩']], answer: '⟨y = 3x + 5⟩',
      check: { list: ['3*0+5', '3*1+5', '3*2+5', '3*3+5'], is: [5, 8, 11, 14] } },
    { title: 'Linear or Nonlinear?', color: 'orange', kind: 'table', plain: true, head: ['Linear', 'Nonlinear'], rows: [
      ['constant rate of change', 'rate of change varies'], ['graph is a straight line', 'graph curves or bends'], ['⟨y = mx + b⟩', '⟨y = x^2,\\ y = 2^x,\\ y = \\tfrac{1}{x}⟩'], ['⟨y⟩: 2, 5, 8, 11 (+3 each)', '⟨y⟩: 1, 4, 9, 16 (+3, +5, +7)']],
      check: { list: ['5-2', '8-5', '11-8'], is: [3, 3, 3] } },
    { title: 'Slope from Two Points', color: 'pink', kind: 'example', text: '⟨m = \\dfrac{y_2 - y_1}{x_2 - x_1}⟩ = rise ÷ run.',
      example: 'The line through ⟨(0, -1)⟩ and ⟨(2, 3)⟩', steps: [['Slope:', '⟨\\tfrac{3 - (-1)}{2 - 0} = \\tfrac{4}{2} = 2⟩'], ['Intercept:', '⟨b = -1⟩']], answer: '⟨y = 2x - 1⟩', fig: lin,
      check: [{ num: '(3-(-1))/(2-0)', is: 2 }, { num: '2*2-1', is: 3 }] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Subtract in the same order on top and bottom of the slope formula.', 'The initial value is where the graph meets the ⟨y⟩-axis.', 'Units of the rate: ⟨y⟩-units per ⟨x⟩-unit.'],
      bad: [['Run over rise', 'slope is rise over run'], ['Calling repeated outputs "not a function"', 'only repeated inputs matter'], ['Assuming every table is linear', 'check the differences']] }
  ],
  back: [
    { title: 'Three Ways to Show a Line', color: 'purple', kind: 'table', plain: true, head: ['Form', '⟨y = 4x - 2⟩'], rows: [
      ['Equation', 'slope 4, ⟨y⟩-intercept −2'], ['Table', '⟨x⟩: 0, 1, 2 → ⟨y⟩: −2, 2, 6'], ['Graph', 'start at ⟨(0, -2)⟩, up 4, right 1'], ['Words', 'start at −2 and add 4 each time']],
      check: { list: ['4*0-2', '4*1-2', '4*2-2'], is: [-2, 2, 6] } },
    { title: 'Comparing Functions', color: 'blue', kind: 'example', text: 'Compare rates (slopes) and initial values, even when the functions are shown in different ways.',
      example: 'A: ⟨y = 3x + 10⟩. B: table ⟨(0, 4), (2, 12)⟩. Which grows faster?', steps: [['Rate of B:', '⟨\\tfrac{12 - 4}{2 - 0} = 4⟩'], ['Compare:', '⟨4 > 3⟩']], answer: 'B grows faster; A starts higher',
      check: { num: '(12-4)/(2-0)', is: 4 } },
    { title: 'Increasing and Decreasing', color: 'green', kind: 'html', html: 'Read the graph from <b>left to right</b>. <b>Increasing</b>: going up. <b>Decreasing</b>: going down. <b>Constant</b>: flat. A <b>maximum</b> is the highest point; a <b>minimum</b> is the lowest.<br>Here: increasing from ⟨x = 0⟩ to 2, constant from 2 to 4, decreasing from 4 to 6; maximum value 4.', fig: pw },
    { title: 'Rate of Change in Context', color: 'orange', kind: 'example', text: 'The slope tells how much the output changes for each 1 unit of input. Include units.',
      example: 'A plant is 6 cm tall and grows 1.5 cm per week: ⟨h = 1.5w + 6⟩. Height after 8 weeks?', steps: [['Substitute:', '⟨h = 1.5(8) + 6⟩']], answer: '18 cm (rate 1.5 cm/week, start 6 cm)',
      check: { num: '1.5*8+6', is: 18 } },
    { title: 'Sketching from a Story', color: 'pink', kind: 'list', items: [
      'Label the axes (time is usually ⟨x⟩).', 'Break the story into pieces: each piece is one segment.', 'Steeper segment = faster change. Flat segment = no change.',
      '"Walks to school, waits at the bus stop, then rides the bus": slow rise, flat, steep rise.'] },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Does each input have only one output?', 'Is the rate of change constant (linear) or not?', 'Did I read the graph from left to right?', 'Did I state the rate and starting value with units?'] }
  ]
};
