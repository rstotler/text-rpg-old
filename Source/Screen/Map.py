import pygame
from pygame import *
from GameData.World.Room import Room
from Components.Utility import writeFast

class Map:

    def __init__(self):
        self.surface = pygame.Surface([200, 200])
        self.surface.fill([10, 30, 70])
        self.font = pygame.font.Font("../Assets/Fonts/CodeNewRomanB.otf", 12)

        self.cellSize = 32
        self.sizeRatioList = [1.0, .72, .50, .30, .18, .12]

        self.surfaceMapDict = None
        self.surfaceCell = None
        self.surfaceCellWall = {}
        self.surfaceDoor = {}
        self.surfaceMapPlayerIconDict = None
        
        self.zoomLevel = 0
        self.mapCellSizeList = None

        self.init()

    def init(self):
        self.surfaceCell = pygame.Surface([self.cellSize, self.cellSize])
        self.surfaceCell.fill([140, 140, 140])
        
        self.surfaceCellWall["North"] = pygame.Surface([self.cellSize, self.cellSize], pygame.SRCALPHA, 32)
        self.surfaceCellWall["East"] = pygame.Surface([self.cellSize, self.cellSize], pygame.SRCALPHA, 32)
        self.surfaceCellWall["South"] = pygame.Surface([self.cellSize, self.cellSize], pygame.SRCALPHA, 32)
        self.surfaceCellWall["West"] = pygame.Surface([self.cellSize, self.cellSize], pygame.SRCALPHA, 32)
        pygame.draw.line(self.surfaceCellWall["North"], [50, 50, 50], [0, 0], [self.cellSize, 0], 3)
        pygame.draw.line(self.surfaceCellWall["East"], [50, 50, 50], [self.cellSize-1, 0], [self.cellSize-1, self.cellSize], 3)
        pygame.draw.line(self.surfaceCellWall["South"], [50, 50, 50], [0, self.cellSize], [self.cellSize, self.cellSize], 5)
        pygame.draw.line(self.surfaceCellWall["West"], [50, 50, 50], [0, 0], [0, self.cellSize], 2)
        
        self.surfaceDoor["North"] = pygame.Surface([self.cellSize, self.cellSize], pygame.SRCALPHA, 32)
        self.surfaceDoor["East"] = pygame.Surface([self.cellSize, self.cellSize], pygame.SRCALPHA, 32)
        self.surfaceDoor["South"] = pygame.Surface([self.cellSize, self.cellSize], pygame.SRCALPHA, 32)
        self.surfaceDoor["West"] = pygame.Surface([self.cellSize, self.cellSize], pygame.SRCALPHA, 32)
        pygame.draw.line(self.surfaceDoor["North"], [50, 50, 50], [0, 0], [self.cellSize, 0], 3)
        pygame.draw.line(self.surfaceDoor["East"], [50, 50, 50], [self.cellSize-1, 0], [self.cellSize-1, self.cellSize], 3)
        pygame.draw.line(self.surfaceDoor["South"], [50, 50, 50], [0, self.cellSize], [self.cellSize, self.cellSize], 3)
        pygame.draw.line(self.surfaceDoor["West"], [50, 50, 50], [0, 0], [0, self.cellSize], 3)

    def loadMap(self, area):

        # Draw Default Map #
        if True:
            surfaceMap = pygame.Surface([area.size[0] * self.cellSize, area.size[1] * self.cellSize], pygame.SRCALPHA, 32)
            surfaceMap.convert_alpha()
            
            for currentRoom in area.roomList:
                if currentRoom.mapCoordinates != [None, None]:
                    cellBlitLoc = [(currentRoom.mapCoordinates[0] * self.cellSize), (currentRoom.mapCoordinates[1] * self.cellSize)]
                    surfaceMap.blit(self.surfaceCell, cellBlitLoc)
                    for exitDir in ["North", "East", "South", "West"]:
                        if currentRoom.exit[exitDir] == None:
                            surfaceMap.blit(self.surfaceCellWall[exitDir], cellBlitLoc)
                        if exitDir in ["North", "East"] and currentRoom.door[exitDir] != None:
                            surfaceMap.blit(self.surfaceDoor[exitDir], cellBlitLoc)
                    writeFast(str(currentRoom.room), [50, 50, 50], [cellBlitLoc[0] + 4, cellBlitLoc[1] + 4], self.font, surfaceMap)
                    
        # Resize Default Map For Zoom #
        if True:
            defaultSize = [area.size[0] * self.cellSize, area.size[1] * self.cellSize]
            self.surfaceMapDict = {}
            self.surfaceMapPlayerIconDict = {}
            self.mapCellSizeList = []
            for i, sizeRatio in enumerate(self.sizeRatioList):
                self.surfaceMapDict[i] = pygame.transform.scale(surfaceMap, [int(round(defaultSize[0] * sizeRatio)), int(round(defaultSize[1] * sizeRatio))])
                
                # Cell Size List #
                surfaceRect = self.surfaceMapDict[i].get_rect()
                self.mapCellSizeList.append([(surfaceRect.width / (area.size[0] + 0.0)),
                                             (surfaceRect.height / (area.size[1] + 0.0))])
                                                
                # Player Icon #
                defaultRect = self.surface.get_rect()
                self.surfaceMapPlayerIconDict[i] = pygame.Surface([defaultRect.width, defaultRect.height], pygame.SRCALPHA, 32)
                playerIconLoc = [int(round(defaultRect.width / 2)), int(round(defaultRect.height / 2))]
                pygame.draw.circle(self.surfaceMapPlayerIconDict[i], [170, 10, 10], playerIconLoc, int(round(10 * sizeRatio)))
                
    def moveMouseWheel(self, targetDirNum, player):
        if targetDirNum > 1 : targetDirNum = 1
        elif targetDirNum < -1 : targetDirNum = -1
        drawCheck = False
        if self.zoomLevel + targetDirNum >= 0 and self.zoomLevel + targetDirNum < len(self.sizeRatioList):
            self.zoomLevel += targetDirNum

    def draw(self, window, galaxyList, player):
        targetArea, targetRoom = Room.getAreaAndRoom(galaxyList, player)
        defaultRect = self.surface.get_rect()
        mapCellSize = self.mapCellSizeList[self.zoomLevel]
        startLoc = [(defaultRect.width / 2) - (mapCellSize[0] / 2), (defaultRect.height / 2) - (mapCellSize[1] / 2)]
        mapOffset = [-(int(round(targetRoom.mapCoordinates[0] * mapCellSize[0]))), -(int(round(targetRoom.mapCoordinates[1] * mapCellSize[1])))]
        mapDisplayLoc = [startLoc[0] + mapOffset[0], startLoc[1] + mapOffset[1]]
        
        if self.surfaceMapDict != None:
            self.surface.fill([10, 10, 30])
            if self.zoomLevel in self.surfaceMapDict:
                self.surface.blit(self.surfaceMapDict[self.zoomLevel], mapDisplayLoc)
            self.surface.blit(self.surfaceMapPlayerIconDict[self.zoomLevel], [0, 0])
                
        targetPlanet = None
        targetPlanetName = None
        if player.planet != None:
            targetPlanet = galaxyList[player.galaxy].systemList[player.system].planetList[player.planet]
            targetPlanetName = targetPlanet.name
        writeFast("Planet: " + targetPlanetName["String"], [200, 200, 200], [0, 10], self.font, self.surface)
        writeFast("Area: " + targetArea.name["String"], [200, 200, 200], [0, 0], self.font, self.surface)
                
        window.blit(self.surface, [600, 0])
        