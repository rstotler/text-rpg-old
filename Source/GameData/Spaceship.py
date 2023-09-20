class Spaceship:
    numCount = 0

    def __init__(self, galaxy, system, planet, hatchPassword=None, hatchLocation=[0, 0], exitList=[[0, 0]]):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.num = Spaceship.generateNum()

        self.name = {"String":"", "Code":""}
        self.keyList = []
        self.areaList = []
        self.exitList = exitList

        self.hatchPassword = hatchPassword
        self.hatchLocation = hatchLocation

        self.landedLocation = None

    def getRoom(self, area, room):
        if area <= len(self.areaList):
            if isinstance(room, int) and room <= len(self.areaList[area].roomList):
                return self.areaList[area].roomList[room]

        return None

    @staticmethod
    def generateNum():
        Spaceship.numCount += 1
        return Spaceship.numCount
