/* Daily Lesson Planner — engine (no DOM).

   For any day of the Algebra 1 scope & sequence (planner/scope-algebra1.js) it builds one day's plan:
     Do Now · Notes (worked examples) · Practice · Exit ticket / summary
   Problems come from the same verified skill generators as the Worksheet and Assessment Generators
   (MKMENU.generateProblem: generate → verify independently → de-duplicate). planner/lesson-skills.js says
   which skills practice each lesson; Do Nows draw on do_now_source_ids + spiral_review_ids.
   A problem that cannot be verified becomes a flagged slot, never a substitute.

   MKPLAN.buildDay(day, {level, seed, practice})  → plan
   MKPLAN.regenerate(plan, sectionId, groupIndex, itemIndex) → new problem in that slot */
(function (G) {
  'use strict';
  var NS = G.MKMENU, WS = G.MKWS, P = (G.MKPLAN = G.MKPLAN || {});
  function scope() { return G.MKPLAN_SCOPE; }
  function map() { return G.MKPLAN_SKILLS; }

  P.day = function (n) { var d = scope().days[(n | 0) - 1]; return d && d.day === (n | 0) ? d : scope().days.filter(function (x) { return x.day === (n | 0); })[0]; };
  P.lessonById = function (id) { return scope().days.filter(function (x) { return x.lesson_id === id; })[0]; };
  P.unitOf = function (n) { return scope().units.filter(function (u) { return u.unit === n; })[0]; };
  P.unitSetId = function (unitNum) { var k = map().UNIT_SET[unitNum]; return k ? map().SETS[k] : null; };
  /* "Students will be able to evaluate…" → "I can evaluate…" */
  P.iCan = function (obj) {
    var s = String(obj || '').trim();
    var m = s.match(/^Students will be able to\s+(.*)$/i);
    return m ? 'I can ' + m[1] : s;
  };
  P.vocab = P.vocab || function (d) { return String(d.key_vocabulary || '').split(/\s*,\s*/).filter(Boolean); };   // notes-content.js replaces it to apply teacher edits
  P.template = function (d) { return d.components || scope().day_types[d.day_type] || {}; };
  P.coverOf = function (id) { return map().lessons[id] || null; };

  /* ---------- skill entries ---------- */
  function entriesFor(ids) {
    var out = [];
    (ids || []).forEach(function (id) {
      var m = map().lessons[id]; if (!m) return;
      m.skills.forEach(function (s, k) { out.push({ lesson: id, set: map().SETS[s[0]], skill: s[1], cmin: s[2] || 1, cmax: s[3] || 7, k: k }); });
    });
    return out;
  }
  P.entriesFor = entriesFor;
  /* Round-robin by lesson first, then by skill inside the lesson, so every lesson is used before any repeats. */
  function interleave(ids) {
    var byLesson = (ids || []).map(function (id) { return entriesFor([id]); }).filter(function (a) { return a.length; });
    var out = [], i = 0, more = true;
    while (more) { more = false; byLesson.forEach(function (a) { if (i < a.length) { out.push(a[i]); more = true; } }); i++; }
    // second pass order: lesson-major rotation is what callers cycle through
    var rot = [], maxLen = Math.max.apply(null, [0].concat(byLesson.map(function (a) { return a.length; })));
    for (var r = 0; r < maxLen; r++) byLesson.forEach(function (a) { rot.push(a[r % a.length]); });
    return rot.length ? rot : out;
  }
  function clampC(e, c) { return Math.max(e.cmin, Math.min(e.cmax, Math.max(1, Math.min(7, c)))); }
  function uniq(a) { var s = {}; return a.filter(function (x) { if (s[x]) return false; s[x] = 1; return true; }); }

  /* ---------- generation ---------- */
  function policy(plan) { var lv = NS.LEVELS[plan.level] || NS.LEVELS.cp1; return { intOnly: lv.intOnly, level: lv.id }; }
  function makeProblem(plan, slot, e, c, salt) {
    var cc = clampC(e, c);
    var p = NS.generateProblem(e.set, e.skill, cc, policy(plan), [plan.seed, plan.day.day, slot, salt || 0].join('|'), plan.used);
    var set = NS.skillSets[e.set], sk = set && set.byId[e.skill];
    if (p.failed) p = { failed: true, reason: p.reason, skill: e.skill, c: cc };
    p.slot = slot; p.entry = e; p.lesson = e.lesson; p.skillName = sk ? sk.name : e.skill; p.setTitle = set ? set.unitName || set.title : e.set;
    return p;
  }
  function items(plan, slotPrefix, rot, count, cAt) {
    var out = [];
    if (!rot.length) return out;
    for (var i = 0; i < count; i++) out.push(makeProblem(plan, slotPrefix + i, rot[i % rot.length], cAt(i, count)));
    return out;
  }
  function ramp(tiers) { return function (i, n) { return n <= 1 ? tiers[1] : tiers[Math.round(i * 2 / (n - 1))] ; }; }
  function fixed(c) { return function () { return c; }; }

  /* Do Now lessons: the day's sources plus spiral review; sensible fallbacks when the scope lists none. */
  function doNowIds(d) {
    var ids = uniq((d.do_now_source_ids || []).concat(d.spiral_review_ids || []));
    if (!entriesFor(ids).length) {
      if (d.day_type === 'Lesson') { var prev = previousLesson(d); ids = prev ? [prev] : ['LAUNCH-2']; }
      else if (/Review|Flex|Practice|Project/.test(d.day_type)) ids = (d.lessons_covered || []).slice(-3);
    }
    return ids.filter(function (id) { return entriesFor([id]).length; });
  }
  function previousLesson(d) {
    for (var n = d.day - 1; n >= 1; n--) { var x = P.day(n); if (x && x.day_type === 'Lesson' && x.unit === d.unit) return x.lesson_id; }
    return null;
  }
  function doNow(plan, d, count, tiers) {
    var ids = doNowIds(d), main = (d.do_now_source_ids || []).filter(function (id) { return entriesFor([id]).length; }), spiral = (d.spiral_review_ids || []).filter(function (id) { return entriesFor([id]).length && main.indexOf(id) < 0; });
    if (!ids.length) return [];
    if (!main.length) main = ids.filter(function (id) { return spiral.indexOf(id) < 0; });
    if (!main.length) { main = spiral; spiral = []; }
    var nSpiral = spiral.length ? Math.min(spiral.length, Math.max(1, Math.floor(count / 3))) : 0;
    var out = items(plan, 'dn', interleave(main), count - nSpiral, fixed(tiers[0]));
    items(plan, 'dns', interleave(spiral), nSpiral, fixed(tiers[0])).forEach(function (p) { p.spiral = true; out.push(p); });
    return out;
  }

  /* ---------- the plan ---------- */
  P.DEFAULTS = { level: 'cp1', practice: 10 };
  P.buildDay = function (dayNum, opts) {
    opts = opts || {};
    var d = P.day(dayNum); if (!d) throw new Error('No day ' + dayNum + ' in the scope & sequence.');
    var level = NS.LEVELS[opts.level] ? opts.level : P.DEFAULTS.level, lv = NS.LEVELS[level], t = lv.tiers;
    var nPr = Math.max(4, Math.min(20, opts.practice | 0 || P.DEFAULTS.practice));
    var plan = { day: d, level: level, seed: String(opts.seed || 'A'), practiceCount: nPr, used: { keys: new Set(), sigs: new Set() }, sections: [] };
    var cov = d.lessons_covered || [], T = P.template(d);
    var harder = Math.min(7, t[2] + 1);
    function sec(id, title, extra) { var s = { id: id, title: title, groups: [] }; for (var k in extra) s[k] = extra[k]; plan.sections.push(s); return s; }
    function group(s, name, list, note) { s.groups.push({ name: name, note: note || '', items: list }); }
    var dn, notes, pr, ex;
    switch (d.day_type) {
      case 'Lesson':
        dn = sec('donow', 'Do Now', { minutes: 5 }); group(dn, '', doNow(plan, d, 4, t));
        notes = sec('notes', 'Notes', { minutes: 15 });
        var nEx = /pre-filled/i.test(d.notes_style || '') ? 2 : 3;
        group(notes, 'Examples', items(plan, 'ex', interleave(cov), nEx, function (i) { return t[Math.min(2, i)]; }));
        pr = sec('practice', 'Practice', { minutes: 20 });
        var rot = interleave(cov);
        group(pr, 'We do', items(plan, 'wd', rot, 2, fixed(t[0])), 'Work these together.');
        group(pr, 'You do', items(plan, 'yd', rot.slice(1).concat(rot.slice(0, 1)), nPr - 2, ramp(t)), 'Easier to harder.');
        ex = sec('exit', 'Exit Ticket', { minutes: 5, frame: d.sentence_frame }); group(ex, '', items(plan, 'et', rot, 2, fixed(t[1])));
        break;
      case 'Practice':
        dn = sec('donow', 'Do Now', { minutes: 5 }); group(dn, '', doNow(plan, d, 4, t));
        notes = sec('notes', 'Reference Sheet', { minutes: 5, reference: cov });
        pr = sec('practice', 'Tiered Practice', { minutes: 30 });
        var per = Math.max(2, Math.round(nPr / 3)), r2 = interleave(cov);
        group(pr, 'Level 1', items(plan, 'l1', r2, per, fixed(t[0])));
        group(pr, 'Level 2', items(plan, 'l2', r2.slice(1).concat(r2.slice(0, 1)), per, fixed(t[1])));
        group(pr, 'Level 3', items(plan, 'l3', r2.slice(2).concat(r2.slice(0, 2)), per, fixed(t[2])));
        ex = sec('exit', 'Exit Ticket', { minutes: 5, selfAssess: cov }); group(ex, '', items(plan, 'et', r2.slice().reverse(), 2, fixed(t[1])));
        break;
      case 'Quiz':
        dn = sec('donow', 'Warm-up', { minutes: 3 }); group(dn, '', doNow(plan, d, 2, t));
        pr = sec('practice', 'Quiz', { minutes: 35, quiz: true }); group(pr, '', items(plan, 'qz', interleave(cov), 12, ramp(t)));
        ex = sec('exit', 'Quiz Reflection', { minutes: 5, prompt: 'Which problem was hardest and why?' });
        break;
      case 'Review':
        dn = sec('donow', 'Do Now (spiral)', { minutes: 5 }); group(dn, '', doNow(plan, d, 4, t));
        notes = sec('notes', 'Unit Study Guide', { minutes: 10, reference: cov, myExample: true });
        pr = sec('practice', 'Review Stations', { minutes: 25 });
        cov.forEach(function (id, i) { var l = P.lessonById(id); group(pr, 'Station ' + (i + 1) + ': ' + (l ? l.title : id), items(plan, 'st' + i, interleave([id]), 2, function (k) { return t[k + 1]; }), P.coverOf(id) && P.coverOf(id).cover !== 'full' ? P.coverOf(id).note : ''); });
        ex = sec('exit', 'Unit Self-Assessment', { minutes: 5, iCan: cov }); group(ex, '', items(plan, 'et', interleave(cov).slice().reverse(), 1, fixed(t[1])));
        break;
      case 'Assessment':
        dn = sec('donow', 'Calm Start', { minutes: 1, prompt: 'Take a breath. Write one thing you know well from this unit.' });
        pr = sec('practice', 'Unit Test', { minutes: 40, quiz: true, test: true }); group(pr, '', items(plan, 'ut', interleave(cov), 16, ramp(t)));
        ex = sec('exit', 'Post-Test Reflection', { minutes: 4, confidence: cov });
        break;
      case 'Flex':
        dn = sec('donow', 'Do Now (most-missed review)', { minutes: 5 }); group(dn, '', doNow(plan, d, 4, t));
        notes = sec('notes', 'Reteach Mini-Lessons', { minutes: 10, corrections: true });
        pr = sec('practice', 'Corrections, Reteach & Enrichment', { minutes: 25 });
        var r3 = interleave(cov), fl = cov.length > 12 ? 12 : cov.length;
        group(pr, 'Tier 1 reteach', items(plan, 'rt', r3, Math.max(4, fl), fixed(t[0])), 'One problem per lesson. Work with the teacher or a partner.');
        group(pr, 'Enrichment', items(plan, 'en', r3.slice().reverse(), 4, fixed(harder)), 'For students who finish their corrections.');
        ex = sec('exit', 'Correction Reflection', { minutes: 5, frame: 'My error was ___. The correct approach is ___.' });
        break;
      case 'Diagnostic':
        pr = sec('practice', 'Readiness Check', { minutes: 35 }); group(pr, '', items(plan, 'dg', interleave(['LAUNCH-2']), 12, function (i, n) { return i < n / 2 ? 1 : 2; }));
        ex = sec('exit', 'Self-Rating', { minutes: 5, confidence: ['LAUNCH-2'] });
        break;
      case 'Exam Review':
        dn = sec('donow', 'Do Now (cumulative)', { minutes: 5 }); group(dn, '', doNow(plan, d, 4, t));
        notes = sec('notes', 'Cumulative Review Guide', { minutes: 5, reference: cov, byUnit: true });
        pr = sec('practice', 'Mixed Review', { minutes: 30 });
        byUnit(cov).forEach(function (g) { group(pr, 'Unit ' + g.unit + ': ' + g.title, items(plan, 'u' + g.unit, interleave(g.ids), 4, ramp(t))); });
        ex = sec('exit', 'Self-Assessment', { minutes: 5, iCanUnits: byUnit(cov) });
        break;
      case 'Exam':
        pr = sec('practice', 'Cumulative Exam', { minutes: 45, quiz: true, test: true });
        var ex2 = [];
        byUnit(cov).forEach(function (g) { items(plan, 'x' + g.unit, interleave(g.ids), 2, function (k) { return t[k + 1]; }).forEach(function (p) { ex2.push(p); }); });
        group(pr, '', ex2);
        break;
      case 'Project':
        dn = sec('donow', 'Project Check-in', { minutes: 5, prompt: 'Today my goal for the project is ___. One thing I need is ___.' }); group(dn, '', doNow(plan, d, 2, t));
        notes = sec('notes', 'Rubric & Model Selection', { minutes: 5, project: true });
        pr = sec('practice', 'Project Work Time', { minutes: 30, project: true });
        ex = sec('exit', 'Progress Log', { minutes: 5, frame: 'Today I finished ___. Next class I will ___.' });
        break;
      default: // Launch
        dn = sec('donow', 'Do Now', { minutes: 5, prompt: d.lesson_id === 'LAUNCH-1' ? 'Write your math autobiography: one time math went well for you, one time it was hard, and what helped.' : 'How do you get unstuck on a hard problem? List two things you try.' });
        notes = sec('notes', d.lesson_id === 'LAUNCH-1' ? 'Classroom Routines' : 'Problem-Solving Norms', { minutes: 10, routines: true });
        pr = sec('practice', 'Launch Task', { minutes: 25, launch: true });
        ex = sec('exit', 'Reflection', { minutes: 5, frame: d.sentence_frame });
    }
    plan.notesMode = opts.notes === 'filled' || opts.notes === 'fill' ? opts.notes : P.lessonNotesMode(d);
    plan.sections.forEach(function (s) { s.defaultMinutes = s.minutes; });
    if (opts.minutes) P.applyMinutes(plan, opts.minutes);
    plan.sections.forEach(function (s) { s.template = T[{ donow: 'do_now', notes: 'notes', practice: 'practice', exit: 'exit_ticket' }[s.id]] || ''; });
    plan.coverage = uniq(cov.concat(d.day_type === 'Diagnostic' ? ['LAUNCH-2'] : [])).map(function (id) { var m = P.coverOf(id) || { cover: 'none', note: 'Not in the skill map.' }, l = P.lessonById(id); return { id: id, title: l ? l.title : id, cover: m.cover, note: m.note || '' }; });
    plan.unitSet = d.unit ? P.unitSetId(d.unit) : null;
    renumber(plan);
    return plan;
  };
  function byUnit(ids) {
    var out = [], idx = {};
    ids.forEach(function (id) {
      var l = P.lessonById(id); if (!l || !l.unit) return;
      if (!(l.unit in idx)) { idx[l.unit] = out.length; out.push({ unit: l.unit, title: l.unit_title, ids: [] }); }
      out[idx[l.unit]].ids.push(id);
    });
    return out;
  }
  P.byUnit = byUnit;
  /* Problems are numbered straight through each section. */
  function renumber(plan) {
    plan.sections.forEach(function (s) { var n = 0; s.groups.forEach(function (g) { g.items.forEach(function (p) { p.num = ++n; }); }); });
  }
  P.allItems = function (plan) { var out = []; plan.sections.forEach(function (s) { s.groups.forEach(function (g) { g.items.forEach(function (p) { out.push(p); }); }); }); return out; };
  P.regenerate = function (plan, si, gi, ii) {
    var old = plan.sections[si].groups[gi].items[ii];
    var salt = (old.salt || 0) + 1;
    var p = makeProblem(plan, old.slot, old.entry, old.c || old.entry.cmin, salt);
    p.salt = salt; p.spiral = old.spiral; p.num = old.num;
    plan.sections[si].groups[gi].items[ii] = p;
    return p;
  };
  /* Fixed text for days without generated problems (launch tasks, routines, project checkpoints). */
  P.launchTask = function (d) {
    if (d.lesson_id === 'LAUNCH-1') return { title: 'Four 4s', student: 'Use exactly four 4s and any operations (+, −, ×, ÷, exponents, parentheses) to make each number from 1 to 10. Work with your group; record one expression for each number.', teacher: 'Groups of 3–4. Rotate roles (recorder, checker, reporter, materials). Share-out: which numbers were hardest, and how did order of operations matter?' };
    return { title: 'Handshake problem', student: 'Everyone in a group of 10 shakes hands with everyone else once. How many handshakes are there? Solve it for groups of 2, 3, 4 and 5 first. Look for a pattern, then predict 10 and 30.', teacher: 'Model a productive struggle: draw, make a table, find a pattern. Celebrate different strategies before anyone shows a formula.' };
  };
  P.routines = function (d) {
    if (d.lesson_id === 'LAUNCH-1') return [['Do Now', 'Starts when the bell rings: 3–5 problems on the board, about 5 minutes, done silently.'], ['Notes', 'Guided notes with blanks to fill in, plus worked examples (I do, we do, you try).'], ['Practice', 'We do problems together, then you do problems from easier to harder.'], ['Exit ticket', 'A summary sentence and 2–3 problems; hand it in on the way out.'], ['Getting help', 'Ask three before me; use your notes; flag a problem with a star.']];
    return [['When I am stuck', 'Reread, draw a picture, try a simpler number, make a table.'], ['In my group', 'Everyone talks, everyone writes, nobody is done until everyone is done.'], ['Mistakes', 'Mistakes show where to learn next; circle them, do not erase them.']];
  };
  P.projectCheckpoints = function (d) {
    return { 'END-6': ['Choose a question', 'Collect at least 10 data points', 'Make a scatter plot'], 'END-7': ['Choose a linear, exponential or quadratic model', 'Write the equation', 'Check residuals'], 'END-8': ['Prepare 3-minute presentation', 'Explain why your model fits', 'Answer one audience question'] }[d.lesson_id] || ['Set a goal', 'Work', 'Log progress'];
  };
  /* Notes: 'filled' (definitions, key idea and worked examples printed) or 'fill' (students write them in).
     The scope's notes_style decides the default: "Pre-filled reference notes" → filled, anything else → fill. */
  P.lessonNotesMode = function (d) { return /pre-filled/i.test(d.notes_style || '') ? 'filled' : 'fill'; };
  /* Minutes per part: {donow: 5, notes: 20, …}; a part not listed keeps its default. 0–180 minutes. */
  P.applyMinutes = function (plan, m) {
    plan.sections.forEach(function (s) {
      var v = m && m[s.id];
      s.minutes = v === undefined || v === null || v === '' || isNaN(+v) ? s.defaultMinutes : Math.max(0, Math.min(180, Math.round(+v)));
    });
    return plan;
  };
  P.totalMinutes = function (plan) { return plan.sections.reduce(function (n, s) { return n + (s.minutes || 0); }, 0); };
  P.summary = function (plan) {
    var all = P.allItems(plan);
    return { problems: all.length, failed: all.filter(function (p) { return p.failed; }).length, unverified: all.filter(function (p) { return !p.failed && (!p.verify || p.verify.status !== 'verified'); }).length };
  };
})(typeof window !== 'undefined' ? window : globalThis);
