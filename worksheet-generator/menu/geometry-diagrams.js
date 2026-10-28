/* Shared Geometry SVG renderer. Data-only specifications; no DOM dependencies.
   Figures are explicitly not to scale when their labels represent algebraic unknowns. */
(function(G){
'use strict';
var NS=G.MKMENU=(G.MKMENU||{}), D=NS.geoDiagram={};
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function positive(n){return Number.isFinite(n)&&n>0}
function svg(inner,description){return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 430 155" width="4.1in" style="max-width:100%;height:auto" role="img" aria-label="'+esc(description)+'"><rect width="430" height="155" fill="white"/>'+inner+'</svg>'}
function tx(x,y,s,anchor){return '<text x="'+x+'" y="'+y+'" text-anchor="'+(anchor||'middle')+'" font-family="Arial,sans-serif" font-size="15" fill="#111">'+esc(s)+'</text>'}

/* Horizontal number line: points placed in proportion to their values, named above and valued below.
   spec: {kind:'geo-numline', pts:[{n:'A',v:0,l:'0'}...], brackets:[{from:'B',to:'C',l:'84'}], ticks:[['A','M'],['M','B']]}
   Unknown coordinates are labelled with a letter; only the labels given are printed, so the picture never states an answer. */
function numline(spec){
 var pts=spec.pts||[];if(pts.length<2||pts.length>4)return '';
 var lo=Math.min.apply(null,pts.map(function(p){return p.v})),hi=Math.max.apply(null,pts.map(function(p){return p.v}));if(lo===hi)return '';
 var X=function(v){return 48+(v-lo)/(hi-lo)*334},Y=88,h='',by={};
 pts.forEach(function(p){by[p.n]=p});
 h+='<path d="M24 '+Y+' H406" stroke="#111" stroke-width="2.5" fill="none"/><path d="M406 '+Y+' l-9 -5 M406 '+Y+' l-9 5" stroke="#111" stroke-width="2" fill="none"/>';
 (spec.ticks||[]).forEach(function(t){var p=by[t[0]],q=by[t[1]];if(!p||!q)return;var mx=(X(p.v)+X(q.v))/2;h+='<path d="M'+(mx-3)+' '+(Y+9)+' L'+(mx+3)+' '+(Y-9)+'" stroke="#111" stroke-width="2"/>';});
 (spec.brackets||[]).forEach(function(b){var p=by[b.from],q=by[b.to];if(!p||!q)return;var x1=X(p.v),x2=X(q.v),yb=36;
  h+='<path d="M'+x1+' '+(yb+6)+' V'+yb+' H'+x2+' V'+(yb+6)+'" stroke="#111" stroke-width="1.4" fill="none"/>'+tx((x1+x2)/2,yb-7,b.l);});
 pts.forEach(function(p){h+='<circle cx="'+X(p.v).toFixed(1)+'" cy="'+Y+'" r="4.5" fill="#111"/>'+tx(X(p.v),Y-17,p.n)+tx(X(p.v),Y+26,p.l);});
 return '<div class="mm-geometry-figure" style="break-inside:avoid">'+svg(h,spec.description||'Number line with labelled points')+'<div style="font-size:10px;color:#555">Schematic, not to scale.</div></div>';
}
/* Triangle ABC with midsegment DE, median AM and centroid G; the labels object says what is printed on each segment. */
function triChain(spec){
 var A=[190,24],B=[70,134],C=[365,134],L=spec.lab||{},mid=function(p,q){return [(p[0]+q[0])/2,(p[1]+q[1])/2]},Dd=mid(A,B),E=mid(A,C),M=mid(B,C),G=[(A[0]+B[0]+C[0])/3,(A[1]+B[1]+C[1])/3],h='';
 var ln=function(p,q,w){return '<path d="M'+p[0].toFixed(1)+' '+p[1].toFixed(1)+' L'+q[0].toFixed(1)+' '+q[1].toFixed(1)+'" stroke="#111" stroke-width="'+(w||2.5)+'" fill="none"/>'},dt=function(p){return '<circle cx="'+p[0].toFixed(1)+'" cy="'+p[1].toFixed(1)+'" r="3.5" fill="#111"/>'};
 h+=ln(A,B)+ln(B,C)+ln(C,A)+ln(Dd,E,2.2)+ln(A,M,2.2);
 [A,Dd,E,M,G].forEach(function(p){h+=dt(p)});
 h+=tx(A[0],A[1]-9,'A')+tx(B[0]-12,B[1]+5,'B')+tx(C[0]+12,C[1]+5,'C')+tx(Dd[0]-13,Dd[1]-2,'D')+tx(E[0]+13,E[1]-2,'E')+tx(M[0]+2,M[1]+17,'M')+tx(G[0]-11,G[1]+14,'G');
 if(L.DE)h+=tx(Dd[0]+(E[0]-Dd[0])*0.25+4,Dd[1]-9,L.DE);
  if(L.AG)h+=tx(A[0]+(G[0]-A[0])*0.5+9,A[1]+(G[1]-A[1])*0.5+2,L.AG,'start');
 if(L.GM)h+=tx(G[0]+(M[0]-G[0])*0.5+9,G[1]+(M[1]-G[1])*0.5+2,L.GM,'start');
 if(L.BC)h+=tx((B[0]+M[0])/2,B[1]+19,L.BC);
 return '<div class="mm-geometry-figure" style="break-inside:avoid">'+svg(h,spec.description||'Triangle with a midsegment, a median and the centroid')+'<div style="font-size:10px;color:#555">'+(spec.given?spec.given+'. ':'')+'Schematic, not to scale. D, E and M are midpoints; G is the centroid.</div></div>';
}

/* Two congruent triangles ABC and DEF drawn side by side. Only the labels the problem gives are printed.
   spec: {kind:'geo-cong-pair', sides:{AB:'x+3',DE:'25'}, angles:{B:'(2x+1)°',E:'51°'}, arcs:{A:1,D:1,B:2,E:2}, note:'...'} */
function congPair(spec){
 var base=[[60,128],[200,128],[125,26]],off=200,pts={},nm=['A','B','C','D','E','F'];
 base.forEach(function(p,i){pts[nm[i]]=p;pts[nm[i+3]]=[p[0]+off,p[1]];});
 var halo=function(x,y,t,an){return tx(x,y,t,an).replace('<text ','<text stroke="#fff" stroke-width="4" paint-order="stroke" ');};
 var h='',tris=[['A','B','C'],['D','E','F']],S=spec.sides||{},An=spec.angles||{},Ar=spec.arcs||{};
 tris.forEach(function(t){var P=t.map(function(k){return pts[k]});h+='<path d="M'+P.map(function(p){return p[0]+' '+p[1]}).join(' L')+' Z" fill="none" stroke="#111" stroke-width="2.5" stroke-linejoin="round"/>';
  var cx=(P[0][0]+P[1][0]+P[2][0])/3,cy=(P[0][1]+P[1][1]+P[2][1])/3;
  t.forEach(function(k,i){var p=pts[k],q=pts[t[(i+1)%3]],m=[(p[0]+q[0])/2,(p[1]+q[1])/2],key=k+t[(i+1)%3],lab=S[key]||S[t[(i+1)%3]+k];
   if(lab){var nx=m[0]-cx,ny=m[1]-cy,d=Math.hypot(nx,ny)||1;h+=halo(m[0]+nx/d*(14+lab.length*2.2),m[1]+ny/d*(10+4)+4,lab);}});
  t.forEach(function(k,i){var p=pts[k],a=pts[t[(i+2)%3]],b=pts[t[(i+1)%3]],u=[a[0]-p[0],a[1]-p[1]],v=[b[0]-p[0],b[1]-p[1]],lu=Math.hypot(u[0],u[1]),lv=Math.hypot(v[0],v[1]);u=[u[0]/lu,u[1]/lu];v=[v[0]/lv,v[1]/lv];
   var n=Ar[k]||0,j;for(j=0;j<n;j++){var r=15+j*4,p1=[p[0]+u[0]*r,p[1]+u[1]*r],p2=[p[0]+v[0]*r,p[1]+v[1]*r],cr=u[0]*v[1]-u[1]*v[0];h+='<path d="M'+p1[0].toFixed(1)+' '+p1[1].toFixed(1)+' A'+r+' '+r+' 0 0 '+(cr>0?1:0)+' '+p2[0].toFixed(1)+' '+p2[1].toFixed(1)+'" fill="none" stroke="#111" stroke-width="1.5"/>';}
   var al=An[k];if(al){var bx=u[0]+v[0],by=u[1]+v[1],bl=Math.hypot(bx,by)||1;var ux=bx/bl;h+=halo(p[0]+ux*(ux<-0.3||ux>0.3?22:33),p[1]+by/bl*33+4,al,ux<-0.3?'end':ux>0.3?'start':'middle');}
   var ox=p[0]-cx,oy=p[1]-cy,od=Math.hypot(ox,oy)||1;h+=tx(p[0]+ox/od*15,p[1]+oy/od*15+5,k);});});
 return '<div class="mm-geometry-figure" style="break-inside:avoid">'+svg(h,spec.description||'Two congruent triangles ABC and DEF')+'<div style="font-size:10px;color:#555">'+(spec.note?spec.note+' ':'')+'Schematic, not to scale.</div></div>';
}
D.render=function(spec){
 if(!spec||!['geo-segment','geo-angle','geo-angle-pair','geo-triangle-pair','geo-proof','geo-triangle-landmark','geo-similar-pair','geo-right-triangle','geo-numline','geo-tri-chain','geo-cong-pair'].includes(spec.kind))return '';
 var h='',a=spec.labels||[],m=spec.measures||[];
 if(spec.kind==='geo-numline')return numline(spec);
 if(spec.kind==='geo-tri-chain')return triChain(spec);
 if(spec.kind==='geo-cong-pair')return congPair(spec);
 if(spec.kind==='geo-right-triangle'){
   if(!['hyp','leg','sin','cos','tan','45','30','elevation'].includes(spec.case))return '';
   var q=spec.case, elevation=q==='elevation';
   var a=elevation?[105,125]:[100,125],b=elevation?[345,125]:[100,30],c=elevation?[345,30]:[345,125];
   function ln(p,v){return '<path d="M'+p[0]+' '+p[1]+' L'+v[0]+' '+v[1]+'" stroke="#111" stroke-width="2.5" fill="none"/>';}
   var out=ln(a,b)+ln(b,c)+ln(c,a);
   if(elevation){
     out+='<path d="M333 125 V113 H345" stroke="#111" stroke-width="1.5" fill="none"/>'+
       tx(355,77,'height')+tx(225,145,'horizontal distance')+tx(140,116,'θ');
   }else{
     out+='<path d="M100 113 H112 V125" stroke="#111" stroke-width="1.5" fill="none"/>'+
       tx(87,77,q==='leg'?'leg':'opposite')+
       tx(226,145,q==='hyp'?'leg':'adjacent')+
       tx(240,69,q==='hyp'?'x':'hypotenuse');
     if(['sin','cos','tan'].includes(q))out+=tx(332,116,'θ');
     if(q==='45')out+=tx(335,116,'45°')+tx(118,43,'45°');
     if(q==='30')out+=tx(335,116,'30°')+tx(119,43,'60°');
   }
   return '<div class="mm-geometry-figure" style="break-inside:avoid">'+
     svg(out,elevation?'Right-triangle angle of elevation diagram':'Right triangle showing '+q+' relationship')+
     '<div style="font-size:10px;color:#555">Schematic, not to scale. Use the numerical measurements stated in the question.</div></div>';
 }
 if(spec.kind==='geo-similar-pair'){
   if(!['aa','sas','sss','sides','parallel'].includes(spec.case))return '';
   if(spec.case==='parallel'){
     var figure='<path d="M215 17 L70 131 L360 131 Z M166.67 55 L263.33 55" stroke="#111" stroke-width="2.5" fill="none"/>'+
       tx(215,14,'A')+tx(58,145,'B')+tx(372,145,'C')+
       tx(151,56,'D')+tx(278,56,'E')+
       tx(215,49,'DE')+tx(215,148,'BC');
     return '<div class="mm-geometry-figure" style="break-inside:avoid">'+
       svg(figure,'Triangle ABC with D on AB, E on AC, and DE parallel to BC')+
       '<div style="font-size:10px;color:#555">DE is parallel to BC. Schematic, not to scale; use the given measurements.</div></div>';
   }
   var left=[[70,26],[45,128],[186,128]],right=[[270,22],[242,130],[390,130]];
   function edge(p,q){return '<path d="M'+p[0]+' '+p[1]+' L'+q[0]+' '+q[1]+'" stroke="#111" stroke-width="2.5" fill="none"/>';}
   function triangle(t){return edge(t[0],t[1])+edge(t[1],t[2])+edge(t[2],t[0]);}
   var out=triangle(left)+triangle(right);
   out+=tx(70,16,'A')+tx(35,145,'B')+tx(194,145,'C')+
     tx(270,14,'D')+tx(232,147,'E')+tx(398,147,'F');
   // Angular arc indicators are used only for AA, never equal-side tick marks
   // (similar sides are proportional, not necessarily congruent).
   if(spec.case==='aa'){
     out+='<path d="M66 45 Q73 51 81 44 M266 43 Q273 49 281 42" fill="none" stroke="#111" stroke-width="1.5"/>';
     out+='<path d="M48 109 Q60 113 69 124 M245 111 Q257 116 268 126" fill="none" stroke="#111" stroke-width="1.5"/>';
   }
   if(spec.case==='sas'){
     out+='<path d="M66 45 Q73 51 81 44 M266 43 Q273 49 281 42" fill="none" stroke="#111" stroke-width="1.5"/>';
   }
   return '<div class="mm-geometry-figure" style="break-inside:avoid">'+
     svg(out,'Corresponding triangles ABC and DEF; similarity '+spec.case)+
     '<div style="font-size:10px;color:#555">Schematic, not to scale. Use the measurements and correspondence stated in the question.</div></div>';
 }
 if(spec.kind==='geo-triangle-landmark'){
   var type=spec.case;
   if(!['midsegment','centroid','altitude','bisector'].includes(type))return '';
   function ln(x1,y1,x2,y2){return '<path d="M'+x1+' '+y1+' L'+x2+' '+y2+'" stroke="#111" stroke-width="2.5" fill="none"/>';}
   function dash(x1,y1,x2,y2){return '<path d="M'+x1+' '+y1+' L'+x2+' '+y2+'" stroke="#111" stroke-width="2" stroke-dasharray="6 5" fill="none"/>';}
   var h2='';
   if(type==='midsegment'){
     // A(215,20), B(65,130), C(365,130); D/E are actual midpoints.
     h2=ln(215,20,65,130)+ln(215,20,365,130)+ln(65,130,365,130)+ln(140,75,290,75)+
       tx(215,14,'A')+tx(53,143,'B')+tx(377,143,'C')+tx(127,72,'D')+tx(303,72,'E')+
       tx(215,69,'DE')+tx(215,148,'BC');
   }else if(type==='centroid'){
     // G divides AM in the ratio AG:GM=2:1.
     h2=ln(215,20,65,130)+ln(215,20,365,130)+ln(65,130,365,130)+ln(215,20,215,130)+
       '<circle cx="215" cy="93.33" r="4" fill="#111"/>'+
       tx(215,14,'A')+tx(53,143,'B')+tx(377,143,'C')+tx(228,96,'G')+tx(215,147,'M');
   }else if(type==='altitude'){
     // D lies outside BC; this is an obtuse-triangle altitude.
     h2=ln(110,20,185,130)+ln(110,20,365,130)+ln(185,130,365,130)+
       dash(110,20,110,130)+dash(110,130,185,130)+
       '<path d="M110 118 H122 V130" stroke="#111" stroke-width="1.6" fill="none"/>'+
       tx(110,14,'A')+tx(183,146,'B')+tx(372,146,'C')+tx(97,145,'D')+tx(93,77,'AD');
   }else{
     // P is on the perpendicular bisector of AB; PA=PB.
     h2=ln(115,35,115,125)+ln(115,80,305,80)+ln(305,80,115,35)+ln(305,80,115,125)+
       '<path d="M115 68 H127 V80" stroke="#111" stroke-width="1.6" fill="none"/>'+
       tx(102,31,'A')+tx(102,142,'B')+tx(116,98,'M')+tx(318,84,'P');
   }
   return '<div class="mm-geometry-figure" style="break-inside:avoid">'+
     svg(h2,'Triangle geometry diagram: '+type)+
     '<div style="font-size:10px;color:#555">Schematic, not to scale. Use the stated geometric givens.</div></div>';
 }
 if(spec.kind==='geo-proof'){
   if(spec.case!=='shared'&&spec.case!=='vertical')return '';
   function segment(p,q){return '<path d="M'+p[0]+' '+p[1]+' L'+q[0]+' '+q[1]+'" stroke="#111" stroke-width="2.5" fill="none"/>';}
   function ticks(p,q,n){var mx=(p[0]+q[0])/2,my=(p[1]+q[1])/2,dx=q[0]-p[0],dy=q[1]-p[1],ll=Math.hypot(dx,dy),nx=-dy/ll,ny=dx/ll,h='';
     for(var j=0;j<n;j++){var t=j-(n-1)/2,xx=mx+t*6*dx/ll,yy=my+t*6*dy/ll;h+='<path d="M'+(xx-5*nx)+' '+(yy-5*ny)+' L'+(xx+5*nx)+' '+(yy+5*ny)+'" stroke="#111" stroke-width="1.7"/>';}return h;}
   if(spec.case==='shared'){
     var A=[215,23],B=[215,132],C=[75,80],D=[355,80];
     h=segment(A,B)+segment(A,C)+segment(B,C)+segment(A,D)+segment(B,D)+
       ticks(A,C,1)+ticks(A,D,1)+ticks(B,C,2)+ticks(B,D,2)+
       tx(215,15,'A')+tx(215,150,'B')+tx(59,84,'C')+tx(372,84,'D');
   }else{
     var A=[65,22],O=[215,78],C=[365,134],B=[65,134],D=[365,22];
     h=segment(A,C)+segment(B,D)+ticks(A,O,1)+ticks(O,C,1)+ticks(B,O,2)+ticks(O,D,2)+
       tx(51,20,'A')+tx(51,149,'B')+tx(379,149,'C')+tx(379,20,'D')+tx(215,69,'O');
   }
   return '<div class="mm-geometry-figure" style="break-inside:avoid">'+svg(h,spec.case==='shared'?'Two triangles ABC and ABD share side AB, with AC equal AD and BC equal BD':'Intersecting lines AC and BD, with AO equal CO and BO equal DO')+'<div style="font-size:10px;color:#555">Given side equalities are marked; schematic not to scale.</div></div>';
 }
 if(spec.kind==='geo-triangle-pair'){
   if(!['sss','sas','asa','aas','hl','ssa','aaa'].includes(spec.criterion))return '';
   var right=spec.criterion==='hl';
   var A=[65,30],B=right?[65,122]:[48,122],C=[187,122];
   var D=[253,30],E=right?[253,122]:[236,122],F=[375,122];
   function line(p,q){return '<path d="M'+p[0]+' '+p[1]+' L'+q[0]+' '+q[1]+'" stroke="#111" stroke-width="2.5" fill="none"/>';}
   function mark(p,q,n){var mx=(p[0]+q[0])/2,my=(p[1]+q[1])/2,dx=q[0]-p[0],dy=q[1]-p[1],len=Math.hypot(dx,dy),nx=-dy/len,ny=dx/len,out='';
     for(var j=0;j<n;j++){var t=j-(n-1)/2,xx=mx+t*6*dx/len,yy=my+t*6*dy/len;out+='<path d="M'+(xx-6*nx)+' '+(yy-6*ny)+' L'+(xx+6*nx)+' '+(yy+6*ny)+'" stroke="#111" stroke-width="1.7"/>';}return out;}
   h=line(A,B)+line(B,C)+line(C,A)+line(D,E)+line(E,F)+line(F,D);
   var k=spec.criterion;
   if(k==='sss'||k==='sas'||k==='hl')h+=mark(A,B,1)+mark(D,E,1);
   if(k==='sss'||k==='sas'||k==='hl')h+=mark(A,C,2)+mark(D,F,2);
   if(k==='sss')h+=mark(B,C,3)+mark(E,F,3);
   if(k==='aas')h+=mark(A,C,1)+mark(D,F,1);
   if(k==='ssa')h+=mark(A,B,1)+mark(D,E,1)+mark(B,C,2)+mark(E,F,2);
   if(k==='asa')h+=mark(A,B,1)+mark(D,E,1);
   function arc(p,q,v,rank){var ux=(p[0]-v[0])/Math.hypot(p[0]-v[0],p[1]-v[1]),uy=(p[1]-v[1])/Math.hypot(p[0]-v[0],p[1]-v[1]);var vx=(q[0]-v[0])/Math.hypot(q[0]-v[0],q[1]-v[1]),vy=(q[1]-v[1])/Math.hypot(q[0]-v[0],q[1]-v[1]);var rr=17+rank*5;return '<path d="M'+(v[0]+rr*ux)+' '+(v[1]+rr*uy)+' A'+rr+' '+rr+' 0 0 1 '+(v[0]+rr*vx)+' '+(v[1]+rr*vy)+'" fill="none" stroke="#111" stroke-width="1.5"/>';}
   if(['sas','asa','aas','ssa','aaa'].includes(k))h+=arc(B,C,A,0)+arc(E,F,D,0);
   if(['asa','aas','aaa'].includes(k))h+=arc(A,C,B,1)+arc(D,F,E,1);
   if(k==='aaa')h+=arc(A,B,C,2)+arc(D,E,F,2);
   if(right)h+='<path d="M65 110 H77 V122 M253 110 H265 V122" stroke="#111" fill="none" stroke-width="1.6"/>';
   h+=tx(65,20,'A')+tx(B[0]-12,139,'B')+tx(193,139,'C')+tx(253,20,'D')+tx(E[0]-12,139,'E')+tx(381,139,'F');
   return '<div class="mm-geometry-figure" style="break-inside:avoid">'+svg(h,'Two triangles ABC and DEF; the given congruence relationships are stated in the question')+'<div style="font-size:10px;color:#555">Schematic, not to scale. Matching marks indicate equal corresponding sides or angles.</div></div>';
 }
 if(spec.kind==='geo-segment'){
   if(a.length!==3||m.length!==3||!m.every(x=>typeof x==='string'&&x.length<50))return '';
   h='<path d="M54 76 H376" fill="none" stroke="#111" stroke-width="2.5"/>'+
     '<circle cx="54" cy="76" r="4" fill="#111"/><circle cx="198" cy="76" r="4" fill="#111"/><circle cx="376" cy="76" r="4" fill="#111"/>'+
     tx(54,105,a[0])+tx(198,105,a[1])+tx(376,105,a[2])+
     tx(125,59,m[0])+tx(287,59,m[1])+
     (/\d/.test(m[2])?'<path d="M54 118 V126 H376 V118 M215 126 V132" fill="none" stroke="#111" stroke-width="1.5"/>'+tx(215,148,m[2]):tx(215,139,m[2]));
 }else if(spec.kind==='geo-angle'){
   if(a.length!==3||m.length!==3)return '';
   /* Adjacent angles ABD and DBC inside the whole angle ABC. Wedge sizes follow the numbers when they are plain
      degrees (kept readable), each part has its own arc and label, and the whole angle has its own outer arc. */
   var V=[215,125],num=function(t){var q=/^(\d+)°$/.exec(String(t));return q?Number(q[1]):null;},T0=num(m[2]),P2=num(m[1]),
     Tv=T0===null?110:Math.max(70,Math.min(115,T0)),f=spec.equal?0.5:(T0!==null&&P2!==null&&T0>0)?(T0-P2)/T0:0.55,
     t1=Math.max(30,Math.min(Tv-30,f*Tv)),pt=function(ph,r){return [V[0]+r*Math.cos(ph*Math.PI/180),V[1]-r*Math.sin(ph*Math.PI/180)];},
     P=function(q){return q[0].toFixed(1)+' '+q[1].toFixed(1);},arcp=function(p1,p2,r){return '<path d="M'+P(pt(p1,r))+' A'+r+' '+r+' 0 0 1 '+P(pt(p2,r))+'" fill="none" stroke="#111" stroke-width="1.6"/>';},
     e1=180-t1,e2=180-Tv,rayEnd=pt(e1,spec.mid?98:98),cEnd=pt(e2,108),cLab=pt(e2,122),aEnd=pt(180,150),l1=pt(180-t1/2,62),l2=pt(180-t1-(Tv-t1)/2,62),lt=pt(180-Tv/2,114);
   h='<path d="M'+P(aEnd)+' L'+P(V)+' L'+P(cEnd)+' M'+P(V)+' L'+P(rayEnd)+'" fill="none" stroke="#111" stroke-width="2.5"/>'+
     arcp(180,e1,36)+arcp(e1,e2,44)+(spec.equal?arcp(180,e1,41)+arcp(e1,e2,49):'')+(m[2]===''?'':arcp(180,e2,86))+
     '<circle cx="'+V[0]+'" cy="'+V[1]+'" r="3.5" fill="#111"/>'+
     tx(aEnd[0]-14,aEnd[1]+5,a[0])+tx(V[0],V[1]+23,a[1])+tx(cLab[0],cLab[1]+5,a[2])+
     tx(l1[0],l1[1],m[0])+tx(l2[0],l2[1],m[1])+(m[2]===''?'':tx(lt[0],lt[1],m[2]))+(spec.mid?tx(pt(e1,112)[0],pt(e1,112)[1]+5,spec.mid):'');
 }else{
   if(m.length!==3)return '';
   var right=spec.relationship==='complement';
   h='<path d="M90 126 H355 M90 126 V25 M90 126 L'+(right?'278 36':'165 29')+'" fill="none" stroke="#111" stroke-width="2.5"/>'+
    tx(245,108,m[0])+tx(123,77,m[1])+tx(347,45,m[2]);
   if(right)h+='<path d="M90 111 H105 V126" fill="none" stroke="#111" stroke-width="1.5"/>';
 }
 return '<div class="mm-geometry-figure" style="break-inside:avoid">'+svg(h,spec.description||'Geometry schematic; not drawn to scale')+'<div style="font-size:10px;color:#555">Schematic, not to scale</div></div>';
};
D.validate=function(spec){
 if(!spec||!D.render(spec))return false;
 if(spec.kind==='geo-segment')return spec.labels.length===3&&spec.labels.every(x=>/^[A-Z]$/.test(x))&&spec.labels[0]!==spec.labels[1]&&spec.labels[1]!==spec.labels[2]&&spec.labels[0]!==spec.labels[2];
 return true;
};
var prior=NS.figHtml;
NS.figHtml=function(spec){return D.render(spec)||(prior?prior(spec):'')};
})(typeof window!=='undefined'?window:globalThis);
