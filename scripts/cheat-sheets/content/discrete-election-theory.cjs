/* Discrete Math Unit 9 cheat sheet (Election Theory). Every tally, index and apportionment is recomputed by the checks. */
const S = [[14, 'ABC'], [10, 'CBA'], [8, 'BCA'], [3, 'CAB']];
const first = x => S.filter(r => r[1][0] === x).reduce((a, r) => a + r[0], 0);
const borda = x => S.reduce((a, r) => a + r[0] * (3 - r[1].indexOf(x)), 0);
const h2h = (x, y) => S.filter(r => r[1].indexOf(x) < r[1].indexOf(y)).reduce((a, r) => a + r[0], 0);
const banz = (q, w) => { const c = w.map(() => 0); for (let m = 1; m < 1 << w.length; m++) { const s = w.reduce((t, x, i) => t + (m >> i & 1 ? x : 0), 0); if (s >= q) w.forEach((x, i) => { if (m >> i & 1 && s - x < q) c[i]++; }); } return c; };
const ham = (p, n) => { const T = p.reduce((a, b) => a + b), q = p.map(x => x * n / T), a = q.map(Math.floor), left = n - a.reduce((x, y) => x + y); q.map((x, i) => [x - a[i], i]).sort((x, y) => y[0] - x[0]).slice(0, left).forEach(([, i]) => a[i]++); return a; };
module.exports = {
  name: 'discrete-election-theory', course: 'Discrete Math', unitNo: 9, unitName: 'Election Theory',
  focus: 'preference schedules and four named voting methods, fairness criteria',
  morefocus: 'weighted voting, coalitions and power, fair division and apportionment',
  front: [
    { title: 'Preference Schedule', color: 'purple', kind: 'table', head: ['Voters', '14', '10', '8', '3'], rows: [['1st', 'A', 'C', 'B', 'C'], ['2nd', 'B', 'B', 'C', 'A'], ['3rd', 'C', 'A', 'A', 'B']],
      after: '35 voters, so a <b>majority</b> is 18 (more than half). First-place votes: A 14, C 13, B 8 — no majority.',
      check: [{ num: first('A'), is: 14 }, { num: first('C'), is: 13 }, { num: first('B'), is: 8 }] },
    { title: 'Four Methods, Four Winners?', color: 'blue', kind: 'table', plain: true, head: ['Method (rule)', 'Result for the schedule'], rows: [
      ['<b>Plurality</b>: most first-place votes', 'A (14)'],
      ['<b>Borda</b>: 3, 2, 1 points', 'A 66, <b>B 75</b>, C 69'],
      ['<b>Plurality with elimination</b>: drop the fewest first places', 'drop B (8 → C): <b>C</b> 21–14'],
      ['<b>Pairwise comparisons</b>: 1 point per head-to-head win', 'B beats A 18–17 and C 22–13: <b>B</b>']],
      after: 'Name the method <b>and</b> the tie-breaking rule before counting.',
      check: [{ num: borda('A'), is: 66 }, { num: borda('B'), is: 75 }, { num: borda('C'), is: 69 }, { num: h2h('B', 'A'), is: 18 }, { num: h2h('B', 'C'), is: 22 }, { num: first('C') + 8, is: 21 }] },
    { title: 'Fairness Criteria', color: 'green', kind: 'table', plain: true, head: ['Criterion', 'Says', 'Can fail under'], rows: [
      ['majority', 'a majority candidate wins', 'Borda'], ['Condorcet', 'a candidate who wins every head-to-head wins', 'plurality, Borda, elimination'],
      ['monotonicity', 'gaining support never hurts a winner', 'plurality with elimination'], ['independence of irrelevant alternatives', 'removing a loser does not change the winner', 'all four methods']],
      after: '<b>Arrow\'s theorem:</b> with 3 or more candidates no ranked method satisfies every fairness condition.' },
    { title: 'Condorcet Check', color: 'orange', kind: 'example', text: 'Compare every pair head-to-head.',
      example: 'Schedule above', steps: [['A vs B:', '17–18 (B)'], ['A vs C:', '14–21 (C)'], ['B vs C:', '22–13 (B)']], answer: 'B is the Condorcet winner; plurality (A) and elimination (C) violate the Condorcet criterion',
      check: [{ num: h2h('A', 'B'), is: 17 }, { num: h2h('A', 'C'), is: 14 }] },
    { title: 'Weighted Voting', color: 'pink', kind: 'table', plain: true, head: ['Term', 'In [6: 4, 3, 2]'], rows: [
      ['quota ⟨q⟩: more than half the total, at most the total', 'total 9: valid quotas 5 to 9'], ['dictator: weight ≥ quota', 'none'], ['veto power: others total < quota', 'P1 (3 + 2 = 5 < 6)'],
      ['dummy: never critical', 'none'], ['winning coalitions', '{P1, P2}, {P1, P3}, {P1, P2, P3}']],
      check: { num: '3+2', is: 5 } },
    { title: 'Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Majority means more than half.', 'Borda uses every position on every ballot.', 'Keep eliminating until someone has a majority.'],
      bad: [['Plurality = majority', 'a plurality can be under half'], ['Largest weight = dictator', 'needs weight ≥ quota'], ['Power ∝ weight', 'count critical appearances']] }
  ],
  back: [
    { title: 'Banzhaf Power Index', color: 'purple', kind: 'example', text: 'Count how often each player is <b>critical</b> (its removal turns a winning coalition into a losing one), then divide by the total.',
      example: '[6: 4, 3, 2]', steps: [['Critical:', 'P1 in all three coalitions; P2 in {P1, P2}; P3 in {P1, P3}'], ['Counts:', '3, 1, 1 (total 5)']], answer: '⟨\\tfrac35, \\tfrac15, \\tfrac15⟩',
      check: { true: '"' + banz(6, [4, 3, 2]).join() + '" === "3,1,1"' } },
    { title: 'Fair Division', color: 'blue', kind: 'table', plain: true, head: ['Method', 'How it works'], rows: [
      ['divider-chooser (2)', 'one cuts two pieces equal to them; the other chooses'], ['lone divider (N)', 'divider cuts N pieces; choosers bid; standoffs recombined'],
      ['sealed bids (items)', 'highest bid wins; cash settles fair shares; surplus split'], ['markers (items in a row)', 'markers split the row into N equal-value segments']],
      after: 'A <b>fair share</b> is worth at least ⟨\\tfrac1N⟩ of the total <b>in that player\'s own opinion</b>.' },
    { title: 'Sealed Bids Example', color: 'green', kind: 'example', text: 'Two heirs; house and car.',
      example: 'Ann bids house $300, car $120; Ben bids house $240, car $180.', steps: [['Items:', 'Ann gets the house, Ben the car'], ['Fair shares:', 'Ann $210, Ben $210'], ['Settle:', 'Ann owes $90; Ben is owed $30; surplus $60 split']], answer: 'Ann pays $60 to Ben',
      check: [{ num: '(300+120)/2', is: 210 }, { num: '300-210', is: 90 }, { num: '210-180', is: 30 }, { num: '90-30', is: 60 }, { num: '90-30', is: 60 }, { num: '90-60/2', is: 60 }] },
    { title: 'Apportionment Methods', color: 'orange', kind: 'table', plain: true, head: ['Method', 'Rule'], rows: [
      ['standard divisor', '⟨SD = \\tfrac{\\text{total population}}{\\text{seats}}⟩; quota = population ÷ SD'],
      ['Hamilton', 'round quotas down, then give leftover seats by largest remainder'], ['Jefferson', 'modified divisor; round <b>down</b>'],
      ['Webster', 'modified divisor; round to <b>nearest</b>'], ['Adams', 'modified divisor; round <b>up</b>']] },
    { title: 'Hamilton Example', color: 'pink', kind: 'example', text: 'Towns 450, 330, 220; 10 seats.',
      example: '⟨SD = 100⟩: quotas 4.5, 3.3, 2.2', steps: [['Lower quotas:', '4, 3, 2 = 9 seats'], ['Leftover 1 seat:', 'largest remainder 0.5']], answer: '5, 3, 2',
      check: { true: '"' + ham([450, 330, 220], 10).join() + '" === "5,3,2"' } },
    { title: 'Paradoxes and Challenge', color: 'teal', kind: 'html',
      html: '<b>Alabama paradox</b>: more seats, a state loses one. Hamilton with populations 130, 690, 410: 13 seats → 2, 7, 4; 14 seats → <b>1</b>, 8, 5. <b>Population</b> and <b>new-states</b> paradoxes also affect Hamilton; divisor methods avoid them but can violate the quota rule (Balinski–Young: no method does everything).',
      check: [{ true: '"' + ham([130, 690, 410], 13).join() + '" === "2,7,4"' }, { true: '"' + ham([130, 690, 410], 14).join() + '" === "1,8,5"' }] }
  ]
};
