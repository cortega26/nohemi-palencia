#!/usr/bin/env python3
"""Lossless-geometry editorial crop of the artist-supplied catalog reference.

This does not claim a camera-resolution original. Keep source JPEG unchanged.
"""
import argparse,io
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'assets/obras/el-aroma-a-canelo-preview.jpg'
OUTPUT=ROOT/'assets/obras/el-aroma-a-canelo-reference-cropped.webp'
def generate():
    with Image.open(SOURCE) as original:
        im=original.convert('RGB')
    w,h=im.size
    if not (450<=w<=1200 and 600<=h<=1500):
        raise ValueError(f'Unexpected source size {im.size}')
    # Remove photographic black framing, without recropping painted edges.
    crop=im.crop((round(w*.048),round(h*.031),round(w*.946),round(h*.940)))
    out=io.BytesIO();crop.save(out,'WEBP',quality=92,method=6)
    return out.getvalue(),crop.size
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    raw,size=generate()
    if a.check:
        assert OUTPUT.is_file() and OUTPUT.read_bytes()==raw,'Reference out of sync'
    else:OUTPUT.write_bytes(raw)
    with Image.open(io.BytesIO(raw)) as im:
        assert im.format=='WEBP' and im.size==size
    print('Canelo: documented PDF reference, edge-cropped',size,len(raw),flush=True)
if __name__=='__main__':main()
