import pathlib
from PIL import Image, ImageOps

SRC = pathlib.Path("assets/img")
OUT = pathlib.Path("assets/img/productos")
# Los originales viven fuera del repositorio publicado.
ORIG = pathlib.Path(__file__).resolve().parent.parent.parent / "Edi_Repuestos_originales"
OUT.mkdir(parents=True, exist_ok=True)
ORIG.mkdir(exist_ok=True)

# slug: (archivo original, tamaño de tarjeta 4:5, miniatura 1:1)
ITEMS = {
    "liqui-moly-linea": ("conjunto_liqui.jpeg", True, True),
    "liqui-moly-ceratec": ("ceratec_liqui.jpeg", True, True),
    "liqui-moly-mos2": ("mos2_liqui.jpeg", True, False),
    "liqui-moly-atf": ("atf_liqui.jpeg", True, False),
    "liqui-moly-hidraulico": ("hydro_liqui.jpeg", True, False),
    "liqui-moly-tapafugas": ("tapa_fugas_liqui.jpeg", True, False),
    "correas": ("correas_repuesto.jpeg", True, True),
    "grasas": ("grasa_rulemans.jpeg", True, False),
    "refrigerante": ("fluido_radiador_verde.jpeg", True, False),
    "estetica": ("estetica.jpeg", True, True),
    "herramientas-electricas": ("tornilladora_impacto_inmeco_herramientas.jpeg", True, False),
    "herramientas-taller": ("herramientas002.jpeg", True, True),
    "iluminacion-led": ("luz_led_caminero.jpeg", True, True),
    "accesorios-12v": ("jarra_electrica_12v_accesorios.jpeg", True, True),
    "quimicos": ("epoxy_uno.jpeg", True, True),
    "camara-endoscopica": ("camara_endoscopica.jpeg", True, False),
    "limpia-contactos": ("limpia_contacto_electrico.jpeg", True, False),
    "mangueras-hidraulicas": ("hidro_manguera.jpeg", True, False),
    "linterna-frontal": ("linterna_cabeza_herramientas.jpeg", True, False),
}

def cover(im, w, h):
    return ImageOps.fit(im.convert("RGB"), (w, h), Image.LANCZOS, centering=(0.5, 0.5))

total_card = total_thumb = 0
report = []
for slug, (name, card, thumb) in ITEMS.items():
    src = SRC / name
    if not src.exists():
        report.append((slug, "FALTA", 0, 0))
        continue
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if card:
        p = OUT / f"{slug}-720.webp"
        cover(im, 720, 900).save(p, "WEBP", quality=78, method=6)
        total_card += p.stat().st_size
        report.append((slug, "720x900", p.stat().st_size, 0))
    if thumb:
        p = OUT / f"{slug}-480.webp"
        cover(im, 480, 480).save(p, "WEBP", quality=72, method=6)
        total_thumb += p.stat().st_size
        report.append((slug, "480x480", 0, p.stat().st_size))

print(f"{'slug':24} {'tam':10} {'tarjeta':>9} {'mini':>8}")
for slug, size, c, t in report:
    print(f"{slug:24} {size:10} {c/1024 if c else 0:8.1f}K {t/1024 if t else 0:7.1f}K")
print(f"TOTAL tarjetas: {total_card/1024:.0f} KB · miniaturas: {total_thumb/1024:.0f} KB")

# Los originales se guardan fuera de la carpeta publicada.
for p in sorted(SRC.glob("*.jpeg")):
    dest = ORIG / p.name
    if not dest.exists():
        p.replace(dest)
print("originales movidos:", len(list(ORIG.glob('*.jpeg'))))
