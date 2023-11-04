import pygame, random, opensimplex
from pygame import *
from Utility import *

pygame.init()
pygame.display.set_caption("Map Generation Test")
window = pygame.display.set_mode((960, 720), 0, 32)
clock = pygame.time.Clock()

size = [300, 300]
cellSize = 2

def getTerrainCell(terrainType):
    terrainCell = pygame.Surface([cellSize, cellSize])
    if terrainType == "Water" : terrainCell.fill([30, 65, 200])
    if terrainType == "Beach" : terrainCell.fill([200, 200, 120])
    if terrainType == "Grass" : terrainCell.fill([30, 140, 45])
    if terrainType == "Desert" : terrainCell.fill([200, 200, 120])
    if terrainType == "Mountain" : terrainCell.fill([85, 60, 10])
    return terrainCell

def createContinent(size, cellSize):
    mapData = []
    for renderIndex in range(4):
        simplexBase = opensimplex.OpenSimplex(random.randrange(2560))
        simplexDetail = opensimplex.OpenSimplex(random.randrange(2560))
        simplexFine = opensimplex.OpenSimplex(random.randrange(2560))
    
        for y in range(size[1]):
            if renderIndex == 0 : mapData.append([])
            for x in range(size[0]):
            
                # Get HeightMap Value #
                if True:
                    if renderIndex == 0 : renderResolutionMod = 3.0
                    elif renderIndex in [1, 2] : renderResolutionMod = 1.0
                    elif renderIndex == 3 : renderResolutionMod = 1.4
                    valueBase = simplexBase.noise2(x / (48.0 * renderResolutionMod), y / (48.0 * renderResolutionMod))
                    valueDetail = simplexDetail.noise2(x / (18.0 * renderResolutionMod), y / (18.0 * renderResolutionMod))
                    valueFine = simplexFine.noise2(x / (8.0 * renderResolutionMod), y / (8.0 * renderResolutionMod))
                    heightValue = valueBase + (valueDetail * .5) + (valueFine * .25)
                    heightValue = (heightValue + 1.0) / 2.0
                    if heightValue > 1.0 : heightValue = 1.0
                    
                # Get Terrain Type #
                if True:
                    terrainType = None
                    if renderIndex == 0:
                        if heightValue < .64 : terrainType = "Grass"
                        elif heightValue < .655 : terrainType = "Beach"
                        else : terrainType = "Water"
                    elif renderIndex == 1:
                        if heightValue < .33 : terrainType = "Water"
                        elif heightValue < .37 : terrainType = "Beach"
                    elif renderIndex == 2:
                        if heightValue < .21 : terrainType = "Desert"
                    elif renderIndex == 3:
                        if heightValue > .73 : terrainType = "Mountain"
                        
                # Round Edges #
                if renderIndex == 3:
                    if not circleCircleCollide([x, y], 1, [int(size[0] / 2), int(size[1] / 2)], int(size[0] * .465)):
                        if mapData[y][x] not in ["Water", "Mountain"]:
                            terrainType = "Beach"
                    if not circleCircleCollide([x, y], 1, [int(size[0] / 2), int(size[1] / 2)], int(size[0] * .47)):
                        terrainType = "Water"
                        
                # Assign Data #
                if renderIndex == 0:
                    mapData[-1].append(terrainType)
                    
                elif terrainType != None:
                    if not (renderIndex in [1, 2, 3] and mapData[y][x] == "Water"):
                        mapData[y][x] = terrainType

    surface = pygame.Surface([size[0] * cellSize, size[1] * cellSize])
    surface.fill([0, 0, 0])
    for y, yData in enumerate(mapData):
        for x, xData in enumerate(yData):
            terrainCell = getTerrainCell(mapData[y][x])
            surface.blit(terrainCell, [x * cellSize, y * cellSize])

    return surface
                    
def processInput():
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            pass
        elif event.type == MOUSEBUTTONUP:
            pass
        elif event.type == MOUSEMOTION:
            pass
        elif (event.type == KEYDOWN and event.key == K_ESCAPE) or event.type == QUIT:
            raise SystemExit

def draw(window, surface):
    window.fill([0, 0, 0])
    window.blit(surface, [0, 0])

def update(window, surface):
    processInput()
    draw(window, surface)

surface = createContinent(size, cellSize)
while True:
    clock.tick(60)
    update(window, surface)
    pygame.display.flip()
