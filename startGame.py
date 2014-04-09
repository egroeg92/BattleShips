import pygame, pygbutton, sys
from pygame.locals import *
from socket import *
import threading
import Matchup
import endGame
from Board import Board
from Weapon import Mine
from Ship import Ship
from Ship import MineLayer
from PlayerState import PlayerState
from Game import Game
from Coral import Coral
from Square import Square

from reefGeneration import reefGeneration

import textbox2
import pickle


FPS = 30
WINDOWWIDTH = 1250
WINDOWHEIGHT = 700

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0, 0.8)
DARKGRAY = (20,20,20)
GRAY = (70,70,70)

moveValid = False
positionValid = False
VISIBLE = True

FONT = pygame.font.SysFont("Arial", 14)
TITLEFONT = pygame.font.SysFont("Arial",20)
d = 15

global blank
blank = FONT.render("", 1, BLACK)
mineexplode = FONT.render("Mine exploded", 1, BLACK)
yourturn = FONT.render("Your turn", 1, BLACK)
oppturn = FONT.render("Opponent turn", 1, BLACK)


def drawMessagePanel(screen, turn):
    
    if turn:
        color = pygame.Color(194, 242, 221) #green
        screen.blit(yourturn, (200, WINDOWHEIGHT - 100))        

    else:
        color = pygame.Color(250, 200, 200) #red
        screen.blit(oppturn, (200, WINDOWHEIGHT - 100))

    pygame.draw.rect(screen, color, [670, 10,550, 100])
    if positioned:
        if turn:
            screen.blit(FONT.render("Your turn to make a move.",1,BLACK),(880,40))
        else:
            screen.blit(FONT.render("Your opponent is making their move...",1,BLACK),(820,40))

def drawStatPanel(screen, shiplist, op_shiplist):
    
    pygame.draw.rect(screen, WHITE, [670, 130, 550, 200])
    
    
    count = [0,0,0,0,0,0,0]
    for ship in shiplist:
        if sum(ship.getHealth()) != 0:
            if ship.getSubclass() == 'Cruiser':
                count[0] = count[0] + 1
            elif ship.getSubclass() == 'Destroyer':
                count[1] = count[1] + 1
            elif ship.getSubclass() == 'TorpedoBoat':
                count[2] = count[2] + 1
            elif ship.getSubclass() == 'RadarBoat':
                count[3] = count[3] + 1
            elif ship.getSubclass() == 'MineLayer':
                count[4] = count[4] + 1
            elif ship.getSubclass() == 'Kamikaze':
                count[5] = count[5] + 1
            
    pygame.draw.rect(screen, DARKGRAY, [670, 130, 550, 30])
    screen.blit(TITLEFONT.render("OVERVIEW", 1, WHITE),(900,135))

    screen.blit(TITLEFONT.render("YOUR SHIPS:", 1, BLACK),(750,170))

    screen.blit(FONT.render("Cruiser x"+str(count[0]), 1, BLACK),(750,200))
    screen.blit(FONT.render("Destroyer x"+str(count[1]), 1, BLACK),(750,220))
    screen.blit(FONT.render("TorpedoBoat x"+str(count[2]), 1, BLACK),(750,240))
    screen.blit(FONT.render("RadarBoat x"+str(count[3]), 1, BLACK),(750,260))
    screen.blit(FONT.render("MineLayer x"+str(count[4]), 1, BLACK),(750,280))
    screen.blit(FONT.render("Kamikaze x"+str(count[5]), 1, BLACK),(750,300))
    
    ocount = [0,0,0,0,0,0,0]
    for ship in op_shiplist:
        if sum(ship.getHealth()) != 0:
            if ship.getSubclass() == 'Cruiser':
                ocount[0] = ocount[0] + 1
            elif ship.getSubclass() == 'Destroyer':
                ocount[1] = ocount[1] + 1
            elif ship.getSubclass() == 'TorpedoBoat':
                ocount[2] = ocount[2] + 1
            elif ship.getSubclass() == 'RadarBoat':
                ocount[3] = ocount[3] + 1
            elif ship.getSubclass() == 'MineLayer':
                ocount[4] = ocount[4] + 1
            elif ship.getSubclass() == 'Kamikaze':
                ocount[5] = ocount[5] + 1
    screen.blit(TITLEFONT.render("ENEMY SHIPS:", 1, BLACK),(1000,170))

    screen.blit(FONT.render("Cruiser x"+str(ocount[0]), 1, BLACK),(1000,200))
    screen.blit(FONT.render("Destroyer x"+str(ocount[1]), 1, BLACK),(1000,220))
    screen.blit(FONT.render("TorpedoBoat x"+str(ocount[2]), 1, BLACK),(1000,240))
    screen.blit(FONT.render("RadarBoat x"+str(ocount[3]), 1, BLACK),(1000,260))
    screen.blit(FONT.render("MineLayer x"+str(ocount[4]), 1, BLACK),(1000,280))
    screen.blit(FONT.render("Kamikaze x"+str(ocount[5]), 1, BLACK),(1000,300))

def drawSelectedPanel(screen, shiplist):
    pygame.draw.rect(screen, WHITE, [670, 350, 550, 300])
    pygame.draw.rect(screen, DARKGRAY, [670, 350, 550, 30])
    screen.blit(TITLEFONT.render("OPTIONS", 1, WHITE),(900,355))
    
    for s in shiplist:
        if s.isSelected():
            screen.blit(TITLEFONT.render(s.getSubclass(), 1, BLACK),(700,400))

            screen.blit(FONT.render("Size: "+str(s.getSize()), 1, BLACK),(700,440))
            screen.blit(FONT.render("Orientation: "+s.getOrientation(), 1, BLACK),(700,460))
            screen.blit(FONT.render("Health: "+str(s.getHealth()), 1, BLACK),(700,480))
            screen.blit(FONT.render("Radar Range: "+str(s.getRadarX()), 1, BLACK),(700,500))
            screen.blit(FONT.render("Speed: "+str(s.getSpeed()), 1, BLACK),(700,520))
            screen.blit(FONT.render("Armour: "+str(s.getArmour()), 1, BLACK),(700,540))

            if (s.getTurnRadius() == 1) :
                screen.blit(FONT.render("Turn Radius: 90 deg", 1, BLACK),(700,560))
            else :
                screen.blit(FONT.render("Turn Radius: 180 deg", 1, BLACK),(700,560))
            
            screen.blit(FONT.render("Weapons: ", 1, BLACK),(860,440))
            y = 440
            for w in s.getWeaponList():
                screen.blit(FONT.render(w.getName(), 1, BLACK),(930,y))
                y = y + 20
                
            if s.getSubclass() == 'MineLayer':
                screen.blit(FONT.render("Remaining mines: " +str(s.getMineCount()), 1, BLACK),(860,y))
            return
        
    
    if turnType == "baseRepair":
        screen.blit(FONT.render("Select the ship you'd like to repair", 1, BLACK),(880,510))

    elif turnType != "reef" and turnType != "reefButton" and turnType != "waitForReefResponse":
        screen.blit(FONT.render("No ship selected", 1, BLACK),(900,510))
        
#             screen.blit(FONT.render("RadarBoat x"+str(ocount[3]), 1, BLACK),(1000,550))
#             screen.blit(FONT.render("MineLayer x"+str(ocount[4]), 1, BLACK),(1000,570))
#             screen.blit(FONT.render("Kamikaze x"+str(ocount[5]), 1, BLACK),(1000,590))


