import customtkinter as ctk
from pdf_to_markdown import PDFtoMarkdownConverter

class PDFtoMarkdownWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Extractor PDF a Markdown")
        self.geometry("800x700")
        self.resizable(True, True)
        
        # Inicializar el conversor de PDF a Markdown
        self.converter = PDFtoMarkdownConverter(self)
        
        # Configurar la ventana para que se cierre correctamente
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centrar la ventana
        self.center_window()
    
    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def on_closing(self):
        self.destroy()
