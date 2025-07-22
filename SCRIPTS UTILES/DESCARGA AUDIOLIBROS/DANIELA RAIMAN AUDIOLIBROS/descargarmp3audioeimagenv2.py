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

# Función para convertir audio a texto
def transcribe_audio(file_path, chunk_duration_ms=600000):  # 600,000 ms = 10 minutos
    audio = AudioSegment.from_wav(file_path)
    duration_ms = len(audio)
    transcription = ""
    
    for i in range(0, duration_ms, chunk_duration_ms):
        chunk = audio[i:i + chunk_duration_ms]
        chunk_file = f"temp_chunk_{i}.wav"
        chunk.export(chunk_file, format="wav")
        
        # Procesar cada fragmento con el motor de Google
        with sr.AudioFile(chunk_file) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='es-ES')
            transcription += text + "\n"
        except sr.UnknownValueError:
            transcription += "[No se pudo transcribir este fragmento]\n"
        except sr.RequestError as e:
            transcription += f"[Error de conexión: {e}]\n"
        
        os.remove(chunk_file)  # Limpiar los archivos temporales
    
    return transcription

# Procesar los episodios en el orden en que fueron subidos (por fecha)
for entry in reversed(feed.entries):
    title = entry.title.replace("/", "-")  # Reemplaza caracteres problemáticos para el sistema de archivos
    description = entry.description
    audio_url = entry.enclosures[0]['href']
    image_url = entry.image.href if 'image' in entry else None  # Puede que algunos episodios no tengan imagen
    
    # Mostrar información
    print(f"Descargando: {title}")
    
    # Descargar el archivo MP3
    response = requests.get(audio_url)
    file_name = f"podcasts/{title}.mp3"
    
    # Verificar si el archivo se ha descargado completamente
    if len(response.content) < 1024:  # Verifica si el archivo es muy pequeño
        print(f"Error: El archivo {title}.mp3 parece estar corrupto o incompleto.")
        continue  # Salta al siguiente archivo
    
    with open(file_name, 'wb') as f:
        f.write(response.content)
    
    # Descargar la imagen si está disponible
    if image_url:
        img_response = requests.get(image_url)
        img_file = f"podcasts/{title}.jpg"
        with open(img_file, 'wb') as img_f:
            img_f.write(img_response.content)
    
    # Convertir el archivo MP3 a WAV (más fácil para la transcripción)
    try:
        audio = AudioSegment.from_mp3(file_name)
        wav_file = file_name.replace('.mp3', '.wav')
        audio.export(wav_file, format='wav')
    except CouldntDecodeError:
        print(f"Error: No se pudo decodificar {file_name}. Verifique si el archivo está corrupto.")
        continue  # Salta al siguiente archivo si hay un error
    
    # Transcribir el audio en fragmentos
    transcription = transcribe_audio(wav_file)
    
    # Guardar la transcripción en un archivo de texto
    with open(f"podcasts/{title}.txt", 'w') as txt_file:
        txt_file.write(f"Título: {title}\nDescripción: {description}\n\nTranscripción:\n{transcription}")
    
    print(f"Transcripción completada para {title}")

print("Proceso completado.")
