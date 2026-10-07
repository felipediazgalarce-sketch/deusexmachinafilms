import json,sys
sys.path.insert(0,".")
from gen import *
NEG,BLA,TUR,MEN,ROS="#0a0a0a","#ffffff","#0d9488","#3fe0c5","#ec4899"
lg=Logo(una_linea()); V={}
def neon(c,films_caja=True):
    f='''<filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b1"/><feGaussianBlur stdDeviation="7" result="b2"/>
<feMerge><feMergeNode in="b2"/><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''
    return lg.svg('<g filter="url(#g)">'+lg.cajas(f' fill="none" stroke="{c}" stroke-width="2.6"',films=films_caja)+lg.letras(BLA,c,films=c if films_caja else BLA,attrs_base=' opacity="0.92"')+'</g>',f)
V["a_v3_sin-films"]=lg.svg(lg.cajas(f' fill="{TUR}"')+lg.letras(NEG,NEG))
V["b_v3_films-en-caja"]=lg.svg(lg.cajas(f' fill="{TUR}"',films=True)+lg.letras(NEG,NEG))
V["c_v4_sin-films"]=lg.svg(lg.cajas(f' fill="{NEG}"')+lg.letras(NEG,TUR))
V["d_v4_films-en-caja"]=lg.svg(lg.cajas(f' fill="{NEG}"',films=True)+lg.letras(NEG,TUR,films=TUR))
V["e_negra-blanca_films-en-caja"]=lg.svg(lg.cajas(f' fill="{NEG}"',films=True)+lg.letras(NEG,BLA,films=BLA))
V["f_contorno-negro"]=lg.svg(lg.cajas(f' fill="none" stroke="{NEG}" stroke-width="2"',films=True)+lg.letras(NEG,NEG))
V["g_contorno-turquesa"]=lg.svg(lg.cajas(f' fill="none" stroke="{TUR}" stroke-width="2.2"',films=True)+lg.letras(NEG,TUR,films=TUR))
V["h_contorno-fino-turquesa_letra-negra"]=lg.svg(lg.cajas(f' fill="none" stroke="{TUR}" stroke-width="1.4"',films=True)+lg.letras(NEG,NEG))
V["i_neon-turquesa_films-en-caja"]=neon(MEN)
V["j_neon-rosa_films-en-caja"]=neon(ROS)
json.dump(V,open("prueba_films.json","w")); print(len(V),lg.tam())
