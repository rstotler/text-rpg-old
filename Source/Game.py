import pygame, random
from pygame import *
from Screen.Console import Console
from Screen.InputBar import InputBar
from Screen.Map import Map
from Components.Keyboard import Keyboard
from GameData.Player import Player
from GameData.Skill import Skill
from GameData.World.Galaxy import Galaxy
from GameData.World.SolarSystem import SolarSystem
from GameData.World.Planet import Planet
from GameData.World.Area import Area
from GameData.World.Room import Room
from GameData.World.Spaceship import Spaceship
from GameData.Item import Item
from GameData.Action import Action
from Components.Utility import stringIsNumber
from Components.Utility import appendKeyList

# To Do List:
    # Basic Mob Speech
    # Implement wordWrap()
    # Combat:
    # -Time-Based Action
    # -Auto-Reload
    # -Mobs Counter-Attack
    # Make Player Lose Sight Of Mobs On Darkness
    # Mob Updates/Movement
    # Attack Command
    # Dodge Command
    # Parry Command
    # Fix Map Doors (Active Map)
    # Auto-Loot
    # Counter-Attack (Passive Skill)

class Game:

    def __init__(self):
        self.keyboard = Keyboard()
        self.console = Console()
        self.inputBar = InputBar()
        self.map = Map()

        self.player = Player(0, 0, 1, 0, 1, None, None)
        self.galaxyList = []

        self.frameTick = 0
        
        self.loadGame()
        # self.inputBar.inputList = ["n", "w", "loot cab", "wear pis", "wear pis", "e", "s", "s", "reload"]
        
    def loadGame(self):
        galaxyProtoMilkyWay = Galaxy()
        self.galaxyList.append(galaxyProtoMilkyWay)
        galaxyProtoMilkyWay.name = {"String":"Proto Milky Way"}

        # (System) Proto Sol #
        if True:
            systemProtoSol = SolarSystem()
            galaxyProtoMilkyWay.systemList.append(systemProtoSol)
            systemProtoSol.name = {"String":"Proto Sol"}

            starProtoSol = Planet(0, 0, 0, 0, 38880, 0)
            systemProtoSol.planetList.append(starProtoSol)
            starProtoSol.name = {"String":"Proto Sol"}
            starProtoSol.type = "Star"
            starProtoSol.axialTilt = 6

            areaLimbo = Area(0)
            starProtoSol.areaList.append(areaLimbo)
            areaLimbo.name = {"String":"Limbo"}

            roomLimbo = Room(0, 0, 0, 0, 0)
            areaLimbo.roomList.append(roomLimbo)
            roomLimbo.name = {"String":"Limbo"}

            planetProtoEarth = Planet(0, 0, 1, 93456, 1440, 525600)
            systemProtoSol.planetList.append(planetProtoEarth)
            planetProtoEarth.name = {"String":"Proto Earth"}
            planetProtoEarth.axialTilt = 23.5
            
            planetProtoEarth.currentMinutesInDay = 480
            planetProtoEarth.currentMinutesInYear = 480
            planetProtoEarth.updateNightDayTimers()
            planetProtoEarth.updateLocation()

        # (Area) Center of the Universe #
        if True:
            areaCOTU = Area(0)
            planetProtoEarth.areaList.append(areaCOTU)
            areaCOTU.name = {"String":"Center of the Universe"}

            roomCOTU00 = Room(0, 0, 1, 0, 0)
            areaCOTU.roomList.append(roomCOTU00)
            roomCOTU00.name = {"String":"Center of the Universe", "Code":"1w1ddw1da2dw2da1dw2ddw1da1dw1w2w2dw2ddw1da2ddw"}
            roomCOTU00.exit["South"] = [0, 0, 1, 0, 1]
            roomCOTU00.exit["North"] = [0, 0, 1, 0, 3]
            roomCOTU00.description = [{"String":"You stand on a large floating platform at the Center of the", "Code":"46w1w1ddw1da2dw2da1dw2ddw1da1dw1w"},
                                    {"String":"Universe. Billions of multi-colored stars twinkle and flash", "Code":"1w2dw2ddw1da2ddw2y13w1dc1c1ddc1w1y1r1dr1do1o1y1dy1ddy7w1c1dc1ddc2dc1c1ddc5w1c1dc1ddc1dc1c"},
                                    {"String":"from ages past. You see a bridge leading to the Spaceport", "Code":"14w2y32w1w1dw2ddw1dw1w1dw1ddw1dw"},
                                    {"String":"to the South and a garden to the North.", "Code":"7w1w5ddw6w1g1dg1ddg1g1dg1ddg8w1w4ddw1y"}]
            
            roomCOTU01 = Room(0, 0, 1, 0, 1)
            areaCOTU.roomList.append(roomCOTU01)
            roomCOTU01.name = {"String":"Bridge To The Spaceport", "Code":"14w1w1dw2ddw1dw1w1dw1ddw1dw"}
            roomCOTU01.exit["North"] = [0, 0, 1, 0, 0]
            roomCOTU01.exit["South"] = [0, 0, 1, 0, 2]
            roomCOTU01.mobList.append(Player(0, 0, 1, 0, 1, None, 1))

            roomCOTU02 = Room(0, 0, 1, 0, 2)
            areaCOTU.roomList.append(roomCOTU02)
            roomCOTU02.name = {"String":"Spaceport Entrance", "Code":"1w1dw2ddw1dw1w1dw1ddw1dw9w"}
            roomCOTU02.exit["North"] = [0, 0, 1, 0, 1]
            roomCOTU02.exit["South"] = [0, 0, 1, 0, 5]
            roomCOTU02.inside = True

            roomCOTU03 = Room(0, 0, 1, 0, 3)
            areaCOTU.roomList.append(roomCOTU03)
            roomCOTU03.name = {"String":"A Peaceful Garden", "Code":"2w1w1dw2ddw1dw1w1ddw1da1w1g1dg1ddg1g1dg1ddg"}
            roomCOTU03.exit["South"] = [0, 0, 1, 0, 0]
            roomCOTU03.exit["West"] = [0, 0, 1, 0, 4]

            roomCOTU04 = Room(0, 0, 1, 0, 4)
            areaCOTU.roomList.append(roomCOTU04)
            roomCOTU04.name = {"String":"A Little Wooden Shack", "Code":"9w1do1ddo1dddo1do1ddo1dddo6w"}
            roomCOTU04.exit["East"] = [0, 0, 1, 0, 3]
            roomCOTU04.inside = True
            roomCOTU04.itemList.append(Item(904))
            ornateChest = Item(902)
            roomCOTU04.itemList.append(ornateChest)
            ornateChest.containerList.append(Item(901))
            for i in range(1, 14):
                ornateChest.containerList.append(Item(i))
            ornateChest.containerList.append(Item(14))
            weaponsCabinet = Item(903)
            roomCOTU04.itemList.append(weaponsCabinet)
            for i in range(101, 105):
                weaponsCabinet.containerList.append(Item(i))
                weaponsCabinet.containerList.append(Item(i))
            weaponsCabinet.containerList.append(Item(105))
            weaponsCabinet.containerList.append(Item(106))
            weaponsCabinet.containerList.append(Item(107))
            weaponsCabinet.containerList.append(Item(108))
            weaponsCabinet.containerList.append(Item(108))
            weaponsCabinet.containerList.append(Item(109))
            weaponsCabinet.containerList.append(Item(201))
            weaponsCabinet.containerList.append(Item(202))
            weaponsCabinet.containerList.append(Item(201))
            weaponsCabinet.containerList.append(Item(202))
            weaponsCabinet.containerList.append(Item(203, 50))
            weaponsCabinet.containerList.append(Item(204, 50))
            weaponsCabinet.containerList.append(Item(208, 25))
            weaponsCabinet.containerList.append(Item(205, 25))
            weaponsCabinet.containerList.append(Item(207, 10))
            weaponsCabinet.containerList.append(Item(206, 40))
            weaponsCabinet.containerList.append(Item(209))
            weaponsCabinet.containerList.append(Item(210, 25))

            roomCOTU05 = Room(0, 0, 1, 0, 5)
            areaCOTU.roomList.append(roomCOTU05)
            roomCOTU05.name = {"String":"COTU Landing Pad"}
            roomCOTU05.exit["North"] = [0, 0, 1, 0, 2]

            # Zero Area Coordinates #
            areaCOTU.zeroCoordinates(self.galaxyList)

        # Debug Spaceship #
        if True:
            cotuTransportShip = Spaceship(0, 0, 1, "COTU Spaceport", [0, 1], [[0, 1]])
            roomCOTU05.spaceshipList.append(cotuTransportShip)
            systemProtoSol.spaceshipList.append(cotuTransportShip)
            cotuTransportShip.name = {"String":"COTU Transport Ship", "Code":"19w"}
            appendKeyList(cotuTransportShip.keyList, cotuTransportShip.name["String"].lower())
            appendKeyList(cotuTransportShip.keyList, "spaceship")

            cotuTransportShipArea0 = Area(0)
            cotuTransportShip.areaList.append(cotuTransportShipArea0)
            cotuTransportShipArea0.name = {"String":"Debug Ship"}
            
            cotuTransportShipRoom00 = Room(None, None, None, 0, 0)
            cotuTransportShipArea0.roomList.append(cotuTransportShipRoom00)
            cotuTransportShipRoom00.name = {"String":"Ship Cockpit"}
            cotuTransportShipRoom00.exit["South"] = [0, 1]

            cotuTransportShipRoom01 = Room(None, None, None, 0, 1)
            cotuTransportShipArea0.roomList.append(cotuTransportShipRoom01)
            cotuTransportShipRoom01.name = {"String":"Ship Hallway"}
            cotuTransportShipRoom01.exit["North"] = [0, 0]

            # Spaceship Setup #
            cotuTransportShip.landedLocation = [0, 0, 1, 0, 5]
            for area in cotuTransportShip.areaList:
                for room in area.roomList:
                    for exitDir in room.exit:
                        if room.exit[exitDir] != None and len(room.exit[exitDir]) == 2:
                            room.exit[exitDir].insert(0, cotuTransportShip.num)
                    room.inside = True
                    room.spaceshipObject = cotuTransportShip
            for spaceshipExit in cotuTransportShip.exitList:
                for exitDir in ["West", "South", "North", "East"]:
                    if cotuTransportShip.areaList[spaceshipExit[0]].roomList[spaceshipExit[1]].exit[exitDir] == None:
                        targetExitRoom = cotuTransportShip.areaList[spaceshipExit[0]].roomList[spaceshipExit[1]]
                        targetExitRoom.exit[exitDir] = "Spaceship Exit"
                        targetExitRoom.installDoor(self.galaxyList, exitDir, "Automatic", None, "Closed", True)
                        break
            cotuTransportShipArea0.zeroCoordinates(self.galaxyList)
            
        # Milky Way & Sol #
        if True:
            galaxyMilkyWay = Galaxy()
            self.galaxyList.append(galaxyMilkyWay)
            galaxyMilkyWay.name = {"String":"Milky Way"}

            systemSol = SolarSystem()
            galaxyMilkyWay.systemList.append(systemSol)
            systemSol.name = {"String":"Sol"}

            starSol = Planet(1, 1, 0, 0, 38880, 0)
            systemSol.planetList.append(starSol)
            starSol.name = {"String":"Sol"}
            starSol.type = "Star"
            starSol.axialTilt = 6

            planetMercury = Planet(1, 1, 1, 29945, 84960, 126720)
            systemSol.planetList.append(planetMercury)
            planetMercury.name = {"String":"Mercury"}
            
            planetVenus = Planet(1, 1, 2, 67443, 349920, 324000)
            systemSol.planetList.append(planetVenus)
            planetVenus.name = {"String":"Venus"}
            planetVenus.orbit = "Clockwise"
            planetVenus.axialTilt = 3
            
            planetEarth = Planet(1, 1, 3, 93456, 1440, 525600)
            systemSol.planetList.append(planetEarth)
            planetEarth.name = {"String":"Earth"}
            planetEarth.axialTilt = 23.5

            planetMars = Planet(1, 1, 4, 15044, 1477, 989280)
            systemSol.planetList.append(planetMars)
            planetMars.name = {"String":"Mars"}
            planetJupiter = Planet(1, 1, 5, 484000000, 596, 6239520)
            systemSol.planetList.append(planetJupiter)
            planetJupiter.name = {"String":"Jupiter"}
            planetSaturn = Planet(1, 1, 6, 886000000, 634, 15448640)
            systemSol.planetList.append(planetSaturn)
            planetSaturn.name = {"String":"Saturn"}
            planetUranus = Planet(1, 1, 7, 1824000000, 1034, 44189280)
            systemSol.planetList.append(planetUranus)
            planetUranus.name = {"String":"Uranus"}
            planetNeptune = Planet(1, 1, 8, 2779300000, 966, 86673600)
            systemSol.planetList.append(planetNeptune)
            planetNeptune.name = {"String":"Neptune"}
            planetPluto = Planet(1, 1, 9, 3700000000, 9180, 130348800)
            systemSol.planetList.append(planetPluto)
            planetPluto.name = {"String":"Pluto"}

        # Load Doors AFTER ALL Rooms Are Loaded! #
        roomCOTU02.installDoor(self.galaxyList, "North", "Automatic", "COTU Spaceport")
        roomCOTU02.lockUnlockDoor(self.galaxyList, "Lock", "North")
        roomCOTU04.installDoor(self.galaxyList, "East", "Manual", None, "Open")
        cotuTransportShipRoom00.installDoor(self.galaxyList, "South", "Automatic", "COTU Spaceport")
        cotuTransportShipRoom00.lockUnlockDoor(self.galaxyList, "Lock", "South")

        # Load Map #
        playerArea, playerRoom = Room.getAreaAndRoom(self.galaxyList, self.player)
        self.map.loadMap(playerArea)

    def draw(self, window):
        window.fill([0, 0, 0])

        self.console.draw(window)
        self.inputBar.draw(window)
        self.map.draw(window, self.galaxyList, self.player)

    def update(self, window):
        self.processInput()
        self.inputBar.update(self)

        if self.frameTick == 0:
            self.galaxyList[self.player.galaxy].systemList[self.player.system].update(self.galaxyList, self.player, self.console)
        if self.frameTick in [0, 30]:
            playerArea, playerRoom = Room.getAreaAndRoom(self.galaxyList, self.player)
            updateAreaList, updateRoomList = Room.getSurroundingRoomData(self.galaxyList, playerArea, playerRoom, 4)
            for room in updateRoomList:
                for mob in room.mobList:
                    mob.update(self.console, self.galaxyList, self.player, room)

            Action.updateActionCommand(self.console, self.player)
            for updateRoom in updateRoomList:
                for mob in updateRoom.mobList:
                    Action.updateActionCommand(self.console, mob)
                
        self.frameTick += 1
        if self.frameTick >= 60:
            self.frameTick = 0

        self.draw(window)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in [K_LSHIFT, K_RSHIFT]:
                    self.keyboard.shift = True
                elif event.key in [K_LCTRL, K_RCTRL]:
                    self.keyboard.control = True
                elif event.key == K_BACKSPACE:
                    self.keyboard.backspace = True
                elif event.key == K_ESCAPE:
                    raise SystemExit
                elif self.keyboard.control == True and event.key in [K_UP, K_RIGHT, K_DOWN, K_LEFT]:
                    currentRoom = Room.exists(self.galaxyList, self.player.spaceship, self.player.galaxy, self.player.system, self.player.planet, self.player.area, self.player.room)
                    if currentRoom != None:
                        if event.key == K_UP : targetDir = "n"
                        elif event.key == K_RIGHT : targetDir = "e"
                        elif event.key == K_DOWN : targetDir = "s"
                        elif event.key == K_LEFT : targetDir = "w"
                        self.player.moveCheck(self.console, self.map, self.galaxyList, self.player, currentRoom, targetDir)
                else:
                    keyName = pygame.key.name(event.key)
                    self.inputBar.processInput(keyName, self)

            elif event.type == KEYUP:
                if event.key in [K_LSHIFT, K_RSHIFT]:
                    self.keyboard.shift = False
                elif event.key in [K_LCTRL, K_RCTRL]:
                    self.keyboard.control = False
                elif event.key == K_BACKSPACE:
                    self.keyboard.backspace = False
                    self.keyboard.backspaceTick = -1
                
            elif event.type == MOUSEWHEEL:
                x, y = pygame.mouse.get_pos()
                if x >= 600 and y < 200:
                    self.map.moveMouseWheel(-event.y, self.player)
                else:
                    if len(self.inputBar.inputList) == 0:
                        self.console.scroll(self.keyboard, event.y)

            elif event.type == QUIT:
                raise SystemExit

        self.keyboard.update()

    def processInputBarCommand(self, input):
        directionStringList = ["north", "nort", "nor", "no", "n", "east", "eas", "ea", "e", "south", "sout", "sou", "so", "s", "west", "wes", "we", "w"]
        combatSkill, parsedCombatInput = Skill.parseSkillString(input.lower(), self.player.getCombatSkillList())
        currentRoom = Room.exists(self.galaxyList, self.player.spaceship, self.player.galaxy, self.player.system, self.player.planet, self.player.area, self.player.room)
        if currentRoom == None:
            currentRoom = self.galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
        
        ## Basic Commands ##
        # Look/Examine #
        if input.lower().split()[0] in ["look", "loo", "lo", "l", "examine", "examin", "exami", "exam", "exa", "ex"]:
            targetDir = None
            if len(input.split()) > 1:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"]:
                    targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"]:
                    targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"]:
                    targetDir = "South"
                elif input.lower().split()[1] in ["west", "wes", "we", "w"]:
                    targetDir = "West"
            
            # Look 'Direction' #
            if len(input.split()) == 2 and targetDir != None:
                self.player.lookDirection(self.console, self.galaxyList, currentRoom, targetDir, 1)

            # Look 'Direction' '#' #
            elif len(input.split()) == 3 and targetDir != None and stringIsNumber(input.split()[2]) and int(input.split()[2]) > 0:
                self.player.lookDirection(self.console, self.galaxyList, currentRoom, targetDir, int(input.split()[2]))

            # Look 'Direction' '#' Item/Mob/Spaceship #
            elif len(input.split()) > 3 and input.lower().split()[1] in directionStringList and stringIsNumber(input.split()[2]) and int(input.split()[2]) > 0:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"] : targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"] : targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"] : targetDir = "South"
                else : targetDir = "West"
                lookTarget = ' '.join(input.lower().split()[3::])
                self.player.lookTargetCheck(self.console, self.galaxyList, currentRoom, targetDir, int(input.split()[2]), lookTarget)

            # Look 'Direction' Item/Mob/Spaceship #
            elif len(input.split()) > 2 and input.lower().split()[1] in directionStringList:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"] : targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"] : targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"] : targetDir = "South"
                else : targetDir = "West"
                lookTarget = ' '.join(input.lower().split()[2::])
                self.player.lookTargetCheck(self.console, self.galaxyList, currentRoom, targetDir, 1, lookTarget)

            # Look Item In Container #
            elif len(input.split()) > 3 and "in" in input.lower().split() and input.lower().split()[1] != "in" and input.lower().split()[-1] != "in":
                inIndex = input.lower().split().index("in")
                targetItemKey = ' '.join(input.lower().split()[1:inIndex])
                targetContainerKey = ' '.join(input.lower().split()[inIndex + 1::])
                self.player.lookItemInContainerCheck(self.console, currentRoom, targetItemKey, targetContainerKey)

            # Look Item/Mob/Spaceship/Inventory/Gear #
            elif len(input.split()) > 1:
                lookTarget = ' '.join(input.lower().split()[1::])
                self.player.lookTargetCheck(self.console, self.galaxyList, currentRoom, None, None, lookTarget)

            # Look #
            elif len(input.split()) == 1 and input.lower().split()[0] in ["look", "loo", "lo", "l"]:
                self.console.lineList.insert(0, {"Blank": True})
                currentRoom.display(self.console, self.galaxyList, self.player)

            # Examine #
            elif len(input.split()) == 1 and len(self.player.targetList) > 0:
                self.player.targetList[0].lookDescription(self.console)
                
            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Examine what?", "Code":"12w1y"})

        # Target #
        elif input.lower().split()[0] in ["target", "targe", "targ", "tar", "ta", "t"]:

            # Target All Mob 'Direction' '#' #
            if len(input.split()) > 4 and input.lower().split()[1] == "all" and input.lower().split()[-2] in directionStringList and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                targetMobKey = ' '.join(input.lower().split()[2:-2])
                targetDirKey = input.lower().split()[-2]
                targetDirCount = int(input.split()[-1])
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, "All", targetDirCount)

            # Target All Mob 'Direction' #
            elif len(input.split()) > 3 and input.lower().split()[1] == "all" and input.lower().split()[-1] in directionStringList:
                targetMobKey = ' '.join(input.lower().split()[2:-1])
                targetDirKey = input.lower().split()[-1]
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, "All", 1)

            # Target '#' Mob 'Direction' '#' #
            elif len(input.split()) > 4 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and input.lower().split()[-2] in directionStringList and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                targetMobCount = int(input.split()[1])
                targetMobKey = ' '.join(input.lower().split()[2:-2])
                targetDirKey = input.lower().split()[-2]
                targetDirCount = int(input.split()[-1])
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, targetDirCount)

            # Target '#' Mob 'Direction' #
            elif len(input.split()) > 3 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and input.lower().split()[-1] in directionStringList:
                targetMobCount = int(input.split()[1])
                targetMobKey = ' '.join(input.lower().split()[2:-1])
                targetDirKey = input.lower().split()[-1]
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, 1)

            # Target All 'Direction' '#' #
            elif len(input.split()) == 4 and input.lower().split()[1] == "all" and input.lower().split()[2] in directionStringList and stringIsNumber(input.split()[3]) and int(input.split()[3]) > 0:
                targetDirKey = input.lower().split()[2]
                targetDirCount = int(input.split()[3])
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, "All", targetDirKey, "All", targetDirCount)

            # Target All 'Direction' #
            elif len(input.split()) == 3 and input.lower().split()[1] == "all" and input.lower().split()[2] in directionStringList:
                targetDirKey = input.lower().split()[2]
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, "All", targetDirKey, "All", 1)

            # Target Mob 'Direction' '#' #
            elif len(input.split()) > 3 and input.lower().split()[-2] in directionStringList and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                targetMobKey = ' '.join(input.lower().split()[1:-2])
                targetDirKey = input.lower().split()[-2]
                targetDirCount = int(input.split()[-1])
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, 1, targetDirCount)

            # Target Mob 'Direction' #
            elif len(input.split()) > 2 and input.lower().split()[-1] in directionStringList:
                targetMobKey = ' '.join(input.lower().split()[1:-1])
                targetDirKey = input.lower().split()[-1]
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, 1, 1)

            # Target All #
            elif len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, "All", None, "All", None)

            # Target All Mob #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                targetMobKey = ' '.join(input.lower().split()[2::])
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, None, "All", None)

            # Target '#' Mob #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetMobCount = int(input.split()[1])
                targetMobKey = ' '.join(input.lower().split()[2::])
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, None, targetMobCount, None)

            # Target Mob #
            elif len(input.split()) > 1:
                targetMobKey = ' '.join(input.lower().split()[1::])
                self.player.targetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, None, 1, None)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Target what?", "Code":"11w1y"})

        # Untarget #
        elif input.lower().split()[0] in ["untarget", "untarge", "untarg", "untar", "unta", "unt", "un", "u"]:

            # Untarget All Mob 'Direction' '#' #
            if len(input.split()) > 4 and input.lower().split()[1] == "all" and input.lower().split()[-2] in directionStringList and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                targetMobKey = ' '.join(input.lower().split()[2:-2])
                targetDirKey = input.lower().split()[-2]
                targetDirCount = int(input.split()[-1])
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, "All", targetDirCount)

            # Untarget All Mob 'Direction' #
            elif len(input.split()) > 3 and input.lower().split()[1] == "all" and input.lower().split()[-1] in directionStringList:
                targetMobKey = ' '.join(input.lower().split()[2:-1])
                targetDirKey = input.lower().split()[-1]
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, "All", 1)

            # Untarget '#' Mob 'Direction' '#' #
            elif len(input.split()) > 4 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and input.lower().split()[-2] in directionStringList and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                targetMobKey = ' '.join(input.lower().split()[2:-2])
                targetDirKey = input.lower().split()[-2]
                targetMobCount = int(input.split()[1])
                targetDirCount = int(input.split()[-1])
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, targetDirCount)

            # Untarget '#' Mob 'Direction' #
            elif len(input.split()) > 3 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and input.lower().split()[-1] in directionStringList:
                targetMobKey = ' '.join(input.lower().split()[2:-1])
                targetDirKey = input.lower().split()[-1]
                targetMobCount = int(input.split()[1])
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, 1)

            # Untarget All 'Direction' '#' #
            elif len(input.split()) == 4 and input.lower().split()[1] == "all" and input.lower().split()[2] in directionStringList and stringIsNumber(input.split()[3]) and int(input.split()[3]) > 0:
                targetDirKey = input.lower().split()[-2]
                targetDirCount = int(input.split()[-1])
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, "All", targetDirKey, "All", targetDirCount)

            # Untarget All 'Direction' #
            elif len(input.split()) == 3 and input.lower().split()[1] == "all" and input.lower().split()[2] in directionStringList:
                targetDirKey = input.lower().split()[-1]
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, "All", targetDirKey, "All", 1)

            # Untarget Mob 'Direction' '#' #
            elif len(input.split()) > 3 and input.lower().split()[-2] in directionStringList and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                targetMobKey = ' '.join(input.lower().split()[1:-2])
                targetDirKey = input.lower().split()[-2]
                targetDirCount = int(input.split()[-1])
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, 1, targetDirCount)

            # Untarget Mob 'Direction' #
            elif len(input.split()) > 2 and input.lower().split()[-1] in directionStringList:
                targetMobKey = ' '.join(input.lower().split()[1:-1])
                targetDirKey = input.lower().split()[-1]
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, targetDirKey, 1, 1)

            # Untarget All #
            elif len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, "All", None, "All", None)

            # Untarget All Mob #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                targetMobKey = ' '.join(input.lower().split()[2::])
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, None, "All", None)

            # Untarget '#' Mob #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetMobKey = ' '.join(input.lower().split()[2::])
                targetMobCount = int(input.split()[1])
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, None, targetMobCount, None)

            # Untarget Mob #
            elif len(input.split()) > 1:
                targetMobKey = ' '.join(input.lower().split()[1::])
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, targetMobKey, None, 1, None)

            # Untarget #
            elif len(input.split()) == 1:
                self.player.untargetCheck(self.console, self.galaxyList, currentRoom, "All", None, 1, None)

        # Movement #
        elif len(input.split()) == 1 and input.lower() in directionStringList:
            
            # Move Direction '#' #

            # Move Direction #
            self.player.moveCheck(self.console, self.map, self.galaxyList, self.player, currentRoom, input.lower())

        # Open/Close #
        elif input.lower().split()[0] in ["open", "ope", "op", "o", "close", "clos", "clo", "cl"]:
            if input.lower().split()[0] in ["open", "ope", "op", "o"] : targetAction = "Open"
            else : targetAction = "Close"
            
            # Open/Close 'Direction' #
            if len(input.split()) == 2 and input.lower().split()[1] in directionStringList:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"] : targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"] : targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"] : targetDir = "South"
                else : targetDir = "West"
                self.player.openCloseDoorCheck(self.console, self.galaxyList, currentRoom, targetAction, targetDir)

            # Open/Close Target #
            elif len(input.split()) > 1:
                self.player.openCloseTargetCheck(self.console, self.galaxyList, currentRoom, targetAction, ' '.join(input.lower().split()[1::]))

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": targetAction + " what?", "Code":str(len(targetAction)) + "w5w1y"})

        # Lock/Unlock #
        elif input.lower().split()[0] in ["lock", "loc", "unlock", "unloc", "unlo"]:
            if input.lower().split()[0] in ["lock", "loc"] : targetAction = "Lock"
            else : targetAction = "Unlock"

            # Lock/Unlock 'Direction' #
            if len(input.split()) == 2 and input.lower().split()[1] in directionStringList:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"] : targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"] : targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"] : targetDir = "South"
                else : targetDir = "West"
                self.player.lockUnlockDoorCheck(self.console, self.galaxyList, currentRoom, targetAction, targetDir)

            # Lock/Unlock Target #
            elif len(input.split()) > 1:
                self.player.lockUnlockTargetCheck(self.console, self.galaxyList, currentRoom, targetAction, ' '.join(input.lower().split()[1::]))

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": targetAction + " what?", "Code":str(len(targetAction)) + "w5w1y"})

        # Get #
        elif input.lower().split()[0] in ["get", "ge", "g"]:

            # Get All Item From All (Loot Item From All) #
            if len(input.split()) > 4 and input.lower().split()[1] == "all" and "from" in input.lower().split() and input.lower().split()[2] != "from" and input.lower().split()[-1] == "all":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[2:fromIndex])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, "All", "All")
             
            # Get All Item From Container (Loot Item From Container) #
            elif len(input.split()) > 4 and input.lower().split()[1] == "all" and "from" in input.lower().split() and input.lower().split()[2] != "from" and input.lower().split()[-1] != "from":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[2:fromIndex])
                targetContainerKey = ' '.join(input.lower().split()[fromIndex + 1::])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, targetContainerKey, "All")

            # Get All From All (Loot All) #
            elif len(input.split()) == 4 and input.lower().split()[1] == "all" and input.lower().split()[2] == "from" and input.lower().split()[3] == "all":
                self.player.getCheck(self.console, self.galaxyList, currentRoom, "All", "All", "All")

            # Get All From Container (Loot Container) #
            elif len(input.split()) > 3 and input.lower().split()[1] == "all" and input.lower().split()[2] == "from":
                targetContainerKey = ' '.join(input.lower().split()[3::])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, "All", targetContainerKey, "All")

            # Get '#' Item From All #
            elif len(input.split()) > 4 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and "from" in input.lower().split() and input.lower().split()[2] != "from" and input.lower().split()[-1] == "all":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[2:fromIndex])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, "All", int(input.split()[1]))

            # Get '#' Item From Container #
            elif len(input.split()) > 4 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and "from" in input.lower().split() and input.lower().split()[2] != "from" and input.lower().split()[-1] != "from":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[2:fromIndex])
                targetContainerKey = ' '.join(input.lower().split()[fromIndex + 1::])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, targetContainerKey, int(input.split()[1]))

            # Get Item From All #
            elif len(input.split()) > 3 and input.lower().split()[-2] == "from" and input.lower().split()[-1] == "all":
                targetItemKey = ' '.join(input.lower().split()[1:-2])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, "All", 1)

            # Get Item From Container #
            elif len(input.split()) > 3 and "from" in input.lower().split() and input.lower().split()[1] != "from" and input.lower().split()[-1] != "from":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[1:fromIndex])
                targetContainerKey = ' '.join(input.lower().split()[fromIndex + 1::])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, targetContainerKey, 1)

            # Get All #
            elif len(input.split()) == 2 and input.split()[1].lower() == "all":
                self.player.getCheck(self.console, self.galaxyList, currentRoom, "All", None, "All")
                
            # Get All Item #
            elif len(input.split()) > 2 and input.split()[1].lower() == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, None, "All")

            # Get '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, None, int(input.split()[1]))

            # Get Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, None, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Get what?", "Code":"8w1y"})

        # Loot #
        elif input.lower().split()[0] in ["loot"]:

            # Loot Item From All #
            if len(input.split()) > 3 and input.lower().split()[-2] == "from" and input.lower().split()[-1] == "all":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[1:fromIndex])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, "All", "All")

            # Loot Item From Container #
            elif len(input.split()) > 3 and "from" in input.lower().split() and input.lower().split()[1] != "from" and input.lower().split()[-1] != "from":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[1:fromIndex])
                targetContainerKey = ' '.join(input.lower().split()[fromIndex + 1::])
                self.player.getCheck(self.console, self.galaxyList, currentRoom, targetItemKey, targetContainerKey, "All")

            # Loot All #
            elif len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.getCheck(self.console, self.galaxyList, currentRoom, "All", "All", "All")

            # Loot Container #
            elif len(input.split()) > 1:
                self.player.getCheck(self.console, self.galaxyList, currentRoom, "All", ' '.join(input.lower().split()[1::]), "All")

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Loot what?", "Code":"9w1y"})

        # Empty #

            # Empty Container/Drink #

        # Put #
        elif input.lower().split()[0] in ["put", "pu", "p"]:

            # Put All Item In Container #
            if len(input.split()) > 4 and input.lower().split()[1] == "all" and "in" in input.lower().split() and input.lower().split()[2] != "in" and input.lower().split()[-1] != "in":
                inIndex = input.lower().split().index("in")
                targetItemKey = ' '.join(input.lower().split()[2:inIndex])
                targetContainerKey = ' '.join(input.lower().split()[inIndex + 1::])
                self.player.putCheck(self.console, self.galaxyList, currentRoom, targetItemKey, targetContainerKey, "All")

            # Put All In Container #
            elif len(input.split()) > 3 and input.lower().split()[1] == "all" and input.lower().split()[2] == "in":
                targetContainerKey = ' '.join(input.lower().split()[3::])
                self.player.putCheck(self.console, self.galaxyList, currentRoom, "All", targetContainerKey, "All")

            # Put '#' Item In Container #
            elif len(input.split()) > 4 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and "in" in input.lower().split() and input.lower().split()[2] != "in" and input.lower().split()[-1] != "in":
                inIndex = input.lower().split().index("in")
                targetItemKey = ' '.join(input.lower().split()[2:inIndex])
                targetContainerKey = ' '.join(input.lower().split()[inIndex + 1::])
                self.player.putCheck(self.console, self.galaxyList, currentRoom, targetItemKey, targetContainerKey, int(input.split()[1]))

            # Put Item In Container #
            elif len(input.split()) > 3 and "in" in input.lower().split() and input.lower().split()[1] != "in" and input.lower().split()[-1] != "in":
                inIndex = input.lower().split().index("in")
                targetItemKey = ' '.join(input.lower().split()[1:inIndex])
                targetContainerKey = ' '.join(input.lower().split()[inIndex + 1::])
                self.player.putCheck(self.console, self.galaxyList, currentRoom, targetItemKey, targetContainerKey, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Put what in what?", "Code":"16w1y"})

        # Drop #
        elif input.lower().split()[0] in ["drop", "dro", "dr"]:

            # Drop All #
            if len(input.split()) == 2 and input.split()[1].lower() == "all":
                self.player.dropCheck(self.console, self.galaxyList, currentRoom, "All", "All")

            # Drop All Pocket #
            elif len(input.split()) == 3 and input.lower().split()[1] == "all" and input.lower().split()[2] in self.player.getPocketList(True):
                pocketKey = ' '.join(input.lower().split()[2::])
                self.player.dropCheck(self.console, self.galaxyList, currentRoom, "All", "All", pocketKey)

            # Drop All Item #
            elif len(input.split()) > 2 and input.split()[1].lower() == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.dropCheck(self.console, self.galaxyList, currentRoom, targetItemKey, "All")

            # Drop '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.dropCheck(self.console, self.galaxyList, currentRoom, targetItemKey, int(input.split()[1]))

            # Drop Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.dropCheck(self.console, self.galaxyList, currentRoom, targetItemKey, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Drop what?", "Code":"9w1y"})
        
        # Wear #
        elif input.lower().split()[0] in ["wear", "wea"]:

            # Wear All #
            if len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.wearCheck(self.console, "All", "All")

            # Wear All Item #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.wearCheck(self.console, targetItemKey, "All")

            # Wear Item 'GearSlot' #
            elif len(input.split()) > 2 and ((stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0) or input.lower().split()[-1] in ["left", "lef", "le", "l", "right", "righ", "rig", "ri", "r"]):
                targetItemKey = ' '.join(input.lower().split()[1:-1])
                self.player.wearCheck(self.console, targetItemKey, 1, input.lower().split()[-1])

            # Wear '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.wearCheck(self.console, targetItemKey, int(input.split()[1]))

            # Wear Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.wearCheck(self.console, targetItemKey, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Wear what?", "Code":"9w1y"})
        
        # Wield #
        elif input.lower().split()[0] in ["wield", "wiel", "wie" "wi", "hold", "hol", "ho"]:

            # Wield All #
            if len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.wieldCheck(self.console, "All", None, 2)

            # Wield Item 'Slot' #
            elif len(input.split()) > 2 and ((stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0) or input.lower().split()[-1] in ["left", "lef", "le", "l", "right", "righ", "rig", "ri", "r"]):
                self.player.wieldCheck(self.console, ' '.join(input.lower().split()[1:-1]), input.lower().split()[-1], 1)

            # Wield All Item #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                self.player.wieldCheck(self.console, ' '.join(input.lower().split()[2::]), None, 2)

            # Wield '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                self.player.wieldCheck(self.console, ' '.join(input.lower().split()[2::]), None, int(input.split()[1]))

            # Wield Item #
            elif len(input.split()) > 1:
                self.player.wieldCheck(self.console, ' '.join(input.lower().split()[1::]), None, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Wield what?", "Code":"10w1y"})

        # Remove #
        elif input.lower().split()[0] in ["remove", "remov", "remo", "rem"]:

            # Remove All #
            if len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.removeCheck(self.console, "All", "All")

            # Remove All Gear/Weapon #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.removeCheck(self.console, targetItemKey, "All")

            # Remove Gear/Weapon 'GearSlot' #
            elif len(input.split()) > 2 and (stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0) or input.lower().split()[-1] in ["left", "right"]:
                if stringIsNumber(input.split()[-1]):
                    targetGearSlotIndex = int(input.split()[-1]) - 1
                else:
                    targetGearSlotIndex = input.lower().split()[-1]
                targetItemKey = ' '.join(input.lower().split()[1:-1])
                self.player.removeCheck(self.console, targetItemKey, 1, targetGearSlotIndex)

            # Remove '#' Gear/Weapon #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.removeCheck(self.console, targetItemKey, int(input.split()[1]))

            # Remove Gear/Weapon #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.removeCheck(self.console, targetItemKey, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Remove what?", "Code":"11w1y"})

        ## Combat Commands ##
        # Attack #
        elif input.lower().split()[0] in ["attack", "attac", "atta", "att", "at", "a"]:
            
            # Attack Mob #
            if len(input.split()) > 1:
                mobKey = ' '.join(input.lower().split()[1::])
                self.player.attackCheck(self.console, self.galaxyList, currentRoom, mobKey)

            # Attack #
            else:
                self.player.attackCheck(self.console, self.galaxyList, currentRoom, None)

        # Combat Skill #
        elif combatSkill != None:
            parsedCombatInput = parsedCombatInput.split()
            
            # Skill '#' Mob Direction '#' #
            if len(parsedCombatInput) > 3 and stringIsNumber(parsedCombatInput[0]) and int(parsedCombatInput[0]) > 0 and parsedCombatInput[-2] in directionStringList and stringIsNumber(parsedCombatInput[-1]) and int(parsedCombatInput[-1]) > 0:
                mobCount = int(parsedCombatInput[0])
                mobKey = ' '.join(parsedCombatInput[1:-2])
                directionKey = parsedCombatInput[-2]
                directionCount = int(parsedCombatInput[-1])
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill All/Group Mob Direction '#' #
            elif len(parsedCombatInput) > 3 and parsedCombatInput[0] in ["all", "group"] and parsedCombatInput[-2] in directionStringList and stringIsNumber(parsedCombatInput[-1]) and int(parsedCombatInput[-1]) > 0:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = ' '.join(parsedCombatInput[1:-2])
                directionKey = parsedCombatInput[-2]
                directionCount = int(parsedCombatInput[-1])
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill All/Group Direction '#' #
            elif len(parsedCombatInput) == 3 and parsedCombatInput[0] in ["all", "group"] and parsedCombatInput[1] in directionStringList and stringIsNumber(parsedCombatInput[2]) and int(parsedCombatInput[2]) > 0:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = "All"
                directionKey = parsedCombatInput[-2]
                directionCount = int(parsedCombatInput[-1])
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill Mob Direction '#' #
            elif len(parsedCombatInput) > 2 and parsedCombatInput[-2] in directionStringList and stringIsNumber(parsedCombatInput[-1]) and int(parsedCombatInput[-1]) > 0:
                mobCount = 1
                mobKey = ' '.join(parsedCombatInput[0:-2])
                directionKey = parsedCombatInput[-2]
                directionCount = int(parsedCombatInput[-1])
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill '#' Mob Direction #
            elif len(parsedCombatInput) > 2 and stringIsNumber(parsedCombatInput[0]) and int(parsedCombatInput[0]) > 0 and parsedCombatInput[-1] in directionStringList:
                mobCount = int(parsedCombatInput[0])
                mobKey = ' '.join(parsedCombatInput[1:-1])
                directionKey = parsedCombatInput[-1]
                directionCount = 1
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill All/Group Mob Direction #
            elif len(parsedCombatInput) > 2 and parsedCombatInput[0] in ["all", "group"] and parsedCombatInput[-1] in directionStringList:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = ' '.join(parsedCombatInput[1:-1])
                directionKey = parsedCombatInput[-1]
                directionCount = 1
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill All/Group Direction #
            elif len(parsedCombatInput) == 2 and parsedCombatInput[0] in ["all", "group"] and parsedCombatInput[1] in directionStringList:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = "All"
                directionKey = parsedCombatInput[-1]
                directionCount = 1
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill Mob Direction #
            elif len(parsedCombatInput) > 1 and parsedCombatInput[-1] in directionStringList:
                mobCount = 1
                mobKey = ' '.join(parsedCombatInput[0:-1])
                directionKey = parsedCombatInput[-1]
                directionCount = 1
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill Direction '#' #
            elif len(parsedCombatInput) == 2 and parsedCombatInput[0] in directionStringList and stringIsNumber(parsedCombatInput[1]) and int(parsedCombatInput[1]) > 0:
                mobCount = "All"
                mobKey = "All"
                directionKey = parsedCombatInput[0]
                directionCount = int(parsedCombatInput[1])
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill '#' Mob #
            elif len(parsedCombatInput) > 1 and stringIsNumber(parsedCombatInput[0]) and int(parsedCombatInput[0]) > 0:
                mobCount = int(parsedCombatInput[0])
                mobKey = ' '.join(parsedCombatInput[1::])
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, None, None)

            # Skill All/Group Mob #
            elif len(parsedCombatInput) > 1 and parsedCombatInput[0] in ["all", "group"]:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = ' '.join(parsedCombatInput[1::])
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, None, None)
            
            # Skill All/Group #
            elif len(parsedCombatInput) == 1 and parsedCombatInput[0] in ["all", "group"]:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = "All"
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, None, None)

            # Skill Direction #
            elif len(parsedCombatInput) == 1 and parsedCombatInput[0] in directionStringList:
                mobCount = "All"
                mobKey = "All"
                directionKey = parsedCombatInput[0]
                directionCount = 1
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill Mob/Self #
            elif len(parsedCombatInput) > 0:
                mobCount = 1
                mobKey = ' '.join(parsedCombatInput)
                if mobKey == "self" : mobKey = "Self"
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, mobCount, mobKey, None, None)

            # Skill #
            elif parsedCombatInput == []:
                self.player.combatSkillCheck(self.console, self.galaxyList, currentRoom, combatSkill, None, None, None, None)
            
        # Cast #

            # Cast Spell All/Self Direction/Num #

            # Cast Spell Direction/Num #

            # Cast Spell Mob Direction/Num #

            # Cast Spell All/Self #

            # Cast Spell #

            # Cast Spell Mob #

            # Cast #

        # Dodge #

        # Parry #

        # Switch #
        elif len(input.split()) == 1 and input.lower() in ["switch", "switc", "swit", "swi", "sw"]:
            self.player.switchCheck(self.console)

        # Reload/Load #
        elif input.lower().split()[0] in ["reload", "reloa", "relo", "rel", "re", "load", "loa"]:

            # Reload Left/Right Ammo #
            if len(input.split()) > 2 and (input.lower().split()[1] in ["left", "lef", "le", "l", "right", "righ", "rig", "ri", "r"] or (stringIsNumber(input.split()[1]) and int(input.split()[1] > 0))):
                reloadSlot = input.lower().split()[1]
                ammoKey = ' '.join(input.lower().split()[2::])
                self.player.reloadCheck(self.console, self.galaxyList, self.player, currentRoom, None, reloadSlot, ammoKey)

            # Reload All Ammo #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                ammoKey = ' '.join(input.lower().split()[2::])
                self.player.reloadCheck(self.console, self.galaxyList, self.player, currentRoom, "All", "All", ammoKey)

            # Reload Weapon Ammo #
            elif len(input.split()) > 2:
                reloadKey = input.lower().split()[1]
                ammoKey = ' '.join(input.lower().split()[2::])
                self.player.reloadCheck(self.console, self.galaxyList, self.player, currentRoom, reloadKey, None, ammoKey)

            # Reload All #
            elif len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.reloadCheck(self.console, self.galaxyList, self.player, currentRoom, "All", "All", None)

            # Reload Left/Right #
            elif len(input.split()) == 2 and (input.lower().split()[1] in ["left", "lef", "le", "l", "right", "righ", "rig", "ri", "r"] or (stringIsNumber(input.split()[1]) and int(input.split()[1] > 0))):
                reloadSlot = input.lower().split()[1]
                self.player.reloadCheck(self.console, self.galaxyList, self.player, currentRoom, None, reloadSlot, None)

            # Reload Weapon/Ammo #
            elif len(input.split()) == 2:
                reloadKey = input.lower().split()[1]
                self.player.reloadCheck(self.console, self.galaxyList, self.player, currentRoom, reloadKey, None, None)

            # Reload #
            else:
                self.player.reloadCheck(self.console, self.galaxyList, self.player, currentRoom, "All", None, None)

        # Unload #
        elif input.lower().split()[0] in ["unload", "unloa", "unlo", "unl"]:

            # Unload All Ammo #
            if len(input.split()) > 2 and input.lower().split()[1] == "all":
                ammoKey = ' '.join(input.lower().split()[2::])
                self.player.unloadCheck(self.console, self.galaxyList, self.player, currentRoom, "All", None, ammoKey)

            # Unload All #
            elif len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.unloadCheck(self.console, self.galaxyList, self.player, currentRoom, "All", None, None)

            # Unload Left/Right #
            elif len(input.split()) == 2 and (input.lower().split()[1] in ["left", "lef", "le", "l", "right", "righ", "rig", "ri", "r"] or (stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0)):
                unloadSlotKey = input.lower().split()[1]
                self.player.unloadCheck(self.console, self.galaxyList, self.player, currentRoom, None, unloadSlotKey, None)

            # Unload Weapon #
            elif len(input.split()) > 1:
                unloadKey = ' '.join(input.lower().split()[1::])
                self.player.unloadCheck(self.console, self.galaxyList, self.player, currentRoom, unloadKey, None, None)

            # Unload #
            else:
                self.player.unloadCheck(self.console, self.galaxyList, self.player, currentRoom, "All", "All", None)

        # Recruit/Tame [Needs Testing] #
        elif input.lower().split()[0] in ["tame", "tam", "recruit", "recrui", "recru", "recr", "rec"]:

            # Recruit All Mob #
            if len(input.split()) > 2 and input.lower().split()[1] == "all":
                mobCount = "All"
                mobKey = ' '.join(input.lower().split()[2::])
                self.player.recruitCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)

            # Recruit '#' Mob #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                mobCount = int(input.split()[1])
                mobKey = ' '.join(input.lower().split()[2::])
                self.player.recruitCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)

            # Recruit All #
            elif len(input.split()) == 2 and input.lower().split()[1] == "all":
                mobCount = "All"
                mobKey = "All"
                self.player.recruitCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)

            # Recruit Mob #
            elif len(input.split()) > 1:
                mobCount = 1
                mobKey = ' '.join(input.lower().split()[1::])
                self.player.recruitCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)

            # Recruit #
            else:
                self.player.recruitCheck(self.console, self.galaxyList, self.player, currentRoom, None, None)

        # Disband #
        elif input.lower().split()[0] in ["disband", "disban", "disba", "disb", "dis"]:
            
            # Disband All Mob #
            if len(input.split()) > 2 and input.lower().split()[1] == "all":
                mobCount = "All"
                mobKey = ' '.join(input.lower().split()[2::])
                self.player.disbandCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)

            # Disband '#' Mob #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                mobCount = int(input.split()[1])
                mobKey = ' '.join(input.lower().split()[2::])
                self.player.disbandCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)

            # Disband All #
            elif len(input.split()) == 2 and input.lower().split()[1] == "all":
                mobCount = "All"
                mobKey = "All"
                self.player.disbandCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)

            # Disband Mob #
            elif len(input.split()) > 1:
                mobCount = 1
                mobKey = ' '.join(input.lower().split()[1::])
                self.player.disbandCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)
            
            # Disband #
            else:
                mobCount = "All"
                mobKey = "All"
                self.player.disbandCheck(self.console, self.galaxyList, self.player, currentRoom, mobKey, mobCount)

        # Stop #
        elif len(input.split()) == 1 and input.lower() == "stop":
            self.player.stopCheck(self.console)

        ## Status Commands ##
        # Inventory #
        elif input.lower().split()[0] in ["inventory", "inventor", "invento", "invent", "inven", "inve", "inv", "in", "i"]:
            targetPocketKey = None
            if len(input.split()) > 1:
                targetPocketKey = ' '.join(input.lower().split()[1::])
            self.player.displayInventory(self.console, self.galaxyList, currentRoom, targetPocketKey)
        
        # Gear #
        elif len(input.split()) == 1 and input.lower() in ["gear", "gea"]:
            self.player.displayGear(self.console, self.galaxyList, currentRoom)

        # Skills #
        elif len(input.split()) == 1 and input.lower() in ["skills", "skill", "skil", "ski", "sk"]:
            self.player.displaySkills(self.console)

        # Character/Status #
        elif len(input.split()) == 1 and input.lower() in ["status", "statu", "stat", "sta", "st"]:
            self.player.displayStatus(self.console)

        # Time #
        elif len(input.split()) == 1 and input.lower() in ["time", "tim", "ti"]:
            currentPlanet = self.galaxyList[self.player.galaxy].systemList[self.player.system].planetList[self.player.planet]
            currentPlanet.displayTime(self.console)

        # Weather #

        # Astro(?) #

        ## Other Commands ##
        # Eat/Drink #

        # Fill #

        # List #

        # Buy(?) #

        # Sell(?) #

        ## Spaceship Commands ##
        # Board #
        elif input.lower().split()[0] in ["board", "boar", "boa", "bo"]:
            if len(input.split()) > 1:
                self.player.boardCheck(self.console, self.map, self.galaxyList, currentRoom, ' '.join(input.lower().split()[1::]))
            
            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Board what?", "Code":"10w1y"})

        # Launch #

        # Scan #

        # Radar #

        # Course #

        # Calculate #

        # Throttle #

        # System #

        # Land #

        ## Crafting Commands ##
        # Inspect #
        
        # Prospect #

        # Plant #

            # Plant All #

            # Plant All Item #

            # Plant '#' Item #

            # Plant Item #

        # Forage/Harvest #

        # Craft/Create #

        ## Config Commands ##
        # Auto Loot #
        elif input.lower().split()[0] == "autoloot" or (len(input.split()) == 2 and input.lower().split()[0] == "auto" and input.lower().split()[1] == "loot"):
            self.player.autoLoot = not self.player.autoLoot
            self.console.lineList.insert(0, {"Blank": True})
            self.console.lineList.insert(0, {"String": "Setting changed.", "Code":"15w1y"})

        # Auto Reload #
        elif input.lower().split()[0] == "autoreload" or (len(input.split()) == 2 and input.lower().split()[0] == "auto" and input.lower().split()[1] == "reload"):
            self.player.autoReload = not self.player.autoReload
            self.console.lineList.insert(0, {"Blank": True})
            self.console.lineList.insert(0, {"String": "Setting changed.", "Code":"15w1y"})

        # Team Damage #
        elif input.lower().split()[0] == "teamdamage" or (len(input.split()) == 2 and input.lower().split()[0] == "team" and input.lower().split()[1] == "damage"):
            self.player.teamDamage = not self.player.teamDamage
            self.console.lineList.insert(0, {"Blank": True})
            self.console.lineList.insert(0, {"String": "Setting changed.", "Code":"15w1y"})

        # Heal Enemies #
        elif input.lower().split()[0] == "healenemies" or (len(input.split()) == 2 and input.lower().split()[0] == "heal" and input.lower().split()[1] == "enemies"):
            self.player.healEnemies = not self.player.healEnemies
            self.console.lineList.insert(0, {"Blank": True})
            self.console.lineList.insert(0, {"String": "Setting changed.", "Code":"15w1y"})

        ## God Commands ##
        # Manifest #
        elif input.lower().split()[0] in ["manifest", "manifes", "manife", "manif", "mani", "man"]:
            inputCheck = True

            # Manifest Mob #
            if len(input.split()) > 1 and input.lower().split()[1] == "mob":

                # Manifest Mob Num Count #
                if len(input.split()) > 3 and stringIsNumber(input.split()[-2]) and int(input.split()[-2]) > 0 and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                    mobNum = int(input.split()[-2])
                    mobCount = int(input.split()[-1])
                    self.player.manifestCheck(self.console, currentRoom, "Mob", mobNum, mobCount)

                # Manifest Mob Num #
                elif len(input.split()) > 2 and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                    mobNum = int(input.split()[-1])
                    mobCount = 1
                    self.player.manifestCheck(self.console, currentRoom, "Mob", mobNum, mobCount)
                
                else : inputCheck = False
            else : inputCheck = False

            if inputCheck == False:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Manifest what?", "Code":"13w1y"})

        ## Emotes ##
        elif input.lower().split()[0] in self.player.emoteList:
            self.player.emote(self.console, input.lower())

        else:
            self.console.lineList.insert(0, {"Blank": True})
            self.console.lineList.insert(0, {"String": "Huh?", "Code":"3w1y"})
