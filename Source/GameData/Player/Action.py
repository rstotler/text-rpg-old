import copy
from GameData.World.Room import Room

class Action:

    def __init__(self, actionType, flags, maxTick=2):
        self.actionType = actionType
        self.flags = flags
        
        self.currentTick = 0
        self.maxTick = maxTick

    def update(self, config, console, galaxyList, player, target, targetRoom, messageDataList):
        self.currentTick += 1
        if self.currentTick >= self.maxTick:
            if self.actionType == "Reload":
                target.reloadCompleteAction(console, self.flags)
            elif self.actionType == "Unload":
                target.unloadCompleteAction(console, self.flags)
            elif self.actionType == "Combat Skill":
                messageDataList = target.combatSkillCompleteAction(config, console, galaxyList, player, self.flags, messageDataList)
            elif self.actionType == "Stumble":
                target.stumbleCompleteAction(console, galaxyList, player, self.flags)
            elif self.actionType == "Stun":
                target.stunCompleteAction(console, galaxyList, player, self.flags)
            elif self.actionType == "Knocked Down":
                target.knockedDownCompleteAction(console, galaxyList, player, self.flags)

        return messageDataList
