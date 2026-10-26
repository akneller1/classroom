(function () {
  'use strict';
  var title = document.getElementById('activity-title');
  var message = document.getElementById('activity-message');
  var original = document.getElementById('original-link');
  var content = document.getElementById('activity-content');
  var params = new URLSearchParams(window.location.search);
  var path = params.get('path');
  // Presentation-only focus mode. This is NOT authentication or a security boundary.
  var studentFocus = params.get('student') === '1';
  if (studentFocus) document.body.classList.add('student-focus');
  // Keep previously shared viewer links working after the worksheet move.
  if (path === 'Mr_Ks_Algebra_Inequalities_Cheat_Sheet.pdf') {
    window.location.replace('activity.html?path=' + encodeURIComponent('artifacts/inequalities-cheat-sheet/worksheet.pdf'));
    return;
  }
  var match = null;
  function shareableActivity(activity) {
    if (!activity || /^worksheet-generator\//i.test(activity.path || '')) return false;
    var name = ((activity.path || '') + ' ' + (activity.title || '')).toLowerCase();
    var types = Array.isArray(activity.type) ? activity.type : [activity.type || ''];
    return types.some(function (type) { return /^game$/i.test(type); }) ||
      /flashcard|cheat.sheet|study.guide|picture.reveal|connect.four|jeopardy|showdown|tic.tac.toe|escape.room|detective|mini.golf|zombie.fence/.test(name);
  }
  var library = window.LIBRARY;
  if (library && Array.isArray(library.courses)) {
    library.courses.forEach(function (course) {
      course.units.forEach(function (unit) {
        unit.artifacts.forEach(function (activity) {
          if (activity.path === path) match = activity;
        });
      });
    });
  }
  // Only embed a known local activity, never an arbitrary URL from a query string.
  if (!match || !/^(?:artifacts|worksheet-generator)\/[a-z0-9_\-/]+\.(?:html|pdf)$/i.test(match.path) || match.path.indexOf('..') >= 0) {
    title.textContent = 'Activity not found';
    message.textContent = 'This activity could not be found. Choose Home to browse the available activities.';
    return;
  }
  if (studentFocus && !shareableActivity(match)) {
    title.textContent = 'Student link unavailable';
    message.textContent = 'This link is not a student game or study guide.';
    return;
  }
  title.textContent = match.title;
  document.title = match.title + ' | Mr. K’s Classroom';
  original.href = match.path;
  original.textContent = /\.pdf$/i.test(match.path) ? 'Open / print PDF ↗' : 'Open full page ↗';
  original.setAttribute('aria-label', original.textContent + ' (opens in a new tab)');
  original.hidden = studentFocus;
  if (!studentFocus && shareableActivity(match)) {
    var share = document.getElementById('share-student');
    share.hidden = false;
    share.addEventListener('click', function () {
      var url = new URL('activity.html', window.location.href);
      url.search = new URLSearchParams({path: match.path, student: '1'}).toString();
      var value = url.href;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(value).then(function () { share.textContent = 'Student link copied!'; }, function () { window.prompt('Copy student link:', value); });
      } else { window.prompt('Copy student link:', value); }
    });
  }
  var details = (window.RESOURCE_DETAILS || {})[match.path];
  var info = document.getElementById('resource-details');
  if (details) {
    var labels = [details.pages + (details.pages === 1 ? ' page' : ' pages')];
    if (details.embeddedKey) labels.push('Answer key included in this PDF');
    if (details.studentOnly) labels.push('Student worksheets only');
    if (details.referenceSheet) labels.push('Reference sheet');
    info.textContent = labels.join(' · ');
    if (details.answerKey && !studentFocus) {
      var key = document.createElement('a');
      key.href = '#teacher-key';
      key.setAttribute('aria-haspopup', 'dialog');
      key.textContent = '🔒 Open teacher key (' + details.keyPages + (details.keyPages === 1 ? ' page' : ' pages') + ')';
      var dialog = document.getElementById('teacher-key-dialog');
      var code = document.getElementById('teacher-key-code');
      var error = document.getElementById('teacher-key-error');
      key.addEventListener('click', function (event) {
        event.preventDefault();
        code.value = ''; error.textContent = '';
        dialog.showModal(); code.focus();
      });
      document.getElementById('teacher-key-cancel').addEventListener('click', function () { dialog.close(); });
      document.getElementById('teacher-key-form').addEventListener('submit', function (event) {
        event.preventDefault();
        if (code.value.trim() !== '205') {
          error.textContent = 'Incorrect code. Please try again.';
          code.select(); return;
        }
        window.open(details.answerKey, '_blank', 'noopener');
        dialog.close(); code.value = '';
      });
      dialog.addEventListener('close', function () { code.value = ''; key.focus(); });
      info.appendChild(key);
    }
  }
  var report = document.getElementById('report-problem');
  report.href = 'https://github.com/akneller1/classroom/issues/new?title=' + encodeURIComponent('Resource problem: ' + match.title) +
    '&body=' + encodeURIComponent('Activity: ' + match.title + '\nLink: https://akneller1.github.io/classroom/activity.html?path=' + encodeURIComponent(match.path) + '\n\nProblem (broken link, incorrect answer, unclear directions, or other):\n\nProblem number / steps to reproduce:\n\nExpected result:\n');
  report.hidden = studentFocus;
  var frame = document.createElement('iframe');
  frame.className = 'activity-frame';
  frame.title = match.title;
  frame.src = match.path;
  frame.allow = 'fullscreen; autoplay';
  frame.setAttribute('allowfullscreen', '');
  message.hidden = true;
  content.appendChild(frame);
})();
