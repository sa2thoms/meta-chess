import pieces.Piece

class Bishop(Piece):
    movementRule

    def __init__(self, position, idNumber, color, symbol='bi', movementRule = None):
        Piece.__init__(self, position, idNumber, color, symbol)
        self.movementRule = movementRule