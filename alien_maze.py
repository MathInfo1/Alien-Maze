from math import sqrt, atan2, degrees
from my_display import convertColor

class AlienMaze():
    def __init__(self, display, moveInput):
        self.display = display
        self.input = moveInput
        self.pos = [0, 0, 2]
        self.dir = 90
        self.fovH = 90
        self.fovV = 60
        self.objects = []
        self.screen = []
        self.drawScreen()

    def addRect(self, x0, y0, z0, x1, y1, z1, color):
        self.objects.append([color, (x0, y0, z0), (x0, y0, z1), (x1, y1, z1), (x1, y1, z0)])

    def drawScreen(self):
        self.display.cs.value(0)
        self.display.dc.value(0)
        self.display.spi.write(b'\x2C')
        self.display.dc.value(1)

        for i in self.screen:
            for x in i:
                color = bytes([convertColor(x[2] & 0xFF0000), convertColor(x[2] & 0xFF00), convertColor(x[2] & 0xFF)])
                self.display.spi.write(color * (x[1] - x[0] + 1))

        self.display.cs.value(1)

    def addLine(self, x, y1, y2, color):
        pass

    def drawPoint(self, x, y, z, color):
        dx, dy, dz = x-self.pos[0], y-self.pos[1], z-self.pos[2]
        notZdist = sqrt(dx ** 2 + dy ** 2)
        dist = sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        angleI = (degrees(atan2(dy, dx))) % 360 - (self.dir % 360)
        angleJ = degrees(atan2(dz, notZdist))

        px = (self.fovH / 2 - angleI) / self.fovH * 479
        py = (self.fovV / 2 - angleJ) / self.fovV * 319
        colorP = 0.6 + 0.4 * (1 - notZdist / 30)
        shadedColor = (round(color[0] * colorP), round(color[1] * colorP), round(color[2] * colorP))

        return (px, py, shadedColor, dist)

    
    def createDrawPoints(self):
        self.screen = [[(0, 319, 0x84e8ff, 200)] for x in range(480)]

        for object in self.objects:
            dx1, dy1, dx2, dy2 = object[1][0] - self.pos[0], object[1][1] - self.pos[1], object[3][0] - self.pos[0], object[3][1] - self.pos[1]
            angle1 = (self.dir - degrees(atan2(dy1, dx1))) % 360
            angle2 = (self.dir - degrees(atan2(dy2, dx2))) % 360
            dist = max(sqrt(dx1 ** 2 + dy1 ** 2), sqrt(dx2 ** 2 + dy2 ** 2))
            print(angle1, angle2)
            if angle1 == angle2: continue
            if angle1 < (self.fovH / 2) or angle1 > (360 - self.fovH / 2) or angle2 < (self.fovH / 2) or angle2 > (360 - self.fovH / 2): 
                pass
            if angle1 < angle2:
                if (degrees(atan2(dy2, dx2)) - degrees(atan2(dy1, dx1))) % 360 < 180: 
                    for x in range(480):
                        pass
            else:
                if (degrees(atan2(dy1, dx1)) - degrees(atan2(dy2, dx2))) % 360 < 180: 
                    return True, dist

        self.drawScreen()