def listener(clientsocket,screen):
    global turn
    global op_positioned
    global op_positionedShips
    global gameOver
    global win
    global shiplist
    global op_shiplist
    global acceptreef
    global reefReq

    global turnType
    global message

    shiplist = game.getCurrentPlayer().getShipList()
    op_shiplist = game.getOpponent().getShipList()
    # global turnType
    while True:
        data = clientsocket.recv(1024)
        print 'Active Game data recv ' +str(data)
        # screen.fill(GRAY)  # Put this here temporarily to see the output
        drawMessagePanel(screen, turn)
        # updateBoard(game.getBoard(),screen, turn)

        if data == 'Win':
            print 'winner'
            clientsocket.send("WinGame")
            win = True
            gameOver = True
            break

        if data == 'Lose':
            print 'loser'
            win = False
            gameOver = True
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
            setKa = dataList[5]

            mine = dataList[6]
            if dataList[7] == 'True':
                backwards = True
            else:
                backwards = False

            ship.setSelected(True)
            
            string = ''
            if vis == 'True':
                if (setKa == 'True'):
                    game.detonateKamikaze()
                    string = 'Kamikaze attack at ' + (str(x)) + ' '+str(y)
                    game.getBoard().setNot(x,y,screen)

                game.moveShip(x,y,True)
                game.getBoard().setNot(-1,-1,screen)
                updateBoard(game.getBoard(),screen, turn)
                message = string
            else:
                game.moveShip(x,y,False)
                
                string =  'collision at '+ str(x)  +' ' +str(y)
                notifier = FONT.render(string, 1, (255,255,255))
                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                game.getBoard().setNot(x,y,screen)
                updateBoard(game.getBoard(),Screen, turn,string)
                message = string

            if mine == 'True':
                minhit = checkMineDamage(ship, x, y, 99, screen, backwards)
                x = minhit[0]
                y = minhit[1]
                string = 'Mine exploded at '+str(x)+ ' '+str(y)

                game.getBoard().setNot(x,y,screen)
                updateBoard(game.getBoard(),screen, turn)
                message = string


            ship.setSelected(False)
            # ship.move(int(dataList[2]))
            turn = True
            game.setTurn(True)

        elif dataList[0] == 'ReefRequest':
            reeflist = dataList[1]


            reeflist = reeflist.replace("[",'')
            reeflist = reeflist.replace("]",'')

            reeflist = reeflist.replace(" ",'')
            reeflist = reeflist.replace('),(',')||(')
            reeflist = reeflist.split('||')
                
            l = []
            for i in reeflist:
                z = i.replace('(','')
                z = z.replace(')','')
                x = int(z.split(',')[0])    
                    
                y = int(z.split(',')[1])
                l.append((x,y))

            print "RE ", l ,len(l)
            game.setCoral(l)

            screen.fill(GRAY);
            updateBoard(game.getBoard(),screen, turn)
            message = ''
            reefReq = True
            turnType = "reef"

        elif dataList[0] == 'ReefAccept':
            print "lol"
            turnType = "accept"
        elif dataList[0] == 'ReefReject':
            print 'yo'
            turnType = "reef"

        elif dataList[0] == 'Repair':
            ship = op_shiplist[int(dataList[1])]
            game.repairShip(ship)
            updateBoard(game.getBoard(),screen, turn)
            message = 'Repaired'
            turn = True
            game.setTurn(True)

        
        elif dataList[0] == 'Turn':
            #print'turning'
            ship = op_shiplist[int(dataList[1])]
            rot = int(dataList[2])
            degree = dataList[3]
            vis = dataList[4]
            mine = dataList[5]

            if mine == 'True':
                minehit = checkMineDamage(ship,1,1, rot, screen, False)
                string = "Hit mine at "+ str(minehit[0])+' '+str(minehit[1])
                game.getBoard().setNot(minehit[0],minehit[1],screen)
                updateBoard(game.getBoard(),Screen, turn)
                message = string



            else:
                if degree =='True':
                    if vis == 'True':
                        game.rotate(ship,rot,True,True)
                        game.getBoard().setNot(-1,-1,screen)
                        updateBoard(game.getBoard(),screen, turn)
                        message = ''
                    else:
                        game.rotate(ship,rot,True,False)
                        string =  'collision at '+ str(ship.getPositionList()[0][0]) +' ' +str(ship.getPositionList()[0][1])
                        notifier = FONT.render(string, 1, (255,255,255))
                        print string
                        # listbox.insert(END, string)
                        screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                        game.getBoard().setNot(ship.getPositionList()[0][0],ship.getPositionList()[0][1],screen)
                        updateBoard(game.getBoard(),Screen, turn)
                        message = string




                    
                else:
                    if vis == 'True':
                        game.getBoard().setNot(-1,-1,screen)                    
                        game.rotate(ship,rot,False,True)
                    else:
                        game.rotate(ship,rot,False,False)
                        string =  'collision at '+ str(ship.getPositionList()[0][0])  +' ' +str(ship.getPositionList()[0][1])
                        notifier = FONT.render(string, 1, (255,255,255))
                        print 's ' , string
                        # listbox.insert(END, string)
                        screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                        updateBoard(game.getBoard(),Screen, turn)
                        message = string
                        game.getBoard().setNot(ship.getPositionList()[0][0],ship.getPositionList()[0][1],screen)




            turn = True
            game.setTurn(True)
        
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
            # listbox.insert(END, resultString)
            ship.setSelected(False)
            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
            game.getBoard().setNot(x,y,screen)
            updateBoard(game.getBoard(),screen, turn)
            message = resultString

            turn = True
            game.setTurn(True)

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

            # listbox.insert(END, resultString)

            ship.setSelected(False)
            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
            game.getBoard().setNot(x,y,screen)
            updateBoard(game.getBoard(),screen, turn)
            message = resultString


            turn = True
            game.setTurn(True)
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
            # listbox.insert(END, resultString)

            ship.setSelected(False)
            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
            game.getBoard().setNot(x,y,screen)
            updateBoard(game.getBoard(),screen, turn)
            message = resultString


            turn = True
            game.setTurn(True)
        elif dataList[0] =='MineDrop':
            x = int(dataList[1])
            y = int(dataList[2])
            mine = Mine(1, 0, 0, (x,y)) 
            
            game.dropMineOnBoard(mine, (x,y))
            addMineList((x,y))
            turn = True
            game.setTurn(True)
        elif dataList[0] == 'MinePick':
            x = int(dataList[1])
            y = int(dataList[2])
            removeMineList(x,y)
            game.removeMine(x, y)
            turn =True
            game.setTurn(True)

        elif dataList[0] == 'Save':
            print 'opSaved ', dataList[1]
            savefile = dataList[1]
            pickle.dump(game,open('savedGames/'+savefile+".bsh","wb"))

            # if Player1:
            #     pickle.dump(game,open('savedGames/'+savefile+".bsh","wb"))
            # else:
            #     pickle.dump(game,open('savedGames2/'+savefile+".bsh","wb"))


            updateBoard(game.getBoard(),screen, turn)
            message = 'Game Saved as '+savefile+'.bsh'




        else:
            dataList = data[1:-1]
            dataList = dataList.replace(' ','')
            dataList = dataList.replace('\'','')
            dataList = dataList.split(',')
            #print dataList
            
            if dataList[0] == 'Position':
                dataList = dataList[:-2]
                dataList.reverse()

                op_positionedShips = dataList


                op_positioned = True


        # updateBoard(game.getBoard(),screen, turn)
#         if dataList[0] == 'Move'
   
def main(clientsocket, opp,user,player,corallist,loadGame):
    print 'user ',user
    print 'opp ', opp

    pygame.mixer.init()
    pygame.mixer.music.load('images/titanic.WAV')
    # explosion = pygame.mixer.Sound.load('images/Exploding.WAV')
    pygame.mixer.music.play()    
    # for offine play (for debugging)
    global positiontext
    global positiontext1
    positiontext = FONT.render("Click on your ships to position them.", 1, BLACK)
    positiontext1 = FONT.render("(You can only position ships on your side of the board.)", 1, BLACK)


    global message
    message = ''
    global win
    win = False
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
    global mineList 
    mineList = []
    global mine

    ## creating the screen

    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    
    pygame.display.set_caption('Battle Ships')
    
    ## Game object

    global turnType
    turnType = "reef"
    global game

    global turn
    turn = True
    
    global acceptreef
    acceptreef = False

    global reefReq
    reefReq = False
    
    global positioned
    positioned = False

    global buttonPositionShips
    buttonRotate = pygbutton.PygButton((1090, 400, 120, 30), 'Rotate Ship')
    buttonPositionShips = pygbutton.PygButton((1040, 610, 170, 30), 'Done Positioning Ships')
    buttonLongRadar = pygbutton.PygButton((1065, 520, 145, 30), 'Long Radar Toggle')

    buttonMove = pygbutton.PygButton((1090, 400, 120, 30), 'Move Ship')
    buttonMove2 = pygbutton.PygButton((1090,400,120,30), 'Move Ship')
    buttonTurn = pygbutton.PygButton((1090, 440, 120, 30), 'Turn Ship')
    buttonFire = pygbutton.PygButton((1090, 480, 120, 30), 'Fire Weapon')
    kbuttonFire = pygbutton.PygButton((1090, 520, 120, 30), 'Arm Explosives')
    buttonDropMine = pygbutton.PygButton((1090, 520, 120, 30), 'Drop Mine')
    buttonPickUpMine = pygbutton.PygButton((1090, 560, 120, 30), 'Pickup Mine')

    
    # shipOptions = [buttonMove, buttonTurn, buttonFire, buttonDropMine, buttonPickUpMine]
    # kshipOptions = [buttonMove, kbuttonFire]
    # positionOptions = [buttonRotate]
    global buttonCannon
    global buttonHeavyCannon
    global buttonTorpedo
    buttonCannon = pygbutton.PygButton((1090, 400, 120, 30), 'Cannon')
    buttonHeavyCannon = pygbutton.PygButton((1090, 440, 120, 30), 'HeavyCannon')
    buttonTorpedo = pygbutton.PygButton((1090, 480, 120, 30), 'Torpedo')
  
    buttonSave = pygbutton.PygButton((960, 660, 120, 30), 'Save Game')
    buttonExit = pygbutton.PygButton((1090, 660, 120, 30), 'Quit')

    global buttonRequestReef
    global buttonReef
    global buttonAcceptReef
    global buttonRejectReef

    buttonRequestReef = pygbutton.PygButton((880, 490, 120, 30), 'Request Reef')
    buttonReef = pygbutton.PygButton((880, 450, 120, 30), 'New Reef')

    buttonAcceptReef = pygbutton.PygButton((880, 450, 120, 30), 'Accept Reef')
    buttonRejectReef = pygbutton.PygButton((880, 490, 120, 30), 'Reject Reef')

    global shipOptions
    global mshipOptions
    global kshipOptions
    global shipOptions2
    global shipOptionsRadar
    global positionOptions
    global buttonRepair

    shipOptions = [buttonMove, buttonTurn, buttonFire]
    mshipOptions = [buttonMove, buttonTurn, buttonFire, buttonDropMine, buttonPickUpMine]
    kshipOptions = [buttonMove, kbuttonFire]

    shipOptions2 = [buttonTurn, buttonFire, buttonLongRadar]
    shipOptionsRadar = [buttonMove2, buttonTurn, buttonFire, buttonLongRadar]
    
    positionOptions = [buttonRotate]

    buttonRepair = pygbutton.PygButton((700, 580, 120, 30), 'Repair')    
    

    if not offline:
        if loadGame == '':
            game = Game(Player1,[],user,opp)
            reeflist = corallist
            reeflist = reeflist.replace("[",'')
            reeflist = reeflist.replace("]",'')

            reeflist = reeflist.replace(" ",'')
            reeflist = reeflist.replace('),(',')||(')
            reeflist = reeflist.split('||')
                
            
            l = []
            for i in reeflist:
                z = i.replace('(','')
                z = z.replace(')','')
                x = int(z.split(',')[0])    
                    
                y = int(z.split(',')[1])
                l.append((x,y))
            
            game.setCoral(l)
            screen.fill(GRAY);
            updateBoard(game.getBoard(),screen, turn)
            message = ''
        else:
            l = 'savedGames/'+loadGame 
            # if(Player1):
            #     l = 'savedGames/'+loadGame 
            # else:
            #     l = 'savedGames2/'+loadGame
            game = pickle.load(open(l,"rb"))
            shiplist = []
            op_shiplist = []
            turnType = game.getTurnType()

            shiplist = game.getCurrentPlayer().getShipList()
            op_shiplist = game.getOpponent().getShipList()
            
            if(game.getTurn() == True):
                turn = True
            else:
                turn = False
            
            print turn
            turnType = ''
            positioned = True
        print 'reef'


    else:
        print "reef"
        reeflist = []
        game = Game(Player1, reeflist,user,opp)
        game.setCoral(reeflist)
        for(x,y) in reeflist:
            c = Coral()
            sq = Square(c,(x,y))
            game.getBoard().setSquare(x,y,sq)

        screen.fill(GRAY);
        updateBoard(game.getBoard(),screen, True)
        message = ''
    #     if not offline:
    #         clientsocket.send("Reef:"+str(corallist))
    # else:
    #     game = Game(Player1, corallist)
    
    global colx
    global coly

    # colx = -1
    # coly = -1

    ## creating the button objects


    ## start the listener thread if playing not offline

    if not offline:
        l_thread = threading.Thread(target = listener, args = (clientsocket,screen))
        l_thread.start()


    ## turn is true if its your turn, false if its the opponents turn

    global shiplist
    global op_shiplist
    
    global baselist
    global op_baselist
    
    shiplist = []
    op_shiplist = []

    baselist = []
    op_baselist = [] 

    shiplist = game.getCurrentPlayer().getShipList()
    op_shiplist = game.getOpponent().getShipList()

    baselist = game.getCurrentPlayer().getBase().getPositionList()
    op_baselist = game.getOpponent().getBase().getPositionList()




    global armKamikaze
    armKamikaze = False

    
    global positionRotation
    positionRotation = 0

    global resultString
    resultString = ""


    global longRadar
    longRadar = False

    global radarboatselected
    radarboatselected = False    

    ## booleans for what kind of weapon options to display (initiated to none)
    cannon = False
    torpedo = False
    hcannon = False 

    screen.fill(GRAY)
    # drawStatPanel(screen, shiplist, op_shiplist)
    # drawSelectedPanel(screen, shiplist)
    # drawMessagePanel(screen, turn)



    global op_positionedShips
    op_positionedShips = []

    global gameOver
    gameOver = False
    global validDrop            
    validDrop = False
