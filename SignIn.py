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
WINDOWHEIGHT = 700

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)

FONT = pygame.font.SysFont("Arial", 14)



def start(socketerror, ip):

	print 'Sign In'

	CLOCK = pygame.time.Clock()
	SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Connect to Server')

	SCREEN.blit(pygame.image.load('images/ivanaivazovsky.png').convert(),(0,0))
	SCREEN.blit(pygame.image.load('images/overlay.png').convert_alpha(),(100,350))


	label = FONT.render("Enter the IP address of the server, and hit ENTER:", 1, WHITE)
	SCREEN.blit(label, (200, 400))
	
	#buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 560, 120, 30), 'Back')

	#buttonSignIn.draw(SCREEN)
# 	buttonExit.draw(SCREEN)
	
	if socketerror:
		msg = FONT.render("Couldnt connect to IP: " + ip, 1, RED)
		SCREEN.blit(msg, (200,500))	

	loop = True
	while loop :
		host = textbox.start(SCREEN," ")
		print host
		port = 9999
		addr = (host, port)
		clientsocket = socket(AF_INET, SOCK_STREAM)
		
		pygame.display.update()
		try:
			loop = False
			clientsocket.connect(addr)
			clientsocket.send("Signed In")
			login.start(clientsocket)
		except gaierror:
			loop = False
			start(True,host)
		except error:
			loop = False
			start(True,host)
			
# 		for event in pygame.event.get():
# 			
# 			if 'click' in buttonExit.handleEvent(event):
# 				print 'back-sign in'
# 				loop = False
# 				Start.main()
# 				
				

if __name__ == '__main__':
	import random 
	import string

	host = "127.0.0.1"
	print host
	port = 9999
	addr = (host, port)
	clientsocket = socket(AF_INET, SOCK_STREAM)
	clientsocket.connect(addr)
	print clientsocket
	clientsocket.send("Signed In")
	Matchup.start(clientsocket,''.join(random.choice(string.lowercase) for x in range(5)))