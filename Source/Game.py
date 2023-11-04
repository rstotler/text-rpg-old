import pygame, random
from pygame import *
from Screen.Console import Console
from Screen.InputBar import InputBar
from Screen.Map import Map
from Screen.RoomScreen import RoomScreen
from Components.Keyboard import Keyboard
from GameData.Config import Config
from GameData.Player.Player import Player
from GameData.Player.Action import Action
from GameData.Player.Skill import Skill
from GameData.Player.CombatSkill import CombatSkill
from GameData.World.Galaxy import Galaxy
from GameData.World.SolarSystem import SolarSystem
from GameData.World.Planet import Planet
from GameData.World.Area import Area
from GameData.World.Room import Room
from GameData.World.Spaceship import Spaceship
from GameData.Item.Item import Item
from GameData.Item.Components.Button import Button
from Components.Utility import *

# To Do List:
    # Tropes:
        # Elemental Planetary Energy
        # Computer/Hacking/Simulation/Breaking The Third Wall
        # Love Story
    # Test To Do:
        # Make Player Lose Sight Of Mobs On Darkness & Other Darkness Effects
        # Let Player Do 'All' Combat Skills In Rooms Without Mobs
        # Stack Damage In Attack Messages
        # Message Data For Stunning Enemy On Failed Block
        # Make Combat Prioritize Hitting Available Targets In Player.targetList First
        # Mute Mob Speech If More Than One Copy In Room
        # Create & Apply .stunCheck In CombatSkill, Go Over Stun/Stumble
        # Attacks With Knockback (Explosives)
        # Auto-Combat
        # Counter-Attack (Passive Skill)
        # Enemy Groups
        # Move Direction '#'
        # Bleeding
        # Add Mob To Player Target List If Mob Attacks First (Agro Mobs)
        # Make Reload Function Prioritize Guns Over Magazines/Etc. ("Reload 45" Tries To Reload Magazine First)
        # Wall Texture
    # Other To Do:
        # Gun Mods, Scopes Modify Accuracy
        # Add Item Skills To Skill List
        # Mob Vs. Mob Combat
        # Moons
        # Reload Messages For Mobs
        # Make Sure Items Don't Generate Over Special Item Numbers

