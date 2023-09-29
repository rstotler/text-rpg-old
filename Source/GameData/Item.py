class Item:

    def __init__(self, num, quantity=None):
        self.num = num
        self.quantity = quantity
        self.flags = {}

        self.prefix = "A"
        self.name = {"String":"Debug Item"}
        self.roomDescription = {"String":"is laying on the ground.", "Code":"23w1y"}
        self.keyList = []

        self.weight = 1.0
        self.pocket = "Misc"
        self.gearSlot = None
        self.twoHanded = False

        self.ranged = False
        self.ammoType = None
        self.magazine = None # (Object) Magazine Item OR (Object) Ammo
        self.shellCapacity = None

        self.containerList = None
        self.containerPassword = None
        self.containerMaxLimit = None

        self.loadItem(num)

    def loadItem(self, num):
        
        # Armor (1 - 100) #
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
            elif num == 14:
                self.name = {"String":"Backpack", "Code":"8w"}
                self.pocket = "Armor"
                self.gearSlot = "About Body"
                self.containerList = []
                self.containerMaxLimit = 50.0

        # Weapons (101 - 200) #
        if self.name["String"] == "Debug Item":
            if num == 101:
                self.name = {"String":"Sword", "Code":"1w4ddw"}
                self.pocket = "Weapon"
            elif num == 102:
                self.name = {"String":"Shield", "Code":"1w5ddw"}
                self.pocket = "Weapon"
            elif num == 103:
                self.name = {"String":"Lance", "Code":"1w4ddw"}
                self.pocket = "Weapon"
            elif num == 104:
                self.name = {"String":"Greatsword", "Code":"1w9ddw"}
                self.keyList = ["great"]
                self.pocket = "Weapon"
                self.twoHanded = True
            elif num == 105:
                self.prefix = "An"
                self.name = {"String":"Ebony Pistol", "Code":"1w5ddw1w5ddw"}
                self.pocket = "Weapon"
                self.ranged = True
                self.ammoType = ".45"
            elif num == 106:
                self.prefix = "An"
                self.name = {"String":"Ivory Pistol", "Code":"1w5ddw1w5ddw"}
                self.pocket = "Weapon"
                self.ranged = True
                self.ammoType = ".45"
            elif num == 107:
                self.name = {"String":"Sniper Rifle", "Code":"1w6ddw1w4ddw"}
                self.pocket = "Weapon"
                self.twoHanded = True
                self.ranged = True
                self.ammoType = "5.56"
            elif num == 108:
                self.name = {"String":"Rocket Launcher", "Code":"15w"}
                self.pocket = "Weapon"
                # self.twoHanded = True
                self.ranged = True
                self.shellCapacity = 1
                self.ammoType = "Missile"
            elif num == 109:
                self.name = {"String":"Shotgun", "Code":"7w"}
                self.pocket = "Weapon"
                self.twoHanded = True
                self.ranged = True
                self.shellCapacity = 5
                self.ammoType = "12 Gauge"

        # Ammo & Magazines (201 - 300) #
        if self.name["String"] == "Debug Item":
            if num == 201:
                self.name = {"String":".45 8-Round Magazine", "Code":"1y4w1y14w"}
                self.pocket = "Ammo"
                self.ammoType = ".45"
                self.shellCapacity = 8
            if num == 202:
                self.name = {"String":".45 12-Round Magazine", "Code":"1y5w1y14w"}
                self.pocket = "Ammo"
                self.ammoType = ".45"
                self.shellCapacity = 12
            if num == 203:
                self.name = {"String":".45 Round", "Code":"1y8w"}
                self.pocket = "Ammo"
                self.ammoType = ".45"
            if num == 204:
                self.name = {"String":".45 AP Round", "Code":"1y11w"}
                self.pocket = "Ammo"
                self.ammoType = ".45"
            if num == 205:
                self.name = {"String":"Missile", "Code":"7w"}
                self.pocket = "Ammo"
                self.ammoType = "Missile"
            if num == 206:
                self.name = {"String":"12 Gauge Shell", "Code":"14w"}
                self.pocket = "Ammo"
                self.ammoType = "12 Gauge"
            if num == 207:
                self.name = {"String":"AP Missile", "Code":"10w"}
                self.pocket = "Ammo"
                self.ammoType = "Missile"
            if num == 208:
                self.name = {"String":".45 HP Round", "Code":"1y11w"}
                self.pocket = "Ammo"
                self.ammoType = ".45"

        # Misc. (901 - 1000) #
        if self.name["String"] == "Debug Item":
            if num == 901:
                self.name = {"String":"Silver Keycard", "Code":"1ddw1dw1w1ddw1dw1w8w"}
                self.keyList = ["key", "card"]
                self.flags["Password List"] = ["COTU Spaceport"]
            elif num == 902:
                self.prefix = "An"
                self.name = {"String":"Ornate Chest", "Code":"1y1dy1ddy1dddy1ddy1dy1w1ddo4dddo"}
                self.roomDescription = {"String":"sits on the ground.", "Code":"18w1y"}
                self.flags["No Get"] = True
                self.containerList = []
            elif num == 903:
                self.name = {"String":"Weapon Cabinet", "Code":"1w6ddw1w6ddw"}
                self.roomDescription = {"String":"is sitting here.", "Code":"15w1y"}
                self.flags["No Get"] = True
                self.containerList = []
                self.containerMaxLimit = 500.0
            elif num == 904:
                self.name = {"String":"Lamp", "Code":"4w"}
                self.roomDescription = {"String":"is sitting in the corner.", "Code":"24w1y"}
                self.flags["Glowing"] = True
                self.flags["No Get"] = True

        # Quantity Item Setup #
        if self.quantity == None:
            if self.pocket == "Ammo" and self.magazine == False:
                self.quantity = 1

        # Container Setup #
        if self.containerList != None:
            if self.containerMaxLimit == None:
                self.containerMaxLimit = 100.0
        
        # Create Key List #
        for index, word in enumerate(self.name["String"].split()):
            if word.lower() not in self.keyList:
                self.keyList.append(word.lower())
            if word[0] == '.':
                self.keyList.append(word.lower()[1::])
            if index < len(self.name["String"].split()) - 1:
                self.keyList.append(' '.join(self.name["String"].lower().split()[index:index + 2]))
            if len(word) > 2 and '-' in word:
                for subWord in word.split('-'):
                    self.keyList.append(subWord.lower())
            for i in range(4):
                if len(word) > i + 3:
                    self.keyList.append(word.lower()[0:3 + i])
        self.keyList.append(self.name["String"].lower())

        # Ammo & Magazine Setup #
        if self.pocket == "Ammo":
            if self.shellCapacity != None:
                self.flags["Ammo"] = None

            if self.ammoType[0] == '.':
                self.keyList.append(self.ammoType[1::])
            if self.shellCapacity != None:
                self.keyList.append("mag")
                self.keyList.append(self.ammoType + " mag")
                self.keyList.append(self.ammoType + " magazine")
                if self.ammoType[0] == '.':
                    self.keyList.append(self.ammoType[1::] + " mag")
                    self.keyList.append(self.ammoType[1::] + " magazine")
                if "round" in self.keyList:
                    del self.keyList[self.keyList.index("round")]

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
                displayList = []
                for item in self.containerList:
                    if item.ranged == True:
                        displayList.append({"ItemData":item})
                    else:
                        displayData = None
                        for data in displayList:
                            if "Num" in data and data["Num"] == item.num:
                                displayData = data
                                break
                        if displayData == None:
                            itemCount = 1
                            if item.quantity != None:
                                itemCount = item.quantity
                            displayList.append({"Num":item.num, "Count":itemCount, "ItemData":item})
                        else:
                            displayData["Count"] += 1

                for itemData in displayList:
                    displayString = itemData["ItemData"].prefix + " " + itemData["ItemData"].name["String"]
                    displayCode = str(len(itemData["ItemData"].prefix)) + "w1w" + itemData["ItemData"].name["Code"]
                    modString = ""
                    modCode = ""
                    if "Glowing" in itemData["ItemData"].flags and itemData["ItemData"].flags["Glowing"] == True:
                        modString = " (Glowing)"
                        modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                    countString = ""
                    countCode = ""
                    if "Count" in itemData and itemData["Count"] > 1:
                        countString = " (" + str(itemData["Count"]) + ")"
                        countCode = "2r" + str(len(str(itemData["Count"]))) + "w1r"
                    weaponStatusString, weaponStatusCode = itemData["ItemData"].getWeaponStatusString()
                    console.lineList.insert(0, {"String":displayString + weaponStatusString + modString + countString, "Code":displayCode + weaponStatusCode + modCode + countCode})
            
    def lightInContainerCheck(self):
        if self.containerList != None:
            for item in self.containerList:
                if "Glowing" in item.flags and item.flags["Glowing"] == True:
                    return True

        return False

    def getWeight(self, multiplyQuantity=True):
        if self.quantity == None:
            weight = self.weight + self.getContainerWeight()
            if self.ranged == True and self.magazine != None:
                if self.magazine.shellCapacity == None and self.magazine.quantity != None:
                    weight += self.magazine.weight * self.magazine.quantity
                else:
                    weight += self.magazine.weight
                    if self.magazine.flags["Ammo"] != None:
                        weight += self.magazine.flags["Ammo"].weight * self.magazine.flags["Ammo"].quantity

            return weight
        else:
            if multiplyQuantity == True:
                return self.weight * self.quantity
            else:
                return self.weight

    def getContainerWeight(self):
        weight = 0
        if self.containerList != None:
            for item in self.containerList:
                weight += item.getWeight()
        return weight

    def getContainerItem(self, targetItemKey):
        if self.containerList != None:
            for item in self.containerList:
                if (isinstance(targetItemKey, str) and targetItemKey in item.keyList) or (isinstance(targetItemKey, int) and targetItemKey == item.num):
                    return item
        return None

    def isLoaded(self, ammoList=[]):
        maxInventoryMagCapacity = -1
        if len(ammoList) > 0:
            maxInventoryMagCapacity = 0
            for item in ammoList:
                if item.shellCapacity != None and item.ammoType == self.ammoType:
                    if item.shellCapacity > maxInventoryMagCapacity:
                        maxInventoryMagCapacity = item.shellCapacity
        
        if self.pocket == "Weapon" and self.ranged == True:
            if self.shellCapacity != None and self.magazine != None and self.shellCapacity >= self.magazine.quantity:
                return True
            elif self.shellCapacity == None and self.magazine != None and maxInventoryMagCapacity <= self.magazine.shellCapacity and "Ammo" in self.magazine.flags and self.magazine.flags["Ammo"] != None and self.magazine.flags["Ammo"].quantity >= self.magazine.shellCapacity:
                return True
        return False

    def getWeaponStatusString(self):
        statusString = ""
        statusCode = ""
        if self.ranged == True:
            if self.shellCapacity == None and self.magazine == None:
                statusString = " [Empty]"
                statusCode = "2y5w1y"
            else:
                if self.shellCapacity != None:
                    currentRounds = 0
                    if self.magazine != None:
                        currentRounds = self.magazine.quantity
                    maxRounds = self.shellCapacity
                else:
                    currentRounds = 0
                    if self.magazine.flags["Ammo"] != None:
                        currentRounds = self.magazine.flags["Ammo"].quantity
                    maxRounds = self.magazine.shellCapacity
                statusString += " [" + str(currentRounds) + "/" + str(maxRounds) + "]"
                statusCode += "2y" + str(len(str(currentRounds))) + "w1y" + str(len(str(maxRounds))) + "w1y"

        return statusString, statusCode
