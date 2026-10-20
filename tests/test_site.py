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
    def test_gallery_all_eleven_unique(self):
        self.assertEqual(len(self.data),11)
        self.assertEqual(len(self.parser.art),11)
        self.assertEqual(len({w['slug'] for w in self.data}),11)
    def test_works_have_metadata(self):
        for work in self.data:
            for f in ('slug','titulo','anio','tecnica','dimensiones','pagina_pdf','archivo'):self.assertTrue(work.get(f))
            self.assertIn(work['titulo'],self.html)
            self.assertTrue((ROOT/'assets/obras'/work['archivo']).stat().st_size>1000)
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
        self.assertNotIn('nohemipalencia',self.html.lower().replace('nohemi palencia',''))
    def test_no_pending_placeholders(self):
        self.assertNotIn('{{',self.html);self.assertNotIn('POR CONFIRMAR',self.html)
    def test_decorative_controls_are_not_mistaken_for_navigation(self):
        self.assertNotIn('class="marquee-bar"', self.html)
        self.assertNotIn('class="hero-index"', self.html)
        self.assertNotIn('class="timeline-icon"', self.html)
    def test_curatorial_sections_are_distinct_and_grounded(self):
        self.assertIn('id="exhibitions-heading"', self.html)
        self.assertIn('id="background-heading"', self.html)
        self.assertIn('id="exposicion"', self.html)
        self.assertIn('Proyecto Artístico Fusión', self.html)
        self.assertIn('Escuela de Artes Plásticas Arturo Michelena', self.html)
        self.assertIn('Gregorio Adán Palencia Castellanos', self.html)
        self.assertNotIn('Las Condes', self.html)
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
        self.assertEqual(self.html.count('class="artwork-detail-link"'),11)
        self.assertEqual(len({w['slug'] for w in self.data}),11)
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
            self.assertIn(f'href="../{slugs[(i-1)%len(slugs)]}/"',page)
            self.assertIn(f'href="../{slugs[(i+1)%len(slugs)]}/"',page)
            for relative in (f'../../assets/obras/{work["archivo"]}','../../assets/styles.css','../../assets/img/favicon.svg'):
                self.assertTrue((path.parent/relative).resolve().is_file(),relative)

    def test_script_exists(self):
        self.assertTrue((ROOT/'assets/main.js').exists())
    def test_structured_data(self):
        s=re.search(r'<script type="application/ld\+json">(.*?)</script>',self.html,re.S)
        self.assertTrue(s)
        data=json.loads(s.group(1));self.assertEqual(data['name'],'Nohemi Palencia Cisneros')

if __name__=='__main__':unittest.main()
