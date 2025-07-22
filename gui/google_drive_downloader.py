import os
import re
import requests
import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
from urllib.parse import urlparse, parse_qs
import urllib.parse
import json
import time
import random
import bs4
import warnings
import tempfile

class GoogleDriveDownloader:
    def __init__(self, master=None):
        self.master = master
        
        # Configuración de la ventana
        if master:
            self.window = ctk.CTkToplevel(master)
            self.window.title("Descargador de Google Drive")
            self.window.geometry("700x500")
            self.window.resizable(True, True)
            self.window.grid_columnconfigure(0, weight=1)
            self.window.grid_rowconfigure(2, weight=1)
            
            # Variables para almacenar rutas
            self.drive_url = ""
            self.output_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            self.current_file_id = None  # Para almacenar el ID del archivo actual
            
            self.create_widgets()
    
    def create_widgets(self):
        # Frame superior para URL y opciones
        top_frame = ctk.CTkFrame(self.window)
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        top_frame.grid_columnconfigure(1, weight=1)
        
        # Entrada para URL de Google Drive
        url_label = ctk.CTkLabel(top_frame, text="URL de Google Drive:")
        url_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.url_entry = ctk.CTkEntry(top_frame, width=400)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.url_entry.bind("<Return>", lambda event: self.start_download())
        
        # Botón para pegar desde el portapapeles
        paste_btn = ctk.CTkButton(
            top_frame,
            text="Pegar",
            command=self.paste_from_clipboard,
            width=80
        )
        paste_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Carpeta de destino
        folder_label = ctk.CTkLabel(top_frame, text="Carpeta destino:")
        folder_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.folder_var = ctk.StringVar(value=self.output_folder)
        folder_display = ctk.CTkEntry(top_frame, textvariable=self.folder_var, width=400)
        folder_display.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        browse_btn = ctk.CTkButton(
            top_frame,
            text="Examinar",
            command=self.select_output_folder,
            width=80
        )
        browse_btn.grid(row=1, column=2, padx=10, pady=10)
        
        # Frame para opciones de descarga
        options_frame = ctk.CTkFrame(self.window)
        options_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Opciones de descarga
        self.rename_var = ctk.BooleanVar(value=True)
        rename_check = ctk.CTkCheckBox(
            options_frame,
            text="Renombrar automáticamente si el archivo ya existe",
            variable=self.rename_var
        )
        rename_check.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.alt_method_var = ctk.BooleanVar(value=True)
        alt_method_check = ctk.CTkCheckBox(
            options_frame,
            text="Usar método alternativo si falla la descarga normal",
            variable=self.alt_method_var
        )
        alt_method_check.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Área de log
        log_frame = ctk.CTkFrame(self.window)
        log_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(0, weight=1)
        
        self.log_text = ctk.CTkTextbox(log_frame, wrap="word")
        self.log_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.log_text.insert("1.0", "Bienvenido al Descargador de Google Drive.\n")
        self.log_text.insert("2.0", "1. Pega la URL del archivo de Google Drive que deseas descargar\n")
        self.log_text.insert("3.0", "2. Selecciona la carpeta de destino (opcional)\n")
        self.log_text.insert("4.0", "3. Haz clic en 'Descargar'\n\n")
        self.log_text.insert("5.0", "Nota: Para archivos grandes o con restricciones, es posible que necesites permisos de acceso.\n")
        
        # Barra de progreso
        progress_frame = ctk.CTkFrame(self.window)
        progress_frame.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")
        progress_frame.grid_columnconfigure(1, weight=1)
        
        progress_label = ctk.CTkLabel(progress_frame, text="Progreso:")
        progress_label.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="w")
        
        self.progress_var = ctk.DoubleVar(value=0.0)
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.progress_bar.set(0)
        
        self.progress_text = ctk.CTkLabel(progress_frame, text="0%")
        self.progress_text.grid(row=0, column=2, padx=(5, 10), pady=5, sticky="e")
        
        # Frame de botones
        button_frame = ctk.CTkFrame(self.window)
        button_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Botón para descargar
        self.download_btn = ctk.CTkButton(
            button_frame,
            text="Descargar",
            command=self.start_download,
            width=120,
            fg_color="#2ECC71",
            hover_color="#27AE60"
        )
        self.download_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Botón para cancelar
        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=self.cancel_download,
            width=120,
            fg_color="#E74C3C",
            hover_color="#C0392B"
        )
        self.cancel_btn.grid(row=0, column=1, padx=10, pady=10)
        self.cancel_btn.configure(state="disabled")
        
        # Botón para limpiar
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="Limpiar",
            command=self.clear_fields,
            width=120
        )
        self.clear_btn.grid(row=0, column=2, padx=10, pady=10)
        
        self.download_thread = None
        self.is_downloading = False
    
    def clear_fields(self):
        """Limpia los campos y reinicia el estado."""
        if not self.is_downloading:
            self.url_entry.delete(0, "end")
            self.log_text.delete("1.0", "end")
            self.log_text.insert("1.0", "Bienvenido al Descargador de Google Drive.\n")
            self.log_text.insert("2.0", "1. Pega la URL del archivo de Google Drive que deseas descargar\n")
            self.log_text.insert("3.0", "2. Selecciona la carpeta de destino (opcional)\n")
            self.log_text.insert("4.0", "3. Haz clic en 'Descargar'\n\n")
            self.log_text.insert("5.0", "Nota: Para archivos grandes o con restricciones, es posible que necesites permisos de acceso.\n")
            self.update_progress(0)
    
    def log_message(self, message):
        """Añade un mensaje al área de log."""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
    
    def paste_from_clipboard(self):
        """Pega el contenido del portapapeles en el campo de URL."""
        try:
            clipboard_text = self.window.clipboard_get()
            if clipboard_text.strip().startswith("https://drive.google.com"):
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, clipboard_text.strip())
                self.log_message("URL pegada desde el portapapeles.")
            else:
                self.log_message("El contenido del portapapeles no parece ser una URL de Google Drive.")
        except Exception as e:
            self.log_message(f"Error al acceder al portapapeles: {str(e)}")
    
    def select_output_folder(self):
        """Abre un diálogo para seleccionar la carpeta de destino."""
        folder_selected = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if folder_selected:
            self.output_folder = folder_selected
            self.folder_var.set(folder_selected)
            self.log_message(f"Carpeta de destino: {folder_selected}")
    
    def extract_file_id(self, url):
        """Extrae el ID del archivo de una URL de Google Drive."""
        # Para URLs de tipo /file/d/{ID}/
        file_id_match = re.search(r'/file/d/([^/]+)', url)
        if file_id_match:
            return file_id_match.group(1)
        
        # Para URLs de tipo ?id={ID}
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        
        if 'id' in query_params:
            return query_params['id'][0]
        
        return None
    
    def start_download(self):
        """Inicia la descarga en un hilo separado."""
        url = self.url_entry.get().strip()
        if not url:
            self.log_message("Por favor, introduce una URL de Google Drive.")
            return
        
        if not url.startswith("https://drive.google.com"):
            self.log_message("La URL no parece ser de Google Drive.")
            return
        
        file_id = self.extract_file_id(url)
        if not file_id:
            self.log_message("No se pudo extraer el ID del archivo de la URL proporcionada.")
            return
        
        self.current_file_id = file_id  # Guardar el ID del archivo actual
        self.is_downloading = True
        self.download_btn.configure(state="disabled")
        self.cancel_btn.configure(state="normal")
        
        self.download_thread = threading.Thread(target=self.download_file, args=(file_id,))
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def _get_session(self, proxy=None, use_cookies=True, user_agent=None):
        """
        Crea una sesión mejorada basada en las técnicas de gdown.
        """
        sess = requests.Session()
        
        # Configurar proxy si se proporciona
        if proxy is not None:
            sess.proxies = {"http": proxy, "https": proxy}
        
        # Configurar User-Agent (similar a gdown)
        if user_agent is None:
            # User-Agent actualizado para evitar detección
            user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
        
        # Headers mejorados
        sess.headers.update({
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"'
        })
        
        # Configurar cookies si es necesario
        if use_cookies:
            try:
                # Crear carpeta de cookies si no existe
                cache_root = os.path.join(os.path.expanduser("~"), ".cache", "gdown")
                os.makedirs(cache_root, exist_ok=True)
                
                # Archivo de cookies
                cookies_file = os.path.join(cache_root, "cookies.txt")
                
                # Si existe un archivo de cookies, cargarlo
                if os.path.exists(cookies_file):
                    try:
                        from http.cookiejar import MozillaCookieJar
                        cookie_jar = MozillaCookieJar(cookies_file)
                        cookie_jar.load(ignore_discard=True, ignore_expires=True)
                        sess.cookies.update(cookie_jar)
                        self.log_message("Cookies cargadas desde archivo local")
                    except Exception as e:
                        self.log_message(f"No se pudieron cargar cookies: {e}")
                        
            except Exception as e:
                self.log_message(f"Error configurando cookies: {e}")
        
        return sess
    
    def _get_filename_from_response(self, response):
        """Extrae el nombre del archivo desde los headers de respuesta."""
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition:
            # Buscar filename*= primero (UTF-8 encoding)
            match = re.search(r'filename\*=UTF-8\'\'([^;]+)', content_disposition)
            if match:
                try:
                    filename = urllib.parse.unquote(match.group(1))
                    return filename
                except:
                    pass
            
            # Buscar filename= clásico
            match = re.search(r'filename="?([^";]+)"?', content_disposition)
            if match:
                return match.group(1).strip('"')
        
        return None
    
    def download_file(self, file_id):
        """Descarga un archivo de Google Drive usando su ID - Versión mejorada basada en gdown."""
        try:
            # Obtener información sobre el archivo
            self.log_message(f"Obteniendo información del archivo con ID: {file_id}")
            
            # Usar el método mejorado de sesión
            sess = self._get_session(use_cookies=True)
            
            # URL base de descarga
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            # Verificar si el archivo es un recurso compartido que requiere acceso especial
            try:
                share_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
                share_response = sess.head(share_url, timeout=5)
                if share_response.status_code == 200:
                    # Intentar usar el método especializado para archivos compartidos
                    self.log_message("Detectado posible archivo compartido. Intentando método especializado...")
                    if hasattr(self, 'handle_shared_file'):
                        success, result = self.handle_shared_file(file_id)
                        if success:
                            return
                        self.log_message(f"Método para archivos compartidos falló: {result}")
            except Exception as e:
                self.log_message(f"Error al verificar si es archivo compartido: {str(e)}")
            
            # Primero intentar con el método especializado para videos (más efectivo para archivos multimedia con advertencia de virus)
            if self.alt_method_var.get():
                self.log_message("Intentando descarga con método especializado para archivos multimedia...")
                success, result = self.try_direct_download_video(file_id)
                if success:
                    return
                self.log_message(f"Método especializado falló: {result}")
            
            # Intentar descarga directa con gdown mejorado
            filename_from_url = None
            
            # Loop principal de descarga similar a gdown
            while True:
                self.log_message(f"Intentando descarga desde: {url}")
                res = sess.get(url, stream=True, verify=True)
                
                if not res.ok:
                    self.log_message(f"Error HTTP {res.status_code}: {res.reason}")
                    break
                
                # Verificar si es la descarga directa del archivo
                if "Content-Disposition" in res.headers:
                    # Tenemos el archivo
                    self.log_message("¡Descarga directa exitosa!")
                    filename_from_url = self._get_filename_from_response(res)
                    break
                
                # Verificar si necesitamos manejar confirmación
                if res.headers.get("Content-Type", "").startswith("text/html"):
                    self.log_message("Página de confirmación detectada, procesando...")
                    
                    try:
                        # Usar el método mejorado de gdown
                        url = self.get_url_from_gdrive_confirmation(res.text)
                        self.log_message(f"Nueva URL obtenida: {url}")
                        continue
                    except Exception as e:
                        self.log_message(f"Error procesando confirmación: {e}")
                        
                        # Si falla el método principal, intentar métodos de fallback
                        if self.alt_method_var.get():
                            self.log_message("Intentando métodos alternativos...")
                            
                            # Método avanzado
                            success = self.advanced_download(file_id)
                            if success:
                                return
                            
                            # Método para videos
                            success, result = self.try_direct_download_video(file_id)
                            if success:
                                return
                        
                        raise e
                else:
                    # Caso inesperado
                    self.log_message(f"Tipo de contenido inesperado: {res.headers.get('Content-Type', 'unknown')}")
                    break
            
            # Si llegamos aquí, tenemos una respuesta válida para descargar
            if "Content-Disposition" in res.headers or not res.headers.get("Content-Type", "").startswith("text/html"):
                # Determinar nombre del archivo
                if filename_from_url:
                    filename = filename_from_url
                else:
                    # Obtener nombre desde URL o usar genérico
                    filename = f"google_drive_file_{file_id}.bin"
                    
                    # Intentar obtener extensión desde Content-Type
                    content_type = res.headers.get("Content-Type", "")
                    if "video/" in content_type:
                        ext = content_type.split("/")[-1].split(";")[0]
                        filename = f"video_{file_id}.{ext}"
                    elif "audio/" in content_type:
                        ext = content_type.split("/")[-1].split(";")[0]
                        filename = f"audio_{file_id}.{ext}"
                    elif "image/" in content_type:
                        ext = content_type.split("/")[-1].split(";")[0]
                        filename = f"image_{file_id}.{ext}"
                
                # Proceder con la descarga
                self._download_file_content(res, filename)
                
            else:
                raise Exception("No se pudo obtener el archivo después de procesar confirmación")
                
        except Exception as e:
            self.log_message(f"Error durante la descarga: {str(e)}")
            self.progress_bar.set(0)
            self.progress_text.configure(text="Error")
        finally:
            self.is_downloading = False
            self.download_btn.configure(state="normal")
            self.cancel_btn.configure(state="disabled")
    
    def _download_file_content(self, response, filename):
        """Descarga el contenido del archivo desde la respuesta HTTP."""
        try:
            # Crear ruta completa del archivo
            filepath = os.path.join(self.output_folder, filename)
            
            # Verificar tamaño del archivo
            total_size = response.headers.get('Content-Length')
            if total_size:
                total_size = int(total_size)
                self.log_message(f"Tamaño del archivo: {total_size // (1024*1024)} MB")
            else:
                total_size = 0
                self.log_message("Tamaño del archivo: Desconocido")
            
            # Descargar archivo
            self.log_message(f"Descargando archivo: {filename}")
            downloaded = 0
            chunk_size = 8192  # 8KB por chunk
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if not self.is_downloading:
                        f.close()
                        os.remove(filepath)
                        raise Exception("Descarga cancelada por el usuario")
                    
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Actualizar progreso
                        if total_size > 0:
                            progress = downloaded / total_size
                            self.progress_bar.set(progress)
                            self.progress_text.configure(text=f"{int(progress * 100)}%")
                        else:
                            # Para archivos sin tamaño conocido
                            self.progress_text.configure(text=f"{downloaded // (1024*1024)} MB")
            
            self.log_message(f"Descarga completada: {filepath}")
            self.progress_bar.set(1.0)
            self.progress_text.configure(text="100%")
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Descarga completada", f"Archivo descargado exitosamente:\n{filepath}")
            
        except Exception as e:
            if "Descarga cancelada" in str(e):
                self.log_message("Descarga cancelada por el usuario")
            else:
                self.log_message(f"Error durante la descarga del contenido: {str(e)}")
            raise e

    def advanced_download(self, file_id):
        """Método avanzado para descargar archivos con restricciones"""
        try:
            self.log_message(f"Iniciando descarga avanzada para ID: {file_id}")
            
            # Crear una sesión con cookies persistentes
            session = requests.Session()
            
            # Configurar headers para simular un navegador real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Paso 1: Visitar la página de visualización primero (como lo haría un navegador)
            view_url = f"https://drive.google.com/file/d/{file_id}/view"
            self.log_message("Visitando página de visualización...")
            session.get(view_url, headers=headers)
            
            # Paso 2: Obtener información del archivo
            info_url = f"https://drive.google.com/drive/metadata?resourcekey&id={file_id}"
            info_response = session.get(info_url, headers=headers)
            
            filename = None
            try:
                # Intentar extraer el nombre del archivo desde la respuesta JSON
                json_data = info_response.text.split('\n')[1]  # Google envía un formato especial
                if json_data.startswith(")]}'\n"):
                    json_data = json_data[5:]
                data = json.loads(json_data)
                if 'fileName' in data:
                    filename = data['fileName']
            except Exception:
                pass
            
            if not filename:
                # Intentar extraer el nombre de la página de visualización
                view_response = session.get(view_url, headers=headers)
                title_match = re.search(r'<title>(.*?)(?: - Google Drive)?</title>', view_response.text)
                if title_match:
                    filename = title_match.group(1).strip()
                else:
                    filename = f"google_drive_file_{file_id}"
            
            # Limpiar el nombre de archivo
            filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
            self.log_message(f"Nombre de archivo detectado: {filename}")
            
            # Crear ruta completa
            full_path = os.path.join(self.output_folder, filename)
            
            # Manejar archivos existentes
            if os.path.exists(full_path) and self.rename_var.get():
                base_name, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(full_path):
                    new_filename = f"{base_name}_{counter}{extension}"
                    full_path = os.path.join(self.output_folder, new_filename)
                    counter += 1
                filename = os.path.basename(full_path)
                self.log_message(f"El archivo ya existe. Renombrando a: {filename}")
                
            # Paso 3: Iniciar la descarga directamente con la URL correcta para archivos que muestran advertencia
            download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
            
            # Primera solicitud para obtener cookies y el token de confirmación
            initial_response = session.get(download_url, headers=headers, stream=True)
            
            # Buscar el token de confirmación para archivos con advertencia de virus
            confirm_token = None
            
            # Método 1: Buscar en las cookies
            for cookie in session.cookies:
                if cookie.name == 'download_warning':
                    confirm_token = cookie.value
                    break
            
            # Método 2: Buscar en el HTML si no se encontró en las cookies
            if not confirm_token and 'text/html' in initial_response.headers.get('Content-Type', ''):
                html_content = initial_response.text
                token_match = re.search(r'confirm=([^&"\']+)', html_content)
                if token_match:
                    confirm_token = token_match.group(1)
            
            # Método 3: Buscar el formulario específico de confirmación
            if not confirm_token and 'text/html' in initial_response.headers.get('Content-Type', ''):
                html_content = initial_response.text
                # Buscar el formulario con acción de descarga
                form_match = re.search(r'action="([^"]+)".*?(?:id="downloadForm"|name="downloadForm")', html_content, re.DOTALL)
                if form_match:
                    action_url = form_match.group(1)
                    # Extraer token de la URL
                    token_match = re.search(r'confirm=([^&]+)', action_url)
                    if token_match:
                        confirm_token = token_match.group(1)
            
            if confirm_token:
                self.log_message(f"Token de confirmación encontrado: {confirm_token}")
                download_url = f"{download_url}&confirm={confirm_token}"
                time.sleep(1)  # Pequeña pausa para simular comportamiento humano
            
            # Intentar extraer el enlace directo de la página de confirmación
            if 'text/html' in initial_response.headers.get('Content-Type', ''):
                html_content = initial_response.text
                direct_link = self.extract_download_link_from_confirmation_page(html_content)
                if direct_link:
                    self.log_message("Enlace de descarga directa encontrado en la página de confirmación")
                    download_url = direct_link
            
            # Realizar la descarga final
            self.log_message("Iniciando descarga con método avanzado...")
            final_response = session.get(download_url, headers=headers, stream=True)
            
            # Verificar si aún recibimos HTML en lugar del archivo
            if 'text/html' in final_response.headers.get('Content-Type', ''):
                self.log_message("Advertencia: Aún recibimos HTML. Intentando método de descarga directo...")
                
                # Intentar extraer enlace directo de esta página también
                html_content = final_response.text
                
                # Verificar si es la página de advertencia de virus
                if "Virus scan warning" in html_content or "cannot be scanned for viruses" in html_content or "Descargar de todos modos" in html_content:
                    self.log_message("Detectada página de advertencia de virus.")
                    # Usar el nuevo método especializado
                    virus_response = self.handle_virus_warning(session, file_id, html_content, headers)
                    if 'text/html' not in virus_response.headers.get('Content-Type', ''):
                        final_response = virus_response
                    else:
                        self.log_message("El método especializado no funcionó. Continuando con otros métodos...")
                
                # Si no es página de virus o el método especializado no funcionó
                if 'text/html' in final_response.headers.get('Content-Type', ''):
                    # Intentar extraer enlace directo
                    direct_link = self.extract_download_link_from_confirmation_page(html_content)
                    if direct_link:
                        self.log_message("Enlace de descarga directa encontrado en la segunda página")
                        final_response = session.get(direct_link, headers=headers, stream=True)
                    else:
                        # Intentar con el método de exportación directa para ciertos tipos de archivos
                        direct_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token if confirm_token else 't'}"
                        final_response = session.get(direct_url, headers=headers, stream=True, allow_redirects=True)
                
                # Un último intento con otro parámetro de confirmación
                if 'text/html' in final_response.headers.get('Content-Type', ''):
                    final_url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t&uuid={int(time.time())}"
                    final_response = session.get(final_url, headers=headers, stream=True, allow_redirects=True)
                
                # Verificar nuevamente
                if 'text/html' in final_response.headers.get('Content-Type', ''):
                    self.log_message("Analizando HTML para extraer enlace final...")
                    html_content = final_response.text
                    if "Virus scan warning" in html_content or "cannot be scanned for viruses" in html_content:
                        self.log_message("Detectada advertencia de escaneo de virus. Intentando extraer enlace directo...")
                        direct_link = self.extract_download_link_from_confirmation_page(html_content)
                        if direct_link:
                            self.log_message("Enlace directo encontrado en la página de advertencia de virus")
                            final_response = session.get(direct_link, headers=headers, stream=True)
                    
                    # Si todavía no podemos obtener el archivo
                    if 'text/html' in final_response.headers.get('Content-Type', ''):
                        # Intentar método de descarga directa
                        self.log_message("Último intento: Método de descarga alternativo...")
                        download_urls = [
                            f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t&uuid={int(time.time())}",
                            f"https://drive.google.com/uc?id={file_id}&export=download&confirm=t&uuid={int(time.time())}",
                            f"https://docs.google.com/uc?export=download&id={file_id}&confirm=t"
                        ]
                        
                        for url in download_urls:
                            temp_response = session.get(url, headers=headers, stream=True, allow_redirects=True)
                            if 'text/html' not in temp_response.headers.get('Content-Type', ''):
                                final_response = temp_response
                                break
                        
                        # Si aún tenemos HTML, es hora de rendirse
                        if 'text/html' in final_response.headers.get('Content-Type', ''):
                            raise Exception("No se pudo obtener el archivo después de múltiples intentos")
            
            # Obtener tamaño total si está disponible
            total_size = int(final_response.headers.get('content-length', 0))
            self.log_message(f"Descargando: {filename}")
            self.log_message(f"Tamaño: {self.format_size(total_size)}" if total_size > 0 else "Tamaño desconocido")
            
            # Descargar el archivo
            downloaded_size = 0
            with open(full_path, 'wb') as f:
                for chunk in final_response.iter_content(chunk_size=8192):
                    if not self.is_downloading:
                        raise Exception("Descarga cancelada por el usuario")
                    
                    if chunk:  # Filtrar posibles keep-alive chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Actualizar progreso
                        if total_size > 0:
                            progress = downloaded_size / total_size
                            self.update_progress(progress)
                            
                            # Actualizar mensaje de estado cada ~5%
                            if total_size // 20 > 0 and downloaded_size % (total_size // 20) < 8192:
                                progress_percent = int(progress * 100)
                                self.log_message(f"Descargando... {progress_percent}% completado ({self.format_size(downloaded_size)}/{self.format_size(total_size)})")
                        else:
                            # Si no conocemos el tamaño total, actualizar cada 1MB
                            if downloaded_size % (1024 * 1024) < 8192:
                                self.log_message(f"Descargando... {self.format_size(downloaded_size)} descargados")
            
            # Verificar el archivo descargado
            if os.path.getsize(full_path) == 0:
                raise Exception("La descarga produjo un archivo vacío")
                
            # Descarga completada
            self.update_progress(1.0)
            self.log_message(f"¡Descarga completada! Archivo guardado en: {full_path}")
            
            # Preguntar si desea abrir la carpeta
            if self.master:
                if messagebox.askyesno("Descarga Completada", f"¿Desea abrir la carpeta donde se guardó el archivo?\n{os.path.dirname(full_path)}"):
                    self.open_folder(os.path.dirname(full_path))
                    
            return True
                
        except Exception as e:
            self.log_message(f"Error en descarga avanzada: {str(e)}")
            return False
    
    def format_size(self, size_bytes):
        """Formatea un tamaño en bytes a una representación legible."""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ("B", "KB", "MB", "GB", "TB")
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024
            i += 1
        
        return f"{size_bytes:.2f} {size_names[i]}"
    
    def open_folder(self, path):
        """Abre la carpeta especificada en el explorador de archivos."""
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # macOS, Linux
            if os.uname().sysname == 'Darwin':  # macOS
                os.system(f'open "{path}"')
            else:  # Linux
                os.system(f'xdg-open "{path}"')
    
    def handle_shared_file(self, file_id):
        """Método especializado para manejar archivos compartidos que requieren acceso."""
        try:
            self.log_message("Detectando como archivo compartido que requiere acceso...")
            
            # Crear una sesión con cookies persistentes
            session = requests.Session()
            
            # Headers avanzados que simulan un navegador real
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'cross-site',
                'Sec-Fetch-User': '?1'
            }
            
            # Visitar primero la página de acceso compartido
            access_url = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
            self.log_message(f"Visitando página de acceso compartido: {access_url}")
            
            response = session.get(access_url, headers=headers)
            
            # Extraer información de la página
            html_content = response.text
            
            # Buscar el nombre del archivo
            filename = None
            title_match = re.search(r'<title>(.*?)(?: - Google Drive)?</title>', html_content)
            if title_match:
                filename = title_match.group(1).strip()
            else:
                # Intentar buscar en otras partes del HTML
                name_match = re.search(r'itemName:"([^"]+)"', html_content)
                if name_match:
                    filename = name_match.group(1)
                else:
                    filename = f"shared_file_{file_id}"
            
            # Limpiar el nombre de archivo
            filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
            self.log_message(f"Archivo compartido detectado: {filename}")
            
            # Buscar URLs específicas en la página
            download_patterns = [
                r'href="(https://drive\.google\.com/uc\?export=download[^"]+id=[^"]+)"',
                r'href="(/uc\?export=download[^"]+id=[^"]+)"',
                r'downloadUrl:"([^"]+)"',
                r'id="download-form".+?action="([^"]+)"'
            ]
            
            download_url = None
            for pattern in download_patterns:
                match = re.search(pattern, html_content, re.DOTALL)
                if match:
                    download_url = match.group(1)
                    if download_url.startswith('/'):
                        download_url = f"https://drive.google.com{download_url}"
                    download_url = download_url.replace('&amp;', '&')
                    break
            
            if not download_url:
                # Si no encontramos una URL directa, construir una
                download_url = f"https://drive.google.com/uc?id={file_id}&export=download&authuser=0&confirm=t"
            
            self.log_message(f"URL de descarga para archivo compartido: {download_url}")
            
            # Intentar la descarga con la sesión que ya tiene las cookies adecuadas
            response = session.get(download_url, headers=headers, stream=True)
            
            # Verificar si obtenemos contenido real o HTML
            if 'text/html' in response.headers.get('Content-Type', ''):
                # Si recibimos HTML, es posible que necesitemos manejar una página de confirmación
                html_content = response.text
                
                # Buscar token de confirmación
                confirm_token = re.search(r'confirm=([0-9A-Za-z_-]+)', html_content)
                if confirm_token:
                    confirm_value = confirm_token.group(1)
                    download_url = f"https://drive.google.com/uc?id={file_id}&export=download&confirm={confirm_value}"
                    response = session.get(download_url, headers=headers, stream=True)
                
                # Si seguimos recibiendo HTML, intentar el enfoque para archivos con restricciones
                if 'text/html' in response.headers.get('Content-Type', ''):
                    # Intentar el método de descarga de video como último recurso
                    return self.try_direct_download_video(file_id, filename)
            
            # Crear ruta completa
            full_path = os.path.join(self.output_folder, filename)
            
            # Manejar archivos existentes
            if os.path.exists(full_path) and self.rename_var.get():
                base_name, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(full_path):
                    new_filename = f"{base_name}_{counter}{extension}"
                    full_path = os.path.join(self.output_folder, new_filename)
                    counter += 1
                filename = os.path.basename(full_path)
                self.log_message(f"El archivo ya existe. Renombrando a: {filename}")
            
            # Obtener tamaño total si está disponible
            total_size = int(response.headers.get('content-length', 0))
            self.log_message(f"Descargando archivo compartido: {filename}")
            self.log_message(f"Tamaño: {self.format_size(total_size)}" if total_size > 0 else "Tamaño desconocido")
            
            # Descargar el archivo
            downloaded_size = 0
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if not self.is_downloading:
                        raise Exception("Descarga cancelada por el usuario")
                    
                    if chunk:  # Filtrar posibles keep-alive chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Actualizar progreso
                        if total_size > 0:
                            progress = downloaded_size / total_size
                            self.update_progress(progress)
                            
                            # Actualizar mensaje de estado cada ~5%
                            if total_size // 20 > 0 and downloaded_size % (total_size // 20) < 8192:
                                progress_percent = int(progress * 100)
                                self.log_message(f"Descargando... {progress_percent}% completado ({self.format_size(downloaded_size)}/{self.format_size(total_size)})")
                        else:
                            # Si no conocemos el tamaño total, actualizar cada 1MB
                            if downloaded_size % (1024 * 1024) < 8192:
                                self.log_message(f"Descargando... {self.format_size(downloaded_size)} descargados")
            
            # Verificar el archivo descargado
            if os.path.getsize(full_path) == 0:
                return False, "El archivo descargado está vacío"
            
            # Descarga completada
            self.update_progress(1.0)
            self.log_message(f"¡Descarga completada! Archivo compartido guardado en: {full_path}")
            
            # Preguntar si desea abrir la carpeta
            if self.master:
                if messagebox.askyesno("Descarga Completada", f"¿Desea abrir la carpeta donde se guardó el archivo?\n{os.path.dirname(full_path)}"):
                    self.open_folder(os.path.dirname(full_path))
            
            return True, full_path
            
        except Exception as e:
            self.log_message(f"Error al manejar archivo compartido: {str(e)}")
            return False, str(e)

            return True, full_path
            
        except Exception as e:
            self.log_message(f"Error al manejar archivo compartido: {str(e)}")
            return False, str(e)

    def get_url_from_gdrive_confirmation(self, contents):
        """
        Método mejorado basado en gdown para extraer URL de confirmación.
        Usa técnicas más robustas de parsing HTML.
        """
        url = ""
        
        # Método 1: Buscar enlaces de descarga directa usando regex
        for line in contents.splitlines():
            m = re.search(r'href="(\/uc\?export=download[^"]+)', line)
            if m:
                url = "https://docs.google.com" + m.groups()[0]
                url = url.replace("&amp;", "&")
                break
            
            # Método 2: Usar BeautifulSoup para parsing más robusto del formulario
            soup = bs4.BeautifulSoup(line, features="html.parser")
            form = soup.select_one("#download-form")
            if form is not None and form.get("action"):
                url = form["action"].replace("&amp;", "&")
                url_components = urllib.parse.urlsplit(url)
                query_params = urllib.parse.parse_qs(url_components.query)
                
                # Extraer todos los inputs hidden del formulario
                for param in form.findChildren("input", attrs={"type": "hidden"}):
                    if param.get("name") and param.get("value"):
                        query_params[param["name"]] = param["value"]
                
                query = urllib.parse.urlencode(query_params, doseq=True)
                url = urllib.parse.urlunsplit(url_components._replace(query=query))
                break
            
            # Método 3: Buscar downloadUrl en formato JSON
            m = re.search('"downloadUrl":"([^"]+)', line)
            if m:
                url = m.groups()[0]
                url = url.replace("\\u003d", "=")
                url = url.replace("\\u0026", "&")
                break
            
            # Método 4: Buscar errores específicos
            m = re.search('<p class="uc-error-subcaption">(.*)</p>', line)
            if m:
                error = m.groups()[0]
                raise Exception(f"Error de Google Drive: {error}")
        
        # Si usamos BeautifulSoup en todo el contenido
        if not url:
            try:
                soup = bs4.BeautifulSoup(contents, features="html.parser")
                
                # Buscar formulario de descarga
                form = soup.select_one("#download-form")
                if form and form.get("action"):
                    url = form["action"].replace("&amp;", "&")
                    
                    # Obtener parámetros del formulario
                    url_components = urllib.parse.urlsplit(url)
                    query_params = urllib.parse.parse_qs(url_components.query)
                    
                    for param in form.findChildren("input", attrs={"type": "hidden"}):
                        if param.get("name") and param.get("value"):
                            query_params[param["name"]] = param["value"]
                    
                    query = urllib.parse.urlencode(query_params, doseq=True)
                    url = urllib.parse.urlunsplit(url_components._replace(query=query))
                
                # Si no encontramos formulario, buscar enlaces de descarga
                if not url:
                    download_links = soup.find_all("a", href=re.compile(r"uc\?export=download"))
                    for link in download_links:
                        href = link.get("href")
                        if href and "confirm" in href:
                            url = href.replace("&amp;", "&")
                            if not url.startswith("http"):
                                url = "https://drive.google.com" + url
                            break
                            
            except Exception as e:
                self.log_message(f"Error en parsing con BeautifulSoup: {e}")
        
        if not url:
            raise Exception(
                "No se pudo obtener el enlace de descarga. "
                "Es posible que necesites cambiar los permisos a "
                "'Cualquiera con el enlace', o que haya habido demasiados accesos."
            )
        
        return url

    def extract_download_link_from_confirmation_page(self, html_content):
        """Extrae el enlace de descarga directa desde la página de confirmación de virus."""
        try:
            return self.get_url_from_gdrive_confirmation(html_content)
        except Exception as e:
            self.log_message(f"Error en extracción con método principal: {e}")
            
        # Fallback a métodos anteriores si el nuevo falla
        # Método 1: Buscar el formulario estándar de descarga
        form_match = re.search(r'<form.+?id="downloadForm".+?action="([^"]+)".+?</form>', html_content, re.DOTALL)
        if form_match:
            action_url = form_match.group(1)
            # Decodificar URL si es necesario
            action_url = action_url.replace('&amp;', '&')
            return action_url
        
        # Método 2: Buscar enlaces con confirmación (formato más reciente)
        confirm_link = re.search(r'href="(/uc\?export=download[^"]+&confirm=[^"]+)"', html_content)
        if confirm_link:
            return "https://drive.google.com" + confirm_link.group(1).replace('&amp;', '&')
        
        # Método 3: Buscar enlaces de descarga directa
        download_link = re.search(r'href="(https://drive\.google\.com/uc\?export=download[^"]+)"', html_content)
        if download_link:
            return download_link.group(1).replace('&amp;', '&')
        
        # Método 4: Buscar cualquier formulario con acción a la URL de descarga
        any_form = re.search(r'<form.+?action="([^"]+(?:uc\?|export=download)[^"]+)".+?</form>', html_content, re.DOTALL)
        if any_form:
            return any_form.group(1).replace('&amp;', '&')
            
        # Método 5: Buscar el token de confirmación directamente
        confirm_token = re.search(r'confirm=([0-9A-Za-z_-]+)', html_content)
        if confirm_token:
            return f"https://drive.google.com/uc?export=download&id={self.current_file_id}&confirm={confirm_token.group(1)}"
            
        # Método 6: Búsqueda de patrones alternativos para formatos más recientes
        alt_confirm = re.search(r'id="download-form".+?href="([^"]+)"', html_content, re.DOTALL)
        if alt_confirm:
            href = alt_confirm.group(1).replace('&amp;', '&')
            if not href.startswith('http'):
                href = "https://drive.google.com" + href
            return href
        
        # Método 7: Buscar cualquier enlace con "export=download"
        export_links = re.findall(r'href="([^"]+export=download[^"]*)"', html_content)
        if export_links:
            for link in export_links:
                if 'confirm' in link:
                    href = link.replace('&amp;', '&')
                    if not href.startswith('http'):
                        if href.startswith('/'):
                            href = "https://drive.google.com" + href
                        else:
                            href = "https://drive.google.com/" + href
                    return href
        
        return None

    def handle_virus_warning(self, session, file_id, html_content, headers):
        """Maneja específicamente la página de advertencia de virus de Google Drive."""
        self.log_message("Detectada pantalla de advertencia de virus. Intentando bypass...")
        
        # Método 1: Extraer el enlace de confirmación directo
        direct_link = self.extract_download_link_from_confirmation_page(html_content)
        if direct_link:
            self.log_message("Enlace de confirmación encontrado. Intentando descarga directa...")
            response = session.get(direct_link, headers=headers, stream=True)
            if 'text/html' not in response.headers.get('Content-Type', ''):
                return response
                
        # Método 2: Simular clic en "Descargar de todos modos"
        download_anyway_url = None
        
        # Buscar el formulario de descarga
        form_match = re.search(r'<form[^>]*action="([^"]+)"[^>]*>', html_content)
        if form_match:
            download_anyway_url = form_match.group(1).replace('&amp;', '&')
            if not download_anyway_url.startswith('http'):
                if download_anyway_url.startswith('/'):
                    download_anyway_url = f"https://drive.google.com{download_anyway_url}"
                else:
                    download_anyway_url = f"https://drive.google.com/{download_anyway_url}"
        
            self.log_message(f"Intentando con URL de 'Descargar de todos modos': {download_anyway_url}")
            response = session.get(download_anyway_url, headers=headers, stream=True)
            if 'text/html' not in response.headers.get('Content-Type', ''):
                return response
        
        # Método 3: Usar un formato de URL conocido con el token de confirmación
        confirm_token = None
        token_match = re.search(r'confirm=([0-9A-Za-z_-]+)', html_content)
        if token_match:
            confirm_token = token_match.group(1)
            
        if confirm_token:
            self.log_message(f"Token de confirmación encontrado: {confirm_token}")
            # Probar diferentes formatos de URL
            urls_to_try = [
                f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}",
                f"https://drive.google.com/uc?id={file_id}&export=download&confirm={confirm_token}",
                f"https://drive.google.com/uc?confirm={confirm_token}&id={file_id}&export=download",
                f"https://drive.google.com/uc?export=download&confirm={confirm_token}&id={file_id}",
                f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}&authuser=0"
            ]
            
            for url in urls_to_try:
                self.log_message(f"Intentando con URL alternativa: {url}")
                response = session.get(url, headers=headers, stream=True)
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    return response
                time.sleep(1)  # Pequeña pausa entre intentos
        
        # Método 4: Probar con parámetros aleatorios adicionales
        random_uuid = int(time.time())
        final_urls = [
            f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token if confirm_token else 't'}&uuid={random_uuid}",
            f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token if confirm_token else 't'}&ts={random_uuid}",
            f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token if confirm_token else 't'}&authuser=0&uuid={random_uuid}"
        ]
        
        self.log_message("Intentando métodos adicionales con parámetros aleatorios...")
        for url in final_urls:
            response = session.get(url, headers=headers, stream=True)
            if 'text/html' not in response.headers.get('Content-Type', ''):
                return response
            time.sleep(1)  # Pequeña pausa entre intentos
        
        # Método 5: Usar el enfoque para documentos
        docs_url = f"https://docs.google.com/uc?export=download&id={file_id}&confirm={confirm_token if confirm_token else 't'}"
        self.log_message("Intentando método alternativo para documentos...")
        response = session.get(docs_url, headers=headers, stream=True)
        
        return response

    def try_direct_download_video(self, file_id, filename=None):
        """Método especializado para descargar archivos de video o audio con restricciones de virus scan."""
        try:
            self.log_message("Intentando método especializado para archivos multimedia...")
            
            # Crear una sesión con cookies persistentes
            session = requests.Session()
            
            # Configurar headers para simular un navegador de Chrome en Windows
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"'
            }
            
            # 1. Primero visitar la página del archivo para obtener cookies
            view_url = f"https://drive.google.com/file/d/{file_id}/view"
            self.log_message("Visitando página del archivo...")
            session.get(view_url, headers=headers)
            
            # 2. Obtener la página de descarga que contiene la advertencia de virus
            download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
            response = session.get(download_url, headers=headers)
            
            # Extraer token de confirmación y nombre del archivo si no se proporcionó
            if 'text/html' in response.headers.get('Content-Type', ''):
                html_content = response.text
                
                # Buscar token de confirmación
                confirm_token = None
                token_match = re.search(r'confirm=([0-9A-Za-z_-]+)', html_content)
                if token_match:
                    confirm_token = token_match.group(1)
                    self.log_message(f"Token de confirmación encontrado: {confirm_token}")
                
                # Buscar nombre del archivo si no se proporcionó
                if not filename:
                    title_match = re.search(r'<title>(.*?)(?: - Google Drive)?</title>', html_content)
                    if title_match:
                        filename = title_match.group(1).strip()
                    else:
                        filename = f"google_drive_file_{file_id}"
                    
                    # Limpiar el nombre de archivo
                    filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
                    self.log_message(f"Nombre de archivo detectado: {filename}")
            
            # Si no encontramos un token, usar valor predeterminado
            if not confirm_token:
                confirm_token = "t"
            
            # Crear ruta completa
            full_path = os.path.join(self.output_folder, filename)
            
            # Manejar archivos existentes
            if os.path.exists(full_path) and self.rename_var.get():
                base_name, extension = os.path.splitext(filename)
                counter = 1
                while os.path.exists(full_path):
                    new_filename = f"{base_name}_{counter}{extension}"
                    full_path = os.path.join(self.output_folder, new_filename)
                    counter += 1
                filename = os.path.basename(full_path)
                self.log_message(f"El archivo ya existe. Renombrando a: {filename}")
            
            # 3. Técnica especial: solicitar el archivo con el token y cabeceras adecuadas
            # Esta URL está diseñada para evitar la pantalla de advertencia
            download_url_with_token = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}"
            
            # Añadir cabeceras específicas para solicitudes de media
            media_headers = headers.copy()
            media_headers.update({
                'Range': 'bytes=0-',  # Solicitar desde el inicio
                'Accept': '*/*',  # Aceptar cualquier tipo de contenido
                'Referer': view_url,  # Establecer el referer como la página de vista
            })
            
            self.log_message("Iniciando descarga con método especializado para archivos multimedia...")
            final_response = session.get(download_url_with_token, headers=media_headers, stream=True)
            
            # Verificar si recibimos contenido de archivo real o HTML
            if 'text/html' in final_response.headers.get('Content-Type', ''):
                self.log_message("Todavía recibiendo HTML. Intentando método alternativo...")
                
                # Nueva estrategia: Intentar usar la API alternativa de Google Drive
                api_urls = [
                    f"https://drive.google.com/u/0/uc?id={file_id}&export=download&confirm={confirm_token}",
                    f"https://drive.google.com/u/1/uc?id={file_id}&export=download&confirm={confirm_token}",
                    f"https://docs.google.com/uc?export=download&id={file_id}&confirm={confirm_token}",
                    f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}&uuid={int(time.time())}"
                ]
                
                for url in api_urls:
                    self.log_message(f"Probando URL alternativa: {url}")
                    alt_response = session.get(url, headers=media_headers, stream=True)
                    if 'text/html' not in alt_response.headers.get('Content-Type', ''):
                        final_response = alt_response
                        break
                    time.sleep(1)  # Pequeña pausa entre intentos
                
                # Si seguimos recibiendo HTML, intentar extraer directamente el enlace de descarga
                if 'text/html' in final_response.headers.get('Content-Type', ''):
                    html_content = final_response.text
                    direct_link = self.extract_download_link_from_confirmation_page(html_content)
                    if direct_link:
                        self.log_message(f"Enlace de descarga directo encontrado: {direct_link}")
                        final_response = session.get(direct_link, headers=media_headers, stream=True)
            
            # Si aún tenemos HTML, intentar con un enfoque más agresivo para archivos grandes
            if 'text/html' in final_response.headers.get('Content-Type', ''):
                # Técnica para archivos muy grandes (más de 100MB)
                self.log_message("Intentando método para archivos grandes...")
                
                # Generar nuevos parámetros aleatorios
                timestamp = int(time.time())
                random_uuid = f"{timestamp}_{random.randint(1000, 9999)}"
                
                large_file_urls = [
                    f"https://drive.google.com/uc?id={file_id}&export=download&confirm={confirm_token}&uuid={random_uuid}",
                    f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}&authuser=0",
                    f"https://drive.google.com/uc?export=download&id={file_id}&confirm={confirm_token}&authuser=1"
                ]
                
                for url in large_file_urls:
                    alt_headers = headers.copy()
                    alt_headers['Cookie'] = f"download_warning_{file_id}={confirm_token}"
                    self.log_message(f"Intentando URL para archivos grandes: {url}")
                    alt_response = session.get(url, headers=alt_headers, stream=True)
                    if 'text/html' not in alt_response.headers.get('Content-Type', ''):
                        final_response = alt_response
                        break
                    time.sleep(1)
            
            # Si aún tenemos HTML, es un fallo
            if 'text/html' in final_response.headers.get('Content-Type', ''):
                return False, "No se pudo descargar el archivo, sigue recibiendo HTML."
            
            # Obtener tamaño total si está disponible
            total_size = int(final_response.headers.get('content-length', 0))
            self.log_message(f"Descargando: {filename}")
            self.log_message(f"Tamaño: {self.format_size(total_size)}" if total_size > 0 else "Tamaño desconocido")
            
            # Descargar el archivo
            downloaded_size = 0
            with open(full_path, 'wb') as f:
                for chunk in final_response.iter_content(chunk_size=8192):
                    if not self.is_downloading:
                        raise Exception("Descarga cancelada por el usuario")
                    
                    if chunk:  # Filtrar posibles keep-alive chunks
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        # Actualizar progreso
                        if total_size > 0:
                            progress = downloaded_size / total_size
                            self.update_progress(progress)
                            
                            # Actualizar mensaje de estado cada ~5%
                            if total_size // 20 > 0 and downloaded_size % (total_size // 20) < 8192:
                                progress_percent = int(progress * 100)
                                self.log_message(f"Descargando... {progress_percent}% completado ({self.format_size(downloaded_size)}/{self.format_size(total_size)})")
                        else:
                            # Si no conocemos el tamaño total, actualizar cada 1MB
                            if downloaded_size % (1024 * 1024) < 8192:
                                self.log_message(f"Descargando... {self.format_size(downloaded_size)} descargados")
            
            # Verificar el archivo descargado
            if os.path.getsize(full_path) == 0:
                return False, "La descarga produjo un archivo vacío"
                
            # Descarga completada
            self.update_progress(1.0)
            self.log_message(f"¡Descarga completada! Archivo guardado en: {full_path}")
            
            # Preguntar si desea abrir la carpeta
            if self.master:
                if messagebox.askyesno("Descarga Completada", f"¿Desea abrir la carpeta donde se guardó el archivo?\n{os.path.dirname(full_path)}"):
                    self.open_folder(os.path.dirname(full_path))
                    
            return True, full_path
                
        except Exception as e:
            self.log_message(f"Error en método especializado: {str(e)}")
            return False, str(e)

    def update_progress(self, value):
        """Actualiza la barra de progreso y el texto de porcentaje."""
        self.progress_bar.set(value)
        percent = int(value * 100)
        self.progress_text.configure(text=f"{percent}%")
    
    def cancel_download(self):
        """Cancela la descarga en curso."""
        if self.is_downloading:
            self.is_downloading = False
            self.log_message("Cancelando descarga...")

def main():
    app = ctk.CTk()
    app.title("Descargador de Google Drive")
    downloader = GoogleDriveDownloader(app)
    app.mainloop()

if __name__ == "__main__":
    main()
