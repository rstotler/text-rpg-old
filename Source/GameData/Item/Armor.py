from GameData.Item.Item import Item
from Components.Utility import *

class Armor(Item):
    
    def __init__(self, num):
        Item.__init__(self, num)
        self.pocket = "Armor"

        self.skillList = []

        self.gearSlot = None
        self.armorRating = {"Piercing":0, "Cutting":0, "Blunt":0}

        self.loadArmor(num)

    def loadArmor(self, num):
        if num == 1:
            self.prefix = "An"
            self.name = {"String":"Iron Helmet", "Code":"1a1da1dda1ddda1w1ddda1dda1da1a1da1dda"}
            self.gearSlot = "Head"
        elif num == 2:
            self.prefix = "An"
            self.name = {"String":"Ancient Mask", "Code":"1y1dy1ddy1dddy1ddy1dy1y1w1y1dy1ddy1dddy"}
            self.gearSlot = "Face"
        elif num == 3:
            self.name = {"String":"Heart Locket", "Code":"1lr1r1dr1lr1r1w1y1dy1ddy1y1dy1ddy"}
            self.gearSlot = "Neck"
        elif num == 4:
            self.name = {"String":"Star Pendant", "Code":"1y1dy1ddy1dddy1w1y1dy1ddy1dddy1ddy1dy1y"}
            self.gearSlot = "Neck"
        elif num == 5:
            self.name = {"String":"Fuzzy Sweater", "Code":"1r1g1do1dr1ddg1w1da6dda"}
            self.gearSlot = "Body Under"
        elif num == 6:
            self.name = {"String":"Breastplate", "Code":"1ddda1dda1da1a1da1dda1ddda1dda1da1a1da"}
            self.gearSlot = "Body Over"
        elif num == 7:
            self.prefix = "A pair of"
            self.name = {"String":"Leather Gloves", "Code":"1ddo6dddo1w1ddo5dddo"}
            self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
            self.gearSlot = "Hands"
        elif num == 8:
            self.name = {"String":"Ruby Ring", "Code":"1lr1r1dr1ddr1w1ly1y1dy1ddy"}
            self.roomDescription = {"String":"has been dropped on the ground.", "Code":"30w1y"}
            self.gearSlot = "Finger"
            self.flags["Glowing"] = True
        elif num == 9:
            self.prefix = "An"
            self.name = {"String":"Emerald Ring", "Code":"1g1dg1ddg1dddg1ddg1dg1g1w1ly1y1dy1ddy"}
            self.gearSlot = "Finger"
        elif num == 10:
            self.name = {"String":"Gold Ring", "Code":"1ly1y1dy1ddy1w1ly1y1dy1ddy"}
            self.gearSlot = "Finger"
        elif num == 11:
            self.prefix = "A pair of"
            self.name = {"String":"Swimming Trunks", "Code":"1dr1ddr1dddr1ddr1dddr1ddr1dddr1ddr1w1dr1ddr1dddr1ddr1dddr1ddr"}
            self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
            self.gearSlot = "Legs Under"
        elif num == 12:
            self.prefix = "A pair of"
            self.name = {"String":"Iron Greaves", "Code":"1a1da1dda1ddda1w1ddda1dda1da2a1da1dda"}
            self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
            self.gearSlot = "Legs Over"
        elif num == 13:
            self.prefix = "A pair of"
            self.name = {"String":"Leather Boots", "Code":"1ddo7dddo1ddo4dddo"}
            self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
            self.gearSlot = "Feet"
        elif num == 14:
            self.name = {"String":"Backpack", "Code":"8w"}
            self.gearSlot = "About Body"
            self.containerList = []
            self.containerMaxLimit = 50.0

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
