/* Shared curriculum discovery for generator unit selectors.
   Exposes NEW grade-level courses without manufacturing question banks.
   A unit becomes selectable only after its MKMENU skill set is actually registered. */
(function (G) {
  'use strict';
  var ns = G.MKMENU, library = G.LIBRARY, catalog = G.MK_COURSE_CATALOG;
  if (!ns || !Array.isArray(ns.CATALOG) || !library || !catalog) return;
  var courseIds = ['math6', 'prealgebra7', 'prealgebra'];
  var seen = Object.create(null);
  ns.CATALOG.forEach(function (group) { group.units.forEach(function (u) { seen[u[0]] = true; }); });
  courseIds.forEach(function (id) {
    var course = library.courses.filter(function (c) { return c.id === id; })[0];
    if (!course) return;
    var units = course.units.map(function (unit, i) {
      var bankId = id + '-' + unit.id;
      return [bankId, 'Unit ' + (i + 1) + ' · ' + unit.name];
    }).filter(function (u) { return !seen[u[0]]; });
    if (units.length) {
      ns.CATALOG.unshift({ course: course.name, units: units });
      units.forEach(function (u) { seen[u[0]] = true; });
    }
  });
  ns.courseBridge = { version: 1, registeredCourses: courseIds.slice() };
})(typeof window !== 'undefined' ? window : globalThis);
