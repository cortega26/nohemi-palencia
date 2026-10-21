#!/usr/bin/env python3
"""Apply the documented 2026-10-21 P0 source corrections once."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def patch(path,old,new):
 f=R/path;s=f.read_text('utf-8')
 if s.count(old)!=1:raise ValueError(f'Unexpected source: {path}: {old[:60]}')
 f.write_text(s.replace(old,new),'utf-8')
wpath=R/'data/obras.json';works=json.loads(wpath.read_text('utf-8'))
slugs={'guardiana','vision-frontal-sueno-con-el-iznik','hilos-del-subconciente','atomica-ii'}
for w in works:
 if w['slug'] in slugs:
  w['archivo']=w['slug']+'-studio-original-web.webp'
  w['archivo_original_sin_retoque']=w['slug']+'-original-web.webp'
  w['retoque_fotografico']='Corrección tonal reversible, localizada y no generativa de brillo fotográfico; fuente archivada intacta.'
 if w['slug']=='el-aroma-a-canelo':
  assert w['tecnica']=='Técnica mixta sobre MDF'
  w['archivo']='el-aroma-a-canelo-reference-cropped.webp'
  w['fuente_soporte']='MDF confirmado por el responsable del sitio el 21-10-2026.'
  w['fuente_documental']='Fotografía de referencia del catálogo proporcionado por Nohemi, reencuadrada sin ampliar resolución. No es original de cámara HD.'
assert len(works)==13
wpath.write_text(json.dumps(works,indent=2,ensure_ascii=False)+'\n','utf-8')
p=R/'data/confirmaciones-artista.json';c=json.loads(p.read_text('utf-8'))
c['titulo_canelo']['soporte_confirmado']='MDF'
c['titulo_canelo']['soporte_estado']='MDF, confirmado por el responsable del sitio; prevalece sobre la ficha previa que decía lienzo.'
p.write_text(json.dumps(c,indent=2,ensure_ascii=False)+'\n','utf-8')
patch('scripts/build.py',
'Imagen provisional del catálogo; fotografía original pendiente.',
'Imagen documental reencuadrada sin ampliación digital; fotografía original de cámara HD pendiente.')
patch('tests/test_site.py',
"'-retouched-original-web.webp' if slug in ('guardiana','vision-frontal-sueno-con-el-iznik')",
"'-studio-original-web.webp' if slug in ('guardiana','vision-frontal-sueno-con-el-iznik','hilos-del-subconciente','atomica-ii')")
patch('tests/test_site.py','def test_retouched_paintings_are_reversible_and_only_two(self):',
'def test_four_reversible_photo_corrections(self):')
patch('tests/test_site.py',"treated=('guardiana','vision-frontal-sueno-con-el-iznik')",
"treated=('guardiana','vision-frontal-sueno-con-el-iznik','hilos-del-subconciente','atomica-ii')")
patch('tests/test_site.py',"self.html.count('-retouched-original-web.webp'),2",
"self.html.count('-studio-original-web.webp'),4")
patch('tests/test_site.py','Imagen provisional del catálogo; fotografía original pendiente.',
'Imagen documental reencuadrada sin ampliación digital; fotografía original de cámara HD pendiente.')
p=R/'README.md';p.write_text(p.read_text('utf-8')+'\n## Cierre editorial P0 21-10-2026\nEl aroma a canelo: **MDF**, confirmado por el responsable. La reproducción fotográfica actual se reencuadra desde el archivo suministrado por la artista, sin aumento artificial de píxeles; no se recibió fotografía HD de cámara. Guardiana, Visión frontal / Sueño con el Iznik, Hilos del subconciente y Atómica II tienen corrección localizada, no generativa, de la luz reflejada, y se conservan intactas sus fuentes.\n','utf-8')
print('P0 metadata migrated: four paintings + Canelo MDF',flush=True)
