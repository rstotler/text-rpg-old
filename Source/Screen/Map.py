import pygame
from pygame import *
from GameData.World.Room import Room
from Components.Utility import *

class Map:

    def __init__(self):
        self.surface = pygame.Surface([220, 220])
        self.surface.fill([10, 30, 70])
        self.font = pygame.font.Font("../Assets/Fonts/CodeNewRomanB.otf", 12)
        
        self.screenLevel = "Area"

        self.cellSize = 48
        self.sizeRatioList = [1.0, .72, .50, .30, .18]

        self.surfaceMapDict = None
        self.surfaceCellDict = {}
        self.surfaceCellWall = {}
        self.surfaceDoor = {}
        self.surfaceMapPlayerIconDict = None
        
        self.zoomLevel = 0
        self.mapCellSizeList = None

        self.targetSystem = None
        self.surfaceSystemDict = None

        self.init()

    def init(self):
        for terrainType in ["Default", "Water", "Beach", "Dirt", "Grass", "Desert", "Mountain"]:
            terrainCell = pygame.Surface([self.cellSize, self.cellSize])
            if terrainType == "Default" : terrainCell.fill([130, 130, 130])
            elif terrainType == "Water" : terrainCell.fill([30, 65, 200])
            elif terrainType == "Beach" : terrainCell.fill([200, 200, 120])
            elif terrainType == "Dirt" : terrainCell.fill([130, 75, 60])
            elif terrainType == "Grass" : terrainCell.fill([30, 140, 45])
            elif terrainType == "Desert" : terrainCell.fill([200, 200, 120])
            elif terrainType == "Mountain" : terrainCell.fill([85, 60, 10])
            self.surfaceCellDict[terrainType] = terrainCell
        
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

    def loadAreaMap(self, area):

        # Draw Default Map #
        if True:
            surfaceMap = pygame.Surface([area.size[0] * self.cellSize, area.size[1] * self.cellSize], pygame.SRCALPHA, 32)
            surfaceMap.convert_alpha()
            
            for currentRoom in area.roomList:
                if currentRoom.mapCoordinates != [None, None]:
                    cellBlitLoc = [(currentRoom.mapCoordinates[0] * self.cellSize), (currentRoom.mapCoordinates[1] * self.cellSize)]
                    terrainCell = self.surfaceCellDict[currentRoom.terrainType]
                    surfaceMap.blit(terrainCell, cellBlitLoc)
                    for exitDir in ["North", "East", "South", "West"]:
                        if currentRoom.exit[exitDir] == None:
                            surfaceMap.blit(self.surfaceCellWall[exitDir], cellBlitLoc)
                        if exitDir in ["North", "East"] and currentRoom.door[exitDir] != None:
                            surfaceMap.blit(self.surfaceDoor[exitDir], cellBlitLoc)
                    if area.name["String"].split()[0] != "Continent":
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
            
    def loadSystemMap(self, system):
        self.targetSystem = system
        
    def toggle(self, keyName):
        if self.screenLevel == "Area":
            self.screenLevel = "System"
        else:
            self.screenLevel = "Area"

    def moveMouseWheel(self, targetDirNum, player):
        if targetDirNum > 1 : targetDirNum = 1
        elif targetDirNum < -1 : targetDirNum = -1
        drawCheck = False
        
        if self.screenLevel == "Area":
            if self.zoomLevel + targetDirNum >= 0 and self.zoomLevel + targetDirNum < len(self.sizeRatioList):
                self.zoomLevel += targetDirNum

    def draw(self, window, galaxyList, player):
        if self.screenLevel == "Area":
            self.drawAreaMap(window, galaxyList, player)
        elif self.screenLevel == "System":
            self.drawSystemMap(window, galaxyList, player)
        
    def drawAreaMap(self, window, galaxyList, player):
        targetArea, targetRoom = Room.getAreaAndRoom(galaxyList, player)
        defaultRect = self.surface.get_rect()
        mapCellSize = self.mapCellSizeList[self.zoomLevel]
        startLoc = [(defaultRect.width / 2) - (mapCellSize[0] / 2), (defaultRect.height / 2) - (mapCellSize[1] / 2)]
        mapOffset = [-(int(round(targetRoom.mapCoordinates[0] * mapCellSize[0]))), -(int(round(targetRoom.mapCoordinates[1] * mapCellSize[1])))]
        mapDisplayLoc = [startLoc[0] + mapOffset[0], startLoc[1] + mapOffset[1]]
        
        if self.surfaceMapDict != None:
            self.surface.fill([10, 10, 30])
            self.surface.blit(self.surfaceMapDict[self.zoomLevel], mapDisplayLoc)
            self.surface.blit(self.surfaceMapPlayerIconDict[self.zoomLevel], [0, 0])
                
        targetPlanet = None
        targetPlanetName = {"String":"None", "Code":"4w"}
        if player.planet != None:
            targetPlanet = galaxyList[player.galaxy].systemList[player.system].planetList[player.planet]
            targetPlanetName = targetPlanet.name
        writeFast("Planet: " + targetPlanetName["String"], [200, 200, 200], [6, 6], self.font, self.surface)
        writeFast("Area: " + targetArea.name["String"], [200, 200, 200], [6, 16], self.font, self.surface)
                
        window.blit(self.surface, [580, 0])
        
    def drawSystemMap(self, window, galaxyList, player):
        import math
        self.surface.fill([10, 10, 10])
        
        distance = 0
        orbitRadius = 0
        for p, planet in enumerate(self.targetSystem.planetList):
            orbitMod = 1
            if planet.orbit == "Clockwise":
                orbitMod = -1

            x = distance
            y = 0
            if planet.minutesInYear != 0:
                x = math.cos(math.radians((planet.currentMinutesInYear / planet.minutesInYear) * 360)) * distance
                y = (math.sin(math.radians((planet.currentMinutesInYear / planet.minutesInYear) * 360)) * distance) * orbitMod

            if p > 0:
                pygame.draw.circle(self.surface, [110, 110, 110], [100, 100], distance, 1)
            
            pygame.draw.circle(self.surface, planet.getDrawColor(), [100 + x, 100 + y], planet.getDrawRadius())
            if p < len(self.targetSystem.planetList) - 1:
                distance += planet.getDrawRadius() + self.targetSystem.planetList[p + 1].getDrawRadius() + 2
                if p == 0:
                    distance += 6

        writeFast("System: " + self.targetSystem.name["String"], [200, 200, 200], [6, 6], self.font, self.surface)
        
        window.blit(self.surface, [580, 0])
