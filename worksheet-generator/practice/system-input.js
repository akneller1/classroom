/* Two-line graphing for systems: each boundary is drawn from two student points. */
(function(G){
'use strict';
var API=G.MKSYSTEM={};
function target(q){
 var p=q.problem,check=p&&p.parts&&p.parts.length===1?p.parts[0].check:null;
 if(!check||check.type!=='graph-key'||!Array.isArray(check.eqs)||check.eqs.length!==2||!G.MKLINE)return null;
 var eqs=check.eqs.map(eq=>G.MKLINE.target({problem:{prompt:'Graph the equation',parts:[{answer:eq}]}}));
 return eqs.every(Boolean)?eqs:null;
}
API.target=target;
function read(q){try{if(!(q.response||'').startsWith('system:'))return [[],[]];var a=JSON.parse(q.response.slice(7));return Array.isArray(a)&&a.length===2?a:[[],[]];}catch(e){return [[],[]];}}
function graphic(q){
 var all=read(q),s='<svg viewBox="0 0 340 340" class="pt-line-svg" role="img" aria-label="Tap two points for each of two lines">';
 for(var k=-10;k<=10;k++){var n=170+k*15;s+='<path d="M'+n+' 20V320 M20 '+n+'H320" stroke="#dbe5ee"/>';}
 s+='<path d="M170 20V320 M20 170H320" stroke="#647d91" stroke-width="2"/>';
 all.forEach(function(points,j){
 if(points.length===2){var p=points[0],r=points[1],dx=r[0]-p[0],dy=r[1]-p[1],x1=-10,x2=10,y1=dx? p[1]+(x1-p[0])*dy/dx:-10,y2=dx? p[1]+(x2-p[0])*dy/dx:10;if(dx===0)x1=x2=p[0];
 s+='<line x1="'+(170+15*x1)+'" y1="'+(170-15*y1)+'" x2="'+(170+15*x2)+'" y2="'+(170-15*y2)+'" stroke="'+(j?'#d05a27':'#245eab')+'" stroke-width="3"/>';}
 points.forEach(p=>s+='<circle cx="'+(170+15*p[0])+'" cy="'+(170-15*p[1])+'" r="6" fill="'+(j?'#d05a27':'#245eab')+'" stroke="white" stroke-width="2"/>');
 });return s+'</svg>';
}
API.render=function(q,i){var a=read(q),active=a[0].length<2?0:1;return '<div class="pt-system-editor" data-system="'+i+'"><strong>Graph both equations using two points per line</strong><p class="pt-muted">Blue: first equation. Orange: second equation. Tap grid intersections. Use Undo or Restart to correct points.</p>'+graphic(q)+'<p>First line: '+a[0].length+'/2 points · Second line: '+a[1].length+'/2 points</p><div class="pt-actions"><button type="button" data-undo-system class="pt-secondary">Undo point</button><button type="button" data-clear-system class="pt-secondary">Restart graph</button></div></div>';};
function same(t,p){if(p.length!==2||p[0][0]===p[1][0]&&p[0][1]===p[1][1])return false;var a=p[0][1]-p[1][1],b=p[1][0]-p[0][0],c=-a*p[0][0]-b*p[0][1];return Math.abs(a*t.b-b*t.a)<1e-7&&Math.abs(a*t.c-c*t.a)<1e-7&&Math.abs(b*t.c-c*t.b)<1e-7;}
API.grade=function(q){var t=target(q),a=read(q);return {status:t&&((same(t[0],a[0])&&same(t[1],a[1]))||(same(t[0],a[1])&&same(t[1],a[0])))?'correct':'incorrect'};};
API.bind=function(root,state,save){root.querySelectorAll('[data-system]').forEach(function(box){var i=+box.dataset.system,q=state.questions[i];function update(a){q.response='system:'+JSON.stringify(a);save();box.outerHTML=API.render(q,i);API.bind(root,state,save);}
 box.querySelector('svg').onclick=function(e){var a=read(q),j=a[0].length<2?0:1;if(a[1].length===2)return;var r=this.getBoundingClientRect(),x=Math.round(((e.clientX-r.left)/r.width*340-170)/15),y=Math.round((170-(e.clientY-r.top)/r.height*340)/15);x=Math.max(-10,Math.min(10,x));y=Math.max(-10,Math.min(10,y));if(a[j].some(p=>p[0]===x&&p[1]===y))return;a[j].push([x,y]);update(a);};
 box.querySelector('[data-clear-system]').onclick=()=>update([[],[]]);box.querySelector('[data-undo-system]').onclick=()=>{var a=read(q),j=a[1].length?1:0;a[j].pop();update(a);};});};
})(window);