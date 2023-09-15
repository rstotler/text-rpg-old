import pygame
from pygame import *
from Components.Utility import writeColor

# Input Bar Width (Characters) - 56 #
# Character Size - [10, 18] #

class InputBar:

    def __init__(self):
        self.font = pygame.font.Font("../Assets/Fonts/CodeNewRomanB.otf", 18)
        
        rectSize = [600, 22]
        self.surface = pygame.Surface(rectSize)

        self.input = ""
        self.inputBlinkerTimer = 0

        self.previousInputList = []
        self.previousInputIndex = -1

    def processInput(self, keyName, game):
        if keyName == "up":
            if self.previousInputIndex < len(self.previousInputList) - 1:
                self.previousInputIndex += 1
                self.input = self.previousInputList[self.previousInputIndex]
                self.inputBlinkerTimer = 0

        elif keyName == "down":
            if self.previousInputIndex > -1:
                self.previousInputIndex -= 1
                self.inputBlinkerTimer = 0
                if self.previousInputIndex > -1:
                    self.input = self.previousInputList[self.previousInputIndex]
                else:
                    self.input = ""            

        elif keyName == "return":
            if len(self.input) > 0:
                if len(self.previousInputList) == 0 or self.input != self.previousInputList[0]:
                    self.previousInputList.insert(0, self.input)
                    self.previousInputIndex = -1
                    if len(self.previousInputList) > 20:
                        self.previousInputList = self.previousInputList[0:20]

                game.processInputBarCommand(self.input)
                self.input = ""

        elif keyName in game.keyboard.keys:
            targetKey = game.keyboard.keys[keyName]
            if game.keyboard.shift and targetKey in game.keyboard.shiftKeys:
                targetKey = game.keyboard.shiftKeys[targetKey]

            self.input = self.input + targetKey

    def update(self, keyboard):
        if len(self.input) > 0 and keyboard.backspaceTick == 0:
            self.input = self.input[0:len(self.input) - 1]

    def draw(self, window):
        self.inputBlinkerTimer += 1
        if self.inputBlinkerTimer >= 60:
            self.inputBlinkerTimer = 0

        self.surface.fill([10, 30, 70])
        
        displayInput = self.input
        if len(displayInput) >= 57:
            displayInput = displayInput[-56:]
        if self.inputBlinkerTimer >= 30:
            displayInput = displayInput + "_"
        displayInput = "> " + displayInput
        labelCode = "2y" + str(len(displayInput)) + "w"
        writeColor(displayInput, labelCode, [5, 1], self.font, self.surface)

        window.blit(self.surface, [0, 600 - self.surface.get_height()])
