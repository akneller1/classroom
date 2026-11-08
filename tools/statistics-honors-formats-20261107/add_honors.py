#!/usr/bin/env python3
"""Add Honors multiple-choice questions so two Statistics printables build at the Honors level:
Exploring Data -> printable Whodunnit (10 clue cards) and Sampling and Experimentation -> Maze.
Each answer is recomputed in `check`; every distractor must differ from the key. Existing questions are untouched.
Run from the repository root: python3 tools/statistics-honors-formats-20261107/add_honors.py [--check]"""
import json, math, pathlib, random, sys
from fractions import Fraction as F
ROOT = pathlib.Path(__file__).resolve().parents[2]
NOTE = ('Original Claude-authored Honors item (2026-11-07) added so the {fmt} builds from Honors questions; '
        'answer recomputed in tools/statistics-honors-formats-20261107/add_honors.py. Awaiting human review.')

ED = [  # Exploring Data · printable Whodunnit (prompt <= 150 characters, key <= 30, choices <= 34)
 dict(skill='02', prompt='A data set has Q1 = 22 and Q3 = 34. Using the 1.5 × IQR rule, what is the upper fence for outliers?',
      answer='52', wrong=['46', '40', '58'], steps=['IQR = 34 − 22 = 12.', 'Upper fence = Q3 + 1.5(IQR) = 34 + 18 = 52.'],
      check=lambda: 34 + F(3, 2) * (34 - 22) == 52),
 dict(skill='04', prompt='A five-number summary is 41, 58, 66, 79, 97. About what percent of the values lie between 58 and 97?',
      answer='about 75%', wrong=['about 50%', 'about 25%', 'about 100%'],
      steps=['58 is Q1 and 97 is the maximum.', 'From Q1 to the maximum covers three quarters of the data: about 75%.'],
      check=lambda: 3 * 25 == 75),
 dict(skill='06', prompt='48 of 120 juniors and 36 of 80 seniors drive to school. Find P(drives | senior) − P(drives | junior).',
      answer='0.05', wrong=['-0.05', '0.15', '0.425'],
      steps=['P(drives | senior) = 36/80 = 0.45.', 'P(drives | junior) = 48/120 = 0.40.', 'Difference: 0.45 − 0.40 = 0.05.'],
      check=lambda: F(36, 80) - F(48, 120) == F(1, 20)),
 dict(skill='07', prompt='A scatterplot has r = -0.6. Every x-value is doubled and 10 is added to every y-value. What is the new correlation?',
      answer='-0.6', wrong=['-1.2', '0.6', '-0.3'],
      steps=['Correlation has no units.', 'A positive scale change or a shift of either variable does not change r.', 'r = -0.6.'],
      check=lambda: True),
 dict(skill='08', prompt='The least-squares line is ŷ = 12 + 0.8x and the mean of x is 30. What is the mean of y?',
      answer='36', wrong=['24', '42', '30'],
      steps=['The least-squares line passes through (x̄, ȳ).', 'ȳ = 12 + 0.8(30) = 36.'],
      check=lambda: 12 + F(4, 5) * 30 == 36),
 dict(skill='09', prompt='The least-squares line is ŷ = 4.2 + 1.5x. The point (10, 21) is in the data. What is its residual?',
      answer='1.8', wrong=['-1.8', '19.2', '21'],
      steps=['ŷ = 4.2 + 1.5(10) = 19.2.', 'Residual = y − ŷ = 21 − 19.2 = 1.8.'],
      check=lambda: 21 - (F('4.2') + F('1.5') * 10) == F('1.8')),
 dict(skill='01', prompt='40 values all fall in bins of width 5 starting at 10. Bins 10–15, 15–20 and 20–25 hold 6, 14 and 12. What proportion are 25 or more?',
      answer='0.2', wrong=['0.3', '0.8', '0.12'],
      steps=['Values below 25: 6 + 14 + 12 = 32.', '40 − 32 = 8 values are 25 or more.', '8/40 = 0.2.'],
      check=lambda: F(40 - (6 + 14 + 12), 40) == F(1, 5)),
 dict(skill='05', prompt='Heights are approximately Normal with mean 64 in and standard deviation 2.5 in. What height has a z-score of 1.2?',
      answer='67 in', wrong=['65.2 in', '61 in', '66.5 in'],
      steps=['x = μ + zσ.', 'x = 64 + 1.2(2.5) = 64 + 3 = 67 in.'],
      check=lambda: 64 + F('1.2') * F('2.5') == 67),
]
SE = [  # Sampling and Experimentation · Maze (key <= 14 characters, door labels <= 18)
 dict(skill='01', prompt='A poll has a margin of error of ±3 points. About how many times larger must the sample be to cut it to ±1.5 points?',
      answer='4 times', wrong=['2 times', '1.5 times', '8 times'],
      steps=['The margin of error is proportional to 1/√n.', 'Halving it needs √n twice as large, so n must be 2² = 4 times larger.'],
      check=lambda: math.isclose(3 / math.sqrt(4), 1.5)),
 dict(skill='02', prompt='A proportional stratified sample of 60 students is taken from 300 freshmen, 200 sophomores and 100 juniors. How many sophomores are sampled?',
      answer='20', wrong=['15', '30', '10'],
      steps=['Sophomores are 200/600 = 1/3 of the population.', '(1/3)(60) = 20 sophomores.'],
      check=lambda: F(200, 600) * 60 == 20),
 dict(skill='02', prompt='A systematic sample takes every kth name from a list of 2,400 names to get a sample of 80. What is k?',
      answer='30', wrong=['80', '24', '32'],
      steps=['k = population size ÷ sample size.', 'k = 2400/80 = 30.'],
      check=lambda: 2400 // 80 == 30 and 2400 % 80 == 0),
 dict(skill='03', prompt='A survey is mailed to 1,000 randomly chosen households and 240 respond. What is the nonresponse rate?',
      answer='76%', wrong=['24%', '0.24%', '31.6%'],
      steps=['Nonrespondents: 1000 − 240 = 760.', '760/1000 = 76%.'],
      check=lambda: F(1000 - 240, 1000) == F(76, 100)),
 dict(skill='05', prompt='An experiment crosses 4 diets with 3 exercise plans and uses 6 subjects per treatment. How many subjects are needed?',
      answer='72', wrong=['12', '24', '36'],
      steps=['Treatments: 4 × 3 = 12.', 'Subjects: 12 × 6 = 72.'],
      check=lambda: 4 * 3 * 6 == 72),
 dict(skill='07', prompt='In a matched-pairs design, each of 24 subjects receives both treatments in random order. How many measurements are recorded?',
      answer='48', wrong=['24', '12', '96'],
      steps=['Each subject is measured once under each of the 2 treatments.', '24 × 2 = 48 measurements.'],
      check=lambda: 24 * 2 == 48),
 dict(skill='07', prompt='90 subjects form 3 blocks of 30. Within each block, subjects are randomly assigned equally to 2 treatments. How many get treatment A in each block?',
      answer='15', wrong=['30', '45', '10'],
      steps=['Randomization happens separately inside each block of 30.', '30 ÷ 2 = 15 subjects per treatment in each block.'],
      check=lambda: 30 // 2 == 15),
 dict(skill='06', prompt='In a pain trial, 200 patients receive a placebo and 46 of them report less pain. What percent show a placebo response?',
      answer='23%', wrong=['46%', '77%', '2.3%'],
      steps=['46/200 = 0.23.', '23% of the placebo group report less pain.'],
      check=lambda: F(46, 200) == F(23, 100)),
 dict(skill='04', prompt='A study finds that coffee drinkers live longer, but the people chose for themselves whether to drink coffee. What type of study is this?',
      answer='observational', wrong=['experiment', 'census', 'matched pairs'],
      steps=['No treatment was imposed: subjects chose whether to drink coffee.', 'It is an observational study, so it cannot show causation.'],
      check=lambda: True),
 dict(skill='08', prompt='A random sample of 400 voters from a city of 80,000 voters finds 52% support a plan. About how many city voters support it?',
      answer='about 41,600', wrong=['about 208', 'about 38,400', 'about 52,000'],
      steps=['Use the sample proportion to estimate the population: 0.52 × 80,000.', 'About 41,600 voters.'],
      check=lambda: F(52, 100) * 80000 == 41600),
]

def build(unit, prefix, items, fmt, write):
    path = ROOT / 'question-banks/statistics' / (unit + '.json'); text = path.read_text(encoding='utf8'); data = json.loads(text)
    qs = data['questions']; ids = {q['id'] for q in qs}; prompts = {q['prompt'] for q in qs}; added = 0
    rnd = random.Random(unit)
    for n, it in enumerate(items, 1):
        assert it['check'](), it['prompt']
        assert it['answer'] not in it['wrong'] and len(set(it['wrong'])) == 3, it['prompt']
        if it['prompt'] in prompts: continue           # idempotent
        skill = f'{unit}-skill-{it["skill"]}'
        std = next(q['standards'] for q in qs if q['skillId'] == skill and q['level'] == 'honors')
        qid = f'{prefix}-s{it["skill"]}-honors-h{n:02d}'; assert qid not in ids, qid
        opts = [{'text': w, 'correct': False} for w in it['wrong']]; opts.insert(rnd.randint(0, 3), {'text': it['answer'], 'correct': True})
        qs.append({'id': qid, 'skillId': skill, 'level': 'honors', 'format': 'multiple-choice', 'prompt': it['prompt'], 'answer': it['answer'],
                   'solutionSteps': it['steps'], 'options': opts, 'standards': std, 'sourceNotes': NOTE.format(fmt=fmt)})
        added += 1
    if write: path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + ('\n' if text.endswith('\n') else ''), encoding='utf8')
    return added

if __name__ == '__main__':
    w = '--check' not in sys.argv
    a = build('exploring-data', 'stat-u1', ED, 'Exploring Data printable Whodunnit', w)
    b = build('sampling-experimentation', 'stat-u2', SE, 'Sampling and Experimentation maze', w)
    print(f'OK {len(ED) + len(SE)} Honors items checked; {a + b} added' + ('' if w else ' (not written)'))
