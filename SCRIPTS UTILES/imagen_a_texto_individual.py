import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from docx import Document
import os

# Configurar la ruta de Tesseract si no está en PATH
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Descomentar para Windows


class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Español a DOCX")
        
        self.create_widgets()
    
    def create_widgets(self):
        self.btn_select = tk.Button(self.root, text="Seleccionar imagen", command=self.select_image)
        self.btn_select.pack(pady=10)
        
        self.btn_convert = tk.Button(self.root, text="Convertir a DOCX", command=self.convert_to_docx, state=tk.DISABLED)
        self.btn_convert.pack(pady=5)
        
        self.label = tk.Label(self.root, text="")
        self.label.pack(pady=10)
    
    def select_image(self):
        self.file_path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
        )
        if self.file_path:
            self.btn_convert.config(state=tk.NORMAL)
            self.label.config(text=f"Archivo seleccionado:\n{os.path.basename(self.file_path)}")
    
    def convert_to_docx(self):
        try:
            # Cargar imagen
            img = Image.open(self.file_path)
            
            # Realizar OCR en español
            text = pytesseract.image_to_string(img, lang='spa')
            
            # Crear documento Word
            doc = Document()
            doc.add_paragraph(text)
            
            # Guardar archivo
            output_file = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Documentos Word", "*.docx")]
            )
            
            if output_file:
                doc.save(output_file)
                self.label.config(text=f"Archivo guardado:\n{output_file}")
            
        except Exception as e:
            self.label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()