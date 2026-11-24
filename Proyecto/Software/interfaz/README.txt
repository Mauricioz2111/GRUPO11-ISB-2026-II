EOG-ADAPTA — APLICACIÓN DE ESCRITORIO

ARCHIVOS
  aplicacion.py            Interfaz Streamlit.
  launcher.py              Abre la interfaz como ventana de escritorio.
  instalar_escritorio.ps1  Instala dependencias y crea el acceso directo.
  iniciar_EOG_Adapta.bat   Inicio alternativo mediante doble clic.
  requirements.txt         Dependencias del proyecto.

INSTALACIÓN (SOLO UNA VEZ)

1. Copia todos los archivos dentro de:
   Proyecto\Software\interfaz

2. Abre PowerShell en esa carpeta.

3. Ejecuta:
   powershell -ExecutionPolicy Bypass -File .\instalar_escritorio.ps1

4. Aparecerá un acceso directo llamado EOG-Adapta en el escritorio.

USO DIARIO

Haz doble clic en el acceso directo EOG-Adapta. La aplicación abrirá una
ventana independiente, sin pestañas ni barra de direcciones de Chrome.
Al cerrar la ventana también se detiene el servidor local.

Si no deseas crear el acceso directo, también puedes ejecutar con doble clic:
   iniciar_EOG_Adapta.bat

NOTA

El modo Demostración funciona completamente. El modo Señal real contiene el
punto de integración leer_prediccion_real(), pero todavía necesita el modelo
exportado de Edge Impulse y el código de adquisición del BITalino.

