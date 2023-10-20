import random
from GameData.Player.Skill import Skill

class CombatSkill(Skill):

    def __init__(self, num):
        Skill.__init__(self, num)
        
        self.weaponTypeList = []
        self.weaponDataList = []
        self.offHandAttacks = True

        self.maxTargets = 1
        self.maxRange = 0

        self.healCheck = False
        self.cutLimbPercent = None
        self.onTarget = False

        self.canBeStunned = False

        self.ruleDict = {}

        self.loadCombatSkill(num)

    def loadCombatSkill(self, num):

        # Combat (1 - 500) #
        # "All Only" Skills Hit Everyone (Ignore Team Damage/Heal Enemies)
        if num == 1:
            self.name = {"String":"Punch", "Code":"5w"}
            self.weaponTypeList = [["Open Hand"]]
            self.canBeStunned = True
        elif num == 2:
            self.name = {"String":"Spin Fist", "Code":"9w"}
            self.weaponTypeList = [["Open Hand"], ["Open Hand"]]
            self.maxTargets = "All"
            self.offHandAttacks = False
            self.canBeStunned = True
        elif num == 3:
            self.name = {"String":"Fireball", "Code":"8w"}
            self.maxRange = 2
            self.cutLimbPercent = 5
        elif num == 4:
            self.name = {"String":"Inferno", "Code":"7w"}
            self.maxTargets = "All"
            self.maxRange = 1
            self.offHandAttacks = False
        elif num == 5:
            self.name = {"String":"Explosion", "Code":"9w"}
            self.ruleDict["All Only"] = True
            self.maxRange = 1
            self.offHandAttacks = False
            self.cutLimbPercent = 20
            # self.maxTargets = "All" # Is Automatically Set Below
        elif num == 6:
            self.name = {"String":"Snipe", "Code":"5w"}
            self.ruleDict["From Another Room"] = True
            self.ruleDict["Requires Two-Handed Weapon"] = True
            self.weaponTypeList = [["Gun"]]
            self.maxRange = 3
            self.offHandAttacks = False
        elif num == 7:
            self.name = {"String":"Shoot", "Code":"5w"}
            self.weaponTypeList = [["Gun"]]
            self.maxRange = 2
        elif num == 8:
            self.name = {"String":"Slash", "Code":"5w"}
            self.weaponTypeList = [["Sword", "Dagger", "Axe"]]
            self.cutLimbPercent = 10
            self.canBeStunned = True
        elif num == 9:
            self.name = {"String":"Slash All", "Code":"9w"}
            self.weaponTypeList = [["Sword", "Axe"]]
            self.ruleDict["All Only"] = True
            self.offHandAttacks = False
            self.cutLimbPercent = 5
            self.canBeStunned = True
            # self.maxTargets = "All" # Is Automatically Set Below
        elif num == 10:
            self.name = {"String":"Bash", "Code":"4w"}
            self.ruleDict["Gear Num List"] = [102]
            self.canBeStunned = True
        elif num == 11:
            self.name = {"String":"Pray", "Code":"4w"}
            self.maxTargets = 1
            self.healCheck = True
        elif num == 12:
            self.name = {"String":"Bless", "Code":"5w"}
            self.ruleDict["All Only"] = True
            self.maxRange = 1
            self.healCheck = True
            # self.maxTargets = "All" # Is Automatically Set Below
        elif num == 13:
            self.name = {"String":"Bullet Storm", "Code":"12w"}
            self.weaponTypeList = [["Gun"]]
            self.ruleDict["All Only"] = True
            self.maxRange = 1
            self.offHandAttacks = False
            # self.maxTargets = "All" # Is Automatically Set Below
        elif num == 14:
            self.name = {"String":"Block", "Code":"5w"}
        elif num == 15:
            self.name = {"String":"Dodge", "Code":"5w"}

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
                    if not (phrase[0:s + cNum + 1][-2] == ' '):
                        self.keyList.append(phrase[0:s + cNum + 1])
        if self.name["String"].lower().replace(' ', '') not in self.keyList:
            self.keyList.append(self.name["String"].lower().replace(' ', ''))
        
    def weaponAttackCheck(self, mainHandWeapon, offHandWeapon="Unused"):
        # Checks For Skills That Require Two Weapons Don't Exist Yet! #

        self.weaponDataList = []
        if "Gear Num List" in self.ruleDict:
            if self in mainHandWeapon.skillList:
                self.weaponDataList = [mainHandWeapon]
                return True
            elif offHandWeapon != "Unused" and self in offHandWeapon.skillList:
                self.weaponDataList = [offHandWeapon]
                return True
            return False
        elif len(self.weaponTypeList) == 0:
            return True
        elif len(self.weaponTypeList) == 1 and "Open Hand" in self.weaponTypeList[0]:
            self.weaponDataList = ["Open Hand"]
            return True
        elif len(self.weaponTypeList) == 2 and "Open Hand" in self.weaponTypeList[0] and "Open Hand" in self.weaponTypeList[1]:
            self.weaponDataList = ["Open Hand", "Open Hand"]
            return True
        elif len(self.weaponTypeList) == 1:
            if mainHandWeapon != None and mainHandWeapon.weaponType in self.weaponTypeList[0]:
                self.weaponDataList = [mainHandWeapon]
            elif offHandWeapon not in [None, "Unused"] and offHandWeapon.weaponType in self.weaponTypeList[0]:
                self.weaponDataList = [offHandWeapon]
            return True
        return False

    def ruleCheck(self, flags):
        if "Distance" in flags:
            if "From Another Room" in self.ruleDict and flags["Distance"] == 0:
                return False
            elif flags["Distance"] > self.maxRange:
                return False

        if '"All" Attacks Disabled' in flags and "All Only" in self.ruleDict:
            return False

        if "Disable Two-Handed Attacks" in flags and "Requires Two-Handed Weapon" in self.ruleDict:
            return False

        if "Disable No Off-Hand Attack Attacks" in flags and self.offHandAttacks == False:
            return False

        if "Disable Healing" in flags and self.healCheck == True:
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
