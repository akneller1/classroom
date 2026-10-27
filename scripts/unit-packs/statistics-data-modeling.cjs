/* Unit 12 · Statistics and Data Modeling: unit pack content (see build.cjs). */
'use strict';
const T = (rows) => '<table>' + rows.map((r, i) => '<tr>' + r.map((c, k) => (i && k ? '<td>' : '<th>') + c + (i && k ? '</td>' : '</th>')).join('') + '</tr>').join('') + '</table>';
module.exports = {
  unit: 'statistics-data-modeling', unitNo: 12, unitName: 'Statistics and Data Modeling', course: 'Algebra 1',

  mystery: {
    skills: 'mean, median, mode, range, IQR and outliers, two-way tables, lines of fit and residuals.',
    slug: 'stadium-scoreboard-scandal', title: 'The Stadium Scoreboard Scandal', eyebrow: 'Case file No. 12',
    tagline: 'The championship trophy vanished from Riverside Stadium at halftime. Solve each problem to earn a clue.',
    palette: { navy: '#10283a', accent: '#4fd1a5' },
    labels: { p: 'The Suspects', l: 'The Places', m: 'The Methods' },
    placeholder: 'Your answer', inputHint: 'Type a number like 8.5. For a percent, type the number, like 24 or 24%.', symbols: [],
    intro: [
      'It was the championship game at <b>Riverside Stadium</b>. At halftime the band marched, the fans cheered, and when the lights came back up, the <b>championship trophy</b> was gone from its stand at midfield!',
      'Six people were near the field, each seen in a different spot, and there are six ways the trophy could have been sneaked out. You are the lead detective. Find out <b>who</b> took it, <b>where</b> they were, and <b>how</b> they did it.'
    ],
    suspects: [
      { name: 'Coach Diaz', role: 'Home Team Coach', skin: '#c68a5b', hair: 'short', hairColor: '#1d1d1d', color: '#1f7a4d', bg: '#d3f1ea', acc: 'cap' },
      { name: 'Riley Shaw', role: 'Team Statistician', skin: '#f4d3b5', hair: 'long', hairColor: '#b5651d', color: '#2b3a8c', bg: '#dbe2fb', acc: 'glasses' },
      { name: 'Mr. Benton', role: 'Rival Team Owner', skin: '#e0ac7e', hair: 'bald', hairColor: '#1d1d1d', color: '#8a2b2b', bg: '#f6d9d9', acc: 'bowtie' },
      { name: 'Jada Brooks', role: 'Band Leader', skin: '#8d5a3b', hair: 'bun', hairColor: '#15151a', color: '#7a3fb0', bg: '#e8d9f5', acc: 'none' },
      { name: 'Sal Romano', role: 'Hot Dog Vendor', skin: '#f1c9a5', hair: 'short', hairColor: '#5a3a22', color: '#e4752a', bg: '#ffe3c9', acc: 'cap' },
      { name: 'Kim Tanaka', role: 'Sports Reporter', skin: '#f4d3b5', hair: 'long', hairColor: '#15151a', color: '#24406e', bg: '#d6e2f7', acc: 'none' }
    ],
    places: ['Locker Room', 'Press Box', 'Snack Stand', 'Band Section', 'Scoreboard Tower', 'Parking Lot'],
    methods: ['Hidden in a tuba case', 'Packed in a hot dog cart', 'Rolled out in an equipment bag', 'Dropped in a confetti cannon', 'Tucked under a team banner', 'Carried off on a golf cart'],
    culprit: { p: 2, l: 4, m: 2 },
    ending: 'At halftime <b>Mr. Benton</b>, the rival team owner, climbed into the <b>Scoreboard Tower</b> while everyone watched the band. He lowered the trophy into an <b>equipment bag</b> and rolled it out with the visiting team’s gear. The numbers never lie. Case closed, Mr. Benton!',
    questions: [
      { instr: 'Find the mean of the data:', tex: '4,\\ 8,\\ 6,\\ 10,\\ 7', answer: { t: 'num', v: '7' }, check: { num: '(4+8+6+10+7)/5', is: 7 },
        steps: ['Add: ⟨4 + 8 + 6 + 10 + 7 = 35⟩', 'Divide by 5: ⟨35 \\div 5 = 7⟩'], clue: { p: 0, l: 0, text: 'Coach Diaz was giving a halftime speech in the Locker Room. Forty players heard every word.' } },
      { instr: 'Find the median of the data:', tex: '12,\\ 5,\\ 9,\\ 3,\\ 15,\\ 8', answer: { t: 'num', v: '8.5' }, check: { num: '(8+9)/2', is: 8.5 },
        steps: ['Order: ⟨3, 5, 8, 9, 12, 15⟩', 'Two middle values: ⟨\\dfrac{8 + 9}{2} = 8.5⟩'], clue: { m: 0, text: 'The tuba case was on the field the whole halftime show. The tuba was inside it.' } },
      { instr: 'Find the range of the data:', tex: '22,\\ 17,\\ 30,\\ 11,\\ 25', answer: { t: 'num', v: '19' }, check: { num: '30-11', is: 19 },
        steps: ['Range = max − min', '⟨30 - 11 = 19⟩'], clue: { p: 1, l: 1, text: 'Riley Shaw was updating the stats in the Press Box. The broadcast camera shows her typing.' } },
      { instr: 'Find the mode of the data:', tex: '3,\\ 7,\\ 7,\\ 2,\\ 9,\\ 7,\\ 2', answer: { t: 'num', v: '7' }, check: { num: '7', is: 7 },
        steps: ['Count each value: 7 appears three times.', 'The mode is ⟨7⟩'], clue: { m: 1, text: 'The hot dog cart is too small. It barely holds the buns.' } },
      { instr: 'Find the interquartile range (IQR) of the data:', tex: '2,\\ 4,\\ 5,\\ 7,\\ 8,\\ 10,\\ 12,\\ 15', answer: { t: 'num', v: '6.5' }, check: { num: '(10+12)/2-(4+5)/2', is: 6.5 },
        steps: ['Lower half ⟨2, 4, 5, 7⟩: ⟨Q_1 = 4.5⟩. Upper half ⟨8, 10, 12, 15⟩: ⟨Q_3 = 11⟩', '⟨IQR = 11 - 4.5 = 6.5⟩'], clue: { p: 3, l: 3, text: 'Jada Brooks was leading the band in the Band Section. She never put down her baton.' } },
      { instr: 'Find the mode of the data:', tex: '2,\\ 4,\\ 4,\\ 6,\\ 8', answer: { t: 'num', v: '4' }, check: { num: '4', is: 4 },
        steps: ['Count the frequency of each value.', '4 appears twice, more than any other value.'], clue: { m: 3, text: 'The confetti cannons fired at halftime. Only confetti came out.' } },
      { instr: 'What percent of the 9th graders have a dog?', text: 'Survey of students:', html: T([['', 'Dog', 'No dog', 'Total'], ['8th grade', '12', '13', '25'], ['9th grade', '6', '19', '25']]), answer: { t: 'num', v: '24' }, check: { num: '6/25*100', is: 24 },
        steps: ['Use only the 9th grade row: 6 of 25.', '⟨\\dfrac{6}{25} = 0.24 = 24\\%⟩'], clue: { p: 4, l: 2, text: 'Sal Romano was selling hot dogs at the Snack Stand. The line was 30 people long all halftime.' } },
      { instr: 'The line of fit y = 2.5x + 10 models the data. Predict y when x = 8.', tex: 'y = 2.5(8) + 10', answer: { t: 'num', v: '30' }, check: { num: '2.5*8+10', is: 30 },
        steps: ['Substitute ⟨x = 8⟩: ⟨2.5(8) + 10⟩', '⟨20 + 10 = 30⟩'], clue: { m: 4, text: 'The team banner was flat on the field. Nothing was underneath.' } },
      { instr: 'A model predicts y = 3x + 4. At x = 9 the actual value is 34. Find the residual.', text: 'residual = actual − predicted', answer: { t: 'num', v: '3' }, check: { num: '34-(3*9+4)', is: 3 },
        steps: ['Predicted: ⟨3(9) + 4 = 31⟩', 'Residual: ⟨34 - 31 = 3⟩'], clue: { p: 5, l: 5, text: 'Kim Tanaka was interviewing fans in the Parking Lot. Her live report is on the news.' } },
      { instr: 'A data set has Q1 = 10 and Q3 = 18. Find the upper fence for outliers (Q3 + 1.5 · IQR).', text: 'upper fence = Q3 + 1.5(Q3 − Q1)', answer: { t: 'num', v: '30' }, check: { num: '18+1.5*(18-10)', is: 30 },
        steps: ['⟨IQR = 18 - 10 = 8⟩', '⟨18 + 1.5(8) = 18 + 12 = 30⟩'], clue: { m: 5, text: 'The golf cart’s battery was dead all night. It never moved.' } }
    ]
  },

  escape: {
    title: 'Escape the Stats Lab', emoji: '📊', endEmoji: '📊🏆',
    intro: 'Your class is visiting the sports Stats Lab when the computers glitch and lock every door! The lab only opens for people who can read data. Solve five rooms and get out in <b>30 minutes</b>, before the final buzzer.',
    finalStory: 'The exit has a five-letter keypad. A sticky note says: “Line up your key cards from the smallest stamp to the largest. The letters spell the password.”',
    finalAsk: 'Password?', word: 'GRAPH',
    outro: 'GRAPH! The door slides open and the scoreboard flashes your name. The head analyst nods: “You can read data like a pro.”',
    stages: [
      { name: 'The Data Wall', type: 'fields', stamp: 64, letter: 'P',
        story: 'A screen shows five game scores: 3, 5, 5, 7, 10. Enter the mean and the median to unlock it.',
        scene: { kind: 'svg', viewBox: '0 0 400 300', svg: '<rect x="70" y="60" width="260" height="150" rx="14" fill="#10283a" stroke="#4fd1a5" stroke-width="3"/><text x="200" y="100" text-anchor="middle" fill="#fff" font-size="18">GAME SCORES</text><text x="200" y="150" text-anchor="middle" fill="#4fd1a5" font-size="28" font-weight="700">3, 5, 5, 7, 10</text><text x="200" y="260" text-anchor="middle" font-size="48">🏀</text>' },
        title: 'Unlock the screen', prompt: '<p>Data: 3, 5, 5, 7, 10</p>', fields: [{ label: 'Mean =', answer: 6 }, { label: 'Median =', answer: 5 }], button: 'Unlock',
        hints: ['Mean: add them all and divide by how many.', '3 + 5 + 5 + 7 + 10 = 30, and 30 ÷ 5 = 6.', 'The median is the middle value of the ordered list.'], key: 'Mean = 6, median = 5.', check: [['(3+5+5+7+10)/5', 6], ['5', 5]] },
      { name: 'The Film Room', type: 'cipher', stamp: 18, letter: 'G',
        story: 'A coded message is paused on the game film. The shift is written somewhere in this room. Click things to search.',
        scene: { kind: 'emoji', bg: '#101a2e', floor: '#1f2b45', items: [{ e: '📺', x: 90, y: 150, s: 60, msg: 'The game film, paused.' }, { e: '📋', x: 300, y: 200, s: 50, clue: 'Clipboard:<br>Shift = the range of 4, 9, 2, 11', msg: 'A clipboard with a note!' }, { e: '🍿', x: 200, y: 215, s: 40, msg: 'Popcorn. Cold.' }, { e: '🏈', x: 210, y: 110, s: 44, msg: 'A football. Not a clue.' }] },
        plain: 'THE NEXT KEY IS UNDER THE SCOREBOARD', shift: 9, answer: 'SCOREBOARD', askLabel: 'Where is the next key?',
        hints: ['Click the clipboard.', 'Range = largest − smallest.', '11 − 2 = 9. Set the shift to 9.'], key: 'Range = 11 − 2 = 9. The message says THE NEXT KEY IS UNDER THE SCOREBOARD.', checkNum: ['11-2', 9] },
      { name: 'The Scatter Room', type: 'classify', stamp: 95, letter: 'H',
        story: 'Four scatter plots hang on the wall. Label the kind of correlation each one would show.',
        scene: { kind: 'emoji', bg: '#1d1530', floor: '#3a2b4a', items: [{ e: '📈', x: 70, y: 170, s: 54 }, { e: '📉', x: 160, y: 170, s: 54 }, { e: '❓', x: 250, y: 170, s: 54 }, { e: '🚗', x: 340, y: 170, s: 54 }], caption: 'which way does the data go?' },
        title: 'What kind of correlation?', prompt: '<p style="color:var(--dim)">As the first quantity goes up, what does the second do?</p>',
        items: ['Hours studied vs. test score', 'Outside temperature vs. hot cocoa sales', 'Shoe size vs. favorite number', 'Age of a car vs. its value'], options: ['Positive', 'Negative', 'No correlation'], answer: [0, 1, 2, 1],
        hints: ['Positive: both go up together. Negative: one goes up while the other goes down.', 'Warmer days mean less hot cocoa.', 'Shoe size has nothing to do with favorite numbers.'], key: 'Positive, negative, no correlation, negative.' },
      { name: 'The Box Plot Room', type: 'order', stamp: 33, letter: 'R',
        story: 'The computer wants the steps for finding the interquartile range, in order.',
        scene: { kind: 'emoji', bg: '#13261c', floor: '#2c4a2c', items: [{ e: '📦', x: 120, y: 170, s: 70, msg: 'A box. Get it? A box plot.' }, { e: '🧮', x: 290, y: 175, s: 50, msg: 'An abacus.' }], caption: 'put the steps in order' },
        title: 'Find the IQR', prompt: '<p>Place the steps from first to last.</p>',
        steps: ['Order the data from least to greatest', 'Find the median, which splits the data into two halves', 'Find Q1 and Q3, the medians of the lower and upper halves', 'Subtract: IQR = Q3 − Q1'],
        hints: ['You cannot find a middle until the data is in order.', 'The median comes before the quartiles.', 'Subtracting is the last step.'], key: 'Order; median; Q1 and Q3; IQR = Q3 − Q1.' },
      { name: 'The Exit Gate', type: 'fields', stamp: 47, letter: 'A', ui: 'dial',
        story: 'The gate shows a five-number summary: min 1, Q1 3, median 6, Q3 8, max 9. Dial A is the IQR. Dial B is the range.',
        scene: { kind: 'emoji', bg: '#20160e', floor: '#3a2a1a', items: [{ e: '🚪', x: 200, y: 180, s: 120, msg: 'A gate with two dials.' }], caption: 'dial A, then dial B' },
        title: 'The Gate Summary', prompt: '<div class="eq">min 1 · Q1 3 · median 6 · Q3 8 · max 9</div><p>A = IQR, B = range.</p>', fields: [{ label: 'A', answer: 5 }, { label: 'B', answer: 8 }], button: 'Open the gate',
        hints: ['IQR = Q3 − Q1.', 'Range = max − min.', 'A = 8 − 3 = 5 and B = 9 − 1 = 8.'], key: 'A = 5 (8 − 3), B = 8 (9 − 1).', check: [['8-3', 5], ['9-1', 8]] }
    ]
  },

  cheat: {
    focus: 'center, spread, box plots and outliers',
    morefocus: 'two-way tables, scatter plots, lines of fit and residuals',
    front: [
      { title: 'Key Vocabulary', color: 'purple', kind: 'vocab', rows: [
        ['mean', 'Add the values, divide by how many.', '⟨2, 4, 9⟩: 5'], ['median', 'The middle value of the ordered data.', '⟨2, 4, 9⟩: 4'],
        ['mode', 'The value that appears most often.', '⟨1, 3, 3⟩: 3'], ['range', 'Maximum minus minimum.', '⟨9 - 2 = 7⟩'],
        ['outlier', 'A value far away from the rest of the data.', '⟨2, 3, 4, 40⟩']] },
      { title: 'Measures of Center', color: 'blue', kind: 'example', text: 'Mean is the average, median is the middle value after sorting, and mode is the most frequent value.',
        example: 'Find the mean, median and mode of ⟨2, 4, 4, 6, 9⟩.', steps: [['Mean:', '⟨25 \\div 5 = 5⟩'], ['Median:', '⟨4⟩'], ['Mode:', '⟨4⟩']], answer: 'Mean 5; median 4; mode 4' },
      { title: 'Quartiles and IQR', color: 'green', kind: 'example', text: 'Q1 is the median of the lower half, Q3 the median of the upper half. IQR = Q3 − Q1.',
        example: '⟨2, 4, 5, 7, 8, 10, 12, 15⟩', steps: [['Halves:', '⟨2, 4, 5, 7⟩ and ⟨8, 10, 12, 15⟩'], ['Quartiles:', '⟨Q_1 = 4.5,\\ Q_3 = 11⟩'], ['IQR:', '⟨11 - 4.5 = 6.5⟩']], answer: 'IQR ⟨= 6.5⟩' },
      { title: 'Box Plots', color: 'orange', kind: 'list', items: [
        'Five-number summary: <b>min, Q1, median, Q3, max</b>.', 'The box goes from Q1 to Q3; the line inside is the median.', 'The whiskers reach the min and max.',
        'Each part (whisker or half-box) holds about 25% of the data.', 'A longer box means more spread in the middle half.'] },
      { title: 'Outliers', color: 'pink', kind: 'example', text: 'A value is an outlier if it is below Q1 − 1.5·IQR or above Q3 + 1.5·IQR.',
        example: '⟨Q_1 = 10,\\ Q_3 = 18⟩. Is 31 an outlier?', steps: [['IQR:', '⟨18 - 10 = 8⟩'], ['Fences:', '⟨10 - 12 = -2⟩ and ⟨18 + 12 = 30⟩']], answer: '31 > 30: yes' },
      { title: 'Quick Reminders & Common Mistakes', color: 'teal', kind: 'mistakes',
        good: ['Put the data in order before finding the median or quartiles.', 'Outliers pull the mean, not the median.', 'Use median and IQR for skewed data; mean for roughly symmetric data.'],
        bad: [['median of unordered data', 'order it first!'], ['two middle values', 'average them'], ['range', 'is max − min, not the biggest number']] }
    ],
    back: [
      { title: 'Two-Way Tables', color: 'green', kind: 'html', html: T([['', 'Dog', 'No dog', 'Total'], ['8th', '12', '13', '25'], ['9th', '6', '19', '25'], ['Total', '18', '32', '50']]).replace('<table>', '<table class="vt">') +
        '<div style="margin-top:4px"><b>Joint</b> relative frequency: one cell ÷ grand total, e.g. 12/50 = 24%.<br><b>Marginal</b>: a row or column total ÷ grand total, e.g. 18/50 = 36%.<br><b>Conditional</b>: one cell ÷ ITS row (or column) total, e.g. 6/25 = 24% of 9th graders have a dog.</div>' },
      { title: 'Correlation', color: 'purple', kind: 'table', head: ['Type', 'Looks like', 'Example'], rows: [
        ['positive', 'rises left to right', 'study time vs. score'], ['negative', 'falls left to right', 'car age vs. value'], ['none', 'no pattern', 'shoe size vs. birthday'],
        ['r near ±1', 'strong (tight line)', '⟨r = 0.95⟩'], ['r near 0', 'weak or none', '⟨r = 0.1⟩']], after: 'Correlation does NOT mean one thing causes the other.' },
      { title: 'Line of Fit', color: 'blue', kind: 'example', text: 'Use the line to predict: substitute x and find y. The slope is the rate; the y-intercept is the starting value.',
        example: '⟨y = 2.5x + 10⟩. Predict ⟨y⟩ at ⟨x = 8⟩.', steps: [['Substitute:', '⟨2.5(8) + 10⟩'], ['Simplify:', '⟨20 + 10 = 30⟩']], answer: '⟨y = 30⟩' },
      { title: 'Residuals', color: 'orange', kind: 'example', text: 'Residual = actual − predicted. Positive: the point is above the line. Negative: below the line.',
        example: 'Model ⟨y = 3x + 4⟩; at ⟨x = 9⟩, actual ⟨y = 34⟩.', steps: [['Predicted:', '⟨3(9) + 4 = 31⟩'], ['Residual:', '⟨34 - 31 = 3⟩']], answer: '⟨3⟩ (above the line)' },
      { title: 'Shape of Data', color: 'pink', kind: 'table', head: ['Shape', 'Tail', 'Mean vs. median'], rows: [
        ['symmetric', 'none: both sides match', 'mean ≈ median'], ['skewed right', 'long tail to the right', 'mean > median'], ['skewed left', 'long tail to the left', 'mean < median']] },
      { title: 'Check Yourself', color: 'teal', kind: 'list', items: [
        'Did I order the data first?', 'Did I divide by the right total in the two-way table?', 'Residual: actual minus predicted (not the other way)?', 'Does my prediction make sense in the context?'] }
    ]
  }
};
