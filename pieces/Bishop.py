import Piece

class Bishop(Piece):
    movementRule

    def __init__(self, position = None, idNumber, color, movementRule = None):
        Piece.__init__(self, position, idNumber, color)
        self.movementRule = movementRule