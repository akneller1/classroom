/* Original MCAS-style contextual question bank for all 12 Algebra 1 units.
   Each scene generates linked, multi-part questions. A separate verifier
   reconstructs the mathematics from the numeric data in the printed stem. */
(function(G) {
  'use strict';
  var M=G.MKMENU;
  var scenes={
    'algebra1-foundations':function(r,c){
      var n=r.int(2,6+c),price=r.int(2,5+c),fee=r.int(2,7+c);
      return ['A class orders '+n+' notebooks at $'+price+' each. Shipping costs $'+fee+' per order.',
        ['What is the cost of the notebooks before shipping?','What is the total cost including shipping?','If the class places two identical orders, what is the combined total cost?'],
        [n*price,n*price+fee,2*(n*price+fee)]];
    },
    'algebra1-expressions-equations':function(r,c){
      var fee=r.int(5,18+c),rate=r.int(3,9+c),visits=r.int(3,9+c),total=fee+rate*visits;
      return ['A recreation center charges a $'+fee+' registration fee and $'+rate+' per visit. A member paid $'+total+' in total.',
        ['How much of the payment was for visits, excluding the registration fee?','How many visits did the member make?','What would the total cost be for one additional visit?'],
        [total-fee,visits,total+rate]];
    },
    'algebra1-inequalities':function(r,c){
      var start=r.int(8,30+c*3),each=r.int(4,11+c),need=r.int(3,8+c),goal=start+each*need;
      return ['A club has $'+start+' saved. Each ticket sold raises $'+each+'. The club must have at least $'+goal+' for a trip.',
        ['How much more money does the club need?','What is the minimum number of tickets that must be sold?','How much money will the club have after selling one fewer ticket than that minimum?'],
        [goal-start,need,start+each*(need-1)]];
    },
    'algebra1-relations-functions':function(r,c){
      var m=r.int(2,6+c),b=r.int(3,14+c),x=r.int(2,6+c);
      return ['A custom-print shop charges a $'+b+' setup fee plus $'+m+' for each shirt. A customer orders '+x+' shirts.',
        ['What is the total cost for the order?','What would the total cost be for one more shirt?','By how many dollars does the cost increase when the quantity increases by one?'],
        [b+m*x,b+m*(x+1),m]];
    },
    'algebra1-linear-equations-slope':function(r,c){
      var rate=r.int(2,6+c),hours=r.int(2,5+c),capacity=rate*r.int(hours+2,hours+7+c);
      return ['A tank starts with '+capacity+' gallons and drains at '+rate+' gallons per hour. A technician checks it after '+hours+' hours.',
        ['How many gallons remain when the technician checks?','What is the slope of the amount-versus-time graph? Use a negative value for draining.','How many hours after draining starts will the tank be empty?'],
        [capacity-rate*hours,-rate,capacity/rate]];
    },
    'algebra1-systems-of-equations':function(r,c){
      var adult=r.int(3,9+c),student=r.int(4,10+c),pa=r.int(10,19+c),ps=r.int(3,9+c);if(pa===ps)pa++;
      var count=adult+student, revenue=adult*pa+student*ps;
      return ['A school show sells '+count+' tickets for $'+revenue+'. Adult tickets cost $'+pa+' and student tickets cost $'+ps+'.',
        ['How many adult tickets were sold?','How many student tickets were sold?','How much money came from adult tickets?'],
        [adult,student,adult*pa]];
    },
    'algebra1-exponents-scientific-notation':function(r,c){
      var base=r.int(2,8+c),power=r.int(2,3+(c>4?2:0)),copies=r.int(2,6+c),q=base*Math.pow(10,power);
      return ['A lab measures '+base+' times ten to the power of '+power+' particles in one sample. It collects '+copies+' identical samples.',
        ['How many particles are in one sample in standard notation?','How many particles are in all the samples?','What is the exponent of ten in the original measurement?'],
        [q,q*copies,power]];
    },
    'algebra1-exponential-functions':function(r,c){
      var initial=r.int(2,8+c),time=r.int(2,4+(c>4?2:0));
      return ['A culture starts with '+initial+' cells and doubles every hour. A scientist checks the culture after '+time+' hours.',
        ['How many cells are present at that time?','How many cells are present one hour later?','By how many cells does the population increase during that final hour?'],
        [initial*Math.pow(2,time),initial*Math.pow(2,time+1),initial*Math.pow(2,time)]];
    },
    'algebra1-polynomials':function(r,c){
      var a=r.int(1,5+c),b=r.int(1,5+c),x=r.int(2,6+c);
      return ['A rectangle has side lengths (x + '+a+') feet and (x + '+b+') feet. For this design, x = '+x+'.',
        ['What is the numerical area of the rectangle in square feet?','What is the coefficient of x in the expanded area expression?','What is the constant term of that expanded expression?'],
        [(x+a)*(x+b),a+b,a*b]];
    },
    'algebra1-factoring-zero-product':function(r,c){
      var a=r.int(2,7+c),b=r.int(a+1,a+6+c),sum=a+b,product=a*b;
      return ['A polynomial is x squared plus '+sum+'x plus '+product+'. It factors into two linear expressions with integer constants.',
        ['What is the smaller zero of the polynomial?','What is the larger zero of the polynomial?','What is the product of the two zeros?'],
        [-b,-a,product]];
    },
    'algebra1-quadratics':function(r,c){
      var peakTime=r.int(2,5+c),flight=2*peakTime,height=peakTime*peakTime;
      return ['The height of a ball, in meters, is modeled by h(t) = -t squared + '+flight+'t, where t is seconds after launch.',
        ['After how many seconds does the ball return to the ground?','At what time does the ball reach its maximum height?','What is that maximum height in meters?'],
        [flight,peakTime,height]];
    },
    'algebra1-statistics-data-modeling':function(r,c){
      var start=r.int(3,13+c),step=r.int(2,6+c);var a=[0,1,2,3,4].map(i=>start+i*step);
      return ['Five students report study times of '+a.join(', ')+' minutes, listed in order.',
        ['What is the mean study time in minutes?','What is the median study time in minutes?','What is the range in minutes?'],
        [a[2],a[2],a[4]-a[0]]];
    }
  };
  /* Second distinct modeling task for every unit. These require the same
     independent printed-data verification as the first 12 families. */
  var extensions={
    'algebra1-foundations':function(r,c){
      var a=r.int(3,10+c),b=r.int(2,8+c),d=r.int(2,7+c);
      return ['A field trip has '+a+' groups with '+b+' students per group. Each student receives '+d+' pencils.',
        ['How many students attend?','How many pencils are needed?','How many pencils are needed if one more group attends?'],[a*b,a*b*d,(a+1)*b*d]];
    },
    'algebra1-expressions-equations':function(r,c){
      var a=r.int(3,10+c),b=r.int(2,8+c),d=r.int(2,9+c);
      return ['A student buys '+a+' identical folders and pays a one-time 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var variant=ctx.rng.int(0,1)===1?'extension':'original';
    if (variant==='extension' && extensions[unit]) fn=extensions[unit];
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i,variant:variant}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit+'-'+variant,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+b+' handling fee. The total is 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+(a*d+b)+'.',
        ['What is the amount spent on folders alone?','What is the price of each folder?','What would '+(a+1)+' folders cost including the same fee?'],[a*d,d,(a+1)*d+b]];
    },
    'algebra1-inequalities':function(r,c){
      var a=r.int(30,60+c*3),b=r.int(3,9+c),d=r.int(3,9+c),budget=a+b*d;
      return ['A school club has a budget of 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+budget+'. A bus costs 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+a+' and each admission costs 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+b+'.',
        ['How much of the budget remains after paying for the bus?','What is the maximum number of admissions it can purchase?','What will be left after purchasing one fewer admission?'],[budget-a,d,b]];
    },
    'algebra1-relations-functions':function(r,c){
      var a=r.int(5,15+c),b=r.int(2,8+c),d=r.int(3,9+c);
      return ['A bike rental costs 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+a+' to start plus 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+b+' per hour. A customer rents a bike for '+d+' hours.',
        ['What is the total cost?','What is the cost for two more hours?','What is the difference between the two costs?'],[a+b*d,a+b*(d+2),2*b]];
    },
    'algebra1-linear-equations-slope':function(r,c){
      var a=r.int(2,7+c),b=r.int(3,8+c),d=r.int(2,8+c);
      return ['A cyclist starts '+a+' miles from home and rides farther away at '+b+' miles per hour for '+d+' hours.',
        ['How far from home is the cyclist at the end?','What is the slope of the distance-versus-time graph?','What is the distance from home one hour later at the same rate?'],[a+b*d,b,a+b*(d+1)]];
    },
    'algebra1-systems-of-equations':function(r,c){
      var a=r.int(4,12+c),b=r.int(3,10+c),d=r.int(2,6+c),e=d+r.int(2,6+c);
      return ['A fundraiser sells '+(a+b)+' items for 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+(a*d+b*e)+'. Small items cost 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+d+' and large items cost 
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
+e+'.',
        ['How many small items were sold?','How many large items were sold?','How much revenue came from large items?'],[a,b,b*e]];
    },
    'algebra1-exponents-scientific-notation':function(r,c){
      var a=r.int(2,9+c),b=r.int(2,4+(c>4?1:0)),d=r.int(2,7+c);
      return ['A digital image contains '+a+' times ten to the power of '+b+' pixels. A gallery displays '+d+' identical images.',
        ['How many pixels are in one image?','How many pixels are displayed in total?','How many more pixels are displayed than in one image?'],[a*10**b,a*10**b*d,a*10**b*(d-1)]];
    },
    'algebra1-exponential-functions':function(r,c){
      var a=r.int(2,8+c),b=r.int(2,5+(c>4?1:0));
      return ['A video has '+a+' views and its total views triple every day. The pattern continues for '+b+' days.',
        ['How many views are there after the stated number of days?','How many views are there one day later?','What is the ratio of the later total to the earlier total?'],[a*3**b,a*3**(b+1),3]];
    },
    'algebra1-polynomials':function(r,c){
      var a=r.int(2,8+c),b=r.int(2,8+c),d=r.int(2,7+c);
      return ['A garden has width (x + '+a+') meters and length (x + '+b+') meters. Use x = '+d+'.',
        ['What is its area in square meters?','What is the coefficient of x in the expanded area expression?','What is the constant term in that expression?'],[(d+a)*(d+b),a+b,a*b]];
    },
    'algebra1-factoring-zero-product':function(r,c){
      var a=r.int(2,8+c),b=r.int(a+1,a+6+c);
      return ['A polynomial is x squared minus '+(a+b)+'x plus '+(a*b)+'. Its zeros are positive integers.',
        ['What is its smaller zero?','What is its larger zero?','What is the sum of the zeros?'],[a,b,a+b]];
    },
    'algebra1-quadratics':function(r,c){
      var a=r.int(2,7+c),b=r.int(2,7+c);
      return ['The height of a launched toy is h(t) = -(t - '+a+') squared + '+b*b+' meters.',
        ['At what time does the toy reach its maximum height?','What is that height in meters?','How many meters below the maximum is it one second after the peak?'],[a,b*b,1]];
    },
    'algebra1-statistics-data-modeling':function(r,c){
      var a=r.int(4,14+c),b=r.int(2,7+c),arr=[a,a+b,a+2*b,a+3*b,a+4*b];
      return ['A runner records five training distances of '+arr.join(', ')+' kilometers, listed in order.',
        ['What is the median distance?','What is the range of the distances?','What is the mean distance?'],[arr[2],arr[4]-arr[0],arr[2]]];
    }
  };
  M.contextScenes=scenes;
  M.contextExtensions=extensions;
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var x=fn(ctx.rng,ctx.c),parts=x[1].map(function(t,i){
      return {label:String.fromCharCode(97+i),prompt:t,answer:String(x[2][i]),
        check:{type:'mcas-context',unit:unit,index:i}};
    });
    // Vary the framing as well as the numbers so 25-question batches can
    // generate distinct verified prompts even for constrained CP2 values.
    var audiences=['a teacher','a coach','a student','a club adviser','a principal','a volunteer',
      'a technician','a mentor','a project leader','a parent','a counselor','a coordinator'];
    var purposes=['a class report','a project summary','a team presentation','a budget meeting',
      'a planning session','a math journal','a school newsletter','a progress report',
      'a small-group discussion','a homework review','a study guide','an investigation'];
    var frame='Present your findings to '+ctx.rng.pick(audiences)+' for '+ctx.rng.pick(purposes)+'. ';
    return {variant:'mcas-context-'+unit,prompt:x[0]+' '+frame+'Answer all three parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'MCAS contextual open response',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
