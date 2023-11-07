import pygame, random
from pygame import *
from Components.Utility import *

# Console Size - [57, 32] #
# Character Size - [10, 18] #

class Console:

    def __init__(self):
        self.consoleLines = 18

        rectSize = [580, (self.consoleLines * 18) + 6]
        self.surface = pygame.Surface(rectSize)
        self.font = pygame.font.Font("../Assets/Fonts/CodeNewRomanB.otf", 18)

        self.starBackgroundList = []
        self.starBackgroundAlpha = [55, 35, 15]
        self.starBackgroundDir = []

        self.characterWidth = 57
        
        self.lineList = []
        self.displayLine = 0

        self.loadSurfaces(rectSize)

    def loadSurfaces(self, rectSize):
        for i in range(len(self.starBackgroundAlpha)):
            self.starBackgroundList.append(pygame.Surface(rectSize, flags=SRCALPHA))
            self.starBackgroundDir.append(random.randrange(8) / 2)
            for s in range(50):
                x = random.randrange(rectSize[0])
                y = random.randrange(rectSize[1])
                starColor = [200, 200, 200]
                if random.randrange(7) == 0:
                    colorNum = random.randrange(3)
                    if colorNum == 0 : starColor = [200, 0, 0]
                    elif colorNum == 1 : starColor = [0, 200, 0]
                    elif colorNum == 2 : starColor = [0, 0, 200]
                self.starBackgroundList[-1].set_at([x, y], starColor)

    def draw(self, window):
        self.surface.fill([15, 15, 15])
        for i in range(len(self.starBackgroundAlpha)):
            self.starBackgroundAlpha[i] += self.starBackgroundDir[i]
            if self.starBackgroundAlpha[i] >= 120 or self.starBackgroundAlpha[i] <= 15:
                self.starBackgroundDir[i] *= -1
            self.starBackgroundList[i].set_alpha(self.starBackgroundAlpha[i])
            self.surface.blit(self.starBackgroundList[i], [0, 0])

        startIndex = self.displayLine
        endIndex = startIndex + self.consoleLines
        if endIndex > len(self.lineList):
            endIndex = len(self.lineList)

        drawLoc = [5, self.surface.get_height() - 21]
        for line in self.lineList[startIndex:endIndex]:
            if "String" in line:
                lineCode = str(len(line["String"])) + "w"
                if "Code" in line:
                    lineCode = line["Code"]
                writeColor(line["String"], lineCode, drawLoc, self.font, self.surface)
            drawLoc[1] -= 18
        window.blit(self.surface, [0, 248])

    def scroll(self, keyboard, yMod):
        scrollMod = 1.0
        if keyboard.control == True:
            scrollMod = 6.0
        self.displayLine += int(yMod * scrollMod)
        if self.displayLine < 0:
            self.displayLine = 0
        elif self.displayLine > len(self.lineList) - self.consoleLines:
            self.displayLine = len(self.lineList) - self.consoleLines

    def write(self, displayString, displayCode, blankCheck=False):
        if blankCheck == True and not (len(self.lineList) > 0 and "Blank" in self.lineList[0]):
            self.lineList.insert(0, {"Blank":True})

        if len(displayString) <= self.characterWidth:
            self.lineList.insert(0, {"String":displayString, "Code":displayCode})
        else:
            for displayLine in wordWrap(displayString, displayCode, self.characterWidth):
                self.lineList.insert(0, {"String":displayLine["String"], "Code":displayLine["Code"]})

        self.displayLine = 0
        