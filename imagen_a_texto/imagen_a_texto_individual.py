# Script para convertir una imagen a texto y guardar en DOCX
# Uso: Ejecutar y seguir la interfaz gráfica

import pytesseract
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from docx import Document
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

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
            img = Image.open(self.file_path)
            text = pytesseract.image_to_string(img, lang="spa")
            doc = Document()
            doc.add_paragraph(text)
            save_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
            if save_path:
                doc.save(save_path)
                self.label.config(text="Guardado en: " + save_path)
        except Exception as e:
            self.label.config(text=f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
