import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

def create_index(input_folder="datos_procesados", db_folder="./chroma_db"):
    """
    Lee los archivos .md, los divide en chunks, extrae metadatos (carpeta original)
    y crea/actualiza la base de datos vectorial local.
    """
    input_path = Path(input_folder)
    
    if not input_path.exists():
        print(f"La carpeta '{input_folder}' no existe. Ejecutá formatter.py primero.")
        return

    documents = []
    
    # 1. Leer los archivos y extraer metadatos
    print("Leyendo archivos Markdown...")
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                
                # Obtener la carpeta padre como metadato (categoría/temario)
                relative_path = file_path.relative_to(input_path)
                folder_name = relative_path.parent.name if relative_path.parent.name else "raiz"

                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                
                # Crear el documento con su texto y metadatos
                doc = Document(
                    page_content=text,
                    metadata={"source": str(relative_path), "carpeta": folder_name}
                )
                documents.append(doc)

    if not documents:
        print("No se encontraron archivos .md para indexar.")
        return

    # 2. Dividir el texto en chunks
    print("Dividiendo los textos en fragmentos (chunks)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Se generaron {len(chunks)} fragmentos en total.")

    # 3. Configurar Embeddings (se ejecutan en tu VRAM) y ChromaDB
    print("Creando vectores en ChromaDB (esto puede demorar un poco la primera vez)...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Crear y persistir la base de datos en la carpeta especificada
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_folder
    )
    
    print(f"¡Indexación completa! Base de datos guardada en '{db_folder}'.")

if __name__ == "__main__":
    create_index()