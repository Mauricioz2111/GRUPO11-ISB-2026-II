from datetime import datetime
import random

import numpy as np
import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="EOG-Adapta",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# -----------------------------------------------------------------------------
# Configuración del prototipo
# -----------------------------------------------------------------------------
UMBRAL_CONFIANZA = 0.80
COLUMNAS = 3

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
    "indice": 0,
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


def procesar_movimiento(movimiento: str, confianza: float) -> None:
    st.session_state.ultimo_movimiento = movimiento
    st.session_state.ultima_confianza = confianza

    # La ayuda y la reactivación permanecen disponibles aunque el sistema esté pausado.
    if not st.session_state.sistema_activo and movimiento not in {"cejas", "pestaneo3"}:
        registrar_evento("Ignorado: sistema pausado", movimiento, confianza)
        return

    if movimiento != "reposo" and confianza < UMBRAL_CONFIANZA:
        registrar_evento("Ignorado: baja confianza", movimiento, confianza)
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
        st.session_state.mensaje = "Selección cancelada"
        st.session_state.resultado = "cancelado"
        resultado = "Cancelado"
    elif movimiento == "pestaneo3":
        st.session_state.alerta_ayuda = True
        st.session_state.mensaje = "Necesito ayuda inmediata"
        st.session_state.resultado = "cancelado"
        resultado = "Solicitud de ayuda"
    elif movimiento == "cejas":
        st.session_state.sistema_activo = not st.session_state.sistema_activo
        resultado = "Sistema reactivado" if st.session_state.sistema_activo else "Sistema pausado"

    registrar_evento(resultado, movimiento, confianza)


def seleccionar_manual(indice: int) -> None:
    st.session_state.indice = indice
    st.session_state.mensaje = OPCIONES[indice]["mensaje"]
    st.session_state.resultado = "esperando"


def cancelar() -> None:
    st.session_state.mensaje = "Selección cancelada"
    st.session_state.resultado = "cancelado"


def confirmar_manual() -> None:
    opcion = OPCIONES[st.session_state.indice]
    st.session_state.mensaje = opcion["mensaje"]
    st.session_state.resultado = "confirmado"


def leer_prediccion_real():
    """Punto de conexión para BITalino + Edge Impulse.

    Debe devolver una tupla (etiqueta, confianza), por ejemplo:
        return "derecha", 0.91

    Mientras no esté conectado el modelo exportado, devuelve None.
    """
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
                procesar_movimiento("izquierda", confianza_demo)
            if st.button("⬆ Arriba"):
                procesar_movimiento("arriba", confianza_demo)
        with c2:
            if st.button("➡ Derecha"):
                procesar_movimiento("derecha", confianza_demo)
            if st.button("⬇ Abajo"):
                procesar_movimiento("abajo", confianza_demo)

        if st.button("🤨 Cejas — Pausar/reactivar"):
            procesar_movimiento("cejas", confianza_demo)
        if st.button("😉 Pestañeo 1 — Confirmar"):
            procesar_movimiento("pestaneo1", confianza_demo)
        if st.button("😉😉 Pestañeo 2 — Cancelar"):
            procesar_movimiento("pestaneo2", confianza_demo)
        if st.button("🆘 Pestañeo 3 — Ayuda", type="primary"):
            procesar_movimiento("pestaneo3", confianza_demo)
        if st.button("⚪ Reposo"):
            procesar_movimiento("reposo", 1.0)

    elif modo == "Señal real":
        st.info("Conector preparado. Falta incorporar el modelo exportado y la adquisición BITalino.")
        if st.button("Leer una predicción"):
            prediccion = leer_prediccion_real()
            if prediccion is None:
                st.warning("Todavía no existe una fuente EOG conectada.")
            else:
                procesar_movimiento(*prediccion)

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
        "Un pestañeo confirma, dos cancelan y tres solicitan ayuda."
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
                st.markdown(
                    f"""
                    <div class="{clase}">
                        <div class="icono">{opcion['icono']}</div>
                        <div class="titulo-tarjeta">{opcion['titulo']}</div>
                        <div class="mensaje-tarjeta">{opcion['mensaje']}</div>
                    </div>
                    """,
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
    s2.metric("Modelo", "Interfaz preparada")
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

