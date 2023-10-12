import copy
from GameData.World.Room import Room

class Area:

    def __init__(self, num, name):
        self.num = num
        self.roomList = []
        self.size = [0, 0]
        
        self.name = name

        self.flavorTextTickMax = 400
        self.flavorTextTick = 0

    def update(self, console):
        self.flavorTextTick += 1
        if self.flavorTextTick >= self.flavorTextTickMax:
            self.flavorTextTick = 0
            console.write("You hear some squeaking sounds.", "30w1y", True)

    def zeroCoordinates(self, galaxyList):
        def examineRoomData(currentLoc, targetRoom, examinedRoomNumList):
            self.roomList[targetRoom.room].mapCoordinates = copy.deepcopy(currentLoc)
            examinedRoomNumList.append(targetRoom.room)
            firstRoom = copy.deepcopy(targetRoom)
            for targetExitDir in ["North", "East", "South", "West"]:
                if targetExitDir != "North":
                    currentLoc = firstRoom.mapCoordinates
                    
                if targetExitDir in targetRoom.exit and targetRoom.exit[targetExitDir] != None:
                    tempArea, tempRoom, unusedDistance, unusedMessage = Room.getTargetRoomFromStartRoom(galaxyList, self, targetRoom, targetExitDir, 1, True)
                    if tempArea == self and tempRoom.room not in examinedRoomNumList:
                        if targetExitDir == "North" : currentLoc[1] -= 1
                        elif targetExitDir == "East" : currentLoc[0] += 1
                        elif targetExitDir == "South" : currentLoc[1] += 1
                        elif targetExitDir == "West" : currentLoc[0] -= 1
                        
                        examinedRoomNumList = examineRoomData(currentLoc, tempRoom, examinedRoomNumList)
                        currentLoc = copy.deepcopy(self.roomList[firstRoom.room].mapCoordinates)
                        firstRoom.mapCoordinates = copy.deepcopy(self.roomList[firstRoom.room].mapCoordinates)
                        
            return examinedRoomNumList

        # Get Map Dimensions #
        examinedRoomNumList = []
        for room in self.roomList:
            if room.room not in examinedRoomNumList:
                currentLoc = [0, 0]
                examinedRoomNumList = examineRoomData(currentLoc, room, examinedRoomNumList)
    
        # Zero Map Dimensions From Bottom-Right Corner To Top-Left Corner #
        if len(examinedRoomNumList) > 0:
            yModList = []
            currentStartIndex = 0
            maxTopLeftPoint = [0, 0]
            maxBottomRightPoint = [0, 0]
            self.size = [0, 0]
            
            for tempIndex, currentRoomNum in enumerate(examinedRoomNumList):
                currentRoom = self.roomList[currentRoomNum]
                if currentRoom.mapCoordinates[0] < maxTopLeftPoint[0] : maxTopLeftPoint[0] = currentRoom.mapCoordinates[0]
                elif currentRoom.mapCoordinates[0] > maxBottomRightPoint[0] : maxBottomRightPoint[0] = currentRoom.mapCoordinates[0]
                if currentRoom.mapCoordinates[1] < maxTopLeftPoint[1] : maxTopLeftPoint[1] = currentRoom.mapCoordinates[1]
                elif currentRoom.mapCoordinates[1] > maxBottomRightPoint[1] : maxBottomRightPoint[1] = currentRoom.mapCoordinates[1]
                
                if ((tempIndex + 1) == len(examinedRoomNumList) or (self.roomList[examinedRoomNumList[tempIndex + 1]].mapCoordinates == [0, 0])):
                    yMod = 0
                    if len(yModList) > 0:
                        for tempSize in yModList:
                            yMod += (tempSize + 1)

                    for tempRoomNum in examinedRoomNumList[currentStartIndex:tempIndex + 1]:
                        tempRoom = self.roomList[tempRoomNum]
                        tempRoom.mapCoordinates[0] += abs(maxTopLeftPoint[0])
                        tempRoom.mapCoordinates[1] += abs(maxTopLeftPoint[1]) + yMod
                        if tempRoom.mapCoordinates[0] > self.size[0] : self.size[0] = tempRoom.mapCoordinates[0]
                        if tempRoom.mapCoordinates[1] > self.size[1] : self.size[1] = tempRoom.mapCoordinates[1]
                    yModList.append(abs(maxTopLeftPoint[1]) + 1 + abs(maxBottomRightPoint[1]))
                    currentStartIndex = tempIndex + 1
                    maxTopLeftPoint = [0, 0]
                    maxBottomRightPoint = [0, 0]
                    
            self.size[0] += 1
            self.size[1] += 1