#####################################################
##                                                 ##
##              MAIN GAME LOOP                     ##
##                                                 ##
#####################################################
    while True:

        # print turnType

        if gameOver:
            endGame.start(clientsocket,user,opp,win)
            # Matchup.start(clientsocket,user)
            break
        # print user
        for s in shiplist:
            if(sum(s.getHealth()) == 0):
                shiplist.remove(s)



        for s in op_shiplist:
            if(sum(s.getHealth()) == 0):
                op_shiplist.remove(s)

        if len(shiplist)==0:
            # lose
            gameOver = True
            clientsocket.send("LoseGame")

        ## if offline its always your turn, (for debugging)
        if offline:
            turn = True
            game.setTurn(True)

        if positioned and op_positioned:
            while len(op_positionedShips) >0:
                op_positionedShips.pop()
                ship = op_shiplist[int(op_positionedShips.pop())]
                #print "SHIP NAME"+str(ship.getName())
                x1 = int(op_positionedShips.pop())
                y1 = int(op_positionedShips.pop())
                d1 = op_positionedShips.pop()
                ship.setSelected(True)
                if Player1: #then positioning player 2
                    if d1 == 'W':
                        p =0
                    elif d1 =='N':
                        p =1
                    elif d1 =='E':
                        p =2
                    elif d1 == 'S':
                        p = 3
                else:
                    if d1 == 'E':
                        p = 0
                    elif d1 =='S':
                        p =1
                    elif d1 =='W':
                        p =2
                    elif d1 =='N':
                        p = 3

                game.positionShip(x1, y1, p)
                ship.setSelected(False)


        ## Player 1 always has first turn 
        if Player1 and op_positioned == True and turnType == "" and positioned:
            print 'yay'
            turn = True
            game.setTurn(True)
            if positioned:
                op_positioned = False
       
        # drawMessagePanel(screen, turn)  
        # drawSelectedPanel(screen, shiplist)
        # drawStatPanel(screen, shiplist, op_shiplist)
      
        ## can only quit if its your turn

        game.getBoard().animate(screen,(pygame.time.get_ticks()/500)%2)
        if turnType == '':
            updateBoard(game.getBoard(),screen, turn)

        ## draw the ships
        

        if turn:
            buttonSave.draw(screen)
            buttonExit.draw(screen)
            


