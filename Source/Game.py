import pygame, random
from pygame import *
from Components.Utility import stringIsNumber
from Components.Keyboard import Keyboard
from Screen.Console import Console
from Screen.InputBar import InputBar
from GameData.Player import Player
from GameData.Galaxy import Galaxy
from GameData.SolarSystem import SolarSystem
from GameData.Planet import Planet
from GameData.Area import Area
from GameData.Room import Room
from GameData.Item import Item

class Game:

    def __init__(self):
        self.keyboard = Keyboard()
        self.console = Console()
        self.inputBar = InputBar()

        self.player = Player()
        self.galaxyList = []

        self.updateTick = 0

        self.loadGame()

    def loadGame(self):
        galaxyMilkyWay = Galaxy()
        self.galaxyList.append(galaxyMilkyWay)
        galaxyMilkyWay.name = {"String":"Milky Way"}

        systemProtoSol = SolarSystem()
        galaxyMilkyWay.systemList.append(systemProtoSol)
        systemProtoSol.name = {"String":"Proto Sol"}

        starProtoSol = Planet(0, 0, 0, 0, 38880, 0)
        systemProtoSol.planetList.append(starProtoSol)
        starProtoSol.name = {"String":"Proto Sol"}
        starProtoSol.type = "Star"
        starProtoSol.axialTilt = 6

        areaLimbo = Area()
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

        areaCOTU = Area()
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
                                  {"String":"to the South and a garden lies to the North.", "Code":"7w1w5ddw6w1g1dg1ddg1g1dg1ddg13w1w4ddw1y"}]
        # for i in range(5, 18):
        #     roomCOTU00.itemList.append(Item(i))

        roomCOTU01 = Room(0, 0, 1, 0, 1)
        areaCOTU.roomList.append(roomCOTU01)
        roomCOTU01.name = {"String":"Bridge To The Spaceport", "Code":"14w1w1dw2ddw1dw1w1dw1ddw1dw"}
        roomCOTU01.exit["North"] = [0, 0, 1, 0, 0]
        roomCOTU01.exit["South"] = [0, 0, 1, 0, 2]
        roomCOTU01.itemList.append(Item(4))

        roomCOTU02 = Room(0, 0, 1, 0, 2)
        areaCOTU.roomList.append(roomCOTU02)
        roomCOTU02.name = {"String":"Spaceport Entrance", "Code":"1w1dw2ddw1dw1w1dw1ddw1dw9w"}
        roomCOTU02.exit["North"] = [0, 0, 1, 0, 1]

        roomCOTU03 = Room(0, 0, 1, 0, 3)
        areaCOTU.roomList.append(roomCOTU03)
        roomCOTU03.name = {"String":"A Peaceful Garden", "Code":"2w1w1dw2ddw1dw1w1ddw1da1w1g1dg1ddg1g1dg1ddg"}
        roomCOTU03.exit["South"] = [0, 0, 1, 0, 0]
        roomCOTU03.exit["West"] = [0, 0, 1, 0, 4]
        # for i in range(random.randrange(5, 15)):
        #     roomCOTU03.itemList.append(Item(1))
        # for i in range(random.randrange(5, 15)):
        #     roomCOTU03.itemList.append(Item(2))
        # for i in range(random.randrange(5, 15)):
        #     roomCOTU03.itemList.append(Item(3))
        roomCOTU03.itemList.append(Item(12))

        roomCOTU04 = Room(0, 0, 1, 0, 4)
        areaCOTU.roomList.append(roomCOTU04)
        roomCOTU04.name = {"String":"A Little Wooden Shack", "Code":"9w1do1dddo1ddo1do1dddo1ddo6w"}
        roomCOTU04.exit["East"] = [0, 0, 1, 0, 3]
        roomCOTU04.inside = True
        
        systemSol = SolarSystem()
        galaxyMilkyWay.systemList.append(systemSol)
        systemSol.name = {"String":"Sol"}

        starSol = Planet(0, 1, 0, 0, 38880, 0)
        systemSol.planetList.append(starSol)
        starSol.name = {"String":"Sol"}
        starSol.type = "Star"
        starSol.axialTilt = 6

        planetMercury = Planet(0, 1, 1, 29945, 84960, 126720)
        systemSol.planetList.append(planetMercury)
        planetMercury.name = {"String":"Mercury"}
        
        planetVenus = Planet(0, 1, 2, 67443, 349920, 324000)
        systemSol.planetList.append(planetVenus)
        planetVenus.name = {"String":"Venus"}
        planetVenus.orbit = "Clockwise"
        planetVenus.axialTilt = 3
        
        planetEarth = Planet(0, 1, 3, 93456, 1440, 525600)
        systemSol.planetList.append(planetEarth)
        planetEarth.name = {"String":"Earth"}
        planetEarth.axialTilt = 23.5

        planetMars = Planet(0, 1, 4, 15044, 1477, 989280)
        systemSol.planetList.append(planetMars)
        planetMars.name = {"String":"Mars"}
        planetJupiter = Planet(0, 1, 5, 484000000, 596, 6239520)
        systemSol.planetList.append(planetJupiter)
        planetJupiter.name = {"String":"Jupiter"}
        planetSaturn = Planet(0, 1, 6, 886000000, 634, 15448640)
        systemSol.planetList.append(planetSaturn)
        planetSaturn.name = {"String":"Saturn"}
        planetUranus = Planet(0, 1, 7, 1824000000, 1034, 44189280)
        systemSol.planetList.append(planetUranus)
        planetUranus.name = {"String":"Uranus"}
        planetNeptune = Planet(0, 1, 8, 2779300000, 966, 86673600)
        systemSol.planetList.append(planetNeptune)
        planetNeptune.name = {"String":"Neptune"}
        planetPluto = Planet(0, 1, 9, 3700000000, 9180, 130348800)
        systemSol.planetList.append(planetPluto)
        planetPluto.name = {"String":"Pluto"}

        # Load Doors AFTER ALL Rooms Are Loaded! #
        roomCOTU02.installDoor(self.galaxyList, "North", "Automatic", "COTU Spaceport")
        roomCOTU02.lockUnlockDoor(self.galaxyList, "Lock", "North")
        roomCOTU04.installDoor(self.galaxyList, "East", "Manual", None, "Open")

    def update(self, window):
        self.processInput()
        self.inputBar.update(self.keyboard)

        self.updateTick += 1
        if self.updateTick >= 60:
            self.galaxyList[self.player.currentGalaxy].systemList[self.player.currentSystem].update(self.galaxyList, self.player, self.console)
            self.updateTick = 0

        self.draw(window)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key in [K_LSHIFT, K_RSHIFT]:
                    self.keyboard.shift = True
                elif event.key == K_BACKSPACE:
                    self.keyboard.backspace = True
                elif event.key == K_ESCAPE:
                    raise SystemExit
                else:
                    keyName = pygame.key.name(event.key)
                    self.inputBar.processInput(keyName, self)

            elif event.type == KEYUP:
                if event.key in [K_LSHIFT, K_RSHIFT]:
                    self.keyboard.shift = False
                elif event.key == K_BACKSPACE:
                    self.keyboard.backspace = False
                    self.keyboard.backspaceTick = -1
                
            elif event.type == QUIT:
                raise SystemExit

        self.keyboard.update()

    def processInputBarCommand(self, input):
        targetRoom = Room.exists(self.galaxyList, self.player.currentGalaxy, self.player.currentSystem, self.player.currentPlanet, self.player.currentArea, self.player.currentRoom)
        if targetRoom == None:
            targetRoom = self.galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
        
        # Look #
        if input.lower().split()[0] in ["look", "loo", "lo", "l"]:
            
            # Look 'Dir' #
            if len(input.split()) == 2 and input.lower().split()[1] in ["north", "nort", "nor", "no", "n", "east", "eas", "ea", "e", "south", "sout", "sou", "so", "s", "west", "wes", "we", "w"]:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"]:
                    targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"]:
                    targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"]:
                    targetDir = "South"
                else:
                    targetDir = "West"
                
                self.player.lookDirection(self.console, self.galaxyList, targetDir, 1)

            # Look 'Dir' '#' #
            elif len(input.split()) == 3 and input.lower().split()[1] in ["north", "nort", "nor", "no", "n", "east", "eas", "ea", "e", "south", "sout", "sou", "so", "s", "west", "wes", "we", "w"] and stringIsNumber(input.split()[2]) and int(input.split()[2]) > 0:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"]:
                    targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"]:
                    targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"]:
                    targetDir = "South"
                else:
                    targetDir = "West"
                
                self.player.lookDirection(self.console, self.galaxyList, targetDir, int(input.split()[2]))

            # Look Item/Mob #

            # Look Item/Mob 'Dir' #

            # Look Item/Mob 'Dir' '#' #

            # Look #
            elif len(input.split()) == 1:
                self.console.lineList.insert(0, {"Blank": True})
                targetRoom.display(self.console, self.galaxyList, self.player)

        # Movement - (North, East, South, West) #
        elif len(input.split()) == 1 and input.lower() in ["north", "nort", "nor", "no", "n", "east", "eas", "ea", "e", "south", "sout", "sou", "so", "s", "west", "wes", "we", "w"]:
            if input.lower() in ["north", "nort", "nor", "no", "n"]:
                targetDir = "North"
            elif input.lower() in ["east", "eas", "ea", "e"]:
                targetDir = "East"
            elif input.lower() in ["south", "sout", "sou", "so", "s"]:
                targetDir = "South"
            else:
                targetDir = "West"
            self.player.moveCheck(self.console, self.galaxyList, targetDir)

        # Open/Close #
        elif input.lower().split()[0] in ["open", "ope", "op", "o", "close", "clos", "clo", "cl"]:
            if input.lower().split()[0] in ["open", "ope", "op", "o"]:
                targetAction = "Open"
            else:
                targetAction = "Close"
            
            # Open/Close 'Direction' #
            if len(input.split()) == 2 and input.lower().split()[1] in ["north", "nort", "nor", "no", "n", "east", "eas", "ea", "e", "south", "sout", "sou", "so", "s", "west", "wes", "we", "w"]:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"]:
                    targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"]:
                    targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"]:
                    targetDir = "South"
                else:
                    targetDir = "West"
                
                targetRoom.openCloseDoorCheck(self.console, self.galaxyList, targetAction, targetDir)

            # Open/Close 'Object' #
            elif len(input.split()) > 1:
                pass

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": targetAction + " what?", "Code":str(len(targetAction)) + "w5w1y"})

        # Lock/Unlock #
        elif input.lower().split()[0] in ["lock", "loc", "unlock", "unloc", "unlo", "unl", "un"]:
            if input.lower().split()[0] in ["lock", "loc"]:
                targetAction = "Lock"
            else:
                targetAction = "Unlock"

            # Lock/Unlock 'Direction' #
            if len(input.split()) == 2 and input.lower().split()[1] in ["north", "nort", "nor", "no", "n", "east", "eas", "ea", "e", "south", "sout", "sou", "so", "s", "west", "wes", "we", "w"]:
                if input.lower().split()[1] in ["north", "nort", "nor", "no", "n"]:
                    targetDir = "North"
                elif input.lower().split()[1] in ["east", "eas", "ea", "e"]:
                    targetDir = "East"
                elif input.lower().split()[1] in ["south", "sout", "sou", "so", "s"]:
                    targetDir = "South"
                else:
                    targetDir = "West"
                
                targetRoom.lockUnlockDoorCheck(self.console, self.galaxyList, self.player, targetAction, targetDir)

            # Lock/Unlock 'Object' #
            elif len(input.split()) > 1:
                pass

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": targetAction + " what?", "Code":str(len(targetAction)) + "w5w1y"})

        # Get #
        elif input.lower().split()[0] in ["get", "ge", "g"]:

            # Get All #
            if len(input.split()) == 2 and input.split()[1].lower() == "all":
                self.player.getCheck(self.console, self.galaxyList, "All", "All")
                
            # Get All Item #
            elif len(input.split()) > 2 and input.split()[1].lower() == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.getCheck(self.console, self.galaxyList, targetItemKey, "All")

            # Get '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.getCheck(self.console, self.galaxyList, targetItemKey, int(input.split()[1]))

            # Get Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.getCheck(self.console, self.galaxyList, targetItemKey, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Get what?", "Code":"8w1y"})

        # Drop #
        elif input.lower().split()[0] in ["drop", "dro", "dr"]:

            # Drop All #
            if len(input.split()) == 2 and input.split()[1].lower() == "all":
                self.player.dropCheck(self.console, self.galaxyList, "All", "All")

            # Drop All Item #
            elif len(input.split()) > 2 and input.split()[1].lower() == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.dropCheck(self.console, self.galaxyList, targetItemKey, "All")

            # Drop '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.dropCheck(self.console, self.galaxyList, targetItemKey, int(input.split()[1]))

            # Drop Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.dropCheck(self.console, self.galaxyList, targetItemKey, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Drop what?", "Code":"9w1y"})

        # Inventory #
        elif input.lower().split()[0] in ["inventory", "inventor", "invento", "invent", "inven", "inve", "inv", "in", "i"]:
            
            # Display Armor Pocket #
            if len(input.split()) == 2 and input.lower().split()[1] in ["armor", "armo", "arm", "ar", "a"]:
                self.player.displayInventory(self.console, self.galaxyList, "Armor")
            
            # Display Misc. Pocket #
            elif len(input.split()) == 2 and input.lower().split()[1] in ["misc", "mis", "mi", "m"]:
                self.player.displayInventory(self.console, self.galaxyList, "Misc")

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String":"Open which bag? (Armor, Misc.)", "Code":"14w2y1r5w2y4w1y1r"})

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
            elif len(input.split()) > 2 and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                targetGearSlotIndex = int(input.split()[-1]) - 1
                targetItemKey = ' '.join(input.lower().split()[1:-1])
                self.player.wearCheck(self.console, targetItemKey, 1, targetGearSlotIndex)

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

        # Remove #
        elif input.lower().split()[0] in ["remove", "remov", "remo", "rem"]:

            # Remove All #
            if len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.removeCheck(self.console, "All", "All")

            # Remove All Item #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.removeCheck(self.console, targetItemKey, "All")

            # Remove Item 'GearSlot' #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0:
                targetGearSlotIndex = int(input.split()[-1]) - 1
                targetItemKey = ' '.join(input.lower().split()[1:-1])
                self.player.removeCheck(self.console, targetItemKey, 1, targetGearSlotIndex)

            # Remove '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.removeCheck(self.console, targetItemKey, int(input.split()[1]))

            # Remove Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.removeCheck(self.console, targetItemKey, 1)

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String": "Remove what?", "Code":"11w1y"})

        # Wield #

            # Wield All #

            # Wield All Item #

            # Wield '#' Item #

            # Wield Item #

        # Gear #
        elif len(input.split()) == 1 and input.lower() in ["gear", "gea"]:
            self.player.displayGear(self.console, self.galaxyList)

        # Board #

        # Time #
        elif len(input.split()) == 1 and input.lower() in ["time", "tim", "ti"]:
            currentPlanet = self.galaxyList[self.player.currentGalaxy].systemList[self.player.currentSystem].planetList[self.player.currentPlanet]
            currentPlanet.displayTime(self.console)

        # Weather #

        # Plant #

            # Plant All #

            # Plant All Item #

            # Plant '#' Item #

            # Plant Item #

        # Emotes #
        elif input.lower().split()[0] in self.player.emoteList:
            self.player.emote(self.console, input.lower())

        else:
            self.console.lineList.insert(0, {"Blank": True})
            self.console.lineList.insert(0, {"String": "Huh?", "Code":"3w1y"})

    def draw(self, window):
        window.fill([0, 0, 0])

        self.console.draw(window)
        self.inputBar.draw(window)
