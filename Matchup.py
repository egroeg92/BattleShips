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
WINDOWWIDTH = 860
WINDOWHEIGHT = 700


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)
DARKGRAY = (20,20,20)
GRAY = (70,70,70)

FONT = pygame.font.SysFont("Arial", 14)
TITLEFONT = pygame.font.SysFont("Arial", 20)
HEADFONT = pygame.font.SysFont("Arial", 34)
global username
username = ""

def drawChallengePanels(screen):
    
    screen.blit(pygame.image.load('images/matchupbg.png').convert_alpha(),(0,0))

    label = HEADFONT.render('Welcome, '+ username, 1, (255,255,255))
    screen.blit(label, (300, 20))
    
    
    screen.blit(pygame.image.load('images/matchupoverlay.png').convert_alpha(),(20,100))
    pygame.draw.rect(screen, DARKGRAY, [20, 100, 400, 30])
    screen.blit(TITLEFONT.render("ONLINE: ", 1, WHITE),(180,105))
    
    screen.blit(pygame.image.load('images/matchupoverlay1.png').convert_alpha(),(440,100))
    pygame.draw.rect(screen, DARKGRAY, [440, 100, 400, 30])
    screen.blit(TITLEFONT.render("CHALLENGES: ", 1, WHITE),(570,105))


def listener(clientsocket,SCREEN):
    global buttonlist
    global challengelist
    global opp
    global user
    global Set_up
    people_list = []
    user = 'null'
    print 'listening '
 
    while True: 
        data = clientsocket.recv(1024)
        print 'data rec = '+data
        

        if data == 'Signout':
            break
        
        elif data == 'Setup':
            Set_up = True
            break

        dataList = data.split(':')

        if len(dataList) > 1:
            if dataList[1] == 'CHALLENGED':
                challenger = dataList[2]
                print 'challenger '+str(challenger)
                if challenger not in challengelist:
                    challengelist.append(challenger)
                print 'challenge list '+str(challengelist)
            
            elif dataList[1] == 'ACCEPTED':
                print 'CHALLENGE ACCEPTED FROM '+str(dataList[2])
                opp = dataList[2]
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
            if user == '\'\'':
                import string
                import random
                user = ''.join(random.choice(string.lowercase) for x in range(5))
                print user
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
    drawChallengePanels(SCREEN)
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 630, 120, 30), 'Log Out')
    buttonExit.draw(SCREEN)
    
    x = 150
    buttonList = []
    for y in people_list :
        SCREEN.blit(pygame.image.load('images/matchupnamebg.png').convert_alpha(),(20,x-20))

       
        
        l = str(y)[1:-1].split(';')
        print "Y STRING " +y
        
        person = FONT.render(l[0],1,GREEN)
        SCREEN.blit(person,(40,x))
        wins = FONT.render("Wins: "+str(l[2]), 1, WHITE)
        loss = FONT.render("Losses: " + str(l[4]), 1, WHITE)
        
        SCREEN.blit(wins,(40, x+20))
        SCREEN.blit(loss,(110, x+20))
        
        button = pygbutton.PygButton((300,x+5,100,30), "challenge")
        button.draw(SCREEN)
        buttonList.append((button,str(y)))
        x = x + 80

    x = 150
    for c in challengelist:
        SCREEN.blit(pygame.image.load('images/matchupnamebg.png').convert_alpha(),(440,x-20))

        ch = 'chal'+str(c)
        l = c.split(';')
        msg = str(l[0]) + " has sent you a challenge!"
        SCREEN.blit(FONT.render(msg,1,(255,255,255)),(460,x+10))
        button = pygbutton.PygButton((720,x+5,100,30), "accept")
        button.draw(SCREEN)
        buttonList.append((button,ch))
        x = x + 80

    pygame.display.update()
    return buttonList


def start(clientsocket,un):
    global username
    username = un
    print 'Matchup'
    global SCREEN
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption("Match up")

    drawChallengePanels(SCREEN)

    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2-60, 630, 120, 30), 'Log Out')
    buttonExit.draw(SCREEN)
    pygame.display.update()
    
    clientsocket.send('Matchup:'+un)
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
#         drawChallengePanels(SCREEN)
#         buttonExit.draw(SCREEN)

        if Set_up == True:
            Setup.start(clientsocket,opp,user,un)
            break
        
        for event in pygame.event.get():
            if 'click' in buttonExit.handleEvent(event):
                clientsocket.send("Signed Out:"+str(un))
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
                        
                        
                        
