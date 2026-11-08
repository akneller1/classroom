"""Unit 8: Theory of Graphs and Trees (7 skills). Course definitions (stated in prompts where they matter):
walk = alternating sequence of vertices and edges; trail = walk with no repeated edge; path = walk with no repeated vertex;
circuit = closed walk with at least one edge and no repeated edge; cycle (simple circuit) = circuit with no repeated vertex except
the first/last. Graphs are undirected unless stated; loops and parallel edges are allowed only when stated. A loop adds 2 to the degree."""
import itertools, math
import networkx as nx
from core import Bank, fmt_set, seeded
import figs

U = 'graphs-trees'
DEF = 'Definitions: a trail repeats no edge; a path repeats no vertex; a circuit is a closed trail; an Euler circuit uses every edge exactly once.'


def build():
    b = Bank(U, 'gr', 7)
    for f in (s1, s2, s3, s4, s5, s6, s7, topup, errors):
        f(b)
    return b


def num_mc(b, k, L, prompt, ans, wr, steps, fam):
    ws = [str(w) for w in dict.fromkeys(wr) if str(w) != str(ans)]
    return b.mc(k, L, prompt, str(ans), ws[:3], steps, fam, order='sort')


def degrees(V, E):
    d = {v: 0 for v in V}
    for u, w in E:
        d[u] += 1
        d[w] += 1
    return d


def connected(V, E):
    G = nx.MultiGraph(); G.add_nodes_from(V); G.add_edges_from(E)
    return nx.is_connected(G)


def euler_kind(V, E):
    d = degrees(V, E)
    odd = [v for v in V if d[v] % 2]
    nonisolated = [v for v in V if d[v] > 0]
    G = nx.MultiGraph(); G.add_nodes_from(nonisolated); G.add_edges_from(E)
    if not nx.is_connected(G):
        return 'none', odd
    return ('circuit' if not odd else 'trail' if len(odd) == 2 else 'none'), odd


def chromatic(V, E):
    simple = {tuple(sorted(e)) for e in E if e[0] != e[1]}
    for k in range(1, len(V) + 1):
        for col in itertools.product(range(k), repeat=len(V)):
            c = dict(zip(V, col))
            if all(c[u] != c[w] for u, w in simple):
                return k


def ham_circuit(V, E):
    S = {frozenset(e) for e in E if e[0] != e[1]}
    first = V[0]
    for p in itertools.permutations(V[1:]):
        cyc = (first,) + p + (first,)
        if all(frozenset((cyc[i], cyc[i + 1])) in S for i in range(len(V))):
            return cyc
    return None


