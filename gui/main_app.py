import customtkinter as ctk
from PIL import Image, ImageTk
import os
from youtube_downloader_window import YouTubeDownloaderWindow
from podcast_downloader_window import PodcastDownloaderWindow
from ocr_window import OcrWindow
from transcriber_window import TranscriberWindow
from image_manager_window import ImageManagerWindow
from web_scraper_window import WebScraperWindow
from pdf_to_markdown_window import PDFtoMarkdownWindow
from google_drive_downloader_window import GoogleDriveDownloaderWindow

class ToolCard(ctk.CTkFrame):
    """Una tarjeta para mostrar una herramienta en la ventana principal."""
    def __init__(self, master, title, icon_path, command):
        super().__init__(master, corner_radius=10, fg_color="#ffffff")

        self.command = command
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Contenedor para el ícono
        icon_frame = ctk.CTkFrame(self, fg_color="transparent")
        icon_frame.grid(row=0, column=0, pady=(20, 10))

        # Cargar y mostrar el ícono
        icon_image = Image.open(icon_path).resize((48, 48))
        icon_photo = ImageTk.PhotoImage(icon_image)
        
        icon_label = ctk.CTkLabel(icon_frame, image=icon_photo, text="")
        icon_label.image = icon_photo
        icon_label.pack()

        # Título de la herramienta
        title_label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color="#111827")
        title_label.grid(row=1, column=0, sticky="n", padx=10, pady=(0, 20))

        # Hacer que toda la tarjeta sea clickeable
        self.bind("<Button-1>", self.on_click)
        icon_frame.bind("<Button-1>", self.on_click)
        icon_label.bind("<Button-1>", self.on_click)
        title_label.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        if self.command:
            self.command()

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Suite de Herramientas de Productividad")
        self.geometry("800x600")
        self.configure(fg_color="#f0f4f8")

        # Crear directorio de íconos si no existe
        self.icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
        if not os.path.exists(self.icon_path):
            os.makedirs(self.icon_path)
            print(f"Directorio de íconos creado en: {self.icon_path}")
            print("Por favor, descarga y coloca los íconos necesarios en esta carpeta.")

        # --- Layout Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Cabecera ---
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, pady=(40, 20), padx=20, sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(header_frame, text="Mis Herramientas de Productividad", font=ctk.CTkFont(size=32, weight="bold"), text_color="#111827")
        title_label.grid(row=0, column=0)

        # --- Contenedor de Herramientas ---
        tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        tools_frame.grid(row=1, column=0, padx=50, pady=20, sticky="nsew")
        tools_frame.grid_columnconfigure((0, 1, 2), weight=1)
        tools_frame.grid_rowconfigure((0, 1), weight=1)

        # --- Definición de Herramientas ---
        tools = [
            {"title": "Descargador de YouTube", "icon": "iconodescargadordeyoutubeenpantallaprincipal.png", "command": self.open_youtube_downloader},
            {"title": "Descargador de Podcasts", "icon": "iconodescargadordepodcastsenpantallaprincipal.png", "command": self.open_podcast_downloader},
            {"title": "Imagen a Texto (OCR)", "icon": "iconoimagenatextoocrenpantallaprincipal.png", "command": self.open_ocr_tool},
            {"title": "Transcriptor de Audio", "icon": "iconotranscriptordeaudioenpantallaprincipal.png", "command": self.open_transcriber},
            {"title": "Gestión de Imágenes", "icon": "iconogestiondeimagenesenpantallaprincipal.png", "command": self.open_image_manager},
            {"title": "Scraping Web", "icon": "iconoscrapingwebenpantallaprincipal.png", "command": self.open_web_scraper},
            {"title": "PDF a Markdown", "icon": "iconopdfamarkdownenpantallaprincipal.png", "command": self.open_pdf_to_markdown},
            {"title": "Descargador de Drive", "icon": "iconogoogledrivedownloaderenpantallaprincipal.png", "command": self.open_google_drive_downloader},
        ]

        # --- Crear y Colocar las Tarjetas de Herramientas ---
        for i, tool in enumerate(tools):
            row = i // 3
            col = i % 3
            icon_full_path = os.path.join(self.icon_path, tool["icon"])
            
            # Verificar si el ícono existe, si no, usar un placeholder
            if not os.path.exists(icon_full_path):
                # Crear un ícono placeholder si no existe
                placeholder_img = Image.new('RGB', (64, 64), color = 'grey')
                placeholder_img.save(icon_full_path)
                print(f"Ícono no encontrado: {tool['icon']}. Se creó un placeholder.")

            card = ToolCard(tools_frame, title=tool["title"], icon_path=icon_full_path, command=tool["command"])
            card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

        # --- Pie de Página ---
        footer_label = ctk.CTkLabel(self, text="Desarrollado con IA - 2025", font=ctk.CTkFont(size=12), text_color="#9ca3af")
        footer_label.grid(row=2, column=0, pady=(10, 20))

        self.youtube_window = None
        self.podcast_window = None
        self.ocr_window = None
        self.transcriber_window = None
        self.image_manager_window = None
        self.web_scraper_window = None
        self.pdf_to_markdown_window = None
        self.google_drive_downloader_window = None

    # --- Comandos para abrir las ventanas de las herramientas (placeholders) ---
    def open_youtube_downloader(self):
        if self.youtube_window is None or not self.youtube_window.winfo_exists():
            self.youtube_window = YouTubeDownloaderWindow(self)
            self.youtube_window.focus()
        else:
            self.youtube_window.focus()

    def open_podcast_downloader(self):
        if self.podcast_window is None or not self.podcast_window.winfo_exists():
            self.podcast_window = PodcastDownloaderWindow(self)
            self.podcast_window.focus()
        else:
            self.podcast_window.focus()

    def open_ocr_tool(self):
        if self.ocr_window is None or not self.ocr_window.winfo_exists():
            self.ocr_window = OcrWindow(self)
            self.ocr_window.focus()
        else:
            self.ocr_window.focus()

    def open_transcriber(self):
        if self.transcriber_window is None or not self.transcriber_window.winfo_exists():
            self.transcriber_window = TranscriberWindow(self)
            self.transcriber_window.focus()
        else:
            self.transcriber_window.focus()

    def open_image_manager(self):
        if self.image_manager_window is None or not self.image_manager_window.winfo_exists():
            self.image_manager_window = ImageManagerWindow(self)
            self.image_manager_window.focus()
        else:
            self.image_manager_window.focus()

    def open_web_scraper(self):
        if self.web_scraper_window is None or not self.web_scraper_window.winfo_exists():
            self.web_scraper_window = WebScraperWindow(self)
            self.web_scraper_window.focus()
        else:
            self.web_scraper_window.focus()

    def open_pdf_to_markdown(self):
        if self.pdf_to_markdown_window is None or not self.pdf_to_markdown_window.winfo_exists():
            self.pdf_to_markdown_window = PDFtoMarkdownWindow(self)
            self.pdf_to_markdown_window.focus()
        else:
            self.pdf_to_markdown_window.focus()
            
    def open_google_drive_downloader(self):
        if self.google_drive_downloader_window is None or not self.google_drive_downloader_window.winfo_exists():
            self.google_drive_downloader_window = GoogleDriveDownloaderWindow(self)
            self.google_drive_downloader_window.focus()
        else:
            self.google_drive_downloader_window.focus()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
