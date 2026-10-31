/* Daily Lesson Planner course selector.
   The same planner UI and exports serve Algebra 1, Geometry, and Algebra 2. */
(function (G) {
  'use strict';
  var h = {};
  try { (G.location && G.location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var p = kv.split('='); if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); }); } catch (e) { /* no location */ }
  var a2 = (h.course === 'algebra2' || /^algebra2-/.test(h.unit || '')) && G.MKPLAN_SCOPE_ALGEBRA2 && G.MKPLAN_SKILLS_ALGEBRA2;
  var geo = !a2 && (h.course === 'geometry' || /^geometry-/.test(h.unit || '')) && G.MKPLAN_SCOPE_GEOMETRY && G.MKPLAN_SKILLS_GEOMETRY;
  G.MKPLAN_COURSE = a2 ? 'algebra2' : geo ? 'geometry' : 'algebra1';
  if (a2) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_ALGEBRA2; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_ALGEBRA2; }
  else if (geo) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_GEOMETRY; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_GEOMETRY; }
})(typeof window !== 'undefined' ? window : globalThis);
