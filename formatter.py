import os
from pathlib import Path
from markitdown import MarkItDown
import docx
import fitz  # Librería PyMuPDF para lectura lógica de PDFs

def extraer_texto_docx(file_path):
    doc = docx.Document(file_path)
    texto_lineal = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(texto_lineal)

def extraer_texto_pdf(file_path):
    """Extrae texto de PDF leyendo por bloques lógicos y limpiando saltos de línea."""
    doc = fitz.open(file_path)
    texto_lineal = []
    
    for page in doc:
        # get_text("blocks") agrupa el texto que pertenece al mismo párrafo/elemento
        bloques = page.get_text("blocks")
        for b in bloques:
            texto_bloque = b[4].strip() # b[4] contiene el string del texto
            if texto_bloque:
                # Reemplazamos los saltos de línea internos por espacios para no cortar oraciones
                texto_limpio = texto_bloque.replace('\n', ' ')
                texto_lineal.append(texto_limpio)
                
    return "\n\n".join(texto_lineal)

def format_documents(input_folder="datos_entrada", output_folder="datos_procesados", history_file="historial.txt"):
    md_converter = MarkItDown()
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    history_path = Path(history_file)

    valid_extensions = {".pdf", ".docx", ".pptx", ".xlsx", ".csv", ".txt", ".html"}

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

            try:
                print(f"Convirtiendo: {file_path.name}")
                
                # Derivación según el formato del archivo para máxima precisión
                if file_path.suffix.lower() == ".docx":
                    texto_final = extraer_texto_docx(file_path)
                elif file_path.suffix.lower() == ".pdf":
                    texto_final = extraer_texto_pdf(file_path)
                else:
                    result = md_converter.convert(str(file_path))
                    texto_final = result.text_content
                
                with open(output_file_path, "w", encoding="utf-8") as f:
                    f.write(texto_final)
                
                extracto = texto_final.replace('\n', ' ')[:150].strip() + "..."
                
                with open(history_path, "a", encoding="utf-8") as f_hist:
                    f_hist.write(f"✅ Archivo: {file_path.name} | Ubicación: {relative_path.parent} | Extracto: {extracto}\n")
                    
            except Exception as e:
                print(f"❌ Se ha encontrado un error en el archivo '{file_path.name}': {e}")

if __name__ == "__main__":
    format_documents()