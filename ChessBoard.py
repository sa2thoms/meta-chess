from tkinter import *
from pieces.Piece import Piece
from Square import Square
from pieceImages import pieceImages
from color import squareColors, BLACK, WHITE
from Ai import Ai
from MoveRecord import MoveRecord

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

class ChessBoard:

    SQUARES = 8
    RATIO = 1/SQUARES
    CANVAS_SIZE = 640
    M = RATIO*CANVAS_SIZE
    RANKS = ['A','B','C','D','E','F','G','H']

    def __init__(self, master, myGame):

        self.master = master
        self.myGame = myGame
        self.colours = squareColors.SQUARE_COLORS
        self.hColours = squareColors.SQUARE_HIGHLIGHTS

    def printSquares(self):

        M = ChessBoard.M

        self.myframe = Frame(self.master)
        self.myframe.pack(fill=BOTH, expand=YES)

        self.myCanvas = ResizingCanvas(self.myframe, 
                        width=ChessBoard.CANVAS_SIZE, 
                        height=ChessBoard.CANVAS_SIZE, highlightthickness=0)
        self.myCanvas.pack(fill=BOTH, expand=YES)

        self.blackKing = PhotoImage(file = pieceImages.bKImage)
        self.blackQueen = PhotoImage(file = pieceImages.bQImage)
        self.blackBishop = PhotoImage(file = pieceImages.bBImage)
        self.blackKnight = PhotoImage(file = pieceImages.bNImage)
        self.blackRook = PhotoImage(file = pieceImages.bRImage)
        self.blackPawn = PhotoImage(file = pieceImages.bPImage)
        self.whiteKing = PhotoImage(file = pieceImages.wKImage)
        self.whiteQueen = PhotoImage(file = pieceImages.wQImage)
        self.whiteBishop = PhotoImage(file = pieceImages.wBImage)
        self.whiteKnight = PhotoImage(file = pieceImages.wNImage)
        self.whiteRook = PhotoImage(file = pieceImages.wRImage)
        self.whitePawn = PhotoImage(file = pieceImages.wPImage)


        for i in range(ChessBoard.SQUARES):
            for j in range(ChessBoard.SQUARES):
                label = ChessBoard.RANKS[i]+str(8-j)
                fillchoice = self.colours[(i+j)%2]
                self.myCanvas.create_rectangle(i*M, (j)*M,(i+1)*M,(j+1)*M, fill=fillchoice, tag=label)

        self.myCanvas.addtag_all("all")
        self.myCanvas.itemconfig("B6",fill = self.hColours[0])

        self.myCanvas.bind('<Button-1>', self.aiMakeMove)


    def aiMakeMove(self, event):
        ai = Ai(3)
        print(self.myGame.move(ai.bestMove(self.myGame)))
        self.mapPieces()


    def mapPieces(self):

        M = ChessBoard.M

        #return to original square colours
        for i in range(ChessBoard.SQUARES):
            for j in range(ChessBoard.SQUARES):
                label = ChessBoard.RANKS[i]+str(8-j)
                fillchoice = self.colours[(i+j)%2]
                self.myCanvas.itemconfig(label, fill = fillchoice)

        #highlight move squares from most recent move
        if (len(self.myGame.moveHistory) == 0):
            print("no moves made")
        else:
            thisMoveRecord = self.myGame.moveHistory[len(self.myGame.moveHistory)-1]
            start = thisMoveRecord.move.start
            end = thisMoveRecord.move.end
            startLabel = str(start)
            endLabel = str(end)
            startFill = self.hColours[(start.file + start.rank+1)%2]
            endFill = self.hColours[(end.file + end.rank+1)%2]
            self.myCanvas.itemconfig(startLabel, fill = startFill)
            self.myCanvas.itemconfig(endLabel, fill = endFill)
        
        #delete pieces
        self.myCanvas.delete("pieces")

        #remap pieces based on current game state
        for i in range(ChessBoard.SQUARES):
            for j in range(ChessBoard.SQUARES):
                thisPiece = self.myGame.getPiece(Square(i,j))
                if (thisPiece):
                    if (thisPiece.color == BLACK):
                        if (thisPiece.symbol == 'pa'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.blackPawn, tag = ("bP","pieces"))
                        if (thisPiece.symbol == 'ro'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.blackRook, tag=("bR","pieces"))
                        if (thisPiece.symbol == 'kn'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.blackKnight, tag=("bN","pieces"))
                        if (thisPiece.symbol == 'bi'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.blackBishop, tag=("bB","pieces"))
                        if (thisPiece.symbol == 'Qu'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.blackQueen, tag=("bQ","pieces"))
                        if (thisPiece.symbol == 'Ki'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.blackKing, tag=("bK","pieces"))
                    if (thisPiece.color == WHITE):
                        if (thisPiece.symbol == 'pa'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.whitePawn, tag = ("wP","pieces"))
                        if (thisPiece.symbol == 'ro'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.whiteRook, tag=("wR","pieces"))
                        if (thisPiece.symbol == 'kn'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.whiteKnight, tag=("wN","pieces"))
                        if (thisPiece.symbol == 'bi'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.whiteBishop, tag=("wB","pieces"))
                        if (thisPiece.symbol == 'Qu'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.whiteQueen, tag=("wQ","pieces"))
                        if (thisPiece.symbol == 'Ki'):
                            self.myCanvas.create_image(i*M+M/2, (7-j)*M+M/2, image = self.whiteKing, tag=("wK","pieces"))        
        self.myCanvas.addtag_all("all")  

