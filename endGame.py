"""

Author: George Macrae
2014

"""


import pygame, pygbutton, sys

from pygame.locals import *
from socket import *


import Matchup

FPS = 30
WINDOWWIDTH = 799
WINDOWHEIGHT = 700

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)


def start(clientsocket,user,op,win):
	SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('End Game')

	SCREEN.blit(pygame.image.load('images/endbg.png').convert(),(0,0))

	FONT = pygame.font.SysFont("Arial", 20)
	TITLEFONT = pygame.font.SysFont("Arial", 30)
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
		SCREEN.blit(pygame.image.load('images/victorytext.png').convert_alpha(),(200,50))
		x = int(userStats[2]) +1
		y = int(opStats[4]) +1
		userStats[2] = str(x)
		opStats[4] = str(y)
	else:
		SCREEN.blit(pygame.image.load('images/defeattext.png').convert_alpha(),(200,50))
		x = int(userStats[4]) +1
		y = int(opStats[2]) +1
		userStats[4] = str(x)
		opStats[2] = str(y)

	print 'userStats ',userStats
	print 'opStats ', opStats

	SCREEN.blit(pygame.image.load('images/overlay.png').convert_alpha(),(100,300))
	SCREEN.blit(FONT.render(str(userStats[0]), 1, (255,255,255)), (200, 350))
	SCREEN.blit(FONT.render(str(opStats[0]), 1, (255,255,255)), (440, 350))
	
	SCREEN.blit(FONT.render("Wins: " + str(userStats[2]), 1, (255,255,255)), (200, 380))
	SCREEN.blit(FONT.render("Wins: " + str(opStats[2]), 1, (255,255,255)), (440, 380))
	
	SCREEN.blit(FONT.render("Losses: " + str(userStats[4]), 1, (255,255,255)), (200, 410))
	SCREEN.blit(FONT.render("Losses: " + str(opStats[4]), 1, (255,255,255)), (440, 410))
	
	buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 600, 120, 30), 'Match Up')
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
