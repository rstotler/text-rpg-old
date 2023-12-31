import copy, random
from GameData.World.Room import Room
from GameData.World.Spaceship import Spaceship
from GameData.Player.Action import Action
from GameData.Player.Skill import Skill
from GameData.Player.CombatSkill import CombatSkill
from GameData.Combat import Combat
from GameData.Item.Item import Item
from GameData.Item.Components.Button import Button
from Components.Utility import *

class Player:

    def __init__(self, galaxy, system, planet, area, room, spaceship, num):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.area = area
        self.room = room
        self.spaceship = spaceship
        self.num = num
        self.flags = {}

        self.prefix = "A"
        self.name = {"String":"Debug Mob", "Code":"9w"}
        self.roomDescription = {"String":"is standing here.", "Code":"16w1y"}
        self.keyList = []

        self.combatSkillDict = {"Melee":[], "Sword":[], "Dagger":[], "Axe":[], "Blunt":[], "Polearm":[], "Claw":[], "Shield":[], "Bow":[], "Pistol":[], "Rifle":[]}

        self.actionList = []
        self.stunList = []
        self.stunnedByList = []

        self.currentHealth = 4

        self.maxLookDistance = 5

        self.targetList = []
        self.recruitList = []
        self.combatList = []

        self.itemDict = {"Armor":[], "Weapon":[], "Ammo":[], "Materium":[], "Key":[], "Organic":[], "Misc":[]}
        self.gearDict = {"Head":None, "Face":None, "Neck":[None, None], "Body Under":None, "Body Over":None, "About Body":None, "Hands":None, "Finger":[None, None], "Legs Under":None, "Legs Over":None, "Feet":None, "Left Hand":None, "Right Hand":None}
        self.cutLimbList = []
        self.dominantHand = "Right Hand"

        self.emoteList = ["hmm", "hm", "nod", "nodnod", "tap", "boggle", "ahah", "jump", "gasp", "haha", "lol", "cheer", "smile", "swear", "sigh", "grin", "snicker", "whistle"]

        self.debugDualWield = True

        # Mob-Specific Variables #
        self.displayOffset = [0, 0]

        self.speechTickMax = 8
        self.speechTick = 0
        self.speechIndex = 0
        self.speechList = []

        if num != None:
            self.loadMob(num)

    def update(self, config, console, map, galaxyList, player, currentRoom, messageDataList):
        messageDataList = self.updateAction(config, console, galaxyList, player, currentRoom, messageDataList)
        
        # Mob Update #
        if self.num != None:
            if self in player.combatList:
                if len(self.actionList) == 0:
                    distanceToPlayer, directionToPlayer, unused = Room.getTargetRange(galaxyList, currentRoom, player, self.maxLookDistance)
                    if distanceToPlayer != -1:
                        skillChoiceList = []
                        maxSkillRange = -1
                        for skill in self.getCombatSkillList():
                            if skill.ruleCheck({"Distance":distanceToPlayer, "Disable Healing":True}) == True:
                                if self.skillWeaponCheck(skill) == True:
                                    if len(skill.weaponTypeList) > 0 and ("Pistol" in skill.weaponTypeList[0] or "Rifle" in skill.weaponTypeList[0]) and ((self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].isGun() and self.gearDict[self.dominantHand].isEmpty(True) == True) and (self.gearDict[self.getOppositeHand(self.dominantHand)] == None or (self.gearDict[self.getOppositeHand(self.dominantHand)] != None and self.gearDict[self.getOppositeHand(self.dominantHand)].isGun() and self.gearDict[self.getOppositeHand(self.dominantHand)].isEmpty(True) == True))):
                                        # No Ammo
                                        pass
                                    else:
                                        skillChoiceList.append(skill)
                                        if skill.maxRange > maxSkillRange:
                                            maxSkillRange = skill.maxRange

                        # Chase Player, Next Room Locked Door Check #
                        if distanceToPlayer > 0:
                            if not (currentRoom.door[directionToPlayer] != None and currentRoom.door[directionToPlayer]["Status"] == "Locked" and "Password" in currentRoom.door[directionToPlayer] and self.hasKey(currentRoom.door[directionToPlayer]["Password"]) == False):
                                messageDataList += self.moveCheck(console, map, galaxyList, player, currentRoom, directionToPlayer.lower())

                        # Use Skill #
                        elif len(skillChoiceList) > 0:
                            targetSkill = random.choice(skillChoiceList)
                            directionKey = None
                            directionCount = None
                            if directionToPlayer != None:
                                directionKey = directionToPlayer
                                directionCount = distanceToPlayer
                            messageDataList += self.combatSkillCheck(config, console, galaxyList, player, currentRoom, targetSkill, 1, "Player", directionKey, directionCount, messageDataList)

            else:

                # Speech #
                firstUniqueMobCheck = False
                for i, mob in enumerate(currentRoom.mobList):
                    if mob.num == self.num:
                        if mob == self:
                            firstUniqueMobCheck = True
                        else:
                            break

                if currentRoom.sameRoomCheck(player) == True and len(self.speechList) > 0 and firstUniqueMobCheck == True:
                    self.speechTick += 1
                    if self.speechTick >= self.speechTickMax:
                        self.sayCheck(console, galaxyList, player, currentRoom, self.speechList[self.speechIndex])
                        self.speechTick = 0
                        self.speechIndex += 1
                        if self.speechIndex >= len(self.speechList):
                            self.speechIndex = 0
                            self.speechTick =  -150

        return messageDataList

    def updateAction(self, config, console, galaxyList, player, currentRoom, messageDataList):
        if len(self.actionList) > 0:
            targetAction = self.actionList[0]
            messageDataList = targetAction.update(config, console, galaxyList, player, self, currentRoom, messageDataList)
            if len(self.actionList) > 0 and targetAction.currentTick >= targetAction.maxTick:
                del self.actionList[0]

        return messageDataList

    def lookDirection(self, console, galaxyList, currentRoom, lookDirKey, count):
        lookDir = Room.getTargetDirection(lookDirKey)
        if isinstance(count, int) and count > 50:
            count = 50
        messageType = None
        lookCheck = False
        lookDistance = count
        peerThroughDoorCheck = False
        if lookDistance > self.maxLookDistance:
            lookDistance = self.maxLookDistance
        for i in range(lookDistance):
            if currentRoom.exit[lookDir] == None or (currentRoom.door[lookDir] != None and currentRoom.door[lookDir]["Type"] == "Hidden" and currentRoom.door[lookDir]["Status"] != "Open"):
                messageType = "Can't See Further"
                break
            elif currentRoom.door[lookDir] != None and currentRoom.door[lookDir]["Status"] in ["Closed", "Locked"] and \
            not (currentRoom.spaceshipObject != None and i == 0 and currentRoom.exit[lookDir] == "Spaceship Exit"):
                messageType = "View Obstructed"
                break
            else:
                lookCheck = True
                if len(currentRoom.exit[lookDir]) == 3 and currentRoom.spaceshipObject != None:
                    currentRoom = currentRoom.spaceshipObject.areaList[currentRoom.exit[lookDir][1]].roomList[currentRoom.exit[lookDir][2]]
                elif len(currentRoom.exit[lookDir]) == 5:
                    currentRoom = Room.exists(galaxyList, None, currentRoom.exit[lookDir][0], currentRoom.exit[lookDir][1], currentRoom.exit[lookDir][2], currentRoom.exit[lookDir][3], currentRoom.exit[lookDir][4])
                    if currentRoom == None:
                        currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                elif currentRoom.exit[lookDir] == "Spaceship Exit":
                    if currentRoom.spaceshipObject.landedLocation != None:
                        currentRoom = galaxyList[currentRoom.spaceshipObject.galaxy].systemList[currentRoom.spaceshipObject.system].planetList[currentRoom.spaceshipObject.planet].areaList[currentRoom.spaceshipObject.landedLocation[0]].roomList[currentRoom.spaceshipObject.landedLocation[1]]
                        peerThroughDoorCheck = True
                    else:
                        messageType = "Outside Ship Door"
                        break

        countString = ""
        countCode = ""
        if i > 0 or count > self.maxLookDistance:
            if count > self.maxLookDistance:
                i += 1
            sString = ""
            if i > 1:
                sString = "s"
            countString = " (" + str(i) + " Room" + sString + " Away)"
            if sString == "" : countCode = "2r" + str(len(str(i))) + "w10w1r"
            else : countCode = "2r" + str(len(str(i))) + "w11w1r"

        drawBlankLine = True
        if peerThroughDoorCheck == True:
            console.write("You peer through the opening in the door.", "40w1y", drawBlankLine)
            drawBlankLine = False
        if messageType == None and count > self.maxLookDistance:
            console.write("You can't see that far." + countString, "7w1y14w1y" + countCode, drawBlankLine)
        elif messageType != None:
            if messageType == "Can't See Further":
                console.write("You can't see any farther to the " + lookDir + "." + countString, "7w1y25w" + str(len(lookDir)) + "w1y" + countCode, drawBlankLine)
            elif messageType == "View Obstructed":
                console.write("Your view to the " + lookDir + " is obstructed by a door." + countString, "17w" + str(len(lookDir)) + "w24w1y" + countCode, drawBlankLine)
            elif messageType == "Outside Ship Door":
                if currentRoom.spaceshipObject.launchLandTick == -1:
                    console.write("You look outside and see an endless sea of stars.", "48w1y", True)
                else:
                    console.write("You don't see anything special.", "7w1y22w1y", True)
                lookCheck = False
        if lookCheck:
            currentRoom.display(console, galaxyList, self)
    
    def lookTargetCheck(self, console, galaxyList, player, currentRoom, lookDirKey, count, lookTarget):
        lookDir = None
        if lookDirKey != None:
            lookDir = Room.getTargetDirection(lookDirKey)
        if isinstance(count, int) and count > 50:
            count = 50
        messageType = None
        lookCount = 0
        if count != None and lookTarget != "Target":
            lookDistance = count
            if lookDistance > self.maxLookDistance:
                lookDistance = self.maxLookDistance
            for i in range(lookDistance):
                if currentRoom.exit[lookDir] == None:
                    messageType = "Can't See Further"
                    break
                elif currentRoom.door[lookDir] != None and currentRoom.door[lookDir]["Status"] in ["Closed", "Locked"]:
                    messageType = "View Obstructed"
                    break
                else:
                    if len(currentRoom.exit[lookDir]) == 3 and currentRoom.spaceshipObject != None:
                        currentRoom = currentRoom.spaceshipObject.areaList[currentRoom.exit[lookDir][1]].roomList[currentRoom.exit[lookDir][2]]
                    elif len(currentRoom.exit[lookDir]) == 5:
                        currentRoom = Room.exists(galaxyList, None, currentRoom.exit[lookDir][0], currentRoom.exit[lookDir][1], currentRoom.exit[lookDir][2], currentRoom.exit[lookDir][3], currentRoom.exit[lookDir][4])
                    if currentRoom == None:
                        currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                    lookCount += 1
                    
        if messageType == "Can't See Further":
            console.write("There is nothing there.", "22w1y", True)
        elif messageType == "View Obstructed":
            countString = ""
            countCode = ""
            sString = ""
            sCode = ""
            if lookCount > 0:
                if lookCount > 1:
                    sString = "s"
                    sCode = "1w"
                countString = " (" + str(lookCount) + " Room" + sString + " Away)"
                countCode = "2r" + str(len(str(lookCount))) + "w5w" + sCode + "5w1r"
            console.write("Your view to the " + lookDir + " is obstructed by a door." + countString, "17w" + str(len(lookDir)) + "w24w1y" + countCode, True)
            
            if lookCount > 0:
                currentRoom.display(console, galaxyList, self)

        else:
            roomTarget = None
            if count == None:
                roomTarget, playerItemLocation = self.getTargetItem(lookTarget)
            if roomTarget == None:
                roomTarget = currentRoom.getTargetObject(lookTarget, ["Mobs", "Items", "Spaceships", "Buttons", "Hidden Objects"])
            if roomTarget == None and lookTarget == "self" and lookDirKey == None and count == None:
                roomTarget = self

            if currentRoom.isLit(galaxyList, player, self) == False and not (isinstance(roomTarget, Item) and roomTarget.containerList != None and roomTarget.lightInContainerCheck() == True):
                console.write("It's too dark to see.", "2w1y17w1y", True)
            elif roomTarget != None and isinstance(roomTarget, dict) and "Type" in roomTarget and roomTarget["Type"] == "Hidden":
                console.write("It looks a little out of place.", "30w1y", True)
            elif roomTarget != None and isinstance(roomTarget, Button) == True:
                console.write("It's a button.", "2w1y10w1y", True)
            elif roomTarget == None:
                console.write("You don't see anything like that.", "7w1y24w1y", True)
            else:
                if isinstance(roomTarget, Item):
                    passwordCheck = False
                    if roomTarget.containerPassword != None:
                        passwordCheck = self.hasKey(roomTarget.containerPassword)
                    roomTarget.lookDescription(console, lookCount, passwordCheck)
                elif isinstance(roomTarget, Spaceship):
                    roomTarget.lookDescription(console)
                else:
                    roomTarget.lookDescription(console, galaxyList, player, currentRoom)

    def lookItemInContainerCheck(self, console, currentRoom, targetItemKey, targetContainerKey):
        targetContainer = currentRoom.getTargetObject(targetContainerKey)
        if targetContainer == None:
            console.write("You can't find it.", "7w1y9w1y", True)
        elif isinstance(targetContainer, Item) == False or targetContainer.containerList == None:
            console.write("That's not a container!", "4w1y17w1y", True)
        else:
            containerItem = targetContainer.getContainerItem(targetItemKey)
            if containerItem == None:
                console.write("You don't see anything like that.", "7w1y24w1y", True)
            else:
                containerItem.lookDescription(console)

    def targetCheck(self, console, galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, targetDirCount):
        if targetDirCount != None and targetDirCount > self.maxLookDistance:
            console.write("You can't see that far.", "7w1y14w1y", True)
        elif targetDirCount != None and targetDirCount > self.maxLookDistance:
            console.write("It's too far away to target.", "2w1y24w1y", True)
        
        else:
            targetRoom = currentRoom
            messageType = None
            roomCount = 0
            targetDir = None
            if targetDirKey != None and targetDirCount != None:
                targetDir = Room.getTargetDirection(targetDirKey)
                for i in range(targetDirCount):
                    if targetRoom.exit[targetDir] == None:
                        messageType = "Can't See Further"
                        break
                    elif targetRoom.door[targetDir] != None and targetRoom.door[targetDir]["Status"] in ["Closed", "Locked"]:
                        messageType = "View Obstructed"
                        break
                    elif targetRoom.exit[targetDir] == "Spaceship Exit" and targetRoom.spaceshipObject.landedLocation == None:
                        messageType = "View Obstructed"
                        break
                    else:
                        if targetRoom.exit[targetDir] == "Spaceship Exit":
                            landedLocation = targetRoom.spaceshipObject.landedLocation
                            targetRoom = Room.exists(galaxyList, None, targetRoom.spaceshipObject.galaxy, targetRoom.spaceshipObject.system, targetRoom.spaceshipObject.planet, landedLocation[0], landedLocation[1])
                            if targetRoom == None:
                                targetRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                        elif len(targetRoom.exit[targetDir]) == 3 and targetRoom.spaceshipObject != None:
                            targetRoom = targetRoom.spaceshipObject.areaList[targetRoom.exit[targetDir][1]].roomList[targetRoom.exit[targetDir][2]]
                        elif len(targetRoom.exit[targetDir]) == 5:
                            targetRoom = Room.exists(galaxyList, None, targetRoom.exit[targetDir][0], targetRoom.exit[targetDir][1], targetRoom.exit[targetDir][2], targetRoom.exit[targetDir][3], targetRoom.exit[targetDir][4])
                            if targetRoom == None:
                                targetRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                        roomCount += 1
            
            if messageType == "Can't See Further":
                console.write("There is nothing there.", "22w1y", True)
            elif messageType == "View Obstructed":
                countString = ""
                countCode = ""
                sString = ""
                sCode = ""
                if roomCount > 0:
                    if roomCount > 1:
                        sString = "s"
                        sCode = "1w"
                    countString = " (" + str(roomCount) + " Room" + sString + " Away)"
                    countCode = "2r" + str(len(str(roomCount))) + "w5w" + sCode + "5w1r"
                console.write("Your view to the " + targetDir + " is obstructed by a door." + countString, "17w" + str(len(targetDir)) + "w24w1y" + countCode, True)
        
            else:
                targetMob = None
                if targetMobKey != "All":
                    targetMob = targetRoom.getTargetObject(targetMobKey)

                if targetMobKey != "All" and targetMob == None:
                    console.write("You don't see them.", "7w1y10w1y", True)
                elif targetMob != None and hasattr(targetMob, "dominantHand") == False:
                    console.write("You can't target that.", "7w1y13w1y", True)
                
                else:
                    targetMob = None
                    targetCount = 0
                    targetRange = targetMobCount
                    alreadyTargetingCheck = False
                    recruitedCheck = False
                    if targetRange == "All":
                        targetRange = len(targetRoom.mobList)
                    for i in range(targetRange):
                        for mob in targetRoom.mobList:
                            if mob in self.recruitList:
                                recruitedCheck = True
                            elif targetMobKey == "All" or targetMobKey in mob.keyList:
                                if mob in self.targetList:
                                    alreadyTargetingCheck = True
                                else:
                                    if targetMobKey == "All":
                                        self.targetList.append(mob)
                                    else:
                                        self.targetList.insert(0, mob)
                                    targetCount += 1
                                    if targetMob == None:
                                        targetMob = mob
                                    elif targetMob != "Multiple" and targetMob.num != mob.num:
                                        targetMob = "Multiple"
                                    break

                    if targetCount == 0 and (alreadyTargetingCheck == True or recruitedCheck):
                        console.write("You are already targeting them.", "30w1y", True)
                    elif targetCount == 0:
                        console.write("You don't see them.", "7w1y10w1y", True)
                    
                    elif targetMob != "Multiple":
                        displayString = "You narrow your vision on " + targetMob.prefix.lower() + " " + targetMob.name["String"] + "."
                        displayCode = "26w" + str(len(targetMob.prefix)) + "w1w" + targetMob.name["Code"] + "1y"
                        targetCountString, targetCountCode = getCountString(targetCount)
                        dirString = ""
                        dirCode = ""
                        dirCountString = ""
                        dirCountCode = ""
                        if targetDir != None:
                            displayString = displayString[0:-1]
                            displayCode = displayCode[0:-2]
                            dirString = " to the " + targetDir + "."
                            dirCode = "8w" + str(len(targetDir)) + "w1y"
                            if roomCount > 1:
                                dirString = dirString[0:-1]
                                dirCode = dirCode[0:-2]
                                dirCountString = " (" + str(roomCount) + ")."
                                dirCountCode = "2r" + str(len(str(roomCount))) + "w1r1y"
                        console.write(displayString + targetCountString + dirString + dirCountString, displayCode + targetCountCode + dirCode + dirCountCode, True)
                    
                    else:
                        displayString = "You focus your attention on the group."
                        displayCode = "37w1y"
                        dirString = ""
                        dirCode = ""
                        dirCountString = ""
                        dirCountCode = ""
                        if targetDir != None:
                            displayString = displayString[0:-1]
                            displayCode = displayCode[0:-2]
                            dirString = " to the " + targetDir + "."
                            dirCode = "8w" + str(len(str(targetDir))) + "w1y"
                            if roomCount > 1:
                                dirString = dirString[0:-1]
                                dirCode = dirCode[0:-2]
                                dirCountString = " (" + str(roomCount) + ")."
                                dirCountCode = "2r" + str(len(str(roomCount))) + "w1r1y"
                        console.write(displayString + dirString + dirCountString, displayCode + dirCode + dirCountCode, True)

    def untargetCheck(self, console, galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, targetDirCount):
        if targetDirCount != None and targetDirCount > self.maxLookDistance:
            console.write("You can't see that far.", "7w1y14w1y", True)
        
        else:
            targetRoom = currentRoom
            messageType = None
            roomCount = 0
            targetDir = None
            if targetDirKey != None and targetDirCount != None:
                targetDir = Room.getTargetDirection(targetDirKey)
                for i in range(targetDirCount):
                    if targetRoom.exit[targetDir] == None:
                        messageType = "Can't See Further"
                        break
                    elif targetRoom.door[targetDir] != None and targetRoom.door[targetDir]["Status"] in ["Closed", "Locked"]:
                        messageType = "View Obstructed"
                        break
                    elif targetRoom.exit[targetDir] == "Spaceship Exit" and targetRoom.spaceshipObject.landedLocation == None:
                        messageType = "View Obstructed"
                        break
                    else:
                        if targetRoom.exit[targetDir] == "Spaceship Exit":
                            landedLocation = targetRoom.spaceshipObject.landedLocation
                            targetRoom = Room.exists(galaxyList, None, targetRoom.spaceshipObject.galaxy, targetRoom.spaceshipObject.system, targetRoom.spaceshipObject.planet, landedLocation[0], landedLocation[1])
                            if targetRoom == None:
                                targetRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                        elif len(targetRoom.exit[targetDir]) == 3 and targetRoom.spaceshipObject != None:
                            targetRoom = targetRoom.spaceshipObject.areaList[targetRoom.exit[targetDir][1]].roomList[targetRoom.exit[targetDir][2]]
                        elif len(targetRoom.exit[targetDir]) == 5:
                            targetRoom = Room.exists(galaxyList, None, targetRoom.exit[targetDir][0], targetRoom.exit[targetDir][1], targetRoom.exit[targetDir][2], targetRoom.exit[targetDir][3], targetRoom.exit[targetDir][4])
                            if targetRoom == None:
                                targetRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                        roomCount += 1
            
            if messageType == "Can't See Further":
                console.write("There is nothing there.", "22w1y", True)
            elif messageType == "View Obstructed":
                countString = ""
                countCode = ""
                sString = ""
                sCode = ""
                if roomCount > 0:
                    if roomCount > 1:
                        sString = "s"
                        sCode = "1w"
                    countString = " (" + str(roomCount) + " Room" + sString + " Away)"
                    countCode = "2r" + str(len(str(roomCount))) + "w5w" + sCode + "5w1r"
                console.write("Your view to the " + targetDir + " is obstructed by a door." + countString, "17w" + str(len(targetDir)) + "w24w1y" + countCode, True)
        
            else:
                targetMob = None
                if targetDirKey != None and targetMobKey != "All":
                    targetMob = targetRoom.getTargetObject(targetMobKey)
                    if targetMob == None:
                        console.write("You don't see them.", "7w1y10w1y", True)
                        return
                    elif hasattr(targetMob, "dominantHand") == False:
                        console.write("You can't target that.", "7w1y13w1y", True)
                        return
                                
                targetList = targetRoom.mobList
                if targetDirKey == None and targetDirCount == None:
                    targetList = self.targetList

                targetCount = 0
                targetRange = targetMobCount
                targetRoomList = []
                if targetRange == "All":
                    targetRange = len(targetList)
                for i in range(targetRange):
                    for mob in targetList:
                        if targetMobKey == "All" or targetMobKey in mob.keyList:
                            if mob in self.targetList:
                                del self.targetList[self.targetList.index(mob)]
                                targetCount += 1
                                if {"Galaxy":mob.galaxy, "System":mob.system, "Planet":mob.planet, "Area":mob.area, "Room":mob.room, "Spaceship":mob.spaceship} not in targetRoomList:
                                    targetRoomList.append({"Galaxy":mob.galaxy, "System":mob.system, "Planet":mob.planet, "Area":mob.area, "Room":mob.room, "Spaceship":mob.spaceship})
                                if targetMob == None:
                                    targetMob = mob
                                elif targetMob != "Multiple" and targetMob.num != mob.num:
                                    targetMobRange, targetMobDir, message =  Room.getTargetRange(galaxyList, targetRoom, targetMob, self.maxLookDistance)
                                    if targetMobRange != -1 and targetMobDir != None:
                                        targetDir = targetMobDir
                                        roomCount = targetMobRange
                                    targetMob = "Multiple"
                                break
                                
                if targetMobCount == "All" and targetMobKey != "All" and targetMob == None:
                    targetMob = targetRoom.getTargetObject(targetMobKey, ["Mobs"])

                if targetCount > 1 and targetMobKey == "All":
                    console.write("You take a breath out and relax your mind.", "41w1y", True)
                elif targetMob == "Multiple" and len(targetRoomList) > 1:
                    console.write("You relax your mind a little.", "28w1y", True)
                elif targetCount == 0 and targetDirKey == None and targetMobKey == "All":
                    console.write("You aren't targeting anyone.", "8w1y18w1y", True)
                elif targetCount == 0 and targetMob == None:
                    console.write("You don't see them.", "7w1y10w1y", True)
                elif targetCount == 0:
                    console.write("You aren't targeting them.", "8w1y16w1y", True)
                
                elif targetMob != "Multiple":
                    if targetDirKey == None and targetDirCount == None and targetMob not in targetRoom.mobList and len(targetRoomList) == 1:
                        targetMobRange, targetMobDir, message =  Room.getTargetRange(galaxyList, targetRoom, targetMob, self.maxLookDistance)
                        if targetMobRange != -1 and targetMobDir != None:
                            targetDir = targetMobDir
                            roomCount = targetMobRange

                    displayString = "You stop targeting " + targetMob.prefix.lower() + " " + targetMob.name["String"] + "."
                    displayCode = "19w" + str(len(targetMob.prefix)) + "w1w" + targetMob.name["Code"] + "1y"
                    targetCountString, targetCountCode = getCountString(targetCount)
                    dirString = ""
                    dirCode = ""
                    dirCountString = ""
                    dirCountCode = ""
                    if targetDir != None:
                        displayString = displayString[0:-1]
                        displayCode = displayCode[0:-2]
                        dirString = " to the " + targetDir + "."
                        dirCode = "8w" + str(len(targetDir)) + "w1y"
                        if roomCount > 1:
                            dirString = dirString[0:-1]
                            dirCode = dirCode[0:-2]
                            dirCountString = " (" + str(roomCount) + ")."
                            dirCountCode = "2r" + str(len(str(roomCount))) + "w1r1y"
                    console.write(displayString + targetCountString + dirString + dirCountString, displayCode + targetCountCode + dirCode + dirCountCode, True)
                
                else:
                    displayString = "You stop targeting the group."
                    displayCode = "28w1y"
                    dirString = ""
                    dirCode = ""
                    dirCountString = ""
                    dirCountCode = ""
                    if targetDir != None and len(targetRoomList) == 1:
                        displayString = displayString[0:-1]
                        displayCode = displayCode[0:-2]
                        dirString = " to the " + targetDir + "."
                        dirCode = "8w" + str(len(str(targetDir))) + "w1y"
                        if roomCount > 1:
                            dirString = dirString[0:-1]
                            dirCode = dirCode[0:-2]
                            dirCountString = " (" + str(roomCount) + ")."
                            dirCountCode = "2r" + str(len(str(roomCount))) + "w1r1y"
                    console.write(displayString + dirString + dirCountString, displayCode + dirCode + dirCountCode, True)

    def moveCheck(self, console, map, galaxyList, player, currentRoom, targetDirKey):
        messageDataList = []

        if targetDirKey.lower() in ["north", "nort", "nor", "no", "n"] : targetDir = "North"
        elif targetDirKey.lower() in ["east", "eas", "ea", "e"] : targetDir = "East"
        elif targetDirKey.lower() in ["south", "sout", "sou", "so", "s"] : targetDir = "South"
        elif targetDirKey.lower() in ["west", "wes", "we", "w"] : targetDir = "West"
        elif targetDirKey.lower() in ["up", "u"] : targetDir = "Up"
        else : targetDir = "Down"
        
        if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Status"] == "Locked" and "Password" in currentRoom.door[targetDir] and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
            if self.num == None:
                console.write("You lack the proper key.", "23w1y", True)
        elif currentRoom.exit[targetDir] == None or (currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Hidden" and currentRoom.door[targetDir]["Status"] in ["Closed", "Locked"]):
            if self.num == None:
                console.write("You can't go that way!", "7w1y13w1y", True)
        elif currentRoom.exit[targetDir] == "Spaceship Exit" and currentRoom.spaceshipObject != None and currentRoom.spaceshipObject.landedLocation == None:
            if self.num == None:
                console.write("The hatch is sealed.", "19w1y", True)

        else:
            mobString = self.prefix + " " + self.name["String"]
            mobCode = str(len(self.prefix)) + "w1w" + self.name["Code"]
            if len(self.actionList) > 0 and self.actionList[0].actionType not in ["Combat Skill", "Reload"]:
                targetAction = self.actionList[0]
                self.actionList = []
                if self.num == None:
                    console.write("You stop " + targetAction.actionType.lower() + "ing and move.", "9w" + str(len(targetAction.actionType)) + "w12w1y", True)
                elif currentRoom.sameRoomCheck(player):
                    messageDataList.append({"String":mobString + " stops " + targetAction.actionType.lower() + "ing and moves " + targetDir + ".", "Code":mobCode + "7w" + str(len(targetAction.actionType)) + "w14w" + str(len(targetDir)) + "w1y", "Draw Blank Line":True})
            elif self.num != None and currentRoom.sameRoomCheck(player) and not (currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic"):
                messageDataList.append({"String":mobString + " moves " + targetDir + ".", "Code":mobCode + "7w" + str(len(targetDir)) + "w1y", "Draw Blank Line":True})

            currentArea = Room.getAreaAndRoom(galaxyList, self)[0]
            targetArea, targetRoom, unusedDistance, unusedMessage = Room.getTargetRoomFromStartRoom(galaxyList, currentArea, currentRoom, targetDir, 1, True)

            if len(self.actionList) > 0 and self.actionList[0].actionType == "Combat Skill" and self.actionList[0].flags["combatSkill"].maxRange > 0:
                attackDistance = Room.getTargetRange(galaxyList, targetRoom, self.actionList[0].flags["targetRoom"], self.actionList[0].flags["combatSkill"].maxRange)[0]
                if attackDistance == -1:
                    del self.actionList[0]
                    if self.num == None:
                        console.write("You move out of your attack range.", "33w1y", True)
                    else:
                        messageDataList.append({"String":mobString + " releases their attack.", "Code":mobCode + "22w1y", "Draw Blank Line":True})

            # Move #
            automaticDoorCheck = False
            if targetRoom.spaceshipObject != None:
                self.area = targetRoom.area
                self.room = targetRoom.room
            else:
                oldSpaceship = self.spaceship
                oldArea = self.area
                self.galaxy = targetRoom.galaxy
                self.system = targetRoom.system
                self.planet = targetRoom.planet
                self.area = targetRoom.area
                self.room = targetRoom.room
                if self.spaceship != None:
                    self.spaceship = None

                if self.num == None:
                    if self.spaceship != oldSpaceship or self.area != oldArea:
                        map.loadAreaMap(targetArea)
                        targetArea.flavorTextTick = 0

            openCheck = False
            lockCheck = False
            if currentRoom.door[targetDir] != None:
                if currentRoom.door[targetDir]["Status"] == "Locked":
                    lockCheck = True
                if currentRoom.door[targetDir]["Type"] == "Manual" and currentRoom.door[targetDir]["Status"] != "Open":
                    currentRoom.openCloseDoor(galaxyList, "Open", targetDir)
                    openCheck = True
            
            if self.num == None or targetRoom.sameRoomCheck(player) == True or currentRoom.sameRoomCheck(player) == True:
                if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Manual" and openCheck:
                    if self.num == None:
                        openString = "open"
                        if lockCheck:
                            openString = "unlock and open"
                        console.write("You " + openString + " the door and walk through.", "4w" + str(len(openString)) + "w26w1y", True)
                    elif currentRoom.sameRoomCheck(player) == True:
                        openString = "opens"
                        if lockCheck:
                            openString = "unlocks and opens"
                        displayString = self.prefix + " " + self.name["String"] + " " + openString + " the door to the " + targetDir + " and walks through."
                        displayCode = str(len(self.prefix)) + "w1w" + self.name["Code"] + "1w" + str(len(openString)) + "w17w" + str(len(targetDir)) + "w18w1y"
                        messageDataList.append({"String":displayString, "Code":displayCode, "Draw Blank Line":True})
                    elif targetRoom.sameRoomCheck(player) == True:
                        displayString = "The door to the " + Room.getOppositeDirection(targetDir) + " opens as " + self.prefix.lower() + " " + self.name["String"] + " walks through."
                        displayCode = "16w" + str(len(Room.getOppositeDirection(targetDir))) + "w10w" + str(len(self.prefix)) + "w1w" + self.name["Code"] + "14w1y"
                        messageDataList.append({"String":displayString, "Code":displayCode, "Draw Blank Line":True})
                
                elif currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic":
                    doorString = "door"
                    if currentRoom.exit[targetDir] == "Spaceship Exit":
                        doorString = "hatch"
                    if self.num == None:
                        console.write("The " + doorString + " opens and closes as you walk through.", "4w" + str(len(doorString)) + "w37w1y", True)
                    else:
                        displayDirection = targetDir
                        leavesString = " leaves"
                        if targetRoom.sameRoomCheck(player) == True:
                            displayDirection = Room.getOppositeDirection(targetDir)
                            leavesString = " enters"
                        displayString = "The door to the " + displayDirection + " opens and closes as " + mobString + leavesString + "."
                        displayCode = "16w" + str(len(displayDirection)) + "w21w" + mobCode + str(len(leavesString)) + "w1y"
                        messageDataList.append({"String":displayString, "Code":displayCode, "Draw Blank Line":True})
                    automaticDoorCheck = True

            if self.num == None:
                for mob in targetRoom.mobList:
                    mob.speechTick = 0
                    mob.speechIndex = 0

            if self.num != None:
                if self in currentRoom.mobList:
                    del currentRoom.mobList[currentRoom.mobList.index(self)]
                createMob(None, targetRoom, self)
                self.actionList.append(Action("Buffer Action", {}, 3))

            delTargetList = []
            delMobData = None
            loseSightDir = None
            if self.num == None:
                for targetMob in self.targetList:
                    distance, direction, message = Room.getTargetRange(galaxyList, targetRoom, targetMob, self.maxLookDistance + 1)
                    if distance == self.maxLookDistance + 1:
                        delTargetList.append(targetMob)
                        loseSightDir = direction
                        if delMobData == None:
                            delMobData = targetMob
                        elif delMobData != "Multiple" and delMobData.num != targetMob.num:
                            delMobData = "Multiple"
                for targetMob in delTargetList:
                    if targetMob in self.targetList:
                        del self.targetList[self.targetList.index(targetMob)]

                targetRoom.display(console, galaxyList, self)

            if self.num != None and self in player.targetList:
                playerRoom = Room.exists(galaxyList, player.spaceship, player.galaxy, player.system, player.planet, player.area, player.room)
                if playerRoom == None:
                    playerRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                mobDistance, mobDirection, unused = Room.getTargetRange(galaxyList, targetRoom, playerRoom, player.maxLookDistance + 1)
                if len(player.targetList) > 0 and player.targetList[0] == self and len(player.actionList) > 0 and player.actionList[0].actionType == "Combat Skill" and player.actionList[0].flags["combatSkill"].onTarget == True and mobDistance > player.actionList[0].flags["combatSkill"].maxRange:
                    del player.actionList[0]
                    messageDataList.append({"String":"Your target moved out of range for your attack.", "Code":"46w1y", "Draw Blank Line":True})
                elif self in player.targetList and mobDistance > player.maxLookDistance:
                    displayString = "You lose sight of " + self.prefix.lower() + " " + self.name["String"] + " as it moves " + Room.getOppositeDirection(mobDirection) + "."
                    displayCode = "18w" + str(len(self.prefix)) + "w1w" + self.name["Code"] + "13w" + str(len(Room.getOppositeDirection(mobDirection))) + "w1y"
                    messageDataList.append({"String":displayString, "Code":displayCode})
                    if player.targetList[0] == self and len(player.actionList) > 0 and player.actionList[0].actionType == "Combat Skill" and player.actionList[0].flags["combatSkill"].onTarget == True:
                        del player.actionList[0]
                        messageDataList.append({"String":"Your target moved out of range for your attack.", "Code":"46w1y", "Draw Blank Line":False})
                    del player.targetList[player.targetList.index(self)]
                    
            if self.num == None and len(delTargetList) > 0:
                countString, countCode = getCountString(len(delTargetList))
                if delMobData != "Multiple":
                    displayString = "You lose sight of " + delMobData.prefix.lower() + " " + delMobData.name["String"] + countString + " to the " + loseSightDir + "."
                    displayCode = "18w" + str(len(delMobData.prefix)) + "w1w" + delMobData.name["Code"] + countCode + "8w" + str(len(loseSightDir)) + "w1y"
                    console.write(displayString, displayCode, True)
                else:
                    someString = "some"
                    if len(self.targetList) == 0:
                        someString = "your"
                    displayString = "You lose sight of " + someString + " targets" + countString + " to the " + loseSightDir + "."
                    displayCode = "18w" + str(len(someString)) + "w8w" + countCode + "8w" + str(len(loseSightDir)) + "w1y"
                    console.write(displayString, displayCode, True)

            elif self.num != None and targetRoom.sameRoomCheck(player) == True and automaticDoorCheck == False:
                displayString = self.prefix + " " + self.name["String"] + " enters from the " + Room.getOppositeDirection(targetDir) + "."
                displayCode = str(len(self.prefix)) + "w1w" + self.name["Code"] + "17w" + str(len(Room.getOppositeDirection(targetDir))) + "w1y"
                messageDataList.append({"String":displayString, "Code":displayCode, "Draw Blank Line":True})

        return messageDataList

    def openCloseDoorCheck(self, console, galaxyList, player, currentRoom, targetAction, targetDirKey):
        targetDoorAction = targetAction
        if targetAction == "Close":
            targetDoorAction = "Closed"

        targetDir = Room.getTargetDirection(targetDirKey)
        if currentRoom.door[targetDir] == None:
            console.write("There is no door in that direction.", "34w1y", True)
        elif currentRoom.door[targetDir]["Type"] == "Automatic":
            console.write("That door is automatic.", "22w1y", True)
        elif currentRoom.door[targetDir]["Status"] == targetDoorAction or (targetDoorAction == "Closed" and currentRoom.door[targetDir]["Status"] == "Locked"):
            console.write("It's already " + targetDoorAction.lower() + ".", "2w1y10w" + str(len(targetDoorAction)) + "w1y", True)
        
        else:
            drawBlankLine = self.stopActions(console, galaxyList, player)

            if targetDoorAction == "Open" and currentRoom.door[targetDir]["Status"] == "Locked" and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
                console.write("It's locked.", "2w1y8w1y", drawBlankLine)
            else:
                unlockString = ""
                unlockCode = ""
                if currentRoom.door[targetDir]["Status"] == "Locked" and targetDoorAction == "Open":
                    unlockString = "unlock and "
                    unlockCode = "11w"

                currentRoom.door[targetDir]["Status"] = targetDoorAction

                if currentRoom.exit[targetDir] != None:
                    otherRoom = None
                    if len(currentRoom.exit[targetDir]) == 3 and currentRoom.spaceshipObject != None:
                        otherRoom = currentRoom.spaceshipObject.areaList[currentRoom.exit[targetDir][1]].roomList[currentRoom.exit[targetDir][2]]
                    elif len(currentRoom.exit[targetDir]) == 5:
                        otherRoom = Room.exists(galaxyList, None, currentRoom.exit[targetDir][0], currentRoom.exit[targetDir][1], currentRoom.exit[targetDir][2], currentRoom.exit[targetDir][3], currentRoom.exit[targetDir][4])
                    if otherRoom != None:
                        otherRoomExitDir = None
                        for exitDir in otherRoom.exit:
                            exitData = otherRoom.exit[exitDir]
                            if exitData != None and currentRoom.sameRoomCheck(exitData):
                                otherRoomExitDir = exitDir
                                break

                        if otherRoomExitDir != None:
                            otherRoom.door[otherRoomExitDir]["Status"] = targetDoorAction

                console.write("You " + unlockString + targetAction.lower() + " the door to the " + targetDir + ".", "4w" + unlockCode + str(len(targetAction)) + "w17w" + str(len(targetDir)) + "w1y", drawBlankLine)

    def lockUnlockDoorCheck(self, console, galaxyList, player, currentRoom, targetAction, targetDirKey):
        if targetAction == "Lock":
            targetActionStatus = "Locked"
        else:
            targetActionStatus = "Closed"

        targetDir = Room.getTargetDirection(targetDirKey)
        if currentRoom.door[targetDir] == None:
            console.write("There is no door in that direction.", "34w1y", True)
        elif "Password" not in currentRoom.door[targetDir]:
            haveString = "require a key"
            if targetAction == "Lock":
                haveString = "have a lock"
            console.write("That door doesn't " + haveString + ".", "15w1y2w" + str(len(haveString)) + "w1y", True)
        elif currentRoom.door[targetDir]["Type"] == "Automatic":
            console.write("That door " + targetAction.lower() + "s automatically.", "10w" + str(len(targetAction)) + "w15w1y", True)
        elif currentRoom.door[targetDir]["Status"] == targetActionStatus:
            console.write("It's already " + targetAction.lower() + "ed.", "2w1y10w" + str(len(targetAction)) + "w2w1y", True)
        
        else:
            drawBlankLine = self.stopActions(console, galaxyList, player)

            if self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
                console.write("You lack the key.", "16w1y", drawBlankLine)
            else:
                closeString = ""
                closeCode = ""
                if targetRoom.door[targetDir]["Status"] == "Open" and targetActionStatus == "Locked":
                    closeString = "close and "
                    closeCode = "10w"

                targetRoom.door[targetDir]["Status"] = targetActionStatus
                
                if targetRoom.exit[targetDir] != None:
                    otherRoom = None
                    if len(targetRoom.exit[targetDir]) == 3 and targetRoom.spaceshipObject != None:
                        otherRoom = targetRoom.spaceshipObject.areaList[targetRoom.exit[targetDir][1]].roomList[targetRoom.exit[targetDir][2]]
                    elif len(targetRoom.exit[targetDir]) == 5:
                        otherRoom = Room.exists(galaxyList, None, targetRoom.exit[targetDir][0], targetRoom.exit[targetDir][1], targetRoom.exit[targetDir][2], targetRoom.exit[targetDir][3], targetRoom.exit[targetDir][4])
                    if otherRoom != None:
                        otherRoomExitDir = None
                        for exitDir in otherRoom.exit:
                            exitData = otherRoom.exit[exitDir]
                            if exitData != None and targetRoom.sameRoomCheck(exitData):
                                otherRoomExitDir = exitDir
                                break

                        if otherRoomExitDir != None:
                            otherRoom.door[otherRoomExitDir]["Status"] = targetActionStatus
                        
                console.write("You " + closeString + targetAction.lower() + " the door to the " + targetDir + ".", "4w" + closeCode + str(len(targetAction)) + "w17w" + str(len(targetDir)) + "w1y", drawBlankLine)

    def openCloseTargetCheck(self, console, galaxyList, player, currentRoom, targetAction, targetObjectKey):
        targetObject = currentRoom.getTargetObject(targetObjectKey)
        if targetObject == None:
            targetObject, playerItemLocation = self.getTargetItem(targetObjectKey)

        if currentRoom.isLit(galaxyList, player, self) == False:
            console.write("It's too dark to see.", "2w1y17w1y", True)
        elif targetObject == None:
            console.write("You don't see anything like that.", "7w1y24w1y", True)
        elif hasattr(targetObject, "dominantHand") == True:
            console.write("You can't " + targetAction.lower() + " that!", "7w1y2w" + str(len(targetAction)) + "w5w1y", True)
        
        elif isinstance(targetObject, Spaceship):
            if targetObject.password != None and self.hasKey(targetObject.password) == False:
                console.write("It's locked.", "2w1y8w1y", True)
            else:
                console.write("The hatch " + targetAction.lower() + "s automatically.", "10w" + str(len(targetAction)) + "w15w1y", True)
            
        elif isinstance(targetObject, Item):
            if targetObject.containerList == None:
                console.write("It doesn't " + targetAction.lower() + ".", "8w1y2w" + str(len(targetAction)) + "w1y", True)
            else:
                console.write("There is no need to " + targetAction.lower() + " it.", "20w" + str(len(targetAction)) + "w3w1y", True)
            
    def lockUnlockTargetCheck(self, console, galaxyList, player, currentRoom, targetAction, targetObjectKey):
        targetObject = currentRoom.getTargetObject(targetObjectKey)
        if targetObject == None:
            targetObject, playerItemLocation = self.getTargetItem(targetObjectKey)
            
        if currentRoom.isLit(galaxyList, player, self) == False:
            console.write("It's too dark to see.", "2w1y17w1y", True)
        elif targetObject == None:
            console.write("You don't see anything like that.", "7w1y24w1y", True)
        
        elif hasattr(targetObject, "dominantHand") == True:
            console.write("You can't " + targetAction.lower() + " that!", "7w1y2w" + str(len(targetAction)) + "w5w1y", True)
        
        elif isinstance(targetObject, Spaceship):
            if targetObject.password == None:
                console.write("The hatch doesn't have a lock.", "15w1y13w1y", True)
            else:
                console.write("The hatch " + targetAction.lower() + "s automatically.", "10w" + str(len(targetAction)) + "w15w1y", True)
        
        elif isinstance(targetObject, Item):
            if targetObject.containerList == None:
                console.write("It doesn't " + targetAction.lower() + ".", "8w1y2w" + str(len(targetAction)) + "w1y", True)
            else:
                console.write("There is no need to " + targetAction.lower() + " it.", "20w" + str(len(targetAction)) + "w3w1y", True)

    def getCheck(self, console, galaxyList, player, currentRoom, targetItemKey, targetContainerKey, count, overrideContainer=None, messageDataList=[]):
        drawBlankLine = True
        if overrideContainer == None:
            drawBlankLine = self.stopActions(console, galaxyList, player)

        targetContainer = overrideContainer

        itemList = currentRoom.itemList
        playerItemLocation = None
        if targetContainerKey != None:
            if targetContainerKey == "All":
                itemList = "All Room Containers"
            else:
                itemList, playerItemLocation = self.getTargetItem(targetContainerKey)
                if itemList == None:
                    itemList = currentRoom.getTargetObject(targetContainerKey)

        if targetContainerKey not in [None, "All"] and itemList != None and (isinstance(itemList, Item) == False or itemList.containerList == None):
            console.write("That's not a container!", "4w1y17w1y", drawBlankLine)
        else:
            if targetContainer != None:
                combinedItemList = [targetContainer]
            elif targetItemKey == "All" and (targetContainerKey in ["All", None]) and count == "All":
                combinedItemList = currentRoom.itemList
            else:
                combinedItemList = currentRoom.itemList + self.getAllItemList()
            if isinstance(itemList, Item):
                itemList = itemList.containerList

            getItem = None
            if itemList != None:
                if targetItemKey != "All":
                    if itemList == "All Room Containers":
                        breakCheck = False
                        for container in combinedItemList:
                            if container.containerList != None:
                                for item in container.containerList:
                                    if targetItemKey in item.keyList:
                                        getItem = item
                                        breakCheck = True
                                        break
                            if breakCheck:
                                break
                    else:
                        for item in itemList:
                            if targetItemKey in item.keyList:
                                getItem = item
                                break
            
            if itemList == None or (targetItemKey != "All" and getItem == None):
                console.write("You can't find it.", "7w1y9w1y", drawBlankLine)

            else:
                if targetContainer != None:
                    itemList = targetContainer.containerList
                if itemList == "All Room Containers":
                    itemCount = 0
                    for container in combinedItemList:
                        if container.containerList != None and len(container.containerList) > 0:
                            itemCount += len(container.containerList)
                else:
                    itemCount = len(itemList)

                if targetContainerKey == "All" and itemCount == 0:
                    console.write("There is nothing to loot.", "24w1y", drawBlankLine)
                
                else:
                    getCount = 0
                    quantityCount = count
                    getContainerIndexList = []
                    noGetCheck = False
                    tooMuchWeightCheck = False
                    breakCheck = False
                    for c in range(itemCount):
                        containerCount = 1
                        copyCheck = None
                        if targetContainerKey == "All":
                            containerCount = len(combinedItemList)
                        for containerIndex in range(containerCount):
                            delIndex = -1
                            tempContainerLocation = None
                            if combinedItemList[containerIndex] in currentRoom.itemList : tempContainerLocation = "Room"
                                
                            if targetContainerKey == "All":
                                itemList = combinedItemList[containerIndex].containerList
                                if itemList == None : itemList = []
                            for i, item in enumerate(itemList):
                                if targetItemKey == "All" or targetItemKey in item.keyList:
                                    if "No Get" in item.flags:
                                        noGetCheck = True
                                    elif (self.getWeight() + item.getWeight(False) > self.getMaxWeight()) and \
                                    (targetContainerKey == None or (playerItemLocation == None and tempContainerLocation == "Room")):
                                        tooMuchWeightCheck = True
                                    else:
                                        if hasattr(item, "quantity") == True and item.quantity != None:
                                            if quantityCount != "All" : getQuantity = quantityCount
                                            else : getQuantity = item.quantity
                                            if getQuantity > item.quantity:
                                                getQuantity = item.quantity
                                            if playerItemLocation == None and tempContainerLocation == "Room" and getQuantity * item.getWeight(False) > self.getMaxWeight() - self.getWeight():
                                                getQuantity = int((self.getMaxWeight() - self.getWeight()) / item.getWeight(False))
                                            if getQuantity < item.quantity:
                                                item.quantity -= getQuantity
                                                copyCheck = True
                                            else:
                                                copyCheck = False

                                            inventoryQuantityItem, unused = self.getTargetItem(item.num, ["Inventory"], item.pocket)
                                            if inventoryQuantityItem != None:
                                                if hasattr(inventoryQuantityItem, "quantity") == True and inventoryQuantityItem.quantity != None:
                                                    inventoryQuantityItem.quantity += getQuantity
                                            else:
                                                if item.pocket in self.itemDict:
                                                    splitItem = copy.deepcopy(item)
                                                    splitItem.quantity = getQuantity
                                                    self.itemDict[item.pocket].append(splitItem)
                                            getCount += getQuantity
                                            if quantityCount != "All":
                                                quantityCount -= getCount
                                        else:
                                            self.itemDict[item.pocket].append(item)
                                            getCount += 1

                                        if getItem == None:
                                            getItem = item
                                        elif getItem != "Multiple" and (getItem.num != item.num or getItem.pocket != item.pocket):
                                            getItem = "Multiple"
                                        if containerIndex not in getContainerIndexList:
                                            getContainerIndexList.append(containerIndex)
                                        if targetContainerKey != None:
                                            if targetContainer == None:
                                                if targetContainerKey == "All":
                                                    targetContainer = combinedItemList[containerIndex]
                                                else:
                                                    if playerItemLocation != None : targetContainer, containerLoc = self.getTargetItem(targetContainerKey, [playerItemLocation])
                                                    else : targetContainer = currentRoom.getTargetObject(targetContainerKey, ["Items"])
                                                    
                                        if copyCheck != True:
                                            delIndex = i
                                        break
                            if delIndex != -1:
                                del itemList[delIndex]
                                break
                            elif copyCheck != None:
                                break
                        if (count != "All" and getCount >= count) or (count != "All" and copyCheck != None and getCount >= count):
                            break
                        elif count != "All" and ((getItem == None or (tooMuchWeightCheck == True or noGetCheck == True)) and containerIndex == containerCount - 1):
                            break
                        
                    if getCount == 0:
                        if tooMuchWeightCheck == True:
                            console.write("You can't carry that much weight.", "7w1y24w1y", drawBlankLine)
                        elif noGetCheck == True:
                            console.write("You can't pick that up.", "7w1y14w1y", drawBlankLine)
                        elif itemCount == 0:
                            console.write("There is nothing to get.", "23w1y", drawBlankLine)
                        else:
                            console.write("You can't pick anything up.", "7w1y18w1y", drawBlankLine)
                    else:
                        if targetContainerKey == "All" and getCount > 1 and (count == "All" or len(getContainerIndexList) > 1):
                            modString = ""
                            modCode = ""
                            if tooMuchWeightCheck == False and targetItemKey == "All":
                                modString = "every corner of "
                                modCode = "16w"
                            consonle.write("You loot " + modString + "the place.", "9w" + modCode + "9w1y", drawBlankLine)
                        elif targetContainerKey == None and getItem == "Multiple" and getCount > 1 and getCount == itemCount and overrideContainer == None:
                            console.write("You pick everything up.", "22w1y", drawBlankLine)
                        elif getItem == "Multiple":
                            if targetContainerKey == "All" : totalContainerCount = len(combinedItemList)
                            else:
                                if playerItemLocation != None : totalContainerCount = len(self.getAllItemList([playerItemLocation]))
                                else : totalContainerCount = len(currentRoom.itemList)
                            
                            if (targetContainerKey != None and getContainerIndexList[-1] < totalContainerCount) or overrideContainer != None:
                                if overrideContainer != None:
                                    stringHalf1 = "You get some things out of " + targetContainer.prefix.lower() + " " + targetContainer.name["String"] + "."
                                    stringHalf2 = ""
                                    codeHalf1 = "27w" + str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"] + "1y"
                                    codeHalf2 = ""
                                    drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != "Get Check"))
                                    combineLinesCheck = self.num != None
                                    stackDisplayMessage(messageDataList, "Get Check", stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                                else:
                                    console.write("You get some things out of " + targetContainer.prefix.lower() + " " + targetContainer.name["String"] + ".", "27w" + str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"] + "1y", drawBlankLine)
                            else:
                                console.write("You pick some things up.", "23w1y", drawBlankLine)
                        
                        elif getItem != "Multiple":
                            countString, countCode = getCountString(getCount)
                            fromString = ""
                            fromCode = ""
                            if targetContainerKey == "All" : totalContainerCount = len(combinedItemList)
                            else:
                                if playerItemLocation != None : totalContainerCount = len(self.getAllItemList([playerItemLocation]))
                                else : totalContainerCount = len(currentRoom.itemList)
                            if (targetContainerKey != None and getContainerIndexList[0] < totalContainerCount) or overrideContainer != None:
                                targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                                targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                                if currentRoom.isLit(galaxyList, player, self) == False:
                                    targetContainerString = "something"
                                    targetContainerCode = "9w"
                                fromString = " from " + targetContainerString
                                fromCode = "6w" + targetContainerCode
                            pickUpString = "pick up "
                            pickUpCode = "8w"
                            if targetContainer != None:
                                pickUpString = "get "
                                pickUpCode = "4w"
                            itemNameString = getItem.prefix.lower() + " " + getItem.name["String"]
                            itemNameCode = str(len(getItem.prefix)) + "w1w" + getItem.name["Code"]
                            if getItem.num == Item.getSpecialItemNum("Corpse"):
                                itemNameString = "a corpse"
                                itemNameCode = "8w"
                            getString = "You " + pickUpString + itemNameString + countString + fromString + "."
                            getCode = "4w" + pickUpCode + itemNameCode + countCode + fromCode + "1y"

                            if overrideContainer != None:
                                stringHalf1 = getString
                                stringHalf2 = ""
                                codeHalf1 = getCode
                                codeHalf2 = ""
                                drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != "Get Check"))
                                combineLinesCheck = self.num != None
                                stackDisplayMessage(messageDataList, "Get Check", stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                            else:
                                console.write(getString, getCode, drawBlankLine)
        
        return messageDataList

    def putCheck(self, console, galaxyList, player, currentRoom, targetItemKey, targetContainerKey, count):
        drawBlankLine = self.stopActions(console, galaxyList, player)

        targetContainer, playerItemLocation = self.getTargetItem(targetContainerKey)
        if targetContainer == None:
            targetContainer = currentRoom.getTargetObject(targetContainerKey, ["Mobs", "Items", "Spaceships"])
    
        if targetContainer == None:
            console.write("You can't find it.", "7w1y9w1y", drawBlankLine)
        elif isinstance(targetContainer, Item) == False or targetContainer.containerList == None:
            console.write("That's not a container!", "4w1y17w1y", drawBlankLine)
        
        else:
            putItem = None
            inventorySize = 0
            breakCheck = False
            for pocket in self.itemDict:
                inventorySize += len(self.itemDict[pocket])
                if targetItemKey != "All":
                    for item in self.itemDict[pocket]:
                        if putItem == None and targetItemKey in item.keyList:
                            putItem = item

            if targetItemKey != "All" and putItem == None:
                console.write("You can't find it.", "7w1y9w1y", drawBlankLine)
            elif targetItemKey != "All" and putItem == targetContainer:
                console.write("You can't put something inside itself.", "7w1y29w1y", drawBlankLine)
            elif inventorySize == 0:
                console.write("You don't have anything to put in.", "7w1y25w1y", drawBlankLine)
            elif targetItemKey != "All" and hasattr(targetContainer, "ammoCapacity") and targetContainer.ammoCapacity != None and targetContainer.ammoType == "Arrow" and not (putItem != None and putItem.pocket == "Ammo" and putItem.ammoType == "Arrow" and putItem.ammoCapacity == None):
                console.write("You can only put arrows in that.", "31w1y", drawBlankLine)

            else:
                putCount = 0
                quantityCount = count
                for i in range(inventorySize):
                    breakCheck = False
                    for pocket in self.itemDict:
                        delIndex = -1
                        for i, item in enumerate(self.itemDict[pocket]):
                            if targetContainer.getContainerWeight() + item.getWeight(False) <= targetContainer.containerMaxLimit:
                                if item != targetContainer and (targetItemKey == "All" or targetItemKey in item.keyList):
                                    if not (hasattr(targetContainer, "ammoCapacity") and targetContainer.ammoCapacity != None and targetContainer.ammoType == "Arrow" and not (item.pocket == "Ammo" and item.ammoType == "Arrow" and item.ammoCapacity == None)):
                                        if hasattr(item, "quantity") == True and item.quantity != None:
                                            if quantityCount != "All" : putQuantity = quantityCount
                                            else : putQuantity = item.quantity
                                            if putQuantity > item.quantity:
                                                putQuantity = item.quantity
                                            if putQuantity * item.getWeight(False) > targetContainer.containerMaxLimit - targetContainer.getContainerWeight():
                                                putQuantity = int((targetContainer.containerMaxLimit - targetContainer.getContainerWeight()) / item.getWeight(False))
                                                
                                            containerQuantityItem = targetContainer.getContainerItem(item.num, item.pocket)
                                            if containerQuantityItem != None:
                                                if hasattr(containerQuantityItem, "quantity") == True and containerQuantityItem.quantity != None:
                                                    containerQuantityItem.quantity += putQuantity
                                            else:
                                                splitItem = copy.deepcopy(item)
                                                splitItem.quantity = putQuantity
                                                targetContainer.containerList.append(splitItem)

                                            if putQuantity < item.quantity:
                                                item.quantity -= putQuantity
                                            else:
                                                delIndex = i

                                            putCount += putQuantity
                                            if quantityCount != "All":
                                                quantityCount -= putCount
                                        else:
                                            targetContainer.containerList.append(item)
                                            putCount += 1
                                            delIndex = i

                                        if putItem == None:
                                            putItem = item
                                        elif putItem != "Multiple" and (putItem.num != item.num or putItem.pocket != item.pocket):
                                            putItem = "Multiple"
                                        breakCheck = True
                                        break
                        if delIndex != -1:
                            del self.itemDict[pocket][i]
                        if breakCheck == True:
                            break
                    if count != "All" and putCount == count:
                        break

                if putCount == 0 and len(self.getAllItemList(["Inventory"])) > 0 and targetItemKey != "All":
                    console.write("It won't fit.", "6w1y5w1y", drawBlankLine)
                elif putCount == 0:
                    console.write("You don't have anything to put in.", "7w1y25w1y", drawBlankLine)
                elif putItem == "Multiple":
                    targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                    targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                    if currentRoom.isLit(galaxyList, player, self) == False:
                        targetContainerString = "something"
                        targetContainerCode = "9w"
                    displayString = "You put some things in " + targetContainerString + "."
                    displayCode = "23w" + targetContainerCode + "1y"
                    console.write(displayString, displayCode, drawBlankLine)
                else:
                    countString, countCode = getCountString(putCount)
                    targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                    targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                    if currentRoom.isLit(galaxyList, player, self) == False:
                        targetContainerString = "something"
                        targetContainerCode = "9w"
                    displayString = "You put " + putItem.prefix.lower() + " " + putItem.name["String"] + countString + " in " + targetContainerString + "."
                    displayCode = "8w" + str(len(putItem.prefix)) + "w1w" + putItem.name["Code"] + countCode + "4w" + targetContainerCode + "1y"
                    console.write(displayString, displayCode, drawBlankLine)
                
    def dropCheck(self, console, galaxyList, player, currentRoom, targetItemKey, count, pocketKey=None):
        drawBlankLine = self.stopActions(console, galaxyList, player)

        if pocketKey != None:
            pocketKey = pocketKey[0].upper() + pocketKey[1::].lower()

        dropItem = None
        breakCheck = False
        if targetItemKey != "All":
            for pocket in self.itemDict:
                for item in self.itemDict[pocket]:
                    if targetItemKey in item.keyList:
                        dropItem = item
                        breakCheck = True
                        break
                if breakCheck:
                    break

        if targetItemKey != "All" and dropItem == None:
            console.write("You can't find it.", "7w1y9w1y", drawBlankLine)

        else:
            dropCount = 0
            quantityCount = count
            delDict = {}
            breakCheck = False
            for pocket in self.itemDict:
                delDict[pocket] = []
                for i, item in enumerate(self.itemDict[pocket]):
                    if (targetItemKey == "All" or targetItemKey in item.keyList) and not (pocketKey != None and pocket != pocketKey):
                        if hasattr(item, "quantity") == True and item.quantity != None:
                            if quantityCount != "All" : dropQuantity = quantityCount
                            else : dropQuantity = item.quantity
                            if dropQuantity > item.quantity:
                                dropQuantity = item.quantity
                            roomQuantityItem = currentRoom.getTargetObject(item.num, ["Items"], item.pocket)
                            if roomQuantityItem != None:
                                if hasattr(roomQuantityItem, "quantity") == True and roomQuantityItem.quantity != None:
                                    roomQuantityItem.quantity += dropQuantity
                            else:
                                splitItem = copy.deepcopy(item)
                                splitItem.quantity = dropQuantity
                                currentRoom.itemList.append(splitItem)

                            if dropQuantity < item.quantity:
                                item.quantity -= dropQuantity
                            else:
                                delDict[pocket].append(i)
                            dropCount += dropQuantity
                            if quantityCount != "All":
                                quantityCount -= dropCount
                        else:
                            currentRoom.itemList.append(item)
                            dropCount += 1
                            delDict[pocket].append(i)

                        if dropItem == None:
                            dropItem = item
                        elif dropItem != "Multiple" and (dropItem.num != item.num or dropItem.pocket != item.pocket):
                            dropItem = "Multiple"

                        if count != "All" and dropCount >= count:
                            breakCheck = True
                            break
                if breakCheck:
                    break

            inventoryCount = 0
            for pocket in self.itemDict:
                inventoryCount += len(self.itemDict[pocket])

            for pocket in delDict:
                delDict[pocket].reverse()
                for i in delDict[pocket]:
                    del self.itemDict[pocket][i]

            if dropCount == 0:
                console.write("You aren't carrying anything.", "8w1y19w1y", drawBlankLine)
            elif dropCount > 1 and dropCount == inventoryCount:
                console.write("You drop everything on the ground.", "33w1y", drawBlankLine)    
            elif dropItem == "Multiple":
                console.write("You drop some things on the ground.", "34w1y", drawBlankLine)
            elif dropItem != None:
                itemNameString = dropItem.prefix.lower() + " " + dropItem.name["String"]
                itemNameCode = str(len(dropItem.prefix)) + "w1w" + dropItem.name["Code"]
                if dropItem.num == Item.getSpecialItemNum("Corpse"):
                    itemNameString = "a corpse"
                    itemNameCode = "8w"
                countString, countCode = getCountString(dropCount)
                dropString = "You drop " + itemNameString + " on the ground." + countString
                dropCode = "9w" + itemNameCode + "14w1y" + countCode
                console.write(dropString, dropCode, drawBlankLine)

    def wearCheck(self, console, galaxyList, player, targetItemKey, count, targetGearSlotIndex=None):
        drawBlankLine = self.stopActions(console, galaxyList, player)

        wearItem = None
        otherItem = None
        if targetItemKey != "All":
            for item in self.itemDict["Armor"] + self.itemDict["Weapon"]:
                if targetItemKey in item.keyList:
                    wearItem = item
                    break
            if wearItem == None:
                for item in self.getAllItemList(["Inventory"]):
                    if targetItemKey in item.keyList:
                        otherItem = item
                        break
        
        if targetItemKey != "All" and otherItem != None:
            console.write("You can't wear that.", "7w1y11w1y", drawBlankLine)
        elif targetItemKey != "All" and wearItem == None:
            console.write("You can't find it.", "7w1y9w1y", drawBlankLine)
        elif targetItemKey != "All" and wearItem.pocket == "Weapon":
            tempCount = count
            if tempCount == "All":
                tempCount = 2
            self.wieldCheck(console, galaxyList, player, targetItemKey, targetGearSlotIndex, tempCount)
            return

        else:
            wearCount = 0
            wearItem = None
            delInvList = []
            previousWornItemList = []
            wornItemSlotList = []
            breakCheck = False
            for itemIndex, item in enumerate(self.itemDict["Armor"]):
                if item.gearSlot != None and item.gearSlot in self.gearDict:
                    targetGearSlot = self.gearDict[item.gearSlot]
                    slotRange = 1
                    if targetGearSlotIndex == None and isinstance(targetGearSlot, list):
                        slotRange = len(targetGearSlot)
                    for slotIndex in range(slotRange):
                        if isinstance(self.gearDict[item.gearSlot], list) and count == 1 and self.gearDict[item.gearSlot][0] != None and self.gearDict[item.gearSlot][1] == None:
                            slotIndex = 1
                        elif isinstance(self.gearDict[item.gearSlot], list) and item.gearSlot in wornItemSlotList:
                            slotIndex = 1
                                    
                        if targetGearSlotIndex != None:
                            if targetGearSlotIndex in ["left", "lef", "le", "l"]:
                                targetGearSlotIndex = 0
                            elif targetGearSlotIndex in ["right", "righ", "rig", "ri", "r"]:
                                targetGearSlotIndex = 1
                            elif stringIsNumber(targetGearSlotIndex):
                                targetGearSlotIndex = int(targetGearSlotIndex)
                            if isinstance(self.gearDict[item.gearSlot], list):
                                if targetGearSlotIndex > len(self.gearDict[item.gearSlot]) - 1:
                                    targetGearSlotIndex = len(self.gearDict[item.gearSlot]) - 1
                            slotIndex = targetGearSlotIndex
                            
                        if isinstance(self.gearDict[item.gearSlot], list):
                            targetGearSlot = self.gearDict[item.gearSlot][slotIndex]
                        if targetGearSlot == None or targetItemKey != "All":
                            if targetItemKey == "All" or targetItemKey in item.keyList:
                                if isinstance(self.gearDict[item.gearSlot], list):
                                    if True:
                                        if self.gearDict[item.gearSlot][slotIndex] != None:
                                            previousWornItemList.append(self.gearDict[item.gearSlot][slotIndex])
                                        if item.gearSlot not in wornItemSlotList:
                                            wornItemSlotList.append(item.gearSlot)
                                        self.gearDict[item.gearSlot][slotIndex] = item
                                        wearCount += 1
                                else:
                                    if True:
                                        if self.gearDict[item.gearSlot] != None:
                                            previousWornItemList.append(self.gearDict[item.gearSlot])
                                        if item.gearSlot not in wornItemSlotList:
                                            wornItemSlotList.append(item.gearSlot)
                                        self.gearDict[item.gearSlot] = item
                                        wearCount += 1
                                        
                                if wearItem != "Multiple":
                                    if wearItem == None:
                                        wearItem = item
                                    elif wearItem.num != item.num or wearItem.pocket != item.pocket:
                                        wearItem = "Multiple"
                                delInvList.append(itemIndex)

                                if count != "All" and wearCount >= count:
                                    breakCheck = True
                                break
                if breakCheck:
                    break

            delInvList.reverse()
            for delIndex in delInvList:
                del self.itemDict["Armor"][delIndex]
            for wornItem in previousWornItemList:
                self.itemDict[wornItem.pocket].append(wornItem)

            # Messages #
            if wearCount == 0 and len(self.itemDict["Armor"]) == 0:
                console.write("You don't have any gear to wear.", "7w1y23w1y", drawBlankLine)    
            elif wearCount == 0:
                console.write("You are already wearing something.", "33w1y", drawBlankLine)    
            elif len(previousWornItemList) > 0 and wearCount > 1:
                console.write("You switch around some of your gear.", "35w1y", drawBlankLine)
            elif len(previousWornItemList) == 0 and wearCount > 1 and wearItem == "Multiple":
                console.write("You put on some armor.", "21w1y", drawBlankLine)
            elif len(previousWornItemList) == 1 and isinstance(wearItem, Item):
                wearString = "You remove " + previousWornItemList[0].prefix.lower() + " " + previousWornItemList[0].name["String"] + " and wear " + wearItem.prefix.lower() + " " + wearItem.name["String"] + "."
                wearCode = "11w" + str(len(previousWornItemList[0].prefix)) + "w1w" + previousWornItemList[0].name["Code"] + "10w" + str(len(wearItem.prefix)) + "w1w" + wearItem.name["Code"] + "1y"
                console.write(wearString, wearCode, drawBlankLine)
            elif len(previousWornItemList) == 0 and isinstance(wearItem, Item):
                wearString = "You wear " + wearItem.prefix.lower() + " " + wearItem.name["String"] + " on your " + wearItem.gearSlot.lower() + "."
                wearCode = "9w" + str(len(wearItem.prefix)) + "w1w" + wearItem.name["Code"] + "9w" + str(len(wearItem.gearSlot)) + "w1y"
                countString = ""
                countCode = ""
                if wearItem != "Multiple" and wearCount > 1:
                    countString = " (" + str(wearCount) + ")"
                    countCode = "2r" + str(len(str(wearCount))) + "w1r"
                console.write(wearString + countString, wearCode + countCode, drawBlankLine)

            # Wield Check #
            if targetItemKey == "All" and count == "All":
                self.wieldCheck(console, galaxyList, player, "All", None, 2, False)

    def wieldCheck(self, console, galaxyList, player, targetItemKey, targetGearSlotKey, count, blankCheck=True):
        drawBlankLine = self.stopActions(console, galaxyList, player)

        wieldItem = None
        checkItem = None
        for pocket in self.itemDict:
            for item in self.itemDict[pocket]:
                if targetItemKey == "All" or targetItemKey in item.keyList:
                    if item.pocket == "Weapon" and wieldItem == None:
                        wieldItem = item
                    if checkItem == None:
                        checkItem = item

        if targetItemKey == "All" and (wieldItem == None or wieldItem.pocket != "Weapon"):
            if blankCheck == True:
                console.write("You don't have anything to wield.", "7w1y24w1y", drawBlankLine)
        elif wieldItem == None and checkItem != None and checkItem.pocket != "Weapon":
            console.write("You can't wield that.", "7w1y12w1y", blankCheck == True and drawBlankLine)
        elif wieldItem == None:
            console.write("You can't find it.", "7w1y9w1y", blankCheck == True and drawBlankLine)
        elif wieldItem.pocket != "Weapon":
            console.write("You can't wield that.", "7w1y12w1y", blankCheck == True and drawBlankLine)

        else:
            targetGearSlot = None
            if targetGearSlotKey != None:
                if stringIsNumber(targetGearSlotKey) == False:
                    if targetGearSlotKey in ["left", "lef", "le", "l"]:
                        targetGearSlot = "Left Hand"
                    elif targetGearSlotKey in ["right", "righ", "rig", "ri", "r"]:
                        targetGearSlot = "Right Hand"
                else:
                    if int(targetGearSlotKey) == 1 : targetGearSlot = "Left Hand"
                    else : targetGearSlot = "Right Hand"
                if wieldItem != None and wieldItem.twoHanded and (self.debugDualWield == False or "Disable Dual Wielding" in wieldItem.flags):
                    targetGearSlot = self.dominantHand
            else:
                if wieldItem.twoHanded == False and self.debugDualWield == True and self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].twoHanded == True and self.gearDict[self.getOppositeHand(self.dominantHand)] == None:
                    targetGearSlot = self.getOppositeHand(self.dominantHand)

            wieldCount = 0
            slotCount = 0
            slotItem = None
            breakCheck = False
            for c in range(count):
                defaultGearSlot = self.dominantHand
                if (targetItemKey == "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[defaultGearSlot].twoHanded == False and (self.debugDualWield == False or "Disable Dual Wielding" in self.gearDict[defaultGearSlot].flags)) or \
                (targetItemKey != "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[self.getOppositeHand(defaultGearSlot)] == None and self.gearDict[defaultGearSlot].twoHanded == False and wieldItem.twoHanded == False and count == 1) or \
                (c == 1 and not (self.gearDict[defaultGearSlot] != None and self.gearDict[defaultGearSlot].twoHanded == True and (self.debugDualWield == False or "Disable Dual Wielding" in self.gearDict[defaultGearSlot].flags))) or \
                (targetItemKey != "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[self.getOppositeHand(defaultGearSlot)] == None and wieldItem.twoHanded == True and "Disable Dual Wielding" not in wieldItem.flags and self.debugDualWield == True and "Disable Dual Wielding" not in self.gearDict[defaultGearSlot].flags):
                    defaultGearSlot = self.getOppositeHand(self.dominantHand)
                if targetGearSlot != None:
                    defaultGearSlot = targetGearSlot
                delIndex = -1
                for i, item in enumerate(self.itemDict["Weapon"]):
                    if targetItemKey == "All" or targetItemKey in item.keyList:
                        if not (targetItemKey == "All" and self.gearDict[defaultGearSlot] != None) and \
                        not (targetItemKey == "All" and item.twoHanded == True and (self.gearDict[self.dominantHand] != None or self.gearDict[self.getOppositeHand(self.dominantHand)] != None) and (self.debugDualWield == False or "Disable Dual Wielding" in item.flags)):
                            if self.gearDict[defaultGearSlot] != None:
                                self.itemDict[self.gearDict[defaultGearSlot].pocket].append(self.gearDict[defaultGearSlot])
                                slotCount += 1
                                if slotItem == None:
                                    slotItem = self.gearDict[defaultGearSlot]
                                elif slotItem != "Multiple" and (slotItem.num != self.gearDict[defaultGearSlot].num or slotItem.pocket != self.gearDict[defaultGearSlot].pocket):
                                    slotItem = "Multiple"
                            oppositeHand = self.gearDict[self.getOppositeHand(defaultGearSlot)]
                            if oppositeHand != None and (item.twoHanded == True or oppositeHand.twoHanded == True) and (self.debugDualWield == False or ((item.twoHanded == True and "Disable Dual Wielding" in item.flags) or (oppositeHand.twoHanded == True and "Disable Dual Wielding" in oppositeHand.flags))):
                                self.itemDict[oppositeHand.pocket].append(oppositeHand)
                                self.gearDict[self.getOppositeHand(defaultGearSlot)] = None
                                slotCount += 1
                                if slotItem == None:
                                    slotItem = oppositeHand
                                elif slotItem != "Multiple" and (slotItem.num != oppositeHand.num or slotItem.pocket != oppositeHand.pocket):
                                    slotItem = "Multiple"
                            self.gearDict[defaultGearSlot] = item
                            wieldCount += 1
                            if wieldItem == None:
                                wieldItem = item
                            elif wieldItem != "Multiple" and (wieldItem.num != item.num or wieldItem.pocket != item.pocket):
                                wieldItem = "Multiple"
                            delIndex = i
                            break
                if delIndex != -1:
                    if self.itemDict["Weapon"][delIndex].twoHanded == True and (self.debugDualWield == False or "Disable Dual Wielding" in self.itemDict["Weapon"][delIndex].flags):
                        breakCheck = True
                    del self.itemDict["Weapon"][delIndex]
                if breakCheck:
                    break

            if wieldCount == 0:
                if blankCheck == True:
                    console.write("You're already holding something.", "3w1y28w1y", drawBlankLine)
            elif wieldItem == "Multiple":
                if slotItem == None:
                    console.write("You hold some weapons in your hands.", "35w1y", blankCheck == True and drawBlankLine)
                else:
                    console.write("You switch some weapons around.", "30w1y", blankCheck == True and drawBlankLine)
            elif slotItem == None:
                countString = ""
                countCode = ""
                handsString = defaultGearSlot.lower()
                handsCode = str(len(defaultGearSlot)) + "w"
                if wieldCount == 2 or wieldItem.twoHanded == True:
                    if wieldItem.twoHanded == False:
                        countString = " (2)"
                        countCode = "2r1w1r"
                    if self.debugDualWield == False:
                        handsString = "hands"
                        handsCode = "5w"
                displayString = "You hold " + wieldItem.prefix.lower() + " " + wieldItem.name["String"] + countString + " in your " + handsString + "."
                displayCode = "9w" + str(len(wieldItem.prefix)) + "w1w" + wieldItem.name["Code"] + countCode + "9w" + handsCode + "1y"
                console.write(displayString, displayCode, blankCheck == True and drawBlankLine)
            else:
                slotString = "some gear"
                slotCode = "9w"
                slotCountString = ""
                slotCountCode = ""
                wieldString = "some gear"
                wieldCode = "9w"
                wieldCountString = ""
                wieldCountCode = ""
                if slotItem != "Multiple":
                    slotString = slotItem.prefix.lower() + " " + slotItem.name["String"]
                    slotCode = str(len(slotItem.prefix)) + "w1w" + slotItem.name["Code"]
                    if slotCount > 1:
                        slotCountString = " (2)"
                        slotCountCode = "2r1w1r"
                if wieldItem != "Multiple":
                    handsString = defaultGearSlot.lower()
                    if slotItem == "Multiple" or (wieldItem.twoHanded == True and self.debugDualWield == False):
                        handsString = "hands"
                    wieldString = wieldItem.prefix.lower() + " " + wieldItem.name["String"] + " in your " + handsString
                    wieldCode = str(len(wieldItem.prefix)) + "w1w" + wieldItem.name["Code"] + "9w" + str(len(handsString)) + "w"
                    if wieldCount > 1:
                        wieldCountString = " (2)"
                        wieldCountCode = "2r1w1r"
                displayString = "You remove " + slotString + slotCountString + " and wield " + wieldString + "." + wieldCountString
                displayCode = "11w" + slotCode + slotCountCode + "11w" + wieldCode + "1y" + wieldCountCode
                console.write(displayString, displayCode, blankCheck == True and drawBlankLine)

    def removeCheck(self, console, galaxyList, player, targetItemKey, count, targetGearSlotIndex=None):
        drawBlankLine = self.stopActions(console, galaxyList, player)

        removeItem = None
        if targetItemKey != "All":
            for gearSlot in self.gearDict:

                # Focus On Dominant Hand First #
                if targetItemKey not in ["All", None] and targetGearSlotIndex == None:
                    if gearSlot == "Left Hand" and self.dominantHand != "Left Hand":
                        gearSlot = "Right Hand"
                    elif gearSlot == "Right Hand" and self.dominantHand == "Right Hand":
                        gearSlot = "Left Hand"

                # Focus On Target Hand Only #
                if isinstance(targetGearSlotIndex, str):
                    if targetGearSlotIndex == "left":
                        gearSlot = "Left Hand"
                    elif targetGearSlotIndex == "right":
                        gearSlot = "Right Hand"

                targetGearSlot = self.gearDict[gearSlot]
                slotRange = 1
                if targetGearSlotIndex == None and isinstance(targetGearSlot, list):
                    slotRange = len(targetGearSlot)
                for slotIndex in range(slotRange):
                    if isinstance(self.gearDict[gearSlot], list):
                        targetGearSlot = self.gearDict[gearSlot][slotIndex]
                    if targetGearSlot != None:
                        if targetItemKey in targetGearSlot.keyList:
                            removeItem = targetGearSlot
                            break
        
        if targetItemKey != "All" and removeItem == None:
            console.write("You can't find it.", "7w1y9w1y", drawBlankLine)

        else:
            removeCount = 0
            breakCheck = False
            removeItem = None
            removeHand = None
            for gearSlot in self.gearDict:

                # Focus On Dominant Hand First #
                if targetItemKey not in ["All", None] and targetGearSlotIndex == None:
                    if gearSlot == "Left Hand" and self.dominantHand != "Left Hand":
                        gearSlot = "Right Hand"
                    elif gearSlot == "Right Hand" and self.dominantHand == "Right Hand":
                        gearSlot = "Left Hand"

                # Focus On Target Hand Only #
                if isinstance(targetGearSlotIndex, str):
                    if targetGearSlotIndex == "left":
                        gearSlot = "Left Hand"
                    elif targetGearSlotIndex == "right":
                        gearSlot = "Right Hand"

                slotRange = 1
                if targetGearSlotIndex == None and isinstance(self.gearDict[gearSlot], list):
                    slotRange = len(self.gearDict[gearSlot])
                for slotIndex in range(slotRange):
                    targetGearSlot = self.gearDict[gearSlot]
                    if isinstance(self.gearDict[gearSlot], list):
                        if isinstance(targetGearSlotIndex, int):
                            if targetGearSlotIndex >= len(self.gearDict[gearSlot]):
                                targetGearSlotIndex = len(self.gearDict[gearSlot]) - 1
                            slotIndex = targetGearSlotIndex
                        targetGearSlot = self.gearDict[gearSlot][slotIndex]
                    
                    if targetGearSlot != None:
                        if targetItemKey == "All" or targetItemKey in targetGearSlot.keyList:
                            self.itemDict[targetGearSlot.pocket].append(targetGearSlot)
                            removeCount += 1
                            if removeItem != "Multiple":
                                if removeItem == None:
                                    removeItem = targetGearSlot
                                elif removeItem.num != targetGearSlot.num or removeItem.pocket != targetGearSlot.pocket:
                                    removeItem = "Multiple"
                            if isinstance(self.gearDict[gearSlot], list):
                                self.gearDict[gearSlot][slotIndex] = None
                            else:
                                self.gearDict[gearSlot] = None
                            if gearSlot in ["Left Hand", "Right Hand"]:
                                removeHand = gearSlot

                            if count != "All" and removeCount >= count:
                                breakCheck = True
                                break
                if breakCheck:
                    break

            # Messages #
            if removeCount == 0:
                displayMessage = "You have nothing to remove."
                displayCode = "26w1y"
                console.write(displayMessage, displayCode, drawBlankLine)
            elif targetItemKey == "All" and count == "All" and removeItem == "Multiple":
                displayString = "You remove all of your gear."
                displayCode = "27w1y"
                if random.randrange(10) == 0:
                    displayString = "You strip down to your birthday suit."
                    displayCode = "36w1y"
                console.write(displayString, displayCode, drawBlankLine)
            elif removeItem == "Multiple":
                console.write("You remove some gear.", "20w1y", drawBlankLine)
            elif isinstance(removeItem, Item):
                countString, countCode = getCountString(removeCount)
                holdingString = " remove"
                if removeItem.pocket == "Weapon":
                    holdingString = " stop wielding"
                handString = ""
                if removeHand in ["Left Hand", "Right Hand"]:
                    handString = " in your " + removeHand.lower()
                displayString = "You" + holdingString + " " + removeItem.prefix + " " + removeItem.name["String"] + handString + "." + countString
                displayCode = "3w" + str(len(holdingString)) + "w1w" + str(len(removeItem.prefix)) + "w1w" + removeItem.name["Code"] + str(len(handString)) + "w1y" + countCode
                console.write(displayString, displayCode, drawBlankLine)

    def switchCheck(self, console):
        oldHand = self.dominantHand
        if self.dominantHand == "Left Hand":
            newHand = "Right Hand"
        else:
            newHand = "Left Hand"
        self.dominantHand = newHand

        targetWeapon = None
        if self.gearDict[oldHand] != None and self.gearDict[oldHand].twoHanded == True and self.debugDualWield == False:
            self.gearDict[newHand] = self.gearDict[oldHand]
            self.gearDict[oldHand] = None

        if targetWeapon != None:
            displayString = "You switch " + targetWeapon.prefix.lower() + " " + targetWeapon.name["String"] + " to your " + newHand.lower() + "."
            displayCode = "11w" + str(len(targetWeapon.prefix)) + "w1w" + targetWeapon.name["Code"] + "9w" + str(len(newHand)) + "w1y"
            console.write(displayString, displayCode, True)
        else:
            console.write("You switch your dominant hand to your " + self.dominantHand.lower() + ".", "38w" + str(len(self.dominantHand)) + "w1y", True)

    def reloadCheck(self, console, galaxyList, player, currentRoom, reloadKey, reloadSlotKey, ammoKey, autoReload=False, messageDataList=[]):
        if currentRoom.isLit(galaxyList, player, self) == False:
            if autoReload == False:
                console.write("It's too dark to see.", "2w1y17w1y", True)

        else:
            reloadSlot = None
            if reloadSlotKey not in ["All", None]:
                if reloadSlotKey in ["left", "lef", "le", "l", "1"] : reloadSlot = "Left Hand"
                else : reloadSlot = "Right Hand"
                if reloadSlot != self.dominantHand and self.gearDict[reloadSlot] == None and self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].twoHanded == True:
                    reloadSlot = self.getOppositeHand(reloadSlot)

            reloadList = []
            targetItem = None
            gunInventoryCount = 0
            if reloadSlot != None:
                if self.gearDict[reloadSlot] != None:
                    if self.gearDict[reloadSlot].pocket == "Weapon" and self.gearDict[reloadSlot].isGun():
                        reloadList.append(self.gearDict[reloadSlot])
                    else:
                        targetItem = self.gearDict[reloadSlot]
            elif reloadKey == "All":
                if self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].pocket == "Weapon" and self.gearDict[self.dominantHand].isGun():
                    reloadList.append(self.gearDict[self.dominantHand])
                if self.gearDict[self.getOppositeHand(self.dominantHand)] != None and self.gearDict[self.getOppositeHand(self.dominantHand)].pocket == "Weapon" and self.gearDict[self.getOppositeHand(self.dominantHand)].isGun():
                    reloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
                if reloadSlotKey == "All":
                    for pocket in self.itemDict:
                        for item in self.itemDict[pocket]:
                            if pocket == "Weapon" and item.isGun():
                                reloadList.append(item)
                                gunInventoryCount += 1
            else:
                if self.gearDict["Left Hand"] != None and reloadKey in self.gearDict["Left Hand"].keyList:
                    if self.gearDict["Left Hand"].isGun():
                        reloadList.append(self.gearDict["Left Hand"])
                    else:
                        targetItem = self.gearDict["Left Hand"]
                elif self.gearDict["Right Hand"] != None and reloadKey in self.gearDict["Right Hand"].keyList:
                    if self.gearDict["Right Hand"].isGun():
                        reloadList.append(self.gearDict["Right Hand"])
                    else:
                        targetItem = self.gearDict["Right Hand"]
                else:
                    for item in self.getAllItemList(["Inventory"]):
                        if reloadKey in item.keyList:
                            if item.pocket == "Weapon" and item.isGun():
                                reloadList.append(item)
                                targetItem = None
                                break
                            else:
                                targetItem = item

            reloadTargetShiftCheck = False
            if reloadKey not in ["All", None] and reloadSlotKey == None and ammoKey == None:
                if len(reloadList) == 0:
                    reloadTargetShiftCheck = True
                    if self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].isGun() and reloadKey in self.gearDict[self.dominantHand].keyList:
                        reloadList.append(self.gearDict[self.dominantHand])
                    if self.gearDict[self.getOppositeHand(self.dominantHand)] != None and self.gearDict[self.getOppositeHand(self.dominantHand)].isGun() and reloadKey in self.gearDict[self.getOppositeHand(self.dominantHand)].keyList:
                        reloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
                            
            alreadyReloadedCheck = False
            if reloadKey == "All" and len(reloadList) > 0 and ammoKey == None:
                alreadyReloadedCheck = True
                for weapon in reloadList:
                    if weapon.isLoaded(self.itemDict["Ammo"]) == False:
                        alreadyReloadedCheck = False
                        break 
            
            if reloadKey not in ["All", None] and len(reloadList) == 0 and targetItem != None and (targetItem.pocket != "Weapon" or targetItem.isGun() == False):
                console.write("You can't reload that.", "7w1y13w1y", True)
            elif alreadyReloadedCheck == True:
                displayString = "It's already loaded."
                displayCode = "2w1y16w1y"
                if len(reloadList) > 1:
                    displayString = "Your weapons are already loaded."
                    displayCode = "31w1y"
                console.write(displayString, displayCode, True)
            elif reloadKey == "All" and len(reloadList) == 0:
                console.write("You don't have anything to reload.", "7w1y25w1y", True)
            elif reloadKey not in ["All", None] and len(reloadList) == 0 and targetItem == None:
                console.write("You can't find it.", "7w1y9w1y", True)
            elif (reloadSlot != None or reloadKey not in ["All", None]) and len(reloadList) == 0 and targetItem != None and not (reloadKey not in ["All", None] and reloadSlotKey == None and ammoKey == None):
                console.write("You can't reload that.", "7w1y13w1y", True)
            elif reloadSlot != None and len(reloadList) == 0 and targetItem == None:
                console.write("You aren't holding anything.", "8w1y18w1y", True)

            else:
                drawBlankLine = False
                if autoReload == False:
                    drawBlankLine = self.stopActions(console, galaxyList, player)

                flags = self.reloadFunction(copy.deepcopy(self), copy.deepcopy(reloadList), reloadTargetShiftCheck, reloadKey, ammoKey)
                requireWeapon = flags["requireWeapon"]
                magazineCheck = flags["magazineCheck"]
                reloadCount = flags["reloadCount"]
                targetAmmo = flags["targetAmmo"]
                reloadWeapon = flags["reloadWeapon"]

                if autoReload == False and requireWeapon != None and magazineCheck == False and reloadCount == 0 and not (requireWeapon.ammoCapacity == None and requireWeapon.magazine != None):
                    displayString = "It requires a " + requireWeapon.ammoType + "."
                    displayCode = "14w" + str(len(requireWeapon.ammoType)) + "w1y"
                    if requireWeapon.ammoCapacity == None:
                        displayString = "You don't have a " + requireWeapon.ammoType + " magazine."
                        displayCode = "7w1y9w" + str(len(requireWeapon.ammoType)) + "w9w1y"
                    console.write(displayString, displayCode, drawBlankLine)
                elif autoReload == False and reloadCount == 0 and reloadKey != "All":
                    if ammoKey != None and targetAmmo == None:
                        console.write("You don't have that ammo.", "7w1y16w1y", drawBlankLine)
                    elif ammoKey == None and targetAmmo == None:
                        console.write("You don't have any ammo.", "7w1y15w1y", drawBlankLine)
                    else:
                        console.write("It's already loaded.", "2w1y16w1y", drawBlankLine)
                elif autoReload == False and reloadCount == 0 and reloadKey == "All":
                    if ammoKey != None and targetAmmo == None:
                        console.write("You don't have that ammo.", "7w1y16w1y", drawBlankLine)
                    elif ammoKey == None and targetAmmo == None:
                        console.write("You don't have any ammo.", "7w1y15w1y", drawBlankLine)
                    elif gunInventoryCount == 1:
                        console.write("It's already loaded.", "2w1y16w1y", drawBlankLine)
                    else:
                        console.write("Your weapons are already loaded.", "31w1y", drawBlankLine)
                elif autoReload == False and reloadCount == 0 and ammoCheck == False:
                    thatString = "any"
                    if ammoKey != None:
                        thatString = "that"
                    console.write("You don't have " + thatString + " ammo.", "7w1y7w" + str(len(thatString)) + "w5w1y", drawBlankLine)
                
                elif reloadWeapon == "Multiple":
                    actionFlags = {"Reload List":reloadList, "Reload Target Shift Check":reloadTargetShiftCheck, "Reload Key":reloadKey, "Ammo Key":ammoKey}
                    self.actionList.append(Action("Reload", actionFlags))
                    
                    if autoReload == True:
                        stringHalf1 = "You start reloading some weapons.."
                        stringHalf2 = ""
                        codeHalf1 = "32w2y"
                        codeHalf2 = ""
                        drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != "Reload Check"))
                        combineLinesCheck = self.num != None
                        stackDisplayMessage(messageDataList, "Reload Check", stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                    else:
                        console.write("You start reloading some weapons..", "32w2y", drawBlankLine)
                    drawBlankLine = False

                elif reloadWeapon != None:
                    actionFlags = {"Reload List":reloadList, "Reload Target Shift Check":reloadTargetShiftCheck, "Reload Key":reloadKey, "Ammo Key":ammoKey}
                    self.actionList.append(Action("Reload", actionFlags))

                    countString = ""
                    countCode = ""
                    if reloadWeapon != "Multiple" and reloadCount > 1:
                        countString = " (" + str(reloadCount) + ")"
                        countCode = "2r" + str(len(str(reloadCount))) + "w1r"

                    if autoReload == True:
                        stringHalf1 = "You start reloading " + reloadWeapon.prefix.lower() + " " + reloadWeapon.name["String"] + ".." + countString
                        stringHalf2 = ""
                        codeHalf1 = "20w" + str(len(reloadWeapon.prefix)) + "w1w" + reloadWeapon.name["Code"] + "2y" + countCode
                        codeHalf2 = ""
                        drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != "Reload Check"))
                        combineLinesCheck = self.num != None
                        stackDisplayMessage(messageDataList, "Reload Check", stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                    else:
                        console.write("You start reloading " + reloadWeapon.prefix.lower() + " " + reloadWeapon.name["String"] + ".." + countString, "20w" + str(len(reloadWeapon.prefix)) + "w1w" + reloadWeapon.name["Code"] + "2y" + countCode, drawBlankLine)
                    drawBlankLine = False

        return messageDataList

    def reloadCompleteAction(self, console, flags):
        reloadList = flags["Reload List"]
        reloadTargetShiftCheck = flags["Reload Target Shift Check"]
        reloadKey = flags["Reload Key"]
        ammoKey = flags["Ammo Key"]

        flags = self.reloadFunction(self, reloadList, reloadTargetShiftCheck, reloadKey, ammoKey)
        reloadWeapon = flags["reloadWeapon"]
        reloadCount = flags["reloadCount"]

        if reloadWeapon != "Multiple":
            displayString = "You finish reloading " + reloadWeapon.prefix.lower() + " " + reloadWeapon.name["String"] + "."
            displayCode = "21w" + str(len(reloadWeapon.prefix)) + "w1w" + reloadWeapon.name["Code"] + "1y"
            countString = ""
            countCode = ""
            if reloadCount > 1:
                countString = " (" + str(reloadCount) + ")"
                countCode = "2r" + str(len(str(reloadCount))) + "w1y"
            console.write(displayString + countString, displayCode + countCode, True)
        else:
            displayString = "You finish reloading."
            displayCode = "20w1y"
            console.write(displayString, displayCode, True)

    def reloadFunction(self, targetPlayer, reloadList, reloadTargetShiftCheck, reloadKey, ammoKey):
        magazineCheck = False
        reloadCount = 0
        reloadWeapon = None
        requireWeapon = None
        for weaponIndex, weapon in enumerate(reloadList):
            ammoCheck = False
            targetAmmo = None
            targetMagazine = None
            ammoIndex = -1
            reloadQuantity = 0
            targetMagazine = None
            heldMagazineCheck = False

            # Non-Magazine Weapons #
            if weapon.ammoCapacity != None:
                targetAmmo, ammoIndex = targetPlayer.ammoCheck(weapon.ammoType)
                if ammoKey != None:
                    targetAmmo, ammoIndex = targetPlayer.ammoCheck(weapon.ammoType, ammoKey)
                elif reloadTargetShiftCheck == True:
                    targetAmmo, ammoIndex = targetPlayer.ammoCheck(weapon.ammoType, reloadKey)

                if weapon.magazine == None or weapon.magazine.quantity < weapon.ammoCapacity or (targetAmmo != None and weapon.magazine.num != targetAmmo.num):
                    if ammoIndex != -1 and not (reloadKey == "All" and ammoKey == None and weapon.magazine != None and weapon.magazine.num != targetAmmo.num):
                        if weapon.magazine != None and weapon.magazine.num != targetAmmo.num:
                            inventoryAmmo, unused = targetPlayer.getTargetItem(weapon.magazine.num, ["Inventory"]. weapon.magazine.pocket)
                            if inventoryAmmo != None:
                                inventoryAmmo.quantity += weapon.magazine.quantity
                            else:
                                targetPlayer.itemDict["Ammo"].append(weapon.magazine)
                            weapon.magazine = None

                        alreadyLoadedCount = 0
                        if weapon.magazine != None:
                            alreadyLoadedCount = weapon.magazine.quantity
                        reloadQuantity = weapon.ammoCapacity - alreadyLoadedCount
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
                        elif reloadWeapon != "Multiple" and (reloadWeapon.num != weapon.num or reloadWeapon.pocket != weapon.pocket):
                            reloadWeapon = "Multiple"

            # Magazine Weapons #
            else:
                targetMagazine, magazineIndex = targetPlayer.ammoCheck(weapon.ammoType, None, True)
                if magazineIndex != -1:
                    magazineCheck = True
                else:
                    requireWeapon = weapon
                if weapon.magazine != None or magazineIndex != -1:
                    targetAmmo, ammoIndex = targetPlayer.ammoCheck(weapon.ammoType)
                    if ammoKey != None:
                        targetAmmo, ammoIndex = targetPlayer.ammoCheck(weapon.ammoType, ammoKey)
                    elif reloadTargetShiftCheck == True:
                        targetAmmo, ammoIndex = targetPlayer.ammoCheck(weapon.ammoType, reloadKey)

                    if ammoIndex != -1 and not (reloadKey == "All" and ammoKey == None and weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and weapon.magazine.flags["Ammo"].num != targetAmmo.num):
                        if weapon.magazine == None or weapon.magazine.flags["Ammo"] == None or weapon.magazine.flags["Ammo"].quantity < weapon.magazine.ammoCapacity or weapon.isLoaded(targetPlayer.itemDict["Ammo"]) == False or (targetAmmo != None and weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and targetAmmo.num != weapon.magazine.flags["Ammo"].num):
                            weaponMagazine = weapon.magazine
                            if weaponMagazine == None:
                                weaponMagazine = targetMagazine
                                heldMagazineCheck = True
                            elif weaponMagazine != None and targetMagazine != None and weaponMagazine.ammoCapacity < targetMagazine.ammoCapacity:
                                targetPlayer.itemDict["Ammo"].append(weaponMagazine)
                                if weaponMagazine.flags["Ammo"] != None:
                                    heldAmmo, unused = targetPlayer.getTargetItem(weaponMagazine.flags["Ammo"].num, ["Inventory"], weaponMagazine.flags["Ammo"].pocket)
                                    if heldAmmo != None:
                                        heldAmmo.quantity += weaponMagazine.flags["Ammo"].quantity
                                    else:
                                        targetPlayer.itemDict["Ammo"].append(weaponMagazine.flags["Ammo"])
                                    weaponMagazine.flags["Ammo"] = None
                                weaponMagazine = targetMagazine

                            if weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and weapon.magazine.flags["Ammo"].num != targetAmmo.num:
                                inventoryAmmo, unused = targetPlayer.getTargetItem(weapon.magazine.flags["Ammo"].num, ["Inventory"], weaponMagazine.flags["Ammo"].pocket)
                                if inventoryAmmo != None:
                                    inventoryAmmo.quantity += weapon.magazine.flags["Ammo"].quantity
                                else:
                                    targetPlayer.itemDict["Ammo"].append(weapon.magazine.flags["Ammo"])
                                weapon.magazine.flags["Ammo"] = None
                                
                            alreadyLoadedCount = 0
                            if weaponMagazine.flags["Ammo"] != None:
                                alreadyLoadedCount = weaponMagazine.flags["Ammo"].quantity
                            reloadQuantity = weaponMagazine.ammoCapacity - alreadyLoadedCount
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
                            elif reloadWeapon.num != weapon.num or reloadWeapon.pocket != weapon.pocket:
                                reloadWeapon = "Multiple"

            if targetAmmo != None:
                if reloadQuantity >= targetAmmo.quantity:
                    del targetPlayer.itemDict["Ammo"][ammoIndex]
                else:
                    targetAmmo.quantity -= reloadQuantity
            if targetMagazine != None and ammoCheck == True and heldMagazineCheck == True:
                if targetMagazine in targetPlayer.itemDict["Ammo"]:
                    magazineIndex = targetPlayer.itemDict["Ammo"].index(targetMagazine)
                    del targetPlayer.itemDict["Ammo"][magazineIndex]
        
        returnFlags = {}
        returnFlags["requireWeapon"] = requireWeapon
        returnFlags["magazineCheck"] = magazineCheck
        returnFlags["reloadCount"] = reloadCount
        returnFlags["targetAmmo"] = targetAmmo
        returnFlags["reloadWeapon"] = reloadWeapon
        return returnFlags

    def autoReload(self, config, console, galaxyList, player, currentRoom, shootGunDataList, messageDataList):
        autoReloadCheck = False
        if len(shootGunDataList) == 2 and shootGunDataList[0]["Weapon Data"].isEmpty(True) and shootGunDataList[1]["Weapon Data"].isEmpty(True):
            if self.ammoCheck(shootGunDataList[0]["Weapon Data"].ammoType, shootGunDataList[0]["Last Used Ammo Name"])[0] != None:
                messageDataList = self.reloadCheck(console, galaxyList, player, currentRoom, "All", None, shootGunDataList[0]["Last Used Ammo Name"], True, messageDataList)
                autoReloadCheck = True
            elif self.ammoCheck(shootGunDataList[1]["Weapon Data"].ammoType, shootGunDataList[1]["Last Used Ammo Name"])[0] != None:
                messageDataList = self.reloadCheck(console, galaxyList, player, currentRoom, "All", None, shootGunDataList[1]["Last Used Ammo Name"], True, messageDataList)
                autoReloadCheck = True
            elif self.ammoCheck(shootGunDataList[0]["Weapon Data"].ammoType)[0] != None or self.ammoCheck(shootGunDataList[1]["Weapon Data"].ammoType)[0] != None:
                messageDataList = self.reloadCheck(console, galaxyList, player, currentRoom, "All", None, None, True, messageDataList)
                autoReloadCheck = True
        else:
            for shootGunData in shootGunDataList:
                if shootGunData["Weapon Data"].isEmpty(True) == True:
                    if self.ammoCheck(shootGunData["Weapon Data"].ammoType, shootGunData["Last Used Ammo Name"])[0] != None:
                        messageDataList = self.reloadCheck(console, galaxyList, player, currentRoom, shootGunData["Weapon Data"].name["String"].lower(), None, shootGunData["Last Used Ammo Name"], True, messageDataList)
                        autoReloadCheck = True
                        break
                    elif self.ammoCheck(shootGunData["Weapon Data"].ammoType)[0] != None:
                        messageDataList = self.reloadCheck(console, galaxyList, player, currentRoom, shootGunData["Weapon Data"].name["String"].lower(), None, None, True, messageDataList)
                        autoReloadCheck = True
                        break

        return messageDataList, autoReloadCheck

    def unloadCheck(self, console, galaxyList, player, currentRoom, unloadKey, unloadSlotKey, ammoKey):
        if currentRoom.isLit(galaxyList, player, self) == False:
            console.write("It's too dark to see.", "2w1y17w1y", True)

        else:
            unloadSlot = None
            if unloadSlotKey != None:
                if unloadSlotKey in ["left", "lef", "le", "l", "1"] : unloadSlot = "Left Hand"
                else : unloadSlot = "Right Hand"
                if unloadSlot != self.dominantHand and self.gearDict[unloadSlot] == None and self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].twoHanded == True:
                    unloadSlot = self.getOppositeHand(unloadSlot)

            unloadList = []
            targetItem = None
            roomItem = None
            if unloadSlot != None:
                if self.gearDict[unloadSlot] != None:
                    if self.gearDict[unloadSlot].pocket == "Weapon" and self.gearDict[unloadSlot].isGun():
                        unloadList.append(self.gearDict[unloadSlot])
                    else:
                        targetItem = self.gearDict[unloadSlot]
            elif unloadKey == "All":
                if self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].pocket == "Weapon" and self.gearDict[self.dominantHand].isGun():
                    unloadList.append(self.gearDict[self.dominantHand])
                if self.gearDict[self.getOppositeHand(self.dominantHand)] != None and self.gearDict[self.getOppositeHand(self.dominantHand)].pocket == "Weapon" and self.gearDict[self.getOppositeHand(self.dominantHand)].isGun():
                    unloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
                for item in self.itemDict["Weapon"]:
                    if item.isGun():
                        unloadList.append(item)
            elif unloadKey == None:
                if self.gearDict[self.dominantHand] != None:
                    if self.gearDict[self.dominantHand].pocket == "Weapon" and self.gearDict[self.dominantHand].isGun():
                        unloadList.append(self.gearDict[self.dominantHand])
                if self.gearDict[self.getOppositeHand(self.dominantHand)] != None:
                    if self.gearDict[self.getOppositeHand(self.dominantHand)].pocket == "Weapon" and self.gearDict[self.getOppositeHand(self.dominantHand)].isGun():
                        unloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
            else:
                if self.gearDict[self.dominantHand] != None and unloadKey in self.gearDict[self.dominantHand].keyList:
                    if self.gearDict[self.dominantHand].pocket == "Weapon" and self.gearDict[self.dominantHand].isGun():
                        unloadList.append(self.gearDict[self.dominantHand])
                    else:
                        targetItem = self.gearDict[self.dominantHand]
                elif self.gearDict[self.getOppositeHand(self.dominantHand)] != None and unloadKey in self.gearDict[self.getOppositeHand(self.dominantHand)].keyList:
                    if self.gearDict[self.getOppositeHand(self.dominantHand)].pocket == "Weapon" and self.gearDict[self.getOppositeHand(self.dominantHand)].isGun():
                        unloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
                    else:
                        targetItem = self.gearDict[self.getOppositeHand(self.dominantHand)]
                elif self.getTargetItem(unloadKey, ["Gear"])[0] != None and unloadKey in self.getTargetItem(unloadKey, ["Gear"])[0].keyList:
                    searchItem = self.getTargetItem(unloadKey, ["Gear"])[0]
                    if searchItem.pocket == "Weapon" and searchItem.isGun():
                        unloadList.append(searchItem)
                    else:
                        targetItem = searchItem
                elif self.getTargetItem(unloadKey, ["Inventory"])[0] != None:
                    searchItem = self.getTargetItem(unloadKey, ["Inventory"])[0]
                    if searchItem.pocket == "Weapon" and searchItem.isGun():
                        unloadList.append(searchItem)
                    else:
                        targetItem = searchItem
                elif currentRoom.getTargetObject(unloadKey, ["Items"]) != None:
                    searchItem = currentRoom.getTargetObject(unloadKey, ["Items"])
                    if searchItem.pocket == "Weapon" and searchItem.isGun():
                        unloadList.append(searchItem)
                    else:
                        targetItem = searchItem
                    roomItem = searchItem

            alreadyUnloadedCheck = False
            if unloadKey == "All" and len(unloadList) > 0 and ammoKey == None:
                alreadyUnloadedCheck = True
                for weapon in unloadList:
                    if weapon.isEmpty() == False:
                        alreadyUnloadedCheck = False
                        break

            if unloadKey not in ["All", None] and len(unloadList) == 0 and targetItem != None and (targetItem.pocket != "Weapon" or targetItem.isGun() == False):
                console.write("You can't unload that.", "7w1y13w1y", True)
            elif alreadyUnloadedCheck == True:
                displayString = "It's already unloaded."
                displayCode = "2w1y18w1y"
                if len(unloadList) > 1:
                    displayString = "Your weapons are already unloaded."
                    displayCode = "33w1y"
                console.write(displayString, displayCode, True)
            elif unloadKey == "All" and len(unloadList) == 0:
                console.write("You don't have anything to unload.", "7w1y25w1y", True)
            elif unloadKey not in ["All", None] and len(unloadList) == 0 and targetItem == None:
                console.write("You can't find it.", "7w1y9w1y", True)
            elif (unloadSlot != None or unloadKey not in ["All", None]) and len(unloadList) == 0 and targetItem != None and not (unloadKey not in ["All", None] and unloadSlotKey == None and ammoKey == None):
                console.write("You can't unload that.", "7w1y13w1y", True)
            elif unloadSlot != None and len(unloadList) == 0 and targetItem == None:
                console.write("You aren't holding anything.", "8w1y18w1y", True)

            else:
                drawBlankLine = self.stopActions(console, galaxyList, player)

                flags = self.unloadFunction(copy.deepcopy(self), copy.deepcopy(unloadList), roomItem, ammoKey)
                unloadWeapon = flags["unloadWeapon"]
                unloadCount = flags["unloadCount"]
                tooMuchWeightCheck = flags["tooMuchWeightCheck"]
                shellCount = flags["shellCount"]

                if ammoKey != None and unloadCount == 0:
                    console.write("You can't find that ammo.", "7w1y16w1y", drawBlankLine)
                elif unloadCount == 0 and tooMuchWeightCheck == True:
                    console.write("You can't carry that much weight.", "7w1y24w1y", drawBlankLine)
                elif unloadKey not in ["All", None] and unloadCount == 0 and len(unloadList) == 0:
                    console.write("You can't unload that.", "7w1y13w1y", drawBlankLine)
                elif unloadKey not in ["All", None] and unloadCount == 0 and unloadList[0].isEmpty():
                    console.write("It's already unloaded.", "2w1y18w1y", drawBlankLine)
                elif unloadKey == "All" and unloadCount == 0 and unloadList[0].isEmpty():
                    console.write("Your weapons are already unloaded.", "33w1y", drawBlankLine)
                elif unloadWeapon == "Multiple":
                    actionFlags = {"unloadList":unloadList, "roomItem":roomItem, "ammoKey":ammoKey, "shellCount":shellCount}
                    self.actionList.append(Action("Unload", actionFlags))

                    console.write("You start unloading some weapons..", "32w2y", drawBlankLine)
                elif unloadWeapon != None:
                    actionFlags = {"unloadList":unloadList, "roomItem":roomItem, "ammoKey":ammoKey, "shellCount":shellCount}
                    self.actionList.append(Action("Unload", actionFlags))

                    countString = ""
                    countCode = ""
                    if unloadWeapon != "Multiple" and unloadCount > 1:
                        countString = " (" + str(unloadCount) + ")"
                        countCode = "2r" + str(len(str(unloadCount))) + "w1r"
                    console.write("You start unloading " + unloadWeapon.prefix.lower() + " " + unloadWeapon.name["String"] + ".." + countString, "20w" + str(len(unloadWeapon.prefix)) + "w1w" + unloadWeapon.name["Code"] + "2y" + countCode, drawBlankLine)

    def unloadCompleteAction(self, console, flags):
        unloadList = flags["unloadList"]
        roomItem = flags["roomItem"]
        ammoKey = flags["ammoKey"]

        flags = self.unloadFunction(self, unloadList, roomItem, ammoKey)
        unloadWeapon = flags["unloadWeapon"]
        unloadCount = flags["unloadCount"]
        targetAmmo = flags["targetAmmo"]
        targetMagazine = flags["targetMagazine"]
        magazineCount = flags["magazineCount"]
        shellCount = flags["shellCount"]

        if unloadWeapon == "Multiple" or magazineCount > 1:
            console.write("You finish unloading your weapons.", "33w1y", True)

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
            console.write("You unload " + unloadString + " from " + unloadWeapon.prefix.lower() + " " + unloadWeapon.name["String"] + "." + countString, "11w" + unloadCode + "6w" + str(len(unloadWeapon.prefix)) + "w1w" + unloadWeapon.name["Code"] + "1y" + countCode, True)

    def unloadFunction(self, targetPlayer, unloadList, roomItem, ammoKey):
        unloadWeapon = None
        unloadCount = 0
        targetAmmo = None
        shellCount = 0
        targetMagazine = None
        magazineCount = 0
        tooMuchWeightCheck = False
        for weaponIndex, weapon in enumerate(unloadList):
            
            # Non-Magazine Weapons #
            if weapon.ammoCapacity != None and weapon.magazine != None:
                if not (ammoKey != None and ammoKey not in weapon.magazine.keyList):
                    getQuantity = weapon.magazine.quantity
                    if roomItem != None and targetPlayer.getWeight() + roomItem.getWeight() > targetPlayer.getMaxWeight():
                        getQuantity = 0
                        tooMuchWeightCheck = True
                        if targetPlayer.getWeight() + roomItem.getWeight(False) <= targetPlayer.getMaxWeight():
                            getQuantity = int((targetPlayer.getMaxWeight() - targetPlayer.getWeight()) / roomItem.getWeight(False))

                    if getQuantity > 0:
                        shellCount += getQuantity
                        inventoryAmmo, unused = targetPlayer.getTargetItem(weapon.magazine.num, ["Inventory"], weapon.magazine.pocket)
                        if inventoryAmmo != None:
                            inventoryAmmo.quantity += getQuantity
                        else:
                            splitItem = copy.deepcopy(weapon.magazine)
                            splitItem.quantity = getQuantity
                            targetPlayer.itemDict["Ammo"].append(splitItem)
                        targetAmmo = weapon.magazine
                        if getQuantity == weapon.magazine.quantity:
                            weapon.magazine = None
                        else:
                            weapon.magazine.quantity -= getQuantity

                        if unloadWeapon == None:
                            unloadWeapon = weapon
                        elif unloadWeapon != "Multiple" and (unloadWeapon.num != weapon.num or unloadWeapon.pocket != weapon.pocket):
                            unloadWeapon = "Multiple"
                        unloadCount += 1

            # Magazine Weapons #
            elif weapon.magazine != None:
                if not (ammoKey != None and weapon.magazine.flags["Ammo"] != None and ammoKey not in weapon.magazine.flags["Ammo"].keyList):
                    getQuantity = 0
                    if weapon.magazine.flags["Ammo"] != None:
                        getQuantity = weapon.magazine.flags["Ammo"].quantity
                    if roomItem != None and weapon.magazine.flags["Ammo"] != None and targetPlayer.getWeight() + weapon.magazine.flags["Ammo"].getWeight() > targetPlayer.getMaxWeight():
                        getQuantity = 0
                        tooMuchWeightCheck = True
                        if targetPlayer.getWeight() + weapon.magazine.flags["Ammo"].getWeight(False) <= targetPlayer.getMaxWeight():
                            getQuantity = int((targetPlayer.getMaxWeight() - targetPlayer.getWeight()) / weapon.magazine.flags["Ammo"].getWeight(False))

                    if getQuantity > 0:
                        shellCount += getQuantity
                        inventoryAmmo, unused = targetPlayer.getTargetItem(weapon.magazine.flags["Ammo"].num, ["Inventory"], weapon.magazine.flags["Ammo"].pocket)
                        if inventoryAmmo != None:
                            inventoryAmmo.quantity += getQuantity
                        else:
                            splitItem = copy.deepcopy(weapon.magazine.flags["Ammo"])
                            splitItem.quantity = getQuantity
                            targetPlayer.itemDict["Ammo"].append(splitItem)
                        targetAmmo = weapon.magazine.flags["Ammo"]
                        if getQuantity == weapon.magazine.flags["Ammo"].quantity:
                            weapon.magazine.flags["Ammo"] = None
                        else:
                            weapon.magazine.flags["Ammo"].quantity -= getQuantity

                    magazineCheck = False
                    if roomItem != None and targetPlayer.getWeight() + weapon.magazine.getWeight() > targetPlayer.getMaxWeight():
                        tooMuchWeightCheck = True
                    else:
                        targetPlayer.itemDict["Ammo"].append(weapon.magazine)
                        targetMagazine = weapon.magazine
                        weapon.magazine = None
                        magazineCheck = True
                        magazineCount += 1
                    
                    if getQuantity > 0 or magazineCheck == True:
                        if unloadWeapon == None:
                            unloadWeapon = weapon
                        elif unloadWeapon != "Multiple" and (unloadWeapon.num != weapon.num or unloadWeapon.pocket != weapon.pocket):
                            unloadWeapon = "Multiple"
                        unloadCount += 1

        returnFlags = {}
        returnFlags["unloadWeapon"] = unloadWeapon
        returnFlags["unloadCount"] = unloadCount
        returnFlags["tooMuchWeightCheck"] = tooMuchWeightCheck
        returnFlags["targetAmmo"] = targetAmmo
        returnFlags["shellCount"] = shellCount
        returnFlags["targetMagazine"] = targetMagazine
        returnFlags["magazineCount"] = magazineCount
        return returnFlags

    def recruitCheck(self, console, galaxyList, player, currentRoom, mobKey, mobCount):
        if currentRoom.isLit(galaxyList, player, self) == False:
            console.write("It's too dark to see.", "2w1y17w1y", True)
        elif mobKey in ["All", None] and len(currentRoom.mobList) == 0:
            console.write("There is no one here.", "20w1y", True)
        elif mobKey == None and len(self.targetList) == 0:
            console.write("You aren't targeting anyone.", "8w1y18w1y", True)
        
        else:
            drawBlankLine = self.stopActions(console, galaxyList, player)

            if mobCount in ["All", None]:
                maxRecruitCount = len(currentRoom.mobList)
            else:
                maxRecruitCount = mobCount

            recruitList = []
            recruitMob = None
            alreadyInGroupCheck = False
            currentlyFightingCheck = False
            for mob in currentRoom.mobList:
                if mobKey == "All" or mobKey in mob.keyList or (mobKey == None and mob in self.targetList):
                    if mob in self.recruitList:
                        alreadyInGroupCheck = True
                    elif mob in self.combatList:
                        currentlyFightingCheck = True
                    else:
                        self.recruitList.append(mob)
                        if mob in self.targetList:
                            del self.targetList[self.targetList.index(mob)]
                        recruitList.append(mob)

                        if recruitMob == None:
                            recruitMob = mob
                        elif recruitMob != "Multiple" and recruitMob.num != mob.num:
                            recruitMob = "Multiple"
                        if len(recruitList) > maxRecruitCount:
                            break

            if mobKey not in ["All", None] and len(recruitList) == 0 and alreadyInGroupCheck == False and currentlyFightingCheck == False:
                console.write("You don't see them.", "7w1y10w1y", drawBlankLine)
            elif len(recruitList) == 0 and alreadyInGroupCheck == True:
                themString = "everyone here"
                themCode = "13w"
                if mobCount in [1, None]:
                    themString = "them"
                    themCode = "4w"
                console.write("You've already recruited " + themString + ".", "3w1y21w" + themCode + "1y", drawBlankLine)
            elif len(recruitList) == 0 and currentlyFightingCheck == True:
                console.write("You can't recruit if you're fighting!", "7w1y16w1y11w1y", drawBlankLine)
            elif recruitMob == "Multiple":
                console.write("You welcome some new members to the group.", "41w1y", drawBlankLine)
            else:
                displayString = "You welcome " + recruitMob.prefix.lower() + " " + recruitMob.name["String"] + " to the group."
                displayCode = "12w" + str(len(recruitMob.prefix)) + "w1w" + recruitMob.name["Code"] + "13w1y"
                countString, countCode = getCountString(len(recruitList))
                console.write(displayString + countString, displayCode + countCode, drawBlankLine)

    def disbandCheck(self, console, galaxyList, player, currentRoom, mobKey, mobCount):
        pass

    def displayGroup(self, console, galaxyList):
        console.write("Group Status", "12w", True)
        console.write("--========--", "1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy")
        
        if len(self.recruitList) == 0:
            console.write("-None", "1y4w")

        else:
            for mob in self.recruitList:
                displayString = mob.name["String"] + " [" + str(mob.currentHealth) + " HP]"
                displayCode = mob.name["Code"] + "2y" + str(len(str(mob.currentHealth))) + "r3w1y"
                console.write(displayString, displayCode)

    def stopCheck(self, console, galaxyList, player):
        if len(self.actionList) == 0:
            console.write("You aren't doing anything.", "8w1y16w1y", True)
        elif self.actionList[0].actionType == "Combat Skill" and self.actionList[0].flags["combatSkill"].name["String"] in ["Dodge", "Block"]:
            console.write("You can't stop that!", "7w1y11w1y", True)
        else:
            self.stopActions(console, galaxyList, player)
    
    def attackCheck(self, config, console, galaxyList, player, currentRoom, mobKey, messageDataList=None, autoAttackCheck=False):
        if mobKey == None and len(self.targetList) == 0:
            console.write("Attack who?", "10w1y", True)
        
        else:
            distance = 0
            directionKey = None
            directionCount = None
            if len(self.targetList) > 0 and mobKey == None:
                targetDistance, targetDirection, unused = Room.getTargetRange(galaxyList, currentRoom, self.targetList[0], self.maxLookDistance)
                if targetDistance != -1:
                    distance = targetDistance
                    if targetDistance > 0:
                        directionKey = targetDirection.lower()
                        directionCount = targetDistance

            randomCombatSkill, unused = self.getRandomAttackSkill(self.gearDict[self.dominantHand], None, {"Distance":distance})
            if randomCombatSkill == None:
                randomCombatSkill, unused = self.getRandomAttackSkill(self.gearDict[self.getOppositeHand(self.dominantHand)], None, {"Distance":distance})

            if randomCombatSkill == None:
                console.write("You can't attack from here!", "7w1y18w1y", True)
            elif randomCombatSkill == "Reload":
                console.write("You need to reload first.", "24w1y", True)

            elif isinstance(randomCombatSkill, CombatSkill):
                messageDataList = self.combatSkillCheck(config, console, galaxyList, player, currentRoom, randomCombatSkill, 1, mobKey, directionKey, directionCount, messageDataList, autoAttackCheck)

        return messageDataList

    def combatSkillCheck(self, config, console, galaxyList, player, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount, messageDataList=None, autoAttackCheck=False):
        if len(self.actionList) > 0 and self.actionList[0].actionType == "Combat Skill" and self.actionList[0].flags["combatSkill"].name["String"] in ["Dodge", "Block"]:
            self.actionList = []
            self.actionList.append(Action("Stumble", {}, 3))
            console.write("You trip over yourself trying to do too much at once.", "52w1y", True)

        elif combatSkill.name["String"] in ["Block", "Dodge"]:
            drawBlankLine = True
            if len(self.actionList) > 0:
                drawBlankLine = self.stopActions(console, galaxyList, player)
            
            actionFlags = {"combatSkill":combatSkill}
            self.actionList.append(Action("Combat Skill", actionFlags, 3))
            if self.num != None and currentRoom.sameRoomCheck(player):
                console.write(self.prefix + " " + self.name["String"] + " prepares to attack..", str(len(self.prefix)) + "w1w" + self.name["Code"] + "19w2y", drawBlankLine)
            elif self.num == None:
                console.write("You prepare to " + combatSkill.name["String"] + " an incoming attack..", "15w" + combatSkill.name["Code"] + "19w2y", drawBlankLine)

        else:
            combatSkillRange = combatSkill.maxRange
            if len(combatSkill.weaponTypeList) > 0 and combatSkill.weaponTypeList[0] in [["Bow"], ["Pistol"], ["Rifle"]]:
                combatSkillRange = self.maxLookDistance

            if self.skillWeaponCheck(combatSkill) == False:
                if self.num == None:
                    console.write("You can't use that now.", "7w1y14w1y", True)
            elif combatSkill.weaponTypeList == [["Bow"]] and self.ammoCheck("Arrow")[0] == None:
                if self.num == None:
                    console.write("You don't have any arrows.", "7w1y17w1y", True)
            elif mobKey == None and directionKey == None and len(self.targetList) == 0 and "All Only" not in combatSkill.ruleDict and combatSkill.healCheck == False:
                if self.num == None:
                    console.write("You aren't targeting anyone.", "8w1y18w1y", True)
            elif ((directionCount != None and directionCount > combatSkillRange) or (mobKey == None and len(self.targetList) > 0 and Room.getTargetRange(galaxyList, currentRoom, self.targetList[0], combatSkillRange)[0] == -1)):
                if self.num == None:
                    console.write("That's too far.", "4w1y9w1y", True)
            elif mobKey == None and "From Another Room" in combatSkill.ruleDict and Room.getTargetRange(galaxyList, currentRoom, self.targetList[0], combatSkillRange)[0] == 0:
                if self.num == None:
                    console.write("You're too close!", "3w1y12w1y", True)
            elif mobKey == "Self" and combatSkill.healCheck == False:
                if self.num == None:
                    console.write("You can't use it on yourself.", "7w1y20w1y", True)
            
            else:
                message = None
                roomDistance = 0
                targetRoom = currentRoom
                targetDirection = None
                if mobKey == None and len(self.targetList) > 0:
                    targetArea, targetRoom = Room.getAreaAndRoom(galaxyList, self.targetList[0])
                    roomDistance, targetDirection, message = Room.getTargetRange(galaxyList, currentRoom, self.targetList[0], self.maxLookDistance)
                elif directionCount != None:
                    targetDirection = Room.getTargetDirection(directionKey)
                    targetArea, targetRoom = Room.getAreaAndRoom(galaxyList, targetRoom)
                    targetArea, targetRoom, roomDistance, message = Room.getTargetRoomFromStartRoom(galaxyList, targetArea, targetRoom, targetDirection, directionCount, True)
                
                if message == "No Exit":
                    if self.num == None:
                        console.write("There is nothing there.", "22w1y", True)
                elif message == "Door Is Closed":
                    if self.num == None:
                        console.write("The door is closed.", "18w1y", True)
                
                else:
                    drawBlankLine = False
                    if autoAttackCheck == False:
                        drawBlankLine = self.stopActions(console, galaxyList, player)
                    
                    flags = self.combatSkillFunction(config, player, combatSkill, currentRoom, targetRoom, roomDistance, mobKey, mobCount, directionKey, True, {})
                    targetMob = flags["targetMob"]
                    selfSkill = flags["selfSkill"]
                    targetMobList = flags["targetMobList"]
                    attackList = flags["attackList"]
                    allOnlyCheck = flags["allOnlyCheck"]

                    if len(targetMobList) > 0 and "From Another Room" in combatSkill.ruleDict and roomDistance == 0:
                        if self.num == None:
                            console.write("You're too close!", "3w1y12w1y", True)
                    elif len(targetMobList) == 0 and mobKey not in ["All", None, "Self"]:
                        console.write("You don't see them.", "7w1y10w1y", drawBlankLine)
                    elif len(targetMobList) == 0 and mobKey == "All" and allOnlyCheck == False:
                        if directionKey != None:
                            console.write("You don't see anyone there.", "7w1y18w1y", drawBlankLine)
                        else:
                            console.write("You don't see anyone.", "7w1y12w1y", drawBlankLine)
                    else:
                        actionFlags = {"combatSkill":combatSkill, "targetRoom":targetRoom, "roomDistance":roomDistance, "mobKey":mobKey, "mobCount":mobCount, "directionKey":directionKey, "targetDirection":targetDirection, "attackList":attackList}
                        if self.inStunnedTargetRoom(galaxyList) == True and combatSkill.maxTargets == 1 and targetMob in self.stunList and combatSkill.healCheck == False:
                            messageDataList = self.combatSkillCompleteAction(config, console, galaxyList, player, actionFlags, [])
                            for messageData in messageDataList:
                                console.write(messageData["String"], messageData["Code"], messageData["Draw Blank Line"])
                        else:
                            if self.num == None:
                                if messageDataList != None:
                                    stringHalf1 = "You prepare to " + combatSkill.name["String"] + ".."
                                    stringHalf2 = ""
                                    codeHalf1 = "15w" + combatSkill.name["Code"] + "2y"
                                    codeHalf2 = ""
                                    stackDisplayMessage(messageDataList, "Combat Check", stringHalf1, stringHalf2, codeHalf1, codeHalf2, False)
                                else:
                                    console.write("You prepare to " + combatSkill.name["String"] + "..", "15w" + combatSkill.name["Code"] + "2y", drawBlankLine)
                                    
                            elif currentRoom.sameRoomCheck(player) == True:
                                if messageDataList != None:
                                    stringHalf1 = self.prefix + " " + self.name["String"] + " "
                                    stringHalf2 = "prepares to attack.."
                                    codeHalf1 = str(len(self.prefix)) + "w1w" + self.name["Code"] + "1w"
                                    codeHalf2 = "18w2y"
                                    stackDisplayMessage(messageDataList, "Combat Check", stringHalf1, stringHalf2, codeHalf1, codeHalf2, False)
                                else:
                                    console.write(self.prefix + " " + self.name["String"] + " prepares to attack..", str(len(self.prefix)) + "w1w" + self.name["Code"] + "1w18w2y", drawBlankLine)
                                    
                            self.actionList.append(Action("Combat Skill", actionFlags, combatSkill.tickCount))

        return messageDataList

    def combatSkillCompleteAction(self, config, console, galaxyList, player, flags, messageDataList):
        if flags["combatSkill"].name["String"] in ["Dodge", "Block"]:
            pass

        else:
            combatSkill = flags["combatSkill"]
            oldTargetRoom = flags["targetRoom"]
            roomDistance = flags["roomDistance"]
            mobKey = flags["mobKey"]
            mobCount = flags["mobCount"]
            directionKey = flags["directionKey"]
            targetDirection = flags["targetDirection"]
            currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
            if currentRoom == None:
                currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]

            combatSkillRange = combatSkill.maxRange
            if len(combatSkill.weaponTypeList) > 0 and combatSkill.weaponTypeList[0] in [["Bow"], ["Pistol"], ["Rifle"]]:
                combatSkillRange = self.maxLookDistance

            if combatSkillRange == 0:
                targetRoom = currentRoom
            elif len(self.targetList) > 0 and mobKey == None:
                targetRoom = Room.exists(galaxyList, self.targetList[0].spaceship, self.targetList[0].galaxy, self.targetList[0].system, self.targetList[0].planet, self.targetList[0].area, self.targetList[0].room)
                if targetRoom == None:
                    targetRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
            else:
                targetRoom = oldTargetRoom

            if oldTargetRoom != targetRoom:
                distance, targetDirection, unused = Room.getTargetRange(galaxyList, targetRoom, currentRoom, combatSkillRange)
                if distance != -1:
                    roomDistance = distance
                    if targetDirection != None:
                        targetDirection = Room.getOppositeDirection(targetDirection)
            
            flags = self.combatSkillFunction(config, player, combatSkill, currentRoom, targetRoom, roomDistance, mobKey, mobCount, directionKey, False, flags)

            if self.num != None:
                self.actionList.append(Action("Buffer Action", {}, 2))

            selfSkill = flags["selfSkill"]
            attackDisplayList = flags["attackDisplayList"]
            targetMob = flags["targetMob"]
            targetMobList = flags["targetMobList"]
            shootGunDataList = flags["shootGunDataList"]

            targetUserLine = getTargetUserString(self)
            targetUserString = targetUserLine["String"]
            targetUserCode = targetUserLine["Code"]
            targetUserNonPossLine = getTargetUserString(self, False)
            targetUserNonPossString = targetUserNonPossLine["String"]
            targetUserNonPossCode = targetUserNonPossLine["Code"]

            directionString = ""
            directionCode = ""
            directionCountString = ""
            directionCountCode = ""
            toTheString = ""
            if roomDistance > 0:
                toTheString = " to the "
                targetDirectionString = targetDirection
                if self.num != None and targetRoom.sameRoomCheck(player) == True:
                    targetDirectionString = Room.getOppositeDirection(targetDirection)
                    toTheString = " from the "
                directionString = toTheString + targetDirectionString
                directionCode = str(len(toTheString)) + "w" + str(len(targetDirectionString)) + "w"
                directionCountString, directionCountCode = getCountString(roomDistance)

            messageType = "Attack Complete"
            drawBlankLine = True
            if (targetMob == None and "All Only" in combatSkill.ruleDict and selfSkill == None) or \
            (len(targetMobList) == 0):
                if not (self.num != None and targetRoom.sameRoomCheck(player) == False):
                    stringHalf1 = targetUserString
                    stringHalf2 = combatSkill.name["String"] + directionString + " doesn't hit anyone."
                    codeHalf1 = targetUserCode
                    codeHalf2 = combatSkill.name["Code"] + directionCode + "6w1y12w1y"
                    drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                    combineLinesCheck = self.num != None
                    stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                    drawBlankLine = False

            elif selfSkill != None and targetRoom.sameRoomCheck(self):
                targetUserStringHeal = "You "
                targetUserCodeHeal = "4w"
                healString = "heal yourself with "
                if self.num != None:
                    targetUserStringHeal = self.prefix + " " + self.name["String"] + " "
                    targetUserCodeHeal = str(len(self.prefix)) + "w1w" + self.name["Code"] + "1w"
                    healString = "heals themself with "
                if not (self.num != None and targetRoom.sameRoomCheck(player) == False):
                    damageString = ""
                    damageCode = ""
                    if len(attackDisplayList) > 0 and "Player Data" in attackDisplayList[0] and "Attack Damage" in attackDisplayList[0]:
                        damageLine = getDamageString(attackDisplayList[0]["Attack Damage"], "dg")
                        damageString = damageLine["String"]
                        damageCode = damageLine["Code"]
                    stringHalf1 = targetUserStringHeal
                    stringHalf2 = healString + combatSkill.name["String"] + ". " + damageString
                    codeHalf1 = targetUserCodeHeal
                    codeHalf2 = str(len(healString)) + "w" + combatSkill.name["Code"] + "2y" + damageCode
                    drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                    combineLinesCheck = self.num != None
                    stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                    drawBlankLine = False

            if len(targetMobList) > 0:
                for attackData in attackDisplayList:
                    secondaryAttackString = ""
                    secondaryAttackCode = ""
                    if "Second Attack" in attackData:
                        secondaryAttackString = "follow up "
                        secondaryAttackCode = "10w"

                    if "Miss Check" in attackData:
                        if attackData["Miss Check"] == "Out Of Ammo":
                            gunString = attackData["Weapon Data List"][0].name["String"]
                            gunCode = attackData["Weapon Data List"][0].name["Code"]
                            if not (self.num != None and currentRoom.sameRoomCheck(player) == False):
                                stringHalf1 = targetUserString
                                stringHalf2 = gunString + " *CLICKS* due to having no ammo."
                                codeHalf1 = targetUserCode
                                codeHalf2 = gunCode + "2y6w1y22w1y"
                                drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                                stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, False)
                                drawBlankLine = False
                        
                        elif attackData["Miss Check"] == "Miss Attack" and not (attackData["Mob Data"] == "Multiple" and attackData["Count"] > 0):
                            countString = ""
                            countCode = ""
                            mobString = "the group"
                            mobCode = "9w"
                            if attackData["Mob Data"] != "Multiple":
                                countString, countCode = getCountString(attackData["Miss Count"])
                                mobString = attackData["Mob Data"].prefix + " " + attackData["Mob Data"].name["String"]
                                mobCode = str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"]
                                if attackData["Mob Data"].num == None and len(targetMobList) == 1:
                                    mobString = "you"
                                    mobCode = "3w"
                            if not (self.num != None and targetRoom.sameRoomCheck(player) == False):
                                if "Dodge Check" in attackData:
                                    stumbleString = "."
                                    stumbleCode = "1y"
                                    if attackData["Mob Data"].num == None:
                                        if "Stumble Check" in attackData:
                                            stumbleString = ", throwing them off balance."
                                            stumbleCode = "2y25w1y"
                                        stringHalf1 = "You "
                                        stringHalf2 = "dodge " + self.prefix.lower() + " " + self.name["String"] + "'s " + attackData["Attack Data"].name["String"] + stumbleString
                                        codeHalf1 = "4w"
                                        codeHalf2 = "6w" + str(len(self.prefix)) + "w1w" + self.name["Code"] + "1y2w" + attackData["Attack Data"].name["Code"] + stumbleCode
                                    else:
                                        if "Stumble Check" in attackData:
                                            stumbleString = ", throwing " + targetUserNonPossString + "off balance."
                                            stumbleCode = "2y9w" + targetUserNonPossCode + "11w1y"
                                        stringHalf1 = attackData["Mob Data"].prefix + " " + attackData["Mob Data"].name["String"]
                                        stringHalf2 = "dodges " + targetUserString + " " + attackData["Attack Data"].name["String"] + stumbleString
                                        codeHalf1 = str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"]
                                        codeHalf2 = "7w" + targetUserCode + "1w" + attackData["Attack Data"].name["Code"] + stumbleCode
                                else:
                                    stringHalf1 = targetUserString
                                    stringHalf2 = secondaryAttackString + attackData["Attack Data"].name["String"] + directionString + directionCountString + " misses " + mobString + "." + countString
                                    codeHalf1 = targetUserCode
                                    codeHalf2 = secondaryAttackCode + attackData["Attack Data"].name["Code"] + directionCode + directionCountCode + "8w" + mobCode + "1y" + countCode
                                drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                                combineLinesCheck = self.num != None
                                stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                                drawBlankLine = False

                    if attackData["Count"] > 0:
                        hitString = " hits"
                        hitCode = "5w"
                        damageColor = "dr"
                        if attackData["Attack Data"].healCheck == True:
                            hitString = " heals"
                            hitCode = "6w"
                            damageColor = "dg"

                        if attackData["Mob Data"] == "Multiple":
                            if not (self.num != None and targetRoom.sameRoomCheck(player) == False):
                                stringHalf1 = targetUserString
                                stringHalf2 = secondaryAttackString + attackData["Attack Data"].name["String"] + directionString + directionCountString + hitString + " the group! " + getDamageString(attackData["Attack Damage"], damageColor)["String"]
                                codeHalf1 = targetUserCode
                                codeHalf2 = secondaryAttackCode + attackData["Attack Data"].name["Code"] + directionCode + directionCountCode + hitCode + "10w2y" + getDamageString(attackData["Attack Damage"], damageColor)["Code"]
                                drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                                combineLinesCheck = self.num != None
                                stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                        
                        elif attackData["Mob Data"] != None:
                            countString, countCode = getCountString(attackData["Count"])
                            targetEnemyString = attackData["Mob Data"].prefix.lower() + " " + attackData["Mob Data"].name["String"]
                            targetEnemyCode = str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"]
                            if attackData["Mob Data"].num == None:
                                targetEnemyString = "you"
                                targetEnemyCode = "3w"
                            if not (self.num != None and targetRoom.sameRoomCheck(player) == False):
                                if "Target Block Check" in attackData and attackData["Target Block Check"] == True:
                                    blockString = " Block "
                                    if attackData["Mob Data"].num != None:
                                        blockString = " Blocks "
                                    stunString = "."
                                    stunCode = "1y"
                                    if "Stun Check" in attackData:
                                        stunTargetString = "them"
                                        if attackData["Mob Data"].num != None:
                                            stunTargetString = "you"
                                        stunString = ", temporarily stunning " + stunTargetString + "."
                                        stunCode = "2y21w" + str(len(stunTargetString)) + "w1y"
                                    stringHalf1 = targetEnemyString[0].upper() + targetEnemyString[1::]
                                    stringHalf2 = blockString + targetUserString + attackData["Attack Data"].name["String"] + stunString
                                    codeHalf1 = targetEnemyCode
                                    codeHalf2 = str(len(blockString)) + "w" + targetUserCode + attackData["Attack Data"].name["Code"] + stunCode
                                
                                else:
                                    stunString = "!"
                                    stunCode = "1y"
                                    if "Stun Check" in attackData and attackData["Stun Check"] == True:
                                        stunString = ", sending them reeling!"
                                        stunCode = "2y20w1y"
                                        if attackData["Mob Data"].num == None:
                                            stunString = ", sending you reeling!"
                                            stunCode = "2y19w1y"

                                    if "Knock Down Check" in attackData and attackData["Knock Down Check"] == True:
                                        stunString = ", knocking them to the ground!"
                                        stunCode = "2y27w1y"
                                        if attackData["Mob Data"].num == None:
                                            stunString = ", knocking you to the ground!"
                                            stunCode = "2y26w1y"

                                    attackDamageLine = {"String":"", "Code":""}
                                    if "Attack Damage" in attackData:
                                        attackDamageLine = getDamageString(attackData["Attack Damage"], damageColor)
                                    stringHalf1 = targetUserString
                                    stringHalf2 = secondaryAttackString + attackData["Attack Data"].name["String"] + directionString + directionCountString + hitString + " " + targetEnemyString + stunString + countString + " " + attackDamageLine["String"]
                                    codeHalf1 = targetUserCode
                                    codeHalf2 = secondaryAttackCode + attackData["Attack Data"].name["Code"] + directionCode + directionCountCode + hitCode + "1w" + targetEnemyCode + stunCode + countCode + "1w" + attackDamageLine["Code"]
                                
                                    if "Sweep Check" in attackData and attackData["Sweep Check"] == True:
                                        if attackData["Mob Data"].num == None:
                                            stringHalf1 = targetUserString
                                            stringHalf2 = "sweep knocks you to the ground!"
                                            codeHalf1 = targetUserCode
                                            codeHalf2 = "30w1y"
                                        else:
                                            stringHalf1 = targetUserString
                                            stringHalf2 = "sweep knocks " + attackData["Mob Data"].prefix + " " + attackData["Mob Data"].name["String"] + " to the ground!"
                                            codeHalf1 = targetUserCode
                                            codeHalf2 = "13w" + str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"] + "14w1y"

                                drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                                combineLinesCheck = self.num != None
                                stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                
                        if "Cut Limb" in attackData:
                            if attackData["Cut Limb"] == "Head":
                                stringHalf1 = targetUserString
                                stringHalf2 = attackData["Attack Data"].name["String"] + " completely DECAPITATES " + attackData["Mob Data"].prefix.lower() + " " + attackData["Mob Data"].name["String"] + "!"
                                codeHalf1 = targetUserCode
                                codeHalf2 = attackData["Attack Data"].name["Code"] + "24w" + str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"] + "1y"
                                drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                                combineLinesCheck = self.num != None
                                stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)
                
                            else:
                                targetLimb = attackData["Cut Limb"]
                                if "Cut Limb Weapon" in attackData:
                                    stringHalf1 = attackData["Mob Data"].prefix + " " + attackData["Mob Data"].name["String"] + "'s " + attackData["Cut Limb Weapon"].name["String"] + " falls to the ground as " + targetUserString.lower()
                                    stringHalf2 = attackData["Attack Data"].name["String"] + " cuts off their " + targetLimb.lower() + "!"
                                    codeHalf1 = str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"] + "1y2w" + attackData["Cut Limb Weapon"].name["Code"] + "24w" + targetUserCode
                                    codeHalf2 = attackData["Attack Data"].name["Code"] + "16w" + str(len(targetLimb)) + "w1y"
                                else:
                                    stringHalf1 = targetUserString
                                    stringHalf2 = attackData["Attack Data"].name["String"] + " cuts off " + attackData["Mob Data"].prefix.lower() + " " + attackData["Mob Data"].name["String"] + "'s " + targetLimb.lower() + "!"
                                    codeHalf1 = targetUserCode
                                    codeHalf2 = attackData["Attack Data"].name["Code"] + "10w" + str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"] + "1y2w" + str(len(targetLimb)) + "w1y"
                                drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                                combineLinesCheck = self.num != None
                                stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)

                if attackDisplayList[0]["Kill Count"] > 0:
                    countString, countCode = getCountString(attackData["Kill Count"])
                    if attackData["Killed Mob Data"] == "Multiple":
                        yourString = "your"
                        if self.num != None:
                            yourString = "their"
                        if not (self.num != None and targetRoom.sameRoomCheck(player) == False):
                            stringHalf1 = targetUserString
                            stringHalf2 = "attack kills " + yourString + " targets!" + countString
                            codeHalf1 = targetUserCode
                            codeHalf2 = "13w" + str(len(yourString)) + "w8w1y" + countCode
                            drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                            stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck)

                    else:
                        if attackDisplayList[0]["Killed Mob Data"].num == None:
                            stringHalf1 = "You are DEAD!"
                            stringHalf2 = ""
                            codeHalf1 = "12w1y"
                            codeHalf2 = ""
                            drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                            stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck)
                        elif not (attackDisplayList[0]["Killed Mob Data"].num != None and self.num != None and currentRoom.sameRoomCheck(player) == False):
                            stringHalf1 = attackDisplayList[0]["Killed Mob Data"].prefix + " " + attackDisplayList[0]["Killed Mob Data"].name["String"] + " is DEAD!"
                            stringHalf2 = ""
                            codeHalf1 = str(len(attackDisplayList[0]["Killed Mob Data"].prefix)) + "w1w" + attackDisplayList[0]["Killed Mob Data"].name["Code"] + "8w1y"
                            codeHalf2 = ""
                            drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                            stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck)

                for attackData in attackDisplayList:
                    if "Return Weapon To Inventory" in attackData:
                        stringHalf1 = attackData["Mob Data"].prefix + " " + attackData["Mob Data"].name["String"] + " drops " + attackData["Return Weapon To Inventory"].prefix.lower() + " " + attackData["Return Weapon To Inventory"].name["String"] + " on the ground."
                        stringHalf2 = ""
                        codeHalf1 = str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"] + "7w" + str(len(attackData["Return Weapon To Inventory"].prefix.lower())) + "w1w" + attackData["Return Weapon To Inventory"].name["Code"] + "14w1y"
                        codeHalf2 = ""
                        drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != messageType))
                        combineLinesCheck = self.num != None
                        stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLineCheck, combineLinesCheck)

            # Auto-Loot Check #
            if len(attackDisplayList[0]["Mob Corpse List"]) > 0 and self.num == None and config.autoLoot == True and targetRoom.sameRoomCheck(player):
                for mobCorpse in attackDisplayList[0]["Mob Corpse List"]:
                    if len(mobCorpse.containerList) > 0:
                        messageDataList = self.getCheck(console, galaxyList, player, currentRoom, "All", None, "All", mobCorpse, messageDataList)

            # Auto-Reload Check #
            autoReloadCheck = False
            if len(shootGunDataList) > 0:
                if (self.num == None and config.autoReload == True) or self.num != None:
                    messageDataList, autoReloadCheck = self.autoReload(config, console, galaxyList, player, currentRoom, shootGunDataList, messageDataList)
                    if self.num == None and autoReloadCheck == False and (shootGunDataList[0]["Weapon Data"].isEmpty(True) or (len(shootGunDataList) > 1 and shootGunDataList[1]["Weapon Data"].isEmpty(True))):
                        drawBlankLineCheck = drawBlankLine and (len(messageDataList) == 0 or (len(messageDataList) > 0 and messageDataList[-1]["Message Type"] != "Reload Check"))
                        stackDisplayMessage(messageDataList, "Reload Check", "You're out of ammo!", "", "3w1y14w1y", "", False)

            # Auto-Combat Check #
            if autoReloadCheck == False and config.autoCombat == True and self.num == None:
                messageDataList = self.attackCheck(config, console, galaxyList, player, currentRoom, None, messageDataList, True)
                
        return messageDataList

    def combatSkillFunction(self, config, player, combatSkill, currentRoom, targetRoom, roomDistance, mobKey, mobCount, directionKey, copyCheck, flags):
        attackDisplayList = []                

        # Get Attack List Data #
        attackList = []
        mainAttackHand = self.gearDict[self.dominantHand]
        offAttackHand = self.gearDict[self.getOppositeHand(self.dominantHand)]
        combatSkill = copy.deepcopy(combatSkill)

        if len(combatSkill.weaponTypeList) == 2 or combatSkill.offHandAttacks == False:
            if combatSkill.weaponAttackCheck(mainAttackHand, offAttackHand) == True:
                enableSecondAttackCheck = combatSkill.attackModCheck(self)
                attackList.append(combatSkill)
                if enableSecondAttackCheck == True and len(combatSkill.weaponDataList) == 1 and (combatSkill.weaponDataList[0] == offAttackHand or (combatSkill.weaponDataList[0] == "Open Hand" and offAttackHand == None)):
                    offAttackHand = self.gearDict[self.dominantHand]

        if len(combatSkill.weaponTypeList) in [0, 1] or combatSkill.offHandAttacks == True:
            if len(attackList) == 0 and combatSkill.weaponAttackCheck(mainAttackHand, offAttackHand) == True:
                combatSkill.attackModCheck(self)
                attackList.append(combatSkill)
                if len(combatSkill.weaponDataList) == 1 and (combatSkill.weaponDataList[0] == offAttackHand or (combatSkill.weaponDataList[0] == "Open Hand" and offAttackHand == None)):
                    offAttackHand = self.gearDict[self.dominantHand]
            if combatSkill.healCheck == False and len(self.cutLimbList) == 0 and combatSkill.offHandAttacks == True and \
            not (len(combatSkill.weaponDataList) == 1 and combatSkill.weaponDataList[0] != "Melee" and combatSkill.weaponDataList[0].twoHanded == True and ("Disable Dual Wielding" in combatSkill.weaponDataList[0].flags or self.debugDualWield == False)):
                offHandFlagList = {"Distance":roomDistance, '"All" Attacks Disabled':True, "Disable Off Hand Attacks":True, "Disable Healing":True}
                if self.num == None:
                    offHandFlagList["Disable Weaponless Skills"] = True
                else:
                    offHandFlagList["Disable No Off-Hand Attack Attacks"] = True
                offAttackSkill, offAttackMessage = self.getRandomAttackSkill(offAttackHand, "Unused", offHandFlagList)
                offAttackSkill = copy.deepcopy(offAttackSkill)
                if offAttackSkill != None and offAttackSkill.weaponAttackCheck(offAttackHand) == True:
                    offAttackSkill.attackModCheck(self)
                    attackList.append(offAttackSkill)

        for skill in attackList:
            displayData = {"Mob Data":None, "Killed Mob Data":None, "Count":0, "Kill Count":0, "Mob Corpse List":[], "Miss Count":0, "Attack Data":skill}
            attackDisplayList.append(displayData)
            if mobKey == None and directionKey == None:
                skill.onTarget = True
            
        allOnlyCheck = False
        for attackSkill in attackList:
            if "All Only" in attackSkill.ruleDict:
                allOnlyCheck = True
        
        if mobCount in ["All", "Group", None] or allOnlyCheck == True:
            maxTargets = len(targetRoom.mobList)
            if targetRoom.sameRoomCheck(player) == True:
                maxTargets += 1
        else : maxTargets = mobCount
        if combatSkill.maxTargets != "All" and maxTargets > combatSkill.maxTargets:
            maxTargets = combatSkill.maxTargets
        
        selfSkill = None
        if combatSkill.healCheck == True and \
        (allOnlyCheck == True \
        or \
        ((mobKey == "Self" or \
        (mobKey == None and mobCount == None and (len(self.targetList) == 0 or config.healEnemies == False)) or \
        (mobKey == "All" and directionKey == None)))):
            selfSkill = True

        targetMobList = []
        targetMob = None
        mobKillList = []
        shootGunDataList = []
        if not (combatSkill.healCheck == True and mobKey == None and mobCount == None and len(self.targetList) > 0 and config.healEnemies == False and allOnlyCheck == False):
            if maxTargets > 0:
                if (targetRoom.sameRoomCheck(player) == True) and not (mobKey == None and len(self.targetList) > 0 and allOnlyCheck == False):
                    targetList = [player] + targetRoom.mobList
                else:
                    targetList = targetRoom.mobList
                for mob in targetList:
                    if not (combatSkill.healCheck == False and mob == self):
                        if mobKey == "All" or allOnlyCheck == True or \
                        (mobKey != None and mobKey in mob.keyList) or \
                        (mobKey == None and mob in self.targetList) or \
                        (mobKey in [None, "Self"] and combatSkill.healCheck == True) or \
                        (self.num != None and mobKey == "Player" and mob.num == None):
                            if allOnlyCheck == True or \
                            (not (config.healEnemies == False and combatSkill.healCheck == True and mob not in self.recruitList) and \
                            not (config.teamDamage == False and combatSkill.healCheck == False and mob in self.recruitList)):
                                if allOnlyCheck == True or not (mobCount == "Group" and mob not in self.recruitList):
                                    for i, attackSkill in enumerate(attackList):
                                        hitCheck = False
                                        
                                        if len(attackSkill.weaponDataList) in [0, 2]:
                                            if copyCheck == True:
                                                attackHitCheck, attackDisplayList[i] = Combat.hitCheck(attackDisplayList[i], copy.deepcopy(self), attackSkill, copy.deepcopy(mob), copy.deepcopy(targetRoom), i)
                                            else:
                                                attackHitCheck, attackDisplayList[i] = Combat.hitCheck(attackDisplayList[i], self, attackSkill, mob, targetRoom, i)
                                            if attackHitCheck == True:
                                                hitCheck = True
                                            
                                            # Shoot Gun/Auto-Reload Check Not Implemented Here Yet #

                                        else:
                                            for w, weapon in enumerate(attackSkill.weaponDataList):
                                                if weapon != "Melee" and weapon.isGun() and weapon.isLoaded(1) == False:
                                                    # Is This Needed Above, For Two Weapon Attacks? (Probably) #
                                                    attackDisplayList[i]["Miss Check"] = "Out Of Ammo"
                                                    attackDisplayList[i]["Weapon Data List"] = [attackSkill.weaponDataList[0]]
                                                else:
                                                    if w == 0:
                                                        if copyCheck == True:
                                                            attackHitCheck, attackDisplayList[i] = Combat.hitCheck(attackDisplayList[i], copy.deepcopy(self), attackSkill, copy.deepcopy(mob), copy.deepcopy(targetRoom), i)
                                                        else:
                                                            attackHitCheck, attackDisplayList[i] = Combat.hitCheck(attackDisplayList[i], self, attackSkill, mob, targetRoom, i)
                                                        if attackHitCheck == True:
                                                            hitCheck = True

                                                    if copyCheck == False and weapon != "Melee":
                                                        if weapon.isGun() and weapon.isLoaded(1) == True:
                                                            shootGunDataList.append({"Weapon Data":weapon, "Last Used Ammo Name":weapon.getLoadedAmmo().name["String"].lower()})
                                                            weapon.shoot()
                                                        elif weapon.weaponType == "Bow":
                                                            weapon.shoot(self)
                                        
                                        if self.num == None and mob.num == None:
                                            attackDisplayList[i]["Player Data"] = mob
                                        else:
                                            if attackDisplayList[i]["Mob Data"] == None:
                                                attackDisplayList[i]["Mob Data"] = mob
                                            elif attackDisplayList[i]["Mob Data"] != "Multiple" and attackDisplayList[i]["Mob Data"].num != mob.num:
                                                attackDisplayList[i]["Mob Data"] = "Multiple"
                                            if hitCheck == True:
                                                attackDisplayList[i]["Count"] += 1
                                            else:
                                                attackDisplayList[i]["Miss Count"] += 1
                                            if i == 1:
                                                attackDisplayList[i]["Second Attack"] = True

                                        if copyCheck == False:

                                            # Cut Enemy Head Check #
                                            if "Head" in mob.cutLimbList:
                                                mob.currentHealth = 0
                                            if mob.currentHealth <= 0 and len(attackList) > 1 and i == 0:
                                                del attackList[1]
                                                break

                                            # Enemy Dodge/Block #
                                            if mob.getCombatAction() != None and mob.getCombatAction().name["String"] in ["Dodge", "Block"]:

                                                # Enemy Dodge Check #
                                                if mob.getCombatAction().name["String"] == "Dodge":
                                                    if hitCheck == False:
                                                        attackDisplayList[i]["Dodge Check"] = True
                                                        if True: # Stumble Check On Successful Enemy Dodge
                                                            del mob.actionList[0]
                                                            if attackSkill.name["String"] != "Sweep": # Don't Stumble If Sweeping
                                                                self.actionList.append(Action("Stumble", {}, 3))
                                                                attackDisplayList[i]["Stumble Check"] = True
                                                        break

                                                # Enemy Block Check #
                                                elif mob.getCombatAction().name["String"] == "Block":
                                                    if "Target Block Check" in attackDisplayList[i]:
                                                        if attackDisplayList[i]["Target Block Check"] == True:
                                                            del mob.actionList[0]

                                                            # Stun-Block Check #
                                                            if attackSkill.stunUserOnBlock == True:
                                                                mob.stunList.append(self)
                                                                self.stunnedByList.append(mob)
                                                                self.actionList.append(Action("Stun", {}, 4))
                                                                attackDisplayList[i]["Stun Check"] = True
                                                            break
                                                        else:
                                                            del mob.actionList[0]
                                                            self.stunList.append(mob)
                                                            mob.stunnedByList.append(self)
                                                            mob.actionList.append(Action("Stun", {}, 4))
                                                            # Needs Message Data

                                            # Knock Down Enemy Check #
                                            elif "Knock Down Check" in attackDisplayList[i] and attackDisplayList[i]["Knock Down Check"] == True:
                                                if len(mob.actionList) > 0:
                                                    del mob.actionList[0]
                                                mob.actionList.append(Action("Knocked Down", {}, 8))

                                            # Interrupt Enemy Action & Stun #
                                            elif combatSkill.healCheck == False and len(mob.actionList) > 0 and hitCheck == True and mob.actionList[0].actionType not in ["Buffer Action", "Stun", "Stumble", "Knocked Down"]:
                                                if True: # Interrupt Enemy Action Check Goes Here
                                                    del mob.actionList[0]
                                                    attackDisplayList[i]["Interrupt Check"] = True
                                                    if True: # Stun Enemy Check Goes Here
                                                        mob.stunnedByList.append(self)
                                                        mob.actionList.append(Action("Stun", {}, 4))
                                                        attackDisplayList[i]["Stun Check"] = True

                                    targetMobList.append(mob)

                                    if copyCheck == True:
                                        if self.num == None:
                                            if combatSkill.healCheck == False and len(combatSkill.weaponTypeList) > 0:
                                                if mob not in self.combatList and targetRoom.sameRoomCheck(player) == True:
                                                    mob.actionList.append(Action("Buffer Action", {}, 2))
                                                    self.combatList.append(mob)
                                            if mob not in self.targetList:
                                                if mob != self:
                                                    if not (combatSkill.healCheck == True and mobKey in ["All", "Self", None]):
                                                        self.targetList.insert(0, mob)
                                    else:

                                        # Player/Mob Dead Check #
                                        if mob.currentHealth <= 0:
                                            testItem = createItem(1, "Armor", None)#
                                            mob.itemDict[testItem.pocket].append(testItem)#
                                            mobKillList.append(mob)
                                            if self.num != None and self in player.combatList:
                                                self.speechIndex = 0
                                                self.speechTick = -50
                                            attackDisplayList[0]["Kill Count"] += 1
                                            if attackDisplayList[0]["Killed Mob Data"] == None:
                                                attackDisplayList[0]["Killed Mob Data"] = mob
                                            elif attackDisplayList[0]["Killed Mob Data"] != "Multiple" and attackDisplayList[0]["Killed Mob Data"].num != mob.num:
                                                attackDisplayList[0]["Killed Mob Data"] = "Multiple"
                                            
                                        # Mob NOT Dead #
                                        else:
                                            if self.num == None:
                                                if mob not in self.targetList:
                                                    if mob != self:
                                                        if not (combatSkill.healCheck == True and mobKey in ["All", "Self", None]):
                                                            self.targetList.insert(0, mob)
                                                if combatSkill.healCheck == False:
                                                    if mob in self.recruitList:
                                                        del self.recruitList[self.recruitList.index(mob)]
                                                    if mob not in self.combatList and \
                                                    not ("Miss Check" in attackDisplayList[0] and attackDisplayList[0]["Miss Check"] == "Out Of Ammo" and (len(attackDisplayList) == 1 or ("Miss Check" in attackDisplayList[1] and attackDisplayList[1]["Miss Check"] == "Out Of Ammo")) and targetRoom.sameRoomCheck(player) == False):
                                                        mob.actionList.append(Action("Buffer Action", {}, 2))
                                                        self.combatList.append(mob)
                                            if mob in self.stunList:
                                                del self.stunList[self.stunList.index(mob)]

                                    if targetMob == None:
                                        targetMob = mob
                                    elif targetMob != "Multiple" and targetMob.num != mob.num:
                                        targetMob = "Multiple"
                                    if len(targetMobList) >= maxTargets or "Stun Check" in attackDisplayList[0]:
                                        break
            
        if copyCheck == False:
            for mob in mobKillList:
                if mob in self.targetList:
                    del self.targetList[self.targetList.index(mob)]
                if mob in self.recruitList:
                    del self.recruitList[self.recruitList.index(mob)]
                if mob in self.combatList:
                    del self.combatList[self.combatList.index(mob)]

                if len(mob.stunnedByList) > 0:
                    for stunnedByMob in mob.stunnedByList:
                        if mob in stunnedByMob.stunList:
                            del stunnedByMob.stunList[stunnedByMob.stunList.index(mob)]

                mobCorpse = Item.createCorpse(mob)
                targetRoom.itemList.append(mobCorpse)
                if mob in targetRoom.mobList:
                    del targetRoom.mobList[targetRoom.mobList.index(mob)]
                attackDisplayList[0]["Mob Corpse List"].append(mobCorpse)

                if mob.num == None:
                    mob.currentHealth = 3
                    mob.combatList = []
                    mob.targetList = []
                    mob.recruitList = []
                    for gearSlot in mob.gearDict:
                        if isinstance(gearSlot, list) == True:
                            for slot in mob.gearDict[gearSlot]:
                                mob.gearDict[gearSlot][slot] = None
                        else:
                            mob.gearDict[gearSlot] = None
                    for pocket in mob.itemDict:
                        mob.itemDict[pocket] = []
        
        returnFlags = {}
        returnFlags["targetMob"] = targetMob
        returnFlags["selfSkill"] = selfSkill
        returnFlags["targetMobList"] = targetMobList
        returnFlags["attackDisplayList"] = attackDisplayList
        returnFlags["currentRoom"] = currentRoom
        returnFlags["attackList"] = attackList
        returnFlags["shootGunDataList"] = shootGunDataList
        returnFlags["allOnlyCheck"] = allOnlyCheck

        return returnFlags

    def stumbleCompleteAction(self, console, galaxyList, player, flags):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        if currentRoom == None:
            currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]

        if self.num != None and currentRoom.sameRoomCheck(player) == True:
            console.write(self.prefix + " " + self.name["String"] + " regains balance.", str(len(self.prefix)) + "w1w" + self.name["Code"] + "16w1y", True)
        elif self.num == None:
            console.write("You regain balance.", "18w1y", True)

    def stunCompleteAction(self, console, galaxyList, player, flags):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        if currentRoom == None:
            currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]

        if len(self.stunnedByList) > 0:
            for mob in self.stunnedByList:
                if self in mob.stunList:
                    del mob.stunList[mob.stunList.index(self)]
            self.stunnedByList = []

        if self.num != None and currentRoom.sameRoomCheck(player) == True:
            console.write(self.prefix + " " + self.name["String"] + " regains their senses.", str(len(self.prefix)) + "w1w" + self.name["Code"] + "21w1y", True)
        elif self.num == None:
            console.write("You regain your senses.", "22w1y", True)
    
    def knockedDownCompleteAction(self, console, galaxyList, player, flags):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        if currentRoom == None:
            currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]

        if self.num != None and currentRoom.sameRoomCheck(player) == True:
            console.write(self.prefix + " " + self.name["String"] + " gets back up off the ground.", str(len(self.prefix)) + "w1w" + self.name["Code"] + "28w1y", True)
        elif self.num == None:
            console.write("You get up off the ground.", "25w1y", True)

    def displayInventory(self, console, galaxyList, player, currentRoom, targetPocketKey):
        targetPocket = None
        if targetPocketKey in ["gear", "gea", "ge", "g", "armor", "armo", "arm", "ar", "a"]:
            targetPocket = "Armor"
        elif targetPocketKey in ["weapons", "weapon", "weapo", "weap", "wea", "we", "w"]:
            targetPocket = "Weapon"
        elif targetPocketKey in ["ammo", "amm", "am"]:
            targetPocket = "Ammo"
        elif targetPocketKey in ["materium", "materiu", "materi", "mater", "mate", "mat", "ma", "m"]:
            targetPocket = "Materium"
        elif targetPocketKey in ["key", "ke", "k"]:
            targetPocket = "Key"
        elif targetPocketKey in ["organic", "organi", "organ", "orga", "org", "or", "o"]:
            targetPocket = "Organic"

        if targetPocket not in self.itemDict:
            console.write("Open which bag? (Gear, Weapon, Ammo, Materium, Food, Key)", "14w2y1r4w2y6w2y4w2y8w2y4w2y3w1r", True)

        else:
            displayList = []
            for item in self.itemDict[targetPocket]:
                if item.pocket == "Weapon" and item.isGun():
                    displayList.append({"ItemData":item})
                else:
                    displayData = None
                    for data in displayList:
                        if "Num" in data and "Pocket" in data and data["Num"] == item.num and data["Pocket"] == item.pocket:
                            if item.num != Item.getSpecialItemNum("Corpse") or item.name["String"] == data["ItemData"].name["String"]:
                                displayData = data
                                break
                    if displayData == None:
                        itemCount = 1
                        if hasattr(item, "quantity") == True and item.quantity != None:
                            itemCount = item.quantity
                        displayList.append({"Num":item.num, "Pocket":item.pocket, "Count":itemCount, "ItemData":item})
                    else:
                        displayData["Count"] += 1

            targetPocketDisplayString = targetPocket
            targetPocketDisplayCode = str(len(targetPocket)) + "w"
            if targetPocket == "Armor":
                targetPocketDisplayString = "Gear"
                targetPocketDisplayCode = "4w"
            elif targetPocket == "Misc":
                targetPocketDisplayString = "Misc."
                targetPocketDisplayCode = "4w1y"
            underlineString = ""
            underlineCode = ""
            for i in range(len(targetPocketDisplayString) + 4):
                underlineChar = "-"
                indentCount = int(len(targetPocketDisplayString + " Bag") * .25)
                if indentCount <= 0:
                    indentCount = 1
                if i not in range(0, indentCount) and i not in range(len(targetPocketDisplayString + " Bag") - indentCount, len(targetPocketDisplayString + " Bag")):
                    underlineChar = "="
                underlineString = underlineString + underlineChar
                if i % 2 == 1:
                    underlineCode = underlineCode + "1y"
                else:
                    underlineCode = underlineCode + "1dy"
            console.write(targetPocketDisplayString + " Bag", targetPocketDisplayCode + "4w", True)
            console.write(underlineString, underlineCode)

            if len(self.itemDict[targetPocket]) == 0:
                console.write("-Empty", "1y5w")
            elif currentRoom.isLit(galaxyList, player, self) == False and self.lightInBagCheck(targetPocket) == False:
                inventoryCount = 0
                for displayItemData in displayList:
                    if "Count" in displayItemData:
                        inventoryCount += displayItemData["Count"]
                    else:
                        inventoryCount += 1
                countString, countCode = getCountString(inventoryCount)
                console.write("-Something" + countString, "1y9w" + countCode)
            else:
                for displayItemData in displayList:
                    item = displayItemData["ItemData"]
                    modString = ""
                    modCode = ""
                    if "Glowing" in item.flags and item.flags["Glowing"] == True:
                        modString = " (Glowing)"
                        modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                    countNum = 0
                    if "Count" in displayItemData : countNum = displayItemData["Count"]
                    countString, countCode = getCountString(countNum)
                    itemDisplayString = item.prefix + " " + item.name["String"]
                    itemDisplayCode = str(len(item.prefix)) + "w1w" + item.name["Code"]
                    weaponStatusString = ""
                    weaponStatusCode = ""
                    if item.pocket == "Weapon":
                        weaponStatusString, weaponStatusCode = item.getWeaponStatusString()
                    console.write(itemDisplayString + weaponStatusString + countString + modString, itemDisplayCode + weaponStatusCode + countCode + modCode)

    def displaySkills(self, console, targetGroupKey):
        def displaySkillGroup(skillGroupLabel, skillList):
            blankString = ""
            for i in range(25 - len(skillGroupLabel["String"])):
                blankString += " "
            console.write(" *=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*", "2dr1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1dr", True)
            console.write(" | " + skillGroupLabel["String"] + ":" + blankString + "                          |", "3ddy" + skillGroupLabel["Code"] + "1y" + str(len(blankString)) + "w26w" + "1ddy")
            if len(skillList) > 0:
                console.write(" *=-=-=-=-=-=-=-=-=o=-=-=-=-=-=-=-=-=o=-=-=-=-=-=-=-=-=*", "2dr1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1dr")
            else:
                console.write(" *=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*", "2dr1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1dr")

            longestString = [0, 0, 0]
            for s, skill in enumerate(skillList):
                if len(skill.name["String"]) > longestString[s % 3]:
                    longestString[s % 3] = len(skill.name["String"])

            displayString = ""
            displayCode = ""
            for s, skill in enumerate(skillList):
                blank1String = ""
                blank2String = ""
                endString = ""
                endCode = ""
                if s % 3 == 2 or s == len(skillList) - 1:
                    endString = " | "
                    endCode = "3ddy"
                for i in range(longestString[s % 3] - len(skill.name["String"])):
                    blank1String += " "
                for i in range(12 - longestString[s % 3] + (2 - len(str(skill.learnPercent)))):
                    blank2String += " "
                displayString += " | " + blank1String + skill.name["String"] + blank2String + str(skill.learnPercent) + "%" + endString
                displayCode += "3ddy" + str(len(blank1String)) + "w" + skill.name["Code"] + str(len(blank2String)) + "w" + str(len(str(skill.learnPercent))) + "w1y" + endCode

                if s == len(skillList) - 1 and s % 3 != 2:
                    for i in range(2 - (s % 3)):
                        displayString += "                | "
                        displayCode += "16w2ddy"

                if s % 3 == 2 or s == len(skillList) - 1:
                    console.write(displayString, displayCode)
                    displayString = ""
                    displayCode = ""

            if len(skillList) == 0:
                console.write(" | -None                                               |", "3ddy1y1w3ddw47w1ddy")

            if len(skillList) > 0:
                console.write(" *=-=-=-=-=-=-=-=-=o=-=-=-=-=-=-=-=-=o=-=-=-=-=-=-=-=-=*", "2dr1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1dr")
            else:
                console.write(" *=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=*", "2dr1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y1dr")

        targetGroup = None
        if targetGroupKey != None:
            if targetGroupKey == "all" : targetGroup = None
            else:
                for skillGroup in self.combatSkillDict:
                    if targetGroupKey[0] == skillGroup[0].lower():
                        targetGroup = skillGroup
                        break

        for skillGroup in self.combatSkillDict:
            if targetGroup in [None, skillGroup]:
                lineBreak = False
                drawEndLine = False
                if skillGroup == "Basic":
                    drawEndLine = True
                elif skillGroup == "Sword":
                    lineBreak = True
                skillGroupString = skillGroup + " Skills"
                skillGroupCode = ""
                for n, name in enumerate(skillGroup.split()):
                    spaceCode = ""
                    if n != len(skillGroup.split()) - 1:
                        spaceCode = "1w"
                    skillGroupCode += "1w" + str(len(name) - 1) + "ddw" + spaceCode
                skillGroupCode += "2w5ddw"
                skillGroupLabel = {"String":skillGroupString, "Code":skillGroupCode}
                displaySkillGroup(skillGroupLabel, self.combatSkillDict[skillGroup])
            
        console.lineList.insert(0, {"Blank": True})

    def displayGear(self, console, galaxyList, player, currentRoom, descriptionCheck=False):
        gearSlotDisplayDict = {"Body Under":{"String":"(Under) Body", "Code":"1r1w4ddw2r4w"}, "Body Over":{"String":"(Over) Body", "Code":"1r1w3ddw2r4w"}, "Legs Under":{"String":"(Under) Legs", "Code":"1r1w4ddw2r4w"}, "Legs Over":{"String":"(Over) Legs", "Code":"1r1w3ddw2r4w"}, "Left Hand":{"String":"L-Hand", "Code":"1w1y4w"}, "Right Hand":{"String":"R-Hand", "Code":"1w1y4w"}}

        if descriptionCheck == False:
            console.write("Worn Gear", "1w4ddw1w3ddw", True)
            console.write("--=====--", "1y1dy1y1dy1y1dy1y1dy1y")

        for gearSlot in self.gearDict:
            gearSlotString = gearSlot
            if gearSlot in gearSlotDisplayDict and "String" in gearSlotDisplayDict[gearSlot]:
                gearSlotString = gearSlotDisplayDict[gearSlot]["String"]
            gearSlotCode = str(len(gearSlotString)) + "w"
            if gearSlot in gearSlotDisplayDict and "Code" in gearSlotDisplayDict[gearSlot]:
                gearSlotCode = gearSlotDisplayDict[gearSlot]["Code"]
            
            if gearSlotString in ["L-Hand", "R-Hand"]:
                if self.dominantHand[0] == gearSlotString[0] and descriptionCheck == False:
                    gearSlotString = "(D) " + gearSlotString
                    gearSlotCode = "1y1w2y" + gearSlotCode

            indent = 12 - len(gearSlotString)
            for i in range(indent):
                gearSlotString = " " + gearSlotString
                gearSlotCode = "1w" + gearSlotCode

            slotRange = 1
            if isinstance(self.gearDict[gearSlot], list):
                slotRange = len(self.gearDict[gearSlot])
            for slotIndex in range(slotRange):
                gearString = "(Nothing)"
                gearCode = "1r1w6ddw1r"
                if gearSlot in ["Left Hand", "Right Hand"]:
                    targetLimb = gearSlot.split()[0] + " Arm"
                    if targetLimb in self.cutLimbList:
                        gearString = "(Missing)"
                weaponStatusString = ""
                weaponStatusCode = ""
                modString = ""
                modCode = ""
                
                if isinstance(self.gearDict[gearSlot], list):
                    targetSlot = self.gearDict[gearSlot][slotIndex]
                else:
                    targetSlot = self.gearDict[gearSlot]
                if targetSlot == None:
                    if gearSlot == self.getOppositeHand(self.dominantHand) and self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].twoHanded == True:
                        gearString = "[Two-Handed]"
                        gearCode = "1r3ddw1y6ddw1r"
                else:
                    if "Glowing" in targetSlot.flags and targetSlot.flags["Glowing"] == True:
                        modString = " (Glowing)"
                        modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                    if currentRoom.isLit(galaxyList, player, self) == False:
                        gearString = "(Something)"
                        gearCode = "1r1w8wwd1r"
                    else:
                        gearString = targetSlot.name["String"]
                        gearCode = str(len(gearString)) + "w"
                        if "Code" in targetSlot.name:
                            gearCode = targetSlot.name["Code"]
                    if targetSlot.pocket == "Weapon":
                        weaponStatusString, weaponStatusCode = targetSlot.getWeaponStatusString()
                console.write(gearSlotString + ": " + gearString + weaponStatusString + modString, gearSlotCode + "2y" + gearCode + weaponStatusCode + modCode)

        defenseRatingData = self.getArmorRating()
        defenseRatingString = str(defenseRatingData["Piercing"]) + "/" + str(defenseRatingData["Cutting"]) + "/" + str(defenseRatingData["Blunt"])
        defenseRatingCode = str(len(str(defenseRatingData["Piercing"]))) + "w1r" + str(len(str(defenseRatingData["Cutting"]))) + "w1r" + str(len(str(defenseRatingData["Blunt"]) )) + "w"
        upperArmorString = "Armor Rating: " + defenseRatingString
        upperArmorCode = "12w2y" + defenseRatingCode
        console.write(upperArmorString, upperArmorCode, True)

    def displayStatus(self, console, config):
        console.write("Player Status", "1w9ddw1w5ddw", True)
        console.write("--=========--", "1y1dy1y1dy1y1dy1y1dy1y1ddy1y1ddy1y")

        autoLootString  = "[ ]"
        if config.autoLoot == True:
            autoLootString = "[X]"
        console.write(autoLootString + " - Auto Loot", "1y1dr1y3y9w")

        autoReloadString  = "[ ]"
        if config.autoReload == True:
            autoReloadString = "[X]"
        console.write(autoReloadString + " - Auto Reload", "1y1dr1y3y11w")
        
        autoCombatString  = "[ ]"
        if config.autoCombat == True:
            autoCombatString = "[X]"
        console.write(autoCombatString + " - Auto Combat", "1y1dr1y3y11w")
        
        teamDamageString  = "[ ]"
        if config.teamDamage == True:
            teamDamageString = "[X]"
        console.write(teamDamageString + " - Team Damage", "1y1dr1y3y11w")
        
        healEnemiesString  = "[ ]"
        if config.healEnemies == True:
            healEnemiesString = "[X]"
        console.write(healEnemiesString + " - Heal Enemies", "1y1dr1y3y12w")
        
    def displayTime(self, console, galaxyList):
        currentPlanet = galaxyList[self.galaxy].systemList[self.system].planetList[self.planet]
        hoursString = str(int(currentPlanet.currentMinutesInDay / 60))
        if currentPlanet.name["String"] in ["Earth", "Proto Earth"]:
            if hoursString == "0":
                hoursString = "12"
            elif int(hoursString) > 12:
                hoursString = str(int(hoursString) - 12)

        minutesString = str(int(currentPlanet.currentMinutesInDay % 60))
        if len(minutesString) == 1:
            minutesString = "0" + minutesString

        if currentPlanet.name["String"] in ["Earth", "Proto Earth"]:
            amPmString = " A.M"
            if currentPlanet.currentMinutesInDay >= currentPlanet.minutesInDay / 2:
                amPmString = " P.M"
            amPmCode = "2w1y1w"
            console.write("The time is " + str(hoursString) + ":" + str(minutesString) + amPmString + ".", "12w" + str(len(hoursString)) +"w1y" + str(len(minutesString)) + "w" + amPmCode + "1y", True)
        else:
            console.write("The time is " + str(hoursString) + ":" + str(minutesString) + ".", "12w" + str(len(hoursString)) +"w1y" + str(len(minutesString)) + "w1y", True)
       
    def searchCheck(self, console, galaxyList, player, currentRoom, searchKey):
        searchData = None
        for tempSearchData in currentRoom.searchList:
            if "Key List" in tempSearchData and searchKey in tempSearchData["Key List"]:
                searchData = tempSearchData
                break
        if searchData == None:
            console.write("You search but don't find anything..", "18w1y15w2y", True)

        else:
            targetDir = searchData["Target Direction"]
            if searchData["Type"] == "Hidden Door" and "Target Direction" in searchData and currentRoom.door[targetDir] != None:
                targetDoor = currentRoom.door[targetDir]
                if targetDoor["Status"] == "Open":
                    console.write("The hidden entrance is already open.", "35w1y", True)
                elif targetDoor["Status"] == "Locked" and self.hasKey(targetDoor["Password"]) == False:
                    console.write("You lack the key.", "16w1y")

                else:
                    currentRoom.openCloseDoor(galaxyList, "Open", searchData["Target Direction"])
                    console.write(searchData["Open Display String"], searchData["Open Display Code"], True)

    def pushCheck(self, console, galaxyList, player, currentRoom, pushKey):
        targetButton = currentRoom.getTargetObject(pushKey, ["Mobs", "Items", "Spaceships", "Buttons"])
        if targetButton == None:
            targetButton = self.getTargetItem(pushKey)[0]
        
        if targetButton == None:
            console.write("You don't see it.", "7w1y8w1y", True)
        elif isinstance(targetButton, Button) == False:
            console.write("That's not a button.", "4w1y14w1y", True)

        else:
            targetButton.push(console, player, self, currentRoom)

    def sayCheck(self, console, galaxyList, player, currentRoom, sayKey):
        sayString = "say"
        if sayKey["String"][-1] == '?':
            sayString = "ask"
        userString = "You " + sayString
        userCode = "7w"
        if self.num != None and currentRoom.sameRoomCheck(player) == True:
            userString = self.prefix + " " + self.name["String"] + " says"
            userCode = str(len(self.prefix)) + "w1w" + self.name["Code"] + "5w"
            if currentRoom.isLit(galaxyList, player, self) == False:
                userString = "Someone says"
                userCode = "12w"

        targetString = userString + ", '"
        targetCode = userCode + "3y"
        periodString = '.'
        keyString = sayKey["String"]
        if sayKey["String"][-1] == '.':
            keyString = ' '.join(sayKey["String"].split()[0:-1] + [sayKey["String"].split()[-1].replace('.', '')])
        elif sayKey["String"][-1] == '?':
            keyString = ' '.join(sayKey["String"].split()[0:-1] + [sayKey["String"].split()[-1].replace('?', '')])
            periodString = "?"
        elif sayKey["String"][-1] == '!':
            keyString = ' '.join(sayKey["String"].split()[0:-1] + [sayKey["String"].split()[-1].replace('!', '')])
            periodString = "!"
        displayString = targetString + keyString + periodString + "'"
        displayCode = targetCode + str(len(keyString)) + "w1y" + "1y"
        console.write(displayString, displayCode, True)

    def consumeCheck(self, console, galaxyList, player, currentRoom, consumeKey):
        pass

    def boardCheck(self, console, map, galaxyList, player, currentRoom, targetSpaceshipKey):
        drawBlankLine = self.stopActions(console, galaxyList, player)

        targetSpaceship = None
        for spaceship in currentRoom.spaceshipList:
            if targetSpaceshipKey in spaceship.keyList:
                targetSpaceship = spaceship
                break

        if self.spaceship != None:
            console.write("You are already inside.", "22w1y", drawBlankLine)
        elif targetSpaceship == None:
            console.write("You don't see anything like that.", "7w1y24w1y", drawBlankLine)
        elif targetSpaceship.password != None and self.hasKey(targetSpaceship.password) == False:
            console.write("You lack the proper key.", "23w1y", drawBlankLine)
        
        else:
            self.spaceship = targetSpaceship.num
            self.area = targetSpaceship.hatchLocation[0]
            self.room = targetSpaceship.hatchLocation[1]

            console.write("The hatch opens and closes as you step inside.", "45w1y", drawBlankLine)

            spaceshipHatchRoom = targetSpaceship.areaList[self.area].roomList[self.room]
            spaceshipHatchRoom.display(console, galaxyList, self)

            map.loadAreaMap(targetSpaceship.areaList[self.area])

    def launchCheck(self, console, galaxyList, player, currentRoom):
        if currentRoom.spaceshipObject == None or "Cockpit" not in currentRoom.flags:
            console.write("You must be in a cockpit to do that.", "35w1y", True)
        elif currentRoom.spaceshipObject.password != None and self.hasKey(currentRoom.spaceshipObject.password) == False:
            console.write("You lack the key.", "16w1y", True)
        elif currentRoom.spaceshipObject.launchLandAction == "Land":
            console.write("You can't do that while landing.", "7w1y23w1y", True)
        elif currentRoom.spaceshipObject.landedLocation == None:
            console.write("You must be landed to do that.", "29w1y", True)

        else:
            landedPlanet = galaxyList[currentRoom.spaceshipObject.galaxy].systemList[currentRoom.spaceshipObject.system].planetList[currentRoom.spaceshipObject.planet]
            landedArea = landedPlanet.areaList[currentRoom.spaceshipObject.landedLocation[0]]
            for room in landedArea.roomList:
                if currentRoom.spaceshipObject in room.spaceshipList:
                    del room.spaceshipList[room.spaceshipList.index(currentRoom.spaceshipObject)]
            
            currentRoom.spaceshipObject.launchLandAction = "Launch"
            currentRoom.spaceshipObject.landedLocation = None
            currentRoom.spaceshipObject.launchLandTick = 0
            currentRoom.spaceshipObject.launchLandPhase = 0

            console.write('''A computerized voice says, 'Commencing launch countdown.' ''', "25w3y27w2y", True)
    
    def radarCheck(self, console, galaxyList, player, currentRoom):
        if currentRoom.spaceshipObject == None or "Cockpit" not in currentRoom.flags:
            console.write("You must be in a cockpit to do that.", "35w1y", True)
        
        else:
            console.write("You look at the ship's radar screen.", "20w1y14w1y", True)
            xPositionLine = insertCommasInNumber(str(int(currentRoom.spaceshipObject.position[0])))
            yPositionLine = insertCommasInNumber(str(int(currentRoom.spaceshipObject.position[1])))
            positionString = "Position - X:" + xPositionLine["String"] + " Y:" + yPositionLine["String"]
            positionCode = "9w2y1r1y" + xPositionLine["Code"] + "w1w1r1y" + yPositionLine["Code"] + "w"
            console.write(positionString, positionCode)

            statusString = "[Orbiting]" 
            statusCode = "1y8w1y"
            if currentRoom.spaceshipObject.planet != None:
                orbitingPlanet = galaxyList[currentRoom.spaceshipObject.galaxy].systemList[currentRoom.spaceshipObject.system].planetList[currentRoom.spaceshipObject.planet]
                statusString = "[Orbiting " + orbitingPlanet.name["String"] + "]"
                statusCode = "1y9w" + orbitingPlanet.name["Code"] + "1y"
            if currentRoom.spaceshipObject.landedLocation != None:
                statusString = "[Landed]"
                statusCode = "1y6w1y"
            elif currentRoom.spaceshipObject.launchLandTick != -1 and currentRoom.spaceshipObject.launchLandAction in ["Launch", "Land"]:
                statusString = "[" + currentRoom.spaceshipObject.launchLandAction + "ing]"
                statusCode = "1y" + str(len(currentRoom.spaceshipObject.launchLandAction)) + "w3w1y"
            elif currentRoom.spaceshipObject.planet == None:
                statusString = "[In Flight]"
                statusCode = "1y9w1y"
            
            headingString = " Heading - " + statusString
            headingCode = "9w2y" + statusCode
            headingPlanetString = ""
            headingPlanetCode = ""
            if currentRoom.spaceshipObject.course != None:
                xCourseLine = insertCommasInNumber(str(int(currentRoom.spaceshipObject.course[0])))
                yCourseLine = insertCommasInNumber(str(int(currentRoom.spaceshipObject.course[1])))
                if currentRoom.spaceshipObject.targetPlanet != None and currentRoom.spaceshipObject.clearCourseCheck == False:
                    headingPlanetString = " [" + currentRoom.spaceshipObject.targetPlanet.name["String"] + "]"
                    headingPlanetCode = "2y" + currentRoom.spaceshipObject.targetPlanet.name["Code"] + "1y"
                headingString = " Heading - X:" + xCourseLine["String"] + " Y:" + yCourseLine["String"] + headingPlanetString
                headingCode = "9w2y1r1y" + xCourseLine["Code"] + "w1w1r1y" + yCourseLine["Code"] + headingPlanetCode
            console.write(headingString, headingCode)

            speedString = "   Speed - " + str(currentRoom.spaceshipObject.speedPercent) + "%" 
            speedCode = "9w2y" + str(len(str(currentRoom.spaceshipObject.speedPercent))) + "w1y" 
            console.write(speedString, speedCode)

            longestNameString = 0
            for planet in galaxyList[currentRoom.spaceshipObject.galaxy].systemList[currentRoom.spaceshipObject.system].planetList:
                if len(planet.name["String"]) > longestNameString:
                    longestNameString = len(planet.name["String"])
            console.write("Bodies Detected:", "1w6ddw1w7ddw1y", True)
            for planet in galaxyList[currentRoom.spaceshipObject.galaxy].systemList[currentRoom.spaceshipObject.system].planetList:
                bufferString = ""
                for i in range(longestNameString - len(planet.name["String"])):
                    bufferString += " "
                xPositionLine = insertCommasInNumber(str(int(planet.position[0])))
                yPositionLine = insertCommasInNumber(str(int(planet.position[1])))
                orbitString = " " + statusString
                orbitCode = "1w" + statusCode
                if currentRoom.spaceshipObject.landedLocation == None:
                    orbitString = " [Orbiting]"
                    orbitCode = "2y8w1y"
                    if currentRoom.spaceshipObject.launchLandAction != None:
                        orbitString = " [" + currentRoom.spaceshipObject.launchLandAction + "ing]"
                        orbitCode = "2y" + str(len(currentRoom.spaceshipObject.launchLandAction)) + "w3w1y"
                if currentRoom.spaceshipObject.planet != planet.planet:
                    orbitString = ""
                    orbitCode = ""
                displayString = bufferString + planet.name["String"] + " - X:" + xPositionLine["String"] + " Y:" + yPositionLine["String"] + orbitString
                displayCode = str(len(bufferString)) + "w" + planet.name["Code"] + "3y1r1y" + xPositionLine["Code"] + "2r1y" + yPositionLine["Code"] + orbitCode
                console.write(displayString, displayCode)

    def courseCheck(self, console, galaxyList, player, currentRoom, courseKey):
        if currentRoom.spaceshipObject == None or "Cockpit" not in currentRoom.flags:
            console.write("You must be in a cockpit to do that.", "35w1y", True)
        elif currentRoom.spaceshipObject.landedLocation != None:
            console.write("You can't do that while landed.", "7w1y22w1y", True)
        elif currentRoom.spaceshipObject.launchLandTick != -1:
            actionString = currentRoom.spaceshipObject.launchLandAction.lower() + "ing"
            console.write("You can't do that while " + actionString + ".", "7w1y16w" + str(len(actionString)) + "w1y", True)
        elif courseKey == "none" and (currentRoom.spaceshipObject.clearCourseCheck == True or currentRoom.spaceshipObject.course == None):
            console.write("Your heading is already clear.", "29w1y", True)
        elif courseKey == None:
            displayString = '''A computerized voice says, 'Set your course with "Course X Y/Destination".' '''
            displayCode = "25w3y21w1y10w1r11w3y"
            console.write(displayString, displayCode, True)
        
        else:
            if courseKey == "none" and currentRoom.spaceshipObject.speedMod > 0:
                currentRoom.spaceshipObject.clearCourseCheck = True
                currentRoom.spaceshipObject.speedMod = 0
                currentRoom.spaceshipObject.displaySlowDownMessage = 1
                currentRoom.spaceshipObject.displaySpeedUpMessage = False
                console.write("You clear the ships heading.", "27w1y", True)

            else:
                targetPlanet = None
                if isinstance(courseKey, str) == True:
                    for planet in galaxyList[self.galaxy].systemList[self.system].planetList:
                        if courseKey in planet.keyList:
                            targetPlanet = planet
                            break
                else:
                    rangeBound = 100
                    for planet in galaxyList[self.galaxy].systemList[self.system].planetList:
                        if courseKey[0] >= planet.position[0] - rangeBound and courseKey[0] < planet.position[0] + rangeBound:
                            if courseKey[1] >= planet.position[1] - rangeBound and courseKey[1] < planet.position[1] + rangeBound:
                                targetPlanet = planet
                                break

                if isinstance(courseKey, str) == True and targetPlanet == None:
                    console.write("You can't find it on the radar.", "7w1y22w1y", True)
                elif isinstance(courseKey, str) == True and targetPlanet.planet == self.planet:
                    console.write("You are already orbiting " + targetPlanet.name["String"] + ".", "25w" + targetPlanet.name["Code"] + "1y", True)

                else:
                    if targetPlanet != None:
                        currentRoom.spaceshipObject.course = targetPlanet.position
                        currentRoom.spaceshipObject.targetPlanet = targetPlanet
                        console.write("You punch in the coordinates for " + targetPlanet.name["String"] + ".", "33w" + targetPlanet.name["Code"] + "1y", True)
                    else:
                        currentRoom.spaceshipObject.course = courseKey
                        currentRoom.spaceshipObject.targetPlanet = None
                        console.write("You punch some coordinates into the ship's computer.", "40w1y10w1y", True)

                    if currentRoom.spaceshipObject.planet != None:
                        currentRoom.spaceshipObject.lastPlanet = galaxyList[currentRoom.spaceshipObject.galaxy].systemList[currentRoom.spaceshipObject.system].planetList[currentRoom.spaceshipObject.planet]
                    else:
                        currentRoom.spaceshipObject.lastPlanet = None
                    currentRoom.spaceshipObject.speedMod = 100
                    currentRoom.spaceshipObject.planet = None
                    if currentRoom.spaceshipObject.speedPercent == 0:
                        currentRoom.spaceshipObject.displaySpeedUpMessage = 1
                    currentRoom.spaceshipObject.displaySlowDownMessage = False
                    if currentRoom.spaceshipObject.num == player.spaceship:
                        player.planet = None
                    for area in currentRoom.spaceshipObject.areaList:
                        for room in area.roomList:
                            for mob in room.mobList:
                                mob.planet = None

    def throttleCheck(self, console, galaxyList, player, currentRoom, throttleKey):
        if currentRoom.spaceshipObject == None or "Cockpit" not in currentRoom.flags:
            console.write("You must be in a cockpit to do that.", "35w1y", True)
        elif currentRoom.spaceshipObject.landedLocation != None:
            console.write("You can't do that while landed.", "7w1y22w1y", True)
        elif currentRoom.spaceshipObject.launchLandTick != -1:
            actionString = currentRoom.spaceshipObject.launchLandAction.lower() + "ing"
            console.write("You can't do that while " + actionString + ".", "7w1y16w" + str(len(actionString)) + "w1y", True)
        elif currentRoom.spaceshipObject.planet != None or currentRoom.spaceshipObject.clearCourseCheck == True or (currentRoom.spaceshipObject.course == None and currentRoom.spaceshipObject.speedPercent == 0):
            console.write('''A computerized voice says, 'Please choose a heading.' ''', "25w3y23w2y", True)
        
        else:
            targetSpeed = None
            if throttleKey != None:
                if stringIsNumber(throttleKey):
                    targetSpeed = int(throttleKey)
                    if targetSpeed < 0 : targetSpeed = 0
                    elif targetSpeed > 100 : targetSpeed = 100
                elif throttleKey == "max":
                    targetSpeed = 100
                elif throttleKey in ["none", "off"]:
                    targetSpeed = 0

            if targetSpeed == None:
                displayString = '''A computerized voice says, 'Adjust speed using "Speed #/Max/None".' '''
                displayCode = "25w3y19w1y7w1r3w1r4w3y" 
                console.write(displayString, displayCode, True)
            elif targetSpeed == currentRoom.spaceshipObject.speedMod:
                console.write("The speed is already set to " + str(targetSpeed) + "%.", "28w" + str(len(str(targetSpeed))) + "w2y", True)

            else:
                if currentRoom.spaceshipObject.speedPercent == currentRoom.spaceshipObject.speedMod:
                    if targetSpeed > currentRoom.spaceshipObject.speedPercent:
                        currentRoom.spaceshipObject.displaySpeedUpMessage = 1
                        currentRoom.spaceshipObject.displaySlowDownMessage = False
                    else:
                        currentRoom.spaceshipObject.displaySlowDownMessage = 1
                        currentRoom.spaceshipObject.displaySpeedUpMessage = False
                currentRoom.spaceshipObject.speedMod = targetSpeed
                console.write("You adjust the throttle to " + str(targetSpeed) + "%.", "27w" + str(len(str(targetSpeed))) + "w2y", True)

    def scanCheck(self, console, galaxyList, player, currentRoom):
        if currentRoom.spaceshipObject == None or "Cockpit" not in currentRoom.flags:
            console.write("You must be in a cockpit to do that.", "35w1y", True)
        elif currentRoom.spaceshipObject.planet == None:
            console.write("You must be in orbit to scan for landing sites.", "46w1y", True)
        
        else:
            targetPlanet = galaxyList[currentRoom.spaceshipObject.galaxy].systemList[currentRoom.spaceshipObject.system].planetList[currentRoom.spaceshipObject.planet]
            underline = createUnderlineString("Scanning: " + targetPlanet.name["String"])
            console.write("Scanning: " + targetPlanet.name["String"], "8w2y" + targetPlanet.name["Code"], True)
            console.write(underline["String"], underline["Code"])

            landingRoomDataList = targetPlanet.getLandingRoomDataList()
            if len(landingRoomDataList) == 0:
                console.write("-No suitable landing locations.", "1y29w1y")

            else:
                for i, landingData in enumerate(landingRoomDataList):
                    displayString = "[" + str(i + 1) + "] [" + landingData["Area"].name["String"] + "] - " + landingData["Room"].name["String"]
                    displayCode = "1r" + str(len(str(i + 1))) + "w1r2y" + landingData["Area"].name["Code"] + "4y" + landingData["Room"].name["Code"]
                    console.write(displayString, displayCode)

    def landCheck(self, console, galaxyList, player, currentRoom, landKey):
        if currentRoom.spaceshipObject == None or "Cockpit" not in currentRoom.flags:
            console.write("You must be in a cockpit to do that.", "35w1y", True)
        elif currentRoom.spaceshipObject.landedLocation != None:
            console.write("You are already landed.", "22w1y", True)
        elif currentRoom.spaceshipObject.launchLandAction == "Launch":
            console.write("You can't do that while launching.", "7w1y25w1y", True)
        elif currentRoom.spaceshipObject.planet == None:
            console.write("You must be in orbit to do that.", "31w1y", True)
        elif landKey != None and stringIsNumber(landKey) == False:
            console.write('''A computerized voice says, 'Choose a landing site using "Land #".' ''', "25w3y28w1y6w3y", True)

        else:
            targetPlanet = galaxyList[currentRoom.spaceshipObject.galaxy].systemList[currentRoom.spaceshipObject.system].planetList[currentRoom.spaceshipObject.planet]
            landingRoomDataList = targetPlanet.getLandingRoomDataList()
            if len(landingRoomDataList) == 0:
                console.write('''A computerized voice says, 'There are no suitable landing sites.' ''', "25w3y35w2y", True)
            
            else:
                targetLandingIndex = 0
                if landKey != None:
                    targetLandingIndex = int(landKey) - 1
                    if targetLandingIndex < 0:
                        targetLandingIndex = 0
                    elif targetLandingIndex > len(landingRoomDataList) - 1:
                        targetLandingIndex = len(landingRoomDataList) - 1
                
                currentRoom.spaceshipObject.launchLandAction = "Land"
                currentRoom.spaceshipObject.launchLandTick = 0
                currentRoom.spaceshipObject.launchLandPhase = 0
                landingData = landingRoomDataList[targetLandingIndex]
                currentRoom.spaceshipObject.flags["Target Landing Location"] = [landingData["Area"].num, landingData["Room"].room]
                console.write('A computerized voice says, "Initiating landing sequence."', "25w3y27w2y", True)

    def manifestCheck(self, console, currentRoom, targetType, targetNum, targetCount):
        manifestTarget = None
        for i in range(targetCount):
            if targetType == "Mob":
                newMob = createMob(targetNum, currentRoom)
                if manifestTarget == None:
                    manifestTarget = newMob

        if manifestTarget == None:
            console.write("You wave your hand and nothing happens.", "38w1y", True)
        else:
            countString, countCode = getCountString(targetCount)
            console.write("You wave your hand and " + manifestTarget.prefix.lower() + " " + manifestTarget.name["String"] + " appears." + countString, "23w" + str(len(manifestTarget.prefix)) + "w1w" + manifestTarget.name["Code"] + "8w1y" + countCode, True)

    # Utility Functions #
    def getCombatSkillList(self, useableFirst=False):
        # Gets An Entire List Of Skills (No Rules) #

        skillList = []
        useableDominantHand = []
        useableOffHand = []
        for skillGroup in self.combatSkillDict:
            for skill in self.combatSkillDict[skillGroup]:
                skillList.append(skill)
                if useableFirst == True:
                    if skill.name["String"] == "Slash" and skill.weaponTypeList[0] == ["Polearm"] and \
                    self.gearDict["Left Hand"] != None and self.gearDict["Right Hand"] != None:
                        pass
                    elif skill.weaponAttackCheck(self.gearDict[self.dominantHand]) == True:
                        useableDominantHand.append(skill)
                    elif skill.weaponAttackCheck(self.gearDict[self.getOppositeHand(self.dominantHand)]) == True:
                        useableOffHand.append(skill)

        for gearSlot in self.gearDict:
            if isinstance(self.gearDict[gearSlot], list):
                gearList = self.gearDict[gearSlot]
            else:
                gearList = [self.gearDict[gearSlot]]
            for gear in gearList:
                if gear != None:
                    for skill in gear.skillList:
                        skillList.append(skill)
        
        return useableDominantHand + useableOffHand + skillList

    def getRandomAttackSkill(self, targetWeapon, secondWeapon, ruleCheckFlags):
        # Don't Choose Attacks That Don't Require Weapons #
        # Don't Choose Dodge, Block, Or Sweep #
        # Ammo Check #

        skillList = []
        returnMessage = None
        for skill in self.getCombatSkillList():
            if skill.name["String"] not in ["Dodge", "Block", "Sweep"] and skill.ruleCheck(ruleCheckFlags) == True:
                if not ("Disable Off Hand Attacks" in ruleCheckFlags and skill.offHandAttacks == False):
                    if self.skillWeaponCheck(skill, targetWeapon) == True:
                        if len(skill.weaponTypeList) == 0 and "Disable Weaponless Skills" in ruleCheckFlags:
                            pass
                        elif len(skill.weaponTypeList) > 0 and ("Pistol" in skill.weaponTypeList[0] or "Rifle" in skill.weaponTypeList[0]) and ((targetWeapon not in [None, "Unused"] and targetWeapon.isGun() and targetWeapon.isEmpty(True) == True) and (secondWeapon == None or (secondWeapon not in [None, "Unused"] and secondWeapon.isGun() and secondWeapon.isEmpty(True) == True))):
                            returnMessage = "Reload"
                            skillList.append(skill)
                        else:
                            skillList.append(skill)
                    
        if len(skillList) > 0:
            return random.choice(skillList), returnMessage
        return None, returnMessage

    def skillWeaponCheck(self, combatSkill, targetWeapon="Unused"):
        # Weapon Checks & Gear Skill Check #

        # Polearm Slash Check (Weapon Requires CutLimb%) #
        if combatSkill.name["String"] == "Slash" and combatSkill.weaponTypeList[0] == ["Polearm"]:
            if self.gearDict["Left Hand"] != None and self.gearDict["Right Hand"] != None:
                return False
            elif (self.gearDict["Left Hand"] != None and self.gearDict["Left Hand"].cutLimbPercent == 0) or \
            (self.gearDict["Right Hand"] != None and self.gearDict["Right Hand"].cutLimbPercent == 0):
                return False

        if "Gear Num List" in combatSkill.ruleDict:
            if targetWeapon == "Unused":
                playerGearDictNumList = self.getPlayerGearDictNumList()
                for gearNum in combatSkill.ruleDict["Gear Num List"]:
                    if gearNum in playerGearDictNumList:
                        return True
            elif combatSkill in targetWeapon.skillList:
                return True
            return False

        if len(combatSkill.weaponTypeList) == 0:
            return True
        elif len(combatSkill.weaponTypeList) == 1 and "Melee" in combatSkill.weaponTypeList[0]:
            if not (self.debugDualWield == False and self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].twoHanded == True):
                if targetWeapon == "Unused":
                    if (self.gearDict["Left Hand"] == None and "Left Arm" not in self.cutLimbList) or (self.gearDict["Right Hand"] == None and "Right Arm" not in self.cutLimbList):
                        return True
                elif targetWeapon in ["Melee", None]:
                    return True
        elif len(combatSkill.weaponTypeList) == 1:
            if targetWeapon == "Unused":
                if self.gearDict["Left Hand"] != None and self.gearDict["Left Hand"].weaponType in combatSkill.weaponTypeList[0]:
                    return True
                if self.gearDict["Right Hand"] != None and self.gearDict["Right Hand"].weaponType in combatSkill.weaponTypeList[0]:
                    return True
            elif (targetWeapon in ["Melee", None] and "Melee" in combatSkill.weaponTypeList[0]) or (targetWeapon != None and targetWeapon.weaponType in combatSkill.weaponTypeList[0]):
                return True

        elif len(combatSkill.weaponTypeList) == 2 and targetWeapon == "Unused" and len(self.cutLimbList) == 0:
            correctWeaponTypeList = [[], []]
            playerHeldList = []
            if self.gearDict["Left Hand"] == None : playerHeldList.append("Melee")
            else : playerHeldList.append(self.gearDict["Left Hand"])
            if self.gearDict["Right Hand"] == None : playerHeldList.append("Melee")
            else : playerHeldList.append(self.gearDict["Right Hand"])

            if playerHeldList[0] in combatSkill.weaponTypeList[0] and playerHeldList[1] in combatSkill.weaponTypeList[1]:
                return True
            elif playerHeldList[0] in combatSkill.weaponTypeList[1] and playerHeldList[1] in combatSkill.weaponTypeList[0]:
                return True
            
        return False
    
    def getCombatAction(self):
        if len(self.actionList) > 0 and self.actionList[0].actionType == "Combat Skill":
            return self.actionList[0].flags["combatSkill"]
        return None

    def ammoCheck(self, ammoType, ammoKey=None, magazineCheck=False):
        returnItem = None
        returnIndex = -1

        magSize = 0
        magazineIndex = -1
        targetQuiver = None
        for i, item in enumerate(self.itemDict["Ammo"]):
            if item.ammoType == ammoType and not (ammoKey != None and ammoKey not in item.keyList):
                if magazineCheck == False and item.ammoCapacity == None:
                    return item, i
                elif magazineCheck == True and item.ammoCapacity != None:
                    if item.ammoCapacity > magSize:
                        returnItem = item
                        magSize = item.ammoCapacity
                        magazineIndex = i

                elif magazineCheck == False and item.ammoType == "Arrow" and item.ammoCapacity != None:
                     if len(item.containerList) > 0:
                        targetQuiver = item

        if targetQuiver != None:
            return targetQuiver, None

        if magazineIndex != -1:
            returnIndex = magazineIndex
        return returnItem, returnIndex

    def getArmorRating(self):
        defenseDict = {"Piercing":0, "Cutting":0, "Blunt":0}
        for gearSlot in self.gearDict:
            if gearSlot not in ["Left Hand", "Right Hand"]:
                slotRange = 1
                if isinstance(self.gearDict[gearSlot], list):
                    slotRange = 2
                for slotNum in range(slotRange):
                    if isinstance(self.gearDict[gearSlot], list):
                        targetSlot = self.gearDict[gearSlot][slotNum]
                    else:
                        targetSlot = self.gearDict[gearSlot]
                        
                    if targetSlot != None:
                        defenseDict["Piercing"] += targetSlot.armorRating["Piercing"]
                        defenseDict["Cutting"] += targetSlot.armorRating["Cutting"]
                        defenseDict["Blunt"] += targetSlot.armorRating["Blunt"]

        return defenseDict

    def stopActions(self, console, galaxyList, player):
        if len(self.actionList) > 0:
            currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
            actionString = self.actionList[0].actionType.lower()
            if actionString == "combat skill":
                actionString = self.actionList[0].flags["combatSkill"].name["String"].lower()

            if self.num == None:
                console.write("You stop " + actionString + "ing.", "9w" + str(len(actionString)) + "w3w1y", True)
            elif currentRoom != None and currentRoom.sameRoomCheck(player):
                console.write(self.prefix + " " + self.name["String"] + " stops " + actionString + "ing.", str(len(self.prefix)) + "w1w" + self.name["Code"] + "7w" + str(len(actionString)) + "w3w1y", True)
            
            self.actionList = []
            return False
        return True

    def inStunnedTargetRoom(self, galaxyList):
        currentRoom = Room.exists(galaxyList, self.spaceship, self.galaxy, self.system, self.planet, self.area, self.room)
        if currentRoom != None:
            for mob in self.stunList:
                if currentRoom.sameRoomCheck(mob):
                    return True
        return False

    def getTargetItem(self, targetItemKey, includeList=["Inventory", "Gear"], targetItemPocket=None):
        if "Inventory" in includeList:
            for pocket in self.itemDict:
                for item in self.itemDict[pocket]:
                    if (isinstance(targetItemKey, str) and targetItemKey in item.keyList) or \
                    (isinstance(targetItemKey, int) and targetItemKey == item.num and targetItemPocket != None and targetItemPocket == item.pocket):
                        return item, "Inventory"
        if "Gear" in includeList:
            for gearSlot in self.gearDict:
                if isinstance(self.gearDict[gearSlot], list) == False:
                    if self.gearDict[gearSlot] != None:
                        if (isinstance(targetItemKey, str) and targetItemKey in self.gearDict[gearSlot].keyList) or \
                        (isinstance(targetItemKey, int) and targetItemKey == self.gearDict[gearSlot].num and targetItemPocket != None and targetItemPocket == self.gearDict[gearSlot].pocket):
                            return self.gearDict[gearSlot], "Gear"
                else:
                    for gearSubSlot in self.gearDict[gearSlot]:
                        if gearSubSlot != None:
                            if (isinstance(targetItemKey, str) and targetItemKey in gearSubSlot.keyList) or \
                            (isinstance(targetItemKey, int) and targetItemKey == gearSubSlot.num and targetItemPocket != None and targetItemPocket == gearSubSlot.pocket):
                                return gearSubSlot, "Gear"
        return None, None

    def getAllItemList(self, includeList=["Inventory", "Gear"]):
        itemList = []
        if "Inventory" in includeList:
            for pocket in self.itemDict:
                itemList = itemList + self.itemDict[pocket]
        if "Gear" in includeList:
            for gearSlot in self.gearDict:
                if isinstance(self.gearDict[gearSlot], list):
                    for subSlot in self.gearDict[gearSlot]:
                        if subSlot != None:
                            itemList.append(subSlot)
                elif self.gearDict[gearSlot] != None:
                    itemList.append(self.gearDict[gearSlot])
        return itemList

    def getPocketList(self, lowerCheck=False):
        pocketList = []
        for pocket in self.itemDict:
            if lowerCheck == True:
                pocketList.append(pocket.lower())
            else:
                pocketList.append(pocket)
        return pocketList

    def getWeight(self):
        currentWeight = 0.0
        for itemPocket in self.itemDict:
            for item in self.itemDict[itemPocket]:
                currentWeight += item.getWeight()
        for itemSlot in self.gearDict:
            if isinstance(self.gearDict[itemSlot], list):
                for subSlot in self.gearDict[itemSlot]:
                    if subSlot != None:
                        currentWeight += subSlot.getWeight()
            elif self.gearDict[itemSlot] != None:
                currentWeight += self.gearDict[itemSlot].getWeight()
        return currentWeight

    def getMaxWeight(self):
        return 100

    def getOppositeHand(self, targetHand):
        if targetHand == "Left Hand":
            return "Right Hand"
        else:
            return "Left Hand"

    def hasKey(self, password):
        for pocket in self.itemDict:
            for item in self.itemDict[pocket]:
                if "Password List" in item.flags:
                    for targetPassword in item.flags["Password List"]:
                        if targetPassword == password:
                            return True
        return False
    
    def lightInBagCheck(self, targetPocket):
        for item in self.itemDict[targetPocket]:
            if "Glowing" in item.flags and item.flags["Glowing"] == True:
                return True

        return False
    
    def getPlayerGearDictNumList(self):
        numList = []
        for item in self.getAllItemList(["Gear"]):
            numList.append(item.num)
        return numList

    def emote(self, console, input):
        if input in ["hmm", "hm"]:
            console.write("You scratch your chin and go, 'Hmm..'", "28w3y3w3y", True)
        elif input in "nod":
            console.write("You nod your head in agreement.", "30w1y", True)
        elif input == "nodnod":
            console.write("You nodnod.", "10w1y", True)
        elif input == "tap":
            console.write("You tap your foot impatiently..", "29w2y", True)
        elif input == "boggle":
            console.write("You boggle in complete incomprehension.", "38w1y", True)
        elif input == "jump":
            console.write("You jump up and down.", "20w1y", True)
        elif input == "ahah":
            console.write("Comprehension dawns upon you.", "28w1y", True)
        elif input == "gasp":
            console.write("You gasp!", "8w1y", True)
        elif input in ["haha", "lol"]:
            console.write("You laugh out loud!", "18w1y", True)
        elif input == "cheer":
            console.write("And the peasants rejoiced.", "25w1y", True)
        elif input == "smile":
            console.write("You smile happily.", "17w1y", True)
        elif input == "swear":
            swearString = "@#$%"
            displayString = "!"
            displayCode = ""
            for i in range(4):
                targetChar = swearString[random.randrange(len(swearString))]
                displayString = targetChar + displayString
                swearString = swearString.replace(targetChar, "")
            if random.randrange(4) == 0:
                mNum = random.randrange(3)
                if mNum == 0 : displayString = "Holy " + displayString
                elif mNum == 1 : displayString = "God " + displayString
                else:
                    displayString = "I sure am one foul-mouthed son of a gun!"
                    displayCode = "18w1y20w1y"
            if displayCode == "":
                displayCode = str(len(displayString) - 1) + "w1y"
            console.write(displayString, displayCode, True)
        elif input == "sigh":
            console.write("You sigh.", "8w1y", True)
        elif input == "grin":
            console.write("You grin.", "8w1y", True)
        elif input == "snicker":
            console.write("You snicker softly.", "18w1y", True)
        elif input == "whistle":
            console.write("You whistle innocently.", "22w1y", True)
        
    # Mob Functions #
    def loadMob(self, num):
        if num == 1:
            self.name = {"String":"Robotic Greeter Droid", "Code":"21w"}
            self.speechList = [{"String":"Welcome to the COTU Spaceport!", "Code":"29w1y"}, \
                               {"String":"Please have your badge ready.", "Code":"28w1y"}]
        elif num == 2:
            self.name = {"String":"Spider", "Code":"1w5ddw"}

        # Create Key List #
        appendKeyList(self.keyList, self.name["String"].lower())

    def lookDescription(self, console, galaxyList, player, currentRoom):
        targetNameString = self.prefix.lower() + " " + self.name["String"]
        targetNameCode = str(len(self.prefix)) + "w1w" + self.name["Code"]
        youString = "They"
        if self.num == None:
            targetNameString = "yourself"
            targetNameCode = "8w"
            youString = "You"
        console.write("You look at " + targetNameString + ".", "12w" + targetNameCode + "1y", True)
        console.write("You see nothing special.", "23w1y")
        console.write(youString + " are wearing:", str(len(youString)) + "w12w1y")
        self.displayGear(console, galaxyList, player, currentRoom, True)
