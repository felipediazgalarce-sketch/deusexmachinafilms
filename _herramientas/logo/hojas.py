"""Hojas de contacto para cada formato/estilo de una carpeta de logos."""
import glob,os,sys
from PIL import Image, ImageDraw
raiz=sys.argv[1]
for fmt in sorted(d for d in os.listdir(raiz) if os.path.isdir(os.path.join(raiz,d))):
    for est in sorted(os.listdir(os.path.join(raiz,fmt))):
        car=os.path.join(raiz,fmt,est)
        if not os.path.isdir(car): continue
        fs=sorted(glob.glob(car+"/*.png"))
        if not fs: continue
        ims=[Image.open(f).convert("RGBA") for f in fs]; ar=max(i.height/i.width for i in ims)
        cols=3 if ar<0.2 else (4 if ar<0.45 else 6); tw=1560//cols; th=round(tw*ar)+18; rows=(len(fs)+cols-1)//cols
        oscuro=("oscuro" in est or "neon" in est)
        h=Image.new("RGB",(cols*tw,rows*th),(16,16,18) if oscuro else (236,233,229)); d=ImageDraw.Draw(h)
        for k,(f,im) in enumerate(zip(fs,ims)):
            im.thumbnail((tw-10,tw*3)); x=(k%cols)*tw+5; y=(k//cols)*th
            n=os.path.basename(f)[:-4]
            if not oscuro and ("blanco" in n or "blanca" in n and "fondo-oscuro" in n or "mate" in n): d.rectangle((x-5,y,x-5+tw,y+th),fill=(40,40,44))
            h.paste(im,(x,y),im); d.text((x,y+th-15),n,fill=(130,130,130))
        h.save(os.path.join(raiz,fmt,f"hoja_{est}.jpg"),quality=85)
print("hojas listas")
