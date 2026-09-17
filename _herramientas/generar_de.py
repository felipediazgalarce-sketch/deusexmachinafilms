#!/usr/bin/env python3
"""Genera la version alemana estatica del sitio en /de/.

Uso (desde la raiz del repo):  python3 _herramientas/generar_de.py

- Toma cada pagina en ingles, traduce los textos con _herramientas/de.json
  (clave: frase en ingles, valor: frase en aleman; textos sin clave quedan igual),
  cambia titulo y descripcion por las de META, agrega hreflang y canonical,
  y ajusta las rutas de imagenes/css/js (un nivel mas abajo).
- Tambien agrega los hreflang a las paginas en ingles y escribe sitemap.xml.
Hay que volver a correrlo cada vez que cambia una pagina en ingles.
"""
import json, re, os, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://deusexmachinafilms.art"
PAGINAS = ["", "short-films/", "music-video/", "cinematography/", "work-in-progress/", "about-us/",
           "contacts/", "the-session/", "the-session/marlie-amsterdam/", "the-session/nina-valdivia/"]

META = {
 "": ("dEUSeXmACHINA films — Videoproduktion, Tanzfilm & Musikvideos in Klagenfurt, Kärnten",
      "Filmproduktion von Felipe Díaz Galarce mit Sitz in Klagenfurt am Wörthersee (Kärnten, Österreich) und Chile: Tanzfilm, experimenteller Dokumentarfilm, hybride Fiktion und Musikvideos – gezeigt auf internationalen Filmfestivals.",
      "dEUSeXmACHINA films — Klagenfurt · Chile",
      "Tanzfilm, experimenteller Dokumentarfilm und Musikvideos aus Klagenfurt und Chile."),
 "short-films/": ("Kurzfilme — dEUSeXmACHINA films",
      "Kurzfilme von dEUSeXmACHINAfilms (Klagenfurt · Chile): EL CORAZÓN NO ES UNA BOMBA, EXPLORADORES DE LA REDONDA, MORAR, ECDISIS/LICUAR, ESCAPE und misoginia PANDORA. Credits, Besetzung und Festivals.", None, None),
 "music-video/": ("Musikvideos — dEUSeXmACHINA films",
      "Musikvideos von dEUSeXmACHINAfilms für SOL BUSTAMANTE, Oliver Aron, IVOLIER, Elías André und SUBE. Musikvideo-Produktion in Klagenfurt, Kärnten.", None, None),
 "cinematography/": ("Kamera — dEUSeXmACHINA films",
      "Kameraarbeit von Felipe Díaz Galarce für andere Künstler*innen: Tanz, Performance und Theater in Chile — TIBIA, MEMBRANA, Al Caer la Noche, Artidanza und F.A.S.E. 0.", None, None),
 "work-in-progress/": ("In Arbeit — dEUSeXmACHINA films",
      "Filme in Entwicklung und Postproduktion bei dEUSeXmACHINAfilms: MEDUSA OF STONE, HELIX EVOLUTION, VENUS IN VITRO und AMATEURS.", None, None),
 "about-us/": ("Über uns — dEUSeXmACHINA films",
      "dEUSeXmACHINAfilms, 2018 von Felipe Díaz Galarce gegründet: Tanzfilme, experimenteller Dokumentarfilm und Musikvideos, gezeigt in dreizehn Ländern. Sitz in Klagenfurt, Kärnten.", None, None),
 "contacts/": ("Kontakt — dEUSeXmACHINA films",
      "Kontakt zu dEUSeXmACHINAfilms in Klagenfurt (Kärnten, Österreich) und Chile – für Kooperationen, Festivals, Vorführungen und Auftragsproduktionen.", None, None),
 "the-session/": ("The Session — dEUSeXmACHINA films",
      "THE SESSION ist eine audiovisuelle Praxis, die auf der Begegnung zwischen einer realen Person, einem realen Ort, einer Kamera, Bewegung und Zeit beruht. In der Session entsteht der Film.",
      "THE SESSION — dEUSeXmACHINA films",
      "Wir erschaffen nicht alles. Wir schaffen die Bedingungen, damit etwas geschieht."),
 "the-session/marlie-amsterdam/": ("The Session — Marlie, Amsterdam",
      "THE SESSION — Marlie, Amsterdam. Eine Begegnung zwischen einer Tänzerin, einer Brücke in Amsterdam und einer Kamera in Bewegung.",
      "THE SESSION — Marlie, Amsterdam", "Ein Mensch betritt einen Ort. Die Kamera beginnt sich zu bewegen."),
 "the-session/nina-valdivia/": ("The Session — Nina, Valdivia",
      "THE SESSION — Nina, Valdivia. Eine Begegnung zwischen einer Tänzerin, einem Wald im Süden Chiles und einer Kamera in Bewegung.",
      "THE SESSION — Nina, Valdivia", "Ein Mensch betritt einen Ort. Die Kamera beginnt sich zu bewegen."),
}

