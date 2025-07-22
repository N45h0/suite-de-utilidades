import os
from PIL import Image
from PIL.ExifTags import TAGS

# Cambiar el directorio donde están las imágenes
image_folder_path = 'C:/Users/Usuario/Downloads/Fotos glampings'

# Diccionario con los nombres de archivos y sus respectivos alt text
image_alt_texts = {
    'IMG-20240918-WA0125.jpg': ('tranquilidad_al_atardecer.jpg', 'Vista panorámica de la puesta de sol sobre las colinas desde el Glamping.'),
    'IMG-20240918-WA0126.jpg': ('terraza_al_atardecer.jpg', 'Terraza de madera con muebles rústicos frente a un atardecer sereno en Villa Serrana.'),
    # ...continúa el diccionario completo...
}

def add_alt_text(image_path, alt_text):
    image = Image.open(image_path)
    print(f'Archivo: {image_path} - Alt Text: "{alt_text}"')
    image.close()

for image_name, (new_name, alt_text) in image_alt_texts.items():
    image_path = os.path.join(image_folder_path, image_name)
    new_path = os.path.join(image_folder_path, new_name)
    if os.path.exists(image_path):
        os.rename(image_path, new_path)
        add_alt_text(new_path, alt_text)
    else:
        print(f"Archivo no encontrado: {image_path}")

print("Proceso completado.")
