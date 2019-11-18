import turtle
from random import randint

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
            
skk = turtle.Turtle() 
skk.speed(9)
drawSquare(100)
skk.setpos(0,0)

for n in range(200):
    d = randint(0, 360)
    skk.setheading(d)
    # print(skk.pos())
    # go forward until meet boundary
    lastpos = skk.pos()
    while inBounds(100):
        lastpos = skk.pos()
        skk.forward(3)

    skk.setpos(lastpos)


turtle.done()

