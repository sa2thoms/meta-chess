from tkinter import *
#import NormalChessConfig
#from Game import Game
from pieces.Piece import Piece
from Square import Square

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

#def promoCallback():
#    return 'q' #this means a pawn always promotes to a queen upon reaching the other side of the board

# this is your instance of the game object, and it now has standard rules
#myGame = Game(NormalChessConfig.ruleSet, promoCallback)

# myGame will not have any pieces until you call load on it
#myGame.load()

class ChessBoard:

    def __init__(self, master, myGame):

        self.master = master
        self.myGame = myGame

        canvasSize = 800
        colours = ("#EADDC5", "#BA893C")
        squares = 8
        ratio = 1/squares
        m = ratio*canvasSize
        
        self.myframe = Frame(master)
        self.myframe.pack(fill=BOTH, expand=YES)

        self.myCanvas = ResizingCanvas(self.myframe, 
                    width=canvasSize, 
                    height=canvasSize, highlightthickness=0)
        self.myCanvas.pack(fill=BOTH, expand=YES)

        self.blackKing = PhotoImage(file = "images/bK.gif")
        self.blackQueen = PhotoImage(file = "images/bQ.gif")
        self.blackBishop = PhotoImage(file = "images/bB.gif")
        self.blackKnight = PhotoImage(file = "images/bN.gif")
        self.blackRook = PhotoImage(file = "images/bR.gif")
        self.blackPawn = PhotoImage(file = "images/bP.gif")
        self.whiteKing = PhotoImage(file = "images/wK.gif")
        self.whiteQueen = PhotoImage(file = "images/wQ.gif")
        self.whiteBishop = PhotoImage(file = "images/wB.gif")
        self.whiteKnight = PhotoImage(file = "images/wN.gif")
        self.whiteRook = PhotoImage(file = "images/wR.gif")
        self.whitePawn = PhotoImage(file = "images/wP.gif")

        for i in range(squares):
            for j in range(squares):
                fillchoice = colours[(i+j)%2]
                self.myCanvas.create_rectangle(i*m, j*m,(i+1)*m,(j+1)*m, fill=fillchoice, tag="squares")
                thisPiece = myGame.getPiece(Square(i,j))
                if (thisPiece):
                    if (thisPiece.color == 0):
                        if (thisPiece.symbol == 'pa'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.blackPawn, tag = "bP")
                        if (thisPiece.symbol == 'ro'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.blackRook, tag="bR")
                        if (thisPiece.symbol == 'kn'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.blackKnight, tag="bN")
                        if (thisPiece.symbol == 'bi'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.blackBishop, tag="bB")
                        if (thisPiece.symbol == 'Qu'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.blackQueen, tag="bQ")
                        if (thisPiece.symbol == 'Ki'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.blackKing, tag="bK")
                    if (thisPiece.color == 1):
                        if (thisPiece.symbol == 'pa'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.whitePawn, tag = "bP")
                        if (thisPiece.symbol == 'ro'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.whiteRook, tag="bR")
                        if (thisPiece.symbol == 'kn'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.whiteKnight, tag="bN")
                        if (thisPiece.symbol == 'bi'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.whiteBishop, tag="bB")
                        if (thisPiece.symbol == 'Qu'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.whiteQueen, tag="bQ")
                        if (thisPiece.symbol == 'Ki'):
                            self.myCanvas.create_image(i*m+m/2, j*m+m/2, image = self.whiteKing, tag="bK")        
                

        self.myCanvas.addtag_all("all")

