/* Teacher convenience: copy student-focused links from game and study-guide cards. */
(function () {
  'use strict';
  var eligible = Object.create(null);
  var library = window.LIBRARY;
  if (!library || !Array.isArray(library.courses)) return;

  function canShare(activity) {
    if (!activity || !activity.path || /^worksheet-generator\//i.test(activity.path)) return false;
    var types = Array.isArray(activity.type) ? activity.type : [activity.type || ''];
    var label = (activity.path + ' ' + (activity.title || '')).toLowerCase();
    return types.some(function (type) { return /^game$/i.test(type); }) ||
      /flashcard|cheat.sheet|study.guide|picture.reveal|connect.four|jeopardy|showdown|tic.tac.toe|escape.room|detective|mini.golf|zombie.fence/.test(label);
  }
  library.courses.forEach(function (course) {
    (course.units || []).forEach(function (unit) {
      (unit.artifacts || []).forEach(function (activity) {
        if (canShare(activity)) eligible[activity.path] = true;
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
      button.addEventListener('click', function () {
        var url = new URL('activity.html', window.location.href);
        url.hash = '';
        url.search = new URLSearchParams({ path: path, student: '1' }).toString();
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

  var main = document.getElementById('main');
  if (!main) return;
  enhanceCards();
  new MutationObserver(enhanceCards).observe(main, { childList: true, subtree: true });
})();
