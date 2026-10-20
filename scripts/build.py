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
    exhibitions = json.loads((ROOT / 'data/exposiciones.json').read_text(encoding='utf-8'))
    assert len(exhibitions) == 1, 'Expected one verified institutional exhibition'
    exhibition = exhibitions[0]
    assert exhibition['id'] == 'rostros-oniricos-2026'
    assert exhibition['fecha_evento'] == '2026-09-03'
    assert exhibition['obras_exhibidas_confirmadas'] == [], 'Do not infer exhibition membership from portfolio works'
    assert exhibition['fecha_cierre'] is None, 'Closing date not documented'
    assert exhibition['fuente_institucional'].startswith('https://comunidadcreativalosrios.cultura.gob.cl/events/')
    assert exhibition['fuente_declaracion'].startswith('https://comunidadcreativalosrios.cultura.gob.cl/catalogo/')
    def h(key):
        return html.escape(exhibition[key], quote=True)
    feature = f'''<section class="exhibition" id="exposicion" aria-labelledby="exhibition-title">
      <div class="shell exhibition-inner">
        <div class="exhibition-head">
          <p class="kicker"><span>02</span> / Exposición documentada · 2026</p>
          <p class="exhibition-edition">ARCHIVO EXPOSITIVO / VALDIVIA</p>
        </div>
        <div class="exhibition-content">
          <div class="exhibition-main">
            <p class="exhibition-pretitle">Galería Urbana Santo Tomás</p>
            <h2 id="exhibition-title">{h('titulo_evento')}<span>.</span></h2>
            <p class="exhibition-subtitle">Cartografía de lo invisible</p>
            <p class="exhibition-intro">La exposición se presentó en Valdivia en 2026. La figura femenina, la geometría y los elementos de la naturaleza forman parte de la investigación artística que Nohemi describe en su propia declaración.</p>
            <div class="exhibition-links">
              <a href="{h('fuente_institucional')}" target="_blank" rel="noopener noreferrer">Consultar registro de la exposición <span aria-hidden="true">↗</span></a>
              <a href="{h('fuente_declaracion')}" target="_blank" rel="noopener noreferrer">Leer la presentación de la artista <span aria-hidden="true">↗</span></a>
            </div>
          </div>
          <div class="exhibition-facts">
            <p class="exhibition-facts-title">Ficha de exposición</p>
            <dl>
              <div><dt>Presentación</dt><dd><time datetime="{h('fecha_evento')}">{h('fecha_presentacion')}</time></dd></div>
              <div><dt>Espacio</dt><dd>{h('espacio')}</dd></div>
              <div><dt>Ciudad</dt><dd>{h('ciudad')}</dd></div>
            </dl>
            <p class="exhibition-source">Fecha y sede documentadas por Comunidad Creativa de Los Ríos. El subtítulo procede del portafolio facilitado por la artista.</p>
          </div>
        </div>
      </div>
    </section>'''
    timeline = f'''<div class="timeline-item"><span class="year">2026</span><div><h4><a class="timeline-link" href="#exposicion">{h('titulo_evento')} <span aria-hidden="true">↗</span></a></h4><p>{h('espacio')} · {h('ciudad')}</p></div></div>'''
    schema = {"@context":"https://schema.org", "@type":"Person", "name":"Nohemi Palencia Cisneros", "jobTitle":"Artista plástica", "description":"Artista plástica venezolana radicada en Valdivia, Chile, dedicada al dibujo y la pintura.", "homeLocation":{"@type":"Place","name":"Valdivia, Chile"}, "sameAs":["https://www.instagram.com/nohe.palencia/"]}
    template = (ROOT / 'templates/index.html').read_text(encoding='utf-8')
    assert all(token in template for token in ('{{GALLERY_ITEMS}}', '{{SCHEMA_JSON}}', '{{EXHIBITION_FEATURE}}', '{{EXHIBITION_TIMELINE}}'))
    return (template.replace('{{GALLERY_ITEMS}}','\n'.join(cards))
                    .replace('{{EXHIBITION_FEATURE}}',feature)
                    .replace('{{EXHIBITION_TIMELINE}}',timeline)
                    .replace('{{SCHEMA_JSON}}',json.dumps(schema, ensure_ascii=False).replace('<','\\u003c')))

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
