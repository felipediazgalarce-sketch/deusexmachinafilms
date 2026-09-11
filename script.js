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
    f.src = "https://www.youtube-nocookie.com/embed/" + id
          + "?autoplay=1&rel=0&modestbranding=1&playsinline=1";
    f.title = titulo || "Video";
    f.allow = "autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.allowFullscreen = true;
    caja.innerHTML = "";
    caja.appendChild(f);
  }

  // Bloques de video con poster (fichas completas y destacado)
  Array.prototype.forEach.call(document.querySelectorAll(".ratio[data-video]"), function (caja) {
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


/* ============ IDIOMA: ingles <-> español ============
   El sitio se escribe en ingles. La traduccion vive en traduccion.js,
   como pares "frase en ingles": "frase en español".
   Para añadir texto nuevo basta con sumar el par a ese archivo.
   =================================================== */
(function(){
  var IDIOMA = "dxm-idioma";
  var boton  = document.querySelector(".idioma");
  if (!boton) return;

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
    boton.setAttribute("aria-label", lang === "es" ? "Read in English" : "Leer en español");
    try { localStorage.setItem(IDIOMA, lang); } catch(e){}
  }

  var guardado = "en";
  try { guardado = localStorage.getItem(IDIOMA) || "en"; } catch(e){}
  if (guardado === "es") aplicar("es"); else aplicar("en");

  boton.addEventListener("click", function(){
    aplicar(document.documentElement.lang === "es" ? "en" : "es");
  });
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
