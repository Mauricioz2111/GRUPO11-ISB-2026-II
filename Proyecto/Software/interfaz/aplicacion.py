from datetime import datetime
import random
import time
import unicodedata

import numpy as np
import streamlit as st
import streamlit.components.v1 as components

import json
import os
import subprocess
from pathlib import Path

st.set_page_config(
    page_title="EOG-Adapta",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# Configuración del prototipo
# -----------------------------------------------------------------------------
UMBRAL_CONFIANZA = 0.65
COLUMNAS = 3
INTERVALO_SEGURIDAD_REAL_S = 0.60

CARPETA_INFERENCIA = Path(__file__).resolve().parent / "inferencia_edge_impulse"
RUTA_EJECUTABLE = CARPETA_INFERENCIA / "build" / "app.exe"

OPCIONES = [
    {"icono": "💧", "titulo": "Agua", "mensaje": "Quiero tomar agua"},
    {"icono": "🍽️", "titulo": "Comida", "mensaje": "Tengo hambre"},
    {"icono": "🚻", "titulo": "Baño", "mensaje": "Necesito ir al baño"},
    {"icono": "🩺", "titulo": "Dolor", "mensaje": "Siento dolor"},
    {"icono": "🛏️", "titulo": "Descanso", "mensaje": "Quiero descansar"},
    {"icono": "🤝", "titulo": "Compañía", "mensaje": "Quiero estar acompañado"},
]

NOMBRES_MOVIMIENTOS = {
    "izquierda": "Mirada a la izquierda",
    "derecha": "Mirada a la derecha",
    "arriba": "Mirada hacia arriba",
    "abajo": "Mirada hacia abajo",
    "cejas": "Elevación de cejas",
    "pestaneo1": "Un pestañeo",
    "pestaneo2": "Dos pestañeos",
    "pestaneo3": "Tres pestañeos",
    "reposo": "Reposo",
}

ESTADO_INICIAL = {
    # Comenzar en una tarjeta central reduce el recorrido máximo.
    "indice": 1,
    "sistema_activo": True,
    "ultimo_movimiento": None,
    "ultima_confianza": None,
    "mensaje": "Seleccione una necesidad",
    "resultado": "esperando",
    "alerta_ayuda": False,
    "historial": [],
    "puntaje": 0,
    "intentos": 0,
    "objetivo": random.choice(list(NOMBRES_MOVIMIENTOS.keys())[:-1]),
    "demo_confidence": 0.95,
    "ultimo_comando_tiempo": 0.0,
    "latencia_modelo_ms": None,
    "ultima_muestra": None,
    "estado_procesamiento": "Esperando una señal",
}

for clave, valor in ESTADO_INICIAL.items():
    if clave not in st.session_state:
        st.session_state[clave] = valor


# -----------------------------------------------------------------------------
# Estilos
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --fondo: #061522;
        --panel: #102b3e;
        --panel-2: #15384a;
        --turquesa: #21e6c1;
        --texto: #f7fbff;
        --secundario: #b9d4e5;
        --borde: #31566c;
        --verde: #24d17e;
        --rojo: #ff4b61;
        --amarillo: #ffc94a;
    }

    .stApp { background: var(--fondo); }
    [data-testid="stSidebar"] { min-width: 260px; max-width: 260px; }
    [data-testid="stSidebar"] > div:first-child { background: #181915; }
    .block-container { max-width: 1500px; padding-top: 2rem; padding-bottom: 2rem; }

    h1, h2, h3, p, label, [data-testid="stMetricValue"] { color: var(--texto); }
    .subtitulo { color: #8fc9ef; margin-top: -0.8rem; margin-bottom: 1.4rem; }

    .estado-linea {
        padding: .75rem 1rem;
        border-radius: .65rem;
        font-weight: 700;
        margin-bottom: .7rem;
    }
    .activo { background: rgba(36, 209, 126, .18); color: #64f2ad; }
    .pausado { background: rgba(255, 75, 97, .18); color: #ff8796; }
    .modo { background: rgba(255, 201, 74, .13); color: #ffd96e; }

    [data-testid="stMetric"] {
        background: var(--panel);
        border: 1px solid var(--borde);
        padding: .75rem 1rem;
        border-radius: .75rem;
        min-height: 105px;
    }
    [data-testid="stMetricLabel"] { color: var(--secundario); }

    .tarjeta {
        min-height: 168px;
        background: var(--panel);
        border: 2px solid var(--borde);
        border-radius: 16px;
        padding: 1.2rem .8rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        transition: .2s ease;
    }
    .tarjeta.seleccionada {
        background: #154d55;
        border: 4px solid var(--turquesa);
        box-shadow: 0 0 18px rgba(33, 230, 193, .22);
    }
    .icono { font-size: 2.8rem; line-height: 1; margin-bottom: .7rem; }
    .titulo-tarjeta { color: white; font-size: 1.35rem; font-weight: 800; }
    .mensaje-tarjeta { color: #c2e9ff; font-size: .95rem; margin-top: .35rem; }

    .mensaje-principal {
        border-left: 7px solid var(--turquesa);
        background: #124655;
        color: white;
        border-radius: 12px;
        padding: 1.35rem 1.5rem;
        font-size: 1.45rem;
        font-weight: 800;
        margin: .5rem 0 1rem;
    }
    .mensaje-confirmado { border-left-color: var(--verde); background: #123f32; }
    .mensaje-cancelado { border-left-color: var(--rojo); background: #48242b; }

    .ayuda {
        background: #7b1827;
        border: 2px solid #ff6277;
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        font-size: 1.35rem;
        font-weight: 900;
        text-align: center;
        animation: pulso 1.2s infinite;
    }
    @keyframes pulso { 50% { opacity: .72; } }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        min-height: 44px;
        font-weight: 700;
        white-space: normal;
    }
    .nota { color: #89a8bb; font-size: .84rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Lógica de control
# -----------------------------------------------------------------------------
def normalizar_etiqueta(etiqueta: str) -> str:
    """Uniformiza etiquetas como pestañeo1, pestaneo1 o pesta_eo1."""
    texto = unicodedata.normalize("NFKD", str(etiqueta).lower())
    texto = "".join(caracter for caracter in texto if not unicodedata.combining(caracter))
    texto = texto.replace("_", "").replace("-", "").replace(" ", "")

    alias = {
        "pestaeo1": "pestaneo1",
        "pestaneo1": "pestaneo1",
        "pestaeo2": "pestaneo2",
        "pestaneo2": "pestaneo2",
        "pestaeo3": "pestaneo3",
        "pestaneo3": "pestaneo3",
    }
    return alias.get(texto, texto)


def registrar_evento(resultado: str, movimiento: str, confianza: float) -> None:
    st.session_state.historial.insert(
        0,
        {
            "Hora": datetime.now().strftime("%H:%M:%S"),
            "Movimiento": NOMBRES_MOVIMIENTOS.get(movimiento, movimiento),
            "Confianza": f"{confianza * 100:.1f}%",
            "Resultado": resultado,
        },
    )
    st.session_state.historial = st.session_state.historial[:30]


def mover_seleccion(movimiento: str) -> None:
    fila, columna = divmod(st.session_state.indice, COLUMNAS)
    filas = (len(OPCIONES) + COLUMNAS - 1) // COLUMNAS

    if movimiento == "izquierda":
        columna = (columna - 1) % COLUMNAS
    elif movimiento == "derecha":
        columna = (columna + 1) % COLUMNAS
    elif movimiento == "arriba":
        fila = (fila - 1) % filas
    elif movimiento == "abajo":
        fila = (fila + 1) % filas

    nuevo_indice = fila * COLUMNAS + columna
    if nuevo_indice < len(OPCIONES):
        st.session_state.indice = nuevo_indice


def procesar_movimiento(
    movimiento: str,
    confianza: float,
    origen: str = "real",
) -> None:
    movimiento = normalizar_etiqueta(movimiento)
    st.session_state.ultimo_movimiento = movimiento
    st.session_state.ultima_confianza = confianza

    ahora = time.monotonic()

    if movimiento not in NOMBRES_MOVIMIENTOS:
        st.session_state.estado_procesamiento = (
            f"Etiqueta desconocida ({movimiento}): no se ejecutó ninguna acción"
        )
        registrar_evento("Ignorado: etiqueta desconocida", movimiento, confianza)
        return

    # Reposo no desplaza la interfaz.
    if movimiento == "reposo":
        st.session_state.estado_procesamiento = "Sistema preparado para el siguiente comando"
        registrar_evento("Sin acción", movimiento, confianza)
        return

    # La ayuda y la reactivación permanecen disponibles aunque el sistema esté pausado.
    if not st.session_state.sistema_activo and movimiento not in {"cejas", "pestaneo3"}:
        registrar_evento("Ignorado: sistema pausado", movimiento, confianza)
        return

    if movimiento != "reposo" and confianza < UMBRAL_CONFIANZA:
        st.session_state.estado_procesamiento = "Señal no concluyente: no se ejecutó ninguna acción"
        registrar_evento("Ignorado: baja confianza", movimiento, confianza)
        return

    # En señal real evita dobles activaciones accidentales. En demostración cada
    # clic representa una orden independiente, aunque repita la dirección.
    if (
        origen == "real"
        and ahora - st.session_state.ultimo_comando_tiempo
        < INTERVALO_SEGURIDAD_REAL_S
    ):
        st.session_state.estado_procesamiento = "Comando bloqueado por intervalo de seguridad"
        registrar_evento("Ignorado: intervalo de seguridad", movimiento, confianza)
        return

    resultado = "Sin acción"
    if movimiento in {"izquierda", "derecha", "arriba", "abajo"}:
        mover_seleccion(movimiento)
        resultado = "Navegación"
    elif movimiento == "pestaneo1":
        opcion = OPCIONES[st.session_state.indice]
        st.session_state.mensaje = opcion["mensaje"]
        st.session_state.resultado = "confirmado"
        resultado = f"Confirmado: {opcion['titulo']}"
    elif movimiento == "pestaneo2":
        # Se conserva como clase del modelo, pero no se asigna a cancelar
        # para evitar confusiones entre cantidades de pestañeos.
        resultado = "Detectado: sin acción asignada"
    elif movimiento == "pestaneo3":
        st.session_state.alerta_ayuda = True
        st.session_state.mensaje = "Necesito ayuda inmediata"
        st.session_state.resultado = "cancelado"
        resultado = "Solicitud de ayuda"
    elif movimiento == "cejas":
        st.session_state.sistema_activo = not st.session_state.sistema_activo
        resultado = "Sistema reactivado" if st.session_state.sistema_activo else "Sistema pausado"

    st.session_state.ultimo_comando_tiempo = ahora
    st.session_state.estado_procesamiento = resultado
    registrar_evento(resultado, movimiento, confianza)


def seleccionar_manual(indice: int) -> None:
    st.session_state.indice = indice
    st.session_state.mensaje = (
        f"{OPCIONES[indice]['titulo']} seleccionado. Confirme para comunicar."
    )
    st.session_state.resultado = "esperando"


def cancelar() -> None:
    st.session_state.mensaje = "Selección cancelada"
    st.session_state.resultado = "cancelado"


def confirmar_manual() -> None:
    opcion = OPCIONES[st.session_state.indice]
    st.session_state.mensaje = opcion["mensaje"]
    st.session_state.resultado = "confirmado"


def obtener_muestras_disponibles() -> list[Path]:
    """Devuelve las muestras .txt disponibles para la demostración."""
    if not CARPETA_INFERENCIA.exists():
        return []
    return sorted(CARPETA_INFERENCIA.glob("*.txt"), key=lambda ruta: ruta.name.lower())


def leer_prediccion_real(muestra: Path):
    """Ejecuta el modelo local de Edge Impulse y devuelve etiqueta y confianza."""

    if not RUTA_EJECUTABLE.exists():
        st.error(f"No se encontró el modelo: {RUTA_EJECUTABLE}")
        return None

    if not muestra.exists():
        st.error(f"No se encontró la muestra: {muestra}")
        return None

    try:
        inicio = time.perf_counter()
        entorno = os.environ.copy()
        entorno["PATH"] = (
            r"C:\msys64\ucrt64\bin;"
            + entorno.get("PATH", "")
        )

        proceso = subprocess.run(
            [str(RUTA_EJECUTABLE), str(muestra)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=True,
            env=entorno,
            creationflags=(
                subprocess.CREATE_NO_WINDOW
                if os.name == "nt"
                else 0
            ),
        )
        latencia_ms = (time.perf_counter() - inicio) * 1000

        lineas = [
            linea.strip()
            for linea in proceso.stdout.splitlines()
            if linea.strip()
        ]

        resultado = json.loads(lineas[-1])

        etiqueta = normalizar_etiqueta(resultado["label"])
        confianza = float(resultado["confidence"])

        return etiqueta, confianza, latencia_ms

    except Exception as error:
        st.error(f"Error al ejecutar Edge Impulse: {error}")
        return None


def reproducir_mensaje(texto: str) -> None:
    texto_seguro = texto.replace("\\", "\\\\").replace("'", "\\'")
    components.html(
        f"""
        <script>
        const voz = new SpeechSynthesisUtterance('{texto_seguro}');
        voz.lang = 'es-PE';
        voz.rate = 0.9;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(voz);
        </script>
        """,
        height=0,
    )


# -----------------------------------------------------------------------------
# Barra lateral
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 👁️ EOG-Adapta")
    modulo = st.radio("Módulo", ["Comunicación", "Entrenamiento", "Monitoreo"])
    st.divider()

    modo = st.selectbox("Modo de funcionamiento", ["Demostración", "Señal real", "Calibración"])

    clase_estado = "activo" if st.session_state.sistema_activo else "pausado"
    texto_estado = "● SISTEMA ACTIVO" if st.session_state.sistema_activo else "⏸ SISTEMA PAUSADO"
    st.markdown(f'<div class="estado-linea {clase_estado}">{texto_estado}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="estado-linea modo">Modo: {modo}</div>', unsafe_allow_html=True)
    st.caption(
        f"Umbral de aceptación: {UMBRAL_CONFIANZA * 100:.0f}%. "
        "Una predicción menor no ejecuta acciones."
    )

    if modo == "Demostración":
        confianza_demo = st.slider(
            "Confianza simulada",
            min_value=0.50,
            max_value=1.00,
            step=0.01,
            key="demo_confidence",
        )
        st.markdown("### Control EOG simulado")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("⬅ Izquierda"):
                procesar_movimiento("izquierda", confianza_demo, origen="demo")
            if st.button("⬆ Arriba"):
                procesar_movimiento("arriba", confianza_demo, origen="demo")
        with c2:
            if st.button("➡ Derecha"):
                procesar_movimiento("derecha", confianza_demo, origen="demo")
            if st.button("⬇ Abajo"):
                procesar_movimiento("abajo", confianza_demo, origen="demo")

        if st.button("🤨 Cejas — Pausar/reactivar"):
            procesar_movimiento("cejas", confianza_demo, origen="demo")
        if st.button("😉 Pestañeo 1 — Confirmar"):
            procesar_movimiento("pestaneo1", confianza_demo, origen="demo")
        if st.button("😉😉 Pestañeo 2 — Sin acción"):
            procesar_movimiento("pestaneo2", confianza_demo, origen="demo")
        if st.button("🆘 Pestañeo 3 — Ayuda", type="primary"):
            procesar_movimiento("pestaneo3", confianza_demo, origen="demo")
        if st.button("⚪ Reposo"):
            procesar_movimiento("reposo", 1.0, origen="demo")

    elif modo == "Señal real":
        muestras_disponibles = obtener_muestras_disponibles()

        if RUTA_EJECUTABLE.exists():
            st.success("Modelo de Edge Impulse disponible.")
        else:
            st.error("No se encontró build/app.exe.")

        st.caption(
            "Esta prueba utiliza una muestra EOG real pregrabada. "
            "La adquisición continua por BITalino queda como siguiente etapa."
        )

        muestra_seleccionada = None
        if muestras_disponibles:
            muestra_seleccionada = st.selectbox(
                "Muestra EOG",
                options=muestras_disponibles,
                format_func=lambda ruta: ruta.name,
            )
        else:
            st.warning("No se encontraron muestras .txt.")

        puede_predecir = RUTA_EJECUTABLE.exists() and muestra_seleccionada is not None
        if st.button("Leer una predicción", disabled=not puede_predecir):
            prediccion = leer_prediccion_real(muestra_seleccionada)
            if prediccion is None:
                st.warning("No se pudo procesar la muestra seleccionada.")
            else:
                etiqueta, confianza, latencia_ms = prediccion
                st.session_state.latencia_modelo_ms = latencia_ms
                st.session_state.ultima_muestra = muestra_seleccionada.name
                procesar_movimiento(etiqueta, confianza, origen="real")

    else:
        st.info("Realice cada movimiento cuando lo solicite el evaluador.")
        progreso = st.slider("Progreso de calibración", 0, 9, 0)
        st.progress(progreso / 9)


# -----------------------------------------------------------------------------
# Encabezado y estado
# -----------------------------------------------------------------------------
st.title("EOG-Adapta")
st.markdown(
    '<p class="subtitulo">Sistema interactivo de comunicación y entrenamiento controlado mediante señales electrooculográficas</p>',
    unsafe_allow_html=True,
)

movimiento_mostrado = (
    NOMBRES_MOVIMIENTOS.get(st.session_state.ultimo_movimiento, "Esperando señal")
    if st.session_state.ultimo_movimiento
    else "Esperando señal"
)
confianza_mostrada = (
    f"{st.session_state.ultima_confianza * 100:.1f}%"
    if st.session_state.ultima_confianza is not None
    else "—"
)

m1, m2, m3, m4 = st.columns([1, 1.2, 1, 1.1])
m1.metric("Estado", "ACTIVO" if st.session_state.sistema_activo else "PAUSADO")
m2.metric("Movimiento detectado", movimiento_mostrado)
m3.metric("Confianza", confianza_mostrada)
m4.metric("Entrada", "Simulación" if modo == "Demostración" else modo)

st.caption(st.session_state.estado_procesamiento)
if st.session_state.latencia_modelo_ms is not None:
    st.caption(
        f"Ejecución del modelo: {st.session_state.latencia_modelo_ms:.1f} ms. "
        "Este valor no incluye los aproximadamente 3 s de adquisición de la ventana."
    )
    if st.session_state.ultima_muestra:
        st.caption(f"Muestra procesada: {st.session_state.ultima_muestra}")

if st.session_state.alerta_ayuda:
    st.markdown('<div class="ayuda">🆘 SOLICITUD DE AYUDA ACTIVADA</div>', unsafe_allow_html=True)
    if st.button("Desactivar alerta de ayuda"):
        st.session_state.alerta_ayuda = False
        st.session_state.mensaje = "Seleccione una necesidad"
        st.session_state.resultado = "esperando"
        st.rerun()


# -----------------------------------------------------------------------------
# Módulos
# -----------------------------------------------------------------------------
if modulo == "Comunicación":
    st.header("Panel de comunicación")
    st.caption(
        "Utilice izquierda, derecha, arriba y abajo para navegar. "
        "Un pestañeo confirma y tres solicitan ayuda. "
        "La navegación es circular para reducir el recorrido."
    )

    for inicio in range(0, len(OPCIONES), COLUMNAS):
        columnas = st.columns(COLUMNAS)
        for desplazamiento, columna in enumerate(columnas):
            indice = inicio + desplazamiento
            if indice >= len(OPCIONES):
                continue
            opcion = OPCIONES[indice]
            seleccionada = indice == st.session_state.indice
            clase = "tarjeta seleccionada" if seleccionada else "tarjeta"
            with columna:
                tarjeta_html = (
                    f'<div class="{clase}">'
                    f'<div class="icono">{opcion["icono"]}</div>'
                    f'<div class="titulo-tarjeta">{opcion["titulo"]}</div>'
                    f'<div class="mensaje-tarjeta">{opcion["mensaje"]}</div>'
                    f'</div>'
                )
                st.markdown(
                    tarjeta_html,
                    unsafe_allow_html=True,
                )
                if modo == "Demostración":
                    st.button(
                        "Seleccionar manualmente",
                        key=f"seleccionar_{indice}",
                        on_click=seleccionar_manual,
                        args=(indice,),
                    )

    st.header("Mensaje comunicado")
    clase_mensaje = "mensaje-principal"
    if st.session_state.resultado == "confirmado":
        clase_mensaje += " mensaje-confirmado"
    elif st.session_state.resultado == "cancelado":
        clase_mensaje += " mensaje-cancelado"

    st.markdown(
        f'<div class="{clase_mensaje}">{st.session_state.mensaje}</div>',
        unsafe_allow_html=True,
    )

    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("🔊 Reproducir mensaje"):
            reproducir_mensaje(st.session_state.mensaje)
    with a2:
        if st.button("✅ Confirmar manualmente"):
            confirmar_manual()
            st.rerun()
    with a3:
        if st.button("❌ Cancelar"):
            cancelar()
            st.rerun()


elif modulo == "Entrenamiento":
    st.header("Entrenamiento de movimientos EOG")
    st.write("Realice el movimiento indicado y luego selecciónelo en el panel de demostración.")

    objetivo = st.session_state.objetivo
    st.info(f"Movimiento objetivo: **{NOMBRES_MOVIMIENTOS[objetivo]}**")

    elegido = st.selectbox("Movimiento realizado", list(NOMBRES_MOVIMIENTOS.keys()), format_func=NOMBRES_MOVIMIENTOS.get)
    if st.button("Evaluar intento", type="primary"):
        st.session_state.intentos += 1
        if elegido == objetivo:
            st.session_state.puntaje += 1
            st.success("Movimiento correcto")
        else:
            st.error(f"Se esperaba: {NOMBRES_MOVIMIENTOS[objetivo]}")
        st.session_state.objetivo = random.choice(list(NOMBRES_MOVIMIENTOS.keys())[:-1])

    e1, e2 = st.columns(2)
    e1.metric("Aciertos", st.session_state.puntaje)
    e2.metric("Intentos", st.session_state.intentos)


else:
    st.header("Monitoreo del sistema")
    st.caption("La gráfica es demostrativa hasta conectar la adquisición real del BITalino.")

    tiempo = np.linspace(0, 3, 600)
    ruido = np.random.default_rng(7).normal(0, 0.035, len(tiempo))
    senal = 0.08 * np.sin(2 * np.pi * 1.5 * tiempo) + ruido
    st.line_chart(senal, height=280)

    s1, s2, s3 = st.columns(3)
    s1.metric("BITalino", "Pendiente" if modo != "Señal real" else "Sin conexión")
    s2.metric("Modelo", "Disponible" if RUTA_EJECUTABLE.exists() else "No encontrado")
    s3.metric("Calidad de señal", "Sin evaluar")

    st.subheader("Historial de eventos")
    if st.session_state.historial:
        st.dataframe(st.session_state.historial, use_container_width=True, hide_index=True)
    else:
        st.info("Todavía no se han registrado movimientos.")


st.divider()
st.markdown(
    '<p class="nota">EOG-Adapta — Prototipo académico para asistencia comunicativa. '
    'No debe utilizarse como único medio para comunicar una emergencia médica.</p>',
    unsafe_allow_html=True,
)

