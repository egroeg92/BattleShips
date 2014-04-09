from PlayerState import PlayerState
from Board import Board
from Square import Square
from reefGeneration import reefGeneration
import pygame
from Coral import Coral

reefGenerator = reefGeneration()

class Game(object):
    def __init__(self, player,coral,user,opp):
        self.player = player
        if player:    
            self.player1 = PlayerState(True,user)
            self.player2 = PlayerState(False,opp)
        else:
            self.player1 = PlayerState(False,user)
            self.player2 = PlayerState(True,opp)

        self.shiplist = self.player1.getShipList() + self.player2.getShipList()
        # coral = [(10, 3), (18, 4), (17, 9), (10,10), (14, 11), (18, 20), (16, 26), (10, 23)]
        self.coral = coral

        self.gameBoard = Board(coral)
        self.updateVisibility()
        self.updateVisibilityRadar()
        self.updateBoard()
        self.turn = True
        self.turnType = ''

    #?

    def reversePlayers(self):
        x = self.player1
        self.player1 = self.player2
        self.player2 = self.player1

    def setTurn(self,var):
        self.turn = var
    def getTurn(self):
        return self.turn
    def setTurnType(self,var):
        self.turnType = var      
    def getTurnType(self):
        return self.turnType


    #?
    def getCoral(self):
        return self.coral        
    #?
    def setCoral(self, coral):
        oldcorallist = self.coral
        print 'oldcorallist ',oldcorallist
        
        for (x,y) in oldcorallist:
            sq = Square(None,(x,y))
            self.getBoard().setSquare(x,y, sq)
               
        self.coral = coral
        for (x,y) in self.coral:
            c = Coral()
            sq = Square(c,(x,y))
            self.getBoard().setSquare(x,y, sq)
        
        
        self.updateVisibility()
        
    #?
    def randomizeReef(self,corallist):
        
        i = 0
        j = 0
        k = 0
        l = 0
        while i != 11:
            coordinate = reefGenerator.random()
            if coordinate not in corallist:
                corallist.append(coordinate)
                i = i + 1
        while j != 1:
            coordinate = reefGenerator.randommid()
            if coordinate not in corallist:
                corallist.append(coordinate)
                j = j + 1
        while k != 1:
            coordinate = reefGenerator.randommid2()
            if coordinate not in corallist:
                corallist.append(coordinate)
                k = k + 1
        while l != 11:
            coordinate = reefGenerator.random2()
            if coordinate not in corallist:
                corallist.append(coordinate)
                l = l + 1

        return corallist
        print "Length of corallist is: ", len(corallist)       
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

    def mineDamagedShip(self, ship, x, y, backwards):
        if ship.getName() == "Kamikaze":
                health = ship.getHealth()
                health[0] = 0
                print sum(health)
                if sum(health) == 0:
                    ship.destroyKamakazi(self.gameBoard,x,y)
                    self.updateVisibility()
                    self.updateVisibilityRadar()

        elif ship.getName() != "Kamikaze": # This can be easily changed if the minelayer does not get destroyed
            tuple = (x,y)
            index = ship.positionIndex(tuple)
            health = ship.getHealth()
            if backwards:
                health[-1] = 0
                health[-2] = 0
            else:
                print ship.getName()
                print ship.getHealth()
                if(sum(health) <= 4  and ship.getName() == "Cruiser"):
                    ship.destroyShip(self.gameBoard)
                    self.updateVisibility()
                    self.updateVisibilityRadar()
                    return 1

                elif(sum(health) <= 2  and ship.getName() == "Destroyer"):
                    ship.destroyShip(self.gameBoard)
                    self.updateVisibility()
                    self.updateVisibilityRadar()
                    return 1

                elif(sum(health) <= 2  and ship.getName() == "TorpedoBoat"):
                    ship.destroyShip(self.gameBoard)
                    self.updateVisibility()
                    self.updateVisibilityRadar()
                    return 1

                elif(sum(health) <= 2  and ship.getName() == "RadarBoat"):
                    ship.destroyShip(self.gameBoard)
                    self.updateVisibility()
                    self.updateVisibilityRadar()
                    return 1

                elif(index == 0):
                    health[index] = 0
                    health[index+1] = 0

                else:
                    health[index] = 0
                    health[index-1] = 0
                    print health
            if sum(health) == 0:
                ship.destroyShip(self.gameBoard)
                self.updateVisibility()
                self.updateVisibilityRadar()
                return 1
            else:
                return 0
    
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

    def dropMine(self, x, y):
        if(x<30 and y<30):
            objectOn = self.gameBoard.getSquare(x,y).getObjectOn()  
            if objectOn == None:
        # if mine is not dropped on base or coal, or a ship, or another mine then it cant be droppped                
                if(y-1 >= 0):
                    objectOnN = self.gameBoard.getSquare(x,(y-1)).getObjectOn()
                    if objectOnN != None:
                        if(objectOnN.getClassName() == "Ship"):
                            if objectOnN.getName() != "MineLayer":
                                return "Cant drop mine at selected location"
                        if(objectOnN.getClassName() != "Ship" and objectOnN.getClassName() != "Mine"):
                            return "Cant drop mine at selected location"
                if(x+1 < 30):
                    objectOnE = self.gameBoard.getSquare((x+1),y).getObjectOn()
                    if objectOnE != None:
                        if(objectOnE.getClassName() == "Ship"):
                            if objectOnE.getName() != "MineLayer":
                                return "Cant drop mine at selected location" 
                        if(objectOnE.getClassName() != "Ship" and objectOnE.getClassName() != "Mine"):
                            return "Cant drop mine at selected location"
                                   
                if(y+1 < 30):
                    objectOnS = self.gameBoard.getSquare(x,(y+1)).getObjectOn()
                    if objectOnS != None:
                        if(objectOnS.getClassName() == "Ship"):
                            if objectOnS.getName() != "MineLayer":
                                return "Cant drop mine at selected location"
                        if(objectOnS.getClassName() != "Ship" and objectOnS.getClassName() != "Mine"):
                            return "Cant drop mine at selected location"

                if(x-1 >= 0): 
                    objectOnW = self.gameBoard.getSquare((x-1),y).getObjectOn()
                    if objectOnW != None:
                        if(objectOnW.getClassName() == "Ship"):
                            if objectOnW.getName() != "MineLayer":
                                return "Cant drop mine at selected location"
                        if(objectOnW.getClassName() != "Ship" and objectOnW.getClassName() != "Mine"):
                            return "Cant drop mine at selected location"
                else:
                    if objectOn == None:
                        return "Mine dropped successful!" 
                    else:
                        return "Cant drop mine at selected location"
            else: 
                return "Cant drop mine at selected location"
        else: 
                return "Cant drop mine at selected location" 


    def dropMineOnBoard(self, mine, position):
        # Add mind to the sqaure object
        x = position[0]
        y = position[1]
        square = self.gameBoard.getSquare(x,y) 
        self.gameBoard.getSquare(x,y).setObjectOn(mine)
        print "MINE DROOPPED AT"

    def removeMine(self, x, y):
        print"Removing mine from board"
        x = x
        y = y
        #square = self.gameBoard.getSquare(x,y).getClassName()
        #print square
        #self.gameBoard.getSquare(x,y).removeObjectOn()
        if self.gameBoard.getSquare(x,y).getObjectOn() != None:
            sq = self.gameBoard.getSquare(x,y).getObjectOn().getClassName()
            print sq
            if sq == "Mine":
                self.gameBoard.getSquare(x,y).removeObjectOn()

    def PickUpMine(self, x, y):
        objectOn = self.gameBoard.getSquare(x,y).getObjectOn()
        if objectOn == None:
            return 1
        elif objectOn.getClassName() == "Mine":
            return 0
        else:
            return 1
    
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
        sonarList = []
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
            
            if (ship.getSubclass() != "MineLayer" and ship.getSubclass() != "Kamikaze"):
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
            elif ship.getSubclass() == "MineLayer":
                l = ship.getPositionList()
                if (ship.getOrientation() == "E"):
                    for x1 in range(l[0][0] - 3, l[1][0] + 4):
                        for y1 in range(l[0][1] - 2, l[0][1] + 3):
                            sonarList.append((x1, y1))
                            radarList.append((x1, y1))
                elif ( ship.getOrientation() == "W"):
                    for x1 in range(l[1][0] - 3, l[0][0] + 4):
                        for y1 in range(l[0][1] - 2, l[0][1] + 3):
                            sonarList.append((x1, y1))
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "N" ):
                    for x1 in range(l[0][0] - 2, l[0][0] + 3):
                        for y1 in range(l[1][1] - 3, l[0][1] + 4):
                            sonarList.append((x1, y1))
                            radarList.append((x1, y1))
                elif (ship.getOrientation() == "S"):
                    for x1 in range(l[0][0] - 2, l[0][0] + 3):
                        for y1 in range(l[0][1] - 3, l[1][1] + 4):
                            sonarList.append((x1, y1))
                            radarList.append((x1, y1))
            elif ship.getSubclass() == "Kamikaze":
                l = ship.getPositionList()
                for x1 in range(l[0][0] - 2, l[0][0] + 3):
                    for y1 in range(l[0][1] - 2, l[0][1] + 3):
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

        for i in range(30):
            for j in range(30):
                if(i,j) in sonarList:
                    self.gameBoard.getSquare(i,j).setSonarVisible(True)
                else:
                    self.gameBoard.getSquare(i,j).setSonarVisible(False)


                # self.gameBoard.getSquare(i,j).setVisible(True)



    def detonateKamikaze(self):
        print "DETONATING..."
        for ship in self.shiplist:
            if ship.isSelected() and ship.getSubclass() == 'Kamikaze':
                print "ship found"
                l = ship.getPositionList()
                
                for (x,y) in l:
                    self.gameBoard.getSquare(x, y).setObjectOn(None)
                    
                detonateZone = []
                
                for x1 in range(l[0][0] - 1, l[0][0] + 2):
                    for y1 in range(l[0][1] - 1, l[0][1] + 2):
                        detonateZone.append((x1, y1))
                
                for (x,y) in detonateZone:
                    print "checking ", (x,y)
                    sq = self.gameBoard.getSquare(x,y)
                    o = sq.getObjectOn()
                    
                    if o == None or o == ship or o.getClassName() == "Coral":
                        continue
                    elif o.getClassName() == "Base":
                        index = o.positionIndex((x,y))
                        health = o.getHealth()
                        #print "INITIAL HEALTH:",health  
                        health[index] = 0
                        sq.setObjectOn(None)    # remove base
                        continue
                    elif o.getClassName() == "Ship":
                        index = o.positionIndex((x,y))
                        armour = o.getArmour()
                        #print armour  # 1 (Normal)  2 (Heavy)
                        health = o.getHealth()
                        #print "INITIAL HEALTH:",health  
                        health[index] = 0
                        if sum(health) == 0:
                            o.destroyShip(self.gameBoard)
                            self.updateVisibility()
                            continue
    
                        o.updateSpeed()                        
                        
                        
                    
                ship.detonate();
                ship.selected = False
                
                
        self.updateVisibility()

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
                            
                            
                