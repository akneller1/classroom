"""Small SVG helpers for the Geometry escape rooms (dark scene style used by the room engine)."""
import math
def pt(p): return '%.1f,%.1f'%p
def mid(a,b): return ((a[0]+b[0])/2,(a[1]+b[1])/2)
def foot(p,a,b):
    dx,dy=b[0]-a[0],b[1]-a[1]; t=((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy); return (a[0]+t*dx,a[1]+t*dy)
def line(a,b,color='#ffc857',w=3,dash=None):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>'%(a[0],a[1],b[0],b[1],color,w,(' stroke-dasharray="%s"'%dash if dash else ''))
def dot(p,r=3.5,c='#fff'): return '<circle cx="%.1f" cy="%.1f" r="%s" fill="%s"/>'%(p[0],p[1],r,c)
def text(p,s,size=15,c='#fff',anchor='start',w=700): return '<text x="%.1f" y="%.1f" fill="%s" font-size="%s" font-weight="%s" text-anchor="%s">%s</text>'%(p[0],p[1],c,size,w,anchor,s)
def tick(a,b,n=1,color='#fff'):
    m=mid(a,b); dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy); ux,uy=dx/L,dy/L; nx,ny=-uy,ux; out=''
    for j in range(n):
        o=(j-(n-1)/2)*6; x,y=m[0]+ux*o,m[1]+uy*o
        out+='<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2.2"/>'%(x-5*nx,y-5*ny,x+5*nx,y+5*ny,color)
    return out
def rightmark(v,p,q,s=11):
    ux,uy=p[0]-v[0],p[1]-v[1]; L=math.hypot(ux,uy); ux,uy=ux/L,uy/L
    wx,wy=q[0]-v[0],q[1]-v[1]; L=math.hypot(wx,wy); wx,wy=wx/L,wy/L
    a=(v[0]+s*ux,v[1]+s*uy); b=(a[0]+s*wx,a[1]+s*wy); c=(v[0]+s*wx,v[1]+s*wy)
    return '<polyline points="%s %s %s" fill="none" stroke="#fff" stroke-width="2"/>'%(pt(a),pt(b),pt(c))
def arc(v,p,q,r,color='#fff'):
    a1=math.atan2(p[1]-v[1],p[0]-v[0]); a2=math.atan2(q[1]-v[1],q[0]-v[0])
    d=(a2-a1+math.pi)%(2*math.pi)-math.pi
    s=(v[0]+r*math.cos(a1),v[1]+r*math.sin(a1)); e=(v[0]+r*math.cos(a1+d),v[1]+r*math.sin(a1+d))
    return '<path d="M%.1f %.1f A%s %s 0 0 %d %.1f %.1f" fill="none" stroke="%s" stroke-width="2"/>'%(s[0],s[1],r,r,1 if d>0 else 0,e[0],e[1],color)
