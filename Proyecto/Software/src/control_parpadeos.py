from collections import Counter
from pathlib import Path
import re
import threading
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, detrend, find_peaks, sosfiltfilt


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

# Tiempo disponible desde el primer parpadeo
VENTANA_SEGUNDOS = 5.0

# Se utiliza si el TXT no indica la frecuencia de muestreo
FRECUENCIA_MANUAL = 1000.0

# -1 significa que se usará la última columna numérica del TXT
COLUMNA_EOG = -1

# Evita detectar varias veces un mismo parpadeo
DISTANCIA_MINIMA = 0.35

# Sensibilidad de la detección
FACTOR_UMBRAL = 6.0


# ============================================================
# ACCIONES DE PESTANEO1, PESTANEO2 Y PESTANEO3
# ============================================================

def ejecutar_accion(cantidad):
    """
    Ejecuta una acción de acuerdo con el número
    de parpadeos detectados.
    """

    if cantidad == 1:
        pestaneo1()

    elif cantidad == 2:
        pestaneo2()

    elif cantidad == 3:
        pestaneo3()

    elif cantidad > 3:
        print(
            f"Secuencia inválida: "
            f"se detectaron {cantidad} eventos."
        )

    else:
        print("No se detectaron parpadeos.")


def pestaneo1():
    print("PESTANEO1: se detectó 1 parpadeo.")
    print("Acción: acceder a la opción 1.")

    # Posteriormente se coloca aquí la acción real.
    # Ejemplo:
    # abrir_actividad_1()


def pestaneo2():
    print("PESTANEO2: se detectaron 2 parpadeos.")
    print("Acción: acceder a la opción 2.")

    # Posteriormente se coloca aquí la acción real.
    # Ejemplo:
    # abrir_actividad_2()


def pestaneo3():
    print("PESTANEO3: se detectaron 3 parpadeos.")
    print("Acción: acceder a la opción 3.")

    # Posteriormente se coloca aquí la acción real.
    # Ejemplo:
    # abrir_actividad_3()


# ============================================================
# CONTROL DE PARPADEOS EN TIEMPO REAL
# ============================================================

class ControlTiempoReal:

    def __init__(self):
        self.contador = 0
        self.temporizador = None
        self.bloqueo = threading.Lock()

    def registrar_parpadeo(self):
        """
        Esta función se ejecutará cada vez que el sistema
        reconozca un parpadeo individual.
        """

        with self.bloqueo:

            if self.contador >= 3:
                print(
                    "Ya se registraron 3 parpadeos. "
                    "Espere el resultado."
                )
                return

            self.contador += 1

            print(
                f"Parpadeo {self.contador} registrado."
            )

            # El primer parpadeo inicia la ventana
            if self.contador == 1:

                print(
                    "Se inició la ventana de 5 segundos."
                )

                self.temporizador = threading.Timer(
                    VENTANA_SEGUNDOS,
                    self.cerrar_ventana
                )

                self.temporizador.daemon = True
                self.temporizador.start()

    def cerrar_ventana(self):
        """
        Se ejecuta automáticamente al finalizar
        los cinco segundos.
        """

        with self.bloqueo:

            cantidad = self.contador

            # Reinicio del contador
            self.contador = 0
            self.temporizador = None

        print("\nFinalizaron los 5 segundos.")

        ejecutar_accion(cantidad)

        print(
            "\nSistema listo para una nueva secuencia."
        )

    def cancelar(self):
        """
        Cancela la secuencia antes de cerrar.
        """

        with self.bloqueo:

            if self.temporizador is not None:
                self.temporizador.cancel()

            self.contador = 0
            self.temporizador = None


# ============================================================
# SIMULACIÓN CON EL TECLADO
# ============================================================

def probar_con_teclado():

    control = ControlTiempoReal()

    print("\nB + Enter: simular un parpadeo")
    print("Q + Enter: regresar al menú\n")

    while True:

        opcion = input("> ").strip().lower()

        if opcion == "b":
            control.registrar_parpadeo()

        elif opcion == "q":
            control.cancelar()
            return

        else:
            print(
                "Use B para parpadear "
                "o Q para regresar."
            )


# ============================================================
# LECTURA DE LA FRECUENCIA DE OPENSIGNALS
# ============================================================

