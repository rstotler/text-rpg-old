class Item:

    def __init__(self, num):
        self.num = num
        self.weight = 10.0
        self.flags = {}

        self.prefix = "A"
        self.name = {"String":"Debug Item"}
        self.roomDescription = {"String":"is laying on the ground.", "Code":"23w1y"}
        self.keyList = []
        self.pocket = "Misc"

        self.loadItem(num)

    def loadItem(self, num):
        if num == 1:
            self.prefix = "An"
            self.name = {"String":"Oak Seed", "Code":"1ddo3do4w"}
        elif num == 2:
            self.name = {"String":"Maple Seed", "Code":"1ddg5dg4w"}
        elif num == 3:
            self.name = {"String":"Pine Seed", "Code":"1ddo4do4w"}
        elif num == 4:
            self.name = {"String":"Gold Key", "Code":"1y4dy3w"}
            self.flags["Password List"] = ["1234"]
        elif num == 5:
            self.name = {"String":"Silver Keycard", "Code":"1ddw6dw7w"}
            self.flags["Password List"] = ["Spaceport"]

        # Create Key List #
        for word in self.name["String"].split():
            if word.lower() not in self.keyList:
                self.keyList.append(word.lower())

        if "Code" not in self.name:
            self.name["Code"] = str(len(self.name["String"])) + "w"
        if "Code" not in self.roomDescription:
            self.roomDescription["Code"] = str(len(self.roomDescription["String"])) + "w"
