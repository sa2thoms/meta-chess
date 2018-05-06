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

blackKing = PhotoImage(file = "images/bK.gif")
blackQueen = PhotoImage(file = "images/bQ.gif")
blackBishop = PhotoImage(file = "images/bB.gif")
blackKnight = PhotoImage(file = "images/bN.gif")
blackRook = PhotoImage(file = "images/bR.gif")
blackPawn = PhotoImage(file = "images/bP.gif")
whiteKing = PhotoImage(file = "images/wK.gif")
whiteQueen = PhotoImage(file = "images/wQ.gif")
whiteBishop = PhotoImage(file = "images/wB.gif")
whiteKnight = PhotoImage(file = "images/wN.gif")
whiteRook = PhotoImage(file = "images/wR.gif")
whitePawn = PhotoImage(file = "images/wP.gif")

m = ratio*canvasSize

for i in range(squares):
    for j in range(squares):
        fillchoice = colours[(i+j)%2]
        w.create_rectangle(i*m, j*m,(i+1)*m,(j+1)*m, fill=fillchoice)


row = 0
w.create_image(0*m+m/2, row*m+m/2, image = blackRook)
w.create_image(1*m+m/2, row*m+m/2, image = blackKnight)
w.create_image(2*m+m/2, row*m+m/2, image = blackBishop)
w.create_image(3*m+m/2, row*m+m/2, image = blackKing)
w.create_image(4*m+m/2, row*m+m/2, image = blackQueen)
w.create_image(5*m+m/2, row*m+m/2, image = blackBishop)
w.create_image(6*m+m/2, row*m+m/2, image = blackKnight)
w.create_image(7*m+m/2, row*m+m/2, image = blackRook)
for j in range (squares):
    w.create_image(j*m+m/2, (row+1)*m+m/2, image = blackPawn)

row = 7
w.create_image(0*m+m/2, row*m+m/2, image = whiteRook)
w.create_image(1*m+m/2, row*m+m/2, image = whiteKnight)
w.create_image(2*m+m/2, row*m+m/2, image = whiteBishop)
w.create_image(3*m+m/2, row*m+m/2, image = whiteKing)
w.create_image(4*m+m/2, row*m+m/2, image = whiteQueen)
w.create_image(5*m+m/2, row*m+m/2, image = whiteBishop)
w.create_image(6*m+m/2, row*m+m/2, image = whiteKnight)
w.create_image(7*m+m/2, row*m+m/2, image = whiteRook)
for j in range (squares):
    w.create_image(j*m+m/2, (row-1)*m+m/2, image = whitePawn)


mainloop()
