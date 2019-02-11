import pygame
from pygame.locals import *

import random

pygame.init() #Se inicializa pygame y el control de los FPS del juego
fpsClock = pygame.time.Clock()

screen_width = 480
screen_height = 640

surface = pygame.display.set_mode((screen_width, screen_height))

highscore_file = open("highscore")
highscore = highscore_file.read()
highscore_file.close()

pygame.font.init()
#Se crea una fuente para los textos grandes en pantalla
fuente = pygame.font.Font("BEBAS.ttf", 48)
gameover_txt = fuente.render("Game Over", True, (255, 0, 0))
youwin_txt = fuente.render("You win!", True, (0, 255, 0))

#Se crea una fuente más pequeña para la puntuación
fuentecilla = pygame.font.Font("BEBAS.ttf", 30)
score_txt = fuentecilla.render("Score: 0", True, (0, 0, 255))

#Carga los sonidos en variables
disparo_fx = pygame.mixer.Sound("flechazo.wav")
explosion_fx = pygame.mixer.Sound("explosion_marciano.wav")
nodriza_fx = pygame.mixer.Sound("nodriza_pass.wav")
alarma_fx = pygame.mixer.Sound("ambiente.wav")

#Se cargan los datos de imagen desde el archivo externo
archivo = open("ejemplo.txt")
contenido = archivo.readlines()
archivo.close()
largo = len(contenido)

#Se crean los arrays que guardarán los marcianos 
marcianotes = []
marcianotes_backup = []

contador = 0

while contador < largo:
    elemento = contenido[contador].split()

    if elemento[0] == "nave":
        nave_img = pygame.image.load(elemento[1])
        nave_w,nave_h = nave_img.get_rect().size[0], nave_img.get_rect().size[1]
        #Si la imagen fuese más grande de lo debido habría que redimensionar y
        #almacenar de nuevo su tamaño o habría problemas al calcular límites y posiciones
        #nave_img = pygame.transform.scale(nave_img, (int(nave_w/2), int(nave_h/2)))
        #nave_w,nave_h = nave_img.get_rect().size[0], nave_img.get_rect().size[1]
    
    elif elemento[0] == "disparo":
        disparo_img = pygame.image.load(elemento[1])
        disparo_file = elemento[1]
        disparo_w,disparo_h = disparo_img.get_rect().size[0], disparo_img.get_rect().size[1]
    
    elif elemento[0] == "marcianito1":
        mar1_img = pygame.image.load(elemento[1])
        marcianito1_file = elemento[1]
        mar1_w,mar1_h = mar1_img.get_rect().size[0], mar1_img.get_rect().size[1]
        #mar1_img = pygame.transform.scale(mar1_img, (mar1_w/2, mar1_h/2))
        #mar1_w,mar1_h = mar1_img.get_rect().size[0], mar1_img.get_rect().size[1]
        
    #Comentados porque ahora mismo sólo se usa un tipo de marciano
    #elif elemento[0] == "marcianito2":
        #mar2_img = pygame.image.load(elemento[1])
        #mar2_w,mar2_h = mar2_img.get_rect().size[0], mar2_img.get_rect().size[1]
        #mar2_img = pygame.transform.scale(mar2_img, (mar2_w/2, mar2_h/2))
        #mar2_w,mar2_h = mar2_img.get_rect().size[0], mar2_img.get_rect().size[1]
        
    #elif elemento[0] == "marcianito3":
        #mar3_img = pygame.image.load(elemento[1])
        #mar3_w,mar3_h = mar3_img.get_rect().size[0], mar3_img.get_rect().size[1]
        
    elif elemento[0] == "nodriza":
        nodriza_img = pygame.image.load(elemento[1])
        nodriza_w,nodriza_h = nodriza_img.get_rect().size[0], nodriza_img.get_rect().size[1]
        
    elif elemento[0] == "fondo":
        fondo_img = pygame.image.load(elemento[1])
        
    contador = contador + 1
#ARCHIVO CARGADO    

#Se inicializan las variables
marcianitos_column = 8
marcianitos_filas = 5
contador_marcianitos = 0
contador_filas = 0
initial_x, initial_y = 0,64
current_x, current_y = initial_x,initial_y
posiciones = []
posiciones_backup = []
disparado = False
gameover = False

