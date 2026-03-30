# 📋 Workflow de Pull Request - Revisión de Código

## 🔄 Estructura de Ramas

```
origin/main              ← Producción estable (requiere PR + revisión)
    ↑
    └─ Pull Request ← Merges solo mediante PR
        ↑
origin/develop          ← Rama de integración (donde estamos ahora)
    ↑
    └─ Feature Branches (futuros sprints)
```

---

## ✅ Estado Actual

```
Ramas locales:
  * develop     ← Rama actual (donde trabajamos)
    main        ← Rama protegida (solo PRs)

Ramas remotas:
  origin/develop    ← Ya subida a GitHub ✅
  origin/main       ← En GitHub sin cambios aún

Commits:
  dd22141 (en ambas ramas y origin)
```

---

## 🚀 Crear Pull Request en GitHub

### Paso 1: Ir a GitHub

Abre en el navegador:
```
https://github.com/nanci1121/transcripcion_audio_texto
```

### Paso 2: Crear el PR

Deberías ver un banner que dice:

```
Compare & pull request
develop had recent pushes
```

Haz clic en **"Compare & pull request"**

### Paso 3: Llenar el Formulario del PR

```
Title (Asunto):
🚀 [Sprint 0] Inicialización proyecto: MVC + 6 agentes especializados

Description (Descripción):
```

Copia esto:

```markdown
## 📋 Descripción
Inicialización completa del proyecto Transcriptor de Audio para Windows 11.

## ✅ Cambios Principales

### Arquitectura
- ✅ Estructura MVC (Models, Views, Controllers)
- ✅ Separación limpia de responsabilidades
- ✅ Sin imports circulares

### Agentes de Copilot
- ✅ 6 agentes especializados (Desktop, Backend, Frontend, UX, QA, PM)
- ✅ Instrucciones automáticas por archivo
- ✅ Documentación de referencia rápida

### Interfaz Gráfica
- ✅ tkinter UI profesional (900x700)
- ✅ 4 frames (archivo, transcripción, botones, estado)
- ✅ Manejo de eventos completo

### Código Base
- ✅ Type hints obligatorios
- ✅ Docstrings en todas las funciones
- ✅ Validadores reutilizables
- ✅ Configuración centralizada

### Testing
- ✅ Tests unitarios básicos (3 tests)
- ✅ Fixtures de prueba
- ✅ Base para cobertura ≥80%

### Documentación
- ✅ README.md con getting started
- ✅ PROJECT_STRUCTURE.md (mapa del proyecto)
- ✅ AGENTS.md (guía de agentes)
- ✅ Matriz de decisión de agentes

## 📊 Estadísticas
- Commits: 1
- Archivos: 33
- Líneas de código: 3,582
- Paquetes: 16

## 🔍 Checklist de Revisión

- [ ] Arquitectura MVC es clara y limpia
- [ ] No hay code duplicado
- [ ] Type hints presentes en todas partes
- [ ] Docstrings completos
- [ ] Tests pasan: `pytest tests/`
- [ ] No hay warnings de linting
- [ ] Archivos no hay hardcoding
- [ ] Documentación es completa

## 🎯 Siguiente Sprint
Implementar transcripción real con SpeechRecognition API (Sprint 1)

## 📝 Related Issues
Closes #0 (Initial setup)
```

### Paso 4: Configurar el PR

En la derecha verás opciones:

```
Reviewers (Revisores):
  → Selecciona a ti mismo como revisor

Assignees:
  → Asigna a ti mismo

Labels:
  → Elige: "enhancement", "documentation"

Milestone:
  → Sprint 0 (si lo has creado, opcional)
```

### Paso 5: Crear el PR

Haz clic en **"Create pull request"**

---

## 🔍 Revisión del Código (Como si fueras otro desarrollador)

### En la pestaña "Files Changed"

Verifica:

✅ **Code Quality**
- [ ] Nombres de variables significativos
- [ ] Funciones < 20 líneas
- [ ] Type hints presentes
- [ ] Docstrings completos

✅ **Architecture**
- [ ] Separación MVC clara
- [ ] No hay imports circulares
- [ ] Validaciones en el lugar correcto
- [ ] Configuración centralizada

✅ **Testing**
- [ ] Hay tests unitarios
- [ ] Edge cases cubiertos
- [ ] Tests pasan localmente

✅ **Security**
- [ ] Sin hardcoding de valores
- [ ] Validación de entrada
- [ ] Manejo de errores adecuado

