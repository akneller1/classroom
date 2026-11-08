# Source of manifest.json for the Discrete Math Interactive Math tools. Run inside this folder: python3 manifest_src.py
# The Linear Programming unit reuses the existing Algebra 2 Feasible Region Optimizer (listed in data.js, not rebuilt here).
import json
T = []
def tool(slug, unit, unitName, title, intro, description, topics, discovery):
    T.append(dict(slug=slug, course='discrete', unit=unit, unitName=unitName, title=title, intro=intro, description=description, topics=topics, discovery=discovery))

tool('discrete-truth-table-lab', 'compound-statements-logic', 'The Logic of Compound Statements', 'Truth Table Lab',
     'Type a compound statement and watch its truth table build itself. Compare two statements row by row, generate the converse, inverse and contrapositive, and test whether an argument form is valid.',
     'Type statements with ~, ∧, ∨, ⊕, → and ↔ and see a full truth table with every intermediate column. Compare two statements for logical equivalence, make the converse, inverse, contrapositive and negation of a conditional, and test argument forms using critical rows.',
     ['Truth tables', 'Logical equivalence', 'Conditional statements', 'Valid and invalid arguments'],
     'Two statements are equivalent exactly when their truth-table columns agree in every row; a conditional is equivalent to its contrapositive but not to its converse or inverse; an argument form is valid exactly when the conclusion is true in every critical row.')
tool('discrete-euclid-explorer', 'number-theory-proof', 'Elementary Number Theory and Methods of Proof', 'Euclidean Algorithm Explorer',
     'Pick two whole numbers and cut their rectangle into the largest possible squares. Each cut is one step of the Euclidean algorithm, and the last square size is the GCD.',
     'See the Euclidean algorithm as square tiling of an a × b rectangle, step through a = bq + r, back-substitute to write gcd(a, b) as a linear combination, compare prime factorizations, and explore the quotient-remainder theorem for negative numbers.',
     ['Greatest common divisor', 'Euclidean algorithm', 'Quotient-remainder theorem', 'Prime factorization'],
     'gcd(a, b) = gcd(b, r) where r is the remainder of a ÷ b, so repeated division shrinks the problem until the remainder is 0; the last nonzero remainder is the GCD, it can be written as sa + tb, and gcd · lcm = ab.')
tool('discrete-recursion-explorer', 'sequences-induction-recursion', 'Sequences, Mathematical Induction, and Recursion', 'Recursion & Closed Form Explorer',
     'Build a sequence from a recurrence relation and initial terms, watch the terms and partial sums grow, then type a closed-form guess and test it against the terms.',
     'Set first-order (aₙ = c·aₙ₋₁ + d) or second-order (aₙ = c·aₙ₋₁ + d·aₙ₋₂) recurrences with any initial terms. See the terms, partial sums and a graph, recognize arithmetic and geometric sequences, and check a closed-form guess against the first 15 terms before proving it by induction.',
     ['Recurrence relations', 'Arithmetic and geometric sequences', 'Closed formulas', 'Mathematical induction'],
     'A recurrence plus initial terms determines every term; c = 1 gives an arithmetic sequence and d = 0 a geometric one; a closed form that matches many terms is only a conjecture until an induction proof shows the recurrence carries it from n to n + 1.')
tool('discrete-venn-explorer', 'set-theory', 'Set Theory', 'Venn Diagram & Membership Table Explorer',
     'Type set expressions with ∪, ∩, −, ⊕ and complements, see the regions they shade, and compare two expressions with a membership table. Shade regions yourself and check your work.',
     'Two- or three-set Venn diagrams inside a stated universe U = {1, …, 20}. Shade any set expression, compare two expressions region by region (a membership table), click or tab through regions to shade your own answer, and list the actual elements of the result.',
     ['Set operations', 'Venn diagrams', 'Set identities', 'Membership tables'],
     'Every set expression in A, B, C is determined by which of the 2ⁿ regions it contains, so two expressions are equal exactly when their membership-table columns agree; complements are always taken relative to the universe U.')
