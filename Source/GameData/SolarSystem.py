class SolarSystem:

    def __init__(self):
        self.planetList = []
        self.spaceshipList = []
        
        self.name = {"String":"", "Code":""}

    def update(self, galaxyList, player, console):
        for planet in self.planetList:
            planet.update(galaxyList, player, console)

    def getSpaceship(self, spaceshipNum):
        for spaceship in self.spaceshipList:
            if spaceship.num == spaceshipNum:
                return spaceship
        return None
