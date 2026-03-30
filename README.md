# 🎙️ Transcripción de Audio - Aplicación Desktop Windows 11

Aplicación de escritorio para Windows 11 que transcribe archivos de audio a texto. Arquitectura MVC limpia, código modular y bien estructurado.

---

## 🚀 Quick Start

### 1. Clonar el Repositorio
```bash
git clone <url-repositorio>
cd Transcripcion_Audio_Texto
```

### 2. Crear y Activar Entorno Virtual
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar en Desarrollo
```bash
python -m src.main
```

---

## 📁 Estructura del Proyecto

```
Transcripcion_Audio_Texto/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Punto de entrada
│   ├── models/                 # Lógica de negocio
│   │   ├── __init__.py
│   │   └── transcription.py
│   ├── views/                  # Interfaz gráfica (tkinter)
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   └── dialogs.py
│   ├── controllers/            # Orquestación
│   │   ├── __init__.py
│   │   └── app_controller.py
│   ├── utils/                  # Funciones auxiliares
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── validators.py
│   └── resources/              # Íconos, estilos
├── tests/                      # Tests unitarios
├── .github/
│   ├── agents/
│   │   └── windows-desktop-app.agent.md
│   └── copilot-instructions.md
├── .venv/                      # Entorno virtual (ignorado por git)
├── requirements.txt            # Dependencias
├── .gitignore
├── AGENTS.md                   # Documentación de agentes
└── README.md
```

---

## 🔧 Dependencias

- **Python**: 3.10+
- **tkinter**: Incluido con Python
- **SpeechRecognition**: Para transcripción
- **pytest**: Tests unitarios
- **PyInstaller**: Generar .exe

Ver `requirements.txt` para la lista completa.

---

## 📊 Arquitectura MVC

### Modelo (src/models/)
Lógica de negocio pura, sin dependencias de UI.

```python
class TranscriptionTask:
    def mark_completed(self, transcript: str) -> None:
        pass
```

### Vista (src/views/)
Interfaz gráfica con tkinter.

```python
class MainWindow:
    def set_transcribe(self, callback) -> None:
        pass
```

### Controlador (src/controllers/)
Orquesta interacciones entre Modelo y Vista.

```python
class AppController:
    def on_transcribe(self) -> None:
        pass
```

---

## 🧪 Tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src tests/
```

---

## 📦 Generar .exe

```bash
python build_exe.py
```

El ejecutable se generará en `dist/Transcriptor.exe`

---

## 🤝 Agentes de Copilot

Este proyecto incluye un agente **WindowsDesktopApp** especializado.

### Activación

Se activa automáticamente al trabajar en `src/**/*.py`

O menciona: "*Usa el agente WindowsDesktopApp*"

Ver [AGENTS.md](AGENTS.md) para más.

---

## 📝 Guía de Contribución

1. Sigue la arquitectura MVC
2. Type hints obligatorios
3. Funciones ≤ 20 líneas
4. Docstrings en clases/funciones públicas
5. Tests para lógica crítica
6. Sin valores hardcodeados

Ver `.github/copilot-instructions.md` para más detalles.

---

## 📄 Licencia

MIT
