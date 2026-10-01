# LABORATORIO 6: USO DE BITALINO PARA ECG

## Índice

1. [Objetivos](#objetivos)
2. [Materiales y equipos](#materiales-y-equipos)
3. [Resultados](#resultados)
   - 3.1 [Conexión usada](#conexión-usada)
   - 3.2 [Video de la señal](#video-de-la-señal)
   - 3.3 [Ploteo de la señal en OpenSignal](#ploteo-de-la-señal-en-opensignal)
   - 3.4 [Archivos](#archivos)
   - 3.5 [Ploteo de la señal en Python](#ploteo-de-la-señal-en-python)
4. [Preguntas de la sesion](#preguntas-de-la-sesion)

## Objetivos

- 
- 
- 
- 

Se realizaron adquisiciones en:
- Derivación I de Einthoven.
- Derivación II de Einthoven.
- Derivación III de Einthoven.

Las condiciones evaluadas fueron:
- 
- 
- 
- 

## Materiales y equipos
- 
- 
- 
- 
-

## Procedimiento general
El sensor ECG se conectó a uno de los canales analógicos disponibles del BITalino. Después, los tres cables del sensor se conectaron a sus respectivos electrodos: entrada positiva (IN+), entrada negativa (IN−) y referencia (REF). Una vez verificada la conexión, se inició el registro en OpenSignals.

Se realizaron adquisiciones utilizando las derivaciones I, II y III de Einthoven. Para cada derivación se evaluaron cuatro condiciones:
- Reposo.
- Hipoventilación.
- Hiperventilación.
- Actividad física.

Durante el registro en reposo, el participante permaneció quieto y respiró con normalidad. En las pruebas respiratorias se modificó voluntariamente el patrón de respiración para generar las condiciones de hipoventilación e hiperventilación. Para la actividad física, el participante realizó el ejercicio establecido por el grupo y se registró la señal ECG correspondiente.
Finalmente, se detuvo cada adquisición y los registros obtenidos se guardaron en formato H5 y TXT para su posterior análisis.

## Resultados
Se empleó una conexión bipolar frontal. FP1 se utilizó como entrada positiva (IN+), FP2 como entrada negativa (IN−) y el electrodo de referencia se colocó detrás de la oreja.

# foto de conexión hecha por el grupo a WILL

## PRUEBA 1: Línea basal y apertura/cierre de ojos

#### A. Línea basal
El participante permaneció relajado, en silencio y sin estímulos externos durante aproximadamente uno a dos minutos. Se evitó el movimiento de la cabeza, los ojos y los músculos faciales para obtener una señal basal con la menor cantidad posible de artefactos.



#### B. Apertura y cierre de ojos
Después de registrar la línea basal, se realizaron cinco repeticiones de apertura y cierre de los ojos. Cada estado se mantuvo durante aproximadamente cinco segundos.

Esta prueba permitió comparar la señal obtenida con los ojos abiertos y cerrados. La actividad alfa suele presentar una mayor presencia durante la relajación con los ojos cerrados y disminuir al abrirlos. Sin embargo, este cambio se puede observar con mayor claridad mediante el análisis en frecuencia.



### Video de la señal 

#### A. Línea basal


#### B. Apertura y cierre de ojos


### Ploteo de la señal en OpenSignal
Para facilitar la visualización, se seleccionaron segmentos representativos de la línea basal y de los ciclos de apertura y cierre de ojos.

#### A. Línea basal


#### B. Apertura y cierre de ojos



### Archivos


### Ploteo de la señal en Python

#### A. Línea basal


#### B. Apertura y cierre de ojos


## PRUEBA 2: Preguntas complejas
Durante esta prueba se evaluó la señal EEG mientras el participante resolvía mentalmente cinco preguntas complejas. Para escuchar las indicaciones, se retiró uno de los audífonos. Cada pregunta tuvo una duración aproximada de 20 a 30 segundos.

El participante no respondió en voz alta y trató de mantener la cabeza, los ojos y los músculos faciales sin movimiento. El objetivo fue comparar la señal durante una tarea que requería atención y concentración con la señal obtenida durante la línea basal.


### Video de la señal 


### Ploteo de la señal en OpenSignal
En la imagen se presenta la señal EEG registrada mientras el participante resolvía las cinco preguntas. Para facilitar su interpretación, se deben señalar los intervalos correspondientes a cada pregunta.


### Archivos


### Ploteo de la señal en Python


## PRUEBA 3: Música suave

Durante esta prueba, el participante escuchó música suave durante aproximadamente uno a un minuto y medio. Se mantuvo relajado y evitó realizar movimientos innecesarios.

El objetivo fue registrar la señal EEG frente a un estímulo auditivo de baja intensidad y compararla posteriormente con la línea basal y con la prueba de música estruendosa.

### Video de la señal 


### Ploteo de la señal en OpenSignal
En la siguiente imagen se presenta la señal EEG registrada mientras el participante escuchaba música suave.


### Archivos


### Ploteo de la señal en Python



**## PRUEBA 4: Música estruendosa**

Durante esta prueba, el participante escuchó música estruendosa durante aproximadamente uno a un minuto y medio. Se mantuvieron las mismas condiciones de postura y conexión utilizadas durante la prueba de música suave.

El objetivo fue comparar la señal EEG obtenida con ambos estímulos auditivos. Para realizar esta comparación se debe considerar que los cambios también pueden estar relacionados con la atención, el tipo de música y los movimientos involuntarios del participante.

### Video de la señal 


### Ploteo de la señal en OpenSignal
En la siguiente imagen se presenta la señal EEG registrada mientras el participante escuchaba música estruendosa.


### Archivos


### Ploteo de la señal en Python





## Preguntas de la sesión

   - **¿Cuáles son las frecuencias significativas para la adquisición de señales de EEG?¿Son las mismas en todas las áreas cerebrales?** 
   Las bandas de frecuencias del EEG no son exactamente las mismas en tods las áreas cerebrales. Las bandas de frecuencia son las mismas como clasificación general, pero su potencia y predominancia pueden variar según la región cerebral, el estado del sujeto y la tarea realizada. Por ejemplo, la actividad alfa suele observarse con mayor claridad en regiones posteriroes, mientras que otras actividades pueden presentar mayor predominancia en regiones frontales.
   Las principales bandas de frecuencia del EEG son:
   - Delta (δ): Esta banda tiene una frecuencia aproximda de 0.5-4Hz y se asocia al sueño profundo
   - Theta (θ): La banda tiene una frecuencia de 4-8Hz y principalmente se asocia a la somnolencia, memoria y procesos cognitivos
   - Alpha (α): Con una frecuencia aproximada de 8-13Hz y se asocia a la relajación, especialmente con ojos cerrados
   - Beta (β): La banda Beta tiene una frecuencia de entre 13-30Hz y se asocia a la actividad mental, atención y concentración.
   - Gamma (γ): Enta banda abarca frecuencias mayores a 30Hz y se asocia a procesos cognitivos y percepción. 

   - **¿Qué tipo de filtro es esencial al trabajar con señales de EEG?¿Por qué es necesario aplicar dicho filtro?** 
   El filtro pasa banda (band-pass) es fundamental para el procesamiento del EEG, ya que permite conservar el rango de frecuencias de interés y atenuar componentes no deseados que distorsionen mi señal.
   Por ejemplo, dependiendo de lo que se quiera, puede utilizarse un rango de entre 0.5-40Hz para conservar las principales bandas del EEG y reducir ruido de alta frecuencia (>40Hz), deriva de la línea base y artefactos de muy baja frecuencia (<0.5Hz). Tambien, por la interferencia de red eléctrica, puede ser neceario un filtro de notch para reducir el ruido.
   
   - **¿Es posible influir en la señal de EEG mediante los pensamientos?¿Qué acción se puede realizar para activar una banda de frecuencia específica?¿Fue posible visualizar el cambio en la señal**  
   Sí, los pensamientos y estados mentales pueden modificar la actividad cerebral que registra el EEG, aunque no significa que podamos controlar voluntariamente una banda de frecuencia con precisión absoluta.
   Dando ejemplos de acciones que puedan activar una banda de frecuencia específica, si nos relajamos y cerramos los ojos, se puede aumenta la actividad alfa, especialmente en regiones posteriores; si nos concentramos en una tarea mental, se puede modificar principalmente la actividad beta dependiendo de la tarea.
   Por último, sí, el puede puede visualizarse en el EEG, aunque normalmente es más evidente al analizar la potencia de una banda mediante un espectro de frecuencia o un análisis tiempo-frecuencia que simplemente observando la señal cruda. Por ejemplo, al comparar ojos abiertos vs. ojos cerrados (como en el laboratorio), puede observarse un incremento de la potencia alfa durante los ojos cerrados.

   - **Muestre una captura de pantalla de una parte relevante de los datos de EEG obtenidos en el experimento propuesto.¿Corresponde esta señal a lo que esperaba?¿Por qué?**
   asda
   
   - **¿Existe alguna diferencia en la señalentre las dos ubicaciones, FP1 y FP2?** 
  

   - **Que frecuencias deberían variar durante las tareas planteadas?¿Es posible observar cambios específicos en la señal en bruto (RAW)? Describa lo que observa**
   asdas

   - **Según su criterio, ¿la amplitud de la señal de EEG se corresponde con el nivel de concentración aplicado?**
  

