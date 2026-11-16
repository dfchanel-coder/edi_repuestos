# Auditoría — Edi Repuestos

Fecha: 16/11/2026
Alcance: `index.html`, `assets/css/styles.css`, `assets/js/main.js`, `assets/img/productos/`, `robots.txt`, `sitemap.xml`.
Método: revisión de código, medición en navegador real (Chromium vía Edge), Lighthouse 13.4.1 sobre servidor local `http://localhost:4173/`, y comprobaciones programáticas de layout, contraste, semántica e interacción.

---

## 1. Resultado general

| Área | Resultado |
| --- | --- |
| Lighthouse Accessibility | **100** |
| Lighthouse Best Practices | **100** |
| Lighthouse SEO | **100** |
| Errores de consola | 0 |
| Recursos con error (4xx/5xx) | 0 |
| Scroll horizontal | Ninguno en 14 anchos (320 → 1440 px) |
| Contraste de texto | Todos los textos pasan AA; sin excepciones reales |
| Interacciones | Menú móvil, Escape, clic externo, formulario, estado de copiado y pausa de la tira verificados |
| Catálogo | 17 tarjetas y 12 miniaturas WebP, todas con 200 y sin imágenes rotas |
| Tira del hero | 6 fotos + 6 clones, bucle de 52 s, pausa accesible y sin desborde de página |
| Mapa embebido | Iframe de Google Maps con HTTP 200, alto reservado y sin desborde en 14 anchos |

La categoría Performance no fue emitida por la herramienta de auditoría disponible. La medición se cubrió con análisis de peso, recursos y renderizado. El mapa embebido de Google es el único recurso de terceros y carga diferido.

---

## 2. Problemas encontrados y corregidos

### ALTO — Enlaces con área táctil menor a 24 px

**Detectado:** medición de `getBoundingClientRect()` sobre todos los elementos interactivos.

- Enlaces de tarjetas (`.card-link`): 23 px de alto.
- Enlaces de navegación del footer: 21 px.
- Enlaces del menú principal en desktop: 21 px.

**Riesgo:** incumple WCAG 2.2 AA 2.5.8 (Target Size Minimum) y complica el uso en móvil.

**Corregido:**

- `.card-link` → `min-height: 24px` (mantiene el subrayado inferior).
- `.footer-nav a`, `.footer-contact a` → `padding-block: 2px`.
- `.nav-list a` → `padding-block: 9px` (≈27 px de alto).

**Verificación:** la medición automática posterior devolvió `issues: []` en los 14 anchos probados.

### MEDIO — Indicador de foco poco visible sobre fondos oscuros

**Detectado:** revisión de estilos. El outline lima sobre el hero negro se confundía con el acento de marca y no delimitaba el elemento.

**Corregido:** `:focus-visible` ahora usa outline lima + `box-shadow: 0 0 0 2px var(--ink)`, generando un anillo de contraste en fondos claros y oscuros. Se eliminó la excepción de `.btn-primary`, que dejaba botones lima sin anillo.

### MEDIO — Nombre accesible del botón flotante no coincidía con el texto visible

**Detectado:** Lighthouse (`label-content-name-mismatch`) marcó el enlace `.wa-float`: el texto visible era “WhatsApp 099 823 483” y el `aria-label` decía “Escribinos por WhatsApp al 099 823 483”.

**Riesgo:** incumple WCAG 2.1 A / 2.5.3 (Label in Name): quien usa control por voz no puede activar el enlace diciendo lo que ve.

**Corregido:** `aria-label="WhatsApp 099 823 483"`, que contiene exactamente la etiqueta visible.

**Verificación:** nueva auditoría Lighthouse sin fallos.

### MEDIO — Navegación móvil inutilizable sin JavaScript

**Detectado:** el botón de menú dependía de JS; con JS desactivado el listado quedaba oculto en pantallas menores a 980 px.

