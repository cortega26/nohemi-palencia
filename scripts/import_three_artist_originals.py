#!/usr/bin/env python3
"""One-shot import of three artist-authorized camera originals (20 Oct 2026).
Fetch expiring connector image URLs and produce faithful, EXIF-corrected WebP.
"""
import io
import os
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageOps

ROOT=Path(__file__).resolve().parents[1]
ARTWORKS=(
    ("AURA_I_URL","aura-cosmica-i-original-web.webp"),
    ("HUELLICHES_II_URL","huelliches-ii-original-web.webp"),
    ("PLUMAJE_AZUL_URL","plumaje-azul-original-web.webp"),
)
def run():
    dest=ROOT/"assets/obras"
    for key,filename in ARTWORKS:
        url=os.environ[key]
        if not url.startswith("https://"):
            raise ValueError("Expected signed HTTPS file URL")
        with urlopen(Request(url,headers={"User-Agent":"Nohemi-portfolio-import/1.0"}),timeout=90) as response:
            binary=response.read()
        if not (3_000_000<=len(binary)<=10_000_000):
            raise RuntimeError(f"Unexpected image source size for {filename}: {len(binary)}")
        with Image.open(io.BytesIO(binary)) as source:
            if source.size!=(4000,3000):
                raise RuntimeError(f"Unexpected camera photo size for {filename}: {source.size}")
            oriented=ImageOps.exif_transpose(source).convert("RGB")
            if oriented.size!=(3000,4000):
                raise RuntimeError(f"Unexpected EXIF orientation for {filename}: {oriented.size}")
            # Faithful photographic reproduction. No generative restoration/cropping.
            web=oriented.resize((1800,2400),Image.Resampling.LANCZOS)
            path=dest/filename
            web.save(path,"WEBP",quality=87,method=6)
        with Image.open(path) as probe:
            if probe.size!=(1800,2400):
                raise RuntimeError(f"Incorrect generated output for {filename}")
        print(f"Imported {filename}: 1800 x 2400, {path.stat().st_size} bytes",flush=True)

if __name__=="__main__":
    run()
