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

        self.loadItem(num)

    def loadItem(self, num):
        if num == 1:
            self.prefix = "An"
            self.name = {"String":"Oak Seed", "Code":"1do3ddo4w"}
        elif num == 2:
            self.name = {"String":"Maple Seed", "Code":"1dg5ddg4w"}
        elif num == 3:
            self.name = {"String":"Pine Seed", "Code":"1do4ddo4w"}
        elif num == 4:
            self.name = {"String":"Silver Keycard", "Code":"1ddw1dw1w1ddw1dw1w8w"}
            self.keyList = ["key", "card"]
            self.flags["Password List"] = ["COTU Spaceport"]
        elif num == 5:
            self.name = {"String":"Iron Helmet"}
            self.pocket = "Armor"
            self.gearSlot = "Head"
        elif num == 6:
            self.name = {"String":"Ancient Mask"}
            self.pocket = "Armor"
            self.gearSlot = "Face"
        elif num == 7:
            self.name = {"String":"Heart Locket"}
            self.pocket = "Armor"
            self.gearSlot = "Neck"
        elif num == 8:
            self.name = {"String":"Star Pendant"}
            self.pocket = "Armor"
            self.gearSlot = "Neck"
        elif num == 9:
            self.name = {"String":"Fuzzy Sweater"}
            self.pocket = "Armor"
            self.gearSlot = "Body Under"
        elif num == 10:
            self.name = {"String":"Breastplate"}
            self.pocket = "Armor"
            self.gearSlot = "Body Over"
        elif num == 11:
            self.name = {"String":"Leather Gloves"}
            self.prefix = "A pair of"
            self.roomDescription = {"String":"are laying on the ground.", "Code":"24w1y"}
            self.pocket = "Armor"
            self.gearSlot = "Hands"
        elif num == 12:
            self.name = {"String":"Ruby Ring", "Code":"1lr1r1dr1ddr1w1ly1y1dy1ddy"}
            self.roomDescription = {"String":"has been dropped on the ground.", "Code":"30w1y"}
            self.pocket = "Armor"
            self.gearSlot = "Finger"
            self.flags["Glowing"] = True
        elif num == 13:
            self.name = {"String":"Emerald Ring"}
            self.pocket = "Armor"
            self.gearSlot = "Finger"
        elif num == 14:
            self.name = {"String":"Gold Ring"}
            self.pocket = "Armor"
            self.gearSlot = "Finger"
        elif num == 15:
            self.name = {"String":"Warm Pants"}
            self.pocket = "Armor"
            self.gearSlot = "Legs Under"
        elif num == 16:
            self.name = {"String":"Pair of Greaves"}
            self.pocket = "Armor"
            self.gearSlot = "Legs Over"
        elif num == 17:
            self.name = {"String":"Leather Boots"}
            self.pocket = "Armor"
            self.gearSlot = "Feet"
        elif num == 18:
            self.name = {"String":"An Ornate Chest"}
            self.containerList = []

        # Containers Are Automatically NO GET #
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
