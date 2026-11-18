# Edge Impulse — Movimiento 1: pestañeo (clase `pestaneo1`)

Proyecto Edge Impulse: **Señales_biomedicas_EOG_GRUPO11** (ID 1163950). Prueba preliminar binaria **pestaneo1 vs reposo**. Este documento solo registra lo que se completó realmente.

## 1. Objetivo
Probar de punta a punta el flujo (preparación de datos, carga, impulsos, entrenamiento, Model Testing, comparación y deployment) con la clase `pestaneo1` (un pestañeo) frente a `reposo`. Los resultados no validan un clasificador definitivo.

## 2. Función de los tres archivos originales (en `datos/pestaneo/`, no modificados)
- `pestaneo1.txt`: registro OpenSignals (BITalino) con la señal de EOG; es la fuente de la preparación.
- `pestaneo1eventos.txt`: tiempos de inicio y fin de cada evento (columnas MAC, CHANNEL, ID, START, END).
- `pestaneo1.h5`: copia del registro en H5. **No se procesó porque `h5py` no estaba disponible** (no se instaló). La preparación se hizo con el TXT de OpenSignals y el archivo de eventos. Verificar el H5 queda pendiente.

## 3. Frecuencia de muestreo
1000 Hz. Registro de 62.85 s (62 850 muestras).

## 4. Canal utilizado
A1 (columna 5), ADC de 10 bits (0–1023). Se exporta como `eog_a1`. A2 es casi constante y las entradas/salidas digitales son constantes.

## 5. Eventos
9 filas en el archivo de eventos, **5 eventos únicos** (inicios en 18.75, 34.2, 39.75, 50.1 y 60.3 s). Todos proceden de un solo registro.

## 6. Eliminación de duplicados
Las filas con el mismo START se contaron una sola vez (9 filas → 5 inicios únicos). No se eliminó ningún evento válido para mejorar resultados.

## 7. Segmentación
Ventanas de 2 s: 0.75 s antes y 1.25 s después del inicio del evento (pestañeo centrado). 2000 muestras por CSV.

## 8. Corrección de línea base
Se resta la mediana de los primeros 300 ms de cada ventana. En `pestaneo1_003` y `pestaneo1_005` esos 300 ms están saturados (línea base 1018), por lo que la corrección es poco confiable.

## 9. Extracción de reposo
Segmentos de 2 s centrados en los intervalos libres entre eventos, con 0.5 s de margen. Son datos reales del mismo registro, no inventados. Se obtuvieron 5 (inicios en 8.0, 25.73, 36.23, 44.17 y 54.45 s).

## 10. División entrenamiento / testing
Por evento completo (semilla 11), sin solape.
- Entrenamiento: 4 `pestaneo1` (001, 002, 003, 005) + 4 `reposo` (001–004).
- Testing: 1 `pestaneo1` (004) + 1 `reposo` (005).
Testing tiene **una muestra por clase**: cada una vale 50 %.

## 11. Formato CSV
`timestamp,eog_a1`; timestamp en ms (0–1999), valor con un decimal. Carpetas `datos_edge_impulse/{training|testing}/{pestaneo1|reposo}/`. Control de calidad en `resultados/pestaneo1_control_calidad.csv`; figuras `resultados/pestaneo1_senal_completa.png` y `resultados/pestaneo1_segmentos.png`.

## 12. Carga a Edge Impulse
Los 10 CSV se subieron manualmente (el navegador automatizado no puede elegir archivos). Al principio todas las muestras entraron como entrenamiento y con etiquetas `reposo_training`, `testing_reposo` y `testing_pestaneo1`; se corrigieron las etiquetas a `pestaneo1` / `reposo` y se movieron 2 muestras a Testing. Resultado: 8 muestras de entrenamiento y 2 de testing. No se subieron `pestaneo1.txt`, el archivo de eventos ni el H5.

## 13. Experimentos
Configuración común: ventana 2000 ms, incremento 2000 ms, 1000 Hz, eje `eog_a1`, zero-pad, 30 ciclos, LR 0.0005, red pequeña, sin bloques de Heart Rate, validación ≈ 20 %. Los impulsos se renombraron en Edge Impulse (sin cambiar configuración, datos ni resultados) tras confirmar sus bloques en la tabla Experiments. Antes se llamaban Impulse #1 a #4.

