import random

class Skill:

    def __init__(self, num):
        self.num = num
        self.name = {"String":"Debug Skill", "Code":"11w"}
        self.keyList = []
        
        self.weaponTypeList = []
        self.weaponDataList = []
        self.offHandAttacks = True

        self.maxTargets = 1
        self.maxRange = 0

        self.healCheck = False
        self.ruleDict = {}

        self.loadSkill(num)

    def loadSkill(self, num):

        # Combat #
        if num == 1:
            self.name = {"String":"Punch", "Code":"5w"}
            self.weaponTypeList = ["Open Hand"]
            self.offHandAttacks = False
        elif num == 2:
            self.name = {"String":"Spin Fist", "Code":"9w"}
            self.weaponTypeList = ["Open Hand", "Open Hand"]
            self.maxTargets = "All"
            self.offHandAttacks = False
        elif num == 3:
            self.name = {"String":"Fireball", "Code":"8w"}
            self.maxRange = 2
        elif num == 4:
            self.name = {"String":"Inferno", "Code":"7w"}
            self.maxTargets = "All"
            self.maxRange = 1
        elif num == 5:
            self.name = {"String":"Explosion", "Code":"9w"}
            self.ruleDict["All Only"] = True
            # self.maxTargets = "All" # Is Automatically Set Below
            self.maxRange = 1
            self.offHandAttacks = False
        elif num == 6:
            self.name = {"String":"Snipe", "Code":"5w"}
            self.ruleDict["From Another Room"] = True
            self.weaponTypeList = ["Gun"]
            self.maxRange = 2
            self.offHandAttacks = False
        elif num == 7:
            self.name = {"String":"Shoot", "Code":"5w"}
            self.weaponTypeList = ["Gun"]
            self.maxRange = 1
        elif num == 8:
            self.name = {"String":"Slash", "Code":"5w"}
            self.weaponTypeList = ["Sword"]
        elif num == 9:
            self.name = {"String":"Slash All", "Code":"9w"}
            self.weaponTypeList = ["Sword"]
            self.ruleDict["All Only"] = True
            # self.maxTargets = "All" # Is Automatically Set Below
        elif num == 10:
            self.name = {"String":"Bash", "Code":"4w"}
            self.ruleDict["Gear Num List"] = [102]
            self.ruleDict["r"] = random.randrange(8888)
        elif num == 11:
            self.name = {"String":"Pray", "Code":"4w"}
            self.maxTargets = "All"
            self.healCheck = True

        if "All Only" in self.ruleDict:
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
        
    def weaponCheck(self, mainHandWeapon, offHandWeapon="Unused"):
        if len(self.weaponTypeList) == 0:
            if mainHandWeapon == None : self.weaponDataList = ["Open Hand"]
            else : self.weaponDataList = [mainHandWeapon]
            return True
        elif len(self.weaponTypeList) == 1 and self.weaponTypeList[0] == "Open Hand":
            self.weaponDataList = ["Open Hand"]
            return True
        elif len(self.weaponTypeList) == 2 and self.weaponTypeList[0] == "Open Hand" and self.weaponTypeList[1] == "Open Hand":
            self.weaponDataList = ["Open Hand", "Open Hand"]
            return True
        elif len(self.weaponTypeList) == 1:
            if mainHandWeapon != None and mainHandWeapon.weaponType == self.weaponTypeList[0]:
                self.weaponDataList = [mainHandWeapon]
            elif offHandWeapon not in [None, "Unused"] and offHandWeapon.weaponType == self.weaponTypeList[0]:
                self.weaponDataList = [offHandWeapon]
            return True

        return False

    def ruleCheck(self, distance=None):
        if "From Another Room" in self.ruleDict and distance != None and distance == 0:
            return False
        elif distance != None and distance > self.maxRange:
            return False
        return True

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
        if len(combatSkill.weaponTypeList) == 0:
            return True
        elif len(combatSkill.weaponTypeList) == 1 and combatSkill.weaponTypeList == ["Open Hand"]:
            if target.gearDict["Left Hand"] == None or target.gearDict["Right Hand"] == None:
                if not (target.debugDualWield == False and target.gearDict[target.dominantHand] != None and target.gearDict[target.dominantHand].twoHanded == True):
                    return True
        elif len(combatSkill.weaponTypeList) == 2 and combatSkill.weaponTypeList == ["Open Hand", "Open Hand"]:
            if target.gearDict["Left Hand"] == None and target.gearDict["Right Hand"] == None:
                return True
        elif len(combatSkill.weaponTypeList) == 1 and ((target.gearDict["Left Hand"] != None and combatSkill.weaponTypeList[0] == target.gearDict["Left Hand"].weaponType) or (target.gearDict["Right Hand"] != None and combatSkill.weaponTypeList[0] == target.gearDict["Right Hand"].weaponType)):
            return True

        return False
