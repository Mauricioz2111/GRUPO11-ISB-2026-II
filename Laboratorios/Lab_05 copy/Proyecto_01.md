# Avance 1 – Introducción a Señales Biomédicas
## 1. Nombre del proyecto
**UCIPlay — Sistema EOG que se adapta a cada mirada.**

## 2. Integrantes
- Integrante 1: Wilber Mauricio Zenteno Castilla
- Integrante 2: Mastio Torres Ricalde
- Integrante 3: Jairo Villalobos Vargas
- Integrante 4: Miguel Tello Ocaña

## 3. Planteamiento del problema
En las Unidades de Cuidados Intensivos Pediátricos (UCIP) hay niños que a pesar de estar concientes de lo que pasa a su alrededor, no son capaces de usar las manos ni el habla con normalidad, esto debido a el uso de dispositivos que necesitan de la inmovilización del usuario, para mantenerlos estables, como el tubo endotraqueal con ventilación mecánica, los catéteres, las vías centrales, los inmovilizadores, etc. En este caso la limitación no surge de un daño motor o neurológico permanente, sino que es una condición clínica y del tratamiento.
En esta situación, la estimulación del niño es más importante de lo que parece. Para un niño, jugar o realizar actividades sencillas ayuda a mantener la atención, orientarse en lo que ocurre a su alrededor y distraerse del miedo y de la incomodidad [1]. Cuando pasa varios días en una cama recibiendo muy poca estimulación, sumado a la sedación y la inmovilización, se pueden generar efectos psicológicos negativos, como cambios repentinos de atención y pensamiento que pueden confundir al niño y desconectarlo de su entorno [2]. Además, los niños que logran superar las adversidades de su tratamiento, desarrollan después secuelas físicas, cognitivas, emocionales y sociales, lo que se conoce como Síndrome Post-Cuidados Intensivos [3]. Por eso, se ha visto que actividades como el juego y la estimulación cognitiva ayudan a reducir el delirium y mejoran el estado mental de los niños hospitalizados [4], [5].
Los movimientos oculares suelen ser uno de los canales que estos niños todavía pueden usar. Sin embargo, la capacidad no es igual en todos, un niño puede controlar mejor los movimientos horizontales, otro los verticales y otro solo el parpadeo. Además, la capacidad varía a partir del tipo de tratamiento, por ejemplo un paciente crítico puede cambiar su capacidad ocular según la sedación, el cansancio o su estado clínico del momento. Por lo que una interfaz con comandos fijos para todos podría fallar o ser muy difícil de usar, es por eso, que se necesita una herramienta que primero evalúe qué movimientos oculares conserva cada niño y después adapte su funcionamiento a esa capacidad.

### 3.1. Descripción de la condición
El proyecto no está dirigido a una enfermedad en particular, sino a una condición referente a niños conscientes hospitalizados en una Unidad de Cuidados Intensivos Pediátricos (UCIP) los cuales tienen una movilidad restringida por dispositivos médicos, pero que aún conservan la capacidad de percepción del entorno e interacción con el.
Se estima que aproximadamente tres de cada cinco niños que ingresan a una UCIP presentan delirium, una alteración repentina y temporal de la atención, la consciencia y la cognición, este está relacionado con la sedación e inmovilización que los niños padecen al reciben ventilación mecánica [2]. Además, como cada vez sobreviven más niños a los cuidados intensivos, también aumentan los casos con secuelas físicas, cognitivas, emocionales y sociales a largo plazo. Este conjunto se conoce como Síndrome Post-Cuidados Intensivos (PICS) y afecta tanto al paciente como a su familia [3].
Entre las posibles consecuencias de esta situación, la más grave es el riesgo de delirium durante la UCIP, seguido de las secuelas cognitivas, emocionales y sociales que pueden aparecer a largo plazo por el PICS [2], [3]. También se suman la ansiedad, el miedo y la sensación de pérdida de control que suelen vivir los niños durante la hospitalización [1], y la dificultad para comunicar sus necesidades, ya que estos pacientes son considerados vulnerables en comunicación [6]. En su estancia en la UCIP, el niño depende por completo de terceros para cualquier actividad de entretenimiento o estimulación, esto complica la situación del niño, porque la evidencia sobre estimulación cognitiva y juego asume, en su mayoría, que el niño puede usar las manos, así que casi no hay estrategias pensadas para quienes no pueden hacerlo [4].
Un niño en una sala general puede jugar con las manos, mientras que un niño de UCIP, a pesar de tener la capacidad cognitiva para poder participar en estos juegos, está limitado por los dispositivos que lo mantienen estable, restringiendo las interacciones que las manos y el habla podrían proporcionarle. A pesar de esto, los músculos que mueven los ojos suelen verse menos afectados por estos dispositivos, así que el movimiento ocular puede funcionar como un canal de interacción que todavía se puede aprovechar.
Este sistema no busca reemplazar al personal de salud ni a los especialistas en juego terapéutico, por el contrario, busca ofrecer un canal de interacción adicional para los momentos en que el niño esté consciente y sin acompañamiento. El sistema podría usarse en otras condiciones, siempre que el usuario conserve al menos un movimiento ocular voluntario que se pueda registrar mediante EOG.

