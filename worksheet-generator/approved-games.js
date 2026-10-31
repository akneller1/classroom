(function(root){'use strict';
var doc=root.document,params=new URLSearchParams(root.location.search),courseId=params.get('course'),unitId=params.get('unit');
var el=function(id){return doc.getElementById(id)},course=root.LIBRARY.courses.find(function(c){return c.id===courseId}),unit=course&&course.units.find(function(u){return u.id===unitId});
if(!unit){el('agStatus').textContent='Choose a valid course and unit from Mr. K’s Classroom.';return;}
var names=root.MK_COURSE_CATALOG.getSkillRecords(courseId,unitId);
names.forEach(function(s){var o=doc.createElement('option');o.value=s.id;o.textContent=s.name;el('agSkill').appendChild(o)});
var board=[],turn=1,pending=-1,question=null,items=[],cursor=0,finished=false,selectedAnswer=-1;
function text(node,value){node.textContent=String(value)}
function dimensions(){return el('agGame').value==='connect-4'?42:el('agGame').value==='picture-reveal'?16:9}
function game(){return el('agGame').value}
function win(){if(game()==='picture-reveal')return board.every(function(x){return x!=='-'});var cols=game()==='connect-4'?7:3,rows=game()==='connect-4'?6:3;for(var i=0;i<board.length;i++){var y=Math.floor(i/cols),x=i%cols,p=board[i];if(!p)continue;for(var d of [[1,0],[0,1],[1,1],[1,-1]]){var count=0;for(var k=0;k<(cols===7?4:3);k++){var xx=x+d[0]*k,yy=y+d[1]*k;if(xx>=0&&xx<cols&&yy>=0&&yy<rows&&board[yy*cols+xx]===p)count++;}if(count===(cols===7?4:3))return true;}}return board.every(Boolean)}
function render(){var grid=el('agGrid');grid.replaceChildren();grid.dataset.game=game();board.forEach(function(p,i){var b=doc.createElement('button');b.type='button';b.className='ag-cell';b.dataset.owner=p===1?'1':p===2?'2':p==='-'?'revealed':'';b.textContent=p===1?'X':p===2?'O':p==='-'?'✓':'';b.disabled=finished||!!p||pending>=0;b.setAttribute('aria-label','Square '+(i+1)+(p?' claimed':''));b.addEventListener('click',function(){ask(i)});grid.appendChild(b)});
text(el('agTurn'),finished?'Round complete. Start a new game.':game()==='picture-reveal'?'Reveal all tiles by answering correctly.':'Player '+turn+' — choose a square');}
function ask(i){if(finished||pending>=0||board[i])return;var target=i;if(game()==='connect-4'){var col=i%7;target=-1;for(var row=5;row>=0;row--){if(!board[row*7+col]){target=row*7+col;break}}if(target<0)return;}
if(!items.length){text(el('agStatus'),'No compatible approved questions for this difficulty.');return;}
pending=target;question=items[cursor++%items.length];selectedAnswer=-1;text(el('agPrompt'),question.prompt);var opts=el('agOptions');opts.replaceChildren();
question.options.forEach(function(o,n){var b=doc.createElement('button');b.type='button';text(b,String.fromCharCode(65+n)+'. '+o.text);b.addEventListener('click',function(){selectedAnswer=n;Array.from(opts.children).forEach(function(c,j){c.setAttribute('aria-pressed',String(j===n))})});opts.appendChild(b)});
el('agReveal').hidden=false;el('agSolution').hidden=true;el('agCorrect').hidden=true;el('agWrong').hidden=true;el('agQuestion').hidden=false;render();}
function judge(correct){if(pending<0||!question)return;var answerShown=el('agSolution').hidden===false;if(!answerShown)return;
if(correct)board[pending]=game()==='picture-reveal'?'-':turn;
if(game()!=='picture-reveal')turn=turn===1?2:1;
pending=-1;question=null;el('agQuestion').hidden=true;finished=win();render();}
el('agReveal').addEventListener('click',function(){if(!question)return;var solution='Answer: '+(Array.isArray(question.answer)?question.answer.join(', '):question.answer)+'\n'+question.solutionSteps.join('\n');text(el('agSolution'),solution);el('agSolution').hidden=false;el('agCorrect').hidden=false;el('agWrong').hidden=false;el('agReveal').hidden=true;});
el('agCorrect').addEventListener('click',function(){judge(true)});el('agWrong').addEventListener('click',function(){judge(false)});
function reset(){var result=root.MK_APPROVED_GAME_ITEMS.prepare({game:game(),courseId:courseId,unitId:unitId,level:el('agLevel').value,skillIds:el('agSkill').value?[el('agSkill').value]:undefined});items=result.items;cursor=0;board=Array(dimensions()).fill(null);turn=1;pending=-1;finished=false;el('agQuestion').hidden=true;text(el('agStatus'),result.ready?course.name+' · '+unit.name+' · '+items.length+' approved question(s)':'No compatible approved questions for these settings.');render();}
['agGame','agLevel','agSkill'].forEach(function(id){el(id).addEventListener('change',reset)});el('agReset').addEventListener('click',reset);
root.MK_BANK_LOADER.loadFromSite().then(function(){if(!root.MK_QUESTION_BANKS.available(courseId,unitId)){text(el('agStatus'),'No approved question bank is available for this unit.');return;}el('agApp').hidden=false;reset()}).catch(function(e){text(el('agStatus'),'Could not load approved questions: '+e.message)});
})(window);