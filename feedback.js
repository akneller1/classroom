/* Offer webmail or the visitor's configured mail app for website feedback.
 * Never send messages automatically. Keep existing mailto: links as a no-JS fallback. */
(function () {
  'use strict';

  var dialog = document.getElementById('feedbackChooser');
  if (!dialog || typeof dialog.showModal !== 'function') return;

  var gmail = document.getElementById('feedbackGmail');
  var outlook = document.getElementById('feedbackOutlook');
  var nativeMail = document.getElementById('feedbackDefault');
  var close = document.getElementById('feedbackChooserClose');
  if (!gmail || !outlook || !nativeMail || !close) return;

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
    gmail.href = links.gmail;
    outlook.href = links.outlook;
    nativeMail.href = links.native;
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
 * introduction line. Nothing is added to the header, so the layout stays exactly as it was. */
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
  var main = doc.getElementById('main');
  if (!main || typeof MutationObserver !== 'function') return;
  function hint() {
    // The home page's lede under "More learning. Less planning." (only the home page has .home-intro)
    var p = main.querySelector('.home-intro .lede');
    if (!p || p.querySelector('.guide-hint')) return;
    var a = doc.createElement('a');
    a.className = 'guide-hint'; a.href = 'guide.html';
    a.textContent = 'Read the teacher guide';
    p.appendChild(doc.createTextNode(' New here? '));
    p.appendChild(a);
    p.appendChild(doc.createTextNode('.'));
  }
  hint();
  new MutationObserver(hint).observe(main, { childList: true, subtree: true });
})();