########################################################
##                                                    ##
##                    EVENT LOOP                      ##
##                                                    ##
########################################################  

        for event in pygame.event.get():
            # if event.type == pygame.KEYDOWN:
                    # if event.key == pygame.K_s:
                    #     print 'save'
                    #     game.getCurrentPlayer

                    #     pickle.dump(game,open("savedGames/savedGame.bsh","wb"))
                    #     if Player1:
                    #         pickle.dump(game,open("savedGames/savedGame.bsh","wb"))
                    #     else:
                    #         pickle.dump(game,open("savedGames2/savedGame.bsh","wb"))
                            
                    # if event.key == pygame.K_l:
                    #     if Player1:
                    #         game = pickle.load(open("savedGames/savedGame.bsh","rb"))
                    #     else:
                    #         game = pickle.load(open("savedGames2/savedGame.bsh","rb"))
                    #     print turn
                    #     print Player1
                    #     print shiplist
                    #     del shiplist
                    #     del op_shiplist
                        
                    #     shiplist = game.getCurrentPlayer().getShipList()
                    #     op_shiplist = game.getOpponent().getShipList()
                        
                    #     for s in shiplist:
                    #         print s.getPositionList()
                    #     for s in op_shiplist:
                    #         print s.getPositionList()

                    #     game.getCurrentPlayer().getUsername()
            ## set isSelected to True if a ship isSelected

            isKamikaze = False;
            for q in shiplist:
                isSelected = True
                if q.isSelected():
                    if q.getSubclass() == 'Kamikaze':
                        isKamikaze = True;
                    break
                isSelected = False

            # set radarboatselected True if RadarBoat is selected
            for w in shiplist:
                if w.isSelected() and w.getName() == "RadarBoat":
                    radarboatselected = True
                elif w.isSelected() and w.getName() != "RadarBoat":
                    radarboatselected = False                


            ## Events only matter if its the clients turn
            if turn:

                ##  QUITTING
                buttonExit.draw(screen)

                if 'click' in buttonExit.handleEvent(event) and (turnType == '' or turnType == 'position' or turnType == 'reef'):
                    print 'quit'
                    if offline:
                        sys.exit();
                    else:
                        gameOver = True
                        clientsocket.send("LoseGame")



                ## MOVING

                if turnType == "move":
                    if event.type == pygame.MOUSEMOTION:

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
                        print "in"
                        for ship in shiplist:
                            if ship.isSelected():
                                i, j = event.pos
                                i = (i - d) / 21
                                j = (j - 10) / 21
                                for x,y in ship.getPositionList():            
                                    if (i == (x-1) and ship.getOrientation() == "E"): # Ship is moving backwards            
                                        backwards = True            
                                        break           
                                    elif (i == (x+1) and ship.getOrientation() == "W"):         
                                        backwards = True            
                                        break           
                                    elif (j == (y+1) and ship.getOrientation() == "N"):         
                                        backwards = True            
                                        break           
                                    elif (j == (y-1) and ship.getOrientation() == "S"):         
                                        backwards = True            
                                        break           
                                    else:           
                                        backwards = False

                                if moveValid:
                                    x, y = event.pos
                                    x = (x - d) / 21
                                    y = (y - 10) / 21
                                    
                                    mine = False
                                    if ship.getOrientation() == "E":
                                        if x >= (ship.getSize()-1) and x <= 29 and y >= 0 and y <= 29:
                                            if VISIBLE:
                                                #print "move"
                                                p = x
                                                q = y

                                                MLIST = getMineDamagedCoordinates(ship, x, y, False, screen, backwards) 

                                                if(len(MLIST) != 0):                     
                                                    p = MLIST[0]            
                                                    q = MLIST[1]            
                                                    game.moveShip(p,q, True)            
                                                    MLIST = ()
                                                    mine = True
                                                else:           
                                                    game.moveShip(x, y, True)

                                                if (armKamikaze):
                                                    ship.setSelected(True)
                                                    game.detonateKamikaze()

                                                if not offline:
                                                    minehit = checkMineDamage(ship, x, y, 99, screen, backwards)

                                                    print mine
                                                    if(minehit != (-1,-1)):
                                                        mine = True

                                                    print "MINE ,",mine
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(p)+':'+str(q)+':True:'+str(armKamikaze)+':'+str(mine)+':'+str(backwards))
                                                    turn = False
                                                    game.setTurn(False)
                                            else:
                                                game.moveShip(x, y, False)
                                                print "COLLISION"


                                                string =  'collision at '+ str(x) +str(y)
                                                notifier = FONT.render(string, 1, (255,255,255))
                                                # screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                                
                                                updateBoard(game.getBoard(),screen, turn)
                                                message = string

                                                print "CO",colx,coly
                                                if not offline:
                                                    minehit = checkMineDamage(ship, x, y, 99, screen, backwards)

                                                    print mine
                                                    if(minehit != (-1,-1)):
                                                        mine = True
                                                    
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(colx)+':'+str(coly)+':False:False'+':'+str(mine)+':'+str(backwards))
                                                    turn = False
                                                    game.setTurn(False)
                                    
                                    elif ship.getOrientation() == "W":
                                        if x <= 29 - ship.getSize() and x >= 0 and y >= 0 and y <= 29:
                                            if VISIBLE:
                                                #print "move"
                                                p = x
                                                q = y

                                                MLIST = getMineDamagedCoordinates(ship, x, y, False, screen, backwards)
                                                minehit = checkMineDamage(ship, x, y, 99, screen, backwards)
                                                if(minehit != (-1,-1)):
                                                    mine = True
 
                                                if(len(MLIST) != 0):                     
                                                    
                                                    p = MLIST[0]            
                                                    q = MLIST[1]
                                                    print p,q            
                                                    game.moveShip(p,q, True)            
                                                    MLIST = ()
                                                    mine = True          
                                                else:           
                                                    game.moveShip(x, y, True)
                                                
                                                if not offline:
                                                    minehit = checkMineDamage(ship, x, y, 99, screen, backwards)

                                                    print mine
                                                    if(minehit != (-1,-1)):
                                                        mine = True
                                                    
                                                    print 'sent p,q',p,q
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(p)+':'+str(q)+':True:False'+':'+str(mine)+':'+str(backwards))
                                                    turn = False
                                                    game.setTurn(False)
                                            else:
                                                print "COLLISION"

                                                game.moveShip(x, y, False)
                                                string =  'collision at '+ str(x) +str(y)
                                                notifier = FONT.render(string, 1, (255,255,255))
                                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                                

                                                updateBoard(game.getBoard(),screen, turn)
                                                message = string

                                                print "CO",colx,coly
                                                if not offline:
                                                    minehit = checkMineDamage(ship, x, y, 99, screen, backwards)

                                                    print mine
                                                    if(minehit != (-1,-1)):
                                                        mine = True
                                                    
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(colx)+':'+str(coly)+':False:False'+':'+str(mine)+':'+str(backwards))
                                                    turn = False
                                                    game.setTurn(False)
                                    elif ship.getOrientation() == "S":
                                        back_postion = ship.getPositionList()[-1]
            
                                        if x >= 0 and x <= 29 and y >= back_postion[1] and y <= 29:
                                            if VISIBLE:
                                                #print "move"
                                                p = x
                                                q = y
                                                MLIST = getMineDamagedCoordinates(ship, x, y, False, screen, backwards) 
                                                if(len(MLIST) != 0):                     
                                                    p = MLIST[0]            
                                                    q = MLIST[1]            
                                                    game.moveShip(p,q, True)            
                                                    MLIST = ()
                                                    mine = True          
                                                else:           
                                                    game.moveShip(x, y, True)

                                                if not offline:
                                                    minehit = checkMineDamage(ship, x, y, 99, screen, backwards)

                                                    print mine
                                                    if(minehit != (-1,-1)):
                                                        mine = True
                                                    
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(p)+':'+str(q)+':True:False'+':'+str(mine)+':'+str(backwards))
                                                    turn = False
                                                    game.setTurn(False)
                                            else:
                                                print "COLLISION"

                                                game.moveShip(x, y, False)
                                                string =  'collision at '+ str(x) +str(y)
                                                notifier = FONT.render(string, 1, (255,255,255))
                                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                                
                                                updateBoard(game.getBoard(),screen, turn)
                                                message = string

                                                if not offline:
                                                    minehit = checkMineDamage(ship, x, y, 99, screen, backwards)

                                                    print mine
                                                    if(minehit != (-1,-1)):
                                                        mine = True
                                                    
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(colx)+':'+str(coly)+':False:False'+':'+str(mine)+':'+str(backwards))
                                                    turn = False
                                                    game.setTurn(False)

                                    elif ship.getOrientation() == "N":
                                        if x >= 0 and x <= 29 and y >= 0 and y <= 29-ship.getSize():
                                            if VISIBLE:
                                                #print "move"
                                                p = x
                                                q = y
                                                MLIST = getMineDamagedCoordinates(ship, x, y, False, screen, backwards)
                                                minehit = checkMineDamage(ship, x, y, 99, screen, backwards)
                                                if(minehit != (-1,-1)):
                                                    mine = True 
                                                if(len(MLIST) != 0):                     
                                                    p = MLIST[0]            
                                                    q = MLIST[1]            
                                                    game.moveShip(p,q, True)            
                                                    MLIST = ()          
                                                else:           
                                                    game.moveShip(x, y, True)
                                                if not offline:
                                                    minehit = checkMineDamage(ship, x, y, 99, screen, backwards)

                                                    print mine
                                                    if(minehit != (-1,-1)):
                                                        mine = True
                                                    
                                                    clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(p)+':'+str(q)+':True:False'+':'+str(mine)+':'+str(backwards))
                                                    turn = False
                                                    game.setTurn(False)

                                            else:
                                                game.moveShip(x, y, False)
                                                print "COLLISION"

                                                string =  'collision at '+ str(x) +str(y)
                                                notifier = FONT.render(string, 1, (255,255,255))
                                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                                
                                                updateBoard(game.getBoard(),screen, turn)
                                                message = string

                                            if not offline:
                                                minehit = checkMineDamage(ship, x, y, 99, screen, backwards)

                                                print mine
                                                if(minehit != (-1,-1)):
                                                    mine = True
                                                
                                                clientsocket.send('Move:'+str(shiplist.index(ship))+':'+str(colx)+':'+str(coly)+':False:False'+':'+str(mine)+':'+str(backwards))
                                                turn = False
                                                game.setTurn(False)
                                
                                #CHECK MINE MOVING
                                minehit = checkMineDamage(ship, x, y, 99, screen, backwards)
                                backwards == False
                                ship.setSelected(False)
                                global turnType
                                turnType = ""
                                screen.fill(GRAY);
                                

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

                                screen.fill(GRAY);
                                
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
                                    screen.fill(GRAY);


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
                                i, j = event.pos
                                i = (i - d) / 21
                                j = (j - 10) / 21
                                #hit

                                minehit = checkMineDamage(ship,i,j, rot, screen, False)
                                if minehit != (-1,-1):            
                                    moveValid = False
                                    if not offline:
                                        clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:True:True')
                                        game.setTurn(False)
                                        turn = False
                                if moveValid:
                                    x, y = event.pos
                                    x = (x - d) / 21
                                    y = (y - 10) / 21
                                    if ship.getTurnRadius() == 1:
                                        #TODO, Client socket takes in  more arguments

                                        if VISIBLE:
                                            game.rotate(ship,rot,True, True)
                                            if not offline:
                                                clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:True:False')
                                                turn = False
                                                game.setTurn(False)
                                        else:
                                            game.rotate(ship, rot, True, False)

                                            print "COLLISION"

                                            string =  'turn collision at '+ str(x) +str(y)
                                            notifier = FONT.render(string, 1, (255,255,255))
                                            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                            
                                            updateBoard(game.getBoard(),screen, turn)
                                            message = string

                                            if not offline:
                                                clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:False:False')
                                                turn = False
                                                game.setTurn(False)
                                    
                                    elif ship.getTurnRadius() == 2:

                                        if VISIBLE:
                                            game.rotate(ship,rot,False, True)
                                            if not offline:
                                                clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:True:False')
                                                turn = False
                                                game.setTurn(False)

                                        else:
                                            game.rotate(ship, rot, False, False)
                                            
                                            print "COLLISION"
                                            string =  'turn collision at '+ str(x) +str(y)
                                            notifier = FONT.render(string, 1, (255,255,255))
                                            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                            

                                            updateBoard(game.getBoard(),screen, turn)
                                            message = string

                                            if not offline:
                                                clientsocket.send('Turn:'+str(shiplist.index(ship))+':'+str(rot)+':True:False:False')
                                                turn = False
                                                game.setTurn(False)


                                ship.setSelected(False)
                                global turnType
                                turnType = ""
                                screen.fill(GRAY);

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
                                    screen.fill(GRAY);
                                    game.updateRange("cannon", False)
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    
                                    updateBoard(game.getBoard(),screen, turn)
                                    message = resultString
                                    if not offline:
                                        clientsocket.send("Cannon:"+str(shiplist.index(ship))+':'+str(x)+":"+str(y))
                                        turn = False
                                        game.setTurn(False)
                                else:
                                    moveValid = False
                                    turnType = ""
                                    game.updateRange("",False)
                                    screen.fill(GRAY);
                
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
                                    screen.fill(GRAY);
                                    game.updateRange("heavycannon", False)
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    
                                    #print resultString
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    updateBoard(game.getBoard(),screen, turn)
                                    message = resultString
                                    if not offline:
                                        clientsocket.send("HCannon:"+str(shiplist.index(ship))+':'+str(x)+":"+str(y))
                                        turn = False
                                        game.setTurn(False)
                                else:
                                    moveValid = False
                                    turnType = ""
                                    game.updateRange("",False)
                                    screen.fill(GRAY)

                   # Dropping Mine
                elif turnType == "mine":

                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        x = (x - d) / 21
                        y = (y - 10) / 21
                        
                        for ship in shiplist:
                            # print ship
                            if ship.isSelected():
                                print "ship has been selected"
                                print ship.getName()
                                if ship.getSubclass() != "MineLayer":
                                    resultString = "Ship selected cant drop mines..."
                                    screen.fill(GRAY);
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    global turnType
                                    turnType = ""

                                else:
                                    position = ship.position
                                    game.getBoard().paint(screen)
                                    tuple = (x,y)
                                    if (x,y) in ship.getdroppingRange(position):
                                        if game.dropMine(x,y) == "Cant drop mine at selected location":
                                            print "Invalid droppping"
                                            drawRedWeapon(screen, x, y)
                                        else:
                                            drawWeapon(screen, x, y)
                                            minedDroppingShip = ship
                                            print "Valid dropping area"
                                            validDrop = True
                                            break
                                    else:
                                        drawRedWeapon(screen, x, y)
                                        print "Invalid coordinates"
                                print ship

                    elif event.type == pygame.MOUSEBUTTONUP:   
                        #print mineShip.getName()
                        #objectOnN = game.getBoard().getSquare(x,y).getObjectOn()
                        #if objectOnN != None:
                        if(validDrop):
                            validDrop = False
                            print minedDroppingShip.getdroppingRange(minedDroppingShip.getPositionList())
                            print minedDroppingShip.getSubclass()

                            if (x,y) in minedDroppingShip.getdroppingRange(minedDroppingShip.getPositionList()) and minedDroppingShip.getSubclass() == "MineLayer":
                                tuple = (x,y)
                                global turnType
                                turnType = ""
                                resultString = game.dropMine(x,y)  
                                screen.fill(GRAY);
                                notifier = FONT.render(resultString, 1, (255,255,255))
                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                mine = Mine(1, 0, 0, tuple)    # Create mine object
                                result = ship.mineDropped(minedDroppingShip)
                                print result
                                if(result == 0):
                                    game.dropMineOnBoard(mine, tuple)
                                    addMineList(tuple)
                                    ship.setSelected(False)
                                    if not offline:
                                        clientsocket.send("MineDrop:"+str(x)+':'+str(y))
                                        turn = False
                                        game.setTurn(False)

                                else:
                                    resultString = "Can't drop Mine.  The boat is out of Mines!" 
                                    screen.fill(GRAY);
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    global turnType
                                    turnType = ""

                            else:
                                resultString = "Can't drop mine in selected location" 
                                screen.fill(GRAY);
                                notifier = FONT.render(resultString, 1, (255,255,255))
                                screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                global turnType
                                turnType = ""
                        else:
                            resultString = "Can't drop mine in selected location" 
                            screen.fill(GRAY);
                            notifier = FONT.render(resultString, 1, (255,255,255))
                            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                            global turnType
                            turnType = ""

                

                # Picking up Mine
                elif turnType == "minePickUp":                 
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        x = (x - d) / 21
                        y = (y - 10) / 21
                        
                        for ship in shiplist:
                            if ship.isSelected():
                                if ship.getSubclass() != "MineLayer":
                                    resultString = "Selected boat can't pick up mines" 
                                    screen.fill(GRAY);
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    global turnType
                                    turnType = ""
                                else:
                                    newBoatForPickUp = ship
                                    position = newBoatForPickUp.position
                                    game.getBoard().paint(screen)
                                    tuple = (x,y)
                                    if (x,y) in newBoatForPickUp.getdroppingRange(position):
                                        if game.PickUpMine(x,y) == 1:        
                                            drawRedWeapon(screen, x, y)
                                            print "Invalid pick up area.."
                                        else:
                                            drawYellowWeapon(screen, x, y)
                                            print "Valid pick up area"

                                    else:
                                        drawRedWeapon(screen, x, y)
                                        print "Invalid coordinates"
                    
                    elif event.type == pygame.MOUSEBUTTONUP: 
                        if (x,y) in newBoatForPickUp.getdroppingRange(position):
                            result = game.PickUpMine(x,y)
                            print "HERE IS RESULT"
                            print x,y
                            if(result == 0):
                                if newBoatForPickUp.getSubclass() == "MineLayer":
                                    print "Mine Count update:="
                                    removeMineList(x,y)
                                    game.removeMine(x, y)
                                    ship.minePickedUp(newBoatForPickUp)
                                    print newBoatForPickUp.getMineCount()
                                    resultString = "Mine has been successfully picked up!" 
                                    screen.fill(GRAY);
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    global turnType
                                    turnType = ""
                                    ship.setSelected(False)
                                    if not offline:
                                        clientsocket.send("MinePick:"+str(x)+':'+str(y))
                                        turn = False
                                        game.setTurn(False)
                        else:
                            resultString = "Mine pick up unseuccessful" 
                            screen.fill(GRAY);
                            notifier = FONT.render(resultString, 1, (255,255,255))
                            screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                            global turnType
                            turnType = "" 

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
                                    print "RESULT STRING ",resultString

                                    resultString = resultString.split(':')

                                    if resultString[0] == 'ship sunk ':
                                        resultString = resultString[0]+':'+resultString[1]+'at '+str(x)+' '+str(y)
                                    else:
                                        print resultString
                                        resultString = resultString[0]+'at '+str(x)+' '+str(y)

                                    ship.setSelected(False)
                                    turnType = ""
                                    screen.fill(GRAY);
                                    game.updateRange("torpedo", False)
                                    notifier = FONT.render(resultString, 1, (255,255,255))
                                    
                                    screen.blit(notifier, (200, WINDOWHEIGHT - 100))
                                    
                                    if not offline:
                                        clientsocket.send("Torpedo:"+str(shiplist.index(ship))+':'+str(x)+':'+str(y))                                   
                                        turn = False
                                        game.setTurn(False)
                                else:
                                    moveValid = False
                                    turnType = ""
                                    game.updateRange("",False)
                                    screen.fill(GRAY)
                elif turnType == "reefButton":
                    corallist = []
                    game.randomizeReef(corallist)
                    game.setCoral(corallist)
                    print corallist                    
                    print(len(corallist))
                    turnType = "reef"

                    screen.fill(GRAY);
                    updateBoard(game.getBoard(),screen,turn)
                    message = ''

                elif turnType == "request":
                    screen.fill(GRAY)
                    screen.blit(positiontext, (200, WINDOWHEIGHT - 100))
                    buttonExit.draw(screen)
                    buttonPositionShips.draw(screen)
                    # turnType = "position"
                    updateBoard(game.getBoard(),screen,turn)
                    message = ''

                    print ("SENT CORAL "+ str(game.getCoral())) + str(len(game.getCoral()))

                    if not offline:
                        clientsocket.send('ReefRequest:'+str(game.getCoral()))
                        turnType = "waitForReefResponse"
                    else:
                        turnType = "position"
                        acceptreef = True

                elif turnType == "repairBoat":                  
                    
                    if game.getCurrentPlayer().getBase().isSelected() == True:
                        for ship in shiplist:
                            if ship.isSelected():
                                game.repairShip(ship)
                                print ship.getHealth()
                                
                                turnType = ""
                                game.getCurrentPlayer().getBase().setSelected(False)
                                ship.setSelected(False)
                                screen.fill(GRAY);
                                turn = False
                                game.setTurn(False)
                                if not offline:
                                    clientsocket.send("Repair:"+str(shiplist.index(ship)))
                                 
                
                # clicked to turn radar on
                elif turnType == "radaron":
                    global longRadar
                    longRadar = True
                    for s in shiplist:
                        if (s.isSelected() and positioned and s.getSubclass() == "RadarBoat"):
                            screen.fill(GRAY)  # Put this here temporarily to see the output
                            if longRadar == True: 
                                for o in shipOptions2:
                                    o.draw(screen)                     
                    game.updateVisibilityRadar() 
                    global turnType
                    turnType = ""
                    screen.fill(GRAY);

                #?
                # clicked to turn radar off
                elif turnType == "radaroff":
                    global longRadar
                    longRadar = False
                    for s in shiplist:
                        if (s.isSelected() and positioned and s.getSubclass() == "RadarBoat"):
                            screen.fill(GRAY)  # Put this here temporarily to see the output
                            if longRadar == False:
                                for o in shipOptionsRadar:
                                    o.draw(screen)                                                        
                    game.updateVisibility() 
                    global turnType
                    turnType = ""
                    screen.fill(GRAY);       

               
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
                        game.setTurn(True)
                    
                    else:
                        turn = False
                        game.setTurn(False)

                    turnType = ""


                    screen.fill(GRAY);                                

                elif 'click' in buttonSave.handleEvent(event):
                    print 'save'
                    pygame.draw.rect(screen, GRAY, [670, 350, 550, 300])
                    screen.blit(FONT.render("Enter a file name (don't include extension):",1,WHITE),(750,420))
                    savefile = textbox2.start(screen," ")
                    
                    pickle.dump(game,open('savedGames/'+savefile+".bsh","wb"))
                    
                    # if Player1:
                    #     pickle.dump(game,open('savedGames/'+savefile+".bsh","wb"))
                    
                    # else:
                    #     pickle.dump(game,open('savedGames2/'+savefile+".bsh","wb"))

                    screen.fill(GRAY)
                    updateBoard(game.getBoard(),screen,turn)
                    message = 'Saving'

                    if not offline:
                        clientsocket.send("Save:"+savefile)


                elif 'click' in buttonDropMine.handleEvent(event) and turnType == '' and isSelected and not radarboatselected and not isKamikaze:
                    turnType = "mine" 

                elif 'click' in buttonPickUpMine.handleEvent(event) and turnType == '' and isSelected:
                    turnType = 'minePickUp'

        
             
                elif 'click' in buttonMove.handleEvent(event) and turnType == '' and isSelected and not radarboatselected:
                    turnType = "move"
                elif 'click' in buttonMove2.handleEvent(event) and turnType == '' and isSelected and not longRadar:
                    turnType = "move"

                elif 'click' in kbuttonFire.handleEvent(event) and turnType == '' and isSelected and isKamikaze:
                    print "KAMIKAZE ARMED"
                    armKamikaze = True
                    turnType = "move"

                elif 'click' in buttonFire.handleEvent(event) and turnType == '' and isSelected:
                    turnType = "fire"

                elif 'click' in buttonCannon.handleEvent(event) and turnType == 'fire' and isSelected:
                    turnType = "cannon"

                    game.updateRange("cannon", True)
                    updateBoard(game.getBoard(),screen, turn)



                elif 'click' in buttonHeavyCannon.handleEvent(event) and turnType == 'fire' and isSelected:
                    print 'click in heavy'
                    turnType = "heavycannon"
                    game.updateRange("heavycannon", True)
                    updateBoard(game.getBoard(),screen, turn)
                    #print turnType

                elif 'click' in buttonTorpedo.handleEvent(event) and turnType == 'fire' and isSelected:
                    turnType = "torpedo"
                    game.updateRange("torpedo", True)
                    updateBoard(game.getBoard(),screen, turn)                    
                        
                elif 'click' in buttonTurn.handleEvent(event) and turnType == '' and isSelected:
                    turnType = "turn"
                    x,y = event.pos
                    x = (x - d) / 21
                    y = (y - 10) / 21
               
                elif 'click' in buttonRepair.handleEvent(event) and turnType == 'baseRepair':
                    turnType = "repairBoat"



                elif 'click' in buttonRequestReef.handleEvent(event) and acceptreef == False and turnType == "reef" and Player1:
                    turnType = "request"
                    updateBoard(game.getBoard(),screen,turn) 

                elif 'click' in buttonReef.handleEvent(event) and acceptreef == False and turnType == "reef" and Player1:
                    turnType = "reefButton"
                    updateBoard(game.getBoard(),screen,turn)

                elif 'click' in buttonAcceptReef.handleEvent(event) and acceptreef == False and not Player1 and reefReq:
                    clientsocket.send('ReefAccept')
                    turnType = "position"
                    reefReq = False
                    acceptreef = True
                    updateBoard(game.getBoard(),screen,turn)

                elif 'click' in buttonRejectReef.handleEvent(event) and acceptreef == False and turnType == "reef" and not Player1 and reefReq:
                    clientsocket.send('ReefReject')
                    reefReq = False
                    updateBoard(game.getBoard(),screen,turn)

                elif 'click' in buttonLongRadar.handleEvent(event) and radarboatselected and turnType == "" and isSelected:
                    for ship in shiplist:
                        if ship.getSubclass() == "RadarBoat" and ship.getLongRadar() == True:
                            turnType = "radaroff"
                            ship.setLongRadar(False)
                            global longRadar
                            longRadar = False
                            
                        elif ship.getSubclass() == "RadarBoat" and ship.getLongRadar() == False:
                            turnType = "radaron"
                            ship.setLongRadar(True)
                            global longRadar
                            longRadar = True 


                elif event.type == pygame.MOUSEBUTTONUP and turnType != "reef" and turnType != "reefButton" and turnType != "waitForReefResponse":
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
                                turnType = "positionActive"
                            
                            break;                            
                            total = total - 1
                            
                            
                        #ship was not clicked, take off ship options
                    
                    if total == 0:
                        print "ship not detected"
                    if total == 0 and positioned:

                        ## MAYBE DELETE
                        screen.fill(GRAY);
                        for sh in shiplist:
                            sh.setSelected(False)

                    if (x >= 0 and x <= 29 and y >= 0 and y <= 29):
                        obj = game.getBoard().getSquare(x,y).getObjectOn()
                        if obj == None:
                            turnType = ''
                            for z in shiplist:
                                z.setSelected(False)
                            for b in baselist:
                                x1 = b[0]
                                x2 = b[1]
                                game.getBoard().getSquare(x1,x2).getObjectOn().setSelected(False)
                        
                        elif obj.getClassName() == "Base" and turnType != "position" and (x,y) not in op_baselist:
                            obj.setSelected(True)
                            turnType = "baseRepair"
                            
                    print turnType
                if turnType != "move" and turnType != "positionActive" and turnType != "turn" and turnType != "cannon" and turnType != "mine" and turnType !="minePickUp" and turnType != "heavycannon" and turnType != "torpedo" and turnType != "radaron" and turnType != "radaroff":

                    updateBoard(game.getBoard(),screen, turn)
                  
