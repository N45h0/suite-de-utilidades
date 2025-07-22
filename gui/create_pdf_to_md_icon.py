from tkinter import Tk
from PIL import Image, ImageDraw, ImageFont
import os

# Crear una imagen de icono para el extractor PDF a Markdown
width, height = 64, 64
background_color = (52, 131, 235)  # Azul para PDFs
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)

# Dibujar un símbolo de documento PDF
# Rectángulo principal (documento)
draw.rectangle([(12, 8), (52, 56)], fill=(255, 255, 255), outline=(0, 0, 0), width=2)

# Esquina doblada
draw.polygon([(42, 8), (52, 18), (42, 18)], fill=(200, 200, 200), outline=(0, 0, 0), width=1)

# Texto "PDF"
draw.text((22, 15), "PDF", fill=(255, 0, 0), stroke_width=1)

# Texto "MD"
draw.text((22, 35), "MD", fill=(0, 100, 0), stroke_width=1)

# Flecha de conversión
draw.line([(32, 28), (32, 32)], fill=(0, 0, 0), width=2)
draw.polygon([(28, 30), (32, 35), (36, 30)], fill=(0, 0, 0))

# Guardar el icono
icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
if not os.path.exists(icons_dir):
    os.makedirs(icons_dir)

icon_path = os.path.join(icons_dir, "iconopdfamarkdownenpantallaprincipal.png")
image.save(icon_path)
print(f"Icono creado y guardado en: {icon_path}")
