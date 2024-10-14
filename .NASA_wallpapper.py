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

# Colocamos fuera la variable de la imágen descargada
imagen_descargada = ""

#Colocamos el diccionario fuera de las funciones 
diccionario_meses= {"01":"Enero","02":"Febrero","03":"Marzo",
                            "04":"Abril","05":"Mayo","06":"Junio",
                            "07":"Julio","08":"Agosto","09":"Septiembre",
                            "10":"Octubre","11":"Noviembre","12":"Diciembre"}

fecha_completa= ""
dia= fecha_completa[8:10]
mes= fecha_completa[5:7]
anyo= fecha_completa[0:4]
texto_pantalla=""
        

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
        global titulo, texto_pantalla
        titulo = results["title"]
        autores = results["copyright"]
        explicacion = results["explanation"]
        texto_pantalla= (f"Título: {titulo}\nAutor: {autores} \n{explicacion}")
        
        
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
            lista_aleatorio= os.listdir('/home/ignacio/fotos_NASA') #Crea una lista con los archivos de la carpeta especificada
            foto_sustituta= random.choice(lista_aleatorio) #Elige un elemento aleatorio de la lista indicada
            while not foto_sustituta.startswith('2'):  # Repetimos mientras no empiece por '2'
                foto_sustituta = random.choice(lista_aleatorio)  # Elegimos otra imagen
            origen= Path("/home/ignacio/fotos_NASA").joinpath(foto_sustituta) #Crea una ruta con el directorio de las fotos y el archivo elegido aleatoriamente
            shutil.copy(origen ,"/home/ignacio/fotos_NASA/apod.jpg") #Copia la imágen afortunada en el archivo raíz con el nompre apod.jpg que luego subira como salvapantallas
            fecha_completa= str(foto_sustituta)
            """dia= fecha_completa[8:10]
            mes= str(fecha_completa[5:7])
            anyo= fecha_completa[0:4]"""
            texto_pantalla= (f"Hoy no hay 'Pic of the day', pero te sugerimos la foto del {dia} de {(diccionario_meses[mes])} de {anyo}.")
            
    # Si no hay una respuesta correcta de la API imprimiría en la terminal el siguiente texto.        
    else:
        print("No se pudo obtener la imagen.")
    

def refrescar_contenido():
    # Actualizamos el texto
    etiqueta_texto.config(text=texto_pantalla)

    # Actualizamos la imagen
    global imagen_descargada
    imagen_nueva = Image.open('/home/ignacio/fotos_NASA/apod.jpg')
    imagen_redimensionada = imagen_nueva.resize((300, 200))  # Redimensionar la imagen
    imagen_descargada = ImageTk.PhotoImage(imagen_redimensionada)  # Convertir la imagen redimensionada
    prew_imagen.config(image=imagen_descargada)  #Actualizar el label que muestra la imágen
    # Refrescar el texto de la etiqueta
    
def aleatoria():
    global texto_pantalla
    # Elegir una imagen aleatoria de la carpeta de la base de datos
    aleatorio = os.listdir('/home/ignacio/fotos_NASA')  # Crea una lista con los archivos de la carpeta especificada

    # Bucle para asegurarse de que la imagen elegida comience con '2'
    foto_sustituta = random.choice(aleatorio)  # Elegimos una primera opción
    while not foto_sustituta.startswith('2'):  # Repetimos mientras no empiece por '2'
        foto_sustituta = random.choice(aleatorio)  # Elegimos otra imagen

    # Ahora que tenemos una imagen que cumple la condición, continuamos
    origen = Path("/home/ignacio/fotos_NASA").joinpath(foto_sustituta)  # Crea una ruta con el archivo elegido
    shutil.copy(origen, "/home/ignacio/fotos_NASA/apod.jpg")  # Copiamos la imagen elegida

    #globals, dia, mes, anyo, diccionario_meses
    # Extraer fecha del nombre del archivo (suponiendo que el nombre es YYYY-MM-DD.jpg)
    fecha_completa = str(foto_sustituta)  # Convertimos a cadena
    dia = fecha_completa[8:10]  # Extraemos el día
    mes = str(fecha_completa[5:7])  # Extraemos el mes
    anyo = fecha_completa[0:4]  # Extraemos el año
    
    #Actualizar el texto para mostrar la fecha de la imágen aleatoria
    texto_pantalla= f"La foto que te mostramos es del {dia} de {diccionario_meses[mes]} de {anyo}."

    #Llamamos a la función refrescar que será la encargada de cambiar el texto y la imágen.
    refrescar_contenido()

