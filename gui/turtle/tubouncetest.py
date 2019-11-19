# import TK
import turtle
from random import randint
from random import random
import math

def drawSquare(siz):
    for n  in range(4):
        t.forward(siz)
        t.left(90)
        # print(t.pos())

def inBounds(siz):
    x = t.xcor()
    y = t.ycor()
    # print(x,y)
    if x >= 0 and x <= siz and y >= 0 and y <= siz:
        return True
    else:
        return False

# These use y-y1/x-x1 = m
def solveForX(posOrig, m, yNew):
    (xOrig, yOrig) = posOrig
    if m == 0:
        return math.inf
    x = (yNew - yOrig)/m + xOrig
    return x
    
def solveForY(posOrig, m, xNew):
    (xOrig, yOrig) = posOrig
    y = (xNew - xOrig) * m + yOrig
    return y

# find the intersection if any with the sqsiz boundary,
# given the current position and angle
def findIntersect(angle, sqsiz):
    posOrig = t.pos()
    print("posOrig is ", posOrig)
    (xOrig, yOrig) = posOrig
    rads = math.radians(angle)
    # print("rads=", rads)
    m = math.tan(rads)
    angsin = math.sin(rads)
    angcos = math.cos(rads)
    if abs(angcos) < 1e-15:
        angcos = 0
    if abs(angsin) < 1e-15:
        angsin = 0
    
    print('slope=%f, sin=%f, cos=%f'% (m, angsin, angcos))

    # horizontal or vertical directions
    if angcos == 0 and angsin > 0:
        return(xOrig, sqsiz)
    elif angcos == 0 and angsin < 0:
        return(xOrig, 0)
    elif angsin == 0 and angcos > 0:
        return(sqsiz, yOrig)
    elif angsin == 0 and angcos < 0:
        return(0, yOrig)
    else:
        # calculate the 4 possible intersects
        yright = solveForY(posOrig, m, sqsiz)
        print("yright=", yright)
        yleft = solveForY(posOrig, m, 0)
        print("yleft=", yleft)
        # calculate x intersect with y==sqsiz and y == 0
        xtop = solveForX(posOrig, m, sqsiz)
        print("xtop=", xtop)
        xbot = solveForX(posOrig, m, 0)
        print("xbot=", xbot)
        if angsin > 0 and angcos > 0:
            if yright <= sqsiz:
                return (sqsiz, yright)
            else:
                return (xtop, sqsiz)
        elif angsin > 0 and angcos < 0:
            if yleft <= sqsiz:
                return (0, yleft)
            else:
                return (xtop, sqsiz)
        elif angsin < 0 and angcos > 0:
            if yright >= 0:
                return (sqsiz, yright)
            else:
                return (xbot, 0)
        elif angsin < 0 and angcos < 0:
            if xbot >= 0:
                return (xbot, 0)
            else:
                return (0, yleft)

    
    
#root = TK.Tk()
#cv1 = TK.Canvas(root, width=300, height=300, bg="#ddffff")
scr = turtle.Screen()
t = turtle.RawTurtle(scr) 
t.speed(0)
scr.colormode(255)
print(scr.mode())
sqsiz = 300
drawSquare(sqsiz)
xStart = 150
yStart = 130
t.pencolor("red")
t.setpos(xStart, yStart)
t.pencolor("black")
side = 0

# headTest = float(input("degrees?").rstrip())
# for headTest in [180]:
for headTest in [30, 80, 110, 160, 200, 260, 280, 350, 270, 0, 90,  180]:
    t.setheading(headTest)
    print('Computing for %d' % headTest)
    pos = findIntersect(headTest, sqsiz)
    print('for %d, pos is' % headTest, pos)
    t.pendown()
    t.goto(pos)
    t.penup()
    t.setpos(xStart, yStart)
#t.goto(sqsiz, y)

turtle.done()

