/* Pre-Algebra (8th Grade) Unit 2 cheat sheet. Every worked example is checked by build.cjs. */
module.exports = {
  name: 'prealgebra-equations-expressions', course: 'Pre-Algebra (8th Grade)', unitNo: 2, unitName: 'Equations and Expressions',
  focus: 'expressions with exponents and roots, writing linear equations',
  morefocus: 'variables on both sides, the distributive property and the number of solutions',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['expression', 'Numbers, variables and operations; no equals sign.', '⟨3x^2 - 5⟩'],
      ['equation', 'Two expressions that are equal.', '⟨2x + 1 = 9⟩'],
      ['like terms', 'Same variable raised to the same power.', '⟨4x⟩ and ⟨-7x⟩'],
      ['coefficient', 'The number multiplying a variable.', '6 in ⟨6y⟩'],
      ['solution', 'A value that makes the equation true.', '⟨x = 4⟩ in ⟨2x + 1 = 9⟩']] },
    { title: 'Expressions with Exponents', color: 'blue', kind: 'example', text: 'Use the order of operations: parentheses, exponents, multiply/divide, add/subtract. Use the exponent rules to simplify.',
      example: 'Evaluate ⟨2x^3 - 4x^{-1}⟩ for ⟨x = 2⟩.', steps: [['Substitute:', '⟨2(2)^3 - 4(2)^{-1}⟩'], ['Simplify:', '⟨2(8) - 4 \\cdot \\tfrac{1}{2} = 16 - 2⟩']], answer: '⟨14⟩',
      check: { num: '2*2**3-4*2**-1', is: 14 } },
    { title: 'Expressions with Roots', color: 'green', kind: 'table', plain: true, head: ['Expression', 'Simplified'], rows: [
      ['⟨\\sqrt{x^2}⟩', '⟨|x|⟩ (a root is never negative)'], ['⟨\\sqrt{25x^4}⟩', '⟨5x^2⟩'], ['⟨\\sqrt[3]{27y^3}⟩', '⟨3y⟩'], ['⟨\\sqrt{16} + \\sqrt[3]{-8}⟩', '⟨4 + (-2) = 2⟩']],
      after: 'Square roots undo squaring; cube roots undo cubing.', check: [{ num: 'Math.sqrt(25*3**4)', is: 45 }, { num: 'Math.cbrt(27*2**3)', is: 6 }, { num: 'Math.sqrt(16)+Math.cbrt(-8)', is: 2 }] },
    { title: 'Writing Linear Equations', color: 'orange', kind: 'example', text: 'Name the unknown, translate the words, then solve. Key words: "is" =, "per/each" ×, "more than" +.',
      example: 'A gym charges $25 to join plus $15 per month. Sam paid $130. How many months?', steps: [['Equation:', '⟨25 + 15m = 130⟩'], ['Solve:', '⟨15m = 105⟩']], answer: '⟨m = 7⟩ months',
      check: { num: '(130-25)/15', is: 7 } },
    { title: 'Combining Like Terms', color: 'pink', kind: 'example', text: 'Collect like terms on each side first, then solve with inverse operations.',
      example: '⟨5x - 3 + 2x + 8 = 26⟩', steps: [['Combine:', '⟨7x + 5 = 26⟩'], ['Subtract 5, divide by 7:', '⟨7x = 21⟩']], answer: '⟨x = 3⟩',
      check: { num: '5*3-3+2*3+8', is: 26 } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Do the same thing to both sides.', 'Distribute to every term inside the parentheses.', 'Check by substituting your answer.'],
      bad: [['⟨-2(x - 3) = -2x - 6⟩', 'it is ⟨-2x + 6⟩'], ['Combining ⟨3x + 2 = 5x⟩', '3x and 2 are not like terms'], ['⟨x^2 = 16 \\Rightarrow x = 8⟩', 'take the square root: ⟨x = \\pm 4⟩']] }
  ],
  back: [
    { title: 'Variables on Both Sides', color: 'purple', kind: 'example', text: 'Move the variable terms to one side and the numbers to the other.',
      example: '⟨7x - 4 = 3x + 12⟩', steps: [['Subtract ⟨3x⟩:', '⟨4x - 4 = 12⟩'], ['Add 4, divide by 4:', '⟨4x = 16⟩']], answer: '⟨x = 4⟩',
      check: { num: '7*4-4 - (3*4+12)', is: 0 } },
    { title: 'The Distributive Property', color: 'blue', kind: 'example', text: '⟨a(b + c) = ab + ac⟩. Distribute first, then combine like terms.',
      example: '⟨3(2x - 5) = 4(x + 1) + 3⟩', steps: [['Distribute:', '⟨6x - 15 = 4x + 4 + 3⟩'], ['Combine:', '⟨6x - 15 = 4x + 7⟩'], ['Solve:', '⟨2x = 22⟩']], answer: '⟨x = 11⟩',
      check: { num: '3*(2*11-5) - (4*(11+1)+3)', is: 0 } },
    { title: 'One, None or Infinitely Many', color: 'green', kind: 'table', plain: true, head: ['Simplifies to', 'Solutions'], rows: [
      ['⟨x = 5⟩ (a number)', '<b>one</b> solution'], ['⟨4 = 9⟩ (false)', '<b>no</b> solution'], ['⟨4 = 4⟩ (always true)', '<b>infinitely many</b>']],
      after: '⟨2(x + 3) = 2x + 6⟩ → ⟨6 = 6⟩: infinitely many. ⟨2x + 3 = 2x - 1⟩ → ⟨3 = -1⟩: none.', check: { expr: '2*(x+3)', is: '2*x+6' } },
    { title: 'Exponent Equations', color: 'orange', kind: 'table', plain: true, head: ['Equation', 'Solution'], rows: [
      ['⟨x^2 = 81⟩', '⟨x = \\pm 9⟩'], ['⟨x^3 = 125⟩', '⟨x = 5⟩'], ['⟨2x^2 = 50⟩', '⟨x^2 = 25,\\ x = \\pm 5⟩'], ['⟨x^2 = -4⟩', 'no real solution'], ['⟨x^2 = 7⟩', '⟨x = \\pm\\sqrt{7}⟩']],
      after: 'Get the power alone first, then take the square root (two answers) or the cube root (one answer).', check: [{ num: 'Math.cbrt(125)', is: 5 }, { num: 'Math.sqrt(50/2)', is: 5 }] },
    { title: 'Fractions in Equations', color: 'pink', kind: 'example', text: 'Multiply every term by the least common denominator to clear the fractions.',
      example: '⟨\\tfrac{x}{3} + \\tfrac{1}{2} = \\tfrac{5}{6}⟩', steps: [['Multiply by 6:', '⟨2x + 3 = 5⟩'], ['Solve:', '⟨2x = 2⟩']], answer: '⟨x = 1⟩',
      check: { num: '1/3+1/2', is: 0.8333333333333334 } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I distribute the sign as well as the number?', 'Did I combine like terms on each side before moving terms?', 'If the variable disappeared, is the statement true (infinitely many) or false (none)?',
      'Did I substitute my answer back into the original equation?'] }
  ]
};