### 3.2. Importancia del problema
En el ámbito hospitalario peruano, un análisis de costos en dos UCIP del Ministerio de Salud reportó que el tratamiento con ventilación mecánica tuvo un costo unitario promedio de S/ 5076,52, con una estancia promedio de 8 días [7]. Son varios días en los que el niño puede pasar mucho tiempo despierto y sin ninguna actividad que lo estimule. Además, un estudio sobre los cuidados intensivos pediátricos en Latinoamérica demostro que la tecnología disponible varía considerablemente entre países e incluso entre ciudades [8]. Esto hace poco probable que todos los establecimientos del país cuenten con equipos de seguimiento ocular comerciales. Por eso es necesario investigar alternativas que se puedan desarrollar con equipos accesibles como BITalino, programas de código abierto y una interfaz que funcione sin conexión permanente a internet.
Acerca de la estimulación lúdica como apoyo para los infantes, una revisión de la Universidad Norbert Wiener indica que el juego terapéutico ya se reconoce como beneficioso en pacientes pediátricos hospitalizados en el país, pero su aplicación formal en unidades de cuidados críticos sigue siendo limitada [9].
A nivel internacional, la situación es parecida. Hay evidencia de que la estimulación cognitiva y el juego ayudan a reducir el delirium y mejoran el estado mental de los niños hospitalizados, pero su uso a gran escala se ve limitado por la falta de recursos y porque casi siempre se plantean para niños que pueden usar las manos [4], [5]. Además, los sistemas de seguimiento ocular para UCI son muy costosos. Un hospital del Reino Unido reportó un gasto de cerca de USD 13 000 por un solo equipo [10], una cifra difícil de asumir en el contexto peruano descrito arriba.
Con lo anterior, la población objetivo del proyecto se delimita a niños conscientes de aproximadamente 4 a 12 años, hospitalizados en una UCIP, con la movilidad manual restringida por dispositivos médicos (y no por un daño neurológico permanente), y que conserven al menos un movimiento ocular voluntario detectable. Esto los diferencia de otras poblaciones ya trabajadas con EOG, como los pacientes con ELA.

### 3.3. Relación con la señal biomédica

El electrooculograma (EOG), una señal electrofisiológica, se genera por los movimientos oculares y puede medirse con electrodos colocados alrededor del ojo. En general, un EOG mide la diferencia de potencial entre la retina y la córnea. El globo ocular puede modelarse como un dipolo con la córnea positiva en la parte frontal y la retina negativa en la parte posterior. Las principales aplicaciones del EOG son el diagnóstico oftalmológico y el registro de los movimientos oculares. Para registrar los movimientos oculares, se suelen colocar electrodos de superficie en cuatro posiciones alrededor de los ojos (arriba, abajo, izquierda y derecha). El par de electrodos colocados arriba y abajo de los ojos se utiliza para medir el movimiento vertical de los ojos, y el par de electrodos colocados a la izquierda y derecha de los ojos se utiliza para medir el movimiento horizontal de los ojos. Cuando la mirada se desplaza hacia la izquierda, el campo eléctrico del lado izquierdo de los ojos se vuelve positivo y el del lado opuesto se vuelve negativo [11].
En varios estudios de interacción persona-ordenador basados en EOG, los electrodos se colocaban de manera que uno se ubicaba encima y otro por debajo del ojo (izquierdo o derecho) [20].
> ![alt text](<Imágenes/Colocación de electrodos para EOG convencional.JPG>)

