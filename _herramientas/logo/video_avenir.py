import json,sys,random
sys.path.insert(0,".")
from gen2 import *
NEG,BLA,TUR="#0a0a0a","#ffffff","#0d9488"
COL={"turquesa":"#0d9488","menta":"#3fe0c5","verde-agua":"#5eead4","esmeralda":"#059669","verde-lima":"#84cc16","verde-bosque":"#166534",
     "morado":"#7c3aed","lila":"#c4b0e8","azul":"#2563eb","celeste":"#38bdf8","rojo":"#dc2626","naranja":"#f97316","amarillo":"#facc15","rosa":"#ec4899"}
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c:c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
    return .2126*f(r)+.7152*f(g)+.0722*f(b)
def contra(c): return NEG if lum(c)>0.22 else BLA
V={}
FMT=dict(FORMATOS); FMT['3_tres-lineas']=lambda:tres_lineas(LIN=0.98,GF=0.76); FMT['4_cuatro-lineas']=lambda:cuatro_lineas(LIN=0.98,GF=0.76)
for fn,lay in FMT.items():
    g=lay(); rd=rect_dem(g); rf=rect_films(g); todas=rd+[rf]
    def letras(base,dem=None,films=None,extra=""):
        dem=dem or base; films=films or base; out=""
        for k,gl in enumerate(g):
            c=dem if k in DEM else (films if k in FILMS else base)
            out+=path(gl,c,extra)
        return out
    cajas=lambda rs,at:"".join(caja_svg(r,at) for r in rs)
    P=lambda k,cuerpo,rects=(),defs="":V.__setitem__(f"{fn}/{k}",svg(g,cuerpo,rects,M=14,defs=defs))
    # 01 limpio
    P("01_limpio/negro",letras(NEG)); P("01_limpio/blanco",letras(BLA))
    # 02 contorno fino (estilo h)
    for n,c in list(COL.items())+[("negro",NEG)]:
        P(f"02_contorno-fino_fondo-claro/contorno-{n}",cajas(todas,f' fill="none" stroke="{c}" stroke-width="1.6"')+letras(NEG),todas)
    for n,c in list(COL.items())+[("blanco",BLA)]:
        P(f"03_contorno-fino_fondo-oscuro/contorno-{n}",cajas(todas,f' fill="none" stroke="{c}" stroke-width="1.6"')+letras(BLA),todas)
    # 04 cajas rellenas
    P("04_cajas/1_caja-negra_letra-blanca",cajas(rd,f' fill="{NEG}"')+letras(NEG,BLA),rd)
    P("04_cajas/2_caja-turquesa_letra-blanca",cajas(rd,f' fill="{TUR}"')+letras(NEG,BLA),rd)
    P("04_cajas/3_caja-turquesa_letra-negra",cajas(rd,f' fill="{TUR}"')+letras(NEG),rd)
    P("04_cajas/4_caja-negra_letra-turquesa",cajas(rd,f' fill="{NEG}"')+letras(NEG,TUR),rd)
    P("04_cajas/5_films-en-caja_negra-blanca",cajas(todas,f' fill="{NEG}"')+letras(NEG,BLA,BLA),todas)
    P("04_cajas/6_films-en-caja_turquesa-negra",cajas(todas,f' fill="{TUR}"')+letras(NEG),todas)
    P("04_cajas/7_films-en-caja_negra-turquesa",cajas(todas,f' fill="{NEG}"')+letras(NEG,TUR,TUR),todas)
    # 05 neon (fondo oscuro)
    glow='''<filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b1"/><feGaussianBlur stdDeviation="7" result="b2"/><feMerge><feMergeNode in="b2"/><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''
    for n in ["turquesa","menta","rosa","morado","azul","amarillo","rojo","naranja"]:
        c=COL[n]; P(f"05_neon/neon-{n}",'<g filter="url(#g)">'+cajas(todas,f' fill="none" stroke="{c}" stroke-width="2.6"')+letras(BLA,c,c,' opacity="0.95"')+'</g>',todas,glow)
    # 06 calados y mates
    demk="".join(path(gl,"#000") for k,gl in enumerate(g) if k in DEM)
    mk=f'<mask id="k" maskUnits="userSpaceOnUse" x="-3000" y="-3000" width="8000" height="8000"><rect x="-3000" y="-3000" width="8000" height="8000" fill="#fff"/>{demk}</mask>'
    resto=lambda c:"".join(path(gl,c) for k,gl in enumerate(g) if k not in DEM)
    P("06_calados/1_caja-negra_letra-calada",mk+'<g mask="url(#k)">'+cajas(rd,f' fill="{NEG}"')+'</g>'+resto(NEG),rd)
    P("06_calados/2_caja-blanca_letra-calada_fondo-oscuro",mk+'<g mask="url(#k)">'+cajas(rd,f' fill="{BLA}"')+'</g>'+resto(BLA),rd)
    P("06_calados/3_caja-turquesa_letra-calada",mk+'<g mask="url(#k)">'+cajas(rd,f' fill="{TUR}"')+'</g>'+resto(NEG),rd)
    P("06_calados/mate_d-e-m","".join(path(gl,BLA) for k,gl in enumerate(g) if k in DEM),todas)
    P("06_calados/mate_cajas",cajas(rd,f' fill="{BLA}"'),todas)
    P("06_calados/mate_cajas-con-films",cajas(todas,f' fill="{BLA}"'),todas)
    P("06_calados/mate_todas-las-letras",letras(BLA),todas)
    # 07 texturas: crayon, cromo, papel
    cray=lambda s:f'''<filter id="cr" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="{s}" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" result="d"/><feTurbulence type="fractalNoise" baseFrequency="1.6 0.25" numOctaves="2" seed="{s+5}" result="t"/><feColorMatrix in="t" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 1.55" result="h"/><feComposite in="d" in2="h" operator="in"/></filter>'''
    for n in ["turquesa","menta","rosa","amarillo"]:
        P(f"07_texturas/crayon-{n}",'<g filter="url(#cr)">'+cajas(rd,f' fill="{COL[n]}"')+'</g>'+letras(NEG),rd,cray(3))
    crom='''<linearGradient id="cm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f8fafc"/><stop offset=".22" stop-color="#9ca3af"/><stop offset=".45" stop-color="#ffffff"/><stop offset=".5" stop-color="#4b5563"/><stop offset=".62" stop-color="#d1d5db"/><stop offset=".85" stop-color="#6b7280"/><stop offset="1" stop-color="#e5e7eb"/></linearGradient>'''
    P("07_texturas/cromo_cajas",cajas(rd,' fill="url(#cm)"')+letras(NEG),rd,crom)
    P("07_texturas/cromo_letras_fondo-oscuro",cajas(rd,f' fill="{NEG}"')+letras(BLA,"url(#cm)"),rd,crom)
    pap=lambda s:f'''<filter id="pp" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency="0.035 0.6" numOctaves="4" seed="{s}" result="f"/><feColorMatrix in="f" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .35 0" result="fa"/><feComposite in="fa" in2="SourceAlpha" operator="in" result="fc"/><feTurbulence type="turbulence" baseFrequency="0.25" numOctaves="2" seed="{s+2}" result="b"/><feDisplacementMap in="SourceGraphic" in2="b" scale="2.2" result="c"/><feMerge result="h"><feMergeNode in="c"/><feMergeNode in="fc"/></feMerge><feDropShadow in="h" dx="1.6" dy="2.2" stdDeviation="1.6" flood-color="#000" flood-opacity=".35"/></filter>'''
    random.seed(5)
    def cajas_rot(rs,at):
        out=""
        for r in rs:
            a=random.uniform(-2.5,2.5); out+=f'<rect x="{r[0]:.2f}" y="{r[1]:.2f}" width="{r[2]:.2f}" height="{r[3]:.2f}"{at} transform="rotate({a:.2f} {r[0]+r[2]/2:.1f} {r[1]+r[3]/2:.1f})"/>'
        return out
    for n,c in [("turquesa",COL["turquesa"]),("menta",COL["menta"]),("amarillo",COL["amarillo"]),("kraft","#c8a46e")]:
        P(f"07_texturas/papel-{n}",'<g filter="url(#pp)">'+cajas_rot(rd,f' fill="{c}"')+'</g>'+letras(NEG),rd,pap(1))
json.dump(V,open("/tmp/video_avenir.json","w")); print(len(V))
