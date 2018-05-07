from tkinter import *

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        scale = float(event.width)/self.width
        self.width = event.width
        self.height = event.width
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,scale,scale)


canvasSize = 800

colours = ("#EADDC5", "#BA893C")
squares = 8
ratio = 1/squares

master = Tk()
myframe = Frame(master)
myframe.pack(fill=BOTH, expand=YES)

w = ResizingCanvas(myframe, 
           width=canvasSize, 
           height=canvasSize, highlightthickness=0)
w.pack(fill=BOTH, expand=YES)

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
        w.create_rectangle(i*m, j*m,(i+1)*m,(j+1)*m, fill=fillchoice, tag="squares")


row = 0
w.create_image(0*m+m/2, row*m+m/2, image = blackRook, tag="bR")
w.create_image(1*m+m/2, row*m+m/2, image = blackKnight, tag="bN")
w.create_image(2*m+m/2, row*m+m/2, image = blackBishop, tag="bB")
w.create_image(3*m+m/2, row*m+m/2, image = blackKing, tag="bK")
w.create_image(4*m+m/2, row*m+m/2, image = blackQueen, tag="bQ")
w.create_image(5*m+m/2, row*m+m/2, image = blackBishop, tag="bB")
w.create_image(6*m+m/2, row*m+m/2, image = blackKnight, tag="bN")
w.create_image(7*m+m/2, row*m+m/2, image = blackRook, tag="bR")
for j in range (squares):
    w.create_image(j*m+m/2, (row+1)*m+m/2, image = blackPawn, tag = "bP")

row = 7
w.create_image(0*m+m/2, row*m+m/2, image = whiteRook, tag="bR")
w.create_image(1*m+m/2, row*m+m/2, image = whiteKnight, tag="bN")
w.create_image(2*m+m/2, row*m+m/2, image = whiteBishop, tag="bB")
w.create_image(3*m+m/2, row*m+m/2, image = whiteKing, tag="bK")
w.create_image(4*m+m/2, row*m+m/2, image = whiteQueen, tag="bQ")
w.create_image(5*m+m/2, row*m+m/2, image = whiteBishop, tag="bB")
w.create_image(6*m+m/2, row*m+m/2, image = whiteKnight, tag="bN")
w.create_image(7*m+m/2, row*m+m/2, image = whiteRook, tag="bR")
for j in range (squares):
    w.create_image(j*m+m/2, (row-1)*m+m/2, image = whitePawn, tag="bP")

w.addtag_all("all")

mainloop()