> **Figura 1.** Colocación de electrodos para EOG convencional [11].
Normalmente se utiliza la EOG para monitorizar los movimientos oculares o para confirmar enfermedades como la "enfermedad de Best" la cual se identifica por la apariencia de un fondo de ojo amarillo huevo y se puede confirmar mediante el registro de un electroretinograma (ERG) y un electrooculograma (EOG) [12]. En este proyecto, la señal no se utilizará para identificar qué enfermedad tiene el usuario, sino para reconocer los movimientos oculares que todavía puede controlar.
Un desafío central en la adquisición de esta señal es su alta vulnerabilidad frente a diversos artefactos, como los movimientos palpebrales (parpadeo), la contaminación electromiográfica (EMG) de alta frecuencia, los temblores musculares leves y las variaciones por la posición o impedancia de los electrodos [13]. Adicionalmente, al ser una señal electrofisiológica, parámetros como la amplitud, la duración y la velocidad de los movimientos varian en cada persona. Por ello, el sistema deberá realizar una calibración individual y no utilizar exactamente los mismos parámetros para todos los usuarios.

### 3.4. Problema específico
Los niños conscientes hospitalizados en una UCI pediátrica que presentan movilidad restringida por dispositivos médicos tienen dificultades para interactuar y acceder de manera autónoma a actividades de entretenimiento y estimulación cognitiva, debido a que las alternativas convencionales requieren interacción manual. Aunque existen sistemas de control mediante la mirada que permiten una interacción sin manos, su elevado costo y la limitada adaptación a las capacidades oculomotoras individuales dificultan su aplicación en este contexto.

### 3.5. Pregunta del proyecto
> ¿Cómo puede una interfaz basada en señales EOG adaptarse a las capacidades oculomotoras individuales de niños conscientes con movilidad restringida en UCI pediátrica para permitir su interacción con actividades lúdico-educativas sin requerir interacción manual?

## 4. Propuesta de solución
### 4.1. Descripción general
Se propone desarrollar una interfaz lúdico-interactiva basada en señales de electrooculografía (EOG) que permita a niños conscientes con movilidad restringida interactuar con actividades de entretenimiento y estimulación cognitiva sin requerir el uso de las manos. El sistema estará diseñado para adaptarse individualmente a las capacidades oculomotoras de cada usuario, en lugar de imponer una configuración de comandos fija.
La propuesta parte de que la capacidad de realizar determinados movimientos oculares puede variar entre usuarios. Por ello, antes de iniciar la interacción, el sistema realizará una calibración individual destinada a caracterizar las respuestas EOG asociadas a diferentes movimientos oculares y determinar cuáles pueden ser identificados de manera suficientemente consistente.
Durante la calibración, el sistema solicitará al usuario realizar diferentes acciones, como mirar hacia la izquierda, derecha, arriba y abajo, así como realizar parpadeos voluntarios. Las señales obtenidas serán procesadas para identificar características relevantes de cada movimiento, considerando parámetros como amplitud, duración, dirección, velocidad de cambio y comportamiento de la señal durante el reposo.
A partir de esta información, el sistema determinará qué comandos pueden utilizarse de manera confiable y seleccionará automáticamente una modalidad de interacción adecuada para el usuario. Por ejemplo:
- **Control horizontal:** si los movimientos hacia la izquierda y derecha presentan una detección suficientemente consistente, estos podrán utilizarse para desplazarse entre opciones.
- **Control vertical:** si los movimientos verticales presentan mejor separabilidad que los horizontales, podrán utilizarse como comandos principales.
- **Control multidireccional:** si varios movimientos son identificados correctamente, se habilitará una interfaz con un mayor número de comandos.
- **Control mediante parpadeo:** si el usuario presenta un movimiento ocular limitado pero puede realizar parpadeos voluntarios de manera consistente, podrá utilizarse un esquema basado en selección mediante barrido automático.
- **Recalibración:** si durante la calibración las señales presentan baja separabilidad, elevada variabilidad o demasiado ruido, el sistema solicitará repetir el proceso antes de habilitar la interacción.
De esta manera, el sistema no asumirá que todos los usuarios poseen las mismas capacidades oculomotoras. La configuración de la interfaz será determinada a partir de la señal registrada de cada usuario.
Una vez completada la calibración, los movimientos oculares detectados serán convertidos en comandos digitales que permitirán controlar diferentes actividades dentro de la interfaz. Estas actividades podrían incluir juegos sencillos, selección de imágenes, ejercicios de memoria, reconocimiento de patrones, actividades educativas y otras tareas de estimulación cognitiva adaptadas al contexto pediátrico.
> ![alt text](<Imágenes/Arquitectura general del sistema.JPG>)

> **Figura 2.** Arquitectura general del sistema
Un aspecto fundamental será que el sistema también deberá distinguir entre movimientos intencionales y estados de reposo. Esto permitirá evitar que pequeñas fluctuaciones de la señal sean interpretadas como comandos. Asimismo, podrán implementarse mecanismos de confirmación, tiempos mínimos de activación o zonas de tolerancia para reducir activaciones accidentales.

