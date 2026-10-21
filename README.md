# Nohemi Palencia Cisneros — portafolio artístico

Sitio estático en español de la artista **Nohemi Palencia Cisneros**, basado en el portafolio proporcionado por ella: **«Rostros Oníricos: Cartografía de lo invisible»** (15 páginas; obras y trayectoria). Diseñado primero para usuarios móviles que acceden desde el código QR de una exposición.

## Estado

- **Versión publicada:** https://tooltician.com/nohemi-palencia/ (sitio público verificado el 20-10-2026). El mecanismo de sincronización de ese sitio externo con GitHub no está documentado aquí; un merge en `main` no demuestra por sí solo que el dominio público se haya actualizado.
- **11 obras** con título, técnica, medidas y año; todas las fichas se basan en el PDF facilitado por la artista (páginas 3–13).
- **Fotografías:** 12 reproducciones originales autorizadas y una reproducción provisional de El aroma a canelo, pendiente de fotografía HD confirmada.
- Biografía y trayectoria documentadas; CA660 noviembre 2026 incluye cuatro obras identificadas y enlazadas desde el catálogo.
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
data/obras.json             Inventario canónico vigente de trece obras
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

Pendientes antes del lanzamiento definitivo: adquirir dominio, configurar URL canónica y HTTPS, validar contacto, fotografía HD final de El aroma a canelo y metadatos técnicos todavía contradictorios.

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

### Confirmaciones directas de Nohemi — 20-10-2026

Se recibió una respuesta de la artista, conservada de forma estructurada en `data/confirmaciones-artista.json`:

- Nombre artístico: **Nohemi Palencia Cisneros**, **sin tilde**. Nacionalidad indicada por la artista: **venezolana**, residente en Valdivia, Chile. Estos valores ya coincidían con la identidad pública empleada por la web.
- **Rostros Oníricos en Santo Tomás:** la exposición incluyó **algunas** obras del portafolio entregado y **otras obras de distintas etapas y técnicas**. No hay aún identificaciones individuales; `obras_exhibidas_confirmadas` sigue vacío, intencionalmente.
- La artista escribió una fecha de cierre imposible («31 de septiembre») y después indicó que la corregía, sin que en la captura se vea una fecha válida. No publicar ninguna fecha de término hasta obtenerla.
- **Próxima exposición en Las Condes:** informó montaje el **28 de octubre de 2026 a las 12:00**, inauguración el **6 de noviembre a las 18:00**, encuentro con artistas el **14 de noviembre a las 12:00** y desmontaje el **27 de noviembre**. La presentación facilitada posteriormente identifica **CA660, Rosario Norte 660, Las Condes**; el título definitivo de la edición y las obras participantes aún no se han confirmado. La portada publica una mención cautelosa de la participación, no un catálogo comercial.
- Las fotografías originales de alta resolución permanecen pendientes; no aplicar upscaling a la copia del PDF.

**Fuentes y prioridad:** información primaria expresada por la artista en comunicación directa, aportada por el responsable del sitio; para el título y la fecha de presentación de la muestra Santo Tomás, también se mantiene la referencia institucional de CCLR. No confundir material del portafolio con catálogo completo de una exposición.

### Participación anunciada en CA660 — 20-10-2026

