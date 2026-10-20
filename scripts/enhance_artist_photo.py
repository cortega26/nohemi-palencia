#!/usr/bin/env python3
"""Conservative 2x reproduction of artist-in-gallery portrait (non-generative)."""
from __future__ import annotations
import hashlib
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets/img/nohemi-galeria-preview.jpg"
TARGET = ROOT / "assets/img/nohemi-galeria-mejorada-2x.webp"
SOURCE_SHA256 = "526856530c09fd22e15695e84dbaf8d35e295b3d8ee128cc1edae8c8714e80c8"

def main() -> None:
    source_bytes = SOURCE.read_bytes()
    digest = hashlib.sha256(source_bytes).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError("Source portrait changed; inspect before processing")
    with Image.open(SOURCE) as original:
        original = ImageOps.exif_transpose(original).convert("RGB")
        if original.size != (936, 716):
            raise ValueError(f"Unexpected portrait dimensions: {original.size}")
        # Remove the dark document border, not the pictures or artist.
        photo = original.crop((31, 20, 923, 696))
        photo = ImageEnhance.Color(photo).enhance(1.035)
        photo = ImageEnhance.Contrast(photo).enhance(1.025)
        photo = photo.resize((1784, 1352), Image.Resampling.LANCZOS)
        photo = photo.filter(ImageFilter.UnsharpMask(radius=1.2, percent=62, threshold=3))
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        photo.save(TARGET, "WEBP", quality=83, method=6)
    with Image.open(TARGET) as test:
        if test.size != (1784, 1352):
            raise ValueError("Incorrect enhanced image dimensions")
    print(f"Created {TARGET} ({TARGET.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
