# Nohemi Palencia Cisneros — portafolio artístico

Sitio estático en español de la artista **Nohemi Palencia Cisneros**, basado en el portafolio proporcionado por ella: **«Rostros Oníricos: Cartografía de lo invisible»** (15 páginas; obras y trayectoria). Diseñado primero para usuarios móviles que acceden desde el código QR de una exposición.

## Estado

- **Versión publicada:** https://tooltician.com/nohemi-palencia/ (sitio público verificado el 20-10-2026). El mecanismo de sincronización de ese sitio externo con GitHub no está documentado aquí; un merge en `main` no demuestra por sí solo que el dominio público se haya actualizado.
- **11 obras** con título, técnica, medidas y año; todas las fichas se basan en el PDF facilitado por la artista (páginas 3–13).
- **Fotografías provisionales** extraídas del mismo PDF; reemplazables por las fotografías originales en alta resolución que proporcionará la artista. Son vistas previas, **no recursos finales**.
- Biografía, declaración artística y trayectoria documentadas por el PDF (páginas 2 y 14). La participación de noviembre de 2026 en CA660 (Las Condes) tiene sede y calendario comunicados por la artista; el título definitivo de la edición y las obras participantes siguen pendientes.
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

Pendientes antes del lanzamiento definitivo con dominio de la artista: URL canónica, meta `og:image` absoluta, imagen social final, verificación de contacto, fotos de alta resolución, título definitivo de la edición de Las Condes y obras participantes.

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
