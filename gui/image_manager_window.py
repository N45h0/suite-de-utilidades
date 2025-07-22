import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
import csv

class ImageManagerWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Imágenes para WordPress")
        self.geometry("700x600")
        self.configure(fg_color="#f8f9fa")
        self.transient(master)
        self.grab_set()

        self.selected_folder = None
        self.status_text = "Listo."

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # --- Cabecera ---
        header = ctk.CTkLabel(main_frame, text="Gestión de Imágenes para WordPress", font=ctk.CTkFont(size=24, weight="bold"))
        header.grid(row=0, column=0, pady=(20, 10))
        subtitle = ctk.CTkLabel(main_frame, text="Renombra imágenes, genera texto alternativo y crea CSV para WordPress.", text_color="#64748b")
        subtitle.grid(row=1, column=0, pady=(0, 10))

        # --- Pestañas ---
        self.tab_view = ctk.CTkTabview(main_frame, fg_color="transparent")
        self.tab_view.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.tab_rename = self.tab_view.add("Renombrar y Alt Text")
        self.tab_csv = self.tab_view.add("Generar CSV para WP")

        self.setup_rename_tab()
        self.setup_csv_tab()

    def setup_rename_tab(self):
        self.tab_rename.grid_columnconfigure(0, weight=1)
        folder_label = ctk.CTkLabel(self.tab_rename, text="Selecciona la carpeta con las imágenes a procesar.")
        folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        select_folder_button = ctk.CTkButton(self.tab_rename, text="Seleccionar Carpeta", command=self.select_folder)
        select_folder_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.selected_folder_label = ctk.CTkLabel(self.tab_rename, text="Carpeta no seleccionada", text_color="gray")
        self.selected_folder_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        process_button = ctk.CTkButton(self.tab_rename, text="Procesar Imágenes", command=self.process_images)
        process_button.grid(row=3, column=0, padx=10, pady=20, sticky="w")
        self.progress_bar = ctk.CTkProgressBar(self.tab_rename)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.status_label = ctk.CTkLabel(self.tab_rename, text=self.status_text)
        self.status_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

    def setup_csv_tab(self):
        self.tab_csv.grid_columnconfigure(0, weight=1)
        folder_label = ctk.CTkLabel(self.tab_csv, text="Selecciona la carpeta con imágenes y textos para generar el CSV.")
        folder_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        select_folder_button = ctk.CTkButton(self.tab_csv, text="Seleccionar Carpeta", command=self.select_folder_csv)
        select_folder_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.selected_folder_label_csv = ctk.CTkLabel(self.tab_csv, text="Carpeta no seleccionada", text_color="gray")
        self.selected_folder_label_csv.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        process_button = ctk.CTkButton(self.tab_csv, text="Generar CSV", command=self.generate_csv)
        process_button.grid(row=3, column=0, padx=10, pady=20, sticky="w")
        self.status_label_csv = ctk.CTkLabel(self.tab_csv, text="Listo.")
        self.status_label_csv.grid(row=4, column=0, padx=10, pady=5, sticky="w")

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder = folder_path
            self.selected_folder_label.configure(text=folder_path)

    def process_images(self):
        if not self.selected_folder or not os.path.isdir(self.selected_folder):
            self.status_label.configure(text="Por favor, selecciona una carpeta válida.", text_color="orange")
            return
        self.status_label.configure(text="Procesando imágenes...", text_color="black")
        self.progress_bar.set(0)
        threading.Thread(target=self.run_rename_and_alt, args=(self.selected_folder,)).start()

    def run_rename_and_alt(self, folder_path):
        try:
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            if not image_files:
                self.after(0, lambda: self.status_label.configure(text="No se encontraron imágenes.", text_color="orange"))
                return
            for i, filename in enumerate(image_files, 1):
                old_path = os.path.join(folder_path, filename)
                # Renombrar: ejemplo simple, puedes personalizar
                new_name = f"imagen_{i}{os.path.splitext(filename)[1]}"
                new_path = os.path.join(folder_path, new_name)
                os.rename(old_path, new_path)
                # Generar alt text (simple)
                alt_text = f"Imagen número {i} para WordPress"
                with open(new_path + ".txt", "w", encoding="utf-8") as f:
                    f.write(alt_text)
                progress = i / len(image_files)
                self.after(0, lambda p=progress: self.progress_bar.set(p))
            self.after(0, lambda: self.status_label.configure(text="Imágenes renombradas y alt text generado.", text_color="green"))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {e}", text_color="red"))

    def select_folder_csv(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder_label_csv.configure(text=folder_path)

    def generate_csv(self):
        folder_path = self.selected_folder_label_csv.cget("text")
        if not os.path.isdir(folder_path):
            self.status_label_csv.configure(text="Por favor, selecciona una carpeta válida.", text_color="orange")
            return
        self.status_label_csv.configure(text="Generando CSV...", text_color="black")
        threading.Thread(target=self.run_generate_csv, args=(folder_path,)).start()

    def run_generate_csv(self, folder_path):
        try:
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
            if not image_files:
                self.after(0, lambda: self.status_label_csv.configure(text="No se encontraron imágenes.", text_color="orange"))
                return
            csv_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
            if not csv_path:
                self.after(0, lambda: self.status_label_csv.configure(text="Proceso cancelado.", text_color="orange"))
                return
            with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["imagen", "alt_text"])
                for filename in image_files:
                    img_path = os.path.join(folder_path, filename)
                    txt_path = img_path + ".txt"
                    alt_text = ""
                    if os.path.exists(txt_path):
                        with open(txt_path, "r", encoding="utf-8") as f:
                            alt_text = f.read().strip()
                    writer.writerow([filename, alt_text])
            self.after(0, lambda: self.status_label_csv.configure(text=f"CSV generado en: {csv_path}", text_color="green"))
        except Exception as e:
            self.after(0, lambda: self.status_label_csv.configure(text=f"Error: {e}", text_color="red"))

if __name__ == '__main__':
    app = ctk.CTk()
    app.withdraw()
    window = ImageManagerWindow(app)
    app.mainloop()
