"""Logo dEUSeXmACHINA films con la fuente limpia: Avenir Black (la del logo original)."""
from fontTools.ttLib import TTCollection
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
FONT=TTCollection("/System/Library/Fonts/Avenir.ttc").fonts[2]   # Avenir Black
GS=FONT.getGlyphSet(); CMAP=FONT.getBestCmap(); UPM=FONT["head"].unitsPerEm; HMTX=FONT["hmtx"]
S=100; SF=0.62; TRACK_F=0.14; PAD=6
def glifo(ch,x,base,size):
    g=CMAP[ord(ch)]; s=size/UPM
    sp=SVGPathPen(GS); GS[g].draw(TransformPen(sp,(s,0,0,-s,x,base)))
    bp=BoundsPen(GS); GS[g].draw(TransformPen(bp,(s,0,0,-s,x,base)))
    return {"ch":ch,"d":sp.getCommands(),"bb":bp.bounds,"adv":HMTX[g][0]*s,"base":base,"t":(0,0)}
def linea(texto,x,base,size,track=0.0):
    out=[]
    for ch in texto:
        if ch==" ": x+=size*0.28; continue
        gl=glifo(ch,x,base,size); out.append(gl); x+=gl["adv"]+track*size
    return out
def mover(g,dx,dy):
    b=g["bb"]; t=g["t"]; return dict(g,bb=(b[0]+dx,b[1]+dy,b[2]+dx,b[3]+dy),t=(t[0]+dx,t[1]+dy),base=g["base"]+dy)
def centrar(gls,cx):
    x0=min(g["bb"][0] for g in gls); x1=max(g["bb"][2] for g in gls); return [mover(g,cx-(x0+x1)/2,0) for g in gls]
def path(g,fill,extra=""):
    t=g["t"]; tr=f' transform="translate({t[0]:.2f} {t[1]:.2f})"' if t!=(0,0) else ""
    return f'<path d="{g["d"]}" fill="{fill}"{tr}{extra}/>'
# ---- disenos: lista de glifos en orden d E U S e X m A C H I N A f i l m s
def cuatro_lineas(LIN=0.88,GF=0.66):
    lineas=[linea(t,0,S*(0.75+k*LIN),S) for k,t in enumerate(["dEUS","eX","mACHINA"])]
    lineas.append(linea("films",0,S*(0.75+2*LIN)+S*GF,S*SF,TRACK_F))
    ancho=max(max(x["bb"][2] for x in l)-min(x["bb"][0] for x in l) for l in lineas)
    return [g for l in lineas for g in centrar(l,ancho/2)]
def una_linea(G=0.30):
    out=[]; x=0
    for t in ["dEUS","eX","mACHINA"]:
        g=linea(t,x,S*0.75,S); out+=g; x=g[-1]["bb"][0]-g[-1]["bb"][0]+x+sum(0 for _ in g)
        x=g[-1]["t"][0]+g[-1]["bb"][2]+S*G
    out+=linea("films",x+S*0.04,S*0.75,S*SF,TRACK_F)
    return out
DEM=(0,4,6); FILMS=(13,14,15,16,17)
def rect_dem(gls):
    d=gls[0]; alto=d["base"]-d["bb"][1]          # altura de la d (ascendente) = alto comun de las cajas
    out=[]
    for i in DEM:
        g=gls[i]; b=g["bb"]; out.append((b[0]-PAD, g["base"]-alto-PAD, b[2]-b[0]+2*PAD, alto+2*PAD))
    return out
def rect_films(gls):
    fs=[gls[i] for i in FILMS]; base=fs[0]["base"]; top=min(g["bb"][1] for g in fs)
    x0=fs[0]["bb"][0]-PAD*1.4; x1=fs[-1]["bb"][2]+PAD*1.4
    return (x0, top-PAD, x1-x0, base-top+2*PAD)
def caja_svg(r,attrs): return f'<rect x="{r[0]:.2f}" y="{r[1]:.2f}" width="{r[2]:.2f}" height="{r[3]:.2f}"{attrs}/>'
def limites(gls,rects=()):
    xs=[];ys=[]
    for g in gls: b=g["bb"]; xs+=[b[0],b[2]]; ys+=[b[1],b[3]]
    for r in rects: xs+=[r[0],r[0]+r[2]]; ys+=[r[1],r[1]+r[3]]
    return min(xs),min(ys),max(xs),max(ys)
def svg(gls,cuerpo,rects=(),M=8,defs=""):
    x0,y0,x1,y1=limites(gls,rects)
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0-M:.2f} {y0-M:.2f} {x1-x0+2*M:.2f} {y1-y0+2*M:.2f}"><defs>{defs}</defs>{cuerpo}</svg>'
def _films_centrado(base,ancho_obj,cx):
    # films con el tracking necesario para ocupar ancho_obj, centrado en cx
    g=linea("films",0,base,S*SF,0); w=g[-1]["bb"][2]-g[0]["bb"][0]
    tr=max(0.0,(ancho_obj-w)/4/(S*SF)); g=linea("films",0,base,S*SF,tr)
    return centrar(g,cx)
def original(GF=0.66):
    l1=linea("dEUSeXmACHINA",0,S*0.75,S); W=l1[-1]["bb"][2]-l1[0]["bb"][0]
    return l1+_films_centrado(S*(0.75+GF),W*0.48,(l1[0]["bb"][0]+l1[-1]["bb"][2])/2)
def separado(GF=0.66,G=0.30):
    out=[]; x=0
    for t in ["dEUS","eX","mACHINA"]:
        g=linea(t,x,S*0.75,S); out+=g; x=g[-1]["bb"][2]+S*G
    W=out[-1]["bb"][2]-out[0]["bb"][0]
    return out+_films_centrado(S*(0.75+GF),W*0.42,(out[0]["bb"][0]+out[-1]["bb"][2])/2)
def tres_lineas(LIN=0.88,G=0.30,GF=0.66):
    l1=linea("dEUS",0,S*0.75,S)
    g1=linea("eX",0,S*(0.75+LIN),S); x=g1[-1]["bb"][2]+S*G; g2=linea("mACHINA",x,S*(0.75+LIN),S); l2=g1+g2
    l3=linea("films",0,S*(0.75+LIN)+S*GF,S*SF,TRACK_F)
    A=max(max(g["bb"][2] for g in l)-min(g["bb"][0] for g in l) for l in (l1,l2,l3))
    return [g for l in (l1,l2,l3) for g in centrar(l,A/2)]
FORMATOS={"1_original":original,"2_separado":separado,"3_tres-lineas":tres_lineas,"4_cuatro-lineas":cuatro_lineas,"5_una-linea":una_linea}
