# import TK
import sys
import time
import turtle
from random import *
import math

global dbg

def dbgprint(*args):
    if dbg:
        print(args)
    
def vectorEnd(x1, y1, ang, len):
    angrad = math.radians(ang)
    angcos = math.cos(angrad)
    angsin = math.sin(angrad)
    x2 = x1 + len * angcos
    y2 = y1 + len * angsin
    return (x2, y2)

# a wall is basically a line
class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        if (x2 == x1):
            self.mw = math.inf
            self.ang = 90
        else:
            self.mw = (y2-y1)/(x2-x1)
            self.ang = math.degrees(math.atan(self.mw))

    @classmethod
    def fromVector(cls, x1, y1, ang, len):
        (x2, y2) = vectorEnd(x1, y1, ang, len)
        return cls(x1, y1, x2, y2)
            
    def __str__(self):
        return('(%d,%d) to (%d,%d), slope=%f, ang=%f' % (self.x1, self.y1, self.x2, self.y2, self.mw, self.ang))

    def x2y2(self):
        return(self.x2, self.y2)

    def containsPoint(self, x, y):
        e = 0.1
        if self.x1 < self.x2:
            xpart = self.x1-e <= x <= self.x2+e
        elif self.x1 > self.x2:
            xpart = self.x2-e <= x <= self.x1+e
        else:
            xpart = True
        if self.y1 < self.y2:
            ypart = self.y1-e <= y <= self.y2+e
        elif self.y1 > self.y2:
            ypart = self.y2-e <= y <= self.y1+e
        else:
            ypart = True
        return xpart and ypart

    def draw(self, t):
        t.penup()
        t.goto(self.x1, self.y1)
        t.pendown()
        t.pencolor("red")
        t.goto(self.x2, self.y2)
        
def genPolygonWalls(x0, y0, numsides, heading, sidelen, headingChange=None):
    a = []
    if headingChange is None:
        headingChange = 360/numsides
    a.append(Wall.fromVector(x0, y0, heading, sidelen))
    for n in range(numsides-1):
        heading = heading + headingChange
        print(heading)
        a.append(Wall.fromVector(*(a[-1].x2y2()), heading, sidelen))

    return a    

# rounding errors?
def genSquareWalls(x0, y0, heading, sidelen):
    return genPolygonWalls(x0, y0, 4, heading, sidelen)

def genTriangleWalls(x0, y0, heading, sidelen):
    return genPolygonWalls(x0, y0, 3, heading, sidelen)


# notes
# call (y2-y1)/(x2-x1) = mw

# wall equation is y=y1 + (x-x1)*mw
# turt equation is y=y0 + (x-x0)*mt
# so at intersection:
# y1 + (x-x1)*mw = y0 + mt*(x-x0)
# y1 + mw*x - x1*mw = y0 + mt*x - mt*x0
# x*(mt-mw) + mw*x1 - mt*x0 = (y1-y0)
# x = (y1-y0 - mw*x1 + mt*x0)/(mt-mw)

# special case:  wall line x=constant (vertical), so mw = inf
# then equations are x=x1 and y=(x-x0)*mt + y0
# so solve for y get:
# y = (x1-x0)*mt + y0
#
# special case 2: turang is 90 or 180 so turslope = inf
# then tur equation is x=x0
# then eqs are x=x0 (tur) and y=(x-x1)*mw + y1 (wall)
# so solve for y get:
# y = (x0-x1)*mw + y1

# example:
# wall(vert) = 300, 0, 300, 300,  turtang=30(mt=0.5), turpos=(150, 150)
# y = (300-150)*0.5 + 150 = 225

# example (turt vert):
# wall = 300, 0, 0 300, (mw=-1)  turtang=90, turpos=(60, 60)
# y = (60-300)*(-1) + 0 = 225
# y = 240 + 0 = 240

# example:
# wall = 150, 300, 300, 150  turtang=45(mt=1), turpos=(0,0)
# mw = -1
# x = (y1-y0 - mw*x1 + mt*x0)/(mt-mw)
# xint = (300-0 - (-1*150) + 1*0)/(1 - -1)
#      = 450/2 = 225
# yint = x0 + mt*x-x0 = 0 + 1*225 = 150

