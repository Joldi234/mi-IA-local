# Roadmap — mi-IA-local

## 1. Propósito

Este documento define la evolución planificada de **mi-IA-local**, desde el prototipo inicial hasta un asistente de inteligencia artificial local con memoria, capacidades multimodales, acceso a Internet y herramientas.

El desarrollo será incremental.

Cada versión deberá:

1. Tener un objetivo claramente definido.
2. Implementar únicamente las funcionalidades correspondientes a esa etapa.
3. Ser probada antes de avanzar.
4. Mantener la arquitectura preparada para futuras funcionalidades.
5. Documentar las decisiones técnicas importantes.

**Importante:** completar una versión no significa implementar automáticamente las siguientes.

---

# v0.1 — Prototipo de IA local

### Objetivo

Crear la primera aplicación propia capaz de comunicarse con **Ollama** y utilizar **Qwen3 8B**.

### Funcionalidades

* Crear el backend inicial en Python.
* Conectarse con Ollama.
* Enviar mensajes a Qwen3 8B.
* Recibir respuestas del modelo.
* Mostrar las respuestas al usuario.
* Manejar errores básicos de conexión.
* Crear una estructura inicial de proyecto.
* Establecer una configuración básica mediante variables o archivos de configuración.

### Arquitectura

```text
Usuario
   ↓
Aplicación Python
   ↓
Ollama
   ↓
Qwen3 8B
   ↓
Respuesta
```

### No implementar todavía

* Memoria persistente.
* Base de datos.
* Internet.
* Búsqueda web.
* Lectura de documentos.
* Visión.
* Herramientas.
* Ejecución autónoma de comandos.
* Sistema de agentes.

### Resultado esperado

Una aplicación mínima que permita conversar con Qwen3 8B sin depender directamente del comando `ollama run` como interfaz principal.

---

# v0.2 — Aplicación e interfaz

### Objetivo

Convertir el prototipo en una aplicación más cómoda para utilizar.

### Funcionalidades

* Crear una interfaz gráfica/web.
* Crear un sistema de conversación.
* Mostrar mensajes del usuario y de la IA.
* Mostrar estados de carga.
* Manejar errores de comunicación.
* Permitir iniciar una nueva conversación.
* Mantener temporalmente el contexto/historial de la conversación (solo durante la sesión).

### Tecnologías previstas

* Backend: Python.
* Frontend: TypeScript.
* Framework frontend previsto: Angular.

### Arquitectura

```text
Frontend Angular
       ↓
API Python
       ↓
Ollama
       ↓
Qwen3 8B
```

### No implementar todavía

* Memoria permanente y persistencia del historial (corresponden a v0.3).
* Internet.
* Agentes autónomos.
* Herramientas peligrosas.
* Sistemas complejos de autenticación.

### Resultado esperado

Una aplicación local funcional que permita conversar con el modelo mediante una interfaz propia.

---

# v0.3 — Memoria y persistencia

### Objetivo

Permitir que la aplicación conserve información entre sesiones.

### Base de datos

Se utilizará inicialmente:

**SQLite**

### Funcionalidades

* Crear la base de datos local.
* Registrar conversaciones.
* Registrar mensajes.
* Recuperar conversaciones anteriores.
* Crear memoria persistente.
* Consultar memorias relevantes.
* Permitir eliminar memorias.
* Permitir consultar qué información está almacenada.
* Crear mecanismos para evitar almacenar información innecesaria.

### Posibles entidades

```text
conversations
messages
memories
settings
```

### Flujo

```text
Usuario
   ↓
Python
   ├──→ SQLite
   │      ↓
   │    Memoria
   │
   └──→ Ollama
          ↓
       Qwen3 8B
```

### Principio de privacidad

La memoria permanecerá almacenada localmente.

No se enviará automáticamente a servicios externos.

### Resultado esperado

La IA podrá utilizar información almacenada localmente para mejorar conversaciones futuras.

---

# v0.4 — Documentos

### Objetivo

Permitir que la IA trabaje con documentos proporcionados por el usuario.

### Formatos iniciales

* PDF.
* TXT.
* DOCX.

### Funcionalidades

* Importar documentos.
* Extraer texto.
* Registrar documentos.
* Buscar información dentro de documentos.
* Proporcionar fragmentos relevantes al modelo.
* Responder preguntas basadas en documentos.
* Mantener los archivos localmente.

### Ejemplo

```text
Usuario
   ↓
"Analiza este PDF"
   ↓
Sistema de documentos
   ↓
Extracción / búsqueda
   ↓
Información relevante
   ↓
Qwen3
   ↓
Respuesta
```

### Resultado esperado

El usuario podrá proporcionar documentos y hacer preguntas sobre su contenido.

---

# v0.5 — Visión

### Objetivo

Agregar capacidades para analizar imágenes.

### Funcionalidades

* Cargar imágenes.
* Analizar capturas de pantalla.
* Analizar imágenes proporcionadas por el usuario.
* Describir contenido visual.
* Identificar elementos relevantes.
* Analizar errores mostrados en capturas de pantalla.
* Integrar un modelo multimodal compatible.

### Importante

