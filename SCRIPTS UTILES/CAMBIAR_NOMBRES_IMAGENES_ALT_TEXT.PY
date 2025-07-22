import pandas as pd
import os

# Ruta base donde están las imágenes originales
image_folder_path = 'C:/Users/Usuario/Downloads/Fotos glampings'

# Nombres de archivo originales y nuevos nombres propuestos
original_files = [
    'IMG-20240918-WA0128.jpg', 'IMG-20240918-WA0129.jpg', 'IMG-20240918-WA0130.jpg',
    'IMG-20240918-WA0131.jpg', 'IMG-20240918-WA0132.jpg', 'IMG-20240918-WA0133.jpg',
    'IMG-20240918-WA0134.jpg', 'IMG-20240918-WA0135.jpg', 'IMG-20240918-WA0136.jpg',
    'IMG-20240918-WA0137.jpg', 'IMG-20240918-WA0138.jpg', 'IMG-20240918-WA0139.jpg',
    'IMG-20240918-WA0140.jpg', 'IMG-20240918-WA0141.jpg', 'IMG-20240918-WA0142.jpg',
    'IMG-20240918-WA0143.jpg', 'IMG-20240918-WA0144.jpg', 'IMG-20240918-WA0145.jpg',
    'IMG-20240918-WA0146.jpg', 'IMG-20240918-WA0147.jpg', 'IMG-20240918-WA0148.jpg',
    'IMG-20240918-WA0149.jpg'
]

new_filenames = [
    'Vista-al-atardecer-desde-la-terraza.jpg', 'Espacio-de-relajacion-en-la-terraza.jpg', 'Atardecer-desde-la-terraza.jpg',
    'Terraza-al-atardecer.jpg', 'Terraza-con-vistas-al-atardecer.jpg', 'Relax-en-la-terraza-de-madera.jpg',
    'Vista-de-la-piscina-desde-la-terraza.jpg', 'Atardecer-con-vistas-a-la-piscina.jpg', 'Colinas-al-atardecer.jpg',
    'Despedida-del-dia-en-Glampings-Uruguay.jpg', 'Interior-acogedor-con-vistas-al-atardecer.jpg', 
    'Piscina-bajo-el-cielo-del-atardecer.jpg', 'Terraza-con-vistas-despejadas-al-atardecer.jpg', 
    'Puerta-abierta-hacia-el-atardecer.jpg', 'Atardecer-desde-la-puerta.jpg', 'Vistas-al-atardecer-desde-la-ventana.jpg',
    'Ventana-abierta-al-paisaje-nocturno.jpg', 'Sala-de-estar-con-diseno-rustico.jpg', 'Entrada-a-una-sala-de-estar-rustica.jpg',
    'Sala-de-estar-acogedora-al-anochecer.jpg', 'Sala-de-estar-con-ventanas-panoramicas.jpg', 'Comodidad-rustica-en-Glampings-Uruguay.jpg'
]

alt_texts = [
    'Imagen que muestra un atardecer sobre las colinas, visto desde la terraza de la cabaña en Glampings Uruguay. Se observan muebles de exterior y vegetación.',
    'Terraza de madera con sillas de madera rústica, rodeada de naturaleza, perfecta para disfrutar de un atardecer en Glampings Uruguay.',
    'Imagen de una terraza con vistas despejadas hacia las colinas al atardecer, mostrando una atmósfera tranquila en Glampings Uruguay.',
    'Vista lateral de una terraza con muebles rústicos de madera, al fondo un cielo con los últimos rayos de sol, en Glampings Uruguay.',
    'Imagen de una terraza elevada de madera, con vistas a un paisaje natural en el atardecer, ubicada en Glampings Uruguay.',
    'Terraza rústica de madera con sillas y mesa, con vistas a la naturaleza al atardecer, parte de las comodidades de Glampings Uruguay.',
    'Imagen de la piscina circular vista desde la terraza al atardecer en Glampings Uruguay, con colinas y vegetación de fondo.',
    'Vista panorámica del paisaje con colinas y piscina al atardecer desde la terraza en Glampings Uruguay.',
    'Vista amplia de colinas y vegetación al atardecer desde la terraza de Glampings Uruguay.',
    'Vista lateral desde la terraza al atardecer en Glampings Uruguay, mostrando el cielo en tonos anaranjados.',
    'Imagen del interior de una cabaña en Glampings Uruguay, con una puerta abierta hacia la terraza y una guitarra en una cama.',
    'Imagen panorámica de la piscina y el paisaje natural al atardecer en Glampings Uruguay.',
    'Terraza de madera con vistas a las colinas y la piscina al atardecer en Glampings Uruguay.',
    'Imagen del interior de la cabaña con la puerta abierta hacia la terraza, dejando entrar la luz del atardecer en Glampings Uruguay.',
    'Vista parcial desde el interior de la cabaña hacia la terraza al atardecer en Glampings Uruguay.',
    'Imagen del interior de la cabaña en Glampings Uruguay, mostrando una ventana abierta con vistas a las colinas al atardecer.',
    'Vista desde el interior de la cabaña en Glampings Uruguay, mostrando la ventana abierta al caer la noche.',
    'Sala de estar de una cabaña en Glampings Uruguay, con sofás rústicos y ventanas grandes, ofreciendo un ambiente acogedor.',
    'Vista de la entrada hacia una sala de estar rústica en Glampings Uruguay, con detalles en madera y piedras naturales.',
    'Sala de estar rústica con sofás y detalles de madera, iluminada sutilmente al anochecer en Glampings Uruguay.',
    'Imagen de la sala de estar en una cabaña de Glampings Uruguay, con grandes ventanas que ofrecen vistas al exterior.',
    'Sala de estar rústica con sofás y ambiente acogedor, parte del alojamiento en Glampings Uruguay.'
]

# Crear dataframe con la información
data = {
    'original_filename': original_files,
    'new_filename': new_filenames,
    'alt_text': alt_texts
}

df = pd.DataFrame(data)

# Cambiar los nombres de los archivos en el sistema
for original, new in zip(original_files, new_filenames):
    original_path = os.path.join(image_folder_path, original)
    new_path = os.path.join(image_folder_path, new)
    os.rename(original_path, new_path)

# Crear CSV para WP All Import y subir en Wordpress
csv_path = 'C:/Users/Usuario/Downloads/Fotos glampings/glampings_uruguay_images.csv'
df.to_csv(csv_path, index=False)

csv_path
