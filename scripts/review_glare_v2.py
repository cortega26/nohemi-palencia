#!/usr/bin/env python3
"""Candidate glare reduction for photographic REVIEW ONLY.

Preserves the original photograph and all dimensions, painted geometry and text.
Identifies isolated high-luminance neutral specular glints inside manually
chosen photographic regions and softly blends those pixels with a local RGB
median. Never inpaints/makes up artwork details. Produces diagnostic previews
that MUST pass visual scrutiny before any catalogue image is changed.
"""
import io
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'assets/obras'
OUT=ROOT/'assets/review'
# Ellipse centers/radii normalized to original image dimensions, not web viewport.
# (cx,cy,rx,ry,weight), broad-luminance attenuation amount.
CROPS={
 'guardiana': (
     [(0.49,0.21,0.35,0.28,0.88),(0.78,0.21,0.25,0.29,0.68),
      (0.52,0.56,0.38,0.28,0.48)], 0.042),
 'vision-frontal-sueno-con-el-iznik': (
     [(0.28,0.18,0.38,0.27,0.99),(0.59,0.33,0.43,0.33,0.96),
      (0.16,0.42,0.19,0.26,0.70)],0.073),
 'hilos-del-subconciente': (
     [(0.44,0.12,0.48,0.23,0.87),(0.59,0.28,0.28,0.18,0.53)],0.041),
 'atomica-ii': (
     [(0.52,0.12,0.49,0.22,0.87),(0.89,0.27,0.17,0.18,0.38)],0.044),
}
def process(slug):
    path=SOURCE/f'{slug}-original-web.webp'
    with Image.open(path) as source:
        assert source.format=='WEBP'
        pix=np.array(source.convert('RGB'),dtype=np.uint8)
        icc=source.info.get('icc_profile')
    h,w=pix.shape[:2]
    median=cv2.medianBlur(pix,9)
    y=(.2126*pix[:,:,0]+.7152*pix[:,:,1]+.0722*pix[:,:,2]).astype(np.float32)
    ym=(.2126*median[:,:,0]+.7152*median[:,:,1]+.0722*median[:,:,2]).astype(np.float32)
    mx=np.max(pix,axis=2).astype(np.float32)
    mn=np.min(pix,axis=2).astype(np.float32)
    sat=(mx-mn)/np.maximum(mx,1)
    medmax=np.max(median,axis=2).astype(np.float32)
    medmin=np.min(median,axis=2).astype(np.float32)
    medsat=(medmax-medmin)/np.maximum(medmax,1)
    yy,xx=np.ogrid[0:1:complex(h),0:1:complex(w)]
    local=np.zeros((h,w),np.float32)
    regions,broad=CROPS[slug]
    for cx,cy,rx,ry,weight in regions:
        norm=((xx-cx)/rx)**2+((yy-cy)/ry)**2
        local=np.maximum(local,weight*np.exp(-2.1*norm).astype(np.float32))
    reflect=np.clip((y-ym-18)/33,0,1)
    high=np.clip((y-95)/95,0,1)
    near_neutral=np.clip((.51-sat)/.34,0,1)
    desaturated=np.clip((medsat-sat+.05)/.18,0,1)
    spec=reflect*high*np.maximum(near_neutral,desaturated)*local
    # Edge safe: only correct isolated glints, not broad painted color fields.
    strength=np.clip(spec*.93,0,.91).astype(np.float32)
    corrected=(pix.astype(np.float32)*(1-strength[...,None])+
               median.astype(np.float32)*strength[...,None])
    # Low-amplitude localized neutral veil correction; limit to brighter surfaces.
    soft=(local*broad*np.clip((y-105)/140,0,1)*255).astype(np.float32)
    corrected=np.clip(np.maximum(corrected-soft[:,:,None],pix.astype(np.float32)-105),0,255).astype(np.uint8)
    d=np.abs(corrected.astype(np.int16)-pix.astype(np.int16))
    active=local>.08
    altered=(d.max(axis=2)>8)
    src_outliers=int(((y-ym>35)&active&(y>155)).sum())
    y2=(.2126*corrected[:,:,0]+.7152*corrected[:,:,1]+.0722*corrected[:,:,2])
    out_outliers=int(((y2-ym>35)&active&(y2>155)).sum())
    metrics={
        'slug':slug,'dimensions':[w,h],
        'mean_abs_rgb_delta':round(float(d.mean()),2),
        'max_pixel_delta':int(d.max()),
        'changed_over_8_pct':round(float(altered.mean()*100),2),
        'specular_candidate_before':src_outliers,
        'specular_candidate_after':out_outliers,
        'outlier_reduction_pct':round(100*(src_outliers-out_outliers)/max(src_outliers,1),1),
        'outside_roi_mean_abs_delta':round(float(d[local<.02].mean()) if (local<.02).any() else 0,2)
    }
    # Not a claim of successful perceptual glare removal: only image diagnostics.
    if not 0<metrics['mean_abs_rgb_delta']<14 or metrics['max_pixel_delta']>135:
        raise ValueError(metrics)
    return corrected,icc,metrics

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    allstats=[]
    for slug in CROPS:
        arr,icc,metrics=process(slug)
        options={'format':'WEBP','quality':91,'method':6}
        if icc: options['icc_profile']=icc
        full=OUT/(slug+'-glare-v2.webp')
        Image.fromarray(arr).save(full,**options)
        preview=Image.fromarray(arr)
        preview.thumbnail((960,1600),Image.Resampling.LANCZOS)
        preview.save(OUT/(slug+'-glare-v2-preview.webp'),**options)
        allstats.append(metrics)
        print(json.dumps(metrics,ensure_ascii=False),flush=True)
    (OUT/'glare-v2-audit.json').write_text(json.dumps(allstats,indent=2,ensure_ascii=False)+'\n','utf-8')
if __name__=='__main__':main()
