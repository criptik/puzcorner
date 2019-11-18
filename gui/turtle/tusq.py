import turtle  

def drawSquare(siz):
    for n  in range(4):
        skk.forward(siz)
        skk.left(90)
    
def drawLoop(steps, siz):
    for n in range(steps):
        if n % 2 == 1 :
            skk.color("red", "blue")  # Blue is the fill color
        else:
            skk.color("blue", "red")  # Red is the fill color
            
        skk.down()
        skk.begin_fill()
        drawSquare(siz)
        skk.end_fill()
        # skk.up()
        skk.forward(360/steps)
        skk.right(360/steps)
        # skk.stamp()
    

skk = turtle.Turtle() 
skk.speed(0)
print(skk.speed())
    
drawLoop(36, 100)

turtle.done()

