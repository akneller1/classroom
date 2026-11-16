/* Shared teacher setup. Labels come from each game's own bank. */
(function (G) {
  'use strict';
  function text(value) {
    var el = G.document.createElement('div');
    el.innerHTML = String(value || '');
    return el.textContent.replace(/\s+/g, ' ').trim();
  }
  function applyStudentFocus() {
    var doc = G.document, params = new URLSearchParams(G.location.search);
    if (params.get('student') !== '1' || params.get('teacherShare') === '1' || !doc.documentElement || !doc.head) return;
    doc.documentElement.classList.add('student-focus');
    var style = doc.createElement('style');
    style.textContent = 'html.student-focus .gm-eyebrow,html.student-focus .topbar,html.student-focus .home-button,html.student-focus .back-button,html.student-focus .brand-link,html.student-focus #activityHeader{display:none!important}';
    doc.head.appendChild(style);
    var pathname = G.location.pathname;
    var marker = pathname.indexOf('/artifacts/');
    if (marker < 0) marker = pathname.indexOf('/worksheet-generator/');
    var root = marker < 0 ? G.location.origin : pathname.slice(0, marker);
    function cleanLinks() {
      Array.prototype.slice.call(doc.querySelectorAll('a')).forEach(function (a) {
        var label = (a.textContent || '').toLowerCase();
        var href = a.getAttribute('href') || '';
        var target;
        try { target = new URL(href, G.location.href); } catch (e) { return; }
        var home = target.origin === G.location.origin && (target.pathname === root + '/' || target.pathname === root + '/index.html');
        var classroomLabel = label.indexOf('mr. k') >= 0 || label.indexOf('mr k') >= 0 || label.indexOf('classroom') >= 0 || label.indexOf('back to class') >= 0 || label.indexOf('return home') >= 0;
        if (home || classroomLabel) a.remove();
      });
      var heading = doc.querySelector('h1:not([data-static-h1])');
      var docTitle = (doc.title || '').toLowerCase();
      if (heading && (docTitle.indexOf('mr. k') >= 0 || docTitle.indexOf('mr k') >= 0 || docTitle.indexOf('classroom') >= 0)) doc.title = text(heading.textContent);
    }
    cleanLinks();
    if (typeof G.MutationObserver === 'function') {
      new G.MutationObserver(cleanLinks).observe(doc.documentElement, { childList: true, subtree: true });
    }
  }
  applyStudentFocus();
  function choose(skills, start, note) {
    var params = new URLSearchParams(G.location.search);
    if (params.get('student') === '1') {
      var requested;
      try { requested = params.has('skills') ? JSON.parse(params.get('skills')) : skills.map(function (s) { return s.id; }); }
      catch (e) { requested = []; }
      var selected = Array.isArray(requested) ? skills.filter(function (s) { return requested.indexOf(s.id) >= 0; }).map(function (s) { return s.id; }) : [];
      if (!selected.length) {
        var error = G.document.createElement('p'); error.setAttribute('role', 'alert');
        error.textContent = 'These assigned skills are unavailable. Ask your teacher for a new student link.';
        G.document.body.replaceChildren(error); return;
      }
      var grade = G.MK_KID_GRADE;
      if (G.MKKid && grade >= 1 && grade <= 5) {
        var host = G.document.getElementById('app') || G.document.body;
        G.MKKid.playScreen(host, {title: text(G.document.title).split(' · ')[0], subtitle: 'You can do it!', grade: grade, onPlay: function () { G.MK_KID_STARTED = true; start(selected); }});
      } else start(selected);
      return;
    }
    var sharing = params.get('teacherShare') === '1';
    if (sharing && G.parent !== G) G.parent.postMessage({ type: 'teacher-skills-ready', skills: skills }, G.location.origin);
    var doc = G.document, dialog = doc.createElement('dialog');
    dialog.className = 'teacher-skills';
    var loading = typeof doc.querySelectorAll !== 'function' ? [] : [].filter.call(doc.querySelectorAll('body *'), function (el) { return !el.children.length && /^\s*Loading(\s+mathematics game)?(…|\.\.\.)\s*$/.test(el.textContent); });
    loading.forEach(function (el) { el.setAttribute('data-picker-hidden', el.style.visibility); el.style.visibility = 'hidden'; });
    var restoreLoading = function () { loading.forEach(function (el) { el.style.visibility = el.getAttribute('data-picker-hidden') || ''; el.removeAttribute('data-picker-hidden'); }); };
    dialog.style.cssText = 'box-sizing:border-box;width:min(640px,94vw);max-height:88vh;overflow:auto;border:2px solid #3456d1;border-radius:16px;padding:24px;background:#fff;color:#17233b;font:16px/1.5 system-ui;';
    var title = doc.createElement('h2'); title.textContent = 'Choose skills for this game';
    title.style.marginTop = '0'; dialog.appendChild(title);
    var context = doc.createElement('p'); context.textContent = text(doc.title).split(' | ')[0];
    context.style.fontWeight = '600'; dialog.appendChild(context);
    var help = doc.createElement('p'); help.textContent = note || 'All available skills are selected. Choose the skills you want students to practice.';
    dialog.appendChild(help);
    var actions = doc.createElement('div'); dialog.appendChild(actions);
    var list = doc.createElement('fieldset');
    var legend = doc.createElement('legend'); legend.textContent = 'Skills'; list.appendChild(legend);
    var inputs = skills.map(function (skill) {
      var label = doc.createElement('label'), input = doc.createElement('input');
      label.style.cssText = 'display:flex;align-items:baseline;gap:10px;margin:10px 0;text-align:left;';
      input.type = 'checkbox'; input.checked = true; input.value = skill.id;
      input.style.cssText = 'width:18px;height:18px;flex:none;';
      label.appendChild(input); label.appendChild(doc.createTextNode(text(skill.name))); list.appendChild(label);
      return input;
    });
    dialog.appendChild(list);
    /* Level travels with the student link (games that use the shared levels read ?level=). */
    var levelPick = null;
    if (G.MKGAMES && G.MKGAMES.LEVELS && G.MKGAMES.LEVELS.cp1) {
      var lvWrap = doc.createElement('label'); lvWrap.style.cssText = 'display:block;margin:12px 0 4px;font-weight:600;';
      lvWrap.appendChild(doc.createTextNode('Level for the student link '));
      levelPick = doc.createElement('select'); levelPick.style.cssText = 'margin-left:8px;padding:6px;font:inherit;';
      var want = params.get('level');
      [['cp2', 'Support'], ['cp1', 'Standard'], ['honors', 'Advanced']].forEach(function (o) { var opt = doc.createElement('option'); opt.value = o[0]; opt.textContent = o[1]; if (o[0] === (want || 'cp1')) opt.selected = true; levelPick.appendChild(opt); });
      lvWrap.appendChild(levelPick); dialog.appendChild(lvWrap);
    }
    var status = doc.createElement('p'); status.setAttribute('role', 'status'); dialog.appendChild(status);
    function button(label, parent, fn) {
      var b = doc.createElement('button'); b.type = 'button'; b.textContent = label;
      b.style.cssText = 'padding:9px 16px;margin:4px;border:1px solid #3456d1;border-radius:8px;background:#f2f5ff;color:#17233b;font:inherit;cursor:pointer;';
      b.onclick = fn; parent.appendChild(b); return b;
    }
    var go = button(sharing ? 'Generate student link' : 'Continue', dialog, function () {
      var ids = inputs.filter(function (i) { return i.checked; }).map(function (i) { return i.value; });
      if (!ids.length && skills.length) return;
      dialog.close(); dialog.remove(); restoreLoading();
      if (sharing && G.parent !== G) G.parent.postMessage({ type: 'teacher-skills-selected', skills: ids, level: levelPick ? levelPick.value : undefined }, G.location.origin);
      else start(ids);
    });
    function studentUrl(ids) {
      var url = new URL(G.location.href); url.hash = '';
      ['teacher', 'teacherShare'].forEach(function (k) { url.searchParams.delete(k); });
      url.searchParams.set('student', '1'); if (G.MK_GAME_CAPABILITIES && G.MK_GAME_CAPABILITIES.studentUrl) G.MK_GAME_CAPABILITIES.studentUrl(url);
      url.searchParams.set('skills', JSON.stringify(ids)); if (levelPick) url.searchParams.set('level', levelPick.value);
      return url.href;
    }
    if (!sharing && params.get('student') !== '1') {
      var shareRow = doc.createElement('div'); dialog.appendChild(shareRow);
      var linkField = null;
      button('Copy student link', shareRow, function () {
        var ids = inputs.filter(function (i) { return i.checked; }).map(function (i) { return i.value; }); if (!ids.length) return;
        var href = studentUrl(ids);
        if (!linkField) { linkField = doc.createElement('input'); linkField.readOnly = true; linkField.setAttribute('aria-label', 'Student link'); linkField.style.cssText = 'display:block;box-sizing:border-box;width:100%;padding:10px;margin-top:8px'; shareRow.appendChild(linkField); }
        linkField.value = href; linkField.focus(); linkField.select();
        if (G.navigator.clipboard && G.navigator.clipboard.writeText) G.navigator.clipboard.writeText(href).then(function () { status.textContent = 'Student link copied. It opens straight into the game with these skills and this level.'; }, function () { status.textContent = 'Copy the selected student link.'; });
        else status.textContent = 'Copy the selected student link.';
      });
      button('Preview as student', shareRow, function () {
        var ids = inputs.filter(function (i) { return i.checked; }).map(function (i) { return i.value; }); if (!ids.length) return;
        G.open(studentUrl(ids), '_blank', 'noopener');
      });
    }
    function update() {
      var n = inputs.filter(function (i) { return i.checked; }).length;
      var canContinue = !skills.length || n > 0; go.disabled = !canContinue; go.style.opacity = canContinue ? '1' : '.5';
      status.textContent = !skills.length ? 'No game questions are available for this unit yet.' : n ? n + ' of ' + skills.length + ' selected' : 'Select at least one skill to continue.';
    }
    button('Select All', actions, function () { inputs.forEach(function (i) { i.checked = true; }); update(); });
    button('Clear All', actions, function () { inputs.forEach(function (i) { i.checked = false; }); update(); });
    inputs.forEach(function (i) { i.onchange = update; });
    dialog.addEventListener('cancel', function (e) {
      e.preventDefault();
      if (sharing && G.parent !== G) G.parent.postMessage({ type: 'teacher-skills-cancel' }, G.location.origin);
    });
    doc.body.appendChild(dialog); update(); dialog.showModal();
  }
  function bank(items, label, start, note) {
    var names = items.map(function (q) { return text(label(q)); });
    var unique = Array.from(new Set(names));
    choose(unique.map(function (name, i) { return { id: String(i), name: name }; }), function (ids) {
      var selected = new Set(ids.map(function (id) { return unique[+id]; }));
      start(items.filter(function (_, i) { return selected.has(names[i]); }));
    }, note);
  }
  function questionLabel(q) {
    // Older mystery banks store a clue number where newer banks store a skill.
    // Use the actual instruction in that case, never an invented topic tag.
    return q.skill && !/^clue\s*\d+$/i.test(text(q.skill)) ? q.skill : q.instr;
  }
  function activityBank(items, label, start) {
    var params = new URLSearchParams(G.location.search);
    if (params.get('teacherShare') === '1' || params.get('student') === '1') bank(items, label, start);
    else start(items.slice());
  }
  G.TeacherSkills = { choose: choose, bank: bank, questionLabel: questionLabel, activityBank: activityBank };
})(window);
