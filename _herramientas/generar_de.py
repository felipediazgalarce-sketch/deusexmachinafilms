#!/usr/bin/env python3
"""Genera las versiones estaticas en aleman (/de/) y en español (/es/).

Uso (desde la raiz del repo):  python3 _herramientas/generar_de.py

- Toma cada pagina en ingles, traduce los textos con _herramientas/de.json
  (clave: frase en ingles, valor: frase en aleman; textos sin clave quedan igual);
  el español sale de traduccion.js (el mismo diccionario de siempre),
  cambia titulo y descripcion por las de META, agrega hreflang y canonical,
  y ajusta las rutas de imagenes/css/js (un nivel mas abajo).
- Tambien agrega los hreflang a las paginas en ingles y escribe sitemap.xml.
Hay que volver a correrlo cada vez que cambia una pagina en ingles.
"""
import json, re, os, html

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITIO = "https://deusexmachinafilms.art"
PAGINAS = ["", "short-films/", "music-video/", "collaborations/", "work-in-progress/", "about-us/",
           "the-session/"]

META = {
 "": ("dEUSeXmACHINA films — Videoproduktion, Tanzfilm & Musikvideos in Klagenfurt, Kärnten",
      "Filmproduktion von Felipe Díaz Galarce mit Sitz in Klagenfurt am Wörthersee (Kärnten, Österreich) und Chile: Tanzfilm, experimenteller Dokumentarfilm, hybride Fiktion und Musikvideos – gezeigt auf internationalen Filmfestivals.",
      "dEUSeXmACHINA films — Klagenfurt · Chile",
      "Tanzfilm, experimenteller Dokumentarfilm und Musikvideos aus Klagenfurt und Chile."),
 "short-films/": ("Kurzfilme — dEUSeXmACHINA films",
      "Kurzfilme von dEUSeXmACHINAfilms (Klagenfurt · Chile): EL CORAZÓN NO ES UNA BOMBA, EXPLORADORES DE LA REDONDA, MORAR, ECDISIS/LICUAR, ESCAPE, misoginia PANDORA und misoginia EVA. Credits, Besetzung und Festivals.", None, None),
 "music-video/": ("Musikvideos — dEUSeXmACHINA films",
      "Musikvideos von dEUSeXmACHINAfilms für SOL BUSTAMANTE, Oliver Aron, IVOLIER, Elías André, SUBE und Emmanuel Bermedo. Musikvideo-Produktion in Klagenfurt, Kärnten.", None, None),
 "collaborations/": ("Darstellende Künste — dEUSeXmACHINA films",
      "Kameraarbeit von Felipe Díaz Galarce für andere Künstler*innen: Tanz, Performance und Theater in Chile — TIBIA, PAISAJE LOA, MEMBRANA, Artidanza, Al Caer la Noche und F.A.S.E. 0.", None, None),
 "work-in-progress/": ("In Arbeit — dEUSeXmACHINA films",
      "Filme in Entwicklung und Postproduktion bei dEUSeXmACHINAfilms: HELIX EVOLUTION, VENUS IN VITRO und AMATEURS.", None, None),
 "about-us/": ("Über uns — dEUSeXmACHINA films",
      "dEUSeXmACHINAfilms, 2018 von Felipe Díaz Galarce gegründet: Tanzfilme, experimenteller Dokumentarfilm und Musikvideos, gezeigt auf mehr als 40 Festivals in 18 Ländern. Sitz in Klagenfurt, Kärnten.", None, None),
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
import subprocess
ES = json.loads(subprocess.check_output(["node", "-e",
    "global.window={}; require(process.argv[1]); process.stdout.write(JSON.stringify(window.ES))",
    os.path.join(RAIZ, "traduccion.js")]).decode("utf-8"))
META_ES = {
 "": ("dEUSeXmACHINA films — Cine de danza, documental y videoclips · Austria y Chile",
      "Productora de Felipe Díaz Galarce con base en Klagenfurt (Austria) y Chile: cine de danza, documental experimental, ficción híbrida y videoclips, exhibidos en más de 40 festivales de 18 países.",
      "dEUSeXmACHINA films — Klagenfurt · Chile", "Cine de danza, documental experimental y videoclips desde Klagenfurt y Chile."),
 "short-films/": ("Cortometrajes — dEUSeXmACHINA films",
      "Cortometrajes de dEUSeXmACHINAfilms: EL CORAZÓN NO ES UNA BOMBA, EXPLORADORES DE LA REDONDA, MORAR, ECDISIS/LICUAR, ESCAPE, misoginia PANDORA y misoginia EVA. Créditos, elenco y festivales.", None, None),
 "music-video/": ("Videoclips — dEUSeXmACHINA films",
      "Videoclips dirigidos y filmados por dEUSeXmACHINAfilms para SOL BUSTAMANTE, Oliver Aron, IVOLIER, Elías André, SUBE y Emmanuel Bermedo.", None, None),
 "collaborations/": ("Artes escénicas — dEUSeXmACHINA films",
      "Cámara y video de Felipe Díaz Galarce para danza, performance y teatro en Chile: TIBIA, PAISAJE LOA, MEMBRANA, Artidanza, Al Caer la Noche y F.A.S.E. 0.", None, None),
 "work-in-progress/": ("En desarrollo — dEUSeXmACHINA films",
      "Películas en desarrollo y postproducción de dEUSeXmACHINAfilms: HELIX EVOLUTION, VENUS IN VITRO y AMATEURS.", None, None),
 "about-us/": ("Nosotros — dEUSeXmACHINA films",
      "dEUSeXmACHINAfilms, fundada en 2018 por Felipe Díaz Galarce: cine de danza, documental experimental y videoclips, exhibidos en 18 países. Con base en Klagenfurt y Chile.", None, None),
 "the-session/": ("The Session — dEUSeXmACHINA films",
      "THE SESSION es una práctica audiovisual basada en el encuentro entre una persona real, un lugar real, una cámara, el movimiento y el tiempo. En la sesión sucede la película.",
      "THE SESSION — dEUSeXmACHINA films", "No creamos todo. Creamos las condiciones para que algo suceda."),
}
ACTIVO = re.compile(r'\.(css|js|png|jpe?g|svg|webp|gif|mp4|webm|ico|pdf)(\?[^"]*)?$', re.I)

def hreflang(p):
    return ('<link rel="alternate" hreflang="en" href="%s/%s">\n'
            '<link rel="alternate" hreflang="es" href="%s/es/%s">\n'
            '<link rel="alternate" hreflang="de" href="%s/de/%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s/%s">\n') % (SITIO, p, SITIO, p, SITIO, p, SITIO, p)

def poner_hreflang(t, p):
    t = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', '', t)
    return t.replace('</head>', hreflang(p) + '</head>', 1)

def traducir_textos(t, DIC):
    trozos = re.split(r'(<[^>]+>)', t)
    dentro = None
    for i, s in enumerate(trozos):
        if s.startswith('<'):
            m = re.match(r'<\s*(/?)\s*(script|style|title)\b', s, re.I)
            if m: dentro = None if m.group(1) else m.group(2).lower()
            continue
        if dentro or not s.strip(): continue
        clave = re.sub(r'\s+', ' ', html.unescape(s)).strip()
        if clave in DIC:
            ini = re.match(r'^\s*', s).group(0); fin = re.search(r'\s*$', s).group(0)
            trozos[i] = ini + html.escape(DIC[clave], quote=False) + fin
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

def meta(t, p, lang='de'):
    titulo, desc, ogt, ogd = (META if lang == 'de' else META_ES)[p]
    t = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(titulo, quote=False), t, 1, re.S)
    t = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), t, 1)
    if ogt: t = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(ogt), t, 1)
    if ogd: t = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(ogd), t, 1)
    url = '%s/%s/%s' % (SITIO, lang, p)
    t = re.sub(r'(<link rel="canonical" href=")[^"]*', lambda m: m.group(1) + url, t, 1)
    t = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + url, t, 1)
    # datos estructurados de video: las fichas apuntan a la pagina alemana
    t = t.replace('"url": "%s/%s#' % (SITIO, p), '"url": "%s/%s/%s#' % (SITIO, lang, p))
    if 'og:locale' not in t:
        t = t.replace('</head>', '<meta property="og:locale" content="%s">\n</head>' % ('de_AT' if lang == 'de' else 'es_CL'), 1)
    return t

