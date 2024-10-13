# Importamos las librerías que nos van a hacer falta. La primera para poder descargar la imágen desde la web,
import requests
import os  #Es para poder jugar con el sistema operativo para cambiar el fondo de pantalla.
import shutil #Es para poder copiar la imágen descargada a otro directorio y así teneruna base de datos
from pathlib import Path #Para poder crear rutas de archivos
import random
from tkinter import *
from PIL import ImageTk,Image #Importamos este módulo para poder trabajar con imágenes dentro de TKinter.


# Tenemos que colocar esta variable de entorno para que pueda funcionar el comando Crontab
os.environ["DBUS_SESSION_BUS_ADDRESS"]="unix:path=/run/user/1001/bus,guid=552ef0db6eb70d8d9c46163765ae55af"




def nasa():
    # Creamos una variable para poder almacenar la api_key de NASA. NASA nos permite usar su api sin key 30 veces por hora, 50 veces al día
    # como sólo vamos a acceder una vez al día no será necesario solicitar una API, pero si la tuviéramos deberíamos cambiarla por DEMO_KEY
    params = {
        "api_key": "DEMO_KEY"
    }

    # En la variable r vamos a guardar la llamada a la API de la NASA, si la conexión es correcta nos devolverá un 200
    # Qué es paramas=params
    r= requests.get("https://api.nasa.gov/planetary/apod", params=params)

    # Si la respuesta de la api es correcta (200) la guardamos en la variable "results" indicando que es formato json
    # y en la variable url la direccion de la foto
    if r.status_code == 200:
        results = r.json()
        url = results["url"]
        
        
        # Si es una imagen, guardar el archivo con el nombre apod.jpg, El archivo se guarda en la raiz.
        if results["media_type"] == "image":
            # La funcion with nos ayuda a abrir el archivo sin necesidad de cerrarlo
            # Hemos especificado que abrimos el archivo con nombre apod.jpg en la ruta elegida.
            # wb--> w es modo escritura y b modo binario, que se usa para imágenes
            with open("/home/ignacio/fotos_NASA/apod.jpg", "wb") as f:
                f.write(requests.get(url).content) 
            # Creamos una variable obteniendo la fecha de la imágen de la API y le sumamos la extensión jpg
            fecha= results["date"] + (".jpg")
            # Creamos la variable ruta a la que enviaremos las imágenes para la bbdd sumando el directorio
            ruta_destino= Path("/home/ignacio/fotos_NASA").joinpath(fecha)
            # Aquí copiamos la imágen descargada en la carpeta especidicada cambiando de nombre.
            shutil.copy("/home/ignacio/fotos_NASA/apod.jpg", ruta_destino)
        # Si el archivo recibido es un vídeo (cosa que no creo que suceda) imprimiría la url en la terminal.
        else:
            # Elegir una imágen aleatoria de la carpeta de la base de datos
            aleatorio= os.listdir('/home/ignacio/fotos_NASA') #Crea una lista con los archivos de la carpeta especificada
            foto_sustituta= random.choice(aleatorio) #Elige un elemento aleatorio de la lista indicada
            origen= Path("/home/ignacio/fotos_NASA").joinpath(foto_sustituta) #Crea una ruta con el directorio de las fotos y el archivo elegido aleatoriamente
            shutil.copy(origen ,"/home/ignacio/fotos_NASA/apod.jpg") #Copia la imágen afortunada en el archivo raíz con el nompre apod.jpg que luego subira como salvapantallas
            print(f"Hoy no hay 'Pic of the day', se ha colocado la imágen del {foto_sustituta}")
        
    # Si no hay una respuesta correcta de la API imprimiría en la terminal el siguiente texto.        
    else:
        print("No se pudo obtener la imagen.")


 # Una vez descargada la imágen, esta sentencia le dice al SO que coloque como wallpaper el archivo indicado en la dirección de abajo
    # Este comando sólo sirve para Gnome, para otro entorno deberíamos buscar la manera de hacerlo.
def aplicar_wallpapper():
    shutil.copy("/home/ignacio/fotos_NASA/apod.jpg","/home/ignacio/fotos_NASA/apod2.jpg") #Copia la imágen desgargada y le cambia el nombre a apod2.jpg para evitar que la descarga cambie automáticamente el salvapantallas.
    os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///home/ignacio/fotos_NASA/apod2.jpg'")

