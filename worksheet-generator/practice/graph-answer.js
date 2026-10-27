/* Graph responses for automatically checkable Algebra 1 drawings. */
(function(G){
'use strict';
var A=G.MKGRAPHANSWER={};
function line(q){return q.problem&&q.problem.parts&&q.problem.parts[0]&&q.problem.parts[0].answerFig;}
A.type=function(q){
 var p=q.problem||{},c=p.parts&&p.parts[0]&&p.parts[0].check||{},prompt=(p.prompt||'').toLowerCase();
 if(c.type==='graph-key'&&c.eqs&&c.eqs.length===2)return 'intersection';
 if(c.type==='graph-key'&&c.ineqs&&c.ineqs.length===1)return 'halfplane';
 if(c.type==='ineq'&&/graph|number line/.test(prompt)&&p.parts&&p.parts.length===1)return 'numberline';
 return null;
};
var esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
function svg(kind){
 var lines='';for(var n=-6;n<=6;n++){var p=(n+6)*24;lines+='<line x1="'+p+'" y1="0" x2="'+p+'" y2="288" stroke="#d5e1ec"/><line x1="0" y1="'+p+'" x2="288" y2="'+p+'" stroke="#d5e1ec"/>'; }
 lines+='<line x1="0" y1="144" x2="288" y2="144" stroke="#546b80" stroke-width="2"/><line x1="144" y1="0" x2="144" y2="288" stroke="#546b80" stroke-width="2"/>';
 return '<svg class="pt-draw-grid" role="img" aria-label="Interactive coordinate grid from negative six to positive six" viewBox="0 0 288 288">'+lines+'<g class="pt-draw-marks"></g><rect class="pt-draw-click" x="0" y="0" width="288" height="288" fill="transparent"/></svg>';
}
A.html=function(q,i){
 var t=A.type(q);if(!t)return '';
 if(t==='numberline')return '<div class="pt-graph-answer" data-graph="'+i+'"><strong>Interactive number line</strong><p>Enter the solved inequality below; the number line shows your solution, including open or closed endpoints.</p><div class="pt-line-visual" aria-label="Number line from negative ten to ten"></div><input class="pt-line-input" aria-label="Inequality for question '+(i+1)+'" placeholder="x > -3, -2 ≤ x ≤ 4, or x < -2 or x > 2" value="'+esc(q.response||'')+'"></div>';
 return '<div class="pt-graph-answer" data-graph="'+i+'"><strong>'+(t==='intersection'?'Plot the intersection point':'Graph the inequality boundary')+'</strong><p>'+(t==='intersection'?'Click the intersection of the two lines.':'Click two points on the boundary line, then choose dashed/solid and the shading direction.')+'</p>'+svg(t)+(t==='halfplane'?'<div class="pt-draw-options"><label>Boundary<select class="pt-boundary"><option value="solid">Solid</option><option value="dashed">Dashed</option></select></label><label>Shade<select class="pt-shade"><option value="above">Above</option><option value="below">Below</option></select></label><button type="button" class="pt-draw-clear">Clear points</button></div>':'')+'<p class="pt-graph-coords">Select point(s) on the grid.</p></div>';
};
function fraction(n){return Math.round(n*1000)/1000;}
A.bind=function(holder,q,change){
 var t=A.type(q),wrap=holder.querySelector('[data-graph]');if(!t||!wrap)return;
 if(t==='numberline'){
  var inp=wrap.querySelector('.pt-line-input'),visual=wrap.querySelector('.pt-line-visual');
  function paint(){var v=inp.value.trim();change(v);var s='<div class="pt-numberline"><div class="pt-nl-axis"></div>';for(var n=-10;n<=10;n+=2)s+='<span style="left:'+((n+10)*5)+'%">'+n+'</span>';
  // draw a simple directional ray for solved one-sided inequalities
  var match=/^x\s*(<=|>=|<|>|≤|≥)\s*(-?\d+(?:\.\d+)?)$/.exec(v);
  if(match){var x=+match[2],left=match[1][0]==='< '||match[1][0]==='<';left=match[1].charAt(0)==='< '||match[1].charAt(0)==='<';var pos=Math.max(0,Math.min(100,(x+10)*5));s+='<i class="pt-nl-ray" style="left:'+(left?0:pos)+'%;width:'+(left?pos:100-pos)+'%"></i><i class="pt-nl-dot '+((match[1].length>1||match[1]==='≤'||match[1]==='≥')?'closed':'open')+'" style="left:'+pos+'%"></i>';}
  visual.innerHTML=s+'</div>';
  }inp.oninput=paint;paint();return;
 }
 var selected=q.graphResponse&&q.graphResponse.points||[];
 function update(){var mark=wrap.querySelector('.pt-draw-marks'),render='';selected.forEach(function(p){render+='<circle cx="'+((p[0]+6)*24)+'" cy="'+((6-p[1])*24)+'" r="6" fill="#1674cd" stroke="#fff" stroke-width="2"/>';});if(selected.length===2)render='<line x1="'+((selected[0][0]+6)*24)+'" y1="'+((6-selected[0][1])*24)+'" x2="'+((selected[1][0]+6)*24)+'" y2="'+((6-selected[1][1])*24)+'" stroke="#1674cd" stroke-width="3"/>'+render;mark.innerHTML=render;wrap.querySelector('.pt-graph-coords').textContent=selected.map(p=>'('+p.join(', ')+')').join(' to ')||'Select point(s) on the grid.';}
 var boundary=wrap.querySelector('.pt-boundary'),shade=wrap.querySelector('.pt-shade');
 if(boundary)boundary.value=q.graphResponse&&q.graphResponse.boundary||'solid';
 if(shade)shade.value=q.graphResponse&&q.graphResponse.shade||'above';
 function commit(){q.graphResponse={points:selected.slice(),boundary:boundary&&boundary.value,shade:shade&&shade.value};change(JSON.stringify(q.graphResponse));update();}
 wrap.querySelector('.pt-draw-click').addEventListener('click',function(e){var box=this.getBoundingClientRect(),x=Math.round((e.clientX-box.left)/box.width*12-6),y=Math.round(6-(e.clientY-box.top)/box.height*12);selected=t==='intersection'?[[x,y]]:selected.length>=2?[[x,y]]:selected.concat([[x,y]]);commit();});
 if(boundary)boundary.onchange=commit;if(shade)shade.onchange=commit;var clear=wrap.querySelector('.pt-draw-clear');if(clear)clear.onclick=function(){selected=[];commit();};update();
};
A.grade=function(q){
 var t=A.type(q);if(!t)return null;
 if(t==='numberline')return G.MKPRACTICE.grade(q.problem,q.response||'');
 var answer=line(q),got=q.graphResponse;
 if(!got||!got.points||!got.points.length)return {status:'incorrect'};
 if(t==='intersection'){var p=answer&&answer.points&&answer.points[0];return {status:p&&got.points.length===1&&got.points[0][0]===p.x&&got.points[0][1]===p.y?'correct':'incorrect'};}
 if(t==='halfplane'){
  var hp=answer&&answer.halfplanes&&answer.halfplanes[0],g=got.points;
  // Only accept when the answer geometry can be independently reconstructed.
  if(!hp||g.length!==2||g[0][0]===g[1][0])return {status:'self'};
  var m=(g[1][1]-g[0][1])/(g[1][0]-g[0][0]),b=g[0][1]-m*g[0][0];
  var a=hp.a,c=hp.b;if(!a||!c||a[0]===c[0])return {status:'self'};
  var actual=(c[1]-a[1])/(c[0]-a[0]),intercept=a[1]-actual*a[0];
  return {status:Math.abs(m-actual)<1e-8&&Math.abs(b-intercept)<1e-8&&got.boundary===(hp.dashed?'dashed':'solid')&&got.shade===(hp.side[1]>intercept?'above':'below')?'correct':'incorrect'};
 }
 return {status:'self'};
};
})(window);