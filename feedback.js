/* Offer webmail or the visitor's configured mail app for website feedback.
 * Never send messages automatically. Keep existing mailto: links as a no-JS fallback. */
(function () {
  'use strict';

  var dialog = document.getElementById('feedbackChooser');
  if (!dialog) {
    dialog = document.createElement('dialog'); dialog.id = 'feedbackChooser';
    dialog.className = 'feedback-chooser';
    dialog.setAttribute('aria-label', 'Report a problem');
    dialog.innerHTML = '<button id="feedbackChooserClose" type="button">Close</button><h2>Report a problem</h2><p>Your message opens as a draft for you to send.</p><p><a id="feedbackGmail" target="_blank" rel="noopener">Gmail</a> · <a id="feedbackOutlook" target="_blank" rel="noopener">Outlook</a> · <a id="feedbackDefault">Email application</a></p>';
    document.body.appendChild(dialog);
  }
  if (typeof dialog.showModal !== 'function') return;
  var gmail = document.getElementById('feedbackGmail');
  var outlook = document.getElementById('feedbackOutlook');
  var nativeMail = document.getElementById('feedbackDefault');
  var close = document.getElementById('feedbackChooserClose');
  var fields = document.createElement('div');
  fields.innerHTML = '<p><label>Page or activity<input id="feedbackPage" readonly style="display:block;width:100%;box-sizing:border-box"></label></p><p><label>What went wrong?<select id="feedbackKind" style="display:block"><option>Broken link</option><option>Wrong answer</option><option>Unclear directions</option><option>Printing problem</option><option>Other</option></select></label></p><p><label>Details<textarea id="feedbackDetails" rows="5" style="display:block;width:100%;box-sizing:border-box"></textarea></label></p>';
  dialog.insertBefore(fields, dialog.querySelector('.feedback-chooser-options') || gmail.parentNode);
  var page = document.getElementById('feedbackPage'), kind = document.getElementById('feedbackKind'), details = document.getElementById('feedbackDetails');
  var activeMail = '', activeBody = '';
  function refresh() {
    var parsed = new URL(activeMail, document.baseURI);
    parsed.searchParams.set('body', activeBody + '\n\nWhat went wrong: ' + kind.value + '\nDetails: ' + details.value);
    var links = composeLinks(parsed.href);
    gmail.href = links.gmail; outlook.href = links.outlook; nativeMail.href = links.native;
  }
  kind.addEventListener('change', refresh); details.addEventListener('input', refresh);

  function composeLinks(mailto) {
    var parsed = new URL(mailto, document.baseURI);
    if (parsed.protocol !== 'mailto:') return null;
    var recipient = decodeURIComponent(parsed.pathname);
    if (recipient.toLowerCase() !== 'akneller@gmail.com') return null;
    var subject = parsed.searchParams.get('subject') || "Mr. K's Classroom — Feedback";
    var body = parsed.searchParams.get('body') || '';

    var gmailUrl = new URL('https://mail.google.com/mail/u/0/');
    gmailUrl.searchParams.set('to', recipient);
    gmailUrl.searchParams.set('su', subject);
    gmailUrl.searchParams.set('body', body);
    gmailUrl.searchParams.set('tf', 'cm');

    var outlookUrl = new URL('https://outlook.live.com/mail/0/deeplink/compose');
    outlookUrl.searchParams.set('to', recipient);
    outlookUrl.searchParams.set('subject', subject);
    outlookUrl.searchParams.set('body', body);

    return { gmail: gmailUrl.href, outlook: outlookUrl.href, native: mailto };
  }

  // Event delegation covers footer feedback and dynamically rendered activity cards.
  document.addEventListener('click', function (event) {
    if (!event.target || typeof event.target.closest !== 'function') return;
    var source = event.target.closest('a[data-feedback-chooser], a.report-problem');
    if (!source) return;
    var mailto = source.getAttribute('href');
    if (!mailto || mailto.slice(0, 7).toLowerCase() !== 'mailto:') return;
    var links;
    try { links = composeLinks(mailto); } catch (_) { return; }
    if (!links) return;
    activeMail = mailto; activeBody = new URL(mailto, document.baseURI).searchParams.get('body') || '';
    /* A generic link (footer, home page) carries only a template: name the page the visitor is on (site audit 2, 2026-11-20). */
    if (!/https?:\/\//.test(activeBody)) activeBody = 'Page: ' + document.title + '\nLink: ' + location.href;
    page.value = activeBody.replace(/\n+/g, ' · '); details.value = ''; kind.value = 'Other';
    /* A page-level link (one per page, 2026-11-20) asks which activity the problem is with. */
    var pick = document.getElementById('feedbackActivity');
    if (pick) pick.parentNode.parentNode.removeChild(pick.parentNode);
    if (source.hasAttribute('data-report-choices')) {
      var cards = Array.prototype.slice.call(document.querySelectorAll('.card[data-report]'));
      if (cards.length) {
        var wrap = document.createElement('p'), label = document.createElement('label');
        label.textContent = 'Which activity?';
        var sel = document.createElement('select'); sel.id = 'feedbackActivity'; sel.style.cssText = 'display:block;width:100%;box-sizing:border-box';
        var o0 = document.createElement('option'); o0.value = ''; o0.textContent = 'This page in general'; sel.appendChild(o0);
        cards.forEach(function (c, i) { var o = document.createElement('option'); o.value = String(i); o.textContent = c.getAttribute('data-report-title'); sel.appendChild(o); });
        sel.addEventListener('change', function () {
          var m = sel.value === '' ? mailto : cards[+sel.value].getAttribute('data-report');
          activeMail = m; activeBody = new URL(m, document.baseURI).searchParams.get('body') || ''; page.value = activeBody; refresh();
        });
        label.appendChild(sel); wrap.appendChild(label); fields.insertBefore(wrap, fields.firstChild);
      }
    }
    refresh();
    event.preventDefault();
    dialog.showModal();
  });

  close.addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (event) {
    if (event.target === dialog) dialog.close();
  });
  [gmail, outlook, nativeMail].forEach(function (link) {
    link.addEventListener('click', function () { dialog.close(); });
  });
})();

