import copy, random
from GameData.World.Room import Room
from GameData.World.Spaceship import Spaceship
from GameData.Item import Item
from GameData.Skill import Skill
from GameData.Action import Action
from GameData.Combat import Combat
from Components.Utility import appendKeyList
from Components.Utility import stringIsNumber
from Components.Utility import getCountString
from Components.Utility import wordWrap

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

        self.actionList = []
        self.combatSkillList = [Skill(1), Skill(2), Skill(3), Skill(4), Skill(5), Skill(6), Skill(7), Skill(8), Skill(9), Skill(11), Skill(12), Skill(13)]

        self.currentHealth = 2

        self.maxLookDistance = 3
        self.maxTargetDistance = 2
        self.targetList = [] # Not Used For Mobs
        self.recruitList = []
        self.combatList = [] # Player - Contains Other Mobs, Mobs - Also Only Contains Other Mobs

        self.itemDict = {"Armor": [], "Weapon":[], "Ammo":[], "Misc": []}
        self.gearDict = {"Head":None, "Face":None, "Neck":[None, None], "Body Under":None, "Body Over":None, "About Body":None, "Hands":None, "Finger":[None, None], "Legs Under":None, "Legs Over":None, "Feet":None, "Left Hand":None, "Right Hand":None}
        self.dominantHand = "Right Hand"

        self.emoteList = ["hmm", "hm", "nod", "nodnod", "tap", "boggle", "ahah", "jump", "gasp", "haha", "lol", "cheer", "smile", "swear", "sigh", "grin", "snicker"]

        self.autoLoot = False
        self.autoReload = False
        self.teamDamage = True
        self.healEnemies = True

        self.debugDualWield = False

        if num != None:
            self.loadMob(num)

    def update(self, console, galaxyList, player, currentRoom):
        if self.num != None:
            distanceToPlayer, directionToPlayer, unused = Room.getTargetRange(galaxyList, currentRoom, player, self.maxTargetDistance)
            
            # Chase Player #
            if self in player.combatList and distanceToPlayer != -1:
                
                # Next Room Locked Door Check #
                if "No Chase" not in self.flags and distanceToPlayer > 0 \
                and not (currentRoom.door[directionToPlayer] != None and currentRoom.door[directionToPlayer]["Status"] == "Locked" and "Password" in currentRoom.door[directionToPlayer] and self.hasKey(currentRoom.door[directionToPlayer]["Password"]) == False):
                    self.moveCheck(console, map, galaxyList, player, currentRoom, directionToPlayer.lower())

    def lookDirection(self, console, galaxyList, currentRoom, lookDir, count):
        if isinstance(count, int) and count > 50:
            count = 50
        messageType = None
        lookCheck = False
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
                lookCheck = True
                if len(currentRoom.exit[lookDir]) == 3 and currentRoom.spaceshipObject != None:
                    currentRoom = currentRoom.spaceshipObject.areaList[currentRoom.exit[lookDir][1]].roomList[currentRoom.exit[lookDir][2]]
                elif len(currentRoom.exit[lookDir]) == 5:
                    currentRoom = Room.exists(galaxyList, None, currentRoom.exit[lookDir][0], currentRoom.exit[lookDir][1], currentRoom.exit[lookDir][2], currentRoom.exit[lookDir][3], currentRoom.exit[lookDir][4])
                    if currentRoom == None:
                        currentRoom = galaxyList[0].systemList[0].planetList[0].areaList[0].roomList[0]
                    
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

        if messageType == None and count > self.maxLookDistance:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't see that far." + countString, "Code":"7w1y14w1y" + countCode})
        elif messageType != None:
            console.lineList.insert(0, {"Blank": True})
            if messageType == "Can't See Further":
                console.lineList.insert(0, {"String":"You can't see any farther to the " + lookDir + "." + countString, "Code":"7w1y25w" + str(len(lookDir)) + "w1y" + countCode})
            elif messageType == "View Obstructed":
                console.lineList.insert(0, {"String":"Your view to the " + lookDir + " is obstructed." + countString, "Code":"17w" + str(len(lookDir)) + "w14w1y" + countCode})
        if lookCheck:
            console.lineList.insert(0, {"Blank": True})
            currentRoom.display(console, galaxyList, self)
    
    def lookTargetCheck(self, console, galaxyList, currentRoom, lookDir, count, lookTarget):
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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "There is nothing there.", "Code":"22w1y"})
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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "Your view to the " + lookDir + " is obstructed." + countString, "Code":"17w" + str(len(lookDir)) + "w14w1y" + countCode})
            
            if lookCount > 0:
                console.lineList.insert(0, {"Blank": True})
                currentRoom.display(console, galaxyList, self)

        else:
            roomTarget = None
            if count == None:
                roomTarget, playerItemLocation = self.getTargetItem(lookTarget)
            if roomTarget == None:
                roomTarget = currentRoom.getTargetObject(lookTarget)

            if currentRoom.isLit(galaxyList, self) == False and not (isinstance(roomTarget, Item) and roomTarget.containerList != None and roomTarget.lightInContainerCheck() == True):
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})
            elif roomTarget == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You don't see anything like that.", "Code":"7w1y24w1y"})
            else:
                if isinstance(roomTarget, Item):
                    passwordCheck = False
                    if roomTarget.containerPassword != None:
                        passwordCheck = self.hasKey(roomTarget.containerPassword)
                    roomTarget.lookDescription(console, lookCount, passwordCheck)
                else:
                    roomTarget.lookDescription(console)

    def lookItemInContainerCheck(self, console, currentRoom, targetItemKey, targetContainerKey):
        targetContainer = currentRoom.getTargetObject(targetContainerKey)
        if targetContainer == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You can't find it.", "Code":"7w1y9w1y"})
        elif isinstance(targetContainer, Item) == False or targetContainer.containerList == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "That's not a container!", "Code":"4w1y17w1y"})
        else:
            containerItem = targetContainer.getContainerItem(targetItemKey)
            if containerItem == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You don't see anything like that.", "Code":"7w1y24w1y"})
            else:
                containerItem.lookDescription(console)

    def targetCheck(self, console, galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, targetDirCount):
        if targetDirCount != None and targetDirCount > self.maxLookDistance:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't see that far.", "Code":"7w1y14w1y"})
        
        else:
            targetRoom = currentRoom
            messageType = None
            roomCount = 0
            targetDir = None
            if targetDirKey != None and targetDirCount != None:
                if targetDirKey in ["north", "nort", "nor", "no", "n"] : targetDir = "North"
                elif targetDirKey in ["east", "eas", "ea", "e"] : targetDir = "East"
                elif targetDirKey in ["south", "sout", "sou", "so", "s"] : targetDir = "South"
                else : targetDir = "West"

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
                            targetRoom = Room.exists(galaxyList, None, landedLocation[0], landedLocation[1], landedLocation[2], landedLocation[3], landedLocation[4])
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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"There is nothing there.", "Code":"22w1y"})
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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"Your view to the " + targetDir + " is obstructed." + countString, "Code":"17w" + str(len(targetDir)) + "w14w1y" + countCode})
        
            else:
                targetMob = None
                if targetMobKey != "All":
                    targetMob = targetRoom.getTargetObject(targetMobKey)

                if targetMobKey != "All" and targetMob == None:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String": "You don't see them.", "Code":"7w1y10w1y"})
                elif targetMob != None and hasattr(targetMob, "dominantHand") == False:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You can't target that.", "Code":"7w1y13w1y"})
                
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
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You are already targeting them.", "Code":"30w1y"})
                    elif targetCount == 0:
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You don't see them.", "Code":"7w1y10w1y"})
                    
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
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":displayString + targetCountString + dirString + dirCountString, "Code":displayCode + targetCountCode + dirCode + dirCountCode})
                    
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
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":displayString + dirString + dirCountString, "Code":displayCode + dirCode + dirCountCode})

    def untargetCheck(self, console, galaxyList, currentRoom, targetMobKey, targetDirKey, targetMobCount, targetDirCount):
        if targetDirCount != None and targetDirCount > self.maxLookDistance:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't see that far.", "Code":"7w1y14w1y"})
        
        else:
            targetRoom = currentRoom
            messageType = None
            roomCount = 0
            targetDir = None
            if targetDirKey != None and targetDirCount != None:
                if targetDirKey in ["north", "nort", "nor", "no", "n"] : targetDir = "North"
                elif targetDirKey in ["east", "eas", "ea", "e"] : targetDir = "East"
                elif targetDirKey in ["south", "sout", "sou", "so", "s"] : targetDir = "South"
                else : targetDir = "West"

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
                            targetRoom = Room.exists(galaxyList, None, landedLocation[0], landedLocation[1], landedLocation[2], landedLocation[3], landedLocation[4])
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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"There is nothing there.", "Code":"22w1y"})
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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"Your view to the " + targetDir + " is obstructed." + countString, "Code":"17w" + str(len(targetDir)) + "w14w1y" + countCode})
        
            else:
                targetMob = None
                if targetDirKey != None and targetMobKey != "All":
                    targetMob = targetRoom.getTargetObject(targetMobKey)
                    if targetMob == None:
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String": "You don't see them.", "Code":"7w1y10w1y"})
                        return
                    elif hasattr(targetMob, "dominantHand") == False:
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You can't target that.", "Code":"7w1y13w1y"})
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
                                    targetMobRange, targetMobDir, message =  Room.getTargetRange(galaxyList, targetRoom, targetMob, self.maxTargetDistance)
                                    if targetMobRange != -1 and targetMobDir != None:
                                        targetDir = targetMobDir
                                        roomCount = targetMobRange
                                    targetMob = "Multiple"
                                break
                                
                if targetMobCount == "All" and targetMobKey != "All" and targetMob == None:
                    targetMob = targetRoom.getTargetObject(targetMobKey, ["Mobs"])

                if targetCount > 1 and targetMobKey == "All":
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You take a breath out and relax your mind.", "Code":"41w1y"})
                elif targetMob == "Multiple" and len(targetRoomList) > 1:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You relax your mind a little.", "Code":"28w1y"})
                elif targetCount == 0 and targetDirKey == None and targetMobKey == "All":
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You aren't targeting anyone.", "Code":"8w1y18w1y"})
                elif targetCount == 0 and targetMob == None:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You don't see them.", "Code":"7w1y10w1y"})
                elif targetCount == 0:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You aren't targeting them.", "Code":"8w1y16w1y"})
                
                elif targetMob != "Multiple":
                    if targetDirKey == None and targetDirCount == None and targetMob not in targetRoom.mobList and len(targetRoomList) == 1:
                        targetMobRange, targetMobDir, message =  Room.getTargetRange(galaxyList, targetRoom, targetMob, self.maxTargetDistance)
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
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString + targetCountString + dirString + dirCountString, "Code":displayCode + targetCountCode + dirCode + dirCountCode})
                
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
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString + dirString + dirCountString, "Code":displayCode + dirCode + dirCountCode})

    def moveCheck(self, console, map, galaxyList, player, currentRoom, targetDirKey):
        if targetDirKey.lower() in ["north", "nort", "nor", "no", "n"] : targetDir = "North"
        elif targetDirKey.lower() in ["east", "eas", "ea", "e"] : targetDir = "East"
        elif targetDirKey.lower() in ["south", "sout", "sou", "so", "s"] : targetDir = "South"
        else : targetDir = "West"
        
        if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Manual" and currentRoom.door[targetDir]["Status"] in ["Closed", "Locked"]:
            if self.num == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The door is closed.", "Code":"18w1y"})
        elif currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic" and currentRoom.door[targetDir]["Status"] == "Locked" and "Password" in currentRoom.door[targetDir] and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
            if self.num == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You lack the proper key.", "Code":"23w1y"})
        elif currentRoom.exit[targetDir] == None:
            if self.num == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You can't go that way!", "Code":"7w1y13w1y"})

        else:
            mobString = self.prefix + " " + self.name["String"]
            mobCode = str(len(self.prefix)) + "w1w" + self.name["Code"]
            if len(self.actionList) > 0:
                self.actionList = []
                if self.num == None:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String": "You stop what you're doing and move.", "Code":"17w1y17w1y"})
                elif currentRoom.sameRoomCheck(player):
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":mobString + " stops what they're doing and moves " + targetDir + ".", "Code":mobCode + "16w1y19w" + str(len(targetDir)) + "w1y"})
            elif self.num != None and currentRoom.sameRoomCheck(player) and not (currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic"):
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":mobString + " moves " + targetDir + ".", "Code":mobCode + "7w" + str(len(targetDir)) + "w1y"})

            currentArea = Room.getAreaAndRoom(galaxyList, self)[0]
            targetArea, targetRoom, unusedDistance, unusedMessage = Room.getTargetRoomFromStartRoom(galaxyList, currentArea, currentRoom, targetDir, 1, True)

            # Move #
            automaticDoorCheck = False
            if targetRoom.spaceshipObject != None:
                self.area = targetRoom.area
                self.room = targetRoom.room
            else:
                self.galaxy = targetRoom.galaxy
                self.system = targetRoom.system
                self.planet = targetRoom.planet
                self.area = targetRoom.area
                self.room = targetRoom.room
                if self.spaceship != None:
                    self.spaceship = None
                    if self.num == None:
                        map.loadMap(targetArea)
                
                if self.num == None or targetRoom.sameRoomCheck(player) == True or currentRoom.sameRoomCheck(player) == True:
                    if self.num == None:
                        console.lineList.insert(0, {"Blank": True})
                    if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic":
                        doorString = "door"
                        if currentRoom.exit[targetDir] == "Spaceship Exit":
                            doorString = "hatch"
                        if self.num == None:
                            console.lineList.insert(0, {"String": "The " + doorString + " opens and closes as you walk through.", "Code":"4w" + str(len(doorString)) + "w37w1y"})
                        else:
                            displayDirection = targetDir
                            leavesString = " leaves"
                            if targetRoom.sameRoomCheck(player) == True:
                                displayDirection = Room.getOppositeDirection(targetDir)
                                leavesString = " enters"
                            displayString = "The door to the " + displayDirection + " opens and closes as " + mobString + leavesString + "."
                            displayCode = "16w" + str(len(displayDirection)) + "w21w" + mobCode + str(len(leavesString)) + "w1y"
                            console.lineList.insert(0, {"Blank": True})
                            for displayLine in wordWrap(displayString, displayCode, console.characterWidth):
                                console.lineList.insert(0, {"String":displayLine["String"], "Code":displayLine["Code"]})
                        if self.num == None:
                            console.lineList.insert(0, {"Blank": True})
                        automaticDoorCheck = True

            if self.num != None:
                if self in currentRoom.mobList:
                    del currentRoom.mobList[currentRoom.mobList.index(self)]
                targetRoom.mobList.append(self)

            delTargetList = []
            delMobData = None
            loseSightDir = None
            if self.num == None:
                for targetMob in self.targetList:
                    distance, direction, message = Room.getTargetRange(galaxyList, targetRoom, targetMob, self.maxTargetDistance + 1)
                    if distance == self.maxTargetDistance + 1:
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

            if self.num == None and len(delTargetList) > 0:
                countString, countCode = getCountString(len(delTargetList))
                if delMobData != "Multiple":
                    displayString = "You lose sight of " + delMobData.prefix.lower() + " " + delMobData.name["String"] + countString + " to the " + loseSightDir + "."
                    displayCode = "18w" + str(len(delMobData.prefix)) + "w1w" + delMobData.name["Code"] + countCode + "8w" + str(len(loseSightDir)) + "w1y"
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                else:
                    someString = "some"
                    if len(self.targetList) == 0:
                        someString = "your"
                    displayString = "You lose sight of " + someString + " targets" + countString + " to the " + loseSightDir + "."
                    displayCode = "18w" + str(len(someString)) + "w8w" + countCode + "8w" + str(len(loseSightDir)) + "w1y"
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})

            elif self.num != None and targetRoom.sameRoomCheck(player) == True and automaticDoorCheck == False:
                displayString = self.prefix + " " + self.name["String"] + " enters from the " + Room.getOppositeDirection(targetDir) + "."
                displayCode = str(len(self.prefix)) + "w1w" + self.name["Code"] + "17w" + str(len(Room.getOppositeDirection(targetDir))) + "w1y"
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})

    def openCloseDoorCheck(self, console, galaxyList, currentRoom, targetAction, targetDir):
        targetDoorAction = targetAction
        if targetAction == "Close":
            targetDoorAction = "Closed"

        if currentRoom.door[targetDir] == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"There is no door in that direction.", "Code":"34w1y"})
        elif currentRoom.door[targetDir]["Type"] == "Automatic":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door is automatic.", "Code":"22w1y"})
        elif currentRoom.door[targetDir]["Status"] == targetDoorAction or (targetDoorAction == "Closed" and currentRoom.door[targetDir]["Status"] == "Locked"):
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"It's already " + targetDoorAction.lower() + ".", "Code":"2w1y10w" + str(len(targetDoorAction)) + "w1y"})
        
        else:
            blankCheck = self.stopActions(console)

            if targetDoorAction == "Open" and currentRoom.door[targetDir]["Status"] == "Locked" and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"It's locked.", "Code":"2w1y8w1y"})
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

                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You " + unlockString + targetAction.lower() + " the door to the " + targetDir + ".", "Code":"4w" + unlockCode + str(len(targetAction)) + "w17w" + str(len(targetDir)) + "w1y"})

    def lockUnlockDoorCheck(self, console, galaxyList, currentRoom, targetAction, targetDir):
        if targetAction == "Lock":
            targetActionStatus = "Locked"
        else:
            targetActionStatus = "Closed"

        if currentRoom.door[targetDir] == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"There is no door in that direction.", "Code":"34w1y"})
        elif "Password" not in currentRoom.door[targetDir]:
            haveString = "require a key"
            if targetAction == "Lock":
                haveString = "have a lock"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door doesn't " + haveString + ".", "Code":"15w1y2w" + str(len(haveString)) + "w1y"})
        elif currentRoom.door[targetDir]["Type"] == "Automatic":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That door " + targetAction.lower() + "s automatically.", "Code":"10w" + str(len(targetAction)) + "w15w1y"})
        elif currentRoom.door[targetDir]["Status"] == targetActionStatus:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"It's already " + targetAction.lower() + "ed.", "Code":"2w1y10w" + str(len(targetAction)) + "w2w1y"})
        
        else:
            blankCheck = self.stopActions(console)

            if self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You lack the key.", "Code":"16w1y"})
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
                        
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You " + closeString + targetAction.lower() + " the door to the " + targetDir + ".", "Code":"4w" + closeCode + str(len(targetAction)) + "w17w" + str(len(targetDir)) + "w1y"})

    def openCloseTargetCheck(self, console, galaxyList, currentRoom, targetAction, targetObjectKey):
        targetObject = currentRoom.getTargetObject(targetObjectKey)
        if targetObject == None:
            targetObject, playerItemLocation = self.getTargetItem(targetObjectKey)

        if currentRoom.isLit(galaxyList, self) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})
        elif targetObject == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You don't see anything like that.", "Code":"7w1y24w1y"})
        
        elif hasattr(targetObject, "dominantHand") == True:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You can't " + targetAction.lower() + " that!", "Code":"7w1y2w" + str(len(targetAction)) + "w5w1y"})
        
        elif isinstance(targetObject, Spaceship):
            if targetObject.hatchPassword != None and self.hasKey(targetObject.hatchPassword) == False:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "It's locked.", "Code":"2w1y8w1y"})
            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The hatch " + targetAction.lower() + "s automatically.", "Code":"10w" + str(len(targetAction)) + "w15w1y"})
            
        elif isinstance(targetObject, Item):
            if targetObject.containerList == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "It doesn't " + targetAction.lower() + ".", "Code":"8w1y2w" + str(len(targetAction)) + "w1y"})
            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"There is no need to " + targetAction.lower() + " it.", "Code":"20w" + str(len(targetAction)) + "w3w1y"})
            
    def lockUnlockTargetCheck(self, console, galaxyList, currentRoom, targetAction, targetObjectKey):
        targetObject = currentRoom.getTargetObject(targetObjectKey)
        if targetObject == None:
            targetObject, playerItemLocation = self.getTargetItem(targetObjectKey)
            
        if currentRoom.isLit(galaxyList, self) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})
        elif targetObject == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You don't see anything like that.", "Code":"7w1y24w1y"})
        
        elif hasattr(targetObject, "dominantHand") == True:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You can't " + targetAction.lower() + " that!", "Code":"7w1y2w" + str(len(targetAction)) + "w5w1y"})
        
        elif isinstance(targetObject, Spaceship):
            if targetObject.hatchPassword == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The hatch doesn't have a lock.", "Code":"15w1y13w1y"})
            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The hatch " + targetAction.lower() + "s automatically.", "Code":"10w" + str(len(targetAction)) + "w15w1y"})
        
        elif isinstance(targetObject, Item):
            if targetObject.containerList == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "It doesn't " + targetAction.lower() + ".", "Code":"8w1y2w" + str(len(targetAction)) + "w1y"})
            else:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"There is no need to " + targetAction.lower() + " it.", "Code":"20w" + str(len(targetAction)) + "w3w1y"})

    def getCheck(self, console, galaxyList, currentRoom, targetItemKey, targetContainerKey, count):
        blankCheck = self.stopActions(console)

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
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That's not a container!", "Code":"4w1y17w1y"})
        else:
            if targetItemKey == "All" and (targetContainerKey in ["All", None]) and count == "All":
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
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

            else:
                if itemList == "All Room Containers":
                    itemCount = 0
                    for container in combinedItemList:
                        if container.containerList != None and len(container.containerList) > 0:
                            itemCount += len(container.containerList)
                else:
                    itemCount = len(itemList)

                if targetContainerKey == "All" and itemCount == 0:
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"There is nothing to loot.", "Code":"24w1y"})
                
                else:
                    getCount = 0
                    quantityCount = count
                    getContainerIndexList = []
                    targetContainer = None
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
                                        if item.quantity != None:
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

                                            inventoryQuantityItem, unused = self.getTargetItem(item.num, ["Inventory"])
                                            if inventoryQuantityItem != None:
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
                                        elif getItem != "Multiple" and getItem.num != item.num:
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
                            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't carry that much weight.", "Code":"7w1y24w1y"})
                        elif noGetCheck == True:
                            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick that up.", "Code":"7w1y14w1y"})
                        elif itemCount == 0:
                            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"There is nothing to get.", "Code":"23w1y"})
                        else:
                            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick anything up.", "Code":"7w1y18w1y"})
                    else:
                        if targetContainerKey == "All" and getCount > 1 and (count == "All" or len(getContainerIndexList) > 1):
                            modString = ""
                            modCode = ""
                            if tooMuchWeightCheck == False and targetItemKey == "All":
                                modString = "every corner of "
                                modCode = "16w"
                            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You loot " + modString + "the place.", "Code":"9w" + modCode + "9w1y"})
                        elif targetContainerKey == None and getItem == "Multiple" and getCount > 1 and getCount == itemCount:
                            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You pick everything up.", "Code":"22w1y"})
                        elif getItem == "Multiple":
                            if targetContainerKey == "All" : totalContainerCount = len(combinedItemList)
                            else:
                                if playerItemLocation != None : totalContainerCount = len(self.getAllItemList([playerItemLocation]))
                                else : totalContainerCount = len(currentRoom.itemList)
                            if targetContainerKey != None and getContainerIndexList[-1] < totalContainerCount:
                                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                                console.lineList.insert(0, {"String":"You get some things out of " + targetContainer.prefix.lower() + " " + targetContainer.name["String"] + ".", "Code":"27w" + str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"] + "1y"})
                            else:
                                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                                console.lineList.insert(0, {"String":"You pick some things up.", "Code":"23w1y"})
                        elif getItem != "Multiple":
                            countString, countCode = getCountString(getCount)
                            fromString = ""
                            fromCode = ""
                            if targetContainerKey == "All" : totalContainerCount = len(combinedItemList)
                            else:
                                if playerItemLocation != None : totalContainerCount = len(self.getAllItemList([playerItemLocation]))
                                else : totalContainerCount = len(currentRoom.itemList)
                            if targetContainerKey != None and getContainerIndexList[0] < totalContainerCount:
                                targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                                targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                                if currentRoom.isLit(galaxyList, self) == False:
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
                            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":getString, "Code":getCode})
         
    def putCheck(self, console, galaxyList, currentRoom, targetItemKey, targetContainerKey, count):
        blankCheck = self.stopActions(console)

        targetContainer, playerItemLocation = self.getTargetItem(targetContainerKey)
        if targetContainer == None:
            targetContainer = currentRoom.getTargetObject(targetContainerKey, ["Mobs", "Items", "Spaceships"])
    
        if targetContainer == None:
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
        elif isinstance(targetContainer, Item) == False or targetContainer.containerList == None:
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"That's not a container!", "Code":"4w1y17w1y"})
        
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
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
            elif targetItemKey != "All" and putItem == targetContainer:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't put something inside itself.", "Code":"7w1y29w1y"})
            elif inventorySize == 0:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have anything to put in.", "Code":"7w1y25w1y"})

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
                                    if item.quantity != None:
                                        if quantityCount != "All" : putQuantity = quantityCount
                                        else : putQuantity = item.quantity
                                        if putQuantity > item.quantity:
                                            putQuantity = item.quantity
                                        if putQuantity * item.getWeight(False) > targetContainer.containerMaxLimit - targetContainer.getContainerWeight():
                                            putQuantity = int((targetContainer.containerMaxLimit - targetContainer.getContainerWeight()) / item.getWeight(False))
                                            
                                        containerQuantityItem = targetContainer.getContainerItem(item.num)
                                        if containerQuantityItem != None:
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
                                    elif putItem != "Multiple" and putItem.num != item.num:
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
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"It won't fit.", "Code":"6w1y5w1y"})
                elif putCount == 0:
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You don't have anything to put in.", "Code":"7w1y25w1y"})
                elif putItem == "Multiple":
                    targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                    targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                    if currentRoom.isLit(galaxyList, self) == False:
                        targetContainerString = "something"
                        targetContainerCode = "9w"
                    displayString = "You put some things in " + targetContainerString + "."
                    displayCode = "23w" + targetContainerCode + "1y"
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                else:
                    countString, countCode = getCountString(putCount)
                    targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                    targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                    if currentRoom.isLit(galaxyList, self) == False:
                        targetContainerString = "something"
                        targetContainerCode = "9w"
                    displayString = "You put " + putItem.prefix.lower() + " " + putItem.name["String"] + countString + " in " + targetContainerString + "."
                    displayCode = "8w" + str(len(putItem.prefix)) + "w1w" + putItem.name["Code"] + countCode + "4w" + targetContainerCode + "1y"
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                
    def dropCheck(self, console, galaxyList, currentRoom, targetItemKey, count, pocketKey=None):
        blankCheck = self.stopActions(console)

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
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

        else:
            dropCount = 0
            quantityCount = count
            delDict = {}
            breakCheck = False
            for pocket in self.itemDict:
                delDict[pocket] = []
                for i, item in enumerate(self.itemDict[pocket]):
                    if (targetItemKey == "All" or targetItemKey in item.keyList) and not (pocketKey != None and pocket != pocketKey):
                        if item.quantity != None:
                            if quantityCount != "All" : dropQuantity = quantityCount
                            else : dropQuantity = item.quantity
                            if dropQuantity > item.quantity:
                                dropQuantity = item.quantity
                            roomQuantityItem = currentRoom.getTargetObject(item.num, ["Items"])
                            if roomQuantityItem != None:
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
                        elif dropItem != "Multiple" and dropItem.num != item.num:
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
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You aren't carrying anything.", "Code":"8w1y19w1y"})
            elif dropCount > 1 and dropCount == inventoryCount:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You drop everything on the ground.", "Code":"33w1y"})    
            elif dropItem == "Multiple":
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You drop some things on the ground.", "Code":"34w1y"})
            elif dropItem != None:
                itemNameString = dropItem.prefix.lower() + " " + dropItem.name["String"]
                itemNameCode = str(len(dropItem.prefix)) + "w1w" + dropItem.name["Code"]
                if dropItem.num == Item.getSpecialItemNum("Corpse"):
                    itemNameString = "a corpse"
                    itemNameCode = "8w"
                countString, countCode = getCountString(dropCount)
                dropString = "You drop " + itemNameString + " on the ground." + countString
                dropCode = "9w" + itemNameCode + "14w1y" + countCode
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":dropString, "Code":dropCode})

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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":displayString, "Code":displayCode})
        else:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You switch your handedness to your " + self.dominantHand.lower() + ".", "Code":"35w" + str(len(self.dominantHand)) + "w1y"})

    def reloadCheck(self, console, galaxyList, player, currentRoom, reloadKey, reloadSlotKey, ammoKey):
        if currentRoom.isLit(galaxyList, player) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})

        else:
            blankCheck = self.stopActions(console)

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
                    if self.gearDict[reloadSlot].pocket == "Weapon" and self.gearDict[reloadSlot].ranged == True:
                        reloadList.append(self.gearDict[reloadSlot])
                    else:
                        targetItem = self.gearDict[reloadSlot]
            elif reloadKey == "All":
                if self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].pocket == "Weapon" and self.gearDict[self.dominantHand].ranged == True:
                    reloadList.append(self.gearDict[self.dominantHand])
                if self.gearDict[self.getOppositeHand(self.dominantHand)] != None and self.gearDict[self.getOppositeHand(self.dominantHand)].pocket == "Weapon" and self.gearDict[self.getOppositeHand(self.dominantHand)].ranged == True:
                    reloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
                if reloadSlotKey == "All":
                    for pocket in self.itemDict:
                        for item in self.itemDict[pocket]:
                            if pocket == "Weapon" and item.ranged == True:
                                reloadList.append(item)
                                gunInventoryCount += 1
            else:
                if self.gearDict["Left Hand"] != None and reloadKey in self.gearDict["Left Hand"].keyList:
                    if self.gearDict["Left Hand"].ranged == True:
                        reloadList.append(self.gearDict["Left Hand"])
                    else:
                        targetItem = self.gearDict["Left Hand"]
                elif self.gearDict["Right Hand"] != None and reloadKey in self.gearDict["Right Hand"].keyList:
                    if self.gearDict["Right Hand"].ranged == True:
                        reloadList.append(self.gearDict["Right Hand"])
                    else:
                        targetItem = self.gearDict["Right Hand"]
                else:
                    for item in self.getAllItemList(["Inventory"]):
                        if reloadKey in item.keyList:
                            if item.pocket == "Weapon" and item.ranged == True:
                                reloadList.append(item)
                                targetItem = None
                                break
                            else:
                                targetItem = item

            reloadTargetShiftCheck = False
            if reloadKey not in ["All", None] and reloadSlotKey == None and ammoKey == None:
                if len(reloadList) == 0:
                    reloadTargetShiftCheck = True
                    if self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].ranged == True:
                        reloadList.append(self.gearDict[self.dominantHand])
                    if self.gearDict[self.getOppositeHand(self.dominantHand)] != None and self.gearDict[self.getOppositeHand(self.dominantHand)].ranged == True:
                        reloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
                            
            alreadyReloadedCheck = False
            if reloadKey == "All" and len(reloadList) > 0 and ammoKey == None:
                alreadyReloadedCheck = True
                for weapon in reloadList:
                    if weapon.isLoaded(self.itemDict["Ammo"]) == False:
                        alreadyReloadedCheck = False
                        break 

            if reloadKey not in ["All", None] and len(reloadList) == 0 and targetItem != None and targetItem.ranged == False:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't reload that.", "Code":"7w1y13w1y"})
            elif alreadyReloadedCheck == True:
                displayString = "It's already loaded."
                displayCode = "2w1y16w1y"
                if len(reloadList) > 1:
                    displayString = "Your weapons are already loaded."
                    displayCode = "31w1y"
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            elif reloadKey == "All" and len(reloadList) == 0:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have anything to reload.", "Code":"7w1y25w1y"})
            elif reloadKey not in ["All", None] and len(reloadList) == 0 and targetItem == None:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
            elif (reloadSlot != None or reloadKey not in ["All", None]) and len(reloadList) == 0 and targetItem != None and not (reloadKey not in ["All", None] and reloadSlotKey == None and ammoKey == None):
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't reload that.", "Code":"7w1y13w1y"})
            elif reloadSlot != None and len(reloadList) == 0 and targetItem == None:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You aren't holding anything.", "Code":"8w1y18w1y"})

            else:
                playerCopy = copy.deepcopy(self)
                magazineCheck = False
                reloadCount = 0
                reloadWeapon = None
                requireWeapon = None
                for weaponIndex, weapon in enumerate(reloadList):
                    weapon = copy.deepcopy(weapon)
                    ammoCheck = False
                    targetAmmo = None
                    targetMagazine = None
                    ammoIndex = -1
                    reloadQuantity = 0
                    targetMagazine = None
                    heldMagazineCheck = False

                    # Non-Magazine Weapons #
                    if weapon.shellCapacity != None:
                        targetAmmo, ammoIndex = playerCopy.ammoCheck(weapon.ammoType)
                        if ammoKey != None:
                            targetAmmo, ammoIndex = playerCopy.ammoCheck(weapon.ammoType, ammoKey)
                        elif reloadTargetShiftCheck == True:
                            targetAmmo, ammoIndex = playerCopy.ammoCheck(weapon.ammoType, reloadKey)

                        if weapon.magazine == None or weapon.magazine.quantity < weapon.shellCapacity or (targetAmmo != None and weapon.magazine.num != targetAmmo.num):
                            if ammoIndex != -1 and not (reloadKey == "All" and ammoKey == None and weapon.magazine != None and weapon.magazine.num != targetAmmo.num):
                                if weapon.magazine != None and weapon.magazine.num != targetAmmo.num:
                                    inventoryAmmo, unused = playerCopy.getTargetItem(weapon.magazine.num, ["Inventory"])
                                    if inventoryAmmo != None:
                                        inventoryAmmo.quantity += weapon.magazine.quantity
                                    else:
                                        playerCopy.itemDict["Ammo"].append(weapon.magazine)
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
                        targetMagazine, magazineIndex = playerCopy.ammoCheck(weapon.ammoType, None, True)
                        if magazineIndex != -1:
                            magazineCheck = True
                        else:
                            requireWeapon = weapon
                        if weapon.magazine != None or magazineIndex != -1:
                            targetAmmo, ammoIndex = playerCopy.ammoCheck(weapon.ammoType)
                            if ammoKey != None:
                                targetAmmo, ammoIndex = playerCopy.ammoCheck(weapon.ammoType, ammoKey)
                            elif reloadTargetShiftCheck == True:
                                targetAmmo, ammoIndex = playerCopy.ammoCheck(weapon.ammoType, reloadKey)

                            if ammoIndex != -1 and not (reloadKey == "All" and ammoKey == None and weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and weapon.magazine.flags["Ammo"].num != targetAmmo.num):
                                if weapon.magazine == None or weapon.magazine.flags["Ammo"] == None or weapon.magazine.flags["Ammo"].quantity < weapon.magazine.shellCapacity or weapon.isLoaded(playerCopy.itemDict["Ammo"]) == False or (targetAmmo != None and weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and targetAmmo.num != weapon.magazine.flags["Ammo"].num):
                                    weaponMagazine = weapon.magazine
                                    if weaponMagazine == None:
                                        weaponMagazine = targetMagazine
                                        heldMagazineCheck = True
                                    elif weaponMagazine != None and targetMagazine != None and weaponMagazine.shellCapacity < targetMagazine.shellCapacity:
                                        playerCopy.itemDict["Ammo"].append(weaponMagazine)
                                        if weaponMagazine.flags["Ammo"] != None:
                                            heldAmmo, unused = playerCopy.getTargetItem(weaponMagazine.flags["Ammo"].num, ["Inventory"])
                                            if heldAmmo != None:
                                                heldAmmo.quantity += weaponMagazine.flags["Ammo"].quantity
                                            else:
                                                playerCopy.itemDict["Ammo"].append(weaponMagazine.flags["Ammo"])
                                            weaponMagazine.flags["Ammo"] = None
                                        weaponMagazine = targetMagazine

                                    if weapon.magazine != None and weapon.magazine.flags["Ammo"] != None and weapon.magazine.flags["Ammo"].num != targetAmmo.num:
                                        inventoryAmmo, unused = playerCopy.getTargetItem(weapon.magazine.flags["Ammo"].num, ["Inventory"])
                                        if inventoryAmmo != None:
                                            inventoryAmmo.quantity += weapon.magazine.flags["Ammo"].quantity
                                        else:
                                            playerCopy.itemDict["Ammo"].append(weapon.magazine.flags["Ammo"])
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
                            del playerCopy.itemDict["Ammo"][ammoIndex]
                        else:
                            targetAmmo.quantity -= reloadQuantity
                    if targetMagazine != None and ammoCheck == True and heldMagazineCheck == True:
                        if targetMagazine in playerCopy.itemDict["Ammo"]:
                            magazineIndex = playerCopy.itemDict["Ammo"].index(targetMagazine)
                            del playerCopy.itemDict["Ammo"][magazineIndex] 
                
                if requireWeapon != None and magazineCheck == False and reloadCount == 0 and not (requireWeapon.shellCapacity == None and requireWeapon.magazine != None):
                    displayString = "It requires a " + requireWeapon.ammoType + "."
                    displayCode = "14w" + str(len(requireWeapon.ammoType)) + "w1y"
                    if requireWeapon.shellCapacity == None:
                        displayString = "You don't have a " + requireWeapon.ammoType + " magazine."
                        displayCode = "7w1y9w" + str(len(requireWeapon.ammoType)) + "w9w1y"
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                elif reloadCount == 0 and reloadKey != "All":
                    if ammoKey != None and targetAmmo == None:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You don't have that ammo.", "Code":"7w1y16w1y"})
                    elif ammoKey == None and targetAmmo == None:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You don't have any ammo.", "Code":"7w1y15w1y"})
                    else:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"It's already loaded.", "Code":"2w1y16w1y"})
                elif reloadCount == 0 and reloadKey == "All":
                    if ammoKey != None and targetAmmo == None:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You don't have that ammo.", "Code":"7w1y16w1y"})
                    elif ammoKey == None and targetAmmo == None:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You don't have any ammo.", "Code":"7w1y15w1y"})
                    elif gunInventoryCount == 1:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"It's already loaded.", "Code":"2w1y16w1y"})
                    else:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"Your weapons are already loaded.", "Code":"31w1y"})
                elif reloadCount == 0 and ammoCheck == False:
                    thatString = "any"
                    if ammoKey != None:
                        thatString = "that"
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You don't have " + thatString + " ammo.", "Code":"7w1y7w" + str(len(thatString)) + "w5w1y"})
                elif reloadWeapon == "Multiple":
                    actionFlags = {"Reload List":reloadList, "Reload Key":reloadKey, "Ammo Key":ammoKey, "Reload Target Shift Check":reloadTargetShiftCheck}
                    self.actionList.append(Action("Reload", actionFlags))
                    
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You start reloading some weapons..", "Code":"32w2y"})
                elif reloadWeapon != None:
                    actionFlags = {"Reload List":reloadList, "Reload Key":reloadKey, "Ammo Key":ammoKey, "Reload Target Shift Check":reloadTargetShiftCheck}
                    self.actionList.append(Action("Reload", actionFlags))

                    countString = ""
                    countCode = ""
                    if reloadWeapon != "Multiple" and reloadCount > 1:
                        countString = " (" + str(reloadCount) + ")"
                        countCode = "2r" + str(len(str(reloadCount))) + "w1r"
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You start reloading " + reloadWeapon.prefix.lower() + " " + reloadWeapon.name["String"] + ".." + countString, "Code":"20w" + str(len(reloadWeapon.prefix)) + "w1w" + reloadWeapon.name["Code"] + "2y" + countCode})

    def unloadCheck(self, console, galaxyList, player, currentRoom, unloadKey, unloadSlotKey, ammoKey):
        if currentRoom.isLit(galaxyList, player) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})

        else:
            blankCheck = self.stopActions(console)

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
                    if self.gearDict[unloadSlot].pocket == "Weapon" and self.gearDict[unloadSlot].ranged == True:
                        unloadList.append(self.gearDict[unloadSlot])
                    else:
                        targetItem = self.gearDict[unloadSlot]
            elif unloadKey == "All":
                if self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].pocket == "Weapon" and self.gearDict[self.dominantHand].ranged == True:
                    unloadList.append(self.gearDict[self.dominantHand])
                if self.gearDict[self.getOppositeHand(self.dominantHand)] != None and self.gearDict[self.getOppositeHand(self.dominantHand)].pocket == "Weapon" and self.gearDict[self.getOppositeHand(self.dominantHand)].ranged == True:
                    unloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
                for item in self.itemDict["Weapon"]:
                    if item.ranged == True:
                        unloadList.append(item)
            elif unloadKey == None:
                if self.gearDict[self.dominantHand] != None:
                    if self.gearDict[self.dominantHand].pocket == "Weapon" and self.gearDict[self.dominantHand].ranged == True:
                        unloadList.append(self.gearDict[self.dominantHand])
                if self.gearDict[self.getOppositeHand(self.dominantHand)] != None:
                    if self.gearDict[self.getOppositeHand(self.dominantHand)].pocket == "Weapon" and self.gearDict[self.getOppositeHand(self.dominantHand)].ranged == True:
                        unloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
            else:
                if self.gearDict[self.dominantHand] != None and unloadKey in self.gearDict[self.dominantHand].keyList:
                    if self.gearDict[self.dominantHand].pocket == "Weapon" and self.gearDict[self.dominantHand].ranged == True:
                        unloadList.append(self.gearDict[self.dominantHand])
                    else:
                        targetItem = self.gearDict[self.dominantHand]
                elif self.gearDict[self.getOppositeHand(self.dominantHand)] != None and unloadKey in self.gearDict[self.getOppositeHand(self.dominantHand)].keyList:
                    if self.gearDict[self.getOppositeHand(self.dominantHand)].pocket == "Weapon" and self.gearDict[self.getOppositeHand(self.dominantHand)].ranged == True:
                        unloadList.append(self.gearDict[self.getOppositeHand(self.dominantHand)])
                    else:
                        targetItem = self.gearDict[self.getOppositeHand(self.dominantHand)]
                elif self.getTargetItem(unloadKey, ["Gear"])[0] != None and unloadKey in self.getTargetItem(unloadKey, ["Gear"])[0].keyList:
                    searchItem = self.getTargetItem(unloadKey, ["Gear"])[0]
                    if searchItem.pocket == "Weapon" and searchItem.ranged == True:
                        unloadList.append(searchItem)
                    else:
                        targetItem = searchItem
                elif self.getTargetItem(unloadKey, ["Inventory"])[0] != None:
                    searchItem = self.getTargetItem(unloadKey, ["Inventory"])[0]
                    if searchItem.pocket == "Weapon" and searchItem.ranged == True:
                        unloadList.append(searchItem)
                    else:
                        targetItem = searchItem
                elif currentRoom.getTargetObject(unloadKey, ["Items"]) != None:
                    searchItem = currentRoom.getTargetObject(unloadKey, ["Items"])
                    if searchItem.pocket == "Weapon" and searchItem.ranged == True:
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

            if unloadKey not in ["All", None] and len(unloadList) == 0 and targetItem != None and targetItem.ranged == False:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't unload that.", "Code":"7w1y13w1y"})
            elif alreadyUnloadedCheck == True:
                displayString = "It's already unloaded."
                displayCode = "2w1y18w1y"
                if len(unloadList) > 1:
                    displayString = "Your weapons are already unloaded."
                    displayCode = "33w1y"
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            elif unloadKey == "All" and len(unloadList) == 0:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have anything to unload.", "Code":"7w1y25w1y"})
            elif unloadKey not in ["All", None] and len(unloadList) == 0 and targetItem == None:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
            elif (unloadSlot != None or unloadKey not in ["All", None]) and len(unloadList) == 0 and targetItem != None and not (unloadKey not in ["All", None] and unloadSlotKey == None and ammoKey == None):
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't unload that.", "Code":"7w1y13w1y"})
            elif unloadSlot != None and len(unloadList) == 0 and targetItem == None:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You aren't holding anything.", "Code":"8w1y18w1y"})

            else:
                player = copy.deepcopy(self)
                unloadWeapon = None
                unloadCount = 0
                tooMuchWeightCheck = False
                for weaponIndex, weapon in enumerate(unloadList):
                    weapon = copy.deepcopy(weapon)
                    
                    # Non-Magazine Weapons #
                    if weapon.shellCapacity != None and weapon.magazine != None:
                        if not (ammoKey != None and ammoKey not in weapon.magazine.keyList):
                            getQuantity = weapon.magazine.quantity
                            if roomItem != None and player.getWeight() + roomItem.getWeight() > player.getMaxWeight():
                                getQuantity = 0
                                tooMuchWeightCheck = True
                                if player.getWeight() + roomItem.getWeight(False) <= player.getMaxWeight():
                                    getQuantity = int((player.getMaxWeight() - player.getWeight()) / roomItem.getWeight(False))

                            if getQuantity > 0:
                                inventoryAmmo, unused = player.getTargetItem(weapon.magazine.num, ["Inventory"])
                                if inventoryAmmo != None:
                                    inventoryAmmo.quantity += getQuantity
                                else:
                                    splitItem = copy.deepcopy(weapon.magazine)
                                    splitItem.quantity = getQuantity
                                    player.itemDict["Ammo"].append(splitItem)
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
                            if roomItem != None and weapon.magazine.flags["Ammo"] != None and player.getWeight() + weapon.magazine.flags["Ammo"].getWeight() > player.getMaxWeight():
                                getQuantity = 0
                                tooMuchWeightCheck = True
                                if player.getWeight() + weapon.magazine.flags["Ammo"].getWeight(False) <= player.getMaxWeight():
                                    getQuantity = int((player.getMaxWeight() - player.getWeight()) / weapon.magazine.flags["Ammo"].getWeight(False))

                            if getQuantity > 0:
                                inventoryAmmo, unused = player.getTargetItem(weapon.magazine.flags["Ammo"].num, ["Inventory"])
                                if inventoryAmmo != None:
                                    inventoryAmmo.quantity += getQuantity
                                else:
                                    splitItem = copy.deepcopy(weapon.magazine.flags["Ammo"])
                                    splitItem.quantity = getQuantity
                                    player.itemDict["Ammo"].append(splitItem)
                                if getQuantity == weapon.magazine.flags["Ammo"].quantity:
                                    weapon.magazine.flags["Ammo"] = None
                                else:
                                    weapon.magazine.flags["Ammo"].quantity -= getQuantity

                            magazineCheck = False
                            if roomItem != None and player.getWeight() + weapon.magazine.getWeight() > player.getMaxWeight():
                                tooMuchWeightCheck = True
                            else:
                                player.itemDict["Ammo"].append(weapon.magazine)
                                weapon.magazine = None
                                magazineCheck = True
                            
                            if getQuantity > 0 or magazineCheck == True:
                                if unloadWeapon == None:
                                    unloadWeapon = weapon
                                elif unloadWeapon != "Multiple" and unloadWeapon.num != weapon.num:
                                    unloadWeapon = "Multiple"
                                unloadCount += 1

                if ammoKey != None and unloadCount == 0:
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You can't find that ammo.", "Code":"7w1y16w1y"})
                elif unloadCount == 0 and tooMuchWeightCheck == True:
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You can't carry that much weight.", "Code":"7w1y24w1y"})
                elif unloadKey not in ["All", None] and unloadCount == 0 and len(unloadList) == 0:
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You can't unload that.", "Code":"7w1y13w1y"})
                elif unloadKey not in ["All", None] and unloadCount == 0 and unloadList[0].isEmpty():
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"It's already unloaded.", "Code":"2w1y18w1y"})
                elif unloadKey == "All" and unloadCount == 0 and unloadList[0].isEmpty():
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"Your weapons are already unloaded.", "Code":"33w1y"})
                elif unloadWeapon == "Multiple":
                    actionFlags = {"Unload List":unloadList, "Ammo Key":ammoKey, "Room Item":roomItem}
                    self.actionList.append(Action("Unload", actionFlags))

                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You start unloading some weapons..", "Code":"32w2y"})
                elif unloadWeapon != None:
                    actionFlags = {"Unload List":unloadList, "Ammo Key":ammoKey, "Room Item":roomItem}
                    self.actionList.append(Action("Unload", actionFlags))

                    countString = ""
                    countCode = ""
                    if unloadWeapon != "Multiple" and unloadCount > 1:
                        countString = " (" + str(unloadCount) + ")"
                        countCode = "2r" + str(len(str(unloadCount))) + "w1r"
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You start unloading " + unloadWeapon.prefix.lower() + " " + unloadWeapon.name["String"] + ".." + countString, "Code":"20w" + str(len(unloadWeapon.prefix)) + "w1w" + unloadWeapon.name["Code"] + "2y" + countCode})

    def recruitCheck(self, console, galaxyList, player, currentRoom, mobKey, mobCount):
        if currentRoom.isLit(galaxyList, player) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "It's too dark to see.", "Code":"2w1y17w1y"})
        elif mobKey in ["All", None] and len(currentRoom.mobList) == 0:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "There is no one here.", "Code":"20w1y"})
        elif mobKey == None and len(self.targetList) == 0:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You aren't targeting anyone.", "Code":"8w1y18w1y"})
        
        else:
            blankCheck =self.stopActions(console)

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

            for mob in recruitList:
                if mob in currentRoom.mobList:
                    del currentRoom.mobList[currentRoom.mobList.index(mob)]
                    currentRoom.mobList.append(mob)

            if mobKey not in ["All", None] and len(recruitList) == 0 and alreadyInGroupCheck == False and currentlyFightingCheck == False:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't see them.", "Code":"7w1y10w1y"})
            elif len(recruitList) == 0 and alreadyInGroupCheck == True:
                themString = "everyone here"
                themCode = "13w"
                if mobCount in [1, None]:
                    themString = "them"
                    themCode = "4w"
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You've already recruited " + themString + ".", "Code":"3w1y21w" + themCode + "1y"})
            elif len(recruitList) == 0 and currentlyFightingCheck == True:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't recruit if you're fighting!", "Code":"7w1y16w1y11w1y"})
            elif recruitMob == "Multiple":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You welcome some new members to the group.", "Code":"41w1y"})
            else:
                displayString = "You welcome " + recruitMob.prefix.lower() + " " + recruitMob.name["String"] + " to the group."
                displayCode = "12w" + str(len(recruitMob.prefix)) + "w1w" + recruitMob.name["Code"] + "13w1y"
                countString, countCode = getCountString(len(recruitList))
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString + countString, "Code":displayCode + countCode})

    def disbandCheck(self, console, galaxyList, player, currentRoom, mobKey, mobCount):
        pass

    def stopCheck(self, console):
        if len(self.actionList) == 0:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You aren't doing anything.", "Code":"8w1y16w1y"})
        else:
            self.stopActions(console)
           
    def wearCheck(self, console, targetItemKey, count, targetGearSlotIndex=None):
        blankCheck = self.stopActions(console)

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
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't wear that.", "Code":"7w1y11w1y"})
        elif targetItemKey != "All" and wearItem == None:
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
        elif targetItemKey != "All" and wearItem.pocket == "Weapon":
            tempCount = count
            if tempCount == "All":
                tempCount = 2
            self.wieldCheck(console, targetItemKey, targetGearSlotIndex, tempCount)
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
                                    elif wearItem.num != item.num:
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
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have any gear to wear.", "Code":"7w1y23w1y"})    
            elif wearCount == 0:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You are already wearing something.", "Code":"33w1y"})    
            elif len(previousWornItemList) > 0 and wearCount > 1:
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You switch around some of your gear.", "Code":"35w1y"})
            elif len(previousWornItemList) == 0 and wearCount > 1 and wearItem == "Multiple":
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You put on some armor.", "Code":"21w1y"})
            elif len(previousWornItemList) == 1 and isinstance(wearItem, Item):
                wearString = "You remove " + previousWornItemList[0].prefix.lower() + " " + previousWornItemList[0].name["String"] + " and wear " + wearItem.prefix.lower() + " " + wearItem.name["String"] + "."
                wearCode = "11w" + str(len(previousWornItemList[0].prefix)) + "w1w" + previousWornItemList[0].name["Code"] + "10w" + str(len(wearItem.prefix)) + "w1w" + wearItem.name["Code"] + "1y"
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":wearString, "Code":wearCode})
            elif len(previousWornItemList) == 0 and isinstance(wearItem, Item):
                wearString = "You wear " + wearItem.prefix.lower() + " " + wearItem.name["String"] + " on your " + wearItem.gearSlot.lower() + "."
                wearCode = "9w" + str(len(wearItem.prefix)) + "w1w" + wearItem.name["Code"] + "9w" + str(len(wearItem.gearSlot)) + "w1y"
                countString = ""
                countCode = ""
                if wearItem != "Multiple" and wearCount > 1:
                    countString = " (" + str(wearCount) + ")"
                    countCode = "2r" + str(len(str(wearCount))) + "w1r"
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":wearString + countString, "Code":wearCode + countCode})

            # Wield Check #
            if targetItemKey == "All" and count == "All":
                self.wieldCheck(console, "All", None, 2, False)

    def wieldCheck(self, console, targetItemKey, targetGearSlotKey, count, blankCheck=True):
        actionBlankCheck = self.stopActions(console)

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
                if actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have anything to wield.", "Code":"7w1y24w1y"})
        elif wieldItem == None and checkItem != None and checkItem.pocket != "Weapon":
            if blankCheck == True and actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't wield that.", "Code":"7w1y12w1y"})
        elif wieldItem == None:
            if blankCheck == True and actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
        elif wieldItem.pocket != "Weapon":
            if blankCheck == True and actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't wield that.", "Code":"7w1y12w1y"})

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
                if wieldItem != None and wieldItem.twoHanded and (self.debugDualWield == False or wieldItem.ranged == True):
                    targetGearSlot = self.dominantHand

            wieldCount = 0
            slotCount = 0
            slotItem = None
            breakCheck = False
            for c in range(count):
                defaultGearSlot = self.dominantHand
                if (targetItemKey == "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[defaultGearSlot].twoHanded == False and (self.debugDualWield == False or self.gearDict[defaultGearSlot].ranged == True)) or \
                (targetItemKey != "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[self.getOppositeHand(defaultGearSlot)] == None and self.gearDict[defaultGearSlot].twoHanded == False and wieldItem.twoHanded == False and count == 1) or \
                (c == 1 and not (self.gearDict[defaultGearSlot] != None and self.gearDict[defaultGearSlot].twoHanded == True and (self.debugDualWield == False or self.gearDict[defaultGearSlot].ranged == True))) or \
                (targetItemKey != "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[self.getOppositeHand(defaultGearSlot)] == None and wieldItem.twoHanded == True and wieldItem.ranged == False and self.debugDualWield == True and self.gearDict[defaultGearSlot].ranged == False):
                    defaultGearSlot = self.getOppositeHand(self.dominantHand)
                if targetGearSlot != None:
                    defaultGearSlot = targetGearSlot
                delIndex = -1
                for i, item in enumerate(self.itemDict["Weapon"]):
                    if targetItemKey == "All" or targetItemKey in item.keyList:
                        if not (targetItemKey == "All" and self.gearDict[defaultGearSlot] != None) and \
                        not (targetItemKey == "All" and item.twoHanded == True and (self.gearDict[self.dominantHand] != None or self.gearDict[self.getOppositeHand(self.dominantHand)] != None) and (self.debugDualWield == False or item.ranged == True)):
                            if self.gearDict[defaultGearSlot] != None:
                                self.itemDict[self.gearDict[defaultGearSlot].pocket].append(self.gearDict[defaultGearSlot])
                                slotCount += 1
                                if slotItem == None:
                                    slotItem = self.gearDict[defaultGearSlot]
                                elif slotItem != "Multiple" and slotItem.num != self.gearDict[defaultGearSlot].num:
                                    slotItem = "Multiple"
                            oppositeHand = self.gearDict[self.getOppositeHand(defaultGearSlot)]
                            if oppositeHand != None and (item.twoHanded == True or oppositeHand.twoHanded == True) and (self.debugDualWield == False or ((item.twoHanded == True and item.ranged == True) or (oppositeHand.twoHanded == True and oppositeHand.ranged == True))):
                                self.itemDict[oppositeHand.pocket].append(oppositeHand)
                                self.gearDict[self.getOppositeHand(defaultGearSlot)] = None
                                slotCount += 1
                                if slotItem == None:
                                    slotItem = oppositeHand
                                elif slotItem != "Multiple" and slotItem.num != oppositeHand.num:
                                    slotItem = "Multiple"
                            self.gearDict[defaultGearSlot] = item
                            wieldCount += 1
                            if wieldItem == None:
                                wieldItem = item
                            elif wieldItem != "Multiple" and wieldItem.num != item.num:
                                wieldItem = "Multiple"
                            delIndex = i
                            break
                if delIndex != -1:
                    if self.itemDict["Weapon"][delIndex].twoHanded == True and (self.debugDualWield == False or self.itemDict["Weapon"][delIndex].ranged == True):
                        breakCheck = True
                    del self.itemDict["Weapon"][delIndex]
                if breakCheck:
                    break

            if wieldCount == 0:
                if blankCheck == True:
                    if actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You're already holding something.", "Code":"3w1y28w1y"})
            elif wieldItem == "Multiple":
                if slotItem == None:
                    if blankCheck == True and actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You hold some weapons in your hands.", "Code":"35w1y"})
                else:
                    if blankCheck == True and actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You switch some weapons around.", "Code":"30w1y"})
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
                if blankCheck == True and actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
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
                if blankCheck == True and actionBlankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                           
    def removeCheck(self, console, targetItemKey, count, targetGearSlotIndex=None):
        blankCheck = self.stopActions(console)

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
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

        else:
            removeCount = 0
            breakCheck = False
            removeItem = None
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
                    slotIndex = -1
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
                                elif removeItem.num != targetGearSlot.num:
                                    removeItem = "Multiple"
                            if slotIndex != -1:
                                self.gearDict[gearSlot][slotIndex] = None
                            else:
                                self.gearDict[gearSlot] = None

                            if count != "All" and removeCount >= count:
                                breakCheck = True
                                break
                if breakCheck:
                    break

            # Messages #
            if removeCount == 0:
                displayMessage = "You have nothing to remove."
                displayCode = "26w1y"
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayMessage, "Code":displayCode})
            elif targetItemKey == "All" and count == "All":
                displayString = "You remove all of your gear."
                displayCode = "27w1y"
                if random.randrange(10) == 0:
                    displayString = "You strip down to your birthday suit."
                    displayCode = "36w1y"
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            elif removeItem == "Multiple":
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You remove some gear.", "Code":"20w1y"})
            elif isinstance(removeItem, Item):
                countString, countCode = getCountString(removeCount)
                holdingString = " remove"
                if removeItem.pocket == "Weapon":
                    holdingString = " stop wielding"
                handString = ""
                if gearSlot in ["Left Hand", "Right Hand"]:
                    handString = " in your " + gearSlot.lower()
                displayString = "You" + holdingString + " " + removeItem.prefix + " " + removeItem.name["String"] + handString + "." + countString
                displayCode = "3w" + str(len(holdingString)) + "w1w" + str(len(removeItem.prefix)) + "w1w" + removeItem.name["Code"] + str(len(handString)) + "w1y" + countCode
                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})

    def attackCheck(self, console, galaxyList, currentRoom, mobKey):
        if mobKey == None and len(self.targetList) == 0:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"Attack who?", "Code":"10w1y"})
        
        else:
            distance = 0
            directionKey = None
            directionCount = None
            if len(self.targetList) > 0:
                targetDistance, targetDirection, unused = Room.getTargetRange(galaxyList, currentRoom, self.targetList[0], self.maxTargetDistance)
                if targetDistance != -1:
                    distance = targetDistance
                    if mobKey == None and targetDistance > 0:
                        directionKey = targetDirection.lower()
                        directionCount = targetDistance

            randomCombatSkill = self.getRandomAttackSkill(self.gearDict[self.dominantHand], self.gearDict[self.getOppositeHand(self.dominantHand)], {"Distance":distance})

            if randomCombatSkill == None:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't attack from here!", "Code":"7w1y18w1y"})
            elif randomCombatSkill == "Reload":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You need to reload first.", "Code":"24w1y"})

            elif isinstance(randomCombatSkill, Skill):
                self.combatSkillCheck(console, galaxyList, currentRoom, randomCombatSkill, 1, mobKey, directionKey, directionCount)

    def combatSkillCheck(self, console, galaxyList, currentRoom, combatSkill, mobCount, mobKey, directionKey, directionCount):
        if self.skillAvailableCheck(combatSkill) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You can't use that now.", "Code":"7w1y14w1y"})
        elif mobKey == None and directionKey == None and len(self.targetList) == 0 and "All Only" not in combatSkill.ruleDict and combatSkill.healCheck == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You aren't targeting anyone.", "Code":"8w1y18w1y"})
        elif (directionCount != None and directionCount > combatSkill.maxRange) or (mobKey == None and len(self.targetList) > 0 and Room.getTargetRange(galaxyList, currentRoom, self.targetList[0], combatSkill.maxRange)[0] == -1):
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "That's too far.", "Code":"4w1y9w1y"})
        elif mobKey == None and "From Another Room" in combatSkill.ruleDict and Room.getTargetRange(galaxyList, currentRoom, self.targetList[0], combatSkill.maxRange)[0] == 0:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You're too close!", "Code":"3w1y12w1y"})
        elif mobKey == "Self" and combatSkill.healCheck == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You can't use it on yourself.", "Code":"7w1y20w1y"})
        
        else:
            message = None
            roomDistance = 0
            targetRoom = currentRoom
            if mobKey == None and len(self.targetList) > 0:
                targetArea, targetRoom = Room.getAreaAndRoom(galaxyList, self.targetList[0])
                roomDistance, targetDirection, message = Room.getTargetRange(galaxyList, currentRoom, self.targetList[0], self.maxTargetDistance)
            elif directionCount != None:
                if directionKey[0] == "n" : targetDirection = "North"
                elif directionKey[0] == "e" : targetDirection = "East"
                elif directionKey[0] == "s" : targetDirection = "South"
                else : targetDirection = "West"
                targetArea, targetRoom = Room.getAreaAndRoom(galaxyList, targetRoom)
                targetArea, targetRoom, roomDistance, message = Room.getTargetRoomFromStartRoom(galaxyList, targetArea, targetRoom, targetDirection, directionCount, True)

            if message == "No Exit":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "There is nothing there.", "Code":"22w1y"})
            elif message == "Door Is Closed":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The door is closed.", "Code":"18w1y"})
            
            else:
                blankCheck = self.stopActions(console)

                attackList = []
                mainAttackHand = self.gearDict[self.dominantHand]
                offAttackHand = self.gearDict[self.getOppositeHand(self.dominantHand)]
                combatSkill.weaponDataList = []
                if combatSkill.weaponAttackCheck(mainAttackHand, offAttackHand) == True:
                    attackList.append(combatSkill)
                    if len(combatSkill.weaponDataList) == 1 and (combatSkill.weaponDataList[0] == offAttackHand or (combatSkill.weaponDataList[0] == "Open Hand" and offAttackHand == None)):
                        offAttackHand = self.gearDict[self.dominantHand]
                if combatSkill.offHandAttacks == True and len(combatSkill.weaponTypeList) != 2 and combatSkill.healCheck == False:
                    offAttackSkill = copy.deepcopy(self.getRandomAttackSkill(offAttackHand, None, {"Distance":roomDistance, '"All" Attacks Disabled':True, "Disable Two-Handed Attacks":True, "Disable Healing":True}))
                    if isinstance(offAttackSkill, Skill) and offAttackSkill.weaponAttackCheck(offAttackHand) == True:
                        attackList.append(offAttackSkill)

                allOnlyCheck = False
                for attackSkill in attackList:
                    if "All Only" in attackSkill.ruleDict:
                        allOnlyCheck = True
                
                if mobCount in ["All", "Group", None] or allOnlyCheck == True : maxTargets = len(targetRoom.mobList)
                else : maxTargets = mobCount
                if combatSkill.maxTargets != "All" and maxTargets > combatSkill.maxTargets:
                    maxTargets = combatSkill.maxTargets
                
                selfSkill = None
                if combatSkill.healCheck == True and \
                (allOnlyCheck == True \
                or \
                ((mobKey == "Self" or \
                (mobKey == None and mobCount == None and (len(self.targetList) == 0 or self.healEnemies == False)) or \
                (mobKey == "All" and directionKey == None)))):
                    selfSkill = True

                attackDisplayList = []
                targetMobList = []
                targetMob = None
                mobKillList = []
                if not ((mobKey == "Self" and allOnlyCheck == False) or (combatSkill.healCheck == True and mobKey == None and mobCount == None and len(self.targetList) > 0 and self.healEnemies == False and allOnlyCheck == False)):
                    for i in range(len(attackList)):
                        attackDisplayList.append({"Mob Data":None, "Killed Mob Data":None, "Count":0, "Kill Count":0, "Miss Count":0, "Attack Data":attackList[i]})
                    if maxTargets > 0 and not (combatSkill.healCheck == True and mobKey == "Self" and allOnlyCheck == False):
                        for mob in targetRoom.mobList:
                            if mobKey == "All" or allOnlyCheck == True or \
                            (mobKey != None and mobKey in mob.keyList) or \
                            (mobKey == None and mob in self.targetList):
                                if allOnlyCheck == True or \
                                (not (self.healEnemies == False and combatSkill.healCheck == True and mob not in self.recruitList) and \
                                not (self.teamDamage == False and combatSkill.healCheck == False and mob in self.recruitList)):
                                    if allOnlyCheck == True or not (mobCount == "Group" and mob not in self.recruitList):
                                        for i, attackSkill in enumerate(attackList):
                                            hitCheck = False
                                            if len(attackSkill.weaponDataList) in [0, 2]:
                                                attackHitCheck, attackHitData = Combat.hitCheck(self, attackSkill, mob)
                                                if attackHitCheck == False:
                                                    attackDisplayList[i].update(attackHitData)
                                                else:
                                                    hitCheck = True
                                            else:
                                                for weapon in attackSkill.weaponDataList:
                                                    if weapon != "Open Hand" and weapon.weaponType == "Gun" and weapon.isLoaded(1) == False:
                                                        attackDisplayList[i]["Miss Check"] = "Out Of Ammo"
                                                        attackDisplayList[i]["Weapon Data List"] = [attackSkill.weaponDataList[0]]
                                                    else:
                                                        attackHitCheck, attackHitData = Combat.hitCheck(self, attackSkill, mob)
                                                        if attackHitCheck == False:
                                                            attackDisplayList[i].update(attackHitData)
                                                        else:
                                                            hitCheck = True

                                                        if weapon != "Open Hand" and weapon.weaponType == "Gun" and weapon.isLoaded(1) == True:
                                                            weapon.shoot()
                                                    
                                            if attackDisplayList[i]["Mob Data"] == None:
                                                attackDisplayList[i]["Mob Data"] = mob
                                            elif attackDisplayList[i]["Mob Data"] != "Multiple" and attackDisplayList[i]["Mob Data"].num != mob.num:
                                                attackDisplayList[i]["Mob Data"] = "Multiple"
                                            if hitCheck == True:
                                                attackDisplayList[i]["Count"] += 1
                                            else:
                                                attackDisplayList[i]["Miss Count"] += 1

                                        targetMobList.append(mob)

                                        if mob.currentHealth <= 0:
                                            mobKillList.append(mob)
                                            attackDisplayList[0]["Kill Count"] += 1
                                            targetRoom.itemList.append(Item.createCorpse(mob))
                                            if mob in self.targetList : del self.targetList[self.targetList.index(mob)]
                                            if mob in self.recruitList : del self.recruitList[self.recruitList.index(mob)]
                                            if attackDisplayList[0]["Killed Mob Data"] == None:
                                                attackDisplayList[0]["Killed Mob Data"] = mob
                                            elif attackDisplayList[0]["Killed Mob Data"] != "Multiple" and attackDisplayList[0]["Killed Mob Data"].num != mob.num:
                                                attackDisplayList[0]["Killed Mob Data"] = "Multiple"
                                        elif mob.currentHealth > 0 and combatSkill.healCheck == False and mob not in self.targetList and mob not in self.recruitList:
                                            self.targetList.insert(0, mob)
                                            if mob not in self.combatList : self.combatList.append(mob)

                                        if targetMob == None:
                                            targetMob = mob
                                        elif targetMob != "Multiple" and targetMob.num != mob.num:
                                            targetMob = "Multiple"
                                        if allOnlyCheck != True and len(targetMobList) >= maxTargets:
                                            break
                    
                for mob in mobKillList:
                    if mob in targetRoom.mobList:
                        del targetRoom.mobList[targetRoom.mobList.index(mob)]

                if targetMob == None and "All Only" in combatSkill.ruleDict and selfSkill == None:
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String": "Your " + combatSkill.name["String"] + " doesn't hit anyone.", "Code":"5w" + combatSkill.name["Code"] + "6w1y12w1y"})
                elif len(targetMobList) == 0 and mobKey not in ["All", None, "Self"]:
                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String": "You don't see them.", "Code":"7w1y10w1y"})
                elif len(targetMobList) == 0 and mobKey == "All" and selfSkill == None:
                    if directionKey != None:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String": "You don't see anyone there.", "Code":"7w1y18w1y"})
                    else:
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String": "You don't see anyone.", "Code":"7w1y12w1y"})
                else:
                    if selfSkill != None:
                        displayString = "You heal yourself with " + combatSkill.name["String"] + "."
                        displayCode = "23w" + combatSkill.name["Code"] + "1y"
                        if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                        blankCheck = True

                    if len(targetMobList) > 0:
                        directionString = ""
                        directionCode = ""
                        directionCountString = ""
                        directionCountCode = ""
                        if roomDistance > 0:
                            directionString = " to the " + targetDirection
                            directionCode = "8w" + str(len(targetDirection)) + "w"
                            directionCountString, directionCountCode = getCountString(roomDistance)
                            
                        for attackData in attackDisplayList:
                            if "Miss Check" in attackData:
                                if attackData["Miss Check"] == "Out Of Ammo":
                                    gunString = attackData["Weapon Data List"][0].name["String"]
                                    gunCode = attackData["Weapon Data List"][0].name["Code"]
                                    displayString = "Your " + gunString + " *CLICKS* due to having no ammo."
                                    displayCode = "5w" + gunCode + "2y6w1y22w1y"
                                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                                    console.lineList.insert(0, {"String": displayString, "Code":displayCode})
                                    blankCheck = True
                                elif attackData["Miss Check"] == "Miss Attack" and not (attackData["Mob Data"] == "Multiple" and attackData["Count"] > 0):
                                    countString = ""
                                    countCode = ""
                                    mobString = "the group"
                                    mobCode = "9w"
                                    if attackData["Mob Data"] != "Multiple":
                                        countString, countCode = getCountString(attackData["Miss Count"])
                                        mobString = attackData["Mob Data"].prefix + " " + attackData["Mob Data"].name["String"]
                                        mobCode = str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"]
                                    displayString = "Your " + attackData["Attack Data"].name["String"] + directionString + directionCountString + " misses " + mobString + "." + countString
                                    displayCode = "5w" + attackData["Attack Data"].name["Code"] + directionCode + directionCountCode + "8w" + mobCode + "1y" + countCode
                                    if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                                    console.lineList.insert(0, {"String": displayString, "Code":displayCode})
                                    blankCheck = True

                            if attackData["Count"] > 0:
                                hitString = " hits"
                                hitCode = "5w"
                                if blankCheck == False : console.lineList.insert(0, {"Blank": True})
                                blankCheck = True
                                if attackData["Attack Data"].healCheck == True:
                                    hitString = " heals"
                                    hitCode = "6w"

                                if attackData["Mob Data"] == "Multiple":
                                    displayString = "Your " + attackData["Attack Data"].name["String"] + directionString + directionCountString + hitString + " the group!"
                                    displayCode = "5w" + attackData["Attack Data"].name["Code"] + directionCode + directionCountCode + hitCode + "10w1y"
                                    console.lineList.insert(0, {"String": displayString, "Code":displayCode})
                                elif attackData["Mob Data"] != None:
                                    countString, countCode = getCountString(attackData["Count"])
                                    displayString = "Your " + attackData["Attack Data"].name["String"] + directionString + directionCountString + hitString + " " + attackData["Mob Data"].prefix.lower() + " " + attackData["Mob Data"].name["String"] + "!"
                                    displayCode = "5w" + attackData["Attack Data"].name["Code"] + directionCode + directionCountCode + hitCode + "1w" + str(len(attackData["Mob Data"].prefix)) + "w1w" + attackData["Mob Data"].name["Code"] + "1y"
                                    console.lineList.insert(0, {"String": displayString + countString, "Code":displayCode + countCode})
                        
                        if attackDisplayList[0]["Kill Count"] > 0:
                            countString, countCode = getCountString(attackData["Kill Count"])
                            if attackData["Killed Mob Data"] == "Multiple":
                                displayString = "Your attack kills your targets!"
                                displayCode = "30w1y"
                                console.lineList.insert(0, {"String": displayString + countString, "Code":displayCode + countCode})
                            else:
                                displayString = attackDisplayList[0]["Killed Mob Data"].prefix + " " + attackDisplayList[0]["Killed Mob Data"].name["String"] + " is DEAD!"
                                displayCode = str(len(attackDisplayList[0]["Killed Mob Data"].prefix)) + "w1w" + attackDisplayList[0]["Killed Mob Data"].name["Code"] + "8w1y"
                                console.lineList.insert(0, {"String": displayString + countString, "Code":displayCode + countCode})

    def displayInventory(self, console, galaxyList, currentRoom, targetPocketKey):
        targetPocket = None
        if targetPocketKey in ["gear", "gea", "ge", "g"]:
            targetPocket = "Armor"
        elif targetPocketKey in ["weapons", "weapon", "weapo", "weap", "wea", "we", "w"]:
            targetPocket = "Weapon"
        elif targetPocketKey in ["ammo", "amm", "am", "a"]:
            targetPocket = "Ammo"
        elif targetPocketKey in ["misc.", "misc", "mis", "mi", "m"]:
            targetPocket = "Misc"

        if targetPocket not in self.itemDict:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"Open which bag? (Gear, Weapon, Ammo, Misc.)", "Code":"14w2y1r4w2y6w2y4w2y4w1y1r"})

        else:
            displayList = []
            for item in self.itemDict[targetPocket]:
                if item.ranged == True:
                    displayList.append({"ItemData":item})
                else:
                    displayData = None
                    for data in displayList:
                        if "Num" in data and data["Num"] == item.num:
                            if item.num != Item.getSpecialItemNum("Corpse") or item.name["String"] == data["ItemData"].name["String"]:
                                displayData = data
                                break
                    if displayData == None:
                        itemCount = 1
                        if item.quantity != None:
                            itemCount = item.quantity
                        displayList.append({"Num":item.num, "Count":itemCount, "ItemData":item})
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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": targetPocketDisplayString + " Bag", "Code": targetPocketDisplayCode + "4w"})
            console.lineList.insert(0, {"String": underlineString, "Code": underlineCode})

            if len(self.itemDict[targetPocket]) == 0:
                console.lineList.insert(0, {"String": "-Empty", "Code": "1y5w"})
            elif currentRoom.isLit(galaxyList, self) == False and self.lightInBagCheck(targetPocket) == False:
                inventoryCount = 0
                for displayItemData in displayList:
                    if "Count" in displayItemData:
                        inventoryCount += displayItemData["Count"]
                    else:
                        inventoryCount += 1
                countString, countCode = getCountString(inventoryCount)
                console.lineList.insert(0, {"String": "-Something" + countString, "Code": "1y9w" + countCode})
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
                    weaponStatusString, weaponStatusCode = item.getWeaponStatusString()
                    console.lineList.insert(0, {"String":itemDisplayString + weaponStatusString + countString + modString, "Code":itemDisplayCode + weaponStatusCode + countCode + modCode})

    def displaySkills(self, console):
        console.lineList.insert(0, {"Blank": True})
        console.lineList.insert(0, {"String":"Skill List:", "Code":"10w1y"})
        console.lineList.insert(0, {"String":"--=======--", "Code":"1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1y"})

        columnWidth = 25
        displayString = ""
        displayCode = ""
        displayedList = []
        for i, skill in enumerate(self.getCombatSkillList()):
            if skill.name["String"] not in displayedList:
                displayString += skill.name["String"]
                if self.skillAvailableCheck(skill):
                    displayCode += str(len(skill.name["String"])) + "w"
                else:
                    displayCode += str(len(skill.name["String"])) + "dda"
                if i % 2 == 0:
                    for ii in range(columnWidth - len(skill.name["String"])):
                        displayString += " "
                        displayCode += "1w"
                if i % 2 == 1 or i == len(self.getCombatSkillList()) - 1:
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                    displayString = ""
                    displayCode = ""
                displayedList.append(skill.name["String"])

    def displayGear(self, console, galaxyList, currentRoom):
        gearSlotDisplayDict = {"Body Under":{"String":"(Under) Body", "Code":"1r5w2r4w"}, "Body Over":{"String":"(Over) Body", "Code":"1r4w2r4w"}, "Legs Under":{"String":"(Under) Legs", "Code":"1r5w2r4w"}, "Legs Over":{"String":"(Over) Legs", "Code":"1r4w2r4w"}, "Left Hand":{"String":"L-Hand", "Code":"1w1y4w"}, "Right Hand":{"String":"R-Hand", "Code":"1w1y4w"}}

        console.lineList.insert(0, {"Blank": True})
        console.lineList.insert(0, {"String":"Worn Gear", "Code":"1w4ddw1w3ddw"})
        console.lineList.insert(0, {"String":"--=====--", "Code":"1y1dy1y1dy1y1dy1y1dy1y"})
        for gearSlot in self.gearDict:
            gearSlotString = gearSlot
            if gearSlot in gearSlotDisplayDict and "String" in gearSlotDisplayDict[gearSlot]:
                gearSlotString = gearSlotDisplayDict[gearSlot]["String"]
            gearSlotCode = str(len(gearSlotString)) + "w"
            if gearSlot in gearSlotDisplayDict and "Code" in gearSlotDisplayDict[gearSlot]:
                gearSlotCode = gearSlotDisplayDict[gearSlot]["Code"]
            
            if gearSlotString in ["L-Hand", "R-Hand"]:
                if self.dominantHand[0] == gearSlotString[0]:
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
                weaponStatusString = ""
                weaponStatusCode = ""
                modString = ""
                modCode = ""
                
                if isinstance(self.gearDict[gearSlot], list):
                    targetSlot = self.gearDict[gearSlot][slotIndex]
                else:
                    targetSlot = self.gearDict[gearSlot]
                if targetSlot == None:
                    if self.debugDualWield == False and gearSlot == self.getOppositeHand(self.dominantHand) and self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].twoHanded == True:
                        gearString = "[Two-Handed]"
                        gearCode = "1r3ddw1y6ddw1r"
                else:
                    if "Glowing" in targetSlot.flags and targetSlot.flags["Glowing"] == True:
                        modString = " (Glowing)"
                        modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                    if currentRoom.isLit(galaxyList, self) == False:
                        gearString = "(Something)"
                        gearCode = "1r1w8wwd1r"
                    else:
                        gearString = targetSlot.name["String"]
                        gearCode = str(len(gearString)) + "w"
                        if "Code" in targetSlot.name:
                            gearCode = targetSlot.name["Code"]
                    weaponStatusString, weaponStatusCode = targetSlot.getWeaponStatusString()
                console.lineList.insert(0, {"String":gearSlotString + ": " + gearString + weaponStatusString + modString, "Code":gearSlotCode + "2y" + gearCode + weaponStatusCode + modCode})

    def displayStatus(self, console):
        console.lineList.insert(0, {"Blank": True})
        console.lineList.insert(0, {"String":"Character Status", "Code":"1w9ddw1w5ddw"})
        console.lineList.insert(0, {"String":"---==========---", "Code":"1y1dy1y1dy1y1dy1y1dy1y1ddy1y1ddy1y1ddy1y1ddy1y1ddy1r"})

        autoLootString  = "[ ]"
        if self.autoLoot == True:
            autoLootString = "[X]"
        console.lineList.insert(0, {"String":autoLootString + " - Auto Loot", "Code":"1y1dr1y3y9w"})

        autoReloadString  = "[ ]"
        if self.autoReload == True:
            autoReloadString = "[X]"
        console.lineList.insert(0, {"String":autoReloadString + " - Auto Reload", "Code":"1y1dr1y3y11w"})
        
        teamDamageString  = "[ ]"
        if self.teamDamage == True:
            teamDamageString = "[X]"
        console.lineList.insert(0, {"String":teamDamageString + " - Team Damage", "Code":"1y1dr1y3y11w"})
        
        healEnemiesString  = "[ ]"
        if self.healEnemies == True:
            healEnemiesString = "[X]"
        console.lineList.insert(0, {"String":healEnemiesString + " - Heal Enemies", "Code":"1y1dr1y3y12w"})
        
    def boardCheck(self, console, map, galaxyList, currentRoom, targetSpaceshipKey):
        blankCheck = self.stopActions(console)

        targetSpaceship = None
        for spaceship in currentRoom.spaceshipList:
            if targetSpaceshipKey in spaceship.keyList:
                targetSpaceship = spaceship
                break

        if self.spaceship != None:
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You are already inside.", "Code":"22w1y"})
        elif targetSpaceship == None:
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You don't see anything like that.", "Code":"7w1y24w1y"})
        elif targetSpaceship.hatchPassword != None and self.hasKey(targetSpaceship.hatchPassword) == False:
            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You lack the proper key.", "Code":"23w1y"})
        
        else:
            self.spaceship = targetSpaceship.num
            self.area = targetSpaceship.hatchLocation[0]
            self.room = targetSpaceship.hatchLocation[1]

            if blankCheck == False : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"The hatch opens and closes as you step inside.", "Code":"45w1y"})
            console.lineList.insert(0, {"Blank": True})

            spaceshipHatchRoom = targetSpaceship.areaList[self.area].roomList[self.room]
            spaceshipHatchRoom.display(console, galaxyList, self)

            map.loadMap(targetSpaceship.areaList[self.area])

    def manifestCheck(self, console, currentRoom, targetType, targetNum, targetCount):
        manifestTarget = None
        if currentRoom.spaceshipObject != None:
            targetGalaxy = currentRoom.spaceshipObject.galaxy
            targetSystem = currentRoom.spaceshipObject.system
            targetPlanet = currentRoom.spaceshipObject.planet
            targetArea = currentRoom.area
            targetRoom = currentRoom.room
            targetSpaceship = currentRoom.spaceshipObject.num
        else:
            targetGalaxy = currentRoom.galaxy
            targetSystem = currentRoom.system
            targetPlanet = currentRoom.planet
            targetArea = currentRoom.area
            targetRoom = currentRoom.room
            targetSpaceship = None

        for i in range(targetCount):
            if targetType == "Mob":
                newMob = Player(targetGalaxy, targetSystem, targetPlanet, targetArea, targetRoom, targetSpaceship, targetNum)
                currentRoom.mobList.append(newMob)
                if manifestTarget == None:
                    manifestTarget = newMob

        if manifestTarget == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You wave your hand and nothing happens.", "Code":"38w1y"})
        else:
            countString, countCode = getCountString(targetCount)
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You wave your hand and " + manifestTarget.prefix.lower() + " " + manifestTarget.name["String"] + " appears." + countString, "Code":"23w" + str(len(manifestTarget.prefix)) + "w1w" + manifestTarget.name["Code"] + "8w1y" + countCode})

    # Utility Functions #
    def getTargetItem(self, targetItemKey, includeList=["Inventory", "Gear"]):
        if "Inventory" in includeList:
            for pocket in self.itemDict:
                for item in self.itemDict[pocket]:
                    if (isinstance(targetItemKey, str) and targetItemKey in item.keyList) or \
                    (isinstance(targetItemKey, int) and targetItemKey == item.num):
                        return item, "Inventory"
        if "Gear" in includeList:
            for gearSlot in self.gearDict:
                if isinstance(self.gearDict[gearSlot], list) == False:
                    if self.gearDict[gearSlot] != None:
                        if (isinstance(targetItemKey, str) and targetItemKey in self.gearDict[gearSlot].keyList) or \
                        (isinstance(targetItemKey, int) and targetItemKey == self.gearDict[gearSlot].num):
                            return self.gearDict[gearSlot], "Gear"
                else:
                    for gearSubSlot in self.gearDict[gearSlot]:
                        if gearSubSlot != None:
                            if (isinstance(targetItemKey, str) and targetItemKey in gearSubSlot.keyList) or \
                            (isinstance(targetItemKey, int) and targetItemKey == gearSubSlot.num):
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

    def ammoCheck(self, ammoType, ammoKey=None, magazineCheck=False):
        returnItem = None
        returnIndex = -1
        magSize = 0
        magazineIndex = -1
        for i, item in enumerate(self.itemDict["Ammo"]):
            if item.ammoType == ammoType and not (ammoKey != None and ammoKey not in item.keyList):
                if magazineCheck == False and item.shellCapacity == None:
                    return item, i
                elif magazineCheck == True and item.shellCapacity != None:
                    if item.shellCapacity > magSize:
                        returnItem = item
                        magSize = item.shellCapacity
                        magazineIndex = i
        if magazineIndex != -1:
            returnIndex = magazineIndex
        return returnItem, returnIndex

    def getCombatSkillList(self):
        # Gets An Entire List Of Skills (No Rules) #

        skillList = []
        for skill in self.combatSkillList:
            skillList.append(skill)
        for gearSlot in self.gearDict:
            if isinstance(self.gearDict[gearSlot], list):
                gearList = self.gearDict[gearSlot]
            else:
                gearList = [self.gearDict[gearSlot]]
            for gear in gearList:
                if gear != None:
                    for skill in gear.skillList:
                        skillList.append(skill)
        return skillList

    def getRandomAttackSkill(self, targetWeapon, secondWeapon, ruleCheckFlags):
        # Don't Choose Attacks That Don't Require Weapons #
        # Ammo Check #

        skillList = []
        returnMessage = None
        for skill in self.getCombatSkillList():
            if skill.ruleCheck(ruleCheckFlags) == True:
                if self.skillAvailableCheck(skill, targetWeapon) == True:
                    if len(skill.weaponTypeList) == 0:
                        pass
                    elif skill.weaponTypeList[0] == "Gun" and ((targetWeapon != None and targetWeapon.weaponType == "Gun" and targetWeapon.isEmpty(True) == True) and (secondWeapon == None or (secondWeapon != None and secondWeapon.weaponType == "Gun" and secondWeapon.isEmpty(True) == True))):
                        returnMessage = "Reload"
                    else:
                        skillList.append(skill)
                    
        if len(skillList) > 0:
            return random.choice(skillList)
        return returnMessage

    def skillAvailableCheck(self, combatSkill, targetWeapon="Unused"):
        # Weapon Checks & Gear Skill Check #

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
        elif len(combatSkill.weaponTypeList) == 1 and combatSkill.weaponTypeList == ["Open Hand"]:
            if not (self.debugDualWield == False and self.gearDict[self.dominantHand] != None and self.gearDict[self.dominantHand].twoHanded == True):
                if targetWeapon == "Unused":
                    if self.gearDict["Left Hand"] == None or self.gearDict["Right Hand"] == None:
                        return True
                elif targetWeapon in ["Open Hand", None]:
                    return True
        elif len(combatSkill.weaponTypeList) == 1:
            if targetWeapon == "Unused":
                if self.gearDict["Left Hand"] != None and combatSkill.weaponTypeList[0] == self.gearDict["Left Hand"].weaponType:
                    if not ("Requires Two-Handed Weapon" in combatSkill.ruleDict and self.gearDict["Left Hand"].twoHanded == False):
                        return True
                if self.gearDict["Right Hand"] != None and combatSkill.weaponTypeList[0] == self.gearDict["Right Hand"].weaponType:
                    if not ("Requires Two-Handed Weapon" in combatSkill.ruleDict and self.gearDict["Right Hand"].twoHanded == False):
                        return True
            elif (targetWeapon in ["Open Hand", None] and combatSkill.weaponTypeList[0] == "Open Hand") or (targetWeapon != None and targetWeapon.weaponType == combatSkill.weaponTypeList[0]):
                if not ("Requires Two-Handed Weapon" in combatSkill.ruleDict and targetWeapon not in ["Open Hand", None] and targetWeapon.twoHanded == False):
                    return True

        elif len(combatSkill.weaponTypeList) == 2 and targetWeapon == "Unused":
            correctWeaponTypeList = []
            playerHeldList = [self.gearDict["Left Hand"], self.gearDict["Right Hand"]]
            for weaponType in combatSkill.weaponTypeList:
                if weaponType == "Open Hand" and None in playerHeldList:
                    correctWeaponTypeList.append("Open Hand")
                    del playerHeldList[playerHeldList.index(None)]
                elif weaponType in playerHeldList:
                    correctWeaponTypeList.append(weaponType)
                    del playerHeldList[playerHeldList.index(weaponType)]
            if len(correctWeaponTypeList) == 2:
                return True
            
        return False
    
    def getOppositeHand(self, targetHand):
        if targetHand == "Left Hand":
            return "Right Hand"
        else:
            return "Left Hand"

    def stopActions(self, console):
        if len(self.actionList) > 0:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You stop " + self.actionList[0].actionType.lower() + "ing.", "Code":"9w" + str(len(self.actionList[0].actionType)) + "w3w1y"})
            self.actionList = []
            return True
        return False

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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You scratch your chin and go, 'Hmm..'", "Code":"28w3y3w3y"})
        elif input in "nod":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You nod your head in agreement.", "Code":"30w1y"})
        elif input == "nodnod":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You nodnod.", "Code":"10w1y"})
        elif input == "tap":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You tap your foot impatiently..", "Code":"29w2y"})
        elif input == "boggle":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You boggle in complete incomprehension.", "Code":"38w1y"})
        elif input == "jump":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You jump up and down.", "Code":"20w1y"})
        elif input == "ahah":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"Comprehension dawns upon you.", "Code":"28w1y"})
        elif input == "gasp":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You gasp!", "Code":"8w1y"})
        elif input in ["haha", "lol"]:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You laugh out loud!", "Code":"18w1y"})
        elif input == "cheer":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"And the peasants rejoiced.", "Code":"25w1y"})
        elif input == "smile":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You smile happily.", "Code":"17w1y"})
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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":displayString, "Code":displayCode})
        elif input == "sigh":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You sigh.", "Code":"8w1y"})
        elif input == "grin":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You grin.", "Code":"8w1y"})
        elif input == "snicker":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You snicker softly.", "Code":"18w1y"})
        
    # Mob Functions #
    def loadMob(self, num):
        if num == 1:
            self.name = {"String":"Robotic Greeter Droid", "Code":"21w"}
        elif num == 2:
            self.name = {"String":"Mummy", "Code":"5w"}
            self.flags ["No Chase"] = True
        elif num == 3:
            self.name = {"String":"Reptoid", "Code":"7w"}
        elif num == 4:
            self.name = {"String":"Tall Droid", "Code":"10w"}

        # Create Key List #
        appendKeyList(self.keyList, self.name["String"].lower())

    def lookDescription(self, console):
        console.lineList.insert(0, {"Blank": True})
        console.lineList.insert(0, {"String": "You look at " + self.prefix.lower() + " " + self.name["String"] + ".", "Code":"12w" + str(len(self.prefix)) + "w1w" + self.name["Code"] + "1y"})
        console.lineList.insert(0, {"String": "You see nothing special.", "Code":"23w1y"})
