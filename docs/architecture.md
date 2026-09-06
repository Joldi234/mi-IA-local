# Arquitectura — mi-IA-local

## 1. Propósito

Este documento describe la arquitectura técnica de **mi-IA-local** y la forma en que sus diferentes componentes se comunicarán.

La arquitectura debe permitir que el proyecto crezca progresivamente sin tener que reconstruir el sistema completo cada vez que se agregue una nueva capacidad.

---

# 2. Principios arquitectónicos

La arquitectura seguirá estos principios:

### Modularidad

Cada capacidad importante deberá estar separada en módulos independientes.

### Bajo acoplamiento

Los componentes deberán depender lo menos posible unos de otros.

### Local-first

El procesamiento y almacenamiento local deberán ser la opción predeterminada.

### Extensibilidad

La arquitectura deberá permitir agregar posteriormente:

* Memoria.
* Documentos.
* Visión.
* Internet.
* Herramientas.
* Agentes.
* Nuevos modelos de IA.

### Seguridad

Las funciones capaces de interactuar con el sistema operativo o servicios externos deberán estar controladas.

---

# 3. Arquitectura general

La arquitectura prevista a largo plazo será:

```text
                         USUARIO
                            │
                            ▼
                    ┌───────────────┐
                    │   Frontend    │
                    │    Angular    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Python Backend│
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
         Conversation    Memory       Tool Manager
           Manager       Manager           │
              │             │              │
              │             ▼        ┌─────┼─────┐
              │          SQLite      │     │     │
              │                     Web  Files  Other
              │
              ▼
         AI Model Manager
              │
              ▼
           Ollama
              │
              ▼
          Qwen3 8B
```

Esta representa la arquitectura objetivo y no significa que todos estos componentes deban existir desde v0.1.

---

# 4. v0.1 — Arquitectura inicial

La primera versión será deliberadamente sencilla.

```text
Usuario
   │
   ▼
Python
   │
   ▼
Ollama
   │
   ▼
Qwen3 8B
   │
   ▼
Python
   │
   ▼
Usuario
```

En esta etapa no se utilizará todavía una base de datos.

Tampoco se implementarán herramientas, Internet, documentos o visión.

---

# 5. Backend

El backend será desarrollado principalmente utilizando **Python**.

Será responsable de:

* Gestionar las solicitudes del usuario.
* Comunicarse con Ollama.
* Administrar el contexto de las conversaciones.
* Gestionar posteriormente la memoria.
* Gestionar herramientas.
* Coordinar los diferentes módulos.
* Controlar errores.
* Aplicar reglas de seguridad.

La lógica principal de la aplicación deberá permanecer en el backend.

---

# 6. Comunicación con Ollama

Ollama funcionará como el motor local encargado de ejecutar el modelo.

La aplicación Python se comunicará con Ollama mediante su API local.

```text
Python Backend
      │
      │ API local
      ▼
    Ollama
      │
      ▼
   Qwen3 8B
```

La aplicación no deberá depender directamente de detalles internos del modelo.

Esto permitirá cambiar posteriormente de modelo si fuera necesario.

---

# 7. Modelo de inteligencia artificial

El modelo inicial será:

**Qwen3 8B**

Ollama será responsable de ejecutarlo localmente.

La arquitectura deberá utilizar una capa de abstracción para la comunicación con el modelo cuando sea conveniente.

Esto permitirá incorporar posteriormente otros modelos sin modificar toda la aplicación.

---

# 8. Base de datos

A partir de v0.3 se utilizará:

**SQLite**

La base de datos tendrá inicialmente como objetivo almacenar:

* Conversaciones.
* Mensajes.
* Memorias.
* Configuración.
* Información relacionada con documentos.

La base de datos deberá permanecer local.

---

# 9. Memoria

La memoria será implementada como un componente independiente.

```text
Usuario
   │
   ▼
Conversation Manager
   │
   ├──────► Memory Manager
   │              │
   │              ▼
   │           SQLite
   │
   ▼
Ollama
```

La memoria no debe mezclarse directamente con la lógica del modelo.

El sistema deberá decidir qué información recuperar y proporcionar al modelo como contexto.

---

# 10. Sistema de documentos

En v0.4 se agregará un módulo especializado para documentos.

