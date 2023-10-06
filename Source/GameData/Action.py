import copy

class Action:

    def __init__(self, actionType, flags):
        self.actionType = actionType
        self.flags = flags
        
        self.currentTick = 0
        self.maxTick = 2

    def update(self, console, player, target):
        self.currentTick += 1
        if self.currentTick >= self.maxTick:
            if self.actionType == "Reload":
                target.reloadCompleteAction(console, self.flags)
            elif self.actionType == "Unload":
                target.unloadCompleteAction(console, self.flags)
            elif self.actionType == "Combat Skill":
                target.combatSkillCompleteAction(console, player, self.flags)
