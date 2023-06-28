import numpy as np #Importamos NumPy para todo el tema que tiene que ver con números dentro de nuestro código (puntajes)
import pygame #Pygame es una libreria que se explica en el repo, pero en pocas palabras nos ayuda con la creación de la interfaz para el juego
import pygame.font #Importa todas las fuentes para el juego
from pygame.locals import * # Proporciona constantes y eventos predefinidos que son útiles para interactuar

pygame.init() #Inicia el juego

width = 400 #Dimensiones de las ventana que se abre al momento de ejecutar
height = 400
blanco = (255, 255, 255)

fuente = pygame.font.Font(None, 75) #Fuente del texto de la pantalla
#Se colocan todas las variables que se van a utilizar y se inicializan en 0 o vacías dependiendo el caso
jugadores = 0
estados1 = []
estados2 = []
intentos1 = 0
intentos2 = 0
r_idx = 0
palabra = ''
enigma = ''
nivelp = 0
pasos = []
#Se desprende la ventana para comenzar el juego
ventana = pygame.display.set_mode((width, height)) 
i = 0
j = 0
puntaje = 0
puntaje2 = 0
def ingresar(texto): # Esta función se utiliza para solicitar al usuario que ingrese texto desde el teclado.
    input_text = '' #Esta variable se utilizará para almacenar el texto ingresado por el usuario.
    print(texto) # Esta línea imprime en la consola el texto pasado como parámetro a la función ingresar
    writing = True #Esta variable se utiliza para controlar un bucle mientras el usuario está escribiendo.
    while writing: #Se define el bucle
        for evento in pygame.event.get(): #Se utiliza pygame.event.get() para obtener los eventos que ocurren en la ventana del juego.
            if evento.type == pygame.QUIT: #Se coloca esto en caso de que el usuario intente cerrar el programa, entonces se detendrá la ejecución del programa
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN: #Si se detecta un evento de tipo pygame.KEYDOWN, significa que el usuario ha presionado una tecla
                if evento.key == pygame.K_RETURN or evento.key == K_KP_ENTER: #Si se presiona la tecla "Return" o "Enter" se establece writing en False para salir del bucle y finalizar la entrada de texto.
                    writing = False
                    print('')
                elif evento.key == pygame.K_BACKSPACE: #Si se presiona la tecla de retroceso, se elimina el último carácter de la cadena input_text y se imprime el resultado actualizado en la consola.
                    input_text = input_text[:-1]
                    print(input_text + " ", end='\r')
                elif evento.unicode.isprintable(): #Si se presiona cualquier otra tecla imprimible, se agrega el carácter a la cadena input_text y se imprime el resultado actualizado en la consola.
                    input_text += evento.unicode 
                    print(input_text, end='\r') #El 'end='\r'' funciona para sobrescribir sobre la línea actual

    return input_text #Retorna el resultado final, dependiendo de lo que se ingreso en el teclado



"""
Cada línea de código pygame.draw.line o pygame.draw.circle 
dibuja una parte específica del ahorcado en la ventana de 
Pygame, utilizando las coordenadas y dimensiones proporcionadas. 
La función pygame.draw.line dibuja una línea recta, mientras que pygame.draw.circle 
dibuja un círculo.

El estado de cada parte del dibujo se determina según los valores en la 
lista estados. Si el valor correspondiente en estados es 1, se dibuja la 
parte del ahorcado en la ventana; de lo contrario, si es 0, la parte no se dibuja.
"""
def hangman(centro, estados, s): #Función para dibujar el muñequito del ahorcado
    if estados[0] == 1:
        pygame.draw.circle(ventana, (blanco), (centro[0], centro[1]), s, 3)
    if estados[1] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0], centro[1] + s), (centro[0], centro[1] + 2 * s), 3)
    if estados[2] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0], centro[1] + s), (centro[0] - s , centro[1] + 2 * s), 3)
    if estados[3] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0], centro[1] + s), (centro[0] + s , centro[1] + 2 * s), 3)
    if estados[4] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0], centro[1] + 2 * s), (centro[0] - s , centro[1] + 3 * s), 3)
    if estados[5] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0], centro[1] + 2 * s), (centro[0] + s , centro[1] + 3 * s), 3)
    if estados[6] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0] - 4 * s, centro[1] + 5 * s), (centro[0] + 3 * s , centro[1] + 5 * s), 3)
    if estados[7] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0] - 2 * s, centro[1] + 5 * s), (centro[0] - 2 * s , centro[1] - 3 * s), 3)
    if estados[8] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0] - 3 * s, centro[1] - 2 * s), (centro[0] + 2 * s , centro[1] - 2 * s), 3)
    if estados[9] == 1:
        pygame.draw.line(ventana, (blanco), (centro[0], centro[1] - 2 * s), (centro[0], centro[1] - s), 3)

