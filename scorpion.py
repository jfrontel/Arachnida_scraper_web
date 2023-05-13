import sys
from PIL import Image
from PIL.ExifTags import TAGS

def scorpion(file):
    for n in file:
        try: # Abrir la imagen
            imagen = Image.open(n)
        except:    
            print('ERROR. No se pudo abrir {file}, compruebe permisos del archivo')
                     
        else: 
            if not imagen.getexif():  # Indicar si no tiene datos EXIF 
                print(f"{'Exif':32}: {imagen.getexif()}")    
                exifdata = imagen.getexif() # extrayendo metadatos
                for tag_id in exifdata:  # looping through all the tags present in exifdata
                    try:
                        tagname = TAGS.get(tag_id, tag_id) # getting the tag name instead of tag id
                        value = exifdata.get(tag_id)  # passing the tagid to get its respective value
                        print(f"{tagname:25}: {value}")
                    except Exception: 
                        print(f"Etiqueta {tag_id} no encontrada.")
            
if __name__ == "__main__":    
        scorpion(sys.argv[1:])            
