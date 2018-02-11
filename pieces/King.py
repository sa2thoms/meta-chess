import Piece

class King(Piece):
    def __init__(self, position = None, idNumber, color):
        Piece.__init__(self, position, idNumber, color)
        