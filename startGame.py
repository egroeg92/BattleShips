import pygame, pygbutton, sys
from pygame.locals import *
from socket import *
import threading
import Matchup
from Board import Board
from Ship import Ship
from PlayerState import PlayerState
from Game import Game

FPS = 30
WINDOWWIDTH = 800
WINDOWHEIGHT = 750

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)

moveValid = False
positionValid = False
VISIBLE = True

FONT = pygame.font.SysFont("Arial", 14)
d = 85
def listener(clientsocket,screen):
    global active
    global turn
    global op_positioned
    # global turnType
    while True:
        data = clientsocket.recv(1024)
        print 'Active Game data recv ' +str(data)
        # screen.fill(BLACK)  # Put this here temporarily to see the output
        pygame.draw.rect(screen, BLACK, [100, 650 , 500, 50])
        # updateBoard(game.getBoard(),screen)

        if data == 'Win':
            print 'winner'
            active = False
            # Matchup.start(clientsocket,'username')

            break
        if data == 'Lose':
            print 'loser'
            # Matchup.start(clientsocket,'username')

            active = False
            break
        dataList = []

        dataList = data.split(':')
        if dataList[0] == 'Move':
            #print 'moving'

            
            ship = op_shiplist[int(dataList[1])]
            #print str(ship.getName())
            x = int(dataList[2])
            y = int(dataList[3])
            vis = dataList[4]
            ship.setSelected(True)
            
            if vis == 'True':
                game.moveShip(x,y,True)
                game.getBoard().setNot(-1,-1,screen)
                updateBoard(game.getBoard(),screen)
            else:
                game.moveShip(x,y,False)
                
                string =  'collision at '+ str(x)  +' ' +str(y)
                notifier = FONT.render(string, 1, (255,255,255))
                screen.blit(notifier, (200, WINDOWHEIGHT - 100))               
                game.getBoard().setNot(x,y,screen)
                updateBoard(game.getBoard(),screen)


            ship.setSelected(False)
            # ship.move(int(dataList[2]))
            turn = True
        
        elif dataList[0] == 'Turn':
            #print'turning'
            ship = op_shiplist[int(dataList[1])]
            rot = int(dataList[2])
            degree = dataList[3]
            vis = dataList[4]

            if degree =='True':
                if vis == 'True':
                    game.rotate(ship,rot,True,True)
                    game.getBoard().setNot(-1,-1,screen)
                    updateBoard(game.getBoard(),screen)
                else:
                    game.rotate(ship,rot,True,False)
                    string =  'collision at '+ str(x) +' ' +str(y)
                    notifier = FONT.render(string, 1, (255,255,255))
                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                    game.getBoard().setNot(x,y,screen)
                    updateBoard(game.getBoard(),screen)




                
            else:
                if vis == 'True':
                    game.getBoard().setNot(-1,-1,screen)                    
                    game.rotate(ship,rot,False,True)
                else:
                    game.rotate(ship,rot,False,False)
                    string =  'collision at '+ str(x)  +' ' +str(y)
                    notifier = FONT.render(string, 1, (255,255,255))
                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                    updateBoard(game.getBoard(),screen)
                    game.getBoard().setNot(x,y,screen)




            turn = True
        
        elif dataList[0] == 'Cannon':
            #print 'cannon'

            ship = op_shiplist[int(dataList[1])]
            x = int(dataList[2])
            y = int(dataList[3])
            ship.setSelected(True)
            resultString = game.fireCannon(x,y)
            # resultString = resultString.split(':')
            resultString = resultString +' x = ' + str(x) +' y = ' + str(y)

            print resultString

            notifier = FONT.render(resultString, 1, (255,255,255))
            ship.setSelected(False)
            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
            game.getBoard().setNot(x,y,screen)
            updateBoard(game.getBoard(),screen)

            turn = True

        elif dataList[0] == 'HCannon':
            #print 'heavycannon'
            ship = op_shiplist[int(dataList[1])]
            x = int(dataList[2])
            y = int(dataList[3])
            ship.setSelected(True)
            resultString = game.fireHeavyCannon(x,y)
            # resultString = resultString.split(':')
            # resultString = resultString
            resultString = resultString +' x = ' + str(x) +' y = ' + str(y)

            print resultString

            
            notifier = FONT.render(resultString, 1, (255,255,255))
            ship.setSelected(False)
            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
            game.getBoard().setNot(x,y,screen)
            updateBoard(game.getBoard(),screen)

            turn = True
        elif dataList[0] == 'Torpedo':
            #print 'torpedo'
            ship = op_shiplist[int(dataList[1])]
            x = int(dataList[2])
            y = int(dataList[3])
            ship.setSelected(True)
            game.fireTorpedo
            resultString = game.fireTorpedo(x,y)

            print resultString
            # resultString = resultString.split(':')
            # resultString = resultString
            
            resultString = resultString +' x = ' + str(x) +' y = ' + str(y)

            print resultString



            notifier = FONT.render(resultString, 1, (255,255,255))
            ship.setSelected(False)
            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
            game.getBoard().setNot(x,y,screen)
            updateBoard(game.getBoard(),screen)

            turn = True

        else:
            dataList = data[1:-1]
            dataList = dataList.replace(' ','')
            dataList = dataList.replace('\'','')
            dataList = dataList.split(',')
            #print dataList
            
            if dataList[0] == 'Position':
                dataList = dataList[:-2]
                #print 'position'
                #print 'dataList',dataList
                dataList.reverse()
                #print 'dataList R',dataList
                #print len(dataList)
                # dataList.pop()

                while len(dataList) >0:
                    dataList.pop()
                    ship = op_shiplist[int(dataList.pop())]
                    #print "SHIP NAME"+str(ship.getName())
                    x = int(dataList.pop())
                    y = int(dataList.pop())
                    d = dataList.pop()
                    ship.setSelected(True)
                    if Player1: #then positioning player 2
                        if d == 'W':
                            p =0
                        elif d =='N':
                            p =1
                        elif d =='E':
                            p =2
                        elif d == 'S':
                            p = 3
                    else:
                        if d == 'E':
                            p = 0
                        elif d =='S':
                            p =1
                        elif d =='W':
                            p =2
                        elif d =='N':
                            p = 3

                    game.positionShip(x, y, p)
                    ship.setSelected(False)

                op_positioned = True


