class Skill:

    def __init__(self, num):
        self.num = num
        self.name = {"String":"Debug Skill", "Code":"11w"}
        self.keyList = []

        self.learnPercent = 0

        self.loadSkill(num)

    def loadSkill(self, num):

        # Weapon Skill (1001 - ???) #
        if num == 1001:
            self.name = {"String":"Swords", "Code":"1w5ddw"}
        elif num == 1002:
            self.name = {"String":"Daggers", "Code":"1w6ddw"}
        elif num == 1003:
            self.name = {"String":"Axes", "Code":"1w3ddw"}
        elif num == 1004:
            self.name = {"String":"Blunt", "Code":"1w4ddw"}
        elif num == 1005:
            self.name = {"String":"Polearms", "Code":"1w7ddw"}
        elif num == 1006:
            self.name = {"String":"Unarmed", "Code":"1w6ddw"}
        elif num == 1007:
            self.name = {"String":"Bows", "Code":"1w3ddw"}
        elif num == 1008:
            self.name = {"String":"Pistols", "Code":"1w6ddw"}
        elif num == 1009:
            self.name = {"String":"Rifles", "Code":"1w5ddw"}
        elif num == 1010:
            self.name = {"String":"Explosives", "Code":"1w9ddw"}
        elif num == 1011:
            self.name = {"String":"Throwing", "Code":"1w7ddw"}
