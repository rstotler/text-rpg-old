import pygame, traceback
from pygame import *
from GameData.World.Room import Room

class RoomScreen:
    def __init__(self):
        self.imageDict = self.loadImages()
        self.surface = pygame.Surface([200, 200])

    def loadImages(self):
        imageDict = {}

        for area in ["Floor", "Ceiling", "Wall"]:
            imageDict[area] = {}
            for row in ["Back", "Middle", "Front", "BackWall"]:
                try:
                    if not (area != "Wall" and row == "BackWall"):
                        imageDict[area][row] = {}
                        if not (area == "Wall" and row == "Front"):
                            imageDict[area][row]["Middle"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + row + "_Middle.png").convert_alpha()
                        imageDict[area][row]["Left 1"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + row + "_Left_1.png").convert_alpha()
                        imageDict[area][row]["Right 1"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + row + "_Right_1.png").convert_alpha()
                        if row in ["Back", "Middle", "BackWall"]:
                            imageDict[area][row]["Left 2"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + row + "_Left_2.png").convert_alpha()
                            imageDict[area][row]["Right 2"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + row + "_Right_2.png").convert_alpha()
                        if row in ["Back", "BackWall"]:
                            imageDict[area][row]["Left 3"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + row + "_Left_3.png").convert_alpha()
                            imageDict[area][row]["Right 3"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + row + "_Right_3.png").convert_alpha()
                except Exception as error:
                    print(traceback.format_exc())

        return imageDict

    def draw(self, window, galaxyList, player):
        self.surface.fill([10, 30, 70])

        playerArea, playerRoom = Room.getAreaAndRoom(galaxyList, player)
        targetSpaceshipNum = None
        if playerRoom.spaceshipObject != None:
            targetSpaceshipNum = playerRoom.spaceshipObject.num

        rowList = ["Back", "Middle", "Front"]
        for row in rowList:
            if row == "Back" : loopRange = 4
            elif row == "Middle" : loopRange = 3
            else : loopRange = 2
            for i in range(loopRange):
                sideList = ["Left", "Right"]
                if i == loopRange - 1:
                    sideList = ["Middle"]
                for side in sideList:
                    if side == "Middle":
                        targetSide = side
                    else:
                        targetSide = side + " " + str(i + 1)
                    if targetSide in self.imageDict["Floor"][row]:
                        xOffset = loopRange - 1 - i
                        if side == "Left" : xOffset *= -1
                        yOffset = -(2 - rowList.index(row))
                        targetLoc = [playerRoom.mapCoordinates[0] + xOffset, playerRoom.mapCoordinates[1] + yOffset]

                        # Get Data #
                        if True:
                            northRoom = None
                            targetRoom = None
                            if targetLoc[0] >= 0 and targetLoc[1] >= 0 and targetLoc[0] < len(playerArea.roomNumMap) and targetLoc[1] < len(playerArea.roomNumMap[0]):
                                if playerArea.roomNumMap[targetLoc[0]][targetLoc[1]] != None:
                                    targetRoom = playerArea.roomList[playerArea.roomNumMap[targetLoc[0]][targetLoc[1]]]
                            
                            if targetRoom != None:
                                if isinstance(targetRoom.exit["North"], list) == True:
                                    northRoom = Room.exists(galaxyList, targetSpaceshipNum, targetRoom.exit["North"][0], targetRoom.exit["North"][1], targetRoom.exit["North"][2], targetRoom.exit["North"][3], targetRoom.exit["North"][4])
                                
                            drawFloor = True
                            if targetRoom == None:
                                drawFloor = False

                        # Back Wall #
                        if row == "Back" and playerRoom.inside == True and (northRoom == None or northRoom.inside == False):
                            self.surface.blit(self.imageDict["Wall"]["BackWall"][targetSide], [0, 0])

                        # Outside Walls #
                        if targetRoom != None and targetRoom.inside == True:
                            
                            # Ceiling #
                            if True:
                                ceilingImage = self.imageDict["Ceiling"][row][targetSide]
                                self.surface.blit(ceilingImage, [0, 0])

                            # Outside Walls #
                            if playerRoom.inside == False:
                                wallImage = self.imageDict["Wall"][row][targetSide]
                                self.surface.blit(wallImage, [0, 0])
                                drawFloor = False

                        # Inside Walls #
                        elif (playerRoom.inside == True and ((targetRoom != None and targetRoom.inside == False) or targetRoom == None)):
                            self.surface.blit(self.imageDict["Wall"][row][targetSide], [0, 0])
                            drawFloor = False
                            
                        # Floor #
                        if drawFloor == True:
                            floorImage = self.imageDict["Floor"][row][targetSide]
                            self.surface.blit(floorImage, [0, 0])

        window.blit(self.surface, [600, 200])
