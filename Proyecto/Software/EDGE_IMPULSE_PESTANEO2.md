# Edge Impulse — Movimiento: pestañeo doble (clase `pestaneo2`)

Estado (2026-11-20): **datos subidos al proyecto GRUPO11 y auditados. NO se entrenó ningún modelo** porque el proyecto mezcla muestras con ejes incompatibles (ver sección "Auditoría de GRUPO11"). Prueba preliminar pestaneo2 vs reposo, mismo flujo que `pestaneo1` (ver `EDGE_IMPULSE_PESTANEO1.md`).

## Archivos de entrada (en `datos/pestaneo/`, no modificados)
- `pestaneo2.txt`: registro OpenSignals (BITalino), 1000 Hz, canal A1 (EOG, ADC 10 bits), 46.05 s. Grabado el 2026-11-13.
- `pestaneo2eventos.txt`: 13 filas, 7 marcas únicas (15.45, 16.8, 21.15, 26.4, 32.55, 37.5, 43.65 s).
- `pestaneo2.h5`: **no se procesó** (`h5py` no disponible y no autorizado instalarlo). Verificar el H5 queda pendiente.

## Preparación de datos
Ventana de 2 s (0.5 s antes y 1.5 s después de la primera marca), línea base = mediana de los primeros 300 ms, columnas `timestamp,eog_a1`, 2000 filas (script `src/preparar_pestaneo2_edge_impulse.py`). Reposo: 5 ventanas de 2 s en huecos libres (6.475, 17.8, 23.275, 28.975 y 40.075 s). Sin ventanas superpuestas ni duplicadas entre Training y Test (verificado por tiempos). QC en `resultados/pestaneo2_control_calidad.csv`.

## Conversión a JSON
La subida de los CSV **falló las 5 veces**: el CSV Wizard activo del proyecto (config `mov5.csv`, de un compañero) busca una columna `A1` y mis CSV tienen `eog_a1` ("Cannot find value column A1"). No se tocó el Wizard. Se convirtieron los mismos datos al formato JSON de Edge Impulse (1 sensor `eog_a1`, `interval_ms` 1.0, 2000 valores; firma `none`), que no pasa por el Wizard. Quedan en `datos_edge_impulse_pestaneo2/json/{training|testing}/{pestaneo2|reposo}/`. Subida con "Enter label" y categoría explícita. Resultado en EI: 5 + 4 en Training y 1 + 1 en Test, todas de 2 s y con un solo eje `eog_a1` (comprobado abriendo `reposo_p2_004`; las 2000 muestras se comprobaron en los archivos antes de subir).

## Auditoría de las seis ventanas `pestaneo2` (visual + conteo)
Criterio: señal suavizada (50 ms); "deflexión" = excursión >800 (ADC) de al menos 60 ms. Figura: `resultados/pestaneo2_auditoria_ventanas.png`; tabla: `resultados/pestaneo2_auditoria_ventanas.csv`. No se usó solo el archivo de marcas.

| Ventana | Deflexiones altas (s) | Veredicto |
|---|---|---|
| 001 | 15.09–15.37 y 16.17–16.46 | Dos deflexiones (~1.1 s) |
| 002 | 21.51–21.80 | **Solo una clara**; el posible primer pestañeo (~20.2 s) queda ~0.45 s antes del inicio de la ventana |
| 003 | 26.60–26.69 y 27.09–27.17 | Dos (~0.5 s) |
| 004 | 32.33–32.47 y 32.70–32.88 | Dos (~0.4 s) |
| 005 | 37.10–37.47 y 38.54–38.72 | Dos (~1.4 s); la marca cae en el flanco de la primera |
| 006 | 43.39–43.54 y 43.76–43.99 | Dos (~0.4 s) |

Conclusión: **5 de 6 ventanas muestran dos deflexiones compatibles con dos pestañeos; la 002 muestra una.** Limitaciones: la señal está saturada (no hay polaridad ni forma de onda fiable), el conteo es por umbral, y hay dos ritmos distintos de doble pestañeo (~0.4–0.5 s y ~1.1–1.4 s). Las marcas no son un localizador preciso (preceden o siguen a la deflexión entre 0.1 y ~1.3 s).

### Ventanas de `reposo`
`reposo_p2_002`, `_003` y `_005` están limpias; `_004` tiene el inicio de una excursión alta al final (~30.9 s). **`reposo_p2_001` (6.475–8.475 s) está contaminada**: tiene 3 excursiones altas y 1 baja. Los primeros ~10 s de la grabación contienen muchas deflexiones sin marcar, por lo que no son reposo. Esa muestra sigue subida en Training (no se tocó); se recomienda deshabilitarla o reemplazarla antes del modelo final.

