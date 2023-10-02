import pygame, traceback
from pygame import *
from Components.Utility import writeColor
from Components.Utility import writeCrashReport

# Input Bar Width (Characters) - 56 #
# Character Size - [10, 18] #

class InputBar:

    def __init__(self):
        rectSize = [600, 22]
        self.surface = pygame.Surface(rectSize)
        self.font = pygame.font.Font("../Assets/Fonts/CodeNewRomanB.otf", 18)

        self.input = ""
        self.inputBlinkerTimer = 0

        self.previousInputList = []
        self.previousInputIndex = -1

        self.inputList = []
        self.inputListTimer = 999

    def processInput(self, keyName, game):
        if keyName == "up":
            if game.keyboard.control == False and self.previousInputIndex < len(self.previousInputList) - 1:
                self.previousInputIndex += 1
                self.input = self.previousInputList[self.previousInputIndex]
                self.inputBlinkerTimer = 0

        elif keyName == "down":
            if game.keyboard.control == False and self.previousInputIndex > -1:
                self.previousInputIndex -= 1
                self.inputBlinkerTimer = 0
                if self.previousInputIndex > -1:
                    self.input = self.previousInputList[self.previousInputIndex]
                else:
                    self.input = ""            

        elif keyName == "return":
            if len(self.input) > 0 and len(self.inputList) == 0:
                self.input = self.input.strip()
                if len(self.input) > 0:
                    try:
                        if len(self.previousInputList) == 0 or self.input != self.previousInputList[0]:
                            self.previousInputList.insert(0, self.input)
                            if len(self.previousInputList) > 20:
                                self.previousInputList = self.previousInputList[0:20]
                        game.processInputBarCommand(self.input)
                        game.console.displayLine = 0
                    except Exception as error:
                        writeCrashReport(traceback.format_exc(), self.input, game.player)
                        print(traceback.format_exc())
                        raise SystemExit
                    
                self.input = ""
                self.previousInputIndex = -1

        elif keyName in game.keyboard.keys:
            targetKey = game.keyboard.keys[keyName]
            if game.keyboard.shift and targetKey in game.keyboard.shiftKeys:
                targetKey = game.keyboard.shiftKeys[targetKey]

            self.input = self.input + targetKey

    def update(self, game):
        if len(self.inputList) > 0:
            self.inputListTimer += 1
            if self.inputListTimer >= 3:
                self.inputListTimer = 0
                game.processInputBarCommand(self.inputList[0])
                game.console.displayLine = 0
                del self.inputList[0]

        if len(self.input) > 0 and game.keyboard.backspaceTick == 0:
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
