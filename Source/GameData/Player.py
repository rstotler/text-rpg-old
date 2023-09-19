from GameData.Room import Room
from GameData.Item import Item

class Player:

    def __init__(self):
        self.spaceship = None
        self.galaxy = 0
        self.system = 0
        self.planet = 1
        self.area = 0
        self.room = 5

        self.itemDict = {"Armor": [], "Misc": []}
        self.gearDict = {"Head":None, "Face":None, "Neck":[None, None], "Body Under":None, "Body Over":None, "Hands":None, "Finger":[None, None], "Legs Under":None, "Legs Over":None, "Feet":None, "Left Hand":None, "Right Hand":None}
        self.maxWeight = 100.0

        self.maxLookDistance = 5

        self.emoteList = ["hmm", "hm", "nod", "nodnod", "tap"]

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
                    if len(currentRoom.exit[lookDir]) == 3:
                        currentSpaceship = galaxyList[self.galaxy].systemList[self.system].getSpaceship(self.spaceship)
                        if currentSpaceship != None:
                            currentRoom = currentSpaceship.areaList[currentRoom.exit[lookDir][1]].roomList[currentRoom.exit[lookDir][2]]
                        else:
                            currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
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
                    console.lineList.insert(0, {"String":"Your view is obstructed to the " + lookDir + "." + countString, "Code":"31w" + str(len(lookDir)) + "w1y" + countCode})
            if lookCheck:
                console.lineList.insert(0, {"Blank": True})
                currentRoom.display(console, galaxyList, self)
        
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
                    if len(targetRoomData) == 3:
                        targetSpaceship = galaxyList[self.galaxy].systemList[self.system].getSpaceship(self.spaceship)
                        if targetSpaceship != None:
                            targetRoom = targetSpaceship.areaList[targetRoomData[1]].roomList[targetRoomData[2]]
                    elif len(targetRoomData) == 5:
                        targetRoom = Room.exists(galaxyList, None, targetRoomData[0], targetRoomData[1], targetRoomData[2], targetRoomData[3], targetRoomData[4])
                    if targetRoom != None:
                        if len(targetRoomData) == 3:
                            self.area = targetRoomData[1]
                            self.room = targetRoomData[2]
                        else:
                            self.galaxy = targetRoomData[0]
                            self.system = targetRoomData[1]
                            self.planet = targetRoomData[2]
                            self.area = targetRoomData[3]
                            self.room = targetRoomData[4]
                            if self.spaceship != None:
                                self.spaceship = None

                        console.lineList.insert(0, {"Blank": True})
                        if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic":
                            console.lineList.insert(0, {"String": "The door opens and closes as you walk through.", "Code":"45w1y"})
                            console.lineList.insert(0, {"Blank": True})
                        targetRoom.display(console, galaxyList, self)

            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You can't go that way!", "Code":"7w1y13w1y"})

    def getCheck(self, console, galaxyList, targetItemKey, count):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        if currentRoom != None:
            getItem = None
            if targetItemKey != "All":
                for item in currentRoom.itemList:
                    if targetItemKey in item.keyList:
                        getItem = item
                        break

            if targetItemKey != "All" and getItem == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't see it.", "Code":"7w1y8w1y"})

            else:
                getCount = 0
                itemCount = len(currentRoom.itemList)
                targetCount = count
                if count == "All":
                    targetCount = len(currentRoom.itemList)

                noGetCheck = False
                tooMuchWeightCheck = False
                for i in range(targetCount):
                    delIndex = -1
                    for i, item in enumerate(currentRoom.itemList):
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

                                delIndex = i
                                break
                    if delIndex != -1:
                        del currentRoom.itemList[delIndex]

                if targetItemKey == "All" and count == "All":
                    if getCount == 0:
                        if noGetCheck == True:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick that up.", "Code":"7w1y14w1y"})
                        elif tooMuchWeightCheck == True:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't carry that much weight.", "Code":"7w1y24w1y"})
                        else:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick anything up.", "Code":"7w1y18w1y"})
                    else:
                        if getItem != "Multiple":
                            countString = ""
                            countCode = ""
                            if getCount > 1:
                                countString = " (" + str(getCount) + ")"
                                countCode = "2r" + str(len(str(getCount))) + "w1r"
                            getString = "You get " + getItem.prefix.lower() + " " + getItem.name["String"] + "." + countString
                            getCode = "8w" + str(len(getItem.prefix)) + "w1w" + getItem.name["Code"] + "1y" + countCode
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":getString, "Code":getCode})
                        elif getCount == itemCount:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You pick everything up.", "Code":"22w1y"})
                        else:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You get everything you can.", "Code":"26w1y"})

                else:
                    countString = ""
                    countCode = ""
                    if getCount == 0:
                        if noGetCheck == True:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick that up.", "Code":"7w1y14w1y"})
                        elif tooMuchWeightCheck == True:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't carry that much weight.", "Code":"7w1y24w1y"})
                        else:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick anything up.", "Code":"7w1y18w1y"})
                    elif getItem == "Multiple":
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You get everything you can.", "Code":"26w1y"})
                    else:
                        if getCount > 1:
                            countString = " (" + str(getCount) + ")"
                            countCode = "2r" + str(len(str(getCount))) + "w1r"
                        getString = "You get " + getItem.prefix.lower() + " " + getItem.name["String"] + "." + countString
                        getCode = "8w" + str(len(getItem.prefix)) + "w1w" + getItem.name["Code"] + "1y" + countCode
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":getString, "Code":getCode})

    def getCurrentWeight(self):
        currentWeight = 0.0
        for itemPocket in self.itemDict:
            for item in self.itemDict[itemPocket]:
                currentWeight += item.weight
        return currentWeight

    def dropCheck(self, console, galaxyList, targetItemKey, count):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        if currentRoom != None:
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
                
    def displayInventory(self, console, galaxyList, targetPocket):
        if targetPocket in self.itemDict:
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

            currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
            if currentRoom == None:
                currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
    
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

    def lightInBagCheck(self, targetPocket):
        for item in self.itemDict[targetPocket]:
            if "Glowing" in item.flags and item.flags["Glowing"] == True:
                return True

        return False

    def wearCheck(self, console, targetItemKey, count, targetGearSlotIndex=None):
        wearItem = None
        if targetItemKey != "All":
            for item in self.itemDict["Armor"]:
                if targetItemKey in item.keyList:
                    wearItem = item
                    break

        if targetItemKey != "All" and wearItem == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You remove all of your armor.", "Code":"28w1y"})
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
            
    def displayGear(self, console, galaxyList):
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
                currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
                if currentRoom == None:
                    currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
        
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

    def boardCheck(self, console, galaxyList, targetRoom, targetSpaceshipKey):
        targetSpaceship = None
        for spaceship in targetRoom.spaceshipList:
            if targetSpaceshipKey in spaceship.keyList:
                targetSpaceship = spaceship
                break

        if self.spaceship != None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You are already inside.", "Code":"22w1y"})
        elif targetSpaceship == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You don't see it.", "Code":"7w1y8w1y"})
        elif targetSpaceship.hatchStatus in ["Closed", "Locked"]:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"The hatch is closed.", "Code":"19w1y"})
        
        else:
            self.spaceship = spaceship.num
            self.area = spaceship.hatchLocation[0]
            self.room = spaceship.hatchLocation[1]

            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You step inside.", "Code":"15w1y"})
            console.lineList.insert(0, {"Blank": True})

            spaceshipHatchRoom = spaceship.areaList[self.area].roomList[self.room]
            spaceshipHatchRoom.display(console, galaxyList, self)

    def hasKey(self, password):
        for pocket in self.itemDict:
            for item in self.itemDict[pocket]:
                if "Password List" in item.flags:
                    for playerPassword in item.flags["Password List"]:
                        if playerPassword == password:
                            return True
        return False

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
        