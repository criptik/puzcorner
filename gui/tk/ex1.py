from Tkinter import *

master = Tk()
master.minsize(300,100)

def callback():
    print "click!"

b = Button(master, text="OK", command=callback)
b.pack()

mainloop()
