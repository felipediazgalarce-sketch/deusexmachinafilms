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
  var bar = document.querySelector("header");
  if (bar) {
    addEventListener("scroll", function () {
      bar.classList.toggle("scrolled", scrollY > 10);
    }, { passive: true });
  }

  // Icono de play, inyectado para no repetir el SVG en cada ficha
  var SVG = '<svg viewBox="0 0 68 48" aria-hidden="true">'
          + '<path d="M66.5 7.7a8.6 8.6 0 0 0-6-6.1C55.2 0 34 0 34 0S12.8 0 7.5 1.6a8.6 8.6 0 0 0-6 6.1A90 90 0 0 0 0 24a90 90 0 0 0 1.5 16.3 8.6 8.6 0 0 0 6 6C12.8 48 34 48 34 48s21.2 0 26.5-1.7a8.6 8.6 0 0 0 6-6A90 90 0 0 0 68 24a90 90 0 0 0-1.5-16.3z" fill="#000" opacity=".55"/>'
          + '<path d="M27 34V14l18 10z" fill="#fff"/></svg>';

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
        onReady: function (e) { e.target.mute(); e.target.playVideo(); },
        onStateChange: function (e) {
          // si se pausa o termina, volver a reproducir de inmediato:
          // asi YouTube no llega a dibujar los controles centrales
          if (e.data === YT.PlayerState.ENDED) {
            // bucle sin usar 'playlist': con lista, YouTube dibuja
            // los botones de anterior/siguiente en el centro
            e.target.seekTo(0); e.target.playVideo();
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
