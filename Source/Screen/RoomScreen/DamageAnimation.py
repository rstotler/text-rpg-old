import math
from Components.Utility import writeOutline

class DamageAnimation:

    def __init__(self, name, drawLoc, mobImageHeight, font):
        self.name = name
        self.drawLoc = drawLoc
        self.mobImageHeight = mobImageHeight

        self.currentAnimation = "Attack Animation"
        self.currentFrame = 0
        self.frameTick = 0
        self.frameTickMax = 1
        self.damageBounceHeight = 20

        self.damageSurface = writeOutline("9999", font)

    def update(self, attackAnimation):
        self.frameTick += 1
        if self.frameTick >= self.frameTickMax:
            self.frameTick = 0
            self.currentFrame += 1
            if self.currentAnimation == "Attack Animation" and self.currentFrame >= len(attackAnimation):
                self.currentFrame = 0
                self.currentAnimation = "Damage Animation"
                self.frameTickMax = 16

    def draw(self, targetSurface, attackAnimation, roomDisplayOffset):
        if self.currentAnimation == "Attack Animation":
            drawLoc = [roomDisplayOffset[0] - (attackAnimation[0].get_width() / 2) + self.drawLoc[0], roomDisplayOffset[1] - (attackAnimation[0].get_height() / 2) + self.drawLoc[1] - (self.mobImageHeight / 1.5)]
            targetSurface.blit(attackAnimation[self.currentFrame], drawLoc)
        elif self.currentAnimation == "Damage Animation":
            yMod = (math.sin(math.radians((self.frameTick / self.frameTickMax) * 180)) * self.damageBounceHeight) * -1
            drawLoc = [roomDisplayOffset[0] - (self.damageSurface.get_width() / 2) + self.drawLoc[0], roomDisplayOffset[1] - (self.damageSurface.get_height() / 2) + self.drawLoc[1] - (self.mobImageHeight / 1.5) + yMod]
            targetSurface.blit(self.damageSurface, drawLoc)