#         if dataList[0] == 'Move'
        

        
def main(clientsocket, opp,user,player):
    
    # for offine play (for debugging)

    global offline
    offline = False
    if clientsocket == 'offline':
        offline = True

    # True if this client is player 1
    global Player1
    
    Player1 = False
    if player:
        Player1 = True
        print 'PLAYER 1!!!!!!!!'
    else:
        print 'PLAYER 2!!!!!!!!'

    # true if the op has placed there ships
    global op_positioned 
    op_positioned = False
        

    ## creating the screen

    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Battle Ships')
    
    ## Game object

    global game
    game = Game(Player1);
    

    global colx
    global coly

    # colx = -1
    # coly = -1

    ## creating the button objects

    buttonRotate = pygbutton.PygButton((570, WINDOWHEIGHT - 100, 120, 30), 'Rotate Ship')
    buttonMove = pygbutton.PygButton((200, WINDOWHEIGHT - 100, 120, 30), 'Move Ship')
    buttonTurn = pygbutton.PygButton((370, WINDOWHEIGHT - 100, 120, 30), 'Turn Ship')
    buttonFire = pygbutton.PygButton((540, WINDOWHEIGHT - 100, 120, 30), 'Fire Weapon')
    
    shipOptions = [buttonMove, buttonTurn, buttonFire]
    
    positionOptions = [buttonRotate]

    buttonCannon = pygbutton.PygButton((70, WINDOWHEIGHT - 40, 120, 30), 'Cannon')
    buttonHeavyCannon = pygbutton.PygButton((70, WINDOWHEIGHT - 70, 120, 30), 'HeavyCannon')
    buttonTorpedo = pygbutton.PygButton((70, WINDOWHEIGHT - 100, 120, 30), 'Torpedo')
  
    buttonExit = pygbutton.PygButton((WINDOWWIDTH/2+30, 700, 120, 30), 'Quit')
    buttonPositionShips = pygbutton.PygButton((WINDOWWIDTH/2-150, 700, 120, 30), 'Done Positioning')
    
    
    positiontext = FONT.render("Click on your ships to position them", 1, (255,255,255))
    
    ## start the listener thread if playing not offline

    if not offline:
        l_thread = threading.Thread(target = listener, args = (clientsocket,screen))
        l_thread.start()

    ## game active

    global active
    active = True

    ## turn is true if its your turn, false if its the opponents turn

    global turn
    
    global shiplist
    global op_shiplist
    
    shiplist = []
    op_shiplist = []
    
    shiplist = game.getCurrentPlayer().getShipList()
    op_shiplist = game.getOpponent().getShipList()

    turn = True

    global turnType
    turnType = "position"

    global positioned 
    positioned = False
    
    global positionRotation
    positionRotation = 0

    global resultString
    resultString = ""

    ## booleans for what kind of weapon options to display (initiated to none)
    cannon = False
    torpedo = False
    hcannon = False 


#####################################################
##                                                 ##
##              MAIN GAME LOOP                     ##
##                                                 ##
#####################################################
    while True:
        if active != True:
            break

        ## if offline its always your turn, (for debugging)
        if offline:
            turn = True

        ## Player 1 always has first turn 
        if Player1 and op_positioned == True and turnType == "":
            turn = True
            op_positioned = False
        
        ## can only quit if its your turn

        if turn:
            buttonExit.draw(screen)
            
            if not positioned:
                screen.blit(positiontext, (200, WINDOWHEIGHT - 100))
                buttonPositionShips.draw(screen)
        
        else:
            updateBoard(game.getBoard(),screen)


        game.getBoard().animate(screen,(pygame.time.get_ticks()/500)%2)

        ## draw the ships
        for s in shiplist:
            if (s.isSelected() and positioned):
                screen.fill(BLACK)  # Put this here temporarily to see the output
                for o in shipOptions:
                    o.draw(screen)
        
        if (turnType == "positionActive"):
            for o in positionOptions:
                o.draw(screen)

        ## if firing
        if (turnType == "fire"):
            screen.fill(BLACK);
            buttons = []
            for ship in shiplist:
                if ship.isSelected():
                    cannon = False
                    torpedo = False
                    hcannon = False    
                    weaponList = ship.getWeaponList()
                    
                    for weapon in weaponList:
                        if weapon.getName() == "Cannon":
                            buttons.append(buttonCannon)
                            cannon = True
                        if weapon.getName() == "HeavyCannon":
                            buttons.append(buttonHeavyCannon)
                            hcannon = True
                        if weapon.getName() == "Torpedo":
                            buttons.append(buttonTorpedo)
                            torpedo = True
            for button in buttons:
                button.draw(screen)


