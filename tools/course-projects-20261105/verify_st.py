"""Recomputes every number used in p_st.py (Statistics projects). Run: python3 verify_st.py"""
import statistics as S, numpy as np
A=[4,5,6,6,7,7,8,8,8,9,10,11,12,14,25]
B=[3,4,4,5,5,6,6,6,7,7,7,8,8,9,10]
def q(x):
    x=sorted(x); n=len(x); m=S.median(x)
    lo=x[:n//2]; hi=x[(n+1)//2:]
    return min(x),S.median(lo),m,S.median(hi),max(x)
for name,x in (('A',A),('B',B)):
    f=q(x); iqr=f[3]-f[1]
    print(name,'mean',S.mean(x),'median',f[2],'5num',f,'IQR',iqr,'fences',f[1]-1.5*iqr,f[3]+1.5*iqr,'range',f[4]-f[0],'sd',round(S.stdev(x),3))
A2=A[:-1]; print('A no 25 mean',round(S.mean(A2),3),'median',S.median(A2),'sd',round(S.stdev(A2),3))
# CP2 small set
C=[4,6,7,8,8,9,10,12,26]; print('C',S.mean(C),S.median(C),q(C))
# regression
x=np.array([2,4,5,6,8,10,12,15]); y=np.array([3,4,6,6,8,9,11,13])
b,a=np.polyfit(x,y,1); r=np.corrcoef(x,y)[0,1]
print('slope',b,'int',a,'r',r,'r2',r*r,'mean x',x.mean(),'mean y',y.mean(),'sx',x.std(ddof=1),'sy',y.std(ddof=1))
print('pred 9', a+b*9,'resid at 10', 9-(a+b*10), 'pred 40', a+b*40)
from math import *
from scipy import stats
import statistics as S
print('--U1 normal'); print(1-stats.norm.cdf(1.5), 9+stats.norm.ppf(.9)*2, stats.norm.cdf(-1)-0, stats.norm.cdf((7-9)/2), stats.norm.cdf(1)-stats.norm.cdf(-0.5))
print('--U2 digits')
d="1922395034057562871396409125314254482853"; pairs=[d[i:i+2] for i in range(0,len(d),2)]; out=[]
for p in pairs:
    v=int(p)
    if 1<=v<=60 and v not in out: out.append(v)
print(pairs); print(out)
print('--U3')
X=[1,3,10,25]; P=[.5,.3,.15,.05]
m=sum(x*p for x,p in zip(X,P)); v=sum((x-m)**2*p for x,p in zip(X,P)); sd=sqrt(v)
print('E',m,'Var',v,'SD',sd,'profit mean',5-m)
print('P>=1 gc in 20',1-.95**20,'P exactly 1',20*.05*.95**19,'P0',.95**20)
print('geom 3rd',.95**2*.05,'within 10', 1-.95**10)
print('two boxes sd',sqrt(2)*sd,'mean',2*m)
print('phat sd 200',sqrt(.05*.95/200))
print('mean of 100 sd',sd/10,'day profit mean',100*(5-m),'sd',10*sd,'P(profit<0)',stats.norm.cdf(-85/(10*sd)),'P(profit<50)',stats.norm.cdf((50-85)/(10*sd)))
print('P(phat>=.08) n200', 1-stats.norm.cdf((.08-.05)/sqrt(.05*.95/200)))
print('binom n=10 p=.2 P(X>=3)',1-stats.binom.cdf(2,10,.2),'P(X=2)',stats.binom.pmf(2,10,.2),'mean',2,'sd',sqrt(10*.2*.8))
# price change new price 6: profit Y=6-X
print('--U4')
ph=.62;n=400;se=sqrt(ph*(1-ph)/n);print('se',se,'ME95',1.96*se,(ph-1.96*se,ph+1.96*se),'99',2.576*se)
print('n for .03',(1.96/.03)**2*.25,'with .62',(1.96/.03)**2*.62*.38)
print('z',(.62-.5)/sqrt(.25/400))
se2=sqrt(.62*.38/100);print('cp2 se',se2,'ME',1.96*se2,(.62-1.96*se2,.62+1.96*se2))
print('cp2 z',(.62-.5)/sqrt(.25/100),'p',1-stats.norm.cdf((.62-.5)/sqrt(.25/100)))
ts=stats.t.ppf(.975,15);print('t*15',ts,6.8-ts*.3,6.8+ts*.3,'t',(6.8-8)/.3,'p',stats.t.cdf(-4,15))
p1,p2=130/200,118/200;se=sqrt(p1*(1-p1)/200+p2*(1-p2)/200);print('2prop',p1,p2,p1-p2,se,(p1-p2-1.96*se,p1-p2+1.96*se))
pc=248/400;sep=sqrt(pc*(1-pc)*(2/200));z=(p1-p2)/sep;print('pooled z',z,'p two-sided',2*(1-stats.norm.cdf(z)))
diff=[0.5,1.0,0.25,0.75,-0.25,1.25,0.5,0.0,1.0,0.5]
md=S.mean(diff);sd=S.stdev(diff);t=md/(sd/sqrt(10));print('paired',md,sd,sd/sqrt(10),'t',t,'p one',1-stats.t.cdf(t,9),'t*9',stats.t.ppf(.975,9),md-stats.t.ppf(.975,9)*sd/sqrt(10),md+stats.t.ppf(.975,9)*sd/sqrt(10))
print('new prize table E', 1*.575+3*.225+10*.15+25*.05, 'sum', .575+.225+.15+.05)
print('two-prop n', (1.96/.05)**2*.5, '30 people pred', 1.4625468+0.7790262*30)