**Corregido:** bloque `<noscript>` en el `<head>` que muestra la navegación en línea y oculta el botón. El resto del contenido ya era accesible sin JS.

### BAJO — Saltos de línea del H1 en lectores de pantalla

**Detectado:** el H1 usa tres `<span>` en bloque para el tratamiento tipográfico.

**Resultado:** el nombre accesible se lee correctamente (“Repuestos y accesorios automotores en Rivera | Edi Repuestos”); no requiere cambios. Se documenta para evitar que se “corrija” agregando texto invisible innecesario.

---

## 3. Comprobaciones realizadas

### Layout y responsive

Medición en iframes a **320, 360, 390, 414, 480, 560, 640, 768, 834, 980, 1024, 1180, 1280 y 1440 px**:

- `scrollWidth ≈ innerWidth - 15` en todos los casos (sin desborde horizontal).
- Sin solapamiento entre copy del hero y ficha del local.
- Sin textos recortados por `overflow: hidden`.
- Sin desbordes de elementos de flujo (el único elemento que excede el viewport es el número decorativo `570`, contenido por `overflow: hidden` en `.hero`).
- Mapa de Google: el `.map-frame` mantiene la proporción `1.06 / 1` en todos los anchos (265×250 px a 320 px, 620×585 px en desktop) y la cabecera del mapa no desborda ni recorta texto.

### Catálogo y multimedia

- **Grilla:** 4 columnas en desktop → 3 a 1180 px → 2 a 760 px; estrellas 5 → 4 → 3 → 2. Verificado midiendo `gridTemplateColumns` en once anchos (320 → 1440 px).
- **Imágenes:** 17 tarjetas (5 estrellas + 12 rubros) y 12 miniaturas. Todas responden 200 y ninguna queda rota; las tarjetas usan `width`/`height` y `aspect-ratio` para no aportar CLS.
- **Área táctil:** los enlaces “Consultar” y las tarjetas mantienen un mínimo de 24 px; la medición automática no devolvió objetivos pequeños.
- **Enlaces de consulta:** cada tarjeta arma `https://wa.me/59899823483?text=` con el nombre del producto. Verificado el prefijo y el texto decodificado en una tarjeta del catálogo.
- **Tira del hero:** con JS se duplican los seis elementos, los clones quedan `aria-hidden="true"` y con `alt=""`. El botón aparece solo con JS, alterna `data-paused` y `aria-pressed`, cambia entre Pausar y Reanudar, y `animation-play-state` pasa a `paused`. Con `prefers-reduced-motion` no se duplica nada y no hay animación.
- **Respaldo sin JS:** el contenedor es `overflow-x: auto` con `scroll-snap`; si no hay JS, la tira se recorre a mano y el botón permanece oculto.
- **Desborde:** el único elemento que excede el viewport es la pista de la tira dentro de su contenedor con `overflow: hidden`, comportamiento intencional. El `scrollWidth` del documento sigue igual al ancho de ventana en los once anchos.
- **Contraste del catálogo:** los textos nuevos (`#b9bbae`, `#8f9184` y lima sobre `#0a0b08`; `#3f6d12` y `#5b5d51` sobre blanco) pasan AA.

### Contraste

Cálculo de relación de contraste sobre color computado y fondo efectivo heredado, para todos los nodos de texto visibles.

- Sin fallos AA (4.5:1 texto normal, 3:1 texto grande).
- Único falso positivo: el número decorativo `570` (`color: transparent`, `aria-hidden="true"`).
- Pares críticos: `#5b5d51` sobre `#f3f2ec` (≈5.2:1), `#a9ab9d` sobre `#0a0b08` (≈7.4:1), `#8f9184` sobre `#0a0b08` (≈4.9:1), lima `#74c32c` sobre negro (≈7:1).

### Semántica y accesibilidad