### 4.2. Diferenciador del proyecto
El proyecto no se plantea como la creación de la primera interfaz controlada mediante EOG, debido a que tanto las interfaces EOG como los sistemas de interacción mediante seguimiento ocular y los juegos controlados por la mirada han sido previamente investigados. El diferenciador propuesto se encuentra en la adaptación individual de la interfaz al repertorio oculomotor disponible en cada usuario. En lugar de utilizar una configuración predeterminada del tipo (izquierda = comando1, derecha = comando2) para todos los usuarios, el sistema buscará determinar previamente qué movimiento pueden ser ejecutados y detectados de forma consistente por cada persona.
Esta adaptación permitiría seleccionar los comandos que mejor se ajusten a las capacidades oculomotoras detectadas durante la calibración, con el objetivo de facilitar una interacción más accesible y personalizada. En el contexto de la UCI pediátrica, la interfaz podría permitir que niños conscientes con movilidad restringida participen en actividades lúdicas, de entretenimiento y estimulación cognitiva sin requerir interacción manual. De esta manera, además de constituir una aplicación de la interfaz EOG adaptativa, el sistema podría proporcionar una alternativa de interacción que favorezca la participación del niño durante su estancia hospitalaria y contribuya a hacer más llevadero el tiempo de hospitalización.

### 4.3. Obtención de los datos
Para el desarrollo de la interfaz propuesta se realizará una primera etapa de adquisición de señales electrooculográficas (EOG) mediante el sistema BITalino, utilizando su sensor específico para electrooculografía. El EOG permite registrar los cambios de potencial eléctrico asociados con la rotación del globo ocular, que puede modelarse eléctricamente como un dipolo con una región corneal relativamente positiva y una región retinal relativamente negativa. Cuando el ojo cambia de orientación, cambia la distribución de este potencial sobre la superficie de la piel y, por tanto, la diferencia de potencial registrada por los electrodos [11]–[13].
Para identificar los movimientos oculares en dos dimensiones se emplearán dos componentes de la señal:
- **EOG horizontal (EOG-H):** obtenido mediante electrodos ubicados aproximadamente a los lados de los ojos, permitiendo identificar movimientos hacia la izquierda y derecha.
- **EOG vertical (EOG-V):** obtenido mediante electrodos ubicados por encima y por debajo del ojo, permitiendo identificar movimientos hacia arriba y abajo y proporcionando información útil para la detección del parpadeo.

### 4.4. Protocolo de adquisición
Cada participante realizará una secuencia controlada de movimientos oculares correspondiente a las seis clases consideradas en el proyecto:
1. Izquierda.
2. Derecha.
3. Arriba.
4. Abajo.
5. Parpadeo voluntario.
6. Reposo.
Cada movimiento deberá repetirse varias veces para obtener suficientes ejemplos de cada clase. Entre movimientos se incorporarán períodos de reposo para facilitar posteriormente la segmentación de los eventos.
Además de las señales adquiridas mediante BITalino, se utilizará una base de datos pública de señales EOG como fuente independiente de información para evaluar el procesamiento y clasificación propuestos.
Una fuente adecuada para este proyecto es el **EOG Dataset de la University of Malta**, desarrollado dentro del proyecto EyeCon. La Universidad de Malta proporciona públicamente diferentes conjuntos de señales EOG para investigación.
Particularmente, el **Dataset 1: Zero-Centred Horizontal and Vertical Bipolar EOG Data** contiene señales EOG horizontales y verticales. Cada ensayo incluye dos movimientos sacádicos y un parpadeo: el participante realiza un movimiento desde el centro hacia una posición indicada, regresa al centro y posteriormente realiza un parpadeo. Los participantes mantenían la cabeza apoyada en un soporte para reducir los movimientos de esta [14].

### 4.5. Procesamiento propuesto
Las señales obtenidas mediante BITalino y las señales de la base pública serán sometidas a un procesamiento previo antes de realizar la clasificación.
La finalidad del procesamiento es reducir el ruido y los artefactos, corregir la deriva de línea base y obtener características que permitan diferenciar los movimientos oculares. Las revisiones sobre interfaces EOG identifican el procesamiento de la señal como una etapa fundamental antes de la clasificación. Para el procesamiento de los datos se considerará la adquisición de la señal mediante el Bitalino, después un filtrado, corrección de línea base, una segmentación de los movimientos, extracción de las características [13], [15].

