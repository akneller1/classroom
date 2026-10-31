const F = require('../figs.cjs');
const N = x => Math.exp(-x * x / 2) / Math.sqrt(2 * Math.PI) * 8;
module.exports = {
  name: 'probability-statistics', course: 'Algebra 2', unitNo: 11, unitName: 'Probability & Statistics',
  focus: 'counting, permutations, combinations, independent and dependent events, and conditional probability',
  morefocus: 'probability distributions, expected value, normal distributions, z-scores and sampling',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['sample space', 'The set of all possible outcomes.', '{H, T}'], ['permutation', 'An arrangement where order matters.', 'president, VP'],
      ['combination', 'A selection where order does not matter.', 'a 3-person team'], ['independent', 'One event does not change the other’s probability.', 'two dice'],
      ['conditional probability', '⟨P(A \\mid B)⟩: probability of ⟨A⟩ given ⟨B⟩ happened.', '⟨\\tfrac{P(A \\cap B)}{P(B)}⟩']] },
    { title: 'Counting & Permutations', color: 'blue', kind: 'words', rows: [
      ['Counting principle: 4 shirts, 3 pants, 2 shoes', '⟨4 \\cdot 3 \\cdot 2 = 24⟩'], ['⟨_nP_r = \\dfrac{n!}{(n - r)!}⟩: 1st, 2nd, 3rd from 8 runners', '⟨_8P_3 = 336⟩'],
      ['Arrange all letters of BOOK (O repeats)', '⟨\\tfrac{4!}{2!} = 12⟩'], ['Seat 5 people in a row', '⟨5! = 120⟩']],
      check: { list: ['4*3*2', '8*7*6', '24/2', '5*4*3*2'], is: [24, 336, 12, 120] } },
    { title: 'Combinations', color: 'green', kind: 'example', text: '⟨_nC_r = \\dfrac{n!}{r!(n - r)!}⟩. Multiply when choosing from separate groups.',
      example: 'A committee of 3 from 7 boys and 5 girls with exactly 2 girls.', steps: [['Girls:', '⟨_5C_2 = 10⟩'], ['Boys:', '⟨_7C_1 = 7⟩']], answer: '⟨10 \\cdot 7 = 70⟩ committees',
      check: { list: ['5*4/2', '7'], is: [10, 7] } },
    { title: 'Independent & Dependent', color: 'orange', kind: 'words', rows: [
      ['Independent: ⟨P(A \\text{ and } B) = P(A) \\cdot P(B)⟩. Two heads in a row', '⟨\\tfrac{1}{4}⟩'], ['Dependent: 2 red without replacement from 5 red, 3 blue: ⟨\\tfrac{5}{8} \\cdot \\tfrac{4}{7}⟩', '⟨\\tfrac{5}{14}⟩'],
      ['Or: ⟨P(A \\text{ or } B) = P(A) + P(B) - P(A \\text{ and } B)⟩. King or heart', '⟨\\tfrac{4 + 13 - 1}{52} = \\tfrac{4}{13}⟩']],
      check: { list: ['0.5*0.5', '5/8*4/7', '16/52'], is: [0.25, 5 / 14, 4 / 13] } },
    { title: 'Conditional Probability', color: 'pink', kind: 'table', head: ['', 'Sport', 'No sport', 'Total'], rows: [
      ['Juniors', '18', '12', '30'], ['Seniors', '20', '10', '30'], ['Total', '38', '22', '60']],
      after: '⟨P(\\text{sport} \\mid \\text{junior}) = \\tfrac{18}{30} = \\tfrac{3}{5}⟩, but ⟨P(\\text{junior} \\mid \\text{sport}) = \\tfrac{18}{38} = \\tfrac{9}{19}⟩. The condition is the denominator.',
      check: { list: ['18/30', '18/38', '18+20', '12+10'], is: [0.6, 9 / 19, 38, 22] } },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Ask “does order matter?” before choosing ⟨P⟩ or ⟨C⟩.', 'Probabilities are between 0 and 1 and the sample space sums to 1.', '“At least one” = ⟨1 - P(\\text{none})⟩.'],
      bad: [['⟨P(A \\mid B) = P(B \\mid A)⟩', 'usually different denominators'], ['Adding for “and”', 'multiply for “and”, add for “or”'], ['Forgetting to subtract the overlap', '⟨P(A \\text{ or } B)⟩ subtracts ⟨P(A \\text{ and } B)⟩']] }
  ],
  back: [
    { title: 'Probability Distributions', color: 'purple', kind: 'table', head: ['Heads in 3 flips ⟨X⟩', '0', '1', '2', '3'], rows: [['⟨P(X)⟩', '⟨\\tfrac{1}{8}⟩', '⟨\\tfrac{3}{8}⟩', '⟨\\tfrac{3}{8}⟩', '⟨\\tfrac{1}{8}⟩']],
      after: 'Each ⟨P \\ge 0⟩ and they sum to 1. Binomial: ⟨P(k) = {}_nC_k\\, p^k (1 - p)^{n - k}⟩. Exactly 4 of 5 free throws at ⟨p = 0.7⟩: ⟨5(0.7)^4(0.3) \\approx 0.360⟩.',
      check: [{ num: '1/8+3/8+3/8+1/8', is: 1 }, { num: 'Math.round(5*0.7**4*0.3*1000)/1000', is: 0.36 }] },
    { title: 'Expected Value', color: 'blue', kind: 'example', text: '⟨E(X) = \\sum x \\cdot P(x)⟩: the long-run average per trial. A fair game has ⟨E = 0⟩.',
      example: 'Pay $2 to roll a die; win $10 on a 6.', steps: [['Net:', '⟨+8⟩ with ⟨\\tfrac{1}{6}⟩, ⟨-2⟩ with ⟨\\tfrac{5}{6}⟩'], ['⟨E⟩:', '⟨\\tfrac{8}{6} - \\tfrac{10}{6} = -\\tfrac{1}{3}⟩']], answer: 'lose about $0.33 per game',
      check: { num: '8/6-10/6', is: -1 / 3 } },
    { title: 'Normal Distributions', color: 'green', kind: 'html', html: 'Bell-shaped and symmetric about the mean ⟨\\mu⟩. Empirical rule: about <b>68%</b> within ⟨1\\sigma⟩, <b>95%</b> within ⟨2\\sigma⟩, <b>99.7%</b> within ⟨3\\sigma⟩.',
      fig: F.plane({ id: 'nd', xmin: -3.5, xmax: 3.5, ymin: -0.6, ymax: 3.6, size: 2.7, grid: false, fns: [{ f: N }], vlines: [{ x: -1, color: '#16a34a' }, { x: 1, color: '#16a34a' }, { x: -2, color: '#999' }, { x: 2, color: '#999' }],
        labels: [{ x: 0, y: 1.2, t: '68%', color: '#16a34a' }, { x: 0, y: 0.35, t: '95%', color: '#666' }, { x: -2, y: -0.45, t: 'μ−2σ', bold: false, fs: 8 }, { x: -1, y: -0.45, t: 'μ−σ', bold: false, fs: 8 }, { x: 0, y: -0.45, t: 'μ', bold: false }, { x: 1, y: -0.45, t: 'μ+σ', bold: false, fs: 8 }, { x: 2, y: -0.45, t: 'μ+2σ', bold: false, fs: 8 }] }) },
    { title: 'z-Scores', color: 'orange', kind: 'example', text: '⟨z = \\dfrac{x - \\mu}{\\sigma}⟩: how many standard deviations from the mean.',
      example: 'Scores: ⟨\\mu = 70⟩, ⟨\\sigma = 8⟩. A student scores 86.', steps: [['⟨z⟩:', '⟨\\tfrac{86 - 70}{8} = 2⟩'], ['Rule:', '95% within ⟨\\pm 2⟩, so 2.5% above']], answer: 'about 97.5% scored lower',
      check: { list: ['(86-70)/8', '50+95/2'], is: [2, 97.5] } },
    { title: 'Sampling & Studies', color: 'pink', kind: 'table', plain: true, rows: [
      ['Survey', 'asks a sample; random sampling avoids bias'], ['Observational study', 'observes without assigning treatments: no cause and effect'], ['Experiment', 'randomly assigns treatments: can show cause and effect'],
      ['Margin of error', '⟨\\approx \\pm\\tfrac{1}{\\sqrt{n}}⟩: ⟨n = 400⟩ gives ⟨\\pm 5\\%⟩']], check: { num: '1/Math.sqrt(400)', is: 0.05 } },
    { title: 'Using a Sample', color: 'teal', kind: 'example', text: 'A sample proportion estimates the population proportion; report it with its margin of error.',
      example: '240 of 400 randomly chosen voters support a measure.', steps: [['Proportion:', '⟨\\tfrac{240}{400} = 60\\%⟩'], ['Interval:', '⟨60\\% \\pm 5\\%⟩']], answer: 'likely between 55% and 65%',
      check: { list: ['240/400', '1/Math.sqrt(400)'], is: [0.6, 0.05] } }
  ]
};
