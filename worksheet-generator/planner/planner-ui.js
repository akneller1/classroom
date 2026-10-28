/* Daily Lesson Planner — page (DOM).

   Left: pick a day (by unit), class level, number of practice problems, new problems, print.
   Right: three views of the day —
     Plan            the teacher's plan with every problem, its answer and a "New problem" button
     Student handout one printable packet: Do Now · Notes · Practice · Exit ticket
     Teacher key     the plan page + every answer with worked steps
   URL: lesson-planner.html#day=<n>&level=<cp2|cp1|honors>&seed=<s>   or   #unit=<skill set id> (first day of that unit). */
(function (G) {
  'use strict';
  var doc = G.document, NS = G.MKMENU, WS = G.MKWS, P = G.MKPLAN, SC = G.MKPLAN_SCOPE;
  var KEY_LEVEL = 'mk-planner-level', KEY_THEME = 'mkws-theme', KEY_N = 'mk-planner-practice', KEY_NOTES = 'mk-planner-notes', KEY_MIN = 'mk-planner-minutes', KEY_NOTE_EDITS = 'mk-planner-note-edits', KEY_SECTIONS = 'mk-planner-sections-v1', KEY_SECTION_ORDER = 'mk-planner-section-order-v1', KEY_PROBLEM_LABELS = 'mk-planner-problem-labels-v1', KEY_COUNTS = 'mk-planner-section-counts-v1';
  function lsGet(k) { try { return G.localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { G.localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  function $(s) { return doc.querySelector(s); }
  function esc(s) { return String(s === undefined || s === null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var ms = function (s) { return NS.mathSafe(s); };

  var ui = { day: 4, level: lsGet(KEY_LEVEL) || 'cp1', seed: 'A', practice: +(lsGet(KEY_N) || 10), view: 'plan', plan: null, notes: lsGet(KEY_NOTES) || 'lesson' };
  if (!/^(lesson|fill|filled)$/.test(ui.notes)) ui.notes = 'lesson';
  ui.selectedDays = [ui.day];
  function resetSelection() { ui.selectedDays = [ui.day]; }

  var sectionLabels = { donow:'Do Now', mixed:'Mixed Review', notes:'Notes', examples:'Examples', practice:'Practice', challenge:'Challenge Problems', summary:'Lesson Summary', exit:'Exit Ticket' };
  var sectionChoices = { donow:true, mixed:false, notes:true, examples:true, practice:true, challenge:false, summary:false, exit:true };
  try { var savedSections = JSON.parse(lsGet(KEY_SECTIONS) || '{}'); Object.keys(sectionChoices).forEach(function(k) { if (typeof savedSections[k] === 'boolean') sectionChoices[k] = savedSections[k]; }); } catch(e) {}
  var sectionOrder = (function() {
    var base = Object.keys(sectionChoices);
    try {
      var stored = JSON.parse(lsGet(KEY_SECTION_ORDER) || 'null');
      if (Array.isArray(stored)) {
        var valid = stored.filter(function(k, i) { return base.indexOf(k) >= 0 && stored.indexOf(k) === i; });
        var ordered = valid.concat(base.filter(function(k) { return valid.indexOf(k) < 0; }));
        if (valid.indexOf('challenge') < 0) { ordered.splice(ordered.indexOf('challenge'), 1); var afterPractice = ordered.indexOf('practice'); ordered.splice(afterPractice < 0 ? ordered.length : afterPractice + 1, 0, 'challenge'); }
        return ordered;
      }
    } catch(e) {}
    return base;
  })();
  var KEY_SEQUENCE = 'mk-planner-sequence-v1';
  var sectionSequence = (function() {
    try { var v = JSON.parse(lsGet(KEY_SEQUENCE) || 'null');
      if (Array.isArray(v) && v.length && v.length <= 30 && v.every(function(k) { return k in sectionChoices; })) return v;
    } catch(e) {}
    return sectionOrder.slice();
  })();
  function saveSequence() { lsSet(KEY_SEQUENCE, JSON.stringify(sectionSequence)); }
  function applySectionChoices(plan) {
    var original = {};
    plan.sections.forEach(function(s) { original[s.id] = s; });
    var occurrences = {};
    plan.sections = sectionSequence.filter(function(id) { return sectionChoices[id] && original[id]; }).map(function(id) {
      var n = occurrences[id] = (occurrences[id] || 0) + 1;
      if (n === 1) return original[id];
      var s = Object.assign({}, original[id]);
      s.title = s.title + ' (' + n + ')';
      s.groups = original[id].groups.map(function(g) {
        return Object.assign({}, g, {items:g.items.map(function(p) { return Object.assign({}, p); })});
      });
      return s;
    });
    plan.sections.forEach(function(s, si) {
      if (!/\\(\\d+\\)$/.test(s.title)) return;
      s.groups.forEach(function(g, gi) { g.items.forEach(function(p, pi) {
        if (p.entry) P.regenerate(plan, si, gi, pi);
      }); });
    });
  }

  var problemCounts = (function() {
    try { var v = JSON.parse(lsGet(KEY_COUNTS) || '{}'); return v && typeof v === 'object' && !Array.isArray(v) ? v : {}; }
    catch(e) { return {}; }
  })();
  function totalProblems(section) {
    return section ? section.groups.reduce(function(n, g) { return n + g.items.length; }, 0) : null;
  }
  function problemCountInput(id) {
    if (['donow','mixed','examples','practice','challenge','exit'].indexOf(id) < 0) return '';
    var section = ui.plan && ui.plan.sections.find(function(s) { return s.id === id; });
    var count = Object.prototype.hasOwnProperty.call(problemCounts,id) ? problemCounts[id] : totalProblems(section);
    var unavailable = !section || (!totalProblems(section) && !Object.prototype.hasOwnProperty.call(problemCounts,id));
    if (count == null) count = 0;
    return '<label class="pl-hint" style="display:flex;align-items:center;gap:4px;margin:0">Problems <input type="number" data-problem-count="' + id +
      '" min="0" max="30" step="1" value="' + count + '"' + (unavailable ? ' disabled title="No generated problems for this lesson section"' : '') +
      ' aria-label="Number of problems in ' + esc(sectionLabels[id]) + '" style="width:68px;max-width:68px;padding:5px"></label>';
  }
  /* Minutes the teacher typed, remembered per day type (a Lesson-day timing applies to every Lesson day). */
  var minutesStore = (function () { try { return JSON.parse(lsGet(KEY_MIN) || '{}') || {}; } catch (e) { return {}; } })();
  function minutesFor(d) { return minutesStore[d.day_type] || null; }
  function saveMinutes(d, secId, v) {
    var m = minutesStore[d.day_type] = minutesStore[d.day_type] || {};
    if (v === null) delete m[secId]; else m[secId] = v;
    if (!Object.keys(m).length) delete minutesStore[d.day_type];
    lsSet(KEY_MIN, JSON.stringify(minutesStore));
  }
  var problemLabels = (function () { try { return JSON.parse(lsGet(KEY_PROBLEM_LABELS) || '{}') || {}; } catch(e) { return {}; } })();
  function labelKey(day, section, group, index) { return day + ':' + section + ':' + group + ':' + index; }
  function applyProblemLabels(plan) {
    plan.sections.forEach(function(s) { s.groups.forEach(function(g, gi) { g.items.forEach(function(p, pi) {
      p.teacherLabel = problemLabels[labelKey(plan.day.day, s.id, gi, pi)] || '';
    }); }); });
  }
  function displayProblemLabel(p, fallback) { return fallback + (p.teacherLabel ? ' · ' + p.teacherLabel : ''); }
  function problemLabelPicker(plan, p, s, gi, pi) {
    var values = ['', 'I do', 'We do', 'You do'];
    return '<label class="pl-problem-label">Instructional label <select data-problem-label="' + esc(s.id) + '" data-group="' + gi + '" data-item="' + pi + '" aria-label="Label for ' + esc(s.title) + ' problem ' + p.num + '">' +
      values.map(function(v) { return '<option value="' + esc(v) + '"' + (p.teacherLabel === v ? ' selected' : '') + '>' + (v ? esc(v) : 'No label') + '</option>'; }).join('') +
      '</select></label>';
  }
  function filled(plan) { return plan.notesMode === 'filled'; }
  /* Notes the teacher edited, per lesson, kept in this browser (MKPLAN.noteEdits is read by define/keyIdea/vocab). */
  P.noteEdits = (function () { try { return JSON.parse(lsGet(KEY_NOTE_EDITS) || '{}') || {}; } catch (e) { return {}; } })();
  function saveNoteEdits() { lsSet(KEY_NOTE_EDITS, JSON.stringify(P.noteEdits)); }
  function editRecord(d) {   // the first edit copies the current notes so later edits change one field at a time
    if (!P.noteEdits[d.lesson_id]) { var n = P.lessonNotes(d); P.noteEdits[d.lesson_id] = { words: n.words.map(function (w) { return w.slice(); }), idea: n.idea, watch: n.watch, extra: n.extra }; }
    return P.noteEdits[d.lesson_id];
  }
  function notesEditor(plan) {
    var d = plan.day, n = P.lessonNotes(d);
    return '<div class="pl-noted" id="plNoted"><div class="pl-noted-hd"><b>Notes</b> <span class="pl-hint">Edit anything below. Your changes are saved in this browser and used on the handout, the key and the slides.</span>' +
      ' <button type="button" class="link" id="plNotesReset"' + (P.notesEdited(d) ? '' : ' hidden') + '>Reset to the original notes</button></div>' +
      '<label class="pl-nl">Key idea<textarea data-n="idea" rows="2">' + esc(n.idea) + '</textarea></label>' +
      '<div class="pl-nl">Vocabulary</div><table class="pl-ntbl"><thead><tr><th>Word</th><th>What it means / example</th><th></th></tr></thead><tbody>' +
      n.words.map(function (w, i) { return '<tr><td><input type="text" data-n="w" data-i="' + i + '" value="' + esc(w[0]) + '" aria-label="Word ' + (i + 1) + '"></td><td><textarea data-n="d" data-i="' + i + '" rows="2" aria-label="Meaning of ' + esc(w[0]) + '">' + esc(w[1]) + '</textarea></td><td><button type="button" class="btn ghost sm pl-delword" data-i="' + i + '" aria-label="Remove ' + esc(w[0]) + '">✕</button></td></tr>'; }).join('') +
      '</tbody></table><button type="button" class="btn ghost sm" id="plAddWord">+ Add a word</button>' +
      '<label class="pl-nl">Watch out (common mistake)<textarea data-n="watch" rows="2">' + esc(n.watch) + '</textarea></label>' +
      '<label class="pl-nl">My notes <small>(printed on the handout and the slides; leave blank for none)</small><textarea data-n="extra" rows="3" placeholder="Anything else students should write down: a rule, a diagram description, a reminder…">' + esc(n.extra) + '</textarea></label></div>';
  }
  if (!NS.LEVELS[ui.level]) ui.level = 'cp1';

  /* ---------- groups of days for the picker ---------- */
  function dayGroups() {
    var out = [{ key: 'launch', name: 'Course launch (days 1–3)', days: [] }];
    SC.units.forEach(function (u) { out.push({ key: 'u' + u.unit, name: 'Unit ' + u.unit + ': ' + u.title + ' (days ' + u.start_day + '–' + u.end_day + ')', days: [] }); });
    out.push({ key: 'sem', name: 'Semester review & exam (days 87–90)', days: [] }, { key: 'final', name: 'Final review, exam & project (days 172–180)', days: [] });
    SC.days.forEach(function (d) {
      var k = d.unit ? 'u' + d.unit : d.day <= 3 ? 'launch' : d.day < 100 ? 'sem' : 'final';
      out.filter(function (g) { return g.key === k; })[0].days.push(d);
    });
    return out;
  }
  function groupKey(d) { return d.unit ? 'u' + d.unit : d.day <= 3 ? 'launch' : d.day < 100 ? 'sem' : 'final'; }
  var TYPE_CLS = { Lesson: 'lesson', Practice: 'practice', Quiz: 'quiz', Review: 'review', Assessment: 'test', Flex: 'flex', Launch: 'launch', Diagnostic: 'launch', 'Exam Review': 'review', Exam: 'test', Project: 'project' };

  /* ---------- hash ---------- */
  function readHash() {
    var h = {}; (location.hash || '').replace(/^#/, '').split('&').forEach(function (kv) { var p = kv.split('='); if (p[0]) h[decodeURIComponent(p[0])] = decodeURIComponent(p[1] || ''); });
    if (h.unit) {
      var num = null; Object.keys(G.MKPLAN_SKILLS.UNIT_SET).forEach(function (n) { if (P.unitSetId(+n) === h.unit || String(n) === h.unit) num = +n; });
      var u = num && P.unitOf(num); if (u) ui.day = u.start_day;
    }
    if (h.day && P.day(+h.day)) ui.day = +h.day;
    if (h.level && NS.LEVELS[h.level]) ui.level = h.level;
    if (h.seed) ui.seed = h.seed.slice(0, 12);
    if (h.view && /^(plan|student|key)$/.test(h.view)) ui.view = h.view;
  }
  function writeHash() {
    var h = '#day=' + ui.day + '&level=' + ui.level + (ui.seed !== 'A' ? '&seed=' + encodeURIComponent(ui.seed) : '') + (ui.view !== 'plan' ? '&view=' + ui.view : '');
    if (location.hash !== h) history.replaceState(null, '', h);
  }

  /* ---------- problem pieces ---------- */
  function promptHtml(p) {
    if (p.failed) return '<div class="pl-missing">No verified problem for this slot (' + esc(p.reason || '') + '). Click “New problem” or write your own.</div>';
    var h = '<div class="pl-q">' + ms(p.prompt || '') + '</div>';
    if (p.work && p.work.length) h += '<ol class="mm-work-lines">' + p.work.map(function (w, i) { return '<li><span>Line ' + (i + 1) + ':</span> ' + ms('⟨' + w + '⟩') + '</li>'; }).join('') + '</ol>';
    if (p.fig) h += NS.figHtml(p.fig);
    var parts = (p.parts || []).filter(function (pt) { return pt.prompt; });
    if (parts.length) h += '<div class="pl-parts">' + parts.map(function (pt) { return '<div><b>' + (pt.label ? '(' + esc(pt.label) + ')' : '') + '</b> ' + ms(pt.prompt) + '</div>'; }).join('') + '</div>';
    return h;
  }
  function answerHtml(p) {
    if (p.failed) return '';
    var parts = p.parts || [];
    return '<div class="pl-ans"><b>Answer:</b> ' + parts.map(function (pt) { return (parts.length > 1 && pt.label ? '<b>(' + esc(pt.label) + ')</b> ' : '') + ms(pt.answer || '') + (pt.answerFig ? NS.figHtml(pt.answerFig) : ''); }).join(' &nbsp; ') + '</div>';
  }
  function stepsHtml(p) {
    var st = (p.steps || []).filter(function (s) { return s.t || s.m; });
    if (!st.length) return '';
    return '<ol class="pl-steps">' + st.map(function (s) { return '<li>' + ms(s.t || '') + (s.m ? ' ' + ms('⟨' + s.m + '⟩') : '') + '</li>'; }).join('') + '</ol>';
  }
  function wide(p) { return (p.parts || []).filter(function (x) { return x.prompt; }).length > 1 || (p.prompt || '').replace(/⟨[^⟩]*⟩/g, 'xxxxxxxx').length > 140 || (p.fig && /twoway/.test(p.fig.kind)); }
  function lessonTitle(id) { var l = P.lessonById(id); return l ? l.title : id; }
  function levelName() { return NS.LEVELS[ui.level].name; }
  function lines(n, label) { var h = '<div class="pl-lines">'; for (var i = 0; i < n; i++) h += '<div class="pl-line">' + (i === 0 && label ? '<span>' + esc(label) + '</span>' : '') + '</div>'; return h + '</div>'; }
  function frameHtml(f) { return esc(f || '').replace(/_{2,}/g, '<span class="pl-blank"></span>'); }

  /* ---------- the plan view (teacher, interactive) ---------- */
  function planInfo(plan) {
    var d = plan.day, T = P.template(d), u = d.unit ? P.unitOf(d.unit) : null;
    var meta = [['Standards', esc(d.standards)], ['Content objective', esc(d.content_objective)], ['Language objective', esc(d.language_objective)]];
    if (d.sentence_frame) meta.push(['Sentence frame', '<i>' + frameHtml(d.sentence_frame) + '</i>']);
    if (d.key_vocabulary) meta.push(['Key vocabulary', P.vocab(d).map(function (v) { return '<span class="pl-chip">' + esc(v) + '</span>'; }).join(' ')]);
    if (P.watchOut(d)) meta.push(['Watch for', esc(P.watchOut(d))]);
    if (d.notes_style) meta.push(['Notes style', esc(d.notes_style)]);
    if (d.do_now_strategy) meta.push(['Do Now strategy', esc(d.do_now_strategy) + ((d.do_now_source_ids || []).length ? ' — from ' + d.do_now_source_ids.map(function (id) { return '<span class="pl-chip" title="' + esc(lessonTitle(id)) + '">' + esc(id) + '</span>'; }).join(' ') : '') + ((d.spiral_review_ids || []).length ? '; spiral ' + d.spiral_review_ids.map(function (id) { return '<span class="pl-chip" title="' + esc(lessonTitle(id)) + '">' + esc(id) + '</span>'; }).join(' ') : '')]);
    var changed = plan.sections.some(function (s) { return s.minutes !== s.defaultMinutes; });
    var agenda = '<table class="pl-agenda"><thead><tr><th>Part</th><th>Minutes</th><th>What happens</th></tr></thead><tbody>' + plan.sections.map(function (s, si) {
      return '<tr><td><b>' + esc(s.title) + '</b></td><td><input type="number" class="pl-mins" min="0" max="180" step="1" data-s="' + si + '" value="' + (s.minutes || 0) + '" aria-label="Minutes for ' + esc(s.title) + '"></td><td>' + esc(s.template || '') + '</td></tr>';
    }).join('') + '<tr class="pl-total"><td><b>Total</b></td><td><b id="plTotal">' + P.totalMinutes(plan) + '</b> min</td><td>' +
      '<span class="pl-hint">Times you change are kept for every ' + esc(d.day_type) + ' day.</span>' + ' <button type="button" class="link" id="plResetMin"' + (changed ? '' : ' hidden') + '>Reset to the planned times</button>' + '</td></tr></tbody></table>';
    var cov = plan.coverage.filter(function (c) { return c.cover !== 'full'; });
    var covHtml = cov.length ? '<div class="pl-cover"><b>Generator coverage</b>' + cov.map(function (c) { return '<div><span class="pl-chip ' + c.cover + '">' + esc(c.id) + ' · ' + (c.cover === 'none' ? 'not covered' : 'partly covered') + '</span> ' + esc(c.note) + '</div>'; }).join('') + '</div>' : '';
    var res = resourceLinks(plan);
    return '<div class="pl-info card">' +
      '<dl class="pl-meta">' + meta.map(function (m) { return '<dt>' + m[0] + '</dt><dd>' + m[1] + '</dd>'; }).join('') + '</dl>' + agenda + covHtml + res + '</div>';
  }
  function resourceLinks(plan) {
    var set = plan.unitSet, d = plan.day, links = [];
    if (set) {
      links.push(['Worksheet Generator', 'worksheet.html#unit=' + set], ['Assessment Generator', 'menu-assessment.html#unit=' + set]);
      if (/Practice|Review|Flex/.test(d.day_type)) links.push(['Maze', 'printables.html#unit=' + set + '&kind=maze'], ['Partner Check', 'printables.html#unit=' + set + '&kind=partner'], ['Stations', 'printables.html#unit=' + set + '&kind=stations']);
      if (/Quiz/.test(d.day_type)) links.splice(2, 0, ['Short quiz (versions A–C)', 'menu-assessment.html#unit=' + set]);
      links.push(['Unit page', '../index.html#algebra.' + unitPageId(d.unit)]);
    } else if (/Exam/.test(d.day_type)) {
      links.push(['Assessment Generator', 'menu-assessment.html']);
    }
    if (!links.length) return '';
    return '<div class="pl-res"><b>Unit resources</b> ' + links.map(function (l) { return '<a class="btn ghost sm" href="' + esc(l[1]) + '">' + esc(l[0]) + '</a>'; }).join(' ') + '</div>';
  }
  var UNIT_PAGE = { 1: 'foundations-algebra', 2: 'expressions-equations', 3: 'inequalities', 4: 'relations-functions', 5: 'linear-equations-slope', 6: 'systems-of-equations', 7: 'exponents-exponential-functions', 8: 'exponential-functions', 9: 'polynomials-factoring', 10: 'factoring-zero-product', 11: 'quadratics', 12: 'statistics-data-modeling' };
  function unitPageId(n) { return UNIT_PAGE[n] || ''; }

  function planView(plan) {
    var h = planInfo(plan);
    plan.sections.forEach(function (s, si) {
      h += '<section class="pl-sec card"><div class="pl-sechd"><h2>' + esc(s.title) + '</h2>' + '<span class="pl-min" data-min="' + si + '">' + (s.minutes ? s.minutes + ' min' : '') + '</span>' + '<span class="pl-tpl">' + esc(s.template || '') + '</span></div>';
      h += sectionTeacherExtras(plan, s);
      s.groups.forEach(function (g, gi) {
        if (g.name || g.note) h += '<h3 class="pl-grp">' + esc(g.name) + (g.note ? ' <small>' + esc(g.note) + '</small>' : '') + '</h3>';
        h += '<div class="pl-cards">' + g.items.map(function (p, ii) {
          return '<article class="pl-card' + (p.failed ? ' failed' : '') + '"><div class="pl-chd"><b>' + p.num + '.</b> <span class="pl-skill">' + esc(p.skillName) + ' · ' + esc(p.lesson) + (p.spiral ? ' · spiral' : '') + '</span>' +
            (p.failed ? '<span class="pl-badge bad">not verified</span>' : '<span class="pl-badge ok" title="Answer re-derived from the printed problem">✓ checked</span>') + '<span class="pl-diff">c' + (p.c || '') + '</span></div>' +
            promptHtml(p) + (p.challengeQuestion ? '<p class="pl-prompt"><b>Go further:</b> ' + esc(p.challengeQuestion) + '</p>' : '') + answerHtml(p) + problemLabelPicker(plan, p, s, gi, ii) + '<button type="button" class="btn ghost sm pl-regen" data-s="' + si + '" data-g="' + gi + '" data-i="' + ii + '">New problem</button></article>';
        }).join('') + '</div>';
      });
      h += '</section>';
    });
    return h;
  }
  function sectionTeacherExtras(plan, s) {
    var d = plan.day, out = '';
    if (s.prompt) out += '<p class="pl-prompt">Prompt: <i>' + esc(s.prompt) + '</i></p>';
    if (s.id === 'notes' && d.day_type === 'Lesson') {
      out += notesEditor(plan);
      out += '<p class="pl-hint">Student notes: <b>' + (filled(plan) ? 'pre-filled' : 'students write them in') + '</b> (change under Options).</p>';

      out += '<p class="pl-hint">Examples go from the level’s easiest to hardest: Example 1 I do, Example 2 we do' + (s.groups[0] && s.groups[0].items.length > 2 ? ', Example 3 you try' : '') + '.</p>';
    }
    if (s.frame) out += '<p class="pl-prompt">Summary frame: <i>' + frameHtml(s.frame) + '</i></p>';
    if (s.launch) out += '<p class="pl-prompt">' + esc(launchTask(d).teacher) + '</p>';
    if (s.project && s.id === 'practice') out += '<p class="pl-prompt">Checkpoints: ' + projectCheckpoints(d).map(esc).join(' · ') + '</p>';
    return out;
  }

  /* ---------- fixed text for non-problem parts ---------- */
  var launchTask = P.launchTask, routines = P.routines, projectCheckpoints = P.projectCheckpoints;

  /* Two problems per row; a row is a block that never splits across pages (grid items do not page-break reliably). */
  function rows(list) {
    var out = '', row = [];
    function flush() { if (row.length) { out += '<div class="pl-row">' + row.join('') + (row.length === 1 ? '<div class="pl-cell"></div>' : '') + '</div>'; row = []; } }
    list.forEach(function (x) { if (x.wide) { flush(); out += '<div class="pl-row one">' + x.html + '</div>'; } else { row.push(x.html); if (row.length === 2) flush(); } });
    flush();
    return out;
  }

  /* ---------- student handout (paper) ---------- */
  function studentProblem(p, label) {
    var space = p.failed ? 1 : Math.max(0.6, (p.space || [1, 1.3, 1.6])[1]);
    return '<div class="pl-p"><div class="pl-ph"><b>' + esc(label || (p.num + '.')) + '</b></div>' + (p.failed ? '<div class="pl-q">&nbsp;</div>' : promptHtml(p)) + (p.challengeQuestion ? '<p class="pl-challenge"><b>Challenge:</b> ' + esc(p.challengeQuestion) + '</p><div class="pl-space" style="height:1.0in"></div>' : '<div class="pl-space" style="height:' + space.toFixed(2) + 'in"></div>') + '</div>';
  }
  function workedProblem(p, label) {
    return '<div class="pl-p pl-worked"><div class="pl-ph"><b>' + esc(label) + '</b></div>' + promptHtml(p) + stepsHtml(p) + answerHtml(p) + '</div>';
  }
  function sheetHead(plan, kind) {
    var d = plan.day, u = d.unit ? 'Unit ' + d.unit + ': ' + d.unit_title : d.unit_title;
    return '<div class="pl-head"><div><div class="pl-title">' + esc(d.title) + '</div><div class="pl-sub">Algebra 1 · Day ' + d.day + ' · ' + esc(u) + (d.unit ? ' · day ' + esc(d.unit_day) : '') + ' · ' + esc(d.day_type) + '</div></div>' +
      (kind === 'key' ? '<span class="pl-tag key">Teacher key · ' + levelName() + '</span>' : '<span class="pl-tag">' + levelName() + '</span>') + '</div>' +
      (kind === 'key' ? '' : '<div class="pl-name"><span>Name <i></i></span><span>Date <i class="s"></i></span><span>Period <i class="s"></i></span></div>');
  }
  function studentSheet(plan) {
    var d = plan.day, h = sheetHead(plan, 'student');
    if (d.content_objective && !/Exam$|Assessment/.test(d.day_type)) h += '<div class="pl-ican"><b>Today:</b> ' + esc(P.iCan(d.content_objective)) + '</div>';
    plan.sections.forEach(function (s) {
      if (s.id === 'exit' || s.id === 'summary') return;
      h += '<div class="pl-sbox pl-s-' + s.id + '"><div class="pl-shd">' + esc(s.title) + (s.id === 'notes' && plan.day.day_type === 'Lesson' && !filled(plan) ? ' <small>· fill in as we go</small>' : '') + (s.minutes ? '<span>' + s.minutes + ' min</span>' : '') + '</div>';
      h += studentSectionBody(plan, s);
      h += '</div>';
    });
    var ex = plan.sections.filter(function (s) { return s.id === 'exit'; })[0];
    if (ex) h += '<div class="pl-exit"><div class="pl-cut">✂ cut here</div><div class="pl-shd">' + esc(ex.title) + '<span>Name ______________________</span></div>' + studentSectionBody(plan, ex) + '</div>';
    var summary = plan.sections.filter(function(s) { return s.id === 'summary'; })[0];
    if (summary) h += '<div class="pl-sbox pl-s-summary"><div class="pl-shd">' + esc(summary.title) + '</div>' + studentSectionBody(plan, summary) + '</div>';
    return '<div class="pl-sheet">' + h + '</div>';
  }
  function studentSectionBody(plan, s) {
    var d = plan.day, h = '';
    if (s.prompt) h += '<p class="pl-sprompt">' + esc(s.prompt) + '</p>' + (s.id === 'challenge' ? '' : lines(3));
    if (s.id === 'notes') h += notesBody(plan, s);
    if (s.launch) { var lt = launchTask(d); h += '<p class="pl-sprompt"><b>' + esc(lt.title) + '.</b> ' + esc(lt.student) + '</p><div class="pl-space" style="height:3.2in"></div>'; }
    if (s.project && s.id === 'practice') h += '<table class="pl-tbl"><thead><tr><th>Checkpoint</th><th>Done?</th><th>Notes</th></tr></thead><tbody>' + projectCheckpoints(d).map(function (c) { return '<tr><td>' + esc(c) + '</td><td class="pl-chk">☐</td><td></td></tr>'; }).join('') + '</tbody></table><div class="pl-space" style="height:1.6in"></div>';
    if (s.quiz) h += '<p class="pl-dir">Show your work for every problem. Box your final answer.</p>';
    s.groups.forEach(function (g) {
      if (g.name && s.id !== 'notes') h += '<div class="pl-gh">' + esc(g.name) + (g.note ? ' <small>' + esc(g.note) + '</small>' : '') + '</div>';
      if (s.id === 'notes') return;   // notes are drawn inside notesBody
      h += rows(g.items.map(function (p, i) { return { wide: s.id === 'challenge' || wide(p), html: s.id === 'examples' && filled(plan) && i < g.items.length - 1 && !p.failed ? workedProblem(p, displayProblemLabel(p, 'Example ' + (i + 1))) : studentProblem(p, s.id === 'examples' ? displayProblemLabel(p, 'Example ' + (i + 1)) : undefined) }; }));
    });
    if (s.frame) h += '<p class="pl-frame"><b>Summary:</b> ' + frameHtml(s.frame) + '</p>';
    if (s.selfAssess) h += rateTable(s.selfAssess, 'How sure am I?');
    if (s.confidence) h += rateTable(s.confidence, 'Confidence (1 = not yet, 4 = I could teach it)');
    if (s.iCan) h += '<ul class="pl-checklist">' + s.iCan.map(function (id) { var l = P.lessonById(id); return '<li>☐ ' + esc(l ? P.iCan(l.content_objective) : id) + '</li>'; }).join('') + '</ul>';
    if (s.iCanUnits) h += rateTable(s.iCanUnits.map(function (g) { return 'Unit ' + g.unit + ': ' + g.title; }), 'How ready am I?', true);
    if (s.id === 'exit' && s.prompt === undefined && !s.groups.length && !s.frame && !s.confidence) h += lines(3);
    return h;
  }
  function rateTable(ids, head, raw) {
    return '<table class="pl-tbl pl-rate"><thead><tr><th>' + (raw ? 'Topic' : 'Lesson') + '</th><th colspan="4">' + esc(head) + '</th></tr></thead><tbody>' +
      ids.map(function (id) { return '<tr><td>' + esc(raw ? id : (id === 'LAUNCH-2' ? 'Pre-algebra skills (expressions, equations, proportions)' : lessonTitle(id))) + '</td><td>1</td><td>2</td><td>3</td><td>4</td></tr>'; }).join('') + '</tbody></table>';
  }
  function notesBody(plan, s, singleDay) {
    if (!singleDay && plan.selectedDays && plan.selectedDays.length > 1 && !s.reference && !s.routines && !s.project && !s.corrections) {
      return plan.selectedDays.map(function(n) {
        var d = P.day(n);
        return d ? '<div class="pl-gh">' + esc(d.title) + '</div>' + notesBody(plan, s, d) : '';
      }).join('');
    }
    var d = singleDay || plan.day, h = '', voc = P.vocab(d);
    if (s.routines) return '<table class="pl-tbl"><tbody>' + routines(d).map(function (r) { return '<tr><th>' + esc(r[0]) + '</th><td>' + esc(r[1]) + '</td></tr>'; }).join('') + '</tbody></table>';
    if (s.project) return '<table class="pl-tbl"><thead><tr><th>Model</th><th>Pattern in the data</th><th>Equation</th></tr></thead><tbody><tr><td>Linear</td><td>constant differences (same amount added)</td><td>⟨y = mx + b⟩</td></tr><tr><td>Exponential</td><td>constant ratios (same factor multiplied)</td><td>⟨y = a·b^x⟩</td></tr><tr><td>Quadratic</td><td>constant second differences; rises then falls (or falls then rises)</td><td>⟨y = ax^2 + bx + c⟩</td></tr></tbody></table>'.replace(/⟨[^⟩]*⟩/g, function (m) { return ms(m); }) + '<div class="pl-gh">Rubric: model choice · equation · graph · explanation · presentation (4 points each)</div>';
    if (s.corrections) return '<table class="pl-tbl pl-corr"><thead><tr><th>#</th><th>My error</th><th>Correct work</th></tr></thead><tbody>' + [1, 2, 3, 4].map(function () { return '<tr><td></td><td></td><td></td></tr>'; }).join('') + '</tbody></table>';
    if (s.reference) {
      var groups = s.byUnit ? P.byUnit(s.reference) : [{ ids: s.reference }];
      return groups.map(function (g) {
        return (g.unit ? '<div class="pl-gh">Unit ' + g.unit + ': ' + esc(g.title) + '</div>' : '') + '<table class="pl-tbl pl-ref"><thead><tr><th>Lesson</th><th>Key vocabulary</th><th>' + (s.myExample ? 'My example' : 'Key idea / example') + '</th></tr></thead><tbody>' +
          g.ids.map(function (id) { var l = P.lessonById(id); return '<tr><td><b>' + esc(l ? l.title : id) + '</b></td><td>' + esc(l ? l.key_vocabulary : '') + '</td><td>' + (filled(plan) && !s.myExample ? esc(P.keyIdea(id)) : '') + '</td></tr>'; }).join('') + '</tbody></table>';
      }).join('');
    }
    var full = filled(plan), idea = P.keyIdea(d.lesson_id);
    if (voc.length) h += '<table class="pl-tbl pl-vocab' + (full ? ' filled' : '') + '"><thead><tr><th>Word</th><th>What it means / example</th></tr></thead><tbody>' + voc.map(function (v) { return '<tr><td><b>' + esc(v) + '</b></td><td>' + (full ? esc(P.define(v, d)) : '') + '</td></tr>'; }).join('') + '</tbody></table>';
    if (full) {
      if (idea) h += '<div class="pl-gh">Key idea</div><p class="pl-idea">' + esc(idea) + '</p>';
      if (P.watchOut(d)) h += '<p class="pl-watchout"><b>Watch out:</b> ' + esc(P.watchOut(d)) + '</p>';
    } else {
      if (/exploration/i.test(d.notes_style || '')) h += '<div class="pl-two"><div><div class="pl-gh">I notice…</div>' + lines(2) + '</div><div><div class="pl-gh">I wonder…</div>' + lines(2) + '</div></div>';
      h += '<div class="pl-gh">Key idea</div>' + lines(2);
    }
    if (P.myNotes(d)) h += '<div class="pl-mynotes">' + esc(P.myNotes(d)).replace(/\n/g, '<br>') + '</div>';
    return h;
  }

  /* ---------- teacher key (paper) ---------- */
  function keySheet(plan) {
    var d = plan.day, h = sheetHead(plan, 'key');
    var info = [['Standards', d.standards], ['Content objective', d.content_objective], ['Language objective', d.language_objective], ['Sentence frame', d.sentence_frame], ['Key vocabulary', d.key_vocabulary], ['Watch for', P.watchOut(d)], ['My notes', P.myNotes(d)], ['Notes style', d.notes_style], ['Do Now', d.do_now_strategy]].filter(function (r) { return r[1]; });
    if (P.keyIdea(d.lesson_id)) info.splice(4, 0, ['Key idea', P.keyIdea(d.lesson_id)]);
    var kv = P.vocab(d);
    if (kv.length && d.day_type === 'Lesson') info = info.map(function (r) { return r[0] === 'Key vocabulary' ? ['Key vocabulary', r[1], kv.map(function (v) { return '<b>' + esc(v) + '</b>: ' + esc(P.define(v, d)); }).join('<br>')] : r; });
    h += '<table class="pl-tbl pl-keyinfo"><tbody>' + info.map(function (r) { return '<tr><th>' + r[0] + '</th><td>' + (r[2] ? r[2] : r[0] === 'Sentence frame' ? frameHtml(r[1]) : esc(r[1])) + '</td></tr>'; }).join('') + '</tbody></table>';
    h += '<table class="pl-tbl pl-keyagenda"><thead><tr><th>Part</th><th>Min</th><th>What happens</th></tr></thead><tbody>' + plan.sections.map(function (s) { return '<tr><td><b>' + esc(s.title) + '</b></td><td>' + (s.minutes || '') + '</td><td>' + esc(s.template) + (s.prompt ? ' <i>Prompt: ' + esc(s.prompt) + '</i>' : '') + (s.launch ? ' ' + esc(launchTask(d).teacher) : '') + '</td></tr>'; }).join('') + '</tbody></table>';
    var cov = plan.coverage.filter(function (c) { return c.cover !== 'full'; });
    if (cov.length) h += '<div class="pl-keycov"><b>Add your own:</b> ' + cov.map(function (c) { return esc(c.note); }).join(' ') + '</div>';
    plan.sections.forEach(function (s) {
      var all = []; s.groups.forEach(function (g) { g.items.forEach(function (p) { all.push([g, p]); }); });
      if (!all.length) return;
      h += '<div class="pl-shd">' + esc(s.title) + ' — answers</div>';
      s.groups.forEach(function (g) {
        if (!g.items.length) return;
        if (g.name && s.id !== 'notes') h += '<div class="pl-gh">' + esc(g.name) + '</div>';
        h += rows(g.items.map(function (p) { return { wide: wide(p) && !!p.fig && /plane|twoway/.test(p.fig.kind), html: '<div class="pl-kitem"><div class="pl-ph"><b>' + (s.id === 'notes' ? displayProblemLabel(p, 'Example ' + p.num) : displayProblemLabel(p, p.num + '.')) + '</b> <small>' + esc(p.skillName) + ' · c' + (p.c || '') + '</small></div>' + promptHtml(p) + answerHtml(p) + stepsHtml(p) + '</div>' }; }));
      });
    });
    return '<div class="pl-sheet pl-key">' + h + '</div>';
  }

  /* ---------- page ---------- */
  function picker() {
    var cur = P.day(ui.day), gk = groupKey(cur), groups = dayGroups();
    var sel = '<label class="pl-lab" for="plUnit">Unit</label><select id="plUnit">' + groups.map(function (g) { return '<option value="' + g.key + '"' + (g.key === gk ? ' selected' : '') + '>' + esc(g.name) + '</option>'; }).join('') + '</select>';
    var g = groups.filter(function (x) { return x.key === gk; })[0];
    var list = '<p class="pl-hint">Choose a primary day, then check additional lessons in this unit to combine their problem banks.</p>' + '<ol class="pl-days" aria-label="Days">' + g.days.map(function (d) {
      return '<li>' + (d.day_type === 'Lesson' ? '<label style="display:inline-flex;align-items:center;margin-right:7px" title="Include this lesson"><input type="checkbox" data-lesson-day="' + d.day + '"' + (ui.selectedDays.indexOf(d.day) >= 0 ? ' checked' : '') + ' aria-label="Include ' + esc(d.title) + '"></label>' : '') + '<button type="button" class="pl-daybtn' + (d.day === ui.day ? ' on' : '') + '" data-day="' + d.day + '"' + (d.day === ui.day ? ' aria-current="true"' : '') + '><span class="pl-dnum">' + d.day + '</span><span class="pl-type t-' + TYPE_CLS[d.day_type] + '">' + esc(d.day_type) + '</span><span class="pl-dtitle">' + esc(d.title) + '</span></button></li>';
    }).join('') + '</ol>';
    return sel + list;
  }
  function controls() {
    var lv = ['cp2', 'cp1', 'honors'].map(function (id) { var L = NS.LEVELS[id]; return '<label class="pl-lv' + (ui.level === id ? ' on' : '') + '"><input type="radio" name="plLevel" value="' + id + '"' + (ui.level === id ? ' checked' : '') + '> <span><b>' + L.name + '</b> <small>' + esc(L.long.split('·')[1] || '') + '</small></span></label>'; }).join('');
    return '<fieldset class="pl-levels"><legend class="pl-lab">Class level</legend>' + lv + '</fieldset>' +
      '<fieldset class="pl-levels"><legend class="pl-lab">Student notes</legend>' + [['lesson', 'As planned', 'Pre-filled only where the scope says so'], ['fill', 'Students write them in', 'Blank definitions and key idea'], ['filled', 'Pre-filled', 'Definitions, key idea and worked examples printed']].map(function (o) {
        return '<label class="pl-lv' + (ui.notes === o[0] ? ' on' : '') + '"><input type="radio" name="plNotes" value="' + o[0] + '"' + (ui.notes === o[0] ? ' checked' : '') + '> <span><b>' + o[1] + '</b> <small>' + o[2] + '</small></span></label>';
      }).join('') + '</fieldset>' +
      '<fieldset class="pl-levels pl-section-options"><legend class="pl-lab">Include in lesson</legend><p class="pl-hint">Unchecked sections are omitted from the lesson preview, handout, teacher key, and PowerPoint.</p>' +
      sectionSequence.map(function(k, i) { return '<div class="pl-section-choice" style="display:flex;align-items:center;gap:8px;margin:7px 0"><label style="flex:1;display:flex;gap:7px;align-items:center"><input type="checkbox" data-section-toggle="' + k + '"' + (sectionChoices[k] ? ' checked' : '') + '> ' + esc(sectionLabels[k]) + '</label>' + problemCountInput(k) + '<button type="button" class="btn ghost sm" data-move-section="' + i + '" data-direction="-1"' + (i === 0 ? ' disabled' : '') + ' aria-label="Move ' + esc(sectionLabels[k]) + ' up">↑</button><button type="button" class="btn ghost sm" data-move-section="' + i + '" data-direction="1"' + (i === sectionSequence.length - 1 ? ' disabled' : '') + ' aria-label="Move ' + esc(sectionLabels[k]) + ' down">↓</button></div>'; }).join('') + '<p class="pl-hint">Use arrows to change the sequence. The order is saved and used in all exports.</p></fieldset>' +
      '<div class="pl-btns"><button type="button" class="btn sec2" id="plNew">New problems</button></div>' +
      '<div class="pl-btns"><button type="button" class="btn" id="plPrintS">Print student handout</button><button type="button" class="btn ghost" id="plPrintK">Print teacher key</button></div>' +
      '<div class="pl-btns"><button type="button" class="btn ghost" id="plPptxStudent">Student PowerPoint</button><button type="button" class="btn ghost" id="plPptxTeacher">Teacher PowerPoint</button></div><p id="plPptxMsg" class="pl-hint" role="status" aria-live="polite"></p>' +
      '<p class="hint">Every answer is re-derived from the printed problem by the same checker as the Worksheet and Assessment Generators.</p>';
  }
  function render() {
    var d = P.day(ui.day);
    if (!ui.selectedDays.length || ui.selectedDays.some(function(n) { var x = P.day(n); return !x || x.unit !== d.unit; })) resetSelection();
    ui.plan = P.buildDay(ui.day, { level: ui.level, seed: ui.seed, practice: ui.practice, selectedDays: ui.selectedDays, notes: ui.notes === 'lesson' ? null : ui.notes, minutes: minutesFor(d), include: sectionChoices, counts: problemCounts });
    applySectionChoices(ui.plan);
    applyProblemLabels(ui.plan);
    $('#plPick').innerHTML = picker();
    $('#plCtl').innerHTML = controls();
    var prev = P.day(ui.day - 1), next = P.day(ui.day + 1), sum = P.summary(ui.plan);
    $('#plHead').innerHTML = '<div class="pl-nav"><button type="button" class="btn ghost sm" id="plPrev"' + (prev ? '' : ' disabled') + '>← Day ' + (ui.day - 1) + '</button>' +
      '<div class="pl-htitle"><div class="pl-kicker">Day ' + d.day + ' · Quarter ' + d.quarter + ' · Week ' + d.week + (d.unit ? ' · Unit ' + d.unit + ', day ' + esc(d.unit_day) : ' · ' + esc(d.unit_title)) + '</div><h1>' + esc(d.title) + ' <span class="pl-type t-' + TYPE_CLS[d.day_type] + '">' + esc(d.day_type) + '</span></h1>' +
      (ui.plan.selectedLessonTitles.length > 1 ? '<p class="pl-hint">Combined lessons: ' + ui.plan.selectedLessonTitles.map(esc).join(' · ') + '</p>' : '') +
      '<div class="pl-stat">' + sum.problems + ' problems' + (sum.failed ? ' · <b class="bad">' + sum.failed + ' need a new problem</b>' : sum.problems ? ' · all answers checked' : '') + '</div></div>' +
      '<button type="button" class="btn ghost sm" id="plNext"' + (next ? '' : ' disabled') + '>Day ' + (ui.day + 1) + ' →</button></div>' +
      '<div class="pl-tabs" role="tablist">' + [['plan', 'Plan'], ['student', 'Student handout'], ['key', 'Teacher key']].map(function (t) { return '<button type="button" role="tab" class="tab" data-view="' + t[0] + '" aria-selected="' + (ui.view === t[0]) + '">' + t[1] + '</button>'; }).join('') + '</div>';
    renderView();
    var list = doc.querySelector('.pl-days'), on = doc.querySelector('.pl-daybtn.on');
    if (list && on) list.scrollTop = Math.max(0, on.getBoundingClientRect().top - list.getBoundingClientRect().top + list.scrollTop - list.clientHeight / 2 + on.offsetHeight / 2);
    writeHash();
    doc.title = 'Day ' + d.day + ': ' + d.title + ' · Daily Lesson Planner';
  }
  function renderView() {
    var v = $('#plView');
    v.className = 'pl-view v-' + ui.view;
    v.innerHTML = ui.view === 'plan' ? planView(ui.plan) : '<div class="pl-paperwrap">' + (ui.view === 'student' ? studentSheet(ui.plan) : keySheet(ui.plan)) + '</div>';
    Array.prototype.forEach.call(doc.querySelectorAll('.pl-tabs .tab'), function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-view') === ui.view)); });
  }
  function doPrint(kind) {
    var root = $('#printRoot');
    root.innerHTML = kind === 'student' ? studentSheet(ui.plan) : keySheet(ui.plan);
    doc.body.classList.add('printing');
    setTimeout(function () { G.print(); }, 60);
  }
  G.addEventListener('afterprint', function () { doc.body.classList.remove('printing'); $('#printRoot').innerHTML = ''; });

  doc.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('button') : null; if (!t) return;
    if (t.classList.contains('pl-daybtn')) { ui.day = +t.getAttribute('data-day'); resetSelection(); render(); $('#plView').scrollIntoView ? G.scrollTo(0, 0) : 0; return; }
    if (t.hasAttribute('data-move-section')) {
      var from = +t.getAttribute('data-move-section'), to = from + +t.getAttribute('data-direction');
      if (from >= 0 && to >= 0 && to < sectionSequence.length) {
        sectionSequence.splice(to, 0, sectionSequence.splice(from, 1)[0]);
        saveSequence(); render();
      }
      return;
    }
    if (t.id === 'plRepeat') {
      var id = $('#plRepeatType').value;
      if (id in sectionChoices && sectionSequence.length < 30) {
        sectionChoices[id] = true; sectionSequence.push(id);
        lsSet(KEY_SECTIONS, JSON.stringify(sectionChoices));
        saveSequence(); render();
      }
      return;
    }
    if (t.hasAttribute('data-remove-repeat')) {
      var i = +t.getAttribute('data-remove-repeat'), k = sectionSequence[i];
      if (sectionSequence.filter(function(x){return x === k;}).length > 1) {
        sectionSequence.splice(i,1); saveSequence(); render();
      }
      return;
    }
    if (t.id === 'plPrev') { ui.day--; resetSelection(); render(); return; }
    if (t.id === 'plNext') { ui.day++; resetSelection(); render(); return; }
    if (t.id === 'plNew') { ui.seed = Math.random().toString(36).slice(2, 7); render(); return; }
    if (t.id === 'plPrintS') { doPrint('student'); return; }
    if (t.id === 'plPrintK') { doPrint('key'); return; }
    if (t.id === 'plAddWord') { editRecord(ui.plan.day).words.push(['', '']); saveNoteEdits(); rerenderKeep(); var ins = doc.querySelectorAll('#plNoted input[data-n="w"]'); if (ins.length) ins[ins.length - 1].focus(); return; }
    if (t.classList.contains('pl-delword')) { editRecord(ui.plan.day).words.splice(+t.getAttribute('data-i'), 1); saveNoteEdits(); rerenderKeep(); return; }
    if (t.id === 'plNotesReset') { delete P.noteEdits[ui.plan.day.lesson_id]; saveNoteEdits(); rerenderKeep(); return; }
    if (t.id === 'plResetMin') { delete minutesStore[ui.plan.day.day_type]; lsSet(KEY_MIN, JSON.stringify(minutesStore)); P.applyMinutes(ui.plan, null); var y0 = G.scrollY; renderView(); G.scrollTo(0, y0); return; }
    if (t.id === 'plPptxStudent' || t.id === 'plPptxTeacher') {
      var audience = t.id === 'plPptxStudent' ? 'student' : 'teacher';
      var msg = $('#plPptxMsg'); t.disabled = true; msg.textContent = 'Building slides…';
      P.exportPptx(ui.plan, audience).then(function () { msg.textContent = 'Downloaded ' + P.deckFileName(ui.plan, audience) + '.'; }, function (err) { msg.textContent = 'Could not build the PowerPoint: ' + (err && err.message || err); }).then(function () { t.disabled = false; });
      return;
    }
    if (t.classList.contains('tab') && t.getAttribute('data-view')) { ui.view = t.getAttribute('data-view'); renderView(); writeHash(); return; }
    if (t.classList.contains('pl-regen')) {
      P.regenerate(ui.plan, +t.getAttribute('data-s'), +t.getAttribute('data-g'), +t.getAttribute('data-i'));
      var y = G.scrollY; renderView(); G.scrollTo(0, y); return;
    }
  });
  var noteTimer = null;
  doc.addEventListener('input', function (e) {
    var t = e.target, k = t.getAttribute && t.getAttribute('data-n');
    if (!k || !ui.plan) return;
    var rec = editRecord(ui.plan.day), i = +t.getAttribute('data-i');
    if (k === 'idea' || k === 'watch' || k === 'extra') rec[k] = t.value;
    else if (k === 'w') rec.words[i][0] = t.value;
    else if (k === 'd') rec.words[i][1] = t.value;
    $('#plNotesReset').hidden = false;
    clearTimeout(noteTimer); noteTimer = setTimeout(saveNoteEdits, 300);
  });
  function rerenderKeep() { var y = G.scrollY; renderView(); G.scrollTo(0, y); }
  doc.addEventListener('change', function (e) {
    var t = e.target;
    if (t.hasAttribute && t.hasAttribute('data-problem-count')) {
      var sectionId = t.getAttribute('data-problem-count');
      if (['donow','mixed','examples','practice','challenge','exit'].indexOf(sectionId) < 0) return;
      var v = Math.max(0, Math.min(30, Math.round(Number(t.value))));
      if (!isFinite(v) || t.value.trim() === '') return;
      problemCounts[sectionId] = v;
      lsSet(KEY_COUNTS, JSON.stringify(problemCounts));
      render();
      return;
    }
    if (t.hasAttribute && t.hasAttribute('data-section-toggle')) {
      var k = t.getAttribute('data-section-toggle'); if (!(k in sectionChoices)) return;
      sectionChoices[k] = t.checked;
      lsSet(KEY_SECTIONS, JSON.stringify(sectionChoices));
      render(); return;
    }
    if (t.hasAttribute && t.hasAttribute('data-problem-label')) {
      var sectionId = t.getAttribute('data-problem-label'), gi = +t.getAttribute('data-group'), pi = +t.getAttribute('data-item');
      var sec = ui.plan.sections.find(function(s) { return s.id === sectionId; });
      if (sec && sec.groups[gi] && sec.groups[gi].items[pi]) {
        var value = ['I do','We do','You do'].indexOf(t.value) >= 0 ? t.value : '';
        sec.groups[gi].items[pi].teacherLabel = value;
        var key = labelKey(ui.plan.day.day, sectionId, gi, pi);
        if (value) problemLabels[key] = value; else delete problemLabels[key];
        lsSet(KEY_PROBLEM_LABELS, JSON.stringify(problemLabels));
      }
      return;
    }
    if (t.hasAttribute && t.hasAttribute('data-lesson-day')) {
      var dayNo = +t.getAttribute('data-lesson-day');
      if (t.checked) { if (ui.selectedDays.indexOf(dayNo) < 0) ui.selectedDays.push(dayNo); }
      else { ui.selectedDays = ui.selectedDays.filter(function(n) { return n !== dayNo; }); }
      ui.selectedDays.sort(function(a,b) { return a-b; });
      if (!ui.selectedDays.length) ui.selectedDays = [ui.day];
      if (ui.selectedDays.indexOf(ui.day) < 0) ui.day = ui.selectedDays[0];
      render(); return;
    }
    if (t.id === 'plUnit') { var g = dayGroups().filter(function (x) { return x.key === t.value; })[0]; if (g && g.days.length) { ui.day = g.days[0].day; resetSelection(); render(); } return; }
    if (t.name === 'plLevel') { ui.level = t.value; lsSet(KEY_LEVEL, ui.level); render(); return; }
    if (t.name === 'plNotes') {   // the notes setting changes only the printed notes, not the problems
      ui.notes = t.value; lsSet(KEY_NOTES, ui.notes);
      ui.plan.notesMode = ui.notes === 'lesson' ? P.lessonNotesMode(ui.plan.day) : ui.notes;
      $('#plCtl').innerHTML = controls(); var y1 = G.scrollY; renderView(); G.scrollTo(0, y1); return;
    }
    if (t.classList && t.classList.contains('pl-mins')) {   // a minute box: keeps the problems, updates every view
      var si = +t.getAttribute('data-s'), sec = ui.plan.sections[si], v = Math.max(0, Math.min(180, Math.round(+t.value || 0)));
      sec.minutes = v; t.value = v;
      saveMinutes(ui.plan.day, sec.id, v === sec.defaultMinutes ? null : v);
      var hd = doc.querySelector('.pl-min[data-min="' + si + '"]'); if (hd) hd.textContent = v ? v + ' min' : '';
      $('#plTotal').textContent = P.totalMinutes(ui.plan);
      $('#plResetMin').hidden = !ui.plan.sections.some(function (x) { return x.minutes !== x.defaultMinutes; });
      return;   // the handout, key and slides read the minutes when they are shown or built
    }
    if (t.id === 'plN') { ui.practice = Math.max(4, Math.min(20, +t.value || 10)); lsSet(KEY_N, ui.practice); render(); return; }
  });
  G.addEventListener('hashchange', function () { readHash(); resetSelection(); render(); });

  function applyTheme(t) { if (t) doc.documentElement.setAttribute('data-theme', t); else doc.documentElement.removeAttribute('data-theme'); }
  applyTheme(lsGet(KEY_THEME));
  $('#themeBtn').onclick = function () {
    var cur = doc.documentElement.getAttribute('data-theme') || (G.matchMedia && G.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var nx = cur === 'dark' ? 'light' : 'dark'; applyTheme(nx); lsSet(KEY_THEME, nx);
  };
  readHash();
  resetSelection();
  render();
  P.ui = ui;   // for tests
})(window);