class World:
    def __init__(self, walls):
        self.walls = walls
        self.wallHit = None
        
    def draw(self, t):
        t.clear()
        for wall in self.walls:
            wall.draw(t)
        t.penup()

    def isRightDirection(self, x0, y0, xint, yint, angsin, angcos):
        if angcos == 0:
            rightx = (x0 == xint)
        elif angcos > 0:
            rightx = xint > x0
        else:
            rightx = xint < x0
        if angsin == 0:
            righty = (y0 == yint)
        elif angsin > 0:
            righty = yint > y0
        else:
            righty = yint < y0
        return (rightx and righty)

    def hitsEarlier(self, xint, yint, angsin, angcos):
        if self.xret is None:
            return True
        if angcos > 0:
            return xint < self.xret
        if angcos < 0:
            return xint > self.xret
        # zero cos, check sing
        if angsin > 0:
            return yint < self.yret
        if angsin < 0:
            return yint > self.yret
        return False
        
    def isValidIntersection(self, wall, x0, y0, xint, yint, angsin, angcos):
        if not wall.containsPoint(xint, yint):
            dbgprint('does not contain (%f, %f)' % (xint, yint))
            return False
        dbgprint('wall does contain (%f, %f)' % (xint, yint))
        rightDirection = self.isRightDirection(x0, y0, xint, yint, angsin, angcos)
        dbgprint('rightDirection = %s' % rightDirection)
        if not rightDirection:
            return False
        earlier = self.hitsEarlier(xint, yint, angsin, angcos)
        dbgprint('hits Earlier = %s' % earlier)
        if not earlier:
            return False
        #  if we made it this far...
        return True
    
    # find the intersection with any wall
    # given the current position and angle
    def findIntersect(self, posOrig, angle, excludeWalls=[]):
        dbgprint("posOrig is ", posOrig)
        (x0, y0) = posOrig

        rads = math.radians(angle)
        # print("rads=", rads)
        mt = math.tan(rads)
        if (angle % 180) == 90:
            mt = math.inf
        elif (angle % 180) == 0:
            mt = 0
        angsin = math.sin(rads)
        angcos = math.cos(rads)
        if abs(angcos) < 1e-15:
            angcos = 0
        if abs(angsin) < 1e-15:
            angsin = 0
        
        dbgprint('turtle slope=%f, sin=%f, cos=%f'% (mt, angsin, angcos))

        self.xret = None
        self.yret = None
        for wall in self.walls:
            if wall in excludeWalls:
                continue
            xint = None
            yint = None
            dbgprint('wall is %s' % (wall))
            # special case if wall and turtle path are parallel
            if wall.mw == mt:
                dbgprint('skipping %s, parallel to turtle' % (wall))

            # special case if wall is vertical (equation x=x1)
            elif wall.mw == math.inf:
                yint = (wall.x1 - x0) * mt + y0
                xint = wall.x1

            # special case if turtle path is vertical (equation x=x0)
            elif mt == math.inf:
                yint = (x0-wall.x1) * wall.mw + wall.y1
                xint = x0

            else:
                xint = (wall.y1 - y0 - wall.mw * wall.x1 + mt * x0)/(mt - wall.mw)
                yint = y0 + (xint - x0) * mt
                # special cases for vertical, etc.
                if wall.x1 == wall.x2:
                    xint = wall.x1
                if wall.y1 == wall.y2:
                    yint = wall.y1
                    
            # if we computed a wall turtle intersection, see if it is really on a wall
            # and also whether it is in the right turtle direction, and is earlier than any existing one
            if xint is not None:
                dbgprint('computed intersection at (%f,%f)' % (xint, yint))
            if xint is not None and self.isValidIntersection(wall, x0, y0, xint, yint, angsin, angcos):
                self.xret = xint
                self.yret = yint
                self.wallHit = wall
                    

        # having finished all walls, xret,yret should conotain the first intersect
        if self.xret is not None:
            dbgprint('returning (%f, %f)' % (self.xret, self.yret))
        posret = (self.xret, self.yret)
        return(posret)
    
    def getWallHit(self):
        return self.wallHit

# ---------- main program ----------------
scr = turtle.Screen()
t = turtle.RawTurtle(scr) 
t.shape('circle')
t.resizemode('user')
t.shapesize(0.5, 0.5)
t.speed(0)
scr.colormode(255)
mywalls = []
sqsiz = 300
smsqsiz = 50
mywalls.extend(genSquareWalls(0, 0, 0, sqsiz))
    
if True:
    mywalls.extend(genTriangleWalls(100, 100, -30, smsqsiz*4))
else:
    mywalls.append(Wall(50, 0, 50, 280))
    mywalls.append(Wall(100, 300, 100, 20))
    mywalls.append(Wall(150, 0, 150, 280))
    mywalls.append(Wall(200, 300, 200, 20))
    mywalls.append(Wall(250, 0, 250, 280))
    
for w in mywalls:
    print(w)
    
world = World(mywalls)
world.draw(t)

xStart = 25
yStart = 25
t.setpos(xStart, yStart)
t.pencolor("black")

scr.title("Testing...")
dbg = False
for headTest in [82.24861134413653, 115, 80, 30, 160, 210, 260, 280, 340, 270, 0, 90,  180]:
    t.setheading(headTest)
    dbgprint('Computing for %d' % headTest)
    pos = world.findIntersect(t.pos(), headTest)
    # dbgprint('for %d, pos is %s' % (headTest, pos))
    if True:
        t.pendown()
        t.goto(pos)
        t.penup()
    t.setpos(xStart, yStart)
    # sys.exit()

time.sleep(3)

t.clear()
t.penup()
world.draw(t)
t.pencolor("black")
t.goto(100, 50)
# sys.exit()

scr.title("Bouncing")
dbg = False
newhead = random() * 90
randerr = True
if True:
    t.pendown()
t.speed(0)
excludes = []
while True:
    t.setheading(newhead)
    pos = world.findIntersect(t.pos(), newhead, excludes)
    (posx, posy) = pos
    dbgprint(newhead, posx, posy)
    if posx == None:
        print(t.pos(), newhead, excludes, pos)
        time.sleep(10)
        sys.exit()
        continue
    t.goto(pos)
    # t.dot(5, "blue")
    
    if False:
        newhead = random() * 360
    else:
        # this only handles the horiz and vertical walls
        # will generalize later
        wallHit = world.getWallHit()
        if wallHit in mywalls[5:7]:
            pass
            
        newhead = (2 * wallHit.ang - newhead) % 360
        if randerr:
            newhead = newhead + (random()*5 - 2.5)
        # for next time, make sure we don't hit the same wall.
        excludes = [wallHit]
            
turtle.done()

