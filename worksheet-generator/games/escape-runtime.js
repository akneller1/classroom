(function(ROOM){
const TOTAL=10*60, HINT_COST=90, STAGES=ROOM.stages;
let t=TOTAL, used=0, stage=-1, timer=null, cards=[], hintsShown={}, st={};
const $=s=>document.querySelector(s);
const ALPHA='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const caesar=(s,k)=>s.replace(/[A-Z]/g,c=>ALPHA[(ALPHA.indexOf(c)+k+26)%26]);
const fmt=s=>{s=Math.max(0,s);return String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')};
function tick(){t--;$('#clock').textContent=fmt(t);$('#clock').classList.toggle('low',t<300);if(t<=0){clearInterval(timer);timeUp()}}
function dots(){$('#dots').innerHTML=STAGES.map((_,i)=>`<div class="dot ${i<stage?'done':''} ${i==stage?'now':''}"></div>`).join('')}
function timeUp(){const el=document.createElement('div');el.className='panel';el.style.cssText='position:fixed;top:70px;left:50%;transform:translateX(-50%);z-index:9;border-color:var(--red)';el.innerHTML='⏰ Time is up! Keep going, but note how long your team takes.<br><button onclick="this.parentNode.remove()">Keep going</button>';document.body.appendChild(el)}
function wrong(msg){t=Math.max(0,t-30);const clock=$('#clock');if(clock)clock.textContent=fmt(t);say(msg+' (−30 seconds)',false);if(t<=0&&timer){clearInterval(timer);timer=null;timeUp()}}
function say(txt,ok){const m=$('#m');m.textContent=txt;m.className='msg '+(ok?'good':'bad');if(!ok){const p=m.closest('.panel');p.classList.remove('shake');void p.offsetWidth;p.classList.add('shake')}}
function getHint(){const s=STAGES[stage];hintsShown[stage]=hintsShown[stage]||0;if(hintsShown[stage]>=s.hints.length)return;t-=HINT_COST;used++;$('#hu').textContent=used;$('#clock').textContent=fmt(t);hintsShown[stage]++;$('#hints').innerHTML=s.hints.slice(0,hintsShown[stage]).map(h=>`<div class="hint">💡 ${h}</div>`).join('')}
function pass(){cards.push({stamp:STAGES[stage].stamp,letter:STAGES[stage].letter});stage++;dots();show()}
/* ---- scenes ---- */
function sceneEmoji(sc){
 const items=(sc.items||[]).map((it,i)=>`<g class="hot" data-i="${i}" onclick="hot(${i})"><text x="${it.x}" y="${it.y}" font-size="${it.s||44}" text-anchor="middle">${it.e}</text></g>`).join('');
 return `<svg class="scene" viewBox="0 0 400 300"><rect width="400" height="300" fill="${sc.bg||'#0b0e20'}"/><rect y="230" width="400" height="70" fill="${sc.floor||'#1b1f3f'}"/>${items}<text x="200" y="292" fill="#9aa0c3" font-size="12" text-anchor="middle">${sc.caption||'(click things to inspect them)'}</text></svg>`}
function hot(i){const it=STAGES[stage].scene.items[i];if(it.clue){const n=$('#note');if(n)n.innerHTML=`<div class="note">${it.clue}</div>`;say(it.msg||'You found something!',true)}else say(it.msg||'Nothing useful here.',true)}
function sceneGrid(sc){
 const W=400,H=sc.h||400,pad=26,ux=(W-2*pad)/(sc.xmax-sc.xmin),uy=(H-2*pad)/(sc.ymax-sc.ymin),u=Math.min(ux,uy);
 const X=x=>pad+(x-sc.xmin)*u,Y=y=>H-pad-(y-sc.ymin)*u,step=(sc.xmax-sc.xmin)>14?2:1;
 let g='';
 for(let x=sc.xmin;x<=sc.xmax;x++){g+=`<line x1="${X(x)}" y1="${Y(sc.ymin)}" x2="${X(x)}" y2="${Y(sc.ymax)}" stroke="#222a55"/>`;if(x%step==0&&x!=0)g+=`<text x="${X(x)}" y="${Y(Math.max(sc.ymin,Math.min(0,sc.ymax)))+13}" fill="#9aa0c3" font-size="10" text-anchor="middle">${x}</text>`}
 for(let y=sc.ymin;y<=sc.ymax;y++){g+=`<line x1="${X(sc.xmin)}" y1="${Y(y)}" x2="${X(sc.xmax)}" y2="${Y(y)}" stroke="#222a55"/>`;if(y%step==0&&y!=0)g+=`<text x="${X(Math.max(sc.xmin,Math.min(0,sc.xmax)))-4}" y="${Y(y)+4}" fill="#9aa0c3" font-size="10" text-anchor="end">${y}</text>`}
 const ax=Math.max(sc.xmin,Math.min(0,sc.xmax)),ay=Math.max(sc.ymin,Math.min(0,sc.ymax));
 g+=`<line x1="${X(ax)}" y1="${Y(sc.ymin)}" x2="${X(ax)}" y2="${Y(sc.ymax)}" stroke="#6a72c0" stroke-width="2"/><line x1="${X(sc.xmin)}" y1="${Y(ay)}" x2="${X(sc.xmax)}" y2="${Y(ay)}" stroke="#6a72c0" stroke-width="2"/>`;
 (sc.polys||[]).forEach(p=>{g+=`<polygon points="${p.pts.map(q=>X(q[0])+','+Y(q[1])).join(' ')}" fill="${p.fill||'none'}" fill-opacity=".25" stroke="${p.color||'#ffc857'}" stroke-width="3"/>`;if(p.label)g+=`<text x="${X(p.lx)}" y="${Y(p.ly)}" fill="${p.color||'#ffc857'}" font-size="13" font-weight="700">${p.label}</text>`});
 (sc.lines||[]).forEach(l=>{g+=`<line x1="${X(l.a[0])}" y1="${Y(l.a[1])}" x2="${X(l.b[0])}" y2="${Y(l.b[1])}" stroke="${l.color||'#ff3d5a'}" stroke-width="4"/>`;if(l.label)g+=`<text x="${X(l.lx)}" y="${Y(l.ly)}" fill="${l.color||'#ff3d5a'}" font-size="13" font-weight="700">${l.label}</text>`});
 (sc.points||[]).forEach(p=>{g+=`<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="5" fill="${p.color||'#fff'}"/>`;if(p.label)g+=`<text x="${X(p.x)+7}" y="${Y(p.y)-7}" fill="#fff" font-size="13" font-weight="700">${p.label}</text>`});
 return `<svg class="scene" viewBox="0 0 ${W} ${H}">${g}</svg>`}
function scene(s){const sc=s.scene||{kind:'emoji',items:[]};if(sc.kind==='image')return '<img class="scene-image" src="../'+sc.src+'" alt="'+sc.alt+'">';return sc.kind=='grid'?sceneGrid(sc):sc.kind=='svg'?`<svg class="scene" viewBox="${sc.viewBox||'0 0 400 300'}"><rect width="100%" height="100%" fill="#0b0e20"/>${sc.svg}</svg>`:sceneEmoji(sc)}
/* ---- puzzles ---- */
const P={
bankChoice(s){return '<h2>'+s.title+'</h2>'+s.prompt+'<div class="source-choices">'+s.options.map((o,i)=>'<button class="source-choice" data-choice="'+i+'" onclick="pickSource('+i+')" aria-pressed="false">'+o+'</button>').join('')+'</div><button id="go" onclick="checkSource()">Unlock</button>';},
fields(s){return `<h2>${s.title||'Lock'}</h2><div>${s.prompt}</div><div class="row">${s.fields.map((f,i)=>s.ui=='dial'?`<div class="dialbox"><button onclick="dl(${i},1)">▲</button><div class="num" id="d${i}">0</div><button onclick="dl(${i},-1)">▼</button><small>${f.label}</small></div>`:`<span>${f.label}</span><input id="f${i}" type="number" step="any">`).join('')}<button id="go" onclick="chkFields()">${s.button||'Unlock'}</button></div>`},
classify(s){return `<h2>${s.title||'Panels'}</h2><div>${s.prompt||''}</div>${s.items.map((it,i)=>`<div class="q">${it}</div><div class="sw" id="sw${i}">${s.options.map((o,j)=>`<button onclick="pv(${i},${j})">${o}</button>`).join('')}</div>`).join('')}<button id="go" onclick="chkClass()">${s.button||'Test the code'}</button>`},
order(s){return `<h2>${s.title||'Put in order'}</h2><div>${s.prompt||''}</div><div id="ol"></div><button id="go" onclick="chkOrder()">${s.button||'Lock it in'}</button>`},
cipher(s){return `<h2>${s.title||'The Cipher'}</h2><div id="note"></div>${s.sourceChoices?'<div class="source-choices">'+s.sourceChoices.map((o,i)=>'<button class="source-choice" data-cipher-choice="'+i+'" onclick="chooseCipherAnswer('+i+')" aria-pressed="false">'+o+'</button>').join('')+'</div>':''}<div class="cipher">${caesar(s.plain,s.shift)}</div><div>${s.prompt||'Each letter was moved FORWARD in the alphabet by the shift. Set the decoder to undo it.'}</div><div class="row"><label>Calculated shift: <input id="shiftGuess" type="number" min="0" max="25" step="1" style="width:85px"></label><button onclick="lockShift()">Lock shift (wrong: −0:30)</button></div><div id="shiftTools" style="display:none"><div class="row"><button class="ghost" onclick="sh(-1)">−</button><b id="kk">shift locked</b><button class="ghost" onclick="sh(1)">+</button></div></div><div class="wheel" id="wheel"></div><div class="cipher" id="dec" style="color:var(--blue)"></div><div class="row">${s.askLabel||'Answer word'}: <input type="text" id="w" maxlength="14"> <button id="go" onclick="chkCipher()">Open</button></div>`}};
function show(){
 if(stage>=STAGES.length){finalStage();return}
 const s=STAGES[stage];st={};
 $('#app').innerHTML=`<main><div class="panel"><h2>Room ${stage+1}: ${s.name}</h2><p class="story">${s.story}</p>${scene(s)}</div><div class="panel">${P[s.type](s)}<div class="msg" id="m"></div><div id="hints"></div><button class="ghost" onclick="getHint()">💡 Hint (−1:30)</button>${stage?`<div style="margin-top:8px">Key cards: ${cards.map(c=>`<span class="card">${c.stamp}</span>`).join('')}</div>`:''}</div></main>`;
 if(s.type=='fields')st.dv=s.fields.map(()=>0);
 if(s.type=='classify')st.pick=s.items.map(()=>-1);
 if(s.type=='order'){let a=s.steps.map((_,i)=>i);do{a.sort(()=>Math.random()-.5)}while(a.every((v,i)=>v==i));st.ord=a;ordDraw()}
 if(s.type=='cipher'){st.k=0;st.shiftLocked=false;}
}
function pickSource(i){st.pickSource=i;document.querySelectorAll('[data-choice]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.choice===i)))}
function checkSource(){if(st.pickSource===undefined){say('Choose an answer first.',false);return}st.pickSource===STAGES[stage].answer?pass():wrong('Locked. Check your work and try again.')}
function dl(i,d){st.dv[i]=(st.dv[i]+d+10)%10;$('#d'+i).textContent=st.dv[i]}
function chkFields(){const s=STAGES[stage];const ok=s.fields.every((f,i)=>{const v=s.ui=='dial'?st.dv[i]:parseFloat($('#f'+i).value);const alts=[f.answer].concat(f.alts||[]);return alts.some(a=>Math.abs(v-a)<=(f.tol||1e-9))});ok?pass():wrong(s.fail||'Locked. Check your work and try again.' )}
function pv(i,j){st.pick[i]=j;[...$('#sw'+i).children].forEach((b,x)=>b.classList.toggle('on',x==j))}
function chkClass(){const s=STAGES[stage];s.answer.every((a,i)=>st.pick[i]==a)?pass():wrong(s.fail||'Alarm! At least one answer is wrong.' )}
function ordDraw(){const s=STAGES[stage];$('#ol').innerHTML=st.ord.map((v,p)=>`<div class="ord"><span class="t">${s.steps[v]}</span><button onclick="mv(${p},-1)">▲</button><button onclick="mv(${p},1)">▼</button></div>`).join('')}
function mv(p,d){const q=p+d;if(q<0||q>=st.ord.length)return;[st.ord[p],st.ord[q]]=[st.ord[q],st.ord[p]];ordDraw()}
function chkOrder(){const s=STAGES[stage];st.ord.every((v,i)=>v==i)?pass():wrong(s.fail||'Not quite in order. Re-read the logic.' )}
function chooseCipherAnswer(i){st.cipherAnswer=i;document.querySelectorAll('[data-cipher-choice]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.cipherChoice===i)))}
function lockShift(){if(STAGES[stage].sourceChoices&&st.cipherAnswer!==STAGES[stage].sourceCorrect){wrong('Solve the question and lock the correct answer first.');return;}const v=$('#shiftGuess').value.trim(),n=Number(v);if(!v||!Number.isInteger(n)||n<0||n>25){say('Enter a whole-number shift from 0 to 25.',false);return}if(n!==STAGES[stage].shift){wrong('Incorrect shift. Solve the clue before trying again.');return}st.shiftLocked=true;st.k=n;$('#shiftGuess').disabled=true;$('#shiftTools').style.display='block';sh(0);say('Shift locked. Decode the message and enter the password.',true)}
function sh(d){if(!st.shiftLocked)return;const s=STAGES[stage];st.k=(st.k+d+26)%26;$('#kk').textContent='shift '+st.k;$('#wheel').textContent='written: '+ALPHA.split('').join(' ')+'\nreal   : '+ALPHA.split('').map(c=>caesar(c,-st.k)).join(' ');$('#dec').textContent=caesar(caesar(s.plain,s.shift),-st.k)}
function chkCipher(){if(!st.shiftLocked){say('Lock the shift before submitting the code.',false);return}const s=STAGES[stage];$('#w').value.trim().toUpperCase()==s.answer.toUpperCase()?pass():wrong('Still locked. Check your shift.' )}
function finalStage(){const sh=[...cards].sort(()=>Math.random()-.5);
 $('#app').innerHTML=`<main style="grid-template-columns:1fr"><div class="panel"><h2>The Final Door</h2><p class="story">${ROOM.finalStory}</p><div>${sh.map(c=>`<span class="card">${c.stamp}<b>${c.letter}</b></span>`).join('')}</div><div class="row">${ROOM.finalAsk} <input type="text" id="w" maxlength="12"> <button id="go" onclick="fin()">Open</button></div><div class="msg" id="m"></div></div></main>`}
function fin(){$('#w').value.trim().toUpperCase()==ROOM.word?victory():wrong('Nothing happens. Re-check the order of the cards.' )}
function victory(){clearInterval(timer);$('#app').innerHTML=`<div id="end" class="panel big"><div style="font-size:4rem">${ROOM.endEmoji}</div><h2>You escaped!</h2><p>${ROOM.outro}</p><p>Escape time: <b>${fmt(TOTAL-t)}</b> &nbsp; Hints used: <b>${used}</b></p><button onclick="location.reload()">Play again</button></div>`}
function start(){stage=0;dots();timer=setInterval(tick,1000);show()}
function intro(){$('#app').innerHTML=`<div id="intro" class="panel big"><div style="font-size:3.5rem">${ROOM.endEmoji}</div><h2>${ROOM.title}</h2><p class="story">${ROOM.intro}</p><p>Work as a team. You have <b>10 minutes</b>. Each hint costs 1:30.</p><button onclick="start()">Begin</button></div>`}
if(location.hash=='#key'&&prompt('Teacher code')==='205'){$('#key').style.display='block';$('#key').innerHTML='<h2>Teacher answer key</h2>'+STAGES.map((s,i)=>`<p><b>Room ${i+1} (${s.name}):</b> ${s.key}</p>`).join('')+`<p><b>Final:</b> sort stamps ${[...STAGES].sort((a,b)=>a.stamp-b.stamp).map(s=>s.stamp).join(', ')} to spell <b>${ROOM.word}</b>.</p>`}
Object.assign(window,{hot,dl,chkFields,pv,chkClass,mv,chkOrder,lockShift,sh,chkCipher,fin,start,getHint,pickSource,checkSource,chooseCipherAnswer});window.MK_ESCAPE_STATE=()=>({stage,t,used,st,cards});window.MK_ESCAPE_ROOM=ROOM;intro();

})(window.MK_ACTIVE_ESCAPE_ROOM);
