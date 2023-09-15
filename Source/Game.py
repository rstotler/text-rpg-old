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

        self.loadGame()

    def loadGame(self):
        roomCOTU00 = Room()
        roomCOTU00.name = {"String":"Limbo"}
        roomCOTU01 = Room()
        roomCOTU01.name = {"String":"A Floating Platform"}
        roomCOTU01.exit["North"] = [0, 0, 0, 0, 2]
        roomCOTU01.description = [{"String":"You stand on a large floating platform in the middle of"},
                                  {"String":"space. Billions of multi-colored stars twinkle and flash", "Code":"5w2y13w1dc1c1ddc1w1y1r1dr1do1o1y1dy1ddy24w"},
                                  {"String":"from ages past.", "Code":"14w1y"}]
        for i in range(random.randrange(5, 15)):
            roomCOTU01.itemList.append(Item(1))
        for i in range(random.randrange(5, 15)):
            roomCOTU01.itemList.append(Item(2))
        for i in range(random.randrange(5, 15)):
            roomCOTU01.itemList.append(Item(3))

        roomCOTU02 = Room()
        roomCOTU02.name = {"String":"A Crystaline Bridge", "Code":"2w11c6w"}
        roomCOTU02.exit["South"] = [0, 0, 0, 0, 1]

        areaCOTU = Area()
        areaCOTU.name = {"String":"Center Of The Universe"}
        areaCOTU.roomList.append(roomCOTU00)
        areaCOTU.roomList.append(roomCOTU01)
        areaCOTU.roomList.append(roomCOTU02)

        planetEarth = Planet()
        planetEarth.name = {"String":"Earth"}
        planetEarth.areaList.append(areaCOTU)

        systemSol = SolarSystem()
        systemSol.name = {"String":"Sol"}
        systemSol.planetList.append(planetEarth)

        galaxyMilkyWay = Galaxy()
        galaxyMilkyWay.name = {"String":"Milky Way"}
        galaxyMilkyWay.systemList.append(systemSol)

        self.galaxyList.append(galaxyMilkyWay)

    def update(self, window):
        self.processInput()
        self.inputBar.update(self.keyboard)

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

        # Look #
        if input.lower() in ["look", "loo", "lo", "l"]:
            targetRoom = Room.exists(self.galaxyList, self.player.currentGalaxy, self.player.currentSystem, self.player.currentPlanet, self.player.currentArea, self.player.currentRoom)
            if targetRoom == None:
                targetRoom = self.galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
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

        else:
            self.console.lineList.insert(0, {"Blank": True})
            self.console.lineList.insert(0, {"String": "Huh?", "Code":"3w1y"})

    def draw(self, window):
        window.fill([0, 0, 0])

        self.console.draw(window)
        self.inputBar.draw(window)
