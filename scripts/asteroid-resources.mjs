// Released elementary courses are assembled after the base catalog loads.
// Register only audited quick-answer units, preserving the three-per-grade limit.
export const asteroidUnits = {
  grade2: ['place-value-1000', 'count-compare-1000'],
  grade3: ['properties-fact-strategies', 'equivalent-comparing-fractions'],
  grade4: ['factors-multiples-patterns', 'fractions-equivalent-fractions'],
  grade5: ['place-value-number-sense', 'multi-digit-multiplication-division', 'decimal-operations']
};
export function addAsteroidBlaster(course) {
  for (const id of asteroidUnits[course.id] || []) {
    const unit = course.units.find(u => u.id === id);
    if (!unit) throw Error('Asteroid Blaster: missing unit ' + course.id + '/' + id);
    const gamePath = 'worksheet-generator/asteroid-blaster.html?course=' + course.id + '&unit=' + id;
    if (unit.artifacts.some(a => a.bankFormat === 'asteroid-blaster')) continue;
    unit.artifacts.push({
      title: 'Asteroid Blaster', path: gamePath, type: 'Game', bankFormat: 'asteroid-blaster',
      thumb: 'thumbs/asteroid-blaster.jpg',
      description: 'Quick-answer mental math arcade game with teacher-selected skills.',
      topics: [unit.name, 'Mental Math', 'Arcade'], added: '2026-11-13'
    });
  }
  return course;
}
