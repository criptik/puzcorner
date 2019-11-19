import turtle
import time

scr = turtle.Screen()
t = turtle.RawTurtle(scr)
t.speed(0)
print(t.speed())

siz = 400
t.setheading(0)
t.penup()
t.goto(200,0)
t.pendown()
pts = 3
while pts < 55:
    t.clear()
    scr.title('%d' % pts)
    for n in range(pts):
        t.right(180-(180/pts))
        t.forward(siz)
    time.sleep(1)
    pts = pts + 2
    
turtle.done()

