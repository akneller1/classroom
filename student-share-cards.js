/* Teacher convenience: copy student-focused links from game and study-guide cards. */
(function () {
  'use strict';
  var eligible = Object.create(null);
  var library = window.LIBRARY;
  if (!library || !Array.isArray(library.courses)) return;

  function integratedStudentDestination(activity, level) {
    var path = activity.path;
    var type = String(activity.type || '');
    if (activity.courseId === 'grade5' && type === 'Project') {
      var match = /^(https:\/\/akneller1\.github\.io\/FinancialAlgebra\/)math5-project-([a-z0-9-]+)\/index\.html$/.exec(path);
      if (!match) return null;
      path = match[1] + 'math5-project-' + match[2] + '/' + match[2] + '-' + level + '.pdf';
    }
    var url = new URL(path, window.location.href);
    if (/\.html$/i.test(url.pathname)) {
      url.searchParams.delete('teacher');
      url.searchParams.delete('teacherShare');
      url.searchParams.delete('mode');
      url.searchParams.delete('present');
      url.searchParams.set('student', '1');
      if (activity.courseId === 'grade5' && (type === 'Game' || type === 'Study Guide' && activity.title === 'Understanding Check')) {
        url.searchParams.set('level', level);
      }
    }
    return url.href;
  }
  function canShare(activity) {
    if (!activity || !activity.path) return false;
    var shareTypes = Array.isArray(activity.type) ? activity.type : [activity.type || ''];
    if (!shareTypes.some(function (type) { return /^(game|study guide)$/i.test(type); }) && !/flashcards|cheat.sheet|study.guide/i.test(activity.path+' '+(activity.title||''))) return false;
    if (activity.courseId === 'grade5') return ['Game','Study Guide','Interactive','Project'].indexOf(String(activity.type)) >= 0;
    if (activity.courseId === 'financial-algebra') return ['Game','Study Guide','Interactive','Project'].indexOf(String(activity.type)) >= 0;
    if (/^artifacts\/geometry-congruence-proofs\/index\.html$/.test(activity.path)) return true;
    if (/^worksheet-generator\/(?:course-(game|activity)|algebra2-game)\.html\?/i.test(activity.path)) return /[?&]game=(flashcards|picture-reveal|detective|escape-room)(?:&|$)/i.test(activity.path);
    if (/^worksheet-generator\//i.test(activity.path)) return false;
    if (/jeopardy|showdown|connect-four|inequality-four|tic-tac-toe/i.test(activity.path)) return false;
    var types = Array.isArray(activity.type) ? activity.type : [activity.type || ''];
    var label = (activity.path + ' ' + (activity.title || '')).toLowerCase();
    return types.some(function (type) { return /^(game|interactive)$/i.test(type); }) ||
      /flashcard|cheat.sheet|study.guide|picture.reveal|connect.four|jeopardy|showdown|tic.tac.toe|escape.room|detective|mini.golf|zombie.fence/.test(label);
  }
  library.courses.forEach(function (course) {
    (course.units || []).forEach(function (unit) {
      (unit.artifacts || []).forEach(function (activity) {
        if (canShare(Object.assign({courseId:course.id},activity))) eligible[activity.path] = Object.assign({courseId:course.id},activity);
      });
    });
  });

  function enhanceCards() {
    document.querySelectorAll('#main .card[data-path]').forEach(function (card) {
      var path = card.getAttribute('data-path');
      if (!eligible[path] || card.querySelector('.share-student')) return;
      var actions = card.querySelector('.actions');
      if (!actions) return;
      var button = document.createElement('button');
      button.type = 'button';
      button.className = 'btn btn-ghost share-student';
      button.textContent = 'Copy student link';
      button.setAttribute('aria-label', 'Copy student link for ' +
        (card.querySelector('h3') ? card.querySelector('h3').textContent.trim() : 'activity'));
      var resource = eligible[path];
      if (resource.courseId === 'grade5' && (resource.type === 'Project' || /[?&]game=fraction-frenzy(?:&|$)/.test(resource.path))) {
        var select = document.createElement('select');
        select.className = 'student-share-level';
        select.setAttribute('aria-label', 'Student difficulty for ' + resource.title);
        [['cp2','Remedial'],['cp1','Standard'],['honors','Advanced']].forEach(function (entry) {
          var option = document.createElement('option');
          option.value = entry[0]; option.textContent = entry[1];
          if (entry[0] === 'cp1') option.selected = true;
          select.appendChild(option);
        });
        actions.appendChild(select);
      }
      button.addEventListener('click', function () {
        if (window.MK_INTEGRATED_STUDENT_SHARE && window.MK_INTEGRATED_STUDENT_SHARE.supports(resource)) {
          window.MK_INTEGRATED_STUDENT_SHARE.open(resource);
          return;
        }
        if (resource.courseId === 'grade5' || resource.courseId === 'financial-algebra') {
          var levelControl = actions.querySelector('.student-share-level');
          var destination = integratedStudentDestination(resource, levelControl ? levelControl.value : 'cp1');
          if (!destination) { window.alert('This student resource is not available.'); return; }
          var copied = function () { button.textContent = 'Copied!'; window.setTimeout(function () { button.textContent = 'Copy student link'; }, 2000); };
          var manual = function () { window.prompt('Copy student link:', destination); };
          if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(destination).then(copied, manual);
          else manual();
          return;
        }
        if (window.TeacherGameShare && window.TeacherGameShare.supports(path)) { window.TeacherGameShare.open(path); return; }
        var url = new URL(path, window.location.href); url.hash = ''; if (/\.html(?:[?#]|$)/i.test(path)) url.searchParams.set('student', '1');
        function success() {
          button.textContent = 'Copied!';
          window.setTimeout(function () { button.textContent = 'Copy student link'; }, 2000);
        }
        function fallback() { window.prompt('Copy student link:', url.href); }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url.href).then(success, fallback);
        } else fallback();
      });
      actions.appendChild(button);
    });
  }


  /* Course unit cards: open assessment setup before copying a student URL. */
  var readinessUnits = {
    'foundations-algebra':'algebra1-foundations',
    'expressions-equations':'algebra1-expressions-equations',
    'inequalities':'algebra1-inequalities',
    'relations-functions':'algebra1-relations-functions',
    'linear-equations-slope':'algebra1-linear-equations-slope',
    'systems-of-equations':'algebra1-systems-of-equations',
    'exponents-exponential-functions':'algebra1-exponents-scientific-notation',
    'exponential-functions':'algebra1-exponential-functions',
    'polynomials-factoring':'algebra1-polynomials',
    'factoring-zero-product':'algebra1-factoring-zero-product',
    'quadratics':'algebra1-quadratics',
    'statistics-data-modeling':'algebra1-statistics-data-modeling'
  };
  function openAssessmentSetup(unitId) {
    var existing = document.getElementById('readiness-setup-modal');
    if (existing) existing.remove();
    var oldOverflow = document.body.style.overflow;
    var overlay = document.createElement('div');
    overlay.id = 'readiness-setup-modal';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Configure and copy self-assessment student link');
    overlay.style.cssText = 'position:fixed;inset:0;z-index:9999;background:rgba(10,22,38,.75);display:flex;align-items:center;justify-content:center;padding:12px;';
    var panel = document.createElement('div');
    panel.style.cssText = 'width:min(960px,100%);height:min(850px,94vh);background:#fff;border-radius:14px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 18px 70px rgba(0,0,0,.32);';
    var bar = document.createElement('div');
    bar.style.cssText = 'display:flex;align-items:center;gap:12px;justify-content:space-between;padding:10px 16px;background:#f3f6fc;border-bottom:1px solid #dbe2ef;';
    var heading = document.createElement('strong');
    heading.textContent = 'Set up self-assessment · then copy student link';
    var close = document.createElement('button');
    close.type = 'button';
    close.textContent = 'Close ✕';
    close.className = 'btn btn-ghost';
    var frame = document.createElement('iframe');
    var url = new URL('worksheet-generator/practice-test.html', window.location.href);
    url.hash = new URLSearchParams({unit:unitId,setup:'1'}).toString();
    frame.src = url.href;
    frame.title = 'Self-assessment setup';
    frame.setAttribute('allow', 'clipboard-write');
    frame.style.cssText = 'width:100%;flex:1;border:0;min-height:0;';
    var previousFocus = document.activeElement;
    function dismiss() {
      document.removeEventListener('keydown', onKey);
      overlay.remove();
      document.body.style.overflow = oldOverflow;
      if (previousFocus && previousFocus.isConnected) previousFocus.focus();
    }
    function onKey(e) { if (e.key === 'Escape') dismiss(); }
    close.addEventListener('click', dismiss);
    overlay.addEventListener('click', function(e) { if (e.target === overlay) dismiss(); });
    document.addEventListener('keydown', onKey);
    bar.appendChild(heading);
    bar.appendChild(close);
    panel.appendChild(bar);
    panel.appendChild(frame);
    overlay.appendChild(panel);
    document.body.appendChild(overlay);
    document.body.style.overflow = 'hidden';
    close.focus();
  }
  document.addEventListener('click', function (event) {
    var btn = event.target.closest && event.target.closest('.readiness-activity-share[data-readiness-unit]');
    if (btn) { event.preventDefault(); openAssessmentSetup(btn.getAttribute('data-readiness-unit')); }
  });

  var main = document.getElementById('main');
  if (!main) return;
  enhanceCards();
  new MutationObserver(enhanceCards).observe(main, { childList: true, subtree: true });
})();
