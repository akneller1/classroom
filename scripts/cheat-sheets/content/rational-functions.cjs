const F = require('../figs.cjs');
module.exports = {
  name: 'rational-functions', course: 'Algebra 2', unitNo: 7, unitName: 'Rational Functions',
  focus: 'simplifying, multiplying, dividing, adding and subtracting rational expressions, and solving rational equations',
  morefocus: 'asymptotes and holes, graphing, transformations of 1/x, variation and work problems',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['rational expression', 'A ratio of polynomials ⟨\\tfrac{P}{Q}⟩, ⟨Q \\ne 0⟩.', '⟨\\tfrac{x + 1}{x - 3}⟩'], ['excluded value', 'Makes the original denominator 0.', '⟨x = 3⟩'],
      ['vertical asymptote', 'Line ⟨x = a⟩ the graph approaches but never crosses.', '⟨x = 3⟩'], ['horizontal asymptote', 'Value ⟨y⟩ approaches as ⟨x \\to \\pm\\infty⟩.', '⟨y = 1⟩'],
      ['hole', 'A missing point from a canceled factor.', '⟨(2, 4)⟩']] },
    { title: 'Simplifying', color: 'blue', kind: 'example', text: 'Factor completely, list excluded values <b>before</b> canceling, then cancel common factors.',
      example: '⟨\\dfrac{x^2 - 9}{x^2 + x - 6}⟩', steps: [['Factor:', '⟨\\dfrac{(x - 3)(x + 3)}{(x + 3)(x - 2)}⟩'], ['Exclude:', '⟨x \\ne -3,\\ 2⟩']], answer: '⟨\\dfrac{x - 3}{x - 2}⟩',
      check: { expr: '(x*x-9)/(x*x+x-6)', is: '(x-3)/(x-2)' } },
    { title: 'Multiplying & Dividing', color: 'green', kind: 'words', rows: [
      ['⟨\\dfrac{x^2 - 4}{x + 1} \\cdot \\dfrac{x + 1}{x - 2}⟩', '⟨x + 2⟩ (⟨x \\ne -1, 2⟩)'], ['⟨\\dfrac{x}{x - 3} \\div \\dfrac{x^2}{x^2 - 9}⟩', '⟨\\dfrac{x + 3}{x}⟩ (⟨x \\ne 0, \\pm 3⟩)'],
      ['⟨\\dfrac{2x}{5} \\cdot \\dfrac{15}{x^2}⟩', '⟨\\dfrac{6}{x}⟩']], after: 'To divide, multiply by the reciprocal. Factor first, then cancel.',
      check: [{ expr: '(x*x-4)/(x+1)*(x+1)/(x-2)', is: 'x+2' }, { expr: '(x/(x-3))/(x*x/(x*x-9))', is: '(x+3)/x' }, { expr: '2*x/5*15/(x*x)', is: '6/x' }] },
    { title: 'Adding & Subtracting', color: 'orange', kind: 'example', text: 'Find the LCD, rewrite each fraction over it, combine numerators, simplify.',
      example: '⟨\\dfrac{2}{x - 1} + \\dfrac{3}{x + 2}⟩', steps: [['LCD:', '⟨(x - 1)(x + 2)⟩'], ['Numerator:', '⟨2(x + 2) + 3(x - 1) = 5x + 1⟩']], answer: '⟨\\dfrac{5x + 1}{(x - 1)(x + 2)}⟩',
      check: { expr: '2/(x-1)+3/(x+2)', is: '(5*x+1)/((x-1)*(x+2))' } },
    { title: 'Solving Rational Equations', color: 'pink', kind: 'example', text: 'Multiply every term by the LCD, solve, and reject any excluded value.',
      example: '⟨\\dfrac{x}{x - 2} + 1 = \\dfrac{2}{x - 2}⟩', steps: [['Times ⟨(x - 2)⟩:', '⟨x + (x - 2) = 2 \\to x = 2⟩'], ['Check:', '⟨x = 2⟩ makes a denominator 0 ✘']], answer: 'no solution',
      check: { num: '(2+(2-2))/2', is: 1 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['State excluded values from the <b>original</b> denominators.', 'Cancel factors, never terms.', 'Check solutions against the excluded values.'],
      bad: [['⟨\\tfrac{x + 5}{x} = 5⟩', 'you cannot cancel the ⟨x⟩ terms'], ['⟨\\tfrac{1}{a} + \\tfrac{1}{b} = \\tfrac{2}{a + b}⟩', 'it is ⟨\\tfrac{a + b}{ab}⟩'], ['Subtracting ⟨\\tfrac{x - 1}{x + 2}⟩ without parentheses', 'distribute the minus to the whole numerator']],
      check: { num: '1/2+1/3', is: (2 + 3) / 6 } }
  ],
  back: [
    { title: 'Asymptotes & Holes', color: 'purple', kind: 'table', plain: true, rows: [
      ['Hole', 'factor that cancels; plug ⟨x⟩ into the simplified form'], ['Vertical asymptote', 'zero of the denominator after canceling'], ['HA: deg top < deg bottom', '⟨y = 0⟩'],
      ['HA: degrees equal', '⟨y = \\tfrac{\\text{lead coeff. top}}{\\text{lead coeff. bottom}}⟩'], ['deg top > deg bottom', 'no HA (slant if one more)']] },
    { title: 'Graphing Example', color: 'blue', kind: 'example', text: 'Find the asymptotes and intercepts, then test points on each side.',
      example: '⟨f(x) = \\dfrac{2x + 1}{x - 1}⟩', steps: [['Asymptotes:', '⟨x = 1⟩, ⟨y = 2⟩'], ['Intercepts:', '⟨(-\\tfrac{1}{2}, 0)⟩, ⟨(0, -1)⟩']], answer: 'two branches around ⟨(1, 2)⟩',
      fig: F.plane({ id: 'rg', xmin: -5, xmax: 6, ymin: -5, ymax: 9, size: 1.45, ticks: 2, fns: [{ f: x => (2 * x + 1) / (x - 1), to: 0.6 }, { f: x => (2 * x + 1) / (x - 1), from: 1.35 }, { f: x => 2, color: '#db2777', dashed: true }], vlines: [{ x: 1 }], points: [{ x: -0.5, y: 0 }, { x: 0, y: -1 }] }),
      check: { list: ['(2*0+1)/(0-1)', '(2*(-0.5)+1)'], is: [-1, 0] } },
    { title: 'Holes vs. Asymptotes', color: 'green', kind: 'example', text: 'A canceled factor gives a hole; a factor left in the denominator gives an asymptote.',
      example: '⟨g(x) = \\dfrac{x^2 + x - 2}{x^2 - 4}⟩', steps: [['Factor:', '⟨\\dfrac{(x + 2)(x - 1)}{(x + 2)(x - 2)} = \\dfrac{x - 1}{x - 2}⟩'], ['Hole:', '⟨x = -2⟩: ⟨\\tfrac{-3}{-4} = \\tfrac{3}{4}⟩']], answer: 'hole ⟨(-2, \\tfrac{3}{4})⟩; VA ⟨x = 2⟩; HA ⟨y = 1⟩',
      check: [{ expr: '(x*x+x-2)/(x*x-4)', is: '(x-1)/(x-2)' }, { num: '(-2-1)/(-2-2)', is: 0.75 }] },
    { title: 'Transformations of 1/x', color: 'orange', kind: 'example', text: '⟨y = \\dfrac{a}{x - h} + k⟩ has VA ⟨x = h⟩ and HA ⟨y = k⟩. ⟨a < 0⟩ flips the branches into the other quadrants.',
      example: '⟨y = \\dfrac{3}{x + 2} - 1⟩', steps: [['Shift:', 'left 2, down 1'], ['Points:', '⟨(-1, 2)⟩, ⟨(-3, -4)⟩']], answer: 'VA ⟨x = -2⟩, HA ⟨y = -1⟩', check: { list: ['3/(-1+2)-1', '3/(-3+2)-1'], is: [2, -4] } },
    { title: 'Variation', color: 'pink', kind: 'words', rows: [
      ['Inverse: ⟨y = \\tfrac{k}{x}⟩; ⟨y = 6⟩ when ⟨x = 4⟩. Find ⟨y⟩ when ⟨x = 8⟩.', '⟨k = 24⟩, ⟨y = 3⟩'], ['Joint: ⟨z = kxy⟩; ⟨z = 60⟩ when ⟨x = 3, y = 4⟩.', '⟨k = 5⟩'],
      ['Combined: ⟨y = \\tfrac{kx}{z}⟩; ⟨y = 10⟩ when ⟨x = 5, z = 2⟩.', '⟨k = 4⟩']], check: { list: ['24/8', '60/12', '10*2/5'], is: [3, 5, 4] } },
    { title: 'Work & Rate Problems', color: 'teal', kind: 'example', text: 'Add the rates (jobs per hour): ⟨\\tfrac{1}{a} + \\tfrac{1}{b} = \\tfrac{1}{t}⟩.',
      example: 'Pipe A fills a tank in 3 h, pipe B in 6 h. Together?', steps: [['Rates:', '⟨\\tfrac{1}{3} + \\tfrac{1}{6} = \\tfrac{1}{2}⟩ tank per hour'], ['Time:', '⟨\\tfrac{1}{t} = \\tfrac{1}{2}⟩']], answer: '⟨t = 2⟩ hours',
      check: { num: '1/(1/3+1/6)', is: 2 } }
  ]
};
