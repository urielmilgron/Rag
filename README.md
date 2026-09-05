# 📚 Local RAG Pipeline

Un sistema de Generación Aumentada por Recuperación (RAG) 100% local, modular y privado. Este orquestador permite ingerir documentos (PDF, Word, Excel), convertirlos a Markdown, vectorizarlos y realizar consultas interactivas utilizando modelos de lenguaje locales a través de Ollama.

Optimizado para ejecutarse eficientemente de forma híbrida en CPU y memoria RAM, ideal para configuraciones como procesadores Ryzen y gráficas de la serie RX.

---

## 🛠️ Requisitos de Instalación

Es necesario instalar las dependencias de Python divididas según su función en el pipeline.

### 1. Formatter (Conversión de documentos)
`pip install markitdown[all]`

### 2. Indexer (Fragmentación y Vectorización)
`pip install langchain langchain-ollama langchain-chroma chromadb`
`pip install langchain-text-splitters`

### 3. Orquestador (Main & Verificador)
`pip install ollama python-dotenv`

---

## 🧠 Configuración de Ollama

El motor de inferencia local. Requiere tener el servicio instalado y los modelos descargados.

1. **Descargar Ollama:** Instalalo desde [ollama.com](https://ollama.com/).
2. **Descargar modelo de lenguaje (Generación):**
   `ollama pull qwen2.5:3b`
3. **Descargar modelo de Embeddings (Vectorización):**
   `ollama pull nomic-embed-text`
4. **Verificación:**
   Comprobá que los modelos estén instalados correctamente ejecutando:
   `ollama list`
   *(Deberían aparecer `nomic-embed-text` y `qwen2.5:3b` en la lista).*

---

## 🚀 Uso

El sistema cuenta con un verificador automático que validará tus dependencias la primera vez que lo ejecutes. 

Para iniciar el orquestador interactivo, simplemente ejecutá:

`python main.py`

### Flujo de Trabajo (Menú Principal)
1. **Procesar documentos:** Arrojá tus archivos en `datos_entrada`. El sistema replicará la jerarquía y extraerá el texto limpio hacia `datos_procesados`.
2. **Indexar:** Se generarán los chunks y vectores en una base de datos local oculta (`chroma_db`).
3. **Iniciar Chat RAG:** Interactuá con tus documentos. El modelo responderá citando las fuentes y carpetas originales.

---

## 📂 Estructura del Proyecto

* `main.py` - Menú orquestador principal.
* `verificador.py` - Chequeo de dependencias de Ollama y Python (`.env`).
* `formatter.py` - Extracción de texto y conversión a `.md`.
* `indexer.py` - Chunking y creación de la base vectorial ChromaDB.
* `rag.py` - Motor de recuperación y generación de respuestas.