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
        
        for cNum in range(len(phrase)):
            if cNum > 1:
                if phrase[0:cNum].strip() not in targetKeyList:
                    targetKeyList.append(phrase[0:cNum].strip())
                    if len(phrase[0:cNum].strip()) > 2 and phrase[0:cNum].strip()[0] == '.' and phrase[0:cNum].strip()[1::] not in targetKeyList:
                        targetKeyList.append(phrase[0:cNum].strip()[1::])
                    if '-' in phrase[0:cNum].strip():
                        newPhrase = phrase[0:cNum].strip().replace('-', ' ').strip()
                        if newPhrase not in targetKeyList:
                            targetKeyList.append(newPhrase)

        if phrase.strip() not in targetKeyList:
            targetKeyList.append(phrase.strip())

def getCountString(targetCount):
    displayString = ""
    displayCode = ""
    if targetCount > 1:
        displayString = " (" + str(targetCount) + ")"
        displayCode = "2r" + str(len(str(targetCount))) + "w1r"
    return displayString, displayCode
