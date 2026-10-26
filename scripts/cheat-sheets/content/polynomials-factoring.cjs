module.exports = {
  name: 'polynomials-factoring', course: 'Algebra 1', unitNo: 10, unitName: 'Factoring and Zero Product',
  focus: 'factoring GCF, trinomials, special patterns and grouping',
  morefocus: 'factoring completely and solving quadratics with the Zero Product Property',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['factor', 'Write as a product (undo distributing).', '⟨6x + 9 = 3(2x + 3)⟩'], ['GCF', 'Greatest common factor of every term.', '⟨3x^2⟩ in ⟨6x^3 + 9x^2⟩'],
      ['trinomial', 'A polynomial with three terms.', '⟨x^2 + 7x + 12⟩'], ['prime', 'Cannot be factored over the integers.', '⟨x^2 + 4⟩'], ['zero / root', 'An ⟨x⟩ that makes the expression 0.', '⟨x = -3⟩']] },
    { title: 'Factor Out the GCF', color: 'blue', kind: 'example', text: 'Find the largest number and the lowest power of each variable that divide every term.',
      example: 'Factor ⟨6x^3 + 9x^2⟩.', steps: [['GCF:', '⟨3x^2⟩'], ['Divide each term:', '⟨2x⟩ and ⟨3⟩']], answer: '⟨3x^2(2x + 3)⟩', check: { expr: '3*x**2*(2*x+3)', is: '6*x**3+9*x**2' } },
    { title: 'Trinomials, Leading Coefficient 1', color: 'green', kind: 'example', text: 'Find two numbers that <b>multiply to c</b> and <b>add to b</b>.',
      example: 'Factor ⟨x^2 + 7x + 12⟩.', steps: [['Multiply to 12, add to 7:', '⟨3⟩ and ⟨4⟩']], answer: '⟨(x + 3)(x + 4)⟩', check: { expr: '(x+3)*(x+4)', is: 'x**2+7*x+12' } },
    { title: 'Trinomials: the AC Method', color: 'orange', kind: 'example', text: 'AC method: find two numbers that multiply to ⟨ac⟩ and add to ⟨b⟩, split the middle term, then group.',
      example: 'Factor ⟨2x^2 + 7x + 3⟩.', steps: [['⟨ac = 6⟩:', '⟨6 \\cdot 1⟩, sum 7'], ['Split:', '⟨2x^2 + 6x + x + 3⟩'], ['Group:', '⟨2x(x + 3) + 1(x + 3)⟩']], answer: '⟨(2x + 1)(x + 3)⟩', check: { expr: '(2*x+1)*(x+3)', is: '2*x**2+7*x+3' } },
    { title: 'Special Patterns', color: 'pink', kind: 'table', head: ['Pattern', 'Factors', 'Example'], rows: [
      ['⟨a^2 - b^2⟩', '⟨(a - b)(a + b)⟩', '⟨x^2 - 25 = (x - 5)(x + 5)⟩'], ['⟨a^2 + 2ab + b^2⟩', '⟨(a + b)^2⟩', '⟨x^2 + 8x + 16 = (x + 4)^2⟩'], ['⟨a^2 - 2ab + b^2⟩', '⟨(a - b)^2⟩', '⟨x^2 - 6x + 9 = (x - 3)^2⟩']],
      after: 'A <b>sum</b> of squares like ⟨x^2 + 25⟩ is prime.', check: [{ expr: '(x-5)*(x+5)', is: 'x**2-25' }, { expr: '(x+4)**2', is: 'x**2+8*x+16' }, { expr: '(x-3)**2', is: 'x**2-6*x+9' }] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Always take out the GCF first.', 'Check signs: ⟨c > 0⟩ → same signs; ⟨c < 0⟩ → different signs.', 'Multiply the factors back to check.'],
      bad: [['Right product, wrong sum', 'both conditions must hold'], ['⟨x^2 - 9 \\ne (x - 3)^2⟩', 'it is ⟨(x - 3)(x + 3)⟩'], ['Stopping too early', 'factor completely']] }
  ],
  back: [
    { title: 'Factoring by Grouping', color: 'purple', kind: 'example', text: 'Four terms: group in pairs, factor each pair, then factor out the common binomial.',
      example: 'Factor ⟨x^3 + 3x^2 + 2x + 6⟩.', steps: [['Group:', '⟨x^2(x + 3) + 2(x + 3)⟩']], answer: '⟨(x + 3)(x^2 + 2)⟩', check: { expr: '(x+3)*(x**2+2)', is: 'x**3+3*x**2+2*x+6' } },
    { title: 'Factor Completely', color: 'blue', kind: 'example', text: 'GCF first, then look again at what is left.',
      example: 'Factor ⟨3x^2 - 12⟩.', steps: [['GCF:', '⟨3(x^2 - 4)⟩'], ['Difference of squares:', '⟨3(x - 2)(x + 2)⟩']], answer: '⟨3(x - 2)(x + 2)⟩', check: { expr: '3*(x-2)*(x+2)', is: '3*x**2-12' } },
    { title: 'Strategy', color: 'green', kind: 'words', rows: [
      ['1. Is there a GCF?', 'factor it out'], ['2. Two terms: ⟨a^2 - b^2⟩?', 'difference of squares'], ['3. Three terms: perfect square or ⟨x^2 + bx + c⟩ / ⟨ax^2 + bx + c⟩?', 'pattern or AC method'], ['4. Four terms?', 'grouping'], ['5. Can any factor be factored again?', 'keep going']] },
    { title: 'Zero Product Property', color: 'orange', kind: 'example', text: 'If ⟨ab = 0⟩, then ⟨a = 0⟩ or ⟨b = 0⟩. Set each factor equal to zero.',
      example: 'Solve ⟨(x - 4)(2x + 6) = 0⟩.', steps: [['⟨x - 4 = 0⟩:', '⟨x = 4⟩'], ['⟨2x + 6 = 0⟩:', '⟨x = -3⟩']], answer: '⟨x = 4⟩ or ⟨x = -3⟩', check: { list: ['(4-4)*(2*4+6)', '(-3-4)*(2*(-3)+6)'], is: [0, 0] } },
    { title: 'Solving by Factoring', color: 'pink', kind: 'example', text: 'Get 0 on one side, factor, then use the Zero Product Property.',
      example: 'Solve ⟨x^2 + 2x = 15⟩.', steps: [['Standard form:', '⟨x^2 + 2x - 15 = 0⟩'], ['Factor:', '⟨(x + 5)(x - 3) = 0⟩']], answer: '⟨x = -5⟩ or ⟨x = 3⟩', check: { list: ['(-5)**2+2*(-5)', '3**2+2*3'], is: [15, 15] } },
    { title: 'Applications', color: 'teal', kind: 'example', text: 'Write the equation, solve by factoring, and reject answers that do not make sense.',
      example: 'A rectangle is 3 ft longer than it is wide; its area is 40 ft². Width?', steps: [['Equation:', '⟨w(w + 3) = 40⟩'], ['Factor:', '⟨(w + 8)(w - 5) = 0⟩']], answer: '5 ft (reject ⟨-8⟩)', check: { num: '5*(5+3)', is: 40 } }
  ]
};
