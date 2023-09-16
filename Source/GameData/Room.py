class Room:

    def __init__(self, galaxy, system, planet, area, room):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.area = area
        self.room = room

        self.name = {"String":"A Debug Room"}
        self.exit = {"North": None, "East": None, "South": None, "West": None}
        self.door = {"North": None, "East": None, "South": None, "West": None}
        self.description = []

        self.itemList = []

    def display(self, console, galaxyList):

        # Name #
        console.lineList.insert(0, self.name)
        underlineString = ""
        underlineCode = ""
        for i in range(len(self.name["String"])):
            underlineString = underlineString + "-"
            if i % 2 == 1:
                underlineCode = underlineCode + "1y"
            else:
                underlineCode = underlineCode + "1dy"
        console.lineList.insert(0, {"String":underlineString, "Code":underlineCode})

        # Description #
        for line in self.description:
            console.lineList.insert(0, line)

        # Exits #
        for exitDir in ["North", "East", "South", "West"]:
            spaceString = ""
            if exitDir in ["East", "West"]:
                spaceString = " "
            if self.exit[exitDir] != None:
                exitRoom = Room.exists(galaxyList, self.exit[exitDir][0], self.exit[exitDir][1], self.exit[exitDir][2], self.exit[exitDir][3], self.exit[exitDir][4])
                if exitRoom == None:
                    exitRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                
                if self.door[exitDir] != None and self.door[exitDir]["Status"] in ["Closed", "Locked"]:
                    exitRoomString = "( " + spaceString + exitDir + " ) - [Closed]"
                    exitRoomCode = "2r5w2r3y1r6w1r"
                else:
                    exitRoomString = "( " + spaceString + exitDir + " ) - " + exitRoom.name["String"]
                
                exitRoomNameCode = str(len(exitRoomString)) + "w"
                if "Code" in exitRoom.name:
                    exitRoomNameCode = exitRoom.name["Code"]
                
                if self.door[exitDir] == None or self.door[exitDir]["Status"] == "Open":
                    if exitDir in ["East", "West"]:
                        exitRoomCode = "3r" + str(len(exitDir)) + "w2r3y" + exitRoomNameCode
                    else:
                        exitRoomCode = "2r" + str(len(exitDir)) + "w2r3y" + exitRoomNameCode
                console.lineList.insert(0, {"String":exitRoomString, "Code":exitRoomCode})
            else:
                if exitDir in ["East", "West"]:
                    exitRoomCode = "3r" + str(len(exitDir)) + "w2r3y2r7w2r"
                else:
                    exitRoomCode = "2r" + str(len(exitDir)) + "w2r3y2r7w2r"
                console.lineList.insert(0, {"String":"( " + spaceString + exitDir + " ) - ( Nothing )", "Code":exitRoomCode})

        # Items #
        itemDisplayDict = {}
        for item in self.itemList:
            if item.num not in itemDisplayDict:
                itemDisplayDict[item.num] = {"Count":1, "ItemData":item}
            else:
                itemDisplayDict[item.num]["Count"] += 1
        for item in self.itemList:
            if item.num in itemDisplayDict:
                countString = ""
                countCode = ""
                if itemDisplayDict[item.num]["Count"] > 1:
                    countString = " (" + str(itemDisplayDict[item.num]["Count"]) + ")"
                    countCode = "2r" + str(len(str(itemDisplayDict[item.num]["Count"]))) + "w1r"
                
                itemDisplayString = itemDisplayDict[item.num]["ItemData"].prefix + " " + itemDisplayDict[item.num]["ItemData"].name["String"] + " " + itemDisplayDict[item.num]["ItemData"].roomDescription["String"] + countString
                itemDisplayCode = str(len(itemDisplayDict[item.num]["ItemData"].prefix)) + "w1w" + itemDisplayDict[item.num]["ItemData"].name["Code"] + "1w" + itemDisplayDict[item.num]["ItemData"].roomDescription["Code"] + countCode
                console.lineList.insert(0, {"String":itemDisplayString, "Code":itemDisplayCode})
                del itemDisplayDict[item.num]

    def installDoor(self, galaxyList, targetDir, doorType, password, status="Closed"):
        self.door[targetDir] = {"Type": doorType, "Status": status}
        if password != None:
            self.door[targetDir]["Password"] = password

        if self.exit[targetDir] != None:
            otherRoom = Room.exists(galaxyList, self.exit[targetDir][0], self.exit[targetDir][1], self.exit[targetDir][2], self.exit[targetDir][3], self.exit[targetDir][4])
            if otherRoom != None:
                otherRoomExitDir = None
                for exitDir in otherRoom.exit:
                    exitData = otherRoom.exit[exitDir]
                    if exitData != None and exitData[0] == self.galaxy and exitData[1] == self.system and exitData[2] == self.planet and exitData[3] == self.area and exitData[4] == self.room:
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
            self.door[targetDir]["Status"] = targetAction

            if self.exit[targetDir] != None:
                otherRoom = Room.exists(galaxyList, self.exit[targetDir][0], self.exit[targetDir][1], self.exit[targetDir][2], self.exit[targetDir][3], self.exit[targetDir][4])
                if otherRoom != None:
                    otherRoomExitDir = None
                    for exitDir in otherRoom.exit:
                        exitData = otherRoom.exit[exitDir]
                        if exitData != None and exitData[0] == self.galaxy and exitData[1] == self.system and exitData[2] == self.planet and exitData[3] == self.area and exitData[4] == self.room:
                            otherRoomExitDir = exitDir
                            break

                    if otherRoomExitDir != None:
                        otherRoom.door[otherRoomExitDir]["Status"] = targetAction

    def openCloseDoorCheck(self, console, galaxyList, targetAction, targetDir):
        targetDoorAction = targetAction
        if targetAction == "Close":
            targetDoorAction = "Closed"

        if self.door[targetDir] == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"There is no door in that direction.", "Code":"34w1y"})
        elif self.door[targetDir]["Type"] == "Automatic":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door is automatic.", "Code":"22w1y"})
        elif self.door[targetDir]["Status"] == targetDoorAction or (targetDoorAction == "Closed" and self.door[targetDir]["Status"] == "Locked"):
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"It's already " + targetDoorAction.lower() + ".", "Code":"2w1y10w" + str(len(targetDoorAction)) + "w1y"})
        elif targetDoorAction == "Open" and self.door[targetDir]["Status"] == "Locked":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"It's locked.", "Code":"2w1y8w1y"})
        
        else:
            self.door[targetDir]["Status"] = targetDoorAction

            if self.exit[targetDir] != None:
                otherRoom = Room.exists(galaxyList, self.exit[targetDir][0], self.exit[targetDir][1], self.exit[targetDir][2], self.exit[targetDir][3], self.exit[targetDir][4])
                if otherRoom != None:
                    otherRoomExitDir = None
                    for exitDir in otherRoom.exit:
                        exitData = otherRoom.exit[exitDir]
                        if exitData != None and exitData[0] == self.galaxy and exitData[1] == self.system and exitData[2] == self.planet and exitData[3] == self.area and exitData[4] == self.room:
                            otherRoomExitDir = exitDir
                            break

                    if otherRoomExitDir != None:
                        otherRoom.door[otherRoomExitDir]["Status"] = targetDoorAction
                    
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You " + targetAction.lower() + " the door to the " + targetDir + ".", "Code":"4w" + str(len(targetAction)) + "w17w" + str(len(targetDir)) + "w1y"})

    def lockUnlockDoorCheck(self, console, galaxyList, player, targetAction, targetDir):
        if targetAction == "Lock":
            targetActionStatus = "Locked"
        else:
            targetActionStatus = "Closed"

        if self.door[targetDir] == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"There is no door in that direction.", "Code":"34w1y"})
        elif "Password" not in self.door[targetDir]:
            haveString = "require a key"
            if targetAction == "Lock":
                haveString = "have a lock"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door doesn't " + haveString + ".", "Code":"15w1y2w" + str(len(haveString)) + "w1y"})
        elif self.door[targetDir]["Type"] == "Automatic":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door " + targetAction.lower() + "s automatically.", "Code":"10w" + str(len(targetAction)) + "w15w1y"})
        elif self.door[targetDir]["Status"] == targetActionStatus:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"It's already " + targetAction.lower() + "ed.", "Code":"2w1y10w" + str(len(targetAction)) + "w2w1y"})
        elif player.hasKey(self.door[targetDir]["Password"]) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You lack the key.", "Code":"16w1y"})
        
        else:
            self.door[targetDir]["Status"] = targetActionStatus

            if self.exit[targetDir] != None:
                otherRoom = Room.exists(galaxyList, self.exit[targetDir][0], self.exit[targetDir][1], self.exit[targetDir][2], self.exit[targetDir][3], self.exit[targetDir][4])
                if otherRoom != None:
                    otherRoomExitDir = None
                    for exitDir in otherRoom.exit:
                        exitData = otherRoom.exit[exitDir]
                        if exitData != None and exitData[0] == self.galaxy and exitData[1] == self.system and exitData[2] == self.planet and exitData[3] == self.area and exitData[4] == self.room:
                            otherRoomExitDir = exitDir
                            break

                    if otherRoomExitDir != None:
                        otherRoom.door[otherRoomExitDir]["Status"] = targetActionStatus
                    
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You " + targetAction.lower() + " the door to the " + targetDir + ".", "Code":"4w" + str(len(targetAction)) + "w17w" + str(len(targetDir)) + "w1y"})

    @staticmethod
    def exists(galaxyList, targetGalaxy, targetSystem, targetPlanet, targetArea, targetRoom):
        if targetGalaxy <= len(galaxyList) - 1 and \
        targetSystem <= len(galaxyList[targetGalaxy].systemList) - 1 and \
        targetPlanet <= len(galaxyList[targetGalaxy].systemList[targetSystem].planetList) - 1 and \
        targetArea <= len(galaxyList[targetGalaxy].systemList[targetSystem].planetList[targetPlanet].areaList) - 1 and \
        targetRoom <= len(galaxyList[targetGalaxy].systemList[targetSystem].planetList[targetPlanet].areaList[targetArea].roomList) -1:
            return galaxyList[targetGalaxy].systemList[targetSystem].planetList[targetPlanet].areaList[targetArea].roomList[targetRoom]
        else:
            return None
