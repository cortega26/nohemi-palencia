#!/usr/bin/env python3
"""Headless rendered visual/accessibility smoke audit of the PUBLIC live site.

Evidence is generated only on an ephemeral GitHub Actions branch. No site writes.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "https://nohemipalencia.com"
OUT = Path("visual-audit/evidence")
OUT.mkdir(parents=True, exist_ok=True)
SLUGS = [
    "guardiana","princesa-onirica","vision-frontal-sueno-con-el-iznik",
    "hilos-del-subconciente","shitikari","atomica-ii","sacerdotiza-solar",
    "hindu-celular","guardiana-del-umbral","el-aroma-a-canelo",
    "aura-cosmica-ii","huelliches-ii","plumaje-azul",
]
SIZES = {"desktop":(1440,900),"tablet":(768,900),"phone":(390,844),"compact":(320,720)}
report={"origin":BASE,"viewports":{},"pages":{},"console_errors":[],"request_errors":[],"screenshots":[]}
bad_pages=[]
def shot(page,name,selector=None,full=False):
    dest=OUT/(name+".jpg")
    try:
        if selector:
            loc=page.locator(selector).first
            if loc.count() and loc.is_visible(timeout=2500):
                loc.screenshot(path=str(dest),type="jpeg",quality=78,animations="disabled",timeout=22000)
            else:return False
        else:
            page.screenshot(path=str(dest),type="jpeg",quality=76,full_page=full,animations="disabled",timeout=22000)
        report["screenshots"].append(str(dest))
        return True
    except Exception as exc:
        report.setdefault("screenshot_warnings",[]).append({"name":name,"error":str(exc)[:180]})
        return False
def scan(page):
    return page.evaluate("""() => {
      const els=[...document.querySelectorAll('main img, footer img, .upcoming-work img, .gallery-grid img')];
      const broken=els.filter(e=>e.complete && (!e.naturalWidth||!e.naturalHeight)).map(e=>e.currentSrc||e.src);
      const waiting=els.filter(e=>!e.complete).length;
      const w=document.documentElement.clientWidth;
      const wide=[...document.querySelectorAll('body *')]
        .filter(e=>{const r=e.getBoundingClientRect();const cs=getComputedStyle(e);
         return r.width>0 && cs.position!=='fixed' && r.right>w+3 && r.left<w && !['SCRIPT','STYLE'].includes(e.tagName)})
        .slice(0,25).map(e=>({tag:e.tagName,cls:typeof e.className==='string'?e.className.slice(0,90):'',
          text:(e.textContent||'').trim().slice(0,70),right:Math.round(e.getBoundingClientRect().right)}));
      const thumbs=[...document.querySelectorAll('.upcoming-work')].map(e=>{
         const ir=e.querySelector('img')?.getBoundingClientRect();const cap=e.querySelector('span')?.getBoundingClientRect();
         return {name:(e.querySelector('span')?.textContent||'').trim(),imageMid:ir?+(ir.x+ir.width/2).toFixed(1):null,
          captionMid:cap?+(cap.x+cap.width/2).toFixed(1):null,captionWidth:cap?.width||0}
      });
      const undersized=[...document.querySelectorAll('a,button')].filter(e=>{
          const r=e.getBoundingClientRect();return r.width>0 && r.height>0 && (r.width<24||r.height<24);})
          .slice(0,22).map(e=>({tag:e.tagName,text:(e.textContent||'').trim().slice(0,55),
           w:Math.round(e.getBoundingClientRect().width),h:Math.round(e.getBoundingClientRect().height)}));
      return {viewport:w,scrollWidth:document.documentElement.scrollWidth,bodyScrollWidth:document.body.scrollWidth,
        images:els.length,broken,waiting,wide,thumbs,undersized,
        fontsReady:document.fonts.status,headings:[...document.querySelectorAll('h1')].map(e=>e.innerText)};
    }""")
with sync_playwright() as play:
    browser=play.chromium.launch(headless=True,args=["--no-sandbox","--disable-dev-shm-usage"])
    for label,(width,height) in SIZES.items():
        page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1,is_mobile=(label in ("phone","compact")),has_touch=(label in ("phone","compact")),reduced_motion="reduce")
        errors=[];page.on("pageerror",lambda e: errors.append(str(e)[:200]))
        resp=page.goto(BASE+"/",wait_until="networkidle",timeout=35000)
        page.evaluate("document.fonts.ready")
        page.locator(".gallery-grid img").last.scroll_into_view_if_needed()
        page.wait_for_timeout(700)
        page.evaluate("scrollTo(0,0)")
        data=scan(page);data["http_status"]=resp.status if resp else None
        data["js_errors"]=errors
        report["viewports"][label]=data
        shot(page,label+"_hero")
        if label in ("desktop","phone","compact"):
            shot(page,label+"_ca660",".upcoming-selected")
            shot(page,label+"_gallery",".gallery-grid")
            shot(page,label+"_footer",".site-footer")
            if label!="compact":shot(page,label+"_full",full=True)
        link=page.locator("[data-artwork]").first
        if link.count() and label in ("desktop","phone"):
            link.click()
            page.wait_for_timeout(100)
            is_open=page.locator("#artwork-dialog").evaluate("(el)=>el.open")
            shot(page,label+"_lightbox","#artwork-dialog")
            page.keyboard.press("Escape")
            data["lightbox_opened"]=is_open
            data["lightbox_escape_closed"]=not page.locator("#artwork-dialog").evaluate("(el)=>el.open")
        if data["scrollWidth"]>width+3 or data["broken"] or errors:
            bad_pages.append({"name":label,"error":"overflow, broken images, or page script error"})
        page.close()
    # All permanent routes and exhibition, at 390px; sample artwork detail also at 1440px.
    for ix,slug in enumerate(SLUGS):
        page=browser.new_page(viewport={"width":390,"height":844},device_scale_factor=1,reduced_motion="reduce")
        errors=[];page.on("pageerror",lambda e: errors.append(str(e)[:200]))
        url=f"{BASE}/obras/{slug}/"
        response=page.goto(url,wait_until="networkidle",timeout=35000)
        page.evaluate("document.fonts.ready")
        page.locator(".artwork-detail-figure img").scroll_into_view_if_needed()
        page.wait_for_timeout(100)
        d=scan(page);d["http_status"]=response.status if response else None;d["js_errors"]=errors
        report["pages"][slug]=d
        if slug in ["guardiana","el-aroma-a-canelo","vision-frontal-sueno-con-el-iznik"]:
            shot(page,"detail_phone_"+slug,full=True)
        if d["scrollWidth"]>393 or d["broken"] or errors:bad_pages.append({"name":slug,"error":"overflow, broken images or script error"})
        page.close()
    for name,path in [("exposition","/exposiciones/rostros-oniricos/")]:
        p=browser.new_page(viewport={"width":390,"height":844},device_scale_factor=1,reduced_motion="reduce")
        resp=p.goto(BASE+path,wait_until="networkidle",timeout=35000)
        d=scan(p);d["http_status"]=resp.status if resp else None
        report["pages"][name]=d
        shot(p,name+"_phone",full=True)
        if d["scrollWidth"]>393 or d["broken"]:bad_pages.append({"name":name,"error":"overflow/broken images"})
        p.close()
    browser.close()
report["critical"]=bad_pages
(OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"viewports":{k:{"scroll":v["scrollWidth"],"viewport":v["viewport"],"broken":v["broken"],"wide":v["wide"],"under":v["undersized"],"thumbs":v["thumbs"],"modal":v.get("lightbox_opened")} for k,v in report["viewports"].items()},"routeCount":len(report["pages"]),"failures":bad_pages,"shots":report["screenshots"]},ensure_ascii=False))
if bad_pages: print("Visual audit found defects; evidence committed for review.",flush=True)