DE = json.load(open(os.path.join(RAIZ, "_herramientas", "de.json"), encoding="utf-8"))
ACTIVO = re.compile(r'\.(css|js|png|jpe?g|svg|webp|gif|mp4|webm|ico|pdf)(\?[^"]*)?$', re.I)

def hreflang(p):
    return ('<link rel="alternate" hreflang="en" href="%s/%s">\n'
            '<link rel="alternate" hreflang="de" href="%s/de/%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s/%s">\n') % (SITIO, p, SITIO, p, SITIO, p)

def poner_hreflang(t, p):
    t = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', '', t)
    return t.replace('</head>', hreflang(p) + '</head>', 1)

def traducir_textos(t):
    trozos = re.split(r'(<[^>]+>)', t)
    dentro = None
    for i, s in enumerate(trozos):
        if s.startswith('<'):
            m = re.match(r'<\s*(/?)\s*(script|style|title)\b', s, re.I)
            if m: dentro = None if m.group(1) else m.group(2).lower()
            continue
        if dentro or not s.strip(): continue
        clave = re.sub(r'\s+', ' ', html.unescape(s)).strip()
        if clave in DE:
            ini = re.match(r'^\s*', s).group(0); fin = re.search(r'\s*$', s).group(0)
            trozos[i] = ini + html.escape(DE[clave], quote=False) + fin
    return ''.join(trozos)

def rutas(t):
    def fix(m):
        attr, url = m.group(1), m.group(2)
        if re.match(r'^(https?:|mailto:|tel:|#|/|data:)', url): return m.group(0)
        if ACTIVO.search(url): return '%s="../%s"' % (attr, url)
        return m.group(0)
    t = re.sub(r'\b(src|href|poster)="([^"]*)"', fix, t)
    # imagenes dentro de estilos en linea (laureles originales)
    return re.sub(r'url\((?!https?:|data:|/)([^)]*)\)', lambda m: 'url(../%s)' % m.group(1), t)

def meta(t, p):
    titulo, desc, ogt, ogd = META[p]
    t = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(titulo, quote=False), t, 1, re.S)
    t = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), t, 1)
    if ogt: t = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(ogt), t, 1)
    if ogd: t = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(ogd), t, 1)
    url = '%s/de/%s' % (SITIO, p)
    t = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, t, 1)
    t = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, t, 1)
    if 'og:locale' not in t:
        t = t.replace('</head>', '<meta property="og:locale" content="de_AT">\n</head>', 1)
    return t

for p in PAGINAS:
    ruta = os.path.join(RAIZ, p, "index.html")
    en = open(ruta, encoding="utf-8").read()
    en = poner_hreflang(en, p)
    open(ruta, "w", encoding="utf-8").write(en)
    de = re.sub(r'<html lang="en"[^>]*>', '<html lang="de" data-version="de">', en, 1)
    de = meta(de, p)
    de = rutas(traducir_textos(de))
    destino = os.path.join(RAIZ, "de", p, "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    open(destino, "w", encoding="utf-8").write(de)
    print("de/" + p)

urls = []
for p in PAGINAS:
    for base in ("", "de/"):
        urls.append('  <url><loc>%s/%s%s</loc>'
                    '<xhtml:link rel="alternate" hreflang="en" href="%s/%s"/>'
                    '<xhtml:link rel="alternate" hreflang="de" href="%s/de/%s"/></url>' % (SITIO, base, p, SITIO, p, SITIO, p))
open(os.path.join(RAIZ, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "\n".join(urls) + "\n</urlset>\n")
open(os.path.join(RAIZ, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITIO)
