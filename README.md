# Nohemi Palencia Cisneros — portafolio artístico

Sitio estático en español de la artista **Nohemi Palencia Cisneros**, basado en el portafolio proporcionado por ella: **«Rostros Oníricos: Cartografía de lo invisible»** (15 páginas; obras y trayectoria). Diseñado primero para usuarios móviles que acceden desde el código QR de una exposición.

## Estado

- **Boceto funcional**, sin dominio definitivo ni publicación en GitHub Pages.
- **11 obras** con título, técnica, medidas y año; todas las fichas se basan en el PDF facilitado por la artista (páginas 3–13).
- **Fotografías provisionales** extraídas del mismo PDF; reemplazables por las fotografías originales en alta resolución que proporcionará la artista. Son vistas previas, **no recursos finales**.
- Biografía, declaración artística y trayectoria documentadas por el PDF (páginas 2 y 14). La muestra de Las Condes se agregará cuando estén confirmados oficialmente su nombre, lugar y fechas.
- Instagram oficial indicado en el PDF: **[@nohe.palencia](https://www.instagram.com/nohe.palencia/)**. La disponibilidad del perfil no se ha verificado directamente.

## Uso

Abrir `index.html` en un navegador. No requiere Node, dependencias, servidor ni despliegue para funcionar.

Para servirlo localmente (opcional):

```bash
python3 -m http.server 8080
```

## Mantener las obras y sustituir fotografías

1. **Datos canónicos:** editar `data/obras.json` (sin copiar/duplicar títulos a mano en `index.html`). `pagina_pdf` registra la página de origen del PDF. La grafía de los títulos se conserva de la ficha técnica del portafolio, con capitalización y tildes normalizadas cuando corresponde. Confirmar con la artista cualquier corrección de nombres.
2. **Imágenes:** guardar nuevas fotografías optimizadas (idealmente WebP, ancho suficiente para móviles y pantallas grandes) en `assets/obras/`, y cambiar `archivo` en `data/obras.json` por el nuevo nombre. No modificar la ruta fija de portada `assets/obras/el-aroma-a-canelo-preview.jpg` sin actualizarla también en `templates/index.html`. Para la foto de la artista, cambiar `assets/img/nohemi-galeria-preview.jpg` y la ruta de `templates/index.html` si corresponde.
3. Regenerar el HTML estático: `python3 scripts/build.py`.
4. Ejecutar verificaciones: `python3 scripts/build.py --check && python3 -m unittest discover -s tests -v`.
5. Revisar todas las obras a tamaño completo y en móvil; verificar títulos, perfiles y autorización antes del lanzamiento.

> Recomendación: mantener los nombres de archivo del portafolio en el JSON, optimizar imágenes finales y no incluir el PDF original de 29 MB en producción.

## Estructura

```text
index.html                   HTML final generado, listo para GitHub Pages
assets/styles.css            Diseño editorial, responsive
assets/main.js               Visor accesible de obras; enlaces funcionan sin JS
assets/obras/*-preview.*      Fotografías TEMPORALES del PDF
assets/img/*                 Fotografía de la artista y favicon
data/obras.json             Inventario canónico de once obras
 templates/index.html        Plantilla del sitio
 scripts/build.py            Generador estático con Python estándar
 tests/test_site.py          Pruebas de integridad y enlaces
 .github/workflows/verify.yml  CI de verificación
```

## Subir a GitHub

En un equipo con Git y GitHub CLI (`gh`) autenticado como `cortega26`, ejecutar desde la carpeta del proyecto:

```bash
bash scripts/publicar-github.sh
```

El script verifica el sitio, crea el repositorio **público** `cortega26/nohemi-palencia` si no existe o envía su contenido a `main`. No activa GitHub Pages.

## Publicación y QR

El despliegue previsto es **GitHub Pages** con una carpeta raíz, sin pipeline de compilación en el servidor. Se puede probar inicialmente en `https://cortega26.github.io/nohemi-palencia/` *si se crea el repositorio y se activa GitHub Pages*. Esta dirección es **una ruta propuesta, no confirmada ni publicada**.

Elegir dominio antes de imprimir un QR permanente. Si se necesita imprimir antes, usar primero una URL estable propia o un redireccionador administrado por el responsable del sitio para evitar QR obsoletos.

Pendientes para publicar: URL canónica, meta `og:image` absoluta, favicon/imagen social finales, verificación de contacto y fechas de la exposición de Las Condes.

## Derechos

**© Nohemi Palencia Cisneros. Todos los derechos reservados sobre las obras, fotografías y contenido artístico.** La autorización a preparar y publicar este portafolio no constituye licencia libre ni autorización de reutilización por terceros.
