---
applyTo: src/**/*.py
---

# Instrucciones de Copilot para el Proyecto

## Activación Automática

Este archivo activa el agente **WindowsDesktopApp** automáticamente cuando trabajas con archivos Python en `src/`.
Adicionalmente, el proyecto usa instrucciones por dominio en `.github/instructions/*.instructions.md` para reforzar comportamiento especifico de Backend, Frontend, UX, QA y Project Management segun la ruta del archivo.

## 🎯 Contexto del Proyecto

- **Tipo**: Aplicación de escritorio .exe para Windows 11
- **Arquitectura**: MVC (Model-View-Controller)
- **Stack**: Python 3.10+, tkinter/PyQt, modular
- **Objetivo**: Código rápido, limpio y bien estructurado

## 📋 Reglas de Código

1. **Separación de capas**: Modelo (datos), Vista (UI), Controlador (lógica)
2. **Sin imports circulares**: Asegúrate de que A → B → C, nunca C → A
3. **Functions ≤ 20 líneas**: Extrae métodos si es necesario
4. **Type hints**: Siempre en argumentos y valores de retorno
5. **Docstrings**: Toda clase y función pública necesita documentación
6. **Nombres significativos**: El código debe explicarse a sí mismo

## 🚫 Anti-patrones (evitar)

- ❌ Lógica de negocio mezclada con UI
- ❌ Funciones que hacen demasiadas cosas
- ❌ Variables globales para estado compartido
- ❌ Imports de módulos no necesarios
- ❌ Valores hardcodeados (usar `.config`)

## ✅ Cuando crees código

Asegúrate de:

```
1. Proponer ubicación correcta en el árbol (src/models, src/views, etc.)
2. Seguir naming conventions (PascalCase clases, snake_case funciones)
3. Incluir type hints y docstrings
4. Dividir en métodos pequeños y enfocados
5. Considerar reutilización y testabilidad
```

## 🔧 Herramientas Disponibles

- Ayuda para estructura de directorios
- Revisión de arquitectura MVC
- Sugerencias de refactorización
- Plantillas de código modular
- Validación de buenas prácticas

---

*Este archivo aplica a todos los archivos `.py` dentro de `src/`*
