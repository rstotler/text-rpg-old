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
        self.onTarget = False

        self.knockDownCheck = False
        self.stunUserOnBlock = False

        self.disableCutLimb = False

        self.ruleDict = {}

        self.tickCount = 3

        self.loadCombatSkill(num)

    def loadCombatSkill(self, num):
        # "All Only" Skills Hit Everyone (Ignore Team Damage/Heal Enemies)

        # Basic Skills (1 - 100) #
        if num == 1: # Dodge #
            self.name = {"String":"Dodge", "Code":"5w"}
            self.tickCount = 2

        elif num == 2: # Block #
            self.name = {"String":"Block", "Code":"5w"}
            self.tickCount = 2

        elif num == 3: # Sweep #
            self.name = {"String":"Sweep", "Code":"5w"}
            self.offHandAttacks = False
            self.stunUserOnBlock = True
            self.tickCount = 2

        elif num == 4: # Kick #
            self.name = {"String":"Kick", "Code":"4w"}
            self.offHandAttacks = False
            self.stunUserOnBlock = True

        elif num == 5: # Punch #
            self.name = {"String":"Punch", "Code":"5w"}
            self.weaponTypeList = [["Melee"]]
            self.stunUserOnBlock = True

        elif num == 6: # Jab #
            self.name = {"String":"Jab", "Code":"3w"}
            self.weaponTypeList = [["Melee"]]
            self.offHandAttacks = False
            self.tickCount = 1

        # Sword (101 - 150) #

        # Dagger (151 - 200) #
        
        # Axes (201 - 250) #

        # Blunt (251 - 300) #
        elif num == 251: # Smash #
            self.name = {"String":"Smash", "Code":"5w"}
            self.weaponTypeList = [["Blunt"]]
            self.offHandAttacks = False
            self.knockDownCheck = True
            self.stunUserOnBlock = True

        # Polearm (301 - 350) #
        elif num == 301: # Stab #
            self.name = {"String":"Stab", "Code":"4w"}
            self.weaponTypeList = [["Polearm"]]
            self.maxRange = 1
            self.disableCutLimb = True

        elif num == 302: # Slash #
            self.name = {"String":"Slash", "Code":"5w"}
            self.weaponTypeList = [["Polearm"]]
            self.offHandAttacks = False
            self.stunUserOnBlock = True

        # Claws (351 - 400) #

        # Shield (401 - 450) #
        
        # Bow (451 - 500) #
        elif num == 451: # Shoot #
            self.name = {"String":"Shoot", "Code":"5w"}
            self.weaponTypeList = [["Bow"]]

        # Pistol (501 - 550) #
        elif num == 501: # Shoot #
            self.name = {"String":"Shoot", "Code":"5w"}
            self.weaponTypeList = [["Pistol"]]

        # Rifle (551 - 600) #
        elif num == 551: # Shoot #
            self.name = {"String":"Shoot", "Code":"5w"}
            self.weaponTypeList = [["Rifle"]]

        elif num == 552: # Snipe #
            self.name = {"String":"Snipe", "Code":"5w"}
            self.weaponTypeList = [["Rifle"]]
            self.ruleDict["From Another Room"] = True

        # Combined Skills (1001 - 2000) #
        elif num == 1001: # Stab #
            self.name = {"String":"Stab", "Code":"4w"}
            self.weaponTypeList = [["Sword", "Dagger"]]
            self.stunUserOnBlock = True
            self.disableCutLimb = True

        elif num == 1002: # Slash #
            self.name = {"String":"Slash", "Code":"5w"}
            self.weaponTypeList = [["Sword", "Dagger", "Axe", "Claw"]]
            self.stunUserOnBlock = True

        elif num == 1003: # Bash #
            self.name = {"String":"Bash", "Code":"4w"}
            self.weaponTypeList = [["Sword", "Dagger", "Axe", "Blunt", "Shield"]]
            self.offHandAttacks = False
            self.stunUserOnBlock = True

        # Test Skills #
            # elif num == X:
            #     self.name = {"String":"Explosion", "Code":"9w"}
            #     self.ruleDict["All Only"] = True
            #     self.maxRange = 1
            #     self.offHandAttacks = False
            #     # self.maxTargets = "All" # Is Automatically Set Below

            # elif num == X:
            #     self.name = {"String":"Pray", "Code":"4w"}
            #     self.maxRange = 1
            #     self.maxTargets = 1
            #     self.healCheck = True

            # elif num == X:
            #     self.name = {"String":"Bless", "Code":"5w"}
            #     self.ruleDict["All Only"] = True
            #     self.maxRange = 1
            #     self.healCheck = True
            #     # self.maxTargets = "All" # Is Automatically Set Below

            # Gear/Weapon Skill #
            # elif num == X:
            #     self.name = {"String":"Power Bash", "Code":"10w"}
            #     self.ruleDict["Gear Num List"] = [10] # On A Shield Or Something
            #     self.stunUserOnBlock = True

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
        elif len(self.weaponTypeList) == 1 and "Melee" in self.weaponTypeList[0]:
            self.weaponDataList = ["Melee"]
            return True
        elif len(self.weaponTypeList) == 2 and "Melee" in self.weaponTypeList[0] and "Melee" in self.weaponTypeList[1]:
            self.weaponDataList = ["Melee", "Melee"]
            return True
        elif len(self.weaponTypeList) == 1:
            if mainHandWeapon != None and mainHandWeapon.weaponType in self.weaponTypeList[0]:
                self.weaponDataList = [mainHandWeapon]
                return True
            elif offHandWeapon not in [None, "Unused"] and offHandWeapon.weaponType in self.weaponTypeList[0]:
                self.weaponDataList = [offHandWeapon]
                return True
        return False

    def attackModCheck(self, targetUser):
        enableSecondAttackCheck = False

        # 2-Handed Axe Slash Mod #
        if self.name["String"] == "Slash" and len(self.weaponDataList) > 0 and self.weaponDataList[0].weaponType == "Axe" and self.weaponDataList[0].twoHanded == True and (targetUser.gearDict[targetUser.getOppositeHand(targetUser.dominantHand)] == None or targetUser.gearDict[targetUser.dominantHand] == None):
            self.offHandAttacks = False
            self.maxTargets = 3
            self.ruleDict["All Only"] = True

        # Blunt/Shield Bash Mod #
        elif self.name["String"] == "Bash" and len(self.weaponDataList) > 0 and self.weaponDataList[0].weaponType in ["Blunt", "Shield"]:
            if self.offHandAttacks == False:
                enableSecondAttackCheck = True

            self.offHandAttacks = True
            self.stunUserOnBlock = False

        return enableSecondAttackCheck

    def ruleCheck(self, flags):
        if "Distance" in flags:
            if "From Another Room" in self.ruleDict and flags["Distance"] == 0:
                return False
            elif flags["Distance"] > self.maxRange and (len(self.weaponTypeList) == 0 or (len(self.weaponTypeList) > 0 and self.weaponTypeList[0] not in [["Bow"], ["Pistol"], ["Rifle"]])):
                return False

        if '"All" Attacks Disabled' in flags and "All Only" in self.ruleDict:
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
