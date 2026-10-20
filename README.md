# Nohemi Palencia Cisneros — portafolio artístico

Sitio estático en español de la artista **Nohemi Palencia Cisneros**, basado en el portafolio proporcionado por ella: **«Rostros Oníricos: Cartografía de lo invisible»** (15 páginas; obras y trayectoria). Diseñado primero para usuarios móviles que acceden desde el código QR de una exposición.

## Estado

- **Versión publicada:** https://tooltician.com/nohemi-palencia/ (sitio público verificado el 20-10-2026). El mecanismo de sincronización de ese sitio externo con GitHub no está documentado aquí; un merge en `main` no demuestra por sí solo que el dominio público se haya actualizado.
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

La versión visible actualmente está en **https://tooltician.com/nohemi-palencia/**. Este repositorio también puede alojarse en GitHub Pages, pero no se presume que el despliegue externo sea automático. Verificarlo en vivo después de cada publicación.

Elegir dominio antes de imprimir un QR permanente. Si se necesita imprimir antes, usar primero una URL estable propia o un redireccionador administrado por el responsable del sitio para evitar QR obsoletos.

Pendientes antes del lanzamiento definitivo con dominio de la artista: URL canónica, meta `og:image` absoluta, imagen social final, verificación de contacto, fotos de alta resolución y fechas de la exposición de Las Condes.

### Refinamiento editorial — primera iteración (20-10-2026)

- Se eliminaron ornamentos redundantes (franja de palabras, círculos decorativos, indicadores de sección no funcionales y flechas que aparentaban enlaces).
- Se simplificaron las superficies alrededor de las pinturas y se ajustaron la composición de galería y el contraste de la tipografía secundaria.
- Se corrigieron las zonas táctiles de la navegación móvil y la adaptación del título de contacto a pantallas estrechas.
- No se modificaron las once obras, su autoría ni sus fichas técnicas.
- El proceso de despliegue en Tooltician debe comprobarse por separado de la integración del código.

## Derechos

**© Nohemi Palencia Cisneros. Todos los derechos reservados sobre las obras, fotografías y contenido artístico.** La autorización a preparar y publicar este portafolio no constituye licencia libre ni autorización de reutilización por terceros.

### Iteración editorial 2 — trayectoria y contenido curatorial (2026-10-20)

- Se reemplazaron eslóganes genéricos por una presentación de la serie y del lenguaje plástico extraída/parafraseada del portafolio entregado por la artista (página 2).
- La trayectoria se organizó en **Exposiciones seleccionadas** y **Reconocimientos y formación**. No se afirma exhaustividad; los hitos provienen de la página 14 del mismo PDF.
- Se mantuvo la cita original de Nohemi, las once obras, sus fichas y las imágenes provisionales sin alteración.
- La exposición de Las Condes queda pendiente de documentación y las fotografías en alta resolución pendientes de entrega.
- Para confirmar publicación en tooltician.com no basta con el merge en GitHub; verificar manualmente en ese host después de desplegar.

### Registro expositivo documentado — iteración 3 (20-10-2026)

- Fuente institucional: [CCLR: «Exposición Rostros Oníricos»](https://comunidadcreativalosrios.cultura.gob.cl/events/exposicion-rostros-oniricos-nohemi-palencia/), con **fecha anunciada de presentación 3/9/2026** y **Galería Urbana Santo Tomás, Valdivia**. Fecha de cierre no acreditada.
- [CCLR: declaración de Nohemi](https://comunidadcreativalosrios.cultura.gob.cl/catalogo/nohemi-palencia-cisneros/) documenta su descripción de dibujo, pintura y figura femenina.
- El subtítulo **«Cartografía de lo invisible»** procede del portafolio de la artista, no de la ficha del evento de CCLR.
- `data/exposiciones.json` centraliza la exposición verificada y conserva nulos explícitos: no asigna ninguna de las once obras a la muestra hasta recibir confirmación.
- `scripts/build.py` compila la ficha expositiva y su registro en la cronología desde la misma fuente de datos; no duplicar el registro manualmente.
- Se incorporaron dos pruebas de regresión sobre procedencia, fecha, sede y ausencia de atribuciones no confirmadas.
- Pendientes de Nohemi: piezas efectivamente expuestas, fecha de cierre (si quiere publicarla), crédito/fotos oficiales y nombre preferido para exposiciones futuras.

### Página permanente de «Rostros Oníricos» — iteración 3

- Ruta prevista: `/nohemi-palencia/exposiciones/rostros-oniricos/`, enlazada desde el módulo expositivo y la cronología.
- La página se genera junto con la portada mediante `scripts/build.py`, a partir de `data/exposiciones.json` y `templates/exposicion-rostros-oniricos.html`.
- La agenda de [Comunidad Creativa de Los Ríos](https://comunidadcreativalosrios.cultura.gob.cl/events/exposicion-rostros-oniricos-nohemi-palencia/) confirma la **fecha anunciada de presentación (3/9/2026)** y la **Galería Urbana Santo Tomás, Valdivia**. No confirma una fecha de cierre.
- La [presentación pública de la artista](https://comunidadcreativalosrios.cultura.gob.cl/catalogo/nohemi-palencia-cisneros/) documenta su trabajo con figura femenina, geometría y naturaleza.
- El subtítulo procede del portafolio entregado por Nohemi. No se asignan obras individuales a la exposición sin validación documental.
- La galería con once obras se mantiene separada, y los archivos originales de mayor resolución siguen pendientes.
- El despliegue en Tooltician debe verificarse para confirmar que también publica el subdirectorio nuevo.

### Fichas individuales de obra — iteración 4

- Se crean once rutas permanentes relativas `obras/<slug>/`, por ejemplo `obras/guardiana/`, con `VisualArtwork` en JSON-LD, título, año, técnica, medidas y fotografía de referencia.
- Todas las páginas se generan desde `data/obras.json` por `scripts/build.py`. No existe copia manual de metadatos que pueda desincronizarse.
- La galería conserva su visor y añade enlaces explícitos a las fichas. Cada ficha enlaza a la obra anterior, la siguiente y a la galería.
- Los datos provienen del portafolio de la artista; fotografías extraídas del PDF siguen siendo **provisionales**. No se inventan interpretaciones de obras, estatus comercial, procedencia de colecciones ni pertenencia a una exposición.
- Se mantiene la URL de ruta para futuros QR, pero **no imprimir QR definitivos** antes de elegir un dominio estable que controle la artista.
- Integridad: `python3 scripts/build.py --check` y `python3 -m unittest discover -s tests -v`. El generador verifica y produce portada, exposición y once fichas.
