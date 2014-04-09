from Base import Base
from Ship import Cruiser, Destroyer, RadarBoat, TorpedoBoat, MineLayer, Kamikaze
from Weapon import Cannon, HeavyCannon, Torpedo, Explosive
import pygame

WHITE = (255, 255, 255)     # WHITE          
#ENEMY = (255,0,0)           # RED
ENEMY = (76,0,153)          # PURPLE
HIGHLIGHT = (250,250,155)   # YELLOW
d = 85

class PlayerState(object):
    def __init__(self, playerType,user):
        self.username = user
        self.shipList = []


        # boolean to identify the player
        self.you = playerType
        hc = HeavyCannon(2, 15, 11)
        dc = Cannon(2, 12, 9)
        dt = Torpedo(2, 10, 10)
        rc = Cannon(2, 5, 3)
        tc = Cannon(2, 5, 5)
        tt = Torpedo(2, 10, 10)
        mc = Cannon(2, 4, 5)
        ex = Explosive(2,3,3)


        if (self.you):
            self.color = WHITE
            self.base = Base([(0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19)], [2,2,2,2,2,2,2,2,2,2], self.color)
            s1 = Cruiser([(5,10),(4,10),(3,10),(2,10),(1,10)], "E", self.color, [hc]) 
            s2 = Cruiser([(5,11),(4,11),(3,11),(2,11),(1,11)], "E", self.color, [hc])
            s3 = Destroyer([(4,12),(3,12),(2,12),(1,12)], "E", self.color, [dc, dt])
            s4 = Destroyer([(4,13),(3,13),(2,13),(1,13)], "E", self.color, [dc, dt])
            s5 = Destroyer([(4,14),(3,14),(2,14),(1,14)], "E", self.color, [dc, dt])
            s6 = RadarBoat([(3,15),(2,15),(1,15)], "E", self.color, [rc])
            s7 = TorpedoBoat([(3,16),(2,16),(1,16)], "E", self.color, [tc, tt])
            s8 = TorpedoBoat([(3,17),(2,17),(1,17)], "E", self.color, [tc, tt])
            s9 = MineLayer([(2,18),(1,18)], "E", self.color, [mc])
            s10 = MineLayer([(2,19),(1,19)], "E", self.color, [mc]) 
            s11 = Kamikaze([(1,20)], "E", self.color, [ex]) 

        else:
            self.color = ENEMY
            self.base = Base([(29, 10), (29, 11), (29, 12), (29, 13), (29, 14), (29, 15), (29, 16), (29, 17), (29, 18), (29, 19)], [2,2,2,2,2,2,2,2,2,2], self.color)
            s1 = Cruiser([(24,10),(25,10),(26,10),(27,10),(28,10)], "W", self.color, [hc])
            s2 = Cruiser([(24,11),(25,11),(26,11),(27,11),(28,11)], "W", self.color, [hc]) 
            s3 = Destroyer([(25,12),(26,12),(27,12),(28,12)], "W", self.color, [dc, dt])
            s4 = Destroyer([(25,13),(26,13),(27,13),(28,13)], "W", self.color, [dc, dt])
            s5 = Destroyer([(25,14),(26,14),(27,14),(28,14)], "W", self.color, [dc, dt])
            s6 = RadarBoat([(26,15),(27,15),(28,15)], "W", self.color, [rc])
            s7 = TorpedoBoat([(26,16),(27,16),(28,16)], "W", self.color, [tc, tt])
            s8 = TorpedoBoat([(26,17),(27,17),(28,17)], "W", self.color, [tc, tt])
            s9 = MineLayer([(27,18),(28,18)], "W", self.color, [mc])
            s10 = MineLayer([(27,19),(28,19)], "W", self.color, [mc]) 
            s11 = Kamikaze([(28,20)], "E", self.color, [ex]) 


        # self.shipList = [s3,s4]
        self.shipList = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11]


    def getUsername(self):
        return self.username
    def setUsername(self,var):
        self.username = var

    def getShipList(self):
        return self.shipList

    def getShipIndex(self, index):
        return self.shipList[index]

    def appendShip(self, aship):
        self.shipList.append(aship)

    def getBase(self):
        return self.base

"""
player1 = PlayerState('Tom', True)
player2 = PlayerState('Mary', False)
player1.paintBase('surface')
player2.paintBase('surface')
"""