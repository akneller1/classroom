/* Daily Lesson Planner: picks the course (Algebra 1 or Geometry) before the planner loads.
   Geometry is chosen by  #course=geometry  or by a Geometry unit link (#unit=geometry-…).  It swaps in the Geometry
   scope & sequence (scope-geometry.js) and lesson→skill map (lesson-skills-geometry.js); everything else is shared.
   G.MKPLAN_COURSE is 'algebra1' or 'geometry'. Load this after the scope and skill files and before planner.js. */
(function (G) {
  'use strict';
  var h = {};
  try { (G.location && G.location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var p = kv.split('='); if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); }); } catch (e) { /* no location */ }
  if(h.course==='algebra2'||/^algebra2-/.test(h.unit||'')){G.location.replace('bank-printable.html?mode=lesson'+(h.unit?'&unit='+encodeURIComponent(h.unit.replace(/^algebra2-/,'')):''));return;}
  var geo = (h.course === 'geometry' || /^geometry-/.test(h.unit || '')) && G.MKPLAN_SCOPE_GEOMETRY && G.MKPLAN_SKILLS_GEOMETRY;
  G.MKPLAN_COURSE = geo ? 'geometry' : 'algebra1';
  if (geo) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_GEOMETRY; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_GEOMETRY; }
})(typeof window !== 'undefined' ? window : globalThis);
