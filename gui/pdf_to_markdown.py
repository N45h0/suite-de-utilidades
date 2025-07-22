import os
import sys
import re
import fitz  # PyMuPDF
import customtkinter as ctk
from PIL import Image, ImageTk
import tempfile
import shutil

class PDFtoMarkdownConverter:
    def __init__(self, master=None):
        self.master = master
        
        # Configuración de la ventana
        if master:
            self.window = ctk.CTkToplevel(master)
            self.window.title("Extractor PDF a Markdown")
            self.window.geometry("800x700")
            self.window.resizable(True, True)
            self.window.grid_columnconfigure(0, weight=1)
            self.window.grid_rowconfigure(2, weight=1)
        
            # Variables para almacenar rutas
            self.pdf_path = ""
            self.output_folder = ""
            self.images_folder = "pdf_images"  # Carpeta para guardar imágenes extraídas
            self.create_widgets()
    
    def create_widgets(self):
        # Frame superior para seleccionar archivo y opciones
        top_frame = ctk.CTkFrame(self.window)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Botón para seleccionar PDF
        self.select_btn = ctk.CTkButton(
            top_frame,
            text="Seleccionar PDF",
            command=self.select_pdf
        )
        self.select_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Mostrar ruta del archivo seleccionado
        self.file_label = ctk.CTkLabel(top_frame, text="Ningún archivo seleccionado")
        self.file_label.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón para seleccionar carpeta de salida
        self.output_btn = ctk.CTkButton(
            top_frame,
            text="Carpeta de Salida",
            command=self.select_output_folder
        )
        self.output_btn.grid(row=1, column=0, padx=10, pady=10)
        
        # Mostrar ruta de la carpeta de salida
        self.output_label = ctk.CTkLabel(top_frame, text="Carpeta predeterminada")
        self.output_label.grid(row=1, column=1, padx=10, pady=10)
        
        # Frame para opciones de conversión
        options_frame = ctk.CTkFrame(self.window)
        options_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Opciones de conversión
        self.extract_images_var = ctk.BooleanVar(value=True)
        self.extract_images_check = ctk.CTkCheckBox(
            options_frame,
            text="Extraer imágenes",
            variable=self.extract_images_var
        )
        self.extract_images_check.grid(row=0, column=0, padx=10, pady=10)
        
        self.keep_layout_var = ctk.BooleanVar(value=True)
        self.keep_layout_check = ctk.CTkCheckBox(
            options_frame,
            text="Mantener diseño",
            variable=self.keep_layout_var
        )
        self.keep_layout_check.grid(row=0, column=1, padx=10, pady=10)
        
        self.include_metadata_var = ctk.BooleanVar(value=True)
        self.include_metadata_check = ctk.CTkCheckBox(
            options_frame,
            text="Incluir metadatos",
            variable=self.include_metadata_var
        )
        self.include_metadata_check.grid(row=0, column=2, padx=10, pady=10)
        
        # Frame para texto y resultados
        text_frame = ctk.CTkFrame(self.window)
        text_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)
        
        # Área de texto para mostrar resultado
        self.result_text = ctk.CTkTextbox(text_frame, wrap="word")
        self.result_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Frame inferior para botones de acción
        bottom_frame = ctk.CTkFrame(self.window)
        bottom_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        
        # Botón para convertir
        self.convert_btn = ctk.CTkButton(
            bottom_frame,
            text="Convertir PDF a Markdown",
            command=self.convert_pdf_to_md
        )
        self.convert_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Botón para guardar resultado
        self.save_btn = ctk.CTkButton(
            bottom_frame,
            text="Guardar resultado",
            command=self.save_markdown
        )
        self.save_btn.grid(row=0, column=1, padx=10, pady=10)
    
    def select_pdf(self):
        filepath = ctk.filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if filepath:
            self.pdf_path = filepath
            self.file_label.configure(text=os.path.basename(filepath))
    
    def select_output_folder(self):
        folder_path = ctk.filedialog.askdirectory(title="Seleccionar carpeta de salida")
        if folder_path:
            self.output_folder = folder_path
            self.output_label.configure(text=folder_path)
    
    def convert_pdf_to_md(self):
        if not self.pdf_path:
            self.result_text.insert("1.0", "Por favor, selecciona un archivo PDF primero.\n")
            return
        
        try:
            # Limpiar área de texto
            self.result_text.delete("1.0", ctk.END)
            self.result_text.insert("1.0", "Procesando PDF, por favor espera...\n")
            self.window.update()
            
            # Crear carpeta temporal para imágenes si es necesario
            temp_dir = None
            if self.extract_images_var.get():
                temp_dir = tempfile.mkdtemp()
            
            # Abrir PDF con PyMuPDF
            doc = fitz.open(self.pdf_path)
            markdown_text = ""
            
            # Extraer metadatos si está activado
            if self.include_metadata_var.get():
                metadata = doc.metadata
                if metadata:
                    markdown_text += "---\n"
                    for key, value in metadata.items():
                        if value:
                            markdown_text += f"{key}: {value}\n"
                    markdown_text += "---\n\n"
            
            # Extraer título si existe
            if "title" in doc.metadata and doc.metadata["title"]:
                markdown_text += f"# {doc.metadata['title']}\n\n"
            
            # Procesar cada página
            for page_num, page in enumerate(doc):
                # Anunciar página actual
                markdown_text += f"\n## Página {page_num + 1}\n\n"
                
                # Extraer imágenes si está activado
                if self.extract_images_var.get():
                    img_list = page.get_images(full=True)
                    for img_idx, img_info in enumerate(img_list):
                        xref = img_info[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        image_filename = f"page{page_num+1}_img{img_idx+1}.{image_ext}"
                        image_path = os.path.join(temp_dir, image_filename)
                        
                        # Guardar imagen en directorio temporal
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_bytes)
                        
                        # Añadir referencia en markdown
                        markdown_text += f"![Imagen {img_idx+1} de la página {page_num+1}]({self.images_folder}/{image_filename})\n\n"
                
                # Extraer texto
                text = page.get_text()
                
                # Procesar texto según opciones
                if self.keep_layout_var.get():
                    # Mantener diseño: Convertir múltiples espacios a uno solo,
                    # pero preservar saltos de línea
                    text = re.sub(r" {2,}", " ", text)
                else:
                    # No mantener diseño: Convertir saltos de línea a espacios
                    # y luego múltiples espacios a uno solo
                    text = re.sub(r"\n", " ", text)
                    text = re.sub(r" {2,}", " ", text)
                    
                    # Restaurar párrafos
                    text = re.sub(r"(\. |\? |! )", "\\1\n\n", text)
                
                markdown_text += text + "\n\n"
            
            # Mostrar resultado en el área de texto
            self.result_text.delete("1.0", ctk.END)
            self.result_text.insert("1.0", markdown_text)
            
            # Guardar temporalmente el markdown y las imágenes
            self.markdown_content = markdown_text
            self.temp_images_dir = temp_dir
            
        except Exception as e:
            self.result_text.delete("1.0", ctk.END)
            self.result_text.insert("1.0", f"Error al procesar el PDF: {str(e)}")
    
    def save_markdown(self):
        if not hasattr(self, "markdown_content"):
            self.result_text.insert("1.0", "Primero debes convertir un PDF.\n")
            return
        
        # Determinar ruta de salida
        if not self.output_folder:
            self.output_folder = os.path.dirname(self.pdf_path)
        
        base_name = os.path.splitext(os.path.basename(self.pdf_path))[0]
        md_filepath = os.path.join(self.output_folder, f"{base_name}.md")
        
        # Crear carpeta de imágenes si es necesario
        images_dir = os.path.join(self.output_folder, self.images_folder)
        if self.extract_images_var.get() and hasattr(self, "temp_images_dir") and self.temp_images_dir:
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            
            # Copiar imágenes de carpeta temporal a carpeta de destino
            for file in os.listdir(self.temp_images_dir):
                shutil.copy(
                    os.path.join(self.temp_images_dir, file),
                    os.path.join(images_dir, file)
                )
            
            # Limpiar directorio temporal
            shutil.rmtree(self.temp_images_dir)
        
        # Guardar archivo markdown
        with open(md_filepath, "w", encoding="utf-8") as md_file:
            md_file.write(self.markdown_content)
        
        # Mostrar mensaje de éxito
        self.result_text.insert("1.0", f"Archivo guardado exitosamente en: {md_filepath}\n")

def main():
    app = ctk.CTk()
    app.title("Extractor PDF a Markdown")
    converter = PDFtoMarkdownConverter(app)
    app.mainloop()

if __name__ == "__main__":
    main()
