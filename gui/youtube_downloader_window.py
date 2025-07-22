import customtkinter as ctk
from tkinter import filedialog
import os
import yt_dlp
import threading

class YouTubeDownloaderWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Descargador de YouTube")
        self.geometry("600x550")
        self.configure(fg_color="#f7f9fa")
        self.transient(master)
        self.grab_set()

        # --- Colores y Fuentes ---
        self.primary_color = "#0c7ff2"
        self.text_primary = "#111418"
        self.text_secondary = "#60758a"
        self.border_color = "#dbe0e6"
        self.card_bg = "#ffffff"

        # --- Layout Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self, fg_color=self.card_bg, corner_radius=10)
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)

        # --- Cabecera ---
        header_label = ctk.CTkLabel(main_frame, text="Descargador de YouTube", font=ctk.CTkFont(size=24, weight="bold"), text_color=self.text_primary)
        header_label.grid(row=0, column=0, pady=(20, 30))

        # --- Sección de URL ---
        url_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        url_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        url_frame.grid_columnconfigure(0, weight=1)

        url_label = ctk.CTkLabel(url_frame, text="URL del Video", font=ctk.CTkFont(size=12), text_color=self.text_secondary)
        url_label.grid(row=0, column=0, sticky="w")

        self.url_entry = ctk.CTkEntry(url_frame, placeholder_text="Pega la URL del video de YouTube aquí", height=40, border_color=self.border_color, fg_color="white")
        self.url_entry.grid(row=1, column=0, sticky="ew")

        # --- Sección de Formato ---
        format_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        format_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        format_frame.grid_columnconfigure((0, 1), weight=1)

        format_label = ctk.CTkLabel(format_frame, text="Formato", font=ctk.CTkFont(size=12), text_color=self.text_secondary)
        format_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        self.format_var = ctk.StringVar(value="mp3")
        
        radio_video = ctk.CTkRadioButton(format_frame, text="Video (MP4)", variable=self.format_var, value="mp4", text_color=self.text_primary)
        radio_audio = ctk.CTkRadioButton(format_frame, text="Audio (MP3)", variable=self.format_var, value="mp3", text_color=self.text_primary)
        
        radio_video.grid(row=1, column=0, padx=(0, 5), sticky="ew")
        radio_audio.grid(row=1, column=1, padx=(5, 0), sticky="ew")

        # --- Botón de Descarga ---
        download_button = ctk.CTkButton(main_frame, text="Descargar", command=self.start_download, height=40, font=ctk.CTkFont(weight="bold"))
        download_button.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        # --- Sección de Progreso ---
        self.progress_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.progress_frame.grid(row=4, column=0, padx=20, pady=5, sticky="ew")
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(self.progress_frame, text="Listo para descargar.", text_color=self.text_secondary)
        self.status_label.grid(row=0, column=0, sticky="w")

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, orientation="horizontal")
        self.progress_bar.set(0)
        
        # --- Sección Post-Descarga ---
        self.post_download_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.post_download_frame.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        self.open_folder_button = ctk.CTkButton(self.post_download_frame, text="Abrir Carpeta", command=self.open_folder, height=40, fg_color="#e5e7eb", text_color=self.text_primary, hover_color="#d1d5db")
        
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")

    def start_download(self):
        url = self.url_entry.get()
        download_format = self.format_var.get()
        
        if not url:
            self.status_label.configure(text="Por favor, introduce una URL.", text_color="red")
            return

        self.status_label.configure(text="Iniciando...", text_color=self.text_secondary)
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(5,0))
        self.progress_bar.set(0)
        self.open_folder_button.grid_forget()

        # Ejecutar la descarga en un hilo separado para no bloquear la GUI
        download_thread = threading.Thread(target=self.run_download, args=(url, download_format))
        download_thread.start()

    def run_download(self, url, download_format):
        try:
            # Opciones para yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best' if download_format == 'mp3' else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'nocheckcertificate': True,
                'ignoreerrors': True,
            }

            if download_format == 'mp3':
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="red")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes and downloaded_bytes:
                progress = downloaded_bytes / total_bytes
                self.progress_bar.set(progress)
                self.status_label.configure(text=f"Descargando... {int(progress * 100)}%")
        
        if d['status'] == 'finished':
            self.status_label.configure(text="Descarga completada. Procesando...", text_color="blue")
            self.progress_bar.set(1)
            self.after(1000, self.finalize_download) # Dar tiempo para el post-procesamiento

    def finalize_download(self):
        self.status_label.configure(text="¡Listo!", text_color="green")
        self.open_folder_button.grid(row=0, column=0, sticky="ew")


    def open_folder(self):
        # Abre el explorador de archivos en la carpeta de descargas
        os.startfile(self.download_path)

if __name__ == '__main__':
    # Esto es para probar la ventana de forma aislada
    app = ctk.CTk()
    app.withdraw() # Ocultar la ventana raíz principal
    window = YouTubeDownloaderWindow(app)
    app.mainloop()
