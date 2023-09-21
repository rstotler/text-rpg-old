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
            for spaceship in self.spaceshipList:
                displayString = "A " + spaceship.name["String"] + " is sitting on the launch pad."
                displayCode = "2w" + spaceship.name["Code"] + "29w1y"
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            
        # Items #
        itemDisplayDict = {}
        totalCount = 0
        for item in self.itemList:
            if item.num not in itemDisplayDict:
                itemDisplayDict[item.num] = {"Count":1, "ItemData":item}
                totalCount += 1
            else:
                itemDisplayDict[item.num]["Count"] += 1
                totalCount += 1
        
        if roomIsLit == False and totalCount > 0:
            countString = ""
            countCode = ""
            if totalCount > 1:
                countString = " (" + str(totalCount) + ")"
                countCode = "2r" + str(len(str(totalCount))) + "w1r"
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
