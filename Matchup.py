"""

Author: George Macrae
2014

"""

import pygame, pygbutton, sys

from pygame.locals import *
from socket import *

import threading

import Start
import textbox

import Setup

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)

FONT = pygame.font.SysFont("Arial", 14)

def listener(clientsocket,SCREEN):
    global buttonlist
    global challengelist
    global opp
    global user
    global Set_up
    user = 'null'
    print 'listening '
 
    while True: 
        data = clientsocket.recv(1024)
        print 'data rec = '+data
        
        if data[0:10] == 'CHALLENGED':
            challenger = data[10:]
            print 'challenger '+str(challenger)
            if challenger not in challengelist:
                challengelist.append(challenger)
            print 'challenge list '+str(challengelist)
        
        elif data == 'Signout':
            break
        
        elif data == 'Setup':
            Set_up = True
            break

        elif data[0:8] == 'ACCEPTED':
            print 'CHALLENGE ACCEPTED FROM '+str(data[8:])
            opp = data[8:]
            clientsocket.send('SetupA')
            Set_up = True
            break

        else:
            
            people_list = []
            people = str(data)[1:-1]
            temp_people_list = people.split(", ")
            
            print 'people'+people
            if user == 'null':
                user = temp_people_list[-1]
            for x in temp_people_list:
                if x != user:
                    people_list.append(x)
            for y in challengelist:
                if y not in temp_people_list:
                    challengelist.remove(y)
            print 'people list'+str(people_list)
            print 'user '+str(user)

        buttonlist = setOnlineDisplay(SCREEN,people_list,clientsocket,buttonlist,challengelist)


        
def setOnlineDisplay(SCREEN, people_list, clientsocket,buttonList,challengelist):
    
    print "update screen"
    windowBgColor = BLACK
    SCREEN.fill(windowBgColor)
    label = FONT.render("Match up", 1, (255,255,0))
    SCREEN.blit(label, (100, 100))
    
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 250, 120, 30), 'back')
    buttonExit.draw(SCREEN)
    x = 120
    buttonList = []
    for y in people_list :
        person = FONT.render(str(y),1,(255,255,0))
        SCREEN.blit(person,(120,x))

        button = pygbutton.PygButton((170,x,120,30), "challenge "+str(y))
        button.draw(SCREEN)
        buttonList.append((button,str(y)))
        x = x+30

    x = 120
    for c in challengelist:
        ch = 'chal'+str(c)
        button = pygbutton.PygButton((400,x,120,30), "accept"+str(c))
        button.draw(SCREEN)
        buttonList.append((button,ch))
        x = x+30

    pygame.display.update()
    return buttonList


def start(clientsocket,un):

    print 'Matchup'
    windowBgColor = BLACK

    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Welcome '+un)

    SCREEN.fill(windowBgColor)
    label = FONT.render("Match up", 1, (255,255,0))
    SCREEN.blit(label, (100, 100))
    
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 250, 120, 30), 'back')
    buttonExit.draw(SCREEN)

    pygame.display.update()
    
    clientsocket.send('Matchup')
    print 'T1 '+ str(threading.activeCount())
    l_thread = threading.Thread(target = listener, args = (clientsocket,SCREEN))
    

    global opp
    global buttonlist 
    global challengelist
    global user
    global Set_up
    user = 'null'
    challengelist = []
    buttonlist = []
    
    l_thread.start()

    Set_up = False
    print 'T2 '+ str(threading.activeCount())
    while True :
        
        if Set_up == True:
            Setup.start(clientsocket,opp,user,un)
            break
        
        for event in pygame.event.get():
            if 'click' in buttonExit.handleEvent(event):
                clientsocket.send("Signed Out")
                # May need to lock
                clientsocket.close()
                print 'Back-matchup'
                Start.main()
                break

            if not buttonlist:
                continue
            for x in buttonlist:
                req = x[1]
                if 'click' in x[0].handleEvent(event):                    
                    # button press to accept challenge
                    if req[0:4] == 'chal':
                        clientsocket.send("Accept:"+req[4:])
                        clientsocket.send("SetupC")
                        opp = req[4:]

                    else:
                    #    button press to send challenge
                        clientsocket.send("Challenge:"+x[1])