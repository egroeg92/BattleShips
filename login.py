from socket import *
import threading

import pygame, pygbutton, sys
from pygame.locals import *

import Matchup
import Start
import textbox


FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 750

FONT = pygame.font.SysFont("Arial", 14)


BLACK = (0, 0, 0, 0.8)

def listener(clientsocket,screen):
    print 'listening'
    global loop
    while loop:
        data = clientsocket.recv(1024) 
        print str(data)
        if(data == 'SignedIn'):
        	loop = False
 


def start(clientsocket):

	print 'login'
	windowBgColor = BLACK

	FPSCLOCK = pygame.time.Clock()
	SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Login')

	SCREEN.fill(windowBgColor)
	label = FONT.render("Login or create new account", 1, (255,255,0))
	SCREEN.blit(label, (100, 100))
	
	un = textbox.start(SCREEN,"Enter Username:")

	pw = textbox.start(SCREEN,"Enter Password:")


	global loop
	loop = True
	buttonLogin = pygbutton.PygButton((WINDOWWIDTH/2-60, 100, 120, 30), 'Login In')
	buttonSignUp = pygbutton.PygButton((WINDOWWIDTH/2-60, 150, 120, 30), 'Sign Up')
	buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 250, 120, 30), 'Disconnect')
	l_thread = threading.Thread(target = listener, args = (clientsocket,SCREEN))
	l_thread.start()

	dc = False
	while  loop:
		buttonSignUp.draw(SCREEN)
		buttonLogin.draw(SCREEN)
		buttonExit.draw(SCREEN)
		pygame.display.update()
		for event in pygame.event.get():

			if 'click' in buttonLogin.handleEvent(event):
				clientsocket.send("Login:"+un+':'+pw)
   
			
			if 'click' in buttonSignUp.handleEvent(event):
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
