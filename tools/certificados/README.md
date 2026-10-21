# Certificados de autenticidad

El generador imprime **modelos sin emitir** para las cuatro pinturas de CA660, usando la ficha canónica de cada obra y su fotografía publicada. Nunca asigna identificadores ni firma certificados.

## Regenerar

- Revisar primero la obra física y su ficha.
- Validación sin dependencias: python tools/certificados/generar.py --check
- Instalar dependencias locales: python -m pip install reportlab Pillow
- Generar solo en una ruta privada: python tools/certificados/generar.py --out /tmp/nohemi-certificados
- Selección individual: python tools/certificados/generar.py --slug princesa-onirica --out /tmp/nohemi-certificados

## Emisión y privacidad

1. No asignar números al crear borradores. Cada certificado firmado deberá recibir un ID irrepetible del registro privado, por ejemplo NPC-2026-0001. No usar posiciones de galería.
2. Registrar fecha, obra, código, firma, comprobante y comprador en un inventario privado fuera de GitHub.
3. Completar lugar/fecha y firmar de puño y letra de Nohemi. Entregar en A4 con papel opalina mate de 180 g/m², previa prueba de impresora.
4. Conservar copia privada; el documento no reemplaza boleta/factura, pericia ni registro estatal.
5. No agregar QR hasta que la URL definitiva opere mediante HTTPS. Nunca exponer datos del comprador en verificaciones públicas.

## Fundamento

Chile: Ley 17.336, artículo 37, distingue la adquisición del soporte material de los derechos de reproducción con fines de lucro.
Fuente: https://www.bcn.cl/leychile/navegar?idNorma=28933
El DDI confirma que inscribir una obra no es requisito para que quede protegida por derecho de autor.
Fuente: https://www.propiedadintelectual.gob.cl/node/551
