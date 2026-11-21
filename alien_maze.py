from math import sqrt, sin, cos, atan2, degrees, radians
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
        self.screen = [[] for i in range(480)]
        self.drawScreen()

    def addRect(self, x0, y0, z0, x1, y1, z1, color):
        self.objects.append([color, (x0, y0, z0), (x0, y0, z1), (x1, y1, z1), (x1, y1, z0)])

    def drawScreen(self):
        self.display.setWindow(0, 0, 319, 479)

        self.display.cs.value(0)
        self.display.dc.value(0)
        self.display.spi.write(b'\x2C')
        self.display.dc.value(1)
        for i in self.screen:
            for x in i:
                color = bytes([convertColor(x[2] // 256 ** 2), convertColor((x[2] // 256) % 256), convertColor(x[2] % 256)])
                #print(x, color)
                length = x[1] - x[0] + 1
                while length > 0:
                    chunk = min(length, 100)
                    self.display.spi.write(color * chunk)
                    length -= chunk

        self.display.cs.value(1)

    def addLine(self, x, y1, y2, color, dist): # AI-generated function
        y1, y2 = int(min(y1, y2)), int(max(y1, y2))

        if y2 < 0 or y1 > 319:
            return

        y1 = max(0, y1)
        y2 = min(319, y2)

        color = color[0] * 65536 + color[1] * 256 + color[2]

        column = self.screen[x]

        # Collect all segment boundaries
        points = [y1, y2 + 1]

        for start, end, c, d in column:
            points.append(start)
            points.append(end + 1)

        points.sort()

        result = []
        last = None

        for j in range(len(points) - 1):
            start = points[j]
            end = points[j + 1] - 1

            if start > end:
                continue

            # Existing segment covering this range
            old = None
            for s, e, c, d in column:
                if s <= start and e >= end:
                    old = (s, e, c, d)
                    break

            # Is the new line covering this range?
            new_visible = y1 <= start and y2 >= end

            if new_visible and (old is None or dist < old[3]):
                segment = (start, end, color, dist)
            elif old is not None:
                segment = (start, end, old[2], old[3])
            else:
                continue

            # Merge consecutive identical segments
            if result and result[-1][1] + 1 == segment[0] and result[-1][2:] == segment[2:]:
                result[-1] = (result[-1][0], segment[1], segment[2], segment[3])
            else:
                result.append(segment)

        self.screen[x] = result

    def createDrawPoints(self):
        for i in range(480):
            self.screen[i] = [(0, 319, 0x84e8ff, 200)]

        for object in self.objects:
            dx1, dy1, dx2, dy2 = object[1][0] - self.pos[0], object[1][1] - self.pos[1], object[3][0] - self.pos[0], object[3][1] - self.pos[1]
            angle1 = (self.dir - degrees(atan2(dy1, dx1))) % 360
            angle2 = (self.dir - degrees(atan2(dy2, dx2))) % 360
            dist = max(sqrt(dx1 ** 2 + dy1 ** 2), sqrt(dx2 ** 2 + dy2 ** 2))
            # print(angle1, angle2)
            if angle1 == angle2: continue
            if angle1 < (self.fovH / 2) or angle1 > (360 - self.fovH / 2) or angle2 < (self.fovH / 2) or angle2 > (360 - self.fovH / 2): 
                for x in range(480):
                    angle = self.dir + self.fovH / 2 - x * self.fovH / 480
                    try:
                        r = (dy1 * cos(radians(angle)) - dx1 * sin(radians(angle))) / ((dx2 - dx1) * sin(radians(angle)) - (dy2 - dy1) * cos(radians(angle)))
                        s = (dy1 * (dx2 - dx1) - dx1 * (dy2 - dy1)) / ((dx2 - dx1) * sin(radians(angle)) - (dy2 - dy1) * cos(radians(angle)))
                    except ZeroDivisionError as e:
                        print(x, e)
                    if 0 <= r <= 1 and s > 0:
                        dx3, dy3 = dx1 + r * (dx2 - dx1), dy1 + r * (dy2 - dy1)
                        dist = sqrt(dx3 ** 2 + dy3 ** 2)
                        angleV1 = degrees(atan2(object[1][2] - self.pos[2], dist))
                        angleV2 = degrees(atan2(object[2][2] - self.pos[2], dist))

                        py1 = (self.fovV / 2 - angleV1) / self.fovV * 319
                        py2 = (self.fovV / 2 - angleV2) / self.fovV * 319
                        colorP = 0.6 + 0.4 * (1 - dist / 30)
                        color = (int(colorP * object[0][0]), int(colorP * object[0][1]), int(colorP * object[0][2]))
                        self.addLine(x, py1, py2, color, dist)
                continue
            if angle1 > angle2 and (degrees(atan2(dy1, dx1)) - degrees(atan2(dy2, dx2))) % 360 < 180: 
                dx1, dy1, dx2, dy2 = dx2, dy2, dx1, dy1
                angle1, angle2 = angle2, angle1
            if angle1 < angle2:
                if (degrees(atan2(dy2, dx2)) - degrees(atan2(dy1, dx1))) % 360 < 180:
                    for x in range(480):
                        angle = self.dir + self.fovH / 2 - x * self.fovH / 480
                        s = (dy1 * (dx2 - dx1) - dx1 * (dy2 - dy1)) / ((dx2 - dx1) * sin(radians(angle)) - (dy2 - dy1) * cos(radians(angle)))
                        
                        dx3, dy3 = s * cos(angle), s * sin(angle)
                        dist = sqrt(dx3 ** 2 + dy3 ** 2)
                        angleV1 = degrees(atan2(object[1][2] - self.pos[2], dist))
                        angleV2 = degrees(atan2(object[2][2] - self.pos[2], dist))

                        py1 = (self.fovV / 2 - angleV1) / self.fovV * 319
                        py2 = (self.fovV / 2 - angleV2) / self.fovV * 319
                        colorP = 0.6 + 0.4 * (1 - dist / 30)
                        color = (int(colorP * object[0][0]), int(colorP * object[0][1]), int(colorP * object[0][2]))
                        self.addLine(x, py1, py2, color, dist)
        self.drawScreen()
