// Apply reviewed gameplay fixes to every pinned course copy before deployment.
import fs from 'node:fs';import path from 'node:path';
const out=path.resolve(process.argv[2]||'_site'), root=process.cwd();
let board=fs.readFileSync('patches/elementary-board.js','utf8');
function edit(file,fn){if(!fs.existsSync(file))throw Error('Missing game release file: '+file);fs.writeFileSync(file,fn(fs.readFileSync(file,'utf8')));}
for(let grade=1;grade<=5;grade++){
 const base=path.join(out,'grade'+grade,'worksheet-generator'), elementary=grade<5;
 const engine=path.join(base,elementary?'elementary/el-games.js':'grade5/g5-games.js');
 edit(engine,s=>{
  const start=s.indexOf('  function playC4()'),end=s.indexOf('  /* ---------- engine: card match',start);if(start<0||end<0)throw Error('Board engine anchor changed: '+engine);
  let replacement=elementary?board:board.replaceAll('el-', 'g5-').replaceAll('K.errorBox','g5.errorBox');
  s=s.slice(0,start)+replacement+s.slice(end);
  s=s.replace('c4: playC4','c4: playBoard, ttt: playBoard');
  const anchor='  var state =';
  s=s.replace(anchor,`  Object.keys(GAMES).forEach(function(id){if(GAMES[id].engine==='c4')GAMES[id].modes=[['solo','Solo vs. computer'],['class2','2 teams']];});
  GAMES['tic-tac-toe']={title:'Tic-Tac-Toe',icon:'⭕',engine:'ttt',modes:[['solo','Solo vs. computer'],['class2','2 teams']],intro:'Answer correctly to claim a square. Make three in a row to win!'};
`+anchor);
  return s;
 });
 const core=path.join(base,elementary?'elementary/el-core.js':'grade5/g5-core.js');
 edit(core,s=>{
    // Student assignments always start in an actually supported individual mode.
  s=s.replace('    host.innerHTML = \'\';\n    var p = el(\'section\', host,',`    if(P.get('student')==='1'&&cfg.modes){cfg=Object.assign({},cfg,{modes:cfg.modes.filter(function(m){return m[0]==='solo';})});if(!cfg.modes.length){errorBox(host,'This game requires teams. Ask your teacher for an individual game.');return;}}
    host.innerHTML = '';
    var p = el('section', host,`);
  if(elementary){s=s.replace("if (P.get('student') !== '1') studentLink(p, cfg);","if (P.get('student') !== '1' && (!cfg.modes || cfg.modes.some(function(m){return m[0]==='solo';}))) studentLink(p, cfg);");s=s.replace("if (m) q.set('mode', m.value);","if (m) q.set('mode', 'solo');");}
  s=s.replace("if (!student) {\n      var share","if (!student && (!G.MK_GAME_CAPABILITIES || G.MK_GAME_CAPABILITIES.canShare({path:G.location.href,type:'Game'}))) {\n      var share");
  // Grade 5's header share button predates player-mode checking.
  s=s.replace("share.onclick = function () {", "share.onclick = function () {if(G.MK_GAME_CAPABILITIES&&!G.MK_GAME_CAPABILITIES.canShare({path:G.location.href,type:'Game'}))return;");
  return s;
 });
 const page=path.join(base,'grade'+grade+'-games.html');
 fs.mkdirSync(path.join(base,'games'),{recursive:true});fs.copyFileSync(path.join(root,'worksheet-generator/games/solo-ai.js'),path.join(base,'games/solo-ai.js'));
 edit(page,s=>s.replace(/<script src="(?:elementary\/el-games|grade5\/g5-games)\.js/, '<script src="games/solo-ai.js?v=solo-20261116"></script><script src="'+(elementary?'elementary/el-games':'grade5/g5-games')+'.js'));
}
// Financial Algebra bundles the same generated engine in two locations.
for(const folder of ['financial/games/vendor','financial-algebra/financial/games/vendor']){
 const dir=path.join(out,folder);if(!fs.existsSync(dir))continue;
 for(const file of ['games.js','solo-ai.js'])fs.copyFileSync(path.join(root,'worksheet-generator/games',file),path.join(dir,file));
}
// Add the new Tic-Tac-Toe engine to all elementary unit catalogs.
const catalog=`(function(G){for(const c of G.LIBRARY.courses){if(!/^grade[1-5]$/.test(c.id))continue;for(const u of c.units){if(u.artifacts.some(a=>/game=tic-tac-toe(?:&|$)/.test(a.path)))continue;const a=u.artifacts.find(a=>/game=/.test(a.path)&&a.type==='Game');if(!a)continue;const b=Object.assign({},a,{title:'Tic-Tac-Toe',format:'tic-tac-toe',bankFormat:'tic-tac-toe',description:'Play solo against the computer or with two teams. Answer correctly to claim a square.',path:a.path.replace(/([?&]game=)[^&]+/,'$1tic-tac-toe')});u.artifacts.push(b);}}})(window);`;
fs.writeFileSync(path.join(out,'elementary-board-catalog.js'),catalog);
// Inject capabilities before the app, including independently rendered course pages.
function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const f=path.join(dir,e.name);if(e.isDirectory()&&!['vendor','node_modules'].includes(e.name))walk(f);else if(e.name.endsWith('.html'))edit(f,s=>{
 const rel=path.relative(path.dirname(f),out).split(path.sep).join('/'),base=rel?rel+'/':'';
 if(/<script src="[^"]*app\.js/.test(s)&&!s.includes('elementary-board-catalog.js'))s=s.replace(/<script src="([^"<>]*app\.js[^"<>]*)">/,'<script src="'+base+'elementary-board-catalog.js?v=solo-20261116"></script><script src="$1">');
 if(s.includes('</head>')&&!s.includes('game-capabilities.js'))s=s.replace('</head>','<script src="'+base+'game-capabilities.js?v=site-audit-20261120"></script></head>');
 s=s.replace("'connect-four','puzzle-masters'","'connect-four','tic-tac-toe','puzzle-masters'").replace("['student','skills'].forEach","['student','skills','mode','level'].forEach");
 return s.replace(/((?:el-games|el-core|g5-games|g5-core|games\/games|solo-legacy|student-share-cards|student-game-share|integrated-student-share|app|activity)\.js)(?:\?v=[^"<> ]*)?(?=")/g,'$1?v=solo-20261116');
 });}}
walk(out);console.log('Applied solo modes, student-link guards and board catalogs across all courses.');
