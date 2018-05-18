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
        self.originalWidth = self.width
        self.currentScale = self.width/self.originalWidth

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        scale = float(event.width)/self.width
        self.width = event.width
        self.height = event.width*ChessBoard.ASPECT_RATIO
        self.currentScale = self.width/self.originalWidth
        # resize the canvas 
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,scale,scale)

class ChessBoard:

    SQUARES = 8
    CANVAS_SIZE = 640
    DIM = CANVAS_SIZE/SQUARES
    AI_OVER = 0.2 #percentage of chessboard
    AI_DOWN = 0.02 #percentage of chessboard
    ASPECT_RATIO = (CANVAS_SIZE*(1+(2*AI_DOWN))+DIM/2)/CANVAS_SIZE

    def __init__(self, master, myGame):
        self.master = master
        self.myGame = myGame
        self.colours = squareColors.SQUARE_COLORS
        self.hColours = squareColors.SQUARE_HIGHLIGHTS

    def printSquares(self):
        DIM = ChessBoard.DIM
        width = ChessBoard.CANVAS_SIZE
        height = ChessBoard.CANVAS_SIZE * ChessBoard.ASPECT_RATIO
        self.myCanvas = ResizingCanvas(self.master, width=width, 
                        height=height, highlightthickness=0)
        self.myCanvas.pack(fill=BOTH, expand=YES)
        for file in range(ChessBoard.SQUARES):
            for rank in range(ChessBoard.SQUARES):
                label = str(Square(file, rank))
                fillchoice = self.colours[(file+rank+1)%2]
                self.myCanvas.create_rectangle(file*DIM, (7-rank)*DIM,(file+1)*DIM,(8-rank)*DIM, fill=fillchoice, tag=label)
        xloc = ChessBoard.CANVAS_SIZE*ChessBoard.AI_OVER
        yloc = ChessBoard.CANVAS_SIZE*(1+ChessBoard.AI_DOWN)
        self.aiButton = self.myCanvas.create_rectangle(xloc, yloc, xloc+2*DIM, yloc+DIM/2, fill = self.colours[1], tag = "aiTurn")
        self.myCanvas.create_text(xloc+DIM, yloc+DIM/4, text = "AI's turn", font = ("Courier", 12), tag = "aiTurn")
        self.myCanvas.addtag_all("all")
        self.myCanvas.tag_bind("aiTurn", '<Button-1>', self.aiMakeMove)

    def aiMakeMove(self, event):
        ai = Ai(3)
        print(self.myGame.move(ai.bestMove(self.myGame)))
        self.reMapPieces()

    def playerStartMove(self, event):
        self.currentX = event.x
        self.currentY = event.y
        self.dragItem = self.myCanvas.find_closest(event.x, event.y)[0]
        squareSize = self.myCanvas.currentScale*ChessBoard.CANVAS_SIZE/ChessBoard.SQUARES
        rank = 7-int( event.y / squareSize)
        file = int (event.x / squareSize)
        self.startSquare = Square(file, rank)

    def playerDraggingMove(self, event):
        self.myCanvas.move(self.dragItem,event.x-self.currentX, event.y-self.currentY)
        self.currentX = event.x
        self.currentY = event.y
        
    def playerMakeMove(self, event):
        squareSize = self.myCanvas.currentScale*ChessBoard.CANVAS_SIZE/ChessBoard.SQUARES
        rank = 7-int( event.y / squareSize)
        file = int (event.x / squareSize)
        self.endSquare = Square(file, rank)
        print(self.myGame.move(self.startSquare, self.endSquare))
        self.reMapPieces()

    def setUpPieces(self):
        DIM = ChessBoard.DIM
        self.blackKing = PhotoImage(file = pieceImages.bKiImage)
        self.blackQueen = PhotoImage(file = pieceImages.bQuImage)
        self.blackBishop = PhotoImage(file = pieceImages.bbiImage)
        self.blackKnight = PhotoImage(file = pieceImages.bknImage)
        self.blackRook = PhotoImage(file = pieceImages.broImage)
        self.blackPawn = PhotoImage(file = pieceImages.bpaImage)
        self.whiteKing = PhotoImage(file = pieceImages.wKiImage)
        self.whiteQueen = PhotoImage(file = pieceImages.wQuImage)
        self.whiteBishop = PhotoImage(file = pieceImages.wbiImage)
        self.whiteKnight = PhotoImage(file = pieceImages.wknImage)
        self.whiteRook = PhotoImage(file = pieceImages.wroImage)
        self.whitePawn = PhotoImage(file = pieceImages.wpaImage)      

    def reMapPieces(self):
        DIM = ChessBoard.DIM
        #return to original square colours
        for file in range(ChessBoard.SQUARES):
            for rank in range(ChessBoard.SQUARES):
                label = str(Square(file, rank))
                fillchoice = self.colours[(file + rank + 1)%2]
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
            startFill = self.hColours[(start.file + start.rank + 1)%2]
            endFill = self.hColours[(end.file + end.rank + 1)%2]
            self.myCanvas.itemconfig(startLabel, fill = startFill)
            self.myCanvas.itemconfig(endLabel, fill = endFill)
        
        #delete pieces
        self.myCanvas.delete("pieces")

        #remap pieces based on current game state
        bpIndex = 0
        brIndex = 0
        bbIndex = 0
        bnIndex = 0
        wpIndex = 0
        wrIndex = 0
        wbIndex = 0
        wnIndex = 0
        for file in range(ChessBoard.SQUARES):
            for rank in range(ChessBoard.SQUARES):
                thisPiece = self.myGame.getPiece(Square(file,rank))
                filePosition = (file*DIM+DIM/2)*self.myCanvas.currentScale
                rankPosition = ((7-rank)*DIM+DIM/2)*self.myCanvas.currentScale
                if (thisPiece):
                    if (thisPiece.color == BLACK):
                        if (thisPiece.symbol == 'pa'):
                            label = "bp"+str(bpIndex)
                            bpIndex += 1
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.blackPawn, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'ro'):
                            label = "br"+str(brIndex)
                            brIndex += 1
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.blackRook, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'kn'):
                            label = "bn"+str(bnIndex)
                            bnIndex += 1
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.blackKnight, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'bi'):
                            label = "bb"+str(bbIndex)
                            bbIndex += 1
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.blackBishop, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'Qu'):
                            label = "bq"
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.blackQueen, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'Ki'):
                            label = "bk"
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.blackKing, tag=(label,"pieces"))
                    if (thisPiece.color == WHITE):
                        if (thisPiece.symbol == 'pa'):
                            label = "wp"+str(wpIndex)
                            wpIndex += 1
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.whitePawn, tag = (label,"pieces"))
                        if (thisPiece.symbol == 'ro'):
                            label = "wr"+str(wrIndex)
                            wrIndex += 1
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.whiteRook, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'kn'):
                            label = "wn"+str(wnIndex)
                            wnIndex += 1
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.whiteKnight, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'bi'):
                            label = "wb"+str(wbIndex)
                            wbIndex += 1
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.whiteBishop, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'Qu'):
                            label = "wq"
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.whiteQueen, tag=(label,"pieces"))
                        if (thisPiece.symbol == 'Ki'):
                            label = "wk"
                            self.myCanvas.create_image(filePosition, rankPosition, image = self.whiteKing, tag=(label,"pieces"))        
                self.myCanvas.tag_bind(label, '<Button-1>', self.playerStartMove)
                self.myCanvas.tag_bind(label, '<B1-Motion>', self.playerDraggingMove)
                self.myCanvas.tag_bind(label, '<ButtonRelease-1>', self.playerMakeMove)
        self.myCanvas.addtag_all("all")  

