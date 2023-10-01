from Components.Utility import appendKeyList

class Mob:

    def __init__(self, num, galaxy, system, planet, area, room, spaceship):
        self.num = num

        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.area = area
        self.room = room
        self.spaceship = spaceship

        self.prefix = "A"
        self.name = {"String":"Debug Mob", "Code":"9w"}
        self.roomDescription = {"String":"is standing here.", "Code":"16w1y"}
        self.keyList = []

        self.loadMob(num)

    def loadMob(self, num):
        if num == 1:
            self.name = {"String":"Robotic Greeter Droid", "Code":"21w"}
        elif num == 2:
            self.name = {"String":"Mummy", "Code":"5w"}
        elif num == 3:
            self.name = {"String":"Reptoid", "Code":"7w"}
        elif num == 4:
            self.name = {"String":"Tall Droid", "Code":"10w"}

        # Create Key List #
        appendKeyList(self.keyList, self.name["String"].lower())

    def lookDescription(self, console):
        console.lineList.insert(0, {"Blank": True})
        console.lineList.insert(0, {"String": "You see nothing special.", "Code":"23w1y"})