#### 4.5. Características que se analizarán
- **Amplitud máxima:** mayor valor positivo alcanzado por la señal.
- **Amplitud mínima:** menor valor registrado durante el movimiento.
- **Rango de amplitud:** diferencia entre la amplitud máxima y mínima.
- **Duración del movimiento:** tiempo durante el cual se mantiene el cambio.
- **Pendiente máxima:** rapidez con la que cambia la señal.
Estas características permitirán comparar los movimientos y determinar cuáles son más estables para cada usuario.

### 4.6. Clasificación o detección
**Clasificación de las señales EOG**
Las señales EOG procesadas serán clasificadas en seis categorías: izquierda, derecha, arriba, abajo, parpadeo voluntario y reposo. Se utilizarán dos estrategias: un método basado en umbrales personalizados y algoritmos de aprendizaje automático, como SVM y Random Forest, con el fin de comparar su desempeño. Los métodos basados en umbrales son utilizados en sistemas EOG para identificar movimientos direccionales a partir de variaciones de amplitud y polaridad de la señal [13], [15], [16].

**Clasificación mediante umbrales personalizados**
Antes de la clasificación se realizará una calibración individual, en la cual cada usuario ejecutará repetidamente los seis movimientos definidos. A partir de estas señales se determinarán las características propias de cada usuario y los umbrales correspondientes.
Para el canal horizontal se utilizarán los cambios de amplitud para diferenciar los movimientos hacia la izquierda y derecha, mientras que el canal vertical permitirá identificar los movimientos hacia arriba y abajo. La dirección asociada a cada polaridad dependerá de la disposición de los electrodos y será determinada durante la calibración.
De manera general:
EOG horizontal > umbral positivo → Derecha
EOG horizontal < umbral negativo → Izquierda
EOG vertical > umbral positivo → Arriba
EOG vertical < umbral negativo → Abajo
Los valores de los umbrales serán calculados individualmente y no serán establecidos como valores fijos para todos los usuarios. Esto permite considerar la variabilidad de amplitud existente entre personas y entre diferentes condiciones de adquisición.

**Ejemplo de determinación de umbrales**
Durante la calibración, las señales de un usuario pueden presentar valores positivos para un movimiento horizontal y negativos para el movimiento contrario. A partir de la distribución de amplitudes obtenida en varias repeticiones se establecerán los límites de clasificación.
Por ejemplo, si experimentalmente se determina un umbral horizontal de 250 µV, de manera ilustrativa:
EOG horizontal > +250 µV → Derecha
EOG horizontal < −250 µV → Izquierda
Este valor es únicamente un ejemplo; los umbrales reales serán determinados para cada usuario mediante la etapa de calibración.

**Clasificación del parpadeo y reposo**
El parpadeo voluntario se clasificará utilizando principalmente el canal vertical y características temporales como amplitud, duración y velocidad de cambio, debido a que su comportamiento temporal permite diferenciarlo de los movimientos verticales de la mirada [13], [16].
La clase reposo se utilizará cuando la señal permanezca dentro del rango establecido durante la calibración y no se detecte un evento ocular significativo. De esta manera, el sistema evitará asignar un comando cuando el usuario no esté realizando intencionalmente un movimiento.
El proceso general será:
Señal EOG → extracción de características → umbrales personalizados → clasificación
Las clases finales serán: izquierda, derecha, arriba, abajo, parpadeo y reposo.

### 4.7. Frontend
La aplicación será desarrollada en Python utilizando Streamlit y podrá ejecutarse de manera local en una computadora, sin requerir una conexión permanente a Internet. La interfaz integrará las diferentes etapas del sistema EOG y permitirá realizar el proceso completo de interacción.
La aplicación contará con los siguientes apartados:
- **Adquisición:** recepción y visualización de las señales EOG provenientes del BITalino.
- **Calibración:** registro de los movimientos de cada usuario para determinar sus características y establecer los umbrales personalizados.
- **Procesamiento:** filtrado, corrección de línea base y segmentación de las señales.
- **Características:** visualización de parámetros como amplitud, rango, duración, velocidad y otras características extraídas.
- **Clasificación:** identificación de las seis clases: izquierda, derecha, arriba, abajo, parpadeo y reposo.
- **Configuración personalizada:** almacenamiento y aplicación de los umbrales determinados durante la calibración de cada usuario.
- **Actividad interactiva:** utilización de los movimientos oculares clasificados como comandos para controlar actividades de entretenimiento o estimulación cognitiva.
- **Resultados:** visualización del desempeño de la clasificación mediante métricas como accuracy, precision, recall, F1-score y matriz de confusión.
De esta manera, la aplicación permitirá integrar en una única plataforma la adquisición, calibración, procesamiento, extracción de características, clasificación y utilización de las señales EOG, manteniendo un funcionamiento local que facilite su uso en el contexto de la UCIP.

