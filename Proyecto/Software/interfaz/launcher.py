"""Lanzador de escritorio para EOG-Adapta.

Inicia Streamlit de forma local y muestra la interfaz dentro de una ventana
nativa mediante WebView2. Al cerrar la ventana se detiene el servidor.
"""

from __future__ import annotations

import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

import webview


TITULO = "EOG-Adapta"
CARPETA = Path(__file__).resolve().parent
APLICACION = CARPETA / "aplicacion.py"


def mostrar_error(mensaje: str) -> None:
    try:
        import tkinter.messagebox as messagebox

        messagebox.showerror(TITULO, mensaje)
    except Exception:
        pass


def obtener_puerto_libre() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind(("127.0.0.1", 0))
        return int(servidor.getsockname()[1])


def esperar_streamlit(url_salud: str, proceso: subprocess.Popen, limite: float = 45.0) -> bool:
    inicio = time.monotonic()
    while time.monotonic() - inicio < limite:
        if proceso.poll() is not None:
            return False
        try:
            with urlopen(url_salud, timeout=1) as respuesta:
                if respuesta.status == 200:
                    return True
        except (URLError, TimeoutError, OSError):
            time.sleep(0.25)
    return False


def iniciar_servidor(puerto: int) -> subprocess.Popen:
    entorno = os.environ.copy()
    entorno["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"

    comando = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(APLICACION),
        "--server.headless=true",
        "--server.address=127.0.0.1",
        f"--server.port={puerto}",
        "--server.fileWatcherType=none",
        "--browser.gatherUsageStats=false",
    ]

    opciones = {
        "cwd": str(CARPETA),
        "env": entorno,
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
    }
    if os.name == "nt":
        opciones["creationflags"] = subprocess.CREATE_NO_WINDOW

    return subprocess.Popen(comando, **opciones)


def cerrar_servidor(proceso: subprocess.Popen | None) -> None:
    if proceso is None or proceso.poll() is not None:
        return
    proceso.terminate()
    try:
        proceso.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proceso.kill()


def main() -> None:
    if not APLICACION.exists():
        mostrar_error(f"No se encontró el archivo:\n{APLICACION}")
        return

    proceso = None
    try:
        puerto = obtener_puerto_libre()
        url = f"http://127.0.0.1:{puerto}"
        proceso = iniciar_servidor(puerto)

        if not esperar_streamlit(f"{url}/_stcore/health", proceso):
            mostrar_error(
                "No se pudo iniciar EOG-Adapta. Verifique que las dependencias "
                "estén instaladas mediante instalar_escritorio.ps1."
            )
            return

        webview.create_window(
            TITULO,
            url,
            width=1440,
            height=900,
            min_size=(1050, 700),
            background_color="#061522",
        )
        webview.start()
    except Exception as error:
        mostrar_error(f"Ocurrió un error al abrir EOG-Adapta:\n{error}")
    finally:
        cerrar_servidor(proceso)


if __name__ == "__main__":
    main()
