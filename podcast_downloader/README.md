# podcast_downloader

Script para descargar episodios de un podcast desde un feed RSS, convertir el audio a texto y guardar los archivos en carpetas organizadas.

## Script
- **podcast_downloader.py**: Descarga episodios, convierte el audio a WAV y transcribe el contenido a texto.

## Requisitos
- Python 3
- Paquetes: `feedparser`, `requests`, `pydub`, `speech_recognition`
- Tesseract no es necesario para este script.

## Uso
Ejecuta el script. Los archivos descargados y transcritos se guardarán en la carpeta `podcasts`.
