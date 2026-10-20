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
    def test_script_exists(self):
        self.assertTrue((ROOT/'assets/main.js').exists())
    def test_structured_data(self):
        s=re.search(r'<script type="application/ld\+json">(.*?)</script>',self.html,re.S)
        self.assertTrue(s)
        data=json.loads(s.group(1));self.assertEqual(data['name'],'Nohemi Palencia Cisneros')

if __name__=='__main__':unittest.main()
