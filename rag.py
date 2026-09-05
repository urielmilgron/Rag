import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

def iniciar_chat(db_folder="./chroma_db"):
    """
    Carga la base de datos, configura el LLM y lanza un bucle de chat 
    para hacerle preguntas a tus documentos.
    """
    if not os.path.exists(db_folder):
        print("No se encontró la base de datos. Ejecutá indexer.py primero.")
        return

    # 1. Cargar Embeddings y conectarse a ChromaDB
    print("Cargando base de datos vectorial...")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_db = Chroma(persist_directory=db_folder, embedding_function=embeddings)
    
    # Configurar el buscador (trae los 3 fragmentos más relevantes)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    
    # 2. Configurar el LLM local (Ollama)
    # Aumentamos num_ctx a 4096 para que entre bien el contexto de los documentos
    print("Cargando LLM...")
    llm = ChatOllama(model="qwen2.5:3b", temperature=0.2, num_ctx=4096, num_gpu=10)
    
    # 3. Definir el Prompt
    system_prompt = (
        "Sos un asistente experto. Respondé la pregunta del usuario utilizando "
        "ÚNICAMENTE el siguiente contexto recuperado de sus documentos. "
        "Si no encontrás la respuesta en el contexto, decí 'No tengo información "
        "sobre esto en los documentos proporcionados'. No inventes datos.\n\n"
        "Contexto:\n{context}"
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # 4. Ensamblar la cadena RAG (LangChain Expression Language)
    qa_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, qa_chain)
    
    # 5. Bucle de interacción
    print("\n" + "="*50)
    print("🤖 Sistema RAG iniciado. Podés hacer preguntas sobre tus archivos.")
    print("Escribí 'salir' para terminar el programa.")
    print("="*50)
    
    while True:
        pregunta = input("\nVos: ")
        if pregunta.lower() in ['salir', 'exit', 'quit']:
            print("¡Nos vemos!")
            break
        
        if not pregunta.strip():
            continue

        print("Buscando y analizando...")
        
        # Ejecutar la búsqueda y la generación
        resultado = rag_chain.invoke({"input": pregunta})
        
        # Imprimir respuesta
        print(f"\n🤖 Asistente: {resultado['answer']}")
        
        # Imprimir las fuentes (archivos) de donde sacó la información
        fuentes = set(
            doc.metadata.get("source", "Desconocido") 
            for doc in resultado["context"]
        )
        print(f"\n[Fuentes consultadas: {', '.join(fuentes)}]")

if __name__ == "__main__":
    iniciar_chat()