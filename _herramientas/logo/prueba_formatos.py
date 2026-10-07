import json,sys
sys.path.insert(0,".")
from gen import *
NEG,BLA,TUR,MEN,ROS="#0a0a0a","#ffffff","#0d9488","#3fe0c5","#ec4899"
V={}
for dn,fn in DISENOS.items():
  lg=Logo(fn()); P={}
  lgF=Logo(fn(FD=14)) if dn in ('1_original','2_separado') else lg
  def neon(c,films_caja=True,lg=lgF):
      f='''<filter id="g" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b1"/><feGaussianBlur stdDeviation="7" result="b2"/>
  <feMerge><feMergeNode in="b2"/><feMergeNode in="b2"/><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''
      return lg.svg('<g filter="url(#g)">'+lg.cajas(f' fill="none" stroke="{c}" stroke-width="2.6"',films=films_caja)+lg.letras(BLA,c,films=c if films_caja else BLA,attrs_base=' opacity="0.92"')+'</g>',f)
  P["a_v3_sin-films"]=lg.svg(lg.cajas(f' fill="{TUR}"')+lg.letras(NEG,NEG))
  P["b_v3_films-en-caja"]=lgF.svg(lgF.cajas(f' fill="{TUR}"',films=True)+lgF.letras(NEG,NEG))
  P["c_v4_sin-films"]=lg.svg(lg.cajas(f' fill="{NEG}"')+lg.letras(NEG,TUR))
  P["d_v4_films-en-caja"]=lgF.svg(lgF.cajas(f' fill="{NEG}"',films=True)+lgF.letras(NEG,TUR,films=TUR))
  P["e_negra-blanca_films-en-caja"]=lgF.svg(lgF.cajas(f' fill="{NEG}"',films=True)+lgF.letras(NEG,BLA,films=BLA))
  P["f_contorno-negro"]=lgF.svg(lgF.cajas(f' fill="none" stroke="{NEG}" stroke-width="2"',films=True)+lgF.letras(NEG,NEG))
  P["g_contorno-turquesa"]=lgF.svg(lgF.cajas(f' fill="none" stroke="{TUR}" stroke-width="2.2"',films=True)+lgF.letras(NEG,TUR,films=TUR))
  P["h_contorno-fino-turquesa_letra-negra"]=lgF.svg(lgF.cajas(f' fill="none" stroke="{TUR}" stroke-width="1.4"',films=True)+lgF.letras(NEG,NEG))
  P["i_neon-turquesa_films-en-caja"]=neon(MEN)
  P["j_neon-rosa_films-en-caja"]=neon(ROS)
  for k,v in P.items(): V[dn+'/'+k]=v
json.dump(V,open("prueba_formatos.json","w")); print(len(V))
