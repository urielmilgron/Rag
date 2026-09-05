import sys
from verificador import verificar_todo
from formatter import format_documents
from indexer import create_index
from rag import iniciar_chat

def main():
    # 1. Verificación inicial de requisitos
    if not verificar_todo():
        print("\nPor favor, instalá los componentes faltantes y volvé a ejecutar main.py")
        sys.exit(1)
    
    # 2. Menú de orquestación
    while True:
        print("\n" + "="*40)
        print("      ORQUESTADOR RAG LOCAL")
        print("="*40)
        print("1. Procesar documentos (Word/PDF a .md)")
        print("2. Indexar (Crear base vectorial)")
        print("3. Iniciar Chat RAG")
        print("4. Ejecutar flujo completo (1 -> 2 -> 3)")
        print("5. Salir")
        
        opcion = input("\nElegí una opción (1-5): ")
        
        if opcion == '1':
            format_documents()
        elif opcion == '2':
            create_index()
        elif opcion == '3':
            iniciar_chat()
        elif opcion == '4':
            format_documents()
            create_index()
            iniciar_chat()
        elif opcion == '5':
            print("Cerrando el sistema...")
            sys.exit(0)
        else:
            print("Opción no válida. Intentá de nuevo.")

if __name__ == "__main__":
    main()