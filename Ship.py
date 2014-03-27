"""
positionList: List<Position>
orientation: NSEW
speed: int
totalHealth: int
armour: int[]
x1Range: int
x2Range: int
y1Range: int
y2Range: int
weaponList: ArrayList<Weapon>
"""

class Ship(object):
    def __init__(self, size, position, orientation, color, weapon, radarX):
        self.radarX = radarX
        self.size = size
        self.position = position
        self.orientation = orientation
        self.selected = False
        self.color = color
        self.weapon = weapon
        
    def getRadarX(self):
        return self.radarX

    def getWeaponList(self):
        return self.weapon
    
    def getWeapon(self, type):
        for w in self.weapon:
            if w.getClass() == type:
                return w

    def getCannonRange(self):
        #print self.getWeapon("cannon")
        ranges = (self.getWeapon("cannon").getRangeX(), self.getWeapon("cannon").getRangeY())
        rlist = []
        
        x = (ranges[0] - self.getSize()) / 2
        y = (ranges[1] - 1) / 2 
        ##print str(xRange) + str(yRange)
        p = self.getPositionList()


        if (self.getOrientation() == "E"):  # check using tail
            for i in range(p[-1][0] - x, p[0][0] + x + 1):
                for j in range(p[0][1] - y, p[0][1] + y + 1):
                    if i >= 0 and i <= 29 and j >= 0 and j <= 29:
                        rlist.append((i, j))
    
        elif (self.getOrientation() == "W"): # check using head
            for i in range(p[0][0] - x, p[-1][0] + x + 1):
                for j in range(p[0][1] - y, p[0][1] + y + 1):
                    if i >= 0 and i <= 29 and j >= 0 and j <= 29:
                        rlist.append((i, j))    
        elif (self.getOrientation() == "N"): # check using head
            for i in range(p[-1][0] - y, p[0][0] + y + 1):
                for j in range(p[0][1] - x, p[0][1] + x + 1):
                    if i >= 0 and i <= 29 and j >= 0 and j <= 29:
                        rlist.append((i, j))      
        elif (self.getOrientation() == "S"): # check using tail
            for i in range(p[0][0] - y, p[-1][0] + y + 1):
                for j in range(p[0][1] - x, p[0][1] + x + 1):
                    if i >= 0 and i <= 29 and j >= 0 and j <= 29:
                        rlist.append((i, j))  
                
        return rlist


    def getHeavyCannonRange(self):
        #print self.getWeapon("heavycannon")
        ranges = (self.getWeapon("heavycannon").getRangeX(), self.getWeapon("heavycannon").getRangeY())
        rlist = []
        
        x = (ranges[0] - self.getSize()) / 2
        y = (ranges[1] - 1) / 2 
        ##print str(xRange) + str(yRange)
        p = self.getPositionList()


        if (self.getOrientation() == "E"):  # check using tail
            for i in range(p[-1][0] - x, p[0][0] + x + 1):
                for j in range(p[0][1] - y, p[0][1] + y + 1):
                    if i >= 0 and i <= 29 and j >= 0 and j <= 29:
                        rlist.append((i, j))      
        elif (self.getOrientation() == "W"): # check using head
            for i in range(p[0][0] - x, p[-1][0] + x + 1):
                for j in range(p[0][1] - y, p[0][1] + y + 1):
                    if i >= 0 and i <= 29 and j >= 0 and j <= 29:
                        rlist.append((i, j))      
        elif (self.getOrientation() == "N"): # check using head
            for i in range(p[-1][0] - y, p[0][0] + y + 1):
                for j in range(p[0][1] - x, p[0][1] + x + 1):
                    if i >= 0 and i <= 29 and j >= 0 and j <= 29:
                        rlist.append((i, j))      
        elif (self.getOrientation() == "S"): # check using tail
            for i in range(p[0][0] - y, p[-1][0] + y + 1):
                for j in range(p[0][1] - x, p[0][1] + x + 1):
                    if i >= 0 and i <= 29 and j >= 0 and j <= 29:
                        rlist.append((i, j))  
                
        return rlist

    def getTorpedoRange(self):
        #print self.getWeapon("torpedo")
        ranges = (self.getWeapon("torpedo").getRangeX(), self.getWeapon("torpedo").getRangeY())
        rlist = []
        rangeten = ranges[0]
        pList = self.getPositionList()
        (x1, y1) = pList[0] # head

        tempx = x1
        xLimitRight = x1 + rangeten
        xLimitLeft = x1 - rangeten
        tempy = y1
        yLimitDown = y1 + rangeten
        yLimitUp = y1 - rangeten

        if (self.getOrientation() == "E"):
            while (tempx + 1 <= xLimitRight):
                if tempx+1 >=0 and tempx+1<=29 and y1>=0 and y1<=29:
                    rlist.append((tempx + 1, y1))
                tempx = tempx + 1

        elif (self.getOrientation() == "W"):
            while (tempx - 1 >= xLimitLeft):
                if tempx-1 >=0 and tempx-1<=29 and y1>=0 and y1<=29:
                    rlist.append((tempx - 1, y1))
                tempx = tempx - 1

        elif (self.getOrientation() == "S"):
            while (tempy + 1 <= yLimitDown):
                if x1 >=0 and x1<=29 and tempy+1>=0 and tempy+1<=29:
                    rlist.append((x1 , tempy + 1))
                tempy = tempy + 1
        elif (self.getOrientation() == "N"):
            while (tempy - 1 >= yLimitUp):
                if x1 >=0 and x1<=29 and tempy-1>=0 and tempy-1<=29:
                    rlist.append((x1 , tempy - 1))
                tempy = tempy - 1

        return rlist   

    def getSize(self):
        return self.size;
    
    def isSelected(self):
        return self.selected;
    
    def setSelected(self, var):
        self.selected = var
        
    def getPositionList(self):
        return self.position;

    def getPositionBetween(self, x, y):
        coordinates = []
        if (self.orientation == "E"):
            (hx,hy) = self.position[0]  # head index
            tempx = hx + 1
            while (tempx <= x):
                coordinates.append((tempx,y))
                tempx = tempx + 1
        elif (self.orientation == "W"):
            (hx,hy) = self.position[0]  # head index
            tempx = hx - 1
            while (tempx >= x):
                coordinates.append((tempx,y))
                tempx = tempx - 1
        elif (self.orientation == "N"):
            (hx,hy) = self.position[0]  # head index
            tempy = hy - 1
            while (tempy >= y):
                coordinates.append((x,tempy))
                tempy = tempy - 1        
        elif (self.orientation == "S"):
            (hx,hy) = self.position[0]  # head index
            tempy = hy + 1
            while (tempy <= y):
                coordinates.append((x,tempy))
                tempy = tempy + 1           
        return coordinates

    def setPositionList(self, list):
        self.position = []
        self.position = list
    
    def positionIndex(self, (x,y)):
        if (x,y) in self.position:
            return self.position.index((x,y));
        else:
            return -1
        
    def setOrientation(self, new):
        self.orientation = new
    
    def getOrientation(self):
        return self.orientation;
    
    def getColor(self):
        return self.color

    def getTurnRadius(self):
        return self.turnRadius
    
    def updateSpeed(self): 
        if (self.name == 'cruiser'):
            self.speed = self.size * 2 - self.health.count(0) * 2
        
        if (self.name == 'mine'):
            self.speed = self.size * 3/2 - self.health.count(0) * 3/2

        if (self.name == 'destroyer'):
            self.speed = sum(self.health) * 2

        if (self.name == 'torpedo'):
            self.speed = sum(self.health) * 3
            
        if (self.name =='radar'):
            self.speed = sum(self.health)
    
    def rotateClockwise(self, rotation):
        newpos = []
            
        while (rotation > 0):
            if self.orientation == "N":
                var = self.size - 1
                for (x,y) in self.position:
                    x = x + var
                    y = y + var
                    newpos.append((x,y)) 
                    var = var - 1
                        
                rotation = rotation - 1
                self.orientation = "E"
                    
            elif self.orientation == "E":
                var = self.size - 1
                for (x,y) in self.position:
                    x = x - var
                    y = y + var
                    newpos.append((x,y))
                    var = var - 1 
                rotation = rotation - 1
                self.orientation = "S"
                    
            elif self.orientation == "S":
                var = self.size - 1
                for (x,y) in self.position:
                    x = x - var
                    y = y - var
                    newpos.append((x,y))
                    var = var - 1 
                rotation = rotation - 1
                self.orientation = "W"
                    
            elif self.orientation == "W":
                var = self.size - 1
                for (x,y) in self.position:
                    x = x + var
                    y = y + var
                    newpos.append((x,y))
                    var = var - 1 
                rotation = rotation - 1
                self.orientation = "N"
        #print newpos    
        return newpos

    def rotateClockwiseEnd(self, rotation):
        newpos = []
        end = self.position[-1]
        #print 'end = ',end
        #print self.orientation
        #print self.orientation == "E"
        while (rotation > 0):
            newpos = []
            if self.orientation == "N":
                var = self.size - 1
                for (x,y) in self.position:
                    # #print 'old ',(x,y)
                    y = end[1]
                    x = end[0]+var
                    var-=1
                    newpos.append((x,y))
                    # #print'new',(x,y)        
                rotation = rotation - 1
                self.orientation = "E"
                    
            elif self.orientation == "E":
                #print 'heyo'
                var = self.size - 1
                for (x,y) in self.position:
                    x = end[0]
                    y = end[1]+var
                    #print x,y
                    newpos.append((x,y))
                    var -= 1 
                rotation = rotation - 1
                self.orientation = "S"

                    
            elif self.orientation == "S":
                var = self.size - 1
                for (x,y) in self.position:
                    x = end[0] - var
                    y = end[1]
                    newpos.append((x,y))
                    var -= 1 
                rotation = rotation - 1
                self.orientation = "W"
                    
            elif self.orientation == "W":
                var = self.size - 1

                for (x,y) in self.position:
                    x = end[0]
                    y = end[1] - var
                    newpos.append((x,y))
                    var -= 1 
                rotation = rotation - 1
                self.orientation = "N"
        #print 'oldpos ', self.position    

        self.position = []
        self.position = newpos
        #print 'newpos ',newpos
        #print 'positionlist', self.position
        return newpos  

    # only works for ship of size 3
    def rotateClockwiseCenter(self, rotation):
        newpos = []

        middle = self.position[1]
        #print 'middle = ',middle
        #print rotation
        # rotation = 2
        while (rotation > 0):
            newpos = []
            if self.orientation == "N":
                var = 1
                for (x,y) in self.position:
                    #print 'old ',(x,y)
                    x = middle[0]+var
                    y = middle[1]
                    var-=1
                    newpos.append((x,y))
                    #print'new',(x,y)        
                rotation = rotation - 1
                self.orientation = "E"
                    
            elif self.orientation == "E":
                var = 1
                #print self.position
                for (x,y) in self.position:
                    # #print (x,y)
                    x = middle[0]
                    y = middle[1]+var
                    newpos.append((x,y))
                    var -= 1 
                rotation = rotation - 1
                self.orientation = "S"
                    
            elif self.orientation == "S":
                var = 1
                for (x,y) in self.position:
                    #print (x,y)
                    x = middle[0] - var
                    y = middle[1]
                    #print (x,y)
                    newpos.append((x,y))
                    var -= 1 
                rotation = rotation - 1
                self.orientation = "W"
                    
            elif self.orientation == "W":
                var = 1

                for (x,y) in self.position:
                    x = middle[0]
                    y = middle[1] - var
                    newpos.append((x,y))
                    var -= 1 
                rotation = rotation - 1
                self.orientation = "N"
        #print 'oldpos ', self.position    

        self.position = []
        self.position = newpos
        #print 'newpos ',newpos
        return newpos

    def getTurnZone(self, rotation):
        tzone = []
        p = self.position
        
        if (self.orientation == "E"):
            if (self.getTurnRadius() == 2):
                if (rotation == 3): # rotating counterclockwise
                    endpos = p[-1]
                    midpos = p[1]
                    ##print "ENDPOS IS: ", endpos
                    ##print "MIDDLE POS IS: ", midpos
                    tzone.append((p[-1][0], p[-1][1] + 1))  # gets the left bottom square 
                    tzone.append((p[1][0], p[1][1] - 1 ))   # gets the middle 2 squares
                    tzone.append((p[1][0], p[1][1] + 1))
                    tzone.append((p[0][0], p[0][1] - 1))    # gets the upper right square
                    ##print "TESTING THE SQUARES ARE AHH!: ", tzone
                if (rotation == 1): # rotating clockwise
                    endpos = p[-1]
                    midpos = p[1]
                    #print "ENDPOS IS: ", endpos
                    #print "MIDDLE POS IS: ", midpos
                    tzone.append((p[-1][0], p[-1][1] - 1))  # gets the upper left square 
                    tzone.append((p[1][0], p[1][1] - 1 ))   # gets the middle 2 squares
                    tzone.append((p[1][0], p[1][1] + 1))
                    tzone.append((p[0][0], p[0][1] + 1))    # gets the bottom right square
                    #print "THE SQUARES ARE: ", tzone
            else:
                if rotation == 1:
                    y = p[-1][1] + 1
                    s = self.getSize() 
                    while (s > 1):
                        for x in range(p[-1][0], p[-1][0] + s):
                            tzone.append((x,y))
                        y += 1
                        s -= 1
                #add 
                if rotation == 3:
                    y = p[-1][1] - 1
                    s = self.getSize() 
                    while (s > 1):
                        for x in range(p[-1][0], p[-1][0] + s):
                            tzone.append((x,y))
                        y -= 1
                        s -= 1
        if (self.orientation == "S"):
            if (self.getTurnRadius() == 2):
                if (rotation == 3): # rotating counterclockwise
                    endpos = p[-1]
                    midpos = p[1]
                    #print "ENDPOS IS: ", endpos
                    #print "MIDDLE POS IS: ", midpos
                    tzone.append((p[-1][0] - 1, p[-1][1])) # gets the left upper square 
                    tzone.append((p[1][0] + 1, p[1][1]))   # gets the middle 2 squares
                    tzone.append((p[1][0] - 1, p[1][1]))
                    tzone.append((p[0][0] + 1, p[0][1]))   # gets the bottom right square
                    #print "THE SQUARES ARE: ", tzone
                if (rotation == 1): # rotating clockwise
                    endpos = p[-1]
                    midpos = p[1]
                    #print "ENDPOS IS: ", endpos
                    #print "MIDDLE POS IS: ", midpos
                    tzone.append((p[-1][0] + 1, p[-1][1]))  # gets the upper right square 
                    tzone.append((p[1][0] + 1, p[1][1]))   # gets the middle 2 squares
                    tzone.append((p[1][0] - 1, p[1][1]))
                    tzone.append((p[0][0] - 1, p[0][1]))    # gets the bottom left square
                    #print "THE SQUARES ARE: ", tzone
            else:
                if rotation == 1:
                    y = p[-1][1]
                    s = self.getSize()
                    for x in range(p[-1][0] + 1 - s, p[-1][0] + 1):
                        tzone.append((x,y))
                        
                    y += 1
                    while (s > 1):
                        for x in range(p[-1][0] + 1 - s, p[-1][0] + 1):
                            tzone.append((x,y))
                        y += 1
                        s -= 1        
                if rotation == 3:
                    y = p[-1][1]
                    s = self.getSize()
                    
                    for x in range(p[-1][0], p[-1][0] + s):
                        tzone.append((x,y))
                    
                    y += 1
                    while (s > 1):
                        for x in range(p[-1][0], p[-1][0] + s):
                            tzone.append((x,y))
                        y += 1
                        s -= 1
        if (self.orientation == "N"):
            if (self.getTurnRadius() == 2):
                if (rotation == 3): # rotating counterclockwise
                    endpos = p[-1]
                    midpos = p[1]
                    #print "ENDPOS IS: ", endpos
                    #print "MIDDLE POS IS: ", midpos
                    tzone.append((p[-1][0] + 1, p[-1][1])) # gets the right bottom square 
                    tzone.append((p[1][0] + 1, p[1][1]))   # gets the middle 2 squares
                    tzone.append((p[1][0] - 1, p[1][1]))
                    tzone.append((p[0][0] - 1, p[0][1]))   # gets the upper left square
                    #print "THE SQUARES ARE: ", tzone
                if (rotation == 1): # rotating clockwise
                    endpos = p[-1]
                    midpos = p[1]
                    #print "ENDPOS IS: ", endpos
                    #print "MIDDLE POS IS: ", midpos
                    tzone.append((p[-1][0] - 1, p[-1][1]))  # gets the upper right square 
                    tzone.append((p[1][0] + 1, p[1][1]))   # gets the middle 2 squares
                    tzone.append((p[1][0] - 1, p[1][1]))
                    tzone.append((p[0][0] + 1, p[0][1]))    # gets the bottom left square
                    #print "THE SQUARES ARE: ", tzone
            else:              
                if rotation == 1:
                    y = p[-1][1]
                    s = self.getSize()
                    for x in range(p[-1][0], p[-1][0] + s):
                        tzone.append((x,y))
                    y -= 1
                    while (s > 1):
                        for x in range(p[-1][0], p[-1][0] + s):
                            tzone.append((x,y))
                        y -= 1
                        s -= 1 
                if rotation == 3:
                    y = p[-1][1] 
                    s = self.getSize()
                    for x in range(p[-1][0] + 1 - s, p[-1][0] + 1):
                        tzone.append((x,y))
                    y -= 1
                    while (s > 1):
                        for x in range(p[-1][0] + 1 - s, p[-1][0] + 1):
                            tzone.append((x,y))
                        y -= 1
                        s -= 1 
                        
        if (self.orientation == "W"):
            if (self.getTurnRadius() == 2):
                if (rotation == 3): # rotating counterclockwise
                    endpos = p[-1]
                    midpos = p[1]
                    #print "ENDPOS IS: ", endpos
                    #print "MIDDLE POS IS: ", midpos
                    tzone.append((p[-1][0], p[-1][1] - 1))  # gets the upper right square 
                    tzone.append((p[1][0], p[1][1] - 1 ))   # gets the middle 2 squares
                    tzone.append((p[1][0], p[1][1] + 1))
                    tzone.append((p[0][0], p[0][1] + 1 ))    # gets the bottom right square
                    #print "THE SQUARES ARE: ", tzone
                if (rotation == 1): # rotating clockwise
                    endpos = p[-1]
                    midpos = p[1]
                    #print "ENDPOS IS: ", endpos
                    #print "MIDDLE POS IS: ", midpos
                    tzone.append((p[-1][0], p[-1][1] + 1))  # gets the right bottom square 
                    tzone.append((p[1][0], p[1][1] - 1 ))   # gets the middle 2 squares
                    tzone.append((p[1][0], p[1][1] + 1))
                    tzone.append((p[0][0], p[0][1] - 1))    # gets the upper left square
                    #print "THE SQUARES ARE: ", tzone                    
            else:
                if rotation == 1:
                    y = p[-1][1] - 1
                    s = self.getSize()
                    while (s > 1):
                        for x in range(p[-1][0] + 1 - s, p[-1][0] + 1):
                            tzone.append((x,y))
                        y -= 1
                        s -= 1 
                if rotation == 3:
                    y = p[-1][1] + 1
                    s = self.getSize()
                    while (s > 1):
                        for x in range(p[-1][0] + 1 - s, p[-1][0] + 1):
                            tzone.append((x,y))
                        y += 1
                        s -= 1
            
        return tzone
                 
    
    def move(self, x, y):
        #positive displace = moving forward
        #negative displacement = moving backward
        (x1, y1) = self.position[0]
        #print x, y
        #print x1, y1
        dx = x - x1
        dy = y - y1
        #print dx, dy
        
        
        #print self.position
        newpos = []
        for (x,y) in self.position:
            y = y + dy
            x = x + dx
            newpos.append((x,y))
        self.position = []
        self.position = newpos
        #print newpos

    def destroyShip(self, board):
        print "DESTROY SHIP"
        for (x,y) in self.position:
            sq = board.getSquare(x,y)
            sq.setObjectOn(None)
        
    def getClassName(self):
        return "Ship"

