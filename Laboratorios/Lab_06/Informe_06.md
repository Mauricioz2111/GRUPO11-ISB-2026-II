# LABORATORIO 6: USO DE BITALINO PARA EEG

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

## PRUEBA 1: Derivación I

### Conexión utilizada: Derivación I: El electrodo negativo (−) se coloca en RA, ubicado en la clavícula derecha, y el positivo (+) en LA, ubicado en la clavícula izquierda. El electrodo de referencia (REF) se coloca en la cresta ilíaca.
En esta prueba se utilizó la derivación I de Einthoven. El electrodo positivo, conectado al cable rojo (IN+), se colocó sobre la clavícula izquierda. El electrodo negativo, conectado al cable negro (IN-), se ubicó sobre la clavícula derecha. El electrodo de referencia, conectado al cable blanco (REF), se colocó en la cresta ilíaca. 

<p align="center">
  <img src="./Imágenes/prueba1_conexión.jpg" alt="Conexión de prueba" width="500">
</p>

#### A. Reposo
El participante permaneció quieto y mantuvo una respiración normal durante la adquisición. Se evitó mover los brazos y el resto del cuerpo para reducir los artefactos de movimiento y obtener una señal basal.

https://github.com/user-attachments/assets/7d7d8282-91c8-47d0-ba61-9d6debcc7626


#### B. Hipoventilación
Durante esta prueba, el participante disminuyó voluntariamente su frecuencia respiratoria. La señal ECG se registró durante esta condición para observar si el cambio en el patrón respiratorio producía variaciones en la señal.



<p align="center">
  <img src="./Imágenes/prueba1_hipo.jpg" alt="Hipoventilación para caso 1" width="500">
</p>

#### C. Hiperventilación
Durante esta prueba, el participante aumentó voluntariamente la frecuencia y profundidad de su respiración. La señal ECG se registró durante esta condición para observar las variaciones producidas por una respiración más rápida y profunda.




https://github.com/user-attachments/assets/c32edcd3-f383-4ba3-9b65-f405412b2bfe

#### D. Actividad física
El participante realizó la actividad física establecida por el grupo. La señal ECG se registró para observar los cambios producidos en la frecuencia cardiaca y la presencia de artefactos ocasionados por el movimiento.






### Video de la señal 


#### A. Reposo


#### B. Hipoventilación

https://github.com/user-attachments/assets/a032e770-d6e9-4e4d-9f10-4318813bb395
#### C. Hiperventilación

https://github.com/user-attachments/assets/92dbc05d-d1f6-4c48-842d-00e78e6e39eb

#### D. Actividad física

https://github.com/user-attachments/assets/ed31f0db-9505-4315-b5ab-c63d668f071d

### Ploteo de la señal en OpenSignal
En las imagenes, para facilitar la visualización del comportamiento de las señales, se delimitó el rango de tiempo entre 0 y 15 segundos
#### A. Reposo

![alt text](Imágenes/01_SeñalOpenSignal_lab04.jpeg)

#### B. Hipoventilación

![alt text](Imágenes/02_SeñalOpenSignal_lab04.jpeg)

#### C. Hiperventilación

![alt text](Imágenes/03_SeñalOpenSignal_lab04.jpeg)

#### D. Actividad física

![alt text](Imágenes/04_SeñalOpenSignal_lab04.jpeg)


### Archivos

[ECG en reposo - Derivación I](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Reposo_I.csv)

[ECG en Hipoventilación - Derivación I](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Hipoventilacion_I.csv)

[ECG en Hiperventilación - Derivación I](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Hiperventilacion_I.csv)

[ECG en Actividad física - Derivación I](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_actividadfisica_I.csv)

### Ploteo de la señal en Python
Ploteo de la señal en Python
#### A. Reposo

<img width="1200" height="400" alt="ECG_Reposo_1" src="https://github.com/user-attachments/assets/bef6af24-13bb-41cb-8634-e70bb7397bef" />

