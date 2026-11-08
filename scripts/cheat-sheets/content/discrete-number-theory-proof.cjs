/* Discrete Math Unit 3 cheat sheet (Elementary Number Theory and Methods of Proof). Every worked example is checked by build.cjs. */
module.exports = {
  name: 'discrete-number-theory-proof', course: 'Discrete Math', unitNo: 3, unitName: 'Number Theory and Proof',
  focus: 'definitions, counterexamples, direct proof, existential and universal statements, rational numbers',
  morefocus: 'divisibility, the quotient-remainder theorem, proof by contradiction and contraposition, choosing a strategy',
  front: [
    { title: 'Definitions to Use', color: 'purple', kind: 'vocab', rows: [
      ['even', '⟨n = 2k⟩ for some integer ⟨k⟩', '⟨-6 = 2(-3)⟩'],
      ['odd', '⟨n = 2k + 1⟩ for some integer ⟨k⟩', '⟨7 = 2(3) + 1⟩'],
      ['rational', '⟨r = a/b⟩, integers, ⟨b \\ne 0⟩', '⟨0.75 = 3/4⟩'],
      ['divides', '⟨d \\mid n⟩ means ⟨n = dk⟩, ⟨k⟩ an integer', '⟨3 \\mid 12⟩'],
      ['prime', '⟨n > 1⟩ with divisors only 1, ⟨n⟩', '2, 3, 5, 7, 11'],
      ['composite', '⟨n > 1⟩ and not prime', '⟨91 = 7 \\cdot 13⟩']] },
    { title: 'Example vs Proof', color: 'blue', kind: 'table', plain: true, head: ['Goal', 'What is enough'], rows: [
      ['prove “there exists …”', 'one example (a witness)'],
      ['disprove “for all …”', 'one counterexample'],
      ['prove “for all …”', 'a general argument with an arbitrary element'],
      ['disprove “there exists …”', 'a general argument that nothing works']],
      after: '⟨n^2 + n + 41⟩ is prime for ⟨n = 0, \\dots, 39⟩, but ⟨n = 40⟩ gives ⟨41^2⟩: examples never prove “for all”.',
      check: { num: '40*40+40+41', is: 1681 } },
    { title: 'Direct Proof Template', color: 'green', kind: 'example', text: '<b>Suppose</b> the hypothesis for an arbitrary element → <b>write</b> definitions → <b>algebra</b> → <b>conclude</b> with the definition.',
      example: 'If ⟨m⟩ and ⟨n⟩ are odd, then ⟨mn⟩ is odd.', steps: [['Suppose:', '⟨m = 2a + 1⟩, ⟨n = 2b + 1⟩'], ['Multiply:', '⟨mn = 4ab + 2a + 2b + 1⟩'], ['Rewrite:', '⟨mn = 2(2ab + a + b) + 1⟩']], answer: '⟨mn⟩ is odd since ⟨2ab + a + b⟩ is an integer',
      check: { true: '[-3,0,2,5].every(a => [-1,4,7].every(b => (2*a+1)*(2*b+1) === 2*(2*a*b+a+b)+1))' } },
    { title: 'Rational Numbers', color: 'orange', kind: 'example', text: 'Rationals are closed under ⟨+, -, \\times⟩ and ⟨\\div⟩ by nonzero numbers. Repeating decimals are rational.',
      example: 'Write ⟨x = 0.\\overline{45}⟩ as a fraction.', steps: [['Multiply:', '⟨100x = 45.\\overline{45}⟩'], ['Subtract:', '⟨99x = 45⟩, so ⟨x = 45/99⟩']], answer: '⟨\\tfrac{5}{11}⟩',
      check: { num: '45/99', is: 5 / 11 } },
    { title: 'Counterexamples', color: 'pink', kind: 'words', rows: [
      ['“Every prime is odd.”', '2'], ['“⟨x^2 > x⟩ for every real ⟨x⟩.”', '⟨x = \\tfrac{1}{2}⟩'], ['“If ⟨a \\mid bc⟩ then ⟨a \\mid b⟩ or ⟨a \\mid c⟩.”', '⟨6 \\mid 2 \\cdot 3⟩'], ['“The product of irrationals is irrational.”', '⟨\\sqrt2 \\cdot \\sqrt2 = 2⟩']],
      check: [{ true: '0.25 < 0.5' }, { true: '(2*3) % 6 === 0 && 2 % 6 !== 0 && 3 % 6 !== 0' }] },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Use different letters for different numbers (⟨m = 2a⟩, ⟨n = 2b⟩).', 'Say why the factor is an integer.', 'End with the definition you are proving.'],
      bad: [['Proving with examples', 'use an arbitrary element'], ['⟨(2k + 1)^2 = 4k^2 + 1⟩', 'it is ⟨4k^2 + 4k + 1⟩'], ['Assuming what you want to prove', 'that is circular']] }
  ],
  back: [
    { title: 'Quotient-Remainder Theorem', color: 'purple', kind: 'example', text: 'For any integer ⟨n⟩ and ⟨d > 0⟩ there are unique ⟨q, r⟩ with ⟨n = dq + r⟩ and ⟨0 \\le r < d⟩.',
      example: '⟨n = -17⟩, ⟨d = 5⟩', steps: [['Choose q:', '⟨q = -4⟩ (not ⟨-3⟩)'], ['Check:', '⟨5(-4) + 3 = -17⟩']], answer: '⟨q = -4,\\ r = 3⟩',
      check: { num: '5*(-4)+3', is: -17 } },
    { title: 'Divisibility Facts', color: 'blue', kind: 'table', plain: true, head: ['Fact', 'Why'], rows: [
      ['⟨a \\mid b⟩ and ⟨b \\mid c⟩ ⟹ ⟨a \\mid c⟩', '⟨c = bs = a(rs)⟩'],
      ['⟨a \\mid b⟩ and ⟨a \\mid c⟩ ⟹ ⟨a \\mid (xb + yc)⟩', '⟨xb + yc = a(xr + ys)⟩'],
      ['⟨n(n + 1)⟩ is even', 'one of two consecutive integers is even'],
      ['⟨\\gcd(252, 198) = 18⟩', 'Euclid: ⟨252 = 198 + 54⟩, ⟨198 = 3 \\cdot 54 + 36⟩, ⟨54 = 36 + 18⟩, ⟨36 = 2 \\cdot 18⟩']],
      check: [{ num: '252-198', is: 54 }, { num: '198-3*54', is: 36 }, { num: '54-36', is: 18 }, { num: '36 % 18', is: 0 }] },
    { title: 'Proof by Contradiction', color: 'green', kind: 'example', text: 'Assume the statement is <b>false</b>; reason until you reach something impossible.',
      example: 'Prove ⟨\\sqrt2⟩ is irrational.', steps: [['Assume:', '⟨\\sqrt2 = a/b⟩ in lowest terms'], ['Then:', '⟨a^2 = 2b^2⟩, so ⟨a⟩ is even, ⟨a = 2k⟩'], ['Then:', '⟨b^2 = 2k^2⟩, so ⟨b⟩ is even too']], answer: 'Contradiction: ⟨a/b⟩ was not in lowest terms' },
    { title: 'Proof by Contraposition', color: 'orange', kind: 'example', text: 'To prove ⟨p \\to q⟩, prove ⟨\\neg q \\to \\neg p⟩ (they are equivalent).',
      example: 'If ⟨n^2⟩ is even, then ⟨n⟩ is even.', steps: [['Contrapositive:', 'if ⟨n⟩ is odd, ⟨n^2⟩ is odd'], ['Proof:', '⟨n = 2k + 1⟩ ⟹ ⟨n^2 = 2(2k^2 + 2k) + 1⟩']], answer: 'proved',
      check: { true: '[-4,-1,0,3,8].every(k => (2*k+1)**2 === 2*(2*k*k+2*k)+1)' } },
    { title: 'Choosing a Strategy', color: 'pink', kind: 'table', plain: true, head: ['Statement looks like …', 'Try'], rows: [
      ['“There is …”', 'give a witness'], ['“For all …” with usable definitions', 'direct proof'], ['“There is no …”, “… is irrational”, “infinitely many”', 'contradiction'],
      ['“If ⟨n^2⟩ …, then ⟨n⟩ …”', 'contraposition'], ['finite domain', 'exhaustion (check every case)'], ['false “for all”', 'counterexample']] },
    { title: 'Challenge: Infinitely Many Primes', color: 'teal', kind: 'html',
      html: 'Suppose the primes were only ⟨p_1, p_2, \\dots, p_n⟩. Let ⟨N = p_1 p_2 \\cdots p_n + 1⟩. Some prime ⟨p⟩ divides ⟨N⟩. It must be one of the ⟨p_i⟩, so ⟨p⟩ divides ⟨N - p_1\\cdots p_n = 1⟩ — impossible. So there are infinitely many primes. (⟨N⟩ itself need not be prime: ⟨2\\cdot3\\cdot5\\cdot7\\cdot11\\cdot13 + 1 = 30031 = 59 \\cdot 509⟩.)',
      check: [{ num: '2*3*5*7*11*13+1', is: 30031 }, { num: '59*509', is: 30031 }] }
  ]
};
