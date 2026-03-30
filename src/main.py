"""
Punto de entrada de la aplicación.
"""

import tkinter as tk
import sys
import warnings
from pathlib import Path

# Suprimir warning inofensivo de pydub sobre ffmpeg en PATH
# (la app usa imageio-ffmpeg, no el ffmpeg del sistema)
warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub")

# Agregar el directorio raíz al path para los imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.views.main_window import MainWindow
from src.controllers.app_controller import AppController

def main() -> None:
    """Función principal que inicia la aplicación."""
    root = tk.Tk()
    view = MainWindow(root)
    controller = AppController(view)
    view.run()

if __name__ == "__main__":
    main()
