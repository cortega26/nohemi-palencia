#!/usr/bin/env python3
"""Conservative, reversible photo-glare attenuation. No inpainting or painting reconstruction."""
import argparse
import hashlib
import io
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'assets/obras'
# Reference: EXIF-corrected crop dimensions and manually reviewed elliptical masks.
# Each ellipse is cx,cy,rx,ry,strength; scaled to current authorized WebP pixels.
REGIONS={
 'guardiana':((2730,1945),[(1400,515,860,650,.14),(2020,560,710,670,.12),(990,1160,750,560,.08)]),
 'vision-frontal-sueno-con-el-iznik':((2105,3075),[(820,680,780,610,.25),(1300,770,670,700,.18),(460,520,570,800,.10)])
}
def corrected(slug):
    path=ART/(slug+'-original-web.webp')
    with Image.open(path) as im:
        assert im.format=='WEBP',slug
        src=im.convert('RGB')
        icc=im.info.get('icc_profile')
    w,h=src.size
    if min(w,h)<1200: raise ValueError('Source too small: '+slug)
    rw,rh=REGIONS[slug][0]
    sx,sy=w/rw,h/rh
    y,x=np.ogrid[:h,:w]
    field=np.zeros((h,w),np.float32)
    for cx,cy,rx,ry,weight in REGIONS[slug][1]:
        field+=weight*np.exp(-2*((x-cx*sx)**2/(rx*sx)**2+(y-cy*sy)**2/(ry*sy)**2))
    field=np.clip(field,0,.28)
    rgb=np.asarray(src,dtype=np.uint8)
    hi=np.max(rgb,axis=2).astype(np.float32)
    lo=np.min(rgb,axis=2).astype(np.float32)
    sat=np.divide(hi-lo,np.maximum(hi,1))
    alpha=field*(np.clip((hi/255-.25)/.65,0,1)**.8)*(.5+.5*(1-sat))
    edit=np.clip((rgb.astype(np.float32)-alpha[:,:,None]*255)/(1-alpha[:,:,None]),0,255).astype(np.uint8)
    delta=np.abs(edit.astype(np.float32)-rgb.astype(np.float32))
    if not .2<delta.mean()<8 or delta.max()>65:
        raise ValueError(f'Unsafe change for {slug}: avg={delta.mean()} max={delta.max()}')
    output=io.BytesIO()
    kw={'format':'WEBP','quality':90,'method':6}
    if icc: kw['icc_profile']=icc
    Image.fromarray(edit,'RGB').save(output,**kw)
    return output.getvalue(),src.size,float(delta.mean()),float(delta.max())
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--check',action='store_true')
    args=p.parse_args()
    assert len(REGIONS)==2
    for slug in REGIONS:
        data,size,avg,maximum=corrected(slug)
        dest=ART/(slug+'-retouched-original-web.webp')
        if args.check:
            assert dest.exists(), f'Missing edited asset: {dest}'
            assert hashlib.sha256(dest.read_bytes()).digest()==hashlib.sha256(data).digest(),slug
        else:
            dest.write_bytes(data)
        with Image.open(io.BytesIO(data)) as check:
            assert check.size==size and check.format=='WEBP'
        print(f'{slug} {size} bytes={len(data)} mean_pixel_delta={avg:.2f} max_pixel_delta={maximum:.0f} checked={args.check}',flush=True)
if __name__=='__main__':main()
