print('''
--------------------------------------------------------------------------------------------------------------
==============================================================================================================                           
                                                S P I D E R                                        by jfrontel
==============================================================================================================
--------------------------------------------------------------------------------------------------------------
''')

import argparse
import requests
import os
from bs4 import BeautifulSoup as sopa
from urllib.parse import urlparse
from bs4 import BeautifulSoup

'''Spider permitirá extraer todas las imágenes de un sitio web, de manera recursiva, proporcionando una url como parámetro. 
Gestionarás las siguientes opciones del programa: ./spider [-rlp] URL
• Opción -r : descarga recursivamente las imágenes de una URL recibida como parámetro.
• Opción -r -l [N] : indica el nivel profundidad máximo de la descarga recursiva. En caso de no indicarse, será 5.
• Opción -p [PATH] : indica la ruta donde se guardarán los archivos descargados. En caso de no indicarse, se utilizará ./data/.
El programa descargará por defecto las siguientes extensiones: .jpg/jpeg, .png, .gif, .bmp'''

# __________________________________________  MENÚ DE ARGUMENTOS  _____________________________________________ #
# ft_get_argument() tomará los argumentos de entrada del programa spider

def ft_get_argument():
    flag = argparse.ArgumentParser()
    flag.add_argument("url", type=str, help="URL del sitio web de donde se descargarán las imagenes")
    flag.add_argument("-r", action="store_true", help="Descarga de forma recursiva imágenes de una URL recibida como parámetro (default L=5).")
    flag.add_argument("-l", type=int, default=5, help="Indica el nivel profundidad máximo de la descarga recursiva. En caso de no indicarse, será 5.")
    flag.add_argument("-p", type=str, default="./data/", help="Indica la ruta donde se guardarán los archivos descargados. En caso de no indicarse, se utilizará ./data/.")
    print(flag.parse_args())
    args = flag.parse_args()
    print("\n", "-"*90, f"\n[+] URL analizada: {args.url}\n[+] Carpeta descarga de imagenes: {args.p}\n", "-"*90, "\n")
    return(args)

# __________________________________  MODO RECURSIVO: BUSQUEDA DE LINKS  _______________________________________ #
# ft_search_link() renera una petición get a la url dada, si todo va bien buscaremos en el contenido ya parseado 
# todos los enlaces de esa url buscado en la sopa con soup.find_all('a') formateamos cada uno de estos datos hasta 
# conseguir las url limpias que iremos guardando en lst_url_level. Si aún no se alcanzó la profundidad indicada 
# volverá a realizar la misma operación con los links encontrados esa url.

def ft_search_link(url, level):
    lst_url_level =[]
    print(f"URL={url} de nivel {level} buscando enlaces:")
    try:
        req = requests.get(url)
        if req.status_code == 200: 
            soup = BeautifulSoup(req.content, 'html.parser')
            table_web = list(soup.find_all('a'))
            for im in table_web:
                urlweb = str(im)
                format_protocol = ['https://', 'http://', 'https://www', 'http://www']
                for q in format_protocol:
                    start = 0
                    end = len(urlweb)                
                    if urlweb.find(f'a href="{q}') != -1:
                        start = urlweb.find('a href="{q}') + len('a href="{q}') - 1
                        end = urlweb.find('/"')
                        simple_urlweb = urlweb[start:end]  
                        if (simple_urlweb not in recursively_found_sites and simple_urlweb.find('"')  < 0):
                            recursively_found_sites.add(simple_urlweb)
                            lst_url_level.append(simple_urlweb)
        for url in lst_url_level:
            if level < nivel:
                print(f"link encontrado: {url} de nivel {level + 1}")     
                ft_search_link(url, level + 1)
        return lst_url_level                           
    except Exception as excepcion:
        print(excepcion.args)

# __________________________________  BUSCAR FORMATO IMAGEN Y DESCARGAR  _______________________________________ #
# ft_download_img() descarga todas las imagenes de todas las urls que se encuentren en recursively_found_sites, para ello 
# hacemos petición get y buscamos en el contenido parseado los links de esa url buscando en la sopa con soup.find_all('img') 
# formatea y deja limpia las imagenes .jpg', '.jpeg', '.png', '.gif', '.bmp'. Guarda imagenes en carpeta indicada 

def ft_search_format(table):
    i = 0
    lst_url = []
    for im in table:
        imag_1 = str(table[i])
        index_j = imag_1.find('src=') + 5
        format = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        for w in format:
            if (imag_1.find(w) != -1):
                index_z = imag_1.find(w) + 4
        if (index_j > 0 and index_z < len(imag_1) and index_z ):
            img_url = imag_1[index_j:index_z]
            lst_url.append(img_url)
        i += 1      
    return lst_url

def ft_download_img():
    for url in recursively_found_sites:
        try:
            resp = requests.get(url)
        except:
            print("Ha ocurrido un error, compruebe que ha escrito bien la url")
            exit()
        if resp.status_code == 200:
            print(f"\nConexión con {url} realizada con éxito {resp} buscando imagenes...")
            soup = BeautifulSoup(resp.content, 'html.parser')
            table_img = list(soup.find_all('img'))
            lst_url_imagen = ft_search_format(table_img)
            for img_url in lst_url_imagen:
                try:
                    resp = requests.get(img_url, timeout=5)
                except Exception as excepcion:
                    print(f"excepcion: {excepcion.args}")   
                if resp.status_code == 200:
                    nombre = img_url.split("/")[-1]
                    if nombre not in downloaded_images:
                        downloaded_images.add(nombre)
                        if not os.path.exists(args.p):
                            os.makedirs(args.p)
                        with open((args.p) + "/" + nombre, "wb") as archivo:
                            archivo.write(resp.content)
                        if nombre.find("thumb-spacer") == -1:
                            print(f"Imagen {nombre} descargada con éxito en {args.p}")

# __________________________________________  RUN_SPIDER: LÓGICA  _______________________________________________ #

def ft_run_spider():
    if rec:
        ft_search_link(url, 0)          # Buscar y extraer todos los links de la url dada
    else:
        recursively_found_sites.add(url)     # Si no existe recursividad, analiza solo la url inicial
    print("Spider se está preparando para la descarga de imágenes...")
    ft_download_img()

# __________________________________________________  MAIN  _______________________________________________________ #

global url, nivel
recursively_found_sites = set()     # Conjunto de urls encontradas.
downloaded_images = set()           # Conjunto de URLs de imágenes encontradas y descargadas

if __name__ == "__main__":
    print("Spider está comprobando los argumentos de entrada...")
    args = ft_get_argument()
    url = args.url
    nivel = args.l
    dir = args.p
    rec = args.r
    print("Argumentos introducidos correctamente...\nCargando Spider...")
    ft_run_spider()


