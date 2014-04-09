import pygame, pygbutton, sys

from pygame.locals import *
from socket import *

import threading


import Start
import textbox
import Matchup
FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 700

FONT = pygame.font.SysFont("Arial", 14)

RED = (255, 0, 0)

BLACK = (0, 0, 0, 0.8)

def listener(clientsocket,screen):
    print 'listening'
    global loop
    loop = True
    while loop:
        data = clientsocket.recv(1024) 
        print "asd " + str(data)
        label = FONT.render(str(data), 1, RED)
        screen.blit(label, (200, 400))
        
        if(data == 'SignedIn'):
            print "SIGNED IN"
            loop = False
            


def start(clientsocket):
    
    print 'login'
    
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Login')
    

# 	un = textbox.start(SCREEN,"Enter Username:")
# 
# 	pw = textbox.start(SCREEN,"Enter Password:")

    buttonLogin = pygbutton.PygButton((WINDOWWIDTH/2-60, 400, 120, 30), 'Login In')
    buttonSignUp = pygbutton.PygButton((WINDOWWIDTH/2-60, 450, 120, 30), 'Sign Up')
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 500, 120, 30), 'Disconnect')
    l_thread = threading.Thread(target = listener, args = (clientsocket,SCREEN))
    l_thread.start()
    global loop
    loop = True
    dc = False
    while  loop:
        SCREEN.blit(pygame.image.load('images/ivanaivazovsky.png').convert(),(0,0))

        buttonSignUp.draw(SCREEN)
        buttonLogin.draw(SCREEN)
        buttonExit.draw(SCREEN)
        pygame.display.update()
        
        for event in pygame.event.get():
        
            if 'click' in buttonLogin.handleEvent(event):
                SCREEN.blit(pygame.image.load('images/ivanaivazovsky.png').convert(),(0,0))
                SCREEN.blit(pygame.image.load('images/overlay.png').convert_alpha(),(100,350)) 
                label = FONT.render("Enter Username:", 1, (255,255,255))
                SCREEN.blit(label, (200, 400))
                un = textbox.start(SCREEN," ")
                
                SCREEN.blit(pygame.image.load('images/ivanaivazovsky.png').convert(),(0,0))
                SCREEN.blit(pygame.image.load('images/overlay.png').convert_alpha(),(100,350)) 
                label = FONT.render("Enter Password:", 1, (255,255,255))
                SCREEN.blit(label, (200, 400))
                pw = textbox.start(SCREEN," ")
                clientsocket.send("Login:"+un+':'+pw)    
            
            if 'click' in buttonSignUp.handleEvent(event):
                SCREEN.blit(pygame.image.load('images/ivanaivazovsky.png').convert(),(0,0))
                SCREEN.blit(pygame.image.load('images/overlay.png').convert_alpha(),(100,350)) 
                label = FONT.render("Enter Username:", 1, (255,255,255))
                SCREEN.blit(label, (200, 400))
                un = textbox.start(SCREEN," ")
                
                SCREEN.blit(pygame.image.load('images/ivanaivazovsky.png').convert(),(0,0))
                SCREEN.blit(pygame.image.load('images/overlay.png').convert_alpha(),(100,350)) 
                label = FONT.render("Enter Password:", 1, (255,255,255))
                SCREEN.blit(label, (200, 400))
                pw = textbox.start(SCREEN," ")
                
                clientsocket.send("SignUp:"+un+':'+pw)
    
            if 'click' in buttonExit.handleEvent(event):
                print 'Disconnect'
                clientsocket.send('Disconnect')
                clientsocket.close()
                Start.main()
                dc = True
                loop = False

    
    if not dc:
        Matchup.start(clientsocket,un)