### 4.8. Resultado esperado
Se espera que el programa entregue:
- Gráfica de la señal EOG original adquirida durante la prueba.
- Gráfica de la señal después del filtrado.
- Movimiento ocular detectado: izquierda, derecha, arriba, abajo o parpadeo.
- Porcentaje de reconocimiento obtenido para cada movimiento.
- Comandos habilitados y deshabilitados según los resultados de la calibración.
- Perfil individual de comandos EOG recomendado.
- Historial de las opciones seleccionadas durante la sesión.
- Acción ejecutada dentro de la actividad, como avanzar, desplazarse, seleccionar o confirmar.
- Retroalimentación visual o auditiva después de cada acción.
- Aviso cuando la calidad de la señal disminuya o sea necesario repetir la calibración.
Estos son resultados esperados del prototipo, tomando como referencia la calibración individual y el reconocimiento de movimientos mediante EOG descritos por Lin et al. [16]. La interfaz incluirá actividades sencillas de entretenimiento y ejercicios de atención, memoria o selección. En esta etapa no se evaluará si su uso produce una mejora cognitiva medible en el niño; eso requeriría un diseño de evaluación aparte.
Los porcentajes de reconocimiento y las métricas de desempeño se colocarán recién después de probar el prototipo. La evaluación inicial se hará con voluntarios sanos. Usarlo directamente con niños hospitalizados requeriría autorización institucional, consentimiento informado y aprobación de un comité de ética, algo que queda fuera del alcance de esta etapa del proyecto.

## 5. Paper de referencia
### 5.1. Información del paper
- **Título:** Design of a Wearable Eye-Movement Detection System Based on Electrooculography Signals and Its Experimental Validation.
- **Autores:** Chin-Teng Lin, Wei-Ling Jiang, Sheng-Fu Chen, Kuan-Chih Huang y Lun-De Liao.
- **Año:** 2021.
- **Revista:** Biosensors.
- **Volumen:** 11. **Número:** 9. **Artículo:** 343.
- **DOI:** https://doi.org/10.3390/bios11090343

### 5.2. Problema abordado
Los autores desarrollaron una interfaz humano-computadora basada en EOG capaz de reconocer distintos movimientos oculares en tiempo real. El problema que identificaron fue que varias interfaces oculares anteriores tenían dificultades de estabilidad de la señal, de implementación del hardware y de variabilidad entre usuarios. Para resolverlo, construyeron un sistema portátil con una etapa de calibración individual, procesamiento de la señal y clasificación de movimientos, que luego usaron para controlar una interfaz en computadora [16].
Esto se relaciona directamente con lo que nosotros necesitamos: reconocer distintos movimientos oculares y convertirlos en comandos para controlar una actividad sin usar las manos.

### 5.3. Datos utilizados
En el estudio de Lin et al. [16]:
- Participaron seis hombres sanos, entre 20 y 28 años.
- Los participantes se ubicaron frente a un monitor.
- Se registraron señales EOG horizontales y verticales con electrodos Ag/AgCl y también con sensores secos.
- La frecuencia de muestreo fue de 51,2 Hz.
- Se evaluaron movimientos hacia arriba, abajo, izquierda y derecha, además de movimientos diagonales, de mayor amplitud, parpadeo y fijación.
- El estudio contó con la aprobación de un comité de ética.
Una limitación importante es que todos los participantes fueron adultos sanos; el estudio no se hizo con niños ni en una UCIP [16].

### 5.4. Metodología
El sistema se dividió en cuatro etapas: calibración de parámetros individuales, preprocesamiento de la señal, extracción de características y clasificación de los movimientos. Colocaron electrodos en las regiones laterales de los ojos para el componente horizontal, por encima y debajo de un ojo para el componente vertical, y un electrodo de referencia entre las cejas. En la calibración, cada participante realizaba los movimientos solicitados y con esas señales se calculaban los parámetros para reconocer fijación, parpadeo y cada dirección. Con los movimientos ya clasificados, controlaban una interfaz de marcación: se desplazaban con arriba, abajo, izquierda y derecha, y confirmaban con un doble parpadeo [16].
De este paper tomamos como base la calibración individual, la separación de las señales horizontal y vertical, el reconocimiento de movimientos direccionales y la detección del parpadeo [16]. Nosotros reduciremos los movimientos que se convertirán en comandos a cinco: izquierda, derecha, arriba, abajo y parpadeo.