def escribir(texto, centro):
    #La variable text_surface almacena la superficie generada que contiene el texto renderizado.
    text_surface = fuente.render(texto, True, blanco) #La función render se utiliza para generar una superficie que contiene el texto renderizado, utilizando la fuente especificada.
    text_rect = text_surface.get_rect() #Se llama al método get_rect() en la superficie text_surface para obtener un rectángulo que representa el área ocupada por el texto en la superficie.
    text_rect.center = centro # Hace que el centro del rectángulo coincida con las coordenadas centro proporcionadas.

    ventana.blit(text_surface, text_rect) 

def reducir(texto): #Esta función nos ayuda a reemplazar todas las vocales que tienen tilde para que no tengan tilde Y que este en minúscula
    return texto.lower().replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ü', 'u')

def ocurrencias(caracter, texto):
    texto = reducir(texto)
    indices = [i for i, c in enumerate(texto) if c == caracter]
    return indices 




"""
La función nivel(texto) calcula el nivel de dificultad
del juego, elimina los espacios en blanco y cuenta la cantidad 
de caracteres únicos que quedan después de este procesamiento.
"""
def nivel(texto):

    texto = reducir(texto).replace(' ', '')#Elimina todos los espacios en blanco 
    return len(set(texto)) #se aplica el método set(texto) para obtener un conjunto de caracteres únicos presentes en el texto.

"""
Finalmente, se devuelve la longitud de este conjunto de caracteres 
únicos utilizando la función len(). Esto indica el nivel del texto,
que es la cantidad de caracteres únicos presentes en él después de 
aplicar el procesamiento y eliminar los espacios en blanco.
"""



