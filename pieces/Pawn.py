from pieces.Piece import Piece

class Pawn(Piece):

    def __init__(self, position, color, symbol='pa'):
        Piece.__init__(self, position, color, symbol)