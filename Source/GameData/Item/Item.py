from Components.Utility import *

class Item:

    def __init__(self, num):
        self.num = num
        self.flags = {}

        self.prefix = "A"
        self.name = {"String":"Debug Item"}
        self.roomDescription = {"String":"is laying on the ground.", "Code":"23w1y"}
        self.description = {"String":"You see nothing special.", "Code":"23w1y"}
        self.keyList = []

        self.pocket = "Misc"
        self.weight = 1.0
        
        self.containerList = None
        self.containerPassword = None
        self.containerMaxLimit = None

        self.buttonList = None

        self.loadItem(num)

    def loadItem(self, num):
        
        # Keys (701 - 800) #
        if self.name["String"] == "Debug Item":
            if num == 701:
                self.name = {"String":"Silver Keycard", "Code":"1ddw1dw1w1ddw1dw1w8w"}
                self.pocket = "Key"
                appendKeyList(self.keyList, "card")
                self.flags["Password List"] = ["COTU Spaceport"]

        # Food (801 - 900) #
        if self.name["String"] == "Debug Item":
            if num == 801:
                self.name = {"String":"Hamburger", "Code":"9w"}
                self.pocket = "Food"
            if num == 802:
                self.name = {"String":"Panini", "Code":"6w"}
                self.pocket = "Food"
            if num == 803:
                self.name = {"String":"Salad", "Code":"5w"}
                self.pocket = "Food"
            if num == 804:
                self.name = {"String":"Cookie", "Code":"6w"}
                self.pocket = "Food"

        # Misc. (901 - 1000) #
        if self.name["String"] == "Debug Item":
            if num == 902:
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
            elif num == 905:
                self.name = {"String":"Control Panel", "Code":"13w"}
                self.roomDescription = {"String":"is attatched to the wall.", "Code":"24w1y"}
                self.flags["No Get"] = True
                self.buttonList = []

        # Organic (1001 - 1100) #
        if self.name["String"] == "Debug Item":
            if self.num == 1001:
                self.name = {"String":"Seed", "Code":"4w"}
                self.pocket = "Organic"

        # Special Items #
        if self.name["String"] == "Debug Item":
            if num == 666:
                self.name = {"String":"Corpse", "Code":"6w"}
                self.roomDescription = {"String":"is laying on the ground.", "Code":"23w1y"}
                self.containerList = []
            elif num == 667:
                self.name = {"String":"Body Part", "Code":"9w"}
                self.roomDescription = {"String":"is laying on the ground.", "Code":"23w1y"}

        # Container Setup #
        if self.containerList != None:
            if self.containerMaxLimit == None:
                self.containerMaxLimit = 100.0
        
        # Create Key List #
        appendKeyList(self.keyList, self.name["String"].lower())
        for word in self.name["String"].lower().split():
            if '-' in word:
                for subword in word.split('-'):
                    if subword not in self.keyList:
                        self.keyList.append(subword)
                if word.replace('-', ' ').strip() not in self.keyList:
                    self.keyList.append(word.replace('-', ' ').strip())

        if "Code" not in self.name:
            self.name["Code"] = str(len(self.name["String"])) + "w"
        if "Code" not in self.roomDescription:
            self.roomDescription["Code"] = str(len(self.roomDescription["String"])) + "w"

    def lookDescription(self, console, lookDistance=0, passwordCheck=False):
        console.write("You look at " + self.prefix.lower() + " " + self.name["String"] + ".", "12w" + str(len(self.prefix)) + "w1w" + self.name["Code"] + "1y", True)
        
        if "Glowing" in self.flags and self.flags["Glowing"] == True:
            console.write("It's glowing.", "2w1y9w1y")
        elif self.containerList == None:
            console.write(self.description["String"], self.description["Code"])

        # Container #
        if self.containerList != None and lookDistance == 0:
            if self.containerPassword != None and passwordCheck == False:
                console.write("It's locked.", "2w1y8w1y")
            elif len(self.containerList) == 0:
                console.write("It's empty.", "2w1y7w1y")
            else:
                console.write("It contains:", "11w1y")
                displayList = []
                for item in self.containerList:
                    if item.pocket == "Weapon" and item.ranged == True:
                        displayList.append({"ItemData":item})
                    else:
                        displayData = None
                        for data in displayList:
                            if "Num" in data and data["Num"] == item.num:
                                displayData = data
                                break
                        if displayData == None:
                            itemCount = 1
                            if hasattr(item, "quantity") == True:
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
                    countNum = 0
                    if "Count" in itemData : countNum = itemData["Count"]
                    countString, countCode = getCountString(countNum)
                    weaponStatusString = ""
                    weaponStatusCode = ""
                    if itemData["ItemData"].pocket == "Weapon":
                        weaponStatusString, weaponStatusCode = itemData["ItemData"].getWeaponStatusString()
                    console.write(displayString + weaponStatusString + modString + countString, displayCode + weaponStatusCode + modCode + countCode)
            
        # Gun #
        elif self.pocket == "Weapon" and self.ranged == True:
            displayString, displayCode = self.getWeaponStatusString()
            console.write("Rounds:" + displayString, "6w1y" + displayCode)

        # Buttons #
        if self.buttonList != None and len(self.buttonList) > 0:
            if len(self.buttonList) == 1 and self.buttonList[0].label == None:
                console.write("It has an unlabled button.", "25w")
            elif len(self.buttonList) == 1:
                console.write("It has a button labled, '" + self.buttonList[0].label["String"] + "'.", "22w3y" + self.buttonList[0].label["Code"] + "2y", True)
            else:
                console.write("It has several buttons:", "22w1y")
                for button in self.buttonList:
                    if button.label == None:
                        console.write("An unlabled button.", "18w")
                    else:
                        displayString = "A button labled, '" + button.label["String"] + "'."
                        displayCode = "15w3y" + button.label["Code"] + "2y"
                        console.write(displayString, displayCode)

    def getWeight(self, multiplyQuantity=True):
        if hasattr(self, "quantity") == False:
            weight = self.weight + self.getContainerWeight()
            if self.pocket == "Weapon" and self.ranged == True and self.magazine != None:
                if self.magazine.shellCapacity == None:
                    if self.magazine.quantity != None:
                        weight += self.magazine.weight * self.magazine.quantity
                else:
                    weight += self.magazine.weight
                    if self.magazine.flags["Ammo"] != None:
                        weight += self.magazine.flags["Ammo"].weight * self.magazine.flags["Ammo"].quantity

            return weight

        else:
            if multiplyQuantity == True and hasattr(self, "quantity") == True:
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

    def isEmpty(self, magazineCheck=False):

        # Empty Container Check #
        if self.containerList != None:
            if len(self.containerList) == 0:
                return True
            return False

        return False

    def lightInContainerCheck(self):
        if self.containerList != None:
            for item in self.containerList:
                if "Glowing" in item.flags and item.flags["Glowing"] == True:
                    return True

        return False

    @staticmethod
    def createCorpse(targetMob):
        corpseItem = createItem(666)

        if targetMob.num == None:
            corpseItem.prefix = "Your"
            corpseItem.name["String"] = "corpse"
            corpseItem.name["Code"] = "6w"
            appendKeyList(corpseItem.keyList, "your corpse")
        else:
            corpseItem.prefix = "The corpse of"
            if "Head" in targetMob.cutLimbList:
                corpseItem.prefix = "The headless corpse of"
                appendKeyList(corpseItem.keyList, "headless")
            corpseItem.name["String"] = targetMob.prefix.lower() + " " + targetMob.name["String"]
            corpseItem.name["Code"] = str(len(targetMob.prefix)) + "w1w" + targetMob.name["Code"]
        for item in targetMob.getAllItemList():
            corpseItem.containerList.append(item)
        appendKeyList(corpseItem.keyList, corpseItem.name["String"].lower())
        return corpseItem

    @staticmethod
    def createBodyPart(targetMob, targetLimb):
        bodyPartItem = createItem(667)
        bodyPartItem.prefix = "The"
        bodyPartItem.name["String"] = targetLimb.lower() + " of " + targetMob.prefix.lower() + " " + targetMob.name["String"]
        bodyPartItem.name["Code"] = str(len(targetLimb)) + "w4w" + str(len(targetMob.prefix)) + "w1w" + targetMob.name["Code"]
        appendKeyList(bodyPartItem.keyList, bodyPartItem.name["String"].lower())
        return bodyPartItem

    @staticmethod
    def getSpecialItemNum(targetItem):
        if targetItem == "Corpse":
            return 666
        return 0
