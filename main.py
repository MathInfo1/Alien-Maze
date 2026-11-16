from my_display import *
from alien_maze import *

myDisplay = Display(18, 19, 16, 17, 22, 21, 13, "landscape")
myDisplay.drawRect(0, 0, 480, 320, (132, 232, 255))

myGame = AlienMaze(myDisplay, None)
# myGame.addRect(-100, -100, 81.6, 1, 1, 0, (255, 0, 0))
# myGame.addRect(-1, -1, -1, 50, 50, 20, (0, 0, 255))
# myGame.addRect(-2, -2, 0, 2, 9, 5, (255, 0, 0))
# myGame.addRect(3, 8, 0, 5, 1, 4, (0, 0, 255))

myGame.addRect(-2, 2, 0, 2, 2, 2, (255, 0, 0))
myGame.addRect(1, 1, 0, 1, -1, 3, (0, 0, 255))
myGame.addRect(-3, 3, 0, -3, -2, 5, (0, 255, 0))
myGame.addRect(-3, -1, 0, 2, -1, 4, (255, 255, 0))

for i in range(36):
    myGame.visibleObjects()
    print(myGame.dir)
    myGame.dir -= 10
