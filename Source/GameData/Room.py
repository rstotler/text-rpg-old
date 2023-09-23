import copy

class Room:

    def __init__(self, galaxy, system, planet, area, room):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.area = area
        self.room = room
        self.spaceshipObject = None

        self.name = {"String":"A Debug Room"}
        self.description = []
        self.exit = {"North": None, "East": None, "South": None, "West": None}
        self.door = {"North": None, "East": None, "South": None, "West": None}

        self.mobList = []
        self.itemList = []
        self.spaceshipList = []

        self.inside = False

    def display(self, console, galaxyList, player):
        roomIsLit = self.isLit(galaxyList, player)

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
        console.lineList.insert(0, {"String":nameString, "Code":nameCode})

        # Underline #
        underlineString = ""
        underlineCode = ""
        for i in range(len(nameString)):
            underlineChar = "-"
            indentCount = int(len(nameString) * .15)
            if indentCount <= 0:
                indentCount = 1
            if i not in range(0, indentCount) and i not in range(len(nameString) - indentCount, len(nameString)):
                underlineChar = "="
            underlineString = underlineString + underlineChar
            if i % 2 == 1:
                underlineCode = underlineCode + "1y"
            else:
                underlineCode = underlineCode + "1dy"
        console.lineList.insert(0, {"String":underlineString, "Code":underlineCode})

        # Description #
        if roomIsLit == False:
            console.lineList.insert(0, {"String":"It's too dark to see..", "Code":"2w1y17w2y"})
        else:
            for line in self.description:
                console.lineList.insert(0, line)

        # Exits #
        otherRoomSpaceshipNum = None
        for exitDir in ["North", "East", "South", "West"]:
            spaceString = ""
            if exitDir in ["East", "West"]:
                spaceString = " "
            if self.exit[exitDir] != None:
                exitRoom = None
                if len(self.exit[exitDir]) == 5:
                    exitRoom = Room.exists(galaxyList, None, self.exit[exitDir][0], self.exit[exitDir][1], self.exit[exitDir][2], self.exit[exitDir][3], self.exit[exitDir][4])
                elif len(self.exit[exitDir]) == 3 and self.spaceshipObject != None:
                    exitRoom = self.spaceshipObject.getRoom(self.exit[exitDir][1], self.exit[exitDir][2])
                elif self.exit[exitDir] == "Spaceship Exit" and self.spaceshipObject.landedLocation != None:
                    exitRoom = Room.exists(galaxyList, None, self.spaceshipObject.landedLocation[0], self.spaceshipObject.landedLocation[1], self.spaceshipObject.landedLocation[2], self.spaceshipObject.landedLocation[3], self.spaceshipObject.landedLocation[4])
                if exitRoom == None:
                    exitRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                
                if roomIsLit == False and exitRoom.isLit(galaxyList, player) == False:
                    exitRoomString = "( " + spaceString + exitDir + " ) - ( Black )"
                    exitRoomCode = "2r1w4ddw2r3y2r1dw1a2da1dda2r"
                elif self.door[exitDir] != None and self.door[exitDir]["Status"] in ["Closed", "Locked"]:
                    exitRoomString = "( " + spaceString + exitDir + " ) - [Closed]"
                    exitRoomCode = "2r1w4ddw2r3y1r6w1r"
                else:
                    exitRoomString = "( " + spaceString + exitDir + " ) - " + exitRoom.name["String"]
                
                if roomIsLit == False and exitRoom.isLit(galaxyList, player) == False:
                    exitRoomNameCode = "2r1dw1a2da1dda2r"
                else:
                    exitRoomNameCode = str(len(exitRoomString)) + "w"
                    if "Code" in exitRoom.name:
                        exitRoomNameCode = exitRoom.name["Code"]
                
                if self.door[exitDir] == None or self.door[exitDir]["Status"] == "Open":
                    if exitDir in ["East", "West"]:
                        exitRoomCode = "3r1w" + str(len(exitDir) - 1) + "ddw2r3y" + exitRoomNameCode
                    else:
                        exitRoomCode = "2r1w" + str(len(exitDir) - 1) + "ddw2r3y" + exitRoomNameCode
                console.lineList.insert(0, {"String":exitRoomString, "Code":exitRoomCode})
            else:
                if exitDir in ["East", "West"]:
                    exitRoomCode = "3r1w" + str(len(exitDir) - 1) + "ddw2r3y2r1w6ddw2r"
                else:
                    exitRoomCode = "2r1w" + str(len(exitDir) - 1) + "ddw2r3y2r1w6ddw2r"
                
                if roomIsLit == False:
                    exitRoomCode = exitRoomCode[0:-8] + "1dw1a2da1dda2r"
                    console.lineList.insert(0, {"String":"( " + spaceString + exitDir + " ) - ( Black )", "Code":exitRoomCode})
                else:
                    console.lineList.insert(0, {"String":"( " + spaceString + exitDir + " ) - ( Nothing )", "Code":exitRoomCode})

        # Spaceships #
        if len(self.spaceshipList) > 0:
            if roomIsLit == False:
                displayString = "A spaceship is sitting on the launch pad."
                displayCode = "40w1y"
                countString = ""
                countCode = ""
                if len(self.spaceshipList) > 1:
                    countString = " (" + str(len(self.spaceshipList)) + ")"
                    countCode = "2r" + str(len(str(len(self.spaceshipList)))) + "w1r"
                console.lineList.insert(0, {"String":displayString + countString, "Code":displayCode + countCode})
            else:
                for spaceship in self.spaceshipList:
                    displayString = "A " + spaceship.name["String"] + " is sitting on the launch pad."
                    displayCode = "2w" + spaceship.name["Code"] + "29w1y"
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            
        # Mobs #
        if True:
            mobDisplayDict = {}
            totalMobCount = 0
            for mob in self.mobList:
                if mob.num not in mobDisplayDict:
                    mobDisplayDict[mob.num] = {"Count":1, "MobData":mob}
                    totalMobCount += 1
                else:
                    mobDisplayDict[mob.num]["Count"] += 1
                    totalMobCount += 1
                if mob in player.targetList:
                    mobDisplayDict[mob.num]["Target Check"] = True

            if roomIsLit == False and totalMobCount > 0:
                countString = ""
                countCode = ""
                if totalMobCount > 1:
                    countString = " (" + str(totalMobCount) + ")"
                    countCode = "2r" + str(len(str(totalMobCount))) + "w1r"
                console.lineList.insert(0, {"String":"There is someone here." + countString, "Code":"21w1y" + countCode})

            else:
                for mob in self.mobList:
                    if mob.num in mobDisplayDict:
                        targetString = ""
                        targetCode = ""
                        if "Target Check" in mobDisplayDict[mob.num] and mobDisplayDict[mob.num]["Target Check"] == True:
                            targetString = "[+]"
                            targetCode = "3m"
                        countString = ""
                        countCode = ""
                        if mobDisplayDict[mob.num]["Count"] > 1:
                            countString = " (" + str(mobDisplayDict[mob.num]["Count"]) + ")"
                            countCode = "2r" + str(len(str(mobDisplayDict[mob.num]["Count"]))) + "w1r"

                        mobDisplayString = targetString + mobDisplayDict[mob.num]["MobData"].prefix + " " + mobDisplayDict[mob.num]["MobData"].name["String"] + " " + mobDisplayDict[mob.num]["MobData"].roomDescription["String"] + countString
                        mobDisplayCode = targetCode + str(len(mobDisplayDict[mob.num]["MobData"].prefix)) + "w1w" + mobDisplayDict[mob.num]["MobData"].name["Code"] + "1w" + mobDisplayDict[mob.num]["MobData"].roomDescription["Code"] + countCode
                        console.lineList.insert(0, {"String":mobDisplayString, "Code":mobDisplayCode})
                        del mobDisplayDict[mob.num]

        # Items #
        if True:
            itemDisplayDict = {}
            totalItemCount = 0
            for item in self.itemList:
                if item.num not in itemDisplayDict:
                    itemDisplayDict[item.num] = {"Count":1, "ItemData":item}
                    totalItemCount += 1
                else:
                    itemDisplayDict[item.num]["Count"] += 1
                    totalItemCount += 1
            
            if roomIsLit == False and totalItemCount > 0:
                countString = ""
                countCode = ""
                if totalItemCount > 1:
                    countString = " (" + str(totalItemCount) + ")"
                    countCode = "2r" + str(len(str(totalItemCount))) + "w1r"
                console.lineList.insert(0, {"String":"There is something on the ground." + countString, "Code":"32w1y" + countCode})
                        
            else:
                for item in self.itemList:
                    if item.num in itemDisplayDict:
                        modString = ""
                        modCode = ""
                        if "Glowing" in item.flags and item.flags["Glowing"] == True:
                            modString = " (Glowing)"
                            modCode = "2y1w1dw1ddw1w2dw1ddw1y"

                        countString = ""
                        countCode = ""
                        if itemDisplayDict[item.num]["Count"] > 1:
                            countString = " (" + str(itemDisplayDict[item.num]["Count"]) + ")"
                            countCode = "2r" + str(len(str(itemDisplayDict[item.num]["Count"]))) + "w1r"

                        itemDisplayString = itemDisplayDict[item.num]["ItemData"].prefix + " " + itemDisplayDict[item.num]["ItemData"].name["String"] + " " + itemDisplayDict[item.num]["ItemData"].roomDescription["String"] + modString + countString
                        itemDisplayCode = str(len(itemDisplayDict[item.num]["ItemData"].prefix)) + "w1w" + itemDisplayDict[item.num]["ItemData"].name["Code"] + "1w" + itemDisplayDict[item.num]["ItemData"].roomDescription["Code"] + modCode + countCode
                        console.lineList.insert(0, {"String":itemDisplayString, "Code":itemDisplayCode})
                        del itemDisplayDict[item.num]

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

                        if otherRoomExitDir != None:
                            otherRoom.door[otherRoomExitDir]["Status"] = targetAction

    def sameRoomCheck(self, target):
        if isinstance(target, list):
            if len(target) == 3 and self.spaceshipObject != None:
                if target[0] == self.spaceshipObject.num and target[1] == self.area and target[2] == self.room:
                    return True
            elif len(target) == 5:
                if target[0] == self.galaxy and target[1] == self.system and target[2] == self.planet and target[3] == self.area and target[4] == self.room:
                    return True

        elif target.spaceship == None and self.spaceshipObject == None:
            if target.galaxy == self.galaxy and target.system == self.system and target.planet == self.planet and target.area == self.area and target.room == self.room:
                return True
        elif target.spaceship != None and self.spaceshipObject != None:
            if target.spaceship == self.spaceshipObject.num and target.area == self.area and target.room == self.room:
                return True

        return False
    
    def isLit(self, galaxyList, player):
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

        if self.sameRoomCheck(player):
            for gearSlot in player.gearDict:
                if isinstance(player.gearDict[gearSlot], list):
                    for gearSubSlot in player.gearDict[gearSlot]:
                        if gearSubSlot != None:
                            if "Glowing" in gearSubSlot.flags and gearSubSlot.flags["Glowing"] == True:
                                return True
                else:
                    if player.gearDict[gearSlot] != None:
                        item = player.gearDict[gearSlot]
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
                if targetObjectKey in tempObject.keyList:
                    return tempObject
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
    def getTargetRoomFromStartRoom(galaxyList, currentArea, currentRoom, targetDir, targetRoomDistance):
        for rNum in range(targetRoomDistance):
            if currentRoom.exit[targetDir] == None:
                break
            else:
                targetExit = currentRoom.exit[targetDir]
                
                # Spaceship Exit #
                if targetExit == "Spaceship Exit" and currentRoom.spaceshipObject != None and currentRoom.spaceshipObject.landedLocation != None:
                    landedLocation = currentRoom.spaceshipObject.landedLocation
                    if Room.exists(galaxyList, None, landedLocation[0], landedLocation[1], landedLocation[2], landedLocation[3], landedLocation[4]) != None:
                        currentRoom = Room.exists(galaxyList, None, landedLocation[0], landedLocation[1], landedLocation[2], landedLocation[3], landedLocation[4])
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
                        
        return currentArea, currentRoom

    @staticmethod
    def getSurroundingRoomData(galaxyList, startArea, startRoom, targetRange):
        oppositeDir = {"North":"South", "East":"West", "South":"North", "West":"East"}
        def examineRoomData(targetArea, targetRoom, targetRange, targetDir, examinedAreaList, examinedRoomList, viewLoc):
            spaceshipNum = targetRoom.spaceshipObject
            if spaceshipNum != None:
                spaceshipNum = spaceshipNum.num
            if {"Galaxy":targetRoom.galaxy, "System":targetRoom.system, "Planet":targetRoom.planet, "Area":targetRoom.area, "Spaceship":spaceshipNum} not in examinedAreaList:
                examinedAreaList.append({"Galaxy":targetRoom.galaxy, "System":targetRoom.system, "Planet":targetRoom.planet, "Area":targetRoom.area, "Spaceship":spaceshipNum})
            examinedRoomList.append({"Galaxy":targetRoom.galaxy, "System":targetRoom.system, "Planet":targetRoom.planet, "Area":targetRoom.area, "Room":targetRoom.room, "Spaceship":spaceshipNum})

            if viewLoc[0] + viewLoc[1] < targetRange:
                firstLoc = copy.deepcopy(viewLoc)
                exitDirList = ["North", "East", "South", "West"]
                if targetDir != None and oppositeDir[targetDir] in exitDirList:
                    del exitDirList[exitDirList.index(oppositeDir[targetDir])]
                for targetExitDir in exitDirList:
                    if targetExitDir != "North":
                        viewLoc = copy.deepcopy(firstLoc)
                    if targetExitDir in targetRoom.exit:
                        nextArea, nextRoom = Room.getTargetRoomFromStartRoom(galaxyList, targetArea, targetRoom, targetExitDir, 1)
                        if targetExitDir in ["East", "West"] : viewLoc[0] += 1
                        elif targetExitDir in ["North", "South"] : viewLoc[1] += 1

                        spaceshipNum = nextRoom.spaceshipObject
                        if spaceshipNum != None:
                            spaceshipNum = spaceshipNum.num
                        if {"Galaxy":nextRoom.galaxy, "System":nextRoom.system, "Planet":nextRoom.planet, "Area":nextRoom.area, "Room":nextRoom.room, "Spaceship":spaceshipNum} not in examinedRoomList:
                            examinedAreaList, examinedRoomList = examineRoomData(nextArea, nextRoom, targetRange, targetExitDir, examinedAreaList, examinedRoomList, viewLoc)

            return examinedAreaList, examinedRoomList
        return examineRoomData(startArea, startRoom, targetRange, None, [], [], [0, 0])
