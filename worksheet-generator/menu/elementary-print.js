/* Shared Grades 1–5 paper presentation. Bank questions, choices and keys stay intact. */
(function(G){'use strict';
const E=G.MK_ELEMENTARY_PRINT={},NS=G.MKMENU,doc=G.document;
const directions=G.MK_ELEMENTARY_DIRECTIONS;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const math=s=>NS.mathSafe(s??'');
const script=doc?.currentScript;
const base=script?new URL('../core/elementary/',script.src).href:'core/elementary/';
E.grade=cfg=>Number(/^grade([1-5])-/.exec(cfg?.unitId||'')?.[1]||0);
E.className=cfg=>{const g=E.grade(cfg);return g?'el-g'+(g<3?g:'35'):'';};
E.icon=(id,cls='')=>'<img class="'+esc(cls)+'" src="'+esc(base+'icons/'+id+'.svg')+'" alt="" aria-hidden="true">';
E.direction=function(cfg,key,activity){const entry=(activity?directions.activities:directions.formats)[key];return entry?'<div class="el-dir">'+E.icon(entry.icon)+'<span>'+esc(entry[E.grade(cfg)<3?'g12':'g35'])+'</span></div>':'';};
E.name=function(cfg){const young=E.grade(cfg)<3;return '<div class="el-name">'+E.icon('name')+'<span>'+(young?'My name':'Name')+'</span><span class="el-lines"></span>'+(young?'':'<span>Date</span><span class="el-lines el-date"></span>')+'</div>';};
E.header=function(cfg,title,version){const set=NS.skillSets[cfg.unitId];return '<div class="el-band">'+E.icon('count','el-mascot')+'<div><div class="el-unit">'+esc(set?.unitName||cfg.unitId)+(version?' · '+esc(version):'')+'</div><h1>'+esc(title)+'</h1></div></div>'+E.name(cfg);};
function singleBlank(p){return !p.mc&&!p.multi&&p.authoredFormat!=='plot'&&(String(p.prompt).match(/_{2,}/g)||[]).length===1&&!(p.parts||[]).some(pt=>pt.prompt)&&p.parts?.length===1;}
E.singleBlank=singleBlank;
E.prompt=function(p,key){let out=math(p.prompt);if(singleBlank(p))out=out.replace(/<span class="ans-box"[^>]*><\/span>/,()=>key?'<span class="ans-box key" aria-label="Answer: '+esc(p.parts[0].answer)+'">'+math(p.parts[0].answer)+'</span>':'<span class="ans-box answer" role="img" aria-label="blank"></span>');return out;};
function answer(cfg){return '<div class="el-answer"><span class="lbl">Answer</span><span class="box">'+(E.grade(cfg)<3?'<span class="el-lines"></span>':'')+'</span></div>';}
function work(){return '<div class="el-work" aria-label="Work space"></div>';}
function choices(opts){const short=opts.every(o=>String(o).replace(/⟨|⟩/g,'').length<=12);return '<div class="el-choices '+(short?'short':'long')+'">'+opts.map((o,i)=>'<div class="el-choice"><span class="el-bubble">'+String.fromCharCode(65+i)+'</span><span>'+math(o)+'</span></div>').join('')+'</div>';}
function format(cfg,si,p){const f=NS.sectionFormat(cfg,si);return f==='mc'&&p.mc?'multiple-choice':f==='multi'&&p.multi?'select-all':p.authoredFormat==='plot'?'plot':(p.parts||[]).some(pt=>pt.prompt)?'open-response':'short-answer-work';}
E.question=function(p,cfg,si,n){
 if(p.failed)return '<article class="mm-dish el-q mm-missing" data-uid="'+esc(p.uid)+'"><span class="el-num">'+n+'</span><div>No verified question. Choose another question before printing.</div></article>';
 const f=format(cfg,si,p),g=E.grade(cfg),points=!NS.isWorksheet(cfg)&&g>2?'<span class="el-points">'+esc(cfg.sections[si].points)+' pts</span>':'';
 let h='<article class="mm-dish el-q" data-uid="'+esc(p.uid)+'"><span class="el-num">'+n+'</span><div class="el-content">'+points+'<div class="mm-q el-prompt">'+E.prompt(p.mc?.prompt?Object.assign({},p,{prompt:p.mc.prompt}):p,false)+'</div>';
 if(p.work?.length)h+='<ol class="el-student-work">'+p.work.map(w=>'<li>'+math(w)+'</li>').join('')+'</ol>';
 if(p.fig&&NS.figHtml)h+='<div class="el-figure">'+NS.figHtml(p.fig)+'</div>';
 if(f==='multiple-choice')h+=p.mc.graphs?'<div class="el-choices long">'+p.mc.opts.map((o,i)=>'<div class="el-choice"><span class="el-bubble">'+String.fromCharCode(65+i)+'</span>'+NS.figHtml(p.mc.graphs[i])+'</div>').join('')+'</div>':choices(p.mc.opts);
 else if(f==='select-all')h+=choices(p.multi.opts);
 else if(f==='open-response')h+='<div class="el-parts" style="--el-part-count:'+p.parts.filter(pt=>pt.prompt).length+'">'+p.parts.filter(pt=>pt.prompt).map((pt,i)=>'<div><b>('+esc(pt.label||String.fromCharCode(97+i))+')</b> '+math(pt.prompt)+work()+'</div>').join('')+'</div>';
 else if(f!=='plot'&&!singleBlank(p))h+='<div class="el-workrow">'+(p.fig&&/count|how many (?:in all|are there)/i.test(p.prompt)?'':work())+answer(cfg)+'</div>';
 return h+'</div></article>';
};
E.renderPages=async function(state,vIdx){
 const cfg=state.config,g=E.grade(cfg),rows=[],version=state.versions[vIdx],max=g===1?4:6;
 let number=0;version.sections.forEach((s,si)=>s.items.forEach(p=>rows.push({p,si,n:++number})));
 const stage=doc.createElement('div');stage.className='measure-stage mm-stage';doc.body.appendChild(stage);
 if(doc.fonts?.ready)await doc.fonts.ready;
 const pages=[],overflow=[];let current;
 const title=NS.isWorksheet(cfg)?(cfg.title||'Worksheet'):directions.quiz.title[g<3?'g12':'g35'];
 function start(){const page=doc.createElement('div');page.className='page mm-page el-paper '+E.className(cfg);page.style.setProperty('--el-work-scale',({compact:.75,standard:1,spacious:1.4})[cfg.layout.density]||1);page.innerHTML='<div class="mm-body">'+E.header(cfg,title,state.versions.length>1?'Version '+version.label:'')+'<div class="el-paper-sections"></div></div><div class="el-foot"><span class="mm-pno"></span><span class="el-sticker"></span></div>';stage.appendChild(page);current={page,body:page.querySelector('.mm-body'),host:page.querySelector('.el-paper-sections'),count:0,section:null};pages.push(page);}
 function append(batch){const si=batch[0].si,f=format(cfg,si,batch[0].p),nodes=[];if(current.section!==si){const d=doc.createElement('div');d.className='el-part-heading';d.innerHTML='<div class="el-part-title">'+esc(cfg.sections[si].name||'')+'</div>'+E.direction(cfg,f);current.host.appendChild(d);nodes.push(d);}const row=doc.createElement('div');row.className='el-qs';if(batch.length===1)row.classList.add('el-single');row.innerHTML=batch.map(x=>E.question(x.p,cfg,x.si,x.n)).join('');current.host.appendChild(row);nodes.push(row);return nodes;}
 async function images(nodes){await Promise.all(nodes.flatMap(n=>[...n.querySelectorAll('img')]).map(img=>img.complete?Promise.resolve():new Promise(resolve=>{img.onload=img.onerror=resolve;})));}
 try{
  start();for(let i=0;i<rows.length;){let batch=[rows[i]];const wide=x=>String(x.p.prompt).length>240||(x.p.parts||[]).some(p=>p.prompt)||x.p.fig?.kind==='authored-plot';if(g>2&&rows[i+1]?.si===rows[i].si&&!wide(rows[i])&&!wide(rows[i+1]))batch.push(rows[i+1]);
   if(current.count+batch.length>max)start();let nodes=append(batch);await images(nodes);
   if(current.body.scrollHeight>current.body.clientHeight+1&&current.count){nodes.forEach(n=>n.remove());start();nodes=append(batch);await images(nodes);}
   if(current.body.scrollHeight>current.body.clientHeight+1&&batch.length===2){nodes.forEach(n=>n.remove());batch=batch.slice(0,1);nodes=append(batch);await images(nodes);}
   if(current.body.scrollHeight>current.body.clientHeight+1){if(current.count){nodes.forEach(n=>n.remove());start();nodes=append(batch);await images(nodes);}if(current.body.scrollHeight>current.body.clientHeight+1){overflow.push(batch[0].n);current.page.classList.add('el-oversize');}}
   current.count+=batch.length;current.section=batch[0].si;i+=batch.length;
  }
  pages.forEach((p,i)=>{p.querySelector('.mm-pno').textContent="Mr. K's Classroom · page "+(i+1);if(i===pages.length-1)p.querySelector('.el-sticker').innerHTML=E.icon('i-did-it');p.remove();});
  pages.overflow=overflow;return pages;
 }finally{stage.remove();}
};
// Activity boards keep their puzzle geometry. Flowing question sheets use the
// grade typography before measurement, so their existing paginator can adapt.
E.activity=function(cfg,html,key){
 if(!E.grade(cfg)||key)return html;
 const kind=({error:'error-analysis',color:'color-by-number',partner:'partner-check',match:'matching',tarsia:'cut-and-paste'})[cfg.kind]||cfg.kind;
 const line=E.direction(cfg,kind,true);if(!line)return html;
 html=html.replace(/<div class="(?:mm-name|pc-name|ps-nm|pe-names)">[\s\S]*?<\/div>/g,E.name(cfg));
 html=html.replace(/<div class="pp-names">[\s\S]*?<\/div>/g,E.name(cfg)+'<p class="el-partner-name">Partner’s name: __________________</p>');
 html=html.replace(/<div class="(?:mm-box mm-dirs pr-dirs|pp-dirs|ps-note|pe-sub)">[\s\S]*?<\/div>/g,old=>cfg.kind==='match'?line+old:line).replace(/<p class="pc-line">[\s\S]*?<\/p>/g,line);
 if(!html.includes('class="el-dir"'))html=html.replace(/(<div class="mm-body[^"]*">)/,'$1'+line);
 if(E.grade(cfg)<3)html=html.replace(/ \(1 point\)/g,'').replace(/<div class="pe-foot">[\s\S]*?<\/div>/g,'');
 return html;
};
})(typeof window!=='undefined'?window:globalThis);
