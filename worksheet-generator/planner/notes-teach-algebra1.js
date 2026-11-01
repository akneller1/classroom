/* Teaching notes for the Algebra 1 lesson planner (see notes-teach.js for the format). */
(function (G) {
  'use strict';
  var T = (G.MKPLAN_TEACH = G.MKPLAN_TEACH || {}), N = T.algebra1 = T.algebra1 || {};
  /* ---------- Unit 1 · Foundations of Algebra ---------- */
  N['U1-L1'] = [{
    h: 'From words to an expression',
    big: 'A {{variable}} is a letter that stands for a number. An expression is built from {{terms}}: a term is a number times variables (its number is the {{coefficient}}) or a number alone (a {{constant}}).',
    steps: ['Find the operation words: sum/more than → +, difference/less than → −, product/times → ×, quotient → ÷.', '“{{less than}}” and “more than” reverse the order: 5 less than ⟨x⟩ is ⟨{{x - 5}}⟩.', 'Use parentheses when a whole quantity is operated on: “twice the sum of ⟨n⟩ and 3” is ⟨{{2(n+3)}}⟩.'],
    figs: [{ t: 'tbl', head: ['Words', 'Expression'], rows: [['7 more than ⟨x⟩', '{{⟨x+7⟩}}'], ['4 less than twice ⟨n⟩', '{{⟨2n-4⟩}}'], ['the quotient of ⟨y⟩ and 3', '{{⟨\\frac{y}{3}⟩}}'], ['3 times the difference of ⟨a⟩ and 1', '{{⟨3(a-1)⟩}}']] },
      { t: 'tbl', head: ['⟨4x^2⟩', '⟨-7y⟩', '⟨9⟩'], rows: [['coefficient {{4}}', 'coefficient {{−7}}', '{{constant}}']], cap: 'The three terms of ⟨4x^2-7y+9⟩' }]
  }];
  N['U1-L2'] = [{
    h: 'Order of operations',
    big: 'To {{evaluate}} an expression, {{substitute}} the value for the variable, then simplify in order: grouping symbols, {{exponents}}, multiply and divide from {{left to right}}, then add and subtract from left to right.',
    steps: ['Replace each variable with its value in parentheses: ⟨x=-3⟩ in ⟨x^2⟩ gives ⟨(-3)^2 = {{9}}⟩.', 'Work inside grouping symbols (parentheses, brackets, fraction bars) first.', 'Multiply and divide in the order they appear; then add and subtract in the order they appear.'],
    figs: [{ t: 'chain', nodes: ['2 + 3·4²', '2 + 3·16', '2 + 48', '{{50}}'], ops: ['exponent', 'multiply', 'add'], bw: 62, gap: 56, cap: 'Exponent first, then multiply, then add: the value is {{50}}' }]
  }];
  N['U1-L3'] = [{
    h: 'Sorting real numbers',
    big: 'A {{rational}} number can be written as a fraction of two integers; its decimal ends or repeats. An {{irrational}} number cannot; its decimal never ends and never repeats (⟨\\sqrt{2}⟩, ⟨\\pi⟩). Each set sits inside the next: natural ⊂ whole ⊂ integers ⊂ rational.',
    steps: ['Simplify first: ⟨\\sqrt{25} = 5⟩ is rational, but ⟨\\sqrt{7}⟩ is irrational.', 'A number belongs to {{every}} set that contains it: −4 is an integer and also rational and real.', 'A repeating decimal like ⟨0.\\overline{3}⟩ = ⟨\\frac{1}{3}⟩ is {{rational}}.'],
    figs: [{ t: 'geo', w: 270, dots: false, P: { _a: [0, 0], _b: [10, 0], _c: [10, 6.2], _d: [0, 6.2], _e: [0.3, 0.3], _f: [6.8, 0.3], _g: [6.8, 5.9], _h: [0.3, 5.9], _i: [0.6, 0.6], _j: [5.2, 0.6], _k: [5.2, 4.3], _l: [0.6, 4.3], _m: [0.9, 0.9], _n: [3.8, 0.9], _o: [3.8, 2.9], _p: [0.9, 2.9] },
      poly: [['_a', '_b', '_c', '_d'], ['_e', '_f', '_g', '_h', '#1f5fbf'], ['_i', '_j', '_k', '_l', '#1f5fbf'], ['_m', '_n', '_o', '_p', '#1f5fbf']],
      txt: [[5, 6.6, 'Real numbers'], [3.3, 5.35, '{{Rational}}'], [2.9, 3.75, 'Integers'], [2.35, 2.4, 'Whole'], [2.35, 1.5, '0, 1, 2, …'], [4.5, 1.4, '−3'], [6.0, 2.4, '⅔, 0.25'], [8.4, 4.0, '{{Irrational}}'], [8.4, 3.2, '√2, π']],
      cap: 'Every rational and every irrational number is real' }]
  }];
  N['U1-L4'] = [{
    h: 'Adding and subtracting signed numbers',
    big: 'Think of a number line. Adding a positive moves {{right}}; adding a negative moves {{left}}. Subtracting is adding the {{opposite}}: ⟨5-(-2) = 5+2⟩.',
    steps: ['Same signs: add the absolute values and keep the {{common}} sign: ⟨-3+(-5) = {{-8}}⟩.', 'Different signs: subtract the absolute values and take the sign of the number with the {{larger}} absolute value: ⟨-7+4 = {{-3}}⟩.', 'Rewrite subtraction as adding the opposite before you use the rules.'],
    figs: [{ t: 'nl', min: -8, max: 2, pts: [[-3, 'c', 'start −3'], [-8, 'c', '{{−8}}']], seg: [[-8, -3]], cap: '⟨-3+(-5)⟩: start at −3, move 5 to the {{left}}' }]
  }, {
    h: 'Multiplying and dividing signed numbers',
    big: 'The product or quotient of two numbers with the {{same}} sign is positive; with {{different}} signs it is negative. Dividing by a number is multiplying by its {{reciprocal}}.',
    steps: ['Find the answer’s size from the absolute values.', 'Count the negative factors: an even count gives {{positive}}, an odd count gives {{negative}}.'],
    figs: [{ t: 'tbl', head: ['×, ÷', '+', '−'], rowHead: true, rows: [['+', '{{+}}', '{{−}}'], ['−', '{{−}}', '{{+}}']], cap: 'Sign of the answer' }]
  }];
  N['U1-L5'] = [{
    h: 'Properties of real numbers',
    big: 'Properties let you rewrite an expression without changing its value. {{Commutative}} changes the order, {{associative}} changes the grouping, the {{identity}} (0 for adding, 1 for multiplying) keeps a number the same, and an {{inverse}} undoes it.',
    steps: ['Check what moved: the order of the numbers (commutative) or the parentheses (associative).', 'Subtraction and division are {{not}} commutative: ⟨8-3 \\ne 3-8⟩.', 'Use the properties to make mental math easy: ⟨25 \\cdot 7 \\cdot 4 = 25 \\cdot 4 \\cdot 7 = {{700}}⟩.'],
    figs: [{ t: 'tbl', head: ['Property', 'Example'], rows: [['{{Commutative}}', '⟨a+b=b+a⟩, ⟨ab=ba⟩'], ['{{Associative}}', '⟨(a+b)+c=a+(b+c)⟩'], ['Identity', '⟨a+{{0}}=a⟩, ⟨a\\cdot {{1}}=a⟩'], ['Inverse', '⟨a+({{-a}})=0⟩, ⟨a\\cdot\\frac{1}{a}=1⟩'], ['Distributive', '⟨a(b+c)={{ab+ac}}⟩']] }]
  }];
  N['U1-L6'] = [{
    h: 'The distributive property',
    big: 'To {{distribute}}, multiply the number outside the parentheses by {{every}} term inside, sign included. An area model shows why: ⟨3(x+4)⟩ is a rectangle 3 tall made of an ⟨x⟩ part and a 4 part.',
    steps: ['Multiply the outside factor by the first term, then by the second term.', 'Keep the signs: ⟨-2(x-5) = -2x {{+10}}⟩.'],
    figs: [{ t: 'area', top: ['x', '4'], side: ['3'], cells: [['{{3x}}', '{{12}}']], cap: '⟨3(x+4) = {{3x+12}}⟩' }]
  }, {
    h: 'Combining like terms',
    big: '{{Like terms}} have exactly the same variable part (⟨4x⟩ and ⟨-x⟩; ⟨3x^2⟩ and ⟨x^2⟩). Combine them by adding their {{coefficients}}; the variable part does not change.',
    steps: ['Distribute first if there are parentheses.', 'Group like terms, keeping the sign in front of each term.', 'Add the coefficients: ⟨5x+3-2x+7 = {{3x+10}}⟩.'],
    figs: []
  }];
  N['U1-L7'] = [{
    h: 'What each part of an expression means',
    big: 'In context, every part of an expression has a meaning. In ⟨15+8h⟩ for a rental, 15 is a {{fixed fee}} that is paid once (the constant), 8 is the {{cost per hour}} (the coefficient), and ⟨h⟩ is the {{number of hours}}.',
    steps: ['Name the variable and its units.', 'A coefficient multiplies the variable: it is a {{rate}} (“per”).', 'A constant does not change with the variable: it is a {{starting}} or fixed amount.', 'A factor like ⟨(1-0.2)⟩ in ⟨(1-0.2)p⟩ means “{{80%}} of the price”.'],
    figs: [{ t: 'tbl', head: ['Part of ⟨15+8h⟩', 'Meaning'], rows: [['⟨15⟩', '{{fixed fee, $15}}'], ['⟨8⟩', '{{$8 for each hour}}'], ['⟨8h⟩', '{{cost of the hours}}'], ['⟨15+8h⟩', '{{total cost}}']] }]
  }];
  /* ---------- Unit 2 · Solving Linear Equations ---------- */
  N['U2-L1'] = [{
    h: 'Inverse operations',
    big: 'An equation is a balance: both sides have the same value. To {{isolate}} the variable, undo its operation with the {{inverse}} operation, and do the same thing to {{both sides}}.',
    steps: ['Addition and subtraction undo each other; multiplication and division undo each other.', '⟨x+7=12⟩: subtract 7 from both sides, so ⟨x={{5}}⟩.', '⟨\\frac{x}{4}=3⟩: multiply both sides by 4, so ⟨x={{12}}⟩.', 'Check by substituting your answer into the original equation.'],
    figs: [{ t: 'chain', nodes: ['x', 'x + 7'], ops: ['+ 7'], back: ['{{− 7}}'], bw: 58, gap: 90, cap: 'Undo “+ 7” with “{{− 7}}”' }]
  }];
  N['U2-L2'] = [{
    h: 'Solving two-step equations',
    big: 'In ⟨3x+5=17⟩ the variable was multiplied by 3, then 5 was added. Undo them in {{reverse}} order: first undo the {{addition}}, then undo the {{multiplication}}.',
    steps: ['Subtract 5 from both sides: ⟨3x={{12}}⟩.', 'Divide both sides by 3: ⟨x={{4}}⟩.', 'Check: ⟨3(4)+5 = 17⟩ ✓'],
    figs: [{ t: 'chain', nodes: ['x', '3x', '3x + 5'], ops: ['× 3', '+ 5'], back: ['{{÷ 3}}', '{{− 5}}'], cap: 'Build the expression left to right; solve right to left' }]
  }];
  N['U2-L3'] = [{
    h: 'Solving multi-step equations',
    big: 'Simplify each side first: {{distribute}}, then {{combine like terms}}. Now the equation is a two-step equation.',
    steps: ['Distribute, including the sign: ⟨-2(x-3) = -2x {{+6}}⟩.', 'Combine like terms on each side.', 'Undo addition/subtraction, then multiplication/division.', 'Check in the {{original}} equation.'],
    figs: [{ t: 'tbl', head: ['Step', 'Equation'], rows: [['Original', '⟨4(x+2)-x=23⟩'], ['Distribute', '{{⟨4x+8-x=23⟩}}'], ['Combine', '{{⟨3x+8=23⟩}}'], ['Subtract 8', '{{⟨3x=15⟩}}'], ['Divide by 3', '{{⟨x=5⟩}}']] }]
  }];
  N['U2-L4'] = [{
    h: 'Variables on both sides',
    big: 'Collect the {{variable terms}} on one side and the {{constants}} on the other by adding or subtracting the same term on both sides. Moving the smaller variable term usually keeps the coefficient positive.',
    steps: ['Simplify each side.', 'Subtract the smaller variable term from both sides: ⟨5x+2=2x+14 \\Rightarrow 3x+2=14⟩.', 'Solve the two-step equation: ⟨3x={{12}}⟩, so ⟨x={{4}}⟩.'],
    figs: []
  }];
  N['U2-L5'] = [{
    h: 'One, none, or infinitely many solutions',
    big: 'Sometimes the variable terms {{cancel}}. If what is left is {{true}} (like ⟨5=5⟩) every number works: infinitely many solutions. If it is {{false}} (like ⟨5=2⟩) no number works: no solution.',
    steps: ['Solve as usual until the variables cancel.', 'Read the statement that is left: true → {{all real numbers}}; false → {{no solution}}.', 'Shortcut: same coefficient of ⟨x⟩ on both sides means one of these two cases.'],
    figs: [{ t: 'tbl', head: ['Equation', 'After simplifying', 'Solutions'], rows: [['⟨2x+3=x+5⟩', '⟨x=2⟩', '{{one}}'], ['⟨2(x+3)=2x+6⟩', '⟨6=6⟩', '{{infinitely many}}'], ['⟨2x+3=2x+5⟩', '⟨3=5⟩', '{{none}}']] }]
  }];
  N['U2-L6'] = [{
    h: 'Writing an equation from a story',
    big: 'First {{define a variable}} (what it is and its units). Translate the story into an equation, solve it, and answer in a {{sentence}} that makes sense in the context.',
    steps: ['Let ⟨x⟩ = the unknown quantity.', 'Find the fixed amount and the rate: “a $20 fee plus $6 per class” is ⟨{{20+6x}}⟩.', 'Set it equal to the total: ⟨20+6x=74⟩, so ⟨x={{9}}⟩.', 'Check: is the answer reasonable (whole number, positive)?'],
    figs: []
  }];
  N['U2-L7'] = [{
    h: 'Proportions',
    big: 'A {{proportion}} says two ratios are equal. Keep the units in the same places in both ratios, then use {{cross products}}: if ⟨\\frac{a}{b}=\\frac{c}{d}⟩ then ⟨ad=bc⟩.',
    steps: ['Write both ratios with matching units: ⟨\\frac{\\text{miles}}{\\text{hours}} = \\frac{\\text{miles}}{\\text{hours}}⟩.', 'Cross multiply: ⟨\\frac{x}{12}=\\frac{5}{4} \\Rightarrow 4x = {{60}}⟩.', 'Solve: ⟨x={{15}}⟩.'],
    figs: [{ t: 'tbl', head: ['', 'Trip 1', 'Trip 2'], rowHead: true, rows: [['miles', '150', '⟨x⟩'], ['hours', '3', '5']], cap: '⟨\\frac{150}{3}=\\frac{x}{5}⟩, so ⟨x={{250}}⟩ miles' }]
  }, {
    h: 'Percent equations',
    big: 'Percent means “per {{100}}”. Use ⟨\\text{part} = \\text{percent} \\times \\text{whole}⟩ with the percent as a {{decimal}}.',
    steps: ['What is 30% of 80? ⟨0.30 \\times 80 = {{24}}⟩.', '18 is what percent of 72? ⟨18 = p \\cdot 72⟩, ⟨p = {{0.25}} = 25\\%⟩.', '12 is 40% of what? ⟨12 = 0.40w⟩, ⟨w = {{30}}⟩.'],
    figs: []
  }];
  N['U2-L8'] = [{
    h: 'Solving a formula for a variable',
    big: 'A {{literal equation}} has several letters. To solve for one of them, treat every other letter like a {{number}} and use the same inverse operations as always.',
    steps: ['Circle the variable you are solving for.', 'Undo the operations around it in reverse order: ⟨P=2l+2w⟩ → subtract ⟨2w⟩ → ⟨P-2w={{2l}}⟩.', 'Divide by its coefficient: ⟨l={{\\frac{P-2w}{2}}}⟩.', 'Divide the {{whole}} side, not just one term.'],
    figs: [{ t: 'geo', w: 200, P: { A: [0, 0], B: [6, 0], C: [6, 3], D: [0, 3] }, poly: [['A', 'B', 'C', 'D']], hide: ['A', 'B', 'C', 'D'], slab: [['A', 'B', 'l', -1], ['B', 'C', 'w', -1]], cap: 'Perimeter of a rectangle: ⟨P=2l+2w⟩' }]
  }];
  N['U2-L9'] = [{
    h: 'Converting units',
    big: 'A {{conversion factor}} is a fraction equal to 1, like ⟨\\frac{12\\text{ in}}{1\\text{ ft}}⟩. Write it so the unit you want to remove is on the {{opposite}} side of the fraction, so it cancels.',
    steps: ['Write the starting quantity with its units.', 'Multiply by factors that cancel units one at a time.', '⟨60\\,\\frac{\\text{mi}}{\\text{h}}\\cdot\\frac{1\\text{ h}}{60\\text{ min}} = {{1}}\\,\\frac{\\text{mi}}{\\text{min}}⟩', 'Round to a sensible precision.'],
    figs: []
  }];
  /* ---------- Unit 3 · Linear Inequalities ---------- */
  N['U3-L1'] = [{
    h: 'Writing and graphing inequalities',
    big: 'An inequality compares two amounts. “At least” means {{≥}} and “at most” means {{≤}}. On a number line use an {{open}} circle for ⟨<⟩ or ⟨>⟩ (the endpoint is not included) and a {{closed}} circle for ⟨\\le⟩ or ⟨\\ge⟩.',
    steps: ['Put the endpoint on the number line.', 'Open or closed circle?', 'Shade toward the solutions: test a number like 0 to check the direction.'],
    figs: [{ t: 'nl', min: -2, max: 8, pts: [[3, 'o', '3']], ray: [[3, '>']], cap: '⟨x>3⟩: {{open}} circle, shade {{right}}' },
      { t: 'nl', min: -2, max: 8, pts: [[5, 'c', '5']], ray: [[5, '<']], cap: '⟨x \\le 5⟩ (“at most 5”): {{closed}} circle, shade {{left}}' }]
  }];
  N['U3-L2'] = [{
    h: 'Solving inequalities',
    big: 'Solve an inequality like an equation, with one new rule: when you multiply or divide both sides by a {{negative}} number, {{reverse}} the inequality sign.',
    steps: ['Undo addition/subtraction (the sign stays the same).', 'Divide by the coefficient. Negative? Flip the sign: ⟨-3x>12 \\Rightarrow x {{<}} -4⟩.', 'Graph the solution and check one point from the shaded part.'],
    figs: [{ t: 'nl', min: -8, max: 2, pts: [[-4, 'o', '−4']], ray: [[-4, '<']], cap: '⟨x<-4⟩. Check ⟨x=-5⟩: ⟨-3(-5)=15>12⟩ ✓' }]
  }];
  N['U3-L3'] = [{
    h: 'Multi-step inequalities',
    big: 'Simplify first: {{distribute}} and combine like terms, then collect the variable on one side. If the variable cancels, a {{true}} statement means all real numbers and a {{false}} one means no solution.',
    steps: ['⟨2(x-4) \\ge 5x+1⟩ → ⟨2x-8 \\ge 5x+1⟩.', 'Subtract ⟨5x⟩ and add 8: ⟨-3x \\ge {{9}}⟩.', 'Divide by −3 and flip: ⟨x {{\\le}} -3⟩.'],
    figs: [{ t: 'nl', min: -7, max: 3, pts: [[-3, 'c', '−3']], ray: [[-3, '<']], cap: '⟨x \\le -3⟩' }]
  }];
  N['U3-L5'] = [{
    h: 'Absolute value means distance',
    big: '⟨|x|⟩ is the {{distance}} from ⟨x⟩ to 0, so it is never negative. ⟨|x|=4⟩ has two solutions, ⟨x=4⟩ or ⟨x={{-4}}⟩. ⟨|x|<4⟩ means less than 4 units from 0: an {{AND}} inequality. ⟨|x|>4⟩ means more than 4 units away: an {{OR}} inequality.',
    steps: ['Isolate the absolute value first: ⟨2|x-1|+3=11 \\Rightarrow |x-1|={{4}}⟩.', 'Equation: inside = 4 or inside = −4, so ⟨x=5⟩ or ⟨x={{-3}}⟩.', '⟨|A|<b⟩ → ⟨-b<A<b⟩; ⟨|A|>b⟩ → ⟨A<-b⟩ or ⟨A>b⟩.', 'If the absolute value equals a negative number there is {{no solution}}.'],
    figs: [{ t: 'nl', min: -6, max: 6, pts: [[-4, 'o', '−4'], [4, 'o', '4']], seg: [[-4, 4]], cap: '⟨|x|<4⟩: ⟨-4<x<4⟩ (within 4 of 0)' },
      { t: 'nl', min: -6, max: 6, pts: [[-4, 'o', '−4'], [4, 'o', '4']], ray: [[-4, '<'], [4, '>']], cap: '⟨|x|>4⟩: ⟨x<-4⟩ or ⟨x>4⟩' }]
  }];
  N['U3-L6'] = [{
    h: 'Inequalities in context',
    big: 'Key phrases: “at least”, “minimum”, “no less than” → {{≥}}; “at most”, “maximum”, “no more than” → {{≤}}. After solving, keep only answers that are {{viable}} in the situation.',
    steps: ['Define the variable.', 'Write the inequality: “$12 per shirt plus $30, budget at most $150”: ⟨{{12x+30 \\le 150}}⟩.', 'Solve: ⟨x \\le {{10}}⟩.', 'Interpret: whole shirts only, so 0, 1, 2, …, 10 shirts.'],
    figs: [{ t: 'nl', min: 0, max: 12, pts: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(function (k) { return [k, 'c']; }), cap: 'Only whole numbers make sense: {{0 to 10}} shirts' }]
  }];
  /* ---------- Unit 4 · Relations and Functions ---------- */
  N['U4-L1'] = [{
    h: 'Four ways to show a relation',
    big: 'A {{relation}} pairs each {{input}} (⟨x⟩) with an {{output}} (⟨y⟩). The same relation can be a list of ordered pairs, a table, a mapping diagram, or a graph.',
    steps: ['In an ordered pair ⟨(x, y)⟩ the input comes {{first}}.', 'To plot ⟨(3, -2)⟩: move 3 {{right}}, then 2 {{down}}.'],
    figs: [{ t: 'tbl', head: ['⟨x⟩', '−1', '0', '2', '3'], rows: [['⟨y⟩', '4', '1', '1', '−2']], cap: '{(−1, 4), (0, 1), (2, 1), (3, −2)}' },
      { t: 'plane', x: [-3, 4], y: [-3, 5], pts: [[-1, 4, '(−1, 4)'], [0, 1], [2, 1], [3, -2, '{{(3, −2)}}']] }]
  }];
  N['U4-L2'] = [{
    h: 'Domain and range',
    big: 'The {{domain}} is the set of all inputs (⟨x⟩-values). The {{range}} is the set of all outputs (⟨y⟩-values). On a graph, read the domain {{left to right}} and the range {{bottom to top}}.',
    steps: ['List each value only once, in order.', 'For a graph, find the smallest and largest ⟨x⟩ the graph reaches; closed dot = included, open dot = not included.', 'Write with inequalities or intervals: domain ⟨-3 \\le x \\le 4⟩.'],
    figs: [{ t: 'plane', x: [-4, 5], y: [-3, 5], fns: [{ f: '0.5*x+1.5', dom: [-3, 4] }], pts: [[-3, 0, '(−3, 0)', null, null, 2, -9], [4, 3.5, '(4, 3.5)', null, null, -4, -9]], cap: 'Domain ⟨{{-3 \\le x \\le 4}}⟩; range ⟨{{0 \\le y \\le 3.5}}⟩' }]
  }];
  N['U4-L3'] = [{
    h: 'Is it a function?',
    big: 'A {{function}} gives each input exactly {{one}} output. Two different inputs may share an output, but one input may not have two outputs. On a graph, use the {{vertical line test}}: no vertical line may cross the graph twice.',
    steps: ['Table or ordered pairs: look for a repeated ⟨x⟩ with different ⟨y⟩-values → {{not}} a function.', 'Mapping diagram: an input with two arrows → not a function.', 'Graph: slide a vertical line across.'],
    figs: [{ t: 'plane', x: [-1, 7], y: [-4, 4], par: [{ p: '[t*t/2, t]', t: [-2.8, 2.8] }], vl: [[2, true, 'x = 2']], pts: [[2, 2], [2, -2]], cap: 'A vertical line hits twice: {{not a function}}' },
      { t: 'plane', x: [-4, 4], y: [-1, 7], fns: [{ f: 'x*x/2' }], vl: [[2, true, 'x = 2']], pts: [[2, 2]], cap: 'Each vertical line hits once: {{a function}}' }]
  }];
  N['U4-L4'] = [{
    h: 'Function notation',
    big: '⟨f(x)⟩ is read “f {{of}} x”; it is the {{output}} of ⟨f⟩ for the input ⟨x⟩ (not f times x). ⟨f(3)⟩ means substitute {{3}} for ⟨x⟩. On a graph, ⟨f(3)⟩ is the ⟨y⟩-value of the point where ⟨x=3⟩.',
    steps: ['Evaluate: ⟨f(x)=2x-1⟩, ⟨f(4) = 2(4)-1 = {{7}}⟩.', 'Solve ⟨f(x)=k⟩: set the rule equal to ⟨k⟩: ⟨2x-1=9⟩, ⟨x={{5}}⟩.', 'From a graph: go to the input on the ⟨x⟩-axis, up or down to the graph, read the ⟨y⟩-value.'],
    figs: [{ t: 'plane', x: [-2, 6], y: [-3, 8], fns: [{ f: '2*x-1', lab: 'f(x) = 2x − 1', at: [1.6, 6] }], segs: [[4, 0, 4, 7, true], [4, 7, 0, 7, true]], pts: [[4, 7, '{{(4, 7)}}']], cap: '⟨f(4) = {{7}}⟩' }]
  }];
  N['U4-L5'] = [{
    h: 'Key features of a graph',
    big: 'Describe a graph by its intercepts, where it is {{increasing}} (rising left to right) or {{decreasing}}, and its {{maximum}} or minimum. Intervals of increase and decrease are written with ⟨x⟩-values.',
    steps: ['⟨y⟩-intercept: where the graph crosses the ⟨y⟩-axis (⟨x=0⟩).', '⟨x⟩-intercepts (zeros): where it crosses the ⟨x⟩-axis (⟨y=0⟩).', 'Read left to right to find where it rises and falls.'],
    figs: [{ t: 'plane', x: [-2, 6], y: [-2, 6], fns: [{ f: '-(x-2)*(x-2)+4' }], pts: [[2, 4, '{{max (2, 4)}}'], [0, 0, '(0, 0)', null, null, -5, -7], [4, 0, '{{(4, 0)}}', null, null, 6, -7]], cap: 'Increasing for ⟨x<{{2}}⟩, decreasing for ⟨x>{{2}}⟩' }]
  }];
  N['U4-L6'] = [{
    h: 'Telling a story with a graph',
    big: 'A graph of a story shows how one quantity changes over time. Rising means {{increasing}}, falling means {{decreasing}}, flat means {{not changing}}. A {{steeper}} piece means a faster change. The graph is not a picture of the path.',
    steps: ['Split the story into time pieces.', 'For each piece decide: up, down or flat, and fast or slow.', 'Label the axes with the quantities and units.'],
    figs: [{ t: 'plane', x: [0, 10], y: [0, 6], nums: false, xl: 'time', yl: 'distance from home', fns: [{ f: 'x<=3? 1.5*x : x<=5 ? 4.5 : x<=8 ? 4.5-1.5*(x-5) : 0', dom: [0, 8] }], txt: [[1.3, 3.4, '{{walks away}}', 10], [4, 5.2, '{{stops}}', 10], [7.6, 3.2, '{{returns}}', 10]], cap: 'Walk away, stop, walk home' }]
  }];
  N['U4-L7'] = [{
    h: 'Discrete or continuous?',
    big: 'A {{discrete}} function has separate inputs you can count (tickets, people), so its graph is separate {{points}}. A {{continuous}} function has inputs that can be any value in an interval (time, distance), so its graph is a {{connected}} line or curve.',
    steps: ['Ask: can the input be a fraction like 2.5 in this situation?', 'Yes → continuous; no → discrete.', 'The reasonable domain is set by the context: ⟨0 \\le h \\le 8⟩ hours, or {0, 1, 2, …, 20} tickets.'],
    figs: [{ t: 'plane', x: [0, 6], y: [0, 12], ystep: 2, pts: [[0, 0], [1, 2], [2, 4], [3, 6], [4, 8], [5, 10]], cap: 'Cost of tickets: {{discrete}}' },
      { t: 'plane', x: [0, 6], y: [0, 12], ystep: 2, fns: [{ f: '2*x', dom: [0, 5] }], cap: 'Water in a tank over time: {{continuous}}' }]
  }];
  N['U4-L8'] = [{
    h: 'Arithmetic sequences',
    big: 'An {{arithmetic sequence}} adds the same number, the {{common difference}} ⟨d⟩, to get each next term. Its explicit formula is ⟨a_n = a_1 + (n-1)d⟩, a {{linear}} function of ⟨n⟩.',
    steps: ['Find ⟨d⟩ by subtracting consecutive terms: 5, 8, 11, 14 → ⟨d={{3}}⟩.', 'Explicit: ⟨a_n = 5 + (n-1)\\cdot 3⟩.', '20th term: ⟨a_{20} = 5 + 19\\cdot 3 = {{62}}⟩.', 'Recursive: ⟨a_1=5⟩, ⟨a_n = a_{n-1} + {{3}}⟩.'],
    figs: [{ t: 'plane', x: [0, 5], y: [0, 16], ystep: 2, numEveryY: 2, xl: 'n', yl: 'aₙ', pts: [[1, 5, '5'], [2, 8, '8'], [3, 11, '11'], [4, 14, '14']], cap: 'The points lie on a line with slope {{3}}' }]
  }];
  /* ---------- Unit 5 · Linear Equations and Slope ---------- */
  N['U5-L1'] = [{
    h: 'Rate of change',
    big: 'A {{rate of change}} compares how much the output changes for each 1-unit change in the input: ⟨\\frac{\\text{change in } y}{\\text{change in } x}⟩. A line has a {{constant}} rate of change, called its {{slope}}.',
    steps: ['Pick two rows of the table (or two points).', 'Subtract the ⟨y⟩-values and the ⟨x⟩-values in the {{same order}}.', 'Divide and include units: ⟨\\frac{\\$60-\\$20}{4\\text{ h}-0\\text{ h}} = {{\\$10}}⟩ per hour.'],
    figs: [{ t: 'tbl', head: ['hours ⟨x⟩', '0', '1', '2', '3', '4'], rows: [['cost ⟨y⟩ ($)', '20', '30', '40', '50', '60'], ['change', '', '{{+10}}', '{{+10}}', '{{+10}}', '{{+10}}']], cap: 'Constant change of {{$10 per hour}}' }]
  }];
  N['U5-L2'] = [{
    h: 'Finding slope',
    big: 'Slope ⟨m = \\frac{\\text{rise}}{\\text{run}} = \\frac{y_2-y_1}{x_2-x_1}⟩. A line that rises left to right has {{positive}} slope, a falling line has {{negative}} slope, a horizontal line has slope {{0}}, and a vertical line has {{undefined}} slope.',
    steps: ['Label the points ⟨(x_1, y_1)⟩ and ⟨(x_2, y_2)⟩.', 'Subtract in the same order on top and bottom.', '⟨(1, 2)⟩ and ⟨(4, 8)⟩: ⟨m = \\frac{8-2}{4-1} = \\frac{6}{3} = {{2}}⟩.'],
    figs: [{ t: 'plane', x: [-1, 6], y: [-1, 9], fns: [{ f: '2*x' }], segs: [[1, 2, 4, 2, true], [4, 2, 4, 8, true]], pts: [[1, 2, '(1, 2)', null, null, -5, -7], [4, 8, '(4, 8)', null, null, -5, -5]], txt: [[2.5, 1.2, 'run = {{3}}'.replace('{{3}}', '3')], [5.2, 5, '{{rise 6}}']], cap: '⟨m=\\frac{6}{3}={{2}}⟩' }]
  }];
  N['U5-L3'] = [{
    h: 'Slope-intercept form',
    big: 'In ⟨y = mx + b⟩, ⟨m⟩ is the {{slope}} and ⟨b⟩ is the {{y-intercept}}, the point ⟨(0, b)⟩ where the line crosses the ⟨y⟩-axis. In a story, ⟨b⟩ is the {{starting value}} and ⟨m⟩ is the rate.',
    steps: ['Solve for ⟨y⟩ first if needed: ⟨y = 3 - 2x⟩ is ⟨y = -2x + 3⟩, so ⟨m = {{-2}}⟩ and ⟨b = {{3}}⟩.', 'Write a line from ⟨m⟩ and ⟨b⟩: slope 4, ⟨y⟩-intercept −1 → ⟨y = {{4x - 1}}⟩.'],
    figs: [{ t: 'plane', x: [-3, 4], y: [-4, 6], fns: [{ f: '-2*x+3', lab: 'y = −2x + 3', at: [1.5, -1.6], anchor: 'start' }], pts: [[0, 3, '{{(0, 3)}}']], cap: '⟨y⟩-intercept {{3}}, slope {{−2}}' }]
  }];
  N['U5-L4'] = [{
    h: 'Graphing ⟨y = mx + b⟩',
    big: 'Start at the {{y-intercept}} ⟨(0, b)⟩. From there use the slope as {{rise over run}}: for ⟨m = \\frac{2}{3}⟩ go up 2 and right 3. Plot two or three points and draw the line through them.',
    steps: ['Plot ⟨(0, b)⟩.', 'Move by the slope: up for a positive rise, down for a negative rise, then right by the run.', 'Repeat, then draw the line with arrows.'],
    figs: [{ t: 'plane', x: [-4, 7], y: [-3, 6], fns: [{ f: '2/3*x-1' }], vec: [[0, -1, 0, 1], [0, 1, 3, 1], [3, 1, 3, 3], [3, 3, 6, 3]], pts: [[0, -1, '{{(0, −1)}}', null, null, -6, 4], [3, 1], [6, 3]], cap: '⟨y = \\frac{2}{3}x - 1⟩: up 2, right 3' }]
  }];
  N['U5-L5'] = [{
    h: 'Standard form and intercepts',
    big: 'Standard form is ⟨Ax + By = C⟩. To graph it quickly use the intercepts: the {{x-intercept}} is where ⟨y = 0⟩ and the {{y-intercept}} is where ⟨x = 0⟩.',
    steps: ['⟨2x + 3y = 12⟩. Let ⟨y=0⟩: ⟨2x = 12⟩, ⟨x = {{6}}⟩ → ⟨(6, 0)⟩.', 'Let ⟨x=0⟩: ⟨3y = 12⟩, ⟨y = {{4}}⟩ → ⟨(0, 4)⟩.', 'Draw the line through both intercepts. Its slope is ⟨-\\frac{A}{B} = {{-\\frac{2}{3}}}⟩.'],
    figs: [{ t: 'plane', x: [-2, 8], y: [-2, 6], fns: [{ f: '(12-2*x)/3' }], pts: [[6, 0, '{{(6, 0)}}', null, null, 2, -8], [0, 4, '{{(0, 4)}}', null, null, 5, -6]], cap: '⟨2x + 3y = 12⟩' }]
  }];
  N['U5-L6'] = [{
    h: 'Point-slope form',
    big: 'If you know the slope ⟨m⟩ and any point ⟨(x_1, y_1)⟩ on a line, write ⟨y - y_1 = m(x - x_1)⟩. The signs inside are {{subtraction}}, so a negative coordinate becomes a plus.',
    steps: ['Slope 3 through ⟨(2, -5)⟩: ⟨y - ({{-5}}) = 3(x - 2)⟩, which is ⟨y + 5 = 3(x - 2)⟩.', 'To change to slope-intercept form, distribute and solve for ⟨y⟩: ⟨y = {{3x - 11}}⟩.'],
    figs: [{ t: 'plane', x: [-1, 5], y: [-7, 3], fns: [{ f: '3*x-11' }], pts: [[2, -5, '{{(2, −5)}}', null, null, 6, 4]], cap: 'Slope 3 through ⟨(2, -5)⟩' }]
  }];
  N['U5-L7'] = [{
    h: 'Writing the equation of a line',
    big: 'To write a line you need a {{slope}} and a {{point}}. Get the slope from two points, a table or a graph. Then substitute a point to find ⟨b⟩, or use point-slope form.',
    steps: ['Through ⟨(1, 5)⟩ and ⟨(3, 9)⟩: ⟨m = \\frac{9-5}{3-1} = {{2}}⟩.', 'Substitute ⟨(1, 5)⟩ into ⟨y = 2x + b⟩: ⟨5 = 2 + b⟩, ⟨b = {{3}}⟩.', 'Equation: ⟨y = {{2x + 3}}⟩. Check with the other point: ⟨2(3) + 3 = 9⟩ ✓'],
    figs: [{ t: 'tbl', head: ['⟨x⟩', '1', '2', '3', '4'], rows: [['⟨y⟩', '5', '7', '9', '11']], cap: 'When ⟨x⟩ goes up 1, ⟨y⟩ goes up {{2}}; at ⟨x = 0⟩, ⟨y = {{3}}⟩' }]
  }];
  N['U5-L8'] = [{
    h: 'Parallel and perpendicular lines',
    big: '{{Parallel}} lines never meet and have {{equal}} slopes. {{Perpendicular}} lines meet at a right angle and have {{opposite reciprocal}} slopes: flip the fraction and change the sign, so the slopes multiply to −1.',
    steps: ['Find the slope of the given line (solve for ⟨y⟩ first).', 'Parallel: same slope. Perpendicular to slope ⟨\\frac{2}{3}⟩: slope ⟨{{-\\frac{3}{2}}}⟩.', 'Use the given point to write the new line.'],
    figs: [{ t: 'plane', x: [-4, 5], y: [-4, 5], fns: [{ f: '2/3*x+1', lab: 'm = 2/3', at: [3.4, 4.1] }, { f: '2/3*x-2', lab: '{{m = 2/3}}', at: [4.3, 1.2], color: '#2f7a50' }, { f: '-3/2*x+1', lab: '{{m = −3/2}}', at: [-2.3, 4.6], color: '#c0561b' }], cap: 'Green is parallel; orange is perpendicular' }]
  }];
  N['U5-L9'] = [{
    h: 'Transforming ⟨f(x) = x⟩',
    big: 'Starting from the parent line ⟨y = x⟩: changing ⟨b⟩ {{shifts}} the line up or down; making ⟨|m|⟩ bigger makes it {{steeper}}; ⟨|m|⟩ between 0 and 1 makes it {{less steep}}; a negative ⟨m⟩ {{reflects}} it so it falls.',
    steps: ['⟨y = x + 3⟩: up 3.', '⟨y = 3x⟩: steeper; ⟨y = \\frac{1}{3}x⟩: flatter.', '⟨y = -x⟩: reflected over the ⟨x⟩-axis.'],
    figs: [{ t: 'plane', x: [-4, 4], y: [-4, 5], fns: [{ f: 'x', lab: 'y = x', at: [3.2, 2.4] }, { f: 'x+3', lab: '{{up 3}}', at: [-2.3, 1.0], color: '#2f7a50', anchor: 'end' }, { f: '3*x', lab: '{{steeper}}', at: [1.25, 4.2], color: '#c0561b', anchor: 'start' }], cap: 'Shift and stretch of ⟨y = x⟩' }]
  }];
  N['U5-L10'] = [{
    h: 'Linear models',
    big: 'In a linear model ⟨y = mx + b⟩, the slope ⟨m⟩ is the {{rate}} (units of ⟨y⟩ per unit of ⟨x⟩) and ⟨b⟩ is the {{initial value}} (the value of ⟨y⟩ when ⟨x = 0⟩).',
    steps: ['A phone plan: ⟨C = 15m + 40⟩. The 15 means {{$15 per month}}; the 40 means {{a $40 starting fee}}.', 'Use the model to predict: ⟨m = 6⟩ gives ⟨C = {{130}}⟩.', 'Check the answer makes sense for the situation.'],
    figs: [{ t: 'plane', x: [0, 8], y: [0, 160], step: 1, ystep: 20, numEveryY: 2, maxH: 200, xl: 'months', yl: 'cost ($)', fns: [{ f: '15*x+40', dom: [0, 8] }], pts: [[0, 40, '{{start 40}}'], [6, 130, '(6, 130)', null, null, -6, -6]], cap: 'Slope {{15}} dollars per month' }]
  }];
  N['U5-L11'] = [{
    h: 'Comparing linear functions',
    big: 'Functions can be shown as an equation, a table, a graph or words. To compare them, find the same two features in each: the {{rate of change}} (slope) and the {{initial value}} (⟨y⟩-intercept).',
    steps: ['Equation: read ⟨m⟩ and ⟨b⟩ from ⟨y = mx + b⟩.', 'Table: slope = change in ⟨y⟩ ÷ change in ⟨x⟩; the ⟨y⟩ when ⟨x = 0⟩ is the start.', 'Graph: count rise over run; read where it crosses the ⟨y⟩-axis.', 'Compare: larger slope = {{faster}} change.'],
    figs: [{ t: 'tbl', head: ['', 'Plan A: ⟨y = 8x + 20⟩', 'Plan B (table)'], rowHead: true, rows: [['rate', '{{8}}', '{{10}}'], ['start', '{{20}}', '{{5}}']], cap: 'Plan B: (0, 5), (2, 25), (4, 45)' }]
  }];
  /* ---------- Unit 6 · Systems of Equations ---------- */
  N['U6-L1'] = [{
    h: 'Solving a system by graphing',
    big: 'A {{system}} is two equations at once. Its solution is the ordered pair that makes {{both}} equations true: the point where the lines {{intersect}}.',
    steps: ['Graph both lines carefully (slope-intercept form helps).', 'Read the intersection point.', 'Check it in {{both}} equations.'],
    figs: [{ t: 'plane', x: [-2, 6], y: [-2, 7], fns: [{ f: 'x+1', lab: 'y = x + 1', at: [4.9, 6.6] }, { f: '-2*x+7', lab: 'y = −2x + 7', at: [4.3, -1.0], color: '#c0561b', anchor: 'start' }], pts: [[2, 3, '{{(2, 3)}}', null, null, 7, 4]], cap: 'Check: ⟨3 = 2 + 1⟩ ✓ and ⟨3 = -4 + 7⟩ ✓' }]
  }];
  N['U6-L2'] = [{
    h: 'Substitution',
    big: 'Solve one equation for one variable, then {{substitute}} that expression into the {{other}} equation. Now there is one equation with one variable.',
    steps: ['⟨y = 2x - 1⟩ and ⟨3x + y = 14⟩.', 'Substitute: ⟨3x + (2x - 1) = 14⟩, so ⟨5x = 15⟩, ⟨x = {{3}}⟩.', 'Substitute back: ⟨y = 2(3) - 1 = {{5}}⟩.', 'Answer as a point: ⟨({{3, 5}})⟩. Check in both equations.'],
    figs: []
  }];
  N['U6-L3'] = [{
    h: 'Elimination by adding',
    big: 'If one variable has {{opposite}} coefficients in the two equations (like ⟨+2y⟩ and ⟨-2y⟩), add the equations: that variable is {{eliminated}}.',
    steps: ['Line up the like terms.', '⟨\\begin{aligned} 3x + 2y &= 16\\\\ x - 2y &= 0 \\end{aligned}⟩ add: ⟨4x = {{16}}⟩, ⟨x = {{4}}⟩.', 'Substitute ⟨x = 4⟩ into either equation: ⟨4 - 2y = 0⟩, ⟨y = {{2}}⟩.', 'If the coefficients are equal instead of opposite, {{subtract}} the equations.'],
    figs: []
  }];
  N['U6-L4'] = [{
    h: 'Elimination with multiplication',
    big: 'When no variable has opposite coefficients, multiply {{every term}} of one equation (or both) by a number so that one variable gets opposite coefficients. Then add.',
    steps: ['⟨2x + 3y = 13⟩ and ⟨x + y = 5⟩.', 'Multiply the second equation by −2: ⟨-2x - 2y = {{-10}}⟩.', 'Add: ⟨y = {{3}}⟩. Then ⟨x + 3 = 5⟩, ⟨x = {{2}}⟩.', 'Solution: ⟨(2, 3)⟩.'],
    figs: []
  }];
  N['U6-L5'] = [{
    h: 'How many solutions?',
    big: 'Two lines can cross {{once}} (one solution), be {{parallel}} (same slope, different intercepts: no solution), or be the {{same line}} (infinitely many solutions). Algebra shows the same thing: ⟨0 = 5⟩ means no solution; ⟨0 = 0⟩ means infinitely many.',
    steps: ['Write both equations in slope-intercept form.', 'Different slopes → one solution.', 'Same slope, different ⟨b⟩ → {{no solution}}; same slope and same ⟨b⟩ → {{infinitely many}}.'],
    figs: [{ t: 'plane', x: [-3, 4], y: [-3, 5], w: 150, nums: false, fns: [{ f: '2*x+2' }, { f: '2*x-1', color: '#c0561b' }], cap: 'Parallel: {{no solution}}' },
      { t: 'plane', x: [-3, 4], y: [-3, 5], w: 150, nums: false, fns: [{ f: '-0.5*x+1', dash: false }, { f: '-0.5*x+1', dash: true, color: '#c0561b' }], cap: 'Same line: {{infinitely many}}' }]
  }];
  N['U6-L6'] = [{
    h: 'Writing a system from a story',
    big: 'Define {{two variables}}. Each fact in the story becomes {{one equation}}. Then choose the quickest method: substitution if a variable is already alone, elimination if the equations are in standard form.',
    steps: ['Adult tickets cost $8 and student tickets $5. 120 tickets earned $780.', 'Let ⟨a⟩ = adult tickets and ⟨s⟩ = student tickets.', 'Count: ⟨a + s = {{120}}⟩. Money: ⟨8a + 5s = {{780}}⟩.', 'Solve: ⟨a = {{60}}⟩, ⟨s = {{60}}⟩.'],
    figs: []
  }];
  N['U6-L7'] = [{
    h: 'Systems applications',
    big: 'Many problems have a {{quantity}} equation (how many in total) and a {{value}} equation (quantity × price or rate). Solve, then answer in words for {{both}} variables with units.',
    steps: ['Make a table: rows for each item, columns for number, price, value.', 'Write the two equations from the totals.', 'Solve and interpret.'],
    figs: [{ t: 'tbl', head: ['', 'Number', 'Price', 'Value'], rowHead: true, rows: [['Adult', '⟨a⟩', '$8', '{{⟨8a⟩}}'], ['Student', '⟨s⟩', '$5', '{{⟨5s⟩}}'], ['Total', '120', '', '$780']] }]
  }];
  N['U6-L8'] = [{
    h: 'Graphing a linear inequality',
    big: 'Graph the boundary line ⟨y = mx + b⟩: {{dashed}} for ⟨<⟩ or ⟨>⟩ (points on it are not solutions), {{solid}} for ⟨\\le⟩ or ⟨\\ge⟩. Then shade the half-plane of solutions: test a point such as ⟨(0, 0)⟩.',
    steps: ['⟨y > 2x - 1⟩: dashed line through ⟨(0, -1)⟩ with slope 2.', 'Test ⟨(0, 0)⟩: ⟨0 > -1⟩ is {{true}}, so shade the side with ⟨(0, 0)⟩: {{above}} the line.', 'If you divide by a negative to solve for ⟨y⟩, flip the sign first.'],
    figs: [{ t: 'plane', x: [-4, 4], y: [-4, 5], shade: [{ f: '2*x-1', side: '>' }], fns: [{ f: '2*x-1', dash: true }], pts: [[0, 0, 'test (0, 0)', null, '#c0561b', -6, -7]], cap: '⟨y > 2x - 1⟩: {{dashed}} line, shade {{above}}' }]
  }];
  N['U6-L9'] = [{
    h: 'Systems of inequalities',
    big: 'Graph each inequality on the same plane. The solutions of the system are in the region where the shadings {{overlap}}. Points on a {{dashed}} boundary are not included.',
    steps: ['Graph and shade the first inequality.', 'Graph and shade the second.', 'Label the overlap; check one point from it in {{both}} inequalities.'],
    figs: [{ t: 'plane', x: [-4, 5], y: [-4, 5], region: [[[-4, 6], [1, 1], [5, 1], [5, 6]].map(function (p) { return p; })], shade: [], fns: [{ f: '-x+2', dash: false, lab: 'y ≥ −x + 2', at: [-3.4, 4.6], anchor: 'start' }, { f: '1', dash: true, lab: 'y > 1', at: [4.2, 1.5], color: '#c0561b' }], pts: [[3, 3, '{{(3, 3) works}}', null, null, -4, -7]], cap: 'Shaded: both are true' }]
  }];
  N['U6-L10'] = [{
    h: 'Modeling with constraints',
    big: 'Each limit in the story is a {{constraint}} and becomes an inequality. Counts and amounts usually also need ⟨x \\ge 0⟩ and ⟨y \\ge 0⟩. Points in the overlap are {{viable}}; points outside are not.',
    steps: ['Define the variables.', 'Write one inequality per constraint, including the hidden ones (no negatives).', 'Graph, find the feasible region, and choose points that make sense (often whole numbers).'],
    figs: [{ t: 'plane', x: [-1, 9], y: [-1, 7], region: [[[0, 0], [8, 0], [0, 6]]], fns: [{ f: '6-0.75*x', dom: [-1, 9] }], vl: [[0, false, '', '#111']], pts: [[2, 3, '{{viable}}', null, '#2f7a50'], [7, 4, '{{not viable}}', null, '#c0561b', -5, -7]], cap: '⟨3x + 4y \\le 24⟩, ⟨x \\ge 0⟩, ⟨y \\ge 0⟩' }]
  }];
  /* ---------- Unit 7 · Exponents ---------- */
  N['U7-L1'] = [{
    h: 'Product and power rules',
    big: 'An exponent counts repeated factors: ⟨x^3 = x \\cdot x \\cdot x⟩. When you multiply powers with the same base, {{add}} the exponents. For a power of a power, {{multiply}} the exponents. A power of a product applies to {{every factor}}.',
    steps: ['⟨x^2 \\cdot x^3 = (x \\cdot x)(x \\cdot x \\cdot x) = x^{{5}}⟩', '⟨(x^2)^3 = x^2 \\cdot x^2 \\cdot x^2 = x^{{6}}⟩', '⟨(2x)^3 = 2^3x^3 = {{8x^3}}⟩'],
    figs: [{ t: 'tbl', head: ['Rule', 'Example'], rows: [['⟨a^m \\cdot a^n = a^{m+n}⟩', '⟨3^2 \\cdot 3^4 = 3^{{6}}⟩'], ['⟨(a^m)^n = a^{mn}⟩', '⟨(5^2)^3 = 5^{{6}}⟩'], ['⟨(ab)^n = a^nb^n⟩', '⟨(4y)^2 = {{16y^2}}⟩']] }]
  }];
  N['U7-L2'] = [{
    h: 'Quotient, zero and negative exponents',
    big: 'When you divide powers with the same base, {{subtract}} the exponents. Any nonzero number to the zero power is {{1}}. A negative exponent means {{reciprocal}}: ⟨x^{-n} = \\frac{1}{x^n}⟩; it does not make the number negative.',
    steps: ['⟨\\frac{x^7}{x^3} = x^{{4}}⟩', '⟨5^0 = {{1}}⟩', '⟨2^{-3} = \\frac{1}{2^3} = {{\\frac{1}{8}}}⟩'],
    figs: [{ t: 'tbl', head: ['⟨2^3⟩', '⟨2^2⟩', '⟨2^1⟩', '⟨2^0⟩', '⟨2^{-1}⟩', '⟨2^{-2}⟩'], rows: [['8', '4', '2', '{{1}}', '{{⟨\\frac{1}{2}⟩}}', '{{⟨\\frac{1}{4}⟩}}']], cap: 'Each step left to right divides by 2' }]
  }];
  N['U7-L3'] = [{
    h: 'Using several exponent rules',
    big: 'Simplify one step at a time: handle {{coefficients}} as ordinary numbers, use the exponent rules on each variable, and finish with only {{positive}} exponents.',
    steps: ['⟨\\frac{(2x^3y)^2}{4x^2y^5}⟩: power first: ⟨\\frac{4x^6y^2}{4x^2y^5}⟩.', 'Divide: coefficients ⟨\\frac{4}{4} = 1⟩, ⟨x^{6-2} = x^{{4}}⟩, ⟨y^{2-5} = y^{{-3}}⟩.', 'Rewrite: ⟨{{\\frac{x^4}{y^3}}}⟩.'],
    figs: []
  }];
  N['U7-L4'] = [{
    h: 'Radicals and rational exponents',
    big: 'A fractional exponent is a root: ⟨x^{1/n} = \\sqrt[n]{x}⟩ and ⟨x^{m/n} = (\\sqrt[n]{x})^m⟩. The {{denominator}} is the index of the root and the {{numerator}} is the power. To simplify a radical, take out the largest {{perfect square}} factor.',
    steps: ['⟨8^{2/3} = (\\sqrt[3]{8})^2 = 2^2 = {{4}}⟩', '⟨\\sqrt{72} = \\sqrt{36 \\cdot 2} = {{6\\sqrt{2}}}⟩', '⟨x^{1/2}⟩ means ⟨\\sqrt{x}⟩, not ⟨\\frac{x}{2}⟩.'],
    figs: []
  }];
  N['U7-L5'] = [{
    h: 'Scientific notation',
    big: 'Scientific notation writes a number as ⟨a \\times 10^n⟩ with ⟨1 \\le a < 10⟩. The exponent ⟨n⟩ counts how many places the decimal point moves: {{positive}} for large numbers, {{negative}} for small numbers.',
    steps: ['⟨45{,}000 = 4.5 \\times 10^{{4}}⟩ (point moved 4 places left).', '⟨0.0062 = 6.2 \\times 10^{{-3}}⟩ (point moved 3 places right).', 'Back to standard form: ⟨3.1 \\times 10^5 = {{310{,}000}}⟩.'],
    figs: []
  }];
  N['U7-L6'] = [{
    h: 'Calculating with scientific notation',
    big: 'To multiply, multiply the {{coefficients}} and {{add}} the exponents. To divide, divide the coefficients and subtract the exponents. Then adjust so the coefficient is between 1 and 10.',
    steps: ['⟨(3 \\times 10^4)(5 \\times 10^6) = 15 \\times 10^{10}⟩.', 'Adjust: ⟨15 \\times 10^{10} = {{1.5 \\times 10^{11}}}⟩.', '⟨\\frac{8 \\times 10^9}{2 \\times 10^3} = {{4 \\times 10^6}}⟩.'],
    figs: []
  }];
  /* ---------- Unit 8 · Exponential Functions ---------- */
  N['U8-L1'] = [{
    h: 'Linear or exponential?',
    big: 'Look at equal steps in ⟨x⟩. A {{linear}} pattern adds the same amount each step (common {{difference}}). An {{exponential}} pattern multiplies by the same amount each step (common {{ratio}}).',
    steps: ['Find the differences between consecutive ⟨y⟩-values: all equal → linear.', 'If not, find the ratios (divide): all equal → exponential.'],
    figs: [{ t: 'tbl', head: ['⟨x⟩', '0', '1', '2', '3', 'pattern'], rows: [['linear', '3', '5', '7', '9', '{{+2}} each time'], ['exponential', '3', '6', '12', '24', '{{×2}} each time']] },
      { t: 'plane', x: [0, 4], y: [0, 26], ystep: 2, numEveryY: 4, maxH: 190, pts: [[0, 3], [1, 5], [2, 7], [3, 9], [0, 3, '', null, '#c0561b'], [1, 6, '', null, '#c0561b'], [2, 12, '', null, '#c0561b'], [3, 24, '', null, '#c0561b']], fns: [{ f: '2*x+3', dom: [0, 3.6], lab: 'linear', at: [3.5, 12] }, { f: '3*pow(2,x)', dom: [0, 3.1], color: '#c0561b', lab: 'exponential', at: [2.2, 22] }] }]
  }];
  N['U8-L2'] = [{
    h: 'Graphs of ⟨y = a \\cdot b^x⟩',
    big: 'The graph of ⟨y = a \\cdot b^x⟩ (with ⟨a > 0⟩) crosses the ⟨y⟩-axis at ⟨(0, {{a}})⟩. If ⟨b > 1⟩ it shows {{growth}}; if ⟨0 < b < 1⟩ it shows {{decay}}. It gets closer and closer to the {{asymptote}} ⟨y = 0⟩ but never touches it.',
    steps: ['Domain: all real numbers. Range: ⟨y > 0⟩.', 'Make a table with ⟨x = -1, 0, 1, 2⟩ and plot.'],
    figs: [{ t: 'plane', x: [-3, 3], y: [-1, 9], fns: [{ f: '2*pow(2,x)', lab: '{{y = 2·2ˣ growth}}', at: [1.5, 6.4], anchor: 'end' }, { f: '2*pow(0.5,x)', color: '#c0561b', lab: 'y = 2·(½)ˣ', at: [-1.4, 7.6], anchor: 'start' }], hl: [[0, true, '{{asymptote y = 0}}']], pts: [[0, 2, '(0, 2)']], cap: 'Same start ⟨(0, 2)⟩; growth vs decay' }]
  }];
  N['U8-L3'] = [{
    h: 'Exponential growth',
    big: 'When an amount grows by the same {{percent}} each period, ⟨y = a(1 + r)^t⟩, where ⟨a⟩ is the {{initial amount}}, ⟨r⟩ is the rate as a decimal, and ⟨1 + r⟩ is the {{growth factor}}.',
    steps: ['5% growth → factor ⟨1 + 0.05 = {{1.05}}⟩ (not 0.05).', '$800 growing 5% per year: ⟨y = 800(1.05)^t⟩.', 'After 3 years: ⟨800(1.05)^3 \\approx {{\\$926.10}}⟩.'],
    figs: [{ t: 'plane', x: [0, 10], y: [0, 1400], step: 1, ystep: 200, numEveryY: 2, maxH: 190, xl: 't (years)', fns: [{ f: '800*pow(1.05,x)' }], pts: [[0, 800, '800'], [3, 926.1, '{{926.10}}', null, null, -5, -7]] }]
  }];
  N['U8-L4'] = [{
    h: 'Exponential decay',
    big: 'When an amount decreases by the same percent each period, ⟨y = a(1 - r)^t⟩. The {{decay factor}} ⟨1 - r⟩ is between 0 and 1. A {{half-life}} means the factor is ⟨\\frac{1}{2}⟩ per half-life.',
    steps: ['20% decrease → factor ⟨1 - 0.20 = {{0.80}}⟩.', 'A $20,000 car loses 20% per year: ⟨y = 20000(0.8)^t⟩.', 'After 2 years: ⟨20000(0.8)^2 = {{\\$12{,}800}}⟩.'],
    figs: [{ t: 'plane', x: [0, 6], y: [0, 22], ystep: 2, numEveryY: 2, maxH: 170, xl: 't', yl: 'value ($1000s)', fns: [{ f: '20*pow(0.8,x)' }], pts: [[0, 20, '20'], [2, 12.8, '{{12.8}}']] }]
  }];
  N['U8-L5'] = [{
    h: 'Writing ⟨y = a \\cdot b^x⟩',
    big: 'Find ⟨a⟩, the value when ⟨x = 0⟩. Find ⟨b⟩, the common {{ratio}}, by {{dividing}} a ⟨y⟩-value by the one before it (for steps of 1 in ⟨x⟩).',
    steps: ['Table: (0, 5), (1, 15), (2, 45). ⟨a = {{5}}⟩.', '⟨b = \\frac{15}{5} = {{3}}⟩ (check: ⟨\\frac{45}{15} = 3⟩).', 'Equation: ⟨y = {{5 \\cdot 3^x}}⟩.'],
    figs: [{ t: 'tbl', head: ['⟨x⟩', '0', '1', '2', '3'], rows: [['⟨y⟩', '5', '15', '45', '{{135}}']], cap: 'Multiply by {{3}} each step' }]
  }];
  N['U8-L6'] = [{
    h: 'Compound interest',
    big: 'Interest compounded ⟨n⟩ times a year: ⟨A = P\\left(1 + \\frac{r}{n}\\right)^{nt}⟩. ⟨P⟩ is the {{principal}}, ⟨r⟩ the yearly rate as a decimal, ⟨t⟩ the years. Divide the {{rate}} by ⟨n⟩ and multiply the {{time}} by ⟨n⟩.',
    steps: ['$1000 at 6% compounded monthly for 2 years: ⟨n = {{12}}⟩.', '⟨A = 1000\\left(1 + \\frac{0.06}{12}\\right)^{24} = 1000(1.005)^{24}⟩.', '⟨A \\approx {{\\$1127.16}}⟩.'],
    figs: [{ t: 'tbl', head: ['Compounded', '⟨n⟩'], rows: [['yearly', '1'], ['quarterly', '{{4}}'], ['monthly', '{{12}}'], ['daily', '365']] }]
  }];
  N['U8-L7'] = [{
    h: 'Geometric sequences',
    big: 'A {{geometric sequence}} multiplies by the same number, the common {{ratio}} ⟨r⟩, to get each next term. Explicit formula: ⟨a_n = a_1 \\cdot r^{n-1}⟩.',
    steps: ['3, 6, 12, 24, … ⟨r = \\frac{6}{3} = {{2}}⟩.', '⟨a_n = 3 \\cdot 2^{n-1}⟩.', '8th term: ⟨3 \\cdot 2^{7} = {{384}}⟩.', 'Recursive: ⟨a_1 = 3⟩, ⟨a_n = {{2}} \\cdot a_{n-1}⟩.'],
    figs: []
  }];
  N['U8-L8'] = [{
    h: 'Linear versus exponential models',
    big: 'An increasing exponential model {{eventually}} passes any increasing linear model, even one that starts higher, because it multiplies instead of adding.',
    steps: ['Compare ⟨y = 50x + 100⟩ and ⟨y = 2^x⟩ with a table or graph.', 'At ⟨x = 10⟩: linear 600, exponential 1024 → exponential is {{greater}}.', 'Find about where they cross (between ⟨x = 9⟩ and ⟨x = 10⟩).'],
    figs: [{ t: 'plane', x: [0, 11], y: [0, 1200], step: 1, ystep: 200, numEveryY: 2, maxH: 190, fns: [{ f: '50*x+100', lab: 'y = 50x + 100', at: [3.2, 520] }, { f: 'pow(2,x)', color: '#c0561b', lab: 'y = 2ˣ', at: [9.3, 1130] }], cap: 'The exponential passes the line near ⟨x \\approx {{9.2}}⟩' }]
  }];
  N['U8-L9'] = [{
    h: 'Solving exponential equations',
    big: 'If both sides can be written with the {{same base}}, set the {{exponents}} equal. Otherwise estimate the solution from a table or the intersection of two graphs.',
    steps: ['⟨2^{x+1} = 32⟩: ⟨32 = 2^{{5}}⟩.', 'Set exponents equal: ⟨x + 1 = 5⟩, ⟨x = {{4}}⟩.', '⟨9^x = 27⟩: ⟨3^{2x} = 3^3⟩, ⟨x = {{\\frac{3}{2}}}⟩.'],
    figs: []
  }];
  /* ---------- Unit 9 · Polynomials ---------- */
  N['U9-L1'] = [{
    h: 'Naming polynomials',
    big: 'A {{polynomial}} is a sum of monomials (number × variables with whole-number exponents). Write it in {{standard form}}: highest degree first. The {{degree}} is the highest exponent, and the {{leading coefficient}} is the number in front of that term.',
    steps: ['Put the terms in order: ⟨4x - 3x^3 + 7 = -3x^3 + 4x + 7⟩.', 'Degree {{3}} (cubic); leading coefficient {{−3}}.', 'Number of terms: 1 monomial, 2 binomial, 3 {{trinomial}}.'],
    figs: [{ t: 'tbl', head: ['Degree', 'Name', 'Example'], rows: [['0', 'constant', '⟨7⟩'], ['1', '{{linear}}', '⟨2x - 5⟩'], ['2', '{{quadratic}}', '⟨x^2 + 3x⟩'], ['3', '{{cubic}}', '⟨-3x^3 + 4x + 7⟩']] }]
  }];
  N['U9-L2'] = [{
    h: 'Adding and subtracting polynomials',
    big: 'To add polynomials, combine {{like terms}}. To subtract, first {{distribute the negative}} to every term of the second polynomial, then combine like terms.',
    steps: ['⟨(3x^2 + 2x - 5) - (x^2 - 4x + 1)⟩', 'Distribute −1: ⟨3x^2 + 2x - 5 - x^2 {{+ 4x - 1}}⟩.', 'Combine: ⟨{{2x^2 + 6x - 6}}⟩.'],
    figs: [{ t: 'tbl', head: ['', '⟨x^2⟩', '⟨x⟩', 'const'], rowHead: true, rows: [['first', '3', '2', '−5'], ['minus second', '{{−1}}', '{{+4}}', '{{−1}}'], ['result', '{{2}}', '{{6}}', '{{−6}}']], cap: 'Line up like terms in columns' }]
  }];
  N['U9-L3'] = [{
    h: 'Monomial × polynomial',
    big: 'Distribute the monomial to {{every}} term. For each product, {{multiply}} the coefficients and {{add}} the exponents of the same variable.',
    steps: ['⟨2x(3x^2 - 5x + 4)⟩', '⟨2x \\cdot 3x^2 = {{6x^3}}⟩, ⟨2x \\cdot (-5x) = {{-10x^2}}⟩, ⟨2x \\cdot 4 = {{8x}}⟩.', 'Answer: ⟨6x^3 - 10x^2 + 8x⟩.'],
    figs: [{ t: 'area', top: ['3x²', '−5x', '4'], side: ['2x'], cells: [['{{6x³}}', '{{−10x²}}', '{{8x}}']] }]
  }];
  N['U9-L4'] = [{
    h: 'Multiplying binomials',
    big: 'Each term of the first binomial multiplies {{each}} term of the second: four products in all (an area model or FOIL keeps track). Then combine the {{like terms}}, usually the two middle products.',
    steps: ['⟨(x + 3)(x + 5)⟩: products ⟨x^2⟩, ⟨5x⟩, ⟨3x⟩, ⟨15⟩.', 'Combine: ⟨x^2 + {{8x}} + 15⟩.', '⟨(x + 3)^2 = (x + 3)(x + 3) = x^2 + {{6x}} + 9⟩, not ⟨x^2 + 9⟩.'],
    figs: [{ t: 'area', top: ['x', '5'], side: ['x', '3'], cells: [['{{x²}}', '{{5x}}'], ['{{3x}}', '{{15}}']], cap: '⟨(x + 3)(x + 5) = {{x^2 + 8x + 15}}⟩' }]
  }];
  N['U9-L5'] = [{
    h: 'Special products',
    big: 'Some products follow patterns. Square of a sum: ⟨(a + b)^2 = a^2 + {{2ab}} + b^2⟩. Square of a difference: ⟨(a - b)^2 = a^2 - 2ab + b^2⟩. Sum times difference: ⟨(a + b)(a - b) = {{a^2 - b^2}}⟩ (the middle terms cancel).',
    steps: ['⟨(2x - 3)^2 = 4x^2 - {{12x}} + 9⟩.', '⟨(x + 7)(x - 7) = {{x^2 - 49}}⟩.', 'Binomial × trinomial: multiply each of the 2 terms by each of the 3 terms (6 products), then combine.'],
    figs: [{ t: 'area', top: ['a', 'b'], side: ['a', 'b'], cells: [['{{a²}}', '{{ab}}'], ['{{ab}}', '{{b²}}']], cap: '⟨(a + b)^2⟩: the two ⟨ab⟩ pieces give ⟨2ab⟩' }]
  }];
  N['U9-L6'] = [{
    h: 'Polynomials in context; closure',
    big: 'Adding, subtracting or multiplying two polynomials always gives another polynomial: polynomials are {{closed}} under these operations. Dividing is {{not}} always closed (⟨\\frac{1}{x}⟩ is not a polynomial). Polynomials describe areas and volumes.',
    steps: ['A rectangle is ⟨(2x + 1)⟩ by ⟨(x + 4)⟩: area ⟨= {{2x^2 + 9x + 4}}⟩.', 'Perimeter ⟨= 2(2x + 1) + 2(x + 4) = {{6x + 10}}⟩.'],
    figs: [{ t: 'geo', w: 230, pad: 40, P: { A: [0, 0], B: [7, 0], C: [7, 3.2], D: [0, 3.2] }, poly: [['A', 'B', 'C', 'D']], hide: ['A', 'B', 'C', 'D'], slab: [['A', 'B', '2x + 1', -1], ['B', 'C', 'x + 4', -1, 24]], cap: 'Area ⟨(2x + 1)(x + 4)⟩' }]
  }];
  /* ---------- Unit 10 · Factoring ---------- */
  N['U10-L1'] = [{
    h: 'Factoring out the GCF',
    big: '{{Factoring}} undoes distributing. Find the {{greatest common factor}} of all the terms (the biggest number and the lowest power of each shared variable), write it outside, and write what is left inside the parentheses.',
    steps: ['⟨12x^3 + 18x^2⟩: GCF of 12 and 18 is 6; of ⟨x^3⟩ and ⟨x^2⟩ is ⟨x^2⟩ → ⟨{{6x^2}}⟩.', 'Divide each term: ⟨6x^2(\\,{{2x + 3}}\\,)⟩.', 'Check by distributing. If a term equals the GCF, a {{1}} stays: ⟨3x + 3 = 3(x + 1)⟩.'],
    figs: [{ t: 'area', top: ['{{2x}}', '{{3}}'], side: ['6x²'], cells: [['12x³', '18x²']], cap: 'Work backward from the area to the sides' }]
  }];
  N['U10-L2'] = [{
    h: 'Factoring by grouping',
    big: 'With four terms, group them in {{pairs}}, factor the GCF out of each pair, then factor out the {{common binomial}}.',
    steps: ['⟨x^3 + 3x^2 + 2x + 6 = x^2(x + 3) + 2(x + 3)⟩', 'Common binomial ⟨(x + 3)⟩: ⟨= ({{x + 3}})({{x^2 + 2}})⟩.', 'If the second pair starts with a minus, factor out a {{negative}}: ⟨-4x - 8 = -4(x + 2)⟩.'],
    figs: []
  }];
  N['U10-L3'] = [{
    h: 'Factoring ⟨x^2 + bx + c⟩',
    big: 'Find two numbers that {{multiply}} to ⟨c⟩ and {{add}} to ⟨b⟩. Then ⟨x^2 + bx + c = (x + p)(x + q)⟩.',
    steps: ['⟨x^2 + 7x + 12⟩: factor pairs of 12: 1·12, 2·6, {{3·4}}.', '⟨3 + 4 = 7⟩ ✓ so ⟨(x + 3)(x + 4)⟩.', '⟨x^2 - 2x - 15⟩: product −15, sum −2: ⟨{{-5}}⟩ and ⟨{{3}}⟩ → ⟨(x - 5)(x + 3)⟩.'],
    figs: [{ t: 'tbl', head: ['Factors of 12', 'Sum'], rows: [['1 · 12', '13'], ['2 · 6', '8'], ['3 · 4', '{{7}} ✓']] },
      { t: 'area', top: ['x', '4'], side: ['x', '3'], cells: [['x²', '{{4x}}'], ['{{3x}}', '12']] }]
  }];
  N['U10-L4'] = [{
    h: 'Factoring ⟨ax^2 + bx + c⟩',
    big: 'Take out any GCF first. Then find two numbers that multiply to ⟨a \\cdot c⟩ and add to ⟨b⟩, {{split}} the middle term with them, and factor by {{grouping}}.',
    steps: ['⟨2x^2 + 7x + 3⟩: ⟨ac = 6⟩; ⟨1 \\cdot 6 = 6⟩ and ⟨1 + 6 = 7⟩.', 'Split: ⟨2x^2 + x + 6x + 3⟩.', 'Group: ⟨x(2x + 1) + 3(2x + 1) = ({{2x + 1}})({{x + 3}})⟩.'],
    figs: [{ t: 'area', top: ['2x', '1'], side: ['x', '3'], cells: [['2x²', '{{x}}'], ['{{6x}}', '3']], cap: 'The middle term ⟨7x⟩ splits into ⟨x + 6x⟩' }]
  }];
  N['U10-L5'] = [{
    h: 'Special factoring patterns',
    big: 'A {{difference of squares}} ⟨a^2 - b^2 = (a + b)(a - b)⟩. A {{perfect square trinomial}} ⟨a^2 + 2ab + b^2 = (a + b)^2⟩. A sum of squares like ⟨x^2 + 9⟩ does {{not}} factor over the integers.',
    steps: ['⟨9x^2 - 25 = (3x)^2 - 5^2 = ({{3x + 5}})({{3x - 5}})⟩.', '⟨x^2 - 10x + 25⟩: first and last are squares and ⟨10x = 2 \\cdot x \\cdot 5⟩, so ⟨= {{(x - 5)^2}}⟩.'],
    figs: [{ t: 'geo', w: 200, dots: false, P: { A: [0, 0], B: [5, 0], C: [5, 5], D: [0, 5], E: [2, 5], F: [2, 2], G: [5, 2] }, fill: [['A', 'B', 'G', 'F', 'E', 'D', '#dce8fb']], poly: [['A', 'B', 'C', 'D']], seg: ['EF:dash', 'FG:dash'], hide: ['A', 'B', 'C', 'D', 'E', 'F', 'G'], slab: [['A', 'B', 'a', -1], ['G', 'C', 'b', -1], ['E', 'C', 'b', 1, 10]], txt: [[1.2, 1.2, '{{a² − b²}}']], cap: 'Big square ⟨a^2⟩ minus the corner ⟨b^2⟩' }]
  }];
  N['U10-L6'] = [{
    h: 'Factoring completely',
    big: 'Factor {{completely}}: keep going until no factor can be factored again. A checklist: (1) {{GCF}}, (2) two terms → difference of squares, (3) three terms → trinomial or perfect square, (4) four terms → {{grouping}}.',
    steps: ['⟨2x^3 - 18x = 2x(x^2 - 9)⟩ — not done yet!', '⟨x^2 - 9⟩ is a difference of squares: ⟨= 2x({{x + 3}})({{x - 3}})⟩.', 'Check each factor; a factor that cannot be factored is {{prime}}.'],
    figs: [{ t: 'chain', nodes: ['GCF?', '2 terms?', '3 terms?', '4 terms?'], ops: ['then', 'then', 'then'], bw: 58, gap: 34, cap: 'Use the checklist on every factor' }]
  }];
  N['U10-L7'] = [{
    h: 'The Zero Product Property',
    big: 'If a product equals {{zero}}, then at least one factor equals {{zero}}. So set {{each factor}} equal to 0 and solve. This only works when the other side is 0.',
    steps: ['⟨(x - 4)(x + 7) = 0⟩', '⟨x - 4 = 0⟩ or ⟨x + 7 = 0⟩', '⟨x = {{4}}⟩ or ⟨x = {{-7}}⟩.', '⟨3x(x - 2) = 0⟩ gives ⟨x = {{0}}⟩ or ⟨x = 2⟩ — do not divide away the ⟨x⟩.'],
    figs: [{ t: 'plane', x: [-9, 6], y: [-32, 8], step: 1, ystep: 4, numEvery: 3, numEveryY: 2, maxH: 170, fns: [{ f: '(x-4)*(x+7)' }], pts: [[-7, 0, '{{−7}}', null, null, 0, -8], [4, 0, '{{4}}', null, null, 0, -8]], cap: 'The solutions are the ⟨x⟩-intercepts of ⟨y = (x - 4)(x + 7)⟩' }]
  }];
  N['U10-L8'] = [{
    h: 'Solving quadratics by factoring',
    big: 'First write the equation in {{standard form}} with 0 on one side. Then {{factor}} and use the Zero Product Property.',
    steps: ['⟨x^2 + 3x = 10⟩ → ⟨x^2 + 3x - 10 = 0⟩.', 'Factor: ⟨(x + 5)(x - 2) = 0⟩.', 'Solve: ⟨x = {{-5}}⟩ or ⟨x = {{2}}⟩. Check both.'],
    figs: []
  }];
  N['U10-L9'] = [{
    h: 'Factoring in applications',
    big: 'Write the equation from the situation, solve by factoring, then {{reject}} solutions that do not make sense, such as a {{negative}} length or time.',
    steps: ['A rectangle has length 3 more than its width and area 40: ⟨w(w + 3) = 40⟩.', '⟨w^2 + 3w - 40 = 0⟩, ⟨(w + 8)(w - 5) = 0⟩.', '⟨w = -8⟩ (reject) or ⟨w = {{5}}⟩, so the rectangle is 5 by {{8}}.'],
    figs: [{ t: 'geo', w: 200, P: { A: [0, 0], B: [8, 0], C: [8, 5], D: [0, 5] }, poly: [['A', 'B', 'C', 'D']], hide: ['A', 'B', 'C', 'D'], slab: [['A', 'B', 'w + 3', -1], ['B', 'C', 'w', -1]], txt: [[4, 2.5, 'Area = 40']] }]
  }];
  /* ---------- Unit 11 · Quadratic Functions ---------- */
  N['U11-L1'] = [{
    h: 'Parts of a parabola',
    big: 'The graph of a quadratic function is a {{parabola}}. Its turning point is the {{vertex}} (a minimum if it opens up, a maximum if it opens down). The {{axis of symmetry}} is the vertical line ⟨x = h⟩ through the vertex. The {{zeros}} are the ⟨x⟩-intercepts.',
    steps: ['Read the vertex ⟨(h, k)⟩ from the graph.', 'Write the axis as an equation: ⟨x = h⟩.', 'Points on the parabola come in mirror pairs around the axis.'],
    figs: [{ t: 'plane', x: [-2, 6], y: [-5, 6], fns: [{ f: '(x-2)*(x-2)-4' }], vl: [[2, true, '{{x = 2}}']], pts: [[2, -4, '{{vertex (2, −4)}}', null, null, 6, 4], [0, 0, '', null], [4, 0, '', null]], txt: [[-0.6, 0.8, 'zero 0', 9], [4.9, 0.8, '{{zero 4}}', 9]], cap: 'Minimum value {{−4}}' }]
  }];
  N['U11-L2'] = [{
    h: 'Graphing ⟨y = ax^2 + bx + c⟩',
    big: 'If ⟨a > 0⟩ the parabola opens {{up}}; if ⟨a < 0⟩ it opens {{down}}. The axis of symmetry is ⟨x = -\\frac{b}{2a}⟩. Substitute that ⟨x⟩ to find the vertex. ⟨c⟩ is the {{y-intercept}}.',
    steps: ['⟨y = x^2 - 4x + 1⟩: ⟨x = -\\frac{-4}{2(1)} = {{2}}⟩.', '⟨y = 4 - 8 + 1 = {{-3}}⟩, so the vertex is ⟨(2, -3)⟩.', 'Plot ⟨(0, 1)⟩ and its mirror point ⟨({{4}}, 1)⟩, then sketch.'],
    figs: [{ t: 'plane', x: [-2, 6], y: [-4, 6], fns: [{ f: 'x*x-4*x+1' }], vl: [[2, true, 'x = 2']], pts: [[2, -3, '{{(2, −3)}}', null, null, 6, 4], [0, 1, '(0, 1)', null, null, -5, -6], [4, 1, '{{(4, 1)}}']] }]
  }];
  N['U11-L3'] = [{
    h: 'Vertex form',
    big: 'In ⟨y = a(x - h)^2 + k⟩ the vertex is ⟨({{h}}, {{k}})⟩. Compared with ⟨y = x^2⟩: ⟨h⟩ shifts it right (⟨x - h⟩), ⟨k⟩ shifts it up, ⟨|a| > 1⟩ makes it {{narrower}}, ⟨|a| < 1⟩ wider, and ⟨a < 0⟩ flips it {{upside down}}.',
    steps: ['⟨y = 2(x + 1)^2 - 3⟩: ⟨x + 1 = x - (-1)⟩, so the vertex is ⟨({{-1}}, {{-3}})⟩.', 'It opens up and is narrower than ⟨y = x^2⟩.'],
    figs: [{ t: 'plane', x: [-5, 3], y: [-4, 6], fns: [{ f: 'x*x', dash: true, color: '#888', lab: 'y = x²', at: [2.2, 5.6] }, { f: '2*(x+1)*(x+1)-3', lab: 'y = 2(x+1)² − 3', at: [-1.2, 5.6], anchor: 'end' }], pts: [[-1, -3, '{{(−1, −3)}}', null, null, 6, 4]], cap: 'Left 1, down 3, stretched by 2' }]
  }];
  N['U11-L4'] = [{
    h: 'Factored form',
    big: 'In ⟨y = a(x - p)(x - q)⟩ the zeros are ⟨x = {{p}}⟩ and ⟨x = {{q}}⟩. The axis of symmetry is {{halfway}} between them: ⟨x = \\frac{p + q}{2}⟩.',
    steps: ['⟨y = (x - 1)(x + 3)⟩: zeros ⟨x = 1⟩ and ⟨x = {{-3}}⟩.', 'Axis: ⟨x = \\frac{1 + (-3)}{2} = {{-1}}⟩.', 'Vertex: ⟨y = (-2)(2) = {{-4}}⟩, so ⟨(-1, -4)⟩.'],
    figs: [{ t: 'plane', x: [-5, 3], y: [-5, 5], fns: [{ f: '(x-1)*(x+3)' }], vl: [[-1, true, 'x = −1']], pts: [[1, 0, '{{1}}', null, null, 5, -6], [-3, 0, '{{−3}}', null, null, -5, -6], [-1, -4, '(−1, −4)', null, null, 6, 4]] }]
  }];
  N['U11-L5'] = [{
    h: 'Solving by graphing',
    big: 'The real solutions of ⟨ax^2 + bx + c = 0⟩ are the {{x-intercepts}} (zeros) of ⟨y = ax^2 + bx + c⟩. A parabola can cross the ⟨x⟩-axis twice ({{2}} solutions), touch it once (1 solution), or miss it ({{no real}} solutions).',
    steps: ['Graph the related function.', 'Read where it crosses ⟨y = 0⟩ (estimate if needed).', 'Check by substituting.'],
    figs: [{ t: 'plane', x: [-4, 4], y: [-3, 5], w: 150, nums: false, fns: [{ f: 'x*x-2' }], cap: '{{2}} solutions' }, { t: 'plane', x: [-4, 4], y: [-3, 5], w: 150, nums: false, fns: [{ f: '(x-1)*(x-1)' }], cap: '{{1}} solution' }, { t: 'plane', x: [-4, 4], y: [-3, 5], w: 150, nums: false, fns: [{ f: 'x*x+1' }], cap: '{{no real}} solutions' }]
  }];
  N['U11-L6'] = [{
    h: 'Solving by square roots',
    big: 'When there is no ⟨x⟩-term, {{isolate}} the squared part and take the square root of both sides. Every positive number has two square roots, so write {{±}}.',
    steps: ['⟨3x^2 - 5 = 22⟩ → ⟨3x^2 = 27⟩ → ⟨x^2 = 9⟩.', '⟨x = \\pm {{3}}⟩.', '⟨(x - 2)^2 = 12⟩ → ⟨x - 2 = \\pm\\sqrt{12} = \\pm 2\\sqrt{3}⟩ → ⟨x = {{2 \\pm 2\\sqrt{3}}}⟩.'],
    figs: []
  }];
  N['U11-L7'] = [{
    h: 'Completing the square',
    big: 'Make the ⟨x⟩-side a {{perfect square}}: add ⟨\\left(\\frac{b}{2}\\right)^2⟩ to {{both sides}}. Then factor and use square roots.',
    steps: ['⟨x^2 + 6x - 7 = 0⟩ → ⟨x^2 + 6x = 7⟩.', '⟨\\left(\\frac{6}{2}\\right)^2 = {{9}}⟩: ⟨x^2 + 6x + 9 = 16⟩.', '⟨(x + 3)^2 = 16⟩, ⟨x + 3 = \\pm 4⟩, ⟨x = {{1}}⟩ or ⟨x = {{-7}}⟩.'],
    figs: [{ t: 'area', top: ['x', '3'], side: ['x', '3'], cells: [['x²', '3x'], ['3x', '{{9}}']], cap: 'Split ⟨6x⟩ into two ⟨3x⟩ strips; the missing corner is ⟨{{9}}⟩' }]
  }];
  N['U11-L8'] = [{
    h: 'The quadratic formula',
    big: 'For ⟨ax^2 + bx + c = 0⟩ (standard form first!), ⟨x = \\dfrac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}⟩. Put negative values in {{parentheses}} when you substitute.',
    steps: ['⟨2x^2 - 3x - 2 = 0⟩: ⟨a = 2⟩, ⟨b = {{-3}}⟩, ⟨c = -2⟩.', '⟨x = \\frac{3 \\pm \\sqrt{9 + 16}}{4} = \\frac{3 \\pm {{5}}}{4}⟩.', '⟨x = {{2}}⟩ or ⟨x = {{-\\frac{1}{2}}}⟩.'],
    figs: []
  }];
  N['U11-L9'] = [{
    h: 'The discriminant',
    big: 'The {{discriminant}} ⟨b^2 - 4ac⟩ is the part under the square root. Positive → {{2}} real solutions; zero → {{1}} real solution; negative → {{no}} real solutions.',
    steps: ['⟨x^2 - 6x + 9 = 0⟩: ⟨(-6)^2 - 4(1)(9) = {{0}}⟩ → one solution.', '⟨x^2 + 2x + 5 = 0⟩: ⟨4 - 20 = {{-16}}⟩ → no real solutions.', 'Square ⟨b⟩ with its sign: ⟨(-6)^2 = +36⟩.'],
    figs: [{ t: 'tbl', head: ['⟨b^2 - 4ac⟩', '> 0', '= 0', '< 0'], rows: [['real solutions', '{{2}}', '{{1}}', '{{0}}'], ['graph', 'crosses twice', 'touches once', 'misses']] }]
  }];
  N['U11-L10'] = [{
    h: 'Choosing a method',
    big: 'Pick the quickest method: {{square roots}} when there is no ⟨x⟩-term, {{factoring}} when the trinomial factors easily, completing the square when ⟨a = 1⟩ and ⟨b⟩ is even, and the {{quadratic formula}} for anything else.',
    steps: ['⟨x^2 = 50⟩ → square roots.', '⟨x^2 - x - 12 = 0⟩ → factor: ⟨(x - 4)(x + 3)⟩.', '⟨3x^2 + 5x - 1 = 0⟩ → formula.'],
    figs: []
  }];
  N['U11-L11'] = [{
    h: 'Projectile models',
    big: 'Height of a launched object: ⟨h(t) = -16t^2 + v_0t + h_0⟩ (feet, seconds). The {{vertex}} gives the maximum height (⟨k⟩) and the time it happens (⟨h⟩). The positive {{zero}} is when it lands.',
    steps: ['⟨h(t) = -16t^2 + 64t + 80⟩: ⟨t = -\\frac{64}{2(-16)} = {{2}}⟩ s.', 'Max height: ⟨h(2) = -64 + 128 + 80 = {{144}}⟩ ft.', 'Lands when ⟨h = 0⟩: ⟨-16(t - 5)(t + 1) = 0⟩, ⟨t = {{5}}⟩ s.'],
    figs: [{ t: 'plane', x: [0, 6], y: [0, 160], step: 1, ystep: 20, numEveryY: 2, maxH: 170, xl: 't (s)', yl: 'h (ft)', fns: [{ f: '-16*x*x+64*x+80', dom: [0, 5] }], pts: [[2, 144, '{{max (2, 144)}}', null, null, 6, 2], [5, 0, '{{lands t = 5}}', null, null, -4, -8], [0, 80, '80 ft', null, null, 5, -4]] }]
  }];
  N['U11-L12'] = [{
    h: 'Which model fits?',
    big: 'Use equally spaced ⟨x⟩-values. Constant {{first differences}} → linear. Constant {{second differences}} → quadratic. Constant {{ratios}} → exponential.',
    steps: ['Find the first differences; if they are not equal, find the differences of those.', 'If neither is constant, try the ratios.'],
    figs: [{ t: 'tbl', head: ['⟨x⟩', '0', '1', '2', '3', '4'], rows: [['⟨y⟩', '1', '3', '9', '19', '33'], ['1st diff.', '', '2', '6', '10', '14'], ['2nd diff.', '', '', '{{4}}', '{{4}}', '{{4}}']], cap: 'Second differences constant → {{quadratic}}' }]
  }];
  /* ---------- Unit 12 · Statistics ---------- */
  N['U12-L1'] = [{
    h: 'Mean, median and mode',
    big: 'Measures of center summarize a data set with one number. {{Mean}}: add the values and divide by how many. {{Median}}: the middle value after putting the data {{in order}} (average the two middle values if there is an even count). {{Mode}}: the most frequent value.',
    steps: ['Data: 4, 8, 6, 5, 8, 9. Ordered: 4, 5, 6, 8, 8, 9.', 'Mean ⟨= \\frac{40}{6} \\approx {{6.67}}⟩.', 'Median ⟨= \\frac{6 + 8}{2} = {{7}}⟩. Mode ⟨= {{8}}⟩.'],
    figs: [{ t: 'dot', axis: [3, 10, 1], data: [4, 5, 6, 8, 8, 9], mark: [[7, '{{median 7}}']], cap: 'Half the data is on each side of the median' }]
  }];
  N['U12-L2'] = [{
    h: 'Dot plots, histograms and box plots',
    big: 'A {{dot plot}} shows every value. A {{histogram}} shows how many values fall in each interval (a bar is a count, not a data value). A {{box plot}} shows the five-number summary: minimum, ⟨Q_1⟩, median, ⟨Q_3⟩, maximum.',
    steps: ['Order the data and find the median.', '⟨Q_1⟩ is the median of the lower half; ⟨Q_3⟩ the median of the upper half.', 'IQR ⟨= Q_3 - Q_1⟩: the spread of the middle 50%.'],
    figs: [{ t: 'box', axis: [0, 20, 2], v: [2, 6, 9, 13, 18], labs: ['{{min}}', '{{Q₁}}', '{{median}}', '{{Q₃}}', '{{max}}'], cap: 'IQR ⟨= 13 - 6 = {{7}}⟩' },
      { t: 'hist', bins: [[0, 5, 2], [5, 10, 5], [10, 15, 4], [15, 20, 1]], cap: '5 values are from 5 up to 10' }]
  }];
  N['U12-L3'] = [{
    h: 'Shape, center and spread',
    big: 'A distribution can be {{symmetric}} or {{skewed}} (a long tail to one side). An {{outlier}} is far from the rest: below ⟨Q_1 - 1.5 \\cdot IQR⟩ or above ⟨Q_3 + 1.5 \\cdot IQR⟩. For skewed data or outliers use the {{median}} and IQR; for symmetric data use the mean and standard deviation.',
    steps: ['⟨Q_1 = 6⟩, ⟨Q_3 = 13⟩, IQR ⟨= 7⟩.', 'Fences: ⟨6 - 10.5 = -4.5⟩ and ⟨13 + 10.5 = {{23.5}}⟩.', 'A value of 30 is an {{outlier}}.'],
    figs: [{ t: 'dot', axis: [0, 12, 1], data: [1, 2, 2, 3, 3, 3, 4, 4, 5, 7, 11], cap: 'Skewed {{right}}: the tail is on the right' }]
  }];
  N['U12-L4'] = [{
    h: 'Two-way tables',
    big: 'A two-way table counts data in two categories. Numbers inside are {{joint}} frequencies; the totals are {{marginal}} frequencies. A {{conditional}} relative frequency divides by a row or column total, not the grand total.',
    steps: ['Of the students who play sports, what fraction prefer dogs? Use the Sports {{row}} total.', '⟨\\frac{30}{50} = {{60\\%}}⟩.'],
    figs: [{ t: 'tbl', head: ['', 'Dogs', 'Cats', 'Total'], rowHead: true, rows: [['Sports', '30', '20', '{{50}}'], ['No sports', '25', '25', '{{50}}'], ['Total', '{{55}}', '{{45}}', '100']] }]
  }];
  N['U12-L5'] = [{
    h: 'Scatter plots and association',
    big: 'A scatter plot shows paired data. Describe it by {{direction}} (positive: up to the right; negative: down to the right; none), {{form}} (linear or not), {{strength}} (how close to a line), and any outliers or clusters.',
    steps: ['Look at the whole cloud of points, not one point.', 'Use the words of the context: “as study time increases, scores tend to increase.”'],
    figs: [{ t: 'plane', x: [0, 10], y: [0, 10], w: 150, nums: false, xl: '', yl: '', pts: [[1, 2], [2, 2.5], [3, 3.8], [4, 4.2], [5, 5.5], [6, 5.6], [7, 7.2], [8, 7.6], [9, 9]], cap: '{{positive}}, strong' }, { t: 'plane', x: [0, 10], y: [0, 10], w: 150, nums: false, xl: '', yl: '', pts: [[1, 8.5], [2, 8.8], [3, 6.5], [4, 7], [5, 5], [6, 5.8], [7, 3.5], [8, 3.9], [9, 2]], cap: '{{negative}}' }, { t: 'plane', x: [0, 10], y: [0, 10], w: 150, nums: false, xl: '', yl: '', pts: [[1, 5], [2, 8], [3, 2], [4, 6], [5, 3], [6, 9], [7, 4], [8, 7], [9, 1.5]], cap: '{{no association}}' }]
  }];
  N['U12-L6'] = [{
    h: 'Lines of fit',
    big: 'A {{line of fit}} follows the trend with about as many points above it as below it. Use its equation to predict. Predicting inside the data range ({{interpolation}}) is more reliable than predicting outside it ({{extrapolation}}).',
    steps: ['Draw a line through the middle of the points.', 'Pick two points on the line (not necessarily data points) and write ⟨y = mx + b⟩.', 'Interpret the slope in context.'],
    figs: [{ t: 'plane', x: [0, 10], y: [0, 10], pts: [[1, 2], [2, 2.5], [3, 3.8], [4, 4.2], [5, 5.5], [6, 5.6], [7, 7.2], [8, 7.6], [9, 9]], fns: [{ f: '0.85*x+1', color: '#c0561b', lab: 'y ≈ 0.85x + 1', at: [3, 7.5] }] }]
  }];
  N['U12-L7'] = [{
    h: 'Correlation and causation',
    big: 'The correlation coefficient ⟨r⟩ is between −1 and 1. Its {{sign}} gives the direction and its distance from 0 gives the {{strength}} (close to ±1 is strong; close to 0 is weak). A strong correlation does {{not}} prove that one variable causes the other: a {{lurking variable}} may affect both.',
    steps: ['⟨r = -0.92⟩: strong {{negative}} linear association.', 'Ice cream sales and sunburns are correlated; heat (a lurking variable) causes both.'],
    figs: [{ t: 'nl', min: -1, max: 1, step: 0.25, w: 320, lab: [[-0.9, 'strong −'], [-0.25, '{{weak}}'], [0.25, 'weak'], [0.9, '{{strong +}}']], cap: 'The scale of ⟨r⟩' }]
  }];
  N['U12-L8'] = [{
    h: 'Residuals',
    big: 'A {{residual}} is ⟨\\text{actual} - \\text{predicted}⟩. A positive residual means the point is {{above}} the line. A residual plot with no pattern means a linear model is a good fit; a curved pattern means it is {{not}}.',
    steps: ['Model ⟨\\hat{y} = 2x + 1⟩; data point ⟨(3, 8)⟩.', 'Predicted: ⟨2(3) + 1 = {{7}}⟩.', 'Residual: ⟨8 - 7 = {{1}}⟩ (the point is 1 unit above the line).'],
    figs: [{ t: 'plane', x: [0, 5], y: [0, 10], fns: [{ f: '2*x+1' }], segs: [[3, 7, 3, 8, false]], pts: [[3, 8, '{{actual (3, 8)}}', null, '#c0561b', -6, -6], [3, 7, 'predicted', 'o', null, 6, 10]], cap: 'Residual = {{1}}' }]
  }];
  N['U3-L4'] = [{
    h: 'AND compound inequalities',
    big: 'An AND inequality is true only when {{both}} parts are true. Its graph is the {{overlap}} (intersection) of the two graphs, usually a {{segment}} between two endpoints.',
    steps: ['Solve each part — or work on all three parts of ⟨a < bx + c < d⟩ at once.', 'Flip {{both}} signs if you multiply or divide by a negative.', 'Graph the values that are in {{both}} solutions.'],
    figs: [{ t: 'nl', min: -4, max: 6, pts: [[-2, 'c', '{{−2}}'], [3, 'o', '{{3}}']], seg: [[-2, 3]], cap: '⟨-2 \\le x < 3⟩: closed at {{−2}}, open at {{3}}' }]
  }, {
    h: 'OR compound inequalities',
    big: 'An OR inequality is true when {{at least one}} part is true. Its graph is the {{union}} of the two graphs, usually two {{rays}} pointing away from each other.',
    steps: ['Solve each inequality separately.', 'Graph both solutions on one number line.', 'Write the answer with the word {{or}} between the two parts.'],
    figs: [{ t: 'nl', min: -5, max: 5, pts: [[-3, 'o'], [2, 'c']], ray: [[-3, '<'], [2, '>']], cap: '⟨x < -3⟩ {{or}} ⟨x \\ge 2⟩' }]
  }];
})(typeof window !== 'undefined' ? window : globalThis);
