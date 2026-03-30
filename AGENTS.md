# 🤖 Agentes Disponibles - Equipo Multidisciplinario

Este proyecto incluye **6 agentes especializados** para diferentes roles de desarrollo. Cada agente proporciona directrices, patrones y checklists específicos.

---

## 1. **WindowsDesktopApp** 🖥️

Arquitectura MVC y estructura de proyecto.

### Cuándo usarlo
- ✓ Creando interfaces gráficas con tkinter/PyQt
- ✓ Estructurando código con arquitectura MVC
- ✓ Refactorizando módulos
- ✓ Generando archivos ejecutables `.exe`

### Activación
- **Automática**: Al trabajar en `src/**/*.py`
- **Manual**: "*Usa el agente WindowsDesktopApp*"

### Proporciona
✅ Estructura de carpetas MVC  
✅ Patrones de código modular  
✅ Type hints y docstrings  
✅ Guide de empaquetado .exe

---

## 2. **BackendDeveloper** 🔧

APIs, bases de datos, lógica de servidor.

### Cuándo usarlo
- ✓ Construyendo APIs REST/gRPC
- ✓ Documentando servicios
- ✓ Integrando bases de datos (SQLAlchemy, SQLite)
- ✓ Implementando autenticación y autorización
- ✓ Escribiendo tests unitarios de servicios

### Activación
- **Automática**: Al trabajar en `src/services/**/*.py`, `src/models/**/*.py`, `src/controllers/**/*.py`, `src/utils/**/*.py` (via `.github/instructions/backend.instructions.md`)
- **Manual**: "*Usa el agente BackendDeveloper*" o "*Backend*"

### Proporciona
✅ Estructura de servicios  
✅ Documentación de API  
✅ Manejo de excepciones  
✅ Patrones de testing  
✅ Índices de base de datos

### Ejemplo
```python
# Crea servicio de transcripción con fastapi
# Implementa encolamiento con Celery
# Integra con base de datos
```

---

## 3. **FrontendDeveloper** 🎨

Interfaces gráficas, componentes, gestión de estado.

### Cuándo usarlo
- ✓ Construyendo componentes reutilizables
- ✓ Mejorando experiencia de usuario
- ✓ Gestión de estado de la aplicación
- ✓ Handling de eventos y callbacks
- ✓ Optimizando responsividad

### Activación
- **Automática**: Al trabajar en `src/views/**/*.py` (via `.github/instructions/frontend.instructions.md`)
- **Manual**: "*Usa el agente FrontendDeveloper*" o "*Frontend*"

### Proporciona
✅ Componentes modulares  
✅ Gestión centralizada de estado  
✅ Patrones de eventos  
✅ Accesibilidad (a11y)  
✅ Atajos de teclado

### Ejemplo
```python
# Crea componente de carga de archivo
# Implementa gestor de estado UI
# Configura atajos Alt+
```

---

## 4. **UXDesigner** 🎭

Wireframes, prototipos, experiencia de usuario.

### Cuándo usarlo
- ✓ Diseñando nuevas pantallas
- ✓ Mejorando accesibilidad (WCAG 2.1)
- ✓ Definiendo sistema de diseño (colores, tipografía)
- ✓ Creando wireframes y flujos
- ✓ Validando contraste y tamaño de elementos

### Activación
- **Automática**: Al trabajar en `src/views/**/*.py` y `README.md` (via `.github/instructions/ux.instructions.md`)
- **Manual**: "*Usa el agente UXDesigner*" o "*UX*" o "*Diseño*"

### Proporciona
✅ Paleta de colores (Windows 11)  
✅ Guías de accesibilidad WCAG AA  
✅ Wireframes de componentes  
✅ Matriz de estados UI  
✅ Sistema de espaciado

### Ejemplo
```
- Dialog "Seleccionar archivo": Wireframe + Estados
- Validar contraste colores: 4.5:1 (WCAG AA)
- Componente "Botón Transcribir": 44x44px mínimo
```

---

## 5. **QAEngineer** 🧪

Testing, validación, aseguramiento de calidad.

### Cuándo usarlo
- ✓ Escribiendo tests unitarios (pytest)
- ✓ Definiendo casos de prueba
- ✓ Evaluando cobertura de código (≥80%)
- ✓ Documentando regresiones
- ✓ Validando requisitos

### Activación
- **Automática**: Al trabajar en `tests/**/*.py` (via `.github/instructions/qa.instructions.md`)
- **Manual**: "*Usa el agente QAEngineer*" o "*Testing*" o "*QA*"

### Proporciona
✅ Estructura de tests (fixtures, assert)  
✅ Edge cases a validar  
✅ Matriz de casos de prueba  
✅ Reportes de bugs  
✅ Cobertura por componente

### Ejemplo
```python
# Tests para validators.is_valid_audio_file()
# Casos: archivo válido, inválido, vacío, corrupto
# Cobertura: 100%
```

---

## 6. **ProjectManager** 📋

Gestión ágil, planificación, sprint.

