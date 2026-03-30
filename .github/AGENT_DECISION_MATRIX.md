# 🎯 Matriz de Decisión de Agentes

Use esta tabla para saber **cuál agente activar** basado en tu tarea actual.

---

## ¿Qué necesito hacer?

| Situación | Agente | Comando |
|-----------|--------|---------|
| Estructurar código con MVC | WindowsDesktopApp | `Usa el agente WindowsDesktopApp` |
| Crear un modelo o servicio | BackendDeveloper | `Usa el agente BackendDeveloper` |
| Hacer API o base de datos | BackendDeveloper | `Usa el agente BackendDeveloper` |
| Crear componente UI tkinter | FrontendDeveloper | `Usa el agente FrontendDeveloper` |
| Mejorar gestión de estado | FrontendDeveloper | `Usa el agente FrontendDeveloper` |
| Arreglar interactividad | FrontendDeveloper | `Usa el agente FrontendDeveloper` |
| Diseñar wireframe/prototipo | UXDesigner | `Usa el agente UXDesigner` |
| Revisar accesibilidad WCAG | UXDesigner | `Usa el agente UXDesigner` |
| Mejorar estética/diseño | UXDesigner | `Usa el agente UXDesigner` |
| Escribir tests unitarios | QAEngineer | `Usa el agente QAEngineer` |
| Revisar cobertura de código | QAEngineer | `Usa el agente QAEngineer` |
| Reportar o analizar bugs | QAEngineer | `Usa el agente QAEngineer` |
| Planificar sprint | ProjectManager | `Usa el agente ProjectManager` |
| Escribir user stories | ProjectManager | `Usa el agente ProjectManager` |
| Priorizar tareas (MoSCoW) | ProjectManager | `Usa el agente ProjectManager` |

---

## Por Archivo/Directorio

| Directorio | Agente Primario | Agentes Secundarios |
|-----------|-----------------|-------------------|
| `src/models/` | BackendDeveloper | WindowsDesktopApp |
| `src/controllers/` | WindowsDesktopApp | BackendDeveloper, FrontendDeveloper |
| `src/views/` | FrontendDeveloper | UXDesigner, QAEngineer |
| `src/utils/` | BackendDeveloper | QAEngineer |
| `tests/` | QAEngineer | BackendDeveloper, FrontendDeveloper |
| `build_exe.py` | WindowsDesktopApp | - |
| Carpeta raíz | ProjectManager | WindowsDesktopApp |

---

## Por Tecnología

| Tech | Agente | Uso |
|------|--------|-----|
| **Python** | WindowsDesktopApp | Todo tu código |
| **tkinter** | FrontendDeveloper | Componentes UI |
| **SQLAlchemy** | BackendDeveloper | ORM para BD |
| **FastAPI** | BackendDeveloper | APIs REST |
| **pytest** | QAEngineer | Tests automatizados |
| **PyInstaller** | WindowsDesktopApp | Generar .exe |

---

## Por Fase del Proyecto

### 📋 Planificación
```
ProjectManager → Define user stories
    ↓
UXDesigner → Crea wireframes
    ↓
[Listo para implementar]
```

### 🛠️ Implementación
```
Backend Dev → Crea servicios
    ↓
Frontend Dev → Crea componentes
    ↓
Desktop App → Conecta todo con MVC
```

### 🧪 Testing
```
QAEngineer → Escribe tests
    ↓
QAEngineer → Valida cobertura (≥80%)
    ↓
[Ready for release]
```

### 📦 Empaquetado
```
Desktop App → Genera .exe
    ↓
[Ejecutable listo]
```

---

## 🎯 Ejemplos del Mundo Real

### Escenario 1: "El botón no responde cuando hago clic"

```mermaid
¿Qué revisar?
    ↓
¿Es problema de UI? → SÍ → FrontendDeveloper
    ↓ NO
¿Es problema de lógica? → SÍ → BackendDeveloper
    ↓ NO
¿Falta el test? → SÍ → QAEngineer
    ↓ NO
Revisar arquitectura → WindowsDesktopApp
```

**Solución**:
```
Usa el agente FrontendDeveloper: Fix botón no responde
[Al describir el problema]
```

---

### Escenario 2: "Mi función hace demasiadas cosas"

```
Usa el agente WindowsDesktopApp

Mi función en src/controllers/app_controller.py tiene 40 líneas.
¿Cómo la refactorizo manteniendo MVC?
```

---

### Escenario 3: "Necesito escribir un test para validar archivos"

```
Usa el agente QAEngineer

Escribe tests para src/utils/validators.is_valid_audio_file()
Casos:
- Archivo válido (MP3)
- Archivo inválido (TXT)
- Archivo corrupto
- Archivo > 500MB

Objetivo: Cobertura 100%
```

---

### Escenario 4: "¿Cumple con WCAG 2.1?"

```
Usa el agente UXDesigner

Revisa si la interfaz cumple:
- Contraste de colores (4.5:1)
- Tamaño mínimo de botones (44x44px)
- Fuente legible (≥12px)
```

---

### Escenario 5: "Planificar segunda semana"

```
Usa el agente ProjectManager

Crea sprint backlog para Sprint 2:
1. User stories con acceptance criteria
2. Story points
3. Asignaciones
4. Dependencias

Features a completar:
- Transcripción real con SpeechRecognition
- Exportar a múltiples formatos
- Historial de transcripciones
```

---

## 💡 Combinaciones de Agentes

### "Mejorar la UX del flujo de transcripción"

```
Paso 1: Usa el agente UXDesigner
→ Revisa wireframe actual
→ Sugiere mejoras

Paso 2: Usa el agente FrontendDeveloper
→ Implementa cambios

Paso 3: Usa el agente QAEngineer
→ Valida con tests de usabilidad
```

### "Refactorizar toda la capa de modelo"

```
Paso 1: Usa el agente WindowsDesktopApp
→ Revisa estructura actual

Paso 2: Usa el agente BackendDeveloper
→ Mejora servicios

Paso 3: Usa el agente QAEngineer
→ Escribe tests

Paso 4: Usa el agente ProjectManager
→ Documenta cambios
```

---

## 🚫 Evita

| ❌ | ✅ |
|----|-----|
| "¿Qué hago?" (vago) | "Crea un modelo para Usuario con validación de email" |
| Usar un agente para todo | Usa el agente correcto según la tarea |
| No activar agentes | Menciona el agente específicamente |
| Mezclar responsabilidades | Ej: Frontend + BD juntos |

---

## 🔗 Referencia Rápida

- 📖 **Documentación**: Ver `AGENTS.md`
- 🚀 **Quick Start**: Ver `README.md`
- 📁 **Estructura**: Ver `PROJECT_STRUCTURE.md`
- ⚡ **Comandos**: Ver `.github/AGENTS_QUICK_REFERENCE.md`

---

*Última actualización: 30 de marzo de 2026 | Equipo: Desktop App Dev*
