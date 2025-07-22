import customtkinter as ctk
import os
import threading
import requests
from bs4 import BeautifulSoup
import yt_dlp
from tkinter import filedialog

class CheckboxListItem(ctk.CTkFrame):
    """Un widget para un ítem de la lista con un checkbox y un título."""
    def __init__(self, master, text):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        
        self.checkbox_var = ctk.StringVar(value="off")
        self.checkbox = ctk.CTkCheckBox(self, text="", variable=self.checkbox_var, onvalue="on", offvalue="off")
        self.checkbox.grid(row=0, column=0)

        self.label = ctk.CTkLabel(self, text=text, anchor="w")
        self.label.grid(row=0, column=1, sticky="ew", padx=5)
        self.url = "" # Para almacenar la URL del episodio

    def is_checked(self):
        return self.checkbox_var.get() == "on"

    def set_checked(self, state):
        if state:
            self.checkbox_var.set("on")
        else:
            self.checkbox_var.set("off")

class PodcastDownloaderWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Descargador de Podcasts")
        self.geometry("700x700")
        self.configure(fg_color="#f8f9fa")
        self.transient(master)
        self.grab_set()

        # --- Colores y Fuentes ---
        self.text_primary = "#111418"
        self.text_secondary = "#60758a"
        self.card_background = "#ffffff"
        self.border_color = "#dee2e6"

        # --- Atributos de datos ---
        self.episodes = []
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads", "Podcasts")
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)

        # --- Layout Principal ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Contenedor Principal ---
        main_container = ctk.CTkFrame(self, fg_color=self.card_background, corner_radius=10, border_width=1, border_color=self.border_color)
        main_container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)

        # --- Título ---
        title_label = ctk.CTkLabel(main_container, text="Descargador de Podcasts", font=ctk.CTkFont(size=28, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # --- Búsqueda de URL ---
        url_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        url_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        url_frame.grid_columnconfigure(0, weight=1)

        self.url_entry = ctk.CTkEntry(url_frame, placeholder_text="Pega la URL base del podcast")
        self.url_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        search_button = ctk.CTkButton(url_frame, text="Buscar Episodios", command=self.search_episodes)
        search_button.grid(row=0, column=1)

        # --- Lista de Episodios ---
        episodes_container = ctk.CTkFrame(main_container, fg_color="transparent", border_width=1, border_color=self.border_color, corner_radius=5)
        episodes_container.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        episodes_container.grid_columnconfigure(0, weight=1)
        episodes_container.grid_rowconfigure(1, weight=1)

        episodes_header = ctk.CTkFrame(episodes_container, fg_color="transparent")
        episodes_header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        episodes_header.grid_columnconfigure(0, weight=1)

        episodes_label = ctk.CTkLabel(episodes_header, text="Episodios", font=ctk.CTkFont(size=16, weight="bold"))
        episodes_label.grid(row=0, column=0, sticky="w")

        selection_frame = ctk.CTkFrame(episodes_header, fg_color="transparent")
        selection_frame.grid(row=0, column=1, sticky="e")

        select_all_button = ctk.CTkButton(selection_frame, text="Seleccionar Todos", command=self.select_all, fg_color="gray", hover_color="darkgray", width=120)
        select_all_button.grid(row=0, column=0, padx=(0, 5))
        deselect_all_button = ctk.CTkButton(selection_frame, text="Deseleccionar Todos", command=self.deselect_all, fg_color="gray", hover_color="darkgray", width=140)
        deselect_all_button.grid(row=0, column=1)

        self.episodes_list_frame = ctk.CTkScrollableFrame(episodes_container, fg_color="transparent")
        self.episodes_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.episode_widgets = []

        # --- Descarga y Progreso ---
        download_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        download_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        download_frame.grid_columnconfigure(0, weight=1)

        download_button = ctk.CTkButton(download_frame, text="Descargar Seleccionados", command=self.download_selected, height=40)
        download_button.grid(row=0, column=0, sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(download_frame, orientation="horizontal")
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(download_frame, text="Listo.", text_color=self.text_secondary)
        
    def search_episodes(self):
        url = self.url_entry.get()
        if not url:
            self.status_label.configure(text="Por favor, introduce una URL base.", text_color="orange")
            self.status_label.grid(row=2, column=0, sticky="w", pady=(5,0))
            return

        self.status_label.configure(text="Buscando episodios...", text_color=self.text_secondary)
        self.status_label.grid(row=2, column=0, sticky="w", pady=(5,0))
        
        # Limpiar lista anterior
        for widget in self.episode_widgets:
            widget.destroy()
        self.episode_widgets = []

        # Ejecutar búsqueda en un hilo separado
        search_thread = threading.Thread(target=self.run_search, args=(url,))
        search_thread.start()

    def run_search(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            self.episodes = []
            # Esta es una heurística, puede necesitar ajuste para diferentes webs de podcasts
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and (href.endswith('.mp3') or 'download' in href or 'episode' in href):
                    title = link.text.strip() if link.text.strip() else os.path.basename(href)
                    if not href.startswith('http'):
                        href = requests.compat.urljoin(url, href)
                    self.episodes.append({'title': title, 'url': href})
            
            # Eliminar duplicados
            unique_episodes = []
            seen_urls = set()
            for episode in self.episodes:
                if episode['url'] not in seen_urls:
                    unique_episodes.append(episode)
                    seen_urls.add(episode['url'])
            self.episodes = unique_episodes

            self.after(0, self.populate_episodes)

        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error en la búsqueda: {e}", text_color="red"))

    def populate_episodes(self):
        if not self.episodes:
            self.status_label.configure(text="No se encontraron episodios. Intenta con otra URL.", text_color="orange")
            return

        for episode in self.episodes:
            item = CheckboxListItem(self.episodes_list_frame, text=episode['title'])
            item.url = episode['url']
            item.pack(fill="x", padx=5, pady=2)
            self.episode_widgets.append(item)
        
        self.status_label.configure(text=f"{len(self.episodes)} episodios encontrados. Selecciona cuáles descargar.")

    def select_all(self):
        for item in self.episode_widgets:
            item.set_checked(True)

    def deselect_all(self):
        for item in self.episode_widgets:
            item.set_checked(False)

    def download_selected(self):
        selected_items = [item for item in self.episode_widgets if item.is_checked()]
        if not selected_items:
            self.status_label.configure(text="No hay episodios seleccionados.", text_color="orange")
            return
        
        self.status_label.configure(text=f"Iniciando descarga de {len(selected_items)} episodios...", text_color=self.text_secondary)
        self.progress_bar.grid(row=1, column=0, sticky="ew", pady=(10,0))
        self.progress_bar.set(0)

        # Ejecutar descargas en un hilo separado
        download_thread = threading.Thread(target=self.run_downloads, args=(selected_items,))
        download_thread.start()

    def run_downloads(self, items_to_download):
        total_items = len(items_to_download)
        for i, item in enumerate(items_to_download):
            try:
                self.after(0, lambda text=f"Descargando ({i+1}/{total_items}): {item.label.cget('text')}": self.status_label.configure(text=text))
                
                ydl_opts = {
                    'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                    'nocheckcertificate': True,
                    'ignoreerrors': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                    }],
                    'format': 'bestaudio/best',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # yt-dlp puede a veces extraer el título mejor que nuestro scraping
                    info_dict = ydl.extract_info(item.url, download=False)
                    title = info_dict.get('title', item.label.cget("text"))
                    ydl.params['outtmpl'] = os.path.join(self.download_path, f"{title}.mp3")
                    ydl.download([item.url])

                progress = (i + 1) / total_items
                self.after(0, lambda p=progress: self.progress_bar.set(p))

            except Exception as e:
                print(f"Error descargando {item.url}: {e}")
                self.after(0, lambda text=f"Error en: {item.label.cget('text')}": self.status_label.configure(text=text, text_color="red"))
                continue
        
        self.after(0, lambda: self.status_label.configure(text="Descarga completada.", text_color="green"))


if __name__ == '__main__':
    app = ctk.CTk()
    app.withdraw()
    window = PodcastDownloaderWindow(app)
    app.mainloop()
