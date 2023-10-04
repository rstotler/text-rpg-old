import copy

class Action:

    def __init__(self, actionType, flags):
        self.actionType = actionType
        self.flags = flags
        
        self.currentTick = 0
        self.maxTick = 2

    def update(self, console, target):
        self.currentTick += 1
        if self.currentTick >= self.maxTick:
            if self.actionType == "Reload":
                self.completeReload(console, target)
            elif self.actionType == "Unload":
                self.completeUnload(console, target)

    def completeReload(self, console, target):
        magazineCheck = False
        reloadCount = 0
        reloadWeapon = None
        requireWeapon = None

        reloadList = self.flags["Reload List"]
        reloadKey = self.flags["Reload Key"]
        ammoKey = self.flags["Ammo Key"]
        reloadTargetShiftCheck = self.flags["Reload Target Shift Check"]

        for weaponIndex, weapon in enumerate(reloadList):
            ammoCheck = False
            targetAmmo = None
            targetMagazine = None
            ammoIndex = -1
            reloadQuantity = 0
            targetMagazine = None
            heldMagazineCheck = False

            # Non-Magazine Weapons #
            if weapon.shellCapacity != None:
                targetAmmo, ammoIndex = target.ammoCheck(weapon.ammoType)
                if ammoKey != None:
                    targetAmmo, ammoIndex = target.ammoCheck(weapon.ammoType, ammoKey)
                elif reloadTargetShiftCheck == True:
                    targetAmmo, ammoIndex = target.ammoCheck(weapon.ammoType, reloadKey)

                if weapon.magazine == None or weapon.magazine.quantity < weapon.shellCapacity or (targetAmmo != None and weapon.magazine.num != targetAmmo.num):
                    if ammoIndex != -1 and not (reloadKey == "All" and ammoKey == None and weapon.magazine != None and weapon.magazine.num != targetAmmo.num):
                        if weapon.magazine != None and weapon.magazine.num != targetAmmo.num:
                            inventoryAmmo, unused = target.getTargetItem(weapon.magazine.num, ["Inventory"])
                            if inventoryAmmo != None:
                                inventoryAmmo.quantity += weapon.magazine.quantity
                            else:
                                target.itemDict["Ammo"].append(weapon.magazine)
                            weapon.magazine = None

                        alreadyLoadedCount = 0
                        if weapon.magazine != None:
                            alreadyLoadedCount = weapon.magazine.quantity
                        reloadQuantity = weapon.shellCapacity - alreadyLoadedCount
                        if reloadQuantity > targetAmmo.quantity:
                            reloadQuantity = targetAmmo.quantity
                        if weapon.magazine == None:
                            splitItem = copy.deepcopy(targetAmmo)
                            splitItem.quantity = reloadQuantity
                            weapon.magazine = splitItem
                        else:
                            weapon.magazine.quantity += reloadQuantity
                        ammoCheck = True
                        magazineCheck = None
                        reloadCount += 1
                        if reloadWeapon == None:
                            reloadWeapon = weapon
                        elif reloadWeapon != "Multiple" and reloadWeapon.num != weapon.num:
                            reloadWeapon = "Multiple"

            # Magazine Weapons #
            else:
                targetMagazine, magazineIndex = target.ammoCheck(weapon.ammoType, None, True)
                if magazineIndex != -1:
                    magazineCheck = True
                else:
                    requireWeapon = weapon
                if weapon.magazine != None or magazineIndex != -1:
                    targetAmmo, ammoIndex = target.ammoCheck(weapon.ammoType)
                    if ammoKey != None:
                        targetAmmo, ammoIndex = target.ammoCheck(weapon.ammoType, ammoKey)
                    elif reloadTargetShiftCheck == True:
                        targetAmmo, ammoIndex = target.ammoCheck(weapon.ammoType, reloadKey)

                    if ammoIndex != -1 and not (reloadKey == "All" and ammoKey == None and weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and weapon.magazine.flags["Ammo"].num != targetAmmo.num):
                        if weapon.magazine == None or weapon.magazine.flags["Ammo"] == None or weapon.magazine.flags["Ammo"].quantity < weapon.magazine.shellCapacity or weapon.isLoaded(target.itemDict["Ammo"]) == False or (targetAmmo != None and weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and targetAmmo.num != weapon.magazine.flags["Ammo"].num):
                            weaponMagazine = weapon.magazine
                            if weaponMagazine == None:
                                weaponMagazine = targetMagazine
                                heldMagazineCheck = True
                            elif weaponMagazine != None and targetMagazine != None and weaponMagazine.shellCapacity < targetMagazine.shellCapacity:
                                target.itemDict["Ammo"].append(weaponMagazine)
                                if weaponMagazine.flags["Ammo"] != None:
                                    heldAmmo, unused = target.getTargetItem(weaponMagazine.flags["Ammo"].num, ["Inventory"])
                                    if heldAmmo != None:
                                        heldAmmo.quantity += weaponMagazine.flags["Ammo"].quantity
                                    else:
                                        target.itemDict["Ammo"].append(weaponMagazine.flags["Ammo"])
                                    weaponMagazine.flags["Ammo"] = None
                                weaponMagazine = targetMagazine

                            if weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and weapon.magazine.flags["Ammo"].num != targetAmmo.num:
                                inventoryAmmo, unused = target.getTargetItem(weapon.magazine.flags["Ammo"].num, ["Inventory"])
                                if inventoryAmmo != None:
                                    inventoryAmmo.quantity += weapon.magazine.flags["Ammo"].quantity
                                else:
                                    target.itemDict["Ammo"].append(weapon.magazine.flags["Ammo"])
                                weapon.magazine.flags["Ammo"] = None
                                
                            alreadyLoadedCount = 0
                            if weaponMagazine.flags["Ammo"] != None:
                                alreadyLoadedCount = weaponMagazine.flags["Ammo"].quantity
                            reloadQuantity = weaponMagazine.shellCapacity - alreadyLoadedCount
                            if reloadQuantity > targetAmmo.quantity:
                                reloadQuantity = targetAmmo.quantity
                            if weaponMagazine.flags["Ammo"] == None:
                                splitItem = copy.deepcopy(targetAmmo)
                                splitItem.quantity = reloadQuantity
                                weaponMagazine.flags["Ammo"] = splitItem
                            else:
                                weaponMagazine.flags["Ammo"].quantity += reloadQuantity
                                
                            weapon.magazine = weaponMagazine
                            ammoCheck = True
                            reloadCount += 1
                            if reloadWeapon == None:
                                reloadWeapon = weapon
                            elif reloadWeapon.num != weapon.num:
                                reloadWeapon = "Multiple"

            if targetAmmo != None:
                if reloadQuantity >= targetAmmo.quantity:
                    del target.itemDict["Ammo"][ammoIndex]
                else:
                    targetAmmo.quantity -= reloadQuantity
            if targetMagazine != None and ammoCheck == True and heldMagazineCheck == True:
                if targetMagazine in target.itemDict["Ammo"]:
                    magazineIndex = target.itemDict["Ammo"].index(targetMagazine)
                    del target.itemDict["Ammo"][magazineIndex]

        if reloadWeapon != "Multiple":
            displayString = "You finish reloading " + reloadWeapon.prefix.lower() + " " + reloadWeapon.name["String"] + "."
            displayCode = "21w" + str(len(reloadWeapon.prefix)) + "w1w" + reloadWeapon.name["Code"] + "1y"
            countString = ""
            countCode = ""
            if reloadCount > 1:
                countString = " (" + str(reloadCount) + ")"
                countCode = "2r" + str(len(str(reloadCount))) + "w1y"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":displayString + countString, "Code":displayCode + countCode})
        else:
            displayString = "You finish reloading."
            displayCode = "20w1y"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":displayString, "Code":displayCode})
        
    def completeUnload(self, console, target):
        unloadWeapon = None
        unloadCount = 0
        targetAmmo = None
        targetMagazine = None
        magazineCount = 0
        shellCount = 0

        unloadList = self.flags["Unload List"]
        ammoKey = self.flags["Ammo Key"]
        roomItem = self.flags["Room Item"]

        for weaponIndex, weapon in enumerate(unloadList):
            
            # Non-Magazine Weapons #
            if weapon.shellCapacity != None and weapon.magazine != None:
                if not (ammoKey != None and ammoKey not in weapon.magazine.keyList):
                    getQuantity = weapon.magazine.quantity
                    if roomItem != None and target.getWeight() + roomItem.getWeight() > target.getMaxWeight():
                        getQuantity = 0
                        if target.getWeight() + roomItem.getWeight(False) <= target.getMaxWeight():
                            getQuantity = int((target.getMaxWeight() - target.getWeight()) / roomItem.getWeight(False))

                    if getQuantity > 0:
                        shellCount += getQuantity
                        inventoryAmmo, unused = target.getTargetItem(weapon.magazine.num, ["Inventory"])
                        if inventoryAmmo != None:
                            inventoryAmmo.quantity += getQuantity
                        else:
                            splitItem = copy.deepcopy(weapon.magazine)
                            splitItem.quantity = getQuantity
                            target.itemDict["Ammo"].append(splitItem)
                        targetAmmo = weapon.magazine
                        if getQuantity == weapon.magazine.quantity:
                            weapon.magazine = None
                        else:
                            weapon.magazine.quantity -= getQuantity

                        if unloadWeapon == None:
                            unloadWeapon = weapon
                        elif unloadWeapon != "Multiple" and unloadWeapon.num != weapon.num:
                            unloadWeapon = "Multiple"
                        unloadCount += 1

            # Magazine Weapons #
            elif weapon.magazine != None:
                if not (ammoKey != None and weapon.magazine.flags["Ammo"] != None and ammoKey not in weapon.magazine.flags["Ammo"].keyList):
                    getQuantity = 0
                    if weapon.magazine.flags["Ammo"] != None:
                        getQuantity = weapon.magazine.flags["Ammo"].quantity
                    if roomItem != None and weapon.magazine.flags["Ammo"] != None and target.getWeight() + weapon.magazine.flags["Ammo"].getWeight() > target.getMaxWeight():
                        getQuantity = 0
                        if target.getWeight() + weapon.magazine.flags["Ammo"].getWeight(False) <= target.getMaxWeight():
                            getQuantity = int((target.getMaxWeight() - target.getWeight()) / weapon.magazine.flags["Ammo"].getWeight(False))

                    if getQuantity > 0:
                        shellCount += getQuantity
                        inventoryAmmo, unused = target.getTargetItem(weapon.magazine.flags["Ammo"].num, ["Inventory"])
                        if inventoryAmmo != None:
                            inventoryAmmo.quantity += getQuantity
                        else:
                            splitItem = copy.deepcopy(weapon.magazine.flags["Ammo"])
                            splitItem.quantity = getQuantity
                            target.itemDict["Ammo"].append(splitItem)
                        targetAmmo = weapon.magazine.flags["Ammo"]
                        if getQuantity == weapon.magazine.flags["Ammo"].quantity:
                            weapon.magazine.flags["Ammo"] = None
                        else:
                            weapon.magazine.flags["Ammo"].quantity -= getQuantity

                    magazineCheck = False
                    if roomItem != None and target.getWeight() + weapon.magazine.getWeight() > target.getMaxWeight():
                        tooMuchWeightCheck = True
                    else:
                        target.itemDict["Ammo"].append(weapon.magazine)
                        targetMagazine = weapon.magazine
                        weapon.magazine = None
                        magazineCheck = True
                        magazineCount += 1
                    
                    if getQuantity > 0 or magazineCheck == True:
                        if unloadWeapon == None:
                            unloadWeapon = weapon
                        elif unloadWeapon != "Multiple" and unloadWeapon.num != weapon.num:
                            unloadWeapon = "Multiple"
                        unloadCount += 1

        if unloadWeapon == "Multiple" or magazineCount > 1:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You finish unloading your weapons.", "Code":"33w1y"})

        else:
            countString = ""
            countCode = ""
            if unloadWeapon != "Multiple" and unloadCount > 1:
                countString = " (" + str(unloadCount) + ")"
                countCode = "2r" + str(len(str(unloadCount))) + "w1r"
            unloadString = ""
            unloadCode = ""
            if targetAmmo != None and shellCount > 0:
                shellString = ""
                shellCode = ""
                if shellCount > 1:
                    shellString = " (" + str(shellCount) + ")"
                    shellCode = "2r" + str(len(str(shellCount))) + "w1r"
                unloadString = targetAmmo.name["String"] + shellString
                unloadCode = targetAmmo.name["Code"] + shellCode
            elif targetAmmo == None and targetMagazine != None:
                unloadString = targetMagazine.prefix.lower() + " " + targetMagazine.name["String"]
                unloadCode = str(len(targetMagazine.prefix)) + "w1w" + targetMagazine.name["Code"]
                if magazineCount > 1:
                    unloadString = "some magazines"
                    unloadCode = "14w"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You unload " + unloadString + " from " + unloadWeapon.prefix.lower() + " " + unloadWeapon.name["String"] + "." + countString, "Code":"11w" + unloadCode + "6w" + str(len(unloadWeapon.prefix)) + "w1w" + unloadWeapon.name["Code"] + "1y" + countCode})

    @staticmethod
    def updateActionCommand(console, target):
        if len(target.actionList) > 0:
            target.actionList[0].update(console, target)
            if target.actionList[0].currentTick >= target.actionList[0].maxTick:
                del target.actionList[0]
