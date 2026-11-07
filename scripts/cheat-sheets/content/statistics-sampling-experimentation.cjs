/* Statistics Unit 2 cheat sheet (Sampling and Experimentation). Every worked example is checked by build.cjs. */
module.exports = {
  name: 'statistics-sampling-experimentation', course: 'Statistics', unitNo: 2, unitName: 'Sampling and Experimentation',
  focus: 'populations and samples, random sampling methods and sources of bias',
  morefocus: 'observational studies, experiments, experimental designs and the scope of inference',
  front: [
    { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
      ['population', 'The entire group we want information about.', 'all 1,200 students at a school'],
      ['sample', 'The part of the population we actually measure.', '80 students surveyed'],
      ['census', 'Data from every member of the population.', 'asking all 1,200'],
      ['parameter', 'A number describing the population (usually unknown).', '⟨p⟩, ⟨\\mu⟩'],
      ['statistic', 'A number computed from a sample.', '⟨\\hat{p}⟩, ⟨\\bar{x}⟩']] },
    { title: 'Sampling Methods', color: 'blue', kind: 'table', plain: true, head: ['Method', 'How it works'], rows: [
      ['<b>Simple random (SRS)</b>', 'every group of ⟨n⟩ is equally likely to be chosen'],
      ['<b>Stratified</b>', 'split into similar groups (strata); take an SRS from <i>each</i>'],
      ['<b>Cluster</b>', 'split into groups that each look like the population; take <i>all</i> of a few groups'],
      ['<b>Systematic</b>', 'random start, then every ⟨k⟩th individual'],
      ['<span class="no">Convenience / voluntary</span>', 'easy-to-reach or self-selected people: biased']] },
    { title: 'Choosing an SRS with Random Digits', color: 'green', kind: 'example', text: 'Label every individual with the same number of digits, read pairs from the table, skip out-of-range numbers and repeats.',
      example: 'Pick 3 of 40 students (label 01–40). Digits: 07 51 40 13 07 22', steps: [['Read pairs:', '07 ✔, 51 skip (&gt; 40), 40 ✔, 13 ✔'], ['Stop:', 'we have 3 students']],
      answer: 'students 07, 40 and 13',
      check: { true: "(() => { const out = []; [7, 51, 40, 13, 7, 22].forEach(d => { if (d >= 1 && d <= 40 && !out.includes(d) && out.length < 3) out.push(d); }); return out.join() === '7,40,13'; })()" } },
    { title: 'Stratified or Cluster?', color: 'orange', kind: 'words', rows: [
      ['Survey 20 freshmen, 20 sophomores, 20 juniors, 20 seniors (random within each grade)', 'stratified'],
      ['Randomly choose 4 homerooms and survey everyone in them', 'cluster'],
      ['Number all students and pick 80 with a random generator', 'SRS'],
      ['Survey every 15th student entering, starting at a random one of the first 15', 'systematic']],
      check: { num: '4*20', is: 80 } },
    { title: 'Sources of Bias', color: 'pink', kind: 'table', plain: true, head: ['Bias', 'Example'], rows: [
      ['<b>Undercoverage</b>: some groups left out of the frame', 'phone survey misses people with no phone'],
      ['<b>Nonresponse</b>: chosen people don’t answer', 'only 30% return a mailed survey'],
      ['<b>Response bias</b>: answers are not truthful', 'asking about cheating face to face'],
      ['<b>Wording</b>: the question pushes an answer', '“Don’t you agree that …?”']],
      after: 'A bigger sample does <b>not</b> fix bias; random selection does.' },
    { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
      good: ['Name the population and the sample in context.', 'Describe the random method well enough to repeat it.', 'Say the <i>direction</i> of bias (over- or underestimate).'],
      bad: [['“Random” = haphazard', 'use a random number generator or table'], ['Stratified = cluster', 'strata are similar inside; clusters are mini-populations'], ['Large sample removes bias', 'it only reduces variability']] }
  ],
  back: [
    { title: 'Observational Study or Experiment?', color: 'purple', kind: 'table', plain: true, head: ['Type', 'What happens'], rows: [
      ['<b>Observational study</b>', 'observe and measure; no treatment is imposed. Shows association only.'],
      ['<b>Experiment</b>', 'deliberately impose treatments on units. With random assignment it can show <b>cause and effect</b>.']],
      after: '<b>Confounding</b>: two variables whose effects on the response cannot be separated (e.g. coffee drinkers also smoke more).' },
    { title: 'Experiment Vocabulary', color: 'blue', kind: 'vocab', rows: [
      ['experimental units', 'Who or what receives the treatments.', '60 tomato plants'],
      ['factor / levels', 'Explanatory variable / its values.', 'fertilizer: 0, 5, 10 g'],
      ['treatment', 'A specific condition applied.', '5 g of fertilizer'],
      ['response variable', 'The outcome measured.', 'plant height'],
      ['placebo', 'A fake treatment with no active ingredient.', 'sugar pill']] },
    { title: 'Principles of Experimental Design', color: 'green', kind: 'table', plain: true, rows: [
      ['<b>Comparison</b>', 'compare two or more treatments (often a control group)'],
      ['<b>Random assignment</b>', 'assign treatments by chance so groups are alike'],
      ['<b>Control</b>', 'keep other variables the same for every group'],
      ['<b>Replication</b>', 'use enough units in each group']],
      after: '<b>Blinding</b>: single-blind (subjects don’t know), double-blind (subjects <i>and</i> evaluators don’t know).' },
    { title: 'Designs', color: 'orange', kind: 'table', plain: true, head: ['Design', 'How units get treatments'], rows: [
      ['<b>Completely randomized</b>', 'all units randomly assigned to treatments'],
      ['<b>Randomized block</b>', 'group similar units into blocks (e.g. by gender), then randomize within each block'],
      ['<b>Matched pairs</b>', 'pairs of similar units, or each unit gets both treatments in random order']],
      after: 'Block to reduce variability from a variable you <i>know</i> affects the response.' },
    { title: 'Counting Treatments', color: 'pink', kind: 'example', text: 'Number of treatments = product of the number of levels of each factor.',
      example: '3 doses × 2 times of day; 60 volunteers', steps: [['Treatments:', '⟨3 \\times 2 = 6⟩'], ['Per group:', '⟨60 \\div 6 = 10⟩'], ['Assign:', 'number 1–60, randomly pick 10 for each treatment']],
      answer: '6 treatments, 10 volunteers each',
      check: [{ num: '3*2', is: 6 }, { num: '60/6', is: 10 }] },
    { title: 'Scope of Inference', color: 'teal', kind: 'table', head: ['', 'Random assignment', 'No random assignment'], rows: [
      ['<b>Random sample</b>', 'cause and effect; generalize to population', 'association only; generalize'],
      ['<b>Not random sample</b>', 'cause and effect for these subjects only', 'association, these subjects only']],
      after: '<span class="no">✘</span> Correlation is not causation. <span class="ok">✔</span> Random <i>sampling</i> → generalize; random <i>assignment</i> → causation.' }
  ]
};
