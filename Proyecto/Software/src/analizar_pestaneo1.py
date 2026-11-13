from pathlib import Path
import json

import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# UBICACIÓN DE LOS ARCHIVOS
# ============================================================

# El programa se encuentra dentro de Software/src.
BASE_SOFTWARE = Path(__file__).resolve().parent.parent

CARPETA_DATOS = (
    BASE_SOFTWARE
    / "datos"
    / "pestaneo"
)

ARCHIVO_SENAL = (
    CARPETA_DATOS
    / "pestaneo1.txt"
)

ARCHIVO_EVENTOS = (
    CARPETA_DATOS
    / "pestaneo1eventos.txt"
)


# ============================================================
# CONFIGURACIÓN DEL SEGMENTO
# ============================================================

# Se extraerán 1.5 segundos antes y después
# del pestañeo marcado.
SEGUNDOS_ANTES = 1.5
SEGUNDOS_DESPUES = 1.5

# Si se coloca None, se utiliza automáticamente
# el primer evento del archivo.
TIEMPO_EVENTO_MANUAL = None


# ============================================================
# LECTURA DEL ENCABEZADO DE OPENSIGNALS
# ============================================================

def leer_encabezado_opensignals(ruta):
    """
    Obtiene información como la frecuencia de
    muestreo y los nombres de las columnas.
    """

    with ruta.open(
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as archivo:

        for linea in archivo:

            if linea.startswith("# {"):

                contenido = json.loads(
                    linea[2:].strip()
                )

                dispositivo = next(
                    iter(contenido.values())
                )

                return dispositivo

            if linea.strip() == "# EndOfHeader":
                break

    raise ValueError(
        "No se encontró el encabezado "
        "de OpenSignals."
    )


# ============================================================
# LECTURA DE LOS EVENTOS
# ============================================================

def leer_eventos(ruta):
    """
    Lee los tiempos marcados durante la adquisición.
    """

    eventos = []

    with ruta.open(
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as archivo:

        for linea in archivo:

            linea = linea.strip()

            if not linea or linea.startswith("#"):
                continue

            columnas = linea.split("\t")

            if len(columnas) < 5:
                continue

            eventos.append(
                {
                    "mac": columnas[0],
                    "canal": columnas[1],
                    "id": columnas[2],
                    "inicio": float(columnas[3]),
                    "fin": float(columnas[4])
                }
            )

    if not eventos:

        raise ValueError(
            "No se encontraron eventos "
            "en el archivo de anotaciones."
        )

    return eventos


def obtener_inicios_unicos(eventos):
    """
    Evita contar dos veces eventos que tienen
    el mismo tiempo de inicio.
    """

    inicios = []

    for evento in eventos:

        tiempo = evento["inicio"]

        if (
            not inicios
            or not np.isclose(
                tiempo,
                inicios[-1]
            )
        ):
            inicios.append(tiempo)

    return inicios


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    # Verificación de los archivos
    if not ARCHIVO_SENAL.exists():

        raise FileNotFoundError(
            f"No se encontró:\n{ARCHIVO_SENAL}"
        )

    if not ARCHIVO_EVENTOS.exists():

        raise FileNotFoundError(
            f"No se encontró:\n{ARCHIVO_EVENTOS}"
        )

    # Lectura del encabezado
    encabezado = leer_encabezado_opensignals(
        ARCHIVO_SENAL
    )

    frecuencia = float(
        encabezado["sampling rate"]
    )

    nombres_columnas = encabezado["column"]

    # Se utiliza A1, no la última columna
    if "A1" not in nombres_columnas:

        raise ValueError(
            "El archivo no contiene "
            "el canal A1."
        )

    columna_a1 = nombres_columnas.index("A1")

    # Carga de las muestras numéricas
    datos = np.loadtxt(
        ARCHIVO_SENAL,
        comments="#"
    )

    senal_a1 = datos[:, columna_a1]

    tiempo_total = (
        np.arange(len(senal_a1))
        / frecuencia
    )

    # Lectura de las anotaciones
    eventos = leer_eventos(
        ARCHIVO_EVENTOS
    )

    inicios = obtener_inicios_unicos(
        eventos
    )

    print(
        "Eventos encontrados:",
        inicios
    )

    # El primer evento corresponde a pestañeo
    if TIEMPO_EVENTO_MANUAL is None:

        tiempo_evento = inicios[0]

    else:

        tiempo_evento = float(
            TIEMPO_EVENTO_MANUAL
        )

    # Conversión de tiempo a muestras
    muestra_inicio = max(
        0,
        int(
            round(
                (
                    tiempo_evento
                    - SEGUNDOS_ANTES
                )
                * frecuencia
            )
        )
    )

    muestra_final = min(
        len(senal_a1),
        int(
            round(
                (
                    tiempo_evento
                    + SEGUNDOS_DESPUES
                )
                * frecuencia
            )
        )
    )

    # Extracción del segmento
    segmento_raw = senal_a1[
        muestra_inicio:muestra_final
    ]

    tiempo_segmento = (
        tiempo_total[
            muestra_inicio:muestra_final
        ]
        - tiempo_evento
    )

    # Cálculo de la línea basal
    muestras_basales = max(
        1,
        int(0.5 * frecuencia)
    )

    nivel_basal = np.median(
        segmento_raw[:muestras_basales]
    )

    segmento_centrado = (
        segmento_raw
        - nivel_basal
    )

    # Evaluación de saturación
    porcentaje_bajo = (
        100
        * np.mean(segmento_raw <= 5)
    )

    porcentaje_alto = (
        100
        * np.mean(segmento_raw >= 1018)
    )

    # Carpeta de resultados
    carpeta_resultados = (
        BASE_SOFTWARE
        / "resultados"
        / "pestaneo1"
    )

    carpeta_resultados.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # GUARDADO DEL SEGMENTO EN CSV
    # ========================================================

    ruta_csv = (
        carpeta_resultados
        / "pestaneo1_segmento.csv"
    )

    salida_csv = np.column_stack(
        (
            tiempo_segmento,
            segmento_raw,
            segmento_centrado
        )
    )

    np.savetxt(
        ruta_csv,
        salida_csv,
        delimiter=",",
        header=(
            "tiempo_relativo_s,"
            "A1_raw,"
            "A1_centrada"
        ),
        comments="",
        fmt="%.6f"
    )

    # ========================================================
    # GRÁFICA
    # ========================================================

    ruta_grafica = (
        carpeta_resultados
        / "pestaneo1_segmento.png"
    )

    figura, ejes = plt.subplots(
        2,
        1,
        figsize=(12, 7),
        sharex=True
    )

    # Señal original
    ejes[0].plot(
        tiempo_segmento,
        segmento_raw,
        color="navy",
        linewidth=0.8
    )

    ejes[0].axvline(
        0,
        color="red",
        linestyle="--",
        label="Evento: pestañeo"
    )

    ejes[0].set_ylabel(
        "A1 raw"
    )

    ejes[0].set_title(
        "Pestañeo 1: segmento "
        "registrado en OpenSignals"
    )

    ejes[0].grid(
        alpha=0.25
    )

    ejes[0].legend()

    # Señal centrada
    ejes[1].plot(
        tiempo_segmento,
        segmento_centrado,
        color="darkgreen",
        linewidth=0.8
    )

    ejes[1].axvline(
        0,
        color="red",
        linestyle="--"
    )

    ejes[1].axhline(
        0,
        color="black",
        linewidth=0.7
    )

    ejes[1].set_xlabel(
        "Tiempo respecto al evento (s)"
    )

    ejes[1].set_ylabel(
        "A1 centrada"
    )

    ejes[1].grid(
        alpha=0.25
    )

    plt.tight_layout()

    plt.savefig(
        ruta_grafica,
        dpi=200
    )

    plt.close(figura)

    # ========================================================
    # RESULTADOS EN LA TERMINAL
    # ========================================================

    print("\n========== PESTAÑEO 1 ==========")

    print(
        f"Frecuencia de muestreo: "
        f"{frecuencia:.0f} Hz"
    )

    print(
        f"Duración del registro: "
        f"{len(senal_a1) / frecuencia:.2f} s"
    )

    print(
        f"Canal utilizado: "
        f"A1, columna {columna_a1}"
    )

    print(
        f"Evento utilizado: "
        f"{tiempo_evento:.2f} s"
    )

    print(
        f"Muestras extraídas: "
        f"{len(segmento_raw)}"
    )

    print(
        f"Nivel basal estimado: "
        f"{nivel_basal:.2f}"
    )

    print(
        f"Muestras cercanas al "
        f"límite inferior: "
        f"{porcentaje_bajo:.2f} %"
    )

    print(
        f"Muestras cercanas al "
        f"límite superior: "
        f"{porcentaje_alto:.2f} %"
    )

    print(
        f"CSV guardado en:\n"
        f"{ruta_csv}"
    )

    print(
        f"Gráfica guardada en:\n"
        f"{ruta_grafica}"
    )

    if (
        porcentaje_bajo > 1
        or porcentaje_alto > 1
    ):

        print(
            "\nADVERTENCIA: el segmento "
            "presenta recorte o saturación."
        )

        print(
            "Conviene revisar la conexión "
            "y repetir la adquisición."
        )


if __name__ == "__main__":
    main()