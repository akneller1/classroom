/* Shared curriculum discovery for all generator unit selectors.
   Read the same published course list as the main Classroom.
   Discovery does not manufacture question banks or make unsupported units selectable. */
(function (G) {
  'use strict';
  var ns = G.MKMENU, library = G.LIBRARY;
  if (!ns || !Array.isArray(ns.CATALOG) || !library || !Array.isArray(library.courses)) return;

  var aliases = { algebra: 'Algebra 1', geometry: 'Geometry', algebra2: 'Algebra 2' };
  var reserved = { algebra: 'algebra1' };
  var registered = [];
  var published = library.courses.filter(function (c) { return c && !c.comingSoon && Array.isArray(c.units); });

  published.forEach(function (course) {
    var title = aliases[course.id] || course.name;
    var prefix = reserved[course.id] || course.id;
    var group = ns.CATALOG.find(function (entry) { return entry.course === title; });
    var units = course.units.map(function (unit, i) {
      return [prefix + '-' + unit.id, 'Unit ' + (i + 1) + ' · ' + unit.name];
    });

    if (group) {
      /* Preserve IDs of hand-written skill sets; refresh all matching published units. */
      var existing = Object.create(null);
      group.units.forEach(function (unit) { existing[unit[0]] = unit; });
      group.units = units.map(function (unit) { return existing[unit[0]] ? [unit[0], unit[1]] : unit; });
    } else if (units.length) {
      ns.CATALOG.push({ course: title, units: units });
    }
    registered.push(course.id);
  });

  /* A future/retired course must never remain in the generator list from a
     static fallback catalog. */
  var publishedNames = published.map(function (c) { return aliases[c.id] || c.name; });
  ns.CATALOG = ns.CATALOG.filter(function (group) {
    return publishedNames.indexOf(group.course) >= 0;
  });
  ns.courseBridge = { version: 2, registeredCourses: registered };
})(typeof window !== 'undefined' ? window : globalThis);
