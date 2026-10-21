import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class Collector(HTMLParser):
    def __init__(self):
        super().__init__(); self.images=[];self.links=[];self.sections=[];self.art=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag=='img': self.images.append(d)
        if tag=='a' and 'href' in d:self.links.append(d['href'])
        if d.get('id'):self.sections.append(d['id'])
        if tag=='a' and 'data-artwork' in d:self.art.append(d)

class PortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=(ROOT/'index.html').read_text('utf-8'); cls.data=json.loads((ROOT/'data/obras.json').read_text('utf-8'))
        cls.parser=Collector();cls.parser.feed(cls.html)
    def test_owner_corrected_all_current_work_years_to_2026(self):
        # Direct correction from website owner supersedes the 2017 catalog entries;
        # documentation of the historical discrepancy must remain available.
        self.assertEqual(len(self.data),13)
        self.assertTrue(all(w['anio']==2026 for w in self.data))
        for slug in ('hindu-celular','plumaje-azul'):
            work=next(w for w in self.data if w['slug']==slug)
            self.assertIn('responsable del sitio',work['fuente_anio'])
            self.assertIn('2017',work['fuente_anio'])
            page=(ROOT/'obras'/slug/'index.html').read_text('utf-8')
            self.assertIn('dateCreated":"2026"',page)
            self.assertIn('<time datetime="2026">2026</time>',page)
            self.assertNotIn('(2017)',page)
            self.assertNotIn('dateCreated":"2017"',page)
            item=self.html.split('id="obra-'+slug+'"',1)[1].split('</article>',1)[0]
            self.assertIn('class="artwork-year">2026',item)
            self.assertNotIn('2017',item)

    def test_gallery_all_thirteen_unique(self):
        self.assertEqual(len(self.data),13)
        self.assertEqual(len(self.parser.art),13)
        self.assertEqual(len({w['slug'] for w in self.data}),13)
    def test_works_have_metadata(self):
        for work in self.data:
            for f in ('slug','titulo','anio','tecnica','dimensiones','archivo'):self.assertTrue(work.get(f))
            self.assertIn(work['titulo'],self.html)
            self.assertTrue((ROOT/'assets/obras'/work['archivo']).stat().st_size>1000)
    def test_three_reframed_paintings_are_responsive_and_keep_full_file(self):
        for slug in ('aura-cosmica-ii','huelliches-ii','plumaje-azul'):
            work=next(w for w in self.data if w['slug']==slug)
            full='assets/obras/'+work['archivo']
            gallery='assets/obras/gallery/'+slug+'-480.webp'
            retina='assets/obras/gallery/'+slug+'-960.webp'
            self.assertIn(f'href="{full}" data-artwork',self.html)
            self.assertIn(f'src="{gallery}"',self.html)
            self.assertIn(f'{retina} 960w',self.html)
            self.assertGreater((ROOT/full).stat().st_size,500_000)
            self.assertLess((ROOT/gallery).stat().st_size,(ROOT/full).stat().st_size)
            self.assertIn(f'../../{full}',(ROOT/'obras'/slug/'index.html').read_text('utf-8'))

    def test_three_new_artworks_are_artist_sourced(self):
        expected={
            'aura-cosmica-ii': ('Aura cósmica II',2026,'aura-cosmica-ii-reframed-original-web.webp'),
            'huelliches-ii': ('Huelliches II',2026,'huelliches-ii-reframed-original-web.webp'),
            'plumaje-azul': ('Plumaje azul',2026,'plumaje-azul-reframed-original-web.webp'),
        }
        indexed={w['slug']:w for w in self.data}
        for slug,(title,year,image) in expected.items():
            work=indexed[slug]
            self.assertEqual(work['titulo'],title)
            self.assertEqual(work['anio'],year)
            self.assertEqual(work['archivo'],image)
            if slug=='aura-cosmica-ii':
                self.assertNotIn('archivo_original_sin_recorte',work)
                self.assertIn('17634.jpg',work['nota_recorte'])
            else:
                self.assertEqual(work['archivo_original_sin_recorte'],slug+'-original-web.webp')
                self.assertTrue((ROOT/'assets/obras'/work['archivo_original_sin_recorte']).is_file())
            self.assertIn('superficie pictórica',work['nota_recorte'])
            self.assertNotIn('pagina_pdf',work)
            self.assertIn('Correo de Nohemi',work['fuente_fotografia'])
            path=ROOT/'assets/obras'/image
            self.assertTrue(path.is_file(),image)
            self.assertGreater(path.stat().st_size,500_000,image)
            header=path.read_bytes()[:12]
            self.assertEqual(header[:4],b'RIFF')
            self.assertEqual(header[8:12],b'WEBP')
        self.assertNotIn('Las fotografías originales se incorporarán posteriormente',self.html)
        self.assertNotIn('class="asset-note"',self.html)

    def test_referenced_images_exist(self):
        for image in self.parser.images:
            if image.get('id')=='lightbox-img':
                continue  # populated dynamically when the dialog opens
            self.assertTrue(image.get('alt'),image)
            self.assertTrue((ROOT/image['src']).exists(),image['src'])
    def test_internal_links_resolve(self):
        ids=set(self.parser.sections)
        for url in self.parser.links:
            if url.startswith('#'):self.assertIn(url[1:],ids)
    def test_instagram_is_artist_source(self):
        self.assertIn('https://www.instagram.com/nohe.palencia/',self.html)
        self.assertNotIn('instagram.com/nohemipalencia',self.html.lower())
    def test_no_pending_placeholders(self):
        self.assertNotIn('{{',self.html);self.assertNotIn('POR CONFIRMAR',self.html)
    def test_decorative_controls_are_not_mistaken_for_navigation(self):
        self.assertNotIn('class="marquee-bar"', self.html)
        self.assertNotIn('class="hero-index"', self.html)
        self.assertNotIn('class="timeline-icon"', self.html)
    def test_2026_portfolio_additions_are_artist_sourced_and_selective(self):
        # The artist's 16-page PDF, page 3, lists these earlier career events.
        self.assertIn('En su trayectoria venezolana participó en muestras y salones',self.html)
        for title in (
            'Gran Salón de Pintura · Aniversario de la Cámara de Comercio',
            'Muestra de Artes Visuales del Estado Carabobo',
            '2.ª Muestra de Artes en homenaje al profesor Luis Díaz',
        ):
            self.assertIn(title,self.html)
        # Contradictions must not be silently rewritten from a later catalog.
        records={w['slug']:w for w in self.data}
        self.assertEqual(records['plumaje-azul']['anio'],2026)
        self.assertEqual(records['aura-cosmica-ii']['archivo'],'aura-cosmica-ii-reframed-original-web.webp')
        self.assertNotIn('Exposición individual «Galería Urbana»',self.html)

    def test_curatorial_sections_are_distinct_and_grounded(self):
        self.assertIn('id="exhibitions-heading"', self.html)
        self.assertIn('id="background-heading"', self.html)
        self.assertIn('id="exposicion"', self.html)
        self.assertIn('Proyecto Artístico Fusión', self.html)
        self.assertIn('Escuela de Artes Plásticas Arturo Michelena', self.html)
        self.assertIn('Gregorio Adán Palencia Castellanos', self.html)
        history_fragment=self.html.split('<section class="history"',1)[1].split('</section>',1)[0]
        self.assertNotIn('Las Condes', history_fragment)
        self.assertNotIn('Una trayectoria<br>', self.html)

    def test_verified_exhibition_provenance_and_no_assumed_works(self):
        exhibitions=json.loads((ROOT/'data/exposiciones.json').read_text('utf-8'))
        self.assertEqual(len(exhibitions),1)
        ex=exhibitions[0]
        self.assertEqual(ex['titulo_evento'],'Rostros Oníricos')
        self.assertEqual(ex['fecha_evento'],'2026-09-03')
        self.assertEqual(ex['espacio'],'Galería Urbana Santo Tomás')
        self.assertIsNone(ex['fecha_cierre'])
        self.assertEqual(ex['obras_exhibidas_confirmadas'], [])
        self.assertIn(ex['fuente_institucional'],self.html)
        self.assertIn(ex['fuente_declaracion'],self.html)
        self.assertIn('href="exposiciones/rostros-oniricos/"',self.html)
        self.assertNotIn('Exposición individual «Galería Urbana»',self.html)
        self.assertNotIn('Todas las obras fueron exhibidas',self.html)
    def test_single_source_exhibition_timeline(self):
        self.assertIn('<time datetime="2026-09-03">',self.html)
        self.assertEqual(self.html.count('Galería Urbana Santo Tomás'),3)

    def test_permanent_exhibition_page(self):
        ex=json.loads((ROOT/'data/exposiciones.json').read_text('utf-8'))[0]
        exhibit_path=ROOT/ex['ruta_permanente']/'index.html'
        self.assertTrue(exhibit_path.is_file())
        rendered=exhibit_path.read_text('utf-8')
        self.assertIn('href="exposiciones/rostros-oniricos/"',self.html)
        self.assertIn('Rostros Oníricos: Cartografía de lo invisible',rendered)
        self.assertIn('datetime="2026-09-03"',rendered)
        self.assertIn(ex['fuente_institucional'],rendered)
        self.assertIn(ex['fuente_declaracion'],rendered)
        self.assertIn('La obra de la artista puede explorarse por separado',rendered)
        self.assertNotIn('{{',rendered)
        self.assertEqual(ex['obras_exhibidas_confirmadas'],[])
        self.assertTrue((exhibit_path.parent/'../../assets/styles.css').resolve().is_file())

    def test_all_artworks_have_linked_permanent_records(self):
        self.assertEqual(self.html.count('class="artwork-detail-link"'),13)
        self.assertEqual(len({w['slug'] for w in self.data}),13)
        for work in self.data:
            url=f"obras/{work['slug']}/"
            self.assertIn(f'href="{url}"',self.html)
            target=ROOT/url/'index.html'
            self.assertTrue(target.is_file(),url)
            page=target.read_text('utf-8')
            self.assertIn(f'<h1>{work["titulo"]}</h1>',page)
            self.assertIn(work['tecnica'],page)
            self.assertIn(work['dimensiones'],page)
            self.assertIn(str(work['anio']),page)
            self.assertIn(f'../../assets/obras/{work["archivo"]}',page)
            self.assertIn('href="../../#obra"',page)
            self.assertIn('nohemi',page.lower())
            self.assertNotIn('{{',page)
            self.assertNotIn('Precio de venta',page)
            self.assertNotIn('Obra exhibida en',page)

    def test_artwork_schema_and_navigation(self):
        slugs=[w['slug'] for w in self.data]
        for i,work in enumerate(self.data):
            path=ROOT/'obras'/work['slug']/'index.html'
            page=path.read_text('utf-8')
            m=re.search(r'<script type="application/ld\+json">(.*?)</script>',page,re.S)
            self.assertIsNotNone(m,work['slug'])
            schema=json.loads(m.group(1))
            self.assertEqual(schema['@type'],'VisualArtwork')
            self.assertEqual(schema['name'],work['titulo'])
            self.assertEqual(schema['dateCreated'],str(work['anio']))
            self.assertEqual(schema['size'],work['dimensiones'])
            self.assertEqual(schema['artMedium'],work['tecnica'])
            self.assertEqual(schema['creator']['name'],'Nohemi Palencia Cisneros')
            self.assertEqual(schema['image'],'https://nohemipalencia.com/assets/obras/'+work['archivo'])
            self.assertIn(f'href="../{slugs[(i-1)%len(slugs)]}/"',page)
            self.assertIn(f'href="../{slugs[(i+1)%len(slugs)]}/"',page)
            for relative in (f'../../assets/obras/{work["archivo"]}','../../assets/styles.css','../../assets/img/favicon.svg'):
                self.assertTrue((path.parent/relative).resolve().is_file(),relative)

    def test_artist_confirmations_preserve_uncertainty(self):
        confirmed=json.loads((ROOT/'data/confirmaciones-artista.json').read_text('utf-8'))
        self.assertEqual(confirmed['identidad']['nombre_artistico'], 'Nohemi Palencia Cisneros')
        self.assertTrue(confirmed['identidad']['sin_tilde'])
        self.assertEqual(confirmed['identidad']['nacionalidad'], 'venezolana')
        ex=confirmed['rostros_oniricos']
        self.assertTrue(ex['incluyo_otras_obras'])
        self.assertTrue(ex['otras_etapas_y_tecnicas'])
        self.assertEqual(ex['obra_especifica_confirmada'], [])
        self.assertIsNone(ex['fecha_fin_confirmada'])
        page=(ROOT/'exposiciones/rostros-oniricos/index.html').read_text('utf-8')
        self.assertIn(ex['nota_publicable'],page)
        self.assertNotIn('31 de septiembre',page)
        next_ex=confirmed['proxima_exposicion']
        self.assertEqual(next_ex['nombre_oficial'],'La Escena del Arte')
        self.assertEqual(next_ex['sede'],'CA660 · Centro Cultural de Fundación CorpArtes')
        self.assertEqual(next_ex['direccion'],'Rosario Norte 660, Las Condes, Santiago, Chile')
        self.assertEqual(next_ex['nombre_oficial'],'La Escena del Arte')
        self.assertEqual(next_ex['obras_confirmadas'],[
            'princesa-onirica','shitikari','hindu-celular','vision-frontal-sueno-con-el-iznik'
        ])
        for slug in next_ex['obras_confirmadas']:
            work=next(w for w in self.data if w['slug']==slug)
            self.assertIn(f'href="obras/{slug}/"',self.html)
            self.assertIn(f'assets/obras/gallery/{slug}-480.webp',self.html)
            self.assertIn(work['titulo'],self.html)
        self.assertEqual(next_ex['titulo_promocional_presentacion'],'La Escena de Arte')
        self.assertEqual(next_ex['titulo_ejemplo_tarjeta'],'La Escena del Arte')
        self.assertFalse(next_ex['organizador_formal_confirmado'])
        self.assertEqual(next_ex['tarjeta_artista_formato_cm'],'15 × 30')
        self.assertIn('QR al catálogo digital del organizador',next_ex['tarjeta_artista_contenido'])
        self.assertIn('id="proxima-exposicion"',self.html)
        self.assertIn('datetime="2026-11-06T18:00"',self.html)
        self.assertIn('datetime="2026-11-14T12:00"',self.html)
        self.assertIn('CA660 · Rosario Norte 660, Las Condes',self.html)
        self.assertIn(next_ex['referencia_galeria_url'],self.html)
        self.assertNotIn('La Escena de Arte',self.html)
        self.assertIn('La Escena del Arte',self.html)
        self.assertIn('edición Noviembre 2026',self.html)
        self.assertEqual(next_ex['edicion_confirmada'],'Noviembre 2026')

        expected=[
            ('montaje','2026-10-28','12:00'),
            ('inauguracion','2026-11-06','18:00'),
            ('encuentro con artistas','2026-11-14','12:00'),
            ('desmontaje','2026-11-27',None),
        ]
        self.assertEqual([(a['tipo'],a['fecha'],a['hora_local']) for a in next_ex['actividades']],expected)

    def test_upcoming_horizontal_padding(self):
        css=(ROOT/'assets/styles.css').read_text('utf-8')
        self.assertIn('.upcoming{box-sizing:border-box',css)
        self.assertIn('padding-inline:clamp(20px,3.4vw,48px)',css)


    def test_final_domain_cname_and_canonical_agree(self):
        site=json.loads((ROOT/'data/site.json').read_text('utf-8'))
        self.assertEqual(site['final_domain'],'nohemipalencia.com')
        self.assertEqual((ROOT/'CNAME').read_text('utf-8').strip(),site['final_domain'])
        self.assertEqual(site['public_base_url'],'https://nohemipalencia.com/')
        self.assertNotIn('tooltician.com/nohemi-palencia',self.html)
        for page in [ROOT/'index.html',ROOT/'exposiciones/rostros-oniricos/index.html']:
            self.assertIn('https://nohemipalencia.com/',page.read_text('utf-8'))

    def test_canonical_and_social_metadata_for_all_pages(self):
        from xml.etree import ElementTree
        site=json.loads((ROOT/'data/site.json').read_text('utf-8'))
        base=site['public_base_url']
        self.assertEqual(base,'https://nohemipalencia.com/')
        works=self.data
        pages=[('', ROOT/'index.html'), ('exposiciones/rostros-oniricos/', ROOT/'exposiciones/rostros-oniricos/index.html')]
        pages += [(f"obras/{w['slug']}/", ROOT/'obras'/w['slug']/'index.html') for w in works]
        self.assertEqual(len(pages),15)
        for route,filename in pages:
            html=filename.read_text('utf-8')
            canonical=re.search(r'<link rel="canonical" href="([^"]+)"',html)
            ogurl=re.search(r'<meta property="og:url" content="([^"]+)"',html)
            image=re.search(r'<meta property="og:image" content="([^"]+)"',html)
            self.assertIsNotNone(canonical,route)
            self.assertIsNotNone(ogurl,route)
            self.assertIsNotNone(image,route)
            self.assertEqual(canonical.group(1),base+route)
            self.assertEqual(ogurl.group(1),base+route)
            self.assertTrue(image.group(1).startswith(base+'assets/'),route)
            self.assertTrue((ROOT/image.group(1)[len(base):]).is_file(),route)
            self.assertIn('<meta name="twitter:card" content="summary">',html)
            self.assertIn('property="og:image:alt"',html)
        sitemap=(ROOT/'sitemap.xml').read_text('utf-8')
        doc=ElementTree.fromstring(sitemap)
        urls=[e.text for e in doc.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        self.assertEqual(len(urls),15)
        self.assertEqual(set(urls),{base+route for route,_ in pages})

    def test_upcoming_facts_readability(self):
        css=(ROOT/'assets/styles.css').read_text('utf-8')
        self.assertIn('.upcoming-details dd{font:500 16px/1.55 var(--sans)',css)
        self.assertIn('.upcoming-details dl div{grid-template-columns:minmax(0,1fr);gap:6px}',css)
        self.assertIn('18:00&nbsp;h',self.html)
        self.assertIn('12:00&nbsp;h',self.html)
        self.assertNotIn('18:00 h</time>',self.html)
        self.assertNotIn('12:00 h</time>',self.html)

    def test_small_functional_text_is_not_set_in_display_typeface(self):
        css=(ROOT/'assets/styles.css').read_text('utf-8')
        for selector in (
            '.hero-art-label strong', '.collection-subtitle', '.about-copy .about-lead',
            '.timeline-item h3', '.timeline-item h4',
            '.exhibition-facts dd', '.archive-date time', '.archive-record dd',
            '.artwork-details-list dd'
        ):
            match=re.search(re.escape(selector)+r'\{([^}]*)\}',css)
            self.assertIsNotNone(match,selector)
            declaration=match.group(1)
            self.assertIn('var(--sans)',declaration,selector)
            self.assertNotIn('var(--serif)',declaration,selector)

    def test_upcoming_year_is_not_repeated_in_reading_copy(self):
        upcoming=self.html.split('<section class="upcoming shell"',1)[1].split('</section>',1)[0]
        self.assertNotIn('<span>NOVIEMBRE 2026</span>',upcoming)
        self.assertEqual(upcoming.count('edición Noviembre 2026'),1)
        self.assertIn('datetime="2026-11-06T18:00"',upcoming)
        self.assertIn('datetime="2026-11-14T12:00"',upcoming)

    def test_gallery_caption_legibility_and_touch_targets(self):
        css=(ROOT/'assets/styles.css').read_text('utf-8')
        self.assertIn('.artwork-number{display:block;margin-bottom:9px;color:#4b594f;font-size:11px',css)
        self.assertIn('.artwork-info p{font-size:13px;line-height:1.7;color:#46564a}',css)
        self.assertIn('.artwork-year{font-size:12px;color:#48594e}',css)
        self.assertIn('.artwork-detail-link{display:inline-flex;align-items:center;min-height:44px',css)
        self.assertIn('font-size:13px;font-weight:700',css)
        self.assertIn('.gallery-grid{column-gap:36px;row-gap:76px}',css)
        self.assertIn('.gallery-grid{column-gap:24px;row-gap:62px}',css)
        self.assertIn('.gallery-grid{row-gap:52px}',css)
        self.assertEqual(self.html.count('class="artwork-detail-link"'),len(self.data))

    def test_artwork_creation_year_appears_once_in_visible_record(self):
        template=(ROOT/'templates/obra.html').read_text('utf-8')
        self.assertNotIn('class="artwork-detail-year"',template)
        self.assertIn('<dt>Año</dt><dd><time datetime="{{YEAR}}">{{YEAR}}</time></dd>',template)
        for work in self.data:
            page=(ROOT/'obras'/work['slug']/'index.html').read_text('utf-8')
            self.assertNotIn('class="artwork-detail-year"',page,work['slug'])
            self.assertEqual(page.count('<dt>Año</dt>'),1,work['slug'])
            self.assertIn(
                f'<dt>Año</dt><dd><time datetime="{work["anio"]}">{work["anio"]}</time></dd>',
                page,work['slug']
            )

    def test_css_fingerprint_consistent_across_generated_pages(self):
        import hashlib
        css=(ROOT/'assets/styles.css').read_bytes()
        version=hashlib.sha1(f'blob {len(css)}'.encode('ascii')+bytes([0])+css).hexdigest()[:12]
        expected=[
            (ROOT/'index.html','assets/styles.css'),
            (ROOT/'exposiciones/rostros-oniricos/index.html','../../assets/styles.css'),
        ]
        expected.extend((ROOT/'obras'/w['slug']/'index.html','../../assets/styles.css') for w in self.data)
        self.assertEqual(len(expected),15)
        for page,relative in expected:
            html=page.read_text('utf-8')
            self.assertIn(f'href="{relative}?v={version}"',html,str(page))
            self.assertNotIn(f'href="{relative}"',html,str(page))
            self.assertEqual(html.count('styles.css?v='),1,str(page))

    def test_artist_portrait_is_enhanced_and_preserves_attribution(self):
        photo=ROOT/'assets/img/nohemi-galeria-neural-2x.webp'
        original=ROOT/'assets/img/nohemi-galeria-preview.jpg'
        self.assertTrue(original.exists())
        self.assertTrue((ROOT/'assets/img/nohemi-galeria-mejorada-2x.webp').exists())
        self.assertTrue((ROOT/'scripts/neural_upscale_artist.py').exists())
        self.assertTrue(photo.is_file())
        self.assertGreater(photo.stat().st_size,100_000)
        data=photo.read_bytes()
        self.assertEqual(data[:4],b'RIFF')
        self.assertEqual(data[8:12],b'WEBP')
        self.assertIn('src="assets/img/nohemi-galeria-neural-2x.webp"',self.html)
        self.assertIn('width="1784" height="1352"',self.html)
        self.assertIn('alt="Nohemi Palencia en una sala rodeada de sus pinturas"',self.html)
        self.assertIn('nohemi-galeria-neural-2x.webp',json.loads(
            (ROOT/'data/site.json').read_text('utf-8'))['social_image_default'])

    def test_artist_gallery_photo_is_shown_in_full_color_without_crop(self):
        css=(ROOT/'assets/styles.css').read_text('utf-8')
        self.assertIn('.about-image-wrap{aspect-ratio:1784 / 1352;',css)
        self.assertIn('.about-image-wrap img{display:block;width:100%;height:100%;object-fit:contain;object-position:center;filter:none}',css)
        self.assertNotIn('filter:saturate(.75)',css)
        self.assertNotIn('.about-image-wrap{aspect-ratio:1.02}',css)
        self.assertIn('src="assets/img/nohemi-galeria-neural-2x.webp"',self.html)
        self.assertIn('grid-template-columns:minmax(0,1.25fr) minmax(0,1fr)',css)


    def test_nine_artist_originals_are_source_traced_without_faux_frames(self):
        expected={'guardiana':'17677.jpg','hilos-del-subconciente':'17679.jpg',
            'guardiana-del-umbral':'17678.jpg','vision-frontal-sueno-con-el-iznik':'17673.jpg',
            'sacerdotiza-solar':'17663.jpg','princesa-onirica':'17662.jpg',
            'atomica-ii':'17659.jpg','hindu-celular':'17653.jpg','shitikari':'17652.jpg'}
        indexed={w['slug']:w for w in self.data}
        for slug,source in expected.items():
            work=indexed[slug]
            self.assertEqual(work['archivo'],slug+(
                '-studio-original-web.webp' if slug in ('guardiana','vision-frontal-sueno-con-el-iznik','hilos-del-subconciente','atomica-ii')
                else '-original-web.webp'))
            self.assertIn(source,work['fuente_fotografia'])
            path=ROOT/'assets/obras'/work['archivo']
            self.assertGreater(path.stat().st_size,300_000,slug)
            header=path.read_bytes()[:12]
            self.assertEqual((header[:4],header[8:12]),(b'RIFF',b'WEBP'),slug)
            self.assertIn('assets/obras/'+work['archivo'],self.html)
        styles=(ROOT/'assets/styles.css').read_text('utf-8')
        self.assertIn('.artwork-image,.artwork-feature .artwork-image{padding:0;background:transparent}',styles)
        self.assertIn('.artwork-detail-view{padding:0;background:transparent}',styles)


    def test_four_reversible_photo_corrections(self):
        treated=('guardiana','vision-frontal-sueno-con-el-iznik','hilos-del-subconciente','atomica-ii')
        self.assertEqual([w['slug'] for w in self.data if 'retoque_fotografico' in w],list(treated))
        for slug in treated:
            work=next(w for w in self.data if w['slug']==slug)
            self.assertEqual(work['archivo_original_sin_retoque'],slug+'-original-web.webp')
            self.assertIn('reversible',work['retoque_fotografico'])
            self.assertTrue((ROOT/'assets/obras'/work['archivo_original_sin_retoque']).exists())
            self.assertTrue((ROOT/'assets/obras'/work['archivo']).exists())
            page=(ROOT/'obras'/slug/'index.html').read_text('utf-8')
            self.assertIn('../../assets/obras/'+work['archivo'],page)
        self.assertEqual(self.html.count('-studio-original-web.webp'),4)

    def test_only_authorized_artwork_routes_exist(self):
        slugs=[w['slug'] for w in self.data]
        self.assertEqual(len(slugs),13)
        self.assertEqual(slugs.count('aura-cosmica-ii'),1)
        self.assertEqual(slugs.index('aura-cosmica-ii'),10)
        routes={p.name for p in (ROOT/'obras').iterdir() if p.is_dir()}
        self.assertEqual(routes,set(slugs))
        self.assertIn('aura-cosmica-ii-reframed-original-web.webp',self.html)
        self.assertNotIn('http-equiv="refresh"',self.html)
        canelo=next(w for w in self.data if w['slug']=='el-aroma-a-canelo')
        self.assertEqual(canelo['titulo'],'El aroma a canelo')
        self.assertIn('confirmado por Nohemi',canelo['fuente_titulo'])

    def test_ca660_has_exactly_four_distinct_linked_artworks(self):
        confirmed=json.loads((ROOT/'data/confirmaciones-artista.json').read_text('utf-8'))
        selected=confirmed['proxima_exposicion']['obras_confirmadas']
        self.assertEqual(selected,['princesa-onirica','shitikari','hindu-celular',
                                   'vision-frontal-sueno-con-el-iznik'])
        upcoming=self.html.split('<section class="upcoming shell"',1)[1].split('</section>',1)[0]
        self.assertEqual(upcoming.count('class="upcoming-work"'),4)
        for slug in selected:
            self.assertIn(f'href="obras/{slug}/"',upcoming)
            self.assertIn(f'assets/obras/gallery/{slug}-480.webp',upcoming)
        self.assertIn('Obras que participarán',upcoming)
        self.assertNotIn('obras participantes pendientes',upcoming)

    def test_ca660_artwork_labels_centered_under_each_painting(self):
        css=(ROOT/'assets/styles.css').read_text('utf-8')
        self.assertIn('.upcoming-work{display:flex;flex-direction:column;align-items:center;text-align:center;',css)
        self.assertIn('.upcoming-work span{display:block;max-width:min(100%,240px);',css)
        self.assertIn('text-wrap:balance}',css)
        self.assertIn('object-fit:contain;object-position:center;',css)
        self.assertIn('.upcoming-artworks{grid-template-columns:repeat(2,minmax(0,1fr));',css)
        self.assertEqual(self.html.count('class="upcoming-work"'),4)

    def test_responsive_gallery_only_for_confirmed_originals(self):
        expected_full = {w['slug']:w for w in self.data}
        self.assertEqual(len(self.parser.art),13)
        self.assertEqual(sum(bool(w.get('fuente_fotografia')) for w in self.data),12)
        for work in self.data:
            slug = work['slug']
            matching = [i for i in self.parser.images if i.get('alt') ==
                        f"{work['titulo']}, obra de Nohemi Palencia Cisneros"]
            self.assertEqual(len(matching),1,slug)
            image = matching[0]
            full = f"assets/obras/{work['archivo']}"
            full_link = [a for a in self.parser.art if a.get('href') == full]
            self.assertEqual(len(full_link),1,slug)
            detail = (ROOT/'obras'/slug/'index.html').read_text('utf-8')
            self.assertIn(f"../../{full}",detail)
            if work.get('fuente_fotografia'):
                small=f"assets/obras/gallery/{slug}-480.webp"
                big=f"assets/obras/gallery/{slug}-960.webp"
                self.assertEqual(image.get('src'),small,slug)
                self.assertEqual(image.get('srcset'),f"{small} 480w, {big} 960w",slug)
                self.assertTrue(image.get('sizes'),slug)
                for candidate in (small,big):
                    p=ROOT/candidate
                    self.assertTrue(p.is_file(),candidate)
                    self.assertGreater(p.stat().st_size,4000,candidate)
                    self.assertLess(p.stat().st_size,(ROOT/full).stat().st_size,candidate)
            else:
                self.assertEqual(image.get('src'),full,slug)
                self.assertNotIn('srcset',image,slug)
        self.assertNotIn('assets/obras/gallery/',json.dumps(self.data))

    def test_artwork_provenance_credit_matches_actual_image(self):
        self.assertEqual(sum(bool(w.get('fuente_fotografia')) for w in self.data),12)
        for work in self.data:
            page=(ROOT/'obras'/work['slug']/'index.html').read_text('utf-8')
            if work.get('fuente_fotografia'):
                self.assertIn('Fotografía original proporcionada por Nohemi Palencia.',page)
                self.assertNotIn('Imagen provisional del catálogo',page)
            else:
                self.assertIn('Imagen documental reencuadrada sin ampliación digital; fotografía original de cámara HD pendiente.',page)
                self.assertNotIn('Fotografía original proporcionada por Nohemi Palencia.',page)

    def test_tooltician_footer_credit_has_correct_utm_on_every_page(self):
        from html import unescape
        from urllib.parse import urlparse, parse_qs
        pages=[ROOT/'index.html',ROOT/'exposiciones/rostros-oniricos/index.html']
        pages.extend(ROOT/'obras'/w['slug']/'index.html' for w in self.data)
        self.assertEqual(len(pages),15)
        for page in pages:
            html=page.read_text('utf-8')
            footer=re.search(r'<footer class="site-footer">(.*?)</footer>',html,re.S)
            self.assertIsNotNone(footer,str(page))
            self.assertEqual(footer.group(1).count('Hecho por '),1,str(page))
            match=re.search(r'<a href="([^"]+)" target="_blank" rel="noopener noreferrer">Tooltician</a>',footer.group(1))
            self.assertIsNotNone(match,str(page))
            url=urlparse(unescape(match.group(1)))
            self.assertEqual((url.scheme,url.netloc,url.path),('https','tooltician.com','/'),str(page))
            self.assertEqual(parse_qs(url.query),{
                'utm_source':['nohemipalencia.com'],
                'utm_medium':['referral'],
                'utm_campaign':['portfolio_footer'],
            },str(page))
            self.assertIn('© 2026 Nohemi Palencia Cisneros',footer.group(1))

    def test_documented_canelo_photo_is_also_used_in_hero(self):
        source=(ROOT/'templates/index.html').read_text('utf-8')
        for page in (source,self.html):
            self.assertIn('src="assets/obras/el-aroma-a-canelo-reference-cropped.webp"',page)
            self.assertNotIn('src="assets/obras/el-aroma-a-canelo-preview.jpg"',page)
            self.assertIn('width="540" height="677"',page)
        canelo=next(x for x in self.data if x['slug']=='el-aroma-a-canelo')
        self.assertEqual(canelo['archivo'],'el-aroma-a-canelo-reference-cropped.webp')
        self.assertTrue((ROOT/'assets/obras'/canelo['archivo']).is_file())

    def test_secondary_editorial_links_have_mobile_touch_targets(self):
        css=(ROOT/'assets/styles.css').read_text('utf-8')
        self.assertIn('.upcoming-intro a,.exhibition-links a,.site-footer a{display:inline-flex;align-items:center;min-height:28px}',css)
        self.assertIn('Hecho por ',self.html)

    def test_script_exists(self):
        self.assertTrue((ROOT/'assets/main.js').exists())
    def test_structured_data(self):
        s=re.search(r'<script type="application/ld\+json">(.*?)</script>',self.html,re.S)
        self.assertTrue(s)
        data=json.loads(s.group(1));self.assertEqual(data['name'],'Nohemi Palencia Cisneros')

if __name__=='__main__':unittest.main()
