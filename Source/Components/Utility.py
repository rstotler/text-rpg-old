def circleCircleCollide(loc1, radius1, loc2, radius2):
    import math
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    dr = math.sqrt((dx ** 2) + (dy ** 2))

    if dr <= radius1 + radius2:
        return True
    return False

def writeFast(label, color, location, font, surface):
	labelRender = font.render(label, True, color)
	surface.blit(labelRender, location)

def writeColor(label, colorCode, location, font, surface):
    targetColor = ""
    colorCount = 0
    printIndex = 0
    displayX = location[0]
    writeCheck = False

    for i, letter in enumerate(colorCode):

        # Sort #
        if stringIsNumber(letter):
            if colorCount != 0 : colorCount *= 10
            colorCount += int(letter)
        else:
            targetColor = targetColor + letter
            if len(colorCode) > i + 1 and stringIsNumber(colorCode[i + 1]):
                writeCheck = True

        # Write Check #
        if i + 1 == len(colorCode):
            writeCheck = True

        # Write #
        if writeCheck == True:
            writeColor = [255, 255, 255]
            if targetColor in colorDict : writeColor = colorDict[targetColor]

            textString = label[printIndex:printIndex + colorCount]
            textRender = font.render(textString, True, writeColor)	
            surface.blit(textRender, [displayX, location[1]])

            printIndex += colorCount
            if printIndex == len(label) : return
            displayX += font.size(textString)[0]
            colorCount = 0
            targetColor = ""
            writeCheck = False

colorDict = {"lr":[255, 80,  80],  "r":[255, 0,   0],   "dr":[145, 0,   0],   "ddr":[80,  0,   0],   "dddr":[40, 0, 0],
             "lo":[255, 150, 75],  "o":[255, 100, 0],   "do":[170, 95,  0],   "ddo":[80,  40,  0],   "dddo":[40, 20, 0],
             "ly":[255, 255, 80],  "y":[255, 255, 0],   "dy":[145, 145, 0],   "ddy":[80,  80,  0],   "dddy":[40, 40, 0],
             "lg":[80,  255, 80],  "g":[0,   255, 0],   "dg":[0,   145, 0],   "ddg":[0,   80,  0],   "dddg":[0, 40, 0],
             "lc":[80,  255, 255], "c":[0,   255, 255], "dc":[0,   145, 145], "ddc":[0,   80,  80],  "dddc":[0, 40, 40],
             "lb":[80,  80,  255], "b":[0,   0,   255], "db":[0,   0,   145], "ddb":[0,   0,   80],  "dddb":[0, 0, 40],
             "lv":[255, 80,  255], "v":[255, 0,   255], "dv":[145, 0,   145], "ddv":[80,  0,   80],  "dddv":[40, 0, 40],
             "lm":[175, 80,  255], "m":[175, 0,   255], "dm":[95,  0,   145], "ddm":[75,  0,   80],  "dddm":[37, 0, 40],
             "lw":[255, 255, 255], "w":[255, 255, 255], "dw":[220, 220, 220], "ddw":[150, 150, 150], "dddw":[70, 70, 70],
             "la":[150, 150, 150], "a":[150, 150, 150], "da":[120, 120, 120], "dda":[70,  70,  70],  "ddda":[35, 35, 35],
              "x":[0, 0, 0]}

def writeOutline(label, font, pxOutline=2, textColor=[230, 230, 230], outlineColor=[10, 10, 10]):
    import pygame
    surfaceText = font.render(label, True, textColor).convert_alpha()
    textWidth = surfaceText.get_width() + 2 * pxOutline
    textHeight = font.get_height()

    surfaceOutline = pygame.Surface([textWidth, textHeight + 2 * pxOutline]).convert_alpha()
    surfaceOutline.fill([0, 0, 0, 0])
    surfaceMain = surfaceOutline.copy()
    surfaceOutline.blit(font.render(str(label), True, outlineColor).convert_alpha(), [0, 0])

    circleCache = {}
    for dx, dy in circlePoints(circleCache, pxOutline):
        surfaceMain.blit(surfaceOutline, [dx + pxOutline, dy + pxOutline])
    surfaceMain.blit(surfaceText, [pxOutline, pxOutline])

    return surfaceMain

