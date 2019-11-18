# import TK
import turtle
from random import randint
from random import random

def drawSquare(siz):
    for n  in range(4):
        skk.forward(siz)
        skk.left(90)
        print(skk.pos())

def inBounds(siz):
    x = skk.xcor()
    y = skk.ycor()
    # print(x,y)
    if x >= 0 and x <= siz and y >= 0 and y <= siz:
        return True
    else:
        return False
            
#root = TK.Tk()
#cv1 = TK.Canvas(root, width=300, height=300, bg="#ddffff")
scr = turtle.Screen()
skk = turtle.RawTurtle(scr) 
skk.speed(0)
scr.colormode(255)
print(scr.mode())
sqsiz = 300
drawSquare(sqsiz)
skk.setpos(0,0)
side = 0

#skk.begin_fill()
for m in range(2):
    for n in range(50):
        # pick a random side
        while True:
            newside = randint(0, 3)
            if newside != side and newside % 2 == m:
                break
            
        side = newside
        
        # gen random x y in case needed later
        randx = random() * sqsiz
        randy = random() * sqsiz
        if newside == 2:
            randx = sqsiz - skk.xcor()
            skk.pendown()
        elif newside == 3:
            randy = sqsiz - skk.ycor()
            skk.pendown()
        else:
            skk.penup()
        if newside == 0:
            x, y = randx, 0
        elif newside == 1:
            x, y = sqsiz, randy
        elif newside == 2:
            x, y = randx, sqsiz
        elif newside == 3:
            x, y = 0, randy
        newhead = skk.towards(x, y)
        skk.setheading(newhead)
        skk.color(randint(0,255), randint(0,255), randint(0,255))
        skk.setpos(x, y)

#skk.end_fill()

turtle.done()

