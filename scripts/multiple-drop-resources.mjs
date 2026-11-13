// Shared release hook: course assemblers retain this game when refreshing content.
const unitsByCourse = {
  grade3: ['multiplication-meaning', 'properties-fact-strategies'],
  grade4: ['multiplication-strategies', 'factors-multiples-patterns'],
  grade5: ['multi-digit-multiplication-division']
};
export function addMultipleDrop(course) {
  for (const id of unitsByCourse[course.id] || []) {
    const unit = course.units.find(u => u.id === id);
    if (!unit) throw Error('Multiple Drop: missing unit ' + course.id + '/' + id);
    if (!unit.artifacts.some(a => a.path === '/artifacts/times-table-sorter/index.html')) {
      unit.artifacts.push({
        title: 'Times Table Sorter', path: '/artifacts/times-table-sorter/index.html',
        thumb: '/thumbs/times-table-sorter.svg', type: 'Game', bankFormat: 'topic-games',
        description: 'Sort product tiles into a multiplication grid. Choose tables up to 12×12 and three difficulty levels. Grade 5 fact-fluency review; drag, tap or use the keyboard.',
        topics: ['Multiplication facts', 'Multiplication tables', 'Factors and products'], added: '2026-11-13'
      });
    }
    if (unit.artifacts.some(a => a.path === '/artifacts/multiple-drop/index.html')) continue;
    unit.artifacts.push({
      title: 'Multiple Drop', path: '/artifacts/multiple-drop/index.html',
      thumb: '/thumbs/multiple-drop.svg', type: 'Game', bankFormat: 'topic-games',
      description: 'Choose a times table from 1–12 and tap falling multiples in order. Build multiplication fluency with three lives and increasing speed. Scores stay on this device.',
      topics: ['Multiplication facts', 'Multiples', 'Skip counting'], added: '2026-11-13'
    });
  }
  return course;
}
