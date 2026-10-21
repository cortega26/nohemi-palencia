import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"tools/certificados/generar.py"
class CertificateTests(unittest.TestCase):
    def setUp(self):
        spec=importlib.util.spec_from_file_location("certgen",SCRIPT)
        self.mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
    def test_ca660_works_match_canonical_catalog(self):
        items=self.mod.catalog()
        self.assertEqual([x["slug"] for x,_ in items],[
            "princesa-onirica","shitikari","hindu-celular","vision-frontal-sueno-con-el-iznik"])
        self.assertTrue(all(x["anio"]==2026 and x["tecnica"]=="Técnica mixta sobre MDF" for x,_ in items))
    def test_bad_or_duplicate_slug_is_rejected(self):
        with self.assertRaises(ValueError):self.mod.catalog(("aura-cosmica-i",))
        with self.assertRaises(ValueError):self.mod.catalog(("princesa-onirica","princesa-onirica"))
    def test_no_private_buyer_data_or_automatic_sale_ids(self):
        text=SCRIPT.read_text(encoding="utf-8")
        self.assertIn("NPC-______________",text)
        self.assertIn("MODELO SIN EMITIR",text)
        self.assertNotIn("comprador_privado",text)
