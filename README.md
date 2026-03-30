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

## ✅ Requisitos en Windows 11

Para que la aplicación funcione correctamente en Windows 11, se recomienda tener:

- **Windows 11** actualizado
- **Python 3.10+** instalado y disponible en PATH
- **Conexión a internet** (SpeechRecognition usa Google para transcripción)
- **Permisos de lectura/escritura** en la carpeta del proyecto (para `output/` y archivos temporales)

### Programas necesarios

1. **Python 3.10 o superior**
2. **pip** (normalmente viene con Python)
3. **Git** (para clonar y actualizar el proyecto)

### Programas opcionales recomendados

1. **FFmpeg global en PATH**: no es obligatorio en este proyecto porque se usa `imageio-ffmpeg`, pero puede ayudar en diagnóstico y conversión manual de audio.
2. **Visual Studio Code**: recomendado para desarrollo y depuración.

### Instalación rápida con winget (Windows 11)

Puedes instalar lo base con estos comandos en PowerShell:

```powershell
# Python 3.11
winget install -e --id Python.Python.3.11

# Git
winget install -e --id Git.Git
```

Opcionales recomendados:

```powershell
# Visual Studio Code
winget install -e --id Microsoft.VisualStudioCode

# FFmpeg (opcional)
winget install -e --id Gyan.FFmpeg
```

Si ya tienes alguno instalado, winget lo indicará y no duplicará la instalación.

### Verificación rápida

```bash
python --version
pip --version
git --version
```

Si estos comandos responden correctamente, el entorno base está listo.

### Verificación post-instalación (recomendada)

Ejecuta esta comprobación completa en PowerShell:

```powershell
winget --version
python --version
pip --version
git --version
ffmpeg -version
```

Interpretación:

1. Si `ffmpeg -version` falla, no es bloqueante para esta app, pero conviene instalarlo si haces conversiones manuales.
2. Si `python`, `pip` o `git` no responden, revisa la instalación o el PATH.
3. Si `winget` no responde, actualiza App Installer desde Microsoft Store.

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