### Cuándo usarlo
- ✓ Planificando sprints de 2 semanas
- ✓ Definiéndose user stories con acceptance criteria
- ✓ Priorizando tareas (MoSCoW)
- ✓ Documentando decisiones
- ✓ Facilitando standups y retrospectives

### Activación
- **Automática**: Al trabajar en `README.md`, `AGENTS.md`, `.github/**/*.md` (via `.github/instructions/project-management.instructions.md`)
- **Manual**: "*Usa el agente ProjectManager*" o "*PM*" o "*Scrum*"

### Proporciona
✅ Estructura de sprint (2 semanas)  
✅ Template de user stories  
✅ Matriz MoSCoW  
✅ Burndown chart  
✅ Documentación CHANGELOG

### Ejemplo
```markdown
# US-001: Seleccionar archivo
AS A usuario
I WANT seleccionar un archivo de audio
SO THAT lo transoriba a texto

ACCEPTANCE CRITERIA:
- [ ] Botón visible
- [ ] Soporta MP3, WAV, M4A
- [ ] Valida tamaño <500MB
```

---

## 📊 Matriz de Responsabilidades

| Componente | Backend | Frontend | UX/UI | QA | PM |
|-----------|---------|----------|-------|----|----|
| API REST | ✅ | - | - | ✓ | - |
| BD/ORM | ✅ | - | - | ✓ | - |
| UI (tkinter) | - | ✅ | ✓ | ✓ | - |
| Componentes | - | ✅ | ✓ | ✓ | - |
| Tests | ✓ | - | - | ✅ | - |
| Documentación | ✓ | ✓ | ✓ | ✓ | ✅ |
| Requisitos | - | - | - | - | ✅ |

---

## 🔄 Flujo de Trabajo Recomendado

### 1️⃣ Inicio de Sprint

```
ProjectManager
  ↓
Define user stories + acceptance criteria
  ↓
UXDesigner
  ↓
Wireframes + componentes
  ↓
Equipo Dev (Backend + Frontend)
  ↓
Implementación
  ↓
QAEngineer
  ↓
Testing + validación
  ↓
Review + Demo
```

### 2️⃣ Ciclo Diario

```
ProjectManager
  ↓
Daily Standup (15 min)
  ↓
Backend Dev | Frontend Dev | QA
  ↓
Implementación + Testing
  ↓
Code Review
  ↓
Commit + Merge
```

---

## 💡 Ejemplos de Uso

### Backend: Crear servicio de transcripción

```
"Agente BackendDeveloper: 
Crea un servicio TranscriptionService que:
1. Valide archivos de audio
2. Use una cola de procesamiento
3. Guarde resultados en BD
4. Retorne estado en tiempo real"
```

### Frontend: Crear componente de carga

```
"Agente FrontendDeveloper:
Crea un componente AudioUploadPanel que:
1. Permita drag-and-drop
2. Muestre barra de progreso
3. Tenga callbacks para on_success/on_error"
```

### UX: Diseñar flujo de transcripción

```
"Agente UXDesigner:
Diseña wireframe del flujo:
1. Seleccionar archivo
2. Mostrar progreso
3. Mostrar resultado
Valida WCAG AA en cada paso"
```

### QA: Escribir tests de integración

```
"Agente QAEngineer:
Escribe tests para flujo E2E:
1. Seleccionar archivo → 
2. Transcribir → 
3. Exportar resultado
Cobertura: 100%"
```

### PM: Planificar sprint

```
"Agente ProjectManager:
Crea sprint backlog:
- US-001: Carga de archivo (3 pts)
- US-002: Transcripción (5 pts)
- US-003: Exportar (2 pts)
Total: 10 pts"
```

---

## 🚀 Stack Recomendado

| Categoría | Tecnología | Agente |
|-----------|-----------|--------|
| **Lenguaje** | Python 3.10+ | - |
| **UI** | tkinter | Frontend |
| **API** | FastAPI | Backend |
| **BD** | SQLite / SQLAlchemy | Backend |
| **Testing** | pytest | QA |
| **Empaquetado** | PyInstaller | Desktop |
| **Versionado** | Git | PM |

---

## 📁 Ubicación de Agentes

```
.github/agents/
├── windows-desktop-app.agent.md
├── backend-developer.agent.md
├── frontend-developer.agent.md
├── ux-designer.agent.md
├── qa-engineer.agent.md
└── project-manager.agent.md
```

---

## ✅ Checklist de Calidad

Antes de cada commit:

- [ ] Backend: Type hints + tests + documentación
- [ ] Frontend: Componentes reutilizables + a11y
- [ ] UX/UI: WCAG AA + contraste 4.5:1
- [ ] QA: ≥80% cobertura de código
- [ ] PM: User story completada + acceptance criteria

---

## 🔗 Referencias Rápidas

- [Scrum Guide](https://scrumguides.org/)
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [pytest](https://docs.pytest.org/)
- [Windows 11 Design](https://learn.microsoft.com/en-us/windows/windows-app-sdk/design/)

---

*Actualiza este archivo cuando agregues nuevos agentes o roles.*