Qwen3 8B utilizado inicialmente es nuestro modelo de lenguaje principal.

La capacidad de visión podrá requerir un modelo multimodal adicional.

La arquitectura deberá permitir incorporar dicho modelo sin reemplazar innecesariamente el sistema completo.

### Resultado esperado

El usuario podrá enviar una imagen y realizar preguntas relacionadas con ella.

---

# v0.6 — Internet e investigación

### Objetivo

Permitir que la IA investigue información actual mediante Internet.

### Funcionalidades

* Integrar un sistema de búsqueda web.
* Realizar búsquedas mediante herramientas.
* Obtener información de páginas web.
* Procesar contenido relevante.
* Proporcionar fuentes utilizadas.
* Diferenciar información local de información obtenida de Internet.
* Informar al usuario cuando se utilice Internet.

### Flujo

```text
Pregunta
   ↓
Qwen3
   ↓
¿Necesita información actual?
   ↓
   Sí
   ↓
Búsqueda web
   ↓
Fuentes
   ↓
Información
   ↓
Qwen3
   ↓
Respuesta + fuentes
```

### Principio de privacidad

El acceso a Internet será una función externa.

El sistema deberá dejar claro cuándo una solicitud requiere comunicación con servicios externos.

### Resultado esperado

La IA podrá realizar investigaciones utilizando información actual y presentar las fuentes utilizadas.

---

# v0.7 — Herramientas

### Objetivo

Permitir que la IA utilice herramientas controladas.

### Posibles herramientas

* Calculadora.
* Sistema de archivos.
* Lectura de archivos.
* Búsqueda web.
* Consultas a la base de datos.
* Utilidades del sistema.
* Otras herramientas aprobadas.

### Arquitectura

```text
                 Qwen3
                   ↓
              Decisión
                   ↓
              Tool Manager
          ┌────────┼────────┐
          ↓        ↓        ↓
      Web Search  Files   Database
```

### Seguridad

Las herramientas deberán tener permisos definidos.

Las operaciones potencialmente destructivas deberán requerir autorización explícita.

Ejemplos:

* Eliminar archivos.
* Modificar archivos importantes.
* Ejecutar comandos.
* Instalar software.
* Realizar acciones externas.

### Resultado esperado

La IA podrá utilizar herramientas de manera controlada en lugar de limitarse a generar texto.

---

# v1.0 — Agente de IA

### Objetivo

Integrar las capacidades anteriores en un sistema capaz de realizar tareas de múltiples pasos.

### Capacidades esperadas

* Conversación.
* Memoria.
* Documentos.
* Visión.
* Internet.
* Herramientas.
* Planificación.
* Ejecución de tareas.
* Verificación de resultados.
* Manejo de errores.
* Solicitud de autorización cuando sea necesario.

### Ejemplo

El usuario podría solicitar:

> "Investiga este tema, compara varias fuentes y prepara un resumen utilizando el documento que te proporcioné."

El sistema podría:

```text
Solicitud
   ↓
Planificación
   ↓
┌───────────────┐
│ Leer documento│
└───────┬───────┘
        ↓
   Buscar Internet
        ↓
   Analizar fuentes
        ↓
   Comparar información
        ↓
   Generar respuesta
        ↓
   Verificar resultado
        ↓
      Usuario
```

### Principio fundamental

La autonomía deberá estar acompañada de controles de seguridad.

El sistema no debe ejecutar automáticamente cualquier acción solamente porque el modelo la haya solicitado.

---

# 🚧 Funcionalidades futuras

Las siguientes funciones podrán evaluarse después de v1.0:

* Modelos especializados.
* Mejoras avanzadas de memoria.
* RAG avanzado.
* Base de datos vectorial.
* Reconocimiento de voz.
* Síntesis de voz.
* Interacción por voz.
* Automatización avanzada.
* Integración con servicios externos.
* Multiusuario.
* Sincronización opcional.
* Aplicación móvil.
* Optimización avanzada del uso de GPU.
* Cambio dinámico entre modelos.

Estas funciones **no forman parte del alcance inicial**.

---

# 📊 Estado del proyecto

| Versión             | Estado            |
| ------------------- | ----------------- |
| v0.1 — IA local     | 🔵 En preparación |
| v0.2 — Aplicación   | ⚪ Pendiente       |
| v0.3 — Memoria      | ⚪ Pendiente       |
| v0.4 — Documentos   | ⚪ Pendiente       |
| v0.5 — Visión       | ⚪ Pendiente       |
| v0.6 — Internet     | ⚪ Pendiente       |
| v0.7 — Herramientas | ⚪ Pendiente       |
| v1.0 — Agente       | ⚪ Pendiente       |

---

# 📌 Regla de desarrollo

El desarrollo debe avanzar de forma secuencial.

No se deberá implementar una funcionalidad perteneciente a una versión posterior sin que la versión correspondiente haya sido aprobada.

Si una funcionalidad futura resulta necesaria para implementar correctamente la versión actual, OpenCode deberá:

1. Explicar por qué es necesaria.
2. Proponer una solución.
3. Esperar aprobación antes de ampliar el alcance.

El objetivo es mantener el proyecto pequeño, estable y comprensible durante cada etapa.