class Cruiser(Ship):
    def __init__(self, position, orientation, color, weapon):
        Ship.__init__(self, 5, position, orientation, color, weapon, 10)
        self.health = [2,2,2,2,2]
        self.speed = sum(self.health)
        self.armour = 2   
        self.mines = 0
        self.turnRadius = 1  
        self.name = 'cruiser'      
    def getSubclass(self):
        return "Cruiser"
    def getSpeed(self):
        return self.speed

    def getArmour(self):
        return self.armour

    def getHealth(self):
        return self.health

    # Gets the class name
    def getName(self):
        return self.__class__.__name__

class Destroyer(Ship):
    def __init__(self, position, orientation, color, weapon):
        Ship.__init__(self, 4, position, orientation, color, weapon, 8)
        self.armour = 1
        self.health = [1,1,1,1]
        self.speed = sum(self.health) * 2
        self.mines = 0
        self.turnRadius = 1
        self.name = 'destroyer'        
        
    def getSubclass(self):
        return "Destroyer"
    
    def getSpeed(self):
        return self.speed

    def getArmour(self):
        return self.armour

    def getHealth(self):
        return self.health

    # Gets the class name
    def getName(self):
        return self.__class__.__name__

class TorpedoBoat(Ship):
    def __init__(self, position, orientation, color, weapon):
        Ship.__init__(self, 3, position, orientation, color, weapon, 6)
        self.armour = 1
        self.health = [1,1,1]
        self.speed = sum(self.health) * 3
        self.mines = 0
        self.turnRadius = 2
        self.name = 'torpedo'        
        
    def getSubclass(self):
        return "TorpedoBoat"
    
    def getSpeed(self):
        return self.speed

    def getArmour(self):
        return self.armour

    def getHealth(self):
        return self.health

    # Gets the class name
    def getName(self):
        return self.__class__.__name__
    
