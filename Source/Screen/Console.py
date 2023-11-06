import pygame
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
        
        self.characterWidth = 57
        
        self.lineList = []
        self.displayLine = 0

    def draw(self, window):
        self.surface.fill([5, 15, 35])

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
        