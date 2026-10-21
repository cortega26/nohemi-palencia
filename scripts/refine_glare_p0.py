#!/usr/bin/env python3
"""Faithful photographic glare correction of four artist-supplied source WebPs.

No image synthesis or detail reconstruction. Original source files are never
modified. Correct luminance only in softly masked areas, preserving geometry.
"""
import argparse,hashlib,io
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'assets/obras'
REGIONS={
'guardiana':[(.35,.23,.36,.30,.23),(.57,.54,.38,.31,.18),(.81,.28,.28,.31,.18)],
'vision-frontal-sueno-con-el-iznik':[(.32,.17,.39,.30,.39),(.64,.28,.37,.35,.30),(.56,.58,.31,.37,.16)],
'hilos-del-subconciente':[(.50,.10,.45,.24,.28),(.73,.33,.30,.28,.14),(.43,.63,.42,.34,.13)],
'atomica-ii':[(.48,.12,.49,.28,.24),(.14,.48,.25,.34,.12),(.85,.72,.27,.27,.07)]
}
def render(slug):
 with Image.open(ART/(slug+'-original-web.webp')) as im:
  assert im.format=='WEBP' and min(im.size)>1200
  src=im.convert('RGB');profile=im.info.get('icc_profile')
 pix=np.asarray(src,dtype=np.uint8);arr=pix.astype(np.float32)
 h,w=pix.shape[:2];yy,xx=np.ogrid[:h,:w];xx=xx/w;yy=yy/h
 mask=np.zeros((h,w),np.float32)
 for cx,cy,rx,ry,amp in REGIONS[slug]:
  field=amp*np.exp(-2*(((xx-cx)/rx)**2+((yy-cy)/ry)**2))
  np.maximum(mask,field,out=mask)
 grey=.299*arr[:,:,0]+.587*arr[:,:,1]+.114*arr[:,:,2]
 mx=np.max(arr,axis=2);mn=np.min(arr,axis=2)
 saturation=(mx-mn)/np.maximum(mx,1)
 light=np.clip((grey-76)/173,0,1)**.88
 veil=np.clip(mask*light*(1-.32*saturation)*1.65,0,.5)
 gs=np.asarray(src.convert('L').filter(ImageFilter.GaussianBlur(radius=3.2)),dtype=np.float32)
 glint=np.clip((grey-gs-9)/32,0,1)*veil*.24
 blurred=np.asarray(src.filter(ImageFilter.GaussianBlur(radius=2.2)),dtype=np.float32)
 details=np.clip(arr-blurred,-12,12)
 edited=np.clip((arr*(1-.94*veil[:,:,None])+details*(veil*.18)[:,:,None])*(1-glint[:,:,None]),0,255).astype(np.uint8)
 delta=np.abs(edited.astype(np.float32)-arr)
 if not .7<float(delta.mean())<16 or delta.max()>175:raise ValueError('Excessive or trivial change')
 output=io.BytesIO();kw=dict(format='WEBP',quality=90,method=6)
 if profile:kw['icc_profile']=profile
 Image.fromarray(edited).save(output,**kw)
 return output.getvalue(),src.size,round(float(delta.mean()),2)
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
 for slug in REGIONS:
  raw,size,mean=render(slug);path=ART/(slug+'-studio-original-web.webp')
  if args.check:
   assert path.is_file() and path.read_bytes()==raw,f'Stale or missing {slug}'
  else:path.write_bytes(raw)
  with Image.open(io.BytesIO(raw)) as im:assert im.size==size and im.format=='WEBP'
  print(f'{slug}: mean RGB correction {mean}/255; size {size}; bytes {len(raw)}',flush=True)
if __name__=='__main__':main()
