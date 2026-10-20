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
  <div class="artwork-info"><div><span class="artwork-number">{i:02d} / 11</span><h3>{esc(w['titulo'])}</h3><p>{esc(w['tecnica'])} · {esc(w['dimensiones'])}</p><a class="artwork-detail-link" href="obras/{esc(w['slug'])}/">Ficha de la obra <span aria-hidden="true">↗</span></a></div><span class="artwork-year">{w['anio']}</span></div>
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
              <a class="exhibition-detail-link" href="{h('ruta_permanente')}">Conocer la exposición <span aria-hidden="true">↗</span></a>
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
    timeline = f'''<div class="timeline-item"><span class="year">2026</span><div><h4><a class="timeline-link" href="{h('ruta_permanente')}">{h('titulo_evento')} <span aria-hidden="true">↗</span></a></h4><p>{h('espacio')} · {h('ciudad')}</p></div></div>'''
    schema = {"@context":"https://schema.org", "@type":"Person", "name":"Nohemi Palencia Cisneros", "jobTitle":"Artista plástica", "description":"Artista plástica venezolana radicada en Valdivia, Chile, dedicada al dibujo y la pintura.", "homeLocation":{"@type":"Place","name":"Valdivia, Chile"}, "sameAs":["https://www.instagram.com/nohe.palencia/"]}
    template = (ROOT / 'templates/index.html').read_text(encoding='utf-8')
    assert all(token in template for token in ('{{GALLERY_ITEMS}}', '{{SCHEMA_JSON}}', '{{EXHIBITION_FEATURE}}', '{{EXHIBITION_TIMELINE}}'))
    return (template.replace('{{GALLERY_ITEMS}}','\n'.join(cards))
                    .replace('{{EXHIBITION_FEATURE}}',feature)
                    .replace('{{EXHIBITION_TIMELINE}}',timeline)
                    .replace('{{SCHEMA_JSON}}',json.dumps(schema, ensure_ascii=False).replace('<','\\u003c')))

def render_exhibition():
    exhibitions = json.loads((ROOT / 'data/exposiciones.json').read_text(encoding='utf-8'))
    assert len(exhibitions) == 1
    ex = exhibitions[0]
    assert ex['id'] == 'rostros-oniricos-2026'
    assert ex['ruta_permanente'] == 'exposiciones/rostros-oniricos/'
    assert ex['obras_exhibidas_confirmadas'] == []
    assert ex['fecha_cierre'] is None
    confirmation = json.loads((ROOT / 'data/confirmaciones-artista.json').read_text(encoding='utf-8'))
    artist_works = confirmation['rostros_oniricos']
    assert artist_works['incluyo_otras_obras'] is True
    assert artist_works['otras_etapas_y_tecnicas'] is True
    assert artist_works['obra_especifica_confirmada'] == []
    assert ex['obras_exhibidas_confirmadas'] == []
    page = (ROOT / 'templates/exposicion-rostros-oniricos.html').read_text(encoding='utf-8')
    mapping = {
        '{{TITLE}}': ex['titulo_evento'],
        '{{SUBTITLE}}': ex['titulo_portafolio'].split(': ',1)[1],
        '{{DATE}}': ex['fecha_presentacion'],
        '{{ISO_DATE}}': ex['fecha_evento'],
        '{{VENUE}}': ex['espacio'],
        '{{CITY}}': ex['ciudad'],
        '{{EVENT_URL}}': ex['fuente_institucional'],
        '{{ARTIST_URL}}': ex['fuente_declaracion'],
        '{{ARTIST_NOTE}}': artist_works['nota_publicable'],
    }
    for token,value in mapping.items():
        assert token in page, f'Missing template placeholder: {token}'
        page = page.replace(token, html.escape(str(value), quote=True))
    assert '{{' not in page, 'Unresolved exhibition template placeholders'
    return page

def render_artwork_pages():
    """Render artwork records from the artist's portfolio, with no invented curatorial descriptions."""
    import re
    works = json.loads((ROOT / 'data/obras.json').read_text(encoding='utf-8'))
    assert len(works) == 11, 'Expected eleven authored artwork records'
    template = (ROOT / 'templates/obra.html').read_text(encoding='utf-8')
    assert len({w['slug'] for w in works}) == len(works), 'Duplicate artwork slug'
    output = {}
    for i, work in enumerate(works):
        slug = work['slug']
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug), f'Unsafe artwork slug: {slug}'
        assert work['titulo'] and work['tecnica'] and work['dimensiones'] and work['anio']
        assert re.fullmatch(r'[\w-]+\.(?:webp|jpg|jpeg|png)',work['archivo']), 'Unsafe image filename'
        image_path = ROOT / 'assets' / 'obras' / work['archivo']
        assert image_path.is_file(), f'Missing original preview: {image_path}'
        previous = works[i-1]
        following = works[(i+1)%len(works)]
        details = f"{work['tecnica']}, {work['dimensiones']}"
        schema = {
            '@context': 'https://schema.org', '@type': 'VisualArtwork',
            'name': work['titulo'],
            'creator': {'@type':'Person', 'name':'Nohemi Palencia Cisneros'},
            'dateCreated': str(work['anio']),
            'artMedium': work['tecnica'],
            'size': work['dimensiones'],
            'image': f"../../assets/obras/{work['archivo']}",
            'copyrightHolder': {'@type':'Person','name':'Nohemi Palencia Cisneros'},
        }
        replacements = {
            '{{TITLE}}': work['titulo'],
            '{{DESCRIPTION}}': f"{work['titulo']}, obra de Nohemi Palencia Cisneros ({work['anio']}). {details}.",
            '{{YEAR}}': str(work['anio']),
            '{{INDEX}}': f'{i+1:02d}',
            '{{TOTAL}}': str(len(works)),
            '{{IMAGE_URL}}': f"../../assets/obras/{work['archivo']}",
            '{{IMAGE_ALT}}': f"{work['titulo']}, obra de Nohemi Palencia Cisneros",
            '{{MEDIUM}}': work['tecnica'],
            '{{DIMENSIONS}}': work['dimensiones'],
            '{{PREVIOUS_SLUG}}': previous['slug'],
            '{{PREVIOUS_TITLE}}': previous['titulo'],
            '{{NEXT_SLUG}}': following['slug'],
            '{{NEXT_TITLE}}': following['titulo'],
            '{{SCHEMA_JSON}}': json.dumps(schema, ensure_ascii=False, separators=(',',':')).replace('<','\\u003c'),
        }
        rendered = template
        for token,value in replacements.items():
            assert token in rendered, f'Missing artwork template placeholder: {token}'
            rendered = rendered.replace(token, value if token == '{{SCHEMA_JSON}}' else html.escape(value,quote=True))
        assert '{{' not in rendered, f'Unresolved placeholders in {slug}'
        output[ROOT / 'obras' / slug / 'index.html'] = rendered + '\n'
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true',help='Fail when generated index.html is stale')
    args=parser.parse_args()
    expected_pages = {
        ROOT/'index.html': render()+'\n',
        ROOT/'exposiciones/rostros-oniricos/index.html': render_exhibition()+'\n',
    }
    expected_pages.update(render_artwork_pages())
    if args.check:
        for output,expected in expected_pages.items():
            assert output.exists() and output.read_text(encoding='utf-8')==expected, f'{output} is out of sync. Run python3 scripts/build.py'
        print('Generated HTML pages are up to date')
    else:
        for output,expected in expected_pages.items():
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(expected, encoding='utf-8')
            print(f'Built {output}')
