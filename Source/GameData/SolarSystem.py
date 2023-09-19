class SolarSystem:

    def __init__(self):
        self.name = {"String":"", "Code":""}
        self.planetList = []

    def update(self, galaxyList, player, console):
        for planet in self.planetList:
            planet.update(galaxyList, player, console)