#Se crea el array de marcianos
while contador_filas < marcianitos_filas:
    
    contador_marcianitos = 0
    current_x = initial_x
    while contador_marcianitos < marcianitos_column:
        
        #Se añade a los dos arrays para tener una copia para reiniciar el juego
        #sin tener que hacer todo el proceso de nuevo
        marcianotes.append(mar1_img)
        marcianotes_backup.append(mar1_img)

        #Se almacena el tamaño de la imagen para calcular las posiciones
        marciano_width = marcianotes[len(marcianotes)-1].get_rect().size[0]
        marciano_height = marcianotes[len(marcianotes)-1].get_rect().size[1]
    
        #Al igual que con los marcianos, se guardan dos copias para poder reiniciarlo
        posiciones.append((current_x, current_y))
        posiciones_backup.append((current_x, current_y))

        current_x += marciano_width + 8

        contador_marcianitos += 1
    
    current_y += marciano_height + 8
    contador_filas += 1

nave_x = 0
nave_desp = 6
nave_mov = 0

nodriza_x, nodriza_y = -nodriza_w,38
nodriza_desp = 6
nodriza_dir = 1
nodriza_mov = False

mar1_x = 0
#Dirección en la que se mueven los marcianos
marcianos_dir = 1

#Se sitúa el disparo fuera de imagen para controlar cuándo está en uso y cuándo no
disparo_x, disparo_y = -1000, -1000
disparo_speed = 15
def Disparar (x, y):
    global disparo_x
    global disparo_y
    global disparo_speed
    global disparado
    global score
    global score_txt
    global nodriza_mov
    global nodriza_x
    
    #Si el disparo está fuera de la pantalla se coloca en la posición del jugador
    if disparo_x == -1000:
        disparo_x = x
        disparo_y = y
    
    if disparado:
        surface.blit(disparo_img, (disparo_x,disparo_y))
        
    muerto = False
    contador = 0
    #Por cada posicion de marcianos se comprueba si coincide con la del disparo,
    #si coinciden se elimina la posición, se reinicia el disparo y se suma la puntuación.
    while contador < len(posiciones) and not muerto:
        x_marciano,y_marciano = posiciones[contador]
        if disparo_x >= x_marciano and disparo_x <= x_marciano + mar1_w:
            if disparo_y >= y_marciano and disparo_y <= y_marciano + mar1_h:
                explosion_fx.play()
                disparado = False
                disparo_x, disparo_y = -1000, -1000
                
                del marcianotes[contador]
                del posiciones[contador]
                
                score += 1
                score_txt = fuentecilla.render("Score: " + str(score), True, (0, 0, 255))
                
        contador += 1
    
    #Si la nodriza está activa también se comprueban las posiciones
    #Al estar más alta si ha llegado aquí es porque el disparo no ha matado ningún marciano
    if nodriza_mov:
        if disparo_x >= nodriza_x and disparo_x <= nodriza_x + nodriza_w:
            if disparo_y >= nodriza_y and disparo_y <= nodriza_y + nodriza_h:
                explosion_fx.play()
                disparado = False
                disparo_x, disparo_y = -1000, -1000
                
                #Reiniciar Nodriza
                nodriza_mov = False
                nodriza_x = -nodriza_w
                nodriza_fx.stop()
                
                score += 5
                score_txt = fuentecilla.render("Score: " + str(score), True, (0, 0, 255))

    #Si el disparo sigue activo se modifica su posición
    disparo_y -= disparo_speed
    
    #Si ha llegado al límite superior de la pantalla se reinicia su posición
    if disparo_y <= 0:
        disparado = False
        disparo_x, disparo_y = -1000, -1000

def GuardarHighscore ():
    global completado
    global score
    global highscore
    
    if not completado:
        if score > int(highscore):
            highscore_file = open("highscore", "w")
            highscore_file.write(str(score))
            highscore_file.close()
        completado = True


#Función para que todos los marcianos bajen una línea por haber llegado al límite
def Avanzar ():
    global posiciones
    global gameover
    
    paso = 16
    contador = 0
    while contador < len(posiciones):
        x_temporal,y_temporal = posiciones[contador]
        y_temporal += paso
        
        #Si en algún momento una nave baja lo suficiente se acaba el juego
        if y_temporal >= screen_height-nave_h*2:
            gameover = True
        
        posiciones[contador] = (x_temporal, y_temporal)
        contador += 1
    

