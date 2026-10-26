const F = require('../figs.cjs');
module.exports = {
  name: 'exponential-logarithmic-functions', course: 'Algebra 2', unitNo: 6, unitName: 'Exponential & Log Functions',
  focus: 'exponential functions, the number e and the logarithm',
  morefocus: 'log properties, solving equations and modeling',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['exponential function', '⟨f(x) = a \\cdot b^x⟩, ⟨b > 0⟩, ⟨b \\ne 1⟩.', '⟨3(1.05)^x⟩'], ['e', 'Irrational constant ⟨\\approx 2.71828⟩; continuous growth.', '⟨Pe^{rt}⟩'],
      ['logarithm', '⟨\\log_b x = y⟩ means ⟨b^y = x⟩: the log is an exponent.', '⟨\\log_2 8 = 3⟩'], ['common / natural log', '⟨\\log x⟩ is base 10; ⟨\\ln x⟩ is base ⟨e⟩.', '⟨\\log 100 = 2⟩'],
      ['extraneous', 'A result that fails in the original (log of a number ⟨\\le 0⟩).', '⟨x = -2⟩']] },
    { title: 'Growth & Decay', color: 'blue', kind: 'html', html: '⟨f(x) = a \\cdot b^x⟩. Growth ⟨b = 1 + r > 1⟩; decay ⟨b = 1 - r⟩. Domain all reals, range ⟨y > 0⟩ (⟨a > 0⟩), y-intercept ⟨(0, a)⟩, asymptote ⟨y = 0⟩.',
      fig: F.plane({ id: 'gd', xmin: -3, xmax: 3, ymin: -1, ymax: 8, size: 1.05, fns: [{ f: x => Math.pow(2, x), color: '#2563eb' }, { f: x => Math.pow(0.5, x), color: '#db2777' }], points: [{ x: 0, y: 1, label: '(0, 1)', dx: 6 }], labels: [{ x: 2.2, y: 6.6, t: 'y = 2ˣ', color: '#2563eb' }, { x: -2.1, y: 6.6, t: 'y = (½)ˣ', color: '#db2777' }] }) },
    { title: 'Transformations', color: 'green', kind: 'example', text: '⟨g(x) = a \\cdot b^{x - h} + k⟩: right ⟨h⟩, up ⟨k⟩ (the asymptote moves to ⟨y = k⟩), ⟨a < 0⟩ reflects.',
      example: '⟨f(x) = 2^{x + 1} - 3⟩', steps: [['Shift:', 'left 1, down 3'], ['Asymptote:', '⟨y = -3⟩; y-int ⟨2^1 - 3 = -1⟩']], answer: 'range ⟨y > -3⟩', check: { num: '2**1-3', is: -1 } },
    { title: 'The Number e & Interest', color: 'orange', kind: 'example', text: '⟨n⟩ times a year: ⟨A = P\\left(1 + \\tfrac{r}{n}\\right)^{nt}⟩. Continuously: ⟨A = Pe^{rt}⟩.',
      example: '$2,000 at 5% for 6 years', steps: [['Quarterly:', '⟨2000(1.0125)^{24} \\approx 2694.70⟩'], ['Continuous:', '⟨2000e^{0.3} \\approx 2699.72⟩']], answer: '$2,694.70 and $2,699.72',
      check: { list: ['Math.round(2000*1.0125**24*100)/100', 'Math.round(2000*Math.exp(0.3)*100)/100'], is: [2694.70, 2699.72] } },
    { title: 'Log ↔ Exponential Form', color: 'pink', kind: 'table', head: ['Exponential', 'Logarithmic'], rows: [
      ['⟨2^5 = 32⟩', '⟨\\log_2 32 = 5⟩'], ['⟨9^{1/2} = 3⟩', '⟨\\log_9 3 = \\tfrac{1}{2}⟩'], ['⟨10^{-2} = 0.01⟩', '⟨\\log 0.01 = -2⟩'], ['⟨e^4 = x⟩', '⟨\\ln x = 4⟩']],
      after: 'Special values: ⟨\\log_b 1 = 0⟩, ⟨\\log_b b = 1⟩, ⟨\\log_b b^x = x⟩, ⟨b^{\\log_b x} = x⟩.', check: { list: ['2**5', '9**0.5', '10**-2'], is: [32, 3, 0.01] } },
    { title: 'Log Graphs', color: 'teal', kind: 'html', html: '⟨y = \\log_b x⟩ is the inverse of ⟨y = b^x⟩. Domain ⟨x > 0⟩, range all reals, asymptote ⟨x = 0⟩, through ⟨(1, 0)⟩ and ⟨(b, 1)⟩. ⟨\\log_3(2x - 6)⟩ needs ⟨x > 3⟩.',
      fig: F.plane({ id: 'lg', xmin: -3, xmax: 6, ymin: -3, ymax: 6, size: 1.05, fns: [{ f: x => Math.pow(2, x), color: '#2563eb' }, { f: x => x > 0.02 ? Math.log2(x) : NaN, from: 0.02, color: '#16a34a' }, { f: x => x, color: '#999', dashed: true }], labels: [{ x: 4.6, y: 1.4, t: 'log₂x', color: '#16a34a' }, { x: 1.3, y: 5.4, t: '2ˣ', color: '#2563eb' }] }) }
  ],
  back: [
    { title: 'Properties of Logs', color: 'purple', kind: 'table', head: ['Rule', 'Statement'], rows: [
      ['Product', '⟨\\log_b(MN) = \\log_b M + \\log_b N⟩'], ['Quotient', '⟨\\log_b\\tfrac{M}{N} = \\log_b M - \\log_b N⟩'], ['Power', '⟨\\log_b(M^p) = p\\log_b M⟩'], ['Change of base', '⟨\\log_b x = \\tfrac{\\ln x}{\\ln b}⟩']],
      after: '✘ ⟨\\log(a + b) \\ne \\log a + \\log b⟩. ⟨\\log_5 40 = \\tfrac{\\ln 40}{\\ln 5} \\approx 2.2920⟩.', check: { num: 'Math.round(Math.log(40)/Math.log(5)*10000)/10000', is: 2.292 } },
    { title: 'Expanding & Condensing', color: 'blue', kind: 'words', rows: [
      ['Expand ⟨\\log_2 \\tfrac{8x^3}{y}⟩', '⟨3 + 3\\log_2 x - \\log_2 y⟩'], ['Condense ⟨2\\ln x + \\ln 5 - \\ln y⟩', '⟨\\ln \\tfrac{5x^2}{y}⟩'], ['⟨\\log_6 4 + \\log_6 9 = \\log_6 36⟩', '⟨2⟩']],
      check: { num: 'Math.log(36)/Math.log(6)', is: 2 } },
    { title: 'Solving Exponential Equations', color: 'green', kind: 'example', text: 'Same base: set exponents equal. Otherwise isolate the power and take a log of both sides.',
      example: '⟨2 \\cdot 5^x = 70⟩', steps: [['Isolate:', '⟨5^x = 35⟩'], ['Log:', '⟨x = \\dfrac{\\log 35}{\\log 5}⟩']], answer: '⟨x \\approx 2.209⟩', check: { num: 'Math.round(Math.log(35)/Math.log(5)*1000)/1000', is: 2.209 } },
    { title: 'Solving Log Equations (Check!)', color: 'orange', kind: 'example', text: 'Condense, convert to exponential form, solve, and reject answers that make a log argument ⟨\\le 0⟩.',
      example: '⟨\\log_2 x + \\log_2(x - 2) = 3⟩', steps: [['Condense:', '⟨x(x - 2) = 2^3 = 8⟩'], ['Solve:', '⟨(x - 4)(x + 2) = 0⟩']], answer: '⟨x = 4⟩ (reject ⟨-2⟩)', check: { num: 'Math.log2(4)+Math.log2(2)', is: 3 } },
    { title: 'Modeling Formulas', color: 'pink', kind: 'words', rows: [
      ['Growth or decay', '⟨y = a(1 \\pm r)^t⟩'], ['Continuous', '⟨A = Pe^{rt}⟩'], ['Half-life ⟨h⟩', '⟨N = N_0\\left(\\tfrac{1}{2}\\right)^{t/h}⟩'], ['Doubling time (continuous)', '⟨t = \\tfrac{\\ln 2}{r}⟩'], ['pH', '⟨-\\log[H^+]⟩']] },
    { title: 'Real-World Example', color: 'teal', kind: 'example', text: 'Isolate the exponential part, then take ⟨\\ln⟩ (or ⟨\\log⟩) of both sides.',
      example: '⟨P = 500e^{0.04t}⟩. When is ⟨P = 2000⟩?', steps: [['Isolate:', '⟨e^{0.04t} = 4⟩'], ['ln:', '⟨t = \\dfrac{\\ln 4}{0.04}⟩']], answer: 'about 34.7 years', check: { num: 'Math.round(Math.log(4)/0.04*10)/10', is: 34.7 } }
  ]
};
