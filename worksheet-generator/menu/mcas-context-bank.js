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
    'algebra1-foundations':function(r,c){var a=r.int(3,10+c),b=r.int(2,8+c),d=r.int(2,7+c);return ['A field trip has '+a+' groups of '+b+' students. Each student gets '+d+' pencils.',['How many students?','How many pencils?','How many pencils if one more group joins?'],[a*b,a*b*d,(a+1)*b*d]];},
    'algebra1-expressions-equations':function(r,c){var a=r.int(3,10+c),b=r.int(2,8+c),d=r.int(2,9+c);return ['A student buys '+a+' folders and pays '+b+' dollars as a one-time handling fee. The total is '+(a*d+b)+' dollars.',['How much is spent on folders alone?','How much does each folder cost?','How much would one additional folder cost in total, including the same fee?'],[a*d,d,(a+1)*d+b]];},
    'algebra1-inequalities':function(r,c){var a=r.int(30,60+c*3),b=r.int(3,9+c),d=r.int(3,9+c),budget=a+b*d;return ['A club has '+budget+' dollars. The bus costs '+a+' dollars and each admission costs '+b+' dollars.',['How much remains after the bus?','What is the maximum number of admissions?','How much remains after purchasing one fewer admission?'],[budget-a,d,b]];},
    'algebra1-relations-functions':function(r,c){var a=r.int(5,15+c),b=r.int(2,8+c),d=r.int(3,9+c);return ['A bike rental costs '+a+' dollars to start plus '+b+' dollars per hour for '+d+' hours.',['What is the total cost?','What would two more hours cost in total?','What is the increase in cost?'],[a+b*d,a+b*(d+2),2*b]];},
    'algebra1-linear-equations-slope':function(r,c){var a=r.int(2,7+c),b=r.int(3,8+c),d=r.int(2,8+c);return ['A cyclist is '+a+' miles from home and travels farther away at '+b+' miles per hour for '+d+' hours.',['What is the ending distance?','What is the slope of distance against time?','How far from home after one additional hour?'],[a+b*d,b,a+b*(d+1)]];},
    'algebra1-systems-of-equations':function(r,c){var a=r.int(4,12+c),b=r.int(3,10+c),d=r.int(2,6+c),e=d+r.int(2,6+c);return ['A fundraiser sells '+(a+b)+' items for '+(a*d+b*e)+' dollars. Small items cost '+d+' dollars and large items cost '+e+' dollars.',['How many small items?','How many large items?','How much revenue came from large items?'],[a,b,b*e]];},
    'algebra1-exponents-scientific-notation':function(r,c){var a=r.int(2,9+c),b=r.int(2,4+(c>4?1:0)),d=r.int(2,7+c);return ['One image has '+a+' times ten to the power of '+b+' pixels. There are '+d+' identical images.',['How many pixels in one image?','How many pixels total?','How many more pixels than in one image?'],[a*10**b,a*10**b*d,a*10**b*(d-1)]];},
    'algebra1-exponential-functions':function(r,c){var a=r.int(2,8+c),b=r.int(2,5+(c>4?1:0));return ['A video begins with '+a+' views and the view count triples daily for '+b+' days.',['How many views after the stated days?','How many views one day later?','What is the ratio of later views to earlier views?'],[a*3**b,a*3**(b+1),3]];},
    'algebra1-polynomials':function(r,c){var a=r.int(2,8+c),b=r.int(2,8+c),d=r.int(2,7+c);return ['A garden has width (x + '+a+') and length (x + '+b+'). Take x = '+d+'.',['What is the garden area?','What is the coefficient of x in its expanded area expression?','What is the constant term?'],[(d+a)*(d+b),a+b,a*b]];},
    'algebra1-factoring-zero-product':function(r,c){var a=r.int(2,8+c),b=r.int(a+1,a+6+c);return ['A polynomial is x squared minus '+(a+b)+'x plus '+(a*b)+'. Its zeros are positive integers.',['What is the smaller zero?','What is the larger zero?','What is the sum of the zeros?'],[a,b,a+b]];},
    'algebra1-quadratics':function(r,c){var a=r.int(2,7+c),b=r.int(2,7+c);return ['The height of a toy is h(t) = -(t - '+a+') squared + '+b*b+' meters.',['When is the maximum height reached?','What is the maximum height?','How far below the maximum is the height one second after the peak?'],[a,b*b,1]];},
    'algebra1-statistics-data-modeling':function(r,c){var a=r.int(4,14+c),b=r.int(2,7+c),v=[a,a+b,a+2*b,a+3*b,a+4*b];return ['Five training distances are '+v.join(', ')+' kilometers.',['What is the median?','What is the range?','What is the mean?'],[v[2],v[4]-v[0],v[2]]];}
  };
  /* Third-family interpretation bank: tables, paired observations and model checks.
     More structurally varied than the two straightforward word-problem families. */
  var interpretations={
    'algebra1-relations-functions':function(r,c){
      var start=r.int(2,12+c),step=r.int(2,7+c),x=r.int(2,6+c);
      return ['A machine produces a table of input-output pairs: input 0, output '+start+'; input 1, output '+(start+step)+'; input 2, output '+(start+2*step)+'. The output changes at a constant rate. Find its value at input '+x+'.',
        ['What is the rate of change?','What is the output at the requested input?','What is the output at the next input?'],[step,start+step*x,start+step*(x+1)]];
    },
    'algebra1-linear-equations-slope':function(r,c){
      var start=r.int(5,20+c),m=r.int(2,7+c),x=r.int(3,8+c);
      return ['A table records time and distance for constant-speed travel: at time 0 hours, '+start+' miles; at time 1 hour, '+(start+m)+' miles; at time 2 hours, '+(start+2*m)+' miles. Predict the distance at time '+x+' hours.',
        ['What is the slope in miles per hour?','What is the predicted distance at the requested time?','How far does the traveler go during the first two hours?'],[m,start+m*x,2*m]];
    },
    'algebra1-exponential-functions':function(r,c){
      var first=r.int(2,6+c),factor=r.int(2,3+(c>5?1:0)),time=r.int(2,5+c);
      return ['A table shows a population pattern: at hour 0, '+first+' organisms; at hour 1, '+(first*factor)+'; at hour 2, '+(first*factor*factor)+'. Assume the same multiplicative pattern until hour '+time+'.',
        ['What is the growth factor per hour?','What is the population at the requested hour?','How much larger is the population at the next hour?'],[factor,first*Math.pow(factor,time),first*Math.pow(factor,time)*(factor-1)]];
    },
    'algebra1-statistics-data-modeling':function(r,c){
      var a=r.int(5,16+c),d=r.int(2,6+c),values=[a,a+d,a+2*d,a+3*d,a+4*d];
      return ['Five ordered scores are shown in a table: '+values.join(', ')+'. The team wants to compare typical performance and spread.',
        ['What is the median score?','What is the interquartile range using medians of the lower and upper halves?','What is the mean score?'],[values[2],3*d,values[2]]];
    }
  };
  /* Additional distinct multi-part families with modeling and comparison. */
  var applied={
    'algebra1-foundations':function(r,c){
      var rows=r.int(3,7+c),columns=r.int(4,9+c),empty=r.int(1,rows-1);
      return ['A theater has '+rows+' rows with '+columns+' seats in each row. '+empty+' entire rows are reserved and unavailable.',
       ['How many seats are in the theater?','How many seats are available?','How many seats are unavailable?'],
       [rows*columns,(rows-empty)*columns,empty*columns]];
    },
    'algebra1-expressions-equations':function(r,c){
      var hours=r.int(3,7+c),rate=r.int(9,18+c),bonus=r.int(10,30+c);
      return ['A student earns '+rate+' dollars per hour for '+hours+' hours of tutoring and also earns a '+bonus+' dollar bonus.',
       ['How much is earned from hourly pay?','What is the total pay?','What would the total pay be after one additional hour at the same rate?'],
       [hours*rate,hours*rate+bonus,(hours+1)*rate+bonus]];
    },
    'algebra1-inequalities':function(r,c){
      var capacity=r.int(40,75+c),occupied=r.int(12,25+c),group=r.int(3,7+c);
      return ['A room holds at most '+capacity+' people. There are already '+occupied+' people inside. Each arriving team has '+group+' people.',
       ['How many more people can enter?','What is the greatest number of complete teams that can enter?','How many spaces remain after that many teams enter?'],
       [capacity-occupied,Math.floor((capacity-occupied)/group),(capacity-occupied)%group]];
    },
    'algebra1-systems-of-equations':function(r,c){
      var n=r.int(4,10+c),m=r.int(4,10+c),adult=r.int(10,18+c),child=r.int(3,8+c),total=n*adult+m*child;
      return ['A museum sells '+(n+m)+' passes for '+total+' dollars. Adult passes cost '+adult+' dollars and child passes cost '+child+' dollars.',
       ['How many adult passes were sold?','How many child passes were sold?','What revenue came from child passes?'],
       [n,m,m*child]];
    },
    'algebra1-exponents-scientific-notation':function(r,c){
      var base=r.int(2,7+c),power=r.int(3,5),machines=r.int(2,6+c);
      return ['A sensor records '+base+' times ten to the power of '+power+' readings per day. '+machines+' identical sensors operate for one day.',
       ['How many readings does one sensor record?','How many readings do all sensors record?','How many additional readings does adding one more sensor produce?'],
       [base*10**power,base*10**power*machines,base*10**power]];
    },
    'algebra1-polynomials':function(r,c){
      var a=r.int(2,7+c),b=r.int(2,6+c),x=r.int(2,6+c);
      return ['A rectangle has dimensions (x + '+a+') and (x + '+b+'). Evaluate its area when x = '+x+'.',
       ['What is the coefficient of x in the expanded area polynomial?','What is the constant term?','What is the numerical area for the stated x?'],
       [a+b,a*b,(x+a)*(x+b)]];
    },
    'algebra1-factoring-zero-product':function(r,c){
      var a=r.int(2,6+c),b=r.int(a+1,a+6+c);
      return ['A polynomial is x squared minus '+(a+b)+'x plus '+a*b+'. A graph crosses the horizontal axis at its two zeros.',
       ['What is the smaller zero?','What is the greater zero?','What is the distance between the zeros?'],
       [a,b,b-a]];
    },
    'algebra1-quadratics':function(r,c){
      var h=r.int(2,6+c),k=r.int(3,10+c);
      return ['A parabola has equation y = -(x - '+h+') squared + '+k+'.',
       ['What is the x-coordinate of its vertex?','What is its maximum y-value?','What is its y-value one unit to the right of the vertex?'],
       [h,k,k-1]];
    }
  };
  M.contextScenes=scenes;
  M.contextExtensions=extensions;
  M.contextInterpretations=interpretations;
  M.contextApplied=applied;
  M.makeContextProblem=function(unit, ctx) {
    var fn=scenes[unit];if(!fn)return {failed:true,reason:'No contextual bank for '+unit};
    var draw=ctx.rng.int(0,applied[unit]?3:interpretations[unit]?2:1);
    var variant=draw===3?'applied':draw===2?'interpret':draw===1?'extension':'original';
    if (variant==='extension' && extensions[unit]) fn=extensions[unit];
    if (variant==='interpret' && interpretations[unit]) fn=interpretations[unit];
    if (variant==='applied' && applied[unit]) fn=applied[unit];
    var x=fn(ctx.rng,ctx.c);
    // Fourth part requires interpreting the calculation, not just returning a scalar.
    x[1].push('A classmate doubles your numerical answer to part (a). What number would that produce? Explain whether doubling that quantity makes sense for this situation.');
    x[2].push(2*x[2][0]);
    var parts=x[1].map(function(t,i){
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
    return {variant:'mcas-context-'+unit+'-'+variant,prompt:x[0]+' '+frame+'Answer all four parts and show your reasoning.',
      parts:parts,steps:parts.map(function(part){return {t:'Part ('+part.label+'): '+part.answer,w:1};}),
      space:[2.4,3.0,3.7]};
  };
  Object.keys(scenes).forEach(function(unit){
    var set=M.skillSets[unit];if(!set)return;
    var first=set.skills[0];
    var skill={id:'mcas-context',name:'Open Response contextual scenario',tag:first.tag,
      best:[1,2],blurb:'Original multi-part applied scenario with separately verified answers.',
      generate:function(ctx){return M.makeContextProblem(unit,ctx);}};
    set.skills.push(skill);set.byId[skill.id]=skill;
  });
})(typeof window!=='undefined'?window:globalThis);
