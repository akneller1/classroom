"""Discrete Math audit #11 (2026-11-18): proof skills practice writing proofs, not only recognizing them.
For each proof skill, six short proofs become (a) "put the steps in order" items and (b) four-part open-response items in
which students write each step. Run after standards.py."""
import os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from lib import load, save, items

NOTE = 'Original Claude-authored Discrete Math item (family: {}). Discrete Math audit 2026-11-18 (tools/discrete-audit-20261118/proofs.py).'
# (theorem, [4 proof lines], [4 part prompts]) per skill; lines are in the correct order.
P = {
 'number-theory-proof-skill-02': [
  ('If n is odd, then n² is odd.', ['Suppose n is an odd integer.', 'Then n = 2k + 1 for some integer k.', 'So n² = 4k² + 4k + 1 = 2(2k² + 2k) + 1.', 'Since 2k² + 2k is an integer, n² is odd.']),
  ('The sum of an even integer and an odd integer is odd.', ['Let m be even and n be odd.', 'Then m = 2a and n = 2b + 1 for some integers a and b.', 'So m + n = 2a + 2b + 1 = 2(a + b) + 1.', 'Since a + b is an integer, m + n is odd.']),
  ('If a | b and a | c, then a | (b + c).', ['Suppose a | b and a | c.', 'Then b = ar and c = as for some integers r and s.', 'So b + c = ar + as = a(r + s).', 'Since r + s is an integer, a | (b + c).']),
  ('The product of two odd integers is odd.', ['Let m and n be odd integers.', 'Then m = 2a + 1 and n = 2b + 1 for some integers a and b.', 'So mn = 4ab + 2a + 2b + 1 = 2(2ab + a + b) + 1.', 'Since 2ab + a + b is an integer, mn is odd.']),
  ('If n is a multiple of 6, then n is even.', ['Suppose n is a multiple of 6.', 'Then n = 6k for some integer k.', 'So n = 2(3k).', 'Since 3k is an integer, n is even.']),
  ('For every integer n, n² + n is even.', ['Let n be any integer.', 'Then n² + n = n(n + 1), a product of two consecutive integers.', 'One of n and n + 1 is even, say equal to 2m.', 'So n(n + 1) is 2 times an integer, hence even.'])],
 'number-theory-proof-skill-06': [
  ('There is no largest even integer.', ['Suppose there is a largest even integer N.', 'Then N + 2 is also an even integer.', 'But N + 2 > N.', 'This contradicts N being the largest, so there is no largest even integer.']),
  ('√2 is irrational.', ['Suppose √2 = a/b with integers a, b in lowest terms.', 'Then a² = 2b², so a² is even and therefore a is even: a = 2k.', 'Then 4k² = 2b², so b² = 2k² and b is even too.', 'Both a and b are even, contradicting lowest terms, so √2 is irrational.']),
  ('No integer is both even and odd.', ['Suppose n is both even and odd.', 'Then n = 2a and n = 2b + 1 for some integers a and b.', 'So 2a = 2b + 1, which gives 2(a − b) = 1 and a − b = 1/2.', 'But a − b is an integer, a contradiction; so no integer is both.']),
  ('The sum of a rational number and an irrational number is irrational.', ['Suppose r is rational, x is irrational and r + x is rational.', 'Then x = (r + x) − r is a difference of two rational numbers.', 'A difference of rational numbers is rational, so x is rational.', 'This contradicts x being irrational, so r + x is irrational.']),
  ('There are infinitely many primes.', ['Suppose there are only finitely many primes p₁, …, pₙ.', 'Let N = p₁p₂···pₙ + 1.', 'N has a prime factor, but dividing N by any pᵢ leaves remainder 1.', 'So N has a prime factor not in the list, a contradiction.']),
  ('If n² is even, then n is even (by contradiction).', ['Suppose n² is even but n is odd.', 'Then n = 2k + 1 for some integer k.', 'So n² = 2(2k² + 2k) + 1 is odd.', 'n² cannot be both even and odd, so n must be even.'])],
 'number-theory-proof-skill-07': [
  ('If n² is odd, then n is odd.', ['Contrapositive: if n is even, then n² is even.', 'Suppose n is even, so n = 2k for some integer k.', 'Then n² = 4k² = 2(2k²).', 'n² is even, so the contrapositive and therefore the original statement are true.']),
  ('If 3n + 2 is odd, then n is odd.', ['Contrapositive: if n is even, then 3n + 2 is even.', 'Suppose n = 2k for some integer k.', 'Then 3n + 2 = 6k + 2 = 2(3k + 1).', '3n + 2 is even, which proves the original statement.']),
  ('If xy is irrational, then x or y is irrational.', ['Contrapositive: if x and y are both rational, then xy is rational.', 'Suppose x = a/b and y = c/d with integers and b, d ≠ 0.', 'Then xy = ac/(bd) with bd ≠ 0.', 'So xy is rational, which proves the original statement.']),
  ('If n² is not divisible by 3, then n is not divisible by 3.', ['Contrapositive: if 3 | n, then 3 | n².', 'Suppose n = 3k for some integer k.', 'Then n² = 9k² = 3(3k²).', 'So 3 | n², which proves the original statement.']),
  ('If a + b ≥ 10, then a ≥ 5 or b ≥ 5.', ['Contrapositive: if a < 5 and b < 5, then a + b < 10.', 'Suppose a < 5 and b < 5.', 'Adding the inequalities gives a + b < 10.', 'So the contrapositive holds, and the original statement is true.']),
  ('If n² − 6n + 5 is even, then n is odd.', ['Contrapositive: if n is even, then n² − 6n + 5 is odd.', 'Suppose n = 2k for some integer k.', 'Then n² − 6n + 5 = 4k² − 12k + 5 = 2(2k² − 6k + 2) + 1.', 'That is odd, which proves the original statement.'])],
 'set-theory-skill-06': [
  ('A ∩ B ⊆ A ∪ B.', ['Let x ∈ A ∩ B.', 'Then x ∈ A and x ∈ B.', 'In particular x ∈ A.', 'So x ∈ A ∪ B, and therefore A ∩ B ⊆ A ∪ B.']),
  ('If A ⊆ B, then A − C ⊆ B − C.', ['Suppose A ⊆ B and let x ∈ A − C.', 'Then x ∈ A and x ∉ C.', 'Since A ⊆ B, x ∈ B.', 'So x ∈ B and x ∉ C, that is x ∈ B − C.']),
  ('If A ⊆ B and B ⊆ C, then A ⊆ C.', ['Suppose A ⊆ B and B ⊆ C, and let x ∈ A.', 'Since A ⊆ B, x ∈ B.', 'Since B ⊆ C, x ∈ C.', 'Every element of A is in C, so A ⊆ C.']),
  ('A − B ⊆ A ∩ B′.', ['Let x ∈ A − B.', 'Then x ∈ A and x ∉ B.', 'x ∉ B means x ∈ B′.', 'So x ∈ A ∩ B′, and A − B ⊆ A ∩ B′.']),
  ('If A ⊆ B, then B′ ⊆ A′.', ['Suppose A ⊆ B and let x ∈ B′.', 'Then x ∉ B.', 'If x were in A, then x would be in B, so x ∉ A.', 'So x ∈ A′, and B′ ⊆ A′.']),
  ('{n ∈ ℤ | 12 | n} ⊆ {n ∈ ℤ | 4 | n}.', ['Let n be an element of the first set.', 'Then n = 12k for some integer k.', 'So n = 4(3k), and 3k is an integer.', 'So 4 | n, and n is in the second set.'])],
 'set-theory-skill-07': [
  ('A ∪ (A ∩ B) = A.', ['A ∩ B ⊆ A, so every element of A ∪ (A ∩ B) is in A: A ∪ (A ∩ B) ⊆ A.', 'Conversely, every element of A is in A ∪ (A ∩ B): A ⊆ A ∪ (A ∩ B).', 'Each set is a subset of the other.', 'So A ∪ (A ∩ B) = A (absorption law).']),
  ('(A ∪ B)′ = A′ ∩ B′.', ['Let x ∈ (A ∪ B)′, so x ∉ A ∪ B, so x ∉ A and x ∉ B.', 'Then x ∈ A′ and x ∈ B′, so x ∈ A′ ∩ B′: (A ∪ B)′ ⊆ A′ ∩ B′.', 'Each step reverses: x ∈ A′ ∩ B′ means x ∉ A and x ∉ B, so x ∉ A ∪ B.', 'So A′ ∩ B′ ⊆ (A ∪ B)′, and the sets are equal.']),
  ('A − (A − B) = A ∩ B.', ['A − (A − B) = A ∩ (A ∩ B′)′ (difference law).', '= A ∩ (A′ ∪ B) (De Morgan, double complement).', '= (A ∩ A′) ∪ (A ∩ B) (distributive law).', '= ∅ ∪ (A ∩ B) = A ∩ B (complement and identity laws).']),
  ('(A − B) ∪ (A ∩ B) = A.', ['(A − B) ∪ (A ∩ B) = (A ∩ B′) ∪ (A ∩ B) (difference law).', '= A ∩ (B′ ∪ B) (distributive law).', '= A ∩ U (complement law).', '= A (identity law).']),
  ('A ∩ (B − A) = ∅.', ['A ∩ (B − A) = A ∩ (B ∩ A′) (difference law).', '= (A ∩ A′) ∩ B (commutative and associative laws).', '= ∅ ∩ B (complement law).', '= ∅ (universal bound law).']),
  ('A ∪ (B ∩ C) = (A ∪ B) ∩ (A ∪ C).', ['Let x ∈ A ∪ (B ∩ C): if x ∈ A it is in both A ∪ B and A ∪ C; if x ∈ B ∩ C it is in B and C, so again in both.', 'So A ∪ (B ∩ C) ⊆ (A ∪ B) ∩ (A ∪ C).', 'Let x ∈ (A ∪ B) ∩ (A ∪ C): if x ∈ A we are done; if x ∉ A then x ∈ B and x ∈ C, so x ∈ B ∩ C.', 'So (A ∪ B) ∩ (A ∪ C) ⊆ A ∪ (B ∩ C), and the sets are equal.'])],
 'sequences-induction-recursion-skill-08': [
  ('1 + 3 + 5 + … + (2n − 1) = n² for all n ≥ 1.', ['Base case: n = 1 gives 1 = 1².', 'Assume 1 + 3 + … + (2k − 1) = k² for some k ≥ 1.', 'Then 1 + 3 + … + (2k − 1) + (2k + 1) = k² + 2k + 1 = (k + 1)².', 'So the statement holds for k + 1, and by induction for all n ≥ 1.']),
  ('3 | (n³ − n) for all n ≥ 0.', ['Base case: n = 0 gives 0 = 3·0.', 'Assume 3 | (k³ − k) for some k ≥ 0.', '(k + 1)³ − (k + 1) = (k³ − k) + 3k² + 3k = (k³ − k) + 3(k² + k).', 'Both terms are multiples of 3, so 3 | ((k + 1)³ − (k + 1)); by induction it holds for all n ≥ 0.']),
  ('2ⁿ > n for all n ≥ 1.', ['Base case: n = 1 gives 2 > 1.', 'Assume 2ᵏ > k for some k ≥ 1.', 'Then 2ᵏ⁺¹ = 2·2ᵏ > 2k = k + k ≥ k + 1.', 'So 2ᵏ⁺¹ > k + 1, and by induction 2ⁿ > n for all n ≥ 1.']),
  ('1 + 2 + 4 + … + 2ⁿ = 2ⁿ⁺¹ − 1 for all n ≥ 0.', ['Base case: n = 0 gives 1 = 2 − 1.', 'Assume 1 + 2 + … + 2ᵏ = 2ᵏ⁺¹ − 1 for some k ≥ 0.', 'Then 1 + … + 2ᵏ + 2ᵏ⁺¹ = 2ᵏ⁺¹ − 1 + 2ᵏ⁺¹ = 2ᵏ⁺² − 1.', 'So the formula holds for k + 1, and by induction for all n ≥ 0.']),
  ('5ⁿ − 1 is divisible by 4 for all n ≥ 0.', ['Base case: n = 0 gives 5⁰ − 1 = 0 = 4·0.', 'Assume 4 | (5ᵏ − 1) for some k ≥ 0.', '5ᵏ⁺¹ − 1 = 5(5ᵏ − 1) + 4.', 'Both terms are multiples of 4, so 4 | (5ᵏ⁺¹ − 1); by induction it holds for all n ≥ 0.']),
  ('n! > 2ⁿ for all n ≥ 4.', ['Base case: n = 4 gives 24 > 16.', 'Assume k! > 2ᵏ for some k ≥ 4.', 'Then (k + 1)! = (k + 1)·k! > (k + 1)·2ᵏ ≥ 2·2ᵏ = 2ᵏ⁺¹, since k + 1 ≥ 2.', 'So (k + 1)! > 2ᵏ⁺¹, and by induction n! > 2ⁿ for all n ≥ 4.'])],
}
PARTS = {'number-theory-proof-skill-02': ['State what you assume.', 'Rewrite it with a definition.', 'Do the algebra.', 'Conclude, saying why the definition applies.'],
         'number-theory-proof-skill-06': ['State the assumption (the negation).', 'Write what follows from it.', 'Reason one more step.', 'Name the contradiction and conclude.'],
         'number-theory-proof-skill-07': ['Write the contrapositive.', 'State its hypothesis with a definition.', 'Do the algebra.', 'Conclude about the original statement.'],
         'set-theory-skill-06': ['Start with an arbitrary element.', 'Apply the definitions.', 'Use the given facts.', 'Conclude the subset relation.'],
         'set-theory-skill-07': ['First step.', 'Second step.', 'Third step.', 'Conclusion.'],
         'sequences-induction-recursion-skill-08': ['Prove the base case.', 'State the inductive hypothesis.', 'Do the inductive step.', 'Conclude.']}

