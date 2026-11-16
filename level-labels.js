/* Display labels never change saved level codes or student link parameters. */
(function(G){'use strict';const doc=G.document;if(!doc)return;/* One public level vocabulary site-wide; high-school teacher pages may prefix the CP code. */
const labels={cp2:'Support',cp1:'Standard',honors:'Advanced'};G.MK_LEVEL_LABELS=labels;
function apply(){doc.querySelectorAll('select').forEach(sel=>{if(!Array.from(sel.options).some(o=>o.value==='cp2'))return;const student=new URLSearchParams(location.search).get('student')==='1'||/game|practice|flashcard|understanding|asteroid|millionaire/.test(location.pathname);Array.from(sel.options).forEach(o=>{if(labels[o.value]){const text=labels[o.value];if(o.textContent===text)return;if(student||/^(On Level|Challenge|Level [123]\b.*)$/.test(o.textContent.trim()))o.textContent=text}})});doc.querySelectorAll('[data-level]').forEach(e=>{if(e.tagName==='BUTTON'&&labels[e.dataset.level]&&e.textContent!==labels[e.dataset.level])e.textContent=labels[e.dataset.level]})}
apply();let scheduled=false;new MutationObserver(()=>{if(!scheduled){scheduled=true;queueMicrotask(()=>{scheduled=false;apply()})}}).observe(doc.body,{childList:true,subtree:true});
})(window);
