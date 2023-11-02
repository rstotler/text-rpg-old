from GameData.Item.Item import Item
from Components.Utility import *

class Ammo(Item):
    
    def __init__(self, num, quantity):
        Item.__init__(self, num, False)
        self.pocket = "Ammo"

        self.ammoType = None
        self.ammoCapacity = None
        
        self.quantity = quantity

        self.loadAmmo(num)

    def loadAmmo(self, num):
        if num == 1:
            self.name = {"String":"Quiver", "Code":"6w"}
            self.ammoType = "Arrow"
            self.ammoCapacity = 25

        elif num == 2:
            self.prefix = "An"
            self.name = {"String":"Arrow", "Code":"5w"}
            self.ammoType = "Arrow"

        elif num == 3:
            self.name = {"String":"9mm 12-Round Magazine", "Code":"6w1y14w"}
            self.ammoType = "9mm"
            self.ammoCapacity = 12

        elif num == 4:
            self.name = {"String":"9mm Standard Round", "Code":"18w"}
            self.ammoType = "9mm"

        elif num == 5:
            self.name = {"String":".45 8-Round Magazine", "Code":"1y4w1y14w"}
            self.ammoType = ".45"
            self.ammoCapacity = 8

        elif num == 6:
            self.name = {"String":".45 Standard Round", "Code":"1y17w"}
            self.ammoType = ".45"

        elif num == 7:
            self.name = {"String":"5.56 6-Round Magazine", "Code":"1w1y4w1y14w"}
            self.ammoType = "5.56"
            self.ammoCapacity = 6

        elif num == 8:
            self.name = {"String":"5.56 Standard Round", "Code":"1w1y17w"}
            self.ammoType = "5.56"

        elif num == 9:
            self.name = {"String":"12 Gauge Shell", "Code":"14w"}
            self.ammoType = "12 Gauge"

        elif num == 10:
            self.name = {"String":"Missile", "Code":"7w"}
            self.ammoType = "Missile"

        # Quiver Setup #
        if self.ammoType == "Arrow" and self.ammoCapacity != None:
            self.containerList = []
            self.containerMaxLimit = 10.0

        # Magazine Setup #
        if self.ammoCapacity != None:
            self.flags["Ammo"] = None

        # Quantity Item Setup #
        if self.quantity == None and self.ammoCapacity == None:
            self.quantity = 1

        # Create Key List #
        appendKeyList(self.keyList, self.name["String"].lower())
        for word in self.name["String"].lower().split():
            if '-' in word:
                for subword in word.split('-'):
                    if subword not in self.keyList:
                        self.keyList.append(subword)
                if word.replace('-', ' ').strip() not in self.keyList:
                    self.keyList.append(word.replace('-', ' ').strip())

        if self.ammoType[0] == '.':
            self.keyList.append(self.ammoType[1::])
        if self.ammoCapacity != None:
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
