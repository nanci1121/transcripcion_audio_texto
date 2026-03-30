"""
Punto de entrada de la aplicación.
"""

import tkinter as tk
import sys
from pathlib import Path

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
