from Tkinter import *
from PIL import Image
from PIL import ImageTk

master = Tk()
master.minsize(1000,1000)
master.geometry("1100x1100")

def callback():
    print "click!"


photo=PhotoImage(file="/home/tom/Downloads/like.png")
b = Button(master,image=photo, command=callback, height=1000, width=1000, text='OK', compound=LEFT)
b.pack()

mainloop()
