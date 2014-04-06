import pygame
from Square import Square
from Coral import Coral

DARKSEA = (62, 100, 201)
LIGHTSEA = (68, 144, 219)

DARKSEA = (12, 90, 168)
LIGHTSEA = (22, 130, 240)
CORAL = (242, 186, 111)
WHITE = (255,255,255)
RED = (250, 0, 0)
ORANGE = (255,128,0)
SELECTED = (250, 250, 215)
GREEN = (190, 252, 187)
YELLOW = (247, 255, 94)

#?
DARKGREEN = (102,102,0)
#?
BROWN = (51,0,25)


d = 85

clock = pygame.time.Clock()
fps = clock.tick(30) / 1000.0
        
class Board:
    def __init__(self, coral):
        
        self.x = -1
        self.y = -1 

        self.tick = 0



        self.board = []
        for x in range(30):
            row = []
            for y in range(30):
                if x >= 10 and x<= 20 and y >= 3 and y < 27: #if inside coral zone
                    if (x,y) in coral:  
                        c = Coral()
                        sq = Square(c, (x,y))
                        row.append(sq)
                    else:
                        sq = Square(None, (x,y))
                        row.append(sq)
                else:
                    sq = Square(None, (x,y))
                    row.append(sq)
            self.board.append(row)

    def getBoard(self):
        return self.board

    def getSquare(self, x, y):
        return self.board[x][y]
    
    def setSquare(self,x,y,sq):
        self.board[x][y] = sq
    

    def animate(self,surface,t):

        self.tick = t
        for x in range(30):
            for y in range(30):
                obj = self.board[x][y].getObjectOn()
                vis = self.board[x][y].isVisible()
                aRange = self.board[x][y].isActiveRange()
                #drawing initial board with sea and coral
                if (obj == None):
                    if (aRange):
                        pygame.draw.rect(surface, GREEN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    elif (vis):
                        if self.tick == 0:
                            # print 'w1'
                            surface.blit(pygame.image.load('images/water1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            # print 'w2'
                            surface.blit(pygame.image.load('images/water2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, LIGHTSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if self.tick == 0:
                            surface.blit(pygame.image.load('images/darkwater1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(pygame.image.load('images/darkwater2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, DARKSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                      
                elif (obj.getClassName() == "Coral"):
                    if self.tick == 0:
                            # print 'w1'
                        surface.blit(pygame.image.load('images/coral1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                    else:
                        surface.blit(pygame.image.load('images/coral2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))

                
                elif (obj.getClassName() != "Coral"):
                    if (aRange):
                        pygame.draw.rect(surface,GREEN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    elif (vis and not aRange):
                        if self.tick == 0:
                            surface.blit(pygame.image.load('images/water1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(pygame.image.load('images/water2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, LIGHTSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if self.tick == 0:
                            surface.blit(pygame.image.load('images/darkwater1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(pygame.image.load('images/darkwater2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))


    def setNot(self,x,y,surface):
        self.x = x
        self.y = y

    def paint(self, surface):
        # print (pygame.time.get_ticks()/500)%2

        for x in range(30):
            for y in range(30):
                obj = self.board[x][y].getObjectOn()
                vis = self.board[x][y].isVisible()
                aRange = self.board[x][y].isActiveRange()
                sonarVisibility = self.board[x][y].isSonarVisible()
                #drawing initial board with sea and coral
                if (obj == None):
                    if (aRange):
                        pygame.draw.rect(surface, GREEN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    elif (vis):
                        if self.tick == 0:
                            surface.blit(pygame.image.load('images/water1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(pygame.image.load('images/water2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, LIGHTSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if self.tick == 0:
                            surface.blit(pygame.image.load('images/darkwater1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(pygame.image.load('images/darkwater2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))


                elif (obj.getClassName() == "Coral"):
                    if self.tick == 0:
                            # print 'w1'
                        surface.blit(pygame.image.load('images/coral1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                    else:
                        surface.blit(pygame.image.load('images/coral2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))

                
                elif (obj.getClassName() != "Coral"):
                    if (aRange):
                        pygame.draw.rect(surface,GREEN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    elif (vis and not aRange):
                        if self.tick == 0:
                            surface.blit(pygame.image.load('images/water1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(pygame.image.load('images/water2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, LIGHTSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if self.tick == 0:
                            surface.blit(pygame.image.load('images/darkwater1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(pygame.image.load('images/darkwater2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))

                if (sonarVisibility):
                    if(obj == None):
                        surface.blit(pygame.image.load('images/radar.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                    elif(obj.getClassName() == "Mine"):
                        #print "MINE"
                        if self.tick == 0:
                            surface.blit(pygame.image.load('images/mine1.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(pygame.image.load('images/mine2.png').convert(),(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        

                #drawing the ships
                if (obj != None and obj.getClassName() == "Ship" and vis):
                    if (obj.isSelected()):
                        c = SELECTED        # YELLOW
                    else:
                        c = obj.getColor()  # WHITE

                    if obj.getColor() == (255,255,255) :
                        player1=True
                    else:
                        player1=False
                        
                    if (obj.positionIndex((x,y)) == 0 and obj.getSubclass() != "Kamikaze"):
                        if (obj.getOrientation() == "E"):
                            if (obj.isSelected()):
                                surface.blit(pygame.image.load('images/FEs.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                            elif (obj.getHealth()[0] <= 0):
                                # pygame.draw.polygon(surface, RED, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d+20-1, y*20 + y*1 + 20)], 0)
                                surface.blit(pygame.image.load('images/FEDe.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                            elif (obj.getHealth()[0] == 1 and obj.getArmour() == 2):
                                # pygame.draw.polygon(surface, ORANGE, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d+20-1, y*20 + y*1 + 20)], 0)
                                surface.blit(pygame.image.load('images/FED.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                            else:
                                if player1:
                                    surface.blit(pygame.image.load('images/FE.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                                else:
                                    surface.blit(pygame.image.load('images/P2FE.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

        
                                # pygame.draw.polygon(surface, c, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d+20-1, y*20 + y*1 + 20)], 0)
                        elif (obj.getOrientation() == "S"):
                            if (obj.isSelected()):
                                surface.blit(pygame.image.load('images/FSs.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                            elif (obj.getHealth()[0] <= 0):
                                surface.blit(pygame.image.load('images/FSDe.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                                # pygame.draw.polygon(surface, RED, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 10, y*20 + y*1 + 29)], 0)
                            elif (obj.getHealth()[0] == 1 and obj.getArmour() == 2):
                                surface.blit(pygame.image.load('images/FSD.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                                # pygame.draw.polygon(surface, ORANGE, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 10, y*20 + y*1 + 29)], 0)
                            else:
                                if player1:    
                                    surface.blit(pygame.image.load('images/P1FS.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                                else:
                                    surface.blit(pygame.image.load('images/P2FS.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                                # pygame.draw.polygon(surface, c, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 10, y*20 + y*1 + 29)], 0)
                        elif obj.orientation == "W":
                            if (obj.isSelected()):
                                surface.blit(pygame.image.load('images/FWs.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                            elif (obj.getHealth()[0] <= 0):                            
                                surface.blit(pygame.image.load('images/FWDe.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                                # pygame.draw.polygon(surface, RED, [(x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 29), (x*20 + x*1 + d, y*20 + y*1 + 20)], 0)
                            elif (obj.getHealth()[0] == 1 and obj.getArmour() == 2):
                                surface.blit(pygame.image.load('images/FWD.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                                # pygame.draw.polygon(surface, ORANGE, [(x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 29), (x*20 + x*1 + d, y*20 + y*1 + 20)], 0)
                            else:
                                if player1:
                                    surface.blit(pygame.image.load('images/FW.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                                else:
                                    surface.blit(pygame.image.load('images/P2Fw.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                                # pygame.draw.polygon(surface, c, [(x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 29), (x*20 + x*1 + d, y*20 + y*1 + 20)], 0)
                        
                        elif obj.orientation == "N":
                            if (obj.isSelected()):
                                surface.blit(pygame.image.load('images/FNs.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                            elif (obj.getHealth()[0] <= 0):                            
                                surface.blit(pygame.image.load('images/FNDe.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                            elif (obj.getHealth()[0] == 1 and obj.getArmour() == 2):
                                surface.blit(pygame.image.load('images/FND.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                            else:
                                if player1:
                                    surface.blit(pygame.image.load('images/NS.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))
                                else:
                                    surface.blit(pygame.image.load('images/P2FN.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                        else:
                            pygame.draw.rect(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if (obj.getOrientation() == "E" or obj.getOrientation() == "W"):
                            if(obj.isSelected()):
                                surface.blit(pygame.image.load('images/EWs.png').convert(),(x*20 + x*1 + d-1, y*20 + y*1 + 10))

                            #?
                            elif (obj.getName() == "RadarBoat" and obj.positionIndex((x,y)) == 1): # This is where the middle part of te boat is at
                                pygame.draw.rect(surface, BROWN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 21])
                                if (obj.getHealth()[obj.positionIndex((x,y))] <= 0):
                                    pygame.draw.rect(surface, RED, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])


                            elif (obj.getHealth()[obj.positionIndex((x,y))] <= 0):
                                surface.blit(pygame.image.load('images/EWDe.png').convert(),(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                                # pygame.draw.rect(surface, RED, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                            elif (obj.getHealth()[obj.positionIndex((x,y))] == 1 and obj.getArmour() == 2):
                                surface.blit(pygame.image.load('images/EWD.png').convert(),(x*20 + x*1 + d-1, y*20 + y*1 + 10))

                                # pygame.draw.rect(surface, ORANGE, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                            else:
                                if player1:
                                    surface.blit(pygame.image.load('images/EW.png').convert(),(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                                else:
                                    surface.blit(pygame.image.load('images/P2EW.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))


                        else:
                            if(obj.isSelected()):
                                surface.blit(pygame.image.load('images/NSs.png').convert(),(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                            
                            elif (obj.getName() == "RadarBoat" and obj.positionIndex((x,y)) == 1):
                                pygame.draw.rect(surface, BROWN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 21])
                                if (obj.getHealth()[obj.positionIndex((x,y))] <= 0):
                                    pygame.draw.rect(surface, RED, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])


                            elif (obj.getHealth()[obj.positionIndex((x,y))] <= 0):
                                surface.blit(pygame.image.load('images/NSDe.png').convert(),(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                                # pygame.draw.rect(surface, RED, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                            elif (obj.getHealth()[obj.positionIndex((x,y))] == 1 and obj.getArmour() == 2):
                                surface.blit(pygame.image.load('images/NSD.png').convert(),(x*20 + x*1 + d-1, y*20 + y*1 + 10))

                                # pygame.draw.rect(surface, ORANGE, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                            else:
                                if player1:
                                    surface.blit(pygame.image.load('images/NS.png').convert(),(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                                else:
                                    surface.blit(pygame.image.load('images/P2NSM.png').convert(),(x*20 + x*1 + d, y*20 + y*1 + 10))

                            # pygame.draw.rect(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                        
                if (obj != None and obj.getClassName() == "Base"):
                    if (obj.isSelected()):
                        c = DARKGREEN       # DARKGREEN
                    else:
                        c = obj.getColor()  # WHITE
                    pygame.draw.rect(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 21])

        
        if self.x != -1 and self.y != -1:
            # print x, y
            surface.blit(pygame.image.load('images/notifier.png').convert(),(self.x*20 + self.x*1 + d, self.y*20 + self.y*1 + 10))

