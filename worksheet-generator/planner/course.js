/* Daily Lesson Planner course selector.
   The same planner UI and exports serve Algebra 1, Geometry, and Algebra 2. */
(function (G) {
  'use strict';
  var h = {};
  try { (G.location && G.location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var p = kv.split('='); if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); }); } catch (e) { /* no location */ }
  var pa8 = (h.course === 'prealgebra' || /^prealgebra-/.test(h.unit || '')) && G.MKPLAN_SCOPE_PREALGEBRA;
  var a2 = (h.course === 'algebra2' || /^algebra2-/.test(h.unit || '')) && G.MKPLAN_SCOPE_ALGEBRA2 && G.MKPLAN_SKILLS_ALGEBRA2;
  var geo = !a2 && (h.course === 'geometry' || /^geometry-/.test(h.unit || '')) && G.MKPLAN_SCOPE_GEOMETRY && G.MKPLAN_SKILLS_GEOMETRY;
  G.MKPLAN_COURSE = pa8 ? 'prealgebra' : a2 ? 'algebra2' : geo ? 'geometry' : 'algebra1';
  if (pa8) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_PREALGEBRA; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_PREALGEBRA; Object.keys(G.MKMENU.LEVELS).forEach(function(k){var name={cp2:'Remedial',cp1:'Standard',honors:'Advanced'}[k];G.MKMENU.LEVELS[k].name=name;G.MKMENU.LEVELS[k].long=name;}); }
  else if (a2) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_ALGEBRA2; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_ALGEBRA2; }
  else if (geo) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_GEOMETRY; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_GEOMETRY; }
})(typeof window !== 'undefined' ? window : globalThis);