<img width="1200" height="400" alt="FFT_Reposo_1" src="https://github.com/user-attachments/assets/926a2d80-f254-4374-ad8b-b0564c7deb2f" />


#### B. Hipoventilación

<img width="1200" height="400" alt="ECG_Hipoventilacion_1" src="https://github.com/user-attachments/assets/b049e7aa-5547-439b-bcb8-d80c749b2bcc" />

<img width="1200" height="400" alt="FFT_Hipoventilacion_1" src="https://github.com/user-attachments/assets/c0aa8310-2eea-45fc-b2ae-548032230e6f" />


#### C. Hiperventilación

<img width="1200" height="400" alt="ECG_Hiperventilacion_1" src="https://github.com/user-attachments/assets/8810185c-2a5a-4a5b-86af-60650b632963" />

<img width="1200" height="400" alt="FFT_Hiperventilacion_1" src="https://github.com/user-attachments/assets/3aa186ba-a40d-4241-a200-0733248ccc26" />


#### D. Actividad física

<img width="1200" height="400" alt="ECG_ActividadFisica_1" src="https://github.com/user-attachments/assets/6cfbd5e7-b883-4620-b66d-479b4304f5bb" />

<img width="1200" height="400" alt="FFT_ActividadFisica_1" src="https://github.com/user-attachments/assets/06c67f64-c62b-487a-a745-3978e1fd067c" />

## PRUEBA 2: Derivación II

### Conexión utilizada:Derivación II: El electrodo negativo (−) se coloca en RA, ubicado en la clavícula derecha, y el positivo (+) en LL/LF, ubicado en la pierna izquierda. El electrodo de referencia (REF) se coloca en la cresta ilíaca.

En esta prueba se utilizó la derivación II de Einthoven, la cual registra la diferencia de potencial desde el brazo derecho, correspondiente al polo negativo, hacia la pierna izquierda, correspondiente al polo positivo.

Para obtener esta derivación, el electrodo negativo negro (IN−) se colocó en el lado correspondiente al brazo derecho y el electrodo positivo rojo (IN+) en la posición correspondiente a la pierna izquierda. El electrodo blanco se utilizó como referencia.

<p align="center">
  <img src="./Imágenes/prueba2_conexión.png" alt="Conexión de prueba 2" width="500">
</p>


#### A. Reposo
El participante permaneció quieto y respiró normalmente durante la adquisición. Este registro se utilizó como señal basal de la derivación II.

https://github.com/user-attachments/assets/d8814ab4-fb6f-4e16-b76a-a65e575d9085


#### B. Hipoventilación
El participante disminuyó voluntariamente su frecuencia respiratoria mientras se registraba la señal ECG mediante la derivación II. Se evitó realizar movimientos adicionales para reducir la aparición de artefactos.

<p align="center">
  <img src="./Imágenes/prueba2_hipo.jpg" alt="Hipoventilación para caso 2" width="500">
</p>

#### C. Hiperventilación
El participante aumentó voluntariamente la frecuencia y profundidad de la respiración mientras se registraba la señal ECG mediante la derivación II.

https://github.com/user-attachments/assets/4a5d418c-aa11-4dcd-8c74-164994804043

#### D. Actividad física
El participante realizó la actividad física establecida por el grupo y se registró la señal correspondiente a la derivación II. Esta adquisición permitió observar los cambios posteriores al esfuerzo físico.

https://github.com/user-attachments/assets/c2fcb044-5dac-4cd2-b5eb-d6344efd8973



### Video de la señal 


#### A. Reposo


#### B. Hipoventilación



https://github.com/user-attachments/assets/ba160a4e-98d6-4db4-87b7-93162339581a


#### C. Hiperventilación

https://github.com/user-attachments/assets/204ea454-55b3-43f6-a29e-63909ff0f8cd


#### D. Actividad física


https://github.com/user-attachments/assets/d5f3f819-1b03-4b83-9730-5f76fcc96100



