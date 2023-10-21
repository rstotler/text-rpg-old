from GameData.Player.CombatSkill import CombatSkill
from GameData.Item.Item import Item
from Components.Utility import appendKeyList
from Components.Utility import getTargetUserString

class Button:

    def __init__(self, type, flags):
        self.type = type
        self.label = None
        self.keyList = []
        self.flags = flags

        if "Label" in flags:
            self.label = flags["Label"]
            appendKeyList(self.keyList, self.label["String"].lower())

        appendKeyList(self.keyList, "button")
        if "Key List" in flags:
            self.keyList += flags["Key List"]

    def push(self, console, player, targetUser, currentRoom):
        if self.type == "Spawn Mob" and "Num" in self.flags:
            from GameData.Player.Player import Player
            galaxyNum = currentRoom.galaxy
            systemNum = currentRoom.system
            planetNum = currentRoom.planet
            spaceshipNum = None
            if currentRoom.spaceshipObject != None:
                galaxyNum = currentRoom.spaceshipObject.galaxy
                systemNum = currentRoom.spaceshipObject.system
                planetNum = currentRoom.spaceshipObject.planet
                spaceshipNum = currentRoom.spaceshipObject.num
            spawnedMob = Player(galaxyNum, systemNum, planetNum, currentRoom.area, currentRoom.room, spaceshipNum, self.flags["Num"])

            if "Skill List" in self.flags:
                spawnedMob.combatSkillDict = {"Basic":[], "Sword":[], "Dagger":[], "Axe":[], "Blunt":[], "Polearm":[], "Unarmed":[], "Bow":[], "Pistol":[], "Rifle":[], "Offensive Magic":[], "Healing Magic":[]}
                for skillNum in self.flags["Skill List"]:
                    combatSkill = CombatSkill(skillNum)
                    spawnedMob.combatSkillDict[combatSkill.skillGroup].append(combatSkill)

            if "Gear Dict" in self.flags:
                for gearSlot in self.flags["Gear Dict"]:
                    for itemNum in self.flags["Gear Dict"][gearSlot]:
                        if gearSlot in spawnedMob.gearDict:
                            slotRange = 1
                            if isinstance(spawnedMob.gearDict[gearSlot], list):
                                slotRange = 2
                            for slotNum in range(slotRange):
                                if isinstance(spawnedMob.gearDict[gearSlot], list):
                                    targetSlot = spawnedMob.gearDict[gearSlot][slotNum]
                                else:
                                    targetSlot = spawnedMob.gearDict[gearSlot]
                                if targetSlot == None:
                                    if isinstance(spawnedMob.gearDict[gearSlot], list):
                                        spawnedMob.gearDict[gearSlot][slotNum] = Item(itemNum)
                                    else:
                                        spawnedMob.gearDict[gearSlot] = Item(itemNum)
                                    break
            
            currentRoom.mobList.append(spawnedMob)
            
            if currentRoom.sameRoomCheck(player) == True:
                targetUserLine = getTargetUserString(targetUser, False)
                pushString = "push"
                if targetUser.num != None:
                    pushString = "pushes"
                displayString = targetUserLine["String"] + pushString + " the button and " + spawnedMob.prefix.lower() + " " + spawnedMob.name["String"] + " materializes in the room."
                displayCode = targetUserLine["Code"] + str(len(pushString)) + "w16w" + str(len(spawnedMob.prefix)) + "w1w" + spawnedMob.name["Code"] + "25w1y"
                console.write(displayString, displayCode, True)
