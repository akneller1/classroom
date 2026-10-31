/* Share the same skill catalogue and filtering used by each individual game. */
(function (G) {
  'use strict';
  function supports(path) { return /^worksheet-generator\/course-(game|activity)\.html\?/.test(path) || /^artifacts\/[a-z0-9-]+\/index\.html$/i.test(path) && !/escape-room/i.test(path); }
  function open(path) {
    var doc = G.document, previous = doc.activeElement;
    var old = doc.getElementById('game-share-dialog'); if (old) old.close();
    var dialog = doc.createElement('dialog'); dialog.id = 'game-share-dialog';
    dialog.setAttribute('aria-label', 'Choose skills and generate student link');
    dialog.style.cssText = 'width:min(920px,94vw);height:90vh;max-height:90vh;box-sizing:border-box;border:2px solid #3456d1;border-radius:14px;padding:16px;background:white;color:#17233b;';
    var close = doc.createElement('button'); close.type = 'button'; close.textContent = 'Close'; close.className = 'btn';
    close.onclick = function () { dialog.close(); }; dialog.appendChild(close);
    var frame = doc.createElement('iframe'); frame.title = 'Choose game skills';
    frame.style.cssText = 'display:block;width:100%;height:calc(100% - 48px);border:0;margin-top:12px;';
    var game = new URL(path, G.location.href); game.searchParams.set('teacherShare', '1'); frame.src = game.href;
    dialog.appendChild(frame);
    var catalogue = null;
    function receive(event) {
      if (event.origin !== G.location.origin || event.source !== frame.contentWindow || !event.data) return;
      if (event.data.type === 'teacher-skills-cancel') { dialog.close(); return; }
      if (event.data.type === 'teacher-skills-ready' && Array.isArray(event.data.skills)) {
        catalogue = event.data.skills.filter(function (s) { return s && typeof s.id === 'string' && typeof s.name === 'string'; });
      } else if (event.data.type === 'teacher-skills-selected' && catalogue) {
        var ids = event.data.skills;
        if (!Array.isArray(ids) || !ids.length || !ids.every(function (id) { return catalogue.some(function (s) { return s.id === id; }); })) return;
        G.removeEventListener('message', receive);
        var nativeCourse = /^worksheet-generator\/course-(game|activity)\.html\?/.test(path);
        var url = new URL(nativeCourse ? path : 'activity.html', G.location.href); url.hash = '';
        if(nativeCourse){url.searchParams.set('student','1');url.searchParams.set('skills',JSON.stringify(ids));}
        else url.search = new URLSearchParams({path:path,student:'1',skills:JSON.stringify(ids)}).toString();
        frame.remove();
        var heading = doc.createElement('h2'); heading.textContent = 'Student link ready'; dialog.appendChild(heading);
        var summary = doc.createElement('p'); summary.textContent = 'Selected skills: ' + catalogue.filter(function (s) { return ids.indexOf(s.id) >= 0; }).map(function (s) { return s.name; }).join('; '); dialog.appendChild(summary);
        var label = doc.createElement('label'); label.textContent = 'Student link';
        var input = doc.createElement('input'); input.id = 'game-student-link'; input.readOnly = true; input.value = url.href;
        input.style.cssText = 'display:block;box-sizing:border-box;width:100%;padding:12px;margin:12px 0;'; label.appendChild(input); dialog.appendChild(label);
        var copy = doc.createElement('button'); copy.type = 'button'; copy.textContent = 'Copy student link'; copy.className = 'btn';
        copy.onclick = function () {
          function fallback() { input.focus(); input.select(); }
          if (G.navigator.clipboard && G.navigator.clipboard.writeText) G.navigator.clipboard.writeText(input.value).then(function () { copy.textContent = 'Copied!'; }, fallback);
          else fallback();
        };
        dialog.appendChild(copy); input.focus(); input.select();
      }
    }
    G.addEventListener('message', receive);
    dialog.addEventListener('close', function () { G.removeEventListener('message', receive); dialog.remove(); if (previous && previous.isConnected) previous.focus(); });
    doc.body.appendChild(dialog); dialog.showModal();
  }
  G.TeacherGameShare = { supports: supports, open: open };
})(window);