POS5 = {'A': (0, 1), 'B': (0.95, 0.31), 'C': (0.59, -0.81), 'D': (-0.59, -0.81), 'E': (-0.95, 0.31)}
POS4 = {'A': (-1, 1), 'B': (1, 1), 'C': (1, -1), 'D': (-1, -1)}
POS6 = {'A': (-1.2, 0.8), 'B': (0, 1.1), 'C': (1.2, 0.8), 'D': (1.2, -0.8), 'E': (0, -1.1), 'F': (-1.2, -0.8)}
GRAPHS = {
    'g1': (list('ABCD'), [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'), ('A', 'C')], POS4),
    'g2': (list('ABCD'), [('A', 'B'), ('A', 'B'), ('B', 'C'), ('C', 'C'), ('C', 'D')], POS4),
    'g3': (list('ABCDE'), [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A'), ('A', 'C'), ('A', 'D')], POS5),
    'g4': (list('ABCDE'), [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A'), ('A', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'A'), ('E', 'B')], POS5),
    'g5': (list('ABCDEF'), [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('F', 'A'), ('B', 'E')], POS6),
    'g6': (list('ABCDEF'), [('A', 'B'), ('A', 'F'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F'), ('A', 'D'), ('B', 'E'), ('C', 'F')], POS6),
    'g7': (list('ABCD'), [('A', 'B'), ('A', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'D'), ('A', 'D'), ('A', 'D')], POS4),
    'g8': (list('ABCDE'), [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A')], POS5),
    't1': (list('ABCDEF'), [('A', 'B'), ('A', 'C'), ('C', 'D'), ('C', 'E'), ('E', 'F')], POS6),
}


def pic(key, **kw):
    V, E, pos = GRAPHS[key]
    return figs.graph(U, key + kw.pop('suffix', ''), V, E, pos=pos, **kw)


def alt(key):
    V, E, _ = GRAPHS[key]
    return 'Undirected graph with vertices %s and edges %s.' % (', '.join(V), ', '.join(('loop at %s' % u) if u == w else u + w for u, w in E))


# ---------------------------------------------------------------- 1. vertices, edges, endpoints, loops
def s1(b):
    for L, key, v in (('cp2', 'g1', 'A'), ('cp2', 'g8', 'C'), ('cp1', 'g2', 'C'), ('cp1', 'g3', 'A'), ('honors', 'g7', 'A'), ('honors', 'g2', 'B')):
        V, E, _ = GRAPHS[key]
        d = degrees(V, E)[v]
        r = num_mc(b, 1, L, 'Find the degree of vertex %s in the graph shown (a loop adds 2 to the degree; parallel edges each count).' % v, d, [d - 1, d + 1, d * 2],
                   ['Count edge-ends at %s.' % v, 'deg(%s) = %d' % (v, d)], 'degree')
        b.image(r, pic(key), alt(key))
    for L, key in (('cp2', 'g8'), ('cp1', 'g3'), ('honors', 'g2')):
        V, E, _ = GRAPHS[key]
        tot = sum(degrees(V, E).values())
        r = b.sa(1, L, 'Find the SUM of the degrees of all vertices in the graph shown.', tot, ['Handshake theorem: the degree sum is 2·(number of edges).', '2·%d = %d' % (len(E), tot)], 'degree_sum')
        b.image(r, pic(key), alt(key))
    HS = [('cp2', 'A graph has 9 edges. What is the sum of the degrees?', 18), ('cp1', 'A graph has degrees 3, 3, 2, 2, 2. How many edges does it have?', 6),
          ('honors', 'A graph has 8 vertices, each of degree 3. How many edges?', 12), ('honors', 'Can a graph have exactly 5 vertices of odd degree? Answer 0 for no, 1 for yes.', 0)]
    for L, t, v in HS:
        b.sa(1, L, t, v, ['Handshake theorem: Σ deg(v) = 2|E|, so the number of odd-degree vertices is even.', 'Answer: %d' % v], 'handshake')
    b.sel(1, 'cp2', 'A graph has vertices A, B, C, D and edges AB, AB (two parallel edges), BC, a loop at C, and CD. Which statements are true?',
          [('There is a loop at C', True), ('A and B are joined by parallel edges', True), ('D has degree 1', True), ('C has degree 3', False), ('The graph has 4 edges', False)],
          ['Degrees: A 2, B 3, C 4 (loop counts 2), D 1; there are 5 edges.'], 'graph_terms_select')
    b.sel(1, 'cp1', 'Which degree lists are possible for an undirected graph (loops and parallel edges allowed)?', [('2, 2, 2', True), ('3, 3, 1, 1', True), ('4, 1, 1', True), ('3, 2, 2', False), ('1, 1, 1', False)],
          ['A list is possible exactly when its sum is even (with loops and parallel edges allowed).'], 'graph_terms_select')
    b.sel(1, 'honors', 'For every graph G, which statements are true?', [('The number of odd-degree vertices is even', True), ('Σ deg(v) is even', True), ('|E| = Σ deg(v) / 2', True), ('Every vertex has positive degree', False), ('Σ deg(v) = |E|', False)],
          ['Handshake theorem and its corollary; isolated vertices have degree 0.'], 'graph_terms_select')
    b.orq(1, 'cp2', 'Graph: vertices P, Q, R, S; edges PQ, QR, RS, SP, QS.',
          [('Find each degree.', 'P 2, Q 3, R 2, S 3'), ('Find the degree sum.', '10'), ('How many edges?', '5'), ('Check the handshake theorem.', '10 = 2·5')],
          ['Count edge-ends.', 'Add.', 'Count edges.', 'Σ deg = 2|E|.'], 'degree_or')
    b.orq(1, 'cp1', 'A graph has 6 vertices with degrees 1, 2, 2, 3, 3, x.',
          [('What must be true about the degree sum?', 'It must be even.'), ('Which values of x from 0 to 5 are possible by that rule?', '1, 3, 5'), ('If x = 3, how many edges?', '7'), ('If the graph is simple, can x = 6? Explain.', 'No; in a simple graph with 6 vertices, max degree is 5.')],
          ['Handshake.', '11 + x even.', '14/2.', 'Only 5 other vertices.'], 'degree_or')
    b.orq(1, 'honors', 'At a party, people shake hands (each pair at most once).',
          [('Model this as a graph.', 'Vertices = people, edges = handshakes (a simple graph).'), ('If 10 people each shake 3 hands, how many handshakes?', '15'),
           ('Can 9 people each shake exactly 3 hands? Explain.', 'No; the degree sum 27 would be odd.'), ('What is the maximum number of handshakes among 10 people?', '45')],
          ['Simple graph.', '30/2.', 'Handshake theorem.', 'C(10, 2).'], 'degree_or')


# ---------------------------------------------------------------- 2. directed vs undirected
DG = (list('ABCD'), [('A', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'D'), ('D', 'D'), ('A', 'D')])


def s2(b):
    V, E = DG
    p = figs.graph(U, 'digraph1', V, E, pos=POS4, directed=True)
    a_ = 'Directed graph with arrows A→B, B→C, C→A, C→D, A→D and a loop at D.'
    indeg = {v: sum(1 for x in E if x[1] == v) for v in V}
    outdeg = {v: sum(1 for x in E if x[0] == v) for v in V}
    for L, t, v in (('cp2', 'What is the out-degree of A?', outdeg['A']), ('cp2', 'What is the in-degree of D? (A loop counts once toward in-degree and once toward out-degree.)', indeg['D']),
                    ('cp1', 'What is the sum of all in-degrees?', sum(indeg.values())), ('cp1', 'Which vertex has the largest in-degree? (Answer with a letter.)', max(V, key=lambda x: indeg[x])),
                    ('honors', 'How many vertices have in-degree equal to out-degree?', sum(1 for x in V if indeg[x] == outdeg[x]))):
        r = b.sa(2, L, 'Use the directed graph shown. ' + t, v, ['In-degree counts arrows coming in; out-degree counts arrows going out.', 'In: %s; out: %s.' % (indeg, outdeg)], 'in_out_degree')
        b.image(r, p, a_)
    UD = [('cp2', 'Friendship on a social network where friendship is mutual', 'Undirected'), ('cp2', 'One-way streets in a town', 'Directed'),
          ('cp1', '"Follows" on a platform where you can follow someone who does not follow you', 'Directed'), ('cp1', 'Roads between towns that can be driven both ways', 'Undirected'),
          ('honors', 'Prerequisites between courses', 'Directed'), ('honors', 'Pairs of countries sharing a border', 'Undirected')]
    for L, t, a in UD:
        b.mc(2, L, 'Which kind of graph models this situation best? %s' % t, a, ['Directed' if a == 'Undirected' else 'Undirected', 'Neither: it needs a tree', 'Both, with loops required'],
             ['Use directed edges when the relationship has a direction (A to B need not mean B to A).', a], 'directed_choice')
    b.sel(2, 'cp1', 'In ANY directed graph, which statements are true?', [('Σ in-degrees = number of edges', True), ('Σ out-degrees = number of edges', True), ('Σ in-degrees = Σ out-degrees', True), ('Every vertex has in-degree = out-degree', False), ('Σ in-degrees = 2·edges', False)],
          ['Each arrow has one tail and one head.'], 'directed_select')
    b.sel(2, 'cp2', 'Which features belong to a DIRECTED graph?', [('Edges have arrows', True), ('Each edge has a start and an end', True), ('(A, B) and (B, A) can be different edges', True), ('Edges never have a direction', False), ('It cannot have loops', False)],
          ['Directed edges are ordered pairs; loops are allowed.'], 'directed_select')
    b.sel(2, 'honors', 'Directed graph with arrows A→B, B→C, C→A, C→D, A→D and a loop at D. Which statements are true?', [('There is a directed path from A to C', True), ('There is no directed path from D to A', True), ('A→B→C→A is a directed cycle', True), ('There is a directed path from D to B', False), ('Every vertex can reach every other vertex', False)],
          ['D has only its loop going out, so nothing else is reachable from D.'], 'directed_select')
    b.orq(2, 'cp2', 'Directed graph: A→B, B→C, A→C, C→A.',
          [('Find the out-degree of each vertex.', 'A 2, B 1, C 1'), ('Find the in-degree of each vertex.', 'A 1, B 1, C 2'), ('Check Σ in = Σ out = edges.', '4 = 4 = 4'), ('Is there a directed path from B to A?', 'Yes: B→C→A')],
          ['Tails.', 'Heads.', 'Each edge counted once.', 'Follow arrows.'], 'directed_or')
    b.orq(2, 'cp1', 'A tournament: 4 teams play each other once; draw an arrow from winner to loser.',
          [('How many arrows are there?', '6'), ('What is the sum of the out-degrees?', '6'), ('If one team beats everyone, what is its out-degree?', '3'), ('Can two teams both have out-degree 3? Explain.', 'No; they played each other, so one of them lost.')],
          ['C(4, 2).', 'One win per game.', 'Beats 3 teams.', 'Each game has one winner.'], 'directed_or')
    b.orq(2, 'honors', 'A directed graph models web links among pages P1, ..., P5.',
          [('What does in-degree measure?', 'How many pages link TO the page.'), ('If there are 12 links, find Σ out-degrees.', '12'), ('Can every page have out-degree 5 if self-links are not allowed? Explain.', 'No; the most is 4 other pages.'),
           ('Explain why an undirected graph would lose information here.', 'A link from P1 to P2 does not imply a link from P2 to P1.')],
          ['Incoming links.', 'Each link has one tail.', 'Simple digraph.', 'Direction matters.'], 'directed_or')


# ---------------------------------------------------------------- 3. constructing graphs
def graphical(seq):
    s = sorted(seq, reverse=True)
    while s and s[0] > 0:
        d = s.pop(0)
        if d > len(s):
            return False
        for i in range(d):
            s[i] -= 1
            if s[i] < 0:
                return False
        s.sort(reverse=True)
    return all(x == 0 for x in s)


def s3(b):
    SEQ = [('cp2', [2, 2, 2]), ('cp2', [3, 1, 1, 1]), ('cp2', [1, 1, 1]), ('cp1', [3, 3, 3, 3]), ('cp1', [4, 2, 1, 1]), ('cp1', [3, 3, 2, 2, 2]),
           ('honors', [4, 4, 4, 1, 1]), ('honors', [3, 3, 3, 3, 3, 3]), ('honors', [5, 3, 3, 3, 3, 3])]
    for L, s in SEQ:
        g = graphical(s)
        reason = 'Yes' if g else ('No: the degree sum is odd' if sum(s) % 2 else 'No: a vertex would need more neighbors than exist' if max(s) >= len(s) else 'No: the Havel–Hakimi reduction fails')
        bad = ['Yes', 'No: the degree sum is odd', 'No: a vertex would need more neighbors than exist', 'No: the Havel–Hakimi reduction fails']
        b.mc(3, L, 'Is there a SIMPLE graph (no loops, no parallel edges) with degree sequence %s?' % ', '.join(map(str, s)), reason, [x for x in bad if x != reason],
             ['Check: the sum must be even; no degree may exceed n − 1; then repeatedly remove the largest degree d and subtract 1 from the next d degrees (Havel–Hakimi).', reason + '.'], 'degree_sequence')
    KN = [('cp2', 'How many edges does the complete graph K₅ have?', 10), ('cp1', 'How many edges does K₈ have?', 28), ('cp1', 'How many edges does the complete bipartite graph K₃,₄ have?', 12),
          ('honors', 'K_n has 66 edges. Find n.', 12), ('honors', 'How many edges does the cycle C₇ have, and what is each degree? Answer as "edges, degree".', '7, 2'), ('cp2', 'What is the degree of each vertex in K₆?', 5)]
    for L, t, v in KN:
        b.sa(3, L, t, v, ['K_n has C(n, 2) = n(n − 1)/2 edges, each vertex of degree n − 1; K_{m,n} has mn edges; C_n has n edges, each vertex degree 2.', 'Answer: %s' % v], 'special_graphs')
    b.sel(3, 'cp1', 'Which graphs are bipartite?', [('C₄ (a 4-cycle)', True), ('Any tree', True), ('K₂,₃', True), ('K₃ (a triangle)', False), ('C₅', False)],
          ['A graph is bipartite exactly when it has no odd cycle.'], 'construct_select')
    b.sel(3, 'cp2', 'Which statements describe a SIMPLE graph?', [('No loops', True), ('No parallel edges', True), ('Edges join two different vertices', True), ('Every vertex has degree 1', False), ('It must be connected', False)],
          ['Simple means no loops and no multiple edges; it need not be connected.'], 'construct_select')
    SQ = [[4, 3, 3, 2, 2], [2, 2, 2, 2, 2], [4, 4, 1, 1, 0], [3, 3, 3, 3, 0], [1, 1, 1, 1, 0]]
    b.sel(3, 'honors', 'Which degree sequences belong to a simple graph with 5 vertices?', [('Degrees ' + ', '.join(map(str, q)), graphical(q)) for q in SQ],
          ['Apply Havel–Hakimi to each.', '4, 4, 1, 1, 0 fails: two vertices adjacent to all four others would give every other vertex degree ≥ 2. 3, 3, 3, 3, 0 is K₄ plus an isolated vertex.'], 'construct_select')
    b.orq(3, 'cp2', 'Draw a simple graph with 4 vertices and degrees 2, 2, 2, 2.',
          [('How many edges will it have?', '4'), ('Describe one such graph.', 'A 4-cycle A–B–C–D–A'), ('Is it connected?', 'Yes'), ('Could two separate triangles work? Explain.', 'No; that needs 6 vertices.')],
          ['8/2.', 'Cycle.', 'One piece.', 'Count vertices.'], 'construct_or')
    b.orq(3, 'cp1', 'Consider K₄.',
          [('How many vertices and edges?', '4 vertices, 6 edges'), ('What is each degree?', '3'), ('Is K₄ bipartite?', 'No; it contains a triangle.'), ('How many edges must be removed to make a 4-cycle?', '2')],
          ['C(4, 2).', 'n − 1.', 'Odd cycle.', '6 − 4.'], 'construct_or')
    b.orq(3, 'honors', 'Apply Havel–Hakimi to the sequence 3, 3, 2, 2, 1, 1.',
          [('Remove 3 and subtract 1 from the next three terms.', '2, 1, 1, 1, 1'), ('Repeat.', '0, 0, 1, 1 → 1, 1, 0, 0'), ('Finish.', '0, 0, 0'), ('Is the sequence graphical?', 'Yes')],
          ['3,3,2,2,1,1 → 2,1,1,1,1.', 'Remove 2: 0,0,1,1 sorted 1,1,0,0.', 'Remove 1: 0,0,0.', 'Reduced to all zeros.'], 'construct_or')
    assert graphical([3, 3, 2, 2, 1, 1])


# ---------------------------------------------------------------- 4. coloring
def s4(b):
    for L, key in (('cp2', 'g8'), ('cp2', 'g1'), ('cp1', 'g3'), ('cp1', 'g5'), ('honors', 'g4'), ('honors', 'g6')):
        V, E, _ = GRAPHS[key]
        k = chromatic(V, E)
        r = num_mc(b, 4, L, 'What is the chromatic number of the graph shown (fewest colors so that adjacent vertices differ)?', k, [k - 1, k + 1, len(V)],
                   ['Find a coloring with k colors and a reason that k − 1 colors fail (for example, an odd cycle needs 3, a K₄ needs 4).', 'χ = %d' % k], 'chromatic')
        b.image(r, pic(key), alt(key))
    KN = [('cp2', 'K₄', 4), ('cp2', 'a path with 5 vertices', 2), ('cp1', 'C₆', 2), ('cp1', 'C₇', 3), ('honors', 'K₃,₃', 2), ('honors', 'the wheel W₅ (a 5-cycle plus a hub joined to all 5)', 4)]
    for L, g, k in KN:
        b.sa(4, L, 'What is the chromatic number of %s?' % g, k, ['K_n needs n colors; bipartite graphs need 2 (if they have an edge); odd cycles need 3; a hub adds 1.', 'χ = %d' % k], 'chromatic_family')
    SCH = [('cp1', 'Exams must not overlap for students taking both. Conflicts: Math–Bio, Math–Chem, Bio–Chem, Chem–Art. What is the minimum number of time slots?', 3),
           ('honors', 'Six radio stations: pairs closer than 100 km need different frequencies. Conflicts form a 6-cycle plus one long diagonal joining opposite stations. Minimum number of frequencies?', 2),
           ('cp2', 'Four countries: every pair shares a border. How many colors are needed for a map?', 4)]
    for L, t, v in SCH:
        b.sa(4, L, t, v, ['Build the conflict graph and find its chromatic number.', 'Answer: %d' % v], 'coloring_context')
    b.sel(4, 'cp1', 'Which graphs can be properly colored with 2 colors?', [('C₈', True), ('A tree with 10 vertices', True), ('K₂,₅', True), ('K₃', False), ('C₉', False)], ['Exactly the bipartite graphs (no odd cycles).'], 'coloring_select')
    b.sel(4, 'cp2', 'Which statements about proper colorings are true?', [('Adjacent vertices get different colors', True), ('Non-adjacent vertices may share a color', True), ('A triangle needs 3 colors', True), ('Every graph needs 4 colors', False), ('Each color can be used only once', False)],
          ['Definition of proper coloring.'], 'coloring_select')
    b.sel(4, 'honors', 'For any graph G with maximum degree Δ, which statements are true?', [('χ(G) ≤ Δ + 1', True), ('If G contains K₄, then χ(G) ≥ 4', True), ('If G has an odd cycle, then χ(G) ≥ 3', True), ('χ(G) = Δ always', False), ('χ(G) ≤ 2 always', False)],
          ['Greedy coloring uses at most Δ + 1 colors; subgraphs force lower bounds.'], 'coloring_select')
    b.orq(4, 'cp2', 'Color the 5-cycle A–B–C–D–E–A.',
          [('Try 2 colors starting red, blue, red, blue. What happens at E?', 'E is adjacent to D (blue) and A (red), so it needs a third color.'), ('What is the chromatic number?', '3'), ('Give a 3-coloring.', 'A red, B blue, C red, D blue, E green'), ('Which cycles can be 2-colored?', 'Even cycles')],
          ['Alternate.', 'Odd cycle.', 'Any valid one.', 'Even length.'], 'coloring_or')
    b.orq(4, 'cp1', 'Committees: A shares members with B and C; B shares with C and D; D shares with E.',
          [('Draw the conflict graph (list edges).', 'AB, AC, BC, BD, DE'), ('Find a lower bound for the number of meeting times.', '3, because A, B, C form a triangle'), ('Give a schedule with 3 times.', 'A 1, B 2, C 3, D 1, E 2'), ('What is the minimum?', '3')],
          ['Edges = conflicts.', 'Triangle.', 'Proper coloring.', 'Lower bound met.'], 'coloring_or')
    b.orq(4, 'honors', 'Greedy coloring: order the vertices and give each the smallest color not used by its neighbors.',
          [('Greedy-color C₆ in the order A, D, B, E, C, F (cycle A–B–C–D–E–F–A). How many colors are used?', '3'), ('What is χ(C₆)?', '2'),
           ('What does this show about greedy coloring?', 'It can use more colors than necessary; the order matters.'), ('Give an order for which greedy uses 2 colors on C₆.', 'A, B, C, D, E, F')],
          ['A1, D1, B2, E2, C3, F3.', 'Even cycle.', 'Not always optimal.', 'Going around the cycle.'], 'coloring_or')


# ---------------------------------------------------------------- 5. trails and paths
def s5(b):
    V, E, _ = GRAPHS['g1']
    p = pic('g1')
    CL = [('cp2', 'A–B–C–D', 'A path (no repeated vertex, so also a trail)'), ('cp2', 'A–B–C–A–D', 'A trail that is not a path'), ('cp1', 'A–B–A–C', 'A walk that is not a trail'),
          ('cp1', 'A–C–D', 'A path (no repeated vertex, so also a trail)'), ('honors', 'D–A–C–B–A', 'A trail that is not a path'), ('honors', 'B–C–A–B–C', 'A walk that is not a trail')]
    opts = ['A path (no repeated vertex, so also a trail)', 'A trail that is not a path', 'A walk that is not a trail', 'Not a walk in this graph']
    edges = {frozenset(e) for e in E}
    for L, w, good in CL:
        seq = w.split('–')
        es = [frozenset((seq[i], seq[i + 1])) for i in range(len(seq) - 1)]
        assert all(e in edges for e in es)
        calc = opts[0] if len(set(seq)) == len(seq) else opts[1] if len(set(es)) == len(es) else opts[2]
        assert calc == good, w
        r = b.mc(5, L, 'In the graph shown, classify the sequence %s. %s' % (w, DEF), good, [o for o in opts if o != good], ['Check for repeated edges (trail) and repeated vertices (path).', good], 'classify_walk')
        b.image(r, p, alt('g1'))
    for L, key in (('cp2', 'g8'), ('cp1', 'g5'), ('cp1', 'g1'), ('honors', 'g3'), ('honors', 'g2')):
        V, E, _ = GRAPHS[key]
        kind, odd = euler_kind(V, E)
        good = {'circuit': 'An Euler circuit (every vertex has even degree)', 'trail': 'An Euler trail from %s to %s, but no Euler circuit' % tuple(odd[:2] if len(odd) == 2 else ('?', '?')), 'none': 'Neither (more than two odd-degree vertices, or disconnected)'}[kind]
        bad = ['An Euler circuit (every vertex has even degree)', 'An Euler trail between two odd vertices, but no Euler circuit', 'Neither (more than two odd-degree vertices, or disconnected)', 'Both an Euler circuit and an Euler trail that is not closed']
        if kind == 'trail':
            bad[1] = 'An Euler trail from %s to %s, but no Euler circuit' % (sorted(set(V) - set(odd))[0], odd[0])
        r = b.mc(5, L, 'Does the graph shown have an Euler circuit, an Euler trail (using every edge exactly once, not closed), or neither?', good, [x for x in bad if x != good][:3],
                 ['Degrees: %s.' % degrees(V, E), 'Connected with 0 odd vertices → Euler circuit; exactly 2 odd vertices → Euler trail between them; otherwise neither.', good], 'euler_trail')
        b.image(r, pic(key), alt(key))
    b.sel(5, 'cp1', 'Which statements match the course definitions?', [('Every path is a trail', True), ('Every trail is a walk', True), ('A trail may repeat a vertex', True), ('Every trail is a path', False), ('A path may repeat an edge', False)],
          ['Path ⊂ trail ⊂ walk.'], 'trail_select')
    b.sel(5, 'cp2', 'A graph has vertices with degrees 2, 2, 3, 3 and is connected. Which statements are true?', [('It has an Euler trail', True), ('The trail must start at an odd vertex', True), ('It has no Euler circuit', True), ('It has an Euler circuit', False), ('Any vertex can start the Euler trail', False)],
          ['Exactly two odd vertices: an Euler trail starts at one and ends at the other.'], 'trail_select')
    b.sel(5, 'honors', 'For which complete graphs K_n (n ≥ 2) does an Euler trail OR circuit exist?', [('K₂', True), ('K₃', True), ('K₅', True), ('K₄', False), ('K₆', False)],
          ['K_n has degree n − 1 at all n vertices: odd n → all even (circuit); n = 2 → two odd vertices (trail); even n ≥ 4 → more than 2 odd vertices.'], 'trail_select')
    b.orq(5, 'cp2', 'The Königsberg bridges: four land areas with degrees 5, 3, 3, 3.',
          [('How many vertices have odd degree?', '4'), ('Can you walk across every bridge exactly once? Explain.', 'No; an Euler trail needs 0 or 2 odd vertices.'), ('How many bridges are there?', '7'), ('Add one bridge between two odd areas: how many odd vertices remain?', '2')],
          ['All four.', 'Euler\'s theorem.', '14/2.', 'Two become even.'], 'trail_or')
    b.orq(5, 'cp1', 'Graph: square A–B–C–D–A plus diagonal A–C.',
          [('List the degrees.', 'A 3, B 2, C 3, D 2'), ('Does it have an Euler circuit?', 'No'), ('Give an Euler trail.', 'A–B–C–A–D–C'), ('Is your trail a path? Why?', 'No; it repeats vertices A and C.')],
          ['Count.', 'Two odd vertices.', 'Start at an odd vertex.', 'Vertices repeat.'], 'trail_or')
    b.orq(5, 'honors', 'Prove: if a connected graph has an Euler trail that is not a circuit, then exactly two vertices have odd degree.',
          [('Consider an internal vertex of the trail. Why is its degree even?', 'Each pass through it uses one edge in and one edge out.'), ('Why does the start vertex have odd degree?', 'It has one extra edge used at the beginning.'),
           ('Why does the end vertex have odd degree?', 'One extra edge at the end.'), ('Why must start ≠ end?', 'If they were equal the trail would be a circuit.')],
          ['Pairs of edges.', 'Unpaired first edge.', 'Unpaired last edge.', 'Not closed.'], 'trail_or')


# ---------------------------------------------------------------- 6. circuits
def s6(b):
    for L, key in (('cp2', 'g8'), ('cp1', 'g5'), ('honors', 'g6'), ('honors', 'g7')):
        V, E, _ = GRAPHS[key]
        h = ham_circuit(V, E)
        good = 'Yes, for example ' + '–'.join(h) if h else 'No Hamiltonian circuit exists'
        bad = ['No Hamiltonian circuit exists' if h else 'Yes, for example ' + '–'.join(V + [V[0]]), 'Yes, because every vertex has degree at least 2', 'No, because some vertex has odd degree']
        r = b.mc(6, L, 'Does the graph shown have a Hamiltonian circuit (a cycle through every vertex exactly once)?', good, [x for x in bad if x != good],
                 ['Search for a cycle visiting each vertex once (degree conditions alone do not decide this).', good], 'hamiltonian')
        b.image(r, pic(key), alt(key))
    CI = [('cp2', 'Is A–B–C–A a circuit in a triangle ABC?', 'Yes: it is closed and repeats no edge', ['No: it repeats vertex A', 'No: a circuit must use 4 edges', 'Yes: but only because it repeats an edge']),
          ('cp1', 'In the square A–B–C–D–A with diagonal AC, is A–B–C–A–D–C–A a circuit?', 'No: it repeats the edge CA', ['Yes: it is closed', 'Yes: it is an Euler circuit', 'No: it repeats vertex C, which a circuit never allows']),
          ('honors', 'What distinguishes a cycle (simple circuit) from a circuit?', 'A cycle repeats no vertex except that it starts and ends at the same vertex', ['A cycle repeats no edge but may repeat vertices', 'A cycle must use every edge', 'A cycle must use every vertex'])]
    for L, t, good, bad in CI:
        b.mc(6, L, t + ' ' + DEF, good, bad, ['Circuits are closed trails; cycles are closed paths.', good], 'circuit_def')
    EC = [('cp2', 'A connected graph has degrees 2, 4, 4, 2, 2. Does it have an Euler circuit? Answer Yes or No.', 'Yes'), ('cp1', 'A connected graph has degrees 2, 3, 3, 2, 4, 2. Does it have an Euler circuit? Answer Yes or No.', 'No'),
          ('honors', 'For which n ≥ 3 does K_n have an Euler circuit? Answer: "n odd", "n even" or "all n".', 'n odd'), ('cp1', 'How many edges does an Euler circuit of K₅ traverse?', '10'),
          ('honors', 'How many Hamiltonian cycles does K₅ have, counting cycles as the same if they use the same edges?', str(math.factorial(4) // 2)), ('cp2', 'How many edges does a Hamiltonian circuit in a graph with 6 vertices use?', '6')]
    for L, t, a in EC:
        b.sa(6, L, t, a, ['Euler circuit ⟺ connected and all degrees even. A Hamiltonian cycle on n vertices uses n edges; K_n has (n − 1)!/2 of them.', 'Answer: ' + a], 'circuit_facts')
    b.sel(6, 'cp1', 'Which graphs have an Euler circuit?', [('C₆', True), ('K₅', True), ('K₂,₂', True), ('K₄', False), ('A path with 3 vertices', False)], ['All degrees even and connected.'], 'circuit_select')
    b.sel(6, 'cp2', 'Which statements about Euler circuits are true?', [('They use every edge exactly once', True), ('They start and end at the same vertex', True), ('They need every degree to be even (connected graph)', True), ('They visit every vertex exactly once', False), ('They exist in every graph', False)],
          ['Visiting every vertex once is the Hamiltonian idea.'], 'circuit_select')
    b.sel(6, 'honors', 'Which graphs have a Hamiltonian cycle?', [('C₇', True), ('K₄', True), ('K₃,₃', True), ('K₂,₃', False), ('A tree with 4 vertices', False)],
          ['K₂,₃ would need the cycle to alternate sides equally (2 ≠ 3); trees have no cycles.'], 'circuit_select')
    b.orq(6, 'cp2', 'Graph: triangle A–B–C plus triangle C–D–E sharing vertex C.',
          [('List the degrees.', 'A 2, B 2, C 4, D 2, E 2'), ('Does it have an Euler circuit?', 'Yes'), ('Give one.', 'A–B–C–D–E–C–A'), ('Does it have a Hamiltonian cycle? Why?', 'No; any cycle through all vertices would pass through C twice.')],
          ['Count.', 'All even, connected.', 'Use both triangles.', 'C is a cut vertex.'], 'circuit_or')
    b.orq(6, 'cp1', 'A mail carrier must walk every street exactly once and return to the post office.',
          [('What graph concept models this?', 'An Euler circuit'), ('What condition on the street graph is needed?', 'Connected and every intersection has even degree.'), ('If two intersections have odd degree, what is the fewest streets to repeat?', 'The streets on a shortest route between those two intersections.'), ('Which concept models visiting every house (vertex) once instead?', 'A Hamiltonian cycle')],
          ['Every edge.', 'Euler\'s theorem.', 'Route inspection.', 'Every vertex.'], 'circuit_or')
    b.orq(6, 'honors', 'Traveling salesperson on K₄ with weights AB 3, AC 5, AD 4, BC 2, BD 6, CD 1.',
          [('How many distinct Hamiltonian cycles does K₄ have?', '3'), ('Find the weight of A–B–C–D–A.', '3 + 2 + 1 + 4 = 10'), ('Find the weights of the other two cycles.', 'A–B–D–C–A: 3 + 6 + 1 + 5 = 15; A–C–B–D–A: 5 + 2 + 6 + 4 = 17'), ('Which cycle is cheapest?', 'A–B–C–D–A (10)')],
          ['(4 − 1)!/2.', 'Add.', 'Add.', 'Compare.'], 'circuit_or')


# ---------------------------------------------------------------- 7. trees
def s7(b):
    TF = [('cp2', 'A tree has 12 vertices. How many edges does it have?', 11), ('cp2', 'A tree has 20 edges. How many vertices?', 21), ('cp1', 'A forest has 30 vertices and 3 trees (components). How many edges?', 27),
          ('cp1', 'A tree has 2 vertices of degree 3, 1 vertex of degree 2, and the rest are leaves. How many leaves?', 4), ('honors', 'A tree has 3 vertices of degree 4 and all others are leaves. How many leaves?', 8),
          ('honors', 'How many labeled trees are there on 5 vertices (Cayley\'s formula nⁿ⁻²)?', 125)]
    for L, t, v in TF:
        b.sa(7, L, t, v, ['A tree with n vertices has n − 1 edges; use the degree sum 2(n − 1) to solve for leaves.', 'Answer: %d' % v], 'tree_facts')
    V, E, _ = GRAPHS['t1']
    r = b.sa(7, 'cp2', 'How many leaves (vertices of degree 1) does the tree shown have?', sum(1 for v, d in degrees(V, E).items() if d == 1), ['A leaf has degree 1.', 'Leaves: B, D, F.'], 'tree_read')
    b.image(r, pic('t1'), alt('t1'))
    r = b.mc(7, 'cp1', 'In the tree shown, which edge could be removed to leave exactly two components, one containing only F?', 'EF', ['CE', 'AC', 'AB'], ['Every edge of a tree is a bridge; removing EF isolates F.'], 'tree_read')
    b.image(r, pic('t1', suffix='_b'), alt('t1'))
    W = [('A', 'B', 4), ('A', 'C', 2), ('B', 'C', 5), ('B', 'D', 10), ('C', 'D', 3), ('C', 'E', 8), ('D', 'E', 6)]
    G = nx.Graph(); G.add_weighted_edges_from(W)
    mst = sum(d['weight'] for *_, d in nx.minimum_spanning_tree(G).edges(data=True))
    pw = figs.graph(U, 'weighted1', list('ABCDE'), [(u, v) for u, v, _ in W], pos={'A': (-1, 0.6), 'B': (0, 1.2), 'C': (0, 0), 'D': (1, 0.6), 'E': (1, -0.8)}, weights=[w for *_, w in W])
    for L, t in (('cp1', 'Find the total weight of a minimum spanning tree of the weighted graph shown (Kruskal\'s or Prim\'s algorithm).'), ('honors', 'Find the total weight of a minimum spanning tree of the weighted graph shown, and be ready to justify each edge choice with Kruskal\'s algorithm.')):
        r = b.sa(7, L, t, mst, ['Kruskal: sort edges by weight; add each edge unless it makes a cycle: AC 2, CD 3, AB 4, DE 6.', 'Total = %d' % mst], 'mst')
        b.image(r, pw, 'Weighted graph: AB 4, AC 2, BC 5, BD 10, CD 3, CE 8, DE 6.')
    b.mc(7, 'honors', 'Using the same weighted graph, how many edges does any spanning tree have?', '4', ['5', '7', '3'], ['5 vertices → 4 edges.'], 'mst', order='sort')
    b.sel(7, 'cp1', 'Which statements are true for EVERY tree with n ≥ 2 vertices?', [('It has n − 1 edges', True), ('It is connected', True), ('It has at least two leaves', True), ('It contains a cycle', False), ('Every vertex has degree at most 2', False)],
          ['Trees are connected and acyclic, with n − 1 edges and at least two leaves.'], 'tree_select')
    b.sel(7, 'cp2', 'Which graphs are trees?', [('A path with 5 vertices', True), ('A star with one center and 4 leaves', True), ('A triangle', False), ('A single vertex', True), ('Two separate edges', False)],
          ['A tree is connected with no cycles; a single vertex counts.'], 'tree_select')
    b.sel(7, 'honors', 'A connected graph G has n vertices. Which conditions each guarantee G is a tree?', [('G has n − 1 edges', True), ('G has no cycles', True), ('Removing any edge disconnects G', True), ('G has n edges', False), ('Every vertex has even degree', False)],
          ['For connected graphs, each of n − 1 edges, acyclic, or minimally connected characterizes trees.'], 'tree_select')
    b.orq(7, 'cp2', 'A company\'s org chart is a tree with the CEO at the top and 9 other employees.',
          [('How many edges does the chart have?', '9'), ('Why is there no cycle?', 'Each employee has exactly one boss.'), ('If the CEO has 3 direct reports, what is the CEO\'s degree?', '3'), ('What are the leaves?', 'Employees who supervise no one.')],
          ['n − 1.', 'Unique parent.', 'Edges at the CEO.', 'Degree 1 (other than the root).'], 'tree_or')
    b.orq(7, 'cp1', 'Use Kruskal\'s algorithm on edges AB 1, BC 2, AC 3, CD 4, BD 5.',
          [('Which edges are chosen in order?', 'AB, BC, CD'), ('Why is AC rejected?', 'It would form the cycle A–B–C–A.'), ('What is the MST weight?', '7'), ('How many edges does the MST have?', '3')],
          ['Sort and add.', 'Cycle check.', '1 + 2 + 4.', 'n − 1.'], 'tree_or')
    b.orq(7, 'honors', 'Prove that every tree with n ≥ 2 vertices has at least two leaves.',
          [('Take a longest path v₁, ..., v_k. Why can v₁ have no neighbor outside the path?', 'The path could be extended, contradicting maximality.'), ('Why can v₁ not be adjacent to v_j for j > 2?', 'That edge would create a cycle.'),
           ('What is deg(v₁)?', '1'), ('Apply the same argument to v_k and conclude.', 'v_k is also a leaf, so there are at least two leaves.')],
          ['Maximality.', 'Acyclic.', 'Only neighbor v₂.', 'Symmetric end.'], 'tree_or')


def topup(b):
    need = lambda k, L: b.counter.get((k, L), 0) < 10
    rng = seeded('u8top')
    for k in range(1, 8):
        for L in ('cp2', 'cp1', 'honors'):
            g = 0
            while need(k, L) and g < 30:
                g += 1
                n = rng.randint(4, 7)
                V = [chr(65 + i) for i in range(n)]
                E = [e for e in itertools.combinations(V, 2) if rng.random() < 0.5]
                if len(E) < n - 1:
                    continue
                Es = ', '.join(u + w for u, w in E)
                d = degrees(V, E)
                pre = 'A simple graph has vertices %s and edges %s. ' % (', '.join(V), Es)
                if any(q['prompt'].startswith(pre) for q in b.q):
                    continue
                if k == 1:
                    v = rng.choice(V)
                    num_mc(b, 1, L, pre + 'Find deg(%s).' % v, d[v], [d[v] + 1, max(0, d[v] - 1), len(E)], ['Count edges containing %s.' % v, 'deg(%s) = %d' % (v, d[v])], 'degree')
                elif k == 2:
                    num_mc(b, 2, L, pre + 'If every edge is replaced by two arrows (one each way), what is the sum of the in-degrees?', 2 * len(E), [len(E), 4 * len(E), 2 * len(E) + 1],
                           ['Each undirected edge becomes 2 arrows; Σ in-degrees = number of arrows.', '%d' % (2 * len(E))], 'in_out_degree')
                elif k == 3:
                    num_mc(b, 3, L, pre + 'How many edges must be added to make it the complete graph K_%d?' % n, n * (n - 1) // 2 - len(E), [n * (n - 1) // 2, len(E), n * (n - 1) // 2 - len(E) + 1],
                           ['K_%d has C(%d, 2) = %d edges.' % (n, n, n * (n - 1) // 2), '%d − %d = %d' % (n * (n - 1) // 2, len(E), n * (n - 1) // 2 - len(E))], 'special_graphs')
                elif k == 4:
                    c = chromatic(V, E)
                    num_mc(b, 4, L, pre + 'Find its chromatic number.', c, [c - 1 if c > 1 else c + 2, c + 1, n], ['Find a proper coloring with the fewest colors (a triangle forces 3, K₄ forces 4).', 'χ = %d (found by exhaustive search)' % c], 'chromatic')
                elif k == 5:
                    kind, odd = euler_kind(V, E)
                    good = {'circuit': 'An Euler circuit', 'trail': 'An Euler trail but no Euler circuit', 'none': 'Neither'}[kind]
                    b.mc(5, L, pre + 'Does it have an Euler circuit, an Euler trail (not closed), or neither? (Isolated vertices are ignored.)', good, [x for x in ['An Euler circuit', 'An Euler trail but no Euler circuit', 'Neither', 'Both an Euler circuit and a Hamiltonian circuit'] if x != good],
                         ['Degrees: ' + ', '.join('%s %d' % kv for kv in d.items()) + '.', 'Odd-degree vertices: %d → %s.' % (len(odd), good)], 'euler_trail')
                elif k == 6:
                    h = ham_circuit(V, E)
                    good = 'Yes, for example ' + '–'.join(h) if h else 'No'
                    b.mc(6, L, pre + 'Does it have a Hamiltonian cycle?', good, ['No' if h else 'Yes, for example ' + '–'.join(V + [V[0]]), 'Yes, because it is connected', 'No, because some degree is odd'],
                         ['Search systematically for a cycle through every vertex once.', good + (' (verified by checking all orderings).' if not h else '.')], 'hamiltonian')
                elif k == 7:
                    G = nx.Graph(); G.add_nodes_from(V); G.add_edges_from(E)
                    if not nx.is_connected(G):
                        continue
                    num_mc(b, 7, L, pre + 'How many edges must be removed to leave a spanning tree?', len(E) - (n - 1), [len(E) - n, n - 1, len(E)],
                           ['A spanning tree on %d vertices has %d edges.' % (n, n - 1), '%d − %d = %d' % (len(E), n - 1, len(E) - n + 1)], 'tree_facts')


def errors(b):
    E = b.err
    E(1, 'cp2', 'Find the degree of a vertex with one loop and two other edges.', 'Jordan', ['1 loop + 2 edges = 3.'],
      '4', 'Jordan counted the loop once. A loop contributes 2 to the degree (both ends are at the vertex).', 'Degree counts edge-ends.', ['2 + 1 + 1 = 4.'], 'loop_degree_error')
    E(1, 'cp2', 'A graph has degrees 3, 2, 2, 1. How many edges?', 'Sam', ['3 + 2 + 2 + 1 = 8 edges.'],
      '4', 'Sam forgot to divide by 2. Each edge adds 2 to the degree sum.', 'Handshake theorem.', ['8 / 2 = 4.'], 'handshake_error')
    E(5, 'cp2', 'In the square A–B–C–D–A with diagonal AC, is A–B–C–A–D a path?', 'Riley', ['Yes, because it never uses the same edge twice.'],
      'No; it is a trail (no repeated edge) but not a path, because vertex A repeats', 'Riley confused "no repeated edge" (trail) with "no repeated vertex" (path).', 'Every path is a trail, but not every trail is a path.', ['Vertices: A, B, C, A, D: A appears twice.'], 'path_trail_error')
    E(4, 'cp2', 'Chromatic number of a triangle?', 'Casey', ['Two colors: red, blue, red.'],
      '3', 'Casey reused red on two adjacent vertices; in a triangle every pair is adjacent.', 'Check every edge.', ['Each vertex needs its own color.'], 'triangle_color_error')
    E(7, 'cp2', 'How many edges in a tree with 15 vertices?', 'Avery', ['15 edges.'],
      '14', 'Avery used n instead of n − 1. A tree with n edges would contain a cycle.', 'Trees: |E| = |V| − 1.', ['15 − 1 = 14.'], 'tree_edges_error')
    E(2, 'cp2', 'Directed edges A→B, B→A, A→C. Find the out-degree of A.', 'Morgan', ['A touches 3 arrows, so 3.'],
      '2', 'Morgan counted all arrows at A. Out-degree counts only arrows leaving A.', 'In-degree and out-degree are separate.', ['A→B and A→C.'], 'out_degree_error')
    E(5, 'cp1', 'A connected graph has degrees 2, 2, 3, 3, 4. Does it have an Euler circuit?', 'Taylor', ['Yes, because most degrees are even.'],
      'No (it has an Euler trail between the two odd vertices)', 'Taylor ignored the odd vertices. An Euler circuit needs EVERY degree even.', 'Euler\'s theorem.', ['Two odd vertices → Euler trail only.'], 'most_even_error')
    E(6, 'cp1', 'Every vertex of a connected graph has degree ≥ 2. Must it have a Hamiltonian cycle?', 'Jamie', ['Yes; each vertex can be entered and left.'],
      'No; e.g., two triangles sharing one vertex', 'Jamie assumed a degree condition guarantees a Hamiltonian cycle; local degree is not enough.', 'A cut vertex blocks a Hamiltonian cycle.', ['The shared vertex would be visited twice.'], 'ham_degree_error')
    E(3, 'cp1', 'Is there a simple graph with 4 vertices and degrees 4, 2, 1, 1?', 'Quinn', ['The degree sum 4 + 2 + 1 + 1 = 8 is even, so yes.'],
      'No', 'Quinn checked only parity. In a simple graph with 4 vertices a vertex has at most 3 neighbors, so degree 4 is impossible.', 'An even sum is necessary but not sufficient.', ['Max degree is n − 1 = 3.'], 'degree_bound_error')
    E(7, 'cp1', 'Kruskal on AB 1, AC 1, BC 2, CD 3. Find the MST weight.', 'Alex', ['Take the three cheapest edges: 1 + 1 + 2 = 4.'],
      '5', 'Alex took BC, which forms a cycle A–B–C with AB and AC. Kruskal skips cycle-forming edges.', 'Check for cycles before adding an edge.', ['AB, AC, CD: 1 + 1 + 3 = 5.'], 'kruskal_cycle_error')
    E(4, 'cp1', 'Chromatic number of C₆ (a 6-cycle)?', 'Jordan', ['It is a cycle, and cycles need 3 colors.'],
      '2', 'Jordan generalized from odd cycles. Even cycles alternate two colors.', 'Only odd cycles need 3.', ['Red, blue, red, blue, red, blue.'], 'even_cycle_error')
    E(2, 'cp1', 'In a directed graph Σ in-degrees = 7. How many edges?', 'Sam', ['Edges = 7/2.'],
      '7', 'Sam applied the undirected handshake theorem. Each arrow adds 1 to exactly one in-degree.', 'Directed: Σ in = Σ out = |E|.', ['|E| = 7.'], 'directed_handshake_error')
    E(6, 'honors', 'Does K₄ have an Euler circuit?', 'Riley', ['K₄ has a Hamiltonian cycle A–B–C–D–A, so it has an Euler circuit.'],
      'No; every vertex of K₄ has odd degree 3', 'Riley confused Hamiltonian (every vertex once) with Euler (every edge once).', 'Different conditions.', ['Four odd vertices → no Euler trail or circuit.'], 'euler_ham_error')
    E(5, 'honors', 'Find an Euler trail in a connected graph with odd vertices B and E.', 'Casey', ['Start at A and use every edge once.'],
      'Start at B and end at E (or the reverse)', 'Casey started at an even vertex. An Euler trail must start and end at the two odd vertices.', 'Starting elsewhere leaves an odd vertex unbalanced.', ['Start at one odd vertex, end at the other.'], 'trail_start_error')
    E(7, 'honors', 'A connected graph has 10 vertices and 9 edges. Is it a tree?', 'Avery', ['Not necessarily; it could contain a cycle.'],
      'Yes', 'Avery missed the theorem: a connected graph with n vertices and n − 1 edges is a tree.', 'A cycle would force at least n edges in a connected graph.', ['Connected + n − 1 edges ⇒ acyclic.'], 'tree_theorem_error')
    E(3, 'honors', 'How many edges does K₃,₄ have?', 'Morgan', ['C(7, 2) = 21'],
      '12', 'Morgan counted K₇. In K₃,₄ edges only join the two parts.', 'K_{m,n} has mn edges.', ['3·4 = 12.'], 'bipartite_edges_error')
    E(4, 'honors', 'A graph has maximum degree 3. Must χ = 4?', 'Taylor', ['χ ≤ Δ + 1 = 4, so χ = 4.'],
      'No; χ ≤ 4 is only an upper bound (K₃,₃ has Δ = 3 and χ = 2)', 'Taylor treated an upper bound as an exact value.', 'Bounds give inequalities.', ['K₃,₃ has Δ = 3 and χ = 2.'], 'bound_exact_error')
    E(1, 'honors', 'Prove there is no graph with degrees 3, 3, 3.', 'Jamie', ['Try drawing it: I could not, so it is impossible.'],
      'The degree sum 9 is odd, contradicting Σ deg = 2|E|', 'Jamie relied on failed attempts, which do not prove impossibility.', 'Use the handshake theorem.', ['Odd degree sum is impossible.'], 'drawing_proof_error')
