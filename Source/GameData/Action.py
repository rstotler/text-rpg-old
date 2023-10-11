import copy

class Action:

    def __init__(self, actionType, flags, maxTick=2):
        self.actionType = actionType
        self.flags = flags
        
        self.currentTick = 0
        self.maxTick = maxTick

    def update(self, console, galaxyList, player, target, messageDataList):
        self.currentTick += 1
        if self.currentTick >= self.maxTick:
            if self.actionType == "Reload":
                target.reloadCompleteAction(console, self.flags)
            elif self.actionType == "Unload":
                target.unloadCompleteAction(console, self.flags)
            elif self.actionType == "Combat Skill":
                messageDataList = target.combatSkillCompleteAction(console, galaxyList, player, self.flags, messageDataList)

        return messageDataList
