import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from pydub import AudioSegment
import whisper

class TranscriberWindow(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Transcriptor de Audio a Texto")
        self.geometry("700x600")
        self.configure(fg_color="#f8f9fa")
        self.transient(master)
        self.grab_set()

        self.selected_audio_path = None
        self.transcription_text = ""
        self.model = None

        # --- Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        main_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10, border_width=1, border_color="#e5e7eb")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        # --- Cabecera ---
        header = ctk.CTkLabel(main_frame, text="Transcriptor de Audio a Texto", font=ctk.CTkFont(size=24, weight="bold"), text_color="#111418")
        header.grid(row=0, column=0, pady=(20, 10))
        subtitle = ctk.CTkLabel(main_frame, text="Sube un archivo de audio y obtén la transcripción.", text_color="#22292f")
        subtitle.grid(row=1, column=0, pady=(0, 10))

        # --- Selección de archivo ---
        file_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        file_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        file_frame.grid_columnconfigure(1, weight=1)

        select_button = ctk.CTkButton(file_frame, text="Seleccionar Archivo de Audio", command=self.select_audio_file)
        select_button.grid(row=0, column=0, sticky="w")
        self.file_label = ctk.CTkLabel(file_frame, text="Ningún archivo seleccionado", text_color="#22292f")
        self.file_label.grid(row=0, column=1, sticky="w", padx=10)

        # --- Botón de transcribir ---
        transcribe_button = ctk.CTkButton(main_frame, text="Transcribir", command=self.start_transcription, height=40)
        transcribe_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # --- Progreso y estado ---
        self.status_label = ctk.CTkLabel(main_frame, text="Listo", text_color="#22292f")
        self.status_label.grid(row=4, column=0, sticky="w", padx=10)
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=5, column=0, sticky="ew", padx=10, pady=5)

        # --- Transcripción ---
        transcript_label = ctk.CTkLabel(main_frame, text="Transcripción", font=ctk.CTkFont(weight="bold"), text_color="#111418")
        transcript_label.grid(row=6, column=0, sticky="w", padx=10, pady=(10,0))
        self.transcript_box = ctk.CTkTextbox(main_frame, state="disabled", fg_color="#f3f4f6", text_color="#111418")
        self.transcript_box.grid(row=7, column=0, sticky="nsew", padx=10, pady=(0,10))

        save_button = ctk.CTkButton(main_frame, text="Guardar Transcripción", command=self.save_transcription)
        save_button.grid(row=8, column=0, sticky="e", padx=10, pady=(0,10))

    def select_audio_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav *.m4a *.opus")])
        if file_path:
            self.selected_audio_path = file_path
            self.file_label.configure(text=os.path.basename(file_path), text_color="#111418")
        else:
            self.selected_audio_path = None
            self.file_label.configure(text="Ningún archivo seleccionado", text_color="#6c757d")

    def start_transcription(self):
        if not self.selected_audio_path:
            messagebox.showwarning("Archivo no seleccionado", "Por favor, selecciona un archivo de audio.")
            return
        self.status_label.configure(text="Cargando modelo...", text_color="#6c757d")
        self.progress_bar.set(0)
        self.transcript_box.configure(state="normal")
        self.transcript_box.delete("1.0", "end")
        self.transcript_box.configure(state="disabled")
        threading.Thread(target=self.run_transcription).start()

    def run_transcription(self):
        try:
            if self.model is None:
                self.model = whisper.load_model("base")
            self.after(0, lambda: self.status_label.configure(text="Transcribiendo...", text_color="#0c7ff2"))
            audio = self.selected_audio_path
            result = self.model.transcribe(audio, language="es")
            text = result["text"]
            self.transcription_text = text
            self.after(0, lambda: self.show_transcription(text))
            self.after(0, lambda: self.status_label.configure(text="¡Listo!", text_color="green"))
            self.after(0, lambda: self.progress_bar.set(1))
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text=f"Error: {e}", text_color="red"))

    def show_transcription(self, text):
        self.transcript_box.configure(state="normal", text_color="#111418")
        self.transcript_box.delete("1.0", "end")
        self.transcript_box.insert("1.0", text)
        self.transcript_box.configure(state="disabled")

    def save_transcription(self):
        if not self.transcription_text.strip():
            messagebox.showwarning("Sin texto", "No hay transcripción para guardar.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(self.transcription_text)
            messagebox.showinfo("Guardado", f"Archivo guardado en: {save_path}")

if __name__ == '__main__':
    app = ctk.CTk()
    app.withdraw()
    window = TranscriberWindow(app)
    app.mainloop()
