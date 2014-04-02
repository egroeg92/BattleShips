"""

Author: George Macrae
2014

"""


import pygame, pygbutton, sys

from pygame.locals import *
from socket import *


import Matchup

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)


def start(clientsocket,user,op,win):
	SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('End Game')

	SCREEN.fill(BLACK)

	FONT = pygame.font.SysFont("Arial", 20)
	userStats = user
	opStats = op

	userStats = userStats.split(';')
	opStats = opStats.split(';')

	i = 0
	while i < len(userStats):
		x = userStats[i].replace('\'','')
		userStats[i] = x
		i+=1
	
	i = 0
	while i < len(opStats):
		x = opStats[i].replace('\'','')
		opStats[i] = x
		i+=1

	print 'useStats ',userStats
	print 'opStats ', opStats


	if (len(userStats) <2):
		userStats = ['d','Wins','0','Loses','0']
	if (len(opStats) <2):
		opStats = ['aad','Wins','0','Loses','0']
		

	if win:
		positiontext = FONT.render("YOU WIN!!", 1, (255,255,255))
		x = int(userStats[2]) +1
		y = int(opStats[4]) +1
		userStats[2] = str(x)
		opStats[4] = str(y)
	else:
		positiontext = FONT.render("YOU ARE A LOSER!!", 1, (255,255,255))
		x = int(userStats[4]) +1
		y = int(opStats[2]) +1
		userStats[4] = str(x)
		opStats[2] = str(y)

	userText = FONT.render(str(userStats), 1, (255,255,255))
	opText = FONT.render(str(opStats), 1, (255,255,255))

	print 'useStats ',userStats
	print 'opStats ', opStats

	SCREEN.blit(positiontext, (300, 100))
	SCREEN.blit(userText, (300, 200))
	SCREEN.blit(opText, (300, 300))
	buttonExit = pygbutton.PygButton((WINDOWWIDTH/2+30, 700, 120, 30), 'Match Up')
	active = True
	
	while active:
		buttonExit.draw(SCREEN)
		pygame.display.update()
		for event in pygame.event.get():

			if 'click' in buttonExit.handleEvent(event):
				print 'back-sign in'
				Matchup.start(clientsocket, userStats[0])
				active = False
				break
