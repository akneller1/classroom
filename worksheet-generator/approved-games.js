(function(root){'use strict';
var doc=root.document,params=new URLSearchParams(root.location.search),courseId=params.get('course'),unitId=params.get('unit');
var el=function(id){return doc.getElementById(id)},course=root.LIBRARY.courses.find(function(c){return c.id===courseId}),unit=course&&course.units.find(function(u){return u.id===unitId});
if(!unit){el('agStatus').textContent='Choose a valid course and unit from Mr. K’s Classroom.';return;}
var names=root.MK_COURSE_CATALOG.getSkillRecords(courseId,unitId);
names.forEach(function(s){var o=doc.createElement('option');o.value=s.id;o.textContent=s.name;el('agSkill').appendChild(o)});
var bridge=root.MK_GRADE_LEGACY_BRIDGE,isLegacy=bridge&&bridge.isGrade(courseId),engine=null;
if(names.some(function(x){return x.id===params.get('skill')}))el('agSkill').value=params.get('skill');
var requestedGame=params.get('game');if(['tic-tac-toe','connect-4','picture-reveal'].indexOf(requestedGame)>=0)el('agGame').value=requestedGame;
var solo=params.get('student')==='1'||params.get('mode')==='solo',cpuTimer=null,generation=0;
var players=doc.createElement('select');players.id='agPlayers';players.setAttribute('aria-label','Players');[['teams','Two players'],['solo','Solo vs. computer']].forEach(function(o){var opt=doc.createElement('option');opt.value=o[0];opt.textContent=o[1];players.appendChild(opt);});players.value=solo?'solo':'teams';el('agGame').parentNode.appendChild(players);players.addEventListener('change',function(){solo=players.value==='solo';reset()});
var board=[],turn=1,pending=-1,question=null,items=[],cursor=0,finished=false,selectedAnswer=-1,feedback='',attempts=0,correctCount=0;
function text(node,value){node.textContent=String(value)}
function dimensions(){return el('agGame').value==='connect-4'?42:el('agGame').value==='picture-reveal'?16:9}
function game(){return el('agGame').value}
function outcome(){
 if(game()==='picture-reveal')return board.every(function(x){return x==='-'})?{type:'complete'}:null;
 var cols=game()==='connect-4'?7:3, rows=game()==='connect-4'?6:3, needed=cols===7?4:3;
 for(var i=0;i<board.length;i++){
  var y=Math.floor(i/cols),x=i%cols,p=board[i];if(p!==1&&p!==2)continue;
  for(var d of [[1,0],[0,1],[1,1],[1,-1]]){
   var count=0;for(var k=0;k<needed;k++){var xx=x+d[0]*k,yy=y+d[1]*k;if(xx>=0&&xx<cols&&yy>=0&&yy<rows&&board[yy*cols+xx]===p)count++;}
   if(count===needed)return {type:'win',player:p};
  }
 }
 return board.every(Boolean)?{type:'draw'}:null;
}
function render(){text(el('agScore'),'Questions: '+attempts+' · Correct: '+correctCount);var grid=el('agGrid');grid.replaceChildren();grid.dataset.game=game();board.forEach(function(p,i){var b=doc.createElement('button');b.type='button';b.className='ag-cell';b.dataset.owner=p===1?'1':p===2?'2':p==='-'?'revealed':'';b.textContent=p===1?'X':p===2?'O':p==='-'?'':(game()==='picture-reveal'?String(i+1):'');b.disabled=finished||!!p||pending>=0||!items.length||(solo&&turn===2);b.setAttribute('aria-label','Square '+(i+1)+(p?' claimed':''));b.addEventListener('click',function(){ask(i)});grid.appendChild(b)});
text(el('agTurn'),feedback || (finished?'Round complete. Start a new game.':game()==='picture-reveal'?'Reveal all tiles by answering correctly.':(solo?(turn===1?'You — choose a square':'The computer is thinking…'):'Player '+turn+' — choose a square')));}
var plotWidget=null,plotMisses=0;
function ask(i){if(finished||pending>=0||board[i]||(solo&&turn===2))return;var target=i;if(game()==='connect-4'){var col=i%7;target=-1;for(var row=5;row>=0;row--){if(!board[row*7+col]){target=row*7+col;break}}if(target<0)return;}
if(!items.length){text(el('agStatus'),'No compatible approved questions for this difficulty.');return;}
feedback='';pending=target;question=items[cursor++%items.length];selectedAnswer=-1;text(el('agPrompt'),question.prompt);var opts=el('agOptions');opts.replaceChildren();
plotWidget=null;plotMisses=0;if(question.diagram){var image=doc.createElement('img');image.src='../'+question.diagram.spec.src;image.alt=question.diagram.spec.alt;image.style.maxWidth='100%';opts.appendChild(image);}if(question.plot){var host=doc.createElement('div');opts.appendChild(host);plotWidget=root.MK_PLOT.create(host,question.plot,{onSubmit:function(){el('agReveal').click();}});}
question.options.forEach(function(o,n){var b=doc.createElement('button');b.type='button';text(b,String.fromCharCode(65+n)+'. '+o.text);b.addEventListener('click',function(){selectedAnswer=n;Array.from(opts.children).forEach(function(c,j){c.setAttribute('aria-pressed',String(j===n))})});opts.appendChild(b)});
el('agReveal').hidden=false;el('agSolution').hidden=true;el('agCorrect').hidden=true;el('agWrong').hidden=true;el('agQuestion').hidden=false;render();if(question.options.length)question.options.length&&opts.querySelector('button').focus();else el('agReveal').focus();}
function judge(correct){if(pending<0||!question)return;var answerShown=el('agSolution').hidden===false;if(!answerShown)return;
attempts++;if(correct)correctCount++;
if(correct)board[pending]=game()==='picture-reveal'?'-':turn;
feedback=correct?'Correct — square claimed.':'Incorrect — no square claimed.';
if(game()!=='picture-reveal')turn=turn===1?2:1;
pending=-1;question=null;el('agQuestion').hidden=true;var result=outcome();finished=!!result;if(result)feedback=result.type==='win'?'Player '+result.player+' wins!':result.type==='draw'?'Draw — no more moves.':'Picture revealed — all tiles cleared!';render();if(solo&&turn===2&&!finished&&game()!=='picture-reveal')computerTurn();}
function computerTurn(){var token=generation;cpuTimer=setTimeout(function(){if(token!==generation||finished||turn!==2)return;var ai=root.MKSOLOAI;if(!ai){feedback='Computer opponent could not load. Reload to try again.';render();return;}if(ai.answers('easy')){var move=game()==='connect-4'?ai.connectFourMove(Array.from({length:6},(_,r)=>board.slice(r*7,r*7+7)),2,1,'easy'):ai.ticTacToeMove(board,2,1,'easy');if(game()==='connect-4'){for(var r=5;r>=0;r--)if(!board[r*7+move]){board[r*7+move]=2;break;}}else if(move>=0)board[move]=2;feedback='The computer played its turn.';}else feedback='The computer missed its problem. Your turn.';var result=outcome();finished=!!result;if(result)feedback=result.type==='win'?'The computer wins!':'Draw — no more moves.';turn=1;render();},850);}
el('agReveal').addEventListener('click',function(){if(!question)return;if(question.plot){var result=root.MK_PLOT.check(question.plot,plotWidget.getResponse());if(!result.ok){plotMisses++;text(el('agSolution'),question.plot.feedback[result.code]||'Check your graph and try again.');el('agSolution').hidden=false;if(plotMisses>=2){var key=doc.createElement('img');key.src='../'+question.plot.answerKey.src;key.alt=question.plot.answerKey.alt;key.style.maxWidth='100%';el('agSolution').appendChild(key);el('agWrong').hidden=false;}return;}el('agSolution').hidden=false;judge(true);return;}var solution='Answer: '+(Array.isArray(question.answer)?question.answer.join(', '):question.answer)+'\n'+question.solutionSteps.join('\n');text(el('agSolution'),solution);el('agSolution').hidden=false;var auto=question.options.length>0&&selectedAnswer>=0;el('agCorrect').hidden=auto;el('agWrong').hidden=auto;el('agReveal').hidden=true;if(auto){var ok=question.options[selectedAnswer].correct===true;text(el('agSolution'),solution+'\n'+(ok?'Correct choice.':'Incorrect choice.'));judge(ok);}});
el('agCorrect').addEventListener('click',function(){judge(true)});el('agWrong').addEventListener('click',function(){judge(false)});
function reset(){generation++;clearTimeout(cpuTimer);var result=isLegacy?{items:bridge.prepare(engine,{courseId:courseId,unitId:unitId,level:el('agLevel').value,skillId:el('agSkill').value||''})}:root.MK_APPROVED_GAME_ITEMS.prepare({game:game(),courseId:courseId,unitId:unitId,level:el('agLevel').value,skillIds:el('agSkill').value?[el('agSkill').value]:undefined});if(isLegacy)result.ready=result.items.length>0;items=result.items;cursor=0;board=Array(dimensions()).fill(null);turn=1;pending=-1;finished=false;feedback='';attempts=0;correctCount=0;el('agQuestion').hidden=true;text(el('agStatus'),result.ready?course.name+' · '+unit.name+' · '+items.length+(isLegacy?' shared-generator questions':' approved question(s)'):'No compatible approved questions for these settings.');render();}
['agGame','agLevel','agSkill'].forEach(function(id){el(id).addEventListener('change',reset)});el('agReset').addEventListener('click',reset);
if(isLegacy){bridge.load().then(function(w){engine=w;el('agApp').hidden=false;reset()}).catch(function(e){text(el('agStatus'),'Unable to load shared questions: '+e.message)});return;}
root.MK_BANK_LOADER.loadFromSite(undefined,'../').then(function(){if(!root.MK_QUESTION_BANKS.available(courseId,unitId)){text(el('agStatus'),'No approved question bank is available for this unit.');return;}el('agApp').hidden=false;reset()}).catch(function(e){text(el('agStatus'),'Could not load approved questions: '+e.message)});
})(window);