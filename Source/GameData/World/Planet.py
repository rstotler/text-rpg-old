import math, random, opensimplex
from GameData.World.Area import Area
from GameData.World.Room import Room
from Components.Utility import *

class Planet:

    def __init__(self, galaxyList, galaxy, system, planet, name, type, distanceFromSun, minutesInDay, minutesInYear, axialTilt, diameter):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.areaList = []

        self.name = name
        self.keyList = []
        appendKeyList(self.keyList, self.name["String"].lower())

        self.type = type
        self.position = [0, 0]
        self.distanceFromSun = distanceFromSun
        self.orbit = "Counter Clockwise"
        self.axialTilt = axialTilt
        self.diameter = diameter

        self.minutesInDay = minutesInDay
        self.minutesInYear = minutesInYear

        self.currentMinutesInYear = 0
        self.currentMinutesInDay = 0

        self.dawnPercent = 0; self.sunrisePercent = 0; self.noonPercent = 0; self.duskPercent = 0; self.sunsetPercent = 0
        self.dawnMessage = False; self.sunriseMessage = False; self.noonMessage = False; self.duskMessage = False; self.sunsetMessage = False

        if self.type == "Planet":
            self.currentMinutesInYear = random.randrange(self.minutesInYear)
            self.currentMinutesInDay = self.currentMinutesInYear % self.minutesInDay

    def createContinent(self, galaxyList, size):
        areaNum = len(self.areaList)
        areaName = {"String":"Continent " + str(areaNum + 1), "Code":"10w" + str(len(str(areaNum)))}
        areaContinent = Area(areaNum, areaName)
        areaContinent.size = size
        
        # Dirt, Beach & Water #
        for y in range(size[1]):
            for x in range(size[0]):
                if not circleCircleCollide([x, y], 1, [int(size[0] / 2), int(size[1] / 2)], int(size[0] * .365)):
                    terrainType = "Water"
                elif not circleCircleCollide([x, y], 1, [int(size[0] / 2), int(size[1] / 2)], int(size[0] * .315)):
                    terrainType = "Beach"
                else:
                    terrainType = "Dirt"

                roomNum = (y * size[0]) + x
                roomName = {"String":terrainType, "Code":str(len(terrainType)) + "w"}
                targetRoom = Room(self.galaxy, self.system, self.planet, areaNum, roomNum, roomName)
                targetRoom.terrainType = terrainType
                targetRoom.mapCoordinates = [x, y]
                areaContinent.roomList.append(targetRoom)

                # Exits #
                if y > 0:
                    targetRoom.exit["North"] = [self.galaxy, self.system, self.planet, areaNum, roomNum - size[0]]
                if x < size[0] - 1:
                    targetRoom.exit["East"] = [self.galaxy, self.system, self.planet, areaNum, roomNum + 1]
                if y < size[1] - 1:
                    targetRoom.exit["South"] = [self.galaxy, self.system, self.planet, areaNum, roomNum + size[0]]
                if x > 0:
                    targetRoom.exit["West"] = [self.galaxy, self.system, self.planet, areaNum, roomNum - 1]

        # Create RoomNumMap #
        areaContinent.roomNumMap = []
        for x in range(size[0]):
            areaContinent.roomNumMap.append([])
            for y in range(size[1]):
                areaContinent.roomNumMap[-1].append((y * size[1]) + x)

        self.areaList.append(areaContinent)

    def createContinent2(self, galaxyList, size):
        areaNum = len(self.areaList)
        areaName = {"String":"Continent " + str(areaNum + 1), "Code":"10w" + str(len(str(areaNum)))}
        areaContinent = Area(areaNum, areaName)
        areaContinent.size = size
        
        renderRange = 1
        for renderIndex in range(renderRange):
            simplexBase = opensimplex.OpenSimplex(random.randrange(2560))
            simplexDetail = opensimplex.OpenSimplex(random.randrange(2560))
            simplexFine = opensimplex.OpenSimplex(random.randrange(2560))
        
            for y in range(size[1]):
                for x in range(size[0]):
                    roomNum = (y * size[0]) + x
                
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
                            
                    # Assign Data #
                    if renderIndex == 0:
                        roomName = {"String":terrainType, "Code":str(len(terrainType)) + "w"}
                        newRoom = Room(self.galaxy, self.system, self.planet, areaNum, roomNum, roomName)
                        newRoom.mapCoordinates = [x, y]
                        newRoom.terrainType = terrainType
                        areaContinent.roomList.append(newRoom)
                    elif terrainType != None:
                        targetRoom = areaContinent.roomList[roomNum]
                        if not (renderIndex in [1, 2, 3] and targetRoom.terrainType == "Water"):
                            targetRoom.terrainType = terrainType
                        
                    # Round Edges #
                    if renderIndex == 3 or renderRange == 1:
                        if renderRange == 1:
                            targetRoom = newRoom
                        else:
                            targetRoom = areaContinent.roomList[roomNum]
                        if not circleCircleCollide([x, y], 1, [int(size[0] / 2), int(size[1] / 2)], int(size[0] * .365)):
                            if targetRoom.terrainType not in ["Water", "Mountain"]:
                                terrainType = "Beach"
                                targetRoom.terrainType = terrainType
                                targetRoom.name = {"String":terrainType, "Code":str(len(terrainType)) + "w"}
                        if not circleCircleCollide([x, y], 1, [int(size[0] / 2), int(size[1] / 2)], int(size[0] * .37)):
                            terrainType = "Water"
                            targetRoom.terrainType = terrainType
                            targetRoom.name = {"String":terrainType, "Code":str(len(terrainType)) + "w"}
                            
                    # Set Room Data #
                    if renderIndex == 3:
                        targetRoom = areaContinent.roomList[roomNum]
                        if targetRoom.terrainType == "Water" : targetRoomName = {"String":"In The Ocean", "Code":"12w"}
                        elif targetRoom.terrainType == "Beach" : targetRoomName = {"String":"On A Beach", "Code":"10w"}
                        elif targetRoom.terrainType == "Grass" : targetRoomName = {"String":"Grasslands", "Code":"10w"}
                        elif targetRoom.terrainType == "Desert" : targetRoomName = {"String":"In A Desert", "Code":"11w"}
                        elif targetRoom.terrainType == "Mountain" : targetRoomName = {"String":"Climbing A Mountain", "Code":"19w"}
                        targetRoom.name = targetRoomName

                        #targetRoom.mapElevationValue = 0.0
                        #elevationValue = 1.0 - heightValue
                        #newRoom.mapElevationValue = elevationValue # Shadow Effect On Map #
                            
                    # Debug Line #
                    if areaContinent.roomList[roomNum].terrainType != "Water":
                        areaContinent.roomList[roomNum].terrainType = "Dirt"

                    # Exits #
                    if renderIndex == 3 or renderRange == 1:
                        if renderRange == 1:
                            targetRoom = newRoom

                        if y > 0:
                            targetRoom.exit["North"] = [self.galaxy, self.system, self.planet, areaNum, roomNum - size[0]]
                        if x < size[0] - 1:
                            targetRoom.exit["East"] = [self.galaxy, self.system, self.planet, areaNum, roomNum + 1]
                        if y < size[1] - 1:
                            targetRoom.exit["South"] = [self.galaxy, self.system, self.planet, areaNum, roomNum + size[0]]
                        if x > 0:
                            targetRoom.exit["West"] = [self.galaxy, self.system, self.planet, areaNum, roomNum - 1]

        # Create RoomNumMap #
        areaContinent.roomNumMap = []
        for x in range(size[0]):
            areaContinent.roomNumMap.append([])
            for y in range(size[1]):
                areaContinent.roomNumMap[-1].append((y * size[1]) + x)

        self.areaList.append(areaContinent)

    def update(self, galaxyList, player, console):
        self.currentMinutesInDay += 1
        self.currentMinutesInYear += 1

        # Sunrise/Sunset Messages #
        if self.type == "Planet" and self.galaxy == player.galaxy and self.system == player.system and self.planet == player.planet:
            playerRoom = Room.exists(galaxyList, player.spaceship, player.galaxy, player.system, player.planet, player.area, player.room)
            if playerRoom != None and not (playerRoom.spaceshipObject != None and playerRoom.spaceshipObject.landedLocation == None):
                dayPercent = 0.0
                if self.minutesInDay != 0:
                    dayPercent = self.currentMinutesInDay / self.minutesInDay

                if dayPercent >= self.dawnPercent and self.dawnMessage == False:
                    self.dawnMessage = True
                    console.write("The sky begins to lighten.", "4w1dc2ddc11w1dw6ddw1y", True)
                elif dayPercent >= self.sunrisePercent and self.sunriseMessage == False:
                    self.sunriseMessage = True
                    console.write("The sun rises over the horizon.", "4w1dy2ddy16w1dw6ddw1y", True)
                elif dayPercent >= self.noonPercent and self.noonMessage == False:
                    self.noonMessage = True
                    console.write("It's noon.", "2w1y6w1y", True)
                elif dayPercent >= self.duskPercent and self.duskMessage == False:
                    self.duskMessage = True
                    console.write("The sun begins to set.", "4w1dy2ddy11w1dw2ddw1y", True)
                elif dayPercent >= self.sunsetPercent and self.sunsetMessage == False:
                    self.sunsetMessage = True
                    console.write("The sun sinks beyond the horizon.", "4w1dy2ddy18w1dw6ddw1y", True)

        self.updatePosition()
        if self.currentMinutesInDay >= self.minutesInDay:
            self.currentMinutesInDay = 0
            self.updateNightDayTimers()

    def updateNightDayTimers(self):
        yearRatio = 0
        if self.minutesInYear != 0:
            yearRatio = math.cos(math.radians(((self.currentMinutesInYear) / (self.minutesInYear)) * 360))
        ratio = ((self.axialTilt / 100.0) * yearRatio) * (self.minutesInDay / 2.50)
        nightMinutes = self.minutesInDay - ((self.minutesInDay / 1.9) - ratio)
        
        self.dawnPercent = (nightMinutes / 2.01) / self.minutesInDay
        self.sunrisePercent = (nightMinutes / 1.80) / self.minutesInDay
        self.noonPercent = .5
        self.duskPercent = ((nightMinutes / 1.94) + (self.minutesInDay - nightMinutes)) / self.minutesInDay
        self.sunsetPercent = ((nightMinutes / 1.64) + (self.minutesInDay - nightMinutes)) / self.minutesInDay

        self.dawnMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.dawnPercent
        self.sunriseMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.sunrisePercent
        self.noonMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.noonPercent
        self.duskMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.duskPercent
        self.sunsetMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.sunsetPercent

        # sunriseTime = (self.sunrisePercent * self.minutesInDay)
        # sunriseString = str(int(sunriseTime / 60)) + ":" + str(int(sunriseTime % 60))
        # sunsetTime = (self.sunsetPercent * self.minutesInDay)
        # sunsetString = str(int(sunsetTime / 60)) + ":" + str(int(sunsetTime % 60))
        # dawnTime = (self.dawnPercent * self.minutesInDay)
        # dawnString = str(int(dawnTime / 60)) + ":" + str(int(dawnTime % 60))
        # duskTime = (self.duskPercent * self.minutesInDay)
        # duskString = str(int(duskTime / 60)) + ":" + str(int(duskTime % 60))
        # print("Dawn: ", dawnString)
        # print("Sunrise: ", sunriseString)
        # print("Dusk: ", duskString)
        # print("SunSet: ", sunsetString)

    def updatePosition(self):
        x = self.distanceFromSun
        y = 0
        orbitMod = 1
        if self.orbit == "Clockwise":
            orbitMod = -1

        if self.minutesInYear != 0:
            x = math.cos(math.radians((self.currentMinutesInYear / self.minutesInYear) * 360)) * self.distanceFromSun
            y = ((math.sin(math.radians((self.currentMinutesInYear / self.minutesInYear) * 360)) * self.distanceFromSun) / 1.4) * orbitMod
        
        self.position = [x, y]

    def dayCheck(self):
        if self.type == "Star":
            dayCheck = True
        else:
            dayCheck = (self.currentMinutesInDay / self.minutesInDay) >= self.dawnPercent and (self.currentMinutesInDay / self.minutesInDay) < self.sunsetPercent 

        return dayCheck
        
    def getLandingRoomDataList(self):
        landingRoomDataList = []
        for area in self.areaList:
            for room in area.roomList:
                if "Landing Site" in room.flags:
                    landingRoomDataList.append({"Area":area, "Room":room})
        return landingRoomDataList

    def getDrawColor(self):
        if self.type == "Star":
            return [200, 150, 0]
        elif self.diameter > 10000:
            return [150, 0, 150]
        elif self.diameter > 3500:
            return [0, 0, 150]
        else:
            return [150, 0, 0]

    def getDrawRadius(self):
        if self.type == "Star":
            return 12
        elif self.diameter >= 10000:
            return 9
        elif self.diameter >= 3500:
            return 6
        else:
            return 4
