from GameData.Player.CombatSkill import CombatSkill
from GameData.Item.Item import Item
from Components.Utility import *

class Weapon(Item):
    
    def __init__(self, num):
        Item.__init__(self, num, False)
        self.pocket = "Weapon"

        self.skillList = []

        self.weaponType = None
        self.twoHanded = False

        self.cutLimbPercent = 0
        
        self.ammoType = None
        self.ammoCapacity = None
        self.magazine = None  # Guns with no magazine - Ammo Item Object, Guns with a magazine - Magazine Item Object

        self.loadWeapon(num)

    def loadWeapon(self, num):
        # Polearms Recieve A Natural Damage Boost When Single-Wielding #
        # Rifles are ALWAYS 2-Handed (Not Including Dual-Wield) #

        if num == 1:
            self.name = {"String":"Sword", "Code":"1w4ddw"}
            self.weaponType = "Sword"

        elif num == 2:
            self.name = {"String":"Greatsword", "Code":"1w9ddw"}
            appendKeyList(self.keyList, "great")
            self.weaponType = "Sword"
            self.twoHanded = True

        elif num == 3:
            self.name = {"String":"Dagger", "Code":"6w"}
            self.weaponType = "Dagger"

        elif num == 4:
            self.name = {"String":"Claws", "Code":"5w"}
            self.weaponType = "Claw"

        elif num == 5:
            self.prefix = "An"
            self.name = {"String":"Axe", "Code":"3w"}
            self.weaponType = "Axe"

        elif num == 6:
            self.name = {"String":"Battle Axe", "Code":"10w"}
            self.weaponType = "Axe"

        elif num == 7:
            self.name = {"String":"Mace", "Code":"4w"}
            self.weaponType = "Blunt"

        elif num == 8:
            self.name = {"String":"Spear", "Code":"5w"}
            self.weaponType = "Polearm"

        elif num == 9:
            self.name = {"String":"Halberd", "Code":"7w"}
            self.weaponType = "Polearm"

        elif num == 10:
            self.name = {"String":"Shield", "Code":"1w5ddw"}
            self.weaponType = "Shield"
            # self.skillList.append(CombatSkill(X))

        elif num == 11:
            self.name = {"String":"Bow", "Code":"3w"}
            self.weaponType = "Bow"

        elif num == 12:
            self.prefix = "An"
            self.name = {"String":"Ebony Pistol", "Code":"1w5ddw1w5ddw"}
            self.weaponType = "Pistol"
            self.ammoType = ".45"

        elif num == 13:
            self.prefix = "An"
            self.name = {"String":"Ivory Pistol", "Code":"1w5ddw1w5ddw"}
            self.weaponType = "Pistol"
            self.ammoType = ".45"

        elif num == 14:
            self.name = {"String":"Sniper Rifle", "Code":"1w6ddw1w4ddw"}
            self.weaponType = "Rifle"
            self.twoHanded = True
            self.ammoType = "5.56"

        elif num == 15:
            self.name = {"String":"Shotgun", "Code":"7w"}
            self.weaponType = "Rifle"
            self.twoHanded = True
            self.ammoCapacity = 5
            self.ammoType = "12 Gauge"

        elif num == 16:
            self.name = {"String":"Rocket Launcher", "Code":"15w"}
            self.weaponType = "Rifle"
            self.twoHanded = True
            self.ammoCapacity = 1
            self.ammoType = "Missile"

        elif num == 17:
            self.name = {"String":"Shurikan", "Code":"8w"}
            self.weaponType = "Throwable"

        elif num == 18:
            self.name = {"String":"Grenade", "Code":"7w"}
            self.weaponType = "Explosive"

        elif num == 19:
            self.name = {"String":"Staff", "Code":"5w"}
            self.weaponType = "Staves"

        # Create Key List #
        appendKeyList(self.keyList, self.name["String"].lower())
        for word in self.name["String"].lower().split():
            if '-' in word:
                for subword in word.split('-'):
                    if subword not in self.keyList:
                        self.keyList.append(subword)
                if word.replace('-', ' ').strip() not in self.keyList:
                    self.keyList.append(word.replace('-', ' ').strip())

        if "Code" not in self.name:
            self.name["Code"] = str(len(self.name["String"])) + "w"
        if "Code" not in self.roomDescription:
            self.roomDescription["Code"] = str(len(self.roomDescription["String"])) + "w"

    def isRanged(self):
        if self.weaponType in ["Pistol", "Rifle", "Bow", "Throwable"]:
            return True
        return False

    def isLoaded(self, ammoList=[]):
        maxInventoryMagCapacity = -1
        if isinstance(ammoList, list) and len(ammoList) > 0:
            maxInventoryMagCapacity = 0
            for item in ammoList:
                if item.ammoCapacity != None and item.ammoType == self.ammoType:
                    if item.ammoCapacity > maxInventoryMagCapacity:
                        maxInventoryMagCapacity = item.ammoCapacity

        if self.weaponType in ["Pistol", "Rifle"]:
            if self.ammoCapacity != None and self.magazine != None:
                maxCapacity = self.ammoCapacity
                if isinstance(ammoList, int) : maxCapacity = ammoList
                if self.magazine.quantity >= maxCapacity:
                    return True
            elif self.ammoCapacity == None and self.magazine != None and "Ammo" in self.magazine.flags and self.magazine.flags["Ammo"] != None and maxInventoryMagCapacity <= self.magazine.ammoCapacity:
                maxCapacity = self.magazine.ammoCapacity
                if isinstance(ammoList, int) : maxCapacity = ammoList
                if self.magazine.flags["Ammo"].quantity >= maxCapacity:
                    return True
        return False

    def isEmpty(self, magazineCheck=False):
        if self.pocket == "Weapon":
            if self.ammoCapacity != None:
                if self.magazine == None:
                    return True
            else:
                if self.magazine == None:
                    return True
                elif magazineCheck == True and self.magazine.flags["Ammo"] == None:
                    return True

        return False

    def getLoadedAmmo(self):
        if self.weaponType in ["Pistol", "Rifle"]:
            if self.ammoCapacity != None:
                if self.magazine != None:
                    return self.magazine
            else:
                if self.magazine != None and "Ammo" in self.magazine.flags and self.magazine.flags["Ammo"] != None:
                    return self.magazine.flags["Ammo"]
        return None

    def getWeaponStatusString(self):
        statusString = ""
        statusCode = ""
        if self.isRanged():
            if self.ammoCapacity == None and self.magazine == None:
                statusString = " [Empty]"
                statusCode = "2y5w1y"
            else:
                if self.ammoCapacity != None:
                    currentRounds = 0
                    if self.magazine != None:
                        currentRounds = self.magazine.quantity
                    maxRounds = self.ammoCapacity
                else:
                    currentRounds = 0
                    if self.magazine.flags["Ammo"] != None:
                        currentRounds = self.magazine.flags["Ammo"].quantity
                    maxRounds = self.magazine.ammoCapacity
                statusString += " [" + str(currentRounds) + "/" + str(maxRounds) + "]"
                statusCode += "2y" + str(len(str(currentRounds))) + "w1y" + str(len(str(maxRounds))) + "w1y"

        return statusString, statusCode

    def shoot(self):
        if self.ammoCapacity != None:
            if self.magazine != None:
                self.magazine.quantity -= 1
                if self.magazine.quantity <= 0:
                    self.magazine = None
        else:
            if "Ammo" in self.magazine.flags and self.magazine.flags["Ammo"] != None:
                self.magazine.flags["Ammo"].quantity -= 1
                if self.magazine.flags["Ammo"].quantity <= 0:
                    self.magazine.flags["Ammo"] = None
