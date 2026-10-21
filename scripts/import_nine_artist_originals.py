#!/usr/bin/env python3
"""Artist-authorized camera photographs -> faithful border-free WebP reproductions.
One-shot import: crop only photographic surround (wall/frame/mat), not artwork.
Coordinates reference EXIF-corrected pixels. SHA gates prevent file mix-ups.
"""
import hashlib,io,os
from pathlib import Path
from urllib.request import urlopen,Request
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[1]
ARTWORKS={
 'guardiana':('17677.jpg','9ee611baf0d0984c',(110,195,2840,2140)),
 'hilos-del-subconciente':('17679.jpg','67c83ab0c2712e9e',(286,468,2643,3440)),
 'guardiana-del-umbral':('17678.jpg','2e0c2d8d7c1b0e0e',(575,480,2440,3430)),
 'vision-frontal-sueno-con-el-iznik':('17673.jpg','9762dcfd0bd1365b',(480,460,2585,3535)),
 'sacerdotiza-solar':('17663.jpg','cb1dc32fe0c4d905',(572,685,2440,3260)),
 'princesa-onirica':('17662.jpg','48a5b173a7833f51',(430,480,2670,3460)),
 'atomica-ii':('17659.jpg','25297d2c5d5694b',(579,728,2404,3237)),
 'hindu-celular':('17653.jpg','ac43f6d654d3f2a7',(569,715,2410,3228)),
 'shitikari':('17652.jpg','a47e854efef25743',(750,860,2315,3058)),
}
def process_bytes(slug,data,dest):
    name,prefix,crop=ARTWORKS[slug]
    digest=hashlib.sha256(data).hexdigest()
    if not digest.startswith(prefix): raise ValueError(f'{slug}: wrong source SHA-256')
    with Image.open(io.BytesIO(data)) as source:
        rgb=ImageOps.exif_transpose(source).convert('RGB')
        expected=(3000,2353) if slug=='guardiana' else (3000,4000)
        if rgb.size!=expected: raise ValueError(f'{slug}: unexpected dimensions {rgb.size}')
        l,t,r,b=crop
        if not (0<=l<r<=rgb.width and 0<=t<b<=rgb.height): raise ValueError('crop bounds')
        art=rgb.crop(crop)
        if max(art.size)>2400:
            art=art.resize(tuple(round(v*2400/max(art.size)) for v in art.size),Image.Resampling.LANCZOS)
        dest.parent.mkdir(parents=True,exist_ok=True)
        art.save(dest,'WEBP',quality=88,method=6,icc_profile=source.info.get('icc_profile',b''))
        with Image.open(dest) as probe:
            if probe.format!='WEBP' or probe.size!=art.size: raise AssertionError('broken WebP export')
        print(f'{slug}: {art.size}, {dest.stat().st_size} bytes, source sha256={digest}',flush=True)
def run():
    for slug,(filename,_,_) in ARTWORKS.items():
        key=slug.upper().replace('-','_')+'_URL'
        if os.getenv('PHOTO_SOURCE_DIR'): data=(Path(os.environ['PHOTO_SOURCE_DIR'])/filename).read_bytes()
        else:
            url=os.environ[key]
            if not url.startswith('https://'): raise ValueError('source must be signed HTTPS URL')
            with urlopen(Request(url,headers={'User-Agent':'Nohemi-portfolio-import/2.0'}),timeout=90) as response: data=response.read()
        if not 1_000_000<=len(data)<=12_000_000: raise ValueError(f'{slug}: unexpected JPG size')
        process_bytes(slug,data,ROOT/'assets/obras'/f'{slug}-original-web.webp')
if __name__=='__main__':run()
