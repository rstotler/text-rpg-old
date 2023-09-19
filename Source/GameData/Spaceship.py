class Spaceship:
    numCount = 0

    def __init__(self, galaxy, system, planet):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.num = Spaceship.generateNum()

        self.name = {"String":"", "Code":""}
        self.keyList = []
        self.areaList = []

        self.hatchStatus = "Open"
        self.hatchPassword = None
        self.hatchLocation = [0, 0]

    def getRoom(self, area, room):
        if area <= len(self.areaList) and \
        room <= len(self.areaList[area].roomList):
            return self.areaList[area].roomList[room]
        return None

    @staticmethod
    def generateNum():
        Spaceship.numCount += 1
        return Spaceship.numCount
