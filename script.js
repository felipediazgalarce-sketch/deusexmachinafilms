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

/* ---------------------------------------------------------------
   REEL DE PORTADA con la API de YouTube.
   Un iframe normal muestra los controles centrales (play/pausa,
   avanzar, retroceder) en cuanto el video se pausa o se queda
   cargando. Con la API el reproductor se reanuda solo, asi que
   nunca entra en ese estado y esa interfaz no llega a dibujarse.
   Es lo mismo que hacia el sitio anterior con RevSlider.
--------------------------------------------------------------- */
(function () {
  "use strict";
  var caja = document.getElementById("reel");
  if (!caja) return;                       // solo existe en la portada

  var ID = "5Xr_eElt6vE", player = null;

  /* El play reaparecia en cada vuelta porque el video LLEGABA al final:
     al entrar en estado "terminado", YouTube dibuja su interfaz dentro
     del iframe, donde el CSS de fuera no alcanza.
     Solucion: no dejarlo terminar. Se vigila el tiempo y se rebobina
     medio segundo antes del final, de modo que el reproductor nunca
     sale del estado "reproduciendo" y no llega a dibujar nada. */
  var vigilante = null;
  function vigilarFinal(p) {
    if (vigilante) return;
    vigilante = setInterval(function () {
      try {
        var dur = p.getDuration(), t = p.getCurrentTime();
        if (!dur || dur < 1) return;              // aun sin metadatos
        if (t >= dur - 0.5) p.seekTo(0.05, true); // rebobina antes del final
      } catch (e) { /* el reproductor aun no responde */ }
    }, 200);
  }

  window.onYouTubeIframeAPIReady = function () {
    player = new YT.Player("reel", {
      videoId: ID,
      host: "https://www.youtube-nocookie.com",
      playerVars: {
        autoplay: 1, mute: 1, controls: 0,
        disablekb: 1, fs: 0, rel: 0, modestbranding: 1,
        iv_load_policy: 3, playsinline: 1
      },
      events: {
        onReady: function (e) {
          e.target.mute(); e.target.playVideo(); vigilarFinal(e.target);
        },
        onStateChange: function (e) {
          // en cuanto reproduce de verdad, se retira la tapa del logo
          if (e.data === YT.PlayerState.PLAYING) {
            var c = document.getElementById("reel-caja");
            if (c) c.classList.add("reproduciendo");
            vigilarFinal(e.target);
          }
          // red de seguridad por si aun asi termina o alguien lo pausa
          if (e.data === YT.PlayerState.ENDED) {
            e.target.seekTo(0.05, true); e.target.playVideo();
          } else if (e.data === YT.PlayerState.PAUSED) {
            e.target.playVideo();
          }
        }
      }
    });
  };

  var s = document.createElement("script");
  s.src = "https://www.youtube.com/iframe_api";
  document.head.appendChild(s);
})();

/* ---------------------------------------------------------------
   DIA / NOCHE. Por defecto noche (el negro es la marca). La
   eleccion se guarda para las siguientes visitas.
--------------------------------------------------------------- */
(function () {
  "use strict";
  var raiz = document.documentElement,
      boton = document.querySelector(".tema");

  function pintar(tema) {
    if (tema === "dia") raiz.setAttribute("data-tema", "dia");
    else raiz.removeAttribute("data-tema");
    if (boton) boton.textContent = (tema === "dia") ? "Noche" : "Día";
  }

  var guardado = null;
  try { guardado = localStorage.getItem("tema"); } catch (e) {}
  pintar(guardado || "noche");

  if (boton) {
    boton.addEventListener("click", function () {
      var nuevo = raiz.getAttribute("data-tema") === "dia" ? "noche" : "dia";
      pintar(nuevo);
      try { localStorage.setItem("tema", nuevo); } catch (e) {}
    });
  }
})();
