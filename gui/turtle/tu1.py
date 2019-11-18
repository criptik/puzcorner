import turtle  
skk = turtle.Turtle() 
skk.speed(0)
print(skk.speed())
    
for n in range(45):
    if n % 2 == 1 :
        skk.color("red", "blue")  # Blue is the fill color
    else:
        skk.color("blue", "red")  # Red is the fill color
        
    skk.down()
    skk.begin_fill()
    skk.circle(50)
    skk.end_fill()
    # skk.up()
    skk.forward(8)
    skk.right(8)
    # skk.stamp()

turtle.done()

