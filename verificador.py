import os
import sys
from pathlib import Path

# 1. Verificación de librerías de Python (Requisitos del README)
try:
    import ollama
    from dotenv import load_dotenv, set_key
except ImportError:
    print("\n⚠️ Faltan librerías de Python. Instalalas con los siguientes comandos:\n")
    print("Requisitos Formatter:")
    print("pip install markitdown[all]\n")
    print("Requisitos Indexer:")
    print("pip install langchain langchain-ollama langchain-chroma chromadb")
    print("pip install langchain-text-splitters\n")
    print("Requisitos Ollama y Main:")
    print("pip install ollama python-dotenv\n")
    sys.exit(1)

ENV_PATH = ".env"

def verificar_todo():
    """
    Verifica la conexión a Ollama y los modelos instalados.
    Lee y escribe la flag en el .env para no repetir el proceso.
    """
    load_dotenv(ENV_PATH)
    if os.getenv("todoListo") == "1":
        return True

    print("Realizando verificación inicial del sistema...")
    modelos_requeridos = ["nomic-embed-text", "qwen2.5:3b"]
    faltantes = []

    # 2. Verificación del servicio base de Ollama
    try:
        modelos_locales = [modelo['model'] for modelo in ollama.list()['models']]
    except Exception:
        print("\n❌ Error: No se pudo conectar con Ollama.")
        print(ollama.list())
        print("Podes descargarlo en: https://ollama.com/")
        print("Asegurate de instalarlo y que el servicio esté corriendo.\n")
        return False

    # 3. Verificación de modelos específicos
    for modelo in modelos_requeridos:
        if not any(modelo in m for m in modelos_locales):
            faltantes.append(modelo)

    if faltantes:
        print("\n⚠️ Faltan instalar los modelos de Ollama:")
        if "qwen2.5:3b" in faltantes:
            print("Modelo: ollama pull qwen2.5:3b")
        if "nomic-embed-text" in faltantes:
            print("Embebidos: ollama pull nomic-embed-text")
        
        print("\nVerificar con: ollama list")
        print("Al ingresar este comando debe aparecerte nomic-embed-text y qwen2.5:3b\n")
        return False
    
    print("✅ Verificación exitosa. Todos los modelos están listos.")
    
    # 4. Crear .env y guardar la flag
    if not Path(ENV_PATH).exists():
        Path(ENV_PATH).touch()
        
    set_key(ENV_PATH, "todoListo", "1")
    print("📁 Archivo .env actualizado (todoListo=1). No se volverá a verificar.")
    return True