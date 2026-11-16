# Edi Repuestos — Sitio web

Sitio de una página para **Edi Repuestos**, casa de repuestos y accesorios automotores en Rivera, Uruguay.

- **Dirección:** Dr. Fernández Crespo 570, 40000 Rivera, Uruguay
- **Teléfonos:** +598 4622 7161 (local) · +598 99 823 483 (WhatsApp) · +598 94 497 866 · +598 99 822 370
- **Horario:** lunes a viernes 8:30–12:00 y 14:00–18:30 · sábados 8:30–12:30
- **Redes:** [Instagram @edirepuestos](https://www.instagram.com/edirepuestos/) · [TikTok @edi.repuestos](https://www.tiktok.com/@edi.repuestos)

---

## 1. Stack

Sitio estático sin framework, sin build y sin dependencias externas. Se publica tal cual en cualquier hosting estático (Netlify, Vercel, Cloudflare Pages, cPanel, Nginx, etc.).

| Pieza | Implementación |
| --- | --- |
| HTML | `index.html` — una sola página semántica |
| CSS | `assets/css/styles.css` — sistema visual propio, mobile-first |
| JS | `assets/js/main.js` — menú móvil y generador de consulta (mejora progresiva) |
| Tipografías | Barlow Condensed + Inter, autoalojadas en `assets/fonts/` |
| Imágenes | Logo real en WebP, favicon SVG/PNG, imagen Open Graph JPEG |
| SEO técnico | `robots.txt`, `sitemap.xml`, canonical, Open Graph, Twitter Card |
| Datos estructurados | JSON-LD `AutoPartsStore`, `WebSite`, `FAQPage` |

Todo el contenido es legible y navegable sin JavaScript. El formulario no envía datos a ningún servidor: arma un mensaje y ofrece enviarlo por WhatsApp o copiarlo.

Un botón flotante de WhatsApp acompaña la lectura en el borde inferior derecho y reserva espacio en el pie para no tapar el crédito de desarrollo.

---

## 2. Estructura

```text
Edi_Repuestos/
├─ index.html                 Página completa (contenido, metadata, JSON-LD)
├─ robots.txt
├─ sitemap.xml
├─ README.md
├─ AUDIT.md
├─ assets/
│  ├─ css/styles.css
│  ├─ js/main.js
│  ├─ fonts/                  Barlow Condensed 600/700 + Inter variable
│  └─ img/
│     ├─ edi-logo-320.webp    Logo en header y footer
│     ├─ edi-logo-640.webp    Logo en la ficha del hero
│     ├─ edi-logo-square.png  Logo cuadrado para schema.org
│     ├─ og-edirepuestos.jpg  Imagen 1200×630 para redes
│     ├─ favicon.svg / favicon-32.png / apple-touch-icon.png
└─ tools/
   └─ og-card.html            Fuente para regenerar la imagen Open Graph
```

---

## 3. Ver el sitio en local

Cualquier servidor estático sirve. Con Python:

```bash
cd Edi_Repuestos
python -m http.server 4173
```

Abrir `http://localhost:4173/`.

No abrir `index.html` con doble clic (`file://`): el menú móvil, el clipboard y las rutas relativas se comportan distinto según el navegador.

---

## 4. Estructura de la página

1. **Header** — navegación fija, horario de atención en la barra superior.
2. **Hero** — propuesta de valor, CTA de llamada, ficha del local con logo real.
3. **Qué encontrás** — repuestos, accesorios y consulta de disponibilidad.
4. **Cómo consultar** — tres pasos.
5. **Región fronteriza** — Rivera ↔ Santana do Livramento (incluye línea en portugués).
6. **Ubicación** — dirección, horario, mapa de Google embebido y enlace para abrir la ubicación.
7. **Contacto** — WhatsApp, teléfonos, redes y generador de consulta con envío directo.
8. **Preguntas frecuentes** — seis respuestas, también en JSON-LD.
9. **Footer** — horario, crédito de desarrollo FB Informática.
10. **Botón flotante de WhatsApp** — visible en todo el sitio, con mensaje precargado.

---

## 5. SEO

- **Title (56):** `Edi Repuestos | Repuestos Automotores en Rivera, Uruguay`
- **Meta description (146):** repuestos y accesorios multimarca, dirección y teléfono.
- **H1 único:** `Repuestos y accesorios automotores en Rivera | Edi Repuestos`.
- **Canonical:** raíz del dominio (el sitio es una sola página; no se creó una URL hija para la keyword principal).
- **Keywords cubiertas en texto real:** repuestos automotores Rivera, repuestos y accesorios, multimarca, autopartes, frontera con Santana do Livramento, casa de repuestos.
- **JSON-LD:** `AutoPartsStore` (dirección, teléfono, `contactPoint` de WhatsApp, `openingHoursSpecification`, área servida, `sameAs`), `WebSite` y `FAQPage` alineado con las preguntas visibles.

### Dominio

El sitio quedó configurado para **`https://edirepuestos.com`** (dominio apex, sin `www`) en:

- `index.html` → canonical, `og:url`, `og:image`, `twitter:image`, `@id` y `url` del JSON-LD
- `robots.txt` → línea `Sitemap:`
- `sitemap.xml` → `<loc>`

Al publicar (repositorio ya subido a `github.com/dfchanel-coder/edi_repuestos`, rama `main`):

1. En **Settings → Pages**, publicar desde la rama `main`, carpeta `/ (root)`.
2. En **Settings → Pages → Custom domain**, cargar `edirepuestos.com`; GitHub Pages redirige `www.edirepuestos.com` al apex. Activar **Enforce HTTPS** cuando el certificado esté emitido.
3. En el DNS del dominio:
   - `A` del apex a `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   - `CNAME` de `www` a `dfchanel-coder.github.io`.
4. Verificar que `https://edirepuestos.com/assets/img/og-edirepuestos.jpg` responda público: las redes sociales no siempre siguen redirecciones al buscar la imagen.
5. Confirmar que `https://edirepuestos.com/robots.txt` y `/sitemap.xml` respondan 200 sin autenticación.

### Mapa de Google (contenido de terceros)

La sección de ubicación usa el `<iframe>` oficial de Google Maps del lugar (place ID `0x95a9ff2d2af20ed5:0x6f6b1f5be98f7fb8`), con `loading="lazy"`, `title` descriptivo y `referrerpolicy="strict-origin-when-cross-origin"`. El alto se reserva con `aspect-ratio`, así que el iframe no genera desplazamiento de layout al cargar.

Implica una dependencia externa: al llegar a la sección, el navegador descarga scripts de Google y Google puede setear cookies propias. Si el cliente pide privacidad estricta, la alternativa es reemplazar el iframe por una imagen estática del mapa con enlace a Google Maps (carga cero de terceros). El enlace “Abrir en Google Maps” y la dirección en texto siguen funcionando aunque el iframe no cargue.

---

## 6. Datos verificados y datos omitidos

### Verificado y publicado

- Nombre comercial: Edi Repuestos.
- Dirección: Dr. Fernández Crespo 570, Rivera, Uruguay (confirmada por el cliente y por listados públicos).
- Horario: lunes a viernes 8:30–12:00 y 14:00–18:30; sábados 8:30–12:30.
- Teléfono fijo: 4622 7161 · +598 4622 7161.
- WhatsApp principal: 099 823 483 · +598 99 823 483.
- Celulares: 094 497 866 y 099 822 370.
- Instagram y TikTok oficiales.
- Rubro: repuestos y accesorios automotores multimarca.

### Omitido a propósito (sin confirmación)

| Dato | Motivo |
| --- | --- |
| `edirepuestos@hotmail.com` | Sin confirmación de vigencia. |
| Teléfono de Brasil `55 981141494` | Sin confirmación. |
| Medios de pago / crédito de la casa | Mencionado en redes, sin detalle contractual. |
| Envíos a todo el país | Se menciona en redes; la web solo invita a consultar por envíos. |

Cuando el cliente confirme estos datos, se agregan al HTML y al JSON-LD (`email`, `paymentAccepted`, etc.).

---

## 7. Checklist de publicación

- [ ] Publicar desde `main` en GitHub Pages y cargar el dominio `edirepuestos.com`.
- [ ] Crear los registros DNS (A del apex y CNAME de `www`) y activar Enforce HTTPS.
- [ ] Publicar sobre HTTPS (obligatorio para el clipboard y para el canonical).
- [ ] Verificar que `/assets/*` responda 200 y con cache largo (`Cache-Control: public, max-age=31536000, immutable` para fuentes e imágenes).
- [ ] Comprimir HTML/CSS/JS con gzip o brotli en el servidor.
- [ ] Enviar `sitemap.xml` en Google Search Console y Bing Webmaster Tools.
- [ ] Validar el JSON-LD en [Rich Results Test](https://search.google.com/test/rich-results).
- [ ] Probar la imagen Open Graph en [opengraph.xyz](https://www.opengraph.xyz/) con la URL final.
- [ ] Actualizar la dirección y el horario en Google Business Profile y Waze para que coincidan con la web.
- [ ] Verificar que el número de WhatsApp `+598 99 823 483` siga activo en el enlace `wa.me`.

---

## 8. Mantenimiento

### Regenerar la imagen Open Graph

`tools/og-card.html` es la fuente (1200×630, usa las tipografías y el logo del sitio). Se renderiza con Edge/Chrome headless:

```bash
msedge --headless=new --disable-gpu --hide-scrollbars --window-size=1200,630 \
  --screenshot=tools/og.png "file:///ruta/al/proyecto/tools/og-card.html"
```

Luego convertir `tools/og.png` a `assets/img/og-edirepuestos.jpg` (calidad ~88, progresivo).

### Cambiar contenido

Todo el texto está en `index.html`. Si se agrega o modifica una pregunta frecuente, actualizar también el bloque `FAQPage` del JSON-LD para que coincida.

### Crédito de desarrollo

El pie incluye el crédito discreto a FB Informática con enlace a `https://www.fbinformaticauy.com`. Mantenerlo salvo indicación contraria.
