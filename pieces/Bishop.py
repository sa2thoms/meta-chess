import Piece

class Bishop(Piece):
    movementRule

    def __init__(self, position = None, idNumber, movementRule = None):
        Piece.__init__(self, position, idNumber)
        self.movementRule = movementRule