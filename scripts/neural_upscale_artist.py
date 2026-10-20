#!/usr/bin/env python3
"""Reproducible 2x neural upscale from the original portfolio photograph.
Weights: RealESRGAN_x2plus, SHA-256 pinned. AI detail is blended with the
unaltered documentary image so faces and paintings are not freely regenerated.
"""
from __future__ import annotations
import argparse
import hashlib
import os
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import torch
from torch import nn
from torch.nn import functional as F

SOURCE_SHA256 = "526856530c09fd22e15695e84dbaf8d35e295b3d8ee128cc1edae8c8714e80c8"
WEIGHTS_SHA256 = "49fafd45f8fd7aa8d31ab2a22d14d91b536c34494a5cfe31eb5d89c2fa266abb"

class ResidualDenseBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1=nn.Conv2d(64,32,3,1,1)
        self.conv2=nn.Conv2d(96,32,3,1,1)
        self.conv3=nn.Conv2d(128,32,3,1,1)
        self.conv4=nn.Conv2d(160,32,3,1,1)
        self.conv5=nn.Conv2d(192,64,3,1,1)
        self.lrelu=nn.LeakyReLU(.2,inplace=True)
    def forward(self,x):
        a=self.lrelu(self.conv1(x))
        b=self.lrelu(self.conv2(torch.cat([x,a],1)))
        c=self.lrelu(self.conv3(torch.cat([x,a,b],1)))
        d=self.lrelu(self.conv4(torch.cat([x,a,b,c],1)))
        e=self.conv5(torch.cat([x,a,b,c,d],1))
        return x+.2*e

class RRDB(nn.Module):
    def __init__(self):
        super().__init__()
        self.rdb1=ResidualDenseBlock()
        self.rdb2=ResidualDenseBlock()
        self.rdb3=ResidualDenseBlock()
    def forward(self,x):
        return x+.2*self.rdb3(self.rdb2(self.rdb1(x)))

class RRDBNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_first=nn.Conv2d(12,64,3,1,1)
        self.body=nn.Sequential(*(RRDB() for _ in range(23)))
        self.conv_body=nn.Conv2d(64,64,3,1,1)
        self.conv_up1=nn.Conv2d(64,64,3,1,1)
        self.conv_up2=nn.Conv2d(64,64,3,1,1)
        self.conv_hr=nn.Conv2d(64,64,3,1,1)
        self.conv_last=nn.Conv2d(64,3,3,1,1)
        self.lrelu=nn.LeakyReLU(.2,inplace=True)
    def forward(self,x):
        x=F.pixel_unshuffle(x,2)
        feat=self.conv_first(x)
        feat=feat+self.conv_body(self.body(feat))
        feat=self.lrelu(self.conv_up1(F.interpolate(feat,scale_factor=2,mode='nearest')))
        feat=self.lrelu(self.conv_up2(F.interpolate(feat,scale_factor=2,mode='nearest')))
        return self.conv_last(self.lrelu(self.conv_hr(feat)))

@torch.inference_mode()
def tiled(net,image,step=224,pad=14):
    arr=np.asarray(image).astype(np.float32)/255
    h,w=arr.shape[:2]
    x=torch.from_numpy(arr.transpose(2,0,1)).unsqueeze(0)
    out=np.zeros((h*2,w*2,3),dtype=np.uint8)
    n=0
    for top in range(0,h,step):
        for left in range(0,w,step):
            bottom,right=min(h,top+step),min(w,left+step)
            t,l=max(0,top-pad),max(0,left-pad)
            b,r=min(h,bottom+pad),min(w,right+pad)
            part=x[:,:,t:b,l:r]
            ih,iw=part.shape[-2:]
            part=F.pad(part,(0,iw%2,0,ih%2),mode='reflect')
            pred=net(part).clamp(0,1)[:,:,:ih*2,:iw*2]
            crop=pred[:,:,(top-t)*2:(bottom-t)*2,(left-l)*2:(right-l)*2]
            out[top*2:bottom*2,left*2:right*2]=(
                crop[0].permute(1,2,0).numpy()*255).round().astype(np.uint8)
            n+=1
            print('Neural tile:',n,flush=True)
    return Image.fromarray(out)

def main():
    p=argparse.ArgumentParser()
    for name in ['source','weights','output']:
        p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args()
    for path,expected in [(a.source,SOURCE_SHA256),(a.weights,WEIGHTS_SHA256)]:
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
            raise RuntimeError(f'Hash mismatch: {path}')
    source=ImageOps.exif_transpose(Image.open(a.source)).convert('RGB')
    assert source.size==(936,716)
    source=source.crop((31,20,923,696))
    torch.set_num_threads(min(4,max(1,os.cpu_count() or 2)))
    model=RRDBNet().eval()
    weights=torch.load(a.weights,map_location='cpu',weights_only=True)
    model.load_state_dict(weights.get('params_ema',weights.get('params',weights)),strict=True)
    neural=tiled(model,source)
    faithful=source.resize(neural.size,Image.Resampling.LANCZOS)
    # Intentionally retain documentary structure instead of synthesizing facial features.
    image=Image.blend(faithful,neural,.84)
    image=ImageEnhance.Contrast(image).enhance(1.04)
    image=ImageEnhance.Color(image).enhance(1.035)
    image=image.filter(ImageFilter.UnsharpMask(radius=.68,percent=45,threshold=3))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    image.save(a.output,'WEBP',quality=89,method=6)
    with Image.open(a.output) as saved:
        assert saved.size==(1784,1352)
    print('OUTPUT',a.output,'BYTES',a.output.stat().st_size,flush=True)

if __name__=='__main__':
    main()
