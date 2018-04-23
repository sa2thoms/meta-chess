from tkinter import *

canvasSize = 800


colours = ("#EADDC5", "#BA893C")
squares = 8
ratio = 1/squares

master = Tk()

w = Canvas(master, 
           width=canvasSize, 
           height=canvasSize)
w.pack()

for i in range(squares):
    for j in range(squares):
        fillchoice = colours[(i+j)%2]
        m = ratio*canvasSize
        
        w.create_rectangle(i*m, j*m,(i+1)*m,(j+1)*m, fill=fillchoice)


mainloop()
