import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random

# URL base de la carpeta wp-content
base_url = 'https://www.wpadictos.com/wp-content/'
download_directory = 'C:/Users/Usuario/Desktop/SCRIPTS UTILES/scrappingwpadictos/wp-content'  # Cambia esta ruta según tu entorno

# Crear el directorio de descarga si no existe
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

def download_file(url, download_directory):
    parsed_url = urlparse(url)
    path = parsed_url.path.lstrip('/')  # Eliminar la barra inicial
    local_filename = os.path.join(download_directory, path)
    
    # Crear directorios necesarios
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Descargado: {local_filename}")
    return local_filename

def scrape_directory(url, download_directory):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Encuentra todos los enlaces en la página
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('/'):
            # Es una subcarpeta, recursion
            new_url = urljoin(url, href)
            print(f"Entrando en subcarpeta: {new_url}")
            scrape_directory(new_url, download_directory)
        elif any(href.endswith(ext) for ext in ['.jpg', '.png', '.css', '.js', '.woff', '.woff2', '.ttf', '.svg']):
            # Es un archivo, descargar
            file_url = urljoin(url, href)
            print(f"Iniciando descarga de: {file_url}")
            download_file(file_url, download_directory)
            
            # Pausa aleatoria entre 1 y 5 segundos
            pause_duration = random.uniform(1, 5)
            print(f"Pausa por {pause_duration:.2f} segundos para evitar ser detectado...")
            time.sleep(pause_duration)

# Comienza el scraping desde la URL base
print(f"Iniciando scraping en {base_url}")
scrape_directory(base_url, download_directory)
print("Proceso de scraping completado.")