B = load(); ids = {q['id'] for _, q in items(B)}; added = 0
CODE = {'number-theory-proof': 'np', 'set-theory': 'st', 'sequences-induction-recursion': 'sq'}
LEVELS = ['cp2', 'cp1', 'honors']
for sk, proofs in P.items():
    unit = sk.rsplit('-skill-', 1)[0]; s = int(sk.rsplit('-', 1)[1])
    std = next(q['standards'] for _, q in items(B) if q['skillId'] == sk)
    for i, (thm, lines) in enumerate(proofs):
        lv = LEVELS[i % 3]
        rng = random.Random(sk + str(i)); order = list(range(4))
        while order == [0, 1, 2, 3]: rng.shuffle(order)
        letters = 'ABCD'; shown = [lines[j] for j in order]
        ans = ''.join(letters[order.index(j)] for j in range(4))
        def nid(kind):
            k = 1
            while f'dm-{CODE[unit]}-s{s:02d}-{lv}-{kind}{k:02d}' in ids: k += 1
            ids.add(f'dm-{CODE[unit]}-s{s:02d}-{lv}-{kind}{k:02d}'); return f'dm-{CODE[unit]}-s{s:02d}-{lv}-{kind}{k:02d}'
        B[unit]['questions'].append({'id': nid('p'), 'skillId': sk, 'level': lv, 'format': 'short-answer',
            'prompt': f'Theorem: {thm}\nPut the steps of the proof in order:\n' + '\n'.join(f'({letters[k]}) {t}' for k, t in enumerate(shown)) + '\nAnswer with the four letters, like ABCD.',
            'answer': ans, 'solutionSteps': [f'A proof starts from what is assumed: ({ans[0]}) {lines[0]}', f'Then ({ans[1]}) and ({ans[2]}) apply the definitions and do the work: {lines[1]} {lines[2]}', f'It ends with the conclusion ({ans[3]}): {lines[3]}', f'Order: {ans}.'],
            'sourceNotes': NOTE.format('proof_order'), 'standards': std})
        B[unit]['questions'].append({'id': nid('w'), 'skillId': sk, 'level': LEVELS[(i + 1) % 3] if False else lv, 'format': 'open-response',
            'prompt': f'Write a proof: {thm}', 'answer': ' | '.join(f'({"abcd"[k]}) {t}' for k, t in enumerate(lines)),
            'solutionSteps': list(lines), 'parts': [{'prompt': PARTS[sk][k], 'answer': lines[k]} for k in range(4)],
            'sourceNotes': NOTE.format('proof_write'), 'standards': std})
        added += 2
save(B)
print('proof items added', added)
