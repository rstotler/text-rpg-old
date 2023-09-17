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
        roomLimbo = Room(0, 0, 0, 0, 0)
        roomLimbo.name = {"String":"Limbo"}

        areaLimbo = Area()
        areaLimbo.name = {"String":"Limbo"}
        areaLimbo.roomList.append(roomLimbo)

        starSol = Planet(0, 0, 0, 0, 38880, 0)
        starSol.name = {"String":"Sol"}
        starSol.type = "Star"
        starSol.axialTilt = 6
        starSol.areaList.append(areaLimbo)

        planetMercury = Planet(0, 0, 1, 29945, 84960, 126720)
        planetMercury.name = {"String":"Mercury"}
        
        planetVenus = Planet(0, 0, 2, 67443, 349920, 324000)
        planetVenus.name = {"String":"Venus"}
        planetVenus.axialTilt = 3
        
        roomCOTU00 = Room(0, 0, 3, 0, 0)
        roomCOTU00.name = {"String":"A Floating Platform"}
        roomCOTU00.exit["South"] = [0, 0, 3, 0, 1]
        roomCOTU00.description = [{"String":"You stand on a large floating platform in the middle of"},
                                  {"String":"space. Billions of multi-colored stars twinkle and flash", "Code":"5w2y13w1dc1c1ddc1w1y1r1dr1do1o1y1dy1ddy24w"},
                                  {"String":"from ages past.", "Code":"14w1y"}]
        for i in range(random.randrange(5, 15)):
            roomCOTU00.itemList.append(Item(1))
        for i in range(random.randrange(5, 15)):
            roomCOTU00.itemList.append(Item(2))
        for i in range(random.randrange(5, 15)):
            roomCOTU00.itemList.append(Item(3))
        roomCOTU00.itemList.append(Item(4))

        roomCOTU01 = Room(0, 0, 3, 0, 1)
        roomCOTU01.name = {"String":"Crystal Bridge To The Spaceport", "Code":"1c7dc1c6dc16w"}
        roomCOTU01.exit["North"] = [0, 0, 3, 0, 0]
        roomCOTU01.exit["South"] = [0, 0, 3, 0, 2]
        roomCOTU01.itemList.append(Item(5))

        roomCOTU02 = Room(0, 0, 3, 0, 2)
        roomCOTU02.name = {"String":"Spaceport Entrance", "Code":"18w"}
        roomCOTU02.exit["North"] = [0, 0, 3, 0, 1]

        areaCOTU = Area()
        areaCOTU.name = {"String":"Center Of The Universe"}
        areaCOTU.roomList.append(roomCOTU00)
        areaCOTU.roomList.append(roomCOTU01)
        areaCOTU.roomList.append(roomCOTU02)

        planetEarth = Planet(0, 0, 3, 93456, 1440, 525600)
        planetEarth.name = {"String":"Earth"}
        planetEarth.axialTilt = 23.5
        planetEarth.areaList.append(areaCOTU)
        planetEarth.updateNightDayTimers() # Update Night/Day Timers #

        systemSol = SolarSystem()
        systemSol.name = {"String":"Sol"}
        systemSol.planetList.append(starSol)
        systemSol.planetList.append(planetMercury)
        systemSol.planetList.append(planetVenus)
        systemSol.planetList.append(planetEarth)
        
        galaxyMilkyWay = Galaxy()
        galaxyMilkyWay.name = {"String":"Milky Way"}
        galaxyMilkyWay.systemList.append(systemSol)

        self.galaxyList.append(galaxyMilkyWay)

        # Load Doors AFTER ALL Rooms Are Loaded! #
        roomCOTU01.installDoor(self.galaxyList, "North", "Manual", "1234")
        roomCOTU02.installDoor(self.galaxyList, "North", "Automatic", "Spaceport")
        roomCOTU02.lockUnlockDoor(self.galaxyList, "Lock", "North")

    def update(self, window):
        self.processInput()
        self.inputBar.update(self.keyboard)

        self.updateTick += 1
        if self.updateTick >= 1:
            self.galaxyList[self.player.currentGalaxy].systemList[self.player.currentSystem].update(self.player, self.console)
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

            # Look #
            else:
                self.console.lineList.insert(0, {"Blank": True})
                targetRoom.display(self.console, self.galaxyList)

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
                self.player.displayInventory(self.console, "Armor")
            
            # Display Misc. Pocket #
            elif len(input.split()) == 2 and input.lower().split()[1] in ["misc", "mis", "mi", "m"]:
                self.player.displayInventory(self.console, "Misc")

            else:
                self.console.lineList.insert(0, {"Blank": True})
                self.console.lineList.insert(0, {"String":"Open which bag? (Armor, Misc.)", "Code":"14w2y1r5w2y4w1y1r"})

        # Time #
        elif len(input.split()) == 1 and input.lower() in ["time", "tim", "ti"]:
            currentPlanet = self.galaxyList[self.player.currentGalaxy].systemList[self.player.currentSystem].planetList[self.player.currentPlanet]
            currentPlanet.displayTime(self.console)

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
