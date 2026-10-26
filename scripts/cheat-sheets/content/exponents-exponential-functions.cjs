const F = require('../figs.cjs');
module.exports = {
  name: 'exponents-exponential-functions', course: 'Algebra 1', unitNo: 8, unitName: 'Exponential Functions',
  focus: 'exponential functions, growth and decay',
  morefocus: 'writing models, compound interest, geometric sequences and solving equations',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['exponential function', 'The variable is in the exponent.', '⟨f(x) = 3 \\cdot 2^x⟩'], ['initial value', 'The starting amount ⟨a⟩ (value at ⟨x = 0⟩).', '⟨a = 3⟩'],
      ['growth factor', '⟨b > 1⟩: multiply by ⟨b⟩ each step.', '⟨1.05⟩ = 5% growth'], ['decay factor', '⟨0 < b < 1⟩: the amount shrinks.', '⟨0.8⟩ = 20% decay'],
      ['asymptote', 'A line the graph approaches but never reaches.', '⟨y = 0⟩']] },
    { title: 'The Exponential Form', color: 'blue', kind: 'table', head: ['Part', 'Meaning'], rows: [
      ['⟨a⟩', 'initial value (the y-intercept)'], ['⟨b⟩', 'the factor ⟨y⟩ is multiplied by each time ⟨x⟩ goes up 1'], ['⟨b = 1 + r⟩', 'growth at rate ⟨r⟩'], ['⟨b = 1 - r⟩', 'decay at rate ⟨r⟩']],
      after: '⟨y = 200(1.10)^x⟩: starts at 200 and grows 10% each step.' },
    { title: 'Growth vs. Decay', color: 'green', kind: 'html', html: '<b>Growth</b> ⟨b > 1⟩: rises left to right. <b>Decay</b> ⟨0 < b < 1⟩: falls. Both cross the y-axis at ⟨(0, a)⟩ and approach the asymptote ⟨y = 0⟩.',
      fig: '<div style="display:flex;gap:8px;justify-content:center;font-size:7.5pt;text-align:center"><div>' + F.plane({ id: 'eg', xmin: -3, xmax: 3, ymin: -1, ymax: 7, size: 0.9, fns: [{ f: x => Math.pow(2, x), color: '#16a34a' }], points: [{ x: 0, y: 1, label: '(0,1)' }] }) + '<br>⟨y = 2^x⟩</div><div>'.replace('⟨y = 2^x⟩', 'y = 2ˣ') + F.plane({ id: 'ed', xmin: -3, xmax: 3, ymin: -1, ymax: 7, size: 0.9, fns: [{ f: x => Math.pow(0.5, x), color: '#db2777' }], points: [{ x: 0, y: 1, label: '(0,1)' }] }) + '<br>y = (½)ˣ</div></div>' },
    { title: 'Evaluate', color: 'orange', kind: 'example', text: 'Exponent first, then multiply by ⟨a⟩.',
      example: '⟨f(x) = 3(2)^x⟩. Find ⟨f(4)⟩.', steps: [['Substitute:', '⟨3(2)^4 = 3(16)⟩']], answer: '⟨48⟩', check: { num: '3*2**4', is: 48 } },
    { title: 'Linear or Exponential?', color: 'pink', kind: 'table', head: ['', 'Linear', 'Exponential'], rows: [
      ['pattern', 'add the same amount', 'multiply by the same factor'], ['table', 'x: 0, 1, 2 → y: 5, 8, 11', 'x: 0, 1, 2 → y: 5, 10, 20'], ['equation', '⟨y = mx + b⟩', '⟨y = a \\cdot b^x⟩']],
      after: 'An increasing exponential eventually passes any linear function.' },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['⟨a⟩ is the value when ⟨x = 0⟩.', 'Percent → decimal: 6% growth → ⟨b = 1.06⟩.', 'Check for a constant <b>ratio</b> (divide consecutive ⟨y⟩-values).'],
      bad: [['⟨3(2)^4 \\ne 6^4⟩', 'do the power first: ⟨3 \\cdot 16⟩'], ['20% decay is not ⟨b = 0.2⟩', 'it is ⟨b = 0.8⟩'], ['Subtracting ⟨y⟩-values', 'that tests linear, not exponential']] }
  ],
  back: [
    { title: 'Write from a Table', color: 'purple', kind: 'example', text: 'Find ⟨a⟩ (the value at ⟨x = 0⟩) and ⟨b⟩ (divide consecutive outputs).',
      example: 'x: 0, 1, 2, 3 → y: 5, 10, 20, 40', steps: [['⟨a⟩:', '⟨5⟩'], ['⟨b⟩:', '⟨10 \\div 5 = 2⟩']], answer: '⟨y = 5(2)^x⟩', check: { list: ['5*2**0', '5*2**1', '5*2**2', '5*2**3'], is: [5, 10, 20, 40] } },
    { title: 'Growth & Decay in Context', color: 'blue', kind: 'example', text: 'Growth: ⟨y = a(1 + r)^t⟩. Decay: ⟨y = a(1 - r)^t⟩.',
      example: 'A town of 8,000 grows 3% per year. Population after 5 years?', steps: [['Model:', '⟨y = 8000(1.03)^t⟩'], ['⟨t = 5⟩:', '⟨8000(1.03)^5 \\approx 9274⟩']], answer: 'about 9,274 people', check: { num: 'Math.round(8000*1.03**5)', is: 9274 } },
    { title: 'Compound Interest', color: 'green', kind: 'example', text: '⟨A = P\\left(1 + \\dfrac{r}{n}\\right)^{nt}⟩, with ⟨n⟩ compounding periods per year.',
      example: '$1,000 at 6% compounded monthly for 2 years.', steps: [['Substitute:', '⟨1000\\left(1 + \\tfrac{0.06}{12}\\right)^{24}⟩']], answer: '$1,127.16', check: { num: 'Math.round(1000*(1+0.06/12)**24*100)/100', is: 1127.16 } },
    { title: 'Geometric Sequences', color: 'orange', kind: 'example', text: 'Multiply by the common ratio ⟨r⟩: ⟨a_n = a_1 \\cdot r^{n-1}⟩.',
      example: '⟨3, 6, 12, 24, \\dots⟩: find ⟨a_8⟩.', steps: [['⟨r⟩:', '⟨6 \\div 3 = 2⟩'], ['⟨n = 8⟩:', '⟨3 \\cdot 2^7 = 384⟩']], answer: '⟨384⟩', check: { num: '3*2**7', is: 384 } },
    { title: 'Solving with a Common Base', color: 'pink', kind: 'example', text: 'Write both sides with the same base, then set the exponents equal.',
      example: 'Solve ⟨8^x = 2^{x + 6}⟩.', steps: [['Rewrite:', '⟨2^{3x} = 2^{x + 6}⟩'], ['Exponents:', '⟨3x = x + 6,\\ x = 3⟩']], answer: '⟨x = 3⟩', check: { num: '8**3 - 2**(3+6)', is: 0 } },
    { title: 'Key Features of the Graph', color: 'teal', kind: 'list', items: [
      'For ⟨y = a \\cdot b^x⟩ with ⟨a > 0⟩: <b>domain</b> all real numbers. <b>Range</b>: ⟨y > 0⟩.', '<b>y-intercept</b>: ⟨(0, a)⟩.', '<b>Asymptote</b>: ⟨y = 0⟩.', 'Half-life: the amount halves each period, ⟨b = \\tfrac{1}{2}⟩.'] }
  ]
};
