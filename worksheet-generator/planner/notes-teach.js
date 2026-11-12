/* Daily Lesson Planner — teaching notes (shared by Algebra 1, Geometry and Algebra 2).

   Each Lesson day's Notes teach the lesson: a big idea, one or more explanation cards (what it means, the steps,
   an exact diagram), worked examples made by the same verified generators / approved bank as the problems,
   the vocabulary and the "watch out" mistake. The content lives in notes-teach-<course>.js:

     MKPLAN_TEACH.<course>['<lesson id>'] = card | [card, …]
       card = { h: heading, big: explanation, steps: [ … ], figs: [diagram spec, …] }
     Text may hold ⟨TeX⟩ math and {{blanks}}: a {{…}} is printed on completed notes and on the teacher sheet
     (highlighted there) and is a blank to fill in on guided notes. Diagram labels use the same {{…}} marks.

   MKPLAN.teachCards(day)          the cards for a lesson day (teacher edits applied)
   MKPLAN.guidedStep(step)         {lead, blank} for a worked-example step: what is printed and what is left blank
   MKPLAN.NOTE_MODES               the two student-sheet choices */
(function (G) {
  'use strict';
  var P = (G.MKPLAN = G.MKPLAN || {});
  var DATA = G.MKPLAN_TEACH = G.MKPLAN_TEACH || {};
  P.NOTE_MODES = { filled: 'Completed notes', fill: 'Guided notes' };
  P.noteModeName = function (mode) { return mode === 'filled' ? 'Completed notes' : 'Guided notes'; };
  function course() { return G.MKPLAN_COURSE || 'algebra1'; }
  /* A record is keyed by lesson id; Algebra 2 records are keyed by the lesson's catalog skill. */
  P.teachRecord = function (lessonId) {
    var c = DATA[course()] || {};
    if (c[lessonId]) return c[lessonId];
    var m = G.MKPLAN_SKILLS && G.MKPLAN_SKILLS.lessons && G.MKPLAN_SKILLS.lessons[lessonId];
    var sk = m && m.skills && m.skills[0] && m.skills[0][1];
    return sk && c[sk] ? c[sk] : null;
  };
  P.hasTeachNotes = function (lessonId) { return !!P.teachRecord(lessonId); };
  P.teachCards = function (d) {
    if (!d) return [];
    var rec = P.teachRecord(d.lesson_id), cards = rec ? (Array.isArray(rec) ? rec : rec.cards ? rec.cards : [rec]) : [];
    cards = cards.map(function (c) { return { h: c.h || d.title, big: c.big || '', steps: (c.steps || []).slice(), figs: (c.figs || []).slice() }; });
    if (!cards.length) {
      var idea = P.keyIdea ? P.keyIdea(d.lesson_id) : '';
      if (idea) cards = [{ h: d.title, big: idea, steps: [], figs: [], fallback: true }];
    }
    var e = P.noteEdits && P.noteEdits[d.lesson_id];
    if (e && Array.isArray(e.cards)) e.cards.forEach(function (ce, i) {
      if (!cards[i] || !ce) return;
      if (typeof ce.big === 'string') cards[i].big = ce.big;
      if (Array.isArray(ce.steps)) cards[i].steps = ce.steps.filter(function (x) { return String(x).trim(); });
    });
    return cards;
  };

  /* Algebra 2: the catalog has no glossary or key ideas, so the teaching-notes record supplies them
     (a teacher's saved edit still wins). */
  if ((course() === 'algebra2' || /^grade[1-5]$/.test(course())) && P.define && P.keyIdea) {
    var baseDefine = P.define, baseIdea = P.keyIdea;
    P.define = function (term, day) {
      var e = day && day.lesson_id && P.noteEdits && P.noteEdits[day.lesson_id];
      if (e && Array.isArray(e.words)) return baseDefine(term, day);
      var r = day && P.teachRecord(day.lesson_id), t = String(term || '').trim().toLowerCase();
      var hit = r && r.voc && r.voc.filter(function (w) { return w[0].toLowerCase() === t; })[0];
      return hit ? hit[1] : baseDefine(term, day);
    };
    P.keyIdea = function (lessonId) {
      var e = P.noteEdits && P.noteEdits[lessonId];
      if (e && typeof e.idea === 'string') return e.idea;
      var r = P.teachRecord(lessonId);
      return r && r.idea ? r.idea : baseIdea(lessonId);
    };
  }

  /* Worked-example steps on guided notes: keep the description and the left side, blank the result.
     Math: the part after the last top-level = < > ≤ ≥ ≠ ≈ is blank (the whole line when there is none).
     Text-only steps (approved bank): the part after the last "=" is blank; a step without one is printed. */
  var REL = /(=|\\le(?![a-z])|\\ge(?![a-z])|\\leq|\\geq|\\ne(?![a-z])|\\neq|\\approx|<|>|≤|≥|≠|≈)/g;
  function lastTopRel(m) {
    var depth = 0, best = -1, len = 0, i, re = new RegExp(REL.source, 'g'), mm;
    var level = []; for (i = 0; i < m.length; i++) { var ch = m.charAt(i); if (ch === '{' || ch === '(' || ch === '[') depth++; else if (ch === '}' || ch === ')' || ch === ']') depth--; level.push(depth); }
    while ((mm = re.exec(m))) { if (level[mm.index] === 0 && m.slice(mm.index).replace(/\s/g, '').length > mm[0].length) { best = mm.index; len = mm[0].length; } }
    return best < 0 ? null : { i: best, len: len };
  }
  P.guidedStep = function (st) {
    st = st || {};
    if (st.m) {
      var r = lastTopRel(String(st.m));
      if (r) return { t: st.t || '', m: st.m.slice(0, r.i + r.len), blank: st.m.slice(r.i + r.len), mathBlank: true };
      return { t: st.t || '', m: '', blank: st.m, mathBlank: true };
    }
    var t = String(st.t || ''), k = t.lastIndexOf('=');
    if (k > 0 && k < t.length - 1 && !/[⟨⟩]/.test(t.slice(k))) return { t: t.slice(0, k + 1), m: '', blank: t.slice(k + 1).replace(/\.\s*$/, ''), mathBlank: false };
    return { t: t, m: '', blank: '', mathBlank: false };
  };
})(typeof window !== 'undefined' ? window : globalThis);