def updateBoard(gameBoard,screen, turn):
    shiplist = game.getCurrentPlayer().getShipList()
    op_shiplist = game.getOpponent().getShipList()
    drawStatPanel(screen, shiplist, op_shiplist)
    drawSelectedPanel(screen, shiplist)
    drawMessagePanel(screen, turn)

    global message

    if (turnType == "fire"):
        # screen.fill(GRAY);
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
    else:

        for s in shiplist:
            if (s.isSelected() and positioned and s.getSubclass() == 'Kamikaze'):
                # drawSelectedPanel(screen,shiplist)
                for o in kshipOptions:
                    o.draw(screen)
            elif (s.isSelected() and positioned and s.getSubclass() == 'MineLayer'):
                # drawSelectedPanel(screen,shiplist)
                for o in mshipOptions:
                    o.draw(screen)
            elif (s.isSelected() and positioned and s.getSubclass() == "RadarBoat"):
                # drawSelectedPanel(screen,shiplist)
                if longRadar == True:
                    for o in shipOptions2:
                        o.draw(screen)
                else:                
                    for o in shipOptionsRadar:
                        o.draw(screen)   

            elif (s.isSelected()):
                drawSelectedPanel(screen,shiplist)
                for o in shipOptions:
                    o.draw(screen)

    if turnType == "reef" and not Player1 and not acceptreef and not reefReq:
        screen.blit(FONT.render("Opponent is selecting a reef configuration...",1,BLACK),(830, 430))
    
    if turnType != "position" and Player1 and turnType == "waitForReefResponse":
        screen.blit(FONT.render("Opponent is deliberating...",1,BLACK),(830, 430))

    if turn:
        if turnType == "reef":
            if Player1 and not reefReq:
                screen.blit(FONT.render("Please select a reef configuration:",1,BLACK),(830, 410))
                buttonRequestReef.draw(screen)
                buttonReef.draw(screen)
            
            
            
        if not Player1 and reefReq :
            screen.blit(FONT.render("Do you accept this reef configuration?",1,BLACK),(830, 410))
            buttonAcceptReef.draw(screen)
            buttonRejectReef.draw(screen)

    if turnType == "position":
        print "POSITION TURNTYPE"
        screen.blit(positiontext, (850, 40))
        screen.blit(positiontext1, (780, 60))
        buttonPositionShips.draw(screen)

    if (turnType == "positionActive"):
        for s in shiplist:
            if (s.isSelected() and s.getSubclass() != "Kamikaze"):
                for o in positionOptions:
                    o.draw(screen)
    if (turnType == "baseRepair"):
        buttons = []
        dockedships = []
        p1 = ()
        p2 = ()
        p3 = ()

        # print "Current Player is selected: ", game.getCurrentPlayer().getBase().isSelected()
        # print "Opponent Player is selected: ", game.getOpponent().getBase().isSelected()                                
        
        if game.getCurrentPlayer().getBase().isSelected() == True:
            for (x,y) in baselist:
                obj = game.getBoard().getSquare(x,y).getObjectOn()
                if obj != None and obj.getClassName() == "Base":
                    p1 = (x, y-1) 
                    p2 = (x, y+1)
                    
                    if Player1:
                        p3 = (x+1, y)
                    else:
                        p3 = (x-1, y)

                    
                    for ship in shiplist:
                        ship.setDocked(False)
                        
                    for ship in shiplist:
                        poslist = ship.getPositionList()
                        # print poslist
                        if (p1 in poslist) or (p2 in poslist) or (p3 in poslist) and ship not in dockedships:
                            #print ship.getNaming()
                            dockedships.append(ship)
                            ship.setDocked(True)
                            # print 'repairable ' ,ship.getName()
        for ship in shiplist:
            if ship in dockedships and ship.isSelected() and sum(ship.getHealth()) < ship.getHealthSum():
                buttonRepair.draw(screen) 
            elif ship in dockedships and ship.isSelected() :
                screen.blit(FONT.render("Nothing to repair!",1,GREEN),(700,580))             
                


    mess = FONT.render(message,1,BLACK)

    if turn:
        screen.blit(mess,(800,60))
    else:
        screen.blit(mess,(800,60))



    pygame.draw.rect(screen, WHITE, [9,5,641,640])
    pygame.draw.rect(screen, BLACK, [14,9,631,631])
    gameBoard.paint(screen)
    pygame.display.update()

