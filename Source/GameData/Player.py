import copy, random
from Components.Utility import stringIsNumber
from GameData.Room import Room
from GameData.Mob import Mob
from GameData.Item import Item
from GameData.Spaceship import Spaceship

class Player:

    def __init__(self):
        self.galaxy = 0
        self.system = 0
        self.planet = 1
        self.area = 0
        self.room = 0
        self.spaceship = None

        self.currentAction = None

        self.maxLookDistance = 5
        self.maxTargetDistance = 3
        self.targetList = []

        self.itemDict = {"Armor": [], "Weapon":[], "Ammo":[], "Misc": []}
        self.gearDict = {"Head":None, "Face":None, "Neck":[None, None], "Body Under":None, "Body Over":None, "About Body":None, "Hands":None, "Finger":[None, None], "Legs Under":None, "Legs Over":None, "Feet":None, "Left Hand":None, "Right Hand":None}
        self.dominantHand = "Right Hand"

        self.emoteList = ["hmm", "hm", "nod", "nodnod", "tap", "boggle", "ahah", "jump", "gasp", "haha", "lol", "cheer", "smile", "swear", "sigh"]

        self.debugDualWield = False

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
                elif targetMob != None and isinstance(targetMob, Mob) == False:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You can't target that.", "Code":"7w1y13w1y"})
                
                else:
                    targetMob = None
                    targetCount = 0
                    targetRange = targetMobCount
                    alreadyTargetingCheck = False
                    if targetRange == "All":
                        targetRange = len(targetRoom.mobList)
                    for i in range(targetRange):
                        for mob in targetRoom.mobList:
                            if targetMobKey == "All" or targetMobKey in mob.keyList:
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

                    if targetCount == 0 and alreadyTargetingCheck == True:
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You are already targeting them.", "Code":"30w1y"})
                    elif targetCount == 0:
                        console.lineList.insert(0, {"Blank": True})
                        console.lineList.insert(0, {"String":"You don't see them.", "Code":"7w1y10w1y"})
                    
                    elif targetMob != "Multiple":
                        displayString = "You narrow your vision on " + targetMob.prefix.lower() + " " + targetMob.name["String"] + "."
                        displayCode = "26w" + str(len(targetMob.prefix)) + "w1w" + targetMob.name["Code"] + "1y"
                        targetCountString = ""
                        targetCountCode = ""
                        if targetCount > 1:
                            targetCountString = " (" + str(targetCount) + ")"
                            targetCountCode = "2r" + str(len(str(targetCount))) + "w1r"
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
                    elif isinstance(targetMob, Mob) == False:
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
                    targetCountString = ""
                    targetCountCode = ""
                    if targetCount > 1:
                        targetCountString = " (" + str(targetCount) + ")"
                        targetCountCode = "2r" + str(len(str(targetCount))) + "w1r"
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

    def moveCheck(self, console, galaxyList, currentRoom, targetDir):
        if currentRoom.exit[targetDir] != None:
            if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Manual" and currentRoom.door[targetDir]["Status"] in ["Closed", "Locked"]:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "The door is closed.", "Code":"18w1y"})
            elif currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic" and currentRoom.door[targetDir]["Status"] == "Locked" and "Password" in currentRoom.door[targetDir] and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String": "You lack the proper key.", "Code":"23w1y"})

            else:
                targetRoom = None
                targetRoomData = currentRoom.exit[targetDir]
                if len(targetRoomData) == 3 and currentRoom.spaceshipObject != None:
                    targetRoom = currentRoom.spaceshipObject.areaList[targetRoomData[1]].roomList[targetRoomData[2]]
                elif len(targetRoomData) == 5:
                    targetRoom = Room.exists(galaxyList, None, targetRoomData[0], targetRoomData[1], targetRoomData[2], targetRoomData[3], targetRoomData[4])
                elif targetRoomData == "Spaceship Exit" and currentRoom.spaceshipObject != None:
                    targetRoom = Room.exists(galaxyList, None, currentRoom.spaceshipObject.landedLocation[0], currentRoom.spaceshipObject.landedLocation[1], currentRoom.spaceshipObject.landedLocation[2], currentRoom.spaceshipObject.landedLocation[3], currentRoom.spaceshipObject.landedLocation[4])

                if targetRoom != None:
                    if len(targetRoomData) == 3:
                        self.area = targetRoomData[1]
                        self.room = targetRoomData[2]
                    else:
                        self.galaxy = targetRoom.galaxy
                        self.system = targetRoom.system
                        self.planet = targetRoom.planet
                        self.area = targetRoom.area
                        self.room = targetRoom.room
                        if self.spaceship != None:
                            self.spaceship = None

                    console.lineList.insert(0, {"Blank": True})
                    if currentRoom.door[targetDir] != None and currentRoom.door[targetDir]["Type"] == "Automatic":
                        doorString = "door"
                        if currentRoom.exit[targetDir] == "Spaceship Exit":
                            doorString = "hatch"
                        console.lineList.insert(0, {"String": "The " + doorString + " opens and closes as you walk through.", "Code":"4w" + str(len(doorString)) + "w37w1y"})
                        console.lineList.insert(0, {"Blank": True})
                    targetRoom.display(console, galaxyList, self)

        else:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String": "You can't go that way!", "Code":"7w1y13w1y"})

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
        elif targetDoorAction == "Open" and currentRoom.door[targetDir]["Status"] == "Locked" and self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
            console.lineList.insert(0, {"Blank": True})
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

            console.lineList.insert(0, {"Blank": True})
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
        elif self.hasKey(currentRoom.door[targetDir]["Password"]) == False:
            console.lineList.insert(0, {"Blank": True})
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
                    
            console.lineList.insert(0, {"Blank": True})
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
        
        elif isinstance(targetObject, Mob):
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
        
        elif isinstance(targetObject, Mob):
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
            console.lineList.insert(0, {"Blank": True})
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
                console.lineList.insert(0, {"Blank": True})
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
                    console.lineList.insert(0, {"Blank": True})
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
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't carry that much weight.", "Code":"7w1y24w1y"})
                        elif noGetCheck == True:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick that up.", "Code":"7w1y14w1y"})
                        elif itemCount == 0:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"There is nothing to get.", "Code":"23w1y"})
                        else:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You can't pick anything up.", "Code":"7w1y18w1y"})
                    else:
                        if targetContainerKey == "All" and getCount > 1 and (count == "All" or len(getContainerIndexList) > 1):
                            modString = ""
                            modCode = ""
                            if tooMuchWeightCheck == False and targetItemKey == "All":
                                modString = "every corner of "
                                modCode = "16w"
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You loot " + modString + "the place.", "Code":"9w" + modCode + "9w1y"})
                        elif targetContainerKey == None and getItem == "Multiple" and getCount > 1 and getCount == itemCount:
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":"You pick everything up.", "Code":"22w1y"})
                        elif getItem == "Multiple":
                            if targetContainerKey == "All" : totalContainerCount = len(combinedItemList)
                            else:
                                if playerItemLocation != None : totalContainerCount = len(self.getAllItemList([playerItemLocation]))
                                else : totalContainerCount = len(currentRoom.itemList)
                            if targetContainerKey != None and getContainerIndexList[-1] < totalContainerCount:
                                console.lineList.insert(0, {"Blank": True})
                                console.lineList.insert(0, {"String":"You get some things out of " + targetContainer.prefix.lower() + " " + targetContainer.name["String"] + ".", "Code":"27w" + str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"] + "1y"})
                            else:
                                console.lineList.insert(0, {"Blank": True})
                                console.lineList.insert(0, {"String":"You pick some things up.", "Code":"23w1y"})
                        elif getItem != "Multiple":
                            countString = ""
                            countCode = ""
                            if getCount > 1:
                                countString = " (" + str(getCount) + ")"
                                countCode = "2r" + str(len(str(getCount))) + "w1r"
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
                            getString = "You " + pickUpString + getItem.prefix.lower() + " " + getItem.name["String"] + countString + fromString + "."
                            getCode = "4w" + pickUpCode + str(len(getItem.prefix)) + "w1w" + getItem.name["Code"] + countCode + fromCode + "1y"
                            console.lineList.insert(0, {"Blank": True})
                            console.lineList.insert(0, {"String":getString, "Code":getCode})
         
    def putCheck(self, console, galaxyList, currentRoom, targetItemKey, targetContainerKey, count):
        targetContainer, playerItemLocation = self.getTargetItem(targetContainerKey)
        if targetContainer == None:
            targetContainer = currentRoom.getTargetObject(targetContainerKey, ["Mobs", "Items", "Spaceships"])
    
        if targetContainer == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
        elif isinstance(targetContainer, Item) == False or targetContainer.containerList == None:
            console.lineList.insert(0, {"Blank": True})
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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
            elif targetItemKey != "All" and putItem == targetContainer:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You can't put something inside itself.", "Code":"7w1y29w1y"})
            elif inventorySize == 0:
                console.lineList.insert(0, {"Blank": True})
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
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"It won't fit.", "Code":"6w1y5w1y"})
                elif putCount == 0:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You don't have anything to put in.", "Code":"7w1y25w1y"})
                elif putItem == "Multiple":
                    targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                    targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                    if currentRoom.isLit(galaxyList, self) == False:
                        targetContainerString = "something"
                        targetContainerCode = "9w"
                    displayString = "You put some things in " + targetContainerString + "."
                    displayCode = "23w" + targetContainerCode + "1y"
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                else:
                    countString = ""
                    countCode = ""
                    if putCount > 1:
                        countString = " (" + str(putCount) + ")"
                        countCode = "2r" + str(len(str(putCount))) + "w1r"
                    targetContainerString = targetContainer.prefix.lower() + " " + targetContainer.name["String"]
                    targetContainerCode = str(len(targetContainer.prefix)) + "w1w" + targetContainer.name["Code"]
                    if currentRoom.isLit(galaxyList, self) == False:
                        targetContainerString = "something"
                        targetContainerCode = "9w"
                    displayString = "You put " + putItem.prefix.lower() + " " + putItem.name["String"] + countString + " in " + targetContainerString + "."
                    displayCode = "8w" + str(len(putItem.prefix)) + "w1w" + putItem.name["Code"] + countCode + "4w" + targetContainerCode + "1y"
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                
    def dropCheck(self, console, galaxyList, currentRoom, targetItemKey, count):
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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

        else:
            dropCount = 0
            quantityCount = count
            delDict = {}
            breakCheck = False
            for pocket in self.itemDict:
                delDict[pocket] = []
                for i, item in enumerate(self.itemDict[pocket]):
                    if targetItemKey == "All" or targetItemKey in item.keyList:
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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You aren't carrying anything.", "Code":"8w1y19w1y"})
            elif dropCount > 1 and dropCount == inventoryCount:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You drop everything on the ground.", "Code":"33w1y"})    
            elif dropItem == "Multiple":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You drop some things on the ground.", "Code":"34w1y"})
            elif dropItem != None:
                countString = ""
                countCode = ""
                if dropCount > 1:
                    countString = " (" + str(dropCount) + ")"
                    countCode = "2r" + str(len(str(dropCount))) + "w1r"
                dropString = "You drop " + dropItem.prefix.lower() + " " + dropItem.name["String"] + " on the ground." + countString
                dropCode = "9w" + str(len(dropItem.prefix.lower())) + "w1w" + dropItem.name["Code"] + "14w1y" + countCode
                console.lineList.insert(0, {"Blank": True})
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
            targetWeapon = self.gearDict[oldHand]

        if targetWeapon != None:
            displayString = "You switch " + targetWeapon.prefix.lower() + " " + targetWeapon.name["String"] + " to your " + newHand.lower() + "."
            displayCode = "11w" + str(len(targetWeapon.prefix)) + "w1w" + targetWeapon.name["Code"] + "9w" + str(len(newHand)) + "w1y"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":displayString, "Code":displayCode})
        else:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You switch up your handedness.", "Code":"29w1y"})

    def reloadCheck(self, console, reloadKey, reloadSlot, ammoKey):
        # use the highest capacity mag available
        weaponRange = 1
        if reloadKey == "All":
            weaponRange = 2
        for weaponCount in range(weaponRange):
            pass

    def unloadCheck(self, console, unloadKey):
        pass
        # unload held guns
        # unload guns in inventory
        # unload guns on ground

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
            displayDict = {}
            for item in self.itemDict[targetPocket]:
                if item.num not in displayDict:
                    itemCount = 1
                    if item.quantity != None:
                        itemCount = item.quantity
                    displayDict[item.num] = {"Count": itemCount, "ItemData": item}
                else:
                    displayDict[item.num]["Count"] += 1
            
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
                countString = ""
                countCode = ""
                inventoryCount = 0
                for displayItemData in displayDict:
                    inventoryCount += displayDict[displayItemData]["Count"]
                if inventoryCount > 1:
                    countString = " (" + str(inventoryCount) + ")"
                    countCode = "2r" + str(len(str(inventoryCount))) + "w1r"
                console.lineList.insert(0, {"String": "-Something" + countString, "Code": "1y9w" + countCode})
            else:
                for item in self.itemDict[targetPocket]:
                    if item.num in displayDict:
                        modString = ""
                        modCode = ""
                        if "Glowing" in item.flags and item.flags["Glowing"] == True:
                            modString = " (Glowing)"
                            modCode = "2y1w1dw1ddw1w2dw1ddw1y"
                        countString = ""
                        countCode = ""
                        if displayDict[item.num]["Count"] > 1:
                            countString = " (" + str(displayDict[item.num]["Count"]) + ")"
                            countCode = "2r" + str(len(str(displayDict[item.num]["Count"]))) + "w1r"
                        itemDisplayString = item.prefix + " " + item.name["String"]
                        itemDisplayCode = str(len(item.prefix)) + "w1w" + item.name["Code"]
                        console.lineList.insert(0, {"String":itemDisplayString + countString + modString, "Code":itemDisplayCode + countCode + modCode})
                        del displayDict[item.num]

    def wearCheck(self, console, targetItemKey, count, targetGearSlotIndex=None):
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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't wear that.", "Code":"7w1y11w1y"})
        elif targetItemKey != "All" and wearItem == None:
            console.lineList.insert(0, {"Blank": True})
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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have anything to wear.", "Code":"7w1y23w1y"})    
            elif wearCount == 0:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You are already wearing something.", "Code":"33w1y"})    
            elif len(previousWornItemList) > 0 and wearCount > 1:
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You switch around some of your gear.", "Code":"35w1y"})
            elif len(previousWornItemList) == 0 and wearCount > 1 and wearItem == "Multiple":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You put on some armor.", "Code":"21w1y"})
            elif len(previousWornItemList) == 1 and isinstance(wearItem, Item):
                wearString = "You remove " + previousWornItemList[0].prefix.lower() + " " + previousWornItemList[0].name["String"] + " and wear " + wearItem.prefix.lower() + " " + wearItem.name["String"] + "."
                wearCode = "11w" + str(len(previousWornItemList[0].prefix)) + "w1w" + previousWornItemList[0].name["Code"] + "10w" + str(len(wearItem.prefix)) + "w1w" + wearItem.name["Code"] + "1y"
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":wearString, "Code":wearCode})
            elif len(previousWornItemList) == 0 and isinstance(wearItem, Item):
                wearString = "You wear " + wearItem.prefix.lower() + " " + wearItem.name["String"] + " on your " + wearItem.gearSlot.lower() + "."
                wearCode = "9w" + str(len(wearItem.prefix)) + "w1w" + wearItem.name["Code"] + "9w" + str(len(wearItem.gearSlot)) + "w1y"
                countString = ""
                countCode = ""
                if wearItem != "Multiple" and wearCount > 1:
                    countString = " (" + str(wearCount) + ")"
                    countCode = "2r" + str(len(str(wearCount))) + "w1r"
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":wearString + countString, "Code":wearCode + countCode})

            # Wield Check #
            if targetItemKey == "All" and count == "All":
                self.wieldCheck(console, "All", None, 2, False)

    def wieldCheck(self, console, targetItemKey, targetGearSlotKey, count, blankCheck=True):
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
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You don't have anything to wield.", "Code":"7w1y24w1y"})
        elif wieldItem == None:
            if blankCheck == True : console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})
        elif wieldItem.pocket != "Weapon":
            if blankCheck == True : console.lineList.insert(0, {"Blank": True})
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
                if wieldItem != None and wieldItem.twoHanded and self.debugDualWield == False:
                    targetGearSlot = self.dominantHand

            wieldCount = 0
            slotCount = 0
            slotItem = None
            breakCheck = False
            for c in range(count):
                defaultGearSlot = self.dominantHand
                if (targetItemKey == "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[defaultGearSlot].twoHanded == False and self.debugDualWield == False) or \
                (targetItemKey != "All" and self.gearDict[defaultGearSlot] != None and self.gearDict[self.getOppositeHand(defaultGearSlot)] == None and self.gearDict[defaultGearSlot].twoHanded == False and wieldItem.twoHanded == False and count == 1) or \
                (c == 1 and not (self.gearDict[defaultGearSlot] != None and self.gearDict[defaultGearSlot].twoHanded == True and self.debugDualWield == False)):
                    defaultGearSlot = self.getOppositeHand(self.dominantHand)
                if targetGearSlot != None:
                    defaultGearSlot = targetGearSlot
                delIndex = -1
                for i, item in enumerate(self.itemDict["Weapon"]):
                    if targetItemKey == "All" or targetItemKey in item.keyList:
                        if not (targetItemKey == "All" and self.gearDict[defaultGearSlot] != None) and \
                        not (targetItemKey == "All" and item.twoHanded == True and (self.gearDict[self.dominantHand] != None or self.gearDict[self.getOppositeHand(self.dominantHand)] != None) and self.debugDualWield == False):
                            if self.gearDict[defaultGearSlot] != None:
                                self.itemDict[self.gearDict[defaultGearSlot].pocket].append(self.gearDict[defaultGearSlot])
                                slotCount += 1
                                if slotItem == None:
                                    slotItem = self.gearDict[defaultGearSlot]
                                elif slotItem != "Multiple" and slotItem.num != self.gearDict[defaultGearSlot].num:
                                    slotItem = "Multiple"
                            self.gearDict[defaultGearSlot] = item
                            oppositeHand = self.gearDict[self.getOppositeHand(defaultGearSlot)]
                            if oppositeHand != None and (self.gearDict[defaultGearSlot].twoHanded == True or oppositeHand.twoHanded == True) and self.debugDualWield == False:
                                self.itemDict[oppositeHand.pocket].append(oppositeHand)
                                self.gearDict[self.getOppositeHand(defaultGearSlot)] = None
                                slotCount += 1
                                if slotItem == None:
                                    slotItem = oppositeHand
                                elif slotItem != "Multiple" and slotItem.num != oppositeHand.num:
                                    slotItem = "Multiple"
                            wieldCount += 1
                            if wieldItem == None:
                                wieldItem = item
                            elif wieldItem != "Multiple" and wieldItem.num != item.num:
                                wieldItem = "Multiple"
                            delIndex = i
                            break
                if delIndex != -1:
                    if self.itemDict["Weapon"][delIndex].twoHanded == True and self.debugDualWield == False:
                        breakCheck = True
                    del self.itemDict["Weapon"][delIndex]
                if breakCheck:
                    break

            if wieldCount == 0:
                if blankCheck == True:
                    console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You're already holding something.", "Code":"3w1y28w1y"})
            elif wieldItem == "Multiple":
                if slotItem == None:
                    if blankCheck == True : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You hold some weapons in your hands.", "Code":"35w1y"})
                else:
                    if blankCheck == True : console.lineList.insert(0, {"Blank": True})
                    console.lineList.insert(0, {"String":"You switch some weapons around.", "Code":"30w1y"})
            elif slotItem == None:
                countString = ""
                countCode = ""
                handsString = defaultGearSlot.lower()
                handsCode = str(len(defaultGearSlot)) + "w"
                if wieldCount == 2:
                    countString = " (2)"
                    countCode = "2r1w1r"
                    handsString = "hands"
                    handsCode = "5w"
                displayString = "You hold " + wieldItem.prefix.lower() + " " + wieldItem.name["String"] + countString + " in your " + handsString + "."
                displayCode = "9w" + str(len(wieldItem.prefix)) + "w1w" + wieldItem.name["Code"] + countCode + "9w" + handsCode + "1y"
                if blankCheck == True : console.lineList.insert(0, {"Blank": True})
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
                    wieldString = wieldItem.prefix.lower() + " " + wieldItem.name["String"]
                    wieldCode = str(len(wieldItem.prefix)) + "w1w" + wieldItem.name["Code"]
                    if wieldCount > 1:
                        wieldCountString = " (2)"
                        wieldCountCode = "2r1w1r"
                displayString = "You remove " + slotString + slotCountString + " and wield " + wieldString + "." + wieldCountString
                displayCode = "11w" + slotCode + slotCountCode + "11w" + wieldCode + "1y" + wieldCountCode
                if blankCheck == True : console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
                           
    def removeCheck(self, console, targetItemKey, count, targetGearSlotIndex=None):
        removeItem = None
        if targetItemKey != "All":
            for gearSlot in self.gearDict:
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
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You can't find it.", "Code":"7w1y9w1y"})

        else:
            removeCount = 0
            breakCheck = False
            removeItem = None
            for gearSlot in self.gearDict:
                slotRange = 1
                targetGearSlot = self.gearDict[gearSlot]
                if targetGearSlotIndex == None and isinstance(targetGearSlot, list):
                    slotRange = len(targetGearSlot)
                for slotIndex in range(slotRange):
                    if isinstance(self.gearDict[gearSlot], list):
                        if targetGearSlotIndex != None:
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
                            if isinstance(self.gearDict[gearSlot], list):
                                self.gearDict[gearSlot][slotIndex] = None
                            else:
                                self.gearDict[gearSlot] = None

                            if count != "All" and removeCount >= count:
                                breakCheck = True
                                break
                if breakCheck:
                    break

            # Messages #
            if targetItemKey == "All" and count == "All":
                displayString = "You remove all of your gear."
                displayCode = "27w1y"
                if random.randrange(10) == 0:
                    displayString = "You strip down to your birthday suit."
                    displayCode = "36w1y"
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})
            elif removeItem == "Multiple":
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"You remove some gear.", "Code":"20w1y"})
            elif isinstance(removeItem, Item):
                countString = ""
                countCode = ""
                if removeCount > 1:
                    countString = " (" + str(removeCount) + ")"
                    countCode = "2r" + str(len(str(removeCount))) + "w1r"
                console.lineList.insert(0, {"Blank": True})
                displayString = "You remove " + removeItem.prefix + " " + removeItem.name["String"] + "." + countString
                displayCode = "11w" + str(len(removeItem.prefix)) + "w1w" + removeItem.name["Code"] + "1y" + countCode
                console.lineList.insert(0, {"String":displayString, "Code":displayCode})

    def displaySkills(self, console):
        pass

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
                modString = ""
                modCode = ""
                
                if isinstance(self.gearDict[gearSlot], list):
                    targetSlot = self.gearDict[gearSlot][slotIndex]
                else:
                    targetSlot = self.gearDict[gearSlot]
                if targetSlot != None:
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
                        if targetSlot.ranged == True:
                            if targetSlot.magazine == "Empty":
                                gearString += " [Empty]"
                                gearCode += "2r5w1r"
                console.lineList.insert(0, {"String":gearSlotString + ": " + gearString + modString, "Code":gearSlotCode + "2y" + gearCode + modCode})

    def boardCheck(self, console, galaxyList, currentRoom, targetSpaceshipKey):
        targetSpaceship = None
        for spaceship in currentRoom.spaceshipList:
            if targetSpaceshipKey in spaceship.keyList:
                targetSpaceship = spaceship
                break

        if self.spaceship != None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You are already inside.", "Code":"22w1y"})
        elif targetSpaceship == None:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You don't see anything like that.", "Code":"7w1y24w1y"})
        elif targetSpaceship.hatchPassword != None and self.hasKey(targetSpaceship.hatchPassword) == False:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You lack the proper key.", "Code":"23w1y"})
        
        else:
            self.spaceship = targetSpaceship.num
            self.area = targetSpaceship.hatchLocation[0]
            self.room = targetSpaceship.hatchLocation[1]

            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"The hatch opens and closes as you step inside.", "Code":"45w1y"})
            console.lineList.insert(0, {"Blank": True})

            spaceshipHatchRoom = targetSpaceship.areaList[self.area].roomList[self.room]
            spaceshipHatchRoom.display(console, galaxyList, self)

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

    def hasKey(self, password):
        for pocket in self.itemDict:
            for item in self.itemDict[pocket]:
                if "Password List" in item.flags:
                    for playerPassword in item.flags["Password List"]:
                        if playerPassword == password:
                            return True
        return False

    def lightInBagCheck(self, targetPocket):
        for item in self.itemDict[targetPocket]:
            if "Glowing" in item.flags and item.flags["Glowing"] == True:
                return True

        return False

    def getOppositeHand(self, targetHand):
        if targetHand == "Left Hand":
            return "Right Hand"
        else:
            return "Left Hand"

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
            displayString = ""
            for i in range(4):
                targetChar = swearString[random.randrange(len(swearString))]
                displayString = displayString + targetChar
                swearString = swearString.replace(targetChar, "")
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":displayString + "!", "Code":"4w1y"})
        elif input == "sigh":
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"You sigh.", "Code":"8w1y"})
        