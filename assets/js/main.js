/* Edi Repuestos — interacciones mínimas
   Sin dependencias. Todo el contenido funciona sin JavaScript;
   el menú móvil y el generador de consultas son mejoras progresivas. */

(function () {
  "use strict";

  /* ---------------------------------------------------------------------
     Año del pie de página
     --------------------------------------------------------------------- */

  var year = document.getElementById("year");
  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  /* ---------------------------------------------------------------------
     Menú móvil
     --------------------------------------------------------------------- */

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("nav-principal");
  var header = document.querySelector(".site-header");

  if (toggle && nav && header) {
    var setOpen = function (open) {
      nav.setAttribute("data-open", String(open));
      toggle.setAttribute("aria-expanded", String(open));
    };

    var isOpen = function () {
      return toggle.getAttribute("aria-expanded") === "true";
    };

    toggle.addEventListener("click", function () {
      setOpen(!isOpen());
    });

    nav.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        setOpen(false);
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen()) {
        setOpen(false);
        toggle.focus();
      }
    });

    document.addEventListener("click", function (event) {
      if (isOpen() && !header.contains(event.target)) {
        setOpen(false);
      }
    });

    var desktop = window.matchMedia("(min-width: 981px)");
    var onChange = function (event) {
      if (event.matches) {
        setOpen(false);
      }
    };

    if (typeof desktop.addEventListener === "function") {
      desktop.addEventListener("change", onChange);
    } else if (typeof desktop.addListener === "function") {
      desktop.addListener(onChange);
    }
  }

  /* ---------------------------------------------------------------------
     Generador de consulta (100% local, no envía ni guarda datos)
     --------------------------------------------------------------------- */

  var form = document.getElementById("consulta-form");
  var vehicleInput = document.getElementById("vehiculo");
  var partInput = document.getElementById("repuesto");
  var nameInput = document.getElementById("nombre");
  var result = document.getElementById("consulta-resultado");
  var message = document.getElementById("mensaje");
  var copyButton = document.getElementById("copiar");
  var status = document.getElementById("copiar-estado");
  var waLink = document.getElementById("enviar-wa");

  if (form && vehicleInput && partInput && nameInput && result && message) {
    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      var vehicle = vehicleInput.value.trim();
      var part = partInput.value.trim();
      var name = nameInput.value.trim();

      if (!part) {
        partInput.focus();
        return;
      }

      var lines = [
        "Hola, les escribo desde la web de Edi Repuestos.",
        ""
      ];

      if (vehicle) {
        lines.push("Vehículo: " + vehicle);
      }

      lines.push("Necesito: " + part);

      if (name) {
        lines.push("Mi nombre: " + name);
      }

      lines.push("", "¿Me pueden confirmar disponibilidad? Gracias.");

      message.value = lines.join("\n");

      if (waLink) {
        waLink.href = "https://wa.me/59899823483?text=" + encodeURIComponent(message.value);
      }

      result.hidden = false;
      message.focus({ preventScroll: true });
      result.scrollIntoView({
        behavior: reducedMotion ? "auto" : "smooth",
        block: "nearest"
      });
    });

    form.addEventListener("input", function () {
      if (!result.hidden) {
        result.hidden = true;
        if (status) {
          status.textContent = "";
        }
      }
    });

    if (copyButton && status) {
      copyButton.addEventListener("click", function () {
        var text = message.value;
        if (!text) {
          return;
        }

        var announce = function (ok) {
          status.textContent = ok
            ? "Mensaje copiado. Pegalo en WhatsApp o en Instagram."
            : "No pudimos copiar automáticamente. Seleccioná el texto y copialo.";
        };

        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(text).then(
            function () {
              announce(true);
            },
            function () {
              legacyCopy(text, announce);
            }
          );
        } else {
          legacyCopy(text, announce);
        }
      });
    }

    function legacyCopy(text, announce) {
      var copied = false;
      message.removeAttribute("readonly");
      message.focus();
      message.select();
      message.setSelectionRange(0, text.length);

      try {
        copied = document.execCommand("copy");
      } catch (error) {
        copied = false;
      }

      message.setAttribute("readonly", "readonly");
      announce(copied);
    }
  }
})();
