import math
from GameData.Room import Room

class Planet:

    def __init__(self, galaxy, system, planet, distanceFromSun, minutesInDay, minutesInYear):
        self.galaxy = galaxy
        self.system = system
        self.planet = planet

        self.name = {"String":"", "Code":""}
        self.areaList = []

        self.type = "Planet"
        self.location = [0, 0]
        self.distanceFromSun = distanceFromSun
        self.orbit = "Counter Clockwise"
        self.axialTilt = 0

        self.minutesInDay = minutesInDay
        self.minutesInYear = minutesInYear

        self.currentMinutesInDay = 0
        self.currentMinutesInYear = 0

        self.dawnPercent = 0; self.sunrisePercent = 0; self.noonPercent = 0; self.duskPercent = 0; self.sunsetPercent = 0
        self.dawnMessage = False; self.sunriseMessage = False; self.noonMessage = False; self.duskMessage = False; self.sunsetMessage = False

    def update(self, galaxyList, player, console):
        self.currentMinutesInDay += 1
        self.currentMinutesInYear += 1

        # Sunrise/Sunset Messages #
        if self.type == "Planet" and self.galaxy == player.galaxy and self.system == player.system and self.planet == player.planet:
            dayPercent = 0.0
            if self.minutesInDay != 0:
                dayPercent = self.currentMinutesInDay / self.minutesInDay

            if dayPercent >= self.dawnPercent and self.dawnMessage == False:
                self.dawnMessage = True
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"The sky begins to lighten.", "Code":"4w1dc2ddc11w1dw6ddw1y"})
            elif dayPercent >= self.sunrisePercent and self.sunriseMessage == False:
                self.sunriseMessage = True
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"The sun rises over the horizon.", "Code":"4w1dy2ddy16w1dw6ddw1y"})
            elif dayPercent >= self.noonPercent and self.noonMessage == False:
                self.noonMessage = True
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"It is noon.", "Code":"10w1y"})
            elif dayPercent >= self.duskPercent and self.duskMessage == False:
                self.duskMessage = True
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"The sun begins to set.", "Code":"4w1dy2ddy11w1dw2ddw1y"})
            elif dayPercent >= self.sunsetPercent and self.sunsetMessage == False:
                self.sunsetMessage = True
                console.lineList.insert(0, {"Blank": True})
                console.lineList.insert(0, {"String":"The sun sinks beyond the horizon.", "Code":"4w1dy2ddy18w1dw6ddw1y"})

        if self.currentMinutesInDay % 60 == 0:
            self.updateLocation()

        if self.currentMinutesInDay >= self.minutesInDay:
            self.currentMinutesInDay = 0
            self.updateNightDayTimers()

    def updateNightDayTimers(self):
        yearRatio = 0
        if self.minutesInYear != 0:
            yearRatio = math.cos(math.radians(((self.currentMinutesInYear) / (self.minutesInYear)) * 360))
        ratio = ((self.axialTilt / 100) * yearRatio) * (self.minutesInDay / 2)
        nightMinutes = self.minutesInDay - ((self.minutesInDay / 2) - ratio)
        
        self.dawnPercent = (nightMinutes / 2.2) / self.minutesInDay
        self.sunrisePercent = (nightMinutes / 1.86) / self.minutesInDay
        self.noonPercent = .5
        self.duskPercent = ((nightMinutes / 2.15) + (self.minutesInDay - nightMinutes)) / self.minutesInDay
        self.sunsetPercent = ((nightMinutes / 1.85) + (self.minutesInDay - nightMinutes)) / self.minutesInDay

        self.dawnMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.dawnPercent
        self.sunriseMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.sunrisePercent
        self.noonMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.noonPercent
        self.duskMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.duskPercent
        self.sunsetMessage = (self.currentMinutesInDay / self.minutesInDay) >= self.sunsetPercent

    def updateLocation(self):
        x = self.distanceFromSun
        y = 0
        orbitMod = 1
        if self.orbit == "Clockwise":
            orbitMod = -1

        if self.minutesInYear != 0:
            x = math.cos(math.radians((self.currentMinutesInYear / self.minutesInYear) * 360)) * self.distanceFromSun
            y = ((math.sin(math.radians((self.currentMinutesInYear / self.minutesInYear) * 360)) * self.distanceFromSun) / 1.5) * orbitMod
        
        self.location = [x, y]

    def displayTime(self, console):
        hoursString = str(int(self.currentMinutesInDay / 60))
        if self.name["String"] in ["Earth", "Proto Earth"]:
            if hoursString == "0":
                hoursString = "12"
            elif int(hoursString) > 12:
                hoursString = str(int(hoursString) - 12)

        minutesString = str(int(self.currentMinutesInDay % 60))
        if len(minutesString) == 1:
            minutesString = "0" + minutesString

        if self.name["String"] in ["Earth", "Proto Earth"]:
            amPmString = " A.M"
            if self.currentMinutesInDay >= self.minutesInDay / 2:
                amPmString = " P.M"
            amPmCode = "2w1y1w"
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"The time is " + str(hoursString) + ":" + str(minutesString) + amPmString + ".", "Code":"12w" + str(len(hoursString)) +"w1y" + str(len(minutesString)) + "w" + amPmCode + "1y"})
        else:
            console.lineList.insert(0, {"Blank": True})
            console.lineList.insert(0, {"String":"The time is " + str(hoursString) + ":" + str(minutesString) + ".", "Code":"12w" + str(len(hoursString)) +"w1y" + str(len(minutesString)) + "w1y"})

    def dayCheck(self):
        if self.type == "Star":
            dayCheck = True
        else:
            dayCheck = (self.currentMinutesInDay / self.minutesInDay) >= self.dawnPercent and (self.currentMinutesInDay / self.minutesInDay) < self.sunsetPercent 

        return dayCheck
        