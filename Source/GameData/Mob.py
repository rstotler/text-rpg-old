class Mob:

    def __init__(self, num):
        self.num = num

        self.prefix = "A"
        self.name = {"String":"Debug Mob", "Code":"9w"}
        self.roomDescription = {"String":"is standing here.", "Code":"16w1y"}
        self.keyList = []

        self.loadMob(num)

    def loadMob(self, num):
        if num == 1:
            self.name = {"String":"Robotic Greeter Droid", "Code":"21w"}

        # Create Key List #
        for word in self.name["String"].split():
            if word.lower() not in self.keyList:
                self.keyList.append(word.lower())
        self.keyList.append(self.name["String"].lower())

    def lookDescription(self, console):
        console.lineList.insert(0, {"Blank": True})
        console.lineList.insert(0, {"String": "You see nothing special.", "Code":"23w1y"})
