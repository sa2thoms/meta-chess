from tkinter import *
from pieces.Piece import Piece
from Square import Square
from pieceImages import pieceImages
from Move import Move
from color import squareColors, BLACK, WHITE
from Ai import Ai
from MoveRecord import MoveRecord
from IllegalMoveException import IllegalMoveException

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
    BOARD_SIZE = 640
    DIM = BOARD_SIZE/SQUARES
    BUTTON_SPACER = 0.2 #percentage of chessboard
    BOARD_SPACER = 0.02 #percentage of chessboard
    ASPECT_RATIO = (BOARD_SIZE + 2*BOARD_SPACER*BOARD_SIZE + DIM/2 )/BOARD_SIZE

    def __init__(self, master, myGame):
        self.master = master
        self.myGame = myGame
        self.colours = squareColors.SQUARE_COLORS
        self.hColours = squareColors.SQUARE_HIGHLIGHTS

    def printSquares(self):
        DIM = ChessBoard.DIM
        boardSpacer = ChessBoard.BOARD_SPACER*ChessBoard.BOARD_SIZE
        width = ChessBoard.BOARD_SIZE + 2*boardSpacer
        height = ChessBoard.BOARD_SIZE * ChessBoard.ASPECT_RATIO
        files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.myCanvas = ResizingCanvas(self.master, width=width, 
                        height=height, highlightthickness=0)
        self.myCanvas.pack(fill=BOTH, expand=YES)
        self.myCanvas.tagException = False
        #print file labels
        xloc = boardSpacer + DIM/2
        yloc = boardSpacer/2
        for file in range(ChessBoard.SQUARES):
            self.myCanvas.create_text(xloc + file*DIM, yloc, text = files[file], 
                font = ("Courier", 12))
        yloc = 3*boardSpacer/2 + ChessBoard.BOARD_SIZE
        for file in range(ChessBoard.SQUARES):
            self.myCanvas.create_text(xloc + file*DIM, yloc, text = files[file], 
                font = ("Courier", 12))
        #print rank labels
        xloc = boardSpacer/2
        yloc = boardSpacer + DIM/2
        for rank in range(ChessBoard.SQUARES):
            self.myCanvas.create_text(xloc, yloc+(7-rank)*DIM, text = str(rank+1), 
                font = ("Courier", 12))
        xloc = 3*boardSpacer/2 + ChessBoard.BOARD_SIZE
        for rank in range(ChessBoard.SQUARES):
            self.myCanvas.create_text(xloc, yloc+(7-rank)*DIM, text = str(rank+1), 
                font = ("Courier", 12))
        #print squares
        for file in range(ChessBoard.SQUARES):
            for rank in range(ChessBoard.SQUARES):
                label = str(Square(file, rank))
                fillchoice = self.colours[(file+rank+1)%2]
                xloc = file*DIM + boardSpacer
                yloc = (7-rank)*DIM + boardSpacer
                self.myCanvas.create_rectangle(xloc, yloc, xloc+DIM, yloc+DIM, fill=fillchoice, 
                    tag=label)
        #print buttons
        xloc = ChessBoard.BOARD_SIZE * ChessBoard.BUTTON_SPACER + boardSpacer
        yloc = ChessBoard.BOARD_SIZE + 3*boardSpacer
        self.aiButton = self.myCanvas.create_rectangle(xloc, yloc, xloc+2*DIM, yloc+DIM/2, 
            fill = self.colours[1], tag = "aiTurn")
        self.myCanvas.create_text(xloc+DIM, yloc+DIM/4, text = "AI's turn", font = ("Courier", 12), 
            tag = "aiTurn")
        xloc = ChessBoard.BOARD_SIZE*(1 - ChessBoard.BUTTON_SPACER) - 2*DIM + boardSpacer
        self.undoButton = self.myCanvas.create_rectangle(xloc, yloc, xloc+2*DIM, yloc+DIM/2, 
            fill = self.colours[1], tag = "undo")
        self.myCanvas.create_text(xloc+DIM, yloc+DIM/4, text = "undo", font = ("Courier", 12), 
            tag = "undo")
        self.myCanvas.addtag_all("all")
        self.myCanvas.tag_bind("aiTurn", '<Button-1>', self.aiMakeMove)
        self.myCanvas.tag_bind("undo", '<Button-1>', self.undoLastMove)

    def aiMakeMove(self, event):
        if self.myCanvas.tagException == False:
            ai = Ai(3)
            message = self.myGame.move(ai.bestMove(self.myGame))
            print(message)
            if message == "check":
                self.gameStateWindow(message)
            self.reMapPieces()

    def undoLastMove(self, event):
        if self.myCanvas.tagException == False:
            print(self.myGame.undoLastMove())
            self.reMapPieces()

    def playerStartMove(self, event):
        if self.myCanvas.tagException == False:
            self.currentX = event.x
            self.currentY = event.y
            self.dragItem = self.myCanvas.find_closest(event.x, event.y)[0]
            squareSize = self.myCanvas.currentScale*ChessBoard.BOARD_SIZE/ChessBoard.SQUARES
            rank = 7-int( event.y / squareSize)
            file = int (event.x / squareSize)
            self.startSquare = Square(file, rank)

    def playerDraggingMove(self, event):
        if self.myCanvas.tagException == False:
            self.myCanvas.move(self.dragItem,event.x-self.currentX, event.y-self.currentY)
            self.currentX = event.x
            self.currentY = event.y
        
    def playerMakeMove(self, event):
        if self.myCanvas.tagException == False:
            boardSpacer = ChessBoard.BOARD_SIZE*ChessBoard.BOARD_SPACER
            boardSize = self.myCanvas.currentScale*ChessBoard.BOARD_SIZE*(1+2*ChessBoard.BOARD_SPACER)
            squareSize = boardSize/ChessBoard.SQUARES
            xloc = 1.5*squareSize
            yloc = 3.5*squareSize
            rank = 7-int( event.y / squareSize)
            file = int (event.x / squareSize)
            self.endSquare = Square(file, rank)
            if self.endSquare != self.startSquare:
                try:
                    message = self.myGame.move(Move(self.startSquare, self.endSquare))
                    print(message)
                    if message == 'check':
                        self.gameStateWindow(message)
                except IllegalMoveException as e:
                    self.myCanvas.create_rectangle(xloc, yloc, boardSize-xloc, boardSize - yloc, 
                        fill = self.colours[1], width = 5, tag = "exception")
                    self.myCanvas.create_text(boardSize/2, boardSize/2-2*boardSpacer, 
                        text = str(e) + ", try again", 
                        font = ("Courier", 12), tag = "exception")
                    self.myCanvas.create_text(boardSize/2, boardSize/2+2*boardSpacer, 
                        text = "click to dismiss", 
                        font = ("Courier", 12), tag = "exception")
                    popUpTag = "exception"
                    self.myCanvas.tag_bind(popUpTag, '<Button-1>', 
                        lambda event: self.removePopUp(event,popUpTag))
                    self.myCanvas.tagException = True
                    print('\nThat move is not legal: ' + str(e) + '. Try again: ', end="")
            self.reMapPieces()

    def gameStateWindow(self, message):
        boardSpacer = ChessBoard.BOARD_SIZE*ChessBoard.BOARD_SPACER
        boardSize = self.myCanvas.currentScale*ChessBoard.BOARD_SIZE*(1+2*ChessBoard.BOARD_SPACER)
        squareSize = boardSize/ChessBoard.SQUARES
        xloc = 2.5*squareSize
        yloc = 3.5*squareSize
        self.myCanvas.create_rectangle(xloc, yloc, boardSize-xloc, boardSize - yloc, 
                        fill = self.colours[1], width = 5, tag = "game_state")
        self.myCanvas.create_text(boardSize/2, boardSize/2-boardSpacer, 
                        text = message +'!', 
                        font = ("Courier", 16), tag = "game_state")
        self.myCanvas.create_text(boardSize/2, boardSize/2+2*boardSpacer, 
                        text = "click to dismiss", 
                        font = ("Courier", 12), tag = "game_state")
        popUpTag = "game_state"
        self.myCanvas.tag_bind(popUpTag, '<Button-1>', 
            lambda event: self.removePopUp(event, popUpTag))
        self.myCanvas.tagException = True

    def removePopUp(self, event, tag):
        self.myCanvas.tagException = False
        self.myCanvas.delete(tag)

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
        boardSpacer = ChessBoard.BOARD_SPACER*ChessBoard.BOARD_SIZE
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
        fileNames = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for file in range(ChessBoard.SQUARES):
            for rank in range(ChessBoard.SQUARES):
                thisPiece = self.myGame.getPiece(Square(file,rank))
                filePosition = boardSpacer+(file*DIM+DIM/2)*self.myCanvas.currentScale
                rankPosition = boardSpacer+((7-rank)*DIM+DIM/2)*self.myCanvas.currentScale
                if (thisPiece):
                    label = 'piece'+fileNames[file]+str(rank+1)
                    if (thisPiece.color == BLACK):
                        if (thisPiece.symbol == 'pa'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.blackPawn, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'ro'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.blackRook, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'kn'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.blackKnight, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'bi'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.blackBishop, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'Qu'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.blackQueen, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'Ki'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.blackKing, tag = (label, "pieces"))
                    if (thisPiece.color == WHITE):
                        if (thisPiece.symbol == 'pa'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.whitePawn, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'ro'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.whiteRook, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'kn'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.whiteKnight, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'bi'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.whiteBishop, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'Qu'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.whiteQueen, tag = (label, "pieces"))
                        if (thisPiece.symbol == 'Ki'):
                            self.myCanvas.create_image(filePosition, rankPosition, 
                                            image = self.whiteKing, tag = (label, "pieces"))        
                self.myCanvas.tag_bind(label, '<Button-1>', self.playerStartMove)
                self.myCanvas.tag_bind(label, '<B1-Motion>', self.playerDraggingMove)
                self.myCanvas.tag_bind(label, '<ButtonRelease-1>', self.playerMakeMove)
        self.myCanvas.addtag_all("all")
        lowerList = ['pieceB4', 'pieceC4', 'pieceD4', 'pieceE4', 'pieceF4', 'pieceG4', 
                    'pieceB5', 'pieceC5', 'pieceD5', 'pieceE5', 'pieceF5', 'pieceG5']
        for item in lowerList:
            if bool(self.myCanvas.find_withtag(item)):
                self.myCanvas.tag_raise("exception",item)
                self.myCanvas.tag_raise("game_state",item) 

