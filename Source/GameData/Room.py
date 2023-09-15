class Room:

    def __init__(self):
        self.name = {"String":"A Debug Room"}
        self.exit = {"North": None, "East": None, "South": None, "West": None}
        self.description = []

        self.itemList = []

    def display(self, console, galaxyList):

        # Name #
        console.lineList.insert(0, {"Blank": True})
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
                exitRoomString = "( " + spaceString + exitDir + " ) - " + exitRoom.name["String"]
                exitRoomNameCode = str(len(exitRoomString)) + "w"
                if "Code" in exitRoom.name:
                    exitRoomNameCode = exitRoom.name["Code"]
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
