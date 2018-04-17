from pieces.Piece import Piece
from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop

class MoveRecord:

    def __init__(self, move, pieceInMotion, pieceTaken = None, piecePromotedTo = None):
        self.move = move
        self.pieceInMotion = pieceInMotion
        self.pieceTaken = pieceTaken
        self.piecePromotedTo = piecePromotedTo
