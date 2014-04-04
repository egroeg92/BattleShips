from PlayerState import PlayerState
from Board import Board
from Square import Square
from reefGeneration import reefGeneration
import pygame

class Game(object):
    def __init__(self, player,coral):
        self.player = player
        if player:    
            self.player1 = PlayerState(True)
            self.player2 = PlayerState(False)
        else:
            self.player1 = PlayerState(False)
            self.player2 = PlayerState(True)

        self.shiplist = self.player1.getShipList() + self.player2.getShipList()
        # coral = [(10, 3), (18, 4), (17, 9), (10,10), (14, 11), (18, 20), (16, 26), (10, 23)]
        self.coral = coral
        P1E_front = pygame.image.load('images/FE.png').convert()
        P1EW_mid = pygame.image.load('images/EW.png').convert()

        E_frontD = pygame.image.load('images/FED.png').convert()
        EW_midD = pygame.image.load('images/EWD.png').convert()

        E_frontDe = pygame.image.load('images/FEDe.png').convert()
        EW_midDe = pygame.image.load('images/EWDe.png').convert()

        E_frontS = pygame.image.load('images/FEs.png').convert()
        EW_midS = pygame.image.load('images/EWs.png').convert()

        P1N_front = pygame.image.load('images/P1FN.png').convert()
        P1NS_mid = pygame.image.load('images/NS.png').convert()
        
        N_frontD = pygame.image.load('images/FND.png').convert()
        NS_midD = pygame.image.load('images/NSD.png').convert()

        N_frontDe = pygame.image.load('images/FNDe.png').convert()
        NS_midDe = pygame.image.load('images/NSDe.png').convert()
        
        N_s = pygame.image.load('images/FNs.png').convert()
        NS_s = pygame.image.load('images/NSs.png').convert()


        FW_s = pygame.image.load('images/FWs.png').convert()
        FWD = pygame.image.load('images/FWD.png').convert()
        FWDe = pygame.image.load('images/FWDe.png').convert()
        P1_Wfront =pygame.image.load('images/FW.png').convert()

        FS_s = pygame.image.load('images/FSs.png').convert()
        FSD = pygame.image.load('images/FSD.png').convert()
        FSDe = pygame.image.load('images/FSDe.png').convert()
        P1_Sfront =pygame.image.load('images/P1FS.png').convert()

        P2NF = pygame.image.load('images/P2FN.png').convert()
        P2EWM = pygame.image.load('images/P2EW.png').convert()
        P2SF = pygame.image.load('images/P2FS.png').convert()
        P2EF =pygame.image.load('images/P2FE.png').convert()
        P2WF =pygame.image.load('images/P2FW.png').convert()
        P2NSM = pygame.image.load('images/P2NSM.png').convert()

        w1 = pygame.image.load('images/water1.png').convert()
        w2 = pygame.image.load('images/water2.png').convert()
        dw1 = pygame.image.load('images/darkwater1.png').convert()
        dw2 = pygame.image.load('images/darkwater2.png').convert()

        c1 = pygame.image.load('images/coral1.png').convert()
        c2 = pygame.image.load('images/coral2.png').convert()

        note = pygame.image.load('images/notifier.png').convert()

        
        
        images = []
        images.append(P1E_front)
        images.append(P1EW_mid)
        images.append(E_frontD)
        images.append(EW_midD)
        images.append(E_frontDe)
        images.append(EW_midDe)
        images.append(E_frontS)
        images.append(EW_midS)

        images.append(P1N_front)
        images.append(P1NS_mid)
        images.append(N_frontD)
        images.append(NS_midD)
        images.append(N_frontDe)
        images.append(NS_midDe)
        images.append(N_s)
        images.append(NS_s)

        images.append(P1_Wfront)
        images.append(FWD)
        images.append(FWDe)
        images.append(FW_s)

        images.append(P1_Sfront)
        images.append(FSD)
        images.append(FSDe)
        images.append(FS_s)
        
        images.append(P2NF) 
        images.append(P2EWM) 
        images.append(P2SF) 
        images.append(P2EF) 
        images.append(P2WF) 
        images.append(P2NSM) 

        images.append(w1)
        images.append(w2)
        images.append(dw1)
        images.append(dw2)

        images.append(c1)
        images.append(c2)
        images.append(note)
        
        self.gameBoard = Board(coral,images)
        self.updateVisibility()
        self.updateVisibilityRadar()
        self.updateBoard()

    #?
    def getCoral(self):
        return self.coral        
    #?
    def setCoral(self, coral):
        self.coral = coral
    #?
    def updateReef(self, reefGenerator,corallist, oldcorallist):
        for (x,y) in oldcorallist:
            #print game.getBoard().getSquare(x,y).getObjectOn()
            sq = Square(None,(x,y))
            self.getBoard().setSquare(x,y, sq)
        for x in range(24):
            coordinate = reefGenerator.random()
            corallist.append(coordinate)  
        
        
                    
    def getCurrentPlayer(self):
        return self.player1
    
    def getOpponent(self):
        return self.player2
    
    def getBoard(self):
        return self.gameBoard;
    
    def updateBoard(self):
        for ship in self.shiplist:

            dead = True
            for h in ship.getHealth():
                if h !=0:
                    dead = False
            
            if dead:
                continue
                  
        # for ship in self.player1.getShipList():
            plist = ship.getPositionList();
            for (x,y) in plist:
                self.gameBoard.getSquare(x, y).setObjectOn(ship)
                
                
        for (x,y) in self.player1.getBase().getPositionList():
            self.gameBoard.getSquare(x, y).setObjectOn(self.player1.getBase())
 
        for (x,y) in self.player2.getBase().getPositionList():
            self.gameBoard.getSquare(x, y).setObjectOn(self.player2.getBase())       
      
      
    def positionShip(self, x1, y1, rotation):
        # for ship in self.player1.getShipList():
        for ship in self.shiplist:
            if ship.isSelected():
                #print "position ship"
                
                newOrientation = ship.getOrientation()
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
                
                for (x,y) in ship.getPositionList():
                    self.gameBoard.getSquare(x, y).setObjectOn(None)
                
                if newOrientation == "E":
                    newpos=[]
                    for i in range(ship.getSize()):
                        newpos.append((x1,y1))
                        x1 = x1 - 1
                if newOrientation == "W":
                    newpos=[]
                    for i in range(ship.getSize()):
                        newpos.append((x1,y1))
                        x1 = x1 + 1
                if newOrientation == "S":
                    newpos=[]
                    for i in range(ship.getSize()):
                        newpos.append((x1,y1))
                        y1 = y1 - 1
                if newOrientation == "N":
                    newpos=[]
                    for i in range(ship.getSize()):
                        newpos.append((x1,y1))
                        y1 = y1 + 1
                        
                ship.setOrientation(newOrientation)
                #print ship.getPositionList()
                #print newpos
                ship.setPositionList(newpos)
                
                for (x,y) in ship.getPositionList():
                    self.gameBoard.getSquare(x,y).setObjectOn(ship)
                
                self.updateVisibility()
                self.updateVisibilityRadar()



        
    def moveShip(self, x1, y1, visible):
        if not visible:
            #print 'COLLISION'
            return
        else:
            print 'moving...'

        # for ship in self.player1.getShipList():
        for ship in self.shiplist:
            if ship.isSelected():
                #print "move ", ship.getClassName()
                
                for (x,y) in ship.getPositionList():
                    self.gameBoard.getSquare(x, y).setObjectOn(None)
                ship.move(x1, y1)
                ship.selected = False
                
                for (x,y) in ship.getPositionList():
                    self.gameBoard.getSquare(x,y).setObjectOn(ship)
        self.updateVisibility()
        self.updateVisibilityRadar()

                
    def rotate(self, ship,rot,end,visible):
        if not visible:
            #print 'COLLISION'
            return
        else:
            print 'moving...'
        
        for (x,y) in ship.getPositionList():
            self.gameBoard.getSquare(x, y).setObjectOn(None)
        if end:
            ship.rotateClockwiseEnd(rot)
        else:
            ship.rotateClockwiseCenter(rot)
        
        #print ship.getPositionList()
        for (x,y) in ship.getPositionList():
            self.gameBoard.getSquare(x,y).setObjectOn(ship)
        self.updateVisibility()
        self.updateVisibilityRadar()

 

    def fireCannon(self, x, y):
        # for ship in self.player1.getShipList():
        for ship in self.shiplist:
            if ship.isSelected():
                sq = self.gameBoard.getSquare(x,y)
                object = sq.getObjectOn()
                #print object
                if object == None:
                    return "Shot fell into water" + " at " + str((x,y))                    
                elif object.getClassName() == "Coral":
                    return "Shot hit coral" + " at " + str((x,y))    
                elif object.getClassName() == "Base":
                    index = object.positionIndex((x,y))
                    health = object.getHealth()
                    #print "INITIAL HEALTH:",health  
                    health[index] = 0
                    sq.setObjectOn(None)    # remove base
                    return "base hit : REMAINING HEALTH: " + str(health)

                elif object.getClassName() == "Ship":
                    index = object.positionIndex((x,y))
                    armour = object.getArmour()
                    #print armour  # 1 (Normal)  2 (Heavy)
                    health = object.getHealth()
                    #print "INITIAL HEALTH:",health
                    if armour == 2 and health[index] != 0:
                        health[index] = health[index] - 1
                        if sum(health) == 0:
                            object.destroyShip(self.gameBoard)
                            self.updateVisibility()
                            self.updateVisibilityRadar()

                            return "ship sunk :"+object.getName()

                        object.updateSpeed()
                        return "ship hit : REMAINING HEALTH: " + str(health)
                    else:
                        health[index] = 0
                        if sum(health) == 0:
                            object.destroyShip(self.gameBoard)
                            self.updateVisibility()
                            self.updateVisibilityRadar()
                            # object.updateSpeed()
                            return "ship sunk :"+object.getName()


                        object.updateSpeed()
                        return "ship hit : FINAL HEALTH: " + str(health)

                    object.updateSpeed() 
        


    def fireHeavyCannon(self, x, y):
        # for ship in self.player1.getShipList():

        for ship in self.shiplist:
            if ship.isSelected():
                sq = self.gameBoard.getSquare(x,y)
                object = sq.getObjectOn()
                #print object
                if object == None:
                    return "Shot fell into water" + " at " + str((x,y))                    
                elif object.getClassName() == "Coral":
                    return "Shot hit coral" + " at " + str((x,y))   
                elif object.getClassName() == "Base":
                    index = object.positionIndex((x,y))
                    health = object.getHealth()
                    #print "INITIAL HEALTH:",health  
                    health[index] = 0
                    sq.setObjectOn(None)    # remove base
                    return "base hit : FINAL HEALTH: " + str(health)
                elif object.getClassName() == "Ship":
                    index = object.positionIndex((x,y))
                    armour = object.getArmour()
                    #print armour  # 1 (Normal)  2 (Heavy)
                    health = object.getHealth()
                    #print "INITIAL HEALTH:",health  
                    health[index] = 0
                    if sum(health) == 0:
                        object.destroyShip(self.gameBoard)
                        self.updateVisibility()
                        self.updateVisibilityRadar()
                        return "ship sunk :"+object.getName()

                    object.updateSpeed()                        
                    return "ship hit : REMAINING HEALTH: " + str(health)                    

    def fireTorpedo(self, x, y):
        # for ship in self.player1.getShipList():

        for ship in self.shiplist:
            if ship.isSelected():
                object = None
                tuple = ()
                pList = ship.getPositionBetween(x, y)
                #print pList # returns the list of positions
                for (xs,ys) in pList:
                    objectOn = self.gameBoard.getSquare(xs,ys).getObjectOn()
                    # if it is sea or ship with 0 health
                    if objectOn == None or objectOn.getClassName() == "Ship" and objectOn.getHealth()[objectOn.positionIndex((xs,ys))] == 0:
                        tuple = (xs,ys)
                        #print tuple
                    # if it is a ship with health remaining
                    elif (objectOn.getClassName() == "Ship" and objectOn.getHealth()[objectOn.positionIndex((xs,ys))] != 0):
                        object = objectOn
                        tuple = (xs,ys)
                        #print tuple
                        break
                    # if it is a coral or a base
                    elif (objectOn != None and objectOn.getClassName() != "Ship"):
                        object = objectOn
                        tuple = (xs,ys)
                        #print tuple
                        break                        

                sq = self.gameBoard.getSquare(tuple[0], tuple[1])
                object = sq.getObjectOn()
                orientation = ship.getOrientation()

                if object == None:
                    return "Shot disappeared" + " at " + str(tuple)    
                elif object.getClassName() == "Coral":
                    return "Shot hit coral" + " at " + str(tuple)
                elif object.getClassName() == "Base":
                    index = object.positionIndex(tuple)
                    health = object.getHealth()
                    health[index] = 0
                    sq.setObjectOn(None)    # remove base
                    return "Base hit" + str(health)

                elif object.getClassName() == "Ship":
                    if (((object.getOrientation() == "E" or object.getOrientation() == "W") and (orientation == "N" or orientation == "S")) or ((object.getOrientation() == "N" or object.getOrientation() == "S") and (orientation == "E" or orientation == "W"))):
                        index = object.positionIndex(tuple)
                        armour = object.getArmour()
                        health = object.getHealth()
                        
                        if armour == 2 and health[index] != 0:      # if armoured and still have health
                            health[index] = health[index] - 1
                
                            if (index == object.getSize() - 1 and health[index - 1] != 0):      # if at the end of the ship and it's side square is not dead
                                health[index - 1] = health[index - 1] - 1                       # damage the side 
                            elif (index == object.getSize() - 1 and health[index - 1] == 0):    # if at the end of the ship and it's side square is dead
                                health[index] = health[index]                                   # no damage
                            elif(index == 0 and health[index + 1] != 0):                        # if at head and its side square is not damaged
                                health[index + 1] = health[index + 1] - 1                       # damage the square beside the head                                
                            elif(index == 0 and health[index + 1] == 0):                        # if at head and its side square is already dead
                                health[index] = health[index]                                   # no damage
                            else:
                                if (health[index - 1] != 0):
                                    health[index - 1] = health[index - 1] - 1
                                elif(health[index + 1] != 0):
                                    health[index + 1] = health[index + 1] - 1
                            if sum(health) == 0:
                                object.destroyShip(self.gameBoard)
                                self.updateVisibility()
                                self.updateVisibilityRadar()
                                return "ship sunk :"+object.getName()

                            object.updateSpeed()                            
                            return "ship hit : REMAINING HEALTH: " + str(health)
                            
                        elif armour == 2 and health[index] == 0:    # if armoured and no health                         
                            health[index] = 0

                            object.updateSpeed()
                            return "ship hit : FINAL HEALTH: " + str(health)
                            
                        elif armour == 1 and health[index] == 0:    # if not armoured and no health                         
                            health[index] = 0             

                            object.updateSpeed()
                            return "ship hit : FINAL HEALTH: " + str(health)               
                        else:                                       # if not armoured
                            health[index] = 0
                            if (index == object.getSize() - 1):                                
                                health[index - 1] = 0 
                            elif(index == 0):
                                health[index + 1] = 0                                
                            else:
                                if (health[index - 1] != 0):
                                    health[index - 1] = 0
                                elif(health[index + 1] != 0):
                                    health[index + 1] = 0
                            if sum(health) == 0:
                                object.destroyShip(self.gameBoard) 
                                self.updateVisibility()
                                self.updateVisibilityRadar()
                                return "ship sunk :"+object.getName()

                            object.updateSpeed()
                            return "ship hit : FINAL HEALTH: " + str(health)
                    else:                                            # firing at straight on onto a ship
                        index = object.positionIndex(tuple)
                        armour = object.getArmour()
                        health = object.getHealth()
                        #print "INITIAL HEALTH:",health  
                        if armour == 2 and health[index] != 0:
                            health[index] = health[index] - 1
                            if sum(health) == 0:
                                object.destroyShip(self.gameBoard)
                                self.updateVisibility()
                                self.updateVisibilityRadar()
                                return "ship sunk :"+object.getName()

                            object.updateSpeed()                            
                            return "ship hit : REMAINING HEALTH: " + str(health)                             
                        else:
                            health[index] = 0
                            if sum(health) == 0:
                                object.destroyShip(self.gameBoard) 
                                self.updateVisibility()
                                self.updateVisibilityRadar()
                                return object.getName() + " sunk"

                            object.updateSpeed()
                            return "ship hit : FINAL HEALTH: " + str(health)
        self.updateVisibility()
        self.updateVisibilityRadar()
    
    def repairShip(self, ship):
        i = 0
        squarehealth = ship.getSquareHealth()
        health = ship.getHealth()
        for h in health:
            if h != squarehealth:
                health[i] = squarehealth
                break
            else:
                i = i + 1

    def updateRange(self, type, update):
        for x in range(30):
            for y in range(30):
                # #print x,y
                self.gameBoard.getSquare(x, y).setActiveRange(False)

        if not update:
            return
        
        if type == "heavycannon":
            for ship in self.player1.getShipList():
                if ship.isSelected():
                    list = ship.getHeavyCannonRange()
                    # #print list
                    for (x,y) in list:
                        # #print x,y
                        self.gameBoard.getSquare(x, y).setActiveRange(True)
        elif type == "cannon":
            for ship in self.player1.getShipList():
                if ship.isSelected():
                    list = ship.getCannonRange()
                    
                    for (x,y) in list:
                        self.gameBoard.getSquare(x, y).setActiveRange(True)
        elif type == "torpedo":
            for ship in self.player1.getShipList():
                if ship.isSelected():
                    list = ship.getTorpedoRange()

                    for (x,y) in list:
                        self.gameBoard.getSquare(x, y).setActiveRange(True)            

    def updateVisibility(self):

        radarList = []
        b = self.player1.getBase().getPositionList()
        #print 'base coords ', b

        x = b[0][0]
        y = b[0][1] 

        # i = 1
        if self.player:
            radarList.append((x,y-1))
            while y <20:
                radarList.append((x+1, y))
                y+=1
            radarList.append((x,y))
        else:
            radarList.append((x,y-1))
            while y <20:
                radarList.append((x-1, y))
                y+=1
            radarList.append((x,y))


        #print radarList

        for ship in self.player1.getShipList():
            
            dead = True
            for h in ship.getHealth():
                if h !=0:
                    dead = False
            
            if dead:
                continue
            
            if (ship.getSubclass() != "MineLayer"):
                l = ship.getPositionList()
                if (ship.getOrientation() == "W"):
                    radarList.append(l[-1])
                    for x1 in range(l[-1][0] - ship.getRadarX() , l[-1][0]):
                        for y1 in range (l[-2][1] - 1, l[-2][1] + 2):
                            
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "E"):
                    radarList.append(l[-1])
                    for x1 in range(l[-2][0], l[-2][0] + ship.getRadarX()):
                        for y1 in range (l[-2][1] - 1, l[-2][1] + 2):
                            
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "N"):
                    radarList.append(l[-1])
                    for x1 in range(l[-2][0] - 1, l[-2][0] + 2):
                        for y1 in range (l[-1][1] - ship.getRadarX(), l[-1][1]):
                            
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "S"):
                    radarList.append(l[-1])
                    for x1 in range(l[-2][0] - 1, l[-2][0] + 2):
                        for y1 in range (l[-2][1], l[-2][1] + ship.getRadarX()):
                            radarList.append((x1, y1))
            else:
                l = ship.getPositionList()
                if (ship.getOrientation() == "E"):
                    for x1 in range(l[0][0] - 3, l[1][0] + 4):
                        for y1 in range(l[0][1] - 2, l[0][1] + 3):
                            radarList.append((x1, y1))
                elif ( ship.getOrientation() == "W"):
                    for x1 in range(l[1][0] - 3, l[0][0] + 4):
                        for y1 in range(l[0][1] - 2, l[0][1] + 3):
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "N" ):
                    for x1 in range(l[0][0] - 2, l[0][0] + 3):
                        for y1 in range(l[1][1] - 3, l[0][1] + 4):
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "S"):
                    for x1 in range(l[0][0] - 2, l[0][0] + 3):
                        for y1 in range(l[0][1] - 3, l[1][1] + 4):
                            radarList.append((x1, y1))

        for i in range(30):
            for j in range(30):


                if (i,j) in radarList:
                    self.gameBoard.getSquare(i,j).setVisible(True)
                else:
                    self.gameBoard.getSquare(i,j).setVisible(False)

                if self.gameBoard.getSquare(i,j).getObjectOn() != None:
                
                    if self.gameBoard.getSquare(i,j).getObjectOn().getClassName() == 'Coral':
                        # print 'dfd'
                        self.gameBoard.getSquare(i,j).setVisible(True)



                # self.gameBoard.getSquare(i,j).setVisible(True)

    def updateVisibilityRadar(self):
        radarList = []
        for ship in self.player1.getShipList():
            
            dead = True
            for h in ship.getHealth():
                if h !=0:
                    dead = False
            
            if dead:
                continue
            if (ship.getName() == "RadarBoat" and ship.getLongRadar()):
                l = ship.getPositionList()
                if (ship.getOrientation() == "W"):
                    radarList.append(l[-1])
                    for x1 in range(l[-1][0] - ship.getLongRadarX() , l[-1][0]):
                        for y1 in range (l[-2][1] - 1, l[-2][1] + 2):
                            
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "E"):
                    radarList.append(l[-1])
                    for x1 in range(l[-2][0], l[-2][0] + ship.getLongRadarX()):
                        for y1 in range (l[-2][1] - 1, l[-2][1] + 2):
                            
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "N"):
                    radarList.append(l[-1])
                    for x1 in range(l[-2][0] - 1, l[-2][0] + 2):
                        for y1 in range (l[-1][1] - ship.getLongRadarX(), l[-1][1]):
                            
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "S"):
                    radarList.append(l[-1])
                    for x1 in range(l[-2][0] - 1, l[-2][0] + 2):
                        for y1 in range (l[-2][1], l[-2][1] + ship.getLongRadarX()):
                            radarList.append((x1, y1))

        for i in range(30):
            for j in range(30):


                if (i,j) in radarList:
                    self.gameBoard.getSquare(i,j).setVisible(True)
                #else:
                #    self.gameBoard.getSquare(i,j).setVisible(False)

                if self.gameBoard.getSquare(i,j).getObjectOn() != None:
                
                    if self.gameBoard.getSquare(i,j).getObjectOn().getClassName() == 'Coral':
                        # print 'dfd'
                        self.gameBoard.getSquare(i,j).setVisible(True)
                            
                            
                