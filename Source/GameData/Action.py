import copy

class Action:

    def __init__(self, actionType, flags):
        self.actionType = actionType
        self.flags = flags
        
        self.currentTick = 0
        self.maxTick = 2

    def update(self, console, target):
        self.currentTick += 1
        if self.currentTick >= self.maxTick:
            if self.actionType == "Reload":
                target.reloadCompleteAction(console, self.flags)
            elif self.actionType == "Unload":
                target.unloadCompleteAction(console, self.flags)
            elif self.actionType == "Combat Skill":
                target.combatSkillCompleteAction(console, self.flags)

    @staticmethod
    def updateActionCommand(console, target):
        if len(target.actionList) > 0:
            target.actionList[0].update(console, target)
            if target.actionList[0].currentTick >= target.actionList[0].maxTick:
                del target.actionList[0]
