import pygame
from pygame import *
from Components.Utility import writeColor

# Console Size - [59, 38] #
# Character Size - [10, 18] #

class Console:

    def __init__(self):
        self.font = pygame.font.Font("../Assets/Fonts/CodeNewRomanB.otf", 18)
        
        rectSize = [600, 600 - 22]
        self.surface = pygame.Surface(rectSize)

        self.lineList = []

    def draw(self, window):
        self.surface.fill([5, 15, 35])

        endIndex = len(self.lineList)
        if len(self.lineList) > 38:
            endIndex = 38
        drawLoc = [5, self.surface.get_height() - 18]
        for line in self.lineList[0:endIndex]:
            if "String" in line and "Code" in line:
                writeColor(line["String"], line["Code"], drawLoc, self.font, self.surface)
            drawLoc[1] -= 18

        window.blit(self.surface, [0, 0])