Responsabilidades:

* Importar archivos.
* Extraer texto.
* Procesar contenido.
* Buscar información relevante.
* Proporcionar contexto al modelo.

Inicialmente se contemplan:

* PDF.
* TXT.
* DOCX.

Los documentos deberán permanecer localmente salvo que el usuario autorice explícitamente una operación externa.

---

# 11. Sistema de visión

En v0.5 se agregará un módulo de visión.

La arquitectura deberá permitir utilizar un modelo multimodal independiente del modelo principal.

```text
Imagen
   │
   ▼
Vision Manager
   │
   ▼
Modelo multimodal
   │
   ▼
Información visual
   │
   ▼
Sistema principal
```

No se asumirá que Qwen3 8B sea responsable de todas las tareas visuales.

---

# 12. Sistema de Internet

En v0.6 se agregará acceso controlado a Internet.

El acceso a Internet deberá realizarse mediante herramientas específicas.

```text
Qwen3
   │
   ▼
Tool Manager
   │
   ▼
Web Search
   │
   ▼
Internet
```

El modelo no tendrá acceso directo e ilimitado a Internet.

El sistema deberá controlar:

* Qué herramienta se utiliza.
* Qué información se solicita.
* Qué resultados se devuelven al modelo.
* Qué fuentes se presentan al usuario.

---

# 13. Sistema de herramientas

En v0.7 se implementará un sistema para administrar herramientas.

Las herramientas estarán separadas del modelo.

Ejemplo:

```text
Tool Manager
│
├── Web Search
├── File Reader
├── Database
├── Calculator
└── System Tools
```

Cada herramienta deberá definir claramente:

* Nombre.
* Propósito.
* Entradas.
* Salidas.
* Permisos.
* Restricciones.

---

# 14. Agente

La arquitectura de agente se implementará principalmente en v1.0.

El agente podrá:

1. Analizar una solicitud.
2. Crear un plan.
3. Seleccionar herramientas.
4. Ejecutar acciones.
5. Analizar resultados.
6. Continuar con el siguiente paso.
7. Verificar el resultado.
8. Solicitar autorización cuando sea necesario.

```text
Solicitud
   ↓
Planificación
   ↓
Herramienta
   ↓
Resultado
   ↓
Análisis
   ↓
Siguiente acción
   ↓
Resultado final
```

---

# 15. Seguridad

La seguridad será una parte fundamental de la arquitectura.

Las acciones deberán clasificarse según su riesgo.

### Bajo riesgo

Ejemplos:

* Realizar cálculos.
* Leer información.
* Buscar información.
* Analizar documentos.

### Riesgo medio

Ejemplos:

* Crear archivos.
* Modificar archivos.
* Realizar determinadas operaciones del sistema.

### Alto riesgo

Ejemplos:

* Eliminar archivos.
* Ejecutar comandos destructivos.
* Instalar software.
* Realizar acciones externas irreversibles.

Las operaciones de mayor riesgo deberán requerir autorización explícita.

---

# 16. Configuración

La configuración del sistema deberá estar separada del código.

Se podrán configurar aspectos como:

* Modelo utilizado.
* URL del servicio Ollama.
* Parámetros del modelo.
* Opciones de memoria.
* Herramientas habilitadas.

No se deberán almacenar secretos directamente en el código fuente.

---

# 17. Evolución de la arquitectura

La arquitectura debe crecer de manera incremental.

```text
v0.1
Python → Ollama → Qwen3

        ↓

v0.2
Frontend → Python → Ollama → Qwen3

        ↓

v0.3
Frontend → Python → SQLite
                  ↓
                Ollama
                  ↓
                Qwen3

        ↓

v0.4+
Frontend → Backend → Memory
                   → Documents
                   → Vision
                   → Internet
                   → Tools
                   → Ollama
```

Cada nueva capacidad deberá integrarse como un componente independiente siempre que sea posible.

---

# 18. Regla arquitectónica

No se deberá agregar complejidad únicamente porque una tecnología sea popular o técnicamente interesante.

Cada componente deberá justificar su existencia por una necesidad real del proyecto.

La arquitectura debe priorizar:

**simplicidad → estabilidad → seguridad → extensibilidad → optimización**