def obtener_frecuencia(ruta):
    """
    Busca la frecuencia de muestreo dentro
    del encabezado del TXT.
    """

    patrones = [
        r'"sampling rate"\s*:\s*([0-9]+(?:\.[0-9]+)?)',
        r'"sampling_rate"\s*:\s*([0-9]+(?:\.[0-9]+)?)',
        r'"sample rate"\s*:\s*([0-9]+(?:\.[0-9]+)?)'
    ]

    with ruta.open(
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as archivo:

        for _ in range(30):

            linea = archivo.readline()

            if not linea:
                break

            for patron in patrones:

                resultado = re.search(
                    patron,
                    linea,
                    re.IGNORECASE
                )

                if resultado:
                    return float(
                        resultado.group(1)
                    )

    print(
        "No se encontró la frecuencia en el "
        "encabezado."
    )

    print(
        f"Se utilizará "
        f"{FRECUENCIA_MANUAL:.0f} Hz."
    )

    return FRECUENCIA_MANUAL


# ============================================================
# LECTURA DEL ARCHIVO TXT
# ============================================================

def cargar_txt(ruta):
    """
    Lee las filas numéricas del archivo TXT
    generado por OpenSignals.
    """

    filas = []

    with ruta.open(
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as archivo:

        for linea in archivo:

            linea = linea.strip()

            # Omite encabezados y líneas vacías
            if not linea or linea.startswith("#"):
                continue

            elementos = re.split(
                r"[;\t\s]+",
                linea
            )

            try:

                fila = [
                    float(elemento)
                    for elemento in elementos
                    if elemento
                ]

            except ValueError:
                continue

            if fila:
                filas.append(fila)

    if not filas:

        raise ValueError(
            "El TXT no contiene filas "
            "numéricas reconocibles."
        )

    # Identifica la cantidad de columnas más frecuente
    numero_columnas = Counter(
        len(fila) for fila in filas
    ).most_common(1)[0][0]

    filas_validas = [
        fila
        for fila in filas
        if len(fila) == numero_columnas
    ]

    return np.asarray(
        filas_validas,
        dtype=float
    )


# ============================================================
# FILTRADO DE LA SEÑAL EOG
# ============================================================

def filtrar_senal(senal, frecuencia_muestreo):
    """
    Elimina la tendencia y aplica un filtro
    pasa banda.
    """

    senal_sin_tendencia = detrend(
        senal,
        type="linear"
    )

    frecuencia_alta = min(
        15.0,
        0.45 * frecuencia_muestreo
    )

    if frecuencia_alta <= 0.5:

        raise ValueError(
            "La frecuencia de muestreo "
            "es demasiado baja."
        )

    filtro = butter(
        4,
        [0.5, frecuencia_alta],
        btype="bandpass",
        fs=frecuencia_muestreo,
        output="sos"
    )

    senal_filtrada = sosfiltfilt(
        filtro,
        senal_sin_tendencia
    )

    return senal_filtrada


# ============================================================
# DETECCIÓN DE PICOS
# ============================================================

def detectar_picos(
    senal_filtrada,
    frecuencia_muestreo
):
    """
    Detecta los posibles parpadeos mediante
    un umbral calculado desde la propia señal.
    """

    magnitud = np.abs(senal_filtrada)

    mediana = np.median(magnitud)

    mad = np.median(
        np.abs(magnitud - mediana)
    )

    variacion = 1.4826 * mad

    if variacion == 0:
        variacion = np.std(magnitud)

    if variacion == 0:

        raise ValueError(
            "La señal no presenta variación "
            "suficiente."
        )

    umbral = (
        mediana
        + FACTOR_UMBRAL * variacion
    )

    distancia_muestras = max(
        1,
        int(
            DISTANCIA_MINIMA
            * frecuencia_muestreo
        )
    )

    picos, propiedades = find_peaks(
        magnitud,
        height=umbral,
        prominence=2.0 * variacion,
        distance=distancia_muestras
    )

    return picos, propiedades, umbral


# ============================================================
# AGRUPACIÓN EN VENTANAS DE CINCO SEGUNDOS
# ============================================================

def agrupar_picos(tiempos_picos):
    """
    Agrupa los parpadeos que ocurren dentro
    de los cinco segundos posteriores al primero.
    """

    grupos = []
    indice = 0

    while indice < len(tiempos_picos):

        inicio = tiempos_picos[indice]
        siguiente = indice

        while (
            siguiente < len(tiempos_picos)
            and tiempos_picos[siguiente] - inicio
            <= VENTANA_SEGUNDOS
        ):
            siguiente += 1

        grupos.append(
            tiempos_picos[indice:siguiente]
        )

        indice = siguiente

    return grupos


# ============================================================
# GENERACIÓN DE LA GRÁFICA
# ============================================================

def guardar_grafica(
    ruta,
    tiempo,
    senal_filtrada,
    picos,
    umbral
):
    """
    Guarda una gráfica con los picos detectados.
    """

    magnitud = np.abs(senal_filtrada)

    plt.figure(figsize=(12, 5))

    plt.plot(
        tiempo,
        magnitud,
        linewidth=0.8,
        color="navy",
        label="EOG filtrado"
    )

    plt.axhline(
        umbral,
        color="red",
        linestyle="--",
        label="Umbral"
    )

    if len(picos) > 0:

        plt.scatter(
            tiempo[picos],
            magnitud[picos],
            color="orange",
            edgecolor="black",
            label="Picos detectados",
            zorder=3
        )

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")

    plt.title(
        "Detección de parpadeos EOG"
    )

    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()

    ruta_salida = ruta.with_name(
        f"{ruta.stem}_picos.png"
    )

    plt.savefig(
        ruta_salida,
        dpi=200
    )

    plt.close()

    return ruta_salida


# ============================================================
# ANÁLISIS DEL TXT DE OPENSIGNALS
# ============================================================

def analizar_txt():

    texto_ruta = input(
        "Pegue la ruta completa "
        "del archivo TXT:\n> "
    ).strip()

    # Elimina comillas si se copia la ruta
    # utilizando "Copiar como ruta" en Windows.
    ruta = Path(
        texto_ruta.strip('"')
    )

    if not ruta.exists():

        print(
            f"No se encontró el archivo:\n{ruta}"
        )

        return

    try:

        frecuencia_muestreo = obtener_frecuencia(
            ruta
        )

        datos = cargar_txt(ruta)

        numero_columnas = datos.shape[1]

        if not (
            -numero_columnas
            <= COLUMNA_EOG
            < numero_columnas
        ):

            print(
                f"El TXT contiene "
                f"{numero_columnas} columnas."
            )

            print(
                f"La columna "
                f"{COLUMNA_EOG} no existe."
            )

            return

        senal_eog = datos[
            :,
            COLUMNA_EOG
        ]

        senal_filtrada = filtrar_senal(
            senal_eog,
            frecuencia_muestreo
        )

        picos, propiedades, umbral = detectar_picos(
            senal_filtrada,
            frecuencia_muestreo
        )

        tiempo = (
            np.arange(
                len(senal_filtrada)
            )
            / frecuencia_muestreo
        )

        tiempos_picos = tiempo[picos]

        grupos = agrupar_picos(
            tiempos_picos
        )

        print("\n========== RESULTADOS ==========")

        print(
            f"Archivo: {ruta.name}"
        )

        print(
            f"Frecuencia de muestreo: "
            f"{frecuencia_muestreo:.2f} Hz"
        )

        print(
            f"Columnas encontradas: "
            f"{numero_columnas}"
        )

        print(
            f"Columna EOG utilizada: "
            f"{COLUMNA_EOG}"
        )

        print(
            f"Total de picos detectados: "
            f"{len(picos)}"
        )

        if not grupos:

            ejecutar_accion(0)

        else:

            for numero, grupo in enumerate(
                grupos,
                start=1
            ):

                print(
                    f"\nSecuencia {numero}"
                )

                tiempos_texto = ", ".join(
                    f"{valor:.2f} s"
                    for valor in grupo
                )

                print(
                    f"Tiempos: {tiempos_texto}"
                )

                ejecutar_accion(
                    len(grupo)
                )

        ruta_grafica = guardar_grafica(
            ruta,
            tiempo,
            senal_filtrada,
            picos,
            umbral
        )

        print(
            f"\nGráfica guardada en:\n"
            f"{ruta_grafica}"
        )

    except (
        ValueError,
        IndexError
    ) as error:

        print(
            f"No se pudo analizar "
            f"el archivo: {error}"
        )


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def main():

    while True:

        print("\n====================================")
        print("     CONTROL DE PARPADEOS EOG")
        print("====================================")

        print(
            "1. Probar parpadeos con el teclado"
        )

        print(
            "2. Analizar un TXT de OpenSignals"
        )

        print(
            "3. Cerrar"
        )

        opcion = input("> ").strip()

        if opcion == "1":
            probar_con_teclado()

        elif opcion == "2":
            analizar_txt()

        elif opcion == "3":
            print("Programa finalizado.")
            break

        else:
            print(
                "Seleccione 1, 2 o 3."
            )


if __name__ == "__main__":
    main()