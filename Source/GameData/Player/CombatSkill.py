import random
from GameData.Player.Skill import Skill

class CombatSkill(Skill):

    def __init__(self, num):
        Skill.__init__(self, num)
        
        self.skillGroup = "Basic" # Used As A Key For Player.combatSkillDict
        
        self.weaponTypeList = []
        self.weaponDataList = []
        self.offHandAttacks = True

        self.maxTargets = 1
        self.maxRange = 0

        self.healCheck = False
        self.onTarget = False

        self.stunUserOnBlock = False

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
            self.tickCount = 2

        elif num == 4: # Kick #
            self.name = {"String":"Kick", "Code":"4w"}
            self.skillGroup = "Melee"
            self.offHandAttacks = False
            self.stunUserOnBlock = True

        elif num == 5: # Punch #
            self.name = {"String":"Punch", "Code":"5w"}
            self.skillGroup = "Melee"
            self.weaponTypeList = [["Melee"]]
            self.stunUserOnBlock = True

        elif num == 6: # Jab #
            self.name = {"String":"Jab", "Code":"3w"}
            self.skillGroup = "Melee"
            self.weaponTypeList = [["Melee"]]
            self.offHandAttacks = False
            self.tickCount = 1

        # Sword (101 - 150) #
        elif num == 101:
            self.name = {"String":"Stab", "Code":"4w"}
            self.skillGroup = "Sword"
            self.weaponTypeList = [["Sword"]]
            self.stunUserOnBlock = True

        elif num == 102:
            self.name = {"String":"Slash", "Code":"5w"}
            self.skillGroup = "Sword"
            self.weaponTypeList = [["Sword"]]
            self.stunUserOnBlock = True

        # Dagger (151 - 200) #
        elif num == 151:
            self.name = {"String":"Stab", "Code":"4w"}
            self.skillGroup = "Dagger"
            self.weaponTypeList = [["Dagger"]]
            self.stunUserOnBlock = True

        elif num == 152:
            self.name = {"String":"Slash", "Code":"5w"}
            self.skillGroup = "Dagger"
            self.weaponTypeList = [["Dagger"]]
            self.stunUserOnBlock = True

        # Claws (201 - 250) #
        elif num == 201:
            self.name = {"String":"Slash", "Code":"5w"}
            self.skillGroup = "Claw"
            self.weaponTypeList = [["Claw"]]
            self.stunUserOnBlock = True

        # Axes (251 - 300) #
        elif num == 251:
            self.name = {"String":"Slash", "Code":"5w"}
            self.skillGroup = "Axe"
            self.weaponTypeList = [["Axe"]]
            self.stunUserOnBlock = True

        elif num == 252:
            self.name = {"String":"Bash", "Code":"4w"}
            self.skillGroup = "Axe"
            self.weaponTypeList = [["Axe"]]
            self.stunUserOnBlock = True

        elif num == 253:
            self.name = {"String":"Slash All", "Code":"9w"}
            self.skillGroup = "Axe"
            self.weaponTypeList = [["Axe"]]
            self.offHandAttacks = False
            self.stunUserOnBlock = True
            self.maxTargets = 3

        # Blunt (301 - 350) #
        elif num == 301:
            self.name = {"String":"Bash", "Code":"4w"}
            self.skillGroup = "Blunt"
            self.weaponTypeList = [["Blunt"]]
            self.stunUserOnBlock = True

        elif num == 302:
            self.name = {"String":"Smash", "Code":"5w"}
            self.skillGroup = "Blunt"
            self.weaponTypeList = [["Blunt"]]

        # Polearm (351 - 400) #
        elif num == 351:
            self.name = {"String":"Stab", "Code":"4w"}
            self.skillGroup = "Polearm"
            self.weaponTypeList = [["Polearm"]]
            self.stunUserOnBlock = True

        elif num == 352:
            self.name = {"String":"Slash", "Code":"5w"}
            self.skillGroup = "Polearm"
            self.weaponTypeList = [["Polearm"]]
            self.stunUserOnBlock = True

        # Shield (401 - 450) #
        elif num == 401:
            self.name = {"String":"Bash", "Code":"4w"}
            self.skillGroup = "Shield"
            self.weaponTypeList = [["Shield"]]
        
        # Bow (451 - 500) #
        elif num == 451:
            self.name = {"String":"Shoot", "Code":"5w"}
            self.skillGroup = "Bow"
            self.weaponTypeList = [["Bow"]]
            self.maxRange = 2

        # Pistol (501 - 550) #
        elif num == 501:
            self.name = {"String":"Shoot", "Code":"5w"}
            self.skillGroup = "Pistol"
            self.weaponTypeList = [["Pistol"]]
            self.maxRange = 2

        # Rifle (551 - 600) #
        elif num == 551:
            self.name = {"String":"Shoot", "Code":"5w"}
            self.skillGroup = "Rifle"
            self.weaponTypeList = [["Rifle"]]
            self.maxRange = 2

        elif num == 552:
            self.name = {"String":"Snipe", "Code":"5w"}
            self.skillGroup = "Rifle"
            self.ruleDict["From Another Room"] = True
            self.ruleDict["Requires Two-Handed Weapon"] = True
            self.weaponTypeList = [["Rifle"]]
            self.maxRange = 3
            self.offHandAttacks = False

        # Combined Skills (1000 - 2000) #
        elif num == 1000:
            self.name = {"String":"Bash", "Code":"4w"}
            self.skillGroup = None # ???
            self.stunUserOnBlock = True

        # Test Skills #
            # elif num == X:
            #     self.name = {"String":"Spin Fist", "Code":"9w"}
            #     self.skillGroup = "Melee"
            #     self.weaponTypeList = [["Melee"], ["Melee"]]
            #     self.maxTargets = "All"
            #     self.offHandAttacks = False
            #     self.stunUserOnBlock = True

            # elif num == X:
            #     self.name = {"String":"Slash All", "Code":"9w"}
            #     self.skillGroup = "Sword"
            #     self.weaponTypeList = [["Sword"]]
            #     self.ruleDict["All Only"] = True
            #     self.offHandAttacks = False
            #     self.stunUserOnBlock = True
            #     # self.maxTargets = "All" # Is Automatically Set Below

            # elif num == X:
            #     self.name = {"String":"Bullet Storm", "Code":"12w"}
            #     self.skillGroup = "Pistol"
            #     self.weaponTypeList = [["Pistol"]]
            #     self.ruleDict["All Only"] = True
            #     self.maxRange = 1
            #     self.offHandAttacks = False
            #     # self.maxTargets = "All" # Is Automatically Set Below

            # elif num == X:
            #     self.name = {"String":"Fireball", "Code":"8w"}
            #     self.skillGroup = "Offensive Magic"
            #     self.maxRange = 2

            # elif num == X:
            #     self.name = {"String":"Inferno", "Code":"7w"}
            #     self.skillGroup = "Offensive Magic"
            #     self.maxTargets = "All"
            #     self.maxRange = 1
            #     self.offHandAttacks = False

            # elif num == X:
            #     self.name = {"String":"Explosion", "Code":"9w"}
            #     self.skillGroup = "Offensive Magic"
            #     self.ruleDict["All Only"] = True
            #     self.maxRange = 1
            #     self.offHandAttacks = False
            #     # self.maxTargets = "All" # Is Automatically Set Below

            # elif num == X:
            #     self.name = {"String":"Pray", "Code":"4w"}
            #     self.skillGroup = "Healing Magic"
            #     self.maxRange = 1
            #     self.maxTargets = 1
            #     self.healCheck = True

            # elif num == X:
            #     self.name = {"String":"Bless", "Code":"5w"}
            #     self.skillGroup = "Healing Magic"
            #     self.ruleDict["All Only"] = True
            #     self.maxRange = 1
            #     self.healCheck = True
            #     # self.maxTargets = "All" # Is Automatically Set Below

            # Gear/Weapon Skill #
            # elif num == X:
            #     self.name = {"String":"Power Bash", "Code":"10w"}
            #     self.skillGroup = None
            #     self.ruleDict["Gear Num List"] = [10] # On A Shield Or Something
            #     self.stunUserOnBlock = True

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
