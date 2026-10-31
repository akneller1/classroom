module.exports = {
  name: 'sequences-series', course: 'Algebra 2', unitNo: 8, unitName: 'Sequences & Series',
  focus: 'arithmetic and geometric sequences, recursive and explicit formulas',
  morefocus: 'arithmetic and geometric series, sigma notation, infinite series and applications',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['sequence', 'An ordered list of terms ⟨a_1, a_2, a_3, \\dots⟩.', '⟨2, 5, 8, \\dots⟩'], ['common difference ⟨d⟩', 'Constant added each step (arithmetic).', '⟨d = 3⟩'],
      ['common ratio ⟨r⟩', 'Constant multiplier each step (geometric).', '⟨r = 2⟩'], ['series', 'The sum of the terms of a sequence.', '⟨2 + 5 + 8⟩'],
      ['recursive formula', 'Gives a term from the one before it.', '⟨a_n = a_{n-1} + 3⟩']] },
    { title: 'Arithmetic Sequences', color: 'blue', kind: 'example', text: '⟨a_n = a_1 + (n - 1)d⟩. Linear: equal differences.',
      example: '⟨7, 11, 15, \\dots⟩: find ⟨a_{20}⟩.', steps: [['⟨d = 4⟩:', '⟨a_{20} = 7 + 19(4)⟩']], answer: '⟨a_{20} = 83⟩', check: { num: '7+19*4', is: 83 } },
    { title: 'Geometric Sequences', color: 'green', kind: 'example', text: '⟨a_n = a_1 \\cdot r^{\\,n - 1}⟩. Exponential: equal ratios.',
      example: '⟨3, 6, 12, \\dots⟩: find ⟨a_{10}⟩.', steps: [['⟨r = 2⟩:', '⟨a_{10} = 3 \\cdot 2^9⟩']], answer: '⟨a_{10} = 1536⟩', check: { num: '3*2**9', is: 1536 } },
    { title: 'Recursive ↔ Explicit', color: 'orange', kind: 'table', head: ['Recursive', 'Explicit'], rows: [
      ['⟨a_1 = 5,\\ a_n = a_{n-1} - 3⟩', '⟨a_n = 8 - 3n⟩'], ['⟨a_1 = 2,\\ a_n = 3a_{n-1}⟩', '⟨a_n = 2 \\cdot 3^{\\,n - 1}⟩'], ['⟨a_1 = 64,\\ a_n = \\tfrac{1}{2}a_{n-1}⟩', '⟨a_n = 64\\left(\\tfrac{1}{2}\\right)^{n - 1}⟩']],
      after: 'Check: ⟨a_3⟩ is ⟨-1⟩, ⟨18⟩ and ⟨16⟩ from either form.', check: { list: ['8-3*3', '2*3**2', '64*0.5**2'], is: [-1, 18, 16] } },
    { title: 'Which Kind?', color: 'pink', kind: 'words', rows: [
      ['⟨2, 5, 8, 11, \\dots⟩ (differences 3)', 'arithmetic, ⟨d = 3⟩'], ['⟨81, 27, 9, 3, \\dots⟩ (ratios ⟨\\tfrac{1}{3}⟩)', 'geometric, ⟨r = \\tfrac{1}{3}⟩'], ['⟨1, 4, 9, 16, \\dots⟩', 'neither'], ['⟨5, -10, 20, -40, \\dots⟩', 'geometric, ⟨r = -2⟩']] },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['⟨n⟩ counts terms: the first term is ⟨n = 1⟩.', 'Find ⟨r⟩ as later ÷ earlier.', 'A recursive formula needs a starting term.'],
      bad: [['⟨a_n = a_1 + nd⟩', 'it is ⟨(n - 1)d⟩'], ['⟨a_n = (a_1 r)^{n - 1}⟩', 'only ⟨r⟩ is raised to the power'], ['⟨r = 3⟩ for ⟨81, 27, 9⟩', '⟨r = \\tfrac{27}{81} = \\tfrac{1}{3}⟩']] }
  ],
  back: [
    { title: 'Arithmetic Series', color: 'purple', kind: 'example', text: '⟨S_n = \\dfrac{n(a_1 + a_n)}{2}⟩: number of terms × average of first and last.',
      example: '⟨3 + 7 + 11 + \\dots + 79⟩', steps: [['Count:', '⟨n = \\tfrac{79 - 3}{4} + 1 = 20⟩'], ['Sum:', '⟨\\tfrac{20(3 + 79)}{2}⟩']], answer: '⟨820⟩',
      check: { num: 'Array.from({length:20},(_,i)=>3+4*i).reduce((a,b)=>a+b)', is: 820 } },
    { title: 'Geometric Series', color: 'blue', kind: 'example', text: '⟨S_n = \\dfrac{a_1(1 - r^n)}{1 - r}⟩, ⟨r \\ne 1⟩.',
      example: 'First 8 terms of ⟨2 + 6 + 18 + \\dots⟩', steps: [['⟨r = 3⟩:', '⟨S_8 = \\dfrac{2(1 - 3^8)}{1 - 3}⟩']], answer: '⟨6560⟩',
      check: { num: 'Array.from({length:8},(_,i)=>2*3**i).reduce((a,b)=>a+b)', is: 6560 } },
    { title: 'Sigma Notation', color: 'green', kind: 'words', rows: [
      ['⟨\\displaystyle\\sum_{k=1}^{5} (2k + 1) = 3 + 5 + 7 + 9 + 11⟩', '⟨35⟩'], ['⟨\\displaystyle\\sum_{k=1}^{4} 3 \\cdot 2^{k-1} = 3 + 6 + 12 + 24⟩', '⟨45⟩'], ['⟨\\displaystyle\\sum_{k=1}^{100} k⟩', '⟨5050⟩']],
      check: { list: ['3+5+7+9+11', '3+6+12+24', '100*101/2'], is: [35, 45, 5050] } },
    { title: 'Infinite Geometric Series', color: 'orange', kind: 'example', text: 'Converges only when ⟨|r| < 1⟩: ⟨S = \\dfrac{a_1}{1 - r}⟩. If ⟨|r| \\ge 1⟩ it diverges (no sum).',
      example: '⟨12 + 6 + 3 + \\dots⟩ and ⟨0.\\overline{3} = 0.3 + 0.03 + \\dots⟩', steps: [['⟨r = \\tfrac{1}{2}⟩:', '⟨\\tfrac{12}{1 - 1/2} = 24⟩'], ['⟨r = \\tfrac{1}{10}⟩:', '⟨\\tfrac{0.3}{0.9} = \\tfrac{1}{3}⟩']], answer: '⟨24⟩ and ⟨\\tfrac{1}{3}⟩',
      check: { list: ['12/(1-0.5)', '0.3/0.9'], is: [24, 1 / 3] } },
    { title: 'Application: Seating', color: 'pink', kind: 'example', text: 'Equal increases each row: arithmetic. Total seats: an arithmetic series.',
      example: 'Row 1 has 20 seats; each row has 2 more; 25 rows.', steps: [['Last row:', '⟨a_{25} = 20 + 24(2) = 68⟩'], ['Total:', '⟨\\tfrac{25(20 + 68)}{2}⟩']], answer: '⟨1100⟩ seats',
      check: { num: 'Array.from({length:25},(_,i)=>20+2*i).reduce((a,b)=>a+b)', is: 1100 } },
    { title: 'Application: Bouncing Ball', color: 'teal', kind: 'example', text: 'Each bounce is a fixed percent of the last: geometric. Count up and down trips.',
      example: 'Dropped from 10 ft; each rebound is 60% as high.', steps: [['Rebounds:', '⟨6 + 3.6 + \\dots = \\tfrac{6}{1 - 0.6} = 15⟩'], ['Total:', '⟨10 + 2(15)⟩ (up and down)']], answer: '⟨40⟩ ft',
      check: { num: '10+2*(6/(1-0.6))', is: 40 } }
  ]
};