### Ploteo de la señal en OpenSignal
En las imagenes, para facilitar la visualización del comportamiento de las señales, se delimitó el rango de tiempo entre 0 y 15 segundos
#### A. Reposo

![alt text](Imágenes/05_SeñalOpenSignal_lab04.jpeg)

#### B. Hipoventilación

![alt text](Imágenes/06_SeñalOpenSignal_lab04.jpeg)

#### C. Hiperventilación

![alt text](Imágenes/07_SeñalOpenSignal_lab04.jpeg)

#### D. Actividad física

![alt text](Imágenes/08_SeñalOpenSignal_lab04.jpeg)

### Archivos

[ECG en reposo - Derivación II](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Reposo_II.csv)

[ECG en Hipoventilación - Derivación II](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Hipoventilacion_II.csv)

[ECG en Hiperventilación - Derivación II](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Hiperventilacion_II.csv)

[ECG en Actividad física - Derivación II](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_actividadfisica_II.csv)

### Ploteo de la señal en Python

#### A. Reposo

<img width="1200" height="400" alt="ECG_Reposo_2" src="https://github.com/user-attachments/assets/2e1610df-ddbb-4744-9f9f-19d60275b5d5" />

<img width="1200" height="400" alt="FFT_Reposo_2" src="https://github.com/user-attachments/assets/9843ce6a-e82b-4103-98ae-f2c04a808512" />

#### B. Hipoventilación

<img width="1200" height="400" alt="ECG_Hipoventilacion_2" src="https://github.com/user-attachments/assets/4c11bcaf-68f7-4710-a959-b565c22b6798" />

<img width="1200" height="400" alt="FFT_Hipoventilacion_2" src="https://github.com/user-attachments/assets/50776dab-e5fb-440d-911c-3b0b7a3aa1ce" />


#### C. Hiperventilación

<img width="1200" height="400" alt="ECG_Hiperventilacion_2" src="https://github.com/user-attachments/assets/63958c79-146a-4727-a988-47a2541e0108" />

<img width="1200" height="400" alt="FFT_Hiperventilacion_2" src="https://github.com/user-attachments/assets/ba632b29-911b-45c2-b662-826b37ce9417" />

#### D. Actividad física

<img width="1200" height="400" alt="ECG_ActividadFisica_2" src="https://github.com/user-attachments/assets/f0f1994b-c251-4ad4-9932-2986baba1fec" />

<img width="1200" height="400" alt="FFT_ActividadFisica_2" src="https://github.com/user-attachments/assets/dbbdb984-a23e-4753-9d5b-c3853173831f" />

## PRUEBA 3: Derivación III

### Conexión utilizada:El electrodo negativo (−) se coloca en LA, ubicado en la clavícula izquierda, y el positivo (+) en LL/LF, ubicado en la pierna izquierda. El electrodo de referencia (REF) se coloca en la cresta ilíaca.
En esta prueba se utilizó la derivación III de Einthoven, la cual registra la diferencia de potencial desde el brazo izquierdo, correspondiente al polo negativo, hacia la pierna izquierda, correspondiente al polo positivo.

El electrodo negativo negro (IN−) se colocó en la posición correspondiente al brazo izquierdo y el electrodo positivo rojo (IN+) en la posición correspondiente a la pierna izquierda. El electrodo blanco se utilizó como referencia.

<p align="center">
  <img src="./Imágenes/prueba3_conexión.jpg" alt="Conexión de prueba 3" width="500">
</p>


#### A. Reposo
El participante permaneció quieto y respiró normalmente durante la adquisición. Este registro se utilizó como señal basal de la derivación III.

https://github.com/user-attachments/assets/161a731d-d6a2-48fe-adad-bcf8fa3ecc25

#### B. Hipoventilación
El participante disminuyó voluntariamente su frecuencia respiratoria mientras se registraba la señal ECG mediante la derivación III.

<p align="center">
  <img src="./Imágenes/prueba3_hipo.jpg" alt="Hipoventilación para caso 3" width="500">
