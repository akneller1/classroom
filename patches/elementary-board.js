  /* Shared board game: only the student answers questions in solo mode. */
  function playBoard(cfg) {
    var ttt = cfg.engine === 'ttt', rows = ttt ? 3 : 6, cols = ttt ? 3 : 7, needed = ttt ? 3 : 4;
    var grid = Array.from({length:rows}, function(){return Array(cols).fill(null);});
    var turn = 0, over = false, earned = false, solo = state.mode === 'solo', AI = G.MKSOLOAI;
    var names = solo ? ['You','Computer'] : TEAM_NAMES;
    var hud = el('div',stage,'el-hud'), scene = el('div',stage,'el-board'), qhost = el('div',stage);
    function winner(){
      for(var r=0;r<rows;r++)for(var c=0;c<cols;c++)for(var d of [[0,1],[1,0],[1,1],[1,-1]]){
        if(grid[r][c]===null)continue;var n=1;
        while(n<needed&&grid[r+d[0]*n]&&grid[r+d[0]*n][c+d[1]*n]===grid[r][c])n++;
        if(n===needed)return grid[r][c];
      }return null;
    }
    function draw(){
      hud.replaceChildren();names.slice(0,2).forEach(function(name,i){var chip=el('span',hud,'el-team'+(i===turn?' el-turn':''),name);chip.style.background=TEAM_COLORS[i];});
      scene.replaceChildren();var board=el('div',scene,'el-grid-btns');board.style.cssText='display:grid;grid-template-columns:repeat('+cols+',1fr);gap:6px;max-width:34rem;margin:1rem auto';
      grid.forEach(function(row,r){row.forEach(function(v,c){var b=el('button',board,'el-btn',v===null?'·':ttt?(v===0?'X':'O'):'●');b.type='button';b.style.cssText='min-height:48px;padding:8px;background:'+(v===null?'#eef4ff':TEAM_COLORS[v])+';color:'+(v===null?'#263452':'#fff');b.setAttribute('aria-label',ttt?'Square '+(r*cols+c+1):'Drop in column '+(c+1));b.disabled=over||!earned||v!==null||(solo&&turn===1);b.onclick=function(){if(!earned||over||(solo&&turn===1))return;earned=false;drop(r,c);};});});
    }
    function drop(r,c){
      if(!ttt){r=rows-1;while(r>=0&&grid[r][c]!==null)r--;}
      if(r<0||grid[r][c]!==null)return;grid[r][c]=turn;
      var win=winner(), full=grid.every(function(row){return row.every(function(v){return v!==null;});});
      if(win!==null||full){over=true;draw();qhost.replaceChildren();summary(qhost,win!==null?names[win]+' '+(ttt?'made three in a row!':'connected four!'):'The board is full. It’s a tie!','🎉');return;}
      turn=1-turn;round();
    }
    function round(){
      earned=false;draw();qhost.replaceChildren();
      if(solo&&turn===1){
        el('p',qhost,'el-chip','The computer is thinking…');
        G.setTimeout(function(){
          if(over||!stage.isConnected)return;
          if(!AI.answers('easy')){turn=0;round();el('p',hud,'el-chip','The computer missed its problem. Your turn!');return;}
          var move=ttt?AI.ticTacToeMove(grid.flat(),1,0,'easy'):AI.connectFourMove(grid,1,0,'easy');
          drop(ttt?Math.floor(move/cols):0,ttt?move%cols:move);
          if(!over)el('p',hud,'el-chip','The computer played '+(ttt?'square ':'column ')+(move+1)+'.');
        },850);return;
      }
      ask(qhost,{label:names[turn]+' — answer correctly to earn '+(ttt?'a square.':'a disc.'),choiceOnly:true,tries:1,
        done:function(ok){earned=ok;draw();},
        onNext:function(){if(earned){el('p',hud,'el-chip',ttt?'Choose an open square.':'Choose a column.');return;}turn=1-turn;round();},nextLabel:'Continue →'});
    }
    if(solo&&!AI){K.errorBox(qhost,'The computer opponent could not load. Reload the page to try again.');return;}
    round();
  }
