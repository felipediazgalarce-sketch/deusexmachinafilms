"""Icono del sitio: letra blanca en Futura Medium sobre turquesa. Uso: python3 _herramientas/icono.py d [carpeta_salida]"""
import sys
from PIL import Image, ImageFont, ImageDraw
letra=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else '.'
BG=(13,148,136); N=1024; ALTO=203*2; CY=255.5*2
def maestro():
    f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Futura.ttc',800,index=0)
    l,t,r,b=f.getbbox(letra); s=ALTO/(b-t); f=ImageFont.truetype('/System/Library/Fonts/Supplemental/Futura.ttc',int(800*s),index=0)
    l,t,r,b=f.getbbox(letra); im=Image.new('RGB',(N,N),BG); d=ImageDraw.Draw(im)
    d.text((N/2-(l+r)/2, CY-(t+b)/2),letra,font=f,fill=(255,255,255)); return im
m=maestro()
for nombre,t in [('icon-512.png',512),('icon-192.png',192),('apple-touch-icon.png',180),('favicon-32.png',32)]:
    m.resize((t,t),Image.LANCZOS).save(out+'/'+nombre)
m.resize((48,48),Image.LANCZOS).save(out+'/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
