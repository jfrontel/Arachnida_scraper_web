print('''
--------------------------------------------------------------------------------------------------------------
==============================================================================================================                           
                                            S C O R P I O N                                        by jfrontel
==============================================================================================================
--------------------------------------------------------------------------------------------------------------
''')

import sys
from PIL import Image
from PIL.ExifTags import TAGS

'''El segundo programa scorpion recibirá archivos de imagen como parámetros y será capaz de analizarlos en busca 
datos EXIF y otros metadatos, mostrándolos en pantalla.
El programa será compatible, al menos, con las mismas extensiones que gestiona spider.
Deberá mostrar atributos básicos como la fecha de creación, así como otros datos EXIF.
El formato en el que se muestren los metadatos queda a tu elección.
./scorpion FILE1 [FILE2 ...]'''

# ________________________________________  RUN_SPIDER: LÓGICA  _____________________________________________ #
# Por medio de los mudulos pillow y exifTags extraeremos informacion y metadatos de las imagenes introducida

def ft_scorpion(imagenes):
    for imagen in imagenes:
        try:
            imagen = Image.open(imagen)
            if imagen:
                # Mostrar los metadatos básicos de la imagen
                print(f"{'[+] Nombre de imagen':20}: {imagen.filename.split('/')[-1]}") 
                print(f"{'[+] Tipo de imagen':20}: {imagen.format}")
                print(f"{'[+] Ancho de la imagen':20}: {imagen.width} píxeres")
                print(f"{'[+] Alto de la imagen':20}: {imagen.height} píxeres")            
                print(f"{'[+] Dimensiones':20}: {imagen.size[0]} x {imagen.size[1]}")
                print(f"{'[+] Modo':20}: {imagen.mode}")
                print(f"{'[+] Paleta':20}: {imagen.getpalette()}")

                if not imagen.getexif():
                    print(f"[-] La imagen no tiene metadatos\n")
                else:
                    datos = imagen.getexif()
                    for id in datos:        # Mostrar los metadatos EXIF como "Nombre : Valor"
                        try:
                            nombre = TAGS.get(id)
                            valor = datos.get(id)
                            print(f"{nombre:20}: {valor}")
                        except Exception:
                            print(f"Tag de valor: {id} no encontrado.")
        except:
            print(f"No se pudo abrir {imagen}.")
            
if __name__ == "__main__":    
        ft_scorpion(sys.argv[1:])            
