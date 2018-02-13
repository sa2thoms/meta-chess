from pieces.Piece import Piece

class Pawn(Piece):

    def __init__(self, position, idNumber, color, symbol='pa'):
        Piece.__init__(self, position, idNumber, color, symbol)