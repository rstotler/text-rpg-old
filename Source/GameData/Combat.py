import random

class Combat:

    @staticmethod
    def hitCheck(user, attackSkill, target):
        if random.randrange(4) == 0:
            dataDict = {}
            if len(attackSkill.weaponDataList) == 0:
                dataDict["Miss Check"] = "Miss Attack"
                dataDict["Weapon Data List"] = "Non-Weapon Attack"
            elif len(attackSkill.weaponDataList) == 2:
                dataDict["Miss Check"] = "Miss Attack"
                dataDict["Weapon Data List"] = attackSkill.weaponDataList
            elif len(attackSkill.weaponDataList) == 1:
                if attackSkill.weaponDataList[0] != "Open Hand" and attackSkill.weaponDataList[0].weaponType == "Gun":
                    dataDict["Miss Check"] = "Miss Attack"
                else:
                    dataDict["Miss Check"] = "Miss Attack"
                dataDict["Weapon Data List"] = [attackSkill.weaponDataList[0]]

            return False, dataDict

        target.currentHealth -= 100
        return True, None
