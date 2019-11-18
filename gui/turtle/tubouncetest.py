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
    
def findIntersect(angle, sqsiz):
    posOrig = t.pos()
    print(posOrig)
    (xOrig, yOrig) = posOrig
    rads = math.radians(angle)
    print("rads=", rads)
    m = math.tan(rads)
    print("slope=", m)
    # calculate y intersect with x==sqsiz and x==0
    yright = solveForY(posOrig, m, sqsiz)
    print("yright=", yright)
    yleft = solveForY(posOrig, m, 0)
    print("yleft=", yleft)
    # calculate x intersect with y==sqsiz and y == 0
    xtop = solveForX(posOrig, m, sqsiz)
    print("xtop=", xtop)
    xbot = solveForX(posOrig, m, 0)
    print("xbot=", xbot)
    
    return yright
    
    
#root = TK.Tk()
#cv1 = TK.Canvas(root, width=300, height=300, bg="#ddffff")
scr = turtle.Screen()
t = turtle.RawTurtle(scr) 
t.speed(0)
scr.colormode(255)
print(scr.mode())
sqsiz = 300
drawSquare(sqsiz)
t.setpos(100, 200)
side = 0

# headTest = float(input("degrees?").rstrip())
headTest = 89
t.setheading(headTest)
y = findIntersect(headTest, sqsiz)
print(y)
t.goto(sqsiz, y)

turtle.done()

