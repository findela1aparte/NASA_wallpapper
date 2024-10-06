# Importamos dos librerías que nos van a hacer falta. La primera para poder descargar la imágen desde la web,
# la segunda para poder jugar con el sistema operativo para cambiar el fondo de pantalla.
import requests
import os

# Tenemos que colocar esta variable de entorno para que pueda funcionar el comando Crontab
os.environ["DBUS_SESSION_BUS_ADDRESS"]="unix:path=/run/user/1001/bus,guid=552ef0db6eb70d8d9c46163765ae55af"

# Creamos una variable para poder almacenar la api_key de NASA. NASA nos permite usar su api sin key 30 veces por hora, 50 veces al día
# como sólo vamos a acceder una vez al día no será necesario solicitar una API, pero si la tuviéramos deberíamos cambiarla por DEMO_KEY
params = {
    "api_key": "DEMO_KEY"
}

# En la variable r vamos a guardar la llamada a la API de la NASA, si la conexión es correcta nos devolverá un 200
# Qué es paramas=params
r = requests.get("https://api.nasa.gov/planetary/apod", params=params)

# Si la respuesta de la api es correcta (200) la guardamos en la variable "results" indicando que es formato json
# y en la variable url la direccion de la foto
if r.status_code == 200:
    results = r.json()
    url = results["url"]
    # Si es una imagen, guardar el archivo con el nombre apod.jpg, El archivo se guarda en la raiz.
    if results["media_type"] == "image":
        # La funcion with nos ayuda a abrir el archivo sin necesidad de cerrarlo
        # wb--> w es modo escritura y b modo binario, que se usa para imágenes
        with open("apod.jpg", "wb") as f:
            f.write(requests.get(url).content)
    # Si el archivo recibido es un vídeo (cosa que no creo que suceda) imprimiría la url en la terminal.
    else:
        print(url)
# Si no hay una respuesta correcta de la API imprimiría en la terminal el siguiente texto.        
else:
    print("No se pudo obtener la imagen.")

# Una vez descargada la imágen, esta sentencia le dice al SO que coloque como wallpaper el archivo indicado en la dirección de abajo
# Este comando sólo sirve para Gnome, para otro entorno deberíamos buscar la manera de hacerlo.
os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///home/ignacio/apod.jpg'")



# https://coffeebytes.dev/como-crear-un-cambiador-de-wallpaper-automatico-usando-python-en-gnome/
# https://recursospython.com/guias-y-manuales/imagenes-satelitales-nasa-apod/