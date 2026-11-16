/* Reviewed Phase 3 activities, using the selected unit's authored questions and seeded facts. */
(function(G){'use strict';
const NS=G.MKMENU,PR=NS.printables,E=G.MK_ELEMENTARY_PRINT;
const young=cfg=>/^grade[12]-/.test(cfg.unitId),grade=cfg=>E.grade(cfg),math=s=>NS.mathSafe(String(s)),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const extras=[['roll-cover','Roll & Cover','Roll two dice. Add, find the sum and cover it.'],['cut-paste','Cut & Paste Sort','Cut out the cards and glue each in its group.'],['number-bonds','Number Bonds','Write the missing part or whole.'],['spin-solve','Spin & Solve','Use a paper clip and pencil. Spin, then solve.']];
extras.forEach(([id,name,blurb])=>PR.KINDS.push({id,name,blurb}));
PR.kindsFor=function(unit){return PR.KINDS.filter(x=>/^grade[12]-/.test(unit)?!['who','tarsia','vocabulary'].includes(x.id):!extras.some(e=>e[0]===x.id)).map(x=>/^grade[12]-/.test(unit)&&x.id==='maze'?Object.assign({},x,{name:'Stepping-Stone Maze',blurb:'Solve each island. Choose the stone with your answer to reach the treasure.'}):x)};
function rng(cfg,v){return G.MKWS.rng.make(G.MKWS.rng.hash([cfg.seed,v,cfg.kind].join('|')))}
function numeric(q){const m=/^\s*(\d+)(?:\s+[a-zA-Z]+)?\s*$/.exec(String(q.answer));return m?+m[1]:null}
function candidates(cfg,skill){const m=/^(grade[12])-(.+)$/.exec(cfg.unitId);if(!m)return [];
return G.MK_QUESTION_BANKS.select({courseId:m[1],unitId:m[2],level:cfg.level||'cp1',skillIds:skill?[skill]:Object.keys(cfg.skills||{}).filter(k=>cfg.skills[k]),formats:['short-answer']}).filter(q=>numeric(q)!==null&&!(q.parts||[]).length&&q.prompt.length<=(cfg.kind==='color'?90:155)&&(cfg.kind!=='color'||!q.diagram&&numeric(q)<=(grade(cfg)===1?20:100)))}
PR.youngSupported=function(unit,kind){if(!/^grade[12]-/.test(unit))return extras.some(e=>e[0]===kind)?false:null;
if(['who','tarsia','vocabulary'].includes(kind))return false;
if(extras.some(e=>e[0]===kind))return /(?:add-subtract|odd-even|place-value|word-problems)/.test(unit);
return null};
const cap=PR.capable;
PR.capable=function(unit,skill,kind,level){if(/^grade[12]-/.test(unit)&&['maze','color',...extras.map(e=>e[0])].includes(kind)){
if(extras.some(e=>e[0]===kind))return PR.youngSupported(unit,kind);
return candidates({unitId:unit,kind,level:level||'cp1',skills:{[skill]:true}},skill).length>0;
}return cap.apply(this,arguments)};
const build=PR.build;
PR.build=function(cfg,v){if(!young(cfg)||!['maze','color',...extras.map(e=>e[0])].includes(cfg.kind))return build.apply(this,arguments);
const r=rng(cfg,v),g=grade(cfg),B={kind:cfg.kind,young:true,items:[]};
if(cfg.kind==='maze'||cfg.kind==='color'){
 const seen=new Set(),n=cfg.kind==='color'?6:g===1?4:6;
 for(const q of r.shuffle(candidates(cfg))){const answer=numeric(q);if(seen.has(answer))continue;seen.add(answer);const p=NS.authoredProblem(q,cfg.unitId,4);B.items.push({p,key:String(answer),answer,correctLeft:r.int(0,1)===0,wrong:answer===0?1:answer+(r.int(0,1)?1:-1)});if(B.items.length===n)break}
 if(B.items.length<n)return {error:'This activity needs '+n+' different whole-number answers at this level. Select more skills or another activity.'};
}else if(cfg.kind==='roll-cover'){
 const base=Array.from({length:11},(_,i)=>i+2),weighted=[];for(let a=1;a<=6;a++)for(let b=1;b<=6;b++)weighted.push(a+b);B.board=r.shuffle(base.concat(Array.from({length:9},()=>r.pick(weighted))));
}else if(cfg.kind==='cut-paste'){
 const even=g===2;B.labels=even?['Even','Odd']:['Makes 10','Does not make 10'];
 B.cards=r.shuffle(Array.from({length:8},(_,i)=>{const group=i<4?0:1,a=r.int(1,8),b=group===0?10-a:r.int(1,9);const value=even?r.int(1,24)*2+group:a+(group===1&&a+b===10?b+1:b);return {text:even?String(value):a+' + '+(value-a),group,value}}));
}else if(cfg.kind==='number-bonds'){
 const max=g===2?10:/add-subtract-20/.test(cfg.unitId)?20:10,min=max===20?11:5,mult=g===2?10:1;
 B.bonds=Array.from({length:6},(_,i)=>{const whole=r.int(min,max)*mult,a=r.int(1,whole/mult-1)*mult;return {values:[whole,a,whole-a],missing:i%3}});
}else {B.spins=r.shuffle([1,2,3,4,5,6,7,8]);B.target=g===2?20:10}
return B};
const colors=[['Blue','#4f8fe8'],['Orange','#ff8a1f'],['Yellow','#ffd23f'],['Green','#22c08a'],['Black','#222222'],['White','#ffffff']];
const fish=['BBBBBBBBBBBB','BBWBBBBBBBBB','BBBBBBBBBWBB','BBBBOOOOBBBB','BBBOOOOOOBYY','BBOOKOOOOYYB','BBOOOOOOOYYB','BBBOOOOOOBYY','BBBBOOOOBBBB','BBBBBBBBBBWB','GGBBGBBBBGBB','GGGGGGGGGGGG'];
function qhtml(it){return E.prompt(it.p,false)+(it.p.fig?'<div class="el-figure">'+NS.figHtml(it.p.fig)+'</div>':'')}
function box(value,key){return key?'<b>'+math(value)+'</b>':'<span class="ans-box answer" aria-label="blank"></span>'}
PR.youngPages=function(cfg,B,v,nV,key){
 if(B.kind==='maze'&&B.items.length>4){const pages=[];for(let i=0;i<B.items.length;i+=3)pages.push(...PR.youngPages(Object.assign({},cfg,{mazeStart:i,mazeLast:i+3>=B.items.length}),Object.assign({},B,{items:B.items.slice(i,i+3)}),v,nV,key));return pages;}
 const name=PR.kindsFor(cfg.unitId).find(x=>x.id===cfg.kind),r=rng(cfg,v);let h='';
 if(B.kind==='maze')h='<div class="path"><div class="start">'+(cfg.mazeStart?'CONTINUE FROM PAGE '+Math.ceil(cfg.mazeStart/3):'START')+'</div>'+B.items.map((it,i)=>'<div class="island"><b>'+(i+1+(cfg.mazeStart||0))+'</b><div>'+qhtml(it)+'</div></div><div class="stones">'+(it.correctLeft?[it.answer,it.wrong]:[it.wrong,it.answer]).map(a=>'<div class="stone '+(key?(a===it.answer?'ok':'no'):'')+'"><span>'+a+'</span>'+(key?'<em>'+(a===it.answer?'Go on':'Oops! Go back')+'</em>':'')+'</div>').join('')+'</div>').join('')+'<div class="treasure">'+(cfg.mazeLast===false?'KEEP GOING ON THE NEXT PAGE':'TREASURE')+'</div></div>';
 if(B.kind==='color'){
 h='<div class="cbn-probs">'+B.items.map((it,i)=>'<div class="cbn-row"><span>'+(i+1)+'. '+E.prompt(it.p,key)+'</span> → <span class="pr-sw" style="background:'+colors[i][1]+'"></span> '+colors[i][0]+'</div>').join('')+'</div><div class="cbn-grid">';
 fish.forEach((row,y)=>[...row].forEach((c,x)=>{const i='BOYGKW'.indexOf(c);h+='<div style="'+(key?'background:'+colors[i][1]+';color:'+([0,4].includes(i)?'#fff':'#14173a'):'')+'">'+B.items[i].answer+'</div>'}));h+='</div>';
 }if(B.kind==='roll-cover')h='<div class="yc-board">'+B.board.map(a=>'<div>'+a+'</div>').join('')+'</div><h2>My rolls</h2>'+Array.from({length:3},()=>'<p>'+box('',false)+' + '+box('',false)+' = '+box('',false)+'</p>').join('')+(key?'<p>Each sum 2–12 appears. Cover any matching uncovered square. Partner with the most covered squares wins. Roll records vary.</p>':'<p>Take turns. Roll two dice, add, and cover one matching square. Most covered squares wins.</p>');
 if(B.kind==='cut-paste')h='<div class="cp-bins">'+B.labels.map((l,i)=>'<div class="cp-bin"><div class="cp-h">'+esc(l)+'</div>'+Array.from({length:4},()=>'<div class="cp-slot"></div>').join('')+(key?B.cards.filter(c=>c.group===i).map(c=>math(c.text)).join(', '):'')+'</div>').join('')+'</div><div class="cp-cutline">'+E.icon('cut')+' Cut. '+E.icon('glue')+' Glue.</div><div class="cp-cards">'+B.cards.map(c=>'<div class="cp-card">'+math(c.text)+'</div>').join('')+'</div>';
 if(B.kind==='number-bonds')h='<div class="bonds">'+B.bonds.map(b=>'<div class="bond"><svg class="bond-lines" viewBox="0 0 200 150"><path d="M100 35L50 115M100 35L150 115" fill="none" stroke="#14173a" stroke-width="3"/></svg>'+b.values.map((a,i)=>'<div class="bc '+['whole','p1','p2'][i]+'">'+(i===b.missing?box(a,key):a)+'</div>').join('')+'</div>').join('')+'</div>';
 if(B.kind==='spin-solve'){
 h='<div class="ss-wrap"><svg class="spinner" viewBox="0 0 300 300" role="img" aria-label="Eight-sector spinner">';
 B.spins.forEach((a,i)=>{const t=i*Math.PI/4,x=150+140*Math.cos(t),y=150+140*Math.sin(t);h+='<path d="M150 150L'+x+' '+y+'A140 140 0 0 1 '+(150+140*Math.cos(t+Math.PI/4))+' '+(150+140*Math.sin(t+Math.PI/4))+'Z" fill="'+(i%2?'#d6f5e8':'#fff4e0')+'" stroke="#14173a"/><text x="'+(150+100*Math.cos(t+Math.PI/8))+'" y="'+(156+100*Math.sin(t+Math.PI/8))+'" text-anchor="middle" font-size="24">'+a+'</text>'});h+='</svg><div class="ss-rows">'+Array.from({length:6},()=>'<div class="ss-row">I spun '+box('',false)+' + '+box('',false)+' = '+B.target+'</div>').join('')+'</div></div>'+(key?'<p>Spin → missing part: '+B.spins.map(a=>a+' → '+(B.target-a)).join('; ')+'.</p>':'');
 }
 return [{cls:E.className(cfg)+' el-activity yc-paper',nofoot:true,html:'<div class="mm-body">'+E.header(cfg,name.name+(key?' · Teacher key':''),'Version '+'ABC'[v])+'<div class="el-dir">'+esc(name.blurb)+'</div>'+h+'</div>'}];
};
})(window);
