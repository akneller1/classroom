/* Shared report dialog. Email drafts are opened only after the visitor submits. */
(function(){
 'use strict';
 if(window.MK_FEEDBACK_READY)return;window.MK_FEEDBACK_READY=true;
 function normalize(value){var u=new URL(value,location.href);u.pathname=u.pathname.replace(/\/{2,}/g,'/');return u.href;}
 function openReport(title,url){
  if(!dialog)makeDialog();
  dialog.querySelector('[name=title]').value=title||document.title;
  dialog.querySelector('[name=url]').value=normalize(url||location.href);
  dialog.querySelector('[name=details]').value='';
  dialog.querySelector('[name=problem]').value='broken link';
  dialog.dispatchEvent(new Event('input'));
  dialog.showModal();
 }
 var dialog;
 function makeDialog(){
  dialog=document.createElement('dialog');dialog.id='mk-feedback';dialog.setAttribute('aria-labelledby','mk-feedback-title');
  dialog.innerHTML='<form><h2 id="mk-feedback-title">Report a problem</h2><label>Page or activity<input name="title" readonly></label><label>Link<input name="url" readonly></label><label>What went wrong?<select name="problem"><option value="broken link">Broken link</option><option value="wrong answer">Wrong answer</option><option value="unclear directions">Unclear directions</option><option value="printing problem">Printing problem</option><option value="other">Other</option></select></label><label>Details<textarea name="details" rows="4" placeholder="Problem number, what happened, and what you expected"></textarea></label><label>Open email draft in<select name="provider"><option value="native">Email application</option><option value="gmail">Gmail</option><option value="outlook">Outlook</option></select></label><p>Your report opens as a draft. Review it and send it in your email app.</p><div class="mk-feedback-actions"><button type="button" data-close>Cancel</button><button type="submit">Open email draft</button></div><a data-fallback href="mailto:akneller@gmail.com">Email fallback</a></form>';
  var style=document.createElement('style');style.textContent='#mk-feedback{width:min(520px,90vw);max-height:90vh;overflow:auto;border:1px solid #9ba7b7;border-radius:14px;padding:24px;color:#18212f;background:#fff;font:16px/1.4 system-ui}#mk-feedback::backdrop{background:#0008}#mk-feedback label{display:block;margin:12px 0}#mk-feedback input,#mk-feedback select,#mk-feedback textarea{box-sizing:border-box;display:block;width:100%;font:inherit;margin-top:4px;padding:8px;color:#18212f;background:white;border:1px solid #9ba7b7;border-radius:5px}#mk-feedback h2{margin:0 0 12px}#mk-feedback p{font-size:14px}#mk-feedback button{font:inherit;padding:9px 14px;cursor:pointer;border-radius:6px;border:1px solid #9ba7b7}.mk-feedback-actions{display:flex;justify-content:flex-end;gap:10px;margin:12px 0}#mk-feedback button[type=submit]{background:#2459a6;color:white}';
  document.head.appendChild(style);document.body.appendChild(dialog);
  dialog.querySelector('[data-close]').onclick=function(){dialog.close();};
  function draft(){
   var f=dialog.querySelector('form').elements;
   var subject="Mr. K's Classroom — "+f.problem.value+': '+f.title.value;
   var body='Activity: '+f.title.value+'\nLink: '+f.url.value+'\nProblem: '+f.problem.value+'\n\n'+f.details.value;
   var email='mailto:akneller@gmail.com?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body);
   dialog.querySelector('[data-fallback]').href=email;
   return {subject:subject,body:body,email:email,provider:f.provider.value};
  }
  dialog.addEventListener('input',draft);
  dialog.querySelector('form').onsubmit=function(event){
   event.preventDefault();var d=draft(),target;
   if(d.provider==='gmail'){target=new URL('https://mail.google.com/mail/u/0/');target.search=new URLSearchParams({to:'akneller@gmail.com',su:d.subject,body:d.body,tf:'cm'});}
   else if(d.provider==='outlook'){target=new URL('https://outlook.live.com/mail/0/deeplink/compose');target.search=new URLSearchParams({to:'akneller@gmail.com',subject:d.subject,body:d.body});}
   if(target)window.open(target.href,'_blank','noopener,noreferrer');else location.href=d.email;
  };
 }
 document.addEventListener('click',function(event){
  var a=event.target.closest&&event.target.closest('a');if(!a)return;
  var href=a.getAttribute('href')||'';
  if(!(a.matches('[data-feedback-chooser],.report-problem,#report-problem')||/^mailto:akneller@gmail\.com/i.test(href)||/github\.com\/akneller1\/classroom\/issues\/new/.test(href)))return;
  event.preventDefault();var title=a.dataset.reportTitle,url=a.dataset.reportUrl;
  if(!url&&href.startsWith('mailto:')){var body=new URL(href).searchParams.get('body')||'',match=/Link: (https?:\/\/[^\n]+)/.exec(body),t=/Activity: ([^\n]+)/.exec(body);if(match)url=match[1];if(t)title=t[1];}
  openReport(title,url);
 });
 if(!document.querySelector('a[data-feedback-chooser],a.report-problem,#report-problem')){
  var footer=document.createElement('p'),link=document.createElement('a');
  footer.className='mk-feedback-footer';footer.style.cssText='text-align:center;margin:16px;font:14px system-ui';
  link.href='mailto:akneller@gmail.com';link.className='report-problem';link.textContent='Report a problem';footer.appendChild(link);document.body.appendChild(footer);
  var printStyle=document.createElement('style');printStyle.textContent='@media print{.mk-feedback-footer,#mk-feedback{display:none!important}}';document.head.appendChild(printStyle);
 }
 window.MK_FEEDBACK={open:openReport,normalize:normalize};
})();

/* Teacher guide hint on the homepage. */
(function(){var main=document.getElementById('main');if(!main)return;function hint(){var p=main.querySelector('.home-intro .lede');if(!p||p.querySelector('.guide-hint'))return;var a=document.createElement('a');a.href='guide.html';a.className='guide-hint';a.textContent='Read the teacher guide';p.appendChild(document.createElement('br'));p.appendChild(document.createTextNode('New here? '));p.appendChild(a);p.appendChild(document.createTextNode('.'));}hint();new MutationObserver(hint).observe(main,{childList:true,subtree:true});})();
