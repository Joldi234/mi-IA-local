# mi-IA-local

> Asistente de inteligencia artificial local en desarrollo.

## 📌 Descripción

**mi-IA-local** es un proyecto experimental cuyo objetivo es desarrollar un asistente de inteligencia artificial capaz de ejecutarse localmente en el equipo del usuario.

El proyecto comienza utilizando **Qwen3 8B** mediante **Ollama** y evolucionará progresivamente para incorporar diferentes capacidades.

El nombre definitivo de la IA se decidirá durante una etapa posterior del desarrollo.

Actualmente, la IA se identifica como **Prototipo**.

---

## 🎯 Objetivo

Crear un asistente que pueda evolucionar desde un sistema básico de conversación hasta un sistema capaz de:

* 💬 Mantener conversaciones.
* 🧠 Recordar información.
* 🗃️ Mantener memoria persistente.
* 📄 Leer y analizar documentos.
* 👁️ Analizar imágenes.
* 🌐 Investigar información en Internet.
* 🔎 Consultar diferentes fuentes.
* 🛠️ Utilizar herramientas.
* 🤖 Realizar tareas de múltiples pasos.

El proyecto será desarrollado de manera incremental para mantener el sistema estable, seguro y fácil de mantener.

---

## 🧠 Tecnología principal

### Modelo de lenguaje

**Qwen3 8B**

### Motor de ejecución

**Ollama**

Ollama permite ejecutar el modelo de lenguaje localmente y proporciona una interfaz para que nuestra aplicación pueda comunicarse con él.

---

## 💻 Hardware de desarrollo

El proyecto está siendo desarrollado principalmente en el siguiente equipo:

| Componente        | Especificación              |
| ----------------- | --------------------------- |
| CPU               | AMD Ryzen 5 5500X           |
| GPU               | NVIDIA RTX 4060 — 8 GB VRAM |
| RAM               | 16 GB DDR4                  |
| Almacenamiento    | 1 TB                        |
| Sistema operativo | Windows 11                  |

Las decisiones técnicas deberán considerar especialmente la capacidad de VRAM y RAM disponible.

---

## 🔐 Filosofía

El proyecto seguirá principalmente estos principios:

### Local-first

Priorizar el procesamiento y almacenamiento local siempre que sea posible.

### Privacidad

Los datos personales, conversaciones y memoria deberán permanecer localmente siempre que sea técnicamente posible.

Las funciones que necesiten servicios externos deberán estar claramente identificadas.

### Modularidad

Las diferentes capacidades de la IA deberán desarrollarse como módulos independientes.

### Seguridad

Las acciones que puedan modificar archivos, ejecutar comandos o realizar operaciones sensibles deberán contar con controles apropiados.

### Desarrollo incremental

Cada versión deberá construirse y probarse antes de avanzar a la siguiente.

---

## 🗺️ Roadmap

El proyecto se dividirá inicialmente en las siguientes etapas:

| Versión  | Objetivo                                      |
| -------- | --------------------------------------------- |
| **v0.1** | Comunicación básica con Qwen3 mediante Ollama |
| **v0.2** | Aplicación e interfaz propia                  |
| **v0.3** | Historial y memoria persistente               |
| **v0.4** | Lectura y análisis de documentos              |
| **v0.5** | Análisis de imágenes                          |
| **v0.6** | Investigación y navegación por Internet       |
| **v0.7** | Integración de herramientas                   |
| **v1.0** | Sistema de agente de IA                       |

Para conocer el roadmap completo:

`docs/roadmap.md`

---

## 📁 Estructura del proyecto

```text
mi-IA-local/
│
├── AGENTS.md
├── README.md
├── .gitignore
│
├── docs/
│   ├── roadmap.md
│   ├── architecture.md
│   └── decisions.md
│
├── backend/
│
├── frontend/
│
└── tests/
```

---

## Desarrollo con IA

El proyecto utiliza herramientas de inteligencia artificial para asistir en el desarrollo.

**OpenCode** será utilizado principalmente como asistente de programación.

Antes de implementar cambios importantes, se deberá revisar la arquitectura, el roadmap y las decisiones técnicas existentes.

La IA utilizada para programar no debe asumir automáticamente que una característica futura debe implementarse.

---

## 📊 Estado actual

**Estado:** Prototipo inicial

### Completado

* [x] Repositorio privado en GitHub.
* [x] Ollama instalado.
* [x] Qwen3 8B instalado.
* [x] Ejecución local del modelo.
* [x] Uso de GPU NVIDIA RTX 4060.
* [x] Contexto inicial para OpenCode.

### Próximo objetivo

* [ ] Crear la primera aplicación propia.
* [ ] Conectar la aplicación con Ollama.
* [ ] Crear la primera conversación desde nuestra aplicación.
* [ ] Establecer la arquitectura inicial del backend.

---

## 📄 Licencia

La licencia del proyecto se decidirá posteriormente.
