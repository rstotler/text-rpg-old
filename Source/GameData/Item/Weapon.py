from GameData.Player.CombatSkill import CombatSkill
from GameData.Item.Item import Item
from Components.Utility import *

class Weapon(Item):
    
    def __init__(self, num):
        Item.__init__(self, num)
        self.pocket = "Weapon"

        self.skillList = []

        self.weaponType = None
        self.twoHanded = False
        
        self.ranged = False
        self.ammoType = None
        self.shellCapacity = None
        self.magazine = None  # Guns with no magazine - Ammo Item Object, Guns with a magazine - Magazine Item Object

        self.loadWeapon(num)

    def loadWeapon(self, num):
        # Polearms Recieve A Natural Damage Boost When Single-Wielding #
        # Rifles are ALWAYS 2-Handed (Not Including Dual-Wield) #

        if num == 101:
            self.name = {"String":"Sword", "Code":"1w4ddw"}
            self.weaponType = "Sword"
        elif num == 102:
            self.name = {"String":"Shield", "Code":"1w5ddw"}
            self.weaponType = "Shield"
            self.skillList.append(CombatSkill(10))
        elif num == 103:
            self.name = {"String":"Lance", "Code":"1w4ddw"}
            self.weaponType = "Polearm"
        elif num == 104:
            self.name = {"String":"Greatsword", "Code":"1w9ddw"}
            appendKeyList(self.keyList, "great")
            self.weaponType = "Sword"
            self.twoHanded = True
        elif num == 105:
            self.prefix = "An"
            self.name = {"String":"Ebony Pistol", "Code":"1w5ddw1w5ddw"}
            self.weaponType = "Gun"
            self.ranged = True
            self.ammoType = ".45"
        elif num == 106:
            self.prefix = "An"
            self.name = {"String":"Ivory Pistol", "Code":"1w5ddw1w5ddw"}
            self.weaponType = "Gun"
            self.ranged = True
            self.ammoType = ".45"
        elif num == 107:
            self.name = {"String":"Sniper Rifle", "Code":"1w6ddw1w4ddw"}
            self.weaponType = "Gun"
            self.twoHanded = True
            self.ranged = True
            self.ammoType = "5.56"
        elif num == 108:
            self.name = {"String":"Rocket Launcher", "Code":"15w"}
            self.weaponType = "Gun"
            self.twoHanded = True
            self.ranged = True
            self.shellCapacity = 1
            self.ammoType = "Missile"
        elif num == 109:
            self.name = {"String":"Shotgun", "Code":"7w"}
            self.weaponType = "Gun"
            self.twoHanded = True
            self.ranged = True
            self.shellCapacity = 5
            self.ammoType = "12 Gauge"
        elif num == 110:
            self.name = {"String":"Dagger", "Code":"6w"}
            self.weaponType = "Dagger"
        elif num == 111:
            self.prefix = "An"
            self.name = {"String":"Axe", "Code":"3w"}
            self.weaponType = "Axe"
        elif num == 112:
            self.name = {"String":"Mace", "Code":"4w"}
            self.weaponType = "Blunt"
        elif num == 113:
            self.name = {"String":"Spear", "Code":"5w"}
            self.weaponType = "Polearm"
        elif num == 114:
            self.name = {"String":"Bow", "Code":"3w"}
            self.weaponType = "Bow"
        elif num == 115:
            self.name = {"String":"Grenade", "Code":"7w"}
            self.weaponType = "Explosive"
        elif num == 116:
            self.name = {"String":"Shurikan", "Code":"8w"}
            self.weaponType = "Throwable"

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

    def isLoaded(self, ammoList=[]):
        maxInventoryMagCapacity = -1
        if isinstance(ammoList, list) and len(ammoList) > 0:
            maxInventoryMagCapacity = 0
            for item in ammoList:
                if item.shellCapacity != None and item.ammoType == self.ammoType:
                    if item.shellCapacity > maxInventoryMagCapacity:
                        maxInventoryMagCapacity = item.shellCapacity

        if self.weaponType == "Gun":
            if self.shellCapacity != None and self.magazine != None:
                maxCapacity = self.shellCapacity
                if isinstance(ammoList, int) : maxCapacity = ammoList
                if self.magazine.quantity >= maxCapacity:
                    return True
            elif self.shellCapacity == None and self.magazine != None and "Ammo" in self.magazine.flags and self.magazine.flags["Ammo"] != None and maxInventoryMagCapacity <= self.magazine.shellCapacity:
                maxCapacity = self.magazine.shellCapacity
                if isinstance(ammoList, int) : maxCapacity = ammoList
                if self.magazine.flags["Ammo"].quantity >= maxCapacity:
                    return True
        return False

    def isEmpty(self, magazineCheck=False):
        if self.pocket == "Weapon":
            if self.shellCapacity != None:
                if self.magazine == None:
                    return True
            else:
                if self.magazine == None:
                    return True
                elif magazineCheck == True and self.magazine.flags["Ammo"] == None:
                    return True

        return False

    def getLoadedAmmo(self):
        if self.weaponType == "Gun":
            if self.shellCapacity != None:
                if self.magazine != None:
                    return self.magazine
            else:
                if self.magazine != None and "Ammo" in self.magazine.flags and self.magazine.flags["Ammo"] != None:
                    return self.magazine.flags["Ammo"]
        return None

    def getWeaponStatusString(self):
        statusString = ""
        statusCode = ""
        if self.ranged == True:
            if self.shellCapacity == None and self.magazine == None:
                statusString = " [Empty]"
                statusCode = "2y5w1y"
            else:
                if self.shellCapacity != None:
                    currentRounds = 0
                    if self.magazine != None:
                        currentRounds = self.magazine.quantity
                    maxRounds = self.shellCapacity
                else:
                    currentRounds = 0
                    if self.magazine.flags["Ammo"] != None:
                        currentRounds = self.magazine.flags["Ammo"].quantity
                    maxRounds = self.magazine.shellCapacity
                statusString += " [" + str(currentRounds) + "/" + str(maxRounds) + "]"
                statusCode += "2y" + str(len(str(currentRounds))) + "w1y" + str(len(str(maxRounds))) + "w1y"

        return statusString, statusCode

    def shoot(self):
        if self.shellCapacity != None:
            if self.magazine != None:
                self.magazine.quantity -= 1
                if self.magazine.quantity <= 0:
                    self.magazine = None
        else:
            if "Ammo" in self.magazine.flags and self.magazine.flags["Ammo"] != None:
                self.magazine.flags["Ammo"].quantity -= 1
                if self.magazine.flags["Ammo"].quantity <= 0:
                    self.magazine.flags["Ammo"] = None
