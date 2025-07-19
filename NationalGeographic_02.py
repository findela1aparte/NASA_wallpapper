import bs4
import requests
import os
from datetime import datetime
import re
from pathlib import Path #Para poder crear rutas de archivos
import shutil #Es para poder copiar la imágen descargada a otro directorio y así teneruna base de datos


resultado = requests.get("https://www.nationalgeographic.com.es/fotografia/foto-del-dia")

sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

este_mes = datetime.today().strftime("%Y/%m/")
hoy = datetime.today().strftime("%Y_%m_%d")

# Regex para encontrar la URL que coincide
pattern = rf'https://content.nationalgeographic.com.es/medio/{este_mes}.*?.webp'

# Busca en todo el HTML convertido a texto
coincidencias = re.findall(pattern, sopa.prettify())
coincidencias_b = coincidencias[0]
coincidencias_c = coincidencias_b[0:70]

pattern = rf'{coincidencias_c}.*?.webp'
coincidencias = re.findall(pattern, sopa.prettify())

url= coincidencias[-1]


with open("/home/ignacio/fotos_NationalGeographic/apod_temp.jpg", "wb") as f:
                f.write(requests.get(url).content)

# Creamos la variable ruta a la que enviaremos las imágenes para la bbdd sumando el directorio
ruta_destino= Path("/home/ignacio/fotos_NationalGeographic").joinpath(hoy + ".jpg")
# Aquí copiamos la imágen descargada en la carpeta especidicada cambiando de nombre.
shutil.copy("/home/ignacio/fotos_NationalGeographic/apod_temp.jpg", ruta_destino)




os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///home/ignacio/apod_02.jpg'")