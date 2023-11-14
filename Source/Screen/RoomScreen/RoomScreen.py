import pygame, os, traceback
from pygame import *
from GameData.World.Room import Room
from Components.Utility import *

class RoomScreen:
    displayOffset = {"Back":{"Left 2":[57, 147], "Left 3":[133, 147], "Left 4":[212, 147], "Middle":[291, 147], "Right 4":[366, 147], "Right 3":[445, 147], "Right 2":[521, 147]}, \
                     "Middle":{"Left 2":[63, 164], "Left 3":[177, 164], "Middle":[291, 164], "Right 3":[401, 164], "Right 2":[515, 164]}, \
                     "Front":{"Left 2":[100, 207], "Middle":[291, 207], "Right 2":[478, 207]}}

    def __init__(self):
        self.surface = {"Back":pygame.Surface([580, 248], pygame.SRCALPHA), "Middle":pygame.Surface([580, 248], pygame.SRCALPHA), "Front":pygame.Surface([580, 248], pygame.SRCALPHA)}
        self.font = pygame.font.Font("../Assets/Fonts/CodeNewRomanB.otf", 33)

        self.imageDict = self.loadImages()

    def loadImages(self):
        imageDict = {}

        # Floors, Ceilings, Walls #
        for area in ["Floor", "Ceiling", "Wall"]:
            imageDict[area] = {}
            for row in ["Back", "Middle", "Front", "BackWall"]:
                imageDict[area][row] = {}
                for terrainType in ["Default", "Dirt"]:
                    try:
                        imageDict[area][row][terrainType] = {}
                        if not (area != "Wall" and row == "BackWall") and \
                        not (area != "Floor" and terrainType == "Dirt"):
                            if not (area == "Wall" and row == "Front"):
                                imageDict[area][row][terrainType]["Middle"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Middle.png").convert_alpha()
                            imageDict[area][row][terrainType]["Left 1"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Left_1.png").convert_alpha()
                            imageDict[area][row][terrainType]["Right 1"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Right_1.png").convert_alpha()
                            imageDict[area][row][terrainType]["Left 2"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Left_2.png").convert_alpha()
                            imageDict[area][row][terrainType]["Right 2"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Right_2.png").convert_alpha()
                            if row in ["Back", "Middle", "BackWall"]:
                                imageDict[area][row][terrainType]["Left 3"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Left_3.png").convert_alpha()
                                imageDict[area][row][terrainType]["Right 3"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Right_3.png").convert_alpha()
                            if row in ["Back", "BackWall"]:
                                imageDict[area][row][terrainType]["Left 4"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Left_4.png").convert_alpha()
                                imageDict[area][row][terrainType]["Right 4"] = pygame.image.load("../Assets/Images/RoomScreen/" + area + "/" + terrainType + "/" + row + "_Right_4.png").convert_alpha()
                    
                    except Exception as error:
                        print(traceback.format_exc())

        # Mobs #
        imageDict["Mob"] = {}
        for subdir, dirs, files in os.walk("../Assets/Images/Mob/"):
            for file in files:
                mobNum = file[0:file.rindex('.')]
                if stringIsNumber(mobNum):
                    mobNum = int(mobNum)
                    mobImage = pygame.image.load(subdir + file).convert_alpha()
                    imageDict["Mob"][mobNum] = {"Front":mobImage, "Middle":None, "Back":None}
                    for row in ["Middle", "Back"]:
                        if row == "Middle":
                            newSize = [int(mobImage.get_width() * .75), int(mobImage.get_height() * .75)]
                            imageDict["Mob"][mobNum][row] = pygame.transform.scale(mobImage, newSize)
                        elif row == "Back":
                            newSize = [int(mobImage.get_width() * .5), int(mobImage.get_height() * .5)]
                            imageDict["Mob"][mobNum][row] = pygame.transform.scale(mobImage, newSize)

        # Attack Animations #
        imageDict["Attack Animation"] = {}
        for subdir, dirs, files in os.walk("../Assets/Images/Attack/"):
            attackName = subdir[subdir.rindex('/') + 1::]
            if attackName not in imageDict["Attack Animation"]:
                imageDict["Attack Animation"][attackName] = []
            for file in files:
                attackFrame = pygame.image.load(subdir + "/" + file).convert_alpha()
                imageDict["Attack Animation"][attackName].append(attackFrame)

        return imageDict

    def draw(self, window, galaxyList, player):
        playerPlanet = None
        playerArea, playerRoom = Room.getAreaAndRoom(galaxyList, player)
        targetSpaceshipNum = None
        if playerRoom.spaceshipObject != None:
            targetSpaceshipNum = playerRoom.spaceshipObject.num
        if playerRoom.spaceshipObject == None or playerRoom.spaceshipObject.landedLocation != None:
            playerPlanet = galaxyList[player.galaxy].systemList[player.system].planetList[player.planet]

        screenSurface = {"Back":self.surface["Back"].copy(), "Middle":self.surface["Middle"].copy(), "Front":self.surface["Front"].copy()}

        # Sky #
        if True:
            totalDayPercent = playerPlanet.currentMinutesInDay / playerPlanet.minutesInDay
            skyColor = playerPlanet.skyColor
            if totalDayPercent < playerPlanet.dawnPercent or totalDayPercent >= playerPlanet.sunsetPercent:
                skyColor = playerPlanet.nightSkyColor

            dawnDuskPercent = None
            minutesBeforeDusk = None
            minutesBeforeDawn = (playerPlanet.dawnPercent * playerPlanet.minutesInDay)
            if totalDayPercent >= playerPlanet.dawnPercent and totalDayPercent < playerPlanet.sunrisePercent:
                dawnMinutes = (playerPlanet.sunrisePercent * playerPlanet.minutesInDay) - minutesBeforeDawn
                dawnDuskPercent = (playerPlanet.currentMinutesInDay - minutesBeforeDawn) / dawnMinutes
            elif totalDayPercent >= playerPlanet.duskPercent and totalDayPercent < playerPlanet.sunsetPercent:
                minutesBeforeDusk = (playerPlanet.duskPercent * playerPlanet.minutesInDay)
                duskMinutes = (playerPlanet.sunsetPercent * playerPlanet.minutesInDay) - minutesBeforeDusk
                dawnDuskPercent = (playerPlanet.currentMinutesInDay - minutesBeforeDusk) / duskMinutes

            if dawnDuskPercent != None:
                if dawnDuskPercent <= .5 : dawnDuskPercentMod = dawnDuskPercent * 2
                else : dawnDuskPercentMod = (dawnDuskPercent - .5) * 2
                if dawnDuskPercent > .5 and playerPlanet.switchSkyColorCheck == False:
                    playerPlanet.switchSkyColorCheck = True
                    playerPlanet.currentSkyColor = playerPlanet.targetSkyColor
                    playerPlanet.targetSkyColor = playerPlanet.skyColor
                    if minutesBeforeDusk != None:
                        playerPlanet.targetSkyColor = playerPlanet.nightSkyColor
                skyColor = playerPlanet.updateSkyColor(dawnDuskPercentMod)
            screenSurface["Back"].fill(skyColor)

        # Outside - Draw Sun #
        if totalDayPercent >= playerPlanet.dawnPercent and totalDayPercent < playerPlanet.sunsetPercent:
            import math

            dayMinutes = (playerPlanet.sunsetPercent * playerPlanet.minutesInDay) - minutesBeforeDawn
            dayLightPercent = (playerPlanet.currentMinutesInDay - minutesBeforeDawn) / dayMinutes
            x = (math.cos(math.radians(dayLightPercent * 180)) * 260)
            y = ((math.sin(math.radians(dayLightPercent * 180)) * 175) * -1)
            pygame.draw.circle(screenSurface["Back"], [100, 100, 0], [290 + x, 175 + y], 30)

        # Draw Room Rows #
        rowList = ["Back", "Middle", "Front"]
        for row in rowList:
            if row == "Back" : loopRange = 5
            elif row == "Middle" : loopRange = 4
            else : loopRange = 3
            for i in range(loopRange):

                # Static Ground #
                if i == 0:
                    if row == "Back":
                        pygame.draw.rect(screenSurface["Back"], [20, 10, 0], [0, 141, 580, 13])
                    elif row == "Middle":
                        pygame.draw.rect(screenSurface["Back"], [20, 10, 0], [0, 154, 580, 22])
                    elif row == "Front":
                        pygame.draw.rect(screenSurface["Back"],[20, 10, 0], [0, 176, 580, 72])
                        
                sideList = ["Left", "Right"]
                if i == loopRange - 1:
                    sideList = ["Middle"]
                for side in sideList:
                    if side == "Middle":
                        targetSide = side
                    else:
                        targetSide = side + " " + str(i + 1)
                    if targetSide in self.imageDict["Floor"][row]["Default"]:
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
                                    if len(targetRoom.exit["North"]) == 3:
                                        northExitArea = targetRoom.exit["North"][1]
                                        northExitRoom = targetRoom.exit["North"][2]
                                        northRoom = targetRoom.spaceshipObject.areaList[northExitArea].roomList[northExitRoom]
                                    else:
                                        northExitGalaxy = targetRoom.exit["North"][0]
                                        northExitSystem = targetRoom.exit["North"][1]
                                        northExitPlanet = targetRoom.exit["North"][2]
                                        northExitArea = targetRoom.exit["North"][3]
                                        northExitRoom = targetRoom.exit["North"][4]
                                        northRoom = Room.exists(galaxyList, targetSpaceshipNum, northExitGalaxy, northExitSystem, northExitPlanet, northExitArea, northExitRoom)
                                    
                            drawFloor = True
                            if targetRoom == None:
                                drawFloor = False

                        # Back Wall #
                        if row == "Back" and playerRoom.inside == True and (northRoom == None or northRoom.inside == False):
                            screenSurface["Back"].blit(self.imageDict["Wall"]["BackWall"]["Default"][targetSide], [0, 0])

                        # Ceiling #
                        if targetRoom != None and targetRoom.inside == True and \
                        not (playerRoom.inside == False and targetSide == "Middle"):
                            ceilingImage = self.imageDict["Ceiling"][row]["Default"][targetSide]
                            screenSurface[row].blit(ceilingImage, [0, 0])
                        else:
                            pass

                        # Outside Walls #
                        if targetRoom != None and targetRoom.inside == True:
                            
                            # Outside Walls #
                            if playerRoom.inside == False:
                                wallImage = self.imageDict["Wall"][row]["Default"][targetSide]
                                screenSurface[row].blit(wallImage, [0, 0])
                                drawFloor = False

                        # Inside Walls #
                        elif (playerRoom.inside == True and ((targetRoom != None and targetRoom.inside == False) or targetRoom == None)):
                            screenSurface[row].blit(self.imageDict["Wall"][row]["Default"][targetSide], [0, 0])
                            drawFloor = False
                            
                        # Floor #
                        if drawFloor == True:
                            terrainType = targetRoom.terrainType
                            if terrainType not in self.imageDict["Floor"][row]:
                                terrainType = "Default"
                            floorImage = self.imageDict["Floor"][row][terrainType][targetSide]
                            screenSurface[row].blit(floorImage, [0, 0])

                            # Mobs #
                            if targetRoom != None and len(targetRoom.mobList) > 0 and row in self.displayOffset and targetSide in self.displayOffset[row]:
                                for mob in targetRoom.mobList:
                                    if mob.num in self.imageDict["Mob"] and row in self.imageDict["Mob"][mob.num]:
                                        mobImage = self.imageDict["Mob"][mob.num][row]
                                        offsetRatio = 1.0
                                        if row == "Middle" : offsetRatio = .44
                                        elif row == "Back" : offsetRatio = .18
                                        x = self.displayOffset[row][targetSide][0] - (mobImage.get_width() / 2) + int(mob.displayOffset[0] * offsetRatio)
                                        y = self.displayOffset[row][targetSide][1] - mobImage.get_height() + int(mob.displayOffset[1] * offsetRatio)
                                        screenSurface[row].blit(mobImage, [x, y])

                        # Damage Animations #
                        if targetRoom != None and len(targetRoom.damageAnimationList) > 0:
                            for damageAnimation in targetRoom.damageAnimationList:
                                damageAnimation.draw(screenSurface[row], self.imageDict["Attack Animation"][damageAnimation.name], self.displayOffset[row][targetSide])
                                damageAnimation.update(self.imageDict["Attack Animation"][damageAnimation.name])

        for row in ["Back", "Middle", "Front"]:
            window.blit(screenSurface[row], [0, 0])
