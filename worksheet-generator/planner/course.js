/* Daily Lesson Planner course selector.
   The same planner UI and exports serve Algebra 1, Geometry, and Algebra 2. */
(function (G) {
  'use strict';

  /* Whole-site audit 2 #1 (2026-11-20): use the pacing guide's 180-day calendar (planner/calendar.js, built at deploy). A planner
     lesson keeps everything it had and only takes its pacing-guide day number; the days the pacing guide adds (mid-unit and
     extra practice, flex, semester and final review and exams, state-test review and sessions, AP review and projects) are
     built from that course's own day templates and review the unit's lessons, or every lesson taught so far. */
  function spread(list, n) { if (list.length <= n) return list.slice(); var out = []; for (var i = 0; i < n; i++) out.push(list[Math.round(i * (list.length - 1) / (n - 1))]); return out; }
  function useCalendar(id) {
    var cal = (G.MKPLAN_CALENDAR || {})[id], base = G.MKPLAN_SCOPE;
    if (!cal || !base || !base.days || !base.days.length || !cal.days || !cal.days.length) return;
    var byId = {}, unitIds = {}, taught = [];
    base.days.forEach(function (d) { byId[d.lesson_id] = d; });
    base.units.forEach(function (u) { unitIds[u.unit] = u.lesson_ids || []; });
    var days = cal.days.map(function (c) {
      var b = byId[c.id];
      if (b && b.day_type === 'Lesson') {
        (c.covered || [c.id]).forEach(function (x) { if (taught.indexOf(x) < 0) taught.push(x); });
        var d = Object.assign({}, b, { day: c.day, title: c.title || b.title });
        if (c.covered) d.lessons_covered = c.covered.slice();
        return d;
      }
      if (b) return Object.assign({}, b, { day: c.day, title: c.title || b.title });
      var ids = c.unit != null && unitIds[c.unit] ? unitIds[c.unit].filter(function (x) { return taught.indexOf(x) >= 0; }) : taught.slice();
      if (!ids.length && c.unit != null) ids = (unitIds[c.unit] || []).slice();
      var unit = c.unit != null ? base.units.filter(function (u) { return u.unit === c.unit; })[0] : null;
      return { day: c.day, quarter: 0, week: 0, unit: c.unit, unit_title: unit ? unit.title : '', unit_day: c.type, day_type: c.type, lesson_id: c.id, title: c.title,
        standards: '', content_objective: c.obj || (c.type === 'Assessment' ? '' : 'Review and practice ' + (unit ? unit.title : 'the topics taught so far') + '.'),
        language_objective: 'Students will explain their mathematical reasoning using accurate mathematical vocabulary.', sentence_frame: 'One strategy I used was ___.',
        key_vocabulary: '', common_misconception: '', notes_style: c.type === 'Assessment' ? '' : 'Guided review', do_now_strategy: 'Review selected topics.',
        do_now_source_ids: ids.slice(-2), spiral_review_ids: ids.slice(-8), lessons_covered: c.unit != null ? ids.slice() : spread(taught, 12), components: (base.day_types || {})[c.type] || (base.day_types || {}).Practice };
    });
    G.MKPLAN_SCOPE = Object.assign({}, base, { meta: Object.assign({}, base.meta, { total_days: days.length, notes: 'Days follow the course pacing guide (180 days).' }), units: cal.units, days: days });
  }
  var h = {};
  try { (G.location && G.location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var p = kv.split('='); if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); }); } catch (e) { /* no location */ }
  var mid = ['prealgebra', 'prealgebra7', 'math6', 'grade1', 'grade2', 'grade3', 'grade4', 'grade5'].filter(function (c) { return (h.course === c || new RegExp('^' + c + '-').test(h.unit || '')) && G['MKPLAN_SCOPE_' + c.toUpperCase()]; })[0];
  var hs = mid ? null : ['precalculus', 'calculus', 'statistics', 'discrete'].filter(function (c) { return (h.course === c || new RegExp('^' + c + '-').test(h.unit || '')) && G['MKPLAN_SCOPE_' + c.toUpperCase()]; })[0];
  var pa8 = !!mid;
  var a2 = (h.course === 'algebra2' || /^algebra2-/.test(h.unit || '')) && G.MKPLAN_SCOPE_ALGEBRA2 && G.MKPLAN_SKILLS_ALGEBRA2;
  var geo = !a2 && (h.course === 'geometry' || /^geometry-/.test(h.unit || '')) && G.MKPLAN_SCOPE_GEOMETRY && G.MKPLAN_SKILLS_GEOMETRY;
  G.MKPLAN_COURSE = pa8 ? mid : hs ? hs : a2 ? 'algebra2' : geo ? 'geometry' : 'algebra1';
  if (hs) { G.MKPLAN_SCOPE = G['MKPLAN_SCOPE_' + hs.toUpperCase()]; G.MKPLAN_SKILLS = G['MKPLAN_SKILLS_' + hs.toUpperCase()]; useCalendar(hs); return; }   // high-school courses keep the CP2 / CP1 / Honors labels
  if (pa8) { G.MKPLAN_SCOPE = G['MKPLAN_SCOPE_' + mid.toUpperCase()]; G.MKPLAN_SKILLS = G['MKPLAN_SKILLS_' + mid.toUpperCase()]; Object.keys(G.MKMENU.LEVELS).forEach(function(k){var name={cp2:'Support',cp1:'Standard',honors:'Advanced'}[k];G.MKMENU.LEVELS[k].name=name;G.MKMENU.LEVELS[k].long=name;}); useCalendar(mid); }
  else if (a2) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_ALGEBRA2; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_ALGEBRA2; useCalendar('algebra2'); }
  else if (geo) { G.MKPLAN_SCOPE = G.MKPLAN_SCOPE_GEOMETRY; G.MKPLAN_SKILLS = G.MKPLAN_SKILLS_GEOMETRY; }
})(typeof window !== 'undefined' ? window : globalThis);

