from GameData.Room import Room

class Player:

    def __init__(self):
        self.currentGalaxy = 0
        self.currentSystem = 0
        self.currentPlanet = 0
        self.currentArea = 0
        self.currentRoom = 1

        self.itemDict = {"Armor": [], "Misc": []}
        self.maxWeight = 100.0

        self.maxLookDistance = 5

    def lookDirection(self, console, galaxyList, lookDir, count):
        currentRoom = Room.exists(galaxyList, self.currentGalaxy, self.currentSystem, self.currentPlanet, self.currentArea, self.currentRoom)
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
                    currentRoom = Room.exists(galaxyList, currentRoom.exit[lookDir][0], currentRoom.exit[lookDir][1], currentRoom.exit[lookDir][2], currentRoom.exit[lookDir][3], currentRoom.exit[lookDir][4])
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
                    console.lineList.insert(0, {"String": "You can't see any farther to the " + lookDir + "." + countString, "Code":"7w1y25w" + str(len(lookDir)) + "w1y" + countCode})
                elif messageType == "View Obstructed":
                    console.lineList.insert(0, {"String": "Your view is obstructed to the " + lookDir + "." + countString, "Code":"31w" + str(len(lookDir)) + "w1y" + countCode})
            if lookCheck:
                console.lineList.insert(0, {"Blank": True})
                currentRoom.display(console, galaxyList)
        
    def moveCheck(self, console, galaxyList, targetDir):
        currentRoom = Room.exists(galaxyList, self.currentGalaxy, self.currentSystem, self.currentPlanet, self.currentArea, self.currentRoom)
        if currentRoom != None:
            if currentRoom.exit[targetDir] != None:
                if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Manual" and currentRoom.door[targetDir]["Status"] in ["Closed", "Locked"]:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String": "The door is closed.", "Code":"18w1y"})
                elif currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic" and currentRoom.door[targetDir]["Status"] == "Locked" and "Password" in currentRoom.door[targetDir] and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String": "This door requires a key to pass through.", "Code":"40w1y"})

                else:
                    targetRoomData = currentRoom.exit[targetDir]
                    targetRoom = Room.exists(galaxyList, targetRoomData[0], targetRoomData[1], targetRoomData[2], targetRoomData[3], targetRoomData[4])
                    if targetRoom != None:
                        self.currentGalaxy = targetRoomData[0]
                        self.currentSystem = targetRoomData[1]
                        self.currentPlanet = targetRoomData[2]
                        self.currentArea = targetRoomData[3]
                        self.currentRoom = targetRoomData[4]

                        console.lineList.insert(0, {"Blank": True})
                        if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic":
                            console.lineList.insert(0, {"String": "The door opens and closes as you walk through.", "Code":"45w1y"})
                            console.lineList.insert(0, {"Blank": True})
                        targetRoom.display(console, galaxyList)

            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You can't go that way!", "Code":"7w1y13w1y"})

    def getCheck(self, console, galaxyList, targetItemKey, count):
        currentRoom = Room.exists(galaxyList, self.currentGalaxy, self.currentSystem, self.currentPlanet, self.currentArea, self.currentRoom)
        if currentRoom != None:
            getItemKey = ""
            breakCheck = False
            if targetItemKey != "All":
                for item in currentRoom.itemList:
                    for guessKey in targetItemKey.split():
                        if guessKey in item.keyList:
                            getItemKey = guessKey
                            breakCheck = True
                            break
                    if breakCheck:
                        break

            if targetItemKey != "All" and getItemKey == "":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't see it.", "Code":"7w1y8w1y"})

            else:
                getCount = 0
                targetCount = count
                if count == "All":
                    targetCount = len(currentRoom.itemList)

                getItem = None
                noGetCheck = False
                for i in range(targetCount):
                    delIndex = -1
                    for i, item in enumerate(currentRoom.itemList):
                        if self.getCurrentWeight() + item.weight <= self.maxWeight:
                            if targetItemKey == "All" or getItemKey in item.keyList:
                                if "No Get" in item.flags:
                                    noGetCheck = True
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
                        else:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick anything up.", "Code":"7w1y18w1y"})
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
        currentRoom = Room.exists(galaxyList, self.currentGalaxy, self.currentSystem, self.currentPlanet, self.currentArea, self.currentRoom)
        if currentRoom != None:
            dropItemKey = ""
            breakCheck = False
            if targetItemKey != "All":
                for pocket in self.itemDict:
                    for item in self.itemDict[pocket]:
                        for guessKey in targetItemKey.split():
                            if guessKey in item.keyList:
                                dropItemKey = guessKey
                                breakCheck = True
                                break
                        if breakCheck:
                            break
                    if breakCheck:
                        break

            if targetItemKey != "All" and dropItemKey == "":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

            else:
                dropCount = 0
                dropItem = None
                delDict = {}
                breakCheck = False
                for pocket in self.itemDict:
                    delDict[pocket] = []
                    for i, item in enumerate(self.itemDict[pocket]):
                        if targetItemKey == "All" or dropItemKey in item.keyList:
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

                for pocket in delDict:
                    delDict[pocket].reverse()
                    for i in delDict[pocket]:
                        del self.itemDict[pocket][i]

                if dropCount == 0:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You aren't carrying anything.", "Code":"8w1y19w1y"})
                elif dropItem == "Multiple":
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You drop everything you can.", "Code":"27w1y"})
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
                
    def displayInventory(self, console, targetPocket):
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
                underlineString = underlineString + "-"
                if i % 2 == 1:
                    underlineCode = underlineCode + "1y"
                else:
                    underlineCode = underlineCode + "1dy"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": targetPocketDisplayString + " Bag", "Code": targetPocketDisplayCode + "4w"})
            console.lineList.insert(0, {"String": underlineString, "Code": underlineCode})

            if len(self.itemDict[targetPocket]) == 0:
                console.lineList.insert(0, {"String": "-Empty", "Code": "1y5w"})

            else:
                for item in self.itemDict[targetPocket]:
                    if item.num in displayDict:
                        countString = ""
                        countCode = ""
                        if displayDict[item.num]["Count"] > 1:
                            countString = " (" + str(displayDict[item.num]["Count"]) + ")"
                            countCode = "2r" + str(len(str(displayDict[item.num]["Count"]))) + "w1r"
                        itemDisplayString = item.prefix + " " + item.name["String"] + countString
                        itemDisplayCode = str(len(item.prefix)) + "w1w" + item.name["Code"] + countCode
                        console.lineList.insert(0, {"String":itemDisplayString, "Code":itemDisplayCode})
                        del displayDict[item.num]

    def hasKey(self, password):
        for pocket in self.itemDict:
            for item in self.itemDict[pocket]:
                if "Password List" in item.flags:
                    for playerPassword in item.flags["Password List"]:
                        if playerPassword == password:
                            return True
        return False
