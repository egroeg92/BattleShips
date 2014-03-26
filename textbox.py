import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *

def get_input():
    while True:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass

def display(screen,message):
    font = pygame.font.SysFont("Arial", 14)
    #surface ,color, rectangle, width
    pygame.draw.rect(screen, (0,0,0),((screen.get_width()/2) - 100, (screen.get_height() / 2) - 10, 200,20),0)
#     pygame.draw.rect(screen, (255,255,255),((screen.get_width() /2 ) - 102, (screen.get_height() / 2) - 12, 224, 24), 1)
    
    if len(message) != 0 :
        screen.blit(font.render(message, 1, (255,255,0)),((screen.get_width()/2)-100,(screen.get_height()/2) - 10))
    pygame.display.flip()
    
def start(screen, message):
    pygame.font.init()
    input = []
    display(screen, message+" : " + string.join(input,""))
        
    while True:
        display(screen, message+" : " + string.join(input,""))
        
        key = get_input()
        if key == K_BACKSPACE:
            input = input[0:-1]
        
        elif key == K_RETURN:
            pygame.draw.rect(screen, (0,0,0),((screen.get_width()/2) - 100, (screen.get_height() / 2) - 10, 200,20),0)
            pygame.display.flip()
            break
        else:
            input.append(chr(key))

       
       
    return string.join(input,"")
# 
def main():
  screen = pygame.display.set_mode((320,240))
  print start(screen, "Name") + " was entered"
  
if __name__ == '__main__': main()
    