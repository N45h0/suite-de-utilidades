# Script para descargar archivos de la carpeta wp-content de un sitio WordPress
# Mantiene la estructura de carpetas

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import random

base_url = 'https://www.wpadictos.com/wp-content/'
download_directory = 'wp-content'  # Se descarga en la carpeta local

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

def download_file(url, download_directory):
    parsed_url = urlparse(url)
    path = parsed_url.path.lstrip('/')
    local_filename = os.path.join(download_directory, path)
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
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href or href.startswith('?') or href.startswith('#'):
            continue
        full_url = urljoin(url, href)
        if href.endswith('/'):
            scrape_directory(full_url, download_directory)
        elif any(href.lower().endswith(ext) for ext in ['.jpg', '.png', '.zip', '.mp3', '.pdf', '.css', '.js']):
            download_file(full_url, download_directory)
            time.sleep(random.uniform(0.5, 2))

if __name__ == "__main__":
    scrape_directory(base_url, download_directory)
