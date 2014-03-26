import pygame, pygbutton, sys
from pygame.locals import *
import SignIn

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)

FONT = pygame.font.SysFont("Arial", 14)


def main():
    windowBgColor = BLACK

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Game Menu')



    # menu buttons
    buttonSignUp = pygbutton.PygButton((WINDOWWIDTH/2-60, 50, 120, 30), 'Sign Up')
    buttonSignIn = pygbutton.PygButton((WINDOWWIDTH/2-60, 100, 120, 30), 'Connect to Server')
    buttonOptions = pygbutton.PygButton((WINDOWWIDTH/2-60, 150, 120, 30), 'Game Options')
    buttonCredits = pygbutton.PygButton((WINDOWWIDTH/2-60, 200, 120, 30), 'Credits')
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 250, 120, 30), 'Exit')
    buttonInstructions = pygbutton.PygButton((WINDOWWIDTH/2-60, 300, 120, 30), 'INSTRUCTIONS')

    buttonBack = pygbutton.PygButton((WINDOWWIDTH/2-60, 50, 120, 30), 'BACK <')

    allButtons = (buttonSignUp, buttonSignIn, buttonOptions, buttonCredits, buttonExit,buttonInstructions)
    for b in allButtons:
            b.draw(screen)

    Start = True
    while Start: # main menu loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                Start = False
                pygame.quit()
                sys.exit()

            if 'click' in buttonSignUp.handleEvent(event):
                windowBgColor = BLACK
                screen.fill(windowBgColor); #erases the prev screen
                label = FONT.render("MATCHUP", 1, (255,255,0))
                screen.blit(label, (100, 100))
                buttonBack.draw(screen)
                pygame.display.update()

            if 'click' in buttonSignIn.handleEvent(event):
                Start = False
                SignIn.start(False,'')

            if 'click' in buttonInstructions.handleEvent(event):
                windowBgColor = GREEN
                screen.fill(windowBgColor); #erases the prev screen
                label = FONT.render("INSTRUCTIONS", 1, (255,255,0))
                screen.blit(label, (100, 100))
                buttonBack.draw(screen)
                pygame.display.update()

            if 'click' in buttonOptions.handleEvent(event):
                windowBgColor = BLUE
                screen.fill(windowBgColor); #erases the prev screen
                label = FONT.render("OPTIONS", 1, (255,255,0))
                screen.blit(label, (100, 100))
                buttonBack.draw(screen)
                #buttonBack = pygbutton.PygButton((WINDOWWIDTH/2-60, 50, 120, 30), 'BACK <')
                buttonBack.draw(screen)
                pygame.display.update()

            if 'click' in buttonCredits.handleEvent(event):
               screen.fill(windowBgColor); #erases the prev screen
               label = FONT.render("CREDITS", 1, (255,255,0))
               screen.blit(label, (100, 100))
               buttonBack.draw(screen)
               pygame.display.update()
                
            if 'click' in buttonExit.handleEvent(event):
                pygame.quit()
                sys.exit()

            if 'click' in buttonBack.handleEvent(event):
                windowBgColor = BLACK
                screen.fill(windowBgColor); #erases the prev screen
                for b in allButtons:
                    b.draw(screen)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
