# Suite de Utilidades - Herramientas de Productividad Python

Una suite completa de utilidades para automatizar tareas diarias, incluyendo descarga avanzada de archivos, procesamiento de imágenes con OCR, transcripción de audio, web scraping y mucho más. Todo integrado en una interfaz gráfica moderna y elegante.

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
git clone https://github.com/N45h0/suite-de-utilidades.git
cd suite-de-utilidades

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

### Aplicación Principal (Suite Unificada)
```bash
python gui/main_app.py
```

### Herramientas Individuales
```bash
# Descargador avanzado de Google Drive
python gui/google_drive_downloader.py

# OCR de imágenes (individual o por lotes)
python imagen_a_texto/imagen_a_texto_individual.py

# Descarga de podcasts
python podcast_downloader/podcast_downloader.py

# Descarga de YouTube
python youtube_downloader/descargar_youtube.py
```

## 📁 Estructura del Proyecto

```
Suite de Utilidades/
├── gui/                          # Aplicaciones con interfaz gráfica unificada
│   ├── main_app.py              # Suite principal - punto de entrada
│   ├── google_drive_downloader.py # Descargador avanzado de Google Drive
│   ├── ocr_window.py            # Interfaz para OCR de imágenes
│   ├── pdf_to_markdown.py       # Conversor PDF a Markdown
│   ├── podcast_downloader_window.py # Descargador de podcasts
│   ├── youtube_downloader_window.py # Descargador de YouTube
│   ├── transcriber_window.py    # Transcriptor de audio a texto
│   ├── web_scraper_window.py    # Herramientas de web scraping
│   └── icons/                   # Iconografía de la suite
├── imagen_a_texto/              # Módulos de OCR especializados
├── podcast_downloader/          # Descarga automatizada de podcasts
├── youtube_downloader/          # Descarga de contenido de YouTube
├── gestion_imagenes/            # Procesamiento y gestión de imágenes
├── scraping/                    # Herramientas de web scraping
├── transcripciones/             # Transcripción y procesamiento de audio
└── requirements.txt             # Dependencias de la suite
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

La Suite de Utilidades está diseñada para mejorar tu productividad personal y debe usarse de manera responsable.

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

⭐ **Si te gusta la Suite de Utilidades, ¡dale una estrella en GitHub!**

🔧 **Desarrollado con ❤️ para la comunidad de desarrolladores Python**
