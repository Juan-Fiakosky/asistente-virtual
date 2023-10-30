import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# opcion de voz
id1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"


# Escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():
    # almacenar recognizer en variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print("Ya puedes hablar")

        # guardar lo que escuche en audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="es-ar")

            # prueba de que pudo ingresar
            print("Digiste " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("Uy, no entendi")

            # devolver error
            return "sigo esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print("Uy, no hay servicio")

            # devolver error
            return "sigo esperando"

        # error inesperado
        except:

            # prueba de que no comprendio el audio
            print("Uy, algo ha salido mal")

            # devolver error
            return "sigo esperando"


# funcion para que el asistente pueda ser esuchcado
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("voice", id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():
    # crear variables con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombres de dias
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # decir el dia de la semana
    hablar(f"Hoy es {calendario[dia_semana]}")


# informar que hora es
def pedir_hora():
    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"Hi Juan, in this moment are {hora.hour} hours with {hora.minute} minutes and {hora.second} seconds"
    print(hora)

    # decir la hora
    hablar(hora)


def saludo_inciial():
    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Good night"
    elif hora.hour >= 6 or hora.hour < 13:
        momento = "Good morning"
    else:
        momento = "Good afternoon"

    # decir el saludo
    hablar(f"{momento}, Im Fernanda, your personal assistant. Tell me where I can help you?")


# funcion central del asistente
def pedir_cosas():
    # activar saludo inicial
    saludo_inciial()

    # variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if "abrir youtube" in pedido:
            hablar("Ok, Im opening youtube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "abrir navegador" in pedido:
            hablar("Ok Juan")
            webbrowser.open("https://www.google.com")
            continue
        elif "que dia es hoy" in pedido:
            pedir_dia()
            continue
        elif "que hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Searching this in wikipedia")
            pedido = pedido.replace("busca en wikipedia", " ")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar("wikipedia say:")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("ok in this moment")
            pedido = pedido.replace("busca en internet", " ")
            pywhatkit.search(pedido)
            hablar("this is finded")
            continue
        elif "reproducir" in pedido:
            hablar("Good idea, in this moment")
            pywhatkit.playonyt(pedido)
            continue
        elif "broma" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple": "APPL",
                       "amazon": "AMZN",
                       "google": "GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"La encontre, el precio de {accion} es {precio_actual}")
                continue
            except:
                hablar("Sorry, Im not find this")
                continue
        elif "adios" in pedido:
            hablar("Im going to sleep, tell me everything")
            break

pedir_cosas()