#Función para reiniciar el juego
def Reiniciar ():
    global marcianotes
    global posiciones
    global completado
    global gameover
    global disparado
    global disparo_x
    global disparo_y
    
    gameover = False
    disparado = False
    completado = False
    disparo_x = -1000
    disparo_y = -1000
    
    marcianotes = []
    posiciones = []
    
    contador = 0
    while contador < len(marcianotes_backup):
        marcianotes.append(marcianotes_backup[contador])
        posiciones.append(posiciones_backup[contador])
        contador += 1

score = 0
completado = False
#-1 indica que el audio hace un loop infinito
alarma_fx.play(-1)

#Manteniendo esta variable se hace un buble infinito para que la aplicación siga
#funcionando constantemente
salir = False
while not salir:
    #Se rellena el fondo en negro, para no dejar huecos si la imagen es más pequeña
    surface.fill((0,0,0))
    
    surface.blit(fondo_img, (0,0))
    
    if nodriza_mov and not gameover:
        surface.blit(nodriza_img, (nodriza_x,nodriza_y))
        nodriza_x += nodriza_desp * nodriza_dir
        #Si la nodriza se sale de la pantalla se reinicia
        if nodriza_x >= screen_width:
            nodriza_mov = False
            nodriza_x = -nodriza_w
            nodriza_fx.stop()
    else:
        #Posibilidades de que se active la nodriza, a mayor número, menos opciones
        if random.randint(1,1000) % 500 == 0:
            nodriza_mov = True
            nodriza_fx.play(-1)
    
    
    contador_marcianitos = 0
    max_x = 0
    min_x = screen_width - mar1_w
    #Se avanza una posición de todos los marcianos
    while contador_marcianitos < len(marcianotes):
        
        x,y = posiciones[contador_marcianitos]
       
        surface.blit(marcianotes[contador_marcianitos], posiciones[contador_marcianitos])
        
        if not gameover:
            x += marcianos_dir * nave_desp/3
            posiciones[contador_marcianitos] = (x, y)
        
            #Se almacenan las posiciones máximas o mínimas según la posición
            if marcianos_dir > 0:
                if x > max_x:
                    max_x = x
            else:
                if x < min_x:
                    min_x = x
        
        contador_marcianitos += 1
        
    #Si alguno de los marcianos se sale de los límites se cambia la dirección
    if min_x <= 0:
        marcianos_dir = 1
        Avanzar()
    elif max_x >= screen_width - mar1_w:
        marcianos_dir = -1
        Avanzar()

    nave_y = screen_height-nave_h-4
    surface.blit(nave_img, (nave_x,nave_y))
        

    keys = pygame.key.get_pressed()
    #Se usan dos if y no un elif para que el movimiento no sea excluyente
    if keys[pygame.K_LEFT]:
        #Se le añade movimiento a la izquierda
        nave_mov -= nave_desp
        if nave_x <= 0:
            nave_x = 0
    if keys[pygame.K_RIGHT]:
        #Se le añade movimiento a la derecha
        nave_mov += nave_desp
        if nave_x >= screen_width - nave_w:
            nave_x = screen_width - nave_w
    #Se le aplica el movimiento calculado arriba
    nave_x += nave_mov
    nave_mov = 0

    if keys[pygame.K_SPACE]:
        if not disparado:
            disparado = True
            disparo_fx.play()
        if gameover or len(marcianotes) == 0:
            Reiniciar()
        

    if disparado:
        Disparar(nave_x + nave_w - disparo_w*2, nave_y)
            
    surface.blit(score_txt, (10, 10))


    if gameover:
        gameOverWidth, gameOverHeight = gameover_txt.get_rect().size[0], gameover_txt.get_rect().size[1]
        surface.blit(gameover_txt, (screen_width/2-gameOverWidth/2, screen_height/2-gameOverHeight/2))
        GuardarHighscore()

    if len(marcianotes) == 0:
        youWinWidth, youWinHeight = youwin_txt.get_rect().size[0], youwin_txt.get_rect().size[1]
        surface.blit(youwin_txt, (screen_width/2-youWinWidth/2, screen_height/2-youWinHeight/2))
        GuardarHighscore()
        alarma_fx.stop()


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            #Se rompe el bucle infinito para poder salir del juego
            salir = True

    pygame.display.update()
    fpsClock.tick(30)