########################################################
##                                                    ##
##                    EVENT LOOP                      ##
##                                                    ##
########################################################  

        for event in pygame.event.get():

            ## set isSelected to True if a ship isSelected

            for ship in shiplist:
                isSelected = True
                if ship.isSelected():
                    break
                isSelected = False

            ## Events only matter if its the clients turn
            if turn:

                ##  QUITTING
                buttonExit.draw(screen)

                if 'click' in buttonExit.handleEvent(event) and (turnType == '' or turnType == 'position'):
                    print 'quit'
                    if offline:
                        sys.exit();
                    else:
                        clientsocket.send("LoseGame")
                        clientsocket.send("WinGame")

                ## MOVING

                if turnType == "move":
                    if event.type == pygame.MOUSEMOTION:
                        # game.getBoard().animate(screen,(pygame.time.get_ticks()/500)%2)

                        for ship in shiplist:
                            if ship.isSelected():
                                
                                x, y = event.pos
                                x = (x - d) / 21
                                y = (y - 10) / 21
                                
                                
                                game.getBoard().paint(screen)
                                
                         
                                if ship.getOrientation() == "E":
                                    if x >= (ship.getSize()-1) and x <= 29 and y >= 0 and y <= 29:
                                        drawShip(screen, ship, x, y, 0, game,screen)
                                        
                                elif ship.getOrientation() == "W":
                                    if x <= 29 - ship.getSize() + 1 and x >= 0 and y >= 0 and y <= 29:
                                        drawShip(screen, ship, x, y, 0, game,screen)
                                
                                elif ship.getOrientation() == "S":
                                    if x >= 0 and x <= 29 and y >= ship.getSize() - 1 and y <= 29:
                                        drawShip(screen, ship, x, y, 0, game,screen)
                                        
                                elif ship.getOrientation() == "N":
                                    if x >= 0 and x <= 29 and y >= 0 and y <= 29 - ship.getSize() + 1:
                                        drawShip(screen, ship, x, y, 0, game,screen)
             
                    elif event.type == pygame.MOUSEBUTTONUP: 
                        for ship in shiplist:
                            if ship.isSelected():
                                if moveValid:
                                    x, y = event.pos
                                    x = (x - d) / 21
                                    y = (y - 10) / 21
                                    

                                    if ship.getOrientation() == "E":
                                        if x >= (ship.getSize()-1) and x <= 29 and y >= 0 and y <= 29:
                                            if VISIBLE:
                                                #print "move"
                                                game.moveShip(x, y, True);
                                                if not offline:
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(x)+':'+str(y)+':True')
                                                    turn = False
                                            else:
                                                game.moveShip(x, y, False)
                                                print "COLLISION"


                                                string =  'collision at '+ str(x) +str(y)
                                                notifier = FONT.render(string, 1, (255,255,255))
                                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                                updateBoard(game.getBoard(),screen)

                                                print "CO",colx,coly
                                                if not offline:
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(colx)+':'+str(coly)+':False')
                                                    turn = False
                                    
                                    elif ship.getOrientation() == "W":
                                        if x <= 29 - ship.getSize() and x >= 0 and y >= 0 and y <= 29:
                                            if VISIBLE:
                                                #print "move"
                                                game.moveShip(x, y, True);
                                                if not offline:
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(x)+':'+str(y)+':True')
                                                    turn = False
                                            else:
                                                print "COLLISION"

                                                game.moveShip(x, y, False)
                                                string =  'collision at '+ str(x) +str(y)
                                                notifier = FONT.render(string, 1, (255,255,255))
                                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                                updateBoard(game.getBoard(),screen)

                                                print "CO",colx,coly
                                                if not offline:
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(colx)+':'+str(coly)+':False')
                                                    turn = False
                                    elif ship.getOrientation() == "S":
                                        back_postion = ship.getPositionList()[-1]
            
                                        if x >= 0 and x <= 29 and y > back_postion[1] and y <= 29:
                                            if VISIBLE:
                                                #print "move"
                                                game.moveShip(x, y, True);
                                                if not offline:
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(x)+':'+str(y)+':True')
                                                    turn = False
                                            else:
                                                print "COLLISION"

                                                game.moveShip(x, y, False)
                                                string =  'collision at '+ str(x) +str(y)
                                                notifier = FONT.render(string, 1, (255,255,255))
                                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                                updateBoard(game.getBoard(),screen)

                                                if not offline:
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(colx)+':'+str(coly)+':False')
                                                    turn = False

                                    elif ship.getOrientation() == "N":
                                        if x >= 0 and x <= 29 and y >= 0 and y <= 29-ship.getSize():
                                            if VISIBLE:
                                                #print "move"
                                                game.moveShip(x, y, True);
                                                if not offline:
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(x)+':'+str(y)+':True')
                                                    turn = False

                                            else:
                                                game.moveShip(x, y, False)
                                                print "COLLISION"

                                                string =  'collision at '+ str(x) +str(y)
                                                notifier = FONT.render(string, 1, (255,255,255))
                                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                                updateBoard(game.getBoard(),screen)

                                            if not offline:
                                                clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(colx)+':'+str(coly)+':False')
                                                turn = False
                               
                                ship.setSelected(False)
                                global turnType
                                turnType = ""
                                screen.fill(BLACK);
                                

                ## POSITIONING 

                elif turnType == "positionActive":
                    if event.type == pygame.MOUSEMOTION:
                        for ship in shiplist:
                            if ship.isSelected():
                                x, y = event.pos
                                x = (x - d) / 21
                                y = (y - 10) / 21
                                
                                newOrientation = ship.getOrientation()
                                rotation = positionRotation

                                while (rotation > 0):
                                    if (newOrientation == "E"):
                                        newOrientation = "S"
                                        rotation = rotation - 1
                                    elif (newOrientation == "S"):
                                        newOrientation = "W"
                                        rotation = rotation - 1
                                    elif (newOrientation == "W"):
                                        newOrientation = "N"
                                        rotation = rotation - 1
                                    elif (newOrientation == "N"):
                                        newOrientation = "E"
                                        rotation = rotation - 1
                                        
                                game.getBoard().paint(screen)
                                global moveValid
                                moveValid = False
                                
                                if newOrientation == "E":
                                    if x >= (ship.getSize()-1) and x <= 29 and y >= 0 and y <= 29:
                                        drawShip(screen, ship, x, y, positionRotation, game,screen)
                                        
                                elif newOrientation == "W":
                                    if x <= 29 - ship.getSize()+1 and x >= 0 and y >= 0 and y <= 29:
                                        drawShip(screen, ship, x, y, positionRotation, game,screen)
                                
                                elif newOrientation == "S":        
                                    if x >= 0 and x <= 29 and y >= ship.getSize() - 1 and y <= 29:
                                        drawShip(screen, ship, x, y, positionRotation, game,screen)
                                        
                                elif newOrientation == "N":
                                    if x >= 0 and x <= 29 and y >= 0 and y <= (29 - ship.getSize() + 1):
                                        drawShip(screen, ship, x, y, positionRotation, game,screen)  
                                                   
                    elif "click" in buttonRotate.handleEvent(event) and turnType == 'positionActive':
                        for ship in shiplist:
                            if ship.isSelected():
                                old = positionRotation
                                global positionRotation
                                positionRotation = old + 1
                                
                                if positionRotation == 4:
                                    global positionRotation
                                    positionRotation = 0

                                screen.fill(BLACK);
                                
                    elif event.type == pygame.MOUSEBUTTONUP: 
                        for ship in shiplist:
                            if ship.isSelected():
                                if moveValid:
                                    x, y = event.pos
                                    x = (x - d) / 21
                                    y = (y - 10) / 21

                                    
                                    game.positionShip(x, y, positionRotation);

                                    ship.setSelected(False)

                                    turnType = "position"
                                    positionRotation = 0
                                    screen.fill(BLACK);


                ##  TURNING

                elif turnType == "turn":

                    if event.type == pygame.MOUSEMOTION:
                        for ship in shiplist:
                            if ship.isSelected():            

                                x, y = event.pos
                                x = (x - d) / 21
                                y = (y - 10) / 21

                                game.getBoard().paint(screen)
                                if ship.getTurnRadius() == 1:
                                    if ship.getOrientation() == 'E' :

                                        if x >= ship.getPositionList()[-1][0] and x <=29 and y > ship.getPositionList()[-1][1] and y <= 29:
                                            drawShip(screen, ship, x, y+(ship.getSize()-2), 1, game,screen)
                                            rot = 1 
                                        elif x >= ship.getPositionList()[-1][0] and x <=29 and y < ship.getPositionList()[-1][1] and y >= ship.getSize() - 2:
                                            drawShip(screen, ship, x, y-(ship.getSize()-2), 3, game,screen)
                                            rot = 3
                                    elif ship.getOrientation() == 'W' :
                                        #print 'Turn west',y, ship.getPositionList()[0][1]

                                        if y > ship.getPositionList()[0][1] and y- ship.getSize() +2 >= 0    and y <=29-ship.getSize()+2 and x>=0 and x<=29:
                                            drawShip(screen, ship, x, y+(ship.getSize()-2), 3, game,screen)
                                            rot = 3
                                             
                                        elif y< ship.getPositionList()[0][1]and y - ship.getSize() +2  >= 0    and y <=29-ship.getSize()+2 and x>=0 and x<=29:
                                            drawShip(screen, ship, x, y-(ship.getSize()-2), 1, game,screen)
                                            rot = 1

                                    elif ship.getOrientation() == 'S' :
                                        #print 'Turn south',x, ship.getPositionList()[0][0]

                                        if x >= ship.getPositionList()[0][0] and x <=29-ship.getSize()+2 and y>=0 and y<=29:
                                            drawShip(screen, ship, x+(ship.getSize()-2), y, 3, game,screen)
                                            rot = 3
                                             
                                        elif x< ship.getPositionList()[0][0]and x - ship.getSize() +2  >= 0    and x <=29-ship.getSize()+2 and y>=0 and y<=29:
                                            drawShip(screen, ship, x -(ship.getSize()-2), y, 1, game,screen)
                                            rot = 1

                                    elif ship.getOrientation() == 'N' :
                                        #print 'Turn North',x, ship.getPositionList()[0][0]

                                        if x > ship.getPositionList()[0][0] and x <=29-ship.getSize()+2 and y>=0 and y<=29:
                                            drawShip(screen, ship, x +(ship.getSize()-2), y, 1, game,screen)
                                            rot = 1
                                             
                                        elif x< ship.getPositionList()[0][0] and x - ship.getSize() +2  >= 0    and x <=29-ship.getSize()+2 and y>=0 and y<=29:
                                            drawShip(screen, ship, x-(ship.getSize()-2), y, 3, game,screen)
                                            rot = 3
                    
                    # For ships that can turn 180
                                if ship.getTurnRadius() == 2:
                                    if ship.getOrientation() == 'E' :
                                        middlex = ship.getPositionList()[1][0]
                                        if y > ship.getPositionList()[0][1] and x> middlex-1 and y- ship.getSize() +2 >= 0    and y <=29-ship.getSize()+2 and x>=0 and x<=29:
                                            drawShip(screen, ship, x, y+(ship.getSize()-3), 1, game,screen)
                                            rot = 1 
                                        elif y< ship.getPositionList()[0][1] and x> middlex-1  and y - ship.getSize() +2  >= 0    and y <=29-ship.getSize()+2 and x>=0 and x<=29:
                                            drawShip(screen, ship, x, y-(ship.getSize()-3), 3, game,screen)
                                            rot = 3
                                        elif y - ship.getSize() +2  >= 0    and y <=29-ship.getSize()+2 and x>=0 and x<=29 :
                                            drawShip(screen,ship,x,y,2,game,screen)
                                            rot = 2

                                    if ship.getOrientation() == 'W' :
                                        middlex = ship.getPositionList()[1][0]
                                        if y > ship.getPositionList()[0][1] and x <middlex+1 and y- ship.getSize() +2 >= 0    and y <=29-ship.getSize()+2 and x>=0 and x<=29:
                                            drawShip(screen, ship, x, y+(ship.getSize()-3), 3, game,screen)
                                            rot = 3
                                             
                                        elif y< ship.getPositionList()[0][1] and x<middlex+1 and y - ship.getSize() +2  >= 0    and y <=29-ship.getSize()+2 and x>=0 and x<=29:
                                            drawShip(screen, ship, x, y-(ship.getSize()-3), 1, game,screen)
                                            rot = 1
                                        elif y - ship.getSize() +2  >= 0    and y <=29-ship.getSize()+2 and x>=0 and x<=29 :
                                            drawShip(screen,ship,x,y,2,game,screen)
                                            rot = 2

                                    elif ship.getOrientation() == 'S' :
                                        middley = ship.getPositionList()[1][1]

                                        if x > ship.getPositionList()[0][0] and y > middley -1 and x- ship.getSize() +2 >= 0    and x <=29-ship.getSize()+2 and y>=0 and y<=29:
                                            drawShip(screen, ship, x+(ship.getSize()-3), y, 3, game,screen)
                                            rot = 3
                                             
                                        elif x< ship.getPositionList()[0][0] and y > middley -1 and x - ship.getSize() +2  >= 0    and x <=29-ship.getSize()+2 and y>=0 and y<=29:
                                            drawShip(screen, ship, x -(ship.getSize()-3), y, 1, game,screen)
                                            rot = 1
                                        elif x- ship.getSize() +2 >=0 and x <= 29-ship.getSize() +2 and y >=0 and y <=29:
                                            drawShip(screen,ship,x,y,2,game,screen)
                                            rot = 2

                                    elif ship.getOrientation() == 'N' :
                                        middley = ship.getPositionList()[1][1]

                                        if x > ship.getPositionList()[0][0] and y < middley +1 and x- ship.getSize() +2 >= 0    and x <=29-ship.getSize()+2 and y>=0 and y<=29:
                                            drawShip(screen, ship, x +(ship.getSize()-3), y, 1, game,screen)
                                            rot = 1
                                             
                                        elif x< ship.getPositionList()[0][0] and y < middley +1 and x - ship.getSize() +2  >= 0    and x <=29-ship.getSize()+2 and y>=0 and y<=29:
                                            drawShip(screen, ship, x-(ship.getSize()-3), y, 3, game,screen)
                                            rot = 3

                                        elif x- ship.getSize() +2 >=0 and x <= 29-ship.getSize() +2 and y >=0 and y <=29:
                                            drawShip(screen,ship,x,y,2,game,screen)
                                            rot = 2


                    
                    elif event.type == pygame.MOUSEBUTTONUP: 
                        for ship in shiplist:
                            if ship.isSelected():
                                if moveValid:
                                    x, y = event.pos
                                    x = (x - d) / 21
                                    y = (y - 10) / 21
                                    if ship.getTurnRadius() == 1:
                                        #TODO, Client socket takes in  more arguments

                                        if VISIBLE:
                                            game.rotate(ship,rot,True, True)
                                            if not offline:
                                                clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:True')
                                                turn = False
                                        else:
                                            game.rotate(ship, rot, True, False)

                                            print "COLLISION"

                                            string =  'turn collision at '+ str(x) +str(y)
                                            notifier = FONT.render(string, 1, (255,255,255))
                                            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                            updateBoard(game.getBoard(),screen)

                                            if not offline:
                                                clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:False')
                                                turn = False
                                    
                                    elif ship.getTurnRadius() == 2:

                                        if VISIBLE:
                                            game.rotate(ship,rot,False, True)
                                            if not offline:
                                                clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:True')
                                                turn = False

                                        else:
                                            game.rotate(ship, rot, False, False)
                                            
                                            print "COLLISION"
                                            string =  'turn collision at '+ str(x) +str(y)
                                            notifier = FONT.render(string, 1, (255,255,255))
                                            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                            updateBoard(game.getBoard(),screen)

                                            if not offline:
                                                clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:False')
                                                turn = False

                                ship.setSelected(False)
                                global turnType
                                turnType = ""
                                screen.fill(BLACK);

                ## FIRING CANNON

                elif turnType == "cannon":                    
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        x = (x - d) / 21
                        y = (y - 10) / 21

                        for ship in shiplist:
                            if ship.isSelected():
                                
                                game.getBoard().paint(screen)
                                if (x,y) in ship.getCannonRange():
                                    drawWeapon(screen, x, y)
                    
                    elif event.type == pygame.MOUSEBUTTONUP:
                        for ship in shiplist:
                            if ship.isSelected():
                                x, y = event.pos
                                x = (x - d) / 21
                                y = (y - 10) / 21
                                crange = firingRange(screen, ship, x, y, "Cannon")
                                
                                if moveValid and x>=0 and x<=29 and y>=0 and y<=29:
                                    resultString = game.fireCannon(x,y)
                                    resultString = resultString.split(':')
                                    if resultString[0] == 'ship sunk ':
                                        resultString = resultString[0]+':'+resultString[1]+'at '+str(x)+' '+str(y)
                                    else:
                                        print resultString
                                        resultString = resultString[0]+'at '+str(x)+' '+str(y)
                                        
                                    ship.setSelected(False)
                                    global turnType
                                    turnType = ""
                                    screen.fill(BLACK);
                                    game.updateRange("cannon", False)
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    updateBoard(game.getBoard(),screen)
                                    if not offline:
                                        clientsocket.send("Cannon:"+str(shiplist.index(ship))+':'+str(x)+":"+str(y))
                                        turn = False
                                else:
                                    moveValid = False
                                    turnType = ""
                                    game.updateRange("",False)
                                    screen.fill(BLACK);
                
                ## FIRING HEAVY CANNON

                elif turnType == "heavycannon":
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        x = (x - d) / 21
                        y = (y - 10) / 21
                        
                        for ship in shiplist:
                            if ship.isSelected():
                                
                                game.getBoard().paint(screen)

                                if (x,y) in ship.getHeavyCannonRange():
                                    drawWeapon(screen, x, y)

                    elif event.type == pygame.MOUSEBUTTONUP:
                        for ship in shiplist:
                            if ship.isSelected():
                                x, y = event.pos
                                x = (x - d) / 21
                                y = (y - 10) / 21

                                hcrange = firingRange(screen, ship, x, y, "HeavyCannon")

                                #print 'x,y ',x,y
                                if moveValid and x>=0 and x<=29 and y>=0 and y<=29:
                                    resultString = game.fireHeavyCannon(x,y)

                                    resultString = resultString.split(':')
                                    if resultString[0] == 'ship sunk ':
                                        resultString = resultString[0]+':'+resultString[1]+'at '+str(x)+' '+str(y)
                                    else:
                                        print resultString
                                        resultString = resultString[0]+'at '+str(x)+' '+str(y)
                                        
                                    ship.setSelected(False)
                                    global turnType
                                    turnType = ""
                                    screen.fill(BLACK);
                                    game.updateRange("heavycannon", False)
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    #print resultString
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    updateBoard(game.getBoard(),screen)
                                    if not offline:
                                        clientsocket.send("HCannon:"+str(shiplist.index(ship))+':'+str(x)+":"+str(y))
                                        turn = False
                                else:
                                    moveValid = False
                                    turnType = ""
                                    game.updateRange("",False)
                                    screen.fill(BLACK)

                ## FIRING TORPEDO

                elif turnType == "torpedo":
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        x = (x - d) / 21
                        y = (y - 10) / 21
                        
                        for ship in shiplist:
                            if ship.isSelected():
                                
                                game.getBoard().paint(screen)
                                if (x,y) in ship.getTorpedoRange():
                                    drawWeapon(screen, x, y)

                    elif event.type == pygame.MOUSEBUTTONUP:
                        for ship in shiplist:
                            if ship.isSelected():
                                x, y = event.pos
                                x = (x - d) / 21
                                y = (y - 10) / 21
                                torpedoRange(screen, ship, x, y, "Torpedo")

                                if moveValid and x>=0 and x<=29 and y>=0 and y<=29:
                                    resultString = game.fireTorpedo(x,y)

                                    resultString = resultString.split(':')

                                    if resultString[0] == 'ship sunk ':
                                        resultString = resultString[0]+':'+resultString[1]+'at '+str(x)+' '+str(y)
                                    else:
                                        print resultString
                                        resultString = resultString[0]+'at '+str(x)+' '+str(y)

                                    ship.setSelected(False)
                                    global turnType
                                    turnType = ""
                                    screen.fill(BLACK);
                                    game.updateRange("torpedo", False)
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    
                                    if not offline:
                                        clientsocket.send("Torpedo:"+str(shiplist.index(ship))+':'+str(x)+':'+str(y))                                   
                                        turn = False
                                else:
                                    moveValid = False
                                    turnType = ""
                                    game.updateRange("",False)
                                    screen.fill(BLACK)
                
                #######################
                ## SETTING TURN TYPES##
                #######################    


                elif 'click' in buttonPositionShips.handleEvent(event) and turnType == "position":
                    global positioned
                    positioned = True
                    string = 'Position:'
                    i = 0
                    for s in shiplist:

                        x = str(s.getPositionList()[0][0])
                        y = str(s.getPositionList()[0][1])
                        p = str(s.getOrientation())
                        string = string + str(i)+':'+ x +':'+ y +':'+ p +':Position:'
                        i += 1
                    #print string
                    if not offline: 
                        clientsocket.send(string)
                    if Player1 and op_positioned == True :
                        turn = True
                    else:
                        turn = False

                    turnType = ""


                    screen.fill(BLACK);                                

                elif 'click' in buttonMove.handleEvent(event) and turnType == '' and isSelected:
                    turnType = "move"

                elif 'click' in buttonFire.handleEvent(event) and turnType == '' and isSelected:
                    turnType = "fire"

                elif 'click' in buttonCannon.handleEvent(event) and turnType == 'fire' and cannon and isSelected:
                    turnType = "cannon"
                    game.updateRange("cannon", True)
                    updateBoard(game.getBoard(),screen)


                elif 'click' in buttonHeavyCannon.handleEvent(event) and turnType == 'fire' and hcannon and isSelected:
                    turnType = "heavycannon"
                    game.updateRange("heavycannon", True)
                    updateBoard(game.getBoard(),screen)
                    #print turnType

                elif 'click' in buttonTorpedo.handleEvent(event) and turnType == 'fire'and torpedo and isSelected:
                    turnType = "torpedo"
                    game.updateRange("torpedo", True)
                    updateBoard(game.getBoard(),screen)                    
                        
                elif 'click' in buttonTurn.handleEvent(event) and turnType == '' and isSelected:
                    turnType = "turn"
                    x,y = event.pos
                    x = (x - d) / 21
                    y = (y - 10) / 21
                                
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    x = (x - d) / 21
                    y = (y - 10) / 21
        
                    if ( x >= 0 and x <= 29 and y >= 0 and y <= 29):
                        #print "hi"
                        print game.getBoard().getSquare(x, y).getObjectOn()
                    
                    total = 10
                    for ship in shiplist:
                        #check if ship was clicked
                        if (x,y) in ship.position:
                            for sh in shiplist:
                                sh.setSelected(False)
    
                            ship.setSelected(True)
                            if not positioned:
                                global turnType
                                turnType = "positionActive"
                            
                            break;                            
                            total = total - 1
                            
                            
                        #ship was not clicked, take off ship options
                    
                    if total == 0:
                        print "ship not detected"
                    if total == 0 and positioned:
                        screen.fill(BLACK);
                        for sh in shiplist:
                            sh.setSelected(False) 
                                
                if turnType != "move" and turnType != "positionActive" and turnType != "turn" and turnType != "cannon" and turnType != "heavycannon" and turnType != "torpedo":

                    updateBoard(game.getBoard(),screen)
                  
