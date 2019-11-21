# import TK
import sys
import turtle
from random import randint
from random import random
import math

global dbg
dbg = False

def dbgprint(*args):
    if dbg:
        print(args)
    
def drawSquare(siz):
    for n  in range(4):
        t.forward(siz)
        t.left(90)
        # print(t.pos())

# These use y-y1/x-x1 = m
def solveForX(posOrig, m, yNew):
    (xOrig, yOrig) = posOrig
    if m == 0:
        return math.inf
    x = (yNew - yOrig)/m + xOrig
    return x if x >= 0 and x <= sqsiz else None
    
def solveForY(posOrig, m, xNew):
    (xOrig, yOrig) = posOrig
    y = (xNew - xOrig) * m + yOrig
    return y if  y >= 0 and y <= sqsiz else None

# find the intersection if any with the sqsiz boundary,
# given the current position and angle
def findIntersect(angle, sqsiz):
    posOrig = t.pos()
    dbgprint("posOrig is ", posOrig)
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
    
    dbgprint('slope=%f, sin=%f, cos=%f'% (m, angsin, angcos))

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
        dbgprint("yright=", yright)
        yleft = solveForY(posOrig, m, 0)
        dbgprint("yleft=", yleft)
        # calculate x intersect with y==sqsiz and y == 0
        xtop = solveForX(posOrig, m, sqsiz)
        dbgprint("xtop=", xtop)
        xbot = solveForX(posOrig, m, 0)
        dbgprint("xbot=", xbot)
        if angcos > 0 and yright is not None:
            return (sqsiz, yright)
        elif angcos < 0 and yleft is not None:
            return (0, yleft)
        elif angsin > 0 and xtop is not None:
            return (xtop, sqsiz)
        elif angsin < 0 and xbot is not None:
            return (xbot, 0)
        else:
            return (None, None)

    
    
#root = TK.Tk()
#cv1 = TK.Canvas(root, width=300, height=300, bg="#ddffff")
scr = turtle.Screen()
t = turtle.RawTurtle(scr) 
t.speed(0)
scr.colormode(255)
dbgprint(scr.mode())
sqsiz = 300
drawSquare(sqsiz)
xStart = 250
yStart = 50
t.pencolor("red")
t.setpos(xStart, yStart)
t.pencolor("black")
side = 0

# headTest = float(input("degrees?").rstrip())
# for headTest in [180]:
scr.title("Testing...")
for headTest in [30, 80, 110, 160, 210, 260, 280, 340, 270, 0, 90,  180]:
    t.setheading(headTest)
    dbgprint('Computing for %d' % headTest)
    pos = findIntersect(headTest, sqsiz)
    dbgprint('for %d, pos is' % headTest, pos)
    t.pendown()
    t.goto(pos)
    t.penup()
    t.setpos(xStart, yStart)
#t.goto(sqsiz, y)

t.clear()
t.penup()
t.goto(0, 0)
t.setheading(0)
t.pendown()
drawSquare(sqsiz)

scr.title("Bouncing")
newhead = random() * 90
randerr = True
t.pendown()
t.speed(10)
while True:
    t.setheading(newhead)
    pos = findIntersect(newhead, sqsiz)
    if pos == (None, None):
        continue
    t.goto(pos)
    if False:
        newhead = random() * 360
    else:
        (x, y) = t.pos()
        if x == sqsiz:
            newhead = 180 - newhead
        elif y == sqsiz:
            newhead = 360 - newhead
        elif x == 0:
            newhead = 180 - newhead
        elif y == 0:
            newhead = 360 - newhead
        if randerr:
            newhead = newhead + (random()*5 - 2.5)
            
turtle.done()

