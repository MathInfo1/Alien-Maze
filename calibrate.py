from my_display import *

myDisplay = Display(18, 19, 16, 17, 22, 21, 13, "landscape")
myDisplay.drawRect(0, 0, 480, 320, (132, 232, 255))

order = [0, 8, 16, 64, 72, 24, 32, 40, 48, 168, 176, 184, 192, 136, 144, 152, 160, 200, 208, 56, 80, 88, 96, 104, 112, 216, 224, 232, 120, 128, 240, 248]
for i in range(len(order)): order.insert(i * 2 + 1, order[i * 2] + 4)
for i in range(0, 256, 8):
    myDisplay.drawRect(i, 0, 8, 300, (order[i // 8], 0, 0))
    inpt = input("Move: ")
    if inpt:
        k = i
        while inpt:
            k -= 1
            order[k], order[k+1] = order[k+1], order[k]
            myDisplay.drawRect(k, 0, 8, 300, (order[k // 8], 0, 0))
            myDisplay.drawRect(k + 1, 0, 8, 300, (order[(k + 1) // 8], 0, 0))
            inpt = input("Still?: ")
            if inpt == "q":
                order[k], order[k+1] = order[k+1], order[k]
                myDisplay.drawRect(k, 0, 8, 300, (order[k // 8], 0, 0))
                myDisplay.drawRect(k + 1, 0, 8, 300, (order[(k + 1) // 8], 0, 0))
                inpt = input("Still?: ")
