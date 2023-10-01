class Skill:

    def __init__(self, num):
        self.num = num
        self.name = {"String":"Debug Skill", "Code":"11w"}
        self.keyList = []

        self.defaultTarget = "Enemies"
        self.maxTargets = 1
        self.maxRange = 0
        self.ruleList = []

        self.loadSkill(num)

    def loadSkill(self, num):

        # Combat #
        if num == 1:
            self.name = {"String":"Punch", "Code":"5w"}
            self.ruleList.append("Requires An Open Hand")
        elif num == 2:
            self.name = {"String":"Spin Fist", "Code":"9w"}
            self.ruleList.append("Requires Two Open Hands")
            self.maxTargets = "All"
        elif num == 3:
            self.name = {"String":"Fireball", "Code":"8w"}
            self.maxRange = 2
        elif num == 4:
            self.name = {"String":"Inferno", "Code":"7w"}
            self.maxTargets = "All"
            self.maxRange = 1
        elif num == 5:
            self.name = {"String":"Explosion", "Code":"9w"}
            self.ruleList.append("All Only")
            self.maxTargets = "All" # Is Automatically Set Below
            self.maxRange = 1
        elif num == 6:
            self.name = {"String":"Snipe", "Code":"5w"}
            self.ruleList.append("From Another Room")
            self.maxRange = 1
        elif num == 7:
            self.name = {"String":"Shoot", "Code":"5w"}
            self.ruleList.append("Requires A Gun")
        elif num == 8:
            self.name = {"String":"Pray", "Code":"4w"}
            self.defaultTarget = "Group"
            self.maxTargets = "All"

        if "All Only" in self.ruleList:
            self.maxTargets = "All"

        # Create Key List #
        nameStringList = self.name["String"].lower().split()
        for i in range(len(nameStringList)):
            word = nameStringList[i]
            phrase = ' '.join(nameStringList[0:i + 1])
            self.keyList.append(phrase)

            for cNum in range(len(word)):
                if (cNum > 0 or i > 0) and cNum != len(word) - 1:
                    s = 0
                    if i > 0:
                        s += len(' '.join(nameStringList[0:i])) + 1
                    self.keyList.append(phrase[0:s + cNum + 1])
        
    @staticmethod
    def parseSkillString(inputString, skillList):
        for i in range(len(inputString.split())):
            if i == 0:
                phrase = inputString
            else:
                phrase = ' '.join(inputString.split()[0:-i])
            for skill in skillList:
                if phrase in skill.keyList:
                    return skill, ' '.join(inputString.split()[len(inputString.split()) - i::])
        return None, None

    @staticmethod
    def skillAvailableCheck(target, combatSkill):
        if "Requires An Open Hand" in combatSkill.ruleList:
            if target.gearDict["Left Hand"] != None and target.gearDict["Right Hand"] != None:
                return False
        if "Requires Two Open Hands" in combatSkill.ruleList:
            if target.gearDict["Left Hand"] != None or target.gearDict["Right Hand"] != None:
                return False
        if "Requires A Gun" in combatSkill.ruleList:
            if (target.gearDict["Left Hand"] == None or target.gearDict["Left Hand"].ranged == False) or \
            (target.gearDict["Right Hand"] == None or target.gearDict["Right Hand"].ranged == False):
                return False

        return True
