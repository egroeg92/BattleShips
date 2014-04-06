"""

Author: George Macrae
2014

"""

import pygame, pygbutton, sys

from pygame.locals import *
from socket import *

import threading

import textbox
import Matchup
import startGame

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)

FONT = pygame.font.SysFont("Arial", 14)

def listener(clientsocket,SCREEN):
    global set_up
    global op_ready
    global ready
    global listen
    while True :
        data = clientsocket.recv(1024)
        print 'SET UP : data recv '+ str(data)

        if data == 'ExitSetup':
            print 'EXIT SETUP'
            set_up = False
            break
        if data == 'OppReady':
                windowBgColor = BLACK
                SCREEN.fill(windowBgColor)
                
                label = FONT.render("Set up", 1, (255,255,0))
                msg = FONT.render("Opponent is Ready", 1, (255,255,0))
                SCREEN.blit(msg,(150,150))
                SCREEN.blit(label, (100, 100))
                buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 250, 120, 30), 'back')   
                buttonStart = pygbutton.PygButton((WINDOWWIDTH/2-60, 50, 120, 30), 'start')
                buttonExit.draw(SCREEN)
                buttonStart.draw(SCREEN)
                pygame.display.update()
                op_ready = True

        if data == 'BreakListener':
#         if op_ready == True and ready == True:
            listen = False
            print 'break listener!!'
            break
        
        if op_ready == True and ready == True:
            listen = False
            print 'break listener,both ready'
            break                    



def start(clientsocket,opp,user,un):

    print 'Set up'+str(threading.activeCount())
    print 'opp = '+ opp
    windowBgColor = BLACK
    
    # pygame.init()

    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Set up')

    SCREEN.fill(windowBgColor)
    label = FONT.render("Set up", 1, (255,255,0))
    SCREEN.blit(label, (100, 100))
    
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 250, 120, 30), 'back')
    
    buttonStart = pygbutton.PygButton((WINDOWWIDTH/2-60, 50, 120, 30), 'start')

    buttonLoad = pygbutton.PygButton((WINDOWWIDTH/2-60, 100, 120,30), 'Load')
    buttonExit.draw(SCREEN)
    buttonStart.draw(SCREEN)
    pygame.display.update()

    global listen
    global set_up
    global op_ready
    global ready
    
    listen = True
    op_ready = False
    set_up = True
    ready = False
    player1 = True
    
    l_thread = threading.Thread(target = listener, args = (clientsocket,SCREEN))
    
    l_thread.start()
          
    
    while True :
        if set_up == False:
            
            Matchup.start(clientsocket,un)
            break
        if op_ready == True and ready == True and listen == False:
            clientsocket.send('StartGame')
            reef = clientsocket.recv(1024)
            reef = reef.split(':')
            reef = reef[1]
            startGame.main(clientsocket, opp,user,player1,reef)
            
            break
            
        for event in pygame.event.get():
            if 'click' in buttonExit.handleEvent(event) and ready == False:
                print 'Back-Setup'
                clientsocket.send('ExitSetup:'+opp)
                clientsocket.send('ExitSetup:'+user[1:-1])

            if 'click' in buttonStart.handleEvent(event) and ready == False:
                    ready = True
                    windowBgColor = BLACK
                    SCREEN.fill(windowBgColor)
                    msg = FONT.render("Waiting for opponent", 1, (255,255,0))
                    SCREEN.blit(msg,(150,150))
                    SCREEN.blit(label, (100, 100))
                    pygame.display.update()
                    clientsocket.send('Ready:'+str(opp))
                    
                    if op_ready == True:
                        clientsocket.send('BreakListener')
                        player1 = False
        
            
   
    
                