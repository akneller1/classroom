/* Pre-Algebra (8th Grade) Unit 1 cheat sheet. Every worked example is checked by build.cjs. */
const F = require('../figs.cjs');
const order = F.svg(300, 46,
  '<line x1="14" y1="20" x2="286" y2="20" stroke="#333" stroke-width="1.5"/>' +
  [1, 1.5, 2, 2.5, 3].map(v => { const x = 22 + (v - 1) * 128; return `<line x1="${x}" y1="15" x2="${x}" y2="25" stroke="#333"/><text x="${x}" y="40" font-size="10" text-anchor="middle">${v}</text>`; }).join('') +
  [[Math.SQRT2, '√2', '#2563eb'], [Math.sqrt(5), '√5', '#db2777'], [1.7, '1.7', '#ea7a12']].map(p => { const x = 22 + (p[0] - 1) * 128; return `<circle cx="${x.toFixed(1)}" cy="20" r="4.5" fill="${p[2]}"/><text x="${x.toFixed(1)}" y="10" font-size="10" font-weight="700" fill="${p[2]}" text-anchor="middle">${p[1]}</text>`; }).join(''), 2.9);
module.exports = {
  name: 'prealgebra-real-numbers-exponents', course: 'Pre-Algebra (8th Grade)', unitNo: 1, unitName: 'Real Numbers and Exponents',
  focus: 'rational and irrational numbers, square and cube roots',
  morefocus: 'negative exponents, exponent rules and scientific notation',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['rational', 'Can be written as ⟨\\tfrac{a}{b}⟩ (b ≠ 0); decimal ends or repeats.', '⟨-3,\\ 0.75,\\ 0.\\overline{6}⟩'],
      ['irrational', 'Decimal never ends and never repeats.', '⟨\\sqrt{2},\\ \\pi⟩'],
      ['perfect square', 'A whole number squared.', '1, 4, 9, 16, 25, …'],
      ['square root', '⟨\\sqrt{n}⟩: the positive number whose square is ⟨n⟩.', '⟨\\sqrt{49} = 7⟩'],
      ['cube root', '⟨\\sqrt[3]{n}⟩: the number whose cube is ⟨n⟩.', '⟨\\sqrt[3]{-8} = -2⟩']] },
    { title: 'The Real Number System', color: 'blue', kind: 'sets' },
    { title: 'Fractions and Decimals', color: 'green', kind: 'example', text: 'Fraction → decimal: divide. A repeating decimal → fraction: let ⟨x⟩ be the decimal, multiply by 10 (or 100), subtract.',
      example: 'Write ⟨0.\\overline{4}⟩ as a fraction.', steps: [['Let', '⟨x = 0.444…⟩, so ⟨10x = 4.444…⟩'], ['Subtract:', '⟨9x = 4⟩']], answer: '⟨x = \\tfrac{4}{9}⟩', check: { num: '4/9', is: 0.4444444444444444 } },
    { title: 'Square and Cube Roots', color: 'orange', kind: 'table', plain: true, head: ['Solve or estimate', 'Answer'], rows: [
      ['⟨x^2 = 64⟩', '⟨x = \\pm 8⟩ (two solutions)'], ['⟨x^3 = -27⟩', '⟨x = -3⟩ (one solution)'], ['⟨\\sqrt{40}⟩ lies between', '⟨\\sqrt{36} = 6⟩ and ⟨\\sqrt{49} = 7⟩, closer to 6: ⟨\\approx 6.3⟩'], ['⟨\\sqrt{\\tfrac{9}{16}}⟩', '⟨\\tfrac{3}{4}⟩']],
      check: [{ num: 'Math.sqrt(40)', is: 6.324555320336759 }, { num: 'Math.cbrt(-27)', is: -3 }, { num: 'Math.sqrt(9/16)', is: 0.75 }] },
    { title: 'Comparing and Ordering', color: 'pink', kind: 'example', text: 'Estimate each irrational number with nearby perfect squares, then place it on a number line.',
      example: 'Order ⟨\\sqrt{5},\\ 1.7,\\ \\sqrt{2}⟩ from least to greatest.', steps: [['Estimate:', '⟨\\sqrt{2} \\approx 1.41⟩, ⟨\\sqrt{5} \\approx 2.24⟩']], answer: '⟨\\sqrt{2},\\ 1.7,\\ \\sqrt{5}⟩', fig: order,
      check: { true: 'Math.SQRT2 < 1.7 && 1.7 < Math.sqrt(5)' } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Every integer and every terminating or repeating decimal is rational.', '⟨\\sqrt{n}⟩ is irrational unless ⟨n⟩ is a perfect square.', 'Rational + irrational is irrational.'],
      bad: [['⟨x^2 = 25 \\Rightarrow x = 5⟩ only', 'also ⟨x = -5⟩'], ['Calling ⟨\\pi = 3.14⟩ rational', '3.14 is only an estimate'], ['⟨\\sqrt{-9} = -3⟩', 'no real square root']] }
  ],
  back: [
    { title: 'Exponent Rules', color: 'purple', kind: 'table', plain: true, head: ['Rule', 'Example'], rows: [
      ['⟨a^m \\cdot a^n = a^{m+n}⟩', '⟨2^3 \\cdot 2^4 = 2^7⟩'], ['⟨\\tfrac{a^m}{a^n} = a^{m-n}⟩', '⟨\\tfrac{5^6}{5^2} = 5^4⟩'], ['⟨(a^m)^n = a^{mn}⟩', '⟨(3^2)^3 = 3^6⟩'],
      ['⟨(ab)^n = a^n b^n⟩', '⟨(2x)^3 = 8x^3⟩'], ['⟨a^0 = 1⟩', '⟨7^0 = 1⟩'], ['⟨a^{-n} = \\tfrac{1}{a^n}⟩', '⟨4^{-2} = \\tfrac{1}{16}⟩']],
      check: [{ num: '2**3*2**4', is: 128 }, { num: '5**6/5**2', is: 625 }, { num: '(3**2)**3', is: 729 }, { num: '4**-2', is: 0.0625 }] },
    { title: 'Negative Exponents', color: 'blue', kind: 'example', text: 'A negative exponent means "reciprocal": move the factor across the fraction bar and make the exponent positive.',
      example: 'Simplify ⟨\\tfrac{x^{-3} y^2}{x^2}⟩.', steps: [['Subtract exponents:', '⟨x^{-3-2} = x^{-5}⟩'], ['Rewrite:', '⟨x^{-5} y^2 = \\tfrac{y^2}{x^5}⟩']], answer: '⟨\\tfrac{y^2}{x^5}⟩',
      check: { expr: 'x**-3*y**2/x**2', is: 'y**2/x**5' } },
    { title: 'Scientific Notation', color: 'green', kind: 'table', plain: true, head: ['Standard form', 'Scientific notation'], rows: [
      ['4,500,000', '⟨4.5 \\times 10^6⟩'], ['0.00072', '⟨7.2 \\times 10^{-4}⟩'], ['602,000,000,000,000,000,000,000', '⟨6.02 \\times 10^{23}⟩']],
      after: 'Form ⟨a \\times 10^n⟩ with ⟨1 \\le a < 10⟩. Big numbers: positive ⟨n⟩. Small numbers: negative ⟨n⟩.', check: [{ num: '4.5e6', is: 4500000 }, { num: '7.2e-4', is: 0.00072 }] },
    { title: 'Multiply and Divide', color: 'orange', kind: 'example', text: 'Multiply (or divide) the decimals, then use the exponent rules on the powers of 10. Fix ⟨a⟩ if it is not between 1 and 10.',
      example: '⟨(3 \\times 10^5)(4 \\times 10^{-2})⟩', steps: [['Multiply:', '⟨12 \\times 10^{3}⟩'], ['Adjust:', '⟨1.2 \\times 10^{4}⟩']], answer: '⟨1.2 \\times 10^{4}⟩ (12,000)',
      check: { num: '3e5*4e-2', is: 12000 } },
    { title: 'Add and Subtract', color: 'pink', kind: 'example', text: 'Rewrite so both numbers have the same power of 10, then add or subtract the decimals.',
      example: '⟨(5.1 \\times 10^4) + (3 \\times 10^3)⟩', steps: [['Match powers:', '⟨5.1 \\times 10^4 + 0.3 \\times 10^4⟩'], ['Add:', '⟨5.4 \\times 10^4⟩']], answer: '⟨5.4 \\times 10^4⟩',
      check: { num: '5.1e4+3e3', is: 54000 } },
    { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
      'Is ⟨a⟩ at least 1 and less than 10?', 'Did I add exponents when multiplying and subtract when dividing?', 'Did I rewrite negative exponents as positive in my final answer?',
      'Does the size make sense? ⟨10^{-4}⟩ is a small number; ⟨10^{6}⟩ is a million.'] }
  ]
};
