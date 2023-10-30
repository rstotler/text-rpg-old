class Skill:

    def __init__(self, num):
        self.num = num
        self.name = {"String":"Debug Skill", "Code":"11w"}
        self.keyList = []

        self.learnPercent = 0

        self.loadSkill(num)

    def loadSkill(self, num):
        if num == 1:
            self.name = {"String":"Melee", "Code":"1w4ddw"}
        elif num == 2:
            self.name = {"String":"Swords", "Code":"1w5ddw"}
        elif num == 3:
            self.name = {"String":"Daggers", "Code":"1w6ddw"}
        elif num == 4:
            self.name = {"String":"Claws", "Code":"1w4ddw"}
        elif num == 5:
            self.name = {"String":"Axes", "Code":"1w3ddw"}
        elif num == 6:
            self.name = {"String":"Blunt", "Code":"1w4ddw"}
        elif num == 7:
            self.name = {"String":"Polearms", "Code":"1w7ddw"}
        elif num == 8:
            self.name = {"String":"Shields", "Code":"1w6ddw"}
        elif num == 9:
            self.name = {"String":"Bows", "Code":"1w3ddw"}
        elif num == 10:
            self.name = {"String":"Pistols", "Code":"1w6ddw"}
        elif num == 11:
            self.name = {"String":"Rifles", "Code":"1w5ddw"}
        elif num == 12:
            self.name = {"String":"Throwing", "Code":"1w7ddw"}
        elif num == 13:
            self.name = {"String":"Explosives", "Code":"1w9ddw"}
        elif num == 14:
            self.name = {"String":"Staves", "Code":"1w5ddw"}
