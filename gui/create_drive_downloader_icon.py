from tkinter import Tk
from PIL import Image, ImageDraw
import os

# Crear una imagen de icono para el descargador de Google Drive
width, height = 64, 64
background_color = (66, 133, 244)  # Azul de Google
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)

# Dibujar un símbolo de Drive (similar al triángulo de Drive)
# Triángulo principal (esquema del logo de Drive)
points = [(16, 48), (32, 16), (48, 48)]
draw.polygon(points, fill=(255, 255, 255))

# Dibujar flecha de descarga
arrow_start = (32, 24)
arrow_end = (32, 44)
draw.line([arrow_start, arrow_end], fill=(66, 133, 244), width=4)

# Punta de flecha
arrow_head = [(26, 38), (32, 44), (38, 38)]
draw.polygon(arrow_head, fill=(66, 133, 244))

# Guardar el icono
icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
if not os.path.exists(icons_dir):
    os.makedirs(icons_dir)

icon_path = os.path.join(icons_dir, "iconogoogledrivedownloaderenpantallaprincipal.png")
image.save(icon_path)
print(f"Icono creado y guardado en: {icon_path}")
