import random
from Components.Utility import stringIsNumber
from GameData.Room import Room
from GameData.Mob import Mob
from GameData.Item import Item
from GameData.Spaceship import Spaceship

class Player:

    def __init__(self):
        self.spaceship = None
        self.galaxy = 0
        self.system = 0
        self.planet = 1
        self.area = 0
        self.room = 0

        self.itemDict = {"Armor": [], "Weapon":[], "Misc": []}
        self.gearDict = {"Head":None, "Face":None, "Neck":[None, None], "Body Under":None, "Body Over":None, "Hands":None, "Finger":[None, None], "Legs Under":None, "Legs Over":None, "Feet":None, "Left Hand":None, "Right Hand":None}
        self.maxWeight = 150.0
        self.dominantHand = "Right Hand"

        self.maxLookDistance = 5

        self.emoteList = ["hmm", "hm", "nod", "nodnod", "tap", "boggle", "jump"]

        self.debugDualWield = False

    def lookDirection(self, console, galaxyList, lookDir, count):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        if currentRoom != None:
            messageType = None
            lookCheck = False
            lookDistance = count
            if lookDistance > self.maxLookDistance:
                lookDistance = self.maxLookDistance
            for i in range(lookDistance):
                if currentRoom.exit[lookDir] == None:
                    messageType = "Can't See Further"
                    break
                elif currentRoom.door[lookDir] != None and currentRoom.door[lookDir]["Status"] in ["Closed", "Locked"]:
                    messageType = "View Obstructed"
                    break
                else:
                    lookCheck = True
                    if len(currentRoom.exit[lookDir]) == 3 and currentRoom.spaceshipObject != None:
                        currentRoom = currentRoom.spaceshipObject.areaList[currentRoom.exit[lookDir][1]].roomList[currentRoom.exit[lookDir][2]]
                    elif len(currentRoom.exit[lookDir]) == 5:
                        currentRoom = Room.exists(galaxyList, None, currentRoom.exit[lookDir][0], currentRoom.exit[lookDir][1], currentRoom.exit[lookDir][2], currentRoom.exit[lookDir][3], currentRoom.exit[lookDir][4])
                    if currentRoom == None:
                        currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                    
            if messageType != None:
                countString = ""
                countCode = ""
                if i > 0:
                    sString = ""
                    if i > 1:
                        sString = "s"
                    countString = " (" + str(i) + " Room" + sString + " Away)"
                    if sString == "" : countCode = "2r" + str(len(str(i))) + "w10w1r"
                    else : countCode = "2r" + str(len(str(i))) + "w11w1r"

                console.lineList.insert(0, {"Blank": True})
                if messageType == "Can't See Further":
                    console.lineList.insert(0, {"String":"You can't see any farther to the " + lookDir + "." + countString, "Code":"7w1y25w" + str(len(lookDir)) + "w1y" + countCode})
                elif messageType == "View Obstructed":
                    console.lineList.insert(0, {"String":"Your view to the " + lookDir + " is obstructed." + countString, "Code":"17w" + str(len(lookDir)) + "w14w1y" + countCode})
            if lookCheck:
                console.lineList.insert(0, {"Blank": True})
                currentRoom.display(console, galaxyList, self)
        
    def lookTargetCheck(self, console, galaxyList, lookDir, count, lookTarget):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        messageType = None
        lookCount = 0
        if currentRoom != None and count != None:
            lookDistance = count
            if lookDistance > self.maxLookDistance:
                lookDistance = self.maxLookDistance
            for i in range(lookDistance):
                if currentRoom.exit[lookDir] == None:
                    messageType = "Can't See Further"
                    break
                elif currentRoom.door[lookDir] != None and currentRoom.door[lookDir]["Status"] in ["Closed", "Locked"]:
                    messageType = "View Obstructed"
                    break
                else:
                    if len(currentRoom.exit[lookDir]) == 3 and currentRoom.spaceshipObject != None:
                        currentRoom = currentRoom.spaceshipObject.areaList[currentRoom.exit[lookDir][1]].roomList[currentRoom.exit[lookDir][2]]
                    elif len(currentRoom.exit[lookDir]) == 5:
                        currentRoom = Room.exists(galaxyList, None, currentRoom.exit[lookDir][0], currentRoom.exit[lookDir][1], currentRoom.exit[lookDir][2], currentRoom.exit[lookDir][3], currentRoom.exit[lookDir][4])
                    if currentRoom == None:
                        currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                    lookCount += 1
                    
        if messageType == "Can't See Further":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "There is nothing there.", "Code":"22w1y"})
        elif messageType == "View Obstructed":
            countString = ""
            countCode = ""
            if lookCount > 0:
                countString = " (" + str(lookCount) + " Room Away)"
                countCode = "2r" + str(len(str(lookCount))) + "w10w1r"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "Your view to the " + lookDir + " is obstructed." + countString, "Code":"17w" + str(len(lookDir)) + "w14w1y" + countCode})
            
            if lookCount > 0:
                console.lineList.insert(0, {"Blank": True})
                currentRoom.display(console, galaxyList, self)

        else:
            roomTarget = currentRoom.getTargetObject(lookTarget)
            if roomTarget == None and count == None:
                roomTarget = self.getTargetItem(lookTarget)

            if currentRoom.isLit(galaxyList, self) == False and not (isinstance(roomTarget, Item) and roomTarget.containerList != None and roomTarget.lightInContainerCheck() == True):
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})
            elif roomTarget == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You don't see it.", "Code":"7w1y8w1y"})
            else:
                if isinstance(roomTarget, Item):
                    passwordCheck = False
                    if roomTarget.containerPassword != None:
                        passwordCheck = self.hasKey(roomTarget.containerPassword)
                    roomTarget.lookDescription(console, lookCount, passwordCheck)
                else:
                    roomTarget.lookDescription(console)

    def targetCheck(console, galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, targetDirCount):
        pass

    def moveCheck(self, console, galaxyList, targetDir):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        if currentRoom != None:
            if currentRoom.exit[targetDir] != None:
                if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Manual" and currentRoom.door[targetDir]["Status"] in ["Closed", "Locked"]:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String": "The door is closed.", "Code":"18w1y"})
                elif currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic" and currentRoom.door[targetDir]["Status"] == "Locked" and "Password" in currentRoom.door[targetDir] and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String": "You lack the proper key.", "Code":"23w1y"})

                else:
                    targetRoom = None
                    targetRoomData = currentRoom.exit[targetDir]
                    if len(targetRoomData) == 3 and currentRoom.spaceshipObject != None:
                        targetRoom = currentRoom.spaceshipObject.areaList[targetRoomData[1]].roomList[targetRoomData[2]]
                    elif len(targetRoomData) == 5:
                        targetRoom = Room.exists(galaxyList, None, targetRoomData[0], targetRoomData[1], targetRoomData[2], targetRoomData[3], targetRoomData[4])
                    elif targetRoomData == "Spaceship Exit" and currentRoom.spaceshipObject != None:
                        targetRoom = Room.exists(galaxyList, None, currentRoom.spaceshipObject.landedLocation[0], currentRoom.spaceshipObject.landedLocation[1], currentRoom.spaceshipObject.landedLocation[2], currentRoom.spaceshipObject.landedLocation[3], currentRoom.spaceshipObject.landedLocation[4])

                    if targetRoom != None:
                        if len(targetRoomData) == 3:
                            self.area = targetRoomData[1]
                            self.room = targetRoomData[2]
                        else:
                            self.galaxy = targetRoom.galaxy
                            self.system = targetRoom.system
                            self.planet = targetRoom.planet
                            self.area = targetRoom.area
                            self.room = targetRoom.room
                            if self.spaceship != None:
                                self.spaceship = None

                        console.lineList.insert(0, {"Blank": True})
                        if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic":
                            doorString = "door"
                            if currentRoom.exit[targetDir] == "Spaceship Exit":
                                doorString = "hatch"
                            console.lineList.insert(0, {"String": "The " + doorString + " opens and closes as you walk through.", "Code":"4w" + str(len(doorString)) + "w37w1y"})
                            console.lineList.insert(0, {"Blank": True})
                        targetRoom.display(console, galaxyList, self)

            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You can't go that way!", "Code":"7w1y13w1y"})

    def openCloseDoorCheck(self, console, galaxyList, currentRoom, targetAction, targetDir):
        targetDoorAction = targetAction
        if targetAction == "Close":
            targetDoorAction = "Closed"

        if currentRoom.door[targetDir] == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"There is no door in that direction.", "Code":"34w1y"})
        elif currentRoom.door[targetDir]["Type"] == "Automatic":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door is automatic.", "Code":"22w1y"})
        elif currentRoom.door[targetDir]["Status"] == targetDoorAction or (targetDoorAction == "Closed" and currentRoom.door[targetDir]["Status"] == "Locked"):
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"It's already " + targetDoorAction.lower() + ".", "Code":"2w1y10w" + str(len(targetDoorAction)) + "w1y"})
        elif targetDoorAction == "Open" and currentRoom.door[targetDir]["Status"] == "Locked" and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"It's locked.", "Code":"2w1y8w1y"})
        
        else:
            unlockString = ""
            unlockCode = ""
            if currentRoom.door[targetDir]["Status"] == "Locked" and targetDoorAction == "Open":
                unlockString = "unlock and "
                unlockCode = "11w"

            currentRoom.door[targetDir]["Status"] = targetDoorAction

            if currentRoom.exit[targetDir] != None:
                otherRoom = None
                if len(currentRoom.exit[targetDir]) == 3 and currentRoom.spaceshipObject != None:
                    otherRoom = currentRoom.spaceshipObject.areaList[currentRoom.exit[targetDir][1]].roomList[currentRoom.exit[targetDir][2]]
                elif len(currentRoom.exit[targetDir]) == 5:
                    otherRoom = Room.exists(galaxyList, None, currentRoom.exit[targetDir][0], currentRoom.exit[targetDir][1], currentRoom.exit[targetDir][2], currentRoom.exit[targetDir][3], currentRoom.exit[targetDir][4])
                if otherRoom != None:
                    otherRoomExitDir = None
                    for exitDir in otherRoom.exit:
                        exitData = otherRoom.exit[exitDir]
                        if exitData != None and currentRoom.sameRoomCheck(exitData):
                            otherRoomExitDir = exitDir
                            break

                    if otherRoomExitDir != None:
                        otherRoom.door[otherRoomExitDir]["Status"] = targetDoorAction

            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You " + unlockString + targetAction.lower() + " the door to the " + targetDir + ".", "Code":"4w" + unlockCode + str(len(targetAction)) + "w17w" + str(len(targetDir)) + "w1y"})

    def lockUnlockDoorCheck(self, console, galaxyList, currentRoom, targetAction, targetDir):
        if targetAction == "Lock":
            targetActionStatus = "Locked"
        else:
            targetActionStatus = "Closed"

        if currentRoom.door[targetDir] == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"There is no door in that direction.", "Code":"34w1y"})
        elif "Password" not in currentRoom.door[targetDir]:
            haveString = "require a key"
            if targetAction == "Lock":
                haveString = "have a lock"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door doesn't " + haveString + ".", "Code":"15w1y2w" + str(len(haveString)) + "w1y"})
        elif currentRoom.door[targetDir]["Type"] == "Automatic":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door " + targetAction.lower() + "s automatically.", "Code":"10w" + str(len(targetAction)) + "w15w1y"})
        elif currentRoom.door[targetDir]["Status"] == targetActionStatus:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"It's already " + targetAction.lower() + "ed.", "Code":"2w1y10w" + str(len(targetAction)) + "w2w1y"})
        elif self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You lack the key.", "Code":"16w1y"})
        
        else:
            closeString = ""
            closeCode = ""
            if targetRoom.door[targetDir]["Status"] == "Open" and targetActionStatus == "Locked":
                closeString = "close and "
                closeCode = "10w"

            targetRoom.door[targetDir]["Status"] = targetActionStatus
            
            if targetRoom.exit[targetDir] != None:
                otherRoom = None
                if len(targetRoom.exit[targetDir]) == 3 and targetRoom.spaceshipObject != None:
                    otherRoom = targetRoom.spaceshipObject.areaList[targetRoom.exit[targetDir][1]].roomList[targetRoom.exit[targetDir][2]]
                elif len(targetRoom.exit[targetDir]) == 5:
                    otherRoom = Room.exists(galaxyList, None, targetRoom.exit[targetDir][0], targetRoom.exit[targetDir][1], targetRoom.exit[targetDir][2], targetRoom.exit[targetDir][3], targetRoom.exit[targetDir][4])
                if otherRoom != None:
                    otherRoomExitDir = None
                    for exitDir in otherRoom.exit:
                        exitData = otherRoom.exit[exitDir]
                        if exitData != None and targetRoom.sameRoomCheck(exitData):
                            otherRoomExitDir = exitDir
                            break

                    if otherRoomExitDir != None:
                        otherRoom.door[otherRoomExitDir]["Status"] = targetActionStatus
                    
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You " + closeString + targetAction.lower() + " the door to the " + targetDir + ".", "Code":"4w" + closeCode + str(len(targetAction)) + "w17w" + str(len(targetDir)) + "w1y"})

    def openCloseTargetCheck(self, console, galaxyList, currentRoom, targetAction, targetObjectKey):
        targetObject = currentRoom.getTargetObject(targetObjectKey)
        if targetObject == None:
            targetObject = self.getTargetItem(targetObjectKey)

        if currentRoom.isLit(galaxyList, self) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})
        elif targetObject == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You don't see it.", "Code":"7w1y8w1y"})
        
        elif isinstance(targetObject, Mob):
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You can't " + targetAction.lower() + " that!", "Code":"7w1y2w" + str(len(targetAction)) + "w5w1y"})
        
        elif isinstance(targetObject, Spaceship):
            if targetObject.hatchPassword != None and self.hasKey(targetObject.hatchPassword) == False:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "It's locked.", "Code":"2w1y8w1y"})
            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The hatch " + targetAction.lower() + "s automatically.", "Code":"10w" + str(len(targetAction)) + "w15w1y"})
            
        elif isinstance(targetObject, Item):
            if targetObject.containerList == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "It doesn't " + targetAction.lower() + ".", "Code":"8w1y2w" + str(len(targetAction)) + "w1y"})
            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"There is no need to " + targetAction.lower() + " it.", "Code":"20w" + str(len(targetAction)) + "w3w1y"})
            
    def lockUnlockTargetCheck(self, console, galaxyList, currentRoom, targetAction, targetObjectKey):
        targetObject = currentRoom.getTargetObject(targetObjectKey)
        if targetObject == None:
            targetObject = self.getTargetItem(targetObjectKey)
            
        if currentRoom.isLit(galaxyList, self) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})
        elif targetObject == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You don't see it.", "Code":"7w1y8w1y"})
        
        elif isinstance(targetObject, Mob):
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You can't " + targetAction.lower() + " that!", "Code":"7w1y2w" + str(len(targetAction)) + "w5w1y"})
        
        elif isinstance(targetObject, Spaceship):
            if targetObject.hatchPassword == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The hatch doesn't have a lock.", "Code":"15w1y13w1y"})
            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The hatch " + targetAction.lower() + "s automatically.", "Code":"10w" + str(len(targetAction)) + "w15w1y"})
        
        elif isinstance(targetObject, Item):
            if targetObject.containerList == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "It doesn't " + targetAction.lower() + ".", "Code":"8w1y2w" + str(len(targetAction)) + "w1y"})
            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"There is no need to " + targetAction.lower() + " it.", "Code":"20w" + str(len(targetAction)) + "w3w1y"})

    def getCheck(self, console, galaxyList, currentRoom, targetItemKey, targetContainerKey, count):
        itemList = currentRoom.itemList
        if targetContainerKey != None:
            if targetContainerKey == "All":
                itemList = "All Room Containers"
            else:
                itemList = currentRoom.getTargetObject(targetContainerKey)

        if targetContainerKey not in [None, "All"] and itemList != None and (isinstance(itemList, Item) == False or itemList.containerList == None):
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That's not a container!", "Code":"4w1y17w1y"})
        else:
            if isinstance(itemList, Item):
                itemList = itemList.containerList

            getItem = None
            if itemList != None:
                if targetItemKey != "All":
                    if itemList == "All Room Containers":
                        breakCheck = False
                        for container in currentRoom.itemList:
                            if container.containerList != None:
                                for item in container.containerList:
                                    if targetItemKey in item.keyList:
                                        getItem = item
                                        breakCheck = True
                                        break
                            if breakCheck:
                                break
                    else:
                        for item in itemList:
                            if targetItemKey in item.keyList:
                                getItem = item
                                break
            
            if itemList == None or (targetItemKey != "All" and getItem == None):
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

            else:
                if itemList == "All Room Containers":
                    itemCount = 0
                    for container in currentRoom.itemList:
                        if container.containerList != None and len(container.containerList) > 0:
                            itemCount += len(container.containerList)
                else:
                    itemCount = len(itemList)

                if targetContainerKey == "All" and itemCount == 0:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"There is nothing to loot.", "Code":"24w1y"})
                
                else:
                    getCount = 0
                    getContainerIndexList = []
                    noGetCheck = False
                    tooMuchWeightCheck = False
                    for c in range(itemCount):
                        containerCount = 1
                        if targetContainerKey == "All":
                            containerCount = len(currentRoom.itemList)
                        for containerIndex in range(containerCount):
                            delIndex = -1
                            if targetContainerKey == "All":
                                itemList = currentRoom.itemList[containerIndex].containerList
                            for i, item in enumerate(itemList):
                                if targetItemKey == "All" or targetItemKey in item.keyList:
                                    if "No Get" in item.flags:
                                        noGetCheck = True
                                    elif self.getCurrentWeight() + item.weight > self.maxWeight:
                                        tooMuchWeightCheck = True
                                    else:
                                        self.itemDict[item.pocket].append(item)
                                        getCount += 1
                                        if getItem == None:
                                            getItem = item
                                        elif getItem != "Multiple" and getItem.num != item.num:
                                            getItem = "Multiple"
                                        if containerIndex not in getContainerIndexList:
                                            getContainerIndexList.append(containerIndex)

                                        delIndex = i
                                        break
                            if delIndex != -1:
                                del itemList[delIndex]
                                break
                        if count != "All" and getCount == count:
                            break
                        
                    if getCount == 0:
                        if noGetCheck == True:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick that up.", "Code":"7w1y14w1y"})
                        elif tooMuchWeightCheck == True:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't carry that much weight.", "Code":"7w1y24w1y"})
                        elif itemCount == 0:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"There is nothing to get.", "Code":"23w1y"})
                        else:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick anything up.", "Code":"7w1y18w1y"})
                    else:
                        if targetContainerKey == "All" and (count == "All" or count > 1):
                            modString = ""
                            modCode = ""
                            if tooMuchWeightCheck == False and targetItemKey == "All":
                                modString = "every corner of "
                                modCode = "16w"
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You loot " + modString + "the place.", "Code":"9w" + modCode + "9w1y"})
                        elif targetContainerKey == None and getCount == itemCount:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You pick everything up.", "Code":"22w1y"})
                        elif getItem == "Multiple":
                            if targetContainerKey != None and getContainerIndexList[-1] < len(currentRoom.itemList):
                                targetContainer = currentRoom.itemList[getContainerIndexList[-1]]
                                console.lineList.insert(0, {"Blank": True})
                                console.lineList.insert(0, {"String":"You get some things out of " + targetContainer.prefix.lower() + " " + targetContainer.name["String"] + ".", "Code":"27w" + str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"] + "1y"})
                            else:
                                console.lineList.insert(0, {"Blank": True})
                                console.lineList.insert(0, {"String":"You pick some things up.", "Code":"23w1y"})
                        elif getItem != "Multiple":
                            countString = ""
                            countCode = ""
                            if getCount > 1:
                                countString = " (" + str(getCount) + ")"
                                countCode = "2r" + str(len(str(getCount))) + "w1r"
                            fromString = ""
                            fromCode = ""
                            if targetContainerKey != None and getContainerIndexList[0] < len(currentRoom.itemList):
                                targetContainer = currentRoom.itemList[getContainerIndexList[0]]
                                targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                                targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                                if currentRoom.isLit(galaxyList, self) == False:
                                    targetContainerString = "something"
                                    targetContainerCode = "9w"
                                fromString = " from " + targetContainerString
                                fromCode = "6w" + targetContainerCode
                            getString = "You get " + getItem.prefix.lower() + " " + getItem.name["String"] + countString + fromString + "."
                            getCode = "8w" + str(len(getItem.prefix)) + "w1w" + getItem.name["Code"] + countCode + fromCode + "1y"
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":getString, "Code":getCode})
                        
    def getCurrentWeight(self):
        currentWeight = 0.0
        for itemPocket in self.itemDict:
            for item in self.itemDict[itemPocket]:
                currentWeight += item.weight
        return currentWeight

    def putCheck(self, console, galaxyList, currentRoom, targetItemKey, targetContainerKey, count):
        targetContainer = currentRoom.getTargetObject(targetContainerKey)
        if targetContainer == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
        elif isinstance(targetContainer, Item) == False or targetContainer.containerList == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That's not a container!", "Code":"4w1y17w1y"})
        
        else:
            putItem = None
            inventorySize = 0
            breakCheck = False
            for pocket in self.itemDict:
                inventorySize += len(self.itemDict[pocket])
                if targetItemKey != "All":
                    for item in self.itemDict[pocket]:
                        if putItem == None and targetItemKey in item.keyList:
                            putItem = item

            if targetItemKey != "All" and putItem == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
            elif inventorySize == 0:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have anything.", "Code":"7w1y15w1y"})

            else:
                putCount = 0
                for i in range(inventorySize):
                    breakCheck = False
                    for pocket in self.itemDict:
                        delIndex = -1
                        for i, item in enumerate(self.itemDict[pocket]):
                            if targetContainer.getContainerWeight() + item.weight <= targetContainer.containerMaxLimit:
                                if targetItemKey == "All" or targetItemKey in item.keyList:
                                    targetContainer.containerList.append(item)
                                    putCount += 1
                                    if putItem == None:
                                        putItem = item
                                    elif putItem != "Multiple" and putItem.num != item.num:
                                        putItem = "Multiple"
                                    delIndex = i
                                    breakCheck = True
                                    break
                        if delIndex != -1:
                            del self.itemDict[pocket][i]
                        if breakCheck == True:
                            break
                    if count != "All" and putCount == count:
                        break

                if putCount == 0:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"It won't fit.", "Code":"6w1t5w1y"})
                elif putItem == "Multiple":
                    targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                    targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                    if currentRoom.isLit(galaxyList, self) == False:
                        targetContainerString = "something"
                        targetContainerCode = "9w"
                    displayString = "You put some things in " + targetContainerString + "."
                    displayCode = "23w" + targetContainerCode + "1y"
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                else:
                    countString = ""
                    countCode = ""
                    if putCount > 1:
                        countString = " (" + str(putCount) + ")"
                        countCode = "2r" + str(len(str(putCount))) + "w1r"
                    targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                    targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                    if currentRoom.isLit(galaxyList, self) == False:
                        targetContainerString = "something"
                        targetContainerCode = "9w"
                    displayString = "You put " + putItem.prefix.lower() + " " + putItem.name["String"] + countString + " in " + targetContainerString + "."
                    displayCode = "8w" + str(len(putItem.prefix)) + "w1w" + putItem.name["Code"] + countCode + "4w" + targetContainerCode + "1y"
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                
    def dropCheck(self, console, galaxyList, currentRoom, targetItemKey, count):
        dropItem = None
        breakCheck = False
        if targetItemKey != "All":
            for pocket in self.itemDict:
                for item in self.itemDict[pocket]:
                    if targetItemKey in item.keyList:
                        dropItem = item
                        breakCheck = True
                        break
                if breakCheck:
                    break

        if targetItemKey != "All" and dropItem == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

        else:
            dropCount = 0
            delDict = {}
            breakCheck = False
            for pocket in self.itemDict:
                delDict[pocket] = []
                for i, item in enumerate(self.itemDict[pocket]):
                    if targetItemKey == "All" or targetItemKey in item.keyList:
                        currentRoom.itemList.append(item)
                        delDict[pocket].append(i)
                        dropCount += 1

                        if dropItem == None:
                            dropItem = item
                        elif dropItem != "Multiple" and dropItem.num != item.num:
                            dropItem = "Multiple"

                        if count != "All" and dropCount >= count:
                            breakCheck = True
                            break
                if breakCheck:
                    break

            inventoryCount = 0
            for pocket in self.itemDict:
                inventoryCount += len(self.itemDict[pocket])

            for pocket in delDict:
                delDict[pocket].reverse()
                for i in delDict[pocket]:
                    del self.itemDict[pocket][i]

            if dropCount == 0:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You aren't carrying anything.", "Code":"8w1y19w1y"})
            elif dropCount > 1 and dropCount == inventoryCount:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You drop everything on the ground.", "Code":"33w1y"})    
            elif dropItem == "Multiple":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You drop some things on the ground.", "Code":"34w1y"})
            elif dropItem != None:
                countString = ""
                countCode = ""
                if dropCount > 1:
                    countString = " (" + str(dropCount) + ")"
                    countCode = "2r" + str(len(str(dropCount))) + "w1r"
                dropString = "You drop " + dropItem.prefix.lower() + " " + dropItem.name["String"] + " on the ground." + countString
                dropCode = "9w" + str(len(dropItem.prefix.lower())) + "w1w" + dropItem.name["Code"] + "14w1y" + countCode
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":dropString, "Code":dropCode})
            
    def displayInventory(self, console, galaxyList, currentRoom, targetPocketKey):
        targetPocket = None
        if targetPocketKey in ["armor", "armo", "arm", "ar", "a"]:
            targetPocket = "Armor"
        elif targetPocketKey in ["weapons", "weapon", "weapo", "weap", "wea", "we", "w"]:
            targetPocket = "Weapon"
        elif targetPocketKey in ["misc.", "misc", "mis", "mi", "m"]:
            targetPocket = "Misc"

        if targetPocket not in self.itemDict:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"Open which bag? (Armor, Weapon, Misc.)", "Code":"14w2y1r5w2y6w2y4w1y1r"})

        else:
            displayDict = {}
            for item in self.itemDict[targetPocket]:
                if item.num not in displayDict:
                    displayDict[item.num] = {"Count": 1, "ItemData": item}
                else:
                    displayDict[item.num]["Count"] += 1
            
            targetPocketDisplayString = targetPocket
            targetPocketDisplayCode = str(len(targetPocket)) + "w"
            if targetPocket == "Misc":
                targetPocketDisplayString = "Misc."
                targetPocketDisplayCode = "4w1y"
            underlineString = ""
            underlineCode = ""
            for i in range(len(targetPocketDisplayString) + 4):
                underlineChar = "-"
                indentCount = int(len(targetPocketDisplayString + " Bag") * .25)
                if indentCount <= 0:
                    indentCount = 1
                if i not in range(0, indentCount) and i not in range(len(targetPocketDisplayString + " Bag") - indentCount, len(targetPocketDisplayString + " Bag")):
                    underlineChar = "="
                underlineString = underlineString + underlineChar
                if i % 2 == 1:
                    underlineCode = underlineCode + "1y"
                else:
                    underlineCode = underlineCode + "1dy"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": targetPocketDisplayString + " Bag", "Code": targetPocketDisplayCode + "4w"})
            console.lineList.insert(0, {"String": underlineString, "Code": underlineCode})

            if len(self.itemDict[targetPocket]) == 0:
                console.lineList.insert(0, {"String": "-Empty", "Code": "1y5w"})
            elif currentRoom.isLit(galaxyList, self) == False and self.lightInBagCheck(targetPocket) == False:
                countString = ""
                countCode = ""
                inventoryCount = 0
                for displayItemData in displayDict:
                    inventoryCount += displayDict[displayItemData]["Count"]
                if inventoryCount > 1:
                    countString = " (" + str(inventoryCount) + ")"
                    countCode = "2r" + str(len(str(inventoryCount))) + "w1r"
                console.lineList.insert(0, {"String": "-Something" + countString, "Code": "1y9w" + countCode})
            else:
                for item in self.itemDict[targetPocket]:
                    if item.num in displayDict:
                        modString = ""
                        modCode = ""
                        if "Glowing" in item.flags and item.flags["Glowing"] == True:
                            modString = " (Glowing)"
                            modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                        countString = ""
                        countCode = ""
                        if displayDict[item.num]["Count"] > 1:
                            countString = " (" + str(displayDict[item.num]["Count"]) + ")"
                            countCode = "2r" + str(len(str(displayDict[item.num]["Count"]))) + "w1r"
                        itemDisplayString = item.prefix + " " + item.name["String"]
                        itemDisplayCode = str(len(item.prefix)) + "w1w" + item.name["Code"]
                        console.lineList.insert(0, {"String":itemDisplayString + countString + modString, "Code":itemDisplayCode + countCode + modCode})
                        del displayDict[item.num]

    def wearCheck(self, console, targetItemKey, count, targetGearSlotIndex=None):
        wearItem = None
        if targetItemKey != "All":
            for item in self.itemDict["Armor"] + self.itemDict["Weapon"]:
                if targetItemKey in item.keyList:
                    wearItem = item
                    break

        if targetItemKey != "All" and wearItem == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
        elif targetItemKey != "All" and wearItem.pocket == "Weapon":
            tempCount = count
            if tempCount == "All":
                tempCount = 2
            self.wieldCheck(console, targetItemKey, targetGearSlotIndex, tempCount)
            return

        else:
            wearCount = 0
            wearItem = None
            delInvList = []
            previousWornItemList = []
            breakCheck = False
            for itemIndex, item in enumerate(self.itemDict["Armor"]):
                if item.gearSlot != None and item.gearSlot in self.gearDict:
                    targetGearSlot = self.gearDict[item.gearSlot]
                    slotRange = 1
                    if targetGearSlotIndex == None and isinstance(targetGearSlot, list):
                        slotRange = len(targetGearSlot)
                    for slotIndex in range(slotRange):
                        if isinstance(self.gearDict[item.gearSlot], list):
                            for emptySlotIndex, slot in enumerate(self.gearDict[item.gearSlot]):
                                if self.gearDict[item.gearSlot][emptySlotIndex] == None:
                                    slotIndex = emptySlotIndex
                                    break
                                    
                        if targetGearSlotIndex != None:
                            if targetGearSlotIndex in ["left", "lef", "le", "l"]:
                                targetGearSlotIndex = 0
                            elif targetGearSlotIndex in ["right", "righ", "rig", "ri", "r"]:
                                targetGearSlotIndex = 1
                            elif stringIsNumber(targetGearSlotIndex):
                                targetGearSlotIndex = int(targetGearSlotIndex)
                            if isinstance(self.gearDict[item.gearSlot], list):
                                if targetGearSlotIndex > len(self.gearDict[item.gearSlot]) - 1:
                                    targetGearSlotIndex = len(self.gearDict[item.gearSlot]) - 1
                            slotIndex = targetGearSlotIndex
                            
                        if isinstance(self.gearDict[item.gearSlot], list):
                            targetGearSlot = self.gearDict[item.gearSlot][slotIndex]
                        if targetGearSlot == None or targetItemKey != "All":
                            if targetItemKey == "All" or targetItemKey in item.keyList:
                                if isinstance(self.gearDict[item.gearSlot], list):
                                    if self.gearDict[item.gearSlot][slotIndex] != None:
                                        previousWornItemList.append(self.gearDict[item.gearSlot][slotIndex])
                                    self.gearDict[item.gearSlot][slotIndex] = item
                                else:
                                    if self.gearDict[item.gearSlot] != None:
                                        previousWornItemList.append(self.gearDict[item.gearSlot])
                                    self.gearDict[item.gearSlot] = item
                                wearCount += 1
                                if wearItem != "Multiple":
                                    if wearItem == None:
                                        wearItem = item
                                    elif wearItem.num != item.num:
                                        wearItem = "Multiple"
                                delInvList.append(itemIndex)

                                if count != "All" and wearCount >= count:
                                    breakCheck = True
                                break
                if breakCheck:
                    break

            delInvList.reverse()
            for delIndex in delInvList:
                del self.itemDict["Armor"][delIndex]
            for wornItem in previousWornItemList:
                self.itemDict[wornItem.pocket].append(wornItem)

            # Messages #
            if wearCount == 0 and len(self.itemDict["Armor"]) == 0:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have anything to wear.", "Code":"7w1y23w1y"})    
            elif wearCount == 0:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You are already wearing something.", "Code":"33w1y"})    
            elif len(previousWornItemList) > 0 and wearCount > 1:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You switch around some of your gear.", "Code":"35w1y"})
            elif len(previousWornItemList) == 0 and wearCount > 1:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You put on some armor.", "Code":"21w1y"})
            elif len(previousWornItemList) == 1 and isinstance(wearItem, Item):
                wearString = "You remove " + previousWornItemList[0].prefix.lower() + " " + previousWornItemList[0].name["String"] + " and wear " + wearItem.prefix.lower() + " " + wearItem.name["String"] + "."
                wearCode = "11w" + str(len(previousWornItemList[0].prefix)) + "w1w" + previousWornItemList[0].name["Code"] + "10w" + str(len(wearItem.prefix)) + "w1w" + wearItem.name["Code"] + "1y"
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":wearString, "Code":wearCode})
            elif len(previousWornItemList) == 0 and isinstance(wearItem, Item):
                wearString = "You wear " + wearItem.prefix.lower() + " " + wearItem.name["String"] + "."
                wearCode = "9w" + str(len(wearItem.prefix)) + "w1w" + wearItem.name["Code"] + "1y"
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":wearString, "Code":wearCode})

            # Wield Check #
            if targetItemKey == "All" and count == "All":
                self.wieldCheck(console, "All", None, 2, False)

    def wieldCheck(self, console, targetItemKey, targetGearSlotKey, count, blankCheck=True):
        wieldItem = None
        checkItem = None
        for pocket in self.itemDict:
            for item in self.itemDict[pocket]:
                if targetItemKey == "All" or targetItemKey in item.keyList:
                    if item.pocket == "Weapon" and wieldItem == None:
                        wieldItem = item
                    if checkItem == None:
                        checkItem = item

        if targetItemKey == "All" and (wieldItem == None or wieldItem.pocket != "Weapon"):
            if blankCheck == True : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You don't have anything to wield.", "Code":"7w1y24w1y"})
        elif wieldItem == None:
            if blankCheck == True : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
        elif wieldItem.pocket != "Weapon":
            if blankCheck == True : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't wield that.", "Code":"7w1y12w1y"})

        else:
            targetGearSlot = None
            if targetGearSlotKey != None:
                if stringIsNumber(targetGearSlotKey) == False:
                    if targetGearSlotKey in ["left", "lef", "le", "l"]:
                        targetGearSlot = "Left Hand"
                    elif targetGearSlotKey in ["right", "righ", "rig", "ri", "r"]:
                        targetGearSlot = "Right Hand"
                else:
                    if int(targetGearSlotKey) == 1 : targetGearSlot = "Left Hand"
                    else : targetGearSlot = "Right Hand"
                if wieldItem != None and wieldItem.twoHanded and self.debugDualWield == False:
                    targetGearSlot = self.dominantHand

            wieldCount = 0
            slotCount = 0
            slotItem = None
            breakCheck = False
            for c in range(count):
                defaultGearSlot = self.dominantHand
                if (targetItemKey == "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[defaultGearSlot].twoHanded == False and self.debugDualWield == False) or \
                (targetItemKey != "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[self.getOppositeHand(defaultGearSlot)] == None and self.gearDict[defaultGearSlot].twoHanded == False and wieldItem.twoHanded == False and count == 1) or \
                (c == 1 and not (self.gearDict[defaultGearSlot] != None and self.gearDict[defaultGearSlot].twoHanded == True and self.debugDualWield == False)):
                    defaultGearSlot = self.getOppositeHand(self.dominantHand)
                if targetGearSlot != None:
                    defaultGearSlot = targetGearSlot
                delIndex = -1
                for i, item in enumerate(self.itemDict["Weapon"]):
                    if targetItemKey == "All" or targetItemKey in item.keyList:
                        if not (targetItemKey == "All" and self.gearDict[defaultGearSlot] != None) and \
                        not (targetItemKey == "All" and item.twoHanded == True and (self.gearDict[self.dominantHand] != None or self.gearDict[self.getOppositeHand(self.dominantHand)] != None) and self.debugDualWield == False):
                            if self.gearDict[defaultGearSlot] != None:
                                self.itemDict[self.gearDict[defaultGearSlot].pocket].append(self.gearDict[defaultGearSlot])
                                slotCount += 1
                                if slotItem == None:
                                    slotItem = self.gearDict[defaultGearSlot]
                                elif slotItem != "Multiple" and slotItem.num != self.gearDict[defaultGearSlot].num:
                                    slotItem = "Multiple"
                            self.gearDict[defaultGearSlot] = item
                            oppositeHand = self.gearDict[self.getOppositeHand(defaultGearSlot)]
                            if oppositeHand != None and (self.gearDict[defaultGearSlot].twoHanded == True or oppositeHand.twoHanded == True) and self.debugDualWield == False:
                                self.itemDict[oppositeHand.pocket].append(oppositeHand)
                                self.gearDict[self.getOppositeHand(defaultGearSlot)] = None
                                slotCount += 1
                                if slotItem == None:
                                    slotItem = oppositeHand
                                elif slotItem != "Multiple" and slotItem.num != oppositeHand.num:
                                    slotItem = "Multiple"
                            wieldCount += 1
                            if wieldItem == None:
                                wieldItem = item
                            elif wieldItem != "Multiple" and wieldItem.num != item.num:
                                wieldItem = "Multiple"
                            delIndex = i
                            break
                if delIndex != -1:
                    if self.itemDict["Weapon"][delIndex].twoHanded == True and self.debugDualWield == False:
                        breakCheck = True
                    del self.itemDict["Weapon"][delIndex]
                if breakCheck:
                    break

            if wieldCount == 0:
                if blankCheck == True:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You're already holding something.", "Code":"3w1y28w1y"})
            elif wieldItem == "Multiple":
                if slotItem == None:
                    if blankCheck == True : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You hold some weapons in your hands.", "Code":"35w1y"})
                else:
                    if blankCheck == True : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You switch some weapons around.", "Code":"30w1y"})
            elif slotItem == None:
                countString = ""
                countCode = ""
                handsString = defaultGearSlot.lower()
                handsCode = str(len(defaultGearSlot)) + "w"
                if wieldCount == 2:
                    countString = " (2)"
                    countCode = "2r1w1r"
                    handsString = "hands"
                    handsCode = "5w"
                displayString = "You hold " + wieldItem.prefix.lower() + " " + wieldItem.name["String"] + countString + " in your " + handsString + "."
                displayCode = "9w" + str(len(wieldItem.prefix)) + "w1w" + wieldItem.name["Code"] + countCode + "9w" + handsCode + "1y"
                if blankCheck == True : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            else:
                slotString = "some gear"
                slotCode = "9w"
                slotCountString = ""
                slotCountCode = ""
                wieldString = "some gear"
                wieldCode = "9w"
                wieldCountString = ""
                wieldCountCode = ""
                if slotItem != "Multiple":
                    slotString = slotItem.prefix.lower() + " " + slotItem.name["String"]
                    slotCode = str(len(slotItem.prefix)) + "w1w" + slotItem.name["Code"]
                    if slotCount > 1:
                        slotCountString = " (2)"
                        slotCountCode = "2r1w1r"
                if wieldItem != "Multiple":
                    wieldString = wieldItem.prefix.lower() + " " + wieldItem.name["String"]
                    wieldCode = str(len(wieldItem.prefix)) + "w1w" + wieldItem.name["Code"]
                    if wieldCount > 1:
                        wieldCountString = " (2)"
                        wieldCountCode = "2r1w1r"
                displayString = "You remove " + slotString + slotCountString + " and wield " + wieldString + wieldCountString + "."
                displayCode = "11w" + slotCode + slotCountCode + "11w" + wieldCode + wieldCountCode + "1y"
                if blankCheck == True : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                           
    def removeCheck(self, console, targetItemKey, count, targetGearSlotIndex=None):
        removeItem = None
        if targetItemKey != "All":
            for gearSlot in self.gearDict:
                targetGearSlot = self.gearDict[gearSlot]
                slotRange = 1
                if targetGearSlotIndex == None and isinstance(targetGearSlot, list):
                    slotRange = len(targetGearSlot)
                for slotIndex in range(slotRange):
                    if isinstance(self.gearDict[gearSlot], list):
                        targetGearSlot = self.gearDict[gearSlot][slotIndex]
                    if targetGearSlot != None:
                        if targetItemKey in targetGearSlot.keyList:
                            removeItem = targetGearSlot
                            break
        
        if targetItemKey != "All" and removeItem == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

        else:
            removeCount = 0
            breakCheck = False
            removeItem = None
            for gearSlot in self.gearDict:
                slotRange = 1
                targetGearSlot = self.gearDict[gearSlot]
                if targetGearSlotIndex == None and isinstance(targetGearSlot, list):
                    slotRange = len(targetGearSlot)
                for slotIndex in range(slotRange):
                    if isinstance(self.gearDict[gearSlot], list):
                        if targetGearSlotIndex != None:
                            if targetGearSlotIndex >= len(self.gearDict[gearSlot]):
                                targetGearSlotIndex = len(self.gearDict[gearSlot]) - 1
                            slotIndex = targetGearSlotIndex
                        targetGearSlot = self.gearDict[gearSlot][slotIndex]
                    if targetGearSlot != None:
                        if targetItemKey == "All" or targetItemKey in targetGearSlot.keyList:
                            self.itemDict[targetGearSlot.pocket].append(targetGearSlot)
                            removeCount += 1
                            if removeItem != "Multiple":
                                if removeItem == None:
                                    removeItem = targetGearSlot
                                elif removeItem.num != targetGearSlot.num:
                                    removeItem = "Multiple"
                            if isinstance(self.gearDict[gearSlot], list):
                                self.gearDict[gearSlot][slotIndex] = None
                            else:
                                self.gearDict[gearSlot] = None

                            if count != "All" and removeCount >= count:
                                breakCheck = True
                                break
                if breakCheck:
                    break

            # Messages #
            if targetItemKey == "All" and count == "All":
                displayString = "You remove all of your gear."
                displayCode = "27w1y"
                if random.randrange(10) == 0:
                    displayString = "You strip down to your birthday suit."
                    displayCode = "36w1y"
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            elif removeItem == "Multiple":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You remove some gear.", "Code":"20w1y"})
            elif isinstance(removeItem, Item):
                countString = ""
                countCode = ""
                if removeCount > 1:
                    countString = " (" + str(removeCount) + ")"
                    countCode = "2r" + str(len(str(removeCount))) + "w1r"
                console.lineList.insert(0, {"Blank": True})
                displayString = "You remove " + removeItem.prefix + " " + removeItem.name["String"] + "." + countString
                displayCode = "11w" + str(len(removeItem.prefix)) + "w1w" + removeItem.name["Code"] + "1y" + countCode
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            
    def displayGear(self, console, galaxyList, currentRoom):
        gearSlotDisplayDict = {"Body Under":{"String":"(Under) Body", "Code":"1r5w2r4w"}, "Body Over":{"String":"(Over) Body", "Code":"1r4w2r4w"}, "Legs Under":{"String":"(Under) Legs", "Code":"1r5w2r4w"}, "Legs Over":{"String":"(Over) Legs", "Code":"1r4w2r4w"}, "Left Hand":{"String":"L-Hand", "Code":"1w1y4w"}, "Right Hand":{"String":"R-Hand", "Code":"1w1y4w"}}

        console.lineList.insert(0, {"Blank": True})
        console.lineList.insert(0, {"String":"Worn Gear", "Code":"1w4ddw1w3ddw"})
        console.lineList.insert(0, {"String":"--=====--", "Code":"1y1dy1y1dy1y1dy1y1dy1y"})
        for gearSlot in self.gearDict:
            gearSlotString = gearSlot
            if gearSlot in gearSlotDisplayDict and "String" in gearSlotDisplayDict[gearSlot]:
                gearSlotString = gearSlotDisplayDict[gearSlot]["String"]
            gearSlotCode = str(len(gearSlotString)) + "w"
            if gearSlot in gearSlotDisplayDict and "Code" in gearSlotDisplayDict[gearSlot]:
                gearSlotCode = gearSlotDisplayDict[gearSlot]["Code"]
            
            indent = 12 - len(gearSlotString)
            for i in range(indent):
                gearSlotString = " " + gearSlotString
                gearSlotCode = "1w" + gearSlotCode

            slotRange = 1
            if isinstance(self.gearDict[gearSlot], list):
                slotRange = len(self.gearDict[gearSlot])
            for slotIndex in range(slotRange):
                gearString = "(Nothing)"
                gearCode = "1r1w6ddw1r"
                modString = ""
                modCode = ""
                
                if isinstance(self.gearDict[gearSlot], list):
                    if self.gearDict[gearSlot][slotIndex] != None:
                        if "Glowing" in self.gearDict[gearSlot][slotIndex].flags and self.gearDict[gearSlot][slotIndex].flags["Glowing"] == True:
                            modString = " (Glowing)"
                            modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                        if currentRoom.isLit(galaxyList, self) == False:
                            gearString = "(Something)"
                            gearCode = "1r1w8wwd1r"
                        else:
                            gearString = self.gearDict[gearSlot][slotIndex].name["String"]
                            gearCode = str(len(gearString)) + "w"
                            if "Code" in self.gearDict[gearSlot][slotIndex].name:
                                gearCode = self.gearDict[gearSlot][slotIndex].name["Code"]
                else:
                    if self.gearDict[gearSlot] != None:
                        if "Glowing" in self.gearDict[gearSlot].flags and self.gearDict[gearSlot].flags["Glowing"] == True:
                            modString = " (Glowing)"
                            modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                        if currentRoom.isLit(galaxyList, self) == False:
                            gearString = "(Something)"
                            gearCode = "1r1w8wwd1r"
                        else:
                            gearString = self.gearDict[gearSlot].name["String"]
                            gearCode = str(len(gearString)) + "w"
                            if "Code" in self.gearDict[gearSlot].name:
                                gearCode = self.gearDict[gearSlot].name["Code"]
                console.lineList.insert(0, {"String":gearSlotString + ": " + gearString + modString, "Code":gearSlotCode + "2y" + gearCode + modCode})

    def boardCheck(self, console, galaxyList, currentRoom, targetSpaceshipKey):
        targetSpaceship = None
        for spaceship in currentRoom.spaceshipList:
            if targetSpaceshipKey in spaceship.keyList:
                targetSpaceship = spaceship
                break

        if self.spaceship != None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You are already inside.", "Code":"22w1y"})
        elif targetSpaceship == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You don't see it.", "Code":"7w1y8w1y"})
        elif targetSpaceship.hatchPassword != None and self.hasKey(targetSpaceship.hatchPassword) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You lack the proper key.", "Code":"23w1y"})
        
        else:
            self.spaceship = targetSpaceship.num
            self.area = targetSpaceship.hatchLocation[0]
            self.room = targetSpaceship.hatchLocation[1]

            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"The hatch opens and closes as you step inside.", "Code":"45w1y"})
            console.lineList.insert(0, {"Blank": True})

            spaceshipHatchRoom = targetSpaceship.areaList[self.area].roomList[self.room]
            spaceshipHatchRoom.display(console, galaxyList, self)

    # Utility Functions #
    def getTargetItem(self, targetItemKey):
        itemCheckList = []
        for pocket in self.itemDict:
            for item in self.itemDict[pocket]:
                itemCheckList.append(item)
        for gearSlot in self.gearDict:
            if isinstance(self.gearDict[gearSlot], list) == False:
                if self.gearDict[gearSlot] != None:
                    itemCheckList.append(self.gearDict[gearSlot])
            else:
                for gearSubSlot in self.gearDict[gearSlot]:
                    if gearSubSlot != None:
                        itemCheckList.append(gearSubSlot)

        for item in itemCheckList:
            if targetItemKey in item.keyList:
                return item
        return None

    def hasKey(self, password):
        for pocket in self.itemDict:
            for item in self.itemDict[pocket]:
                if "Password List" in item.flags:
                    for playerPassword in item.flags["Password List"]:
                        if playerPassword == password:
                            return True
        return False

    def lightInBagCheck(self, targetPocket):
        for item in self.itemDict[targetPocket]:
            if "Glowing" in item.flags and item.flags["Glowing"] == True:
                return True

        return False

    def getOppositeHand(self, targetHand):
        if targetHand == "Left Hand":
            return "Right Hand"
        else:
            return "Left Hand"

    def emote(self, console, input):
        if input in ["hmm", "hm"]:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You scratch your chin and go, 'Hmm..'", "Code":"28w3y3w3y"})
        elif input in "nod":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You nod your head in agreement.", "Code":"30w1y"})
        elif input == "nodnod":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You nodnod.", "Code":"10w1y"})
        elif input == "tap":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You tap your foot impatiently..", "Code":"29w2y"})
        elif input == "boggle":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You boggle in complete incomprehension.", "Code":"38w1y"})
        elif input == "jump":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You jump up and down.", "Code":"20w1y"})
        elif input == "ahah":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"Comprehension dawns upon you.", "Code":"28w1y"})
        