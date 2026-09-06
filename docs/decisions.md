# Decisiones técnicas — mi-IA-local

Este documento registra las decisiones técnicas importantes tomadas durante el desarrollo del proyecto.

Las decisiones no deberán modificarse sin analizar previamente sus consecuencias.

---

# ADR-001 — Modelo inicial

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Decisión

Utilizar **Qwen3 8B** como modelo de lenguaje inicial.

## Motivo

Qwen3 8B proporciona un equilibrio adecuado entre capacidad, tamaño y rendimiento para el hardware disponible.

El proyecto se desarrolla principalmente con una NVIDIA RTX 4060 de 8 GB de VRAM y 16 GB de RAM.

## Consecuencia

El sistema deberá estar diseñado para permitir cambiar posteriormente de modelo.

---

# ADR-002 — Motor de ejecución del modelo

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Decisión

Utilizar **Ollama** como motor local para ejecutar el modelo.

## Motivo

Ollama permite ejecutar modelos localmente y proporciona una interfaz mediante la cual nuestra aplicación puede comunicarse con ellos.

Esto permite separar el modelo de la aplicación.

## Consecuencia

La aplicación no deberá depender directamente de detalles internos de Qwen3.

---

# ADR-003 — Lenguaje principal

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Decisión

Utilizar **Python** como lenguaje principal del backend.

## Motivo

Python cuenta con un ecosistema amplio para inteligencia artificial, procesamiento de documentos, APIs, bases de datos, automatización y desarrollo de agentes.

También facilita la integración con Ollama.

## Consecuencia

La lógica principal del sistema se desarrollará en Python.

---

# ADR-004 — Base de datos

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Decisión

Utilizar **SQLite** como base de datos inicial.

## Motivo

El proyecto tiene un enfoque local-first y no necesita inicialmente un servidor de base de datos independiente.

SQLite permite almacenar información localmente en un archivo y tiene integración directa con Python.

## Consecuencia

La base de datos será local y sencilla de respaldar.

Si el proyecto alcanza necesidades que SQLite no pueda cubrir adecuadamente, se evaluarán alternativas.

---

# ADR-005 — Frontend

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Decisión

Utilizar **TypeScript + Angular** como tecnología prevista para el frontend.

## Motivo

Angular proporciona una estructura adecuada para desarrollar una interfaz organizada y escalable.

Además, el desarrollador del proyecto ya tiene experiencia con Angular y TypeScript.

## Consecuencia

El frontend se implementará después del prototipo inicial y no será una prioridad durante v0.1.

---

# ADR-006 — Desarrollo incremental

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Decisión

El proyecto se desarrollará mediante versiones progresivas.

## Motivo

Intentar implementar simultáneamente conversación, memoria, documentos, visión, Internet y herramientas aumentaría innecesariamente la complejidad y dificultaría la detección de errores.

## Consecuencia

Cada versión deberá completarse y probarse antes de avanzar a la siguiente.

---

# ADR-007 — Enfoque de privacidad

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Decisión

El proyecto seguirá un enfoque **local-first**.

## Motivo

El objetivo principal es ejecutar la IA y almacenar sus datos localmente.

## Consecuencia

Las conversaciones, memoria y documentos deberán permanecer locales siempre que sea posible.

Las funciones que requieran servicios externos deberán estar claramente identificadas.

---

# ADR-008 — Nombre de la IA

**Estado:** Pendiente

## Decisión

No se ha establecido todavía un nombre definitivo para la IA.

Durante el desarrollo inicial se utilizará el nombre provisional:

**Prototipo**

## Motivo

El proyecto todavía se encuentra en una etapa experimental y sus capacidades finales aún no están definidas.

## Consecuencia

El nombre podrá definirse posteriormente sin afectar la arquitectura técnica.

---

# ADR-009 — Arquitectura inicial

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Decisión

La primera versión utilizará una arquitectura sencilla basada en:

**Python → Ollama → Qwen3 8B**

## Motivo

El objetivo de v0.1 es comprobar la comunicación entre nuestra aplicación y el modelo antes de agregar componentes adicionales.

## Consecuencia

No se incorporarán inicialmente base de datos, frontend complejo, Internet, herramientas ni memoria persistente.

---

# ADR-010 — Seguridad de herramientas

**Estado:** Aceptada

## Decisión

Las herramientas capaces de modificar el sistema deberán contar con controles de permisos.

## Motivo

Un modelo de IA no debe tener acceso ilimitado al sistema operativo únicamente porque pueda generar instrucciones o llamadas a herramientas.

## Consecuencia

Las acciones potencialmente destructivas deberán requerir controles adicionales y, cuando corresponda, autorización explícita del usuario.

---

# Registro de cambios

Las nuevas decisiones importantes deberán agregarse siguiendo el formato:

```text
ADR-XXX — Título

Estado:
Fecha:

## Decisión

¿Qué se decidió?

## Motivo

¿Por qué se tomó esta decisión?

## Consecuencia

¿Qué implica para el proyecto?
```

Los registros existentes no deberán eliminarse simplemente porque una decisión cambie.

En caso de modificar una decisión importante, deberá documentarse la nueva decisión y explicar por qué reemplaza a la anterior.