tool('discrete-relation-explorer', 'properties-relations', 'Properties of Relations', 'Relation Property Explorer',
     'Build a relation by clicking cells of its matrix or arrows of its directed graph. The tool tests reflexive, symmetric, antisymmetric and transitive live and shows a counterexample when one fails.',
     'Toggle ordered pairs on a set of 3 to 6 elements using the relation matrix or the directed graph. See which properties hold with a witness for each failure, form reflexive, symmetric and transitive closures and the inverse, and see the equivalence classes whenever the relation is an equivalence relation.',
     ['Reflexive, symmetric, transitive', 'Directed graphs of relations', 'Equivalence relations and classes', 'Closures'],
     'Each property can be read off the digraph (loops everywhere, arrows in pairs, every two-step path has a shortcut) and one failing pair disproves it; an equivalence relation splits the set into disjoint classes that form a partition.')
tool('discrete-counting-explorer', 'counting-probability', 'Counting and Probability', 'Counting Outcomes Explorer',
     'Choose how many items, how many to select, whether order matters and whether repetition is allowed. See the formula, the count and the actual list of outcomes, then find probabilities by counting.',
     'List every outcome for selections of r items from n letters under all four counting models (ordered or not, with or without repetition). Group permutations into combinations to see why P(n, r) = C(n, r) · r!, and compute equally likely probabilities for events like “contains A”.',
     ['Multiplication rule', 'Permutations', 'Combinations', 'Equally likely probability'],
     'n^r, P(n, r), C(n, r) and C(n + r − 1, r) count the four models; each combination corresponds to r! orderings; probability as favorable/total requires outcomes that are equally likely, which multisets are not.')
tool('discrete-graph-lab', 'graphs-trees', 'Theory of Graphs and Trees', 'Graph Explorer: Euler, Hamilton & Trees',
     'Build a graph by clicking (or with the edge form), or start from a classic example. The tool reports degrees, connectivity, Euler trails and circuits, Hamiltonian cycles, trees and colorings, and steps through Kruskal’s algorithm.',
     'Add vertices, edges, loops and parallel edges by pointer or keyboard. See the degree sum, components, Euler circuit or trail (with a route), whether a Hamiltonian cycle exists (by exhaustive search on up to 10 vertices), whether the graph is a tree or bipartite, its chromatic number with a coloring, and a step-by-step minimum spanning tree.',
     ['Degree and the handshake theorem', 'Euler and Hamiltonian circuits', 'Trees and spanning trees', 'Graph coloring'],
     'A connected graph has an Euler circuit exactly when every degree is even and an Euler trail exactly when exactly two degrees are odd; no simple degree test decides Hamiltonian cycles; a connected graph is a tree exactly when it has n − 1 edges; Kruskal builds a minimum spanning tree by skipping cycle-forming edges.')
tool('discrete-voting-explorer', 'election-theory', 'Election Theory', 'Voting, Power & Apportionment Explorer',
     'Edit a preference schedule and compare four named voting methods, measure power in a weighted voting system, and apportion seats with Hamilton, Jefferson, Webster and Adams.',
     'Ranked ballots: plurality, Borda count, plurality with elimination and pairwise comparisons side by side, with majority and Condorcet checks and stated tie rules. Weighted voting: winning coalitions, critical players, Banzhaf and Shapley–Shubik indices, dictators, veto power and dummies. Apportionment: quotas, modified divisors, the quota rule and the Alabama paradox.',
     ['Voting methods', 'Fairness criteria', 'Weighted voting and power', 'Apportionment'],
     'Different reasonable voting methods can pick different winners from the same ballots; voting power depends on critical appearances, not weight; Hamilton always satisfies the quota rule but can show the Alabama paradox, while divisor methods avoid that paradox but can violate quota.')
json.dump({'version': '20261109', 'labVersion': '20261105', 'tools': T}, open('manifest.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(len(T), 'tools')
