# 📁 Estructura Completa del Proyecto

```
Transcripcion_Audio_Texto/
│
├── .github/                          # Configuración de GitHub
│   ├── agents/                       # Agentes especializados de Copilot
│   │   ├── windows-desktop-app.agent.md
│   │   ├── backend-developer.agent.md
│   │   ├── frontend-developer.agent.md
│   │   ├── ux-designer.agent.md
│   │   ├── qa-engineer.agent.md
│   │   └── project-manager.agent.md
│   ├── copilot-instructions.md       # Instrucciones automáticas para src/**/*.py
│   └── AGENTS_QUICK_REFERENCE.md     # Referencia rápida de agentes
│
├── src/                              # Código principal
│   ├── __init__.py
│   ├── main.py                       # 🔴 Punto de entrada
│   │
│   ├── models/                       # 📊 CAPA MODELO (Lógica de negocio)
│   │   ├── __init__.py
│   │   └── transcription.py          # Clase TranscriptionTask
│   │
│   ├── views/                        # 🎨 CAPA VISTA (Interfaz gráfica)
│   │   ├── __init__.py
│   │   ├── main_window.py            # Ventana principal (tkinter)
│   │   ├── dialogs.py                # Diálogos modales
│   │   └── styles/                   # (futuro) Temas y estilos
│   │
│   ├── controllers/                  # 🔗 CAPA CONTROLADOR (Orquestación)
│   │   ├── __init__.py
│   │   └── app_controller.py         # Controlador principal
│   │
│   ├── utils/                        # 🛠️ UTILIDADES
│   │   ├── __init__.py
│   │   ├── config.py                 # ⚙️ Configuración centralizada
│   │   └── validators.py             # ✅ Validaciones de entrada
│   │
│   └── resources/                    # 📦 RECURSOS
│       ├── __init__.py
│       ├── icons/                    # 🎯 Iconos de la aplicación
│       └── styles/                   # 🎨 Temas y CSS (si aplica)
│
├── tests/                            # 🧪 TESTS UNITARIOS
│   ├── __init__.py
│   ├── test_models.py                # Tests del modelo
│   ├── test_controllers.py           # (futuro) Tests del controlador
│   ├── test_utils.py                 # (futuro) Tests de utilidades
│   └── fixtures/                     # Datos de prueba
│       └── sample.mp3                # Archivo de prueba
│
├── .venv/                            # 🐍 Entorno virtual (ignorado en git)
│   ├── Scripts/
│   │   └── activate                  # Activar: .venv\Scripts\activate
│   └── Lib/
│       └── site-packages/
│
├── audio_files/                      # 📁 Archivos de entrada (creado en runtime)
├── output/                           # 📤 Archivos de salida (creado en runtime)
│
├── build/                            # (generado) Construcción PyInstaller
├── dist/                             # (generado) Ejecutable .exe
│
├── .gitignore                        # 🚫 Archivos ignorados por git
├── requirements.txt                  # 📦 Dependencias del proyecto
├── setup.py                          # 🔧 Configuración de distribución
├── build_exe.py                      # 📦 Script para generar .exe
│
├── README.md                         # 📖 Documentación principal
├── AGENTS.md                         # 🤖 Documentación de agentes (5 especializados)
├── ROADMAP.md                        # (futuro) Mapa de ruta del proyecto
├── CHANGELOG.md                      # (futuro) Historial de cambios
│
└── transcribir_reuniones.py          # (heredado) Archivo original
```

---

## 🎯 Convenciones de Nombres

### Archivos y Carpetas

```
✓ snake_case para carpetas: src/, audio_files/
✓ snake_case para archivos Python: transcription.py, app_controller.py
✓ UPPER_CASE para constantes: MAX_FILE_SIZE_MB, SUPPORTED_FORMATS
```

### Clases

```
✓ PascalCase: TranscriptionTask, MainWindow, AppController
✓ Herencia clara: BaseModel, AbstractService
```

