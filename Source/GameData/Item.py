class Item:

    def __init__(self, num):
        self.num = num
        self.flags = {}

        self.prefix = "A"
        self.name = {"String":"Debug Item"}
        self.roomDescription = {"String":"is laying on the ground.", "Code":"23w1y"}
        self.keyList = []

        self.weight = 1.0
        self.pocket = "Misc"
        self.gearSlot = None

        self.containerList = None
        self.containerPassword = None

        self.loadItem(num)

    def loadItem(self, num):
        
        # Armor #
        if self.name["String"] == "Debug Item":
            if num == 1:
                self.prefix = "An"
                self.name = {"String":"Iron Helmet", "Code":"1a1da1dda1ddda1w1ddda1dda1da1a1da1dda"}
                self.pocket = "Armor"
                self.gearSlot = "Head"
            elif num == 2:
                self.prefix = "An"
                self.name = {"String":"Ancient Mask", "Code":"1y1dy1ddy1dddy1ddy1dy1y1w1y1dy1ddy1dddy"}
                self.pocket = "Armor"
                self.gearSlot = "Face"
            elif num == 3:
                self.name = {"String":"Heart Locket", "Code":"1lr1r1dr1lr1r1w1y1dy1ddy1y1dy1ddy"}
                self.pocket = "Armor"
                self.gearSlot = "Neck"
            elif num == 4:
                self.name = {"String":"Star Pendant", "Code":"1y1dy1ddy1dddy1w1y1dy1ddy1dddy1ddy1dy1y"}
                self.pocket = "Armor"
                self.gearSlot = "Neck"
            elif num == 5:
                self.name = {"String":"Fuzzy Sweater", "Code":"1r1g1do1dr1ddg1w1da6dda"}
                self.pocket = "Armor"
                self.gearSlot = "Body Under"
            elif num == 6:
                self.name = {"String":"Breastplate", "Code":"1ddda1dda1da1a1da1dda1ddda1dda1da1a1da"}
                self.pocket = "Armor"
                self.gearSlot = "Body Over"
            elif num == 7:
                self.prefix = "A pair of"
                self.name = {"String":"Leather Gloves", "Code":"1ddo6dddo1w1ddo5dddo"}
                self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
                self.pocket = "Armor"
                self.gearSlot = "Hands"
            elif num == 8:
                self.name = {"String":"Ruby Ring", "Code":"1lr1r1dr1ddr1w1ly1y1dy1ddy"}
                self.roomDescription = {"String":"has been dropped on the ground.", "Code":"30w1y"}
                self.pocket = "Armor"
                self.gearSlot = "Finger"
                self.flags["Glowing"] = True
            elif num == 9:
                self.prefix = "An"
                self.name = {"String":"Emerald Ring", "Code":"1g1dg1ddg1dddg1ddg1dg1g1w1ly1y1dy1ddy"}
                self.pocket = "Armor"
                self.gearSlot = "Finger"
            elif num == 10:
                self.name = {"String":"Gold Ring", "Code":"1ly1y1dy1ddy1w1ly1y1dy1ddy"}
                self.pocket = "Armor"
                self.gearSlot = "Finger"
            elif num == 11:
                self.prefix = "A pair of"
                self.name = {"String":"Swimming Trunks", "Code":"1dr1ddr1dddr1ddr1dddr1ddr1dddr1ddr1w1dr1ddr1dddr1ddr1dddr1ddr"}
                self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
                self.pocket = "Armor"
                self.gearSlot = "Legs Under"
            elif num == 12:
                self.prefix = "A pair of"
                self.name = {"String":"Iron Greaves", "Code":"1a1da1dda1ddda1w1ddda1dda1da2a1da1dda"}
                self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
                self.pocket = "Armor"
                self.gearSlot = "Legs Over"
            elif num == 13:
                self.prefix = "A pair of"
                self.name = {"String":"Leather Boots", "Code":"1ddo7dddo1ddo4dddo"}
                self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
                self.pocket = "Armor"
                self.gearSlot = "Feet"

        # Misc. #
        if self.name["String"] == "Debug Item":
            if num == 100:
                self.name = {"String":"Silver Keycard", "Code":"1ddw1dw1w1ddw1dw1w8w"}
                self.keyList = ["key", "card"]
                self.flags["Password List"] = ["COTU Spaceport"]
            elif num == 101:
                self.prefix = "An"
                self.name = {"String":"Ornate Chest", "Code":"1y1dy1ddy1dddy1ddy1dy1w1ddo4dddo"}
                self.containerList = []
            
        # All Containers Are Automatically NO GET #
        if self.containerList != None:
            self.flags['No Get'] = True
        
        # Create Key List #
        for word in self.name["String"].split():
            if word.lower() not in self.keyList:
                self.keyList.append(word.lower())
        self.keyList.append(self.name["String"].lower())

        if "Code" not in self.name:
            self.name["Code"] = str(len(self.name["String"])) + "w"
        if "Code" not in self.roomDescription:
            self.roomDescription["Code"] = str(len(self.roomDescription["String"])) + "w"

    def lookDescription(self, console, lookDistance=0, passwordCheck=False):
        if "Glowing" in self.flags and self.flags["Glowing"] == True:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "It's glowing.", "Code":"2w1y9w1y"})
        else:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You see nothing special.", "Code":"23w1y"})

        if self.containerList != None and lookDistance == 0:
            console.lineList.insert(0, {"Blank": True})
            if self.containerPassword != None and passwordCheck == False:
                console.lineList.insert(0, {"String": "It's locked.", "Code":"2w1y8w1y"})
            elif len(self.containerList) == 0:
                console.lineList.insert(0, {"String": "It's empty.", "Code":"2w1y7w1y"})
            else:
                console.lineList.insert(0, {"String": "It contains:", "Code":"11w1y"})
                containerItemData = {}
                for item in self.containerList:
                    if item.num not in containerItemData:
                        containerItemData[item.num] = {"Count":1, "Item":item}
                    else:
                        containerItemData[item.num]["Count"] += 1

                for itemData in containerItemData:
                    itemData = containerItemData[itemData]
                    displayString = itemData["Item"].prefix + " " + itemData["Item"].name["String"]
                    displayCode = str(len(itemData["Item"].prefix)) + "w1w" + itemData["Item"].name["Code"]
                    modString = ""
                    modCode = ""
                    if "Glowing" in itemData["Item"].flags and itemData["Item"].flags["Glowing"] == True:
                        modString = " (Glowing)"
                        modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                    countString = ""
                    countCode = ""
                    if itemData["Count"] > 1:
                        countString = " (" + str(itemData["Count"]) + ")"
                        countCode = "2r" + str(len(str(itemData["Count"]))) + "w1r"
                    console.lineList.insert(0, {"String":displayString + modString + countString, "Code":displayCode + modCode + countCode})
            
    def lightInContainerCheck(self):
        if self.containerList != None:
            for item in self.containerList:
                if "Glowing" in item.flags and item.flags["Glowing"] == True:
                    return True

        return False
