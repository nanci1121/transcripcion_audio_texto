---
description: "Referencia rápida de agentes. Use cuando: necesites un agente específico para tu rol o tarea actual. Mención el agente por nombre o alias."
---

# 🎯 Referencia Rápida de Agentes

Copia y pega el comando que necesites en el chat de Copilot:

---

## 🖥️ **WindowsDesktopApp** (Arquitectura)

Para: *Estructurar código MVC, crear archivos ejecutables*

```
Usa el agente WindowsDesktopApp
```

---

## 🔧 **BackendDeveloper** (Backend)

Para: *APIs, bases de datos, servicios, lógica*

```
Usa el agente BackendDeveloper
```

Alias: `Backend`, `API`, `Database`, `Service`

---

## 🎨 **FrontendDeveloper** (Frontend)

Para: *UI, componentes, gestión de estado, eventos*

```
Usa el agente FrontendDeveloper
```

Alias: `Frontend`, `UI`, `Component`, `View`

---

## 🎭 **UXDesigner** (Diseño)

Para: *Wireframes, accesibilidad, componentes visuales*

```
Usa el agente UXDesigner
```

Alias: `UX`, `Design`, `Wireframe`, `WCAG`

---

## 🧪 **QAEngineer** (Testing)

Para: *Tests, validación, casos de prueba, cobertura*

```
Usa el agente QAEngineer
```

Alias: `QA`, `Testing`, `Test`, `Coverage`

---

## 📋 **ProjectManager** (Gestión)

Para: *Sprints, user stories, planificación, requisitos*

```
Usa el agente ProjectManager
```

Alias: `PM`, `Scrum`, `Sprint`, `Planning`

---

## 📚 Ejemplos Completos

### Backend: Crear API de transcripción

```
Usa el agente BackendDeveloper

Necesito crear un servicio TranscriptionService que:
1. Procese archivos de audio
2. Maneje errores específicos
3. Tenga documentación OpenAPI
4. Incluya tests unitarios

Estructura: src/services/transcription_service.py
```

### Frontend: Mejorar componente de carga

```
Usa el agente FrontendDeveloper

Crea un componente AudioUploadPanel que:
1. Soporte drag-and-drop
2. Muestre progreso de carga
3. Callbacks: on_success, on_error
4. Sea reutilizable en otras pantallas
```

### UX: Diseñar flujo de transcripción

```
Usa el agente UXDesigner

Diseña el flujo UI para:
1. Seleccionar archivo
2. Mostrar progreso
3. Mostrar resultado transcrito

Requisitos: WCAG AA, Windows 11 style
```

### QA: Tests de integración

```
Usa el agente QAEngineer

Escribe tests de integración entre:
- MainWindow (vista)
- AppController (controlador)
- TranscriptionTask (modelo)

Incluye: Casos normales, edge cases, errores
Cobertura: ≥85%
```

### PM: Planificar Sprint 1

```
Usa el agente ProjectManager

Crea el sprint backlog para Sprint 1 (2 semanas):
1. User stories con acceptance criteria
2. Estimación en story points
3. Asignación de tareas
4. Definición de "Done"

Features: Seleccionar archivo, validación, UI básica
```

---

## 🔗 Activación Automática

Estos agentes se activan **automáticamente** en ciertos contextos:

- **WindowsDesktopApp**: Al trabajar en `src/**/*.py`

Los demás se activan **manualmente** mencionándolos en el chat.

---

## 💡 Pro Tips

1. **Sé específico**: Da contexto al agente
   ```
   ✓ Usa BackendDeveloper para validar este endpoint de FastAPI
   ✓ El archivo está en src/api/routes.py
   ✓ Necesito tests también
   ```

2. **Combina agentes**: Puedes pedir a varios en un chat
   ```
   Usa UXDesigner: Revisa si este botón cumple WCAG AA
   Usa Frontend: Implementa el componente
   Usa QA: Escribe tests para el componente
   ```

3. **Referencia archivos**: Los agentes entienden rutas relativas
   ```
   Usa BackendDeveloper para revisar src/services/transcription_service.py
   ```

---

*Última actualización: 30 de marzo de 2026*
