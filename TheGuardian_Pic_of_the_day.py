import bs4
import requests
import os
import shutil #Es para poder copiar la imágen descargada a otro directorio y así teneruna base de datos
from pathlib import Path #Para poder crear rutas de archivos


# Le pido que haga una llamada a la página web indicada y lo almacene en la variable resultado
resultado = requests.get("https://www.theguardian.com/news/series/ten-best-photographs-of-the-day")

# En la variable sopa introduzco en formato texto el contenido de la web en formato LXML
sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

# Introduzco en la variable entradas todas las etiquetas con la classe indicada
entradas = sopa.find_all(class_="dcr-4z6ajs")

# Creo una lista vacía donde ahora meteremos todos los elementos que ha encontrado anteriormente
lista = []

# En un bucle for va a meter en la lista un elemento por cada classe encontrada anteriormente
# Quizá podríamos quitar este paso ya que solo necesitamos el primero.
for i in entradas:
    #print(i)
    lista.append(i)

# De la lista anterior buscamos todas las entradas con la entiqueta "a" y lo pasamos a string
segunda_entrada = str(lista[0].find_all("a"))



# Aquí vamos a buscar el enlace web que necesitamos y para ello conseguiremos el texto entre la etiqueta de inicio
# "href" y la de cierre "</a>" y luego extraeremos la subcadena ajustando la posición de los carácteres
indice_inicio = segunda_entrada.index("href=")
indice_final = segunda_entrada.index("</a>")
subcadena = segunda_entrada[indice_inicio+7:indice_final-2]


segunda_dirección = "http://theguardian.com/" + subcadena
#print(segunda_dirección)


enlace_dos = requests.get(segunda_dirección)

sopa_dos = bs4.BeautifulSoup(resultado.text, 'lxml')

imagenes = sopa_dos.find_all(class_="immersive-main-media__media")

#imagen_correcta = imagenes.find(class_="immersive-main-media__media")

#imagen_seleccionada= str(imagenes[1])


#indice_inicio_imagen = imagen_seleccionada.index("https")
#indice_final_imagen = imagen_seleccionada.index('"/>')
#direccion_imagen = imagen_seleccionada[indice_inicio_imagen:indice_final_imagen]


#with open("/home/ignacio/fotos_TheGuardian/apod.jpg", "wb") as f:
#                f.write(requests.get(direccion_imagen).content)

print(imagenes)

