# import TK
import sys
import time
import turtle
from random import randint
from random import random
import math

global dbg
global hitSmall
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
def findIntersect(angle, sqsiz, smsqsiz):
    global hitSmall
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
    checkhv = False
    if checkhv:
        if angcos == 0 and angsin > 0:
            return(xOrig, sqsiz)
        elif angcos == 0 and angsin < 0:
            return(xOrig, 0)
        elif angsin == 0 and angcos > 0:
            return(sqsiz, yOrig)
        elif angsin == 0 and angcos < 0:
            return(0, yOrig)
    # general intersection finder
    # turn off updates
    scr.tracer(0,0)
    t.penup()
    t.hideturtle()
    t.setheading(angle)
    hitsmall = True
    oldx = xOrig
    oldy = yOrig
    while True:
        t.forward(1)
        (x,y) = t.pos()
        
        # small square stuff
        smlo = sqsiz/2 - smsqsiz/2
        smhi = sqsiz/2 + smsqsiz/2
        smleft = smlo
        smright = smhi
        hitSmall = True
        # print(x,y)
        if y >= smlo >= oldy and smleft <= x <= smright:
            y = smlo
            break
        if y <= smhi <= oldy and smleft <= x <= smright:
            y = smhi
            break
        if x >= smleft >= oldx and smlo <= y <= smhi:
            x = smleft
            break
        if x <= smright <= oldx and smlo <= y <= smhi:
            x = smright
            break
        
        # boundary square stuff
        hitSmall = False
        if x >= sqsiz:
            x = sqsiz
            break
        if x <= 0:
            x = 0
            break
        if y >= sqsiz:
            y = sqsiz
            break
        if y <= 0:
            y = 0
            break
        oldx = x
        oldy = y

    if hitSmall:
        print("hit small", x, y, oldx, oldy)
        # sys.exit()
    t.goto(posOrig)
    scr.tracer(1,0)
    t.pendown()
    t.showturtle()
    return (x,y)

    
#root = TK.Tk()
#cv1 = TK.Canvas(root, width=300, height=300, bg="#ddffff")
scr = turtle.Screen()
t = turtle.RawTurtle(scr) 
t.speed(0)
scr.colormode(255)
dbgprint(scr.mode())
sqsiz = 300
drawSquare(sqsiz)
t.penup()
smsqsiz = 40
t.goto(sqsiz/2 - smsqsiz/2, sqsiz/2 - smsqsiz/2)

t.pendown()
drawSquare(smsqsiz)
xStart = 210
yStart = 50
t.pencolor("red")
t.setpos(xStart, yStart)
t.pencolor("black")
side = 0

# headTest = float(input("degrees?").rstrip())
# for headTest in [180]:
scr.title("Testing...")
dbg = True
hitSmall = False
for headTest in [110, 80, 30, 160, 210, 260, 280, 340, 270, 0, 90,  180]:
    t.setheading(headTest)
    dbgprint('Computing for %d' % headTest)
    pos = findIntersect(headTest, sqsiz, smsqsiz)
    dbgprint('for %d, pos is %s, hitSmall is %s' % (headTest, pos, hitSmall))
    t.pendown()
    t.goto(pos)
    t.penup()
    t.setpos(xStart, yStart)
    # time.sleep(3)
#t.goto(sqsiz, y)
time.sleep(5)

t.clear()
t.penup()
t.goto(0, 0)
t.setheading(0)
t.pendown()
drawSquare(sqsiz)
t.penup()
smsqsiz = 40
t.goto(sqsiz/2 - smsqsiz/2, sqsiz/2 - smsqsiz/2)
t.pendown()
drawSquare(smsqsiz)
t.penup()
t.goto(0, 0)
t.pendown()

scr.title("Bouncing")
dbg = False
newhead = random() * 90
randerr = True
t.pendown()
t.speed(10)
while True:
    t.setheading(newhead)
    pos = findIntersect(newhead, sqsiz, smsqsiz)
    if pos == (None, None):
        continue
    t.goto(pos)
    if False:
        newhead = random() * 360
    else:
        (x, y) = pos
        if x == sqsiz or hitSmall and x == sqsiz/2 + smsqsiz/2:
            newhead = 180 - newhead
        elif y >= sqsiz  or hitSmall and y == sqsiz/2 + smsqsiz/2:
            newhead = 360 - newhead
        elif x <= 0 or hitSmall and x == sqsiz/2 - smsqsiz/2:
            newhead = 180 - newhead
        elif y <= 0 or hitSmall and y == sqsiz/2 - smsqsiz/2:
            newhead = 360 - newhead
        if randerr:
            newhead = newhead + (random()*5 - 2.5)
            
turtle.done()

