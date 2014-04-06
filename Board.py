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
        
        self.P1E_front = pygame.image.load('images/FE.png').convert()
        self.P1EW_mid = pygame.image.load('images/EW.png').convert()

        self.E_frontD = pygame.image.load('images/FED.png').convert()
        self.EW_midD = pygame.image.load('images/EWD.png').convert()

        self.E_frontDe = pygame.image.load('images/FEDe.png').convert()
        self.EW_midDe = pygame.image.load('images/EWDe.png').convert()

        self.E_frontS = pygame.image.load('images/FEs.png').convert()
        self.EW_midS = pygame.image.load('images/EWs.png').convert()

        self.P1N_front = pygame.image.load('images/P1FN.png').convert()
        self.P1NS_mid = pygame.image.load('images/NS.png').convert()
        
        self.N_frontD = pygame.image.load('images/FND.png').convert()
        self.NS_midD = pygame.image.load('images/NSD.png').convert()

        self.N_frontDe = pygame.image.load('images/FNDe.png').convert()
        self.NS_midDe = pygame.image.load('images/NSDe.png').convert()
        
        self.N_s = pygame.image.load('images/FNs.png').convert()
        self.NS_s = pygame.image.load('images/NSs.png').convert()


        self.FW_s = pygame.image.load('images/FWs.png').convert()
        self.FWD = pygame.image.load('images/FWD.png').convert()
        self.FWDe = pygame.image.load('images/FWDe.png').convert()
        self.P1_Wfront =pygame.image.load('images/FW.png').convert()

        self.FS_s = pygame.image.load('images/FSs.png').convert()
        self.FSD = pygame.image.load('images/FSD.png').convert()
        self.FSDe = pygame.image.load('images/FSDe.png').convert()
        self.P1_Sfront =pygame.image.load('images/P1FS.png').convert()

        self.P2NF = pygame.image.load('images/P2FN.png').convert()
        self.P2EWM = pygame.image.load('images/P2EW.png').convert()
        self.P2SF = pygame.image.load('images/P2FS.png').convert()
        self.P2EF =pygame.image.load('images/P2FE.png').convert()
        self.P2WF =pygame.image.load('images/P2FW.png').convert()
        self.P2NSM = pygame.image.load('images/P2NSM.png').convert()

        self.w1 = pygame.image.load('images/water1.png').convert()
        self.w2 = pygame.image.load('images/water2.png').convert()
        self.dw1 = pygame.image.load('images/darkwater1.png').convert()
        self.dw2 = pygame.image.load('images/darkwater2.png').convert()

        self.c1 = pygame.image.load('images/coral1.png').convert()
        self.c2 = pygame.image.load('images/coral2.png').convert()

        self.note = pygame.image.load('images/notifier.png').convert()

        self.mine1 = pygame.image.load('images/mine1.png').convert()

        self.mine2 = pygame.image.load('images/mine2.png').convert()
        
        self.radar = pygame.image.load('images/radar.png').convert()

        # self.P1E_front = P1E_front
        # self.P1EW_mid = images[1]

        # self.E_frontD = images[2]
        # self.EW_midD = images[3]

        # self.E_frontDe = images[4]
        # self.EW_midDe = images[5]

        # self.E_frontS = images[6]
        # self.EW_midS = images[7]


        # self.P1N_front = images[8]
        # self.P1NS_mid = images[9]

        # self.N_frontD = images[10]
        # self.NS_midD = images[11]

        # self.N_frontDe = images[12]
        # self.NS_midDe = images[13]

        # self.N_s = images[14]
        # self.NS_s = images[15]

        # self.P1_Wfront = images[16]
        # self.FWD = images[17]
        # self.FWDe= images[18]
        # self.FW_s= images[19]

        # self.P1_Sfront= images[20]
        # self.FSD= images[21]
        # self.FSDe= images[22]
        # self.FS_s= images[23]

        # self.P2NF = images[24] 
        # self.P2NSM= images[25]
        # self.P2SF = images[26]
        # self.P2EF = images[27]
        # self.P2WF = images[28]
        # self.P2EWM = images[29]

        # self.w1 = images[30]
        # self.w2= images[31]
        # self.dw1= images[32]
        # self.dw2= images[33]

        # self.c1 = images[34]
        # self.c2 = images[35]

        # self.note = images[36]

        # self.mine1 = images[37]
        # self.mine2 = images[38]

        # self.radar = images[39]


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
                            surface.blit(self.w1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            # print 'w2'
                            surface.blit(self.w2,(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, LIGHTSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if self.tick == 0:
                            surface.blit(self.dw1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(self.dw2,(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, DARKSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                      
                elif (obj.getClassName() == "Coral"):
                    if self.tick == 0:
                            # print 'w1'
                        surface.blit(self.c1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                    else:
                        surface.blit(self.c2,(x*20 + x*1 + d ,y*20 + y*1 + 10))

                
                elif (obj.getClassName() != "Coral"):
                    if (aRange):
                        pygame.draw.rect(surface,GREEN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    elif (vis and not aRange):
                        if self.tick == 0:
                            surface.blit(self.w1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(self.w2,(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, LIGHTSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if self.tick == 0:
                            surface.blit(self.dw1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(self.dw2,(x*20 + x*1 + d ,y*20 + y*1 + 10))


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
                            surface.blit(self.w1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(self.w2,(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, LIGHTSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if self.tick == 0:
                            surface.blit(self.dw1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(self.dw2,(x*20 + x*1 + d ,y*20 + y*1 + 10))


                elif (obj.getClassName() == "Coral"):
                    if self.tick == 0:
                            # print 'w1'
                        surface.blit(self.c1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                    else:
                        surface.blit(self.c2,(x*20 + x*1 + d ,y*20 + y*1 + 10))

                
                elif (obj.getClassName() != "Coral"):
                    if (aRange):
                        pygame.draw.rect(surface,GREEN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    elif (vis and not aRange):
                        if self.tick == 0:
                            surface.blit(self.w1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(self.w2,(x*20 + x*1 + d ,y*20 + y*1 + 10))

                        # pygame.draw.rect(surface, LIGHTSEA, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if self.tick == 0:
                            surface.blit(self.dw1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(self.dw2,(x*20 + x*1 + d ,y*20 + y*1 + 10))

                if (sonarVisibility):
                    if(obj == None):
                        surface.blit(self.radar,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                    elif(obj.getClassName() == "Mine"):
                        #print "MINE"
                        if self.tick == 0:
                            surface.blit(self.mine1,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        else:
                            surface.blit(self.mine2,(x*20 + x*1 + d ,y*20 + y*1 + 10))
                        

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
                                surface.blit(self.E_frontS,(x*20 + x*1 + d, y*20 + y*1 + 10))

                            elif (obj.getHealth()[0] <= 0):
                                # pygame.draw.polygon(surface, RED, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d+20-1, y*20 + y*1 + 20)], 0)
                                surface.blit(self.E_frontDe,(x*20 + x*1 + d, y*20 + y*1 + 10))

                            elif (obj.getHealth()[0] == 1 and obj.getArmour() == 2):
                                # pygame.draw.polygon(surface, ORANGE, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d+20-1, y*20 + y*1 + 20)], 0)
                                surface.blit(self.E_frontD,(x*20 + x*1 + d, y*20 + y*1 + 10))

                            else:
                                if player1:
                                    surface.blit(self.P1E_front,(x*20 + x*1 + d, y*20 + y*1 + 10))
                                else:
                                    surface.blit(self.P2EF,(x*20 + x*1 + d, y*20 + y*1 + 10))

        
                                # pygame.draw.polygon(surface, c, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d, y*20 + y*1 + 29), (x*20 + x*1 + d+20-1, y*20 + y*1 + 20)], 0)
                        elif (obj.getOrientation() == "S"):
                            if (obj.isSelected()):
                                surface.blit(self.FS_s,(x*20 + x*1 + d, y*20 + y*1 + 10))
                            elif (obj.getHealth()[0] <= 0):
                                surface.blit(self.FSDe,(x*20 + x*1 + d, y*20 + y*1 + 10))
                                # pygame.draw.polygon(surface, RED, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 10, y*20 + y*1 + 29)], 0)
                            elif (obj.getHealth()[0] == 1 and obj.getArmour() == 2):
                                surface.blit(self.FSD,(x*20 + x*1 + d, y*20 + y*1 + 10))
                                # pygame.draw.polygon(surface, ORANGE, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 10, y*20 + y*1 + 29)], 0)
                            else:
                                if player1:    
                                    surface.blit(self.P1_Sfront,(x*20 + x*1 + d, y*20 + y*1 + 10))
                                else:
                                    surface.blit(self.P2SF,(x*20 + x*1 + d, y*20 + y*1 + 10))

                                # pygame.draw.polygon(surface, c, [(x*20 + x*1 + d, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 10, y*20 + y*1 + 29)], 0)
                        elif obj.orientation == "W":
                            if (obj.isSelected()):
                                surface.blit(self.FW_s,(x*20 + x*1 + d, y*20 + y*1 + 10))
                            elif (obj.getHealth()[0] <= 0):                            
                                surface.blit(self.FWDe,(x*20 + x*1 + d, y*20 + y*1 + 10))
                                # pygame.draw.polygon(surface, RED, [(x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 29), (x*20 + x*1 + d, y*20 + y*1 + 20)], 0)
                            elif (obj.getHealth()[0] == 1 and obj.getArmour() == 2):
                                surface.blit(self.FWD,(x*20 + x*1 + d, y*20 + y*1 + 10))

                                # pygame.draw.polygon(surface, ORANGE, [(x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 29), (x*20 + x*1 + d, y*20 + y*1 + 20)], 0)
                            else:
                                if player1:
                                    surface.blit(self.P1_Wfront,(x*20 + x*1 + d, y*20 + y*1 + 10))
                                else:
                                    surface.blit(self.P2WF,(x*20 + x*1 + d, y*20 + y*1 + 10))

                                # pygame.draw.polygon(surface, c, [(x*20 + x*1 + d + 19, y*20 + y*1 + 10), (x*20 + x*1 + d + 19, y*20 + y*1 + 29), (x*20 + x*1 + d, y*20 + y*1 + 20)], 0)
                        
                        elif obj.orientation == "N":
                            if (obj.isSelected()):
                                surface.blit(self.N_s,(x*20 + x*1 + d, y*20 + y*1 + 10))

                            elif (obj.getHealth()[0] <= 0):                            
                                surface.blit(self.N_frontDe,(x*20 + x*1 + d, y*20 + y*1 + 10))

                            elif (obj.getHealth()[0] == 1 and obj.getArmour() == 2):
                                surface.blit(self.N_frontD,(x*20 + x*1 + d, y*20 + y*1 + 10))
                            else:
                                if player1:
                                    surface.blit(self.P1N_front,(x*20 + x*1 + d, y*20 + y*1 + 10))
                                else:
                                    surface.blit(self.P2NF,(x*20 + x*1 + d, y*20 + y*1 + 10))

                        else:
                            pygame.draw.rect(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                    else:
                        if (obj.getOrientation() == "E" or obj.getOrientation() == "W"):
                            if(obj.isSelected()):
                                surface.blit(self.EW_midS,(x*20 + x*1 + d-1, y*20 + y*1 + 10))

                            #?
                            elif (obj.getName() == "RadarBoat" and obj.positionIndex((x,y)) == 1): # This is where the middle part of te boat is at
                                pygame.draw.rect(surface, BROWN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 21])
                                if (obj.getHealth()[obj.positionIndex((x,y))] <= 0):
                                    pygame.draw.rect(surface, RED, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])


                            elif (obj.getHealth()[obj.positionIndex((x,y))] <= 0):
                                surface.blit(self.EW_midDe,(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                                # pygame.draw.rect(surface, RED, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                            elif (obj.getHealth()[obj.positionIndex((x,y))] == 1 and obj.getArmour() == 2):
                                surface.blit(self.EW_midD,(x*20 + x*1 + d-1, y*20 + y*1 + 10))

                                # pygame.draw.rect(surface, ORANGE, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                            else:
                                if player1:
                                    surface.blit(self.P1EW_mid,(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                                else:
                                    surface.blit(self.P2NSM,(x*20 + x*1 + d, y*20 + y*1 + 10))


                        else:
                            if(obj.isSelected()):
                                surface.blit(self.NS_s,(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                            
                            elif (obj.getName() == "RadarBoat" and obj.positionIndex((x,y)) == 1):
                                pygame.draw.rect(surface, BROWN, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 21])
                                if (obj.getHealth()[obj.positionIndex((x,y))] <= 0):
                                    pygame.draw.rect(surface, RED, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])


                            elif (obj.getHealth()[obj.positionIndex((x,y))] <= 0):
                                surface.blit(self.NS_midDe,(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                                # pygame.draw.rect(surface, RED, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                            elif (obj.getHealth()[obj.positionIndex((x,y))] == 1 and obj.getArmour() == 2):
                                surface.blit(self.NS_midD,(x*20 + x*1 + d-1, y*20 + y*1 + 10))

                                # pygame.draw.rect(surface, ORANGE, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                            else:
                                if player1:
                                    surface.blit(self.P1NS_mid,(x*20 + x*1 + d-1, y*20 + y*1 + 10))
                                else:
                                    surface.blit(self.P2EWM,(x*20 + x*1 + d, y*20 + y*1 + 10))

                            # pygame.draw.rect(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 20])
                        
                if (obj != None and obj.getClassName() == "Base"):
                    if (obj.isSelected()):
                        c = DARKGREEN       # DARKGREEN
                    else:
                        c = obj.getColor()  # WHITE
                    pygame.draw.rect(surface, c, [x*20 + x*1 + d, y*20 + y*1 + 10, 20, 21])

        
        if self.x != -1 and self.y != -1:
            # print x, y
            surface.blit(self.note,(self.x*20 + self.x*1 + d, self.y*20 + self.y*1 + 10))