### Funciones y Métodos

```
✓ snake_case: mark_completed(), on_file_selected(), is_valid_audio_file()
✓ Métodos privados con _: _setup_ui(), _notify_listeners()
✓ Booleans con is_/has_: is_completed(), has_error()
```

---

## 📊 Arquitectura en Capas

```
┌──────────────────────────────────────┐
│         VISTA (views/)               │
│    tkinter Interface MainWindow      │
│    - Botones, eventos, UI            │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│   CONTROLADOR (controllers/)          │
│    AppController (Orquestación)      │
│    - Lógica de flujo                 │
│    - Validación de entrada           │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│    MODELO (models/)                  │
│    TranscriptionTask (Negocio)       │
│    - Estados, transiciones           │
│    - Sin UI, sin dependencias         │
└──────────────┬───────────────────────┘
               │
┌──────────────▼───────────────────────┐
│  UTILIDADES (utils/)                 │
│  - config.py (configuración)         │
│  - validators.py (validaciones)      │
└──────────────────────────────────────┘
```

---

## 🔀 Flujo de Datos (Ejemplo: Seleccionar Archivo)

```
1. Usuario hace clic en "Seleccionar"
   └─> View.btn_select.click()

2. Vista abre diálogo de selección
   └─> View._handle_file_selection()

3. Usuario elige archivo.mp3
   └─> callback(Path("archivo.mp3"))

4. Controlador valida entrada
   └─> Controller.on_file_selected(file_path)

5. Controlador crea Modelo
   └─> Model = TranscriptionTask(id=..., audio_path=file_path)

6. Controlador actualiza Vista
   └─> View.set_file_label("📁 archivo.mp3")
   └─> View.set_status("Archivo cargado")
```

---

## 🔄 Ciclo de Vida de la Aplicación

```
START
  ↓
main_window = MainWindow(root)
  ↓
app_controller = AppController(main_window)
  ↓
Config.create_directories()
  ↓
main_window.run()  ← Inicia tkinter event loop
  ↓
[Esperando eventos de usuario]
  ├─ on_file_selected()
  ├─ on_transcribe()
  ├─ on_export()
  └─ on_clear()
  ↓
Usuario cierra ventana
  ↓
END
```

---

## 📦 Que Contiene Cada Carpeta

| Carpeta | Contenido | Responsable | Tests |
|---------|-----------|------------|-------|
| `src/models/` | Lógica de negocio pura | Backend | ✅ test_models.py |
| `src/views/` | Interfaz gráfica tkinter | Frontend | ⏳ test_views.py |
| `src/controllers/` | Orquestación MVC | Desktop/Backend | ⏳ test_controllers.py |
| `src/utils/` | Configuración, validadores | Desktop/Backend | ⏳ test_utils.py |
| `src/resources/` | Iconos, estilos, temas | UX/Frontend | - |
| `tests/` | Tests unitarios | QA | - |

---

## 🚀 Para Empezar

### 1. Activar Entorno Virtual
```bash
.venv\Scripts\activate
```

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar Aplicación
```bash
python -m src.main
```

### 4. Ejecutar Tests
```bash
pytest tests/ -v
```

### 5. Generar Ejecutable
```bash
python build_exe.py
```

---

## 📝 Checklist de Nuevas Características

Cuando implementes una nueva característica:

- [ ] Crea modelo en `src/models/` (sin UI)
- [ ] Crea vista en `src/views/` (solo UI)
- [ ] Agrega lógica en controlador `src/controllers/app_controller.py`
- [ ] Escribe test unitario en `tests/`
- [ ] Valida entrada con `src/utils/validators.py`
- [ ] Usa configuración de `src/utils/config.py`
- [ ] Agrega docstring y type hints
- [ ] Runs tests: `pytest tests/`

---

*Última actualización: 30 de marzo de 2026*