class RadarBoat(Ship):
    def __init__(self, position, orientation, color, weapon):
        Ship.__init__(self, 3, position, orientation, color, weapon, 6)
        self.longRadarX = 12
        self.armour = 1
        self.health = [1,1,1]
        self.speed = sum(self.health)
        self.mines = 0
        self.turnRadius = 2
        self.name ='radar'
        
    def getSubclass(self):
        return "RadarBoat"
    
    def getSpeed(self):
        return self.speed

    def getArmour(self):
        return self.armour

    def getHealth(self):
        return self.health

    # Gets the class name
    def getName(self):
        return self.__class__.__name__
    
class MineLayer(Ship):
    def __init__(self, position, orientation, color, weapon):
        Ship.__init__(self, 2, position, orientation, color, weapon, 6)
        self.armour = 2
        self.health = [2,2]
        self.speed = sum(self.health)*3/2
        self.mines = 5
        self.turnRadius = 1
        self.name = 'mine'        
        
    def getSubclass(self):
        return "MineLayer"
    def getSpeed(self):
        return self.speed

    def getArmour(self):
        return self.armour

    def getHealth(self):
        return self.health

    # Gets the class name
    def getName(self):
        return self.__class__.__name__
    
    def getMineCount(self):
        return self.mines

    def decreaseMineCount(self):
        self.mines = self.mines - 1

    def increaseMineCount(self):
        self.mines = self.mines + 1	
"""
# Testing MineLayer
a = MineLayer(8,'W', 8,10,2,1,2,3,4,9,5)
"""