class Game:

    def __init__(self):
        self.keyboard = Keyboard()
        self.console = Console()
        self.inputBar = InputBar()
        self.map = Map()
        self.roomScreen = RoomScreen()

        self.player = Player(0, 0, 3, 1, 1, None, None)
        self.galaxyList = []
        self.config = Config()

        self.frameTick = 0
        
        self.loadGame()
        
    def loadGame(self):
        galaxyProtoMilkyWay = Galaxy()
        self.galaxyList.append(galaxyProtoMilkyWay)
        galaxyProtoMilkyWay.name = {"String":"Proto Milky Way"}

        # (System) Proto Sol #
        if True:
            systemProtoSol = SolarSystem()
            galaxyProtoMilkyWay.systemList.append(systemProtoSol)
            systemProtoSol.name = {"String":"Proto Sol", "Code":"9w"}

            protoSolName = {"String":"Proto Sol", "Code":"1w5ddw1y2ddy"}
            starProtoSol = Planet(self.galaxyList, 0, 0, 0, protoSolName, "Star", 0, 38880, 0, 7.25, 865370)
            systemProtoSol.planetList.append(starProtoSol)
            starProtoSol.type = "Star"

            areaLimboName = {"String":"Limbo", "Code":"5w"}
            areaLimbo = Area(0, areaLimboName)
            starProtoSol.areaList.append(areaLimbo)

            roomLimbo = Room(0, 0, 0, 0, 0, "Limbo")
            areaLimbo.roomList.append(roomLimbo)

            protoMercuryName = {"String":"Proto Mercury", "Code":"13w"}
            planetProtoMercury = Planet(self.galaxyList, 0, 0, 1, protoMercuryName, "Planet", 29945, 84960, 126720, 0, 3031)
            systemProtoSol.planetList.append(planetProtoMercury)
            protoVenusName = {"String":"Proto Venus", "Code":"11w"}
            planetProtoVenus = Planet(self.galaxyList, 0, 0, 2, protoVenusName, "Planet", 67443, 349920, 324000, 2.63, 7520)
            systemProtoSol.planetList.append(planetProtoVenus)
            planetProtoVenus.orbit = "Clockwise"

            protoEarthName = {"String":"Proto Earth", "Code":"1w5ddw1b4db"}
            planetProtoEarth = Planet(self.galaxyList, 0, 0, 3, protoEarthName, "Planet", 93456, 1440, 525600, 23.43, 7917)
            systemProtoSol.planetList.append(planetProtoEarth)
            
            planetProtoEarth.currentMinutesInDay = 480
            planetProtoEarth.currentMinutesInYear = 480
            planetProtoEarth.updateNightDayTimers()
            planetProtoEarth.updatePosition()

            protoMarsName = {"String":"Proto Mars", "Code":"1w5ddw1dr3ddr"}
            planetProtoMars = Planet(self.galaxyList, 0, 0, 4, protoMarsName, "Planet", 148120, 1477, 989280, 25.19, 4212)
            systemProtoSol.planetList.append(planetProtoMars)
            protoJupiterName = {"String":"Proto Jupiter", "Code":"13w"}
            planetProtoJupiter = Planet(self.galaxyList, 0, 0, 5, protoJupiterName, "Planet", 484000000, 596, 6239520, 3.13, 86881)
            systemProtoSol.planetList.append(planetProtoJupiter)
            protoSaturnName = {"String":"Proto Saturn", "Code":"12w"}
            planetProtoSaturn = Planet(self.galaxyList, 0, 0, 6, protoSaturnName, "Planet", 886000000, 634, 15448640, 26.73, 72367)
            systemProtoSol.planetList.append(planetProtoSaturn)
            protoUranusName = {"String":"Proto Uranus", "Code":"12w"}
            planetProtoUranus = Planet(self.galaxyList, 0, 0, 7, protoUranusName, "Planet", 1824000000, 1034, 44189280, 97.77, 31518)
            systemProtoSol.planetList.append(planetProtoUranus)
            protoNeptuneName = {"String":"Proto Neptune", "Code":"13w"}
            planetProtoNeptune = Planet(self.galaxyList, 0, 0, 8, protoNeptuneName, "Planet", 2779300000, 966, 86673600, 28.32, 30599)
            systemProtoSol.planetList.append(planetProtoNeptune)
            protoPlutoName = {"String":"Proto Pluto", "Code":"11w"}
            planetProtoPluto = Planet(self.galaxyList, 0, 0, 9, protoPlutoName, "Planet", 3700000000, 9180, 130348800, 119.61, 1476)
            systemProtoSol.planetList.append(planetProtoPluto)

        planetProtoEarth.createContinent(self.galaxyList, [25, 25])

        # Test Zone #
        if False:
            planetProtoEarth.areaList[0].roomList[208].inside = True
            planetProtoEarth.areaList[0].roomList[183].inside = True
            # planetProtoEarth.areaList[0].roomList[158].inside = True

            planetProtoEarth.areaList[0].roomList[209].inside = True
            planetProtoEarth.areaList[0].roomList[184].inside = True
            planetProtoEarth.areaList[0].roomList[159].inside = True

            planetProtoEarth.areaList[0].roomList[210].inside = True
            planetProtoEarth.areaList[0].roomList[185].inside = True
            planetProtoEarth.areaList[0].roomList[160].inside = True
            
            planetProtoEarth.areaList[0].roomList[211].inside = True
            # planetProtoEarth.areaList[0].roomList[186].inside = True
            planetProtoEarth.areaList[0].roomList[161].inside = True

            planetProtoEarth.areaList[0].roomList[212].inside = True
            planetProtoEarth.areaList[0].roomList[187].inside = True
            planetProtoEarth.areaList[0].roomList[162].inside = True

        areaCOTUNum = len(planetProtoEarth.areaList)
        areaIceCavernNum = areaCOTUNum + 1

        # (Area) Center of the Universe #
        if True:
            areaCOTUName = {"String":"Center of the Universe", "Code":"22w"}
            areaCOTU = Area(areaCOTUNum, areaCOTUName)
            planetProtoEarth.areaList.append(areaCOTU)

            roomCOTU00Name = {"String":"Center of the Universe", "Code":"1w1ddw1da2dw2da1dw2ddw1da1dw1w2w2dw2ddw1da2ddw"}
            roomCOTU00 = Room(0, 0, 3, areaCOTUNum, 0, roomCOTU00Name)
            areaCOTU.roomList.append(roomCOTU00)
            roomCOTU00.exit["South"] = [0, 0, 3, areaCOTUNum, 1]
            roomCOTU00.exit["North"] = [0, 0, 3, areaCOTUNum, 3]
            roomCOTU00.exit["East"] = [0, 0, 3, areaIceCavernNum, 0]
            roomCOTU00.exit["West"] = [0, 0, 3, 0, 260] # Temporary Debug Teleporter To Earth
            roomCOTU00.description = [{"String":"You stand on a large floating platform at the Center of the", "Code":"46w1w1ddw1da2dw2da1dw2ddw1da1dw1w"},
                                    {"String":"Universe. Billions of multi-colored stars twinkle and flash", "Code":"1w2dw2ddw1da2ddw2y13w1dc1c1ddc1w1y1r1dr1do1o1y1dy1ddy7w1c1dc1ddc2dc1c1ddc5w1c1dc1ddc1dc1c"},
                                    {"String":"from ages past. You see a bridge leading to the Spaceport", "Code":"14w2y32w1w1dw2ddw1dw1w1dw1ddw1dw"},
                                    {"String":"to the South and a garden to the North.", "Code":"7w1w5ddw6w1g1dg1ddg1g1dg1ddg8w1w4ddw1y"}]
            
            roomCOTU01Name = {"String":"Bridge To The Spaceport", "Code":"14w1w1dw2ddw1dw1w1dw1ddw1dw"}
            roomCOTU01 = Room(0, 0, 3, areaCOTUNum, 1, roomCOTU01Name)
            areaCOTU.roomList.append(roomCOTU01)
            roomCOTU01.exit["North"] = [0, 0, 3, areaCOTUNum, 0]
            roomCOTU01.exit["South"] = [0, 0, 3, areaCOTUNum, 2]
            roomCOTU01.mobList.append(Player(0, 0, 3, areaCOTUNum, 1, None, 1))

            roomCOTU02Name = {"String":"Spaceport Entrance", "Code":"1w1dw2ddw1dw1w1dw1ddw1dw9w"}
            roomCOTU02 = Room(0, 0, 3, areaCOTUNum, 2, roomCOTU02Name)
            areaCOTU.roomList.append(roomCOTU02)
            roomCOTU02.exit["North"] = [0, 0, 3, areaCOTUNum, 1]
            roomCOTU02.exit["South"] = [0, 0, 3, areaCOTUNum, 5]
            roomCOTU02.exit["East"] = [0, 0, 3, areaCOTUNum, 6]
            roomCOTU02.inside = True

            roomCOTU03Name = {"String":"A Peaceful Garden", "Code":"2w1w1dw2ddw1dw1w1ddw1da1w1g1dg1ddg1g1dg1ddg"}
            roomCOTU03 = Room(0, 0, 3, areaCOTUNum, 3, roomCOTU03Name)
            areaCOTU.roomList.append(roomCOTU03)
            roomCOTU03.exit["South"] = [0, 0, 3, areaCOTUNum, 0]
            roomCOTU03.exit["West"] = [0, 0, 3, areaCOTUNum, 4]

            for i in range(16):
                createItem(i + 1, "Weapon", 2, roomCOTU03)
            for i in range(10):
                quantity = None
                if i + 1 not in [1, 3, 5, 7]:
                    quantity = 25
                createItem(i + 1, "Ammo", quantity, roomCOTU03)

            roomCOTU04Name = {"String":"A Little Wooden Shack", "Code":"9w1do1ddo1dddo1do1ddo1dddo6w"}
            roomCOTU04 = Room(0, 0, 3, areaCOTUNum, 4, roomCOTU04Name)
            areaCOTU.roomList.append(roomCOTU04)
            roomCOTU04.exit["East"] = [0, 0, 3, areaCOTUNum, 3]
            roomCOTU04.inside = True

            roomCOTU05Name = {"String":"COTU Landing Pad", "Code":"16w"}
            roomCOTU05 = Room(0, 0, 3, areaCOTUNum, 5, roomCOTU05Name)
            areaCOTU.roomList.append(roomCOTU05)
            roomCOTU05.exit["North"] = [0, 0, 3, areaCOTUNum, 2]
            roomCOTU05.flags["Landing Site"] = True

            roomCOTU06Name = {"String":"COTU Training Center Hall", "Code":"25w"}
            roomCOTU06 = Room(0, 0, 3, areaCOTUNum, 6, roomCOTU06Name)
            areaCOTU.roomList.append(roomCOTU06)
            roomCOTU06.exit["West"] = [0, 0, 3, areaCOTUNum, 2]
            roomCOTU06.exit["Up"] = [0, 0, 3, areaCOTUNum, 7]

            roomCOTU07Name = {"String":"COTU Training Center Floor 1", "Code":"28w"}
            roomCOTU07 = Room(0, 0, 3, areaCOTUNum, 7, roomCOTU07Name)
            areaCOTU.roomList.append(roomCOTU07)
            roomCOTU07.exit["Down"] = [0, 0, 3, areaCOTUNum, 6]
            roomCOTU07.exit["North"] = [0, 0, 3, areaCOTUNum, 8]

            roomCOTU08Name = {"String":"Unarmed Mobs Room", "Code":"17w"}
            roomCOTU08 = Room(0, 0, 3, areaCOTUNum, 8, roomCOTU08Name)
            areaCOTU.roomList.append(roomCOTU08)
            roomCOTU08.exit["South"] = [0, 0, 3, areaCOTUNum, 7]
            unarmedUnskilledControlPanel = createItem(5)
            unarmedUnskilledFlagList = {"Num":2, "Label":{"String":"[1] - Unarmed, Unskilled Mob", "Code":"1r1w1r3y7w2y13w"}, "Key List":["1"], "Skill List":[1], "Gear Dict":{}}
            unarmedUnskilledControlPanel.buttonList.append(Button("Spawn Mob", unarmedUnskilledFlagList))
            roomCOTU08.itemList.append(unarmedUnskilledControlPanel)

            # Zero Area Coordinates #
            areaCOTU.zeroCoordinates(self.galaxyList)

            # Load Doors #
            roomCOTU02.installDoor(self.galaxyList, "North", "Automatic", "COTU Spaceport")
            roomCOTU02.lockUnlockDoor(self.galaxyList, "Lock", "North")
            roomCOTU04.installDoor(self.galaxyList, "East", "Manual", None, "Open")

        # (Spaceship) COTU Transport Ship #
        if True:
            cotuTransportShipName = {"String":"COTU Transport Ship", "Code":"19w"}
            cotuTransportShip = Spaceship(self.galaxyList, cotuTransportShipName, "COTU Spaceport", [0, 0, 3, areaCOTUNum, 5], [0, 1], [0, 0])
            roomCOTU05.spaceshipList.append(cotuTransportShip)
            systemProtoSol.spaceshipList.append(cotuTransportShip)

        # (Area) Ice Cavern
        if True:
            areaIceCavernString = {"String":"Ice Cavern", "Code":"10w"}
            areaIceCavern = Area(areaIceCavernNum, areaIceCavernString)
            planetProtoEarth.areaList.append(areaIceCavern)

            roomIceCavern00Name = {"String":"Frozen Entryway", "Code":"1dc1ddc1dw1dc1ddc1dw1dc1ddc1dw1dc1ddc1dw1dc1ddc1dw"}
            roomIceCavern00 = Room(0, 0, 3, areaIceCavernNum, 0, roomIceCavern00Name)
            areaIceCavern.roomList.append(roomIceCavern00)
            roomIceCavern00.exit["West"] = [0, 0, 3, areaCOTUNum, 0]
            roomIceCavern00.exit["North"] = [0, 0, 3, areaIceCavernNum, 1]
            roomIceCavern00.inside = True

            roomIceCavern01Name = {"String":"Ice Cavern", "Code":"4w6w"}
            roomIceCavern01 = Room(0, 0, 3, areaIceCavernNum, 1, roomIceCavern01Name)
            areaIceCavern.roomList.append(roomIceCavern01)
            roomIceCavern01.exit["South"] = [0, 0, 3, areaIceCavernNum, 0]
            roomIceCavern01.exit["East"] = [0, 0, 3, areaIceCavernNum, 2]
            roomIceCavern01.inside = True

            roomIceCavern02Name = {"String":"Ice Cavern", "Code":"4w6w"}
            roomIceCavern02 = Room(0, 0, 3, areaIceCavernNum, 2, roomIceCavern02Name)
            areaIceCavern.roomList.append(roomIceCavern02)
            roomIceCavern02.exit["West"] = [0, 0, 3, areaIceCavernNum, 1]
            roomIceCavern02.exit["North"] = [0, 0, 3, areaIceCavernNum, 3]
            roomIceCavern02.inside = True

            roomIceCavern03Name = {"String":"Ice Cavern", "Code":"4w6w"}
            roomIceCavern03 = Room(0, 0, 3, areaIceCavernNum, 3, roomIceCavern03Name)
            areaIceCavern.roomList.append(roomIceCavern03)
            roomIceCavern03.exit["South"] = [0, 0, 3, areaIceCavernNum, 2]
            roomIceCavern03.inside = True

            # Zero Area Coordinates #
            areaIceCavern.zeroCoordinates(self.galaxyList)

            # Load Doors #
            roomIceCavern00.installDoor(self.galaxyList, "North", "Hidden", None, "Closed", True)
            roomIceCavern00.searchList.append({"Type":"Hidden Door", "Target Direction":"North", "Key List":["wall"], "Open Display String":"You find a loose section of rock, pull on it, and the cave wall before you opens up!", "Open Display Code":"32w1y11w1y38w1y"})

        # Milky Way & Sol #
        if True:
            galaxyMilkyWay = Galaxy()
            self.galaxyList.append(galaxyMilkyWay)
            galaxyMilkyWay.name = {"String":"Milky Way"}

            systemSol = SolarSystem()
            galaxyMilkyWay.systemList.append(systemSol)
            systemSol.name = {"String":"Sol", "Code":"3w"}

            solName = {"String":"Sol", "Code":"3w"}
            starSol = Planet(self.galaxyList, 1, 1, 0, solName, "Star", 0, 38880, 0, 7.25, 865370)
            systemSol.planetList.append(starSol)
            starSol.type = "Star"

            mercuryName = {"String":"Mercury", "Code":"7w"}
            planetMercury = Planet(self.galaxyList, 1, 1, 1, mercuryName, "Planet", 29945, 84960, 126720, 0, 3031)
            systemSol.planetList.append(planetMercury)
            
            venusName = {"String":"Venus", "Code":"5w"}
            planetVenus = Planet(self.galaxyList, 1, 1, 2, venusName, "Planet", 67443, 349920, 324000, 2.63, 7520)
            systemSol.planetList.append(planetVenus)
            planetVenus.orbit = "Clockwise"
            
            earthName = {"String":"Earth", "Code":"5w"}
            planetEarth = Planet(self.galaxyList, 1, 1, 3, earthName, "Planet", 93456, 1440, 525600, 23.43, 7917)
            systemSol.planetList.append(planetEarth)

            marsName = {"String":"Mars", "Code":"4w"}
            planetMars = Planet(self.galaxyList, 1, 1, 4, marsName, "Planet", 148120, 1477, 989280, 25.19, 4212)
            systemSol.planetList.append(planetMars)
            jupiterName = {"String":"Jupiter", "Code":"7w"}
            planetJupiter = Planet(self.galaxyList, 1, 1, 5, jupiterName, "Planet", 484000000, 596, 6239520, 3.13, 86881)
            systemSol.planetList.append(planetJupiter)
            saturnName = {"String":"Saturn", "Code":"6w"}
            planetSaturn = Planet(self.galaxyList, 1, 1, 6, saturnName, "Planet", 886000000, 634, 15448640, 26.73, 72367)
            systemSol.planetList.append(planetSaturn)
            uranusName = {"String":"Uranus", "Code":"6w"}
            planetUranus = Planet(self.galaxyList, 1, 1, 7, uranusName, "Planet", 1824000000, 1034, 44189280, 97.77, 31518)
            systemSol.planetList.append(planetUranus)
            neptuneName = {"String":"Neptune", "Code":"7w"}
            planetNeptune = Planet(self.galaxyList, 1, 1, 8, neptuneName, "Planet", 2779300000, 966, 86673600, 28.32, 30599)
            systemSol.planetList.append(planetNeptune)
            plutoName = {"String":"Pluto", "Code":"5w"}
            planetPluto = Planet(self.galaxyList, 1, 1, 9, plutoName, "Planet", 3700000000, 9180, 130348800, 119.61, 1476)
            systemSol.planetList.append(planetPluto)

        # Load Map #
        playerArea, playerRoom = Room.getAreaAndRoom(self.galaxyList, self.player)
        self.map.loadAreaMap(playerArea)
        self.map.loadSystemMap(self.galaxyList[self.player.galaxy].systemList[self.player.system])

        # Test Variables #
        # self.inputBar.inputList = ["n", "n", "w", "get pis from cab", "get pis from cab", "get 4 mag from cab", "drop 2 mag", "get 3 round from cab", "wear pis", "wear pis", "get sta from cab", "e", "s", "s"]
        # self.inputBar.inputList = ["n", "n", "w", "get sniper from cab", "get 5.56 from cab", "get 5.56 from cab", "get 5.56 from cab", "e", "s", "s", "wear sni", "reload"]
        # self.inputBar.inputList = ["s", "s", "board ship", "n"]
        # self.inputBar.inputList = ["s", "e", "u", "n"]
        # self.inputBar.inputList = ["man mob 2", "man mob 3", "man mob 1", "man mob 2", "n", "n"]
        self.inputBar.inputList = ["n", "n", "get sw", "get 45", "get 45", "get 45", "get 45", "get 45", "drop 45", "wear all", "s", "s", "drop 1 sta", "rel"]

        # Load Skills #
        for i in range(3):
            skill = CombatSkill(1001 + i)
            for weaponType in skill.weaponTypeList[0]:
                self.player.combatSkillDict[weaponType].append(skill)
        for i in range(6) : self.player.combatSkillDict["Melee"].append(CombatSkill(1 + i))
        for i in range(1) : self.player.combatSkillDict["Blunt"].append(CombatSkill(251 + i))
        for i in range(2) : self.player.combatSkillDict["Polearm"].append(CombatSkill(301 + i))
        for i in range(1) : self.player.combatSkillDict["Bow"].append(CombatSkill(451 + i))
        for i in range(1) : self.player.combatSkillDict["Pistol"].append(CombatSkill(501 + i))
        for i in range(2) : self.player.combatSkillDict["Rifle"].append(CombatSkill(551 + i))

        self.player.itemDict["Key"].append(createItem(1))
        self.player.gearDict["Finger"][0] = createItem(8, "Armor")

    def draw(self, window):
        window.fill([0, 0, 0])

        self.console.draw(window)
        self.inputBar.draw(window, self.galaxyList, self.player)
        self.map.draw(window, self.galaxyList, self.player)
        self.roomScreen.draw(window, self.galaxyList, self.player)

    def update(self, window):
        self.processInput()
        self.inputBar.update(self)
        
        if self.frameTick == 0:
            self.galaxyList[self.player.galaxy].systemList[self.player.system].update(self.galaxyList, self.player, self.console)
            playerArea, playerRoom = Room.getAreaAndRoom(self.galaxyList, self.player)
            if playerRoom.spaceshipObject != None:
                playerRoom.spaceshipObject.update(self.console, self.galaxyList, self.player)
        if self.frameTick in [0, 30]:
            if self.frameTick == 30:
                playerArea, playerRoom = Room.getAreaAndRoom(self.galaxyList, self.player)
            updateAreaList, updateRoomList = Room.getSurroundingRoomData(self.galaxyList, playerArea, playerRoom, 5)
            
            messageDataList = []
            playerArea.update(self.console)
            messageDataList = self.player.update(self.config, self.console, self.map, self.galaxyList, self.player, playerRoom, messageDataList)
            for room in updateRoomList:
                for mob in room.mobList:
                    messageDataList = mob.update(self.config, self.console, self.map, self.galaxyList, self.player, room, messageDataList)
            for messageData in messageDataList:
                self.console.write(messageData["String"], messageData["Code"], messageData["Draw Blank Line"])

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
                    if not (len(self.player.actionList) > 0 and self.player.actionList[0].actionType in ["Stumble", "Stun"]):
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
        directionStringList = ["north", "nort", "nor", "no", "n", "east", "eas", "ea", "e", "south", "sout", "sou", "so", "s", "west", "wes", "we", "w", "up", "u", "down", "dow", "do", "d"]
        combatSkill, parsedCombatInput = CombatSkill.parseSkillString(input.lower(), self.player.getCombatSkillList(True))
        currentRoom = Room.exists(self.galaxyList, self.player.spaceship, self.player.galaxy, self.player.system, self.player.planet, self.player.area, self.player.room)
        if currentRoom == None:
            currentRoom = self.galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
        
        ## Basic Commands ##
        # Look/Examine #
        if input.lower().split()[0] in ["look", "loo", "lo", "l", "examine", "examin", "exami", "exam", "exa", "ex"]:
            
            # Look 'Direction' #
            if len(input.split()) == 2 and input.lower().split()[1] in directionStringList:
                targetDirKey = input.lower().split()[1]
                self.player.lookDirection(self.console, self.galaxyList, currentRoom, targetDirKey, 1)

            # Look 'Direction' '#' #
            elif len(input.split()) == 3 and input.lower().split()[1] in directionStringList and stringIsNumber(input.split()[2]) and int(input.split()[2]) > 0:
                targetDirKey = input.lower().split()[1]
                self.player.lookDirection(self.console, self.galaxyList, currentRoom, targetDirKey, int(input.split()[2]))

            # Look 'Direction' '#' Item/Mob/Spaceship #
            elif len(input.split()) > 3 and input.lower().split()[1] in directionStringList and stringIsNumber(input.split()[2]) and int(input.split()[2]) > 0:
                targetDirKey = input.lower().split()[1]
                lookTarget = ' '.join(input.lower().split()[3::])
                self.player.lookTargetCheck(self.console, self.galaxyList, self.player, currentRoom, targetDirKey, int(input.split()[2]), lookTarget)

            # Look 'Direction' Item/Mob/Spaceship #
            elif len(input.split()) > 2 and input.lower().split()[1] in directionStringList:
                targetDirKey = input.lower().split()[1]
                lookTarget = ' '.join(input.lower().split()[2::])
                self.player.lookTargetCheck(self.console, self.galaxyList, self.player, currentRoom, targetDirKey, 1, lookTarget)

            # Look Item In Container #
            elif len(input.split()) > 3 and "in" in input.lower().split() and input.lower().split()[1] != "in" and input.lower().split()[-1] != "in":
                inIndex = input.lower().split().index("in")
                targetItemKey = ' '.join(input.lower().split()[1:inIndex])
                targetContainerKey = ' '.join(input.lower().split()[inIndex + 1::])
                self.player.lookItemInContainerCheck(self.console, currentRoom, targetItemKey, targetContainerKey)

            # Look Item/Mob/Spaceship/Inventory/Gear #
            elif len(input.split()) > 1:
                lookTarget = ' '.join(input.lower().split()[1::])
                self.player.lookTargetCheck(self.console, self.galaxyList, self.player, currentRoom, None, None, lookTarget)

            # Look #
            elif len(input.split()) == 1 and input.lower().split()[0] in ["look", "loo", "lo", "l"]:
                currentRoom.display(self.console, self.galaxyList, self.player)

            # Examine #
            elif len(input.split()) == 1 and len(self.player.targetList) > 0:
                self.player.targetList[0].lookDescription(self.console, self.galaxyList, self.player, currentRoom)
                
            else:
                self.console.write("Examine what?", "12w1y", True)

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
                self.console.write("Target what?", "11w1y", True)

        # Untarget #
        elif input.lower().split()[0] in ["untarget", "untarge", "untarg", "untar", "unta", "unt", "un"]:

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
                targetDirKey = input.lower().split()[1]
                self.player.openCloseDoorCheck(self.console, self.galaxyList, self.player, currentRoom, targetAction, targetDirKey)

            # Open/Close Target #
            elif len(input.split()) > 1:
                self.player.openCloseTargetCheck(self.console, self.galaxyList, self.player, currentRoom, targetAction, ' '.join(input.lower().split()[1::]))

            else:
                self.console.write(targetAction + " what?", str(len(targetAction)) + "w5w1y", True)

        # Lock/Unlock #
        elif input.lower().split()[0] in ["lock", "loc", "unlock", "unloc", "unlo"]:
            if input.lower().split()[0] in ["lock", "loc"] : targetAction = "Lock"
            else : targetAction = "Unlock"

            # Lock/Unlock 'Direction' #
            if len(input.split()) == 2 and input.lower().split()[1] in directionStringList:
                targetDirKey = input.lower().split()[1]
                self.player.lockUnlockDoorCheck(self.console, self.galaxyList, self.player, currentRoom, targetAction, targetDirKey)

            # Lock/Unlock Target #
            elif len(input.split()) > 1:
                self.player.lockUnlockTargetCheck(self.console, self.galaxyList, self.player, currentRoom, targetAction, ' '.join(input.lower().split()[1::]))

            else:
                self.console.write(targetAction + " what?", str(len(targetAction)) + "w5w1y", True)

        # Get #
        elif input.lower().split()[0] in ["get", "ge", "g"]:

            # Get All Item From All (Loot Item From All) #
            if len(input.split()) > 4 and input.lower().split()[1] == "all" and "from" in input.lower().split() and input.lower().split()[2] != "from" and input.lower().split()[-1] == "all":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[2:fromIndex])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, "All", "All")
             
            # Get All Item From Container (Loot Item From Container) #
            elif len(input.split()) > 4 and input.lower().split()[1] == "all" and "from" in input.lower().split() and input.lower().split()[2] != "from" and input.lower().split()[-1] != "from":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[2:fromIndex])
                targetContainerKey = ' '.join(input.lower().split()[fromIndex + 1::])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, targetContainerKey, "All")

            # Get All From All (Loot All) #
            elif len(input.split()) == 4 and input.lower().split()[1] == "all" and input.lower().split()[2] == "from" and input.lower().split()[3] == "all":
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, "All", "All", "All")

            # Get All From Container (Loot Container) #
            elif len(input.split()) > 3 and input.lower().split()[1] == "all" and input.lower().split()[2] == "from":
                targetContainerKey = ' '.join(input.lower().split()[3::])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, "All", targetContainerKey, "All")

            # Get '#' Item From All #
            elif len(input.split()) > 4 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and "from" in input.lower().split() and input.lower().split()[2] != "from" and input.lower().split()[-1] == "all":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[2:fromIndex])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, "All", int(input.split()[1]))

            # Get '#' Item From Container #
            elif len(input.split()) > 4 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and "from" in input.lower().split() and input.lower().split()[2] != "from" and input.lower().split()[-1] != "from":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[2:fromIndex])
                targetContainerKey = ' '.join(input.lower().split()[fromIndex + 1::])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, targetContainerKey, int(input.split()[1]))

            # Get Item From All #
            elif len(input.split()) > 3 and input.lower().split()[-2] == "from" and input.lower().split()[-1] == "all":
                targetItemKey = ' '.join(input.lower().split()[1:-2])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, "All", 1)

            # Get Item From Container #
            elif len(input.split()) > 3 and "from" in input.lower().split() and input.lower().split()[1] != "from" and input.lower().split()[-1] != "from":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[1:fromIndex])
                targetContainerKey = ' '.join(input.lower().split()[fromIndex + 1::])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, targetContainerKey, 1)

            # Get All #
            elif len(input.split()) == 2 and input.split()[1].lower() == "all":
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, "All", None, "All")
                
            # Get All Item #
            elif len(input.split()) > 2 and input.split()[1].lower() == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, None, "All")

            # Get '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, None, int(input.split()[1]))

            # Get Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, None, 1)

            else:
                self.console.write("Get what?", "8w1y", True)

        # Put #
        elif input.lower().split()[0] in ["put", "pu", "p"]:

            # Put All Item In Container #
            if len(input.split()) > 4 and input.lower().split()[1] == "all" and "in" in input.lower().split() and input.lower().split()[2] != "in" and input.lower().split()[-1] != "in":
                inIndex = input.lower().split().index("in")
                targetItemKey = ' '.join(input.lower().split()[2:inIndex])
                targetContainerKey = ' '.join(input.lower().split()[inIndex + 1::])
                self.player.putCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, targetContainerKey, "All")

            # Put All In Container #
            elif len(input.split()) > 3 and input.lower().split()[1] == "all" and input.lower().split()[2] == "in":
                targetContainerKey = ' '.join(input.lower().split()[3::])
                self.player.putCheck(self.console, self.galaxyList, self.player, currentRoom, "All", targetContainerKey, "All")

            # Put '#' Item In Container #
            elif len(input.split()) > 4 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0 and "in" in input.lower().split() and input.lower().split()[2] != "in" and input.lower().split()[-1] != "in":
                inIndex = input.lower().split().index("in")
                targetItemKey = ' '.join(input.lower().split()[2:inIndex])
                targetContainerKey = ' '.join(input.lower().split()[inIndex + 1::])
                self.player.putCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, targetContainerKey, int(input.split()[1]))

            # Put Item In Container #
            elif len(input.split()) > 3 and "in" in input.lower().split() and input.lower().split()[1] != "in" and input.lower().split()[-1] != "in":
                inIndex = input.lower().split().index("in")
                targetItemKey = ' '.join(input.lower().split()[1:inIndex])
                targetContainerKey = ' '.join(input.lower().split()[inIndex + 1::])
                self.player.putCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, targetContainerKey, 1)

            else:
                self.console.write("Put what in what?", "16w1y", True)

        # Loot #
        elif input.lower().split()[0] in ["loot"]:

            # Loot Item From All #
            if len(input.split()) > 3 and input.lower().split()[-2] == "from" and input.lower().split()[-1] == "all":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[1:fromIndex])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, "All", "All")

            # Loot Item From Container #
            elif len(input.split()) > 3 and "from" in input.lower().split() and input.lower().split()[1] != "from" and input.lower().split()[-1] != "from":
                fromIndex = input.lower().split().index("from")
                targetItemKey = ' '.join(input.lower().split()[1:fromIndex])
                targetContainerKey = ' '.join(input.lower().split()[fromIndex + 1::])
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, targetContainerKey, "All")

            # Loot All #
            elif len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, "All", "All", "All")

            # Loot Container #
            elif len(input.split()) > 1:
                self.player.getCheck(self.console, self.galaxyList, self.player, currentRoom, "All", ' '.join(input.lower().split()[1::]), "All")

            else:
                self.console.write("Loot what?", "9w1y", True)

        # Drop #
        elif input.lower().split()[0] in ["drop", "dro", "dr"]:

            # Drop All #
            if len(input.split()) == 2 and input.split()[1].lower() == "all":
                self.player.dropCheck(self.console, self.galaxyList, self.player, currentRoom, "All", "All")

            # Drop All Pocket #
            elif len(input.split()) == 3 and input.lower().split()[1] == "all" and input.lower().split()[2] in self.player.getPocketList(True):
                pocketKey = ' '.join(input.lower().split()[2::])
                self.player.dropCheck(self.console, self.galaxyList, self.player, currentRoom, "All", "All", pocketKey)

            # Drop All Item #
            elif len(input.split()) > 2 and input.split()[1].lower() == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.dropCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, "All")

            # Drop '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.dropCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, int(input.split()[1]))

            # Drop Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.dropCheck(self.console, self.galaxyList, self.player, currentRoom, targetItemKey, 1)

            else:
                self.console.write("Drop what?", "9w1y", True)
        
        # Empty #

            # Empty Container/Drink #

        # Wear #
        elif input.lower().split()[0] in ["wear", "wea"]:

            # Wear All #
            if len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.wearCheck(self.console, self.galaxyList, self.player, "All", "All")

            # Wear All Item #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.wearCheck(self.console, self.galaxyList, self.player, targetItemKey, "All")

            # Wear Item 'GearSlot' #
            elif len(input.split()) > 2 and ((stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0) or input.lower().split()[-1] in ["left", "lef", "le", "l", "right", "righ", "rig", "ri", "r"]):
                targetItemKey = ' '.join(input.lower().split()[1:-1])
                self.player.wearCheck(self.console, self.galaxyList, self.player, targetItemKey, 1, input.lower().split()[-1])

            # Wear '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.wearCheck(self.console, self.galaxyList, self.player, targetItemKey, int(input.split()[1]))

            # Wear Item #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.wearCheck(self.console, self.galaxyList, self.player, targetItemKey, 1)

            else:
                self.console.write("Wear what?", "9w1y", True)
        
        # Wield #
        elif input.lower().split()[0] in ["wield", "wiel", "wie" "wi", "hold", "hol", "ho"]:

            # Wield All #
            if len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.wieldCheck(self.console, self.galaxyList, self.player, "All", None, 2)

            # Wield Item 'Slot' #
            elif len(input.split()) > 2 and ((stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0) or input.lower().split()[-1] in ["left", "lef", "le", "l", "right", "righ", "rig", "ri", "r"]):
                self.player.wieldCheck(self.console, self.galaxyList, self.player, ' '.join(input.lower().split()[1:-1]), input.lower().split()[-1], 1)

            # Wield All Item #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                self.player.wieldCheck(self.console, self.galaxyList, self.player, ' '.join(input.lower().split()[2::]), None, 2)

            # Wield '#' Item #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                self.player.wieldCheck(self.console, self.galaxyList, self.player, ' '.join(input.lower().split()[2::]), None, int(input.split()[1]))

            # Wield Item #
            elif len(input.split()) > 1:
                self.player.wieldCheck(self.console, self.galaxyList, self.player, ' '.join(input.lower().split()[1::]), None, 1)

            else:
                self.console.write("Wield what?", "10w1y", True)

        # Remove #
        elif input.lower().split()[0] in ["remove", "remov", "remo", "rem"]:

            # Remove All #
            if len(input.split()) == 2 and input.lower().split()[1] == "all":
                self.player.removeCheck(self.console, self.galaxyList, self.player, "All", "All")

            # Remove All Gear/Weapon #
            elif len(input.split()) > 2 and input.lower().split()[1] == "all":
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.removeCheck(self.console, self.galaxyList, self.player, targetItemKey, "All")

            # Remove Gear/Weapon 'GearSlot' #
            elif len(input.split()) > 2 and (stringIsNumber(input.split()[-1]) and int(input.split()[-1]) > 0) or input.lower().split()[-1] in ["left", "right"]:
                if stringIsNumber(input.split()[-1]):
                    targetGearSlotIndex = int(input.split()[-1]) - 1
                else:
                    targetGearSlotIndex = input.lower().split()[-1]
                targetItemKey = ' '.join(input.lower().split()[1:-1])
                self.player.removeCheck(self.console, self.galaxyList, self.player, targetItemKey, 1, targetGearSlotIndex)

            # Remove '#' Gear/Weapon #
            elif len(input.split()) > 2 and stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0:
                targetItemKey = ' '.join(input.lower().split()[2::])
                self.player.removeCheck(self.console, self.galaxyList, self.player, targetItemKey, int(input.split()[1]))

            # Remove Gear/Weapon #
            elif len(input.split()) > 1:
                targetItemKey = ' '.join(input.lower().split()[1::])
                self.player.removeCheck(self.console, self.galaxyList, self.player, targetItemKey, 1)

            else:
                self.console.write("Remove what?", "11w1y", True)

        ## Combat Commands ##
        # Attack #
        elif input.lower().split()[0] in ["attack", "attac", "atta", "att", "at", "a"]:
            
            # Attack Mob #
            if len(input.split()) > 1:
                mobKey = ' '.join(input.lower().split()[1::])
                self.player.attackCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, mobKey)

            # Attack #
            else:
                self.player.attackCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, None)

        # Combat Skill #
        elif combatSkill != None:
            parsedCombatInput = parsedCombatInput.split()
            
            # Skill '#' Mob Direction '#' #
            if len(parsedCombatInput) > 3 and stringIsNumber(parsedCombatInput[0]) and int(parsedCombatInput[0]) > 0 and parsedCombatInput[-2] in directionStringList and stringIsNumber(parsedCombatInput[-1]) and int(parsedCombatInput[-1]) > 0:
                mobCount = int(parsedCombatInput[0])
                mobKey = ' '.join(parsedCombatInput[1:-2])
                directionKey = parsedCombatInput[-2]
                directionCount = int(parsedCombatInput[-1])
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill All/Group Mob Direction '#' #
            elif len(parsedCombatInput) > 3 and parsedCombatInput[0] in ["all", "group"] and parsedCombatInput[-2] in directionStringList and stringIsNumber(parsedCombatInput[-1]) and int(parsedCombatInput[-1]) > 0:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = ' '.join(parsedCombatInput[1:-2])
                directionKey = parsedCombatInput[-2]
                directionCount = int(parsedCombatInput[-1])
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill All/Group Direction '#' #
            elif len(parsedCombatInput) == 3 and parsedCombatInput[0] in ["all", "group"] and parsedCombatInput[1] in directionStringList and stringIsNumber(parsedCombatInput[2]) and int(parsedCombatInput[2]) > 0:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = "All"
                directionKey = parsedCombatInput[-2]
                directionCount = int(parsedCombatInput[-1])
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill Mob Direction '#' #
            elif len(parsedCombatInput) > 2 and parsedCombatInput[-2] in directionStringList and stringIsNumber(parsedCombatInput[-1]) and int(parsedCombatInput[-1]) > 0:
                mobCount = 1
                mobKey = ' '.join(parsedCombatInput[0:-2])
                directionKey = parsedCombatInput[-2]
                directionCount = int(parsedCombatInput[-1])
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill '#' Mob Direction #
            elif len(parsedCombatInput) > 2 and stringIsNumber(parsedCombatInput[0]) and int(parsedCombatInput[0]) > 0 and parsedCombatInput[-1] in directionStringList:
                mobCount = int(parsedCombatInput[0])
                mobKey = ' '.join(parsedCombatInput[1:-1])
                directionKey = parsedCombatInput[-1]
                directionCount = 1
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill All/Group Mob Direction #
            elif len(parsedCombatInput) > 2 and parsedCombatInput[0] in ["all", "group"] and parsedCombatInput[-1] in directionStringList:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = ' '.join(parsedCombatInput[1:-1])
                directionKey = parsedCombatInput[-1]
                directionCount = 1
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill All/Group Direction #
            elif len(parsedCombatInput) == 2 and parsedCombatInput[0] in ["all", "group"] and parsedCombatInput[1] in directionStringList:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = "All"
                directionKey = parsedCombatInput[-1]
                directionCount = 1
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill Mob Direction #
            elif len(parsedCombatInput) > 1 and parsedCombatInput[-1] in directionStringList:
                mobCount = 1
                mobKey = ' '.join(parsedCombatInput[0:-1])
                directionKey = parsedCombatInput[-1]
                directionCount = 1
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill Direction '#' #
            elif len(parsedCombatInput) == 2 and parsedCombatInput[0] in directionStringList and stringIsNumber(parsedCombatInput[1]) and int(parsedCombatInput[1]) > 0:
                mobCount = "All"
                mobKey = "All"
                directionKey = parsedCombatInput[0]
                directionCount = int(parsedCombatInput[1])
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill '#' Mob #
            elif len(parsedCombatInput) > 1 and stringIsNumber(parsedCombatInput[0]) and int(parsedCombatInput[0]) > 0:
                mobCount = int(parsedCombatInput[0])
                mobKey = ' '.join(parsedCombatInput[1::])
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, None, None)

            # Skill All/Group Mob #
            elif len(parsedCombatInput) > 1 and parsedCombatInput[0] in ["all", "group"]:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = ' '.join(parsedCombatInput[1::])
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, None, None)
            
            # Skill All/Group #
            elif len(parsedCombatInput) == 1 and parsedCombatInput[0] in ["all", "group"]:
                if parsedCombatInput[0] == "all" : mobCount = "All"
                else : mobCount = "Group"
                mobKey = "All"
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, None, None)

            # Skill Direction #
            elif len(parsedCombatInput) == 1 and parsedCombatInput[0] in directionStringList:
                mobCount = "All"
                mobKey = "All"
                directionKey = parsedCombatInput[0]
                directionCount = 1
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount)

            # Skill Mob/Self #
            elif len(parsedCombatInput) > 0:
                mobCount = 1
                mobKey = ' '.join(parsedCombatInput)
                if mobKey == "self" : mobKey = "Self"
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, mobCount, mobKey, None, None)

            # Skill #
            elif parsedCombatInput == []:
                self.player.combatSkillCheck(self.config, self.console, self.galaxyList, self.player, currentRoom, combatSkill, None, None, None, None)
            
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
            elif len(input.split()) == 2 and (input.lower().split()[1] in ["left", "lef", "le", "l", "right", "righ", "rig", "ri", "r"] or (stringIsNumber(input.split()[1]) and int(input.split()[1]) > 0)):
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

        # Recruit/Tame/Group [Needs Testing] #
        elif input.lower().split()[0] in ["tame", "tam", "recruit", "recrui", "recru", "recr", "rec", "group", "grou", "gro", "gr"]:

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

            # Recruit List #
            elif len(input.split()) == 2 and input.lower().split()[1] == "list":
                self.player.displayGroup(self.console, self.galaxyList)

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
        elif len(input.split()) == 1 and input.lower() in ["stop", "sto", "st"]:
            self.player.stopCheck(self.console, self.galaxyList, self.player)

        ## Status Commands ##
        # Inventory #
        elif input.lower().split()[0] in ["inventory", "inventor", "invento", "invent", "inven", "inve", "inv", "in", "i"]:
            targetPocketKey = None
            if len(input.split()) > 1:
                targetPocketKey = ' '.join(input.lower().split()[1::])
            self.player.displayInventory(self.console, self.galaxyList, self.player, currentRoom, targetPocketKey)
        
        # Gear #
        elif len(input.split()) == 1 and input.lower() in ["gear", "gea"]:
            self.player.displayGear(self.console, self.galaxyList, self.player, currentRoom)

        # Skills #
        elif input.lower().split()[0] in ["skills", "skill", "skil", "ski", "sk"]:
            if len(input.split()) > 1:
                skillGroupKey = ' '.join(input.lower().split()[1::])
                self.player.displaySkills(self.console, skillGroupKey)

            else:
                self.player.displaySkills(self.console, None)

        # Character/Status #
        elif len(input.split()) == 1 and input.lower() in ["status", "statu", "stat", "sta", "st"]:
            self.player.displayStatus(self.console, self.config)

        # Time #
        elif len(input.split()) == 1 and input.lower() in ["time", "tim", "ti"]:
            self.player.displayTime(self.console, self.galaxyList)

        # Weather #

        # Astro(?) #

        ## Other Commands ##
        # Search #
        elif input.lower().split()[0] in ["search", "searc", "sear", "sea", "se"]:
            if len(input.split()) > 1:
                searchKey = ' '.join(input.lower().split()[1::])
                self.player.searchCheck(self.console, self.galaxyList, self.player, currentRoom, searchKey)
            
            else:
                self.console.write("What should you search?", "22w1y", True)

        # Push/Press #
        elif input.lower().split()[0] in ["push", "pus", "pu", "press", "pres", "pre", "pr"]:
            if len(input.split()) > 1:
                pushKey = ' '.join(input.lower().split()[1::])
                self.player.pushCheck(self.console, self.galaxyList, self.player, currentRoom, pushKey)

            else:
                self.console.write("Push what?", "9w1y", True)

        # Say #
        elif input.lower().split()[0] in ["say", "sa"]:
            if len(input.split()) > 1:
                sayKey = ' '.join(input.lower().split()[1::])
                sayText = {"String":sayKey, "Code":str(len(sayKey)) + "w"}
                self.player.sayCheck(self.console, self.galaxyList, self.player, currentRoom, sayText)

            else:
                self.console.write("Say what?", "8w1y", True)

        # Eat/Drink #
        elif input.lower().split()[0] in ["eat", "drink", "drin", "dri"]:
            if len(input.split()) > 1:
                consumeKey = ' '.join(input.lower().split()[1::])
                self.player.consumeCheck(self.console, self.galaxyList, self.player, currentRoom, consumeKey)

            else:
                if input.lower()[0] == "e" : actionString = "Eat"
                else : actionString = "Drink"
                self.console.write(actionString + " what?", str(len(actionString)) + "w5w1y", True)

        # Fill #

        # List #

        # Buy(?) #

        # Sell(?) #

        ## Spaceship Commands ##
        # Board #
        elif input.lower().split()[0] in ["board", "boar", "boa", "bo"]:
            if len(input.split()) > 1:
                self.player.boardCheck(self.console, self.map, self.galaxyList, self.player, currentRoom, ' '.join(input.lower().split()[1::]))
            
            else:
                self.console.write("Board what?", "10w1y", True)

        # Launch #
        elif len(input.split()) == 1 and input.lower() in ["launch", "launc", "laun", "lau"]:
            self.player.launchCheck(self.console, self.galaxyList, self.player, currentRoom)

        # Radar #
        elif len(input.split()) == 1 and input.lower() in ["radar", "rada", "rad"]:
            self.player.radarCheck(self.console, self.galaxyList, self.player, currentRoom)

        # Course #
        elif input.lower().split()[0] in ["course", "cours", "cour", "cou"]:
            
            # Course X Y #
            if len(input.split()) == 3 and stringIsNumber(input.split()[1]) and stringIsNumber(input.split()[2]):
                targetX = int(input.split()[1])
                targetY = int(input.split()[2])
                self.player.courseCheck(self.console, self.galaxyList, self.player, currentRoom, [targetX, targetY])
            
            # Course Target #
            else:
                courseKey = None
                if len(input.split()) > 1:
                    courseKey = ' '.join(input.lower().split()[1::])
                self.player.courseCheck(self.console, self.galaxyList, self.player, currentRoom, courseKey)
            
        # Throttle/Speed #
        elif input.lower().split()[0] in ["throttle", "throttl", "thrott", "throt", "speed", "spee", "spe"]:
            throttleKey = None
            if len(input.split()) > 1:
                throttleKey = ' '.join(input.lower().split()[1::])
            self.player.throttleCheck(self.console, self.galaxyList, self.player, currentRoom, throttleKey)

        # Scan #
        elif len(input.split()) == 1 and input.lower().split()[0] in ["scan", "sca"]:
            self.player.scanCheck(self.console, self.galaxyList, self.player, currentRoom)

        # Land #
        elif input.lower().split()[0] in ["land", "lan"]:
            landKey = None
            if len(input.split()) > 1:
                landKey = ' '.join(input.lower().split()[1::])
            self.player.landCheck(self.console, self.galaxyList, self.player, currentRoom, landKey)

        # Calculate #

        # System #

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

        ## Config/Setting Commands ##
        # Auto Loot #
        elif input.lower().split()[0] == "autoloot" or (len(input.split()) == 2 and input.lower().split()[0] == "auto" and input.lower().split()[1] == "loot"):
            self.config.autoLoot = not self.config.autoLoot
            self.console.write("Setting changed.", "15w1y", True)

        # Auto Reload #
        elif input.lower().split()[0] == "autoreload" or (len(input.split()) == 2 and input.lower().split()[0] == "auto" and input.lower().split()[1] == "reload"):
            self.config.autoReload = not self.config.autoReload
            self.console.write("Setting changed.", "15w1y", True)

        # Auto Combat #
        elif input.lower().split()[0] == "autocombat" or (len(input.split()) == 2 and input.lower().split()[0] == "auto" and input.lower().split()[1] == "combat"):
            self.config.autoCombat = not self.config.autoCombat
            self.console.write("Setting changed.", "15w1y", True)

        # Team Damage #
        elif input.lower().split()[0] == "teamdamage" or (len(input.split()) == 2 and input.lower().split()[0] == "team" and input.lower().split()[1] == "damage"):
            self.config.teamDamage = not self.config.teamDamage
            self.console.write("Setting changed.", "15w1y", True)

        # Heal Enemies #
        elif input.lower().split()[0] == "healenemies" or (len(input.split()) == 2 and input.lower().split()[0] == "heal" and input.lower().split()[1] == "enemies"):
            self.config.healEnemies = not self.config.healEnemies
            self.console.write("Setting changed.", "15w1y", True)

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
                self.console.write("Manifest what?", "13w1y", True)

        ## Emotes ##
        elif input.lower().split()[0] in self.player.emoteList:
            self.player.emote(self.console, input.lower())

        else:
            self.console.write("Huh?", "3w1y", True)
