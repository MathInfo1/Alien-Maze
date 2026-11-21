from my_display import *
from alien_maze import *
from math import sin, cos, radians

myDisplay = Display(18, 19, 16, 17, 22, 21, 13, "landscape")
myDisplay.drawRect(0, 0, 319, 479, (132, 232, 255))

myGame = AlienMaze(myDisplay, None)

myGame.addRect(-2, 2, 0, 2, 2, 2, (255, 0, 0))
myGame.addRect(1, 1, 0, 1, -1, 2.5, (0, 0, 255))
myGame.addRect(-3, 3, 0, -3, -2, 5, (0, 255, 0))
myGame.addRect(-3, -1, 0, 2, -1, 4, (255, 255, 0))


while True:
    myGame.createDrawPoints()
    print(myGame.dir % 360, myGame.pos)
    cmd = input("Command: ").lower()
    if cmd == "w":
        myGame.pos[0] += round(sin(radians(myGame.dir)), 4)
        myGame.pos[1] += round(cos(radians(myGame.dir)), 4)
    elif cmd == "a":
        myGame.pos[0] += round(sin(radians(myGame.dir + 90)), 4)
        myGame.pos[1] += round(cos(radians(myGame.dir + 90)), 4)
    elif cmd == "s":
        myGame.pos[0] += round(sin(radians(myGame.dir + 180)), 4)
        myGame.pos[1] += round(cos(radians(myGame.dir + 180)), 4)
    elif cmd == "d":
        myGame.pos[0] += round(sin(radians(myGame.dir + 270)), 4)
        myGame.pos[1] += round(cos(radians(myGame.dir + 270)), 4)
    elif cmd == "j":
        myGame.dir += 30
    elif cmd == "l":
        myGame.dir -= 30