def circlePoints(circleCache, r):
    r = int(round(r))
    if r in circleCache:
        return circleCache[r]

    x, y, e = r, 0 , 1 - r
    circleCache[r] = points = []

    while x >= y:
        points.append([x, y])
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1

    points += [[y, x] for x, y in points if x > y]
    points += [[-x, y] for x, y in points if x]
    points += [[x, -y] for x, y in points if y]
    points.sort()

    return points

def stringIsNumber(string):
	try:
		int(string)
		return True
	except ValueError:
		return False

def wordWrap(displayString, displayCode, maxWidth):
    def getNextColorLength(code):
        nextColorLengthString = ""
        start = False
        for c in code:
            if stringIsNumber(c):
                start = True
                nextColorLengthString = nextColorLengthString + c
            elif start:
                return int(nextColorLengthString)
        return ""

    def getNextColor(code):
        nextColorString = ""
        start = False
        for index, c in enumerate(code):
            if stringIsNumber(c) == False:
                start = True
                nextColorString = nextColorString + c
            elif start:
                return code[index::], nextColorString
            if start and index == len(code) - 1:
                return code[index-1::]
        return "", ""

    stringList = [{"String":""}]
    for word in displayString.split():
        if len(word) + len(stringList[-1]["String"]) > maxWidth:
            stringList.append({"String":""})
        stringList[-1]["String"] = stringList[-1]["String"] + word + " "

    currentColorLength = getNextColorLength(displayCode)
    code, currentColor = getNextColor(displayCode)
    currentCount = 0
    for displayLine in stringList:
        displayLine["Code"] = ""
        for i in range(len(displayLine["String"])):
            displayLine["Code"] += "1" + currentColor
            currentCount += 1
            if currentCount == currentColorLength:
                currentColorLength = getNextColorLength(code)
                code, currentColor = getNextColor(code)
                currentCount = 0
    return stringList

def appendKeyList(targetKeyList, targetString):
    newKeyList = targetString.split()
    for i in range(len(targetString.split())):
        word = targetString.split()[i]
        if i == 0:
            phrase = targetString
        else:
            phrase = ' '.join(targetString.split()[i::])
        if ',' in phrase:
            phrase = phrase.replace(',', '')
        
        for cNum in range(len(phrase)):
            if cNum > 1:
                if phrase[0:cNum].strip() not in targetKeyList and not (len(phrase[0:cNum].strip()) > 1 and phrase[0:cNum].strip()[-2] == ' ' and phrase[0:cNum].strip()[-1] in ["n", "e", "s", "w"]):
                    targetKeyList.append(phrase[0:cNum].strip())
                    if len(phrase[0:cNum].strip()) > 2 and phrase[0:cNum].strip()[0] == '.' and phrase[0:cNum].strip()[1::] not in targetKeyList and not (len(phrase[0:cNum].strip()[1::]) > 1 and phrase[0:cNum].strip()[1::][-2] == ' ' and phrase[0:cNum].strip()[1::][-1] in ["n", "e", "s", "w"]):
                        targetKeyList.append(phrase[0:cNum].strip()[1::])
                    if '-' in phrase[0:cNum].strip():
                        newPhrase = phrase[0:cNum].strip().replace('-', ' ').strip()
                        if newPhrase not in targetKeyList and not (len(newPhrase) > 1 and newPhrase[-2] == ' ' and newPhrase[-1] in ["n", "e", "s", "w"]):
                            targetKeyList.append(newPhrase)
                    
        if len(phrase.strip()) > 0 and phrase.strip() not in targetKeyList:
            targetKeyList.append(phrase.strip())

