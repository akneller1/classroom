module.exports = {
  name: 'expressions-equations', course: 'Algebra 1', unitNo: 2, unitName: 'Solving Linear Equations',
  focus: 'solving one-step, two-step and multi-step equations, and checking solutions',
  morefocus: 'writing equations from words, proportions, percents and literal equations',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['equation', 'Two expressions with an equal sign.', '⟨2x + 3 = 11⟩'], ['solution', 'A value that makes the equation true.', '⟨x = 4⟩'],
      ['inverse operation', 'An operation that undoes another.', '⟨+\\ \\leftrightarrow\\ -⟩, ⟨\\times\\ \\leftrightarrow\\ \\div⟩'], ['isolate', 'Get the variable alone on one side.', '⟨x = \\dots⟩'],
      ['like terms', 'Same variable, same exponent.', '⟨3x⟩ and ⟨-5x⟩'], ['identity', 'True for every value: infinitely many solutions.', '⟨2x = 2x⟩']] },
    { title: 'One- and Two-Step Equations', color: 'blue', kind: 'example', text: 'Undo addition or subtraction first, then multiplication or division. Do the same thing to <b>both sides</b>.',
      example: 'Solve ⟨3x - 5 = 16⟩.', steps: [['Add 5:', '⟨3x = 21⟩'], ['Divide by 3:', '⟨x = 7⟩']], answer: '⟨x = 7⟩', check: { num: '3*7-5', is: 16 } },
    { title: 'Multi-Step Equations', color: 'green', kind: 'example', text: 'Distribute, combine like terms on each side, then use inverse operations.',
      example: 'Solve ⟨3(x + 2) - 5 = 16⟩.', steps: [['Distribute:', '⟨3x + 6 - 5 = 16⟩'], ['Combine:', '⟨3x + 1 = 16⟩'], ['Solve:', '⟨3x = 15,\\ x = 5⟩']], answer: '⟨x = 5⟩', check: { num: '3*(5+2)-5', is: 16 } },
    { title: 'Variables on Both Sides', color: 'orange', kind: 'example', text: 'Collect the variable terms on one side and the constants on the other.',
      example: 'Solve ⟨4x - 3 = 2x + 9⟩.', steps: [['Subtract ⟨2x⟩:', '⟨2x - 3 = 9⟩'], ['Add 3:', '⟨2x = 12⟩'], ['Divide by 2:', '⟨x = 6⟩']], answer: '⟨x = 6⟩', check: { num: '(4*6-3)-(2*6+9)', is: 0 } },
    { title: 'Special Cases & Checking', color: 'pink', kind: 'words', rows: [
      ['Variables cancel and a <b>false</b> statement is left: ⟨3x + 6 = 3x + 9 \to 6 = 9⟩', 'no solution'],
      ['Variables cancel and a <b>true</b> statement is left: ⟨4x - 12 = 4x - 12 \to 0 = 0⟩', 'infinitely many'],
      ['A value is left: ⟨x = 2⟩', 'one solution'],
      ['Check ⟨x = 4⟩ in ⟨2x - 5 = 3⟩: ⟨2(4) - 5 = 3⟩', '✔ true']] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Keep the equation balanced: same step on both sides.', 'Distribute to <b>every</b> term inside the parentheses.', 'Check by substituting into the original equation.'],
      bad: [['⟨3(x + 4) \\ne 3x + 4⟩', 'it is ⟨3x + 12⟩'], ['⟨x - 5 = 9 \\to x = 4⟩', 'add 5: ⟨x = 14⟩'], ['⟨-x = 6⟩', 'is ⟨x = -6⟩, not ⟨6⟩']] }
  ],
  back: [
    { title: 'Words to Algebra', color: 'purple', kind: 'words', rows: [
      ['sum, more than, increased by', '⟨+⟩'], ['difference, less than, decreased by', '⟨-⟩'], ['product, times, twice', '⟨\\times⟩'], ['quotient, divided by, half of', '⟨\\div⟩'], ['is, equals, gives', '⟨=⟩'], ['“5 less than x”', '⟨x - 5⟩ (order matters!)']] },
    { title: 'Write and Solve', color: 'blue', kind: 'example', text: 'Define a variable, write the equation, solve, and answer in words.',
      example: 'A gym charges $25 to join plus $15 per month. Mia paid $115. How many months?', steps: [['Let ⟨m⟩ = months:', '⟨25 + 15m = 115⟩'], ['Subtract 25:', '⟨15m = 90⟩'], ['Divide by 15:', '⟨m = 6⟩']], answer: '6 months', check: { num: '25+15*6', is: 115 } },
    { title: 'Proportions', color: 'green', kind: 'example', text: 'Two equal ratios. Use cross products: if ⟨\\tfrac{a}{b} = \\tfrac{c}{d}⟩, then ⟨ad = bc⟩.',
      example: 'Solve ⟨\\dfrac{3}{4} = \\dfrac{x}{12}⟩.', steps: [['Cross multiply:', '⟨4x = 36⟩'], ['Divide by 4:', '⟨x = 9⟩']], answer: '⟨x = 9⟩', check: { num: '3/4 - 9/12', is: 0 } },
    { title: 'Percent Equations', color: 'orange', kind: 'example', text: '<b>part = percent × whole</b>. Change the percent to a decimal first.',
      example: '18 is what percent of 72?', steps: [['Equation:', '⟨18 = p \\cdot 72⟩'], ['Divide:', '⟨p = 0.25⟩']], answer: '25%', check: { num: '0.25*72', is: 18 } },
    { title: 'Literal Equations (Formulas)', color: 'pink', kind: 'example', text: 'Solve for one letter; treat the other letters like numbers.',
      example: 'Solve ⟨A = \\tfrac{1}{2}bh⟩ for ⟨h⟩.', steps: [['Multiply by 2:', '⟨2A = bh⟩'], ['Divide by ⟨b⟩:', '⟨h = \\dfrac{2A}{b}⟩']], answer: '⟨h = \\dfrac{2A}{b}⟩', check: { num: '2*(0.5*6*5)/6', is: 5 } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Did I distribute and combine like terms first?', 'Did I do the same step to both sides?', 'If the variables cancelled, is it no solution or infinitely many?', 'Does my answer work in the original equation, and make sense in the story?'] }
  ]
};
