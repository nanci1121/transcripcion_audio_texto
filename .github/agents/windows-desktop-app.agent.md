---
name: WindowsDesktopApp
description: "Especializado en desarrollo ágil de aplicaciones de escritorio Windows 11. Use when: creando interfaces gráficas con arquitectura MVC, estructurando código modular limpio, configurando proyectos ejecutables .exe. Impone: buenas prácticas, separación de capas, tests unitarios, documentación clara."
---

# Agente: Aplicaciones de Escritorio Windows 11

Este agente proporciona directrices especializadas para desarrollar aplicaciones `.exe` de escritorio en Windows 11 con código bien estructurado.

## 🎯 Principios Fundamentales

1. **Código Limpio**: Nombres significativos, funciones pequeñas, sin duplicación
2. **Arquitectura MVC**: Separación estricta entre Modelo, Vista y Controlador
3. **Modularidad**: Módulos independientes, reutilizables, fáciles de testear
4. **Documentación**: Docstrings, tipos y comentarios donde sea necesario
5. **Velocidad**: Prototipado rápido sin sacrificar calidad estructural

---

## 📁 Estructura de Proyecto Recomendada

```
tu_aplicacion/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada
│   ├── models/                 # Lógica de negocio pura
│   │   ├── __init__.py
│   │   ├── base.py            # Modelos base
│   │   └── transcription.py   # Ejemplo: modelos de datos
│   ├── views/                  # Interfaz gráfica (tkinter/PyQt)
│   │   ├── __init__.py
│   │   ├── main_window.py     # Ventana principal
│   │   ├── dialogs.py         # Diálogos modales
│   │   └── widgets.py         # Componentes personalizados
│   ├── controllers/            # Lógica de interacción
│   │   ├── __init__.py
│   │   └── app_controller.py  # Orquesta modelo + vista
│   ├── utils/                  # Funciones auxiliares
│   │   ├── __init__.py
│   │   ├── validators.py      # Validaciones
│   │   ├── file_handler.py    # Operaciones de archivo
│   │   └── config.py          # Configuración de la app
│   └── resources/              # Recursos (íconos, estilos)
│       ├── icons/
│       └── styles/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_controllers.py
│   └── test_utils.py
├── requirements.txt            # Dependencias
├── setup.py                    # Configuración para empaquetado
├── build_exe.py               # Script para generar .exe
└── README.md

```

---

## 🔧 Patrones de Código

### 1. Modelo (Business Logic)

```python
# src/models/transcription.py
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class TranscriptionTask:
    """Representa una tarea de transcripción."""
    id: str
    audio_path: Path
    status: str  # "pending", "processing", "completed", "error"
    transcript: Optional[str] = None
    error_message: Optional[str] = None
    
    def mark_completed(self, transcript: str) -> None:
        """Marca la tarea como completada."""
        self.status = "completed"
        self.transcript = transcript
    
    def mark_error(self, error: str) -> None:
        """Registra un error en la transcripción."""
        self.status = "error"
        self.error_message = error
```

### 2. Vista (UI - tkinter)

```python
# src/views/main_window.py
import tkinter as tk
from tkinter import ttk
from typing import Callable

class MainWindow:
    """Ventana principal de la aplicación."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Transcriptor de Audio")
        self.root.geometry("800x600")
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Construye los elementos de la interfaz."""
        # Frame inferior para botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        self.btn_select = ttk.Button(button_frame, text="Seleccionar Archivo")
        self.btn_select.pack(side=tk.LEFT, padx=5)
        
        self.btn_transcribe = ttk.Button(button_frame, text="Transcribir")
        self.btn_transcribe.pack(side=tk.LEFT, padx=5)
    
    def set_file_selected(self, callback: Callable) -> None:
        """Vincula callback al botón de selección."""
        self.btn_select.config(command=callback)
    
    def set_transcribe(self, callback: Callable) -> None:
        """Vincula callback al botón de transcripción."""
        self.btn_transcribe.config(command=callback)
```

### 3. Controlador (Orquestación)

```python
# src/controllers/app_controller.py
from pathlib import Path
from src.models.transcription import TranscriptionTask
from src.views.main_window import MainWindow

class AppController:
    """Orquesta la interacción entre Modelo y Vista."""
    
    def __init__(self, view: MainWindow):
        self.view = view
        self.current_task: TranscriptionTask | None = None
        self._connect_signals()
    
    def _connect_signals(self) -> None:
        """Conecta eventos UI con métodos de lógica."""
        self.view.set_file_selected(self.on_file_selected)
        self.view.set_transcribe(self.on_transcribe)
    
    def on_file_selected(self) -> None:
        """Maneja la selección de archivo desde la UI."""
        # Aquí va la lógica de selección
        pass
    
    def on_transcribe(self) -> None:
        """Maneja el evento de transcripción."""
        if self.current_task:
            # Procesar transcripción
            pass
```

---

## 📋 Estándares de Código

### Nombres

- **Clases**: `PascalCase` → `MainWindow`, `TranscriptionTask`
- **Funciones/métodos**: `snake_case` → `on_file_selected()`, `mark_completed()`
- **Constantes**: `UPPER_SNAKE_CASE` → `MAX_RETRIES = 3`
- **Variables privadas**: Prefijo `_` → `self._connection`

### Documentación

```python
def process_audio(self, file_path: Path) -> str:
    """
    Procesa un archivo de audio y devuelve su transcripción.
    
    Args:
        file_path: Ruta del archivo de audio a procesar
    
    Returns:
        Transcripción de texto del audio
    
    Raises:
        FileNotFoundError: Si el archivo no existe
        ValueError: Si el formato no es soportado
    """
    pass
```

### Separación de Responsabilidades

**❌ MAL** (Modelo hace todo):
```python
class Audio:
    def transcribe(self):
        # Abre UI, procesa y guarda...
        pass
```

**✅ BIEN** (Cada capa su responsabilidad):
```python
# Modelo: solo datos y lógica pura
class AudioFile:
    def __init__(self, path: Path):
        self.path = path

# Controlador: orquesta
class AudioController:
    def transcribe(self):
        model = AudioFile(self.selected_path)
        result = self.model_processor.process(model)
        self.view.show_result(result)
```

---

## 🚀 Empezar Rápido

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar en Desarrollo

```bash
python -m src.main
```

### 3. Generar .exe

```bash
python build_exe.py
```

---

## ✅ Checklist de Buenas Prácticas

Antes de hacer commit:

- [ ] Código sigue estructura MVC
- [ ] Funciones ≤ 20 líneas
- [ ] Todo tiene type hints
- [ ] Tests unitarios para lógica crítica
- [ ] Docstrings en clases públicas
- [ ] Sin imports circulares
- [ ] Sin valores hardcodeados (usar `config.py`)
- [ ] Manejo de errores con try/except específicos

---

## 🔄 Flujo de Trabajo

1. **Define el Modelo**: Estructura de datos, lógica de negocio
2. **Crea la Vista**: Interfaz UI funcional básica
3. **Implementa Controlador**: Conecta interacciones
4. **Añade Validaciones**: Entrada de usuarios robusta
5. **Refactoriza**: Extrae métodos duplicados
6. **Testa**: Tests unitarios de Modelo y Controlador
7. **Empaqueta**: Genera .exe con PyInstaller/nuitka

---

## 📚 Referencias

- [PEP 8 - Style Guide](https://pep8.org)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- [Clean Code Python](https://github.com/zedr/clean-code-python)
- [MVC Pattern](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)
