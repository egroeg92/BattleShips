import pygame, pygbutton, sys
from pygame.locals import *
import SignIn

FPS = 30
WINDOWWIDTH = 799
WINDOWHEIGHT = 700

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)

FONT = pygame.font.SysFont("Arial", 14)
TITLEFONT = pygame.font.SysFont("Helvetica", 30)

def main():

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Game Menu')

    screen.blit(pygame.image.load('images/ivanaivazovsky.png').convert(),(0,0))

    # menu buttons
    buttonSignIn = pygbutton.PygButton((WINDOWWIDTH/2-75, 360, 150, 30), 'Connect to Server')
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-75, 420, 150, 30), 'Exit')

    buttonBack = pygbutton.PygButton((WINDOWWIDTH/2-75, 50, 120, 30), 'Back')

    allButtons = (buttonSignIn, buttonExit)
    for b in allButtons:
            b.draw(screen)

    Start = True
    while Start: # main menu loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                Start = False
                pygame.quit()
                sys.exit()

            if 'click' in buttonSignIn.handleEvent(event):
                Start = False
                SignIn.start(False,'')

            if 'click' in buttonExit.handleEvent(event):
                pygame.quit()
                sys.exit()

            if 'click' in buttonBack.handleEvent(event):
                screen.blit(pygame.image.load('images/ivanaivazovsky.png').convert(),(0,0))

                for b in allButtons:
                    b.draw(screen)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()
