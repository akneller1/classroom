/* Discrete Math Unit 4 cheat sheet (Sequences, Mathematical Induction, and Recursion). Every worked example is checked by build.cjs. */
const fib = n => { let a = 1, b = 1; for (let k = 2; k < n; k++) [a, b] = [b, a + b]; return n <= 2 ? 1 : b; };
const C = (n, r) => { let x = 1; for (let i = 1; i <= r; i++) x = x * (n - r + i) / i; return Math.round(x); };
module.exports = {
  name: 'discrete-sequences-induction-recursion', course: 'Discrete Math', unitNo: 4, unitName: 'Sequences, Induction & Recursion',
  focus: 'explicit and recursive sequences, arithmetic and geometric patterns, factorials, binomial coefficients, Fibonacci',
  morefocus: 'iteration, the principle of mathematical induction, writing inductive proofs, patterns and tessellations',
  front: [
    { title: 'Sequence Language', color: 'purple', kind: 'vocab', rows: [
      ['explicit formula', 'term from ⟨n⟩ directly', '⟨a_n = 3n - 1⟩: 2, 5, 8, …'],
      ['recursive rule', 'term from earlier terms', '⟨a_1 = 2,\\ a_n = a_{n-1} + 3⟩'],
      ['summation', 'add the terms', '⟨\\sum_{k=1}^{4} k^2 = 30⟩'],
      ['product', 'multiply the terms', '⟨\\prod_{k=1}^{4} k = 24⟩']],
      check: [{ num: '1+4+9+16', is: 30 }, { num: '1*2*3*4', is: 24 }] },
    { title: 'Arithmetic and Geometric', color: 'blue', kind: 'table', head: ['', 'Arithmetic', 'Geometric'], rows: [
      ['rule', 'add ⟨d⟩', 'multiply by ⟨r⟩'],
      ['⟨n⟩th term', '⟨a_n = a_1 + (n - 1)d⟩', '⟨a_n = a_1 r^{n-1}⟩'],
      ['sum of ⟨n⟩ terms', '⟨\\tfrac{n(a_1 + a_n)}{2}⟩', '⟨a_1\\tfrac{r^n - 1}{r - 1}⟩'],
      ['example', '4, 7, 10, …: ⟨a_{10} = 31⟩', '3, 6, 12, …: ⟨a_6 = 96⟩']],
      after: '⟨1 + 2 + \\dots + n = \\tfrac{n(n + 1)}{2}⟩, so ⟨1 + \\dots + 100 = 5050⟩.',
      check: [{ num: '4+9*3', is: 31 }, { num: '3*2**5', is: 96 }, { num: '100*101/2', is: 5050 }] },
    { title: 'Factorials and C(n, r)', color: 'green', kind: 'example', text: '⟨n! = n(n - 1)\\cdots 1⟩, ⟨0! = 1⟩. ⟨\\binom{n}{r} = \\tfrac{n!}{r!\\,(n - r)!}⟩ counts ⟨r⟩-element subsets. Pascal: ⟨\\binom{n}{r} = \\binom{n-1}{r-1} + \\binom{n-1}{r}⟩.',
      example: 'Evaluate ⟨\\binom{7}{3}⟩.', steps: [['Cancel:', '⟨\\tfrac{7 \\cdot 6 \\cdot 5}{3 \\cdot 2 \\cdot 1}⟩'], ['Pascal check:', '⟨\\binom{6}{2} + \\binom{6}{3} = 15 + 20⟩']], answer: '35',
      check: [{ num: C(7, 3), is: 35 }, { num: C(6, 2) + C(6, 3), is: 35 }] },
    { title: 'Fibonacci Numbers', color: 'orange', kind: 'table', head: ['⟨n⟩', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], rows: [['⟨F_n⟩', ...[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(n => String(fib(n)))]],
      after: '⟨F_1 = F_2 = 1⟩, ⟨F_n = F_{n-1} + F_{n-2}⟩. Sum: ⟨F_1 + \\dots + F_n = F_{n+2} - 1⟩. Ratios ⟨F_{n+1}/F_n⟩ approach ⟨\\varphi \\approx 1.618⟩.',
      check: [{ num: fib(10), is: 55 }, { num: [1, 2, 3, 4, 5, 6].reduce((s, n) => s + fib(n), 0), is: fib(8) - 1 }] },
    { title: 'Iteration', color: 'pink', kind: 'example', text: 'Unwind the recurrence until a pattern appears, then check it.',
      example: '⟨m_1 = 1,\\ m_k = 2m_{k-1} + 1⟩ (Tower of Hanoi)', steps: [['Terms:', '1, 3, 7, 15, 31'], ['Pattern:', '⟨m_k = 2^k - 1⟩'], ['Check:', '⟨2(2^{k-1} - 1) + 1 = 2^k - 1⟩']], answer: '⟨m_{10} = 1023⟩',
      check: [{ true: '[1,3,7,15,31].every((v, i) => v === 2**(i+1) - 1)' }, { num: '2**10-1', is: 1023 }] },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Check where the index starts (⟨a_0⟩ or ⟨a_1⟩).', 'Use the previous term, not the first term, in a recursion.', 'Cancel factorials before multiplying.'],
      bad: [['⟨a_{10} = a_1 + 10d⟩', 'it is ⟨a_1 + 9d⟩'], ['⟨0! = 0⟩', '⟨0! = 1⟩'], ['⟨\\tfrac{8!}{6!} = (\\tfrac{8}{6})!⟩', '⟨8 \\cdot 7 = 56⟩']] }
  ],
  back: [
    { title: 'Mathematical Induction', color: 'purple', kind: 'table', plain: true, head: ['Step', 'What you write'], rows: [
      ['1. Base case', 'Check ⟨P(a)⟩ for the first value ⟨a⟩.'],
      ['2. Inductive hypothesis', 'Assume ⟨P(k)⟩ for an arbitrary ⟨k \\ge a⟩.'],
      ['3. Inductive step', 'Show ⟨P(k + 1)⟩ follows from ⟨P(k)⟩.'],
      ['4. Conclusion', 'By induction, ⟨P(n)⟩ is true for all ⟨n \\ge a⟩.']],
      after: 'Dominoes: the first falls, and each one knocks over the next. Strong induction assumes ⟨P(a), \\dots, P(k)⟩.' },
    { title: 'Sum Formula Proof', color: 'blue', kind: 'example', text: 'Prove ⟨1 + 3 + \\dots + (2n - 1) = n^2⟩ for ⟨n \\ge 1⟩.',
      example: 'Base ⟨n = 1⟩: ⟨1 = 1^2⟩.', steps: [['Assume:', '⟨1 + \\dots + (2k - 1) = k^2⟩'], ['Add next term:', '⟨k^2 + (2k + 1)⟩'], ['Factor:', '⟨= (k + 1)^2⟩']], answer: '⟨P(k + 1)⟩ holds',
      check: { true: '[1,2,3,4,9].every(k => k*k + 2*k + 1 === (k+1)**2)' } },
    { title: 'Divisibility Proof', color: 'green', kind: 'example', text: 'Rewrite the ⟨k + 1⟩ expression to contain the old one.',
      example: 'Prove ⟨4 \\mid (5^n - 1)⟩ for ⟨n \\ge 0⟩.', steps: [['Base:', '⟨5^0 - 1 = 0⟩'], ['Step:', '⟨5^{k+1} - 1 = 5(5^k - 1) + 4⟩'], ['Both parts:', 'divisible by 4']], answer: 'true for all ⟨n \\ge 0⟩',
      check: { true: '[0,1,2,3,6].every(k => 5**(k+1) - 1 === 5*(5**k - 1) + 4 && (5**k - 1) % 4 === 0)' } },
    { title: 'Inequality Proof', color: 'orange', kind: 'example', text: 'Use the hypothesis, then a simple bound.',
      example: 'Prove ⟨2^n \\ge n + 1⟩ for ⟨n \\ge 0⟩.', steps: [['Base:', '⟨2^0 = 1 \\ge 1⟩'], ['Step:', '⟨2^{k+1} = 2 \\cdot 2^k \\ge 2(k + 1) = 2k + 2⟩'], ['Bound:', '⟨2k + 2 \\ge k + 2⟩']], answer: '⟨2^{k+1} \\ge (k + 1) + 1⟩',
      check: { true: '[0,1,2,5,10].every(k => 2**k >= k + 1)' } },
    { title: 'Patterns and Tessellations', color: 'pink', kind: 'table', plain: true, head: ['Fact', 'Example'], rows: [
      ['regular ⟨n⟩-gon interior angle ⟨\\tfrac{(n - 2)180°}{n}⟩', 'hexagon: 120°'],
      ['diagonals of an ⟨n⟩-gon ⟨\\tfrac{n(n - 3)}{2}⟩', 'octagon: 20'],
      ['triangular numbers ⟨T_n = \\tfrac{n(n+1)}{2}⟩', '1, 3, 6, 10, 15'],
      ['regular tessellations', 'only triangles (6 at a vertex), squares (4), hexagons (3)']],
      after: 'A regular polygon tiles the plane alone exactly when its interior angle divides 360°.',
      check: [{ num: '4*180/6', is: 120 }, { num: '8*5/2', is: 20 }, { num: '6*60', is: 360 }, { num: '3*120', is: 360 }] },
    { title: 'Mistakes and Challenge', color: 'teal', kind: 'mistakes',
      good: ['Always write the base case.', 'In the step, start from ⟨P(k)⟩; the goal is ⟨P(k + 1)⟩.', 'Check the step works for every ⟨k \\ge⟩ the base value.'],
      bad: [['Assuming ⟨P(k + 1)⟩', 'that is circular'], ['Base case at the wrong ⟨n⟩', 'use the smallest claimed value'], ['Challenge: “all horses are one color”', 'the step fails from ⟨k = 1⟩ to 2']] }
  ]
};