# Ejecutamos la aplicación Tkinter, al final del programa tenemos que poner un comando para que no se cierre la ventana
aplicacion = Tk()

# Creamos la ventana, le damos medidas en px y posición de salida.
aplicacion.geometry ('750x450+100+100')

# Con este comando impedimos que la ventana se pueda expandir o contraer por el usuario
aplicacion.resizable (0,0)

# Indicamos el título de la ventana de la aplicación
aplicacion.title ("Wallpapper Pic of the day")

# Configuramos el color de fondo de la aplicación
aplicacion.config (bg='MediumBlue')


nasa()


# Creamos un frame y le indicamos dónde se va a anidar, el grosor del borde y el tipo de borde
panel_superior= Frame(aplicacion,
                      bd=0, 
                      relief=GROOVE,
                      padx=10, 
                      pady=10,
                      bg='MediumBLue') # Color de fondo

# Colocamos el frame hueco_superior en la parte superior, como ya hay un frame que hemos puesto en la parte
# superior, este se situará justo debajo del anterior.
panel_superior.pack(side=TOP) 

# Introducimos el formato del texto del título.
etiqueta_titulo= Label(panel_superior,#Donde anidarlo
                       text='Wallpaper Pic of the day', #Texto a mostrar
                       fg='White', #Color del texto
                       font=('Dosis', 20), #Tipografía y tamaño de letra
                       bg='MediumBLue', # Color de fondo
                       width=20) #Altura del frame donde irá el texto
                        

# Colocamos el frame etiqueta_titulo en la fila 0 y columna 0
etiqueta_titulo.grid(row=0, column=0)

# Creamos un frame y le indicamos dónde se va a anidar, el grosor del borde y el tipo de borde
panel_medio= Frame(aplicacion,
                      bd=0, 
                      relief=GROOVE,
                      padx=10, 
                      pady=10,
                      bg='MediumBLue') # Color de fondo

# Colocamos el frame hueco_superior en la parte superior, como ya hay un frame que hemos puesto en la parte
# superior, este se situará justo debajo del anterior.
panel_medio.pack(side=TOP) 


# Introducimos el formato del texto del título.
etiqueta_texto= Label(panel_medio,#Donde anidarlo
                       text='Esta es la foto de hoy', #Texto a mostrar
                       fg='White', #Color del texto
                       font=('Dosis', 15), #Tipografía y tamaño de letra
                       bg='MediumBLue',
                       padx=10, 
                       pady=10) # Color de fondo

# Colocamos el frame etiqueta_titulo en la fila 0 y columna 0
etiqueta_texto.pack(side=LEFT)# Alineación a la izquierda

# Colocamos una previsualización de la imágen del día
# Redimensionamos la imagen antes de convertirla a PhotoImage
imagen = Image.open('/home/ignacio/fotos_NASA/apod.jpg')
imagen_redimensionada = imagen.resize((300, 200))  # Redimensionar la imagen
imagen_descargada = ImageTk.PhotoImage(imagen_redimensionada)  # Convertir la imagen redimensionada
prew_imagen = Label(panel_medio, image=imagen_descargada)
prew_imagen.pack(side=RIGHT,padx=10, pady=10)

# Creamos un panel infrior donde colocaremos el botón
panel_inferior= Frame(aplicacion, bd=0, relief=GROOVE)
panel_inferior.pack(side=BOTTOM)
#panel_inferior.grid(row=0, column=0)

# Creamos un botón
boton_play= Button (panel_inferior, #Dónde anidamos el botón
                     text= 'Play', #Texto que pondrá en el botón
                     font=('Dosis', 14, 'bold'), #Fuente del texto del botón y tamaño de letra
                     fg='White', #Color del texto del botón
                     bg='red', #Color del fondo del botón
                     bd=1, #Borde del botón
                     width=10, #Altura del botón
                     command=aplicar_wallpapper) # Al presionar el botón se activará la función aplicar_wallpapper

boton_play.grid(row=0, column=0)



#nasa()


   
aplicacion.mainloop()

# https://coffeebytes.dev/como-crear-un-cambiador-de-wallpaper-automatico-usando-python-en-gnome/
# https://recursospython.com/guias-y-manuales/imagenes-satelitales-nasa-apod/