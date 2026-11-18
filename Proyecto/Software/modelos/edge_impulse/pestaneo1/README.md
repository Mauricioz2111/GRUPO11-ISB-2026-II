# Deployment WebAssembly (int8) - pestaneo1 vs reposo

- Modelo: EOG_RAW_1DCONV (antes Impulse #1), WebAssembly, Quantized (int8), build v1 de Edge Impulse (proyecto Señales_biomedicas_EOG_GRUPO11).
- ZIP descargado: `wasm-v1-impulse1-int8.zip` (nombre original de descarga: `señales_biomedicas_eog_grupo11-wasm-v1-impulse-#1.zip`).
- Contenido ya descomprimido en `node/` (para Node.js) y `browser/`. Para volver a descomprimir: `unzip wasm-v1-impulse1-int8.zip` (o `python3 -m zipfile -e wasm-v1-impulse1-int8.zip .`).

## Repetir la prueba local (Node v22.23.4)
```
cd Proyecto/Software/modelos/edge_impulse/pestaneo1/node
node run-impulse.js "<2000 valores de eog_a1 separados por comas>"
```
Los 2000 valores salen de la columna `eog_a1` de un CSV de `../../../datos_edge_impulse/` (sin la cabecera). Resultados de la prueba hecha: `Proyecto/Software/resultados/prueba_local_wasm_pestaneo1.txt`.

## Advertencia
La prueba usó dos CSV de Testing y dos de Training; no es una validación independiente ni demuestra que el modelo generalice a otros usuarios (un solo registro, 5 eventos, clipping).
