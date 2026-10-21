#!/usr/bin/env python3
"""Create faithful, frame-free reproductions of three documented paintings.

Sources are original JPEGs sent by Nohemi, NOT artwork-detail thumbnails.
Rectangles are manually inspected, in EXIF-normalized 3000x4000 coordinates,
and retain a safety margin around painted boundaries including signatures.
Existing full-frame photographic records in assets/obras remain untouched.
"""
import argparse
import hashlib
import io
import os
from pathlib import Path
from urllib.request import Request, urlopen
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ARTWORKS = {
    'aura-cosmica-i': ('17634.jpg',
        'c455aa11fc363b0e10d4f0634c874efa7adf7f91ed51c942c52709dc38ff0da9', (637,1060,2386,3532)),
    'huelliches-ii': ('17661.jpg',
        '80f2a2aeb6d0ee35a2f9dcdd3686af9e22241fda7881d5590a390278502fc76f', (709,711,2411,3265)),
    'plumaje-azul': ('17651.jpg',
        '15437b38a321530cb1ad28c09770e89025929861f48e16a0940ba8faf6daad95', (553,749,2350,3040)),
}
MAX_EDGE=2400

def process(slug, binary):
    filename, expected_sha, bounds = ARTWORKS[slug]
    assert hashlib.sha256(binary).hexdigest()==expected_sha, f'Unexpected source photograph: {slug}'
    with Image.open(io.BytesIO(binary)) as photo:
        assert photo.format=='JPEG' and photo.size==(4000,3000), f'Unexpected original: {slug}'
        assert photo.getexif().get(274)==6, f'Unexpected EXIF orientation: {slug}'
        oriented=ImageOps.exif_transpose(photo).convert('RGB')
        assert oriented.size==(3000,4000)
        art=oriented.crop(bounds)
        assert art.width>1500 and art.height>2200
        if max(art.size)>MAX_EDGE:
            scale=MAX_EDGE/max(art.size)
            art=art.resize(tuple(round(x*scale) for x in art.size),Image.Resampling.LANCZOS)
        buf=io.BytesIO()
        art.save(buf,'WEBP',quality=90,method=6,icc_profile=photo.info.get('icc_profile',b''))
    return art.size,buf.getvalue()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-dir',type=Path,default=None)
    args=parser.parse_args()
    for slug,(filename,expected_sha,bounds) in ARTWORKS.items():
        if args.source_dir:
            binary=(args.source_dir/filename).read_bytes()
        else:
            key=slug.upper().replace('-','_')+'_URL'
            url=os.environ[key]
            assert url.startswith('https://'), f'Expected HTTPS source for {slug}'
            with urlopen(Request(url,headers={'User-Agent':'Nohemi-artwork-reframe/1.0'}),timeout=90) as response:
                binary=response.read()
        if not 2_000_000<len(binary)<9_000_000:
            raise ValueError(f'Unexpected JPEG file size: {slug}')
        dimensions,webp=process(slug,binary)
        destination=ROOT/'assets'/'obras'/f'{slug}-reframed-original-web.webp'
        destination.write_bytes(webp)
        with Image.open(io.BytesIO(webp)) as verify:
            assert verify.format=='WEBP' and verify.size==dimensions
        print(f'{slug} source={filename} crop={bounds} output={dimensions} bytes={len(webp)} SHA256={hashlib.sha256(webp).hexdigest()}',flush=True)
if __name__=='__main__':
    main()
