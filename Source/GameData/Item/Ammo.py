from GameData.Item.Item import Item
from Components.Utility import *

class Ammo(Item):
    
    def __init__(self, num, quantity):
        Item.__init__(self, num)
        self.pocket = "Ammo"

        self.ammoType = None
        self.shellCapacity = None
        
        self.quantity = quantity

        self.loadAmmo(num)

    def loadAmmo(self, num):
        if num == 201:
            self.name = {"String":".45 8-Round Magazine", "Code":"1y4w1y14w"}
            self.ammoType = ".45"
            self.shellCapacity = 8
        if num == 202:
            self.name = {"String":".45 12-Round Magazine", "Code":"1y5w1y14w"}
            self.ammoType = ".45"
            self.shellCapacity = 12
        if num == 203:
            self.name = {"String":".45 Standard Round", "Code":"1y17w"}
            self.ammoType = ".45"
        if num == 204:
            self.name = {"String":".45 AP Round", "Code":"1y11w"}
            self.ammoType = ".45"
        if num == 205:
            self.name = {"String":"Missile", "Code":"7w"}
            self.ammoType = "Missile"
        if num == 206:
            self.name = {"String":"12 Gauge Shell", "Code":"14w"}
            self.ammoType = "12 Gauge"
        if num == 207:
            self.name = {"String":"AP Missile", "Code":"10w"}
            self.ammoType = "Missile"
        if num == 208:
            self.name = {"String":".45 HP Round", "Code":"1y11w"}
            self.ammoType = ".45"
        if num == 209:
            self.name = {"String":"5.56 6-Round Magazine", "Code":"1w1y4w1y14w"}
            self.ammoType = "5.56"
            self.shellCapacity = 6
        if num == 210:
            self.name = {"String":"5.56 Standard Round", "Code":"1w1y17w"}
            self.ammoType = "5.56"

        # Magazine Setup #
        if self.shellCapacity != None:
            self.flags["Ammo"] = None

        # Quantity Item Setup #
        if self.quantity == None:
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