- Un solo `<h1>`; jerarquía H2/H3 sin saltos.
- `lang="es-UY"`; línea en portugués marcada con `lang="pt"`.
- Imágenes decorativas con `alt=""`; el logo de la ficha con `alt="Edi Repuestos"`.
- Sin enlaces sin nombre accesible.
- Skip link funcional hacia `#contenido`.
- FAQ con `<details>/<summary>` nativos (teclado y lector de pantalla sin JS).
- Formulario: `<label>` explícito en los tres campos, `required` en el campo necesario, `maxlength` definido, estado anunciado con `role="status"` y `aria-live`.
- Menú móvil: `aria-expanded`, `aria-controls`, cierre con Escape devolviendo el foco al botón, cierre por clic externo y al cambiar a desktop.
- WhatsApp flotante: 56 px en móvil / 52 px de alto en desktop, foco visible, `aria-label` igual al texto visible y espacio reservado en el pie para no superponerse al contenido.
- Mapa: `<iframe>` con `title` descriptivo y `loading="lazy"`; la dirección y el enlace a Google Maps siguen disponibles como texto si el iframe no carga.

### SEO técnico

- Title 56 caracteres; description 146; ambos dentro de rango.
- Canonical absoluto; `robots` con `max-image-preview:large`.
- Open Graph completo (type, site_name, locale, title, description, url, image 1200×630 con dimensiones y alt) y Twitter Card `summary_large_image`.
- `sitemap.xml` válido con una URL; `robots.txt` referencia el sitemap.
- JSON-LD parseable: `AutoPartsStore`, `WebSite`, `FAQPage`. El FAQ del schema replica exactamente las seis preguntas visibles.
- Un único H1 con la keyword principal; keywords secundarias distribuidas en H2, texto y FAQ sin sobreoptimización.
- Enlaces externos con `rel="noopener noreferrer"` y `target="_blank"`.

### Seguridad

- Sin backend, sin cookies propias, sin analytics ni trackers.
- Único contenido de terceros: el `<iframe>` oficial de Google Maps en la sección de ubicación (`loading="lazy"`, `referrerpolicy="strict-origin-when-cross-origin"`). Google puede setear cookies propias al cargarlo; no hay scripts de terceros en el documento principal.
- El formulario no envía ni persiste datos: construye el mensaje en memoria y el usuario decide qué hacer con él.
- Sin `innerHTML` ni interpolación de HTML con datos de usuario: el mensaje se escribe con `textarea.value`.
- Sin secretos ni variables de entorno.
- Superficie de ataque reducida a HTML/CSS/JS estático.

### Rendimiento

- Peso inicial: ~55 KB HTML + 47 KB CSS + 7 KB JS + 91 KB fuentes + 41 KB logos + ~160 KB de miniaturas de la tira ≈ **400 KB sin comprimir** (≈150–180 KB con gzip/brotli). El resto del catálogo (≈1,1 MB) se carga por `loading="lazy"` al llegar a la sección.
- Catálogo completo: 27 WebP, **1,3 MB**. Tarjetas 720×900 (27–110 KB) y miniaturas 480×480 (15–42 KB).
- Imagen Open Graph (92 KB) no se descarga al visitar el sitio.
- Fuentes autoalojadas con `preload` y `font-display: swap`; solo dos familias y tres archivos.
- Logo en WebP (13/27 KB) con `width`/`height` explícitos para evitar CLS.
- Sin librerías, sin polyfills, sin JS bloqueante (`defer`).
- Animaciones limitadas a `transform`/`opacity` y desactivadas con `prefers-reduced-motion`.
- CSS con `clamp()` en lugar de múltiples breakpoints de tipografía.
- El mapa embebido y la tira del hero son los únicos recursos que se cargan al inicio sin esperar scroll. El iframe usa `loading="lazy"` y alto reservado (`aspect-ratio`), así que no aporta CLS; las 6 miniaturas de la tira pesan ~160 KB en total y las 27 fotos restantes se cargan por `loading="lazy"`.

---

## 4. Limitaciones conocidas

