# Scripts Útiles - Colección de Herramientas Python

Una colección completa de scripts útiles para diferentes tareas automatizadas, incluyendo descarga de archivos, procesamiento de imágenes, transcripción de audio y más.

## 🚀 Características Principales

### 📥 Descargador de Google Drive Avanzado
- **Bypass de advertencias de virus** - Descarga archivos grandes que Google Drive marca con advertencias
- **Múltiples métodos de descarga** - 7 estrategias diferentes de extracción de enlaces
- **Sesión persistente** - Simula navegadores modernos con headers actualizados
- **Análisis HTML robusto** - Usa BeautifulSoup4 para parsing avanzado
- **Interfaz gráfica moderna** - Built con CustomTkinter

### 🖼️ Gestión de Imágenes
- **OCR (Reconocimiento de texto)** - Extrae texto de imágenes individuales o múltiples
- **Renombrado automático** - Genera nombres de archivo basados en contenido
- **Alt text para WordPress** - Genera descripciones automáticas para SEO
- **Generación de CSV** - Crea archivos CSV para importar a WordPress

### 🎵 Descarga de Audio
- **Descargador de podcasts** - Descarga episodios completos de podcasts
- **Transcripción de audio** - Convierte archivos de audio a texto
- **Descargador de YouTube** - Descarga videos y audio de YouTube

### 🌐 Web Scraping
- **Scraping especializado** - Herramientas para extraer contenido web
- **Compatibilidad con WordPress** - Scripts específicos para sitios WP

### 📄 Procesamiento de Documentos
- **PDF a Markdown** - Convierte documentos PDF a formato Markdown
- **Interfaz gráfica integrada** - Todas las herramientas en una aplicación unificada

## 🛠️ Instalación

### Prerrequisitos
- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Instalación rápida
```bash
# Clonar el repositorio
git clone https://github.com/tuusuario/scripts-utiles.git
cd scripts-utiles

# Crear entorno virtual
python -m venv venv311
venv311\Scripts\activate  # En Windows
# source venv311/bin/activate  # En Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias principales
- `customtkinter` - Interfaz gráfica moderna
- `requests` - Peticiones HTTP
- `beautifulsoup4` - Parsing HTML avanzado
- `Pillow` - Procesamiento de imágenes
- `pytesseract` - OCR (reconocimiento de texto)
- `yt-dlp` - Descarga de videos de YouTube
- `pydub` - Procesamiento de audio

## 🚀 Uso

### Aplicación Principal (GUI)
```bash
python gui/main_app.py
```

### Descargador de Google Drive
```bash
python gui/google_drive_downloader.py
```

### Scripts individuales
```bash
# OCR de imágenes
python imagen_a_texto/imagen_a_texto_individual.py

# Descarga de podcasts
python podcast_downloader/podcast_downloader.py

# Descarga de YouTube
python youtube_downloader/descargar_youtube.py
```

## 📁 Estructura del Proyecto

```
SCRIPTS UTILES/
├── gui/                          # Aplicaciones con interfaz gráfica
│   ├── main_app.py              # Aplicación principal unificada
│   ├── google_drive_downloader.py # Descargador avanzado de Google Drive
│   ├── ocr_window.py            # Interfaz para OCR
│   ├── pdf_to_markdown.py       # Conversor PDF a Markdown
│   └── ...
├── imagen_a_texto/              # Scripts de OCR
├── podcast_downloader/          # Descarga de podcasts
├── youtube_downloader/          # Descarga de YouTube
├── gestion_imagenes/            # Gestión y procesamiento de imágenes
├── scraping/                    # Web scraping
├── transcripciones/             # Transcripción de audio
└── requirements.txt             # Dependencias del proyecto
```

## 🔧 Características Técnicas del Descargador de Google Drive

### Técnicas Avanzadas Implementadas
- **Gestión de sesiones moderna** - Headers de Chrome 98+ con sec-ch-ua
- **Bypass de detección** - Simula comportamiento humano real
- **Parsing HTML robusto** - BeautifulSoup4 + regex como fallback
- **Múltiples estrategias de descarga**:
  1. Descarga directa
  2. Procesamiento de formularios
  3. Extracción de tokens de confirmación
  4. Bypass de advertencias de virus
  5. Método especializado para archivos multimedia
  6. Descarga de archivos compartidos
  7. URLs alternativas con parámetros aleatorios

### Manejo de Casos Especiales
- ✅ Archivos con advertencia de virus
- ✅ Archivos compartidos con restricciones
- ✅ Videos y archivos multimedia grandes
- ✅ Archivos que requieren confirmación
- ✅ Documentos con permisos especiales

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## ⚠️ Disclaimer

Estos scripts son para uso educativo y personal. Asegúrate de cumplir con los términos de servicio de las plataformas que uses y respetar los derechos de autor del contenido descargado.

## 🔍 Troubleshooting

### Problemas comunes

**Error de OCR**: Asegúrate de tener Tesseract instalado
```bash
# Windows
choco install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr
```

**Error de descarga de Google Drive**: 
- Verifica que el archivo sea público o tengas permisos
- Intenta con el método alternativo habilitado
- Algunos archivos muy grandes pueden requerir autenticación

**Error de dependencias**:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📞 Soporte

Si tienes problemas o sugerencias, por favor abre un issue en GitHub.

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub!
