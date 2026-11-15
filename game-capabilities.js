/* One source of truth for catalog player labels and student sharing. */
(function(G){
 'use strict';
 function capabilities(a){
  a=a||{};var path=String(a.path||''), title=String(a.title||''), u;
  try{u=new URL(path,G.location.href)}catch(e){return {solo:false,team:false}}
  var game=u.searchParams.get('game')||'', name=(game+' '+path+' '+title).toLowerCase();
  var board=/connect[- ]?(?:four|4)|four-in-a-row|inequality-four|tic[- ]tac[- ]toe/.test(name);
  var teams=/showdown|jeopardy|math-race|rocket-race|math-soccer|number-race|number-soccer|team[- ]race|soccer|relay/.test(name);
  // Team-only engines must take precedence over the generic Game type.
  if(teams)return {solo:false,team:true};
  if(board)return {solo:true,team:true};
  var types=Array.isArray(a.type)?a.type:[a.type||''];
  return {solo:types.some(function(t){return /^(game|study guide)$/i.test(t)})||/flashcard|cheat.sheet|study.guide/.test(name),team:false};
 }
 function canShare(a){if(!a||!a.path)return false;var types=Array.isArray(a.type)?a.type:[a.type||''];if(!types.some(function(t){return /^(game|study guide)$/i.test(t)})&&!/flashcard|cheat.sheet|study.guide/i.test(a.path+' '+a.title))return false;return capabilities(a).solo;}
 function studentUrl(url){var c=capabilities({path:url.href,type:'Game'});if(c.solo&&c.team)url.searchParams.set('mode','solo');return url;}
 G.MK_GAME_CAPABILITIES={get:capabilities,canShare:canShare,studentUrl:studentUrl};
})(window);
