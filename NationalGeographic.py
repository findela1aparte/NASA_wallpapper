import bs4
import requests
import os


resultado = requests.get("https://www.theguardian.com/news/series/ten-best-photographs-of-the-day")

sopa = bs4.BeautifulSoup(resultado.text, 'lxml')

imagenes = sopa.select('img')

lista = []

for i in imagenes:
    lista.append(i)

frase = str(lista[0])
posicioninicial = frase.index('src=')+5
posicionfinal = frase.index('jpg?')+3

url = frase[posicioninicial:posicionfinal]

with open("apod.jpg", "wb") as f:
            f.write(requests.get(url).content)

os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///home/ignacio/apod.jpg'")
