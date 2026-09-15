/* dEUSeXmACHINA films — comportamiento comun a las 6 paginas */
(function () {
  "use strict";

  // Menu movil
  var burger = document.querySelector(".burger"),
      menu   = document.getElementById("menu");
  if (burger && menu) {
    burger.addEventListener("click", function () {
      var abierto = menu.classList.toggle("open");
      burger.setAttribute("aria-expanded", abierto ? "true" : "false");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.tagName === "A") {
        menu.classList.remove("open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Linea inferior de la cabecera al hacer scroll
  // La cabecera se esconde al bajar y reaparece al devolver el scroll.
  var bar = document.querySelector("header");
  if (bar) {
    var ultimo = 0;
    addEventListener("scroll", function () {
      var y = scrollY;
      if (y > 100 && y > ultimo + 4) {
        bar.classList.add("oculta");                 // bajando: fuera
      } else if (y < ultimo - 4 || y <= 100) {
        bar.classList.remove("oculta");              // subiendo: vuelve
      }
      ultimo = y;
    }, { passive: true });
  }

  // Icono de play, inyectado para no repetir el SVG en cada ficha
  var SVG = '<svg viewBox="0 0 64 64" aria-hidden="true">'
          + '<circle class="aro" cx="32" cy="32" r="24" fill="none" stroke="currentColor" stroke-width="1"/>'
          + '<circle class="luz" cx="32" cy="32" r="24" fill="none" stroke-width="1.4"'
          + ' transform="rotate(-90 32 32)"/>'
          + '<path class="punta" d="M27 23.5 L43 32 L27 40.5 Z" fill="currentColor"/></svg>';

  // Los videos se cargan solo al pulsarlos: la pagina no arranca con 17 iframes.
  function incrustar(caja, id, titulo) {
    var f = document.createElement("iframe");
    f.src = caja.dataset.vimeo
          ? "https://player.vimeo.com/video/" + caja.dataset.vimeo + "?autoplay=1&dnt=1"
          : "https://www.youtube-nocookie.com/embed/" + id
            + "?autoplay=1&rel=0&modestbranding=1&playsinline=1";
    f.title = titulo || "Video";
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    caja.innerHTML = "";
    caja.appendChild(f);
  }

  // Bloques de video con poster (fichas completas y destacado)
  Array.prototype.forEach.call(document.querySelectorAll(".ratio[data-video], .ratio[data-vimeo]"), function (caja) {
    var p = document.createElement("span");
    p.className = "play";
    p.innerHTML = SVG;
    caja.appendChild(p);
    caja.setAttribute("role", "button");
    caja.setAttribute("tabindex", "0");
    caja.setAttribute("aria-label", "Play " + (caja.dataset.titulo || ""));
    function abrir() { incrustar(caja, caja.dataset.video, caja.dataset.titulo); }
    caja.addEventListener("click", abrir);
    caja.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") { e.preventDefault(); abrir(); }
    });
  });

  // Fichas de la grilla de portada
  Array.prototype.forEach.call(document.querySelectorAll("button.work"), function (b) {
    var p = b.querySelector(".play");
    if (p) p.innerHTML = SVG;
    b.addEventListener("click", function () {
      var caja = document.createElement("div");
      caja.className = "ratio";
      b.parentNode.insertBefore(caja, b);
      var titulo = b.querySelector("h3").textContent;
      b.querySelector(".thumb").remove();
      incrustar(caja, b.dataset.video, titulo);
    });
  });

  // Año del pie
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();


/* ============ IDIOMA: ingles <-> español (+ aleman en /de/) ============
   El sitio se escribe en ingles. La traduccion vive en traduccion.js,
   como pares "frase en ingles": "frase en español".
   Para añadir texto nuevo basta con sumar el par a ese archivo.
   =================================================== */
(function(){
  var IDIOMA = "dxm-idioma";
  var botones = document.querySelectorAll(".bandera-btn");
  if (!botones.length) return;

  function textos(){
    var salida = [], saltar = {SCRIPT:1, STYLE:1, NOSCRIPT:1};
    var it = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function(n){
        if (saltar[n.parentNode.nodeName]) return NodeFilter.FILTER_REJECT;
        return n.nodeValue.trim() ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var n; while ((n = it.nextNode())) salida.push(n);
    return salida;
  }

  /* version alemana: son paginas estaticas bajo /de/ (para que Google las indexe).
     Desde /de/ el ingles y el español vuelven a la pagina equivalente de la raiz. */
  var enAleman = document.documentElement.getAttribute("data-version") === "de";
  function irA(ruta){ location.href = ruta + location.hash; }
  function rutaRaiz(){ return location.pathname.replace(/^\/de(\/|$)/, "/"); }
  function rutaAleman(){ return "/de" + location.pathname; }

  function aplicar(lang){
    var dic = window.ES || {};
    textos().forEach(function(n){
      if (n.__en === undefined) n.__en = n.nodeValue;          // guarda el original
      var bruto = n.__en;
      var clave = bruto.replace(/\s+/g, " ").trim();
      if (lang === "es" && dic[clave]) {
        /* se conservan los espacios de los bordes: el texto puede venir con
           saltos de linea o espacios dobles del maquetado */
        n.nodeValue = bruto.match(/^\s*/)[0] + dic[clave] + bruto.match(/\s*$/)[0];
      } else {
        n.nodeValue = bruto;
      }
    });
    document.documentElement.lang = lang;
    botones.forEach(function(x){ x.setAttribute("aria-pressed", x.dataset.lang === lang ? "true" : "false"); });
    try { localStorage.setItem(IDIOMA, lang); } catch(e){}
  }

  var guardado = "en";
  try { guardado = localStorage.getItem(IDIOMA) || "en"; } catch(e){}

  if (enAleman) {
    botones.forEach(function(x){ x.setAttribute("aria-pressed", x.dataset.lang === "de" ? "true" : "false"); });
  } else if (guardado === "de") {
    location.replace(rutaAleman() + location.hash);
  } else if (guardado === "es") aplicar("es"); else aplicar("en");

  botones.forEach(function(x){ x.addEventListener("click", function(){
    var lang = x.dataset.lang;
    try { localStorage.setItem(IDIOMA, lang); } catch(e){}
    if (lang === "de") { if (!enAleman) irA(rutaAleman()); }
    else if (enAleman) irA(rutaRaiz());
    else aplicar(lang);
  }); });
})();


/* ============ Numero de serie (contador de visitas) ============
   Cuenta una visita por navegador y dia, en cualquier pagina.
   El numero vive en el servidor de felipediazgalarce.com y solo
   se muestra al pie del home. */
(function(){
  var hoy = new Date().toISOString().slice(0, 10), sumar = true;
  try { sumar = localStorage.getItem("dxm-visto") !== hoy; localStorage.setItem("dxm-visto", hoy); } catch(e){}
  fetch("https://felipediazgalarce.com/contador.php?sitio=dxm" + (sumar ? "&accion=sumar" : ""), {cache:"no-store"})
    .then(function(r){ return r.json(); })
    .then(function(d){
      var el = document.getElementById("serie");
      if (el && d && typeof d.n === "number") el.textContent = "N.º " + String(d.n).padStart(4, "0");
    })
    .catch(function(){});
})();


/* ============ Visor de miniaturas (catalogo CinemaChile) ============ */
(function(){
  document.querySelectorAll(".miniaturas a, a.tarjeta-cc").forEach(function(a){
    /* la tarjeta vive dentro del bloque del video: que no lo reproduzca */
    a.addEventListener("keydown", function(ev){ ev.stopPropagation(); });
    a.addEventListener("click", function(ev){
      ev.preventDefault();
      ev.stopPropagation();
      var visor = document.createElement("div");
      visor.className = "visor";
      visor.innerHTML = '<img alt="">';
      visor.firstChild.src = a.href;
      visor.firstChild.alt = a.querySelector("img").alt;
      function cerrar(){ visor.remove(); document.removeEventListener("keydown", tecla); }
      function tecla(e){ if (e.key === "Escape") cerrar(); }
      visor.addEventListener("click", cerrar);
      document.addEventListener("keydown", tecla);
      document.body.appendChild(visor);
    });
  });
})();


/* ============ Laureles dibujados: las ramas abrazan el texto ============
   Un texto que se parte en varias lineas ocupa todo su ancho maximo aunque
   sus lineas sean mas cortas; aqui se ajusta al ancho de la linea mas larga
   para que las ramas queden pegadas a las letras. */
(function(){
  var textos = document.querySelectorAll(".sello .st");
  if (!textos.length) return;
  function ajustar(){
    textos.forEach(function(st){
      st.style.width = "";
      var r = document.createRange(), ancho = 0;
      st.querySelectorAll("em, b, i").forEach(function(el){
        if (el.offsetParent === null) return;          // oculto (celular)
        r.selectNodeContents(el);
        Array.prototype.forEach.call(r.getClientRects(), function(x){ ancho = Math.max(ancho, x.width); });
      });
      if (ancho) st.style.width = Math.ceil(ancho + 1) + "px";
    });
  }
  var t;
  addEventListener("resize", function(){ clearTimeout(t); t = setTimeout(ajustar, 150); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(ajustar);
  addEventListener("load", ajustar);
  ajustar();
})();
