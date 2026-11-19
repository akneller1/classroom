"""Teaching notes for the 77 Discrete Math skills (Discrete Math audit #5, 2026-11-18).
Each record: obj (objective, completes "Students will be able to …"), idea (key idea), voc ([term, meaning] pairs),
watch (common mistake) and one explanation card (h, big, steps; {{…}} marks a blank on guided notes).
Run: python3 tools/discrete-audit-20261118/notes.py  → worksheet-generator/planner/notes-teach-discrete.js"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def R(obj, idea, voc, watch, h, big, steps):
    return {'obj': obj, 'idea': idea, 'voc': voc, 'watch': watch, 'cards': [{'h': h, 'big': big, 'steps': steps}]}


N = {}
u = 'speaking-mathematically-skill-'
N[u + '01'] = R('use variables to write mathematical statements and decide whether a sentence is a statement',
    'A statement is a sentence that is true or false, but not both; a variable is a placeholder that lets one sentence say something about many objects.',
    [['statement', 'A sentence that is true or false, but not both.'], ['variable', 'A symbol that stands for any element of a set.'], ['open sentence', 'A sentence with a variable, true for some values and false for others.']],
    'Calling a question, a command or an open sentence such as "x + 2 = 5" a statement.',
    'Statements and variables', 'Rewrite "Is there a number that is its own square?" with a variable.',
    ['Name the object: let x be a {{real number}}.', 'State the property: x² = x.', 'Is the open sentence x² = x a statement? {{No — its truth depends on x}}.'])
N[u + '02'] = R('write and decide the truth of universal and existential statements',
    '"For all" (∀) claims something about every element of the domain; "there exists" (∃) claims it for at least one. One counterexample defeats ∀; one example proves ∃.',
    [['universal statement', 'A statement of the form ∀x ∈ D, P(x).'], ['existential statement', 'A statement of the form ∃x ∈ D such that P(x).'], ['counterexample', 'An element of the domain that makes a universal statement false.']],
    'Proving a universal statement by checking a few examples.',
    'Quantifiers', 'Decide: ∀ integers n, n² ≥ n.',
    ['Try to break it: n = 0 gives 0 ≥ 0; n = −2 gives 4 ≥ −2.', 'Argue generally: if n ≤ 0 then n² ≥ 0 ≥ n; if n ≥ 1 then n·n ≥ {{n·1 = n}}.', 'So the statement is {{true}}.'])
N[u + '03'] = R('write conditional statements in if–then form and identify the hypothesis and conclusion',
    '"If p, then q" promises q whenever p happens; it is false only when p is true and q is false.',
    [['conditional', 'A statement "if p, then q", written p → q.'], ['hypothesis', 'The "if" part p.'], ['conclusion', 'The "then" part q.']],
    'Treating "q if p" or "p only if q" as having the hypothesis in the wrong place.',
    'If–then form', 'Rewrite "A square is a rectangle" as a conditional.',
    ['The hypothesis is the condition: {{x is a square}}.', 'The conclusion is what follows: {{x is a rectangle}}.', 'If x is a square, then x is a rectangle.'])
N[u + '04'] = R('write sets in roster and set-builder notation and move between the two',
    'Roster notation lists the elements; set-builder notation {x ∈ D | P(x)} describes them by a property. Order and repetition do not matter in a set.',
    [['roster notation', 'A list of elements in braces, such as {1, 2, 3}.'], ['set-builder notation', '{x ∈ D | P(x)}: the elements of D that make P(x) true.'], ['empty set', 'The set with no elements, ∅.']],
    'Including the endpoints of a strict inequality, or listing a repeated element twice.',
    'Two ways to write a set', 'Write {n ∈ ℤ | −2 ≤ n < 3} in roster notation.',
    ['Integers from −2 up to but not including 3.', 'Roster: {{{−2, −1, 0, 1, 2}}}.', 'How many elements? {{5}}.'])
N[u + '05'] = R('decide set membership and subset relations, including with the empty set',
    'x ∈ A compares an element with a set; A ⊆ B compares two sets and means every element of A is in B. ∅ is a subset of every set.',
    [['element (∈)', 'An object that belongs to a set.'], ['subset (⊆)', 'A ⊆ B when every element of A is in B.'], ['proper subset', 'A ⊆ B with A ≠ B.']],
    'Confusing ∈ with ⊆, e.g. writing 2 ⊆ {1, 2, 3} or {2} ∈ {1, 2, 3}.',
    'Element or subset?', 'Decide each for B = {1, {2}, 3}.',
    ['1 ∈ B is {{true}}.', '{2} ∈ B is {{true}} (it is listed); {2} ⊆ B is {{false}} because 2 ∉ B.', '∅ ⊆ B is always {{true}}.'])
N[u + '06'] = R('list and count Cartesian products and use ordered pairs',
    'A × B is the set of ordered pairs (a, b) with a ∈ A and b ∈ B, so |A × B| = |A|·|B|; (a, b) = (c, d) only when a = c and b = d.',
    [['ordered pair', '(a, b), where order matters.'], ['Cartesian product', 'A × B = {(a, b) | a ∈ A, b ∈ B}.'], ['ordered n-tuple', 'An ordered list (x₁, …, xₙ).']],
    'Writing pairs of A × B with the coordinates reversed, or assuming A × B = B × A.',
    'Cartesian products', 'A = {1, 2}, B = {x, y, z}.',
    ['List A × B: {{(1, x), (1, y), (1, z), (2, x), (2, y), (2, z)}}.', '|A × B| = 2·3 = {{6}}.', 'Is (x, 1) ∈ A × B? {{No — the first coordinate must come from A}}.'])
N[u + '07'] = R('find the lengths and concatenations of strings over an alphabet and count strings',
    'A string over Σ is a finite ordered list of symbols from Σ; there are |Σ|ⁿ strings of length n, and the empty string λ has length 0.',
    [['alphabet', 'A finite set Σ of symbols.'], ['string', 'A finite sequence of symbols from the alphabet.'], ['concatenation', 'st: the string s followed by the string t.']],
    'Adding instead of multiplying when counting strings (e.g. 3 + 2 for strings of length 3 over {a, b}).',
    'Strings', 'Strings over Σ = {0, 1}.',
    ['Length of 01101: {{5}}.', 'Number of strings of length 4: 2⁴ = {{16}}.', 'Strings of length at most 2, including λ: 1 + 2 + 4 = {{7}}.'])

u = 'compound-statements-logic-skill-'
N[u + '01'] = R('translate between English and symbols using ¬, ∧ and ∨ and find truth values',
    '¬p flips the truth value, p ∧ q is true only when both are true, and p ∨ q (inclusive or) is false only when both are false.',
    [['negation', '¬p, "not p".'], ['conjunction', 'p ∧ q, "p and q"; "but" also means ∧.'], ['disjunction', 'p ∨ q, "p or q" (inclusive).']],
    'Reading "or" as exclusive, or translating "neither p nor q" as ¬p ∨ ¬q instead of ¬p ∧ ¬q.',
    'Connectives', 'p: "It is cold."  q: "It is windy."',
    ['"It is cold but not windy": {{p ∧ ¬q}}.', '"Neither cold nor windy": {{¬p ∧ ¬q}}.', 'If p is T and q is F, p ∨ q is {{T}}.'])
N[u + '02'] = R('build truth tables for compound statements',
    'With n variables a truth table has 2ⁿ rows; build intermediate columns, then combine them row by row in a fixed order (TT, TF, FT, FF).',
    [['truth table', 'A table giving a statement\'s truth value for every combination of its variables.'], ['row', 'One assignment of T/F to the variables.'], ['truth column', 'The final column read top to bottom.']],
    'Using fewer than 2ⁿ rows, or listing the rows in a nonstandard order and misreading the column.',
    'Building a truth table', 'Find the column for ¬p ∨ q.',
    ['¬p over TT, TF, FT, FF: {{FFTT}}.', 'Combine with q (TFTF) using ∨.', 'Column: {{TFTT}}.'])
N[u + '03'] = R('decide logical equivalence with truth tables and laws such as De Morgan\'s',
    'Two forms are equivalent exactly when their truth columns agree in every row; De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q and ¬(p ∨ q) ≡ ¬p ∧ ¬q.',
    [['logically equivalent (≡)', 'Same truth value in every row.'], ['De Morgan\'s laws', 'Negating ∧ gives ∨ of negations, and vice versa.'], ['tautology', 'A form that is true in every row.']],
    'Distributing ¬ without switching ∧ and ∨, e.g. ¬(p ∧ q) ≡ ¬p ∧ ¬q.',
    'Equivalence', 'Show ¬(p ∧ q) ≡ ¬p ∨ ¬q.',
    ['Column of p ∧ q: TFFF, so ¬(p ∧ q): {{FTTT}}.', 'Column of ¬p ∨ ¬q: {{FTTT}}.', 'The columns agree, so the forms are {{equivalent}}.'])
N[u + '04'] = R('find truth values of conditionals and biconditionals and rewrite p → q as ¬p ∨ q',
    'p → q is false only in the row p = T, q = F, so p → q ≡ ¬p ∨ q; p ↔ q is true when p and q agree.',
    [['conditional', 'p → q, false only when p is true and q is false.'], ['biconditional', 'p ↔ q, "p if and only if q".'], ['vacuously true', 'A conditional with a false hypothesis.']],
    'Thinking a conditional with a false hypothesis is false.',
    'The conditional', 'Column of p → q.',
    ['Only row TF is false: {{TFTT}}.', 'p → q ≡ {{¬p ∨ q}}.', '"If 2 + 2 = 5, then pigs fly" is {{true}} (vacuously).'])
N[u + '05'] = R('negate conditional statements correctly in symbols and in words',
    '¬(p → q) ≡ p ∧ ¬q: the negation of "if p then q" says p happens and q does not. It is not another if–then statement.',
    [['negation of a conditional', 'p ∧ ¬q.'], ['counterexample', 'A case where the hypothesis holds and the conclusion fails.']],
    'Writing the negation of "if p then q" as "if p then not q" or as the inverse.',
    'Negating a conditional', 'Negate "If it rains, the game is canceled."',
    ['Form: p → q, negation {{p ∧ ¬q}}.', 'In words: {{It rains and the game is not canceled}}.', 'Check: the negation is true exactly when the original is {{false}}.'])
N[u + '06'] = R('write the converse, inverse and contrapositive and decide which are equivalent',
    'Converse q → p, inverse ¬p → ¬q, contrapositive ¬q → ¬p. Only the contrapositive is equivalent to the original; the converse and inverse are equivalent to each other.',
    [['converse', 'q → p.'], ['inverse', '¬p → ¬q.'], ['contrapositive', '¬q → ¬p, equivalent to p → q.']],
    'Assuming the converse of a true statement is true.',
    'Related conditionals', '"If a number is a multiple of 4, then it is even."',
    ['Converse: {{If a number is even, then it is a multiple of 4}} (false: 6).', 'Contrapositive: {{If a number is not even, then it is not a multiple of 4}} (true).', 'Inverse: {{If a number is not a multiple of 4, then it is not even}}.'])
N[u + '07'] = R('test arguments for validity and use rules of inference such as modus ponens and modus tollens',
    'An argument is valid when every row that makes all premises true also makes the conclusion true; modus ponens (p → q, p ∴ q) and modus tollens (p → q, ¬q ∴ ¬p) are valid forms.',
    [['valid argument', 'The conclusion is true in every row where all premises are true.'], ['modus ponens', 'p → q, p ∴ q.'], ['modus tollens', 'p → q, ¬q ∴ ¬p.']],
    'Judging an argument valid because its conclusion is true, instead of checking its form.',
    'Valid arguments', 'Premises: if Lin works, she eats out; Lin did not eat out.',
    ['Symbols: w → e, ¬e.', 'Rule: {{modus tollens}}.', 'Conclusion: {{Lin did not work (¬w)}}.'])
N[u + '08'] = R('recognize the converse and inverse errors and contradictions',
    'p → q, q ∴ p (converse error) and p → q, ¬p ∴ ¬q (inverse error) are invalid: some row makes the premises true and the conclusion false. A contradiction is false in every row.',
    [['converse error', 'Concluding p from p → q and q.'], ['inverse error', 'Concluding ¬q from p → q and ¬p.'], ['contradiction', 'A form false in every row.']],
    'Accepting "If it rains the grass is wet; the grass is wet; so it rained."',
    'Fallacies', 'Show p → q, q ∴ p is invalid.',
    ['Look for a row with both premises true and p false.', 'Row (p, q) = {{(F, T)}}: p → q is T, q is T, p is F.', 'So the form is {{invalid (converse error)}}.'])

u = 'number-theory-proof-skill-'
N[u + '01'] = R('use the definitions of even, odd, prime and composite and test conjectures with counterexamples',
    'Even means n = 2k, odd means n = 2k + 1 (k an integer); a prime has exactly two positive divisors. Examples can suggest a conjecture, but one counterexample disproves it.',
    [['even / odd', 'n = 2k / n = 2k + 1 for some integer k.'], ['prime', 'An integer greater than 1 whose only positive divisors are 1 and itself.'], ['conjecture', 'A statement believed true but not yet proved.']],
    'Treating many examples that work as a proof.',
    'Definitions and counterexamples', 'Conjecture: n² + n + 41 is prime for every n ≥ 0.',
    ['It works for n = 0, 1, …, 39.', 'At n = 40: 40² + 40 + 41 = {{1681 = 41²}}.', 'So the conjecture is {{false}}.'])
N[u + '02'] = R('write direct proofs of statements about integers',
    'A direct proof assumes the hypothesis, rewrites it with definitions, uses algebra, and reaches the conclusion in the form the definition requires.',
    [['direct proof', 'Assume p, deduce q.'], ['arbitrary element', 'A general element with no special properties assumed.']],
    'Using one specific number instead of an arbitrary one, or the same letter k for two different integers.',
    'Direct proof', 'Prove: the sum of two odd integers is even.',
    ['Let m = 2a + 1 and n = {{2b + 1}} for integers a, b.', 'm + n = 2a + 2b + 2 = {{2(a + b + 1)}}.', 'a + b + 1 is an integer, so m + n is {{even}}.'])
N[u + '03'] = R('prove existential statements with a witness and universal statements in general, and disprove with counterexamples',
    '∃ needs one witness; a false ∀ needs one counterexample; a true ∀ needs an argument for an arbitrary element (or exhaustion over a finite domain).',
    [['witness', 'An element that makes an existential statement true.'], ['method of exhaustion', 'Checking every element of a finite domain.']],
    'Trying to prove a universal statement with a witness.',
    'Proving and disproving', 'There is a positive integer n with n² > 50.',
    ['Try n = 7: 49 > 50 is {{false}}.', 'n = 8: 64 > 50, so n = {{8}} is a witness.', 'One witness is {{enough}} for an existential statement.'])
N[u + '04'] = R('prove facts about rational numbers and use the quotient–remainder theorem',
    'A rational number is a/b with integers a, b and b ≠ 0; for any integer n and d > 0 there are unique q, r with n = dq + r and 0 ≤ r < d.',
    [['rational number', 'a/b with a, b integers and b ≠ 0.'], ['quotient–remainder theorem', 'n = dq + r with 0 ≤ r < d.'], ['closure', 'An operation on elements of a set stays in the set.']],
    'Allowing a negative remainder when n is negative.',
    'Rationals and remainders', 'Find q and r for −17 = 5q + r.',
    ['r must satisfy {{0 ≤ r < 5}}.', '5·(−4) = −20, so r = −17 − (−20) = {{3}}.', 'q = {{−4}}, r = 3.'])
N[u + '05'] = R('prove divisibility facts and use gcd, lcm and prime factorization',
    'd | n means n = dk for some integer k; gcd(a, b)·lcm(a, b) = ab, and the Euclidean algorithm finds the gcd by repeated remainders.',
    [['divides (d | n)', 'n = dk for some integer k.'], ['gcd', 'The largest positive integer dividing both numbers.'], ['lcm', 'The smallest positive common multiple.']],
    'Writing 6 | 3 because 3 = 6·½: k must be an integer.',
    'Divisibility', 'Prove: if a | b and b | c, then a | c.',
    ['b = ak and c = {{bm}} for integers k, m.', 'Substitute: c = (ak)m = {{a(km)}}.', 'km is an integer, so {{a | c}}.'])
N[u + '06'] = R('write proofs by contradiction',
    'Assume the statement is false, reason correctly to something impossible (an integer both even and odd, a fraction not in lowest terms), and conclude the statement is true.',
    [['proof by contradiction', 'Assume ¬p and derive a contradiction.'], ['contradiction', 'A statement that cannot be true.']],
    'Assuming the conclusion instead of its negation, or stopping before an actual contradiction appears.',
    'Proof by contradiction', 'Prove there is no largest integer.',
    ['Assume {{there is a largest integer N}}.', 'N + 1 is an integer and {{N + 1 > N}}.', 'This contradicts N being largest, so {{there is no largest integer}}.'])
N[u + '07'] = R('prove statements by proving their contrapositive',
    'p → q is equivalent to ¬q → ¬p, so proving the contrapositive directly proves the original; this helps when ¬q gives a usable form (such as n = 2k + 1).',
    [['contraposition', 'Proving p → q by proving ¬q → ¬p.'], ['contrapositive', '¬q → ¬p.']],
    'Proving the converse instead of the contrapositive.',
    'Proof by contraposition', 'Prove: if n² is even, then n is even.',
    ['Contrapositive: {{if n is odd, then n² is odd}}.', 'n = 2k + 1 gives n² = 4k² + 4k + 1 = {{2(2k² + 2k) + 1}}.', 'So n² is odd, which proves the {{original statement}}.'])
N[u + '08'] = R('choose a suitable proof strategy for a statement',
    'Match the strategy to the form: ∃ → witness; false ∀ → counterexample; true ∀ conditional → direct proof, or contraposition/contradiction when the negation is easier to use.',
    [['strategy', 'The method chosen for a proof.'], ['negation', 'The opposite statement, used in contradiction and contraposition.']],
    'Starting a direct proof when the hypothesis gives nothing to work with (e.g. "n² is even").',
    'Choosing a strategy', 'Match each statement to a method.',
    ['"Some prime is even": {{witness (2)}}.', '"Every odd number is prime": {{counterexample (9)}}.', '"√7 is irrational": {{contradiction}}.'])

u = 'sequences-induction-recursion-skill-'
N[u + '01'] = R('find terms of sequences from explicit formulas and evaluate Σ and Π notation',
    'An explicit formula gives a_n directly from n; Σ adds and Π multiplies the terms for the stated range of the index.',
    [['explicit formula', 'A rule for a_n in terms of n.'], ['summation notation', 'Σ_{k=m}^{n} a_k = a_m + … + a_n.'], ['index', 'The variable that runs through the range.']],
    'Starting at the wrong index (n = 0 vs n = 1) or including one term too few.',
    'Terms and sums', 'a_n = 3n − 1 for n ≥ 1.',
    ['First four terms: {{2, 5, 8, 11}}.', 'Σ_{k=1}^{4} a_k = {{26}}.', 'a_20 = {{59}}.'])
N[u + '02'] = R('recognize arithmetic and geometric sequences and find terms and sums',
    'Arithmetic: add d each time, a_n = a₁ + (n − 1)d; geometric: multiply by r, a_n = a₁rⁿ⁻¹. Sums: n(a₁ + a_n)/2 and a₁(rⁿ − 1)/(r − 1).',
    [['common difference', 'd = a_{n+1} − a_n.'], ['common ratio', 'r = a_{n+1}/a_n.'], ['series', 'The sum of the terms of a sequence.']],
    'Using n instead of n − 1 steps from the first term.',
    'Arithmetic and geometric', 'a₁ = 3, d = 4.',
    ['a_20 = 3 + {{19}}·4 = {{79}}.', 'Sum of the first 20 terms: 20(3 + 79)/2 = {{820}}.', 'If instead r = 2: a_6 = 3·2⁵ = {{96}}.'])
N[u + '03'] = R('evaluate and simplify factorials and binomial coefficients',
    'n! = n(n − 1)···1 with 0! = 1, and C(n, k) = n!/(k!(n − k)!) counts k-element subsets; cancel before multiplying.',
    [['factorial', 'n! = n(n − 1)···2·1, with 0! = 1.'], ['binomial coefficient', 'C(n, k), the number of k-element subsets of an n-set.'], ['Pascal\'s rule', 'C(n, k) = C(n − 1, k − 1) + C(n − 1, k).']],
    'Computing large factorials in full instead of cancelling, or forgetting 0! = 1.',
    'Factorials', 'Evaluate 7!/5! and C(7, 3).',
    ['7!/5! = 7·6 = {{42}}.', 'C(7, 3) = 7·6·5/(3·2·1) = {{35}}.', 'C(7, 4) = {{35}}, by symmetry.'])
N[u + '04'] = R('generate Fibonacci numbers and use Fibonacci identities',
    'F₁ = F₂ = 1 and F_n = F_{n−1} + F_{n−2}; many identities (such as F₁ + … + F_n = F_{n+2} − 1) can be checked and proved by induction.',
    [['Fibonacci sequence', '1, 1, 2, 3, 5, 8, …'], ['recurrence relation', 'A rule giving each term from earlier terms.']],
    'Starting with F₁ = 1, F₂ = 2, which shifts every term.',
    'Fibonacci numbers', 'List and add.',
    ['F₁ to F₈: {{1, 1, 2, 3, 5, 8, 13, 21}}.', 'F₁ + … + F₆ = {{20}}.', 'F₈ − 1 = {{20}}, as the identity says.'])
N[u + '05'] = R('compute terms of recursively defined sequences and write recursive definitions',
    'A recursive definition gives initial term(s) and a rule for each later term from earlier ones; compute the terms in order.',
    [['recursive definition', 'Initial conditions plus a recurrence.'], ['initial condition', 'The given first term(s).']],
    'Applying the rule to n instead of to the previous term.',
    'Recursion', 'a₁ = 4, a_n = a_{n−1} + 3.',
    ['a₂ = {{7}}, a₃ = {{10}}.', 'a₅ = {{16}}.', 'Explicit form: a_n = {{3n + 1}}.'])
N[u + '06'] = R('use iteration to find explicit formulas for recurrences and solve recursive problems',
    'Iterate a recurrence a few times, spot the pattern, write the explicit formula, then check it (ideally by induction).',
    [['iteration', 'Repeatedly substituting the recurrence into itself.'], ['closed form', 'An explicit formula for a_n.']],
    'Guessing a pattern from too few terms without checking it.',
    'Iteration', 'a₀ = 2, a_n = 3a_{n−1} − 2.',
    ['Terms: 2, {{4, 10, 28}}.', 'a_n − 1 = 1, 3, 9, 27, so a_n = {{3ⁿ + 1}}.', 'Check: 3(3ⁿ⁻¹ + 1) − 2 = {{3ⁿ + 1}}.'])
N[u + '07'] = R('state the parts of a proof by mathematical induction',
    'Show P(base) is true; then assume P(k) for an arbitrary k and prove P(k + 1). Together these give P(n) for every n from the base on.',
    [['base case', 'P(n₀) for the smallest n.'], ['inductive hypothesis', 'The assumption that P(k) is true.'], ['inductive step', 'Proving P(k) → P(k + 1).']],
    'Assuming P(k + 1) (what must be shown) instead of P(k).',
    'Induction outline', 'P(n): 1 + 2 + … + n = n(n + 1)/2.',
    ['Base: n = 1, 1 = {{1·2/2}}.', 'Hypothesis: {{1 + … + k = k(k + 1)/2}}.', 'Goal: 1 + … + k + (k + 1) = {{(k + 1)(k + 2)/2}}.'])
N[u + '08'] = R('write complete inductive proofs for sums, divisibility and inequalities',
    'In the inductive step, find P(k) inside P(k + 1): split off the last term of a sum, rewrite 5^{k+1} − 1 = 5(5ᵏ − 1) + 4, or chain inequalities.',
    [['inductive step', 'P(k) → P(k + 1).'], ['strong induction', 'Assuming P for all values up to k.']],
    'Doing algebra on both sides of P(k + 1) as if it were known to be true.',
    'Completing the step', 'Prove 4 | 5ⁿ − 1.',
    ['Base: 5⁰ − 1 = 0 = {{4·0}}.', '5^{k+1} − 1 = 5(5ᵏ − 1) + {{4}}.', 'Both terms are multiples of 4, so {{4 | 5^{k+1} − 1}}.'])
N[u + '09'] = R('describe and count growing patterns, polygon angles and tessellations',
    'Count how a pattern grows from figure to figure to get a formula; the interior angles of an n-gon add to (n − 2)·180°, and a regular polygon tiles the plane alone only if its angle divides 360°.',
    [['figurate numbers', 'Counts from growing dot patterns (triangular, square, …).'], ['tessellation', 'A covering of the plane by shapes with no gaps or overlaps.'], ['interior angle', 'An angle inside a polygon at a vertex.']],
    'Dividing 360° by n for the interior angle (that is the exterior angle).',
    'Patterns and tilings', 'Regular polygons.',
    ['Each interior angle of a regular hexagon: (6 − 2)·180/6 = {{120°}}.', '360/120 = 3, so hexagons {{tile the plane}}.', 'A regular pentagon has 108°; 360/108 is not whole, so it {{does not tile}}.'])

u = 'set-theory-skill-'
N[u + '01'] = R('decide set equality and work with the empty set',
    'A = B exactly when each is a subset of the other (same elements); ∅ has no elements, is a subset of every set, and differs from {∅} and {0}.',
    [['set equality', 'A = B when A ⊆ B and B ⊆ A.'], ['empty set', '∅ = { }, the set with no elements.']],
    'Thinking {0} or {∅} is empty.',
    'Equal sets', 'Compare sets.',
    ['{1, 2, 3} = {3, 1, 2}? {{Yes — order does not matter}}.', 'Is {0} = ∅? {{No — {0} has one element}}.', '|{∅}| = {{1}}.'])
N[u + '02'] = R('find unions, intersections and differences of sets',
    'A ∪ B: in either set; A ∩ B: in both; A − B: in A but not in B. Work inside parentheses first and go element by element.',
    [['union', 'A ∪ B = {x | x ∈ A or x ∈ B}.'], ['intersection', 'A ∩ B = {x | x ∈ A and x ∈ B}.'], ['difference', 'A − B = {x | x ∈ A and x ∉ B}.']],
    'Treating A − B as B − A, or listing an element twice in a union.',
    'Set operations', 'A = {1, 2, 3, 4}, B = {3, 4, 5}.',
    ['A ∪ B = {{{1, 2, 3, 4, 5}}}.', 'A ∩ B = {{{3, 4}}}.', 'A − B = {{{1, 2}}}; B − A = {{{5}}}.'])
N[u + '03'] = R('find complements and evaluate expressions with several set operations',
    "A′ = U − A depends on the universe U; De Morgan's laws (A ∪ B)′ = A′ ∩ B′ and (A ∩ B)′ = A′ ∪ B′ simplify complements of combinations.",
    [['universal set', 'The set U that contains everything under discussion.'], ['complement', "A′ = U − A."], ["De Morgan's laws for sets", "(A ∪ B)′ = A′ ∩ B′; (A ∩ B)′ = A′ ∪ B′."]],
    "Taking the complement relative to the wrong set, or writing (A ∪ B)′ = A′ ∪ B′.",
    'Complements', 'U = {1, …, 6}, A = {1, 2}, B = {2, 3}.',
    ["A′ = {{{3, 4, 5, 6}}}.", "(A ∪ B)′ = {{{4, 5, 6}}}.", "A′ ∩ B′ = {{{4, 5, 6}}}, as De Morgan says."])
N[u + '04'] = R('draw and read Venn diagrams with two and three sets',
    'Each region of a Venn diagram is one combination of in/out for every set; fill the innermost overlap first and subtract outward when given totals.',
    [['Venn diagram', 'Overlapping regions showing how sets relate.'], ['region', 'The part of the diagram for one in/out combination.']],
    'Writing a set total in the outer part of a circle instead of subtracting the overlaps.',
    'Venn diagrams', '30 students: 18 play soccer, 12 play chess, 5 play both.',
    ['Soccer only: 18 − 5 = {{13}}.', 'Chess only: {{7}}.', 'Neither: 30 − (13 + 7 + 5) = {{5}}.'])
N[u + '05'] = R('list and count the elements of power sets',
    'P(A) is the set of all subsets of A, including ∅ and A itself; if |A| = n then |P(A)| = 2ⁿ.',
    [['power set', 'P(A) = {S | S ⊆ A}.'], ['subset count', 'Each element is in or out: 2ⁿ subsets.']],
    'Leaving out ∅ or A itself.',
    'Power sets', 'A = {a, b, c}.',
    ['|P(A)| = 2³ = {{8}}.', 'Subsets with 2 elements: {{{a, b}, {a, c}, {b, c}}}.', 'Is ∅ ∈ P(A)? {{Yes}}.'])
N[u + '06'] = R('prove that one set is a subset of another by the element method',
    'To prove A ⊆ B, let x be an arbitrary element of A, use the definition of A, and show x satisfies the definition of B.',
    [['element argument', 'Proving A ⊆ B by showing an arbitrary x ∈ A is in B.'], ['arbitrary element', 'An element about which nothing special is assumed.']],
    'Checking a few elements instead of an arbitrary one.',
    'Element method', 'Prove A ∩ B ⊆ A.',
    ['Let x ∈ A ∩ B.', 'By definition, x ∈ A {{and}} x ∈ B.', 'In particular {{x ∈ A}}, so A ∩ B ⊆ A.'])
N[u + '07'] = R('prove set equalities and identities with element arguments and set laws',
    'A = B is proved by showing A ⊆ B and B ⊆ A, or by a chain of set laws (De Morgan, distributive, absorption, complement) applied one step at a time.',
    [['set identity', 'An equation true for all sets.'], ['distributive law', 'A ∩ (B ∪ C) = (A ∩ B) ∪ (A ∩ C).'], ['absorption law', 'A ∪ (A ∩ B) = A.']],
    'Proving only one of the two inclusions.',
    'Proving identities', 'Show A − (A − B) = A ∩ B with laws.',
    ["A − (A − B) = A ∩ (A ∩ B′)′.", "= A ∩ ({{A′ ∪ B}}) by De Morgan.", "= (A ∩ A′) ∪ (A ∩ B) = {{A ∩ B}}."])
N[u + '08'] = R('disprove false set statements with counterexamples',
    'A false "for all sets" statement is disproved by one specific choice of sets that makes the two sides differ; small sets like ∅ and {1} usually suffice.',
    [['counterexample', 'Specific sets for which the statement is false.'], ['universal statement', 'A claim about all sets, false if one choice of sets fails.']],
    'Arguing in general that a statement "seems false" instead of giving specific sets.',
    'Disproving', 'Disprove: A − B = B − A for all sets A, B.',
    ['Try A = {1}, B = ∅.', 'A − B = {{{1}}}, B − A = {{∅}}.', 'They differ, so the statement is {{false}}.'])

u = 'properties-relations-skill-'
N[u + '01'] = R('list relations as sets of ordered pairs and find inverse relations',
    'A relation R from A to B is a subset of A × B; its inverse R⁻¹ reverses every pair: (b, a) ∈ R⁻¹ exactly when (a, b) ∈ R.',
    [['relation', 'A subset of A × B; x R y means (x, y) ∈ R.'], ['inverse relation', 'R⁻¹ = {(y, x) | (x, y) ∈ R}.']],
    'Changing the signs or values of the coordinates instead of swapping them.',
    'Relations', 'A = {1, 2, 3, 4}, a R b iff b = a + 1.',
    ['R = {{{(1, 2), (2, 3), (3, 4)}}}.', 'R⁻¹ = {{{(2, 1), (3, 2), (4, 3)}}}.', 'In words, a R⁻¹ b iff {{b = a − 1}}.'])
N[u + '02'] = R('draw and read directed graphs of relations',
    'In the directed graph of R on A, each element is a vertex and each pair (a, b) ∈ R is an arrow from a to b; (a, a) is a loop.',
    [['directed graph (digraph)', 'Vertices with arrows for ordered pairs.'], ['loop', 'An arrow from a vertex to itself.']],
    'Drawing an arrow in both directions for a single pair.',
    'Digraphs of relations', 'R = {(1, 1), (1, 2), (2, 3), (3, 1)} on {1, 2, 3}.',
    ['Loops: {{1 (at vertex 1)}}.', 'Arrows that are not loops: {{3}}.', 'Is there an arrow 2 → 1? {{No}}.'])
N[u + '03'] = R('decide whether a relation is reflexive, symmetric or transitive',
    'Reflexive: every (a, a) ∈ R. Symmetric: (a, b) ∈ R forces (b, a). Transitive: (a, b) and (b, c) force (a, c). One missing pair is enough to say no.',
    [['reflexive', 'a R a for every a.'], ['symmetric', 'a R b → b R a.'], ['transitive', 'a R b and b R c → a R c.']],
    'Calling a relation transitive because some chains work, or reflexive because some loops are present.',
    'Three properties', 'R = {(1, 1), (2, 2), (1, 2), (2, 3)} on {1, 2, 3}.',
    ['Reflexive? {{No — (3, 3) is missing}}.', 'Symmetric? {{No — (1, 2) without (2, 1)}}.', 'Transitive? {{No — (1, 2), (2, 3) but no (1, 3)}}.'])
N[u + '04'] = R('decide properties of relations on infinite sets with general arguments and counterexamples',
    'On ℤ or ℝ you cannot check pairs one at a time: prove a property with an arbitrary element (e.g. m − m = 0 = 5·0) and disprove it with one counterexample.',
    [['general argument', 'Reasoning about arbitrary elements, valid for all of them.'], ['counterexample', 'Specific elements for which a property fails.']],
    'Declaring a property true on an infinite set after checking a few numbers.',
    'Infinite sets', 'm R n iff 5 | (m − n) on ℤ.',
    ['Reflexive: m − m = {{0 = 5·0}}.', 'Symmetric: m − n = 5k gives n − m = {{5(−k)}}.', 'Transitive: (m − n) + (n − p) = {{m − p}}, a sum of multiples of 5.'])
N[u + '05'] = R('recognize partitions and find the relation a partition induces',
    'A partition splits A into nonempty, non-overlapping blocks that cover A; the induced relation relates two elements exactly when they share a block.',
    [['partition', 'Nonempty, disjoint subsets whose union is A.'], ['block', 'One of the subsets in a partition.'], ['induced relation', 'x R y iff x and y are in the same block.']],
    'Accepting overlapping blocks or forgetting the pairs (a, a) in the induced relation.',
    'Partitions', 'Partition {{1, 2}, {3}} of {1, 2, 3}.',
    ['Is it a partition? {{Yes — disjoint, nonempty, covers A}}.', 'Induced R = {{{(1, 1), (1, 2), (2, 1), (2, 2), (3, 3)}}}.', 'Number of pairs: 2² + 1² = {{5}}.'])
N[u + '06'] = R('decide whether a relation is an equivalence relation',
    'An equivalence relation is reflexive, symmetric and transitive; "has the same ___ as" relations are the typical examples.',
    [['equivalence relation', 'A reflexive, symmetric and transitive relation.'], ['congruence mod n', 'a ≡ b (mod n) when n | (a − b).']],
    'Checking two of the three properties and stopping.',
    'Equivalence relations', 'Is x ≤ y on ℝ an equivalence relation?',
    ['Reflexive: {{yes}}; transitive: {{yes}}.', 'Symmetric: 1 ≤ 2 but {{2 ≰ 1}}.', 'So it is {{not}} an equivalence relation.'])
N[u + '07'] = R('find equivalence classes and the partition they form',
    '[a] = {x | x R a}; the distinct classes partition the set, and congruence mod n has the n classes [0], [1], …, [n − 1].',
    [['equivalence class', '[a], all elements related to a.'], ['representative', 'Any element used to name its class.']],
    'Listing [a] without a itself, or treating [1] and [5] mod 4 as different classes.',
    'Equivalence classes', 'Congruence mod 4 on {0, 1, …, 9}.',
    ['[1] = {{{1, 5, 9}}}.', '[5] = {{[1]}}, the same class.', 'Number of classes: {{4}}.'])

u = 'counting-probability-skill-'
N[u + '01'] = R('describe sample spaces and list events as subsets of the sample space',
    'The sample space lists every possible outcome; an event is a subset of it. Ordered outcomes (first die, second die) keep the outcomes equally likely.',
    [['sample space', 'The set of all possible outcomes.'], ['event', 'A subset of the sample space.'], ['mutually exclusive', 'Events with no outcome in common.']],
    'Listing "one head and one tail" as a single outcome when two coins are tossed.',
    'Sample spaces', 'Toss a coin twice.',
    ['Sample space: {{{HH, HT, TH, TT}}}.', 'Event "exactly one head": {{{HT, TH}}}.', 'Its probability: {{1/2}}.'])
N[u + '02'] = R('count the elements of lists and sublists, including multiples in a range',
    'From m to n inclusive there are n − m + 1 integers; for multiples of d, count the multipliers: ⌊n/d⌋ − ⌊(m − 1)/d⌋.',
    [['list', 'An ordered sequence of objects.'], ['fencepost error', 'Forgetting the + 1 when counting both endpoints.']],
    'Computing n − m and forgetting to include both ends.',
    'Counting a list', 'Seats 101 through 160.',
    ['Count: 160 − 101 + 1 = {{60}}.', 'Even-numbered seats: 102, …, 160 → {{30}}.', 'Multiples of 7: ⌊160/7⌋ − ⌊100/7⌋ = {{8}}.'])
N[u + '03'] = R('draw possibility trees and count outcomes from them',
    'Each path from the root to a leaf is one outcome; stop a branch as soon as the process ends (e.g. a best-of-three match).',
    [['possibility tree', 'A branching diagram of every outcome of a multi-step process.'], ['leaf', 'The end of a branch: one complete outcome.']],
    'Counting branches instead of leaves, or continuing branches after the process has ended.',
    'Possibility trees', 'Best of three (first to win 2).',
    ['Sequences that end in 2 games: {{AA, BB}}.', 'Sequences that need 3 games: {{ABA, ABB, BAA, BAB}}.', 'Total outcomes: {{6}}.'])
N[u + '04'] = R('count with the addition rule and inclusion–exclusion',
    'If cases do not overlap, add; if they do, |A ∪ B| = |A| + |B| − |A ∩ B| (and the three-set version adds back the triple overlap).',
    [['addition rule', '|A ∪ B| = |A| + |B| for disjoint sets.'], ['inclusion–exclusion', '|A ∪ B| = |A| + |B| − |A ∩ B|.']],
    'Adding overlapping counts without subtracting the overlap.',
    'Adding counts', 'Integers 1–120 divisible by 3 or 5.',
    ['By 3: {{40}}; by 5: {{24}}.', 'By both (15): {{8}}.', 'Total: 40 + 24 − 8 = {{56}}.'])
N[u + '05'] = R('count with the multiplication rule',
    'When a process has steps and each step has the same number of choices whatever came before, multiply the numbers of choices.',
    [['multiplication rule', 'm ways then n ways gives mn ways.'], ['with / without repetition', 'Whether a choice can be used again.']],
    'Adding the choices instead of multiplying, or ignoring a restriction such as "first digit not 0".',
    'Multiplying choices', '4-digit PINs with no repeated digit.',
    ['First digit: {{10}} choices; second: {{9}}.', 'Third and fourth: 8 and 7.', 'Total: 10·9·8·7 = {{5040}}.'])
N[u + '06'] = R('choose between permutations and combinations and count systematically',
    'Order matters → permutations P(n, k) = n!/(n − k)!; order does not matter → combinations C(n, k) = P(n, k)/k!.',
    [['permutation', 'An ordered arrangement.'], ['combination', 'An unordered selection.']],
    'Counting teams (unordered) as if they were offices (ordered).',
    'Order or not?', 'A club of 6 chooses people.',
    ['President and vice-president: P(6, 2) = {{30}}.', 'A 2-person team: C(6, 2) = {{15}}.', 'Why half? Each team is counted {{twice}} as officers.'])
N[u + '07'] = R('find probabilities with equally likely outcomes',
    'P(E) = (outcomes in E)/(outcomes in the sample space), valid only when every outcome is equally likely; P(not E) = 1 − P(E).',
    [['equally likely', 'Each outcome has the same probability.'], ['complement', 'E′, the outcomes not in E.']],
    'Treating the sums 2–12 of two dice as equally likely.',
    'Equally likely outcomes', 'Two dice are rolled.',
    ['Outcomes: {{36}} ordered pairs.', 'Sum 8: (2,6), (3,5), (4,4), (5,3), (6,2) → {{5}}.', 'P(sum = 8) = {{5/36}}.'])
N[u + '08'] = R('apply counting rules to compute probabilities',
    'Count the favorable and the total outcomes with the same model (both ordered or both unordered), then divide.',
    [['without replacement', 'An item cannot be drawn again.'], ['counting model', 'The rule (ordered/unordered, with/without repetition) used to count.']],
    'Counting favorable outcomes unordered but total outcomes ordered.',
    'Counting for probability', 'Two cards drawn without replacement.',
    ['Unordered pairs: C(52, 2) = {{1326}}.', 'Pairs of aces: C(4, 2) = {{6}}.', 'P(two aces) = 6/1326 = {{1/221}}.'])

u = 'graphs-trees-skill-'
N[u + '01'] = R('identify vertices, edges, loops and parallel edges and use the handshake theorem',
    'The degree of a vertex counts edge-ends (a loop counts 2); the sum of all degrees is twice the number of edges.',
    [['degree', 'The number of edge-ends at a vertex.'], ['loop', 'An edge from a vertex to itself.'], ['handshake theorem', 'Σ deg(v) = 2|E|.']],
    'Counting a loop as adding 1 to the degree.',
    'Degrees', 'Vertices A, B, C, D; edges AB, AB, BC, loop at C, CD.',
    ['deg(C) = {{4}}.', 'Sum of degrees: {{10}}.', 'Number of edges: 10/2 = {{5}}.'])
N[u + '02'] = R('find in-degrees and out-degrees in directed graphs and choose directed or undirected models',
    'An arrow u → v adds 1 to the out-degree of u and 1 to the in-degree of v, so Σ in-degrees = Σ out-degrees = number of arrows.',
    [['directed graph', 'A graph whose edges are ordered pairs (arrows).'], ['in-degree', 'Arrows coming into a vertex.'], ['out-degree', 'Arrows leaving a vertex.']],
    'Counting every arrow that touches a vertex as out-degree.',
    'Directed graphs', 'Arrows A→B, B→C, A→C, C→A.',
    ['Out-degrees: A {{2}}, B 1, C 1.', 'In-degrees: A 1, B 1, C {{2}}.', 'Both sums equal {{4}}.'])
N[u + '03'] = R('construct graphs with given properties and recognize complete and bipartite graphs',
    'A degree sequence is possible only if its sum is even and no degree exceeds n − 1 (for simple graphs); Kₙ has C(n, 2) edges and K_m,n has mn.',
    [['simple graph', 'No loops and no parallel edges.'], ['complete graph Kₙ', 'Every pair of n vertices joined.'], ['bipartite graph', 'Vertices in two groups, edges only between groups.']],
    'Accepting a degree sequence just because its sum is even.',
    'Building graphs', 'Can a simple graph have degrees 4, 2, 1, 1?',
    ['Sum = {{8}}, even.', 'But 4 vertices allow a maximum degree of {{3}}.', 'So it is {{impossible}}.'])
N[u + '04'] = R('color graphs and find chromatic numbers in scheduling problems',
    'χ(G) is the fewest colors with adjacent vertices different: show a coloring and a reason fewer fail (a triangle needs 3, an odd cycle needs 3, K₄ needs 4).',
    [['proper coloring', 'Adjacent vertices get different colors.'], ['chromatic number', 'χ(G), the fewest colors needed.']],
    'Giving a coloring without showing that fewer colors cannot work.',
    'Coloring', 'The 5-cycle A–B–C–D–E–A.',
    ['Two colors alternate A, B, C, D, but E touches A and D, which {{differ}}.', 'So χ ≥ {{3}}.', 'A coloring with 3 exists, so χ = {{3}}.'])
N[u + '05'] = R('classify walks, trails and paths and find Euler trails',
    'A trail repeats no edge, a path repeats no vertex; a connected graph has an Euler trail (not closed) exactly when it has 2 odd vertices, starting at one and ending at the other.',
    [['walk / trail / path', 'Any route / no repeated edge / no repeated vertex.'], ['Euler trail', 'A trail using every edge exactly once.']],
    'Starting an Euler trail at an even vertex when there are two odd ones.',
    'Trails and paths', 'Degrees 2, 2, 3, 3, 4 (connected).',
    ['Odd vertices: {{2}}.', 'So there is an {{Euler trail}} but no Euler circuit.', 'It must start and end at {{the two odd vertices}}.'])
N[u + '06'] = R('find Euler circuits and Hamiltonian cycles',
    'A connected graph has an Euler circuit exactly when every degree is even; Hamiltonian cycles (every vertex once) have no simple test, so build one or find an obstacle.',
    [['Euler circuit', 'A closed trail using every edge once.'], ['Hamiltonian cycle', 'A cycle through every vertex exactly once.']],
    'Confusing "every edge once" (Euler) with "every vertex once" (Hamilton).',
    'Circuits', 'K₄.',
    ['Each degree is {{3}}, odd, so there is {{no}} Euler circuit.', 'A–B–C–D–A is a {{Hamiltonian cycle}}.', 'Edges in it: {{4}}.'])
N[u + '07'] = R('characterize trees and find minimum spanning trees',
    'A tree is connected with no cycles; with n vertices it has exactly n − 1 edges. Kruskal\'s algorithm adds the cheapest edge that does not form a cycle.',
    [['tree', 'A connected graph with no cycles.'], ['leaf', 'A vertex of degree 1.'], ['spanning tree', 'A tree containing every vertex of the graph.']],
    'Taking the cheapest edges even when one closes a cycle.',
    'Trees', 'Kruskal on AB 1, AC 1, BC 2, CD 3.',
    ['Take AB 1 and {{AC 1}}.', 'Skip BC 2: it would make a {{cycle}}.', 'Take CD 3; total weight {{5}}.'])

u = 'election-theory-skill-'
N[u + '01'] = R('read preference schedules and count voters, first-place votes and majorities',
    'A preference schedule groups identical ballots; a majority is more than half of the votes, while plurality only needs the most.',
    [['preference ballot', 'A voter\'s ranking of all the candidates.'], ['preference schedule', 'A table of how many voters cast each ranking.'], ['majority', 'More than half of the votes.']],
    'Calling half of the votes a majority.',
    'Preference schedules', '5: A > B > C; 4: B > C > A; 2: C > A > B.',
    ['Voters: {{11}}; a majority is {{6}}.', 'First-place votes: A {{5}}, B 4, C 2.', 'Voters preferring A to B: 5 + 2 = {{7}}.'])
N[u + '02'] = R('find winners by plurality, Borda count, instant runoff and pairwise comparisons',
    'Plurality: most first places. Borda: n points down to 1. Instant runoff: eliminate the last-place candidate until someone has a majority. Pairwise: 1 point per head-to-head win.',
    [['Borda count', 'Points by rank: n for first, …, 1 for last.'], ['instant runoff', 'Plurality with elimination.'], ['pairwise comparison', 'A head-to-head contest between two candidates.']],
    'Using only first-place votes in a Borda count.',
    'Voting methods', 'Same schedule: 5 A>B>C, 4 B>C>A, 2 C>A>B.',
    ['Plurality winner: {{A}}.', 'Borda: A 23, B {{24}}, C 19.', 'Different methods can give {{different winners}}.'])
N[u + '03'] = R('check election results against fairness criteria',
    'Majority: a majority candidate should win. Condorcet: a candidate who beats every other head-to-head should win. Monotonicity and independence of irrelevant alternatives are further tests.',
    [['majority criterion', 'A first-place majority candidate should win.'], ['Condorcet criterion', 'A candidate who wins every pairwise comparison should win.'], ['monotonicity', 'Gaining support should never make a winner lose.']],
    'Thinking the plurality winner must be the Condorcet winner.',
    'Fairness criteria', '4: A>B>C; 3: B>C>A; 2: C>B>A.',
    ['Plurality winner: {{A}}.', 'B beats A {{5–4}} and C 7–2.', 'So plurality {{violates the Condorcet criterion}} here.'])
N[u + '04'] = R('analyze weighted voting systems: quotas, dictators, veto power and dummies',
    'In [q: w₁, …, wₙ] a coalition wins when its weight reaches q (more than half the total, at most the total). A dictator wins alone; a veto player is in every winning coalition; a dummy is never critical.',
    [['quota', 'The weight needed to pass a motion.'], ['veto power', 'The others together cannot reach the quota.'], ['dummy', 'A player who is never critical.']],
    'Assuming the heaviest player is a dictator or has veto power.',
    'Weighted voting', '[7: 5, 3, 1].',
    ['Dictator? {{No}} (5 < 7).', 'Veto: P1 (others 4 < 7) and {{P2}} (others 6 < 7).', 'P3 is a {{dummy}}.'])
N[u + '05'] = R('measure voting power with the Banzhaf and Shapley–Shubik indices',
    'Banzhaf: count how often each player is critical in a winning coalition and divide by the total. Shapley–Shubik: count how often each player is pivotal in the n! orderings.',
    [['critical player', 'A member whose removal makes a winning coalition lose.'], ['Banzhaf index', 'A player\'s share of all critical counts.'], ['pivotal player', 'The player whose vote first reaches the quota in an ordering.']],
    'Using the weights themselves as a measure of power.',
    'Voting power', '[6: 4, 3, 2].',
    ['Winning coalitions: {P1, P2}, {P1, P3}, {{{P1, P2, P3}}}.', 'Critical counts: P1 {{3}}, P2 1, P3 1.', 'Banzhaf index of P1: {{3/5}}.'])
N[u + '06'] = R('divide goods fairly with divider–chooser, sealed bids and markers',
    'Divider–chooser gives each of two players at least half by their own values. Sealed bids: each item goes to the highest bidder, everyone is owed a fair share of their own bids, and the surplus is split equally.',
    [['fair share', 'At least 1/n of the total by a player\'s own values.'], ['sealed bids', 'A discrete method using bids and cash settlements.'], ['surplus', 'Cash left after the first settlement, shared equally.']],
    'Letting the divider choose first, or giving an item to the lowest bidder.',
    'Fair division', 'Kim bids $80 and Lee $60 on one bike.',
    ['Kim gets the bike; fair shares: Kim $40, Lee {{$30}}.', 'Kim pays Lee $30; surplus = 40 − 30 = {{$10}}.', 'Each gets half the surplus, so Kim pays Lee {{$35}} in all.'])
N[u + '07'] = R('apportion seats with Hamilton\'s, Jefferson\'s, Webster\'s and Adams\'s methods',
    'Standard divisor = population ÷ seats; Hamilton floors the quotas and gives leftover seats by largest remainder; divisor methods find a modified divisor so the rounded quotas (down, nearest or up) add to the seats.',
    [['standard quota', 'A state\'s population ÷ the standard divisor.'], ['modified divisor', 'A divisor chosen so rounded quotas add to the seats.'], ['quota rule', 'Each state gets its lower or upper quota.']],
    'Rounding every quota normally in Hamilton\'s method, so the total is wrong.',
    'Apportionment', 'Populations 450, 330, 220; 10 seats.',
    ['Standard divisor: {{100}}.', 'Quotas 4.5, 3.3, 2.2 → floors 4, 3, 2 = {{9}}.', 'Largest remainder gets the last seat: {{5, 3, 2}}.'])
N[u + '08'] = R('compare methods for fairness and recognize apportionment paradoxes',
    'No voting method satisfies every fairness criterion (Arrow); Hamilton\'s method can show the Alabama, population and new-states paradoxes, and divisor methods can violate the quota rule.',
    [['Alabama paradox', 'More seats in total make a state lose a seat.'], ['population paradox', 'A faster-growing state loses a seat to a slower one.'], ['Arrow\'s theorem', 'No ranked method meets all fairness criteria.']],
    'Mixing up the Alabama paradox (seats change) with the population paradox (populations change).',
    'Comparing methods', 'Hamilton with 13 and 14 seats.',
    ['Populations 130, 690, 410 with 13 seats: {{2, 7, 4}}.', 'With 14 seats: {{1, 8, 5}}.', 'A lost a seat: the {{Alabama paradox}}.'])

u = 'linear-programming-skill-'
N[u + '01'] = R('write constraints and an objective from a real-world situation',
    'Name the variables, then turn each limited resource into "amount per unit × units ≤ available" (≥ for minimums) and add x ≥ 0, y ≥ 0.',
    [['decision variable', 'A quantity you choose, such as x items.'], ['constraint', 'An inequality every plan must satisfy.'], ['nonnegativity', 'x ≥ 0 and y ≥ 0.']],
    'Writing ≥ for "at most", or reversing the variables in a ratio constraint.',
    'Modeling', 'Shirts (x) cost $8, hats (y) $5; spend at most $100.',
    ['Constraint: {{8x + 5y ≤ 100}}.', 'Also x ≥ 0 and {{y ≥ 0}}.', '"At least 10 items": {{x + y ≥ 10}}.'])
N[u + '02'] = R('graph systems of linear inequalities and test points',
    'Graph each boundary line (solid for ≤ or ≥, dashed for < or >), shade the side a test point satisfies, and keep the overlap of all the shaded half-planes.',
    [['half-plane', 'All points on one side of a line.'], ['boundary line', 'Where the two sides of the inequality are equal.'], ['test point', 'A point used to decide which side to shade.']],
    'Checking a point against one inequality and not the whole system.',
    'Graphing a system', 'x + y ≤ 6, x ≥ 0, y ≥ 0.',
    ['Boundary x + y = 6 is {{solid}}.', '(0, 0) gives 0 ≤ 6, so shade the side {{containing the origin}}.', 'Is (4, 3) a solution? {{No — 7 > 6}}.'])
N[u + '03'] = R('find and describe feasible regions and their corner points',
    'The feasible region is the overlap of all the constraints; its corners are intersections of boundary lines that satisfy every constraint. It can be bounded, unbounded or empty.',
    [['feasible region', 'All points satisfying every constraint.'], ['corner point (vertex)', 'Where two boundary lines meet on the region.'], ['bounded', 'Enclosable in a circle.']],
    'Listing an intersection point that breaks another constraint.',
    'Feasible regions', 'x + y ≤ 8, x ≤ 5, x ≥ 0, y ≥ 0.',
    ['Corners: (0, 0), (0, 8), (5, 0) and {{(5, 3)}}.', 'Is (6, 0) a corner? {{No — it breaks x ≤ 5}}.', 'The region is {{bounded}}.'])
N[u + '04'] = R('write and evaluate objective functions and read level lines',
    'The objective P = ax + by measures what you maximize or minimize; each value k gives a level line ax + by = k, and larger k moves the line away from the origin (for positive a, b).',
    [['objective function', 'The quantity to maximize or minimize.'], ['level line', 'All points where the objective has the same value.']],
    'Writing revenue instead of profit (forgetting to subtract costs).',
    'Objective functions', 'Profit $5 per muffin (x) and $3 per scone (y).',
    ['P = {{5x + 3y}}.', 'At (4, 6): P = 20 + 18 = {{38}}.', 'Level lines have slope {{−5/3}}.'])
N[u + '05'] = R('find corner points by solving boundary equations and list candidate solutions',
    'Each corner is the solution of two boundary equations; solve by substitution or elimination and keep only intersections that satisfy all constraints.',
    [['candidate solution', 'A corner point to test in the objective.'], ['elimination', 'Adding multiples of equations to remove a variable.']],
    'Guessing a corner from the graph instead of solving the two equations.',
    'Finding corners', '2x + y = 10 and x + 2y = 8.',
    ['Double the second: 2x + 4y = 16; subtract: 3y = {{6}}, so y = 2.', 'Then x = {{4}}.', 'Corner: {{(4, 2)}}.'])
N[u + '06'] = R('maximize or minimize an objective with the corner-point method and recognize special cases',
    'On a bounded feasible region the optimum is at a corner: evaluate the objective at every corner. Ties along an edge mean infinitely many optima; an unbounded region may have no maximum; an empty region has no solution.',
    [['corner-point principle', 'An optimum on a bounded region occurs at a corner.'], ['multiple optima', 'Two adjacent corners tie, so the whole edge is optimal.'], ['infeasible', 'No point satisfies all constraints.']],
    'Picking the corner with the largest coordinates instead of evaluating the objective.',
    'Optimizing', 'Maximize P = 3x + 2y on x + y ≤ 8, x ≤ 5, x, y ≥ 0.',
    ['P at (0, 0), (0, 8), (5, 0), (5, 3): 0, 16, 15, {{21}}.', 'Maximum: {{21 at (5, 3)}}.', 'Minimum on the region: {{0 at (0, 0)}}.'])
N[u + '07'] = R('interpret optimal solutions, binding constraints and slack in context',
    'State the optimum in the situation\'s words and units; a binding constraint is used exactly (slack 0), and slack is the unused amount of a resource.',
    [['binding constraint', 'A constraint that holds with equality at the optimum.'], ['slack', 'Limit minus amount used.'], ['integer solution', 'A solution in whole numbers when items cannot be split.']],
    'Rounding a fractional optimum up without checking the constraints.',
    'Interpreting', 'Optimum (10, 10): 10 bracelets, 10 keychains; beads 2x + y ≤ 30.',
    ['Beads used: 2·10 + 10 = {{30}}.', 'Slack: {{0}}, so beads are {{binding}}.', 'Profit 4·10 + 3·10 = {{$70}}.'])

if __name__ == '__main__':
    out = ['/* Teaching notes for the Discrete Math lesson planner (see notes-teach.js for the format).',
           '   Generated by tools/discrete-audit-20261118/notes.py (Discrete Math audit #5, 2026-11-18); edit that file, then rerun.',
           '   Records are keyed by catalog skill id: obj (objective), idea (key idea), voc (vocabulary with meanings),',
           '   watch (common mistake) and cards (the explanation cards). */',
           '(function (G) {', "  'use strict';", '  var T = (G.MKPLAN_TEACH = G.MKPLAN_TEACH || {}), N = T.discrete = T.discrete || {};']
    unit = None
    for k in sorted(N, key=lambda s: (s.rsplit('-skill-', 1)[0], s)):
        un = k.rsplit('-skill-', 1)[0]
        if un != unit:
            out.append(f'  /* ---------- {un} ---------- */'); unit = un
        out.append(f'  N[{json.dumps(k)}] = {json.dumps(N[k], ensure_ascii=False)};')
    out.append("})(typeof window !== 'undefined' ? window : globalThis);")
    open(os.path.join(ROOT, 'worksheet-generator/planner/notes-teach-discrete.js'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print(len(N), 'records')
