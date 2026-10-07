import json,sys
sys.path.insert(0,".")
from gen import *
NEG,BLA="#0a0a0a","#ffffff"
COL={"turquesa":"#0d9488","menta":"#3fe0c5","verde-agua":"#5eead4","esmeralda":"#059669","verde-lima":"#84cc16","verde-bosque":"#166534",
     "morado":"#7c3aed","lila":"#c4b0e8","azul":"#2563eb","celeste":"#38bdf8","rojo":"#dc2626","naranja":"#f97316","amarillo":"#facc15","rosa":"#ec4899"}
H={}; C={}
for dn,fn in DISENOS.items():
    lg=Logo(fn(FD=14)) if dn in ('1_original','2_separado') else Logo(fn())
    # --- estilo h: contorno fino de color, letras negras (fondo claro) o blancas (fondo oscuro)
    for n,c in list(COL.items())+[("negro",NEG)]:
        H[f"{dn}/fondo-claro/contorno-{n}"]=lg.svg(lg.cajas(f' fill="none" stroke="{c}" stroke-width="1.4"',films=True)+lg.letras(NEG,NEG))
    for n,c in list(COL.items())+[("blanco",BLA)]:
        H[f"{dn}/fondo-oscuro/contorno-{n}"]=lg.svg(lg.cajas(f' fill="none" stroke="{c}" stroke-width="1.4"',films=True)+lg.letras(BLA,BLA))
    # --- calados para video
    # cajas rellenas con la d, e, m recortada (el video se ve dentro de la letra)
    dem="".join(f'<path fill-rule="evenodd" d="{d}" fill="#000"/>' for l in lg.L if l["i"] in DEM for d in l["d"])
    def calado(caja,base):
        m=f'<mask id="k" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="5000" height="5000"><rect x="-2000" y="-2000" width="5000" height="5000" fill="#fff"/>{dem}</mask>'
        sin_dem=lg.letras(base,"none",films=base)
        return lg.svg(m+f'<g mask="url(#k)">'+lg.cajas(f' fill="{caja}"')+'</g>'+sin_dem)
    C[f"{dn}/1_caja-negra_letra-calada"]=calado(NEG,NEG)
    C[f"{dn}/2_caja-blanca_letra-calada_fondo-oscuro"]=calado(BLA,BLA)
    C[f"{dn}/3_caja-turquesa_letra-calada"]=calado("#0d9488",NEG)
    # mates (blanco sobre transparente) para "Mate de seguimiento" en Premiere
    C[f"{dn}/mate_d-e-m"]=lg.svg(lg.letras("none",BLA,films="none"))
    C[f"{dn}/mate_cajas"]=lg.svg(lg.cajas(f' fill="{BLA}"'))
    C[f"{dn}/mate_cajas-con-films"]=lg.svg(lg.cajas(f' fill="{BLA}"',films=True))
    C[f"{dn}/mate_todas-las-letras"]=lg.svg(lg.letras(BLA,BLA))
json.dump(H,open("h_colores.json","w")); json.dump(C,open("calados.json","w")); print(len(H),len(C))
