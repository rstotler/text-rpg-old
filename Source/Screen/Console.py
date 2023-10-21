import pygame
from pygame import *
from Components.Utility import writeColor
from Components.Utility import wordWrap

# Console Size - [59, 32] #
# Character Size - [10, 18] #

class Console:

    def __init__(self):
        rectSize = [600, 600 - 22]
        self.surface = pygame.Surface(rectSize)
        self.font = pygame.font.Font("../Assets/Fonts/CodeNewRomanB.otf", 18)

        self.characterWidth = 59
        
        self.lineList = []
        self.displayLine = 0

    def draw(self, window):
        self.surface.fill([5, 15, 35])

        startIndex = self.displayLine
        endIndex = startIndex + 32
        if endIndex > len(self.lineList):
            endIndex = len(self.lineList)

        drawLoc = [5, self.surface.get_height() - 18]
        for line in self.lineList[startIndex:endIndex]:
            if "String" in line:
                lineCode = str(len(line["String"])) + "w"
                if "Code" in line:
                    lineCode = line["Code"]
                writeColor(line["String"], lineCode, drawLoc, self.font, self.surface)
            drawLoc[1] -= 18
        window.blit(self.surface, [0, 0])

    def scroll(self, keyboard, yMod):
        scrollMod = 1.0
        if keyboard.control == True:
            scrollMod = 6.0
        self.displayLine += int(yMod * scrollMod)
        if self.displayLine < 0:
            self.displayLine = 0
        elif self.displayLine > len(self.lineList) - 32:
            self.displayLine = len(self.lineList) - 32

    def write(self, displayString, displayCode, blankCheck=False):
        if blankCheck == True and not (len(self.lineList) > 0 and "Blank" in self.lineList[0]):
            self.lineList.insert(0, {"Blank": True})

        if len(displayString) <= self.characterWidth:
            self.lineList.insert(0, {"String":displayString, "Code":displayCode})
        else:
            for displayLine in wordWrap(displayString, displayCode, self.characterWidth):
                self.lineList.insert(0, {"String":displayLine["String"], "Code":displayLine["Code"]})

        self.displayLine = 0
        