</p>

#### C. Hiperventilación
El participante aumentó voluntariamente la frecuencia y profundidad de la respiración mientras se registraba la señal ECG mediante la derivación III.

https://github.com/user-attachments/assets/869587b5-dbec-4f50-a69a-dcaad1c3abbf

#### D. Actividad física
El participante realizó la actividad física establecida por el grupo y se registró la señal ECG correspondiente a la derivación III. Durante el análisis se deberá considerar que el movimiento puede introducir artefactos en el registro.

https://github.com/user-attachments/assets/aec6b3a4-caf0-4b57-a255-c6e012211248



### Video de la señal 


#### A. Reposo


https://github.com/user-attachments/assets/ea1c222f-60b3-41ae-8806-2a52cf408884



#### B. Hipoventilación

https://github.com/user-attachments/assets/fe62237a-57e4-478c-bb79-23d00ca022cb


#### C. Hiperventilación


https://github.com/user-attachments/assets/2e155caa-2d93-448d-8b06-60f5b2979c4b


#### D. Actividad física

https://github.com/user-attachments/assets/502d7bc4-ee32-402c-bf42-1f743ed8ff26


### Ploteo de la señal en OpenSignal
En las imagenes, para facilitar la visualización del comportamiento de las señales, se delimitó el rango de tiempo entre 0 y 15 segundos
#### A. Reposo

![alt text](Imágenes/09_SeñalOpenSignal_lab04.jpeg)

#### B. Hipoventilación

![alt text](Imágenes/10_SeñalOpenSignal_lab04.jpeg)

#### C. Hiperventilación

![alt text](Imágenes/11_SeñalOpenSignal_lab04.jpeg)

#### D. Actividad física

![alt text](Imágenes/12_SeñalOpenSignal_lab04.jpeg)


### Archivos

[ECG en reposo - Derivación III](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Reposo_III.csv)

[ECG en Hipoventilación - Derivación III](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Hipoventilacion_III.csv)

[ECG en Hiperventilación - Derivación III](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_Hiperventilacion_III.csv)

[ECG en Actividad física - Derivación III](https://github.com/Mauricioz2111/GRUPOX-ISB-2026-II/blob/main/Laboratorios/Lab_04/DatosSeñalesECG_CSV/ECG_actividadfisica_III.csv)

### Ploteo de la señal en Python

#### A. Reposo

<img width="1200" height="400" alt="ECG_Reposo_3" src="https://github.com/user-attachments/assets/18e649e0-9613-42b0-9754-a45cf4d4e530" />

<img width="1200" height="400" alt="FFT_Reposo_3" src="https://github.com/user-attachments/assets/d6c977d5-1c08-45e1-a2be-a8fefe95a299" />

#### B. Hipoventilación

<img width="1200" height="400" alt="ECG_Hiperventilacion_3" src="https://github.com/user-attachments/assets/ec37e23d-ca0d-4a3e-90f0-8b61b947ef05" />

<img width="1200" height="400" alt="FFT_Hipoventilacion_3" src="https://github.com/user-attachments/assets/6be74305-326c-4074-b328-0ebdcba312f5" />

#### C. Hiperventilación

<img width="1200" height="400" alt="ECG_Hiperventilacion_3" src="https://github.com/user-attachments/assets/e21889d1-5f07-4dfd-9e31-cc62ce9b2d46" />

<img width="1200" height="400" alt="FFT_Hiperventilacion_3" src="https://github.com/user-attachments/assets/a55ea0b1-52dc-468f-a14f-047127efee7f" />

#### D. Actividad física

<img width="1200" height="400" alt="ECG_ActividadFisica_3" src="https://github.com/user-attachments/assets/e039b20e-7c95-46a6-9952-0d35f12bbbde" />

<img width="1200" height="400" alt="FFT_ActividadFisica_3" src="https://github.com/user-attachments/assets/d760b35f-f39b-4f33-af2f-05f3175d7dc7" />

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
  

