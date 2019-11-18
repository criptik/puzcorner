from Tkinter import *
from PIL import Image
from PIL import ImageTk

master = Tk()
master.minsize(200, 200)
# master.geometry("1100x1100")

def callback():
    print "click!"

img = Image.open("/home/tom/Downloads/like.png")
img = img.resize((100, 100), Image.ANTIALIAS)
photoImg =  ImageTk.PhotoImage(img)
b = Button(master,image=photoImg, command=callback, text="OK", compound=RIGHT)
b.pack()

mainloop()