### Agregar Comentarios de Review

Si encuentras algo, haz clic en la línea y comenta:

```
Comentario:
"Considerar usar ... instead of ..."

O positivo:
"✅ Buena separación de responsabilidades"
```

---

## 🔗 Merge del PR (Una Vez Aprobado)

### En GitHub (en la página del PR):

1. Espera a que se marquen todos los checks ✅
2. Haz clic en **"Approve"** (si eres revisor)
3. Haz clic en **"Merge pull request"**

Opciones de merge:
- **Create a merge commit** ← Recomendado (mantiene historia clara)
- Squash and merge (menos commits)
- Rebase and merge (historia lineal)

Elige **"Create a merge commit"** y confirma.

---

## 📞 Comandos Git Locales para Simular el PR

Si deseas hacer revisión local antes de crear PR:

```bash
# Ver cambios pendientes en develop
git diff main develop

# Ver commits en develop que no están en main
git log main..develop --oneline

# Cambiarse a main (como si fuera otro revisor)
git checkout main
git pull origin main

# Crear rama de revisión
git checkout -b review/initial-setup origin/develop
```

---

## ✅ Checklist Post-Merge

Una vez que el PR sea mergeado a main:

```bash
# En local, actualizar ramas
git checkout main
git pull origin main

# Verificar que main tiene los cambios
git log --oneline -2

# main y develop ahora están sincronizados
git log main develop --oneline -1
# Deben mostrar el mismo commit
```

---

## 🚀 Próximas Ramas para Futuros Sprints

### Sprint 1: Transcripción Real

```bash
git checkout -b feature/transcription-api develop
# ... hacer cambios ...
git push -u origin feature/transcription-api
# → Crear PR: feature/transcription-api → develop
```

### Sprint 2: Mejorar UI

```bash
git checkout -b feature/ui-components develop
# ... hacer cambios ...
git push -u origin feature/ui-components
# → Crear PR: feature/ui-components → develop
```

### Bugfixes Urgentes

```bash
git checkout -b hotfix/critical-bug main
# ... solucionar ...
git push -u origin hotfix/critical-bug
# → Crear PR: hotfix/critical-bug → main (urgente)
# → Luego PR: hotfix/critical-bug → develop (backport)
```

---

## 📊 Estrategia de Ramas Recomendada

```
main (producción)
├─ Hotfixes: hotfix/nombre
│   └─ PR → main + PR → develop
│
develop (integración)
├─ Features: feature/nombre
│   └─ PR → develop
│
├─ Bugfixes: bugfix/nombre (menores)
│   └─ PR → develop
│
└─ Tests: test/cobertura-mejorada
    └─ PR → develop
```

---

## 🔐 Configuración de Protección de Ramas (Opcional en GitHub)

Para hacer más robusta la revisión:

1. Ir a Settings → Branches
2. Agregar regla para `main`:
   ```
   ✓ Require pull request reviews before merging
   ✓ Require status checks to pass before merging
   ✓ Require branches to be up to date
   ✓ Restrict who can push to matching branches
   ```

3. Agregar regla para `develop`:
   ```
   ✓ Require pull request reviews before merging
   ✓ Require branches to be up to date
   ```

---

## 📝 Template para Comentarios de Review

### ✅ Aprobación

```
Excelente trabajo! Todo se ve bien:
- ✅ Arquitectura MVC limpia
- ✅ Documentación completa
- ✅ Tests presentes

Aprobado para merge.
```

### 🔍 Cambios Solicitados

```
Algunos cambios sugeridos:

1. En `src/models/transcription.py` línea XX:
   - Este método está muy largo (>20 líneas)
   - Sugerir dividir en métodos más pequeños

2. En `src/utils/config.py`:
   - Faltan type hints en esta función
   - Agregar docstring

Por favor, realizar estos cambios y re-request.
```

---

## 🎯 Flujo Completo Visual

```
LOCAL                   GITHUB
develop ─────────>  origin/develop
  (push -u)            (ramas)
                         │
                         ├─ Crear PR: develop → main
                         ├─ Agregar descripción
                         ├─ Revisar cambios
                         ├─ Comentarios (si hay)
                         ├─ Aprobar ✅
                         └─ Merge
                            │
                            v
                      origin/main (actualizado)
                            │
LOCAL                       │
main ────────────<─────────┘
  (pull)
```

---

*Última actualización: 30 de marzo de 2026*
