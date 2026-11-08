/* Discrete Math Unit 8 cheat sheet (Theory of Graphs and Trees). Degrees, Euler conditions and MST weights are checked. */
const D = require('../dmfigs.cjs');
const deg = (E, v) => E.reduce((s, e) => s + (e[0] === v) + (e[1] === v), 0);
const G1 = [['A', 'B'], ['A', 'B'], ['B', 'C'], ['C', 'C'], ['C', 'D']];
const SQ = [['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'A'], ['A', 'C']];
module.exports = {
  name: 'discrete-graphs-trees', course: 'Discrete Math', unitNo: 8, unitName: 'Graphs and Trees',
  focus: 'vertices, edges, loops, degrees, directed graphs, constructing graphs and graph coloring',
  morefocus: 'walks, trails, paths, circuits, Euler and Hamiltonian circuits, trees and spanning trees',
  front: [
    { title: 'Graph Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['vertex, edge', 'points and the connections between them', 'K₄ has 4 vertices, 6 edges'],
      ['loop', 'an edge from a vertex to itself', 'adds 2 to the degree'],
      ['parallel edges', 'two edges with the same endpoints', 'A–B twice'],
      ['simple graph', 'no loops, no parallel edges', 'K₅'],
      ['degree', 'number of edge-ends at a vertex', 'see the figure']] },
    { title: 'Degrees and the Handshake Theorem', color: 'blue', kind: 'html', figFirst: true,
      fig: D.graph({ id: 'g1', v: { A: [5, 15], B: [95, 15], C: [95, 85], D: [5, 85] }, e: G1, inches: 1.85, h: 110 }),
      html: 'Degrees: A 2, B 3, C 4 (the loop counts 2), D 1. Sum ⟨= 10 = 2 \\cdot 5⟩ edges. <b>Handshake:</b> ⟨\\sum \\deg(v) = 2|E|⟩, so the number of odd-degree vertices is even.',
      check: [{ true: [deg(G1, 'A'), deg(G1, 'B'), deg(G1, 'C'), deg(G1, 'D')].join() === '2,3,4,1' ? 'true' : 'false' }, { num: 2 + 3 + 4 + 1, is: 10 }] },
    { title: 'Directed Graphs', color: 'green', kind: 'html', figFirst: true,
      fig: D.graph({ id: 'dg', v: { A: [5, 15], B: [95, 15], C: [95, 85], D: [5, 85] }, e: [['A', 'B'], ['B', 'C'], ['C', 'A'], ['C', 'D'], ['A', 'D']], directed: true, inches: 1.75, h: 100 }),
      html: 'In-degree = arrows in; out-degree = arrows out. ⟨\\sum \\text{in} = \\sum \\text{out} = |E|⟩. Here A: in 1, out 2. Use a directed graph when the relationship is one-way (follows, prerequisites, one-way streets).' },
    { title: 'Special Graphs', color: 'orange', kind: 'table', head: ['Graph', 'Edges', 'Degrees'], rows: [
      ['complete ⟨K_n⟩', '⟨\\binom{n}{2} = \\tfrac{n(n - 1)}{2}⟩', 'all ⟨n - 1⟩'], ['cycle ⟨C_n⟩', '⟨n⟩', 'all 2'], ['complete bipartite ⟨K_{m,n}⟩', '⟨mn⟩', '⟨n⟩ and ⟨m⟩'], ['tree on ⟨n⟩ vertices', '⟨n - 1⟩', 'at least 2 leaves']],
      after: '<b>Degree sequence test</b> (simple graphs): even sum, no degree above ⟨n - 1⟩, then Havel–Hakimi. ⟨4, 2, 1, 1⟩ fails (degree 4 with only 3 other vertices).',
      check: [{ num: '5*4/2', is: 10 }] },
    { title: 'Graph Coloring', color: 'pink', kind: 'html', figFirst: true,
      fig: D.graph({ id: 'gc', v: { A: [50, 0], B: [100, 38], C: [80, 100], D: [20, 100], E: [0, 38] }, e: [['A', 'B'], ['B', 'C'], ['C', 'D'], ['D', 'E'], ['E', 'A']], color: { A: '#fecaca', B: '#bfdbfe', C: '#fecaca', D: '#bfdbfe', E: '#bbf7d0' }, inches: 1.6, h: 105 }),
      html: 'Adjacent vertices get different colors. ⟨\\chi(C_5) = 3⟩ (odd cycle), ⟨\\chi(C_6) = 2⟩, ⟨\\chi(K_n) = n⟩, bipartite ⟨\\chi = 2⟩. Scheduling: vertices = events, edges = conflicts.' },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['A loop adds 2 to the degree.', 'State whether the graph is directed and whether loops are allowed.', 'A lower bound (a triangle) plus a coloring proves χ.'],
      bad: [['Adding degrees and calling it the number of edges', 'divide by 2'], ['“Every cycle needs 3 colors”', 'only odd cycles'], ['Treating an upper bound as χ', '⟨\\chi \\le \\Delta + 1⟩ is a bound']] }
  ],
  back: [
    { title: 'Walks, Trails, Paths, Circuits', color: 'purple', kind: 'table', head: ['Term', 'Repeats an edge?', 'Repeats a vertex?'], rows: [
      ['walk', 'allowed', 'allowed'], ['trail', '<b>no</b>', 'allowed'], ['path', 'no', '<b>no</b>'], ['circuit (closed trail)', 'no', 'allowed (ends at start)'], ['cycle (simple circuit)', 'no', 'only start = end']],
      after: 'In the square A–B–C–D–A with diagonal AC: A–B–C–A–D is a trail, not a path; A–B–C–D is a path.' },
    { title: 'Euler Trails and Circuits', color: 'blue', kind: 'html', figFirst: true,
      fig: D.graph({ id: 'eu', v: { A: [5, 10], B: [95, 10], C: [95, 90], D: [5, 90] }, e: SQ, inches: 1.7, h: 100 }),
      html: 'Uses <b>every edge</b> once. Connected graph: all degrees even ⟹ Euler circuit; exactly two odd vertices ⟹ Euler trail from one to the other; otherwise neither. Here A, C have degree 3: trail A–B–C–A–D–C.',
      check: [{ true: [deg(SQ, 'A'), deg(SQ, 'B'), deg(SQ, 'C'), deg(SQ, 'D')].join() === '3,2,3,2' ? 'true' : 'false' }] },
    { title: 'Hamiltonian Cycles', color: 'green', kind: 'html',
      html: 'Visits every <b>vertex</b> once and returns. No simple degree test decides it: two triangles sharing a vertex have all degrees even (Euler circuit) but no Hamiltonian cycle. ⟨K_n⟩ has ⟨\\tfrac{(n - 1)!}{2}⟩ Hamiltonian cycles (12 for ⟨K_5⟩).',
      check: { num: '24/2', is: 12 } },
    { title: 'Trees', color: 'orange', kind: 'html', figFirst: true,
      fig: D.graph({ id: 'tr', v: { A: [10, 10], B: [10, 90], C: [50, 50], D: [50, 95], E: [90, 50], F: [90, 95] }, e: [['A', 'C'], ['B', 'C'], ['C', 'D'], ['C', 'E'], ['E', 'F']], inches: 1.65, h: 95 }),
      html: 'A <b>tree</b> is connected with no cycles. With ⟨n⟩ vertices it has ⟨n - 1⟩ edges; every edge is a bridge; there are at least 2 leaves (here A, B, D, F). Degree sum ⟨2(n - 1)⟩ helps count leaves.',
      check: { num: '6-1', is: 5 } },
    { title: 'Minimum Spanning Tree', color: 'pink', kind: 'example', text: 'Kruskal: take edges from lightest to heaviest, skipping any that would make a cycle.',
      fig: D.graph({ id: 'ms', v: { A: [0, 35], B: [50, 0], C: [50, 70], D: [100, 35], E: [100, 100] }, e: [['A', 'B'], ['A', 'C'], ['B', 'C'], ['B', 'D'], ['C', 'D'], ['C', 'E'], ['D', 'E']], wt: [4, 2, 5, 10, 3, 8, 6], hl: [1, 4, 0, 6], inches: 1.8, h: 95 }),
      example: 'AB 4, AC 2, BC 5, BD 10, CD 3, CE 8, DE 6', steps: [['Take:', 'AC 2, CD 3, AB 4, DE 6'], ['Skip:', 'BC 5 (cycle A–B–C)']], answer: 'weight 15',
      check: { num: '2+3+4+6', is: 15 } },
    { title: 'Mistakes and Challenge', color: 'teal', kind: 'mistakes',
      good: ['Euler = every edge; Hamilton = every vertex.', 'An Euler trail must start at an odd vertex.', 'A connected graph with ⟨n - 1⟩ edges is a tree.'],
      bad: [['“Most degrees are even, so there is an Euler circuit”', 'all must be even'], ['Including a cycle-forming edge in Kruskal', 'skip it'], ['Challenge: Königsberg (degrees 5, 3, 3, 3)', 'four odd vertices: no Euler trail']] }
  ]
};
