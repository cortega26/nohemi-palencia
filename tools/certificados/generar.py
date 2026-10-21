#!/usr/bin/env python3
"""Produce unsigned A4 authenticity certificates from the canonical catalog.
No buyer data, invented signatures, assigned serials, or fake government marks.
Requires ReportLab+Pillow for PDF output; --check needs stdlib only.
"""
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FOUR=("princesa-onirica","shitikari","hindu-celular","vision-frontal-sueno-con-el-iznik")
def catalog(slugs=FOUR):
    records=json.loads((ROOT/"data/obras.json").read_text(encoding="utf-8"))
    lookup={r["slug"]:r for r in records}
    if len(lookup)!=len(records):raise ValueError("Repeated artwork slug")
    if not slugs or len(set(slugs))!=len(slugs):raise ValueError("Repeated or empty selection")
    out=[]
    for slug in slugs:
        if slug not in lookup:raise ValueError("Unknown artwork "+slug)
        r=lookup[slug];src=ROOT/"assets/obras"/r["archivo"]
        if not src.is_file():raise FileNotFoundError(src)
        assert r["titulo"] and r["anio"] and r["tecnica"] and r["dimensiones"]
        out.append((r,src))
    return out
def render(output,records):
    from PIL import Image
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor
    from reportlab.lib.utils import ImageReader,simpleSplit
    W,H=A4
    output.parent.mkdir(parents=True,exist_ok=True)
    pdf=canvas.Canvas(str(output),pagesize=A4)
    pdf.setTitle("Certificados privados sin emitir - Nohemi Palencia")
    for work,src in records:
        pdf.setFillColor(HexColor("#f9f8f3"));pdf.rect(0,0,W,H,fill=1,stroke=0)
        pdf.setFillColor(HexColor("#24372d"));pdf.setFont("Times-Roman",24)
        pdf.drawString(56,H-82,"Nohemi Palencia")
        pdf.setFont("Helvetica",9);pdf.drawRightString(W-56,H-82,"CISNEROS  -  ARTISTA PLÁSTICA")
        pdf.line(56,H-95,W-56,H-95)
        pdf.setFont("Helvetica-Bold",10);pdf.drawString(56,H-130,"CERTIFICADO DE AUTENTICIDAD")
        pdf.setFont("Times-Roman",17);pdf.drawString(56,H-159,"Obra original")
        with Image.open(src) as image:
            im=image.convert("RGB")
        w,h=im.size;scale=min(220/w,325/h)
        pdf.drawImage(ImageReader(im),57+(220-w*scale)/2,H-521+(325-h*scale)/2,width=w*scale,height=h*scale)
        fields=[("TÍTULO",work["titulo"]),("AÑO",str(work["anio"])),("TÉCNICA Y SOPORTE",work["tecnica"]),("DIMENSIONES",work["dimensiones"]),("IDENTIFICACIÓN","NPC-______________")]
        y=H-207
        for label,value in fields:
            pdf.setFillColor(HexColor("#496553"));pdf.setFont("Helvetica-Bold",8.5);pdf.drawString(304,y,label)
            y-=20;pdf.setFillColor(HexColor("#24372d"));pdf.setFont("Times-Roman",12)
            for line in simpleSplit(value,"Times-Roman",12,224):
                pdf.drawString(304,y,line);y-=15
            y-=24
        pdf.setFont("Helvetica-Bold",9);pdf.drawString(56,H-560,"DECLARACIÓN DE AUTENTICIDAD")
        body=("Yo, Nohemi Palencia Cisneros, declaro que esta pintura es una creación original de mi autoría, identificada mediante los datos precedentes y reconocida con mi firma manuscrita.")
        pdf.setFont("Helvetica",10)
        for i,line in enumerate(simpleSplit(body,"Helvetica",10,W-112)):
            pdf.drawString(56,H-581-i*16,line)
        pdf.line(56,190,W-56,190)
        pdf.setFont("Helvetica",9);pdf.drawString(56,168,"Lugar y fecha de emisión: ______________________________________________")
        pdf.line(322,111,W-56,111)
        pdf.setFont("Helvetica-Bold",9);pdf.drawCentredString(422,96,"Firma de la artista")
        pdf.line(56,82,W-56,82)
        pdf.setFont("Helvetica",7.8)
        pdf.drawString(56,66,"La compra del original no implica cesión de derechos de reproducción comercial.")
        pdf.drawString(56,54,"Ley 17.336, art. 37. No sustituye comprobante tributario ni inscripción estatal.")
        pdf.setFont("Helvetica-Bold",7.5)
        pdf.drawString(56,39,"MODELO SIN EMITIR - REQUIERE CÓDIGO ÚNICO, FECHA Y FIRMA")
        pdf.showPage()
    pdf.save()
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--check",action="store_true")
    p.add_argument("--slug",action="append",dest="slugs")
    p.add_argument("--out",type=Path,default=Path("/tmp/nohemi-certificados"))
    a=p.parse_args()
    items=catalog(tuple(a.slugs) if a.slugs else FOUR)
    print("Validated:",", ".join(w["titulo"] for w,_ in items))
    if not a.check:
        render(a.out/"certificados_sin_firma.pdf",items)
if __name__=="__main__":main()
