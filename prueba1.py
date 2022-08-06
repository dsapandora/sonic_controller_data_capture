import retro
import pygame
import numpy
import numpy as np
from pygame.locals import *
import cv2
import imutils
import random
from random import randint 

# state machine
from statemachine import StateMachine, State

class Vector(StateMachine):
    

    parado = State('Parado', initial=True)
    morir = State('Morir')
    meta = State('Meta')
    izquierda = State('Izquierda')
    derecha = State('derecha')
    agachar = State('Agachar')
    saltar = State('Saltar')

    quieto = parado.to(parado)
    ir_izquierda = parado.to(izquierda)
    mantener_izquierda = izquierda.to(izquierda)
    ir_derecha = parado.to(derecha)
    mantener_derecha = derecha.to(derecha)
    duck = parado.to(agachar)
    mantener_agachado = agachar.to(agachar)
    salto_izquierda = izquierda.to(saltar)
    izquierda_salto = saltar.to(izquierda)
    salto_derecha = derecha.to(saltar)
    derecha_salto = saltar.to(derecha)
    salta_agachado = agachar.to(saltar)
    agachado_salto = saltar.to(agachar)
    detener_izquierda = izquierda.to(parado)
    detener_derecha = derecha.to(parado)
    detener_agachar = agachar.to(parado)
    ganar = derecha.to(meta)
    muerto = derecha.to(morir) | izquierda.to(morir) | agachar.to(morir) | saltar.to(morir) | parado.to(morir)

    def on_quieto(self):
        print("Esta detenido")
        return [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def on_ir_izquierda(self):
        print("izquierda")
        return [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

    def on_salto_izquierda(self):
        print("salto a la izquierda")
        return [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]

video_size = 580,400
env = retro.make(game='Vectorman2-Genesis', state='Level1')
      

def key_action():
   #["B", "A", "MODE", "START", "UP", "DOWN", "LEFT", "RIGHT", "C", "Y", "X", "Z"]
    keys = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    key=pygame.key.get_pressed()
    print(key)
    
    #r = random.randrange(7)
    r=3
    if r == 0:
    	return  [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]  # saltar + 
    if r == 1: #los numeros dentro de los corchetes representan la tecla tocada
        return  [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]  # abajo
    if r == 2:
        return  [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]  # izquierda
    if r == 3:
        return  [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0] # derecha
    if r == 4:
        return  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Saltar  
    if r == 5:
        return  [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0] # correr hacia la derecha
    if r == 6:
        return  [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0] # correr
    return keys
    print (r)
r = numpy.append([[1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],[0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]],[[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]], axis = 0 )


screen = pygame.display.set_mode(video_size)
observation=env.reset()    

i=1
while True:
    img = env.render(mode='rgb_array')
    # ROTATE THE IMAGE THE MATRIX IS 90 grates and mirror
    img = np.flipud(np.rot90(img))
    image_np = imutils.resize(img, width=400)
    screen = pygame.display.set_mode(video_size)
    surf = pygame.surfarray.make_surface(image_np)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    action = key_action()
    #[up,down,left,right,a,b]
    observation, rew, done, info = env.step(action)
    print("Action ", action, "Reward ", rew)
    if done:
        break
