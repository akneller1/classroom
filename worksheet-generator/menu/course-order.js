/* Lists the classes in every generator menu in one order: by grade, then the upper-level electives,
   Financial Algebra last (the same order as the home page and the Lesson Planner).
   Load after every script that adds a class to MKMENU.CATALOG and before menu/app.js or menu/printables-ui.js. */
(function (G) {
  'use strict';
  var NS = G.MKMENU;
  if (!NS || !Array.isArray(NS.CATALOG)) return;
  var ORDER = ['1st Grade Math', '2nd Grade Math', '3rd Grade Math', '4th Grade Math', '5th Grade Math', '6th Grade Math',
    'Pre-Algebra (7th)', 'Pre-Algebra (8th)', 'Algebra 1', 'Geometry', 'Algebra 2', 'Precalculus', 'Calculus',
    'Statistics', 'Discrete Math', 'Financial Algebra'];
  var rank = function (g) { var i = ORDER.indexOf(g && g.course); return i < 0 ? ORDER.length : i; };
  var sorted = NS.CATALOG.map(function (g, i) { return [g, i]; })
    .sort(function (a, b) { return rank(a[0]) - rank(b[0]) || a[1] - b[1]; })
    .map(function (x) { return x[0]; });
  NS.CATALOG.length = 0;
  Array.prototype.push.apply(NS.CATALOG, sorted);
})(typeof window !== 'undefined' ? window : globalThis);