## Supuesto sobre las marcas 15.45 s y 16.8 s
Las dos marcas están a 1.35 s. En la señal hay dos deflexiones en 15.09–16.46 s, con separación (~1.1 s) comparable a las de los gestos 002 (~1.3 s) y 005 (~1.4 s), lo que es compatible con un solo doble pestañeo. Pero hay una tercera deflexión a ~17.2 s (~1.05 s después) y las marcas siguen a las deflexiones con desfases distintos al resto, así que **la evidencia no es concluyente**. Se mantienen como **un único gesto provisional** (6 gestos en total). No hay confirmación del participante. Una sola ventana (001) cubre ambas marcas, por lo que no hay duplicados.

## Clipping y ruido
A1 toca 0 y 1018 con frecuencia: en todo el registro ~17 % de las muestras ≤10 y ~12 % ≥1013; `pestaneo2_001` tiene 58 % en el límite inferior y 33 % en el superior. Las líneas base de 001, 002 y 005 están saturadas (corrección poco confiable). 8 de 11 segmentos tienen observaciones de calidad. Las muestras `reposo` limpias contienen casi sin deflexiones, así que un modelo podría aprender "hay deflexión grande o no", no "doble pestañeo" en específico.

## Auditoría de GRUPO11 (tabla en `resultados/pestaneo2_auditoria_grupo11.csv`)
| Clase | Training | Test | Duración | Ejes | Eje |
|---|---|---|---|---|---|
| pestaneo1 | 4 | 1 | 2 s | 1 | `eog_a1` |
| pestaneo2 | 5 | 1 | 2 s | 1 | `eog_a1` |
| reposo | 8 | 2 | 2 s | 1 | `eog_a1` |
| mov5 (compañero) | 5 | 0 | ~1 s | 2 | `A1`, `A2` |
| mov6 (compañero) | 0 | 7 | ~1 s | 2 | `A1`, `A2` |

Frecuencia: 1000 Hz en mis muestras (JSON `interval_ms` 1.0); la interfaz no la muestra para `mov5`/`mov6`, que duran ~1 s. Total Training 22, Test 11.

**Incompatibilidad:** `mov5` y `mov6` tienen dos ejes (`A1`, `A2`; A2 ≈ 0) y 1 s, frente al eje único `eog_a1` y 2 s de mis clases. Además `mov5` no tiene muestras en Test y `mov6` no tiene en Training.

## Decisión: no se entrenó
Siguiendo la instrucción de detenerse ante ejes incompatibles, **no se creó el experimento `EOG_GRUPO_PARCIAL_RAW_1DCONV`, no se generaron features, no hubo Model Testing y no se modificó el CSV Wizard ni ninguna muestra existente.** No hay resultados de entrenamiento para pestaneo2.

Propuesta (sin ejecutar): crear **copias** de las muestras `mov5`/`mov6` con un único eje `eog_a1` (tomando `A1`, descartando `A2`) y con la misma duración/ventana, conservando los originales; luego decidir si 1 s se rellena o se re-segmenta a 2 s. Alternativa: entrenar solo con `pestaneo1`, `pestaneo2` y `reposo` (todas `eog_a1`, 2 s), con experimento nuevo y sin tocar los anteriores.

## Limitaciones
Una sola grabación de `pestaneo2`, 6 gestos (5 en Training y 1 en Test), una muestra por clase en Test, ruido y saturación, ventana 002 con una sola deflexión, `reposo_p2_001` contaminada, marcas 15.45/16.8 s sin confirmar. Cualquier resultado futuro solo probaría el flujo y no sirve como validación.

## Pendiente (modelo multiclase final)
1. Confirmar con el participante la interpretación de las marcas (6 gestos).
2. Corregir la ventana 002 (p. ej. 19.9–21.9 s) y reemplazar/deshabilitar `reposo_p2_001`.
3. Estandarizar copias de `mov5`/`mov6` a `eog_a1`, 2 s (con aprobación del dueño de esos datos) o excluirlas.
4. Reunir más grabaciones y más muestras de Test por clase.
5. Entrenar un experimento nuevo preliminar, Model Testing, y solo después un deployment definitivo para la interfaz.
6. Verificar el H5 si se autoriza `h5py`.
