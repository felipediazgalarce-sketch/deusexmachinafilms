"""Generador del logo dEUSeXmACHINA films con d, e y m destacadas.
Las letras salen de los SVG del logo animado (about-us/index.html) -> letras.json."""
import json,re,random
ORIG=json.load(open(__file__.rsplit("/",1)[0]+"/letras.json"))
B={l["i"]:l for l in ORIG}
DEM=(0,4,6); FILMS=(13,14,15,16,17)
TOP,BOT,PAD=19.7,78.0,4
E_CORTE=(227.0,62.8,20.0,3.2)   # canal que abre el ojo inferior de la "e" (coordenadas originales)
M=24
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c:c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
def contraste(fondo): return "#0a0a0a" if lum(fondo)>0.22 else "#ffffff"
class Logo:
    def __init__(self,mov=None):
        mov=mov or {i:(0,0) for i in range(18)}; self.L=[]
        for l in ORIG:
            dx,dy=mov[l["i"]]; x,y,w,h=l["vb"]
            ds=[re.sub(r'([ML]) ?([\d.]+) ([\d.]+)',lambda m:f'{m.group(1)}{float(m.group(2))+dx:.2f} {float(m.group(3))+dy:.2f}',d) for d in l["d"]]
            self.L.append({"i":l["i"],"vb":[x+dx,y+dy,w,h],"d":ds,"dx":dx,"dy":dy})
        xs=[];ys=[]
        for l in self.L:
            x,y,w,h=l["vb"]; xs+=[x-PAD-3,x+w+PAD+3]; ys+=[y-3,y+h+3]
            if l["i"] in DEM: ys+=[TOP-PAD+l["dy"],BOT+PAD+l["dy"]]
        self.bx=(min(xs),min(ys),max(xs),max(ys))
    def caja_letra(self,l):
        x,y,w,h=l["vb"]; return (x-PAD,TOP-PAD+l["dy"],w+2*PAD,BOT-TOP+2*PAD)
    def cajas(self,attrs="",rot=False,films=False,attrs_films=None):
        out=[]
        for l in self.L:
            if l["i"] in DEM:
                x,y,w,h=self.caja_letra(l); r=""
                if rot: a=random.uniform(-2.5,2.5); r=f' transform="rotate({a:.2f} {x+w/2:.1f} {y+h/2:.1f})"'
                out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"{attrs}{r}/>')
        if films:
            ls=[l for l in self.L if l["i"] in FILMS]
            x0=min(l["vb"][0] for l in ls)-PAD-6; x1=max(l["vb"][0]+l["vb"][2] for l in ls)+PAD+6
            y0=min(l["vb"][1] for l in ls)-PAD-4; y1=max(l["vb"][1]+l["vb"][3] for l in ls)+PAD+2
            out.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1-x0:.2f}" height="{y1-y0:.2f}"{attrs_films if attrs_films is not None else attrs}/>')
        return "\n".join(out)
    def letras(self,base,dem,films=None,attrs_dem="",attrs_base=""):
        films=films or base; out=[]
        for l in self.L:
            col=dem if l["i"] in DEM else (films if l["i"] in FILMS else base)
            at=attrs_dem if l["i"] in DEM else attrs_base
            ps="".join(f'<path fill-rule="evenodd" d="{d}" fill="{col}"{at}/>' for d in l["d"])
            if l["i"]==4:   # abrir la e
                cx,cy,cw,ch=E_CORTE; cx+=l["dx"]; cy+=l["dy"]; mid=f"ae{abs(hash((l['dx'],l['dy'])))%10**6}"
                ps=(f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="5000" height="5000">'
                    f'<rect x="-2000" y="-2000" width="5000" height="5000" fill="#fff"/>'
                    f'<polygon points="{cx},{cy+ch*0.35} {cx+cw},{cy-0.6} {cx+cw},{cy+ch+0.4} {cx},{cy+ch}" fill="#000"/></mask>'
                    f'<g mask="url(#{mid})">{ps}</g>')
            out.append(ps)
        return "\n".join(out)
    def svg(self,cuerpo,defs=""):
        b=self.bx
        return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{b[0]-M:.1f} {b[1]-M:.1f} {b[2]-b[0]+2*M:.1f} {b[3]-b[1]+2*M:.1f}"><defs>{defs}</defs>{cuerpo}</svg>'
    def tam(self): b=self.bx; return (b[2]-b[0]+2*M, b[3]-b[1]+2*M)
x0=lambda i:B[i]["vb"][0]; x1=lambda i:B[i]["vb"][0]+B[i]["vb"][2]
def una_linea(G=26,GF=30,TRACK=9):
    mov={}
    for i in range(18):
        if i<=3: mov[i]=(0,0)
        elif i<=5: mov[i]=(G,0)
        elif i<=12: mov[i]=(2*G,0)
    x=x1(12)+2*G+GF; dy=78.0-131.0
    for i in range(13,18): mov[i]=(x-x0(i),dy); x+=B[i]["vb"][2]+TRACK
    return mov
def cuatro_lineas(LIN=82,EXTRA=14):
    an={"a":x1(3)-x0(0),"b":x1(5)-x0(4),"c":x1(12)-x0(6),"d":x1(17)-x0(13)}; A=max(an.values()); mov={}
    for i in range(18):
        if i<=3: mov[i]=((A-an["a"])/2-x0(0),0)
        elif i<=5: mov[i]=((A-an["b"])/2-x0(4),LIN)
        elif i<=12: mov[i]=((A-an["c"])/2-x0(6),2*LIN)
        else: mov[i]=((A-an["d"])/2-x0(13),2*LIN+EXTRA)
    return mov
def original(FD=0): return {i:(0,(FD if i>=13 else 0)) for i in range(18)}
def separado(G=26,FD=0):
    return {i:((0 if i<=3 else G if i<=5 else 2*G if i<=12 else G),(FD if i>=13 else 0)) for i in range(18)}
def tres_lineas(G=26,LIN=82,EXTRA=14):
    w1=x1(3)-x0(0); w2=(x1(12)-x0(4))+G; w3=x1(17)-x0(13); A=max(w1,w2,w3); mov={}
    for i in range(18):
        if i<=3: mov[i]=((A-w1)/2-x0(0),0)
        elif i<=5: mov[i]=((A-w2)/2-x0(4),LIN)
        elif i<=12: mov[i]=((A-w2)/2-x0(4)+G,LIN)
        else: mov[i]=((A-w3)/2-x0(13),LIN+EXTRA)
    return mov
DISENOS={"1_original":original,"2_separado":separado,"3_tres-lineas":tres_lineas,"4_cuatro-lineas":cuatro_lineas,"5_una-linea":una_linea}