def getCountString(targetCount, blankSpace=True):
    displayString = ""
    displayCode = ""
    if targetCount > 1:
        displayString = " (" + str(targetCount) + ")"
        displayCode = "2r" + str(len(str(targetCount))) + "w1r"
        if blankSpace == False:
            displayString = displayString[1::]
            displayCode = "1" + displayCode[1::]
    return displayString, displayCode

def getDamageString(targetDamage, color="dr"):
    stringWithCommas = insertCommasInNumber(str(targetDamage), color)
    displayString = "[" + stringWithCommas["String"] + "]"
    displayCode = "1y" + stringWithCommas["Code"] + "1y"
    return {"String":displayString, "Code":displayCode}

def getTargetUserString(target, posessive=True):
    targetUserString = "Your "
    targetUserCode = "5w"
    if posessive == False:
        targetUserString = "You "
        targetUserCode = "4w"
    if target.num != None:
        sString = "'s "
        sCode = "1y2w"
        if posessive == False:
            sString = " "
            sCode = "1w"
        targetUserString = target.prefix + " " + target.name["String"] + sString
        targetUserCode = str(len(target.prefix)) + "w1w" + target.name["Code"] + sCode
    return {"String":targetUserString, "Code":targetUserCode}

def stackDisplayMessage(messageDataList, messageType, stringHalf1, stringHalf2, codeHalf1, codeHalf2, drawBlankLine, combineCheck=True):
    if combineCheck == True:
        for messageData in messageDataList:
            if stringHalf1 + stringHalf2 == messageData["Original String"]:
                messageData["Count"] += 1
                countString, countCode = getCountString(messageData["Count"], False)
                messageData["String"] = messageData["String Half 1"] + countString + " " + messageData["String Half 2"]
                messageData["Code"] = messageData["Code Half 1"] + countCode + "1w" + messageData["Code Half 2"]
                return
    messageDataList.append({"String":stringHalf1 + stringHalf2, "Code":codeHalf1 + codeHalf2, "Draw Blank Line":drawBlankLine, "Count":1, "Message Type":messageType, "Original String":stringHalf1 + stringHalf2, "String Half 1":stringHalf1, "String Half 2":stringHalf2, "Code Half 1":codeHalf1, "Code Half 2":codeHalf2})

def insertCommasInNumber(targetNumString, color="w"):
    returnString = ""
    returnCode = ""

    negativeCheck = False
    if targetNumString[0] == '-':
        negativeCheck = True
        targetNumString = targetNumString[1::]

    loopRange = int((len(targetNumString) - 1) / 3)
    for i in range(loopRange):
        startIndex = 3
        if startIndex > len(targetNumString):
            startIndex = len(targetNumString)
        returnString = "," + targetNumString[-startIndex::] + returnString
        returnCode = "1y" + str(len(targetNumString[-startIndex::])) + color + returnCode
        targetNumString = targetNumString[0:-startIndex]
    returnString = targetNumString + returnString
    returnCode = str(len(targetNumString)) + color + returnCode
    if negativeCheck == True:
        returnString = '-' + returnString
        returnCode = "1y" + returnCode
    return {"String":returnString, "Code":returnCode}

def createUnderlineString(targetString):
    underlineString = ""
    underlineCode = ""
    for i in range(len(targetString)):
        underlineChar = "-"
        indentCount = int(len(targetString) * .15)
        if indentCount <= 0:
            indentCount = 1
        if i not in range(0, indentCount) and i not in range(len(targetString) - indentCount, len(targetString)):
            underlineChar = "="
        underlineString = underlineString + underlineChar
        if i % 2 == 1:
            underlineCode = underlineCode + "1y"
        else:
            underlineCode = underlineCode + "1dy"
    return {"String":underlineString, "Code":underlineCode}

def createDefaultString(targetString):
    if isinstance(targetString, dict):
        return targetString
    else:
        targetCode = str(len(targetString)) + "w"
        return {"String":targetString, "Code":targetCode}

