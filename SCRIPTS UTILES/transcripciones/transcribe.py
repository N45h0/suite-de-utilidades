import whisper
import sys

def transcribir_audio(ruta_audio):
    """
    Función para transcribir un archivo de audio a texto.
    
    Parámetros:
    - ruta_audio: ruta al archivo de audio (por ejemplo, 'audio.wav')

    Retorna:
    - Transcripción en texto.
    """
    # Cargar el modelo (puedes elegir entre "tiny", "base", "small", "medium" o "large")
    modelo = whisper.load_model("base")
    
    # Transcribir el audio. Especificamos "es" para indicar el idioma español.
    resultado = modelo.transcribe(ruta_audio, language="es")
    return resultado["text"]

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python transcribe.py ruta_al_audio.wav")
        sys.exit(1)
        
    ruta_audio = sys.argv[1]
    texto_transcrito = transcribir_audio(ruta_audio)
    
    print("Transcripción:")
    print(texto_transcrito)
