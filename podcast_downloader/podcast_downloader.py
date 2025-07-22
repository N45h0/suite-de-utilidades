import feedparser
import requests
import os
from pydub import AudioSegment
import speech_recognition as sr
from pydub.exceptions import CouldntDecodeError

# URL del feed RSS
feed_url = "https://anchor.fm/s/180660e0/podcast/rss"

# Parsear el RSS
feed = feedparser.parse(feed_url)

# Crear una carpeta para guardar los archivos
os.makedirs("podcasts", exist_ok=True)

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

def transcribe_audio(file_path, chunk_duration_ms=600000):
    audio = AudioSegment.from_wav(file_path)
    duration_ms = len(audio)
    transcription = ""
    for i in range(0, duration_ms, chunk_duration_ms):
        chunk = audio[i:i + chunk_duration_ms]
        chunk_file = f"temp_chunk_{i}.wav"
        chunk.export(chunk_file, format="wav")
        with sr.AudioFile(chunk_file) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='es-ES')
            transcription += text + "\n"
        except sr.UnknownValueError:
            transcription += "[No se pudo transcribir este fragmento]\n"
        except sr.RequestError as e:
            transcription += f"[Error de conexión: {e}]\n"
    return transcription

# Descargar y transcribir episodios
for entry in feed.entries:
    title = entry.title.replace("/", "-")
    audio_url = entry.enclosures[0].href if entry.enclosures else None
    if not audio_url:
        continue
    audio_path = os.path.join("podcasts", f"{title}.mp3")
    if not os.path.exists(audio_path):
        print(f"Descargando: {title}")
        r = requests.get(audio_url)
        with open(audio_path, "wb") as f:
            f.write(r.content)
    # Convertir a WAV
    wav_path = audio_path.replace(".mp3", ".wav")
    if not os.path.exists(wav_path):
        try:
            AudioSegment.from_mp3(audio_path).export(wav_path, format="wav")
        except CouldntDecodeError:
            print(f"No se pudo convertir {audio_path} a WAV.")
            continue
    # Transcribir
    txt_path = audio_path.replace(".mp3", ".txt")
    if not os.path.exists(txt_path):
        print(f"Transcribiendo: {title}")
        texto = transcribe_audio(wav_path)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(texto)
