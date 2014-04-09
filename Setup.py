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

from Tkinter import Tk
from tkFileDialog import askopenfilename


FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 700

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
    global loadGame
    global lg
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
                
                label = FONT.render(" ", 1, (255,255,0))
                msg = FONT.render("Opponent is Ready", 1, (255,255,0))
                SCREEN.blit(msg,(150,150))
                SCREEN.blit(label, (100, 100))
                SCREEN.blit(pygame.image.load('images/endbg.png').convert(),(0,0))
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
        if data[:5]=='Load:':
            l = data.split(':')
            loadGame = l[-1]
            print loadGame

        if op_ready == True and ready == True:
            listen = False
            print 'break listener,both ready'
            break                    



def start(clientsocket,opp,user,un):

    print 'Set up'+str(threading.activeCount())
    print 'opp = '+ opp

    global o
    o = opp
    windowBgColor = BLACK
    
    # pygame.init()

    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Set up')

    SCREEN.fill(windowBgColor)
    label = FONT.render(" ", 1, (255,255,0))
    SCREEN.blit(label, (100, 100))
    SCREEN.blit(pygame.image.load('images/endbg.png').convert(),(0,0))
    
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 250, 120, 30), 'back')
    
    buttonStart = pygbutton.PygButton((WINDOWWIDTH/2-60, 50, 120, 30), 'start')

    buttonLoad = pygbutton.PygButton((WINDOWWIDTH/2-60, 100, 120,30), 'Load')
    
    buttonLoad.draw(SCREEN)
    buttonExit.draw(SCREEN)
    buttonStart.draw(SCREEN)
    pygame.display.update()

    global listen
    global set_up
    global op_ready
    global ready
    global loadGame
    loadGame = ''
    listen = True
    op_ready = False
    set_up = True
    ready = False
    player1 = True
    
    l_thread = threading.Thread(target = listener, args = (clientsocket,SCREEN))
    
    l_thread.start()
    
    load = None 
    
    while True :
        if set_up == False:
            
            Matchup.start(clientsocket,un)
            break
        if op_ready == True and ready == True and listen == False:
            clientsocket.send('StartGame')
            reef = clientsocket.recv(1024)
            reef = reef.split(':')
            
            print reef
            print reef[2]
            if reef[2] != '':
                loadGame = reef[2]

            startGame.main(clientsocket, opp,user,player1,reef[1],loadGame)
            
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
                    SCREEN.blit(pygame.image.load('images/endbg.png').convert(),(0,0))
                    msg = FONT.render("Waiting for opponent...", 1, (0,0,0))
                    SCREEN.blit(msg,(150,150))
                    SCREEN.blit(label, (100, 100))
                    pygame.display.update()
                    clientsocket.send('Ready:'+str(opp))
                    
                    if op_ready == True:
                        clientsocket.send('BreakListener')
                        player1 = False
        
            
            if 'click' in buttonLoad.handleEvent(event) and ready == False:
                print "load"
                filename = 'hello'
                Tk().withdraw() 
                filename = askopenfilename()
                
                print filename == ''
                if filename == '':
                    filename = 'HELLO'
                    
                if(filename[-4]+filename[-3]+filename[-2]+filename[-1] != '.bsh'):
                    print 'not a Name'
                    label = FONT.render("Wrong file extension - can only load .bsh", 1, (255,255,0))
                    SCREEN.blit(label, (100, 100))
    
                else:
                    load = filename
                    clientsocket.send("Load:"+'/'+str(opp)+'/'+filename)


    

                
                