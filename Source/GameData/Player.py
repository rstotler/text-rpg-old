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

    def moveCheck(self, console, galaxyList, targetDir):
        currentRoom = Room.exists(galaxyList, self.currentGalaxy, self.currentSystem, self.currentPlanet, self.currentArea, self.currentRoom)
        if currentRoom != None:
            if currentRoom.exit[targetDir] != None:
                targetRoomData = currentRoom.exit[targetDir]
                self.currentGalaxy = targetRoomData[0]
                self.currentSystem = targetRoomData[1]
                self.currentPlanet = targetRoomData[2]
                self.currentArea = targetRoomData[3]
                self.currentRoom = targetRoomData[4]

                targetRoom = Room.exists(galaxyList, targetRoomData[0], targetRoomData[1], targetRoomData[2], targetRoomData[3], targetRoomData[4])
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
