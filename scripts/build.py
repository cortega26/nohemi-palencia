#!/usr/bin/env python3
"""Compile the data-driven portfolio to a fully static, SEO-readable HTML file."""
import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def render():
    works = json.loads((ROOT / 'data/obras.json').read_text(encoding='utf-8'))
    assert len(works) == 11, 'Expected 11 artworks sourced from the artist portfolio'
    seen = set()
    cards = []
    for i, w in enumerate(works, 1):
        assert w['slug'] not in seen, f"Duplicate artwork slug: {w['slug']}"
        seen.add(w['slug'])
        assert all(w.get(k) for k in ('titulo', 'tecnica', 'dimensiones', 'anio', 'archivo', 'pagina_pdf')), w
        assert 3 <= w['pagina_pdf'] <= 13
        image = ROOT / 'assets/obras' / w['archivo']
        assert image.is_file() and image.stat().st_size > 100, f"Missing artwork image: {image}"
        esc = lambda s: html.escape(str(s), quote=True)
        img_path = f"assets/obras/{w['archivo']}"
        details = f"{w['tecnica']} · {w['dimensiones']} · {w['anio']}"
        cards.append(f'''<article class="artwork {'artwork-feature' if w.get('destacada') else ''}" id="obra-{esc(w['slug'])}">
  <a class="artwork-link" href="{esc(img_path)}" data-artwork data-title="{esc(w['titulo'])}" data-details="{esc(details)}" data-number="{i:02d} / 11" aria-label="Ampliar {esc(w['titulo'])}, {esc(details)}">
    <div class="artwork-image"><img src="{esc(img_path)}" alt="{esc(w['titulo'])}, obra de Nohemi Palencia Cisneros" loading="lazy" decoding="async"><span class="artwork-zoom" aria-hidden="true">↗</span></div>
  </a>
  <div class="artwork-info"><div><span class="artwork-number">{i:02d} / 11</span><h3>{esc(w['titulo'])}</h3><p>{esc(w['tecnica'])} · {esc(w['dimensiones'])}</p></div><span class="artwork-year">{w['anio']}</span></div>
</article>''')
    schema = {"@context":"https://schema.org", "@type":"Person", "name":"Nohemi Palencia Cisneros", "jobTitle":"Artista plástica", "description":"Artista plástica venezolana radicada en Valdivia, Chile, dedicada al dibujo y la pintura.", "homeLocation":{"@type":"Place","name":"Valdivia, Chile"}, "sameAs":["https://www.instagram.com/nohe.palencia/"]}
    template = (ROOT / 'templates/index.html').read_text(encoding='utf-8')
    assert '{{GALLERY_ITEMS}}' in template and '{{SCHEMA_JSON}}' in template
    return template.replace('{{GALLERY_ITEMS}}','\n'.join(cards)).replace('{{SCHEMA_JSON}}',json.dumps(schema, ensure_ascii=False).replace('<','\\u003c'))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true',help='Fail when generated index.html is stale')
    args=parser.parse_args()
    expected=render()+'\n'
    output=ROOT/'index.html'
    if args.check:
        assert output.exists() and output.read_text(encoding='utf-8')==expected, 'index.html is out of sync. Run python3 scripts/build.py'
        print('Generated HTML is up to date')
    else:
        output.write_text(expected,encoding='utf-8');print(f'Built {output}')
