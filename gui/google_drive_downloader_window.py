import customtkinter as ctk
from google_drive_downloader import GoogleDriveDownloader

class GoogleDriveDownloaderWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        
        self.title("Descargador de Google Drive")
        self.geometry("700x500")
        self.resizable(True, True)
        
        # Inicializar el descargador de Google Drive
        self.downloader = GoogleDriveDownloader(self)
        
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
        # Cancelar cualquier descarga en curso antes de cerrar
        if hasattr(self.downloader, 'is_downloading') and self.downloader.is_downloading:
            self.downloader.cancel_download()
        self.destroy()
