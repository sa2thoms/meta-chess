from pieces.Piece import Piece
from pieces.Pawn import Pawn
from pieces.King import King
from pieces.Queen import Queen
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop

class MoveRecord:

    def __init__(self, move, pieceInMotion, pieceTaken = None, piecePromotedTo = None, castleMove = None):
        self.move = move
        self.pieceInMotion = pieceInMotion
        self.pieceTaken = pieceTaken
        self.piecePromotedTo = piecePromotedTo
        self.castleMove = castleMove
    
    def fullCopy(self, piece_map):
        # note that piece_map must be a dictionary mapping the old pieces to the new pieces
        new_pieceInMotion = piece_map[self.pieceInMotion]
        new_pieceTaken = None if not (self.pieceTaken in piece_map) else piece_map[self.pieceTaken]
        new_piecePromotedTo = None if not (self.piecePromotedTo in piece_map) else piece_map[self.piecePromotedTo]
        
        new_castleMove = None
        if self.castleMove:
            new_castleMove = self.castleMove.fullCopy(piece_map)

        return MoveRecord(self.move.fullCopy(), new_pieceInMotion, new_pieceTaken, new_piecePromotedTo, new_castleMove)
