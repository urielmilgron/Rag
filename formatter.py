import os
from pathlib import Path
from markitdown import MarkItDown

def format_documents(input_folder="datos_entrada", output_folder="datos_procesados", history_file="historial.txt"):
    md_converter = MarkItDown()
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    history_path = Path(history_file)

    valid_extensions = {".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".txt", ".html"}

    # Crear directorios iniciales
    if not input_path.exists():
        input_path.mkdir(parents=True, exist_ok=True)
        print(f"Se creó la carpeta '{input_folder}'. Colocá tus archivos ahí y volvé a ejecutar.")
        return
        
    output_path.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(input_path):
        for file in files:
            file_path = Path(root) / file
            
            if file_path.suffix.lower() not in valid_extensions:
                continue

            relative_path = file_path.relative_to(input_path)
            output_file_dir = output_path / relative_path.parent
            output_file_dir.mkdir(parents=True, exist_ok=True)

            output_file_path = output_file_dir / f"{file_path.stem}.md"

            if output_file_path.exists():
                continue

            # Bloque de validación y manejo de errores por documento
            try:
                print(f"Convirtiendo: {file_path.name}")
                result = md_converter.convert(str(file_path))
                
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(result.text_content)
                
                # Crear un extracto rápido limpiando saltos de línea
                extracto = result.text_content.replace('\n', ' ')[:150].strip() + "..."
                
                # Registrar en el historial (modo 'a' para agregar al final del archivo)
                with open(history_path, "a", encoding="utf-8") as f_hist:
                    f_hist.write(f"✅ Archivo: {file_path.name} | Ubicación: {relative_path.parent} | Extracto: {extracto}\n")
                    
            except Exception:
                # Mensaje de error personalizado sin detener el programa
                print(f"❌ Se ha encontrado un error en el archivo '{file_path.name}', por favor, reintentelo nuevamente.")

if __name__ == "__main__":
    format_documents()