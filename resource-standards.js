/* One catalog contract for all courses, including currently hidden courses.
 * Original files and duplicate catalog records remain available in legacyArtifacts. */
(function(G){'use strict';
const types={
 flashcards:{name:'Flashcards',format:'flashcards',description:'Choose skills and difficulty, flip cards for worked solutions, and revisit missed questions.',thumb:'thumbs/foundations-algebra-flashcards.jpg'},
 'connect-four':{name:'Connect 4',format:'connect-four',description:'Teams solve problems to earn discs. A wrong answer opens a steal for the other team. Connect four to win.',thumb:'thumbs/foundations-algebra-connect-four.jpg'},
 'tic-tac-toe':{name:'Tic-Tac-Toe',format:'tic-tac-toe',description:'Answer to claim a square. The other team can steal a missed problem. Make three in a row to win.',thumb:'thumbs/foundations-algebra-tic-tac-toe.jpg'},
 'picture-reveal':{name:'Picture Reveal',format:'picture-reveal',description:'Choose skills and difficulty, solve problems, and uncover the hidden picture.',thumb:'thumbs/foundations-algebra-picture-reveal.jpg'},
 showdown:{name:'Showdown',format:'showdown',description:'Choose categories and point values. Solve questions, reveal worked solutions, and keep team scores.',thumb:'thumbs/foundations-algebra-showdown.jpg'},
 detective:{name:'Detective',format:'detective-games',description:'Earn evidence, clear suspects, locations, and methods, then make your final accusation.',thumb:'thumbs/foundations-algebra-midnight-library-mystery.jpg'},
 'escape-room':{name:'Escape Room',format:'escape-rooms',description:'Unlock five rooms, solve a cipher, arrange steps, collect key cards, and open the final door in ten minutes.',thumb:'thumbs/foundations-algebra-escape-room.jpg'}
};
function kind(a){
 const p=a.path||'';
 if(/\.pdf(?:$|\?)/.test(p))return null;
 const query=/[?&]game=([a-z-]+)/.exec(p);if(query&&types[query[1]])return query[1];
 if(a.bankFormat){const entry=Object.keys(types).find(k=>types[k].format===a.bankFormat);if(entry)return entry;}
 if(/flashcards/i.test(p))return 'flashcards';if(/connect-four|inequality-four/i.test(p))return 'connect-four';if(/tic-tac-toe/i.test(p))return 'tic-tac-toe';if(/picture-reveal/i.test(p))return 'picture-reveal';if(/showdown|jeopardy/i.test(p))return 'showdown';if(/escape-room/i.test(p))return 'escape-room';
 if((a.topics||[]).some(t=>/detective game/i.test(t))||/mystery|caper|whodunnit|fiasco|switcheroo|blackout/i.test(p)&&/index.html$/.test(p))return 'detective';return null;
}
function apply(library){
 library.courses.forEach(c=>c.units.forEach(u=>{
  const seen=new Set(),original=u.artifacts.slice();u.legacyArtifacts=original;
  u.artifacts=original.flatMap(a=>{const k=kind(a);if(!k)return [a];if(seen.has(k))return [];seen.add(k);const t=types[k],preview=G.MK_RESOURCE_PREVIEWS?.[c.id+'/'+u.id+'/'+k];
   let thumb=preview||a.thumb;if(!thumb||/foundations-algebra/.test(thumb)&&u.id!=='foundations-algebra')thumb=t.thumb;
   if(k==='detective'&&/showdown|jeopardy/.test(thumb))thumb=t.thumb;if(k==='escape-room'&&/showdown|jeopardy/.test(thumb))thumb=t.thumb;
   const base=['detective','escape-room'].includes(k)?'course-activity':'course-game';
   return [{...a,originalPath:a.path,legacyPaths:original.filter(item=>kind(item)===k).map(item=>item.path),title:u.name+' '+t.name,description:t.description,bankFormat:t.format,thumb,path:'worksheet-generator/'+base+'.html?course='+c.id+'&unit='+u.id+'&game='+k}];
  });
 }));
}
G.MK_RESOURCE_STANDARDS={types,kind,apply};if(G.LIBRARY)apply(G.LIBRARY);
})(window);
