from GameData.World.Area import Area
from GameData.World.Room import Room
from Components.Utility import appendKeyList

class Spaceship:
    numCount = 0

    def __init__(self, galaxyList, name, password, landedLocation, hatchLocation=[0, 0], exitLocation=[0, 0], cockpitLocation=[0, 0]):
        self.galaxy = landedLocation[0]
        self.system = landedLocation[1]
        self.planet = landedLocation[2]
        self.num = Spaceship.generateNum()
        self.flags = {}

        self.name = name
        self.keyList = []
        self.areaList = []
        self.exitLocation = exitLocation

        self.password = password
        self.hatchLocation = hatchLocation
        self.cockpitLocation = cockpitLocation
        self.landedLocation = [landedLocation[3], landedLocation[4]]

        self.position = [0, 0]
        self.course = None
        self.targetPlanet = None
        self.lastPlanet = None

        self.clearCourseCheck = False
        self.displaySpeedUpMessage = False
        self.displaySlowDownMessage = False
        
        self.speedPercent = 0
        self.speedMod = 0
        self.topSpeed = 2500

        self.launchLandAction = None
        self.launchLandTick = -1
        self.launchLandTickMax = 4
        self.launchLandPhase = 0

        self.buildSpaceship(galaxyList)

    def update(self, console, galaxyList, player):

        # Launch/Land Spaceship #
        if self.launchLandTick > -1 and self.launchLandAction == "Launch":
            self.launch(console, galaxyList)
        elif self.launchLandTick > -1 and self.launchLandAction == "Land":
            self.land(console, galaxyList)

        # Speed Modulator #
        if self.speedPercent != self.speedMod:
            if self.speedPercent < self.speedMod:
                if player.spaceship == self.num and self.displaySpeedUpMessage != False:
                    if self.displaySpeedUpMessage < 2:
                        self.displaySpeedUpMessage += 1
                    else:
                        console.write("The ship lurches slightly as it increases speed.", "47w1y", True)
                        self.displaySpeedUpMessage = False
                self.speedPercent += 2
                if self.speedPercent > self.speedMod:
                    self.speedPercent = self.speedMod
                if player.spaceship == self.num and self.speedPercent == self.speedMod:
                    console.write("The engine sounds normalize as the ship reaches its target speed.", "64w1y", True)
            elif self.speedPercent > self.speedMod:
                if player.spaceship == self.num and self.displaySlowDownMessage != False:
                    if self.displaySlowDownMessage < 2:
                        self.displaySlowDownMessage += 1
                    else:
                        console.write("You feel the ship slow down.", "27w1y", True)
                        self.displaySlowDownMessage = False
                self.speedPercent -= 4
                if self.speedPercent < self.speedMod:
                    self.speedPercent = self.speedMod
                if player.spaceship == self.num:
                    if self.speedPercent == 0:
                        console.write("The electronic hum stops as the ships engines power down.", "56w1y", True)
                    elif self.speedPercent == self.speedMod:
                        console.write("The engine sounds normalize as the ship reaches its top speed.", "61w1y", True)

        # Move In Orbit #
        if self.planet != None:
            orbitingPlanet = galaxyList[self.galaxy].systemList[self.system].planetList[self.planet]
            self.position = orbitingPlanet.position

        # Move Out Of Orbit #
        elif self.planet == None:
            self.move(console, galaxyList, player)

        # Clear Course Check #
        if self.speedPercent == 0 and self.clearCourseCheck == True:
            self.course = None
            self.targetPlanet = None
            self.clearCourseCheck = False

    def launch(self, console, galaxyList):
        self.launchLandTick += 1
        if self.launchLandTick >= self.launchLandTickMax:
            self.launchLandTick = 0
            self.launchLandPhase += 1

            if self.launchLandPhase == 1:
                console.write("The ship rumbles as the engines start up.", "40w1y", True)
            elif self.launchLandPhase == 2:
                console.write("The engines roar as you blast off!", "33w1y", True)
            elif self.launchLandPhase == 3:
                console.write("The ship rumbles as it makes its fiery ascent.", "45w1y", True)

            elif self.launchLandPhase == 4:
                targetPlanet = galaxyList[self.galaxy].systemList[self.system].planetList[self.planet]
                self.launchLandAction = None
                self.launchLandTick = -1
                self.lastPlanet = targetPlanet

                displayString = "You begin orbiting " + targetPlanet.name["String"] + "."
                displayCode = "19w" + targetPlanet.name["Code"] + "1y"
                console.write(displayString, displayCode, True)
    
    def land(self, console, galaxyList):
        self.launchLandTick += 1
        if self.launchLandTick >= self.launchLandTickMax:
            self.launchLandTick = 0
            self.launchLandPhase += 1

            if self.launchLandPhase == 1:
                console.write("You feel a sense of weightlessness as you begin your descent.", "60w1y", True)
            elif self.launchLandPhase == 2:
                console.write("The ship rumbles as it descends toward the plant.", "48w1y", True)
            elif self.launchLandPhase == 3:
                console.write("The ship begins to slow down as it approaches the landing pad.", "61w1y", True)

            elif self.launchLandPhase == 4:
                targetPlanet = galaxyList[self.galaxy].systemList[self.system].planetList[self.planet]
                self.launchLandAction = None
                self.launchLandTick = -1
                if "Target Landing Location" in self.flags:
                    self.landedLocation = self.flags["Target Landing Location"]
                    del self.flags["Target Landing Location"]
                else:
                    self.landedLocation = [targetPlanet.getLandingRoomDataList[0]["Area"].num, targetPlanet.getLandingRoomDataList[0]["Room"].room]
                targetPlanet.areaList[self.landedLocation[0]].roomList[self.landedLocation[1]].spaceshipList.append(self)
                console.write("You feel a slight thud as the ship lands.", "40w1y", True)

    def move(self, console, galaxyList, player):
        if self.targetPlanet != None:
            self.course = self.targetPlanet.position

        if self.speedPercent > 0:
            moveSpeed = self.topSpeed * (self.speedPercent / 100.0)
            distance = [self.course[0] - self.position[0], self.course[1] - self.position[1]]
            slope = distance[0] / distance[1]
            counterSlope = 1.0 - abs(slope)
            if abs(slope) > 1.0:
                counterSlope = 1.0 / slope
                slope = 1.0

            if self.position[0] < self.course[0] : self.position[0] += moveSpeed * abs(slope)
            else : self.position[0] -= moveSpeed * abs(slope)
            if self.position[1] < self.course[1] : self.position[1] += moveSpeed * abs(counterSlope)
            else : self.position[1] -= moveSpeed * abs(counterSlope)

            for planet in galaxyList[self.galaxy].systemList[self.system].planetList:
                if planet != self.lastPlanet:
                    if abs(self.position[0] - planet.position[0]) <= (moveSpeed * 1.25):
                        if abs(self.position[1] - planet.position[1]) <= (moveSpeed * 1.25):
                            self.planet = planet.planet
                            self.course = None
                            self.targetPlanet = None
                            self.speedMod = 0
                            if self.speedPercent > 0:
                                self.displaySlowDownMessage = 1
                                self.displaySpeedUpMessage = False
                            if player.spaceship == self.num:
                                player.planet = planet.planet
                            for area in self.areaList:
                                for room in area.roomList:
                                    for mob in room.mobList:
                                        mob.planet = planet.planet
                            console.write("You being orbiting " + planet.name["String"] + ".", "19w" + planet.name["Code"] + "1y", True)
                            break

    def getRoom(self, area, room):
        if area <= len(self.areaList):
            if isinstance(room, int) and room <= len(self.areaList[area].roomList):
                return self.areaList[area].roomList[room]

        return None

    def lookDescription(self, console):
        console.lineList.insert(0, {"Blank": True})
        console.lineList.insert(0, {"String": "You look at " + self.name["String"] + ".", "Code":"12w" + self.name["Code"] + "1y"})
        console.lineList.insert(0, {"String": "You see nothing special.", "Code":"23w1y"})

    def buildSpaceship(self, galaxyList):
        targetPlanet = galaxyList[self.galaxy].systemList[self.system].planetList[self.planet]
        self.position = targetPlanet.position

        appendKeyList(self.keyList, self.name["String"].lower())
        appendKeyList(self.keyList, "spaceship")

        shipArea0Name = {"String":"Ship Area 1"}
        shipArea0 = Area(0, shipArea0Name)
        self.areaList.append(shipArea0)
        
        shipRoom00Name = {"String":"Ship Cockpit"}
        shipRoom00 = Room(None, None, None, 0, 0, shipRoom00Name)
        shipArea0.roomList.append(shipRoom00)
        shipRoom00.exit["South"] = [0, 1]

        shipRoom01Name = {"String":"Ship Hallway"}
        shipRoom01 = Room(None, None, None, 0, 1, shipRoom01Name)
        shipArea0.roomList.append(shipRoom01)
        shipRoom01.exit["North"] = [0, 0]

        for area in self.areaList:
            for room in area.roomList:
                for exitDir in room.exit:
                    if room.exit[exitDir] != None and len(room.exit[exitDir]) == 2:
                        room.exit[exitDir].insert(0, self.num)
                room.inside = True
                room.spaceshipObject = self
                if room.area == self.cockpitLocation[0] and room.room == self.cockpitLocation[1]:
                    room.flags["Cockpit"] = True
        for exitDir in ["West", "South", "North", "East"]:
            if self.areaList[self.exitLocation[0]].roomList[self.exitLocation[1]].exit[exitDir] == None:
                targetExitRoom = self.areaList[self.exitLocation[0]].roomList[self.exitLocation[1]]
                targetExitRoom.exit[exitDir] = "Spaceship Exit"
                targetExitRoom.installDoor(galaxyList, exitDir, "Automatic", None, "Closed", True)
                break
        shipArea0.zeroCoordinates(galaxyList)

        shipRoom00.installDoor(galaxyList, "South", "Automatic", self.password)
        shipRoom00.lockUnlockDoor(galaxyList, "Lock", "South")

    @staticmethod
    def generateNum():
        Spaceship.numCount += 1
        return Spaceship.numCount
