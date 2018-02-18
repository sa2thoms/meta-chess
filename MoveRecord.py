from pieces.Piece import Piece
from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop

class MoveRecord:

    def __init__(self, startPosition, endPosition, pieceInMotion, pieceTaken = None):
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.pieceInMotion = pieceInMotion
        self.pieceTaken = pieceTaken