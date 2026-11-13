/* Every unit page offers the same four Create cards: Lesson Plan, Worksheet, Activity and Assessment.
   Courses that already list a card for a tool keep theirs; any of the four that is missing is added at the
   top of the unit, pointing at the shared generators with this unit preselected (#unit=<course>-<unit>).
   Grades 3–5 and Financial Algebra bring their own generator cards and are left as they are.
   Load after course-catalog.js. */
(function (G) {
  'use strict';
  var L = G.LIBRARY;
  if (!L || !Array.isArray(L.courses)) return;
  var SKIP = { 'financial-algebra': 1, grade1: 1, grade2: 1, grade3: 1, grade4: 1, grade5: 1 };
  var LEVELS = ['CP2', 'CP1', 'Honors'];
  var TOOLS = [
    { page: 'lesson-planner.html', format: 'lesson-planner', title: 'Daily Lesson Planner', type: 'Planning',
      thumb: 'thumbs/lesson-planner-any-course.svg',
      text: function (c, u) { return 'Plan any day of ' + u + ': Do Now, notes, worked examples, practice and an exit ticket, with handouts and a teacher key.'; } },
    { page: 'worksheet.html', format: 'worksheet-generator', title: 'Worksheet Generator', type: 'Practice',
      thumb: 'thumbs/worksheet-generator-any-course.svg',
      text: function (c, u) { return 'Build ' + u + ' practice worksheets: pick skills and CP2, CP1 or Honors difficulty, then print with an answer key.'; } },
    { page: 'printables.html', format: 'printable-generator', title: 'Activity Generator', type: 'Printable',
      thumb: 'thumbs/activity-generator-any-course.svg',
      text: function (c, u) { return 'Make ' + u + ' mazes, color by number, Tarsia puzzles, stations, partner checks and more, with teacher keys.'; } },
    { page: 'menu-assessment.html', format: 'assessment-generator', title: 'Assessment Generator', type: 'Printable',
      thumb: 'thumbs/menu-assessment-generator.svg',
      text: function (c, u) { return 'Build a ' + u + ' unit test or a choice-based menu assessment, versions A to C, with a teacher key.'; } }
  ];
  function unitKey(course, unit) {
    // Reuse the id the unit's own generator links already use; otherwise <course>-<unit>.
    var list = unit.artifacts || [];
    for (var i = 0; i < list.length; i++) {
      var m = /worksheet-generator\/[a-z-]+\.html#unit=([a-z0-9-]+)/.exec(list[i] && list[i].path || '');
      if (m) return m[1];
    }
    return course.id + '-' + unit.id;
  }
  L.courses.forEach(function (course) {
    if (SKIP[course.id] || course.planned || course.comingSoon) return;
    (course.units || []).forEach(function (unit) {
      if (!Array.isArray(unit.artifacts) || !unit.artifacts.length) return;
      var key = unitKey(course, unit), add = [];
      TOOLS.forEach(function (tool) {
        var has = unit.artifacts.some(function (a) { return a && (a.path || '').indexOf('worksheet-generator/' + tool.page) === 0; });
        if (has) return;
        add.push({ title: tool.title, path: 'worksheet-generator/' + tool.page + '#unit=' + key, thumb: tool.thumb,
          description: tool.text(course.name, unit.name), type: tool.type, bankFormat: tool.format, level: LEVELS.slice(),
          topics: [unit.name] });
      });
      if (add.length) Array.prototype.unshift.apply(unit.artifacts, add);
    });
  });
})(typeof window !== 'undefined' ? window : globalThis);