def drawWeapon(surface, x, y):
    c = (27, 201, 18) #green
    pygame.draw.ellipse(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20], 0)
    pygame.display.update()
def drawRedWeapon(surface, x, y):
    c = (250, 0, 0) # Red
    pygame.draw.ellipse(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20], 0)
    pygame.display.update()

def drawYellowWeapon(surface, x, y):
    c = (255, 255, 0) # Yellow
    pygame.draw.ellipse(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20], 0)
    pygame.display.update()    

def addMineList(position):
    print "ADDING"
    x = position[0]
    y = position[1]
    tuple = (x,y)
    mineList.append(tuple)

def removeMineList(x,y):
    tuple = (x,y)
    mineList.remove(tuple)

def checkMineDamage(ship,x,y, isTurning, screen, backwards):
    indigo = False
    orientation = ship.getOrientation()
    shipList = ship.getPositionList()
    x = -1
    y = -1
    #print ship.getOrientation()
    #print ship.getPositionList()
    #print isTurning
    if isTurning != 99:
        #print x, y
        #print ship.getPositionList()
        #print "this is rot"
        #print isTurning
        #print ship.getTurnZone(isTurning)
        for i, j in mineList:
            print i,j
            for s,t in ship.getTurnZone(isTurning):
                if((i==s and j==t)):  
                    r = game.mineDamagedShip(ship, s, t, False, True)
                    if r == 1:
                        x = i
                        y = j
                        moveValid = False
                        removeMineList(i,j)
                        game.removeMine(i,j)
                        indigo = True
                        break
                if((i+1==s) and j==t):
                    r = game.mineDamagedShip(ship, s, t, False, True)
                    if r == 1:
                        x = i
                        y = j
                        moveValid = False
                        removeMineList(i,j)
                        game.removeMine(i,j)
                        indigo = True
                        break
                if((i-1==s) and j==t):
                    r = game.mineDamagedShip(ship, s, t, False, True)
                    if r == 1:
                        x = i
                        y = j
                        moveValid = False
                        removeMineList(i,j)
                        game.removeMine(i,j)
                        indigo = True
                        break
                if(i==s and (j+1)==t):
                    print "HERE"
                    r = game.mineDamagedShip(ship, s, t, False, True)
                    if r == 1:
                        x = i
                        y = j
                        moveValid = False
                        removeMineList(i,j)
                        game.removeMine(i,j)
                        indigo = True
                        break
                if (i==s and (j-1)==t):
                    r = game.mineDamagedShip(ship, s, t, False, True)
                    if r == 1:
                        x = i
                        y = j
                        moveValid = False
                        removeMineList(i,j)
                        game.removeMine(i,j)
                        indigo = True
                        break

    else:    
        if orientation == "E":
            if backwards == True:
                for i, j in mineList:
                    for s,t in ship.getPositionList():
                        if((i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):   
                            r = game.mineDamagedShip(ship, s, t, True, False)
                            if r == 1:
                                x = i
                                y = j
                                moveValid = True
                                removeMineList(i,j)
                                game.removeMine(i,j)
                                indigo = True
                                break
                if(indigo == False):
                    for i, j in mineList:
                        for s,t in ship.getPositionList():
                            if((i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):
                                r = game.mineDamagedShip(ship, s, t, True, False)
                                if r==1:
                                    x = i
                                    y = j
                                    moveValid = True
                                    removeMineList(i,j)
                                    game.removeMine(i, j)
                                    indigo = True
                                    break
            elif backwards == False:
                for i, j in mineList:
                    for s,t in ship.getPositionList():
                        if( (i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):
                            r = game.mineDamagedShip(ship, s, t, False, False)
                            if r == 1:
                                x = i
                                y = j
                                moveValid = True
                                removeMineList(i,j)
                                game.removeMine(i, j)
                                indigo = True
                                break

        if orientation == "W":
            if backwards == True:
                for i, j in mineList:
                    for s,t in ship.getPositionList():
                        if((i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):   
                            r = game.mineDamagedShip(ship, s, t, True, False)
                            if r == 1:
                                x = i
                                y = j
                                moveValid = True
                                removeMineList(i,j)
                                game.removeMine(i,j)
                                indigo = True
                                break
                if(indigo == False):
                    for i, j in mineList:
                        for s,t in ship.getPositionList():
                            if((i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):
                                t = game.mineDamagedShip(ship, s, t, True, False)
                                if t==1:
                                    x = i
                                    y = j
                                    moveValid = True
                                    removeMineList(i,j)
                                    game.removeMine(i, j)
                                    indigo = True
                                    break
            elif backwards == False:
                for i, j in mineList:
                    for s,t in ship.getPositionList():
                        if( (i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):
                            r = game.mineDamagedShip(ship, s, t, False, False)
                            if r == 1:
                                x = i
                                y = j
                                moveValid = True
                                removeMineList(i,j)
                                game.removeMine(i, j)
                                indigo = True
                                break

        if orientation == "N":
            if backwards == True:
                for i, j in mineList:
                    for s,t in ship.getPositionList():
                        if((i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):   
                            r = game.mineDamagedShip(ship, s, t, True, False)
                            if r == 1:
                                x = i
                                y = j
                                moveValid = True
                                removeMineList(i,j)
                                game.removeMine(i,j)
                                indigo = True
                                break
                if(indigo == False):
                    for i, j in mineList:
                        for s,t in ship.getPositionList():
                            if((i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):
                                t = game.mineDamagedShip(ship, s, t, True, False)
                                if t==1:
                                    x = i
                                    y = j
                                    moveValid = True
                                    removeMineList(i,j)
                                    game.removeMine(i, j)
                                    indigo = True
                                    break
            elif backwards == False:
                for i, j in mineList:
                    for s,t in ship.getPositionList():
                        if( (i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):
                            r = game.mineDamagedShip(ship, s, t, False, False)
                            if r ==1:
                                x = i
                                y = j
                                moveValid = True
                                removeMineList(i,j)
                                game.removeMine(i, j)
                                indigo = True
                                break
        if orientation == "S":
            if backwards == True:
                for i, j in mineList:
                    for s,t in ship.getPositionList():
                        if((i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):   
                            r = game.mineDamagedShip(ship, s, t, True, False)
                            if r == 1:
                                x = i
                                y = j
                                moveValid = True
                                removeMineList(i,j)
                                game.removeMine(i,j)
                                indigo = True
                                break
                if(indigo == False):
                    for i, j in mineList:
                        for s,t in ship.getPositionList():
                            if((i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):
                                t = game.mineDamagedShip(ship, s, t, True, False)
                                if t==1:
                                    x = i
                                    y = j
                                    moveValid = True
                                    removeMineList(i,j)
                                    game.removeMine(i, j)
                                    indigo = True
                                    break
            elif backwards == False:
                for i, j in mineList:
                    for s,t in ship.getPositionList():
                        if( (i==s and j==t) or ((i+1==s) and j==t) or ((i-1==s) and j==t) or (i==s and (j+1)==t) or (i==s and (j-1)==t)):
                            r = game.mineDamagedShip(ship, s, t, False, False)
                            if r == 1:
                                x = i
                                y = j
                                moveValid = True
                                removeMineList(i,j)
                                game.removeMine(i, j)
                                indigo = True
                                break

    if indigo:
        backwards == False
        resulttuple = (x,y)
        print "HER!!!"
        print resulttuple
        return resulttuple
    else:
        backwards == False
        resulttuple = (-1,-1)
        return resulttuple

def getMineDamagedCoordinates(ship,x,y, isTurning, screen, backwards):
    indigo = False
    orientation = ship.getOrientation()
    tuple = ()
    if isTurning:
        for i, j in mineList:
            for s,t in ship.getPositionBetween(x,y):
                if((i+1==s) and j==t):
                    tuple = (i+1, j)
                    indigo = True
                    break
                elif((i-1==s) and j==t and indigo == False):
                    tuple = (i-1, j)
                    indigo = True
                    break
                elif (i==s and (j+1)==t and indigo == False):
                    tuple = (i, j+1)
                    indigo = True
                    break
                elif (i==s and (j-1)==t and indigo == False):
                    tuple = (i, j-1)
                    indigo = True
                    break
                elif((i==s and j==t) and indigo == False):
                    tuple = (i,j)
                    indigo = True
                    break
    else:    
        if orientation == "E":
            if backwards == True:
                for i, j in mineList:
                    for s,t in ship.getPositionBetween(x,y):
                        if((i+1==s) and j==t):
                            tuple = (i+1, j)
                            indigo = True
                            break
                        elif((i-1==s) and j==t and indigo == False):
                            tuple = (i-1, j)
                            indigo = True
                            break
                        elif (i==s and (j+1)==t and indigo == False):
                            tuple = (i, j+1)
                            indigo = True
                            break
                        elif (i==s and (j-1)==t and indigo == False):
                            tuple = (i, j-1)
                            indigo = True
                            break
                        elif((i==s and j==t) and indigo == False):
                            tuple = (i,j)
                            indigo = True
                            break
                if(indigo == False):
                    for i, j in mineList:
                        for s,t in ship.getPositionBetween(x,y):
                            if((i+1==s) and j==t):
                                tuple = (i+1, j)
                                indigo = True
                                break
                            elif((i-1==s) and j==t and indigo == False):
                                tuple = (i-1, j)
                                indigo = True
                                break
                            elif (i==s and (j+1)==t and indigo == False):
                                tuple = (i, j+1)
                                indigo = True
                                break
                            elif (i==s and (j-1)==t and indigo == False):
                                tuple = (i, j-1)
                                indigo = True
                                break
                            elif((i==s and j==t) and indigo == False):
                                tuple = (i,j)
                                indigo = True
                                break
                            
            elif backwards == False:
                for i, j in mineList:
                    for s,t in ship.getPositionBetween(x,y):
                        if((i+1==s) and j==t):
                            tuple = (i+1, j)
                            indigo = True
                            break
                        elif((i-1==s) and j==t and indigo == False):
                            tuple = (i-1, j)
                            indigo = True
                            break
                        elif (i==s and (j+1)==t and indigo == False):
                            tuple = (i, j+1)
                            indigo = True
                            break
                        elif (i==s and (j-1)==t and indigo == False):
                            tuple = (i, j-1)
                            indigo = True
                            break
                        elif((i==s and j==t) and indigo == False):
                            tuple = (i,j)
                            indigo = True
                            break
                        

        if orientation == "W":
            if backwards == True:
                for i, j in mineList:
                    for s,t in ship.getPositionBetween(x,y):
                        if((i+1==s) and j==t):
                            tuple = (i+1, j)
                            indigo = True
                            break
                        elif((i-1==s) and j==t and indigo == False):
                            tuple = (i-1, j)
                            indigo = True
                            break
                        elif (i==s and (j+1)==t and indigo == False):
                            tuple = (i, j+1)
                            indigo = True
                            break
                        elif (i==s and (j-1)==t and indigo == False):
                            tuple = (i, j-1)
                            indigo = True
                            break
                        elif((i==s and j==t) and indigo == False):
                            tuple = (i,j)
                            indigo = True
                            break
                if(indigo == False):
                    for i, j in mineList:
                        for s,t in ship.getPositionBetween(x,y):
                            if((i+1==s) and j==t):
                                tuple = (i+1, j)
                                indigo = True
                                break
                            elif((i-1==s) and j==t and indigo == False):
                                tuple = (i-1, j)
                                indigo = True
                                break
                            elif (i==s and (j+1)==t and indigo == False):
                                tuple = (i, j+1)
                                indigo = True
                                break
                            elif (i==s and (j-1)==t and indigo == False):
                                tuple = (i, j-1)
                                indigo = True
                                break
                            elif((i==s and j==t) and indigo == False):
                                tuple = (i,j)
                                indigo = True
                                break
            elif backwards == False:
                for i, j in mineList:
                    for s,t in ship.getPositionBetween(x,y):
                        if((i+1==s) and j==t):
                            tuple = (i+1, j)
                            indigo = True
                            break
                        elif((i-1==s) and j==t and indigo == False):
                            tuple = (i-1, j)
                            indigo = True
                            break
                        elif (i==s and (j+1)==t and indigo == False):
                            tuple = (i, j+1)
                            indigo = True
                            break
                        elif (i==s and (j-1)==t and indigo == False):
                            tuple = (i, j-1)
                            indigo = True
                            break
                        elif((i==s and j==t) and indigo == False):
                            tuple = (i,j)
                            indigo = True
                            break

        if orientation == "N":
            if backwards == True:
                for i, j in mineList:
                    for s,t in ship.getPositionBetween(x,y):
                        if((i+1==s) and j==t):
                            tuple = (i+1, j)
                            indigo = True
                            break
                        elif((i-1==s) and j==t and indigo == False):
                            tuple = (i-1, j)
                            indigo = True
                            break
                        elif (i==s and (j+1)==t and indigo == False):
                            tuple = (i, j+1)
                            indigo = True
                            break
                        elif (i==s and (j-1)==t and indigo == False):
                            tuple = (i, j-1)
                            indigo = True
                            break
                        elif((i==s and j==t) and indigo == False):
                            tuple = (i,j)
                            indigo = True
                            break
                if(indigo == False):
                    for i, j in mineList:
                        for s,t in ship.getPositionBetween(x,y):
                            if((i+1==s) and j==t):
                                tuple = (i+1, j)
                                indigo = True
                                break
                            elif((i-1==s) and j==t and indigo == False):
                                tuple = (i-1, j)
                                indigo = True
                                break
                            elif (i==s and (j+1)==t and indigo == False):
                                tuple = (i, j+1)
                                indigo = True
                                break
                            elif (i==s and (j-1)==t and indigo == False):
                                tuple = (i, j-1)
                                indigo = True
                                break
                            elif((i==s and j==t) and indigo == False):
                                tuple = (i,j)
                                indigo = True
                                break
            elif backwards == False:
                for i, j in mineList:
                    for s,t in ship.getPositionBetween(x,y):
                        if((i+1==s) and j==t):
                            tuple = (i+1, j)
                            indigo = True
                            break
                        elif((i-1==s) and j==t and indigo == False):
                            tuple = (i-1, j)
                            indigo = True
                            break
                        elif (i==s and (j+1)==t and indigo == False):
                            tuple = (i, j+1)
                            indigo = True
                            break
                        elif (i==s and (j-1)==t and indigo == False):
                            tuple = (i, j-1)
                            indigo = True
                            break
                        elif((i==s and j==t) and indigo == False):
                            tuple = (i,j)
                            indigo = True
                            break
        if orientation == "S":
            if backwards == True:
                for i, j in mineList:
                    for s,t in ship.getPositionBetween(x,y):
                        if((i+1==s) and j==t):
                            tuple = (i+1, j)
                            indigo = True
                            break
                        elif((i-1==s) and j==t and indigo == False):
                            tuple = (i-1, j)
                            indigo = True
                            break
                        elif (i==s and (j+1)==t and indigo == False):
                            tuple = (i, j+1)
                            indigo = True
                            break
                        elif (i==s and (j-1)==t and indigo == False):
                            tuple = (i, j-1)
                            indigo = True
                            break
                        elif((i==s and j==t) and indigo == False):
                            tuple = (i,j)
                            indigo = True
                            break
                if(indigo == False):
                    for i, j in mineList:
                        for s,t in ship.getPositionBetween(x,y):
                            if((i+1==s) and j==t):
                                tuple = (i+1, j)
                                indigo = True
                                break
                            elif((i-1==s) and j==t and indigo == False):
                                tuple = (i-1, j)
                                indigo = True
                                break
                            elif (i==s and (j+1)==t and indigo == False):
                                tuple = (i, j+1)
                                indigo = True
                                break
                            elif (i==s and (j-1)==t and indigo == False):
                                tuple = (i, j-1)
                                indigo = True
                                break
                            elif((i==s and j==t) and indigo == False):
                                tuple = (i,j)
                                indigo = True
                                break
            elif backwards == False:
                for i, j in mineList:
                    for s,t in ship.getPositionBetween(x,y):
                        if((i+1==s) and j==t):
                            tuple = (i+1, j)
                            indigo = True
                            break
                        elif((i-1==s) and j==t and indigo == False):
                            tuple = (i-1, j)
                            indigo = True
                            break
                        elif (i==s and (j+1)==t and indigo == False):
                            tuple = (i, j+1)
                            indigo = True
                            break
                        elif (i==s and (j-1)==t and indigo == False):
                            tuple = (i, j-1)
                            indigo = True
                            break
                        elif((i==s and j==t) and indigo == False):
                            tuple = (i,j)
                            indigo = True
                            break

    if indigo:
        backwards == False
        return tuple
    else:
        backwards == False
        return tuple
def drawShip(surface, ship, x, y, rotation, game,screen):
    global VISIBLE
    VISIBLE = True
    r = rotation

    # game.getBoard().animate(screen,(pygame.time.get_ticks()/500)%2)

    global pList
    pList = ship.getPositionList()
    (x1, y1) = pList[0]
    (x2,y2) = pList[-1]



    global moveValid
    moveValid = True
    board = game.getBoard()

    
    radarList = [];
    if (ship.getSubclass() == "Kamikaze" and turnType != "positionActive" ):
        l = ship.getPositionList()
        for x1 in range(l[0][0] - 2, l[0][0] + 3):
            for y1 in range(l[0][1] - 2, l[0][1] + 3):
                radarList.append((x1, y1))
        
        if (x,y) in radarList:
            if (board.getSquare(x,y).getObjectOn() != None ):
                if (board.getSquare(x,y).getObjectOn() == ship):
                    moveValid = True;
                elif(board.getSquare(x,y).getObjectOn().getClassName() == "Mine"):  
                    moveValid = True;           
                    VISIBLE = True
                else:
                    moveValid = False;
        else:
            moveValid = False;


    
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
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"): 
                                VISIBLE = True          
                                moveValid = True            
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
                    go = False
                    for (i,j) in ship.getTurnZone(r):
                        if (board.getSquare(i,j).getObjectOn() != None ):
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):
                                VISIBLE = True
                                moveValid = True
                                go = True
                                break
                    if go == False:          
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
                            if(board.getSquare(i,y).getObjectOn == MineLayer):  
                                VISIBLE = True          
                                moveValid = True
                            else:
                                colx = i
                                coly = y
                                moveValid = False
                                break
                        i-=1
                else:
                    go = False  
                    for (i,j) in ship.getTurnZone(r):           
                        if (board.getSquare(i,j).getObjectOn() != None ):           
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                go = True           
                    if go == False:         
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
                            elif(board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):          
                                VISIBLE = True          
                                moveValid = True            
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
                    go = False  
                    for (i,j) in ship.getTurnZone(r):           
                        if (board.getSquare(i,j).getObjectOn() != None ):           
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                go = True           
                    if go == False:
                        moveValid = False

                
            #print moveValid
         

        elif  ( ship.getSubclass() != "Kamikaze" and turnType != "positionActive" and ((x - x1 ) >= -1 and ( x - x1 ) <= ship.getSpeed() and (y - y1) == 0) or ((y - y1) >= -1 and (y - y1) <= 1 and (x - x1) == 0)):
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
                    if (board.getSquare(i,y).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
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
                        if (board.getSquare(x-i,y).getObjectOn().getClassName() == "Mine"): 
                            VISIBLE = True          
                            moveValid = True            
                            break
                        else:
                            moveValid = False
                            break
                    i+=1
            #check obstacles behind
            elif x-ship.getSize() <= x2-1 :
                if (board.getSquare(x-ship.getSize()+1,y).getObjectOn() != None):
                    if (board.getSquare(x-ship.getSize()+1,y).getObjectOn().getClassName() == "Mine"):  
                        VISIBLE = True          
                        moveValid = True            
                    elif not board.getSquare(x-ship.getSize()+1,y).isVisible():
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
                    if (board.getSquare(i,y).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
                    elif (board.getSquare(i,y).getObjectOn()== ship):
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
                    if (board.getSquare(i,y).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
                    elif (board.getSquare(i,y).getObjectOn()== ship):
                        i+=1
                        continue
                    
                    moveValid = False
                    break
                i+=1
                
                
        elif (turnType == "positionActive" and ship.getSubclass() == 'Kamikaze'):
            bool99 = False  
            for (i,j) in ship.getTurnZone(r):           
                if (board.getSquare(i,j).getObjectOn() != None ):           
                    if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                        VISIBLE = True          
                        moveValid = True            
                        bool99 = True           
            if bool99 == False:         
                moveValid = False 
        elif ship.getSubclass() != 'Kamikaze':
            moveValid = False
            
        if moveValid == True:
            color = pygame.Color(194, 242, 221) #green
        else:
            color = pygame.Color(250, 200, 200) #red
        
        #print "Drawing", (x,y)
        
        
        if (ship.getSubclass() != "Kamikaze"):
            pygame.draw.polygon(surface, color, [(x*20 + x*1 + d , y*20 + y*1 + 10), (x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d+20 - 1, y*20 + y*1 + 20)], 0)
            x = x - 1
        else:
            pygame.draw.rect(surface, color, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
 
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
                            elif board.getSquare(i,y).getObjectOn().getClassName() == 'Mine':
                                #game.mineDamagedShip(ship, i, y)
                                moveValid = True 
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
                    bool3 = False   
                    for (i,j) in ship.getTurnZone(r):           
                        if (board.getSquare(i,j).getObjectOn() != None ):           
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                bool3 = True            
                    if bool3 == False:          
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
                            if (board.getSquare(i,y).getObjectOn().getClassName() == "Mine"): 
                                VISIBLE = True          
                                moveValid = True            
                                break
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
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"): 
                                VISIBLE = True          
                                moveValid = True            
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
                    bool5 = False   
                    for (i,j) in ship.getTurnZone(r):           
                       if (board.getSquare(i,j).getObjectOn() != None ):           
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                bool5 = True            
                    if bool5 == False:          
                        moveValid = False    

  

            if moveValid != False:
                color = pygame.Color(194, 242, 221) #green
        elif  ship.getSubclass() != "Kamikaze" and  turnType != "positionActive" and ((x - x1 ) <= 1 and ( x - x1 ) >= -ship.getSpeed() and (y - y1) == 0) or ((y - y1) >= -1 and (y - y1) <= 1 and (x - x1) == 0): 
            i = x
            # check for obsticals
            while i <= x1:
                if (board.getSquare(i,y).getObjectOn() != None ):
                    if (board.getSquare(i,y).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
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
                        if (board.getSquare(x+i,y).getObjectOn().getClassName() == "Mine"): 
                            VISIBLE = True          
                            moveValid = True            
                            break
                        if not board.getSquare(x+i,y).isVisible():
                            VISIBLE = False
                        else:
                            
                            moveValid = False
                        break
                    i+=1 
            #check obstacles behind
            elif x+ship.getSize() >= x2+1 :
                if (board.getSquare(x+ship.getSize()-1,y).getObjectOn() != None):
                    if board.getSquare(x + ship.getSize()-1, y).getObjectOn().getClassName() == "Mine": 
                        VISIBLE = True          
                        moveValid = True
                    elif not board.getSquare(x+ship.getSize()-1,y).isVisible():
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
                    if (board.getSquare(i,y).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
                    elif (board.getSquare(i,y).getObjectOn() == ship):
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
                    if (board.getSquare(i,y).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
                    elif (board.getSquare(i,y).getObjectOn() == ship):
                        i-=1
                        continue
                    
                    moveValid = False
                    break
                i-=1
            #print moveValid
   

                        
        else:
            bool8 = False   
            for (i,j) in ship.getTurnZone(r):           
                if (board.getSquare(i,j).getObjectOn() != None ):           
                    if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                        VISIBLE = True          
                        moveValid = True            
                        bool8 = True            
            if(bool8 == False):         
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
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"): 
                                print 'hit Mine'            
                                VISIBLE = True          
                                moveValid = True            
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
                    go = False  
                    for (i,j) in ship.getTurnZone(r):           
                        if (board.getSquare(i,j).getObjectOn() != None):            
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                go = True           
                    if go == False:         
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
                            elif(board.getSquare(x,i).getObjectOn() == MineLayer):  
                                VISIBLE = True          
                                moveValid = True            
                                break
                            elif not board.getSquare(i,y).isVisible():
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
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"): 
                                VISIBLE = True          
                                moveValid = True
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
                    bool1 = False   
                    for (i,j) in ship.getTurnZone(r):           
                        if (board.getSquare(i,j).getObjectOn() != None ):           
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                bool1 = True            
                    if(bool1 == False):         
                        moveValid = False 
            if moveValid != False:
                color = pygame.Color(194, 242, 221) #green

        elif ship.getSubclass() != "Kamikaze" and  turnType != "positionActive" and (( x - x1 ) == 0 and (y - y1) >= -1 and (y - y1) <= ship.getSpeed()) or (abs(( x - x1 )) == 1 and (y - y1) ==0) : 
            
            # check for obstacle
            i = y1
            while i <= y:
                if (board.getSquare(x,i).getObjectOn() != None ):
                    #print board.getSquare(x,i).getObjectOn()
                    if (board.getSquare(x,i).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break 
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
                        if (board.getSquare(x,y-i).getObjectOn().getClassName() == "Mine"): 
                            VISIBLE = True          
                            moveValid = True            
                            break
                        if not board.getSquare(x,y-i).isVisible():
                            VISIBLE = False
                        else:
                            moveValid = False
                        break
                    i+=1
            #check obstacle behind
            elif y-ship.getSize() <= y2-1 :
                if (board.getSquare(x,y-ship.getSize()+1).getObjectOn() != None):
                    if (board.getSquare(x,y-ship.getSize()+1).getObjectOn().getClassName() == "Mine"):  
                        VISIBLE = True          
                        moveValid = True
                    elif not board.getSquare(x,y-ship.getSize()+1).isVisible():
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
                    if (board.getSquare(x,i).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
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
                    if (board.getSquare(x,i).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
                    if (board.getSquare(x,i).getObjectOn()== ship):
                        i+=1
                        continue
                    color = pygame.Color(250, 200, 200) #red
                    moveValid = False
                    break
                i+=1
        else:
            bool9 = False   
            for (i,j) in ship.getTurnZone(r):           
                if (board.getSquare(i,j).getObjectOn() != None ):           
                    if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                        VISIBLE = True          
                        moveValid = True            
                        bool9 = True            
            if(bool9 == False):         
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
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):    
                                print 'hit Mine'            
                                VISIBLE = True          
                                moveValid = True            
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
                    bool9 = False   
                    for (i,j) in ship.getTurnZone(r):           
                        if (board.getSquare(i,j).getObjectOn() != None ):           
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                bool9 = True            
                    if(bool9 == False):         
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
                            if(board.getSquare(x,i).getObjectOn().getClassName() == "Mine"):    
                                print "p1"          
                                potentialmine = True            
                                moveValid = True            
                                VISIBLE = True          
                                go = True           
                                break
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
                    bool10 = False  
                    for (i,j) in ship.getTurnZone(r):           
                        if (board.getSquare(i,j).getObjectOn() != None ):           
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                bool10 = True           
                    if bool10 == False:         
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
                            elif (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"): 
                                #print "GOnna hit Mine"         
                                VISIBLE = True          
                                moveValid = True            
                                go = True           
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
                    bool10 = False  
                    for (i,j) in ship.getTurnZone(r):           
                        if (board.getSquare(i,j).getObjectOn() != None ):           
                            if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                                VISIBLE = True          
                                moveValid = True            
                                bool10 = True           
                    if bool10 == False:         
                        moveValid = False  
           
        elif ship.getSubclass() != "Kamikaze" and turnType != "positionActive" and (( x - x1 ) == 0 and (y1 - y) >= -1 and (y1 - y) <= ship.getSpeed()) or (abs(( x - x1 )) == 1 and (y - y1) ==0) : 
            # check for obsticals
            i = y
            while i <= y1:
                if (board.getSquare(x,i).getObjectOn() != None ):
                    if (board.getSquare(x,i).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
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
                        if (board.getSquare(x,y+i).getObjectOn().getClassName() == "Mine"): 
                            VISIBLE = True          
                            moveValid = True            
                            break
                        if not board.getSquare(i,y+i).isVisible():
                            VISIBLE = False
                        else:
                            moveValid = False
                        break
                    i+=1 
            
            #check obsticals behind
            elif y+ship.getSize() >= y2+1 :
                if (board.getSquare(x,y+ship.getSize()-1).getObjectOn() != None):
                    if (board.getSquare(x,y+ship.getSize()-1).getObjectOn().getClassName() == "Mine"):  
                        VISIBLE = True          
                        moveValid = True
                    elif not board.getSquare(i,y+ship.getSize()-1).isVisible():
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
                    if (board.getSquare(x,i).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
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
                    if (board.getSquare(x,i).getObjectOn().getClassName() == "Mine"):   
                        VISIBLE = True          
                        moveValid = True            
                        break
                    if (board.getSquare(x,i).getObjectOn() == ship):
                        i-=1
                        continue
                    
                    color = pygame.Color(250, 200, 200) #red
                    moveValid = False
                    break
                i-=1

        else:
            bool11 = False  
            for (i,j) in ship.getTurnZone(r):           
                if (board.getSquare(i,j).getObjectOn() != None ):           
                    if (board.getSquare(i,j).getObjectOn().getClassName() == "Mine"):           
                        VISIBLE = True          
                        moveValid = True            
                        bool11 = True           
            if bool11 == False:         
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
    main('offline','player1','player2',True,[],'')