for p in PAGINAS:
    ruta = os.path.join(RAIZ, p, "index.html")
    en = open(ruta, encoding="utf-8").read()
    en = poner_hreflang(en, p)
    open(ruta, "w", encoding="utf-8").write(en)
    for lang, DIC in (("de", DE), ("es", ES)):
        t = re.sub(r'<html lang="en"[^>]*>', '<html lang="%s" data-version="%s">' % (lang, lang), en, 1)
        t = meta(t, p, lang)
        t = rutas(traducir_textos(t, DIC))
        destino = os.path.join(RAIZ, lang, p, "index.html")
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        open(destino, "w", encoding="utf-8").write(t)
        print(lang + "/" + p)

urls = []
for p in PAGINAS:
    for base in ("", "es/", "de/"):
        urls.append('  <url><loc>%s/%s%s</loc>'
                    '<xhtml:link rel="alternate" hreflang="en" href="%s/%s"/>'
                    '<xhtml:link rel="alternate" hreflang="es" href="%s/es/%s"/>'
                    '<xhtml:link rel="alternate" hreflang="de" href="%s/de/%s"/></url>' % (SITIO, base, p, SITIO, p, SITIO, p, SITIO, p))
open(os.path.join(RAIZ, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    + "\n".join(urls) + "\n</urlset>\n")
open(os.path.join(RAIZ, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITIO)
