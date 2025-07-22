#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
import argparse
import logging
from logging.handlers import RotatingFileHandler
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Configuración de logging
logger = logging.getLogger('yt_downloader')
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(fmt)
logger.addHandler(ch)
fh = RotatingFileHandler('yt_downloader.log', maxBytes=1e6, backupCount=3)
fh.setFormatter(fmt)
logger.addHandler(fh)

def descargar_video(url, salida, formato, nivel_log):
    logger.setLevel(getattr(logging, nivel_log))
    logger.info('----- Nueva sesión de descarga iniciada -----')
    logger.info(f'URL: {url}')
    ydl_opts = {
        'format': formato,
        'outtmpl': os.path.join(salida, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'no_warnings': True,
        'retries': 3,
        'continuedl': True,
        'progress_hooks': [lambda d: logger.debug(f"Progreso: {d.get('status')} - {d.get('downloaded_bytes')}/{d.get('total_bytes',0)} bytes")],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Interfaz gráfica
class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.create_widgets()
    def create_widgets(self):
        tk.Label(self.root, text="URL del video:").pack(pady=5)
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack(pady=5)
        tk.Label(self.root, text="Carpeta de destino:").pack(pady=5)
        self.salida_entry = tk.Entry(self.root, width=50)
        self.salida_entry.pack(pady=5)
        tk.Button(self.root, text="Seleccionar carpeta", command=self.seleccionar_carpeta).pack(pady=5)
        tk.Label(self.root, text="Formato (ej: bestvideo+bestaudio/best/mp4/mp3):").pack(pady=5)
        self.formato_entry = tk.Entry(self.root, width=30)
        self.formato_entry.insert(0, "best")
        self.formato_entry.pack(pady=5)
        tk.Button(self.root, text="Descargar", command=self.descargar).pack(pady=10)
        self.status_label = tk.Label(self.root, text="", wraplength=400)
        self.status_label.pack(pady=10)
    def seleccionar_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.salida_entry.delete(0, tk.END)
            self.salida_entry.insert(0, carpeta)
    def descargar(self):
        url = self.url_entry.get()
        salida = self.salida_entry.get() or os.getcwd()
        formato = self.formato_entry.get() or "best"
        if not url:
            messagebox.showerror("Error", "Debes ingresar una URL.")
            return
        self.status_label.config(text="Descargando...")
        threading.Thread(target=self._descargar_thread, args=(url, salida, formato)).start()
    def _descargar_thread(self, url, salida, formato):
        try:
            descargar_video(url, salida, formato, "INFO")
            self.status_label.config(text="Descarga completada.")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
