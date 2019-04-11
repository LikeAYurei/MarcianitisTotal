import pygame
from pygame.locals import *

import random
#import sys

pygame.init()
fpsClock = pygame.time.Clock()

width = 480
height = 640

surface = pygame.display.set_mode((width, height))

highscore_file = open("highscore")
highscore = highscore_file.read()
highscore_file.close()

pygame.font.init()
fuente = pygame.font.Font("BEBAS.ttf", 48)
gameover_txt = fuente.render("Game Over", True, (255, 0, 0))
youwin_txt = fuente.render("You win!", True, (0, 255, 0))

fuentecilla = pygame.font.Font("BEBAS.ttf", 30)
score_txt = fuentecilla.render("Score: 0", True, (0, 0, 255))

disparo_fx = pygame.mixer.Sound("flechazo.wav")
explosion_fx = pygame.mixer.Sound("explosion_marciano.wav")
nodriza_fx = pygame.mixer.Sound("nodriza_pass.wav")
alarma_fx = pygame.mixer.Sound("ambiente.wav")


archivo = open("ejemplo.txt")

contenido = archivo.readlines()
marcianotes = []
marcianotes_backup = []

archivo.close()

largo = len(contenido)
contador = 0



while contador < largo:
    elemento = contenido[contador].split()
    
    if elemento[0] == "nave":
        nave_img = pygame.image.load(elemento[1])
        nave_w,nave_h = nave_img.get_rect().size[0], nave_img.get_rect().size[1]
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
        
    elif elemento[0] == "marcianito2":
        mar2_img = pygame.image.load(elemento[1])
        mar2_w,mar2_h = mar2_img.get_rect().size[0], mar2_img.get_rect().size[1]
        #mar2_img = pygame.transform.scale(mar2_img, (mar2_w/2, mar2_h/2))
        #mar2_w,mar2_h = mar2_img.get_rect().size[0], mar2_img.get_rect().size[1]
        
    elif elemento[0] == "marcianito3":
        mar3_img = pygame.image.load(elemento[1])
        mar3_w,mar3_h = mar3_img.get_rect().size[0], mar3_img.get_rect().size[1]
        
    elif elemento[0] == "nodriza":
        nodriza_img = pygame.image.load(elemento[1])
        nodriza_w,nodriza_h = nodriza_img.get_rect().size[0], nodriza_img.get_rect().size[1]
        
    elif elemento[0] == "fondo":
        fondo_img = pygame.image.load(elemento[1])
        
    contador = contador + 1
    
#ARCHIVO CARGADO    

marcianitos_num = 8
marcianitos_filas = 5
contador_marcianitos = 0
contador_filas = 0
ini_x, ini_y = 0,64
cur_x, cur_y = ini_x,ini_y
posiciones = []
posiciones_backup = []
disparado = False
gameover = False

while contador_filas < marcianitos_filas:
    
    contador_marcianitos = 0
    cur_x = ini_x
    while contador_marcianitos < marcianitos_num:
        #marcianotes.append(pygame.image.load(marcianito1_file))
        marcianotes.append(mar1_img)
        marcianotes_backup.append(mar1_img)

        m_w = marcianotes[len(marcianotes)-1].get_rect().size[0]
        m_h = marcianotes[len(marcianotes)-1].get_rect().size[1]
    
        posiciones.append((cur_x, cur_y))
        posiciones_backup.append((cur_x, cur_y))

        cur_x += m_w + 8

        contador_marcianitos += 1
    
    cur_y += m_h + 8
    contador_filas += 1

nave_x = 0
nave_desp = 6
nave_mov = 0

nodriza_x, nodriza_y = -nodriza_w,38
nodriza_desp = 6
nodriza_dir = 1
nodriza_mov = False

mar1_x = 0
mar2_x = 0
marcianos_dir = 1

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
    
    if disparo_x == -1000:
        disparo_x = x
        disparo_y = y
    
    if disparado:
        surface.blit(disparo_img, (disparo_x,disparo_y))
        
    muerto = False
    contador = 0
    while contador < len(posiciones) and not muerto:
        x_m,y_m = posiciones[contador]
        if disparo_x >= x_m and disparo_x <= x_m + mar1_w:
            if disparo_y >= y_m and disparo_y <= y_m + mar1_h:
                explosion_fx.play()
                disparado = False
                disparo_x, disparo_y = -1000, -1000
                
                del marcianotes[contador]
                del posiciones[contador]
                
                score += 1
                score_txt = fuentecilla.render("Score: " + str(score), True, (0, 0, 255))
                
        contador += 1
    
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

    disparo_y -= disparo_speed
    
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


def Avanzar ():
    global posiciones
    global gameover
    
    paso = 16
    contador = 0
    while contador < len(posiciones):
        x_t,y_t = posiciones[contador]
        y_t += paso
        
        if y_t >= height-nave_h*2:
            gameover = True
        
        posiciones[contador] = (x_t, y_t)
        contador += 1
    

def Reiniciar ():
    global marcianotes
    #global marcianotes_backup
    global posiciones
    #global posiciones_backup
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
alarma_fx.play(-1)

salir = False
while not salir:
    surface.fill((0,0,0))
    
    surface.blit(fondo_img, (0,0))
    
    
    if nodriza_mov and not gameover:
        surface.blit(nodriza_img, (nodriza_x,nodriza_y))
        nodriza_x += nodriza_desp * nodriza_dir
        if nodriza_x >= width:
            nodriza_mov = False
            nodriza_x = -nodriza_w
            nodriza_fx.stop()
    else:
        if random.randint(1,1000) % 500 == 0:
            nodriza_mov = True
            nodriza_fx.play(-1)
    
    
    contador_marcianitos = 0
    max_x = 0
    min_x = width - mar1_w
    while contador_marcianitos < len(marcianotes):
        
        x,y = posiciones[contador_marcianitos]
       
        surface.blit(marcianotes[contador_marcianitos], posiciones[contador_marcianitos])
        
        if not gameover:
            x += marcianos_dir * nave_desp/3
            posiciones[contador_marcianitos] = (x, y)
        
            if marcianos_dir > 0:
                if x > max_x:
                    max_x = x
            else:
                if x < min_x:
                    min_x = x
        
        contador_marcianitos += 1
        
    if min_x <= 0:
        marcianos_dir = 1
        Avanzar()
    elif max_x >= width - mar1_w:
        marcianos_dir = -1
        Avanzar()

    nave_y = height-nave_h-4
    surface.blit(nave_img, (nave_x,nave_y))
        

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        #Mover a la izquierda
        nave_mov -= nave_desp
        if nave_x <= 0:
            nave_x = 0
    if keys[pygame.K_RIGHT]:
        #Mover a la derecha
        nave_mov += nave_desp
        if nave_x >= width - nave_w:
            nave_x = width - nave_w
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
        go_w, go_h = gameover_txt.get_rect().size[0], gameover_txt.get_rect().size[1]
        surface.blit(gameover_txt, (width/2-go_w/2, height/2-go_h/2))
        GuardarHighscore()

    if len(marcianotes) == 0:
        yw_w, yw_h = youwin_txt.get_rect().size[0], youwin_txt.get_rect().size[1]
        surface.blit(youwin_txt, (width/2-yw_w/2, height/2-yw_h/2))
        GuardarHighscore()
        alarma_fx.stop()


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            salir = True

    pygame.display.update()
    fpsClock.tick(30)