"""
La función pasos_dibujo(nivel) asigna diferentes rangos 
de pasos del dibujo del muñeco del ahorcado según el nivel 
proporcionado, y devuelve una lista de tuplas que representan estos pasos.
"""
def pasos_dibujo(nivel):
    p = []
    if nivel <= 3:
        p = [(0, 6), (6, 9), (9, 10)]
    elif nivel == 4:
        p = [(0, 6), (6, 7), (7, 9), (9, 10)]
    elif nivel == 5:
        p = [(0, 6), (6, 7), (7, 8), (8, 9), (9, 10)]
    elif nivel == 6: 
        p = [(0, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]
    elif nivel == 7:
        p = [(0, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]
    elif nivel == 8:
        p = [(0, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]
    elif nivel == 9:
        p = [(0, 2), (2, 3),  (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]
    elif nivel >= 10:
        p = [(0, 1), (1, 2), (2, 3),  (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10)]
    return p




"""
se utiliza la declaración with open(nombre_archivo, 'r') as archivo para abrir el archivo 
en modo de lectura. Esto asegura que el archivo se cierre automáticamente después de su uso
"""
def cargar_palabras(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo: 
        contenido = archivo.read() # Se lee el contenido del archivo utilizando el método read() y se almacena en la variable contenido
        palabras = contenido.split() #Se utiliza el método split() aplicado a contenido para dividirlo en una lista de palabras individuales
    return palabras #La función retorna la lista palabras, que contiene las palabras extraídas del archivo.




"""
La función ocultar(palabra) recibe como parámetro una palabra 
y retorna otra cadena de texto donde las letras de la palabra
original están ocultas por guiones "-" o espacios en blanco.
"""
def ocultar(palabra):
    return ''.join(['-' if i != ' ' else ' ' for i in palabra])


palabras = cargar_palabras('words.txt') #Se carga la base de datos con todas las palabras



def configurar():
    global width, jugadores, estados1, estados2, intentos1, intentos2, r_idx, palabra, enigma, nivelp, pasos, ventana, i, j, puntaje, puntaje2 
    jugadores = ingresar('¿Jugarás con alguien más? (s/n)') #Se pregunta si se va a jugar con alguien más
    jugadores = 1 if jugadores.lower() == 'n' else 2 # Se define si es 1 o 2 jugadores
    estados1 = [0] * 10 #Esta parte representa las partes del dibujo, en este caso son 10 estados y todos inician en 0
    estados2 = [0] * 10 if jugadores == 2 else [] #Esta variable se incia solo en caso de que sean 2 jugadores
    intentos1 = 0 #Inician la cantidad de intentos en 0
    intentos2 = 0 #Lo mismo para el jugador 2

    r_idx = np.random.randint(len(palabras)) #se utiliza para seleccionar una palabra aleatoria de la lista de palabras cargadas previamente.
    palabra = palabras[r_idx] #Se asigna la palabra correspondiente al índice r_idx de la lista palabras a la variable palabra.
    #palabra = 'calendario'
    enigma = ocultar(palabra) #Se oculta la palabra
    nivelp = nivel(palabra) #Se escoge el nivel
    print('El nivel de la palabra es:', nivelp) #Se imprime el nivel 

    pasos = pasos_dibujo(nivelp) #Se habilita el nuñequito para que se comience a dibujar
 
    width = 800 if jugadores == 2 else 400 #Se amplia la ventana en caso de que sean 2 jugadpres
    ventana = pygame.display.set_mode((width, height)) #Se abre la ventana
    i = 0 #Inician las variables en 0
    j = 0
    puntaje = 0
    puntaje2 = 0




"""
Este código representa el bucle principal del juego del ahorcado, 
que controla la lógica del juego, las interacciones con el usuario y 
el renderizado de la interfaz gráfica. Permite que los jugadores 
ingresen letras para adivinar la palabra enigmática y muestra el progreso 
del dibujo del ahorcado. Al finalizar el juego, muestra los puntajes 
obtenidos y reinicia el juego si el jugador desea continuar.
"""
configurar()
vivos = True 

pygame.display.set_caption("Ahorcado") #
ejecutando = True #Se establece el primer bucle
while ejecutando: #Mientras se este ejecutando entonces
    for evento in pygame.event.get(): #se recorren todos los eventos que ocurren en la ventana de la interfaz gráfica
        if evento.type == pygame.QUIT: # si el usuario intenta cerrar la ventana, rompe el bucle y finaliza el juego.
            ejecutando = False # Lo anterior porque el ejecutando == False

    
    
    # Renderizado
    ventana.fill((0, 0, 0)) #Se utiliza ventana.fill((0, 0, 0)) para llenar la ventana con color negro.

    escribir(enigma, (width / 2, height / 2 - 125)) #Para mostrar en pantalla la palabra enigmática en el centro de la ventana.
    if jugadores == 1:  #Coordenadas para dibujar el muñeco en el centro de la ventana si es 1 jugador
        hangman((width / 2, height / 2), estados1, 25)
    else: #Coordenadas para dibujar los muñequitos en caso de que sean 2 jugadores
        hangman((width / 4, height / 2), estados1, 25)
        hangman((3 * width / 4, height / 2), estados2, 25)

    pygame.display.flip() #Actualiza la ventana y mostrar los cambios realizados en el renderizado.
    pygame.event.pump() # Mantiene actualizados los eventos de Pygame.



    """
    Se verifica si la palabra enigmática es igual a la palabra original 
    y si ambos jugadores están vivos (la variable vivos es verdadera). 
    Si estas condiciones se cumplen, significa que se ha adivinado la 
    palabra o se ha llegado al final de los pasos para dibujar el ahorcado.
    """
    if not (palabra == enigma) and vivos: 
        jug = '' if jugadores == 1 else 'Jugador 1, '
        if i < len(pasos): #Mientras la cantidad de intentos sea menor a la cantidad de pasos entonces:
            x = ingresar(jug + 'Ingresa una letra: ')
            o = ocurrencias(x, palabra) #Contador que nos ayuda a saber cuando el hangman ya ha 'muerto' e indica que el juego debe reinciar
            if o != []:
                puntaje += 1
                for k in o:
                    enigma = list(enigma)
                    enigma[k] = palabra[k]
                    enigma = ''.join(enigma)
            else:
                r_estados = [1] * (pasos[i][1] - pasos[i][0]) #En esta parte se va axctualizando el muñeco 
                estados1[pasos[i][0]: pasos[i][1]] = r_estados
                i += 1 #Se va sumando un estado a medida de que se equivoca el usuario
            intentos1 += 1
        elif jugadores == 1:
            vivos = False 
        if jugadores == 2: #Esta parte es en caso de que sean 2 jugadores
            if j < len(pasos):
                x = ingresar( 'Jugador 2, Ingresa una letra: ')
                o = ocurrencias(x, palabra)
                if o != []:
                    puntaje2 += 1 #Se va actualizando el puntaje del jugador
                    for k in o:
                        enigma = list(enigma)
                        enigma[k] = palabra[k]
                        enigma = ''.join(enigma)
                else:
                    r_estados = [1] * (pasos[j][1] - pasos[j][0]) #Se actualiza el hangman del segundo jugador
                    estados2[pasos[j][0]: pasos[j][1]] = r_estados
                    j += 1
                intentos2 += 1 #Se le reduce un intento
            elif i >= len(pasos): #Si la cantidad de intentos es mayor a la cantidad de pasos entonces 'muere'
                vivos = False 
        
    else: 
        puntaje = puntaje / nivelp * 100
        puntaje2 = puntaje2 / nivelp * 100 
        print('¡Fin del juego!')
        print ("La palabra era:", palabra)

        """
        Se imprimen los mensajes correspondientes al final del juego,
        incluyendo el puntaje del jugador 1 y, si hay dos jugadores,
        el puntaje del jugador 2.
        """
        print('Puntaje del Jugador 1: ', puntaje, '\b%' )
        if (jugadores == 2):
            print('Puntaje del Jugador 2:', puntaje2, '\b%')
        
        vivos = True #Se establece vivos = True para reiniciar el juego.
        configurar()

pygame.quit() #Finaliza el juego