# Una vez descargada la imágen, esta sentencia le dice al SO que coloque como wallpaper el archivo indicado en la dirección de abajo
# Este comando sólo sirve para Gnome, para otro entorno deberíamos buscar la manera de hacerlo.
def aplicar_wallpapper():
    #Copia la imágen desgargada y le cambia el nombre a apod2.jpg para evitar que la descarga cambie automáticamente el salvapantallas.
    shutil.copy("/home/ignacio/fotos_NASA/apod.jpg","/home/ignacio/fotos_NASA/apod2.jpg")
    os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///home/ignacio/fotos_NASA/apod2.jpg'")










#EMPIEZA LA APLICACIÓN TKINTER

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

# Le decimos que se coloque en la parte superio, pero por jerarquía se colocará después del que ya hay.
panel_medio.pack(side=TOP) 

"""   OPCIÓN CON BARRA LATERAL HORRIBLE!!!
# Crear el widget Text con la opción de altura para controlar cuántas líneas se ven (en este caso 10 líneas)
texto_largo = Text(panel_medio, wrap=WORD, height=10, width=10, font=('Dosis', 12), bg='LightBlue', fg='White')
texto_largo.insert(END, texto_pantalla)  # Insertar el texto
texto_largo.config(state=DISABLED)  # Para que el usuario no pueda modificar el texto
texto_largo.pack(side=LEFT, fill=BOTH, expand=True)

# Crear un Scrollbar (barra de desplazamiento) vertical y asociarlo al widget Text
scrollbar = Scrollbar(panel_medio, orient=VERTICAL, command=texto_largo.yview)
scrollbar.pack(side=LEFT, fill=BOTH)

# Asociar la scrollbar al widget Text
texto_largo.config(yscrollcommand=scrollbar.set)
"""
#Introducimos el formato del texto del título.
etiqueta_texto= Label(panel_medio,#Donde anidarlo
                       wraplength=350, # Longitud de envoltura en píxeles (se adapta a este ancho)
                       justify=LEFT, # Justifica el texto a la izquierda, por defecto viene centrado.
                       text= texto_pantalla, #Texto a mostrar
                       fg='White', #Color del texto
                       font=('Dosis', 10), #Tipografía y tamaño de letra
                       bg='MediumBLue', # Color de fondo
                       padx=10, 
                       pady=10) 

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

# Creamos un botón para refrescar
boton_refrescar= Button (panel_inferior, #Dónde anidamos el botón
                     text= 'Otra', #Texto que pondrá en el botón
                     font=('Dosis', 14, 'bold'), #Fuente del texto del botón y tamaño de letra
                     fg='White', #Color del texto del botón
                     bg='red', #Color del fondo del botón
                     bd=1, #Borde del botón
                     width=12, #Altura del botón
                     padx=10, 
                     pady=10,
                     command=aleatoria) # Al presionar el botón se activará la función aplicar_wallpapper

boton_refrescar.grid(row=0, column=0, padx=10, pady=10)

# Creamos un botón para el play
boton_play= Button (panel_inferior, #Dónde anidamos el botón
                     text= 'Aplicar', #Texto que pondrá en el botón
                     font=('Dosis', 14, 'bold'), #Fuente del texto del botón y tamaño de letra
                     fg='White', #Color del texto del botón
                     bg='red', #Color del fondo del botón
                     bd=1, #Borde del botón
                     width=10, #Altura del botón
                     padx=10, 
                     pady=10,
                     command=aplicar_wallpapper) # Al presionar el botón se activará la función aplicar_wallpapper

boton_play.grid(row=0, column=1, padx=10, pady= 10)
   
aplicacion.mainloop()

# https://coffeebytes.dev/como-crear-un-cambiador-de-wallpaper-automatico-usando-python-en-gnome/
# https://recursospython.com/guias-y-manuales/imagenes-satelitales-nasa-apod/