def writeCrashReport(errorString, input, player):
    with open("../CrashReport.txt", "w") as f:
        f.write(errorString + "\n")
        f.write("Input: " + input + "\n")
        f.write("Player Loc: [" + str(player.galaxy) + ", " + str(player.system) + ", " + str(player.planet) + ", " + str(player.area) + ", " + str(player.room) + "]" + "\n")
        f.write("Player Spaceship: " + str(player.spaceship) + "\n")
        f.write("Player Targets: " + str(len(player.targetList)) + "\n")
        f.write("Player Group: " + str(len(player.recruitList)) + "\n\n")

        f.write("Player Inventory: " + str(len(player.getAllItemList(["Inventory"]))) + "\n")
        for item in player.getAllItemList(["Inventory"]):
            quantityString = ""
            if hasattr(item, "quantity") == True and item.quantity != None:
                quantityString = " (" + str(item.quantity) + ")"
            f.write(str(item.num) + " - [" + item.pocket + "] " + str(item.name["String"] + quantityString) + "\n")
        f.write("\n")

        f.write("Player Gear: " + str(len(player.getAllItemList(["Gear"]))) + "\n")
        for gearSlot in player.gearDict:
            slotRange = 1
            if isinstance(player.gearDict[gearSlot], list):
                slotRange = 2
            for i in range(slotRange):
                indexString = ""
                if slotRange == 2:
                    indexString = " (" + str(i) + ")" 
                targetSlot = player.gearDict[gearSlot]
                if isinstance(player.gearDict[gearSlot], list):
                    targetSlot = player.gearDict[gearSlot][i]
                slotString = "None"
                if targetSlot != None:
                    slotString = str(targetSlot.num) + " - " + targetSlot.name["String"]
                f.write(gearSlot + indexString + " - " + slotString + "\n")

def createMob(num, targetRoom, targetMob=None):
    if targetMob == None:
        from GameData.Player.Player import Player
        if targetRoom.spaceshipObject != None:
            targetGalaxy = targetRoom.spaceshipObject.galaxy
            targetSystem = targetRoom.spaceshipObject.system
            targetPlanet = targetRoom.spaceshipObject.planet
            targetArea = targetRoom.area
            targetRoomNum = targetRoom.room
            targetSpaceship = targetRoom.spaceshipObject.num
        else:
            targetGalaxy = targetRoom.galaxy
            targetSystem = targetRoom.system
            targetPlanet = targetRoom.planet
            targetArea = targetRoom.area
            targetRoomNum = targetRoom.room
            targetSpaceship = None
        targetMob = Player(targetGalaxy, targetSystem, targetPlanet, targetArea, targetRoomNum, targetSpaceship, num)

    # Set Room Display Position #
    import random
    xOffset = random.randrange(160) - 80
    yOffset = random.randrange(65) - 20
    targetMob.displayOffset = [xOffset, yOffset]

    # Insert Mob Into List (Depending On Y-Offset) #
    insertIndex = None
    for i, mob in enumerate(targetRoom.mobList):
        if yOffset >= mob.displayOffset[1]:
            insertIndex = i + 1
    if len(targetRoom.mobList) == 0 or insertIndex == None:
        insertIndex = 0
    targetRoom.mobList.insert(insertIndex, targetMob)

    return targetMob

def createItem(num, type=None, quantity=None, targetRoom=None):
    import copy
    
    if type == "Armor":
        from GameData.Item.Armor import Armor
        createdItem = Armor(num)
    elif type == "Weapon":
        from GameData.Item.Weapon import Weapon
        createdItem = Weapon(num)
    elif type == "Ammo":
        from GameData.Item.Ammo import Ammo
        createdItem = Ammo(num, quantity)
    else:
        from GameData.Item.Item import Item
        createdItem = Item(num)

    if targetRoom != None:
        loopRange = 1
        if quantity != None and type not in ["Ammo"]: # Add Other Quantity Items Here
            loopRange = quantity
        for i in range(loopRange):
            targetRoom.itemList.append(copy.deepcopy(createdItem))
    return createdItem
