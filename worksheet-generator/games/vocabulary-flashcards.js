/* Display the same vocabulary entries used by the printable builder; no new questions or definitions. */
(function(G){
 'use strict';
 G.MK_VOCAB_FLASHCARDS={build:function(unitId){
  if(!/^prealgebra-/.test(unitId))return [];
  return String((G.MKVOCAB_BANKS||{})[unitId]||'').split(';').filter(Boolean).map(function(row,i){
   var fields=row.split('|'),term=fields[0],definition=fields[1],example=fields[2];
   return {id:'vocabulary-'+unitId+'-'+i,skill:'__vocabulary',skillName:'Vocabulary',tagName:'Vocabulary',vocabulary:true,q:{prompt:'Define: '+term,ask:'',fig:null},answer:definition,steps:example&&!/^see section/i.test(example)?[{t:example}]:[],options:[]};
  }).filter(function(it){return it.answer;});
 }};
})(window);
