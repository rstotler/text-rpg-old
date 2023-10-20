class Skill:

    def __init__(self, num):
        self.num = num
        self.name = {"String":"Debug Skill", "Code":"11w"}
        self.keyList = []

        self.learnPercent = 0

        self.loadSkill(num)

    def loadSkill(self, num):

        # Weapon Skill (501 - ???) #
        if num == 501:
            self.name = {"String":"Swords", "Code":"1w5ddw"}
        elif num == 502:
            self.name = {"String":"Daggers", "Code":"1w6ddw"}
        elif num == 503:
            self.name = {"String":"Axes", "Code":"1w3ddw"}
        elif num == 504:
            self.name = {"String":"Blunt", "Code":"1w4ddw"}
        elif num == 505:
            self.name = {"String":"Polearms", "Code":"1w7ddw"}
        elif num == 506:
            self.name = {"String":"Unarmed", "Code":"1w6ddw"}
        elif num == 507:
            self.name = {"String":"Bows", "Code":"1w3ddw"}
        elif num == 508:
            self.name = {"String":"Pistols", "Code":"1w6ddw"}
        elif num == 509:
            self.name = {"String":"Rifles", "Code":"1w5ddw"}
        elif num == 510:
            self.name = {"String":"Explosives", "Code":"1w9ddw"}
        elif num == 511:
            self.name = {"String":"Throwing", "Code":"1w7ddw"}
