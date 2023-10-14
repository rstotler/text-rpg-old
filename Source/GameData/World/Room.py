import copy
from GameData.Item.Item import Item
from Components.Utility import getCountString
from Components.Utility import createUnderlineString
from Components.Utility import createDefaultString

class Room:

    def __init__(self, galaxy, system, planet, area, room, name):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.area = area
        self.room = room
        self.spaceshipObject = None
        self.flags = {}

        self.mapCoordinates = [None, None]

        self.name = createDefaultString(name)
        self.description = []
        self.searchList = []

        self.exit = {"North": None, "East": None, "South": None, "West": None, "Up":None, "Down":None}
        self.door = {"North": None, "East": None, "South": None, "West": None, "Up":None, "Down":None}

        self.mobList = []
        self.itemList = []
        self.spaceshipList = []

        self.inside = False

    def display(self, console, galaxyList, player):
        roomIsLit = self.isLit(galaxyList, player, player)

        # Name #
        nameString = self.name["String"]
        nameCode = str(len(nameString)) + "w"
        if "Code" in self.name:
            nameCode = self.name["Code"]
        if roomIsLit == False:
            nameString = "Darkness"
            nameCode = "1ddda1dda1da1da1da1a1da1dda"
        if self.inside == True:
            nameString = "(Inside) " + nameString
            nameCode = "1r6w2r" + nameCode
        console.write(nameString, nameCode, True)

        # Underline #
        underline = createUnderlineString(nameString)
        console.write(underline["String"], underline["Code"])

        # Description #
        if roomIsLit == False:
            console.write("It's too dark to see..", "2w1y17w2y")
        else:
            for line in self.description:
                console.write(line["String"], line["Code"])

        # Exits #
        otherRoomSpaceshipNum = None
        for exitDir in ["North", "East", "South", "West", "Up", "Down"]:
            if not (exitDir in ["Up", "Down"] and self.exit[exitDir] == None):
                spaceString = ""
                if exitDir in ["East", "West", "Down"] : spaceString = " "
                elif exitDir == "Up" : spaceString = "   "
                if self.exit[exitDir] != None and not (self.door[exitDir] != None and self.door[exitDir]["Type"] == "Hidden" and self.door[exitDir]["Status"] in ["Locked", "Closed"]):
                    exitRoom = None
                    if len(self.exit[exitDir]) == 5:
                        exitRoom = Room.exists(galaxyList, None, self.exit[exitDir][0], self.exit[exitDir][1], self.exit[exitDir][2], self.exit[exitDir][3], self.exit[exitDir][4])
                    elif len(self.exit[exitDir]) == 3 and self.spaceshipObject != None:
                        exitRoom = self.spaceshipObject.getRoom(self.exit[exitDir][1], self.exit[exitDir][2])
                    elif self.exit[exitDir] == "Spaceship Exit" and self.spaceshipObject.landedLocation != None:
                        exitRoom = Room.exists(galaxyList, None, self.spaceshipObject.galaxy, self.spaceshipObject.system, self.spaceshipObject.planet, self.spaceshipObject.landedLocation[0], self.spaceshipObject.landedLocation[1])
                    if exitRoom == None:
                        exitRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                    
                    if self.door[exitDir] != None and self.door[exitDir]["Status"] in ["Closed", "Locked"]:
                        exitRoomString = "( " + spaceString + exitDir + " ) - [Closed]"
                        exitRoomCode = "2r1w4ddw2r3y1r6w1r"
                    elif roomIsLit == False and exitRoom.isLit(galaxyList, player, player) == False:
                        exitRoomString = "( " + spaceString + exitDir + " ) - ( Black )"
                        exitRoomCode = "2r1w4ddw2r3y2r1dw1a2da1dda2r"
                    else:
                        exitRoomString = "( " + spaceString + exitDir + " ) - " + exitRoom.name["String"]
                    
                    if roomIsLit == False and exitRoom.isLit(galaxyList, player, player) == False:
                        exitRoomNameCode = "2r1dw1a2da1dda2r"
                    else:
                        exitRoomNameCode = str(len(exitRoomString)) + "w"
                        if "Code" in exitRoom.name:
                            exitRoomNameCode = exitRoom.name["Code"]
                    
                    if self.door[exitDir] == None or self.door[exitDir]["Status"] == "Open":
                        if exitDir in ["East", "West", "Down"]:
                            exitRoomCode = "3r1w" + str(len(exitDir) - 1) + "ddw2r3y" + exitRoomNameCode
                        elif exitDir == "Up":
                            exitRoomCode = "5r1w" + str(len(exitDir) - 1) + "ddw2r3y" + exitRoomNameCode
                        else:
                            exitRoomCode = "2r1w" + str(len(exitDir) - 1) + "ddw2r3y" + exitRoomNameCode
                    console.write(exitRoomString, exitRoomCode)
                else:
                    if exitDir in ["East", "West", "Down"]:
                        exitRoomCode = "3r1w" + str(len(exitDir) - 1) + "ddw2r3y2r1w6ddw2r"
                    elif exitDir == "Up":
                        exitRoomCode = "5r1w" + str(len(exitDir) - 1) + "ddw2r3y2r1w6ddw2r"
                    else:
                        exitRoomCode = "2r1w" + str(len(exitDir) - 1) + "ddw2r3y2r1w6ddw2r"
                    
                    if roomIsLit == False:
                        exitRoomCode = exitRoomCode[0:-8] + "1dw1a2da1dda2r"
                        console.write("( " + spaceString + exitDir + " ) - ( Black )", exitRoomCode)
                    else:
                        console.write("( " + spaceString + exitDir + " ) - ( Nothing )", exitRoomCode)

        # Spaceships #
        if len(self.spaceshipList) > 0:
            if roomIsLit == False:
                displayString = "A spaceship is sitting on the launch pad."
                displayCode = "40w1y"
                countString, countCode = getCountString(len(self.spaceshipList))
                console.write(displayString + countString, displayCode + countCode)
            else:
                for spaceship in self.spaceshipList:
                    displayString = "A " + spaceship.name["String"] + " is sitting on the launch pad."
                    displayCode = "2w" + spaceship.name["Code"] + "29w1y"
                    console.write(displayString, displayCode)
            
        # Mobs #
        if True:
            mobDisplayList = []
            totalMobCount = 0
            for mob in self.mobList:
                targetMobData = None
                for data in mobDisplayList:
                    groupCheck = mob in player.recruitList
                    targetCheck = False
                    if groupCheck == False:
                        targetCheck = mob in player.targetList
                    combatCheck = mob in player.combatList
                    if mob.num == data["Num"] and data["Target Check"] == targetCheck and data["Group Check"] == groupCheck and combatCheck == data["Combat Check"]:
                        targetMobData = data
                        break
                if targetMobData == None:
                    groupCheck = mob in player.recruitList
                    targetCheck = False
                    if groupCheck == False:
                        targetCheck = mob in player.targetList
                    combatCheck = mob in player.combatList
                    mobDisplayList.append({"Num":mob.num, "Count":1, "Target Check":targetCheck, "Group Check":groupCheck, "Mob Data":mob, "Combat Check":combatCheck})
                else:
                    targetMobData["Count"] += 1
                totalMobCount += 1

            if roomIsLit == False and totalMobCount > 0:
                countString, countCode = getCountString(totalMobCount)
                console.write("There is someone here." + countString, "21w1y" + countCode)

            else:
                for mobData in mobDisplayList:
                    targetString = ""
                    targetCode = ""
                    if "Group Check" in mobData and mobData["Group Check"] == True:
                        targetString = "[+]"
                        targetCode = "3g"
                    elif "Target Check" in mobData and mobData["Target Check"] == True:
                        targetString = "[+]"
                        targetCode = "3m"
                    countString, countCode = getCountString(mobData["Count"])
                    if "Combat Check" in mobData and mobData["Combat Check"] == True:
                        mobDisplayString = targetString + mobData["Mob Data"].prefix + " " + mobData["Mob Data"].name["String"] + " is here, fighting you!" + countString
                        mobDisplayCode = targetCode + str(len(mobData["Mob Data"].prefix)) + "w1w" + mobData["Mob Data"].name["Code"] + "8w1y13w1y" + countCode
                    else:
                        mobDisplayString = targetString + mobData["Mob Data"].prefix + " " + mobData["Mob Data"].name["String"] + " " + mobData["Mob Data"].roomDescription["String"] + countString
                        mobDisplayCode = targetCode + str(len(mobData["Mob Data"].prefix)) + "w1w" + mobData["Mob Data"].name["Code"] + "1w" + mobData["Mob Data"].roomDescription["Code"] + countCode
                    console.write(mobDisplayString, mobDisplayCode)

        # Items #
        if True:
            displayList = []
            totalItemCount = 0
            for item in self.itemList:
                displayData = None
                for data in displayList:
                    if data["Num"] == item.num:
                        if item.num != Item.getSpecialItemNum("Corpse") or item.name["String"] == data["ItemData"].name["String"]:
                            displayData = data
                            break
                if displayData == None:
                    itemCount = 1
                    if item.quantity != None:
                        itemCount = item.quantity
                    displayList.append({"Num":item.num, "Count":itemCount, "ItemData":item})
                    totalItemCount += itemCount
                else:
                    displayData["Count"] += 1
                    totalItemCount += 1

            if roomIsLit == False and totalItemCount > 0:
                countString, countCode = getCountString(totalItemCount)
                console.write("There is something on the ground." + countString, "32w1y" + countCode)

            else:
                for itemData in displayList:
                    item = itemData["ItemData"]
                    modString = ""
                    modCode = ""
                    if "Glowing" in item.flags and item.flags["Glowing"] == True:
                        modString = " (Glowing)"
                        modCode = "2y1w1dw1ddw1w2dw1ddw1y"

                    countString, countCode = getCountString(itemData["Count"])
                    itemDisplayString = item.prefix + " " + item.name["String"] + " " + item.roomDescription["String"] + modString + countString
                    itemDisplayCode = str(len(item.prefix)) + "w1w" + item.name["Code"] + "1w" + item.roomDescription["Code"] + modCode + countCode
                    console.write(itemDisplayString, itemDisplayCode)

    def installDoor(self, galaxyList, targetDir, doorType, password, status="Closed", oneWay=False):
        self.door[targetDir] = {"Type": doorType, "Status": status}
        if password != None:
            self.door[targetDir]["Password"] = password

        if oneWay == False and self.exit[targetDir] != None:
            otherRoom = None
            if len(self.exit[targetDir]) == 3 and self.spaceshipObject != None:
                otherRoom = self.spaceshipObject.areaList[self.exit[targetDir][1]].roomList[self.exit[targetDir][2]]
            elif len(self.exit[targetDir]) == 5:
                otherRoom = Room.exists(galaxyList, None, self.exit[targetDir][0], self.exit[targetDir][1], self.exit[targetDir][2], self.exit[targetDir][3], self.exit[targetDir][4])
            if otherRoom != None:
                otherRoomExitDir = None
                for exitDir in otherRoom.exit:
                    exitData = otherRoom.exit[exitDir]
                    if exitData != None and self.sameRoomCheck(exitData) == True:
                        otherRoomExitDir = exitDir
                        break

                if otherRoomExitDir != None:
                    otherRoom.door[otherRoomExitDir] = {"Type": doorType, "Status": status}
                    if password != None:
                        otherRoom.door[otherRoomExitDir]["Password"] = password

    def openCloseDoor(self, galaxyList, targetAction, targetDir):
        if self.door[targetDir] != None:
            if targetAction == "Close":
                targetAction = "Closed"

            self.door[targetDir]["Status"] = targetAction

            if self.exit[targetDir] != None:
                otherRoom = None
                if len(self.exit[targetDir]) == 3 and self.spaceshipObject != None:
                    otherRoom = self.spaceshipObject.areaList[self.exit[targetDir][1]].roomList[self.exit[targetDir][2]]
                elif len(self.exit[targetDir]) == 5:
                    otherRoom = Room.exists(galaxyList, None, self.exit[targetDir][0], self.exit[targetDir][1], self.exit[targetDir][2], self.exit[targetDir][3], self.exit[targetDir][4])
                if otherRoom != None:
                    otherRoomExitDir = None
                    for exitDir in otherRoom.exit:
                        exitData = otherRoom.exit[exitDir]
                        if exitData != None and self.sameRoomCheck(exitData) == True:
                            otherRoomExitDir = exitDir
                            break
                    
                    if otherRoomExitDir != None and otherRoom.door[otherRoomExitDir] != None:
                        otherRoom.door[otherRoomExitDir]["Status"] = targetAction

    def lockUnlockDoor(self, galaxyList, targetAction, targetDir):
        if self.door[targetDir] != None:
            if targetAction == "Lock":
                targetAction = "Locked"
            elif targetAction == "Unlock":
                targetAction = "Closed"

            if not (targetAction == "Locked" and "Password" not in self.door[targetDir]):
                self.door[targetDir]["Status"] = targetAction

                if self.exit[targetDir] != None:
                    otherRoom = None
                    if len(self.exit[targetDir]) == 3 and self.spaceshipObject != None:
                        otherRoom = self.spaceshipObject.areaList[self.exit[targetDir][1]].roomList[self.exit[targetDir][2]]
                    elif len(self.exit[targetDir]) == 5:
                        otherRoom = Room.exists(galaxyList, None, self.exit[targetDir][0], self.exit[targetDir][1], self.exit[targetDir][2], self.exit[targetDir][3], self.exit[targetDir][4])
                    if otherRoom != None:
                        otherRoomExitDir = None
                        for exitDir in otherRoom.exit:
                            exitData = otherRoom.exit[exitDir]
                            if exitData != None and self.sameRoomCheck(exitData) == True:
                                otherRoomExitDir = exitDir
                                break

                        if otherRoomExitDir != None and otherRoom.door[otherRoomExitDir] != None:
                            otherRoom.door[otherRoomExitDir]["Status"] = targetAction

    def sameRoomCheck(self, target):
        if isinstance(target, list):
            if len(target) == 3 and self.spaceshipObject != None:
                if target[0] == self.spaceshipObject.num and target[1] == self.area and target[2] == self.room:
                    return True
            elif len(target) == 5:
                if target[0] == self.galaxy and target[1] == self.system and target[2] == self.planet and target[3] == self.area and target[4] == self.room:
                    return True

        elif hasattr(target, "currentHealth"):
            if target.spaceship == None and self.spaceshipObject == None:
                if target.galaxy == self.galaxy and target.system == self.system and target.planet == self.planet and target.area == self.area and target.room == self.room:
                    return True
            elif target.spaceship != None and self.spaceshipObject != None:
                if target.spaceship == self.spaceshipObject.num and target.area == self.area and target.room == self.room:
                    return True

        else:
            if target.galaxy == self.galaxy and target.system == self.system and target.planet == self.planet and target.area == self.area and target.room == self.room and target.spaceshipObject == self.spaceshipObject:
                return True

        return False
    
    def isLit(self, galaxyList, player, targetPlayer):
        targetPlanet = None
        if self.galaxy != None and self.system != None and self.planet != None:
            if self.galaxy <= len(galaxyList) - 1 and self.system <= len(galaxyList[self.galaxy].systemList) -1 and self.planet <= len(galaxyList[self.galaxy].systemList[self.system].planetList) - 1:
                targetPlanet = galaxyList[self.galaxy].systemList[self.system].planetList[self.planet]
        if targetPlanet != None and self.inside == False:
            if targetPlanet.dayCheck():
                return True

        for item in self.itemList:
            if "Glowing" in item.flags and item.flags["Glowing"] == True:
                return True

        targetPlayerList = self.mobList
        if targetPlayer.num == None or self.sameRoomCheck(player):
            targetPlayerList = [player] + self.mobList
        for target in targetPlayerList:
            if self.sameRoomCheck(target):
                for gearSlot in target.gearDict:
                    if isinstance(target.gearDict[gearSlot], list):
                        for gearSubSlot in target.gearDict[gearSlot]:
                            if gearSubSlot != None:
                                if "Glowing" in gearSubSlot.flags and gearSubSlot.flags["Glowing"] == True:
                                    return True
                    else:
                        if target.gearDict[gearSlot] != None:
                            item = target.gearDict[gearSlot]
                            if "Glowing" in item.flags and item.flags["Glowing"] == True:
                                return True
                    
        return False

    def getTargetObject(self, targetObjectKey, includeList=["Mobs", "Items", "Spaceships"]):
        objectCheckList = []
        if "Mob" in includeList or "Mobs" in includeList:
            objectCheckList.append(self.mobList)
        if "Item" in includeList or "Items" in includeList:
            objectCheckList.append(self.itemList)
        if "Spaceship" in includeList or "Spaceships" in includeList:
            objectCheckList.append(self.spaceshipList)

        for objectList in objectCheckList:
            for tempObject in objectList:
                if (isinstance(targetObjectKey, str) and targetObjectKey in tempObject.keyList) or \
                (isinstance(targetObjectKey, int) and targetObjectKey == tempObject.num):
                    return tempObject

        if "Button" in includeList or "Buttons" in includeList:
            for item in self.itemList:
                if item.buttonList != None:
                    for button in item.buttonList:
                        if targetObjectKey in button.keyList:
                            return button

        if "Hidden Object" in includeList or "Hidden Objects" in includeList:
            for exitDir in self.door:
                if self.door[exitDir] != None and self.door[exitDir]["Type"] == "Hidden":
                    return self.door[exitDir]

        return None
        
    @staticmethod
    def exists(galaxyList, targetSpaceship, targetGalaxy, targetSystem, targetPlanet, targetArea, targetRoom):
        if targetSpaceship == None:
            if targetGalaxy <= len(galaxyList) - 1 and \
            targetSystem <= len(galaxyList[targetGalaxy].systemList) - 1 and \
            targetPlanet <= len(galaxyList[targetGalaxy].systemList[targetSystem].planetList) - 1 and \
            targetArea <= len(galaxyList[targetGalaxy].systemList[targetSystem].planetList[targetPlanet].areaList) - 1 and \
            targetRoom <= len(galaxyList[targetGalaxy].systemList[targetSystem].planetList[targetPlanet].areaList[targetArea].roomList) -1:
                return galaxyList[targetGalaxy].systemList[targetSystem].planetList[targetPlanet].areaList[targetArea].roomList[targetRoom]
        else:
            targetSpaceshipObject = galaxyList[targetGalaxy].systemList[targetSystem].getSpaceship(targetSpaceship)
            if targetSpaceshipObject != None and \
            targetArea <= len(targetSpaceshipObject.areaList) and \
            targetRoom <= len(targetSpaceshipObject.areaList[targetArea].roomList):
                return targetSpaceshipObject.areaList[targetArea].roomList[targetRoom]
            
        return None

    @staticmethod
    def getTargetRoomFromStartRoom(galaxyList, currentArea, currentRoom, targetDir, targetRoomDistance, ignoreDoors=False):
        messageType = None
        for rNum in range(targetRoomDistance):
            if currentRoom.exit[targetDir] == None:
                if messageType == None:
                    messageType = "No Exit"
                break
            else:
                targetExit = currentRoom.exit[targetDir]
                if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Status"] in ["Closed", "Locked"]:
                    messageType = "Door Is Closed"
                    if ignoreDoors == False:
                        break
                elif targetExit == "Spaceship Exit" and currentRoom.spaceshipObject.landedLocation == None:
                    messageType = "Door Is Closed"
                    if ignoreDoors == False:
                        break
                    
                # Spaceship Exit #
                if targetExit == "Spaceship Exit" and currentRoom.spaceshipObject != None:
                    if currentRoom.spaceshipObject.landedLocation != None:
                        landedLocation = currentRoom.spaceshipObject.landedLocation
                        if Room.exists(galaxyList, None, currentRoom.spaceshipObject.galaxy, currentRoom.spaceshipObject.system, currentRoom.spaceshipObject.planet, landedLocation[0], landedLocation[1]) != None:
                            currentRoom = Room.exists(galaxyList, None, currentRoom.spaceshipObject.galaxy, currentRoom.spaceshipObject.system, currentRoom.spaceshipObject.planet, landedLocation[0], landedLocation[1])
                            currentArea = galaxyList[currentRoom.galaxy].systemList[currentRoom.system].planetList[currentRoom.planet].areaList[currentRoom.area]
                            
                # Spaceship Room #
                elif len(targetExit) == 3 and currentRoom.spaceshipObject != None:
                    if currentArea.num != targetExit[1]:
                        currentArea = currentRoom.spaceshipObject.areaList[targetExit[1]]
                    if targetExit[2] < len(currentArea.roomList):
                        currentRoom = currentArea.roomList[targetExit[2]]

                # Planet Room #
                elif Room.exists(galaxyList, None, targetExit[0], targetExit[1], targetExit[2], targetExit[3], targetExit[4]) != None:
                    currentRoom = Room.exists(galaxyList, None, targetExit[0], targetExit[1], targetExit[2], targetExit[3], targetExit[4])
                    if currentArea.num != targetExit[3]:
                        currentArea = galaxyList[targetExit[0]].systemList[targetExit[1]].planetList[targetExit[2]].areaList[targetExit[3]]
                        
        return currentArea, currentRoom, rNum + 1, messageType

    @staticmethod
    def getSurroundingRoomData(galaxyList, startArea, startRoom, targetRange):
        oppositeDir = {"North":"South", "East":"West", "South":"North", "West":"East", "Up":"Down", "Down":"Up"}
        def examineRoomData(targetArea, targetRoom, targetRange, targetDir, examinedAreaList, examinedRoomList, viewLoc):
            if targetArea not in examinedAreaList:
                examinedAreaList.append(targetArea)
            examinedRoomList.append(targetRoom)

            if viewLoc[0] + viewLoc[1] + viewLoc[2] < targetRange:
                firstLoc = copy.deepcopy(viewLoc)
                exitDirList = ["North", "East", "South", "West", "Up", "Down"]
                if targetDir != None and oppositeDir[targetDir] in exitDirList:
                    del exitDirList[exitDirList.index(oppositeDir[targetDir])]
                for targetExitDir in exitDirList:
                    if targetExitDir != "North":
                        viewLoc = copy.deepcopy(firstLoc)
                    if targetExitDir in targetRoom.exit:
                        nextArea, nextRoom, distance, message = Room.getTargetRoomFromStartRoom(galaxyList, targetArea, targetRoom, targetExitDir, 1, True)
                        if targetExitDir in ["East", "West"] : viewLoc[0] += 1
                        elif targetExitDir in ["North", "South"] : viewLoc[1] += 1
                        elif targetExitDir in ["Up", "Down"] : viewLoc[2] += 1
                        if nextRoom not in examinedRoomList:
                            examinedAreaList, examinedRoomList = examineRoomData(nextArea, nextRoom, targetRange, targetExitDir, examinedAreaList, examinedRoomList, viewLoc)

            return examinedAreaList, examinedRoomList
        return examineRoomData(startArea, startRoom, targetRange, None, [], [], [0, 0, 0])

    @staticmethod
    def getTargetRange(galaxyList, startRoom, targetObject, maxRange):
        targetFoundCheck = False
        targetRange = 0
        searchDir = None
        messageType = None
        if hasattr(targetObject, "currentHealth"):
            if (targetObject.num != None and targetObject in startRoom.mobList) or \
            (targetObject.num == None and startRoom.sameRoomCheck(targetObject) == True):
                return 0, None, None
        else:
            if startRoom.sameRoomCheck(targetObject) == True:
                return 0, None, None

        sideDirList = {"North":["East", "West", "Up", "Down"],
                        "East":["North", "South", "Up", "Down"],
                        "South":["East", "West", "Up", "Down"],
                        "West":["North", "South", "Up", "Down"],
                        "Up":["North", "East", "South", "West"],
                        "Down":["North", "East", "South", "West"]}
        for searchDir in ["North", "East", "South", "West", "Up", "Down"]:
            messageMaster = None
            currentRoom = startRoom
            if currentRoom.spaceshipObject != None:
                currentArea = currentRoom.spaceshipObject.areaList[currentRoom.area]
            else:
                currentArea = galaxyList[currentRoom.galaxy].systemList[currentRoom.system].planetList[currentRoom.planet].areaList[currentRoom.area]
            for rNum in range(maxRange):
                messageType = messageMaster
                if currentRoom.exit[searchDir] == None:
                    break
                else:
                    currentArea, currentRoom, distance, message = Room.getTargetRoomFromStartRoom(galaxyList, currentArea, currentRoom, searchDir, 1, True)
                    if message == "Door Is Closed":
                        messageMaster = message

                    if hasattr(targetObject, "currentHealth"):
                        if (targetObject.num != None and targetObject in currentRoom.mobList) or \
                        (targetObject.num == None and currentRoom.sameRoomCheck(targetObject) == True):
                            messageType = messageMaster
                            targetFoundCheck = True
                            targetRange = rNum + 1
                            break
                    else:
                        if currentRoom.sameRoomCheck(targetObject) == True:
                            messageType = messageMaster
                            targetFoundCheck = True
                            targetRange = rNum + 1
                            break

                    for sideDir in sideDirList[searchDir]:
                        messageType = messageMaster
                        sideRoom = currentRoom
                        sideArea = currentArea
                        for sideNum in range(maxRange - (rNum + 1)):
                            if sideRoom.exit[sideDir] == None:
                                break
                            else:
                                if sideRoom.exit[sideDir] == None:
                                    break
                                else:
                                    sideArea, sideRoom, distance, message = Room.getTargetRoomFromStartRoom(galaxyList, sideArea, sideRoom, sideDir, 1, True)
                                    if message == "Door Is Closed" : messageType = message

                                    if hasattr(targetObject, "currentHealth"):
                                        if targetObject in sideRoom.mobList or \
                                        (targetObject.num == None and sideRoom.sameRoomCheck(targetObject) == True):
                                            targetFoundCheck = True
                                            targetRange = (rNum + 1) + (sideNum + 1)
                                            break
                                    else:
                                        if sideRoom.sameRoomCheck(targetObject) == True:
                                            targetFoundCheck = True
                                            targetRange = (rNum + 1) + (sideNum + 1)
                                            break
                                        
                        if targetFoundCheck : break
                if targetFoundCheck : break
            if targetFoundCheck : break

        if not targetFoundCheck:
            return -1, None, messageType
        else:
            return targetRange, searchDir, messageType

    @staticmethod
    def getAreaAndRoom(galaxyList, target):
        if isinstance(target, Room):
            if target.spaceshipObject != None:
                spaceshipNum = target.spaceshipObject.num
                targetGalaxy = target.spaceshipObject.galaxy
                targetSystem = target.spaceshipObject.system
                targetPlanet = target.spaceshipObject.planet
            else:
                spaceshipNum = None
        else:
            spaceshipNum = target.spaceship
            targetGalaxy = target.galaxy
            targetSystem = target.system
            targetPlanet = target.planet

        if spaceshipNum != None:
            targetRoom = Room.exists(galaxyList, spaceshipNum, targetGalaxy, targetSystem, targetPlanet, target.area, target.room)
        else:
            targetRoom = Room.exists(galaxyList, None, target.galaxy, target.system, target.planet, target.area, target.room)
        
        if targetRoom == None:
            targetRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
        if targetRoom.spaceshipObject != None:
            targetArea = targetRoom.spaceshipObject.areaList[target.area]
        else:
            targetArea = galaxyList[target.galaxy].systemList[target.system].planetList[target.planet].areaList[target.area]
        return targetArea, targetRoom
        
    @staticmethod
    def getOppositeDirection(targetDirection):
        targetDirection = targetDirection.lower()
        if targetDirection[0] == "n" : return "South"
        elif targetDirection[0] == "e" : return "West"
        elif targetDirection[0] == "s" : return "North"
        elif targetDirection[0] == "w" : return "East"
        elif targetDirection[0] == "u" : return "Down"
        else : return "Up"

    @staticmethod
    def getTargetDirection(targetDirectionString):
        targetDirectionString = targetDirectionString.lower()
        if targetDirectionString[0] == "n" : lookDir = "North"
        elif targetDirectionString[0] == "e" : lookDir = "East"
        elif targetDirectionString[0] == "s" : lookDir = "South"
        elif targetDirectionString[0] == "w" : lookDir = "West"
        elif targetDirectionString[0] == "u" : lookDir = "Up"
        else : lookDir = "Down"
        return lookDir
