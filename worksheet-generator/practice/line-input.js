/* Interactive line and half-plane answer tool. Limited to unambiguous linear forms. */
(function(G){
'use strict';
var API=G.MKLINE={};
function parseNumber(s){if(s===''||s==='+')return 1;if(s==='-')return -1;var n=Number(s);return Number.isFinite(n)?n:null;}
function target(q){
 var p=q.problem;if(!p||!p.parts||p.parts.length!==1)return null;
 if(!/\b(graph|plot|draw|shade)\b/i.test((p.prompt||'')+' '+(p.parts[0].prompt||'')))return null;
 var check=p.parts[0].check||{};
 var raw=(check.type==='graph-key'&&Array.isArray(check.ineqs)&&check.ineqs.length===1)?check.ineqs[0]:String(p.parts[0].answer||'');
 var s=raw.replace(/[⟨⟩]/g,'').replace(/\\(?:leq?|geq?)/g,a=>a.startsWith('\\l')?'<=':'>=')
 .replace(/≤/g,'<=').replace(/≥/g,'>=').replace(/\\left|\\right|\\,/g,'')
 .replace(/−/g,'-').replace(/\s+/g,'').replace(/\\frac\{(-?\d+)\}\{(\d+)\}/g,(_,n,d)=>String(Number(n)/Number(d)));
 var m=/^([xy])(<=|>=|=|<|>)(.+)$/.exec(s);if(!m)return null;
 var variable=m[1],op=m[2],rhs=m[3],a,b,c;
 if(variable==='x'){
   var k=Number(rhs);if(!Number.isFinite(k))return null;
   a=1;b=0;c=-k;
 }else{
   var direct=Number(rhs);
   if(rhs!==''&&Number.isFinite(direct)){a=0;b=1;c=-direct;}
   else{
     var linear=/^([+-]?(?:\d+(?:\.\d+)?|\.\d+)?)x([+-](?:\d+(?:\.\d+)?|\.\d+))?$/.exec(rhs);
     if(!linear)return null;
     var slope=parseNumber(linear[1]),intercept=Number(linear[2]||0);
     if(slope===null||!Number.isFinite(intercept))return null;
     a=-slope;b=1;c=-intercept;
   }
 }
 return {a:a,b:b,c:c,op:op};
}
API.target=target;
function read(q){try{var a=JSON.parse((q.response||'').replace(/^line:/,''));return q.response&&q.response.startsWith('line:')&&Array.isArray(a.points)?a:null;}catch(e){return null;}}
function saveResponse(q,d){q.response='line:'+JSON.stringify(d);}
function side(t,x,y){return t.a*x+t.b*y+t.c;}
function vertices(t,dir){
 var poly=[[-10,-10],[10,-10],[10,10],[-10,10]];
 // Clip half-plane against constructed line using two point coordinates.
 var p=t.points[0],r=t.points[1],a=-(r[1]-p[1]),b=r[0]-p[0],c=-a*p[0]-b*p[1];
 var norm=v=>dir*(a*v[0]+b*v[1]+c);
 var out=[];
 for(var i=0;i<poly.length;i++){var u=poly[i],v=poly[(i+1)%poly.length],fu=norm(u),fv=norm(v),insideU=fu>=-1e-8,insideV=fv>=-1e-8;
 if(insideU)out.push(u);
 if(insideU!==insideV){var f=fu/(fu-fv);out.push([u[0]+f*(v[0]-u[0]),u[1]+f*(v[1]-u[1])]);}
 }return out;
}
function svg(d){
 var h='<svg viewBox="0 0 340 340" class="pt-line-svg" role="img" aria-label="Interactive coordinate plane: click two points to draw a line">';
 for(var i=-10;i<=10;i++){var v=170+i*15;h+='<path d="M'+v+' 20V320 M20 '+v+'H320" stroke="#dce6ee" stroke-width="1"/>';}
 h+='<path d="M170 20V320 M20 170H320" stroke="#72899d" stroke-width="2"/>';
 function px(p){return (170+p[0]*15)+','+(170-p[1]*15);}
 if(d&&d.points.length===2){
 var p=d.points[0],q=d.points[1],dx=q[0]-p[0],dy=q[1]-p[1];
 if(d.shade===1||d.shade===-1){var v=vertices(d,d.shade);h+='<polygon points="'+v.map(px).join(' ')+'" fill="#96bfea" opacity=".5"/>';}
 var x1,x2,y1,y2;
 if(dx===0){x1=x2=p[0];y1=-10;y2=10;}else{x1=-10;x2=10;y1=p[1]+(-10-p[0])*dy/dx;y2=p[1]+(10-p[0])*dy/dx;}
 h+='<line x1="'+(170+x1*15)+'" y1="'+(170-y1*15)+'" x2="'+(170+x2*15)+'" y2="'+(170-y2*15)+'" stroke="#1558a0" stroke-width="3.5" '+(d.dashed?'stroke-dasharray="9 7"':'')+'/>';
 }
 (d&&d.points||[]).forEach(p=>h+='<circle cx="'+(170+p[0]*15)+'" cy="'+(170-p[1]*15)+'" r="6" fill="#e77529" stroke="white" stroke-width="2"/>');
 return h+'</svg>';
}
function content(q,i){var d=read(q)||{points:[],dashed:false,shade:null};var t=target(q);return '<div class="pt-line-editor" data-line="'+i+'"><strong>Draw the line by selecting two points.</strong><p class="pt-muted">Tap two grid intersections. To replace the line choose New line. For inequalities, tap a side to shade.</p>'+svg(d)+'<div class="pt-interval-row"><label>Boundary line<select data-boundary><option value="solid" '+(!d.dashed?'selected':'')+'>Solid</option><option value="dashed" '+(d.dashed?'selected':'')+'>Dashed</option></select></label><button type="button" data-clear-line class="pt-secondary">New line / erase</button>'+(t.op!=='='?'<button type="button" data-clear-shade class="pt-secondary">Clear shading</button>':'')+'</div><p class="pt-muted" data-line-message>'+d.points.length+'/2 points selected'+(t.op!=='='?(d.shade===null?' · choose a side to shade':' · shaded region selected'):'')+'</p></div>';}
API.render=content;
API.grade=function(q){var t=target(q),d=read(q);if(!t||!d||d.points.length!==2)return {status:'incorrect'};var p=d.points[0],r=d.points[1];if(p[0]===r[0]&&p[1]===r[1])return {status:'incorrect'};
 var a=p[1]-r[1],b=r[0]-p[0],c=-a*p[0]-b*p[1];
 var det=a*t.b-b*t.a;
 if(Math.abs(det)>1e-7||Math.abs(a*t.c-c*t.a)>1e-7||Math.abs(b*t.c-c*t.b)>1e-7)return {status:'incorrect'};
 if(t.op==='=')return {status:'correct'};
 if(d.dashed!==(t.op==='<'||t.op==='>')||d.shade===null)return {status:'incorrect'};
 var probe=d.shade===1?1:-1;
 // Determine whether the selected half-plane agrees with the inequality.
 var same=probe*(a*t.a+b*t.b)>0;
 var desired=t.op==='>'||t.op==='>='?1:-1;
 return {status:(same?1:-1)===desired?'correct':'incorrect'};
};
API.bind=function(root,state,save){root.querySelectorAll('[data-line]').forEach(function(box){
 var q=state.questions[+box.dataset.line],t=target(q);
 function refresh(d){saveResponse(q,d);save();box.innerHTML=content(q,+box.dataset.line).replace(/^<div[^>]*>/,'').replace(/<\/div>$/,'');API.bind(root,state,save);}
 var d=read(q)||{points:[],dashed:false,shade:null};
 var board=box.querySelector('svg');
 board.onclick=function(ev){var b=board.getBoundingClientRect(),x=Math.round(((ev.clientX-b.left)/b.width*340-170)/15),y=Math.round((170-(ev.clientY-b.top)/b.height*340)/15);x=Math.max(-10,Math.min(10,x));y=Math.max(-10,Math.min(10,y));
 if(d.points.length<2){if(d.points.length===1&&d.points[0][0]===x&&d.points[0][1]===y)return;d.points.push([x,y]);}
 else if(t.op!=='='){var p=d.points[0],r=d.points[1],f=(r[0]-p[0])*(y-p[1])-(r[1]-p[1])*(x-p[0]);if(Math.abs(f)>0.01)d.shade=f>0?1:-1;}
 refresh(d);
 };
 box.querySelector('[data-boundary]').onchange=e=>{d.dashed=e.target.value==='dashed';refresh(d);};
 box.querySelector('[data-clear-line]').onclick=()=>refresh({points:[],dashed:false,shade:null});
 var sh=box.querySelector('[data-clear-shade]');if(sh)sh.onclick=()=>{d.shade=null;refresh(d);};
 });};
})(window);