### 5.5. Resultados principales
El sistema logró reconocer los movimientos oculares en tiempo real y usarlos para controlar la interfaz. En la evaluación más exigente (diez tipos de movimiento con electrodos Ag/AgCl), la exactitud promedio fue de 87,67 %. Con sensores secos, la exactitud promedio fue de 88,6 %. No todos los movimientos se reconocieron igual de bien: el movimiento hacia arriba fue el más confiable, mientras que algunos movimientos diagonales generaron más errores de clasificación [16].
Entre las limitaciones, participaron solo seis personas, todas adultas y sanas; no hubo pruebas con población pediátrica; la señal podía variar según la posición de los electrodos; los parpadeos inesperados a veces se confundían con movimientos verticales; la presión de los sensores podía limitar el movimiento, y los movimientos de cabeza o rostro podían generar artefactos en la señal [16].

### 5.6. Relación con el proyecto
Usamos este paper como referencia principal porque presenta un sistema capaz de reconocer varios movimientos oculares mediante EOG y convertirlos en comandos, con una etapa de calibración individual que evita depender de un solo patrón de señal para todos los usuarios. De ahí tomamos la calibración individual, la separación de los componentes horizontal y vertical, la detección del parpadeo y la clasificación de movimientos hacia los cuatro lados.
Adaptamos ese enfoque a una interfaz lúdico-interactiva para niños conscientes que presentan una limitación temporal para usar las manos por su condición clínica o por los dispositivos médicos conectados. Después de la calibración, el sistema habilitará solo los comandos que cada niño pueda controlar de forma estable; si no logra controlar los cinco movimientos, la actividad podrá funcionar con menos comandos o con un modo de barrido automático.
La diferencia principal es que el paper controla una interfaz de marcación y fue evaluado en adultos sanos, mientras que nuestro prototipo está pensado para actividades de entretenimiento, atención y selección, como una futura aplicación pediátrica que todavía necesitaría validación clínica.
**Paper complementario**
Tonin et al. (2020) se mantiene como antecedente complementario [17], [18]. Sirve para mostrar que movimientos oculares voluntarios de poca amplitud pueden usarse como comandos en personas con movilidad severamente limitada, aunque su sistema trabaja con un esquema binario (sí/no) y no con clasificación de cinco clases [17], [19].
- **Título:** Auditory Electrooculogram-based Communication System for ALS Patients in Transition from Locked-in to Complete Locked-in State.
- **DOI:** https://doi.org/10.1038/s41598-020-65333-1

## 6. Referencias bibliográficas
[1] W. H. C. Li, J. O. K. Chung, K. Y. Ho y B. M. C. Kwok, “Play interventions to reduce anxiety and negative emotions in hospitalized children,” BMC Pediatrics, vol. 16, art. 36, 2016. https://doi.org/10.1186/s12887-016-0570-5

[2] A. G. Bjerkan, M. Hulsund, H. B. H. Brenne y M.-E. Eilertsen, “Nurses’ perspectives on early mobilization of intubated children in the pediatric intensive care unit: a qualitative study of barriers and facilitators,” Frontiers in Pediatrics, 2026. https://doi.org/10.3389/fped.2026.1853836

[3] J. Engel, F. von Borell, I. Baumgartner, M. Kumpf, M. Hofbeck, J. Michel y F. Neunhoeffer, “Modified ABCDEF-Bundles for Critically Ill Pediatric Patients—What Could They Look Like?,” Frontiers in Pediatrics, vol. 10, art. 886334, 2022. https://doi.org/10.3389/fped.2022.886334

[4] E. Fatima, I. Hill, N. Dover y H. Faisal, “Exploring Cognitive Stimulation as a Therapy for the Prevention of Delirium in a Hospital Setting: A Narrative Review,” Behavioral Sciences, vol. 15, n.º 2, art. 186, 2025. https://doi.org/10.3390/bs15020186

[5] V. N. A. Bharuchi y M. A. Rasheed, “Effect of play-based intervention on children’s mental status and caregiver involvement during hospitalization: findings from Pakistan,” BMC Pediatrics, vol. 24, art. 239, 2024. https://doi.org/10.1186/s12887-024-04659-5

[6] J. M. Costello, L. Patak y J. Pritchard, “Communication vulnerable patients in the pediatric ICU: Enhancing care through augmentative and alternative communication,” Journal of Pediatric Rehabilitation Medicine, vol. 3, n.º 4, pp. 289–301, 2010. https://doi.org/10.3233/PRM-2010-0140