/* Teacher Guide (guide.html): a footer link on every page, and a short "New here?" pointer added to the home page's
 * introduction, on its own line. */
(function () {
  'use strict';
  var doc = document;
  var bottom = doc.querySelector('.site-footer .footer-bottom');
  if (bottom && !bottom.querySelector('a[href="guide.html"]')) {
    var f = doc.createElement('a');
    f.href = 'guide.html'; f.textContent = 'Teacher guide';
    var fb = bottom.querySelector('[data-feedback-chooser]');
    if (fb) bottom.insertBefore(f, fb); else bottom.appendChild(f);
  }
  // Privacy page (privacy.html): anonymous, cookie-free visit counts; no student data.
  if (bottom && !bottom.querySelector('a[href="privacy.html"]')) {
    var pv = doc.createElement('a');
    pv.href = 'privacy.html'; pv.textContent = 'Privacy';
    var fb2 = bottom.querySelector('[data-feedback-chooser]');
    if (fb2) bottom.insertBefore(pv, fb2); else bottom.appendChild(pv);
  }
  var main = doc.getElementById('main');
  if (!main || typeof MutationObserver !== 'function') return;
  function hint() {
    // The home page's lede under "More learning. Less planning." (only the home page has .home-intro)
    var p = main.querySelector('.home-intro .lede');
    if (!p || p.querySelector('.guide-hint')) return;
    var a = doc.createElement('a');
    a.className = 'guide-hint'; a.href = 'guide.html';
    a.textContent = 'Read the teacher guide';
    p.appendChild(doc.createElement('br'));
    p.appendChild(doc.createTextNode('New here? '));
    p.appendChild(a);
    p.appendChild(doc.createTextNode('.'));
  }
  hint();
  new MutationObserver(hint).observe(main, { childList: true, subtree: true });
})();

/* Direct resource and student pages use the same report route as unit cards. */
(function(){
 if(document.querySelector('a[data-feedback-chooser],a.report-problem,#report-problem'))return;
 var footer=document.createElement('p'),link=document.createElement('a');
 footer.className='mk-feedback-footer';footer.style.cssText='text-align:center;margin:16px;font:14px system-ui';
 link.href='mailto:akneller@gmail.com?subject=Mr.%20K%27s%20Classroom%20%E2%80%94%20Resource%20problem';
 link.className='report-problem';link.textContent='Report a problem';link.style.color='inherit';footer.appendChild(link);document.body.appendChild(footer);
 var style=document.createElement('style');style.textContent='#feedbackChooser{box-sizing:border-box;width:min(560px,94vw);max-height:90vh;overflow:auto}@media print{.mk-feedback-footer,#feedbackChooser{display:none!important}}';document.head.appendChild(style);
})();
