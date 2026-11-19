"""Optimiza las fotos del cliente sin recortar las láminas ni mover originales."""
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
PRODUCTS = ROOT / "assets/img/productos"
ITEMS = [
    ("BUJIAS BOSCH.jpeg", "bujias-bosch"),
    ("BUJIAS PREMIUM.jpeg", "bujias-premium"),
    ("LIQUIDO PARA FRENOS.jpeg", "liquido-frenos"),
    ("RULEMANES.jpeg", "rulemanes"),
    ("WhatsApp Image 2026-11-17 at 16.21.52 (2).jpeg", "liquido-frenos-tipos"),
    ("WhatsApp Image 2026-11-17 at 16.21.52.jpeg", "bujias-electrodos"),
]

if __name__ == "__main__":
    for source, slug in ITEMS:
        with Image.open(PRODUCTS / source) as original:
            image = ImageOps.exif_transpose(original).convert("RGB")
            for suffix, size, quality in [("720", 720, 82), ("ampliada", 1536, 88)]:
                resized = image.copy()
                resized.thumbnail((size, size), Image.Resampling.LANCZOS)
                output = PRODUCTS / f"{slug}-{suffix}.webp"
                resized.save(output, "WEBP", quality=quality, method=6)
                print(output.name, resized.size, output.stat().st_size)
