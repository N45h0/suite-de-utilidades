import customtkinter as ctk
from tkinter import messagebox
import threading
import requests
from bs4 import BeautifulSoup
import os

class WebScraperWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Scraping Web para WP Adictos")
        self.geometry("700x600")
        self.configure(fg_color="#f8f9fa")
        self.transient(master)
        self.grab_set()

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        # --- Cabecera ---
        header = ctk.CTkLabel(main_frame, text="Scraper para WP Adictos", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, pady=(20, 10))
        subtitle = ctk.CTkLabel(main_frame, text="Extrae artículos o recursos de una web y muestra el log en tiempo real.", text_color="#22292f")
        subtitle.grid(row=1, column=0, pady=(0, 10))

        # --- Botón de acción ---
        scrape_button = ctk.CTkButton(main_frame, text="Iniciar Scraping", command=self.start_scraping)
        scrape_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # --- Área de log/salida ---
        self.log_box = ctk.CTkTextbox(main_frame, state="disabled", fg_color="#f3f4f6")
        self.log_box.grid(row=3, column=0, sticky="nsew", padx=10, pady=(0,10))

        # --- Estado ---
        self.status_label = ctk.CTkLabel(main_frame, text="Inactivo.", text_color="#22292f")
        self.status_label.grid(row=4, column=0, sticky="w", padx=10, pady=(0,10))

    def start_scraping(self):
        self.status_label.configure(text="Procesando...", text_color="#0c7ff2")
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        threading.Thread(target=self.run_scraping).start()

    def run_scraping(self):
        try:
            url = "https://wpadictos.com/"  # Puedes cambiarlo o pedirlo al usuario
            self.append_log(f"Buscando en: {url}\n")
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')
            if not articles:
                self.append_log("No se encontraron artículos.\n")
            for i, art in enumerate(articles, 1):
                title = art.find('h2')
                if title:
                    self.append_log(f"Artículo {i}: {title.text.strip()}\n")
            self.after(0, lambda: self.status_label.configure(text="Completado.", text_color="green"))
        except Exception as e:
            self.append_log(f"Error: {e}\n")
            self.after(0, lambda: self.status_label.configure(text="Error", text_color="red"))

    def append_log(self, text):
        self.after(0, lambda: self._append_log(text))

    def _append_log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text)
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

if __name__ == '__main__':
    app = ctk.CTk()
    app.withdraw()
    window = WebScraperWindow(app)
    app.mainloop()
