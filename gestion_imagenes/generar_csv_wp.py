import pandas as pd
import os

# Ruta base donde están las imágenes originales
image_folder_path = 'C:/Users/Usuario/Downloads/Fotos glampings'

# Nombres de archivo originales y nuevos nombres propuestos
original_files = [
    'IMG-20240918-WA0128.jpg', 'IMG-20240918-WA0129.jpg', 'IMG-20240918-WA0130.jpg',
    # ...continúa la lista...
]

new_filenames = [
    'Vista-al-atardecer-desde-la-terraza.jpg', 'Espacio-de-relajacion-en-la-terraza.jpg', 'Atardecer-desde-la-terraza.jpg',
    # ...continúa la lista...
]

alt_texts = [
    'Imagen que muestra un atardecer sobre las colinas, visto desde la terraza de la cabaña en Glampings Uruguay. Se observan muebles de exterior y vegetación.',
    # ...continúa la lista...
]

data = {
    'original_filename': original_files,
    'new_filename': new_filenames,
    'alt_text': alt_texts
}

df = pd.DataFrame(data)

csv_path = 'C:/Users/Usuario/Downloads/Fotos glampings/glampings_uruguay_images.csv'
df.to_csv(csv_path, index=False)

print(f"CSV generado en: {csv_path}")
