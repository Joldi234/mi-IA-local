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

# ADR-011 — API HTTP del backend con FastAPI + Uvicorn

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Contexto

La v0.1 se comunica con Ollama mediante una CLI en terminal. La v0.2 introduce la primera interfaz gráfica (Angular), que necesita una API HTTP local para conversar. El backend ya cuenta con `config.py` y `ollama_client.py` probados.

## Decisión

Utilizar **FastAPI + Uvicorn** como capa HTTP del backend, exponiendo un endpoint `POST /api/chat` que reutiliza `ollama_client.py` sin modificarlo.

## Motivo

FastAPI proporciona validación automática de payloads con pydantic, documentación OpenAPI automática, soporte nativo de async (útil para un futuro streaming) y es el estándar actual del ecosistema Python para APIs. Ejecuta endpoints síncronos en threadpool, por lo que el cliente httpx síncrono de v0.1 se integra sin fricción.

## Consecuencias

- Se agregan dos dependencias nuevas al backend: `fastapi` y `uvicorn`.
- La CLI de v0.1 (`python -m backend`) continúa siendo una interfaz válida.
- El modelo sigue configurándose únicamente en el servidor mediante `.env`; el frontend no conoce el nombre del modelo.

## Alternativas consideradas

- **Flask**: más simple, pero sin validación/contrato de API integrado ni documentación automática.
- **`http.server` de la stdlib**: demasiado básico, sin manejo de peticiones JSON tipadas ni capacidad de crecer con el roadmap.

---

# ADR-012 — Angular 22 como framework del frontend

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Contexto

El proyecto ya definió TypeScript + Angular como tecnología del frontend (ADR-005). Al momento de diseñar v0.2, Angular 22 (junio 2026) es la versión estable vigente, con soporte activo hasta junio de 2027 y LTS hasta junio de 2028; Angular 20 pierde soporte en noviembre de 2026 y Angular 19 ya es fin de vida.

## Decisión

Utilizar **Angular 22** para el frontend de v0.2, con el scaffold standalone, zoneless y signal-first que trae por defecto.

## Motivo

Es la versión con mayor respaldo disponible. Su era signal-first (Signal Forms estables, detección de cambios zoneless y OnPush por defecto) coincide con los estándares ya instalados del proyecto, y Vitest es el runner de pruebas por defecto. El Node.js 24 del equipo es compatible.

## Consecuencias

- El frontend se estructura en `frontend/` bajo el patrón por features ya estandarizado.
- En v0.2 no se incorporan router ni librerías de estilos externas.
- Los estándares Angular existentes del proyecto (signals, `inject()`, zoneless, control flow nativo) aplican directamente.

## Alternativas consideradas

- **Angular 21**: LTS hasta mayo de 2027; opción conservadora pero con menos vida útil restante.
- **Angular 20**: pierde soporte en noviembre de 2026.
- **React**: descartado por la decisión previa de Angular (ADR-005).

---

# ADR-013 — API stateless e historial temporal en memoria del frontend

**Estado:** Aceptada

**Fecha:** 2026-09-06

## Contexto

El roadmap establece que en v0.2 el contexto/historial es únicamente temporal durante la sesión y que la persistencia pertenece a v0.3. El backend de v0.1 no almacena estado.

## Decisión

La API HTTP de v0.2 será **stateless**: cada petición `POST /api/chat` recibe el historial completo desde el cliente, y el backend no almacena nada entre peticiones. El historial temporal vive en memoria del frontend mediante signals de Angular.

## Motivo

Una API sin estado elimina estructuralmente la posibilidad de persistir datos sin querer durante v0.2. Mantiene el backend simple y sin sesiones, y reconstruye el contexto del modelo en cada petición de la misma forma que la CLI de v0.1 con su lista en memoria.

## Consecuencias

- Recargar la página reinicia la sesión (comportamiento esperado de v0.2).
- El backend no requiere sesiones, almacenamiento ni base de datos.
- En v0.3 el historial pasará a SQLite y este diseño evolucionará hacia una API con estado persistente.

## Alternativas consideradas

- **Sesiones en memoria del backend**: complejidad adicional sin beneficio real para v0.2.
- **Persistencia temprana en SQLite**: viola el roadmap incremental; pertenece a v0.3.

---

# ADR-014 — Capa de persistencia en SQLite para v0.3-A

**Estado:** Aceptada

**Fecha:** 2026-09-07

## Contexto

El roadmap establece que v0.3 agrega almacenamiento local y memoria persistente (historial de conversaciones). La v0.2 es stateless y mantiene el historial únicamente en memoria del frontend (ADR-013). El backend no almacena estado y las decisiones previas ya fijaron SQLite como base de datos (ADR-004).

## Decisión

Implementar una capa de persistencia para v0.3-A que cumpla la fase de **almacenamiento** —sin exponerla todavía por la API—:

