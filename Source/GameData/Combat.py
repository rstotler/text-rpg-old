import random
from GameData.Item.Item import Item

class Combat:

    @staticmethod
    def hitCheck(attackDisplayList, user, attackSkill, target, targetRoom, roundNum):

        # Miss Attack #
        hitChance = 4
        if roundNum == 0 and target.getCombatAction() != None and target.getCombatAction().name["String"] == "Dodge":
            hitChance = 1
        elif roundNum == 0 and target.getCombatAction() != None and target.getCombatAction().name["String"] == "Block":
            hitChance = None # 100% Hit-Rate
            attackDisplayList["Block Check"] = True
        elif len(target.actionList) > 0 and target.actionList[0].actionType in ["Stun", "Stumble"]:
            hitChance = None # 100% Hit-Rate

        if hitChance != None and attackSkill.healCheck == False and random.randrange(hitChance) == 0:
            if len(attackSkill.weaponDataList) == 0:
                attackDisplayList["Miss Check"] = "Miss Attack"
                attackDisplayList["Weapon Data List"] = "Non-Weapon Attack"
            elif len(attackSkill.weaponDataList) == 2:
                attackDisplayList["Miss Check"] = "Miss Attack"
                attackDisplayList["Weapon Data List"] = attackSkill.weaponDataList
            elif len(attackSkill.weaponDataList) == 1:
                attackDisplayList["Miss Check"] = "Miss Attack"
                attackDisplayList["Weapon Data List"] = [attackSkill.weaponDataList[0]]

            return False, attackDisplayList

        # Hit Attack #
        if "Block Check" not in attackDisplayList and attackSkill.healCheck == False:
            target.currentHealth -= 1
            attackDisplayList["Attack Damage"] = 1

            # Cut Off Limb #
            if target.num != None and attackSkill.cutLimbPercent != None and attackSkill.cutLimbPercent > 0:
                if len(target.cutLimbList) == 0 and random.randrange(100) + 1 <= attackSkill.cutLimbPercent:
                    limbList = ["Left Arm", "Left Arm", "Right Arm", "Right Arm", "Head"]
                    targetLimb = random.choice(limbList)
                    target.cutLimbList.append(targetLimb)
                    limbItem = Item.createBodyPart(target, targetLimb)
                    targetRoom.itemList.append(limbItem)
                    attackDisplayList["Cut Limb"] = targetLimb
                    if targetLimb == "Head":
                        attackDisplayList["Attack Damage"] = target.currentHealth + attackDisplayList["Attack Damage"]
                    else:
                        if targetLimb.split()[0] == "Left" : targetGearSlot = "Left Hand"
                        else : targetGearSlot = "Right Hand"
                        if target.gearDict[targetGearSlot] != None:
                            attackDisplayList["Cut Limb Weapon"] = target.gearDict[targetGearSlot]
                            targetRoom.itemList.append(target.gearDict[targetGearSlot])
                            target.gearDict[targetGearSlot] = None

                        # Opposite Hand 2-Handed Weapon Check #
                        oppositeHandWeapon = target.gearDict[target.getOppositeHand(targetGearSlot)]
                        if oppositeHandWeapon != None and oppositeHandWeapon.twoHanded == True and target.debugDualWield == False:
                            targetRoom.itemList.append(oppositeHandWeapon)
                            attackDisplayList["Return Weapon To Inventory"] = oppositeHandWeapon
                            target.gearDict[target.getOppositeHand(targetGearSlot)] = None

        # Heal Attack #
        elif attackSkill.healCheck == True:
            target.currentHealth += 1
            attackDisplayList["Attack Damage"] = 1

        return True, attackDisplayList