| Nombre anterior | Nombre actual en Studio | Bloque de procesamiento | Clasificador |
|---|---|---|---|
| Impulse #1 | EOG_RAW_1DCONV | Raw data | 1D Conv (Reshape + Conv1D 8 filtros k=3 + Flatten) |
| Impulse #2 | EOG_FLATTEN | Flatten (7 características) | Dense 20-10 |
| Impulse #3 | EOG_STFT | Spectrogram (65 columnas) | 1D Conv (8 y 16 filtros k=3, dropout 0.25) |
| Impulse #4 | EOG_SPECTRAL | Spectral features (13 características) | Dense 20-10 |

**Modelo desplegado: EOG_RAW_1DCONV (antes Impulse #1).**

## 14. Feature Explorer
En los impulsos 3 y 4 las muestras se ven separadas por clase en el explorador, pero con solo 8 muestras de entrenamiento esto no demuestra capacidad de generalización.

## 15. Entrenamiento
Validación 100 % en los cuatro (el conjunto de validación solo contiene muestras de `pestaneo1`; la fila de `reposo` está vacía, por lo que el dato no es informativo). Loss: 0.00 (#1), 0.00 (#2), 0.35 (#3), 0.00 (#4). La interfaz no mostró la accuracy de entrenamiento final; en el log del #4 aparece 0.33–0.50 con loss de entrenamiento 1.5–1.9 en las últimas épocas.

## 16. Matrices de confusión
Validación: 100 % `pestaneo1`; la fila de `reposo` aparece vacía porque la cantidad de muestras es extremadamente pequeña (8 de entrenamiento, y el 20 % de validación no incluyó ninguna de `reposo`). En el explorador de datos de #1, #3 y #4 hay muestras de `reposo` marcadas como incorrectas. Testing: ver sección 17.

## 17. Model Testing
| Impulso | Accuracy | Resultado |
|---|---|---|
| #1 Raw 1D Conv | 100 % | Ambas muestras correctas (2 muestras) |
| #2 Flatten | 50 % | `reposo_005` clasificada como `pestaneo1` |
| #3 Spectrogram | 50 % | `reposo_005` clasificada como `pestaneo1` |
| #4 Spectral Analysis | 50 % | `reposo_005` clasificada como `pestaneo1` |

Un 100 % con 2 muestras significa solo 2 aciertos de 2; no es una medida fiable.

## 18. Comparación (int8, EON, Cortex-M4F 80 MHz)
| Impulso | Latencia | RAM | Flash |
|---|---|---|---|
| #1 Raw 1D Conv | 38 ms | 27.6K | 57.6K |
| #2 Flatten | 9 ms | 7.9K | 14.4K |
| #3 Spectrogram | 148 ms | 52.4K | 32.7K |
| #4 Spectral | 62 ms | 8.5K | 14.6K |

(float32 de #1: 425 ms, 91.1K RAM, 97.5K flash.) Detalle en `resultados/comparacion_modelos_pestaneo1.csv`.

## 19. Modelo preliminar seleccionado
**EOG_RAW_1DCONV (Impulse #1)** como candidato preliminar, únicamente porque fue el único que acertó las dos muestras de Testing y su costo (38 ms, 27.6K RAM) es razonable. No se eligió por accuracy de entrenamiento. Es una elección débil: Testing tiene 2 muestras, hay clipping y los demás modelos también pueden estar aprendiendo saturación. Si se prioriza consumo, Flatten y Spectral son mucho más pequeños pero no discriminaron en Testing.

## 20. Deployment
- **Modelo desplegado:** EOG_RAW_1DCONV (antes Impulse #1: Raw data + 1D Conv). **Descargado como WebAssembly, Quantized (int8)**, motor EON; build `v1 (WebAssembly)` del 18-nov-2026 08:51. Estimación de Studio (MacBook Pro 16" 2020): latencia 1 ms, RAM 33.0K, flash 44.3K.
- **Archivos:** en `modelos/edge_impulse/pestaneo1/` (ver su `README.md`): el ZIP descargado (`wasm-v1-impulse1-int8.zip`, copiado desde Descargas con el nombre original `señales_biomedicas_eog_grupo11-wasm-v1-impulse-#1.zip` cambiado) y su contenido descomprimido (`node/` con `run-impulse.js`, y `browser/`).
- **Prueba local con Node v22.23.4** (npm 10.9.9; no se instaló nada), ejecutando `node run-impulse.js "<2000 valores>"` con cuatro de los CSV generados. Salida completa: `resultados/prueba_local_wasm_pestaneo1.txt`. Las cuatro pruebas fueron correctas, con confianza aproximada de 0.996:
  - `pestaneo1_004` (**Testing**) → pestaneo1.
  - `reposo_005` (**Testing**) → reposo.
  - `pestaneo1_001` (**Training**) → pestaneo1.
  - `reposo_001` (**Training**) → reposo.
- **Cómo interpretarlo:** solo una muestra de pestaneo1 y una de reposo pertenecían a Testing. Los otros dos CSV pertenecían a Training, es decir, el modelo ya los vio al entrenar. Esto **no es una validación independiente**: solo confirma que el paquete corre localmente y reproduce el resultado de Model Testing del modelo cuantizado. No se afirma que el modelo generalice a otros usuarios, sesiones o registros.
- No se tocó la interfaz principal ni `control_parpadeos.py`.
- Incidente: la primera vez que se intentó, el navegador mostró la vista pública sin sesión y no se continuó; no se ingresaron credenciales.

## 21. Saturación y ruido (clipping)
El canal A1 llega a 0 y a 1018 (máximo observado) en las 5 ventanas de pestañeo: entre 38.65 % y 47.5 % de las muestras está en el límite inferior y 11.65–21.9 % cerca del superior, con rachas constantes de 722–806 ms. 8 de 10 segmentos tienen observaciones de calidad (reposo_002, 004 y 005 también tienen algo de saturación). Un clasificador podría estar aprendiendo saturación, amplitud extrema, tramos constantes o cambios de línea base en vez de la forma del pestañeo.

## 22. Limitaciones
Los resultados obtenidos corresponden únicamente a una prueba preliminar de la clase pestaneo1 frente a reposo. Las muestras proceden de un solo registro y presentan clipping, por lo que la exactitud obtenida no permite validar definitivamente el clasificador. Posteriormente, los datos de pestaneo1 se integrarán con las clases pestaneo2, pestaneo3 y los demás movimientos procesados por el grupo.

Además: 5 eventos de un único registro (4 de pestaneo1 en entrenamiento + 1 en testing; 4 de reposo en entrenamiento + 1 en testing); Testing con una muestra por clase; validación sin muestras de reposo; no hay validación clínica ni evidencia de generalización a otros usuarios; el H5 original no se verificó.

## 23. Integración futura
Integrar las clases pestaneo1, pestaneo2, pestaneo3, cerrar_ojos, izquierda, derecha, abajo, elevacion_ceja y reposo cuando los compañeros entreguen sus datos procesados con el mismo formato (`timestamp,eog_a1`, 2000 ms, 1000 Hz). Antes: registrar con menos ganancia o ajustar el sensor para evitar el clipping, tener más eventos y más de un registro, y garantizar muestras de cada clase en validación y testing.

## Capturas de pantalla (en `resultados/capturas/`)
1. Data acquisition: [01_data_acquisition.jpg](resultados/capturas/01_data_acquisition.jpg)
2. Muestra pestaneo1 (se ven las mesetas de saturación): [02_muestra_pestaneo1_001.jpg](resultados/capturas/02_muestra_pestaneo1_001.jpg)
3. Muestra reposo: [03_muestra_reposo_001.jpg](resultados/capturas/03_muestra_reposo_001.jpg)
4. Create impulse (EOG_RAW_1DCONV, capturado antes de renombrar): [04_create_impulse_1.jpg](resultados/capturas/04_create_impulse_1.jpg)
5. Feature Explorer (Spectrogram): [05_feature_explorer_spectrogram.jpg](resultados/capturas/05_feature_explorer_spectrogram.jpg)
6. Entrenamiento y explorador de datos (Raw 1D Conv): [06_07_clasificador_raw_1dconv.jpg](resultados/capturas/06_07_clasificador_raw_1dconv.jpg)
7. Matriz de confusión de validación (fila reposo vacía): [07_matriz_confusion_raw_1dconv.jpg](resultados/capturas/07_matriz_confusion_raw_1dconv.jpg)
8. Model Testing (100 %, 2 muestras): [08_model_testing_raw_1dconv.jpg](resultados/capturas/08_model_testing_raw_1dconv.jpg)
9. Comparación de experimentos con los nombres nuevos: [09_comparacion_experimentos.jpg](resultados/capturas/09_comparacion_experimentos.jpg)
10. Deployment WebAssembly int8 construido: [10_deployment_webassembly_int8.jpg](resultados/capturas/10_deployment_webassembly_int8.jpg)
11. Salida de la prueba local (texto): [prueba_local_wasm_pestaneo1.txt](resultados/prueba_local_wasm_pestaneo1.txt)