- **SQLite** con el módulo `sqlite3` de la stdlib y **sin ORM**.
- Nuevo módulo `backend/storage.py` con funciones que abren y cierran su propia conexión por llamada: `init_db`, `create_conversation`, `list_conversations`, `get_conversation`, `add_message` y `list_messages`.
- Esquema de dos tablas: `conversations` (IDs `INTEGER PRIMARY KEY AUTOINCREMENT`, `title`, `created_at`, `updated_at`) y `messages` (`conversation_id` con FK a `conversations` `ON DELETE CASCADE`, `role` con `CHECK (role IN ('user', 'assistant'))`, `content`, `created_at`), más un índice sobre `messages(conversation_id)`.
- Modelos pydantic v2 en `backend/models.py` (`Conversation`, `ConversationCreate`, `StoredMessage`, `StoredMessageCreate`) para representar los registros almacenados.
- Constante `DATABASE_PATH` en `backend/config.py`, configurable mediante la variable de entorno `DATABASE_PATH` con valor por defecto `./data/mi-ia-local.db`; el archivo de base de datos se ejecuta fuera de Git.
- Los errores de base de datos se traducen a `StorageError` y la ausencia de una conversación al agregar mensajes lanza `ConversationNotFoundError`, en el estilo plano con mensajes en español ya usado en el proyecto.

## Motivo

SQLite con la stdlib cubre el caso local-first sin agregar dependencias ni un servidor de base de datos. IDs enteros autoincrementales son simples y suficientes para un historial local. Cada función abre y cierra su propia conexión (con `PRAGMA foreign_keys = ON` y commit al confirmar), lo que hace que la persistencia sea natural entre llamadas y mantenga aislados los fallos de conexión.

## Consecuencias

- El historial de conversaciones y mensajes queda persistido en un archivo local dentro de `data/`, que se agrega a `.gitignore`.
- La API HTTP de v0.3-B deberá integrar esta capa de almacenamiento y convertirse en una API con estado persistente; la integración queda deliberadamente fuera de v0.3-A.
- Si el proyecto supera las necesidades de SQLite, se evaluarán alternativas (ADR-004).

## Alternativas consideradas

- **ORM (SQLAlchemy)**: agrega una dependencia y complejidad innecesarias para dos tablas simples de historial local.
- **Persistir en JSON**: sin integridad referencial ni consultas; SQLite con la stdlib es igual de simple y más robusto.

---

# ADR-015 — API con conversaciones persistentes para v0.3-B

**Estado:** Aceptada

**Fecha:** 2026-09-07

## Contexto

La v0.3-A implementó la capa de persistencia SQLite (`backend/storage.py`) sin exponerla por la API. La v0.2 expone únicamente `POST /api/chat` stateless (ADR-013), y el frontend mantiene el historial en memoria. El roadmap establece que v0.3 convierte la API en una API con estado persistente.

## Decisión

Exponer la capa de persistencia mediante cinco endpoints REST de conversaciones y mensajes, manteniendo **`POST /api/chat` de v0.2 intacto y compatible** de forma temporal:

- `POST /api/conversations` — crear una conversación (201).
- `GET /api/conversations` — listar conversaciones (orden por `updated_at` DESC).
- `GET /api/conversations/{id}` — obtener una conversación (404 si no existe).
- `GET /api/conversations/{id}/messages` — listar mensajes en orden cronológico (404 si la conversación no existe).
- `POST /api/conversations/{id}/messages` — enviar y persistir un mensaje: persiste el mensaje del usuario, recupera el historial completo, llama a Ollama y persiste la respuesta del asistente (201 con el mensaje del asistente persistido).

La coordinación vive en `api.py` (dependency `get_db_path()` inyectable para pruebas): `storage.py` no conoce FastAPI ni Ollama, y `ollama_client.py` no conoce SQLite. La ruta de la base de datos se inyecta en los tests mediante `dependency_overrides` con una BD temporal en `tmp_path`; la base real `data/mi-ia-local.db` nunca se usa en las pruebas.

## Motivo

Mantener `POST /api/chat` sin cambios preserva la compatibilidad con el frontend de v0.2 y con sus pruebas (la regresión de 33 tests queda intacta). Los endpoints REST nuevos son el contrato al que migrará el frontend (v0.3-C); cuando migre, `/api/chat` podrá deprecarse como decisión separada. La inyección de la ruta de BD mediante dependency de FastAPI permite probar la API con bases aisladas sin acoplar el código a variables globales.

## Consecuencias

- La API pasa a tener estado persistente: las conversaciones y mensajes creados sobreviven a reinicios.
- Ante un fallo de Ollama, el mensaje del usuario recién creado se elimina (rollback) y se devuelve el mismo código HTTP que `/api/chat` (503/404/504/502), para que un reintento no duplique mensajes. Si el rollback falla, el error se registra explícitamente en el log y no se oculta.
- No se mantiene una transacción SQLite abierta durante la llamada a Ollama: cada operación de storage abre y cierra su propia conexión (patrón de v0.3-A).
- El frontend de v0.2 continúa usando `POST /api/chat` hasta su migración (v0.3-C o posterior).
- Se agregan `PRAGMA busy_timeout = 3000` en `connect()` y la operación `delete_message` en `storage.py` para soportar el rollback.

## Alternativas consideradas

- **Evolucionar `POST /api/chat`** para aceptar `conversation_id`: rompe el contrato de v0.2, el frontend actual y sus pruebas; innecesario para esta fase.
- **Envolver `POST /api/chat`** sobre el nuevo flujo: agrega indirección sin beneficio real mientras el frontend no migre.

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