| # | Limitación | Impacto | Decisión |
| --- | --- | --- | --- |
| 1 | Dominio sin DNS ni HTTPS activos | Canonical, OG, sitemap y schema ya apuntan a `https://edirepuestos.com`, pero hasta publicar esos enlaces no resuelven | Archivos listos y repo publicado. Falta activar GitHub Pages, cargar el dominio y crear los DNS (apex `A` + `www` `CNAME`); Pages redirige `www` → apex. |
| 2 | Horarios de feriados no publicados | El local puede cerrar en feriados sin aviso en la web | El horario regular ya está publicado y en el schema. Las excepciones se pueden agregar en `specialOpeningHoursSpecification`. |
| 3 | Mapa embebido de Google (terceros) | Carga scripts de Google y puede setear cookies propias | Se usó el iframe oficial con `loading="lazy"` y alto reservado (`aspect-ratio`) para no afectar CLS. La dirección y el enlace a Maps funcionan sin el iframe. Si se exige privacidad estricta, se cambia por imagen estática enlazada. |
| 4 | Sin formulario con backend | No hay envío automático de consultas desde un servidor | El mensaje se envía por WhatsApp con el texto precargado o se copia. Sin datos almacenados, sin spam, sin mantenimiento. |
| 5 | Datos de contacto secundarios omitidos | Puede faltar un canal que el cliente sí usa | Se documentaron en README para agregarlos cuando se confirmen. |
| 6 | Performance no medida por Lighthouse | Sin métricas LCP/CLS/TBT de laboratorio | Se midió peso y composición; el iframe del mapa y las miniaturas del hero son lo único que carga al inicio. Al publicar conviene correr PageSpeed Insights sobre la URL final. |
| 7 | Nombres de productos sin confirmar | Las etiquetas del catálogo salieron de los nombres de archivo; un nombre o una descripción podría no coincidir con el producto real | Se muestran como referencia y cada tarjeta invita a consultar. El cliente debe validar la lista del README antes de difundir el catálogo. |
| 8 | Fotos de producto no revisadas visualmente por el desarrollador | El recorte 4:5 y la asignación foto–producto no fueron verificados a ojo | Se conservan los originales fuera del repo para reencuadrar. Conviene una revisión rápida del cliente sobre la página publicada. |

---

## 5. Recomendaciones posteriores (no bloqueantes)

1. Mantener sincronizados el horario y el WhatsApp de la web con Google Business Profile (el schema ya los declara).
2. Revisar que el embed de Google Maps siga mostrando el pin correcto si el listado del local cambia de place ID.
3. Crear o reclamar Google Business Profile con la dirección exacta y las mismas horas que la web.
4. Revisar las fotos y los nombres del catálogo con el cliente: el sitio ya evita inventar datos, pero la asignación foto–producto se hizo por nombre de archivo.
5. Evaluar fotos reales del mostrador y del local: hoy el sitio usa fotos de productos, y una toma del frente del local mejora confianza.
6. Si se confirma el envío a todo el país, agregar una sección breve y actualizar el `areaServed` del schema.
7. Si el cliente quiere publicar baterías, reutilizar los tres MP4 que quedaron en `videos/` como sección propia (hoy no se usan).
8. Revisar en Search Console a los 30 días: impresiones por “repuestos Rivera”, CTR y consultas por clic en teléfono.

---

## 6. Conclusión

El sitio cumple el objetivo: una página informativa, rápida y accesible que posiciona “repuestos automotores en Rivera”, muestra los datos verificados del local, presenta una muestra del catálogo con Liqui Moly como estrella y deriva la consulta a WhatsApp, al teléfono o a Instagram.

No quedan problemas críticos ni altos abiertos. Falta publicar el dominio (`edirepuestos.com`) con DNS y HTTPS, unificar el listado de Google Business Profile con estos datos y que el cliente valide los nombres del catálogo. Los datos comerciales no confirmados quedaron fuera de la página de forma deliberada para no publicar información falsa.
