(function () {
  'use strict';
  var title = document.getElementById('activity-title');
  var message = document.getElementById('activity-message');
  var original = document.getElementById('original-link');
  var content = document.getElementById('activity-content');
  var path = new URLSearchParams(window.location.search).get('path');
  // Keep previously shared viewer links working after the worksheet move.
  if (path === 'Mr_Ks_Algebra_Inequalities_Cheat_Sheet.pdf') {
    window.location.replace('activity.html?path=' + encodeURIComponent('artifacts/inequalities-cheat-sheet/worksheet.pdf'));
    return;
  }
  var match = null;
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
  title.textContent = match.title;
  document.title = match.title + ' | Mr. K’s Classroom';
  original.href = match.path;
  original.textContent = /\.pdf$/i.test(match.path) ? 'Open / print PDF ↗' : 'Open full page ↗';
  original.setAttribute('aria-label', original.textContent + ' (opens in a new tab)');
  original.hidden = false;
  var frame = document.createElement('iframe');
  frame.className = 'activity-frame';
  frame.title = match.title;
  frame.src = match.path;
  frame.allow = 'fullscreen; autoplay';
  frame.setAttribute('allowfullscreen', '');
  message.hidden = true;
  content.appendChild(frame);
})();
