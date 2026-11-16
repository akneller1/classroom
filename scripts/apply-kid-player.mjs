// Apply the reviewed player UI after assembling pinned elementary sources.
import fs from 'node:fs';
import path from 'node:path';
const out=path.resolve(process.argv[2]||'_site');
const source='worksheet-generator/core/elementary/kid-ui';
function edit(file,fn){if(!fs.existsSync(file))throw Error('Missing player '+file);const text=fs.readFileSync(file,'utf8');if(text.includes('/* kid-player-v1 */'))return;fs.writeFileSync(file,'/* kid-player-v1 */\n'+fn(text));}
function replace(s,from,to){if(!s.includes(from))throw Error('Player hook changed: '+from);return s.replace(from,to);}
let wording=0;
const pending=[];
for(const course of fs.readdirSync('content-updates/kid-friendly/wording'))for(const f of fs.readdirSync('content-updates/kid-friendly/wording/'+course)){
 const grade=course.replace('math','grade'),unit=f.replace('.wording.json','');
 const {edits}=JSON.parse(fs.readFileSync('content-updates/kid-friendly/wording/'+course+'/'+f));
 for(const bankFile of [path.join(out,'question-banks',grade,unit+'.json'),path.join(out,grade,'question-banks',course,unit+'.json')]){
  const bank=JSON.parse(fs.readFileSync(bankFile));
  for(const e of edits){const q=bank.questions.find(q=>q.id===e.id);if(!q)throw Error('Missing wording question '+e.id);for(const [field,c] of Object.entries(e.changes)){if('append' in c){if(!String(q[field]||'').includes(c.append))q[field]=(q[field]||'')+c.append;}else{const same=(x,y)=>JSON.stringify(x)===JSON.stringify(y);if(!same(q[field],c.from)&&!same(q[field],c.to))throw Error('Wording conflict '+e.id+'/'+field);q[field]=c.to;}}}
  pending.push([bankFile,bank]);
 }wording+=edits.length;
}
if(wording!==169)throw Error('Unexpected wording count '+wording);
for(const [file,bank] of pending)fs.writeFileSync(file,JSON.stringify(bank));
for(let grade=1;grade<=5;grade++){
 const wg=path.join(out,'grade'+grade,'worksheet-generator'),runtime=path.join(wg,grade===5?'grade5':'elementary');
 fs.cpSync(source,path.join(runtime,'kid-ui'),{recursive:true});
 const prefix=grade===5?'g5':'el',K=grade===5?'g5':'K';
 const readQuestion=`G.MKReadAloud.button(box, function () { return p.prompt + (p.options || []).map(function (o, i) { return '. ' + 'ABCDEF'[i] + ': ' + o.text; }).join('') + (p.parts || []).map(function (pt, i) { return '. Part ' + (i + 1) + ': ' + pt.prompt; }).join(''); }, {grade: ${grade}});`;
 edit(path.join(runtime,grade===5?'g5-core.js':'el-core.js'),s=>{
  s=replace(s,`math(el('div', box, '${prefix}-prompt'), p.prompt);`,`math(el('div', box, '${prefix}-prompt'), p.prompt);\n    ${readQuestion}`);
  s=replace(s,"fb.textContent = ok ? pick(PRAISE) : (last ? 'Good effort! Here is how to solve it.' : pick(NUDGE));",`fb.textContent = ok ? G.MKKid.praise(${grade}) : (last ? G.MKKid.lastTry(${grade}) : G.MKKid.nudge(${grade}));`);
  s=s.replace(new RegExp("el\\('p', area, '"+prefix+"-hint-text', (?:CFG.answerHint \\|\\| )?'Fractions:[^\\n]+"),`el('p', area, '${prefix}-hint-text kid-hint', G.MKKid.hint(p.answer, ${grade}));`);
  s=replace(s,'if (done) return; done = true;',"if (done) return; done = true; box.querySelectorAll('.kid-key').forEach(function(b){b.disabled=true;});");
  if(grade<=2)s=replace(s,'go.onclick = submit;',`G.MKKid.numberPad(area, input, {answer:p.answer, grade:${grade}, onCheck:submit});\n      go.onclick = submit;`);
  s=replace(s, "if (P.get('student') === '1' && P.get('level')) { setTimeout(function () { go.click(); }, 0); }", `if (P.get('student') === '1' && P.get('level')) {
      if (!G.MK_KID_STARTED) { p.hidden=true; G.MKKid.playScreen(host,{title:cfg.heading,subtitle:'You can do it!',grade:${grade},onPlay:function(){G.MK_KID_STARTED=true;go.click();}}); }
      else setTimeout(function(){go.click();},0);
    }`);
  return s;
 });
 edit(path.join(runtime,grade===5?'g5-games.js':'el-games.js'),s=>{
  s=replace(s,"    el('div', box, 'big', emoji || '🎉');\n    el('h2', box, null, headline);",'');
  s=replace(s,"    el('p', box, null, right + ' correct answers out of ' + tot + ' questions. Every question you worked on made your brain stronger!');",`    G.MKKid.finish(box, {right:right, total:tot, grade:${grade}, unit:'grade${grade}:'+P.get('unit'), onAgain:function(){G.location.reload();}});`);
  return s.replace(new RegExp("    var again = el\\('button', box, '"+prefix+"-btn primary big', 'Play again'\\); again.onclick = function \\(\\) \\{ G.location.reload\\(\\); \\};"),'');
 });
 edit(path.join(runtime,grade===5?'understanding-check.js':'el-understanding-check.js'),s=>{
  s=replace(s,`${K}.math(el('div', box, '${prefix}-prompt'), p.prompt);`,`${K}.math(el('div', box, '${prefix}-prompt'), p.prompt);\n    ${readQuestion}`);
  if(grade<=2)s=replace(s,"inp.autocomplete = 'off';",`inp.autocomplete = 'off';\n      var pad = G.MKKid.numberPad(box, inp, {answer:p.answer, grade:${grade}}); if(pad)pad.querySelector('.kid-check').remove();`);
  s=replace(s,"    el('div', box, 'big', right === n ? '🌟' : right >= n * 0.7 ? '🎉' : '💪');",`    G.MKKid.finish(box, {right:right,total:n,grade:${grade},unit:'grade${grade}:'+P.get('unit')});`);
  s=s.replace(/    el\('h2', box, null, right === n[^\n]+\n/,'');
  return s;
 });
 edit(path.join(runtime,grade===5?'flashcards.js':'el-flashcards.js'),s=>replace(s,"    btn.onclick = flip;",`    G.MKReadAloud.button(cardBox, function(){return st.flipped ? c.back + (c.example ? '. Example: '+c.example : '') : c.front;}, {grade:${grade}});\n    btn.onclick = flip;`));
 for(const name of fs.readdirSync(wg).filter(n=>new RegExp('^grade'+grade+'-(games|understanding-check|flashcards)\\.html$').test(n))){
  const file=path.join(wg,name);let s=fs.readFileSync(file,'utf8');if(!s.includes('MK_KID_BASE')){
   const base=grade===5?'grade5/kid-ui/':'elementary/kid-ui/';
   const tags=`<link rel="stylesheet" href="${base}kid-ui.css"><script>window.MK_KID_BASE=${JSON.stringify(base)};window.MK_KID_GRADE=${grade};</script><script src="${base}read-aloud.js"></script><script src="${base}kid-ui.js"></script>\n`;
   s=replace(s,'</head>',tags+'</head>');
   s=s.replace(/((?:elementary|grade5)\/(?:el-|g5-)?(?:core|games|flashcards|understanding-check)\.js\?[^"\s]+)/g,'$1-kid-player-v1');
   fs.writeFileSync(file,s);
  }
 }
 // Each assembled course receives a copy of the shared skill picker.
 const setup=path.join(wg,'games/skill-setup.js');fs.copyFileSync(path.join(out,'worksheet-generator/games/skill-setup.js'),setup);
}
console.log(`Kid player: Grades 1–5 read-aloud, rewards, student Play screens; Grades 1–2 keypads; ${wording} shorter prompts in both bank copies.`);
