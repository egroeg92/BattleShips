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
    pygame.draw.rect(screen, (255,255,255),(195,440,450,40),0)
#     pygame.draw.rect(screen, (255,255,255),((screen.get_width() /2 ) - 102, (screen.get_height() / 2) - 12, 224, 24), 1)
    
    if len(message) != 0 :
        screen.blit(font.render(message, 1, (0,0,0)),(200,450))
    pygame.display.flip()
    
def start(screen, message):
    pygame.font.init()
    input = []
    display(screen, string.join(input,""))
    valid = [K_PERIOD, K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9,
             K_a, K_b,K_c, K_d, K_e, K_f, K_g, K_h, K_i, K_j, K_k, K_l, 
             K_m, K_n, K_o, K_p, K_q , K_r , K_s, K_t, K_u, K_v, K_w, 
             K_x, K_y, K_z]

    while True:
        display(screen, string.join(input,""))
        
        key = get_input()
        if key == K_BACKSPACE:
            input = input[0:-1]
        
        elif key == K_RETURN:
            pygame.draw.rect(screen, (255,255,255),(195,440,450,40),0)
            pygame.display.flip()
            break
        elif key in valid :
            input.append(chr(key))

       
       
    return string.join(input,"")
# 
def main():
  screen = pygame.display.set_mode((320,240))
  print start(screen, "Name") + " was entered"
  
if __name__ == '__main__': main()
    