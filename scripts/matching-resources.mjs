// Shared release hook: the interactive matching card sorts for the elementary courses.
// Called by integrate-grade1..4.mjs and integrate-approved-courses.mjs (Grade 5) after each course is assembled,
// so the games appear on the Classroom unit pages. The player is worksheet-generator/match-game.html; the
// kinds are defined in worksheet-generator/menu/match-kinds-elementary.js (and match-kinds-number.js for decimals),
// keyed by the same "grade<N>-<unit>" ids the release catalogs register.
const KIND = {
  place1: ['Tens and Ones Matching Game', 'Match each number to its base-ten blocks, its tens and ones and its expanded form. Look-alikes swap the digits, like 47 and 74.'],
  place: ['Place Value Matching Game', 'Match each number to its base-ten blocks, expanded form and number name. Look-alikes use the same digits in a different order.'],
  placeBig: ['Place Value Matching Game', 'Match each number to its number name, expanded form and place-value chart. Look-alikes use the same digits in a different order.'],
  time: ['Clock Matching Game', 'Match each clock to its digital time and the time in words. Look-alikes swap the hour hand and the minute hand.'],
  money: ['Money Matching Game', 'Match each amount to two different collections of coins and bills worth exactly that much.'],
  mult2: ['Arrays Matching Game', 'Match each repeated addition to its array, its rows (like “3 rows of 4”) and the equation for the total. Every set has a different total.'],
  mult: ['Multiplication Matching Game', 'Match each multiplication to its equal groups, its array and its repeated addition. Every set has a different product.'],
  div: ['Division Matching Game', 'Match each division to its equal-sharing picture, the related multiplication fact and a sharing story.'],
  efrac: ['Fraction Matching Game', 'Match each fraction to a shaded model, a point on a number line and the fraction in words.'],
  shares: ['Equal Shares Matching Game', 'Match halves, thirds and fourths: the words, a picture with equal shares, and “1 of 3 equal shares”.'],
  equiv: ['Equivalent Fraction Matching Game', 'Match each fraction to an equivalent fraction, a shaded model and a point on a number line; the model and the number line use different partitions.'],
  mixed: ['Mixed Number Matching Game', 'Match each mixed number to the same amount as an improper fraction, a shaded model and a point on a number line.'],
  fdp: ['Decimal Matching Game', 'Match tenths and hundredths: each fraction to its decimal, a hundred-grid model and the words. Look-alikes such as 0.4 and 0.04 sit side by side.'],
  graph1: ['Data Matching Game', 'The same survey shown different ways: match each table to its tally chart and its picture graph. Look-alikes swap two of the counts.'],
  graph: ['Graph Matching Game', 'The same survey shown different ways: match each table to its tally chart, picture graph and bar graph. Look-alikes swap two of the counts.'],
  graph3: ['Scaled Graph Matching Game', 'Match each table to its scaled picture graph, its scaled bar graph and a set of facts it shows (“how many more”, totals). Read the key carefully!'],
  expr: ['Expression Matching Game', 'Match each description in words to its numerical expression and its value. Look-alikes use the same numbers in a different order of operations.'],
  area3: ['Area Matching Game', 'Match each rectangle on a grid to its multiplication and its area in square units. Look-alikes share a side length, so check both sides of every rectangle.'],
  area: ['Area Model Matching Game', 'Match each multiplication to its area model, its partial products and the product.']
};
// unit → [player kind, listing kind]
const UNITS = {
  grade1: { 'tens-ones': [['place', 'place1']], 'telling-time': [['time']], data: [['graph', 'graph1']] },
  grade2: { 'place-value-1000': [['place']], 'time-money': [['time'], ['money']], 'odd-even-arrays': [['mult', 'mult2']], 'graphs-data': [['graph']], 'shapes-equal-shares': [['efrac', 'shares']] },
  grade3: { 'multiplication-meaning': [['mult']], 'division-meaning': [['mult', 'div']], 'understanding-fractions': [['efrac']], 'equivalent-comparing-fractions': [['efrac', 'equiv']], 'time-volume-mass': [['time']], 'graphs-measurement-data': [['graph', 'graph3']], area: [['area', 'area3']] },
  grade4: { 'place-value-number-sense': [['place', 'placeBig']], 'multiplication-strategies': [['area']], 'fractions-equivalent-fractions': [['efrac', 'equiv']], 'fraction-operations-decimals': [['fdp']] },
  grade5: { 'place-value-number-sense': [['place', 'placeBig']], 'numerical-expressions-patterns': [['expr']], 'fraction-addition-subtraction': [['efrac', 'mixed']], 'multi-digit-multiplication-division': [['area']] }
};
export function addMatchingGames(course) {
  const map = UNITS[course.id] || {};
  for (const [unitId, games] of Object.entries(map)) {
    const unit = course.units.find(u => u.id === unitId);
    if (!unit) throw Error('Matching games: missing unit ' + course.id + '/' + unitId);
    unit.artifacts = unit.artifacts || [];
    for (const [kind, listing = kind] of games) {
      const path = 'worksheet-generator/match-game.html#unit=' + course.id + '-' + unitId + '&kind=' + kind;
      if (unit.artifacts.some(a => a.path === path)) continue;
      const [title, description] = KIND[listing];
      unit.artifacts.push({ title, path, thumb: 'thumbs/matching-' + kind + '.svg', type: 'Game', bankFormat: 'topic-games',
        level: ['Support', 'Standard', 'Advanced'], description: description + ' Drag or tap, zoom in, check sets and get hints; prints as a card sort.',
        topics: ['Matching game', unit.name || unitId], added: '2026-11-14' });
    }
  }
  return course;
}
export const MATCHING_UNITS = UNITS;
