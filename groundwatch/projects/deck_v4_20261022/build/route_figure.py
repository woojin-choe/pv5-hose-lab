# 실제 명일동 OSM 지도(myeongil_dark.png) 위에 회차별 주행 궤적과 보정 후 정합선을 그린다.
from PIL import Image, ImageDraw, ImageFilter
import math
base=Image.open("myeongil_dark.png").convert("RGB")
x0,y0,x1,y1=790,968,1078,1149
S=6
crop=base.crop((x0,y0,x1,y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.2))
crop=Image.blend(crop,Image.new("RGB",crop.size,(6,12,26)),0.30)
W,H=crop.size
road=[(790,1053),(860,1061),(960,1071),(1038,1079),(1046,1030),(1052,968)]
def dens(pts,step=1.5):
    out=[]
    for (a,b),(c,e) in zip(pts,pts[1:]):
        n=max(1,int(math.hypot(c-a,e-b)/step)); out+=[(a+(c-a)*i/n,b+(e-b)*i/n) for i in range(n)]
    return out+[pts[-1]]
R=dens(road)
def nrm(i):
    a=R[max(0,i-2)];b=R[min(len(R)-1,i+2)];dx,dy=b[0]-a[0],b[1]-a[1];l=math.hypot(dx,dy) or 1;return -dy/l,dx/l
def trace(off,amp,ph,freq):
    return [((x+nrm(i)[0]*(off+amp*math.sin(i*freq+ph))-x0)*S,(y+nrm(i)[1]*(off+amp*math.sin(i*freq+ph))-y0)*S) for i,(x,y) in enumerate(R)]
lay=Image.new("RGBA",(W,H),(0,0,0,0))
for col,(o,a,p,f) in [((154,163,175),(-6.5,1.4,0.3,0.05)),((78,143,217),(0.4,1.6,1.9,0.04)),((245,183,0),(6.2,1.2,3.3,0.06))]:
    pts=trace(o,a,p,f)
    g=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(g).line(pts,fill=col+(120,),width=40,joint="curve")
    lay=Image.alpha_composite(lay,g.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(lay).line(pts,fill=col+(255,),width=13,joint="curve")
pts=trace(0,0,0,0); d=ImageDraw.Draw(lay)
for i in range(0,len(pts)-6,10): d.line(pts[i:i+6],fill=(255,255,255,240),width=7)
for (x,y) in [(1038,1079),(860,1061)]:
    X,Y=(x-x0)*S,(y-y0)*S
    d.ellipse((X-34,Y-34,X+34,Y+34),outline=(255,255,255,255),width=8); d.ellipse((X-9,Y-9,X+9,Y+9),fill=(255,255,255,255))
out=Image.alpha_composite(crop.convert("RGBA"),lay).convert("RGB").resize((W//2,H//2),Image.LANCZOS)
out.save("val_route_real.png"); print(out.size)
