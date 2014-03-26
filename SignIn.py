"""

Author: George Macrae
2014

"""


import pygame, pygbutton, sys

from pygame.locals import *
from socket import *

import Start
import textbox
import Matchup
import login

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)

FONT = pygame.font.SysFont("Arial", 14)



def start(socketerror, ip):

	print 'Sign In'
	windowBgColor = BLACK

	CLOCK = pygame.time.Clock()
	SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Connect to Server')

	SCREEN.fill(windowBgColor)
	label = FONT.render("Sign In", 1, (255,255,0))
	SCREEN.blit(label, (100, 100))
	if socketerror:
		msg = FONT.render("Couldnt connect to ip " + ip, 1, (255,255,0))
		SCREEN.blit(msg, (100,150))	


	
	host = textbox.start(SCREEN,"Enter Server IP")
	print host
	port = 9999
	addr = (host, port)
	clientsocket = socket(AF_INET, SOCK_STREAM)
	
	buttonSignIn = pygbutton.PygButton((WINDOWWIDTH/2-60, 100, 120, 30), 'Sign In')
	buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 250, 120, 30), 'back')

	buttonSignIn.draw(SCREEN)
	buttonExit.draw(SCREEN)

	pygame.display.update()

		
	loop = True
	while loop :
		for event in pygame.event.get():

			if 'click' in buttonSignIn.handleEvent(event):
				try:
					loop = False
					clientsocket.connect(addr)
					clientsocket.send("Signed In")
					login.start(clientsocket)
					# Matchup.start(clientsocket)
					
				except gaierror:
					loop = False
					start(True,host)
				except error:
					loop = False
					start(True,host)
									
			
			if 'click' in buttonExit.handleEvent(event):
				print 'back-sign in'
				loop = False
				Start.main()
				
				

if __name__ == '__main__':
	host = gethostbyname(gethostname())
	print host
	port = 9999
	addr = (host, port)
	clientsocket = socket(AF_INET, SOCK_STREAM)
	clientsocket.connect(addr)
	print clientsocket
	clientsocket.send("Signed In")
	Matchup.start(clientsocket,str(addr))