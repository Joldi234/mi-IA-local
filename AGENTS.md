# AGENTS.md — Contexto del proyecto

## 1. Identidad del proyecto

Nombre del repositorio: mi-IA-local

Nombre actual de la IA: Prototipo

Estado: Desarrollo inicial / prototipo

Objetivo principal:

Crear un asistente de inteligencia artificial local que utilice
un modelo de lenguaje ejecutado en el equipo del usuario y que,
progresivamente, pueda incorporar memoria, análisis de documentos,
visión, acceso controlado a Internet y uso de herramientas.

El nombre definitivo de la IA se decidirá posteriormente.

---

## 2. Hardware objetivo

El desarrollo se realiza principalmente en:

- GPU: NVIDIA RTX 4060 — 8 GB VRAM
- CPU: AMD Ryzen 5 5500X
- RAM: 16 GB DDR4
- Almacenamiento: 1 TB
- Sistema operativo: Windows 11

Las decisiones técnicas deben considerar las limitaciones de este
hardware, especialmente la VRAM y la memoria RAM disponibles.

---

## 3. Modelo de IA

Modelo inicial:

- Qwen3 8B

Motor de ejecución:

- Ollama

La arquitectura debe permitir cambiar posteriormente el modelo
sin tener que reconstruir todo el sistema.

---

## 4. Filosofía del proyecto

El proyecto seguirá principalmente estos principios:

### Local-first

La mayor cantidad posible de procesamiento y almacenamiento
debe realizarse localmente.

### Privacidad

Los datos del usuario, conversaciones y memoria deben permanecer
localmente siempre que sea técnicamente posible.

Cuando una función requiera comunicación externa, debe quedar
claramente identificada.

### Modularidad

Las funciones de la IA deben estar separadas en módulos para
poder modificarlas o reemplazarlas sin afectar todo el sistema.

### Seguridad

La IA no debe ejecutar acciones potencialmente peligrosas o
irreversibles sin controles y permisos adecuados.

### Mantenibilidad

El código debe mantenerse organizado, documentado y fácil de
entender.

### Desarrollo incremental

No se deben implementar todas las funciones al mismo tiempo.

Cada versión debe construirse, probarse y validarse antes de
continuar con la siguiente.

---

## 5. Objetivos a largo plazo

El proyecto podrá evolucionar progresivamente hacia un asistente
capaz de:

1. Mantener conversaciones.
2. Mantener historial de conversaciones.
3. Tener memoria persistente.
4. Leer y analizar documentos.
5. Analizar imágenes y capturas de pantalla.
6. Investigar información en Internet.
7. Consultar fuentes externas.
8. Utilizar herramientas.
9. Realizar tareas mediante múltiples pasos.
10. Funcionar como un agente de IA controlado.

Estas funciones representan objetivos futuros y no deben
implementarse todas durante el prototipo inicial.

---

## 6. Roadmap inicial

### v0.1 — Modelo local

Objetivo:

Crear una aplicación mínima capaz de comunicarse con Ollama
y utilizar Qwen3 8B.

### v0.2 — Aplicación

Objetivo:

Crear una interfaz propia para conversar con la IA y administrar
el historial.

### v0.3 — Memoria

Objetivo:

Agregar almacenamiento local y memoria persistente.

### v0.4 — Documentos

Objetivo:

Permitir que la IA trabaje con archivos como PDF, TXT y DOCX.

### v0.5 — Visión

Objetivo:

Agregar capacidades para analizar imágenes y capturas de pantalla.

### v0.6 — Internet

Objetivo:

Agregar investigación en Internet mediante herramientas
controladas y mostrar las fuentes utilizadas.

### v0.7 — Herramientas

Objetivo:

Permitir que la IA utilice herramientas externas y funciones
controladas.

### v1.0 — Agente

Objetivo:

Integrar razonamiento, memoria y herramientas para permitir que
la IA realice tareas de múltiples pasos bajo controles de seguridad.

---

## 7. Reglas para OpenCode

Antes de modificar el proyecto:

1. Leer este archivo.
2. Revisar la documentación disponible en `docs/`.
3. Identificar en qué versión del roadmap estamos.
4. No implementar funcionalidades pertenecientes a versiones
   posteriores sin autorización.
5. No realizar cambios grandes de arquitectura sin explicarlos
   previamente.
6. No instalar dependencias innecesarias.
7. Mantener el código modular.
8. Explicar los cambios importantes realizados.
9. Ejecutar las pruebas disponibles después de realizar cambios.
10. Informar de cualquier error o limitación encontrada.

Cuando una decisión técnica importante no esté definida,
proponer alternativas antes de implementarla.

---

## 8. Estado actual

El proyecto se encuentra en la etapa inicial.

Actualmente:

- GitHub está configurado.
- El repositorio es privado.
- Ollama está instalado.
- Qwen3 8B está instalado.
- Qwen3 8B puede ejecutarse localmente.
- La GPU RTX 4060 está siendo utilizada para ejecutar el modelo.

Todavía no existe una aplicación propia conectada al modelo.

El siguiente objetivo técnico es construir el primer prototipo
de comunicación entre nuestra aplicación y Ollama.

---

## 9. Importante

Este proyecto está siendo construido de manera progresiva con
ayuda de herramientas de inteligencia artificial para programación.

OpenCode funciona como asistente de desarrollo, pero las decisiones
importantes de arquitectura, seguridad y alcance deben ser
revisadas antes de implementarse.

No asumir que una función debe existir solamente porque sea
técnicamente posible.

Priorizar siempre:

funcionalidad → estabilidad → seguridad → optimización → nuevas funciones.