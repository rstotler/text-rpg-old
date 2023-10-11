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
        
        self.speed = 0
        self.speedMod = 0

        self.launchTick = -1
        self.launchTickMax = 1
        self.launchPhase = 3

        self.buildSpaceship(galaxyList)

    def update(self, console, galaxyList, player):

        # Launch Spaceship #
        if self.launchTick > -1:
            self.launch(console, galaxyList)

        # Move In Orbit #
        if self.planet != None:
            orbitingPlanet = galaxyList[self.galaxy].systemList[self.system].planetList[self.planet]
            self.position = orbitingPlanet.position

        # Move Out Of Orbit #
        elif self.planet == None and (self.speedMod != 0 or self.speed != 0):
            if self.targetPlanet != None:
                self.course = self.targetPlanet.position

            # Speed Modulator #
            if self.speed != self.speedMod:
                if self.speed < self.speedMod:
                    if player.spaceship == self.num and self.speed == 4:
                        console.write("The ship lurches slightly as it begins to move.", "46w1y", True)
                    self.speed += 2
                    if self.speed > self.speedMod:
                        self.speed = self.speedMod
                elif self.speed > self.speedMod:
                    self.speed -= 2
                    if self.speed < self.speedMod:
                        self.speed = self.speedMod

            if self.speed > 0:
                pass

    def launch(self, console, galaxyList):
        self.launchTick += 1
        if self.launchTick >= self.launchTickMax:
            self.launchTick = 0
            self.launchPhase += 1

            if self.launchPhase == 1:
                console.write("The ship rumbles as the engines start up.", "40w1y", True)
            elif self.launchPhase == 2:
                console.write("The engines roar as you blast off!", "33w1y", True)
            elif self.launchPhase == 3:
                console.write("The ship rumbles as it makes its fiery ascent.", "45w1y", True)

            elif self.launchPhase == 4:
                self.launchTick = -1
                targetPlanet = galaxyList[self.galaxy].systemList[self.system].planetList[self.planet]
                displayString = "You begin orbiting " + targetPlanet.name["String"] + "."
                displayCode = "19w" + targetPlanet.name["Code"] + "1y"
                console.write(displayString, displayCode, True)
    
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

        shipArea0 = Area(0)
        self.areaList.append(shipArea0)
        shipArea0.name = {"String":"Ship Area 1"}
        
        shipRoom00 = Room(None, None, None, 0, 0)
        shipArea0.roomList.append(shipRoom00)
        shipRoom00.name = {"String":"Ship Cockpit"}
        shipRoom00.exit["South"] = [0, 1]

        shipRoom01 = Room(None, None, None, 0, 1)
        shipArea0.roomList.append(shipRoom01)
        shipRoom01.name = {"String":"Ship Hallway"}
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
