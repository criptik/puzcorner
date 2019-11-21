import turtle
import time

scr = turtle.Screen()
t = turtle.RawTurtle(scr)
t.speed(0)
print(t.speed())

siz = 400
t.setheading(90)
t.penup()
t.goto(-200,100)
t.pendown()
pts = 5
while pts < 15:
    t.clear()
    list = []
    scr.title('%d' % pts)
    t.hideturtle()
    t.penup()
    for n in range(pts):
        t.right(360/pts)
        t.forward(4*360/pts)
        list.append(t.pos())
    p1index = 0
    for p1 in list:
        # print("p1:", p1, "list:", list[p1index+1:])
        for p2 in list[p1index+1:]:
            t.hideturtle()
            t.goto(p1)
            t.showturtle()
            t.pendown()
            t.goto(p2)
            t.hideturtle()
        p1index = p1index + 1
        
    time.sleep(1)
    pts = pts + 1
    
turtle.done()

