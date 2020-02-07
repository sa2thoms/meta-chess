from tkinter import *
import NormalChessConfig
import SimonsChessConfig
from Game import Game
from ChessBoard import ChessBoard

def promoCallback():
    return 'q' #this means a pawn always promotes to a queen upon reaching the other side of the board

# this is your instance of the game object, and it now has standard rules
myGame = Game(NormalChessConfig.ruleSet, promoCallback)

# myGame will not have any pieces until you call load on it
myGame.load()

master = Tk()
myChessBoard = ChessBoard(master, myGame)
myChessBoard.printSquares()
myChessBoard.setUpPieces()
myChessBoard.reMapPieces()
master.mainloop()