[7] J. C. Alvarado-Jaramillo, A. J. Gonzáles-Ramos y P. Mendoza-Arana, “Análisis de costos en dos unidades de cuidados intensivos pediátricos del Ministerio de Salud del Perú,” Anales de la Facultad de Medicina, vol. 72, n.º 4, pp. 249–254, 2011. http://www.scielo.org.pe/scielo.php?script=sci_arttext&pid=S1025-55832011000400005

[8] S. Campos-Miño, J. S. Sasbón y B. von Dessauer, “Los cuidados intensivos pediátricos en Latinoamérica,” Medicina Intensiva, vol. 36, n.º 1, pp. 3–10, 2012. https://scielo.isciii.es/scielo.php?script=sci_arttext&pid=S0210-56912012000100002

[9] A. Y. Huaynates Castro y J. B. Caro Valera, Eficacia del juego terapéutico en la disminución del dolor, ansiedad y mejora del cuidado humanizado en pacientes pediátricos hospitalizados, trabajo académico, Universidad Privada Norbert Wiener, 2018. https://repositorio.uwiener.edu.pe/items/518a9372-4cac-4353-ad63-6c701a413088

[10] University Hospitals Plymouth NHS Trust, “How Subtle Eye Movements Have Opened Up New Communication Possibilities,” 2023. https://www.plymouthhospitals.nhs.uk/charity-news-events/how-subtle-eye-movements-have-opened-up-new-communication-possibilities-7263/

[11] J. Heo, H. Yoon y K. S. Park, “A Novel Wearable Forehead EOG Measurement System for Human Computer Interfaces,” Sensors, vol. 17, n.º 7, art. 1485, 2017. https://doi.org/10.3390/s17071485

[12] D. J. Creel, “The electrooculogram,” Handbook of Clinical Neurology, vol. 160, pp. 495–499, 2019. https://doi.org/10.1016/B978-0-444-64032-1.00033-3

[13] W.-D. Chang, “Electrooculograms for Human–Computer Interaction: A Review,” Sensors, vol. 19, n.º 12, art. 2690, 2019. https://doi.org/10.3390/s19122690

[14] N. Barbara, T. A. Camilleri y K. P. Camilleri, “A comparison of EOG baseline drift mitigation techniques,” Biomedical Signal Processing and Control, vol. 57, art. 101738, 2020. https://doi.org/10.1016/j.bspc.2019.101738. Base de datos: https://www.um.edu.mt/cbc/ourprojects/eyecon/eogdataset/. Descarga del Dataset 1: https://www.um.edu.mt/media/um/docs/centres/cbc/DATASET.zip

[15] C. Belkhiria, A. Boudir, C. Hurter y V. Peysakhovich, “EOG-Based Human–Computer Interface: 2000–2020 Review,” Sensors, vol. 22, n.º 13, art. 4914, 2022. https://doi.org/10.3390/s22134914

[16] C.-T. Lin, W.-L. Jiang, S.-F. Chen, K.-C. Huang y L.-D. Liao, “Design of a Wearable Eye-Movement Detection System Based on Electrooculography Signals and Its Experimental Validation,” Biosensors, vol. 11, n.º 9, art. 343, 2021. https://doi.org/10.3390/bios11090343

[17] A. Tonin, A. Jaramillo-Gonzalez, A. Rana, M. Khalili-Ardali, N. Birbaumer y U. Chaudhary, “Auditory Electrooculogram-Based Communication System for ALS Patients in Transition from Locked-in to Complete Locked-in State,” Scientific Reports, vol. 10, art. 8452, 2020. https://doi.org/10.1038/s41598-020-65333-1

[18] A. Jaramillo-Gonzalez, S. Wu, A. Tonin, A. Rana, M. Khalili Ardali, N. Birbaumer y U. Chaudhary, “A dataset of EEG and EOG from an auditory EOG-based communication system for patients in locked-in state,” Scientific Data, vol. 8, art. 8, 2021. https://doi.org/10.1038/s41597-020-00789-4

[19] W. D. Chang, H. S. Cha, D. Y. Kim, S. H. Kim y C. H. Im, “Development of an electrooculogram-based eye-computer interface for communication of individuals with amyotrophic lateral sclerosis,” Journal of NeuroEngineering and Rehabilitation, vol. 14, art. 89, 2017. https://doi.org/10.1186/s12984-017-0303-5

[20] C. Belkhiria y V. Peysakhovich, “Electro-Encephalography and Electro-Oculography in Aeronautics: A Review Over the Last Decade (2010–2020),” Frontiers in Neuroergonomics, vol. 1, art. 606719, 2020. https://doi.org/10.3389/fnrgo.2020.606719