- **Fuente primaria:** presentación de «La Escena de Arte» facilitada por Nohemi. Identifica **CA660, Rosario Norte 660, Las Condes**, y explica el sistema de atriles y tarjetas de artista.
- **Nombre no resuelto:** la portada de esa presentación dice «La Escena de Arte», mientras una tarjeta de ejemplo dice «La Escena del Arte»; este último nombre también aparece en el catálogo de AMF Gallery para su edición **septiembre–octubre**, que **no** verifica la denominación de noviembre. Ambos quedan documentados en `data/confirmaciones-artista.json`; la portada evita declarar uno como título oficial.
- **Calendario comunicado por la artista:** montaje 28-10 12:00; inauguración 06-11 18:00; encuentro con artistas 14-11 12:00; desmontaje 27-11 (sin hora).
- **Documentación del recinto:** CA660 es un espacio cultural de Fundación CorpArtes, en la dirección indicada. No se afirma que Fundación CorpArtes sea organizadora de la exposición.
- **Referencia de galería:** [AMF Gallery Chile](https://www.instagram.com/amfchile/) y [sitio AMF](https://www.amfchile.com/). El vínculo con el evento se apoya en material promocional compartido, no en un contrato de representación.
- **Sistema de tarjetas:** 15 × 30 cm, incluye nombre, redes/sitio, biografía, presentación y un QR que lleva al **catálogo del organizador**. Ese catálogo anuncia fichas y precios con contacto WhatsApp **centralizado del organizador**. El sitio propio de Nohemi permanece separado: no debe redirigir ni apropiarse de precios, catálogo ni QR ajenos.
- **Pendientes:** nombre final, lista de pinturas participantes, fotografías definitivas y si la galería acepta mostrar en la tarjeta la URL de Nohemi. Las fotos de ejemplo del dossier no pertenecen a Nohemi y no se han añadido a la página.

### Confirmación de edición noviembre y corrección visual — 20-10-2026

- La artista confirmó expresamente que la edición de noviembre utiliza **el mismo nombre que la exposición de septiembre–octubre: «La Escena del Arte»**, identificándola como «Edición Noviembre». Fuente: captura de sus respuestas por WhatsApp compartida el 20-10-2026. Esta confirmación prevalece sobre la grafía «La Escena de Arte» que aparece en la portada del material de referencia, que se conserva en los datos con su procedencia.
- El bloque «Nohemi en CA660» muestra ahora el nombre confirmado sin mezclar las piezas de la edición anterior ni inventar participantes.
- Se agregó padding horizontal responsive (20–48 px) con `box-sizing: border-box` en la sección `.upcoming`, preservando el ancho de la `.shell` y evitando textos pegados al borde.
- El catálogo del organizador conserva su QR y WhatsApp comercial; el portafolio de Nohemi es independiente.

### Metadatos sociales y URLs canónicas — iteración SEO (20-10-2026)

- `data/site.json` centraliza `public_base_url` — **actualmente temporal: https://tooltician.com/nohemi-palencia/** — y la imagen social general. Al escoger dominio definitivo, actualizar este archivo y regenerar HTML + sitemap mediante `python3 scripts/build.py`.
- El generador aplica `rel="canonical"`, `og:url`, `og:image`, `og:image:alt` y un `twitter:card` moderado en **portada, exposición documentada y once fichas de obra**. Las fichas enlazan a su propia imagen y a su URL individual; el campo `VisualArtwork.image` ahora es absoluto.
- `sitemap.xml` registra las trece páginas públicas desde la misma fuente de datos. Como el proyecto vive en un **subdirectorio de Tooltician**, no se publica un `robots.txt` en esa carpeta: no sustituiría al del dominio raíz.
- Las imágenes sociales son **provisionales** y necesitan fotografías originales autorizadas y posiblemente una portada social curada para mejorar la calidad visual de las tarjetas.
- **No imprimir QR definitivos** antes de determinar y configurar el dominio estable de Nohemi. Al migrar, considerar redirecciones 301 desde las rutas antiguas y verificar metadatos/cachés en aplicaciones sociales; no asumir que cambiar el JSON actualiza por sí mismo el dominio ni los enlaces impresos.
- Las pruebas verifican URL canónica única, `og:url`, existencia de imagen social y coherencia de las trece URLs del sitemap.

Esta fase cubre la **infraestructura técnica** del issue #11; permanece abierta hasta decidir el dominio y reemplazar las imágenes sociales provisionales.

### Ajuste de lectura de galería — iteración siguiente

- El diseño conserva el número de columnas, el aspecto de las reproducciones, las once obras y la jerarquía general. No agranda indiscriminadamente imágenes provisionales.
- Metadatos de obra y años más legibles (`13px` y `12px`), numeración con mejor contraste y enlaces a fichas individuales con área mínima de `44px`.
- Ritmo vertical aumentado a `76px` en escritorio, `62px` en tableta y `52px` en móvil para separar las obras sin introducir ornamentos.
- Se agregó prueba de regresión de CSS y se mantiene la verificación del generador en CI.
- **Pendiente:** inspección visual final y ajuste de la disposición según las fotografías originales de Nohemi; no afirmar que los previews sean ya reproducciones museográficas.

### Huella automática de CSS (evitar estilos obsoletos en caché)

Se detectó en producción que el archivo `assets/styles.css` sin parámetros podía devolver la versión anterior incluso después de un despliegue aprobado de GitHub Pages, mientras la solicitud con una query nueva devolvía el CSS actualizado.

`scripts/build.py` calcula una huella de contenido a partir de `assets/styles.css` y añade `?v=<huella>` al enlace de estilos de portada, exposición y las once fichas de obra. La misma huella cambia automáticamente en cada modificación de CSS; no se introduce una nueva dependencia de JavaScript ni se modifica la URL canónica de ninguna página. La prueba de integridad verifica las trece páginas y la sincronización con el generador.

### Retrato de la artista — ampliación 2× no generativa (20-10-2026)

- Fuente realmente disponible: `assets/img/nohemi-galeria-preview.jpg`, extraída del portafolio facilitado por Nohemi (936 × 716 px). El PDF contiene la misma resolución, **no** un original de cámara de mayor tamaño.
- Nuevo recurso: `assets/img/nohemi-galeria-mejorada-2x.webp`, 1784 × 1352 px, creado con un recorte de la banda documental, ajustes mínimos de color y contraste, interpolación Lanczos 2× y enfoque moderado. Sin composición generativa, reconstrucción facial ni detalles de obras inventados.
- Para reproducirlo: instalar `Pillow==12.3.0` y ejecutar `python scripts/enhance_artist_photo.py` desde el repositorio. El script comprueba el SHA-256 exacto de la fuente y la resolución de salida.
- La sección «La artista» utiliza ahora WebP; el JPEG fuente permanece disponible y el `og:image` social de la portada y del archivo expositivo apunta a la mejora.
- Esta operación **no** reemplaza el objetivo pendiente de obtener fotografías originales autorizadas de las obras y de la artista. No confundir el aumento de píxeles con recuperación fiel de detalle que no existe en la fuente.

### La foto de la artista: corrección del encuadre visual (posterior al 2×)

- Diagnóstico en `main@9d48e68`: el archivo mejorado ya estaba publicado, pero la sección `about` usaba un marco **vertical** (`aspect-ratio:.78`) para una fotografía horizontal (1784 × 1352 px). `object-fit:cover` descartaba una parte importante de los cuadros y `filter:saturate(.75)` restaba color. Al tamaño mostrado, el upscale 2× no era apreciable.
- Solución: mostrar la fotografía **completa y sin desaturación**, con proporción nativa, `object-fit:contain`, mayor proporción de columna visual y presentación horizontal también en móvil. No introducir filtros de estilo ni recreaciones de pinturas o rostro.
- Se conserva el original y su mejora 2×, pero no se afirma que esta operación recupere nuevos detalles: corrige principalmente **composición y fidelidad visual**.
- La huella del CSS está actualizada en las 13 páginas. Prueba de regresión añadida contra recortes y filtros desaturadores.

### Superresolución neuronal real — retrato de Nohemi

- La fotografía original del portafolio (936 × 716 px) fue procesada mediante el modelo abierto **RealESRGAN_x2plus**, con pesos externos verificados por SHA-256 (`49fafd45f8fd7aa8d31ab2a22d14d91b536c34494a5cfe31eb5d89c2fa266abb`). No es la interpolación Lanczos de la versión anterior.
- **Salida:** `assets/img/nohemi-galeria-neural-2x.webp`, 1784 × 1352 px, tras el mismo recorte documental utilizado anteriormente. El resultado combina 84% de reconstrucción neuronal y 16% de interpolación documental para reducir alucinaciones. Ajustes posteriores suaves: contraste, color, enfoque.
- Código reproducible en `scripts/neural_upscale_artist.py`; la inferencia se ejecutó en una rama aislada mediante un workflow temporal, retirado después. El modelo preentrenado está disponible en [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN).
- El archivo fuente y la versión convencional anterior **siguen intactos**. La portada, sección «La artista» y vista previa social de la exposición utilizan la nueva versión.
- **Limitación fundamental:** el modelo estima microdetalles sin información física verificable. Esta fotografía es válida como retrato ambiental/editorial, **no** como reproducción fidedigna ampliada de cada pintura ni como documento de referencia de su técnica. Para las fichas de obra, conservar las reproducciones originales autorizadas.

### Tres nuevas obras y archivos originales — 20-10-2026

**Inventario público:** se amplía de once a catorce obras con tres fichas permanentes nuevas. La procedencia es el correo de la artista y las fechas confirmadas:

| Título | Año | Técnica | Medidas | Fotografía original |
|---|---|---|---|---|
| Aura cósmica II | 2026 (confirmación del usuario a partir de Nohemi) | Mixta sobre MDF | 81,5 × 64 cm | `17634.jpg` |
| Huelliches II | 2026 (confirmación del usuario a partir de Nohemi) | Mixta sobre MDF vitrificado | 81,5 × 64 cm | `17661.jpg` |
| Plumaje azul | 2026 (rectificación editorial posterior; correo original indicaba 2017) | Mixta sobre MDF vitrificado | 81,5 × 64 cm | `17651.jpg` |

Las fotos originales tienen 4000 × 3000 px en el archivo JPEG y orientación EXIF vertical (3000 × 4000 px). Se generaron fielmente versiones WebP de 1800 × 2400 px, sin reconstrucción por IA ni recorte de obras; estas viven en `assets/obras/*-original-web.webp`. El original íntegro permanece en los correos de Nohemi, en vez de duplicar archivos de cámara pesados en el sitio estático.

La portada ya no muestra una advertencia global sobre fotografías provisionales. Las 12 obras con originales recibidos presentan su reproducción optimizada; queda pendiente la imagen HD de **El aroma a canelo**. La correspondencia con la exposición histórica de Valdivia sigue sin inferirse.

El generador, enlaces de navegación circular, numeración, sitemap, metadatos Open Graph y pruebas de integridad se actualizaron para catorce obras y dieciséis rutas públicas.

### Reproducciones originales de nueve obras — 20-10-2026

- Las fotografías de cámara facilitadas por Nohemi se identifican por los archivos 17677, 17679, 17678, 17673, 17663, 17662, 17659, 17653 y 17652 (JPEG).
- `scripts/import_nine_artist_originals.py` valida SHA-256, corrige EXIF, recorta únicamente el entorno fotografiado de cada pintura (pared, marco y paspartú) y genera WebP con un máximo de 2400 px en el lado mayor. No hay generación ni reconstitución de detalles.
- Las reproducciones se registran con procedencia; Aura cósmica II fue consolidada posteriormente con su imagen HD confirmada y El aroma a canelo conserva provisionalmente una imagen de catálogo.
- `data/obras.json` conserva la procedencia de cada fotografía y el generador propaga la URL de cada imagen a las páginas y metadatos.
- La galería y las fichas reducen márgenes, fondos y sombras artificiales para dar prioridad a la pintura.

### Galería responsiva y reproducciones fieles — 20-10-2026

- `scripts/generate_gallery_variants.py` genera, desde las **12 fotografías originales ya autorizadas**, WebP de **480 y 960 píxeles de ancho**, conservando las proporciones, sin IA generativa, reencuadres nuevos ni cambios de color.
- En la portada, cada tarjeta original utiliza `srcset` y `sizes` para adaptar la transferencia al dispositivo. El enlace accesible de la tarjeta, el visor ampliado, las fichas de obra, Schema.org y Open Graph mantienen las reproducciones en alta resolución existentes.
- La única imagen provisional pendiente es **El aroma a canelo**. Aura cósmica II utiliza la fotografía original HD confirmada.
- GitHub Actions verifica que las 24 miniaturas comprometidas coincidan byte por byte con el generador determinista (`Pillow==12.3.0`), además de las pruebas y la sincronización del HTML.
- Regeneración reproducible: `python3 scripts/generate_gallery_variants.py && python3 scripts/build.py`; comprobación: `python3 scripts/generate_gallery_variants.py --check && python3 scripts/build.py --check && python3 -m unittest discover -s tests -v`.

### Reencuadre pictórico de tres pinturas — 20-10-2026

- Solicitud editorial: Aura cósmica II, Huelliches II y Plumaje azul deben mostrar **solo la pintura** como protagonista, sin pared, marco de madera ni paspartú negro.
- Nuevas reproducciones en `assets/obras/`, sin marcos ni paspartús; los antiguos archivos erróneamente nombrados fueron retirados.
- Archivos fuente autorizados: `17634.jpg`, `17661.jpg`, `17651.jpg`; originales JPEG 4000×3000 píxeles con orientación EXIF=6, verificados por SHA-256 dentro de `scripts/reframe_three_artist_originals.py`.
- Rectángulos de superficie pintada, inspeccionados en fotografía original orientada (left, top, right, bottom; tamaño base 3000×4000): Aura cósmica II (637,1060,2386,3532), Huelliches II (709,711,2411,3265), Plumaje azul (553,749,2350,3040). Incluyen margen de seguridad para evitar cortar firmas o pinceladas de borde. Sin reconstrucción, relleno generativo, corrección engañosa de color ni transformación de perspectiva.
- Las miniaturas responsivas 480/960 se regeneran desde las nuevas reproducciones; fichas, visor, `og:image` y Schema.org apuntan a la versión fiel reencuadrada. La información técnica no se modifica.
- **Operación reproducible:** `python3 scripts/reframe_three_artist_originals.py --source-dir /ruta/a/jpg-originales && python3 scripts/generate_gallery_variants.py && python3 scripts/build.py`; validación usual del CI en GitHub.


### Portafolio adicional de 16 páginas — recibido el 20/10/2026

Fuente: `Presentación Portafolio Creativo Moderno Corporativo Gris y Crema (1).pdf`, material recibido directamente de Nohemi Palencia. Revisadas especialmente las **páginas 2 (biografía) y 3 (currículum)**; no sustituye automáticamente los documentos previos.

Aporta participaciones históricas menos representadas: segunda Muestra de Artes en homenaje al profesor Luis Díaz (2001, Universidad de Carabobo), Muestra de Artes Visuales del Estado Carabobo (2002, Museo de la Cultura de Valencia), Gran Salón de Pintura por aniversario de la Cámara de Comercio (2004, Estado Carabobo). La portada integra una selección breve sin reproducir todo el currículo.

**Discrepancias reservadas:** (1) la nueva página 11 indica 2026 para **Plumaje azul** y el correo individual de Nohemi del 20-10-2026 indicaba 2017; el responsable del sitio rectificó posteriormente el año a **2026**. Se conserva la discrepancia histórica, pero el catálogo vigente refleja 2026; (2) el currículum de la nueva página 3 denomina «exposición individual» a una presentación de 2026 en Galería Urbana, mientras la fuente institucional se refiere a «Rostros Oníricos»: no modificar modalidad hasta verificación; (3) la duplicación fue aclarada por Nohemi: hay una única obra catalogada como Aura cósmica II; (4) el PDF presenta «Huelliche II», mientras el registro y correo anterior usan «Huelliches II»: conservar forma previamente verificada hasta aclaración.

No publicar el teléfono personal repetido en el diseño de Canva sin necesidad editorial y aprobación explícita. No usar como URL literal el texto `www.Nohemi Palencia Cisneros. cl`: no es un dominio válido. El PDF incluye además diapositivas en blanco y una ficha de obra titulada «Fotografía de producto», que no se interpretará como título artístico oficial.

### Rectificación de años de las 14 obras — octubre de 2026

El responsable del sitio confirmó expresamente que **las 14 obras representadas son de 2026** y pidió sustituir los dos registros que todavía indicaban 2017. El catálogo canónico en `data/obras.json` se corrigió para **Hindú celular** y **Plumaje azul**; todas las demás obras ya tenían 2026. Se actualizan portada, fichas individuales, textos sociales y `dateCreated` de Schema.org mediante el generador estático, con una prueba de regresión explícita. Fotografías, color, encuadre, medidas, títulos y soportes permanecen inalterados.

**Proveniencia y salvedad:** el PDF histórico consignaba 2017 en una ficha de `Hindú celular`; el correo del 20-10-2026 indicaba 2017 para `Plumaje azul`. El nuevo portafolio recibido también consignaba 2026 para Plumaje azul. La corrección de ambas fichas se basa en la **indicación expresa del responsable de la web**, no se debe reescribir el contenido de esos correos ni atribuirle a Nohemi una confirmación posterior que no consta. Cada registro corregido conserva `fuente_anio` y este historial explica por qué la información pública actual es 2026.

### Edición fotográfica localizada — octubre de 2026

- Obras 1/14 **Guardiana** y 3/14 **Visión frontal / Sueño con el Iznik**: corrección moderada de reflejos del barniz mediante máscaras elípticas de atenuación local. No hay retoques generativos, inpainting, ni generación de pinceladas o texturas.
- El script reproducible `scripts/retouch_artworks.py` conserva intactas las imágenes `*-original-web.webp` y genera nuevas versiones `*-retouched-original-web.webp`. En ellas se aplica únicamente una reducción moderada del velo neutro de luz; validación de magnitud por píxel en el propio script.
- Las miniaturas 480/960 se regeneraron a partir de las dos correcciones fotográficas; los otros cuadros permanecen sin retoques de reflejos.
- CI: `python3 scripts/retouch_artworks.py --check` (reproducibilidad exacta) + `python3 scripts/generate_gallery_variants.py --check` + `python3 scripts/build.py --check` + tests. Dependencias fijadas Pillow 12.3.0 y NumPy 2.2.6.
- Limitación documental: la luz especular intensa puede ocultar textura original que **no puede recuperarse de la fotografía**. Para una reproducción museográfica se recomienda volver a fotografiar con iluminación difusa/polarización; el retoque no sustituye nuevas tomas.

### Confirmaciones del 21-10-2026: duplicado pictórico y selección CA660

**Fuente editorial primaria:** información del responsable del sitio tras consultar a Nohemi y captura de cuatro pinturas para CA660 (2×2). Se identificaron contra originales ya publicados, no por reconocimiento automático.

- Las dos fichas antiguas representaban la misma pintura. La autora confirmó el título **«Aura cósmica II»**; se consolidó un registro HD y el catálogo quedó con **13 obras**.
- La única URL de la obra es `/obras/aura-cosmica-ii/`; se retiraron los archivos, rutas y código de compatibilidad de la identificación descartada.
- Se rectifica también `scripts/reframe_three_artist_originals.py` para que al reproducir el import desde la fotografía auténtica `17634.jpg` genere directamente el nombre correcto `aura-cosmica-ii-reframed-original-web.webp`.
- La autora confirmó el título exacto de la obra 11 original: **«El aroma a canelo»**. El soporte (MDF o lienzo barnizado) no fue aclarado; **no** se inventa una rectificación del soporte ni una nueva fotografía.
- **CA660 «La Escena del Arte», noviembre 2026:** cuatro obras mostradas en la cuadrícula aportada por el responsable del sitio: arriba izquierda **Princesa onírica**, arriba derecha **Shitikari**, abajo izquierda **Hindú celular**, abajo derecha **Visión frontal / Sueño con el Iznik**. Quedan registradas en `data/confirmaciones-artista.json` y enlazadas a sus cuatro fichas desde el módulo de CA660. No confundirlas con el inventario (aún no especificado) de la exposición histórica de Rostros Oníricos en Valdivia.
- Todos los cambios son reproducibles desde `data/obras.json` más `data/confirmaciones-artista.json`, scripts existentes y las reproducciones originales; no se fabricaron pinturas nuevas.

## Cierre editorial P0 21-10-2026
El aroma a canelo: **MDF**, confirmado por el responsable. La reproducción fotográfica actual se reencuadra desde el archivo suministrado por la artista, sin aumento artificial de píxeles; no se recibió fotografía HD de cámara. Guardiana, Visión frontal / Sueño con el Iznik, Hilos del subconciente y Atómica II tienen corrección localizada, no generativa, de la luz reflejada, y se conservan intactas sus fuentes.
