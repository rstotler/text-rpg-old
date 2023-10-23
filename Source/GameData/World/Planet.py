import math, random
from GameData.World.Room import Room
from Components.Utility import *

class Planet:

    def __init__(self, galaxy, system, planet, name, type, distanceFromSun, minutesInDay, minutesInYear, axialTilt, diameter):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet
        self.areaList = []

        self.name = name
        self.keyList = []
        appendKeyList(self.keyList, self.name["String"].lower())

        self.type = type
        self.position = [0, 0]
        self.distanceFromSun = distanceFromSun
        self.orbit = "Counter Clockwise"
        self.axialTilt = axialTilt
        self.diameter = diameter

        self.minutesInDay = minutesInDay
        self.minutesInYear = minutesInYear

        self.currentMinutesInYear = 0
        self.currentMinutesInDay = 0

        self.dawnPercent = 0; self.sunrisePercent = 0; self.noonPercent = 0; self.duskPercent = 0; self.sunsetPercent = 0
        self.dawnMessage = False; self.sunriseMessage = False; self.noonMessage = False; self.duskMessage = False; self.sunsetMessage = False

        if self.type == "Planet":
            self.currentMinutesInYear = random.randrange(self.minutesInYear)
            self.currentMinutesInDay = self.currentMinutesInYear % self.minutesInDay

    def update(self, galaxyList, player, console):
        self.currentMinutesInDay += 1
        self.currentMinutesInYear += 1

        # Sunrise/Sunset Messages #
        if self.type == "Planet" and self.galaxy == player.galaxy and self.system == player.system and self.planet == player.planet:
            playerRoom = Room.exists(galaxyList, player.spaceship, player.galaxy, player.system, player.planet, player.area, player.room)
            if playerRoom != None and not (playerRoom.spaceshipObject != None and playerRoom.spaceshipObject.landedLocation == None):
                dayPercent = 0.0
                if self.minutesInDay != 0:
                    dayPercent = self.currentMinutesInDay / self.minutesInDay

                if dayPercent >= self.dawnPercent and self.dawnMessage == False:
                    self.dawnMessage = True
                    console.write("The sky begins to lighten.", "4w1dc2ddc11w1dw6ddw1y", True)
                elif dayPercent >= self.sunrisePercent and self.sunriseMessage == False:
                    self.sunriseMessage = True
                    console.write("The sun rises over the horizon.", "4w1dy2ddy16w1dw6ddw1y", True)
                elif dayPercent >= self.noonPercent and self.noonMessage == False:
                    self.noonMessage = True
                    console.write("It's noon.", "2w1y6w1y", True)
                elif dayPercent >= self.duskPercent and self.duskMessage == False:
                    self.duskMessage = True
                    console.write("The sun begins to set.", "4w1dy2ddy11w1dw2ddw1y", True)
                elif dayPercent >= self.sunsetPercent and self.sunsetMessage == False:
                    self.sunsetMessage = True
                    console.write("The sun sinks beyond the horizon.", "4w1dy2ddy18w1dw6ddw1y", True)

        self.updatePosition()
        if self.currentMinutesInDay >= self.minutesInDay:
            self.currentMinutesInDay = 0
            self.updateNightDayTimers()

    def updateNightDayTimers(self):
        yearRatio = 0
        if self.minutesInYear != 0:
            yearRatio = math.cos(math.radians(((self.currentMinutesInYear) / (self.minutesInYear)) * 360))
        ratio = ((self.axialTilt / 100.0) * yearRatio) * (self.minutesInDay / 2.50)
        nightMinutes = self.minutesInDay - ((self.minutesInDay / 1.9) - ratio)
        
        self.dawnPercent = (nightMinutes / 2.01) / self.minutesInDay
        self.sunrisePercent = (nightMinutes / 1.80) / self.minutesInDay
        self.noonPercent = .5
        self.duskPercent = ((nightMinutes / 1.94) + (self.minutesInDay - nightMinutes)) / self.minutesInDay
        self.sunsetPercent = ((nightMinutes / 1.64) + (self.minutesInDay - nightMinutes)) / self.minutesInDay

        self.dawnMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.dawnPercent
        self.sunriseMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.sunrisePercent
        self.noonMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.noonPercent
        self.duskMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.duskPercent
        self.sunsetMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.sunsetPercent

        # sunriseTime = (self.sunrisePercent * self.minutesInDay)
        # sunriseString = str(int(sunriseTime / 60)) + ":" + str(int(sunriseTime % 60))
        # sunsetTime = (self.sunsetPercent * self.minutesInDay)
        # sunsetString = str(int(sunsetTime / 60)) + ":" + str(int(sunsetTime % 60))
        # dawnTime = (self.dawnPercent * self.minutesInDay)
        # dawnString = str(int(dawnTime / 60)) + ":" + str(int(dawnTime % 60))
        # duskTime = (self.duskPercent * self.minutesInDay)
        # duskString = str(int(duskTime / 60)) + ":" + str(int(duskTime % 60))
        # print("Dawn: ", dawnString)
        # print("Sunrise: ", sunriseString)
        # print("Dusk: ", duskString)
        # print("SunSet: ", sunsetString)

    def updatePosition(self):
        x = self.distanceFromSun
        y = 0
        orbitMod = 1
        if self.orbit == "Clockwise":
            orbitMod = -1

        if self.minutesInYear != 0:
            x = math.cos(math.radians((self.currentMinutesInYear / self.minutesInYear) * 360)) * self.distanceFromSun
            y = ((math.sin(math.radians((self.currentMinutesInYear / self.minutesInYear) * 360)) * self.distanceFromSun) / 1.5) * orbitMod
        
        self.position = [x, y]

    def dayCheck(self):
        if self.type == "Star":
            dayCheck = True
        else:
            dayCheck = (self.currentMinutesInDay / self.minutesInDay) >= self.dawnPercent and (self.currentMinutesInDay / self.minutesInDay) < self.sunsetPercent 

        return dayCheck
        
    def getLandingRoomDataList(self):
        landingRoomDataList = []
        for area in self.areaList:
            for room in area.roomList:
                if "Landing Site" in room.flags:
                    landingRoomDataList.append({"Area":area, "Room":room})
        return landingRoomDataList

    def getDrawColor(self):
        if self.type == "Star":
            return [200, 150, 0]
        elif self.diameter > 10000:
            return [150, 0, 150]
        elif self.diameter > 3500:
            return [0, 0, 150]
        else:
            return [150, 0, 0]

    def getDrawRadius(self):
        if self.type == "Star":
            return 12
        elif self.diameter >= 10000:
            return 9
        elif self.diameter >= 3500:
            return 6
        else:
            return 4
