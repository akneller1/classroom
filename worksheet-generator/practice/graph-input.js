/* Student graph responses for Assessment Readiness Check.
   Answers are saved as data, not drawn annotations, so they can be graded. */
(function(G){
'use strict';
var API=G.MKGRAPH=(G.MKGRAPH||{});
function val(p){if(p==null)return null;if(Array.isArray(p))return p[0]/p[1];if(typeof p==='object'&&'n'in p)return p.n/p.d;return +p;}
function equal(a,b){return a===null&&b===null||a!==null&&b!==null&&Math.abs(a-b)<1e-7;}
function norm(p){return {lo:val(p.lo),hi:val(p.hi),loC:!!p.loC,hiC:!!p.hiC};}
function isGraph(q){var p=q.problem;return q.kind!=='mc'&&p&&p.parts&&p.parts.length===1&&p.parts[0].answerFig&&p.parts[0].answerFig.kind==='numberline';}
API.supports=isGraph;
function serialize(parts){return 'graph:'+JSON.stringify(parts);}
function parse(response){if(typeof response!=='string'||!response.startsWith('graph:'))return null;try{var p=JSON.parse(response.slice(6));return Array.isArray(p)?p:null;}catch(e){return null;}}
function expected(q){return (q.problem.parts[0].answerFig.pieces||[]).map(norm);}
function same(a,b){return equal(a.lo,b.lo)&&equal(a.hi,b.hi)&&(a.lo===null||a.loC===b.loC)&&(a.hi===null||a.hiC===b.hiC);}
API.grade=function(q){var answer=expected(q),given=parse(q.response);if(!given)return {status:'empty'};if(given.length!==answer.length)return {status:'incorrect'};var taken=new Set();return {status:given.every(function(a){var k=answer.findIndex(function(b,i){return !taken.has(i)&&same(a,b);});if(k<0)return false;taken.add(k);return true;})?'correct':'incorrect'};};
function segmentSVG(p,min,max){var x=v=>36+(v-min)/(max-min)*524;var lo=p.lo===null?min:p.lo,hi=p.hi===null?max:p.hi;return '<line x1="'+x(lo)+'" x2="'+x(hi)+'" y1="44" y2="44" stroke="#2465a7" stroke-width="5" stroke-linecap="round"/>'+(p.lo===null?'<path d="M 36 44 l 12 -8 v 16 z" fill="#2465a7"/>':'<circle cx="'+x(lo)+'" cy="44" r="7" stroke="#2465a7" stroke-width="3" fill="'+(p.loC?'#2465a7':'white')+'"/>')+(p.hi===null?'<path d="M 560 44 l -12 -8 v 16 z" fill="#2465a7"/>':'<circle cx="'+x(hi)+'" cy="44" r="7" stroke="#2465a7" stroke-width="3" fill="'+(p.hiC?'#2465a7':'white')+'"/>');}
function draw(q,preview){var fig=q.problem.parts[0].answerFig, min=+fig.min,max=+fig.max;if(!Number.isFinite(min)||!Number.isFinite(max)||min>=max){min=-10;max=10;}var parts=preview||parse(q.response)||[],ticks='';for(var n=Math.ceil(min);n<=Math.floor(max);n++){if(max-min>32&&n%2)continue;var x=36+(n-min)/(max-min)*524;ticks+='<line x1="'+x+'" x2="'+x+'" y1="37" y2="51" stroke="#71879a"/><text x="'+x+'" y="71" text-anchor="middle" font-size="12" fill="#294660">'+n+'</text>';}return '<svg viewBox="0 0 596 82" role="img" aria-label="Interactive number line" class="pt-numberline-svg"><line x1="30" x2="566" y1="44" y2="44" stroke="#566d82" stroke-width="2"/>'+ticks+parts.map(p=>segmentSVG(p,min,max)).join('')+'</svg>';}
function controls(q,i){var fig=q.problem.parts[0].answerFig, min=Number(fig.min),max=Number(fig.max);if(!Number.isFinite(min)||!Number.isFinite(max)||min>=max){min=-10;max=10;}var pieces=parse(q.response)||[];var html='<div class="pt-graph-editor" data-graph="'+i+'"><strong>Graph your solution on the number line</strong><p class="pt-muted">Touch a number, drag left or right, and release to shade that direction. Choose Open or Closed for the endpoint. Use advanced endpoints for intervals between two values.</p>'+draw(q)+'<details class="pt-advanced-interval"><summary>Advanced: enter exact endpoints or bounded intervals</summary>';for(var j=0;j<Math.max(1,pieces.length);j++){var a=pieces[j]||{lo:null,hi:null,loC:false,hiC:false};html+='<div class="pt-interval-row" data-interval="'+j+'"><label>Left endpoint<input data-end="lo" type="text" inputmode="decimal" pattern="-?[0-9]*[.]?[0-9]*" placeholder="−∞" value="'+(a.lo===null?'':a.lo)+'"><button type="button" data-sign="lo" aria-label="Change left endpoint sign">±</button></label><label><input type="checkbox" data-end="loC" '+(a.loC?'checked':'')+'> Closed</label><label>Right endpoint<input data-end="hi" type="text" inputmode="decimal" pattern="-?[0-9]*[.]?[0-9]*" placeholder="+∞" value="'+(a.hi===null?'':a.hi)+'"><button type="button" data-sign="hi" aria-label="Change right endpoint sign">±</button></label><label><input type="checkbox" data-end="hiC" '+(a.hiC?'checked':'')+'> Closed</label><button type="button" data-remove="'+j+'" class="pt-secondary">Remove</button></div>';}return html+'</details><div class="pt-drag-controls"><label>Endpoint <select data-drag-circle aria-label="Endpoint circle"><option value="open">Open circle (&lt; or &gt;)</option><option value="closed">Closed circle (≤ or ≥)</option></select></label><button type="button" data-reverse-ray class="pt-secondary">Reverse direction</button></div><p class="pt-muted">Drag from your endpoint toward the shaded side. For compound solutions, add another interval below.</p><div class="pt-actions"><button type="button" data-pick-end="lo" aria-pressed="false" class="pt-secondary">Set left endpoint</button><button type="button" data-pick-end="hi" aria-pressed="false" class="pt-secondary">Set right endpoint</button></div><div class="pt-actions"><button type="button" data-add-interval>Add interval</button><button type="button" data-empty-graph class="pt-secondary">No solution</button><button type="button" data-all-graph class="pt-secondary">All real numbers</button></div></div>';}
API.render=controls;
API.bind=function(root,state,save){root.querySelectorAll('[data-graph]').forEach(function(box){var i=+box.dataset.graph,q=state.questions[i];function collect(){var rows=[...box.querySelectorAll('[data-interval]')].map(function(row){function number(end){var v=row.querySelector('[data-end="'+end+'"]').value.trim().replace(/−/g,"-");if(v==="")return null;if(!/^-?(?:\d+(?:\.\d*)?|\.\d+)$/.test(v))throw Error("Enter a valid number");return Number(v);}return {lo:number('lo'),hi:number('hi'),loC:row.querySelector('[data-end="loC"]').checked,hiC:row.querySelector('[data-end="hiC"]').checked};});q.response=serialize(rows);save();box.querySelector('svg').outerHTML=draw(q);}box.querySelectorAll('[data-pick-end]').forEach(function(btn){btn.onclick=function(){var active=box.dataset.pickEnd===btn.dataset.pickEnd?'':btn.dataset.pickEnd;box.dataset.pickEnd=active;box.querySelectorAll('[data-pick-end]').forEach(b=>{b.classList.toggle('pt-selected-tool',b.dataset.pickEnd===active);b.setAttribute('aria-pressed',String(b.dataset.pickEnd===active));});};});
 var board=box.querySelector('svg');
 var dragSelect=box.querySelector('[data-drag-circle]'),oldParts=parse(q.response)||[];
 if(dragSelect&&oldParts.length===1){var ep=oldParts[0];dragSelect.value=(ep.lo!==null?ep.loC:ep.hiC)?'closed':'open';}
 function frameFromEvent(ev){
   var rect=board.getBoundingClientRect(),fig=q.problem.parts[0].answerFig,lo=Number(fig.min),hi=Number(fig.max);
   if(!Number.isFinite(lo)||!Number.isFinite(hi)||hi<=lo){lo=-10;hi=10;}
   var svgX=(ev.clientX-rect.left)/rect.width*596;
   return Math.max(lo,Math.min(hi,Math.round(lo+(svgX-36)/524*(hi-lo))));
 }
 function renderPreview(parts){
   var svg=draw(q,parts);
   board.innerHTML=svg.slice(svg.indexOf('>')+1,svg.lastIndexOf('</svg>'));
 }
 function dragPart(startValue,direction){
   var closed=dragSelect&&dragSelect.value==='closed';
   return direction==='left'?{lo:null,hi:startValue,loC:false,hiC:closed}:{lo:startValue,hi:null,loC:closed,hiC:false};
 }
 function repaint(){box.outerHTML=controls(q,i);API.bind(root,state,save);}
 function commitRay(part){
   var parts=parse(q.response)||[];
   if(parts.length)parts[0]=part;else parts=[part];
   q.response=serialize(parts);save();repaint();
 }
 if(board){
   var drag=null;
   board.addEventListener('pointerdown',function(ev){
     if(ev.button!==undefined&&ev.button!==0)return;
     ev.preventDefault();
     var v=frameFromEvent(ev);
     drag={id:ev.pointerId,value:v,direction:'right'};
     if(board.setPointerCapture)board.setPointerCapture(ev.pointerId);
     renderPreview([dragPart(v,'right')]);
   });
   board.addEventListener('pointermove',function(ev){
     if(!drag||ev.pointerId!==drag.id)return;
     ev.preventDefault();
     var v=frameFromEvent(ev);
     if(v<drag.value)drag.direction='left';
     if(v>drag.value)drag.direction='right';
     renderPreview([dragPart(drag.value,drag.direction)]);
   });
   board.addEventListener('pointerup',function(ev){
     if(!drag||ev.pointerId!==drag.id)return;
     ev.preventDefault();
     var v=frameFromEvent(ev);
     if(v<drag.value)drag.direction='left';
     if(v>drag.value)drag.direction='right';
     var part=dragPart(drag.value,drag.direction);
     drag=null;commitRay(part);
   });
   board.addEventListener('pointercancel',function(){drag=null;repaint();});
 }
 if(dragSelect)dragSelect.onchange=function(){
   var p=(parse(q.response)||[])[0];
   if(!p)return;
   var closed=dragSelect.value==='closed';
   if(p.lo!==null)p.loC=closed;
   if(p.hi!==null)p.hiC=closed;
   commitRay(p);
 };
 var reverse=box.querySelector('[data-reverse-ray]');
 if(reverse)reverse.onclick=function(){
   var p=(parse(q.response)||[])[0];
   if(!p)return;
   if(p.lo!==null&&p.hi===null)commitRay({lo:null,hi:p.lo,loC:false,hiC:p.loC});
   else if(p.hi!==null&&p.lo===null)commitRay({lo:p.hi,hi:null,loC:p.hiC,hiC:false});
 };
 box.querySelectorAll('[data-pick-end]').forEach(function(btn){
   btn.onclick=function(){
     var end=btn.dataset.pickEnd,p=(parse(q.response)||[])[0]||{lo:null,hi:null,loC:false,hiC:false};
     var v=end==='lo'?(p.hi===null?0:p.hi):(p.lo===null?0:p.lo);
     p[end]=v;q.response=serialize([p]);save();repaint();
   };
 });
 box.querySelectorAll('[data-sign]').forEach(btn=>btn.onclick=function(){var el=btn.parentNode.querySelector('input');el.value=el.value.trim().startsWith('-')?el.value.trim().slice(1):'-'+el.value.trim();el.dispatchEvent(new Event('change',{bubbles:true}));});box.querySelectorAll('input').forEach(el=>{el.addEventListener('input',function(){try{collect();}catch(e){/* An unfinished minus sign is valid while typing. */}});el.addEventListener('change',function(){try{collect();}catch(e){el.setCustomValidity('Please enter a valid signed number.');el.reportValidity();el.setCustomValidity('');}});});box.querySelector('[data-add-interval]').onclick=function(){collect();var parts=parse(q.response)||[];parts.push({lo:null,hi:null,loC:false,hiC:false});q.response=serialize(parts);save();box.outerHTML=controls(q,i);API.bind(root,state,save);};box.querySelectorAll('[data-remove]').forEach(btn=>btn.onclick=function(){var parts=parse(q.response)||[];parts.splice(+btn.dataset.remove,1);q.response=serialize(parts);save();box.outerHTML=controls(q,i);API.bind(root,state,save);});box.querySelector('[data-empty-graph]').onclick=function(){q.response=serialize([]);save();box.outerHTML=controls(q,i);API.bind(root,state,save);};box.querySelector('[data-all-graph]').onclick=function(){q.response=serialize([{lo:null,hi:null,loC:false,hiC:false}]);save();box.outerHTML=controls(q,i);API.bind(root,state,save);};});};

/* Plot-a-point questions: store the plotted coordinate and grade both axes exactly. */
function pointTarget(q){var p=q.problem;if(!p||!p.parts||p.parts.length!==1||!/(plot|graph)\s+(?:the\s+)?(?:point|ordered pair)/i.test(p.prompt||''))return null;var a=String(p.parts[0].answer||'').replace(/[⟨⟩]/g,'').trim();var m=/^\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)$/.exec(a);return m?[+m[1],+m[2]]:null;}
API.pointTarget=pointTarget;
function pointRead(q){var m=/^point:(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)$/.exec(q.response||'');return m?[+m[1],+m[2]]:null;}
function pointSVG(q){var a=pointRead(q),html='';for(var v=-10;v<=10;v++){var n=160+v*14;html+='<line x1="'+n+'" x2="'+n+'" y1="20" y2="300" stroke="#e0e8f0"/><line x1="20" x2="300" y1="'+n+'" y2="'+n+'" stroke="#e0e8f0"/>';}html+='<path d="M160 20V300 M20 160H300" stroke="#607a91" stroke-width="2"/>';if(a)html+='<circle cx="'+(160+a[0]*14)+'" cy="'+(160-a[1]*14)+'" r="6" fill="#245eab" stroke="white" stroke-width="2"/>';return '<svg class="pt-coordinate-svg" viewBox="0 0 320 320" role="img" aria-label="Click or tap a grid intersection to plot a point">'+html+'<text x="304" y="154" font-size="12">x</text><text x="166" y="15" font-size="12">y</text></svg>';}
function pointHTML(q,i){var a=pointRead(q)||['',''];return '<div class="pt-graph-editor pt-point-editor" data-point="'+i+'"><strong>Plot your point on the coordinate plane</strong><p class="pt-muted">Tap a grid intersection or enter the coordinates. The point is graded automatically.</p>'+pointSVG(q)+'<div class="pt-interval-row"><label>x<input type="text" inputmode="decimal" pattern="-?[0-9]*[.]?[0-9]*" data-axis="x" value="'+a[0]+'"><button type="button" data-axis-sign="x">±</button></label><label>y<input type="text" inputmode="decimal" pattern="-?[0-9]*[.]?[0-9]*" data-axis="y" value="'+a[1]+'"><button type="button" data-axis-sign="y">±</button></label></div></div>';}
API.pointHTML=pointHTML;
API.pointGrade=function(q){var a=pointRead(q),b=pointTarget(q);return {status:!a?'empty':a[0]===b[0]&&a[1]===b[1]?'correct':'incorrect'};};
API.bindPoints=function(root,state,save){root.querySelectorAll('[data-point]').forEach(function(box){var q=state.questions[+box.dataset.point];box.querySelectorAll('[data-axis-sign]').forEach(btn=>btn.onclick=function(){var el=box.querySelector('[data-axis="'+btn.dataset.axisSign+'"]');el.value=el.value.startsWith('-')?el.value.slice(1):'-'+el.value;el.dispatchEvent(new Event('change',{bubbles:true}));});function set(x,y){q.response='point:'+x+','+y;save();box.querySelector('svg').outerHTML=pointSVG(q);box.querySelector('[data-axis="x"]').value=x;box.querySelector('[data-axis="y"]').value=y;}box.querySelectorAll('[data-axis]').forEach(function(input){input.onchange=function(){var x=box.querySelector('[data-axis="x"]').value,y=box.querySelector('[data-axis="y"]').value;if(x!==''&&y!=='')set(+x,+y);};});box.querySelector('svg').onclick=function(ev){var rect=this.getBoundingClientRect();var x=Math.round(((ev.clientX-rect.left)/rect.width*320-160)/14),y=Math.round((160-(ev.clientY-rect.top)/rect.height*320)/14);set(Math.max(-10,Math.min(10,x)),Math.max(-10,Math.min(10,y)));};});};

})(window);
