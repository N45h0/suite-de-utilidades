import os
from PIL import Image
from PIL.ExifTags import TAGS

# Cambiar el directorio donde están las imágenes
image_folder_path = 'C:/Users/Usuario/Downloads/Fotos glampings'

# Diccionario con los nombres de archivos y sus respectivos alt text
image_alt_texts = {
    'IMG-20240918-WA0125.jpg': ('tranquilidad_al_atardecer.jpg', 'Vista panorámica de la puesta de sol sobre las colinas desde el Glamping.'),
    'IMG-20240918-WA0126.jpg': ('terraza_al_atardecer.jpg', 'Terraza de madera con muebles rústicos frente a un atardecer sereno en Villa Serrana.'),
    'IMG-20240918-WA0127.jpg': ('terraza_de_madera_con_vista.jpg', 'Amplia terraza de madera con vistas a las colinas y piscina al atardecer.'),
    'IMG-20240918-WA0128.jpg': ('atardecer_desde_la_terraza.jpg', 'Vista desde la terraza de un atardecer dorado sobre las colinas.'),
    'IMG-20240918-WA0129.jpg': ('escapada_al_atardecer.jpg', 'Terraza con sillones de madera bajo el cielo pintado de colores cálidos al atardecer.'),
    'IMG-20240918-WA0130.jpg': ('terraza_y_naturaleza.jpg', 'Vista de una terraza de madera rodeada de naturaleza al atardecer.'),
    'IMG-20240918-WA0131.jpg': ('puesta_de_sol_en_villa_serrana.jpg', 'La puesta de sol sobre las montañas vistas desde una terraza de madera.'),
    'IMG-20240918-WA0132.jpg': ('vista_de_la_piscina.jpg', 'Vista de la piscina al aire libre con las montañas al fondo al caer el sol.'),
    'IMG-20240918-WA0133.jpg': ('horizonte_montañoso_al_atardecer.jpg', 'Colinas ondulantes iluminadas por la luz del atardecer en Villa Serrana.'),
    'IMG-20240918-WA0134.jpg': ('cielo_pintado_al_atardecer.jpg', 'La luz dorada del atardecer pintando el cielo y la terraza de un glamping.'),
    'IMG-20240918-WA0135.jpg': ('interior_acogedor_con_vista.jpg', 'Habitación de estilo rústico con acceso directo a la terraza con vista al atardecer.'),
    'IMG-20240918-WA0136.jpg': ('piscina_bajo_el_cielo_nocturno.jpg', 'Piscina al aire libre iluminada por la luz tenue del crepúsculo.'),
    'IMG-20240918-WA0137.jpg': ('atardecer_en_la_terraza_superior.jpg', 'Vistas espectaculares desde la terraza superior durante el atardecer.'),
    'IMG-20240918-WA0138.jpg': ('terraza_al_anochecer.jpg', 'Terraza de madera bajo un cielo que oscurece, capturando la serenidad del lugar.'),
    'IMG-20240918-WA0139.jpg': ('vista_del_horizonte_desde_el_interior.jpg', 'Vista del horizonte al anochecer desde el interior de una cabaña de glamping.'),
    'IMG-20240918-WA0140.jpg': ('luz_del_atardecer_en_la_terraza.jpg', 'La luz suave del atardecer bañando la terraza de madera.'),
    'IMG-20240918-WA0141.jpg': ('puesta_de_sol_vista_desde_el_interior.jpg', 'La puesta de sol vista a través de la puerta abierta de una cabaña rústica.'),
    'IMG-20240918-WA0142.jpg': ('atardecer_desde_el_interior.jpg', 'El sol poniéndose sobre las colinas, visto desde el interior de una cabaña.'),
    'IMG-20240918-WA0143.jpg': ('luz_del_amanecer_en_el_glamping.jpg', 'Primeros rayos de sol entrando por la puerta de una cabaña rústica.'),
    'IMG-20240918-WA0144.jpg': ('ventana_con_vista_al_atardecer.jpg', 'Vista desde la ventana de una cabaña de glamping hacia el paisaje exterior al anochecer.'),
    'IMG-20240918-WA0145.jpg': ('ventana_abierta_al_atardecer.jpg', 'Vista de las colinas desde una ventana abierta en una cabaña.'),
    'IMG-20240918-WA0146.jpg': ('salon_acogedor_de_glamping.jpg', 'Amplio salón de una cabaña de glamping con sofás y decoración rústica.'),
    'IMG-20240918-WA0147.jpg': ('entrada_al_salon_principal.jpg', 'Entrada al salón principal de la cabaña, decorado en estilo rústico.'),
    'IMG-20240918-WA0148.jpg': ('salon_de_estar_rustico.jpg', 'Salón de estar en una cabaña de madera, con grandes ventanas y sofás acogedores.'),
    'IMG-20240918-WA0149.jpg': ('espacio_de_relajacion.jpg', 'Área de descanso dentro de una cabaña de glamping con vista al exterior nocturno.'),
    'IMG-20240918-WA0150.jpg': ('espacio_acogedor_al_anochecer.jpg', 'Vista desde la entrada hacia el salón principal de una cabaña, iluminado suavemente.'),
    'IMG-20240918-WA0151.jpg': ('vista_del_atardecer_desde_el_salon.jpg', 'Vista del exterior al atardecer a través de las ventanas del salón principal.'),
    'IMG-20240918-WA0152.jpg': ('refugio_de_madera_al_anochecer.jpg', 'Salón de cabaña de madera iluminado, creando un ambiente acogedor.'),
    'IMG-20240918-WA0153.jpg': ('interior_iluminado_de_noche.jpg', 'Salón de una cabaña de madera, iluminado por la luz suave de la noche.'),
    'IMG-20240918-WA0154.jpg': ('estancia_de_madera_en_la_cabaña.jpg', 'Espacio principal de una cabaña rústica, con sofás y decoración de madera.'),
    'IMG-20240918-WA0155.jpg': ('atardecer_desde_el_atico.jpg', 'Vista del atardecer desde el interior del ático de una cabaña de glamping.'),
    'IMG-20240918-WA0156.jpg': ('vista_nocturna_desde_el_atico.jpg', 'Vista nocturna desde el ático de una cabaña de glamping, con montañas al fondo.'),
    'IMG-20240918-WA0157.jpg': ('atico_rustico_con_ventana.jpg', 'Ventana abierta en el ático de una cabaña rústica con vista al exterior.')
}

# Función para agregar alt text
def add_alt_text(image_path, alt_text):
    image = Image.open(image_path)
    # No se puede añadir alt text directamente a la imagen, pero esto es una simulación de lo que se podría hacer en un entorno web.
    # Aquí simplemente estamos imprimiendo el nombre de archivo y el alt text asociado
    print(f'Archivo: {image_path} - Alt Text: "{alt_text}"')
    image.close()

# Aplicar alt text a todas las imágenes
for image_name, alt_text in image_alt_texts.items():
    image_path = os.path.join(image_folder_path, image_name)
    if os.path.exists(image_path):
        add_alt_text(image_path, alt_text)
    else:
        print(f"Archivo no encontrado: {image_path}")

print("Proceso completado.")
