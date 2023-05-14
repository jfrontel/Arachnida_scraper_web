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

def scorpion(imagenes):
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
        scorpion(sys.argv[1:])            
