"""
positionList: List<Position>
armour: int[]
rangeX1: int
rangeX2: int
rangeY1: int
rangeY2: int
"""
class Base:
    def __init__(self, positionList, health, color):
        self.color = color
        self.positionList = positionList
        self.health = health
        self.selected = False

    def getClassName(self):
        return "Base"
    
    # Return the list of positions'
    def getPositionList(self):
    	return self.positionList

    # Returns a specific position in the list indicated by the index
    def getPosition(self, index):
    	return self.positionList[index]
 
    def getColor(self):
        return self.color

    # Return the health list of int's
    def getHealth(self):
    	return self.health

    # Returns a specific integer in the health list
    def getArmourIndex(self, index):
    	return self.armour[index]

    def getRadarRangeX1(self):
    	return self.rangeX1

    def getRadarRangeX2(self):
    	return self.rangeX2

    def getRadarRangeY1(self):
    	return self.rangeY1

    def getRadarRangeY2(self):
    	return self.rangeY2

    def positionIndex(self, (x,y)):
        if (x,y) in self.positionList:
            return self.positionList.index((x,y));
        else:
            return -1

    # Set the positionList to be a new list
    def setPositionList(self, newposlist):
    	self.positionList = newposlist

    # Set a position in the positionList indicated by an index
    def setPosition(self, newpos, newindex):
    	self.positionList[newindex] = newpos

    # Set a health specified by the index
    def setArmourIndex(self, index, newhealth):
    	self.armour[index] = newhealth

    def isSelected(self):
        return self.selected;
    
    def setSelected(self, var):
        self.selected = var  
"""
# Test
b = Base([(1,2), (3,4)], [2,3,4,5], 1,2,3,4)
print b.getPositionList()
newposlist = [(5,6), (7,8)]
b.setPositionList(newposlist)
print b.getPositionList()
print b.getPosition(1)
b.setPosition((3,4), 1)
print b.getPosition(1)
print b.getArmour()
print b.getArmourIndex(0)
b.setArmourIndex(0, 8)
print b.getArmour()
"""