def updateBoard(gameBoard,screen):
    gameBoard.paint(screen)
    pygame.display.update()

def drawWeapon(surface, x, y):
    c = (27, 201, 18) #green
    pygame.draw.ellipse(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20], 0)
    pygame.display.update()
    
global pList
def drawShip(surface, ship, x, y, rotation, game,screen):
    global VISIBLE
    VISIBLE = True
    r = rotation
    
    global pList
    pList = ship.getPositionList()
    (x1, y1) = pList[0]
    (x2,y2) = pList[-1]
    
    newOrientation = ship.getOrientation()
    turning = False
    
    global colx 
    global coly 
    colx = -1
    coly = -1

    if rotation != 0 and turnType != "positionActive":
        turning = True

    
    while (rotation > 0):
        if (newOrientation == "E"):
            newOrientation = "S"
            rotation = rotation - 1
        elif (newOrientation == "S"):
            newOrientation = "W"
            rotation = rotation - 1
        elif (newOrientation == "W"):
            newOrientation = "N"
            rotation = rotation - 1
        elif (newOrientation == "N"):
            newOrientation = "E"
            rotation = rotation - 1
    #print newOrientation
    
    global moveValid
    moveValid = True
    board = game.getBoard()
    
    if (newOrientation == "E"):
        if turning:
            
            y0 = y
            x0 = x - ship.getSize() + 1            

            if ship.getTurnRadius() == 1:
                if (x0  == x2 and y0 == y2):
                    #print "r=",r
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if(board.getSquare(i,j).getObjectOn() == ship):
                                continue
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Coral"):
                                print 'hit coral'
                                VISIBLE = True
                                moveValid = False
                                break
                            elif not board.getSquare(i,j).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = j
                            else:
                                #print "found collision item"
                                colx = i
                                coly = j
                                moveValid = False
                                break
                else:
                    moveValid = False
            
            # if turn radius = 180
            elif ship.getTurnRadius() == 2:
                
                if ship.getOrientation() == "W":
                    x0 = x-2
                    y0 = y
                elif ship.getOrientation() == "N":
 
                    x0 = x- ship.getSize() +2
                    y0 = y- ship.getSize() + 2
                
                else: #facing south'
                    x0 = x- ship.getSize() +2
                    y0 = y+ ship.getSize() -2

                #print x0,x1
                #print y0,y1
                if (x0 == x1 and y0 == y1):
                    #print y,y2
                    i = x
                    while i >= x2-1:
                        #print board.getSquare(i,y).getObjectOn()
                        if (board.getSquare(i,y).getObjectOn() != None ):
                            if(board.getSquare(i,y).getObjectOn() == ship):
                                i-=1
                                continue
                            if not board.getSquare(i,y).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = y
                            else:
                                colx = i
                                coly = y
                                moveValid = False
                                break
                        i-=1
                else:
                    moveValid = False

                if (x0 == x1 and y0 == y1):
                    #print "r=",r
                    #print "AHHH: ", ship.getTurnZone(r)                    
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if(board.getSquare(i,j).getObjectOn() == ship):
                                continue
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Coral"):
                                print 'hit coral'

                                moveValid = False
                                break
                            elif not board.getSquare(i,j).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = j
                            else:
                                #print "found collision item"
                                colx = i
                                coly = j
                                moveValid = False
                                break
                else:
                    moveValid = False 

                
            #print moveValid
         

        elif  (turnType != "positionActive" and ((x - x1 ) >= -1 and ( x - x1 ) <= ship.getSpeed() and (y - y1) == 0) or ((y - y1) >= -1 and (y - y1) <= 1 and (x - x1) == 0)):
            i = x1
            # check for obstacles in front
            while i <= x:
                if (board.getSquare(i,y).getObjectOn() != None ):
                    if (board.getSquare(i,y).getObjectOn() == ship):
                        i+=1
                        continue
                    if not board.getSquare(i,y).isVisible():
                        VISIBLE = False
                        colx = i
                        coly = y

                    else:
                        #TODO
                        colx = i
                        coly = y
                        print colx,coly
                        moveValid = False
                        break
                i += 1 
            #check sideways
            if y != y1:
                i = 0
                while i< ship.getSize():
                    if (board.getSquare(x-i,y).getObjectOn() != None):
                        if not board.getSquare(x-i,y).isVisible():
                            VISIBLE = False
                        else:

                            moveValid = False
                            break
                    i+=1
            #check obstacles behind
            elif x-ship.getSize() <= x2-1 :
                if (board.getSquare(x-ship.getSize()+1,y).getObjectOn() != None):
                    if not board.getSquare(x-ship.getSize()+1,y).isVisible():
                        VISIBLE = False
                    else:
                        colx = x-ship.getSize()+1
                        coly = y
                        moveValid = False

        
        elif (turnType == "positionActive" and Player1 and x >= (ship.getSize() - 1) and x <= 14 and y >= 0 and y <= 29):
            i = x-ship.getSize() +1        
            while i <= x:
                #print board.getSquare(i,y).getObjectOn()
                
                if(board.getSquare(i,y).getObjectOn()!= None):
                    if (board.getSquare(i,y).getObjectOn()== ship):
                        i+=1
                        continue
                    
                    moveValid = False
                    break
                i+=1
        elif (turnType == "positionActive" and not Player1 and x <= 29 and x > 14 + ship.getSize() -1 and y >= 0 and y <= 29):
            i = x-ship.getSize() +1        
            while i <= x:
                #print board.getSquare(i,y).getObjectOn()
                
                if(board.getSquare(i,y).getObjectOn()!= None):
                    if (board.getSquare(i,y).getObjectOn()== ship):
                        i+=1
                        continue
                    
                    moveValid = False
                    break
                i+=1
                
                
        else:
            moveValid = False
            
        if moveValid == True:
            color = pygame.Color(194, 242, 221) #green
        else:
            color = pygame.Color(250, 200, 200) #red
        
        #print "Drawing", (x,y)
        
        
        pygame.draw.polygon(surface, color, [(x*20 + x*1 + d , y*20 + y*1 + 10), (x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d+20 - 1, y*20 + y*1 + 20)], 0)
        x = x - 1
        for i in range(ship.getSize() - 1):

            pygame.draw.rect(surface, color, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
            x = x - 1
            i = i + 1
            
    elif (newOrientation == "W"):
        if turning:
            #print ship.getPositionList()
            
            y0 = y
            x0 = x + ship.getSize() - 1            

            #print x0,x2
            #print y0,y2
            if ship.getTurnRadius() == 1:
                if (x0  == x2 and y0 == y2):
                    #print "r=",r
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if(board.getSquare(i,j).getObjectOn() == ship):
                                continue
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Coral"):
                                print 'hit coral'
                                VISIBLE = True
                                moveValid = False
                                break
                            elif not board.getSquare(i,j).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = j
                            else:
                                #print "found collision item"
                                colx = i
                                coly = j
                                moveValid = False
                                break
                else:
                    moveValid = False

            # if turn radius = 180
            elif ship.getTurnRadius() == 2:
                
                if ship.getOrientation() == "E":
                    x0 = x+2
                    y0 = y



                elif ship.getOrientation() == "N":
 
                    x0 = x + ship.getSize() -2
                    y0 = y - ship.getSize() + 2
                
                else: #facing south'
                    x0 = x + ship.getSize() - 2
                    y0 = y + ship.getSize() - 2

                #print 'x ', x0,x1
                #print 'y' , y0,y1
                if (x0 == x1 and y0 == y1):
                    #print x,x2+1
                    #print y
                    i = x2+1
                    while i >= x:
                        #print board.getSquare(i,y).getObjectOn()
                        if (board.getSquare(i,y).getObjectOn() != None ):
                            if(board.getSquare(i,y).getObjectOn() == ship):
                                i-=1
                                continue
                            if not board.getSquare(i,y).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = y
                            else:
                                colx = i
                                coly = y
                                moveValid = False
                            break
                        i-=1
                else:
                    moveValid = False
                if (x0 == x1 and y0 == y1):
                    #print "r=",r
                    #print "AHHH: ", ship.getTurnZone(r)                    
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if(board.getSquare(i,j).getObjectOn() == ship):
                                continue
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Coral"):
                                print 'hit coral'
                                moveValid = False
                                VISIBLE = True
                                break
                            elif not board.getSquare(i,j).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = j
                            else:
                                colx = i
                                coly = j
                                moveValid = False
                                break
                else:
                    moveValid = False    

  

            if moveValid != False:
                color = pygame.Color(194, 242, 221) #green
        elif  turnType != "positionActive" and ((x - x1 ) <= 1 and ( x - x1 ) >= -ship.getSpeed() and (y - y1) == 0) or ((y - y1) >= -1 and (y - y1) <= 1 and (x - x1) == 0): 
            i = x
            # check for obsticals
            while i <= x1:
                if (board.getSquare(i,y).getObjectOn() != None ):
                    if (board.getSquare(i,y).getObjectOn() == ship):
                        i+=1
                        continue
                    if not board.getSquare(i,y).isVisible():
                        VISIBLE = False
                        colx = i
                        coly = y
                    else:
                        colx = i
                        coly = y
                        print colx,coly
                        moveValid = False
                    break
                i += 1
            # side ways movement
            if y != y1:
                i = 0
                while i< ship.getSize():
                    if (board.getSquare(x+i,y).getObjectOn() != None):
                        color = pygame.Color(250, 200, 200) #red
                        if not board.getSquare(x+i,y).isVisible():
                            VISIBLE = False
                        else:
                            
                            moveValid = False
                        break
                    i+=1 
            #check obstacles behind
            elif x+ship.getSize() >= x2+1 :
                if (board.getSquare(x+ship.getSize()-1,y).getObjectOn() != None):
                    if not board.getSquare(x+ship.getSize()-1,y).isVisible():
                        VISIBLE = False
                        colx = x+ship.getSize()-1
                        coly = y
                    else:
                        colx = x+ship.getSize()-1
                        coly = y
                        moveValid = False
            

        elif turnType == "positionActive" and Player1 and x <= 14 - ship.getSize() + 1 and x >= 0 and y >= 0 and y <= 29:      
            color = pygame.Color(194, 242, 221)
            
            moveValid = True
            i = x + ship.getSize() -1
            
            while i >= x:
                if (board.getSquare(i,y).getObjectOn()!= None):
                    if (board.getSquare(i,y).getObjectOn() == ship):
                        i-=1
                        continue
                    
                    moveValid = False
                    break
                i-=1
        elif turnType == "positionActive" and not Player1 and x > 14  and x <= 29 - ship.getSize() +1 and y >= 0 and y <= 29:      
            color = pygame.Color(194, 242, 221)
            
            moveValid = True
            i = x + ship.getSize() -1
            
            while i >= x:
                #print board.getSquare(i,y).getObjectOn()
                if (board.getSquare(i,y).getObjectOn()!= None):
                    if (board.getSquare(i,y).getObjectOn() == ship):
                        i-=1
                        continue
                    
                    moveValid = False
                    break
                i-=1
            #print moveValid
   

                        
        else:
            moveValid = False
        
        if moveValid == True:
            color = pygame.Color(194, 242, 221) #green
        else:
            color = pygame.Color(250, 200, 200) #red
        
        
        
        #print "Drawing w", (x,y)

        pygame.draw.polygon(surface, color, [(x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 29), (x*20 + x*1 + d, y*20 + y*1 + 20)], 0)      
        x = x + 1
        for i in range(ship.getSize() - 1):
            pygame.draw.rect(surface, color, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
            x = x + 1
            i = i + 1
        
    elif (newOrientation == "S"):
        if turning:
            if ship.getTurnRadius() == 1:
                if ship.getOrientation() == "W":
                    #print x 
                    x0 = x- ship.getSize() +1
                    y0 =y- ship.getSize() + 1
                else:
                    x0 = x + ship.getSize() -1
                    y0 = y- ship.getSize() + 1

                if (x0  == x1 and y0 == y1):
                    #print "r=",r
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if(board.getSquare(i,j).getObjectOn() == ship):
                                continue
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Coral"):
                                print 'hit coral'
                                VISIBLE = True

                                moveValid = False
                                break
                            elif not board.getSquare(i,j).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = j
                            else:
                                #print "found collision item"
                                colx = i
                                coly = j
                                moveValid = False
                                break
                else:
                    moveValid = False
            
            # ships that can move 180

            elif ship.getTurnRadius() == 2:
                if ship.getOrientation() == "N":
                    #print "NORTH"
                    x0 = x
                    y0 = y-2

                    #print 'x', x0,x1
                    #print 'y', y0,y1

                elif ship.getOrientation() == "W":
                    #print x 
                    x0 = x- ship.getSize() +2
                    y0 = y- ship.getSize() + 2
                else:
                    x0 = x + ship.getSize() -2
                    y0 = y- ship.getSize() + 2

                if (x0 == x1 and y0 == y1):
                    #print y,y2
                    i = y
                    while i >= y2-1:
                        if (board.getSquare(x,i).getObjectOn() != None ):
                            if(board.getSquare(x,i).getObjectOn() == ship):
                                i-=1
                                continue
                            if not board.getSquare(i,y).isVisible():
                                VISIBLE = False
                                colx = x
                                coly = i
                            else:
                                colx = x
                                coly = i
                                moveValid = False
                            break
                        i-=1
                else:
                    moveValid = False
                if (x0 == x1 and y0 == y1):
                    #print "r=",r
                    #print "AHHH: ", ship.getTurnZone(r)                    
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if(board.getSquare(i,j).getObjectOn() == ship):
                                continue
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Coral"):
                                print 'hit coral'
                                VISIBLE = True

                                moveValid = False
                                break
                            elif not board.getSquare(i,j).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = j
                            else:
                                #print "found collision item"
                                colx = i
                                coly = j
                                moveValid = False
                                break
                else:
                    moveValid = False 
            if moveValid != False:
                color = pygame.Color(194, 242, 221) #green

        elif turnType != "positionActive" and (( x - x1 ) == 0 and (y - y1) >= -1 and (y - y1) <= ship.getSpeed()) or (abs(( x - x1 )) == 1 and (y - y1) ==0) : 
            
            # check for obstacle
            i = y1
            while i <= y:
                if (board.getSquare(x,i).getObjectOn() != None ):
                    #print board.getSquare(x,i).getObjectOn() 
                    if (board.getSquare(x,i).getObjectOn() == ship):
                        i+=1
                        continue
                    elif not board.getSquare(x,i).isVisible():
                        VISIBLE = False
                        colx = x
                        coly = i
                    else:
                        colx = x
                        coly = i
                        moveValid = False
                    break
                i += 1
            if x != x1:
                i = 0
                while i< ship.getSize():
                    if (board.getSquare(x,y-i).getObjectOn() != None):
                        if not board.getSquare(x,y-i).isVisible():
                            VISIBLE = False
                        else:
                            moveValid = False
                        break
                    i+=1
            #check obstacle behind
            elif y-ship.getSize() <= y2-1 :
                if (board.getSquare(x,y-ship.getSize()+1).getObjectOn() != None):
                    if not board.getSquare(x,y-ship.getSize()+1).isVisible():
                        VISIBLE = False
                        colx = x
                        coly = y-ship.getSize()+1
                    else:
                        colx = x
                        coly = y-ship.getSize()+1
                        moveValid = False
    
        
        elif turnType == "positionActive" and Player1 and x >= 0 and x <= 14 and y >= ship.getSize()-1 and y <= 29:

            color = pygame.Color(194, 242, 221)
            global moveValid
            moveValid = True
            #print 'y ',y
            i = y - ship.getSize() +1
            
            while i <= y:
                #print board.getSquare(x,i).getObjectOn()
                
                if(board.getSquare(x,i).getObjectOn()!= None):
                    if (board.getSquare(x,i).getObjectOn()== ship):
                        i+=1
                        continue
                    color = pygame.Color(250, 200, 200) #red
                    moveValid = False
                    break
                i+=1
        elif turnType == "positionActive" and not Player1 and x > 14 and x <= 29 and y >= ship.getSize()-1 and y <= 29:

            color = pygame.Color(194, 242, 221)
            global moveValid
            moveValid = True
            #print 'y ',y
            i = y - ship.getSize() +1
            
            while i <= y:
                #print board.getSquare(x,i).getObjectOn()
                
                if(board.getSquare(x,i).getObjectOn()!= None):
                    if (board.getSquare(x,i).getObjectOn()== ship):
                        i+=1
                        continue
                    color = pygame.Color(250, 200, 200) #red
                    moveValid = False
                    break
                i+=1
        else:
            moveValid = False 
            
        if moveValid == True:
            color = pygame.Color(194, 242, 221) #green
        else:
            color = pygame.Color(250, 200, 200) #red

        #print "Drawing s", (x,y)

        pygame.draw.polygon(surface, color, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 10, y*20 + y*1 + 29)], 0)
        y = y - 1
        for i in range(ship.getSize() - 1):
            pygame.draw.rect(surface, color, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
            y = y - 1
            i = i + 1
            
    elif (newOrientation == "N"):
        if turning:
            #print "PASSED ", (x,y)
            moveValid = True
            color = pygame.Color(250, 200, 200) #red

            if ship.getTurnRadius() == 1:

                if ship.getOrientation() == "W":
                    #print x 
                    x0 = x- ship.getSize() +1
                    y0 = y+ ship.getSize() - 1
                else:
                    x0 = x + ship.getSize() -1
                    y0 = y+ ship.getSize() - 1

                if (x0 == x1 and y0 == y1):
                    #print "r=",r
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if(board.getSquare(i,j).getObjectOn() == ship):
                                continue
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Coral"):
                                print 'hit coral'
                                VISIBLE = True
                                moveValid = False
                                break
                            elif not board.getSquare(i,j).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = j
                            else:
                                #print "found collision item"
                                colx = i
                                coly = j
                                moveValid = False
                                break
                else:
                    moveValid = False
            
            # ships that can do 180
            elif ship.getTurnRadius() == 2:
                
                if ship.getOrientation() == "S":
                    #print "SOUTH"
                    x0 = x
                    y0 = y+2

                    #print 'x', x0,x1
                    #print 'y', y0,y1
                elif ship.getOrientation() == "W":
                    x0 = x- ship.getSize() +2
                    y0 = y+ ship.getSize() - 2
                else:
                    x0 = x + ship.getSize() -2
                    y0 = y+ ship.getSize() - 2

                #print 'x ',x0 , x1
                #print 'y ',y+ ship.getSize() - 2,y1
                if (x0 == x1 and y0 == y1):
                    #print y,y2
                    i = y2+1
                    while i >= y:
                        if (board.getSquare(x,i).getObjectOn() != None ):
                            if(board.getSquare(x,i).getObjectOn() == ship):
                                i-=1
                                continue
                            if not board.getSquare(i,y).isVisible():
                                VISIBLE = False
                                colx = x
                                coly = i
                            else:
                                colx = x
                                coly = i
                                moveValid = False
                            break
                        i-=1
                else:
                    moveValid = False

                if (x0 == x1 and y0 == y1):
                    #print "r=",r
                    #print "AHHH: ", ship.getTurnZone(r)                    
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if(board.getSquare(i,j).getObjectOn() == ship):
                                continue
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Coral"):
                                print 'hit coral'
                                VISIBLE = True
                                moveValid = False
                                break
                            elif not board.getSquare(i,j).isVisible():
                                VISIBLE = False
                                colx = i
                                coly = j
                            else:
                                #print "found collision item"
                                colx = i
                                coly = j
                                moveValid = False
                                break
                else:
                    moveValid = False  
           
        elif turnType != "positionActive" and (( x - x1 ) == 0 and (y1 - y) >= -1 and (y1 - y) <= ship.getSpeed()) or (abs(( x - x1 )) == 1 and (y - y1) ==0) : 
            # check for obsticals
            i = y
            while i <= y1:
                if (board.getSquare(x,i).getObjectOn() != None ):
                    if (board.getSquare(x,i).getObjectOn() == ship):
                        i+=1
                        continue
                    if not board.getSquare(i,y).isVisible():
                        VISIBLE = False
                        colx = x
                        coly = i
                    else:
                        colx = x
                        coly = i
                        moveValid = False
                    break
                i += 1
            if x != x1:
                i = 0
                while i< ship.getSize():
                    if (board.getSquare(x,y+i).getObjectOn() != None):
                        if not board.getSquare(i,y+i).isVisible():
                            VISIBLE = False
                        else:
                            moveValid = False
                        break
                    i+=1 
            
            #check obsticals behind
            elif y+ship.getSize() >= y2+1 :
                if (board.getSquare(x,y+ship.getSize()-1).getObjectOn() != None):
                    if not board.getSquare(i,y+ship.getSize()-1).isVisible():
                        VISIBLE = False
                    else:
                        colx = x
                        coly = ship.getSize()-1
                        moveValid = False
    
 
        elif turnType == "positionActive" and Player1 and x >= 0 and x <= 14 and y >= 0 and y <= 29 - ship.getSize() + 1:
            color = pygame.Color(194, 242, 221)
            global moveValid
            moveValid = True
            
            i = y + ship.getSize()-1
            #print 'i',i
            while i > y:
                if (board.getSquare(x,i).getObjectOn()!= None):
                    if (board.getSquare(x,i).getObjectOn() == ship):
                        i-=1
                        continue
                    
                    color = pygame.Color(250, 200, 200) #red
                    moveValid = False
                    break
                i-=1
        
        elif turnType == "positionActive" and not Player1 and x > 14 and x <= 29 and y >= 0 and y <= 29 - ship.getSize() + 1:
            color = pygame.Color(194, 242, 221)
            global moveValid
            moveValid = True
            
            i = y + ship.getSize()-1
            #print 'i',i
            while i > y:
                if (board.getSquare(x,i).getObjectOn()!= None):
                    if (board.getSquare(x,i).getObjectOn() == ship):
                        i-=1
                        continue
                    
                    color = pygame.Color(250, 200, 200) #red
                    moveValid = False
                    break
                i-=1

        else:
            moveValid = False
            
        if moveValid == True:
            color = pygame.Color(194, 242, 221) #green
        else:
            color = pygame.Color(250, 200, 200) #red

        #print "Drawing n", (x,y)

        pygame.draw.polygon(surface, color, [(x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d + 19, y*20 + y*1 + 29), (x*20 + x*1 + d + 9, y*20 + y*1 + 10)], 0)
        y = y + 1
        for i in range(ship.getSize() - 1):
            pygame.draw.rect(surface, color, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
            y = y + 1
            i = i + 1


    if not VISIBLE:
        print "COLLISION BUT NOT VISIBLE"
    #print "VALID MOVE: ", moveValid
    #print "VISIBLE", VISIBLE
    #print "turntype: ",turnType
    pygame.display.update()
    
def firingRange(surface, ship, x, y, weaponType):
    global moveValid
    pList = ship.getPositionList()
    size = ship.getSize()
    (x1, y1) = pList[0]
    (x2, y2) = pList[size - 1]
    weaponList = ship.getWeaponList()
    i = 0
    for weapon in weaponList:
        if weapon.getName() == weaponType:
            #print weapon.getName()
            break
        else:
            i = i + 1
    weapon = weaponList[i]
    xRange = weapon.getRangeX()
    yRange = weapon.getRangeY()
    tuple = (xRange, yRange)

    if (ship.getOrientation() == "N" or ship.getOrientation() == "S"):
        if (abs(x - x1) <= (yRange - 1)/2) and (abs(y - y1) <= (xRange - size)/2 or abs(y - y2) <= (xRange - size)/2):
            #global moveValid
            moveValid = True
        else:
            #global moveValid
            moveValid = False
    elif (ship.getOrientation() == "E" or ship.getOrientation() == "W"):
        if (abs(x - x1) <= (xRange - size)/2 or abs(x - x2) <= (xRange - size)/2) and (abs(y - y1) <= (yRange - 1)/2 or abs(y - y2) <= (yRange - size)/2):
            #global moveValid
            moveValid = True
        else:
            #global moveValid
            moveValid = False
    return tuple

def torpedoRange(surface, ship, x, y, weaponType):
    global moveValid
    pList = ship.getPositionList()
    (x1, y1) = pList[0]
    weaponList = ship.getWeaponList()
    i = 0
    for weapon in weaponList:
        if weapon.getName() == weaponType:
            break
        else:
            i = i + 1
    
    weapon = weaponList[i]
    xRange = weapon.getRangeX()
    yRange = weapon.getRangeY()    
    
    if (ship.getOrientation() == "N"):
        if ((y1-y) <= yRange and y < y1 and y >= 0 and y <= 29 and x == x1 and y):
            moveValid = True
        else:
            moveValid = False
    elif (ship.getOrientation() == "S"):
        if ((y-y1) <= yRange and y > y1 and y >= 0 and y <= 29 and x == x1 and y):
            moveValid = True
        else:
            moveValid = False        
    elif (ship.getOrientation() == "E"):
        if ((x-x1) <= xRange and x > x1 and x >= 0 and x <= 29 and y == y1):
            moveValid = True
        else:
            moveValid = False 
    elif (ship.getOrientation() == "W"):
        if ((x1-x) <= xRange and x < x1 and x >= 0 and x <= 29 and y == y1):
            moveValid = True
        else:
            moveValid = False            

if __name__ == '__main__':
    global offline
    offline = True
    # main('')
    main('offline',1,1,True)